// sample_E108
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E108.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::atomic<bool> may_fail{true};
static void leaky(){
  m.lock();
  /*DEFECT: 手动 lock() 后这条分支直接 return（没有 unlock / 没有 RAII）：m 被永久泄漏 */
  if (may_fail.load(std::memory_order_acquire)) return;
  m.unlock();
  std::printf("E108 done\n");
}
int main(){
  std::thread a(leaky);
  a.join();
  /*DEFECT: m 仍是锁死状态，后续任何 lock(m) 都会永久阻塞 */
  std::thread b([]{ std::lock_guard<std::mutex> g(m); std::printf("E108 second\n"); });
  b.join();
  return 0;
}
