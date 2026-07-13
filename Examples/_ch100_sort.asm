	.file	"_ch100_sort.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_:
.LFB5189:
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
	mov	rsi, rdx
	sub	rax, rcx
	mov	r12, r8
	mov	r11, rdx
	cmp	rax, 64
	jle	.L1
	lea	rbp, 4[rcx]
	test	r8, r8
	lea	rdi, 48[rsp]
	je	.L45
.L4:
	sar	rax, 3
	mov	r8d, DWORD PTR 4[rbx]
	sub	r12, 1
	lea	r13, [rbx+rax*4]
	mov	esi, DWORD PTR -4[r11]
	mov	r10d, DWORD PTR 0[r13]
	movq	xmm0, QWORD PTR [rbx]
	mov	ecx, r8d
	mov	r9d, esi
	movd	eax, xmm0
	pshufd	xmm1, xmm0, 225
	mov	edx, r10d
	neg	edx
	cmovs	edx, r10d
	neg	ecx
	cmovs	ecx, r8d
	neg	r9d
	cmovs	r9d, esi
	cmp	edx, ecx
	jle	.L31
	cmp	edx, r9d
	jl	.L37
	cmp	ecx, r9d
	jl	.L69
.L34:
	movq	QWORD PTR [rbx], xmm1
	mov	edx, DWORD PTR -4[r11]
.L33:
	mov	r10, r11
	mov	rcx, rbp
	.p2align 4,,10
	.p2align 3
.L35:
	mov	r9d, r8d
	sar	r9d, 31
	xor	r8d, r9d
	sub	r8d, r9d
	mov	r9d, eax
	neg	r9d
	cmovs	r9d, eax
	cmp	r8d, r9d
	jle	.L55
	add	rcx, 4
	.p2align 4,,10
	.p2align 3
.L39:
	mov	eax, DWORD PTR [rcx]
	mov	rsi, rcx
	add	rcx, 4
	mov	r9d, eax
	neg	r9d
	cmovs	r9d, eax
	cmp	r9d, r8d
	jl	.L39
.L38:
	mov	ecx, edx
	neg	ecx
	cmovs	ecx, edx
	cmp	ecx, r8d
	jle	.L40
	lea	rcx, -8[r10]
	.p2align 4,,10
	.p2align 3
.L41:
	mov	edx, DWORD PTR [rcx]
	mov	r10, rcx
	sub	rcx, 4
	mov	r9d, edx
	neg	r9d
	cmovs	r9d, edx
	cmp	r9d, r8d
	jg	.L41
	cmp	rsi, r10
	jnb	.L71
.L43:
	mov	DWORD PTR [rsi], edx
	lea	rcx, 4[rsi]
	mov	edx, DWORD PTR -4[r10]
	mov	DWORD PTR [r10], eax
	mov	r8d, DWORD PTR [rbx]
	mov	eax, DWORD PTR 4[rsi]
	jmp	.L35
.L31:
	cmp	ecx, r9d
	jl	.L34
	cmp	edx, r9d
	jge	.L37
.L69:
	mov	DWORD PTR [rbx], esi
	mov	edx, eax
	mov	DWORD PTR -4[r11], eax
	mov	r8d, DWORD PTR [rbx]
	mov	eax, DWORD PTR 4[rbx]
	jmp	.L33
	.p2align 4,,10
	.p2align 3
.L40:
	sub	r10, 4
	cmp	rsi, r10
	jb	.L43
	.p2align 4,,10
	.p2align 3
.L71:
	mov	r9, rdi
	mov	r8, r12
	mov	rdx, r11
	mov	QWORD PTR 48[rsp], r14
	mov	rcx, rsi
	mov	QWORD PTR 56[rsp], r15
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_
	mov	rax, rsi
	sub	rax, rbx
	cmp	rax, 64
	jle	.L1
	test	r12, r12
	je	.L45
	mov	r11, rsi
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L55:
	mov	rsi, rcx
	jmp	.L38
.L37:
	mov	DWORD PTR [rbx], r10d
	mov	DWORD PTR 0[r13], eax
	mov	r8d, DWORD PTR [rbx]
	mov	eax, DWORD PTR 4[rbx]
	mov	edx, DWORD PTR -4[r11]
	jmp	.L33
.L15:
	lea	r12, -4[rsi]
	.p2align 4,,10
	.p2align 3
.L30:
	mov	eax, DWORD PTR [rbx]
	mov	rsi, r12
	sub	rsi, rbx
	mov	r8d, DWORD PTR [r12]
	mov	rdx, rsi
	sar	rdx, 2
	mov	DWORD PTR [r12], eax
	lea	rax, -1[rdx]
	mov	rdi, rdx
	mov	rbp, rax
	and	edi, 1
	shr	rbp, 63
	add	rbp, rax
	sar	rbp
	cmp	rsi, 8
	jle	.L18
	xor	r11d, r11d
	mov	QWORD PTR 32[rsp], r12
	jmp	.L20
	.p2align 4,,10
	.p2align 3
.L52:
	mov	r11, rax
.L20:
	lea	rcx, 1[r11]
	lea	rax, [rcx+rcx]
	lea	r14, -1[rax]
	lea	rcx, [rbx+rcx*8]
	mov	r9d, DWORD PTR [rcx]
	lea	r15, [rbx+r14*4]
	mov	r10d, DWORD PTR [r15]
	mov	r13d, r9d
	neg	r13d
	mov	r12d, r10d
	cmovs	r13d, r9d
	neg	r12d
	cmovs	r12d, r10d
	cmp	r13d, r12d
	cmovl	rax, r14
	cmovl	r9d, r10d
	cmovl	rcx, r15
	cmp	rax, rbp
	mov	DWORD PTR [rbx+r11*4], r9d
	jl	.L52
	test	rdi, rdi
	mov	r12, QWORD PTR 32[rsp]
	je	.L24
	lea	rdx, -1[rax]
	mov	r9, rdx
	shr	r9, 63
	add	r9, rdx
	sar	r9
	test	rax, rax
	je	.L72
.L25:
	mov	r11d, r8d
	mov	rcx, rax
	neg	r11d
	cmovs	r11d, r8d
	jmp	.L28
	.p2align 4,,10
	.p2align 3
.L74:
	mov	DWORD PTR [rcx], edx
	lea	rdx, -1[r9]
	mov	rcx, r9
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	test	r9, r9
	je	.L73
	mov	r9, rax
.L28:
	lea	r10, [rbx+r9*4]
	mov	edx, DWORD PTR [r10]
	lea	rcx, [rbx+rcx*4]
	mov	eax, edx
	neg	eax
	cmovs	eax, edx
	cmp	eax, r11d
	jl	.L74
.L23:
	sub	r12, 4
	cmp	rsi, 4
	mov	DWORD PTR [rcx], r8d
	jg	.L30
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
.L45:
	sar	rax, 2
	lea	rdx, -2[rax]
	lea	r12, -1[rax]
	not	rax
	sar	rdx
	sar	r12
	mov	r10d, eax
	mov	r8, rdx
	lea	rdi, [rbx+rdx*4]
	and	r10d, 1
	cmp	rdx, r12
	mov	ecx, DWORD PTR [rdi]
	mov	r9, rdi
	jge	.L49
.L77:
	mov	rbp, rdx
	mov	QWORD PTR 32[rsp], r8
	mov	QWORD PTR 40[rsp], rdx
	jmp	.L7
	.p2align 4,,10
	.p2align 3
.L50:
	mov	rbp, rax
.L7:
	lea	rdx, 1[rbp]
	lea	rax, [rdx+rdx]
	lea	r14, -1[rax]
	lea	r9, [rbx+rdx*8]
	mov	edx, DWORD PTR [r9]
	lea	r15, [rbx+r14*4]
	mov	r8d, DWORD PTR [r15]
	mov	r13d, edx
	neg	r13d
	mov	r11d, r8d
	cmovs	r13d, edx
	neg	r11d
	cmovs	r11d, r8d
	cmp	r13d, r11d
	cmovl	rax, r14
	cmovl	edx, r8d
	cmovl	r9, r15
	cmp	rax, r12
	mov	DWORD PTR [rbx+rbp*4], edx
	jl	.L50
	mov	r8, QWORD PTR 32[rsp]
	mov	rdx, QWORD PTR 40[rsp]
.L5:
	cmp	r8, rax
	jne	.L57
	test	r10b, r10b
	jne	.L8
.L57:
	lea	r11, -1[rax]
	sar	r11
	cmp	rdx, rax
	jge	.L11
.L78:
	mov	r13d, ecx
	mov	r14, rax
	neg	r13d
	cmovs	r13d, ecx
	jmp	.L13
	.p2align 4,,10
	.p2align 3
.L76:
	mov	DWORD PTR [r14], r9d
	lea	r9, -1[r11]
	mov	r14, r11
	mov	rax, r9
	shr	rax, 63
	add	rax, r9
	sar	rax
	cmp	rdx, r11
	jge	.L75
	mov	r11, rax
.L13:
	lea	rbp, [rbx+r11*4]
	mov	r9d, DWORD PTR 0[rbp]
	lea	r14, [rbx+r14*4]
	mov	eax, r9d
	neg	eax
	cmovs	eax, r9d
	cmp	eax, r13d
	jl	.L76
.L12:
	test	rdx, rdx
	mov	DWORD PTR [r14], ecx
	je	.L15
.L14:
	sub	rdx, 1
	sub	rdi, 4
	mov	ecx, DWORD PTR [rdi]
	cmp	rdx, r12
	mov	r9, rdi
	jl	.L77
.L49:
	mov	rax, rdx
	jmp	.L5
.L75:
	mov	r14, rbp
	jmp	.L12
.L73:
	mov	rcx, r10
	sub	r12, 4
	cmp	rsi, 4
	mov	DWORD PTR [rcx], r8d
	jg	.L30
	jmp	.L1
.L24:
	sub	rdx, 2
	sar	rdx
	cmp	rdx, rax
	je	.L27
	lea	rdx, -1[rax]
	mov	r9, rdx
	shr	r9, 63
	add	r9, rdx
	sar	r9
	test	rax, rax
	jne	.L25
	jmp	.L23
	.p2align 4,,10
	.p2align 3
.L18:
	test	rdi, rdi
	mov	rcx, rbx
	jne	.L23
	cmp	rax, 2
	ja	.L23
	xor	eax, eax
.L27:
	lea	rdx, 1[rax+rax]
	mov	r9d, DWORD PTR [rbx+rdx*4]
	mov	DWORD PTR [rcx], r9d
	mov	r9, rax
	mov	rax, rdx
	jmp	.L25
.L8:
	lea	r11, [rax+rax]
	lea	rax, 1[r11]
	sar	r11
	lea	rbp, [rbx+rax*4]
	cmp	rdx, rax
	mov	r13d, DWORD PTR 0[rbp]
	mov	DWORD PTR [r9], r13d
	mov	r9, rbp
	jl	.L78
.L11:
	mov	DWORD PTR [r9], ecx
	jmp	.L14
.L72:
	mov	DWORD PTR [rcx], r8d
	sub	r12, 4
	jmp	.L30
	.seh_endproc
	.p2align 4
	.globl	_Z11sort_by_absRSt6vectorIiSaIiEE
	.def	_Z11sort_by_absRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11sort_by_absRSt6vectorIiSaIiEE
_Z11sort_by_absRSt6vectorIiSaIiEE:
.LFB4359:
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
	mov	rbx, QWORD PTR 8[rcx]
	mov	rdi, QWORD PTR [rcx]
	lea	rax, 62[rsp]
	lea	rdx, 63[rsp]
	movq	xmm0, rax
	cmp	rbx, rdi
	movq	xmm1, rdx
	punpcklqdq	xmm0, xmm1
	je	.L80
	mov	rbp, rbx
	mov	r8, -2
	sub	rbp, rdi
	mov	rax, rbp
	sar	rax, 2
	test	rax, rax
	je	.L81
	bsr	rax, rax
	cdqe
	lea	r8, [rax+rax]
.L81:
	lea	r9, 32[rsp]
	mov	rdx, rbx
	mov	rcx, rdi
	movaps	XMMWORD PTR 32[rsp], xmm0
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessEZ11sort_by_absRS5_EUliE_EEDaRT_RT0_EUlOSF_OSH_E_EEEvSF_SF_SH_T1_
	lea	rsi, 4[rdi]
	cmp	rbp, 64
	jg	.L113
	cmp	rbx, rsi
	je	.L80
	mov	ebp, 4
	jmp	.L102
	.p2align 4,,10
	.p2align 3
.L114:
	mov	r8, rsi
	sub	r8, rdi
	cmp	r8, 4
	jle	.L97
	mov	rcx, rbp
	mov	rdx, rdi
	sub	rcx, r8
	add	rcx, rsi
	call	memmove
.L98:
	add	rsi, 4
	mov	DWORD PTR [rdi], r12d
	cmp	rbx, rsi
	je	.L80
.L102:
	mov	r12d, DWORD PTR [rsi]
	mov	r9, rsi
	mov	eax, DWORD PTR [rdi]
	mov	r8d, r12d
	neg	r8d
	mov	edx, eax
	cmovs	r8d, r12d
	neg	edx
	cmovs	edx, eax
	cmp	edx, r8d
	jg	.L114
	mov	eax, DWORD PTR -4[rsi]
	lea	rdx, -4[rsi]
	mov	ecx, eax
	neg	ecx
	cmovs	ecx, eax
	cmp	ecx, r8d
	jle	.L100
	.p2align 4,,10
	.p2align 3
.L101:
	mov	DWORD PTR 4[rdx], eax
	mov	r9, rdx
	mov	eax, DWORD PTR -4[rdx]
	sub	rdx, 4
	mov	ecx, eax
	neg	ecx
	cmovs	ecx, eax
	cmp	r8d, ecx
	jl	.L101
.L100:
	add	rsi, 4
	mov	DWORD PTR [r9], r12d
	cmp	rbx, rsi
	jne	.L102
.L80:
	add	rsp, 72
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L113:
	lea	rbp, 64[rdi]
	mov	r12d, 4
	jmp	.L89
	.p2align 4,,10
	.p2align 3
.L116:
	mov	r8, rsi
	sub	r8, rdi
	cmp	r8, 4
	jle	.L84
	mov	rcx, r12
	mov	rdx, rdi
	sub	rcx, r8
	add	rcx, rsi
	call	memmove
.L85:
	add	rsi, 4
	mov	DWORD PTR [rdi], r13d
	cmp	rsi, rbp
	je	.L115
.L89:
	mov	r13d, DWORD PTR [rsi]
	mov	r9, rsi
	mov	eax, DWORD PTR [rdi]
	mov	r8d, r13d
	neg	r8d
	mov	edx, eax
	cmovs	r8d, r13d
	neg	edx
	cmovs	edx, eax
	cmp	edx, r8d
	jg	.L116
	mov	eax, DWORD PTR -4[rsi]
	lea	rdx, -4[rsi]
	jmp	.L112
	.p2align 4,,10
	.p2align 3
.L117:
	mov	DWORD PTR 4[rdx], eax
	mov	r9, rdx
	mov	eax, DWORD PTR -4[rdx]
	sub	rdx, 4
.L112:
	mov	ecx, eax
	neg	ecx
	cmovs	ecx, eax
	cmp	r8d, ecx
	jl	.L117
	add	rsi, 4
	mov	DWORD PTR [r9], r13d
	cmp	rsi, rbp
	jne	.L89
.L115:
	cmp	rbx, rsi
	mov	r8, rsi
	je	.L80
	.p2align 4,,10
	.p2align 3
.L94:
	mov	r11d, DWORD PTR [r8]
	lea	rdx, -4[r8]
	mov	r10, r8
	mov	eax, DWORD PTR -4[r8]
	mov	r9d, r11d
	neg	r9d
	mov	ecx, eax
	cmovs	r9d, r11d
	neg	ecx
	cmovs	ecx, eax
	cmp	r9d, ecx
	jge	.L92
	.p2align 4,,10
	.p2align 3
.L93:
	mov	DWORD PTR 4[rdx], eax
	mov	r10, rdx
	mov	eax, DWORD PTR -4[rdx]
	sub	rdx, 4
	mov	ecx, eax
	neg	ecx
	cmovs	ecx, eax
	cmp	ecx, r9d
	jg	.L93
.L92:
	add	r8, 4
	mov	DWORD PTR [r10], r11d
	cmp	rbx, r8
	jne	.L94
	add	rsp, 72
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
.L97:
	jne	.L98
	mov	DWORD PTR [rsi], eax
	jmp	.L98
.L84:
	jne	.L85
	mov	DWORD PTR [rsi], eax
	jmp	.L85
	.seh_endproc
	.p2align 4
	.globl	_Z8pipe_sumRKSt6vectorIiSaIiEE
	.def	_Z8pipe_sumRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8pipe_sumRKSt6vectorIiSaIiEE
_Z8pipe_sumRKSt6vectorIiSaIiEE:
.LFB4365:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]
	mov	rcx, QWORD PTR [rcx]
	cmp	r8, rcx
	jne	.L121
	jmp	.L123
	.p2align 4,,10
	.p2align 3
.L131:
	add	rcx, 4
	cmp	r8, rcx
	je	.L123
.L121:
	mov	eax, DWORD PTR [rcx]
	test	eax, eax
	jle	.L131
	cmp	r8, rcx
	je	.L123
	mov	edx, DWORD PTR [rcx]
	xor	r9d, r9d
	.p2align 4,,10
	.p2align 3
.L127:
	lea	rax, 4[rcx]
	lea	r9d, [r9+rdx*2]
	cmp	r8, rax
	jne	.L126
	jmp	.L118
	.p2align 4,,10
	.p2align 3
.L132:
	add	rax, 4
	cmp	r8, rax
	je	.L118
.L126:
	mov	edx, DWORD PTR [rax]
	mov	rcx, rax
	test	edx, edx
	jle	.L132
	cmp	rax, r8
	jne	.L127
.L118:
	mov	eax, r9d
	ret
.L123:
	xor	r9d, r9d
	jmp	.L118
	.seh_endproc
	.section	.text$_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_:
.LFB5182:
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
	mov	r14, QWORD PTR [r9]
	mov	r15, QWORD PTR 8[r9]
	mov	rax, rdx
	mov	rbp, rcx
	mov	rdi, rdx
	sub	rax, rcx
	mov	r12, r8
	mov	r11, rdx
	cmp	rax, 64
	jle	.L133
	lea	rsi, 4[rcx]
	test	r8, r8
	lea	rbx, 32[rsp]
	je	.L177
.L136:
	sar	rax, 3
	movq	xmm0, QWORD PTR 0[rbp]
	sub	r12, 1
	lea	r9, 0[rbp+rax*4]
	mov	r8d, DWORD PTR -4[r11]
	mov	eax, DWORD PTR [r9]
	pshufd	xmm2, xmm0, 0xe5
	movd	ecx, xmm2
	movd	edx, xmm0
	pshufd	xmm1, xmm0, 225
	cmp	ecx, eax
	jge	.L163
	cmp	eax, r8d
	jl	.L169
	cmp	ecx, r8d
	jl	.L199
.L166:
	movq	QWORD PTR 0[rbp], xmm1
	mov	r9d, DWORD PTR -4[r11]
.L165:
	cmp	edx, ecx
	mov	r10, r11
	mov	rax, rsi
	jge	.L187
	.p2align 4,,10
	.p2align 3
.L201:
	add	rax, 4
	.p2align 4,,10
	.p2align 3
.L171:
	mov	rdi, rax
	mov	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	edx, ecx
	jl	.L171
	cmp	r9d, ecx
	jle	.L172
.L202:
	lea	rax, -8[r10]
	.p2align 4,,10
	.p2align 3
.L173:
	mov	r10, rax
	mov	r9d, DWORD PTR [rax]
	sub	rax, 4
	cmp	r9d, ecx
	jg	.L173
	cmp	rdi, r10
	jnb	.L200
.L175:
	mov	DWORD PTR [rdi], r9d
	lea	rax, 4[rdi]
	mov	r9d, DWORD PTR -4[r10]
	mov	DWORD PTR [r10], edx
	mov	ecx, DWORD PTR 0[rbp]
	mov	edx, DWORD PTR 4[rdi]
	cmp	edx, ecx
	jl	.L201
.L187:
	cmp	r9d, ecx
	mov	rdi, rax
	jg	.L202
	.p2align 4,,10
	.p2align 3
.L172:
	sub	r10, 4
	cmp	rdi, r10
	jb	.L175
	.p2align 4,,10
	.p2align 3
.L200:
	mov	r9, rbx
	mov	r8, r12
	mov	rdx, r11
	mov	QWORD PTR 32[rsp], r14
	mov	rcx, rdi
	mov	QWORD PTR 40[rsp], r15
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_
	mov	rax, rdi
	sub	rax, rbp
	cmp	rax, 64
	jle	.L133
	test	r12, r12
	je	.L177
	mov	r11, rdi
	jmp	.L136
.L163:
	cmp	ecx, r8d
	jl	.L166
	cmp	eax, r8d
	jge	.L169
.L199:
	mov	DWORD PTR 0[rbp], r8d
	mov	r9d, edx
	mov	DWORD PTR -4[r11], edx
	mov	ecx, DWORD PTR 0[rbp]
	mov	edx, DWORD PTR 4[rbp]
	jmp	.L165
.L169:
	mov	DWORD PTR 0[rbp], eax
	mov	DWORD PTR [r9], edx
	mov	edx, DWORD PTR 4[rbp]
	mov	ecx, DWORD PTR 0[rbp]
	mov	r9d, DWORD PTR -4[r11]
	jmp	.L165
.L147:
	sub	rdi, 4
	.p2align 4,,10
	.p2align 3
.L162:
	mov	r9, rdi
	mov	eax, DWORD PTR 0[rbp]
	sub	r9, rbp
	mov	r8d, DWORD PTR [rdi]
	mov	r12, r9
	sar	r12, 2
	lea	rdx, -1[r12]
	mov	DWORD PTR [rdi], eax
	mov	r14, r12
	mov	rax, rdx
	and	r14d, 1
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r9, 8
	mov	r13, rax
	jle	.L150
	xor	r10d, r10d
	jmp	.L152
	.p2align 4,,10
	.p2align 3
.L184:
	mov	r10, rax
.L152:
	lea	rdx, 1[r10]
	lea	rax, [rdx+rdx]
	lea	r11, -1[rax]
	lea	rbx, 0[rbp+r11*4]
	lea	rdx, 0[rbp+rdx*8]
	mov	esi, DWORD PTR [rbx]
	mov	ecx, DWORD PTR [rdx]
	cmp	esi, ecx
	jle	.L151
	mov	ecx, esi
	mov	rdx, rbx
	mov	rax, r11
.L151:
	cmp	rax, r13
	mov	DWORD PTR 0[rbp+r10*4], ecx
	jl	.L184
	test	r14, r14
	je	.L156
	lea	r10, -1[rax]
	mov	rcx, r10
	shr	rcx, 63
	add	rcx, r10
	sar	rcx
	test	rax, rax
	jne	.L160
	jmp	.L203
	.p2align 4,,10
	.p2align 3
.L205:
	mov	DWORD PTR [rdx], r10d
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	test	rcx, rcx
	mov	rdx, rax
	mov	rax, rcx
	je	.L204
	mov	rcx, rdx
.L160:
	lea	r11, 0[rbp+rcx*4]
	mov	r10d, DWORD PTR [r11]
	lea	rdx, 0[rbp+rax*4]
	cmp	r8d, r10d
	jg	.L205
.L155:
	sub	rdi, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L162
.L133:
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
.L177:
	sar	rax, 2
	lea	rsi, -2[rax]
	lea	r11, -1[rax]
	sar	rsi
	not	rax
	sar	r11
	mov	r9d, eax
	mov	r8, rsi
	lea	rbx, 0[rbp+rsi*4]
	and	r9d, 1
	cmp	r8, r11
	mov	r10d, DWORD PTR [rbx]
	mov	r12, rbx
	jge	.L181
.L209:
	mov	rcx, r8
	jmp	.L139
	.p2align 4,,10
	.p2align 3
.L182:
	mov	rcx, rax
.L139:
	lea	rdx, 1[rcx]
	lea	rax, [rdx+rdx]
	lea	r13, -1[rax]
	lea	r14, 0[rbp+r13*4]
	lea	r12, 0[rbp+rdx*8]
	mov	r15d, DWORD PTR [r14]
	mov	edx, DWORD PTR [r12]
	cmp	r15d, edx
	jle	.L138
	mov	edx, r15d
	mov	r12, r14
	mov	rax, r13
.L138:
	cmp	rax, r11
	mov	DWORD PTR 0[rbp+rcx*4], edx
	jl	.L182
.L137:
	cmp	rsi, rax
	jne	.L189
	test	r9b, r9b
	jne	.L140
.L189:
	lea	rcx, -1[rax]
	sar	rcx
	cmp	r8, rax
	jl	.L145
	jmp	.L206
	.p2align 4,,10
	.p2align 3
.L208:
	mov	DWORD PTR [rax], edx
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r8, rcx
	mov	rdx, rax
	mov	rax, rcx
	jge	.L207
	mov	rcx, rdx
.L145:
	lea	r12, 0[rbp+rcx*4]
	mov	edx, DWORD PTR [r12]
	lea	rax, 0[rbp+rax*4]
	cmp	r10d, edx
	jg	.L208
.L144:
	test	r8, r8
	mov	DWORD PTR [rax], r10d
	je	.L147
.L146:
	sub	r8, 1
	sub	rbx, 4
	mov	r10d, DWORD PTR [rbx]
	cmp	r8, r11
	mov	r12, rbx
	jl	.L209
.L181:
	mov	rax, r8
	jmp	.L137
.L207:
	mov	rax, r12
	jmp	.L144
.L204:
	mov	rdx, r11
	sub	rdi, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L162
	jmp	.L133
.L156:
	lea	rcx, -2[r12]
	sar	rcx
	cmp	rcx, rax
	je	.L159
	lea	r10, -1[rax]
	mov	rcx, r10
	shr	rcx, 63
	add	rcx, r10
	sar	rcx
	test	rax, rax
	jne	.L160
	jmp	.L155
	.p2align 4,,10
	.p2align 3
.L150:
	test	r14, r14
	jne	.L198
	cmp	rdx, 2
	ja	.L198
	xor	eax, eax
	mov	rdx, rbp
.L159:
	lea	r10, 1[rax+rax]
	mov	ecx, DWORD PTR 0[rbp+r10*4]
	mov	DWORD PTR [rdx], ecx
	mov	rcx, rax
	mov	rax, r10
	jmp	.L160
.L198:
	mov	rdx, rbp
	sub	rdi, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L162
	jmp	.L133
.L140:
	lea	rcx, [rax+rax]
	lea	rax, 1[rcx]
	sar	rcx
	lea	rdx, 0[rbp+rax*4]
	cmp	r8, rax
	mov	r13d, DWORD PTR [rdx]
	mov	DWORD PTR [r12], r13d
	mov	r12, rdx
	jl	.L145
.L206:
	mov	DWORD PTR [r12], r10d
	jmp	.L146
.L203:
	mov	DWORD PTR [rdx], r8d
	sub	rdi, 4
	jmp	.L162
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z10sort_plainRSt6vectorIiSaIiEE
	.def	_Z10sort_plainRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10sort_plainRSt6vectorIiSaIiEE
_Z10sort_plainRSt6vectorIiSaIiEE:
.LFB4344:
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
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	lea	rax, 62[rsp]
	lea	rdx, 63[rsp]
	movq	xmm0, rax
	cmp	rsi, rbp
	movq	xmm1, rdx
	punpcklqdq	xmm0, xmm1
	je	.L234
	mov	rdi, rsi
	mov	r8, -2
	sub	rdi, rbp
	mov	rax, rdi
	sar	rax, 2
	test	rax, rax
	je	.L212
	bsr	rax, rax
	cdqe
	lea	r8, [rax+rax]
.L212:
	lea	r9, 32[rsp]
	mov	rdx, rsi
	mov	rcx, rbp
	movaps	XMMWORD PTR 32[rsp], xmm0
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_
	lea	rbx, 4[rbp]
	cmp	rdi, 64
	jg	.L243
	cmp	rsi, rbx
	je	.L234
	mov	r12d, 4
	jmp	.L231
	.p2align 4,,10
	.p2align 3
.L244:
	mov	r8, rbx
	sub	r8, rbp
	cmp	r8, 4
	jle	.L226
	mov	rcx, r12
	mov	rdx, rbp
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L227:
	add	rbx, 4
	mov	DWORD PTR 0[rbp], edi
	cmp	rsi, rbx
	je	.L234
.L231:
	mov	edi, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	eax, DWORD PTR 0[rbp]
	cmp	edi, eax
	jl	.L244
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	edi, edx
	jge	.L229
	.p2align 4,,10
	.p2align 3
.L230:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	edi, edx
	jl	.L230
.L229:
	add	rbx, 4
	mov	DWORD PTR [rcx], edi
	cmp	rsi, rbx
	jne	.L231
.L234:
	add	rsp, 72
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L243:
	lea	rdi, 64[rbp]
	mov	r13d, 4
	jmp	.L220
	.p2align 4,,10
	.p2align 3
.L246:
	mov	r8, rbx
	sub	r8, rbp
	cmp	r8, 4
	jle	.L215
	mov	rcx, r13
	mov	rdx, rbp
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L216:
	add	rbx, 4
	mov	DWORD PTR 0[rbp], r12d
	cmp	rbx, rdi
	je	.L245
.L220:
	mov	r12d, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	eax, DWORD PTR 0[rbp]
	cmp	r12d, eax
	jl	.L246
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	r12d, edx
	jge	.L218
	.p2align 4,,10
	.p2align 3
.L219:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	r12d, edx
	jl	.L219
.L218:
	add	rbx, 4
	mov	DWORD PTR [rcx], r12d
	cmp	rbx, rdi
	jne	.L220
.L245:
	cmp	rsi, rdi
	je	.L234
	mov	ecx, DWORD PTR [rdi]
	lea	rax, -4[rdi]
	mov	edx, DWORD PTR -4[rdi]
	cmp	ecx, edx
	jge	.L233
	.p2align 4,,10
	.p2align 3
.L223:
	mov	DWORD PTR 4[rax], edx
	mov	r8, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ecx, edx
	jl	.L223
	add	rdi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rsi, rdi
	je	.L234
.L242:
	mov	ecx, DWORD PTR [rdi]
	lea	rax, -4[rdi]
	mov	edx, DWORD PTR -4[rdi]
	cmp	ecx, edx
	jl	.L223
.L233:
	mov	r8, rdi
	add	rdi, 4
	cmp	rsi, rdi
	mov	DWORD PTR [r8], ecx
	jne	.L242
	jmp	.L234
.L226:
	jne	.L227
	mov	DWORD PTR [rbx], eax
	jmp	.L227
.L215:
	jne	.L216
	mov	DWORD PTR [rbx], eax
	jmp	.L216
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	memmove;	.scl	2;	.type	32;	.endef
