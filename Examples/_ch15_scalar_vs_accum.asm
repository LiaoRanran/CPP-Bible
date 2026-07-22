	.file	"_ch15_scalar_vs_accum.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10scalar_sumPKll
	.def	_Z10scalar_sumPKll;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10scalar_sumPKll
_Z10scalar_sumPKll:
.LFB5860:
	.seh_endprologue
	test	edx, edx
	jle	.L4
	movsxd	rdx, edx
	xor	eax, eax
	lea	rdx, [rcx+rdx*4]
	.p2align 4
	.p2align 4
	.p2align 3
.L3:
	add	eax, DWORD PTR [rcx]
	add	rcx, 4
	cmp	rcx, rdx
	jne	.L3
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12four_acc_sumPKll
	.def	_Z12four_acc_sumPKll;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12four_acc_sumPKll
_Z12four_acc_sumPKll:
.LFB5861:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	cmp	edx, 3
	jle	.L12
	mov	r10d, edx
	xor	eax, eax
	pxor	xmm0, xmm0
	shr	r10d, 2
	.p2align 5
	.p2align 4
	.p2align 3
.L9:
	mov	r8, rax
	add	rax, 1
	sal	r8, 4
	movdqu	xmm1, XMMWORD PTR [rcx+r8]
	paddd	xmm0, xmm1
	cmp	eax, r10d
	jb	.L9
	pshufd	xmm1, xmm0, 85
	lea	eax, -4[rdx]
	movd	r10d, xmm0
	movd	ebx, xmm1
	movdqa	xmm1, xmm0
	and	eax, -4
	punpckhdq	xmm1, xmm0
	pshufd	xmm0, xmm0, 255
	add	eax, 4
	movd	r11d, xmm1
	movd	r8d, xmm0
.L8:
	cmp	edx, eax
	jle	.L10
	cdqe
.L11:
	add	r10d, DWORD PTR [rcx+rax*4]
	add	rax, 1
	cmp	edx, eax
	jg	.L11
.L10:
	lea	eax, [r10+rbx]
	add	eax, r11d
	add	eax, r8d
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L12:
	xor	eax, eax
	xor	r8d, r8d
	xor	r11d, r11d
	xor	ebx, ebx
	xor	r10d, r10d
	jmp	.L8
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC4:
	.ascii "scalar_sum  : %8.2f ms  (result=%ld)\12\0"
	.align 8
.LC5:
	.ascii "four_acc_sum: %8.2f ms  (result=%ld)\12\0"
	.section	.text.unlikely,"x"
.LCOLDB6:
	.section	.text.startup,"x"
.LHOTB6:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5862:
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
	movaps	XMMWORD PTR 48[rsp], xmm6
	.seh_savexmm	xmm6, 48
	movaps	XMMWORD PTR 64[rsp], xmm7
	.seh_savexmm	xmm7, 64
	.seh_endprologue
	call	__main
	mov	ecx, 200000000
.LEHB0:
	call	_Znwy
.LEHE0:
	xor	edx, edx
	mov	r8d, 199999996
	mov	DWORD PTR [rax], 0
	lea	rcx, 4[rax]
	mov	rdi, rax
	mov	rsi, rdi
	lea	rbx, 200000000[rdi]
	call	memset
	mov	edx, 354224107
	movdqa	xmm2, XMMWORD PTR .LC0[rip]
	mov	rax, rdi
	movd	xmm3, edx
	mov	edx, 4
	pshufd	xmm3, xmm3, 0
	movdqa	xmm4, xmm3
	movd	xmm5, edx
	psrad	xmm4, 31
	pshufd	xmm5, xmm5, 0
	.p2align 4
	.p2align 3
.L16:
	movdqa	xmm1, xmm2
	movdqa	xmm6, xmm4
	movdqa	xmm0, xmm2
	add	rax, 16
	psrad	xmm1, 31
	pmuludq	xmm6, xmm2
	movdqa	xmm7, xmm4
	pmuludq	xmm1, xmm3
	pmuludq	xmm0, xmm3
	paddq	xmm1, xmm6
	psllq	xmm1, 32
	paddq	xmm0, xmm1
	movdqa	xmm1, xmm2
	psrlq	xmm1, 32
	movdqa	xmm6, xmm1
	pmuludq	xmm7, xmm1
	psrad	xmm6, 31
	pmuludq	xmm1, xmm3
	pmuludq	xmm6, xmm3
	paddq	xmm6, xmm7
	psllq	xmm6, 32
	paddq	xmm1, xmm6
	shufps	xmm0, xmm1, 221
	pshufd	xmm0, xmm0, 216
	psrad	xmm0, 3
	movdqa	xmm1, xmm0
	pslld	xmm1, 1
	paddd	xmm1, xmm0
	pslld	xmm1, 5
	paddd	xmm0, xmm1
	movdqa	xmm1, xmm2
	paddd	xmm2, xmm5
	psubd	xmm1, xmm0
	movups	XMMWORD PTR -16[rax], xmm1
	cmp	rax, rbx
	jne	.L16
	mov	DWORD PTR 44[rsp], 0
	mov	eax, DWORD PTR 44[rsp]
	pxor	xmm6, xmm6
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rbp, rax
	.p2align 5
	.p2align 4
	.p2align 3
.L17:
	movdqu	xmm5, XMMWORD PTR [rsi]
	add	rsi, 16
	paddd	xmm6, xmm5
	cmp	rsi, rbx
	jne	.L17
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	edx, 50000000
	mov	rcx, rdi
	pxor	xmm7, xmm7
	mov	rbx, rax
	call	_Z12four_acc_sumPKll
	mov	esi, eax
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movdqa	xmm1, xmm6
	movsd	xmm0, QWORD PTR .LC3[rip]
	lea	rcx, .LC4[rip]
	psrldq	xmm1, 8
	sub	rax, rbx
	sub	rbx, rbp
	paddd	xmm6, xmm1
	cvtsi2sd	xmm7, rax
	divsd	xmm7, xmm0
	movdqa	xmm1, xmm6
	psrldq	xmm1, 4
	paddd	xmm6, xmm1
	pxor	xmm1, xmm1
	cvtsi2sd	xmm1, rbx
	movd	r8d, xmm6
	divsd	xmm1, xmm0
	movq	rdx, xmm1
.LEHB1:
	call	__mingw_printf
	mov	r8d, esi
	movapd	xmm1, xmm7
	movq	rdx, xmm7
	lea	rcx, .LC5[rip]
	call	__mingw_printf
.LEHE1:
	mov	edx, 200000000
	mov	rcx, rdi
	call	_ZdlPvy
	nop
	movaps	xmm6, XMMWORD PTR 48[rsp]
	movaps	xmm7, XMMWORD PTR 64[rsp]
	xor	eax, eax
	add	rsp, 88
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L19:
	mov	rbx, rax
	jmp	.L18
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
	.uleb128 .L19-.LFB5862
	.uleb128 0
.LLSDACSE5862:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	120
	.seh_savereg	rbx, 88
	.seh_savereg	rsi, 96
	.seh_savereg	rdi, 104
	.seh_savereg	rbp, 112
	.seh_savexmm	xmm6, 48
	.seh_savexmm	xmm7, 64
	.seh_endprologue
main.cold:
.L18:
	mov	rcx, rdi
	mov	edx, 200000000
	call	_ZdlPvy
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5862:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5862-.LLSDACSBC5862
.LLSDACSBC5862:
	.uleb128 .LEHB2-.LCOLDB6
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC5862:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE6:
	.section	.text.startup,"x"
.LHOTE6:
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	0
	.long	1
	.long	2
	.long	3
	.align 8
.LC3:
	.long	0
	.long	1093567616
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
