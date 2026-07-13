	.file	"_ch107_volatile.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12volatile_incv
	.def	_Z12volatile_incv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12volatile_incv
_Z12volatile_incv:
.LFB665:
	.seh_endprologue
	mov	eax, DWORD PTR v[rip]
	add	eax, 1
	mov	DWORD PTR v[rip], eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10atomic_incv
	.def	_Z10atomic_incv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10atomic_incv
_Z10atomic_incv:
.LFB666:
	.seh_endprologue
	lock add	DWORD PTR a[rip], 1
	ret
	.seh_endproc
	.globl	a
	.bss
	.align 4
a:
	.space 4
	.globl	v
	.align 4
v:
	.space 4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
