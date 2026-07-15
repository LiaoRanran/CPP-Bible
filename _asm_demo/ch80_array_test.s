
ch80_array_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <access_by_index(std::array<int, 8ull> const&, int)>:
   0:	48 63 d2             	movsxd rdx,edx
   3:	8b 04 91             	mov    eax,DWORD PTR [rcx+rdx*4]
   6:	c3                   	ret
   7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   e:	00 00 

0000000000000010 <access_raw(int const*, int)>:
  10:	48 63 d2             	movsxd rdx,edx
  13:	8b 04 91             	mov    eax,DWORD PTR [rcx+rdx*4]
  16:	c3                   	ret
  17:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  1e:	00 00 

0000000000000020 <access_at(std::array<int, 8ull> const&, int)>:
  20:	48 83 ec 28          	sub    rsp,0x28
  24:	48 63 d2             	movsxd rdx,edx
  27:	48 83 fa 07          	cmp    rdx,0x7
  2b:	0f 87 00 00 00 00    	ja     31 <access_at(std::array<int, 8ull> const&, int)+0x11>
  31:	8b 04 91             	mov    eax,DWORD PTR [rcx+rdx*4]
  34:	48 83 c4 28          	add    rsp,0x28
  38:	c3                   	ret
  39:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000000040 <get_data(std::array<int, 8ull> const&)>:
  40:	48 89 c8             	mov    rax,rcx
  43:	c3                   	ret
  44:	90                   	nop
  45:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  4c:	00 00 00 00 

0000000000000050 <by_value_copy(std::array<int, 8ull>)>:
  50:	f3 0f 6f 02          	movdqu xmm0,XMMWORD PTR [rdx]
  54:	4c 8b 42 10          	mov    r8,QWORD PTR [rdx+0x10]
  58:	4c 8b 4a 18          	mov    r9,QWORD PTR [rdx+0x18]
  5c:	48 89 c8             	mov    rax,rcx
  5f:	4c 89 41 10          	mov    QWORD PTR [rcx+0x10],r8
  63:	4c 89 49 18          	mov    QWORD PTR [rcx+0x18],r9
  67:	0f 11 01             	movups XMMWORD PTR [rcx],xmm0
  6a:	c3                   	ret
  6b:	90                   	nop
  6c:	90                   	nop
  6d:	90                   	nop
  6e:	90                   	nop
  6f:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <access_at(std::array<int, 8ull> const&, int) [clone .cold]>:
   0:	41 b8 08 00 00 00    	mov    r8d,0x8
   6:	48 8d 0d 00 00 00 00 	lea    rcx,[rip+0x0]        # d <access_at(std::array<int, 8ull> const&, int) [clone .cold]+0xd>
   d:	e8 00 00 00 00       	call   12 <access_at(std::array<int, 8ull> const&, int) [clone .cold]+0x12>
  12:	90                   	nop
  13:	90                   	nop
  14:	90                   	nop
  15:	90                   	nop
  16:	90                   	nop
  17:	90                   	nop
  18:	90                   	nop
  19:	90                   	nop
  1a:	90                   	nop
  1b:	90                   	nop
  1c:	90                   	nop
  1d:	90                   	nop
  1e:	90                   	nop
  1f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	48 83 ec 38          	sub    rsp,0x38
   4:	e8 00 00 00 00       	call   9 <main+0x9>
   9:	c7 44 24 2c 00 00 00 	mov    DWORD PTR [rsp+0x2c],0x0
  10:	00 
  11:	c7 44 24 2c 04 00 00 	mov    DWORD PTR [rsp+0x2c],0x4
  18:	00 
  19:	c7 44 24 2c 04 00 00 	mov    DWORD PTR [rsp+0x2c],0x4
  20:	00 
  21:	c7 44 24 2c 03 00 00 	mov    DWORD PTR [rsp+0x2c],0x3
  28:	00 
  29:	c7 44 24 2c 01 00 00 	mov    DWORD PTR [rsp+0x2c],0x1
  30:	00 
  31:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  35:	83 c0 01             	add    eax,0x1
  38:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
  3c:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  40:	83 c0 20             	add    eax,0x20
  43:	48 83 c4 38          	add    rsp,0x38
  47:	c3                   	ret
  48:	90                   	nop
  49:	90                   	nop
  4a:	90                   	nop
  4b:	90                   	nop
  4c:	90                   	nop
  4d:	90                   	nop
  4e:	90                   	nop
  4f:	90                   	nop
