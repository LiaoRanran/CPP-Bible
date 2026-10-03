// sample_B080
// defect_type: type_punning
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B080.json)

#include <cstdio>
int main(){
  long long L = 0x3FF0000000000000LL;
  double d = reinterpret_cast<double&>(L); /*DEFECT: reinterpret long long as double (UB); aligned, no trap */
  std::printf("%f\n", d);
  return 0;
}