	.file	"ch88_optional_test.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7get_optSt8optionalIiE
	.def	_Z7get_optSt8optionalIiE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7get_optSt8optionalIiE
_Z7get_optSt8optionalIiE:
.LFB392:
	.seh_endprologue
	mov	rax, rcx
	mov	QWORD PTR 8[rsp], rcx
	shr	rax, 32
	test	al, al
	je	.L3
	mov	eax, DWORD PTR 8[rsp]
	ret
	.p2align 4,,10
	.p2align 3
.L3:
	mov	eax, -1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7get_rawPKi
	.def	_Z7get_rawPKi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7get_rawPKi
_Z7get_rawPKi:
.LFB398:
	.seh_endprologue
	test	rcx, rcx
	je	.L7
	mov	eax, DWORD PTR [rcx]
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	mov	eax, -1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7opt_useSt8optionalIiE
	.def	_Z7opt_useSt8optionalIiE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7opt_useSt8optionalIiE
_Z7opt_useSt8optionalIiE:
.LFB399:
	.seh_endprologue
	mov	rax, rcx
	shr	rax, 32
	movzx	eax, al
	add	eax, ecx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10emit_sizesv
	.def	_Z10emit_sizesv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10emit_sizesv
_Z10emit_sizesv:
.LFB401:
	.seh_endprologue
	mov	DWORD PTR g_obs[rip], 8
	mov	DWORD PTR g_obs[rip], 4
	mov	DWORD PTR g_obs[rip], 16
	mov	DWORD PTR g_obs[rip], 2
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB404:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, 42
	mov	DWORD PTR g_obs[rip], 8
	mov	DWORD PTR g_obs[rip], 4
	mov	DWORD PTR g_obs[rip], 16
	mov	DWORD PTR g_obs[rip], 2
	add	rsp, 40
	ret
	.seh_endproc
	.globl	g_obs
	.bss
	.align 4
g_obs:
	.space 4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
