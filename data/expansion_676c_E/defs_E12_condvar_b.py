#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E12_condvar_b.py — condition_variable 缺陷 E186..E200（15 个）。"""
from _dsl import S

# ---------------------------------------------------------------- E186
S("E186", "condition_variable", "high", "miss", ["tsan"], 2, 5, "waiter",
  "wait_until 使用绝对时间点，但时间点在锁外计算且早已过期",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool ready = false;
static std::atomic<int> waiting{0};
static void waiter(){
  /*DEFECT: 截止时间点在「还没拿到锁」时就已算好，等真正进 wait 时可能早已过期：
     wait_until 立即返回 no_timeout 之外的状态，而谓词根本没检查 ⇒ 无谓的超时返回被当成「可以继续」 */
  auto deadline = std::chrono::steady_clock::now() + std::chrono::milliseconds(1);
  std::this_thread::sleep_for(std::chrono::milliseconds(20));
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  std::cv_status st = cv.wait_until(lk, deadline);
  bool ok = (st == std::cv_status::no_timeout);
  std::printf("E186 ok=%d ready=%d\n", (int)ok, (int)ready);
}
static void setter(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    ready = true;
  }
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(setter);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：wait_until 的截止时间在锁外计算且已过期",
  "超时返回值被忽略。预期 miss。")

# ---------------------------------------------------------------- E187
S("E187", "condition_variable", "high", "miss", ["tsan"], 2, 5, "worker",
  "wait 使用谓词但谓词在 notify 之后才更新（更新与通知顺序颠倒）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool a_done = false, b_done = false;
static std::atomic<int> woke{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  while (!a_done) cv.wait(lk);
  /*DEFECT: 在 a_done 满足后继续等待 b_done，但通知方对 b_done 的更新与 notify 的顺序
     在某条路径上是「先 notify 后更新」⇒ 这次唤醒看不到 b_done，只能再等，
     而下一次 notify 不保证到来 */
  while (!b_done) cv.wait(lk);
  woke.store(1, std::memory_order_release);
}
static void updater(){
  {
    std::lock_guard<std::mutex> lk(m);
    a_done = true;
  }
  cv.notify_all();                     // 第一次通知（a_done 已更新）
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    b_done = true;
  }
  /*DEFECT: 若 worker 恰好在这次 notify 之后才进入第二次 wait，这次通知就丢了 */
  cv.notify_all();
}
int main(){
  std::thread a(worker), b(updater);
  a.join(); b.join();
  std::printf("E187 woke=%d\n", woke.load());
  return 0;
}
''',
  "2 线程：两段式谓词的第二次通知可能落在 wait 之前",
  "两阶段等待的通知丢失。是否永久阻塞取决于调度 → 预期 miss（时序相关）。")

# ---------------------------------------------------------------- E188
S("E188", "condition_variable", "high", "catch", ["tsan"], 2, 5, "waiter",
  "条件变量配错了 mutex：wait 用 m2，谓词由 m1 保护",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;              // 两把锁
static std::condition_variable cv;
static bool flag = false;              // 谓词：约定由 m1 保护
static std::atomic<int> waiting{0};
static void waiter(){
  /*DEFECT: cv.wait 必须配「保护谓词的那把锁」。这里用 m2 去 wait，
             而 flag 的读写都在 m1 下 ⇒ 谓词读与写不同步（数据竞争 + 丢失唤醒） */
  std::unique_lock<std::mutex> lk2(m2);
  waiting.store(1, std::memory_order_release);
  while (!flag) cv.wait(lk2);
  std::printf("E188 flag=%d\n", (int)flag);
}
static void setter(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  {
    std::lock_guard<std::mutex> lk1(m1);
    flag = true;
  }
  cv.notify_all();                     // 通知发了，但等待者在 m2 上，谓词不同步
}
int main(){
  std::thread a(waiter), b(setter);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：cv 配 m2，谓词由 m1 保护",
  "条件变量与错误的 mutex 配对：谓词读与写分处两把锁 → 真实数据竞争 → 预期 TSan catch。")

# ---------------------------------------------------------------- E189
S("E189", "condition_variable", "high", "catch", ["tsan"], 3, 5, "waiter",
  "三个线程各用不同的锁 wait 同一个条件变量",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex a, b, c;
static std::condition_variable cv;
static bool event = false;
static int payload = 0;                // 非原子
static std::atomic<int> woke{0};
static void waiter(int id, std::mutex* m){
  /*DEFECT: 同一个条件变量被三把不同的 mutex 搭配使用：
             谓词 event/payload 的同步边界与 wait 的释放/重加锁边界不一致 ⇒ 数据竞争 */
  std::unique_lock<std::mutex> lk(*m);
  while (!event) cv.wait(lk);
  payload += id;                       // 非原子读改写
  woke.fetch_add(1, std::memory_order_release);
}
static void setter(){
  while (woke.load(std::memory_order_acquire) > 100) break;
  {
    std::lock_guard<std::mutex> lk(a);
    event = true;
    payload = 100;
  }
  cv.notify_all();
}
int main(){
  std::thread x(waiter, 1, &a), y(waiter, 2, &b), z(waiter, 3, &c), w(setter);
  x.join(); y.join(); z.join(); w.join();
  std::printf("E189 woke=%d payload=%d\n", woke.load(), payload);
  return 0;
}
''',
  "3 个等待线程各配一把不同的锁 + 1 个通知者",
  "一变量多锁：谓词与 payload 的同步边界不一致 → 真实数据竞争 → 预期 TSan catch。")

# ---------------------------------------------------------------- E190
S("E190", "condition_variable", "high", "catch", ["tsan"], 2, 5, "waiter",
  "谓词本身是原子的，但伴随数据是非原子的（只同步了标志位）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static std::atomic<bool> ready{false};
static int config[16] = {0};           // 非原子配置数据
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: 谓词只同步了「ready 这一个原子」，config 是普通数组：
             即使谓词判断完全正确，读 config 依然没有 happens-before */
  while (!ready.load(std::memory_order_acquire)) cv.wait(lk);
  lk.unlock();
  /*DEFECT: 解锁后无锁读 config，与 loader 的无锁写并发 ⇒ 数据竞争 */
  int s = 0;
  for (int i = 0; i < 400000; ++i) s += config[i % 16];
  std::printf("E190 sum=%d\n", s);
}
static void loader(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  /*DEFECT: 只把 ready 这个原子置位就把读者放行，真正的数据 config 还在锁外继续写 */
  ready.store(true, std::memory_order_relaxed);
  {
    std::lock_guard<std::mutex> lk(m);
  }
  cv.notify_all();
  for (int k = 0; k < 400000; ++k) config[k % 16] += 1;   // 数据尚未就绪
}
int main(){
  std::thread a(waiter), b(loader);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：谓词是原子的，载荷是普通数组且在锁外写",
  "只同步标志位而非数据 → 真实数据竞争 → 预期 TSan catch。")

# ---------------------------------------------------------------- E191
S("E191", "condition_variable", "high", "miss", ["tsan"], 2, 5, "worker",
  "多个条件变量共用一个谓词，但只通知了其中一个",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv_a, cv_b;
static bool slot_free = false;
static std::atomic<int> woke_a{0}, woke_b{0};
static void consumer_a(){
  std::unique_lock<std::mutex> lk(m);
  while (!slot_free) cv_a.wait(lk);
  woke_a.store(1, std::memory_order_release);
}
static void consumer_b(){
  /*DEFECT: 两个条件变量共用同一个谓词 slot_free，但生产者只通知 cv_a，
             于是 cv_b 上的等待者永远收不到通知 ⇒ 永久阻塞（时序相关） */
  std::unique_lock<std::mutex> lk(m);
  while (!slot_free) cv_b.wait(lk);
  woke_b.store(1, std::memory_order_release);
}
static void producer(){
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  {
    std::lock_guard<std::mutex> lk(m);
    slot_free = true;
  }
  cv_a.notify_all();                   // DEFECT: 忘了通知 cv_b
}
int main(){
  std::thread a(consumer_a), b(consumer_b), c(producer);
  a.join(); b.join(); c.join();
  std::printf("E191 woke_a=%d woke_b=%d\n", woke_a.load(), woke_b.load());
  return 0;
}
''',
  "2 个消费者各等一个 cv + 1 个生产者只通知其中一个",
  "多条件变量共用一个谓词。consumer_b 永久阻塞 → 记为阻塞触发（超时挂起）。")

# ---------------------------------------------------------------- E192
S("E192", "condition_variable", "high", "miss", ["tsan"], 2, 5, "waiter",
  "谓词按「边沿」而非「电平」消费：多个等待者共享一次性信号",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool one_shot = false;
static std::atomic<int> served{0};
static void waiter(int id){
  std::unique_lock<std::mutex> lk(m);
  while (!one_shot) cv.wait(lk);
  /*DEFECT: 谓词是「一次性信号」，被第一个等待者读走后不复位：
             第二个等待者进入 wait 时谓词已为 true，会立刻通过（虚假通过），
             语义上等于同一份资源被消费两次 */
  served.fetch_add(1, std::memory_order_release);
  (void)id;
}
static void trigger(){
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    one_shot = true;
  }
  cv.notify_all();
}
int main(){
  std::thread a(waiter, 1), b(waiter, 2), c(trigger);
  a.join(); b.join(); c.join();
  std::printf("E192 served=%d\n", served.load());
  return 0;
}
''',
  "2 等待者共享一次性边沿信号",
  "边沿谓词被当作电平使用。程序跑完但语义错 → 预期 miss。")

# ---------------------------------------------------------------- E193
S("E193", "condition_variable", "high", "miss", ["tsan"], 2, 5, "waiter",
  "谓词在 notify_all 与 wait 之间被第三方线程清零",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool req = false;
static int handled = 0;
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  while (!req) cv.wait(lk);
  handled = 1;
  /*DEFECT: 处理完成后在锁内把 req 清零（当作「消费掉」），而另一个线程可能正在
             同一次 notify_all 的唤醒里检查谓词 ⇒ 谓词被过早清零，
             后续等待者再也等不到（通知丢失） */
  req = false;
}
static void toggler(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  for (int i = 0; i < 2; ++i){
    {
      std::lock_guard<std::mutex> lk(m);
      req = true;
    }
    cv.notify_all();
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
  }
}
int main(){
  std::thread a(waiter), b(toggler);
  a.join(); b.join();
  std::printf("E193 handled=%d\n", handled);
  return 0;
}
''',
  "1 等待者 + 1 个两次置位/清零的线程",
  "谓词被当作「一次性请求」清零。预期 miss。")

# ---------------------------------------------------------------- E194
S("E194", "condition_variable", "high", "catch", ["tsan"], 2, 5, "waiter",
  "谓词在 notify 路径上完全不加锁修改",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool quit_req = false;          // 谓词：无锁读写
static std::atomic<int> loops{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: 谓词 quit_req 由 notifier 无锁写，这里在锁内读：
             两者构成数据竞争（编译器可把读提升到循环外 ⇒ 永久阻塞或虚假通过） */
  while (!quit_req) cv.wait(lk);
  loops.fetch_add(1, std::memory_order_release);
}
static void notifier(){
  for (int i = 0; i < 100000; ++i) loops.fetch_add(1, std::memory_order_relaxed);
  /*DEFECT: 谓词完全不加锁修改 */
  quit_req = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(notifier);
  a.join(); b.join();
  std::printf("E194 loops=%d\n", loops.load());
  return 0;
}
''',
  "2 线程：谓词在通知侧完全不加锁写",
  "谓词无锁写 + 锁内读 → 真实数据竞争 → 预期 TSan catch。")

# ---------------------------------------------------------------- E195
S("E195", "condition_variable", "high", "catch", ["tsan"], 3, 5, "notifier",
  "多个通知者无锁改谓词，等待者在锁内读（竞争 + 唤醒丢失）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool stop = false;              // 无锁写
static int counter = 0;                // 无锁写
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: 谓词 stop 由两个通知者无锁写，这里锁内读 ⇒ 数据竞争 */
  while (!stop) cv.wait(lk);
  std::printf("E195 counter=%d\n", counter);   // counter 也是无锁写的非原子变量
}
static void notifier(int id){
  /*DEFECT: counter / stop 都不加锁修改 */
  for (int i = 0; i < 50000; ++i) counter += id;
  stop = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(notifier, 1), c(notifier, 2);
  a.join(); b.join(); c.join();
  std::printf("E195 final=%d\n", counter);
  return 0;
}
''',
  "1 等待者 + 2 个无锁通知者",
  "通知侧无锁写谓词与共享计数 → 真实数据竞争 → 预期 TSan catch。")

# ---------------------------------------------------------------- E196
S("E196", "condition_variable", "high", "catch", ["tsan"], 2, 5, "waiter",
  "谓词读取在锁外（wait 返回后解锁再读谓词）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool state_changed = false;
static int version = 0;                // 非原子版本号
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: wait 内部谓词正确，但醒来后解锁再读 version */
  if (!cv.wait_for(lk, std::chrono::milliseconds(50), []{ return state_changed; })){}
  lk.unlock();
  /*DEFECT: 无锁读非原子 version，而 updater 仍在锁内持续 ++version ⇒ 数据竞争 */
  long s = 0;
  for (int i = 0; i < 400000; ++i) s += version;
  std::printf("E196 sum=%ld\n", s);
}
static void updater(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  for (int i = 0; i < 400000; ++i){
    {
      std::lock_guard<std::mutex> lk(m);
      ++version;                          // 写始终在锁内
      state_changed = true;
    }
    cv.notify_all();
  }
}
int main(){
  std::thread a(waiter), b(updater);
  waiting.store(1, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：wait 后解锁再读非原子版本号",
  "解锁后读共享状态 → 真实数据竞争 → 预期 TSan catch。")

# ---------------------------------------------------------------- E197
S("E197", "condition_variable", "high", "catch", ["tsan"], 2, 5, "notifier",
  "notify 在不持锁时调用，且谓词更新也在锁外（通知必丢）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool job_ready = false;
static std::atomic<int> picked{0}, waiting{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  while (!job_ready) cv.wait(lk);
  picked.store(1, std::memory_order_release);
}
static void dispatcher(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  /*DEFECT: 谓词在锁外写 + notify 也在锁外：
             两步之间 worker 可能正在 wait（或还没进入 wait）⇒ 通知永久丢失，
             worker 永久阻塞；且锁外写谓词与 worker 锁内读构成数据竞争 */
  job_ready = true;
  cv.notify_all();
}
int main(){
  std::thread a(worker), b(dispatcher);
  a.join(); b.join();
  std::printf("E197 picked=%d\n", picked.load());
  return 0;
}
''',
  "2 线程：谓词与 notify 都在锁外",
  "通知丢失导致永久阻塞 + 无锁写谓词的数据竞争 → 记为阻塞触发。")

# ---------------------------------------------------------------- E198
S("E198", "condition_variable", "high", "miss", ["tsan"], 2, 5, "waiter",
  "notify_one 在有多个「不同谓词」的等待者时通知了错误的目标",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool low_water = false, high_water = false;
static std::atomic<int> woke_low{0}, woke_high{0};
static void waiter_low(){
  std::unique_lock<std::mutex> lk(m);
  while (!low_water) cv.wait(lk);
  woke_low.store(1, std::memory_order_release);
}
static void waiter_high(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: 同一个 cv 上挂着两个语义不同的谓词（low_water / high_water），
             通知方无法指定唤醒哪一个，只能 notify_all 或赌 notify_one 恰好唤醒对的 */
  while (!high_water) cv.wait(lk);
  woke_high.store(1, std::memory_order_release);
}
static void notifier(){
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  {
    std::lock_guard<std::mutex> lk(m);
    low_water = true;                  // 只满足 low_water
  }
  cv.notify_one();                     // DEFECT: 可能唤醒的是 high_water 的等待者
}
int main(){
  std::thread a(waiter_low), b(waiter_high), c(notifier);
  a.join(); b.join(); c.join();
  std::printf("E198 low=%d high=%d\n", woke_low.load(), woke_high.load());
  return 0;
}
''',
  "2 个不同谓词的等待者共用一个 cv + 1 个 notify_one",
  "共享 cv 上的多谓词与 notify_one 的不确定性。是否死锁取决于调度 → 预期 miss（时序相关）。")

# ---------------------------------------------------------------- E199
S("E199", "condition_variable", "high", "miss", ["tsan"], 1, 5, "recursive_worker",
  "condition_variable_any 与 recursive_mutex 搭配：wait 只释放一层锁",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::recursive_mutex m;
static std::condition_variable_any cv;
static bool flag = false;
static std::atomic<bool> resume{false};
static void recursive_worker(){
  std::unique_lock<std::recursive_mutex> lk(m);
  lk.lock();                           // 递归计数 = 2
  resume.store(true, std::memory_order_release);
  /*DEFECT: condition_variable_any 配 recursive_mutex：wait 只解锁一层，
             m 仍被本线程持有（计数 1）⇒ 谓词只能由需要完整锁的线程来改，
             而那把锁永远拿不到 ⇒ 永久阻塞 */
  cv.wait(lk, []{ return flag; });
  std::printf("E199 resumed\n");
}
static void setter(){
  while (!resume.load(std::memory_order_acquire)){}
  std::lock_guard<std::recursive_mutex> g(m);
  flag = true;
  cv.notify_all();
}
int main(){
  std::thread a(recursive_worker), b(setter);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：condition_variable_any + recursive_mutex 递归计数",
  "CV 只能配「wait 能完全解锁」的 mutex。预期记为阻塞触发。")

# ---------------------------------------------------------------- E200
S("E200", "condition_variable", "high", "miss", ["tsan"], 2, 5, "shut_down",
  "关停流程：先 notify_all 让等待者醒来，但此时状态标志尚未置位",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool shutting_down = false;
static bool workers_stopped = false;
static std::atomic<int> finished{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  while (!shutting_down) cv.wait(lk);
  /*DEFECT: 被唤醒时 shutting_down 仍可能是 false（通知早于置位）：
             循环会重新 wait，而关停方已经退出 ⇒ 永久阻塞 */
  while (!workers_stopped) cv.wait(lk);
  finished.fetch_add(1, std::memory_order_release);
}
static void shutdown(){
  cv.notify_all();                     // DEFECT: 先唤醒
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    shutting_down = true;              // 后置位
    workers_stopped = true;
  }
  cv.notify_all();
}
int main(){
  std::thread a(worker), b(worker), c(shutdown);
  a.join(); b.join(); c.join();
  std::printf("E200 finished=%d\n", finished.load());
  return 0;
}
''',
  "2 个工作线程 + 1 个关停线程，先 notify 后置位",
  "关停时序颠倒导致通知丢失。是否永久阻塞取决于调度 → 预期 miss（时序相关）。")
