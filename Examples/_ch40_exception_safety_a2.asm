	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "div by zero\0"
	.section	.text.unlikely,"x"
	.def	_Z13may_throw_divii.part.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z13may_throw_divii.part.0
_Z13may_throw_divii.part.0:
.LFB4:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 8
	call	__cxa_allocate_exception
	mov	rdx, QWORD PTR .refptr._ZTIPKc[rip]
	xor	r8d, r8d
	mov	rcx, rax
	lea	rax, .LC0[rip]
	mov	QWORD PTR [rcx], rax
	call	__cxa_throw
	nop
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z13may_throw_divii
	.def	_Z13may_throw_divii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13may_throw_divii
_Z13may_throw_divii:
.LFB0:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	test	edx, edx
	mov	eax, ecx
	mov	ecx, edx
	je	.L5
	cdq
	idiv	ecx
	add	rsp, 40
	ret
.L5:
	call	_Z13may_throw_divii.part.0
	nop
	.seh_endproc
	.p2align 4
	.globl	_Z12noexcept_addii
	.def	_Z12noexcept_addii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12noexcept_addii
_Z12noexcept_addii:
.LFB1:
	.seh_endprologue
	lea	eax, [rcx+rdx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z14call_may_throwii
	.def	_Z14call_may_throwii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14call_may_throwii
_Z14call_may_throwii:
.LFB6:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	test	edx, edx
	mov	eax, ecx
	mov	ecx, edx
	je	.L9
	cdq
	idiv	ecx
	add	rsp, 40
	ret
.L9:
	call	_Z13may_throw_divii.part.0
	nop
	.seh_endproc
	.p2align 4
	.globl	_Z13call_noexceptii
	.def	_Z13call_noexceptii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13call_noexceptii
_Z13call_noexceptii:
.LFB8:
	.seh_endprologue
	lea	eax, [rcx+rdx]
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZTIPKc, "dr"
	.globl	.refptr._ZTIPKc
	.linkonce	discard
.refptr._ZTIPKc:
	.quad	_ZTIPKc
