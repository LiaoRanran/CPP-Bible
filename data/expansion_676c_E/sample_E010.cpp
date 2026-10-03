// sample_E010
// defect_type: memory_order
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E010.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> cfg{0};
static std::atomic<bool> inited{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void init_once(){
  wait_go();
  cfg.store(77, std::memory_order_relaxed);
  inited.store(true, std::memory_order_seq_cst);
}
static void watcher(){
  wait_go();
  /*DEFECT: inited 用 relaxed 加载，无法消费上面 seq_cst 存储的 release 语义*/
  if (inited.load(std::memory_order_relaxed))
    std::printf("E010 cfg=%d\n", cfg.load(std::memory_order_relaxed));
}
int main(){
  std::thread a(init_once), b(watcher);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
