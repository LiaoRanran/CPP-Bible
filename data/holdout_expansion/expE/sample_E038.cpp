// sample_E038
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E038.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Pool { int* buf; int n; };
static std::atomic<Pool*> pool{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static Pool* get(){
  Pool* p = pool.load(std::memory_order_acquire);
  if (!p){
    p = new Pool{new int[4]{1, 2, 3, 4}, 4};
    /*DEFECT: 二次检查用 relaxed：两线程可同时判定为空，其中一条 delete 后另一条仍持有已释放指针（读侧无 acquire 保护）*/
    if (pool.load(std::memory_order_relaxed) == nullptr) pool.store(p, std::memory_order_release);
    else { delete p->buf; delete p; p = pool.load(std::memory_order_relaxed); }
  }
  /*DEFECT: 返回前用 relaxed 再读一次 pool：可能拿到刚被竞争分支 delete 掉的指针*/
  Pool* q = pool.load(std::memory_order_relaxed);
  return q ? q : p;
}
static void worker(){ wait_go(); Pool* p = get(); std::printf("E038 n=%d buf3=%d\n", p->n, p->buf[3]); }
int main(){
  std::thread a(worker), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
