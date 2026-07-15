
ch81_string_view_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <sv_substr(std::basic_string_view<char, std::char_traits<char> >, unsigned long long, unsigned long long)>:
   0:	48 83 ec 28          	sub    rsp,0x28
   4:	48 89 c8             	mov    rax,rcx
   7:	48 89 d1             	mov    rcx,rdx
   a:	48 8b 12             	mov    rdx,QWORD PTR [rdx]
   d:	48 8b 49 08          	mov    rcx,QWORD PTR [rcx+0x8]
  11:	4c 39 c2             	cmp    rdx,r8
  14:	0f 82 00 00 00 00    	jb     1a <sv_substr(std::basic_string_view<char, std::char_traits<char> >, unsigned long long, unsigned long long)+0x1a>
  1a:	4c 29 c2             	sub    rdx,r8
  1d:	4c 39 ca             	cmp    rdx,r9
  20:	49 0f 47 d1          	cmova  rdx,r9
  24:	4c 01 c1             	add    rcx,r8
  27:	48 89 48 08          	mov    QWORD PTR [rax+0x8],rcx
  2b:	48 89 10             	mov    QWORD PTR [rax],rdx
  2e:	48 83 c4 28          	add    rsp,0x28
  32:	c3                   	ret
  33:	66 90                	xchg   ax,ax
  35:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  3c:	00 00 00 00 

0000000000000040 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)>:
  40:	56                   	push   rsi
  41:	53                   	push   rbx
  42:	48 83 ec 38          	sub    rsp,0x38
  46:	48 8b 5a 08          	mov    rbx,QWORD PTR [rdx+0x8]
  4a:	48 89 ce             	mov    rsi,rcx
  4d:	4c 39 c3             	cmp    rbx,r8
  50:	0f 82 23 00 00 00    	jb     79 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x39>
  56:	48 8d 49 10          	lea    rcx,[rcx+0x10]
  5a:	4c 29 c3             	sub    rbx,r8
  5d:	48 89 0e             	mov    QWORD PTR [rsi],rcx
  60:	48 8b 02             	mov    rax,QWORD PTR [rdx]
  63:	4c 01 c0             	add    rax,r8
  66:	4c 39 cb             	cmp    rbx,r9
  69:	49 0f 47 d9          	cmova  rbx,r9
  6d:	48 89 c2             	mov    rdx,rax
  70:	48 83 fb 0f          	cmp    rbx,0xf
  74:	77 2a                	ja     a0 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x60>
  76:	48 83 fb 01          	cmp    rbx,0x1
  7a:	74 1c                	je     98 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x58>
  7c:	48 85 db             	test   rbx,rbx
  7f:	75 4f                	jne    d0 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x90>
  81:	48 89 f0             	mov    rax,rsi
  84:	48 89 5e 08          	mov    QWORD PTR [rsi+0x8],rbx
  88:	c6 04 19 00          	mov    BYTE PTR [rcx+rbx*1],0x0
  8c:	48 83 c4 38          	add    rsp,0x38
  90:	5b                   	pop    rbx
  91:	5e                   	pop    rsi
  92:	c3                   	ret
  93:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
  98:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  9b:	88 46 10             	mov    BYTE PTR [rsi+0x10],al
  9e:	eb e1                	jmp    81 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x41>
  a0:	48 b8 fe ff ff ff ff 	movabs rax,0x7ffffffffffffffe
  a7:	ff ff 7f 
  aa:	48 39 d8             	cmp    rax,rbx
  ad:	0f 82 17 00 00 00    	jb     ca <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x8a>
  b3:	48 8d 4b 01          	lea    rcx,[rbx+0x1]
  b7:	48 89 54 24 28       	mov    QWORD PTR [rsp+0x28],rdx
  bc:	e8 00 00 00 00       	call   c1 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x81>
  c1:	48 89 5e 10          	mov    QWORD PTR [rsi+0x10],rbx
  c5:	48 8b 54 24 28       	mov    rdx,QWORD PTR [rsp+0x28]
  ca:	48 89 06             	mov    QWORD PTR [rsi],rax
  cd:	48 89 c1             	mov    rcx,rax
  d0:	49 89 d8             	mov    r8,rbx
  d3:	e8 00 00 00 00       	call   d8 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x98>
  d8:	48 8b 0e             	mov    rcx,QWORD PTR [rsi]
  db:	eb a4                	jmp    81 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x41>
  dd:	0f 1f 00             	nop    DWORD PTR [rax]

00000000000000e0 <sv_at(std::basic_string_view<char, std::char_traits<char> >, unsigned long long)>:
  e0:	48 03 51 08          	add    rdx,QWORD PTR [rcx+0x8]
  e4:	0f b6 02             	movzx  eax,BYTE PTR [rdx]
  e7:	c3                   	ret
  e8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
  ef:	00 

00000000000000f0 <sv_size(std::basic_string_view<char, std::char_traits<char> >)>:
  f0:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  f3:	c3                   	ret
  f4:	90                   	nop
  f5:	90                   	nop
  f6:	90                   	nop
  f7:	90                   	nop
  f8:	90                   	nop
  f9:	90                   	nop
  fa:	90                   	nop
  fb:	90                   	nop
  fc:	90                   	nop
  fd:	90                   	nop
  fe:	90                   	nop
  ff:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <sv_substr(std::basic_string_view<char, std::char_traits<char> >, unsigned long long, unsigned long long) [clone .cold]>:
   0:	49 89 d1             	mov    r9,rdx
   3:	48 8d 0d 20 00 00 00 	lea    rcx,[rip+0x20]        # 2a <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long) [clone .cold]+0x13>
   a:	48 8d 15 00 00 00 00 	lea    rdx,[rip+0x0]        # 11 <sv_substr(std::basic_string_view<char, std::char_traits<char> >, unsigned long long, unsigned long long) [clone .cold]+0x11>
  11:	e8 00 00 00 00       	call   16 <sv_substr(std::basic_string_view<char, std::char_traits<char> >, unsigned long long, unsigned long long) [clone .cold]+0x16>
  16:	90                   	nop

0000000000000017 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long) [clone .cold]>:
  17:	48 8d 0d 9f 00 00 00 	lea    rcx,[rip+0x9f]        # bd <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x7d>
  1e:	e8 00 00 00 00       	call   23 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long) [clone .cold]+0xc>
  23:	49 89 d9             	mov    r9,rbx
  26:	48 8d 15 51 00 00 00 	lea    rdx,[rip+0x51]        # 7e <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x3e>
  2d:	48 8d 0d 68 00 00 00 	lea    rcx,[rip+0x68]        # 9c <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long)+0x5c>
  34:	e8 00 00 00 00       	call   39 <str_substr(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned long long, unsigned long long) [clone .cold]+0x22>
  39:	90                   	nop
  3a:	90                   	nop
  3b:	90                   	nop
  3c:	90                   	nop
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop

Disassembly of section .text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv:

0000000000000000 <std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::_M_dispose()>:
   0:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   3:	48 8d 51 10          	lea    rdx,[rcx+0x10]
   7:	48 39 d0             	cmp    rax,rdx
   a:	74 14                	je     20 <std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::_M_dispose()+0x20>
   c:	48 8b 51 10          	mov    rdx,QWORD PTR [rcx+0x10]
  10:	48 89 c1             	mov    rcx,rax
  13:	48 83 c2 01          	add    rdx,0x1
  17:	e9 00 00 00 00       	jmp    1c <std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::_M_dispose()+0x1c>
  1c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  20:	c3                   	ret
  21:	90                   	nop
  22:	90                   	nop
  23:	90                   	nop
  24:	90                   	nop
  25:	90                   	nop
  26:	90                   	nop
  27:	90                   	nop
  28:	90                   	nop
  29:	90                   	nop
  2a:	90                   	nop
  2b:	90                   	nop
  2c:	90                   	nop
  2d:	90                   	nop
  2e:	90                   	nop
  2f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	56                   	push   rsi
   1:	53                   	push   rbx
   2:	48 83 ec 78          	sub    rsp,0x78
   6:	e8 00 00 00 00       	call   b <main+0xb>
   b:	48 8d 4c 24 50       	lea    rcx,[rsp+0x50]
  10:	c7 44 24 2c 00 00 00 	mov    DWORD PTR [rsp+0x2c],0x0
  17:	00 
  18:	c7 44 24 2c 05 00 00 	mov    DWORD PTR [rsp+0x2c],0x5
  1f:	00 
  20:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  24:	48 c7 44 24 38 0b 00 	mov    QWORD PTR [rsp+0x38],0xb
  2b:	00 00 
  2d:	83 c0 6c             	add    eax,0x6c
  30:	c6 44 24 4b 00       	mov    BYTE PTR [rsp+0x4b],0x0
  35:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
  39:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  3d:	c7 44 24 60 68 65 6c 	mov    DWORD PTR [rsp+0x60],0x6c6c6568
  44:	6c 
  45:	83 c0 0b             	add    eax,0xb
  48:	c6 44 24 64 6f       	mov    BYTE PTR [rsp+0x64],0x6f
  4d:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
  51:	48 8d 44 24 40       	lea    rax,[rsp+0x40]
  56:	48 89 44 24 30       	mov    QWORD PTR [rsp+0x30],rax
  5b:	48 b8 68 65 6c 6c 6f 	movabs rax,0x6f77206f6c6c6568
  62:	20 77 6f 
  65:	48 89 44 24 40       	mov    QWORD PTR [rsp+0x40],rax
  6a:	48 8d 44 24 60       	lea    rax,[rsp+0x60]
  6f:	48 89 44 24 50       	mov    QWORD PTR [rsp+0x50],rax
  74:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  78:	c7 44 24 47 6f 72 6c 	mov    DWORD PTR [rsp+0x47],0x646c726f
  7f:	64 
  80:	83 c0 05             	add    eax,0x5
  83:	c6 44 24 65 00       	mov    BYTE PTR [rsp+0x65],0x0
  88:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
  8c:	8b 5c 24 2c          	mov    ebx,DWORD PTR [rsp+0x2c]
  90:	48 c7 44 24 58 05 00 	mov    QWORD PTR [rsp+0x58],0x5
  97:	00 00 
  99:	e8 00 00 00 00       	call   9e <main+0x9e>
  9e:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
  a3:	e8 00 00 00 00       	call   a8 <main+0xa8>
  a8:	8d 43 10             	lea    eax,[rbx+0x10]
  ab:	48 83 c4 78          	add    rsp,0x78
  af:	5b                   	pop    rbx
  b0:	5e                   	pop    rsi
  b1:	c3                   	ret
  b2:	90                   	nop
  b3:	90                   	nop
  b4:	90                   	nop
  b5:	90                   	nop
  b6:	90                   	nop
  b7:	90                   	nop
  b8:	90                   	nop
  b9:	90                   	nop
  ba:	90                   	nop
  bb:	90                   	nop
  bc:	90                   	nop
  bd:	90                   	nop
  be:	90                   	nop
  bf:	90                   	nop
