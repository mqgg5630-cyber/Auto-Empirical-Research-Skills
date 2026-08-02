# AChE/AD 相关候选肽后续机制研究——文献证据基础与实施方案

**（基于 Auto-Empirical-Research-Skills 文献综述流程；检索与核验截至 2026-08-02）**

> **核验声明**：本报告中全部 24 篇文献（14 篇核心 + 10 篇补充）均通过 PubMed E-utilities（esearch/esummary/efetch）逐条核验标题、期刊、年份、卷期页码、DOI 与 PMID，链接均为可访问的 PubMed / doi.org 地址。凡既往资料中记忆有误之处（如 Opazo 2002 的 DOI 应为 `10.1074/jbc.M206428200`、Ayton 2015 标题中 outcomes 为复数、Inestrosa 1996 的 PMID 为 8608006 等）均已按 PubMed 记录纠正。**未经核验的文献一律未列入。**

---

## 0 任务与范围

本研究服务于"12 条候选肽与 AChE 外周阴离子位点（PAS）致病靶点对接、并准备分子动力学（MD）"之后续机制研究。现有工作仅覆盖对接与 MD 准备（方案 4 的起点），本报告就以下问题给出文献证据基础与可执行方案：

1. **Cu/Fe 配位、ROS、脂质过氧化与神经毒性的因果验证路线**（重点）；
2. **Aβ42、tau、ApoE4、ferritin/transferrin 的合理定位与实验边界**；
3. **AlphaFold 3、多构象采样、MD、MM/GBSA、QM/MM/DFT 的正确使用方式**；
4. **12 条肽从初筛到 iPSC 神经元验证的分阶段 Go/No-Go 方案**；
5. **14 篇核心 SCI 文献**（含 *Nature*、*Nature Communications*、*Neuron*、*JBC*、*Biochemistry* 等），附 DOI/PMID 与链接；
6. **两项关键科学纠偏**：Zn²⁺ 不能与 Cu/Fe 等同视为 Fenton 型 ROS 金属；ferritin/transferrin 应定位为铁稳态功能节点而非未经验证的"直接致病结合靶点"。

---

## 1 保留原文：后续机制研究方案（4.1–4.4）

> 以下为课题组原有方案，予以保留；本报告在此基础上补充文献证据与实施方案（第 2–7 节）。

### 4.1 AlphaFold3/多构象肽结构预测

在后续研究中，将对最终候选短肽和长肽进行结构预测。对于短肽，尤其是 7–15 aa 序列，将生成多个可能构象而不依赖单一静态结构。AlphaFold3 可用于候选肽及其与蛋白质、金属离子或其他生物分子复合物的结构建模。由于短肽具有较高构象柔性，预测结果将通过多构象采样、结构置信度和后续分子动力学进行评估。AlphaFold3 的复合物预测框架可作为后续候选结构建模的参考，但不能替代实验结构测定。

### 4.2 后续AChE及AD相关靶点分析

后续将对候选肽与 AChE、BChE、Aβ42、tau、ApoE4、ferritin 和 transferrin 的相互作用进行结构分析。AChE 重点考察 CAS、PAS 及 AChE–Aβ 相互作用区域。Aβ 和 tau 相关分析用于评估候选肽对 AD 病理蛋白聚集或构象稳定性的潜在影响。ferritin 和 transferrin 相关分析用于探讨候选肽与铁稳态相关蛋白之间的潜在相互作用。

### 4.3 后续金属离子和量化计算

后续将重点考察 Cu²⁺、Fe²⁺/Fe³⁺ 和 Zn²⁺。分子对接和结构建模用于筛选潜在配位构象；分子动力学用于分析金属–配位残基距离、配位数和配位稳定性；MM/GBSA 或 MM/PBSA 用于进行相对结合自由能比较。对于稳定的金属配位体系，将进一步采用 QM/MM 或 DFT 分析配位几何、配位能、电荷分布及潜在电子转移特征。

### 4.4 后续实验验证

后续实验将包括金属结合、Cu/Fe 依赖性 ROS、脂质过氧化、AChE/BChE 酶活、Aβ 聚集和神经细胞毒性评价。计算筛选结果仅用于候选优先级排序；只有当候选肽在金属存在条件下引起 ROS 或脂质过氧化增加，并伴随神经细胞损伤时，才能进一步支持其金属相关促氧化神经毒性作用。

---

## 2 重点一：Cu/Fe 配位、ROS、脂质过氧化与神经毒性的因果验证路线

### 2.1 文献确立的机制链条

现有高分文献已将"金属配位 → 金属还原 → ROS 生成 → 脂质过氧化 → 神经损伤"这条链路的每一环节分别做实，这是本课题可借鉴、可验证的因果骨架：

1. **金属配位与还原**：Aβ（及其含 His 的片段）N 端 His6/His13/His14 等残基可配位 Cu²⁺（报道的 Kd 多在纳摩尔至亚微摩尔范围），并使 Cu²⁺ 还原为 Cu⁺、Fe³⁺ 还原为 Fe²⁺。Huang 等（*Biochemistry*, 1999）用细胞外实验直接证明 **Aβ 通过金属离子还原产生 H₂O₂** [C7]；其后续 JBC 工作进一步显示 **Cu(II) 剂量依赖地增强 Aβ 的细胞毒性，且毒性强度与无细胞体系中的 H₂O₂ 产量、金属还原能力定量相关**（Aβ42 > Aβ40 ≫ 鼠 Aβ40）[S3]。
2. **催化性 H₂O₂ 生成**：Opazo 等（*J Biol Chem*, 2002）证明 Aβ 具有"类金属酶"活性——在 Cu 存在下可催化多巴胺、胆固醇等生理还原剂持续产生神经毒性 H₂O₂（对 Cu 依赖、可被 Cu 螯合抑制）[C5]。这为"微量金属 + 生理还原底物 → 持续 ROS"提供了机制模板：**肽–金属复合物只要具备氧化还原循环能力，即可成为稳态 ROS 发生器**。
3. **Fenton/Haber–Weiss 化学**：Cu⁺/Fe²⁺ 与 H₂O₂ 发生 Fenton 型反应生成羟基自由基（•OH）——这是对脂质、蛋白、DNA 氧化修饰最强的物种。Cheignon 等（*Redox Biol*, 2018）系统综述了 Aβ–Cu/Fe 的氧化还原循环、H₂O₂ 与 •OH 生成及其与 AD 氧化应激的关系 [S8]；Hureau & Faller（*Biochimie*, 2009）从配位结构角度阐明 Cu–Aβ 产 ROS 的机制及其结构决定因素 [S6]。
4. **脂质过氧化**：•OH 攻击多不饱和脂肪酸引发链式脂质过氧化，生成 4-羟基壬烯醛（4-HNE）、丙二醛（MDA）等毒性醛类，后者共价修饰蛋白（4-HNE-蛋白加合物）。Butterfield & Lauderback（*Free Radic Biol Med*, 2002）总结了 AD 脑中脂质过氧化与蛋白氧化的病理证据，并将其与 Aβ 相关的自由基氧化应激联系起来 [S4]。
5. **神经毒性读出**：Walsh 等（*Nature*, 2002）证明天然分泌的 **Aβ 寡聚体在体内（大鼠海马）抑制长时程增强（LTP）**，确立"可溶性寡聚体—突触毒性"这一功能性读出 [C2]；Huang 等（JBC, 1999）则直接给出"Cu 依赖 H₂O₂ 与细胞毒性相关"的因果证据 [S3]。

### 2.2 建议的因果验证路线（按证据等级递进）

| 层级 | 内容 | 关键实验 | 核心文献 |
|---|---|---|---|
| L1 化学证据 | 肽–金属配位与还原活性 | ITC/UV–vis 滴定（Kd、化学计量）；EPR 定 Cu²⁺ 配位环境；bathocuproine/ferrozine 法测 Cu⁺/Fe²⁺ 生成速率；Amplex Red/过氧化物酶偶联法测 H₂O₂ 产量；氧化还原电位（循环伏安） | [C5][C7][S8] |
| L2 分子证据 | 自由基种类与脂质损伤 | EPR 自旋捕集（•OH/O₂•⁻）；荧光/比色脂质过氧化（BODIPY 581/591 C11、TBARS/MDA）；4-HNE 蛋白加合物 Western blot | [S4][S8] |
| L3 细胞证据 | 神经元表型 | SH-SY5Y/PC12/iPSC 神经元：MTT/CCK-8、LDH、膜完整性；DCFH-DA/MitoSOX（胞内 ROS/线粒体 ROS）；BODIPY C11 氧化比率流式/成像 | [S3][S8] |
| L4 因果操纵 | 反向验证（最关键） | ① 金属螯合剂（Cu：bathocuproine、TTM；Fe：去铁胺/去铁酮）；② 过氧化氢酶清除 H₂O₂；③ 抗氧化剂（NAC、维生素 E）；④ Chelex 处理缓冲液 + 无金属对照肽；⑤ 细胞铁/铜稳态基因操纵（FTH1、ATP7A 等，可选） | [C5][S3][S7] |
| L5 整合判据 | 因果性判定 | 金属剂量依赖、时间顺序（ROS 先于脂质过氧化先于死亡）、干预可逆转表型、无金属条件下无显著效应 | [C5][S8] |

**因果判定的操作性标准（建议写入方案）**：只有当 ① 效应依赖 Cu/Fe（剂量-反应）；② ROS/脂质过氧化信号在时间上先于细胞损伤；③ 螯合剂、过氧化氢酶或抗氧化剂能够逆转或消除表型时，才支持"金属相关促氧化神经毒性"这一因果解释。这与原方案 4.4 的表述一致，并给出可执行的对照矩阵。

---

## 3 重点二：Aβ42、tau、ApoE4、ferritin/transferrin 的合理定位与实验边界

### 3.1 各靶点定位与证据等级

| 靶点 | 科学定位 | 证据等级 | 建议实验边界 | 核心文献 |
|---|---|---|---|---|
| **Aβ42** | AD 核心病理蛋白；可溶性寡聚体为突触毒性主因 | 强（体内功能性证据：LTP 抑制） | 体外：ThT/浊度/EM/AUC 聚集实验 ± 金属；细胞：寡聚体水平（WB/寡聚体抗体）与 Aβ42/Aβ40 比值；结论限定"体外聚集/构象调节"，不做体内因果断言 | [C2][C7] |
| **tau** | NFT 主要组分；致病机制为"播种–招募"扩增 | 中-强（细胞播种证据充分） | 探索性：ThT/超速离心 + 细胞播种报告系统（FRET/BiFC biosensor）；仅在显示直接结合/聚集调节后再深化；无必要做 tau 激酶活性测定 | [C6] |
| **ApoE4** | 最强遗传风险因子；多效性（脂代谢、Aβ 清除、神经修复、铁稳态调控） | 遗传学强、机制复杂 | 功能读出优先：ApoE2/E3/E4 异构体对照下的脂化/结合实验、Aβ 清除实验；仅异构体特异效应才具解释力；对接仅作假设生成 | [C12][S5][C3] |
| **ferritin** | 脑铁储存蛋白；CSF ferritin 是 AD 进展与 APOE 关联的可测通路 | 强（前瞻队列） | 功能节点而非结合靶点：细胞铁含量（ICP-MS/ferrozine）、H/L 亚基比例、labile iron pool（calcein 探针）、TfR1/ferroportin 表达 | [C3][C8][C9] |
| **transferrin** | 脑铁转运载体（Tf–TfR1 介导摄取）；脑内铁稳态枢纽 | 强（综述共识） | 同上，功能读出（Tf 饱和度、TfR1 介导摄取）；结构对接仅作假设生成 | [C9][C8] |

### 3.2 关键文献要点

- **Aβ42**：Walsh 2002（*Nature*）——自然分泌寡聚体在无单体与纤维的条件下即可抑制大鼠海马 LTP，且 γ-分泌酶抑制剂阻断寡聚体形成后可逆转该效应 [C2]。这提示：**任何候选肽的"抗/促 Aβ 聚集"效应若要转化为功能性结论，必须落到寡聚体水平的功能读出（突触可塑性或细胞表型）**。
- **tau**：Guo & Lee 2011（*J Biol Chem*）——微量预成形 tau 纤维（pffs）即可通过胞吞进入细胞、招募可溶性 tau 形成 NFT 样包涵体，确立"播种-招募"模型 [C6]。候选肽若涉及 tau，最合理的定位是"对 tau 播种/聚集的体外调节"，且需先排除非特异效应。
- **ApoE4**：Strittmatter 1993（*PNAS*）确立 ApoE4 等位基因在晚发家族性 AD 中频率升高并与 Aβ 高亲和结合 [S5]；Huang & Mahley 2014（*Neurobiol Dis*）系统阐明 ApoE 异构体的结构差异（domain interaction）、在脂代谢、Aβ 清除、tau 磷酸化与神经修复中的多效性 [C12]；Ayton 2015（*Nat Commun*）进一步显示 **APOE 基因型调控 CSF ferritin 水平，CSF ferritin 预测 MCI→AD 转化与认知下降** [C3]——这是"APOE–铁稳态–AD 结局"的桥梁证据，也直接支持 3.3 中对 ferritin 的功能节点定位。
- **ferritin/transferrin 与脑铁代谢**：Zecca 2004（*Nat Rev Neurosci*）与 Ward 2014（*Lancet Neurol*）给出脑铁代谢完整网络：Tf–TfR1 摄取、ferritin 储存、ferroportin/铜蓝蛋白释放、非转铁蛋白结合铁（NTBI）等，并综述铁累积与氧化应激、神经退行性疾病的关系 [C8][C9]。**ferritin/transferrin 是"铁稳态的功能节点"，文献中并不支持将其当作与 Aβ/AChE 并列的"直接致病结合靶点"**。

### 3.3 对原方案 4.2 的修订建议（重要）

原方案将 ferritin/transferrin 与 Aβ42、tau、ApoE4 并列作"结构分析靶点"。建议按文献证据改为**两级设计**：

1. **主靶点（有强文献支撑）**：AChE/BChE（酶活 + PAS 位点）、Aβ42（聚集/寡聚体）。这两者与 AD 病理的关联最直接、读出最成熟。
2. **功能节点（替代"直接结合靶点"表述）**：ferritin/transferrin——不宣称为"未经验证的直接致病结合靶点"，而是评估候选肽对铁稳态读出（细胞铁含量、labile iron pool、ferritin 亚基、TfR1 表达）的影响；若体外出现与铁蛋白/转铁蛋白的分子对接命中，仅作为假设生成输入，必须由上述功能实验裁决。
3. **探索性靶点（明确边界）**：tau、ApoE4——先做直接结合/聚集证据，再考虑深化；不做无证据支撑的强关联断言。

---

## 4 重点三：AlphaFold 3、多构象采样、MD、MM/GBSA、QM/MM/DFT 的正确使用方式

### 4.1 AlphaFold 3（AF3）

- **能力**：AF3 采用扩散式架构，可联合预测蛋白质–核酸–小分子–离子–修饰残基复合物结构；其蛋白–配体相互作用精度显著优于此前专用对接工具，抗体-抗原精度也超过 AlphaFold-Multimer v2.3（Abramson 等，*Nature*, 2024）[C1]。
- **正确用法**：
  1. 输入：肽序列 + 靶蛋白序列（AChE/BChE 等）；金属离子与配体以 SMILES/离子形式加入——但 **AF3 对金属离子的处理能力有限，金属配位几何常不可靠，输出需逐条人工检查**；
  2. 输出解读：以 ipTM/pTM、界面 pLDDT、PAE 为依据；低置信区域不得作为结论；
  3. **多构象采样**：多次 seed + 温度/随机采样生成构象集合（ensemble），按 RMSD/PAE 聚类，而非报告单一结构——短肽（7–15 aa）构象柔性大，单结构必然失真；
  4. 边界：AF3 给出的是"折叠/复合物结构假设"，不提供结合亲和力、动力学与电子结构信息；对 intrinsically disordered 短肽（如 Aβ 片段）置信度低；**可作为建模参考，不能替代实验结构测定**（与原方案 4.1 一致）。
- 建议工作流：AF3 多构象采样 → 聚类选择代表性复合物 → 作为 MD 起点；AF3 评分仅用于候选排序。

### 4.2 分子动力学（MD）

- 依据：Hollingsworth & Dror（*Neuron*, 2018）是 MD 在神经科学/药物发现中正确使用的权威综述：MD 提供原子级时间分辨的构象行为，适合回答"结合是否稳定、哪个残基接触、构象如何演化"等问题 [S9]。
- **正确做法**：
  1. 显式溶剂（TIP3P/OPC 水 + 生理离子强度），能量最小化 → 平衡（NVT→NPT）→ 生产运行；
  2. **重复 ≥3 次独立运行**，用 RMSD/RMSF、接触残基驻留时间、氢键/盐桥占有率、自由能面（PCA/umbrella 可选）判断收敛；
  3. 力场：蛋白 ff14SB/ff19SB；**过渡金属（Cu²⁺、Fe²⁺/Fe³⁺、Zn²⁺）需要专用非键参数（如 12-6-4 LJ 参数或 QM 拟合参数），默认参数对金属配位会失效**——这是本课题最容易踩坑处；
  4. 分析：金属–配位残基（His/His/His、Cys/Met 等）距离时间序列、配位数与第一/第二配位层驻留、金属逸出事件。
- **边界**：经典 MD 无法描述键的断裂/形成、氧化还原反应、电子转移——这些必须交给 QM/MM 或 DFT。

### 4.3 MM/GBSA 与 MM/PBSA

- 依据：Genheden & Ryde（*Expert Opin Drug Discov*, 2015）对 MM/PBSA–GBSA 的系统评价：方法介于经验打分与严格自由能微扰之间，适用于**同一受体-同系列配体的相对排序**；但存在明显近似——缺构象熵、忽略结合位点水分子数目与自由能，且方法变体多、性能随体系差异大 [C14]。
- **正确用法与边界**：
  1. 必须基于平衡后的 MD 轨迹做系综平均，而非单帧结构；
  2. **仅用于相对排序**（如 12 条肽两两比较），不得报为绝对结合自由能；
  3. **含金属配位键的体系慎用**：MM 无法描述配位键形成/断裂，建议对金属位点改用 QM/MM 或加 QM 校正（SQM/分块），或至少与实验（ITC 测 Kd）做平行校准；
  4. 结论需以实验亲和力或活性数据校正后才有意义。

### 4.4 QM/MM 与 DFT

- 依据：Senn & Thiel（*Angew Chem Int Ed*, 2009）为 QM/MM 方法的权威综述：对活性区域（金属 + 配体 + 第一配位层残基）用 QM 描述，其余用 MM，从而在合理成本下处理反应与电子过程 [C13]。
- **正确用法**：
  1. QM 区应包含金属离子 + 直接配位残基/配体 + 关键第二层（如参与质子转移的残基）；分层或 ONIOM 方案；
  2. 泛函/基组选择需针对过渡金属与色散作用校准（如 ωB97X-D、M06-2X 或加 D3 色散校正）；明确自旋态（Cu²⁺ d⁹；Fe²⁺/Fe³⁺ 高/低自旋）；
  3. 输出：配位几何优化、配位能、电荷/自旋布居、氧化还原电位、电子转移倾向（与 Marcus 理论结合可选）；
  4. **必须与实验光谱（EPR、UV–vis、XAS、循环伏安）对照校准**——DFT 对过渡金属自旋态与色散的误差不可忽略。
- 适用顺序（建议）：对接/AF3 筛构象 → MD 验证稳定性与配位驻留 → MM/GBSA 相对排序 → 对排名靠前的稳定金属配位体系做 QM/MM/DFT（配位几何、氧化态、电子转移）→ 实验光谱校准。

### 4.5 计算–实验证据等级小结

| 计算方法 | 可回答的问题 | 不可回答的问题 | 正确角色 |
|---|---|---|---|
| AlphaFold 3 | 复合物结构假设、界面残基 | 亲和力、动力学、金属配位准确性 | 构象生成与排序起点 |
| MD | 结合稳定性、柔性、配位驻留 | 反应、电子转移 | 动态验证与筛选 |
| MM/GBSA | 同系列相对排序 | 绝对亲和力、配位键体系 | 排序（需实验校准） |
| QM/MM/DFT | 配位几何、氧化态、电子转移 | 大尺度构象采样 | 终局电子结构分析（需光谱校准） |
| 实验（ITC/EPR/光谱） | 真值 | —— | 裁决一切计算结论 |

---

## 5 重点四：12 条肽从初筛到 iPSC 神经元验证的分阶段 Go/No-Go 方案

### 5.1 总体漏斗（建议 12 → 8 → 4 → 2 → 1–2 条先导肽）

每阶段输出"进入下一阶段的候选子集"，并设置**可否决的 No-Go 判据**，避免资源浪费在无金属/无酶活响应的序列上。

### 5.2 分阶段方案与判据

**Stage 0 — 计算初筛（现状：已完成 AChE-PAS 对接 + MD 准备）**
- 输入：12 条候选肽（7–15 aa 短肽 + 长肽）。
- 输出：AChE PAS 结合模式（PAS 关键残基：Trp286、Tyr72、Tyr124、Asp74 等）、对接打分、MD 稳定性（RMSD 平台、PAS 位点驻留、接触矩阵）、ADMET/毒性预测。
- **Go**：MD 稳定（RMSD 达平台）、PAS 关键残基接触保持、无毒性预警 → 12→8。
- **No-Go**：MD 中肽脱离 PAS 或无特异结合模式 → 淘汰，不再合成。

**Stage 1 — 化学合成与体外生化表征（4–8 周）**
- 指标：纯度（HPLC ≥95%）、溶解度、血清/缓冲液稳定性；金属结合（ITC/UV–vis：Cu²⁺/Fe²⁺/Zn²⁺ 的 Kd 与化学计量）；金属还原与 H₂O₂ 生成（无细胞体系）；AChE/BChE 酶活（Ellman 法）；Aβ42 聚集 ± 金属（ThT/EM）。
- **Go**：≥2 项独立阳性读出，例如：金属依赖 H₂O₂ 生成 ≥2× 对照肽（且可被螯合剂抑制）；或 AChE/BChE 活性调节 IC50 <50 μM；或 Aβ42 聚集调节 ≥30%（±金属矩阵一致）。
- **No-Go**：无金属结合、无 ROS、无酶活/聚集效应 → 终止该肽。

**Stage 2 — 神经元细胞模型（4–6 周）**
- 模型：SH-SY5Y / PC12 / 原代皮层神经元。
- 指标：细胞活力（MTT/LDH）；胞内 ROS（DCFH-DA）与线粒体 ROS（MitoSOX）；脂质过氧化（BODIPY C11 氧化比率、4-HNE 加合物 WB）；**金属矩阵**：±Cu²⁺/Fe²⁺、±螯合剂、±过氧化氢酶/抗氧化剂。
- **Go**：金属依赖的"ROS↑ + 脂质过氧化↑ + 细胞损伤"三联表型，且螯合剂/过氧化氢酶/抗氧化剂可逆转 → 8→4。
- **No-Go**：无金属依赖表型，或仅有与金属无关的非特异毒性 → 终止。

**Stage 3 — iPSC 神经元验证（6–12 个月）**
- 依据：iPSC 来源神经元可重现 AD 关键表型——Israel 等（*Nature*, 2012）证明家族性 AD（APP 复制、PS1 突变）患者的 iPSC 神经元表现出 Aβ42 升高、p-tau 增加与 GSK-3β 激活，且 β/γ-分泌酶抑制剂可降低 p-tau [S1]；Kondo 等（*Cell Stem Cell*, 2013）证明 fAD iPSC 神经元出现细胞内 Aβ 积累与内质网/高尔基体应激、氧化应激表型，且对药物反应存在差异 [S2]。
- 设计：等基因/异基因对照（健康 donor；可选 APOE3/4 敲入系、fAD 突变系）；分化 >60 天成熟神经元；读出包括 Aβ42/Aβ40（ELISA/MSD）、p-tau、ROS（CellROX/MitoSOX）、脂质过氧化（BODIPY/4-HNE）、神经突网络（MAP2/βIII-tubulin）、突触标志（PSD95/SYN1）、功能（MEA 或钙成像）、细胞活力。
- **Go**：金属存在下 ROS/脂质过氧化增加并伴随神经元损伤、无金属时低毒（与原方案 4.4 的因果标准一致）→ 确定 1–2 条先导肽，进入先导优化。
- **No-Go**：iPSC 神经元上无金属依赖表型，或毒性不伴随氧化损伤机制 → 终止该项目/转向其他机制假说。

**Stage 4 — 体内/转化（非本阶段范围）**
- 前置条件：Stage 3 满足 Go 且机制链条完整（金属依赖、可干预逆转）。体内研究（APP/PS1 或 APOE4 小鼠、铁/铜负荷模型）需另行方案与伦理审批，本阶段不承诺。

### 5.3 Go/No-Go 判据汇总表

| 阶段 | 时间 | 关键指标 | Go 判据 | No-Go 判据 |
|---|---|---|---|---|
| 0 计算 | 已完成/2–4 周 | 对接 + MD 稳定性 | PAS 特异结合、MD 稳定 | 无 PAS 结合、MD 发散 |
| 1 生化 | 4–8 周 | 纯度、金属结合、H₂O₂、AChE/BChE、Aβ42 聚集 | ≥2 项独立阳性读出 | 全部阴性 |
| 2 细胞 | 4–6 周 | 活力、ROS、脂质过氧化、金属矩阵 | 金属依赖三联表型 + 干预逆转 | 无金属依赖或非特异毒性 |
| 3 iPSC | 6–12 月 | Aβ、p-tau、ROS、脂质过氧化、网络/功能、活力 | 金属依赖损伤 + 氧化机制一致 | 无表型或机制不符 |
| 4 体内 | 后续 | 认知/病理/铁稳态 | 先满足 0–3 全部 Go | —— |

---

## 6 特别提示（关键科学纠偏）

### 6.1 Zn²⁺ 不是 Fenton 型 ROS 金属

- **化学依据**：Zn²⁺ 为 d¹⁰ 闭壳层离子，氧化还原惰性，**无法像 Cu²⁺/Cu⁺、Fe³⁺/Fe²⁺ 那样进行单电子氧化还原循环**，因此不能直接催化 Fenton/Haber–Weiss 反应生成 ROS。
- **文献定位**：Sensi 等（*Nat Rev Neurosci*, 2009）将 Zn 定位为 CNS 的关键信号离子，其病理机制是谷氨酸能兴奋毒性、线粒体功能障碍、锌稳态失调及 Zn–Aβ 相互作用（促进 Aβ 聚集）等，**并非"Zn–Fenton 产 ROS"** [C10]。
- **实验含义**：
  1. 方案 4.3 中 Zn²⁺ 与 Cu²⁺/Fe²⁺ 并列考察是合理的（配位化学层面），但 **ROS/脂质过氧化机制表述必须将 Zn 与 Cu/Fe 区分**；
  2. Zn²⁺ 组应作为"聚集/配位/毒性对照"，若 Zn 组出现 ROS 增加，应寻求其他机制解释（如线粒体损伤、能量耗竭的继发效应），**不得写作"Zn 介导 Fenton 反应"**；
  3. 文献中亦有 Zn 竞争 Cu 位点而抑制 Cu–Aβ 产 ROS 的机制讨论 [S6]，设计金属矩阵时 Zn 可作为 Cu 的竞争性对照。

### 6.2 ferritin/transferrin 优先作为铁稳态功能节点

- **文献依据**：脑铁代谢网络中，transferrin 经 Tf–TfR1 介导神经元/胶质细胞铁摄取，ferritin（H/L 亚基）负责铁的储存与解毒，ferroportin/铜蓝蛋白介导释放 [C8][C9]；CSF ferritin 水平预测 AD 结局并受 APOE 调控 [C3]。
- **定位建议**：在方案 4.2 中，ferritin/transferrin 应从"直接致病结合靶点（与 AChE、Aβ 并列）"降格为**铁稳态功能节点**：
  1. 结构/对接分析仅作假设生成；
  2. 主实验改为功能读出：细胞内铁含量（ICP-MS/ferrozine）、labile iron pool（calcein/FRET 探针）、ferritin H/L 蛋白与亚基比、TfR1/ferroportin 表达、转铁蛋白饱和度；
  3. 只有当候选肽显著改变上述功能指标时，才讨论其铁稳态相关作用；
  4. 避免在缺乏功能证据时宣称"候选肽与 ferritin/transferrin 直接结合致病"。

---

## 7 参考文献

### 7.1 核心文献（14 篇，含 *Nature*、*Nature Communications*、*Neuron*、*JBC*、*Biochemistry* 等）

| # | 文献（期刊 年；卷:页） | DOI | PMID |
|---|---|---|---|
| C1 | Abramson J, et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. *Nature* 2024; 630:493-500. | [10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w) | [38718835](https://pubmed.ncbi.nlm.nih.gov/38718835/) |
| C2 | Walsh DM, et al. Naturally secreted oligomers of amyloid beta protein potently inhibit hippocampal long-term potentiation in vivo. *Nature* 2002; 416:535-539. | [10.1038/416535a](https://doi.org/10.1038/416535a) | [11932745](https://pubmed.ncbi.nlm.nih.gov/11932745/) |
| C3 | Ayton S, Faux NG, Bush AI; Alzheimer's Disease Neuroimaging Initiative. Ferritin levels in the cerebrospinal fluid predict Alzheimer's disease outcomes and are regulated by APOE. *Nature Communications* 2015; 6:6760. | [10.1038/ncomms7760](https://doi.org/10.1038/ncomms7760) | [25988319](https://pubmed.ncbi.nlm.nih.gov/25988319/) |
| C4 | Inestrosa NC, et al. Acetylcholinesterase accelerates assembly of amyloid-beta-peptides into Alzheimer's fibrils: possible role of the peripheral site of the enzyme. *Neuron* 1996; 16:881-891. | [10.1016/S0896-6273(00)80108-7](https://doi.org/10.1016/S0896-6273(00)80108-7) | [8608006](https://pubmed.ncbi.nlm.nih.gov/8608006/) |
| C5 | Opazo C, et al. Metalloenzyme-like activity of Alzheimer's disease beta-amyloid. Cu-dependent catalytic conversion of dopamine, cholesterol, and biological reducing agents to neurotoxic H₂O₂. *J Biol Chem* 2002; 277:40302-40308. | [10.1074/jbc.M206428200](https://doi.org/10.1074/jbc.M206428200) | [12192006](https://pubmed.ncbi.nlm.nih.gov/12192006/) |
| C6 | Guo JL, Lee VM. Seeding of normal Tau by pathological Tau conformers drives pathogenesis of Alzheimer-like tangles. *J Biol Chem* 2011; 286:15317-15331. | [10.1074/jbc.M110.209296](https://doi.org/10.1074/jbc.M110.209296) | [21372138](https://pubmed.ncbi.nlm.nih.gov/21372138/) |
| C7 | Huang X, et al. The A beta peptide of Alzheimer's disease directly produces hydrogen peroxide through metal ion reduction. *Biochemistry* 1999; 38:7609-7616. | [10.1021/bi990438f](https://doi.org/10.1021/bi990438f) | [10386999](https://pubmed.ncbi.nlm.nih.gov/10386999/) |
| C8 | Zecca L, Youdim MB, Riederer P, Connor JR, Crichton RR. Iron, brain ageing and neurodegenerative disorders. *Nat Rev Neurosci* 2004; 5:863-873. | [10.1038/nrn1537](https://doi.org/10.1038/nrn1537) | [15496864](https://pubmed.ncbi.nlm.nih.gov/15496864/) |
| C9 | Ward RJ, Zucca FA, Duyn JH, Crichton RR, Zecca L. The role of iron in brain ageing and neurodegenerative disorders. *Lancet Neurology* 2014; 13:1045-1060. | [10.1016/S1474-4422(14)70117-6](https://doi.org/10.1016/S1474-4422(14)70117-6) | [25231526](https://pubmed.ncbi.nlm.nih.gov/25231526/) |
| C10 | Sensi SL, Paoletti P, Bush AI, Sekler I. Zinc in the physiology and pathology of the CNS. *Nat Rev Neurosci* 2009; 10:780-791. | [10.1038/nrn2734](https://doi.org/10.1038/nrn2734) | [19826435](https://pubmed.ncbi.nlm.nih.gov/19826435/) |
| C11 | Darvesh S, Hopkins DA, Geula C. Neurobiology of butyrylcholinesterase. *Nat Rev Neurosci* 2003; 4:131-138. | [10.1038/nrn1035](https://doi.org/10.1038/nrn1035) | [12563284](https://pubmed.ncbi.nlm.nih.gov/12563284/) |
| C12 | Huang Y, Mahley RW. Apolipoprotein E: structure and function in lipid metabolism, neurobiology, and Alzheimer's diseases. *Neurobiol Dis* 2014; 72 Pt A:3-12. | [10.1016/j.nbd.2014.08.025](https://doi.org/10.1016/j.nbd.2014.08.025) | [25173806](https://pubmed.ncbi.nlm.nih.gov/25173806/) |
| C13 | Senn HM, Thiel W. QM/MM methods for biomolecular systems. *Angew Chem Int Ed Engl* 2009; 48:1198-1229. | [10.1002/anie.200802019](https://doi.org/10.1002/anie.200802019) | [19173328](https://pubmed.ncbi.nlm.nih.gov/19173328/) |
| C14 | Genheden S, Ryde U. The MM/PBSA and MM/GBSA methods to estimate ligand-binding affinities. *Expert Opin Drug Discov* 2015; 10:449-461. | [10.1517/17460441.2015.1032936](https://doi.org/10.1517/17460441.2015.1032936) | [25835573](https://pubmed.ncbi.nlm.nih.gov/25835573/) |

### 7.2 补充文献（10 篇，供深入检索与写作引用）

| # | 文献（期刊 年；卷:页） | DOI | PMID |
|---|---|---|---|
| S1 | Israel MA, et al. Probing sporadic and familial Alzheimer's disease using induced pluripotent stem cells. *Nature* 2012; 482:216-220. | [10.1038/nature10821](https://doi.org/10.1038/nature10821) | [22278060](https://pubmed.ncbi.nlm.nih.gov/22278060/) |
| S2 | Kondo T, et al. Modeling Alzheimer's disease with iPSCs reveals stress phenotypes associated with intracellular Aβ and differential drug responsiveness. *Cell Stem Cell* 2013; 12:487-496. | [10.1016/j.stem.2013.01.009](https://doi.org/10.1016/j.stem.2013.01.009) | [23434393](https://pubmed.ncbi.nlm.nih.gov/23434393/) |
| S3 | Huang X, et al. Cu(II) potentiation of Alzheimer abeta neurotoxicity. Correlation with cell-free hydrogen peroxide production and metal reduction. *J Biol Chem* 1999; 274:37111-37116. | [10.1074/jbc.274.52.37111](https://doi.org/10.1074/jbc.274.52.37111) | [10601271](https://pubmed.ncbi.nlm.nih.gov/10601271/) |
| S4 | Butterfield DA, Lauderback CM. Lipid peroxidation and protein oxidation in Alzheimer's disease brain: potential causes and consequences involving amyloid beta-peptide-associated free radical oxidative stress. *Free Radic Biol Med* 2002; 32:1050-1060. | [10.1016/S0891-5849(02)00794-3](https://doi.org/10.1016/S0891-5849(02)00794-3) | [12031889](https://pubmed.ncbi.nlm.nih.gov/12031889/) |
| S5 | Strittmatter WJ, et al. Apolipoprotein E: high-avidity binding to beta-amyloid and increased frequency of type 4 allele in late-onset familial Alzheimer disease. *Proc Natl Acad Sci USA* 1993; 90:1977-1981. | [10.1073/pnas.90.5.1977](https://doi.org/10.1073/pnas.90.5.1977) | [8446617](https://pubmed.ncbi.nlm.nih.gov/8446617/) |
| S6 | Hureau C, Faller P. Abeta-mediated ROS production by Cu ions: structural insights, mechanisms and relevance to Alzheimer's disease. *Biochimie* 2009; 91:1212-1217. | [10.1016/j.biochi.2009.03.013](https://doi.org/10.1016/j.biochi.2009.03.013) | [19332103](https://pubmed.ncbi.nlm.nih.gov/19332103/) |
| S7 | Greenough MA, Camakaris J, Bush AI. Metal dyshomeostasis and oxidative stress in Alzheimer's disease. *Neurochem Int* 2013; 62:540-555. | [10.1016/j.neuint.2012.08.014](https://doi.org/10.1016/j.neuint.2012.08.014) | [22982299](https://pubmed.ncbi.nlm.nih.gov/22982299/) |
| S8 | Cheignon C, et al. Oxidative stress and the amyloid beta peptide in Alzheimer's disease. *Redox Biol* 2018; 14:450-464. | [10.1016/j.redox.2017.10.014](https://doi.org/10.1016/j.redox.2017.10.014) | [29080524](https://pubmed.ncbi.nlm.nih.gov/29080524/) |
| S9 | Hollingsworth SA, Dror RO. Molecular Dynamics Simulation for All. *Neuron* 2018; 99:1129-1143. | [10.1016/j.neuron.2018.08.011](https://doi.org/10.1016/j.neuron.2018.08.011) | [30236283](https://pubmed.ncbi.nlm.nih.gov/30236283/) |
| S10 | Alvarez A, Opazo C, Alarcon R, Garrido J, Inestrosa NC. Acetylcholinesterase promotes the aggregation of amyloid-beta-peptide fragments by forming a complex with the growing fibrils. *J Mol Biol* 1997; 272:348-361. | [10.1006/jmbi.1997.1245](https://doi.org/10.1006/jmbi.1997.1245) | [9325095](https://pubmed.ncbi.nlm.nih.gov/9325095/) |

> S10 与本课题直接相关：AChE 可促进 Aβ(12–28) 与 Aβ(25–35) 片段聚集（而对 Aβ(1–16) 无效），提示 AChE–短肽相互作用存在序列特异性——可作为候选肽对接/聚集实验的阳性对照框架。

---

## 8 方法学与局限性

1. **检索策略**：按 AERS 文献综述流程，先确定 5 个重点概念（Cu/Fe–ROS–脂质过氧化–神经毒性；Aβ42/tau/ApoE4/ferritin/transferrin 定位；AlphaFold3/MD/MM-GBSA/QM-MM 方法学；iPSC 神经元验证；Zn 非 Fenton 金属）生成关键词，再以"作者+标题关键词+年份"组合在 PubMed 检索，优先选择高影响力期刊（*Nature*、*Nat Commun*、*Neuron*、*JBC*、*Biochemistry*、*Nat Rev Neurosci*、*Lancet Neurol* 等）与高被引文献。
2. **核验方式**：所有 DOI/PMID 经 PubMed E-utilities 记录比对；DOI 链接基于 PubMed 登记的官方 DOI 构造（doi.org 解析地址），未使用任何未经核验的引用。
3. **局限性**：本报告主要基于摘要、综述与领域共识性证据，未逐篇全文精读；文献检索截至 2026-08-02；对文献结论的转述以原文为准，若用于论文写作请核对原文表述。Go/No-Go 判据中的具体阈值（如 ≥2×、IC50 <50 μM、≥30%）为建议值，应由课题组根据前期数据与文献基准（如 Aβ–Cu 的 Kd、已知 ROS 肽对照）最终确定。
