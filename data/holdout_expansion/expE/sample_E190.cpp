// sample_E190
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E190.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static std::atomic<bool> ready{false};
static int config[16] = {0};           // 非原子配置数据
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: 谓词只同步了「ready 这一个原子」，config 是普通数组：
             即使谓词判断完全正确，读 config 依然没有 happens-before */
  while (!ready.load(std::memory_order_acquire)) cv.wait(lk);
  lk.unlock();
  /*DEFECT: 解锁后无锁读 config，与 loader 的无锁写并发 ⇒ 数据竞争 */
  int s = 0;
  for (int i = 0; i < 400000; ++i) s += config[i % 16];
  std::printf("E190 sum=%d\n", s);
}
static void loader(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  /*DEFECT: 只把 ready 这个原子置位就把读者放行，真正的数据 config 还在锁外继续写 */
  ready.store(true, std::memory_order_relaxed);
  {
    std::lock_guard<std::mutex> lk(m);
  }
  cv.notify_all();
  for (int k = 0; k < 400000; ++k) config[k % 16] += 1;   // 数据尚未就绪
}
int main(){
  std::thread a(waiter), b(loader);
  a.join(); b.join();
  return 0;
}
