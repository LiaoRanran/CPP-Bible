	.file	"_ch96_sort_asm.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0:
.LFB2499:
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, rdx
	mov	rsi, rcx
	mov	rdi, r8
	mov	r11, rdx
	sub	rax, rcx
	cmp	rax, 64
	jle	.L1
	mov	rbp, rax
	sar	rax, 3
	sar	rbp, 2
	test	rdi, rdi
	je	.L65
.L3:
	movq	xmm0, QWORD PTR [rsi]
	lea	r10, [rsi+rax*4]
	mov	r9d, DWORD PTR -4[r11]
	sub	rdi, 1
	mov	r8d, DWORD PTR [r10]
	lea	rax, 4[rsi]
	pshufd	xmm1, xmm0, 0xe5
	movd	edx, xmm1
	movd	ecx, xmm0
	cmp	edx, r8d
	jge	.L32
	cmp	r8d, r9d
	jl	.L37
	cmp	edx, r9d
	jl	.L63
.L35:
	pshufd	xmm0, xmm0, 225
	movq	QWORD PTR [rsi], xmm0
.L34:
	mov	r10, r11
	cmp	ecx, edx
	jge	.L53
	.p2align 4
	.p2align 3
.L67:
	add	rax, 4
	.p2align 4
	.p2align 4
	.p2align 3
.L39:
	mov	r9, rax
	mov	ecx, DWORD PTR [rax]
	add	rax, 4
	cmp	ecx, edx
	jl	.L39
	mov	rbx, r9
	mov	r9d, DWORD PTR -4[r10]
	cmp	r9d, edx
	jle	.L40
.L68:
	lea	rax, -8[r10]
	.p2align 4
	.p2align 4
	.p2align 3
.L41:
	mov	r10, rax
	mov	r9d, DWORD PTR [rax]
	sub	rax, 4
	cmp	r9d, edx
	jg	.L41
	cmp	rbx, r10
	jnb	.L66
.L43:
	mov	DWORD PTR [rbx], r9d
	lea	rax, 4[rbx]
	mov	DWORD PTR [r10], ecx
	mov	edx, DWORD PTR [rsi]
	mov	ecx, DWORD PTR 4[rbx]
	cmp	ecx, edx
	jl	.L67
.L53:
	mov	r9d, DWORD PTR -4[r10]
	mov	rbx, rax
	cmp	r9d, edx
	jg	.L68
	.p2align 4
	.p2align 3
.L40:
	sub	r10, 4
	cmp	rbx, r10
	jb	.L43
	.p2align 4
	.p2align 3
.L66:
	mov	r8, rdi
	mov	rdx, r11
	mov	rcx, rbx
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	mov	rax, rbx
	sub	rax, rsi
	cmp	rax, 64
	jle	.L1
	mov	rbp, rax
	mov	r11, rbx
	sar	rax, 3
	sar	rbp, 2
	test	rdi, rdi
	jne	.L3
.L65:
	lea	r10, -1[rbp]
	lea	rbx, -4[rsi+rax*4]
	lea	r8, -1[rax]
	sar	r10
	mov	r9d, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	rdi, r8
	cmp	r8, r10
	jge	.L4
.L71:
	mov	r12, r8
	jmp	.L6
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L47:
	mov	r12, rax
.L6:
	lea	rdx, 1[r12]
	lea	r13, [rdx+rdx]
	lea	r14, [rsi+rdx*8]
	lea	rax, -1[r13]
	mov	r15d, DWORD PTR [r14]
	lea	rcx, [rsi+rax*4]
	mov	edx, DWORD PTR [rcx]
	cmp	edx, r15d
	cmovle	edx, r15d
	cmovle	rax, r13
	cmovle	rcx, r14
	mov	DWORD PTR [rsi+r12*4], edx
	cmp	rax, r10
	jl	.L47
	test	bpl, 1
	jne	.L59
	cmp	rdi, rax
	je	.L9
.L59:
	lea	rdx, -1[rax]
.L8:
	sar	rdx
	cmp	r8, rax
	jl	.L12
	jmp	.L10
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L70:
	mov	DWORD PTR [rax], ecx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	cmp	r8, rdx
	jge	.L69
	mov	rdx, rcx
	sar	rdx
.L12:
	lea	r12, [rsi+rdx*4]
	lea	rax, [rsi+rax*4]
	mov	ecx, DWORD PTR [r12]
	cmp	r9d, ecx
	jg	.L70
	mov	DWORD PTR [rax], r9d
	test	r8, r8
	je	.L14
.L13:
	sub	rbx, 4
	sub	r8, 1
	mov	r9d, DWORD PTR [rbx]
	mov	rcx, rbx
	cmp	r8, r10
	jl	.L71
.L4:
	test	bpl, 1
	jne	.L10
	cmp	r8, rdi
	je	.L72
.L10:
	mov	DWORD PTR [rcx], r9d
	jmp	.L13
	.p2align 4,,10
	.p2align 3
.L32:
	cmp	edx, r9d
	jl	.L35
	cmp	r8d, r9d
	jge	.L37
.L63:
	mov	DWORD PTR [rsi], r9d
	mov	DWORD PTR -4[r11], ecx
	mov	ecx, DWORD PTR 4[rsi]
	mov	edx, DWORD PTR [rsi]
	jmp	.L34
.L37:
	mov	DWORD PTR [rsi], r8d
	mov	DWORD PTR [r10], ecx
	mov	ecx, DWORD PTR 4[rsi]
	mov	edx, DWORD PTR [rsi]
	jmp	.L34
.L1:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L69:
	mov	rax, r12
	mov	DWORD PTR [rax], r9d
	test	r8, r8
	jne	.L13
.L14:
	mov	rax, r11
	lea	r9, -4[r11]
	sub	rax, rsi
	cmp	rax, 4
	jle	.L1
	.p2align 4
	.p2align 3
.L31:
	mov	r10, r9
	mov	eax, DWORD PTR [rsi]
	mov	r8d, DWORD PTR [r9]
	sub	r10, rsi
	mov	r13, r10
	mov	DWORD PTR [r9], eax
	sar	r13, 2
	cmp	r10, 8
	jle	.L18
	lea	r12, -1[r13]
	xor	ebp, ebp
	sar	r12
	jmp	.L20
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L50:
	mov	rbp, rax
.L20:
	lea	rdx, 1[rbp]
	lea	r11, [rdx+rdx]
	lea	rbx, [rsi+rdx*8]
	lea	rax, -1[r11]
	mov	edi, DWORD PTR [rbx]
	lea	rcx, [rsi+rax*4]
	mov	edx, DWORD PTR [rcx]
	cmp	edx, edi
	cmovle	edx, edi
	cmovle	rax, r11
	cmovle	rcx, rbx
	mov	DWORD PTR [rsi+rbp*4], edx
	cmp	r12, rax
	jg	.L50
	and	r13d, 1
	jne	.L61
	mov	rdx, r10
	sar	rdx, 3
	sub	rdx, 1
	cmp	rdx, rax
	je	.L26
.L61:
	lea	rdx, -1[rax]
	shr	rdx, 63
	lea	rdx, -1[rax+rdx]
	sar	rdx
	test	rax, rax
	jne	.L29
	jmp	.L73
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L75:
	mov	DWORD PTR [rax], ecx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	test	rdx, rdx
	je	.L74
	sar	rcx
	mov	rdx, rcx
.L29:
	lea	r11, [rsi+rdx*4]
	lea	rax, [rsi+rax*4]
	mov	ecx, DWORD PTR [r11]
	cmp	r8d, ecx
	jg	.L75
.L23:
	mov	DWORD PTR [rax], r8d
	cmp	r10, 4
	jle	.L1
.L60:
	sub	r9, 4
	jmp	.L31
.L74:
	mov	rax, r11
	jmp	.L23
.L18:
	and	r13d, 1
	jne	.L62
	cmp	r10, 8
	jne	.L62
	mov	rcx, rsi
	xor	eax, eax
.L26:
	lea	r11, 1[rax+rax]
	mov	edx, DWORD PTR [rsi+r11*4]
	mov	DWORD PTR [rcx], edx
	mov	rdx, rax
	mov	rax, r11
	jmp	.L29
.L62:
	mov	rax, rsi
	jmp	.L23
.L72:
	mov	rax, r8
.L9:
	lea	rdx, [rax+rax]
	lea	rax, 1[rdx]
	lea	r12, [rsi+rax*4]
	mov	r13d, DWORD PTR [r12]
	mov	DWORD PTR [rcx], r13d
	mov	rcx, r12
	jmp	.L8
.L73:
	mov	DWORD PTR [rcx], r8d
	jmp	.L60
	.seh_endproc
	.p2align 4
	.globl	_Z9sort_demoRSt6vectorIiSaIiEE
	.def	_Z9sort_demoRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9sort_demoRSt6vectorIiSaIiEE
_Z9sort_demoRSt6vectorIiSaIiEE:
.LFB2347:
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
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rdi, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	cmp	rbp, rdi
	je	.L76
	mov	rsi, rdi
	lea	rbx, 4[rbp]
	sub	rsi, rbp
	mov	rax, rsi
	sar	rax, 2
	je	.L110
	bsr	rax, rax
	mov	rdx, rdi
	mov	rcx, rbp
	movsxd	r8, eax
	add	r8, r8
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	cmp	rsi, 64
	jle	.L109
	lea	rsi, 64[rbp]
	jmp	.L86
	.p2align 4,,10
	.p2align 3
.L112:
	mov	r8, rbx
	sub	r8, rbp
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[rbx+rax]
	cmp	r8, 4
	jle	.L81
	mov	rdx, rbp
	call	memmove
.L82:
	add	rbx, 4
	mov	DWORD PTR 0[rbp], r12d
	cmp	rsi, rbx
	je	.L111
.L86:
	mov	r12d, DWORD PTR [rbx]
	mov	edx, DWORD PTR 0[rbp]
	cmp	r12d, edx
	jl	.L112
	mov	edx, DWORD PTR -4[rbx]
	cmp	r12d, edx
	jge	.L99
	lea	rax, -4[rbx]
	.p2align 5
	.p2align 4
	.p2align 3
.L85:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	r12d, edx
	jl	.L85
	mov	DWORD PTR [rcx], r12d
.L114:
	add	rbx, 4
	cmp	rsi, rbx
	jne	.L86
.L111:
	cmp	rdi, rsi
	je	.L76
	.p2align 4
	.p2align 3
.L87:
	mov	ecx, DWORD PTR [rsi]
	mov	edx, DWORD PTR -4[rsi]
	cmp	ecx, edx
	jge	.L100
	lea	rax, -4[rsi]
	.p2align 5
	.p2align 4
	.p2align 3
.L90:
	mov	DWORD PTR 4[rax], edx
	mov	r8, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ecx, edx
	jl	.L90
	add	rsi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rdi, rsi
	jne	.L87
.L76:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L113:
	mov	r8, rbx
	sub	r8, rbp
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[rbx+rax]
	cmp	r8, 4
	jle	.L93
	mov	rdx, rbp
	call	memmove
.L94:
	mov	DWORD PTR 0[rbp], esi
.L95:
	add	rbx, 4
.L109:
	cmp	rdi, rbx
	je	.L76
	mov	esi, DWORD PTR [rbx]
	mov	edx, DWORD PTR 0[rbp]
	cmp	esi, edx
	jl	.L113
	mov	edx, DWORD PTR -4[rbx]
	cmp	esi, edx
	jge	.L101
	lea	rax, -4[rbx]
	.p2align 5
	.p2align 4
	.p2align 3
.L97:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	esi, edx
	jl	.L97
	mov	DWORD PTR [rcx], esi
	jmp	.L95
.L110:
	mov	r8, -2
	mov	rdx, rdi
	mov	rcx, rbp
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	jmp	.L109
	.p2align 4,,10
	.p2align 3
.L100:
	mov	r8, rsi
	add	rsi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rdi, rsi
	jne	.L87
	jmp	.L76
.L81:
	jne	.L82
	mov	DWORD PTR [rcx], edx
	jmp	.L82
.L93:
	jne	.L94
	mov	DWORD PTR [rcx], edx
	jmp	.L94
.L99:
	mov	rcx, rbx
	mov	DWORD PTR [rcx], r12d
	jmp	.L114
.L101:
	mov	rcx, rbx
	mov	DWORD PTR [rcx], esi
	jmp	.L95
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2348:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	call	__main
	mov	ecx, 40
	call	_Znwy
	movabs	rdx, 12884901893
	movabs	rcx, 4294967304
	mov	rbx, rax
	mov	QWORD PTR 32[rsp], rax
	lea	rax, 40[rax]
	mov	QWORD PTR [rbx], rdx
	movabs	rdx, 8589934601
	mov	QWORD PTR 8[rbx], rcx
	movabs	rcx, 17179869191
	mov	QWORD PTR 16[rbx], rdx
	mov	QWORD PTR 24[rbx], rcx
	lea	rcx, 32[rsp]
	mov	QWORD PTR 32[rbx], 6
	mov	QWORD PTR 48[rsp], rax
	mov	QWORD PTR 40[rsp], rax
	call	_Z9sort_demoRSt6vectorIiSaIiEE
	mov	esi, DWORD PTR [rbx]
	mov	edx, 40
	mov	rcx, rbx
	call	_ZdlPvy
	mov	eax, esi
	add	rsp, 72
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
