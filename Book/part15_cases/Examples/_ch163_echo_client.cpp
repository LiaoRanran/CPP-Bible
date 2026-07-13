// _ch163_echo_client.cpp  [Windows Winsock2]
// 编译: g++ -std=c++23 -O2 _ch163_echo_client.cpp -lws2_32 -o _ch163_echo_client.exe
// 行为: 连接 127.0.0.1:54321，发送一行 "HELLO_FROM_CLIENT"，打印回显后退出。
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <cstring>

int main() {
    WSADATA wsa{};
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        std::cerr << "[client] WSAStartup 失败\n";
        return 1;
    }
    SOCKET fd = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(54321);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
    if (connect(fd, (sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR) {
        std::cerr << "[client] connect 失败, code=" << WSAGetLastError() << "\n";
        return 1;
    }
    const char* msg = "HELLO_FROM_CLIENT\n";
    send(fd, msg, (int)std::strlen(msg), 0);
    std::cout << "[client] sent: " << msg << std::flush;

    char buf[256];
    int n = recv(fd, buf, sizeof(buf) - 1, 0);
    buf[n] = '\0';
    std::cout << "[client] received echo: " << buf << std::flush;

    closesocket(fd);
    WSACleanup();
    return 0;
}
