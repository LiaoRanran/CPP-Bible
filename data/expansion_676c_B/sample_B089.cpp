// sample_B089
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B089.json)

#include <cstring>
#include <cstdio>
int main(){
  int dst[4] = {0};
  std::memcpy(dst, nullptr, 4 * sizeof(int)); /*DEFECT: memcpy from null source (UB) -> ASan */
  std::printf("%d\n", dst[0]);
  return 0;
}