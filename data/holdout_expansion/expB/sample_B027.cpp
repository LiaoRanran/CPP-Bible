// sample_B027
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B027.json)

#include <cstdio>
int main(){
  volatile long long a = 5000000000LL;
  volatile long long b = a * 5; /*DEFECT: signed 64-bit overflow */
  std::printf("%lld\n", b);
  return 0;
}