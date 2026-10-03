// sample_E009
// defect_type: memory_order
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E009.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> reg{0};
static std::atomic<bool> flag{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void setter(){
  wait_go();
  reg.store(9, std::memory_order_relaxed);
  /*DEFECT: 用 acquire 做「发布」，acquire 不产生 release 语义：读侧 acquire 配不上*/
  flag.store(true, std::memory_order_acquire);
}
static void watcher(){
  wait_go();
  /*DEFECT: 用 relaxed 读，恰好与上面的 acquire 存储「错向配对」，两边都不建立 synchronizes-with*/
  if (flag.load(std::memory_order_relaxed))
    std::printf("E009 reg=%d\n", reg.load(std::memory_order_relaxed));
}
int main(){
  std::thread a(setter), b(watcher);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
