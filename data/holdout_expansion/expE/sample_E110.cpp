// sample_E110
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan,asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E110.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::recursive_mutex m;
static std::condition_variable_any cv;   // 只能配 std::mutex 的 cv 被换成 any 后，配了 recursive_mutex
static bool flag = false;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void waiter(){
  wait_go();
  std::unique_lock<std::recursive_mutex> lk(m);
  lk.lock();                    // 递归加锁，计数 = 2
  /*DEFECT: 条件变量要求配 std::mutex。配 recursive_mutex 时 wait() 只解锁一层，
     m 仍被本线程持有（计数 1）⇒ 谓词永远不会被 notifier 满足 ⇒ 死锁 */
  cv.wait(lk, []{ return flag; });
  std::printf("E110 waiter done\n");
}
static void notifier(){
  wait_go();
  /*DEFECT: notifier 需要完整地拿到 m（计数降到 0），而 A 还留着 1 层 ⇒ 永久阻塞 */
  std::lock_guard<std::recursive_mutex> g(m);
  flag = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(notifier);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
