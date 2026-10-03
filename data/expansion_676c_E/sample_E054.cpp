// sample_E054
// defect_type: atomic_ub
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E054.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<bool> busy{false};
static int critical_writes = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void enter(){
  wait_go();
  /*DEFECT: exchange 返回 true 说明锁已被别人占用，这里直接无视返回值继续写「临界区」→ 互斥失效*/
  busy.exchange(true, std::memory_order_acq_rel);
  critical_writes = critical_writes + 1;
  busy.store(false, std::memory_order_release);
}
int main(){
  std::thread a(enter), b(enter);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E054 writes=%d\n", critical_writes);
  return 0;
}
