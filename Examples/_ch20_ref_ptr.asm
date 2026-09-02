	.file	"_ch20_ref_ptr.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6by_refRi
	.def	_Z6by_refRi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6by_refRi
_Z6by_refRi:
.LFB0:
	.seh_endprologue
	add	DWORD PTR [rcx], 1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6by_ptrPi
	.def	_Z6by_ptrPi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6by_ptrPi
_Z6by_ptrPi:
.LFB1:
	.seh_endprologue
	test	rcx, rcx
	je	.L3
	add	DWORD PTR [rcx], 1
.L3:
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
