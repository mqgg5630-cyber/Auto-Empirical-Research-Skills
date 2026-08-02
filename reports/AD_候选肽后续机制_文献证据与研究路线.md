# 12 条候选肽：AChE–PAS 对接后的机制研究路线与核心文献

**用途**：为已完成的 12 条肽–AChE PAS 分子对接及拟开展的 MD，建立可检验、不过度外推的 AD 相关机制研究框架。  
**检索与整理日期**：2026-08-02。  
**重要边界**：目前没有提供 12 条序列、来源、修饰状态、净电荷或对接构象。因此，本报告提出的是“候选肽优先级与验证路线”，不能据此断言任一肽具有促氧化/神经毒性或抗 AD 活性。尤其是 7–15 aa 肽高度柔性，单一 docking score 不能作为结合或机制证据。

---

## 一、结论先行：最值得做的三条机制链

### 主线 1（优先级最高）：AChE–PAS 占位 → AChE 促 Aβ42 聚集是否被改变
这是与现有结果衔接最紧、实验可证伪性最高的主线。AChE 可通过 PAS 促进 Aβ 成纤维；该作用不依赖催化位点抑制，并会被 PAS 配体 propidium 抑制，而缺少 PAS 的 BChE 未显示同类促聚集作用 [1]。因此，候选肽的关键不是“PAS docking 分数高”，而是：

1. 是否真实结合 AChE 的 PAS（而非仅贴近 gorge 口）；
2. 是否同时/分别抑制 AChE 催化活性（CAS）和 AChE 促进 Aβ42 聚集的非催化功能；
3. 其对 Aβ42 单独聚集、AChE–Aβ42 复合聚集及细胞毒性是抑制、无效还是促进。

**最小可发表的证据组合**：SPR/MST 或 ITC（肽–AChE）+ Ellman（AChE/BChE）+ ThT 动力学（Aβ42 ± AChE ± 肽）+ TEM/AFM + Aβ 寡聚体特异 ELISA/dot blot。一定要纳入 PAS 阳性对照 propidium 或 fasciculin、CAS 对照 donepezil，以及 scrambled 肽。

### 主线 2（优先级最高）：Cu/Fe 配位–氧化还原循环 → ROS/脂质过氧化 → 神经元损伤
这条链最能直接检验题述“金属相关促氧化神经毒性”的因果主张。Aβ 可还原 Cu(II)/Fe(III)，在氧存在下产生 H2O2，并在 Cu/Fe 存在时出现与羟自由基生成相符的 TBARS 信号 [2]。APP 的富 His 铜结合肽段也曾增强铜相关脂质过氧化；将关键 His 置换为 Asn 后，毒性消失 [3]。这为“短肽–金属配位是否驱动氧化还原活性”提供了强的可检验先例。

但要特别区分：**Zn2+ 本身通常不是 Fenton 金属，不能与 Cu/Fe 同等地被表述为 ROS 催化剂**。Zn2+ 更应作为配位/聚集构象调节因子和竞争性金属对照；Cu/Fe 才是 ROS 因果实验的核心。

### 主线 3（第二优先级）：ApoE4–金属–Aβ / 铁稳态–tau–脂质过氧化
这条主线有 AD 相关性，但相对不适合一开始就做“候选肽直接 docking 到 ferritin/transferrin 后下机制结论”。ApoE 异构体会改变金属诱导 Aβ 聚集；在接近 CSF 的体外浓度下，ApoE4 条件下的 Zn/Cu 诱导 Aβ 聚集最高 [4]。CSF ferritin 在 AD 连续谱中与神经退行/炎症和 tau 指标相关 [5]，也与较快 Aβ 病理进展相关 [6]。这支持将 ApoE4、ferritin、transferrin 放入**分层调节因子/生物标志物**层面，而非未经实验验证地认定它们是候选肽的直接病原靶点。

---

## 二、按靶点重审：科学问题、可做/不可直接做的事

| 模块 | 文献支持的病理关联 | 对 12 条肽最合适的问题 | 关键否定对照/判读 |
|---|---|---|---|
| AChE PAS / CAS | AChE PAS 可促进 Aβ 聚集；CAS 负责胆碱酯水解 [1,7] | 肽是否 PAS 占位，是否改变 AChE–Aβ42 聚集和/或 AChE 活性？ | PAS 对照 propidium；CAS 对照 donepezil；BChE；scrambled 肽；无 AChE Aβ42 |
| BChE | BChE 与 AChE 口袋和 PAS 架构不同；不能以 AChE 结果外推 [1] | 肽对 BChE 是否有交叉抑制？ | Ellman IC50/Ki，报告 AChE/BChE 选择性；避免把 BChE 当 PAS 机制替代物 |
| Aβ42 | Cu/Zn/Fe 可改变 Aβ 聚集；Cu/Fe 可参与氧化还原 [2,8] | 肽是否改变 Aβ42 寡聚体、纤维、金属诱导聚集或 ROS？ | Aβ42 单独、各金属单独、肽单独，等离子强度/pH 对照；测游离金属 |
| tau | 金属失衡与 tau 磷酸化/聚集有关，但链条复杂 [8,9] | 候选肽能否改变 seed-induced tau 聚集或细胞内 p-tau？ | 先采用 tau K18/P301S 聚集体系，再进细胞；不要由对接直接推出“稳定 tau” |
| ApoE4 | ApoE4 是晚发 AD 最强遗传风险因素；可改变金属诱导 Aβ 聚集 [4,10] | ApoE2/3/4 是否改变肽对 Aβ–金属体系的效应？ | 必须并列 ApoE2、E3、E4；使用脂化重组 ApoE 或定义清楚的 rApoE |
| ferritin / transferrin | 反映铁储存/转运与 AD 病理、炎症、tau 的关系 [5,6,11] | 肽是否扰动 Fe 结合、铁释放或 TfR 摄取，而非是否“dock 到蛋白表面”？ | apo/holo-transferrin；ferritin Fe 负载状态；游离 Fe、pH、还原剂；ICP-MS/ferrozine |
| Cu2+、Fe2+/Fe3+、Zn2+ | 金属稳态失调与 Aβ/tau 和氧化应激相连，但体内总量结论并不一致 [8,12] | 肽的化学计量、亲和力、配位几何及 redox consequence 是什么？ | EDTA/BCS/DFO 等适当螯合对照；金属滴定；避免只凭 docking 声称“螯合” |

**对 ferritin/transferrin 的关键修正**：二者应先作为“铁稳态功能节点”研究。只有当通过直接结合及功能实验显示候选肽改变 ferritin 的储铁/释铁或 transferrin 的 Fe3+ 装载、TfR1 结合/摄取，才有依据进入蛋白–肽结构建模。它们不是与 AChE PAS 同等成熟的“小肽致病结合位点”。

---

## 三、建议的分阶段工作包（12 条肽可执行）

### WP0：先补齐候选肽可比性（所有后续工作的前提）

- 记录序列、N/C 端状态、环化/脂化/其他修饰、纯度、盐形式、分子量；用 LC–MS/HPLC 复核。
- 计算/实测净电荷、pI、His/Cys/Asp/Glu/Tyr/Met 数量、疏水性、聚集倾向、溶解度和血清稳定性。
- 设计每条肽的 scrambled 肽；若假设金属配位，另设计**配位残基突变肽**（例如 His→Ala/Asn，Asp/Glu→Asn/Gln）。这类“失配位突变”比仅用 docking 更能建立因果性。
- 先做无细胞的自聚集/浊度/ThT 背景和细胞培养基稳定性；短肽常出现假阳性荧光、表面吸附或胶体聚集。

### WP1：把现有 AChE–PAS 对接升级为可检验构象假说（优先）

**计算**

1. 使用人源 AChE 的实验结构，保留与实验 pH 一致的关键质子化状态；明确 CAS（Ser203–His447–Glu334）与 PAS（Tyr72、Asp74、Tyr124、Trp286、Tyr337 等）的接触占有率，而不是只报 docking score。
2. 每肽至少多起点、多重复 MD（建议每体系 ≥3 独立重复；生产段以收敛性而非固定时长为准）。报告 RMSD/RMSF、接触概率、氢键、芳香堆积、盐桥、水桥、gorge 出入口开闭及肽是否离位。
3. 对 PAS、CAS 与 gorge-spanning 三类姿势分别聚类；MM/GBSA 或 MM/PBSA 仅用于同一体系内的**相对排序**，不可当作绝对 Ki。
4. 加入 Aβ42 时，不宜用单一刚性 Aβ42 结构断言三元复合物。应使用 Aβ42 单体/寡聚体构象集合，比较 “AChE–Aβ42” 和 “AChE–肽–Aβ42” 的界面与可及性。

**实验门槛**

- AChE/BChE 抑制：Ellman 法测浓度–反应曲线，给出 IC50、Ki、抑制类型；检查肽对 DTNB/底物读数的干扰。
- 直接结合：优先 MST 或 SPR；对很短肽，应严防表面固定和质量传递假象。ITC 可在溶解度充分时用于给出化学计量和热力学。
- Aβ42：ThT 做全时程（lag time、增长速率、平台），并用 TEM/AFM + SEC-MALS 或 native PAGE/寡聚体抗体交叉验证。只用 ThT 不足以证明“抑制聚集”。

**Go/No-Go 条件**：仅保留满足“直接 AChE 结合 + 至少一种 AChE/Aβ 功能读出一致 + scrambled/竞争对照支持”的 3–4 条肽进入 WP2。

### WP2：金属配位、氧化还原与脂质过氧化（优先）

**先化学、后计算**。金属配位对质子化、溶剂、竞争配体和氧化态极其敏感，常规 protein–ligand docking 和经典力场不能单独验证配位键或电子转移。

1. **结合与化学计量**：以 Cu2+、Fe2+、Fe3+、Zn2+ 分别滴定肽；优先用 UV–Vis、CD、荧光猝灭（须排除内滤效应）、ITC、ESI-MS。可获得条件时，Cu 用 EPR，Fe 用 Mössbauer/EPR，配位几何可用 XAS/EXAFS。用竞争螯合剂估计条件稳定常数。
2. **redox 读出**：
   - Cu2+/Cu+：Cu(I) 特异探针或 BCS 捕获，配合 O2 消耗；
   - Fe3+/Fe2+：ferrozine 法定量 Fe2+；
   - H2O2：Amplex Red/HRP（同时设置肽/金属对荧光体系的直接干扰控制）；
   - 自由基：EPR spin trapping 是强证据；普通 DCFH-DA 不能作为唯一 ROS 结论。
3. **脂质过氧化**：无细胞 liposome/LDL 体系先筛，再进细胞。建议 C11-BODIPY 581/591、4-HNE/MDA 加合物；TBARS 可做但特异性不足，必须有正交读出。
4. **因果验证**：若肽+Cu/Fe 增加 ROS/LPO，效应应被合适螯合剂、配位残基突变肽及缺氧/抗氧化策略显著削弱；若没有这一组证据，只能称“相关”，不能称“金属配位导致”。

**计算分层**：

- 初筛：金属感知的构象采样/对接，用多个质子化状态及明确氧化态；把结果当作候选配位模型，而非结论。
- MD：必须采用经验证的金属参数或 bonded model，检查配位距离、配位数、配体交换及重复间一致性。对 Fe2+/Fe3+、Cu2+/Cu+ 应分别建模。
- QM/MM 或 DFT：只对 WP2 实验支持的 1–2 个体系。报告方法、基组、溶剂模型、自旋态（尤其 Fe/Cu）、BSSE/频率校正和与实验谱学的对应。所谓“配位能”必须说明参照态，避免跨电荷/跨自旋态的无意义比较。

### WP3：Aβ、tau、ApoE4 与铁稳态的分层验证（第二优先）

**Aβ42–金属–肽**

- 采用 full factorial 设计：肽（±）× 金属（无/Cu/Fe/Zn）× Aβ42（±），同时包括 AChE（±）。
- 输出至少包括：Aβ 聚集动力学、寡聚体比例、游离金属、H2O2/脂质过氧化。这样可区分“肽直接促聚集”“肽只在金属存在时促聚集”“肽只是改变 ROS 而非聚集”。

**tau**

- 先选一个明确体系：重组 tau K18/P301S 的 heparin 或 seed-induced 聚集，监测 FRET/ThT、沉淀比例和 TEM；细胞中再测 AT8/PHF-1 p-tau、可溶/不溶 tau、细胞活性。
- 仅当 Aβ/金属或 ROS 条件确实改变 tau 读数时，才将候选肽定位为该轴调节物。

**ApoE4**

- 以 ApoE2/E3/E4 并行而非只测 E4。优先问“E4 是否使肽的 Aβ–金属效应增强”，而不是先假设肽直接结合 ApoE4。
- 脂质化状态会改变 ApoE 行为；论文必须说明 ApoE 制备方式、脂蛋白颗粒/脂质组成和浓度。

**ferritin/transferrin**

- 在纯化体系先测铁释放/氧化还原（ferritin）以及 Fe3+ 装载、TfR1 结合或细胞摄取（transferrin）。
- 在神经元、星形胶质细胞和小胶质细胞中分别检测 labile iron pool、FTH1/FTL、TF、TFRC、FPN1、DMT1、hepcidin 与 ferritinophagy（NCOA4）。
- 如观察到 Fe 依赖性脂质过氧化，可加入 ferrostatin-1/liproxstatin-1、DFO，以及 GPX4、ACSL4、SLC7A11 指标，判断是否符合 ferroptosis；不能以“铁增加+细胞死”直接命名 ferroptosis。

### WP4：神经毒性与因果闭环（最终验证）

**推荐阶梯**：SH-SY5Y/HT22 初筛 → 人 iPSC 来源神经元（必要时与星形胶质/小胶质共培养）确认。若论文主张 AD 转化意义，后者明显更有说服力。

- 处理设计：肽单独、金属单独、肽+金属、Aβ42 单独、Aβ42+肽、Aβ42+金属+肽；每组加相应螯合/抗氧化/突变肽救援。
- 细胞读出：CellTiter-Glo/LDH + Annexin V/PI；线粒体膜电位；C11-BODIPY/4-HNE；神经突长度/突触标记；AChE/BChE 酶活。
- 必须区分细胞外配位、培养基中金属沉淀、肽吸附/摄取和真正细胞内效应。培养基中的白蛋白、血清、转铁蛋白会强烈竞争金属，建议在定义清楚的低蛋白/无血清短时体系和更生理的完全培养基中都验证。

**支持“金属相关促氧化神经毒性”的最低判定标准**：

> 候选肽在定义金属条件下，重复性地提高 ROS 和至少一种正交脂质过氧化指标，并降低神经细胞存活/损伤神经突；该效应被金属螯合、关键配位残基突变或抗氧化/抗铁死亡干预所削弱，并伴有可复核的金属结合/价态变化证据。

反之，任何一个单独的 docking score、MM/GBSA、DCFH-DA 信号或 MTT 下降，都不足以支持该结论。

---

## 四、AlphaFold 3 与多构象策略：应如何写进方案

AlphaFold 3 的原始 Nature 论文显示它可联合预测蛋白、核酸、小分子、离子与修饰残基组成的复合物 [13]。可将它用于生成“肽–靶标”结构假说和复合物初始构象；但短肽、多构象 Aβ/tau、金属配位和蛋白表面瞬时结合是其高风险场景。独立评估也指出 AF3 对本征柔性区域/结构域并不可靠，且 ipTM 不能捕获全部大误差 [14]。

**可执行规范**：

1. 不把 AF3 输出称为“肽的真实结构”；每个短肽使用多 seed、多模型、多起始构象。
2. 以跨模型重复出现的接触、界面 PAE、局部 pLDDT/ipTM 为筛选指标；低置信构象应保留为“未解析集合”，不是强行选一个赢家。
3. 对 Aβ42/tau，将 AF3 作为初始模型生成器，并以 enhanced-sampling MD、实验聚集数据和谱学约束验证。
4. 对 Cu/Fe/Zn，AF3/对接只提出“可能近邻残基”；配位数、键长、氧化态与电子转移必须由谱学 + QM/MM/DFT + 实验 redox 数据共同支持。

---

## 五、建议的论文叙事与优先级

### 最强、最聚焦的第一篇机制论文
**题眼**：`Short peptide X binds the AChE peripheral anionic site and modulates the AChE–Aβ42–metal oxidative axis`。

- 不必一次覆盖 ApoE4、tau、ferritin、transferrin 所有靶点。
- 从 12 条中以 WP1+WP2 的预注册式评分选 1 条主肽、1 条备选肽；其余作为 SAR/阴性对照。
- 主图逻辑：序列–构象集合 → AChE PAS 结合/酶学 → AChE–Aβ42 聚集 → 金属配位/红氧 → 脂质过氧化 → 神经元损伤与救援。

### 第二篇/扩展工作
将最可靠的肽放入 ApoE2/E3/E4 背景和人 iPSC 细胞模型，研究铁稳态与 tau 下游改变。这样可避免在第一篇中因靶点过多而每个机制证据不足。

### 不建议的做法

- 将 12 条肽同时对接 7 个大靶点后，凭 docking score 绘制完整 AD 机制网络；
- 将 Zn2+ 与 Cu/Fe 一并解释为 Fenton ROS 源；
- 用 MM/PBSA 的单点数值宣称结合亲和力或金属螯合能力；
- 未经直接结合/功能实验就称 ferritin/transferrin 为“致病靶点”；
- 将 AChE PAS 占位自动等同于 AChE 酶抑制或抗 Aβ 聚集。

---

## 六、核心 SCI 文献（按直接可用性精选）

### AChE–PAS–Aβ

1. **Inestrosa NC, et al.** Acetylcholinesterase accelerates assembly of amyloid-β-peptides into Alzheimer’s fibrils: possible role of the peripheral site of the enzyme. *Neuron* (1996). **PMID: 8608006**.  
   价值：最直接的 AChE–PAS 促 Aβ 聚集机制依据；propidium 抑制、BChE 不促聚集，是本项目最重要的阳性/机制对照来源。链接：[PubMed](https://pubmed.ncbi.nlm.nih.gov/8608006/)
2. **Inestrosa NC, et al.** Amyloid–cholinesterase interactions. *FEBS Journal* (2008). DOI: **10.1111/j.1742-4658.2007.06238.x**.  
   价值：总结 AChE–Aβ 复合体、PAS 阻断与神经毒性的机制背景。链接：[期刊](https://febs.onlinelibrary.wiley.com/doi/10.1111/j.1742-4658.2007.06238.x)

### Aβ–金属–氧化应激

3. **Huang X, et al.** The Aβ peptide of Alzheimer’s disease directly produces hydrogen peroxide through metal ion reduction. *Biochemistry* (1999) 38:7609–7616. DOI: **10.1021/bi990438f**.  
   价值：Cu(II)/Fe(III) 还原、H2O2、Fenton 型化学和 TBARS 的经典原始证据。链接：[ACS](https://pubs.acs.org/doi/10.1021/bi990438f)
4. **White AR, et al.** The Alzheimer’s disease amyloid precursor protein modulates copper-induced toxicity and oxidative stress in primary neuronal cultures. *Journal of Neuroscience* (1999). **PMCID: PMC6782934**.  
   价值：富 His 肽段、关键 His 突变、铜依赖脂质过氧化与神经元毒性的强因果范例。链接：[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6782934/)
5. **Bush AI, Tanzi RE.** Therapeutics for Alzheimer’s disease based on the metal hypothesis. *Neurotherapeutics* (2008).  
   价值：Aβ–Cu/Zn/Fe、聚集与金属稳态治疗假说的高质量综述。链接：[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1878747923004890)

### ApoE4、铁稳态、ferritin/transferrin

6. **Moir RD, et al.** Differential effects of apolipoprotein E isoforms on metal-induced aggregation of Aβ. *Journal of Biological Chemistry* (1999). **PMID: 10194381**.  
   价值：在近生理 CSF 浓度下，ApoE4 条件中 Cu/Zn 诱导 Aβ 聚集最高；直接支持 E2/E3/E4 并行实验。链接：[PubMed](https://pubmed.ncbi.nlm.nih.gov/10194381/)
7. **Ayton S, Faux NG, Bush AI; ADNI.** Ferritin levels in the cerebrospinal fluid predict Alzheimer’s disease outcomes and are regulated by APOE. *Nature Communications* (2015) 6:6760.  
   价值：高影响力纵向生物标志物论文；将 ferritin 与 APOE 和 AD 病程连接。链接：[PubMed](https://pubmed.ncbi.nlm.nih.gov/25772989/)
8. **Ayton S, Diouf I, Bush AI; ADNI.** Evidence that iron accelerates Alzheimer’s pathology: a CSF biomarker study. *Journal of Neurology, Neurosurgery & Psychiatry* (2018). **PMID: 28939683**.  
   价值：CSF ferritin 高与 Aβ 病理更快进展相关；不是直接肽靶点证据。链接：[PubMed](https://pubmed.ncbi.nlm.nih.gov/28939683/)
9. **Pan R, et al.** The associations of CSF ferritin with neurodegeneration and neuroinflammation along the AD continuum. *Journal of Alzheimer’s Disease* (2022). **PMID: 35754266**.  
   价值：ADNI 302 人，CSF ferritin 与 p-tau/t-tau、认知和炎症蛋白相关。链接：[PubMed](https://pubmed.ncbi.nlm.nih.gov/35754266/)
10. **Goozee K, et al.** Plasma transferrin and hemopexin are associated with altered Aβ and tau burden in Alzheimer’s disease. *Alzheimer’s Research & Therapy* (2020). **PMID: 32517787**.  
   价值：transferrin 与脑淀粉样沉积、海马体积和认知的队列关联；提示其适合作为铁稳态层的 readout。链接：[PubMed](https://pubmed.ncbi.nlm.nih.gov/32517787/)

### 综述、争议与方法边界

11. **Schrag M, et al.** Iron, zinc and copper in the Alzheimer’s disease brain: a quantitative meta-analysis. *Metallomics* (2011). DOI: **10.1039/C1MT00046K**.  
    价值：提醒不能将局部斑块金属富集混同于全脑“总金属升高”；金属总体结论有异质性和引用偏倚。链接：[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3134620/)
12. **Braidy N, et al.** Metals in Alzheimer’s disease. *International Journal of Molecular Sciences* (2023). **PMCID: PMC10136077**.  
    价值：覆盖 Aβ、tau、ApoE、金属稳态及临床转化局限的近期综述。链接：[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10136077/)
13. **Abramson J, et al.** Accurate structure prediction of biomolecular interactions with AlphaFold 3. *Nature* (2024) 630:493–500. DOI: **10.1038/s41586-024-07487-w**.  
    价值：AF3 原始论文；可用于复杂体系的候选构象生成。链接：[Nature](https://www.nature.com/articles/s41586-024-07487-w)
14. **Wee J, Wei G-W.** Evaluation of AlphaFold 3’s protein–protein complexes for predicting mutation-induced binding free energy changes. *Journal of Chemical Information and Modeling* (2024). DOI: **10.1021/acs.jcim.4c00976**.  
    价值：独立评估显示柔性区域风险、ipTM 漏报大误差；支持本方案的“AF3 + ensemble + 实验”原则。链接：[ACS](https://pubs.acs.org/doi/10.1021/acs.jcim.4c00976)

---

## 七、下一步需要提供的信息

若要把本路线从通用方案变成对 12 条肽的具体研究计划，请补充：

1. 12 条肽的**完整序列、N/C 端修饰、是否环化/脂化**及来源；
2. 已用的 AChE 物种/PDB、对接软件、结合构象、打分和是否有 PAS 残基接触表；
3. 计划使用的 MD 软件/力场、金属模型能力和可获得的实验平台；
4. 研究目标究竟是筛选**促氧化神经毒肽**、**保护性/抑制性肽**，还是同时寻找二者。

拿到这些资料后，下一步应输出：每条肽的配位位点预测、PAS/CAS 构象分类、金属实验浓度矩阵、scrambled/突变对照序列及可直接执行的统计与样本量框架。
