	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8sum_spanSt4spanIKiLy18446744073709551615EE
	.def	_Z8sum_spanSt4spanIKiLy18446744073709551615EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8sum_spanSt4spanIKiLy18446744073709551615EE
_Z8sum_spanSt4spanIKiLy18446744073709551615EE:
.LFB904:
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR [rcx]
	test	rdx, rdx
	je	.L4
	lea	rcx, [rax+rdx*4]
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L3:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rcx, rax
	jne	.L3
	mov	eax, edx
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	xor	edx, edx
	mov	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7sum_ptrPKiy
	.def	_Z7sum_ptrPKiy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7sum_ptrPKiy
_Z7sum_ptrPKiy:
.LFB906:
	.seh_endprologue
	test	rdx, rdx
	je	.L10
	lea	rdx, [rcx+rdx*4]
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L9:
	add	eax, DWORD PTR [rcx]
	add	rcx, 4
	cmp	rcx, rdx
	jne	.L9
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	xor	eax, eax
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
