# 方向130：WebAssembly应用——从浏览器到边缘：一次编译，处处确定执行

## 核心结论

1. **WASM 是第一个真正由多方共建、有 W3C 正式标准的可移植编译目标，其诞生是两条失败路线的合流**。Google Native Client（NaCl/PNaCl）安全但不可移植、只能消息通信；Mozilla 的 asm.js（2013-03，Luke Wagner、Alon Zakai、Dave Herman 等）可移植但只是 JS 子集、性能受限[1]。2015-04 Luke Wagner 建立 WebAssembly/design 仓库；2017-02-28 四大浏览器厂商联合宣布 MVP（Chrome、Firefox、Safari、Edge 同年全部出货）；W3C 核心规范于 2019-12-05 成为正式推荐标准[2][3]。WASM 不是语言，而是**为编译器设计的二进制指令格式与栈式虚拟机**。

2. **性能必须按场景精确表述，不能笼统说"接近原生"**。WASM 引入论文（Haas 等，PLDI 2017，《Bringing the Web up to Speed with WebAssembly》）报告：Chrome 上 WASM 比 asm.js 快 34%；24 个 PolyBenchC 小内核中 7 个在原生 10% 以内、几乎全部慢于原生不超过 2 倍[4]。大规模实测（Jangda 等，USENIX ATC 2019，《Not So Fast》）给出更冷静的数字：SPEC CPU 上 WASM 平均慢 45%（Firefox）到 55%（Chrome），峰值慢 2.08 倍/2.5 倍[5]。因此严谨表述是：**计算密集型内核通常约原生 1.1–2 倍，完整大型应用平均开销约 45–55%，但远快于 JS/asm.js**。

3. **WASM 的杀手特性不是性能而是"确定性+能力安全+跨平台"**：WASI（系统接口，capability 导向）、V8/wasmtime/WAMR 三类运行时、Fastly/Cloudflare/Envoy/区块链等生产场景已验证其价值[6][7][8]。SIMD 提案 2021 年随浏览器默认开启，GC 提案 2023 年随 V8 11.4/Chrome 114 默认开启[3]。对阙疑，这是把判决引擎变成"可在浏览器里点击重放"的最便宜路径。

---

## 技术全景与关键数字

### 一、从 asm.js 到 W3C 标准：时间线

- 2013-03：asm.js 发布，定义带隐式静态类型信息的 JS 子集，配合 Emscripten（Alon Zakai）把 C/C++ 编译进浏览器[1]；
- 2015-04：WebAssembly/design 首批提交；W3C 社区组成立于 2015 年[3]；
- 2017-02-28：跨浏览器 MVP 共识发布，MVP 仅 4 种值类型（i32/i64/f32/f64），同年 4 浏览器出货[2][3]；
- 2019-12-05：W3C 推荐标准（Core 1.0），W3C 称之为"继 HTML/CSS/JS 之后第四种 Web 语言"[2][3]；2021 年获 ACM SIGPLAN 编程语言软件奖。标准化路径的价值在事后看格外清楚：正因有统一规范，同一份字节码可在浏览器、服务器与嵌入式三类运行时之间流动，生态不必绑定任何单一厂商，这也是它区别于 ActiveX、Flash 等封闭前身的根本之处。

### 二、WASI：把能力模型带进系统接口

WASI 为浏览器外运行提供系统接口，核心安全原则是**无默认权限**：程序不能直接 open 任意路径，宿主以能力（预打开目录、句柄）显式授予；网络同样需显式注入[6]。WASI 0.1（preview 1）基于类 POSIX 调用；preview 2 转向 Component Model，WASI 0.3 于 2026-06 投票通过、原生异步化。Component Model 提供跨语言组件接口与虚拟化原语，被定位为"安全的软件组合基础"。

### 三、三类运行时：V8、wasmtime、WAMR

V8（Google）采用分层编译：先用 Liftoff（2018 年引入）快速生成基线代码，使大型模块秒开，热点函数再由 TurboFan 优化重编译；模块支持流式编译与边下载边验证，浏览器不必等全部字节到达才启动。V8 同时支持浏览器与 Node；wasmtime（Bytecode Alliance，Cranelift 代码生成，Rust）面向服务器的独立运行时，可 AOT/JIT，WASM GC 与异常在 2026 年的 wasmtime 47 默认开启[7]；WAMR（WebAssembly Micro Runtime，源自 Intel，2019 年随联盟发布）面向嵌入式设备，支持解释器、AOT、极小内存占用，可在无 MMU 环境运行[8]。2019-11-12 Bytecode Alliance 由 Mozilla、Fastly、Intel、Red Hat 创立，同时贡献 wasmtime、Lucet、WAMR[7]。北大综述（arXiv:2404.12621）覆盖 98 篇运行时研究[9]。

### 四、SIMD、GC 与提案进程

WASM 提案沿用类 TC39 阶段制。Post-MVP 已落地：可变全局导入导出、非陷入 float→int、符号扩展、BigInt/i64 互操作、Reference Types、Bulk Memory、Fixed-width SIMD（2018–2021，2021 年主流浏览器默认）[3]；GC 提案经数年迭代，2023 年 V8 11.4/Chrome 114 默认开启，使 Java/Kotlin/Dart 等托管语言可直接以 WASM 为目标而无需自带 GC[3]。线程（SharedArrayBuffer）、异常处理、尾调用等陆续推进。

### 五、生产场景：边缘、代理与区块链

- **Fastly**：Lucet（AOT 编译器/运行时，2019）支撑 Compute@Edge（2019 公测、2020-06 GA，现 Fastly Compute），为每个请求实例化 WASM 模块[10]；
- **Cloudflare Workers**：2017-09 推出，多租户边缘函数运行在 V8 isolate 上，冷启动毫秒级[11]；
- **Envoy/Proxy-Wasm**：2020 年起代理以 WASM 承载过滤器/插件，Istio 采用，插件可用多语言编写并动态加载[12]；
- **区块链**：Polkadot/Substrate、Cosmos、NEAR、DFINITY、EOS 等用 WASM 作为确定性链上执行格式（以太坊 eWASM 路线后被 EOF 等方向取代，未按原计划落地）[9]；
- **Shopify**：2022 年推出 Shopify Functions，让商家/开发者用 WASM 编写后端定制逻辑（折扣、配送、支付校验），平台在多租户环境中安全执行，是电商侧能力化插件的代表；
- Web 应用：Google Earth、Adobe Photoshop（web beta 2021）、AutoCAD Web、Figma（早期 asm.js 后转 WASM）、Unity 导出。

### 六、确定性与沙箱边界

WASM 语义刻意做了浮点可控（可配置 NaN 行为）、无隐式系统调用、执行结果仅取决于模块与输入，天然适合**确定性重放**。确定性还体现在浮点细节：WASM 规定了确定的舍入与运算顺序，NaN 载荷策略可配置，避免了 C++ 原生浮点在不同编译器优化下重排的问题。沙箱由线性内存（访问带边界检查）+ 模块验证（类型/栈/控制流校验）+ 显式导入构成，模块无法跳到线性内存中执行指令，也无法接触未导入的宿主函数。但风险并未归零：JIT 本身的 bug、Spectre 类侧信道、运行时实现缺陷——Patrick Ventuzelo 在 Black Hat USA 2022 演示模糊测试 WASM VM，仅 wasmtime 校验路径即发现约 6 个缺陷[13]。

---

## 对阙疑的映射

### 一、把规则/判决引擎编译为 WASM：跨平台确定性重放

阙疑的 452 条账本、67 条规则、9 个保护器本质是"输入 AST 片段 → 结构化判决（四态）"的纯函数集，天然是 WASM 化的候选。具体路径：把不依赖编译器调用的规则子集（纯 AST/模式匹配部分）用 C++ 或 Rust 重写为无操作系统依赖的库，编译成单一 `quevi_rules.wasm`；账本重放器提供确定性导入（只给日志/哈希等纯函数），执行结果（判决、Merkle 中间哈希）逐位确定。这直接回应可复现性的最严档诉求：**任何机器、任何年份，同一份 .wasm 对同一份账本输出相同字节**——比 Docker 复现更轻（无需内核、无需镜像），审稿人只需 wasmtime 即可独立对账。变异 core 97.3%/all 81.5% 这类数字未来可同时提供"原生结果"与"WASM 重放结果"双份证据，证明结论不依赖执行平台。落地时建议分三步走：先把 AST 访问层定义成稳定的 C 接口（与方向 127 的 ABI 工作共用），再把规则主体改成无全局状态的纯函数（全局状态是确定性重放最大的暗礁），最后在 CI 中加入"原生/WASM 双跑逐位比对"一步，任何不一致都当失败处理。账本中的时间戳、随机数等非确定输入一律改为由导入函数按固定种子供给，使重放结果与运行环境彻底解耦。

### 二、浏览器端可交互 demo：对论文曝光与拿 star 的杠杆

双非本科、合肥、嵌入式、0 影响力起步，NeurIPS 2027 E&D 的可执行开放不仅是合规要求，也是唯一能绕过身份信号的传播通道。做一个静态网页 demo（无需后端、GitHub Pages 可托管）：左侧列出 37 张实卡与 holdout 30 条案例，用户点击任一案例，浏览器内 WASM 模块即时跑规则并高亮判决路径（哪些规则触发、保护器如何介入、四态如何合成），并展示账本哈希。对论文的价值具体且可核实：(i) 审稿人 desk review 阶段 30 秒看到系统真实运行，显著降低"代码跑不起来"的拒稿风险；(ii) 可交互 demo 是技术社区自传播的标准载体，对 GitHub star 与 E&D 赛道"生态与采用"评价有直接帮助；(iii) 演示不暴露原始评测工具链，无安全顾虑。这比写十段 system overview 都有效。实现上 demo 应刻意保持零后端：37 实卡的源码片段、预计算的 AST 与判决路径以紧凑 JSON 打包随静态资源分发，WASM 模块只负责重跑规则与合成四态；用户看到的每一帧计算都发生在自己浏览器里，复现者由此直观验证"系统没有在服务器端偷偷调模型"。页面还可提供一个"换一个编译选项试试"的小交互，让访客亲手改变输入并观察判决翻转——这正好把方向文档中"判决对环境敏感"的论述变成可触摸的体验。

### 三、WASM 作为不可信探针沙箱

承接方向 127/128：第三方提交的规则可要求以 WASM 形式交付而非原生代码。WASM 模块无法直接访问文件系统、进程或宿主内存（只能访问自己的线性内存），内核经导入函数提供 AST 读取与判决写入——恶意规则被天然限制在沙箱内，崩溃只产生 trap、由内核捕获记为 UNKNOWN。配合资源计量（执行指令数/fuel、内存上限），还能防死循环。这比为每个规则开子进程或 microVM 便宜得多：实例化在微秒至毫秒级、内存开销极低，单机可同时加载数十个规则模块。需要诚实承认的边界：JIT 型运行时的安全保证弱于纯 AOT，高安全场景应配 AOT/纯解释模式并及时升级运行时。工程上还可借 Component Model 把规则接口固化为带类型的世界（world）定义：内核提供的导入集合与规则必须实现的导出都写进接口契约，模块版本随契约版本走，未来新增规则能力只需定义新世界而不破坏旧模块——这套做法与方向 127 的 ABI 冻结纪律完全同构，差别只在边界两侧的承载物从原生机器码换成了字节码。

### 四、WASI 能力安全：复现包的最小授权

若提供独立 WASM 复算器，经 WASI 运行时以最小能力启动：只预打开账本目录（只读）、输出目录（只写）、不授网络、加 `--dir` 白名单与 fuel 上限。复现者可审计命令行中授予的全部能力——这比"运行一个来路不明的二进制"心理门槛低一个量级。运行时选型同样可按信任需求分层：CI 对账用 AOT 模式的 wasmtime（无 JIT、无即时生成代码），浏览器交互用内置 JIT 的 V8，嵌入式验证用 WAMR 的解释器；同一份模块在三种运行时下给出同一判决，本身就是"系统不依赖特定实现"的有力佐证。能力声明本身可写进论文复现章节，成为 E&D 系统设计的加分项。

### 五、现实节奏与嵌入式背景的复用

WAMR 的存在使同一套规则 .wasm 未来可下沉到嵌入式目标（作者的本职领域）——例如在资源受限设备上做静态检查探针，这给论文"领域外延"提供自然的 future work，也让作者背景从劣势变成合理的故事线。但优先级必须排清：WASM 化是论文冻结后的增强项，不能干扰 2027 年投稿前 holdout/corpus/变异/反事实四组核心数字的稳定。还要划清一条能力边界：WASM 版规则只覆盖"纯 AST 分析"路径，凡需调用真实编译器或 sanitizer 的实卡，浏览器内只能展示流程、无法在端内产出判决，页面必须如实标注，不能用预录结果冒充实时执行——一旦被复现者发现"演示造假"，对 0 影响力作者的信誉伤害远大于没有 demo。

---

## 对阙疑的三条具体行动

1. **完成纯 AST 规则子集的 WASM 编译验证（2027-02 前）**：选定不依赖外部编译的规则子集，编译为 `quevi_rules.wasm`，用 wasmtime 以无网络、最小 WASI 能力重放 452 账本，比对判决与 Merkle 根和原生结果逐位一致；不一致的规则记录原因（如依赖非确定行为）并在盲区列出。
2. **上线浏览器交互 demo（2027-05 前，投稿前）**：静态站点内嵌 WASM 模块，覆盖 37 实卡与 holdout/corpus 案例的判决路径可视化；在论文匿名仓库首页与 README 给出 demo 链接；同步挂 GitHub Pages，观察并记录 star/访问量作为影响力证据。
3. **把 WASM 定为第三方规则的强制交付格式与沙箱（2027-03 前随插件 ABI 一起冻结）**：在插件规范中增加"规则可提交 .wasm"路径，内核侧用 AOT 模式加载、默认零导入能力、加 fuel 与内存上限，trap 记 UNKNOWN；在 threat model 中对比子进程/microVM/WASM 三档隔离成本。

---

## 盲区

- "1.1–2 倍原生"仅适用于计算密集型小内核，ATC 2019 的 SPEC 大型应用均值是 45–55%，两者不可混用；具体到阙疑规则负载的性能未实测。
- WASI 0.3/Component Model 生态（语言绑定、运行时支持）截至 2026-09 仍在快速变动，长期 API 稳定性未经验证；本文不保证 preview 接口向前兼容。
- GC/SIMD 在各浏览器与 Firefox/Safari 的具体默认开启版本号可能有一个版本内的偏差，Chrome 114 口径外未逐一核对。
- 区块链 eWASM 的实际废弃时点与替代方案（EOF）进展以二手综述为主，未读以太坊核心仓库一手提案。
- WASM 沙箱对 Spectre 类侧信道的防护取决于浏览器站点隔离与内核缓解配置，单机/CI 场景的残余风险未量化。
- 浏览器 demo 能承载的规则复杂度有上限：需要真实编译器的实卡无法在浏览器内完整复现，需明确标注"演示用子集"。

---

## 来源

1. Bytecode Alliance, "10 Years of Wasm: A Retrospective" — https://bytecodealliance.org/articles/ten-years-of-webassembly-a-retrospective — asm.js 2013-03、NaCl/PNaCl、2015 design 仓库 — 2026-01
2. W3C, "WebAssembly Core Specification"（Recommendation, 5 December 2019）— https://www.w3.org/TR/wasm-core-1/
3. W3C, 新闻稿 "WebAssembly becomes a W3C Recommendation" 与 TPAC 2021 更新 — https://www.w3.org/press-releases/2019/wasm/ ；https://www.w3.org/2021/10/TPAC/demos/web-assembly.html — 时间线、Post-MVP 提案、SIMD
4. Haas et al., "Bringing the Web up to Speed with WebAssembly", PLDI 2017 — https://dl.acm.org/doi/10.1145/3062341.3062363 — 较 asm.js 快 34%、7/24 在原生 10% 内
5. Jangda et al., "Not So Fast: Analyzing the Performance of WebAssembly vs. Native Code", USENIX ATC 2019 — https://www.usenix.org/conference/atc19/presentation/jangda — SPEC 平均慢 45%/55%、峰值 2.08x/2.5x
6. WASI 官方站点与规范 — https://wasi.dev/ — 能力导向系统接口、preview 版本
7. Mozilla Hacks, "Announcing the Bytecode Alliance" — https://hacks.mozilla.org/2019/11/announcing-the-bytecode-alliance/ — 2019-11-12 成立、wasmtime/Lucet/WAMR、Cranelift
8. WAMR 项目仓库（嵌入式运行时，源自 Intel）— https://github.com/bytecodealliance/wasm-micro-runtime
9. Zhang et al., "Research on WebAssembly Runtimes: A Survey" — https://arxiv.org/abs/2404.12621 — 98 篇论文、区块链与沙箱场景综述 — 北京大学，2024
10. Fastly, "Announcing Lucet" 与 Compute 平台 — https://www.fastly.com/blog/announcing-lucet-fastly-native-webassembly-compiler-runtime
11. Cloudflare, "Introducing Cloudflare Workers" — https://blog.cloudflare.com/announcing-cloudflare-workers-the-platform-for-building-a-new-serverless-cloud/ — 2017-09
12. Envoy 官方文档，"Extending Envoy with WebAssembly" — https://www.envoyproxy.io/docs/envoy/latest/start/wasm
13. Ventuzelo, "A Journey Into Fuzzing WebAssembly Virtual Machines", Black Hat USA 2022 — https://i.blackhat.com/USA-22/Wednesday/US-22-Ventuzelo-A-Journey-Into-Fuzzing-WebAssembly-Virtual-Machines.pdf
