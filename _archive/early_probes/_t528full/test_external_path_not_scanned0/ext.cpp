#include <cstdio>
#include <fstream>
#include <string>
int main(){ std::ifstream f("/etc/hostname"); std::string line;
  std::getline(f, line); std::printf("%s\n", line.c_str()); }
