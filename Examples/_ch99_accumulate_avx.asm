	.file	"_ch99_accumulate.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10reduce_intPKxy
	.def	_Z10reduce_intPKxy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10reduce_intPKxy
_Z10reduce_intPKxy:
.LFB484:
	.seh_endprologue
	xor	r8d, r8d
	sal	rdx, 3
	mov	rax, rcx
	lea	r9, [rcx+rdx]
	cmp	rdx, 24
	jle	.L2
	.p2align 4,,10
	.p2align 3
.L3:
	mov	rdx, QWORD PTR 8[rax]
	add	rax, 32
	add	rdx, QWORD PTR -32[rax]
	mov	rcx, QWORD PTR -8[rax]
	add	rcx, QWORD PTR -16[rax]
	add	rdx, rcx
	add	r8, rdx
	mov	rdx, r9
	sub	rdx, rax
	cmp	rdx, 24
	jg	.L3
.L2:
	cmp	r9, rax
	je	.L1
	lea	rcx, -8[r9]
	mov	rdx, rax
	sub	rcx, rax
	mov	r10, rcx
	shr	r10, 3
	add	r10, 1
	cmp	rcx, 16
	jbe	.L5
	mov	rcx, r10
	vpxor	xmm0, xmm0, xmm0
	shr	rcx, 2
	sal	rcx, 5
	add	rcx, rax
	.p2align 4,,10
	.p2align 3
.L6:
	vpaddq	ymm0, ymm0, YMMWORD PTR [rdx]
	add	rdx, 32
	cmp	rcx, rdx
	jne	.L6
	vmovdqa	xmm1, xmm0
	vextracti128	xmm0, ymm0, 0x1
	vpaddq	xmm0, xmm1, xmm0
	vpsrldq	xmm1, xmm0, 8
	vpaddq	xmm0, xmm0, xmm1
	vmovq	rdx, xmm0
	add	r8, rdx
	test	r10b, 3
	je	.L15
	and	r10, -4
	lea	rax, [rax+r10*8]
	vzeroupper
.L5:
	lea	rdx, 8[rax]
	add	r8, QWORD PTR [rax]
	cmp	r9, rdx
	je	.L1
	lea	rdx, 16[rax]
	add	r8, QWORD PTR 8[rax]
	cmp	r9, rdx
	je	.L1
	add	r8, QWORD PTR 16[rax]
.L1:
	mov	rax, r8
	ret
	.p2align 4,,10
	.p2align 3
.L15:
	mov	rax, r8
	vzeroupper
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9accum_intPKxy
	.def	_Z9accum_intPKxy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9accum_intPKxy
_Z9accum_intPKxy:
.LFB485:
	.seh_endprologue
	sal	rdx, 3
	lea	r9, [rcx+rdx]
	cmp	r9, rcx
	je	.L23
	sub	rdx, 8
	mov	r8, rdx
	shr	r8, 3
	add	r8, 1
	cmp	rdx, 16
	jbe	.L24
	mov	rdx, r8
	mov	rax, rcx
	vpxor	xmm0, xmm0, xmm0
	shr	rdx, 2
	sal	rdx, 5
	add	rdx, rcx
	.p2align 4,,10
	.p2align 3
.L20:
	vpaddq	ymm0, ymm0, YMMWORD PTR [rax]
	add	rax, 32
	cmp	rax, rdx
	jne	.L20
	vmovdqa	xmm1, xmm0
	vextracti128	xmm0, ymm0, 0x1
	test	r8b, 3
	vpaddq	xmm0, xmm1, xmm0
	vpsrldq	xmm1, xmm0, 8
	vpaddq	xmm0, xmm0, xmm1
	vmovq	rax, xmm0
	je	.L29
	and	r8, -4
	lea	rcx, [rcx+r8*8]
	vzeroupper
.L19:
	lea	rdx, 8[rcx]
	add	rax, QWORD PTR [rcx]
	cmp	r9, rdx
	je	.L17
	lea	rdx, 16[rcx]
	add	rax, QWORD PTR 8[rcx]
	cmp	r9, rdx
	je	.L17
	add	rax, QWORD PTR 16[rcx]
.L17:
	ret
	.p2align 4,,10
	.p2align 3
.L29:
	vzeroupper
	ret
	.p2align 4,,10
	.p2align 3
.L23:
	xor	eax, eax
	ret
.L24:
	xor	eax, eax
	jmp	.L19
	.seh_endproc
	.p2align 4
	.globl	_Z10reduce_dblPKdy
	.def	_Z10reduce_dblPKdy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10reduce_dblPKdy
_Z10reduce_dblPKdy:
.LFB486:
	.seh_endprologue
	vxorpd	xmm2, xmm2, xmm2
	sal	rdx, 3
	mov	rax, rcx
	lea	rcx, [rcx+rdx]
	cmp	rdx, 24
	jle	.L31
	.p2align 4,,10
	.p2align 3
.L32:
	vmovsd	xmm0, QWORD PTR 16[rax]
	mov	rdx, rcx
	add	rax, 32
	vaddsd	xmm0, xmm0, QWORD PTR -8[rax]
	vmovsd	xmm1, QWORD PTR -32[rax]
	vaddsd	xmm1, xmm1, QWORD PTR -24[rax]
	sub	rdx, rax
	cmp	rdx, 24
	vaddsd	xmm0, xmm0, xmm1
	vaddsd	xmm2, xmm2, xmm0
	jg	.L32
.L31:
	cmp	rcx, rax
	je	.L30
	lea	r8, -8[rcx]
	mov	rdx, rax
	sub	r8, rax
	mov	r9, r8
	shr	r9, 3
	add	r9, 1
	cmp	r8, 16
	jbe	.L34
	mov	r8, r9
	vxorpd	xmm0, xmm0, xmm0
	shr	r8, 2
	sal	r8, 5
	add	r8, rax
	.p2align 4,,10
	.p2align 3
.L35:
	vaddpd	ymm0, ymm0, YMMWORD PTR [rdx]
	add	rdx, 32
	cmp	r8, rdx
	jne	.L35
	vextractf128	xmm1, ymm0, 0x1
	vaddpd	xmm1, xmm1, xmm0
	test	r9b, 3
	vunpckhpd	xmm0, xmm1, xmm1
	vaddpd	xmm0, xmm0, xmm1
	vaddsd	xmm2, xmm2, xmm0
	je	.L44
	and	r9, -4
	lea	rax, [rax+r9*8]
	vzeroupper
.L34:
	lea	rdx, 8[rax]
	vaddsd	xmm2, xmm2, QWORD PTR [rax]
	cmp	rcx, rdx
	je	.L30
	lea	rdx, 16[rax]
	vaddsd	xmm2, xmm2, QWORD PTR 8[rax]
	cmp	rcx, rdx
	je	.L30
	vaddsd	xmm2, xmm2, QWORD PTR 16[rax]
.L30:
	vmovsd	xmm0, xmm2, xmm2
	ret
	.p2align 4,,10
	.p2align 3
.L44:
	vzeroupper
	vmovsd	xmm0, xmm2, xmm2
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9accum_dblPKdy
	.def	_Z9accum_dblPKdy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9accum_dblPKdy
_Z9accum_dblPKdy:
.LFB487:
	.seh_endprologue
	sal	rdx, 3
	lea	r9, [rcx+rdx]
	cmp	r9, rcx
	je	.L51
	sub	rdx, 8
	mov	r8, rdx
	shr	r8, 3
	add	r8, 1
	cmp	rdx, 16
	jbe	.L52
	mov	rdx, r8
	mov	rax, rcx
	vxorpd	xmm0, xmm0, xmm0
	shr	rdx, 2
	sal	rdx, 5
	add	rdx, rcx
	.p2align 4,,10
	.p2align 3
.L48:
	vaddpd	ymm0, ymm0, YMMWORD PTR [rax]
	add	rax, 32
	cmp	rax, rdx
	jne	.L48
	vextractf128	xmm1, ymm0, 0x1
	vaddpd	xmm1, xmm1, xmm0
	test	r8b, 3
	vunpckhpd	xmm0, xmm1, xmm1
	vaddpd	xmm0, xmm0, xmm1
	je	.L57
	and	r8, -4
	lea	rcx, [rcx+r8*8]
	vzeroupper
.L47:
	lea	rax, 8[rcx]
	vaddsd	xmm0, xmm0, QWORD PTR [rcx]
	cmp	r9, rax
	je	.L45
	lea	rax, 16[rcx]
	vaddsd	xmm0, xmm0, QWORD PTR 8[rcx]
	cmp	r9, rax
	je	.L45
	vaddsd	xmm0, xmm0, QWORD PTR 16[rcx]
.L45:
	ret
	.p2align 4,,10
	.p2align 3
.L57:
	vzeroupper
	ret
	.p2align 4,,10
	.p2align 3
.L51:
	vxorpd	xmm0, xmm0, xmm0
	ret
.L52:
	vxorpd	xmm0, xmm0, xmm0
	jmp	.L47
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
