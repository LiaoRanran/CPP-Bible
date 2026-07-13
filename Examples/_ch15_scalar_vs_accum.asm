	.file	"_ch15_scalar_vs_accum.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZL6printfPKcz;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL6printfPKcz
_ZL6printfPKcz:
.LFB2332:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rsi, 88[rsp]
	mov	rbx, rcx
	mov	QWORD PTR 88[rsp], rdx
	mov	ecx, 1
	mov	QWORD PTR 96[rsp], r8
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 40[rsp], rsi
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	mov	r8, rsi
	mov	rdx, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10scalar_sumPKll
	.def	_Z10scalar_sumPKll;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10scalar_sumPKll
_Z10scalar_sumPKll:
.LFB5605:
	.seh_endprologue
	test	edx, edx
	jle	.L6
	movsx	rdx, edx
	xor	eax, eax
	lea	rdx, [rcx+rdx*4]
	.p2align 4,,10
	.p2align 3
.L5:
	add	eax, DWORD PTR [rcx]
	add	rcx, 4
	cmp	rcx, rdx
	jne	.L5
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12four_acc_sumPKll
	.def	_Z12four_acc_sumPKll;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12four_acc_sumPKll
_Z12four_acc_sumPKll:
.LFB5606:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	cmp	edx, 3
	mov	r10, rcx
	jle	.L13
	lea	r9d, -4[rdx]
	xor	eax, eax
	pxor	xmm0, xmm0
	shr	r9d, 2
	add	r9d, 1
	.p2align 4,,10
	.p2align 3
.L10:
	mov	rcx, rax
	add	rax, 1
	sal	rcx, 4
	cmp	eax, r9d
	movdqu	xmm1, XMMWORD PTR [r10+rcx]
	paddd	xmm0, xmm1
	jb	.L10
	pshufd	xmm1, xmm0, 85
	movd	ebx, xmm1
	movdqa	xmm1, xmm0
	movd	r8d, xmm0
	punpckhdq	xmm1, xmm0
	sal	r9d, 2
	pshufd	xmm0, xmm0, 255
	movd	r11d, xmm1
	movd	ecx, xmm0
.L9:
	cmp	edx, r9d
	jle	.L11
	movsx	rsi, r9d
	sub	edx, r9d
	lea	rax, [r10+rsi*4]
	add	rdx, rsi
	lea	rdx, [r10+rdx*4]
	.p2align 4,,10
	.p2align 3
.L12:
	add	r8d, DWORD PTR [rax]
	add	rax, 4
	cmp	rdx, rax
	jne	.L12
.L11:
	lea	eax, [r8+rbx]
	add	eax, r11d
	add	eax, ecx
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L13:
	xor	r9d, r9d
	xor	ecx, ecx
	xor	r11d, r11d
	xor	ebx, ebx
	xor	r8d, r8d
	jmp	.L9
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC4:
	.ascii "scalar_sum  : %8.2f ms  (result=%ld)\12\0"
	.align 8
.LC5:
	.ascii "four_acc_sum: %8.2f ms  (result=%ld)\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5607:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 120
	.seh_stackalloc	120
	movaps	XMMWORD PTR 48[rsp], xmm6
	.seh_savexmm	xmm6, 48
	movaps	XMMWORD PTR 64[rsp], xmm7
	.seh_savexmm	xmm7, 64
	movaps	XMMWORD PTR 80[rsp], xmm8
	.seh_savexmm	xmm8, 80
	movaps	XMMWORD PTR 96[rsp], xmm9
	.seh_savexmm	xmm9, 96
	.seh_endprologue
	call	__main
	mov	ecx, 200000000
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r8d, 199999996
	xor	edx, edx
	mov	DWORD PTR [rax], 0
	lea	rcx, 4[rax]
	mov	rdi, rax
	call	memset
	pxor	xmm5, xmm5
	mov	rsi, rdi
	movdqa	xmm3, XMMWORD PTR .LC2[rip]
	movdqa	xmm6, xmm5
	movdqa	xmm4, XMMWORD PTR .LC0[rip]
	mov	rax, rdi
	pcmpgtd	xmm6, xmm3
	movdqa	xmm7, XMMWORD PTR .LC1[rip]
	lea	rbx, 200000000[rdi]
	.p2align 4,,10
	.p2align 3
.L17:
	movdqa	xmm1, xmm4
	movdqa	xmm2, xmm5
	movdqa	xmm8, xmm6
	pcmpgtd	xmm2, xmm1
	movdqa	xmm0, xmm1
	movdqa	xmm9, xmm6
	pmuludq	xmm8, xmm1
	add	rax, 16
	paddd	xmm4, xmm7
	pmuludq	xmm0, xmm3
	pmuludq	xmm2, xmm3
	paddq	xmm2, xmm8
	movdqa	xmm8, xmm5
	psllq	xmm2, 32
	paddq	xmm0, xmm2
	movdqa	xmm2, xmm1
	psrlq	xmm2, 32
	pcmpgtd	xmm8, xmm2
	pmuludq	xmm9, xmm2
	pmuludq	xmm2, xmm3
	pmuludq	xmm8, xmm3
	paddq	xmm8, xmm9
	psllq	xmm8, 32
	paddq	xmm2, xmm8
	shufps	xmm0, xmm2, 221
	pshufd	xmm0, xmm0, 216
	psrad	xmm0, 3
	movdqa	xmm2, xmm0
	pslld	xmm2, 1
	paddd	xmm2, xmm0
	pslld	xmm2, 5
	paddd	xmm0, xmm2
	psubd	xmm1, xmm0
	movups	XMMWORD PTR -16[rax], xmm1
	cmp	rax, rbx
	jne	.L17
	mov	DWORD PTR 44[rsp], 0
	mov	eax, DWORD PTR 44[rsp]
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm0, xmm0
	mov	rbp, rax
	.p2align 4,,10
	.p2align 3
.L18:
	movdqu	xmm7, XMMWORD PTR [rsi]
	add	rsi, 16
	cmp	rsi, rbx
	paddd	xmm0, xmm7
	jne	.L18
	movdqa	xmm1, xmm0
	movdqa	xmm6, xmm0
	pxor	xmm7, xmm7
	psrldq	xmm1, 8
	paddd	xmm6, xmm1
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	edx, 50000000
	mov	rcx, rdi
	mov	rbx, rax
	call	_Z12four_acc_sumPKll
	mov	esi, eax
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm1, xmm1
	movdqa	xmm0, xmm6
	movsd	xmm2, QWORD PTR .LC3[rip]
	psrldq	xmm0, 4
	lea	rcx, .LC4[rip]
	sub	rax, rbx
	sub	rbx, rbp
	paddd	xmm0, xmm6
	cvtsi2sd	xmm1, rbx
	movd	r8d, xmm0
	cvtsi2sd	xmm7, rax
	divsd	xmm1, xmm2
	divsd	xmm7, xmm2
	movq	rdx, xmm1
.LEHB1:
	call	_ZL6printfPKcz
	mov	r8d, esi
	movapd	xmm1, xmm7
	movq	rdx, xmm7
	lea	rcx, .LC5[rip]
	call	_ZL6printfPKcz
.LEHE1:
	mov	edx, 200000000
	mov	rcx, rdi
	call	_ZdlPvy
	nop
	movaps	xmm6, XMMWORD PTR 48[rsp]
	xor	eax, eax
	movaps	xmm7, XMMWORD PTR 64[rsp]
	movaps	xmm8, XMMWORD PTR 80[rsp]
	movaps	xmm9, XMMWORD PTR 96[rsp]
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L20:
	mov	rbx, rax
	mov	rcx, rdi
	mov	edx, 200000000
	call	_ZdlPvy
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5607:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5607-.LLSDACSB5607
.LLSDACSB5607:
	.uleb128 .LEHB0-.LFB5607
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5607
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L20-.LFB5607
	.uleb128 0
	.uleb128 .LEHB2-.LFB5607
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE5607:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	0
	.long	1
	.long	2
	.long	3
	.align 16
.LC1:
	.long	4
	.long	4
	.long	4
	.long	4
	.align 16
.LC2:
	.long	354224107
	.long	354224107
	.long	354224107
	.long	354224107
	.align 8
.LC3:
	.long	0
	.long	1093567616
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
