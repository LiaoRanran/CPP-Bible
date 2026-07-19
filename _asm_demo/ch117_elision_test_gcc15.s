	.file	"ch117_elision_test.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12make_prvaluev
	.def	_Z12make_prvaluev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12make_prvaluev
_Z12make_prvaluev:
.LFB33:
	.seh_endprologue
	mov	rax, rcx
	mov	DWORD PTR [rcx], 42
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9make_nrvov
	.def	_Z9make_nrvov;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9make_nrvov
_Z9make_nrvov:
.LFB34:
	.seh_endprologue
	mov	rax, rcx
	mov	DWORD PTR [rcx], 7
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11make_nomovev
	.def	_Z11make_nomovev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11make_nomovev
_Z11make_nomovev:
.LFB35:
	.seh_endprologue
	mov	rax, rcx
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
