
_ch156_pgo.o:     file format pe-x86-64


Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	b8 68 20 00 00       	mov    eax,0x2068
   5:	e8 00 00 00 00       	call   a <main+0xa>
   a:	48 29 c4             	sub    rsp,rax
   d:	0f 29 b4 24 20 20 00 	movaps XMMWORD PTR [rsp+0x2020],xmm6
  14:	00 
  15:	0f 29 bc 24 30 20 00 	movaps XMMWORD PTR [rsp+0x2030],xmm7
  1c:	00 
  1d:	44 0f 29 84 24 40 20 	movaps XMMWORD PTR [rsp+0x2040],xmm8
  24:	00 00 
  26:	44 0f 29 8c 24 50 20 	movaps XMMWORD PTR [rsp+0x2050],xmm9
  2d:	00 00 
  2f:	e8 00 00 00 00       	call   34 <main+0x34>
  34:	66 0f ef db          	pxor   xmm3,xmm3
  38:	66 0f 6f 15 20 00 00 	movdqa xmm2,XMMWORD PTR [rip+0x20]        # 60 <main+0x60>
  3f:	00 
  40:	66 0f 6f eb          	movdqa xmm5,xmm3
  44:	48 8d 4c 24 20       	lea    rcx,[rsp+0x20]
  49:	66 0f 6f 25 00 00 00 	movdqa xmm4,XMMWORD PTR [rip+0x0]        # 51 <main+0x51>
  50:	00 
  51:	66 0f 66 ea          	pcmpgtd xmm5,xmm2
  55:	66 0f 6f 35 10 00 00 	movdqa xmm6,XMMWORD PTR [rip+0x10]        # 6d <main+0x6d>
  5c:	00 
  5d:	48 89 c8             	mov    rax,rcx
  60:	48 8d 94 24 20 20 00 	lea    rdx,[rsp+0x2020]
  67:	00 
  68:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
  6f:	00 
  70:	66 0f 6f fc          	movdqa xmm7,xmm4
  74:	66 0f 6f c3          	movdqa xmm0,xmm3
  78:	66 44 0f 6f c5       	movdqa xmm8,xmm5
  7d:	66 0f 66 c7          	pcmpgtd xmm0,xmm7
  81:	66 0f 6f cf          	movdqa xmm1,xmm7
  85:	66 44 0f 6f cd       	movdqa xmm9,xmm5
  8a:	66 44 0f f4 c7       	pmuludq xmm8,xmm7
  8f:	48 83 c0 10          	add    rax,0x10
  93:	66 0f fe e6          	paddd  xmm4,xmm6
  97:	66 0f f4 ca          	pmuludq xmm1,xmm2
  9b:	66 0f f4 c2          	pmuludq xmm0,xmm2
  9f:	66 41 0f d4 c0       	paddq  xmm0,xmm8
  a4:	66 44 0f 6f c3       	movdqa xmm8,xmm3
  a9:	66 0f 73 f0 20       	psllq  xmm0,0x20
  ae:	66 0f d4 c8          	paddq  xmm1,xmm0
  b2:	66 0f 6f c7          	movdqa xmm0,xmm7
  b6:	66 0f 73 d0 20       	psrlq  xmm0,0x20
  bb:	66 44 0f 66 c0       	pcmpgtd xmm8,xmm0
  c0:	66 44 0f f4 c8       	pmuludq xmm9,xmm0
  c5:	66 0f f4 c2          	pmuludq xmm0,xmm2
  c9:	66 44 0f f4 c2       	pmuludq xmm8,xmm2
  ce:	66 45 0f d4 c1       	paddq  xmm8,xmm9
  d3:	66 41 0f 73 f0 20    	psllq  xmm8,0x20
  d9:	66 41 0f d4 c0       	paddq  xmm0,xmm8
  de:	0f c6 c8 dd          	shufps xmm1,xmm0,0xdd
  e2:	66 0f 70 c9 d8       	pshufd xmm1,xmm1,0xd8
  e7:	66 0f 72 e1 03       	psrad  xmm1,0x3
  ec:	66 0f 6f c1          	movdqa xmm0,xmm1
  f0:	66 0f 72 f0 01       	pslld  xmm0,0x1
  f5:	66 0f fe c1          	paddd  xmm0,xmm1
  f9:	66 0f 72 f0 05       	pslld  xmm0,0x5
  fe:	66 0f fe c1          	paddd  xmm0,xmm1
 102:	66 0f 6f cb          	movdqa xmm1,xmm3
 106:	66 0f 76 c7          	pcmpeqd xmm0,xmm7
 10a:	66 0f fa cf          	psubd  xmm1,xmm7
 10e:	66 0f db c8          	pand   xmm1,xmm0
 112:	66 0f df c7          	pandn  xmm0,xmm7
 116:	66 0f eb c1          	por    xmm0,xmm1
 11a:	0f 29 40 f0          	movaps XMMWORD PTR [rax-0x10],xmm0
 11e:	48 39 d0             	cmp    rax,rdx
 121:	0f 85 49 ff ff ff    	jne    70 <main+0x70>
 127:	ba 00 08 00 00       	mov    edx,0x800
 12c:	e8 00 00 00 00       	call   131 <main+0x131>
 131:	90                   	nop
 132:	0f 28 b4 24 20 20 00 	movaps xmm6,XMMWORD PTR [rsp+0x2020]
 139:	00 
 13a:	0f 28 bc 24 30 20 00 	movaps xmm7,XMMWORD PTR [rsp+0x2030]
 141:	00 
 142:	44 0f 28 84 24 40 20 	movaps xmm8,XMMWORD PTR [rsp+0x2040]
 149:	00 00 
 14b:	44 0f 28 8c 24 50 20 	movaps xmm9,XMMWORD PTR [rsp+0x2050]
 152:	00 00 
 154:	48 81 c4 68 20 00 00 	add    rsp,0x2068
 15b:	c3                   	ret
 15c:	90                   	nop
 15d:	90                   	nop
 15e:	90                   	nop
 15f:	90                   	nop

Disassembly of section .text.hot:

0000000000000000 <_Z7processPKii>:
   0:	85 d2                	test   edx,edx
   2:	48 89 c8             	mov    rax,rcx
   5:	7e 39                	jle    40 <_Z7processPKii+0x40>
   7:	48 63 d2             	movsxd rdx,edx
   a:	4c 8d 04 91          	lea    r8,[rcx+rdx*4]
   e:	31 c9                	xor    ecx,ecx
  10:	eb 11                	jmp    23 <_Z7processPKii+0x23>
  12:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
  18:	48 83 c0 04          	add    rax,0x4
  1c:	01 d1                	add    ecx,edx
  1e:	49 39 c0             	cmp    r8,rax
  21:	74 1a                	je     3d <_Z7processPKii+0x3d>
  23:	8b 10                	mov    edx,DWORD PTR [rax]
  25:	85 d2                	test   edx,edx
  27:	79 ef                	jns    18 <_Z7processPKii+0x18>
  29:	c1 e2 06             	shl    edx,0x6
  2c:	48 83 c0 04          	add    rax,0x4
  30:	01 15 00 00 00 00    	add    DWORD PTR [rip+0x0],edx        # 36 <_Z7processPKii+0x36>
  36:	01 d1                	add    ecx,edx
  38:	49 39 c0             	cmp    r8,rax
  3b:	75 e6                	jne    23 <_Z7processPKii+0x23>
  3d:	89 c8                	mov    eax,ecx
  3f:	c3                   	ret
  40:	31 c9                	xor    ecx,ecx
  42:	eb f9                	jmp    3d <_Z7processPKii+0x3d>
  44:	90                   	nop
  45:	90                   	nop
  46:	90                   	nop
  47:	90                   	nop
  48:	90                   	nop
  49:	90                   	nop
  4a:	90                   	nop
  4b:	90                   	nop
  4c:	90                   	nop
  4d:	90                   	nop
  4e:	90                   	nop
  4f:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <_Z4coldi>:
   0:	89 c8                	mov    eax,ecx
   2:	c1 e0 06             	shl    eax,0x6
   5:	01 05 00 00 00 00    	add    DWORD PTR [rip+0x0],eax        # b <_Z4coldi+0xb>
   b:	c3                   	ret
   c:	90                   	nop
   d:	90                   	nop
   e:	90                   	nop
   f:	90                   	nop
