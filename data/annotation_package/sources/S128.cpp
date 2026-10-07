int main(){
  int input = 9;
  int* p = new int[2];
  if (input == 9) { delete[] p; } // [redacted]
  delete[] p;
  return 0;
}

