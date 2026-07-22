	.file	"_ch117_move_trap.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "move!\12\0"
	.text
	.p2align 4
	.globl	_Z3badv
	.def	_Z3badv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3badv
_Z3badv:
.LFB234:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	mov	rax, rbx
	mov	DWORD PTR [rbx], 1
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z4goodv
	.def	_Z4goodv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4goodv
_Z4goodv:
.LFB235:
	.seh_endprologue
	mov	rax, rcx
	mov	DWORD PTR [rcx], 1
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB236:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	mov	eax, 2
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
