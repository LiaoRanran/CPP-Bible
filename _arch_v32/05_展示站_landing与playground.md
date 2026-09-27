# 方向五 · 展示站：landing、playground 与"硬核验证项目"的大气开场

> 来源 [Sxx] 见 `99_来源清单.md`。
> 回答 brief：大厂范儿怎么做、暗色还是亮色、单页还是多页、playground 怎么设计、硬核验证项目谁做得好。

---

## 1. 2026 一线开发者产品站的实证范式（teardown 共识，非观点）

对 Linear/Vercel/Stripe/Cursor/PostHog/Resend/Anthropic 的拆解给出可直接照搬的规律 S42 S43 S44：

1. **首屏即产品，不是产品的插画**。最高转化率形态是真实 UI（或可交互的产品切片）直接在 fold 以上；CLI/API 产品就放真代码，dashboard 产品就放最有价值瞬间的真实界面。截图要狠裁、字号比生产环境放大 20–40% 保证缩小后可读。S42
2. **开发者工具暗色默认**：Linear/Vercel/Stripe docs/PostHog/Cursor 全部暗色开站，等宽字体+终端美学；亮色是切换项不是默认——"开着暗色像在 IDE 里，开着亮色像在看营销页"。S42
3. **标题 ≤12 个词**，一句话排除掉错误用户、留住正确用户；无空泛"AI 赋能"。S42
4. **性能即设计系统**：Linear/Vercel/Framer Lighthouse 可访问性 90+，组件级强制而非上线前审计。S42
5. **产品本身即营销**（v0/Cursor/Lovable 路线）：可交互 demo 是 2026 的转化增量；Lovable 把"未注册就能在 hero 里用产品"做成激活面。S43
6. 克制也是信任信号：Anthropic 用编辑式排版（衬线大标题、留白、单一强调色、无发光渐变），面向谨慎买家——**这条对"验证/严谨"定位的阙疑尤其重要**：我们要的是 Anthropic 的气质 + Linear 的暗色产品感，而不是 SaaS 模板的霓虹大杂烩。S43
7. 开源快速起站的现实选择：Velora UI（MIT，Next.js16+React19+Tailwind v4+Motion，64 个动画组件+完整多页，每组件标 gzip 体积、守 reduced-motion、0.3–1.5KB 无 Three.js 重载荷）可作为组件库底稿；shadcn/ui + Tailwind v4 是 2026 事实标准底座。S45

## 2. 硬核验证项目怎么展示自己（三个直接对标）

- **seL4**（世界唯一形式化验证微内核）：网站结构是"主张→证明栈→真实部署→生态→基金会"。首页一句话是 *"The world's most highly assured and fastest operating system kernel"*——**敢把最强主张放第一句，然后立刻用证明栈接住**；专门的 Verification 页分层展示 二进制正确→C 语义→功能正确→初始化→安全执行（完整性/机密性/权限）；History 页讲"2009-07-29 最后一个 sorry 清零"的具体故事。白皮书 PDF 一页放信任/不信任组件隔离图。S46
- **Sigstore**：三个动词的极简口号 **"sign. verify. protect."** + 一句 *"Making sure your software is what it claims to be."*；首屏即生态 logo 带；问题—解法三段（短命密钥/透明账本/社区）；大量一手引语与 npm/Homebrew/PyPI/Maven 采用案例。S47
- **Kani Rust Verifier**：把工具的**三态输出直接当 UX 文案**：*"prove the property, disprove it (with a counterexample), or run out of resources"*——证明/反例/资源耗尽。阙疑 pass/block/abstain 四态完全可学这种"诚实地把不确定性写在脸上"的自信。S48

**阙疑首页叙事提案【推断】**（结构，非定稿文案）：

```
首屏（暗色，星图 L0 在背景缓慢生长后冻结）
  主张：每一条 C/C++ 知识断言，都有可复算的证据。
  副题：37 张真机验证卡 · 锁版本编译器 · 变异负测试 · 透明判决账本
  CTA：[ 进入知识星图 ]  [ 在浏览器里试一段 C++ ]
第二屏：信任三段式（Sigstore 式三动词）
  编译 Compile（真编译器真运行）→ 判决 Decide（67 规则+保护器+人审）→ 见证 Witness（哈希链账本，你可亲手验）
第三屏：星图嵌入（可点，不是截图）
第四屏：内存剧场 demo（ch77 一段，可点步阶）
第五屏：验证链展厅入口 + cs 上界仪表盘 + "如何验证我们"三行命令
第六屏：严谨性时间线（seL4 式里程碑：609→627 diff=0、648 120 组 0 失败、M1–M7 全 blocked）
末屏：MIT 开源、queyi-core 仓库、uvx 一键安装、giscus 讨论
```

没有客户 logo 墙就**坚决不放**（空 logo 带比没有更伤信任 S42）；用真实工件截图与可交互组件代替证言。

## 3. 单页 vs 多页 / 暗色 vs 亮色

- **结构**：营销+产品入口用**少量 MPA 静态页**（landing/星图/剧场/展厅/文档），每页一个主任务；交互内部（星图内节点切换、列表→详情）用 View Transitions 做 SPA 感过渡 S40。理由：MPA 静态站秒开、可 SEO、零路由运行时、契合纯静态零后端纪律；不要为了"应用感"上重 SPA。
- **主题**：暗色默认（开发者受众实证 S42），提供亮色切换（`light-dark()` 2026 已原生支持图片值 S41）；三档强调色要克制——语义色固定（通过青/拒绝红/挂起琥珀/推断紫，全站与 01 号编码一致）。
- 文档层（147 章书站）维持 v31 决策：MkDocs Material 冻结到 2026-11，新交互层在独立 Astro/Starlight 站——本报告全部视觉资产都落在新站 `quyi-lab`，书站不动。

## 4. Interactive Playground 的设计要点

- **打开即有正确代码**：预置 ch77/ch107/648 十卡等已验证片段，第一屏不需用户输入就能按"运行"看效果（v0/Lovable 共同经验：产品先动起来 S43）；
- **左代码右舞台**（02 号报告三区），运行按钮 <300ms 给反馈（wasm 本地无网络往返），耗时步阶显示进度；
- 每个预置片段底部两条链接："这只是教学模拟 → 看真机证据（证书页）"——**playground 同时是信任漏斗**：玩得爽的人被自然引导进验证链展厅；
- 移动端不塞完整 playground：给"精选 30 秒回放"（只读 trace 动画），编辑只在桌面/宽屏开放。

## 5. 性能与"秒开"的工程清单（全站统一预算）

| 项 | 预算 | 手段 |
|---|---|---|
| LCP（中端移动） | <2.0s（hero 星图页 <2.5s） | 静态页、首屏 JS <80KB gz（不含 wasm）、字体 subset+display=swap、星图二进制 <50KB |
| wasm 工具链 | 首屏不载 | browsercc（clang 43MB/sysroot 29MB 等 S，见 v31）按路由+用户点"运行"后才加载，长缓存 |
| 帧率 | 交互 60fps | transform/opacity、InstancedMesh、物理冻结、dpr≤2、按需渲染（01/04 已述） |
| 动画资产 | 单页 Rive/Lottie 总重 <50KB | Rive 优先 S36 |
| 可访问性 | Lighthouse a11y ≥90 | reduced-motion/键盘/焦点/色冗余，CI 卡阈值 S42 |
| 后端 | v1 零后端 | 全站静态 + giscus + Pagefind + 本地进度（v31 决策不变） |

## 6. 通用化落地：Verdict Atlas 套件

把三个炫酷组件做成与业务解耦的开源套件（独立 MIT 仓库，npm 分发，Astro/React/无框架三入口）：

| 包 | 消费的 schema | 对应报告 |
|---|---|---|
| `@quyi/atlas-graph` | graph-bundle v1（节点状态/边类型/轮次） | 01 |
| `@quyi/memory-stage` | trace-events v1（帧/分配/读写/违例） | 02 |
| `@quyi/cert-view` | verifiable-claim v1（指纹/验证链/变异测试/上界） | 03 |
| 共享 | 动效 token、状态色、声音/触觉 hooks | 04 |

阙疑仓库只写**适配器**（Python 构建期把台账/PCK/trace 导成三份 schema，锁哈希进 CI）。这样"通用化"不是口号：渲染器零业务知识，任何验证/知识项目可接入；且构建产物可机检，延续项目宪法。

## 7. 分阶段（与 v31 路线图对齐，串行小批量）

- **P0（1–2 周，出"哇"）**：切片 01-A（星图 hero 静态页）+ 03-A（证书现场验哈希）+ 暗色 landing 骨架（Velora/shadcn 底稿裁剪，不整站搬）。这三样放出来已经是"不是小作坊"。
- **P1**：内存剧场 pilot（ch77）+ 声音触觉开关 + View Transitions。
- **P2**：击败边时间轴、判决检索台、真机 trace 三例、playground 预置库。
- **P3**：三组件 schema 定稿、独立仓库与 npm 发布、适配器进 CI、Lighthouse 门禁。

## 8. 不做清单

- 不做全屏 WebGL 氛围粒子/ shader 背景（性能黑洞，且与"严谨"气质冲突——Anthropic 路线 S43）；
- 不做无客户的 logo 墙、不写"业界领先"式空话（seL4 的主张必须有证明栈接住 S46）；
- 不做重 SPA/账号体系/评论自建（v31 已定）；
- 不把证书叫"区块链/NFT"，账本就是账本（克制即可信）；
- 不在移动端塞编辑器、不在首屏载 wasm。
