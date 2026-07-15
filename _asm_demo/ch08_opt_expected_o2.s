
ch08_opt_expected_o2.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <parse_digit(char)>:
   0:	48 89 c8             	mov    rax,rcx
   3:	8d 4a d0             	lea    ecx,[rdx-0x30]
   6:	80 f9 09             	cmp    cl,0x9
   9:	77 15                	ja     20 <parse_digit(char)+0x20>
   b:	0f be d2             	movsx  edx,dl
   e:	c6 40 08 01          	mov    BYTE PTR [rax+0x8],0x1
  12:	83 ea 30             	sub    edx,0x30
  15:	89 10                	mov    DWORD PTR [rax],edx
  17:	c3                   	ret
  18:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
  1f:	00 
  20:	8d 4a 9f             	lea    ecx,[rdx-0x61]
  23:	80 f9 05             	cmp    cl,0x5
  26:	77 10                	ja     38 <parse_digit(char)+0x38>
  28:	0f be d2             	movsx  edx,dl
  2b:	c6 40 08 01          	mov    BYTE PTR [rax+0x8],0x1
  2f:	83 ea 57             	sub    edx,0x57
  32:	89 10                	mov    DWORD PTR [rax],edx
  34:	c3                   	ret
  35:	0f 1f 00             	nop    DWORD PTR [rax]
  38:	8d 4a bf             	lea    ecx,[rdx-0x41]
  3b:	80 f9 05             	cmp    cl,0x5
  3e:	77 10                	ja     50 <parse_digit(char)+0x50>
  40:	0f be d2             	movsx  edx,dl
  43:	c6 40 08 01          	mov    BYTE PTR [rax+0x8],0x1
  47:	83 ea 37             	sub    edx,0x37
  4a:	89 10                	mov    DWORD PTR [rax],edx
  4c:	c3                   	ret
  4d:	0f 1f 00             	nop    DWORD PTR [rax]
  50:	48 8d 0d 00 00 00 00 	lea    rcx,[rip+0x0]        # 57 <parse_digit(char)+0x57>
  57:	48 c7 40 08 00 00 00 	mov    QWORD PTR [rax+0x8],0x0
  5e:	00 
  5f:	48 89 08             	mov    QWORD PTR [rax],rcx
  62:	c3                   	ret
  63:	66 90                	xchg   ax,ax
  65:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  6c:	00 00 00 00 

0000000000000070 <use(char)>:
  70:	48 83 ec 38          	sub    rsp,0x38
  74:	0f be d1             	movsx  edx,cl
  77:	48 8d 4c 24 20       	lea    rcx,[rsp+0x20]
  7c:	e8 7f ff ff ff       	call   0 <parse_digit(char)>
  81:	80 7c 24 28 00       	cmp    BYTE PTR [rsp+0x28],0x0
  86:	b8 ff ff ff ff       	mov    eax,0xffffffff
  8b:	0f 45 44 24 20       	cmovne eax,DWORD PTR [rsp+0x20]
  90:	48 83 c4 38          	add    rsp,0x38
  94:	c3                   	ret
  95:	90                   	nop
  96:	90                   	nop
  97:	90                   	nop
  98:	90                   	nop
  99:	90                   	nop
  9a:	90                   	nop
  9b:	90                   	nop
  9c:	90                   	nop
  9d:	90                   	nop
  9e:	90                   	nop
  9f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	48 83 ec 28          	sub    rsp,0x28
   4:	e8 00 00 00 00       	call   9 <main+0x9>
   9:	b9 41 00 00 00       	mov    ecx,0x41
   e:	48 83 c4 28          	add    rsp,0x28
  12:	e9 70 00 00 00       	jmp    87 <use(char)+0x17>
  17:	90                   	nop
  18:	90                   	nop
  19:	90                   	nop
  1a:	90                   	nop
  1b:	90                   	nop
  1c:	90                   	nop
  1d:	90                   	nop
  1e:	90                   	nop
  1f:	90                   	nop
