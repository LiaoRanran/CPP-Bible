// sample_E137
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E137.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> value{0};
static std::atomic<long> version{0};
static std::atomic<int> step{0}, commits{0};
int main(){
  value.store(7, std::memory_order_release);
  version.store(1, std::memory_order_release);
  std::thread a([&]{
    int v = value.load(std::memory_order_acquire);
    long ver = version.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 「值未变 + 版本未变」的两段式校验不是原子的：写者可以先把值改回、
       再把版本号写回（甚至还没写），使这里的乐观校验通过而实际基线已失效 */
    if (value.load(std::memory_order_acquire) == v && version.load(std::memory_order_acquire) == ver){
      commits.fetch_add(1, std::memory_order_relaxed);
      version.store(ver + 1, std::memory_order_release);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  value.store(9, std::memory_order_release);
  value.store(7, std::memory_order_release);       // 值回到原值
  version.store(1, std::memory_order_release);     // 版本号「看起来」没变
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E137 commits=%d value=%d version=%ld\n", commits.load(), value.load(), version.load());
  return 0;
}
