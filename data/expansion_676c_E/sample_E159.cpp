// sample_E159
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E159.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex dma_lock;
static int dma_state = 0;
static std::atomic<int> stage{0};
static void cpu_worker(){
  std::lock_guard<std::mutex> lk(dma_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做用户态内存整理（页迁移/规整），持续时间长 */
  for (int k = 0; k < 3000; ++k){
    static int scratch[4096];
    for (int i = 0; i < 4096; ++i) scratch[i] = (scratch[i] + k) & 0xFFFF;
    if (scratch[0] == -1) break;
  }
  stage.store(2, std::memory_order_release);
}
static void dma_done(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: DMA 完成中断回调（最高优先级）等这把锁 */
  std::lock_guard<std::mutex> lk(dma_lock);
  dma_state = 1;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(cpu_worker), b(dma_done);
  a.join(); b.join();
  std::printf("E159 dma=%d\n", dma_state);
  return 0;
}
