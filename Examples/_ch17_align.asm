	.file	"_ch17_align.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	vec_broadcast
	.def	vec_broadcast;	.scl	2;	.type	32;	.endef
	.seh_proc	vec_broadcast
vec_broadcast:
.LFB17:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	r8, 31[rsp]
	movapd	xmm0, xmm1
	and	r8, -32
	unpcklpd	xmm0, xmm0
	movaps	XMMWORD PTR [r8], xmm0
	movaps	XMMWORD PTR 16[r8], xmm0
	test	rcx, rcx
	je	.L7
	pxor	xmm0, xmm0
	mov	eax, 1
	addsd	xmm1, xmm0
	cvttsd2si	r9d, xmm1
	movsd	QWORD PTR [r8], xmm1
	cmp	rcx, 1
	jne	.L3
	jmp	.L2
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L12:
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rax
.L5:
	addsd	xmm0, QWORD PTR [r8+rdx*8]
	add	rax, 1
	movsd	QWORD PTR [r8+rdx*8], xmm0
	cvttsd2si	edx, xmm0
	add	r9d, edx
	cmp	rcx, rax
	je	.L2
.L3:
	mov	rdx, rax
	and	edx, 3
	test	rax, rax
	jns	.L12
	mov	r10, rax
	mov	r11, rax
	pxor	xmm0, xmm0
	shr	r10
	and	r11d, 1
	or	r10, r11
	cvtsi2sd	xmm0, r10
	addsd	xmm0, xmm0
	jmp	.L5
	.p2align 4,,10
	.p2align 3
.L7:
	xor	r9d, r9d
.L2:
	mov	eax, r9d
	mov	DWORD PTR sink[rip], r9d
	add	rsp, 56
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB18:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	movsd	xmm1, QWORD PTR .LC1[rip]
	mov	ecx, 8
	add	rsp, 40
	jmp	vec_broadcast
	.seh_endproc
	.globl	sink
	.bss
	.align 4
sink:
	.space 4
	.section .rdata,"dr"
	.align 8
.LC1:
	.long	0
	.long	1073741824
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
