	.file	"_ch142_lockfree.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8is_aliveRK12EntityRecord
	.def	_Z8is_aliveRK12EntityRecord;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8is_aliveRK12EntityRecord
_Z8is_aliveRK12EntityRecord:
.LFB662:
	.seh_endprologue
	movzx	eax, BYTE PTR 4[rcx]
	test	al, al
	setne	al
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z4killR12EntityRecord
	.def	_Z4killR12EntityRecord;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4killR12EntityRecord
_Z4killR12EntityRecord:
.LFB663:
	.seh_endprologue
	mov	BYTE PTR 4[rcx], 0
	lock add	DWORD PTR [rcx], 1
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB664:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	DWORD PTR 40[rsp], 0
	lea	rcx, 40[rsp]
	mov	BYTE PTR 44[rsp], 1
	movzx	eax, BYTE PTR 44[rsp]
	call	_Z4killR12EntityRecord
	test	al, al
	setne	al
	movzx	eax, al
	add	rsp, 56
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
