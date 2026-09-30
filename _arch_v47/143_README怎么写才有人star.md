# 方向143：README怎么写才有人star——首屏工程与学术仓库的合规骨架

## 一、README只有两个任务：30秒定位与3分钟建立信任

README不是项目说明书，而是一个转化页面。它的任务只有两个：第一，让访客在打开页面的30秒内（不需要滚动或只需极少滚动）回答「这是什么、解决什么问题、我为什么要继续看」；第二，让有兴趣的访客在3分钟内通过demo、数字、对比和文档入口建立「这个作者可信、这个项目可用」的判断。完成这两个任务之后，star、issue、clone才可能发生。

报刊术语「above the fold（首屏/折痕之上）」在这里完全适用：访客到达时未滚动就看到的区域，是转化漏斗的最窄处。学术项目的README最常见、也最致命的错误，正是把首屏让给长篇理念陈述——三屏「为什么这个方向很重要」之后才出现安装方法，此时95%的访客已经离开。阙疑作为一个以「可审计AI」为旗帜的项目，README必须反其道而行：首屏直接给出一句话定位、一张demo图、一组可核对的硬数字。

## 二、高star项目README的标准结构（按出现顺序）

综合starship（约4.7万star）、bun（9万以上）、deno（约10.7万）、astro（约5.52万）等项目的实践，一个完整README按顺序包含以下要素，并非每个都必需，但顺序逻辑不应打乱：

1. **徽章（badges）**：CI状态、版本、license、下载量、社区频道。徽章的真实功能是用最小面积传递「项目是活的、有工程纪律」，但一排超过八个就成为噪音；学术项目可加「论文/预印本」「数据集DOI」徽章。
2. **一句话定位（tagline）**：在标题正下方用一句话说明它是什么、为谁解决什么。检验标准：脱离任何上下文，这句话能否被独立引用到Hacker News标题。
3. **gif/截图demo**：首屏核心资产。CLI工具用终端录屏（asciinema或30秒gif），服务类用界面截图，最好配一段「你看到的是什么」的图注。录屏制作有几条被反复验证的细节：先写脚本再录制，30秒内必须出现最有冲击力的结果画面，去掉无关的等待与打字过程；终端字号放大、配色统一，确保在移动端缩略图上仍能辨认关键输出；gif文件体积控制在数兆以内，过大的首屏资源会拖慢页面、直接恶化到达率。图片应使用仓库内相对路径而非外链图床，避免第三方失效导致首屏裂图。
4. **核心特性列表**：3—6条，每条一个具体卖点，能给数字就给数字，禁止「强大」「智能」「现代化」这类空形容词。
5. **安装（installation）**：一行命令优先；列清平台与依赖前提；给出验证安装成功的命令。
6. **快速开始（quickstart）**：从安装完成到跑出第一个结果不超过五步、不超过五分钟；代码块可整段复制。
7. **文档入口（documentation）**：链接到完整文档、教程、API参考；README自身不承载全部文档。
8. **对比表（comparison）**：与2—4个主流替代方案在具体维度上对比。这是技术读者最重视的部分，也是最容易翻车的部分——所有数字必须可复现、注明实验条件，否则会被评论区逐条拷问。
9. **FAQ**：预判五个最尖锐问题（包括局限与失败场景），主动作答。FAQ的写作顺序应当「反过来」：先收集发布前内测者和评审中最不留情面的质疑，再逐条改写为问答，而不是作者自问自答。每条回答保持三行以内，先给结论再给依据；答不上来的问题直接写「尚未解决、计划如何验证」，坦诚的未知比圆滑的空话更经得起技术读者推敲。
10. **贡献指南（contributing）**：如何提issue、如何发PR、行为准则链接。
11. **许可证（license）**：明确协议；学术项目在此处或单独段落说明数据与代码的授权差异。
12. **引用（citation）**：给出CITATION.cff或BibTeX入口（见第四节）。

维护层面还有一条贯穿性原则：**README是索引，不是唯一事实源**。安装命令、数字结论、实验结果都应从脚本或文档中生成或核对，README只引用不手工誊抄，否则多处手抄很快漂移。建议把README的每一次修改纳入与代码同等的review要求：数字变更必须附对应实验commit，截图更新必须注明版本号，特性增减必须与release notes一致。一个细节可以检查项目纪律——README中是否残留过期数字（如旧的star数、旧版本号），访客会据此推断整个仓库的严谨程度。

## 三、四个优秀案例的可迁移之处

**bun：首屏即数字。** 其README与发布叙事一脉相承：all-in-one定位紧跟速度对比（相对esbuild/swc/babel的具体倍数），首屏内就给访客「为什么值得停下来看」的理由[1]。发布首周2万star的转化，首屏结构功不可没。

**deno：安全模型可视化。** 把「默认安全、权限显式授予」这一最反直觉的差异点用最短示例代码直接演示，访客无需读完设计文档就能理解取舍。

**starship：安装一行、效果一张图。** 作为跨shell提示符工具，README首屏直接给出多shell统一安装命令和效果截图，特性部分用图标化短列表降低阅读成本[2]。

**astro：把架构创新讲成一句话。** 「岛屿架构（island architecture）、默认零JS」是一句话定位的范本；README与官网、年度总结保持同一叙事，2025年初破5万star、年底约55200，而当时GitHub全平台超过5.5万star的仓库仅约295个[3]。

共同规律有三条：首屏从不让位给背景介绍；每个卖点尽量落到可核对的数字或示例；视觉元素（截图、徽章、图标排版）承担信息功能而非装饰功能。

## 四、学术仓库的特殊组件：CITATION.cff与双语取舍

**CITATION.cff是学术仓库最重要的「隐形加分项」。** 它是放在仓库根目录的纯文本YAML文件，提供人和机器都可读的引用元数据，当前规范版本为1.2.0[4]。GitHub官方文档明确：当CITATION.cff存在于默认分支时，仓库首页右侧栏自动出现「Cite this repository」入口，可直接导出APA和BibTeX格式；文件中可包含作者（含ORCID）、标题、版本、DOI、发布日期、仓库URL等字段[4]。更关键的机制是`preferred-citation`覆盖：软件本身之外，可指定一篇期刊/会议论文（conference-paper）或一个数据集（data）作为首选引用对象[4]。这意味着阙疑可以做到「仓库归仓库、论文归论文」——引用者一键拿到的是你希望被引用的那篇论文，而不是笼统的软件地址。

**与Zenodo的联动形成完整引用闭环。** Zenodo与GitHub的集成会在发布release时自动从CITATION.cff读取作者、标题、版本信息，生成带DOI（10.5281/zenodo.*形式）的可引用软件记录[4]。配套工具链成熟：cffinit提供网页表单式生成，cffconvert支持BibTeX/RIS/CodeMeta等格式互转，cff-validator可作为CI中的GitHub Action做校验[5]。一个有DOI、有一键引用、有论文preferred-citation的仓库，在grant评审与申研委员会眼中的专业度与普通仓库有量级差别。

**中英双语取舍：不要做全文双语。** 维护两份完整README的长期成本极高，且两份文档很快会版本漂移。务实做法是：主README英文（面向HN/Reddit/审稿与国际社区），中文内容以独立文件（如README.zh.md）承载并在顶部注明「以英文版为准、中文版可能滞后」，首屏放语言切换链接；核心数字、命令、表格在两个版本中必须完全一致。若精力只够一份，选英文——NeurIPS、grant评审与潜在合作者的工作语言都是英文。

**常见错误清单：** 长篇理念无demo（首屏三屏背景）；特性全是空形容词；对比表数字无出处；quickstart假设读者已装好复杂环境；README写死大量本应在文档里的细节导致维护失控；安装命令在Windows直接失败却只写类Unix路径；license缺失或与数据授权混用；匿名期README残留作者个人站链接导致破盲。

## 五、阙疑README骨架：正式版与匿名合规版

**正式版骨架（双盲解除后启用），首屏顺序如下：**

- 标题下方一句话定位：「Auditable C++ knowledge verification: four-state verdicts backed by an append-only ledger.」
- 徽章行：CI、license、数据集DOI（Zenodo）、论文/预印本链接。
- 30秒终端录屏：对一段C++代码从扫描到四态判决、写入账本的完整过程。
- **「At a glance」数字条（首屏内）**：37 real-world cards · 67 rules · 9 protectors · 452 ledger entries · 3826 LoC kernel。全部是可在仓库内核验的硬数字。
- 特性区（每条带证据）：四态判决（格论偏序支撑，另见方法论文档）；append-only账本可逐条审计；holdout 30条（17真错）检出率66.7%，给Clopper-Pearson区间；corpus 40条检出率43.8%并附「算术不自洽」诚实分析入口；变异测试core 97.3%/all 81.5%，注明两集合口径；反事实修复P=R=F1=0，明确标注为开放问题而非功能。
- 安装一行命令＋quickstart五步以内跑出第一张卡的判决。
- **学术仓库特有段落**：「Datasets & ledger」入口（37实卡与452条账本的获取方式、字段schema、授权条款）；「Reproducibility」入口（复现holdout/corpus/变异三组实验的脚本、环境锁定方法、预期输出与容差）；「Methodology notes」入口（架构调研文档索引）。
- 对比表：与编译器警告、静态分析器、LLM直接问答在「可审计性/证据留存/判决粒度」三维度对比，所有数字注明实验日期与条件。
- FAQ预置尖锐问题：「43.8%为何这么低」「P=R=F1为何还公开」「30条holdout样本是否过小」。
- CITATION.cff就位，preferred-citation指向方法论论文；contributing、license、引用块收尾。

**匿名期合规版（投稿评审期间使用）：** 结构与正式版完全一致（一致性本身也是评审可复现性的一部分），但做四处处理：作者字段写匿名研究组占位，移除个人站/邮箱/资助致谢等一切身份线索；CITATION.cff暂不放入或使用匿名占位（避免Zenodo DOI暴露真实姓名）；commit历史做匿名化处理；数字、demo、复现入口一个不少——双盲只隐匿身份，不隐匿证据。评审义务解除当天，用预先备好的正式版整体替换并启用真实CITATION.cff与DOI，与传播脉冲同步（见方向142）。

数字更新还需一个明确策略，避免README与真实账本脱节。建议采用「版本注记」式管理：核心规模数字（实卡数、账本条数、内核行数）随每个release更新，在数字旁标注对应版本与日期；论文结论类数字（66.7%、43.8%、97.3%、81.5%）锁定为「某次冻结实验的历史结果」，后续重跑若产生新值，以新增段落报告而非覆盖旧值——审稿人和引用者看到的必须始终是他们引用时的那个数字。反事实P=R=F1=0这一条尤其要保持口径稳定：它从「现状」变为「已修复」时，需同时留下修复前后两段记录，而不是悄悄抹去零结果历史。

衡量README是否达标的标准不是「写得全」，而是：陌生访客首屏30秒能否复述项目是什么；评审者3分钟内能否找到复现入口；引用者能否一键导出正确的BibTeX。三个问题都为「是」，star与信任只是顺带结果。

---

### 对阙疑的三条具体行动

1. **2026年12月底前**：按上述骨架完成README正式版初稿，首屏必须在30秒内出现demo与37/67/9/452/3826五个数字，并完成终端录屏gif。
2. **2027年3月投稿同期**：生成匿名合规版（移除身份线索、暂挂CITATION与DOI），保证证据与数字不减项；同时用cffinit预生成正式CITATION.cff备而不发。
3. **双盲解除当天**：替换正式版、启用Zenodo DOI与preferred-citation、同步README.zh.md，且中英两版核心数字逐字核对一致。

### 盲区

1. 优秀案例（bun/deno/starship/astro）均为成熟团队或商业公司支持的项目，其README的打磨工时对独立学生而言可能无法复制，骨架可学、完成度难追。
2. 首屏放大量硬数字存在反噬风险：数字若在后续实验中变化（如账本从452条增加），README与历史截图的口径管理会成为长期负担。
3. CITATION.cff与Zenodo流程对release节奏有隐性要求，频繁更新会产生大量DOI版本，引用者可能引用到旧版本。
4. 匿名期README与commit历史的彻底匿名化在技术上并不简单，git元数据、协作者ID、issue回复都可能成为破盲通道。
5. 「英文版为准」策略下，中文读者（可能是大创评审与国内导师）的理解损耗没有评估。
6. 对比表最容易引发争议甚至原作者抗议，独立项目公开批评主流工具的社区政治成本在文中无法充分量化。

### 来源：

1. Bun发布叙事与首屏数字（首周2万star、对比倍数）：https://bun.com/blog/bun-joins-anthropic
2. starship项目与star量级（约4.7万）：https://web3.career/learn-web3/top-rust-open-source-projects
3. Astro 2025年度总结（5.52万star、全网295仓库超5.5万）：https://astro.build/blog/year-in-review-2025/
4. GitHub官方文档《About CITATION files》（1.2.0、Cite this repository、APA/BibTeX导出、preferred-citation、Zenodo DOI）：https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
5. CITATION.cff生态（cffinit/cffconvert/cff-validator、Zenodo集成机制）：http://raw.githubusercontent.com/api-evangelist/citation-cff/refs/heads/main/apis.yml
6. CFF核心规范1.0.0 PDF（YAML 1.2、字段定义）：https://zenodo.org/records/1108269/files/cff-specifications-1.0.0.pdf
7. Bun vs Deno 2026数据（star量级对照）：https://solodevstack.com/blog/bun-vs-deno-solo-developers
8. 2025年8月GitHub仓库star快照（头部项目参照）：https://repositorystats.com/backintime/2025-08
9. fzf项目README特征（单二进制、shell集成、demo）：https://vim.hizdm.cn/integration/fzf.html
10. Citation File Format官方站（规范、cffinit入口、文档与工具索引）：https://citation-file-format.github.io/
