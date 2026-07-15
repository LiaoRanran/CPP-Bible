
ch77_vector_grow_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <push_no_reserve()>:
   0:	41 56                	push   r14
   2:	41 55                	push   r13
   4:	41 54                	push   r12
   6:	55                   	push   rbp
   7:	57                   	push   rdi
   8:	56                   	push   rsi
   9:	53                   	push   rbx
   a:	48 83 ec 20          	sub    rsp,0x20
   e:	31 ed                	xor    ebp,ebp
  10:	31 f6                	xor    esi,esi
  12:	45 31 e4             	xor    r12d,r12d
  15:	49 bd ff ff ff ff ff 	movabs r13,0x1fffffffffffffff
  1c:	ff ff 1f 
  1f:	31 db                	xor    ebx,ebx
  21:	eb 2f                	jmp    52 <push_no_reserve()+0x52>
  23:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
  2a:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  31:	00 00 00 00 
  35:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  3c:	00 00 00 00 
  40:	89 1e                	mov    DWORD PTR [rsi],ebx
  42:	83 c3 01             	add    ebx,0x1
  45:	48 83 c6 04          	add    rsi,0x4
  49:	83 fb 08             	cmp    ebx,0x8
  4c:	0f 84 9e 00 00 00    	je     f0 <push_no_reserve()+0xf0>
  52:	48 39 ee             	cmp    rsi,rbp
  55:	75 e9                	jne    40 <push_no_reserve()+0x40>
  57:	48 89 ee             	mov    rsi,rbp
  5a:	4c 29 e6             	sub    rsi,r12
  5d:	48 89 f2             	mov    rdx,rsi
  60:	48 c1 fa 02          	sar    rdx,0x2
  64:	4c 39 ea             	cmp    rdx,r13
  67:	0f 84 00 00 00 00    	je     6d <push_no_reserve()+0x6d>
  6d:	48 85 d2             	test   rdx,rdx
  70:	b8 01 00 00 00       	mov    eax,0x1
  75:	48 0f 45 c2          	cmovne rax,rdx
  79:	48 01 d0             	add    rax,rdx
  7c:	48 ba ff ff ff ff ff 	movabs rdx,0x1fffffffffffffff
  83:	ff ff 1f 
  86:	48 39 d0             	cmp    rax,rdx
  89:	48 0f 47 c2          	cmova  rax,rdx
  8d:	48 8d 3c 85 00 00 00 	lea    rdi,[rax*4+0x0]
  94:	00 
  95:	48 89 f9             	mov    rcx,rdi
  98:	e8 00 00 00 00       	call   9d <push_no_reserve()+0x9d>
  9d:	89 1c 30             	mov    DWORD PTR [rax+rsi*1],ebx
  a0:	49 89 c6             	mov    r14,rax
  a3:	48 85 f6             	test   rsi,rsi
  a6:	74 0e                	je     b6 <push_no_reserve()+0xb6>
  a8:	49 89 f0             	mov    r8,rsi
  ab:	4c 89 e2             	mov    rdx,r12
  ae:	48 89 c1             	mov    rcx,rax
  b1:	e8 00 00 00 00       	call   b6 <push_no_reserve()+0xb6>
  b6:	49 8d 74 36 04       	lea    rsi,[r14+rsi*1+0x4]
  bb:	4d 85 e4             	test   r12,r12
  be:	74 0e                	je     ce <push_no_reserve()+0xce>
  c0:	48 89 ea             	mov    rdx,rbp
  c3:	4c 89 e1             	mov    rcx,r12
  c6:	4c 29 e2             	sub    rdx,r12
  c9:	e8 00 00 00 00       	call   ce <push_no_reserve()+0xce>
  ce:	83 c3 01             	add    ebx,0x1
  d1:	49 8d 2c 3e          	lea    rbp,[r14+rdi*1]
  d5:	4d 89 f4             	mov    r12,r14
  d8:	83 fb 08             	cmp    ebx,0x8
  db:	0f 85 71 ff ff ff    	jne    52 <push_no_reserve()+0x52>
  e1:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  e5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  ec:	00 00 00 00 
  f0:	4d 85 e4             	test   r12,r12
  f3:	74 23                	je     118 <push_no_reserve()+0x118>
  f5:	48 89 ea             	mov    rdx,rbp
  f8:	4c 89 e1             	mov    rcx,r12
  fb:	4c 29 e2             	sub    rdx,r12
  fe:	48 83 c4 20          	add    rsp,0x20
 102:	5b                   	pop    rbx
 103:	5e                   	pop    rsi
 104:	5f                   	pop    rdi
 105:	5d                   	pop    rbp
 106:	41 5c                	pop    r12
 108:	41 5d                	pop    r13
 10a:	41 5e                	pop    r14
 10c:	e9 00 00 00 00       	jmp    111 <push_no_reserve()+0x111>
 111:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
 118:	48 83 c4 20          	add    rsp,0x20
 11c:	5b                   	pop    rbx
 11d:	5e                   	pop    rsi
 11e:	5f                   	pop    rdi
 11f:	5d                   	pop    rbp
 120:	41 5c                	pop    r12
 122:	41 5d                	pop    r13
 124:	41 5e                	pop    r14
 126:	c3                   	ret
 127:	e9 0c 00 00 00       	jmp    138 <push_reserved()+0x8>
 12c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000000130 <push_reserved()>:
 130:	41 56                	push   r14
 132:	41 55                	push   r13
 134:	41 54                	push   r12
 136:	55                   	push   rbp
 137:	57                   	push   rdi
 138:	56                   	push   rsi
 139:	53                   	push   rbx
 13a:	48 83 ec 20          	sub    rsp,0x20
 13e:	b9 40 00 00 00       	mov    ecx,0x40
 143:	31 f6                	xor    esi,esi
 145:	49 bd ff ff ff ff ff 	movabs r13,0x1fffffffffffffff
 14c:	ff ff 1f 
 14f:	e8 00 00 00 00       	call   154 <push_reserved()+0x24>
 154:	48 89 c3             	mov    rbx,rax
 157:	48 8d 68 40          	lea    rbp,[rax+0x40]
 15b:	49 89 c4             	mov    r12,rax
 15e:	eb 12                	jmp    172 <push_reserved()+0x42>
 160:	89 33                	mov    DWORD PTR [rbx],esi
 162:	83 c6 01             	add    esi,0x1
 165:	48 83 c3 04          	add    rbx,0x4
 169:	83 fe 08             	cmp    esi,0x8
 16c:	0f 84 9e 00 00 00    	je     210 <push_reserved()+0xe0>
 172:	48 39 dd             	cmp    rbp,rbx
 175:	75 e9                	jne    160 <push_reserved()+0x30>
 177:	48 89 eb             	mov    rbx,rbp
 17a:	4c 29 e3             	sub    rbx,r12
 17d:	48 89 da             	mov    rdx,rbx
 180:	48 c1 fa 02          	sar    rdx,0x2
 184:	4c 39 ea             	cmp    rdx,r13
 187:	0f 84 2b 00 00 00    	je     1b8 <push_reserved()+0x88>
 18d:	48 85 d2             	test   rdx,rdx
 190:	b8 01 00 00 00       	mov    eax,0x1
 195:	48 0f 45 c2          	cmovne rax,rdx
 199:	48 01 d0             	add    rax,rdx
 19c:	48 ba ff ff ff ff ff 	movabs rdx,0x1fffffffffffffff
 1a3:	ff ff 1f 
 1a6:	48 39 d0             	cmp    rax,rdx
 1a9:	48 0f 47 c2          	cmova  rax,rdx
 1ad:	48 8d 3c 85 00 00 00 	lea    rdi,[rax*4+0x0]
 1b4:	00 
 1b5:	48 89 f9             	mov    rcx,rdi
 1b8:	e8 00 00 00 00       	call   1bd <push_reserved()+0x8d>
 1bd:	89 34 18             	mov    DWORD PTR [rax+rbx*1],esi
 1c0:	49 89 c6             	mov    r14,rax
 1c3:	48 85 db             	test   rbx,rbx
 1c6:	74 0e                	je     1d6 <push_reserved()+0xa6>
 1c8:	49 89 d8             	mov    r8,rbx
 1cb:	4c 89 e2             	mov    rdx,r12
 1ce:	48 89 c1             	mov    rcx,rax
 1d1:	e8 00 00 00 00       	call   1d6 <push_reserved()+0xa6>
 1d6:	49 8d 5c 1e 04       	lea    rbx,[r14+rbx*1+0x4]
 1db:	4d 85 e4             	test   r12,r12
 1de:	74 0e                	je     1ee <push_reserved()+0xbe>
 1e0:	48 89 ea             	mov    rdx,rbp
 1e3:	4c 89 e1             	mov    rcx,r12
 1e6:	4c 29 e2             	sub    rdx,r12
 1e9:	e8 00 00 00 00       	call   1ee <push_reserved()+0xbe>
 1ee:	83 c6 01             	add    esi,0x1
 1f1:	49 8d 2c 3e          	lea    rbp,[r14+rdi*1]
 1f5:	4d 89 f4             	mov    r12,r14
 1f8:	83 fe 08             	cmp    esi,0x8
 1fb:	0f 85 71 ff ff ff    	jne    172 <push_reserved()+0x42>
 201:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
 205:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 20c:	00 00 00 00 
 210:	4d 85 e4             	test   r12,r12
 213:	74 23                	je     238 <push_reserved()+0x108>
 215:	48 89 ea             	mov    rdx,rbp
 218:	4c 89 e1             	mov    rcx,r12
 21b:	4c 29 e2             	sub    rdx,r12
 21e:	48 83 c4 20          	add    rsp,0x20
 222:	5b                   	pop    rbx
 223:	5e                   	pop    rsi
 224:	5f                   	pop    rdi
 225:	5d                   	pop    rbp
 226:	41 5c                	pop    r12
 228:	41 5d                	pop    r13
 22a:	41 5e                	pop    r14
 22c:	e9 00 00 00 00       	jmp    231 <push_reserved()+0x101>
 231:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
 238:	48 83 c4 20          	add    rsp,0x20
 23c:	5b                   	pop    rbx
 23d:	5e                   	pop    rsi
 23e:	5f                   	pop    rdi
 23f:	5d                   	pop    rbp
 240:	41 5c                	pop    r12
 242:	41 5d                	pop    r13
 244:	41 5e                	pop    r14
 246:	c3                   	ret
 247:	e9 37 00 00 00       	jmp    283 <push_reserved()+0x153>
 24c:	90                   	nop
 24d:	90                   	nop
 24e:	90                   	nop
 24f:	90                   	nop
 250:	90                   	nop
 251:	90                   	nop
 252:	90                   	nop
 253:	90                   	nop
 254:	90                   	nop
 255:	90                   	nop
 256:	90                   	nop
 257:	90                   	nop
 258:	90                   	nop
 259:	90                   	nop
 25a:	90                   	nop
 25b:	90                   	nop
 25c:	90                   	nop
 25d:	90                   	nop
 25e:	90                   	nop
 25f:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <push_no_reserve() [clone .cold]>:
   0:	48 8d 0d 00 00 00 00 	lea    rcx,[rip+0x0]        # 7 <push_no_reserve() [clone .cold]+0x7>
   7:	e8 00 00 00 00       	call   c <push_no_reserve() [clone .cold]+0xc>
   c:	48 89 c3             	mov    rbx,rax
   f:	4d 85 e4             	test   r12,r12
  12:	74 0e                	je     22 <push_no_reserve() [clone .cold]+0x22>
  14:	48 89 ea             	mov    rdx,rbp
  17:	4c 89 e1             	mov    rcx,r12
  1a:	4c 29 e2             	sub    rdx,r12
  1d:	e8 00 00 00 00       	call   22 <push_no_reserve() [clone .cold]+0x22>
  22:	48 89 d9             	mov    rcx,rbx
  25:	e8 00 00 00 00       	call   2a <push_no_reserve() [clone .cold]+0x2a>
  2a:	90                   	nop

000000000000002b <push_reserved() [clone .cold]>:
  2b:	48 8d 0d 00 00 00 00 	lea    rcx,[rip+0x0]        # 32 <push_reserved() [clone .cold]+0x7>
  32:	e8 00 00 00 00       	call   37 <push_reserved() [clone .cold]+0xc>
  37:	48 89 c3             	mov    rbx,rax
  3a:	4d 85 e4             	test   r12,r12
  3d:	74 0e                	je     4d <push_reserved() [clone .cold]+0x22>
  3f:	48 89 ea             	mov    rdx,rbp
  42:	4c 89 e1             	mov    rcx,r12
  45:	4c 29 e2             	sub    rdx,r12
  48:	e8 00 00 00 00       	call   4d <push_reserved() [clone .cold]+0x22>
  4d:	48 89 d9             	mov    rcx,rbx
  50:	e8 00 00 00 00       	call   55 <push_reserved() [clone .cold]+0x2a>
  55:	90                   	nop
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
   0:	48 83 ec 28          	sub    rsp,0x28
   4:	e8 00 00 00 00       	call   9 <main+0x9>
   9:	e8 00 00 00 00       	call   e <main+0xe>
   e:	e8 30 01 00 00       	call   143 <push_reserved()+0x13>
  13:	31 c0                	xor    eax,eax
  15:	48 83 c4 28          	add    rsp,0x28
  19:	c3                   	ret
  1a:	90                   	nop
  1b:	90                   	nop
  1c:	90                   	nop
  1d:	90                   	nop
  1e:	90                   	nop
  1f:	90                   	nop
