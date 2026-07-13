	.file	"_ch107_mangled.cpp"
	.intel_syntax noprefix
	.text
	.globl	g
	.bss
	.align 4
g:
	.space 4
	.text
	.globl	_Z7add_onev
	.def	_Z7add_onev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7add_onev
_Z7add_onev:
.LFB661:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	DWORD PTR -4[rbp], 1
	mov	DWORD PTR -8[rbp], 0
	mov	edx, DWORD PTR -4[rbp]
	lea	rax, g[rip]
	lock xadd	DWORD PTR [rax], edx
	nop
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
