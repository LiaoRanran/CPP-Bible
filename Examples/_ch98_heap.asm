	.file	"_ch98_heap.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_insert\0"
	.text
	.p2align 4
	.globl	_Z7do_pushRSt6vectorIiSaIiEEi
	.def	_Z7do_pushRSt6vectorIiSaIiEEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7do_pushRSt6vectorIiSaIiEEi
_Z7do_pushRSt6vectorIiSaIiEEi:
.LFB2389:
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
	sub	rsp, 48
	.seh_stackalloc	48
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	cmp	rax, QWORD PTR 16[rcx]
	mov	rbx, QWORD PTR [rcx]
	mov	rbp, rcx
	mov	esi, edx
	je	.L2
	lea	rdi, 4[rax]
	mov	DWORD PTR [rax], edx
	mov	QWORD PTR 8[rcx], rdi
.L3:
	mov	rax, rdi
	sub	rax, rbx
	mov	r8, rax
	sar	r8, 2
	lea	rcx, -1[r8]
	sub	r8, 2
	mov	rdx, r8
	shr	rdx, 63
	add	rdx, r8
	sar	rdx
	test	rcx, rcx
	jg	.L15
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L26:
	mov	DWORD PTR [rcx], eax
	lea	rcx, -1[rdx]
	mov	rax, rcx
	shr	rax, 63
	add	rax, rcx
	mov	rcx, rdx
	sar	rax
	test	rdx, rdx
	je	.L25
	mov	rdx, rax
.L15:
	lea	r8, [rbx+rdx*4]
	mov	eax, DWORD PTR [r8]
	lea	rcx, [rbx+rcx*4]
	cmp	eax, esi
	jl	.L26
.L14:
	mov	DWORD PTR [rcx], esi
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 48
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
.L25:
	mov	rcx, r8
	jmp	.L14
	.p2align 4,,10
	.p2align 3
.L2:
	movabs	rcx, 2305843009213693951
	mov	r14, rax
	sub	r14, rbx
	mov	rdx, r14
	sar	rdx, 2
	cmp	rdx, rcx
	je	.L27
	cmp	rax, rbx
	je	.L28
	lea	rax, [rdx+rdx]
	cmp	rax, rdx
	jb	.L17
	test	rax, rax
	jne	.L29
	xor	r13d, r13d
	xor	r12d, r12d
.L9:
	lea	rdi, 4[r12+r14]
	movq	xmm6, r12
	test	r14, r14
	mov	DWORD PTR [r12+r14], esi
	movq	xmm0, rdi
	punpcklqdq	xmm6, xmm0
	jg	.L30
	test	rbx, rbx
	jne	.L31
.L12:
	mov	esi, DWORD PTR -4[rdi]
	movups	XMMWORD PTR 0[rbp], xmm6
	mov	rbx, r12
	mov	QWORD PTR 16[rbp], r13
	jmp	.L3
.L30:
	mov	rdx, rbx
	mov	r8, r14
	mov	rcx, r12
	call	memmove
	mov	rdx, QWORD PTR 16[rbp]
	sub	rdx, rbx
.L11:
	mov	rcx, rbx
	call	_ZdlPvy
	jmp	.L12
.L28:
	add	rdx, 1
	jc	.L17
	movabs	rax, 2305843009213693951
	cmp	rdx, rax
	cmova	rdx, rax
	lea	r13, 0[0+rdx*4]
.L8:
	mov	rcx, r13
	call	_Znwy
	mov	r12, rax
	add	r13, rax
	jmp	.L9
.L24:
	lea	rcx, -4[rbx+rax]
	jmp	.L14
.L17:
	movabs	r13, 9223372036854775804
	jmp	.L8
.L31:
	mov	rdx, QWORD PTR 16[rbp]
	sub	rdx, rbx
	jmp	.L11
.L27:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.L29:
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	cmovbe	rdx, rax
	mov	r13, rdx
	sal	r13, 2
	jmp	.L8
	.seh_endproc
	.p2align 4
	.globl	_Z6do_popRSt6vectorIiSaIiEE
	.def	_Z6do_popRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6do_popRSt6vectorIiSaIiEE
_Z6do_popRSt6vectorIiSaIiEE:
.LFB2390:
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
	mov	rdx, QWORD PTR [rcx]
	lea	rbx, -4[r10]
	mov	rax, r10
	mov	r9, rcx
	sub	rax, rdx
	cmp	rax, 4
	jg	.L55
.L33:
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
.L55:
	mov	eax, DWORD PTR [rdx]
	mov	r11d, DWORD PTR -4[r10]
	mov	DWORD PTR -4[r10], eax
	mov	rax, rbx
	sub	rax, rdx
	mov	r13, rax
	sar	r13, 2
	lea	rcx, -1[r13]
	mov	r14, r13
	mov	r12, rcx
	and	r14d, 1
	shr	r12, 63
	add	r12, rcx
	sar	r12
	cmp	rax, 8
	jle	.L34
	xor	esi, esi
	jmp	.L36
	.p2align 4,,10
	.p2align 3
.L44:
	mov	rsi, rax
.L36:
	lea	rcx, 1[rsi]
	lea	rax, [rcx+rcx]
	lea	rdi, -1[rax]
	lea	rbp, [rdx+rdi*4]
	lea	rcx, [rdx+rcx*8]
	mov	r15d, DWORD PTR 0[rbp]
	mov	r8d, DWORD PTR [rcx]
	cmp	r15d, r8d
	jle	.L35
	mov	r8d, r15d
	mov	rcx, rbp
	mov	rax, rdi
.L35:
	cmp	rax, r12
	mov	DWORD PTR [rdx+rsi*4], r8d
	jl	.L44
	test	r14, r14
	je	.L38
.L54:
	lea	rsi, -1[rax]
	mov	r8, rsi
	shr	r8, 63
	add	r8, rsi
	sar	r8
	test	rax, rax
	jne	.L43
	jmp	.L39
	.p2align 4,,10
	.p2align 3
.L57:
	mov	DWORD PTR [rcx], esi
	lea	rcx, -1[r8]
	mov	rax, rcx
	shr	rax, 63
	add	rax, rcx
	sar	rax
	test	r8, r8
	mov	rcx, rax
	mov	rax, r8
	je	.L56
	mov	r8, rcx
.L43:
	lea	rdi, [rdx+r8*4]
	mov	esi, DWORD PTR [rdi]
	lea	rcx, [rdx+rax*4]
	cmp	esi, r11d
	jl	.L57
.L39:
	mov	DWORD PTR [rcx], r11d
	jmp	.L33
	.p2align 4,,10
	.p2align 3
.L34:
	test	r14, r14
	mov	rcx, rdx
	jne	.L39
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L38:
	sub	r13, 2
	mov	r8, r13
	shr	r8, 63
	add	r8, r13
	sar	r8
	cmp	r8, rax
	jne	.L54
	lea	rsi, 1[rax+rax]
	mov	r8d, DWORD PTR [rdx+rsi*4]
	mov	DWORD PTR [rcx], r8d
	mov	r8, rax
	mov	rax, rsi
	jmp	.L43
	.p2align 4,,10
	.p2align 3
.L56:
	mov	rcx, rdi
	mov	DWORD PTR [rcx], r11d
	jmp	.L33
	.seh_endproc
	.p2align 4
	.globl	_Z7do_makeRSt6vectorIiSaIiEE
	.def	_Z7do_makeRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7do_makeRSt6vectorIiSaIiEE
_Z7do_makeRSt6vectorIiSaIiEE:
.LFB2391:
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
	mov	r8, QWORD PTR [rcx]
	mov	rdi, QWORD PTR 8[rcx]
	sub	rdi, r8
	cmp	rdi, 4
	jle	.L58
	sar	rdi, 2
	lea	rax, -2[rdi]
	lea	rbx, -1[rdi]
	mov	rbp, rax
	not	rdi
	shr	rbp, 63
	sar	rbx
	and	edi, 1
	add	rbp, rax
	sar	rbp
	lea	rsi, [r8+rbp*4]
	mov	r10, rbp
	cmp	rbx, r10
	mov	r11d, DWORD PTR [rsi]
	mov	rdx, rsi
	jle	.L69
	.p2align 4,,10
	.p2align 3
.L81:
	mov	r9, r10
	jmp	.L62
	.p2align 4,,10
	.p2align 3
.L70:
	mov	r9, rax
.L62:
	lea	rdx, 1[r9]
	lea	rax, [rdx+rdx]
	lea	r12, -1[rax]
	lea	r13, [r8+r12*4]
	lea	rdx, [r8+rdx*8]
	mov	r14d, DWORD PTR 0[r13]
	mov	ecx, DWORD PTR [rdx]
	cmp	r14d, ecx
	jle	.L61
	mov	ecx, r14d
	mov	rdx, r13
	mov	rax, r12
.L61:
	cmp	rbx, rax
	mov	DWORD PTR [r8+r9*4], ecx
	jg	.L70
.L60:
	cmp	rbp, rax
	jne	.L72
	test	dil, dil
	jne	.L63
.L72:
	lea	r9, -1[rax]
	mov	rcx, r9
	shr	rcx, 63
	add	rcx, r9
	sar	rcx
.L65:
	cmp	r10, rax
	jl	.L67
	jmp	.L66
	.p2align 4,,10
	.p2align 3
.L80:
	mov	DWORD PTR [rdx], r9d
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	rcx, r10
	mov	rdx, rax
	mov	rax, rcx
	jle	.L79
	mov	rcx, rdx
.L67:
	lea	r12, [r8+rcx*4]
	mov	r9d, DWORD PTR [r12]
	lea	rdx, [r8+rax*4]
	cmp	r11d, r9d
	jg	.L80
.L66:
	sub	rsi, 4
	test	r10, r10
	mov	DWORD PTR [rdx], r11d
	je	.L58
.L82:
	sub	r10, 1
	mov	r11d, DWORD PTR [rsi]
	mov	rdx, rsi
	cmp	rbx, r10
	jg	.L81
.L69:
	mov	rax, r10
	jmp	.L60
	.p2align 4,,10
	.p2align 3
.L79:
	mov	rdx, r12
	sub	rsi, 4
	test	r10, r10
	mov	DWORD PTR [rdx], r11d
	jne	.L82
.L58:
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
.L63:
	lea	r9, 1[rax+rax]
	lea	rcx, [r8+r9*4]
	mov	r12d, DWORD PTR [rcx]
	mov	DWORD PTR [rdx], r12d
	mov	rdx, rcx
	mov	rcx, rax
	mov	rax, r9
	jmp	.L65
	.seh_endproc
	.p2align 4
	.globl	_Z7do_sortRSt6vectorIiSaIiEE
	.def	_Z7do_sortRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7do_sortRSt6vectorIiSaIiEE
_Z7do_sortRSt6vectorIiSaIiEE:
.LFB2392:
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
	mov	rcx, QWORD PTR [rcx]
	mov	rax, r10
	sub	r10, 4
	sub	rax, rcx
	cmp	rax, 4
	jle	.L83
	.p2align 4,,10
	.p2align 3
.L97:
	mov	eax, DWORD PTR [rcx]
	mov	r11, r10
	sub	r11, rcx
	mov	r9d, DWORD PTR [r10]
	mov	r13, r11
	sar	r13, 2
	mov	DWORD PTR [r10], eax
	lea	rax, -1[r13]
	mov	r14, r13
	mov	r12, rax
	and	r14d, 1
	shr	r12, 63
	add	r12, rax
	sar	r12
	cmp	r11, 8
	jle	.L85
	xor	ebx, ebx
	jmp	.L87
	.p2align 4,,10
	.p2align 3
.L99:
	mov	rbx, rax
.L87:
	lea	rdx, 1[rbx]
	lea	rax, [rdx+rdx]
	lea	rsi, -1[rax]
	lea	rdi, [rcx+rsi*4]
	lea	rdx, [rcx+rdx*8]
	mov	ebp, DWORD PTR [rdi]
	mov	r8d, DWORD PTR [rdx]
	cmp	ebp, r8d
	jle	.L86
	mov	r8d, ebp
	mov	rdx, rdi
	mov	rax, rsi
.L86:
	cmp	r12, rax
	mov	DWORD PTR [rcx+rbx*4], r8d
	jg	.L99
	test	r14, r14
	je	.L91
	lea	rbx, -1[rax]
	mov	r8, rbx
	shr	r8, 63
	add	r8, rbx
	sar	r8
	test	rax, rax
	jne	.L95
	jmp	.L105
	.p2align 4,,10
	.p2align 3
.L107:
	mov	DWORD PTR [rdx], ebx
	lea	rdx, -1[r8]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	test	r8, r8
	mov	rdx, rax
	mov	rax, r8
	je	.L106
	mov	r8, rdx
.L95:
	lea	rsi, [rcx+r8*4]
	mov	ebx, DWORD PTR [rsi]
	lea	rdx, [rcx+rax*4]
	cmp	r9d, ebx
	jg	.L107
.L90:
	sub	r10, 4
	cmp	r11, 4
	mov	DWORD PTR [rdx], r9d
	jg	.L97
.L83:
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
.L106:
	mov	rdx, rsi
	sub	r10, 4
	cmp	r11, 4
	mov	DWORD PTR [rdx], r9d
	jg	.L97
	jmp	.L83
	.p2align 4,,10
	.p2align 3
.L91:
	lea	r8, -2[r13]
	sar	r8
	cmp	r8, rax
	je	.L94
	lea	rbx, -1[rax]
	mov	r8, rbx
	shr	r8, 63
	add	r8, rbx
	sar	r8
	test	rax, rax
	jne	.L95
	jmp	.L90
	.p2align 4,,10
	.p2align 3
.L85:
	test	r14, r14
	mov	rdx, rcx
	jne	.L90
	cmp	rax, 2
	ja	.L90
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L94:
	lea	rbx, 1[rax+rax]
	mov	r8d, DWORD PTR [rcx+rbx*4]
	mov	DWORD PTR [rdx], r8d
	mov	r8, rax
	mov	rax, rbx
	jmp	.L95
.L105:
	mov	DWORD PTR [rdx], r9d
	sub	r10, 4
	jmp	.L97
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
