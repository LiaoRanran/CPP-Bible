	.file	"_ch155_aos.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z9aos_scaleP4Vec3if
	.def	_Z9aos_scaleP4Vec3if;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9aos_scaleP4Vec3if
_Z9aos_scaleP4Vec3if:
.LFB0:
	.seh_endprologue
	test	edx, edx
	mov	r9, rcx
	jle	.L14
	lea	eax, -1[rdx]
	cmp	eax, 6
	jbe	.L8
	mov	rax, rcx
	mov	ecx, edx
	vbroadcastss	ymm0, xmm2
	shr	ecx, 3
	lea	rcx, [rcx+rcx*2]
	sal	rcx, 5
	add	rcx, r9
	.p2align 4,,10
	.p2align 3
.L4:
	vmulps	ymm3, ymm0, YMMWORD PTR 32[rax]
	vmulps	ymm1, ymm0, YMMWORD PTR 64[rax]
	vmulps	ymm4, ymm0, YMMWORD PTR [rax]
	vmovups	YMMWORD PTR 32[rax], ymm3
	vmovups	YMMWORD PTR [rax], ymm4
	add	rax, 96
	vmovups	YMMWORD PTR -32[rax], ymm1
	cmp	rcx, rax
	jne	.L4
	mov	r8d, edx
	and	r8d, -8
	cmp	edx, r8d
	mov	ecx, r8d
	je	.L16
	vzeroupper
.L3:
	mov	r10d, edx
	sub	r10d, ecx
	lea	eax, -1[r10]
	cmp	eax, 2
	jbe	.L6
	lea	rax, [rcx+rcx*2]
	vshufps	xmm0, xmm2, xmm2, 0
	lea	rax, [r9+rax*4]
	vmulps	xmm3, xmm0, XMMWORD PTR 16[rax]
	vmulps	xmm1, xmm0, XMMWORD PTR 32[rax]
	vmulps	xmm0, xmm0, XMMWORD PTR [rax]
	vmovups	XMMWORD PTR 16[rax], xmm3
	vmovups	XMMWORD PTR 32[rax], xmm1
	vmovups	XMMWORD PTR [rax], xmm0
	mov	eax, r10d
	and	eax, -4
	add	r8d, eax
	and	r10d, 3
	je	.L14
.L6:
	vmovsldup	xmm1, xmm2
	movsx	rax, r8d
	lea	rcx, [rax+rax*2]
	sal	rcx, 2
	lea	rax, [r9+rcx]
	vmovq	xmm0, QWORD PTR [rax]
	vmulps	xmm0, xmm0, xmm1
	vmovlps	QWORD PTR [rax], xmm0
	vmulss	xmm0, xmm2, DWORD PTR 8[rax]
	vmovss	DWORD PTR 8[rax], xmm0
	lea	eax, 1[r8]
	cmp	eax, edx
	jge	.L14
	lea	rax, 12[r9+rcx]
	vmovq	xmm0, QWORD PTR [rax]
	vmulps	xmm0, xmm0, xmm1
	vmovlps	QWORD PTR [rax], xmm0
	vmulss	xmm0, xmm2, DWORD PTR 8[rax]
	vmovss	DWORD PTR 8[rax], xmm0
	lea	eax, 2[r8]
	cmp	edx, eax
	jle	.L14
	lea	rax, 24[r9+rcx]
	vmovq	xmm0, QWORD PTR [rax]
	vmulss	xmm2, xmm2, DWORD PTR 8[rax]
	vmulps	xmm0, xmm0, xmm1
	vmovss	DWORD PTR 8[rax], xmm2
	vmovlps	QWORD PTR [rax], xmm0
.L14:
	ret
	.p2align 4,,10
	.p2align 3
.L16:
	vzeroupper
	ret
.L8:
	xor	ecx, ecx
	xor	r8d, r8d
	jmp	.L3
	.seh_endproc
	.p2align 4
	.globl	_Z9soa_scalePfS_S_if
	.def	_Z9soa_scalePfS_S_if;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9soa_scalePfS_S_if
_Z9soa_scalePfS_S_if:
.LFB1:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	vmovss	xmm2, DWORD PTR 56[rsp]
	test	r9d, r9d
	jle	.L30
	lea	eax, -1[r9]
	cmp	eax, 6
	jbe	.L24
	mov	r10d, r9d
	vbroadcastss	ymm0, xmm2
	xor	eax, eax
	shr	r10d, 3
	sal	r10, 5
	.p2align 4,,10
	.p2align 3
.L20:
	vmulps	ymm1, ymm0, YMMWORD PTR [rcx+rax]
	vmovups	YMMWORD PTR [rcx+rax], ymm1
	vmulps	ymm1, ymm0, YMMWORD PTR [rdx+rax]
	vmovups	YMMWORD PTR [rdx+rax], ymm1
	vmulps	ymm1, ymm0, YMMWORD PTR [r8+rax]
	vmovups	YMMWORD PTR [r8+rax], ymm1
	add	rax, 32
	cmp	rax, r10
	jne	.L20
	mov	r10d, r9d
	and	r10d, -8
	cmp	r9d, r10d
	mov	eax, r10d
	je	.L31
	vzeroupper
.L19:
	mov	r11d, r9d
	sub	r11d, eax
	lea	ebx, -1[r11]
	cmp	ebx, 2
	jbe	.L22
	sal	rax, 2
	vshufps	xmm0, xmm2, xmm2, 0
	lea	rsi, [rcx+rax]
	vmulps	xmm1, xmm0, XMMWORD PTR [rsi]
	lea	rbx, [rdx+rax]
	add	rax, r8
	vmovups	XMMWORD PTR [rsi], xmm1
	vmulps	xmm1, xmm0, XMMWORD PTR [rbx]
	vmulps	xmm0, xmm0, XMMWORD PTR [rax]
	vmovups	XMMWORD PTR [rbx], xmm1
	vmovups	XMMWORD PTR [rax], xmm0
	mov	eax, r11d
	and	eax, -4
	add	r10d, eax
	and	r11d, 3
	je	.L30
.L22:
	movsx	rax, r10d
	sal	rax, 2
	lea	r11, [rcx+rax]
	vmulss	xmm0, xmm2, DWORD PTR [r11]
	vmovss	DWORD PTR [r11], xmm0
	lea	r11, [rdx+rax]
	vmulss	xmm0, xmm2, DWORD PTR [r11]
	vmovss	DWORD PTR [r11], xmm0
	lea	r11, [r8+rax]
	vmulss	xmm0, xmm2, DWORD PTR [r11]
	vmovss	DWORD PTR [r11], xmm0
	lea	r11d, 1[r10]
	cmp	r9d, r11d
	jle	.L30
	lea	r11, 4[rax]
	add	r10d, 2
	lea	rbx, [rcx+r11]
	vmulss	xmm0, xmm2, DWORD PTR [rbx]
	vmovss	DWORD PTR [rbx], xmm0
	lea	rbx, [rdx+r11]
	add	r11, r8
	cmp	r9d, r10d
	vmulss	xmm0, xmm2, DWORD PTR [rbx]
	vmovss	DWORD PTR [rbx], xmm0
	vmulss	xmm0, xmm2, DWORD PTR [r11]
	vmovss	DWORD PTR [r11], xmm0
	jle	.L30
	add	rax, 8
	add	rcx, rax
	add	rdx, rax
	add	r8, rax
	vmulss	xmm0, xmm2, DWORD PTR [rcx]
	vmovss	DWORD PTR [rcx], xmm0
	vmulss	xmm0, xmm2, DWORD PTR [rdx]
	vmulss	xmm2, xmm2, DWORD PTR [r8]
	vmovss	DWORD PTR [rdx], xmm0
	vmovss	DWORD PTR [r8], xmm2
.L30:
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L31:
	vzeroupper
	pop	rbx
	pop	rsi
	ret
.L24:
	xor	eax, eax
	xor	r10d, r10d
	jmp	.L19
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
