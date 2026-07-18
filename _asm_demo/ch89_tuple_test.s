	.file	"ch89_tuple_test.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7use_getRKSt5tupleIJidcEE
	.def	_Z7use_getRKSt5tupleIJidcEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7use_getRKSt5tupleIJidcEE
_Z7use_getRKSt5tupleIJidcEE:
.LFB888:
	.seh_endprologue
	movsx	edx, BYTE PTR [rcx]
	cvttsd2si	eax, QWORD PTR 8[rcx]
	add	eax, DWORD PTR 16[rcx]
	add	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8use_bindRKSt5tupleIJidcEE
	.def	_Z8use_bindRKSt5tupleIJidcEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8use_bindRKSt5tupleIJidcEE
_Z8use_bindRKSt5tupleIJidcEE:
.LFB953:
	.seh_endprologue
	movsx	edx, BYTE PTR [rcx]
	cvttsd2si	eax, QWORD PTR 8[rcx]
	add	eax, DWORD PTR 16[rcx]
	add	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7use_aggRK1P
	.def	_Z7use_aggRK1P;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7use_aggRK1P
_Z7use_aggRK1P:
.LFB900:
	.seh_endprologue
	movsx	edx, BYTE PTR 16[rcx]
	cvttsd2si	eax, QWORD PTR 8[rcx]
	add	eax, DWORD PTR [rcx]
	add	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9emit_sizev
	.def	_Z9emit_sizev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9emit_sizev
_Z9emit_sizev:
.LFB901:
	.seh_endprologue
	mov	DWORD PTR g_obs[rip], 24
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB902:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, 123
	mov	DWORD PTR g_obs[rip], 24
	add	rsp, 40
	ret
	.seh_endproc
	.globl	g_obs
	.bss
	.align 4
g_obs:
	.space 4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
