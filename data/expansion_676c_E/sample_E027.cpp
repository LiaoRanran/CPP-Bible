// sample_E027
// defect_type: memory_order
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E027.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int*> slot{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static int* get(){
  int* p = slot.load(std::memory_order_acquire);
  if (!p){
    p = new int(5);
    /*DEFECT: 二次检查用 relaxed 后直接返回新指针：读线程可能拿到未与 release 配对的指针值*/
    if (slot.load(std::memory_order_relaxed) != nullptr){ delete p; p = slot.load(std::memory_order_relaxed); }
    else slot.store(p, std::memory_order_release);
  }
  return p;
}
static void worker(){ wait_go(); std::printf("E027 v=%d\n", *get()); }
int main(){
  std::thread a(worker), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
