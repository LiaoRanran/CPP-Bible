// _ch147_test.cpp —— 测试覆盖审查示例（GoogleTest 风格伪代码）
// 取证角度：每个公共函数至少一条正向 + 一条边界用例。
struct Stack {
    int pop();
    bool empty() const;
};

// 期望的测试关注点（审查时核对是否覆盖）：
//   - 空栈 pop() 行为
//   - 满栈边界
//   - 异常安全
void expect_tests_for(Stack& s) {
    (void)s;
}
