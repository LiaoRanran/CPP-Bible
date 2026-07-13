	.file	"_ch143_soa_loop.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8step_soa3SoAif
	.def	_Z8step_soa3SoAif;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8step_soa3SoAif
_Z8step_soa3SoAif:
.LFB0:
	.seh_endprologue
	mov	r8, QWORD PTR [rcx]
	mov	r9, QWORD PTR 8[rcx]
	test	edx, edx
	jle	.L4
	mov	r10, QWORD PTR 16[rcx]
	movsx	rdx, edx
	xor	eax, eax
	pxor	xmm1, xmm1
	mov	rcx, QWORD PTR 24[rcx]
	sal	rdx, 2
	.p2align 4,,10
	.p2align 3
.L3:
	movss	xmm0, DWORD PTR [r10+rax]
	mulss	xmm0, xmm2
	addss	xmm0, DWORD PTR [r8+rax]
	movss	DWORD PTR [r8+rax], xmm0
	movss	xmm0, DWORD PTR [rcx+rax]
	mulss	xmm0, xmm2
	addss	xmm0, DWORD PTR [r9+rax]
	movss	DWORD PTR [r9+rax], xmm0
	addss	xmm1, DWORD PTR [r8+rax]
	add	rax, 4
	cmp	rdx, rax
	jne	.L3
	movaps	xmm0, xmm1
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	pxor	xmm1, xmm1
	movaps	xmm0, xmm1
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
