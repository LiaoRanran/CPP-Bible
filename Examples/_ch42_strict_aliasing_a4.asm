	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z14sum_norestrictPdPKdi
	.def	_Z14sum_norestrictPdPKdi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14sum_norestrictPdPKdi
_Z14sum_norestrictPdPKdi:
.LFB0:
	.seh_endprologue
	test	r8d, r8d
	jle	.L1
	movsx	r8, r8d
	xor	eax, eax
	sal	r8, 3
	.p2align 4,,10
	.p2align 3
.L3:
	movsd	xmm0, QWORD PTR [rcx+rax]
	addsd	xmm0, QWORD PTR [rdx+rax]
	movsd	QWORD PTR [rcx+rax], xmm0
	add	rax, 8
	cmp	r8, rax
	jne	.L3
.L1:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12sum_restrictPdPKdi
	.def	_Z12sum_restrictPdPKdi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12sum_restrictPdPKdi
_Z12sum_restrictPdPKdi:
.LFB1:
	.seh_endprologue
	test	r8d, r8d
	jle	.L6
	movsx	r8, r8d
	xor	eax, eax
	sal	r8, 3
	.p2align 4,,10
	.p2align 3
.L8:
	movsd	xmm0, QWORD PTR [rcx+rax]
	addsd	xmm0, QWORD PTR [rdx+rax]
	movsd	QWORD PTR [rcx+rax], xmm0
	add	rax, 8
	cmp	r8, rax
	jne	.L8
.L6:
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
