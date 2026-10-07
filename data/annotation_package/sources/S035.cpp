// sample_B064
// [redacted]
// severity: medium
// [redacted]
// expected_verdict: catch
// [redacted]
// (authoritative annotation in sample_B064.json)

#include <cstdio>
int main(){
  alignas(1) char b[16] = {0};
  double* p = (double*)(b + 1); /* [redacted]*/
  *p = 1.0;
  std::printf("%f\n", *p);
  return 0;
}
