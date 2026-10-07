// ATOM-LANG-INLINE-001 夹具（多 TU 组）· 共享头
//
// [redacted]
// [redacted]
//   - 对照组 `stable_fn()`：两个 TU 看到**逐字相同**的定义 ⇒ 合规
// 命令行以 `-D` 传值亦可，但本夹具刻意用**文件内 `#define`**，让"两 TU 定义不同"是**源码事实**
// 而非编译参数差异（减少混淆变量）。
#pragma once

#ifndef ODR_VALUE
#define ODR_VALUE 1
#endif

// [redacted]
inline int odr_fn() { return ODR_VALUE; }

// 合规对照组：两 TU 定义逐字相同 ⇒ 无论链接顺序，行为必须一致（活性对照）
inline int stable_fn() { return 42; }
