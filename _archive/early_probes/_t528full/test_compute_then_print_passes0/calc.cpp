#include <cstdio>
#include <fstream>
#include <string>
int main(){ std::ifstream f("data.txt"); std::string line;
  std::getline(f, line); int v = std::stoi(line.substr(7)) + 1;
  std::printf("result=%d\n", v); }
