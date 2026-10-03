// sample_E047
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E047.json)

#include <atomic>
#include <cstdio>
int main(){
  std::atomic<int> a{5};
  int expected = 5;
  /*DEFECT: 成功序是 memory_order_relaxed，失败序却给了 memory_order_acq_rel：
     标准要求失败序不得强于成功序，此处违反 compare_exchange 的前置条件 → UB */
  bool ok = a.compare_exchange_strong(expected, 9,
                                     std::memory_order_relaxed,
                                     std::memory_order_acq_rel);
  std::printf("E047 ok=%d a=%d\n", (int)ok, a.load());
  return 0;
}
