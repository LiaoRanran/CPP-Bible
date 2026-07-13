	.file	"_ch140_policy_vs_strategy.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK12NoneStrategy5checkEi,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK12NoneStrategy5checkEi
	.def	_ZNK12NoneStrategy5checkEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK12NoneStrategy5checkEi
_ZNK12NoneStrategy5checkEi:
.LFB54:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN13RangeStrategyD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN13RangeStrategyD1Ev
	.def	_ZN13RangeStrategyD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13RangeStrategyD1Ev
_ZN13RangeStrategyD1Ev:
.LFB82:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN12NoneStrategyD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN12NoneStrategyD1Ev
	.def	_ZN12NoneStrategyD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN12NoneStrategyD1Ev
_ZN12NoneStrategyD1Ev:
.LFB89:
	.seh_endprologue
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "OOR\0"
	.section	.text$_ZNK13RangeStrategy5checkEi,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK13RangeStrategy5checkEi
	.def	_ZNK13RangeStrategy5checkEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK13RangeStrategy5checkEi
_ZNK13RangeStrategy5checkEi:
.LFB53:
	.seh_endprologue
	cmp	edx, 100
	ja	.L7
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	lea	rcx, .LC0[rip]
	jmp	puts
	.seh_endproc
	.section	.text$_ZN12NoneStrategyD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN12NoneStrategyD0Ev
	.def	_ZN12NoneStrategyD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN12NoneStrategyD0Ev
_ZN12NoneStrategyD0Ev:
.LFB90:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZN13RangeStrategyD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN13RangeStrategyD0Ev
	.def	_ZN13RangeStrategyD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13RangeStrategyD0Ev
_ZN13RangeStrategyD0Ev:
.LFB83:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z11policy_demoi
	.def	_Z11policy_demoi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11policy_demoi
_Z11policy_demoi:
.LFB60:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	cmp	ecx, 100
	mov	ebx, ecx
	ja	.L12
	mov	eax, ebx
	add	rsp, 32
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L12:
	lea	rcx, .LC0[rip]
	call	puts
	mov	eax, ebx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z19policy_demo_nochecki
	.def	_Z19policy_demo_nochecki;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z19policy_demo_nochecki
_Z19policy_demo_nochecki:
.LFB64:
	.seh_endprologue
	mov	eax, ecx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z13strategy_demoiPK8Strategy
	.def	_Z13strategy_demoiPK8Strategy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13strategy_demoiPK8Strategy
_Z13strategy_demoiPK8Strategy:
.LFB68:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR [rdx]
	mov	ebx, ecx
	mov	rcx, rdx
	mov	edx, ebx
	call	[QWORD PTR 16[rax]]
	mov	eax, ebx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB69:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, 98
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	puts;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
