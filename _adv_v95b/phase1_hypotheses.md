# 547 Phase 1 · 盲列假设（独立对手，未看实现前的猜测）

> 纪律：本文件是"开工前盲猜"，写于读 `tools/viso_diff.py` / `atom_evidence_replay.py` /
> `mutation_fuzz.py` 之前。跑完探针后由 `REPORT.md` 逐条判定 ESCAPE / BLOCKED / INCONCLUSIVE。

## B · V-iso 阴阳同构（545 未饱和）

- B1 `iso_judge` 绕过：阴面伪装"删 1 行实则改语义"（宏/内联把机制藏进一行删除）⇒ 形态合规但非真阴性。
- B2 翻转造假：阳面断言本身恒真（如 `.file`）⇒ 阴面"翻转"被系统当 negative_control_passed 收下。
- B3 阴面不锚 sha：阴面只差 `.file` 基名，fixture 指向**别卡/别优化级**的产物冒充自己的翻转证据。
- B4 阴面编译失败归类：写坏阴面 ⇒ `refute:negative_control_broken` 不被误算成"翻转成功"；
  yang rc≠0 时阴面判决不被错误豁免。
- B5 YAML flow 走私：`negative_controls` 用 flow 写法 / 缩进提升藏假阴面，绕过 539 硬化。
- B6 nc1 诚实性：阳=2 阴=0 是否真由"删 fence"导致？换 -O2 / 换符号名 / 删无关行，翻转是否仍只对 fence 敏感。

## C · 新旧接缝（549/548/535 的缝）

- C1 548 Part 2 的 `CARD-PATH-NOT-CANONICAL` 是否真在 Windows 触发、且**不误伤**真仓库存量。
- C2 549 的 fast 分支接缝：跳过 replay 后，`CARD-PATH-NOT-CANONICAL` 这种纯门禁规则的 warn 是否仍计入 `new_warn`（不被"没跑 replay"漏掉）。
- C3 mutation_fuzz 的沙箱把 `ge.ATOMS/EVIDENCE` 换成 tmp 副本：`check_card_path_canonical` 读副本还是真仓？
  （若读真仓，则 M2 变异在沙箱副本上、规则却看真仓 ⇒ 漏判 ⇒ 逃逸。）

## D · mutation_fuzz 判决诚实性（**本轮最高优先**，545 未饱和）

- D1 只用"已放行变体"不重算正式 verdict ⇒ 用桩/缓存假装跑过。
- D2 把跨卡规则拆成"卡内"判定（按卡裁剪 diff）⇒ 落在别卡上的命中不算。
- D3 n_a 入账方式：把"改了也没反应"算成"门禁拦了"（escaped 当 blocked 凑率）。
- D4 重载不重置 baseline ⇒ 看不出自己引入的门禁降级。
- D5 只报"新 blocked"不报"门禁降级"（confirm→refute 的回归被静默）。
- D6 隐藏 replay 的 infra_error / 编译失败（不当 n_a，直接丢或当 escaped）。
- D7 只对"会逃逸的卡"跑（selection bias）：`--cards all` 其实漏掉一部分卡。
