// sample_E123
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E123.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> refs{0};
static std::atomic<int> step{0};
static int payload = 0;
int main(){
  refs.store(1, std::memory_order_release);
  std::thread a([&]{
    (void)refs.load(std::memory_order_acquire);   // 快照读了却没参与校验（见 DEFECT）
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 「若计数为 0 则由我置 1」的 test-and-set 缺版本保护：计数 0->1->0 之后，
       这里的 CAS 误判仍为 0 而成功，与另一线程同时认为自己独占 payload */
    int exp = 0;
    if (refs.compare_exchange_strong(exp, 1, std::memory_order_acq_rel, std::memory_order_acquire))
      payload = 42;
  });
  while (step.load(std::memory_order_acquire) != 1){}
  refs.store(1, std::memory_order_release);
  refs.store(0, std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E123 refs=%d payload=%d\n", refs.load(), payload);
  return 0;
}
