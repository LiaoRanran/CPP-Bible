// sample_B035
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B035.json)

#include <cstdio>
int main(){
  volatile int m = -2147483648;
  volatile int r = m + m; /*DEFECT: INT_MIN+INT_MIN overflow */
  std::printf("%d\n", (int)r);
  return 0;
}