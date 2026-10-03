// sample_B087
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B087.json)

#include <cstdio>
int main(){
  char* s = (char*)"hello";
  s[0] = 'H'; /*DEFECT: modify string literal (UB) -> ASan RO write */
  std::printf("%s\n", s);
  return 0;
}