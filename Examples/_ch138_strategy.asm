	.file	"_ch138_strategy.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZNSt17_Function_handlerIFddEZ4mainEUldE_E9_M_invokeERKSt9_Any_dataOd;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFddEZ4mainEUldE_E9_M_invokeERKSt9_Any_dataOd
_ZNSt17_Function_handlerIFddEZ4mainEUldE_E9_M_invokeERKSt9_Any_dataOd:
.LFB5991:
	.seh_endprologue
	movsd	xmm0, QWORD PTR .LC0[rip]
	mulsd	xmm0, QWORD PTR [rdx]
	ret
	.seh_endproc
	.p2align 4
	.def	_ZNSt17_Function_handlerIFddEZ4mainEUldE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFddEZ4mainEUldE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
_ZNSt17_Function_handlerIFddEZ4mainEUldE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation:
.LFB5995:
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
.LFB7336:
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
.LFB1038:
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
.LLSDA1038:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1038-.LLSDACSB1038
.LLSDACSB1038:
.LLSDACSE1038:
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB6:
	.section	.text.startup,"x"
.LHOTB6:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5178:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	call	__main
	lea	rax, _ZNSt17_Function_handlerIFddEZ4mainEUldE_E9_M_invokeERKSt9_Any_dataOd[rip]
	lea	rcx, 64[rsp]
	movq	xmm0, QWORD PTR .LC5[rip]
	mov	QWORD PTR 80[rsp], 0
	movq	xmm2, rax
	mov	QWORD PTR 64[rsp], 0
	punpcklqdq	xmm0, xmm2
	mov	QWORD PTR 72[rsp], 0
	mov	QWORD PTR 32[rsp], 0
	mov	QWORD PTR 40[rsp], 0
	mov	QWORD PTR 88[rsp], 0
	movaps	XMMWORD PTR 48[rsp], xmm0
	call	_ZNSt14_Function_baseD2Ev
	cmp	QWORD PTR 48[rsp], 0
	je	.L18
	mov	rax, QWORD PTR .LC1[rip]
	lea	rbx, 32[rsp]
	lea	rdx, 64[rsp]
	mov	rcx, rbx
	mov	QWORD PTR 64[rsp], rax
.LEHB0:
	call	[QWORD PTR 56[rsp]]
	movapd	xmm1, xmm0
.L16:
	mov	rsi, QWORD PTR .refptr._ZSt4cout[rip]
	mov	rcx, rsi
	call	_ZNSo9_M_insertIdEERSoT_
	mov	edx, 10
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_c.isra.0
	movsd	xmm1, QWORD PTR .LC2[rip]
	mov	rcx, rsi
	call	_ZNSo9_M_insertIdEERSoT_
	mov	edx, 10
	mov	rcx, rax
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
	jmp	.L17
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5178:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5178-.LLSDACSB5178
.LLSDACSB5178:
	.uleb128 .LEHB0-.LFB5178
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L19-.LFB5178
	.uleb128 0
.LLSDACSE5178:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	120
	.seh_savereg	rbx, 104
	.seh_savereg	rsi, 112
	.seh_endprologue
main.cold:
.L17:
	mov	rcx, rbx
	call	_ZNSt14_Function_baseD2Ev
	mov	rcx, rsi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5178:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5178-.LLSDACSBC5178
.LLSDACSBC5178:
	.uleb128 .LEHB1-.LCOLDB6
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSEC5178:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE6:
	.section	.text.startup,"x"
.LHOTE6:
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
	.align 8
.LC5:
	.quad	_ZNSt17_Function_handlerIFddEZ4mainEUldE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
