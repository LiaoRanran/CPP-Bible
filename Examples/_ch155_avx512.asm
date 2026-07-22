	.file	"_ch155_avx512.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z13add_arrays512PfS_S_i
	.def	_Z13add_arrays512PfS_S_i;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13add_arrays512PfS_S_i
_Z13add_arrays512PfS_S_i:
.LFB0:
	.seh_endprologue
	test	r9d, r9d
	jle	.L1
	lea	eax, -1[r9]
	cmp	eax, 2
	jbe	.L7
	mov	r10d, r9d
	xor	eax, eax
	shr	r10d, 2
	sal	r10, 4
	.p2align 5
	.p2align 4
	.p2align 3
.L4:
	movups	xmm0, XMMWORD PTR [rcx+rax]
	movups	xmm1, XMMWORD PTR [rdx+rax]
	addps	xmm0, xmm1
	movups	XMMWORD PTR [r8+rax], xmm0
	add	rax, 16
	cmp	rax, r10
	jne	.L4
	mov	eax, r9d
	and	eax, -4
	test	r9b, 3
	je	.L1
.L3:
	cdqe
.L6:
	movss	xmm0, DWORD PTR [rcx+rax*4]
	addss	xmm0, DWORD PTR [rdx+rax*4]
	movss	DWORD PTR [r8+rax*4], xmm0
	add	rax, 1
	cmp	r9d, eax
	jg	.L6
.L1:
	ret
.L7:
	xor	eax, eax
	jmp	.L3
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
