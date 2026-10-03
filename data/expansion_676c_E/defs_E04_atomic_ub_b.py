#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E04_atomic_ub_b.py — atomic_ub 缺陷 E059..E075（17 个）。"""
from _dsl import S

# ---------------------------------------------------------------- E059
S("E059", "atomic_ub", "high", "catch", ["asan"], 2, 5, "worker",
  "栈上的 atomic 对象生命周期结束后仍被另一线程访问",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<bool>* g_at = nullptr;
static std::atomic<bool> escaped{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void publish_and_die(){
  wait_go();
  /*DEFECT: 把一个「生命周期由自己管理」的 atomic 裸指针交给别的线程，
     却不 prolong 它的生命周期：发布之后立刻 delete，
     另一线程对它的访问就变成对已结束对象的访问（UB，dangling atomic） */
  g_at = new std::atomic<bool>(true);
  escaped.store(true, std::memory_order_release);
  delete g_at;
}
static void worker(){
  wait_go();
  while(!escaped.load(std::memory_order_acquire)){}
  /*DEFECT: 通过悬垂的 std::atomic<bool>* 读取一个生命周期已结束的原子对象 → heap-use-after-free */
  std::atomic<bool>* p = reinterpret_cast<std::atomic<bool>*>(g_at);
  std::printf("E059 v=%d\n", (int)p->load(std::memory_order_relaxed));
}
int main(){
  std::thread a(publish_and_die), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；发布者 delete 原子对象后，另一线程仍通过裸指针访问它",
  "原子对象生命周期竞态。ASan 的 heap-use-after-free 可稳定捕获 → 预期 catch。")

# ---------------------------------------------------------------- E060
S("E060", "atomic_ub", "high", "catch", ["asan", "tsan"], 2, 5, "releaser",
  "堆上 atomic 在其它线程还在自旋轮询时被 delete",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int>* cell = nullptr;
static std::atomic<bool> made{false}, quit{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void poller(){
  wait_go();
  while(!made.load(std::memory_order_acquire)){}
  while(!quit.load(std::memory_order_acquire)){
    /*DEFECT: 轮询一个可能已经被 delete 的 atomic 对象 → heap-use-after-free*/
    if (cell->load(std::memory_order_relaxed) == 42) break;
  }
}
static void releaser(){
  wait_go();
  /*DEFECT: 在 poller 还在通过 cell 访问时 delete cell：原子对象生命周期未结束即被销毁 */
  delete cell;
  cell = nullptr;
  quit.store(true, std::memory_order_release);
}
int main(){
  cell = new std::atomic<int>(0);
  made.store(true, std::memory_order_release);
  std::thread a(poller), b(releaser);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；一个 delete 原子对象，另一个正在读它",
  "原子对象生命周期竞态。ASan heap-use-after-free → 预期 catch。")

# ---------------------------------------------------------------- E061
S("E061", "atomic_ub", "high", "miss", ["tsan"], 2, 5, "inc",
  "用 load + store 模拟 RMW（丢失更新）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> n{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void inc(){
  wait_go();
  for (int i = 0; i < 1000; ++i){
    /*DEFECT: x = x.load() + 1 不是原子的读-改-写：两次操作之间可被插入，计数必然丢失更新（应用 fetch_add）*/
    int v = n.load(std::memory_order_relaxed);
    n.store(v + 1, std::memory_order_relaxed);
  }
}
int main(){
  std::thread a(inc), b(inc);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E061 n=%d\n", n.load());
  return 0;
}
''',
  "两线程并发自增同一原子计数",
  "丢失更新。两次访问都是 atomic 操作，TSan 不报竞争 → 预期 miss（真实盲区）。")

# ---------------------------------------------------------------- E062
S("E062", "atomic_ub", "high", "miss", ["tsan"], 2, 5, "bump2",
  "读-改-写序列中混入非原子成员赋值，破坏原子性保证",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Score { std::atomic<int> hi; int lo; };
static Score s{0, 0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void bump2(){
  wait_go();
  /*DEFECT: 复合更新里 hi 用 fetch_add（原子）而 lo 直接赋值（非原子）且读改写未同步：状态可能被撕裂成 hi/lo 不一致 */
  s.hi.fetch_add(1, std::memory_order_relaxed);
  s.lo = s.lo + 1;
}
int main(){
  std::thread a(bump2), b(bump2), c(bump2);
  go.store(true, std::memory_order_release);
  a.join(); b.join(); c.join();
  std::printf("E062 hi=%d lo=%d\n", s.hi.load(), s.lo);
  return 0;
}
''',
  "3 线程并发更新同一结构体（原子+非原子混合）",
  "非原子成员 lo 存在真实竞争，TSan 可捕获；但 lo 读改写极短，命中率不定 → 标注预期 catch 并说明。")

# ---------------------------------------------------------------- E063
S("E063", "atomic_ub", "high", "miss", ["tsan"], 2, 5, "swap_role",
  "CAS 的 expected 变量同时被另一处原子写改写，导致比较对象漂移",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> state{0};
static std::atomic<int> expected_shadow{0};
static int swaps = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void swap_role(int id){
  wait_go();
  int expected = state.load(std::memory_order_relaxed);
  expected_shadow.store(expected, std::memory_order_relaxed);
  /*DEFECT: expected 是被其它线程间接影响的共享计算结果：CAS 的比较基准在「读」与「比较」之间不是稳定快照，
     角色交换的互斥语义不成立 */
  if (state.compare_exchange_strong(expected, id, std::memory_order_acq_rel))
    swaps++;
}
int main(){
  std::thread a(swap_role, 1), b(swap_role, 2);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E063 swaps=%d state=%d\n", swaps, state.load());
  return 0;
}
''',
  "两线程并发做角色交换",
  "CAS 基准不稳定属逻辑缺陷。预期 miss。")

# ---------------------------------------------------------------- E064
S("E064", "atomic_ub", "medium", "miss", ["tsan"], 2, 5, "state_machine",
  "状态机混用 exchange 与 CAS，转换表不完整",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
enum St { IDLE = 0, RUNNING = 1, DONE = 2 };
static std::atomic<int> st{IDLE};
static int transitions = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void advance(){
  wait_go();
  /*DEFECT: 用 exchange 无条件覆盖状态（不做前置状态校验），与另一个线程的 CAS 转换互相踩踏：状态机可从 DONE 退回 RUNNING */
  int prev = st.exchange(RUNNING, std::memory_order_acq_rel);
  if (prev == IDLE) transitions++;
  int exp = RUNNING;
  st.compare_exchange_strong(exp, DONE, std::memory_order_acq_rel);
  transitions++;
}
int main(){
  std::thread a(advance), b(advance);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E064 st=%d transitions=%d\n", st.load(), transitions);
  return 0;
}
''',
  "两线程并发推进同一状态机",
  "状态机转换不完整。预期 miss。")

# ---------------------------------------------------------------- E065
S("E065", "atomic_ub", "high", "catch", ["asan"], 6, 5, "indexer",
  "无符号原子下溢后作为数组下标使用",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int cells[4] = {1, 2, 3, 4};
static std::atomic<unsigned> idx{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void indexer(){
  wait_go();
  /*DEFECT: 无符号 fetch_sub 在 0 处回绕成巨大值，直接当下标 → 数组越界访问（UB）*/
  unsigned i = idx.fetch_sub(1, std::memory_order_relaxed);
  std::printf("E065 cells=%d\n", cells[i]);
}
int main(){
  idx.store(2, std::memory_order_relaxed);
  std::thread a(indexer), b(indexer), c(indexer), d(indexer), e(indexer), f(indexer);
  go.store(true, std::memory_order_release);
  a.join(); b.join(); c.join(); d.join(); e.join(); f.join();
  return 0;
}
''',
  "6 线程并发递减下标（起始 2），必然越过 0 发生无符号回绕",
  "无符号回绕成巨型下标。6 个线程从 2 开始递减，第 3 次就下溢 ⇒ ASan 稳定捕获越界 → 预期 catch。")

# ---------------------------------------------------------------- E066
S("E066", "atomic_ub", "high", "miss", ["ubsan"], 1, 5, "ramp",
  "std::atomic<signed char> 的 fetch_add 溢出",
  r'''
#include <atomic>
#include <cstdio>
int main(){
  std::atomic<signed char> tiny{100};
  /*DEFECT: atomic<signed char> 连续 fetch_add 越过 127：有符号原子算术溢出在 C++17 是 UB */
  for (int i = 0; i < 100; ++i) tiny.fetch_add(1, std::memory_order_relaxed);
  std::printf("E066 tiny=%d\n", (int)tiny.load());
  return 0;
}
''',
  "单线程把有符号字符原子加到溢出",
  "预期 miss：UBSan 不插桩 atomic RMW。")

# ---------------------------------------------------------------- E067
S("E067", "atomic_ub", "medium", "miss", ["asan"], 2, 5, "copy_lock",
  "用 memcpy 复制含 atomic_flag 的锁对象，锁状态被复制成两份",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
#include <cstring>
struct SpinLock {
  std::atomic_flag f = ATOMIC_FLAG_INIT;
  int counter = 0;
};
static std::atomic<bool> g_go{false};
static void wait_go(){ while(!g_go.load(std::memory_order_acquire)){} }
static void worker(SpinLock* dst){
  wait_go();
  /*DEFECT: memcpy 复制含 atomic_flag 的对象：两个锁实例共享同一份「被占用」状态拷贝，互斥完全失效 */
  SpinLock copy;
  std::memcpy(&copy, dst, sizeof(SpinLock));
  while (copy.f.test_and_set(std::memory_order_acquire)){}
  copy.counter++;
  copy.f.clear(std::memory_order_release);
}
int main(){
  SpinLock lk;
  std::thread a(worker, &lk), b(worker, &lk);
  g_go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E067 counter=%d\n", lk.counter);
  return 0;
}
''',
  "两线程并发 memcpy 复制同一个锁对象",
  "复制含原子对象的对象。属 UB 但无检测器；counter 竞争窗口窄 → 预期 miss。")

# ---------------------------------------------------------------- E068
S("E068", "atomic_ub", "high", "miss", ["asan"], 2, 5, "reinit",
  "对仍在被其它线程使用的 atomic 对象做 placement-new 重新初始化",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
#include <new>
static std::atomic<long> shared{0};
static std::atomic<bool> go{false}, stop{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void reset_once(){
  wait_go();
  /*DEFECT: 对一个已有生命周期的原子对象重新 placement-new 覆盖：旧对象的生命周期未结束即被销毁，
     另一线程正在进行的 load/store 变成对已结束对象的访问（UB） */
  new (&shared) std::atomic<long>(0);
}
static void spinner(){
  wait_go();
  long acc = 0;
  while (!stop.load(std::memory_order_acquire))
    acc += shared.load(std::memory_order_relaxed);
  std::printf("E068 acc=%ld\n", acc);
}
int main(){
  std::thread a(reset_once), b(spinner);
  go.store(true, std::memory_order_release);
  std::this_thread::sleep_for(std::chrono::milliseconds(20));
  stop.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；一个重新初始化原子对象，另一个持续读它",
  "对象生命周期被并发结束。ASan 未必命中（地址复用），TSan 可能报竞争 → 标注预期 miss 并说明。")

# ---------------------------------------------------------------- E069
S("E069", "atomic_ub", "high", "catch", ["asan"], 2, 5, "take_owned",
  "原子指针指向的对象被 delete 后，另一线程经 CAS 取出并使用",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Item { int id; int weight; };
static std::atomic<Item*> head{nullptr};
static std::atomic<bool> seeded{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void retire(){
  wait_go();
  Item* old = head.exchange(nullptr, std::memory_order_acq_rel);
  /*DEFECT: 换出后立刻 delete，但 head 这个「唯一的发布点」没有版本/生命周期保护：
     另一线程可能已在此之前读到同一个指针并准备 CAS 取出它 */
  delete old;
}
static void take(){
  wait_go();
  while(!seeded.load(std::memory_order_acquire)){}
  Item* exp = head.load(std::memory_order_acquire);
  if (exp != nullptr && head.compare_exchange_strong(exp, nullptr, std::memory_order_acq_rel)){
    /*DEFECT: CAS 成功不代表对象仍存活：retire() 可能刚刚 delete 了它 → heap-use-after-free */
    std::printf("E069 weight=%d\n", exp->weight);
  }
}
int main(){
  head.store(new Item{1, 5}, std::memory_order_release);
  seeded.store(true, std::memory_order_release);
  std::thread a(retire), b(take);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；一个 delete 原子指针指向的对象，另一个 CAS 取出",
  "取用与回收竞态导致 UAF。ASan 稳定捕获 → 预期 catch。")

# ---------------------------------------------------------------- E070
S("E070", "atomic_ub", "high", "miss", ["tsan"], 2, 5, "peel",
  "CAS 循环用常量 expected 反复重试，无法取得进展",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> cell{0};
static int peeled = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void peel(){
  wait_go();
  for (int round = 0; round < 4; ++round){
    /*DEFECT: 循环里 expected 永远是常量 0：cell 被别人改成 1 后再也 CAS 不回来，逻辑上丢失了 peel 机会 */
    int expected = 0;
    if (cell.compare_exchange_weak(expected, 2, std::memory_order_acq_rel)) peeled++;
  }
  std::printf("E070 peeled=%d\n", peeled);
}
int main(){
  std::thread a(peel), b(peel);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E070 cell=%d\n", cell.load());
  return 0;
}
''',
  "两线程并发 CAS 同一原子，expected 固定为常量",
  "CAS 重试基准错误。预期 miss。")

# ---------------------------------------------------------------- E071
S("E071", "atomic_ub", "high", "miss", ["asan", "ubsan"], 1, 5, "flag_on_stack",
  "在未初始化的栈缓冲区上直接使用 atomic_flag（缺 ATOMIC_FLAG_INIT）",
  r'''
#include <atomic>
#include <cstdio>
int main(){
  alignas(8) unsigned char raw[sizeof(std::atomic_flag) * 2];
  /*DEFECT: 直接把未初始化字节当作 atomic_flag 使用（缺 placement-new + ATOMIC_FLAG_INIT）：
     对未初始化内存做 test_and_set 是 UB */
  std::atomic_flag* f = reinterpret_cast<std::atomic_flag*>(raw);
  if (f->test_and_set(std::memory_order_acquire)) std::printf("E071 busy\n");
  f->clear(std::memory_order_release);
  std::printf("E071 ok\n");
  return 0;
}
''',
  "单线程在未初始化栈内存上使用 atomic_flag",
  "未初始化内存当原子对象用是 UB。ASan 不会报（栈内），→ 预期 miss。")

# ---------------------------------------------------------------- E072
S("E072", "atomic_ub", "high", "miss", ["ubsan"], 2, 5, "push_side_effect",
  "通过 const_cast 绕过 const 原子对象写保护",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static const std::atomic<int> cfg{5};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void push_side_effect(){
  wait_go();
  /*DEFECT: const_cast 去掉 const 后对「本来就是 const 的原子对象」做 store：
     该对象可能被放在只读段里，写它是 UB（对 const 对象的非 const 访问）*/
  std::atomic<int>* p = const_cast<std::atomic<int>*>(&cfg);
  p->store(9, std::memory_order_relaxed);
}
int main(){
  std::thread a(push_side_effect);
  go.store(true, std::memory_order_release);
  a.join();
  std::printf("E072 cfg=%d\n", cfg.load());
  return 0;
}
''',
  "单线程对 const 原子对象做 const_cast 写",
  "对 const 对象的写入是 UB。若放只读段 ASan 可报，否则无检测器 → 标注预期 miss。")

# ---------------------------------------------------------------- E073
S("E073", "atomic_ub", "high", "miss", ["tsan"], 2, 5, "on_signal",
  "在「类信号处理」语境里用非 lock-free 原子的自增",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
#include <csignal>
static std::atomic<long> tick{0};
static volatile int sig_seen = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
extern "C" void on_alarm(int){ sig_seen = 1; }   // 类信号处理：只碰 sig_seen
static void counter(){
  wait_go();
  /*DEFECT: 把「中断/信号上下文会做的事」搬进普通线程却用非 lock-free 原子做长自增：
     atomic 自增只在 lock-free 时才保证异步上下文安全，本类含非原子后备实现 → 潜在死锁（不保证可重入）*/
  for (int i = 0; i < 100000; ++i) tick.fetch_add(1, std::memory_order_relaxed);
}
int main(){
  std::signal(SIGINT, on_alarm);
  std::thread a(counter);
  go.store(true, std::memory_order_release);
  a.join();
  std::printf("E073 tick=%ld sig=%d\n", tick.load(), sig_seen);
  return 0;
}
''',
  "单线程高频原子自增，模拟中断上下文的原子使用",
  "原子操作的异步上下文安全性依赖 is_lock_free，C++17 起标准不再保证。预期 miss（无检测器）。")

# ---------------------------------------------------------------- E074
S("E074", "atomic_ub", "high", "catch", ["asan", "ubsan"], 2, 5, "shift_ptr_int",
  "把原子指针的位运算结果当指针存回并解引用",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int cell = 1;
static std::atomic<unsigned long long> raw{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void shifter(){
  wait_go();
  /*DEFECT: 把对象地址当整数塞进 atomic<unsigned long long> 再做位运算后 reinterpret 回指针：
     整数上不满足指针对齐/表示要求，转回指针解引用是 UB */
  unsigned long long a = reinterpret_cast<unsigned long long>(&cell);
  raw.store((a << 1) | 1ULL, std::memory_order_relaxed);
}
static void dereferencer(){
  wait_go();
  while (raw.load(std::memory_order_relaxed) == 0ULL){}
  /*DEFECT: 由整数位运算结果构造指针并解引用 → 非法指针解引用（UB）*/
  int* p = reinterpret_cast<int*>(static_cast<unsigned long long>(raw.load(std::memory_order_relaxed)));
  std::printf("E074 cell=%d\n", *p);
}
int main(){
  std::thread a(shifter), b(dereferencer);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；整数位运算结果被当作指针解引用",
  "非法指针解引用。ASan 通常会捕获（wild pointer）但地址落在映射区外时可能 segfault 而非报告 → 标注预期 miss。")

# ---------------------------------------------------------------- E075
S("E075", "atomic_ub", "high", "catch", ["asan", "tsan"], 2, 5, "mutate_and_cas",
  "CAS 只比较指针，指针指向的结构体内容被并发改写（伪原子快照）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Rec { int key; int val; char pad[8]; };
static std::atomic<Rec*> slot{nullptr};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void mutator(){
  wait_go();
  Rec* r = new Rec{5, 0, "abcdefg"};
  slot.store(r, std::memory_order_relaxed);
  ready.store(true, std::memory_order_release);
  /*DEFECT: 结构体内容在「发布」之后仍被非原子地改写：CAS/load 只能原子地取指针，取不到内容快照*/
  r->val = 99;
  r->key = 6;
}
static void cas_user(){
  wait_go();
  while(!ready.load(std::memory_order_acquire)){}
  Rec* exp = slot.load(std::memory_order_acquire);
  if (slot.compare_exchange_strong(exp, nullptr, std::memory_order_acq_rel)){
    /*DEFECT: 读到的 key/val 来自一次「非原子的多字段读」，可能撕裂；这里再把已释放风险叠加进来*/
    std::printf("E075 key=%d val=%d\n", exp->key, exp->val);
    delete exp;
  }
}
int main(){
  std::thread a(mutator), b(cas_user);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；一方在发布后继续改写内容，另一方 CAS 取出并读取",
  "伪原子快照 + 双重所有权。竞争真实（key/val 非原子读写）→ 预期 TSan catch；ASan 可能报双删。")
