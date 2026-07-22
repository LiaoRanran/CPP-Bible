	.file	"_ch132_lsm_toy.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.unlikely,"x"
	.align 2
	.def	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0:
.LFB5553:
	.seh_endprologue
	test	rcx, rcx
	je	.L1
	sub	rdx, rcx
	jmp	_ZdlPvy
.L1:
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z17skiplist_containsPK4Nodeii
	.def	_Z17skiplist_containsPK4Nodeii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17skiplist_containsPK4Nodeii
_Z17skiplist_containsPK4Nodeii:
.LFB4593:
	.seh_endprologue
	movsxd	rax, edx
	mov	rdx, QWORD PTR 8[rcx]
	test	eax, eax
	js	.L5
	lea	r9, -1[rax]
	lea	rcx, 0[0+rax*8]
	sub	r9, rax
	sal	r9, 3
	jmp	.L7
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L16:
	cmp	DWORD PTR [rax], r8d
	jge	.L6
	mov	rdx, QWORD PTR 8[rax]
.L7:
	mov	rax, QWORD PTR [rdx+rcx]
	test	rax, rax
	jne	.L16
.L6:
	sub	rcx, 8
	cmp	r9, rcx
	jne	.L7
.L5:
	mov	rax, QWORD PTR [rdx]
	test	rax, rax
	je	.L11
	cmp	DWORD PTR [rax], r8d
	jne	.L11
	mov	eax, DWORD PTR 4[rax]
	ret
.L11:
	mov	eax, -1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8run_findRK3Runi
	.def	_Z8run_findRK3Runi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8run_findRK3Runi
_Z8run_findRK3Runi:
.LFB4594:
	.seh_endprologue
	mov	r9d, DWORD PTR 16[rcx]
	sub	r9d, 1
	js	.L23
	mov	r11, QWORD PTR [rcx]
	xor	r8d, r8d
	jmp	.L22
	.p2align 4,,10
	.p2align 3
.L26:
	lea	r8d, 1[rax]
	cmp	r9d, r8d
	jl	.L23
.L22:
	mov	eax, r9d
	sub	eax, r8d
	sar	eax
	add	eax, r8d
	movsxd	r10, eax
	cmp	DWORD PTR [r11+r10*4], edx
	je	.L25
	jl	.L26
	lea	r9d, -1[rax]
	cmp	r9d, r8d
	jge	.L22
.L23:
	mov	eax, -1
	ret
	.p2align 4,,10
	.p2align 3
.L25:
	mov	rax, QWORD PTR 8[rcx]
	mov	eax, DWORD PTR [rax+r10*4]
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_append\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_
	.def	_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_
_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_:
.LFB4595:
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
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rcx]
	mov	rdi, QWORD PTR [rcx]
	mov	rax, rsi
	sub	rax, rdi
	mov	rbp, rdx
	sar	rax, 3
	mov	r13, rcx
	mov	r12, r8
	movabs	rdx, -6148914691236517205
	imul	rax, rdx
	mov	QWORD PTR 64[rsp], rax
	test	rax, rax
	je	.L48
	lea	r15, 0[0+rax*4]
	mov	rcx, r15
	mov	QWORD PTR 64[rsp], r15
.LEHB0:
	call	_Znwy
	mov	r8, r15
	xor	edx, edx
	mov	rbx, rax
	lea	rax, [rax+r15]
	mov	rcx, rbx
	mov	QWORD PTR 72[rsp], rax
	call	memset
.L28:
	movabs	r15, -6148914691236517205
	sub	rsi, rdi
	je	.L29
	.p2align 4
	.p2align 3
.L76:
	sar	rsi, 3
	mov	rcx, rdi
	mov	edx, -1
	xor	edi, edi
	imul	rsi, r15
	xor	eax, eax
	mov	r9, rsi
	mov	rsi, -1
	.p2align 4
	.p2align 3
.L32:
	movsxd	r8, DWORD PTR [rbx+rax*4]
	cmp	r8d, DWORD PTR 16[rcx]
	jge	.L30
	mov	r10, QWORD PTR [rcx]
	mov	r10d, DWORD PTR [r10+r8*4]
	cmp	edx, -1
	je	.L50
	cmp	r10d, edx
	jge	.L30
.L50:
	mov	rdx, QWORD PTR 8[rcx]
	movsxd	rsi, eax
	mov	edi, DWORD PTR [rdx+r8*4]
	mov	edx, r10d
.L30:
	add	rax, 1
	add	rcx, 24
	cmp	rax, r9
	jb	.L32
	cmp	esi, -1
	je	.L34
	mov	r8, QWORD PTR 8[rbp]
	mov	r9, QWORD PTR 16[rbp]
	cmp	r8, r9
	je	.L36
	mov	DWORD PTR [r8], edx
	add	r8, 4
	mov	r9, QWORD PTR 16[r12]
	mov	QWORD PTR 8[rbp], r8
	mov	rax, QWORD PTR 8[r12]
	cmp	rax, r9
	je	.L41
.L78:
	mov	DWORD PTR [rax], edi
	add	rax, 4
	mov	QWORD PTR 8[r12], rax
.L42:
	add	DWORD PTR [rbx+rsi*4], 1
	mov	rdi, QWORD PTR 0[r13]
	mov	rsi, QWORD PTR 8[r13]
	sub	rsi, rdi
	jne	.L76
.L29:
	test	rbx, rbx
	je	.L77
.L34:
	mov	rdx, QWORD PTR 64[rsp]
	mov	rcx, rbx
	add	rsp, 88
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	jmp	_ZdlPvy
.LEHE0:
	.p2align 4,,10
	.p2align 3
.L36:
	movabs	rcx, 2305843009213693951
	mov	r11, QWORD PTR 0[rbp]
	sub	r8, r11
	mov	rax, r8
	sar	rax, 2
	cmp	rax, rcx
	je	.L72
	test	rax, rax
	mov	r14d, 1
	mov	QWORD PTR 56[rsp], r8
	cmovne	r14, rax
	mov	QWORD PTR 48[rsp], r11
	mov	QWORD PTR 40[rsp], r9
	add	r14, rax
	mov	DWORD PTR 32[rsp], edx
	movabs	rax, 2305843009213693951
	cmp	r14, rax
	cmova	r14, rax
	sal	r14, 2
	mov	rcx, r14
.LEHB1:
	call	_Znwy
	mov	r8, QWORD PTR 56[rsp]
	mov	edx, DWORD PTR 32[rsp]
	mov	r10, rax
	mov	r9, QWORD PTR 40[rsp]
	mov	r11, QWORD PTR 48[rsp]
	test	r8, r8
	mov	DWORD PTR [rax+r8], edx
	je	.L39
	mov	rdx, r11
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], r9
	mov	QWORD PTR 40[rsp], r8
	mov	QWORD PTR 32[rsp], r11
	call	memcpy
	mov	r9, QWORD PTR 48[rsp]
	mov	r8, QWORD PTR 40[rsp]
	mov	r11, QWORD PTR 32[rsp]
	mov	r10, rax
.L39:
	lea	rax, 4[r10+r8]
	test	r11, r11
	je	.L40
	mov	rdx, r9
	mov	rcx, r11
	mov	QWORD PTR 40[rsp], r10
	sub	rdx, r11
	mov	QWORD PTR 32[rsp], rax
	call	_ZdlPvy
	mov	r10, QWORD PTR 40[rsp]
	mov	rax, QWORD PTR 32[rsp]
.L40:
	mov	QWORD PTR 0[rbp], r10
	add	r10, r14
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR 8[r12]
	mov	QWORD PTR 16[rbp], r10
	mov	r9, QWORD PTR 16[r12]
	cmp	rax, r9
	jne	.L78
	.p2align 4
	.p2align 3
.L41:
	movabs	rdx, 2305843009213693951
	mov	r11, QWORD PTR [r12]
	sub	rax, r11
	mov	r8, rax
	sar	rax, 2
	cmp	rax, rdx
	je	.L73
	test	rax, rax
	mov	r14d, 1
	mov	QWORD PTR 48[rsp], r8
	cmovne	r14, rax
	mov	QWORD PTR 40[rsp], r11
	mov	QWORD PTR 32[rsp], r9
	add	r14, rax
	movabs	rax, 2305843009213693951
	cmp	r14, rax
	cmova	r14, rax
	sal	r14, 2
	mov	rcx, r14
	call	_Znwy
.LEHE1:
	mov	r8, QWORD PTR 48[rsp]
	mov	r9, QWORD PTR 32[rsp]
	mov	r10, rax
	mov	r11, QWORD PTR 40[rsp]
	test	r8, r8
	mov	DWORD PTR [rax+r8], edi
	je	.L44
	mov	rdx, r11
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], r9
	mov	QWORD PTR 40[rsp], r8
	mov	QWORD PTR 32[rsp], r11
	call	memcpy
	mov	r9, QWORD PTR 48[rsp]
	mov	r8, QWORD PTR 40[rsp]
	mov	r11, QWORD PTR 32[rsp]
	mov	r10, rax
.L44:
	lea	rdi, 4[r10+r8]
	test	r11, r11
	je	.L45
	mov	rdx, r9
	mov	rcx, r11
	mov	QWORD PTR 32[rsp], r10
	sub	rdx, r11
	call	_ZdlPvy
	mov	r10, QWORD PTR 32[rsp]
.L45:
	mov	QWORD PTR [r12], r10
	add	r10, r14
	mov	QWORD PTR 8[r12], rdi
	mov	QWORD PTR 16[r12], r10
	jmp	.L42
.L77:
	add	rsp, 88
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L48:
	mov	QWORD PTR 72[rsp], 0
	xor	ebx, ebx
	jmp	.L28
.L70:
	jmp	.L71
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4595:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4595-.LLSDACSB4595
.LLSDACSB4595:
	.uleb128 .LEHB0-.LFB4595
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB4595
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L70-.LFB4595
	.uleb128 0
.LLSDACSE4595:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_.cold
	.seh_stackalloc	152
	.seh_savereg	rbx, 88
	.seh_savereg	rsi, 96
	.seh_savereg	rdi, 104
	.seh_savereg	rbp, 112
	.seh_savereg	r12, 120
	.seh_savereg	r13, 128
	.seh_savereg	r14, 136
	.seh_savereg	r15, 144
	.seh_endprologue
_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_.cold:
.L72:
	lea	rcx, .LC0[rip]
.LEHB2:
	call	_ZSt20__throw_length_errorPKc
.L73:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE2:
.L49:
.L71:
	mov	rdx, QWORD PTR 72[rsp]
	mov	rsi, rax
	mov	rcx, rbx
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
	mov	rcx, rsi
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4595:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4595-.LLSDACSBC4595
.LLSDACSBC4595:
	.uleb128 .LEHB2-.LCOLDB1
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L49-.LCOLDB1
	.uleb128 0
	.uleb128 .LEHB3-.LCOLDB1
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSEC4595:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text$_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
	.def	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv:
.LFB5190:
	sub	rsp, 24
	.seh_stackalloc	24
	movaps	XMMWORD PTR [rsp], xmm6
	.seh_savexmm	xmm6, 0
	.seh_endprologue
	pcmpeqd	xmm3, xmm3
	movdqa	xmm5, xmm3
	movdqa	xmm4, xmm3
	pslld	xmm5, 31
	psrld	xmm4, 1
	psrld	xmm3, 31
	mov	r9, rcx
	lea	rdx, 896[rcx]
	mov	rax, rcx
	.p2align 4
	.p2align 3
.L80:
	movdqu	xmm1, XMMWORD PTR [rax]
	movdqu	xmm0, XMMWORD PTR 4[rax]
	add	rax, 16
	movdqu	xmm2, XMMWORD PTR 1572[rax]
	pand	xmm0, xmm4
	pand	xmm1, xmm5
	por	xmm1, xmm0
	movdqa	xmm0, xmm1
	pand	xmm1, xmm3
	psrld	xmm0, 1
	pxor	xmm2, xmm0
	movdqa	xmm0, xmm1
	pslld	xmm0, 3
	paddd	xmm0, xmm1
	pslld	xmm0, 9
	paddd	xmm0, xmm1
	pslld	xmm0, 5
	paddd	xmm0, xmm1
	pslld	xmm0, 2
	psubd	xmm0, xmm1
	pslld	xmm0, 3
	psubd	xmm0, xmm1
	movdqa	xmm6, xmm0
	pslld	xmm6, 4
	paddd	xmm0, xmm6
	pslld	xmm0, 5
	psubd	xmm0, xmm1
	pxor	xmm2, xmm0
	movups	XMMWORD PTR -16[rax], xmm2
	cmp	rdx, rax
	jne	.L80
	mov	r10d, DWORD PTR 896[r9]
	lea	rax, 908[r9]
.L81:
	and	r10d, -2147483648
	add	rdx, 4
	mov	r8d, r10d
	mov	r10d, DWORD PTR [rdx]
	mov	ecx, r10d
	and	ecx, 2147483647
	or	ecx, r8d
	mov	r8d, ecx
	and	ecx, 1
	neg	ecx
	shr	r8d
	xor	r8d, DWORD PTR 1584[rdx]
	and	ecx, -1727483681
	xor	ecx, r8d
	mov	DWORD PTR -4[rdx], ecx
	cmp	rdx, rax
	jne	.L81
	pcmpeqd	xmm3, xmm3
	lea	rdx, 2492[r9]
	movdqa	xmm5, xmm3
	movdqa	xmm4, xmm3
	pslld	xmm5, 31
	psrld	xmm4, 1
	psrld	xmm3, 31
	.p2align 4
	.p2align 3
.L82:
	movdqu	xmm1, XMMWORD PTR [rax]
	movdqu	xmm0, XMMWORD PTR 4[rax]
	add	rax, 16
	movdqu	xmm2, XMMWORD PTR -924[rax]
	pand	xmm0, xmm4
	pand	xmm1, xmm5
	por	xmm1, xmm0
	movdqa	xmm0, xmm1
	pand	xmm1, xmm3
	psrld	xmm0, 1
	pxor	xmm2, xmm0
	movdqa	xmm0, xmm1
	pslld	xmm0, 3
	paddd	xmm0, xmm1
	pslld	xmm0, 9
	paddd	xmm0, xmm1
	pslld	xmm0, 5
	paddd	xmm0, xmm1
	pslld	xmm0, 2
	psubd	xmm0, xmm1
	pslld	xmm0, 3
	psubd	xmm0, xmm1
	movdqa	xmm6, xmm0
	pslld	xmm6, 4
	paddd	xmm0, xmm6
	pslld	xmm0, 5
	psubd	xmm0, xmm1
	pxor	xmm2, xmm0
	movups	XMMWORD PTR -16[rax], xmm2
	cmp	rdx, rax
	jne	.L82
	mov	eax, DWORD PTR 2492[r9]
	mov	edx, DWORD PTR [r9]
	mov	QWORD PTR 2496[r9], 0
	movaps	xmm6, XMMWORD PTR [rsp]
	and	edx, 2147483647
	and	eax, -2147483648
	or	eax, edx
	mov	edx, eax
	and	eax, 1
	neg	eax
	shr	edx
	xor	edx, DWORD PTR 1584[r9]
	and	eax, -1727483681
	xor	eax, edx
	mov	DWORD PTR 2492[r9], eax
	add	rsp, 24
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB5:
	.text
.LHOTB5:
	.p2align 4
	.globl	_Z4demoi
	.def	_Z4demoi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4demoi
_Z4demoi:
.LFB4602:
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
	sub	rsp, 2704
	.seh_stackalloc	2704
	.seh_endprologue
	mov	ebx, 1
	mov	DWORD PTR 192[rsp], ecx
	lea	rdx, 196[rsp]
	.p2align 6
	.p2align 4
	.p2align 3
.L87:
	mov	eax, ecx
	add	rdx, 4
	shr	eax, 30
	xor	eax, ecx
	imul	eax, eax, 1812433253
	lea	ecx, [rax+rbx]
	add	rbx, 1
	mov	DWORD PTR -4[rdx], ecx
	cmp	rbx, 624
	jne	.L87
	mov	ecx, 32
	mov	QWORD PTR 2688[rsp], 624
.LEHB4:
	call	_Znwy
.LEHE4:
	pxor	xmm0, xmm0
	mov	ecx, 32
	mov	DWORD PTR [rax], 0
	mov	rsi, rax
	movups	XMMWORD PTR 4[rax], xmm0
	movups	XMMWORD PTR 16[rax], xmm0
.LEHB5:
	call	_Znwy
.LEHE5:
	mov	DWORD PTR [rax], 0
	pxor	xmm0, xmm0
	mov	ecx, 32
	mov	rdi, rax
	movups	XMMWORD PTR 4[rax], xmm0
	movups	XMMWORD PTR 16[rax], xmm0
.LEHB6:
	call	_Znwy
.LEHE6:
	mov	DWORD PTR [rax], 0
	pxor	xmm0, xmm0
	mov	ecx, 32
	mov	rbp, rax
	movups	XMMWORD PTR 4[rax], xmm0
	movups	XMMWORD PTR 16[rax], xmm0
.LEHB7:
	call	_Znwy
.LEHE7:
	pxor	xmm0, xmm0
	mov	DWORD PTR [rax], 0
	mov	r12, rax
	xor	r14d, r14d
	movups	XMMWORD PTR 4[rax], xmm0
	movups	XMMWORD PTR 16[rax], xmm0
	jmp	.L89
	.p2align 4,,10
	.p2align 3
.L88:
	lea	rbx, 1[rax]
	mov	eax, DWORD PTR 192[rsp+rax*4]
	mov	QWORD PTR 2688[rsp], rbx
	mov	edx, eax
	shr	edx, 11
	xor	eax, edx
	mov	edx, eax
	sal	edx, 7
	and	edx, -1658038656
	xor	eax, edx
	mov	edx, eax
	sal	edx, 15
	and	edx, -272236544
	xor	eax, edx
	mov	edx, eax
	shr	edx, 18
	xor	eax, edx
	mov	edx, eax
	imul	rdx, rdx, 1374389535
	shr	rdx, 37
	imul	edx, edx, 100
	sub	eax, edx
	mov	DWORD PTR [rdi+r14*4], eax
	add	r14, 1
	cmp	r14, 8
	je	.L122
.L89:
	lea	eax, [r14+r14]
	mov	DWORD PTR [rsi+r14*4], eax
	mov	rax, rbx
	cmp	rbx, 623
	jbe	.L88
	lea	rcx, 192[rsp]
	call	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
	mov	rax, QWORD PTR 2688[rsp]
	jmp	.L88
	.p2align 4,,10
	.p2align 3
.L122:
	xor	r14d, r14d
	jmp	.L91
	.p2align 4,,10
	.p2align 3
.L90:
	lea	rbx, 1[rax]
	mov	eax, DWORD PTR 192[rsp+rax*4]
	mov	QWORD PTR 2688[rsp], rbx
	mov	edx, eax
	shr	edx, 11
	xor	eax, edx
	mov	edx, eax
	sal	edx, 7
	and	edx, -1658038656
	xor	eax, edx
	mov	edx, eax
	sal	edx, 15
	and	edx, -272236544
	xor	eax, edx
	mov	edx, eax
	shr	edx, 18
	xor	eax, edx
	mov	edx, eax
	imul	rdx, rdx, 1374389535
	shr	rdx, 37
	imul	edx, edx, 100
	sub	eax, edx
	mov	DWORD PTR [r12+r14*4], eax
	add	r14, 1
	cmp	r14, 8
	je	.L123
.L91:
	lea	eax, 1[r14+r14]
	mov	DWORD PTR 0[rbp+r14*4], eax
	mov	rax, rbx
	cmp	rbx, 623
	jbe	.L90
	lea	rcx, 192[rsp]
	call	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
	mov	rax, QWORD PTR 2688[rsp]
	jmp	.L90
	.p2align 4,,10
	.p2align 3
.L123:
	mov	QWORD PTR 48[rsp], rsi
	mov	ecx, 48
	mov	QWORD PTR 56[rsp], rdi
	movdqa	xmm1, XMMWORD PTR 48[rsp]
	mov	QWORD PTR 64[rsp], 8
	mov	QWORD PTR 160[rsp], 8
	mov	QWORD PTR 168[rsp], rbp
	mov	QWORD PTR 176[rsp], r12
	mov	DWORD PTR 184[rsp], 8
	movaps	XMMWORD PTR 144[rsp], xmm1
.LEHB8:
	call	_Znwy
.LEHE8:
	movdqa	xmm2, XMMWORD PTR 144[rsp]
	mov	rbx, rax
	mov	QWORD PTR 80[rsp], rax
	pxor	xmm0, xmm0
	lea	rax, 48[rax]
	lea	rdx, 112[rsp]
	movaps	XMMWORD PTR 112[rsp], xmm0
	movdqa	xmm3, XMMWORD PTR 160[rsp]
	movups	XMMWORD PTR [rbx], xmm2
	lea	rcx, 80[rsp]
	movdqa	xmm4, XMMWORD PTR 176[rsp]
	lea	r8, 144[rsp]
	movups	XMMWORD PTR 16[rbx], xmm3
	movups	XMMWORD PTR 32[rbx], xmm4
	mov	QWORD PTR 96[rsp], rax
	mov	QWORD PTR 88[rsp], rax
	mov	QWORD PTR 152[rsp], 0
	mov	QWORD PTR 128[rsp], 0
	mov	QWORD PTR 144[rsp], 0
	mov	QWORD PTR 160[rsp], 0
.LEHB9:
	call	_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_
.LEHE9:
	mov	r14, QWORD PTR 112[rsp]
	mov	r11, QWORD PTR 120[rsp]
	xor	edx, edx
	mov	r10d, 7
	mov	r9, QWORD PTR 144[rsp]
	mov	r8, QWORD PTR 128[rsp]
	jmp	.L96
	.p2align 4,,10
	.p2align 3
.L126:
	lea	edx, 1[rax]
	cmp	edx, r10d
	jg	.L124
.L96:
	mov	eax, r10d
	sub	eax, edx
	sar	eax
	add	eax, edx
	movsxd	r13, eax
	mov	ecx, DWORD PTR [rsi+r13*4]
	cmp	ecx, 6
	je	.L125
	cmp	ecx, 5
	jle	.L126
	lea	r10d, -1[rax]
	cmp	edx, r10d
	jle	.L96
.L124:
	mov	r13d, -2
.L93:
	sub	r11, r14
	sar	r11, 2
	add	r13d, r11d
	test	r9, r9
	je	.L97
	mov	rdx, QWORD PTR 160[rsp]
	mov	rcx, r9
	mov	QWORD PTR 40[rsp], r8
	sub	rdx, r9
	call	_ZdlPvy
	mov	r8, QWORD PTR 40[rsp]
.L97:
	test	r14, r14
	je	.L98
	mov	rdx, r8
	mov	rcx, r14
	sub	rdx, r14
	call	_ZdlPvy
.L98:
	mov	rcx, rbx
	mov	edx, 48
	call	_ZdlPvy
	mov	rcx, r12
	mov	edx, 32
	call	_ZdlPvy
	mov	rcx, rbp
	mov	edx, 32
	call	_ZdlPvy
	mov	rcx, rdi
	mov	edx, 32
	call	_ZdlPvy
	mov	edx, 32
	mov	rcx, rsi
	call	_ZdlPvy
	mov	eax, r13d
	add	rsp, 2704
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
.L125:
	mov	r13d, DWORD PTR [rdi+r13*4]
	sub	r13d, 1
	jmp	.L93
.L110:
	jmp	.L99
.L109:
	mov	rbx, rax
	jmp	.L100
.L107:
	mov	rbx, rax
	jmp	.L102
.L108:
	mov	rbx, rax
	jmp	.L101
.L106:
	mov	rbx, rax
	jmp	.L103
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4602:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4602-.LLSDACSB4602
.LLSDACSB4602:
	.uleb128 .LEHB4-.LFB4602
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB5-.LFB4602
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L106-.LFB4602
	.uleb128 0
	.uleb128 .LEHB6-.LFB4602
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L107-.LFB4602
	.uleb128 0
	.uleb128 .LEHB7-.LFB4602
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L108-.LFB4602
	.uleb128 0
	.uleb128 .LEHB8-.LFB4602
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L109-.LFB4602
	.uleb128 0
	.uleb128 .LEHB9-.LFB4602
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L110-.LFB4602
	.uleb128 0
.LLSDACSE4602:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z4demoi.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z4demoi.cold
	.seh_stackalloc	2760
	.seh_savereg	rbx, 2704
	.seh_savereg	rsi, 2712
	.seh_savereg	rdi, 2720
	.seh_savereg	rbp, 2728
	.seh_savereg	r12, 2736
	.seh_savereg	r13, 2744
	.seh_savereg	r14, 2752
	.seh_endprologue
_Z4demoi.cold:
.L99:
	mov	r14, QWORD PTR 112[rsp]
	mov	r13, QWORD PTR 128[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	rdx, QWORD PTR 160[rsp]
	mov	rcx, QWORD PTR 144[rsp]
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
	mov	rdx, r13
	mov	rcx, r14
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
	mov	rcx, rbx
	mov	edx, 48
	call	_ZdlPvy
	mov	rbx, QWORD PTR 40[rsp]
.L100:
	lea	rdx, 32[r12]
	mov	rcx, r12
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
.L101:
	lea	rdx, 32[rbp]
	mov	rcx, rbp
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
.L102:
	lea	rdx, 32[rdi]
	mov	rcx, rdi
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
.L103:
	mov	rcx, rsi
	lea	rdx, 32[rsi]
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
	mov	rcx, rbx
.LEHB10:
	call	_Unwind_Resume
	nop
.LEHE10:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4602:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4602-.LLSDACSBC4602
.LLSDACSBC4602:
	.uleb128 .LEHB10-.LCOLDB5
	.uleb128 .LEHE10-.LEHB10
	.uleb128 0
	.uleb128 0
.LLSDACSEC4602:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE5:
	.text
.LHOTE5:
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4627:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	ecx, 42
	add	rsp, 40
	jmp	_Z4demoi
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
