// sample_B025
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B025.json)

#include <climits>
#include <cstdio>
int main(){
  volatile int m = INT_MIN;
  volatile int r = m / -1; /*DEFECT: INT_MIN / -1 overflow */
  std::printf("%d\n", (int)r);
  return 0;
}