// sample_E086
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E086.json)

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
