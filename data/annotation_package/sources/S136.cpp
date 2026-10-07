// sample_B045
// [redacted]
// severity: medium
// [redacted]
// expected_verdict: catch
// [redacted]
// (authoritative annotation in sample_B045.json)

#include <cstdio>
int main(){
  int* p = new int(1);
  p = new int(2); /* [redacted]*/
  std::printf("%d\n", *p);
  delete p;
  return 0;
}
