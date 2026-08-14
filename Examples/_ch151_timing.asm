	.file	"_ch151_timing.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z9g_nofencev
	.def	_Z9g_nofencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9g_nofencev
_Z9g_nofencev:
.LFB0:
	.seh_endprologue
	mov	eax, 4950
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7g_fencev
	.def	_Z7g_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7g_fencev
_Z7g_fencev:
.LFB1:
	.seh_endprologue
	xor	edx, edx
	xor	eax, eax
	.p2align 4
	.p2align 3
.L4:
	add	rax, rdx
	add	rdx, 1
	cmp	rdx, 100
	jne	.L4
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
