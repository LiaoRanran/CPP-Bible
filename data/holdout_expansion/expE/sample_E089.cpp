// sample_E089
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E089.json)

#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static void f(){
  std::unique_lock<std::mutex> held(m1);      // 先持有 m1
  /*DEFECT: std::lock 的死锁避免算法假设「调用者不持有其中任何一把」；
     此处 m1 已被本线程持有，算法在 try_lock 阶段永远拿不到 m1 ⇒ 自死锁 */
  std::lock(m1, m2);
  std::printf("E089 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
