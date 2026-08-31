	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12add_noinlineii
	.def	_Z12add_noinlineii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12add_noinlineii
_Z12add_noinlineii:
.LFB50:
	.seh_endprologue
	lea	eax, [rcx+rdx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11use_inlinedv
	.def	_Z11use_inlinedv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11use_inlinedv
_Z11use_inlinedv:
.LFB51:
	.seh_endprologue
	mov	eax, 10
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12use_noinlinev
	.def	_Z12use_noinlinev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12use_noinlinev
_Z12use_noinlinev:
.LFB52:
	.seh_endprologue
	mov	edx, 4
	mov	ecx, 3
	jmp	_Z12add_noinlineii
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
