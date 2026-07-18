	.file	"_asm_tpl_basic.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_Z7max_valIiET_S0_S0_,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z7max_valIiET_S0_S0_
	.def	_Z7max_valIiET_S0_S0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7max_valIiET_S0_S0_
_Z7max_valIiET_S0_S0_:
.LFB209:
	.seh_endprologue
	cmp	ecx, edx
	mov	eax, edx
	cmovge	eax, ecx
	ret
	.seh_endproc
	.section	.text$_Z7max_valIdET_S0_S0_,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z7max_valIdET_S0_S0_
	.def	_Z7max_valIdET_S0_S0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7max_valIdET_S0_S0_
_Z7max_valIdET_S0_S0_:
.LFB210:
	.seh_endprologue
	movapd	xmm2, xmm1
	maxsd	xmm2, xmm0
	movapd	xmm0, xmm2
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z12use_implicitii
	.def	_Z12use_implicitii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12use_implicitii
_Z12use_implicitii:
.LFB205:
	.seh_endprologue
	cmp	ecx, edx
	mov	eax, edx
	cmovge	eax, ecx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z14use_implicit_ddd
	.def	_Z14use_implicit_ddd;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14use_implicit_ddd
_Z14use_implicit_ddd:
.LFB206:
	.seh_endprologue
	movapd	xmm2, xmm1
	maxsd	xmm2, xmm0
	movapd	xmm0, xmm2
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB208:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, 9
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
