// sample_E015
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E015.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Cfg { int x; int y; };
static std::atomic<Cfg*> cfg_pub{nullptr};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  Cfg* c = new Cfg{3, 4};
  cfg_pub.store(c, std::memory_order_release);
  ready.store(true, std::memory_order_release);
}
static void consumer(){
  wait_go();
  while(!ready.load(std::memory_order_release)){}   /* 写侧也用 release，读侧无 acquire */
  /*DEFECT: consume 在 C++17 起不再具有特殊含义（实现通常退化为 relaxed），不能用来发布载荷*/
  Cfg* c = cfg_pub.load(std::memory_order_consume);
  std::printf("E015 x=%d y=%d\n", c->x, c->y);
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
