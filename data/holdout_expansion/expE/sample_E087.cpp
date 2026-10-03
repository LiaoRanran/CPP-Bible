// sample_E087
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E087.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex A, B;
static std::atomic<bool> first_held{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void need_b(){
  wait_go();
  std::unique_lock<std::mutex> a(A);
  first_held.store(true, std::memory_order_release);
  while(!first_held.load(std::memory_order_acquire)){}
  /*DEFECT: 持 A 等 B（hold-and-wait）*/
  std::unique_lock<std::mutex> b(B);
  std::printf("E087 got both\n");
}
static void need_a(){
  wait_go();
  while(!first_held.load(std::memory_order_acquire)){}
  std::unique_lock<std::mutex> b(B);
  /*DEFECT: 持 B 等 A，与上面构成循环等待 ⇒ 死锁 */
  std::unique_lock<std::mutex> a(A);
  std::printf("E087 got both reverse\n");
}
int main(){
  std::thread x(need_b), y(need_a);
  go.store(true, std::memory_order_release);
  x.join(); y.join();
  return 0;
}
