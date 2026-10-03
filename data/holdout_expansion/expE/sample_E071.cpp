// sample_E071
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,ubsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E071.json)

#include <atomic>
#include <cstdio>
int main(){
  alignas(8) unsigned char raw[sizeof(std::atomic_flag) * 2];
  /*DEFECT: 直接把未初始化字节当作 atomic_flag 使用（缺 placement-new + ATOMIC_FLAG_INIT）：
     对未初始化内存做 test_and_set 是 UB */
  std::atomic_flag* f = reinterpret_cast<std::atomic_flag*>(raw);
  if (f->test_and_set(std::memory_order_acquire)) std::printf("E071 busy\n");
  f->clear(std::memory_order_release);
  std::printf("E071 ok\n");
  return 0;
}
