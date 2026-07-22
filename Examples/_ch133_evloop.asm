	.file	"_ch133_evloop.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E9_M_invokeERKSt9_Any_dataOi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E9_M_invokeERKSt9_Any_dataOi
_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E9_M_invokeERKSt9_Any_dataOi:
.LFB2612:
	.seh_endprologue
	mov	eax, DWORD PTR [rdx]
	add	DWORD PTR g_counter[rip], eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation:
.LFB2617:
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
	lea	rax, _ZTIZ8run_loopEUliE_[rip]
	mov	QWORD PTR [rcx], rax
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E9_M_invokeERKSt9_Any_dataOi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E9_M_invokeERKSt9_Any_dataOi
_ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E9_M_invokeERKSt9_Any_dataOi:
.LFB2621:
	.seh_endprologue
	mov	eax, DWORD PTR [rdx]
	add	eax, eax
	add	DWORD PTR g_counter[rip], eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
_ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation:
.LFB2624:
	.seh_endprologue
	test	r8d, r8d
	je	.L9
	cmp	r8d, 1
	je	.L10
	xor	eax, eax
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	xor	eax, eax
	mov	QWORD PTR [rcx], rdx
	ret
	.p2align 4,,10
	.p2align 3
.L9:
	lea	rax, _ZTIZ8run_loopEUliE0_[rip]
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
.LFB1748:
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
.LLSDA1748:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1748-.LLSDACSB1748
.LLSDACSB1748:
.LLSDACSE1748:
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_append\0"
	.section	.text$_ZN9EventLoop3addEiSt8functionIFviEE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN9EventLoop3addEiSt8functionIFviEE
	.def	_ZN9EventLoop3addEiSt8functionIFviEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9EventLoop3addEiSt8functionIFviEE
_ZN9EventLoop3addEiSt8functionIFviEE:
.LFB2488:
	push	r14
	.seh_pushreg	r14
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	pxor	xmm0, xmm0
	mov	rdi, QWORD PTR 24[r8]
	mov	rax, QWORD PTR 16[r8]
	mov	DWORD PTR 64[rsp], edx
	mov	r9, rcx
	mov	esi, edx
	mov	QWORD PTR 88[rsp], 0
	mov	QWORD PTR 96[rsp], rdi
	movups	XMMWORD PTR 72[rsp], xmm0
	test	rax, rax
	je	.L18
	movdqu	xmm2, XMMWORD PTR [r8]
	mov	QWORD PTR 88[rsp], rax
	pxor	xmm0, xmm0
	movups	XMMWORD PTR 16[r8], xmm0
	movups	XMMWORD PTR 72[rsp], xmm2
.L18:
	mov	rdx, QWORD PTR 8[r9]
	mov	r8, QWORD PTR 16[r9]
	cmp	rdx, r8
	je	.L19
	mov	rax, QWORD PTR 88[rsp]
	pxor	xmm0, xmm0
	mov	DWORD PTR [rdx], esi
	mov	QWORD PTR 24[rdx], 0
	mov	QWORD PTR 32[rdx], rdi
	movups	XMMWORD PTR 8[rdx], xmm0
	test	rax, rax
	je	.L47
	movdqu	xmm3, XMMWORD PTR 72[rsp]
	mov	QWORD PTR 24[rdx], rax
	movups	XMMWORD PTR 8[rdx], xmm3
.L47:
	add	QWORD PTR 8[r9], 40
.L17:
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	mov	r10, QWORD PTR [r9]
	mov	rax, rdx
	sub	rax, r10
	mov	rcx, rax
	mov	r14, rax
	movabs	rax, -3689348814741910323
	sar	rcx, 3
	imul	rcx, rax
	movabs	rax, 230584300921369395
	cmp	rcx, rax
	je	.L48
	test	rcx, rcx
	mov	eax, 1
	mov	QWORD PTR 56[rsp], r10
	cmovne	rax, rcx
	mov	QWORD PTR 160[rsp], r9
	mov	QWORD PTR 48[rsp], r8
	add	rax, rcx
	mov	QWORD PTR 40[rsp], rdx
	movabs	rcx, 230584300921369395
	cmp	rax, rcx
	cmova	rax, rcx
	lea	r11, [rax+rax*4]
	sal	r11, 3
	mov	rcx, r11
	mov	QWORD PTR 32[rsp], r11
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	rcx, QWORD PTR 88[rsp]
	pxor	xmm0, xmm0
	mov	DWORD PTR [rax+r14], esi
	mov	rbx, rax
	mov	r11, QWORD PTR 32[rsp]
	mov	rdx, QWORD PTR 40[rsp]
	mov	QWORD PTR 32[rax+r14], rdi
	test	rcx, rcx
	mov	r8, QWORD PTR 48[rsp]
	mov	r10, QWORD PTR 56[rsp]
	mov	QWORD PTR 24[rax+r14], 0
	mov	r9, QWORD PTR 160[rsp]
	movups	XMMWORD PTR 8[rax+r14], xmm0
	je	.L23
	movdqu	xmm4, XMMWORD PTR 72[rsp]
	mov	QWORD PTR 24[rax+r14], rcx
	pxor	xmm0, xmm0
	movups	XMMWORD PTR 88[rsp], xmm0
	movups	XMMWORD PTR 8[rax+r14], xmm4
.L23:
	cmp	rdx, r10
	je	.L29
	mov	rcx, r10
	mov	rax, rbx
	pxor	xmm0, xmm0
	.p2align 6
	.p2align 4
	.p2align 3
.L28:
	mov	esi, DWORD PTR [rcx]
	mov	QWORD PTR 24[rax], 0
	movups	XMMWORD PTR 8[rax], xmm0
	mov	DWORD PTR [rax], esi
	mov	rsi, QWORD PTR 32[rcx]
	mov	QWORD PTR 32[rax], rsi
	mov	rsi, QWORD PTR 24[rcx]
	test	rsi, rsi
	je	.L25
	movdqu	xmm1, XMMWORD PTR 8[rcx]
	mov	QWORD PTR 24[rax], rsi
	movups	XMMWORD PTR 8[rax], xmm1
.L25:
	add	rcx, 40
	add	rax, 40
	cmp	rdx, rcx
	jne	.L28
	lea	rax, -40[rdx]
	movabs	rdx, 922337203685477581
	sub	rax, r10
	shr	rax, 3
	imul	rax, rdx
	movabs	rdx, 2305843009213693951
	and	rax, rdx
	lea	rax, 5[rax+rax*4]
	lea	rsi, [rbx+rax*8]
.L24:
	add	rsi, 40
	test	r10, r10
	je	.L26
	mov	rdx, r8
	mov	rcx, r10
	mov	QWORD PTR 32[rsp], r11
	sub	rdx, r10
	mov	QWORD PTR 160[rsp], r9
	call	_ZdlPvy
	mov	r11, QWORD PTR 32[rsp]
	mov	r9, QWORD PTR 160[rsp]
.L26:
	mov	rax, QWORD PTR 88[rsp]
	mov	QWORD PTR [r9], rbx
	add	rbx, r11
	mov	QWORD PTR 8[r9], rsi
	mov	QWORD PTR 16[r9], rbx
	test	rax, rax
	je	.L17
	lea	rcx, 72[rsp]
	mov	r8d, 3
	mov	rdx, rcx
	call	rax
	nop
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L29:
	mov	rsi, rbx
	jmp	.L24
.L30:
	mov	rbx, rax
	jmp	.L27
.L48:
	lea	rcx, .LC0[rip]
.LEHB1:
	call	_ZSt20__throw_length_errorPKc
.LEHE1:
.L27:
	lea	rcx, 72[rsp]
	call	_ZNSt14_Function_baseD2Ev
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2488:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2488-.LLSDACSB2488
.LLSDACSB2488:
	.uleb128 .LEHB0-.LFB2488
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L30-.LFB2488
	.uleb128 0
	.uleb128 .LEHB1-.LFB2488
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L30-.LFB2488
	.uleb128 0
	.uleb128 .LEHB2-.LFB2488
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE2488:
	.section	.text$_ZN9EventLoop3addEiSt8functionIFviEE,"x"
	.linkonce discard
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4
	.globl	run_loop
	.def	run_loop;	.scl	2;	.type	32;	.endef
	.seh_proc	run_loop
run_loop:
.LFB2500:
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
	sub	rsp, 96
	.seh_stackalloc	96
	.seh_endprologue
	lea	rax, _ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E9_M_invokeERKSt9_Any_dataOi[rip]
	mov	edx, 3
	movq	xmm0, QWORD PTR .LC1[rip]
	movq	xmm1, rax
	punpcklqdq	xmm0, xmm1
	lea	rdi, 64[rsp]
	movaps	XMMWORD PTR 80[rsp], xmm0
	lea	rcx, 32[rsp]
	pxor	xmm0, xmm0
	mov	r8, rdi
	movaps	XMMWORD PTR 32[rsp], xmm0
	mov	QWORD PTR 56[rsp], 0
	mov	QWORD PTR 64[rsp], 0
	mov	QWORD PTR 72[rsp], 0
	mov	QWORD PTR 48[rsp], 0
.LEHB3:
	call	_ZN9EventLoop3addEiSt8functionIFviEE
.LEHE3:
	mov	rax, QWORD PTR 80[rsp]
	test	rax, rax
	je	.L50
	mov	r8d, 3
	mov	rdx, rdi
	mov	rcx, rdi
	call	rax
.L50:
	lea	rax, _ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E9_M_invokeERKSt9_Any_dataOi[rip]
	mov	r8, rdi
	mov	edx, 5
	movq	xmm0, QWORD PTR .LC2[rip]
	movq	xmm2, rax
	lea	rcx, 32[rsp]
	mov	QWORD PTR 64[rsp], 0
	mov	QWORD PTR 72[rsp], 0
	punpcklqdq	xmm0, xmm2
	movaps	XMMWORD PTR 80[rsp], xmm0
.LEHB4:
	call	_ZN9EventLoop3addEiSt8functionIFviEE
.LEHE4:
	mov	rax, QWORD PTR 80[rsp]
	mov	rbp, QWORD PTR 32[rsp]
	mov	rsi, QWORD PTR 40[rsp]
	mov	r12, QWORD PTR 48[rsp]
	test	rax, rax
	je	.L51
	mov	r8d, 3
	mov	rdx, rdi
	mov	rcx, rdi
	call	rax
.L51:
	cmp	rsi, rbp
	je	.L52
	mov	rbx, rbp
	.p2align 4
	.p2align 3
.L54:
	cmp	QWORD PTR 24[rbx], 0
	je	.L53
	mov	eax, DWORD PTR [rbx]
	lea	rcx, 8[rbx]
	mov	rdx, rdi
	mov	DWORD PTR 64[rsp], eax
.LEHB5:
	call	[QWORD PTR 32[rbx]]
.LEHE5:
.L53:
	add	rbx, 40
	cmp	rsi, rbx
	jne	.L54
	mov	edi, DWORD PTR g_counter[rip]
	mov	rbx, rbp
	.p2align 4
	.p2align 3
.L56:
	mov	rax, QWORD PTR 24[rbx]
	test	rax, rax
	je	.L55
	lea	rcx, 8[rbx]
	mov	r8d, 3
	mov	rdx, rcx
	call	rax
.L55:
	add	rbx, 40
	cmp	rsi, rbx
	jne	.L56
.L65:
	test	rbp, rbp
	je	.L49
	mov	rdx, r12
	mov	rcx, rbp
	sub	rdx, rbp
	call	_ZdlPvy
.L49:
	mov	eax, edi
	add	rsp, 96
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L52:
	mov	edi, DWORD PTR g_counter[rip]
	jmp	.L65
.L67:
	mov	rbx, rax
	jmp	.L59
.L68:
	mov	rbx, rax
	jmp	.L60
.L66:
	mov	rbx, rax
	jmp	.L58
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2500:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2500-.LLSDACSB2500
.LLSDACSB2500:
	.uleb128 .LEHB3-.LFB2500
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L66-.LFB2500
	.uleb128 0
	.uleb128 .LEHB4-.LFB2500
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L68-.LFB2500
	.uleb128 0
	.uleb128 .LEHB5-.LFB2500
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L67-.LFB2500
	.uleb128 0
.LLSDACSE2500:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	run_loop.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	run_loop.cold
	.seh_stackalloc	136
	.seh_savereg	rbx, 96
	.seh_savereg	rsi, 104
	.seh_savereg	rdi, 112
	.seh_savereg	rbp, 120
	.seh_savereg	r12, 128
	.seh_endprologue
run_loop.cold:
.L58:
	mov	rcx, rdi
	mov	rbp, QWORD PTR 32[rsp]
	mov	rsi, QWORD PTR 40[rsp]
	mov	r12, QWORD PTR 48[rsp]
	call	_ZNSt14_Function_baseD2Ev
.L59:
	mov	rdi, rbp
.L61:
	cmp	rsi, rdi
	je	.L89
	mov	rax, QWORD PTR 24[rdi]
	test	rax, rax
	je	.L62
	lea	rcx, 8[rdi]
	mov	r8d, 3
	mov	rdx, rcx
	call	rax
.L62:
	add	rdi, 40
	jmp	.L61
.L60:
	mov	rcx, rdi
	mov	rbp, QWORD PTR 32[rsp]
	mov	rsi, QWORD PTR 40[rsp]
	mov	r12, QWORD PTR 48[rsp]
	call	_ZNSt14_Function_baseD2Ev
	jmp	.L59
.L89:
	test	rbp, rbp
	je	.L64
	mov	rdx, r12
	mov	rcx, rbp
	sub	rdx, rbp
	call	_ZdlPvy
.L64:
	mov	rcx, rbx
.LEHB6:
	call	_Unwind_Resume
	nop
.LEHE6:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2500:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2500-.LLSDACSBC2500
.LLSDACSBC2500:
	.uleb128 .LEHB6-.LCOLDB3
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSEC2500:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.text
.LHOTE3:
	.section .rdata,"dr"
.LC4:
	.ascii "g_counter=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2558:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	call	run_loop
	lea	rcx, .LC4[rip]
	mov	edx, eax
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
_ZTIZ8run_loopEUliE_:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSZ8run_loopEUliE_
	.align 16
_ZTSZ8run_loopEUliE_:
	.ascii "*Z8run_loopEUliE_\0"
	.align 8
_ZTIZ8run_loopEUliE0_:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSZ8run_loopEUliE0_
	.align 16
_ZTSZ8run_loopEUliE0_:
	.ascii "*Z8run_loopEUliE0_\0"
	.globl	g_counter
	.bss
	.align 4
g_counter:
	.space 4
	.section .rdata,"dr"
	.align 8
.LC1:
	.quad	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
	.align 8
.LC2:
	.quad	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
