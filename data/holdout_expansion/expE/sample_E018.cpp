// sample_E018
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E018.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int payload_a[4] = {0, 0, 0, 0};
static int payload_b[4] = {0, 0, 0, 0};
static std::atomic<bool> flag_a{false}, flag_b{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  for (int i = 0; i < 4; ++i) payload_a[i] = i + 1;      // 非原子写
  flag_a.store(true, std::memory_order_release);
  for (int i = 0; i < 4; ++i) payload_b[i] = i + 51;     // 非原子写
  flag_b.store(true, std::memory_order_release);
  /*DEFECT: 在 flag_b 的 release **之后**又改写 payload_a：
     读侧只 acquire flag_b，拿不到这批写的 happens-before ⇒ 竞争真实存在 */
  for (int i = 0; i < 4; ++i) payload_a[i] = i + 101;
}
static void consumer(){
  wait_go();
  /*DEFECT: 只 acquire flag_b 就去读 payload_a：flag_a 保护的载荷没有对应的 acquire，构成竞争*/
  while(!flag_b.load(std::memory_order_acquire)){}
  std::printf("E018 a3=%d b3=%d\n", payload_a[3], payload_b[3]);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
