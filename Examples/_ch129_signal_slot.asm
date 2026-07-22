	.file	"_ch129_signal_slot.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZNSt17_Function_handlerIFviEZ4mainEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFviEZ4mainEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
_ZNSt17_Function_handlerIFviEZ4mainEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation:
.LFB5850:
	.seh_endprologue
	test	r8d, r8d
	je	.L2
	cmp	r8d, 1
	jne	.L8
	mov	QWORD PTR [rcx], rdx
.L5:
	xor	eax, eax
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	cmp	r8d, 2
	jne	.L5
	mov	rax, QWORD PTR [rdx]
	mov	QWORD PTR [rcx], rax
	jmp	.L5
	.p2align 4,,10
	.p2align 3
.L2:
	lea	rax, _ZTIZ4mainEUliE_[rip]
	mov	QWORD PTR [rcx], rax
	xor	eax, eax
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "[slot] clicked at \0"
.LC1:
	.ascii "\12\0"
	.text
	.p2align 4
	.def	_ZNSt17_Function_handlerIFviEZ4mainEUliE_E9_M_invokeERKSt9_Any_dataOi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFviEZ4mainEUliE_E9_M_invokeERKSt9_Any_dataOi
_ZNSt17_Function_handlerIFviEZ4mainEUliE_E9_M_invokeERKSt9_Any_dataOi:
.LFB5845:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	r8d, 18
	mov	esi, DWORD PTR [rdx]
	mov	rcx, rbx
	lea	rdx, .LC0[rip]
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	edx, esi
	mov	rcx, rbx
	call	_ZNSolsEi
	mov	r8d, 1
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	.seh_endproc
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt14_Function_baseD2Ev
	.def	_ZNSt14_Function_baseD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14_Function_baseD2Ev
_ZNSt14_Function_baseD2Ev:
.LFB4478:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR 16[rcx]
	test	rax, rax
	je	.L10
	mov	r8d, 3
	mov	rdx, rcx
	call	rax
	nop
.L10:
	add	rsp, 40
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4478:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4478-.LLSDACSB4478
.LLSDACSB4478:
.LLSDACSE4478:
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev
	.def	_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev
_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev:
.LFB5612:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbx, QWORD PTR [rcx]
	mov	rdi, rcx
	cmp	rsi, rbx
	je	.L16
	.p2align 4
	.p2align 3
.L18:
	mov	rax, QWORD PTR 16[rbx]
	test	rax, rax
	je	.L17
	mov	r8d, 3
	mov	rdx, rbx
	mov	rcx, rbx
	call	rax
.L17:
	add	rbx, 32
	cmp	rsi, rbx
	jne	.L18
	mov	rbx, QWORD PTR [rdi]
.L16:
	test	rbx, rbx
	je	.L15
	mov	rdx, QWORD PTR 16[rdi]
	mov	rcx, rbx
	sub	rdx, rbx
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
.LEHB0:
	jmp	_ZdlPvy
.LEHE0:
	.p2align 4,,10
	.p2align 3
.L15:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5612:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5612-.LLSDACSB5612
.LLSDACSB5612:
	.uleb128 .LEHB0-.LFB5612
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
.LLSDACSE5612:
	.section	.text$_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB3:
	.section	.text.startup,"x"
.LHOTB3:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5183:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 136
	.seh_stackalloc	136
	.seh_endprologue
	lea	rsi, _ZNSt17_Function_handlerIFviEZ4mainEUliE_E9_M_invokeERKSt9_Any_dataOi[rip]
	call	__main
	pxor	xmm0, xmm0
	movq	xmm1, rsi
	lea	rax, 63[rsp]
	movaps	XMMWORD PTR 64[rsp], xmm0
	mov	ecx, 32
	movq	xmm0, QWORD PTR .LC2[rip]
	mov	QWORD PTR 80[rsp], 0
	punpcklqdq	xmm0, xmm1
	mov	QWORD PTR 96[rsp], rax
	mov	QWORD PTR 104[rsp], 0
	movaps	XMMWORD PTR 112[rsp], xmm0
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	QWORD PTR 24[rax], rsi
	mov	rbx, rax
	lea	rdx, 96[rsp]
	pxor	xmm0, xmm0
	movdqa	xmm2, XMMWORD PTR 96[rsp]
	lea	rsi, 32[rbx]
	mov	rcx, rdx
	mov	QWORD PTR 40[rsp], rdx
	mov	QWORD PTR 80[rsp], rsi
	movups	XMMWORD PTR [rax], xmm2
	lea	rax, _ZNSt17_Function_handlerIFviEZ4mainEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation[rip]
	mov	QWORD PTR 16[rbx], rax
	movaps	XMMWORD PTR 112[rsp], xmm0
	call	_ZNSt14_Function_baseD2Ev
	mov	DWORD PTR 96[rsp], 42
	cmp	QWORD PTR 16[rbx], 0
	je	.L32
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, rbx
.LEHB2:
	call	[QWORD PTR 24[rbx]]
.LEHE2:
	lea	rcx, 64[rsp]
	mov	QWORD PTR 64[rsp], rbx
	mov	QWORD PTR 72[rsp], rsi
	call	_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev
	xor	eax, eax
	add	rsp, 136
	pop	rbx
	pop	rsi
	ret
.L28:
	mov	rbx, rax
	jmp	.L26
.L30:
	jmp	.L27
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5183:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5183-.LLSDACSB5183
.LLSDACSB5183:
	.uleb128 .LEHB1-.LFB5183
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L28-.LFB5183
	.uleb128 0
	.uleb128 .LEHB2-.LFB5183
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L30-.LFB5183
	.uleb128 0
.LLSDACSE5183:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	152
	.seh_savereg	rbx, 136
	.seh_savereg	rsi, 144
	.seh_endprologue
main.cold:
.L32:
.LEHB3:
	call	_ZSt25__throw_bad_function_callv
.LEHE3:
.L26:
	lea	rcx, 96[rsp]
	xor	esi, esi
	call	_ZNSt14_Function_baseD2Ev
	mov	rax, rbx
	xor	ebx, ebx
.L27:
	lea	rcx, 64[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	QWORD PTR 64[rsp], rbx
	mov	QWORD PTR 72[rsp], rsi
	call	_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev
	mov	rcx, QWORD PTR 40[rsp]
.LEHB4:
	call	_Unwind_Resume
.LEHE4:
.L29:
	jmp	.L27
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5183:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5183-.LLSDACSBC5183
.LLSDACSBC5183:
	.uleb128 .LEHB3-.LCOLDB3
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L29-.LCOLDB3
	.uleb128 0
	.uleb128 .LEHB4-.LCOLDB3
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSEC5183:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.section	.text.startup,"x"
.LHOTE3:
	.section .rdata,"dr"
	.align 8
_ZTIZ4mainEUliE_:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSZ4mainEUliE_
	.align 8
_ZTSZ4mainEUliE_:
	.ascii "*Z4mainEUliE_\0"
	.align 8
.LC2:
	.quad	_ZNSt17_Function_handlerIFviEZ4mainEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt25__throw_bad_function_callv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
