// sample_E011
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E011.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int mirror = 0;                    // 非原子镜像
static std::atomic<int> pub{0};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  mirror = 4242;                          // 非原子写（发生在 release 之前的那一批）
  pub.store(mirror, std::memory_order_relaxed);
  ready.store(true, std::memory_order_release);
  /*DEFECT: release 之后又去改非原子 mirror：这批写在 release/acquire 之外，
     读侧即使正确 acquire 了 ready，也与这批写没有 happens-before */
  mirror = 7777;
}
static void consumer(){
  wait_go();
  while(!ready.load(std::memory_order_acquire)){}
  /*DEFECT: 读到的是 release 之后那一批非原子写（值 7777），却没有 acquire 能覆盖它 ⇒ 数据竞争 */
  std::printf("E011 mirror=%d pub=%d\n", mirror, pub.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
