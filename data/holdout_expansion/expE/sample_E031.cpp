// sample_E031
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E031.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> f1{0}, f2{0}, f3{0};
static std::atomic<bool> all_ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  f1.store(10, std::memory_order_relaxed);
  f2.store(20, std::memory_order_relaxed);
  f3.store(30, std::memory_order_relaxed);
  all_ready.store(true, std::memory_order_release);
}
static void consumer(){
  wait_go();
  while(!all_ready.load(std::memory_order_acquire)){}
  /*DEFECT: f1/f2/f3 是 relaxed 存储，读侧也 relaxed 读：acquire 只约束 all_ready 一个原子，三个字段无同步保护*/
  std::printf("E031 f1=%d f2=%d f3=%d\n",
              f1.load(std::memory_order_relaxed),
              f2.load(std::memory_order_relaxed),
              f3.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
