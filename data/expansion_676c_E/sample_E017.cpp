// sample_E017
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E017.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int ring[8];
static std::atomic<int> head{0}, tail{0}, go{0};
static void wait_go(){ while(go.load(std::memory_order_acquire) == 0){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 8; ++i){
    ring[i] = i * 3;
    /*DEFECT: tail 用 relaxed 递增：waiter 以 relaxed 读 tail 作判据，SPSC 无 happens-before，读侧可读到未初始化的 ring*/
    tail.store(tail.load(std::memory_order_relaxed) + 1, std::memory_order_relaxed);
  }
}
static void waiter(){
  wait_go();
  /*DEFECT: 同样 relaxed 读 tail：判据本身不建立同步，后续读 ring 是数据竞争*/
  while (tail.load(std::memory_order_relaxed) < 8){}
  std::printf("E017 ring7=%d\n", ring[7]);
}
int main(){
  std::thread p(producer), w(waiter);
  go.store(1, std::memory_order_release);
  p.join(); w.join();
  return 0;
}
