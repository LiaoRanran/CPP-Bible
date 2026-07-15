
ch47_vs_51_dispatch_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <v_dispatch(ShapeV const&)>:
   0:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   3:	48 ff 20             	rex.W jmp QWORD PTR [rax]
   6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   d:	00 00 00 

0000000000000010 <v_loop(ShapeV const* const*, int)>:
  10:	57                   	push   rdi
  11:	56                   	push   rsi
  12:	53                   	push   rbx
  13:	48 83 ec 20          	sub    rsp,0x20
  17:	85 d2                	test   edx,edx
  19:	7e 35                	jle    50 <v_loop(ShapeV const* const*, int)+0x40>
  1b:	48 63 d2             	movsxd rdx,edx
  1e:	48 89 cb             	mov    rbx,rcx
  21:	31 f6                	xor    esi,esi
  23:	48 8d 3c d1          	lea    rdi,[rcx+rdx*8]
  27:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  2e:	00 00 
  30:	48 8b 0b             	mov    rcx,QWORD PTR [rbx]
  33:	48 83 c3 08          	add    rbx,0x8
  37:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  3a:	ff 10                	call   QWORD PTR [rax]
  3c:	01 c6                	add    esi,eax
  3e:	48 39 fb             	cmp    rbx,rdi
  41:	75 ed                	jne    30 <v_loop(ShapeV const* const*, int)+0x20>
  43:	89 f0                	mov    eax,esi
  45:	48 83 c4 20          	add    rsp,0x20
  49:	5b                   	pop    rbx
  4a:	5e                   	pop    rsi
  4b:	5f                   	pop    rdi
  4c:	c3                   	ret
  4d:	0f 1f 00             	nop    DWORD PTR [rax]
  50:	31 f6                	xor    esi,esi
  52:	89 f0                	mov    eax,esi
  54:	48 83 c4 20          	add    rsp,0x20
  58:	5b                   	pop    rbx
  59:	5e                   	pop    rsi
  5a:	5f                   	pop    rdi
  5b:	c3                   	ret
  5c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000000060 <c_dispatch(CircC const&)>:
  60:	8b 01                	mov    eax,DWORD PTR [rcx]
  62:	0f af c0             	imul   eax,eax
  65:	c3                   	ret
  66:	90                   	nop
  67:	90                   	nop
  68:	90                   	nop
  69:	90                   	nop
  6a:	90                   	nop
  6b:	90                   	nop
  6c:	90                   	nop
  6d:	90                   	nop
  6e:	90                   	nop
  6f:	90                   	nop

Disassembly of section .text$_Z6c_loopI5CircCElPKT_i:

0000000000000000 <long c_loop<CircC>(CircC const*, int)>:
   0:	85 d2                	test   edx,edx
   2:	7e 24                	jle    28 <long c_loop<CircC>(CircC const*, int)+0x28>
   4:	48 63 d2             	movsxd rdx,edx
   7:	4c 8d 04 91          	lea    r8,[rcx+rdx*4]
   b:	31 d2                	xor    edx,edx
   d:	0f 1f 00             	nop    DWORD PTR [rax]
  10:	8b 01                	mov    eax,DWORD PTR [rcx]
  12:	48 83 c1 04          	add    rcx,0x4
  16:	0f af c0             	imul   eax,eax
  19:	01 c2                	add    edx,eax
  1b:	4c 39 c1             	cmp    rcx,r8
  1e:	75 f0                	jne    10 <long c_loop<CircC>(CircC const*, int)+0x10>
  20:	89 d0                	mov    eax,edx
  22:	c3                   	ret
  23:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
  28:	31 d2                	xor    edx,edx
  2a:	89 d0                	mov    eax,edx
  2c:	c3                   	ret
  2d:	90                   	nop
  2e:	90                   	nop
  2f:	90                   	nop

Disassembly of section .text$_Z6c_loopI5RectCElPKT_i:

0000000000000000 <long c_loop<RectC>(RectC const*, int)>:
   0:	85 d2                	test   edx,edx
   2:	7e 34                	jle    38 <long c_loop<RectC>(RectC const*, int)+0x38>
   4:	48 63 d2             	movsxd rdx,edx
   7:	4c 8d 04 d1          	lea    r8,[rcx+rdx*8]
   b:	31 d2                	xor    edx,edx
   d:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
  14:	00 
  15:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  1c:	00 00 00 00 
  20:	8b 01                	mov    eax,DWORD PTR [rcx]
  22:	0f af 41 04          	imul   eax,DWORD PTR [rcx+0x4]
  26:	48 83 c1 08          	add    rcx,0x8
  2a:	01 c2                	add    edx,eax
  2c:	49 39 c8             	cmp    r8,rcx
  2f:	75 ef                	jne    20 <long c_loop<RectC>(RectC const*, int)+0x20>
  31:	89 d0                	mov    eax,edx
  33:	c3                   	ret
  34:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  38:	31 d2                	xor    edx,edx
  3a:	89 d0                	mov    eax,edx
  3c:	c3                   	ret
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop
