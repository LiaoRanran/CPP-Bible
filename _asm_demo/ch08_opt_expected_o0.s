
ch08_opt_expected_o0.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <parse_digit(char)>:
   0:	55                   	push   rbp
   1:	48 89 e5             	mov    rbp,rsp
   4:	48 83 ec 40          	sub    rsp,0x40
   8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   c:	89 d0                	mov    eax,edx
   e:	88 45 18             	mov    BYTE PTR [rbp+0x18],al
  11:	80 7d 18 2f          	cmp    BYTE PTR [rbp+0x18],0x2f
  15:	7e 22                	jle    39 <parse_digit(char)+0x39>
  17:	80 7d 18 39          	cmp    BYTE PTR [rbp+0x18],0x39
  1b:	7f 1c                	jg     39 <parse_digit(char)+0x39>
  1d:	0f be 45 18          	movsx  eax,BYTE PTR [rbp+0x18]
  21:	83 e8 30             	sub    eax,0x30
  24:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
  27:	48 8d 55 ec          	lea    rdx,[rbp-0x14]
  2b:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  2f:	48 89 c1             	mov    rcx,rax
  32:	e8 00 00 00 00       	call   37 <parse_digit(char)+0x37>
  37:	eb 73                	jmp    ac <parse_digit(char)+0xac>
  39:	80 7d 18 60          	cmp    BYTE PTR [rbp+0x18],0x60
  3d:	7e 22                	jle    61 <parse_digit(char)+0x61>
  3f:	80 7d 18 66          	cmp    BYTE PTR [rbp+0x18],0x66
  43:	7f 1c                	jg     61 <parse_digit(char)+0x61>
  45:	0f be 45 18          	movsx  eax,BYTE PTR [rbp+0x18]
  49:	83 e8 57             	sub    eax,0x57
  4c:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
  4f:	48 8d 55 f0          	lea    rdx,[rbp-0x10]
  53:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  57:	48 89 c1             	mov    rcx,rax
  5a:	e8 00 00 00 00       	call   5f <parse_digit(char)+0x5f>
  5f:	eb 4b                	jmp    ac <parse_digit(char)+0xac>
  61:	80 7d 18 40          	cmp    BYTE PTR [rbp+0x18],0x40
  65:	7e 22                	jle    89 <parse_digit(char)+0x89>
  67:	80 7d 18 46          	cmp    BYTE PTR [rbp+0x18],0x46
  6b:	7f 1c                	jg     89 <parse_digit(char)+0x89>
  6d:	0f be 45 18          	movsx  eax,BYTE PTR [rbp+0x18]
  71:	83 e8 37             	sub    eax,0x37
  74:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
  77:	48 8d 55 f4          	lea    rdx,[rbp-0xc]
  7b:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  7f:	48 89 c1             	mov    rcx,rax
  82:	e8 00 00 00 00       	call   87 <parse_digit(char)+0x87>
  87:	eb 23                	jmp    ac <parse_digit(char)+0xac>
  89:	48 8d 15 00 00 00 00 	lea    rdx,[rip+0x0]        # 90 <parse_digit(char)+0x90>
  90:	48 8d 45 f8          	lea    rax,[rbp-0x8]
  94:	48 89 c1             	mov    rcx,rax
  97:	e8 00 00 00 00       	call   9c <parse_digit(char)+0x9c>
  9c:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
  a0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  a4:	48 89 c1             	mov    rcx,rax
  a7:	e8 00 00 00 00       	call   ac <parse_digit(char)+0xac>
  ac:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  b0:	48 83 c4 40          	add    rsp,0x40
  b4:	5d                   	pop    rbp
  b5:	c3                   	ret

00000000000000b6 <use(char)>:
  b6:	55                   	push   rbp
  b7:	48 89 e5             	mov    rbp,rsp
  ba:	48 83 ec 40          	sub    rsp,0x40
  be:	89 c8                	mov    eax,ecx
  c0:	88 45 10             	mov    BYTE PTR [rbp+0x10],al
  c3:	0f be 55 10          	movsx  edx,BYTE PTR [rbp+0x10]
  c7:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  cb:	48 89 c1             	mov    rcx,rax
  ce:	e8 2d ff ff ff       	call   0 <parse_digit(char)>
  d3:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
  da:	48 8d 55 fc          	lea    rdx,[rbp-0x4]
  de:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  e2:	48 89 c1             	mov    rcx,rax
  e5:	e8 00 00 00 00       	call   ea <use(char)+0x34>
  ea:	48 83 c4 40          	add    rsp,0x40
  ee:	5d                   	pop    rbp
  ef:	c3                   	ret

00000000000000f0 <main>:
  f0:	55                   	push   rbp
  f1:	48 89 e5             	mov    rbp,rsp
  f4:	48 83 ec 20          	sub    rsp,0x20
  f8:	e8 00 00 00 00       	call   fd <main+0xd>
  fd:	b9 41 00 00 00       	mov    ecx,0x41
 102:	e8 af ff ff ff       	call   b6 <use(char)>
 107:	90                   	nop
 108:	48 83 c4 20          	add    rsp,0x20
 10c:	5d                   	pop    rbp
 10d:	c3                   	ret
 10e:	90                   	nop
 10f:	90                   	nop

Disassembly of section .text$_ZNSt8expectedIiPKcEC1IiEEOT_:

0000000000000000 <std::expected<int, char const*>::expected<int>(int&&)>:
   0:	55                   	push   rbp
   1:	48 89 e5             	mov    rbp,rsp
   4:	48 83 ec 10          	sub    rsp,0x10
   8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
  10:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
  14:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  18:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
  1c:	8b 10                	mov    edx,DWORD PTR [rax]
  1e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  22:	89 10                	mov    DWORD PTR [rax],edx
  24:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  28:	c6 40 08 01          	mov    BYTE PTR [rax+0x8],0x1
  2c:	90                   	nop
  2d:	48 83 c4 10          	add    rsp,0x10
  31:	5d                   	pop    rbp
  32:	c3                   	ret
  33:	90                   	nop
  34:	90                   	nop
  35:	90                   	nop
  36:	90                   	nop
  37:	90                   	nop
  38:	90                   	nop
  39:	90                   	nop
  3a:	90                   	nop
  3b:	90                   	nop
  3c:	90                   	nop
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop

Disassembly of section .text$_ZNSt10unexpectedIPKcEC1IRA16_S0_EEOT_:

0000000000000000 <std::unexpected<char const*>::unexpected<char const (&) [16]>(char const (&) [16])>:
   0:	55                   	push   rbp
   1:	48 89 e5             	mov    rbp,rsp
   4:	48 83 ec 10          	sub    rsp,0x10
   8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
  10:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
  14:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  18:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
  1c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  20:	48 89 10             	mov    QWORD PTR [rax],rdx
  23:	90                   	nop
  24:	48 83 c4 10          	add    rsp,0x10
  28:	5d                   	pop    rbp
  29:	c3                   	ret
  2a:	90                   	nop
  2b:	90                   	nop
  2c:	90                   	nop
  2d:	90                   	nop
  2e:	90                   	nop
  2f:	90                   	nop

Disassembly of section .text$_ZNSt8expectedIiPKcEC1IS1_EEOSt10unexpectedIT_E:

0000000000000000 <std::expected<int, char const*>::expected<char const*>(std::unexpected<char const*>&&)>:
   0:	55                   	push   rbp
   1:	48 89 e5             	mov    rbp,rsp
   4:	48 83 ec 30          	sub    rsp,0x30
   8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
  10:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
  14:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  18:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
  1c:	48 89 c1             	mov    rcx,rax
  1f:	e8 00 00 00 00       	call   24 <std::expected<int, char const*>::expected<char const*>(std::unexpected<char const*>&&)+0x24>
  24:	48 8b 10             	mov    rdx,QWORD PTR [rax]
  27:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  2b:	48 89 10             	mov    QWORD PTR [rax],rdx
  2e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  32:	c6 40 08 00          	mov    BYTE PTR [rax+0x8],0x0
  36:	90                   	nop
  37:	48 83 c4 30          	add    rsp,0x30
  3b:	5d                   	pop    rbp
  3c:	c3                   	ret
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop

Disassembly of section .text$_ZNKRSt8expectedIiPKcE8value_orIiEEiOT_:

0000000000000000 <int std::expected<int, char const*>::value_or<int>(int&&) const &>:
   0:	55                   	push   rbp
   1:	48 89 e5             	mov    rbp,rsp
   4:	48 83 ec 10          	sub    rsp,0x10
   8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
  10:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  14:	0f b6 40 08          	movzx  eax,BYTE PTR [rax+0x8]
  18:	84 c0                	test   al,al
  1a:	74 08                	je     24 <int std::expected<int, char const*>::value_or<int>(int&&) const &+0x24>
  1c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  20:	8b 00                	mov    eax,DWORD PTR [rax]
  22:	eb 0e                	jmp    32 <int std::expected<int, char const*>::value_or<int>(int&&) const &+0x32>
  24:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
  28:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  2c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
  30:	8b 00                	mov    eax,DWORD PTR [rax]
  32:	48 83 c4 10          	add    rsp,0x10
  36:	5d                   	pop    rbp
  37:	c3                   	ret
  38:	90                   	nop
  39:	90                   	nop
  3a:	90                   	nop
  3b:	90                   	nop
  3c:	90                   	nop
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop

Disassembly of section .text$_ZNOSt10unexpectedIPKcE5errorEv:

0000000000000000 <std::unexpected<char const*>::error() &&>:
   0:	55                   	push   rbp
   1:	48 89 e5             	mov    rbp,rsp
   4:	48 83 ec 10          	sub    rsp,0x10
   8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
  10:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  14:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
  18:	48 83 c4 10          	add    rsp,0x10
  1c:	5d                   	pop    rbp
  1d:	c3                   	ret
  1e:	90                   	nop
  1f:	90                   	nop
