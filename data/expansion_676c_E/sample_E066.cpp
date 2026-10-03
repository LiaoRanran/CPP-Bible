// sample_E066
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E066.json)

#include <atomic>
#include <cstdio>
int main(){
  std::atomic<signed char> tiny{100};
  /*DEFECT: atomic<signed char> 连续 fetch_add 越过 127：有符号原子算术溢出在 C++17 是 UB */
  for (int i = 0; i < 100; ++i) tiny.fetch_add(1, std::memory_order_relaxed);
  std::printf("E066 tiny=%d\n", (int)tiny.load());
  return 0;
}
