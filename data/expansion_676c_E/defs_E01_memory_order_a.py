#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E01_memory_order_a.py — memory_order 缺陷 E001..E020（20 个）。

覆盖变体：release/acquire 不匹配、relaxed 过度使用、DCLP 错误、
指针发布、握手标志、引用计数、fence 误用、consume 误用。
"""
from _dsl import S

# ---------------------------------------------------------------- E001
S("E001", "memory_order", "high", "miss", ["tsan"], 2, 5, "consumer",
  "consumer 用 relaxed 轮询 ready 标志，未与 producer 的 release 配对 acquire",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> data{0};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  data.store(42, std::memory_order_relaxed);
  ready.store(true, std::memory_order_release);
}
static void consumer(){
  wait_go();
  /*DEFECT: relaxed 轮询 ready：与 release 存储之间没有 synchronizes-with，读到 true 也可能读到 data==0*/
  while(!ready.load(std::memory_order_relaxed)){}
  std::printf("E001 data=%d\n", data.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；consumer 的 relaxed 轮询在弱内存序架构上可观测到未发布的数据",
  "release/acquire 不匹配的教科书形态。C++ 内存模型下缺少 synchronizes-with，"
  "属未定义行为；x86 TSO 下通常不显现，TSan 只检查竞争不检查内存序，故预期 miss（真实盲区）。")

# ---------------------------------------------------------------- E002
S("E002", "memory_order", "high", "miss", ["tsan"], 2, 5, "consumer",
  "consumer 用 relaxed 轮询 ready，随后 relaxed 读 double 载荷",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<double> load_v{0.0};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  load_v.store(3.5, std::memory_order_relaxed);
  ready.store(true, std::memory_order_release);
}
static void consumer(){
  wait_go();
  /*DEFECT: ready 用 relaxed 轮询，double 载荷也用 relaxed 读：两处都无 acquire 语义*/
  while(!ready.load(std::memory_order_relaxed)){}
  std::printf("E002 load=%f\n", load_v.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；consumer 可能在载荷发布前读取",
  "浮点载荷变体。缺陷同 E001（缺 acquire），TSan 不检查内存序，预期 miss。")

# ---------------------------------------------------------------- E003
S("E003", "memory_order", "high", "miss", ["tsan"], 2, 5, "get_instance",
  "DCLP 二次检查用 relaxed，读到非空指针时对象未完成构造",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Config { int a; int b; };
static std::atomic<Config*> inst{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static Config* get_instance(){
  Config* p = inst.load(std::memory_order_acquire);
  if (p == nullptr){
    p = new Config{1, 2};
    /*DEFECT: 二次检查用 relaxed，未与下方 release 存储配对：可能读到未完全发布的指针*/
    if (inst.load(std::memory_order_relaxed) == nullptr)
      inst.store(p, std::memory_order_release);
    else { delete p; p = inst.load(std::memory_order_relaxed); }
  }
  return p;
}
int main(){
  std::thread t1([]{ wait_go(); Config* c = get_instance(); std::printf("E003 a=%d\n", c->a); });
  std::thread t2([]{ wait_go(); Config* c = get_instance(); std::printf("E003 a=%d\n", c->a); });
  go.store(true, std::memory_order_release);
  t1.join(); t2.join();
  return 0;
}
''',
  "两线程同时首次调用 get_instance，触发 DCLP 快路径",
  "双重检查锁定内存序错误。构造函数写入与 relaxed 读之间无 happens-before，"
  "TSan 不建模内存序（只建模竞争），预期 miss（真实盲区）。")

# ---------------------------------------------------------------- E004
S("E004", "memory_order", "high", "miss", ["asan", "tsan"], 2, 5, "acquire_node",
  "DCLP 用普通指针承载已发布对象，二次检查走 relaxed",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node* g_node = nullptr;              // 非原子裸指针
static std::atomic<bool> g_init{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static Node* acquire_node(){
  if (g_init.load(std::memory_order_acquire)){
    /*DEFECT: 二次检查用 relaxed，且直接读非原子裸指针：发布前的中间态对读线程可见*/
    if (g_init.load(std::memory_order_relaxed)) return g_node;
  }
  Node* n = new Node{7, nullptr};
  g_node = n;
  g_init.store(true, std::memory_order_release);
  return n;
}
int main(){
  std::thread t1([]{ wait_go(); std::printf("E004 v=%d\n", acquire_node()->v); });
  std::thread t2([]{ wait_go(); std::printf("E004 v=%d\n", acquire_node()->v); });
  go.store(true, std::memory_order_release);
  t1.join(); t2.join();
  return 0;
}
''',
  "两线程并发调用 acquire_node",
  "发布对象用非原子裸指针承载 + relaxed 二次检查。属未定义行为；"
  "ASan/TSan 均不检查内存序正确性，预期 miss。")

# ---------------------------------------------------------------- E005
S("E005", "memory_order", "high", "miss", ["asan", "tsan"], 2, 5, "reader",
  "指针以 relaxed 发布，reader 以 relaxed 读取后解引用",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Payload { int arr[8]; };
static std::atomic<Payload*> pub{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void writer(){
  wait_go();
  Payload* p = new Payload{};
  for (int i = 0; i < 8; ++i) p->arr[i] = i * i;
  /*DEFECT: 指针本身用 relaxed 发布：读侧 acquire 也无法与之配对，对象内容可能未初始化可见*/
  pub.store(p, std::memory_order_relaxed);
}
static void reader(){
  wait_go();
  Payload* p = nullptr;
  /*DEFECT: relaxed 轮询指针：即使随后 acquire 读，也可能在 relaxed 轮询阶段拿到半成品指针*/
  while ((p = pub.load(std::memory_order_relaxed)) == nullptr){}
  std::printf("E005 p7=%d\n", p->arr[7]);
}
int main(){
  std::thread w(writer), r(reader);
  go.store(true, std::memory_order_release);
  w.join(); r.join();
  return 0;
}
''',
  "两线程并发；reader 轮询发布指针",
  "relaxed 发布/读取指针。读侧解引用未同步的对象内容是 UB；预期 miss。")

# ---------------------------------------------------------------- E006
S("E006", "memory_order", "medium", "miss", ["tsan"], 2, 5, "watcher",
  "标志以 release 存储、以 relaxed 加载，acquire 语义被丢弃",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> state{0};
static std::atomic<bool> changed{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void setter(){
  wait_go();
  state.store(5, std::memory_order_relaxed);
  changed.store(true, std::memory_order_release);
}
static void watcher(){
  wait_go();
  /*DEFECT: changed 用 relaxed 加载：与 release 存储不配对，state 的写入无同步保证*/
  if (changed.load(std::memory_order_relaxed))
    std::printf("E006 state=%d\n", state.load(std::memory_order_relaxed));
}
int main(){
  std::thread a(setter), b(watcher);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；watcher 观察到标志后立即读载荷",
  "release/acquire 配对缺失的第二种形态（只加载一次而非轮询）。预期 miss。")

# ---------------------------------------------------------------- E007
S("E007", "memory_order", "high", "miss", ["tsan"], 2, 5, "consumer",
  "两段式握手中第二个标志用 relaxed 发布",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> payload{0};
static std::atomic<bool> stage1{false}, stage2{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  payload.store(11, std::memory_order_relaxed);
  stage1.store(true, std::memory_order_release);
  payload.store(22, std::memory_order_relaxed);
  /*DEFECT: 第二段发布用 relaxed：consumer 若只 acquire stage2，拿不到 payload==22 的可见性*/
  stage2.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!stage2.load(std::memory_order_acquire)){}
  std::printf("E007 payload=%d\n", payload.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；consumer 只等待第二段标志",
  "两段式发布中末段标志内存序过弱。预期 miss（TSan 不检查内存序）。")

# ---------------------------------------------------------------- E008
S("E008", "memory_order", "high", "miss", ["tsan"], 2, 5, "waiter",
  "用 relaxed 计数器的读数作为「数据已就绪」的判据",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> produced{0};
static int table[4] = {0, 0, 0, 0};        // 非原子载荷
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 4; ++i){
    table[i] = i + 100;                   // 非原子写
    /*DEFECT: relaxed 计数递增：waiter 以 relaxed 读该计数作判据，两者之间无 synchronizes-with*/
    produced.fetch_add(1, std::memory_order_relaxed);
  }
}
static void waiter(){
  wait_go();
  /*DEFECT: relaxed 读计数并当作「table 已完全可见」的依据：非原子数组的写可能尚未对读线程可见*/
  while (produced.load(std::memory_order_relaxed) < 4){}
  std::printf("E008 table3=%d\n", table[3]);
}
int main(){
  std::thread p(producer), w(waiter);
  go.store(true, std::memory_order_release);
  p.join(); w.join();
  return 0;
}
''',
  "两线程并发；waiter 轮询 relaxed 计数器",
  "载荷为非原子数组 + relaxed 计数发布。数据竞争真实存在，"
  "但 TSan 的 happens-before 是按原子操作的对称性建模的，relaxed 不建立边 → 预期可被 TSan 捕获。")

# ---------------------------------------------------------------- E009
S("E009", "memory_order", "medium", "miss", ["tsan"], 2, 5, "watcher",
  "acquire 存储配 relaxed 加载（配对方向反了）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> reg{0};
static std::atomic<bool> flag{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void setter(){
  wait_go();
  reg.store(9, std::memory_order_relaxed);
  /*DEFECT: 用 acquire 做「发布」，acquire 不产生 release 语义：读侧 acquire 配不上*/
  flag.store(true, std::memory_order_acquire);
}
static void watcher(){
  wait_go();
  /*DEFECT: 用 relaxed 读，恰好与上面的 acquire 存储「错向配对」，两边都不建立 synchronizes-with*/
  if (flag.load(std::memory_order_relaxed))
    std::printf("E009 reg=%d\n", reg.load(std::memory_order_relaxed));
}
int main(){
  std::thread a(setter), b(watcher);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；watcher 观察标志",
  "acquire 存储 / relaxed 加载的错向配对。预期 miss。")

# ---------------------------------------------------------------- E010
S("E010", "memory_order", "low", "miss", ["tsan"], 2, 5, "watcher",
  "seq_cst 存储配 relaxed 加载（强度不匹配）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> cfg{0};
static std::atomic<bool> inited{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void init_once(){
  wait_go();
  cfg.store(77, std::memory_order_relaxed);
  inited.store(true, std::memory_order_seq_cst);
}
static void watcher(){
  wait_go();
  /*DEFECT: inited 用 relaxed 加载，无法消费上面 seq_cst 存储的 release 语义*/
  if (inited.load(std::memory_order_relaxed))
    std::printf("E010 cfg=%d\n", cfg.load(std::memory_order_relaxed));
}
int main(){
  std::thread a(init_once), b(watcher);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程并发；watcher 观察初始化标志",
  "seq_cst 写 + relaxed 读：强度不匹配（写侧够强、读侧过弱）。预期 miss。")

# ---------------------------------------------------------------- E011
S("E011", "memory_order", "high", "catch", ["tsan"], 2, 5, "consumer",
  "载荷以 relaxed 发布到原子，但读侧读的是非原子镜像",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int mirror = 0;                    // 非原子镜像
static std::atomic<int> pub{0};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  mirror = 4242;                          // 非原子写（发生在 release 之前的那一批）
  pub.store(mirror, std::memory_order_relaxed);
  ready.store(true, std::memory_order_release);
  /*DEFECT: release 之后又去改非原子 mirror：这批写在 release/acquire 之外，
     读侧即使正确 acquire 了 ready，也与这批写没有 happens-before */
  mirror = 7777;
}
static void consumer(){
  wait_go();
  while(!ready.load(std::memory_order_acquire)){}
  /*DEFECT: 读到的是 release 之后那一批非原子写（值 7777），却没有 acquire 能覆盖它 ⇒ 数据竞争 */
  std::printf("E011 mirror=%d pub=%d\n", mirror, pub.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；consumer 读非原子 mirror",
  "release/acquire 只覆盖 release **之前**的写。生产者 release 之后又改了mirror，"
  "这批写对读线程没有 happens-before ⇒ 竞争真实，预期 TSan catch。")

# ---------------------------------------------------------------- E012
S("E012", "memory_order", "high", "catch", ["tsan", "asan"], 2, 5, "release_ref",
  "引用计数用 relaxed 增减，读侧据此判定对象存活",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Res { int payload; };
static std::atomic<int> refs{1};
static std::atomic<bool> go{false};
static Res* g = nullptr;
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void owner(){
  wait_go();
  g = new Res{5};
  refs.store(2, std::memory_order_relaxed);
}
static void dropper(){
  wait_go();
  /*DEFECT: 以 relaxed 读取引用计数并据此 delete：与其他线程的 relaxed 增减之间无同步，读到 2 不代表对象已构造完*/
  while (refs.load(std::memory_order_relaxed) < 2){}
  if (refs.fetch_sub(1, std::memory_order_relaxed) == 2){ /* 误判：以为自己是最后一个引用 */
    delete g; g = nullptr;
  }
}
int main(){
  std::thread a(owner), b(dropper);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E012 done\n");
  return 0;
}
''',
  "两线程并发；dropper 误判引用计数并 delete",
  "relaxed 引用计数导致提前释放。owner 的构造写与 dropper 的 delete 之间无 happens-before → TSan/ASan 可捕获。")

# ---------------------------------------------------------------- E013
S("E013", "memory_order", "high", "miss", ["tsan"], 2, 5, "producer",
  "载荷与标志全部 relaxed 存储，整条发布链无 release",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<unsigned long long> stamp{0};
static std::atomic<bool> flag{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  /*DEFECT: 载荷与标志都用 relaxed：整条发布链没有任何 release，读者无法保证看到载荷*/
  stamp.store(0xDEADBEEFULL, std::memory_order_relaxed);
  flag.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!flag.load(std::memory_order_relaxed)){}
  std::printf("E013 stamp=%llx\n", stamp.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；consumer 轮询全 relaxed 标志",
  "全 relaxed 链路。预期 miss（TSan 只看竞争不看内存序）。")

# ---------------------------------------------------------------- E014
S("E014", "memory_order", "high", "miss", ["tsan"], 2, 5, "producer",
  "用 relaxed fence 代替 release 语义",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> body{0};
static std::atomic<bool> flag{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  body.store(31, std::memory_order_relaxed);
  /*DEFECT: relaxed fence 不提供 release 语义，且其后的 flag.store 也是 relaxed：无任何同步*/
  std::atomic_thread_fence(std::memory_order_relaxed);
  flag.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!flag.load(std::memory_order_acquire)){}
  std::printf("E014 body=%d\n", body.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；fence 完全失效",
  "relaxed fence 是 no-op。预期 miss。")

# ---------------------------------------------------------------- E015
S("E015", "memory_order", "high", "miss", ["tsan"], 2, 5, "consumer",
  "用 memory_order_consume 发布载荷（C++17 起不推荐且实现多等同 relaxed）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Cfg { int x; int y; };
static std::atomic<Cfg*> cfg_pub{nullptr};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  Cfg* c = new Cfg{3, 4};
  cfg_pub.store(c, std::memory_order_release);
  ready.store(true, std::memory_order_release);
}
static void consumer(){
  wait_go();
  while(!ready.load(std::memory_order_release)){}   /* 写侧也用 release，读侧无 acquire */
  /*DEFECT: consume 在 C++17 起不再具有特殊含义（实现通常退化为 relaxed），不能用来发布载荷*/
  Cfg* c = cfg_pub.load(std::memory_order_consume);
  std::printf("E015 x=%d y=%d\n", c->x, c->y);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；读侧用 consume 取载荷",
  "memory_order_consume 误用：既读侧无 acquire，写侧标志也是 release 而非 release+consume 配对。"
  "预期 miss（无内存序检测器）。")

# ---------------------------------------------------------------- E016
S("E016", "memory_order", "high", "miss", ["tsan"], 2, 5, "producer",
  "seq_cst fence 放在载荷写与标志写之间，位置错误导致不构成 release 序列",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> body{0};
static std::atomic<bool> flag{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  body.store(64, std::memory_order_relaxed);
  /*DEFECT: seq_cst fence 被夹在 relaxed 载荷写与 relaxed 标志写之间，fence 两侧都不是 release 操作，fence 形同虚设*/
  std::atomic_thread_fence(std::memory_order_seq_cst);
  flag.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!flag.load(std::memory_order_acquire)){}
  std::printf("E016 body=%d\n", body.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；fence 位置错误",
  "强 fence 也会用错位置。预期 miss。")

# ---------------------------------------------------------------- E017
S("E017", "memory_order", "high", "catch", ["tsan"], 2, 5, "waiter",
  "以 relaxed 读计数作同步判据，随后读非原子缓冲",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int ring[8];
static std::atomic<int> head{0}, tail{0}, go{0};
static void wait_go(){ while(go.load(std::memory_order_acquire) == 0){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 8; ++i){
    ring[i] = i * 3;
    /*DEFECT: tail 用 relaxed 递增：waiter 以 relaxed 读 tail 作判据，SPSC 无 happens-before，读侧可读到未初始化的 ring*/
    tail.store(tail.load(std::memory_order_relaxed) + 1, std::memory_order_relaxed);
  }
}
static void waiter(){
  wait_go();
  /*DEFECT: 同样 relaxed 读 tail：判据本身不建立同步，后续读 ring 是数据竞争*/
  while (tail.load(std::memory_order_relaxed) < 8){}
  std::printf("E017 ring7=%d\n", ring[7]);
}
int main(){
  std::thread p(producer), w(waiter);
  go.store(1, std::memory_order_release);
  p.join(); w.join();
  return 0;
}
''',
  "两线程并发；waiter 轮询 relaxed 尾索引后读非原子环形缓冲",
  "SPSC 单生产者单消费者队列用 relaxed 索引当同步机制。竞争真实 → 预期 TSan catch。")

# ---------------------------------------------------------------- E018
S("E018", "memory_order", "high", "catch", ["tsan"], 2, 5, "consumer",
  "消费者 acquire 了错误的标志，读到未被保护的载荷",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int payload_a[4] = {0, 0, 0, 0};
static int payload_b[4] = {0, 0, 0, 0};
static std::atomic<bool> flag_a{false}, flag_b{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 4; ++i) payload_a[i] = i + 1;      // 非原子写
  flag_a.store(true, std::memory_order_release);
  for (int i = 0; i < 4; ++i) payload_b[i] = i + 51;     // 非原子写
  flag_b.store(true, std::memory_order_release);
  /*DEFECT: 在 flag_b 的 release **之后**又改写 payload_a：
     读侧只 acquire flag_b，拿不到这批写的 happens-before ⇒ 竞争真实存在 */
  for (int i = 0; i < 4; ++i) payload_a[i] = i + 101;
}
static void consumer(){
  wait_go();
  /*DEFECT: 只 acquire flag_b 就去读 payload_a：flag_a 保护的载荷没有对应的 acquire，构成竞争*/
  while(!flag_b.load(std::memory_order_acquire)){}
  std::printf("E018 a3=%d b3=%d\n", payload_a[3], payload_b[3]);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；消费者读错标志对应的载荷",
  "acquire 标志与被保护载荷错配。竞争真实 → 预期 TSan catch。")

# ---------------------------------------------------------------- E019
S("E019", "memory_order", "high", "catch", ["tsan"], 2, 5, "consumer",
  "两段发布中末段标志用 relaxed，读侧 acquire 后读非原子载荷",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static int chunk[16];
static std::atomic<int> phase{0}, go{0};
static void wait_go(){ while(go.load(std::memory_order_acquire) == 0){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 16; ++i) chunk[i] = i * 2;         // 非原子写
  phase.store(1, std::memory_order_release);
  for (int i = 16; i < 32; ++i) chunk[i] = i * 2;
  /*DEFECT: 末段 phase 用 relaxed 存储：读侧即使 acquire 也拿不到第二段非原子写的 happens-before*/
  phase.store(2, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(phase.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 此时读 chunk 的全部 32 个元素，其中后 16 个的写入未被同步保护 → 数据竞争*/
  std::printf("E019 chunk31=%d\n", chunk[31]);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(1, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
''',
  "两线程并发；消费者等待末段标志后读整块缓冲",
  "末段标志内存序过弱导致后半段写入无同步。竞争真实 → 预期 TSan catch。")

# ---------------------------------------------------------------- E020
S("E020", "memory_order", "high", "catch", ["tsan", "asan"], 2, 5, "reader",
  "以 relaxed 发布指针，读侧 acquire 标志后仍读非原子缓存字段",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Cfg { int id; char name[16]; int cached; };
static std::atomic<Cfg*> pub{nullptr};
static std::atomic<bool> live{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void writer(){
  wait_go();
  Cfg* c = new Cfg{};
  c->id = 1;
  for (int i = 0; i < 16; ++i) c->name[i] = 'a' + (i % 26);
  c->cached = 0;                          // 非原子字段
  pub.store(c, std::memory_order_relaxed);
  live.store(true, std::memory_order_release);
  /*DEFECT: 在 live 的 release 之后又改写普通字段 cached：
     读侧 acquire(live) 覆盖不到这批写 ⇒ 数据竞争 */
  c->cached = 4242;
}
static void reader(){
  wait_go();
  while(!live.load(std::memory_order_acquire)){}
  Cfg* c = pub.load(std::memory_order_relaxed);
  /*DEFECT: 只对 live 做了 acquire，c->cached 是普通字段；写入发生在 release 之后，读侧无同步*/
  std::printf("E020 id=%d cached=%d\n", c->id, c->cached);
}
int main(){
  std::thread w(writer), r(reader);
  go.store(true, std::memory_order_release);
  w.join(); r.join();
  return 0;
}
''',
  "两线程并发；读者读非原子缓存字段",
  "acquire 只作用于 live 原子，对象内普通字段的可见性依赖发布链；此处发布链被 relaxed 打断 → 预期 TSan catch。")
