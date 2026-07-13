// _ch163_select.cpp  [Windows Winsock2]
// 编译: g++ -std=c++23 -O2 _ch163_select.cpp -lws2_32 -o _ch163_select.exe
// 作用: select() 单线程并发回显服务器骨架（演示 I/O 多路复用，编译通过证据）。
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <vector>
#include <cstring>

int main() {
    WSADATA wsa{};
    WSAStartup(MAKEWORD(2, 2), &wsa);

    SOCKET lfd = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in a{};
    a.sin_family = AF_INET;
    a.sin_port = htons(54323);
    inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);
    bind(lfd, (sockaddr*)&a, sizeof(a));
    listen(lfd, 8);

    fd_set master;
    FD_ZERO(&master);
    FD_SET(lfd, &master);
    std::vector<SOCKET> clients;
    std::cout << "[select] 单线程多路复用服务器骨架就绪 (port 54323)\n";

    // 骨架：真实工程里在此循环 select/accept/recv/echo，此处仅展示结构。
    (void)master; (void)clients;
    closesocket(lfd);
    WSACleanup();
    return 0;
}
