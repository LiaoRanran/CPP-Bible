// sample_E166
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E166.json)

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
