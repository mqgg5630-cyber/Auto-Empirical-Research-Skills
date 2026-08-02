# 金属离子相关毒性肽与 AD 关联靶点——核心文献整理

**（AERS 文献核验；截至 2026-08-02｜本版重点：Cu/Fe/Zn–肽毒性机制 + Aβ/tau/ApoE4/铁稳态；AChE 已完成对接，本版暂不展开）**

> **核验声明**：下列文献均经 PubMed E-utilities（esearch / esummary / efetch）核对标题、期刊、年卷页、DOI、PMID。链接为 PubMed 或 doi.org。
>
> **本版定位**：按用户要求——**主要整理“后面离子的毒性肽”及 Aβ、tau、ApoE4、ferritin/transferrin 等方向的具体文献**；AChE/BChE 与 PAS 对接工作已完成，**本文件不作为 AChE 文献综述**。计算（AF3/MD/QM）仅在第 6 节作方法索引，不占主体。
>
> **关键边界**：Wang 等 2024（*ACS Chem Neurosci*）证明的是神经肽–Aβ 互作与部分**保护/抑聚集**，**不能**当作“毒性肽”主证据（见 §1.5）。

---

## 0 阅读导航与概念地图

### 0.1 “金属相关毒性肽”在文献里指什么

领域共识中的**经典模板**是 **Aβ 肽本身**（尤其 Aβ1–42）在 **Cu²⁺/Fe³⁺** 存在下：

```
肽配位金属 → 金属还原（Cu²⁺→Cu⁺ / Fe³⁺→Fe²⁺）
    → 催化/化学计量生成 H₂O₂
    → Fenton/Haber–Weiss 产生 •OH
    → 脂质过氧化 / 蛋白氧化
    → 神经细胞毒性
```

因此“毒性肽”文献主线 = **肽–金属配位化学 + ROS + 细胞毒性**，而不是“任意短肽对接得分高”。

### 0.2 本整理覆盖的五块

| 板块 | 科学问题 | 代表文献（详见正文） |
|---|---|---|
| **A. 金属–毒性肽（核心）** | Aβ 如何借 Cu/Fe 产 H₂O₂ 并致毒 | Huang 1999 *Biochemistry*；Huang 1999 *JBC*；Opazo 2002 *JBC* |
| **B. 金属分型（Cu/Fe vs Zn）** | 谁能做 Fenton 型 ROS 金属；Zn 做什么 | Bush 1994 *Science*；Faller & Hureau 2009；Sensi 2009 *NRN* |
| **C. 氧化应激整合** | ROS–脂质过氧化–AD 病理总图 | Cheignon 2018；Butterfield 2002；Greenough 2013 |
| **D. Aβ 寡聚体毒性（非必须金属）** | 可溶性寡聚体的突触毒性读出 | Walsh 2002 *Nature* |
| **E. 其他靶点边界** | tau / ApoE4 / ferritin–transferrin 怎么定位 | Guo & Lee 2011；Huang & Mahley 2014；Ayton 2015；Zecca 2004；Ward 2014 |
| **F. 反例/勿误用** | 神经肽–Aβ 互作 ≠ 毒性肽 | Wang 2024 *ACS Chem Neurosci* |

### 0.3 金属角色一句话

| 离子 | 在毒性肽文献中的角色 | 能否直接写“Fenton 产 ROS” |
|---|---|---|
| **Cu²⁺/Cu⁺** | 主氧化还原金属；Aβ–Cu 类金属酶产 H₂O₂ | **可以**（有直接实验） |
| **Fe³⁺/Fe²⁺** | 可被 Aβ 还原并参与 H₂O₂/•OH 路径 | **可以** |
| **Zn²⁺** | 高亲和促 Aβ 聚集；可**抑制** Cu–Aβ 产 H₂O₂；d¹⁰ 无单电子循环 | **不可以** |

---

## 1 核心板块 A：金属离子相关“毒性肽”文献卡片

> 下列 3 篇构成 **Cu/Fe–Aβ 毒性肽** 的因果骨架，建议作为本课题金属矩阵与（未来）ROS 表述的**一级引用**。

---

### 1.1 【主文献-1】Huang et al., 1999 — Aβ 经金属还原直接产 H₂O₂

| 字段 | 内容 |
|---|---|
| 作者 | Huang X, Atwood CS, … Bush AI |
| 题名 | The A beta peptide of Alzheimer's disease directly produces hydrogen peroxide through metal ion reduction |
| 期刊 | *Biochemistry* 1999; **38**(24):7609-7616 |
| DOI | [10.1021/bi990438f](https://doi.org/10.1021/bi990438f) |
| PMID | [10386999](https://pubmed.ncbi.nlm.nih.gov/10386999/) |

**证明了什么（可核验要点）**

1. 人源 Aβ **直接**通过还原 **Fe(III) 或 Cu(II)** 产生 **H₂O₂**。
2. 光谱证明：Aβ 将 Fe³⁺→Fe²⁺、Cu²⁺→Cu⁺；亚化学计量的 Fe²⁺/Cu⁺ 即可驱动 O₂→H₂O₂。
3. 有 Cu/Fe 时 TBARS 阳性，与 **•OH** 生成相容。
4. 产量与病理相关性排序：**Aβ1–42 ≫ Aβ1–40 > 鼠 Aβ1–40**。

**对本课题的用法**

- 定义“金属相关毒性肽”的**化学金标准叙事**：配位 → 还原 → H₂O₂。
- 计算侧：若候选肽拟类比此机制，QM/MM 应关注 **金属还原趋势 / 配位 His 等**，但**不能**仅凭计算宣称已产 H₂O₂。
- 引用句示例：*“Aβ 可经 Cu/Fe 还原直接生成 H₂O₂（Huang et al., Biochemistry 1999）。”*

---

### 1.2 【主文献-2】Huang et al., 1999 — Cu(II) 增强 Aβ 神经毒性，且与无细胞 H₂O₂/金属还原定量相关

| 字段 | 内容 |
|---|---|
| 作者 | Huang X, Cuajungco MP, Atwood CS, … Bush AI |
| 题名 | Cu(II) potentiation of Alzheimer abeta neurotoxicity. Correlation with cell-free hydrogen peroxide production and metal reduction |
| 期刊 | *J Biol Chem* 1999; **274**(52):37111-37116 |
| DOI | [10.1074/jbc.274.52.37111](https://doi.org/10.1074/jbc.274.52.37111) |
| PMID | [10601271](https://pubmed.ncbi.nlm.nih.gov/10601271/) |

**证明了什么**

1. **Cu(II) 显著增强** 培养神经元中 Aβ 的神经毒性。
2. 毒性增强幅度与序列一致：**Aβ1–42 > Aβ1–40 ≫ 鼠/小鼠 Aβ1–40**。
3. 上述排序与 **无细胞体系** 中：Cu²⁺→Cu⁺ 还原能力、H₂O₂ 产量 **定量相关**。
4. Aβ1–42–Cu 复合物形式还原电位很高（约 +500–550 mV vs Ag/AgCl），呈强还原性铜蛋白特征。

**对本课题的用法**

- 把 **“化学产 ROS”** 接到 **“细胞毒性”** 的关键桥梁文献。
- 因果表述模板：毒性 ∝ 金属还原 ∝ H₂O₂（同序列梯度）。
- 若比较 12 条候选肽，文献提示应做 **±Cu 矩阵**，并看毒性是否与还原/H₂O₂ 同向（实验阶段；本版只标文献逻辑）。

---

### 1.3 【主文献-3】Opazo et al., 2002 — Aβ–Cu 的“类金属酶”活性：催化底物产神经毒性 H₂O₂

| 字段 | 内容 |
|---|---|
| 作者 | Opazo C, Huang X, Cherny RA, … Bush AI |
| 题名 | Metalloenzyme-like activity of Alzheimer's disease beta-amyloid. Cu-dependent catalytic conversion of dopamine, cholesterol, and biological reducing agents to neurotoxic H(2)O(2) |
| 期刊 | *J Biol Chem* 2002; **277**(43):40302-40308 |
| DOI | [10.1074/jbc.M206428200](https://doi.org/10.1074/jbc.M206428200) |
| PMID | [12192006](https://pubmed.ncbi.nlm.nih.gov/12192006/) |

**证明了什么**

1. Aβ1–42 结合最多约 **2 eq Cu²⁺**，形成类似 CuZn-SOD 位点的寡聚复合物。
2. 在生物还原底物（多巴胺、L-DOPA、维生素 C、**胆固醇** 等）存在下，**催化** 持续产生 H₂O₂（底物耗尽前可循环）。
3. 单独 Cu²⁺ 或单独还原剂在相同条件下不形成该 H₂O₂；活性可被 **抗 Aβ 抗体、Cu 螯合剂、Zn²⁺** 抑制。
4. 细胞：无 Cu 时 Aβ 不毒；多巴胺可显著放大 Aβ1–42·Cu 毒性。

**对本课题的用法**

- “毒性肽”不一定要化学计量耗金属——**催化循环**更危险。
- Zn²⁺ 在此文中是 **抑制剂**（抑 Cu–Aβ 产 H₂O₂），与 §2 Zn 定位一致。
- 计算含义：稳定 Cu 配位 + 可及的氧化还原位点，只说明**具备类金属酶的结构前提**；催化周转率必须实验。

---

### 1.4 三篇如何串成一条证据链（汇报可用）

| 步骤 | 文献 | 一句话 |
|---|---|---|
| ① 化学 | Huang *Biochemistry* 1999 | Aβ + Cu/Fe → 还原金属 → H₂O₂ / •OH 化学 |
| ② 细胞相关 | Huang *JBC* 1999 | Cu 增强神经毒性，且与无细胞 H₂O₂、还原能力同序 |
| ③ 催化与底物 | Opazo *JBC* 2002 | Aβ–Cu 募集生理还原剂，**催化** 产神经毒性 H₂O₂；螯合/Zn 可抑 |

**可写结论（谨慎）**：人源 Aβ（尤其 1–42）是目前文献中证据最完整的 **Cu/Fe 依赖促氧化毒性肽** 范式。  
**不可写**：你们的 12 条候选肽“已经是”同类毒性肽——尚无对等实验链。

---

### 1.5 【反例】Wang et al., 2024 — 不能当作毒性肽依据

| 字段 | 内容 |
|---|---|
| 作者 | Wang D, Wang G, Wang X, Ren Z, Jia C |
| 题名 | Native Mass Spectrometry-Centric Approaches Revealed That Neuropeptides Frequently Interact with Amyloid-β |
| 期刊 | *ACS Chem Neurosci* 2024; **15**(15):2719-2728 |
| DOI | [10.1021/acschemneuro.4c00075](https://doi.org/10.1021/acschemneuro.4c00075) |
| PMID | [39066700](https://pubmed.ncbi.nlm.nih.gov/39066700/) |

| 问题 | 裁决 |
|---|---|
| 神经肽–Aβ 互作是否常见？ | **是**（6/12 native MS 复合物） |
| 是否证明“毒性肽”？ | **否**——leptin/cerebellin **抑聚集、降细胞毒**；leptin **螯合 Cu** 偏保护 |
| kisspeptin？ | 可 **促** Aβ 聚集，但仍非完整 Cu–ROS–毒性链 |
| HDOCK 对接？ | 仅界面假说，不能定毒性 |

**引用规范**：可引作“短肽与 Aβ 非共价互作并不罕见；功能方向须另判”。**禁止**引作毒性肽主证据。

---

## 2 核心板块 B：Cu / Fe / Zn 分型文献

### 2.1 Zn²⁺：促聚集为主，不是 Fenton 型 ROS 金属

#### 2.1.1 Bush et al., 1994 — Zn 快速诱导 Aβ 淀粉样形成

| 字段 | 内容 |
|---|---|
| 作者 | Bush AI, Pettingell WH, Multhaup G, … Tanzi RE |
| 题名 | Rapid induction of Alzheimer A beta amyloid formation by zinc |
| 期刊 | *Science* 1994; **265**(5177):1464-1467 |
| DOI | [10.1126/science.8073293](https://doi.org/10.1126/science.8073293) |
| PMID | [8073293](https://pubmed.ncbi.nlm.nih.gov/8073293/) |

**要点**：人 Aβ1–40 与 Zn 特异可饱和结合；**>300 nM Zn** 迅速诱导可染色淀粉样；鼠 Aβ 结合弱、不易被 Zn 诱导——与啮齿类少见脑 Aβ 斑块的讨论相关。  
**用法**：Zn = **聚集诱导金属** 的经典起点；与 Cu 的 ROS 角色分开写。

#### 2.1.2 Faller & Hureau, 2009 — Cu/Zn–Aβ 生物无机化学专论

| 字段 | 内容 |
|---|---|
| 作者 | Faller P, Hureau C |
| 题名 | Bioinorganic chemistry of copper and zinc ions coordinated to amyloid-beta peptide |
| 期刊 | *Dalton Trans* 2009; (7):1080-1094 |
| DOI | [10.1039/b813398k](https://doi.org/10.1039/b813398k) |
| PMID | [19322475](https://pubmed.ncbi.nlm.nih.gov/19322475/) |

**要点**：系统整理 Cu、Zn 与 Aβ 的配位模式、亲和力、对聚集与活性氧的不同影响——**写金属–肽配位计算/讨论时的结构化学首选综述**。

#### 2.1.3 Sensi et al., 2009 — 中枢 Zn 生理与病理（非 Fenton 叙事）

| 字段 | 内容 |
|---|---|
| 作者 | Sensi SL, Paoletti P, Bush AI, Sekler I |
| 题名 | Zinc in the physiology and pathology of the CNS |
| 期刊 | *Nat Rev Neurosci* 2009; **10**(11):780-791 |
| DOI | [10.1038/nrn2734](https://doi.org/10.1038/nrn2734) |
| PMID | [19826435](https://pubmed.ncbi.nlm.nih.gov/19826435/) |

**要点**：Zn 为 CNS 信号与稳态离子；病理涉及兴奋毒性、线粒体、Zn–Aβ 等。  
**硬约束**：Zn²⁺ = d¹⁰ 闭壳层，**无 Cu/Fe 式单电子 Fenton 循环**。计算可做 Zn 配位，结论不得写“Zn–Fenton 产 ROS”。

### 2.2 Cu–Aβ 产 ROS 的结构/机制综述

#### Hureau & Faller, 2009

| 字段 | 内容 |
|---|---|
| 作者 | Hureau C, Faller P |
| 题名 | Aβ-mediated ROS production by Cu ions: structural insights, mechanisms and relevance to Alzheimer's disease |
| 期刊 | *Biochimie* 2009; **91**(10):1212-1217 |
| DOI | [10.1016/j.biochi.2009.03.013](https://doi.org/10.1016/j.biochi.2009.03.013) |
| PMID | [19332103](https://pubmed.ncbi.nlm.nih.gov/19332103/) |

**要点**：从配位结构解释 Cu–Aβ 如何产 ROS、哪些结构因素决定活性——衔接 Huang/Opazo 实验与配位模型。

### 2.3 金属分型速查表（写作直接可用）

| 维度 | Cu | Fe | Zn |
|---|---|---|---|
| 氧化还原 | 活跃（Cu²⁺/Cu⁺） | 活跃（Fe³⁺/Fe²⁺） | 惰性（d¹⁰） |
| 与 Aβ | 高亲和；催化 H₂O₂ | 可被还原；参与 H₂O₂/•OH | 高亲和；**快速促纤丝/聚集** |
| 毒性主路径 | 促氧化（ROS） | 促氧化 + 铁稳态 | 聚集/信号/线粒体等 |
| 对 Cu–Aβ ROS | 主体 | 可协同 | 文献中可 **抑制** 产 H₂O₂（Opazo） |
| 计算标签 | 氧化还原活性金属 | 同左 | **结构/聚集对照金属** |

---

## 3 核心板块 C：氧化应激与脂质过氧化（把 ROS 接到病理）

### 3.1 Cheignon et al., 2018 — Aβ 与氧化应激总述（首选新综述）

| 字段 | 内容 |
|---|---|
| 作者 | Cheignon C, Tomas M, Bonnefont-Rousselot D, Faller P, Hureau C, Collin F |
| 题名 | Oxidative stress and the amyloid beta peptide in Alzheimer's disease |
| 期刊 | *Redox Biol* 2018; **14**:450-464 |
| DOI | [10.1016/j.redox.2017.10.014](https://doi.org/10.1016/j.redox.2017.10.014) |
| PMID | [29080524](https://pubmed.ncbi.nlm.nih.gov/29080524/) |

**要点**：整合 Aβ–金属氧化还原、H₂O₂/•OH、氧化修饰与 AD 的关系；写“金属–ROS–AD”讨论段的**现代入口综述**。

### 3.2 Butterfield & Lauderback, 2002 — AD 脑脂质过氧化与蛋白氧化

| 字段 | 内容 |
|---|---|
| 作者 | Butterfield DA, Lauderback CM |
| 题名 | Lipid peroxidation and protein oxidation in Alzheimer's disease brain: potential causes and consequences involving amyloid beta-peptide-associated free radical oxidative stress |
| 期刊 | *Free Radic Biol Med* 2002; **32**(11):1050-1060 |
| DOI | [10.1016/S0891-5849(02)00794-3](https://doi.org/10.1016/S0891-5849(02)00794-3) |
| PMID | [12031889](https://pubmed.ncbi.nlm.nih.gov/12031889/) |

**要点**：AD 脑中脂质过氧化（如 4-HNE）与蛋白氧化的病理证据，并与 Aβ 相关自由基应激联系——**ROS → 脂质过氧化** 环节的经典引用。

### 3.3 Greenough et al., 2013 — 金属稳态失衡与 AD 氧化应激

| 字段 | 内容 |
|---|---|
| 作者 | Greenough MA, Camakaris J, Bush AI |
| 题名 | Metal dyshomeostasis and oxidative stress in Alzheimer's disease |
| 期刊 | *Neurochem Int* 2013; **62**(5):540-555 |
| DOI | [10.1016/j.neuint.2012.08.014](https://doi.org/10.1016/j.neuint.2012.08.014) |
| PMID | [22982299](https://pubmed.ncbi.nlm.nih.gov/22982299/) |

**要点**：从金属稳态网络（不仅是肽–金属二元）讨论氧化应激——避免把机制写成“只有肽和离子、没有细胞转运”。

---

## 4 核心板块 D：Aβ 寡聚体毒性（功能读出；可不依赖金属）

### Walsh et al., 2002 — 天然分泌 Aβ 寡聚体抑制海马 LTP

| 字段 | 内容 |
|---|---|
| 作者 | Walsh DM, Klyubin I, Fadeeva JV, … Selkoe DJ |
| 题名 | Naturally secreted oligomers of amyloid beta protein potently inhibit hippocampal long-term potentiation in vivo |
| 期刊 | *Nature* 2002; **416**(6880):535-539 |
| DOI | [10.1038/416535a](https://doi.org/10.1038/416535a) |
| PMID | [11932745](https://pubmed.ncbi.nlm.nih.gov/11932745/) |

**要点**

- 细胞自然产生并分泌的 **Aβ 寡聚体**（非纤丝）在体抑制大鼠海马 **LTP**。
- 免疫耗尽 Aβ 则效应消失；降解单体、保留寡聚体仍抑制 LTP。
- γ-分泌酶抑制阻止寡聚体形成后，介质不再破坏 LTP。

**与金属毒性肽的关系**

- 这是 **突触毒性的功能金标准读出**，机制上可与金属–ROS 并行或交叉，但 **Walsh 本身不是 Cu–H₂O₂ 论文**。
- 若候选肽调节 Aβ 聚集，最终功能结论应落到寡聚体/突触或细胞表型，而不是只看 ThT。

---

## 5 核心板块 E：其他方面的具体文献（tau / ApoE4 / 铁稳态）

> AChE 已做过，此处从略。下列靶点按**证据用途**定位，避免并列成“都是致病结合靶点”。

### 5.1 tau —— 播种–招募，非金属毒性肽主线

| 字段 | 内容 |
|---|---|
| 作者 | Guo JL, Lee VM |
| 题名 | Seeding of normal Tau by pathological Tau conformers drives pathogenesis of Alzheimer-like tangles |
| 期刊 | *J Biol Chem* 2011; **286**(17):15317-15331 |
| DOI | [10.1074/jbc.M110.209296](https://doi.org/10.1074/jbc.M110.209296) |
| PMID | [21372138](https://pubmed.ncbi.nlm.nih.gov/21372138/) |

**要点**：微量预成形 tau 纤丝（pffs）进入细胞后大量募集可溶 tau，形成 NFT 样包涵体；支持 prion-like **播种–招募**。  
**定位**：若候选肽碰 tau，合理问题是“是否影响播种/聚集”，**不是** Cu–Fenton 主叙事。探索性；需先有结合/聚集证据再深化。

### 5.2 ApoE4 —— 遗传风险与多效机制；并桥接铁

#### 5.2.1 Strittmatter et al., 1993 — ApoE4 与晚发 AD / Aβ 结合

| 字段 | 内容 |
|---|---|
| 作者 | Strittmatter WJ, et al. |
| 题名 | Apolipoprotein E: high-avidity binding to beta-amyloid and increased frequency of type 4 allele in late-onset familial Alzheimer disease |
| 期刊 | *PNAS* 1993; **90**(5):1977-1981 |
| DOI | [10.1073/pnas.90.5.1977](https://doi.org/10.1073/pnas.90.5.1977) |
| PMID | [8446617](https://pubmed.ncbi.nlm.nih.gov/8446617/) |

**要点**：确立 ApoE4 等位基因频率升高及与 Aβ 高亲和——ApoE–AD 遗传/结合起点。

#### 5.2.2 Huang & Mahley, 2014 — ApoE 结构与神经生物学功能

| 字段 | 内容 |
|---|---|
| 作者 | Huang Y, Mahley RW |
| 题名 | Apolipoprotein E: structure and function in lipid metabolism, neurobiology, and Alzheimer's diseases |
| 期刊 | *Neurobiol Dis* 2014; **72 Pt A**:3-12 |
| DOI | [10.1016/j.nbd.2014.08.025](https://doi.org/10.1016/j.nbd.2014.08.025) |
| PMID | [25173806](https://pubmed.ncbi.nlm.nih.gov/25173806/) |

**要点**：E2/E3/E4 结构差异（domain interaction 等）与脂代谢、Aβ 清除、tau、神经修复等多效性——**写 ApoE4 机制时的结构–功能首选**。  
**计算注意**：单次对接不能解释遗传风险；至少 E3 vs E4 对照。

### 5.3 ferritin / transferrin —— 铁稳态功能节点（非未验证的“直接致病结合靶点”）

#### 5.3.1 Ayton et al., 2015 — CSF ferritin 预测 AD 结局，受 APOE 调控

| 字段 | 内容 |
|---|---|
| 作者 | Ayton S, Faux NG, Bush AI; ADNI |
| 题名 | Ferritin levels in the cerebrospinal fluid predict Alzheimer's disease outcomes and are regulated by APOE |
| 期刊 | *Nat Commun* 2015; **6**:6760 |
| DOI | [10.1038/ncomms7760](https://doi.org/10.1038/ncomms7760) |
| PMID | [25988319](https://pubmed.ncbi.nlm.nih.gov/25988319/) |

**要点**：CSF ferritin 预测 MCI→AD 与认知下降；水平受 **APOE** 调控——**APOE–铁–AD 结局** 桥梁。  
**定位**：ferritin = **可测的铁稳态/预后节点**，不是默认的“肽直接结合致病靶”。

#### 5.3.2 Zecca et al., 2004 — 脑铁、衰老与神经退行

| 字段 | 内容 |
|---|---|
| 作者 | Zecca L, Youdim MB, Riederer P, Connor JR, Crichton RR |
| 题名 | Iron, brain ageing and neurodegenerative disorders |
| 期刊 | *Nat Rev Neurosci* 2004; **5**(11):863-873 |
| DOI | [10.1038/nrn1537](https://doi.org/10.1038/nrn1537) |
| PMID | [15496864](https://pubmed.ncbi.nlm.nih.gov/15496864/) |

#### 5.3.3 Ward et al., 2014 — 脑铁在衰老与神经退行中的作用

| 字段 | 内容 |
|---|---|
| 作者 | Ward RJ, Zucca FA, Duyn JH, Crichton RR, Zecca L |
| 题名 | The role of iron in brain ageing and neurodegenerative disorders |
| 期刊 | *Lancet Neurol* 2014; **13**(10):1045-1060 |
| DOI | [10.1016/S1474-4422(14)70117-6](https://doi.org/10.1016/S1474-4422(14)70117-6) |
| PMID | [25231526](https://pubmed.ncbi.nlm.nih.gov/25231526/) |

**Zecca + Ward 合用要点**：Tf–TfR1 摄取、ferritin 储存、ferroportin 释放、NTBI 与氧化应激网络。  
**transferrin 定位**：铁转运枢纽；读出应是摄取/饱和度/TfR1 等**功能指标**，对接仅假设生成。

### 5.4 非 AChE 靶点总表（文献 → 怎么用）

| 靶点/主题 | 核心文献 | 证据强项 | 建议用法 | 避免 |
|---|---|---|---|---|
| **Cu/Fe–毒性肽** | Huang 1999×2；Opazo 2002 | 化学+细胞相关+催化 | 金属矩阵与 ROS 叙事一级引用 | 无数据就贴到候选肽上 |
| **Zn** | Bush 1994；Sensi 2009；Faller 2009 | 聚集与生理病理 | 聚集/对照金属 | “Zn–Fenton” |
| **Aβ 寡聚体毒性** | Walsh 2002 | 在体 LTP | 功能读出标准 | 只用 ThT 下功能结论 |
| **tau** | Guo & Lee 2011 | 细胞播种 | 探索性聚集/播种 | 无结合证据的强关联 |
| **ApoE4** | Strittmatter 1993；Huang & Mahley 2014；Ayton 2015 | 遗传+多效+铁桥 | 异构体对照；连铁稳态 | 单构象对接解释风险 |
| **ferritin** | Ayton 2015；Zecca；Ward | 队列+代谢网络 | 功能节点 | “直接致病结合靶点” |
| **transferrin** | Zecca；Ward | 转运共识 | 功能节点 | 同上 |
| **神经肽–Aβ** | Wang 2024 | 互作频率 | 互作旁证 | 毒性肽依据 |

---

## 6 计算侧文献索引（简表；非本版主体）

> 金属–肽后续若做理论计算，方法学引用如下；**不替代** §1 实验范式。

| 方法 | 文献 | DOI / PMID |
|---|---|---|
| AlphaFold 3 | Abramson et al. *Nature* 2024; 630:493-500 | [10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w) / [38718835](https://pubmed.ncbi.nlm.nih.gov/38718835/) |
| MD 正确使用 | Hollingsworth & Dror *Neuron* 2018; 99:1129-1143 | [10.1016/j.neuron.2018.08.011](https://doi.org/10.1016/j.neuron.2018.08.011) / [30236283](https://pubmed.ncbi.nlm.nih.gov/30236283/) |
| MM/PBSA–GBSA | Genheden & Ryde *Expert Opin Drug Discov* 2015; 10:449-461 | [10.1517/17460441.2015.1032936](https://doi.org/10.1517/17460441.2015.1032936) / [25835573](https://pubmed.ncbi.nlm.nih.gov/25835573/) |
| QM/MM | Senn & Thiel *Angew Chem Int Ed* 2009; 48:1198-1229 | [10.1002/anie.200802019](https://doi.org/10.1002/anie.200802019) / [19173328](https://pubmed.ncbi.nlm.nih.gov/19173328/) |
| Cu/Zn–Aβ 配位化学 | Faller & Hureau *Dalton Trans* 2009 | [10.1039/b813398k](https://doi.org/10.1039/b813398k) / [19322475](https://pubmed.ncbi.nlm.nih.gov/19322475/) |

**计算允许表述 / 禁止表述（金属毒性语境）**

| 允许 | 禁止 |
|---|---|
| “配位几何类似 Aβ–Cu 报道的 N/O 供体环境（参见 Faller 2009）” | “计算证明该肽具神经毒性” |
| “Cu 配位稳定，具备进一步检测 H₂O₂ 的结构前提（类比 Huang/Opazo）” | “Zn 通过 Fenton 产生 ROS” |
| “相对配位能提示对 Cu 的亲和可能高于对照肽” | “根据 Wang 2024，该肽为毒性肽” |

---

## 7 总文献表（按板块，含链接）

### 7.1 金属–毒性肽与金属分型（优先精读）

| # | 文献 | 期刊年 | DOI | PMID |
|---|---|---|---|---|
| M1 | Huang et al. Aβ 金属还原产 H₂O₂ | *Biochemistry* 1999 | [10.1021/bi990438f](https://doi.org/10.1021/bi990438f) | [10386999](https://pubmed.ncbi.nlm.nih.gov/10386999/) |
| M2 | Huang et al. Cu 增强 Aβ 神经毒性 | *JBC* 1999 | [10.1074/jbc.274.52.37111](https://doi.org/10.1074/jbc.274.52.37111) | [10601271](https://pubmed.ncbi.nlm.nih.gov/10601271/) |
| M3 | Opazo et al. Aβ–Cu 类金属酶产 H₂O₂ | *JBC* 2002 | [10.1074/jbc.M206428200](https://doi.org/10.1074/jbc.M206428200) | [12192006](https://pubmed.ncbi.nlm.nih.gov/12192006/) |
| M4 | Bush et al. Zn 快速诱导 Aβ 淀粉样 | *Science* 1994 | [10.1126/science.8073293](https://doi.org/10.1126/science.8073293) | [8073293](https://pubmed.ncbi.nlm.nih.gov/8073293/) |
| M5 | Faller & Hureau Cu/Zn–Aβ 生物无机 | *Dalton Trans* 2009 | [10.1039/b813398k](https://doi.org/10.1039/b813398k) | [19322475](https://pubmed.ncbi.nlm.nih.gov/19322475/) |
| M6 | Hureau & Faller Cu–Aβ ROS 结构机制 | *Biochimie* 2009 | [10.1016/j.biochi.2009.03.013](https://doi.org/10.1016/j.biochi.2009.03.013) | [19332103](https://pubmed.ncbi.nlm.nih.gov/19332103/) |
| M7 | Sensi et al. 中枢 Zn | *Nat Rev Neurosci* 2009 | [10.1038/nrn2734](https://doi.org/10.1038/nrn2734) | [19826435](https://pubmed.ncbi.nlm.nih.gov/19826435/) |
| M8 | Cheignon et al. Aβ 与氧化应激 | *Redox Biol* 2018 | [10.1016/j.redox.2017.10.014](https://doi.org/10.1016/j.redox.2017.10.014) | [29080524](https://pubmed.ncbi.nlm.nih.gov/29080524/) |
| M9 | Butterfield & Lauderback 脂质/蛋白氧化 | *FRBM* 2002 | [10.1016/S0891-5849(02)00794-3](https://doi.org/10.1016/S0891-5849(02)00794-3) | [12031889](https://pubmed.ncbi.nlm.nih.gov/12031889/) |
| M10 | Greenough et al. 金属稳态与氧化应激 | *Neurochem Int* 2013 | [10.1016/j.neuint.2012.08.014](https://doi.org/10.1016/j.neuint.2012.08.014) | [22982299](https://pubmed.ncbi.nlm.nih.gov/22982299/) |

### 7.2 Aβ 功能毒性 / 其他靶点 / 反例

| # | 文献 | 期刊年 | DOI | PMID |
|---|---|---|---|---|
| O1 | Walsh et al. 寡聚体抑制 LTP | *Nature* 2002 | [10.1038/416535a](https://doi.org/10.1038/416535a) | [11932745](https://pubmed.ncbi.nlm.nih.gov/11932745/) |
| O2 | Guo & Lee tau 播种 | *JBC* 2011 | [10.1074/jbc.M110.209296](https://doi.org/10.1074/jbc.M110.209296) | [21372138](https://pubmed.ncbi.nlm.nih.gov/21372138/) |
| O3 | Strittmatter et al. ApoE4 | *PNAS* 1993 | [10.1073/pnas.90.5.1977](https://doi.org/10.1073/pnas.90.5.1977) | [8446617](https://pubmed.ncbi.nlm.nih.gov/8446617/) |
| O4 | Huang & Mahley ApoE 结构功能 | *Neurobiol Dis* 2014 | [10.1016/j.nbd.2014.08.025](https://doi.org/10.1016/j.nbd.2014.08.025) | [25173806](https://pubmed.ncbi.nlm.nih.gov/25173806/) |
| O5 | Ayton et al. CSF ferritin–APOE–AD | *Nat Commun* 2015 | [10.1038/ncomms7760](https://doi.org/10.1038/ncomms7760) | [25988319](https://pubmed.ncbi.nlm.nih.gov/25988319/) |
| O6 | Zecca et al. 脑铁与衰老 | *Nat Rev Neurosci* 2004 | [10.1038/nrn1537](https://doi.org/10.1038/nrn1537) | [15496864](https://pubmed.ncbi.nlm.nih.gov/15496864/) |
| O7 | Ward et al. 脑铁与神经退行 | *Lancet Neurol* 2014 | [10.1016/S1474-4422(14)70117-6](https://doi.org/10.1016/S1474-4422(14)70117-6) | [25231526](https://pubmed.ncbi.nlm.nih.gov/25231526/) |
| O8 | Wang et al. 神经肽–Aβ（**非毒性肽依据**） | *ACS Chem Neurosci* 2024 | [10.1021/acschemneuro.4c00075](https://doi.org/10.1021/acschemneuro.4c00075) | [39066700](https://pubmed.ncbi.nlm.nih.gov/39066700/) |

### 7.3 计算方法学（可选）

| # | 文献 | DOI | PMID |
|---|---|---|---|
| C1 | Abramson et al. AlphaFold 3 *Nature* 2024 | [10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w) | [38718835](https://pubmed.ncbi.nlm.nih.gov/38718835/) |
| C2 | Hollingsworth & Dror MD *Neuron* 2018 | [10.1016/j.neuron.2018.08.011](https://doi.org/10.1016/j.neuron.2018.08.011) | [30236283](https://pubmed.ncbi.nlm.nih.gov/30236283/) |
| C3 | Genheden & Ryde MM/GBSA 2015 | [10.1517/17460441.2015.1032936](https://doi.org/10.1517/17460441.2015.1032936) | [25835573](https://pubmed.ncbi.nlm.nih.gov/25835573/) |
| C4 | Senn & Thiel QM/MM 2009 | [10.1002/anie.200802019](https://doi.org/10.1002/anie.200802019) | [19173328](https://pubmed.ncbi.nlm.nih.gov/19173328/) |

---

## 8 精读优先级与引用句（可直接粘贴）

### 8.1 若只精读 6 篇（金属毒性肽最小集）

1. **Huang 1999 *Biochemistry*** — 化学产 H₂O₂  
2. **Huang 1999 *JBC*** — Cu 毒性与 H₂O₂ 相关  
3. **Opazo 2002 *JBC*** — 催化与底物、螯合/Zn 抑制  
4. **Cheignon 2018 *Redox Biol*** — 现代总图  
5. **Faller & Hureau 2009 *Dalton*** — 配位化学  
6. **Sensi 2009 *NRN*** — Zn 边界（防写错）

### 8.2 若补“其他方面”再加 5 篇

7. Walsh 2002 *Nature*（寡聚体 LTP）  
8. Guo & Lee 2011 *JBC*（tau 播种）  
9. Huang & Mahley 2014（ApoE）  
10. Ayton 2015 *Nat Commun*（ferritin–APOE）  
11. Ward 2014 *Lancet Neurol*（脑铁网络）

### 8.3 推荐引用句（中文）

- **毒性肽定义**：“人源 Aβ1–42 在 Cu/Fe 存在下通过金属还原产生 H₂O₂，并与神经毒性相关（Huang et al., 1999a,b）；在生理还原底物存在下呈现 Cu 依赖的类金属酶活性（Opazo et al., 2002）。”
- **Zn**：“Zn²⁺ 可快速诱导 Aβ 淀粉样形成（Bush et al., 1994），但作为 d¹⁰ 离子不参与 Fenton 型单电子循环；其中枢病理应在信号与稳态框架下讨论（Sensi et al., 2009）。”
- **铁蛋白**：“CSF ferritin 预测 AD 临床结局并受 APOE 调控（Ayton et al., 2015），支持将 ferritin 作为铁稳态功能节点而非未验证的直接结合靶点。”
- **反例**：“神经肽与 Aβ 的高频非共价互作（Wang et al., 2024）表明结合普遍存在，但功能可表现为抑制聚集与降低毒性，故不能由互作直接推断毒性肽。”

---

## 9 方法学与局限性

1. 检索：以金属–Aβ–ROS、Zn–Aβ、脑铁、ApoE、tau 播种、Aβ 寡聚体 LTP 为概念轴，PubMed 作者+题名关键词核验。  
2. AChE/PAS 文献（Inestrosa 等）本版按用户要求**不展开**。  
3. 摘要级转述；正式写作请核对全文图表与浓度条件。  
4. “毒性肽”金标准目前锚定在 **Aβ–Cu/Fe**；其他序列需独立重建同一证据链。  
5. Wang 2024 仅作互作/反例，不作毒性依据。

---

## 10 一页执行摘要

1. **金属相关毒性肽的文献核心**是 Aβ–**Cu/Fe**–H₂O₂–神经毒性三部曲：**Huang 1999 *Biochemistry*** + **Huang 1999 *JBC*** + **Opazo 2002 *JBC***。  
2. **Zn** 主叙事是聚集（**Bush 1994**）与 CNS 稳态（**Sensi 2009**），**不是** Fenton 型 ROS 金属；Opazo 中 Zn 还可抑制 Cu–Aβ 产 H₂O₂。  
3. **氧化应激总图**用 **Cheignon 2018**；脂质过氧化用 **Butterfield 2002**。  
4. **Aβ 功能毒性**另有 **Walsh 2002**（寡聚体–LTP），与金属路径互补。  
5. **tau** = 播种探索（Guo & Lee 2011）；**ApoE4** = 遗传多效+铁桥（Strittmatter；Huang & Mahley；Ayton）；**ferritin/Tf** = 铁稳态节点（Ayton；Zecca；Ward）。  
6. **Wang 2024 不能当毒性肽依据**。  
7. **AChE 本版不写**（已完成对接）。候选肽是否同类毒性肽，必须未来用 ±Cu/Fe、H₂O₂、螯合逆转等实验裁决；计算只提供配位/结构前提。
