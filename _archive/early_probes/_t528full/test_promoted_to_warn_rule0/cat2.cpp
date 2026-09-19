#include <cstdio>
#include <fstream>
#include <string>
int main(){ std::ifstream f("data.txt"); std::string line;
  while (std::getline(f, line)) std::printf("%s\n", line.c_str()); }
