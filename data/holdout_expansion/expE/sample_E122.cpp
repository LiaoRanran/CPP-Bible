// sample_E122
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E122.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> lo{0}, hi{10};
static std::atomic<int> step{0}, bad{0};
int main(){
  std::thread t([&]{
    int l = lo.load(std::memory_order_acquire);
    int h = hi.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 依赖「读到的 lo/hi 是同一时刻的快照」这一假设，但两次 load 之间 lo/hi
       可被改成非法组合又改回（lo:0->5->0, hi:10->2->10）⇒ 不变式 lo<=hi 的校验形同虚设 */
    if (lo.compare_exchange_strong(l, 9, std::memory_order_acq_rel, std::memory_order_acquire)){
      if (h < l) bad.fetch_add(1, std::memory_order_relaxed);
      int hh = hi.load(std::memory_order_relaxed);
      hi.store(hh - 20, std::memory_order_relaxed);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  lo.store(5, std::memory_order_release); lo.store(0, std::memory_order_release);
  hi.store(2, std::memory_order_release); hi.store(10, std::memory_order_release);
  step.store(2, std::memory_order_release);
  t.join();
  std::printf("E122 bad=%d lo=%d hi=%d\n", bad.load(), lo.load(), hi.load());
  return 0;
}
