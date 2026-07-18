	.file	"ch26_std_function_test.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6squarei
	.def	_Z6squarei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6squarei
_Z6squarei:
.LFB2494:
	.seh_endprologue
	imul	ecx, ecx
	mov	eax, ecx
	ret
	.seh_endproc
	.section	.text$_ZNSt17_Function_handlerIFiiEPS0_E9_M_invokeERKSt9_Any_dataOi,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt17_Function_handlerIFiiEPS0_E9_M_invokeERKSt9_Any_dataOi
	.def	_ZNSt17_Function_handlerIFiiEPS0_E9_M_invokeERKSt9_Any_dataOi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFiiEPS0_E9_M_invokeERKSt9_Any_dataOi
_ZNSt17_Function_handlerIFiiEPS0_E9_M_invokeERKSt9_Any_dataOi:
.LFB2532:
	.seh_endprologue
	mov	rax, rcx
	mov	ecx, DWORD PTR [rdx]
	rex.W jmp	[QWORD PTR [rax]]
	.seh_endproc
	.text
	.p2align 4
	.def	_Z12via_templateIZ4mainEUliE_EiT_i.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z12via_templateIZ4mainEUliE_EiT_i.constprop.0
_Z12via_templateIZ4mainEUliE_EiT_i.constprop.0:
.LFB2552:
	.seh_endprologue
	mov	eax, 25
	ret
	.seh_endproc
	.section	.text$_ZNSt17_Function_handlerIFiiEPS0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt17_Function_handlerIFiiEPS0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
	.def	_ZNSt17_Function_handlerIFiiEPS0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFiiEPS0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
_ZNSt17_Function_handlerIFiiEPS0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation:
.LFB2536:
	.seh_endprologue
	test	r8d, r8d
	je	.L6
	cmp	r8d, 1
	jne	.L11
	mov	QWORD PTR [rcx], rdx
.L9:
	xor	eax, eax
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	cmp	r8d, 2
	jne	.L9
	mov	rax, QWORD PTR [rdx]
	mov	QWORD PTR [rcx], rax
	jmp	.L9
	.p2align 4,,10
	.p2align 3
.L6:
	lea	rax, _ZTIPFiiE[rip]
	mov	QWORD PTR [rcx], rax
	xor	eax, eax
	ret
	.seh_endproc
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt14_Function_baseD2Ev
	.def	_ZNSt14_Function_baseD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14_Function_baseD2Ev
_ZNSt14_Function_baseD2Ev:
.LFB1044:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR 16[rcx]
	test	rax, rax
	je	.L12
	mov	r8d, 3
	mov	rdx, rcx
	call	rax
	nop
.L12:
	add	rsp, 40
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1044:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1044-.LLSDACSB1044
.LLSDACSB1044:
.LLSDACSE1044:
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.globl	_Z16via_std_functionRKSt8functionIFiiEEi
	.def	_Z16via_std_functionRKSt8functionIFiiEEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16via_std_functionRKSt8functionIFiiEEi
_Z16via_std_functionRKSt8functionIFiiEEi:
.LFB2495:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	DWORD PTR 44[rsp], edx
	cmp	QWORD PTR 16[rcx], 0
	je	.L19
	lea	rdx, 44[rsp]
	call	[QWORD PTR 24[rcx]]
	add	rsp, 56
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z16via_std_functionRKSt8functionIFiiEEi.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z16via_std_functionRKSt8functionIFiiEEi.cold
	.seh_stackalloc	56
	.seh_endprologue
_Z16via_std_functionRKSt8functionIFiiEEi.cold:
.L19:
	call	_ZSt25__throw_bad_function_callv
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.text
.LHOTE0:
	.p2align 4
	.globl	_Z15via_template_fpPFiiEi
	.def	_Z15via_template_fpPFiiEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15via_template_fpPFiiEi
_Z15via_template_fpPFiiEi:
.LFB2496:
	.seh_endprologue
	mov	rax, rcx
	mov	ecx, edx
	rex.W jmp	rax
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB1:
	.section	.text.startup,"x"
.LHOTB1:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2498:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	call	__main
	mov	edx, 5
	lea	rax, _Z6squarei[rip]
	lea	rcx, 48[rsp]
	mov	QWORD PTR 48[rsp], rax
	lea	rax, _ZNSt17_Function_handlerIFiiEPS0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation[rip]
	movq	xmm0, rax
	lea	rax, _ZNSt17_Function_handlerIFiiEPS0_E9_M_invokeERKSt9_Any_dataOi[rip]
	mov	QWORD PTR 56[rsp], 0
	movq	xmm1, rax
	mov	DWORD PTR 44[rsp], 0
	punpcklqdq	xmm0, xmm1
	movaps	XMMWORD PTR 64[rsp], xmm0
.LEHB0:
	call	_Z16via_std_functionRKSt8functionIFiiEEi
	mov	edx, 5
	lea	rcx, _Z6squarei[rip]
	mov	DWORD PTR 44[rsp], eax
	call	_Z15via_template_fpPFiiEi
.LEHE0:
	mov	DWORD PTR 44[rsp], eax
	lea	rcx, 48[rsp]
	mov	DWORD PTR 44[rsp], 25
	mov	esi, DWORD PTR 44[rsp]
	call	_ZNSt14_Function_baseD2Ev
	mov	eax, esi
	add	rsp, 88
	pop	rbx
	pop	rsi
	ret
.L23:
	mov	rsi, rax
	jmp	.L22
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2498:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2498-.LLSDACSB2498
.LLSDACSB2498:
	.uleb128 .LEHB0-.LFB2498
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L23-.LFB2498
	.uleb128 0
.LLSDACSE2498:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 88
	.seh_savereg	rsi, 96
	.seh_endprologue
main.cold:
.L22:
	lea	rcx, 48[rsp]
	call	_ZNSt14_Function_baseD2Ev
	mov	rcx, rsi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2498:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2498-.LLSDACSBC2498
.LLSDACSBC2498:
	.uleb128 .LEHB1-.LCOLDB1
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSEC2498:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.section	.text.startup,"x"
.LHOTE1:
	.globl	_ZTSFiiE
	.section	.rdata$_ZTSFiiE,"dr"
	.linkonce same_size
_ZTSFiiE:
	.ascii "FiiE\0"
	.globl	_ZTIFiiE
	.section	.rdata$_ZTIFiiE,"dr"
	.linkonce same_size
	.align 8
_ZTIFiiE:
	.quad	_ZTVN10__cxxabiv120__function_type_infoE+16
	.quad	_ZTSFiiE
	.globl	_ZTSPFiiE
	.section	.rdata$_ZTSPFiiE,"dr"
	.linkonce same_size
_ZTSPFiiE:
	.ascii "PFiiE\0"
	.globl	_ZTIPFiiE
	.section	.rdata$_ZTIPFiiE,"dr"
	.linkonce same_size
	.align 8
_ZTIPFiiE:
	.quad	_ZTVN10__cxxabiv119__pointer_type_infoE+16
	.quad	_ZTSPFiiE
	.long	0
	.space 4
	.quad	_ZTIFiiE
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZSt25__throw_bad_function_callv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
