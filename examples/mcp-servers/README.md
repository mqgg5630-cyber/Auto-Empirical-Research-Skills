# 给科研软件自己写 MCP 接口

> 能不能让反重力给 Orange3、Origin、ImageJ 这类软件写一套 MCP，然后自己调用？
> **能，而且这是反重力最擅长的活。** 本目录给出一个实测可用的样板（Orange3）和一个通用模板。

---

## 1. 先判断：这个软件能不能封装

按下面的顺序检查，命中越靠前越好做：

| 路径 | 判断依据 | 难度 | 例子 |
|---|---|---|---|
| **A. Python API** | `pip install` 后能 `import` | ⭐ 最简单 | Orange3、RDKit、Biopython、scanpy、PyMOL、DEAP |
| **B. 命令行 CLI** | 装完有可执行文件，支持参数批处理 | ⭐⭐ | ImageJ/Fiji（headless macro）、AutoDock Vina、GROMACS、Rscript、pandoc、CD-HIT、BLAST+ |
| **C. 本地 REST** | 软件自带 HTTP 服务 | ⭐⭐ | Cytoscape（CyREST，端口 1234）、ChimeraX（remotecontrol）、KNIME Server |
| **D. COM 自动化** | Windows 上能用 pywin32 驱动 | ⭐⭐⭐ | Origin（OriginExt）、SPSS、Word/Excel、MATLAB Engine |
| **E. 纯 GUI 无接口** | 三种都没有 | ❌ 别做 | 一些老旧的商业软件 |

**E 类不要硬封装。** UI 自动化（截图+点击）极其脆弱，软件一更新就全废，维护成本远高于人工操作。

---

## 2. 样板：Orange3 MCP（已实测）

`orange3_mcp/orange3_mcp.py` — 用 Orange 3.40.0 实跑验证过 7 个工具全部正常。

### 提供的工具

| 工具 | 作用 |
|---|---|
| `orange_info` | 检查环境：Orange 版本、可用学习器与打分方法清单 |
| `load_table` | 加载 .tab/.csv/.xlsx 或内置数据集，返回结构摘要 |
| `describe_data` | 描述统计：连续变量 min/max/mean/std/缺失率，离散变量频数 |
| `feature_scores` | 信息增益 / Gini / ReliefF / Chi2 / ANOVA 等特征排序 |
| `cross_validate` | 多学习器 k 折交叉验证，分类给 CA/AUC/F1/MCC，回归给 RMSE/MAE/R² |
| `train_and_predict` | 训练+预测，可选导出 CSV |
| `open_workflow_in_gui` | 在 Orange 画布里打开 .ows 工作流 |

### 安装

```powershell
conda create -n orange python=3.11 -y
conda activate orange
pip install Orange3 "mcp>=1.28,<2"
python E:/mcp-servers/orange3_mcp/orange3_mcp.py --selftest
```

自检应输出 Orange 版本号和工具清单。**先自检通过再去配反重力**，能省掉一半排查时间。

### 注册到反重力

`~/.gemini/config/mcp_config.json`：

```json
{
  "mcpServers": {
    "orange3": {
      "command": "C:/Users/你的用户名/miniconda3/envs/orange/python.exe",
      "args": ["E:/mcp-servers/orange3_mcp/orange3_mcp.py"]
    }
  }
}
```

⚠️ `command` 必须指向**装了 Orange3 的那个环境的 python.exe**（用 `conda activate orange` 后跑 `where python` 查），且必须是绝对路径。

### 实测输出示例

```
cross_validate("iris", ["logistic","random_forest","tree"], k=5)
→ logistic      CA 0.9667  AUC 0.9977  F1 0.9667  MCC 0.9501
  random_forest CA 0.9533  AUC 0.9864  F1 0.9533  MCC 0.9306
  tree          CA 0.9467  AUC 0.9613  F1 0.9466  MCC 0.9202
```

---

## 3. 让反重力自己写：可直接粘贴的提示词

把下面这段发给反重力，把 `<软件名>` 换成目标软件：

```
帮我给 <软件名> 写一个 MCP 服务器，参考 examples/mcp-servers/_template/template_mcp.py 的骨架。

步骤：
1. 先用 context7 或 paper-search 查 <软件名> 的官方 Python API / CLI 文档，
   确认它属于 A(Python API) / B(CLI) / C(REST) / D(COM) 中的哪一类。如果都不是，
   直接告诉我不建议封装，不要硬做。
2. 列出你打算暴露的 5-8 个工具，每个说明用途、参数、返回值，先给我确认再写代码。
3. 按模板写实现，硬性要求：
   - 用 from mcp.server.fastmcp import FastMCP，并在文档里注明需要 mcp>=1.28,<2
   - 目标库懒加载，没装时返回可读的安装提示而不是崩溃
   - 每个工具返回 dict，不返回长字符串
   - subprocess 一律 shell=False 且设 timeout
   - 写文件的工具必须显式接收 output 路径，不默认覆盖
   - 提供 --selftest 参数，不启动服务器只做环境自检
4. 写完先跑 python xxx_mcp.py --selftest，再用真实数据实跑每一个工具，把输出贴给我。
   不要只说"应该能用"。
5. 最后给我 mcp_config.json 片段和 README。
```

**关键是第 4 步**：一定要求它实跑验证。Agent 写完不测就说完成了，是最常见的翻车点。

---

## 4. 科研 / 办公软件封装可行性速查

| 软件 | 路径 | 备注 |
|---|---|---|
| Orange3 | A | 本目录已有实现 |
| RDKit / Open Babel | A / B | 化学信息学，分子描述符、格式转换 |
| Biopython / scanpy / Seurat | A / B(Rscript) | 生信标配 |
| PyMOL / ChimeraX | A / C | 结构可视化，ChimeraX 有 REST |
| ImageJ / Fiji | B | `ImageJ-win64.exe --headless --console -macro x.ijm` |
| CD-HIT / BLAST+ / MAFFT | B | 序列去冗余与比对，**做抗菌肽课题会用到** |
| AutoDock Vina / GROMACS | B | 分子对接与动力学 |
| Cytoscape | C | CyREST，默认 1234 端口 |
| Origin | D | `OriginExt` (pywin32)，绘图与拟合 |
| SPSS | D / B | 也可走 syntax 批处理 |
| Stata | — | 已有现成的 mcp-stata |
| Word / Excel | — | 已有 office-word-mcp-server / excel-mcp-server，别重复造 |
| EndNote | D | Windows COM；不过 Zotero MCP 更成熟，建议直接用 Zotero |
| KNIME | B | `knime -nosplash -reset -workflowDir=...` 批处理 |

**先查有没有现成的**再动手写。造轮子之前搜一下 github.com/mcp 和 GitHub。

---

## 5. 六条踩坑经验

1. **环境隔离**：每个封装用独立 conda 环境，`command` 指向该环境的 python.exe。别都塞进 base，依赖冲突会让你怀疑人生。
2. **锁 mcp 版本**：`mcp>=1.28,<2`。SDK 2.0 移除了 `mcp.server.fastmcp`，不锁就会随机某天全挂。
3. **懒加载**：目标库在函数内部 import。这样软件没装时服务器还能启动并告诉你缺什么，而不是反重力里只显示一行 "connection closed"。
4. **工具粒度**：一个工具一件事。不要写 `run_anything(command)` —— 既是安全漏洞，Agent 也用不明白。
5. **docstring 就是接口文档**：Agent 靠它判断何时调用哪个工具。写得含糊，它就会乱调。
6. **先 --selftest 再进反重力**：命令行下的报错信息完整，反重力里只给你一行 EOF。

---

## 6. 目录结构

```
examples/mcp-servers/
├── README.md                    # 本文件
├── _template/
│   └── template_mcp.py          # 通用模板，复制改名即用
└── orange3_mcp/
    └── orange3_mcp.py           # Orange3 封装（已实测）
```
