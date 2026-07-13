	.file	"_ch95_parallel.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12par_for_eachRSt6vectorIdSaIdEE
	.def	_Z12par_for_eachRSt6vectorIdSaIdEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12par_for_eachRSt6vectorIdSaIdEE
_Z12par_for_eachRSt6vectorIdSaIdEE:
.LFB6343:
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR [rcx]
	cmp	rax, rdx
	je	.L1
	movsd	xmm1, QWORD PTR .LC0[rip]
	.p2align 4,,10
	.p2align 3
.L3:
	movsd	xmm0, QWORD PTR [rax]
	add	rax, 8
	mulsd	xmm0, xmm0
	addsd	xmm0, xmm1
	movsd	QWORD PTR -8[rax], xmm0
	cmp	rdx, rax
	jne	.L3
.L1:
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1072693248
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
