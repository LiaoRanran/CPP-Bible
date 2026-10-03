// sample_E182
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E182.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool ready = false;             // 谓词
static int payload = 0;                // 非原子
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: 谓词 ready 会被另一线程「无锁写」，wait 的谓词检查与那次写构成数据竞争，
     编译器/CPU 可把它缓存成 false ⇒ 丢失唤醒 */
  while (!ready) cv.wait(lk);
  std::printf("E182 payload=%d\n", payload);
}
static void setter(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  payload = 99;                        // 非原子写
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  /*DEFECT: 不持有 m 就修改谓词 ready：与 wait 里的谓词读是数据竞争 */
  ready = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(setter);
  a.join(); b.join();
  return 0;
}
