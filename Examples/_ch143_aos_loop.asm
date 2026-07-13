	.file	"_ch143_aos_loop.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8step_aosP1Pif
	.def	_Z8step_aosP1Pif;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8step_aosP1Pif
_Z8step_aosP1Pif:
.LFB0:
	.seh_endprologue
	movsldup	xmm2, xmm2
	test	edx, edx
	jle	.L4
	movsx	rdx, edx
	pxor	xmm1, xmm1
	sal	rdx, 4
	lea	rax, [rcx+rdx]
	.p2align 4,,10
	.p2align 3
.L3:
	movq	xmm0, QWORD PTR 8[rcx]
	add	rcx, 16
	movq	xmm3, QWORD PTR -16[rcx]
	mulps	xmm0, xmm2
	addps	xmm0, xmm3
	movlps	QWORD PTR -16[rcx], xmm0
	cmp	rcx, rax
	addss	xmm1, xmm0
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
