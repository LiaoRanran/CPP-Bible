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
	pxor	xmm4, xmm4
	sal	rdx, 3
	lea	rax, [rcx+rdx]
	cmp	rdx, 24
	jle	.L9
	.p2align 4
	.p2align 3
.L3:
	movsd	xmm0, QWORD PTR 8[rcx]
	movsd	xmm3, QWORD PTR [rcx]
	mov	rdx, rax
	add	rcx, 32
	movsd	xmm1, QWORD PTR -8[rcx]
	movsd	xmm2, QWORD PTR -16[rcx]
	sub	rdx, rcx
	mulsd	xmm0, xmm0
	mulsd	xmm3, xmm3
	mulsd	xmm1, xmm1
	mulsd	xmm2, xmm2
	addsd	xmm0, xmm3
	addsd	xmm1, xmm2
	addsd	xmm0, xmm1
	addsd	xmm4, xmm0
	cmp	rdx, 24
	jg	.L3
	cmp	rax, rcx
	je	.L11
	.p2align 4
	.p2align 3
.L5:
	movsd	xmm0, QWORD PTR [rcx]
	add	rcx, 8
	mulsd	xmm0, xmm0
	addsd	xmm4, xmm0
.L9:
	cmp	rax, rcx
	jne	.L5
.L11:
	movapd	xmm0, xmm4
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6tr_mulPKdS0_y
	.def	_Z6tr_mulPKdS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6tr_mulPKdS0_y
_Z6tr_mulPKdS0_y:
.LFB1209:
	.seh_endprologue
	pxor	xmm2, xmm2
	sal	r8, 3
	lea	rax, [rcx+r8]
	cmp	r8, 24
	jle	.L13
	.p2align 4
	.p2align 3
.L14:
	movsd	xmm0, QWORD PTR 8[rdx]
	movsd	xmm1, QWORD PTR [rdx]
	add	rcx, 32
	mov	r8, rax
	mulsd	xmm1, QWORD PTR -32[rcx]
	movsd	xmm3, QWORD PTR 16[rdx]
	add	rdx, 32
	mulsd	xmm0, QWORD PTR -24[rcx]
	mulsd	xmm3, QWORD PTR -16[rcx]
	addsd	xmm0, xmm1
	movsd	xmm1, QWORD PTR -8[rdx]
	mulsd	xmm1, QWORD PTR -8[rcx]
	sub	r8, rcx
	addsd	xmm1, xmm3
	addsd	xmm0, xmm1
	addsd	xmm2, xmm0
	cmp	r8, 24
	jg	.L14
.L13:
	cmp	rax, rcx
	je	.L12
	sub	rax, rcx
	mov	r8, rax
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L16:
	movsd	xmm0, QWORD PTR [rdx+rax]
	mulsd	xmm0, QWORD PTR [rcx+rax]
	add	rax, 8
	addsd	xmm2, xmm0
	cmp	r8, rax
	jne	.L16
.L12:
	movapd	xmm0, xmm2
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6tr_intPKxS0_y
	.def	_Z6tr_intPKxS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6tr_intPKxS0_y
_Z6tr_intPKxS0_y:
.LFB1216:
	.seh_endprologue
	xor	r9d, r9d
	mov	rax, rcx
	sal	r8, 3
	mov	rcx, rdx
	lea	r11, [rax+r8]
	cmp	r8, 24
	jle	.L21
	.p2align 4
	.p2align 3
.L22:
	mov	rdx, QWORD PTR 8[rcx]
	mov	r8, QWORD PTR [rcx]
	add	rax, 32
	add	rcx, 32
	imul	r8, QWORD PTR -32[rax]
	mov	r10, QWORD PTR -16[rcx]
	imul	rdx, QWORD PTR -24[rax]
	imul	r10, QWORD PTR -16[rax]
	add	rdx, r8
	mov	r8, QWORD PTR -8[rcx]
	imul	r8, QWORD PTR -8[rax]
	add	r8, r10
	add	rdx, r8
	add	r9, rdx
	mov	rdx, r11
	sub	rdx, rax
	cmp	rdx, 24
	jg	.L22
.L21:
	cmp	r11, rax
	je	.L20
	sub	r11, rax
	xor	edx, edx
	.p2align 5
	.p2align 4
	.p2align 3
.L24:
	mov	r8, QWORD PTR [rcx+rdx]
	imul	r8, QWORD PTR [rax+rdx]
	add	rdx, 8
	add	r9, r8
	cmp	r11, rdx
	jne	.L24
.L20:
	mov	rax, r9
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
