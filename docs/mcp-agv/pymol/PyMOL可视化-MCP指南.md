# PyMOL × MCP 实操指南

> 把 PyMOL 变成 Agent 可调用的出图与结构分析工具
> 配套目录：`E:\0mcp-agv\pymol`

---

## 1. 为什么 PyMOL 特别适合封 MCP

按 `skills/77-research-software-to-mcp` 的五条路径判断，PyMOL 是**最理想的 A 类**：

- `pip install pymol-open-source` 后能直接 `from pymol import cmd`
- **所有 GUI 操作都有等价的 Python 命令**，没有任何功能只能靠鼠标点
- 支持完全无头运行：`pymol -cq script.py`，不需要显示器
- 出图是高度重复的机械劳动 —— 正是应该交给 Agent 的那类工作

对比一下：GROMACS 要处理几小时的异步作业，Vina 要小心盒子和打分陷阱，
而 PyMOL 的每个操作都是秒级、幂等、无副作用的。**如果你只想封一个软件练手，就从 PyMOL 开始。**

---

## 2. 安装

```bash
conda create -n pymol python=3.11 -y
conda activate pymol
conda install -c conda-forge pymol-open-source -y     # 推荐用 conda，pip 版依赖较麻烦
pip install "mcp>=1.28,<2"

# 验证无头模式
pymol -cq -d "print('pymol headless ok')"
python -c "from pymol import cmd; print('python api ok')"
```

> **版本说明**：开源版（pymol-open-source）足够科研出图使用。
> 商业版 Incentive PyMOL 多了一些插件和技术支持，学术用户可申请教育授权。
> 论文致谢里按官方要求注明使用了 PyMOL 即可。

---

## 3. 无头出图的基本骨架

```python
from pymol import cmd

cmd.reinitialize()
cmd.load('complex.pdb', 'sys')

# 结构表示
cmd.hide('everything')
cmd.show('cartoon', 'polymer')
cmd.show('sticks', 'organic')            # 配体
cmd.color('grey80', 'polymer')
cmd.color('marine', 'chain B')
cmd.util.cnc('organic')                  # 配体按元素上色

# 视角
cmd.orient('organic')
cmd.zoom('organic', 4)

# 出版级渲染
cmd.set('ray_opaque_background', 0)      # 透明背景，方便排版
cmd.set('antialias', 2)
cmd.set('ray_trace_mode', 0)
cmd.set('ambient_occlusion_mode', 1)     # 环境光遮蔽，立体感明显更好
cmd.set('specular', 0.2)
cmd.bg_color('white')

cmd.ray(2400, 1800)                      # 像素尺寸，期刊一般要求 300 dpi
cmd.png('figure.png', dpi=300)
```

运行：`pymol -cq make_figure.py`

---

## 4. MCP 工具划分建议

```
pymol_info()                                   # 版本、可用扩展
load_structure(path, name)                     # 载入 pdb/cif/sdf/pdbqt
list_objects()                                 # 当前会话里有什么
get_sequence(selection)                        # 取序列
align_structures(mobile, target)               # 对齐，返回 RMSD 与对齐残基数
measure_distance(sel1, sel2)                   # 距离/角度/二面角
find_contacts(sel1, sel2, cutoff)              # 界面残基与接触对
show_interactions(sel1, sel2)                  # 氢键、盐桥、疏水接触
apply_style(preset)                            # publication / cartoon / surface / ligand
render_image(out_png, width, height, dpi)      # 出图
save_session(out_pse)                          # 存会话供人工微调
run_pymol_script(path)                         # ⚠️ 见下方安全说明
```

### 关于 `run_pymol_script`

这个工具很方便，但它本质上是任意代码执行（PyMOL 脚本可以 `import os`）。
两个选择：

- **不提供它**，只暴露上面那些语义明确的工具 —— 推荐
- 提供，但只接受**文件路径**而非内联代码，并限定在白名单目录内

不要做成 `run_pymol_command(cmd_string)` 让 Agent 随便传字符串。

---

## 5. 三个高频场景

### 5.1 可视化对接位姿（配合 vina 目录）

```python
cmd.load('receptor.pdb', 'rec')
cmd.load('out.pdbqt', 'poses')          # Vina 输出的多构象
cmd.split_states('poses')               # 拆成 poses_0001, poses_0002...
cmd.delete('poses')

cmd.hide('everything')
cmd.show('surface', 'rec')
cmd.set('transparency', 0.5)
cmd.show('sticks', 'poses_0001')
cmd.color('yellow', 'poses_0001')

# 结合口袋残基
cmd.select('pocket', 'byres (rec within 5 of poses_0001)')
cmd.show('sticks', 'pocket')
cmd.orient('poses_0001')
```

### 5.2 MD 轨迹快照（配合 gmx 目录）

```python
# 先用 gmx trjconv 抽帧并做 PBC 修正
#   gmx trjconv -s prod.tpr -f prod.xtc -o frames.pdb -pbc mol -center -dt 100
cmd.load('frames.pdb', 'traj')          # 多帧自动成为 states
cmd.mset('1 -%d' % cmd.count_states('traj'))
cmd.show('cartoon', 'traj')
cmd.png('frame.png', ray=1)             # 或 cmd.mpng() 出序列帧做动画
```

### 5.3 抗菌肽-膜体系出图

```python
cmd.load('system.pdb', 'sys')
cmd.hide('everything')

# 膜用球棍+半透明，磷原子标出来当膜面参考
cmd.show('spheres', 'resn POPE+POPG and name P')
cmd.color('orange', 'resn POPE and name P')
cmd.color('red',    'resn POPG and name P')
cmd.set('sphere_scale', 0.4)

# 肽突出显示
cmd.show('cartoon', 'polymer.protein')
cmd.color('marine', 'polymer.protein')
cmd.show('sticks', 'polymer.protein and (resn ARG+LYS)')   # 正电残基
cmd.color('blue', 'polymer.protein and (resn ARG+LYS)')

cmd.set('cartoon_transparency', 0.0)
cmd.turn('x', -90)                       # 侧视，看插入深度
cmd.ray(2400, 1800); cmd.png('insertion.png', dpi=300)
```

> 这张图配合 `gmx density` 算出的插入深度曲线，就是「选择性毒性」那部分讨论的核心配图。

---

## 6. 现成的插件（不必自己写的部分）

| 插件 | 用途 |
|---|---|
| **DockingPie** | 在 PyMOL 里直接跑 Vina/Smina/ADFR/RxDock 共识对接 |
| **GetBox-PyMOL-Plugin** | 交互式确定对接盒子，输出 Vina/AutoDock/LeDock 格式（有中文教程） |
| **PyMOL psico** | 大量补充命令的扩展包，`pip install pymol-psico` |

装插件：`Plugin → Plugin Manager → Install New Plugin`。
插件是给人用的 GUI，MCP 是给 Agent 用的接口 —— 两者不冲突，可以并存。

---

## 7. 常见坑

| 现象 | 原因 | 处理 |
|---|---|---|
| `cmd.ray()` 卡死或崩溃 | 分辨率太高、体系太大 | 降到 1600×1200 先试；表面渲染尤其吃内存 |
| 无头模式报 X display 错误 | 某些操作仍试图开窗口 | 用 `pymol -cq`；Linux 上可配 `xvfb-run` |
| 图里背景是黑的 | 默认背景色 | `cmd.bg_color('white')` + `ray_opaque_background=0` |
| 载入 pdbqt 只显示一个构象 | 多模型需要拆分 | `cmd.split_states()` |
| 每次出图角度不一样 | 没保存视角 | `cmd.get_view()` 存下来，下次 `cmd.set_view(...)` 复现 |
| 图在论文里发虚 | 分辨率不够 | `ray` 的宽高按 300 dpi × 目标英寸数算，别只靠 `dpi` 参数 |

**视角可复现小技巧**：手工调好角度后在 PyMOL 里跑 `get_view`，把返回的 18 个数字存进脚本，
以后所有版本的图都用同一视角 —— 审稿人要你改图时会省很多事。

---

## 8. 参考资源

- PyMOL 官方文档 — https://pymol.org/dokuwiki/
- PyMOLWiki（命令大全，最实用） — https://pymolwiki.org
- pymol-open-source — https://github.com/schrodinger/pymol-open-source
- psico 扩展 — https://github.com/speleo3/pymol-psico
- DockingPie — https://github.com/paiardin/DockingPie
- GetBox-PyMOL-Plugin — https://github.com/MengwuXiao/GetBox-PyMOL-Plugin

本仓库配套：`skills/77-research-software-to-mcp/`（封装方法论）、
`examples/mcp-servers/orange3_mcp/orange3_mcp.py`（可直接照抄的 A 类封装样板）。
