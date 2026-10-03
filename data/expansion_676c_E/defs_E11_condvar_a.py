#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E11_condvar_a.py — condition_variable 缺陷 E171..E185（15 个）。

三类后果分别标注：
  (a) 虚假唤醒后继续执行（程序跑完但逻辑错）→ 无检测器 → miss
  (b) 通知丢失导致永久阻塞（程序超时挂起）→ 记为「死锁触发」
  (c) 谓词被无锁读写（真实数据竞争）→ TSan 可捕获
"""
from _dsl import S

# ---------------------------------------------------------------- E171
S("E171", "condition_variable", "high", "miss", ["tsan"], 2, 5, "worker",
  "cv.wait(lk) 不带谓词：被唤醒后无条件继续（虚假唤醒）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool ready = false;
static int work_done = 0;
static std::atomic<int> waiting{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: wait 不带谓词：虚假唤醒（或过早的 notify）会让线程在 ready 仍为 false 时继续执行 */
  cv.wait(lk);
  work_done = 1;                       // 资源其实还没准备好
}
static void waker(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  /*DEFECT: 此刻 ready 仍是 false（数据还没就绪），却发了通知 */
  cv.notify_all();
}
int main(){
  std::thread a(worker), b(waker);
  a.join(); b.join();
  std::printf("E171 work_done=%d ready=%d\n", work_done, (int)ready);
  return 0;
}
''',
  "2 线程：waiter 不检查谓词，waker 在数据未就绪时通知",
  "虚假唤醒型误用。程序能跑完但状态错误，sanitizer 无从判断 → 预期 miss（真实盲区）。")

# ---------------------------------------------------------------- E172
S("E172", "condition_variable", "high", "miss", ["tsan"], 2, 5, "worker",
  "多次 wait 共用一个布尔谓词但只在第一次检查",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static int produced = 0, consumed = 0;
static std::atomic<int> waiting{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: 只在进入前检查一次谓词，之后连续 wait 三次都不重新检查：
     第二/三次 wait 可能在条件已满足的情况下仍被唤醒并继续 */
  if (produced < 3) cv.wait(lk);
  cv.wait(lk);
  cv.wait(lk);
  consumed = 3;                        // 未验证 produced 是否真的到 3
}
static void producer(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  for (int i = 1; i <= 3; ++i){
    {
      std::lock_guard<std::mutex> lk(m);
      produced = i;
    }
    cv.notify_all();
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
  }
}
int main(){
  std::thread a(worker), b(producer);
  a.join(); b.join();
  std::printf("E172 produced=%d consumed=%d\n", produced, consumed);
  return 0;
}
''',
  "2 线程：worker 连续三次 wait 只检查一次谓词",
  "谓词检查缺失型误用。预期 miss。")

# ---------------------------------------------------------------- E173
S("E173", "condition_variable", "high", "catch", ["tsan"], 2, 5, "reader",
  "wait 返回后读取未被锁保护的共享状态（真实数据竞争）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool ready = false;
static int shared_total = 0;           // 非原子，且 wait 后不加锁就读
static std::atomic<int> waiting{0};
static void reader(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: wait 不带谓词：被唤醒时 ready 仍可能是 false，读者不该继续 */
  cv.wait(lk);
  lk.unlock();
  /*DEFECT: 解锁后无锁读非原子 shared_total，与 writer 的无锁写并发 ⇒ 数据竞争 */
  long t = 0;
  for (int i = 0; i < 300000; ++i) t += shared_total;
  std::printf("E173 total=%ld\n", t);
}
static void writer(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  /*DEFECT: 通知早于数据就绪 —— 读者会在数据还没写完时醒来 */
  cv.notify_all();
  for (int i = 0; i < 300000; ++i) shared_total += i;   // 无锁写非原子变量
  std::lock_guard<std::mutex> lk(m);
  ready = true;
  cv.notify_all();
}
int main(){
  std::thread a(reader), b(writer);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：waiter 醒后无锁读非原子计数，writer 无锁写",
  "虚假唤醒 + 无锁访问共享状态，真实数据竞争 → 预期 TSan catch。")

# ---------------------------------------------------------------- E174
S("E174", "condition_variable", "high", "miss", ["tsan"], 2, 5, "consumer",
  "wait 无谓词，且通知与「数据准备」之间的顺序倒置",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static int slot = -1;
static int taken = -1;
static std::atomic<int> waiting{0};
static void consumer(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: wait 不带谓词：即使 slot 还没被填，醒来也会直接取走 slot */
  cv.wait(lk);
  taken = slot;                        // slot 可能仍是 -1
}
static void producer(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  {
    std::lock_guard<std::mutex> lk(m);
    slot = 42;
  }
  cv.notify_all();                     // DEFECT: 通知与数据准备之间没有内存序约束的配对
}
int main(){
  std::thread a(consumer), b(producer);
  a.join(); b.join();
  std::printf("E174 taken=%d\n", taken);
  return 0;
}
''',
  "2 线程：消费者不检查谓词，通知早于数据可用",
  "预期 miss。")

# ---------------------------------------------------------------- E175
S("E175", "condition_variable", "high", "catch", ["tsan"], 2, 5, "consumer",
  "通知早于 wait（丢失唤醒）：notify 在 wait 之前发生",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool ready = false;
static std::atomic<int> notified{0}, finished{0};
static void consumer(){
  std::unique_lock<std::mutex> lk(m);
  while (!ready) cv.wait(lk);          // 谓词本身是对的
  finished.store(1, std::memory_order_release);
}
static void producer(){
  /*DEFECT: 谓词 ready 完全在锁外写 —— 这才是丢失唤醒的真正根因：
     consumer「检查谓词 → 真正阻塞进 wait」之间存在窗口，
     ready=true + notify_all 可以整个从窗口里滑过去，
     于是 consumer 带着（它以为没变过的）谓词进入阻塞，再也收不到通知。
     注意：如果谓词是在锁内写的，notify 的先后顺序其实无关紧要——
     正是「谓词不受锁保护」让这条通知变得不可靠。 */
  notified.store(1, std::memory_order_release);
  ready = true;
  cv.notify_all();
}
int main(){
  std::thread a(consumer), b(producer);
  a.join(); b.join();
  std::printf("E175 finished=%d\n", finished.load());
  return 0;
}
''',
  "2 线程：谓词在锁外写 + notify_all，consumer 在锁内检查谓词",
  "丢失唤醒的根因是「谓词不受mutex 保护」。谓词的检查/写入之间没有 happens-before ⇒ "
  "TSan 能稳定抓到 ready 上的数据竞争；至于是否真的永久阻塞取决于窗口是否命中，"
  "实测触发率见验收报告。")

# ---------------------------------------------------------------- E176
S("E176", "condition_variable", "high", "catch", ["tsan"], 2, 5, "waiter",
  "notify_one 只有一个等待者时通知了「错误的那一个」（实际无通知到达）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool flag = false;
static std::atomic<int> woke{0};
static void waiter(int id){
  std::unique_lock<std::mutex> lk(m);
  if (id == 0){
    while (!flag) cv.wait(lk);
    woke.fetch_add(1, std::memory_order_release);
  } else {
    /*DEFECT: 第二个等待者用 notify_one 语义去「预留」通知，但它自己并不在等：
       通知被投递到系统选择的某个等待者，可能正好唤醒 id==0 之外的路径，
       而真正需要唤醒的等待者再无通知 ⇒ 永久阻塞 */
    while (!flag) cv.wait(lk);
    woke.fetch_add(1, std::memory_order_release);
  }
}
static void setter(){
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    flag = true;
  }
  /*DEFECT: 有两个等待者却只 notify_one()：若一次通知未能唤醒全部依赖该谓词的等待者，
     剩余等待者永久阻塞 */
  cv.notify_one();
}
int main(){
  std::thread a(waiter, 0), b(waiter, 1), c(setter);
  a.join(); b.join(); c.join();
  std::printf("E176 woke=%d\n", woke.load());
  return 0;
}
''',
  "2 个等待者 + 1 个通知者，只发 notify_one",
  "通知丢失导致部分等待者永久阻塞（超时挂起）。")

# ---------------------------------------------------------------- E177
S("E177", "condition_variable", "high", "miss", ["tsan"], 2, 5, "worker",
  "谓词在 wait 之前被判断一次就再也不检查（循环外判断）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static int items = 0;
static std::atomic<int> waiting{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: 谓词判断写在循环外：第一次检查通过后，后续的 wait 就不再验证条件，
     醒来即认为条件成立 */
  if (items > 0){
    cv.wait(lk);
  }
  std::printf("E177 items=%d\n", items);
}
static void producer(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    items = 3;
  }
  cv.notify_all();
}
int main(){
  std::thread a(worker), b(producer);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：谓词判断在循环外",
  "预期 miss。")

# ---------------------------------------------------------------- E178
S("E178", "condition_variable", "high", "catch", ["tsan"], 2, 5, "submitter",
  "先 notify 再设置谓词（顺序颠倒），等待者永久阻塞",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool submitted = false;
static std::atomic<int> got{0};
static void submitter(){
  /*DEFECT: 谓词 submitted 在锁外被读改写（waiter 在锁内读，这里在锁外写）：
     通知与谓词更新都没有与「等待者进入阻塞」这一动作建立任何同步关系，
     通知可以从「检查谓词」与「真正阻塞」之间的窗口里整个漏过去 ⇒ 永久阻塞 */
  submitted = true;
  cv.notify_all();
  std::printf("E178 submitted\n");
}
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  while (!submitted) cv.wait(lk);
  got.store(1, std::memory_order_release);
}
int main(){
  std::thread a(submitter), b(waiter);
  a.join(); b.join();
  std::printf("E178 got=%d\n", got.load());
  return 0;
}
''',
  "2 线程：谓词在锁外写，通知与谓词更新都无同步",
  "谓词不受mutex 保护 ⇒ TSan 可稳定抓到 submitted 上的数据竞争；"
  "是否永久阻塞取决于「检查谓词→阻塞」窗口是否被命中，触发率见验收报告。")

# ---------------------------------------------------------------- E179
S("E179", "condition_variable", "high", "miss", ["tsan"], 3, 5, "waiter",
  "三个等待者共用一个谓词但只 notify_one 两次（依赖运气）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool batch_done = false;
static std::atomic<int> done_count{0}, wake_count{0};
static void waiter(int id){
  std::unique_lock<std::mutex> lk(m);
  while (!batch_done) cv.wait(lk);
  done_count.fetch_add(1, std::memory_order_release);
  (void)id;
}
static void notifier(){
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  {
    std::lock_guard<std::mutex> lk(m);
    batch_done = true;
  }
  /*DEFECT: 三个等待者共用一个谓词，却只在「相信一次 notify_one 能唤醒全部」的前提下
     发了三次通知——一旦某次通知在等待者尚未进入 wait 时发出，就永久丢失 */
  for (int i = 0; i < 3; ++i){
    cv.notify_one();
    wake_count.fetch_add(1, std::memory_order_relaxed);
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
  }
}
int main(){
  std::thread a(waiter, 0), b(waiter, 1), c(waiter, 2), d(notifier);
  a.join(); b.join(); c.join(); d.join();
  std::printf("E179 done=%d wakes=%d\n", done_count.load(), wake_count.load());
  return 0;
}
''',
  "3 个等待者 + 1 个通知者，逐次 notify_one",
  "多次 notify_one 覆盖多等待者的时序依赖缺陷。是否永久阻塞取决于调度 → 预期 miss（时序相关，记录复现率）。")

# ---------------------------------------------------------------- E180
S("E180", "condition_variable", "high", "miss", ["tsan"], 2, 5, "worker",
  "notify_all 写成 notify_one（多等待者漏唤醒）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool shutdown_req = false;
static std::atomic<int> exited{0};
static void worker(int id){
  std::unique_lock<std::mutex> lk(m);
  while (!shutdown_req) cv.wait(lk);
  exited.fetch_add(1, std::memory_order_release);
  (void)id;
}
static void controller(){
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  {
    std::lock_guard<std::mutex> lk(m);
    shutdown_req = true;
  }
  /*DEFECT: 有两个等待者却只 notify_one：只有一个能被唤醒，另一个永久阻塞 */
  cv.notify_one();
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  cv.notify_one();
}
int main(){
  std::thread a(worker, 1), b(worker, 2), c(controller);
  a.join(); b.join(); c.join();
  std::printf("E180 exited=%d\n", exited.load());
  return 0;
}
''',
  "2 等待者 + 控制器分两次 notify_one",
  "notify_all 误用为 notify_one。预期 miss。")

# ---------------------------------------------------------------- E181
S("E181", "condition_variable", "high", "miss", ["tsan"], 2, 5, "waiter",
  "等待「计数达到 N」但只 notify 了一次（notify 次数与谓词语义不匹配）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static int arrived = 0;
static std::atomic<int> left{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: 谓词是「arrived >= 3」，但通知方每来一个就 notify_all 一次；
         醒来后若 arrived 仍不满足（因为通知早于 arrived 更新），等待者继续等，
         而最后一次 notify 已经在它重新 wait 之前发完 ⇒ 永久阻塞 */
  while (arrived < 3) cv.wait(lk);
  left.store(1, std::memory_order_release);
}
static void arrivals(){
  for (int i = 0; i < 3; ++i){
    {
      std::lock_guard<std::mutex> lk(m);
      ++arrived;
    }
    cv.notify_all();
  }
}
int main(){
  std::thread a(waiter), b(arrivals);
  a.join(); b.join();
  std::printf("E181 left=%d arrived=%d\n", left.load(), arrived);
  return 0;
}
''',
  "1 等待者 + 3 次到达通知",
  "谓词与通知节奏不匹配。本例中更新在通知前，通常能收敛 ⇒ 预期 miss（时序相关）。")

# ---------------------------------------------------------------- E182
S("E182", "condition_variable", "high", "catch", ["tsan"], 2, 5, "waiter",
  "谓词标志被无锁写入（真实数据竞争 + 丢失唤醒）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool ready = false;             // 谓词
static int payload = 0;                // 非原子
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: 谓词 ready 会被另一线程「无锁写」，wait 的谓词检查与那次写构成数据竞争，
     编译器/CPU 可把它缓存成 false ⇒ 丢失唤醒 */
  while (!ready) cv.wait(lk);
  std::printf("E182 payload=%d\n", payload);
}
static void setter(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  payload = 99;                        // 非原子写
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  /*DEFECT: 不持有 m 就修改谓词 ready：与 wait 里的谓词读是数据竞争 */
  ready = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(setter);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：谓词被无锁写，wait 侧在锁内读",
  "谓词无锁访问是真实数据竞争 → 预期 TSan catch（同时也是丢失唤醒的根因）。")

# ---------------------------------------------------------------- E183
S("E183", "condition_variable", "high", "miss", ["tsan"], 2, 5, "worker",
  "条件变量在正确的锁上，但「重复通知」被当作「多次许可」消费",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static int permits = 0;
static std::atomic<int> consumed{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  while (permits <= 0) cv.wait(lk);
  --permits;                          // 谓词写法正确
  consumed.fetch_add(1, std::memory_order_release);
}
static void issuer(){
  for (int i = 0; i < 3; ++i){
    {
      std::lock_guard<std::mutex> lk(m);
      ++permits;
    }
    /*DEFECT: 条件变量不是「计数信号量」：三次 notify 并不携带「三份许可」的语义，
             两次通知之间若谓词已被消费，第三次 notify 就是空通知（丢失许可） */
    cv.notify_all();
  }
}
int main(){
  std::thread a(worker), b(issuer);
  a.join(); b.join();
  std::printf("E183 consumed=%d permits=%d\n", consumed.load(), permits);
  return 0;
}
''',
  "1 等待者 + 3 次许可发放",
  "把条件变量当信号量用的经典误用。预期 miss。")

# ---------------------------------------------------------------- E184
S("E184", "condition_variable", "high", "miss", ["tsan"], 2, 5, "waiter",
  "wait_for 超时返回后不重新检查谓词，直接继续",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool done = false;
static int result = 0;
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: wait_for 的返回值被丢弃：超时返回后不检查谓词，直接把「还没完成」当成完成 */
  cv.wait_for(lk, std::chrono::milliseconds(20));
  result = done ? 1 : -1;
  std::printf("E184 result=%d done=%d\n", result, (int)done);
}
static void slow(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  std::this_thread::sleep_for(std::chrono::milliseconds(200));  // 远超超时时间
  {
    std::lock_guard<std::mutex> lk(m);
    done = true;
  }
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(slow);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：wait_for 超时后不检查谓词",
  "超时处理缺失。预期 miss。")

# ---------------------------------------------------------------- E185
S("E185", "condition_variable", "high", "catch", ["tsan"], 2, 5, "waiter",
  "wait_for 超时后走「重试」分支，重试分支无锁读写共享状态",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool done = false;
static long attempts = 0;              // 非原子，被两条路径并发访问
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: wait_for 超时后进入重试分支，而重试分支在释放锁的情况下自增非原子
     attempts（与 slow 线程对同一变量的写并发）⇒ 数据竞争 */
  if (!cv.wait_for(lk, std::chrono::milliseconds(20), []{ return done; })){
    lk.unlock();
    for (int i = 0; i < 100000; ++i) ++attempts;
    lk.lock();
  }
  std::printf("E185 attempts=%ld done=%d\n", attempts, (int)done);
}
static void slow(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  for (int i = 0; i < 100000; ++i) ++attempts;      // 无锁写非原子变量
  std::this_thread::sleep_for(std::chrono::milliseconds(30));
  {
    std::lock_guard<std::mutex> lk(m);
    done = true;
  }
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(slow);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：超时重试分支无锁自增非原子计数",
  "超时路径逃逸出锁保护造成真实数据竞争 → 预期 TSan catch。")
