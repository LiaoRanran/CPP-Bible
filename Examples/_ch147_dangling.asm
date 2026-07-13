	.file	"_ch147_dangling.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z3badB5cxx11v
	.def	_Z3badB5cxx11v;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3badB5cxx11v
_Z3badB5cxx11v:
.LFB1951:
	.seh_endprologue
	xor	eax, eax
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2000:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
