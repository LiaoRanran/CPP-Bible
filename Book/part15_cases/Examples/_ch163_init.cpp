// _ch163_init.cpp  [Windows Winsock2]
// 编译: g++ -std=c++23 -O2 _ch163_init.cpp -lws2_32 -o _ch163_init.exe
// 作用: 验证本机 Winsock2 工具链可初始化，并打印版本号。
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>

int main() {
    WSADATA wsa{};
    int rc = WSAStartup(MAKEWORD(2, 2), &wsa);
    if (rc != 0) {
        std::cerr << "[init] WSAStartup 失败, code=" << rc << "\n";
        return 1;
    }
    std::cout << "[init] Winsock 版本: "
              << (int)LOBYTE(wsa.wVersion) << "."
              << (int)HIBYTE(wsa.wVersion) << "\n";
    std::cout << "[init] 描述: " << wsa.szDescription << "\n";
    WSACleanup();
    return 0;
}
