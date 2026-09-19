# 536 第五轮独立对抗 · REPORT（assistant 亲自执行，非投喂）

> 执行：本模型（豆包主 agent），对 535 新落地的 L2 队列 + V-iso 信任根做沙箱探针对抗。
> 基线 HEAD≈`ee1d7c8`；探针全部在 `_adv_v90/`，**正式目录零改动**（开工前后 git status 受控区无新增 M）。

## 开头一句话
535 的 touch_set 文件写锁，**核心承诺"两个 worker 不并发改同一文件"在 Windows 上被路径写法完全绕过**——`_conflicts` 只做反斜杠替换，不做大小写/`.` 归一化；我用 4 种写法让 wB 从正在飞的 wA 手里"合法"领到同一个物理文件，4/4 逃逸。这是本批最脆的一环，且是**静默逃逸**（不是报错，是直接发活）。

## 一、实测逃逸（挂可复现证据）

### E1（P0，逃逸）：touch_set 路径归一化缺失 → 派发防撞失效
- 位置：`tools/task_queue.py:377` `_conflicts` 的 `want = {str(t).replace("\\","/") ...}`；`:371` `claimed_touch` 同理。只替换反斜杠，**无大小写、无 `.`/`./` 归一化**。
- 构造：wA 领任务 A，`touch=["tools/task_queue.py"]`（在飞）。再造 4 个独立任务（不同 payload_ref 避免 id 幂等碰撞），分别用不同写法 touch 同一物理文件，让新 worker claim。
- 复现：`.venv\Scripts\python.exe _adv_v90\probe_touch_case.py`
- 实测输出：
  ```
  trial1 'TOOLS/TASK_QUEUE.PY'    -> CLAIMED = 逃逸
  trial2 'Tools/Task_Queue.py'   -> CLAIMED = 逃逸
  trial3 './tools/task_queue.py'  -> CLAIMED = 逃逸
  trial4 'tools/./task_queue.py' -> CLAIMED = 逃逸
  逃逸 4/4
  ```
- 危害：Windows 文件系统大小写不敏感，四种写法指向同一字节。两个 worker 同时领到、同时改同一文件 → 互相覆盖、`_touch_audit` 也救不了（审计完成时文件已是最后一个写者的）。
- **修复建议（给建设者，未替他改）**：touch 归一化改用 `os.path.normcase(PurePath(p).as_posix())`——`normcase` 在 Windows 自动小写化、Linux 原样，正好平台相关，不会误伤 Linux 大小写敏感语义；先 `PurePath` 去掉 `.`/`./`。在 `enqueue` 入库时归一化（而非只在比较时），这样存库值就唯一。
- 附带探针教训（方法学）：本仓 `task_id = hash(type+payload_ref)`，**相同 type+payload 幂等成同一 id**——测多任务必须用不同 payload_ref，否则第二个任务压根不入队，会把"没活"误读成"被挡"。我前两版探针就栽在这。

## 二、代码审计级发现（未跑探针，标【推断级】）

- **I1【推断】**：`_anchor_ok`（`:482`）只 `(root/anchor).is_file()`，**不校验行号、不校验锚点与 claim 的相关性**。这正是 534 开头自陈的"信任继承"元问题的机器面：handoff 的 verified_facts 只要指向一个**存在但无关**的文件即过。属已知设计边界（L1 物证"哈希对≠内容对"），建议在 handoff 报告里把"锚点相关性"显式列为**必人审**项，不要让系统给人"已核验"的错觉。
- **I2【推断】**：`_is_sandbox_path`（`:1040`）只看路径第一段 `fnmatch`。正式目录名若以 `_` 开头理论上可被误豁免——但本仓正式目录（tools/tests/atoms/evidence/Book/Examples/References）无一以下划线开头，**当前安全**，留作硬编码白名单的维护提醒即可。
- **I3【已知边界，不重复报】**：`_authorize` 对 d976170 时代认领、`claimed_token` 为 NULL 的行"只认名字放行"（`:828`）——建设者已在 docstring 诚实标注的降级路径，非新洞。

## 三、守住的（诚实记录，不装都打穿了）
- **takeover 无痕接管被拦**：`--force` 无 `--reason` → rc=2 拒绝（`:726`）；心跳新鲜无 force → rc=2 软拒绝并提示（`:723`）。实测逻辑严密。
- **幂等防重**：同 type+payload 二次 enqueue 返回"已存在"，不重复建任务。
- **touch 审计 fail-closed**：`_touch_audit` 基于 `git status --porcelain -uall` 真实改动，审计跑不出去返回"未观测到"而非当通过（`:1075`）；豁免是白名单不是黑名单。

## 四、饱和声明（诚实）
- **B 面（viso_diff / 阴面 / nc1）本轮未跑编译探针**——需要构造多组 -O0/-O2 对照编译，受本轮上下文与时间限制，只做了代码走读，未证伪也未证实，**不算通过、不算失败**，留待下一轮或苦力回归。
- L2 的 A1 handoff 投毒、A5 yield 父子、A6 WAL 高并发、A7 verify_cmd 自证，本轮未逐一实测探针，基于代码走读无明显破绽，**但不等于安全**——下一轮优先打这四个。

## 五、零污染
开工前存基线：受控区（tools/tests/Examples/atoms/evidence）git status 无新增 M；本轮所有探针与输出在 `_adv_v90/`（`probe_touch_case.py`、`_diag_touch.py`），未改任何正式文件、未 commit、未 push、未 accept。

## 结论
- **严格逃逸 1 个（E1 touch 归一化，P0，4/4 复现）**；其余为代码审计推断或守住。
- 本批建设（535）在 takeover/token/幂等/审计这些"硬边界"上做得扎实；**短板集中在路径归一化这种"每步都对、组合漏一环"的经典缝隙**——与六轮对抗反复出现的模式一致。
- E1 修复小（一处 normcase + 入库归一化），但优先级高：它让并发写锁形同虚设。
