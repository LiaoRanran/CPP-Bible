# examples/ — 独立可编译示例集

> 存放各章精华示例的独立版本，可直接编译运行。
> 编译: `g++ -std=c++23 -O2 -Wall -o xxx.exe xxx.cpp`

## 已有示例

| 文件 | 关联内容 | 主题 |
|---|---|---|
| `json/json.hpp` + `json/json_test.cpp` | 贯穿项目（part03/04/05/06/07/08） | 手写 JSON 库：`std::variant` 递归类型 + 递归下降解析 + 序列化 |
| (待提取) | ch82-94 | STL 容器示例 |
| (待提取) | ch120 | Coroutine 示例 |

## 使用

```bash
cd examples
g++ -std=c++23 -O2 -Wall -o example_xxx.exe example_xxx.cpp
./example_xxx.exe
```

### 手写 JSON 库自测

```bash
cd json
g++ -std=c++23 -O2 -Wall -Wextra -o json_test.exe json_test.cpp
./json_test.exe          # 期望输出 "json_test: 68 passed, 0 failed"
```
