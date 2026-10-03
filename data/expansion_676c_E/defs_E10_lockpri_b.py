#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""defs_E10_lockpri_b.py — lock_priority_inversion 缺陷 E156..E170（15 个）。"""
from _dsl import S

# ---------------------------------------------------------------- E156
S("E156", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "rt_consumer",
  "实时消费者与普通生产者共享同一把无优先级继承的锁",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;                  // 无 PI：等待者优先级不会被继承给持锁者
static int sample = 0;
static std::atomic<int> stage{0};
static void rt_consumer(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 实时（高优先级）消费者等一把普通 mutex：
     持锁者若被中优先级线程压制，实时线程的截止期必然被错过 */
  std::lock_guard<std::mutex> lk(m);
  sample = sample + 1;
  stage.store(3, std::memory_order_release);
}
static void normal_producer(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 普通（非实时）线程持锁做长耗时处理 */
  for (long i = 0; i < 4000000; ++i) sample += (int)(i & 3);
  stage.store(2, std::memory_order_release);
}
int main(){
  std::thread a(rt_consumer), b(normal_producer);
  a.join(); b.join();
  std::printf("E156 sample=%d\n", sample);
  return 0;
}
''',
  "2 线程：实时消费者 + 普通持锁者",
  "RT 与非 RT 共享无 PI 锁。预期 miss。")

# ---------------------------------------------------------------- E157
S("E157", "lock_priority_inversion", "high", "miss", ["tsan"], 3, 5, "rt",
  "三个「实时」线程共享锁，低优先级持锁者被中优先级压制",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex bus_lock;
static long long total = 0;
static std::atomic<int> stage{0};
static void rt_low(){
  std::lock_guard<std::mutex> lk(bus_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 最低优先级的总线线程持锁做长时间帧打包 */
  for (int f = 0; f < 20000; ++f) total += f;
  stage.store(2, std::memory_order_release);
}
static void rt_high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  std::lock_guard<std::mutex> lk(bus_lock);
  total += 1;                          /* 关键控制报文，必须按时 */
  stage.store(3, std::memory_order_release);
}
static void rt_mid(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 中优先级线程抢占最低优先级持锁者，令其无法及时释放总线锁 */
  while (stage.load(std::memory_order_acquire) < 2) std::this_thread::yield();
}
int main(){
  std::thread a(rt_low), b(rt_high), c(rt_mid);
  a.join(); b.join(); c.join();
  std::printf("E157 total=%lld\n", total);
  return 0;
}
''',
  "3 线程：RT 高/中/低优先级共享总线锁",
  "RT 经典反转形态。预期 miss。")

# ---------------------------------------------------------------- E158
S("E158", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "rt_render",
  "渲染线程等锁，而持锁线程在做同步磁盘预读（sleep 模拟）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex scene_lock;
static int frame = 0;
static std::atomic<int> stage{0};
static void loader(){
  std::lock_guard<std::mutex> lk(scene_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁等待「同步预读」完成：渲染线程（高优先级）在这段时间完全无法推进 */
  std::this_thread::sleep_for(std::chrono::milliseconds(220));
  frame = 1;
  stage.store(2, std::memory_order_release);
}
static void render(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 渲染线程等锁 */
  std::lock_guard<std::mutex> lk(scene_lock);
  frame = 2;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(loader), b(render);
  a.join(); b.join();
  std::printf("E158 frame=%d\n", frame);
  return 0;
}
''',
  "2 线程：持锁同步预读 vs 渲染等锁",
  "预期 miss。")

# ---------------------------------------------------------------- E159
S("E159", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "rt_dma",
  "DMA 完成回调（高优先级）等锁，持锁者在做用户态大块内存整理",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex dma_lock;
static int dma_state = 0;
static std::atomic<int> stage{0};
static void cpu_worker(){
  std::lock_guard<std::mutex> lk(dma_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做用户态内存整理（页迁移/规整），持续时间长 */
  for (int k = 0; k < 3000; ++k){
    static int scratch[4096];
    for (int i = 0; i < 4096; ++i) scratch[i] = (scratch[i] + k) & 0xFFFF;
    if (scratch[0] == -1) break;
  }
  stage.store(2, std::memory_order_release);
}
static void dma_done(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: DMA 完成中断回调（最高优先级）等这把锁 */
  std::lock_guard<std::mutex> lk(dma_lock);
  dma_state = 1;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(cpu_worker), b(dma_done);
  a.join(); b.join();
  std::printf("E159 dma=%d\n", dma_state);
  return 0;
}
''',
  "2 线程：DMA 回调等锁 vs 用户态内存整理",
  "预期 miss。")

# ---------------------------------------------------------------- E160
S("E160", "lock_priority_inversion", "high", "catch", ["tsan"], 3, 5, "stats",
  "持锁统计线程 + 无锁直写统计数组的高优先级线程",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex stat_lock;
static long stat[8] = {0};
static std::atomic<int> stage{0};
static void sampler(){
  std::lock_guard<std::mutex> lk(stat_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做长时间采样聚合 */
  for (int k = 0; k < 300000; ++k)
    for (int i = 0; i < 8; ++i) stat[i] += (k + i) & 7;
  stage.store(2, std::memory_order_release);
}
static void fast_path(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 快路径（高优先级）直接写统计数组，不取锁：与持锁的采样线程并发访问同一内存 ⇒ 数据竞争 */
  for (int k = 0; k < 300000; ++k) stat[3] += k & 1;
  while (stage.load(std::memory_order_acquire) < 2){}
}
static void reader(){
  while (stage.load(std::memory_order_acquire) < 1){}
  std::lock_guard<std::mutex> lk(stat_lock);
  std::printf("E160 stat3=%ld\n", stat[3]);
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(sampler), b(fast_path), c(reader);
  a.join(); b.join(); c.join();
  return 0;
}
''',
  "3 线程：持锁采样 + 无锁快路径写",
  "含真实数据竞争 → 预期 TSan catch。")

# ---------------------------------------------------------------- E161
S("E161", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "ctrl",
  "控制线程（高优先级）等锁，配置线程（低优先级）持锁做解析",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <string>
#include <cstdio>
static std::mutex cfg_lock;
static std::string cfg = "k=v;k2=v2;k3=v3;k4=v4";
static std::atomic<int> stage{0};
static void cfg_parser(){
  std::lock_guard<std::mutex> lk(cfg_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 低优先级线程持锁做配置解析（字符串切分 + 校验），持续时间长 */
  for (int i = 0; i < 40000; ++i){
    size_t p = cfg.find(';');
    if (p == std::string::npos) break;
    cfg = cfg.substr(p + 1) + ";k=v";
  }
  stage.store(2, std::memory_order_release);
}
static void ctrl(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 控制线程（高优先级）必须等锁才能下发命令 */
  std::lock_guard<std::mutex> lk(cfg_lock);
  cfg = "k=ctrl";
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(cfg_parser), b(ctrl);
  a.join(); b.join();
  std::printf("E161 cfg=%s\n", cfg.c_str());
  return 0;
}
''',
  "2 线程：低优先级持锁解析配置",
  "预期 miss。")

# ---------------------------------------------------------------- E162
S("E162", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "lock_then_block",
  "持锁调用阻塞型函数（条件变量 wait 之外的阻塞，如 join 别的线程）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static int value = 0;
static std::atomic<int> stage{0}, inner_done{0};
static void inner_work(){
  std::this_thread::sleep_for(std::chrono::milliseconds(150));
  inner_done.store(1, std::memory_order_release);
}
static void outer_lock_and_join(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  std::thread t(inner_work);
  /*DEFECT: 持锁 join 另一个线程：锁在等待期间一直被占用，
       而被 join 的线程若需要这把锁就构成完整的死锁/反转结构 */
  t.join();
  value = 1;
  stage.store(2, std::memory_order_release);
}
static void waiter(){
  while (stage.load(std::memory_order_acquire) < 1){}
  std::lock_guard<std::mutex> lk(m);
  value = 2;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(outer_lock_and_join), b(waiter);
  a.join(); b.join();
  std::printf("E162 value=%d inner=%d\n", value, inner_done.load());
  return 0;
}
''',
  "2 线程：持锁 join 等锁线程",
  "持锁调用阻塞函数。预期 miss。")

# ---------------------------------------------------------------- E163
S("E163", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "lock_then_sleep",
  "持锁 sleep（等价于持锁等待硬件/外设）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex hw_lock;
static int reg = 0;
static std::atomic<int> stage{0};
static void device_wait(){
  std::lock_guard<std::mutex> lk(hw_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁等待外设（sleep 模拟硬件就绪等待） */
  std::this_thread::sleep_for(std::chrono::milliseconds(240));
  reg = 0x1234;
  stage.store(2, std::memory_order_release);
}
static void poll(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 轮询线程（高优先级）等锁读寄存器 */
  std::lock_guard<std::mutex> lk(hw_lock);
  reg |= 0x1;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(device_wait), b(poll);
  a.join(); b.join();
  std::printf("E163 reg=%x\n", reg);
  return 0;
}
''',
  "2 线程：持锁等外设",
  "预期 miss。")

# ---------------------------------------------------------------- E164
S("E164", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "lock_then_callback",
  "持锁回调外部注册的函数，回调内部又发起阻塞请求",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <functional>
#include <cstdio>
static std::mutex m;
static int state = 0;
static std::atomic<int> stage{0};
static std::function<void()> on_commit;
static void commit(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁调用外部回调，回调内部会发起「阻塞式」请求 */
  on_commit();
  stage.store(2, std::memory_order_release);
}
static void urgent(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等锁 */
  std::lock_guard<std::mutex> lk(m);
  state = 5;
  stage.store(3, std::memory_order_release);
}
int main(){
  on_commit = []{ std::this_thread::sleep_for(std::chrono::milliseconds(160)); };
  std::thread a(commit), b(urgent);
  a.join(); b.join();
  std::printf("E164 state=%d\n", state);
  return 0;
}
''',
  "2 线程：持锁回调 + 高优先级等锁",
  "预期 miss。")

# ---------------------------------------------------------------- E165
S("E165", "lock_priority_inversion", "high", "miss", ["tsan"], 3, 5, "low2",
  "低优先级线程按「低到高」顺序取两把锁，高优先级线程按相反顺序",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex l1, l2;
static int data[32] = {0};
static std::atomic<int> stage{0};
static void low2(){
  std::lock_guard<std::mutex> a(l1);
  std::lock_guard<std::mutex> b(l2);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 低优先级线程持双锁做长耗时处理 */
  for (int k = 0; k < 200000; ++k)
    for (int i = 0; i < 32; ++i) data[i] ^= k;
  stage.store(2, std::memory_order_release);
}
static void high1(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程按 l2->l1 顺序取锁，与低优先级相反 */
  std::lock_guard<std::mutex> b(l2);
  std::lock_guard<std::mutex> a(l1);
  data[0] = 1;
  stage.store(3, std::memory_order_release);
}
static void mid2(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 中优先级线程抢占低优先级持锁者，放大反转 */
  while (stage.load(std::memory_order_acquire) < 2) std::this_thread::yield();
}
int main(){
  std::thread x(low2), y(high1), z(mid2);
  x.join(); y.join(); z.join();
  std::printf("E165 d0=%d\n", data[0]);
  return 0;
}
''',
  "3 线程：嵌套取锁顺序按优先级相反",
  "预期 miss。")

# ---------------------------------------------------------------- E166
S("E166", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "cond_holder",
  "持锁等待条件变量（释放的是外层锁，内层锁仍被占）",
  r'''
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex outer, inner;
static std::condition_variable cv;
static bool ready = false;
static std::atomic<int> stage{0};
static void holder(){
  std::unique_lock<std::mutex> io(outer);
  std::unique_lock<std::mutex> keep(inner);      // 关键区锁，wait 期间不会释放
  stage.store(1, std::memory_order_release);
  /*DEFECT: cv.wait 只释放 io，keep(inner) 仍被持有：
     于是「低优先级」线程在整个等待期仍占着 inner，而高优先级线程要 inner ⇒ 反转 + 潜在死锁 */
  cv.wait_for(io, std::chrono::milliseconds(200), []{ return ready; });
  stage.store(2, std::memory_order_release);
}
static void urgent(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等 inner */
  std::lock_guard<std::mutex> k(inner);
  std::printf("E166 urgent got inner\n");
  ready = true;
  cv.notify_all();
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(holder), b(urgent);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：cv.wait 只释放外层锁，内层锁仍被占",
  "预期 miss。")

# ---------------------------------------------------------------- E167
S("E167", "lock_priority_inversion", "high", "catch", ["tsan"], 2, 5, "unlocked_fast",
  "持锁线程做长操作，快路径线程无锁读写同一缓冲区",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex tx_lock;
static char txbuf[512];
static std::atomic<int> stage{0};
static void bulk_tx(){
  std::lock_guard<std::mutex> lk(tx_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做大批量「发送」填充，锁占用时间长 */
  for (int k = 0; k < 20000; ++k)
    for (int i = 0; i < 512; ++i) txbuf[i] = (char)('a' + ((k + i) % 26));
  stage.store(2, std::memory_order_release);
}
static void fast_ack(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 快路径（高优先级）直接写同一发送缓冲区，不取锁 ⇒ 与持锁线程真实数据竞争 */
  for (int k = 0; k < 20000; ++k) txbuf[k % 512] = 'Z';
  while (stage.load(std::memory_order_acquire) < 2){}
}
int main(){
  std::thread a(bulk_tx), b(fast_ack);
  a.join(); b.join();
  std::printf("E167 tx0=%c\n", tx0());
  return 0;
}
'''.replace("tx0()", "txbuf[0]"),
  "2 线程：持锁批量填充 vs 无锁快路径写",
  "含真实数据竞争 → 预期 TSan catch。")

# ---------------------------------------------------------------- E168
S("E168", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "page_fault",
  "持锁访问尚未映射的内存（sleep 模拟缺页/换入）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static int page[4096];
static std::atomic<int> stage{0};
static void touch_pages(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁逐页「换入」：真实系统里这是不可中断的缺页处理，
     持锁页错误会让锁被占用毫秒级 ⇒ 实时线程必然错过截止期 */
  for (int p = 0; p < 4096; p += 64){
    page[p] = p;
    if (p % 512 == 0) std::this_thread::sleep_for(std::chrono::microseconds(200));
  }
  stage.store(2, std::memory_order_release);
}
static void rt_read(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 实时读线程等锁 */
  std::lock_guard<std::mutex> lk(m);
  int s = 0;
  for (int p = 0; p < 4096; p += 512) s += page[p];
  std::printf("E168 s=%d\n", s);
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(touch_pages), b(rt_read);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：持锁页换入 vs 实时读",
  "预期 miss。")

# ---------------------------------------------------------------- E169
S("E169", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "alloc_storm",
  "持锁触发大量内存分配（分配器内部锁 + 缺页）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <vector>
#include <cstdio>
static std::mutex alloc_lock;
static std::vector<int*> pool;
static std::atomic<int> stage{0};
static void churn(){
  std::lock_guard<std::mutex> lk(alloc_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做分配/释放风暴：分配器内部还有自己的锁，
     一旦与别的线程的分配路径形成锁序反转，反转会级联放大 */
  for (int i = 0; i < 5000; ++i){
    int* p = new int[256];
    p[0] = i;
    pool.push_back(p);
  }
  stage.store(2, std::memory_order_release);
}
static void reporter(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级统计线程等锁 */
  std::lock_guard<std::mutex> lk(alloc_lock);
  std::printf("E169 pool=%zu\n", pool.size());
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(churn), b(reporter);
  a.join(); b.join();
  for (int* p : pool) delete[] p;
  return 0;
}
''',
  "2 线程：持锁分配风暴",
  "预期 miss。")

# ---------------------------------------------------------------- E170
S("E170", "lock_priority_inversion", "high", "miss", ["tsan"], 2, 5, "crypto",
  "持锁做加密/签名运算（CPU 密集 + 可能换出）",
  r'''
#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex key_lock;
static unsigned char key[32] = {0};
static std::atomic<int> stage{0};
static void sign(){
  std::lock_guard<std::mutex> lk(key_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做多轮签名运算（CPU 密集，真实实现里还可能触发换页） */
  for (int round = 0; round < 5000; ++round)
    for (int i = 0; i < 32; ++i) key[i] = (unsigned char)((key[i] * 31 + round) & 0xFF);
  stage.store(2, std::memory_order_release);
}
static void handshake(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 握手线程（高优先级）必须等锁才能读密钥 */
  std::lock_guard<std::mutex> lk(key_lock);
  std::printf("E170 key0=%d\n", key[0]);
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(sign), b(handshake);
  a.join(); b.join();
  return 0;
}
''',
  "2 线程：持锁做签名运算",
  "预期 miss。")
