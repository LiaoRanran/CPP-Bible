	.file	"_ch99_transform_reduce.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z9tr_squarePKdy
	.def	_Z9tr_squarePKdy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9tr_squarePKdy
_Z9tr_squarePKdy:
.LFB1202:
	.seh_endprologue
	vxorpd	xmm4, xmm4, xmm4
	sal	rdx, 3
	mov	rax, rcx
	lea	rcx, [rcx+rdx]
	cmp	rdx, 24
	jle	.L2
	.p2align 4
	.p2align 3
.L3:
	vmovsd	xmm3, QWORD PTR 8[rax]
	vmovsd	xmm0, QWORD PTR [rax]
	mov	rdx, rcx
	add	rax, 32
	vmovsd	xmm2, QWORD PTR -8[rax]
	vmovsd	xmm1, QWORD PTR -16[rax]
	sub	rdx, rax
	vmulsd	xmm0, xmm0, xmm0
	vmulsd	xmm3, xmm3, xmm3
	vmulsd	xmm1, xmm1, xmm1
	vmulsd	xmm2, xmm2, xmm2
	vaddsd	xmm0, xmm0, xmm3
	vaddsd	xmm1, xmm1, xmm2
	vaddsd	xmm0, xmm0, xmm1
	vaddsd	xmm4, xmm4, xmm0
	cmp	rdx, 24
	jg	.L3
.L2:
	cmp	rcx, rax
	je	.L1
	lea	r9, -8[rcx]
	mov	rdx, rax
	sub	r9, rax
	cmp	r9, 16
	jbe	.L5
	shr	r9, 3
	vxorpd	xmm1, xmm1, xmm1
	add	r9, 1
	mov	r8, r9
	shr	r8, 2
	sal	r8, 5
	add	r8, rax
	.p2align 5
	.p2align 4
	.p2align 3
.L6:
	vmovupd	ymm0, YMMWORD PTR [rdx]
	add	rdx, 32
	vmulpd	ymm0, ymm0, ymm0
	vaddpd	ymm1, ymm1, ymm0
	cmp	rdx, r8
	jne	.L6
	vextractf128	xmm0, ymm1, 0x1
	vaddpd	xmm1, xmm0, xmm1
	vunpckhpd	xmm0, xmm1, xmm1
	vaddpd	xmm0, xmm0, xmm1
	vaddsd	xmm4, xmm4, xmm0
	test	r9b, 3
	je	.L15
	and	r9, -4
	lea	rax, [rax+r9*8]
	vzeroupper
.L5:
	vmovsd	xmm0, QWORD PTR [rax]
	lea	rdx, 8[rax]
	vmulsd	xmm0, xmm0, xmm0
	vaddsd	xmm4, xmm4, xmm0
	cmp	rcx, rdx
	je	.L1
	vmovsd	xmm0, QWORD PTR 8[rax]
	lea	rdx, 16[rax]
	vmulsd	xmm0, xmm0, xmm0
	vaddsd	xmm4, xmm4, xmm0
	cmp	rcx, rdx
	je	.L1
	vmovsd	xmm0, QWORD PTR 16[rax]
	vmulsd	xmm0, xmm0, xmm0
	vaddsd	xmm4, xmm4, xmm0
.L1:
	vmovapd	xmm0, xmm4
	ret
	.p2align 4,,10
	.p2align 3
.L15:
	vzeroupper
	vmovapd	xmm0, xmm4
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6tr_mulPKdS0_y
	.def	_Z6tr_mulPKdS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6tr_mulPKdS0_y
_Z6tr_mulPKdS0_y:
.LFB1209:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	vxorpd	xmm3, xmm3, xmm3
	sal	r8, 3
	mov	rax, rcx
	lea	r9, [rcx+r8]
	cmp	r8, 24
	jle	.L18
	.p2align 4
	.p2align 3
.L19:
	vmovsd	xmm0, QWORD PTR 8[rdx]
	vmovsd	xmm1, QWORD PTR [rdx]
	add	rax, 32
	mov	rcx, r9
	vmulsd	xmm1, xmm1, QWORD PTR -32[rax]
	vmovsd	xmm2, QWORD PTR 16[rdx]
	add	rdx, 32
	vmulsd	xmm0, xmm0, QWORD PTR -24[rax]
	vmulsd	xmm2, xmm2, QWORD PTR -16[rax]
	vaddsd	xmm0, xmm0, xmm1
	vmovsd	xmm1, QWORD PTR -8[rdx]
	vmulsd	xmm1, xmm1, QWORD PTR -8[rax]
	sub	rcx, rax
	vaddsd	xmm1, xmm1, xmm2
	vaddsd	xmm0, xmm0, xmm1
	vaddsd	xmm3, xmm3, xmm0
	cmp	rcx, 24
	jg	.L19
.L18:
	cmp	r9, rax
	je	.L28
	sub	r9, 8
	sub	r9, rax
	mov	r11, r9
	shr	r11, 3
	lea	r10, 1[r11]
	cmp	r9, 16
	jbe	.L29
	mov	r8, r10
	xor	ecx, ecx
	vxorpd	xmm1, xmm1, xmm1
	shr	r8, 2
	sal	r8, 5
	.p2align 5
	.p2align 4
	.p2align 3
.L22:
	vmovupd	ymm0, YMMWORD PTR [rax+rcx]
	vmulpd	ymm0, ymm0, YMMWORD PTR [rdx+rcx]
	add	rcx, 32
	vaddpd	ymm1, ymm1, ymm0
	cmp	r8, rcx
	jne	.L22
	vextractf128	xmm0, ymm1, 0x1
	vaddpd	xmm1, xmm0, xmm1
	vunpckhpd	xmm0, xmm1, xmm1
	vaddpd	xmm0, xmm0, xmm1
	vaddsd	xmm0, xmm0, xmm3
	test	r10b, 3
	je	.L38
	mov	rcx, r10
	and	rcx, -4
	lea	r8, 0[0+rcx*8]
	lea	rbx, [rax+r8]
	add	r8, rdx
	vzeroupper
.L21:
	cmp	rcx, r11
	je	.L25
	vmovupd	xmm0, XMMWORD PTR [rax+rcx*8]
	vmulpd	xmm0, xmm0, XMMWORD PTR [rdx+rcx*8]
	mov	r9, r10
	sub	r9, rcx
	and	r10d, 1
	vaddpd	xmm1, xmm0, xmm1
	vunpckhpd	xmm0, xmm1, xmm1
	vaddpd	xmm0, xmm0, xmm1
	vaddsd	xmm0, xmm0, xmm3
	je	.L17
	and	r9, -2
	lea	rax, 0[0+r9*8]
	add	rbx, rax
	add	r8, rax
.L25:
	vmovsd	xmm1, QWORD PTR [r8]
	vmulsd	xmm1, xmm1, QWORD PTR [rbx]
	vaddsd	xmm0, xmm0, xmm1
.L17:
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L38:
	vzeroupper
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L28:
	vmovapd	xmm0, xmm3
	pop	rbx
	ret
.L29:
	vmovapd	xmm0, xmm3
	mov	rbx, rax
	mov	r8, rdx
	xor	ecx, ecx
	vxorpd	xmm1, xmm1, xmm1
	jmp	.L21
	.seh_endproc
	.p2align 4
	.globl	_Z6tr_intPKxS0_y
	.def	_Z6tr_intPKxS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6tr_intPKxS0_y
_Z6tr_intPKxS0_y:
.LFB1216:
	.seh_endprologue
	xor	r10d, r10d
	mov	rax, rcx
	sal	r8, 3
	mov	rcx, rdx
	lea	r11, [rax+r8]
	cmp	r8, 24
	jle	.L40
	.p2align 4
	.p2align 3
.L41:
	mov	rdx, QWORD PTR 8[rcx]
	mov	r8, QWORD PTR [rcx]
	add	rax, 32
	add	rcx, 32
	imul	r8, QWORD PTR -32[rax]
	mov	r9, QWORD PTR -16[rcx]
	imul	rdx, QWORD PTR -24[rax]
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
	jg	.L41
.L40:
	cmp	r11, rax
	je	.L39
	lea	r8, -8[r11]
	sub	r8, rax
	cmp	r8, 16
	jbe	.L43
	shr	r8, 3
	xor	edx, edx
	vpxor	xmm5, xmm5, xmm5
	add	r8, 1
	mov	r9, r8
	shr	r9, 2
	sal	r9, 5
	.p2align 6
	.p2align 4
	.p2align 3
.L44:
	vmovdqu	ymm3, YMMWORD PTR [rcx+rdx]
	vmovdqu	ymm4, YMMWORD PTR [rax+rdx]
	add	rdx, 32
	vpsrlq	ymm0, ymm3, 32
	vpsrlq	ymm2, ymm4, 32
	vpmuludq	ymm0, ymm0, ymm4
	vpmuludq	ymm2, ymm2, ymm3
	vpmuludq	ymm1, ymm3, ymm4
	vpaddq	ymm0, ymm0, ymm2
	vpsllq	ymm0, ymm0, 32
	vpaddq	ymm0, ymm1, ymm0
	vpaddq	ymm5, ymm5, ymm0
	cmp	r9, rdx
	jne	.L44
	vextracti128	xmm0, ymm5, 0x1
	vpaddq	xmm0, xmm0, xmm5
	vpsrldq	xmm1, xmm0, 8
	vpaddq	xmm0, xmm0, xmm1
	vmovq	rdx, xmm0
	add	r10, rdx
	test	r8b, 3
	je	.L53
	and	r8, -4
	sal	r8, 3
	add	rax, r8
	add	rcx, r8
	vzeroupper
.L43:
	mov	rdx, QWORD PTR [rcx]
	imul	rdx, QWORD PTR [rax]
	add	r10, rdx
	lea	rdx, 8[rax]
	cmp	r11, rdx
	je	.L39
	mov	rdx, QWORD PTR 8[rcx]
	imul	rdx, QWORD PTR 8[rax]
	add	r10, rdx
	lea	rdx, 16[rax]
	cmp	r11, rdx
	je	.L39
	mov	rax, QWORD PTR 16[rax]
	imul	rax, QWORD PTR 16[rcx]
	add	r10, rax
.L39:
	mov	rax, r10
	ret
	.p2align 4,,10
	.p2align 3
.L53:
	mov	rax, r10
	vzeroupper
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
