	.file	"_atom_eval_order.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "g\12\0"
	.text
	.p2align 4
	.globl	_Z1gv
	.def	_Z1gv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1gv
_Z1gv:
.LFB24:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	mov	eax, 1
	add	rsp, 40
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "h\12\0"
	.text
	.p2align 4
	.globl	_Z1hv
	.def	_Z1hv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1hv
_Z1hv:
.LFB25:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	mov	eax, 2
	add	rsp, 40
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "f(%d,%d)\12\0"
	.text
	.p2align 4
	.globl	_Z1fii
	.def	_Z1fii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1fii
_Z1fii:
.LFB26:
	.seh_endprologue
	mov	r8d, edx
	mov	edx, ecx
	lea	rcx, .LC2[rip]
	jmp	__mingw_printf
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB27:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	mov	r8d, 2
	mov	edx, 1
	lea	rcx, .LC2[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
