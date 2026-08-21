#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP 服务器规范检查器
====================

对一个 MCP 服务器源文件做静态检查，验证它是否符合 research-software-to-mcp
skill 里规定的约定。退出码非 0 表示有违规项，可直接接进 CI 或 pre-commit。

用法
----
    python check_mcp_server.py path/to/server.py
    python check_mcp_server.py path/to/server.py --json
    python check_mcp_server.py servers/*.py --strict   # 把 WARN 也当失败

检查项
------
ERROR（必须修）
  E1  依赖未锁 mcp<2（SDK 2.0 移除了 mcp.server.fastmcp）
  E2  subprocess 使用了 shell=True
  E3  subprocess 调用缺少 timeout
  E4  目标库在模块顶层 import（应懒加载）
  E5  存在疑似 shell 透传工具（run/exec/eval 接受任意命令）

WARN（建议修）
  W1  缺少 --selftest 支持
  W2  存在没有 docstring 的 @mcp.tool
  W3  工具 docstring 过短（< 20 字符），Agent 难以判断何时调用
  W4  没有 *_info 类的环境自检工具
  W5  工具数量超过 20 个，会稀释 Agent 注意力
  W6  写文件的工具未见显式 output 参数
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

# 这些是允许在顶层 import 的（标准库 + mcp 本身）
STDLIB_OK = {
    "argparse", "ast", "asyncio", "base64", "collections", "contextlib", "csv",
    "dataclasses", "datetime", "enum", "functools", "glob", "hashlib", "io",
    "itertools", "json", "logging", "math", "os", "pathlib", "re", "shutil",
    "subprocess", "sys", "tempfile", "textwrap", "time", "typing", "uuid",
    "warnings", "mcp", "__future__",
}

SHELL_PASSTHROUGH_NAMES = re.compile(
    r"^(run|exec|execute|eval|shell|cmd|command|run_command|run_shell|bash)$", re.I
)


class Finding:
    def __init__(self, level: str, code: str, msg: str, line: int = 0):
        self.level, self.code, self.msg, self.line = level, code, msg, line

    def as_dict(self) -> dict:
        return {"level": self.level, "code": self.code, "line": self.line, "message": self.msg}

    def __str__(self) -> str:
        loc = f":{self.line}" if self.line else ""
        return f"  [{self.level}] {self.code}{loc}  {self.msg}"


def _is_mcp_tool(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for dec in node.decorator_list:
        target = dec.func if isinstance(dec, ast.Call) else dec
        if isinstance(target, ast.Attribute) and target.attr == "tool":
            return True
        if isinstance(target, ast.Name) and target.id == "tool":
            return True
    return False


def check_file(path: Path) -> list[Finding]:
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return [Finding("ERROR", "E0", f"语法错误：{exc}", getattr(exc, "lineno", 0))]

    out: list[Finding] = []

    # ---- E1: mcp 版本上限 ----
    flat = src.replace(" ", "")
    # 认可的写法： mcp<2 / mcp[cli]<2 / mcp>=1.28,<2 / "mcp>=1.8.0,<2.0"
    has_upper = bool(
        re.search(r"mcp(\[cli\])?(>=[\d.]+,)?<2", flat)
        or re.search(r"mcp(\[cli\])?[<>=!,\d.]*<2", flat)
    )
    if not has_upper:
        out.append(
            Finding(
                "ERROR", "E1",
                '未见 mcp<2 版本约束。SDK 2.0 移除了 mcp.server.fastmcp，'
                '请在依赖声明或文档字符串中写明 mcp>=1.28,<2',
            )
        )

    # ---- 顶层 import 检查（E4）----
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = (
                [a.name.split(".")[0] for a in node.names]
                if isinstance(node, ast.Import)
                else [(node.module or "").split(".")[0]]
            )
            for n in names:
                if n and n not in STDLIB_OK:
                    out.append(
                        Finding(
                            "ERROR", "E4",
                            f"'{n}' 在模块顶层 import。目标库应在函数内懒加载，"
                            f"否则软件未安装时服务器直接崩溃，客户端只显示一行 EOF",
                            node.lineno,
                        )
                    )

    # ---- subprocess 检查（E2 / E3）----
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        is_sub = (
            isinstance(fn, ast.Attribute)
            and fn.attr in {"run", "Popen", "call", "check_output", "check_call"}
            and isinstance(fn.value, ast.Name)
            and fn.value.id == "subprocess"
        )
        if not is_sub:
            continue
        kwargs = {kw.arg: kw.value for kw in node.keywords if kw.arg}
        shell = kwargs.get("shell")
        if isinstance(shell, ast.Constant) and shell.value is True:
            out.append(Finding("ERROR", "E2", "subprocess 使用 shell=True，存在命令注入风险", node.lineno))
        if fn.attr in {"run", "call", "check_output", "check_call"} and "timeout" not in kwargs:
            out.append(Finding("ERROR", "E3", f"subprocess.{fn.attr} 缺少 timeout 参数", node.lineno))

    # ---- 工具级检查 ----
    tools: list[ast.FunctionDef | ast.AsyncFunctionDef] = [
        n for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and _is_mcp_tool(n)
    ]

    if not tools:
        out.append(Finding("WARN", "W0", "未发现任何 @mcp.tool 装饰的函数"))

    for fn in tools:
        doc = ast.get_docstring(fn)
        if not doc:
            out.append(Finding("WARN", "W2", f"工具 '{fn.name}' 没有 docstring，Agent 无法判断何时调用它", fn.lineno))
        elif len(doc.strip()) < 20:
            out.append(Finding("WARN", "W3", f"工具 '{fn.name}' 的 docstring 过短（{len(doc.strip())} 字符）", fn.lineno))

        if SHELL_PASSTHROUGH_NAMES.match(fn.name):
            args = [a.arg for a in fn.args.args]
            if any(a in {"command", "cmd", "shell", "script", "code"} for a in args):
                out.append(
                    Finding("ERROR", "E5",
                            f"'{fn.name}' 疑似 shell 透传工具。一个工具只做一件事，"
                            f"不要暴露任意命令执行", fn.lineno)
                )

        # W6: 看起来会写文件却没有 output 参数
        body_src = ast.get_source_segment(src, fn) or ""
        writes = re.search(r"\bopen\([^)]*['\"][wa]", body_src) or ".to_csv(" in body_src
        has_out = any("out" in a.arg.lower() or "dest" in a.arg.lower() for a in fn.args.args)
        if writes and not has_out:
            out.append(Finding("WARN", "W6", f"工具 '{fn.name}' 似乎会写文件但没有显式的 output 路径参数", fn.lineno))

    if len(tools) > 20:
        out.append(Finding("WARN", "W5", f"共 {len(tools)} 个工具，超过 20 个会稀释 Agent 注意力，考虑拆分服务器"))

    if not any(re.search(r"_info$|^info$|_status$", t.name) for t in tools):
        out.append(Finding("WARN", "W4", "缺少 *_info 环境自检工具，排障时 Agent 无从下手"))

    if "--selftest" not in src and "selftest" not in src:
        out.append(Finding("WARN", "W1", "未提供 --selftest，建议加上以便进客户端前先在终端验证"))

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="MCP 服务器规范检查器")
    ap.add_argument("paths", nargs="+", help="服务器源文件路径")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="把 WARN 也视为失败")
    args = ap.parse_args()

    report: dict[str, list[dict]] = {}
    n_err = n_warn = 0

    for raw in args.paths:
        path = Path(raw)
        if not path.exists():
            print(f"找不到文件：{path}", file=sys.stderr)
            return 2
        findings = check_file(path)
        report[str(path)] = [f.as_dict() for f in findings]
        n_err += sum(1 for f in findings if f.level == "ERROR")
        n_warn += sum(1 for f in findings if f.level == "WARN")

        if not args.json:
            errs = [f for f in findings if f.level == "ERROR"]
            warns = [f for f in findings if f.level == "WARN"]
            status = "FAIL" if errs else ("WARN" if warns else "PASS")
            print(f"\n{path}  [{status}]")
            for f in errs + warns:
                print(f)
            if not findings:
                print("  全部检查项通过")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"\n合计：{n_err} 个 ERROR，{n_warn} 个 WARN")
        if n_err == 0 and n_warn == 0:
            print("符合 research-software-to-mcp 的全部约定。")

    if n_err:
        return 1
    if args.strict and n_warn:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
