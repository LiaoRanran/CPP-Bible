#include <cstdlib>
#include <cstdio>
int main(){
  // 假设 malloc 返回 16 字节对齐（实际仅保证 alignof(max_align_t)）
  void* p = std::malloc(64);
  double* dp = reinterpret_cast<double*>(p);  // <<PLANTED-DEFECT>> 误信充足对齐
  dp[0] = 3.14;
  std::printf("%f\n", dp[0]);
  std::free(p);
  return 0;
}
