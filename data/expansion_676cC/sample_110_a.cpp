extern int y;
int x = y + 1; // <<PLANTED-DEFECT>> 依赖 y，但 y 可能尚未构造（静态初始化顺序未定义）

