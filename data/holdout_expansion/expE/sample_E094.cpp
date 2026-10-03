// sample_E094
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E094.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m1, m2, m3;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void gate(int n){ while (held.load(std::memory_order_acquire) < n){} }
static void t1(){
  wait_go();
  std::lock_guard<std::mutex> a(m1);
  held.fetch_add(1, std::memory_order_release); gate(3);
  /*DEFECT: m1->m2 */
  std::lock_guard<std::mutex> b(m2);
  std::printf("E094 t1\n");
}
static void t2(){
  wait_go();
  std::lock_guard<std::mutex> b(m2);
  held.fetch_add(1, std::memory_order_release); gate(3);
  /*DEFECT: m2->m3 */
  std::lock_guard<std::mutex> c(m3);
  std::printf("E094 t2\n");
}
static void t3(){
  wait_go();
  std::lock_guard<std::mutex> c(m3);
  held.fetch_add(1, std::memory_order_release); gate(3);
  /*DEFECT: m3->m1，与 t1 的 m1->m2、t2 的 m2->m3 构成圆周等待 ⇒ 三方死锁 */
  std::lock_guard<std::mutex> a(m1);
  std::printf("E094 t3\n");
}
int main(){
  std::thread x(t1), y(t2), z(t3);
  go.store(true, std::memory_order_release);
  x.join(); y.join(); z.join();
  return 0;
}
