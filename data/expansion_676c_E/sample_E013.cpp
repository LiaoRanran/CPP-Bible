// sample_E013
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E013.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<unsigned long long> stamp{0};
static std::atomic<bool> flag{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  /*DEFECT: 载荷与标志都用 relaxed：整条发布链没有任何 release，读者无法保证看到载荷*/
  stamp.store(0xDEADBEEFULL, std::memory_order_relaxed);
  flag.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!flag.load(std::memory_order_relaxed)){}
  std::printf("E013 stamp=%llx\n", stamp.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
