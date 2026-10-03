// sample_E109
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E109.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
#include <stdexcept>
static std::mutex outer, inner;
static std::atomic<bool> caught{false};
static void thrower(){
  outer.lock();                        // 手动 lock：没有 RAII 兜底
  std::unique_lock<std::mutex> i(inner);
  /*DEFECT: 抛异常时栈展开只会释放 inner（RAII），手动 lock 的 outer 永久泄漏：
     锁的「异常路径安全性」被破坏，且这种泄漏在栈展开里完全静默 */
  throw std::runtime_error("boom");
}
static void waiter(){
  while(!caught.load(std::memory_order_acquire)){}
  /*DEFECT: 需要 outer，而 outer 已被异常路径永久泄漏 ⇒ 永久阻塞 */
  std::lock_guard<std::mutex> o(outer);
  std::lock_guard<std::mutex> i(inner);
  std::printf("E109 ok\n");
}
int main(){
  std::thread a([&]{
    try { thrower(); }
    catch (const std::exception&){ caught.store(true, std::memory_order_release); }
  });
  std::thread b(waiter);
  a.join(); b.join();
  return 0;
}
