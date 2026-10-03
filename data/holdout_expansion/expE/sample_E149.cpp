// sample_E149
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E149.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static unsigned char img[64][64];
static std::atomic<int> stage{0};
static void low(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做 64x64 像素的滤波运算（持锁耗时计算） */
  for (int pass = 0; pass < 400; ++pass)
    for (int y = 0; y < 64; ++y)
      for (int x = 0; x < 64; ++x)
        img[y][x] = (unsigned char)((img[y][x] * 3 + pass) & 0xFF);
  stage.store(2, std::memory_order_release);
}
static void high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等锁读取像素 */
  std::lock_guard<std::mutex> lk(m);
  std::printf("E149 px=%d\n", img[0][0]);
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(low), b(high);
  a.join(); b.join();
  return 0;
}
