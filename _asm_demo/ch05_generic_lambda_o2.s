	.file	"ch05_generic_lambda.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7twice_ii
	.def	_Z7twice_ii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7twice_ii
_Z7twice_ii:
.LFB0:
	.seh_endprologue
	lea	eax, [rcx+rcx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11use_genericv
	.def	_Z11use_genericv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11use_genericv
_Z11use_genericv:
.LFB1:
	.seh_endprologue
	mov	eax, 19
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB9:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, 19
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
