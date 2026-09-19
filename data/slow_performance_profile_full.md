# 全量 slow 性能剖析（609 B2 · cProfile，不改被测代码）

- 解释器：`C:\CodeLearnling\note\note\C++\CPP-Bible\.venv\Scripts\python.exe`
- 清单来源：`tests/conftest.py::SLOW_MODULES`（共 19 个文件）
- per-file 墙钟预算：**40s**（超时 ⇒ 标注未完成，不许拿残缺数据充数）
- 已完整剖析 **18** 个 · 超时未完成 **1** 个

## Top10 聚合瓶颈（按 tottime 求和）

| # | 函数 | 累计 tottime(s) |
|---|---|---|
| 1 | `~::<method 'read' of '_io.TextIOWrapper' objects>` | 68.883 |
| 2 | `~::<built-in method time.sleep>` | 9.106 |
| 3 | `~::<built-in method _winapi.CreateProcess>` | 5.908 |
| 4 | `~::<built-in method _io.open>` | 4.466 |
| 5 | `difflib.py::find_longest_match` | 1.223 |
| 6 | `~::<built-in method _io.open_code>` | 1.206 |
| 7 | `~::<built-in method nt.stat>` | 1.167 |
| 8 | `~::<method 'read' of '_io.BufferedReader' objects>` | 0.615 |
| 9 | `~::<built-in method marshal.load>` | 0.425 |
| 10 | `~::<built-in method _wmi.exec_query>` | 0.192 |

## 逐文件剖析

### test_artifact_snapshot.py

- 墙钟 **2.12s** · 退出码 0 · passed 5

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 0.558 | 30.2% | 117 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.136 | 7.4% | 2 | `~:0::<built-in method _wmi.exec_query>` |
| 0.094 | 5.1% | 262 | `~:0::<built-in method _io.open_code>` |
| 0.078 | 4.2% | 3185 | `~:0::<built-in method nt.stat>` |
| 0.062 | 3.4% | 287 | `~:0::<built-in method _io.open>` |

- 瓶颈判定：重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_atom_evidence_replay.py

- 墙钟 **13.41s** · 退出码 0 · passed 30

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 9.285 | 70.7% | 498 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 1.675 | 12.8% | 100 | `~:0::<built-in method _winapi.CreateProcess>` |
| 0.229 | 1.7% | 626 | `~:0::<built-in method _io.open>` |
| 0.229 | 1.7% | 404 | `~:0::<method 'read' of '_io.BufferedReader' objects>` |
| 0.152 | 1.2% | 99 | `~:0::<built-in method _winapi.WaitForSingleObject>` |

- 瓶颈判定：重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_ccache_prefix.py

- 墙钟 **1.61s** · 退出码 0 · passed 8

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 0.168 | 12.7% | 127 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.095 | 7.1% | 263 | `~:0::<built-in method _io.open_code>` |
| 0.085 | 6.4% | 3202 | `~:0::<built-in method nt.stat>` |
| 0.056 | 4.2% | 2 | `~:0::<built-in method _wmi.exec_query>` |
| 0.053 | 4.0% | 101 | `~:0::<built-in method marshal.load>` |

- 瓶颈判定：重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_ci_local_precheck.py

- 墙钟 **1.51s** · 退出码 0 · passed 3

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 0.162 | 13.1% | 96 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.091 | 7.3% | 256 | `~:0::<built-in method _io.open_code>` |
| 0.073 | 5.9% | 3085 | `~:0::<built-in method nt.stat>` |
| 0.053 | 4.3% | 101 | `~:0::<built-in method marshal.load>` |
| 0.049 | 3.9% | 478 | `~:0::<built-in method builtins.exec>` |

- 瓶颈判定：重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_discriminative.py

- 墙钟 **1.56s** · 退出码 0 · passed 5

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 0.162 | 12.5% | 110 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.093 | 7.1% | 262 | `~:0::<built-in method _io.open_code>` |
| 0.076 | 5.8% | 3147 | `~:0::<built-in method nt.stat>` |
| 0.058 | 4.5% | 276 | `~:0::<built-in method _io.open>` |
| 0.053 | 4.1% | 101 | `~:0::<built-in method marshal.load>` |

- 瓶颈判定：重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_incremental_replay.py

- 墙钟 **2.09s** · 退出码 0 · passed 10

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 0.547 | 30.2% | 144 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.096 | 5.3% | 336 | `~:0::<built-in method _io.open>` |
| 0.093 | 5.1% | 262 | `~:0::<built-in method _io.open_code>` |
| 0.076 | 4.2% | 3190 | `~:0::<built-in method nt.stat>` |
| 0.053 | 2.9% | 101 | `~:0::<built-in method marshal.load>` |

- 瓶颈判定：重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_json_output.py

- 墙钟 **21.1s** · 退出码 0 · passed 3 · failed 2

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 19.627 | 94.4% | 108 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.094 | 0.5% | 262 | `~:0::<built-in method _io.open_code>` |
| 0.078 | 0.4% | 3166 | `~:0::<built-in method nt.stat>` |
| 0.054 | 0.3% | 101 | `~:0::<built-in method marshal.load>` |
| 0.052 | 0.2% | 5 | `~:0::<built-in method _winapi.CreateProcess>` |

- 瓶颈判定：重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_p02_discriminative.py

- 墙钟 **1.56s** · 退出码 0 · passed 7

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 0.169 | 13.0% | 124 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.092 | 7.1% | 262 | `~:0::<built-in method _io.open_code>` |
| 0.075 | 5.8% | 3162 | `~:0::<built-in method nt.stat>` |
| 0.057 | 4.4% | 281 | `~:0::<built-in method _io.open>` |
| 0.053 | 4.1% | 101 | `~:0::<built-in method marshal.load>` |

- 瓶颈判定：重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_p0g_lock.py

- 墙钟 **10.38s** · 退出码 0 · passed 8

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 5.700 | 56.4% | 175 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 3.002 | 29.7% | 6 | `~:0::<built-in method time.sleep>` |
| 0.132 | 1.3% | 19 | `~:0::<built-in method _winapi.CreateProcess>` |
| 0.093 | 0.9% | 263 | `~:0::<built-in method _io.open_code>` |
| 0.087 | 0.9% | 331 | `~:0::<built-in method _io.open>` |

- 瓶颈判定：显式等待 ⇒ 缩小等待窗口或改事件通知（需确认语义不能被 races 依赖）

### test_patch_blocks.py

- 墙钟 **1.58s** · 退出码 0 · passed 6

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 0.170 | 12.9% | 113 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.092 | 7.0% | 256 | `~:0::<built-in method _io.open_code>` |
| 0.079 | 6.0% | 3100 | `~:0::<built-in method nt.stat>` |
| 0.077 | 5.9% | 281 | `~:0::<built-in method _io.open>` |
| 0.053 | 4.0% | 101 | `~:0::<built-in method marshal.load>` |

- 瓶颈判定：重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_poison_attack_type.py

- 墙钟 **9.81s** · 退出码 0 · passed 16

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 3.991 | 41.8% | 4013 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 1.001 | 10.5% | 2 | `~:0::<built-in method time.sleep>` |
| 0.744 | 7.8% | 4422 | `~:0::<built-in method _io.open>` |
| 0.509 | 5.3% | 42 | `~:0::<built-in method _winapi.CreateProcess>` |
| 0.304 | 3.2% | 433 | `difflib.py:305::find_longest_match` |

- 瓶颈判定：显式等待 ⇒ 缩小等待窗口或改事件通知（需确认语义不能被 races 依赖）；重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_poison_coverage_581.py

- 墙钟 **15.51s** · 退出码 0 · passed 3

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 7.080 | 46.5% | 846 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 2.001 | 13.1% | 4 | `~:0::<built-in method time.sleep>` |
| 0.937 | 6.2% | 77 | `~:0::<built-in method _winapi.CreateProcess>` |
| 0.936 | 6.1% | 1634 | `~:0::<built-in method _io.open>` |
| 0.601 | 3.9% | 866 | `difflib.py:305::find_longest_match` |

- 瓶颈判定：显式等待 ⇒ 缩小等待窗口或改事件通知（需确认语义不能被 races 依赖）

### test_poison_exemptions_581.py

- 墙钟 **9.54s** · 退出码 0 · passed 10

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 3.850 | 41.5% | 3761 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 1.001 | 10.8% | 2 | `~:0::<built-in method time.sleep>` |
| 0.686 | 7.4% | 4204 | `~:0::<built-in method _io.open>` |
| 0.515 | 5.6% | 39 | `~:0::<built-in method _winapi.CreateProcess>` |
| 0.317 | 3.4% | 433 | `difflib.py:305::find_longest_match` |

- 瓶颈判定：显式等待 ⇒ 缩小等待窗口或改事件通知（需确认语义不能被 races 依赖）；重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_build_reproducibility_603.py

- 墙钟 **7.57s** · 退出码 0 · passed 13

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 4.300 | 59.0% | 227 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 1.100 | 15.1% | 1 | `~:0::<built-in method time.sleep>` |
| 0.391 | 5.4% | 385 | `~:0::<built-in method _io.open>` |
| 0.248 | 3.4% | 36 | `~:0::<built-in method _winapi.CreateProcess>` |
| 0.094 | 1.3% | 263 | `~:0::<built-in method _io.open_code>` |

- 瓶颈判定：显式等待 ⇒ 缩小等待窗口或改事件通知（需确认语义不能被 races 依赖）；重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_recompile_invariant.py

- 墙钟 **4.97s** · 退出码 0 · passed 4

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 2.735 | 58.0% | 164 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.611 | 13.0% | 29 | `~:0::<built-in method _winapi.CreateProcess>` |
| 0.104 | 2.2% | 375 | `~:0::<method 'read' of '_io.BufferedReader' objects>` |
| 0.094 | 2.0% | 263 | `~:0::<built-in method _io.open_code>` |
| 0.082 | 1.7% | 3450 | `~:0::<built-in method nt.stat>` |

- 瓶颈判定：（未匹配到已知形态 ⇒ 需人工读 caller 图）

### test_replay_invariants_603.py

- 墙钟 **4.67s** · 退出码 0 · passed 6

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 2.320 | 52.8% | 166 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.511 | 11.6% | 26 | `~:0::<built-in method _winapi.CreateProcess>` |
| 0.282 | 6.4% | 386 | `~:0::<method 'read' of '_io.BufferedReader' objects>` |
| 0.089 | 2.0% | 263 | `~:0::<built-in method _io.open_code>` |
| 0.088 | 2.0% | 377 | `~:0::<built-in method _io.open>` |

- 瓶颈判定：（未匹配到已知形态 ⇒ 需人工读 caller 图）

### test_s1_s6.py

- 墙钟 **18.1s** · 退出码 0 · passed 16

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 7.778 | 43.7% | 4670 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 1.000 | 5.6% | 2 | `~:0::<built-in method time.sleep>` |
| 0.955 | 5.4% | 5767 | `~:0::<built-in method _io.open>` |
| 0.718 | 4.0% | 76 | `~:0::<built-in method _winapi.CreateProcess>` |
| 0.382 | 2.1% | 25049 | `~:0::<built-in method nt.stat>` |

- 瓶颈判定：显式等待 ⇒ 缩小等待窗口或改事件通知（需确认语义不能被 races 依赖）；重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_toolchain_regressions.py

- 墙钟 **1.72s** · 退出码 0 · passed 9

| tottime(s) | 占比 | calls | 函数 |
|---|---|---|---|
| 0.281 | 19.4% | 139 | `~:0::<method 'read' of '_io.TextIOWrapper' objects>` |
| 0.092 | 6.4% | 272 | `~:0::<built-in method _io.open_code>` |
| 0.083 | 5.7% | 3209 | `~:0::<built-in method nt.stat>` |
| 0.054 | 3.7% | 101 | `~:0::<built-in method marshal.load>` |
| 0.051 | 3.5% | 495 | `~:0::<built-in method builtins.exec>` |

- 瓶颈判定：重复读盘/重复哈希 ⇒ 数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希

### test_mutation_fuzz.py

- 墙钟 **40.02s** · 退出码 None · passed 12 · ⚠️ **TIMEOUT（未完成剖析）**

- 无可用 .prof（超时/解析失败）⇒ **不给瓶颈结论**（托底诚实）

