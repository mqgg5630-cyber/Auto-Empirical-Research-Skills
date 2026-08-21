# PyMOL 氢键出图：为什么 AI 总是画不对

> 这份文档针对一个具体现象：**让 AI 用 PyMOL 画配体-受体氢键，它反复交付「周围残基一大坨、
> 配体和蛋白之间一根线都没有、角落里却有一条 1.7 Å 的无关虚线」的图。**
>
> 配套脚本 `hbond_figure.py` 已在 PyMOL 3.x 上实测通过，自带自检与回读校验。

---

## 五个真实根因（按出现频率排序）

### 1. `cmd.distance()` 的返回值不是氢键条数

这是最隐蔽也最致命的一个。

```python
n = cmd.distance("hb", "ligand", "protein", cutoff=3.3, mode=2)
if n == 0:                      # ❌ 永远不成立
    print("没找到氢键")
```

`cmd.distance()` 返回的是**所有测量值的平均距离**（一个浮点数），不是数量。
实测：一个只有 2 条氢键的体系返回 `2.69` —— 脚本会把它当成"找到 2.69 条"或者
"非零即成功"，于是从不报错，也从不知道自己失败了。

AI 拿不到失败信号，就"贴心地"退化成把口袋周围所有残基都画出来交差 ——
这就是你看到的那一坨绿色棒子的由来。

**正确做法**：不要依赖返回值。自己枚举供体/受体原子对，或者事后从会话里读回来核对。

---

### 2. 两个选择集重叠 → 画出蛋白自身的骨架氢键

```python
cmd.distance("hb", "chain B", "polymer")   # ❌ polymer 把 chain B 也包含了
```

`mode=2` 找的是"极性接触"，它不区分分子间还是分子内。选择集一旦重叠，
蛋白自己 i / i+1 残基之间的骨架氢键就会被画出来。

**识别特征**：`1.6–1.8 Å` 的虚线，而且两端都是蛋白残基（比如你图里的 Leu398–Ser399）。
重原子之间的氢键 N···O 通常是 **2.6–3.2 Å**，出现 1.7 Å 只可能是 **H···O**，
说明结构里其实**是有氢的** —— 所以"没有氢原子所以找不到氢键"这个诊断是错的。

**正确写法**：

```python
lig_sel = "chain B"
rec_sel = "(polymer) and not (chain B)"    # ✓ 强制不相交
```

---

### 3. 选择器用错：肽不是 `organic`

```python
cmd.select("ligand", "organic")    # 小分子配体 ✓ ／ 肽配体 ✗ 得到 0 个原子
```

PyMOL 里 `organic` 指的是非聚合物小分子。**多肽属于 `polymer`**，
用 `organic` 选会得到空集，后面所有操作都在空气上执行。

| 配体类型 | 正确选择 |
|---|---|
| 小分子（抑制剂、辅因子） | `organic` 或 `resn LIG` |
| 肽 / 蛋白链 | `chain B`、`polymer and chain B`、`resi 1-15` |
| 从 docking 输出载入 | 独立成对象，直接用对象名 |

**选完必须打印原子数验证**，这一步花 1 秒，能省 1 小时。

---

### 4. `hide("everything")` 把距离对象也藏了

```python
cmd.distance("hb", ...)      # 画好了
cmd.hide("everything")       # ❌ 连 hb 一起藏掉
cmd.show("sticks", ...)
cmd.ray(2400, 1800)          # 出来的图没有黄线
```

距离对象（distance object）也是 object，`hide everything` 一视同仁。
本文档配套脚本最初也踩了这个坑 —— 检测明明成功，图上就是没有线。

**修法**：出图前显式重新打开。

```python
for obj in cmd.get_names("objects"):
    if obj.startswith("__hb_"):
        cmd.enable(obj)
        cmd.show("dashes", obj)
        cmd.show("labels", obj)
```

---

### 5. 显示矩阵 vs 原子坐标不一致

```python
cmd.translate([3.5, 6, 0], object="peptide")   # ⚠ 只改显示矩阵，不改坐标
```

带 `object=` 参数时，PyMOL 改的是对象的 TTT 显示矩阵，**原子坐标原封不动**。
此时用 `iterate_state` 取到的坐标和屏幕上看到的位置对不上，
自己算的距离全是错的（实测偏差可达 6 Å 以上）。

要改坐标应写 `cmd.translate([...], selection="peptide", camera=0)`。

**防御手段**：算完之后用 `cmd.get_distance()` 逐条回读复核 ——
配套脚本就是这么抓到这个 bug 的。

---

## 配套脚本

```bash
# 自检：不需要任何输入文件，内部用 cmd.fab 造测试复合物
python hbond_figure.py --selftest

# 真实体系（单个复合物文件）
python hbond_figure.py --complex complex.pdb \
    --ligand-sel "chain B" --out figure.png --cutoff 3.5

# 受体与配体分属两个文件
python hbond_figure.py --receptor rec.pdb --ligand pep.pdb --out figure.png
```

自检输出实例（真实运行结果）：

```
[诊断] 选择集体检
  配体原子数        : 147
  受体原子数        : 232
  两者重叠原子数    : 0   ✓
  配体氢原子        : 75
  受体氢原子        : 118

[结果] 共检出 1 条配体-受体氢键

  #  配体原子                受体残基/原子              d(Å)   角度(°)
  ------------------------------------------------------------------
  1  LEU4/N                  /GLU13/O                   3.05      140

  参与成键的受体残基（1 个）：GLU13

[校验] 1/1 条已绘制，全部通过 PyMOL 实测复核 ✓
```

### 它做了什么

1. **出图前体检** —— 打印两个选择集的原子数、重叠数、氢原子数；任何一项不合格直接**阻断**，不出图
2. **自己枚举氢键** —— 供体/受体配对 + 距离 ≤ cutoff + D-H···A 夹角 ≥ 120°
3. **回读校验** —— 每条线用 `cmd.get_distance()` 重测一遍，不一致就以 PyMOL 实测为准重新筛选
4. **打印可审计的氢键表** —— 残基、原子名、距离、角度，可直接贴进补充材料
5. **只显示参与成键的残基** —— `byres` 过滤，画面自然干净
6. **找不到就明确报错**（退出码 3）并给出三条排查建议，绝不静默降级

---

## 给 Agent 的诊断指令（先跑这个，别急着出图）

把下面这段丢给反重力，让它先告诉你问题出在哪：

```
先不要出图。在 PyMOL 里加载我的复合物文件，然后只执行诊断并把结果原样打印给我：

1. print(cmd.get_object_list())          # 有几个对象
2. print(cmd.get_chains(对象名))          # 有哪些链
3. 对我认为的配体选择和受体选择，分别打印：
   cmd.count_atoms(配体选择)
   cmd.count_atoms(受体选择)
   cmd.count_atoms(f"({配体选择}) and ({受体选择})")   # 重叠数，必须是 0
   cmd.count_atoms(f"({配体选择}) and hydro")          # 有没有氢
4. print(cmd.count_atoms("organic"), cmd.count_atoms("polymer"))
5. 用 cmd.iterate 列出配体选择里前 10 个原子的 chain/resi/resn/name

把这 5 项的真实输出贴给我，不要解释，不要出图，不要自己下结论。
```

拿到输出后对照上面五个根因，就能定位是哪一个。

---

## 交给 Agent 出图时的硬性要求

```
用 examples/pymol/hbond_figure.py 这个脚本，不要自己另写。

如果必须改，遵守四条：
1. 不要用 cmd.distance() 的返回值判断有没有氢键 —— 它返回的是平均距离
2. 配体和受体的选择集必须不相交，受体写成 "(polymer) and not (配体选择)"
3. hide("everything") 之后必须显式 show("dashes") 把距离对象重新打开
4. 出图前先打印氢键表（残基/原子/距离/角度），我要看到表格再看图

跑完把终端完整输出贴给我，包括诊断段和氢键表。
只说"已完成""应该可以了"而不贴输出的，一律视为没做。
```

---

## 一眼判断图对不对

| 检查点 | 合格 | 不合格 |
|---|---|---|
| 黄虚线两端 | 一端青色配体，一端绿色残基 | 两端都是蛋白 → 选择集重叠 |
| 虚线长度标注 | 2.6–3.3 Å | 1.6–1.8 Å → 那是 H···O，且多半是蛋白内部的 |
| 绿色棒状残基数量 | 2–6 个 | 一大坨 → `byres` 过滤没生效 |
| 有没有线 | 至少 1 条 | 一条没有 → 检测环节就失败了，不是显示问题 |

---

## 已知限制

- 脚本用几何判据（距离 + 角度），不做量化的氢键能量计算。需要严格判据请用
  HBPLUS、MDAnalysis 的 `HydrogenBondAnalysis` 或 PLIP。
- 只处理氢键。盐桥、π-π、疏水接触需要另外的判据（PLIP 一次全给）。
- 晶体结构缺氢时脚本会调 `cmd.h_add("donors or acceptors")` 补理想氢，
  位置是几何推断的，对 Ser/Thr/Tyr 羟基这类可旋转基团只能算近似。

---

## ⚠️ 如何确认 Agent 真的跑了这个脚本

Agent 常见的做法是「参考你给的脚本，自己重写一个」，然后把失败重新引入一遍。
两个一眼可辨的标记：

### 1. 版本指纹

脚本每次运行第一行必然打印：

```
hbond_figure.py v1.1.0  指纹 e5fe43502be0
（若 Agent 声称跑了本脚本但输出里没有这一行，说明它跑的是别的代码）
```

指纹是文件自身的 SHA256 前 12 位，改动一个字节就会变。也可单独查：

```bash
python hbond_figure.py --version
```

### 2. 输出必须包含这三段

| 标记 | 本脚本的输出 |
|---|---|
| 表头 | 有 **角度(°)** 这一列 |
| 物理自检 | `[物理自检] 距离范围 x.xx – y.yy Å（合理区间 2.2–3.6）` |
| 校验 | `[校验] N/N 条已绘制，全部通过 PyMOL 实测复核 ✓` |

缺任何一段 = 跑的不是这个脚本。

---

## 物理常识：一眼判断结果是不是假的

| 距离 | 含义 |
|---|---|
| 0.9 – 1.6 Å | **共价键长度区间**。两个重原子不可能在非成键状态下靠这么近 |
| 1.6 – 2.2 Å | 若两端都是重原子（N/O），是**空间冲突**；只有 H···O 才可能落在这里 |
| **2.5 – 3.3 Å** | **正常氢键**（N···O、O···O 重原子间距） |
| 3.3 – 3.6 Å | 弱氢键 / 边缘接触 |

另外两条：

- **N···N 或 O···O 之间未必是氢键**。必须一端是供体一端是受体。
  两个骨架酰胺 N 之间报氢键（如 `ALA1/N — SER347/N`）是判据错误 —— 骨架 N 只做供体。
- **数量要合理**。7 个残基的肽报出 46 条氢键（每残基 6.6 条）不可能。
  真实的肽-蛋白界面通常是 **3–10 条**。

v1.1.0 起脚本会自动把 < 2.2 Å 的接触剔出氢键列表，单独作为「空间冲突」报告 ——
那是对接位姿有原子重叠，属于对接阶段的问题，不是画图问题。

---

## 手动 GUI 和脚本结果为什么"差距很大"

这是最容易误判的一点：**两者都对，但量的不是同一个距离。**

### GUI 的 `Action → find → polar contacts` 底层就是一条命令

```python
cmd.dist("lig_polar_conts", "(lig)", "(byobj lig) and not lig",
         quiet=1, mode=2, label=0, reset=1)
```

注意第三个参数 `(byobj lig) and not lig` —— GUI 自动做了「同一对象内、但排除选择集自身」，
所以手动操作**天然不会**出现选择集重叠的问题。这也是手动结果通常比 AI 脚本靠谱的原因。

### 关键差异：结构里有氢时，PyMOL 量的是 H···A

实测同一个体系，同一批接触，两种口径：

| PyMOL 画出来的（H···A） | 论文该报的（D···A 重原子） |
|---|---|
| ALA20/H ··· TRP3/O  1.09 | ALA20/**N** ··· TRP3/O  1.94 |
| TRP3/H ··· GLU13/O  2.23 | TRP3/**N** ··· GLU13/O  3.18 |
| SER7/H ··· LYS17/O  2.70 | SER7/**N** ··· LYS17/O  3.47 |
| LEU6/H ··· ALA16/O  2.72 | LEU6/**N** ··· ALA16/O  3.50 |

**系统性相差约 1 Å**（一根 N–H 键长）。所以：

- 你手动图上那个 **1.7**，是 H···O，**完全正常**，不是错误
- 文献里写「氢键距离 2.9 Å」指的是 **D···A 重原子距离**
- 两个数字不能混着报，也不能互相对照说"差得远"

### v1.2.0 的做法

新增 `--engine` 参数：

```bash
# 默认 both：用 PyMOL 原生判据检测（和你手动点菜单逐条一致），
#            但按论文标准报 D···A，同时附上 H···A 供对照，
#            并用独立的几何判据交叉验证
python hbond_figure.py --complex x.pdb --ligand-sel "chain B"

python hbond_figure.py ... --engine pymol   # 只用 PyMOL 判据
python hbond_figure.py ... --engine geom    # 只用几何判据（D···A + 角度）
```

输出实例：

```
[引擎] PyMOL 原生判据（等同 GUI 的 Action → find → polar contacts）
[对照] 几何判据（D···A ≤ 3.5 Å 且角度 ≥ 120°）检出 4 条，PyMOL 判据检出 5 条
       两者一致 3 条；仅几何 1 条；仅 PyMOL 1 条

  #  配体原子              受体残基/原子           D···A   角度(°)   H···A
  1  SER7/O                A/ALA24/N              2.24     n/a     1.77
  2  TRP3/N                A/GLU13/O              3.18     n/a     2.23
  3  SER7/N                A/LYS17/O              3.47     n/a     2.70
```

它同时解决了 GUI 的两个短板：**GUI 只画线不给列表**（无法核对、无法写进论文），
以及**报的是 H···A 不是期刊要的 D···A**。

> 两个引擎结果不完全一致是正常的 —— PyMOL 用的是 h_bond_cutoff_center / _edge /
> h_bond_max_angle 这组内置设置，几何引擎用的是 D···A ≤ cutoff 且 D-H···A ≥ 120°。
> 论文里注明你用的是哪一套判据即可。差异过大（比如一个 5 条一个 40 条）才说明有问题。

---

## 「肽为什么和自己成氢键」以及为什么要拆成两个对象

### 现象解释：那些是 α 螺旋的骨架氢键，完全正常

GUI 的 `Action → find → polar contacts` 是个**多子项菜单**，不同子项底层是不同命令：

| 菜单子项 | 等价命令 | 实测结果（8 残基螺旋肽） |
|---|---|---|
| **within selection** | `dist pc, (lig), (lig), mode=2` | 10 条，**全部是肽内部** |
| to other atoms in object | `dist pc, (lig), (byobj lig) and not lig, mode=2` | 0 条（拆开后同对象里没别的了） |
| **拆成两个对象后** | `dist pc, lig, pro, mode=2` | 9 条，**分子内 0 条** ✓ |

选了 `within selection` 看到的就是肽自身的氢键。明细（实测）：

```
LYS8/H ··· LYS4/O  2.07 Å   残基间隔 i→i+4
LEU6/H ··· LEU2/O  2.07 Å   残基间隔 i→i+4
LEU5/H ··· ALA1/O  2.07 Å   残基间隔 i→i+4
SER7/H ··· TRP3/O  2.08 Å   残基间隔 i→i+4
```

全是 **i→i+4**，这是 α 螺旋骨架氢键的教科书特征。肽只要是螺旋构象就必然有，
不是错误，也不该出现在配体-受体相互作用表里。

### 拆对象是最稳的做法

```
load complex.pdb, tmp
create lig, tmp and chain B
create pro, tmp and polymer and not chain B
delete tmp
dist lig_polar_conts, lig, pro, mode=2
```

拆开之后，`dist lig, pro` 在**结构上**就不可能包含分子内接触 ——
比靠选择表达式互斥更保险，因为不依赖你把表达式写对。

### v1.3.0 起脚本默认这么做

```
[拆分] 已拆成两个独立对象：lig（配体）/ pro（受体） —— 结构上杜绝分子内接触混入

[提示] 配体自身有 10 条分子内氢键（α 螺旋的 i→i+4 骨架氢键）。
       这是正常的二级结构，不计入配体-受体相互作用表。
       GUI 里若选 find → polar contacts → within selection，看到的就是这些。
```

分子内氢键会被**单独统计并报告**（它有信息量：数量多说明肽保持了螺旋构象），
但不混进相互作用表。不想拆用 `--no-split`。

---

## 当自动化结果和你手动结果对不上时：先取基准真值

你在 GUI 里手动做出来的那个 `lig_polar_conts` 就是**基准真值**。
问题在于 PyMOL 只画线不给列表，没法拿来核对。

`dump_contacts.py` 解决这个问题：它读取**你当前会话里已经存在的**距离对象，
把虚线端点反查回原子，打印成表并存 CSV。不重新计算，不重新加载，
读的就是你屏幕上正在显示的那些线。

### 用法：在 PyMOL 命令行里敲一句

```
run E:/0mcp-agv/pymol/dump_contacts.py
```

输出（实测）：

```
当前会话对象： lig, pro, lig_polar_conts
读取的距离对象： lig_polar_conts

共 9 条接触：分子间 9 条，分子内 0 条

  #  原子1（画线端点）              原子2（画线端点）              画的   D···A
  1  lig/B/LYS8/H                  pro/A/GLU19/O                 1.17    1.59
  2  lig/B/ALA1/H                  pro/A/ALA12/O                 1.47    1.86
  3  pro/A/ALA20/H                 lig/B/TRP3/O                  1.09    1.94
  ...

  涉及的残基（14 个）：
      lig: ALA1, LEU6, LYS4, LYS8, SER7, TRP3
      pro: ALA12, ALA15, ALA16, ALA20, ALA24, GLU13, GLU19, LYS17

  已写出 CSV：contacts_dump.csv
```

它同时给出「画的距离」（PyMOL 显示的 H···A）和「D···A」（论文该报的重原子距离），
并自动区分分子间 / 分子内接触。

### 拿到这张表之后

1. 这张表就是**标准答案**，任何自动化脚本的输出都必须能对上它
2. 对不上就是脚本错，不是你手动错
3. 把这张表直接贴给 Agent，让它去对齐，而不是让它自由发挥

> 如果距离对象是在结构被修改（加氢、删水、重新载入）之前生成的，
> 反查会失败。这时先重新执行一次 `dist lig_polar_conts, lig, pro, mode=2`，
> 再 run 本脚本。
