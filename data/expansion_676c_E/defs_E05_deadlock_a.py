#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E05_deadlock_a.py — deadlock 缺陷 E076..E094（19 个）。

统一用「门闸」手法保证确定性：两线程各自先拿到第一把锁并用原子计数确认
对方也已持有，再去抢第二把锁 —— 锁顺序相反 ⇒ 必然死锁（超时挂起）。
"""
from _dsl import S

# ---------------------------------------------------------------- E076
S("E076", "deadlock", "high", "catch", ["tsan"], 2, 5, "threadA",
  "线程 A 按 m1->m2 加锁，线程 B 按 m2->m1 加锁（锁顺序不一致）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void threadA(){
  wait_go();
  std::lock_guard<std::mutex> l1(m1);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}     // 等对方也拿到 m1
  /*DEFECT: A 的加锁顺序是 m1->m2，与 B 的 m2->m1 相反 ⇒ 循环等待，死锁 */
  std::lock_guard<std::mutex> l2(m2);
  std::printf("E076 A ok\n");
}
static void threadB(){
  wait_go();
  std::lock_guard<std::mutex> l2(m2);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: B 的加锁顺序是 m2->m1，与 A 相反 ⇒ 死锁点 */
  std::lock_guard<std::mutex> l1(m1);
  std::printf("E076 B ok\n");
}
int main(){
  std::thread a(threadA), b(threadB);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "两线程同时启动并各自持有第一把锁后去抢对方的锁",
  "教科书式锁顺序反转。用原子门闸保证确定性触发，超时挂起即死锁成立。")

# ---------------------------------------------------------------- E077
S("E077", "deadlock", "high", "catch", ["tsan"], 3, 5, "alpha",
  "三线程分别以 m1->m2、m2->m3、m3->m1 顺序嵌套加锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m1, m2, m3;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void spin_for(int n){ while (held.load(std::memory_order_acquire) < n){} }
static void alpha(){
  wait_go();
  std::lock_guard<std::mutex> a(m1);
  held.fetch_add(1, std::memory_order_release); spin_for(3);
  /*DEFECT: m1->m2->（隐含 m3 由 beta/gamma 持有）形成环形等待 ⇒ 死锁 */
  std::lock_guard<std::mutex> b(m2);
  std::printf("E077 alpha\n");
}
static void beta(){
  wait_go();
  std::lock_guard<std::mutex> b(m2);
  held.fetch_add(1, std::memory_order_release); spin_for(3);
  /*DEFECT: m2->m3 顺序，与 gamma 的 m3->m1->m2 构成环 ⇒ 死锁点 */
  std::lock_guard<std::mutex> c(m3);
  std::printf("E077 beta\n");
}
static void gamma(){
  wait_go();
  std::lock_guard<std::mutex> c(m3);
  held.fetch_add(1, std::memory_order_release); spin_for(3);
  /*DEFECT: m3->m1 与 alpha 的 m1->m2->m3 构成环 ⇒ 死锁点 */
  std::lock_guard<std::mutex> a(m1);
  std::printf("E077 gamma\n");
}
int main(){
  std::thread x(alpha), y(beta), z(gamma);
  go.store(true, std::memory_order_release);
  x.join(); y.join(); z.join();
  return 0;
}
''',
  "3 线程环形嵌套加锁",
  "三锁环形等待。确定性触发。")

# ---------------------------------------------------------------- E078
S("E078", "deadlock", "high", "catch", ["tsan"], 2, 5, "logger",
  "日志路径先锁输出锁再锁配置锁，配置路径先锁配置锁再锁输出锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex out_lock, cfg_lock;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void log_path(){
  wait_go();
  std::lock_guard<std::mutex> o(out_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 日志路径 out->cfg */
  std::lock_guard<std::mutex> c(cfg_lock);
  std::printf("E078 logged\n");
}
static void cfg_path(){
  wait_go();
  std::lock_guard<std::mutex> c(cfg_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 配置路径 cfg->out，与日志路径相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> o(out_lock);
  std::printf("E078 cfg applied\n");
}
int main(){
  std::thread a(log_path), b(cfg_path);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程分别走日志路径与配置路径",
  "现实项目里最常见的顺序反转（日志 vs 配置）。确定性触发。")

# ---------------------------------------------------------------- E079
S("E079", "deadlock", "high", "catch", ["tsan"], 2, 5, "cache_flush",
  "缓存刷新路径 data->meta，旁路读取路径 meta->data",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex data_lock, meta_lock;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void cache_flush(){
  wait_go();
  std::lock_guard<std::mutex> d(data_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 刷新路径 data->meta */
  std::lock_guard<std::mutex> m(meta_lock);
  std::printf("E079 flushed\n");
}
static void side_read(){
  wait_go();
  std::lock_guard<std::mutex> m(meta_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 旁路读取路径 meta->data，与刷新路径相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> d(data_lock);
  std::printf("E079 read side\n");
}
int main(){
  std::thread a(cache_flush), b(side_read);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程走刷新路径与旁路读取路径",
  "数据/元数据双锁顺序反转。确定性触发。")

# ---------------------------------------------------------------- E080
S("E080", "deadlock", "high", "catch", ["tsan"], 2, 5, "engine",
  "引擎层 engine->plugin，插件层 plugin->engine",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex engine_lock, plugin_lock;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void engine(){
  wait_go();
  std::lock_guard<std::mutex> e(engine_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 引擎层 engine->plugin */
  std::lock_guard<std::mutex> p(plugin_lock);
  std::printf("E080 engine\n");
}
static void plugin(){
  wait_go();
  std::lock_guard<std::mutex> p(plugin_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 插件层 plugin->engine，与引擎层相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> e(engine_lock);
  std::printf("E080 plugin\n");
}
int main(){
  std::thread a(engine), b(plugin);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程走引擎层与插件层",
  "分层架构的锁顺序反转。确定性触发。")

# ---------------------------------------------------------------- E081
S("E081", "deadlock", "high", "catch", ["tsan"], 2, 5, "net",
  "网络发送路径 sock->session，会话清理路径 session->sock",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex sock_lock, sess_lock;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void send_path(){
  wait_go();
  std::lock_guard<std::mutex> s(sock_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 发送路径 sock->session */
  std::lock_guard<std::mutex> q(sess_lock);
  std::printf("E081 sent\n");
}
static void cleanup_path(){
  wait_go();
  std::lock_guard<std::mutex> q(sess_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 清理路径 session->sock，与发送路径相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> s(sock_lock);
  std::printf("E081 cleaned\n");
}
int main(){
  std::thread a(send_path), b(cleanup_path);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程走发送路径与清理路径",
  "网络编程常见顺序反转。确定性触发。")

# ---------------------------------------------------------------- E082
S("E082", "deadlock", "high", "catch", ["tsan"], 1, 5, "reenter",
  "同一线程对非递归 std::mutex 二次加锁（递归加锁误用）",
  r'''
#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m;
static int depth = 0;
static void inner(){
  /*DEFECT: 非递归 std::mutex 被同一线程再次 lock：std::mutex 不支持同线程重入 ⇒ 自死锁 */
  std::lock_guard<std::mutex> g(m);
  depth++;
}
static void outer(){
  std::lock_guard<std::mutex> g(m);
  depth++;
  inner();
}
int main(){
  std::thread a(outer);
  a.join();
  std::printf("E082 depth=%d\n", depth);
  return 0;
}
''',
  "单线程内嵌套调用导致同线程重复加锁",
  "std::mutex 上同线程重入是未定义行为，libstdc++ 上表现为自死锁。确定性触发。")

# ---------------------------------------------------------------- E083
S("E083", "deadlock", "high", "catch", ["tsan"], 2, 5, "recursive_enter",
  "两个线程都走「取锁后回调」的路径，回调再次取同一把锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::atomic<int> entered{0};
static void on_event(){
  /*DEFECT: 回调在调用方已持有 m 的栈帧上再次 lock(m)：非递归锁 ⇒ 立即自死锁 */
  std::lock_guard<std::mutex> g(m);
  std::printf("E083 callback done\n");
}
static void enter(){
  std::lock_guard<std::mutex> g(m);
  entered.fetch_add(1, std::memory_order_release);
  on_event();
}
int main(){
  std::thread a(enter), b(enter);
  a.join(); b.join();
  std::printf("E083 entered=%d\n", entered.load());
  return 0;
}
''',
  "2 线程都进入「取锁 + 回调」路径",
  "回调中获取已持有的锁。第一个进入的线程立即自死锁。")

# ---------------------------------------------------------------- E084
S("E084", "deadlock", "high", "catch", ["tsan"], 1, 5, "double_guard",
  "同一作用域内两个 lock_guard 锁同一把 mutex",
  r'''
#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m;
static void f(){
  std::lock_guard<std::mutex> g1(m);
  /*DEFECT: 同一线程对同一把非递归 mutex 再取一次锁（复制粘贴式防御性加锁）⇒ 自死锁 */
  std::lock_guard<std::mutex> g2(m);
  std::printf("E084 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
''',
  "单线程同作用域重复加锁",
  "防御性重复加锁。确定性自死锁。")

# ---------------------------------------------------------------- E085
S("E085", "deadlock", "high", "catch", ["tsan"], 1, 5, "recursive_helper",
  "递归函数每层都加同一把锁",
  r'''
#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m;
static int depth = 0;
static void walk(int n){
  std::lock_guard<std::mutex> g(m);
  depth++;
  if (n > 0) walk(n - 1);        /*DEFECT: 递归下降时重复 lock 同一把非递归 mutex ⇒ 第二层即自死锁 */
}
int main(){
  std::thread t([]{ walk(4); });
  t.join();
  std::printf("E085 depth=%d\n", depth);
  return 0;
}
''',
  "单线程递归下降",
  "递归 + 非递归锁。确定性自死锁。")

# ---------------------------------------------------------------- E086
S("E086", "deadlock", "high", "catch", ["tsan"], 2, 5, "waiter",
  "持锁等待条件变量：等一个只有拿到该锁的线程才能满足的条件",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static std::condition_variable cv;
static bool ready = false;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void waiter(){
  wait_go();
  std::unique_lock<std::mutex> l1(m1);          // 一直持有 m1
  {
    std::unique_lock<std::mutex> l2(m2);
    /*DEFECT: 持 m1 不放，却等一个「只有拿到 m1 的 notifier 才能置位」的条件 ⇒ 死锁 */
    cv.wait(l2, []{ return ready; });
  }
  std::printf("E086 waiter done\n");
}
static void notifier(){
  wait_go();
  /*DEFECT: notifier 必须先拿 m1 才能改 ready，于是永远等不到 ⇒ 与 waiter 互相等待 */
  std::lock_guard<std::mutex> l1(m1);
  ready = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(notifier);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：等待者持锁等条件，通知者需要该锁才能满足条件",
  "持锁等待条件变量。确定性死锁。")

# ---------------------------------------------------------------- E087
S("E087", "deadlock", "high", "catch", ["tsan"], 2, 5, "hold_and_wait",
  "持 A 锁等 B 锁，同时第三线程持 B 锁等 A 锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex A, B;
static std::atomic<bool> first_held{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void need_b(){
  wait_go();
  std::unique_lock<std::mutex> a(A);
  first_held.store(true, std::memory_order_release);
  while(!first_held.load(std::memory_order_acquire)){}
  /*DEFECT: 持 A 等 B（hold-and-wait）*/
  std::unique_lock<std::mutex> b(B);
  std::printf("E087 got both\n");
}
static void need_a(){
  wait_go();
  while(!first_held.load(std::memory_order_acquire)){}
  std::unique_lock<std::mutex> b(B);
  /*DEFECT: 持 B 等 A，与上面构成循环等待 ⇒ 死锁 */
  std::unique_lock<std::mutex> a(A);
  std::printf("E087 got both reverse\n");
}
int main(){
  std::thread x(need_b), y(need_a);
  go.store(true, std::memory_order_release);
  x.join(); y.join();
  return 0;
}
''',
  "2 线程分别持 A 等 B、持 B 等 A",
  "教科书 hold-and-wait 循环等待。确定性触发。")

# ---------------------------------------------------------------- E088
S("E088", "deadlock", "high", "catch", ["tsan"], 2, 5, "prod",
  "生产者持锁等待空间释放，消费者要拿同一把锁才能腾出空间",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m, space_lock;
static std::condition_variable cv;
static int free_slots = 0;
static std::atomic<bool> go{false}, producer_ready{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  std::unique_lock<std::mutex> lk(m);
  std::lock_guard<std::mutex> keep(space_lock);   // 关键：第二把锁，wait 不会释放它
  producer_ready.store(true, std::memory_order_release);
  /*DEFECT: 持 space_lock 等「有空位」，而空位只能由拿到 space_lock 的 consumer 释放
     ⇒ cv.wait 只释放 m，space_lock 仍在手上 ⇒ 死锁 */
  cv.wait(lk, []{ return free_slots > 0; });
  --free_slots;
  std::printf("E088 produced\n");
}
static void consumer(){
  wait_go();
  while(!producer_ready.load(std::memory_order_acquire)){}   // 确保 producer 已持住 space_lock
  /*DEFECT: consumer 必须拿到 space_lock 才能腾出空位，而 space_lock 被 producer 永久持有 */
  std::lock_guard<std::mutex> s(space_lock);
  free_slots += 2;
  cv.notify_all();
}
int main(){
  std::thread a(producer), b(consumer);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：生产者持锁等空间，消费者需该锁腾空间",
  "有界缓冲的经典死锁变体。确定性触发。")

# ---------------------------------------------------------------- E089
S("E089", "deadlock", "high", "catch", ["tsan"], 1, 5, "relock",
  "已持有 m1 时调用 std::lock(m1, m2)",
  r'''
#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static void f(){
  std::unique_lock<std::mutex> held(m1);      // 先持有 m1
  /*DEFECT: std::lock 的死锁避免算法假设「调用者不持有其中任何一把」；
     此处 m1 已被本线程持有，算法在 try_lock 阶段永远拿不到 m1 ⇒ 自死锁 */
  std::lock(m1, m2);
  std::printf("E089 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
''',
  "单线程已持锁再调 std::lock",
  "std::lock 误用。确定性自死锁。")

# ---------------------------------------------------------------- E090
S("E090", "deadlock", "high", "catch", ["tsan"], 1, 5, "adopt_then_lock",
  "adopt_lock 取得所有权后把同一把锁交给 std::lock",
  r'''
#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static void f(){
  std::unique_lock<std::mutex> held(m1, std::adopt_lock);
  m1.lock();
  /*DEFECT: adopt_lock 之后 m1 归本线程所有，再交给 std::lock 会与自身冲突 ⇒ 自死锁 */
  std::lock(m1, m2);
  std::printf("E090 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
''',
  "单线程 adopt_lock 后再 std::lock",
  "adopt_lock 与 std::lock 混用。确定性自死锁。")

# ---------------------------------------------------------------- E091
S("E091", "deadlock", "high", "catch", ["tsan"], 1, 5, "lock_then_manual",
  "std::lock 之后又手动 lock 其中一把",
  r'''
#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static void f(){
  std::lock(m1, m2);                        // 正确用法：一次性拿两把
  /*DEFECT: 拿到两把之后再手动 m2.lock()：同线程重复获取 ⇒ 自死锁 */
  m2.lock();
  std::printf("E091 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
''',
  "单线程 std::lock 后重复 lock",
  "std::lock 与手动 lock 混用。确定性自死锁。")

# ---------------------------------------------------------------- E092
S("E092", "deadlock", "high", "catch", ["tsan"], 2, 5, "reader",
  "读路径 account->ledger，写路径 ledger->account",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex acct, ledger;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void read_balance(){
  wait_go();
  std::lock_guard<std::mutex> a(acct);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 读路径 acct->ledger */
  std::lock_guard<std::mutex> l(ledger);
  std::printf("E092 balance read\n");
}
static void write_entry(){
  wait_go();
  std::lock_guard<std::mutex> l(ledger);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 写路径 ledger->acct，与读路径相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> a(acct);
  std::printf("E092 entry written\n");
}
int main(){
  std::thread a(read_balance), b(write_entry);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程走读路径与写路径",
  "账户/账本双锁顺序反转。确定性触发。")

# ---------------------------------------------------------------- E093
S("E093", "deadlock", "high", "catch", ["tsan"], 2, 5, "upload",
  "上传路径 file->meta，扫描路径 meta->file",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex file_lock, meta_lock;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void upload(){
  wait_go();
  std::lock_guard<std::mutex> f(file_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 上传路径 file->meta */
  std::lock_guard<std::mutex> m(meta_lock);
  std::printf("E093 uploaded\n");
}
static void scan(){
  wait_go();
  std::lock_guard<std::mutex> m(meta_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 扫描路径 meta->file，与上传路径相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> f(file_lock);
  std::printf("E093 scanned\n");
}
int main(){
  std::thread a(upload), b(scan);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程走上传路径与扫描路径",
  "文件/元数据锁顺序反转。确定性触发。")

# ---------------------------------------------------------------- E094
S("E094", "deadlock", "high", "catch", ["tsan"], 3, 5, "t1",
  "三个线程分别持有 m1 / m2 / m3 并按相反圆周顺序等待下一把",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m1, m2, m3;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void gate(int n){ while (held.load(std::memory_order_acquire) < n){} }
static void t1(){
  wait_go();
  std::lock_guard<std::mutex> a(m1);
  held.fetch_add(1, std::memory_order_release); gate(3);
  /*DEFECT: m1->m2 */
  std::lock_guard<std::mutex> b(m2);
  std::printf("E094 t1\n");
}
static void t2(){
  wait_go();
  std::lock_guard<std::mutex> b(m2);
  held.fetch_add(1, std::memory_order_release); gate(3);
  /*DEFECT: m2->m3 */
  std::lock_guard<std::mutex> c(m3);
  std::printf("E094 t2\n");
}
static void t3(){
  wait_go();
  std::lock_guard<std::mutex> c(m3);
  held.fetch_add(1, std::memory_order_release); gate(3);
  /*DEFECT: m3->m1，与 t1 的 m1->m2、t2 的 m2->m3 构成圆周等待 ⇒ 三方死锁 */
  std::lock_guard<std::mutex> a(m1);
  std::printf("E094 t3\n");
}
int main(){
  std::thread x(t1), y(t2), z(t3);
  go.store(true, std::memory_order_release);
  x.join(); y.join(); z.join();
  return 0;
}
''',
  "3 线程圆周顺序加锁",
  "三向圆周死锁。确定性触发。")
