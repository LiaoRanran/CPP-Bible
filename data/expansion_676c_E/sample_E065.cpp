// sample_E065
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 6
// timeout_seconds: 5
// (authoritative annotation in sample_E065.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int cells[4] = {1, 2, 3, 4};
static std::atomic<unsigned> idx{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void indexer(){
  wait_go();
  /*DEFECT: 无符号 fetch_sub 在 0 处回绕成巨大值，直接当下标 → 数组越界访问（UB）*/
  unsigned i = idx.fetch_sub(1, std::memory_order_relaxed);
  std::printf("E065 cells=%d\n", cells[i]);
}
int main(){
  idx.store(2, std::memory_order_relaxed);
  std::thread a(indexer), b(indexer), c(indexer), d(indexer), e(indexer), f(indexer);
  go.store(true, std::memory_order_release);
  a.join(); b.join(); c.join(); d.join(); e.join(); f.join();
  return 0;
}
