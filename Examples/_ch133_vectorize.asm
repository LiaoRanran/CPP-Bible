	.file	"_ch133_vectorize.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10column_addPKfS0_Pfy
	.def	_Z10column_addPKfS0_Pfy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10column_addPKfS0_Pfy
_Z10column_addPKfS0_Pfy:
.LFB17:
	.seh_endprologue
	test	r9, r9
	je	.L1
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L3:
	movss	xmm0, DWORD PTR [rcx+rax*4]
	addss	xmm0, DWORD PTR [rdx+rax*4]
	movss	DWORD PTR [r8+rax*4], xmm0
	add	rax, 1
	cmp	r9, rax
	jne	.L3
.L1:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10column_dotPKfS0_y
	.def	_Z10column_dotPKfS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10column_dotPKfS0_y
_Z10column_dotPKfS0_y:
.LFB18:
	.seh_endprologue
	test	r8, r8
	je	.L16
	lea	rax, -1[r8]
	cmp	rax, 2
	jbe	.L17
	mov	r9, r8
	xor	eax, eax
	pxor	xmm0, xmm0
	shr	r9, 2
	sal	r9, 4
	.p2align 6
	.p2align 4
	.p2align 3
.L12:
	movups	xmm1, XMMWORD PTR [rcx+rax]
	movups	xmm3, XMMWORD PTR [rdx+rax]
	add	rax, 16
	mulps	xmm1, xmm3
	addss	xmm0, xmm1
	movaps	xmm2, xmm1
	shufps	xmm2, xmm1, 85
	addss	xmm0, xmm2
	movaps	xmm2, xmm1
	unpckhps	xmm2, xmm1
	shufps	xmm1, xmm1, 255
	addss	xmm0, xmm2
	addss	xmm0, xmm1
	cmp	rax, r9
	jne	.L12
	test	r8b, 3
	je	.L9
	mov	rax, r8
	and	rax, -4
.L15:
	movss	xmm1, DWORD PTR [rdx+rax*4]
	mulss	xmm1, DWORD PTR [rcx+rax*4]
	add	rax, 1
	addss	xmm0, xmm1
	cmp	rax, r8
	jb	.L15
.L9:
	ret
	.p2align 4,,10
	.p2align 3
.L16:
	pxor	xmm0, xmm0
	ret
.L17:
	xor	eax, eax
	pxor	xmm0, xmm0
	jmp	.L15
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB19:
	sub	rsp, 56
	.seh_stackalloc	56
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	call	__main
	mov	r9d, 2
	xor	eax, eax
	mov	r10d, 1024
	mov	r11d, 4
	movq	xmm6, r9
	movq	xmm3, r10
	movdqa	xmm1, XMMWORD PTR .LC1[rip]
	movq	xmm5, r11
	lea	rdx, _ZZ4mainE1A[rip]
	lea	rcx, _ZZ4mainE1B[rip]
	punpcklqdq	xmm6, xmm6
	punpcklqdq	xmm3, xmm3
	punpcklqdq	xmm5, xmm5
	.p2align 4
	.p2align 3
.L24:
	movdqa	xmm2, xmm1
	movdqa	xmm0, xmm1
	movdqa	xmm4, xmm3
	paddq	xmm2, xmm6
	shufps	xmm0, xmm2, 136
	cvtdq2ps	xmm0, xmm0
	movaps	XMMWORD PTR [rdx+rax], xmm0
	movdqa	xmm0, xmm3
	psubq	xmm0, xmm1
	psubq	xmm4, xmm2
	shufps	xmm0, xmm4, 136
	cvtdq2ps	xmm0, xmm0
	movaps	XMMWORD PTR [rcx+rax], xmm0
	add	rax, 16
	paddq	xmm1, xmm5
	cmp	rax, 4096
	jne	.L24
	xor	eax, eax
	lea	r8, _ZZ4mainE1C[rip]
	.p2align 5
	.p2align 4
	.p2align 3
.L25:
	movaps	xmm0, XMMWORD PTR [rdx+rax]
	addps	xmm0, XMMWORD PTR [rcx+rax]
	movaps	XMMWORD PTR [r8+rax], xmm0
	add	rax, 16
	cmp	rax, 4096
	jne	.L25
	xor	eax, eax
	pxor	xmm1, xmm1
	.p2align 6
	.p2align 4
	.p2align 3
.L26:
	movaps	xmm0, XMMWORD PTR [rcx+rax]
	mulps	xmm0, XMMWORD PTR [rdx+rax]
	add	rax, 16
	addss	xmm1, xmm0
	movaps	xmm2, xmm0
	shufps	xmm2, xmm0, 85
	addss	xmm2, xmm1
	movaps	xmm1, xmm0
	unpckhps	xmm1, xmm0
	shufps	xmm0, xmm0, 255
	addss	xmm1, xmm2
	addss	xmm1, xmm0
	cmp	rax, 4096
	jne	.L26
	cvttss2si	eax, xmm1
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 56
	ret
	.seh_endproc
.lcomm _ZZ4mainE1C,4096,32
.lcomm _ZZ4mainE1B,4096,32
.lcomm _ZZ4mainE1A,4096,32
	.section .rdata,"dr"
	.align 16
.LC1:
	.quad	0
	.quad	1
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
