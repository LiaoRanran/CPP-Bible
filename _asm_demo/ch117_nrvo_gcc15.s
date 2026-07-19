	.file	"_ch117_nrvo.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7computei
	.def	_Z7computei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7computei
_Z7computei:
.LFB30:
	.seh_endprologue
	mov	rax, rcx
	mov	DWORD PTR [rcx], edx
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB31:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, 7
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
