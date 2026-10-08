# 693-A2 · 人类裁决标注指南（Adjudication Guide v1）

- 生成：`tools/annotate_693_b.py` 配套文档（693-A2）
- 配套文件：
  - `data/693_human_adjudication_package.csv`（裁决表，`human_verdict` 列**留空**等你填）
  - `data/693_calibration_examples.md`（10 条校准题 + 答案）
  - `data/693_ai_double_label.json`（AI 双标的完整中间结果，含 B 的逐条理由）
- 适用范围：**只裁决 A 与 B 分歧的 31 条**（不是重标 145 条）

---

## 0. 一句话任务

给你一段**去标识化**的 C++ 源码，判断：**在一套固定的检测条件下，这八类检测资产里有没有任何一个会产出诊断报告？**

> ⚠ **判据是"检测器会不会报告"，不是"代码是不是坏"。**
> 大量真实缺陷（逻辑错误、协议缺陷、调度语义缺陷）在 asan/ubsan/tsan/编译器告警/
> 交叉编译/链接器下**一条报告都不会有**。这类应判 `miss`。
> 这不是你的失误，恰恰是这项研究的核心发现之一。

---

## 1. 八类检测资产（判定所依据的"检测条件"）

| # | 资产 | 判 `catch` 的典型形态 |
|---:|---|---|
| 1 | `asan` | AddressSanitizer 报告（越界读/写、UAF、double-free、alloc-dealloc-mismatch、泄漏 LSan、栈对象逃逸） |
| 2 | `ubsan` | UndefinedBehaviorSanitizer 报告（有符号溢出、除零、位移指数越界/为负、对齐违例、空引用、vptr 类型不符） |
| 3 | `tsan` | ThreadSanitizer 报告（无同步的并发读写同一非原子对象） |
| 4 | `compiler-warn` | 编译器告警（-Wall -Wextra 档；-Wuninitialized / -Wsequence-point / -Wreturn-local-addr / -Wformat / -Wsign-compare / -Wstrict-aliasing / -Wstringop-overflow / -Wshift-count-overflow / -Wparentheses / -Wreturn-type / -Wdeprecated-declarations…） |
| 5 | `wunsequenced` | clang `-Wunsequenced`（**本批标注时视为不可用**，见 §5 边界 C） |
| 6 | `cross-compile` | 两个不同编译器/工具链的**输出是否一致**（不一致 ⇒ 检出） |
| 7 | `linker` | 链接期报错（重复定义、未定义符号、ODR 违反） |
| 8 | `compile-time` | 编译失败（非良定义代码，如 C++11 起禁止的字符串字面量赋给 `char*`） |

**八资产取"或"**：任一资产报告 ⇒ `catch`。

---

## 2. 四态定义（你要填的 `human_verdict` 只能是这四个之一）

| 值 | 含义 | 什么时候用 |
|---|---|---|
| `catch` | 至少一个资产会**明确**产出诊断 | 你能说出是"哪个资产、哪一条规则"命中 |
| `miss` | 八资产**全部静默** | 缺陷真实存在，但没有任何资产会报告 |
| `unknown` | 判定依赖材料里**没给**的上下文 | 缺第二 TU / 缺链接顺序 / 缺 `-std` 版本 / 缺运行期参数 / 实际地址对齐不可知 |
| `contradiction` | 材料自相矛盾，无法给出单一判定 | 依赖文件缺失、代码无法编译到可讨论缺陷的地步、标注条件互斥 |

**不要用第五个值。** 如果你犹豫，就在 `human_note` 里写犹豫点，然后选更接近的那个。

---

## 3. 缺陷类型闭集（34 类，仅供你理解背景；本轮**不要求**你重标类型）

> 类型列 `defect_type_A` 只是给你看 A 侧的记录，用于判断"这个类型是否天生静默"。
> 如果你认为类型标错了，写进 `human_note`，**不要改 CSV 里的类型列**。

### 3.1 内存生命周期（memory_lifetime）
| 类型 | 定义 | 一例 |
|---|---|---|
| `memory_safety` | 内存安全类兜底（无 UAF/double-free/泄漏特征） | 裸指针所有权不清 |
| `use_after_free` | 释放后使用 | `delete p; *p = 2;` |
| `double_free` | 二次释放 | `delete p; delete p;` |
| `memory_leak` | 分配后永不释放 | `new int[100];` 无对应释放 |
| `smart_pointer` | 智能指针误用（成环、所有权错配） | `shared_ptr` 互指成环 |
| `raii_violation` | RAII 释放/析构违例 | 浅拷贝导致同一资源析构两次 |
| `move_semantics` | 移动语义误用（移后使用、返回局部引用） | `return std::move(local);` |

### 3.2 越界 / 空指针 / 未初始化
| 类型 | 定义 | 一例 |
|---|---|---|
| `out_of_bounds` | 越界读或写（堆/栈/全局，含指针算术越界、越界读导致的信息泄露） | `int a[4]; a[5]=1;` |
| `null_pointer_deref` | 空指针/空引用解引用 | `int* p=nullptr; *p=1;` |
| `uninitialized_read` | 读取未初始化对象 | `int x; return x*2;` |

### 3.3 整数与位运算
| 类型 | 定义 | 一例 |
|---|---|---|
| `integer_overflow` | 有符号整数溢出 | `INT_MAX + 1` |
| `bit_operation` | 位运算 UB（位移指数越界/为负、位域截断、符号位左移） | `1 << 40` |

### 3.4 类型 / 别名 / 对齐 / 字节序
| 类型 | 定义 | 一例 |
|---|---|---|
| `type_punning` | 经不相容类型访问同一对象 | `*(int*)&f` |
| `strict_aliasing` | 严格别名规则违例 | `float* pf = reinterpret_cast<float*>(&x);` |
| `alignment` | 未对齐访问 | `char b[16]; *(double*)(b+1) = 1.0;` |
| `endianness` | 字节序假设错误 | 直接按主机序读写网络字 |

### 3.5 并发
| 类型 | 定义 | 一例 |
|---|---|---|
| `data_race` | 无同步的并发访问同一非原子对象 | 两线程 `++g` |
| `atomic_ub` | 原子操作误用（ABA、已释放对象经原子发布后被读） | 发布后 `delete`，读者仍读 |
| `memory_order` | 内存序不足导致的同步缺失 | relaxed 标志同步普通数据 |
| `deadlock` | 死锁 / 锁顺序反转 / 优先级反转 | 持锁顺序不一致 |
| `condition_variable` | 条件变量误用（丢失唤醒、虚假唤醒） | `wait` 不带谓词 |

### 3.6 STL / 迭代器 / 字符串
| 类型 | 定义 | 一例 |
|---|---|---|
| `iterator_invalidation` | 修改容器后使用失效迭代器/引用 | `push_back` 后用旧迭代器 |
| `stl_container_ub` | 容器自身 UB（`vector<bool>` 代理、越界 `at`/`[]`） | `auto p = &vb[0];` |
| `string_ub` | 字符串/`string_view` 悬垂、越界 | `append` 后仍用旧 `string_view` |
| `algorithm_misuse` | 算法**前置条件**违例 | 对未排序区间调 `lower_bound` |

### 3.7 语言 / OOP / lambda
| 类型 | 定义 | 一例 |
|---|---|---|
| `virtual_function` | 虚函数/构造析构期虚调用语义 | 构造期虚调用（**良定义**，注意别误判） |
| `lambda_capture` | lambda 捕获生命周期缺陷 | 按引用捕获局部变量后逃逸 |
| `cross_tu_ub` | 跨翻译单元不一致 | 两 TU 对同一 inline 函数定义不同 |
| `linker_odr` | ODR / 重复定义 | 同一符号两份不同定义 |
| `logic_error` | **非 UB** 的语义/API/状态缺陷（CVE 类） | 重传了整个缓冲区而非增量 |
| `other_ub` | 词表无专属项的 UB 兜底 | 未指定求值顺序、杂项 UB |

### 3.8 嵌入式 / 平台
| 类型 | 定义 | 一例 |
|---|---|---|
| `volatile_misuse` | volatile 语义误用（当同步用、非 volatile 左值访问 volatile 对象） | 用 `volatile` 做跨线程标志 |
| `register_ub` | `register` 相关（弃用、取址） | `register int r;` |
| `interrupt_safety` | 信号/中断上下文安全 | 信号处理函数改非原子全局 |

---

## 4. 十条校准题（先看 `693_calibration_examples.md`，做完再对答案）

校准题覆盖本批最容易出错的五类判断：
1. **"代码坏"≠"catch"**（逻辑错误 ⇒ `miss`）
2. **未指定求值顺序**（unspecified，非 UB ⇒ `miss`；无序列点的多次修改 ⇒ `catch`）
3. **别名 UB 在默认告警档下静默**（⇒ `miss`）
4. **上下文缺失要用 `unknown`**（第二 TU、`-std`、运行期参数）
5. **"良定义但看起来可疑"**（构造期虚调用、`bswap` 两次、无符号位域截断 ⇒ `miss`）

---

## 5. 边界 case 说明（本批 31 条分歧里已经踩到的）

### A. 求值顺序：unspecified vs UB
- `f(g(), h())` —— 实参求值顺序 **unspecified**，两种顺序都合法，程序不会崩 ⇒ **`miss`**。
- `i = i++ + 1`、`a[i] = i++`、`f(i++, i++)` —— 同一表达式中对 `i` **多次修改且无序列点** ⇒ UB，
  且 GCC `-Wsequence-point`（属 `-Wall`）会告警 ⇒ **`catch`**。

### B. 别名 UB
- C 风格强转后解引用 `*(int*)p` ⇒ GCC `-Wstrict-aliasing`（`-Wall` 默认 level 3）告警 ⇒ `catch`。
- `reinterpret_cast<float*>(&x)` 后解引用 ⇒ 默认告警档下**通常静默** ⇒ `miss`
  （能观测它的只有 `-O0`/`-O2` 输出差异，不在八资产内）。

### C. `wunsequenced` 资产在本批标注中视为**不可用**
- 该资产依赖 clang 的 `-Wunsequenced`；本项目的 MinGW g++ 13.1 **不认这个选项**（673u 已如实登记）。
- ⇒ 遇到"只有 `-Wunsequenced` 才能报"的样本，按 compiler-warn 是否有等价告警判定，不要假设该资产存在。

### D. 未初始化读取依赖优化档
- `-Wuninitialized` / `-Wmaybe-uninitialized` 在 `-O0` 下常常**不报**，`-O2` 下才报。
- ⇒ 若你认为只在 `-O2` 才命中，判 `catch` 并在 note 写"仅 -O2"。

### E. `unknown` 的正当用法（不要因为怕出错就滥用）
正当：缺第二 TU（ODR 夹具）、缺 `-std`（`inline` 变量 / `register`）、缺运行期参数（除零依赖 `argc`）。
**不正当**："我不确定编译器会不会告警" —— 这种请直接选 `catch` 或 `miss` 并在 note 记下不确定。

### F. 泄漏污染（重要）
材料包有 **13 条**样本的头部注释残留了 `expected_verdict: catch/miss` 原文（689 净化未覆盖）。
裁决表里这些条目的 `leak_suspected=yes`。**请照常独立判断**，但请在 note 里注明你是否注意到了该注释。

---

## 6. 填写规范

| 列 | 你填吗 | 说明 |
|---|---|---|
| `sample_id` | 不改 | 匿名 ID |
| `code_sha256` | 不改 | 源码校验和，防串行 |
| `defect_type_A` | **不改** | 仅背景参考 |
| `annotator_A` / `annotator_B` / `b_confidence` / `b_reason` | **不改** | 两个标注者的原始结论 |
| `leak_suspected` | 不改 | 见 §5 F |
| `human_verdict` | ✅ **填** | `catch` / `miss` / `unknown` / `contradiction` 四选一 |
| `human_note` | ✅ 建议填 | 你的依据、命中的资产、不确定点 |
| `source_code` | 不改 | 去标识化源码全文 |

- 不要改文件名；不要增删行；不要排序。
- 中途退出也可以：未填的条目留空即视为未裁决，不进入统计。

---

## 7. 结果怎么用（预注册口径）

- 主指标：**人类裁决 vs A（实测标签）** 的 Cohen's κ 与 raw agreement。
- 次要指标：**人类裁决 vs B**、**A vs B** 的 κ（后者已由本批算出：78.6% / κ=0.495）。
- 敏感性：剔除 13 条 `leak_suspected=yes` 后的 κ（本批 A vs B：77.3% / κ=0.458）。
- 达标线沿用 689 协议 §6：verdict κ≥0.8。
- 统计脚本：`python tools/compute_693_iaa.py --csv data/693_human_adjudication_package.csv`
