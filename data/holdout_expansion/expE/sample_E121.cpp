// sample_E121
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E121.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> a{1}, b{10};
static std::atomic<int> step{0}, ops{0};
int main(){
  std::thread t([&]{
    int ea = a.load(std::memory_order_acquire);
    int eb = b.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 两次 CAS 之间读了 b 的旧值：a/b 都被别人改过又改回（1->2->1、10->20->10），
       校验通过但依据的前提（b 未变）已不成立 ⇒ 丢失更新 */
    if (a.compare_exchange_strong(ea, 3, std::memory_order_acq_rel, std::memory_order_acquire)){
      int cur = b.load(std::memory_order_relaxed);
      b.store(eb + cur, std::memory_order_relaxed);
      ops.fetch_add(1, std::memory_order_relaxed);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  a.store(2, std::memory_order_release); a.store(1, std::memory_order_release);
  b.store(20, std::memory_order_release); b.store(10, std::memory_order_release);
  step.store(2, std::memory_order_release);
  t.join();
  std::printf("E121 a=%d b=%d ops=%d\n", a.load(), b.load(), ops.load());
  return 0;
}
