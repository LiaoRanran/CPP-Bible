// sample_B024
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B024.json)

#include <cstdio>
int main(){
  volatile int m = -2147483648;
  volatile int r = -m; /*DEFECT: unary minus overflow on INT_MIN */
  std::printf("%d\n", (int)r);
  return 0;
}