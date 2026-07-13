	.file	"_asm_tpl_variadic.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z9print_allv
	.def	_Z9print_allv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9print_allv
_Z9print_allv:
.LFB16:
	.seh_endprologue
	mov	eax, DWORD PTR g_depth[rip]
	add	eax, 1
	mov	DWORD PTR g_depth[rip], eax
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB19:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	eax, DWORD PTR g_depth[rip]
	add	eax, 1
	mov	DWORD PTR g_depth[rip], eax
	mov	eax, DWORD PTR g_depth[rip]
	add	eax, 1
	mov	DWORD PTR g_depth[rip], eax
	mov	eax, DWORD PTR g_depth[rip]
	add	eax, 1
	mov	DWORD PTR g_depth[rip], eax
	mov	eax, DWORD PTR g_depth[rip]
	add	eax, 1
	mov	DWORD PTR g_depth[rip], eax
	mov	DWORD PTR 44[rsp], 10
	mov	eax, DWORD PTR 44[rsp]
	mov	edx, DWORD PTR g_depth[rip]
	add	eax, edx
	add	rsp, 56
	ret
	.seh_endproc
	.globl	g_depth
	.bss
	.align 4
g_depth:
	.space 4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
