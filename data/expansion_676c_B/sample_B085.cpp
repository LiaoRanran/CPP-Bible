// sample_B085
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B085.json)

#include <cstdio>
int main(){
  volatile int x = -1;
  volatile int y = x << 2; /*DEFECT: left shift of negative value (UB) */
  std::printf("%d\n", (int)y);
  return 0;
}