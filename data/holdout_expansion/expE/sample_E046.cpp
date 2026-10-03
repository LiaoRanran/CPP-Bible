// sample_E046
// defect_type: atomic_ub
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E046.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> version{0};
static int observed = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void bump(int want){
  wait_go();
  int expected = 0;
  /*DEFECT: 循环里用 strong 版：语义上没错，但 strong 不会伪失败，循环退化成「重试阻塞」，在高竞争下造成活锁式的忙等*/
  while (version.compare_exchange_strong(expected, want, std::memory_order_acq_rel))
    expected = 0;
  observed = want;
}
int main(){
  std::thread a(bump, 1), b(bump, 2);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E046 version=%d observed=%d\n", version.load(), observed);
  return 0;
}
