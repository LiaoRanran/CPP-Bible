// sample_E157
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E157.json)

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
