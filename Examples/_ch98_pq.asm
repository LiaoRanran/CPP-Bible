	.file	"_ch98_pq.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_append\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	_Z7pq_pushRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEEi
	.def	_Z7pq_pushRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7pq_pushRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEEi
_Z7pq_pushRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEEi:
.LFB4270:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	rbx, QWORD PTR 16[rcx]
	mov	r9, QWORD PTR [rcx]
	mov	r10d, edx
	cmp	rax, rbx
	je	.L2
	mov	DWORD PTR [rax], edx
	add	rax, 4
	mov	QWORD PTR 8[rcx], rax
.L3:
	sub	rax, r9
	mov	rdx, rax
	sar	rax, 2
	lea	rcx, -1[rax]
	test	rcx, rcx
	jle	.L7
	sub	rax, 2
	sar	rax
	jmp	.L9
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L20:
	mov	DWORD PTR [rcx], edx
	lea	rdx, -1[rax]
	mov	rcx, rax
	shr	rdx, 63
	test	rax, rax
	je	.L19
	lea	rax, -1[rax+rdx]
	sar	rax
.L9:
	lea	r8, [r9+rax*4]
	lea	rcx, [r9+rcx*4]
	mov	edx, DWORD PTR [r8]
	cmp	r10d, edx
	jg	.L20
.L8:
	mov	DWORD PTR [rcx], r10d
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	mov	rcx, r8
	mov	DWORD PTR [rcx], r10d
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L2:
	sub	rax, r9
	mov	rdx, rax
	mov	r8, rax
	movabs	rax, 2305843009213693951
	sar	rdx, 2
	cmp	rdx, rax
	je	.L17
	test	rdx, rdx
	mov	eax, 1
	mov	QWORD PTR 80[rsp], rcx
	cmovne	rax, rdx
	mov	DWORD PTR 88[rsp], r10d
	mov	QWORD PTR 40[rsp], r9
	add	rax, rdx
	mov	QWORD PTR 32[rsp], r8
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	cmova	rax, rdx
	lea	rcx, 0[0+rax*4]
	lea	rdi, 0[0+rax*4]
	call	_Znwy
	mov	r8, QWORD PTR 32[rsp]
	mov	r10d, DWORD PTR 88[rsp]
	mov	r9, QWORD PTR 40[rsp]
	mov	r11, QWORD PTR 80[rsp]
	mov	rsi, rax
	mov	rcx, rax
	test	r8, r8
	mov	DWORD PTR [rax+r8], r10d
	je	.L5
	mov	rdx, r9
	mov	QWORD PTR 40[rsp], r8
	mov	QWORD PTR 32[rsp], r9
	call	memcpy
	mov	r11, QWORD PTR 80[rsp]
	mov	r8, QWORD PTR 40[rsp]
	mov	r9, QWORD PTR 32[rsp]
.L5:
	lea	rax, 4[rsi+r8]
	test	r9, r9
	je	.L6
	sub	rbx, r9
	mov	rcx, r9
	mov	QWORD PTR 80[rsp], r11
	mov	rdx, rbx
	mov	QWORD PTR 32[rsp], rax
	call	_ZdlPvy
	mov	r11, QWORD PTR 80[rsp]
	mov	rax, QWORD PTR 32[rsp]
.L6:
	lea	rdx, [rsi+rdi]
	mov	QWORD PTR [r11], rsi
	mov	r10d, DWORD PTR -4[rax]
	mov	r9, rsi
	mov	QWORD PTR 8[r11], rax
	mov	QWORD PTR 16[r11], rdx
	jmp	.L3
.L7:
	lea	rcx, -4[r9+rdx]
	jmp	.L8
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z7pq_pushRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEEi.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z7pq_pushRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEEi.cold
	.seh_stackalloc	72
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_endprologue
_Z7pq_pushRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEEi.cold:
.L17:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.p2align 4
	.globl	_Z10pq_top_popRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEE
	.def	_Z10pq_top_popRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10pq_top_popRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEE
_Z10pq_top_popRSt14priority_queueIiSt6vectorIiSaIiEESt4lessIiEE:
.LFB4271:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	rdx, QWORD PTR [rcx]
	lea	rbx, -4[rax]
	mov	r11d, DWORD PTR [rdx]
	mov	r9, rcx
	mov	rcx, rax
	sub	rcx, rdx
	cmp	rcx, 4
	jg	.L42
.L22:
	mov	eax, r11d
	mov	QWORD PTR 8[r9], rbx
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L42:
	mov	rdi, rbx
	mov	r10d, DWORD PTR -4[rax]
	mov	DWORD PTR -4[rax], r11d
	sub	rdi, rdx
	mov	rax, rdi
	mov	r15, rdi
	sar	rax, 2
	mov	r14, rax
	cmp	rdi, 8
	jle	.L23
	lea	r13, -1[rax]
	xor	esi, esi
	sar	r13
	jmp	.L25
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L34:
	mov	rsi, rax
.L25:
	lea	rcx, 1[rsi]
	lea	rax, [rcx+rcx]
	lea	rcx, [rdx+rcx*8]
	lea	rdi, -1[rax]
	mov	r8d, DWORD PTR [rcx]
	lea	rbp, [rdx+rdi*4]
	mov	r12d, DWORD PTR 0[rbp]
	cmp	r12d, r8d
	cmovg	r8d, r12d
	cmovg	rax, rdi
	cmovg	rcx, rbp
	mov	DWORD PTR [rdx+rsi*4], r8d
	cmp	r13, rax
	jg	.L34
	and	r14d, 1
	je	.L29
.L41:
	lea	r8, -1[rax]
	shr	r8, 63
	lea	r8, -1[rax+r8]
	sar	r8
	test	rax, rax
	jne	.L33
	jmp	.L28
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L44:
	lea	rax, -1[r8]
	mov	DWORD PTR [rcx], esi
	shr	rax, 63
	lea	rcx, -1[rax+r8]
	mov	rax, r8
	test	r8, r8
	je	.L43
	sar	rcx
	mov	r8, rcx
.L33:
	lea	rdi, [rdx+r8*4]
	lea	rcx, [rdx+rax*4]
	mov	esi, DWORD PTR [rdi]
	cmp	r10d, esi
	jg	.L44
.L28:
	mov	DWORD PTR [rcx], r10d
	jmp	.L22
	.p2align 4,,10
	.p2align 3
.L29:
	mov	r8, r15
	sar	r8, 3
	sub	r8, 1
	cmp	r8, rax
	jne	.L41
.L31:
	lea	rsi, 1[rax+rax]
	mov	r8d, DWORD PTR [rdx+rsi*4]
	mov	DWORD PTR [rcx], r8d
	mov	r8, rax
	mov	rax, rsi
	jmp	.L33
	.p2align 4,,10
	.p2align 3
.L43:
	mov	rcx, rdi
	mov	DWORD PTR [rcx], r10d
	jmp	.L22
	.p2align 4,,10
	.p2align 3
.L23:
	and	r14d, 1
	mov	rcx, rdx
	jne	.L28
	cmp	rdi, 8
	jne	.L28
	xor	eax, eax
	jmp	.L31
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
