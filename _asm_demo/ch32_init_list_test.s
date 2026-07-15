
ch32_init_list_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <sum_il(std::initializer_list<int>)>:
   0:	48 8b 51 08          	mov    rdx,QWORD PTR [rcx+0x8]
   4:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   7:	48 8d 0c 90          	lea    rcx,[rax+rdx*4]
   b:	31 d2                	xor    edx,edx
   d:	48 39 c1             	cmp    rcx,rax
  10:	74 19                	je     2b <sum_il(std::initializer_list<int>)+0x2b>
  12:	0f 1f 00             	nop    DWORD PTR [rax]
  15:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  1c:	00 00 00 00 
  20:	03 10                	add    edx,DWORD PTR [rax]
  22:	48 83 c0 04          	add    rax,0x4
  26:	48 39 c8             	cmp    rax,rcx
  29:	75 f5                	jne    20 <sum_il(std::initializer_list<int>)+0x20>
  2b:	89 d0                	mov    eax,edx
  2d:	c3                   	ret
  2e:	66 90                	xchg   ax,ax

0000000000000030 <il_begin(std::initializer_list<int>)>:
  30:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  33:	c3                   	ret
  34:	90                   	nop
  35:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  3c:	00 00 00 00 

0000000000000040 <dangling_il()>:
  40:	48 8d 15 00 00 00 00 	lea    rdx,[rip+0x0]        # 47 <dangling_il()+0x7>
  47:	48 89 c8             	mov    rax,rcx
  4a:	48 89 11             	mov    QWORD PTR [rcx],rdx
  4d:	48 c7 41 08 03 00 00 	mov    QWORD PTR [rcx+0x8],0x3
  54:	00 
  55:	c3                   	ret
  56:	90                   	nop
  57:	90                   	nop
  58:	90                   	nop
  59:	90                   	nop
  5a:	90                   	nop
  5b:	90                   	nop
  5c:	90                   	nop
  5d:	90                   	nop
  5e:	90                   	nop
  5f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	48 83 ec 38          	sub    rsp,0x38
   4:	e8 00 00 00 00       	call   9 <main+0x9>
   9:	c7 44 24 2c 00 00 00 	mov    DWORD PTR [rsp+0x2c],0x0
  10:	00 
  11:	c7 44 24 2c 64 00 00 	mov    DWORD PTR [rsp+0x2c],0x64
  18:	00 
  19:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  1d:	83 c0 01             	add    eax,0x1
  20:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
  24:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  28:	48 83 c4 38          	add    rsp,0x38
  2c:	c3                   	ret
  2d:	90                   	nop
  2e:	90                   	nop
  2f:	90                   	nop
