# AutoDock Vina × MCP 实操指南

> 分子对接自动化，以及一个必须先说清楚的问题：**Vina 不适合直接对接抗菌肽**
> 配套目录：`E:\0mcp-agv\vina`

---

## 1. ⚠️ 先纠正一个常见误区

AutoDock Vina 是为**小分子**（配体通常 < 10 个可旋转键）设计的。
抗菌肽通常 10–40 个氨基酸，可旋转键上百个，**直接用 Vina 对接结果不可信** ——
搜索空间远超它的采样能力，打分函数也没有为肽段的骨架氢键网络校准过。

### 该用什么

| 你的对象 | 用什么 | 说明 |
|---|---|---|
| 小分子配体（抑制剂、抗生素小分子） | **AutoDock Vina** | 本文主体，成熟可靠 |
| **肽（≤ 20 aa）** | **ADCP**（AutoDock CrankPep） | ccsb-scripps 出品，专为肽设计，蒙特卡洛折叠 + 受体亲和格点，可从序列直接起算 |
| 肽-蛋白复合物 | HPEPDOCK / HADDOCK（在线） | 无需本地部署 |
| 肽-**膜**相互作用 | **不要用对接，用 MD** | 见 `gmx` 目录那份文档。膜不是刚性受体，对接范式不适用 |

> 对你的抗菌肽课题：主战场是 **MD（膜相互作用）**，对接只在你要研究「肽结合某个特定蛋白靶点」
> （如 LPS、细胞壁合成酶）时才用得上，那时用 ADCP 而不是 Vina。

### ADCP + Vina 的组合用法（有实测工作流）

社区已有成熟做法：ADCP 做肽对接 → `reduce` 加氢 → Vina 的 Python `optimize()`
做柔性侧链局部优化和重打分，等于一个简易的诱导契合精修。

```python
from vina import Vina
v = Vina(sf_name='vina')
v.set_receptor(rigid_pdbqt_filename='rec_rigid.pdbqt',
               flex_pdbqt_filename='rec_flex.pdbqt')
v.set_ligand_from_file('adcp_pose.pdbqt')
v.compute_vina_maps(center=[20.1, 11.0, 27.8], box_size=[30, 30, 30])
print('优化前:', v.score())
print('优化后:', v.optimize())
v.write_pose('refined.pdbqt', overwrite=True)
```

---

## 2. Windows 用户注意

**Vina 的 Python bindings 官方只支持 Linux 和 macOS**，Windows 未测试。
你有三个选择：

| 方案 | 说明 | 推荐度 |
|---|---|---|
| **WSL2 + Ubuntu** | `wsl --install`，在 WSL 里建 conda 环境。MCP 的 command 指向 WSL 内的 python | ⭐ 推荐 |
| **Docker** | 拉现成的 docking 镜像，MCP 用 `docker run -i` 启动 | 也可以 |
| Windows 原生二进制 | `vina.exe` 可用（命令行版），但没有 Python bindings，只能走 subprocess | 够用 |

如果只走命令行二进制（路径 B 封装），Windows 原生完全可行，不必折腾 WSL。

---

## 3. 环境安装

```bash
# Linux / macOS / WSL
conda create -n vina python=3.11 -y
conda activate vina
pip install -U numpy scipy rdkit vina meeko gemmi prody "mcp>=1.28,<2"

# 验证
python -c "from vina import Vina; print('vina python ok')"
mk_prepare_ligand.py --help
```

Windows 原生（只要二进制）：从 https://github.com/ccsb-scripps/AutoDock-Vina/releases
下载 `vina_1.2.x_win.exe`，放进 `E:\0mcp-agv\vina\bin\`。

---

## 4. 现成的工具（优先看）

| 项目 | 类型 | 说明 |
|---|---|---|
| **DockingPie** | PyMOL 插件 | 共识对接，一个界面集成 Vina / Smina / ADFR / RxDock，输入准备全自动。**Windows 上只支持 Vina 和 ADFR** |
| **GetBox-PyMOL-Plugin** | PyMOL 插件 | 计算对接盒子坐标，输出 Vina / AutoDock / LeDock 三种格式（中文教程齐全） |
| **AMDock** | 独立 GUI | 辅助对接，Windows 版单独维护 |
| **dockit** | 批量流水线 | 多靶点多配体高通量，支持 vina/smina/qvina |
| **ADCP** | 肽对接引擎 | ccsb-scripps/ADCP，随 ADFR Suite 分发 |

**先用 DockingPie 手工跑通一遍**，理解每步在干什么，再去封 MCP。
不理解流程就自动化，只会得到一堆看起来很像样的垃圾结果。

---

## 5. MCP 工具划分建议

按 `skills/77-research-software-to-mcp` 的规范：

```
vina_info()                              # 版本、可执行文件路径、可用打分函数
prepare_receptor(pdb, out_pdbqt, ph)     # 调 mk_prepare_receptor.py
prepare_ligand(sdf_or_smi, out_pdbqt)    # 调 mk_prepare_ligand.py
define_box(receptor, ref_ligand|residues)# 从共晶配体或残基列表算盒子中心与尺寸
dock(receptor, ligand, box, exhaustiveness, n_poses, out)   # 核心
score_pose(receptor, pose)               # 只打分不搜索
optimize_pose(receptor, pose, flex_res)  # 局部最小化（诱导契合精修）
batch_dock(receptor, ligand_dir, box, out_dir)   # 批量，注意做成异步
parse_results(out_pdbqt)                 # 解析亲和力表 → 结构化 JSON
```

### 两个关键设计点

**盒子（box）是最容易出错的参数。** 一定要有独立的 `define_box` 工具，
从共晶配体或指定残基自动算，不要让 Agent 凭空猜坐标。盒子太小会截断构象，
太大则搜索效率暴跌、假阳性增多。

**批量对接要异步。** 单个配体 `exhaustiveness=32` 大约几十秒，
筛 1000 个化合物就是几小时。和 GROMACS 一样：`submit` → `poll` → `collect`。

---

## 6. 打分函数的局限（写论文时必须知道）

| 误区 | 事实 |
|---|---|
| Vina 打分 = 结合亲和力 | **不是**。它是经验打分函数，与实验 ΔG 的相关性通常只有 R² ≈ 0.4–0.5 |
| 分数低 0.5 kcal/mol 就是更好的结合 | 在噪声范围内，没有意义 |
| 可以用打分排序做虚拟筛选的最终依据 | 只能做粗筛。前 1–5% 富集尚可，绝对排序不可靠 |

**正确用法**：把 Vina 分数当作**粗筛的排序信号**，前若干名再用 MM-PBSA、
自由能微扰或 MD 稳定性做二次验证。论文里不要把 docking score 当成亲和力预测值报告。

---

## 7. 完整示例：小分子对接

```python
from vina import Vina

v = Vina(sf_name='vina', cpu=8, seed=42)          # 固定种子，保证可复现
v.set_receptor('receptor.pdbqt')
v.set_ligand_from_file('ligand.pdbqt')
v.compute_vina_maps(center=[15.19, 53.90, 16.92], box_size=[20, 20, 20])

v.dock(exhaustiveness=32, n_poses=20)
v.write_poses('out.pdbqt', n_poses=5, overwrite=True)

energies = v.energies(n_poses=5)
for i, e in enumerate(energies, 1):
    print(f"pose {i}: affinity {e[0]:.2f} kcal/mol")
```

命令行等价写法：

```bash
vina --receptor receptor.pdbqt --ligand ligand.pdbqt \
     --center_x 15.19 --center_y 53.90 --center_z 16.92 \
     --size_x 20 --size_y 20 --size_z 20 \
     --exhaustiveness 32 --num_modes 20 --seed 42 \
     --out out.pdbqt --log log.txt
```

---

## 8. 常见坑

| 现象 | 原因 | 处理 |
|---|---|---|
| `Parse error ... Unknown or inappropriate tag` | pdbqt 文件格式不对 | 用 Meeko 的 `mk_prepare_*` 重新生成，别手工改 |
| 每次结果不一样 | 没固定 seed | `--seed 42`，且报告时注明 |
| 所有配体分数都差不多 | 盒子太大或位置不对 | 用 `define_box` 从共晶配体重算 |
| 肽对接结果荒谬 | 用错工具了 | 见第 1 节，换 ADCP |
| 受体缺少氢 | 没加氢就直接对接 | `reduce` 或 Meeko 的 `-p` 参数 |
| Windows 上 `pip install vina` 失败 | 官方不支持 | 用 WSL2，或只用 vina.exe 走 subprocess |

---

## 9. 参考资源

- AutoDock Vina — https://github.com/ccsb-scripps/AutoDock-Vina
- Vina 文档 — https://autodock-vina.readthedocs.io
- Meeko（输入准备） — https://github.com/forlilab/Meeko
- **ADCP（肽对接）** — https://github.com/ccsb-scripps/ADCP ｜ https://adcp.scripps.edu
- DockingPie — https://github.com/paiardin/DockingPie
- GetBox-PyMOL-Plugin — https://github.com/MengwuXiao/GetBox-PyMOL-Plugin
- AMDock — https://github.com/Valdes-Tresanco-MS/AMDock
- dockit（高通量） — https://github.com/aretasg/dockit

本仓库配套：`skills/77-research-software-to-mcp/`、`examples/mcp-servers/_template/template_mcp.py`。
