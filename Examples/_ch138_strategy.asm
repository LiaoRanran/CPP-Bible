	.file	"_ch138_strategy.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZNSt17_Function_handlerIFddEZ4mainEUldE_E9_M_invokeERKSt9_Any_dataOd;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFddEZ4mainEUldE_E9_M_invokeERKSt9_Any_dataOd
_ZNSt17_Function_handlerIFddEZ4mainEUldE_E9_M_invokeERKSt9_Any_dataOd:
.LFB4525:
	.seh_endprologue
	movsd	xmm0, QWORD PTR .LC0[rip]
	mulsd	xmm0, QWORD PTR [rdx]
	ret
	.seh_endproc
	.p2align 4
	.def	_ZNSt17_Function_handlerIFddEZ4mainEUldE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFddEZ4mainEUldE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
_ZNSt17_Function_handlerIFddEZ4mainEUldE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation:
.LFB4529:
	.seh_endprologue
	test	r8d, r8d
	je	.L4
	cmp	r8d, 1
	je	.L5
	xor	eax, eax
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	xor	eax, eax
	mov	QWORD PTR [rcx], rdx
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	lea	rax, _ZTIZ4mainEUldE_[rip]
	mov	QWORD PTR [rcx], rax
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_c.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_c.isra.0
_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_c.isra.0:
.LFB4679:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR -24[rax]
	mov	BYTE PTR 56[rsp], dl
	cmp	QWORD PTR 16[rcx+rax], 0
	je	.L8
	lea	rdx, 56[rsp]
	mov	r8d, 1
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	nop
.L7:
	add	rsp, 40
	ret
.L8:
	movsx	edx, BYTE PTR 56[rsp]
	call	_ZNSo3putEc
	jmp	.L7
	.seh_endproc
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt14_Function_baseD2Ev
	.def	_ZNSt14_Function_baseD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14_Function_baseD2Ev
_ZNSt14_Function_baseD2Ev:
.LFB1060:
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
.LLSDA1060:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1060-.LLSDACSB1060
.LLSDACSB1060:
.LLSDACSE1060:
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3949:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	call	__main
	lea	rsi, 64[rsp]
	pxor	xmm0, xmm0
	mov	QWORD PTR 32[rsp], 0
	lea	rax, _ZNSt17_Function_handlerIFddEZ4mainEUldE_E9_M_invokeERKSt9_Any_dataOd[rip]
	movaps	XMMWORD PTR 80[rsp], xmm0
	mov	rcx, rsi
	mov	QWORD PTR 40[rsp], 0
	movdqa	xmm2, XMMWORD PTR 32[rsp]
	movq	xmm3, rax
	mov	QWORD PTR 32[rsp], 0
	lea	rdx, _ZNSt17_Function_handlerIFddEZ4mainEUldE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation[rip]
	movq	xmm0, rdx
	movaps	XMMWORD PTR 64[rsp], xmm2
	mov	QWORD PTR 40[rsp], 0
	punpcklqdq	xmm0, xmm3
	movaps	XMMWORD PTR 48[rsp], xmm0
	call	_ZNSt14_Function_baseD2Ev
	cmp	QWORD PTR 48[rsp], 0
	je	.L18
	mov	rax, QWORD PTR .LC1[rip]
	lea	rbx, 32[rsp]
	mov	rdx, rsi
	mov	rcx, rbx
	mov	QWORD PTR 64[rsp], rax
.LEHB0:
	call	[QWORD PTR 56[rsp]]
	movapd	xmm1, xmm0
.L16:
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	mov	edx, 10
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_c.isra.0
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	movsd	xmm1, QWORD PTR .LC2[rip]
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	mov	edx, 10
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_c.isra.0
.LEHE0:
	mov	rcx, rbx
	call	_ZNSt14_Function_baseD2Ev
	xor	eax, eax
	add	rsp, 104
	pop	rbx
	pop	rsi
	ret
.L18:
	movsd	xmm1, QWORD PTR .LC1[rip]
	lea	rbx, 32[rsp]
	jmp	.L16
.L19:
	mov	rsi, rax
	mov	rcx, rbx
	call	_ZNSt14_Function_baseD2Ev
	mov	rcx, rsi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3949:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3949-.LLSDACSB3949
.LLSDACSB3949:
	.uleb128 .LEHB0-.LFB3949
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L19-.LFB3949
	.uleb128 0
	.uleb128 .LEHB1-.LFB3949
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE3949:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 8
_ZTIZ4mainEUldE_:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSZ4mainEUldE_
	.align 8
_ZTSZ4mainEUldE_:
	.ascii "*Z4mainEUldE_\0"
	.align 8
.LC0:
	.long	-515396076
	.long	1072829562
	.align 8
.LC1:
	.long	0
	.long	1079574528
	.align 8
.LC2:
	.long	0
	.long	1079410688
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
