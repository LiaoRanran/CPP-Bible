// sample_E143
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E143.json)

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
