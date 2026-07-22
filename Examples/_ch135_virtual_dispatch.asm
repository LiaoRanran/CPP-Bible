	.file	"_ch135_virtual_dispatch.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK3Dog5speakEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK3Dog5speakEv
	.def	_ZNK3Dog5speakEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK3Dog5speakEv
_ZNK3Dog5speakEv:
.LFB24:
	.seh_endprologue
	mov	eax, 42
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z6directRK3Dog
	.def	_Z6directRK3Dog;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6directRK3Dog
_Z6directRK3Dog:
.LFB25:
	.seh_endprologue
	lea	rdx, _ZNK3Dog5speakEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR 16[rax]
	cmp	rax, rdx
	jne	.L5
	mov	eax, 42
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	rex.W jmp	rax
	.seh_endproc
	.p2align 4
	.globl	_Z11via_virtualRK6Animal
	.def	_Z11via_virtualRK6Animal;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11via_virtualRK6Animal
_Z11via_virtualRK6Animal:
.LFB26:
	.seh_endprologue
	lea	rdx, _ZNK3Dog5speakEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR 16[rax]
	cmp	rax, rdx
	jne	.L8
	mov	eax, 42
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	rex.W jmp	rax
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB27:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	DWORD PTR 44[rsp], 84
	mov	eax, DWORD PTR 44[rsp]
	xor	eax, eax
	add	rsp, 56
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
