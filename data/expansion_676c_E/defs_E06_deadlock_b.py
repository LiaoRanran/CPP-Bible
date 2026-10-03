#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E06_deadlock_b.py — deadlock 缺陷 E095..E110（16 个）。"""
from _dsl import S

# ---------------------------------------------------------------- E095
S("E095", "deadlock", "high", "catch", ["tsan"], 2, 5, "cb_on_locked",
  "持锁线程触发回调，回调里再加第二把锁；另一线程反向持有",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex big, small;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void on_big_ready(){
  /*DEFECT: 回调在 big 已被持有的栈帧上再取 small，且与另一线程的 small->big 顺序相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> s(small);
  std::printf("E095 callback\n");
}
static void big_path(){
  wait_go();
  std::lock_guard<std::mutex> b(big);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  on_big_ready();
}
static void small_path(){
  wait_go();
  std::lock_guard<std::mutex> s(small);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: small->big，与 big_path 里的 big->small 构成循环等待 */
  std::lock_guard<std::mutex> b(big);
  std::printf("E095 small path\n");
}
int main(){
  std::thread a(big_path), b(small_path);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程走大锁路径（含回调）与小锁路径",
  "回调跨锁 + 顺序反转。确定性触发。")

# ---------------------------------------------------------------- E096
S("E096", "deadlock", "high", "catch", ["tsan"], 2, 5, "notify_cb",
  "持锁调用「通知」回调，回调内部再次请求同一把锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::atomic<int> inside{0};
static void notify_cb(){
  /*DEFECT: 通知回调在调用方仍持有 m 时执行，回调里再 lock(m) ⇒ 自死锁 */
  std::lock_guard<std::mutex> g(m);
  inside.fetch_add(1, std::memory_order_release);
}
static void holder(){
  std::lock_guard<std::mutex> g(m);
  notify_cb();
}
int main(){
  std::thread a(holder), b(holder);
  a.join(); b.join();
  std::printf("E096 inside=%d\n", inside.load());
  return 0;
}
''',
  "2 线程都走「持锁 + 通知回调」路径",
  "回调中获取已持有的锁。确定性触发。")

# ---------------------------------------------------------------- E097
S("E097", "deadlock", "high", "catch", ["tsan"], 2, 5, "hook",
  "钩子注册表在读锁下调用用户钩子，钩子又去拿写锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex reg;
static std::atomic<int> fired{0};
static void user_hook(){
  /*DEFECT: 用户钩子在 reg 被持有期间执行，钩子内部再次 lock(reg) ⇒ 自死锁 */
  std::lock_guard<std::mutex> g(reg);
  fired.fetch_add(1, std::memory_order_release);
}
static void run_hooks(){
  std::lock_guard<std::mutex> g(reg);
  user_hook();
}
int main(){
  std::thread a(run_hooks), b(run_hooks);
  a.join(); b.join();
  std::printf("E097 fired=%d\n", fired.load());
  return 0;
}
''',
  "2 线程都执行「持锁遍历钩子」路径",
  "插件钩子重入。确定性触发。")

# ---------------------------------------------------------------- E098
S("E098", "deadlock", "high", "catch", ["tsan"], 2, 5, "iterator_invalidate",
  "迭代器持有共享锁时调用回调，回调内部请求独占锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex tbl;
static std::atomic<int> visited{0};
static void on_row(){
  /*DEFECT: 在持有 tbl 的遍历过程中进入回调，回调里对同一张表加锁 ⇒ 自死锁 */
  std::lock_guard<std::mutex> g(tbl);
  visited.fetch_add(1, std::memory_order_release);
}
static void scan(){
  std::lock_guard<std::mutex> g(tbl);
  on_row();
}
int main(){
  std::thread a(scan), b(scan);
  a.join(); b.join();
  std::printf("E098 visited=%d\n", visited.load());
  return 0;
}
''',
  "2 线程都走「持锁遍历 + 回调」路径",
  "遍历-回调重入。确定性触发。")

# ---------------------------------------------------------------- E099
S("E099", "deadlock", "high", "catch", ["tsan"], 2, 5, "left",
  "左线程持 la 等 lb，右线程持 lb 等 la（两个条件变量互等）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex la, lb;
static std::condition_variable cva, cvb;
static bool left_done = false, right_done = false;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void left(){
  wait_go();
  std::unique_lock<std::mutex> l(la);
  /*DEFECT: 持 la 等 right_done，而 right_done 只能由右线程在拿到 lb 后设置；右线程正持 lb 等 left_done ⇒ 互等死锁 */
  cva.wait(l, []{ return right_done; });
  left_done = true;
  cvb.notify_all();
}
static void right(){
  wait_go();
  std::unique_lock<std::mutex> l(lb);
  /*DEFECT: 持 lb 等 left_done，构成对称的循环等待 */
  cvb.wait(l, []{ return left_done; });
  right_done = true;
  cva.notify_all();
}
int main(){
  std::thread a(left), b(right);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程各持一把锁、各等对方置位",
  "条件变量互等死锁（且谓词分别由不同的 mutex 保护，本身也是 cv/mutex 配对错误）。确定性触发。")

# ---------------------------------------------------------------- E100
S("E100", "deadlock", "high", "catch", ["tsan"], 2, 5, "req",
  "请求线程持连接锁等响应，等待线程持响应锁等连接",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex conn, resp;
static std::condition_variable cv_conn, cv_resp;
static bool resp_ready = false, conn_released = false;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void request(){
  wait_go();
  std::unique_lock<std::mutex> c(conn);
  /*DEFECT: 持 conn 等 resp_ready；resp_ready 需由应答线程在拿到 conn 后设置 ⇒ 死锁 */
  cv_conn.wait(c, []{ return resp_ready; });
  conn_released = true;
  cv_resp.notify_all();
}
static void respond(){
  wait_go();
  std::unique_lock<std::mutex> r(resp);
  /*DEFECT: 持 resp 等 conn_released，与上面互为因果循环 */
  cv_resp.wait(r, []{ return conn_released; });
  resp_ready = true;
  cv_conn.notify_all();
}
int main(){
  std::thread a(request), b(respond);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程走请求路径与应答路径",
  "请求/应答式互等死锁。确定性触发。")

# ---------------------------------------------------------------- E101
S("E101", "deadlock", "high", "catch", ["tsan"], 3, 5, "p1",
  "三个阶段线程各持一锁并等待下一阶段的锁",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex s1, s2, s3;
static std::condition_variable c1, c2, c3;
static bool d1 = false, d2 = false, d3 = false;
static std::atomic<int> ready{0};
static void gate(){ while (ready.load(std::memory_order_acquire) < 3){} }
static void stage1(){
  std::unique_lock<std::mutex> l(s1);
  ready.fetch_add(1, std::memory_order_release); gate();
  /*DEFECT: 持 s1 等 d1；d1 只能由 stage2 在拿到 s2 后设，而 stage2 持 s2 等 d2… ⇒ 环形等待 */
  c1.wait(l, []{ return d1; });
  d3 = true; c3.notify_all();
}
static void stage2(){
  std::unique_lock<std::mutex> l(s2);
  ready.fetch_add(1, std::memory_order_release); gate();
  /*DEFECT: 持 s2 等 d2 */
  c2.wait(l, []{ return d2; });
  d1 = true; c1.notify_all();
}
static void stage3(){
  std::unique_lock<std::mutex> l(s3);
  ready.fetch_add(1, std::memory_order_release); gate();
  /*DEFECT: 持 s3 等 d3，闭合等待环 */
  c3.wait(l, []{ return d3; });
  d2 = true; c2.notify_all();
}
int main(){
  std::thread a(stage1), b(stage2), c(stage3);
  a.join(); b.join(); c.join();
  return 0;
}
''',
  "3 阶段线程各持一锁等待下一阶段",
  "流水线式环形等待。确定性触发。")

# ---------------------------------------------------------------- E102
S("E102", "deadlock", "high", "catch", ["tsan"], 2, 5, "timeout_wait",
  "超时等待路径在持锁时进入 wait，超时后仍不释放外层锁",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m, gate;
static std::condition_variable cv;
static bool done = false;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void waiter(){
  wait_go();
  std::unique_lock<std::mutex> lk(m);
  std::lock_guard<std::mutex> keep(gate);    // 关键：第二把锁，超时路径也不释放
  /*DEFECT: wait_for 超时返回后不重新检查谓词就往下走；
     而 gate 被一直持有，需要 gate 的线程永远拿不到它 ⇒ 死锁 */
  cv.wait_for(lk, std::chrono::milliseconds(50), []{ return done; });
  done = true;
}
static void helper(){
  wait_go();
  /*DEFECT: helper 必须拿到 gate 才能推进，被 waiter 永久持有 ⇒ 阻塞 */
  std::lock_guard<std::mutex> g(gate);
  std::lock_guard<std::mutex> lk(m);
  done = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(helper);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：超时等待者持锁不释放，助手需该锁",
  "超时路径未正确释放外层锁。确定性触发。")

# ---------------------------------------------------------------- E103
S("E103", "deadlock", "high", "catch", ["tsan"], 1, 5, "relock",
  "unique_lock 已持有时再次调用 lock()",
  r'''
#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m;
static void f(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: unique_lock 已拥有 m 时再调用 lock()：标准未定义此用法，libstdc++ 上退化为自死锁 */
  lk.lock();
  std::printf("E103 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
''',
  "单线程 unique_lock 重复 lock",
  "unique_lock 状态机误用：已拥有所有权时再 lock()。实测（WSL glibc 2.39）不是挂起，"
  "而是由 libstdc++/glibc 抛 std::system_error(\"Resource deadlock avoided\") 并 abort"
  "（EDEADLK）。TSan / ASan / UBSan 均无报告 ⇒ 预期 miss。"
  "与 E110 同类：**一个让进程直接崩溃的并发缺陷对现有 sanitizer 资产完全隐形**。")

# ---------------------------------------------------------------- E104
S("E104", "deadlock", "high", "catch", ["tsan"], 2, 5, "holder",
  "一条路径「先 a 再 std::lock(b,c)」，另一条「先 std::lock(b,c) 再 a」",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex a, b, c;
static std::atomic<int> held{0}, ready{0};
static void gate(){ while (held.load(std::memory_order_acquire) < 2){} }
static void holder(){
  std::lock_guard<std::mutex> la(a);
  held.fetch_add(1, std::memory_order_release);
  ready.store(1, std::memory_order_release);
  gate();
  /*DEFECT: 路径甲：先单独 lock(a)，再 std::lock(b,c)。
     std::lock 只会为自己参数里的两把键做死锁避免，它看不见「a 已被本线程持有」 */
  std::lock(b, c);
  std::printf("E104 holder done\n");
}
static void packer(){
  while (ready.load(std::memory_order_acquire) == 0){}
  /*DEFECT: 路径乙：先 std::lock(b,c) 一次拿走两把，再单独 lock(a) ⇒ 与甲构成循环等待 */
  std::lock(b, c);
  held.fetch_add(1, std::memory_order_release);
  std::lock_guard<std::mutex> la(a);
  std::printf("E104 packer done\n");
}
int main(){
  std::thread x(holder), y(packer);
  x.join(); y.join();
  return 0;
}
''',
  "2 线程分别走「a + std::lock(b,c)」与「std::lock(b,c) + a」两条路径",
  "std::lock 误用：把「已被本线程持有的锁」排在 std::lock 之外，"
  "死锁避免算法因此失效 ⇒ 确定性死锁。")

# ---------------------------------------------------------------- E105
S("E105", "deadlock", "high", "catch", ["tsan"], 1, 5, "scoped_plus_manual",
  "scoped_lock 已持有 m1 后再手动 lock(m1)",
  r'''
#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static void f(){
  std::scoped_lock<std::mutex, std::mutex> sl(m1, m2);
  /*DEFECT: scoped_lock 已同时持有 m1/m2，又手动 m1.lock() ⇒ 同线程重复获取非递归锁，自死锁 */
  std::lock_guard<std::mutex> g(m1);
  std::printf("E105 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
''',
  "单线程 scoped_lock 与手动 lock 混用",
  "RAII 与手动加锁混用。确定性自死锁。")

# ---------------------------------------------------------------- E106
S("E106", "deadlock", "high", "catch", ["tsan"], 1, 5, "scoped_nested",
  "scoped_lock 作用域内再次进入同一函数（再次 scoped_lock 同两把锁）",
  r'''
#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static int depth = 0;
static void enter(int d){
  std::scoped_lock<std::mutex, std::mutex> sl(m1, m2);
  depth++;
  if (d > 0) enter(d - 1);     /*DEFECT: 递归重入时对同一对锁再做一次 scoped_lock ⇒ 自死锁 */
}
int main(){
  std::thread t([]{ enter(3); });
  t.join();
  std::printf("E106 depth=%d\n", depth);
  return 0;
}
''',
  "单线程递归重入同一加锁函数",
  "scoped_lock 递归重入。确定性自死锁。")

# ---------------------------------------------------------------- E107
S("E107", "deadlock", "high", "catch", ["tsan"], 2, 5, "acquire_two_then_one",
  "一条路径一次取两把锁，另一条路径先取其中一把再取另一把",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex a, b;
static std::atomic<bool> holding_a{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void path_atomic(){
  wait_go();
  /*DEFECT: 路径甲「a->b」 */
  std::lock_guard<std::mutex> la(a);
  holding_a.store(true, std::memory_order_release);
  while(!holding_a.load(std::memory_order_acquire)){}
  std::lock_guard<std::mutex> lb(b);
  std::printf("E107 path a\n");
}
static void path_bfirst(){
  wait_go();
  while(!holding_a.load(std::memory_order_acquire)){}
  /*DEFECT: 路径乙「b->a」，与甲相反 ⇒ 死锁（注意 std::lock 与手写顺序混用加剧了不一致） */
  std::lock_guard<std::mutex> lb(b);
  std::lock_guard<std::mutex> la(a);
  std::printf("E107 path b\n");
}
int main(){
  std::thread x(path_atomic), y(path_bfirst);
  go.store(true, std::memory_order_release);
  x.join(); y.join();
  return 0;
}
''',
  "2 线程分别以 a->b 与 b->a 加锁",
  "同一对锁两种书写顺序。确定性触发。")

# ---------------------------------------------------------------- E108
S("E108", "deadlock", "high", "catch", ["tsan"], 2, 5, "leaky_scope",
  "手动 lock 后异常/提前 return 路径未解锁，锁永久泄漏",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::atomic<bool> may_fail{true};
static void leaky(){
  m.lock();
  /*DEFECT: 手动 lock() 后这条分支直接 return（没有 unlock / 没有 RAII）：m 被永久泄漏 */
  if (may_fail.load(std::memory_order_acquire)) return;
  m.unlock();
  std::printf("E108 done\n");
}
int main(){
  std::thread a(leaky);
  a.join();
  /*DEFECT: m 仍是锁死状态，后续任何 lock(m) 都会永久阻塞 */
  std::thread b([]{ std::lock_guard<std::mutex> g(m); std::printf("E108 second\n"); });
  b.join();
  return 0;
}
''',
  "第一线程泄漏锁，第二线程随后阻塞在该锁上",
  "手动加锁缺少 RAII 兜底导致锁永久泄漏。确定性触发。")

# ---------------------------------------------------------------- E109
S("E109", "deadlock", "high", "catch", ["tsan"], 2, 5, "throw_unwind",
  "持两把锁时抛异常，展开顺序使另一线程永久等待",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
#include <stdexcept>
static std::mutex outer, inner;
static std::atomic<bool> caught{false};
static void thrower(){
  outer.lock();                        // 手动 lock：没有 RAII 兜底
  std::unique_lock<std::mutex> i(inner);
  /*DEFECT: 抛异常时栈展开只会释放 inner（RAII），手动 lock 的 outer 永久泄漏：
     锁的「异常路径安全性」被破坏，且这种泄漏在栈展开里完全静默 */
  throw std::runtime_error("boom");
}
static void waiter(){
  while(!caught.load(std::memory_order_acquire)){}
  /*DEFECT: 需要 outer，而 outer 已被异常路径永久泄漏 ⇒ 永久阻塞 */
  std::lock_guard<std::mutex> o(outer);
  std::lock_guard<std::mutex> i(inner);
  std::printf("E109 ok\n");
}
int main(){
  std::thread a([&]{
    try { thrower(); }
    catch (const std::exception&){ caught.store(true, std::memory_order_release); }
  });
  std::thread b(waiter);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：一方持双锁抛异常，另一方随后按固定顺序取双锁",
  "异常展开与锁顺序耦合。确定性触发。")

# ---------------------------------------------------------------- E110
S("E110", "deadlock", "high", "miss", ["tsan", "asan"], 2, 5, "reentrant_wait",
  "condition_variable_any 与 recursive_mutex 错误配对：wait 只释放一层锁",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::recursive_mutex m;
static std::condition_variable_any cv;   // 只能配 std::mutex 的 cv 被换成 any 后，配了 recursive_mutex
static bool flag = false;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void waiter(){
  wait_go();
  std::unique_lock<std::recursive_mutex> lk(m);
  lk.lock();                    // 递归加锁，计数 = 2
  /*DEFECT: 条件变量要求配 std::mutex。配 recursive_mutex 时 wait() 只解锁一层，
     m 仍被本线程持有（计数 1）⇒ 谓词永远不会被 notifier 满足 ⇒ 死锁 */
  cv.wait(lk, []{ return flag; });
  std::printf("E110 waiter done\n");
}
static void notifier(){
  wait_go();
  /*DEFECT: notifier 需要完整地拿到 m（计数降到 0），而 A 还留着 1 层 ⇒ 永久阻塞 */
  std::lock_guard<std::recursive_mutex> g(m);
  flag = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(notifier);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：递归锁下 wait 只释放一层，notifier 拿不到完整锁",
  "条件变量必须配「wait 能完全解锁」的 mutex。实测（WSL glibc 2.39）："
  "这个缺陷**不是挂起**，而是由 libstdc++/glibc 直接抛 std::system_error("
  "\"Resource deadlock avoided\") 并 abort（EDEADLK）。"
  "TSan / ASan / UBSan 三个资产**都不输出任何报告**——"
  "一个让进程直接崩溃的并发缺陷，对现有 sanitizer 资产完全隐形 ⇒ 预期 miss（真实盲区）。")
