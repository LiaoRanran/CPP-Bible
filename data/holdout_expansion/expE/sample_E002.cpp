// sample_E002
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E002.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<double> load_v{0.0};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  load_v.store(3.5, std::memory_order_relaxed);
  ready.store(true, std::memory_order_release);
}
static void consumer(){
  wait_go();
  /*DEFECT: ready 用 relaxed 轮询，double 载荷也用 relaxed 读：两处都无 acquire 语义*/
  while(!ready.load(std::memory_order_relaxed)){}
  std::printf("E002 load=%f\n", load_v.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
