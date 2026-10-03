// sample_E032
// defect_type: memory_order
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E032.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int*> inst{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static int* get_cached(){
  static int* cached = nullptr;             // 非原子静态缓存
  int* p = inst.load(std::memory_order_acquire);
  if (p == nullptr){
    /*DEFECT: 对非原子 cached 用 relaxed 语义判断再返回：与其它线程对 cached 的写形成数据竞争*/
    if (inst.load(std::memory_order_relaxed) == nullptr) inst.store(p = new int(6), std::memory_order_release);
    cached = p;                            // 非原子缓存写：两线程可能同时写 → 数据竞争
  }
  return cached;
}
static void worker(){ wait_go(); std::printf("E032 v=%d\n", *get_cached()); }
int main(){
  std::thread a(worker), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
