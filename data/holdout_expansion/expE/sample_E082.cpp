// sample_E082
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E082.json)

#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m;
static int depth = 0;
static void inner(){
  /*DEFECT: 非递归 std::mutex 被同一线程再次 lock：std::mutex 不支持同线程重入 ⇒ 自死锁 */
  std::lock_guard<std::mutex> g(m);
  depth++;
}
static void outer(){
  std::lock_guard<std::mutex> g(m);
  depth++;
  inner();
}
int main(){
  std::thread a(outer);
  a.join();
  std::printf("E082 depth=%d\n", depth);
  return 0;
}
