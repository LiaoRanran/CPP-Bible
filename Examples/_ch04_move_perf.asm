	.file	"_ch04_move_perf.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.unlikely,"x"
	.align 2
	.def	_ZNSt6vectorI13OwnedThrowingSaIS0_EE12_Guard_allocD1Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI13OwnedThrowingSaIS0_EE12_Guard_allocD1Ev.isra.0
_ZNSt6vectorI13OwnedThrowingSaIS0_EE12_Guard_allocD1Ev.isra.0:
.LFB15937:
	.seh_endprologue
	test	rcx, rcx
	je	.L1
	sal	rdx, 3
	jmp	_ZdlPvy
.L1:
	ret
	.seh_endproc
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.def	_ZL14bench_vec_copyii;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL14bench_vec_copyii
_ZL14bench_vec_copyii:
.LFB13354:
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
	xor	ebp, ebp
	xor	r12d, r12d
	movsxd	rcx, ecx
	mov	r13d, edx
	lea	rdi, 0[0+rcx*4]
	.p2align 4
	.p2align 3
.L8:
	mov	rcx, rdi
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	rsi, rax
	lea	rbx, [rax+rdi]
	test	dil, 4
	je	.L5
	mov	DWORD PTR [rax], 42
	lea	rax, 4[rax]
	cmp	rbx, rax
	je	.L19
	.p2align 5
	.p2align 4
	.p2align 3
.L5:
	mov	DWORD PTR [rax], 42
	add	rax, 8
	mov	DWORD PTR -4[rax], 42
	cmp	rbx, rax
	jne	.L5
.L19:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r14, rax
	sub	rbx, rsi
	je	.L21
	mov	rcx, rbx
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	rdx, rsi
	mov	rcx, rax
	mov	r8, rbx
	mov	r15, rax
	call	memcpy
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rdx, rbx
	mov	rcx, r15
	sub	rax, r14
	add	r12, rax
	call	_ZdlPvy
.L7:
	mov	rdx, rdi
	mov	rcx, rsi
	add	ebp, 1
	call	_ZdlPvy
	cmp	r13d, ebp
	jne	.L8
	pxor	xmm0, xmm0
	pxor	xmm1, xmm1
	cvtsi2sd	xmm0, r12
	cvtsi2sd	xmm1, r13d
	divsd	xmm0, xmm1
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
	.p2align 4,,10
	.p2align 3
.L21:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	sub	rax, r14
	add	r12, rax
	jmp	.L7
.L10:
	mov	rbx, rax
	jmp	.L9
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA13354:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE13354-.LLSDACSB13354
.LLSDACSB13354:
	.uleb128 .LEHB0-.LFB13354
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB13354
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L10-.LFB13354
	.uleb128 0
.LLSDACSE13354:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZL14bench_vec_copyii.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL14bench_vec_copyii.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 40
	.seh_savereg	rsi, 48
	.seh_savereg	rdi, 56
	.seh_savereg	rbp, 64
	.seh_savereg	r12, 72
	.seh_savereg	r13, 80
	.seh_savereg	r14, 88
	.seh_savereg	r15, 96
	.seh_endprologue
_ZL14bench_vec_copyii.cold:
.L9:
	mov	rcx, rsi
	mov	rdx, rdi
	call	_ZdlPvy
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC13354:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC13354-.LLSDACSBC13354
.LLSDACSBC13354:
	.uleb128 .LEHB2-.LCOLDB0
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC13354:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.text
.LHOTE0:
	.p2align 4
	.globl	_Z6mv_vecSt6vectorIiSaIiEE
	.def	_Z6mv_vecSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6mv_vecSt6vectorIiSaIiEE
_Z6mv_vecSt6vectorIiSaIiEE:
.LFB13307:
	.seh_endprologue
	movdqu	xmm0, XMMWORD PTR [rdx]
	mov	rax, rcx
	movups	XMMWORD PTR [rcx], xmm0
	mov	rcx, QWORD PTR 16[rdx]
	pxor	xmm0, xmm0
	mov	QWORD PTR 16[rdx], 0
	mov	QWORD PTR 16[rax], rcx
	movups	XMMWORD PTR [rdx], xmm0
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL19bench_vec_move_calliiid;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL19bench_vec_move_calliiid
_ZL19bench_vec_move_calliiid:
.LFB13341:
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
	sub	rsp, 216
	.seh_stackalloc	216
	movaps	XMMWORD PTR 176[rsp], xmm6
	.seh_savexmm	xmm6, 176
	movaps	XMMWORD PTR 192[rsp], xmm7
	.seh_savexmm	xmm7, 192
	.seh_endprologue
	xor	r10d, r10d
	xor	r15d, r15d
	mov	r9d, edx
	movapd	xmm7, xmm3
	.p2align 4
	.p2align 3
.L25:
	rdtsc
	xor	esi, esi
	mov	r11, rax
	sal	rdx, 32
	or	r11, rdx
	test	r9b, 1
	je	.L24
	mov	esi, 1
	cmp	r9d, 1
	je	.L57
	.p2align 4
	.p2align 3
.L24:
	add	esi, 2
	cmp	r9d, esi
	jne	.L24
.L57:
	rdtsc
	sal	rdx, 32
	sub	r15, r11
	lea	ebx, 1[r10]
	or	rax, rdx
	add	r15, rax
	cmp	r8d, ebx
	je	.L59
	mov	r10d, ebx
	jmp	.L25
	.p2align 4,,10
	.p2align 3
.L59:
	movsxd	r11, ecx
	mov	QWORD PTR 64[rsp], r15
	xor	r13d, r13d
	lea	rbp, 112[rsp]
	lea	rax, 0[0+r11*4]
	mov	DWORD PTR 76[rsp], ebx
	mov	QWORD PTR 56[rsp], rax
	mov	DWORD PTR 72[rsp], r10d
	mov	DWORD PTR 44[rsp], 0
	.p2align 4
	.p2align 3
.L31:
	mov	rbx, QWORD PTR 56[rsp]
	mov	rcx, rbx
	call	_Znwy
	lea	rcx, [rax+rbx]
	mov	rdx, rax
	mov	r9, rcx
	mov	r15, rcx
	sub	r9, rax
	and	r9d, 4
	je	.L26
	lea	rdx, 4[rax]
	mov	DWORD PTR [rax], 42
	cmp	rdx, rcx
	je	.L56
	.p2align 5
	.p2align 4
	.p2align 3
.L26:
	mov	DWORD PTR [rdx], 42
	add	rdx, 8
	mov	DWORD PTR -4[rdx], 42
	cmp	rdx, rcx
	jne	.L26
.L56:
	movq	xmm6, rax
	movq	xmm2, rcx
	punpcklqdq	xmm6, xmm2
	rdtsc
	xor	ebx, ebx
	mov	r10, rax
	sal	rdx, 32
	mov	QWORD PTR 48[rsp], r13
	or	r10, rdx
	mov	r14, r10
	.p2align 4
	.p2align 3
.L29:
	lea	rcx, 80[rsp]
	lea	rdx, 144[rsp]
	mov	QWORD PTR 160[rsp], r15
	movaps	XMMWORD PTR 144[rsp], xmm6
	call	_Z6mv_vecSt6vectorIiSaIiEE
	mov	rcx, QWORD PTR 144[rsp]
	test	rcx, rcx
	je	.L27
	mov	rdx, QWORD PTR 160[rsp]
	sub	rdx, rcx
	call	_ZdlPvy
.L27:
	movdqa	xmm0, XMMWORD PTR 80[rsp]
	mov	rax, QWORD PTR 96[rsp]
	mov	rdx, rbp
	lea	rcx, 144[rsp]
	mov	QWORD PTR 128[rsp], rax
	movaps	XMMWORD PTR 112[rsp], xmm0
	call	_Z6mv_vecSt6vectorIiSaIiEE
	mov	rcx, QWORD PTR 112[rsp]
	mov	rdx, QWORD PTR 128[rsp]
	mov	r13, QWORD PTR 144[rsp]
	mov	r15, QWORD PTR 160[rsp]
	movdqa	xmm6, XMMWORD PTR 144[rsp]
	test	rcx, rcx
	je	.L28
	sub	rdx, rcx
	call	_ZdlPvy
.L28:
	add	ebx, 1
	cmp	esi, ebx
	jne	.L29
	mov	r10, r14
	mov	r14, r13
	mov	r13, QWORD PTR 48[rsp]
	rdtsc
	sal	rdx, 32
	sub	r13, r10
	or	rax, rdx
	add	r13, rax
	test	r14, r14
	je	.L30
	mov	rdx, r15
	mov	rcx, r14
	sub	rdx, r14
	call	_ZdlPvy
.L30:
	mov	ebx, DWORD PTR 44[rsp]
	cmp	DWORD PTR 72[rsp], ebx
	je	.L60
	mov	eax, DWORD PTR 44[rsp]
	add	eax, 1
	mov	DWORD PTR 44[rsp], eax
	jmp	.L31
	.p2align 4,,10
	.p2align 3
.L60:
	mov	ebx, DWORD PTR 76[rsp]
	sub	r13, QWORD PTR 64[rsp]
	pxor	xmm0, xmm0
	pxor	xmm1, xmm1
	mov	eax, 0
	movaps	xmm6, XMMWORD PTR 176[rsp]
	cmovs	r13, rax
	imul	ebx, esi
	cvtsi2sd	xmm0, r13
	lea	eax, [rbx+rbx]
	cvtsi2sd	xmm1, eax
	divsd	xmm0, xmm1
	mulsd	xmm0, xmm7
	movaps	xmm7, XMMWORD PTR 192[rsp]
	add	rsp, 216
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6cp_vecRKSt6vectorIiSaIiEE
	.def	_Z6cp_vecRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6cp_vecRKSt6vectorIiSaIiEE
_Z6cp_vecRKSt6vectorIiSaIiEE:
.LFB13331:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	xor	r9d, r9d
	mov	rax, QWORD PTR 8[rdx]
	sub	rax, QWORD PTR [rdx]
	mov	r8, rax
	mov	rbx, rcx
	mov	rsi, rdx
	je	.L62
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], rax
	call	_Znwy
	mov	r8, QWORD PTR 40[rsp]
	mov	r9, rax
.L62:
	movq	xmm0, r9
	lea	rax, [r9+r8]
	punpcklqdq	xmm0, xmm0
	mov	QWORD PTR 16[rbx], rax
	movups	XMMWORD PTR [rbx], xmm0
	mov	rax, QWORD PTR [rsi]
	mov	rsi, QWORD PTR 8[rsi]
	sub	rsi, rax
	test	rsi, rsi
	jle	.L63
	mov	rcx, r9
	mov	r8, rsi
	mov	rdx, rax
	call	memcpy
	lea	r9, [rax+rsi]
.L63:
	mov	rax, rbx
	mov	QWORD PTR 8[rbx], r9
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9mv_assignRSt6vectorIiSaIiEES2_
	.def	_Z9mv_assignRSt6vectorIiSaIiEES2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9mv_assignRSt6vectorIiSaIiEES2_
_Z9mv_assignRSt6vectorIiSaIiEES2_:
.LFB13332:
	.seh_endprologue
	movdqu	xmm0, XMMWORD PTR [rdx]
	mov	rax, QWORD PTR [rcx]
	mov	r8, QWORD PTR 16[rcx]
	movups	XMMWORD PTR [rcx], xmm0
	mov	r9, QWORD PTR 16[rdx]
	pxor	xmm0, xmm0
	mov	QWORD PTR 16[rcx], r9
	mov	QWORD PTR 16[rdx], 0
	movups	XMMWORD PTR [rdx], xmm0
	test	rax, rax
	je	.L66
	mov	rdx, r8
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L66:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.def	_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:
.LFB13336:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	mov	r8, rcx
	lea	rcx, 16[rcx]
	mov	rax, rdx
	mov	QWORD PTR [r8], rcx
	mov	rdx, QWORD PTR [rdx]
	lea	r9, 16[rax]
	cmp	rdx, r9
	je	.L84
	mov	QWORD PTR [r8], rdx
	mov	rdx, QWORD PTR 16[rax]
	mov	QWORD PTR 16[r8], rdx
.L83:
	mov	rdx, QWORD PTR 8[rax]
.L76:
	mov	QWORD PTR 8[r8], rdx
	mov	QWORD PTR [rax], r9
	mov	QWORD PTR 8[rax], 0
	mov	BYTE PTR 16[rax], 0
	mov	rax, r8
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L84:
	mov	rdx, QWORD PTR 8[rax]
	lea	r10, 1[rdx]
	cmp	r10d, 8
	jnb	.L70
	test	r10b, 4
	jne	.L85
	test	r10d, r10d
	je	.L76
	movzx	edx, BYTE PTR 16[rax]
	mov	BYTE PTR 16[r8], dl
	test	r10b, 2
	je	.L83
	mov	r10d, r10d
	movzx	edx, WORD PTR -2[r9+r10]
	mov	WORD PTR -2[rcx+r10], dx
	mov	rdx, QWORD PTR 8[rax]
	jmp	.L76
	.p2align 4,,10
	.p2align 3
.L70:
	mov	rdx, QWORD PTR 16[rax]
	mov	QWORD PTR 16[r8], rdx
	mov	edx, r10d
	mov	r11, QWORD PTR -8[r9+rdx]
	mov	QWORD PTR -8[rcx+rdx], r11
	lea	rdx, 24[r8]
	mov	r11, r9
	and	rdx, -8
	sub	rcx, rdx
	add	r10d, ecx
	sub	r11, rcx
	and	r10d, -8
	mov	rsi, r11
	cmp	r10d, 8
	jb	.L83
	and	r10d, -8
	xor	ecx, ecx
.L74:
	mov	r11d, ecx
	add	ecx, 8
	mov	rbx, QWORD PTR [rsi+r11]
	mov	QWORD PTR [rdx+r11], rbx
	cmp	ecx, r10d
	jb	.L74
	jmp	.L83
.L85:
	mov	edx, DWORD PTR 16[rax]
	mov	r10d, r10d
	mov	DWORD PTR 16[r8], edx
	mov	edx, DWORD PTR -4[r9+r10]
	mov	DWORD PTR -4[rcx+r10], edx
	mov	rdx, QWORD PTR 8[rax]
	jmp	.L76
	.seh_endproc
	.p2align 4
	.globl	_Z7read_tlv
	.def	_Z7read_tlv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7read_tlv
_Z7read_tlv:
.LFB13338:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, __emutls_v.tl_var[rip]
	call	__emutls_get_address
	mov	eax, DWORD PTR [rax]
	add	rsp, 40
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8write_tli
	.def	_Z8write_tli;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8write_tli
_Z8write_tli:
.LFB13339:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	ebx, ecx
	lea	rcx, __emutls_v.tl_var[rip]
	call	__emutls_get_address
	mov	DWORD PTR [rax], ebx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8null_ptrv
	.def	_Z8null_ptrv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8null_ptrv
_Z8null_ptrv:
.LFB13340:
	.seh_endprologue
	xor	eax, eax
	ret
	.seh_endproc
	.section	.text$_ZSt8_DestroyIP13OwnedThrowingEvT_S2_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt8_DestroyIP13OwnedThrowingEvT_S2_
	.def	_ZSt8_DestroyIP13OwnedThrowingEvT_S2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt8_DestroyIP13OwnedThrowingEvT_S2_
_ZSt8_DestroyIP13OwnedThrowingEvT_S2_:
.LFB14497:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rbx, rcx
	mov	rsi, rdx
	cmp	rcx, rdx
	je	.L89
	.p2align 4
	.p2align 3
.L92:
	mov	rcx, QWORD PTR [rbx]
	test	rcx, rcx
	je	.L91
	call	_ZdaPv
.L91:
	add	rbx, 8
	cmp	rsi, rbx
	jne	.L92
.L89:
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section	.text$_ZNSt19_UninitDestroyGuardIP13OwnedThrowingvED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt19_UninitDestroyGuardIP13OwnedThrowingvED1Ev
	.def	_ZNSt19_UninitDestroyGuardIP13OwnedThrowingvED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_UninitDestroyGuardIP13OwnedThrowingvED1Ev
_ZNSt19_UninitDestroyGuardIP13OwnedThrowingvED1Ev:
.LFB14877:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	test	rax, rax
	jne	.L108
.L97:
	add	rsp, 48
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L108:
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rdx
	cmp	rdx, rax
	je	.L97
	.p2align 4
	.p2align 3
.L100:
	mov	rcx, QWORD PTR [rax]
	test	rcx, rcx
	je	.L99
	mov	QWORD PTR 40[rsp], rax
	call	_ZdaPv
	mov	rax, QWORD PTR 40[rsp]
.L99:
	add	rax, 8
	cmp	rbx, rax
	jne	.L100
	jmp	.L97
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC2:
	.ascii "=== ch04 move \350\257\255\344\271\211\347\234\237\345\256\236\345\237\272\345\207\206 (MinGW GCC 13.1.0 -O2 x86_64) ===\12\0"
.LC3:
	.ascii "[TSC] \0"
.LC5:
	.ascii " GHz | \0"
	.align 8
.LC6:
	.ascii "[\346\263\250] \346\225\260\345\200\274\351\232\217 CPU/\351\242\221\347\216\207/\345\270\246\345\256\275\345\217\230\345\214\226\357\274\214\344\273\205\344\273\243\350\241\250\346\234\254\346\234\272\357\274\233\345\200\215\346\225\260\344\274\230\345\212\277\347\250\263\345\256\232\12\12\0"
	.align 8
.LC7:
	.ascii "[vector<int>(1M)]  move(\345\220\253\350\260\203\347\224\250\345\274\200\351\224\200\344\270\212\347\225\214) = \0"
.LC8:
	.ascii " ns | copy = \0"
	.align 8
.LC9:
	.ascii " ns | (\347\272\257 move \344\273\205 3 \346\214\207\351\222\210\344\272\244\346\215\242, \350\247\201\351\231\204\345\275\225 H \346\261\207\347\274\226)\12\0"
	.align 8
.LC10:
	.ascii "[vector<int>(1K)]   move(\345\220\253\350\260\203\347\224\250\345\274\200\351\224\200\344\270\212\347\225\214) = \0"
.LC11:
	.ascii " ns\12\0"
	.align 8
.LC14:
	.ascii "[string(1KB)]      move(\345\220\253\350\260\203\347\224\250\345\274\200\351\224\200\344\270\212\347\225\214) = \0"
.LC15:
	.ascii "vector::_M_realloc_append\0"
	.align 8
.LC18:
	.ascii "[realloc 20K \345\205\203\347\264\240] Owned(noexcept move\342\206\222\346\265\205\347\247\273\345\212\250) = \0"
.LC19:
	.ascii " ns | \0"
	.align 8
.LC20:
	.ascii "OwnedThrowing(\351\235\236noexcept\342\206\222\346\267\261\346\213\267\350\264\235) = \0"
.LC21:
	.ascii " ns | \346\257\224 \342\211\210 \0"
.LC22:
	.ascii "x\12\0"
	.section	.text.unlikely,"x"
.LCOLDB24:
	.section	.text.startup,"x"
.LHOTB24:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB13440:
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
	sub	rsp, 280
	.seh_stackalloc	280
	movaps	XMMWORD PTR 240[rsp], xmm6
	.seh_savexmm	xmm6, 240
	movaps	XMMWORD PTR 256[rsp], xmm7
	.seh_savexmm	xmm7, 256
	.seh_endprologue
	call	__main
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rsi, rax
	rdtsc
	mov	rdi, rax
	sal	rdx, 32
	or	rdi, rdx
	rdtsc
	mov	rcx, rax
	sal	rdx, 32
	or	rcx, rdx
.L110:
	rdtsc
	sal	rdx, 32
	or	rax, rdx
	sub	rax, rcx
	cmp	rax, 299999999
	jbe	.L110
	rdtsc
	sal	rdx, 32
	mov	rbx, rax
	or	rbx, rdx
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	sub	rbx, rdi
	js	.L111
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rbx
.L112:
	movsd	xmm6, QWORD PTR .LC1[rip]
	sub	rax, rsi
	pxor	xmm1, xmm1
	xor	r14d, r14d
	cvtsi2sd	xmm1, rax
	mov	rsi, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC2[rip]
	divsd	xmm1, xmm6
	mov	rcx, rsi
	mov	QWORD PTR 64[rsp], rsi
	divsd	xmm0, xmm1
	divsd	xmm6, xmm0
.LEHB3:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC3[rip]
	mov	rcx, rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	xmm1, QWORD PTR .LC4[rip]
	mov	rcx, rax
	divsd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC5[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC6[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm3, xmm6
	mov	r8d, 200
	mov	edx, 3000
	mov	ecx, 1000000
	call	_ZL19bench_vec_move_calliiid
	mov	edx, 200
	mov	ecx, 1000000
	movsd	QWORD PTR 32[rsp], xmm0
	call	_ZL14bench_vec_copyii
	lea	rdx, .LC7[rip]
	mov	rcx, rsi
	movapd	xmm7, xmm0
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	xmm1, QWORD PTR 32[rsp]
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC8[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm7
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC9[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm3, xmm6
	mov	r8d, 150
	mov	edx, 4000
	mov	ecx, 1000
	call	_ZL19bench_vec_move_calliiid
	mov	edx, 50000
	mov	ecx, 1000
	movsd	QWORD PTR 32[rsp], xmm0
	call	_ZL14bench_vec_copyii
	lea	rdx, .LC10[rip]
	mov	rcx, rsi
	movapd	xmm7, xmm0
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	xmm1, QWORD PTR 32[rsp]
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC8[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm7
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC11[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	ecx, 150
.L114:
	rdtsc
	mov	r8, rax
	sal	rdx, 32
	mov	eax, 4000
	or	r8, rdx
	.p2align 4
	.p2align 3
.L113:
	sub	eax, 2
	jne	.L113
	rdtsc
	sal	rdx, 32
	sub	r14, r8
	or	rax, rdx
	add	r14, rax
	sub	ecx, 1
	jne	.L114
	lea	rax, 144[rsp]
	mov	DWORD PTR 48[rsp], 150
	lea	rbx, 224[rsp]
	movabs	r15, 8680820740569200760
	mov	QWORD PTR 32[rsp], rax
	lea	rax, 176[rsp]
	lea	rbp, 128[rsp]
	mov	QWORD PTR 104[rsp], rax
	lea	rsi, 208[rsp]
	lea	r12, 160[rsp]
	mov	QWORD PTR 72[rsp], r14
	lea	r13, 192[rsp]
	mov	r14, rax
	mov	QWORD PTR 40[rsp], 0
.L150:
	mov	ecx, 1025
	call	_Znwy
	mov	QWORD PTR 128[rsp], 1024
	lea	rdi, 8[rax]
	mov	rcx, rax
	mov	QWORD PTR 112[rsp], rax
	mov	rdx, rax
	and	rdi, -8
	mov	QWORD PTR [rax], r15
	sub	rcx, rdi
	mov	QWORD PTR 1016[rax], r15
	mov	rax, r15
	add	ecx, 1024
	shr	ecx, 3
	rep stosq
	mov	BYTE PTR 1024[rdx], 0
	mov	QWORD PTR 120[rsp], 1024
	rdtsc
	mov	edi, 4000
	sal	rdx, 32
	or	rax, rdx
	mov	QWORD PTR 56[rsp], rax
	jmp	.L148
	.p2align 4,,10
	.p2align 3
.L115:
	mov	QWORD PTR 208[rsp], rax
	mov	rax, QWORD PTR 128[rsp]
	mov	QWORD PTR 224[rsp], rax
.L122:
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 216[rsp], rdx
	mov	rdx, rsi
	mov	QWORD PTR 112[rsp], rbp
	mov	BYTE PTR 128[rsp], 0
	call	_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	mov	rcx, QWORD PTR 208[rsp]
	cmp	rcx, rbx
	je	.L123
	mov	rax, QWORD PTR 224[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L123:
	mov	rax, QWORD PTR 144[rsp]
	mov	QWORD PTR 208[rsp], rbx
	mov	rdx, QWORD PTR 152[rsp]
	cmp	rax, r12
	je	.L352
	mov	QWORD PTR 208[rsp], rax
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 224[rsp], rax
.L131:
	mov	QWORD PTR 216[rsp], rdx
	mov	rcx, r14
	mov	rdx, rsi
	mov	QWORD PTR 144[rsp], r12
	mov	BYTE PTR 160[rsp], 0
	call	_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	mov	rax, QWORD PTR 112[rsp]
	mov	rdx, rax
	cmp	rax, rbp
	je	.L353
	mov	rcx, QWORD PTR 176[rsp]
	cmp	rcx, r13
	je	.L220
	mov	rdx, QWORD PTR 128[rsp]
	mov	QWORD PTR 112[rsp], rcx
	movq	xmm0, QWORD PTR 184[rsp]
	movhps	xmm0, QWORD PTR 192[rsp]
	movups	XMMWORD PTR 120[rsp], xmm0
	test	rax, rax
	je	.L144
	mov	QWORD PTR 176[rsp], rax
	mov	QWORD PTR 192[rsp], rdx
.L143:
	mov	BYTE PTR [rax], 0
	mov	rcx, QWORD PTR 176[rsp]
	cmp	rcx, r13
	je	.L145
	mov	rax, QWORD PTR 192[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L145:
	mov	rcx, QWORD PTR 208[rsp]
	cmp	rcx, rbx
	je	.L146
	mov	rax, QWORD PTR 224[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L146:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, r12
	je	.L147
	mov	rax, QWORD PTR 160[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L147:
	sub	edi, 1
	je	.L354
.L148:
	mov	rax, QWORD PTR 112[rsp]
	mov	QWORD PTR 208[rsp], rbx
	mov	rdx, QWORD PTR 120[rsp]
	cmp	rax, rbp
	jne	.L115
	lea	r8, 1[rdx]
	mov	r9, rbx
	mov	rax, rbp
	cmp	r8d, 8
	jnb	.L355
.L116:
	xor	ecx, ecx
	test	r8b, 4
	je	.L119
	mov	ecx, DWORD PTR [rax]
	mov	DWORD PTR [r9], ecx
	mov	ecx, 4
.L119:
	test	r8b, 2
	je	.L120
	movzx	r10d, WORD PTR [rax+rcx]
	mov	WORD PTR [r9+rcx], r10w
	add	rcx, 2
.L120:
	and	r8d, 1
	je	.L122
	movzx	eax, BYTE PTR [rax+rcx]
	mov	BYTE PTR [r9+rcx], al
	jmp	.L122
.L353:
	mov	rax, QWORD PTR 176[rsp]
	cmp	rax, r13
	je	.L220
	movq	xmm0, QWORD PTR 184[rsp]
	mov	QWORD PTR 112[rsp], rax
	movhps	xmm0, QWORD PTR 192[rsp]
	movups	XMMWORD PTR 120[rsp], xmm0
.L144:
	mov	QWORD PTR 176[rsp], r13
	lea	r13, 192[rsp]
	mov	rax, r13
	jmp	.L143
.L220:
	mov	rax, QWORD PTR 184[rsp]
	test	rax, rax
	je	.L134
	cmp	rax, 1
	je	.L356
	mov	ecx, eax
	cmp	eax, 8
	jnb	.L137
	test	al, 4
	jne	.L357
	test	eax, eax
	je	.L134
	movzx	r8d, BYTE PTR 0[r13]
	mov	BYTE PTR [rdx], r8b
	test	al, 2
	jne	.L342
.L351:
	mov	rdx, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 184[rsp]
.L134:
	mov	QWORD PTR 120[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rax, QWORD PTR 176[rsp]
	jmp	.L143
.L352:
	lea	r8, 1[rdx]
	mov	r9, rbx
	mov	rax, r12
	cmp	r8d, 8
	jnb	.L358
.L125:
	xor	ecx, ecx
	test	r8b, 4
	je	.L128
	mov	ecx, DWORD PTR [rax]
	mov	DWORD PTR [r9], ecx
	mov	ecx, 4
.L128:
	test	r8b, 2
	je	.L129
	movzx	r10d, WORD PTR [rax+rcx]
	mov	WORD PTR [r9+rcx], r10w
	add	rcx, 2
.L129:
	and	r8d, 1
	je	.L131
	movzx	eax, BYTE PTR [rax+rcx]
	mov	BYTE PTR [r9+rcx], al
	jmp	.L131
.L354:
	rdtsc
	mov	rcx, QWORD PTR 112[rsp]
	mov	rdi, rax
	sal	rdx, 32
	or	rdi, rdx
	cmp	rcx, rbp
	je	.L149
	mov	rax, QWORD PTR 128[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L149:
	mov	rax, QWORD PTR 40[rsp]
	sub	rax, QWORD PTR 56[rsp]
	add	rax, rdi
	sub	DWORD PTR 48[rsp], 1
	mov	QWORD PTR 40[rsp], rax
	jne	.L150
	mov	DWORD PTR 48[rsp], 50000
	mov	r14, QWORD PTR 72[rsp]
	xor	r12d, r12d
	movabs	rbp, 8680820740569200760
	jmp	.L156
.L361:
	movzx	eax, BYTE PTR [rdi]
	mov	BYTE PTR 224[rsp], al
.L153:
	mov	QWORD PTR 216[rsp], r15
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rcx, QWORD PTR 208[rsp]
	mov	rdi, rax
	cmp	rcx, rbx
	je	.L154
	mov	rax, QWORD PTR 224[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L154:
	mov	rcx, QWORD PTR 176[rsp]
	cmp	rcx, r13
	je	.L155
	mov	rax, QWORD PTR 192[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L155:
	sub	rdi, QWORD PTR 56[rsp]
	add	r12, rdi
	sub	DWORD PTR 48[rsp], 1
	je	.L359
.L156:
	mov	ecx, 1025
	call	_Znwy
.LEHE3:
	mov	QWORD PTR 192[rsp], 1024
	lea	rdi, 8[rax]
	mov	rcx, rax
	mov	QWORD PTR 176[rsp], rax
	mov	rdx, rax
	and	rdi, -8
	mov	QWORD PTR [rax], rbp
	sub	rcx, rdi
	mov	QWORD PTR 1016[rax], rbp
	mov	rax, rbp
	add	ecx, 1024
	shr	ecx, 3
	rep stosq
	mov	QWORD PTR 184[rsp], 1024
	mov	BYTE PTR 1024[rdx], 0
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r15, QWORD PTR 184[rsp]
	mov	QWORD PTR 208[rsp], rbx
	mov	QWORD PTR 56[rsp], rax
	mov	rdi, QWORD PTR 176[rsp]
	lea	r8, 1[r15]
	cmp	r15, 15
	ja	.L360
	mov	rcx, rbx
	test	r15, r15
	je	.L361
	mov	rdx, rdi
	call	memcpy
	jmp	.L153
.L358:
	mov	r9d, r8d
	xor	eax, eax
	and	r9d, -8
.L126:
	mov	ecx, eax
	add	eax, 8
	mov	r10, QWORD PTR [r12+rcx]
	mov	QWORD PTR [rbx+rcx], r10
	cmp	eax, r9d
	jb	.L126
	lea	r9, [rbx+rax]
	add	rax, r12
	jmp	.L125
.L355:
	mov	r9d, r8d
	xor	eax, eax
	and	r9d, -8
.L117:
	mov	ecx, eax
	add	eax, 8
	mov	r10, QWORD PTR 0[rbp+rcx]
	mov	QWORD PTR [rbx+rcx], r10
	cmp	eax, r9d
	jb	.L117
	lea	r9, [rbx+rax]
	add	rax, rbp
	jmp	.L116
.L360:
	mov	rcx, r8
	mov	QWORD PTR 72[rsp], r8
.LEHB4:
	call	_Znwy
.LEHE4:
	mov	r8, QWORD PTR 72[rsp]
	mov	rcx, rax
	mov	rdx, rdi
	mov	QWORD PTR 208[rsp], rax
	mov	QWORD PTR 224[rsp], r15
	call	memcpy
	jmp	.L153
.L137:
	mov	rcx, QWORD PTR 0[r13]
	mov	QWORD PTR [rdx], rcx
	mov	ecx, eax
	mov	r8, QWORD PTR -8[r13+rcx]
	mov	QWORD PTR -8[rdx+rcx], r8
	lea	r8, 8[rdx]
	and	r8, -8
	sub	rdx, r8
	mov	rcx, rdx
	mov	rdx, r13
	sub	rdx, rcx
	add	ecx, eax
	and	ecx, -8
	cmp	ecx, 8
	jb	.L351
	and	ecx, -8
	xor	eax, eax
.L141:
	mov	r9d, eax
	add	eax, 8
	mov	r10, QWORD PTR [rdx+r9]
	mov	QWORD PTR [r8+r9], r10
	cmp	eax, ecx
	jb	.L141
	jmp	.L351
.L356:
	movzx	eax, BYTE PTR 192[rsp]
	mov	BYTE PTR [rdx], al
	mov	rdx, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 184[rsp]
	jmp	.L134
.L359:
	mov	rax, QWORD PTR 40[rsp]
	mov	edx, 0
	pxor	xmm1, xmm1
	mov	rcx, QWORD PTR 64[rsp]
	sub	rax, r14
	movabs	r14, 1152921504606846975
	cmovs	rax, rdx
	lea	rdx, .LC14[rip]
	cvtsi2sd	xmm1, rax
	divsd	xmm1, QWORD PTR .LC12[rip]
	mulsd	xmm1, xmm6
	pxor	xmm6, xmm6
	cvtsi2sd	xmm6, r12
	divsd	xmm6, QWORD PTR .LC13[rip]
	movsd	QWORD PTR 40[rsp], xmm1
.LEHB5:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	xmm1, QWORD PTR 40[rsp]
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC8[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm6
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC11[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE5:
	mov	DWORD PTR 40[rsp], 2000
	mov	QWORD PTR 56[rsp], 0
.L157:
	mov	ecx, 160000
.LEHB6:
	call	_Znwy
.LEHE6:
	mov	rbx, rax
	lea	rdi, 160000[rax]
	mov	rbp, rax
	mov	r12d, 20000
	.p2align 4
	.p2align 3
.L169:
	mov	ecx, 256
.LEHB7:
	call	_Znay
	mov	r13, rax
	cmp	rdi, rbx
	je	.L162
	mov	QWORD PTR [rbx], rax
	add	rbx, 8
.L163:
	sub	r12d, 1
	jne	.L169
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	ecx, 256
	mov	QWORD PTR 48[rsp], rax
	call	_Znay
.LEHE7:
	mov	r13, rax
	cmp	rbx, rdi
	je	.L170
	mov	QWORD PTR [rbx], rax
	add	rbx, 8
.L171:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r12, rbp
	sub	rax, QWORD PTR 48[rsp]
	add	QWORD PTR 56[rsp], rax
	cmp	rbp, rbx
	je	.L179
	.p2align 4
	.p2align 3
.L176:
	mov	rcx, QWORD PTR [r12]
	test	rcx, rcx
	je	.L178
	call	_ZdaPv
.L178:
	add	r12, 8
	cmp	r12, rbx
	jne	.L176
	test	rbp, rbp
	je	.L177
.L179:
	sub	rdi, rbp
	mov	rcx, rbp
	mov	rdx, rdi
	call	_ZdlPvy
.L177:
	sub	DWORD PTR 40[rsp], 1
	jne	.L157
	mov	DWORD PTR 100[rsp], 200
	mov	QWORD PTR 48[rsp], 0
.L180:
	mov	ecx, 160000
.LEHB8:
	call	_Znwy
.LEHE8:
	mov	rbx, rax
	lea	rbp, 160000[rax]
	mov	r12, rax
	mov	edi, 20000
	jmp	.L198
.L363:
	mov	QWORD PTR [rbx], rax
	add	rbx, 8
	sub	edi, 1
	je	.L362
.L198:
	mov	ecx, 256
.LEHB9:
	call	_Znay
.LEHE9:
	mov	r13, rax
	cmp	rbp, rbx
	jne	.L363
	movabs	rdx, 1152921504606846975
	mov	r15, rbp
	sub	r15, r12
	mov	rax, r15
	sar	rax, 3
	cmp	rax, rdx
	je	.L339
	test	rax, rax
	mov	edx, 1
	cmovne	rdx, rax
	add	rdx, rax
	movabs	rax, 1152921504606846975
	cmp	rdx, rax
	cmovbe	rax, rdx
	mov	QWORD PTR 72[rsp], rax
	sal	rax, 3
	mov	rcx, rax
	mov	QWORD PTR 88[rsp], rax
.LEHB10:
	call	_Znwy
.LEHE10:
	lea	rdx, [rax+r15]
	mov	QWORD PTR 40[rsp], rax
	mov	QWORD PTR [rdx], r13
	mov	QWORD PTR 80[rsp], rdx
	mov	QWORD PTR 144[rsp], rax
	mov	QWORD PTR 208[rsp], rax
	cmp	rbx, r12
	je	.L190
	mov	rdx, QWORD PTR 32[rsp]
	mov	r15, rax
	mov	r13, r12
	mov	QWORD PTR 216[rsp], rdx
	.p2align 4
	.p2align 3
.L192:
	mov	ecx, 256
	mov	r14, QWORD PTR 0[r13]
.LEHB11:
	call	_Znay
.LEHE11:
	mov	QWORD PTR [r15], rax
	mov	rdx, rax
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L191:
	mov	ecx, DWORD PTR [r14+rax]
	mov	DWORD PTR [rdx+rax], ecx
	add	rax, 4
	cmp	rax, 256
	jne	.L191
	lea	rax, 8[r15]
	add	r13, 8
	mov	QWORD PTR 144[rsp], rax
	cmp	r13, rbx
	je	.L364
	mov	r15, rax
	jmp	.L192
.L162:
	mov	rdx, rdi
	sub	rdx, rbp
	mov	rcx, rdx
	sar	rcx, 3
	cmp	rcx, r14
	je	.L337
	test	rcx, rcx
	mov	eax, 1
	mov	QWORD PTR 48[rsp], rdx
	cmovne	rax, rcx
	add	rax, rcx
	movabs	rcx, 1152921504606846975
	cmp	rax, rcx
	cmova	rax, rcx
	lea	r15, 0[0+rax*8]
	mov	rcx, r15
.LEHB12:
	call	_Znwy
.LEHE12:
	mov	rdx, QWORD PTR 48[rsp]
	mov	r9, rax
	mov	QWORD PTR [rax+rdx], r13
	cmp	rbp, rbx
	je	.L365
	mov	r8, rbx
	mov	rdx, rbp
	sub	r8, rbp
	add	r8, rax
	.p2align 5
	.p2align 4
	.p2align 3
.L167:
	mov	rcx, QWORD PTR [rdx]
	add	rax, 8
	add	rdx, 8
	mov	QWORD PTR -8[rax], rcx
	cmp	rax, r8
	jne	.L167
	mov	rax, r9
	sub	rax, rbp
	lea	rbx, 8[rbx+rax]
	test	rbp, rbp
	je	.L168
.L166:
	sub	rdi, rbp
	mov	rcx, rbp
	mov	QWORD PTR 48[rsp], r9
	mov	rdx, rdi
	call	_ZdlPvy
	mov	r9, QWORD PTR 48[rsp]
.L168:
	lea	rdi, [r9+r15]
	mov	rbp, r9
	jmp	.L163
.L364:
	lea	r13, 16[r15]
	mov	r15, r12
	.p2align 4
	.p2align 3
.L193:
	mov	rcx, QWORD PTR [r15]
	test	rcx, rcx
	je	.L196
	call	_ZdaPv
.L196:
	add	r15, 8
	cmp	r15, rbx
	jne	.L193
	mov	rbx, r13
	test	r12, r12
	je	.L197
	mov	rdx, rbp
	sub	rdx, r12
.L219:
	mov	rcx, r12
	call	_ZdlPvy
.L197:
	mov	rbp, QWORD PTR 88[rsp]
	mov	r12, QWORD PTR 40[rsp]
	add	rbp, r12
	sub	edi, 1
	jne	.L198
.L362:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	ecx, 256
	mov	QWORD PTR 72[rsp], rax
.LEHB13:
	call	_Znay
.LEHE13:
	mov	r13, rax
	cmp	rbx, rbp
	je	.L199
	mov	QWORD PTR [rbx], rax
	lea	r13, 8[rbx]
.L200:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rbx, r12
	sub	rax, QWORD PTR 72[rsp]
	add	QWORD PTR 48[rsp], rax
	cmp	r13, r12
	je	.L212
	.p2align 4
	.p2align 3
.L209:
	mov	rcx, QWORD PTR [rbx]
	test	rcx, rcx
	je	.L211
	call	_ZdaPv
.L211:
	add	rbx, 8
	cmp	r13, rbx
	jne	.L209
	test	r12, r12
	je	.L210
.L212:
	mov	rdx, rbp
	mov	rcx, r12
	sub	rdx, r12
	call	_ZdlPvy
.L210:
	sub	DWORD PTR 100[rsp], 1
	jne	.L180
	mov	rcx, QWORD PTR 64[rsp]
	lea	rdx, .LC18[rip]
	pxor	xmm6, xmm6
	pxor	xmm7, xmm7
	cvtsi2sd	xmm6, QWORD PTR 56[rsp]
	cvtsi2sd	xmm7, QWORD PTR 48[rsp]
	divsd	xmm6, QWORD PTR .LC16[rip]
	divsd	xmm7, QWORD PTR .LC17[rip]
.LEHB14:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm6
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC19[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC20[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm7
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC21[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	divsd	xmm7, xmm6
	mov	rcx, rax
	movapd	xmm1, xmm7
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC22[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	nop
.LEHE14:
	movaps	xmm6, XMMWORD PTR 240[rsp]
	movaps	xmm7, XMMWORD PTR 256[rsp]
	xor	eax, eax
	add	rsp, 280
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L199:
	movabs	rdi, 1152921504606846975
	mov	r15, rbx
	sub	r15, r12
	mov	rax, r15
	sar	rax, 3
	cmp	rax, rdi
	je	.L340
	test	rax, rax
	mov	edx, 1
	cmovne	rdx, rax
	lea	r14, [rdx+rax]
	movabs	rax, 1152921504606846975
	cmp	r14, rax
	cmova	r14, rax
	lea	rax, 0[0+r14*8]
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], rax
.LEHB15:
	call	_Znwy
.LEHE15:
	add	r15, rax
	mov	rdi, rax
	mov	QWORD PTR [r15], r13
	mov	QWORD PTR 176[rsp], rax
	mov	QWORD PTR 208[rsp], rax
	cmp	rbx, r12
	je	.L202
	mov	rax, QWORD PTR 104[rsp]
	mov	r8, rdi
	mov	r9, r12
	mov	QWORD PTR 216[rsp], rax
.L204:
	mov	ecx, 256
	mov	QWORD PTR 88[rsp], r8
	mov	r13, QWORD PTR [r9]
	mov	QWORD PTR 80[rsp], r9
.LEHB16:
	call	_Znay
.LEHE16:
	mov	r8, QWORD PTR 88[rsp]
	mov	r9, QWORD PTR 80[rsp]
	mov	rcx, rax
	mov	QWORD PTR [r8], rax
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L203:
	mov	edx, DWORD PTR 0[r13+rax]
	mov	DWORD PTR [rcx+rax], edx
	add	rax, 4
	cmp	rax, 256
	jne	.L203
	lea	rax, 8[r8]
	add	r9, 8
	mov	QWORD PTR 176[rsp], rax
	cmp	r9, rbx
	je	.L366
	mov	r8, rax
	jmp	.L204
.L190:
	mov	rax, QWORD PTR 40[rsp]
	xor	edx, edx
	lea	rbx, 8[rax]
	jmp	.L219
.L366:
	lea	r13, 16[r8]
	mov	r14, r12
.L205:
	mov	rcx, QWORD PTR [r14]
	test	rcx, rcx
	je	.L207
	call	_ZdaPv
.L207:
	add	r14, 8
	cmp	r14, rbx
	jne	.L205
	test	r12, r12
	jne	.L367
.L208:
	mov	rbp, QWORD PTR 40[rsp]
	mov	r12, rdi
	add	rbp, rdi
	jmp	.L200
.L365:
	lea	rbx, 8[rax]
	jmp	.L166
.L170:
	mov	rdx, rbx
	sub	rdx, rbp
	mov	rax, rdx
	sar	rax, 3
	cmp	rax, r14
	je	.L338
	test	rax, rax
	mov	r12d, 1
	mov	QWORD PTR 72[rsp], rdx
	cmovne	r12, rax
	add	r12, rax
	movabs	rax, 1152921504606846975
	cmp	r12, rax
	cmova	r12, rax
	sal	r12, 3
	mov	rcx, r12
.LEHB17:
	call	_Znwy
.LEHE17:
	mov	rdx, QWORD PTR 72[rsp]
	mov	r15, rax
	mov	QWORD PTR [rax+rdx], r13
	mov	rax, rbp
	mov	rdx, r15
	cmp	rbx, rbp
	je	.L368
.L173:
	mov	rcx, QWORD PTR [rax]
	add	rax, 8
	add	rdx, 8
	mov	QWORD PTR -8[rdx], rcx
	cmp	rax, rbx
	jne	.L173
	sub	rax, rbp
	lea	rbx, 8[r15+rax]
	test	rbp, rbp
	je	.L175
	sub	rdi, rbp
	mov	rdx, rdi
.L174:
	mov	rcx, rbp
	call	_ZdlPvy
.L175:
	lea	rdi, [r15+r12]
	mov	rbp, r15
	jmp	.L171
.L111:
	mov	rdx, rbx
	and	ebx, 1
	pxor	xmm0, xmm0
	shr	rdx
	or	rdx, rbx
	cvtsi2sd	xmm0, rdx
	addsd	xmm0, xmm0
	jmp	.L112
.L367:
	mov	rdx, rbp
	sub	rdx, r12
.L218:
	mov	rcx, r12
	call	_ZdlPvy
	jmp	.L208
.L368:
	lea	rbx, 8[r15]
	xor	edx, edx
	jmp	.L174
.L357:
	mov	eax, DWORD PTR 0[r13]
	mov	DWORD PTR [rdx], eax
	mov	eax, DWORD PTR -4[r13+rcx]
	mov	DWORD PTR -4[rdx+rcx], eax
	mov	rdx, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 184[rsp]
	jmp	.L134
.L342:
	movzx	eax, WORD PTR -2[r13+rcx]
	mov	WORD PTR -2[rdx+rcx], ax
	mov	rdx, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 184[rsp]
	jmp	.L134
.L202:
	lea	r13, 8[rax]
	xor	edx, edx
	jmp	.L218
.L236:
	jmp	.L206
.L242:
	mov	rsi, rax
	jmp	.L213
.L237:
	mov	rsi, rax
	jmp	.L161
.L329:
	jmp	.L330
.L241:
	mov	rsi, rax
	jmp	.L160
.L234:
	mov	rbx, rax
	jmp	.L158
.L238:
	mov	rsi, rax
	jmp	.L195
.L235:
	jmp	.L194
.L333:
	jmp	.L334
.L331:
	jmp	.L332
.L335:
	jmp	.L334
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA13440:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE13440-.LLSDACSB13440
.LLSDACSB13440:
	.uleb128 .LEHB3-.LFB13440
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB4-.LFB13440
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L234-.LFB13440
	.uleb128 0
	.uleb128 .LEHB5-.LFB13440
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LFB13440
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L241-.LFB13440
	.uleb128 0
	.uleb128 .LEHB7-.LFB13440
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L237-.LFB13440
	.uleb128 0
	.uleb128 .LEHB8-.LFB13440
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L242-.LFB13440
	.uleb128 0
	.uleb128 .LEHB9-.LFB13440
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L238-.LFB13440
	.uleb128 0
	.uleb128 .LEHB10-.LFB13440
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L333-.LFB13440
	.uleb128 0
	.uleb128 .LEHB11-.LFB13440
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L235-.LFB13440
	.uleb128 0
	.uleb128 .LEHB12-.LFB13440
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L329-.LFB13440
	.uleb128 0
	.uleb128 .LEHB13-.LFB13440
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L238-.LFB13440
	.uleb128 0
	.uleb128 .LEHB14-.LFB13440
	.uleb128 .LEHE14-.LEHB14
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB15-.LFB13440
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L335-.LFB13440
	.uleb128 0
	.uleb128 .LEHB16-.LFB13440
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L236-.LFB13440
	.uleb128 0
	.uleb128 .LEHB17-.LFB13440
	.uleb128 .LEHE17-.LEHB17
	.uleb128 .L331-.LFB13440
	.uleb128 0
.LLSDACSE13440:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	344
	.seh_savereg	rbx, 280
	.seh_savereg	rsi, 288
	.seh_savereg	rdi, 296
	.seh_savereg	rbp, 304
	.seh_savexmm	xmm6, 240
	.seh_savexmm	xmm7, 256
	.seh_savereg	r12, 312
	.seh_savereg	r13, 320
	.seh_savereg	r14, 328
	.seh_savereg	r15, 336
	.seh_endprologue
main.cold:
.L206:
	mov	rcx, rsi
	mov	rsi, rax
	call	_ZNSt19_UninitDestroyGuardIP13OwnedThrowingvED1Ev
	lea	rdx, 8[r15]
	mov	rcx, r15
	call	_ZSt8_DestroyIP13OwnedThrowingEvT_S2_
	mov	rdx, r14
	mov	rcx, rdi
	call	_ZNSt6vectorI13OwnedThrowingSaIS0_EE12_Guard_allocD1Ev.isra.0
.L195:
	mov	rdi, r12
.L214:
	cmp	rbx, rdi
	je	.L369
	mov	rcx, QWORD PTR [rdi]
	test	rcx, rcx
	je	.L215
	call	_ZdaPv
.L215:
	add	rdi, 8
	jmp	.L214
.L213:
	xor	ebp, ebp
	xor	ebx, ebx
	xor	r12d, r12d
	jmp	.L195
.L160:
	xor	edi, edi
	xor	ebx, ebx
	xor	ebp, ebp
.L161:
	mov	r12, rbp
.L183:
	cmp	r12, rbx
	je	.L370
	mov	rcx, QWORD PTR [r12]
	test	rcx, rcx
	je	.L184
	call	_ZdaPv
.L184:
	add	r12, 8
	jmp	.L183
.L369:
	test	r12, r12
	je	.L217
	mov	rdx, rbp
	mov	rcx, r12
	sub	rdx, r12
	call	_ZdlPvy
.L217:
	mov	rcx, rsi
.LEHB18:
	call	_Unwind_Resume
.LEHE18:
.L337:
	lea	rcx, .LC15[rip]
.LEHB19:
	call	_ZSt20__throw_length_errorPKc
.LEHE19:
.L232:
.L330:
	mov	rcx, r13
	mov	rsi, rax
	call	_ZdaPv
	jmp	.L161
.L158:
	mov	rax, QWORD PTR 192[rsp]
	mov	rcx, rdi
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	rcx, rbx
.LEHB20:
	call	_Unwind_Resume
.LEHE20:
.L339:
	lea	rcx, .LC15[rip]
.LEHB21:
	call	_ZSt20__throw_length_errorPKc
.LEHE21:
.L239:
.L334:
	mov	rcx, r13
	mov	rsi, rax
	call	_ZdaPv
	jmp	.L195
.L194:
	mov	rcx, rsi
	mov	rsi, rax
	call	_ZNSt19_UninitDestroyGuardIP13OwnedThrowingvED1Ev
	mov	rcx, QWORD PTR 80[rsp]
	lea	rdx, 8[rcx]
	call	_ZSt8_DestroyIP13OwnedThrowingEvT_S2_
	mov	rdx, QWORD PTR 72[rsp]
	mov	rcx, QWORD PTR 40[rsp]
	call	_ZNSt6vectorI13OwnedThrowingSaIS0_EE12_Guard_allocD1Ev.isra.0
	jmp	.L195
.L338:
	lea	rcx, .LC15[rip]
.LEHB22:
	call	_ZSt20__throw_length_errorPKc
.LEHE22:
.L233:
.L332:
	mov	rcx, r13
	mov	rsi, rax
	call	_ZdaPv
	jmp	.L161
.L340:
	lea	rcx, .LC15[rip]
.LEHB23:
	call	_ZSt20__throw_length_errorPKc
.LEHE23:
.L370:
	test	rbp, rbp
	je	.L186
	sub	rdi, rbp
	mov	rcx, rbp
	mov	rdx, rdi
	call	_ZdlPvy
.L186:
	mov	rcx, rsi
.LEHB24:
	call	_Unwind_Resume
.LEHE24:
.L240:
	jmp	.L334
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC13440:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC13440-.LLSDACSBC13440
.LLSDACSBC13440:
	.uleb128 .LEHB18-.LCOLDB24
	.uleb128 .LEHE18-.LEHB18
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB19-.LCOLDB24
	.uleb128 .LEHE19-.LEHB19
	.uleb128 .L232-.LCOLDB24
	.uleb128 0
	.uleb128 .LEHB20-.LCOLDB24
	.uleb128 .LEHE20-.LEHB20
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB21-.LCOLDB24
	.uleb128 .LEHE21-.LEHB21
	.uleb128 .L239-.LCOLDB24
	.uleb128 0
	.uleb128 .LEHB22-.LCOLDB24
	.uleb128 .LEHE22-.LEHB22
	.uleb128 .L233-.LCOLDB24
	.uleb128 0
	.uleb128 .LEHB23-.LCOLDB24
	.uleb128 .LEHE23-.LEHB23
	.uleb128 .L240-.LCOLDB24
	.uleb128 0
	.uleb128 .LEHB24-.LCOLDB24
	.uleb128 .LEHE24-.LEHB24
	.uleb128 0
	.uleb128 0
.LLSDACSEC13440:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE24:
	.section	.text.startup,"x"
.LHOTE24:
	.section .rdata,"dr"
	.align 4
__emutls_t.tl_var:
	.space 4
	.globl	__emutls_v.tl_var
	.data
	.align 32
__emutls_v.tl_var:
	.quad	4
	.quad	4
	.quad	0
	.quad	__emutls_t.tl_var
	.section .rdata,"dr"
	.align 8
.LC1:
	.long	0
	.long	1104006501
	.align 8
.LC4:
	.long	0
	.long	1072693248
	.align 8
.LC12:
	.long	0
	.long	1093816192
	.align 8
.LC13:
	.long	0
	.long	1088973312
	.align 8
.LC16:
	.long	0
	.long	1084178432
	.align 8
.LC17:
	.long	0
	.long	1080623104
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__emutls_get_address;	.scl	2;	.type	32;	.endef
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
