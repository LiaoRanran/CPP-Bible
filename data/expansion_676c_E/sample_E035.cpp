// sample_E035
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E035.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int cells[8] = {0, 0, 0, 0, 0, 0, 0, 0};
static std::atomic<int> w_cursor{0}, r_cursor{0}, go{0};
static void wait_go(){ while(go.load(std::memory_order_acquire) == 0){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 8; ++i){
    cells[i] = i + 500;                                   // 非原子写
    /*DEFECT: w_cursor 用 relaxed 递增：发布下标不携带 release，读者据其读 cells 无同步*/
    w_cursor.store(i + 1, std::memory_order_relaxed);
  }
}
static void consumer(){
  wait_go();
  /*DEFECT: relaxed 读 w_cursor 作完成判据，随后读非原子 cells → 数据竞争*/
  while (w_cursor.load(std::memory_order_relaxed) < 8){}
  std::printf("E035 c7=%d\n", cells[7]);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(1, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
