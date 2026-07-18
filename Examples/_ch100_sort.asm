	.file	"_ch100_sort.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_:
.LFB5225:
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
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	mov	r14, QWORD PTR [r9]
	mov	r15, QWORD PTR 8[r9]
	mov	rax, rdx
	mov	rbx, rcx
	mov	rdi, r8
	sub	rax, rcx
	cmp	rax, 64
	jle	.L1
	mov	r10, rax
	sar	rax, 3
	sar	r10, 2
	test	rdi, rdi
	je	.L65
.L3:
	lea	r13, [rbx+rax*4]
	mov	r8d, DWORD PTR 4[rbx]
	mov	r12d, DWORD PTR -4[rdx]
	sub	rdi, 1
	mov	ebp, DWORD PTR 0[r13]
	movq	xmm0, QWORD PTR [rbx]
	lea	rcx, 4[rbx]
	mov	r10d, r8d
	mov	r11d, r12d
	mov	r9d, ebp
	movd	eax, xmm0
	neg	r9d
	cmovs	r9d, ebp
	neg	r10d
	cmovs	r10d, r8d
	neg	r11d
	cmovs	r11d, r12d
	cmp	r9d, r10d
	jle	.L32
	cmp	r9d, r11d
	jl	.L37
	cmp	r10d, r11d
	jl	.L63
.L35:
	pshufd	xmm0, xmm0, 225
	movq	QWORD PTR [rbx], xmm0
.L34:
	mov	r11, rdx
	mov	r10d, r8d
	.p2align 4
	.p2align 3
.L36:
	mov	r8d, r10d
	neg	r8d
	cmovns	r10d, r8d
	mov	r8d, eax
	neg	r8d
	cmovs	r8d, eax
	cmp	r8d, r10d
	jge	.L53
	add	rcx, 4
	.p2align 5
	.p2align 4
	.p2align 3
.L39:
	mov	eax, DWORD PTR [rcx]
	mov	rbp, rcx
	add	rcx, 4
	mov	r8d, eax
	neg	r8d
	cmovs	r8d, eax
	cmp	r8d, r10d
	jl	.L39
.L38:
	mov	ecx, DWORD PTR -4[r11]
	mov	r8d, ecx
	neg	r8d
	cmovs	r8d, ecx
	cmp	r10d, r8d
	jge	.L40
	lea	r8, -8[r11]
	.p2align 5
	.p2align 4
	.p2align 3
.L41:
	mov	ecx, DWORD PTR [r8]
	mov	r11, r8
	sub	r8, 4
	mov	r9d, ecx
	neg	r9d
	cmovs	r9d, ecx
	cmp	r9d, r10d
	jg	.L41
	cmp	rbp, r11
	jnb	.L66
.L43:
	mov	DWORD PTR 0[rbp], ecx
	lea	rcx, 4[rbp]
	mov	DWORD PTR [r11], eax
	mov	eax, DWORD PTR 4[rbp]
	mov	r10d, DWORD PTR [rbx]
	jmp	.L36
.L32:
	cmp	r10d, r11d
	jl	.L35
	cmp	r9d, r11d
	jge	.L37
.L63:
	mov	DWORD PTR [rbx], r12d
	mov	DWORD PTR -4[rdx], eax
	mov	r8d, DWORD PTR [rbx]
	mov	eax, DWORD PTR 4[rbx]
	jmp	.L34
	.p2align 4,,10
	.p2align 3
.L40:
	sub	r11, 4
	cmp	rbp, r11
	jb	.L43
	.p2align 4
	.p2align 3
.L66:
	lea	r9, 48[rsp]
	mov	r8, rdi
	mov	rcx, rbp
	mov	QWORD PTR 48[rsp], r14
	mov	QWORD PTR 56[rsp], r15
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_
	mov	rax, rbp
	sub	rax, rbx
	cmp	rax, 64
	jle	.L1
	mov	r10, rax
	mov	rdx, rbp
	sar	rax, 3
	sar	r10, 2
	test	rdi, rdi
	jne	.L3
.L65:
	lea	rbp, -1[r10]
	lea	rdi, -4[rbx+rax*4]
	mov	rsi, rdx
	lea	rcx, -1[rax]
	sar	rbp
	mov	edx, DWORD PTR [rdi]
	mov	r9, rdi
	mov	r8, rcx
	cmp	rcx, rbp
	jge	.L4
.L69:
	mov	QWORD PTR 32[rsp], rsi
	mov	r12, rcx
	mov	QWORD PTR 40[rsp], rcx
	jmp	.L6
	.p2align 4,,10
	.p2align 3
.L47:
	mov	r12, rax
.L6:
	lea	rcx, 1[r12]
	lea	r14, [rcx+rcx]
	lea	r15, [rbx+rcx*8]
	lea	rax, -1[r14]
	mov	r11d, DWORD PTR [r15]
	lea	r9, [rbx+rax*4]
	mov	ecx, DWORD PTR [r9]
	mov	r13d, r11d
	neg	r13d
	mov	esi, ecx
	cmovs	r13d, r11d
	neg	esi
	cmovs	esi, ecx
	cmp	r13d, esi
	cmovge	ecx, r11d
	cmovge	rax, r14
	cmovge	r9, r15
	mov	DWORD PTR [rbx+r12*4], ecx
	cmp	rax, rbp
	jl	.L47
	mov	rsi, QWORD PTR 32[rsp]
	mov	rcx, QWORD PTR 40[rsp]
	test	r10b, 1
	jne	.L60
	cmp	r8, rax
	je	.L9
.L60:
	lea	r11, -1[rax]
.L8:
	sar	r11
	cmp	rcx, rax
	jge	.L10
	mov	r13d, edx
	neg	r13d
	cmovs	r13d, edx
	jmp	.L12
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L68:
	lea	rax, -1[r11]
	mov	DWORD PTR [r14], r9d
	shr	rax, 63
	lea	r9, -1[rax+r11]
	mov	rax, r11
	cmp	rcx, r11
	jge	.L67
	mov	r11, r9
	sar	r11
.L12:
	lea	r12, [rbx+r11*4]
	lea	r14, [rbx+rax*4]
	mov	r9d, DWORD PTR [r12]
	mov	eax, r9d
	neg	eax
	cmovs	eax, r9d
	cmp	eax, r13d
	jl	.L68
	mov	DWORD PTR [r14], edx
	test	rcx, rcx
	je	.L14
.L13:
	sub	rdi, 4
	sub	rcx, 1
	mov	edx, DWORD PTR [rdi]
	mov	r9, rdi
	cmp	rcx, rbp
	jl	.L69
.L4:
	test	r10b, 1
	jne	.L10
	cmp	rcx, r8
	je	.L70
.L10:
	mov	DWORD PTR [r9], edx
	jmp	.L13
	.p2align 4,,10
	.p2align 3
.L53:
	mov	rbp, rcx
	jmp	.L38
.L37:
	mov	DWORD PTR [rbx], ebp
	mov	DWORD PTR 0[r13], eax
	mov	r8d, DWORD PTR [rbx]
	mov	eax, DWORD PTR 4[rbx]
	jmp	.L34
.L1:
	add	rsp, 72
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L67:
	mov	r14, r12
	mov	DWORD PTR [r14], edx
	test	rcx, rcx
	jne	.L13
.L14:
	mov	rax, rsi
	lea	rdx, -4[rsi]
	sub	rax, rbx
	cmp	rax, 4
	jle	.L1
	.p2align 4
	.p2align 3
.L31:
	mov	rsi, rdx
	mov	eax, DWORD PTR [rbx]
	mov	r11d, DWORD PTR [rdx]
	sub	rsi, rbx
	mov	r15, rsi
	mov	DWORD PTR [rdx], eax
	sar	r15, 2
	cmp	rsi, 8
	jle	.L18
	lea	r14, -1[r15]
	xor	r13d, r13d
	sar	r14
	jmp	.L20
	.p2align 4,,10
	.p2align 3
.L50:
	mov	r13, rax
.L20:
	lea	rcx, 1[r13]
	lea	rbp, [rcx+rcx]
	lea	r12, [rbx+rcx*8]
	lea	rax, -1[rbp]
	mov	r8d, DWORD PTR [r12]
	lea	r9, [rbx+rax*4]
	mov	ecx, DWORD PTR [r9]
	mov	edi, r8d
	neg	edi
	mov	r10d, ecx
	cmovs	edi, r8d
	neg	r10d
	cmovs	r10d, ecx
	cmp	edi, r10d
	cmovge	ecx, r8d
	cmovge	rax, rbp
	cmovge	r9, r12
	mov	DWORD PTR [rbx+r13*4], ecx
	cmp	r14, rax
	jg	.L50
	and	r15d, 1
	jne	.L62
	mov	rcx, rsi
	sar	rcx, 3
	sub	rcx, 1
	cmp	rcx, rax
	je	.L26
.L62:
	lea	r8, -1[rax]
	shr	r8, 63
	lea	r8, -1[rax+r8]
	sar	r8
	test	rax, rax
	je	.L28
.L27:
	mov	edi, r11d
	neg	edi
	cmovs	edi, r11d
	jmp	.L29
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L72:
	lea	rax, -1[r8]
	mov	DWORD PTR [r9], ecx
	shr	rax, 63
	lea	rcx, -1[rax+r8]
	mov	rax, r8
	test	r8, r8
	je	.L71
	sar	rcx
	mov	r8, rcx
.L29:
	lea	r10, [rbx+r8*4]
	lea	r9, [rbx+rax*4]
	mov	ecx, DWORD PTR [r10]
	mov	eax, ecx
	neg	eax
	cmovs	eax, ecx
	cmp	eax, edi
	jl	.L72
.L23:
	mov	DWORD PTR [r9], r11d
	cmp	rsi, 4
	jle	.L1
.L61:
	sub	rdx, 4
	jmp	.L31
.L71:
	mov	r9, r10
	jmp	.L23
.L18:
	and	r15d, 1
	mov	r9, rbx
	jne	.L23
	cmp	rsi, 8
	jne	.L23
	xor	eax, eax
.L26:
	lea	rcx, 1[rax+rax]
	mov	r8d, DWORD PTR [rbx+rcx*4]
	mov	DWORD PTR [r9], r8d
	mov	r8, rax
	mov	rax, rcx
	jmp	.L27
.L70:
	mov	rax, rcx
.L9:
	lea	r11, [rax+rax]
	lea	rax, 1[r11]
	lea	r12, [rbx+rax*4]
	mov	r13d, DWORD PTR [r12]
	mov	DWORD PTR [r9], r13d
	mov	r9, r12
	jmp	.L8
.L28:
	mov	DWORD PTR [r9], r11d
	jmp	.L61
	.seh_endproc
	.p2align 4
	.globl	_Z11sort_by_absRSt6vectorIiSaIiEE
	.def	_Z11sort_by_absRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11sort_by_absRSt6vectorIiSaIiEE
_Z11sort_by_absRSt6vectorIiSaIiEE:
.LFB4431:
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
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	rbx, QWORD PTR 8[rcx]
	mov	rdi, QWORD PTR [rcx]
	lea	rdx, 62[rsp]
	lea	rax, 63[rsp]
	xchg	rdx, rax
	cmp	rbx, rdi
	je	.L74
	mov	rbp, rbx
	mov	QWORD PTR 32[rsp], rax
	sub	rbp, rdi
	mov	QWORD PTR 40[rsp], rdx
	mov	rcx, rbp
	sar	rcx, 2
	je	.L107
	bsr	rcx, rcx
	lea	r9, 32[rsp]
	lea	rsi, 4[rdi]
	mov	rdx, rbx
	movsxd	rcx, ecx
	lea	r8, [rcx+rcx]
	mov	rcx, rdi
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_
	cmp	rbp, 64
	jle	.L106
	lea	rbp, 64[rdi]
	jmp	.L83
	.p2align 4,,10
	.p2align 3
.L109:
	mov	r8, rsi
	sub	r8, rdi
	mov	rdx, r8
	sal	rdx, 62
	sub	rdx, r8
	lea	rcx, 4[rsi+rdx]
	cmp	r8, 4
	jle	.L78
	mov	rdx, rdi
	call	memmove
.L79:
	add	rsi, 4
	mov	DWORD PTR [rdi], r12d
	cmp	rbp, rsi
	je	.L108
.L83:
	mov	r12d, DWORD PTR [rsi]
	mov	eax, DWORD PTR [rdi]
	mov	r8d, r12d
	mov	edx, eax
	neg	r8d
	cmovs	r8d, r12d
	neg	edx
	cmovs	edx, eax
	cmp	edx, r8d
	jg	.L109
	mov	eax, DWORD PTR -4[rsi]
	mov	edx, eax
	neg	edx
	cmovs	edx, eax
	cmp	r8d, edx
	jge	.L96
	lea	rdx, -4[rsi]
	.p2align 5
	.p2align 4
	.p2align 3
.L82:
	mov	DWORD PTR 4[rdx], eax
	mov	r9, rdx
	mov	eax, DWORD PTR -4[rdx]
	sub	rdx, 4
	mov	ecx, eax
	neg	ecx
	cmovs	ecx, eax
	cmp	r8d, ecx
	jl	.L82
	mov	DWORD PTR [r9], r12d
.L111:
	add	rsi, 4
	cmp	rbp, rsi
	jne	.L83
.L108:
	cmp	rbx, rbp
	je	.L74
	.p2align 4
	.p2align 3
.L84:
	mov	r10d, DWORD PTR 0[rbp]
	mov	eax, DWORD PTR -4[rbp]
	mov	r8d, r10d
	mov	edx, eax
	neg	r8d
	cmovs	r8d, r10d
	neg	edx
	cmovs	edx, eax
	cmp	r8d, edx
	jge	.L97
	lea	rdx, -4[rbp]
	.p2align 5
	.p2align 4
	.p2align 3
.L87:
	mov	DWORD PTR 4[rdx], eax
	mov	r9, rdx
	mov	eax, DWORD PTR -4[rdx]
	sub	rdx, 4
	mov	ecx, eax
	neg	ecx
	cmovs	ecx, eax
	cmp	ecx, r8d
	jg	.L87
	add	rbp, 4
	mov	DWORD PTR [r9], r10d
	cmp	rbx, rbp
	jne	.L84
.L74:
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L90:
	je	.L110
	.p2align 4
	.p2align 3
.L91:
	mov	DWORD PTR [rdi], ebp
.L92:
	add	rsi, 4
.L106:
	cmp	rbx, rsi
	je	.L74
	mov	ebp, DWORD PTR [rsi]
	mov	eax, DWORD PTR [rdi]
	mov	r8d, ebp
	mov	edx, eax
	neg	r8d
	cmovs	r8d, ebp
	neg	edx
	cmovs	edx, eax
	cmp	edx, r8d
	jle	.L89
	mov	r8, rsi
	sub	r8, rdi
	mov	rdx, r8
	sal	rdx, 62
	sub	rdx, r8
	lea	rcx, 4[rsi+rdx]
	cmp	r8, 4
	jle	.L90
	mov	rdx, rdi
	call	memmove
	jmp	.L91
.L107:
	lea	r9, 32[rsp]
	mov	rdx, rbx
	lea	rsi, 4[rdi]
	mov	rcx, rdi
	mov	r8, -2
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_
	jmp	.L106
	.p2align 4,,10
	.p2align 3
.L89:
	mov	eax, DWORD PTR -4[rsi]
	mov	edx, eax
	neg	edx
	cmovs	edx, eax
	cmp	r8d, edx
	jge	.L98
	lea	rdx, -4[rsi]
	.p2align 5
	.p2align 4
	.p2align 3
.L94:
	mov	DWORD PTR 4[rdx], eax
	mov	r9, rdx
	mov	eax, DWORD PTR -4[rdx]
	sub	rdx, 4
	mov	ecx, eax
	neg	ecx
	cmovs	ecx, eax
	cmp	r8d, ecx
	jl	.L94
	mov	DWORD PTR [r9], ebp
	jmp	.L92
	.p2align 4,,10
	.p2align 3
.L97:
	mov	r9, rbp
	add	rbp, 4
	mov	DWORD PTR [r9], r10d
	cmp	rbx, rbp
	jne	.L84
	jmp	.L74
.L96:
	mov	r9, rsi
	mov	DWORD PTR [r9], r12d
	jmp	.L111
.L98:
	mov	r9, rsi
	mov	DWORD PTR [r9], ebp
	jmp	.L92
.L78:
	jne	.L79
	mov	DWORD PTR [rcx], eax
	jmp	.L79
.L110:
	mov	DWORD PTR [rcx], eax
	jmp	.L91
	.seh_endproc
	.p2align 4
	.globl	_Z8pipe_sumRKSt6vectorIiSaIiEE
	.def	_Z8pipe_sumRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8pipe_sumRKSt6vectorIiSaIiEE
_Z8pipe_sumRKSt6vectorIiSaIiEE:
.LFB4437:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]
	mov	rcx, QWORD PTR [rcx]
	cmp	r8, rcx
	jne	.L115
	jmp	.L120
	.p2align 4
	.p2align 4,,10
	.p2align 3
.L124:
	add	rcx, 4
	cmp	r8, rcx
	je	.L120
.L115:
	mov	eax, DWORD PTR [rcx]
	test	eax, eax
	jle	.L124
	cmp	r8, rcx
	je	.L120
	mov	edx, DWORD PTR [rcx]
	xor	r9d, r9d
	.p2align 4
	.p2align 3
.L118:
	lea	rax, 4[rcx]
	lea	r9d, [r9+rdx*2]
	cmp	r8, rax
	jne	.L117
	jmp	.L112
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L125:
	add	rax, 4
	cmp	r8, rax
	je	.L112
.L117:
	mov	edx, DWORD PTR [rax]
	mov	rcx, rax
	test	edx, edx
	jle	.L125
	cmp	rax, r8
	jne	.L118
.L112:
	mov	eax, r9d
	ret
.L120:
	xor	r9d, r9d
	mov	eax, r9d
	ret
	.seh_endproc
	.section	.text$_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_:
.LFB5219:
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
	mov	r12, QWORD PTR [r9]
	mov	r13, QWORD PTR 8[r9]
	mov	rax, rdx
	mov	rsi, rcx
	mov	rdi, r8
	mov	r11, rdx
	sub	rax, rcx
	cmp	rax, 64
	jle	.L126
	mov	rbp, rax
	sar	rax, 3
	sar	rbp, 2
	test	rdi, rdi
	je	.L189
.L128:
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
	jge	.L157
	cmp	r8d, r9d
	jl	.L162
	cmp	edx, r9d
	jl	.L188
.L160:
	pshufd	xmm0, xmm0, 225
	movq	QWORD PTR [rsi], xmm0
.L159:
	mov	r10, r11
	cmp	ecx, edx
	jge	.L178
	.p2align 4
	.p2align 3
.L191:
	add	rax, 4
	.p2align 4
	.p2align 4
	.p2align 3
.L164:
	mov	r9, rax
	mov	ecx, DWORD PTR [rax]
	add	rax, 4
	cmp	ecx, edx
	jl	.L164
	mov	rbp, r9
	mov	r9d, DWORD PTR -4[r10]
	cmp	edx, r9d
	jge	.L165
.L192:
	lea	rax, -8[r10]
	.p2align 4
	.p2align 4
	.p2align 3
.L166:
	mov	r10, rax
	mov	r9d, DWORD PTR [rax]
	sub	rax, 4
	cmp	r9d, edx
	jg	.L166
	cmp	rbp, r10
	jnb	.L190
.L168:
	mov	DWORD PTR 0[rbp], r9d
	lea	rax, 4[rbp]
	mov	DWORD PTR [r10], ecx
	mov	edx, DWORD PTR [rsi]
	mov	ecx, DWORD PTR 4[rbp]
	cmp	ecx, edx
	jl	.L191
.L178:
	mov	r9d, DWORD PTR -4[r10]
	mov	rbp, rax
	cmp	edx, r9d
	jl	.L192
	.p2align 4
	.p2align 3
.L165:
	sub	r10, 4
	cmp	rbp, r10
	jb	.L168
	.p2align 4
	.p2align 3
.L190:
	lea	r9, 32[rsp]
	mov	r8, rdi
	mov	rdx, r11
	mov	rcx, rbp
	mov	QWORD PTR 32[rsp], r12
	mov	QWORD PTR 40[rsp], r13
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_
	mov	rax, rbp
	sub	rax, rsi
	cmp	rax, 64
	jle	.L126
	mov	r11, rbp
	mov	rbp, rax
	sar	rax, 3
	sar	rbp, 2
	test	rdi, rdi
	jne	.L128
.L189:
	lea	r10, -1[rbp]
	lea	rbx, -4[rsi+rax*4]
	lea	r8, -1[rax]
	sar	r10
	mov	r9d, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	rdi, r8
	cmp	r8, r10
	jge	.L129
.L195:
	mov	r12, r8
	jmp	.L131
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L172:
	mov	r12, rax
.L131:
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
	jl	.L172
	test	bpl, 1
	jne	.L184
	cmp	rdi, rax
	je	.L134
.L184:
	lea	rdx, -1[rax]
.L133:
	sar	rdx
	cmp	r8, rax
	jl	.L137
	jmp	.L135
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L194:
	mov	DWORD PTR [rax], ecx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	cmp	r8, rdx
	jge	.L193
	mov	rdx, rcx
	sar	rdx
.L137:
	lea	r12, [rsi+rdx*4]
	lea	rax, [rsi+rax*4]
	mov	ecx, DWORD PTR [r12]
	cmp	r9d, ecx
	jg	.L194
	mov	DWORD PTR [rax], r9d
	test	r8, r8
	je	.L139
.L138:
	sub	rbx, 4
	sub	r8, 1
	mov	r9d, DWORD PTR [rbx]
	mov	rcx, rbx
	cmp	r8, r10
	jl	.L195
.L129:
	test	bpl, 1
	jne	.L135
	cmp	r8, rdi
	je	.L196
.L135:
	mov	DWORD PTR [rcx], r9d
	jmp	.L138
	.p2align 4,,10
	.p2align 3
.L157:
	cmp	edx, r9d
	jl	.L160
	cmp	r8d, r9d
	jge	.L162
.L188:
	mov	DWORD PTR [rsi], r9d
	mov	DWORD PTR -4[r11], ecx
	mov	ecx, DWORD PTR 4[rsi]
	mov	edx, DWORD PTR [rsi]
	jmp	.L159
.L162:
	mov	DWORD PTR [rsi], r8d
	mov	DWORD PTR [r10], ecx
	mov	ecx, DWORD PTR 4[rsi]
	mov	edx, DWORD PTR [rsi]
	jmp	.L159
.L126:
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
.L193:
	mov	rax, r12
	mov	DWORD PTR [rax], r9d
	test	r8, r8
	jne	.L138
.L139:
	mov	rax, r11
	sub	r11, 4
	sub	rax, rsi
	cmp	rax, 4
	jle	.L126
	.p2align 4
	.p2align 3
.L156:
	mov	r9, r11
	mov	eax, DWORD PTR [rsi]
	mov	r8d, DWORD PTR [r11]
	sub	r9, rsi
	mov	r13, r9
	mov	DWORD PTR [r11], eax
	sar	r13, 2
	cmp	r9, 8
	jle	.L143
	lea	r12, -1[r13]
	xor	ebp, ebp
	sar	r12
	jmp	.L145
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L175:
	mov	rbp, rax
.L145:
	lea	rdx, 1[rbp]
	lea	r10, [rdx+rdx]
	lea	rbx, [rsi+rdx*8]
	lea	rax, -1[r10]
	mov	edi, DWORD PTR [rbx]
	lea	rcx, [rsi+rax*4]
	mov	edx, DWORD PTR [rcx]
	cmp	edx, edi
	cmovle	edx, edi
	cmovle	rax, r10
	cmovle	rcx, rbx
	mov	DWORD PTR [rsi+rbp*4], edx
	cmp	r12, rax
	jg	.L175
	and	r13d, 1
	jne	.L186
	mov	rdx, r9
	sar	rdx, 3
	sub	rdx, 1
	cmp	rdx, rax
	je	.L151
.L186:
	lea	rdx, -1[rax]
	shr	rdx, 63
	lea	rdx, -1[rax+rdx]
	sar	rdx
	test	rax, rax
	jne	.L154
	jmp	.L197
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L199:
	mov	DWORD PTR [rax], ecx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	test	rdx, rdx
	je	.L198
	sar	rcx
	mov	rdx, rcx
.L154:
	lea	r10, [rsi+rdx*4]
	lea	rax, [rsi+rax*4]
	mov	ecx, DWORD PTR [r10]
	cmp	r8d, ecx
	jg	.L199
.L148:
	mov	DWORD PTR [rax], r8d
	cmp	r9, 4
	jle	.L126
.L185:
	sub	r11, 4
	jmp	.L156
.L198:
	mov	rax, r10
	jmp	.L148
.L143:
	and	r13d, 1
	jne	.L187
	cmp	r9, 8
	jne	.L187
	mov	rcx, rsi
	xor	eax, eax
.L151:
	lea	r10, 1[rax+rax]
	mov	edx, DWORD PTR [rsi+r10*4]
	mov	DWORD PTR [rcx], edx
	mov	rdx, rax
	mov	rax, r10
	jmp	.L154
.L187:
	mov	rax, rsi
	jmp	.L148
.L196:
	mov	rax, r8
.L134:
	lea	rdx, [rax+rax]
	lea	rax, 1[rdx]
	lea	r12, [rsi+rax*4]
	mov	r13d, DWORD PTR [r12]
	mov	DWORD PTR [rcx], r13d
	mov	rcx, r12
	jmp	.L133
.L197:
	mov	DWORD PTR [rcx], r8d
	jmp	.L185
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z10sort_plainRSt6vectorIiSaIiEE
	.def	_Z10sort_plainRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10sort_plainRSt6vectorIiSaIiEE
_Z10sort_plainRSt6vectorIiSaIiEE:
.LFB4416:
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
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	lea	rdx, 62[rsp]
	lea	rax, 63[rsp]
	xchg	rdx, rax
	cmp	rsi, rbp
	je	.L201
	mov	rdi, rsi
	mov	QWORD PTR 32[rsp], rax
	sub	rdi, rbp
	mov	QWORD PTR 40[rsp], rdx
	mov	rcx, rdi
	sar	rcx, 2
	je	.L234
	bsr	rcx, rcx
	lea	r9, 32[rsp]
	lea	rbx, 4[rbp]
	mov	rdx, rsi
	movsxd	rcx, ecx
	lea	r8, [rcx+rcx]
	mov	rcx, rbp
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_
	cmp	rdi, 64
	jle	.L233
	lea	rdi, 64[rbp]
	jmp	.L210
	.p2align 4,,10
	.p2align 3
.L236:
	mov	r8, rbx
	sub	r8, rbp
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[rbx+rax]
	cmp	r8, 4
	jle	.L205
	mov	rdx, rbp
	call	memmove
.L206:
	add	rbx, 4
	mov	DWORD PTR 0[rbp], r12d
	cmp	rdi, rbx
	je	.L235
.L210:
	mov	r12d, DWORD PTR [rbx]
	mov	edx, DWORD PTR 0[rbp]
	cmp	r12d, edx
	jl	.L236
	mov	edx, DWORD PTR -4[rbx]
	cmp	r12d, edx
	jge	.L223
	lea	rax, -4[rbx]
	.p2align 5
	.p2align 4
	.p2align 3
.L209:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	r12d, edx
	jl	.L209
	mov	DWORD PTR [rcx], r12d
.L238:
	add	rbx, 4
	cmp	rdi, rbx
	jne	.L210
.L235:
	cmp	rsi, rdi
	je	.L201
	.p2align 4
	.p2align 3
.L211:
	mov	ecx, DWORD PTR [rdi]
	mov	edx, DWORD PTR -4[rdi]
	cmp	ecx, edx
	jge	.L224
	lea	rax, -4[rdi]
	.p2align 5
	.p2align 4
	.p2align 3
.L214:
	mov	DWORD PTR 4[rax], edx
	mov	r8, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ecx, edx
	jl	.L214
	add	rdi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rsi, rdi
	jne	.L211
.L201:
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L237:
	mov	r8, rbx
	sub	r8, rbp
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[rbx+rax]
	cmp	r8, 4
	jle	.L217
	mov	rdx, rbp
	call	memmove
.L218:
	mov	DWORD PTR 0[rbp], edi
.L219:
	add	rbx, 4
.L233:
	cmp	rsi, rbx
	je	.L201
	mov	edi, DWORD PTR [rbx]
	mov	edx, DWORD PTR 0[rbp]
	cmp	edi, edx
	jl	.L237
	mov	edx, DWORD PTR -4[rbx]
	cmp	edi, edx
	jge	.L225
	lea	rax, -4[rbx]
	.p2align 5
	.p2align 4
	.p2align 3
.L221:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	edi, edx
	jl	.L221
	mov	DWORD PTR [rcx], edi
	jmp	.L219
.L234:
	lea	r9, 32[rsp]
	mov	rdx, rsi
	lea	rbx, 4[rbp]
	mov	rcx, rbp
	mov	r8, -2
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_
	jmp	.L233
	.p2align 4,,10
	.p2align 3
.L224:
	mov	r8, rdi
	add	rdi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rsi, rdi
	jne	.L211
	jmp	.L201
.L205:
	jne	.L206
	mov	DWORD PTR [rcx], edx
	jmp	.L206
.L217:
	jne	.L218
	mov	DWORD PTR [rcx], edx
	jmp	.L218
.L223:
	mov	rcx, rbx
	mov	DWORD PTR [rcx], r12d
	jmp	.L238
.L225:
	mov	rcx, rbx
	mov	DWORD PTR [rcx], edi
	jmp	.L219
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	memmove;	.scl	2;	.type	32;	.endef
