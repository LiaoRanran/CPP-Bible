	.file	"_ch95_for_each.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z14sum_of_squaresRKSt6vectorIiSaIiEE
	.def	_Z14sum_of_squaresRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14sum_of_squaresRKSt6vectorIiSaIiEE
_Z14sum_of_squaresRKSt6vectorIiSaIiEE:
.LFB2635:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]
	mov	rdx, QWORD PTR [rcx]
	xor	ecx, ecx
	cmp	rdx, r8
	je	.L1
	.p2align 4
	.p2align 4
	.p2align 3
.L3:
	mov	eax, DWORD PTR [rdx]
	add	rdx, 4
	imul	eax, eax
	add	ecx, eax
	cmp	rdx, r8
	jne	.L3
.L1:
	mov	eax, ecx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8scale_byRSt6vectorIdSaIdEEd
	.def	_Z8scale_byRSt6vectorIdSaIdEEd;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8scale_byRSt6vectorIdSaIdEEd
_Z8scale_byRSt6vectorIdSaIdEEd:
.LFB2637:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rdx, QWORD PTR 8[rcx]
	cmp	rdx, rax
	je	.L7
	.p2align 5
	.p2align 4
	.p2align 3
.L9:
	movsd	xmm0, QWORD PTR [rax]
	add	rax, 8
	mulsd	xmm0, xmm1
	movsd	QWORD PTR -8[rax], xmm0
	cmp	rax, rdx
	jne	.L9
.L7:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10count_evenRKSt6vectorIiSaIiEE
	.def	_Z10count_evenRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10count_evenRKSt6vectorIiSaIiEE
_Z10count_evenRKSt6vectorIiSaIiEE:
.LFB2639:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]
	mov	rcx, QWORD PTR [rcx]
	cmp	rcx, r8
	je	.L14
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L13:
	mov	edx, DWORD PTR [rcx]
	add	rcx, 4
	not	edx
	and	edx, 1
	add	rax, rdx
	cmp	r8, rcx
	jne	.L13
	ret
	.p2align 4,,10
	.p2align 3
.L14:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z5totalRKSt6vectorIiSaIiEE
	.def	_Z5totalRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5totalRKSt6vectorIiSaIiEE
_Z5totalRKSt6vectorIiSaIiEE:
.LFB2643:
	.seh_endprologue
	xor	edx, edx
	mov	rax, rcx
	mov	rcx, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR [rax]
	cmp	rax, rcx
	je	.L16
	.p2align 4
	.p2align 4
	.p2align 3
.L18:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, rcx
	jne	.L18
.L16:
	mov	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z14square_inplaceRSt6vectorIiSaIiEE
	.def	_Z14square_inplaceRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14square_inplaceRSt6vectorIiSaIiEE
_Z14square_inplaceRSt6vectorIiSaIiEE:
.LFB2644:
	.seh_endprologue
	mov	r9, QWORD PTR 8[rcx]
	mov	rdx, QWORD PTR [rcx]
	cmp	rdx, r9
	je	.L21
	lea	r8, -4[r9]
	mov	rax, rdx
	sub	r8, rdx
	cmp	r8, 8
	jbe	.L23
	shr	r8, 2
	add	r8, 1
	mov	rcx, r8
	shr	rcx, 2
	sal	rcx, 4
	add	rcx, rdx
	.p2align 6
	.p2align 4
	.p2align 3
.L24:
	movdqu	xmm0, XMMWORD PTR [rax]
	add	rax, 16
	movdqa	xmm1, xmm0
	pmuludq	xmm1, xmm0
	psrlq	xmm0, 32
	pmuludq	xmm0, xmm0
	pshufd	xmm1, xmm1, 8
	pshufd	xmm0, xmm0, 8
	punpckldq	xmm1, xmm0
	movups	XMMWORD PTR -16[rax], xmm1
	cmp	rax, rcx
	jne	.L24
	test	r8b, 3
	je	.L21
	and	r8, -4
	lea	rdx, [rdx+r8*4]
.L23:
	mov	rax, rdx
.L26:
	mov	edx, DWORD PTR [rax]
	add	rax, 4
	imul	edx, edx
	mov	DWORD PTR -4[rax], edx
	cmp	r9, rax
	jne	.L26
.L21:
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
