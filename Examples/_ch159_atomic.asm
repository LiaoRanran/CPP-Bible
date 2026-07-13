	.file	"_ch159_atomic.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z4bumpi
	.def	_Z4bumpi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4bumpi
_Z4bumpi:
.LFB665:
	.seh_endprologue
	test	ecx, ecx
	jle	.L4
	xor	eax, eax
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L3:
	mov	r8d, 1
	lock xadd	DWORD PTR g[rip], r8d
	add	eax, 1
	add	edx, r8d
	cmp	ecx, eax
	jne	.L3
	mov	eax, edx
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	xor	edx, edx
	mov	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9read_stopv
	.def	_Z9read_stopv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9read_stopv
_Z9read_stopv:
.LFB666:
	.seh_endprologue
	mov	eax, DWORD PTR g[rip]
	ret
	.seh_endproc
	.globl	g
	.bss
	.align 4
g:
	.space 4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
