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
	movsx	r8, r8d
	xor	eax, eax
	sal	r8, 2
	.p2align 4,,10
	.p2align 3
.L3:
	movss	xmm0, DWORD PTR [rdx+rax]
	mulss	xmm0, xmm3
	movss	DWORD PTR [rcx+rax], xmm0
	add	rax, 4
	cmp	r8, rax
	jne	.L3
.L1:
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
