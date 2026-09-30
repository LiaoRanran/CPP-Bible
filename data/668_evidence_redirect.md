# 668 · 证据卡命令写法修复（shell 重定向 → 运行器捕获）

> 由 `python tools/evidence_cmd_redirect_668.py --report` 生成，**禁止手改**。

待修（`--check` 时）：**0** 处 / 共 67 张证据卡。

## 口径（为什么删而不是让运行器支持 `>`）

`atom_evidence_replay.py` **拒绝**含管道/重定向/通配/变量的命令（`refute:unsupported_shell`，rc=127）。
运行器本身就会捕获子进程 stdout 并与卡里的 `expected.run` / `run_match_file` 比对，
所以 shell 重定向是**冗余**的一截；删掉它 ⇒ 命令可跑、语义不变。
另一条路（放开 `>`）等于给只读门禁开一个 shell 解析口，安全代价不划算 ⇒ **不选**。

## 逐条

| 卡 | 行 | 改前 | 改后 |
|---|---:|---|---|

## 边界

- 只动 `command:` 块里形如 `<exe> > <file>` 的行；`fixture` / `artifact_sha256` / `expected` / `actual` **一字不动**。
  （改证据本身与改写写法是两件事；本工具只做后者。）
- 形如 `2>&1` / 管道 / `$( )` 的其他 shell 特性**不在此列**，遇则交人。
- `Examples/atoms/*.out` 是受控产物，本工具**不写**；它仍是 `run_match_file` 的比对基准。
