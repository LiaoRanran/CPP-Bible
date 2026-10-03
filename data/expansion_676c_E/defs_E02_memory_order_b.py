#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E02_memory_order_b.py — memory_order 缺陷 E021..E040（20 个）。"""
from _dsl import S

# ---------------------------------------------------------------- E021
S("E021", "memory_order", "high", "catch", ["tsan"], 2, 5, "consumer",
  "以 relaxed 读布尔标志作为「数据可读」判据，随后读非原子字段",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Row { int a; int b; };
static Row g_row{0, 0};
static std::atomic<bool> filled{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void filler(){
  wait_go();
  g_row.a = 11; g_row.b = 22;
  filled.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  /*DEFECT: filled 用 relaxed 轮询：无 acquire 语义，随后读非原子 g_row 构成数据竞争*/
  while (!filled.load(std::memory_order_relaxed)){}
  std::printf("E021 a=%d b=%d\n", g_row.a, g_row.b);
}
int main(){
  std::thread f(filler), c(consumer);
  go.store(true, std::memory_order_release);
  f.join(); c.join();
  return 0;
}
''',
  "两线程并发；consumer 读非原子结构体",
  "结构体载荷 + relaxed 标志。竞争真实 → 预期 TSan catch。")

# ---------------------------------------------------------------- E022
S("E022", "memory_order", "high", "catch", ["tsan"], 2, 5, "get",
  "DCLP 中 relaxed 读实例指针 + 构造函数内的非原子字段写",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Registry { int slots[8]; int live; };
static std::atomic<Registry*> reg{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static Registry* get(){
  Registry* r = reg.load(std::memory_order_acquire);
  if (r == nullptr){
    r = new Registry{};
    for (int i = 0; i < 8; ++i) r->slots[i] = i;   // 非原子字段写
    r->live = 8;
    /*DEFECT: 二次检查用 relaxed；构造函数里的 slots/live 写与读线程之间无 synchronizes-with*/
    if (reg.load(std::memory_order_relaxed) == nullptr) reg.store(r, std::memory_order_release);
    else { delete r; r = reg.load(std::memory_order_relaxed); }
  }
  return r;
}
static void worker(){ wait_go(); Registry* r = get(); std::printf("E022 live=%d\n", r->live); }
int main(){
  std::thread a(worker), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发首次调用 get()，走 DCLP 慢路径",
  "DCLP + relaxed 二次检查，读线程可能看到未构造完的 slots/live → 预期 TSan catch。")

# ---------------------------------------------------------------- E023
S("E023", "memory_order", "medium", "miss", ["tsan"], 2, 5, "waiter",
  "以 relaxed 的 fetch_or 位标志作完成判据",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<unsigned> stage_bits{0};
static std::atomic<int> slots[4];
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void worker(int id){
  wait_go();
  slots[id].store(id * 10, std::memory_order_relaxed);
  /*DEFECT: 位标志用 relaxed fetch_or：waiter 若也 relaxed 读，两侧都不建立 happens-before*/
  stage_bits.fetch_or(1u << id, std::memory_order_relaxed);
}
static void waiter(){
  wait_go();
  /*DEFECT: relaxed 读位标志当完成判据：读到 0xF 不保证 slots 的写入已可见*/
  while (stage_bits.load(std::memory_order_relaxed) != 0xFu){}
  std::printf("E023 s3=%d\n", slots[3].load(std::memory_order_relaxed));
}
int main(){
  std::thread a(worker, 0), b(worker, 1), c(worker, 2), d(worker, 3), w(waiter);
  go.store(true, std::memory_order_release);
  a.join(); b.join(); c.join(); d.join(); w.join();
  return 0;
}
''',
  "4 个工作线程 + 1 个等待线程并发",
  "全 atomic，位标志内存序错误不产生非原子竞争 → 预期 miss。")

# ---------------------------------------------------------------- E024
S("E024", "memory_order", "high", "miss", ["tsan"], 2, 5, "reader",
  "acquire 加载与 relaxed 存储错配（读侧够强写侧过弱）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<long> big{0};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void writer(){
  wait_go();
  big.store(123456789L, std::memory_order_relaxed);
  /*DEFECT: ready 用 relaxed 存储：读侧即使 acquire 也无 release 可配对*/
  ready.store(true, std::memory_order_relaxed);
}
static void reader(){
  wait_go();
  while(!ready.load(std::memory_order_acquire)){}
  std::printf("E024 big=%ld\n", big.load(std::memory_order_relaxed));
}
int main(){
  std::thread w(writer), r(reader);
  go.store(true, std::memory_order_release);
  w.join(); r.join();
  return 0;
}
''',
  "两线程并发；读侧 acquire 写侧 relaxed",
  "错向配对的另一形态。预期 miss。")

# ---------------------------------------------------------------- E025
S("E025", "memory_order", "high", "miss", ["tsan"], 2, 5, "writer",
  "在 load 上误用 memory_order_release（release 对 load 无效）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> token{0};
static std::atomic<bool> done{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void writer(){
  wait_go();
  token.store(1, std::memory_order_release);
  /*DEFECT: 写侧标志用 relaxed：读侧的 load(memory_order_release) 是无意义用法，无法与 relaxed 配对*/
  done.store(true, std::memory_order_relaxed);
}
static void reader(){
  wait_go();
  /*DEFECT: load 上用 release：release 语义只对 store 有效，此处既不发布也不获取*/
  while (!done.load(std::memory_order_release)){}
  std::printf("E025 token=%d\n", token.load(std::memory_order_relaxed));
}
int main(){
  std::thread w(writer), r(reader);
  go.store(true, std::memory_order_release);
  w.join(); r.join();
  return 0;
}
''',
  "两线程并发；读侧在 load 上用 release",
  "release 用在 load 上是无效内存序。预期 miss。")

# ---------------------------------------------------------------- E026
S("E026", "memory_order", "high", "miss", ["tsan"], 2, 5, "update",
  "compare_exchange_weak 成功序用 relaxed 做「读-改-写-再写」多步更新",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> idx{0};
static int arr[4] = {0, 1, 2, 3};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void bump(){
  wait_go();
  int expected = 0;
  /*DEFECT: CAS 成功序用 relaxed：随后对 arr 的两次写入不在任何 release 语义内，读线程可见性无保证*/
  if (idx.compare_exchange_weak(expected, 1, std::memory_order_relaxed)){
    arr[0] = 100;
    arr[1] = 200;
  }
}
static void peek(){
  wait_go();
  while (idx.load(std::memory_order_acquire) < 1){}
  std::printf("E026 arr0=%d arr1=%d\n", arr[0], arr[1]);
}
int main(){
  std::thread a(bump), b(peek);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；peek 观察 idx 后读非原子数组",
  "CAS 成功序过弱。注意：peek 用 acquire 读 idx，release 序列在 relaxed CAS 处断开 → 预期 TSan catch 更可能；"
  "若 TSan 判为无竞争则诚实记 miss。")

# ---------------------------------------------------------------- E027
S("E027", "memory_order", "medium", "miss", ["tsan"], 2, 5, "get",
  "DCLP 二次检查的 relaxed 读 + 重试循环",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int*> slot{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static int* get(){
  int* p = slot.load(std::memory_order_acquire);
  if (!p){
    p = new int(5);
    /*DEFECT: 二次检查用 relaxed 后直接返回新指针：读线程可能拿到未与 release 配对的指针值*/
    if (slot.load(std::memory_order_relaxed) != nullptr){ delete p; p = slot.load(std::memory_order_relaxed); }
    else slot.store(p, std::memory_order_release);
  }
  return p;
}
static void worker(){ wait_go(); std::printf("E027 v=%d\n", *get()); }
int main(){
  std::thread a(worker), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发首次调用 get()",
  "纯原子 DCLP 内存序错误。预期 miss。")

# ---------------------------------------------------------------- E028
S("E028", "memory_order", "high", "catch", ["tsan"], 2, 5, "consumer",
  "以 relaxed 读标志 + 非原子裸指针读取已发布对象",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Session { int id; int step; };
static Session* volatile g_sess = nullptr;   // 非原子指针
static std::atomic<bool> open{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void opener(){
  wait_go();
  Session* s = new Session{1, 0};
  s->step = 3;
  g_sess = s;
  open.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  /*DEFECT: open 用 relaxed 轮询，随后读非原子 g_sess 指向的对象 → 竞争 + 可能读到半构造对象*/
  while(!open.load(std::memory_order_relaxed)){}
  std::printf("E028 step=%d\n", g_sess->step);
}
int main(){
  std::thread o(opener), c(consumer);
  go.store(true, std::memory_order_release);
  o.join(); c.join();
  return 0;
}
''',
  "两线程并发；consumer 读非原子指针指向的对象",
  "竞争真实 → 预期 TSan catch。")

# ---------------------------------------------------------------- E029
S("E029", "memory_order", "high", "catch", ["tsan"], 2, 5, "consumer",
  "中间的 relaxed store 打断 release 序列，读侧仍用 acquire",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int slot_v[4] = {0, 0, 0, 0};
static std::atomic<int> a_flag{0}, b_flag{0}, go{0};
static void wait_go(){ while(go.load(std::memory_order_acquire) == 0){} }
static void producer(){
  wait_go();
  slot_v[0] = 1;
  a_flag.store(1, std::memory_order_release);
  slot_v[1] = 2;
  /*DEFECT: b_flag 用 relaxed 存储：它切断了 a_flag 建立的 release 序列的延伸，读侧 acquire b_flag 得不到 slot_v 的可见性*/
  b_flag.store(1, std::memory_order_relaxed);
  slot_v[2] = 3;
}
static void consumer(){
  wait_go();
  while (b_flag.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 此时读 slot_v[2]：该写入在 relaxed store 之后，无任何 acquire 与之配对 → 数据竞争*/
  std::printf("E029 v2=%d\n", slot_v[2]);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(1, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；consumer 读 release 序列之外的写入",
  "release 序列被 relaxed 打断。竞争真实 → 预期 TSan catch。")

# ---------------------------------------------------------------- E030
S("E030", "memory_order", "medium", "miss", ["tsan"], 2, 5, "throttled",
  "以 relaxed 计数作「配额已满」判据（顺序正确性依赖内存序但全是原子）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> in_flight{0};
static std::atomic<long> total{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void task(){
  wait_go();
  /*DEFECT: 准入判断与计数增减全用 relaxed：relaxed 不建立顺序，限流逻辑在弱内存序下可超限*/
  while (in_flight.fetch_add(1, std::memory_order_relaxed) > 4) {}
  total.fetch_add(1, std::memory_order_relaxed);
  in_flight.fetch_sub(1, std::memory_order_relaxed);
}
int main(){
  std::thread a(task), b(task), c(task), d(task), e(task);
  go.store(true, std::memory_order_release);
  a.join(); b.join(); c.join(); d.join(); e.join();
  std::printf("E030 total=%ld\n", total.load(std::memory_order_relaxed));
  return 0;
}
''',
  "5 个线程并发执行限流任务",
  "限流判据内存序错误但全程 atomic，无数据竞争 → 预期 miss。")

# ---------------------------------------------------------------- E031
S("E031", "memory_order", "high", "miss", ["tsan"], 2, 5, "consumer",
  "生产者 relaxed 写多个原子字段，消费者只 acquire 一个总标志",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> f1{0}, f2{0}, f3{0};
static std::atomic<bool> all_ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  f1.store(10, std::memory_order_relaxed);
  f2.store(20, std::memory_order_relaxed);
  f3.store(30, std::memory_order_relaxed);
  all_ready.store(true, std::memory_order_release);
}
static void consumer(){
  wait_go();
  while(!all_ready.load(std::memory_order_acquire)){}
  /*DEFECT: f1/f2/f3 是 relaxed 存储，读侧也 relaxed 读：acquire 只约束 all_ready 一个原子，三个字段无同步保护*/
  std::printf("E031 f1=%d f2=%d f3=%d\n",
              f1.load(std::memory_order_relaxed),
              f2.load(std::memory_order_relaxed),
              f3.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；消费者读三个 relaxed 字段",
  "全 atomic，acquire 不覆盖其余字段 → 无数据竞争 → 预期 miss。")

# ---------------------------------------------------------------- E032
S("E032", "memory_order", "medium", "miss", ["tsan"], 2, 5, "get",
  "DCLP 里 relaxed 检查非原子局部缓存指针",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int*> inst{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static int* get_cached(){
  static int* cached = nullptr;             // 非原子静态缓存
  int* p = inst.load(std::memory_order_acquire);
  if (p == nullptr){
    /*DEFECT: 对非原子 cached 用 relaxed 语义判断再返回：与其它线程对 cached 的写形成数据竞争*/
    if (inst.load(std::memory_order_relaxed) == nullptr) inst.store(p = new int(6), std::memory_order_release);
    cached = p;                            // 非原子缓存写：两线程可能同时写 → 数据竞争
  }
  return cached;
}
static void worker(){ wait_go(); std::printf("E032 v=%d\n", *get_cached()); }
int main(){
  std::thread a(worker), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发首次调用 get_cached()",
  "非原子静态缓存 + relaxed 二次检查。竞争真实但窗口窄，TSan 可能漏报；诚实标注。")

# ---------------------------------------------------------------- E033
S("E033", "memory_order", "high", "miss", ["tsan"], 2, 5, "waiter",
  "spin-wait 中 relaxed 轮询 + relaxed 读载荷（无 release 侧）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> seq{0};
static std::atomic<int> payload{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  payload.store(88, std::memory_order_relaxed);
  seq.store(1, std::memory_order_relaxed);
}
static void waiter(){
  wait_go();
  /*DEFECT: relaxed 轮询 seq：即使读到 1，payload 的写入也没有任何 synchronizes-with 保证*/
  while (seq.load(std::memory_order_relaxed) == 0){}
  std::printf("E033 payload=%d\n", payload.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), w(waiter);
  go.store(true, std::memory_order_release);
  p.join(); w.join();
  return 0;
}
''',
  "两线程并发；waiter relaxed 轮询",
  "全 relaxed 链路，无 release。预期 miss。")

# ---------------------------------------------------------------- E034
S("E034", "memory_order", "high", "miss", ["asan", "tsan"], 2, 5, "take",
  "exchange 用 relaxed 换出指针，读侧 acquire 的是另一个标志",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Job { int id; int prio; };
static std::atomic<Job*> slot{nullptr};
static std::atomic<bool> armed{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void arm(){
  wait_go();
  Job* j = new Job{1, 5};
  j->prio = 9;
  /*DEFECT: slot 用 relaxed exchange 发布：读侧 acquire 的是 armed，对 slot 的发布链无约束*/
  slot.exchange(j, std::memory_order_relaxed);
  armed.store(true, std::memory_order_release);
}
static Job* take(){
  wait_go();
  while (!armed.load(std::memory_order_acquire)){}
  /*DEFECT: 读侧 relaxed 读 slot：与 relaxed exchange 也不构成 synchronizes-with，Job 字段可见性无保证*/
  Job* j = slot.load(std::memory_order_relaxed);
  std::printf("E034 prio=%d\n", j->prio);
  return j;
}
int main(){
  std::thread a(arm), b(take);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；take 读 relaxed 发布的指针",
  "发布链被 relaxed 打断。属 UB；TSan 不建模内存序 → 预期 miss。")

# ---------------------------------------------------------------- E035
S("E035", "memory_order", "high", "catch", ["tsan"], 2, 5, "publish",
  "以 relaxed 计数作数组下标发布，随后读非原子数组",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int cells[8] = {0, 0, 0, 0, 0, 0, 0, 0};
static std::atomic<int> w_cursor{0}, r_cursor{0}, go{0};
static void wait_go(){ while(go.load(std::memory_order_acquire) == 0){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 8; ++i){
    cells[i] = i + 500;                                   // 非原子写
    /*DEFECT: w_cursor 用 relaxed 递增：发布下标不携带 release，读者据其读 cells 无同步*/
    w_cursor.store(i + 1, std::memory_order_relaxed);
  }
}
static void consumer(){
  wait_go();
  /*DEFECT: relaxed 读 w_cursor 作完成判据，随后读非原子 cells → 数据竞争*/
  while (w_cursor.load(std::memory_order_relaxed) < 8){}
  std::printf("E035 c7=%d\n", cells[7]);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(1, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；消费者依 relaxed 下标读非原子单元",
  "竞争真实 → 预期 TSan catch。")

# ---------------------------------------------------------------- E036
S("E036", "memory_order", "high", "catch", ["tsan"], 2, 5, "producer_b",
  "两个生产者一个 acquire 一个 relaxed，发布强度不一致",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int log_[6];
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer_a(){
  wait_go();
  log_[0] = 1; log_[1] = 2;
  /*DEFECT: 生产者 B 用 relaxed 发布同一个 ready；A 用 release：两个生产者强度不一致，读侧无法统一获得可见性*/
  ready.store(true, std::memory_order_release);
}
static void producer_b(){
  wait_go();
  log_[2] = 3; log_[3] = 4;
  ready.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!ready.load(std::memory_order_acquire)){}
  /*DEFECT: 只 acquire 到 B 的 relaxed 写（无 release），却读全部 log_ → 与 A/B 的非原子写竞争*/
  std::printf("E036 l0=%d l3=%d\n", log_[0], log_[3]);
}
int main(){
  std::thread a(producer_a), b(producer_b), c(consumer);
  go.store(true, std::memory_order_release);
  a.join(); b.join(); c.join();
  return 0;
}
''',
  "2 生产者 + 1 消费者并发",
  "多生产者发布强度不一致，读侧覆盖全部载荷。竞争真实 → 预期 TSan catch。")

# ---------------------------------------------------------------- E037
S("E037", "memory_order", "high", "catch", ["tsan"], 2, 5, "consumer",
  "relaxed 轮询标志后读非原子结构体成员",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Acc { long id; double balance; };
static Acc g_acc{0, 0.0};
static std::atomic<bool> synced{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void updater(){
  wait_go();
  g_acc.id = 9001; g_acc.balance = 12.5;
  synced.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  /*DEFECT: synced 用 relaxed 轮询：无 acquire，随后读非原子 g_acc 成员 → 数据竞争*/
  while (!synced.load(std::memory_order_relaxed)){}
  std::printf("E037 id=%ld bal=%f\n", g_acc.id, g_acc.balance);
}
int main(){
  std::thread u(updater), c(consumer);
  go.store(true, std::memory_order_release);
  u.join(); c.join();
  return 0;
}
''',
  "两线程并发；consumer 读非原子账户结构",
  "竞争真实 → 预期 TSan catch。")

# ---------------------------------------------------------------- E038
S("E038", "memory_order", "high", "miss", ["asan", "tsan"], 2, 5, "get",
  "DCLP 中 relaxed 二次检查 + 竞争分支 delete 导致 UAF 窗口",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Pool { int* buf; int n; };
static std::atomic<Pool*> pool{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static Pool* get(){
  Pool* p = pool.load(std::memory_order_acquire);
  if (!p){
    p = new Pool{new int[4]{1, 2, 3, 4}, 4};
    /*DEFECT: 二次检查用 relaxed：两线程可同时判定为空，其中一条 delete 后另一条仍持有已释放指针（读侧无 acquire 保护）*/
    if (pool.load(std::memory_order_relaxed) == nullptr) pool.store(p, std::memory_order_release);
    else { delete p->buf; delete p; p = pool.load(std::memory_order_relaxed); }
  }
  /*DEFECT: 返回前用 relaxed 再读一次 pool：可能拿到刚被竞争分支 delete 掉的指针*/
  Pool* q = pool.load(std::memory_order_relaxed);
  return q ? q : p;
}
static void worker(){ wait_go(); Pool* p = get(); std::printf("E038 n=%d buf3=%d\n", p->n, p->buf[3]); }
int main(){
  std::thread a(worker), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发首次调用 get()，同时进入慢路径",
  "DCLP 的 relaxed 二次检查是真实的内存序缺陷（缺happens-before，发布的对象可能"
  "只被构造了一半）。但「是否恰好撞上 use-after-free」取决于两线程的调度窗口："
  "只有竞争分支真的 delete 掉别人的对象时 ASan 才会报，通用调度下窗口极窄 ⇒ "
  "预期 miss。这条记录了「缺陷成立」与「可被观测」是两件事。")

# ---------------------------------------------------------------- E039
S("E039", "memory_order", "high", "catch", ["tsan"], 2, 5, "consumer",
  "写侧 acq_rel / 读侧 relaxed，载荷为非原子数组",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int wave[8] = {0, 0, 0, 0, 0, 0, 0, 0};
static std::atomic<int> seq{0}, go{0};
static void wait_go(){ while(go.load(std::memory_order_acquire) == 0){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 8; ++i) wave[i] = i + 700;             // 非原子写
  /*DEFECT: seq 用 acq_rel 做读-改-写，但读侧只 relaxed 读 seq：写侧再强也建立不了与读者的边*/
  seq.fetch_add(1, std::memory_order_acq_rel);
}
static void consumer(){
  wait_go();
  /*DEFECT: relaxed 读 seq 后读非原子 wave → 数据竞争*/
  while (seq.load(std::memory_order_relaxed) < 1){}
  std::printf("E039 w7=%d\n", wave[7]);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(1, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；读侧 relaxed 读 seq 后读非原子数组",
  "竞争真实 → 预期 TSan catch。")

# ---------------------------------------------------------------- E040
S("E040", "memory_order", "high", "catch", ["tsan"], 2, 5, "reader",
  "「一次性初始化」标志用 seq_cst 写 + relaxed 读，读侧读非原子全局表",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int table[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static std::atomic<bool> once{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void init_table(){
  wait_go();
  for (int i = 0; i < 16; ++i) table[i] = i * i;        // 非原子写
  once.store(true, std::memory_order_seq_cst);
}
static void reader(){
  wait_go();
  /*DEFECT: once 用 relaxed 轮询：无法消费 seq_cst 存储的 release 语义，读非原子 table 构成竞争*/
  while (!once.load(std::memory_order_relaxed)){}
  std::printf("E040 t15=%d\n", table[15]);
}
int main(){
  std::thread i(init_table), r(reader);
  go.store(true, std::memory_order_release);
  i.join(); r.join();
  return 0;
}
''',
  "两线程并发；reader 读非原子全局表",
  "写侧 seq_cst 读侧 relaxed。竞争真实 → 预期 TSan catch。")
