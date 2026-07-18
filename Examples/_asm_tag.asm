	.file	"_asm_tag.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7use_tagv
	.def	_Z7use_tagv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7use_tagv
_Z7use_tagv:
.LFB2369:
	.seh_endprologue
	mov	eax, DWORD PTR g_count[rip]
	lea	edx, 101[rax]
	mov	eax, DWORD PTR g_step[rip]
	mov	DWORD PTR g_count[rip], edx
	add	eax, 1
	mov	DWORD PTR g_step[rip], eax
	add	eax, edx
	ret
	.seh_endproc
	.globl	g_step
	.bss
	.align 4
g_step:
	.space 4
	.globl	g_count
	.align 4
g_count:
	.space 4
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
