
ch41_esft_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <sizeof_plain()>:
   0:	b8 04 00 00 00       	mov    eax,0x4
   5:	c3                   	ret
   6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   d:	00 00 00 

0000000000000010 <sizeof_with_esft()>:
  10:	b8 18 00 00 00       	mov    eax,0x18
  15:	c3                   	ret
  16:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  1d:	00 00 00 

0000000000000020 <grab(WithEsft*)>:
  20:	48 83 ec 28          	sub    rsp,0x28
  24:	48 8b 42 08          	mov    rax,QWORD PTR [rdx+0x8]
  28:	48 89 41 08          	mov    QWORD PTR [rcx+0x8],rax
  2c:	48 85 c0             	test   rax,rax
  2f:	0f 84 00 00 00 00    	je     35 <grab(WithEsft*)+0x15>
  35:	4c 8d 40 08          	lea    r8,[rax+0x8]
  39:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
  3c:	85 c0                	test   eax,eax
  3e:	0f 84 00 00 00 00    	je     44 <grab(WithEsft*)+0x24>
  44:	44 8d 48 01          	lea    r9d,[rax+0x1]
  48:	f0 45 0f b1 08       	lock cmpxchg DWORD PTR [r8],r9d
  4d:	75 ed                	jne    3c <grab(WithEsft*)+0x1c>
  4f:	48 8b 02             	mov    rax,QWORD PTR [rdx]
  52:	48 89 01             	mov    QWORD PTR [rcx],rax
  55:	48 89 c8             	mov    rax,rcx
  58:	48 83 c4 28          	add    rsp,0x28
  5c:	c3                   	ret
  5d:	90                   	nop
  5e:	90                   	nop
  5f:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <grab(WithEsft*) [clone .cold]>:
   0:	b9 08 00 00 00       	mov    ecx,0x8
   5:	e8 00 00 00 00       	call   a <grab(WithEsft*) [clone .cold]+0xa>
   a:	4c 8d 05 00 00 00 00 	lea    r8,[rip+0x0]        # 11 <grab(WithEsft*) [clone .cold]+0x11>
  11:	48 8d 15 00 00 00 00 	lea    rdx,[rip+0x0]        # 18 <grab(WithEsft*) [clone .cold]+0x18>
  18:	48 89 c1             	mov    rcx,rax
  1b:	48 8b 05 00 00 00 00 	mov    rax,QWORD PTR [rip+0x0]        # 22 <grab(WithEsft*) [clone .cold]+0x22>
  22:	48 83 c0 10          	add    rax,0x10
  26:	48 89 01             	mov    QWORD PTR [rcx],rax
  29:	e8 00 00 00 00       	call   2e <grab(WithEsft*) [clone .cold]+0x2e>
  2e:	90                   	nop
  2f:	90                   	nop
