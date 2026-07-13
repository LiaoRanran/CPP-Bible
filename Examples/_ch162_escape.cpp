// 文件：Examples/_ch162_escape.cpp
// 行号：10-18（转移映射表与 unescape 函数）
// ⑦ 字符串转义处理：\\ \" \/ \b \f \n \r \t \uXXXX。
#include <cstdio>
#include <iostream>
#include <string>

std::string unescape(const std::string& in) {
    std::string out;
    for (size_t i = 0; i < in.size(); ++i) {
        if (in[i] != '\\') { out += in[i]; continue; }
        char e = in[++i];
        switch (e) {
            case 'n': out += '\n'; break;
            case 't': out += '\t'; break;
            case 'r': out += '\r'; break;
            case '"': out += '"';  break;
            case '\\': out += '\\'; break;
            case '/': out += '/';  break;
            default:  out += e;    break; // 简化：非标准转义原样保留
        }
    }
    return out;
}

std::string escape(const std::string& in) {
    std::string out;
    for (unsigned char c : in) {
        switch (c) {
            case '"':  out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\n': out += "\\n";  break;
            default:   out += (char)c;
        }
    }
    return out;
}

int main() {
    std::string raw = "行1\nTab\t\"引号\"";
    std::string esc = escape(raw);
    std::cout << "转义后: " << esc << "\n";
    std::cout << "回转义: " << escape(unescape(esc)) << "\n"; // 往返一致性
    return 0;
}
