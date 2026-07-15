
ch81_sso_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <__tcf_ZZ10short_cstrvE1s>:
   0:	48 8b 0d 00 00 00 00 	mov    rcx,QWORD PTR [rip+0x0]        # 7 <__tcf_ZZ10short_cstrvE1s+0x7>
   7:	48 8d 05 10 00 00 00 	lea    rax,[rip+0x10]        # 1e <__tcf_ZZ10short_cstrvE1s+0x1e>
   e:	48 39 c1             	cmp    rcx,rax
  11:	74 15                	je     28 <__tcf_ZZ10short_cstrvE1s+0x28>
  13:	48 8b 05 10 00 00 00 	mov    rax,QWORD PTR [rip+0x10]        # 2a <__tcf_ZZ10short_cstrvE1s+0x2a>
  1a:	48 8d 50 01          	lea    rdx,[rax+0x1]
  1e:	e9 00 00 00 00       	jmp    23 <__tcf_ZZ10short_cstrvE1s+0x23>
  23:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
  28:	c3                   	ret
  29:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000000030 <__tcf_ZZ9long_cstrvE1s>:
  30:	48 8b 0d 20 00 00 00 	mov    rcx,QWORD PTR [rip+0x20]        # 57 <__tcf_ZZ9long_cstrvE1s+0x27>
  37:	48 8d 05 30 00 00 00 	lea    rax,[rip+0x30]        # 6e <make_short()+0xe>
  3e:	48 39 c1             	cmp    rcx,rax
  41:	74 15                	je     58 <__tcf_ZZ9long_cstrvE1s+0x28>
  43:	48 8b 05 30 00 00 00 	mov    rax,QWORD PTR [rip+0x30]        # 7a <make_short()+0x1a>
  4a:	48 8d 50 01          	lea    rdx,[rax+0x1]
  4e:	e9 00 00 00 00       	jmp    53 <__tcf_ZZ9long_cstrvE1s+0x23>
  53:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
  58:	c3                   	ret
  59:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000000060 <make_short()>:
  60:	48 83 ec 28          	sub    rsp,0x28
  64:	c7 05 fc ff ff ff 02 	mov    DWORD PTR [rip+0xfffffffffffffffc],0x2        # 6a <make_short()+0xa>
  6b:	00 00 00 
  6e:	48 8d 44 24 10       	lea    rax,[rsp+0x10]
  73:	89 05 00 00 00 00    	mov    DWORD PTR [rip+0x0],eax        # 79 <make_short()+0x19>
  79:	48 83 c4 28          	add    rsp,0x28
  7d:	c3                   	ret
  7e:	66 90                	xchg   ax,ax

0000000000000080 <make_long()>:
  80:	48 83 ec 28          	sub    rsp,0x28
  84:	b9 4d 00 00 00       	mov    ecx,0x4d
  89:	e8 00 00 00 00       	call   8e <make_long()+0xe>
  8e:	48 ba 69 6e 67 20 69 	movabs rdx,0x6420736920676e69
  95:	73 20 64 
  98:	c7 05 fc ff ff ff 4c 	mov    DWORD PTR [rip+0xfffffffffffffffc],0x4c        # 9e <make_long()+0x1e>
  9f:	00 00 00 
  a2:	48 89 c1             	mov    rcx,rax
  a5:	48 b8 74 68 69 73 20 	movabs rax,0x7274732073696874
  ac:	73 74 72 
  af:	48 89 51 08          	mov    QWORD PTR [rcx+0x8],rdx
  b3:	48 ba 79 20 6c 6f 6e 	movabs rdx,0x7265676e6f6c2079
  ba:	67 65 72 
  bd:	48 89 01             	mov    QWORD PTR [rcx],rax
  c0:	48 b8 65 66 69 6e 69 	movabs rax,0x6c6574696e696665
  c7:	74 65 6c 
  ca:	48 89 51 18          	mov    QWORD PTR [rcx+0x18],rdx
  ce:	48 ba 65 20 53 53 4f 	movabs rdx,0x7562204f53532065
  d5:	20 62 75 
  d8:	48 89 41 10          	mov    QWORD PTR [rcx+0x10],rax
  dc:	48 b8 20 74 68 61 6e 	movabs rax,0x6874206e61687420
  e3:	20 74 68 
  e6:	48 89 51 28          	mov    QWORD PTR [rcx+0x28],rdx
  ea:	48 ba 20 6d 75 73 74 	movabs rdx,0x6f67207473756d20
  f1:	20 67 6f 
  f4:	48 89 51 38          	mov    QWORD PTR [rcx+0x38],rdx
  f8:	48 ba 74 68 65 20 68 	movabs rdx,0x7061656820656874
  ff:	65 61 70 
 102:	48 89 41 20          	mov    QWORD PTR [rcx+0x20],rax
 106:	48 b8 66 66 65 72 20 	movabs rax,0x646e612072656666
 10d:	61 6e 64 
 110:	48 89 41 30          	mov    QWORD PTR [rcx+0x30],rax
 114:	48 b8 74 20 67 6f 20 	movabs rax,0x206f74206f672074
 11b:	74 6f 20 
 11e:	48 89 51 44          	mov    QWORD PTR [rcx+0x44],rdx
 122:	ba 4d 00 00 00       	mov    edx,0x4d
 127:	48 89 41 3c          	mov    QWORD PTR [rcx+0x3c],rax
 12b:	c6 41 4c 00          	mov    BYTE PTR [rcx+0x4c],0x0
 12f:	89 0d 00 00 00 00    	mov    DWORD PTR [rip+0x0],ecx        # 135 <make_long()+0xb5>
 135:	48 83 c4 28          	add    rsp,0x28
 139:	e9 00 00 00 00       	jmp    13e <make_long()+0xbe>
 13e:	66 90                	xchg   ax,ax

0000000000000140 <short_cstr()>:
 140:	48 83 ec 28          	sub    rsp,0x28
 144:	0f b6 05 40 00 00 00 	movzx  eax,BYTE PTR [rip+0x40]        # 18b <short_cstr()+0x4b>
 14b:	84 c0                	test   al,al
 14d:	74 11                	je     160 <short_cstr()+0x20>
 14f:	48 8b 05 00 00 00 00 	mov    rax,QWORD PTR [rip+0x0]        # 156 <short_cstr()+0x16>
 156:	48 83 c4 28          	add    rsp,0x28
 15a:	c3                   	ret
 15b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
 160:	48 8d 0d 40 00 00 00 	lea    rcx,[rip+0x40]        # 1a7 <long_cstr()+0x7>
 167:	e8 00 00 00 00       	call   16c <short_cstr()+0x2c>
 16c:	85 c0                	test   eax,eax
 16e:	74 df                	je     14f <short_cstr()+0xf>
 170:	48 8d 0d 89 fe ff ff 	lea    rcx,[rip+0xfffffffffffffe89]        # 0 <__tcf_ZZ10short_cstrvE1s>
 177:	e8 00 00 00 00       	call   17c <short_cstr()+0x3c>
 17c:	48 8d 0d 40 00 00 00 	lea    rcx,[rip+0x40]        # 1c3 <long_cstr()+0x23>
 183:	e8 00 00 00 00       	call   188 <short_cstr()+0x48>
 188:	48 8b 05 00 00 00 00 	mov    rax,QWORD PTR [rip+0x0]        # 18f <short_cstr()+0x4f>
 18f:	48 83 c4 28          	add    rsp,0x28
 193:	c3                   	ret
 194:	90                   	nop
 195:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 19c:	00 00 00 00 

00000000000001a0 <long_cstr()>:
 1a0:	53                   	push   rbx
 1a1:	48 83 ec 20          	sub    rsp,0x20
 1a5:	0f b6 05 08 00 00 00 	movzx  eax,BYTE PTR [rip+0x8]        # 1b4 <long_cstr()+0x14>
 1ac:	84 c0                	test   al,al
 1ae:	74 10                	je     1c0 <long_cstr()+0x20>
 1b0:	48 8b 05 20 00 00 00 	mov    rax,QWORD PTR [rip+0x20]        # 1d7 <long_cstr()+0x37>
 1b7:	48 83 c4 20          	add    rsp,0x20
 1bb:	5b                   	pop    rbx
 1bc:	c3                   	ret
 1bd:	0f 1f 00             	nop    DWORD PTR [rax]
 1c0:	48 8d 0d 08 00 00 00 	lea    rcx,[rip+0x8]        # 1cf <long_cstr()+0x2f>
 1c7:	e8 00 00 00 00       	call   1cc <long_cstr()+0x2c>
 1cc:	85 c0                	test   eax,eax
 1ce:	74 e0                	je     1b0 <long_cstr()+0x10>
 1d0:	48 8d 05 30 00 00 00 	lea    rax,[rip+0x30]        # 207 <long_cstr()+0x67>
 1d7:	b9 4f 00 00 00       	mov    ecx,0x4f
 1dc:	48 89 05 20 00 00 00 	mov    QWORD PTR [rip+0x20],rax        # 203 <long_cstr()+0x63>
 1e3:	e8 00 00 00 00       	call   1e8 <long_cstr()+0x48>
 1e8:	48 ba 61 20 73 74 72 	movabs rdx,0x676e697274732061
 1ef:	69 6e 67 
 1f2:	c6 40 4e 00          	mov    BYTE PTR [rax+0x4e],0x0
 1f6:	48 b9 20 66 61 72 20 	movabs rcx,0x6378652072616620
 1fd:	65 78 63 
 200:	48 89 10             	mov    QWORD PTR [rax],rdx
 203:	48 ba 65 65 64 69 6e 	movabs rdx,0x7420676e69646565
 20a:	67 20 74 
 20d:	48 89 48 08          	mov    QWORD PTR [rax+0x8],rcx
 211:	48 b9 68 65 20 66 69 	movabs rcx,0x6574666966206568
 218:	66 74 65 
 21b:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
 21f:	48 ba 65 6e 2d 62 79 	movabs rdx,0x20657479622d6e65
 226:	74 65 20 
 229:	48 89 48 18          	mov    QWORD PTR [rax+0x18],rcx
 22d:	48 b9 73 6d 61 6c 6c 	movabs rcx,0x7473206c6c616d73
 234:	20 73 74 
 237:	48 89 50 20          	mov    QWORD PTR [rax+0x20],rdx
 23b:	48 ba 72 69 6e 67 20 	movabs rdx,0x74706f20676e6972
 242:	6f 70 74 
 245:	48 89 48 28          	mov    QWORD PTR [rax+0x28],rcx
 249:	48 b9 69 6d 69 7a 61 	movabs rcx,0x6f6974617a696d69
 250:	74 69 6f 
 253:	48 89 48 38          	mov    QWORD PTR [rax+0x38],rcx
 257:	48 b9 65 72 20 78 78 	movabs rcx,0x7878787878207265
 25e:	78 78 78 
 261:	48 89 50 30          	mov    QWORD PTR [rax+0x30],rdx
 265:	48 ba 69 6f 6e 20 62 	movabs rdx,0x66667562206e6f69
 26c:	75 66 66 
 26f:	48 89 50 3e          	mov    QWORD PTR [rax+0x3e],rdx
 273:	48 89 48 46          	mov    QWORD PTR [rax+0x46],rcx
 277:	48 8d 0d b2 fd ff ff 	lea    rcx,[rip+0xfffffffffffffdb2]        # 30 <__tcf_ZZ9long_cstrvE1s>
 27e:	48 89 05 20 00 00 00 	mov    QWORD PTR [rip+0x20],rax        # 2a5 <long_cstr()+0x105>
 285:	48 c7 05 2c 00 00 00 	mov    QWORD PTR [rip+0x2c],0x4e        # 2bc <long_cstr()+0x11c>
 28c:	4e 00 00 00 
 290:	48 c7 05 24 00 00 00 	mov    QWORD PTR [rip+0x24],0x4e        # 2bf <long_cstr()+0x11f>
 297:	4e 00 00 00 
 29b:	e8 00 00 00 00       	call   2a0 <long_cstr()+0x100>
 2a0:	48 8d 0d 08 00 00 00 	lea    rcx,[rip+0x8]        # 2af <long_cstr()+0x10f>
 2a7:	e8 00 00 00 00       	call   2ac <long_cstr()+0x10c>
 2ac:	48 8b 05 20 00 00 00 	mov    rax,QWORD PTR [rip+0x20]        # 2d3 <long_cstr()+0x133>
 2b3:	48 83 c4 20          	add    rsp,0x20
 2b7:	5b                   	pop    rbx
 2b8:	c3                   	ret
 2b9:	48 89 c3             	mov    rbx,rax
 2bc:	e9 00 00 00 00       	jmp    2c1 <long_cstr()+0x121>
 2c1:	90                   	nop
 2c2:	90                   	nop
 2c3:	90                   	nop
 2c4:	90                   	nop
 2c5:	90                   	nop
 2c6:	90                   	nop
 2c7:	90                   	nop
 2c8:	90                   	nop
 2c9:	90                   	nop
 2ca:	90                   	nop
 2cb:	90                   	nop
 2cc:	90                   	nop
 2cd:	90                   	nop
 2ce:	90                   	nop
 2cf:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <long_cstr() [clone .cold]>:
   0:	48 8d 0d 08 00 00 00 	lea    rcx,[rip+0x8]        # f <long_cstr() [clone .cold]+0xf>
   7:	e8 00 00 00 00       	call   c <long_cstr() [clone .cold]+0xc>
   c:	48 89 d9             	mov    rcx,rbx
   f:	e8 00 00 00 00       	call   14 <long_cstr() [clone .cold]+0x14>
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
   0:	48 83 ec 28          	sub    rsp,0x28
   4:	e8 00 00 00 00       	call   9 <main+0x9>
   9:	e8 60 00 00 00       	call   6e <make_short()+0xe>
   e:	e8 80 00 00 00       	call   93 <make_long()+0x13>
  13:	e8 40 01 00 00       	call   158 <short_cstr()+0x18>
  18:	e8 a0 01 00 00       	call   1bd <long_cstr()+0x1d>
  1d:	31 c0                	xor    eax,eax
  1f:	48 83 c4 28          	add    rsp,0x28
  23:	c3                   	ret
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
