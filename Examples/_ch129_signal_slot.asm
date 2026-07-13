	.file	"_ch129_signal_slot.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZNSt17_Function_handlerIFviEZ4mainEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFviEZ4mainEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
_ZNSt17_Function_handlerIFviEZ4mainEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation:
.LFB3770:
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
.LFB3765:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	r8d, 18
	mov	ebx, DWORD PTR [rdx]
	lea	rdx, .LC0[rip]
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	edx, ebx
	call	_ZNSolsEi
	mov	r8d, 1
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	add	rsp, 32
	pop	rbx
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
.LFB2455:
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
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2455:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2455-.LLSDACSB2455
.LLSDACSB2455:
.LLSDACSE2455:
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
.LFB3630:
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
	.p2align 4,,10
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
	jmp	_ZdlPvy
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
.LLSDA3630:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3630-.LLSDACSB3630
.LLSDACSB3630:
.LLSDACSE3630:
	.section	.text$_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "vector::_M_realloc_insert\0"
	.section	.text$_ZNSt6vectorISt8functionIFviEESaIS2_EE17_M_realloc_insertIJS2_EEEvN9__gnu_cxx17__normal_iteratorIPS2_S4_EEDpOT_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorISt8functionIFviEESaIS2_EE17_M_realloc_insertIJS2_EEEvN9__gnu_cxx17__normal_iteratorIPS2_S4_EEDpOT_
	.def	_ZNSt6vectorISt8functionIFviEESaIS2_EE17_M_realloc_insertIJS2_EEEvN9__gnu_cxx17__normal_iteratorIPS2_S4_EEDpOT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt8functionIFviEESaIS2_EE17_M_realloc_insertIJS2_EEEvN9__gnu_cxx17__normal_iteratorIPS2_S4_EEDpOT_
_ZNSt6vectorISt8functionIFviEESaIS2_EE17_M_realloc_insertIJS2_EEEvN9__gnu_cxx17__normal_iteratorIPS2_S4_EEDpOT_:
.LFB3847:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	rdi, QWORD PTR 8[rcx]
	mov	r12, QWORD PTR [rcx]
	mov	rax, rdi
	mov	rsi, rdx
	mov	rbx, rdx
	sub	rax, r12
	mov	rbp, rcx
	mov	r14, r8
	movabs	rdx, 288230376151711743
	sar	rax, 5
	cmp	rax, rdx
	je	.L57
	mov	r15, rsi
	sub	r15, r12
	cmp	r12, rdi
	je	.L58
	lea	rdx, [rax+rax]
	cmp	rdx, rax
	jb	.L40
	test	rdx, rdx
	jne	.L59
	mov	ecx, 32
	xor	r13d, r13d
	xor	r9d, r9d
.L30:
	mov	rdx, QWORD PTR 24[r14]
	lea	rax, [r9+r15]
	mov	QWORD PTR [rax], 0
	mov	QWORD PTR 8[rax], 0
	mov	QWORD PTR 16[rax], 0
	mov	QWORD PTR 24[rax], rdx
	mov	rdx, QWORD PTR 16[r14]
	test	rdx, rdx
	je	.L31
	movdqu	xmm4, XMMWORD PTR [r14]
	pxor	xmm0, xmm0
	mov	QWORD PTR 16[rax], rdx
	movups	XMMWORD PTR 16[r14], xmm0
	movups	XMMWORD PTR [rax], xmm4
.L31:
	cmp	rsi, r12
	je	.L32
	mov	r8, rsi
	mov	rdx, r12
	mov	rax, r9
	sub	r8, r12
	.p2align 4,,10
	.p2align 3
.L38:
	mov	rcx, QWORD PTR 24[rdx]
	mov	QWORD PTR [rax], 0
	mov	QWORD PTR 8[rax], 0
	mov	QWORD PTR 16[rax], 0
	mov	QWORD PTR 24[rax], rcx
	mov	rcx, QWORD PTR 16[rdx]
	test	rcx, rcx
	je	.L33
	movdqu	xmm1, XMMWORD PTR [rdx]
	mov	QWORD PTR 16[rax], rcx
	movups	XMMWORD PTR [rax], xmm1
.L33:
	add	rdx, 32
	add	rax, 32
	cmp	rsi, rdx
	jne	.L38
	lea	rcx, 32[r9+r8]
.L32:
	cmp	rsi, rdi
	je	.L34
	mov	r8, rdi
	mov	rax, rcx
	sub	r8, rsi
	.p2align 4,,10
	.p2align 3
.L37:
	mov	rdx, QWORD PTR 24[rbx]
	mov	QWORD PTR [rax], 0
	mov	QWORD PTR 8[rax], 0
	mov	QWORD PTR 16[rax], 0
	mov	QWORD PTR 24[rax], rdx
	mov	rdx, QWORD PTR 16[rbx]
	test	rdx, rdx
	je	.L35
	movdqu	xmm2, XMMWORD PTR [rbx]
	mov	QWORD PTR 16[rax], rdx
	movups	XMMWORD PTR [rax], xmm2
.L35:
	add	rbx, 32
	add	rax, 32
	cmp	rdi, rbx
	jne	.L37
	add	rcx, r8
.L34:
	movq	xmm6, r9
	movq	xmm3, rcx
	test	r12, r12
	punpcklqdq	xmm6, xmm3
	je	.L36
	mov	rdx, QWORD PTR 16[rbp]
	mov	rcx, r12
	sub	rdx, r12
	call	_ZdlPvy
.L36:
	movups	XMMWORD PTR 0[rbp], xmm6
	mov	QWORD PTR 16[rbp], r13
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L40:
	movabs	r13, 9223372036854775776
.L29:
	mov	rcx, r13
	call	_Znwy
	lea	rcx, 32[rax]
	mov	r9, rax
	add	r13, rax
	jmp	.L30
	.p2align 4,,10
	.p2align 3
.L58:
	add	rax, 1
	jc	.L40
	movabs	rdx, 288230376151711743
	cmp	rax, rdx
	cmovbe	rdx, rax
	mov	r13, rdx
	sal	r13, 5
	jmp	.L29
.L59:
	movabs	rax, 288230376151711743
	cmp	rdx, rax
	cmova	rdx, rax
	sal	rdx, 5
	mov	r13, rdx
	jmp	.L29
.L57:
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3319:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	call	__main
	lea	rax, 47[rsp]
	pxor	xmm0, xmm0
	movaps	XMMWORD PTR 48[rsp], xmm0
	lea	rdx, _ZNSt17_Function_handlerIFviEZ4mainEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation[rip]
	mov	QWORD PTR 80[rsp], rax
	lea	rsi, 80[rsp]
	movq	xmm0, rdx
	xor	edx, edx
	mov	QWORD PTR 64[rsp], 0
	lea	rax, _ZNSt17_Function_handlerIFviEZ4mainEUliE_E9_M_invokeERKSt9_Any_dataOi[rip]
	mov	r8, rsi
	mov	QWORD PTR 88[rsp], 0
	lea	rbp, 48[rsp]
	movq	xmm1, rax
	mov	rcx, rbp
	punpcklqdq	xmm0, xmm1
	movaps	XMMWORD PTR 96[rsp], xmm0
.LEHB0:
	call	_ZNSt6vectorISt8functionIFviEESaIS2_EE17_M_realloc_insertIJS2_EEEvN9__gnu_cxx17__normal_iteratorIPS2_S4_EEDpOT_
.LEHE0:
	mov	rcx, rsi
	mov	rdi, QWORD PTR 56[rsp]
	call	_ZNSt14_Function_baseD2Ev
	mov	rbx, QWORD PTR 48[rsp]
	cmp	rdi, rbx
	je	.L61
	.p2align 4,,10
	.p2align 3
.L63:
	cmp	QWORD PTR 16[rbx], 0
	mov	DWORD PTR 80[rsp], 42
	je	.L70
	mov	rdx, rsi
	mov	rcx, rbx
.LEHB1:
	call	[QWORD PTR 24[rbx]]
	add	rbx, 32
	cmp	rdi, rbx
	jne	.L63
.L61:
	mov	rcx, rbp
	call	_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev
	xor	eax, eax
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L70:
	call	_ZSt25__throw_bad_function_callv
.LEHE1:
.L66:
	mov	rcx, rsi
	mov	rbx, rax
	call	_ZNSt14_Function_baseD2Ev
.L65:
	mov	rcx, rbp
	call	_ZNSt6vectorISt8functionIFviEESaIS2_EED1Ev
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
.LEHE2:
.L67:
	mov	rbx, rax
	jmp	.L65
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3319:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3319-.LLSDACSB3319
.LLSDACSB3319:
	.uleb128 .LEHB0-.LFB3319
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L66-.LFB3319
	.uleb128 0
	.uleb128 .LEHB1-.LFB3319
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L67-.LFB3319
	.uleb128 0
	.uleb128 .LEHB2-.LFB3319
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE3319:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 8
_ZTIZ4mainEUliE_:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSZ4mainEUliE_
	.align 8
_ZTSZ4mainEUliE_:
	.ascii "*Z4mainEUliE_\0"
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZSt25__throw_bad_function_callv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
