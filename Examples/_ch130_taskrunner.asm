	.file	"_ch130_taskrunner.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E9_M_invokeERKSt9_Any_data;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E9_M_invokeERKSt9_Any_data
_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E9_M_invokeERKSt9_Any_data:
.LFB2554:
	.seh_endprologue
	mov	eax, DWORD PTR [rcx]
	add	DWORD PTR _ZL9g_counter[rip], eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E10_M_managerERSt9_Any_dataRKS5_St18_Manager_operation;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E10_M_managerERSt9_Any_dataRKS5_St18_Manager_operation
_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E10_M_managerERSt9_Any_dataRKS5_St18_Manager_operation:
.LFB2558:
	.seh_endprologue
	test	r8d, r8d
	je	.L4
	cmp	r8d, 1
	jne	.L9
	mov	QWORD PTR [rcx], rdx
.L7:
	xor	eax, eax
	ret
	.p2align 4,,10
	.p2align 3
.L9:
	cmp	r8d, 2
	jne	.L7
	mov	eax, DWORD PTR [rdx]
	mov	DWORD PTR [rcx], eax
	jmp	.L7
	.p2align 4,,10
	.p2align 3
.L4:
	lea	rax, _ZTIZ8run_loopR10TaskRunneriEUlvE_[rip]
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
.LFB1067:
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
.LLSDA1067:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1067-.LLSDACSB1067
.LLSDACSB1067:
.LLSDACSE1067:
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	_Z8run_loopR10TaskRunneri
	.def	_Z8run_loopR10TaskRunneri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8run_loopR10TaskRunneri
_Z8run_loopR10TaskRunneri:
.LFB2508:
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
	add	rsp, -128
	.seh_stackalloc	128
	movaps	XMMWORD PTR 96[rsp], xmm6
	.seh_savexmm	xmm6, 96
	movaps	XMMWORD PTR 112[rsp], xmm7
	.seh_savexmm	xmm7, 112
	.seh_endprologue
	mov	rbx, rcx
	mov	ebp, edx
	test	edx, edx
	jle	.L16
	movq	xmm6, QWORD PTR .LC0[rip]
	lea	rax, _ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E9_M_invokeERKSt9_Any_data[rip]
	xor	esi, esi
	pxor	xmm7, xmm7
	movq	xmm4, rax
	punpcklqdq	xmm6, xmm4
	jmp	.L20
	.p2align 4,,10
	.p2align 3
.L17:
	mov	r8d, 3
	lea	rdx, 32[rsp]
	lea	rcx, 32[rsp]
	call	r9
.L19:
	lea	eax, 1[rsi]
	cmp	ebp, eax
	je	.L40
.L27:
	mov	esi, eax
.L20:
	mov	QWORD PTR 36[rsp], 0
	lea	r9, _ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E10_M_managerERSt9_Any_dataRKS5_St18_Manager_operation[rip]
	mov	DWORD PTR 44[rsp], 0
	mov	DWORD PTR 32[rsp], esi
	movaps	XMMWORD PTR 48[rsp], xmm6
	cmp	DWORD PTR 2056[rbx], 63
	jg	.L17
	movsxd	rax, DWORD PTR 2052[rbx]
	movdqa	xmm3, XMMWORD PTR 32[rsp]
	movaps	XMMWORD PTR 48[rsp], xmm7
	sal	rax, 5
	add	rax, rbx
	movdqu	xmm0, XMMWORD PTR 16[rax]
	movdqu	xmm2, XMMWORD PTR [rax]
	movups	XMMWORD PTR 16[rax], xmm6
	movups	XMMWORD PTR [rax], xmm3
	movq	r9, xmm0
	movaps	XMMWORD PTR 64[rsp], xmm2
	movaps	XMMWORD PTR 80[rsp], xmm0
	test	r9, r9
	je	.L41
	lea	rdx, 64[rsp]
	mov	r8d, 3
	lea	rcx, 64[rsp]
	call	r9
	mov	eax, DWORD PTR 2052[rbx]
	mov	r9, QWORD PTR 48[rsp]
	add	DWORD PTR 2056[rbx], 1
	add	eax, 1
	cdq
	shr	edx, 26
	add	eax, edx
	and	eax, 63
	sub	eax, edx
	mov	DWORD PTR 2052[rbx], eax
	test	r9, r9
	jne	.L17
	lea	eax, 1[rsi]
	cmp	ebp, eax
	jne	.L27
.L40:
	xor	ebp, ebp
	pxor	xmm7, xmm7
	pxor	xmm6, xmm6
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L42:
	add	eax, 1
	movdqu	xmm1, XMMWORD PTR [r9]
	movups	XMMWORD PTR 16[rbx+rdx], xmm6
	sub	ecx, 1
	cdq
	mov	DWORD PTR 2056[rbx], ecx
	lea	r12, 64[rsp]
	lea	rcx, 64[rsp]
	shr	edx, 26
	mov	QWORD PTR 80[rsp], r10
	add	eax, edx
	movaps	XMMWORD PTR 64[rsp], xmm1
	and	eax, 63
	sub	eax, edx
	mov	DWORD PTR 2048[rbx], eax
.LEHB0:
	call	r8
.LEHE0:
	mov	rax, QWORD PTR 80[rsp]
	test	rax, rax
	je	.L21
	mov	r8d, 3
	lea	rdx, 64[rsp]
	lea	rcx, 64[rsp]
	call	rax
.L21:
	cmp	esi, ebp
	je	.L16
	add	ebp, 1
.L24:
	mov	ecx, DWORD PTR 2056[rbx]
	test	ecx, ecx
	jle	.L21
	movsxd	rdx, DWORD PTR 2048[rbx]
	movaps	XMMWORD PTR 64[rsp], xmm7
	mov	QWORD PTR 80[rsp], 0
	mov	rax, rdx
	sal	rdx, 5
	lea	r9, [rbx+rdx]
	mov	r8, QWORD PTR 24[r9]
	mov	r10, QWORD PTR 16[r9]
	mov	QWORD PTR 88[rsp], r8
	test	r10, r10
	jne	.L42
	jmp	.L22
	.p2align 4,,10
	.p2align 3
.L16:
	mov	eax, DWORD PTR _ZL9g_counter[rip]
	movaps	xmm6, XMMWORD PTR 96[rsp]
	movaps	xmm7, XMMWORD PTR 112[rsp]
	sub	rsp, -128
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L41:
	mov	eax, DWORD PTR 2052[rbx]
	add	DWORD PTR 2056[rbx], 1
	add	eax, 1
	cdq
	shr	edx, 26
	add	eax, edx
	and	eax, 63
	sub	eax, edx
	mov	DWORD PTR 2052[rbx], eax
	jmp	.L19
.L36:
	jmp	.L37
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2508:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2508-.LLSDACSB2508
.LLSDACSB2508:
	.uleb128 .LEHB0-.LFB2508
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L36-.LFB2508
	.uleb128 0
.LLSDACSE2508:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z8run_loopR10TaskRunneri.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8run_loopR10TaskRunneri.cold
	.seh_stackalloc	168
	.seh_savereg	rbx, 128
	.seh_savereg	rsi, 136
	.seh_savereg	rdi, 144
	.seh_savereg	rbp, 152
	.seh_savexmm	xmm6, 96
	.seh_savexmm	xmm7, 112
	.seh_savereg	r12, 160
	.seh_endprologue
_Z8run_loopR10TaskRunneri.cold:
.L22:
	add	eax, 1
	mov	r8d, 64
	sub	ecx, 1
	cdq
	mov	DWORD PTR 2056[rbx], ecx
	lea	r12, 64[rsp]
	idiv	r8d
	mov	DWORD PTR 2048[rbx], edx
.LEHB1:
	call	_ZSt25__throw_bad_function_callv
.LEHE1:
.L29:
.L37:
	mov	rbx, rax
	mov	rcx, r12
	call	_ZNSt14_Function_baseD2Ev
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2508:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2508-.LLSDACSBC2508
.LLSDACSBC2508:
	.uleb128 .LEHB1-.LCOLDB1
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L29-.LCOLDB1
	.uleb128 0
	.uleb128 .LEHB2-.LCOLDB1
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC2508:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text.unlikely,"x"
.LCOLDB2:
	.section	.text.startup,"x"
.LHOTB2:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2512:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 2096
	.seh_stackalloc	2096
	.seh_endprologue
	lea	rsi, 32[rsp]
	lea	rbx, 2080[rsp]
	call	__main
	mov	rax, rsi
	pxor	xmm0, xmm0
	.p2align 5
	.p2align 4
	.p2align 3
.L44:
	mov	QWORD PTR 16[rax], 0
	add	rax, 32
	movaps	XMMWORD PTR -32[rax], xmm0
	mov	QWORD PTR -8[rax], 0
	cmp	rax, rbx
	jne	.L44
	mov	edx, 8
	mov	rcx, rsi
	mov	QWORD PTR 2080[rsp], 0
	mov	DWORD PTR 2088[rsp], 0
.LEHB3:
	call	_Z8run_loopR10TaskRunneri
.LEHE3:
	mov	edi, eax
	lea	rbx, 2016[rsi]
	jmp	.L49
	.p2align 4,,10
	.p2align 3
.L51:
	sub	rbx, 32
.L49:
	mov	rax, QWORD PTR 16[rbx]
	test	rax, rax
	je	.L48
	mov	r8d, 3
	mov	rdx, rbx
	mov	rcx, rbx
	call	rax
.L48:
	cmp	rbx, rsi
	jne	.L51
	mov	eax, edi
	add	rsp, 2096
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L52:
	mov	rdi, rax
	jmp	.L47
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2512:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2512-.LLSDACSB2512
.LLSDACSB2512:
	.uleb128 .LEHB3-.LFB2512
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L52-.LFB2512
	.uleb128 0
.LLSDACSE2512:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	2120
	.seh_savereg	rbx, 2096
	.seh_savereg	rsi, 2104
	.seh_savereg	rdi, 2112
	.seh_endprologue
main.cold:
.L47:
	sub	rbx, 32
	mov	rcx, rbx
	call	_ZNSt14_Function_baseD2Ev
	cmp	rbx, rsi
	jne	.L47
	mov	rcx, rdi
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2512:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2512-.LLSDACSBC2512
.LLSDACSBC2512:
	.uleb128 .LEHB4-.LCOLDB2
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSEC2512:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE2:
	.section	.text.startup,"x"
.LHOTE2:
	.section .rdata,"dr"
	.align 8
_ZTIZ8run_loopR10TaskRunneriEUlvE_:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSZ8run_loopR10TaskRunneriEUlvE_
	.align 32
_ZTSZ8run_loopR10TaskRunneriEUlvE_:
	.ascii "*Z8run_loopR10TaskRunneriEUlvE_\0"
.lcomm _ZL9g_counter,4,4
	.align 8
.LC0:
	.quad	_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E10_M_managerERSt9_Any_dataRKS5_St18_Manager_operation
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZSt25__throw_bad_function_callv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
