// sample_E106
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E106.json)

#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static int depth = 0;
static void enter(int d){
  std::scoped_lock<std::mutex, std::mutex> sl(m1, m2);
  depth++;
  if (d > 0) enter(d - 1);     /*DEFECT: 递归重入时对同一对锁再做一次 scoped_lock ⇒ 自死锁 */
}
int main(){
  std::thread t([]{ enter(3); });
  t.join();
  std::printf("E106 depth=%d\n", depth);
  return 0;
}
