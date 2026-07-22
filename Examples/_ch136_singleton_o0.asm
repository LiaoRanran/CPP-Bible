	.file	"_ch136_singleton_o0.cpp"
	.intel_syntax noprefix
	.text
.lcomm _ZZN6Logger8instanceEvE4inst,4,4
	.align 2
	.globl	_ZN6Logger8instanceEv
	.def	_ZN6Logger8instanceEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6Logger8instanceEv
_ZN6Logger8instanceEv:
.LFB0:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	lea	rax, _ZZN6Logger8instanceEvE4inst[rip]
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z3usev
	.def	_Z3usev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3usev
_Z3usev:
.LFB4:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	call	_ZN6Logger8instanceEv
	mov	eax, DWORD PTR [rax]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
