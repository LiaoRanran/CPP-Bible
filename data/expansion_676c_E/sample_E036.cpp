// sample_E036
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E036.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int log_[6];
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer_a(){
  wait_go();
  log_[0] = 1; log_[1] = 2;
  /*DEFECT: 生产者 B 用 relaxed 发布同一个 ready；A 用 release：两个生产者强度不一致，读侧无法统一获得可见性*/
  ready.store(true, std::memory_order_release);
}
static void producer_b(){
  wait_go();
  log_[2] = 3; log_[3] = 4;
  ready.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!ready.load(std::memory_order_acquire)){}
  /*DEFECT: 只 acquire 到 B 的 relaxed 写（无 release），却读全部 log_ → 与 A/B 的非原子写竞争*/
  std::printf("E036 l0=%d l3=%d\n", log_[0], log_[3]);
}
int main(){
  std::thread a(producer_a), b(producer_b), c(consumer);
  go.store(true, std::memory_order_release);
  a.join(); b.join(); c.join();
  return 0;
}
