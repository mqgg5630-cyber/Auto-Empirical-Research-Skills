# 77 · research-software-to-mcp

把科研 / 办公软件包装成 MCP 服务器，让 Agent 能直接驱动它们。

## 这个 skill 解决什么问题

你的工作流里有一堆软件（Orange3、ImageJ、CD-HIT、Cytoscape、Origin……），
Agent 碰不到它们，只能靠你在 GUI 和聊天窗口之间来回复制粘贴。
MCP 是把这些软件接进 Agent 的标准方式，但自己动手写容易踩坑：

- 依赖没锁版本，某天 SDK 更新就全挂
- 目标库顶层 import，软件没装时客户端只显示一行 `EOF`，无从排查
- `shell=True` 拼命令，把注入口子敞开
- 写完不测就宣称完成

这个 skill 把整套流程规范化成五个阶段，并给出可执行的模板与检查器。

## 目录

```
research-software-to-mcp/
├── SKILL.md                        # 主流程：五阶段工作流
├── references/
│   ├── feasibility.md              # 五条集成路径 A-E 与判断方法
│   ├── tool-design.md              # 命名、docstring、返回结构、粒度
│   ├── security.md                 # 子进程、路径、密钥、提示注入
│   ├── client-setup.md             # Antigravity / Claude / VS Code 配置差异
│   └── RESOURCES.md                # 资源参考清单
└── scripts/
    ├── template_mcp.py             # 四路径通用模板，带 --selftest
    └── check_mcp_server.py         # 规范检查器，退出码可接 CI
```

## 核心判断：先决定能不能封装

| 路径 | 判据 | 难度 |
|---|---|---|
| A. Python API | `pip install X` 后能 import | 最低 |
| B. 命令行 | 有可执行文件支持批处理 | 低 |
| C. 本地 REST | 自带 HTTP 端口 | 低 |
| D. COM 自动化 | Windows + pywin32 | 中 |
| E. 纯 GUI | 三者皆无 | **不要封装** |

E 类明确劝退：UI 自动化会在软件下次更新时全部失效，维护成本高过人工操作。

## 快速使用

```bash
# 1. 检查现有服务器是否合规
python scripts/check_mcp_server.py path/to/your_server.py

# 2. 从模板起步
cp scripts/template_mcp.py my_tool_mcp.py

# 3. 写完先自检，再进客户端
python my_tool_mcp.py --selftest
```

## 安装到 Agent 客户端

```bash
# Claude Code / Cursor / 通用
npx skills add https://github.com/mqgg5630-cyber/Auto-Empirical-Research-Skills --skill research-software-to-mcp

# 反重力（工作区级）
mkdir -p .agents/skills
cp -r skills/77-research-software-to-mcp/research-software-to-mcp .agents/skills/
```

## 已验证的产出

本仓库 `examples/mcp-servers/orange3_mcp/orange3_mcp.py` 是按此 skill 写出的样板，
7 个工具在 Orange 3.40.0 上实测通过，`check_mcp_server.py` 全项 PASS。

## 配套资产

- `examples/mcp-servers/README.md` — 可行性速查 + 让 Agent 自己写的提示词
- `scripts/mcp_vscode_to_antigravity.py`（仓库根）— 配置格式转换
- `references/RESOURCES.md` — 上游官方 skill、SDK、脚手架、注册表清单
