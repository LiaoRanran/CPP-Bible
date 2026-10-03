// sample_E097
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E097.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex reg;
static std::atomic<int> fired{0};
static void user_hook(){
  /*DEFECT: 用户钩子在 reg 被持有期间执行，钩子内部再次 lock(reg) ⇒ 自死锁 */
  std::lock_guard<std::mutex> g(reg);
  fired.fetch_add(1, std::memory_order_release);
}
static void run_hooks(){
  std::lock_guard<std::mutex> g(reg);
  user_hook();
}
int main(){
  std::thread a(run_hooks), b(run_hooks);
  a.join(); b.join();
  std::printf("E097 fired=%d\n", fired.load());
  return 0;
}
