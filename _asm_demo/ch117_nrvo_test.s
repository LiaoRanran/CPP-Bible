
ch117_nrvo_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <make_prvalue()>:
   0:	48 89 c8             	mov    rax,rcx
   3:	c7 01 2a 00 00 00    	mov    DWORD PTR [rcx],0x2a
   9:	c3                   	ret
   a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000000010 <make_nrvo()>:
  10:	48 89 c8             	mov    rax,rcx
  13:	c7 01 07 00 00 00    	mov    DWORD PTR [rcx],0x7
  19:	c3                   	ret
  1a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000000020 <make_nrvo_fail(bool)>:
  20:	53                   	push   rbx
  21:	48 83 ec 20          	sub    rsp,0x20
  25:	48 89 cb             	mov    rbx,rcx
  28:	84 d2                	test   dl,dl
  2a:	74 24                	je     50 <make_nrvo_fail(bool)+0x30>
  2c:	c7 01 01 00 00 00    	mov    DWORD PTR [rcx],0x1
  32:	48 8d 0d 00 00 00 00 	lea    rcx,[rip+0x0]        # 39 <make_nrvo_fail(bool)+0x19>
  39:	e8 00 00 00 00       	call   3e <make_nrvo_fail(bool)+0x1e>
  3e:	48 89 d8             	mov    rax,rbx
  41:	48 83 c4 20          	add    rsp,0x20
  45:	5b                   	pop    rbx
  46:	c3                   	ret
  47:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  4e:	00 00 
  50:	c7 01 02 00 00 00    	mov    DWORD PTR [rcx],0x2
  56:	48 8d 0d 00 00 00 00 	lea    rcx,[rip+0x0]        # 5d <make_nrvo_fail(bool)+0x3d>
  5d:	e8 00 00 00 00       	call   62 <make_nrvo_fail(bool)+0x42>
  62:	48 89 d8             	mov    rax,rbx
  65:	48 83 c4 20          	add    rsp,0x20
  69:	5b                   	pop    rbx
  6a:	c3                   	ret
  6b:	90                   	nop
  6c:	90                   	nop
  6d:	90                   	nop
  6e:	90                   	nop
  6f:	90                   	nop
