// sample_E024
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E024.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<long> big{0};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void writer(){
  wait_go();
  big.store(123456789L, std::memory_order_relaxed);
  /*DEFECT: ready 用 relaxed 存储：读侧即使 acquire 也无 release 可配对*/
  ready.store(true, std::memory_order_relaxed);
}
static void reader(){
  wait_go();
  while(!ready.load(std::memory_order_acquire)){}
  std::printf("E024 big=%ld\n", big.load(std::memory_order_relaxed));
}
int main(){
  std::thread w(writer), r(reader);
  go.store(true, std::memory_order_release);
  w.join(); r.join();
  return 0;
}
