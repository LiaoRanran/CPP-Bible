// sample_E064
// defect_type: atomic_ub
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E064.json)

#include <atomic>
#include <thread>
#include <cstdio>
enum St { IDLE = 0, RUNNING = 1, DONE = 2 };
static std::atomic<int> st{IDLE};
static int transitions = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void advance(){
  wait_go();
  /*DEFECT: 用 exchange 无条件覆盖状态（不做前置状态校验），与另一个线程的 CAS 转换互相踩踏：状态机可从 DONE 退回 RUNNING */
  int prev = st.exchange(RUNNING, std::memory_order_acq_rel);
  if (prev == IDLE) transitions++;
  int exp = RUNNING;
  st.compare_exchange_strong(exp, DONE, std::memory_order_acq_rel);
  transitions++;
}
int main(){
  std::thread a(advance), b(advance);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E064 st=%d transitions=%d\n", st.load(), transitions);
  return 0;
}
