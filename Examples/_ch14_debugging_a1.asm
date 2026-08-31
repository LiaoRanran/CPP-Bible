	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z9add_debugii
	.def	_Z9add_debugii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9add_debugii
_Z9add_debugii:
.LFB0:
	.seh_endprologue
	lea	eax, [rcx+rdx]
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	DWORD PTR 44[rsp], 5
	mov	eax, DWORD PTR 44[rsp]
	xor	eax, eax
	add	rsp, 56
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
