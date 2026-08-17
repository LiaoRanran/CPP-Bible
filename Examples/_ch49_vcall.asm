	.file	"_ch49_vcall.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8call_fooP4Base
	.def	_Z8call_fooP4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8call_fooP4Base
_Z8call_fooP4Base:
.LFB2:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR [rax]]
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
