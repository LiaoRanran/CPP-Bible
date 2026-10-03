#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E03_atomic_ub_a.py — atomic_ub 缺陷 E041..E058（18 个）。

覆盖变体：未初始化原子、CAS 误用、fetch_* 溢出、atomic 指针算术、
atomic_flag、生命周期失效、误用内存序。
"""
from _dsl import S

# ---------------------------------------------------------------- E041
S("E041", "atomic_ub", "high", "miss", ["ubsan", "asan"], 1, 5, "worker",
  "局部 std::atomic<int> 默认初始化（值不确定）后直接 fetch_add",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<bool> go{false};
int main(){
  std::atomic<int> x;                 /* 故意不给初值：默认构造是 trivial，x 的值不确定 */
  std::thread t([&]{
    while(!go.load(std::memory_order_acquire)){}
    /*DEFECT: 从不确定值开始 fetch_add：读取未初始化原子的值是 UB（C++17 下 atomic 构造不做值初始化）*/
    x.fetch_add(1, std::memory_order_relaxed);
  });
  go.store(true, std::memory_order_release);
  t.join();
  std::printf("E041 x=%d\n", x.load(std::memory_order_relaxed));
  return 0;
}
''',
  "单线程线程中读取未初始化原子的值",
  "未初始化原子是真实 UB，但没有任何 sanitizer 会为「原子的不确定初值」设陷阱 → 预期 miss（真实盲区）。")

# ---------------------------------------------------------------- E042
S("E042", "atomic_ub", "high", "miss", ["asan"], 1, 5, "worker",
  "堆上 new std::atomic<int> 未值初始化即参与运算",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
int main(){
  /*DEFECT: new std::atomic<int> 走默认构造（trivial），对象的值不确定；下面直接参与 RMW 是 UB*/
  std::atomic<int>* p = new std::atomic<int>();
  std::thread t([p]{
    int old = p->fetch_add(5, std::memory_order_relaxed);
    std::printf("E042 old=%d\n", old);
  });
  t.join();
  delete p;
  return 0;
}
''',
  "单线程内对未值初始化原子做 RMW",
  "预期 miss：ASan 只管内存错误，不管未初始化值。")

# ---------------------------------------------------------------- E043
S("E043", "atomic_ub", "high", "miss", ["asan"], 2, 5, "step",
  "结构体成员原子未在构造函数中初始化即被读改写",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Meter {
  std::atomic<long> total;            // 构造函数未初始化
  int id;
  Meter(int i) : id(i) {}              // total 故意不初始化
};
static Meter m{1};
int main(){
  std::thread a([]{ m.total.fetch_add(3, std::memory_order_relaxed); });
  std::thread b([]{ /*DEFECT: 读改写一个从未初始化过的原子成员，起点值不确定 → UB*/ m.total.fetch_add(4, std::memory_order_relaxed); });
  a.join(); b.join();
  std::printf("E043 total=%ld\n", m.total.load(std::memory_order_relaxed));
  return 0;
}
''',
  "两线程对未初始化原子成员做 RMW",
  "类成员原子漏初始化。预期 miss（无对应检测器）。")

# ---------------------------------------------------------------- E044
S("E044", "atomic_ub", "high", "miss", ["tsan"], 2, 5, "claim",
  "compare_exchange_weak 失败后不检查 expected，直接拿它当新值用",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> owner{-1};
static int resource = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void claim(int id){
  wait_go();
  int expected = -1;
  if (owner.compare_exchange_weak(expected, id, std::memory_order_acq_rel)){
    resource = id;                     // 正常路径
    return;
  }
  /*DEFECT: CAS 失败后 expected 已被写成当前值，但这里仍把它当成「我拿到的资源编号」使用（未重新检查成功标志）*/
  resource = expected + 1000;
  std::printf("E044 loser saw=%d\n", expected);
}
int main(){
  std::thread a(claim, 1), b(claim, 2);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E044 resource=%d\n", resource);
  return 0;
}
''',
  "两线程竞争同一资源所有权，仅一方 CAS 成功",
  "CAS 失败路径误用 expected。无 sanitizer 覆盖 → 预期 miss。")

# ---------------------------------------------------------------- E045
S("E045", "atomic_ub", "high", "miss", ["tsan"], 2, 5, "try_acquire",
  "单次 compare_exchange_weak 失败即放弃（未放入循环）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> slot{0};
static int taken = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void try_acquire(){
  wait_go();
  int expected = 0;
  /*DEFECT: compare_exchange_weak 允许伪失败，此处不在循环里重试：一次伪失败就丢掉了资源*/
  if (slot.compare_exchange_weak(expected, 1, std::memory_order_acq_rel))
    taken = 1;
  else
    std::printf("E045 gave up (expected=%d)\n", expected);
}
int main(){
  std::thread a(try_acquire), b(try_acquire);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E045 taken=%d\n", taken);
  return 0;
}
''',
  "两线程并发尝试获取单一资源",
  "weak CAS 不循环。属逻辑 UB（伪失败未处理），无检测器 → 预期 miss。")

# ---------------------------------------------------------------- E046
S("E046", "atomic_ub", "low", "miss", ["tsan"], 2, 5, "bump",
  "compare_exchange_strong 用在循环里（该用 weak）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> version{0};
static int observed = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void bump(int want){
  wait_go();
  int expected = 0;
  /*DEFECT: 循环里用 strong 版：语义上没错，但 strong 不会伪失败，循环退化成「重试阻塞」，在高竞争下造成活锁式的忙等*/
  while (version.compare_exchange_strong(expected, want, std::memory_order_acq_rel))
    expected = 0;
  observed = want;
}
int main(){
  std::thread a(bump, 1), b(bump, 2);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E046 version=%d observed=%d\n", version.load(), observed);
  return 0;
}
''',
  "两线程竞争写同一原子版本号",
  "strong 用于循环属性能/活性缺陷而非 UB。无检测器 → 预期 miss（低severity）。")

# ---------------------------------------------------------------- E047
S("E047", "atomic_ub", "high", "miss", ["ubsan"], 1, 5, "reset",
  "compare_exchange 的失败序强于成功序（违反标准前置条件，UB）",
  r'''
#include <atomic>
#include <cstdio>
int main(){
  std::atomic<int> a{5};
  int expected = 5;
  /*DEFECT: 成功序是 memory_order_relaxed，失败序却给了 memory_order_acq_rel：
     标准要求失败序不得强于成功序，此处违反 compare_exchange 的前置条件 → UB */
  bool ok = a.compare_exchange_strong(expected, 9,
                                     std::memory_order_relaxed,
                                     std::memory_order_acq_rel);
  std::printf("E047 ok=%d a=%d\n", (int)ok, a.load());
  return 0;
}
''',
  "单线程调用违反前置条件的 compare_exchange",
  "内存序前置条件违规属 UB，但 libstdc++ 不做运行时检查，UBSan 也不覆盖 → 预期 miss（真实盲区）。")

# ---------------------------------------------------------------- E048
S("E048", "atomic_ub", "high", "miss", ["ubsan"], 2, 5, "bump",
  "std::atomic<int>::fetch_add 有符号溢出（C++17 下为 UB）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> counter{2147483000};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void bump(){
  wait_go();
  /*DEFECT: 对有符号 atomic<int> 连续 fetch_add 越过 INT_MAX：C++17 规定原子算术溢出为 UB（C++20 才定义为回绕）*/
  for (int i = 0; i < 1000; ++i) counter.fetch_add(100000, std::memory_order_relaxed);
}
int main(){
  std::thread a(bump), b(bump);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E048 counter=%d\n", counter.load());
  return 0;
}
''',
  "两线程并发把有符号原子计数推过 INT_MAX",
  "C++17 原子算术溢出是 UB；但 libstdc++ 硬件回绕且 UBSan 不插桩原子 RMW → 预期 miss（真实盲区）。")

# ---------------------------------------------------------------- E049
S("E049", "atomic_ub", "high", "miss", ["ubsan"], 1, 5, "drain",
  "std::atomic<long long>::fetch_sub 无符号下溢后当作合法计数使用",
  r'''
#include <atomic>
#include <cstdio>
int main(){
  std::atomic<long long> budget{10};
  /*DEFECT: fetch_sub 减到负数：对有符号原子做下溢是 UB（C++17），且负值随后被当作合法预算使用*/
  for (int i = 0; i < 25; ++i) budget.fetch_sub(1, std::memory_order_relaxed);
  std::printf("E049 budget=%lld\n", budget.load());
  return 0;
}
''',
  "单线程把有符号原子计数减到负数",
  "预期 miss：UBSan 不插桩 atomic RMW。")

# ---------------------------------------------------------------- E050
S("E050", "atomic_ub", "high", "miss", ["ubsan"], 2, 5, "scale",
  "std::atomic<short> fetch_mul 溢出（C++17 下为 UB）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<short> gain{1000};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void scale(){
  wait_go();
  /*DEFECT: 对 atomic<short> 连续 fetch_add 越过 SHRT_MAX：有符号原子算术溢出在 C++17 是 UB*/
  for (int i = 0; i < 200; ++i) gain.fetch_add(300, std::memory_order_relaxed);
}
int main(){
  std::thread a(scale), b(scale);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E050 gain=%d\n", (int)gain.load());
  return 0;
}
''',
  "两线程并发放大 short 原子计数直至溢出",
  "预期 miss：UBSan 不覆盖 atomic RMW 溢出。")

# ---------------------------------------------------------------- E051
S("E051", "atomic_ub", "high", "catch", ["asan"], 2, 5, "shift_ptr",
  "对 atomic<T*> 做指针算术后存回，越界解引用",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int table[4] = {10, 20, 30, 40};
static std::atomic<int*> cur{table};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void shifter(){
  wait_go();
  int* p = cur.load(std::memory_order_relaxed);
  /*DEFECT: 对原子指针做无边界检查的算术并写回：越出 table 的 4 个元素之外*/
  cur.store(p + 9, std::memory_order_relaxed);
}
static void reader(){
  wait_go();
  while (cur.load(std::memory_order_relaxed) == table){}
  /*DEFECT: 读侧直接解引用越界指针 → 越界访问*/
  std::printf("E051 v=%d\n", *cur.load(std::memory_order_relaxed));
}
int main(){
  std::thread a(shifter), b(reader);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；一方把原子指针推出数组边界，另一方解引用",
  "原子指针算术越界。ASan 的 global-buffer-overflow 可稳定捕获 → 预期 catch。")

# ---------------------------------------------------------------- E052
S("E052", "atomic_ub", "high", "catch", ["asan"], 2, 5, "publish_dangling",
  "把已 delete 的堆地址存进 atomic 指针，另一线程解引用",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int*> slot{nullptr};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void publish(){
  wait_go();
  int* h = new int(7);
  slot.store(h, std::memory_order_relaxed);
  ready.store(true, std::memory_order_release);
  /*DEFECT: 原子指针仍指向已释放的堆对象：把「已 delete 的地址」作为原子值发布出去，等于发布了悬垂指针*/
  delete h;
}
static void consume(){
  wait_go();
  while(!ready.load(std::memory_order_acquire)){}
  /*DEFECT: 解引用悬垂原子指针 → heap-use-after-free*/
  std::printf("E052 v=%d\n", *slot.load(std::memory_order_relaxed));
}
int main(){
  std::thread a(publish), b(consume);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；发布后立即 delete，消费者随后解引用",
  "原子指针悬垂。ASan 稳定捕获 → 预期 catch。")

# ---------------------------------------------------------------- E053
S("E053", "atomic_ub", "medium", "miss", ["tsan"], 2, 5, "signal",
  "atomic<bool>::exchange 的返回值被丢弃，信号丢失",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<bool> shutdown_req{false};
static int shutdowns = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void requester(){
  wait_go();
  /*DEFECT: exchange 的旧值（是否已有请求在途）被丢弃：并发两个请求者时后到者无法察觉信号已被消费*/
  shutdown_req.exchange(true, std::memory_order_acq_rel);
  shutdowns = shutdowns + 1;
}
int main(){
  std::thread a(requester), b(requester);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E053 req=%d count=%d\n", (int)shutdown_req.load(), shutdowns);
  return 0;
}
''',
  "两线程并发发停机请求",
  "exchange 返回值被忽略属逻辑缺陷。预期 miss。")

# ---------------------------------------------------------------- E054
S("E054", "atomic_ub", "medium", "miss", ["tsan"], 2, 5, "enter",
  "用 atomic<bool>::exchange 抢占独占权，忽略「已被占用」返回值",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<bool> busy{false};
static int critical_writes = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void enter(){
  wait_go();
  /*DEFECT: exchange 返回 true 说明锁已被别人占用，这里直接无视返回值继续写「临界区」→ 互斥失效*/
  busy.exchange(true, std::memory_order_acq_rel);
  critical_writes = critical_writes + 1;
  busy.store(false, std::memory_order_release);
}
int main(){
  std::thread a(enter), b(enter);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E054 writes=%d\n", critical_writes);
  return 0;
}
''',
  "两线程并发进入「临界区」",
  "exchange 返回值被忽略导致伪互斥。预期 miss。")

# ---------------------------------------------------------------- E055
S("E055", "atomic_ub", "high", "miss", ["tsan"], 2, 5, "guard",
  "atomic_flag 作为未初始化成员，test_and_set 前无原子状态建立",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Gate {
  std::atomic_flag f;                  // 未在构造函数中 ATOMIC_FLAG_INIT
  int payload;
  Gate() : payload(0) {}
};
static Gate g;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void guard(int id){
  wait_go();
  /*DEFECT: atomic_flag 从未 ATOMIC_FLAG_INIT：其状态不确定就进入自旋，行为未定义*/
  while (g.f.test_and_set(std::memory_order_acquire)){}
  g.payload = id;
  g.f.clear(std::memory_order_release);
}
int main(){
  std::thread a(guard, 1), b(guard, 2);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E055 payload=%d\n", g.payload);
  return 0;
}
''',
  "两线程并发进入未初始化的 atomic_flag 自旋锁",
  "atomic_flag 漏初始化。标准要求用 ATOMIC_FLAG_INIT；无检测器 → 预期 miss。")

# ---------------------------------------------------------------- E056
S("E056", "atomic_ub", "high", "miss", ["tsan"], 2, 5, "spin",
  "自旋锁的 test_and_set 与 clear 都用 relaxed，失去 acquire/release",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic_flag lock = ATOMIC_FLAG_INIT;
static int counter = 0;                // 非原子，受锁保护
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void worker(){
  wait_go();
  /*DEFECT: 获取与释放都用 relaxed：临界区内的写对其它线程无 happens-before，互斥形同虚设（数据竞争）*/
  while (lock.test_and_set(std::memory_order_relaxed)){}
  counter++;
  lock.clear(std::memory_order_relaxed);
}
int main(){
  std::thread a(worker), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E056 counter=%d\n", counter);
  return 0;
}
''',
  "两线程并发进入 relaxed 自旋锁保护的临界区",
  "自旋锁内存序过弱导致真实数据竞争，TSan 可捕获；但若竞争窗口太窄可能漏报，"
  "标注为预期 catch 并在 notes 里说明漏报可能。")

# ---------------------------------------------------------------- E057
S("E057", "atomic_ub", "high", "miss", ["ubsan"], 2, 5, "tweak",
  "把 std::atomic<int> 的引用绑到普通 int 上，当作原子操作使用",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int plain = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void bump_via_fake_atomic(){
  wait_go();
  /*DEFECT: 把普通 int 的地址强转成 std::atomic<int>* 并当原子变量自增：
     实际是对非原子对象做「假装原子」的 RMW，两线程间是真实数据竞争 + 违反对象类型规则（UB）*/
  std::atomic<int>* fake = reinterpret_cast<std::atomic<int>*>(&plain);
  fake->fetch_add(1, std::memory_order_relaxed);
}
int main(){
  std::thread a(bump_via_fake_atomic), b(bump_via_fake_atomic);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E057 plain=%d\n", plain);
  return 0;
}
''',
  "两线程并发对伪装成原子的普通变量做 RMW",
  "对非原子对象施加原子操作是 UB，且实为数据竞争。TSan 可能捕获（它按实际内存访问建模），"
  "但也可能因硬件 LOCK 前缀而无报告；标注预期 miss 并说明。")

# ---------------------------------------------------------------- E058
S("E058", "atomic_ub", "high", "miss", ["ubsan", "asan"], 2, 5, "work",
  "把 atomic<int> placement-new 到未对齐的地址上",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
#include <new>
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void work(int v){
  wait_go();
  /*DEFECT: 在 char 缓冲的 offset 1 处 placement-new 一个 alignof 为 4 的 atomic<int>：对象未对齐，访问是 UB */
  alignas(8) unsigned char buf[sizeof(std::atomic<int>) + 2];
  std::atomic<int>* a = new (buf + 1) std::atomic<int>(0);
  a->fetch_add(v, std::memory_order_relaxed);
  std::printf("E058 v=%d\n", a->load(std::memory_order_relaxed));
}
int main(){
  std::thread a(work, 1), b(work, 2);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程各自在未对齐地址上构造原子对象",
  "未对齐原子对象访问是 UB。libstdc++ 的原子 load/store 编译成普通 mov，"
  "UBSan 的 alignment 插桩不会命中 → 预期 miss（真实盲区）。")
