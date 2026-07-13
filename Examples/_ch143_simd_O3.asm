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
	cmp	r8d, 1
	je	.L3
	lea	r9, 4[rdx]
	mov	rax, rcx
	sub	rax, r9
	cmp	rax, 8
	ja	.L24
.L3:
	movsx	r8, r8d
	xor	eax, eax
	sal	r8, 2
	.p2align 4,,10
	.p2align 3
.L9:
	movss	xmm0, DWORD PTR [rdx+rax]
	mulss	xmm0, xmm3
	movss	DWORD PTR [rcx+rax], xmm0
	add	rax, 4
	cmp	r8, rax
	jne	.L9
.L1:
	ret
	.p2align 4,,10
	.p2align 3
.L24:
	lea	eax, -1[r8]
	mov	r10d, r8d
	cmp	eax, 2
	jbe	.L11
	mov	r9d, r8d
	movaps	xmm1, xmm3
	xor	eax, eax
	shr	r9d, 2
	shufps	xmm1, xmm1, 0
	sal	r9, 4
	.p2align 4,,10
	.p2align 3
.L5:
	movq	xmm0, QWORD PTR [rdx+rax]
	movhps	xmm0, QWORD PTR 8[rdx+rax]
	mulps	xmm0, xmm1
	movlps	QWORD PTR [rcx+rax], xmm0
	movhps	QWORD PTR 8[rcx+rax], xmm0
	add	rax, 16
	cmp	r9, rax
	jne	.L5
	mov	eax, r8d
	and	eax, -4
	cmp	r8d, eax
	mov	r9d, eax
	je	.L1
	mov	r10d, r8d
	sub	r10d, eax
	cmp	r10d, 1
	je	.L7
.L4:
	movsldup	xmm1, xmm3
	mov	r8d, r9d
	test	r10b, 1
	movq	xmm0, QWORD PTR [rdx+r8*4]
	mulps	xmm0, xmm1
	movlps	QWORD PTR [rcx+r8*4], xmm0
	je	.L1
	and	r10d, -2
	add	eax, r10d
.L7:
	cdqe
	mulss	xmm3, DWORD PTR [rdx+rax*4]
	movss	DWORD PTR [rcx+rax*4], xmm3
	ret
.L11:
	xor	r9d, r9d
	xor	eax, eax
	jmp	.L4
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
