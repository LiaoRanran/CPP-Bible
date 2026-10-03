// sample_E142
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E142.json)

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
