#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E09_lockpri_a.py — lock_priority_inversion 缺陷 E141..E155（15 个）。

诚实边界（对所有 lock_priority_inversion 样本适用）：
真正的优先级反转需要「实时调度器 + 明确的线程优先级」。用户态 std::thread
没有优先级接口，因此这些样本建模的是**导致反转的代码形态**：
低优先级线程在持锁期间做长耗时操作 / 阻塞调用，高优先级线程等这把锁，
中优先级线程又抢占低优先级线程。通用调度器上「中优先级抢占」这一步不会
真的发生 ⇒ 绝大多数样本没有任何 sanitizer 会报（真实盲区）。
其中少数样本额外植入了真实数据竞争（中间优先级线程绕过锁写共享状态），
这类可以被 TSan 捕获，用于区分「盲区」与「样本本身不成立」。
"""
from _dsl import S

# ---------------------------------------------------------------- E141
S("E141", "lock_priority_inversion", "high", "miss", ["tsan"], 3, 5, "low_prio",
  "低优先级线程持锁做长耗时计算，高优先级线程等锁，中优先级线程忙等抢占",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static long acc = 0;
static std::atomic<int> stage{0};
static void low_prio(){
  std::lock_guard<std::mutex> lk(m);
  /*DEFECT: 低优先级线程持锁做百万次累加（等价于持锁执行耗时操作）：
     高优先级线程在下面被阻塞，而中优先级线程会抢占本线程 ⇒ 优先级反转三要素齐备 */
  stage.store(1, std::memory_order_release);
  for (long i = 0; i < 3000000; ++i) acc += i % 7;
  stage.store(2, std::memory_order_release);
}
static void high_prio(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程必须等低优先级线程释放锁才能推进 */
  std::lock_guard<std::mutex> lk(m);
  acc += 1;
  stage.store(3, std::memory_order_release);
}
static void mid_prio(){
  while (stage.load(std::memory_order_acquire) < 1){}
  while (stage.load(std::memory_order_acquire) < 2){
    /*DEFECT: 中优先级线程抢占低优先级线程的时间片，进一步推迟锁的释放 */
    std::this_thread::yield();
  }
}
int main(){
  std::thread a(low_prio), b(high_prio), c(mid_prio);
  a.join(); b.join(); c.join();
  std::printf("E141 acc=%ld stage=%d\n", acc, stage.load());
  return 0;
}
''',
  "3 线程：低优先级持锁长算 + 高优先级等锁 + 中优先级抢占",
  "优先级反转的完整三要素代码形态。通用调度器上无检测器可报 → 预期 miss（真实盲区）。")

# ---------------------------------------------------------------- E142
S("E142", "lock_priority_inversion", "high", "miss", ["tsan"], 3, 5, "low",
  "低优先级线程持锁期间做浮点重算，高优先级线程等锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static double table[64];
static std::atomic<int> stage{0};
static void low(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做 64 轮浮点重算（持锁耗时操作）：锁被低优先级线程长时间占用 */
  for (int r = 0; r < 64; ++r)
    for (int i = 0; i < 64; ++i) table[i] = table[i] * 1.0001 + r;
  stage.store(2, std::memory_order_release);
}
static void high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等这把锁；无优先级继承机制时只能被动等待 */
  std::lock_guard<std::mutex> lk(m);
  table[0] += 1.0;
  stage.store(3, std::memory_order_release);
}
static void mid(){
  while (stage.load(std::memory_order_acquire) < 1){}
  while (stage.load(std::memory_order_acquire) < 2) std::this_thread::yield();
}
int main(){
  std::thread a(low), b(high), c(mid);
  a.join(); b.join(); c.join();
  std::printf("E142 t0=%f\n", table[0]);
  return 0;
}
''',
  "3 线程：低优先级持锁做浮点重算",
  "持锁耗时操作型反转。预期 miss。")

# ---------------------------------------------------------------- E143
S("E143", "lock_priority_inversion", "high", "catch", ["tsan"], 3, 5, "mid",
  "中优先级线程绕过锁写共享状态（与持锁的低优先级线程形成真实竞争）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static int shared_slots[8] = {0, 0, 0, 0, 0, 0, 0, 0};
static std::atomic<int> stage{0};
static void low(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 低优先级线程持锁做长耗时操作 */
  for (int k = 0; k < 40000; ++k)
    for (int i = 0; i < 8; ++i) shared_slots[i] += 1;
  stage.store(2, std::memory_order_release);
}
static void high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  std::lock_guard<std::mutex> lk(m);
  shared_slots[0] += 1000;
  stage.store(3, std::memory_order_release);
}
static void mid(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 中优先级线程为了「抢占」而绕过锁直接写共享数组：
     与持锁线程对同一内存并发读写 ⇒ 真实数据竞争（不只是优先级反转） */
  for (int k = 0; k < 40000; ++k) shared_slots[7] += 2;
  while (stage.load(std::memory_order_acquire) < 2){}
}
int main(){
  std::thread a(low), b(high), c(mid);
  a.join(); b.join(); c.join();
  std::printf("E143 s7=%d\n", shared_slots[7]);
  return 0;
}
''',
  "3 线程：中优先级线程无锁写共享数组",
  "本样本除优先级反转外还植入了真实数据竞争，TSan 可捕获 → 预期 catch。")

# ---------------------------------------------------------------- E144
S("E144", "lock_priority_inversion", "high", "miss", ["tsan"], 3, 5, "low_rt",
  "低优先级线程持锁排序，高优先级线程等锁，中优先级线程空转",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <vector>
#include <algorithm>
#include <cstdio>
static std::mutex m;
static std::vector<int> data{5, 3, 9, 1, 7, 2};
static std::atomic<int> stage{0};
static void low_rt(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 低优先级线程持锁做 O(n log n) 排序 + 反复重排：锁被长时间占用 */
  for (int round = 0; round < 2000; ++round){
    std::sort(data.begin(), data.end());
    if (data[0] == 999) break;
  }
  stage.store(2, std::memory_order_release);
}
static void high_rt(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程必须等锁；无 PI（优先级继承）机制 */
  std::lock_guard<std::mutex> lk(m);
  data.push_back(42);
  stage.store(3, std::memory_order_release);
}
static void mid_rt(){
  while (stage.load(std::memory_order_acquire) < 1){}
  while (stage.load(std::memory_order_acquire) < 2) std::this_thread::yield();
}
int main(){
  std::thread a(low_rt), b(high_rt), c(mid_rt);
  a.join(); b.join(); c.join();
  std::printf("E144 n=%zu\n", data.size());
  return 0;
}
''',
  "3 线程：低优先级持锁排序",
  "持锁做重计算型反转。预期 miss。")

# ---------------------------------------------------------------- E145
S("E145", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "low",
  "低优先级线程持锁做内存分配/释放风暴，高优先级线程等锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static int* live = nullptr;
static std::atomic<int> stage{0}, alloc_calls{0};
static void low(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做成千次 new/delete（持锁调用可能阻塞的分配器）：
     缺页 + 分配器内部锁会把持锁时间放大几个数量级 */
  for (int i = 0; i < 20000; ++i){
    int* p = new int[64];
    p[0] = i;
    delete[] p;
    alloc_calls.fetch_add(1, std::memory_order_relaxed);
  }
  stage.store(2, std::memory_order_release);
}
static void high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等这把锁才能更新 live */
  std::lock_guard<std::mutex> lk(m);
  live = new int(1);
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(low), b(high);
  a.join(); b.join();
  delete live;
  std::printf("E145 allocs=%d\n", alloc_calls.load());
  return 0;
}
''',
  "2 线程：低优先级持锁做分配器风暴",
  "持锁调用分配器型反转。预期 miss。")

# ---------------------------------------------------------------- E146
S("E146", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "low",
  "互斥锁无优先级继承：低优先级持锁，高优先级被阻塞且无法提升锁的优先级",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;                       // std::mutex 不提供优先级继承
static int resource = 0;
static std::atomic<int> stage{0};
static void low(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 关键区被低优先级线程拉长，而锁本身不提供优先级继承（PI）：
     持锁者被抢占时，锁的优先级不会跟随高优先级等待者提升 */
  for (long i = 0; i < 2000000; ++i) resource += (int)(i & 1);
  stage.store(2, std::memory_order_release);
}
static void high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程在此阻塞；没有 PI 的话，它的等待无法帮助持锁者尽快退出 */
  std::lock_guard<std::mutex> lk(m);
  resource = -1;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(low), b(high);
  a.join(); b.join();
  std::printf("E146 resource=%d\n", resource);
  return 0;
}
''',
  "2 线程：std::mutex 无优先级继承",
  "PI 缺失型反转（需要实时调度器才能真正观测到时序恶化）→ 预期 miss。")

# ---------------------------------------------------------------- E147
S("E147", "lock_priority_inversion", "high", "miss", ["tsan"], 3, 5, "low",
  "低优先级线程持两把锁做长操作，高优先级线程等其中一把",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex a, b;
static int data[16] = {0};
static std::atomic<int> stage{0};
static void low(){
  std::lock_guard<std::mutex> la(a);
  std::lock_guard<std::mutex> lb(b);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 低优先级线程同时持有两把锁做长耗时变换：
     任何一把被高优先级线程需要时，持锁者都无法被及时抢占让出 */
  for (int round = 0; round < 3000; ++round)
    for (int i = 0; i < 16; ++i) data[i] = data[i] * 3 + round;
  stage.store(2, std::memory_order_release);
}
static void high_a(){
  while (stage.load(std::memory_order_acquire) < 1){}
  std::lock_guard<std::mutex> la(a);
  data[0] += 1;
  stage.store(3, std::memory_order_release);
}
static void high_b(){
  while (stage.load(std::memory_order_acquire) < 1){}
  std::lock_guard<std::mutex> lb(b);
  data[1] += 1;
}
int main(){
  std::thread x(low), y(high_a), z(high_b);
  x.join(); y.join(); z.join();
  std::printf("E147 d0=%d\n", data[0]);
  return 0;
}
''',
  "3 线程：低优先级同时持有两把锁",
  "多锁持有扩大反转窗口。预期 miss。")

# ---------------------------------------------------------------- E148
S("E148", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "low",
  "低优先级线程持锁做字符串/正则匹配，高优先级线程等锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <string>
#include <cstdio>
static std::mutex m;
static std::string blob;
static std::atomic<int> stage{0};
static void low(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做大量字符串构造/拼接（持锁耗时操作） */
  for (int i = 0; i < 20000; ++i) blob += "x";
  stage.store(2, std::memory_order_release);
}
static void high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等锁读取 blob */
  std::lock_guard<std::mutex> lk(m);
  std::printf("E148 len=%zu\n", blob.size());
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(low), b(high);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：低优先级持锁做字符串操作",
  "预期 miss。")

# ---------------------------------------------------------------- E149
S("E149", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "low",
  "低优先级线程持锁做位图/图像处理，高优先级线程等锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static unsigned char img[64][64];
static std::atomic<int> stage{0};
static void low(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做 64x64 像素的滤波运算（持锁耗时计算） */
  for (int pass = 0; pass < 400; ++pass)
    for (int y = 0; y < 64; ++y)
      for (int x = 0; x < 64; ++x)
        img[y][x] = (unsigned char)((img[y][x] * 3 + pass) & 0xFF);
  stage.store(2, std::memory_order_release);
}
static void high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等锁读取像素 */
  std::lock_guard<std::mutex> lk(m);
  std::printf("E149 px=%d\n", img[0][0]);
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(low), b(high);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：低优先级持锁做图像滤波",
  "预期 miss。")

# ---------------------------------------------------------------- E150
S("E150", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "io_holder",
  "持锁执行「类 I/O」阻塞操作（sleep 模拟磁盘/网络等待）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static int state = 0;
static std::atomic<int> stage{0};
static void io_holder(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁进入阻塞等待（等价于持锁做 socket recv / 磁盘读）：
     阻塞期间锁一直被占用，高优先级线程只能干等 */
  std::this_thread::sleep_for(std::chrono::milliseconds(300));
  state = 1;
  stage.store(2, std::memory_order_release);
}
static void urgent(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等这把锁才能推进状态机 */
  std::lock_guard<std::mutex> lk(m);
  state = 2;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(io_holder), b(urgent);
  a.join(); b.join();
  std::printf("E150 state=%d\n", state);
  return 0;
}
''',
  "2 线程：持锁阻塞等待 vs 高优先级等锁",
  "持锁 I/O 是最典型的反转来源。预期 miss。")

# ---------------------------------------------------------------- E151
S("E151", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "net_io",
  "持锁做「网络往返」（sleep 模拟 RTT）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex conn_lock;
static int session = 0;
static std::atomic<int> stage{0};
static void net_io(){
  std::lock_guard<std::mutex> lk(conn_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做网络往返等待（真实项目里就是持锁 recv） */
  std::this_thread::sleep_for(std::chrono::milliseconds(200));
  session = 1;
  stage.store(2, std::memory_order_release);
}
static void heartbeat(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 心跳（高优先级）线程必须等这把锁 */
  std::lock_guard<std::mutex> lk(conn_lock);
  session = 2;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(net_io), b(heartbeat);
  a.join(); b.join();
  std::printf("E151 session=%d\n", session);
  return 0;
}
''',
  "2 线程：持锁网络等待",
  "预期 miss。")

# ---------------------------------------------------------------- E152
S("E152", "lock_priority_inversion", "high", "catch", ["tsan"], 3, 5, "poller",
  "持锁做「日志落盘」等待，同时中优先级线程无锁读日志缓冲",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex log_lock;
static char logbuf[256];
static std::atomic<int> stage{0};
static void flush(){
  std::lock_guard<std::mutex> lk(log_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做长时间「落盘」+ 反复重填缓冲，锁被长时间独占 */
  for (int k = 0; k < 3000; ++k){
    for (int i = 0; i < 256; ++i) logbuf[i] = 'a' + ((k + i) % 26);
    if ((k % 512) == 0) std::this_thread::sleep_for(std::chrono::microseconds(80));
  }
  stage.store(2, std::memory_order_release);
}
static void alert(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级告警线程要等这把锁才能写告警 */
  std::lock_guard<std::mutex> lk(log_lock);
  logbuf[0] = 'Z';
  stage.store(3, std::memory_order_release);
}
static void tail(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 中优先级「日志采集」线程绕过锁直接读 logbuf，
     与持锁线程的写在同一时间段内并发访问同一缓冲区 ⇒ 真实数据竞争 */
  int sum = 0;
  for (int k = 0; k < 300000; ++k) sum += logbuf[k % 256];
  std::printf("E152 sum=%d\n", sum);
  while (stage.load(std::memory_order_acquire) < 2){}
}
int main(){
  std::thread a(flush), b(alert), c(tail);
  a.join(); b.join(); c.join();
  std::printf("E152 logbuf0=%c\n", logbuf[0]);
  return 0;
}
''',
  "3 线程：落盘等待 + 无锁日志采集",
  "除反转形态外还植入真实数据竞争 → 预期 TSan catch。")

# ---------------------------------------------------------------- E153
S("E153", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "slow_consumer",
  "持锁等待慢速消费者（sleep 模拟背压）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex q_lock;
static int queue_len = 0;
static std::atomic<int> stage{0};
static void producer(){
  std::lock_guard<std::mutex> lk(q_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁等待下游消费（背压），锁在阻塞期间一直被占 */
  std::this_thread::sleep_for(std::chrono::milliseconds(200));
  queue_len += 10;
  stage.store(2, std::memory_order_release);
}
static void urgent_producer(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 紧急生产者等同一把锁 */
  std::lock_guard<std::mutex> lk(q_lock);
  queue_len += 1;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(producer), b(urgent_producer);
  a.join(); b.join();
  std::printf("E153 qlen=%d\n", queue_len);
  return 0;
}
''',
  "2 线程：持锁背压",
  "预期 miss。")

# ---------------------------------------------------------------- E154
S("E154", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "rpc",
  "持锁执行 RPC（sleep 模拟往返），高优先级线程等锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex rpc_lock;
static int rpc_result = 0;
static std::atomic<int> stage{0};
static void do_rpc(){
  std::lock_guard<std::mutex> lk(rpc_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做 RPC 往返（真实项目里绝不允许，但确实存在） */
  std::this_thread::sleep_for(std::chrono::milliseconds(180));
  rpc_result = 1;
  stage.store(2, std::memory_order_release);
}
static void urgent_rpc(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级调用等锁 */
  std::lock_guard<std::mutex> lk(rpc_lock);
  rpc_result = 2;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(do_rpc), b(urgent_rpc);
  a.join(); b.join();
  std::printf("E154 rpc=%d\n", rpc_result);
  return 0;
}
''',
  "2 线程：持锁 RPC",
  "预期 miss。")

# ---------------------------------------------------------------- E155
S("E155", "lock_priority_inversion", "high", "catch", ["tsan"], 3, 5, "irq_like",
  "「中断处理器」形态的线程直接获取用户态锁，与持锁线程并发",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex dev_lock;
static int dev_regs[8] = {0};
static std::atomic<int> in_isr{0}, stage{0};
static void driver_thread(){
  std::lock_guard<std::mutex> lk(dev_lock);
  in_isr.store(1, std::memory_order_release);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 驱动持锁做一长串寄存器访问，锁被长时间占用 */
  for (int k = 0; k < 200000; ++k)
    for (int i = 0; i < 8; ++i) dev_regs[i] += k;
  stage.store(2, std::memory_order_release);
}
static void isr_like(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 「中断服务程序」在用户态用线程模拟，却直接获取驱动正在持有的用户态锁：
     真实系统里中断上下文获取可能被中断的锁 ⇒ 锁顺序反转 / 系统级卡死 */
  std::lock_guard<std::mutex> lk(dev_lock);
  dev_regs[0] = 0xFF;
}
static void deferred(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 延后处理线程无锁写同一寄存器组，与驱动线程并发 ⇒ 真实数据竞争 */
  for (int k = 0; k < 200000; ++k) dev_regs[7] ^= k;
  while (stage.load(std::memory_order_acquire) < 2){}
}
int main(){
  std::thread a(driver_thread), b(isr_like), c(deferred);
  a.join(); b.join(); c.join();
  std::printf("E155 r0=%d in_isr=%d\n", dev_regs[0], in_isr.load());
  return 0;
}
''',
  "3 线程：驱动持锁 + 模拟 ISR 取锁 + 延后处理无锁写",
  "中断与用户态锁混用；其中延后处理线程的写入是真实数据竞争 → 预期 TSan catch。")
