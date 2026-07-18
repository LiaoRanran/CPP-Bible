	.file	"_asm_tpl_traits.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10use_traitsv
	.def	_Z10use_traitsv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10use_traitsv
_Z10use_traitsv:
.LFB18:
	sub	rsp, 24
	.seh_stackalloc	24
	.seh_endprologue
	mov	DWORD PTR 12[rsp], 42
	mov	eax, DWORD PTR 12[rsp]
	add	eax, 6
	add	rsp, 24
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
