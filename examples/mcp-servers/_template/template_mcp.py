#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用 MCP 封装模板
=================

把任意「有 Python API / 有命令行 / 有 COM 自动化接口」的软件包装成 MCP 服务器。
复制此文件改名，按 TODO 填空即可。已在 Orange3 上验证过同样的骨架。

四种封装路径（按优先级）
------------------------
1. Python API   → 直接 import，最干净（Orange3、PyMOL、RDKit、Biopython、scanpy）
2. 命令行 CLI   → subprocess 调用（ImageJ/Fiji、AutoDock Vina、GROMACS、Rscript、pandoc）
3. 本地 REST    → requests 调用（Cytoscape 的 CyREST、ChimeraX 的 remotecontrol）
4. COM 自动化   → pywin32，仅 Windows（Origin、SPSS、Word/Excel、MATLAB）

如果四种都没有（纯 GUI、无任何接口），不要硬封装 —— 那属于 UI 自动化的范畴，
脆弱且难维护，不如让人手工操作。

启动
----
    python template_mcp.py --selftest     # 自检
    python template_mcp.py                # 以 stdio 启动

注册（Antigravity ~/.gemini/config/mcp_config.json）
---------------------------------------------------
    {
      "mcpServers": {
        "my-tool": {
          "command": "C:/绝对路径/python.exe",
          "args": ["E:/mcp-servers/my_tool/template_mcp.py"]
        }
      }
    }
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError as exc:  # pragma: no cover
    sys.stderr.write(
        '无法导入 mcp.server.fastmcp。请安装 "mcp>=1.28,<2"（SDK 2.0 已移除该模块）。\n'
        f"原始错误：{exc}\n"
    )
    raise

# TODO: 改成你的服务器名（会显示在 Agent 的工具列表里）
mcp = FastMCP("my-tool")

# TODO: 若封装的是 CLI 程序，填可执行文件名或绝对路径
EXECUTABLE = "my-cli"

INSTALL_HINT = (
    "未检测到目标软件。请先安装，并确保：\n"
    "  - Python API 型：装在本 MCP 所用的解释器环境里\n"
    "  - CLI 型：可执行文件在 PATH 中，或在本文件里把 EXECUTABLE 改成绝对路径"
)


# --------------------------------------------------------------------------
# 通用辅助
# --------------------------------------------------------------------------


def _ok(**payload: Any) -> dict:
    return {"ok": True, **payload}


def _err(msg: str, **extra: Any) -> dict:
    return {"ok": False, "error": msg, **extra}


def _lazy_import(module_name: str):
    """懒加载：软件没装时给出可读提示，而不是让整个服务器崩溃。"""
    try:
        __import__(module_name)
    except ModuleNotFoundError as exc:
        raise RuntimeError(f"{INSTALL_HINT}\n缺少模块：{module_name}") from exc
    return sys.modules[module_name]


def _run_cli(args: list[str], timeout: int = 300, cwd: str | None = None) -> dict:
    """安全地调用命令行程序：不走 shell，超时可控，返回结构化结果。"""
    exe = shutil.which(EXECUTABLE) or EXECUTABLE
    if not os.path.isabs(exe) and shutil.which(exe) is None:
        return _err(f"找不到可执行文件 '{EXECUTABLE}'。{INSTALL_HINT}")
    try:
        proc = subprocess.run(
            [exe, *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            shell=False,  # 关键：绝不用 shell=True，避免命令注入
        )
    except subprocess.TimeoutExpired:
        return _err(f"执行超时（>{timeout}s）", command=[exe, *args])
    except Exception as exc:
        return _err(f"{type(exc).__name__}: {exc}")
    return _ok(
        returncode=proc.returncode,
        stdout=proc.stdout[-8000:],
        stderr=proc.stderr[-4000:],
        command=[exe, *args],
    )


# --------------------------------------------------------------------------
# 工具定义
#
# 写工具的四条经验：
#   1. docstring 就是 Agent 判断「什么时候调用它」的唯一依据 —— 写清楚用途和参数含义。
#   2. 返回 dict 而不是长字符串，Agent 解析结构化数据准确得多。
#   3. 一个工具做一件事。不要做一个万能的 run_anything(cmd)，那既危险又难用对。
#   4. 写操作必须显式传出路径，绝不默认覆盖文件。
# --------------------------------------------------------------------------


@mcp.tool()
def tool_info() -> dict:
    """检查环境：返回软件版本、解释器路径、可用能力清单。排查问题时先调这个。"""
    info: dict[str, Any] = {
        "python": sys.executable,
        "python_version": sys.version.split()[0],
        "executable_found": shutil.which(EXECUTABLE) is not None,
    }
    # TODO: 若是 Python API 型，在这里检查版本
    # try:
    #     lib = _lazy_import("your_library")
    #     info["library_version"] = lib.__version__
    # except RuntimeError as exc:
    #     return _err(str(exc), **info)
    return _ok(**info)


@mcp.tool()
def analyze(input_path: str, option: str = "default") -> dict:
    """【示例】对输入文件做一次分析并返回结构化结果。

    input_path: 输入文件的绝对路径
    option:     分析模式，可选 default / fast / thorough
    """
    if not os.path.exists(input_path):
        return _err(f"找不到文件：{input_path}")
    if option not in {"default", "fast", "thorough"}:
        return _err(f"未知的 option '{option}'，可选：default / fast / thorough")

    # --- 路径 A：Python API ---
    # try:
    #     lib = _lazy_import("your_library")
    # except RuntimeError as exc:
    #     return _err(str(exc))
    # result = lib.do_something(input_path, mode=option)
    # return _ok(source=input_path, result=result)

    # --- 路径 B：命令行 ---
    return _run_cli(["--input", input_path, "--mode", option])


@mcp.tool()
def export_result(input_path: str, output_path: str, fmt: str = "csv") -> dict:
    """【示例】把分析结果导出到文件。写操作必须显式给出 output_path。"""
    if not os.path.exists(input_path):
        return _err(f"找不到输入文件：{input_path}")
    out_dir = os.path.dirname(os.path.abspath(output_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    res = _run_cli(["--input", input_path, "--out", output_path, "--format", fmt])
    if res.get("ok") and res.get("returncode") == 0:
        res["written"] = os.path.abspath(output_path)
    return res


# --------------------------------------------------------------------------
# 自检与启动
# --------------------------------------------------------------------------


def _selftest() -> int:
    print("=== MCP Server 自检 ===")
    print(f"Python      : {sys.executable}")
    print(f"Python 版本 : {sys.version.split()[0]}")
    try:
        import mcp as _m

        print(f"mcp 版本    : {getattr(_m, '__version__', 'unknown')}")
    except Exception as exc:
        print(f"mcp         : 导入失败 {exc}")
    found = shutil.which(EXECUTABLE)
    print(f"可执行文件  : {found or '未找到 ' + EXECUTABLE}")
    print("\n已注册的 MCP 工具：")
    for name, obj in sorted(globals().items()):
        if callable(obj) and getattr(obj, "__module__", None) == __name__ \
           and not name.startswith("_") and name not in {"main"}:
            doc = (obj.__doc__ or "").strip().splitlines()
            print(f"  - {name:20s} {doc[0] if doc else ''}")
    print("\n自检完成。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
