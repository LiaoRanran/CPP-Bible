// 文件：Examples/_ch162_tokenizer.cpp
// 行号：14-22（Token 枚举与 tokenize 函数）
// ⑤ 词法分析（tokenizer）：在解析器之前/之中把字符流切成 token。
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

enum class Tok { LBrace, RBrace, LBrack, RBrack, Colon, Comma, Str, Num, True, False, Null };
struct Token { Tok kind; std::string text; };

std::vector<Token> tokenize(std::string_view s) {
    std::vector<Token> out;
    size_t i = 0;
    while (i < s.size()) {
        char c = s[i];
        if (c == ' ' || c == '\t' || c == '\n' || c == '\r') { ++i; continue; }
        switch (c) {
            case '{': out.push_back({Tok::LBrace, "{"}); ++i; break;
            case '}': out.push_back({Tok::RBrace, "}"}); ++i; break;
            case '[': out.push_back({Tok::LBrack, "["}); ++i; break;
            case ']': out.push_back({Tok::RBrack, "]"}); ++i; break;
            case ':': out.push_back({Tok::Colon,  ":"}); ++i; break;
            case ',': out.push_back({Tok::Comma,  ","}); ++i; break;
            case '"': {
                std::string str; ++i;
                while (i < s.size() && s[i] != '"') str += s[i++];
                if (i < s.size()) ++i; // 跳过闭合 "
                out.push_back({Tok::Str, str});
                break;
            }
            default:
                // 字面量 true / false / null
                if (s.substr(i, 4) == "true")  { out.push_back({Tok::True,  "true"});  i += 4; break; }
                if (s.substr(i, 5) == "false") { out.push_back({Tok::False, "false"}); i += 5; break; }
                if (s.substr(i, 4) == "null")  { out.push_back({Tok::Null,  "null"});  i += 4; break; }
                std::string num;
                while (i < s.size() && (std::isdigit((unsigned char)s[i]) ||
                                        s[i]=='-'||s[i]=='.'||s[i]=='e'||s[i]=='E'))
                    num += s[i++];
                out.push_back({Tok::Num, num});
        }
    }
    return out;
}

int main() {
    auto toks = tokenize(R"({"a":[1,true]})");
    std::cout << "token 数: " << toks.size() << "\n";
    for (const auto& t : toks)
        std::cout << "[" << t.text << "] ";
    std::cout << "\n";
    return 0;
}
