// sample_E008
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E008.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> produced{0};
static int table[4] = {0, 0, 0, 0};        // 非原子载荷
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 4; ++i){
    table[i] = i + 100;                   // 非原子写
    /*DEFECT: relaxed 计数递增：waiter 以 relaxed 读该计数作判据，两者之间无 synchronizes-with*/
    produced.fetch_add(1, std::memory_order_relaxed);
  }
}
static void waiter(){
  wait_go();
  /*DEFECT: relaxed 读计数并当作「table 已完全可见」的依据：非原子数组的写可能尚未对读线程可见*/
  while (produced.load(std::memory_order_relaxed) < 4){}
  std::printf("E008 table3=%d\n", table[3]);
}
int main(){
  std::thread p(producer), w(waiter);
  go.store(true, std::memory_order_release);
  p.join(); w.join();
  return 0;
}
