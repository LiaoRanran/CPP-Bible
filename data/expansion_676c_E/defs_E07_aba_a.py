#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E07_aba_a.py — aba_problem 缺陷 E111..E125（15 个）。

ABA 复现手法（两条路线，都保证可复现）：
  路线 A（静态 arena）：节点放在静态数组里，回收后立刻复用同一槽位
        ⇒ 地址必然回到原值，且**不产生 UAF** ⇒ 表现为纯逻辑破坏，
        sanitizer 完全不报（真实盲区）。
  路线 B（堆）：节点 new/delete，回收后可能复用地址
        ⇒ 陈旧指针解引用落到已释放内存 ⇒ ASan 可捕获。
两路线都用原子 step 做「A 读指针 → B 制造 A→B→A → A 执行 CAS」的确定性编排。
"""
from _dsl import S

# ---------------------------------------------------------------- E111
S("E111", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "popper",
  "无锁栈 pop 用陈旧指针 CAS；静态槽位复用使 top 回到同一地址",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[3];
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> live{0};            // 存活节点数（业务不变量）
static Node* alloc_slot(int v){
  for (int i = 0; i < 3; ++i)
    if (arena[i].v == 0){ arena[i].v = v; arena[i].next = nullptr; live.fetch_add(1); return &arena[i]; }
  return nullptr;
}
static void push(Node* n){
  Node* old = top.load(std::memory_order_relaxed);
  do { n->next = old; }
  while (!top.compare_exchange_weak(old, n, std::memory_order_release, std::memory_order_relaxed));
}
static Node* pop(){
  Node* old = top.load(std::memory_order_acquire);
  while (old && !top.compare_exchange_weak(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire)){}
  return old;
}
int main(){
  push(alloc_slot(1));
  push(alloc_slot(2));
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 用陈旧的 old 做 CAS。期间 top 经历了 A->B->A（同一槽位被回收再复用），
       CAS 只比较指针值，误判为「没变」而成功 ⇒ 新节点被从链表里抹掉 */
    if (top.compare_exchange_strong(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire))
      std::printf("E111 CAS succeeded on stale pointer\n");
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* p = pop(); live.fetch_sub(1); p->v = 0;     // 回收槽位
  push(alloc_slot(3));                              // 复用同一槽位 ⇒ top 回到同一地址
  step.store(2, std::memory_order_release);
  a.join();
  int count = 0; Node* it = top.load();
  while (it != nullptr && count < 8){ ++count; it = it->next; }
  std::printf("E111 reachable=%d live=%d\n", count, live.load());
  return 0;
}
''',
  "两线程：A 读 top 后挂起，B 弹出并复用同一槽位制造 A→B→A",
  "无锁栈 ABA 的教科书形态。静态 arena 保证地址复用且不产生 UAF ⇒ "
  "表现为「可达节点数 ≠ 存活节点数」的纯逻辑破坏，ASan/TSan/UBsan 均无报告 → 预期 miss（真实盲区）。")

# ---------------------------------------------------------------- E112
S("E112", "aba_problem", "high", "catch", ["asan"], 2, 5, "popper",
  "无锁栈 pop 在 ABA 后解引用已 delete 的陈旧指针",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
static void push(Node* n){
  Node* old = top.load(std::memory_order_relaxed);
  do { n->next = old; }
  while (!top.compare_exchange_weak(old, n, std::memory_order_release, std::memory_order_relaxed));
}
static Node* pop(){
  Node* old = top.load(std::memory_order_acquire);
  while (old && !top.compare_exchange_weak(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire)){}
  return old;
}
int main(){
  push(new Node{1, nullptr});
  push(new Node{2, nullptr});
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: ABA 后 old 指向已释放节点，读取 old->next 参与 CAS 就是在读悬垂内存 */
    Node* nxt = old->next;
    /*DEFECT: 继续解引用已 delete 的对象 */
    std::printf("E112 stale v=%d\n", old->v);
    top.compare_exchange_strong(old, nxt, std::memory_order_acq_rel, std::memory_order_acquire);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = pop();
  delete dead;                                    // 制造 A->B->A 的同时释放内存
  push(new Node{3, nullptr});
  step.store(2, std::memory_order_release);
  a.join();
  return 0;
}
''',
  "两线程：A 持有陈旧指针，B 弹出并 delete 后再 push",
  "ABA + use-after-free。ASan 的 heap-use-after-free 可稳定捕获 → 预期 catch。")

# ---------------------------------------------------------------- E113
S("E113", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "popper",
  "无锁栈 pop 后立即 delete 头节点，槽位复用造成 ABA",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[4];
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> pushes{0}, pops{0};
static Node* alloc_slot(int v){
  for (int i = 0; i < 4; ++i)
    if (arena[i].v == 0){ arena[i].v = v; arena[i].next = nullptr; return &arena[i]; }
  return nullptr;
}
static void push(Node* n){
  Node* old = top.load(std::memory_order_relaxed);
  do { n->next = old; }
  while (!top.compare_exchange_weak(old, n, std::memory_order_release, std::memory_order_relaxed));
  pushes.fetch_add(1, std::memory_order_relaxed);
}
static Node* pop(){
  Node* old = top.load(std::memory_order_acquire);
  while (old && !top.compare_exchange_weak(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire)){}
  if (old) pops.fetch_add(1, std::memory_order_relaxed);
  return old;
}
int main(){
  push(alloc_slot(10));
  push(alloc_slot(20));
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: pop 的 CAS 只比较指针值，缺少版本号/tag：top 经历 A->B->A 后这次 CAS 会误成功 */
    if (top.compare_exchange_strong(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire)){}
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* p = pop(); if (p) p->v = 0;          // 回收
  push(alloc_slot(30));                       // 复用
  step.store(2, std::memory_order_release);
  a.join();
  int count = 0; Node* it = top.load();
  while (it != nullptr && count < 8){ ++count; it = it->next; }
  std::printf("E113 reachable=%d pushes=%d pops=%d\n", count, pushes.load(), pops.load());
  return 0;
}
''',
  "2 线程：pop 后立即回收槽位并复用",
  "版本号缺失的 ABA。纯逻辑破坏 ⇒ 预期 miss。")

# ---------------------------------------------------------------- E114
S("E114", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "treaser",
  "无锁栈「预留-发布」两阶段 push 的 ABA",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[3];
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> head_count{0};
static void push(Node* n){
  Node* old = top.load(std::memory_order_relaxed);
  do { n->next = old; }
  while (!top.compare_exchange_weak(old, n, std::memory_order_release, std::memory_order_relaxed));
  head_count.fetch_add(1, std::memory_order_relaxed);
}
int main(){
  Node* n1 = &arena[0]; n1->v = 1;
  Node* n2 = &arena[1]; n2->v = 2;
  push(n1); push(n2);
  std::thread a([&]{
    Node* expected = top.load(std::memory_order_acquire);
    Node* nxt = expected->next;
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 两阶段 push 的「预留」阶段持有陈旧 expected：ABA 后 CAS 仍成功，nxt 已是过期的后继 */
    if (top.compare_exchange_strong(expected, nxt, std::memory_order_acq_rel, std::memory_order_acquire))
      head_count.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  top.store(&arena[0], std::memory_order_release);   // top 变
  top.store(&arena[1], std::memory_order_release);   // top 又变回同一地址（A->B->A）
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E114 head_count=%d top_v=%d\n", head_count.load(), top.load()->v);
  return 0;
}
''',
  "2 线程：A 预留后继指针，B 让 top 走一圈回到同一地址",
  "两阶段 push 的 ABA。预期 miss（逻辑计数错误，sanitizer 无感）。")

# ---------------------------------------------------------------- E115
S("E115", "aba_problem", "high", "catch", ["asan"], 2, 5, "popper",
  "无锁栈 pop 在 ABA 窗口内对已释放节点做 delete（二次释放）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
static void push(Node* n){
  Node* old = top.load(std::memory_order_relaxed);
  do { n->next = old; }
  while (!top.compare_exchange_weak(old, n, std::memory_order_release, std::memory_order_relaxed));
}
static Node* pop(){
  Node* old = top.load(std::memory_order_acquire);
  while (old && !top.compare_exchange_weak(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire)){}
  return old;
}
int main(){
  push(new Node{1, nullptr});
  push(new Node{2, nullptr});
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: ABA 后 CAS 误成功，old 实际已被别人 pop 并 delete；此处 delete 同一块内存 */
    if (top.compare_exchange_strong(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire))
      delete old;                       // 二次释放
    std::printf("E115 popped stale\n");
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = pop();
  delete dead;                          /*DEFECT: 先释放，再让新节点复用同一地址，
     于是 top 的指针值又回到 old —— 这正是 ABA 的「B」那一半 */
  push(new Node{3, nullptr});
  step.store(2, std::memory_order_release);
  a.join();
  delete dead;
  return 0;
}
''',
  "2 线程：A 在 ABA 窗口内 delete，B 已 delete 过同一节点",
  "ABA 导致二次释放。ASan 的 double-free / use-after-free 可捕获 → 预期 catch。")

# ---------------------------------------------------------------- E116
S("E116", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "dequeue",
  "无锁队列 dequeue 的 CAS 遇 A→B→A",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Cell { int v; Cell* next; };
static Cell ring[4];
static std::atomic<Cell*> head{nullptr}, tail{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> dequeued{0}, enqueued{0};
static void enqueue(int v){
  Cell* c = &ring[v % 4];
  c->v = v;
  Cell* t = tail.exchange(c, std::memory_order_acq_rel);
  if (t) t->next = c;
  head.store(c, std::memory_order_release);
  enqueued.fetch_add(1, std::memory_order_relaxed);
}
static int dequeue(){
  Cell* h = head.load(std::memory_order_acquire);
  Cell* nx = h->next;
  if (head.compare_exchange_strong(h, nx, std::memory_order_acq_rel, std::memory_order_acquire))
    dequeued.fetch_add(1, std::memory_order_relaxed);
  return h->v;
}
int main(){
  enqueue(1);
  enqueue(2);
  std::thread a([&]{
    Cell* h = head.load(std::memory_order_acquire);
    Cell* nx = h->next;
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 无锁队列 dequeue 缺少版本号：head 回到同一 Cell 地址后 CAS 误成功，元素被重复/丢失 */
    if (head.compare_exchange_strong(h, nx, std::memory_order_acq_rel, std::memory_order_acquire))
      dequeued.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  head.store(&ring[3], std::memory_order_release);
  head.store(h_ptr(), std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E116 in=%d out=%d\n", enqueued.load(), dequeued.load());
  return 0;
}
'''.replace("h_ptr()", "(&ring[1])"),
  "2 线程：A 读 head 后挂起，B 让 head 走一圈回到同一槽位",
  "无锁队列 ABA。静态 ring ⇒ 纯逻辑重复出队，sanitizer 无感 → 预期 miss。")

# ---------------------------------------------------------------- E117
S("E117", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "dequeue",
  "无锁队列的「head/tail 分离」更新遇 ABA",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Cell { int v; Cell* next; };
static Cell ring[4];
static std::atomic<Cell*> head{nullptr};
static std::atomic<Cell*> tail{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> drained{0};
static void reset_ring(){
  for (int i = 0; i < 4; ++i){ ring[i].v = 0; ring[i].next = nullptr; }
  head.store(&ring[0], std::memory_order_release);
  tail.store(&ring[3], std::memory_order_release);
  ring[3].next = &ring[0];
}
int main(){
  reset_ring();
  for (int i = 0; i < 4; ++i) ring[i].v = i + 1;
  std::thread a([&]{
    Cell* t = tail.load(std::memory_order_acquire);
    Cell* h = head.load(std::memory_order_acquire);
    (void)h;
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: tail 的 CAS 没有版本号：槽位被回收再复用后 tail 回到同一地址，CAS 误判「未变」 */
    Cell* exp = t;
    if (tail.compare_exchange_strong(exp, exp->next, std::memory_order_acq_rel, std::memory_order_acquire))
      drained.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  tail.store(&ring[0], std::memory_order_release);
  tail.store(&ring[3], std::memory_order_release);   // 回到同一地址
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E117 drained=%d head_v=%d\n", drained.load(), head.load()->v);
  return 0;
}
''',
  "2 线程：tail 走一圈回到同一槽位",
  "head/tail 分离的无锁队列 ABA。预期 miss。")

# ---------------------------------------------------------------- E118
S("E118", "aba_problem", "high", "catch", ["asan"], 2, 5, "dequeue",
  "无锁队列 dequeue 后 delete 元素节点，ABA 窗口内二次访问",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Cell { int v; Cell* next; };
static std::atomic<Cell*> head{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> freed{0};
int main(){
  Cell* c1 = new Cell{1, nullptr};
  Cell* c2 = new Cell{2, c1};
  head.store(c2, std::memory_order_release);
  std::thread a([&]{
    Cell* h = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: h 在 ABA 之后已被释放，读取 h->next 是 use-after-free */
    Cell* nx = h->next;
    std::printf("E118 v=%d\n", h->v);
    head.compare_exchange_strong(h, nx, std::memory_order_acq_rel, std::memory_order_acquire);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Cell* taken = head.exchange(nullptr, std::memory_order_acq_rel);
  delete taken;                       // 释放
  head.store(new Cell{9, nullptr});   // 地址可能被复用 ⇒ ABA
  step.store(2, std::memory_order_release);
  a.join();
  delete taken;
  return 0;
}
''',
  "2 线程：A 持有 head 指针，B 释放并重新分配",
  "ABA 引发 UAF。ASan 可捕获 → 预期 catch。")

# ---------------------------------------------------------------- E119
S("E119", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "poll",
  "「队列空判断」轮询在 A→B→A 后误判队列非空",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Cell { int v; };
static Cell ring[3];
static std::atomic<Cell*> head{nullptr};
static std::atomic<int> step{0}, empties{0}, nonempties{0};
int main(){
  head.store(&ring[0], std::memory_order_release);
  ring[0].v = 5;
  std::thread a([&]{
    Cell* h = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 用陈旧 h 判断「队列是否为空」：head 经历 A->B->A 后两次观测无法区分，
       于是把「刚被放回的元素」当成新元素消费，或把空队列当成非空 */
    if (h != nullptr) nonempties.fetch_add(1, std::memory_order_relaxed);
    else empties.fetch_add(1, std::memory_order_relaxed);
    std::printf("E119 h_v=%d\n", h->v);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  head.store(&ring[1], std::memory_order_release);
  head.store(&ring[0], std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E119 empty=%d nonempty=%d\n", empties.load(), nonempties.load());
  return 0;
}
''',
  "2 线程：head 在消费者观测期间走一圈回到原地址",
  "基于陈旧观测的队列状态判断。预期 miss。")

# ---------------------------------------------------------------- E120
S("E120", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "toggle",
  "无锁「值替换」CAS：值 A→B→A 后 CAS 误判未变",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> cell{0};
static std::atomic<int> step{0}, applied{0};
int main(){
  cell.store(1, std::memory_order_release);
  std::thread a([&]{
    int exp = cell.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 只比较值不看版本：cell 经历 1->0->1 后，这次 CAS 会误判「没人改过」而成功，
       基于「未被别人改过」的假设（如下方计数）就失效了 */
    if (cell.compare_exchange_strong(exp, 9, std::memory_order_acq_rel, std::memory_order_acquire))
      applied.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  cell.store(0, std::memory_order_release);
  cell.store(1, std::memory_order_release);      // 回到原值
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E120 applied=%d cell=%d\n", applied.load(), cell.load());
  return 0;
}
''',
  "2 线程：cell 值走 A->B->A",
  "值型 ABA（最容易被误认为「CSC 场景下不会发生」的一类）。预期 miss。")

# ---------------------------------------------------------------- E121
S("E121", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "cas_chain",
  "两步 CAS 之间的读-改-写被 ABA 打断",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> a{1}, b{10};
static std::atomic<int> step{0}, ops{0};
int main(){
  std::thread t([&]{
    int ea = a.load(std::memory_order_acquire);
    int eb = b.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 两次 CAS 之间读了 b 的旧值：a/b 都被别人改过又改回（1->2->1、10->20->10），
       校验通过但依据的前提（b 未变）已不成立 ⇒ 丢失更新 */
    if (a.compare_exchange_strong(ea, 3, std::memory_order_acq_rel, std::memory_order_acquire)){
      int cur = b.load(std::memory_order_relaxed);
      b.store(eb + cur, std::memory_order_relaxed);
      ops.fetch_add(1, std::memory_order_relaxed);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  a.store(2, std::memory_order_release); a.store(1, std::memory_order_release);
  b.store(20, std::memory_order_release); b.store(10, std::memory_order_release);
  step.store(2, std::memory_order_release);
  t.join();
  std::printf("E121 a=%d b=%d ops=%d\n", a.load(), b.load(), ops.load());
  return 0;
}
''',
  "2 线程：a/b 两个原子都走 A->B->A",
  "复合更新里的 ABA。预期 miss。")

# ---------------------------------------------------------------- E122
S("E122", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "cas_pair",
  "双原子「不变式」在 ABA 下被绕过（校验通过但不变式已破）",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> lo{0}, hi{10};
static std::atomic<int> step{0}, bad{0};
int main(){
  std::thread t([&]{
    int l = lo.load(std::memory_order_acquire);
    int h = hi.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 依赖「读到的 lo/hi 是同一时刻的快照」这一假设，但两次 load 之间 lo/hi
       可被改成非法组合又改回（lo:0->5->0, hi:10->2->10）⇒ 不变式 lo<=hi 的校验形同虚设 */
    if (lo.compare_exchange_strong(l, 9, std::memory_order_acq_rel, std::memory_order_acquire)){
      if (h < l) bad.fetch_add(1, std::memory_order_relaxed);
      int hh = hi.load(std::memory_order_relaxed);
      hi.store(hh - 20, std::memory_order_relaxed);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  lo.store(5, std::memory_order_release); lo.store(0, std::memory_order_release);
  hi.store(2, std::memory_order_release); hi.store(10, std::memory_order_release);
  step.store(2, std::memory_order_release);
  t.join();
  std::printf("E122 bad=%d lo=%d hi=%d\n", bad.load(), lo.load(), hi.load());
  return 0;
}
''',
  "2 线程：lo/hi 走 A->B->A",
  "不变式校验被 ABA 绕过。预期 miss。")

# ---------------------------------------------------------------- E123
S("E123", "aba_problem", "high", "miss", ["asan", "tsan"], 2, 5, "refcount",
  "引用计数用「load-判断-置回」实现，计数 A→B→A 后误判无人持有",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> refs{0};
static std::atomic<int> step{0};
static int payload = 0;
int main(){
  refs.store(1, std::memory_order_release);
  std::thread a([&]{
    (void)refs.load(std::memory_order_acquire);   // 快照读了却没参与校验（见 DEFECT）
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 「若计数为 0 则由我置 1」的 test-and-set 缺版本保护：计数 0->1->0 之后，
       这里的 CAS 误判仍为 0 而成功，与另一线程同时认为自己独占 payload */
    int exp = 0;
    if (refs.compare_exchange_strong(exp, 1, std::memory_order_acq_rel, std::memory_order_acquire))
      payload = 42;
  });
  while (step.load(std::memory_order_acquire) != 1){}
  refs.store(1, std::memory_order_release);
  refs.store(0, std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E123 refs=%d payload=%d\n", refs.load(), payload);
  return 0;
}
''',
  "2 线程：引用计数走 0->1->0",
  "引用计数的 ABA。预期 miss。")

# ---------------------------------------------------------------- E124
S("E124", "aba_problem", "high", "catch", ["asan"], 2, 5, "traverse",
  "无锁链表遍历：读 next 之后节点被删除复用",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<int> step{0};
int main(){
  Node* a1 = new Node{1, nullptr};
  Node* a2 = new Node{2, a1};
  head.store(a2, std::memory_order_release);
  std::thread t([&]{
    Node* cur = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 无 hazard pointer / 无 epoch：读到的 cur 在下一步之前可能已被删除并复用，
       下面两行对已释放内存的读写是 use-after-free */
    std::printf("E124 v=%d\n", cur->v);
    Node* nxt = cur->next;
    std::printf("E124 next_v=%d\n", nxt ? nxt->v : -1);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = head.exchange(nullptr, std::memory_order_acq_rel);
  delete dead;                                  // 释放正在被遍历的节点
  head.store(new Node{7, nullptr});             // 地址复用
  step.store(2, std::memory_order_release);
  t.join();
  return 0;
}
''',
  "2 线程：遍历线程无保护地读节点，主线程删除并复用",
  "缺 hazard pointer 的读侧遍历。ASan 捕获 UAF → 预期 catch。")

# ---------------------------------------------------------------- E125
S("E125", "aba_problem", "high", "catch", ["asan"], 2, 5, "hz_user",
  "危险指针「发布顺序」错误：先读数据再登记 hazard",
  r'''
#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<void*> hazard{nullptr};
static std::atomic<int> step{0};
int main(){
  Node* n1 = new Node{1, nullptr};
  head.store(n1, std::memory_order_release);
  std::thread t([&]{
    /*DEFECT: hazard pointer 的协议要求「读指针 → 发布 hazard → **重新校验指针**」；
       这里读指针之后立刻解引用，登记与校验都没有做 ⇒ reclaimer 完全可以在
       读指针与解引用之间把节点回收并复用同一地址 */
    Node* p = head.load(std::memory_order_acquire);
    hazard.store(p, std::memory_order_release);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: p 此刻已被 reclaimer 释放（它无视了已发布的 hazard），解引用即 UAF */
    std::printf("E125 v=%d\n", p->v);
    /*DEFECT: 事后才校验 head 是否仍等于 p —— 校验早已晚于使用（check-after-use）*/
    if (head.load(std::memory_order_acquire) == p) std::printf("E125 still valid\n");
  });
  while (step.load(std::memory_order_acquire) != 1){}
  /*DEFECT: reclaimer 侧完全不扫描 hazard 集合：只要摘下 head 就 delete */
  Node* dead = head.exchange(nullptr, std::memory_order_acq_rel);
  delete dead;
  head.store(new Node{8, nullptr});
  step.store(2, std::memory_order_release);
  t.join();
  std::printf("E125 hazard=%d\n", hazard.load() != nullptr);
  return 0;
}
''',
  "2 线程：读侧不遵守 hazard pointer 发布协议，写侧立即回收",
  "两个协议缺陷叠加：读侧 check-after-use（读指针后立刻解引用，登记与校验都没做），"
  "回收侧不扫描 hazard 集合。用 step 门闸把「登记hazard 之后、解引用之前」的窗口固定住，"
  "所以 ASan 的 heap-use-after-free 可稳定捕获 → 预期 catch。")
