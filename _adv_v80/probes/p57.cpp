#include <cstdio>
#include <fstream>
#include <string>
int main(){ std::ifstream f("_adv_v80/probes/expected_data.txt");
  std::string l;
  while (std::getline(f, l)) std::printf("%s\n", l.c_str()); }
