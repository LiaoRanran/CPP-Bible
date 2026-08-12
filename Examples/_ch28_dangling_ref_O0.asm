	.file	"_ch28_dangling_ref_O0.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z7bad_ptrv
	.def	_Z7bad_ptrv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7bad_ptrv
_Z7bad_ptrv:
.LFB0:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	DWORD PTR -4[rbp], 5
	mov	eax, 0
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.data
	.align 4
_ZZ8good_ptrvE1x:
	.long	5
	.text
	.globl	_Z8good_ptrv
	.def	_Z8good_ptrv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8good_ptrv
_Z8good_ptrv:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	lea	rax, _ZZ8good_ptrvE1x[rip]
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
