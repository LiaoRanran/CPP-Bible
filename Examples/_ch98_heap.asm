	.file	"_ch98_heap.cpp"
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
	.globl	_Z7do_pushRSt6vectorIiSaIiEEi
	.def	_Z7do_pushRSt6vectorIiSaIiEEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7do_pushRSt6vectorIiSaIiEEi
_Z7do_pushRSt6vectorIiSaIiEEi:
.LFB2347:
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
	.def	_Z7do_pushRSt6vectorIiSaIiEEi.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z7do_pushRSt6vectorIiSaIiEEi.cold
	.seh_stackalloc	72
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_endprologue
_Z7do_pushRSt6vectorIiSaIiEEi.cold:
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
	.globl	_Z6do_popRSt6vectorIiSaIiEE
	.def	_Z6do_popRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6do_popRSt6vectorIiSaIiEE
_Z6do_popRSt6vectorIiSaIiEE:
.LFB2348:
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
	mov	r10, QWORD PTR 8[rcx]
	mov	rax, r10
	lea	rbx, -4[r10]
	mov	r9, rcx
	mov	rcx, QWORD PTR [rcx]
	sub	rax, rcx
	cmp	rax, 4
	jg	.L42
.L22:
	mov	eax, DWORD PTR -4[r10]
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
	mov	eax, DWORD PTR [rcx]
	mov	rdi, rbx
	mov	r11d, DWORD PTR -4[r10]
	sub	rdi, rcx
	mov	DWORD PTR -4[r10], eax
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
	lea	rdx, 1[rsi]
	lea	rax, [rdx+rdx]
	lea	rdx, [rcx+rdx*8]
	lea	rdi, -1[rax]
	mov	r8d, DWORD PTR [rdx]
	lea	rbp, [rcx+rdi*4]
	mov	r12d, DWORD PTR 0[rbp]
	cmp	r12d, r8d
	cmovg	r8d, r12d
	cmovg	rax, rdi
	cmovg	rdx, rbp
	mov	DWORD PTR [rcx+rsi*4], r8d
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
	mov	DWORD PTR [rdx], esi
	shr	rax, 63
	lea	rdx, -1[rax+r8]
	mov	rax, r8
	test	r8, r8
	je	.L43
	sar	rdx
	mov	r8, rdx
.L33:
	lea	rdi, [rcx+r8*4]
	lea	rdx, [rcx+rax*4]
	mov	esi, DWORD PTR [rdi]
	cmp	esi, r11d
	jl	.L44
.L28:
	mov	DWORD PTR [rdx], r11d
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
	mov	r8d, DWORD PTR [rcx+rsi*4]
	mov	DWORD PTR [rdx], r8d
	mov	r8, rax
	mov	rax, rsi
	jmp	.L33
	.p2align 4,,10
	.p2align 3
.L43:
	mov	rdx, rdi
	mov	DWORD PTR [rdx], r11d
	jmp	.L22
	.p2align 4,,10
	.p2align 3
.L23:
	and	r14d, 1
	mov	rdx, rcx
	jne	.L28
	cmp	rdi, 8
	jne	.L28
	xor	eax, eax
	jmp	.L31
	.seh_endproc
	.p2align 4
	.globl	_Z7do_makeRSt6vectorIiSaIiEE
	.def	_Z7do_makeRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7do_makeRSt6vectorIiSaIiEE
_Z7do_makeRSt6vectorIiSaIiEE:
.LFB2349:
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
	mov	rax, rcx
	mov	rcx, QWORD PTR [rcx]
	mov	rsi, QWORD PTR 8[rax]
	sub	rsi, rcx
	cmp	rsi, 4
	jle	.L45
	sar	rsi, 2
	lea	rdi, -2[rsi]
	lea	r11, -1[rsi]
	shr	rdi, 63
	sar	r11
	lea	rdi, -2[rsi+rdi]
	sar	rdi
	lea	rbx, [rcx+rdi*4]
	mov	r9, rdi
	mov	r10d, DWORD PTR [rbx]
	mov	rdx, rbx
	cmp	r9, r11
	jge	.L47
	.p2align 4
	.p2align 3
.L69:
	mov	rbp, r9
	jmp	.L49
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L59:
	mov	rbp, rax
.L49:
	lea	rdx, 1[rbp]
	lea	rax, [rdx+rdx]
	lea	rdx, [rcx+rdx*8]
	lea	r12, -1[rax]
	mov	r8d, DWORD PTR [rdx]
	lea	r13, [rcx+r12*4]
	mov	r14d, DWORD PTR 0[r13]
	cmp	r14d, r8d
	cmovg	r8d, r14d
	cmovg	rax, r12
	cmovg	rdx, r13
	mov	DWORD PTR [rcx+rbp*4], r8d
	cmp	r11, rax
	jg	.L59
	test	sil, 1
	jne	.L66
	cmp	rdi, rax
	je	.L61
.L66:
	lea	rbp, -1[rax]
	mov	r8, rbp
	shr	r8, 63
	add	r8, rbp
	sar	r8
	cmp	r9, rax
	jge	.L53
	lea	r12, 0[0+rax*4]
	jmp	.L56
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L68:
	mov	DWORD PTR [rdx], eax
	lea	rax, -1[r8]
	shr	rax, 63
	lea	rdx, -1[rax+r8]
	cmp	r8, r9
	jle	.L67
	sar	rdx
	lea	r12, 0[0+r8*4]
	mov	r8, rdx
.L56:
	lea	rbp, [rcx+r8*4]
	lea	rdx, [rcx+r12]
	mov	eax, DWORD PTR 0[rbp]
	cmp	r10d, eax
	jg	.L68
.L53:
	mov	DWORD PTR [rdx], r10d
	test	r9, r9
	je	.L45
.L70:
	sub	rbx, 4
.L55:
	sub	r9, 1
	mov	r10d, DWORD PTR [rbx]
	mov	rdx, rbx
	cmp	r9, r11
	jl	.L69
.L47:
	test	sil, 1
	jne	.L53
	cmp	r9, rdi
	jne	.L53
	mov	r8, r9
	jmp	.L52
	.p2align 4,,10
	.p2align 3
.L67:
	mov	rdx, rbp
	mov	DWORD PTR [rdx], r10d
	test	r9, r9
	jne	.L70
.L45:
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L61:
	mov	r8, rdi
.L52:
	lea	rax, 1[r8+r8]
	lea	r12, 0[0+rax*4]
	lea	rbp, [rcx+r12]
	mov	r13d, DWORD PTR 0[rbp]
	mov	DWORD PTR [rdx], r13d
	cmp	r9, rax
	jl	.L56
	mov	DWORD PTR 0[rbp], r10d
	sub	rbx, 4
	jmp	.L55
	.seh_endproc
	.p2align 4
	.globl	_Z7do_sortRSt6vectorIiSaIiEE
	.def	_Z7do_sortRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7do_sortRSt6vectorIiSaIiEE
_Z7do_sortRSt6vectorIiSaIiEE:
.LFB2350:
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
	mov	r10, QWORD PTR 8[rcx]
	mov	rdx, QWORD PTR [rcx]
	mov	rax, r10
	sub	r10, 4
	sub	rax, rdx
	cmp	rax, 4
	jle	.L71
	.p2align 4
	.p2align 3
.L86:
	mov	r11, r10
	mov	eax, DWORD PTR [rdx]
	mov	r9d, DWORD PTR [r10]
	sub	r11, rdx
	mov	r13, r11
	mov	DWORD PTR [r10], eax
	sar	r13, 2
	cmp	r11, 8
	jle	.L73
	lea	r12, -1[r13]
	xor	ebx, ebx
	sar	r12
	jmp	.L75
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L88:
	mov	rbx, rax
.L75:
	lea	rcx, 1[rbx]
	lea	rax, [rcx+rcx]
	lea	r8, [rdx+rcx*8]
	lea	rsi, -1[rax]
	mov	ecx, DWORD PTR [r8]
	lea	rdi, [rdx+rsi*4]
	mov	ebp, DWORD PTR [rdi]
	cmp	ebp, ecx
	cmovg	ecx, ebp
	cmovg	rax, rsi
	cmovg	r8, rdi
	mov	DWORD PTR [rdx+rbx*4], ecx
	cmp	r12, rax
	jg	.L88
	and	r13d, 1
	jne	.L94
	mov	rcx, r11
	sar	rcx, 3
	sub	rcx, 1
	cmp	rcx, rax
	je	.L81
.L94:
	lea	rcx, -1[rax]
	shr	rcx, 63
	lea	rcx, -1[rax+rcx]
	sar	rcx
	test	rax, rax
	jne	.L84
	jmp	.L96
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L98:
	mov	DWORD PTR [rax], r8d
	lea	rax, -1[rcx]
	shr	rax, 63
	lea	r8, -1[rax+rcx]
	mov	rax, rcx
	test	rcx, rcx
	je	.L97
	mov	rcx, r8
	sar	rcx
.L84:
	lea	rbx, [rdx+rcx*4]
	lea	rax, [rdx+rax*4]
	mov	r8d, DWORD PTR [rbx]
	cmp	r9d, r8d
	jg	.L98
.L78:
	mov	DWORD PTR [rax], r9d
	cmp	r11, 4
	jle	.L71
.L93:
	sub	r10, 4
	jmp	.L86
	.p2align 4,,10
	.p2align 3
.L97:
	mov	rax, rbx
	mov	DWORD PTR [rax], r9d
	cmp	r11, 4
	jg	.L93
.L71:
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L73:
	and	r13d, 1
	jne	.L95
	cmp	r11, 8
	jne	.L95
	mov	r8, rdx
	xor	eax, eax
	.p2align 4
	.p2align 3
.L81:
	lea	rbx, 1[rax+rax]
	mov	ecx, DWORD PTR [rdx+rbx*4]
	mov	DWORD PTR [r8], ecx
	mov	rcx, rax
	mov	rax, rbx
	jmp	.L84
.L95:
	mov	rax, rdx
	jmp	.L78
.L96:
	mov	DWORD PTR [r8], r9d
	jmp	.L93
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
