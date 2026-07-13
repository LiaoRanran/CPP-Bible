	.file	"_ch144_rangefor.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z9sum_rangeRKSt6vectorIiSaIiEE
	.def	_Z9sum_rangeRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9sum_rangeRKSt6vectorIiSaIiEE
_Z9sum_rangeRKSt6vectorIiSaIiEE:
.LFB1715:
	.seh_endprologue
	xor	edx, edx
	mov	rax, QWORD PTR [rcx]
	mov	rcx, QWORD PTR 8[rcx]
	cmp	rcx, rax
	je	.L1
	.p2align 4,,10
	.p2align 3
.L3:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, rcx
	jne	.L3
.L1:
	mov	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8sum_iterRKSt6vectorIiSaIiEE
	.def	_Z8sum_iterRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8sum_iterRKSt6vectorIiSaIiEE
_Z8sum_iterRKSt6vectorIiSaIiEE:
.LFB1720:
	.seh_endprologue
	xor	edx, edx
	mov	rax, QWORD PTR [rcx]
	mov	rcx, QWORD PTR 8[rcx]
	cmp	rax, rcx
	je	.L7
	.p2align 4,,10
	.p2align 3
.L9:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rcx, rax
	jne	.L9
.L7:
	mov	eax, edx
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
