	.file	"_ch143_simd.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z5scalePfPKfif
	.def	_Z5scalePfPKfif;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5scalePfPKfif
_Z5scalePfPKfif:
.LFB0:
	.seh_endprologue
	test	r8d, r8d
	jle	.L1
	lea	eax, -1[r8]
	cmp	eax, 2
	jbe	.L8
	mov	r9d, r8d
	movaps	xmm1, xmm3
	xor	eax, eax
	shr	r9d, 2
	shufps	xmm1, xmm1, 0
	sal	r9, 4
	.p2align 4,,10
	.p2align 3
.L4:
	movq	xmm0, QWORD PTR [rdx+rax]
	movhps	xmm0, QWORD PTR 8[rdx+rax]
	mulps	xmm0, xmm1
	movlps	QWORD PTR [rcx+rax], xmm0
	movhps	QWORD PTR 8[rcx+rax], xmm0
	add	rax, 16
	cmp	r9, rax
	jne	.L4
	mov	eax, r8d
	and	eax, -4
	cmp	r8d, eax
	mov	r9d, eax
	je	.L1
.L3:
	sub	r8d, r9d
	cmp	r8d, 1
	je	.L6
	movsldup	xmm1, xmm3
	movq	xmm0, QWORD PTR [rdx+r9*4]
	test	r8b, 1
	mulps	xmm0, xmm1
	movlps	QWORD PTR [rcx+r9*4], xmm0
	je	.L1
	and	r8d, -2
	add	eax, r8d
.L6:
	cdqe
	mulss	xmm3, DWORD PTR [rdx+rax*4]
	movss	DWORD PTR [rcx+rax*4], xmm3
.L1:
	ret
.L8:
	xor	r9d, r9d
	xor	eax, eax
	jmp	.L3
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
