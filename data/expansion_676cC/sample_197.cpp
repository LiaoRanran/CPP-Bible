int main(){
  double d = 3.999;
  int r = (int)d; // <<PLANTED-DEFECT>> 浮点截断：r=3 而非 4（特定输入下逻辑错误）
  (void)r;
  return 0;
}

