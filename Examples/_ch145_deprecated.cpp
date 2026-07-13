// _ch145_deprecated.cpp —— [[deprecated]] 弃用属性（g++ 警告取证）
[[deprecated("use new_api() instead; removed in v3")]]
void old_api() {}

void new_api() {}

int main() {
    old_api();   // 触发弃用警告
    new_api();
    return 0;
}
