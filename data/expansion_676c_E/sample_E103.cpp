// sample_E103
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E103.json)

#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m;
static void f(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: unique_lock 已拥有 m 时再调用 lock()：标准未定义此用法，libstdc++ 上退化为自死锁 */
  lk.lock();
  std::printf("E103 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
