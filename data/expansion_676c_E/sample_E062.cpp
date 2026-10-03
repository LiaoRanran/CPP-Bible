// sample_E062
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E062.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Score { std::atomic<int> hi; int lo; };
static Score s{0, 0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void bump2(){
  wait_go();
  /*DEFECT: 复合更新里 hi 用 fetch_add（原子）而 lo 直接赋值（非原子）且读改写未同步：状态可能被撕裂成 hi/lo 不一致 */
  s.hi.fetch_add(1, std::memory_order_relaxed);
  s.lo = s.lo + 1;
}
int main(){
  std::thread a(bump2), b(bump2), c(bump2);
  go.store(true, std::memory_order_release);
  a.join(); b.join(); c.join();
  std::printf("E062 hi=%d lo=%d\n", s.hi.load(), s.lo);
  return 0;
}
