#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 VS Code 的 .vscode/mcp.json 转换成 Antigravity 的 mcp_config.json。

用法：
    python3 scripts/mcp_vscode_to_antigravity.py .vscode/mcp.json -o mcp_config.json
    python3 scripts/mcp_vscode_to_antigravity.py .vscode/mcp.json --install   # 直接写入 Antigravity 全局配置（会先备份）

转换规则：
    servers            -> mcpServers
    type: "stdio"      -> 删除（Antigravity 默认 stdio）
    type: http/sse+url -> serverUrl
    ${input:xxx}       -> ${XXX}（环境变量占位），并在末尾提示你需要设置哪些变量
    ${workspaceFolder} -> 展开为绝对路径
    sandboxEnabled / dev / envFile -> 删除（Antigravity 不支持，改用其权限策略）
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

DROP_KEYS = {"type", "sandboxEnabled", "dev", "envFile", "gallery"}
INPUT_RE = re.compile(r"\$\{input:([A-Za-z0-9_\-\.]+)\}")

ANTIGRAVITY_PATHS = [
    Path.home() / ".gemini" / "config" / "mcp_config.json",      # Antigravity 2.0
    Path.home() / ".gemini" / "antigravity" / "mcp_config.json",  # 早期版本
]


def strip_jsonc(text: str) -> str:
    """去掉 // 与 /* */ 注释和尾逗号（字符串内部的 // 不会被误删）。"""
    out = []
    i, n = 0, len(text)
    in_str = False
    while i < n:
        ch = text[i]
        if in_str:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(ch)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def convert_value(val, workspace: str, needed_env: set):
    if isinstance(val, str):
        val = val.replace("${workspaceFolder}", workspace)
        for name in INPUT_RE.findall(val):
            env_name = re.sub(r"[^A-Za-z0-9]", "_", name).upper()
            needed_env.add(env_name)
            val = val.replace("${input:%s}" % name, "${%s}" % env_name)
        return val
    if isinstance(val, list):
        return [convert_value(v, workspace, needed_env) for v in val]
    if isinstance(val, dict):
        return {k: convert_value(v, workspace, needed_env) for k, v in val.items()}
    return val


def convert(src: dict, workspace: str) -> tuple[dict, set, list]:
    servers = src.get("servers") or src.get("mcpServers") or {}
    needed_env: set = set()
    notes: list = []
    out: dict = {}

    for name, cfg in servers.items():
        if not isinstance(cfg, dict):
            continue
        stype = cfg.get("type")
        new: dict = {}
        for k, v in cfg.items():
            if k in DROP_KEYS:
                continue
            if k == "url":
                new["serverUrl"] = convert_value(v, workspace, needed_env)
            else:
                new[k] = convert_value(v, workspace, needed_env)

        if stype in ("http", "sse") and "serverUrl" not in new and "url" in cfg:
            new["serverUrl"] = cfg["url"]

        # Copilot 专属端点在 Antigravity 里不可用
        if str(new.get("serverUrl", "")).startswith("https://api.githubcopilot.com/mcp"):
            notes.append(
                f"[{name}] GitHub Copilot 远程端点绑定 Copilot 订阅认证，Antigravity 无法使用。"
                f"请改用 MCP Store 里的 GitHub，或本地 Docker 版 ghcr.io/github/github-mcp-server + PAT。"
            )
        if "cwd" in new and "${" in str(new["cwd"]):
            notes.append(f"[{name}] cwd 含变量，Antigravity 可能不解析，建议改绝对路径。")
        if new.get("command") in ("npx", "uvx", "node", "python", "python3", "docker"):
            notes.append(
                f"[{name}] command=\"{new['command']}\" 建议改成绝对路径"
                f"（Antigravity 启动时常不继承 shell PATH，会报 executable file not found）。"
            )
        out[name] = new

    return {"mcpServers": out}, needed_env, notes


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def main() -> int:
    ap = argparse.ArgumentParser(description="VS Code mcp.json -> Antigravity mcp_config.json")
    ap.add_argument("src", nargs="?", default=".vscode/mcp.json", help="源文件（默认 .vscode/mcp.json）")
    ap.add_argument("-o", "--out", help="输出文件（默认打印到标准输出）")
    ap.add_argument("--install", action="store_true", help="直接写入 Antigravity 全局配置（自动备份原文件）")
    ap.add_argument("--workspace", default=os.getcwd(), help="用于展开 ${workspaceFolder} 的绝对路径")
    ap.add_argument("--abs-path", action="store_true", help="尝试把 command 自动替换为绝对路径")
    args = ap.parse_args()

    src_path = Path(args.src).expanduser()
    if not src_path.exists():
        print(f"找不到源文件：{src_path}", file=sys.stderr)
        return 1

    data = json.loads(strip_jsonc(src_path.read_text(encoding="utf-8")))
    result, needed_env, notes = convert(data, os.path.abspath(args.workspace))

    if args.abs_path:
        for name, cfg in result["mcpServers"].items():
            cmd = cfg.get("command")
            if cmd and not os.path.isabs(cmd):
                full = which(cmd)
                if full:
                    cfg["command"] = full

    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    target = None
    if args.install:
        target = next((p for p in ANTIGRAVITY_PATHS if p.exists()), ANTIGRAVITY_PATHS[0])
    elif args.out:
        target = Path(args.out).expanduser()

    if target:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            backup = target.with_suffix(f".bak-{datetime.now():%Y%m%d-%H%M%S}.json")
            shutil.copy2(target, backup)
            print(f"已备份原配置 -> {backup}", file=sys.stderr)
        target.write_text(text, encoding="utf-8")
        print(f"已写入 -> {target}", file=sys.stderr)
    else:
        print(text)

    if needed_env:
        print("\n需要预先设置的环境变量（Antigravity 不支持交互式密钥提示）：", file=sys.stderr)
        for e in sorted(needed_env):
            print(f'  export {e}="..."   # 建议写进 ~/.zshrc 或 ~/.bashrc 后重启 Antigravity', file=sys.stderr)
    if notes:
        print("\n提醒：", file=sys.stderr)
        for n in dict.fromkeys(notes):
            print("  - " + n, file=sys.stderr)
    print("\n最后一步：Antigravity → “…” → MCP Servers → Manage MCP Servers → Refresh", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
