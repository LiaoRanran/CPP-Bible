// sample_E099
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E099.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex la, lb;
static std::condition_variable cva, cvb;
static bool left_done = false, right_done = false;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void left(){
  wait_go();
  std::unique_lock<std::mutex> l(la);
  /*DEFECT: 持 la 等 right_done，而 right_done 只能由右线程在拿到 lb 后设置；右线程正持 lb 等 left_done ⇒ 互等死锁 */
  cva.wait(l, []{ return right_done; });
  left_done = true;
  cvb.notify_all();
}
static void right(){
  wait_go();
  std::unique_lock<std::mutex> l(lb);
  /*DEFECT: 持 lb 等 left_done，构成对称的循环等待 */
  cvb.wait(l, []{ return left_done; });
  right_done = true;
  cva.notify_all();
}
int main(){
  std::thread a(left), b(right);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
