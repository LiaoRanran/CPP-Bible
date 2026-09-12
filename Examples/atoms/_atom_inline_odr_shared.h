// ATOM-LANG-INLINE-001 夹具（多 TU 组）· 共享头
//
// 唯一变量：两个 TU 看到的 `odr_fn` 定义**是否逐字相同**（由 ODR_VALUE 宏在两个 .cpp 中分别定义）。
//   - 实验组 `odr_fn()`：TU A 看到 return 1、TU B 看到 return 2 ⇒ **违反 ODR**（定义不同）
//   - 对照组 `stable_fn()`：两个 TU 看到**逐字相同**的定义 ⇒ 合规
// 命令行以 `-D` 传值亦可，但本夹具刻意用**文件内 `#define`**，让"两 TU 定义不同"是**源码事实**
// 而非编译参数差异（减少混淆变量）。
#pragma once

#ifndef ODR_VALUE
#define ODR_VALUE 1
#endif

// 实验组：inline（外部链接，允许跨 TU 重复定义——ODR 例外的本体）
inline int odr_fn() { return ODR_VALUE; }

// 合规对照组：两 TU 定义逐字相同 ⇒ 无论链接顺序，行为必须一致（活性对照）
inline int stable_fn() { return 42; }
