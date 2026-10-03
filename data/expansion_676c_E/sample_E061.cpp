// sample_E061
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E061.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> n{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void inc(){
  wait_go();
  for (int i = 0; i < 1000; ++i){
    /*DEFECT: x = x.load() + 1 不是原子的读-改-写：两次操作之间可被插入，计数必然丢失更新（应用 fetch_add）*/
    int v = n.load(std::memory_order_relaxed);
    n.store(v + 1, std::memory_order_relaxed);
  }
}
int main(){
  std::thread a(inc), b(inc);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E061 n=%d\n", n.load());
  return 0;
}
