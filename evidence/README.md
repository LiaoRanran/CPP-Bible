# evidence/ — L2 证据库

**与原子的关系**：多对多分离。一条证据可服务多个原子，一个原子引用多条证据。证据独立成文件，才能在证据失效时精确定位受影响的原子集合。

## 证据卡命名

`evidence/{domain}/EV-{DOMAIN}-{NNN}.md`

## kind 枚举

`run`（运行输出）/ `asm`（汇编）/ `layout`（对象布局）/ `abi`（符号与调用约定）/ `symbol` / `bench`（基准）/ `sanitizer`（ASan/UBSan/TSan）/ `godbolt` / `traceable_argument`（不可实证类的可溯源论证）

## 硬要求

1. 每条证据必须写清**可一键复现**的命令与产物路径（`command` + `artifact` + `artifact_sha256`）。
2. 必须写 `expected` 与 `actual` 两栏，并给 `verdict: confirm|refute|partial`。**只写 expected 不写 actual = 伪证据**。
3. 矩阵字段 `matrix: {compiler, std, opt, arch}` 必填——没有矩阵的基准数字不可比。
4. 汇编类证据复用 `tools/verify_asm_evidence.py`（符号级机校，五态：ACCURATE/DRIFT/EMPTY/MISSING_FILE/UNANCHORED）。
5. 不可实证的历史/哲学类走 `traceable_argument`：≥2 个**独立**源 + 时间线 + 权威引用，**禁止硬造实验**。
