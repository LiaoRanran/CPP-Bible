// sample_E048
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E048.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> counter{2147483000};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void bump(){
  wait_go();
  /*DEFECT: 对有符号 atomic<int> 连续 fetch_add 越过 INT_MAX：C++17 规定原子算术溢出为 UB（C++20 才定义为回绕）*/
  for (int i = 0; i < 1000; ++i) counter.fetch_add(100000, std::memory_order_relaxed);
}
int main(){
  std::thread a(bump), b(bump);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E048 counter=%d\n", counter.load());
  return 0;
}
