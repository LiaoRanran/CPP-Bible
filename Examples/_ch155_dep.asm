	.file	"_ch155_dep.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z13add_dependentPfi
	.def	_Z13add_dependentPfi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13add_dependentPfi
_Z13add_dependentPfi:
.LFB0:
	.seh_endprologue
	cmp	edx, 1
	jle	.L1
	sub	edx, 2
	movss	xmm0, DWORD PTR [rcx]
	lea	rax, 4[rcx]
	lea	rdx, 8[rcx+rdx*4]
	.p2align 5
	.p2align 4
	.p2align 3
.L3:
	addss	xmm0, DWORD PTR [rax]
	add	rax, 4
	movss	DWORD PTR -4[rax], xmm0
	cmp	rax, rdx
	jne	.L3
.L1:
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
