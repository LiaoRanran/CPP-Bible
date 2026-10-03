// sample_E105
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E105.json)

#include <mutex>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static void f(){
  std::scoped_lock<std::mutex, std::mutex> sl(m1, m2);
  /*DEFECT: scoped_lock 已同时持有 m1/m2，又手动 m1.lock() ⇒ 同线程重复获取非递归锁，自死锁 */
  std::lock_guard<std::mutex> g(m1);
  std::printf("E105 never\n");
}
int main(){
  std::thread t(f);
  t.join();
  return 0;
}
