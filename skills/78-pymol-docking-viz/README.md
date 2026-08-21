# 78 · pymol-docking-viz

用 PyMOL 做发表级分子对接可视化与相互作用分析的黄金流程。

## 内容

```
78-pymol-docking-viz/
├── README.md
└── pymol-docking-viz/
    └── SKILL.md          # 双对象架构 / mode=2 判据 / 残基提取 / 标签样式 / 双面板排版
```

配套 MCP 服务器：`examples/mcp-servers/pymol_mcp/pymol_mcp.py`（9 个工具，自检通过）。

## 核心要点

| 要点 | 说明 |
|---|---|
| 双对象架构 | 拆成 `lig` / `pro` 两个对象，结构上杜绝分子内接触混入 |
| `mode=2` 原生判据 | 与 GUI 的 `Action → find → polar contacts` 完全一致 |
| 端点反查残基 | 从 `get_session` 里抠出虚线端点坐标，映射回残基编号 |
| H···A vs D···A | 有显式氢时 PyMOL 量的是 H···A，论文要报 D···A，相差约 1 Å |
| 物理下限 | 重原子间 < 2.2 Å 是空间冲突，不是氢键 |

## 相关

- `skills/77-research-software-to-mcp/` — 把科研软件封装成 MCP 的通用方法论
- `examples/pymol/hbond_figure.py` — 可审计的氢键出图脚本（带指纹校验）
- `examples/pymol/dump_contacts.py` — 从 GUI 会话导出基准真值氢键表
- `docs/mcp-agv/pymol/PyMOL可视化-MCP指南.md` — PyMOL × MCP 完整指南
