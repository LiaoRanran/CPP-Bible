// sample_E029
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E029.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int slot_v[4] = {0, 0, 0, 0};
static std::atomic<int> a_flag{0}, b_flag{0}, go{0};
static void wait_go(){ while(go.load(std::memory_order_acquire) == 0){} }
static void producer(){
  wait_go();
  slot_v[0] = 1;
  a_flag.store(1, std::memory_order_release);
  slot_v[1] = 2;
  /*DEFECT: b_flag 用 relaxed 存储：它切断了 a_flag 建立的 release 序列的延伸，读侧 acquire b_flag 得不到 slot_v 的可见性*/
  b_flag.store(1, std::memory_order_relaxed);
  slot_v[2] = 3;
}
static void consumer(){
  wait_go();
  while (b_flag.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 此时读 slot_v[2]：该写入在 relaxed store 之后，无任何 acquire 与之配对 → 数据竞争*/
  std::printf("E029 v2=%d\n", slot_v[2]);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(1, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
