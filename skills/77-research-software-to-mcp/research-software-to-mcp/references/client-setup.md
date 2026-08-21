# 客户端注册

## 通用原则

`command` 必须是**绝对路径**，且指向装了目标软件的那个解释器。
Agent IDE 往往不继承 shell 的 PATH，写 `python` 或 `uvx` 经常报
`executable file not found`。

```bash
conda activate orange
where python      # Windows
which python      # macOS / Linux
```

## Antigravity

`~/.gemini/config/mcp_config.json`（2.0）或 `~/.gemini/antigravity/mcp_config.json`（早期版本），
工作区级为 `<项目>/.agents/mcp_config.json`。

```json
{
  "mcpServers": {
    "orange3": {
      "command": "C:/Users/you/miniconda3/envs/orange/python.exe",
      "args": ["E:/mcp-servers/orange3_mcp/orange3_mcp.py"]
    },
    "remote-example": {
      "serverUrl": "https://api.example.com/mcp/",
      "headers": { "Authorization": "Bearer TOKEN" }
    }
  }
}
```

- 顶层键 `mcpServers`
- 远程用 `serverUrl`，不是 `type` + `url`
- 不支持 `${input:...}` 交互式密钥提示；`${ENV}` 解析也不稳，建议写字面值并把文件排除出 Git
- 改完到 Manage MCP Servers 点 Refresh

## Claude Code

```bash
claude mcp add orange3 -- C:/Users/you/miniconda3/envs/orange/python.exe E:/mcp-servers/orange3_mcp/orange3_mcp.py
claude mcp list
```

## Claude Desktop

`claude_desktop_config.json`，顶层键 `mcpServers`，格式同 Antigravity 但远程要用
`npx mcp-remote <url>` 转成 stdio。

## VS Code

`.vscode/mcp.json`（工作区）或命令面板 `MCP: Open User Configuration`（全局）。

```json
{
  "servers": {
    "orange3": {
      "type": "stdio",
      "command": "C:/Users/you/miniconda3/envs/orange/python.exe",
      "args": ["${workspaceFolder}/mcp-servers/orange3_mcp.py"]
    }
  }
}
```

- 顶层键是 `servers`（不是 `mcpServers`）
- 远程用 `"type": "http"` + `"url"`
- 支持 `inputs` 交互式密钥与 `sandboxEnabled`

## 格式转换

本仓库 `scripts/mcp_vscode_to_antigravity.py` 可自动转换 VS Code → Antigravity：

```bash
python scripts/mcp_vscode_to_antigravity.py .vscode/mcp.json --abs-path
```

## 排障顺序

1. 先在终端手动跑 `python server.py --selftest`，有 Traceback 就是服务器本身的问题
2. `ModuleNotFoundError: mcp.server.fastmcp` → 加 `mcp<2` 约束
3. `executable file not found` → command 改绝对路径
4. 工具列表看不到 → 确认在 Agent 模式且工具已勾选/启用
5. 改完配置点 Refresh；无效再重启 IDE
