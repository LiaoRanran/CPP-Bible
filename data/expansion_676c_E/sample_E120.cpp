// sample_E120
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E120.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> cell{0};
static std::atomic<int> step{0}, applied{0};
int main(){
  cell.store(1, std::memory_order_release);
  std::thread a([&]{
    int exp = cell.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 只比较值不看版本：cell 经历 1->0->1 后，这次 CAS 会误判「没人改过」而成功，
       基于「未被别人改过」的假设（如下方计数）就失效了 */
    if (cell.compare_exchange_strong(exp, 9, std::memory_order_acq_rel, std::memory_order_acquire))
      applied.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  cell.store(0, std::memory_order_release);
  cell.store(1, std::memory_order_release);      // 回到原值
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E120 applied=%d cell=%d\n", applied.load(), cell.load());
  return 0;
}
