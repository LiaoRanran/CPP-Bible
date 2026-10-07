// sample_E049
// [redacted]
// severity: high
// [redacted]
// expected_verdict: miss
// [redacted]
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E049.json)

#include <atomic>
#include <cstdio>
int main(){
  std::atomic<long long> budget{10};
  /* [redacted]*/
  for (int i = 0; i < 25; ++i) budget.fetch_sub(1, std::memory_order_relaxed);
  std::printf("E049 budget=%lld\n", budget.load());
  return 0;
}
