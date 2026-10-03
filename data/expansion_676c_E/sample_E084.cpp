// sample_E084
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E084.json)

#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m;
static void f(){
  std::lock_guard<std::mutex> g1(m);
  /*DEFECT: 同一线程对同一把非递归 mutex 再取一次锁（复制粘贴式防御性加锁）⇒ 自死锁 */
  std::lock_guard<std::mutex> g2(m);
  std::printf("E084 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
