	.file	"_ch95_for_each.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z14sum_of_squaresRKSt6vectorIiSaIiEE
	.def	_Z14sum_of_squaresRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14sum_of_squaresRKSt6vectorIiSaIiEE
_Z14sum_of_squaresRKSt6vectorIiSaIiEE:
.LFB2661:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]
	mov	rdx, QWORD PTR [rcx]
	xor	ecx, ecx
	cmp	rdx, r8
	je	.L1
	.p2align 4,,10
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
.LFB2663:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rdx, QWORD PTR 8[rcx]
	cmp	rdx, rax
	je	.L7
	.p2align 4,,10
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
.LFB2665:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]
	mov	rcx, QWORD PTR [rcx]
	cmp	rcx, r8
	je	.L15
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L14:
	mov	edx, DWORD PTR [rcx]
	not	edx
	and	edx, 1
	cmp	dl, 1
	sbb	rax, -1
	add	rcx, 4
	cmp	r8, rcx
	jne	.L14
	ret
	.p2align 4,,10
	.p2align 3
.L15:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z5totalRKSt6vectorIiSaIiEE
	.def	_Z5totalRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5totalRKSt6vectorIiSaIiEE
_Z5totalRKSt6vectorIiSaIiEE:
.LFB2669:
	.seh_endprologue
	xor	edx, edx
	mov	r8, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR [rcx]
	cmp	rax, r8
	je	.L19
	.p2align 4,,10
	.p2align 3
.L21:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, r8
	jne	.L21
.L19:
	mov	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z14square_inplaceRSt6vectorIiSaIiEE
	.def	_Z14square_inplaceRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14square_inplaceRSt6vectorIiSaIiEE
_Z14square_inplaceRSt6vectorIiSaIiEE:
.LFB2670:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR [rcx]
	cmp	rax, r8
	je	.L24
	.p2align 4,,10
	.p2align 3
.L26:
	mov	edx, DWORD PTR [rax]
	add	rax, 4
	imul	edx, edx
	mov	DWORD PTR -4[rax], edx
	cmp	rax, r8
	jne	.L26
.L24:
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
