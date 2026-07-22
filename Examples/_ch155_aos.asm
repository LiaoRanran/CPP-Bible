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
	mov	r8d, edx
	test	edx, edx
	jle	.L1
	lea	eax, -1[rdx]
	cmp	eax, 2
	jbe	.L7
	shr	edx, 2
	movaps	xmm4, xmm2
	mov	rax, rcx
	lea	rdx, [rdx+rdx*2]
	shufps	xmm4, xmm4, 0
	sal	rdx, 4
	add	rdx, rcx
	.p2align 6
	.p2align 4
	.p2align 3
.L4:
	movups	xmm1, XMMWORD PTR 16[rax]
	movups	xmm0, XMMWORD PTR 32[rax]
	add	rax, 48
	movups	xmm3, XMMWORD PTR -48[rax]
	mulps	xmm1, xmm4
	mulps	xmm0, xmm4
	mulps	xmm3, xmm4
	movups	XMMWORD PTR -32[rax], xmm1
	movups	XMMWORD PTR -16[rax], xmm0
	movups	XMMWORD PTR -48[rax], xmm3
	cmp	rax, rdx
	jne	.L4
	mov	edx, r8d
	and	edx, -4
	test	r8b, 3
	je	.L1
.L3:
	movsxd	rdx, edx
	movaps	xmm1, xmm2
	lea	rax, [rdx+rdx*2]
	shufps	xmm1, xmm1, 0xe0
	movq	xmm1, xmm1
	lea	rax, [rcx+rax*4]
.L6:
	movq	xmm0, QWORD PTR [rax]
	add	rdx, 1
	add	rax, 12
	mulps	xmm0, xmm1
	movlps	QWORD PTR -12[rax], xmm0
	movss	xmm0, DWORD PTR -4[rax]
	mulss	xmm0, xmm2
	movss	DWORD PTR -4[rax], xmm0
	cmp	r8d, edx
	jg	.L6
.L1:
	ret
.L7:
	xor	edx, edx
	jmp	.L3
	.seh_endproc
	.p2align 4
	.globl	_Z9soa_scalePfS_S_if
	.def	_Z9soa_scalePfS_S_if;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9soa_scalePfS_S_if
_Z9soa_scalePfS_S_if:
.LFB1:
	.seh_endprologue
	movss	xmm2, DWORD PTR 40[rsp]
	test	r9d, r9d
	jle	.L11
	lea	eax, -1[r9]
	cmp	eax, 2
	jbe	.L17
	mov	r10d, r9d
	movaps	xmm1, xmm2
	xor	eax, eax
	shr	r10d, 2
	shufps	xmm1, xmm1, 0
	sal	r10, 4
	.p2align 6
	.p2align 4
	.p2align 3
.L14:
	movups	xmm0, XMMWORD PTR [rcx+rax]
	mulps	xmm0, xmm1
	movups	XMMWORD PTR [rcx+rax], xmm0
	movups	xmm0, XMMWORD PTR [rdx+rax]
	mulps	xmm0, xmm1
	movups	XMMWORD PTR [rdx+rax], xmm0
	movups	xmm0, XMMWORD PTR [r8+rax]
	mulps	xmm0, xmm1
	movups	XMMWORD PTR [r8+rax], xmm0
	add	rax, 16
	cmp	rax, r10
	jne	.L14
	mov	eax, r9d
	and	eax, -4
	test	r9b, 3
	je	.L11
.L13:
	cdqe
.L16:
	movss	xmm0, DWORD PTR [rcx+rax*4]
	mulss	xmm0, xmm2
	movss	DWORD PTR [rcx+rax*4], xmm0
	movss	xmm0, DWORD PTR [rdx+rax*4]
	mulss	xmm0, xmm2
	movss	DWORD PTR [rdx+rax*4], xmm0
	movss	xmm0, DWORD PTR [r8+rax*4]
	mulss	xmm0, xmm2
	movss	DWORD PTR [r8+rax*4], xmm0
	add	rax, 1
	cmp	r9d, eax
	jg	.L16
.L11:
	ret
.L17:
	xor	eax, eax
	jmp	.L13
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
