	.file	"_ch127_gvn.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7computei
	.def	_Z7computei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7computei
_Z7computei:
.LFB0:
	.seh_endprologue
	lea	eax, 1[rcx]
	imul	eax, eax
	lea	eax, [rax+rcx*4]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6callerv
	.def	_Z6callerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6callerv
_Z6callerv:
.LFB1:
	.seh_endprologue
	mov	eax, 92
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
