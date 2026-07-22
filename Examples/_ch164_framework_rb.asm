	.file	"_ch164_asm_demo.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.globl	_ZN4Ring4pushEc
	.def	_ZN4Ring4pushEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4Ring4pushEc
_ZN4Ring4pushEc:
.LFB17:
	.seh_endprologue
	mov	r8d, edx
	movsxd	rdx, DWORD PTR 20[rcx]
	mov	rax, rdx
	mov	BYTE PTR [rcx+rdx], r8b
	add	eax, 1
	cdq
	shr	edx, 28
	add	eax, edx
	and	eax, 15
	sub	eax, edx
	mov	DWORD PTR 20[rcx], eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z4demoR4Ringc
	.def	_Z4demoR4Ringc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4demoR4Ringc
_Z4demoR4Ringc:
.LFB18:
	.seh_endprologue
	mov	r8d, edx
	movsxd	rdx, DWORD PTR 20[rcx]
	mov	rax, rdx
	mov	BYTE PTR [rcx+rdx], r8b
	add	eax, 1
	cdq
	shr	edx, 28
	add	eax, edx
	and	eax, 15
	sub	eax, edx
	mov	DWORD PTR 20[rcx], eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
