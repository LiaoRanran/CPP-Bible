	.file	"_ch96_sort_asm.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0:
.LFB2539:
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
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rax, rdx
	mov	rsi, rcx
	mov	r11, rdx
	sub	rax, rcx
	mov	rdi, r8
	mov	rbp, rdx
	cmp	rax, 64
	jle	.L1
	lea	rbx, 4[rcx]
	test	r8, r8
	je	.L45
.L4:
	sar	rax, 3
	movq	xmm0, QWORD PTR [rsi]
	sub	rdi, 1
	lea	r9, [rsi+rax*4]
	mov	r8d, DWORD PTR -4[rbp]
	mov	eax, DWORD PTR [r9]
	pshufd	xmm2, xmm0, 0xe5
	movd	ecx, xmm2
	movd	edx, xmm0
	pshufd	xmm1, xmm0, 225
	cmp	ecx, eax
	jge	.L31
	cmp	eax, r8d
	jl	.L37
	cmp	ecx, r8d
	jl	.L66
.L34:
	movq	QWORD PTR [rsi], xmm1
	mov	r9d, DWORD PTR -4[rbp]
.L33:
	cmp	ecx, edx
	mov	r10, rbp
	mov	rax, rbx
	jle	.L55
	.p2align 4,,10
	.p2align 3
.L69:
	add	rax, 4
	.p2align 4,,10
	.p2align 3
.L39:
	mov	r11, rax
	mov	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	ecx, edx
	jg	.L39
	cmp	ecx, r9d
	jge	.L40
.L70:
	lea	rax, -8[r10]
	.p2align 4,,10
	.p2align 3
.L41:
	mov	r10, rax
	mov	r9d, DWORD PTR [rax]
	sub	rax, 4
	cmp	ecx, r9d
	jl	.L41
	cmp	r11, r10
	jnb	.L68
.L43:
	mov	DWORD PTR [r11], r9d
	lea	rax, 4[r11]
	mov	r9d, DWORD PTR -4[r10]
	mov	DWORD PTR [r10], edx
	mov	edx, DWORD PTR 4[r11]
	mov	ecx, DWORD PTR [rsi]
	cmp	ecx, edx
	jg	.L69
.L55:
	cmp	ecx, r9d
	mov	r11, rax
	jl	.L70
	.p2align 4,,10
	.p2align 3
.L40:
	sub	r10, 4
	cmp	r11, r10
	jb	.L43
	.p2align 4,,10
	.p2align 3
.L68:
	mov	rcx, r11
	mov	r8, rdi
	mov	rdx, rbp
	mov	QWORD PTR 40[rsp], r11
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	mov	r11, QWORD PTR 40[rsp]
	mov	rax, r11
	sub	rax, rsi
	cmp	rax, 64
	jle	.L1
	test	rdi, rdi
	je	.L45
	mov	rbp, r11
	jmp	.L4
.L31:
	cmp	ecx, r8d
	jl	.L34
	cmp	eax, r8d
	jge	.L37
.L66:
	mov	DWORD PTR [rsi], r8d
	mov	r9d, edx
	mov	DWORD PTR -4[rbp], edx
	mov	ecx, DWORD PTR [rsi]
	mov	edx, DWORD PTR 4[rsi]
	jmp	.L33
.L37:
	mov	DWORD PTR [rsi], eax
	mov	DWORD PTR [r9], edx
	mov	edx, DWORD PTR 4[rsi]
	mov	ecx, DWORD PTR [rsi]
	mov	r9d, DWORD PTR -4[rbp]
	jmp	.L33
.L15:
	sub	r11, 4
	.p2align 4,,10
	.p2align 3
.L30:
	mov	r9, r11
	mov	eax, DWORD PTR [rsi]
	sub	r9, rsi
	mov	r8d, DWORD PTR [r11]
	mov	r12, r9
	sar	r12, 2
	lea	rdx, -1[r12]
	mov	DWORD PTR [r11], eax
	mov	r14, r12
	mov	rax, rdx
	and	r14d, 1
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r9, 8
	mov	r13, rax
	jle	.L18
	xor	r10d, r10d
	jmp	.L20
	.p2align 4,,10
	.p2align 3
.L52:
	mov	r10, rax
.L20:
	lea	rdx, 1[r10]
	lea	rax, [rdx+rdx]
	lea	rbx, -1[rax]
	lea	rdi, [rsi+rbx*4]
	lea	rdx, [rsi+rdx*8]
	mov	ebp, DWORD PTR [rdi]
	mov	ecx, DWORD PTR [rdx]
	cmp	ebp, ecx
	jle	.L19
	mov	ecx, ebp
	mov	rdx, rdi
	mov	rax, rbx
.L19:
	cmp	rax, r13
	mov	DWORD PTR [rsi+r10*4], ecx
	jl	.L52
	test	r14, r14
	je	.L24
	lea	r10, -1[rax]
	mov	rcx, r10
	shr	rcx, 63
	add	rcx, r10
	sar	rcx
	test	rax, rax
	jne	.L28
	jmp	.L71
	.p2align 4,,10
	.p2align 3
.L73:
	mov	DWORD PTR [rdx], r10d
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	test	rcx, rcx
	mov	rdx, rax
	mov	rax, rcx
	je	.L72
	mov	rcx, rdx
.L28:
	lea	rbx, [rsi+rcx*4]
	mov	r10d, DWORD PTR [rbx]
	lea	rdx, [rsi+rax*4]
	cmp	r8d, r10d
	jg	.L73
.L23:
	sub	r11, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L30
.L1:
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L45:
	sar	rax, 2
	lea	rbp, -2[rax]
	lea	rbx, -1[rax]
	sar	rbp
	not	rax
	sar	rbx
	mov	r9d, eax
	mov	r8, rbp
	lea	rdi, [rsi+rbp*4]
	and	r9d, 1
	cmp	r8, rbx
	mov	r10d, DWORD PTR [rdi]
	mov	r12, rdi
	jge	.L49
.L77:
	mov	rcx, r8
	jmp	.L7
	.p2align 4,,10
	.p2align 3
.L50:
	mov	rcx, rax
.L7:
	lea	rdx, 1[rcx]
	lea	rax, [rdx+rdx]
	lea	r13, -1[rax]
	lea	r14, [rsi+r13*4]
	lea	r12, [rsi+rdx*8]
	mov	r15d, DWORD PTR [r14]
	mov	edx, DWORD PTR [r12]
	cmp	r15d, edx
	jle	.L6
	mov	edx, r15d
	mov	r12, r14
	mov	rax, r13
.L6:
	cmp	rax, rbx
	mov	DWORD PTR [rsi+rcx*4], edx
	jl	.L50
.L5:
	cmp	rbp, rax
	jne	.L57
	test	r9b, r9b
	jne	.L8
.L57:
	lea	rcx, -1[rax]
	sar	rcx
	cmp	r8, rax
	jl	.L13
	jmp	.L74
	.p2align 4,,10
	.p2align 3
.L76:
	mov	DWORD PTR [rax], edx
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r8, rcx
	mov	rdx, rax
	mov	rax, rcx
	jge	.L75
	mov	rcx, rdx
.L13:
	lea	r12, [rsi+rcx*4]
	mov	edx, DWORD PTR [r12]
	lea	rax, [rsi+rax*4]
	cmp	r10d, edx
	jg	.L76
.L12:
	test	r8, r8
	mov	DWORD PTR [rax], r10d
	je	.L15
.L14:
	sub	r8, 1
	sub	rdi, 4
	mov	r10d, DWORD PTR [rdi]
	cmp	r8, rbx
	mov	r12, rdi
	jl	.L77
.L49:
	mov	rax, r8
	jmp	.L5
.L75:
	mov	rax, r12
	jmp	.L12
.L72:
	mov	rdx, rbx
	sub	r11, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L30
	jmp	.L1
.L24:
	lea	rcx, -2[r12]
	sar	rcx
	cmp	rcx, rax
	je	.L27
	lea	r10, -1[rax]
	mov	rcx, r10
	shr	rcx, 63
	add	rcx, r10
	sar	rcx
	test	rax, rax
	jne	.L28
	jmp	.L23
	.p2align 4,,10
	.p2align 3
.L22:
	cmp	rdx, 2
	mov	rdx, rsi
	ja	.L23
	xor	eax, eax
.L27:
	lea	r10, 1[rax+rax]
	mov	ecx, DWORD PTR [rsi+r10*4]
	mov	DWORD PTR [rdx], ecx
	mov	rcx, rax
	mov	rax, r10
	jmp	.L28
.L18:
	test	r14, r14
	je	.L22
	mov	rdx, rsi
	sub	r11, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L30
	jmp	.L1
	.p2align 4,,10
	.p2align 3
.L8:
	lea	rcx, [rax+rax]
	lea	rax, 1[rcx]
	sar	rcx
	lea	rdx, [rsi+rax*4]
	cmp	r8, rax
	mov	r13d, DWORD PTR [rdx]
	mov	DWORD PTR [r12], r13d
	mov	r12, rdx
	jl	.L13
.L74:
	mov	DWORD PTR [r12], r10d
	jmp	.L14
.L71:
	mov	DWORD PTR [rdx], r8d
	sub	r11, 4
	jmp	.L30
	.seh_endproc
	.p2align 4
	.globl	_Z9sort_demoRSt6vectorIiSaIiEE
	.def	_Z9sort_demoRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9sort_demoRSt6vectorIiSaIiEE
_Z9sort_demoRSt6vectorIiSaIiEE:
.LFB2389:
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	cmp	rbp, rsi
	je	.L78
	mov	rdi, rsi
	sub	rdi, rbp
	mov	rax, rdi
	sar	rax, 2
	test	rax, rax
	je	.L109
	bsr	rax, rax
	mov	rdx, rsi
	mov	rcx, rbp
	lea	rbx, 4[rbp]
	movsx	r8, eax
	add	r8, r8
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	cmp	rdi, 64
	jle	.L81
	lea	rdi, 64[rbp]
	mov	r13d, 4
	jmp	.L88
	.p2align 4,,10
	.p2align 3
.L111:
	mov	r8, rbx
	sub	r8, rbp
	cmp	r8, 4
	jle	.L83
	mov	rcx, r13
	mov	rdx, rbp
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L84:
	add	rbx, 4
	mov	DWORD PTR 0[rbp], r12d
	cmp	rbx, rdi
	je	.L110
.L88:
	mov	r12d, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	eax, DWORD PTR 0[rbp]
	cmp	r12d, eax
	jl	.L111
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	r12d, edx
	jge	.L86
	.p2align 4,,10
	.p2align 3
.L87:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	r12d, edx
	jl	.L87
.L86:
	add	rbx, 4
	mov	DWORD PTR [rcx], r12d
	cmp	rbx, rdi
	jne	.L88
.L110:
	cmp	rsi, rdi
	je	.L78
	.p2align 4,,10
	.p2align 3
.L89:
	mov	ecx, DWORD PTR [rdi]
	lea	rax, -4[rdi]
	mov	edx, DWORD PTR -4[rdi]
	cmp	ecx, edx
	jge	.L101
	.p2align 4,,10
	.p2align 3
.L92:
	mov	DWORD PTR 4[rax], edx
	mov	r8, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ecx, edx
	jl	.L92
	add	rdi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rsi, rdi
	jne	.L89
.L78:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
.L109:
	mov	r8, -2
	mov	rdx, rsi
	mov	rcx, rbp
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	lea	rbx, 4[rbp]
.L81:
	cmp	rsi, rbx
	je	.L78
	mov	r12d, 4
	jmp	.L100
	.p2align 4,,10
	.p2align 3
.L112:
	mov	r8, rbx
	sub	r8, rbp
	cmp	r8, 4
	jle	.L95
	mov	rcx, r12
	mov	rdx, rbp
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L96:
	mov	DWORD PTR 0[rbp], edi
.L97:
	add	rbx, 4
	cmp	rsi, rbx
	je	.L78
.L100:
	mov	edi, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	eax, DWORD PTR 0[rbp]
	cmp	edi, eax
	jl	.L112
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	edx, edi
	jle	.L98
	.p2align 4,,10
	.p2align 3
.L99:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	edi, edx
	jl	.L99
.L98:
	mov	DWORD PTR [rcx], edi
	jmp	.L97
	.p2align 4,,10
	.p2align 3
.L101:
	mov	r8, rdi
	add	rdi, 4
	cmp	rsi, rdi
	mov	DWORD PTR [r8], ecx
	jne	.L89
	jmp	.L78
.L95:
	jne	.L96
	mov	DWORD PTR [rbx], eax
	jmp	.L96
.L83:
	jne	.L84
	mov	DWORD PTR [rbx], eax
	jmp	.L84
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2390:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	call	__main
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	mov	ecx, 40
	mov	QWORD PTR 96[rsp], 6
	movaps	XMMWORD PTR 64[rsp], xmm0
	movdqa	xmm0, XMMWORD PTR .LC1[rip]
	movaps	XMMWORD PTR 80[rsp], xmm0
	call	_Znwy
	mov	rdx, QWORD PTR 64[rsp]
	lea	rcx, 32[rsp]
	mov	rbx, rax
	mov	QWORD PTR 32[rsp], rax
	lea	rax, 40[rax]
	mov	QWORD PTR 48[rsp], rax
	mov	QWORD PTR [rbx], rdx
	mov	rdx, QWORD PTR 72[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	QWORD PTR 8[rbx], rdx
	mov	rdx, QWORD PTR 80[rsp]
	mov	QWORD PTR 16[rbx], rdx
	mov	rdx, QWORD PTR 88[rsp]
	mov	QWORD PTR 24[rbx], rdx
	mov	rdx, QWORD PTR 96[rsp]
	mov	QWORD PTR 32[rbx], rdx
	call	_Z9sort_demoRSt6vectorIiSaIiEE
	mov	esi, DWORD PTR [rbx]
	mov	edx, 40
	mov	rcx, rbx
	call	_ZdlPvy
	mov	eax, esi
	add	rsp, 120
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	5
	.long	3
	.long	8
	.long	1
	.align 16
.LC1:
	.long	9
	.long	2
	.long	7
	.long	4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
