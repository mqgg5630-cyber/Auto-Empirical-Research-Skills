# 资源参考清单 · Research Software → MCP

按「先用现成的，再自己写」的顺序组织。每条都注明用途和适用场景。
核对时间 2026-08-20；MCP 生态迭代快，链接失效时以项目 README 为准。

---

## 1. 官方规范与 SDK（写之前必读）

| 资源 | 地址 | 用途 |
|---|---|---|
| MCP 官方规范 | https://modelcontextprotocol.io | 协议本体；`sitemap.xml` 后加 `.md` 可取纯文本页 |
| Python SDK | https://github.com/modelcontextprotocol/python-sdk | FastMCP 装饰器 API，本 skill 的模板基于它 |
| TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk | Node 侧实现，Zod 定义 schema |
| **v1 → v2 迁移指南** | https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/migration.md | **必读**：SDK 2.0（2026-07-28）把 `mcp.server.fastmcp` 迁到了 `mcp.server.mcpserver`，`FastMCP` 改名 `MCPServer` |
| MCP Inspector | `npx @modelcontextprotocol/inspector python server.py` | 交互式调试，手动发请求验证工具 |
| 官方参考服务器 | https://github.com/modelcontextprotocol/servers | filesystem、git、fetch、memory 等，最好的代码范例 |

> ⚠️ 依赖必须写 `mcp>=1.28,<2`。2026 年 7 月底 SDK 2.0 发布后，所有没写上限的
> Python MCP 服务器集体崩溃（optuna-mcp、wandb-mcp、jupyter-mcp、freecad-mcp…），
> 报错都是 `ModuleNotFoundError: No module named 'mcp.server.fastmcp'`。

---

## 2. 上游 Skills（可直接安装，与本 skill 互补）

| Skill | 来源 | 与本 skill 的关系 |
|---|---|---|
| **mcp-builder**（官方） | `anthropics/skills` → `skills/mcp-builder` | Anthropic 官方的 MCP 开发指南，四阶段流程（研究规划 → 实现 → 评审测试 → 写评测）。偏「包装云 API」，本 skill 偏「包装本地科研软件」，建议两个都装 |
| **build-mcpb**（官方） | `anthropics/claude-plugins-official` | 把本地 MCP 打包成 `.mcpb`（自带运行时的单文件），适合分发给没装 Python/Node 的同事 |
| **skill-creator**（官方） | `anthropics/skills` | 写/改/评 SKILL.md 本身 |
| antigravity-awesome-skills | https://github.com/sickn33/antigravity-awesome-skills | 1900+ 社区技能与安装器 CLI，可搜是否已有现成的 |

安装方式（跨客户端通用）：

```bash
npx skills add https://github.com/anthropics/skills --skill mcp-builder
npx skills add https://github.com/anthropics/skills --skill mcp-builder -a antigravity
```

反重力的 skill 路径：工作区 `.agents/skills/<名字>/`，
全局 `~/.gemini/config/skills/` 或 `~/.gemini/antigravity/skills/`。

---

## 3. 脚手架与代码生成工具

| 工具 | 地址 | 说明 |
|---|---|---|
| `mcp-template`（PyPI） | https://pypi.org/project/mcp-template/ | **专门把已有 CLI 包装成 MCP** 的生成器，支持 `--infer-tools-from-help` 从 `--help` 输出推断工具签名，适合 B 类（命令行）软件 |
| mcp-server cookiecutter | https://github.com/ntk148v/mcp-server-template | Cookiecutter 模板，含 tools/resources/prompts 三层目录结构 |
| shubhamgupta-dat/mcp-server-template | https://github.com/shubhamgupta-dat/mcp-server-template | 另一个 Cookiecutter，含 lifespan 生命周期管理示例 |
| 本 skill 的模板 | `scripts/template_mcp.py` | 四种集成路径都留了位置，带 `--selftest` |

`mcp-template` 的典型用法：

```bash
mcp-template generate /path/to/output \
  --server-name cdhit --tool-name cluster \
  --binary-name cd-hit --bin-path /usr/bin/cd-hit \
  --infer-tools-from-help --dry-run
```

---

## 4. 服务器注册表（找现成的，别重复造）

| registry | 地址 | 特点 |
|---|---|---|
| GitHub MCP Registry | https://github.com/mcp | GitHub 官方收录，条目经过审核，可信度最高 |
| 官方 servers 仓库 | https://github.com/modelcontextprotocol/servers | 参考实现 + 社区清单 |
| Awesome MCP Servers | https://github.com/punkpeye/awesome-mcp-servers | 社区聚合，数量最多 |
| mcpservers.org / mcp.so / glama.ai | — | 第三方目录，带搜索与安装片段 |

**开工前必查**：以下已有成熟实现，不要重写 ——
`excel-mcp-server`、`office-word-mcp-server`、`zotero-mcp`、`mcp-stata`、
`markitdown`、`paper-search-mcp`、`optuna-mcp`、`wandb-mcp-server`、
`jupyter-mcp-server`、HuggingFace 官方 `hf.co/mcp`。

---

## 5. 科研 / 办公软件封装可行性速查

| 软件 | 路径 | 入口 | 备注 |
|---|---|---|---|
| Orange3 | A | `import Orange` | 本仓库 `examples/mcp-servers/orange3_mcp/` 已实测 |
| scikit-learn / XGBoost | A | 直接 import | 通常不必封装，让 Agent 在 Jupyter 里写代码更灵活 |
| RDKit / Open Babel | A / B | `from rdkit import Chem` | 化学信息学，描述符与格式转换 |
| Biopython | A | `from Bio import SeqIO` | 序列读写与解析 |
| scanpy / Seurat | A / B | Python / Rscript | 单细胞分析 |
| PyMOL | A | `import pymol` | 结构可视化，支持无头模式 `pymol -cq` |
| ChimeraX | C | remotecontrol REST | 需在 GUI 里先开启 remote control |
| **CD-HIT** | B | `cd-hit -i in -o out -c 0.4` | **抗菌肽课题去冗余必用** |
| **BLAST+** | B | `blastp -query -db -outfmt 6` | 序列比对，`-outfmt 6` 输出便于解析 |
| MAFFT / MUSCLE | B | CLI | 多序列比对 |
| ImageJ / Fiji | B | `ImageJ-win64.exe --headless --console -macro x.ijm` | 图像批处理 |
| AutoDock Vina | B | `vina --config conf.txt` | 分子对接 |
| GROMACS | B | `gmx mdrun` | 分子动力学，注意作业时长要异步 |
| Cytoscape | C | CyREST，默认 `localhost:1234` | 网络可视化 |
| KNIME | B | `knime -nosplash -reset -workflowDir=...` | 工作流批处理 |
| Origin | D | `OriginExt`（pywin32） | Windows 绘图与拟合 |
| SPSS | D / B | COM 或 syntax 批处理 | — |
| MATLAB | D / A | MATLAB Engine for Python | `pip install matlabengine` |
| Stata | — | 已有 `mcp-stata` | 直接用 |
| Word / Excel | — | 已有官方社区实现 | 直接用 |
| EndNote | D | Windows COM | Zotero MCP 更成熟，建议改用 Zotero |

---

## 6. 客户端配置格式差异

| | 顶层键 | 远程写法 | 配置位置 |
|---|---|---|---|
| Antigravity | `mcpServers` | `serverUrl` | `~/.gemini/config/mcp_config.json` / `.agents/mcp_config.json` |
| Claude Code | `mcpServers` | `--transport http` | `claude mcp add` 命令 |
| Claude Desktop | `mcpServers` | `mcp-remote` 转 stdio | `claude_desktop_config.json` |
| VS Code | `servers` | `type:"http"` + `url` | `.vscode/mcp.json` |
| Cursor | `mcpServers` | 同 Claude Desktop | `.cursor/mcp.json` |

本仓库 `scripts/mcp_vscode_to_antigravity.py` 可自动做 VS Code → Antigravity 的格式转换。

---

## 7. 安全与最佳实践

| 主题 | 出处 | 要点 |
|---|---|---|
| MCPB 本地安全 | Anthropic `build-mcpb` skill 的 `references/local-security.md` | **MCPB 没有沙箱**，manifest 里没有 permissions 块，进程以完整用户权限运行，路径校验和 spawn 白名单全靠自己写 |
| 命令注入 | 通用 | `subprocess` 必须 `shell=False` + argv 数组；Node 侧用 `execFile` 不用 `exec` |
| 提示注入 | MCP 生态共识 | 抓取类工具与写盘/数据库工具不要给同一个 Agent 会话 |
| 权限最小化 | 各客户端文档 | 数据库只读连接、token 最小 scope、写操作保持人工确认 |
| 反重力权限策略 | Antigravity 官方文档 | 默认 Ask 模式；`mcp(server/tool)` 精确放行，`mcp(*)` 全放行不推荐 |

---

## 8. 本仓库内的相关资产

| 路径 | 内容 |
|---|---|
| `examples/mcp-servers/orange3_mcp/orange3_mcp.py` | Orange3 封装，7 个工具，Orange 3.40.0 实测通过 |
| `examples/mcp-servers/_template/template_mcp.py` | 通用模板 |
| `examples/mcp-servers/README.md` | 可行性判断 + 让 Agent 自己写的提示词 |
| `examples/mcp-antigravity/` | 抗菌肽课题的 Windows 版 mcp_config.json 与 dbhub.toml |
| `scripts/mcp_vscode_to_antigravity.py` | 配置格式转换器 |
| `Antigravity科研办公MCP适配指南.docx` | 反重力侧完整说明 |
| `抗菌肽机器学习预测-MCP与Skills实操教学.docx` | 含附录 C 的 MCP 故障排查手册 |

---

## 9. 延伸阅读

- CLI to MCP 转换实践指南（含 TypeScript 与 Python 双版本最小实现）：
  https://www.openaitoolshub.org/en/blog/cli-to-mcp-converter-guide
- Agent Skills 开放标准：https://agentskills.io
- Anthropic 官方 skills 仓库：https://github.com/anthropics/skills
- 反重力 MCP 文档：https://antigravity.google/docs/mcp
- 反重力 Skills 文档：Settings → Customizations → Build with Google Plugins
