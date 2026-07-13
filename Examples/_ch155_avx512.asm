	.file	"_ch155_avx512.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z13add_arrays512PfS_S_i
	.def	_Z13add_arrays512PfS_S_i;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13add_arrays512PfS_S_i
_Z13add_arrays512PfS_S_i:
.LFB0:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	test	r9d, r9d
	jle	.L20
	lea	eax, -1[r9]
	cmp	eax, 14
	jbe	.L8
	mov	r10d, r9d
	xor	eax, eax
	shr	r10d, 4
	sal	r10, 6
	.p2align 4,,10
	.p2align 3
.L4:
	vmovups	zmm1, ZMMWORD PTR [rcx+rax]
	vaddps	zmm0, zmm1, ZMMWORD PTR [rdx+rax]
	vmovups	ZMMWORD PTR [r8+rax], zmm0
	add	rax, 64
	cmp	r10, rax
	jne	.L4
	mov	eax, r9d
	and	eax, -16
	cmp	r9d, eax
	mov	r10d, eax
	je	.L19
.L3:
	mov	r11d, r9d
	sub	r11d, r10d
	lea	ebx, -1[r11]
	cmp	ebx, 6
	jbe	.L6
	vmovups	ymm2, YMMWORD PTR [rcx+r10*4]
	vaddps	ymm0, ymm2, YMMWORD PTR [rdx+r10*4]
	vmovups	YMMWORD PTR [r8+r10*4], ymm0
	mov	r10d, r11d
	and	r10d, -8
	add	eax, r10d
	and	r11d, 7
	je	.L19
.L6:
	movsx	r11, eax
	vmovss	xmm0, DWORD PTR [rcx+r11*4]
	lea	r10, 0[0+r11*4]
	vaddss	xmm0, xmm0, DWORD PTR [rdx+r11*4]
	vmovss	DWORD PTR [r8+r11*4], xmm0
	lea	r11d, 1[rax]
	cmp	r9d, r11d
	jle	.L19
	vmovss	xmm0, DWORD PTR 4[rdx+r10]
	lea	r11d, 2[rax]
	vaddss	xmm0, xmm0, DWORD PTR 4[rcx+r10]
	cmp	r9d, r11d
	vmovss	DWORD PTR 4[r8+r10], xmm0
	jle	.L19
	vmovss	xmm0, DWORD PTR 8[rcx+r10]
	lea	r11d, 3[rax]
	vaddss	xmm0, xmm0, DWORD PTR 8[rdx+r10]
	cmp	r9d, r11d
	vmovss	DWORD PTR 8[r8+r10], xmm0
	jle	.L19
	vmovss	xmm0, DWORD PTR 12[rcx+r10]
	lea	r11d, 4[rax]
	vaddss	xmm0, xmm0, DWORD PTR 12[rdx+r10]
	cmp	r9d, r11d
	vmovss	DWORD PTR 12[r8+r10], xmm0
	jle	.L19
	vmovss	xmm0, DWORD PTR 16[rcx+r10]
	lea	r11d, 5[rax]
	vaddss	xmm0, xmm0, DWORD PTR 16[rdx+r10]
	cmp	r9d, r11d
	vmovss	DWORD PTR 16[r8+r10], xmm0
	jle	.L19
	vmovss	xmm0, DWORD PTR 20[rcx+r10]
	add	eax, 6
	vaddss	xmm0, xmm0, DWORD PTR 20[rdx+r10]
	cmp	r9d, eax
	vmovss	DWORD PTR 20[r8+r10], xmm0
	jle	.L19
	vmovss	xmm0, DWORD PTR 24[rcx+r10]
	vaddss	xmm0, xmm0, DWORD PTR 24[rdx+r10]
	vmovss	DWORD PTR 24[r8+r10], xmm0
	vzeroupper
.L20:
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	vzeroupper
	pop	rbx
	ret
.L8:
	xor	r10d, r10d
	xor	eax, eax
	jmp	.L3
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
