	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z14square_inplaceRSt6vectorIiSaIiEE
	.def	_Z14square_inplaceRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14square_inplaceRSt6vectorIiSaIiEE
_Z14square_inplaceRSt6vectorIiSaIiEE:
.LFB2389:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR [rcx]
	cmp	rax, r8
	je	.L1
	.p2align 4,,10
	.p2align 3
.L3:
	mov	edx, DWORD PTR [rax]
	add	rax, 4
	imul	edx, edx
	mov	DWORD PTR -4[rax], edx
	cmp	rax, r8
	jne	.L3
.L1:
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
