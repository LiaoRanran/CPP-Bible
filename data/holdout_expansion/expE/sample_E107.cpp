// sample_E107
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E107.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex a, b;
static std::atomic<bool> holding_a{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void path_atomic(){
  wait_go();
  /*DEFECT: 路径甲「a->b」 */
  std::lock_guard<std::mutex> la(a);
  holding_a.store(true, std::memory_order_release);
  while(!holding_a.load(std::memory_order_acquire)){}
  std::lock_guard<std::mutex> lb(b);
  std::printf("E107 path a\n");
}
static void path_bfirst(){
  wait_go();
  while(!holding_a.load(std::memory_order_acquire)){}
  /*DEFECT: 路径乙「b->a」，与甲相反 ⇒ 死锁（注意 std::lock 与手写顺序混用加剧了不一致） */
  std::lock_guard<std::mutex> lb(b);
  std::lock_guard<std::mutex> la(a);
  std::printf("E107 path b\n");
}
int main(){
  std::thread x(path_atomic), y(path_bfirst);
  go.store(true, std::memory_order_release);
  x.join(); y.join();
  return 0;
}
