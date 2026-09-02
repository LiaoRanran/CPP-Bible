	.file	"_ch22_auto_zero_cost.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7computev
	.def	_Z7computev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7computev
_Z7computev:
.LFB1561:
	.seh_endprologue
	mov	eax, 42
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8via_autov
	.def	_Z8via_autov;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8via_autov
_Z8via_autov:
.LFB1586:
	.seh_endprologue
	mov	eax, 42
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12via_explicitv
	.def	_Z12via_explicitv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12via_explicitv
_Z12via_explicitv:
.LFB1588:
	.seh_endprologue
	mov	eax, 42
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9front_refRSt6vectorIiSaIiEE
	.def	_Z9front_refRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9front_refRSt6vectorIiSaIiEE
_Z9front_refRSt6vectorIiSaIiEE:
.LFB1564:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9fwd_frontRSt6vectorIiSaIiEE
	.def	_Z9fwd_frontRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9fwd_frontRSt6vectorIiSaIiEE
_Z9fwd_frontRSt6vectorIiSaIiEE:
.LFB1590:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
