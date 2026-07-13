	.file	"_ch18_opt.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z3addii
	.def	_Z3addii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3addii
_Z3addii:
.LFB0:
	.seh_endprologue
	lea	eax, [rcx+rdx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z4mul3i
	.def	_Z4mul3i;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4mul3i
_Z4mul3i:
.LFB1:
	.seh_endprologue
	lea	eax, [rcx+rcx*2]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6callerv
	.def	_Z6callerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6callerv
_Z6callerv:
.LFB2:
	.seh_endprologue
	mov	eax, 15
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7sum_arrPKii
	.def	_Z7sum_arrPKii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7sum_arrPKii
_Z7sum_arrPKii:
.LFB3:
	.seh_endprologue
	test	edx, edx
	jle	.L8
	movsx	rdx, edx
	xor	eax, eax
	lea	rdx, [rcx+rdx*4]
	.p2align 4,,10
	.p2align 3
.L7:
	add	eax, DWORD PTR [rcx]
	add	rcx, 4
	cmp	rcx, rdx
	jne	.L7
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	xor	eax, eax
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
