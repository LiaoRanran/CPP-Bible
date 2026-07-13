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
.LFB49:
	.seh_endprologue
	mov	eax, 42
	ret
	.seh_endproc
	.section	.text$_ZN3DogD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3DogD1Ev
	.def	_ZN3DogD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3DogD1Ev
_ZN3DogD1Ev:
.LFB65:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN3DogD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3DogD0Ev
	.def	_ZN3DogD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3DogD0Ev
_ZN3DogD0Ev:
.LFB66:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z6directRK3Dog
	.def	_Z6directRK3Dog;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6directRK3Dog
_Z6directRK3Dog:
.LFB50:
	.seh_endprologue
	lea	rdx, _ZNK3Dog5speakEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR 16[rax]
	cmp	rax, rdx
	jne	.L7
	mov	eax, 42
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	rex.W jmp	rax
	.seh_endproc
	.p2align 4
	.globl	_Z11via_virtualRK6Animal
	.def	_Z11via_virtualRK6Animal;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11via_virtualRK6Animal
_Z11via_virtualRK6Animal:
.LFB51:
	.seh_endprologue
	lea	rdx, _ZNK3Dog5speakEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR 16[rax]
	cmp	rax, rdx
	jne	.L10
	mov	eax, 42
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	rex.W jmp	rax
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB52:
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
