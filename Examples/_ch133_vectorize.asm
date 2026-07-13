	.file	"_ch133_vectorize.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10column_addPKfS0_Pfy
	.def	_Z10column_addPKfS0_Pfy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10column_addPKfS0_Pfy
_Z10column_addPKfS0_Pfy:
.LFB16:
	.seh_endprologue
	test	r9, r9
	je	.L39
	lea	rax, -1[r9]
	cmp	rax, 6
	jbe	.L12
	lea	r11, 4[rcx]
	mov	r10, r8
	sub	r10, r11
	cmp	r10, 56
	jbe	.L12
	lea	r11, 4[rdx]
	mov	r10, r8
	sub	r10, r11
	cmp	r10, 56
	jbe	.L12
	cmp	rax, 14
	jbe	.L13
	mov	r10, r9
	xor	eax, eax
	shr	r10, 4
	sal	r10, 6
	.p2align 4
	.p2align 3
.L5:
	vmovups	zmm1, ZMMWORD PTR [rcx+rax]
	vaddps	zmm0, zmm1, ZMMWORD PTR [rdx+rax]
	vmovups	ZMMWORD PTR [r8+rax], zmm0
	add	rax, 64
	cmp	rax, r10
	jne	.L5
	mov	rax, r9
	and	rax, -16
	test	r9b, 15
	je	.L38
	mov	r11, r9
	sub	r11, rax
	lea	r10, -1[r11]
	cmp	r10, 6
	jbe	.L7
.L4:
	lea	r10, 0[0+rax*4]
	vmovups	ymm2, YMMWORD PTR [rcx+r10]
	vaddps	ymm0, ymm2, YMMWORD PTR [rdx+r10]
	vmovups	YMMWORD PTR [r8+r10], ymm0
	mov	r10, r11
	and	r10, -8
	add	rax, r10
	and	r11d, 7
	je	.L38
.L7:
	lea	r10, 0[0+rax*4]
	lea	r11, 1[rax]
	vmovss	xmm0, DWORD PTR [rcx+r10]
	vaddss	xmm0, xmm0, DWORD PTR [rdx+r10]
	vmovss	DWORD PTR [r8+r10], xmm0
	cmp	r11, r9
	jnb	.L38
	vmovss	xmm0, DWORD PTR 4[rcx+r10]
	vaddss	xmm0, xmm0, DWORD PTR 4[rdx+r10]
	lea	r11, 2[rax]
	vmovss	DWORD PTR 4[r8+r10], xmm0
	cmp	r11, r9
	jnb	.L38
	vmovss	xmm0, DWORD PTR 8[rcx+r10]
	vaddss	xmm0, xmm0, DWORD PTR 8[rdx+r10]
	lea	r11, 3[rax]
	vmovss	DWORD PTR 8[r8+r10], xmm0
	cmp	r11, r9
	jnb	.L38
	vmovss	xmm0, DWORD PTR 12[rcx+r10]
	vaddss	xmm0, xmm0, DWORD PTR 12[rdx+r10]
	lea	r11, 4[rax]
	vmovss	DWORD PTR 12[r8+r10], xmm0
	cmp	r11, r9
	jnb	.L38
	vmovss	xmm0, DWORD PTR 16[rcx+r10]
	vaddss	xmm0, xmm0, DWORD PTR 16[rdx+r10]
	lea	r11, 5[rax]
	vmovss	DWORD PTR 16[r8+r10], xmm0
	cmp	r11, r9
	jnb	.L38
	vmovss	xmm0, DWORD PTR 20[rcx+r10]
	vaddss	xmm0, xmm0, DWORD PTR 20[rdx+r10]
	add	rax, 6
	vmovss	DWORD PTR 20[r8+r10], xmm0
	cmp	rax, r9
	jnb	.L38
	vmovss	xmm0, DWORD PTR 24[rcx+r10]
	vaddss	xmm0, xmm0, DWORD PTR 24[rdx+r10]
	vmovss	DWORD PTR 24[r8+r10], xmm0
	vzeroupper
.L39:
	ret
	.p2align 4
	.p2align 3
.L12:
	xor	eax, eax
	.p2align 4
	.p2align 3
.L9:
	vmovss	xmm0, DWORD PTR [rcx+rax*4]
	vaddss	xmm0, xmm0, DWORD PTR [rdx+rax*4]
	vmovss	DWORD PTR [r8+rax*4], xmm0
	inc	rax
	cmp	r9, rax
	jne	.L9
	ret
	.p2align 4
	.p2align 3
.L38:
	vzeroupper
	ret
.L13:
	mov	r11, r9
	xor	eax, eax
	jmp	.L4
	.seh_endproc
	.p2align 4
	.globl	_Z10column_dotPKfS0_y
	.def	_Z10column_dotPKfS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10column_dotPKfS0_y
_Z10column_dotPKfS0_y:
.LFB17:
	.seh_endprologue
	mov	r10, rcx
	test	r8, r8
	je	.L49
	lea	rax, -1[r8]
	cmp	rax, 14
	jbe	.L50
	mov	rcx, r8
	xor	eax, eax
	vxorps	xmm0, xmm0, xmm0
	shr	rcx, 4
	sal	rcx, 6
	.p2align 4
	.p2align 3
.L44:
	vmovups	zmm5, ZMMWORD PTR [r10+rax]
	vmulps	zmm1, zmm5, ZMMWORD PTR [rdx+rax]
	add	rax, 64
	vshufps	xmm4, xmm1, xmm1, 85
	vshufps	xmm3, xmm1, xmm1, 255
	vaddss	xmm0, xmm0, xmm1
	valignd	ymm2, ymm1, ymm1, 7
	vaddss	xmm0, xmm0, xmm4
	vunpckhps	xmm4, xmm1, xmm1
	vaddss	xmm0, xmm0, xmm4
	vaddss	xmm0, xmm0, xmm3
	vextractf32x4	xmm3, ymm1, 1
	vaddss	xmm0, xmm0, xmm3
	valignd	ymm3, ymm1, ymm1, 5
	vaddss	xmm0, xmm0, xmm3
	valignd	ymm3, ymm1, ymm1, 6
	vextractf32x8	ymm1, zmm1, 0x1
	vaddss	xmm0, xmm0, xmm3
	vshufps	xmm3, xmm1, xmm1, 85
	vaddss	xmm0, xmm0, xmm2
	vshufps	xmm2, xmm1, xmm1, 255
	vaddss	xmm0, xmm0, xmm1
	vaddss	xmm0, xmm0, xmm3
	vunpckhps	xmm3, xmm1, xmm1
	vaddss	xmm0, xmm0, xmm3
	vaddss	xmm0, xmm0, xmm2
	vextractf32x4	xmm2, ymm1, 1
	vaddss	xmm0, xmm0, xmm2
	valignd	ymm2, ymm1, ymm1, 5
	vaddss	xmm0, xmm0, xmm2
	valignd	ymm2, ymm1, ymm1, 6
	valignd	ymm1, ymm1, ymm1, 7
	vaddss	xmm0, xmm0, xmm2
	vaddss	xmm0, xmm0, xmm1
	cmp	rcx, rax
	jne	.L44
	mov	rax, r8
	and	rax, -16
	test	r8b, 15
	je	.L64
.L43:
	mov	rcx, r8
	sub	rcx, rax
	lea	r9, -1[rcx]
	cmp	r9, 6
	jbe	.L47
	vmovups	ymm5, YMMWORD PTR [r10+rax*4]
	vmulps	ymm1, ymm5, YMMWORD PTR [rdx+rax*4]
	mov	r9, rcx
	and	r9, -8
	add	rax, r9
	and	ecx, 7
	vshufps	xmm3, xmm1, xmm1, 85
	vshufps	xmm2, xmm1, xmm1, 255
	vaddss	xmm0, xmm0, xmm1
	vaddss	xmm0, xmm0, xmm3
	vunpckhps	xmm3, xmm1, xmm1
	vaddss	xmm0, xmm0, xmm3
	vaddss	xmm0, xmm0, xmm2
	vextractf32x4	xmm2, ymm1, 1
	vaddss	xmm0, xmm0, xmm2
	valignd	ymm2, ymm1, ymm1, 5
	vaddss	xmm0, xmm0, xmm2
	valignd	ymm2, ymm1, ymm1, 6
	valignd	ymm1, ymm1, ymm1, 7
	vaddss	xmm0, xmm0, xmm2
	vaddss	xmm0, xmm0, xmm1
	je	.L64
.L47:
	lea	r9, 1[rax]
	vmovss	xmm5, DWORD PTR [r10+rax*4]
	lea	rcx, 0[0+rax*4]
	vfmadd231ss	xmm0, xmm5, DWORD PTR [rdx+rax*4]
	cmp	r9, r8
	jnb	.L64
	lea	r9, 2[rax]
	vmovss	xmm5, DWORD PTR 4[r10+rcx]
	vfmadd231ss	xmm0, xmm5, DWORD PTR 4[rdx+rcx]
	cmp	r9, r8
	jnb	.L64
	lea	r9, 3[rax]
	vmovss	xmm5, DWORD PTR 8[r10+rcx]
	vfmadd231ss	xmm0, xmm5, DWORD PTR 8[rdx+rcx]
	cmp	r9, r8
	jnb	.L64
	lea	r9, 4[rax]
	vmovss	xmm5, DWORD PTR 12[r10+rcx]
	vfmadd231ss	xmm0, xmm5, DWORD PTR 12[rdx+rcx]
	cmp	r9, r8
	jnb	.L64
	lea	r9, 5[rax]
	vmovss	xmm5, DWORD PTR 16[r10+rcx]
	vfmadd231ss	xmm0, xmm5, DWORD PTR 16[rdx+rcx]
	cmp	r9, r8
	jnb	.L64
	add	rax, 6
	vmovss	xmm5, DWORD PTR 20[r10+rcx]
	vfmadd231ss	xmm0, xmm5, DWORD PTR 20[rdx+rcx]
	cmp	rax, r8
	jnb	.L64
	vmovss	xmm5, DWORD PTR 24[r10+rcx]
	vfmadd231ss	xmm0, xmm5, DWORD PTR 24[rdx+rcx]
	vzeroupper
	ret
	.p2align 4
	.p2align 3
.L64:
	vzeroupper
	ret
	.p2align 4
	.p2align 3
.L49:
	vxorps	xmm0, xmm0, xmm0
	ret
.L50:
	xor	eax, eax
	vxorps	xmm0, xmm0, xmm0
	jmp	.L43
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
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
	vmovdqa64	zmm3, ZMMWORD PTR .LC1[rip]
	mov	r8d, 16
	xor	eax, eax
	vpbroadcastq	zmm17, r8
	mov	r8d, 8
	lea	rdx, _ZZ4mainE1A[rip]
	lea	rcx, _ZZ4mainE1B[rip]
	vpbroadcastq	zmm16, r8
	mov	r8d, 1024
	vpbroadcastq	zmm4, r8
	.p2align 4
	.p2align 3
.L66:
	vmovdqa64	zmm0, zmm3
	vpaddq	zmm3, zmm3, zmm17
	vpaddq	zmm1, zmm0, zmm16
	vcvtqq2ps	ymm2, zmm0
	vpsubq	zmm0, zmm4, zmm0
	vcvtqq2ps	ymm5, zmm1
	vpsubq	zmm1, zmm4, zmm1
	vcvtqq2ps	ymm0, zmm0
	vcvtqq2ps	ymm1, zmm1
	vinsertf64x4	zmm2, zmm2, ymm5, 0x1
	vmovaps	ZMMWORD PTR [rdx+rax], zmm2
	vinsertf64x4	zmm0, zmm0, ymm1, 0x1
	vmovaps	ZMMWORD PTR [rcx+rax], zmm0
	add	rax, 64
	cmp	rax, 4096
	jne	.L66
	xor	eax, eax
	lea	r8, _ZZ4mainE1C[rip]
	.p2align 4
	.p2align 3
.L67:
	vmovaps	zmm5, ZMMWORD PTR [rdx+rax]
	vaddps	zmm0, zmm5, ZMMWORD PTR [rcx+rax]
	vmovaps	ZMMWORD PTR [r8+rax], zmm0
	add	rax, 64
	cmp	rax, 4096
	jne	.L67
	xor	eax, eax
	vxorps	xmm0, xmm0, xmm0
	.p2align 4
	.p2align 3
.L68:
	vmovaps	zmm5, ZMMWORD PTR [rcx+rax]
	vmulps	zmm1, zmm5, ZMMWORD PTR [rdx+rax]
	add	rax, 64
	vshufps	xmm4, xmm1, xmm1, 85
	vshufps	xmm3, xmm1, xmm1, 255
	vaddss	xmm0, xmm0, xmm1
	valignd	ymm2, ymm1, ymm1, 7
	vaddss	xmm4, xmm4, xmm0
	vunpckhps	xmm0, xmm1, xmm1
	vaddss	xmm0, xmm0, xmm4
	vaddss	xmm3, xmm3, xmm0
	vextractf32x4	xmm0, ymm1, 1
	vaddss	xmm0, xmm0, xmm3
	valignd	ymm3, ymm1, ymm1, 5
	vaddss	xmm3, xmm3, xmm0
	valignd	ymm0, ymm1, ymm1, 6
	vextractf32x8	ymm1, zmm1, 0x1
	vaddss	xmm0, xmm0, xmm3
	vshufps	xmm3, xmm1, xmm1, 255
	vaddss	xmm2, xmm2, xmm0
	vshufps	xmm0, xmm1, xmm1, 85
	vaddss	xmm2, xmm1, xmm2
	vaddss	xmm0, xmm0, xmm2
	vunpckhps	xmm2, xmm1, xmm1
	vaddss	xmm0, xmm0, xmm2
	vextractf32x4	xmm2, ymm1, 1
	vaddss	xmm0, xmm0, xmm3
	vaddss	xmm0, xmm0, xmm2
	valignd	ymm2, ymm1, ymm1, 5
	vaddss	xmm0, xmm0, xmm2
	valignd	ymm2, ymm1, ymm1, 6
	valignd	ymm1, ymm1, ymm1, 7
	vaddss	xmm0, xmm0, xmm2
	vaddss	xmm0, xmm0, xmm1
	cmp	rax, 4096
	jne	.L68
	vcvttss2si	eax, xmm0
	vzeroupper
	add	rsp, 40
	ret
	.seh_endproc
.lcomm _ZZ4mainE1C,4096,64
.lcomm _ZZ4mainE1B,4096,64
.lcomm _ZZ4mainE1A,4096,64
	.section .rdata,"dr"
	.align 64
.LC1:
	.quad	0
	.quad	1
	.quad	2
	.quad	3
	.quad	4
	.quad	5
	.quad	6
	.quad	7
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
