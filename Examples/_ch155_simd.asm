	.file	"_ch155_simd.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10add_arraysPfS_S_i
	.def	_Z10add_arraysPfS_S_i;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10add_arraysPfS_S_i
_Z10add_arraysPfS_S_i:
.LFB0:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	test	r9d, r9d
	jle	.L14
	lea	eax, -1[r9]
	cmp	eax, 6
	jbe	.L8
	mov	r10d, r9d
	xor	eax, eax
	shr	r10d, 3
	sal	r10, 5
	.p2align 4,,10
	.p2align 3
.L4:
	vmovups	ymm1, YMMWORD PTR [rcx+rax]
	vaddps	ymm0, ymm1, YMMWORD PTR [rdx+rax]
	vmovups	YMMWORD PTR [r8+rax], ymm0
	add	rax, 32
	cmp	r10, rax
	jne	.L4
	mov	r10d, r9d
	and	r10d, -8
	cmp	r9d, r10d
	mov	eax, r10d
	je	.L16
	vzeroupper
.L3:
	mov	r11d, r9d
	sub	r11d, eax
	lea	ebx, -1[r11]
	cmp	ebx, 2
	jbe	.L6
	vmovups	xmm2, XMMWORD PTR [rcx+rax*4]
	vaddps	xmm0, xmm2, XMMWORD PTR [rdx+rax*4]
	vmovups	XMMWORD PTR [r8+rax*4], xmm0
	mov	eax, r11d
	and	eax, -4
	add	r10d, eax
	and	r11d, 3
	je	.L14
.L6:
	movsx	r11, r10d
	vmovss	xmm0, DWORD PTR [rcx+r11*4]
	lea	rax, 0[0+r11*4]
	vaddss	xmm0, xmm0, DWORD PTR [rdx+r11*4]
	vmovss	DWORD PTR [r8+r11*4], xmm0
	lea	r11d, 1[r10]
	cmp	r9d, r11d
	jle	.L14
	vmovss	xmm0, DWORD PTR 4[rcx+rax]
	add	r10d, 2
	vaddss	xmm0, xmm0, DWORD PTR 4[rdx+rax]
	cmp	r9d, r10d
	vmovss	DWORD PTR 4[r8+rax], xmm0
	jle	.L14
	vmovss	xmm0, DWORD PTR 8[rcx+rax]
	vaddss	xmm0, xmm0, DWORD PTR 8[rdx+rax]
	vmovss	DWORD PTR 8[r8+rax], xmm0
.L14:
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L16:
	vzeroupper
	pop	rbx
	ret
.L8:
	xor	eax, eax
	xor	r10d, r10d
	jmp	.L3
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
