// sample_E158
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E158.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex scene_lock;
static int frame = 0;
static std::atomic<int> stage{0};
static void loader(){
  std::lock_guard<std::mutex> lk(scene_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁等待「同步预读」完成：渲染线程（高优先级）在这段时间完全无法推进 */
  std::this_thread::sleep_for(std::chrono::milliseconds(220));
  frame = 1;
  stage.store(2, std::memory_order_release);
}
static void render(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 渲染线程等锁 */
  std::lock_guard<std::mutex> lk(scene_lock);
  frame = 2;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(loader), b(render);
  a.join(); b.join();
  std::printf("E158 frame=%d\n", frame);
  return 0;
}
