// sample_B092
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B092.json)

#include <cstdio>
int main(){
  int x = 0x1;
  int y = x << 32; /*DEFECT: shift by exactly width (UB) -> UBSan catch */
  std::printf("%d\n", (int)y);
  return 0;
}