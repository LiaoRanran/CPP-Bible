	.file	"ch82_span_test.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8sum_spanSt4spanIKiLy18446744073709551615EE
	.def	_Z8sum_spanSt4spanIKiLy18446744073709551615EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8sum_spanSt4spanIKiLy18446744073709551615EE
_Z8sum_spanSt4spanIKiLy18446744073709551615EE:
.LFB905:
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR [rcx]
	lea	rcx, [rax+rdx*4]
	xor	edx, edx
	cmp	rax, rcx
	je	.L1
	.p2align 4
	.p2align 4
	.p2align 3
.L3:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, rcx
	jne	.L3
.L1:
	mov	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7sum_ptrPKiy
	.def	_Z7sum_ptrPKiy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7sum_ptrPKiy
_Z7sum_ptrPKiy:
.LFB910:
	.seh_endprologue
	test	rdx, rdx
	je	.L10
	lea	rdx, [rcx+rdx*4]
	xor	eax, eax
	.p2align 4
	.p2align 4
	.p2align 3
.L9:
	add	eax, DWORD PTR [rcx]
	add	rcx, 4
	cmp	rcx, rdx
	jne	.L9
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7at_spanSt4spanIKiLy18446744073709551615EEy
	.def	_Z7at_spanSt4spanIKiLy18446744073709551615EEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7at_spanSt4spanIKiLy18446744073709551615EEy
_Z7at_spanSt4spanIKiLy18446744073709551615EEy:
.LFB911:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, [rax+rdx*4]
	mov	eax, DWORD PTR [rdx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9emit_sizev
	.def	_Z9emit_sizev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9emit_sizev
_Z9emit_sizev:
.LFB912:
	.seh_endprologue
	mov	DWORD PTR g_obs[rip], 16
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB913:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, 10
	mov	DWORD PTR g_obs[rip], 16
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
