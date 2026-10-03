
#include <string>
const std::string& get(const std::string& s){ return s; }
int main(){ const std::string& r = get(std::string("tmp")); return (int)r.size(); }
