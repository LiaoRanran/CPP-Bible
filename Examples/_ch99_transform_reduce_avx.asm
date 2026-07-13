	.file	"_ch99_transform_reduce.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z9tr_squarePKdy
	.def	_Z9tr_squarePKdy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9tr_squarePKdy
_Z9tr_squarePKdy:
.LFB484:
	.seh_endprologue
	vxorpd	xmm4, xmm4, xmm4
	sal	rdx, 3
	mov	rax, rcx
	lea	rcx, [rcx+rdx]
	cmp	rdx, 24
	jle	.L2
	.p2align 4,,10
	.p2align 3
.L3:
	vmovsd	xmm0, QWORD PTR 8[rax]
	mov	rdx, rcx
	add	rax, 32
	vmovsd	xmm3, QWORD PTR -32[rax]
	vmovsd	xmm1, QWORD PTR -8[rax]
	vmulsd	xmm0, xmm0, xmm0
	vmovsd	xmm2, QWORD PTR -16[rax]
	vmulsd	xmm3, xmm3, xmm3
	sub	rdx, rax
	vmulsd	xmm1, xmm1, xmm1
	cmp	rdx, 24
	vmulsd	xmm2, xmm2, xmm2
	vaddsd	xmm0, xmm0, xmm3
	vaddsd	xmm1, xmm1, xmm2
	vaddsd	xmm0, xmm0, xmm1
	vaddsd	xmm4, xmm4, xmm0
	jg	.L3
.L2:
	cmp	rcx, rax
	je	.L12
	sub	rcx, 8
	mov	rdx, rax
	sub	rcx, rax
	mov	r9, rcx
	shr	r9, 3
	cmp	rcx, 16
	lea	r8, 1[r9]
	jbe	.L13
	mov	rcx, r8
	vxorpd	xmm1, xmm1, xmm1
	shr	rcx, 2
	sal	rcx, 5
	add	rcx, rax
	.p2align 4,,10
	.p2align 3
.L6:
	vmovupd	ymm5, YMMWORD PTR [rdx]
	add	rdx, 32
	cmp	rcx, rdx
	vmulpd	ymm0, ymm5, ymm5
	vaddpd	ymm1, ymm1, ymm0
	jne	.L6
	vextractf128	xmm3, ymm1, 0x1
	vaddpd	xmm2, xmm3, xmm1
	mov	rcx, r8
	and	rcx, -4
	vaddpd	xmm1, xmm1, xmm3
	test	r8b, 3
	lea	rdx, [rax+rcx*8]
	vunpckhpd	xmm0, xmm2, xmm2
	vaddpd	xmm0, xmm0, xmm2
	vaddsd	xmm0, xmm4, xmm0
	je	.L24
	vzeroupper
.L5:
	sub	r8, rcx
	cmp	rcx, r9
	je	.L9
	vmovupd	xmm0, XMMWORD PTR [rax+rcx*8]
	test	r8b, 1
	vmulpd	xmm0, xmm0, xmm0
	vaddpd	xmm1, xmm0, xmm1
	vunpckhpd	xmm0, xmm1, xmm1
	vaddpd	xmm0, xmm0, xmm1
	vaddsd	xmm0, xmm4, xmm0
	je	.L1
	and	r8, -2
	lea	rdx, [rdx+r8*8]
.L9:
	vmovsd	xmm1, QWORD PTR [rdx]
	vmulsd	xmm1, xmm1, xmm1
	vaddsd	xmm0, xmm0, xmm1
.L1:
	ret
	.p2align 4,,10
	.p2align 3
.L24:
	vzeroupper
	ret
	.p2align 4,,10
	.p2align 3
.L12:
	vmovsd	xmm0, xmm4, xmm4
	ret
.L13:
	vmovsd	xmm0, xmm4, xmm4
	xor	ecx, ecx
	vxorpd	xmm1, xmm1, xmm1
	jmp	.L5
	.seh_endproc
	.p2align 4
	.globl	_Z6tr_mulPKdS0_y
	.def	_Z6tr_mulPKdS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6tr_mulPKdS0_y
_Z6tr_mulPKdS0_y:
.LFB491:
	.seh_endprologue
	vxorpd	xmm3, xmm3, xmm3
	sal	r8, 3
	mov	rax, rcx
	lea	r9, [rcx+r8]
	cmp	r8, 24
	jle	.L26
	.p2align 4,,10
	.p2align 3
.L27:
	vmovsd	xmm0, QWORD PTR 24[rdx]
	add	rax, 32
	mov	rcx, r9
	add	rdx, 32
	vmulsd	xmm0, xmm0, QWORD PTR -8[rax]
	vmovsd	xmm1, QWORD PTR -16[rdx]
	vmulsd	xmm1, xmm1, QWORD PTR -16[rax]
	vmovsd	xmm2, QWORD PTR -32[rdx]
	vmulsd	xmm2, xmm2, QWORD PTR -32[rax]
	vaddsd	xmm0, xmm0, xmm1
	vmovsd	xmm1, QWORD PTR -24[rdx]
	vmulsd	xmm1, xmm1, QWORD PTR -24[rax]
	sub	rcx, rax
	cmp	rcx, 24
	vaddsd	xmm1, xmm1, xmm2
	vaddsd	xmm0, xmm0, xmm1
	vaddsd	xmm3, xmm3, xmm0
	jg	.L27
.L26:
	cmp	r9, rax
	je	.L36
	sub	r9, 8
	sub	r9, rax
	mov	r11, r9
	shr	r11, 3
	cmp	r9, 16
	lea	r8, 1[r11]
	jbe	.L37
	mov	r9, r8
	xor	ecx, ecx
	vxorpd	xmm1, xmm1, xmm1
	shr	r9, 2
	sal	r9, 5
	.p2align 4,,10
	.p2align 3
.L30:
	vmovupd	ymm5, YMMWORD PTR [rdx+rcx]
	vmulpd	ymm0, ymm5, YMMWORD PTR [rax+rcx]
	add	rcx, 32
	vaddpd	ymm1, ymm1, ymm0
	cmp	r9, rcx
	jne	.L30
	vextractf128	xmm4, ymm1, 0x1
	vaddpd	xmm2, xmm4, xmm1
	mov	r10, r8
	and	r10, -4
	vaddpd	xmm1, xmm1, xmm4
	lea	rcx, 0[0+r10*8]
	vunpckhpd	xmm0, xmm2, xmm2
	vaddpd	xmm0, xmm0, xmm2
	lea	r9, [rdx+rcx]
	add	rcx, rax
	test	r8b, 3
	vaddsd	xmm0, xmm3, xmm0
	je	.L47
	vzeroupper
.L29:
	sub	r8, r10
	cmp	r10, r11
	je	.L33
	vmovupd	xmm0, XMMWORD PTR [rax+r10*8]
	test	r8b, 1
	vmulpd	xmm0, xmm0, XMMWORD PTR [rdx+r10*8]
	vaddpd	xmm1, xmm0, xmm1
	vunpckhpd	xmm0, xmm1, xmm1
	vaddpd	xmm0, xmm0, xmm1
	vaddsd	xmm0, xmm3, xmm0
	je	.L25
	and	r8, -2
	sal	r8, 3
	add	r9, r8
	add	rcx, r8
.L33:
	vmovsd	xmm1, QWORD PTR [r9]
	vmulsd	xmm1, xmm1, QWORD PTR [rcx]
	vaddsd	xmm0, xmm0, xmm1
.L25:
	ret
	.p2align 4,,10
	.p2align 3
.L47:
	vzeroupper
	ret
	.p2align 4,,10
	.p2align 3
.L36:
	vmovsd	xmm0, xmm3, xmm3
	ret
.L37:
	vmovsd	xmm0, xmm3, xmm3
	mov	rcx, rax
	mov	r9, rdx
	vxorpd	xmm1, xmm1, xmm1
	xor	r10d, r10d
	jmp	.L29
	.seh_endproc
	.p2align 4
	.globl	_Z6tr_intPKxS0_y
	.def	_Z6tr_intPKxS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6tr_intPKxS0_y
_Z6tr_intPKxS0_y:
.LFB498:
	.seh_endprologue
	xor	r10d, r10d
	sal	r8, 3
	mov	rax, rcx
	mov	rcx, rdx
	lea	r11, [rax+r8]
	cmp	r8, 24
	jle	.L49
	.p2align 4,,10
	.p2align 3
.L50:
	mov	rdx, QWORD PTR 8[rcx]
	add	rax, 32
	add	rcx, 32
	imul	rdx, QWORD PTR -24[rax]
	mov	r8, QWORD PTR -32[rcx]
	imul	r8, QWORD PTR -32[rax]
	mov	r9, QWORD PTR -16[rcx]
	imul	r9, QWORD PTR -16[rax]
	add	rdx, r8
	mov	r8, QWORD PTR -8[rcx]
	imul	r8, QWORD PTR -8[rax]
	add	r8, r9
	add	rdx, r8
	add	r10, rdx
	mov	rdx, r11
	sub	rdx, rax
	cmp	rdx, 24
	jg	.L50
.L49:
	cmp	r11, rax
	je	.L48
	lea	rdx, -8[r11]
	sub	rdx, rax
	mov	r9, rdx
	shr	r9, 3
	add	r9, 1
	cmp	rdx, 16
	jbe	.L52
	mov	r8, r9
	xor	edx, edx
	vpxor	xmm5, xmm5, xmm5
	shr	r8, 2
	sal	r8, 5
	.p2align 4,,10
	.p2align 3
.L53:
	vmovdqu	ymm3, YMMWORD PTR [rax+rdx]
	vmovdqu	ymm4, YMMWORD PTR [rcx+rdx]
	add	rdx, 32
	vpsrlq	ymm0, ymm3, 32
	cmp	r8, rdx
	vpsrlq	ymm2, ymm4, 32
	vpmuludq	ymm0, ymm0, ymm4
	vpmuludq	ymm2, ymm2, ymm3
	vpmuludq	ymm1, ymm3, ymm4
	vpaddq	ymm0, ymm0, ymm2
	vpsllq	ymm0, ymm0, 32
	vpaddq	ymm0, ymm1, ymm0
	vpaddq	ymm5, ymm5, ymm0
	jne	.L53
	vmovdqa	xmm0, xmm5
	vextracti128	xmm5, ymm5, 0x1
	vpaddq	xmm0, xmm0, xmm5
	vpsrldq	xmm1, xmm0, 8
	vpaddq	xmm0, xmm0, xmm1
	vmovq	rdx, xmm0
	add	r10, rdx
	mov	rdx, r9
	and	rdx, -4
	sal	rdx, 3
	add	rcx, rdx
	add	rax, rdx
	and	r9d, 3
	je	.L62
	vzeroupper
.L52:
	mov	rdx, QWORD PTR [rcx]
	imul	rdx, QWORD PTR [rax]
	add	r10, rdx
	lea	rdx, 8[rax]
	cmp	r11, rdx
	je	.L48
	mov	rdx, QWORD PTR 8[rcx]
	imul	rdx, QWORD PTR 8[rax]
	add	r10, rdx
	lea	rdx, 16[rax]
	cmp	r11, rdx
	je	.L48
	mov	rax, QWORD PTR 16[rax]
	imul	rax, QWORD PTR 16[rcx]
	add	r10, rax
.L48:
	mov	rax, r10
	ret
	.p2align 4,,10
	.p2align 3
.L62:
	mov	rax, r10
	vzeroupper
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
