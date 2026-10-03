// sample_E019
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E019.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int chunk[16];
static std::atomic<int> phase{0}, go{0};
static void wait_go(){ while(go.load(std::memory_order_acquire) == 0){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 16; ++i) chunk[i] = i * 2;         // 非原子写
  phase.store(1, std::memory_order_release);
  for (int i = 16; i < 32; ++i) chunk[i] = i * 2;
  /*DEFECT: 末段 phase 用 relaxed 存储：读侧即使 acquire 也拿不到第二段非原子写的 happens-before*/
  phase.store(2, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(phase.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 此时读 chunk 的全部 32 个元素，其中后 16 个的写入未被同步保护 → 数据竞争*/
  std::printf("E019 chunk31=%d\n", chunk[31]);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(1, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
