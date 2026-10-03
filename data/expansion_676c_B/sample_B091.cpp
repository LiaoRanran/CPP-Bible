// sample_B091
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B091.json)

#include <cstdio>
int main(){
  alignas(1) char buf[8] = {0};
  int* p = (int*)(buf + 1); /*DEFECT: misaligned access (UB) -> UBSan alignment catch */
  *p = 5;
  std::printf("%d\n", *p);
  return 0;
}