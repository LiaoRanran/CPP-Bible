// sample_E050
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E050.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<short> gain{1000};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void scale(){
  wait_go();
  /*DEFECT: 对 atomic<short> 连续 fetch_add 越过 SHRT_MAX：有符号原子算术溢出在 C++17 是 UB*/
  for (int i = 0; i < 200; ++i) gain.fetch_add(300, std::memory_order_relaxed);
}
int main(){
  std::thread a(scale), b(scale);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E050 gain=%d\n", (int)gain.load());
  return 0;
}
