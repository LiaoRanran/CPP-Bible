// sample_B030
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B030.json)

#include <cstdio>
int main(){
  volatile int i = 0;
  for (volatile int k = 0; k < 2000000000; k++){ i++; /*DEFECT: overflow inside loop bound increment */ }
  std::printf("%d\n", (int)i);
  return 0;
}