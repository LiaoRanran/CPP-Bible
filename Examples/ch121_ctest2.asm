	.file	"ch121_ctest2.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "_asm_demo/ch121_ctest2.cpp\0"
.LC1:
	.ascii "abs_pos\0"
.LC2:
	.ascii "x >= 0\0"
.LC3:
	.ascii "default\0"
	.section	.text.unlikely,"x"
	.def	_Z7abs_posi.part.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z7abs_posi.part.0
_Z7abs_posi.part.0:
.LFB3:
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	lea	rax, .LC1[rip]
	movq	xmm0, QWORD PTR .LC4[rip]
	movq	xmm1, rax
	lea	rax, .LC3[rip]
	punpcklqdq	xmm0, xmm1
	movq	xmm2, rax
	movaps	XMMWORD PTR 32[rsp], xmm0
	lea	rcx, 32[rsp]
	movq	xmm0, QWORD PTR .LC5[rip]
	mov	QWORD PTR 64[rsp], rax
	punpcklqdq	xmm0, xmm2
	mov	DWORD PTR 72[rsp], 1
	movaps	XMMWORD PTR 48[rsp], xmm0
	mov	BYTE PTR 76[rsp], 0
	call	_Z25handle_contract_violationRKNSt12experimental18contract_violationE
	call	_ZSt9terminatev
	nop
	.seh_endproc
.LCOLDB6:
	.text
.LHOTB6:
	.p2align 4
	.globl	_Z7abs_posi
	.def	_Z7abs_posi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7abs_posi
_Z7abs_posi:
.LFB0:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	eax, ecx
	test	ecx, ecx
	js	.L4
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z7abs_posi.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z7abs_posi.cold
	.seh_stackalloc	40
	.seh_endprologue
_Z7abs_posi.cold:
.L4:
	call	_Z7abs_posi.part.0
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE6:
	.text
.LHOTE6:
	.section	.text.unlikely,"x"
.LCOLDB7:
	.text
.LHOTB7:
	.p2align 4
	.globl	_Z4useri
	.def	_Z4useri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4useri
_Z4useri:
.LFB2:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	eax, ecx
	test	ecx, ecx
	js	.L8
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z4useri.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z4useri.cold
	.seh_stackalloc	40
	.seh_endprologue
_Z4useri.cold:
.L8:
	call	_Z7abs_posi.part.0
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE7:
	.text
.LHOTE7:
	.section .rdata,"dr"
	.align 8
.LC4:
	.quad	.LC0
	.align 8
.LC5:
	.quad	.LC2
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Z25handle_contract_violationRKNSt12experimental18contract_violationE;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
