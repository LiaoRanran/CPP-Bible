	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z18push_after_reservev
	.def	_Z18push_after_reservev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z18push_after_reservev
_Z18push_after_reservev:
.LFB1715:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 12
	call	_Znwy
	mov	edx, 12
	mov	rcx, rax
	mov	rax, QWORD PTR .LC0[rip]
	mov	DWORD PTR 8[rcx], 3
	mov	QWORD PTR [rcx], rax
	add	rsp, 40
	jmp	_ZdlPvy
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "vector::_M_realloc_insert\0"
	.text
	.p2align 4
	.globl	_Z27observe_capacity_after_pushRSt6vectorIiSaIiEE
	.def	_Z27observe_capacity_after_pushRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z27observe_capacity_after_pushRSt6vectorIiSaIiEE
_Z27observe_capacity_after_pushRSt6vectorIiSaIiEE:
.LFB1738:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	cmp	rax, QWORD PTR 16[rcx]
	mov	rbx, rcx
	je	.L4
	mov	DWORD PTR [rax], 42
	add	rax, 4
	mov	QWORD PTR 8[rcx], rax
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	mov	rbp, QWORD PTR [rcx]
	mov	rdi, rax
	movabs	rcx, 2305843009213693951
	sub	rdi, rbp
	mov	rdx, rdi
	sar	rdx, 2
	cmp	rdx, rcx
	je	.L21
	cmp	rax, rbp
	je	.L22
	lea	rax, [rdx+rdx]
	cmp	rax, rdx
	jb	.L16
	test	rax, rax
	jne	.L23
	xor	esi, esi
	xor	ecx, ecx
.L11:
	lea	rax, 4[rcx+rdi]
	movq	xmm6, rcx
	test	rdi, rdi
	mov	DWORD PTR [rcx+rdi], 42
	movq	xmm0, rax
	punpcklqdq	xmm6, xmm0
	jg	.L24
	test	rbp, rbp
	jne	.L25
.L14:
	movups	XMMWORD PTR [rbx], xmm6
	mov	QWORD PTR 16[rbx], rsi
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L24:
	mov	rdx, rbp
	mov	r8, rdi
	call	memmove
	mov	rdx, QWORD PTR 16[rbx]
	sub	rdx, rbp
.L13:
	mov	rcx, rbp
	call	_ZdlPvy
	jmp	.L14
	.p2align 4,,10
	.p2align 3
.L22:
	add	rdx, 1
	jc	.L16
	movabs	rax, 2305843009213693951
	cmp	rdx, rax
	cmovbe	rax, rdx
	mov	rsi, rax
	sal	rsi, 2
.L10:
	mov	rcx, rsi
	call	_Znwy
	mov	rcx, rax
	add	rsi, rax
	jmp	.L11
	.p2align 4,,10
	.p2align 3
.L16:
	movabs	rsi, 9223372036854775804
	jmp	.L10
	.p2align 4,,10
	.p2align 3
.L25:
	mov	rdx, QWORD PTR 16[rbx]
	sub	rdx, rbp
	jmp	.L13
.L23:
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	cmova	rax, rdx
	lea	rsi, 0[0+rax*4]
	jmp	.L10
.L21:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	1
	.long	2
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
