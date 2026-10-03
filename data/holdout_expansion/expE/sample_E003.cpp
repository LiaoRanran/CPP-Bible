// sample_E003
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E003.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Config { int a; int b; };
static std::atomic<Config*> inst{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static Config* get_instance(){
  Config* p = inst.load(std::memory_order_acquire);
  if (p == nullptr){
    p = new Config{1, 2};
    /*DEFECT: 二次检查用 relaxed，未与下方 release 存储配对：可能读到未完全发布的指针*/
    if (inst.load(std::memory_order_relaxed) == nullptr)
      inst.store(p, std::memory_order_release);
    else { delete p; p = inst.load(std::memory_order_relaxed); }
  }
  return p;
}
int main(){
  std::thread t1([]{ wait_go(); Config* c = get_instance(); std::printf("E003 a=%d\n", c->a); });
  std::thread t2([]{ wait_go(); Config* c = get_instance(); std::printf("E003 a=%d\n", c->a); });
  go.store(true, std::memory_order_release);
  t1.join(); t2.join();
  return 0;
}
