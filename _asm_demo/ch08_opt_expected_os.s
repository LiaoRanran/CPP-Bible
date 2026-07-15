
ch08_opt_expected_os.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <parse_digit(char)>:
   0:	48 89 c8             	mov    rax,rcx
   3:	8d 4a d0             	lea    ecx,[rdx-0x30]
   6:	80 f9 09             	cmp    cl,0x9
   9:	77 08                	ja     13 <parse_digit(char)+0x13>
   b:	0f be d2             	movsx  edx,dl
   e:	83 ea 30             	sub    edx,0x30
  11:	eb 1e                	jmp    31 <parse_digit(char)+0x31>
  13:	8d 4a 9f             	lea    ecx,[rdx-0x61]
  16:	80 f9 05             	cmp    cl,0x5
  19:	77 08                	ja     23 <parse_digit(char)+0x23>
  1b:	0f be d2             	movsx  edx,dl
  1e:	83 ea 57             	sub    edx,0x57
  21:	eb 0e                	jmp    31 <parse_digit(char)+0x31>
  23:	8d 4a bf             	lea    ecx,[rdx-0x41]
  26:	80 f9 05             	cmp    cl,0x5
  29:	77 0e                	ja     39 <parse_digit(char)+0x39>
  2b:	0f be d2             	movsx  edx,dl
  2e:	83 ea 37             	sub    edx,0x37
  31:	89 10                	mov    DWORD PTR [rax],edx
  33:	c6 40 08 01          	mov    BYTE PTR [rax+0x8],0x1
  37:	eb 10                	jmp    49 <parse_digit(char)+0x49>
  39:	31 d2                	xor    edx,edx
  3b:	48 8d 0d 00 00 00 00 	lea    rcx,[rip+0x0]        # 42 <parse_digit(char)+0x42>
  42:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  46:	48 89 08             	mov    QWORD PTR [rax],rcx
  49:	c3                   	ret

000000000000004a <use(char)>:
  4a:	48 83 ec 38          	sub    rsp,0x38
  4e:	0f be d1             	movsx  edx,cl
  51:	48 8d 4c 24 20       	lea    rcx,[rsp+0x20]
  56:	e8 a5 ff ff ff       	call   0 <parse_digit(char)>
  5b:	80 7c 24 28 00       	cmp    BYTE PTR [rsp+0x28],0x0
  60:	b8 ff ff ff ff       	mov    eax,0xffffffff
  65:	0f 45 44 24 20       	cmovne eax,DWORD PTR [rsp+0x20]
  6a:	48 83 c4 38          	add    rsp,0x38
  6e:	c3                   	ret
  6f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	48 83 ec 28          	sub    rsp,0x28
   4:	e8 00 00 00 00       	call   9 <main+0x9>
   9:	b9 41 00 00 00       	mov    ecx,0x41
   e:	48 83 c4 28          	add    rsp,0x28
  12:	e9 4a 00 00 00       	jmp    61 <use(char)+0x17>
  17:	90                   	nop
  18:	90                   	nop
  19:	90                   	nop
  1a:	90                   	nop
  1b:	90                   	nop
  1c:	90                   	nop
  1d:	90                   	nop
  1e:	90                   	nop
  1f:	90                   	nop
