// sample_E022
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E022.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Registry { int slots[8]; int live; };
static std::atomic<Registry*> reg{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static Registry* get(){
  Registry* r = reg.load(std::memory_order_acquire);
  if (r == nullptr){
    r = new Registry{};
    for (int i = 0; i < 8; ++i) r->slots[i] = i;   // 非原子字段写
    r->live = 8;
    /*DEFECT: 二次检查用 relaxed；构造函数里的 slots/live 写与读线程之间无 synchronizes-with*/
    if (reg.load(std::memory_order_relaxed) == nullptr) reg.store(r, std::memory_order_release);
    else { delete r; r = reg.load(std::memory_order_relaxed); }
  }
  return r;
}
static void worker(){ wait_go(); Registry* r = get(); std::printf("E022 live=%d\n", r->live); }
int main(){
  std::thread a(worker), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
