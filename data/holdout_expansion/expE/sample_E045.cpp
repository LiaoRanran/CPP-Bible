// sample_E045
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E045.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> slot{0};
static int taken = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void try_acquire(){
  wait_go();
  int expected = 0;
  /*DEFECT: compare_exchange_weak 允许伪失败，此处不在循环里重试：一次伪失败就丢掉了资源*/
  if (slot.compare_exchange_weak(expected, 1, std::memory_order_acq_rel))
    taken = 1;
  else
    std::printf("E045 gave up (expected=%d)\n", expected);
}
int main(){
  std::thread a(try_acquire), b(try_acquire);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E045 taken=%d\n", taken);
  return 0;
}
