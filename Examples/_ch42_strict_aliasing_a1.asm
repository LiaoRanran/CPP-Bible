	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z1fPiPfi
	.def	_Z1fPiPfi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1fPiPfi
_Z1fPiPfi:
.LFB0:
	.seh_endprologue
	test	r8d, r8d
	jle	.L1
	xor	eax, eax
	test	r8b, 1
	mov	r9d, DWORD PTR [rcx]
	movss	xmm0, DWORD PTR [rdx]
	movss	xmm1, DWORD PTR .LC0[rip]
	je	.L3
	cmp	r8d, 1
	addss	xmm0, xmm1
	mov	eax, 1
	je	.L10
	.p2align 4,,10
	.p2align 3
.L3:
	addss	xmm0, xmm1
	add	eax, 2
	cmp	r8d, eax
	addss	xmm0, xmm1
	jne	.L3
.L10:
	add	r8d, r9d
	mov	DWORD PTR [rcx], r8d
	movss	DWORD PTR [rdx], xmm0
.L1:
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 4
.LC0:
	.long	1065353216
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
