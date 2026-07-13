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
	sal	rdx, 3
	lea	r9, [rcx+rdx]
	cmp	rdx, 24
	mov	edx, 0
	jle	.L9
	.p2align 4,,10
	.p2align 3
.L3:
	mov	rax, QWORD PTR 8[rcx]
	add	rcx, 32
	add	rax, QWORD PTR -32[rcx]
	mov	r8, QWORD PTR -8[rcx]
	add	r8, QWORD PTR -16[rcx]
	add	rax, r8
	add	rdx, rax
	mov	rax, r9
	sub	rax, rcx
	cmp	rax, 24
	jg	.L3
	cmp	r9, rcx
	je	.L11
	.p2align 4,,10
	.p2align 3
.L5:
	add	rdx, QWORD PTR [rcx]
	add	rcx, 8
.L9:
	cmp	r9, rcx
	jne	.L5
.L11:
	mov	rax, rdx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9accum_intPKxy
	.def	_Z9accum_intPKxy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9accum_intPKxy
_Z9accum_intPKxy:
.LFB485:
	.seh_endprologue
	xor	eax, eax
	lea	rdx, [rcx+rdx*8]
	cmp	rdx, rcx
	je	.L12
	.p2align 4,,10
	.p2align 3
.L14:
	add	rax, QWORD PTR [rcx]
	add	rcx, 8
	cmp	rdx, rcx
	jne	.L14
.L12:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10reduce_dblPKdy
	.def	_Z10reduce_dblPKdy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10reduce_dblPKdy
_Z10reduce_dblPKdy:
.LFB486:
	.seh_endprologue
	pxor	xmm1, xmm1
	sal	rdx, 3
	lea	r8, [rcx+rdx]
	cmp	rdx, 24
	jle	.L18
	.p2align 4,,10
	.p2align 3
.L19:
	movsd	xmm0, QWORD PTR [rcx]
	mov	rax, r8
	add	rcx, 32
	addsd	xmm0, QWORD PTR -24[rcx]
	movsd	xmm2, QWORD PTR -16[rcx]
	addsd	xmm2, QWORD PTR -8[rcx]
	sub	rax, rcx
	cmp	rax, 24
	addsd	xmm0, xmm2
	addsd	xmm1, xmm0
	jg	.L19
.L18:
	cmp	r8, rcx
	je	.L17
	mov	rax, r8
	sub	rax, rcx
	test	al, 8
	je	.L21
	addsd	xmm1, QWORD PTR [rcx]
	add	rcx, 8
	cmp	r8, rcx
	je	.L17
	.p2align 4,,10
	.p2align 3
.L21:
	addsd	xmm1, QWORD PTR [rcx]
	add	rcx, 16
	addsd	xmm1, QWORD PTR -8[rcx]
	cmp	r8, rcx
	jne	.L21
.L17:
	movapd	xmm0, xmm1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9accum_dblPKdy
	.def	_Z9accum_dblPKdy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9accum_dblPKdy
_Z9accum_dblPKdy:
.LFB487:
	.seh_endprologue
	pxor	xmm0, xmm0
	lea	rax, [rcx+rdx*8]
	cmp	rax, rcx
	je	.L30
	mov	rdx, rax
	sub	rdx, rcx
	and	edx, 8
	je	.L32
	movsd	xmm0, QWORD PTR [rcx]
	add	rcx, 8
	cmp	rax, rcx
	je	.L30
	.p2align 4,,10
	.p2align 3
.L32:
	addsd	xmm0, QWORD PTR [rcx]
	add	rcx, 16
	addsd	xmm0, QWORD PTR -8[rcx]
	cmp	rax, rcx
	jne	.L32
.L30:
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
