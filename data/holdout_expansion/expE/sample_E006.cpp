// sample_E006
// defect_type: memory_order
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E006.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> state{0};
static std::atomic<bool> changed{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void setter(){
  wait_go();
  state.store(5, std::memory_order_relaxed);
  changed.store(true, std::memory_order_release);
}
static void watcher(){
  wait_go();
  /*DEFECT: changed 用 relaxed 加载：与 release 存储不配对，state 的写入无同步保证*/
  if (changed.load(std::memory_order_relaxed))
    std::printf("E006 state=%d\n", state.load(std::memory_order_relaxed));
}
int main(){
  std::thread a(setter), b(watcher);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
