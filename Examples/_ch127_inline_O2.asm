	.file	"_ch127_inline.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12add_noinlineii
	.def	_Z12add_noinlineii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12add_noinlineii
_Z12add_noinlineii:
.LFB24:
	.seh_endprologue
	lea	eax, [rcx+rdx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11use_inlinedv
	.def	_Z11use_inlinedv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11use_inlinedv
_Z11use_inlinedv:
.LFB26:
	.seh_endprologue
	mov	eax, 10
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12use_noinlinev
	.def	_Z12use_noinlinev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12use_noinlinev
_Z12use_noinlinev:
.LFB27:
	.seh_endprologue
	mov	edx, 4
	mov	ecx, 3
	jmp	_Z12add_noinlineii
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "%d %d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB28:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	edx, 4
	mov	ecx, 3
	call	_Z12add_noinlineii
	mov	edx, 10
	lea	rcx, .LC0[rip]
	mov	r8d, eax
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
