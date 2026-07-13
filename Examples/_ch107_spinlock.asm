	.file	"_ch107_spinlock.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z4lockv
	.def	_Z4lockv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4lockv
_Z4lockv:
.LFB665:
	sub	rsp, 24
	.seh_stackalloc	24
	.seh_endprologue
	mov	edx, 1
.L3:
	xor	eax, eax
	mov	BYTE PTR 15[rsp], 0
	lock cmpxchg	BYTE PTR locked[rip], dl
	jne	.L3
	add	rsp, 24
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6unlockv
	.def	_Z6unlockv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6unlockv
_Z6unlockv:
.LFB666:
	.seh_endprologue
	mov	BYTE PTR locked[rip], 0
	ret
	.seh_endproc
	.globl	locked
	.bss
locked:
	.space 1
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
