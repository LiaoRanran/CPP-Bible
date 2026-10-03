// sample_E091
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E091.json)

#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static void f(){
  std::lock(m1, m2);                        // 正确用法：一次性拿两把
  /*DEFECT: 拿到两把之后再手动 m2.lock()：同线程重复获取 ⇒ 自死锁 */
  m2.lock();
  std::printf("E091 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
