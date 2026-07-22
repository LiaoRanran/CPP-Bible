	.file	"_ch151_opt_O2.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.def	_ZNSt12_Vector_baseIdSaIdEED2Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIdSaIdEED2Ev.isra.0
_ZNSt12_Vector_baseIdSaIdEED2Ev.isra.0:
.LFB8184:
	.seh_endprologue
	test	rcx, rcx
	je	.L1
	sub	rdx, rcx
	jmp	_ZdlPvy
.L1:
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC4:
	.ascii "opt_O2: axpy_ms=%.3f chk=%.1f\12\0"
	.section	.text.unlikely,"x"
.LCOLDB5:
	.section	.text.startup,"x"
.LHOTB5:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5862:
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
	.seh_endprologue
	call	__main
	mov	ecx, 400000000
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r8d, 399999992
	xor	edx, edx
	mov	QWORD PTR [rax], 0x000000000
	lea	rcx, 8[rax]
	mov	rbx, rax
	lea	rbp, 400000000[rax]
	call	memset
	mov	ecx, 400000000
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	QWORD PTR [rax], 0x000000000
	lea	rcx, 8[rax]
	xor	edx, edx
	mov	rdi, rax
	mov	r8d, 399999992
	lea	r12, 400000000[rax]
	call	memset
	mov	ecx, 400000000
.LEHB2:
	call	_Znwy
.LEHE2:
	mov	QWORD PTR [rax], 0x000000000
	lea	rcx, 8[rax]
	xor	edx, edx
	mov	rsi, rax
	mov	r8d, 399999992
	lea	r13, 400000000[rax]
	call	memset
	movsd	xmm1, QWORD PTR .LC0[rip]
	mov	rax, rbx
	movapd	xmm0, xmm1
	.p2align 5
	.p2align 4
	.p2align 3
.L5:
	movsd	QWORD PTR [rax], xmm0
	add	rax, 8
	addsd	xmm0, xmm1
	cmp	rbp, rax
	jne	.L5
	movsd	xmm0, QWORD PTR .LC1[rip]
	mov	rax, rdi
	.p2align 5
	.p2align 4
	.p2align 3
.L6:
	movsd	QWORD PTR [rax], xmm0
	add	rax, 8
	addsd	xmm0, xmm1
	cmp	r12, rax
	jne	.L6
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r14, rax
	xor	eax, eax
	.p2align 6
	.p2align 4
	.p2align 3
.L7:
	movsd	xmm1, QWORD PTR [rbx+rax*8]
	movsd	xmm0, QWORD PTR [rdi+rax*8]
	mulsd	xmm0, xmm1
	addsd	xmm0, xmm1
	movsd	QWORD PTR [rsi+rax*8], xmm0
	add	rax, 1
	cmp	rax, 50000000
	jne	.L7
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm1, xmm1
	movsd	xmm0, QWORD PTR 399999992[rsi]
	lea	rcx, .LC4[rip]
	sub	rax, r14
	movsd	QWORD PTR 40[rsp], xmm0
	mov	r8, QWORD PTR 40[rsp]
	cvtsi2sd	xmm1, rax
	divsd	xmm1, QWORD PTR .LC3[rip]
	movq	rdx, xmm1
	movq	xmm2, r8
.LEHB3:
	call	__mingw_printf
.LEHE3:
	mov	rdx, r13
	mov	rcx, rsi
	call	_ZNSt12_Vector_baseIdSaIdEED2Ev.isra.0
	mov	rdx, r12
	mov	rcx, rdi
	call	_ZNSt12_Vector_baseIdSaIdEED2Ev.isra.0
	mov	rdx, rbp
	mov	rcx, rbx
	call	_ZNSt12_Vector_baseIdSaIdEED2Ev.isra.0
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
.L11:
	mov	rsi, rax
	jmp	.L10
.L13:
	jmp	.L8
.L12:
	mov	rsi, rax
	jmp	.L9
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5862:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5862-.LLSDACSB5862
.LLSDACSB5862:
	.uleb128 .LEHB0-.LFB5862
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5862
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L11-.LFB5862
	.uleb128 0
	.uleb128 .LEHB2-.LFB5862
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L12-.LFB5862
	.uleb128 0
	.uleb128 .LEHB3-.LFB5862
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L13-.LFB5862
	.uleb128 0
.LLSDACSE5862:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_savereg	rbp, 72
	.seh_savereg	r12, 80
	.seh_savereg	r13, 88
	.seh_savereg	r14, 96
	.seh_endprologue
main.cold:
.L8:
	mov	rcx, rsi
	mov	rdx, r13
	mov	rsi, rax
	call	_ZNSt12_Vector_baseIdSaIdEED2Ev.isra.0
.L9:
	mov	rdx, r12
	mov	rcx, rdi
	call	_ZNSt12_Vector_baseIdSaIdEED2Ev.isra.0
.L10:
	mov	rcx, rbx
	mov	rdx, rbp
	call	_ZNSt12_Vector_baseIdSaIdEED2Ev.isra.0
	mov	rcx, rsi
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5862:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5862-.LLSDACSBC5862
.LLSDACSBC5862:
	.uleb128 .LEHB4-.LCOLDB5
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSEC5862:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE5:
	.section	.text.startup,"x"
.LHOTE5:
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1072693248
	.align 8
.LC1:
	.long	0
	.long	1073741824
	.align 8
.LC3:
	.long	0
	.long	1093567616
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
