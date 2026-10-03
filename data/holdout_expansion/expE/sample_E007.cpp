// sample_E007
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E007.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> payload{0};
static std::atomic<bool> stage1{false}, stage2{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  payload.store(11, std::memory_order_relaxed);
  stage1.store(true, std::memory_order_release);
  payload.store(22, std::memory_order_relaxed);
  /*DEFECT: 第二段发布用 relaxed：consumer 若只 acquire stage2，拿不到 payload==22 的可见性*/
  stage2.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!stage2.load(std::memory_order_acquire)){}
  std::printf("E007 payload=%d\n", payload.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
