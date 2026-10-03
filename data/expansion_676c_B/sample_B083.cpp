// sample_B083
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B083.json)

#include <cstdio>
int main(){
  volatile int x = 1;
  volatile int y = x << 40; /*DEFECT: shift count >= width (UB) */
  std::printf("%d\n", (int)y);
  return 0;
}