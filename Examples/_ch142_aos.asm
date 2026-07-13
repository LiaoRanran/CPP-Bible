	.file	"_ch142_aos.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z13integrate_aosP8Particleif
	.def	_Z13integrate_aosP8Particleif;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13integrate_aosP8Particleif
_Z13integrate_aosP8Particleif:
.LFB1715:
	.seh_endprologue
	test	edx, edx
	jle	.L1
	movsx	rdx, edx
	lea	rax, [rdx+rdx*2]
	lea	rax, [rcx+rax*8]
	.p2align 4,,10
	.p2align 3
.L3:
	movss	xmm0, DWORD PTR 12[rcx]
	add	rcx, 24
	mulss	xmm0, xmm2
	addss	xmm0, DWORD PTR -24[rcx]
	movss	DWORD PTR -24[rcx], xmm0
	cmp	rax, rcx
	jne	.L3
.L1:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1716:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	call	__main
	mov	ecx, 24576
	call	_Znwy
	mov	QWORD PTR [rax], 0
	lea	rdx, 24[rax]
	mov	rcx, rax
	mov	QWORD PTR 8[rax], 0
	lea	rax, 24576[rax]
	mov	QWORD PTR -24560[rax], 0
	.p2align 4,,10
	.p2align 3
.L7:
	mov	r8, QWORD PTR [rcx]
	add	rdx, 24
	mov	QWORD PTR -24[rdx], r8
	mov	r8, QWORD PTR 8[rcx]
	mov	QWORD PTR -16[rdx], r8
	mov	r8, QWORD PTR 16[rcx]
	mov	QWORD PTR -8[rdx], r8
	cmp	rdx, rax
	jne	.L7
	movss	xmm1, DWORD PTR .LC0[rip]
	mov	rdx, rcx
	.p2align 4,,10
	.p2align 3
.L8:
	movss	xmm0, DWORD PTR 12[rdx]
	add	rdx, 24
	mulss	xmm0, xmm1
	addss	xmm0, DWORD PTR -24[rdx]
	movss	DWORD PTR -24[rdx], xmm0
	cmp	rdx, rax
	jne	.L8
	cvttss2si	ebx, DWORD PTR [rcx]
	mov	edx, 24576
	call	_ZdlPvy
	mov	eax, ebx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 4
.LC0:
	.long	1015222895
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
