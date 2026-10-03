// sample_B032
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B032.json)

#include <cstdio>
int main(){
  volatile int a = 100000;
  volatile int b = 100000;
  volatile int dot = a * b + a * b; /*DEFECT: overflow in dot-product-like expr */
  std::printf("%d\n", (int)dot);
  return 0;
}