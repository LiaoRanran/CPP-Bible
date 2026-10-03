// sample_E090
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E090.json)

#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static void f(){
  std::unique_lock<std::mutex> held(m1, std::adopt_lock);
  m1.lock();
  /*DEFECT: adopt_lock 之后 m1 归本线程所有，再交给 std::lock 会与自身冲突 ⇒ 自死锁 */
  std::lock(m1, m2);
  std::printf("E090 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
