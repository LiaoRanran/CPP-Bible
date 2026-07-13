	.file	"_asm_vcall.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK7Derived3fooEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK7Derived3fooEv
	.def	_ZNK7Derived3fooEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK7Derived3fooEv
_ZNK7Derived3fooEv:
.LFB6:
	.seh_endprologue
	mov	eax, 3
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7DerivedD1Ev
	.def	_ZN7DerivedD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD1Ev
_ZN7DerivedD1Ev:
.LFB18:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7DerivedD0Ev
	.def	_ZN7DerivedD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD0Ev
_ZN7DerivedD0Ev:
.LFB19:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
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
	.def	__main;	.scl	2;	.type	32;	.endef
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
