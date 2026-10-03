// sample_E040
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E040.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int table[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static std::atomic<bool> once{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void init_table(){
  wait_go();
  for (int i = 0; i < 16; ++i) table[i] = i * i;        // 非原子写
  once.store(true, std::memory_order_seq_cst);
}
static void reader(){
  wait_go();
  /*DEFECT: once 用 relaxed 轮询：无法消费 seq_cst 存储的 release 语义，读非原子 table 构成竞争*/
  while (!once.load(std::memory_order_relaxed)){}
  std::printf("E040 t15=%d\n", table[15]);
}
int main(){
  std::thread i(init_table), r(reader);
  go.store(true, std::memory_order_release);
  i.join(); r.join();
  return 0;
}
