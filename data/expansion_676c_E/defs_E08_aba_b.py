#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E08_aba_b.py — aba_problem 缺陷 E126..E140（15 个）。"""
from _dsl import S

# ---------------------------------------------------------------- E126
S("E126", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "hz_check",
  "危险指针只发布不重新校验，删除线程无视 hazard 直接回收",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<void*> hazard{nullptr};
static std::atomic<int> step{0}, reclaimed{0};
static void reclaim(Node* n){
  /*DEFECT: 回收路径完全无视已发布的 hazard：只要自己摘下 head 就 delete，
     不检查是否有人在读它 ⇒ 读侧必然出现 ABA / UAF */
  Node* exp = head.load(std::memory_order_acquire);
  if (head.compare_exchange_strong(exp, n->next, std::memory_order_acq_rel, std::memory_order_acquire)){
    delete n;
    reclaimed.fetch_add(1, std::memory_order_relaxed);
  }
}
int main(){
  Node* n1 = new Node{1, nullptr};
  head.store(n1, std::memory_order_release);
  std::thread t([&]{
    /*DEFECT: 读侧只发布 hazard、从不再校验 head：一旦删除线程在两步之间回收并复用，
       这里就会消费到「同地址不同对象」 */
    Node* p = head.load(std::memory_order_acquire);
    hazard.store(p, std::memory_order_release);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    std::printf("E126 v=%d\n", p->v);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  reclaim(head.load(std::memory_order_acquire));
  head.store(new Node{2, nullptr});
  step.store(2, std::memory_order_release);
  t.join();
  std::printf("E126 reclaimed=%d\n", reclaimed.load());
  return 0;
}
''',
  "2 线程：读侧发布 hazard 后挂起，写侧无视 hazard 回收并复用地址",
  "hazard pointer 协议只做了一半。窗口内的 UAF 取决于 delete 与读是否重叠 → 预期 miss（sanitizer 未必命中，但 ABA 语义确实被破坏）。")

# ---------------------------------------------------------------- E127
S("E127", "aba_problem", "high", "catch", ["asan"], 2, 5, "hz_reclaimer",
  "危险指针「扫描-退休」缺失：reclaimer 连续回收多个节点",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
#include <vector>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<void*> hazard{nullptr};
static std::atomic<int> step{0};
int main(){
  Node* n2 = new Node{2, nullptr};
  Node* n1 = new Node{1, n2};
  head.store(n1, std::memory_order_release);
  std::thread t([&]{
    Node* p = head.load(std::memory_order_acquire);
    hazard.store(p, std::memory_order_release);
    /*DEFECT: 读侧把 hazard 登记在自己线程的栈变量上，但 reclaimer 从不扫描 hazard 集合：
       「保护」是单向宣告，不构成任何互斥 */
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 此时 p 已被释放并可能被复用，下面读 p->next 是 use-after-free + ABA */
    std::printf("E127 v=%d next=%d\n", p->v, p->next ? p->next->v : -1);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = head.exchange(nullptr, std::memory_order_acq_rel);
  delete dead;
  delete n2;                              /*DEFECT: 直接 delete 链上的第二个节点，完全不做退休扫描 */
  head.store(new Node{3, nullptr});
  step.store(2, std::memory_order_release);
  t.join();
  return 0;
}
''',
  "2 线程：读侧宣告 hazard，写侧连删两个节点",
  "无退休扫描的 hazard pointer。ASan 可捕获读侧的 UAF → 预期 catch。")

# ---------------------------------------------------------------- E128
S("E128", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "tagless_stack",
  "无锁栈缺少 tagged pointer，节点值 A→B→A",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[3];
static std::atomic<Node*> top{nullptr};
static std::atomic<long> ver{0};
static std::atomic<int> step{0}, ops{0};
int main(){
  for (int i = 0; i < 3; ++i){ arena[i].v = 0; arena[i].next = nullptr; }
  Node* n1 = &arena[0]; n1->v = 1;
  Node* n2 = &arena[1]; n2->v = 2; n2->next = n1;
  top.store(n2, std::memory_order_release);
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 明明有 ver 计数器却没把它和指针打包进同一个原子字（缺 tagged pointer）：
       CAS 只比较指针，ver 的存在不提供任何保护 ⇒ A->B->A 后误成功 */
    if (top.compare_exchange_strong(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire)){
      ops.fetch_add(1, std::memory_order_relaxed);
      ver.fetch_add(1, std::memory_order_relaxed);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  arena[1].v = 0;
  top.store(n1, std::memory_order_release);
  arena[1].v = 2; arena[1].next = n1;
  top.store(n2, std::memory_order_release);      // top 回到同一地址
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E128 ops=%d ver=%ld top_v=%d\n", ops.load(), ver.load(), top.load()->v);
  return 0;
}
''',
  "2 线程：存在版本计数器但未与指针打包",
  "tagged pointer 缺失。预期 miss。")

# ---------------------------------------------------------------- E129
S("E129", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "freelist",
  "内存池 freelist 用无版本 CAS 分配，槽位 A→B→A",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Block { int idx; Block* next; };
static Block pool[3];
static std::atomic<Block*> freelist{nullptr};
static std::atomic<int> step{0}, allocs{0}, frees{0};
int main(){
  for (int i = 0; i < 3; ++i){ pool[i].idx = i; pool[i].next = (i + 1 < 3) ? &pool[i+1] : nullptr; }
  freelist.store(&pool[0], std::memory_order_release);
  std::thread a([&]{
    Block* head = freelist.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: freelist 分配没有版本号：head 槽位被 free 再 alloc 走一圈后回到同一地址，
       CAS 误成功 ⇒ 同一 block 被两个持有者同时分配（double ownership） */
    if (freelist.compare_exchange_strong(head, head->next, std::memory_order_acq_rel, std::memory_order_acquire))
      allocs.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  freelist.store(&pool[1], std::memory_order_release);   // 分配掉 pool[0]
  frees.fetch_add(1, std::memory_order_relaxed);
  freelist.store(&pool[0], std::memory_order_release);   // 释放回同一地址 ⇒ ABA
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E129 allocs=%d frees=%d\n", allocs.load(), frees.load());
  return 0;
}
''',
  "2 线程：freelist 槽位被释放回同一地址",
  "无版本 freelist 的 ABA（双所有者）。预期 miss。")

# ---------------------------------------------------------------- E130
S("E130", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "sweep",
  "RCU 读侧无 rcu_read_lock：同步回调式「伪 RCU」",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<int> step{0}, grace{0};
int main(){
  head.store(new Node{1, nullptr}, std::memory_order_release);
  std::thread r([&]{
    /*DEFECT: 「RCU 读侧」什么保护都没做（没有 read_lock / 没有 hazard / 没有 epoch）：
         读侧随时可能被 reclaim 线程搬走并复用同一地址 ⇒ ABA / UAF 语义上完全敞开 */
    Node* p = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    std::printf("E130 v=%d\n", p->v);
    grace.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = head.exchange(nullptr, std::memory_order_acq_rel);
  /*DEFECT: reclaim 不等读侧 grace period（无条件 sleep 代替），随后复用地址 */
  std::this_thread::sleep_for(std::chrono::milliseconds(1));
  head.store(new Node{1, nullptr});
  step.store(2, std::memory_order_release);
  r.join();
  delete dead;
  std::printf("E130 grace=%d\n", grace.load());
  return 0;
}
''',
  "2 线程：读侧无保护，reclaim 用 sleep 假装 grace period",
  "伪 RCU。读侧访问是否落在已释放内存取决于时序 → 预期 miss（真实盲区）。")

# ---------------------------------------------------------------- E131
S("E131", "aba_problem", "high", "catch", ["asan"], 2, 5, "reader",
  "RCU 读侧无保护 + reclaim 用 sleep 代替 grace period，命中 UAF",
  r'''
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
struct Node { int v; int payload[4]; };
static std::atomic<Node*> head{nullptr};
static std::atomic<int> step{0};
int main(){
  Node* n = new Node{1, {1, 2, 3, 4}};
  head.store(n, std::memory_order_release);
  std::thread r([&]{
    /*DEFECT: 读侧不做任何保护就长期持有指针 */
    Node* p = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: reclaim 已经 delete 了 p：下面读 payload 是 use-after-free */
    int s = 0;
    for (int i = 0; i < 4; ++i) s += p->payload[i];
    std::printf("E131 sum=%d\n", s);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = head.exchange(nullptr, std::memory_order_acq_rel);
  delete dead;                                  /* 立即回收：不给读侧任何窗口 */
  head.store(new Node{1, {1, 2, 3, 4}});
  step.store(2, std::memory_order_release);
  r.join();
  return 0;
}
''',
  "2 线程：reclaim 立即 delete，读侧随后遍历 payload",
  "无保护 RCU 读侧。ASan 的 heap-use-after-free 稳定命中 → 预期 catch。")

# ---------------------------------------------------------------- E132
S("E132", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "mutator",
  "原子指针指向的节点内容被回收方「就地改写复用」（同址不同值）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; int gen; Node* next; };
static Node arena[2];
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0}, read_gen{0};
int main(){
  arena[0].v = 1; arena[0].gen = 100; arena[0].next = nullptr;
  top.store(&arena[0], std::memory_order_release);
  std::thread a([&]{
    Node* p = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 只凭地址判断「还是同一个节点」：其实 gen 字段已经从 100 变成 200，
       消费者以为在读原来的对象，读到的是被复用后的新对象（ABA 的内容维度） */
    read_gen.store(p->gen, std::memory_order_relaxed);
    std::printf("E132 v=%d gen=%d\n", p->v, p->gen);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  top.store(nullptr, std::memory_order_release);
  arena[0].v = 2; arena[0].gen = 200;          // 同址复用，内容全变
  top.store(&arena[0], std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E132 read_gen=%d\n", read_gen.load());
  return 0;
}
''',
  "2 线程：节点被摘下后同址改写复用，读者仍按旧对象解释",
  "内容维度的 ABA（地址相同、语义不同）。预期 miss。")

# ---------------------------------------------------------------- E133
S("E133", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "popper",
  "无锁队列：元素在「出队-回队」后同址复用，被重复消费",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Item { int id; Item* next; };
static Item arena[2];
static std::atomic<Item*> head{nullptr};
static std::atomic<int> step{0}, consumed{0};
static int consumed_ids[4] = {0, 0, 0, 0};
int main(){
  arena[0].id = 1; arena[0].next = nullptr;
  arena[1].id = 2; arena[1].next = &arena[0];
  head.store(&arena[1], std::memory_order_release);
  std::thread a([&]{
    Item* p = head.load(std::memory_order_acquire);
    Item* nxt = p->next;
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: p 已被出队并回队（同一槽位、id 变了），CAS 仍按「同一元素」处理 ⇒ 同一 Item 被消费两次 */
    if (head.compare_exchange_strong(p, nxt, std::memory_order_acq_rel, std::memory_order_acquire)){
      int k = consumed.fetch_add(1, std::memory_order_relaxed);
      if (k < 4) consumed_ids[k] = p->id;
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  head.store(&arena[0], std::memory_order_release);
  arena[1].id = 3; arena[1].next = &arena[0];
  head.store(&arena[1], std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E133 consumed=%d ids=%d,%d\n", consumed.load(), consumed_ids[0], consumed_ids[1]);
  return 0;
}
''',
  "2 线程：元素出队后同址回队，消费者读到新内容",
  "重复消费型 ABA。预期 miss。")

# ---------------------------------------------------------------- E134
S("E134", "aba_problem", "high", "catch", ["asan"], 2, 5, "popper",
  "无锁栈 pop 后把陈旧指针写回链表（UAF 写）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
int main(){
  Node* n1 = new Node{1, nullptr};
  Node* n2 = new Node{2, n1};
  top.store(n2, std::memory_order_release);
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: ABA 后 old 已被 delete：往 old->next 写字段是 use-after-free **写** */
    old->next = nullptr;
    /*DEFECT: 再把陈旧指针挂回链表头，链表从此指向已释放内存 */
    Node* exp = top.load(std::memory_order_acquire);
    do { old->next = exp; }
    while (!top.compare_exchange_weak(exp, old, std::memory_order_release, std::memory_order_relaxed));
    std::printf("E134 relinked stale\n");
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = top.exchange(nullptr, std::memory_order_acq_rel);
  delete dead;
  top.store(new Node{3, nullptr});
  step.store(2, std::memory_order_release);
  a.join();
  return 0;
}
''',
  "2 线程：A 在 ABA 窗口内向已释放节点写并重新挂链",
  "UAF 写。ASan 稳定捕获 → 预期 catch。")

# ---------------------------------------------------------------- E135
S("E135", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "counter_cas",
  "以「指针 + 独立计数器」代替 tagged pointer，两字更新不原子",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[2];
static std::atomic<Node*> top{nullptr};
static std::atomic<unsigned> ver{0};
static std::atomic<int> step{0}, stale_succ{0};
int main(){
  arena[0].v = 1; arena[0].next = nullptr;
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);
  std::thread a([&]{
    Node* p = top.load(std::memory_order_acquire);
    Node* nxt = p->next;
    unsigned v0 = ver.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 指针与版本号分处两个原子对象，校验与更新无法原子完成：
       在「读 p」「读 ver」「写 top」之间 ver 可能已被别人推进，校验形同虚设 ⇒ ABA 仍会发生 */
    if (ver.load(std::memory_order_acquire) == v0){
      stale_succ.fetch_add(1, std::memory_order_relaxed);
      Node* exp = p;
      top.compare_exchange_strong(exp, nxt, std::memory_order_acq_rel, std::memory_order_acquire);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  top.store(&arena[0], std::memory_order_release);
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E135 stale_succ=%d ver=%u\n", stale_succ.load(), ver.load());
  return 0;
}
''',
  "2 线程：指针与版本号分处两个原子，校验不原子",
  "「伪 tagged pointer」。预期 miss。")

# ---------------------------------------------------------------- E136
S("E136", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "window",
  "无锁栈在「摘链」与「改链」之间留出 ABA 窗口",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[3];
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0}, removed{0}, added{0};
int main(){
  for (int i = 0; i < 3; ++i){ arena[i].v = 0; arena[i].next = nullptr; }
  arena[0].v = 1;
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);
  std::thread a([&]{
    /*DEFECT: 先摘链（CAS）再改链，中间非原子 ⇒ 摘下的节点在窗口内可被复用并再次挂链 */
    Node* old = top.load(std::memory_order_acquire);
    Node* nxt = old->next;
    if (top.compare_exchange_strong(old, nxt, std::memory_order_acq_rel, std::memory_order_acquire))
      removed.fetch_add(1, std::memory_order_relaxed);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 窗口内 old 已被别人 push 回同一个槽位（值又变回同一个地址），
       这里再 CAS 摘一次 ⇒ 同一个节点被摘两次 */
    if (top.compare_exchange_strong(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire))
      removed.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  top.store(&arena[2], std::memory_order_release);
  added.fetch_add(1, std::memory_order_relaxed);
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);   // 同址重新挂链
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E136 removed=%d added=%d\n", removed.load(), added.load());
  return 0;
}
''',
  "2 线程：摘链与改链之间节点被同址重新挂链",
  "两段式 pop 的 ABA 窗口。预期 miss。")

# ---------------------------------------------------------------- E137
S("E137", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "value_aba",
  "以「值 + 版本」分开存放导致值 ABA（版本更新滞后）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> value{0};
static std::atomic<long> version{0};
static std::atomic<int> step{0}, commits{0};
int main(){
  value.store(7, std::memory_order_release);
  version.store(1, std::memory_order_release);
  std::thread a([&]{
    int v = value.load(std::memory_order_acquire);
    long ver = version.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 「值未变 + 版本未变」的两段式校验不是原子的：写者可以先把值改回、
       再把版本号写回（甚至还没写），使这里的乐观校验通过而实际基线已失效 */
    if (value.load(std::memory_order_acquire) == v && version.load(std::memory_order_acquire) == ver){
      commits.fetch_add(1, std::memory_order_relaxed);
      version.store(ver + 1, std::memory_order_release);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  value.store(9, std::memory_order_release);
  value.store(7, std::memory_order_release);       // 值回到原值
  version.store(1, std::memory_order_release);     // 版本号「看起来」没变
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E137 commits=%d value=%d version=%ld\n", commits.load(), value.load(), version.load());
  return 0;
}
''',
  "2 线程：值与版本号分别更新，乐观校验被绕过",
  "非原子「值+版本」校验。预期 miss。")

# ---------------------------------------------------------------- E138
S("E138", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "weak_retry",
  "CAS 失败重试时复用已被别人改写的 expected，ABA 使重试逻辑错乱",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0}, retries{0};
static Node arena[2];
int main(){
  arena[0].v = 1; arena[0].next = nullptr;
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);
  std::thread a([&]{
    Node* expected = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    int guard = 0;
    /*DEFECT: 重试循环没有次数/状态校验，且 expected 会被 CAS 失败自动改写；
       ABA 期间一次「伪变化」会让循环把别人的后继当成自己的后继继续推进 */
    while (guard++ < 3){
      Node* nxt = expected->next;
      if (top.compare_exchange_weak(expected, nxt, std::memory_order_acq_rel, std::memory_order_acquire)) break;
      retries.fetch_add(1, std::memory_order_relaxed);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  top.store(&arena[0], std::memory_order_release);
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E138 retries=%d top_v=%d\n", retries.load(), top.load()->v);
  return 0;
}
''',
  "2 线程：CAS 重试循环遇上同址复用",
  "重试逻辑在 ABA 下错乱。预期 miss。")

# ---------------------------------------------------------------- E139
S("E139", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "reclaimer",
  "reclaim 线程把「刚被读侧引用」的对象立即放回 freelist 供他人分配",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Block { int tag; int data; Block* next; };
static std::atomic<Block*> freelist{nullptr};
static std::atomic<Block*> published{nullptr};
static std::atomic<int> step{0};
int main(){
  Block* b1 = new Block{1, 111, nullptr};
  freelist.store(b1, std::memory_order_release);
  published.store(b1, std::memory_order_release);
  std::thread t([&]{
    Block* b = published.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 读侧仍在使用 b；reclaim 已把它 delete 并让新对象复用同一地址，
       这里读到的 tag/data 属于另一个对象（ABA 的典型表现） */
    std::printf("E139 tag=%d data=%d\n", b->tag, b->data);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Block* old = freelist.exchange(nullptr, std::memory_order_acq_rel);
  delete old;                                     /*DEFECT: 立即回收，无 grace period */
  freelist.store(new Block{2, 222, nullptr});     /* 很可能复用同一地址 */
  step.store(2, std::memory_order_release);
  t.join();
  return 0;
}
''',
  "2 线程：reclaim 无 grace period 直接 delete 并复用地址",
  "ABA 的内存复用表现。glibc malloc 对同尺寸的小对象几乎必然复用刚释放的块，"
  "所以实际发生的是「地址复用型 ABA」（读到错数据），内存**没有**落入已释放状态，"
  "ASan 无从报告 ⇒ 预期 miss。这条恰好说明 ABA 与 UAF 是两类缺陷："
  "前者 sanitizer 完全看不见，后者才看得见。")

# ---------------------------------------------------------------- E140
S("E140", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "epoch",
  "epoch-based reclamation 的 epoch 号本身遭遇 ABA",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<unsigned> global_epoch{0};
static std::atomic<int> step{0}, frees{0};
int main(){
  Node arena[2];
  arena[0].v = 1; arena[0].next = nullptr;
  arena[1].v = 2; arena[1].next = &arena[0];
  head.store(&arena[1], std::memory_order_release);
  std::thread t([&]{
    unsigned e = global_epoch.load(std::memory_order_acquire);
    Node* p = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 用「epoch 号相等」当回收安全判据，但 epoch 是有限位宽计数器：
       长时间运行后 epoch 绕回同值，读侧据此认为「没有新 epoch 推进」而错误地允许回收 */
    if (global_epoch.load(std::memory_order_acquire) == e){
      frees.fetch_add(1, std::memory_order_relaxed);
      p->v = 0;                            // 回收：写回槽位
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  global_epoch.store(1, std::memory_order_release);
  global_epoch.store(0, std::memory_order_release);   // epoch 绕回同值
  step.store(2, std::memory_order_release);
  t.join();
  std::printf("E140 frees=%d head_v=%d\n", frees.load(), head.load()->v);
  return 0;
}
''',
  "2 线程：epoch 计数器绕回同值",
  "计数器自身的 ABA。预期 miss。")
