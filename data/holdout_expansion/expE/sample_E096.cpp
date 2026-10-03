// sample_E096
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E096.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::atomic<int> inside{0};
static void notify_cb(){
  /*DEFECT: 通知回调在调用方仍持有 m 时执行，回调里再 lock(m) ⇒ 自死锁 */
  std::lock_guard<std::mutex> g(m);
  inside.fetch_add(1, std::memory_order_release);
}
static void holder(){
  std::lock_guard<std::mutex> g(m);
  notify_cb();
}
int main(){
  std::thread a(holder), b(holder);
  a.join(); b.join();
  std::printf("E096 inside=%d\n", inside.load());
  return 0;
}
