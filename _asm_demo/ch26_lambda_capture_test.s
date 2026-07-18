	.file	"ch26_lambda_capture_test.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z4sinki
	.def	_Z4sinki;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4sinki
_Z4sinki:
.LFB24:
	.seh_endprologue
	mov	eax, ecx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9get_fieldv
	.def	_Z9get_fieldv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9get_fieldv
_Z9get_fieldv:
.LFB31:
	.seh_endprologue
	lea	rax, _ZZ9get_fieldvE1g[rip]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z4bumpPi
	.def	_Z4bumpPi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4bumpPi
_Z4bumpPi:
.LFB32:
	.seh_endprologue
	add	DWORD PTR [rcx], 100
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "%d %zu %zu %zu\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB25:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	call	_Z9get_fieldv
	mov	r9d, DWORD PTR [rax]
	mov	rcx, rax
	mov	r8, rax
	call	_Z4bumpPi
	mov	ecx, 42
	call	_Z4sinki
	mov	ecx, r9d
	mov	r9d, 4
	mov	edx, eax
	call	_Z4sinki
	mov	ecx, DWORD PTR [r8]
	mov	r8d, 1
	add	edx, eax
	call	_Z4sinki
	lea	rcx, .LC0[rip]
	mov	QWORD PTR 32[rsp], 8
	add	edx, eax
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 56
	ret
	.seh_endproc
	.data
	.align 4
_ZZ9get_fieldvE1g:
	.long	7
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
