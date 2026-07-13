	.file	"_ch144_rangefor.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8by_indexRKSt6vectorIiSaIiEERl
	.def	_Z8by_indexRKSt6vectorIiSaIiEERl;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8by_indexRKSt6vectorIiSaIiEERl
_Z8by_indexRKSt6vectorIiSaIiEERl:
.LFB1715:
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	r8, QWORD PTR [rcx]
	mov	r9, rax
	sub	r9, r8
	sar	r9, 2
	cmp	rax, r8
	je	.L1
	mov	ecx, DWORD PTR [rdx]
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L3:
	add	ecx, DWORD PTR [r8+rax*4]
	add	rax, 1
	cmp	rax, r9
	jb	.L3
	mov	DWORD PTR [rdx], ecx
.L1:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11by_iteratorRKSt6vectorIiSaIiEERl
	.def	_Z11by_iteratorRKSt6vectorIiSaIiEERl;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11by_iteratorRKSt6vectorIiSaIiEERl
_Z11by_iteratorRKSt6vectorIiSaIiEERl:
.LFB1716:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	r8, QWORD PTR 8[rcx]
	cmp	rax, r8
	je	.L6
	mov	ecx, DWORD PTR [rdx]
	.p2align 4,,10
	.p2align 3
.L8:
	add	ecx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, r8
	jne	.L8
	mov	DWORD PTR [rdx], ecx
.L6:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8by_rangeRKSt6vectorIiSaIiEERl
	.def	_Z8by_rangeRKSt6vectorIiSaIiEERl;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8by_rangeRKSt6vectorIiSaIiEERl
_Z8by_rangeRKSt6vectorIiSaIiEERl:
.LFB1719:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	r8, QWORD PTR 8[rcx]
	cmp	r8, rax
	je	.L10
	mov	ecx, DWORD PTR [rdx]
	.p2align 4,,10
	.p2align 3
.L12:
	add	ecx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, r8
	jne	.L12
	mov	DWORD PTR [rdx], ecx
.L10:
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
