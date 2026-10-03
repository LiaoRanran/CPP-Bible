// sample_E023
// defect_type: memory_order
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E023.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<unsigned> stage_bits{0};
static std::atomic<int> slots[4];
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void worker(int id){
  wait_go();
  slots[id].store(id * 10, std::memory_order_relaxed);
  /*DEFECT: 位标志用 relaxed fetch_or：waiter 若也 relaxed 读，两侧都不建立 happens-before*/
  stage_bits.fetch_or(1u << id, std::memory_order_relaxed);
}
static void waiter(){
  wait_go();
  /*DEFECT: relaxed 读位标志当完成判据：读到 0xF 不保证 slots 的写入已可见*/
  while (stage_bits.load(std::memory_order_relaxed) != 0xFu){}
  std::printf("E023 s3=%d\n", slots[3].load(std::memory_order_relaxed));
}
int main(){
  std::thread a(worker, 0), b(worker, 1), c(worker, 2), d(worker, 3), w(waiter);
  go.store(true, std::memory_order_release);
  a.join(); b.join(); c.join(); d.join(); w.join();
  return 0;
}
