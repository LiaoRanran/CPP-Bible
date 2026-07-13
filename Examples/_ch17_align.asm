	.file	"_ch17_align.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	vec_broadcast
	.def	vec_broadcast;	.scl	2;	.type	32;	.endef
	.seh_proc	vec_broadcast
vec_broadcast:
.LFB16:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	r8, 31[rsp]
	vmovddup	xmm0, xmm1
	vinsertf128	ymm0, ymm0, xmm0, 1
	and	r8, -32
	test	rcx, rcx
	vmovapd	YMMWORD PTR [r8], ymm0
	je	.L7
	vxorpd	xmm0, xmm0, xmm0
	vaddsd	xmm1, xmm1, xmm0
	cmp	rcx, 1
	vxorps	xmm2, xmm2, xmm2
	mov	eax, 1
	vcvttsd2si	r9d, xmm1
	vmovsd	QWORD PTR [r8], xmm1
	jne	.L3
	jmp	.L2
	.p2align 4,,10
	.p2align 3
.L12:
	vcvtsi2sd	xmm0, xmm2, rax
.L5:
	vaddsd	xmm0, xmm0, QWORD PTR [r8+rdx*8]
	add	rax, 1
	vmovsd	QWORD PTR [r8+rdx*8], xmm0
	vcvttsd2si	edx, xmm0
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
	shr	r10
	and	r11d, 1
	or	r10, r11
	vcvtsi2sd	xmm0, xmm2, r10
	vaddsd	xmm0, xmm0, xmm0
	jmp	.L5
	.p2align 4,,10
	.p2align 3
.L7:
	xor	r9d, r9d
.L2:
	mov	DWORD PTR sink[rip], r9d
	mov	eax, r9d
	vzeroupper
	add	rsp, 56
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB17:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	vmovsd	xmm1, QWORD PTR .LC1[rip]
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
