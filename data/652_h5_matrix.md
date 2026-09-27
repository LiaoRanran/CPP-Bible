# 652 H5 · 探针积木差分矩阵（L1 证据）

- 积木 6 个｜用例 8｜ok 4

| cc | std | opt | sanitizer | compile_rc | run_rc | sanitizer_tripped | status | 来源 |
|---|---|---|---|---|---|---|---|---|
| gcc | c11 | -O0 | none | 0 | 0 | None | ok | 真机 |
| gcc | c11 | -O0 | undefined | 1 |  |  | sanitizer_runtime_missing | 真机 |
| gcc | c11 | -O2 | none | 0 | 0 | None | ok | 真机 |
| gcc | c11 | -O2 | undefined | 1 |  |  | sanitizer_runtime_missing | 真机 |
| clang | c11 | -O0 | none | 0 | 0 | None | ok | 真机 |
| clang | c11 | -O0 | undefined | 1 |  |  | sanitizer_runtime_missing | 真机 |
| clang | c11 | -O2 | none | 0 | 0 | None | ok | 真机 |
| clang | c11 | -O2 | undefined | 1 |  |  | sanitizer_runtime_missing | 真机 |
