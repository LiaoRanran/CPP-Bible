# 693-A2 · 校准题（10 条）+ 答案

- 用途：正式裁决 `693_human_adjudication_package.csv` **之前**先做完这 10 条，再对答案。
- 结构：**C01–C05 有确定答案**（A 侧实测与 B 侧静态判读**一致**，双重支撑）；
  **C06–C10 是真实分歧条目，不提供单一答案**——它们的作用是把你校准到"分歧长什么样"，
  正式裁决时你会遇到同样的题型。
- 答案在文末 §3。**做完再看。**

---

## 1. 题目

### C01（类型：`memory_leak`）
```cpp
#include <cstdio>
int* make() { return new int(1); }       // 调用方需 delete
int main(){ int* p = make(); std::printf("%d\n", *p); /* 漏 delete */ }
```

### C02（类型：`data_race`）
```cpp
#include <thread>
int g = 0;
void inc(){ for(int i=0;i<100000;++i) ++g; }   // 非原子、非加锁
int main(){ std::thread a(inc), b(inc); a.join(); b.join(); }
```

### C03（类型：`out_of_bounds`）
```cpp
#include <cstring>
#include <cstdio>
int main(){ char buf[4]; std::strcpy(buf, "0123456789"); std::printf("%s\n", buf); return 0; }
```

### C04（类型：`virtual_function`）
```cpp
#include <cstdio>
struct B { B(){ vf(); } virtual void vf(){ printf("B\n"); } };
struct D : B { void vf() override { printf("D\n"); } };
int main(){ D d; return 0; }
```

### C05（类型：`algorithm_misuse`）
```cpp
#include <vector>
#include <algorithm>
#include <cstdio>
int main() {
  std::vector<int> v = {5, 3, 1, 4, 2};
  auto it = std::lower_bound(v.begin(), v.end(), 3);
  std::printf("%d\n", (int)(it - v.begin()));
  return 0;
}
```

### C06（类型：`strict_aliasing`）—— 分歧条目
```cpp
int f(float*p){*(int*)p=1;return (int)*p;}
int main(){float x=0;return f(&x);}
```
> A（实测）= `miss`；B（静态）= `catch`。

### C07（类型：`double_free`）—— 分歧条目
```cpp
int main(){int* p=new int(1);delete p;delete p;return 0;}
```
> A（实测）= `miss`；B（静态）= `catch`。
> 提示：注意这段代码的返回值与 `main` 结束前是否还有对该内存的**可观测**使用。

### C08（类型：`integer_overflow`）—— 分歧条目
```cpp
#include <cstdio>
int main(){int x=2147483647;x+=1;std::printf("%d\n",x);}
```
> A（实测）= `miss`；B（静态）= `catch`。

### C09（类型：`linker_odr`）—— 分歧条目
```cpp
// [redacted]
#define ODR_VALUE 1
#include "S016_dep_c24a0d9d.h"

int tu_a_value() { return odr_fn(); }
int tu_a_stable() { return stable_fn(); }
```
```cpp
// S016_dep_c24a0d9d.h
#ifndef ODR_VALUE
#define ODR_VALUE 1
#endif
inline int odr_fn() { return ODR_VALUE; }
inline int stable_fn() { return 42; }
```
> A（实测）= `catch`；B（静态）= `unknown`。
> 提示：ODR 违反需要**两个 TU** 才能成立。

### C10（类型：`other_ub`）—— 分歧条目
```cpp
#include <cstdio>
int bump(int& x){ return ++x; }
int show(int a, int b){ return a * 10 + b; }
int main(){ int i = 0; std::printf("%d\n", show(bump(i), bump(i))); return 0; }
```
> A（实测）= `catch`；B（静态）= `miss`。

---

## 2. 请先写下你的答案（四态之一）

| 题 | 你的答案 |
|---|---|
| C01 | |
| C02 | |
| C03 | |
| C04 | |
| C05 | |
| C06 | |
| C07 | |
| C08 | |
| C09 | |
| C10 | |

---

## 3. 答案与讲解

### C01 = `catch`
`new int(1)` 没有配对的 `delete` ⇒ **LSan（asan 的泄漏检测组件）在进程退出时报告**。
判据是"有没有报告"，不是"泄漏严不严重"。即使泄漏 4 字节也报。

### C02 = `catch`
两个线程无同步地对同一非原子 `int g` 做 `++`（读-改-写）⇒ **TSan 报 data race**。
注意：`g++` 的竞态在 TSan 下命中率很高（100k 次迭代足够），不要因为"可能碰巧没撞上"就判 miss。

### C03 = `catch`
`strcpy` 写 11 字节（含 NUL）到 `char buf[4]` ⇒
**ASan 报 stack-buffer-overflow**；同时 GCC 的 `-Wstringop-overflow=` 也会告警。双重命中。

### C04 = `miss`
**这是陷阱题。** 在构造函数里调用虚函数是**良定义**的：此时动态类型是 `B`，
解析到 `B::vf()`，程序输出 `B\n`。没有 UB，没有告警，没有 sanitizer 报告。
⇒ "看起来危险" ≠ "会检出"。

### C05 = `miss`
`std::lower_bound` 要求区间**已按同一比较器划分**；`{5,3,1,4,2}` 未排序 ⇒ 标准上确实是 UB。
**但是**：ASan/UBSan/TSan 都不检查算法前置条件，编译器也不告警（区间在编译期不可知）。
⇒ 这是"真实 UB 但八资产全静默"的典型 ⇒ **`miss`**。

### C06 —— 不设标准答案（A=`miss`，B=`catch`）
- B 的理由：C 风格强转后解引用，GCC `-Wstrict-aliasing`（-Wall 默认 level 3）会报
  "dereferencing type-punned pointer will break strict-aliasing rules"。
- A 的实测：无报告。
- **裁决要点**：`compiler-warn` 资产的**具体告警档**是什么？如果只用 `-Wall` 而 GCC 版本/优化档
  使该告警未触发，则 `miss` 成立；若告警档含 `-Wstrict-aliasing=2` 则 `catch` 成立。
  请把你依据的告警档写进 `human_note`。

### C07 —— 不设标准答案（A=`miss`，B=`catch`）
- B 的理由：二次 `delete` ⇒ ASan `double-free`。
- A 的实测：无报告。
- **裁决要点**：**编译器优化会消除缺陷**。这个 `main` 在 `delete p` 之后不再使用 `p`，
  整段分配/释放在 `-O2` 下是**死代码**，可被完全删除 ⇒ ASan 没有机会报告。
  这正是本项目"环境敏感性与静默降级"研究的核心现象之一。
  判 `catch` 的人请在 note 说明"我按源码语义判，不考虑优化消除"；
  判 `miss` 的人请说明"我按 -O2 实测判"。**两种都对，口径必须写清。**

### C08 —— 不设标准答案（A=`miss`，B=`catch`）
- B 的理由：`INT_MAX + 1` 有符号溢出 ⇒ UBSan `signed-integer-overflow`。
- A 的实测：无报告。
- **裁决要点**：**常量折叠**。编译器在编译期就把 `x` 折成 `-2147483648`，
  运行期不再有那个"会溢出的加法指令"，UBSan 插桩的检查点也随之消失。
  与 C07 同属"优化消除"家族，但机制不同（折叠 vs 死代码删除）。

### C09 —— 不设标准答案（A=`catch`，B=`unknown`）
- A 的实测：检出（多 TU 组完整存在时，链接后两 TU 对 `odr_fn` 定义不同 ⇒ ODR 违反）。
- B 的静态判读：材料包**只给了 TU A**，没有第二个 TU，也没有链接顺序 ⇒ 无法判定。
- **裁决要点**：这是 `unknown` 的正当用法。若你认为"材料不足以判定" ⇒ `unknown`；
  若你按"该样本所属的多 TU 夹具在仓内确实存在第二 TU"补全上下文 ⇒ `catch`。
  **请把你是否自行补全了上下文写进 note**——这直接影响 κ 的可解释性。

### C10 —— 不设标准答案（A=`catch`，B=`miss`）
- B 的理由：两个 `bump(i)` 的求值顺序 **unspecified**，不是 UB（每个 `bump` 内部对 `i` 的
  修改与其他实参求值之间有函数调用引入的 sequenced-before）⇒ 无 UB、无告警。
- A 的实测：检出。
- **裁决要点**：unspecified 与 UB 的边界。B 按 ISO C++ 语义判 `miss`；
  A 侧实测为 `catch`，可能是某一编译器在该形态下发了 `-Wsequence-point`-类告警，
  也可能是 A 侧标签本身需要复核。**如果你认为 A 侧标签可疑，请直接写在 `human_note`**——
  裁决的目的正是发现这个。

---

## 4. 校准判读

- C01–C05 错 ≥2 条 ⇒ 请回读 `693_annotation_guide.md` §2（四态）与 §5（边界）再开始正式裁决。
- C06–C10 "没有标准答案"的题，只要你在 note 里写清了**判定口径**，任何四态取值都是有效裁决。
- 校准的价值不在"和答案一致"，而在**让你的口径在整个 31 条里保持一致**。
