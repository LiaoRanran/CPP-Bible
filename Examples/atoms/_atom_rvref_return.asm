	.file	"_atom_rvref_return.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "ret_plain copy=%d move=%d / ret_moved copy=%d move=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB236:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	lea	rcx, .LC0[rip]
	mov	DWORD PTR _ZN5Probe6copiesE[rip], 0
	mov	DWORD PTR _ZN5Probe5movesE[rip], 0
	mov	eax, DWORD PTR _ZN5Probe5movesE[rip]
	add	eax, 1
	mov	DWORD PTR _ZN5Probe5movesE[rip], eax
	mov	edx, DWORD PTR _ZN5Probe6copiesE[rip]
	mov	r8d, DWORD PTR _ZN5Probe5movesE[rip]
	mov	DWORD PTR _ZN5Probe6copiesE[rip], 0
	mov	DWORD PTR _ZN5Probe5movesE[rip], 0
	mov	eax, DWORD PTR _ZN5Probe5movesE[rip]
	add	eax, 1
	mov	DWORD PTR _ZN5Probe5movesE[rip], eax
	mov	r9d, DWORD PTR _ZN5Probe6copiesE[rip]
	mov	eax, DWORD PTR _ZN5Probe5movesE[rip]
	mov	DWORD PTR 32[rsp], eax
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 56
	ret
	.seh_endproc
	.globl	_ZN5Probe5movesE
	.bss
	.align 4
_ZN5Probe5movesE:
	.space 4
	.globl	_ZN5Probe6copiesE
	.align 4
_ZN5Probe6copiesE:
	.space 4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
