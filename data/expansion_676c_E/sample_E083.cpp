// sample_E083
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E083.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::atomic<int> entered{0};
static void on_event(){
  /*DEFECT: 回调在调用方已持有 m 的栈帧上再次 lock(m)：非递归锁 ⇒ 立即自死锁 */
  std::lock_guard<std::mutex> g(m);
  std::printf("E083 callback done\n");
}
static void enter(){
  std::lock_guard<std::mutex> g(m);
  entered.fetch_add(1, std::memory_order_release);
  on_event();
}
int main(){
  std::thread a(enter), b(enter);
  a.join(); b.join();
  std::printf("E083 entered=%d\n", entered.load());
  return 0;
}
