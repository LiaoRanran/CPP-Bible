// sample_E085
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E085.json)

#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m;
static int depth = 0;
static void walk(int n){
  std::lock_guard<std::mutex> g(m);
  depth++;
  if (n > 0) walk(n - 1);        /*DEFECT: 递归下降时重复 lock 同一把非递归 mutex ⇒ 第二层即自死锁 */
}
int main(){
  std::thread t([]{ walk(4); });
  t.join();
  std::printf("E085 depth=%d\n", depth);
  return 0;
}
