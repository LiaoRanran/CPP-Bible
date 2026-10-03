// sample_E049
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E049.json)

#include <atomic>
#include <cstdio>
int main(){
  std::atomic<long long> budget{10};
  /*DEFECT: fetch_sub 减到负数：对有符号原子做下溢是 UB（C++17），且负值随后被当作合法预算使用*/
  for (int i = 0; i < 25; ++i) budget.fetch_sub(1, std::memory_order_relaxed);
  std::printf("E049 budget=%lld\n", budget.load());
  return 0;
}
