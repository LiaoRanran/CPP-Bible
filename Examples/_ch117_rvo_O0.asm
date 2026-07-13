	.file	"_ch117_rvo.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN3BigC1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN3BigC1Ev
	.def	_ZN3BigC1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3BigC1Ev
_ZN3BigC1Ev:
.LFB49:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR [rax], -889275714
	nop
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z4makev
	.def	_Z4makev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4makev
_Z4makev:
.LFB53:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN3BigC1Ev
	nop
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB54:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	call	__main
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_Z4makev
	mov	eax, DWORD PTR -32[rbp]
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
