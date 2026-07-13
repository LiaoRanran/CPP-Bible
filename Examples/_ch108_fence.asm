	.file	"_ch108_fence.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8producerv
	.def	_Z8producerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8producerv
_Z8producerv:
.LFB665:
	.seh_endprologue
	mov	DWORD PTR data[rip], 42
	mov	DWORD PTR flag[rip], 1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8consumerv
	.def	_Z8consumerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8consumerv
_Z8consumerv:
.LFB666:
	.seh_endprologue
	mov	eax, DWORD PTR flag[rip]
	test	eax, eax
	jne	.L8
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	ret
	.seh_endproc
	.globl	data
	.bss
	.align 4
data:
	.space 4
	.globl	flag
	.align 4
flag:
	.space 4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
