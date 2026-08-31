	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z9aos_scaleP4Vec3if
	.def	_Z9aos_scaleP4Vec3if;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9aos_scaleP4Vec3if
_Z9aos_scaleP4Vec3if:
.LFB0:
	.seh_endprologue
	movsldup	xmm1, xmm2
	test	edx, edx
	jle	.L1
	movsx	rdx, edx
	lea	rax, [rdx+rdx*2]
	lea	rax, [rcx+rax*4]
	.p2align 4,,10
	.p2align 3
.L3:
	movq	xmm0, QWORD PTR [rcx]
	add	rcx, 12
	mulps	xmm0, xmm1
	movlps	QWORD PTR -12[rcx], xmm0
	movss	xmm0, DWORD PTR -4[rcx]
	mulss	xmm0, xmm2
	movss	DWORD PTR -4[rcx], xmm0
	cmp	rcx, rax
	jne	.L3
.L1:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9soa_scalePfS_S_if
	.def	_Z9soa_scalePfS_S_if;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9soa_scalePfS_S_if
_Z9soa_scalePfS_S_if:
.LFB1:
	.seh_endprologue
	movss	xmm0, DWORD PTR 40[rsp]
	test	r9d, r9d
	jle	.L6
	movsx	r9, r9d
	xor	eax, eax
	sal	r9, 2
	.p2align 4,,10
	.p2align 3
.L8:
	movss	xmm1, DWORD PTR [rcx+rax]
	mulss	xmm1, xmm0
	movss	DWORD PTR [rcx+rax], xmm1
	movss	xmm1, DWORD PTR [rdx+rax]
	mulss	xmm1, xmm0
	movss	DWORD PTR [rdx+rax], xmm1
	movss	xmm1, DWORD PTR [r8+rax]
	mulss	xmm1, xmm0
	movss	DWORD PTR [r8+rax], xmm1
	add	rax, 4
	cmp	r9, rax
	jne	.L8
.L6:
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
