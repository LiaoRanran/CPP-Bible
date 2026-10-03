// sample_E161
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E161.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <string>
#include <cstdio>
static std::mutex cfg_lock;
static std::string cfg = "k=v;k2=v2;k3=v3;k4=v4";
static std::atomic<int> stage{0};
static void cfg_parser(){
  std::lock_guard<std::mutex> lk(cfg_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 低优先级线程持锁做配置解析（字符串切分 + 校验），持续时间长 */
  for (int i = 0; i < 40000; ++i){
    size_t p = cfg.find(';');
    if (p == std::string::npos) break;
    cfg = cfg.substr(p + 1) + ";k=v";
  }
  stage.store(2, std::memory_order_release);
}
static void ctrl(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 控制线程（高优先级）必须等锁才能下发命令 */
  std::lock_guard<std::mutex> lk(cfg_lock);
  cfg = "k=ctrl";
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(cfg_parser), b(ctrl);
  a.join(); b.join();
  std::printf("E161 cfg=%s\n", cfg.c_str());
  return 0;
}
