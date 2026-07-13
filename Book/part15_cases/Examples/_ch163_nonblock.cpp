// _ch163_nonblock.cpp  [Windows Winsock2]
// 编译: g++ -std=c++23 -O2 _ch163_nonblock.cpp -lws2_32 -o _ch163_nonblock.exe
// 作用: 演示 ioctlsocket 设为非阻塞 + select 检测可写，完成异步 connect。
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <cstring>

int main() {
    WSADATA wsa{};
    WSAStartup(MAKEWORD(2, 2), &wsa);

    SOCKET fd = socket(AF_INET, SOCK_STREAM, 0);
    u_long mode = 1;                       // 1 = 非阻塞
    ioctlsocket(fd, FIONBIO, &mode);
    std::cout << "[nonblock] 已设为非阻塞模式\n";

    sockaddr_in a{};
    a.sin_family = AF_INET;
    a.sin_port = htons(54324);
    inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);

    // 非阻塞 connect 通常立即返回 WSAEWOULDBLOCK，需 select 等待可写。
    int r = connect(fd, (sockaddr*)&a, sizeof(a));
    std::cout << "[nonblock] connect 立即返回 r=" << r
              << " errno=" << WSAGetLastError() << "\n";

    fd_set wf;
    FD_ZERO(&wf);
    FD_SET(fd, &wf);
    timeval tv{1, 0};
    int wr = select(0, nullptr, &wf, nullptr, &tv);
    std::cout << "[nonblock] select 可写事件数=" << wr << "\n";

    closesocket(fd);
    WSACleanup();
    return 0;
}
