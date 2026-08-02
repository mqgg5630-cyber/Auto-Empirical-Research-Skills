# 非 Aβ 候选毒性肽：分子对接 / 分子动力学 / 量化计算——可参考做法与文献

**（整理日期 2026-08-02｜docx 由 python-docx 生成标准 OOXML；沙箱无 officecli，Word/WPS 可直接打开）**

> **定位**  
> - 你的肽 **不是 Aβ**：阳性对照与机制锚点用 **PrP106–126、LL-37、人 amylin（IAPP）** 等非 Aβ 毒性肽。  
> - 本文只整理 **分子对接、MD、量化计算（MM/GBSA、QM/MM、DFT）** 能直接参考的文献 **完整题目** + **具体怎么做**。  
> - 计算只做 **优先级排序与结构假设**，不能单独证明“导致 AD”。

---

## 0 总体计算流水线（建议照此写方案）

```
① 肽多构象生成（AF3 / 肽折叠 / 聚类）
        ↓
② 分子对接（膜/受体/金属位点 — 按假说选靶）
        ↓
③ 分子动力学 MD（≥3 次独立重复，显式溶剂）
        ↓
④ MM/GBSA 或 MM/PBSA（仅同系列相对排序）
        ↓
⑤ 头部候选：QM/MM 或 DFT（金属配位 / 电荷 / 相对配位能）
        ↓
⑥ 输出：结构坐标摘要 + 界面残基 + 稳定性指标 + “功能待实验”
```

| 阶段 | 目的 | 主要软件/工具（示例） | 核心参考文献（题目见后文） |
|---|---|---|---|
| 构象 | 短肽柔性 ensemble | AlphaFold 3、PEP-FOLD、MD 聚类 | Abramson 2024 *Nature* |
| 对接 | 结合模式假设 | AutoDock Vina / Glide / HADDOCK / HDOCK | 见 §2 |
| MD | 稳定性、接触、金属驻留 | GROMACS / AMBER / NAMD | Hollingsworth & Dror 2018 *Neuron* |
| 结合能 | 12 肽相对排序 | MMPBSA.py / gmx_MMPBSA | Genheden & Ryde 2015 |
| 量化 | 配位几何与电子结构 | Gaussian / ORCA + QM/MM | Senn & Thiel 2009；金属–肽 DFT 文 |
| 非 Aβ 生物学锚点 | 为何做这些计算 | — | Forloni；Chen LL-37；amylin 线 |

---

## 1 生物学锚点文献（非 Aβ 毒性肽——计算服务的对象）

> 计算方案要写清：对标的是这类 **非 Aβ 毒性肽** 的结构/毒性问题，不是 Aβ 身份证明。

### 1.1 PrP106–126（经典非 Aβ 短毒性肽）

| # | 完整题目 | 期刊 / 年 | DOI | PMID |
|---|---|---|---|---|
| B1 | **Neurotoxicity of a prion protein fragment** | *Nature* 1993; 362:543-546 | [10.1038/362543a0](https://doi.org/10.1038/362543a0) | [8464494](https://pubmed.ncbi.nlm.nih.gov/8464494/) |
| B2 | **Review: PrP 106-126 - 25 years after** | *Neuropathol Appl Neurobiol* 2019; 45:430-440 | [10.1111/nan.12538](https://doi.org/10.1111/nan.12538) | [30635947](https://pubmed.ncbi.nlm.nih.gov/30635947/) |
| B3 | **PHB2 Alleviates Neurotoxicity of Prion Peptide PrP(106-126) via PINK1/Parkin-Dependent Mitophagy** | *Int J Mol Sci* 2023; 24:15919 | [10.3390/ijms242115919](https://doi.org/10.3390/ijms242115919) | [37958902](https://pubmed.ncbi.nlm.nih.gov/37958902/) |

**对计算的含义**：短肽可自身聚集并致神经元死亡 → 计算应覆盖 **肽自组装 / 膜相互作用 /（可选）线粒体相关蛋白接触**，阳性对照序列可用 PrP106–126。

---

### 1.2 LL-37（人源抗菌肽，AD 相关非 Aβ 肽）

| # | 完整题目 | 期刊 / 年 | DOI | PMID |
|---|---|---|---|---|
| B4 | **Human antimicrobial peptide LL-37 contributes to Alzheimer's disease progression** | *Mol Psychiatry* 2022; 27:4790-4799 | [10.1038/s41380-022-01790-6](https://doi.org/10.1038/s41380-022-01790-6) | [36138130](https://pubmed.ncbi.nlm.nih.gov/36138130/) |
| B5 | **LL-37: Structures, Antimicrobial Activity, and Influence on Amyloid-Related Diseases** | *Biomolecules* 2024; 14:320 | [10.3390/biom14030320](https://doi.org/10.3390/biom14030320) | [38540740](https://pubmed.ncbi.nlm.nih.gov/38540740/) |

**对计算的含义**：LL-37 通过 **CLIC1** 等膜相关机制 → 对接/MD 优先靶点可设 **CLIC1 跨膜/近膜区** 或 **阴离子膜模型**；不要默认对接 Aβ。

---

### 1.3 人 amylin / IAPP（非 Aβ 淀粉样毒性肽）

| # | 完整题目 | 期刊 / 年 | DOI | PMID |
|---|---|---|---|---|
| B6 | **Rapid, scalable assay of amylin-β amyloid co-aggregation in brain tissue and blood** | *J Biol Chem* 2023; 299:104682 | [10.1016/j.jbc.2023.104682](https://doi.org/10.1016/j.jbc.2023.104682) | [37030503](https://pubmed.ncbi.nlm.nih.gov/37030503/) |
| B7 | **Skin capillary amylin deposition resembles brain amylin vasculopathy in rats** | *J Stroke Cerebrovasc Dis* 2023; 32:107300 | [10.1016/j.jstrokecerebrovasdis.2023.107300](https://doi.org/10.1016/j.jstrokecerebrovasdis.2023.107300) | [37572602](https://pubmed.ncbi.nlm.nih.gov/37572602/) |
| B8 | **A unifying framework for amyloid-mediated membrane damage: The lipid-chaperone hypothesis** | *Biochim Biophys Acta Proteins Proteom* 2022; 1870:140767 | [10.1016/j.bbapap.2022.140767](https://doi.org/10.1016/j.bbapap.2022.140767) | [35144022](https://pubmed.ncbi.nlm.nih.gov/35144022/) |

**对计算的含义**：IAPP/α-syn 等共享 **膜损伤** 计算问题（肽–脂质、孔道样聚集）→ 可用 **膜 MD（CHARMM-GUI 双层）**，不必走 Aβ 专有假说。

---

## 2 分子对接（Docking）——具体做法

### 2.1 方法学总则

| 步骤 | 具体做法 | 注意 |
|---|---|---|
| 1. 准备肽 | 用 AF3 或肽结构服务器生成 **多构象**（≥5–10 个聚类代表）；短肽 7–15 aa **禁止只对接 1 个刚性构象** | 短肽柔性大 |
| 2. 准备靶标 | 按假说选：**膜（隐式/显式）**、**CLIC1（LL-37 类比）**、**金属结合口袋**、或自组装界面；下载 PDB，去水、补残基、加氢、分配电荷 | 靶要与非 Aβ 锚点一致 |
| 3. 对接盒 | 覆盖结合位点 + 边距 ≥1 nm；盲目对接需全蛋白/全膜补丁 | 记录网格参数 |
| 4. 采样 | Vina：exhaustiveness ≥16–32；或 HADDOCK 柔性对接（肽侧链 + 界面残基） | 输出 top 20–50 |
| 5. 筛选 | 结合能 + 簇大小 + 界面残基合理性 + 与 MD 兼容的取向 | 对接分 ≠ 毒性 |
| 6. 输出 | 每个肽：最优 3 簇的 PDB、界面残基表（距离 <4 Å）、氢键/盐桥列表 | 写入补充材料 |

### 2.2 对接相关可参考文献（完整题目）

| # | 完整题目 | 用途 | 期刊 / 年 | DOI | PMID |
|---|---|---|---|---|---|
| C1 | **Accurate structure prediction of biomolecular interactions with AlphaFold 3** | 复合物/肽–蛋白初始模型；**不能替代对接+MD 验证** | *Nature* 2024; 630:493-500 | [10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w) | [38718835](https://pubmed.ncbi.nlm.nih.gov/38718835/) |
| C2 | **LL-37: Structures, Antimicrobial Activity, and Influence on Amyloid-Related Diseases** | LL-37 螺旋/膜取向结构信息，指导对接姿态 | *Biomolecules* 2024 | [10.3390/biom14030320](https://doi.org/10.3390/biom14030320) | [38540740](https://pubmed.ncbi.nlm.nih.gov/38540740/) |
| C3 | **Human antimicrobial peptide LL-37 contributes to Alzheimer's disease progression** | 指明计算靶点方向（CLIC1 相互作用），对接后应用实验逻辑验证 | *Mol Psychiatry* 2022 | [10.1038/s41380-022-01790-6](https://doi.org/10.1038/s41380-022-01790-6) | [36138130](https://pubmed.ncbi.nlm.nih.gov/36138130/) |

### 2.3 按假说的对接方案（三选一或并行）

**方案 D-A：类 LL-37（膜 / CLIC1）**  
1. 获取 CLIC1 结构（PDB 检索 hCLIC1）；  
2. 肽多构象 → 对接 CLIC1 膜整合相关表面（参考 Chen 2022 的互作叙事）；  
3. 并行：肽与 **阴离子磷脂膜** 的取向对接/吸附模拟（见 MD §3.3）。  

**方案 D-B：类 PrP106–126（自组装 / 膜）**  
1. 肽–肽对接构建寡聚体种子（二聚→六聚试探）；  
2. 寡聚体与膜表面对接；  
3. 与 PrP106–126 对照肽做 **同一流程** 对比界面。  

**方案 D-C：金属配位（仅当序列含 His/Cys/Asp/Glu 等）**  
1. 在肽 N 端/侧链设置 Cu²⁺/Fe²⁺/Zn²⁺ 配位对接或配位几何约束；  
2. 参考金属–肽配位综述选择配位数 4–6；  
3. Zn 只作结构对照，**不写 Fenton**。  

参考文献（金属–肽结构化学）：  

| # | 完整题目 | 期刊 / 年 | DOI | PMID |
|---|---|---|---|---|
| C4 | **Bioinorganic chemistry of copper and zinc ions coordinated to amyloid-beta peptide** | *Dalton Trans* 2009 | [10.1039/b813398k](https://doi.org/10.1039/b813398k) | [19322475](https://pubmed.ncbi.nlm.nih.gov/19322475/) |
| C5 | **Metal Binding of Alzheimer's Amyloid-β and Its Effect on Peptide Self-Assembly** | *Acc Chem Res* 2023; 56:2653-2663 | [10.1021/acs.accounts.3c00370](https://doi.org/10.1021/acs.accounts.3c00370) | [37733746](https://pubmed.ncbi.nlm.nih.gov/37733746/) |
| C6 | **Molecular Insights into the Effect of Metals on Amyloid Aggregation** | *Methods Mol Biol* 2022; 2340:121-137 | [10.1007/978-1-0716-1546-1_7](https://doi.org/10.1007/978-1-0716-1546-1_7) | [35167073](https://pubmed.ncbi.nlm.nih.gov/35167073/) |

> 说明：C4–C6 讲的是 **金属–肽计算/结构方法**，引用时写“金属–肽配位与聚集的计算方法参照”，**不要**写成“我们的肽是 Aβ”。

### 2.4 对接结果允许 / 禁止表述

| 允许 | 禁止 |
|---|---|
| “与 CLIC1 形成可重复界面，主要接触残基为…” | “对接证明该肽导致 AD” |
| “相对对接评分排序为肽 A>B>C” | “Kd = nM（无实验）” |
| “配位构象提示 His 可参与 Cu 结合，待 MD/QM 验证” | “已证实金属毒性机制” |

---

## 3 分子动力学（MD）——具体做法

### 3.1 方法学权威文献（完整题目）

| # | 完整题目 | 期刊 / 年 | DOI | PMID |
|---|---|---|---|---|
| M1 | **Molecular Dynamics Simulation for All** | *Neuron* 2018; 99:1129-1143 | [10.1016/j.neuron.2018.08.011](https://doi.org/10.1016/j.neuron.2018.08.011) | [30236283](https://pubmed.ncbi.nlm.nih.gov/30236283/) |
| M2 | **A unifying framework for amyloid-mediated membrane damage: The lipid-chaperone hypothesis** | *BBA Proteins Proteom* 2022 | [10.1016/j.bbapap.2022.140767](https://doi.org/10.1016/j.bbapap.2022.140767) | [35144022](https://pubmed.ncbi.nlm.nih.gov/35144022/) |
| M3 | **Methods for analyzing the coordination and aggregation of metal-amyloid-β** | *Metallomics* 2023; 15:mfac102 | [10.1093/mtomcs/mfac102](https://doi.org/10.1093/mtomcs/mfac102) | [36617236](https://pubmed.ncbi.nlm.nih.gov/36617236/) |
| M4 | **PHB2 Alleviates Neurotoxicity of Prion Peptide PrP(106-126) via PINK1/Parkin-Dependent Mitophagy** | *IJMS* 2023 | [10.3390/ijms242115919](https://doi.org/10.3390/ijms242115919) | [37958902](https://pubmed.ncbi.nlm.nih.gov/37958902/) |

### 3.2 标准水溶液 MD（肽–蛋白或肽单体/寡聚）

| 步骤 | 具体参数建议 |
|---|---|
| 力场 | 蛋白/肽：ff19SB 或 CHARMM36m；水：TIP3P 或 OPC |
| 盒子 | 肽/复合物边缘 ≥1.0–1.2 nm；立方或十二面体 |
| 离子 | 0.15 M NaCl，电中性 |
| 最小化 | 最陡下降至 Fmax <1000 kJ/mol/nm |
| 平衡 | NVT 100–500 ps（位置限制）→ NPT 1–5 ns |
| 生产 | **≥200–500 ns/条**；短肽自组装可 **1 μs** 级 |
| 重复 | **≥3 条独立轨迹**（不同初速/不同对接簇） |
| 分析 | RMSD/RMSF、回转半径、二级结构（DSSP）、氢键占有率、接触图、聚类（GROMOS/TTClust）、（寡聚）链间 β-sheet |

**收敛判据**：后半段 RMSD 平台；3 次重复主结论一致（界面残基重叠 ≥70% 或排序不变）。

### 3.3 膜 MD（强烈推荐：非 Aβ 毒性肽共性是膜损伤）

依据 M2（IAPP/α-syn 等膜损伤统一框架）：

| 步骤 | 具体做法 |
|---|---|
| 1 | CHARMM-GUI 构建双层：如 POPC:POPS = 4:1 或含脑苷脂的神经元样膜 |
| 2 | 肽初始：水相靠近膜 或 部分插入（对接取向） |
| 3 | 平衡膜面积（NPγT 或半各向异性 NPT）至面积/脂稳定 |
| 4 | 生产 ≥500 ns；分析：插入深度、倾角、序参数扰动、水缺陷/孔道、脂翻转 |
| 5 | 对照：PrP106–126 或 LL-37 同膜条件各跑 1–2 条 |

### 3.4 金属–肽 MD（可选）

| 步骤 | 具体做法 |
|---|---|
| 参数 | Cu²⁺/Fe²⁺/Fe³⁺/Zn²⁺ 使用 **12-6-4 或 QM 拟合非键参数**，禁用裸默认金属参数 |
| 分析 | 金属–供体原子距离时间序列、配位数、配体交换、逸出事件 |
| Zn | 只报告结构稳定性；**禁止**写 Zn–Fenton/ROS |
| 文献做法 | 参考 C5 Abelein 2023（金属–肽动态平衡与聚集）；C6 Miller 2022（金属影响聚集的分子模拟章节） |

### 3.5 MD 输出清单（写进报告/论文方法）

1. 轨迹与代表性帧 PDB  
2. RMSD/RMSF 图（含 3 次重复）  
3. 界面接触表（占有率 >50% 的残基对）  
4. 若做膜：插入深度与膜厚度扰动  
5. 若做金属：配位驻留率  
6. 明确一句：**MD 稳定 ≠ 神经毒性已证实**

---

## 4 结合自由能：MM/GBSA、MM/PBSA——具体做法

### 4.1 参考文献（完整题目）

| # | 完整题目 | 期刊 / 年 | DOI | PMID |
|---|---|---|---|---|
| G1 | **The MM/PBSA and MM/GBSA methods to estimate ligand-binding affinities** | *Expert Opin Drug Discov* 2015; 10:449-461 | [10.1517/17460441.2015.1032936](https://doi.org/10.1517/17460441.2015.1032936) | [25835573](https://pubmed.ncbi.nlm.nih.gov/25835573/) |

### 4.2 操作要点

| 项目 | 做法 |
|---|---|
| 输入 | **平衡后 MD 轨迹**（去掉前 20–50 ns）；隔帧抽 100–200 帧 |
| 方法 | MM/GBSA（快速排序）为主；关键体系可加 MM/PBSA 对照 |
| 比较 | **仅 12 条肽对同一受体/同一膜吸附模型的相对 ΔG** |
| 熵 | 可选 nmode 或交互熵；报告是否含熵 |
| 金属体系 | 慎用；配位键体系优先 QM 校正或只报无金属体系 GBSA |
| 误差 | 报告平均值 ± SD（帧间 + 重复间） |
| 禁止 | 把 GBSA 数值写成实验 Kd；跨不同受体直接比绝对值 |

---

## 5 量化计算：QM/MM 与 DFT——具体做法

### 5.1 参考文献（完整题目）

| # | 完整题目 | 期刊 / 年 | DOI | PMID |
|---|---|---|---|---|
| Q1 | **QM/MM methods for biomolecular systems** | *Angew Chem Int Ed* 2009; 48:1198-1229 | [10.1002/anie.200802019](https://doi.org/10.1002/anie.200802019) | [19173328](https://pubmed.ncbi.nlm.nih.gov/19173328/) |
| Q2 | **Bioinorganic chemistry of copper and zinc ions coordinated to amyloid-beta peptide** | *Dalton Trans* 2009 | [10.1039/b813398k](https://doi.org/10.1039/b813398k) | [19322475](https://pubmed.ncbi.nlm.nih.gov/19322475/) |
| Q3 | **Metal Binding of Alzheimer's Amyloid-β and Its Effect on Peptide Self-Assembly** | *Acc Chem Res* 2023 | [10.1021/acs.accounts.3c00370](https://doi.org/10.1021/acs.accounts.3c00370) | [37733746](https://pubmed.ncbi.nlm.nih.gov/37733746/) |

（Q2/Q3 用于 **配位几何与金属–肽电子结构方法论**，引用时强调方法而非 Aβ 身份。）

### 5.2 何时做 QM/MM 或 DFT

- MD 显示 **稳定金属配位** 的 Top 2–4 条肽；  
- 或需比较 **肽–Cu vs 对照肽–Cu** 相对配位能（螯合/夺金属假说）；  
- 纯有机肽无金属、无化学反应问题时，**可不做 DFT**，MD+GBSA 足够排序。

### 5.3 具体设置建议

| 项目 | 建议 |
|---|---|
| QM 区 | 金属 + 第一配位层残基/主链 O/N + 关键第二层（H 键网络） |
| 边界 | 氢连接原子；或 ONIOM 机械嵌入/电子嵌入 |
| 泛函/基组 | 过渡金属：ωB97X-D / B3LYP-D3 / M06 等 + def2-SVP 优化，def2-TZVP 单点；注明色散校正 |
| 自旋 | Cu²⁺：二重态（d⁹）；Fe²⁺/Fe³⁺：高低自旋均试；**Zn²⁺：闭壳层单重态** |
| 溶剂 | SMD/PCM 或 QM/MM 显式水第一层 |
| 输出 | 优化几何、配位键长/角、NBO/自旋密度、相对结合能（ΔE_coord）、（可选）还原势趋势 |
| 校准 | 能与实验光谱对照最好；否则只报相对排序 |

### 5.4 量化结论边界

| 允许 | 禁止 |
|---|---|
| “Cu 配位几何为 4N/3N1O，与文献金属–肽配位范围一致” | “DFT 证明产生神经毒性 H₂O₂” |
| “相对配位能肽 X 强于对照肽” | “已证实 Fenton 机制” |
| “Zn 配位稳定但无氧化还原活性” | “Zn 介导 ROS 毒性” |

---

## 6 12 条候选肽：可执行的分步 SOP（计算侧）

### Stage 0 — 输入与对照

1. 整理 12 条序列、净电荷、His/Cys 含量、疏水矩。  
2. 设立对照：**PrP106–126**、**LL-37**（或活性片段）、打乱序列肽。  
3. 文献锚点：B1–B5（非 Aβ 毒性肽）。

### Stage 1 — 构象 + 对接（约 1–2 周）

1. AF3/多构象 → 聚类。  
2. 按主假说选 D-A / D-B / D-C。  
3. 每肽保留 3 个对接簇进入 MD。  
4. 参考文献题目：C1, C2, C3（及金属时 C4–C6）。

### Stage 2 — MD（约 3–6 周）

1. 水溶液复合物 MD：200–500 ns × 3。  
2. 膜 MD（推荐）：500 ns×（候选子集 + LL-37/PrP 对照）。  
3. 金属矩阵（可选）：Cu/Fe/Zn 分体系。  
4. 参考文献题目：M1, M2, M3, M4。

### Stage 3 — MM/GBSA 排序（约 1 周）

1. 对稳定体系算相对 ΔG。  
2. 输出 12→4–6 条计算先导。  
3. 参考文献题目：G1。

### Stage 4 — QM/MM 或 DFT（约 1–2 周，仅头部）

1. 稳定 Cu/Fe 配位者做配位能与电子结构。  
2. 参考文献题目：Q1, Q2, Q3。

### Stage 5 — 交付物

| 交付 | 内容 |
|---|---|
| 表 1 | 12 肽对接得分与界面残基 |
| 表 2 | MD 稳定性与接触占有率 |
| 表 3 | MM/GBSA 相对排序 |
| 表 4 | （可选）DFT 配位几何与相对能 |
| 图 | RMSD、膜插入、配位距离 |
| 声明 | 全部为结构假设；毒性需对照 PrP/LL-37 的细胞实验 |

---

## 7 完整参考文献题录表（计算 + 非 Aβ 锚点）

### 7.1 计算方法学（优先精读）

| ID | 完整题目 | 作者 | 期刊 | 年 | DOI | PMID |
|---|---|---|---|---|---|---|
| C1 | Accurate structure prediction of biomolecular interactions with AlphaFold 3 | Abramson J, et al. | *Nature* 630:493-500 | 2024 | 10.1038/s41586-024-07487-w | 38718835 |
| M1 | Molecular Dynamics Simulation for All | Hollingsworth SA, Dror RO | *Neuron* 99:1129-1143 | 2018 | 10.1016/j.neuron.2018.08.011 | 30236283 |
| G1 | The MM/PBSA and MM/GBSA methods to estimate ligand-binding affinities | Genheden S, Ryde U | *Expert Opin Drug Discov* 10:449-461 | 2015 | 10.1517/17460441.2015.1032936 | 25835573 |
| Q1 | QM/MM methods for biomolecular systems | Senn HM, Thiel W | *Angew Chem Int Ed* 48:1198-1229 | 2009 | 10.1002/anie.200802019 | 19173328 |
| M2 | A unifying framework for amyloid-mediated membrane damage: The lipid-chaperone hypothesis | Tempra C, et al. | *BBA Proteins Proteom* 1870:140767 | 2022 | 10.1016/j.bbapap.2022.140767 | 35144022 |
| C5 | Metal Binding of Alzheimer's Amyloid-β and Its Effect on Peptide Self-Assembly | Abelein A | *Acc Chem Res* 56:2653-2663 | 2023 | 10.1021/acs.accounts.3c00370 | 37733746 |
| M3 | Methods for analyzing the coordination and aggregation of metal-amyloid-β | Park S, et al. | *Metallomics* 15:mfac102 | 2023 | 10.1093/mtomcs/mfac102 | 36617236 |
| C6 | Molecular Insights into the Effect of Metals on Amyloid Aggregation | Miller Y | *Methods Mol Biol* 2340:121-137 | 2022 | 10.1007/978-1-0716-1546-1_7 | 35167073 |
| C4 | Bioinorganic chemistry of copper and zinc ions coordinated to amyloid-beta peptide | Faller P, Hureau C | *Dalton Trans* (7):1080-1094 | 2009 | 10.1039/b813398k | 19322475 |

### 7.2 非 Aβ 毒性肽生物学锚点（计算服务的对象）

| ID | 完整题目 | 作者 | 期刊 | 年 | DOI | PMID |
|---|---|---|---|---|---|---|
| B1 | Neurotoxicity of a prion protein fragment | Forloni G, et al. | *Nature* 362:543-546 | 1993 | 10.1038/362543a0 | 8464494 |
| B2 | Review: PrP 106-126 - 25 years after | Forloni G, et al. | *Neuropathol Appl Neurobiol* 45:430-440 | 2019 | 10.1111/nan.12538 | 30635947 |
| B3 | PHB2 Alleviates Neurotoxicity of Prion Peptide PrP(106-126) via PINK1/Parkin-Dependent Mitophagy | Zheng X, et al. | *Int J Mol Sci* 24:15919 | 2023 | 10.3390/ijms242115919 | 37958902 |
| B4 | Human antimicrobial peptide LL-37 contributes to Alzheimer's disease progression | Chen X, et al. | *Mol Psychiatry* 27:4790-4799 | 2022 | 10.1038/s41380-022-01790-6 | 36138130 |
| B5 | LL-37: Structures, Antimicrobial Activity, and Influence on Amyloid-Related Diseases | Bhattacharjya S, et al. | *Biomolecules* 14:320 | 2024 | 10.3390/biom14030320 | 38540740 |
| B6 | Rapid, scalable assay of amylin-β amyloid co-aggregation in brain tissue and blood | Kotiya D, et al. | *J Biol Chem* 299:104682 | 2023 | 10.1016/j.jbc.2023.104682 | 37030503 |
| B7 | Skin capillary amylin deposition resembles brain amylin vasculopathy in rats | Das S, et al. | *J Stroke Cerebrovasc Dis* 32:107300 | 2023 | 10.1016/j.jstrokecerebrovasdis.2023.107300 | 37572602 |

### 7.3 链接速查（复制用）

- AF3: https://doi.org/10.1038/s41586-024-07487-w  
- MD for All: https://doi.org/10.1016/j.neuron.2018.08.011  
- MM/GBSA: https://doi.org/10.1517/17460441.2015.1032936  
- QM/MM: https://doi.org/10.1002/anie.200802019  
- 膜损伤框架: https://doi.org/10.1016/j.bbapap.2022.140767  
- LL-37→AD: https://doi.org/10.1038/s41380-022-01790-6  
- PrP 毒性肽: https://doi.org/10.1038/362543a0  
- Abelein 金属–肽: https://doi.org/10.1021/acs.accounts.3c00370  

---

## 8 方案正文可粘贴段落（计算方法）

> 本研究候选肽为非 Aβ 序列。计算工作对标非 Aβ 神经毒性肽研究范式：PrP106–126 短肽神经毒性（Forloni et al., *Nature*, 1993; Forloni et al., 2019）、人源 LL-37 推动 AD 相关病理（Chen et al., *Mol Psychiatry*, 2022）以及 amylin/IAPP 等膜损伤型淀粉样肽（Tempra et al., 2022; Despa 研究线）。结构预测采用 AlphaFold 3 生成肽及复合物多构象（Abramson et al., *Nature*, 2024），继以分子对接获得结合姿态假设；分子动力学在显式溶剂及（推荐）磷脂双层中评估结合稳定性、膜插入与（可选）金属配位驻留（Hollingsworth & Dror, *Neuron*, 2018）。相对结合自由能采用 MM/GBSA 对同系列肽排序（Genheden & Ryde, 2015）。对稳定金属配位体系进一步以 QM/MM 或 DFT 分析配位几何与相对配位能（Senn & Thiel, 2009）。金属–肽配位与聚集的分析方法参照相关生物无机与模拟文献（Faller & Hureau, 2009; Abelein, 2023; Park et al., 2023）。计算结论仅用于候选优先级排序与结构假说生成；神经毒性判定需以 PrP106–126、LL-37 等为阳性对照的实验读出裁决。

---

## 9 说明

1. 环境无 **officecli**，本 docx 用 **python-docx** 生成标准 Office Open XML，Word 2007+ / WPS / Google Docs 可打开。  
2. 题目、DOI、PMID 均经 PubMed 核验。  
3. C4–C6、Abelein 等含 “amyloid-β” 字样处，仅作 **金属–肽计算与配位方法** 参考，不将候选肽等同 Aβ。  
4. 具体软件版本、力场文件名请按课题组集群环境在正式 SOP 中替换。
