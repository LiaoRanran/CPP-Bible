
ch69_constexpr_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <fib_rt(int)>:
   0:	41 57                	push   r15
   2:	41 56                	push   r14
   4:	41 55                	push   r13
   6:	41 54                	push   r12
   8:	55                   	push   rbp
   9:	57                   	push   rdi
   a:	56                   	push   rsi
   b:	53                   	push   rbx
   c:	48 81 ec 88 00 00 00 	sub    rsp,0x88
  13:	89 cf                	mov    edi,ecx
  15:	83 f9 01             	cmp    ecx,0x1
  18:	0f 8e 42 03 00 00    	jle    360 <fib_rt(int)+0x360>
  1e:	8d 41 ff             	lea    eax,[rcx-0x1]
  21:	41 89 cc             	mov    r12d,ecx
  24:	89 cb                	mov    ebx,ecx
  26:	31 f6                	xor    esi,esi
  28:	89 c2                	mov    edx,eax
  2a:	41 89 c5             	mov    r13d,eax
  2d:	83 e2 fe             	and    edx,0xfffffffe
  30:	41 29 d4             	sub    r12d,edx
  33:	44 39 e3             	cmp    ebx,r12d
  36:	0f 84 21 03 00 00    	je     35d <fib_rt(int)+0x35d>
  3c:	8d 43 fe             	lea    eax,[rbx-0x2]
  3f:	44 89 ea             	mov    edx,r13d
  42:	8d 7b fe             	lea    edi,[rbx-0x2]
  45:	31 ed                	xor    ebp,ebp
  47:	83 e0 fe             	and    eax,0xfffffffe
  4a:	29 c2                	sub    edx,eax
  4c:	89 54 24 60          	mov    DWORD PTR [rsp+0x60],edx
  50:	41 8d 45 ff          	lea    eax,[r13-0x1]
  54:	44 39 6c 24 60       	cmp    DWORD PTR [rsp+0x60],r13d
  59:	0f 84 e1 02 00 00    	je     340 <fib_rt(int)+0x340>
  5f:	41 8d 5d fe          	lea    ebx,[r13-0x2]
  63:	41 89 c5             	mov    r13d,eax
  66:	89 74 24 4c          	mov    DWORD PTR [rsp+0x4c],esi
  6a:	45 31 ff             	xor    r15d,r15d
  6d:	89 da                	mov    edx,ebx
  6f:	89 de                	mov    esi,ebx
  71:	89 eb                	mov    ebx,ebp
  73:	83 e2 fe             	and    edx,0xfffffffe
  76:	41 29 d5             	sub    r13d,edx
  79:	8d 68 ff             	lea    ebp,[rax-0x1]
  7c:	41 39 c5             	cmp    r13d,eax
  7f:	0f 84 8b 02 00 00    	je     310 <fib_rt(int)+0x310>
  85:	83 e8 02             	sub    eax,0x2
  88:	89 ea                	mov    edx,ebp
  8a:	44 89 7c 24 54       	mov    DWORD PTR [rsp+0x54],r15d
  8f:	45 31 f6             	xor    r14d,r14d
  92:	89 c1                	mov    ecx,eax
  94:	89 44 24 58          	mov    DWORD PTR [rsp+0x58],eax
  98:	41 89 e9             	mov    r9d,ebp
  9b:	83 e1 fe             	and    ecx,0xfffffffe
  9e:	44 89 6c 24 50       	mov    DWORD PTR [rsp+0x50],r13d
  a3:	45 89 e5             	mov    r13d,r12d
  a6:	41 89 fc             	mov    r12d,edi
  a9:	29 ca                	sub    edx,ecx
  ab:	89 54 24 64          	mov    DWORD PTR [rsp+0x64],edx
  af:	45 8d 51 ff          	lea    r10d,[r9-0x1]
  b3:	44 39 4c 24 64       	cmp    DWORD PTR [rsp+0x64],r9d
  b8:	0f 84 1c 02 00 00    	je     2da <fib_rt(int)+0x2da>
  be:	41 83 e9 02          	sub    r9d,0x2
  c2:	44 89 d7             	mov    edi,r10d
  c5:	89 da                	mov    edx,ebx
  c7:	45 31 ff             	xor    r15d,r15d
  ca:	44 89 c8             	mov    eax,r9d
  cd:	44 89 4c 24 5c       	mov    DWORD PTR [rsp+0x5c],r9d
  d2:	45 89 f3             	mov    r11d,r14d
  d5:	41 89 f0             	mov    r8d,esi
  d8:	83 e0 fe             	and    eax,0xfffffffe
  db:	45 89 e9             	mov    r9d,r13d
  de:	44 89 e3             	mov    ebx,r12d
  e1:	29 c7                	sub    edi,eax
  e3:	41 8d 42 ff          	lea    eax,[r10-0x1]
  e7:	44 39 d7             	cmp    edi,r10d
  ea:	0f 84 d0 01 00 00    	je     2c0 <fib_rt(int)+0x2c0>
  f0:	41 8d 72 fe          	lea    esi,[r10-0x2]
  f4:	41 89 c5             	mov    r13d,eax
  f7:	41 8d 6a fc          	lea    ebp,[r10-0x4]
  fb:	45 31 f6             	xor    r14d,r14d
  fe:	89 f1                	mov    ecx,esi
 100:	83 e1 fe             	and    ecx,0xfffffffe
 103:	41 29 cd             	sub    r13d,ecx
 106:	44 39 e8             	cmp    eax,r13d
 109:	0f 84 59 01 00 00    	je     268 <fib_rt(int)+0x268>
 10f:	44 8d 60 fe          	lea    r12d,[rax-0x2]
 113:	44 8d 50 fd          	lea    r10d,[rax-0x3]
 117:	83 e8 05             	sub    eax,0x5
 11a:	89 54 24 24          	mov    DWORD PTR [rsp+0x24],edx
 11e:	44 89 e1             	mov    ecx,r12d
 121:	44 89 ca             	mov    edx,r9d
 124:	41 89 e9             	mov    r9d,ebp
 127:	89 7c 24 28          	mov    DWORD PTR [rsp+0x28],edi
 12b:	83 e1 fe             	and    ecx,0xfffffffe
 12e:	89 5c 24 2c          	mov    DWORD PTR [rsp+0x2c],ebx
 132:	41 29 ca             	sub    r10d,ecx
 135:	89 e9                	mov    ecx,ebp
 137:	89 74 24 30          	mov    DWORD PTR [rsp+0x30],esi
 13b:	83 e1 fe             	and    ecx,0xfffffffe
 13e:	44 89 54 24 3c       	mov    DWORD PTR [rsp+0x3c],r10d
 143:	45 31 d2             	xor    r10d,r10d
 146:	29 c8                	sub    eax,ecx
 148:	89 44 24 34          	mov    DWORD PTR [rsp+0x34],eax
 14c:	41 8d 41 01          	lea    eax,[r9+0x1]
 150:	44 39 4c 24 3c       	cmp    DWORD PTR [rsp+0x3c],r9d
 155:	0f 84 d8 00 00 00    	je     233 <fib_rt(int)+0x233>
 15b:	41 8d 79 fe          	lea    edi,[r9-0x2]
 15f:	44 89 5c 24 40       	mov    DWORD PTR [rsp+0x40],r11d
 164:	44 89 ce             	mov    esi,r9d
 167:	89 7c 24 38          	mov    DWORD PTR [rsp+0x38],edi
 16b:	44 89 54 24 44       	mov    DWORD PTR [rsp+0x44],r10d
 170:	45 31 d2             	xor    r10d,r10d
 173:	83 fe 01             	cmp    esi,0x1
 176:	0f 84 84 00 00 00    	je     200 <fib_rt(int)+0x200>
 17c:	89 fb                	mov    ebx,edi
 17e:	44 8d 58 fe          	lea    r11d,[rax-0x2]
 182:	83 e8 04             	sub    eax,0x4
 185:	83 e3 fe             	and    ebx,0xfffffffe
 188:	44 89 d9             	mov    ecx,r11d
 18b:	29 d8                	sub    eax,ebx
 18d:	31 db                	xor    ebx,ebx
 18f:	89 44 24 48          	mov    DWORD PTR [rsp+0x48],eax
 193:	44 89 44 24 7c       	mov    DWORD PTR [rsp+0x7c],r8d
 198:	44 89 5c 24 78       	mov    DWORD PTR [rsp+0x78],r11d
 19d:	89 54 24 74          	mov    DWORD PTR [rsp+0x74],edx
 1a1:	44 89 4c 24 70       	mov    DWORD PTR [rsp+0x70],r9d
 1a6:	44 89 54 24 6c       	mov    DWORD PTR [rsp+0x6c],r10d
 1ab:	89 4c 24 68          	mov    DWORD PTR [rsp+0x68],ecx
 1af:	e8 4c fe ff ff       	call   0 <fib_rt(int)>
 1b4:	8b 4c 24 68          	mov    ecx,DWORD PTR [rsp+0x68]
 1b8:	44 8b 54 24 6c       	mov    r10d,DWORD PTR [rsp+0x6c]
 1bd:	01 c3                	add    ebx,eax
 1bf:	44 8b 4c 24 70       	mov    r9d,DWORD PTR [rsp+0x70]
 1c4:	8b 54 24 74          	mov    edx,DWORD PTR [rsp+0x74]
 1c8:	83 e9 02             	sub    ecx,0x2
 1cb:	39 4c 24 48          	cmp    DWORD PTR [rsp+0x48],ecx
 1cf:	44 8b 5c 24 78       	mov    r11d,DWORD PTR [rsp+0x78]
 1d4:	44 8b 44 24 7c       	mov    r8d,DWORD PTR [rsp+0x7c]
 1d9:	75 b8                	jne    193 <fib_rt(int)+0x193>
 1db:	83 ee 02             	sub    esi,0x2
 1de:	44 89 d8             	mov    eax,r11d
 1e1:	41 89 fb             	mov    r11d,edi
 1e4:	83 ef 02             	sub    edi,0x2
 1e7:	41 83 e3 fe          	and    r11d,0xfffffffe
 1eb:	89 f1                	mov    ecx,esi
 1ed:	44 29 d9             	sub    ecx,r11d
 1f0:	01 d9                	add    ecx,ebx
 1f2:	41 01 ca             	add    r10d,ecx
 1f5:	83 f8 01             	cmp    eax,0x1
 1f8:	0f 85 75 ff ff ff    	jne    173 <fib_rt(int)+0x173>
 1fe:	66 90                	xchg   ax,ax
 200:	41 8d 42 01          	lea    eax,[r10+0x1]
 204:	44 8b 54 24 44       	mov    r10d,DWORD PTR [rsp+0x44]
 209:	44 8b 5c 24 40       	mov    r11d,DWORD PTR [rsp+0x40]
 20e:	8b 7c 24 38          	mov    edi,DWORD PTR [rsp+0x38]
 212:	41 01 c2             	add    r10d,eax
 215:	39 7c 24 34          	cmp    DWORD PTR [rsp+0x34],edi
 219:	0f 84 57 01 00 00    	je     376 <fib_rt(int)+0x376>
 21f:	44 8b 4c 24 38       	mov    r9d,DWORD PTR [rsp+0x38]
 224:	41 8d 41 01          	lea    eax,[r9+0x1]
 228:	44 39 4c 24 3c       	cmp    DWORD PTR [rsp+0x3c],r9d
 22d:	0f 85 28 ff ff ff    	jne    15b <fib_rt(int)+0x15b>
 233:	41 89 d1             	mov    r9d,edx
 236:	8b 7c 24 28          	mov    edi,DWORD PTR [rsp+0x28]
 23a:	8b 54 24 24          	mov    edx,DWORD PTR [rsp+0x24]
 23e:	41 01 c2             	add    r10d,eax
 241:	8b 5c 24 2c          	mov    ebx,DWORD PTR [rsp+0x2c]
 245:	8b 74 24 30          	mov    esi,DWORD PTR [rsp+0x30]
 249:	44 89 e0             	mov    eax,r12d
 24c:	45 01 d6             	add    r14d,r10d
 24f:	83 ed 02             	sub    ebp,0x2
 252:	41 83 fc 01          	cmp    r12d,0x1
 256:	0f 85 aa fe ff ff    	jne    106 <fib_rt(int)+0x106>
 25c:	41 83 c6 01          	add    r14d,0x1
 260:	eb 0b                	jmp    26d <fib_rt(int)+0x26d>
 262:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 268:	46 8d 74 30 ff       	lea    r14d,[rax+r14*1-0x1]
 26d:	41 89 f2             	mov    r10d,esi
 270:	45 01 f7             	add    r15d,r14d
 273:	83 fe 01             	cmp    esi,0x1
 276:	0f 85 67 fe ff ff    	jne    e3 <fib_rt(int)+0xe3>
 27c:	45 89 cd             	mov    r13d,r9d
 27f:	44 8b 4c 24 5c       	mov    r9d,DWORD PTR [rsp+0x5c]
 284:	41 89 dc             	mov    r12d,ebx
 287:	45 89 de             	mov    r14d,r11d
 28a:	44 89 c6             	mov    esi,r8d
 28d:	89 d3                	mov    ebx,edx
 28f:	41 83 c7 01          	add    r15d,0x1
 293:	45 01 fe             	add    r14d,r15d
 296:	41 83 f9 01          	cmp    r9d,0x1
 29a:	0f 85 0f fe ff ff    	jne    af <fib_rt(int)+0xaf>
 2a0:	44 89 e7             	mov    edi,r12d
 2a3:	44 8b 7c 24 54       	mov    r15d,DWORD PTR [rsp+0x54]
 2a8:	45 89 ec             	mov    r12d,r13d
 2ab:	8b 44 24 58          	mov    eax,DWORD PTR [rsp+0x58]
 2af:	44 8b 6c 24 50       	mov    r13d,DWORD PTR [rsp+0x50]
 2b4:	41 83 c6 01          	add    r14d,0x1
 2b8:	eb 39                	jmp    2f3 <fib_rt(int)+0x2f3>
 2ba:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 2c0:	45 89 cd             	mov    r13d,r9d
 2c3:	41 89 dc             	mov    r12d,ebx
 2c6:	44 8b 4c 24 5c       	mov    r9d,DWORD PTR [rsp+0x5c]
 2cb:	45 89 de             	mov    r14d,r11d
 2ce:	44 89 c6             	mov    esi,r8d
 2d1:	89 d3                	mov    ebx,edx
 2d3:	47 8d 7c 3a ff       	lea    r15d,[r10+r15*1-0x1]
 2d8:	eb b9                	jmp    293 <fib_rt(int)+0x293>
 2da:	44 89 e7             	mov    edi,r12d
 2dd:	44 8b 7c 24 54       	mov    r15d,DWORD PTR [rsp+0x54]
 2e2:	45 89 ec             	mov    r12d,r13d
 2e5:	8b 44 24 58          	mov    eax,DWORD PTR [rsp+0x58]
 2e9:	44 8b 6c 24 50       	mov    r13d,DWORD PTR [rsp+0x50]
 2ee:	47 8d 74 31 ff       	lea    r14d,[r9+r14*1-0x1]
 2f3:	45 01 f7             	add    r15d,r14d
 2f6:	83 f8 01             	cmp    eax,0x1
 2f9:	0f 85 7a fd ff ff    	jne    79 <fib_rt(int)+0x79>
 2ff:	89 dd                	mov    ebp,ebx
 301:	41 83 c7 01          	add    r15d,0x1
 305:	89 f3                	mov    ebx,esi
 307:	8b 74 24 4c          	mov    esi,DWORD PTR [rsp+0x4c]
 30b:	eb 10                	jmp    31d <fib_rt(int)+0x31d>
 30d:	0f 1f 00             	nop    DWORD PTR [rax]
 310:	89 dd                	mov    ebp,ebx
 312:	89 f3                	mov    ebx,esi
 314:	8b 74 24 4c          	mov    esi,DWORD PTR [rsp+0x4c]
 318:	46 8d 7c 38 ff       	lea    r15d,[rax+r15*1-0x1]
 31d:	41 89 dd             	mov    r13d,ebx
 320:	44 01 fd             	add    ebp,r15d
 323:	83 fb 01             	cmp    ebx,0x1
 326:	0f 85 24 fd ff ff    	jne    50 <fib_rt(int)+0x50>
 32c:	83 c5 01             	add    ebp,0x1
 32f:	89 fb                	mov    ebx,edi
 331:	01 ee                	add    esi,ebp
 333:	83 fb 01             	cmp    ebx,0x1
 336:	75 16                	jne    34e <fib_rt(int)+0x34e>
 338:	8d 7e 01             	lea    edi,[rsi+0x1]
 33b:	eb 23                	jmp    360 <fib_rt(int)+0x360>
 33d:	0f 1f 00             	nop    DWORD PTR [rax]
 340:	41 8d 6c 2d ff       	lea    ebp,[r13+rbp*1-0x1]
 345:	89 fb                	mov    ebx,edi
 347:	01 ee                	add    esi,ebp
 349:	83 fb 01             	cmp    ebx,0x1
 34c:	74 ea                	je     338 <fib_rt(int)+0x338>
 34e:	8d 43 ff             	lea    eax,[rbx-0x1]
 351:	41 89 c5             	mov    r13d,eax
 354:	44 39 e3             	cmp    ebx,r12d
 357:	0f 85 df fc ff ff    	jne    3c <fib_rt(int)+0x3c>
 35d:	8d 3c 30             	lea    edi,[rax+rsi*1]
 360:	89 f8                	mov    eax,edi
 362:	48 81 c4 88 00 00 00 	add    rsp,0x88
 369:	5b                   	pop    rbx
 36a:	5e                   	pop    rsi
 36b:	5f                   	pop    rdi
 36c:	5d                   	pop    rbp
 36d:	41 5c                	pop    r12
 36f:	41 5d                	pop    r13
 371:	41 5e                	pop    r14
 373:	41 5f                	pop    r15
 375:	c3                   	ret
 376:	45 01 ca             	add    r10d,r9d
 379:	8b 7c 24 28          	mov    edi,DWORD PTR [rsp+0x28]
 37d:	41 89 d1             	mov    r9d,edx
 380:	8b 5c 24 2c          	mov    ebx,DWORD PTR [rsp+0x2c]
 384:	8b 54 24 24          	mov    edx,DWORD PTR [rsp+0x24]
 388:	8b 74 24 30          	mov    esi,DWORD PTR [rsp+0x30]
 38c:	e9 b8 fe ff ff       	jmp    249 <fib_rt(int)+0x249>
 391:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
 395:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 39c:	00 00 00 00 

00000000000003a0 <use_constexpr()>:
 3a0:	b8 6d 1a 00 00       	mov    eax,0x1a6d
 3a5:	c3                   	ret
 3a6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
 3ad:	00 00 00 

00000000000003b0 <use_runtime()>:
 3b0:	56                   	push   rsi
 3b1:	53                   	push   rbx
 3b2:	48 83 ec 28          	sub    rsp,0x28
 3b6:	bb 13 00 00 00       	mov    ebx,0x13
 3bb:	31 f6                	xor    esi,esi
 3bd:	89 d9                	mov    ecx,ebx
 3bf:	83 eb 02             	sub    ebx,0x2
 3c2:	e8 39 fc ff ff       	call   0 <fib_rt(int)>
 3c7:	01 c6                	add    esi,eax
 3c9:	83 fb ff             	cmp    ebx,0xffffffff
 3cc:	75 ef                	jne    3bd <use_runtime()+0xd>
 3ce:	89 f0                	mov    eax,esi
 3d0:	48 83 c4 28          	add    rsp,0x28
 3d4:	5b                   	pop    rbx
 3d5:	5e                   	pop    rsi
 3d6:	c3                   	ret
 3d7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 3de:	00 00 

00000000000003e0 <use_constexpr_runtime_arg(int)>:
 3e0:	41 54                	push   r12
 3e2:	55                   	push   rbp
 3e3:	57                   	push   rdi
 3e4:	56                   	push   rsi
 3e5:	53                   	push   rbx
 3e6:	48 83 ec 20          	sub    rsp,0x20
 3ea:	89 ce                	mov    esi,ecx
 3ec:	89 c8                	mov    eax,ecx
 3ee:	83 f9 01             	cmp    ecx,0x1
 3f1:	7e 31                	jle    424 <use_constexpr_runtime_arg(int)+0x44>
 3f3:	44 8d 61 fe          	lea    r12d,[rcx-0x2]
 3f7:	8d 69 fd             	lea    ebp,[rcx-0x3]
 3fa:	31 ff                	xor    edi,edi
 3fc:	44 89 e0             	mov    eax,r12d
 3ff:	8d 59 ff             	lea    ebx,[rcx-0x1]
 402:	83 e0 fe             	and    eax,0xfffffffe
 405:	29 c5                	sub    ebp,eax
 407:	89 d9                	mov    ecx,ebx
 409:	83 eb 02             	sub    ebx,0x2
 40c:	e8 00 00 00 00       	call   411 <use_constexpr_runtime_arg(int)+0x31>
 411:	01 c7                	add    edi,eax
 413:	39 eb                	cmp    ebx,ebp
 415:	75 f0                	jne    407 <use_constexpr_runtime_arg(int)+0x27>
 417:	d1 ee                	shr    esi,1
 419:	44 89 e0             	mov    eax,r12d
 41c:	8d 54 36 fe          	lea    edx,[rsi+rsi*1-0x2]
 420:	29 d0                	sub    eax,edx
 422:	01 f8                	add    eax,edi
 424:	48 83 c4 20          	add    rsp,0x20
 428:	5b                   	pop    rbx
 429:	5e                   	pop    rsi
 42a:	5f                   	pop    rdi
 42b:	5d                   	pop    rbp
 42c:	41 5c                	pop    r12
 42e:	c3                   	ret
 42f:	90                   	nop

Disassembly of section .text$_Z6fib_cxi:

0000000000000000 <fib_cx(int)>:
   0:	41 57                	push   r15
   2:	41 56                	push   r14
   4:	41 55                	push   r13
   6:	41 54                	push   r12
   8:	55                   	push   rbp
   9:	57                   	push   rdi
   a:	56                   	push   rsi
   b:	53                   	push   rbx
   c:	48 81 ec 88 00 00 00 	sub    rsp,0x88
  13:	89 cf                	mov    edi,ecx
  15:	83 f9 01             	cmp    ecx,0x1
  18:	0f 8e 42 03 00 00    	jle    360 <fib_cx(int)+0x360>
  1e:	8d 41 ff             	lea    eax,[rcx-0x1]
  21:	41 89 cc             	mov    r12d,ecx
  24:	89 cb                	mov    ebx,ecx
  26:	31 f6                	xor    esi,esi
  28:	89 c2                	mov    edx,eax
  2a:	41 89 c5             	mov    r13d,eax
  2d:	83 e2 fe             	and    edx,0xfffffffe
  30:	41 29 d4             	sub    r12d,edx
  33:	44 39 e3             	cmp    ebx,r12d
  36:	0f 84 21 03 00 00    	je     35d <fib_cx(int)+0x35d>
  3c:	8d 43 fe             	lea    eax,[rbx-0x2]
  3f:	44 89 ea             	mov    edx,r13d
  42:	8d 7b fe             	lea    edi,[rbx-0x2]
  45:	31 ed                	xor    ebp,ebp
  47:	83 e0 fe             	and    eax,0xfffffffe
  4a:	29 c2                	sub    edx,eax
  4c:	89 54 24 60          	mov    DWORD PTR [rsp+0x60],edx
  50:	41 8d 45 ff          	lea    eax,[r13-0x1]
  54:	44 39 6c 24 60       	cmp    DWORD PTR [rsp+0x60],r13d
  59:	0f 84 e1 02 00 00    	je     340 <fib_cx(int)+0x340>
  5f:	41 8d 5d fe          	lea    ebx,[r13-0x2]
  63:	41 89 c5             	mov    r13d,eax
  66:	89 74 24 4c          	mov    DWORD PTR [rsp+0x4c],esi
  6a:	45 31 ff             	xor    r15d,r15d
  6d:	89 da                	mov    edx,ebx
  6f:	89 de                	mov    esi,ebx
  71:	89 eb                	mov    ebx,ebp
  73:	83 e2 fe             	and    edx,0xfffffffe
  76:	41 29 d5             	sub    r13d,edx
  79:	8d 68 ff             	lea    ebp,[rax-0x1]
  7c:	41 39 c5             	cmp    r13d,eax
  7f:	0f 84 8b 02 00 00    	je     310 <fib_cx(int)+0x310>
  85:	83 e8 02             	sub    eax,0x2
  88:	89 ea                	mov    edx,ebp
  8a:	44 89 7c 24 54       	mov    DWORD PTR [rsp+0x54],r15d
  8f:	45 31 f6             	xor    r14d,r14d
  92:	89 c1                	mov    ecx,eax
  94:	89 44 24 58          	mov    DWORD PTR [rsp+0x58],eax
  98:	41 89 e9             	mov    r9d,ebp
  9b:	83 e1 fe             	and    ecx,0xfffffffe
  9e:	44 89 6c 24 50       	mov    DWORD PTR [rsp+0x50],r13d
  a3:	45 89 e5             	mov    r13d,r12d
  a6:	41 89 fc             	mov    r12d,edi
  a9:	29 ca                	sub    edx,ecx
  ab:	89 54 24 64          	mov    DWORD PTR [rsp+0x64],edx
  af:	45 8d 51 ff          	lea    r10d,[r9-0x1]
  b3:	44 39 4c 24 64       	cmp    DWORD PTR [rsp+0x64],r9d
  b8:	0f 84 1c 02 00 00    	je     2da <fib_cx(int)+0x2da>
  be:	41 83 e9 02          	sub    r9d,0x2
  c2:	44 89 d7             	mov    edi,r10d
  c5:	89 da                	mov    edx,ebx
  c7:	45 31 ff             	xor    r15d,r15d
  ca:	44 89 c8             	mov    eax,r9d
  cd:	44 89 4c 24 5c       	mov    DWORD PTR [rsp+0x5c],r9d
  d2:	45 89 f3             	mov    r11d,r14d
  d5:	41 89 f0             	mov    r8d,esi
  d8:	83 e0 fe             	and    eax,0xfffffffe
  db:	45 89 e9             	mov    r9d,r13d
  de:	44 89 e3             	mov    ebx,r12d
  e1:	29 c7                	sub    edi,eax
  e3:	41 8d 42 ff          	lea    eax,[r10-0x1]
  e7:	44 39 d7             	cmp    edi,r10d
  ea:	0f 84 d0 01 00 00    	je     2c0 <fib_cx(int)+0x2c0>
  f0:	41 8d 72 fe          	lea    esi,[r10-0x2]
  f4:	41 89 c5             	mov    r13d,eax
  f7:	41 8d 6a fc          	lea    ebp,[r10-0x4]
  fb:	45 31 f6             	xor    r14d,r14d
  fe:	89 f1                	mov    ecx,esi
 100:	83 e1 fe             	and    ecx,0xfffffffe
 103:	41 29 cd             	sub    r13d,ecx
 106:	44 39 e8             	cmp    eax,r13d
 109:	0f 84 59 01 00 00    	je     268 <fib_cx(int)+0x268>
 10f:	44 8d 60 fe          	lea    r12d,[rax-0x2]
 113:	44 8d 50 fd          	lea    r10d,[rax-0x3]
 117:	83 e8 05             	sub    eax,0x5
 11a:	89 54 24 24          	mov    DWORD PTR [rsp+0x24],edx
 11e:	44 89 e1             	mov    ecx,r12d
 121:	44 89 ca             	mov    edx,r9d
 124:	41 89 e9             	mov    r9d,ebp
 127:	89 7c 24 28          	mov    DWORD PTR [rsp+0x28],edi
 12b:	83 e1 fe             	and    ecx,0xfffffffe
 12e:	89 5c 24 2c          	mov    DWORD PTR [rsp+0x2c],ebx
 132:	41 29 ca             	sub    r10d,ecx
 135:	89 e9                	mov    ecx,ebp
 137:	89 74 24 30          	mov    DWORD PTR [rsp+0x30],esi
 13b:	83 e1 fe             	and    ecx,0xfffffffe
 13e:	44 89 54 24 3c       	mov    DWORD PTR [rsp+0x3c],r10d
 143:	45 31 d2             	xor    r10d,r10d
 146:	29 c8                	sub    eax,ecx
 148:	89 44 24 34          	mov    DWORD PTR [rsp+0x34],eax
 14c:	41 8d 41 01          	lea    eax,[r9+0x1]
 150:	44 39 4c 24 3c       	cmp    DWORD PTR [rsp+0x3c],r9d
 155:	0f 84 d8 00 00 00    	je     233 <fib_cx(int)+0x233>
 15b:	41 8d 79 fe          	lea    edi,[r9-0x2]
 15f:	44 89 5c 24 40       	mov    DWORD PTR [rsp+0x40],r11d
 164:	44 89 ce             	mov    esi,r9d
 167:	89 7c 24 38          	mov    DWORD PTR [rsp+0x38],edi
 16b:	44 89 54 24 44       	mov    DWORD PTR [rsp+0x44],r10d
 170:	45 31 d2             	xor    r10d,r10d
 173:	83 fe 01             	cmp    esi,0x1
 176:	0f 84 84 00 00 00    	je     200 <fib_cx(int)+0x200>
 17c:	89 fb                	mov    ebx,edi
 17e:	44 8d 58 fe          	lea    r11d,[rax-0x2]
 182:	83 e8 04             	sub    eax,0x4
 185:	83 e3 fe             	and    ebx,0xfffffffe
 188:	44 89 d9             	mov    ecx,r11d
 18b:	29 d8                	sub    eax,ebx
 18d:	31 db                	xor    ebx,ebx
 18f:	89 44 24 48          	mov    DWORD PTR [rsp+0x48],eax
 193:	44 89 44 24 7c       	mov    DWORD PTR [rsp+0x7c],r8d
 198:	44 89 5c 24 78       	mov    DWORD PTR [rsp+0x78],r11d
 19d:	89 54 24 74          	mov    DWORD PTR [rsp+0x74],edx
 1a1:	44 89 4c 24 70       	mov    DWORD PTR [rsp+0x70],r9d
 1a6:	44 89 54 24 6c       	mov    DWORD PTR [rsp+0x6c],r10d
 1ab:	89 4c 24 68          	mov    DWORD PTR [rsp+0x68],ecx
 1af:	e8 4c fe ff ff       	call   0 <fib_cx(int)>
 1b4:	8b 4c 24 68          	mov    ecx,DWORD PTR [rsp+0x68]
 1b8:	44 8b 54 24 6c       	mov    r10d,DWORD PTR [rsp+0x6c]
 1bd:	01 c3                	add    ebx,eax
 1bf:	44 8b 4c 24 70       	mov    r9d,DWORD PTR [rsp+0x70]
 1c4:	8b 54 24 74          	mov    edx,DWORD PTR [rsp+0x74]
 1c8:	83 e9 02             	sub    ecx,0x2
 1cb:	39 4c 24 48          	cmp    DWORD PTR [rsp+0x48],ecx
 1cf:	44 8b 5c 24 78       	mov    r11d,DWORD PTR [rsp+0x78]
 1d4:	44 8b 44 24 7c       	mov    r8d,DWORD PTR [rsp+0x7c]
 1d9:	75 b8                	jne    193 <fib_cx(int)+0x193>
 1db:	83 ee 02             	sub    esi,0x2
 1de:	44 89 d8             	mov    eax,r11d
 1e1:	41 89 fb             	mov    r11d,edi
 1e4:	83 ef 02             	sub    edi,0x2
 1e7:	41 83 e3 fe          	and    r11d,0xfffffffe
 1eb:	89 f1                	mov    ecx,esi
 1ed:	44 29 d9             	sub    ecx,r11d
 1f0:	01 d9                	add    ecx,ebx
 1f2:	41 01 ca             	add    r10d,ecx
 1f5:	83 f8 01             	cmp    eax,0x1
 1f8:	0f 85 75 ff ff ff    	jne    173 <fib_cx(int)+0x173>
 1fe:	66 90                	xchg   ax,ax
 200:	41 8d 42 01          	lea    eax,[r10+0x1]
 204:	44 8b 54 24 44       	mov    r10d,DWORD PTR [rsp+0x44]
 209:	44 8b 5c 24 40       	mov    r11d,DWORD PTR [rsp+0x40]
 20e:	8b 7c 24 38          	mov    edi,DWORD PTR [rsp+0x38]
 212:	41 01 c2             	add    r10d,eax
 215:	39 7c 24 34          	cmp    DWORD PTR [rsp+0x34],edi
 219:	0f 84 57 01 00 00    	je     376 <fib_cx(int)+0x376>
 21f:	44 8b 4c 24 38       	mov    r9d,DWORD PTR [rsp+0x38]
 224:	41 8d 41 01          	lea    eax,[r9+0x1]
 228:	44 39 4c 24 3c       	cmp    DWORD PTR [rsp+0x3c],r9d
 22d:	0f 85 28 ff ff ff    	jne    15b <fib_cx(int)+0x15b>
 233:	41 89 d1             	mov    r9d,edx
 236:	8b 7c 24 28          	mov    edi,DWORD PTR [rsp+0x28]
 23a:	8b 54 24 24          	mov    edx,DWORD PTR [rsp+0x24]
 23e:	41 01 c2             	add    r10d,eax
 241:	8b 5c 24 2c          	mov    ebx,DWORD PTR [rsp+0x2c]
 245:	8b 74 24 30          	mov    esi,DWORD PTR [rsp+0x30]
 249:	44 89 e0             	mov    eax,r12d
 24c:	45 01 d6             	add    r14d,r10d
 24f:	83 ed 02             	sub    ebp,0x2
 252:	41 83 fc 01          	cmp    r12d,0x1
 256:	0f 85 aa fe ff ff    	jne    106 <fib_cx(int)+0x106>
 25c:	41 83 c6 01          	add    r14d,0x1
 260:	eb 0b                	jmp    26d <fib_cx(int)+0x26d>
 262:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 268:	46 8d 74 30 ff       	lea    r14d,[rax+r14*1-0x1]
 26d:	41 89 f2             	mov    r10d,esi
 270:	45 01 f7             	add    r15d,r14d
 273:	83 fe 01             	cmp    esi,0x1
 276:	0f 85 67 fe ff ff    	jne    e3 <fib_cx(int)+0xe3>
 27c:	45 89 cd             	mov    r13d,r9d
 27f:	44 8b 4c 24 5c       	mov    r9d,DWORD PTR [rsp+0x5c]
 284:	41 89 dc             	mov    r12d,ebx
 287:	45 89 de             	mov    r14d,r11d
 28a:	44 89 c6             	mov    esi,r8d
 28d:	89 d3                	mov    ebx,edx
 28f:	41 83 c7 01          	add    r15d,0x1
 293:	45 01 fe             	add    r14d,r15d
 296:	41 83 f9 01          	cmp    r9d,0x1
 29a:	0f 85 0f fe ff ff    	jne    af <fib_cx(int)+0xaf>
 2a0:	44 89 e7             	mov    edi,r12d
 2a3:	44 8b 7c 24 54       	mov    r15d,DWORD PTR [rsp+0x54]
 2a8:	45 89 ec             	mov    r12d,r13d
 2ab:	8b 44 24 58          	mov    eax,DWORD PTR [rsp+0x58]
 2af:	44 8b 6c 24 50       	mov    r13d,DWORD PTR [rsp+0x50]
 2b4:	41 83 c6 01          	add    r14d,0x1
 2b8:	eb 39                	jmp    2f3 <fib_cx(int)+0x2f3>
 2ba:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 2c0:	45 89 cd             	mov    r13d,r9d
 2c3:	41 89 dc             	mov    r12d,ebx
 2c6:	44 8b 4c 24 5c       	mov    r9d,DWORD PTR [rsp+0x5c]
 2cb:	45 89 de             	mov    r14d,r11d
 2ce:	44 89 c6             	mov    esi,r8d
 2d1:	89 d3                	mov    ebx,edx
 2d3:	47 8d 7c 3a ff       	lea    r15d,[r10+r15*1-0x1]
 2d8:	eb b9                	jmp    293 <fib_cx(int)+0x293>
 2da:	44 89 e7             	mov    edi,r12d
 2dd:	44 8b 7c 24 54       	mov    r15d,DWORD PTR [rsp+0x54]
 2e2:	45 89 ec             	mov    r12d,r13d
 2e5:	8b 44 24 58          	mov    eax,DWORD PTR [rsp+0x58]
 2e9:	44 8b 6c 24 50       	mov    r13d,DWORD PTR [rsp+0x50]
 2ee:	47 8d 74 31 ff       	lea    r14d,[r9+r14*1-0x1]
 2f3:	45 01 f7             	add    r15d,r14d
 2f6:	83 f8 01             	cmp    eax,0x1
 2f9:	0f 85 7a fd ff ff    	jne    79 <fib_cx(int)+0x79>
 2ff:	89 dd                	mov    ebp,ebx
 301:	41 83 c7 01          	add    r15d,0x1
 305:	89 f3                	mov    ebx,esi
 307:	8b 74 24 4c          	mov    esi,DWORD PTR [rsp+0x4c]
 30b:	eb 10                	jmp    31d <fib_cx(int)+0x31d>
 30d:	0f 1f 00             	nop    DWORD PTR [rax]
 310:	89 dd                	mov    ebp,ebx
 312:	89 f3                	mov    ebx,esi
 314:	8b 74 24 4c          	mov    esi,DWORD PTR [rsp+0x4c]
 318:	46 8d 7c 38 ff       	lea    r15d,[rax+r15*1-0x1]
 31d:	41 89 dd             	mov    r13d,ebx
 320:	44 01 fd             	add    ebp,r15d
 323:	83 fb 01             	cmp    ebx,0x1
 326:	0f 85 24 fd ff ff    	jne    50 <fib_cx(int)+0x50>
 32c:	83 c5 01             	add    ebp,0x1
 32f:	89 fb                	mov    ebx,edi
 331:	01 ee                	add    esi,ebp
 333:	83 fb 01             	cmp    ebx,0x1
 336:	75 16                	jne    34e <fib_cx(int)+0x34e>
 338:	8d 7e 01             	lea    edi,[rsi+0x1]
 33b:	eb 23                	jmp    360 <fib_cx(int)+0x360>
 33d:	0f 1f 00             	nop    DWORD PTR [rax]
 340:	41 8d 6c 2d ff       	lea    ebp,[r13+rbp*1-0x1]
 345:	89 fb                	mov    ebx,edi
 347:	01 ee                	add    esi,ebp
 349:	83 fb 01             	cmp    ebx,0x1
 34c:	74 ea                	je     338 <fib_cx(int)+0x338>
 34e:	8d 43 ff             	lea    eax,[rbx-0x1]
 351:	41 89 c5             	mov    r13d,eax
 354:	44 39 e3             	cmp    ebx,r12d
 357:	0f 85 df fc ff ff    	jne    3c <fib_cx(int)+0x3c>
 35d:	8d 3c 30             	lea    edi,[rax+rsi*1]
 360:	89 f8                	mov    eax,edi
 362:	48 81 c4 88 00 00 00 	add    rsp,0x88
 369:	5b                   	pop    rbx
 36a:	5e                   	pop    rsi
 36b:	5f                   	pop    rdi
 36c:	5d                   	pop    rbp
 36d:	41 5c                	pop    r12
 36f:	41 5d                	pop    r13
 371:	41 5e                	pop    r14
 373:	41 5f                	pop    r15
 375:	c3                   	ret
 376:	45 01 ca             	add    r10d,r9d
 379:	8b 7c 24 28          	mov    edi,DWORD PTR [rsp+0x28]
 37d:	41 89 d1             	mov    r9d,edx
 380:	8b 5c 24 2c          	mov    ebx,DWORD PTR [rsp+0x2c]
 384:	8b 54 24 24          	mov    edx,DWORD PTR [rsp+0x24]
 388:	8b 74 24 30          	mov    esi,DWORD PTR [rsp+0x30]
 38c:	e9 b8 fe ff ff       	jmp    249 <fib_cx(int)+0x249>
 391:	90                   	nop
 392:	90                   	nop
 393:	90                   	nop
 394:	90                   	nop
 395:	90                   	nop
 396:	90                   	nop
 397:	90                   	nop
 398:	90                   	nop
 399:	90                   	nop
 39a:	90                   	nop
 39b:	90                   	nop
 39c:	90                   	nop
 39d:	90                   	nop
 39e:	90                   	nop
 39f:	90                   	nop
