	.file	"_ch108_dekker.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8thread_av
	.def	_Z8thread_av;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8thread_av
_Z8thread_av:
.LFB668:
	.seh_endprologue
	mov	eax, 1
	xchg	eax, DWORD PTR flag0[rip]
	mov	eax, DWORD PTR flag1[rip]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8thread_bv
	.def	_Z8thread_bv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8thread_bv
_Z8thread_bv:
.LFB669:
	.seh_endprologue
	mov	eax, 1
	xchg	eax, DWORD PTR flag1[rip]
	mov	eax, DWORD PTR flag0[rip]
	ret
	.seh_endproc
	.globl	turn
	.bss
	.align 4
turn:
	.space 4
	.globl	flag1
	.align 4
flag1:
	.space 4
	.globl	flag0
	.align 4
flag0:
	.space 4
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
