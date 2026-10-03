// sample_E162
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E162.json)

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
