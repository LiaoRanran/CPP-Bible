// sample_B062
// defect_type: type_punning
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B062.json)

#include <cstdio>
int main(){
  char buf[8] = {0};
  long long* p = (long long*)(buf + 3); /*DEFECT: misaligned 8-byte access -> UBSan catch */
  *p = 1;
  std::printf("%lld\n", *p);
  return 0;
}