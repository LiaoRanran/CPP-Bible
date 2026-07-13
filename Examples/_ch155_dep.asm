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
	jle	.L5
	vmovss	xmm0, DWORD PTR [rcx]
	lea	rax, 4[rcx]
	sub	edx, 2
	lea	rdx, 8[rcx+rdx*4]
	.p2align 4,,10
	.p2align 3
.L3:
	vaddss	xmm0, xmm0, DWORD PTR [rax]
	add	rax, 4
	vmovss	DWORD PTR -4[rax], xmm0
	cmp	rax, rdx
	jne	.L3
.L5:
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
