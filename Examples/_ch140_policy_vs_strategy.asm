	.file	"_ch140_policy_vs_strategy.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch140_policy_vs_strategy.cpp"
	.section .rdata,"dr"
.LC0:
	.ascii "OOR\0"
	.section	.text$_ZN10RangeCheck5checkEi,"x"
	.linkonce discard
	.globl	_ZN10RangeCheck5checkEi
	.def	_ZN10RangeCheck5checkEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN10RangeCheck5checkEi
_ZN10RangeCheck5checkEi:
.LFB23:
	.file 1 "Examples/_ch140_policy_vs_strategy.cpp"
	.loc 1 11 33
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	.loc 1 11 48
	cmp	DWORD PTR 16[rbp], 0
	js	.L2
	.loc 1 11 58 discriminator 2
	cmp	DWORD PTR 16[rbp], 100
	jle	.L4
.L2:
	.loc 1 11 79 discriminator 3
	lea	rax, .LC0[rip]
	mov	rcx, rax
	call	puts
.L4:
	.loc 1 11 88
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE23:
	.seh_endproc
	.section	.text$_ZN7NoCheck5checkEi,"x"
	.linkonce discard
	.globl	_ZN7NoCheck5checkEi
	.def	_ZN7NoCheck5checkEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7NoCheck5checkEi
_ZN7NoCheck5checkEi:
.LFB24:
	.loc 1 12 33
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	.loc 1 12 47
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE24:
	.seh_endproc
	.section	.text$_ZNK13RangeStrategy5checkEi,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK13RangeStrategy5checkEi
	.def	_ZNK13RangeStrategy5checkEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK13RangeStrategy5checkEi
_ZNK13RangeStrategy5checkEi:
.LFB25:
	.loc 1 19 40
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
	.loc 1 19 70
	cmp	DWORD PTR 24[rbp], 0
	js	.L7
	.loc 1 19 80 discriminator 2
	cmp	DWORD PTR 24[rbp], 100
	jle	.L9
.L7:
	.loc 1 19 101 discriminator 3
	lea	rax, .LC0[rip]
	mov	rcx, rax
	call	puts
.L9:
	.loc 1 19 110
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE25:
	.seh_endproc
	.section	.text$_ZNK12NoneStrategy5checkEi,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK12NoneStrategy5checkEi
	.def	_ZNK12NoneStrategy5checkEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK12NoneStrategy5checkEi
_ZNK12NoneStrategy5checkEi:
.LFB26:
	.loc 1 20 40
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
	.loc 1 20 67
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE26:
	.seh_endproc
	.section	.text$_ZN14StrategyWidgetC1EPK8Strategy,"x"
	.linkonce discard
	.align 2
	.globl	_ZN14StrategyWidgetC1EPK8Strategy
	.def	_ZN14StrategyWidgetC1EPK8Strategy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN14StrategyWidgetC1EPK8Strategy
_ZN14StrategyWidgetC1EPK8Strategy:
.LFB29:
	.loc 1 25 5
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
.LBB2:
	.loc 1 25 44
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR [rax], 0
	.loc 1 25 41
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR 8[rax], rdx
.LBE2:
	.loc 1 25 47
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE29:
	.seh_endproc
	.section	.text$_ZN14StrategyWidget3setEi,"x"
	.linkonce discard
	.align 2
	.globl	_ZN14StrategyWidget3setEi
	.def	_ZN14StrategyWidget3setEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN14StrategyWidget3setEi
_ZN14StrategyWidget3setEi:
.LFB30:
	.loc 1 26 10
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
	.loc 1 26 23
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	.loc 1 26 31
	mov	rax, QWORD PTR [rax]
	add	rax, 16
	mov	r8, QWORD PTR [rax]
	.loc 1 26 23
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	.loc 1 26 31
	mov	edx, DWORD PTR 24[rbp]
	mov	rcx, rax
	call	r8
.LVL0:
	.loc 1 26 42 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, DWORD PTR 24[rbp]
	mov	DWORD PTR [rax], edx
	.loc 1 26 47
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE30:
	.seh_endproc
	.section	.text$_ZNK14StrategyWidget3getEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK14StrategyWidget3getEv
	.def	_ZNK14StrategyWidget3getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK14StrategyWidget3getEv
_ZNK14StrategyWidget3getEv:
.LFB31:
	.loc 1 27 10
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 1 27 31
	mov	rax, QWORD PTR 16[rbp]
	mov	eax, DWORD PTR [rax]
	.loc 1 27 38
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE31:
	.seh_endproc
	.text
	.globl	_Z11policy_demoi
	.def	_Z11policy_demoi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11policy_demoi
_Z11policy_demoi:
.LFB32:
	.loc 1 30 24
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	.loc 1 31 30
	mov	DWORD PTR -4[rbp], 0
	.loc 1 32 10
	mov	edx, DWORD PTR 16[rbp]
	lea	rax, -4[rbp]
	mov	rcx, rax
	call	_ZN12PolicyWidgetI10RangeCheckE3setEi
	.loc 1 33 17
	lea	rax, -4[rbp]
	mov	rcx, rax
	call	_ZNK12PolicyWidgetI10RangeCheckE3getEv
	.loc 1 34 1
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE32:
	.seh_endproc
	.globl	_Z19policy_demo_nochecki
	.def	_Z19policy_demo_nochecki;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z19policy_demo_nochecki
_Z19policy_demo_nochecki:
.LFB36:
	.loc 1 35 32
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	.loc 1 36 27
	mov	DWORD PTR -4[rbp], 0
	.loc 1 37 10
	mov	edx, DWORD PTR 16[rbp]
	lea	rax, -4[rbp]
	mov	rcx, rax
	call	_ZN12PolicyWidgetI7NoCheckE3setEi
	.loc 1 38 17
	lea	rax, -4[rbp]
	mov	rcx, rax
	call	_ZNK12PolicyWidgetI7NoCheckE3getEv
	.loc 1 39 1
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE36:
	.seh_endproc
	.globl	_Z13strategy_demoiPK8Strategy
	.def	_Z13strategy_demoiPK8Strategy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13strategy_demoiPK8Strategy
_Z13strategy_demoiPK8Strategy:
.LFB40:
	.loc 1 40 45
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	QWORD PTR 24[rbp], rdx
	.loc 1 41 23
	mov	rdx, QWORD PTR 24[rbp]
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZN14StrategyWidgetC1EPK8Strategy
	.loc 1 42 10
	mov	edx, DWORD PTR 16[rbp]
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZN14StrategyWidget3setEi
	.loc 1 43 17
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZNK14StrategyWidget3getEv
	.loc 1 44 1
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE40:
	.seh_endproc
	.section	.text$_ZN8StrategyD2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN8StrategyD2Ev
	.def	_ZN8StrategyD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN8StrategyD2Ev
_ZN8StrategyD2Ev:
.LFB47:
	.loc 1 16 13
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB3:
	.loc 1 16 13
	lea	rdx, _ZTV8Strategy[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
.LBE3:
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE47:
	.seh_endproc
	.section	.text$_ZN13RangeStrategyD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN13RangeStrategyD1Ev
	.def	_ZN13RangeStrategyD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13RangeStrategyD1Ev
_ZN13RangeStrategyD1Ev:
.LFB54:
	.loc 1 19 8
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB4:
	.loc 1 19 8
	lea	rdx, _ZTV13RangeStrategy[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN8StrategyD2Ev
.LBE4:
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE54:
	.seh_endproc
	.section	.text$_ZN13RangeStrategyD0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN13RangeStrategyD0Ev
	.def	_ZN13RangeStrategyD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13RangeStrategyD0Ev
_ZN13RangeStrategyD0Ev:
.LFB55:
	.loc 1 19 8
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 1 19 8
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN13RangeStrategyD1Ev
	.loc 1 19 8 is_stmt 0 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 8
	mov	rcx, rax
	call	_ZdlPvy
	nop
	.loc 1 19 8
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE55:
	.seh_endproc
	.section	.text$_ZN12NoneStrategyD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN12NoneStrategyD1Ev
	.def	_ZN12NoneStrategyD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN12NoneStrategyD1Ev
_ZN12NoneStrategyD1Ev:
.LFB61:
	.loc 1 20 8 is_stmt 1
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB5:
	.loc 1 20 8
	lea	rdx, _ZTV12NoneStrategy[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN8StrategyD2Ev
.LBE5:
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE61:
	.seh_endproc
	.section	.text$_ZN12NoneStrategyD0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN12NoneStrategyD0Ev
	.def	_ZN12NoneStrategyD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN12NoneStrategyD0Ev
_ZN12NoneStrategyD0Ev:
.LFB62:
	.loc 1 20 8
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 1 20 8
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN12NoneStrategyD1Ev
	.loc 1 20 8 is_stmt 0 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 8
	mov	rcx, rax
	call	_ZdlPvy
	nop
	.loc 1 20 8
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE62:
	.seh_endproc
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB41:
	.loc 1 45 12 is_stmt 1
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	sub	rsp, 56
	.seh_stackalloc	56
	.cfi_def_cfa_offset 80
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.cfi_def_cfa 6, 32
	.seh_endprologue
	.loc 1 45 12
	call	__main
	.loc 1 46 19
	lea	rax, _ZTV13RangeStrategy[rip+16]
	mov	QWORD PTR -8[rbp], rax
	.loc 1 47 19
	lea	rax, _ZTV12NoneStrategy[rip+16]
	mov	QWORD PTR -16[rbp], rax
	.loc 1 48 23
	mov	ecx, 42
.LEHB0:
	call	_Z11policy_demoi
	mov	ebx, eax
	.loc 1 48 49 discriminator 2
	mov	ecx, 7
	call	_Z19policy_demo_nochecki
	.loc 1 48 28 discriminator 4
	add	ebx, eax
	.loc 1 49 25
	lea	rax, -8[rbp]
	mov	rdx, rax
	mov	ecx, 42
	call	_Z13strategy_demoiPK8Strategy
	.loc 1 49 10 discriminator 2
	add	ebx, eax
	.loc 1 49 50 discriminator 2
	lea	rax, -16[rbp]
	mov	rdx, rax
	mov	ecx, 7
	call	_Z13strategy_demoiPK8Strategy
.LEHE0:
	.loc 1 49 57 discriminator 4
	add	ebx, eax
	.loc 1 50 1
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZN12NoneStrategyD1Ev
	.loc 1 50 1 is_stmt 0 discriminator 2
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZN13RangeStrategyD1Ev
	.loc 1 50 1
	mov	eax, ebx
	jmp	.L30
.L29:
	mov	rbx, rax
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZN12NoneStrategyD1Ev
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZN13RangeStrategyD1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB1:
	call	_Unwind_Resume
.LEHE1:
.L30:
	add	rsp, 56
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -40
	ret
	.cfi_endproc
.LFE41:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA41:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE41-.LLSDACSB41
.LLSDACSB41:
	.uleb128 .LEHB0-.LFB41
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L29-.LFB41
	.uleb128 0
	.uleb128 .LEHB1-.LFB41
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE41:
	.text
	.seh_endproc
	.section	.text$_ZN12PolicyWidgetI10RangeCheckE3setEi,"x"
	.linkonce discard
	.align 2
	.globl	_ZN12PolicyWidgetI10RangeCheckE3setEi
	.def	_ZN12PolicyWidgetI10RangeCheckE3setEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN12PolicyWidgetI10RangeCheckE3setEi
_ZN12PolicyWidgetI10RangeCheckE3setEi:
.LFB63:
	.loc 1 7 10 is_stmt 1
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
	.loc 1 7 44
	mov	eax, DWORD PTR 24[rbp]
	mov	ecx, eax
	call	_ZN10RangeCheck5checkEi
	.loc 1 7 55 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, DWORD PTR 24[rbp]
	mov	DWORD PTR [rax], edx
	.loc 1 7 60
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE63:
	.seh_endproc
	.section	.text$_ZNK12PolicyWidgetI10RangeCheckE3getEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK12PolicyWidgetI10RangeCheckE3getEv
	.def	_ZNK12PolicyWidgetI10RangeCheckE3getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK12PolicyWidgetI10RangeCheckE3getEv
_ZNK12PolicyWidgetI10RangeCheckE3getEv:
.LFB64:
	.loc 1 8 10
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 1 8 31
	mov	rax, QWORD PTR 16[rbp]
	mov	eax, DWORD PTR [rax]
	.loc 1 8 38
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE64:
	.seh_endproc
	.section	.text$_ZN12PolicyWidgetI7NoCheckE3setEi,"x"
	.linkonce discard
	.align 2
	.globl	_ZN12PolicyWidgetI7NoCheckE3setEi
	.def	_ZN12PolicyWidgetI7NoCheckE3setEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN12PolicyWidgetI7NoCheckE3setEi
_ZN12PolicyWidgetI7NoCheckE3setEi:
.LFB65:
	.loc 1 7 10
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
	.loc 1 7 44
	mov	eax, DWORD PTR 24[rbp]
	mov	ecx, eax
	call	_ZN7NoCheck5checkEi
	.loc 1 7 55 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, DWORD PTR 24[rbp]
	mov	DWORD PTR [rax], edx
	.loc 1 7 60
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE65:
	.seh_endproc
	.section	.text$_ZNK12PolicyWidgetI7NoCheckE3getEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK12PolicyWidgetI7NoCheckE3getEv
	.def	_ZNK12PolicyWidgetI7NoCheckE3getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK12PolicyWidgetI7NoCheckE3getEv
_ZNK12PolicyWidgetI7NoCheckE3getEv:
.LFB66:
	.loc 1 8 10
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 1 8 31
	mov	rax, QWORD PTR 16[rbp]
	mov	eax, DWORD PTR [rax]
	.loc 1 8 38
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE66:
	.seh_endproc
	.globl	_ZTV12NoneStrategy
	.section	.rdata$_ZTV12NoneStrategy,"dr"
	.linkonce same_size
	.align 8
_ZTV12NoneStrategy:
	.quad	0
	.quad	_ZTI12NoneStrategy
	.quad	_ZN12NoneStrategyD1Ev
	.quad	_ZN12NoneStrategyD0Ev
	.quad	_ZNK12NoneStrategy5checkEi
	.globl	_ZTV13RangeStrategy
	.section	.rdata$_ZTV13RangeStrategy,"dr"
	.linkonce same_size
	.align 8
_ZTV13RangeStrategy:
	.quad	0
	.quad	_ZTI13RangeStrategy
	.quad	_ZN13RangeStrategyD1Ev
	.quad	_ZN13RangeStrategyD0Ev
	.quad	_ZNK13RangeStrategy5checkEi
	.globl	_ZTV8Strategy
	.section	.rdata$_ZTV8Strategy,"dr"
	.linkonce same_size
	.align 8
_ZTV8Strategy:
	.quad	0
	.quad	_ZTI8Strategy
	.quad	0
	.quad	0
	.quad	__cxa_pure_virtual
	.globl	_ZTI12NoneStrategy
	.section	.rdata$_ZTI12NoneStrategy,"dr"
	.linkonce same_size
	.align 8
_ZTI12NoneStrategy:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS12NoneStrategy
	.quad	_ZTI8Strategy
	.globl	_ZTS12NoneStrategy
	.section	.rdata$_ZTS12NoneStrategy,"dr"
	.linkonce same_size
	.align 8
_ZTS12NoneStrategy:
	.ascii "12NoneStrategy\0"
	.globl	_ZTI13RangeStrategy
	.section	.rdata$_ZTI13RangeStrategy,"dr"
	.linkonce same_size
	.align 8
_ZTI13RangeStrategy:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS13RangeStrategy
	.quad	_ZTI8Strategy
	.globl	_ZTS13RangeStrategy
	.section	.rdata$_ZTS13RangeStrategy,"dr"
	.linkonce same_size
	.align 16
_ZTS13RangeStrategy:
	.ascii "13RangeStrategy\0"
	.globl	_ZTI8Strategy
	.section	.rdata$_ZTI8Strategy,"dr"
	.linkonce same_size
	.align 8
_ZTI8Strategy:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS8Strategy
	.globl	_ZTS8Strategy
	.section	.rdata$_ZTS8Strategy,"dr"
	.linkonce same_size
	.align 8
_ZTS8Strategy:
	.ascii "8Strategy\0"
	.weak	__cxa_pure_virtual
	.text
.Letext0:
	.file 2 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/stdio.h"
	.file 3 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/corecrt.h"
	.file 4 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/cstdio"
	.file 5 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/x86_64-w64-mingw32/bits/c++config.h"
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0x1455
	.word	0x5
	.byte	0x1
	.byte	0x8
	.secrel32	.Ldebug_abbrev0
	.uleb128 0x29
	.ascii "GNU C++23 15.3.0 -masm=intel -mtune=generic -march=x86-64 -g -O0 -std=c++23\0"
	.byte	0x21
	.byte	0x4
	.long	0x3163e
	.secrel32	.LASF0
	.secrel32	.LASF1
	.secrel32	.LLRL0
	.quad	0
	.secrel32	.Ldebug_line0
	.uleb128 0x1b
	.ascii "__builtin_va_list\0"
	.long	0x8e
	.uleb128 0x9
	.byte	0x1
	.byte	0x6
	.ascii "char\0"
	.uleb128 0x5
	.long	0x8e
	.uleb128 0x16
	.ascii "size_t\0"
	.byte	0x3
	.byte	0x23
	.byte	0x2c
	.long	0xaa
	.uleb128 0x9
	.byte	0x8
	.byte	0x7
	.ascii "long long unsigned int\0"
	.uleb128 0x9
	.byte	0x8
	.byte	0x5
	.ascii "long long int\0"
	.uleb128 0x9
	.byte	0x2
	.byte	0x7
	.ascii "short unsigned int\0"
	.uleb128 0x9
	.byte	0x4
	.byte	0x5
	.ascii "int\0"
	.uleb128 0x9
	.byte	0x4
	.byte	0x5
	.ascii "long int\0"
	.uleb128 0x6
	.long	0x8e
	.uleb128 0x9
	.byte	0x2
	.byte	0x7
	.ascii "wchar_t\0"
	.uleb128 0x9
	.byte	0x4
	.byte	0x7
	.ascii "unsigned int\0"
	.uleb128 0x9
	.byte	0x4
	.byte	0x7
	.ascii "long unsigned int\0"
	.uleb128 0x9
	.byte	0x1
	.byte	0x8
	.ascii "unsigned char\0"
	.uleb128 0xf
	.ascii "_iobuf\0"
	.byte	0x30
	.byte	0x2
	.byte	0x21
	.byte	0xa
	.long	0x1d4
	.uleb128 0x8
	.ascii "_ptr\0"
	.byte	0x2
	.byte	0x25
	.byte	0xb
	.long	0xfe
	.byte	0
	.uleb128 0x8
	.ascii "_cnt\0"
	.byte	0x2
	.byte	0x26
	.byte	0x9
	.long	0xeb
	.byte	0x8
	.uleb128 0x8
	.ascii "_base\0"
	.byte	0x2
	.byte	0x27
	.byte	0xb
	.long	0xfe
	.byte	0x10
	.uleb128 0x8
	.ascii "_flag\0"
	.byte	0x2
	.byte	0x28
	.byte	0x9
	.long	0xeb
	.byte	0x18
	.uleb128 0x8
	.ascii "_file\0"
	.byte	0x2
	.byte	0x29
	.byte	0x9
	.long	0xeb
	.byte	0x1c
	.uleb128 0x8
	.ascii "_charbuf\0"
	.byte	0x2
	.byte	0x2a
	.byte	0x9
	.long	0xeb
	.byte	0x20
	.uleb128 0x8
	.ascii "_bufsiz\0"
	.byte	0x2
	.byte	0x2b
	.byte	0x9
	.long	0xeb
	.byte	0x24
	.uleb128 0x8
	.ascii "_tmpfname\0"
	.byte	0x2
	.byte	0x2c
	.byte	0xb
	.long	0xfe
	.byte	0x28
	.byte	0
	.uleb128 0x16
	.ascii "FILE\0"
	.byte	0x2
	.byte	0x2f
	.byte	0x19
	.long	0x144
	.uleb128 0x16
	.ascii "fpos_t\0"
	.byte	0x2
	.byte	0x70
	.byte	0x25
	.long	0xc4
	.uleb128 0x5
	.long	0x1e1
	.uleb128 0x1c
	.ascii "std\0"
	.word	0x150
	.long	0x320
	.uleb128 0x2
	.byte	0x64
	.byte	0xb
	.long	0x1d4
	.uleb128 0x2
	.byte	0x65
	.byte	0xb
	.long	0x1e1
	.uleb128 0x2
	.byte	0x67
	.byte	0xb
	.long	0x320
	.uleb128 0x2
	.byte	0x68
	.byte	0xb
	.long	0x33b
	.uleb128 0x2
	.byte	0x69
	.byte	0xb
	.long	0x354
	.uleb128 0x2
	.byte	0x6a
	.byte	0xb
	.long	0x36b
	.uleb128 0x2
	.byte	0x6b
	.byte	0xb
	.long	0x384
	.uleb128 0x2
	.byte	0x6c
	.byte	0xb
	.long	0x39d
	.uleb128 0x2
	.byte	0x6d
	.byte	0xb
	.long	0x3b5
	.uleb128 0x2
	.byte	0x6e
	.byte	0xb
	.long	0x3d9
	.uleb128 0x2
	.byte	0x6f
	.byte	0xb
	.long	0x3fb
	.uleb128 0x2
	.byte	0x70
	.byte	0xb
	.long	0x41d
	.uleb128 0x2
	.byte	0x73
	.byte	0xb
	.long	0x44c
	.uleb128 0x2
	.byte	0x74
	.byte	0xb
	.long	0x475
	.uleb128 0x2
	.byte	0x75
	.byte	0xb
	.long	0x499
	.uleb128 0x2
	.byte	0x76
	.byte	0xb
	.long	0x4c6
	.uleb128 0x2
	.byte	0x77
	.byte	0xb
	.long	0x4e8
	.uleb128 0x2
	.byte	0x78
	.byte	0xb
	.long	0x50c
	.uleb128 0x2
	.byte	0x7a
	.byte	0xb
	.long	0x524
	.uleb128 0x2
	.byte	0x7b
	.byte	0xb
	.long	0x53b
	.uleb128 0x2
	.byte	0x80
	.byte	0xb
	.long	0x54b
	.uleb128 0x2
	.byte	0x81
	.byte	0xb
	.long	0x55f
	.uleb128 0x2
	.byte	0x85
	.byte	0xb
	.long	0x587
	.uleb128 0x2
	.byte	0x86
	.byte	0xb
	.long	0x5a0
	.uleb128 0x2
	.byte	0x87
	.byte	0xb
	.long	0x5be
	.uleb128 0x2
	.byte	0x88
	.byte	0xb
	.long	0x5d2
	.uleb128 0x2
	.byte	0x89
	.byte	0xb
	.long	0x5f8
	.uleb128 0x2
	.byte	0x8a
	.byte	0xb
	.long	0x611
	.uleb128 0x2
	.byte	0x8b
	.byte	0xb
	.long	0x63a
	.uleb128 0x2
	.byte	0x8c
	.byte	0xb
	.long	0x669
	.uleb128 0x2
	.byte	0x8d
	.byte	0xb
	.long	0x696
	.uleb128 0x2
	.byte	0x8f
	.byte	0xb
	.long	0x6a6
	.uleb128 0x2
	.byte	0x91
	.byte	0xb
	.long	0x6bf
	.uleb128 0x2
	.byte	0x92
	.byte	0xb
	.long	0x6dd
	.uleb128 0x2
	.byte	0x93
	.byte	0xb
	.long	0x712
	.uleb128 0x2
	.byte	0x94
	.byte	0xb
	.long	0x740
	.uleb128 0x2
	.byte	0xbb
	.byte	0x16
	.long	0x7ac
	.uleb128 0x2
	.byte	0xbc
	.byte	0x16
	.long	0x7e2
	.uleb128 0x2
	.byte	0xbd
	.byte	0x16
	.long	0x815
	.uleb128 0x2
	.byte	0xbe
	.byte	0x16
	.long	0x841
	.uleb128 0x2
	.byte	0xbf
	.byte	0x16
	.long	0x880
	.byte	0
	.uleb128 0x11
	.ascii "clearerr\0"
	.word	0x21e
	.long	0x336
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x6
	.long	0x1d4
	.uleb128 0x4
	.ascii "fclose\0"
	.word	0x21f
	.byte	0xf
	.long	0xeb
	.long	0x354
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x4
	.ascii "feof\0"
	.word	0x226
	.byte	0xf
	.long	0xeb
	.long	0x36b
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x4
	.ascii "ferror\0"
	.word	0x227
	.byte	0xf
	.long	0xeb
	.long	0x384
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x4
	.ascii "fflush\0"
	.word	0x228
	.byte	0xf
	.long	0xeb
	.long	0x39d
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x4
	.ascii "fgetc\0"
	.word	0x229
	.byte	0xf
	.long	0xeb
	.long	0x3b5
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x4
	.ascii "fgetpos\0"
	.word	0x22b
	.byte	0xf
	.long	0xeb
	.long	0x3d4
	.uleb128 0x1
	.long	0x336
	.uleb128 0x1
	.long	0x3d4
	.byte	0
	.uleb128 0x6
	.long	0x1e1
	.uleb128 0x4
	.ascii "fgets\0"
	.word	0x22d
	.byte	0x11
	.long	0xfe
	.long	0x3fb
	.uleb128 0x1
	.long	0xfe
	.uleb128 0x1
	.long	0xeb
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x4
	.ascii "fopen\0"
	.word	0x23b
	.byte	0x11
	.long	0x336
	.long	0x418
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x418
	.byte	0
	.uleb128 0x6
	.long	0x96
	.uleb128 0x7
	.ascii "fprintf\0"
	.word	0x15a
	.ascii "__mingw_fprintf\0"
	.long	0xeb
	.long	0x44c
	.uleb128 0x1
	.long	0x336
	.uleb128 0x1
	.long	0x418
	.uleb128 0xb
	.byte	0
	.uleb128 0x4
	.ascii "fread\0"
	.word	0x240
	.byte	0x12
	.long	0x9b
	.long	0x473
	.uleb128 0x1
	.long	0x473
	.uleb128 0x1
	.long	0x9b
	.uleb128 0x1
	.long	0x9b
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x2a
	.byte	0x8
	.uleb128 0x4
	.ascii "freopen\0"
	.word	0x241
	.byte	0x11
	.long	0x336
	.long	0x499
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x7
	.ascii "fscanf\0"
	.word	0x13d
	.ascii "__mingw_fscanf\0"
	.long	0xeb
	.long	0x4c6
	.uleb128 0x1
	.long	0x336
	.uleb128 0x1
	.long	0x418
	.uleb128 0xb
	.byte	0
	.uleb128 0x4
	.ascii "fseek\0"
	.word	0x245
	.byte	0xf
	.long	0xeb
	.long	0x4e8
	.uleb128 0x1
	.long	0x336
	.uleb128 0x1
	.long	0xf2
	.uleb128 0x1
	.long	0xeb
	.byte	0
	.uleb128 0x4
	.ascii "fsetpos\0"
	.word	0x243
	.byte	0xf
	.long	0xeb
	.long	0x507
	.uleb128 0x1
	.long	0x336
	.uleb128 0x1
	.long	0x507
	.byte	0
	.uleb128 0x6
	.long	0x1f0
	.uleb128 0x4
	.ascii "ftell\0"
	.word	0x246
	.byte	0x10
	.long	0xf2
	.long	0x524
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x4
	.ascii "getc\0"
	.word	0x258
	.byte	0xf
	.long	0xeb
	.long	0x53b
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x1d
	.ascii "getchar\0"
	.word	0x259
	.byte	0xf
	.long	0xeb
	.uleb128 0x11
	.ascii "perror\0"
	.word	0x263
	.long	0x55f
	.uleb128 0x1
	.long	0x418
	.byte	0
	.uleb128 0x7
	.ascii "printf\0"
	.word	0x15e
	.ascii "__mingw_printf\0"
	.long	0xeb
	.long	0x587
	.uleb128 0x1
	.long	0x418
	.uleb128 0xb
	.byte	0
	.uleb128 0x4
	.ascii "remove\0"
	.word	0x273
	.byte	0xf
	.long	0xeb
	.long	0x5a0
	.uleb128 0x1
	.long	0x418
	.byte	0
	.uleb128 0x4
	.ascii "rename\0"
	.word	0x274
	.byte	0xf
	.long	0xeb
	.long	0x5be
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x418
	.byte	0
	.uleb128 0x11
	.ascii "rewind\0"
	.word	0x27a
	.long	0x5d2
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x7
	.ascii "scanf\0"
	.word	0x139
	.ascii "__mingw_scanf\0"
	.long	0xeb
	.long	0x5f8
	.uleb128 0x1
	.long	0x418
	.uleb128 0xb
	.byte	0
	.uleb128 0x11
	.ascii "setbuf\0"
	.word	0x27c
	.long	0x611
	.uleb128 0x1
	.long	0x336
	.uleb128 0x1
	.long	0xfe
	.byte	0
	.uleb128 0x4
	.ascii "setvbuf\0"
	.word	0x280
	.byte	0xf
	.long	0xeb
	.long	0x63a
	.uleb128 0x1
	.long	0x336
	.uleb128 0x1
	.long	0xfe
	.uleb128 0x1
	.long	0xeb
	.uleb128 0x1
	.long	0x9b
	.byte	0
	.uleb128 0x7
	.ascii "sprintf\0"
	.word	0x162
	.ascii "__mingw_sprintf\0"
	.long	0xeb
	.long	0x669
	.uleb128 0x1
	.long	0xfe
	.uleb128 0x1
	.long	0x418
	.uleb128 0xb
	.byte	0
	.uleb128 0x7
	.ascii "sscanf\0"
	.word	0x135
	.ascii "__mingw_sscanf\0"
	.long	0xeb
	.long	0x696
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x418
	.uleb128 0xb
	.byte	0
	.uleb128 0x1d
	.ascii "tmpfile\0"
	.word	0x291
	.byte	0x11
	.long	0x336
	.uleb128 0x4
	.ascii "tmpnam\0"
	.word	0x293
	.byte	0x11
	.long	0xfe
	.long	0x6bf
	.uleb128 0x1
	.long	0xfe
	.byte	0
	.uleb128 0x4
	.ascii "ungetc\0"
	.word	0x294
	.byte	0xf
	.long	0xeb
	.long	0x6dd
	.uleb128 0x1
	.long	0xeb
	.uleb128 0x1
	.long	0x336
	.byte	0
	.uleb128 0x7
	.ascii "vfprintf\0"
	.word	0x177
	.ascii "__mingw_vfprintf\0"
	.long	0xeb
	.long	0x712
	.uleb128 0x1
	.long	0x336
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x7
	.ascii "vprintf\0"
	.word	0x17b
	.ascii "__mingw_vprintf\0"
	.long	0xeb
	.long	0x740
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x7
	.ascii "vsprintf\0"
	.word	0x180
	.ascii "_Z8vsprintfPcPKcS_\0"
	.long	0xeb
	.long	0x777
	.uleb128 0x1
	.long	0xfe
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x1c
	.ascii "__gnu_cxx\0"
	.word	0x175
	.long	0x7ac
	.uleb128 0x2
	.byte	0xb1
	.byte	0xb
	.long	0x7ac
	.uleb128 0x2
	.byte	0xb2
	.byte	0xb
	.long	0x7e2
	.uleb128 0x2
	.byte	0xb3
	.byte	0xb
	.long	0x815
	.uleb128 0x2
	.byte	0xb4
	.byte	0xb
	.long	0x841
	.uleb128 0x2
	.byte	0xb5
	.byte	0xb
	.long	0x880
	.byte	0
	.uleb128 0x7
	.ascii "snprintf\0"
	.word	0x18f
	.ascii "__mingw_snprintf\0"
	.long	0xeb
	.long	0x7e2
	.uleb128 0x1
	.long	0xfe
	.uleb128 0x1
	.long	0x9b
	.uleb128 0x1
	.long	0x418
	.uleb128 0xb
	.byte	0
	.uleb128 0x7
	.ascii "vfscanf\0"
	.word	0x14f
	.ascii "__mingw_vfscanf\0"
	.long	0xeb
	.long	0x815
	.uleb128 0x1
	.long	0x336
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x7
	.ascii "vscanf\0"
	.word	0x14b
	.ascii "__mingw_vscanf\0"
	.long	0xeb
	.long	0x841
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x7
	.ascii "vsnprintf\0"
	.word	0x1a0
	.ascii "_Z9vsnprintfPcyPKcS_\0"
	.long	0xeb
	.long	0x880
	.uleb128 0x1
	.long	0xfe
	.uleb128 0x1
	.long	0x9b
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x7
	.ascii "vsscanf\0"
	.word	0x147
	.ascii "__mingw_vsscanf\0"
	.long	0xeb
	.long	0x8b3
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x418
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0xf
	.ascii "RangeCheck\0"
	.byte	0x1
	.byte	0x1
	.byte	0xb
	.byte	0x8
	.long	0x8ec
	.uleb128 0x1e
	.secrel32	.LASF2
	.byte	0xb
	.ascii "_ZN10RangeCheck5checkEi\0"
	.uleb128 0x1
	.long	0xeb
	.byte	0
	.byte	0
	.uleb128 0xf
	.ascii "NoCheck\0"
	.byte	0x1
	.byte	0x1
	.byte	0xc
	.byte	0x8
	.long	0x91e
	.uleb128 0x1e
	.secrel32	.LASF2
	.byte	0xc
	.ascii "_ZN7NoCheck5checkEi\0"
	.uleb128 0x1
	.long	0xeb
	.byte	0
	.byte	0
	.uleb128 0x2b
	.secrel32	.LASF3
	.byte	0x10
	.byte	0x1
	.byte	0x16
	.byte	0x8
	.long	0x9e7
	.uleb128 0x8
	.ascii "value\0"
	.byte	0x1
	.byte	0x17
	.byte	0x9
	.long	0xeb
	.byte	0
	.uleb128 0x8
	.ascii "s\0"
	.byte	0x1
	.byte	0x18
	.byte	0x15
	.long	0xacd
	.byte	0x8
	.uleb128 0x2c
	.secrel32	.LASF3
	.byte	0x1
	.byte	0x19
	.byte	0x5
	.ascii "_ZN14StrategyWidgetC4EPK8Strategy\0"
	.long	0x977
	.long	0x982
	.uleb128 0x3
	.long	0xad2
	.uleb128 0x1
	.long	0xacd
	.byte	0
	.uleb128 0x17
	.ascii "set\0"
	.byte	0x1a
	.ascii "_ZN14StrategyWidget3setEi\0"
	.long	0x9aa
	.long	0x9b5
	.uleb128 0x3
	.long	0xad2
	.uleb128 0x1
	.long	0xeb
	.byte	0
	.uleb128 0x2d
	.ascii "get\0"
	.byte	0x1
	.byte	0x1b
	.byte	0xa
	.ascii "_ZNK14StrategyWidget3getEv\0"
	.long	0xeb
	.long	0x9e0
	.uleb128 0x3
	.long	0xadc
	.byte	0
	.byte	0
	.uleb128 0x5
	.long	0x91e
	.uleb128 0x18
	.secrel32	.LASF4
	.byte	0xf
	.long	0x9ec
	.long	0xac8
	.uleb128 0xc
	.secrel32	.LASF4
	.ascii "_ZN8StrategyC4ERKS_\0"
	.long	0xa1b
	.long	0xa26
	.uleb128 0x3
	.long	0xee1
	.uleb128 0x1
	.long	0xeeb
	.byte	0
	.uleb128 0xc
	.secrel32	.LASF4
	.ascii "_ZN8StrategyC4Ev\0"
	.long	0xa44
	.long	0xa4a
	.uleb128 0x3
	.long	0xee1
	.byte	0
	.uleb128 0x2e
	.ascii "_vptr.Strategy\0"
	.long	0xefb
	.byte	0
	.uleb128 0x2f
	.ascii "~Strategy\0"
	.byte	0x1
	.byte	0x10
	.byte	0xd
	.ascii "_ZN8StrategyD4Ev\0"
	.byte	0x1
	.long	0x9ec
	.byte	0x1
	.long	0xa8c
	.long	0xa92
	.uleb128 0x3
	.long	0xee1
	.byte	0
	.uleb128 0x30
	.secrel32	.LASF2
	.byte	0x1
	.byte	0x11
	.byte	0x12
	.ascii "_ZNK8Strategy5checkEi\0"
	.byte	0x1
	.uleb128 0x2
	.byte	0x10
	.uleb128 0x2
	.long	0x9ec
	.long	0xabc
	.uleb128 0x3
	.long	0xacd
	.uleb128 0x1
	.long	0xeb
	.byte	0
	.byte	0
	.uleb128 0x5
	.long	0x9ec
	.uleb128 0x6
	.long	0xac8
	.uleb128 0x6
	.long	0x91e
	.uleb128 0x5
	.long	0xad2
	.uleb128 0x6
	.long	0x9e7
	.uleb128 0x5
	.long	0xadc
	.uleb128 0xf
	.ascii "PolicyWidget<RangeCheck>\0"
	.byte	0x4
	.byte	0x1
	.byte	0x5
	.byte	0x8
	.long	0xb9e
	.uleb128 0x8
	.ascii "value\0"
	.byte	0x1
	.byte	0x6
	.byte	0x9
	.long	0xeb
	.byte	0
	.uleb128 0x17
	.ascii "set\0"
	.byte	0x7
	.ascii "_ZN12PolicyWidgetI10RangeCheckE3setEi\0"
	.long	0xb4b
	.long	0xb56
	.uleb128 0x3
	.long	0xba3
	.uleb128 0x1
	.long	0xeb
	.byte	0
	.uleb128 0x1f
	.ascii "get\0"
	.ascii "_ZNK12PolicyWidgetI10RangeCheckE3getEv\0"
	.long	0xeb
	.long	0xb8e
	.long	0xb94
	.uleb128 0x3
	.long	0xbad
	.byte	0
	.uleb128 0x20
	.secrel32	.LASF5
	.long	0x8b3
	.byte	0
	.uleb128 0x5
	.long	0xae6
	.uleb128 0x6
	.long	0xae6
	.uleb128 0x5
	.long	0xba3
	.uleb128 0x6
	.long	0xb9e
	.uleb128 0x5
	.long	0xbad
	.uleb128 0xf
	.ascii "PolicyWidget<NoCheck>\0"
	.byte	0x4
	.byte	0x1
	.byte	0x5
	.byte	0x8
	.long	0xc64
	.uleb128 0x8
	.ascii "value\0"
	.byte	0x1
	.byte	0x6
	.byte	0x9
	.long	0xeb
	.byte	0
	.uleb128 0x17
	.ascii "set\0"
	.byte	0x7
	.ascii "_ZN12PolicyWidgetI7NoCheckE3setEi\0"
	.long	0xc15
	.long	0xc20
	.uleb128 0x3
	.long	0xc69
	.uleb128 0x1
	.long	0xeb
	.byte	0
	.uleb128 0x1f
	.ascii "get\0"
	.ascii "_ZNK12PolicyWidgetI7NoCheckE3getEv\0"
	.long	0xeb
	.long	0xc54
	.long	0xc5a
	.uleb128 0x3
	.long	0xc73
	.byte	0
	.uleb128 0x20
	.secrel32	.LASF5
	.long	0x8ec
	.byte	0
	.uleb128 0x5
	.long	0xbb7
	.uleb128 0x6
	.long	0xbb7
	.uleb128 0x5
	.long	0xc69
	.uleb128 0x6
	.long	0xc64
	.uleb128 0x5
	.long	0xc73
	.uleb128 0x18
	.secrel32	.LASF6
	.byte	0x14
	.long	0x9ec
	.long	0xd89
	.uleb128 0x21
	.long	0x9ec
	.uleb128 0xc
	.secrel32	.LASF6
	.ascii "_ZN12NoneStrategyC4EOS_\0"
	.long	0xcb5
	.long	0xcc0
	.uleb128 0x3
	.long	0xd8e
	.uleb128 0x1
	.long	0xd98
	.byte	0
	.uleb128 0xc
	.secrel32	.LASF6
	.ascii "_ZN12NoneStrategyC4ERKS_\0"
	.long	0xce6
	.long	0xcf1
	.uleb128 0x3
	.long	0xd8e
	.uleb128 0x1
	.long	0xd9d
	.byte	0
	.uleb128 0xc
	.secrel32	.LASF6
	.ascii "_ZN12NoneStrategyC4Ev\0"
	.long	0xd14
	.long	0xd1a
	.uleb128 0x3
	.long	0xd8e
	.byte	0
	.uleb128 0x22
	.secrel32	.LASF2
	.byte	0x14
	.ascii "_ZNK12NoneStrategy5checkEi\0"
	.uleb128 0x2
	.byte	0x10
	.uleb128 0x2
	.long	0xc7d
	.long	0xd4a
	.long	0xd55
	.uleb128 0x3
	.long	0xda2
	.uleb128 0x1
	.long	0xeb
	.byte	0
	.uleb128 0x23
	.ascii "~NoneStrategy\0"
	.ascii "_ZN12NoneStrategyD4Ev\0"
	.long	0xc7d
	.long	0xd82
	.uleb128 0x3
	.long	0xd8e
	.byte	0
	.byte	0
	.uleb128 0x5
	.long	0xc7d
	.uleb128 0x6
	.long	0xc7d
	.uleb128 0x5
	.long	0xd8e
	.uleb128 0x24
	.long	0xc7d
	.uleb128 0x19
	.long	0xd89
	.uleb128 0x6
	.long	0xd89
	.uleb128 0x5
	.long	0xda2
	.uleb128 0x18
	.secrel32	.LASF7
	.byte	0x13
	.long	0x9ec
	.long	0xebe
	.uleb128 0x21
	.long	0x9ec
	.uleb128 0xc
	.secrel32	.LASF7
	.ascii "_ZN13RangeStrategyC4EOS_\0"
	.long	0xde5
	.long	0xdf0
	.uleb128 0x3
	.long	0xec3
	.uleb128 0x1
	.long	0xecd
	.byte	0
	.uleb128 0xc
	.secrel32	.LASF7
	.ascii "_ZN13RangeStrategyC4ERKS_\0"
	.long	0xe17
	.long	0xe22
	.uleb128 0x3
	.long	0xec3
	.uleb128 0x1
	.long	0xed2
	.byte	0
	.uleb128 0xc
	.secrel32	.LASF7
	.ascii "_ZN13RangeStrategyC4Ev\0"
	.long	0xe46
	.long	0xe4c
	.uleb128 0x3
	.long	0xec3
	.byte	0
	.uleb128 0x22
	.secrel32	.LASF2
	.byte	0x13
	.ascii "_ZNK13RangeStrategy5checkEi\0"
	.uleb128 0x2
	.byte	0x10
	.uleb128 0x2
	.long	0xdac
	.long	0xe7d
	.long	0xe88
	.uleb128 0x3
	.long	0xed7
	.uleb128 0x1
	.long	0xeb
	.byte	0
	.uleb128 0x23
	.ascii "~RangeStrategy\0"
	.ascii "_ZN13RangeStrategyD4Ev\0"
	.long	0xdac
	.long	0xeb7
	.uleb128 0x3
	.long	0xec3
	.byte	0
	.byte	0
	.uleb128 0x5
	.long	0xdac
	.uleb128 0x6
	.long	0xdac
	.uleb128 0x5
	.long	0xec3
	.uleb128 0x24
	.long	0xdac
	.uleb128 0x19
	.long	0xebe
	.uleb128 0x6
	.long	0xebe
	.uleb128 0x5
	.long	0xed7
	.uleb128 0x6
	.long	0x9ec
	.uleb128 0x5
	.long	0xee1
	.uleb128 0x19
	.long	0xac8
	.uleb128 0x31
	.long	0xeb
	.long	0xefb
	.uleb128 0xb
	.byte	0
	.uleb128 0x6
	.long	0xf00
	.uleb128 0x1b
	.ascii "__vtbl_ptr_type\0"
	.long	0xef0
	.uleb128 0x4
	.ascii "puts\0"
	.word	0x26f
	.byte	0xf
	.long	0xeb
	.long	0xf2c
	.uleb128 0x1
	.long	0x418
	.byte	0
	.uleb128 0x12
	.long	0xc20
	.long	0xf4b
	.quad	.LFB66
	.quad	.LFE66-.LFB66
	.uleb128 0x1
	.byte	0x9c
	.long	0xf58
	.uleb128 0xd
	.secrel32	.LASF8
	.long	0xc78
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x13
	.long	0xbe5
	.long	0xf77
	.quad	.LFB65
	.quad	.LFE65-.LFB65
	.uleb128 0x1
	.byte	0x9c
	.long	0xf90
	.uleb128 0xd
	.secrel32	.LASF8
	.long	0xc6e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xa
	.ascii "v\0"
	.byte	0x7
	.byte	0x12
	.long	0xeb
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x12
	.long	0xb56
	.long	0xfaf
	.quad	.LFB64
	.quad	.LFE64-.LFB64
	.uleb128 0x1
	.byte	0x9c
	.long	0xfbc
	.uleb128 0xd
	.secrel32	.LASF8
	.long	0xbb2
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x13
	.long	0xb17
	.long	0xfdb
	.quad	.LFB63
	.quad	.LFE63-.LFB63
	.uleb128 0x1
	.byte	0x9c
	.long	0xff4
	.uleb128 0xd
	.secrel32	.LASF8
	.long	0xba8
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xa
	.ascii "v\0"
	.byte	0x7
	.byte	0x12
	.long	0xeb
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x32
	.ascii "main\0"
	.byte	0x1
	.byte	0x2d
	.byte	0x5
	.long	0xeb
	.quad	.LFB41
	.quad	.LFE41-.LFB41
	.uleb128 0x1
	.byte	0x9c
	.long	0x1032
	.uleb128 0x10
	.ascii "rs\0"
	.byte	0x2e
	.byte	0x13
	.long	0xdac
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.uleb128 0x10
	.ascii "ns\0"
	.byte	0x2f
	.byte	0x13
	.long	0xc7d
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.byte	0
	.uleb128 0x25
	.long	0xd55
	.byte	0x14
	.long	0x1040
	.long	0x104a
	.uleb128 0x14
	.secrel32	.LASF8
	.long	0xd93
	.byte	0
	.uleb128 0x15
	.long	0x1032
	.ascii "_ZN12NoneStrategyD0Ev\0"
	.long	0x107f
	.quad	.LFB62
	.quad	.LFE62-.LFB62
	.uleb128 0x1
	.byte	0x9c
	.long	0x1088
	.uleb128 0xe
	.long	0x1040
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x15
	.long	0x1032
	.ascii "_ZN12NoneStrategyD1Ev\0"
	.long	0x10bd
	.quad	.LFB61
	.quad	.LFE61-.LFB61
	.uleb128 0x1
	.byte	0x9c
	.long	0x10c6
	.uleb128 0xe
	.long	0x1040
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x25
	.long	0xe88
	.byte	0x13
	.long	0x10d4
	.long	0x10de
	.uleb128 0x14
	.secrel32	.LASF8
	.long	0xec8
	.byte	0
	.uleb128 0x15
	.long	0x10c6
	.ascii "_ZN13RangeStrategyD0Ev\0"
	.long	0x1114
	.quad	.LFB55
	.quad	.LFE55-.LFB55
	.uleb128 0x1
	.byte	0x9c
	.long	0x111d
	.uleb128 0xe
	.long	0x10d4
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x15
	.long	0x10c6
	.ascii "_ZN13RangeStrategyD1Ev\0"
	.long	0x1153
	.quad	.LFB54
	.quad	.LFE54-.LFB54
	.uleb128 0x1
	.byte	0x9c
	.long	0x115c
	.uleb128 0xe
	.long	0x10d4
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x26
	.long	0xa5f
	.long	0x1169
	.long	0x1173
	.uleb128 0x14
	.secrel32	.LASF8
	.long	0xee6
	.byte	0
	.uleb128 0x27
	.long	0x115c
	.ascii "_ZN8StrategyD2Ev\0"
	.long	0x11a3
	.quad	.LFB47
	.quad	.LFE47-.LFB47
	.uleb128 0x1
	.byte	0x9c
	.long	0x11ac
	.uleb128 0xe
	.long	0x1169
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x1a
	.ascii "strategy_demo\0"
	.byte	0x28
	.ascii "_Z13strategy_demoiPK8Strategy\0"
	.long	0xeb
	.quad	.LFB40
	.quad	.LFE40-.LFB40
	.uleb128 0x1
	.byte	0x9c
	.long	0x1219
	.uleb128 0xa
	.ascii "x\0"
	.byte	0x28
	.byte	0x17
	.long	0xeb
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xa
	.ascii "s\0"
	.byte	0x28
	.byte	0x2a
	.long	0xacd
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x10
	.ascii "w\0"
	.byte	0x29
	.byte	0x14
	.long	0x91e
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.byte	0
	.uleb128 0x1a
	.ascii "policy_demo_nocheck\0"
	.byte	0x23
	.ascii "_Z19policy_demo_nochecki\0"
	.long	0xeb
	.quad	.LFB36
	.quad	.LFE36-.LFB36
	.uleb128 0x1
	.byte	0x9c
	.long	0x127b
	.uleb128 0xa
	.ascii "x\0"
	.byte	0x23
	.byte	0x1d
	.long	0xeb
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x10
	.ascii "w\0"
	.byte	0x24
	.byte	0x1b
	.long	0xbb7
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.byte	0
	.uleb128 0x1a
	.ascii "policy_demo\0"
	.byte	0x1e
	.ascii "_Z11policy_demoi\0"
	.long	0xeb
	.quad	.LFB32
	.quad	.LFE32-.LFB32
	.uleb128 0x1
	.byte	0x9c
	.long	0x12cd
	.uleb128 0xa
	.ascii "x\0"
	.byte	0x1e
	.byte	0x15
	.long	0xeb
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x10
	.ascii "w\0"
	.byte	0x1f
	.byte	0x1e
	.long	0xae6
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.byte	0
	.uleb128 0x12
	.long	0x9b5
	.long	0x12ec
	.quad	.LFB31
	.quad	.LFE31-.LFB31
	.uleb128 0x1
	.byte	0x9c
	.long	0x12f9
	.uleb128 0xd
	.secrel32	.LASF8
	.long	0xae1
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x13
	.long	0x982
	.long	0x1318
	.quad	.LFB30
	.quad	.LFE30-.LFB30
	.uleb128 0x1
	.byte	0x9c
	.long	0x1331
	.uleb128 0xd
	.secrel32	.LASF8
	.long	0xad7
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xa
	.ascii "v\0"
	.byte	0x1a
	.byte	0x12
	.long	0xeb
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x26
	.long	0x945
	.long	0x133e
	.long	0x1352
	.uleb128 0x14
	.secrel32	.LASF8
	.long	0xad7
	.uleb128 0x33
	.ascii "p\0"
	.byte	0x1
	.byte	0x19
	.byte	0x24
	.long	0xacd
	.byte	0
	.uleb128 0x27
	.long	0x1331
	.ascii "_ZN14StrategyWidgetC1EPK8Strategy\0"
	.long	0x1393
	.quad	.LFB29
	.quad	.LFE29-.LFB29
	.uleb128 0x1
	.byte	0x9c
	.long	0x13a4
	.uleb128 0xe
	.long	0x133e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.long	0x1347
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x12
	.long	0xd1a
	.long	0x13c3
	.quad	.LFB26
	.quad	.LFE26-.LFB26
	.uleb128 0x1
	.byte	0x9c
	.long	0x13d8
	.uleb128 0xd
	.secrel32	.LASF8
	.long	0xda7
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x28
	.long	0xeb
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x13
	.long	0xe4c
	.long	0x13f7
	.quad	.LFB25
	.quad	.LFE25-.LFB25
	.uleb128 0x1
	.byte	0x9c
	.long	0x1410
	.uleb128 0xd
	.secrel32	.LASF8
	.long	0xedc
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xa
	.ascii "v\0"
	.byte	0x13
	.byte	0x32
	.long	0xeb
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x34
	.long	0x8fd
	.quad	.LFB24
	.quad	.LFE24-.LFB24
	.uleb128 0x1
	.byte	0x9c
	.long	0x1434
	.uleb128 0x28
	.long	0xeb
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x35
	.long	0x8c7
	.quad	.LFB23
	.quad	.LFE23-.LFB23
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0xa
	.ascii "v\0"
	.byte	0xb
	.byte	0x2b
	.long	0xeb
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.byte	0
	.section	.debug_abbrev,"dr"
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0x8
	.byte	0
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 4
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x18
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 5
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x8
	.byte	0
	.byte	0
	.uleb128 0xa
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0xb
	.uleb128 0x18
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0xc
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xd
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0xe
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0xf
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x10
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x11
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 16
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x12
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7a
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x13
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x14
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x15
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x16
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x17
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 10
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x18
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x19
	.uleb128 0x10
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1a
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 5
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1b
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1c
	.uleb128 0x39
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 5
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1d
	.uleb128 0x2e
	.byte	0
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x1e
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 33
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x1f
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 10
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x20
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x21
	.uleb128 0x1c
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0x21
	.sleb128 0
	.byte	0
	.byte	0
	.uleb128 0x22
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 40
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x4c
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x4d
	.uleb128 0x18
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x23
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x4c
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x24
	.uleb128 0x42
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x25
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x20
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x26
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x20
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x27
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7a
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x28
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x29
	.uleb128 0x11
	.byte	0x1
	.uleb128 0x25
	.uleb128 0x8
	.uleb128 0x13
	.uleb128 0xb
	.uleb128 0x90
	.uleb128 0xb
	.uleb128 0x91
	.uleb128 0x6
	.uleb128 0x3
	.uleb128 0x1f
	.uleb128 0x1b
	.uleb128 0x1f
	.uleb128 0x55
	.uleb128 0x17
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x10
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x2a
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x2b
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2c
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2d
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2e
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x2f
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x4c
	.uleb128 0xb
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x8b
	.uleb128 0xb
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x30
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x4c
	.uleb128 0xb
	.uleb128 0x4d
	.uleb128 0x18
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x31
	.uleb128 0x15
	.byte	0x1
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x32
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x33
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x34
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7a
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x35
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"dr"
	.long	0x12c
	.word	0x2
	.secrel32	.Ldebug_info0
	.byte	0x8
	.byte	0
	.word	0
	.word	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	.LFB23
	.quad	.LFE23-.LFB23
	.quad	.LFB24
	.quad	.LFE24-.LFB24
	.quad	.LFB25
	.quad	.LFE25-.LFB25
	.quad	.LFB26
	.quad	.LFE26-.LFB26
	.quad	.LFB29
	.quad	.LFE29-.LFB29
	.quad	.LFB30
	.quad	.LFE30-.LFB30
	.quad	.LFB31
	.quad	.LFE31-.LFB31
	.quad	.LFB47
	.quad	.LFE47-.LFB47
	.quad	.LFB54
	.quad	.LFE54-.LFB54
	.quad	.LFB55
	.quad	.LFE55-.LFB55
	.quad	.LFB61
	.quad	.LFE61-.LFB61
	.quad	.LFB62
	.quad	.LFE62-.LFB62
	.quad	.LFB63
	.quad	.LFE63-.LFB63
	.quad	.LFB64
	.quad	.LFE64-.LFB64
	.quad	.LFB65
	.quad	.LFE65-.LFB65
	.quad	.LFB66
	.quad	.LFE66-.LFB66
	.quad	0
	.quad	0
	.section	.debug_rnglists,"dr"
.Ldebug_ranges0:
	.long	.Ldebug_ranges3-.Ldebug_ranges2
.Ldebug_ranges2:
	.word	0x5
	.byte	0x8
	.byte	0
	.long	0
.LLRL0:
	.byte	0x7
	.quad	.Ltext0
	.uleb128 .Letext0-.Ltext0
	.byte	0x7
	.quad	.LFB23
	.uleb128 .LFE23-.LFB23
	.byte	0x7
	.quad	.LFB24
	.uleb128 .LFE24-.LFB24
	.byte	0x7
	.quad	.LFB25
	.uleb128 .LFE25-.LFB25
	.byte	0x7
	.quad	.LFB26
	.uleb128 .LFE26-.LFB26
	.byte	0x7
	.quad	.LFB29
	.uleb128 .LFE29-.LFB29
	.byte	0x7
	.quad	.LFB30
	.uleb128 .LFE30-.LFB30
	.byte	0x7
	.quad	.LFB31
	.uleb128 .LFE31-.LFB31
	.byte	0x7
	.quad	.LFB47
	.uleb128 .LFE47-.LFB47
	.byte	0x7
	.quad	.LFB54
	.uleb128 .LFE54-.LFB54
	.byte	0x7
	.quad	.LFB55
	.uleb128 .LFE55-.LFB55
	.byte	0x7
	.quad	.LFB61
	.uleb128 .LFE61-.LFB61
	.byte	0x7
	.quad	.LFB62
	.uleb128 .LFE62-.LFB62
	.byte	0x7
	.quad	.LFB63
	.uleb128 .LFE63-.LFB63
	.byte	0x7
	.quad	.LFB64
	.uleb128 .LFE64-.LFB64
	.byte	0x7
	.quad	.LFB65
	.uleb128 .LFE65-.LFB65
	.byte	0x7
	.quad	.LFB66
	.uleb128 .LFE66-.LFB66
	.byte	0
.Ldebug_ranges3:
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
.LASF3:
	.ascii "StrategyWidget\0"
.LASF7:
	.ascii "RangeStrategy\0"
.LASF2:
	.ascii "check\0"
.LASF8:
	.ascii "this\0"
.LASF5:
	.ascii "CheckingPolicy\0"
.LASF4:
	.ascii "Strategy\0"
.LASF6:
	.ascii "NoneStrategy\0"
	.section	.debug_line_str,"dr"
.LASF0:
	.ascii "Examples\\_ch140_policy_vs_strategy.cpp\0"
.LASF1:
	.ascii "C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible\0"
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	puts;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__cxa_pure_virtual;	.scl	2;	.type	32;	.endef
