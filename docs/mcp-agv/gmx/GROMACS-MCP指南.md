# GROMACS × MCP 实操指南

> 面向抗菌肽（AMP）课题的分子动力学自动化：已有方案盘点、肽-膜体系工作流、MCP 封装设计
> 配套目录：`E:\0mcp-agv\gmx`

---

## 1. 先别自己写：已有四个现成方案

| 项目 | 类型 | 说明 | 适合谁 |
|---|---|---|---|
| **MacromNex/gromacs_mcp** | MCP 服务器 | Docker 内置 GROMACS 2025.4，6 个工具。**做了异步作业跟踪** | 想立刻用上，且装了 Docker |
| **Billwanttobetop/automd-gromacs** | **Agent Skills** | 港科广，MIT，v5.0.0。method-selector 决策层；覆盖增强采样、**膜体系、粗粒化**、QM/MM；论文级出图 | ⭐ 你的首选 |
| **ChatMol/gromacs_copilot** | LLM Agent | pip 安装，agent 模式自动建系→模拟→分析 | 想看别人怎么切分工具 |
| **MDCrow**（ur-whitelab） | Agent + 论文 | 40 个专家工具，四类划分。OpenMM 为主，论文附 GROMACS 适配示例 | 设计参考 |

### 安装

```bash
# gromacs_mcp（Docker）
docker pull ghcr.io/macromnex/gromacs_mcp:latest
```

```powershell
# automd-gromacs（Agent Skills，装进反重力）
git clone https://github.com/Billwanttobetop/automd-gromacs.git
xcopy /E /I automd-gromacs "E:\0mcp-agv\.agents\skills\automd-gromacs"
```

反重力配置（`~/.gemini/config/mcp_config.json`）：

```json
{
  "mcpServers": {
    "gromacs": {
      "command": "docker",
      "args": ["run", "-i", "--rm",
               "-v", "E:/0mcp-agv/gmx:/work",
               "ghcr.io/macromnex/gromacs_mcp:latest"]
    }
  }
}
```

---

## 2. ⚠️ 设计红线：mdrun 绝不能做成同步工具

MD 动辄跑几小时到几天，MCP 工具调用必然超时。正确的切分方式：

| 阶段 | 工具 | 耗时 | 同步？ |
|---|---|---|---|
| 建系 | `build_system`、`build_membrane`、`write_mdp` | 秒级 | ✅ 同步 |
| 提交 | `submit_md` → 返回 job id | 立即返回 | ✅ 同步 |
| 监控 | `get_job_status`、`tail_log` | 秒级 | ✅ 轮询 |
| 分析 | `analyze_trajectory`、`parse_xvg` | 分钟级 | ✅ 同步 |

**分析类工具的性价比远高于模拟类**：快、幂等、不占 GPU，而且是你每天重复最多次的操作。
如果只做一件事，就做分析封装。

---

## 3. 抗菌肽-膜体系的标准工作流

ML 预测出候选肽之后，MD 是最标准的机制验证。核心问题是**选择性毒性**：
为什么这条肽杀细菌而不溶血？

### 3.1 两套膜，对照做

| 膜类型 | 组分 | 模拟什么 |
|---|---|---|
| **细菌膜** | POPE : POPG = 3:1（革兰阴性内膜）<br>或加 CL（心磷脂） | 带负电，肽应快速吸附并插入 |
| **哺乳动物膜** | POPC + 30% 胆固醇 | 电中性、更致密，肽应停留在表面 |

两套体系跑同样的肽，对比插入深度差异 —— 这就是选择性的分子解释。

### 3.2 建议路线：Martini 3 粗粒化

全原子模拟肽-膜相互作用需要几微秒才能看到插入，机时不现实。粗粒化能压到可承受范围。

```bash
# 1. 肽结构（AlphaFold / PEP-FOLD / 螺旋建模）
# 2. 粗粒化
martinize2 -f peptide.pdb -o topol.top -x peptide_cg.pdb -ff martini3001 -dssp -elastic

# 3. 建膜 + 放肽 + 加水加盐
insane -f peptide_cg.pdb -o system.gro -p system.top \
       -pbc square -box 12,12,14 \
       -l POPE:3 -l POPG:1 -sol W -salt 0.15

# 4. EM → NVT → NPT → production
gmx grompp -f em.mdp   -c system.gro -p system.top -o em.tpr   && gmx mdrun -deffnm em
gmx grompp -f npt.mdp  -c em.gro     -p system.top -o npt.tpr  && gmx mdrun -deffnm npt
gmx grompp -f prod.mdp -c npt.gro    -p system.top -o prod.tpr && gmx mdrun -deffnm prod
```

### 3.3 该算哪些指标

| 指标 | 命令 | 说明 |
|---|---|---|
| 插入深度 | `gmx density` / MDAnalysis | 肽质心相对膜中心的 z 距离，**最关键的一个** |
| 膜厚 | `gmx density`（P 原子峰间距） | 肽插入会导致局部变薄 |
| 脂链序参数 | `gmx order` | 有序度下降 = 膜被扰动 |
| 每脂面积 APL | 盒子 xy 面积 / 每叶脂数 | 膜膨胀的指标 |
| 二级结构 | `gmx do_dssp` | 螺旋是否在接触膜后形成/维持（全原子才有意义） |
| 接触残基 | MDAnalysis 距离筛选 | 哪些残基负责结合 —— 配合 ML 的 SHAP 结果互相印证 |
| 成孔 | 水分子跨膜数 / VMD 可视化 | 桶状孔或环形孔的直接证据 |

> 💡 **和你 ML 部分的呼应**：第 6 章 SHAP 分析找出的关键残基，如果在 MD 里也正是接触膜最深的那几个，
> 这就是「计算-计算」的交叉验证，论文讨论部分的分量会明显不一样。

---

## 4. 自己封 MCP 时的工具划分

参考 `skills/77-research-software-to-mcp` 的规范，建议这样切：

```
gmx_info()                    # 版本、可用命令、GPU 检测
build_membrane(lipids, box)   # 调 insane，返回体系组成统计
coarse_grain(pdb, ff)         # 调 martinize2
write_mdp(preset, overrides)  # 从模板生成 .mdp，preset: em/nvt/npt/prod
grompp(mdp, gro, top)         # 预处理，返回警告与错误
submit_md(tpr, nsteps, gpu)   # nohup 或 sbatch，返回 job_id
get_job_status(job_id)        # 轮询
tail_log(job_id, n)           # 看 md.log 末尾
parse_xvg(path)               # .xvg → 结构化 JSON（这个最常用）
analyze_rmsd/rmsf/gyrate(...) # 常规轨迹分析
analyze_insertion(traj, tpr)  # 肽-膜插入深度剖面
analyze_order(traj, tpr)      # 脂链序参数
```

**优先级**：`parse_xvg` + 三个 `analyze_*` 就能覆盖你 80% 的日常操作，先做这四个。

### 值得改成 MCP 的库

| 库 | 路径 | 用途 |
|---|---|---|
| **gmxapi** | A（Python API） | GROMACS 官方接口，2019 版起自带，支持 ensemble 并行、数据流串联 |
| **GromacsWrapper** | A | 把 gmx 命令包成 Python 类，支持 4.6.5–2024 |
| **MDAnalysis / MDTraj** | A | 轨迹分析首选，纯 Python |
| **gmx_MMPBSA** | B（CLI） | 结合自由能 |
| **CHAPERONg** | B | 全流程自动化，20 种分析 |
| **PLUMED** | B | 增强采样与 CV |

---

## 5. 常见坑

| 现象 | 原因 | 处理 |
|---|---|---|
| MCP 调用超时 | 把 mdrun 做成了同步工具 | 改异步提交 + 轮询 |
| `gmx grompp` 报 note/warning 被忽略 | Agent 没读 stderr | 工具要把 stderr 一并返回 |
| 粗粒化肽二级结构崩塌 | 没加弹性网络 | `martinize2 -elastic` 或 `-go`（Gō 模型） |
| 膜体系跑飞 | 平衡不充分 | NPT 半各向同性耦合，先跑几十 ns 弛豫 |
| 插入深度算错 | 没做 PBC 修正与膜居中 | `gmx trjconv -pbc mol -center` 后再分析 |
| 结果不可复现 | 没固定随机种子 | mdp 里写死 `gen_seed`、`ld_seed` |

---

## 6. 参考资源

- MacromNex/gromacs_mcp — https://github.com/MacromNex/gromacs_mcp
- Billwanttobetop/automd-gromacs — https://github.com/Billwanttobetop/automd-gromacs
- ChatMol/gromacs_copilot — https://github.com/ChatMol/gromacs_copilot
- MDCrow — https://github.com/ur-whitelab/MDCrow（有论文）
- GromacsWrapper — https://github.com/Becksteinlab/GromacsWrapper
- CHAPERONg — https://github.com/abeebyekeen/CHAPERONg
- Martini 力场与 insane — http://cgmartini.nl
- gmx_MMPBSA — https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA

本仓库配套：`skills/77-research-software-to-mcp/`（封装方法论）、
`examples/mcp-servers/_template/template_mcp.py`（模板）。
