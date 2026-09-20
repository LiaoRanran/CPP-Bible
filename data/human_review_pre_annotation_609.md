# 人审预标注报告（609 批次辅助）

> **声明**：本报告由 AI 预标注生成，仅作人审辅助参考，**不构成最终人审决策**。
> 最终人审必须由人确认后通过 `human_review_cli.py` 执行，reviewer 必须为 `human`。
> AI 预标注的建议基于 evidence 文本的信号强度分析，可能存在误判，请逐条核实。

## 统计概览

- 总候选边：388 条
- mis_to_prop（人审重点）：194 条
- prop_to_mis（对称边，W2自动击败）：194 条
- 唯一 MIS 组：42 个

### AI 预标注建议分布（仅 mis_to_prop 194 条）

| 建议 | 数量 | 占比 | 说明 |
|---|---:|---:|---|
| approve | 177 | 91.2% | 证据充分，建议确认攻击成立 |
| modify | 17 | 8.8% | 证据一般，建议调整权重待验证 |
| reject | 0 | 0.0% | 证据薄弱，建议拒绝攻击 |

## 按 MIS 组逐条预标注

### MIS-CONC-001（2 条边）

预标注分布：approve 2 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-CONC-001->ATOM-UB-GRAY-001::prop-1 | ATOM-UB-GRAY-001::prop-1 | volatile 只保证不被优化掉、不重排到同一线程内的 volatile 访问之外；**不**提供原子性、不提供跨线程 happens-before / 线程同步要用 std::atomic 配内存序（默认 seq_cst） | **approve** | 证据充分（4个强信号，含），攻击成立可信度高 |
| ae-MIS-CONC-001->ATOM-UB-GRAY-001::prop-2 | ATOM-UB-GRAY-001::prop-2 | volatile 只保证不被优化掉、不重排到同一线程内的 volatile 访问之外；**不**提供原子性、不提供跨线程 happens-before / 线程同步要用 std::atomic 配内存序（默认 seq_cst） | **approve** | 证据充分（4个强信号，含），攻击成立可信度高 |

### MIS-CONC-003（3 条边）

预标注分布：approve 3 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-CONC-003->ATOM-CONC-RACE-001::prop-1 | ATOM-CONC-RACE-001::prop-1 | TSan 只分析被 -fsanitize=thread 插桩的 TU；第三方库/内联汇编/未插桩 TU 内的竞争它看不到（漏报），故「没被报 ≠ 没有」 / 数据竞争是 C++ 标准明文的未定义行为，不是「答案偶尔错」：编译器可据此做激进优... | **approve** | 证据充分（7个强信号，含标准引用），攻击成立可信度高 |
| ae-MIS-CONC-003->ATOM-CONC-RACE-001::prop-2 | ATOM-CONC-RACE-001::prop-2 | TSan 只分析被 -fsanitize=thread 插桩的 TU；第三方库/内联汇编/未插桩 TU 内的竞争它看不到（漏报），故「没被报 ≠ 没有」 / 数据竞争是 C++ 标准明文的未定义行为，不是「答案偶尔错」：编译器可据此做激进优... | **approve** | 证据充分（7个强信号，含标准引用），攻击成立可信度高 |
| ae-MIS-CONC-003->ATOM-CONC-RACE-001::prop-3 | ATOM-CONC-RACE-001::prop-3 | TSan 只分析被 -fsanitize=thread 插桩的 TU；第三方库/内联汇编/未插桩 TU 内的竞争它看不到（漏报），故「没被报 ≠ 没有」 / 数据竞争是 C++ 标准明文的未定义行为，不是「答案偶尔错」：编译器可据此做激进优... | **approve** | 证据充分（7个强信号，含标准引用），攻击成立可信度高 |

### MIS-HIST-001（4 条边）

预标注分布：approve 4 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-HIST-001->ATOM-HIST-AUTOPTR-001::prop-1 | ATOM-HIST-AUTOPTR-001::prop-1 | 两者对拷贝的处置相反：auto_ptr 允许拷贝（且静默转移+清空源），unique_ptr 拷贝构造 = delete（编译期拒绝） | **approve** | 证据充分（7个强信号，含），攻击成立可信度高 |
| ae-MIS-HIST-001->ATOM-HIST-AUTOPTR-001::prop-2 | ATOM-HIST-AUTOPTR-001::prop-2 | 两者对拷贝的处置相反：auto_ptr 允许拷贝（且静默转移+清空源），unique_ptr 拷贝构造 = delete（编译期拒绝） | **approve** | 证据充分（7个强信号，含），攻击成立可信度高 |
| ae-MIS-HIST-001->ATOM-HIST-AUTOPTR-001::prop-3 | ATOM-HIST-AUTOPTR-001::prop-3 | 两者对拷贝的处置相反：auto_ptr 允许拷贝（且静默转移+清空源），unique_ptr 拷贝构造 = delete（编译期拒绝） | **approve** | 证据充分（7个强信号，含），攻击成立可信度高 |
| ae-MIS-HIST-001->ATOM-HIST-AUTOPTR-001::prop-4 | ATOM-HIST-AUTOPTR-001::prop-4 | 两者对拷贝的处置相反：auto_ptr 允许拷贝（且静默转移+清空源），unique_ptr 拷贝构造 = delete（编译期拒绝） | **approve** | 证据充分（7个强信号，含），攻击成立可信度高 |

### MIS-HIST-002（4 条边）

预标注分布：approve 4 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-HIST-002->ATOM-HIST-AUTOPTR-001::prop-1 | ATOM-HIST-AUTOPTR-001::prop-1 | 实测 GCC 15.3 的 libstdc++ 在 -std=c++14/17/23 三档**均仍提供** auto_ptr（<backward/auto_ptr.h>） / libc++ / MSVC 才是真移除 → 构成可移植性陷阱（在... | **approve** | 证据充分（9个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-HIST-002->ATOM-HIST-AUTOPTR-001::prop-2 | ATOM-HIST-AUTOPTR-001::prop-2 | 实测 GCC 15.3 的 libstdc++ 在 -std=c++14/17/23 三档**均仍提供** auto_ptr（<backward/auto_ptr.h>） / libc++ / MSVC 才是真移除 → 构成可移植性陷阱（在... | **approve** | 证据充分（9个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-HIST-002->ATOM-HIST-AUTOPTR-001::prop-3 | ATOM-HIST-AUTOPTR-001::prop-3 | 实测 GCC 15.3 的 libstdc++ 在 -std=c++14/17/23 三档**均仍提供** auto_ptr（<backward/auto_ptr.h>） / libc++ / MSVC 才是真移除 → 构成可移植性陷阱（在... | **approve** | 证据充分（9个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-HIST-002->ATOM-HIST-AUTOPTR-001::prop-4 | ATOM-HIST-AUTOPTR-001::prop-4 | 实测 GCC 15.3 的 libstdc++ 在 -std=c++14/17/23 三档**均仍提供** auto_ptr（<backward/auto_ptr.h>） / libc++ / MSVC 才是真移除 → 构成可移植性陷阱（在... | **approve** | 证据充分（9个强信号，含实测数据编译器验证），攻击成立可信度高 |

### MIS-HIST-003（4 条边）

预标注分布：approve 4 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-HIST-003->ATOM-HIST-AUTOPTR-001::prop-1 | ATOM-HIST-AUTOPTR-001::prop-1 | 拷贝构造签名 auto_ptr(auto_ptr&) 不满足 CopyConstructible 却仍能从非 const 对象拷贝——这是 C++98 **没有移动语义**时表达所有权的合理工程妥协，不是实现失误 / C++11 引入移动语... | **approve** | 证据充分（8个强信号，含），攻击成立可信度高 |
| ae-MIS-HIST-003->ATOM-HIST-AUTOPTR-001::prop-2 | ATOM-HIST-AUTOPTR-001::prop-2 | 拷贝构造签名 auto_ptr(auto_ptr&) 不满足 CopyConstructible 却仍能从非 const 对象拷贝——这是 C++98 **没有移动语义**时表达所有权的合理工程妥协，不是实现失误 / C++11 引入移动语... | **approve** | 证据充分（8个强信号，含），攻击成立可信度高 |
| ae-MIS-HIST-003->ATOM-HIST-AUTOPTR-001::prop-3 | ATOM-HIST-AUTOPTR-001::prop-3 | 拷贝构造签名 auto_ptr(auto_ptr&) 不满足 CopyConstructible 却仍能从非 const 对象拷贝——这是 C++98 **没有移动语义**时表达所有权的合理工程妥协，不是实现失误 / C++11 引入移动语... | **approve** | 证据充分（8个强信号，含），攻击成立可信度高 |
| ae-MIS-HIST-003->ATOM-HIST-AUTOPTR-001::prop-4 | ATOM-HIST-AUTOPTR-001::prop-4 | 拷贝构造签名 auto_ptr(auto_ptr&) 不满足 CopyConstructible 却仍能从非 const 对象拷贝——这是 C++98 **没有移动语义**时表达所有权的合理工程妥协，不是实现失误 / C++11 引入移动语... | **approve** | 证据充分（8个强信号，含），攻击成立可信度高 |

### MIS-LANG-001（3 条边）

预标注分布：approve 0 / modify 3 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-1 | ATOM-LANG-INLINE-001::prop-1 | ODR 要求同一实体的多个定义「consist of the same sequence of tokens」（[basic.def.odr]/16.4）；违反属 IFNDR——**无须诊断**：实测 -Wall -Wextra 编译两个不... | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |
| ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-2 | ATOM-LANG-INLINE-001::prop-2 | ODR 要求同一实体的多个定义「consist of the same sequence of tokens」（[basic.def.odr]/16.4）；违反属 IFNDR——**无须诊断**：实测 -Wall -Wextra 编译两个不... | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |
| ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-3 | ATOM-LANG-INLINE-001::prop-3 | ODR 要求同一实体的多个定义「consist of the same sequence of tokens」（[basic.def.odr]/16.4）；违反属 IFNDR——**无须诊断**：实测 -Wall -Wextra 编译两个不... | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |

### MIS-MEM-001（3 条边）

预标注分布：approve 0 / modify 3 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-1 | ATOM-MEM-MOVE-002::prop-1 | std::move 只是 static_cast<T&&>(x)，本身不生成任何指令 [expr.static.cast] / 移动是否发生取决于重载决议是否选中移动构造；源对象仅保证有效但未指定 [lib.types.movedfrom] | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |
| ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-2 | ATOM-MEM-MOVE-002::prop-2 | std::move 只是 static_cast<T&&>(x)，本身不生成任何指令 [expr.static.cast] / 移动是否发生取决于重载决议是否选中移动构造；源对象仅保证有效但未指定 [lib.types.movedfrom] | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |
| ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-3 | ATOM-MEM-MOVE-002::prop-3 | std::move 只是 static_cast<T&&>(x)，本身不生成任何指令 [expr.static.cast] / 移动是否发生取决于重载决议是否选中移动构造；源对象仅保证有效但未指定 [lib.types.movedfrom] | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |

### MIS-MEM-002（3 条边）

预标注分布：approve 3 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-1 | ATOM-MEM-MOVE-002::prop-1 | 标准只说源对象处于有效但未指定状态，清空是实现细节而非保证 [lib.types.movedfrom] / std::string 的小字符串优化（SSO）下移动后源可能仍保留内容；实测需 volatile 读回才观测得到 | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-2 | ATOM-MEM-MOVE-002::prop-2 | 标准只说源对象处于有效但未指定状态，清空是实现细节而非保证 [lib.types.movedfrom] / std::string 的小字符串优化（SSO）下移动后源可能仍保留内容；实测需 volatile 读回才观测得到 | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-3 | ATOM-MEM-MOVE-002::prop-3 | 标准只说源对象处于有效但未指定状态，清空是实现细节而非保证 [lib.types.movedfrom] / std::string 的小字符串优化（SSO）下移动后源可能仍保留内容；实测需 volatile 读回才观测得到 | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |

### MIS-MEM-003（3 条边）

预标注分布：approve 0 / modify 3 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-1 | ATOM-MEM-MOVE-002::prop-1 | 返回局部对象时编译器本就允许 NRVO / 隐式移动，加 std::move 反而阻断 NRVO / 对返回值而言 std::move 把 lvalue 转 xvalue，使 NRVO 不再适用——是减效不是增效 | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |
| ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-2 | ATOM-MEM-MOVE-002::prop-2 | 返回局部对象时编译器本就允许 NRVO / 隐式移动，加 std::move 反而阻断 NRVO / 对返回值而言 std::move 把 lvalue 转 xvalue，使 NRVO 不再适用——是减效不是增效 | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |
| ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-3 | ATOM-MEM-MOVE-002::prop-3 | 返回局部对象时编译器本就允许 NRVO / 隐式移动，加 std::move 反而阻断 NRVO / 对返回值而言 std::move 把 lvalue 转 xvalue，使 NRVO 不再适用——是减效不是增效 | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |

### MIS-MEM-004（3 条边）

预标注分布：approve 3 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-1 | ATOM-MEM-MOVE-002::prop-1 | std::move(const T&) 得到 const T&&，无法绑定 T&& 移动构造 → 静默退化为拷贝构造 | **approve** | 证据充分（3个强信号，含），攻击成立可信度高 |
| ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-2 | ATOM-MEM-MOVE-002::prop-2 | std::move(const T&) 得到 const T&&，无法绑定 T&& 移动构造 → 静默退化为拷贝构造 | **approve** | 证据充分（3个强信号，含），攻击成立可信度高 |
| ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-3 | ATOM-MEM-MOVE-002::prop-3 | std::move(const T&) 得到 const T&&，无法绑定 T&& 移动构造 → 静默退化为拷贝构造 | **approve** | 证据充分（3个强信号，含），攻击成立可信度高 |

### MIS-MEM-005（6 条边）

预标注分布：approve 6 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-1 | ATOM-MEM-MOVE-002::prop-1 | 函数体场景：具名右值引用是左值（[basic.lval] Note 3 原文：named rvalue references are treated as lvalues），`T y = x;` 触发拷贝构造；要移动须再写 std::mov... | **approve** | 证据充分（3个强信号，含），攻击成立可信度高 |
| ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-2 | ATOM-MEM-MOVE-002::prop-2 | 函数体场景：具名右值引用是左值（[basic.lval] Note 3 原文：named rvalue references are treated as lvalues），`T y = x;` 触发拷贝构造；要移动须再写 std::mov... | **approve** | 证据充分（3个强信号，含），攻击成立可信度高 |
| ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-3 | ATOM-MEM-MOVE-002::prop-3 | 函数体场景：具名右值引用是左值（[basic.lval] Note 3 原文：named rvalue references are treated as lvalues），`T y = x;` 触发拷贝构造；要移动须再写 std::mov... | **approve** | 证据充分（3个强信号，含），攻击成立可信度高 |
| ae-MIS-MEM-005->ATOM-MEM-RVREF-001::prop-1 | ATOM-MEM-RVREF-001::prop-1 | 函数体场景：具名右值引用是左值（[basic.lval] Note 3 原文：named rvalue references are treated as lvalues），`T y = x;` 触发拷贝构造；要移动须再写 std::mov... | **approve** | 证据充分（3个强信号，含），攻击成立可信度高 |
| ae-MIS-MEM-005->ATOM-MEM-RVREF-001::prop-2 | ATOM-MEM-RVREF-001::prop-2 | 函数体场景：具名右值引用是左值（[basic.lval] Note 3 原文：named rvalue references are treated as lvalues），`T y = x;` 触发拷贝构造；要移动须再写 std::mov... | **approve** | 证据充分（3个强信号，含），攻击成立可信度高 |
| ae-MIS-MEM-005->ATOM-MEM-RVREF-001::prop-3 | ATOM-MEM-RVREF-001::prop-3 | 函数体场景：具名右值引用是左值（[basic.lval] Note 3 原文：named rvalue references are treated as lvalues），`T y = x;` 触发拷贝构造；要移动须再写 std::mov... | **approve** | 证据充分（3个强信号，含），攻击成立可信度高 |

### MIS-MEM-011（4 条边）

预标注分布：approve 4 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-011->ATOM-HIST-AUTOPTR-001::prop-1 | ATOM-HIST-AUTOPTR-001::prop-1 | unique_ptr 不可拷贝，按值传参必须 std::move；调用点忘了 move 就是编译错误（这是优点） / 只读场景应传 T& 或 T*，不涉及所有权就别传智能指针 | **approve** | 证据充分（4个强信号，含），攻击成立可信度高 |
| ae-MIS-MEM-011->ATOM-HIST-AUTOPTR-001::prop-2 | ATOM-HIST-AUTOPTR-001::prop-2 | unique_ptr 不可拷贝，按值传参必须 std::move；调用点忘了 move 就是编译错误（这是优点） / 只读场景应传 T& 或 T*，不涉及所有权就别传智能指针 | **approve** | 证据充分（4个强信号，含），攻击成立可信度高 |
| ae-MIS-MEM-011->ATOM-HIST-AUTOPTR-001::prop-3 | ATOM-HIST-AUTOPTR-001::prop-3 | unique_ptr 不可拷贝，按值传参必须 std::move；调用点忘了 move 就是编译错误（这是优点） / 只读场景应传 T& 或 T*，不涉及所有权就别传智能指针 | **approve** | 证据充分（4个强信号，含），攻击成立可信度高 |
| ae-MIS-MEM-011->ATOM-HIST-AUTOPTR-001::prop-4 | ATOM-HIST-AUTOPTR-001::prop-4 | unique_ptr 不可拷贝，按值传参必须 std::move；调用点忘了 move 就是编译错误（这是优点） / 只读场景应传 T& 或 T*，不涉及所有权就别传智能指针 | **approve** | 证据充分（4个强信号，含），攻击成立可信度高 |

### MIS-MEM-012（3 条边）

预标注分布：approve 3 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-1 | ATOM-MEM-MOVE-002::prop-1 | 移动的收益来自**避免深拷贝**（掏空源对象）；对纯值类型（int、小 POD、无堆资源的聚合）移动与拷贝生成的代码完全相同——实测纯值组必搬 32 字节 SIMD，指针组只搬 8 字节，前者 move 无收益 / 无收益却加了 move ... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-2 | ATOM-MEM-MOVE-002::prop-2 | 移动的收益来自**避免深拷贝**（掏空源对象）；对纯值类型（int、小 POD、无堆资源的聚合）移动与拷贝生成的代码完全相同——实测纯值组必搬 32 字节 SIMD，指针组只搬 8 字节，前者 move 无收益 / 无收益却加了 move ... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-3 | ATOM-MEM-MOVE-002::prop-3 | 移动的收益来自**避免深拷贝**（掏空源对象）；对纯值类型（int、小 POD、无堆资源的聚合）移动与拷贝生成的代码完全相同——实测纯值组必搬 32 字节 SIMD，指针组只搬 8 字节，前者 move 无收益 / 无收益却加了 move ... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-013（3 条边）

预标注分布：approve 3 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-013->ATOM-MEM-RAII-001::prop-1 | ATOM-MEM-RAII-001::prop-1 | RAII 把释放绑到析构，由语言在作用域结束（含异常栈展开）保证调用；靠人'记得'在异常/提前 return 路径会漏删 → 泄漏 [except.ctor] / 实测：裸路径在 leak_path 后 g_live 留 1（未释放），同场... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-013->ATOM-MEM-RAII-001::prop-2 | ATOM-MEM-RAII-001::prop-2 | RAII 把释放绑到析构，由语言在作用域结束（含异常栈展开）保证调用；靠人'记得'在异常/提前 return 路径会漏删 → 泄漏 [except.ctor] / 实测：裸路径在 leak_path 后 g_live 留 1（未释放），同场... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-013->ATOM-MEM-RAII-001::prop-3 | ATOM-MEM-RAII-001::prop-3 | RAII 把释放绑到析构，由语言在作用域结束（含异常栈展开）保证调用；靠人'记得'在异常/提前 return 路径会漏删 → 泄漏 [except.ctor] / 实测：裸路径在 leak_path 后 g_live 留 1（未释放），同场... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-014（3 条边）

预标注分布：approve 3 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-014->ATOM-MEM-RAII-001::prop-1 | ATOM-MEM-RAII-001::prop-1 | 函数在 new 与尾部 delete 之间抛异常或提前 return，尾部 delete 不可达 → 泄漏；只有析构（RAII）在栈展开时必然调用 [except.ctor] / 实测：safe_path 抛异常后 RAII 析构仍调用（g... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-014->ATOM-MEM-RAII-001::prop-2 | ATOM-MEM-RAII-001::prop-2 | 函数在 new 与尾部 delete 之间抛异常或提前 return，尾部 delete 不可达 → 泄漏；只有析构（RAII）在栈展开时必然调用 [except.ctor] / 实测：safe_path 抛异常后 RAII 析构仍调用（g... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-014->ATOM-MEM-RAII-001::prop-3 | ATOM-MEM-RAII-001::prop-3 | 函数在 new 与尾部 delete 之间抛异常或提前 return，尾部 delete 不可达 → 泄漏；只有析构（RAII）在栈展开时必然调用 [except.ctor] / 实测：safe_path 抛异常后 RAII 析构仍调用（g... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-015（3 条边）

预标注分布：approve 3 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-015->ATOM-MEM-ALIGN-001::prop-1 | ATOM-MEM-ALIGN-001::prop-1 | 成员按自身对齐排列，编译器插 padding，sizeof 含 padding：实测 Padded{char a; int b} 的 sizeof=8 而非 5，int 偏移 4 而非 1 [basic.align]/[class.mem]... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-015->ATOM-MEM-ALIGN-001::prop-2 | ATOM-MEM-ALIGN-001::prop-2 | 成员按自身对齐排列，编译器插 padding，sizeof 含 padding：实测 Padded{char a; int b} 的 sizeof=8 而非 5，int 偏移 4 而非 1 [basic.align]/[class.mem]... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-015->ATOM-MEM-ALIGN-001::prop-3 | ATOM-MEM-ALIGN-001::prop-3 | 成员按自身对齐排列，编译器插 padding，sizeof 含 padding：实测 Padded{char a; int b} 的 sizeof=8 而非 5，int 偏移 4 而非 1 [basic.align]/[class.mem]... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-016（6 条边）

预标注分布：approve 6 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-016->ATOM-MEM-SHARED-001::prop-1 | ATOM-MEM-SHARED-001::prop-1 | shared_ptr 只在**非循环**的所有权图里自动释放；成环时引用计数永不为 0 → 泄漏（实测 EV-MEM-014 循环引用 destroyed count=0） / 打破循环须用 weak_ptr 旁观（不增计数）；把'自动管理... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-016->ATOM-MEM-SHARED-001::prop-2 | ATOM-MEM-SHARED-001::prop-2 | shared_ptr 只在**非循环**的所有权图里自动释放；成环时引用计数永不为 0 → 泄漏（实测 EV-MEM-014 循环引用 destroyed count=0） / 打破循环须用 weak_ptr 旁观（不增计数）；把'自动管理... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-016->ATOM-MEM-SHARED-001::prop-3 | ATOM-MEM-SHARED-001::prop-3 | shared_ptr 只在**非循环**的所有权图里自动释放；成环时引用计数永不为 0 → 泄漏（实测 EV-MEM-014 循环引用 destroyed count=0） / 打破循环须用 weak_ptr 旁观（不增计数）；把'自动管理... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-016->ATOM-MEM-WEAK-001::prop-1 | ATOM-MEM-WEAK-001::prop-1 | shared_ptr 只在**非循环**的所有权图里自动释放；成环时引用计数永不为 0 → 泄漏（实测 EV-MEM-014 循环引用 destroyed count=0） / 打破循环须用 weak_ptr 旁观（不增计数）；把'自动管理... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-016->ATOM-MEM-WEAK-001::prop-2 | ATOM-MEM-WEAK-001::prop-2 | shared_ptr 只在**非循环**的所有权图里自动释放；成环时引用计数永不为 0 → 泄漏（实测 EV-MEM-014 循环引用 destroyed count=0） / 打破循环须用 weak_ptr 旁观（不增计数）；把'自动管理... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-016->ATOM-MEM-WEAK-001::prop-3 | ATOM-MEM-WEAK-001::prop-3 | shared_ptr 只在**非循环**的所有权图里自动释放；成环时引用计数永不为 0 → 泄漏（实测 EV-MEM-014 循环引用 destroyed count=0） / 打破循环须用 weak_ptr 旁观（不增计数）；把'自动管理... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-017（6 条边）

预标注分布：approve 6 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-017->ATOM-MEM-MOVE-002::prop-1 | ATOM-MEM-MOVE-002::prop-1 | 实测 EV-MEM-022：转发链省略 forward 后，右值实参 copies=1 moves=0——形参是具名变量、函数体内按左值处理（[basic.lval] Note 3），每次转发多付一次拷贝 / std::forward<T>... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-017->ATOM-MEM-MOVE-002::prop-2 | ATOM-MEM-MOVE-002::prop-2 | 实测 EV-MEM-022：转发链省略 forward 后，右值实参 copies=1 moves=0——形参是具名变量、函数体内按左值处理（[basic.lval] Note 3），每次转发多付一次拷贝 / std::forward<T>... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-017->ATOM-MEM-MOVE-002::prop-3 | ATOM-MEM-MOVE-002::prop-3 | 实测 EV-MEM-022：转发链省略 forward 后，右值实参 copies=1 moves=0——形参是具名变量、函数体内按左值处理（[basic.lval] Note 3），每次转发多付一次拷贝 / std::forward<T>... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-017->ATOM-MEM-VALUE-002::prop-1 | ATOM-MEM-VALUE-002::prop-1 | 实测 EV-MEM-022：转发链省略 forward 后，右值实参 copies=1 moves=0——形参是具名变量、函数体内按左值处理（[basic.lval] Note 3），每次转发多付一次拷贝 / std::forward<T>... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-017->ATOM-MEM-VALUE-002::prop-2 | ATOM-MEM-VALUE-002::prop-2 | 实测 EV-MEM-022：转发链省略 forward 后，右值实参 copies=1 moves=0——形参是具名变量、函数体内按左值处理（[basic.lval] Note 3），每次转发多付一次拷贝 / std::forward<T>... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-017->ATOM-MEM-VALUE-002::prop-3 | ATOM-MEM-VALUE-002::prop-3 | 实测 EV-MEM-022：转发链省略 forward 后，右值实参 copies=1 moves=0——形参是具名变量、函数体内按左值处理（[basic.lval] Note 3），每次转发多付一次拷贝 / std::forward<T>... | **approve** | 证据充分（3个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-018（6 条边）

预标注分布：approve 6 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-018->ATOM-MEM-VALUE-001::prop-1 | ATOM-MEM-VALUE-001::prop-1 | 实测 EV-MEM-021：推导语境的模板 T&& 传**左值**时推 T=int&，T&& 经引用折叠成 int&（左值引用）；只有传右值才推 T=int、T&& 才是右值引用——T&& 是否为右值引用取决于实参，不是写死的 / T&& ... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-018->ATOM-MEM-VALUE-001::prop-2 | ATOM-MEM-VALUE-001::prop-2 | 实测 EV-MEM-021：推导语境的模板 T&& 传**左值**时推 T=int&，T&& 经引用折叠成 int&（左值引用）；只有传右值才推 T=int、T&& 才是右值引用——T&& 是否为右值引用取决于实参，不是写死的 / T&& ... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-018->ATOM-MEM-VALUE-001::prop-3 | ATOM-MEM-VALUE-001::prop-3 | 实测 EV-MEM-021：推导语境的模板 T&& 传**左值**时推 T=int&，T&& 经引用折叠成 int&（左值引用）；只有传右值才推 T=int、T&& 才是右值引用——T&& 是否为右值引用取决于实参，不是写死的 / T&& ... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-018->ATOM-MEM-VALUE-002::prop-1 | ATOM-MEM-VALUE-002::prop-1 | 实测 EV-MEM-021：推导语境的模板 T&& 传**左值**时推 T=int&，T&& 经引用折叠成 int&（左值引用）；只有传右值才推 T=int、T&& 才是右值引用——T&& 是否为右值引用取决于实参，不是写死的 / T&& ... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-018->ATOM-MEM-VALUE-002::prop-2 | ATOM-MEM-VALUE-002::prop-2 | 实测 EV-MEM-021：推导语境的模板 T&& 传**左值**时推 T=int&，T&& 经引用折叠成 int&（左值引用）；只有传右值才推 T=int、T&& 才是右值引用——T&& 是否为右值引用取决于实参，不是写死的 / T&& ... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-018->ATOM-MEM-VALUE-002::prop-3 | ATOM-MEM-VALUE-002::prop-3 | 实测 EV-MEM-021：推导语境的模板 T&& 传**左值**时推 T=int&，T&& 经引用折叠成 int&（左值引用）；只有传右值才推 T=int、T&& 才是右值引用——T&& 是否为右值引用取决于实参，不是写死的 / T&& ... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-019（7 条边）

预标注分布：approve 7 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-019->ATOM-MEM-MOVE-002::prop-1 | ATOM-MEM-MOVE-002::prop-1 | 实测 EV-MEM-024：只写析构、不写拷贝构造 → 隐式浅拷贝（allocs=1 same_ptr=1），同一块资源被析构两次（dtor_runs=2）；析构真释放时即 double free（WSL ASan 实报 attemptin... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-019->ATOM-MEM-MOVE-002::prop-2 | ATOM-MEM-MOVE-002::prop-2 | 实测 EV-MEM-024：只写析构、不写拷贝构造 → 隐式浅拷贝（allocs=1 same_ptr=1），同一块资源被析构两次（dtor_runs=2）；析构真释放时即 double free（WSL ASan 实报 attemptin... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-019->ATOM-MEM-MOVE-002::prop-3 | ATOM-MEM-MOVE-002::prop-3 | 实测 EV-MEM-024：只写析构、不写拷贝构造 → 隐式浅拷贝（allocs=1 same_ptr=1），同一块资源被析构两次（dtor_runs=2）；析构真释放时即 double free（WSL ASan 实报 attemptin... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-019->ATOM-MEM-RAII-002::prop-1 | ATOM-MEM-RAII-002::prop-1 | 实测 EV-MEM-024：只写析构、不写拷贝构造 → 隐式浅拷贝（allocs=1 same_ptr=1），同一块资源被析构两次（dtor_runs=2）；析构真释放时即 double free（WSL ASan 实报 attemptin... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-019->ATOM-MEM-RAII-002::prop-2 | ATOM-MEM-RAII-002::prop-2 | 实测 EV-MEM-024：只写析构、不写拷贝构造 → 隐式浅拷贝（allocs=1 same_ptr=1），同一块资源被析构两次（dtor_runs=2）；析构真释放时即 double free（WSL ASan 实报 attemptin... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-019->ATOM-MEM-RAII-002::prop-3 | ATOM-MEM-RAII-002::prop-3 | 实测 EV-MEM-024：只写析构、不写拷贝构造 → 隐式浅拷贝（allocs=1 same_ptr=1），同一块资源被析构两次（dtor_runs=2）；析构真释放时即 double free（WSL ASan 实报 attemptin... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-019->ATOM-MEM-RAII-002::prop-4 | ATOM-MEM-RAII-002::prop-4 | 实测 EV-MEM-024：只写析构、不写拷贝构造 → 隐式浅拷贝（allocs=1 same_ptr=1），同一块资源被析构两次（dtor_runs=2）；析构真释放时即 double free（WSL ASan 实报 attemptin... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-020（7 条边）

预标注分布：approve 7 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-020->ATOM-MEM-RAII-002::prop-1 | ATOM-MEM-RAII-002::prop-1 | Rule of Zero 的前提是**成员都是 RAII 类型**（unique_ptr/vector/string 等）：实测 EV-MEM-023，成员形状驱动隐式规则——unique_ptr 成员让移动隐式生成、拷贝被删、析构正确（a... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-020->ATOM-MEM-RAII-002::prop-2 | ATOM-MEM-RAII-002::prop-2 | Rule of Zero 的前提是**成员都是 RAII 类型**（unique_ptr/vector/string 等）：实测 EV-MEM-023，成员形状驱动隐式规则——unique_ptr 成员让移动隐式生成、拷贝被删、析构正确（a... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-020->ATOM-MEM-RAII-002::prop-3 | ATOM-MEM-RAII-002::prop-3 | Rule of Zero 的前提是**成员都是 RAII 类型**（unique_ptr/vector/string 等）：实测 EV-MEM-023，成员形状驱动隐式规则——unique_ptr 成员让移动隐式生成、拷贝被删、析构正确（a... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-020->ATOM-MEM-RAII-002::prop-4 | ATOM-MEM-RAII-002::prop-4 | Rule of Zero 的前提是**成员都是 RAII 类型**（unique_ptr/vector/string 等）：实测 EV-MEM-023，成员形状驱动隐式规则——unique_ptr 成员让移动隐式生成、拷贝被删、析构正确（a... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-020->ATOM-MEM-UNIQUE-001::prop-1 | ATOM-MEM-UNIQUE-001::prop-1 | Rule of Zero 的前提是**成员都是 RAII 类型**（unique_ptr/vector/string 等）：实测 EV-MEM-023，成员形状驱动隐式规则——unique_ptr 成员让移动隐式生成、拷贝被删、析构正确（a... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-020->ATOM-MEM-UNIQUE-001::prop-2 | ATOM-MEM-UNIQUE-001::prop-2 | Rule of Zero 的前提是**成员都是 RAII 类型**（unique_ptr/vector/string 等）：实测 EV-MEM-023，成员形状驱动隐式规则——unique_ptr 成员让移动隐式生成、拷贝被删、析构正确（a... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-020->ATOM-MEM-UNIQUE-001::prop-3 | ATOM-MEM-UNIQUE-001::prop-3 | Rule of Zero 的前提是**成员都是 RAII 类型**（unique_ptr/vector/string 等）：实测 EV-MEM-023，成员形状驱动隐式规则——unique_ptr 成员让移动隐式生成、拷贝被删、析构正确（a... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-021（7 条边）

预标注分布：approve 7 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-021->ATOM-MEM-ALLOC-001::prop-1 | ATOM-MEM-ALLOC-001::prop-1 | 实测 EV-MEM-027/028：把自定义 arena 策略（或 pmr 的 monotonic_buffer_resource）注入容器，16 次 push_back 零堆分配（heap_new=0 / upstream_allocs=... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-021->ATOM-MEM-ALLOC-001::prop-2 | ATOM-MEM-ALLOC-001::prop-2 | 实测 EV-MEM-027/028：把自定义 arena 策略（或 pmr 的 monotonic_buffer_resource）注入容器，16 次 push_back 零堆分配（heap_new=0 / upstream_allocs=... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-021->ATOM-MEM-ALLOC-001::prop-3 | ATOM-MEM-ALLOC-001::prop-3 | 实测 EV-MEM-027/028：把自定义 arena 策略（或 pmr 的 monotonic_buffer_resource）注入容器，16 次 push_back 零堆分配（heap_new=0 / upstream_allocs=... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-021->ATOM-MEM-ALLOC-001::prop-4 | ATOM-MEM-ALLOC-001::prop-4 | 实测 EV-MEM-027/028：把自定义 arena 策略（或 pmr 的 monotonic_buffer_resource）注入容器，16 次 push_back 零堆分配（heap_new=0 / upstream_allocs=... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-021->ATOM-MEM-NEW-001::prop-1 | ATOM-MEM-NEW-001::prop-1 | 实测 EV-MEM-027/028：把自定义 arena 策略（或 pmr 的 monotonic_buffer_resource）注入容器，16 次 push_back 零堆分配（heap_new=0 / upstream_allocs=... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-021->ATOM-MEM-NEW-001::prop-2 | ATOM-MEM-NEW-001::prop-2 | 实测 EV-MEM-027/028：把自定义 arena 策略（或 pmr 的 monotonic_buffer_resource）注入容器，16 次 push_back 零堆分配（heap_new=0 / upstream_allocs=... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-021->ATOM-MEM-NEW-001::prop-3 | ATOM-MEM-NEW-001::prop-3 | 实测 EV-MEM-027/028：把自定义 arena 策略（或 pmr 的 monotonic_buffer_resource）注入容器，16 次 push_back 零堆分配（heap_new=0 / upstream_allocs=... | **approve** | 证据充分（5个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-022（5 条边）

预标注分布：approve 5 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-022->ATOM-MEM-NEW-001::prop-1 | ATOM-MEM-NEW-001::prop-1 | 实测 EV-MEM-029：len≤15 的字符串构造零堆分配（SSO：短串存对象内部 32 字节缓冲），len=16 才首次落堆（本机 libstdc++ 阈值 15） / 实测 EV-MEM-030：短字符串拷贝 allocs=0（只搬... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-022->ATOM-MEM-NEW-001::prop-2 | ATOM-MEM-NEW-001::prop-2 | 实测 EV-MEM-029：len≤15 的字符串构造零堆分配（SSO：短串存对象内部 32 字节缓冲），len=16 才首次落堆（本机 libstdc++ 阈值 15） / 实测 EV-MEM-030：短字符串拷贝 allocs=0（只搬... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-022->ATOM-MEM-NEW-001::prop-3 | ATOM-MEM-NEW-001::prop-3 | 实测 EV-MEM-029：len≤15 的字符串构造零堆分配（SSO：短串存对象内部 32 字节缓冲），len=16 才首次落堆（本机 libstdc++ 阈值 15） / 实测 EV-MEM-030：短字符串拷贝 allocs=0（只搬... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-022->ATOM-MEM-PERF-002::prop-1 | ATOM-MEM-PERF-002::prop-1 | 实测 EV-MEM-029：len≤15 的字符串构造零堆分配（SSO：短串存对象内部 32 字节缓冲），len=16 才首次落堆（本机 libstdc++ 阈值 15） / 实测 EV-MEM-030：短字符串拷贝 allocs=0（只搬... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-022->ATOM-MEM-PERF-002::prop-2 | ATOM-MEM-PERF-002::prop-2 | 实测 EV-MEM-029：len≤15 的字符串构造零堆分配（SSO：短串存对象内部 32 字节缓冲），len=16 才首次落堆（本机 libstdc++ 阈值 15） / 实测 EV-MEM-030：短字符串拷贝 allocs=0（只搬... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |

### MIS-MEM-023（6 条边）

预标注分布：approve 6 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-023->ATOM-MEM-ALLOC-001::prop-1 | ATOM-MEM-ALLOC-001::prop-1 | 本机实测 EV-MEM-029/031：libstdc++（GCC 15.3.0）SSO 容量 15（sizeof=32）；而 libc++（Clang）为 22 字符（sizeof=24）、MSVC 为 15 字符（sizeof=32）—... | **approve** | 证据充分（5个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-023->ATOM-MEM-ALLOC-001::prop-2 | ATOM-MEM-ALLOC-001::prop-2 | 本机实测 EV-MEM-029/031：libstdc++（GCC 15.3.0）SSO 容量 15（sizeof=32）；而 libc++（Clang）为 22 字符（sizeof=24）、MSVC 为 15 字符（sizeof=32）—... | **approve** | 证据充分（5个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-023->ATOM-MEM-ALLOC-001::prop-3 | ATOM-MEM-ALLOC-001::prop-3 | 本机实测 EV-MEM-029/031：libstdc++（GCC 15.3.0）SSO 容量 15（sizeof=32）；而 libc++（Clang）为 22 字符（sizeof=24）、MSVC 为 15 字符（sizeof=32）—... | **approve** | 证据充分（5个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-023->ATOM-MEM-ALLOC-001::prop-4 | ATOM-MEM-ALLOC-001::prop-4 | 本机实测 EV-MEM-029/031：libstdc++（GCC 15.3.0）SSO 容量 15（sizeof=32）；而 libc++（Clang）为 22 字符（sizeof=24）、MSVC 为 15 字符（sizeof=32）—... | **approve** | 证据充分（5个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-023->ATOM-MEM-PERF-002::prop-1 | ATOM-MEM-PERF-002::prop-1 | 本机实测 EV-MEM-029/031：libstdc++（GCC 15.3.0）SSO 容量 15（sizeof=32）；而 libc++（Clang）为 22 字符（sizeof=24）、MSVC 为 15 字符（sizeof=32）—... | **approve** | 证据充分（5个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-023->ATOM-MEM-PERF-002::prop-2 | ATOM-MEM-PERF-002::prop-2 | 本机实测 EV-MEM-029/031：libstdc++（GCC 15.3.0）SSO 容量 15（sizeof=32）；而 libc++（Clang）为 22 字符（sizeof=24）、MSVC 为 15 字符（sizeof=32）—... | **approve** | 证据充分（5个强信号，含实测数据编译器验证），攻击成立可信度高 |

### MIS-MEM-024（9 条边）

预标注分布：approve 9 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-024->ATOM-MEM-SHARED-001::prop-1 | ATOM-MEM-SHARED-001::prop-1 | 语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-024->ATOM-MEM-SHARED-001::prop-2 | ATOM-MEM-SHARED-001::prop-2 | 语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-024->ATOM-MEM-SHARED-001::prop-3 | ATOM-MEM-SHARED-001::prop-3 | 语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-024->ATOM-MEM-UNIQUE-001::prop-1 | ATOM-MEM-UNIQUE-001::prop-1 | 语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-024->ATOM-MEM-UNIQUE-001::prop-2 | ATOM-MEM-UNIQUE-001::prop-2 | 语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-024->ATOM-MEM-UNIQUE-001::prop-3 | ATOM-MEM-UNIQUE-001::prop-3 | 语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-024->ATOM-MEM-UNIQUE-002::prop-1 | ATOM-MEM-UNIQUE-002::prop-1 | 语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-024->ATOM-MEM-UNIQUE-002::prop-2 | ATOM-MEM-UNIQUE-002::prop-2 | 语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-024->ATOM-MEM-UNIQUE-002::prop-3 | ATOM-MEM-UNIQUE-002::prop-3 | 语言层面：`std::shared_ptr<T, D>` **不存在**——实测 GCC 15.3.0 与 14.2 均报 `error: wrong number of template arguments (2, should be 1... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |

### MIS-MEM-025（6 条边）

预标注分布：approve 6 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-025->ATOM-MEM-NEW-001::prop-1 | ATOM-MEM-NEW-001::prop-1 | 接口不同：实测 EV-MEM-032 编译期 trait——`unique_ptr<int[]>` 有 operator[]（subscript=1）但**没有** operator* 与 operator->（deref=0 arrow=... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-025->ATOM-MEM-NEW-001::prop-2 | ATOM-MEM-NEW-001::prop-2 | 接口不同：实测 EV-MEM-032 编译期 trait——`unique_ptr<int[]>` 有 operator[]（subscript=1）但**没有** operator* 与 operator->（deref=0 arrow=... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-025->ATOM-MEM-NEW-001::prop-3 | ATOM-MEM-NEW-001::prop-3 | 接口不同：实测 EV-MEM-032 编译期 trait——`unique_ptr<int[]>` 有 operator[]（subscript=1）但**没有** operator* 与 operator->（deref=0 arrow=... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-025->ATOM-MEM-UNIQUE-002::prop-1 | ATOM-MEM-UNIQUE-002::prop-1 | 接口不同：实测 EV-MEM-032 编译期 trait——`unique_ptr<int[]>` 有 operator[]（subscript=1）但**没有** operator* 与 operator->（deref=0 arrow=... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-025->ATOM-MEM-UNIQUE-002::prop-2 | ATOM-MEM-UNIQUE-002::prop-2 | 接口不同：实测 EV-MEM-032 编译期 trait——`unique_ptr<int[]>` 有 operator[]（subscript=1）但**没有** operator* 与 operator->（deref=0 arrow=... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-025->ATOM-MEM-UNIQUE-002::prop-3 | ATOM-MEM-UNIQUE-002::prop-3 | 接口不同：实测 EV-MEM-032 编译期 trait——`unique_ptr<int[]>` 有 operator[]（subscript=1）但**没有** operator* 与 operator->（deref=0 arrow=... | **approve** | 证据充分（6个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-026（9 条边）

预标注分布：approve 9 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-026->ATOM-MEM-SHARED-001::prop-1 | ATOM-MEM-SHARED-001::prop-1 | 边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个... | **approve** | 证据充分（7个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-026->ATOM-MEM-SHARED-001::prop-2 | ATOM-MEM-SHARED-001::prop-2 | 边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个... | **approve** | 证据充分（7个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-026->ATOM-MEM-SHARED-001::prop-3 | ATOM-MEM-SHARED-001::prop-3 | 边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个... | **approve** | 证据充分（7个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-026->ATOM-MEM-SHARED-002::prop-1 | ATOM-MEM-SHARED-002::prop-1 | 边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个... | **approve** | 证据充分（7个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-026->ATOM-MEM-SHARED-002::prop-2 | ATOM-MEM-SHARED-002::prop-2 | 边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个... | **approve** | 证据充分（7个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-026->ATOM-MEM-SHARED-002::prop-3 | ATOM-MEM-SHARED-002::prop-3 | 边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个... | **approve** | 证据充分（7个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-026->ATOM-MEM-WEAK-001::prop-1 | ATOM-MEM-WEAK-001::prop-1 | 边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个... | **approve** | 证据充分（7个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-026->ATOM-MEM-WEAK-001::prop-2 | ATOM-MEM-WEAK-001::prop-2 | 边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个... | **approve** | 证据充分（7个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-026->ATOM-MEM-WEAK-001::prop-3 | ATOM-MEM-WEAK-001::prop-3 | 边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个... | **approve** | 证据充分（7个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-027（9 条边）

预标注分布：approve 9 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-027->ATOM-MEM-LEAK-001::prop-1 | ATOM-MEM-LEAK-001::prop-1 | 退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-027->ATOM-MEM-LEAK-001::prop-2 | ATOM-MEM-LEAK-001::prop-2 | 退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-027->ATOM-MEM-LEAK-001::prop-3 | ATOM-MEM-LEAK-001::prop-3 | 退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-027->ATOM-MEM-SHARED-001::prop-1 | ATOM-MEM-SHARED-001::prop-1 | 退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-027->ATOM-MEM-SHARED-001::prop-2 | ATOM-MEM-SHARED-001::prop-2 | 退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-027->ATOM-MEM-SHARED-001::prop-3 | ATOM-MEM-SHARED-001::prop-3 | 退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-027->ATOM-MEM-WEAK-001::prop-1 | ATOM-MEM-WEAK-001::prop-1 | 退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-027->ATOM-MEM-WEAK-001::prop-2 | ATOM-MEM-WEAK-001::prop-2 | 退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-027->ATOM-MEM-WEAK-001::prop-3 | ATOM-MEM-WEAK-001::prop-3 | 退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |

### MIS-MEM-028（9 条边）

预标注分布：approve 9 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-028->ATOM-MEM-ALLOC-001::prop-1 | ATOM-MEM-ALLOC-001::prop-1 | 实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`siz... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-028->ATOM-MEM-ALLOC-001::prop-2 | ATOM-MEM-ALLOC-001::prop-2 | 实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`siz... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-028->ATOM-MEM-ALLOC-001::prop-3 | ATOM-MEM-ALLOC-001::prop-3 | 实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`siz... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-028->ATOM-MEM-ALLOC-001::prop-4 | ATOM-MEM-ALLOC-001::prop-4 | 实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`siz... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-028->ATOM-MEM-PERF-002::prop-1 | ATOM-MEM-PERF-002::prop-1 | 实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`siz... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-028->ATOM-MEM-PERF-002::prop-2 | ATOM-MEM-PERF-002::prop-2 | 实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`siz... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-028->ATOM-MEM-PERF-003::prop-1 | ATOM-MEM-PERF-003::prop-1 | 实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`siz... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-028->ATOM-MEM-PERF-003::prop-2 | ATOM-MEM-PERF-003::prop-2 | 实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`siz... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-MEM-028->ATOM-MEM-PERF-003::prop-3 | ATOM-MEM-PERF-003::prop-3 | 实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`siz... | **approve** | 证据充分（4个强信号，含实测数据编译器验证），攻击成立可信度高 |

### MIS-MEM-029（5 条边）

预标注分布：approve 5 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-029->ATOM-MEM-PERF-001::prop-1 | ATOM-MEM-PERF-001::prop-1 | **平台翻转是实测的**：同一夹具、同一工作量，MinGW 15.3.0/libstdc++ 上 `monotonic < pool < global`（两资源快 4.4× 与 2.0×），Linux/glibc 上 `global < p... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-029->ATOM-MEM-PERF-001::prop-2 | ATOM-MEM-PERF-001::prop-2 | **平台翻转是实测的**：同一夹具、同一工作量，MinGW 15.3.0/libstdc++ 上 `monotonic < pool < global`（两资源快 4.4× 与 2.0×），Linux/glibc 上 `global < p... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-029->ATOM-MEM-PERF-003::prop-1 | ATOM-MEM-PERF-003::prop-1 | **平台翻转是实测的**：同一夹具、同一工作量，MinGW 15.3.0/libstdc++ 上 `monotonic < pool < global`（两资源快 4.4× 与 2.0×），Linux/glibc 上 `global < p... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-029->ATOM-MEM-PERF-003::prop-2 | ATOM-MEM-PERF-003::prop-2 | **平台翻转是实测的**：同一夹具、同一工作量，MinGW 15.3.0/libstdc++ 上 `monotonic < pool < global`（两资源快 4.4× 与 2.0×），Linux/glibc 上 `global < p... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-029->ATOM-MEM-PERF-003::prop-3 | ATOM-MEM-PERF-003::prop-3 | **平台翻转是实测的**：同一夹具、同一工作量，MinGW 15.3.0/libstdc++ 上 `monotonic < pool < global`（两资源快 4.4× 与 2.0×），Linux/glibc 上 `global < p... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |

### MIS-MEM-030（7 条边）

预标注分布：approve 7 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-030->ATOM-MEM-ALLOC-001::prop-1 | ATOM-MEM-ALLOC-001::prop-1 | **零内部碎片只在"批量申请 + 整体释放"下成立**：本批夹具的 `Arena` 只有 `release_all()`（重置 bump 偏移），**没有单块释放接口**；实测峰值 24000 B（= 24×1000）、元数据仅 8 B、内... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-030->ATOM-MEM-ALLOC-001::prop-2 | ATOM-MEM-ALLOC-001::prop-2 | **零内部碎片只在"批量申请 + 整体释放"下成立**：本批夹具的 `Arena` 只有 `release_all()`（重置 bump 偏移），**没有单块释放接口**；实测峰值 24000 B（= 24×1000）、元数据仅 8 B、内... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-030->ATOM-MEM-ALLOC-001::prop-3 | ATOM-MEM-ALLOC-001::prop-3 | **零内部碎片只在"批量申请 + 整体释放"下成立**：本批夹具的 `Arena` 只有 `release_all()`（重置 bump 偏移），**没有单块释放接口**；实测峰值 24000 B（= 24×1000）、元数据仅 8 B、内... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-030->ATOM-MEM-ALLOC-001::prop-4 | ATOM-MEM-ALLOC-001::prop-4 | **零内部碎片只在"批量申请 + 整体释放"下成立**：本批夹具的 `Arena` 只有 `release_all()`（重置 bump 偏移），**没有单块释放接口**；实测峰值 24000 B（= 24×1000）、元数据仅 8 B、内... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-030->ATOM-MEM-ALLOC-002::prop-1 | ATOM-MEM-ALLOC-002::prop-1 | **零内部碎片只在"批量申请 + 整体释放"下成立**：本批夹具的 `Arena` 只有 `release_all()`（重置 bump 偏移），**没有单块释放接口**；实测峰值 24000 B（= 24×1000）、元数据仅 8 B、内... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-030->ATOM-MEM-ALLOC-002::prop-2 | ATOM-MEM-ALLOC-002::prop-2 | **零内部碎片只在"批量申请 + 整体释放"下成立**：本批夹具的 `Arena` 只有 `release_all()`（重置 bump 偏移），**没有单块释放接口**；实测峰值 24000 B（= 24×1000）、元数据仅 8 B、内... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-030->ATOM-MEM-ALLOC-002::prop-3 | ATOM-MEM-ALLOC-002::prop-3 | **零内部碎片只在"批量申请 + 整体释放"下成立**：本批夹具的 `Arena` 只有 `release_all()`（重置 bump 偏移），**没有单块释放接口**；实测峰值 24000 B（= 24×1000）、元数据仅 8 B、内... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |

### MIS-MEM-031（12 条边）

预标注分布：approve 12 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-031->ATOM-MEM-LEAK-001::prop-1 | ATOM-MEM-LEAK-001::prop-1 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-LEAK-001::prop-2 | ATOM-MEM-LEAK-001::prop-2 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-LEAK-001::prop-3 | ATOM-MEM-LEAK-001::prop-3 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-LEAK-002::prop-1 | ATOM-MEM-LEAK-002::prop-1 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-LEAK-002::prop-2 | ATOM-MEM-LEAK-002::prop-2 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-LEAK-002::prop-3 | ATOM-MEM-LEAK-002::prop-3 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-SHARED-001::prop-1 | ATOM-MEM-SHARED-001::prop-1 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-SHARED-001::prop-2 | ATOM-MEM-SHARED-001::prop-2 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-SHARED-001::prop-3 | ATOM-MEM-SHARED-001::prop-3 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-WEAK-001::prop-1 | ATOM-MEM-WEAK-001::prop-1 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-WEAK-001::prop-2 | ATOM-MEM-WEAK-001::prop-2 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |
| ae-MIS-MEM-031->ATOM-MEM-WEAK-001::prop-3 | ATOM-MEM-WEAK-001::prop-3 | **本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_... | **approve** | 证据充分（4个强信号，含实测数据），攻击成立可信度高 |

### MIS-MEM-032（6 条边）

预标注分布：approve 6 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-MEM-032->ATOM-MEM-PERF-003::prop-1 | ATOM-MEM-PERF-003::prop-1 | **无数据竞争 ≠ 无性能代价**：4 线程各累加 1e7 次到**逻辑完全独立**的计数器，相邻布局中位数 562500600 ns、`alignas` 隔离后 29824800 ns ⇒ **慢 18.86 倍**（Linux 同夹具 ... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-032->ATOM-MEM-PERF-003::prop-2 | ATOM-MEM-PERF-003::prop-2 | **无数据竞争 ≠ 无性能代价**：4 线程各累加 1e7 次到**逻辑完全独立**的计数器，相邻布局中位数 562500600 ns、`alignas` 隔离后 29824800 ns ⇒ **慢 18.86 倍**（Linux 同夹具 ... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-032->ATOM-MEM-PERF-003::prop-3 | ATOM-MEM-PERF-003::prop-3 | **无数据竞争 ≠ 无性能代价**：4 线程各累加 1e7 次到**逻辑完全独立**的计数器，相邻布局中位数 562500600 ns、`alignas` 隔离后 29824800 ns ⇒ **慢 18.86 倍**（Linux 同夹具 ... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-032->ATOM-MEM-PERF-004::prop-1 | ATOM-MEM-PERF-004::prop-1 | **无数据竞争 ≠ 无性能代价**：4 线程各累加 1e7 次到**逻辑完全独立**的计数器，相邻布局中位数 562500600 ns、`alignas` 隔离后 29824800 ns ⇒ **慢 18.86 倍**（Linux 同夹具 ... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-032->ATOM-MEM-PERF-004::prop-2 | ATOM-MEM-PERF-004::prop-2 | **无数据竞争 ≠ 无性能代价**：4 线程各累加 1e7 次到**逻辑完全独立**的计数器，相邻布局中位数 562500600 ns、`alignas` 隔离后 29824800 ns ⇒ **慢 18.86 倍**（Linux 同夹具 ... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-MEM-032->ATOM-MEM-PERF-004::prop-3 | ATOM-MEM-PERF-004::prop-3 | **无数据竞争 ≠ 无性能代价**：4 线程各累加 1e7 次到**逻辑完全独立**的计数器，相邻布局中位数 562500600 ns、`alignas` 隔离后 29824800 ns ⇒ **慢 18.86 倍**（Linux 同夹具 ... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |

### MIS-UB-001（2 条边）

预标注分布：approve 0 / modify 2 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-1 | ATOM-UB-GRAY-001::prop-1 | UB 的典型表现恰恰是**在 -O2 下看起来正常**：优化器以 UB 不可能发生为前提做推导，可删掉别的正确代码 / 没有报错不等于没有 UB；判定依据是标准条文而非运行结果 | **modify** | 证据一般（1个强信号/1个弱信号），建议modify为low待进一步验证 |
| ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-2 | ATOM-UB-GRAY-001::prop-2 | UB 的典型表现恰恰是**在 -O2 下看起来正常**：优化器以 UB 不可能发生为前提做推导，可删掉别的正确代码 / 没有报错不等于没有 UB；判定依据是标准条文而非运行结果 | **modify** | 证据一般（1个强信号/1个弱信号），建议modify为low待进一步验证 |

### MIS-UB-002（2 条边）

预标注分布：approve 2 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-UB-002->ATOM-UB-GRAY-001::prop-1 | ATOM-UB-GRAY-001::prop-1 | 有符号溢出是 UB，无符号才是定义好的模运算——两者规则不同，不能类推 / 实测后果：GCC -O2 依此把 for (int i=0; i>=0; ++i) 编译成无条件 jmp 死循环 | **approve** | 证据充分（3个强信号，含实测数据编译器验证），攻击成立可信度高 |
| ae-MIS-UB-002->ATOM-UB-GRAY-001::prop-2 | ATOM-UB-GRAY-001::prop-2 | 有符号溢出是 UB，无符号才是定义好的模运算——两者规则不同，不能类推 / 实测后果：GCC -O2 依此把 for (int i=0; i>=0; ++i) 编译成无条件 jmp 死循环 | **approve** | 证据充分（3个强信号，含实测数据编译器验证），攻击成立可信度高 |

### MIS-UB-003（2 条边）

预标注分布：approve 2 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-UB-003->ATOM-UB-GRAY-001::prop-1 | ATOM-UB-GRAY-001::prop-1 | 解引用空指针已是 UB；优化器据此反推 p 非空，可能把后续判空检查整段删掉 / 实测汇编可见删掉检查后只剩 movl %eax,0 + ud2——保护被优化器移除 | **approve** | 证据较充分（4个强信号），建议approve，可信度medium |
| ae-MIS-UB-003->ATOM-UB-GRAY-001::prop-2 | ATOM-UB-GRAY-001::prop-2 | 解引用空指针已是 UB；优化器据此反推 p 非空，可能把后续判空检查整段删掉 / 实测汇编可见删掉检查后只剩 movl %eax,0 + ud2——保护被优化器移除 | **approve** | 证据较充分（4个强信号），建议approve，可信度medium |

### MIS-UB-004（2 条边）

预标注分布：approve 0 / modify 2 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-UB-004->ATOM-UB-GRAY-001::prop-1 | ATOM-UB-GRAY-001::prop-1 | UB 会去相关：优化器可由一次越界推导出别处条件恒真/恒假，删掉原本正确的边界检查 / 后果不局限于越界点，可能改变整个函数的行为 | **modify** | 证据一般（1个强信号/1个弱信号），建议modify为low待进一步验证 |
| ae-MIS-UB-004->ATOM-UB-GRAY-001::prop-2 | ATOM-UB-GRAY-001::prop-2 | UB 会去相关：优化器可由一次越界推导出别处条件恒真/恒假，删掉原本正确的边界检查 / 后果不局限于越界点，可能改变整个函数的行为 | **modify** | 证据一般（1个强信号/1个弱信号），建议modify为low待进一步验证 |

### MIS-UB-008（2 条边）

预标注分布：approve 0 / modify 2 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-UB-008->ATOM-UB-GRAY-001::prop-1 | ATOM-UB-GRAY-001::prop-1 | reinterpret_cast 的类型双关读违反严格别名规则 [basic.lval] → UB；优化器可重排读写顺序 / 正确做法是 std::bit_cast（C++20）或 memcpy（两者都是定义良好的位重解释） | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |
| ae-MIS-UB-008->ATOM-UB-GRAY-001::prop-2 | ATOM-UB-GRAY-001::prop-2 | reinterpret_cast 的类型双关读违反严格别名规则 [basic.lval] → UB；优化器可重排读写顺序 / 正确做法是 std::bit_cast（C++20）或 memcpy（两者都是定义良好的位重解释） | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |

### MIS-UB-012（2 条边）

预标注分布：approve 2 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-UB-012->ATOM-UB-GRAY-001::prop-1 | ATOM-UB-GRAY-001::prop-1 | 实参初始化是**不确定顺序**（indeterminately sequenced），只保证不重叠、不保证先后 / 实测 GCC 输出 h/g（右→左）、Clang 输出 g/h（左→右）——连编译器之间都相反 | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-UB-012->ATOM-UB-GRAY-001::prop-2 | ATOM-UB-GRAY-001::prop-2 | 实参初始化是**不确定顺序**（indeterminately sequenced），只保证不重叠、不保证先后 / 实测 GCC 输出 h/g（右→左）、Clang 输出 g/h（左→右）——连编译器之间都相反 | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |

### MIS-UB-013（2 条边）

预标注分布：approve 2 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-UB-013->ATOM-UB-GRAY-001::prop-1 | ATOM-UB-GRAY-001::prop-1 | C++17（P0145R3）把**函数实参初始化**从 unsequenced 改为 indeterminately sequenced → 该式在 C++17 起是 unspecified / 而运算符操作数仍为 unsequenced，... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |
| ae-MIS-UB-013->ATOM-UB-GRAY-001::prop-2 | ATOM-UB-GRAY-001::prop-2 | C++17（P0145R3）把**函数实参初始化**从 unsequenced 改为 indeterminately sequenced → 该式在 C++17 起是 unspecified / 而运算符操作数仍为 unsequenced，... | **approve** | 证据较充分（2个强信号），建议approve，可信度medium |

### MIS-UB-014（2 条边）

预标注分布：approve 0 / modify 2 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-UB-014->ATOM-UB-GRAY-001::prop-1 | ATOM-UB-GRAY-001::prop-1 | C++17（P0145R3）把实参初始化从 unsequenced 改为 **indeterminately sequenced**（[expr.call]）：不保证先后，但**绝不允许重叠** → 是 unspecified，不是 UB ... | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |
| ae-MIS-UB-014->ATOM-UB-GRAY-001::prop-2 | ATOM-UB-GRAY-001::prop-2 | C++17（P0145R3）把实参初始化从 unsequenced 改为 **indeterminately sequenced**（[expr.call]）：不保证先后，但**绝不允许重叠** → 是 unspecified，不是 UB ... | **modify** | 证据有一定支撑（1个强信号）但不够充分，建议modify为medium，需进一步验证 |

### MIS-UB-015（2 条边）

预标注分布：approve 2 / modify 0 / reject 0

| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |
|---|---|---|---|---|
| ae-MIS-UB-015->ATOM-UB-GRAY-001::prop-1 | ATOM-UB-GRAY-001::prop-1 | 实测 GCC 输出 h/g（右→左）、Clang 输出 g/h（左→右）——**两个编译器选了相反顺序**，这恰恰证明顺序未被规定，而不是被规定 / 可移植性依赖的是标准给出的**合法结果集合**，不是抽样一致；实现一致随时可能随版本变化（... | **approve** | 证据较充分（4个强信号），建议approve，可信度medium |
| ae-MIS-UB-015->ATOM-UB-GRAY-001::prop-2 | ATOM-UB-GRAY-001::prop-2 | 实测 GCC 输出 h/g（右→左）、Clang 输出 g/h（左→右）——**两个编译器选了相反顺序**，这恰恰证明顺序未被规定，而不是被规定 / 可移植性依赖的是标准给出的**合法结果集合**，不是抽样一致；实现一致随时可能随版本变化（... | **approve** | 证据较充分（4个强信号），建议approve，可信度medium |

## 一键执行脚本（人确认后使用）

确认以上预标注后，可以用以下命令批量执行：

```bash
# 仅执行 approve 建议（需逐条确认后取消注释）
# for edge in $(grep 'approve' data/human_review_pre_annotation_609.md | grep -o 'ae-[^|]*' | head -1); do
#   .venv/Scripts/python.exe tools/human_review_cli.py approve "$edge" --reason "AI预标注approve，人审确认"
# done
```

**注意**：不建议直接批量执行，应逐条核实后执行。AI 预标注的误判率未知，需人审把关。

---

*生成时间：2026-09-20 | 生成工具：AI 预标注脚本 | 数据来源：data/attack_edges_609.json（388条）*