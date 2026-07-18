	.file	"_asm_vcall.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12call_virtualRK4Base
	.def	_Z12call_virtualRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12call_virtualRK4Base
_Z12call_virtualRK4Base:
.LFB7:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 16[rax]]
	.seh_endproc
	.p2align 4
	.globl	_Z15call_nonvirtualRK4Base
	.def	_Z15call_nonvirtualRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15call_nonvirtualRK4Base
_Z15call_nonvirtualRK4Base:
.LFB8:
	.seh_endprologue
	mov	eax, 2
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB9:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, 5
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
