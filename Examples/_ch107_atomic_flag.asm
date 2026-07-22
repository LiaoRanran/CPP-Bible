	.file	"_ch107_atomic_flag.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7acquirev
	.def	_Z7acquirev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7acquirev
_Z7acquirev:
.LFB665:
	.seh_endprologue
	.p2align 4
	.p2align 4
	.p2align 3
.L2:
	mov	eax, 1
	xchg	al, BYTE PTR f[rip]
	test	al, al
	jne	.L2
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7releasev
	.def	_Z7releasev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7releasev
_Z7releasev:
.LFB666:
	.seh_endprologue
	mov	BYTE PTR f[rip], 0
	ret
	.seh_endproc
	.globl	f
	.bss
f:
	.space 1
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
