# PyMOL MCP Server

把 PyMOL 封装成 MCP 服务，供 Antigravity / Claude Code / VS Code 中的 Agent 调用。

**状态**：用户环境实测可用（生成 SCI 双面板对接图成功）。本仓库副本与其一致。

## 工具（9 个）

| 工具 | 作用 |
|---|---|
| `load_pdb` | 载入结构 |
| `save_image` | 渲染出图（可选 ray） |
| `align_structures` | 结构对齐，返回 RMSD |
| `set_view` / `get_view` | 视角矩阵存取（保证多张图视角一致） |
| `render_movie` | 多结构序列出 MP4（需 ffmpeg） |
| `split_complex_pdb` | 物理拆分复合物为 `lig.pdb` / `pro.pdb` |
| `render_sci_docking_composite` | **主力**：双面板 SCI 成品图 + `.pse` 会话 |
| `reset` | 重置会话 |

## 安装

```bash
conda create -n docking python=3.11 -y
conda activate docking
conda install -c conda-forge pymol-open-source -y
pip install "mcp>=1.28,<2" pillow
python pymol_mcp.py --selftest
```

自检应输出 `PyMOL import success OK` 与 9 个工具清单。

## 注册（Antigravity）

```json
{
  "mcpServers": {
    "pymol": {
      "command": "C:/Users/你/miniconda3/envs/docking/python.exe",
      "args": ["E:/0mcp-agv/pymol/pymol_mcp.py"]
    }
  }
}
```

`command` 必须是装了 PyMOL 那个环境的 python.exe 绝对路径。

## 依赖

- `pymol-open-source`
- `mcp>=1.28,<2`（SDK 2.0 移除了 `mcp.server.fastmcp`）
- `pillow`（`render_sci_docking_composite` 拼图用）
- `ffmpeg`（可选，仅 `render_movie` 需要）

## 已知问题

见 `NOTES.md`。当前版本可用，但有三处建议改进（导入失败未 re-raise、subprocess 无 timeout、缺 info 工具）。
