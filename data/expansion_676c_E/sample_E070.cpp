// sample_E070
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E070.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> cell{0};
static int peeled = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void peel(){
  wait_go();
  for (int round = 0; round < 4; ++round){
    /*DEFECT: 循环里 expected 永远是常量 0：cell 被别人改成 1 后再也 CAS 不回来，逻辑上丢失了 peel 机会 */
    int expected = 0;
    if (cell.compare_exchange_weak(expected, 2, std::memory_order_acq_rel)) peeled++;
  }
  std::printf("E070 peeled=%d\n", peeled);
}
int main(){
  std::thread a(peel), b(peel);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E070 cell=%d\n", cell.load());
  return 0;
}
