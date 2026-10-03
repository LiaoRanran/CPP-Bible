// sample_E098
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E098.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex tbl;
static std::atomic<int> visited{0};
static void on_row(){
  /*DEFECT: 在持有 tbl 的遍历过程中进入回调，回调里对同一张表加锁 ⇒ 自死锁 */
  std::lock_guard<std::mutex> g(tbl);
  visited.fetch_add(1, std::memory_order_release);
}
static void scan(){
  std::lock_guard<std::mutex> g(tbl);
  on_row();
}
int main(){
  std::thread a(scan), b(scan);
  a.join(); b.join();
  std::printf("E098 visited=%d\n", visited.load());
  return 0;
}
