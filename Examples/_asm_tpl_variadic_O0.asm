	.file	"_asm_tpl_variadic.cpp"
	.intel_syntax noprefix
	.text
	.globl	g_depth
	.bss
	.align 4
g_depth:
	.space 4
	.text
	.globl	_Z9print_allv
	.def	_Z9print_allv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9print_allv
_Z9print_allv:
.LFB16:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	eax, DWORD PTR g_depth[rip]
	add	eax, 1
	mov	DWORD PTR g_depth[rip], eax
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z8fold_sumIJiiiiEEDaDpT_,"x"
	.linkonce discard
	.globl	_Z8fold_sumIJiiiiEEDaDpT_
	.def	_Z8fold_sumIJiiiiEEDaDpT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8fold_sumIJiiiiEEDaDpT_
_Z8fold_sumIJiiiiEEDaDpT_:
.LFB20:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	mov	DWORD PTR 32[rbp], r8d
	mov	DWORD PTR 40[rbp], r9d
	mov	edx, DWORD PTR 16[rbp]
	mov	eax, DWORD PTR 24[rbp]
	add	edx, eax
	mov	eax, DWORD PTR 32[rbp]
	add	edx, eax
	mov	eax, DWORD PTR 40[rbp]
	add	eax, edx
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB19:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	call	__main
	movsd	xmm0, QWORD PTR .LC0[rip]
	mov	r8d, 99
	movapd	xmm1, xmm0
	mov	ecx, 1
	call	_Z9print_allIiJdcEEvT_DpT0_
	mov	r9d, 4
	mov	r8d, 3
	mov	edx, 2
	mov	ecx, 1
	call	_Z8fold_sumIJiiiiEEDaDpT_
	mov	DWORD PTR -4[rbp], eax
	mov	edx, DWORD PTR -4[rbp]
	mov	eax, DWORD PTR g_depth[rip]
	add	eax, edx
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z9print_allIiJdcEEvT_DpT0_,"x"
	.linkonce discard
	.globl	_Z9print_allIiJdcEEvT_DpT0_
	.def	_Z9print_allIiJdcEEvT_DpT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9print_allIiJdcEEvT_DpT0_
_Z9print_allIiJdcEEvT_DpT0_:
.LFB21:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	movsd	QWORD PTR 24[rbp], xmm1
	mov	eax, r8d
	mov	BYTE PTR 32[rbp], al
	mov	eax, DWORD PTR g_depth[rip]
	add	eax, 1
	mov	DWORD PTR g_depth[rip], eax
	movsx	edx, BYTE PTR 32[rbp]
	mov	rax, QWORD PTR 24[rbp]
	movq	xmm0, rax
	call	_Z9print_allIdJcEEvT_DpT0_
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z9print_allIdJcEEvT_DpT0_,"x"
	.linkonce discard
	.globl	_Z9print_allIdJcEEvT_DpT0_
	.def	_Z9print_allIdJcEEvT_DpT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9print_allIdJcEEvT_DpT0_
_Z9print_allIdJcEEvT_DpT0_:
.LFB22:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	movsd	QWORD PTR 16[rbp], xmm0
	mov	eax, edx
	mov	BYTE PTR 24[rbp], al
	mov	eax, DWORD PTR g_depth[rip]
	add	eax, 1
	mov	DWORD PTR g_depth[rip], eax
	movsx	eax, BYTE PTR 24[rbp]
	mov	ecx, eax
	call	_Z9print_allIcJEEvT_DpT0_
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z9print_allIcJEEvT_DpT0_,"x"
	.linkonce discard
	.globl	_Z9print_allIcJEEvT_DpT0_
	.def	_Z9print_allIcJEEvT_DpT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9print_allIcJEEvT_DpT0_
_Z9print_allIcJEEvT_DpT0_:
.LFB23:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	eax, ecx
	mov	BYTE PTR 16[rbp], al
	mov	eax, DWORD PTR g_depth[rip]
	add	eax, 1
	mov	DWORD PTR g_depth[rip], eax
	call	_Z9print_allv
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1073741824
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
