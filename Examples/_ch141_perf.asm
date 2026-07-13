	.file	"_ch141_perf.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK10MemStorage3getEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK10MemStorage3getEv
	.def	_ZNK10MemStorage3getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK10MemStorage3getEv
_ZNK10MemStorage3getEv:
.LFB49:
	.seh_endprologue
	mov	eax, 42
	ret
	.seh_endproc
	.section	.text$_ZN10MemStorageD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN10MemStorageD1Ev
	.def	_ZN10MemStorageD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN10MemStorageD1Ev
_ZN10MemStorageD1Ev:
.LFB66:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN10MemStorageD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN10MemStorageD0Ev
	.def	_ZN10MemStorageD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN10MemStorageD0Ev
_ZN10MemStorageD0Ev:
.LFB67:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z11via_virtualRK8IStorage
	.def	_Z11via_virtualRK8IStorage;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11via_virtualRK8IStorage
_Z11via_virtualRK8IStorage:
.LFB50:
	.seh_endprologue
	lea	rdx, _ZNK10MemStorage3getEv[rip]
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
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB53:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	DWORD PTR 40[rsp], 42
	mov	DWORD PTR 44[rsp], 42
	mov	eax, DWORD PTR 40[rsp]
	mov	edx, DWORD PTR 44[rsp]
	add	eax, edx
	add	rsp, 56
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
