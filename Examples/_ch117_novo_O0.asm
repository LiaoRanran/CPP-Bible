	.file	"_ch117_novo.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN3BigC1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN3BigC1Ev
	.def	_ZN3BigC1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3BigC1Ev
_ZN3BigC1Ev:
.LFB23:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR [rax], 1
	nop
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "copy ctor!\12\0"
	.section	.text$_ZN3BigC1ERKS_,"x"
	.linkonce discard
	.align 2
	.globl	_ZN3BigC1ERKS_
	.def	_ZN3BigC1ERKS_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3BigC1ERKS_
_ZN3BigC1ERKS_:
.LFB26:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	lea	rax, .LC0[rip]
	mov	rcx, rax
	call	__mingw_printf
	mov	rax, QWORD PTR 24[rbp]
	mov	edx, DWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR [rax], edx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z9make_copyv
	.def	_Z9make_copyv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9make_copyv
_Z9make_copyv:
.LFB27:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZN3BigC1Ev
	lea	rdx, -32[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN3BigC1ERKS_
	nop
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z11make_forcedRK3Big
	.def	_Z11make_forcedRK3Big;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11make_forcedRK3Big
_Z11make_forcedRK3Big:
.LFB28:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN3BigC1ERKS_
	nop
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB29:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 96
	.seh_stackalloc	96
	.seh_endprologue
	call	__main
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZN3BigC1Ev
	lea	rax, -64[rbp]
	lea	rdx, -32[rbp]
	mov	rcx, rax
	call	_Z11make_forcedRK3Big
	mov	eax, DWORD PTR -64[rbp]
	add	rsp, 96
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
