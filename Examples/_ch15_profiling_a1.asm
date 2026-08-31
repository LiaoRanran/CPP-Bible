	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10scalar_sumPKll
	.def	_Z10scalar_sumPKll;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10scalar_sumPKll
_Z10scalar_sumPKll:
.LFB0:
	.seh_endprologue
	test	edx, edx
	jle	.L4
	movsx	rdx, edx
	xor	eax, eax
	lea	rdx, [rcx+rdx*4]
	.p2align 4,,10
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
.LFB1:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	cmp	edx, 3
	mov	r10, rcx
	jle	.L12
	lea	r9d, -4[rdx]
	xor	eax, eax
	pxor	xmm0, xmm0
	shr	r9d, 2
	add	r9d, 1
	.p2align 4,,10
	.p2align 3
.L9:
	mov	rcx, rax
	add	rax, 1
	sal	rcx, 4
	cmp	eax, r9d
	movdqu	xmm1, XMMWORD PTR [r10+rcx]
	paddd	xmm0, xmm1
	jb	.L9
	pshufd	xmm1, xmm0, 85
	movd	ebx, xmm1
	movdqa	xmm1, xmm0
	movd	r8d, xmm0
	punpckhdq	xmm1, xmm0
	sal	r9d, 2
	pshufd	xmm0, xmm0, 255
	movd	r11d, xmm1
	movd	ecx, xmm0
.L8:
	cmp	edx, r9d
	jle	.L10
	movsx	rsi, r9d
	sub	edx, r9d
	lea	rax, [r10+rsi*4]
	add	rdx, rsi
	lea	rdx, [r10+rdx*4]
	.p2align 4,,10
	.p2align 3
.L11:
	add	r8d, DWORD PTR [rax]
	add	rax, 4
	cmp	rdx, rax
	jne	.L11
.L10:
	lea	eax, [r8+rbx]
	add	eax, r11d
	add	eax, ecx
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L12:
	xor	r9d, r9d
	xor	ecx, ecx
	xor	r11d, r11d
	xor	ebx, ebx
	xor	r8d, r8d
	jmp	.L8
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
