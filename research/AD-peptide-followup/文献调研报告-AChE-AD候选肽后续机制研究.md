# AChE/AD 相关候选肽后续机制研究——理论计算文献证据与实施方案

**（基于 Auto-Empirical-Research-Skills 文献综述流程；检索与核验截至 2026-08-02；本版仅含理论计算，不含实验验证章节）**

> **核验声明**：本报告中全部文献均通过 PubMed E-utilities（esearch/esummary/efetch）逐条核验标题、期刊、年份、卷期页码、DOI 与 PMID。链接均为可访问的 PubMed / doi.org 地址。**未经核验的文献一律未列入。**
>
> **版本说明（相对上一版）**：① 按课题组现状，**全文仅保留理论计算内容**，删除原因果验证实验路线、细胞/iPSC 实验、Stage 1–4 实验 Go/No-Go 等全部实验章节；② 新增对 Wang 等（*ACS Chem Neurosci*, 2024）的文献适用性裁决——**该文不能作为“毒性肽”主证据**；③ 原方案 4.1–4.3（计算部分）全文保留，4.4（实验验证）仅作边界说明、不展开。

---

## 0 任务与范围

本研究服务于“12 条候选肽与 AChE 外周阴离子位点（PAS）致病靶点对接、并准备分子动力学（MD）”之后续**理论计算**机制研究。现有工作仅覆盖对接与 MD 准备。本报告范围严格限定为：

1. **原方案 4.1–4.3 保留**（AF3/多构象、靶点结构分析、金属离子与量化计算）；
2. **Aβ42、tau、ApoE4、ferritin/transferrin 在计算层面的合理定位与边界**；
3. **AlphaFold 3、多构象采样、MD、MM/GBSA、QM/MM/DFT 的正确使用方式**；
4. **12 条肽的计算筛选漏斗与计算侧 Go/No-Go**（不含合成/细胞/体内）；
5. **对 Wang 等 2024（*ACS Chem Neurosci*）能否作为“毒性肽”依据的明确裁决**；
6. **两项关键科学纠偏（计算表述层面）**：Zn²⁺ 不能与 Cu/Fe 等同视为 Fenton 型 ROS 金属；ferritin/transferrin 优先作为铁稳态功能节点而非未经验证的“直接致病结合靶点”。

> **明确不在本版范围内**：金属结合实验、ROS/脂质过氧化测定、酶活、聚集实验、细胞毒性、iPSC 与体内验证。原方案 4.4 的因果标准（“只有当候选肽在金属存在下引起 ROS/脂质过氧化增加并伴随神经损伤时，才支持金属相关促氧化神经毒性”）仍作为**未来实验裁决原则**写在边界处，但本版不展开任何实验设计。

---

## 1 保留原文：后续机制研究方案（4.1–4.3 计算部分；4.4 仅边界）

> 以下为课题组原有方案。4.1–4.3 全文保留并作为本版实施主体；4.4 因本课题现阶段“只有理论计算”而不展开，仅保留原文作为未来边界。

### 4.1 AlphaFold3/多构象肽结构预测

在后续研究中，将对最终候选短肽和长肽进行结构预测。对于短肽，尤其是 7–15 aa 序列，将生成多个可能构象而不依赖单一静态结构。AlphaFold3 可用于候选肽及其与蛋白质、金属离子或其他生物分子复合物的结构建模。由于短肽具有较高构象柔性，预测结果将通过多构象采样、结构置信度和后续分子动力学进行评估。AlphaFold3 的复合物预测框架可作为后续候选结构建模的参考，但不能替代实验结构测定。

### 4.2 后续AChE及AD相关靶点分析

后续将对候选肽与 AChE、BChE、Aβ42、tau、ApoE4、ferritin 和 transferrin 的相互作用进行结构分析。AChE 重点考察 CAS、PAS 及 AChE–Aβ 相互作用区域。Aβ 和 tau 相关分析用于评估候选肽对 AD 病理蛋白聚集或构象稳定性的潜在影响。ferritin 和 transferrin 相关分析用于探讨候选肽与铁稳态相关蛋白之间的潜在相互作用。

### 4.3 后续金属离子和量化计算

后续将重点考察 Cu²⁺、Fe²⁺/Fe³⁺ 和 Zn²⁺。分子对接和结构建模用于筛选潜在配位构象；分子动力学用于分析金属–配位残基距离、配位数和配位稳定性；MM/GBSA 或 MM/PBSA 用于进行相对结合自由能比较。对于稳定的金属配位体系，将进一步采用 QM/MM 或 DFT 分析配位几何、配位能、电荷分布及潜在电子转移特征。

### 4.4 后续实验验证（本版不展开，仅保留原文作边界）

> 后续实验将包括金属结合、Cu/Fe 依赖性 ROS、脂质过氧化、AChE/BChE 酶活、Aβ 聚集和神经细胞毒性评价。计算筛选结果仅用于候选优先级排序；只有当候选肽在金属存在条件下引起 ROS 或脂质过氧化增加，并伴随神经细胞损伤时，才能进一步支持其金属相关促氧化神经毒性作用。
>
> **本版裁决**：当前交付物与工作流止于计算优先级排序；任何“毒性肽 / 促氧化神经毒性”的因果结论**不得**仅由对接、MD、MM/GBSA 或 QM/MM 得出。

---

## 2 文献裁决：Wang 等 2024（*ACS Chem Neurosci*）能否作为“毒性肽”依据？

### 2.1 文献身份（已核验）

| 字段 | 内容 |
|---|---|
| 作者 | Wang D, Wang G, Wang X, Ren Z, Jia C |
| 标题 | Native Mass Spectrometry-Centric Approaches Revealed That Neuropeptides Frequently Interact with Amyloid-β |
| 期刊 | *ACS Chemical Neuroscience* 2024; 15(15):2719-2728 |
| DOI | [10.1021/acschemneuro.4c00075](https://doi.org/10.1021/acschemneuro.4c00075) |
| PMID | [39066700](https://pubmed.ncbi.nlm.nih.gov/39066700/) |
| 通讯 | Jia C / Ren Z（国家蛋白质科学中心·北京 / 安徽医科大学） |

### 2.2 该文实际证明了什么

按 PubMed 摘要与公开报道可核验的结论：

1. **互作普遍性（主结论）**：12 条神经肽中 6 条（leptin、kisspeptin、cerebellin、bradykinin、SHLP2、substance P）在非变性质谱气相中与 Aβ 形成非共价异二聚体——支持“神经肽–Aβ 互作并不罕见”。
2. **聚集方向双向**：ThT/凝胶显示 kisspeptin **加速** Aβ 聚集；leptin、cerebellin **抑制** Aβ 聚集。
3. **细胞毒性方向以保护为主**：leptin、cerebellin 减弱 Aβ 诱导的细胞毒性；leptin 可通过**螯合 Cu(II)** 从 Cu–Aβ 中夺铜，从而减弱 Cu 相关毒性。
4. **计算仅为辅助**：作者用 HDOCK 对接推测 leptin/kisspeptin/cerebellin 与 Aβ 的界面残基（如 leptin 的 Cys2/His3/Tyr6 等），属于**假设生成**，并非毒性机制的独立证明。

### 2.3 明确裁决：**不能作为“毒性肽”主依据**

| 问题 | 裁决 | 理由 |
|---|---|---|
| 能否证明“神经肽/候选肽本身是毒性肽”？ | **否** | 文中阳性功能读出主要是 **抑制聚集 + 降低细胞毒性**（leptin、cerebellin）；主体叙事是保护/抑制剂，不是毒性肽 |
| 能否证明“肽–Aβ 互作普遍存在”？ | **是（有限）** | 6/12 在 native MS 下形成复合物，可作为“短肽与 Aβ 结合并非个例”的旁证 |
| 能否证明“肽可双向调节 Aβ 聚集”？ | **是（旁证）** | kisspeptin 促聚集、leptin/cerebellin 抑聚集；说明互作≠毒性，方向必须单独判定 |
| 能否证明“Cu 螯合可减轻 Cu–Aβ 毒性”？ | **是（机制旁证）** | leptin 的 Cu 螯合叙事与本课题 Cu 矩阵相关，但指向**保护**，与“毒性肽”相反 |
| 对接（HDOCK）能否独立支持毒性？ | **否** | 对接只给界面假说；该文自身也用实验（ThT、凝胶、MTT、Cu 滴定）裁决功能方向 |
| 对本课题 12 条候选肽的直接外推？ | **否** | 序列、长度、来源均不同；不得把 leptin 等神经肽结论迁移为候选肽的毒性标签 |

**一句话结论**：Wang 2024 是“**神经肽–Aβ 互作 + 聚集调节（双向）+ 部分保护/Cu 螯合**”的证据，**不是**“毒性肽”证据。若课题组需要支撑“候选肽具金属相关促氧化神经毒性”，必须回到 Cu/Fe–Aβ 氧化还原与 H₂O₂ 文献（Huang 1999 *Biochemistry*；Opazo 2002 *JBC*；Cheignon 2018 *Redox Biol* 等），且最终仍需实验因果链——**这些均超出本版“仅理论计算”范围，此处只标明文献指向，不展开实验。**

### 2.4 该文对本课题**计算工作**的可用之处（有限采纳）

在剔除“毒性肽”误用后，该文对计算侧仍有三点可借鉴：

1. **假设生成模板**：肽–Aβ 对接应报告界面残基、接触距离阈值（文中 <4 Å）、多模型排序，而不是单一最优构象当结论；
2. **功能方向不可由对接推断**：同一套“能结合”的肽，既可促聚集也可抑聚集——计算打分高≠毒性，也不=保护；
3. **金属维度要单独建模**：若讨论 Cu，应构建肽–Cu、Aβ–Cu、肽–Cu–Aβ 竞争/夺铜模型，而不是只做无金属对接；leptin 的“夺铜”叙事提醒：计算上要比较 **肽对 Cu 的配位能力 vs Aβ 对 Cu 的配位能力**（QM/MM 或金属专用 MD），否则无法讨论螯合假说。

> **引用规范建议**：若在计算报告/论文中引用 Wang 2024，建议表述为“支持神经肽与 Aβ 非共价互作的高频性，并提示聚集调节方向需实验判定”；**禁止**表述为“证明了毒性肽机制”或“可作为候选肽神经毒性的文献依据”。

---

## 3 计算靶点定位：AChE/BChE、Aβ42、tau、ApoE4、ferritin/transferrin

### 3.1 各靶点在**理论计算**中的定位

| 靶点 | 计算定位 | 可做的计算 | 不可做的断言 | 核心文献 |
|---|---|---|---|---|
| **AChE** | 主靶点（已有 PAS 对接） | CAS/PAS/ gorge 结合模式；Trp286、Tyr72、Tyr124、Asp74 等接触；与 Aβ 共结合区的空间关系 | 不得由对接直接断言“致病”或“毒性” | [C4][C11][S10] |
| **BChE** | 主靶点（选择性对照） | 与 AChE 的选择性比较（相对 MM/GBSA） | 不得外推临床胆碱酯酶疗效 | [C11] |
| **Aβ42** | 主病理相关蛋白（计算） | 肽–Aβ 单体/寡聚界面；金属–Aβ–肽三元模型；聚集相关构象（有限） | 不得由对接断言促/抑聚集或神经毒性（Wang 2024 已证明方向可相反） | [C2][C7][N1] |
| **tau** | 探索性 | 肽–tau 片段对接/MD；仅作假设生成 | 无结合稳定性证据前不做播种/病理断言 | [C6] |
| **ApoE4** | 探索性（异构体对照） | ApoE3 vs E4 的差异界面；脂化状态需声明模型简化 | 不得由单次对接解释遗传风险 | [C12][S5] |
| **ferritin** | **铁稳态功能节点**（非直接致病结合靶点） | 表面口袋/铁释放相关区域的探索性对接；假设生成 | 禁止写成与 AChE/Aβ 并列的“致病结合靶点” | [C3][C8][C9] |
| **transferrin** | **铁稳态功能节点** | Tf/TfR1 相关界面的探索性建模 | 同上 | [C8][C9] |

### 3.2 对原方案 4.2 的计算侧修订建议

1. **主计算靶点**：AChE/BChE（PAS/CAS + 选择性）、Aβ42（±Cu/Fe 金属矩阵）。
2. **功能节点（降级）**：ferritin/transferrin——对接命中只进入“假设列表”，不进入主结论句；报告中明确标注“功能节点 / 假设生成”。
3. **探索性靶点**：tau、ApoE4——仅在主靶点计算完成且资源允许时进行；输出单独附录，不与主结论混写。
4. **AChE–Aβ 轴线**：Inestrosa 1996 证明 AChE 经 PAS 加速 Aβ 纤维组装 [C4]；Alvarez 1997 显示对 Aβ 片段的序列特异性 [S10]。计算上优先做：
   - 候选肽–AChE PAS；
   - Aβ 片段–AChE PAS；
   - 肽是否与 Aβ 竞争同一 PAS 表位（重叠接触残基分析）；
   - 而非无差别的“七靶点并行对接”。

### 3.3 Wang 2024 与 Aβ 计算的衔接

- 若对候选肽做 Aβ 对接，采用与 Wang 2024 类似的**多模型 + 界面残基表**输出格式，便于与文献对照。
- 同时在方法学中写明：Wang 2024 中结合肽功能方向相反，故本课题 **Aβ 对接结果只用于构象假设与优先级排序，不标注“毒性/保护”标签**。

---

## 4 AlphaFold 3、多构象、MD、MM/GBSA、QM/MM/DFT 的正确使用

### 4.1 AlphaFold 3（AF3）

- **能力**：AF3 采用扩散式架构，可联合预测蛋白质–核酸–小分子–离子–修饰残基复合物；蛋白–配体与抗体-抗原精度显著提升（Abramson 等，*Nature*, 2024）[C1]。
- **正确用法**：
  1. 输入：肽序列 + 靶蛋白序列；金属以离子/配位形式加入时，**必须人工检查配位几何**（AF3 对过渡金属不可靠）；
  2. 解读：ipTM/pTM、界面 pLDDT、PAE；低置信区不得写入结论；
  3. **多构象采样**：多 seed 生成 ensemble，按 RMSD/PAE 聚类——短肽（7–15 aa）禁止只报单结构；
  4. 边界：AF3 = 结构假设生成器，**不提供亲和力、动力学、氧化还原或毒性**。
- 工作流：AF3 多构象 → 聚类代表性复合物 → MD 起点；AF3 分仅用于排序。

### 4.2 分子动力学（MD）

- 依据：Hollingsworth & Dror（*Neuron*, 2018）[S9]。
- **正确做法**：
  1. 显式溶剂 + 生理离子强度；最小化 → NVT/NPT 平衡 → 生产运行；
  2. **≥3 次独立重复**；RMSD/RMSF、接触驻留、氢键/盐桥占有率；
  3. 力场：ff14SB/ff19SB；**Cu²⁺/Fe²⁺/Fe³⁺/Zn²⁺ 必须使用金属专用参数**（如 12-6-4 或 QM 拟合），默认参数对配位常失效；
  4. 金属分析：配位残基距离时间序列、配位数、逸出事件、与 Aβ/AChE 的竞争占位（若做三元体系）。
- **边界**：经典 MD **不能**描述键断裂/形成、Fenton 化学、电子转移——不得把“Cu 在位点停留”写成“产生 ROS/毒性”。

### 4.3 MM/GBSA 与 MM/PBSA

- 依据：Genheden & Ryde（*Expert Opin Drug Discov*, 2015）[C14]。
- **正确用法**：
  1. 基于平衡 MD 轨迹系综平均，禁止单帧；
  2. **仅相对排序**（12 肽内部、或 AChE vs BChE 选择性），不报绝对 ΔG；
  3. **含金属配位键体系慎用**——优先 QM 校正或与后续 ITC 预留接口；
  4. 输出必须带标准差与重复间一致性，避免过度解释 1–2 kcal/mol 差异。

### 4.4 QM/MM 与 DFT

- 依据：Senn & Thiel（*Angew Chem Int Ed*, 2009）[C13]。
- **正确用法**：
  1. QM 区 = 金属 + 第一配位层 + 关键第二层；
  2. 泛函/基组针对过渡金属与色散校准；明确自旋态（Cu²⁺ d⁹；Fe 高/低自旋；**Zn²⁺ d¹⁰ 闭壳层、无氧化还原循环**）；
  3. 输出：配位几何、配位能、电荷/自旋布居、**相对**电子转移倾向；
  4. 若讨论“夺铜/螯合”（呼应 Wang 2024 中 leptin 叙事），应计算 **肽–Cu 与 Aβ–Cu 的配位能差**，而不是只优化一个复合物。
- **边界**：DFT/QM/MM 给出的是电子结构与能学趋势；**“能否产生神经毒性 H₂O₂”属于实验问题**（Huang 1999；Opazo 2002），本版计算不得直接下毒性结论。

### 4.5 推荐计算流水线（仅理论）

```
12 条候选肽
  │
  ├─① AF3 / 多构象采样（肽 alone + 肽–AChE PAS + 可选肽–Aβ）
  │     └─ 置信度过滤、聚类
  ├─② 分子对接精修（PAS 聚焦；金属位点单独取样）
  ├─③ MD ≥3×（稳定性、接触、金属配位驻留）
  ├─④ MM/GBSA 相对排序（同受体同系列）
  ├─⑤ 头部候选：QM/MM 或 DFT（Cu/Fe/Zn 配位几何与能学；Zn 作非氧化还原对照）
  └─⑥ 输出：优先级列表 + 结构假设 + 明确“待实验裁决”标签
```

### 4.6 计算–结论证据等级

| 计算方法 | 可回答 | 不可回答 | 正确角色 |
|---|---|---|---|
| AlphaFold 3 | 复合物结构假设、界面残基 | 亲和力、毒性、金属配位准确性 | 构象生成与排序起点 |
| 对接（含 HDOCK 类） | 可能界面 | 功能方向（促/抑/毒） | 假设生成（Wang 2024 用法） |
| MD | 结合稳定性、柔性、配位驻留 | 反应、ROS、细胞毒性 | 动态验证与筛选 |
| MM/GBSA | 同系列相对排序 | 绝对亲和力、毒性标签 | 排序（预留实验校准） |
| QM/MM/DFT | 配位几何、氧化态趋势、相对配位能 | 体内毒性、聚集动力学终点 | 电子结构终局分析 |
| 实验 | 真值（本版不做） | —— | 未来裁决一切功能标签 |

---

## 5 12 条肽：仅计算侧的分阶段 Go/No-Go

> 本漏斗**止于计算优先级列表**。不设合成、细胞、iPSC 阶段。

### 5.1 总体漏斗（建议 12 → 8 → 4 → 2–3 条“计算先导”）

**Stage C0 — 已完成：AChE-PAS 对接 + MD 准备**
- 输入：12 条候选肽。
- 检查：PAS 关键残基接触是否成立；对接构象是否可用于 MD。
- **Go**：具备可解释的 PAS 结合模式 → 进入 C1。
- **No-Go**：无 PAS 接触或构象明显伪结合 → 标记淘汰，不进入金属/QM 阶段。

**Stage C1 — 多构象 + 靶点扩展计算（2–4 周）**
- 内容：AF3 多构象；AChE/BChE 对比；Aβ42（±）对接；ferritin/transferrin 仅探索性附录。
- **Go**：主靶点（AChE 和/或 Aβ）上出现可重复界面 + 合理置信度 → 12→8。
- **No-Go**：全部主靶点无稳定界面假说。
- **禁止**：根据 Aβ 对接结果标注“毒性肽”（见第 2 节 Wang 2024 裁决）。

**Stage C2 — MD 稳定性与金属配位（3–6 周）**
- 内容：≥3 次 MD；Cu²⁺/Fe²⁺/Fe³⁺/Zn²⁺ 分矩阵；配位驻留与逸出；可选肽–Cu vs Aβ–Cu 竞争模型。
- **Go**：至少一种病理相关条件下（AChE PAS 或 Aβ 界面或 Cu/Fe 配位）MD 稳定、重复一致 → 8→4。
- **No-Go**：MD 中肽迅速解离、金属配位不可维持、重复间完全不一致。
- **Zn 规则**：Zn 组只解释配位/结构对照，**不写“Zn–Fenton/ROS”**（见第 6 节）。

**Stage C3 — MM/GBSA 排序 + 头部 QM/MM（2–4 周）**
- 内容：相对结合能排序；对 Top 候选做 QM/MM/DFT（配位几何、电荷、相对配位能；若做夺铜假说则比肽–Cu 与 Aβ–Cu）。
- **Go**：排序稳定、电子结构无化学不合理处（错误自旋态、配位数荒谬等）→ 输出 2–3 条计算先导。
- **No-Go**：能量排序随方法剧烈翻转且无结构解释；QM 区化学不合理。
- **输出物**：计算先导列表、结构坐标/轨迹摘要、界面残基表、金属配位统计、**“功能标签：未判定（待实验）”**。

### 5.2 计算侧 Go/No-Go 汇总

| 阶段 | 时间 | 关键指标 | Go | No-Go |
|---|---|---|---|---|
| C0 对接/MD 准备 | 已完成 | PAS 结合模式 | 可解释 PAS 接触 | 无特异结合 |
| C1 多构象+扩展靶点 | 2–4 周 | AF3/对接界面与置信度 | 主靶点可重复界面 | 主靶点全阴性 |
| C2 MD+金属矩阵 | 3–6 周 | 稳定性、配位驻留、重复性 | 稳定且可重复 | 解离/不收敛/不重复 |
| C3 MM/GBSA+QM/MM | 2–4 周 | 相对排序、配位电子结构 | 排序稳定、化学合理 | 方法间无解释翻转 |

### 5.3 计算结论的允许表述 / 禁止表述

| 允许 | 禁止 |
|---|---|
| “肽 X 在 MD 中稳定结合 AChE PAS，主要接触 Trp286/…” | “肽 X 是毒性肽” |
| “肽 X 对 Cu²⁺ 呈现 N 配位，QM 配位能高于对照肽” | “肽 X 通过 Fenton 反应产生神经毒性” |
| “肽 X 与 Aβ 的对接界面与 Wang 2024 中某神经肽类似，功能方向待实验” | “根据 Wang 2024，肽 X 具有神经毒性/保护作用” |
| “相对 MM/GBSA 排序为 X>Y>Z（仅同系列）” | “Kd = … nM（无实验）” |
| “Zn²⁺ 可形成稳定配位，但无氧化还原活性，不作 ROS 金属解释” | “Zn²⁺ 介导 ROS/Fenton 毒性” |

---

## 6 特别提示（计算表述中的关键科学纠偏）

### 6.1 Zn²⁺ 不是 Fenton 型 ROS 金属

- **化学依据**：Zn²⁺ 为 d¹⁰ 闭壳层，氧化还原惰性，不能像 Cu⁺/Cu²⁺、Fe²⁺/Fe³⁺ 那样单电子循环驱动 Fenton/Haber–Weiss。
- **文献**：Sensi 等（*Nat Rev Neurosci*, 2009）将 Zn 定位为 CNS 信号与稳态离子，病理涉及兴奋毒性、线粒体、Zn–Aβ 聚集等，**而非 Zn–Fenton** [C10]。
- **计算含义**：
  1. 方案 4.3 中 Zn 与 Cu/Fe 并列做配位计算是合理的；
  2. QM/MM 描述 Zn 时采用闭壳层、不讨论向 O₂/H₂O₂ 的电子转移；
  3. 若 Zn 配位稳定而 Cu/Fe 亦稳定，报告中应分列“结构金属（Zn）”与“氧化还原活性金属（Cu/Fe）”；
  4. 任何“ROS/毒性”字样不得出现在纯计算结果的结论句中。

### 6.2 ferritin/transferrin：铁稳态功能节点

- **文献**：脑铁网络中 Tf–TfR1 摄取、ferritin 储存、ferroportin 释放是共识 [C8][C9]；CSF ferritin 预测 AD 结局并受 APOE 调控 [C3]。
- **计算含义**：
  1. 对接/AF3 命中 = 假设生成；
  2. 不与 AChE、Aβ 并列写入“致病靶点”主结论；
  3. 若资源有限，可降为附录或暂缓，优先保证 AChE PAS + Aβ ± 金属。

### 6.3 “毒性”标签的计算边界（再次强调）

金属–肽配位稳定、甚至 DFT 显示有利于 Cu²⁺→Cu⁺ 还原趋势，**仍只是化学可能性**。Opazo 2002、Huang 1999 等建立的是 **Aβ–金属–H₂O₂–毒性** 实验范式 [C5][C7]，不能在无实验的情况下平移为“本课题候选肽 = 毒性肽”。Wang 2024 更从反面说明：能与 Aβ/Cu 相互作用的肽完全可能是**保护性螯合剂** [N1]。

---

## 7 参考文献

### 7.1 核心文献（14 篇）

| # | 文献（期刊 年；卷:页） | DOI | PMID |
|---|---|---|---|
| C1 | Abramson J, et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. *Nature* 2024; 630:493-500. | [10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w) | [38718835](https://pubmed.ncbi.nlm.nih.gov/38718835/) |
| C2 | Walsh DM, et al. Naturally secreted oligomers of amyloid beta protein potently inhibit hippocampal long-term potentiation in vivo. *Nature* 2002; 416:535-539. | [10.1038/416535a](https://doi.org/10.1038/416535a) | [11932745](https://pubmed.ncbi.nlm.nih.gov/11932745/) |
| C3 | Ayton S, Faux NG, Bush AI; ADNI. Ferritin levels in the cerebrospinal fluid predict Alzheimer's disease outcomes and are regulated by APOE. *Nat Commun* 2015; 6:6760. | [10.1038/ncomms7760](https://doi.org/10.1038/ncomms7760) | [25988319](https://pubmed.ncbi.nlm.nih.gov/25988319/) |
| C4 | Inestrosa NC, et al. Acetylcholinesterase accelerates assembly of amyloid-beta-peptides into Alzheimer's fibrils: possible role of the peripheral site of the enzyme. *Neuron* 1996; 16:881-891. | [10.1016/S0896-6273(00)80108-7](https://doi.org/10.1016/S0896-6273(00)80108-7) | [8608006](https://pubmed.ncbi.nlm.nih.gov/8608006/) |
| C5 | Opazo C, et al. Metalloenzyme-like activity of Alzheimer's disease beta-amyloid. Cu-dependent catalytic conversion of dopamine, cholesterol, and biological reducing agents to neurotoxic H₂O₂. *J Biol Chem* 2002; 277:40302-40308. | [10.1074/jbc.M206428200](https://doi.org/10.1074/jbc.M206428200) | [12192006](https://pubmed.ncbi.nlm.nih.gov/12192006/) |
| C6 | Guo JL, Lee VM. Seeding of normal Tau by pathological Tau conformers drives pathogenesis of Alzheimer-like tangles. *J Biol Chem* 2011; 286:15317-15331. | [10.1074/jbc.M110.209296](https://doi.org/10.1074/jbc.M110.209296) | [21372138](https://pubmed.ncbi.nlm.nih.gov/21372138/) |
| C7 | Huang X, et al. The A beta peptide of Alzheimer's disease directly produces hydrogen peroxide through metal ion reduction. *Biochemistry* 1999; 38:7609-7616. | [10.1021/bi990438f](https://doi.org/10.1021/bi990438f) | [10386999](https://pubmed.ncbi.nlm.nih.gov/10386999/) |
| C8 | Zecca L, et al. Iron, brain ageing and neurodegenerative disorders. *Nat Rev Neurosci* 2004; 5:863-873. | [10.1038/nrn1537](https://doi.org/10.1038/nrn1537) | [15496864](https://pubmed.ncbi.nlm.nih.gov/15496864/) |
| C9 | Ward RJ, et al. The role of iron in brain ageing and neurodegenerative disorders. *Lancet Neurol* 2014; 13:1045-1060. | [10.1016/S1474-4422(14)70117-6](https://doi.org/10.1016/S1474-4422(14)70117-6) | [25231526](https://pubmed.ncbi.nlm.nih.gov/25231526/) |
| C10 | Sensi SL, et al. Zinc in the physiology and pathology of the CNS. *Nat Rev Neurosci* 2009; 10:780-791. | [10.1038/nrn2734](https://doi.org/10.1038/nrn2734) | [19826435](https://pubmed.ncbi.nlm.nih.gov/19826435/) |
| C11 | Darvesh S, Hopkins DA, Geula C. Neurobiology of butyrylcholinesterase. *Nat Rev Neurosci* 2003; 4:131-138. | [10.1038/nrn1035](https://doi.org/10.1038/nrn1035) | [12563284](https://pubmed.ncbi.nlm.nih.gov/12563284/) |
| C12 | Huang Y, Mahley RW. Apolipoprotein E: structure and function in lipid metabolism, neurobiology, and Alzheimer's diseases. *Neurobiol Dis* 2014; 72 Pt A:3-12. | [10.1016/j.nbd.2014.08.025](https://doi.org/10.1016/j.nbd.2014.08.025) | [25173806](https://pubmed.ncbi.nlm.nih.gov/25173806/) |
| C13 | Senn HM, Thiel W. QM/MM methods for biomolecular systems. *Angew Chem Int Ed Engl* 2009; 48:1198-1229. | [10.1002/anie.200802019](https://doi.org/10.1002/anie.200802019) | [19173328](https://pubmed.ncbi.nlm.nih.gov/19173328/) |
| C14 | Genheden S, Ryde U. The MM/PBSA and MM/GBSA methods to estimate ligand-binding affinities. *Expert Opin Drug Discov* 2015; 10:449-461. | [10.1517/17460441.2015.1032936](https://doi.org/10.1517/17460441.2015.1032936) | [25835573](https://pubmed.ncbi.nlm.nih.gov/25835573/) |

### 7.2 本版点名评议文献（用户提供）

| # | 文献 | DOI | PMID | 本报告角色 |
|---|---|---|---|---|
| **N1** | Wang D, et al. Native Mass Spectrometry-Centric Approaches Revealed That Neuropeptides Frequently Interact with Amyloid-β. *ACS Chem Neurosci* 2024; 15:2719-2728. | [10.1021/acschemneuro.4c00075](https://doi.org/10.1021/acschemneuro.4c00075) | [39066700](https://pubmed.ncbi.nlm.nih.gov/39066700/) | **互作普遍性旁证；明确不作为毒性肽依据** |

### 7.3 补充文献（计算与机制边界）

| # | 文献 | DOI | PMID |
|---|---|---|---|
| S3 | Huang X, et al. Cu(II) potentiation of Alzheimer abeta neurotoxicity. Correlation with cell-free hydrogen peroxide production and metal reduction. *J Biol Chem* 1999; 274:37111-37116. | [10.1074/jbc.274.52.37111](https://doi.org/10.1074/jbc.274.52.37111) | [10601271](https://pubmed.ncbi.nlm.nih.gov/10601271/) |
| S5 | Strittmatter WJ, et al. Apolipoprotein E: high-avidity binding to beta-amyloid and increased frequency of type 4 allele in late-onset familial Alzheimer disease. *PNAS* 1993; 90:1977-1981. | [10.1073/pnas.90.5.1977](https://doi.org/10.1073/pnas.90.5.1977) | [8446617](https://pubmed.ncbi.nlm.nih.gov/8446617/) |
| S6 | Hureau C, Faller P. Abeta-mediated ROS production by Cu ions: structural insights, mechanisms and relevance to Alzheimer's disease. *Biochimie* 2009; 91:1212-1217. | [10.1016/j.biochi.2009.03.013](https://doi.org/10.1016/j.biochi.2009.03.013) | [19332103](https://pubmed.ncbi.nlm.nih.gov/19332103/) |
| S8 | Cheignon C, et al. Oxidative stress and the amyloid beta peptide in Alzheimer's disease. *Redox Biol* 2018; 14:450-464. | [10.1016/j.redox.2017.10.014](https://doi.org/10.1016/j.redox.2017.10.014) | [29080524](https://pubmed.ncbi.nlm.nih.gov/29080524/) |
| S9 | Hollingsworth SA, Dror RO. Molecular dynamics simulation for all. *Neuron* 2018; 99:1129-1143. | [10.1016/j.neuron.2018.08.011](https://doi.org/10.1016/j.neuron.2018.08.011) | [30236283](https://pubmed.ncbi.nlm.nih.gov/30236283/) |
| S10 | Alvarez A, et al. Acetylcholinesterase promotes the aggregation of amyloid-beta-peptide fragments by forming a complex with the growing fibrils. *J Mol Biol* 1997; 272:348-361. | [10.1006/jmbi.1997.1245](https://doi.org/10.1006/jmbi.1997.1245) | [9325095](https://pubmed.ncbi.nlm.nih.gov/9325095/) |

> 说明：S3/S6/S8 仅作“若未来讨论金属–ROS 毒性，应引用的实验范式文献”索引；**本版不依据它们给候选肽贴毒性标签**。上一版中的 iPSC 实验文献（Israel 2012、Kondo 2013 等）因本版删除实验章节而不再列入。

---

## 8 方法学与局限性

1. **检索与核验**：PubMed E-utilities 逐条核验；Wang 2024 经 esearch/esummary/efetch 确认 PMID 39066700、DOI 10.1021/acschemneuro.4c00075、卷期页 15(15):2719-2728。
2. **范围裁剪**：按用户要求“实验部分都去掉，这个只有理论计算”，删除因果验证实验路线、细胞/iPSC/体内 Go-No-Go；保留 4.1–4.3 与计算方法学、靶点计算定位、计算漏斗。
3. **Wang 2024 裁决逻辑**：以其摘要可核验的功能方向（抑制聚集、降低细胞毒性、Cu 螯合保护）为据，判定其不支持“毒性肽”主张；保留其对“互作普遍性”和“对接仅假设生成”的方法学启示。
4. **局限性**：
   - 未获取 Wang 2024 全文逐页核对补充图表；裁决以 PubMed 摘要与公开综述信息为准，若用于正式论文请核对全文；
   - 纯计算不能完成毒性/保护的功能定性；
   - Go/No-Go 阈值为程序性建议，可用课题组既有对接/MD 数据校准；
   - AF3/MD/MM-GBSA/QM 对短肽与过渡金属均有固有误差，结论必须保留不确定性表述。

---

## 9 执行摘要（可直接写入汇报 PPT）

1. **Wang 等 2024（*ACS Chem Neurosci*）不能作为毒性肽依据**；它支持神经肽–Aβ 互作常见，且 leptin/cerebellin 偏保护、kisspeptin 偏促聚集，功能方向必须另判。
2. **本课题现阶段只有理论计算**：交付止于 AF3→对接→MD→MM/GBSA→QM/MM 的优先级列表与结构假设。
3. **主计算靶点** = AChE/BChE + Aβ42（±Cu/Fe）；ferritin/transferrin = 功能节点/附录；tau、ApoE4 = 探索性。
4. **Zn²⁺** 只作结构/配位对照，不作 Fenton 型 ROS 金属。
5. **禁止**在纯计算结果上使用“毒性肽”“神经毒性机制已证实”等表述；原方案 4.4 的实验因果标准留待未来，不在本版执行。
