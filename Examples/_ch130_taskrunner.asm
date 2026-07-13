	.file	"_ch130_taskrunner.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E9_M_invokeERKSt9_Any_data;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E9_M_invokeERKSt9_Any_data
_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E9_M_invokeERKSt9_Any_data:
.LFB2229:
	.seh_endprologue
	mov	eax, DWORD PTR [rcx]
	add	DWORD PTR _ZL9g_counter[rip], eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E10_M_managerERSt9_Any_dataRKS5_St18_Manager_operation;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E10_M_managerERSt9_Any_dataRKS5_St18_Manager_operation
_ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E10_M_managerERSt9_Any_dataRKS5_St18_Manager_operation:
.LFB2233:
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
.LFB480:
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
.LLSDA480:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE480-.LLSDACSB480
.LLSDACSB480:
.LLSDACSE480:
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z8run_loopR10TaskRunneri
	.def	_Z8run_loopR10TaskRunneri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8run_loopR10TaskRunneri
_Z8run_loopR10TaskRunneri:
.LFB2185:
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
	sub	rsp, 136
	.seh_stackalloc	136
	movaps	XMMWORD PTR 96[rsp], xmm6
	.seh_savexmm	xmm6, 96
	movaps	XMMWORD PTR 112[rsp], xmm7
	.seh_savexmm	xmm7, 112
	.seh_endprologue
	lea	r12, _ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E10_M_managerERSt9_Any_dataRKS5_St18_Manager_operation[rip]
	lea	rax, _ZNSt17_Function_handlerIFvvEZ8run_loopR10TaskRunneriEUlvE_E9_M_invokeERKSt9_Any_data[rip]
	movq	xmm6, r12
	movq	xmm7, rax
	punpcklqdq	xmm6, xmm7
	test	edx, edx
	mov	rbx, rcx
	mov	ebp, edx
	jle	.L16
	mov	eax, DWORD PTR 2056[rcx]
	lea	rdi, 32[rsp]
	xor	esi, esi
	pxor	xmm7, xmm7
	jmp	.L20
	.p2align 4,,10
	.p2align 3
.L17:
	mov	r8d, 3
	mov	rdx, rdi
	mov	rcx, rdi
	call	r9
	mov	eax, DWORD PTR 2056[rbx]
.L19:
	lea	edx, 1[rsi]
	cmp	ebp, edx
	je	.L36
.L27:
	mov	esi, edx
.L20:
	cmp	eax, 63
	mov	DWORD PTR 44[rsp], 0
	mov	r9, r12
	mov	QWORD PTR 36[rsp], 0
	mov	DWORD PTR 32[rsp], esi
	movaps	XMMWORD PTR 48[rsp], xmm6
	jg	.L17
	movsx	rdx, DWORD PTR 2052[rbx]
	movaps	XMMWORD PTR 48[rsp], xmm7
	movdqa	xmm3, XMMWORD PTR 32[rsp]
	mov	rcx, rdx
	sal	rdx, 5
	add	rdx, rbx
	mov	r9, QWORD PTR 16[rdx]
	movdqu	xmm2, XMMWORD PTR [rdx]
	movups	XMMWORD PTR [rdx], xmm3
	movdqu	xmm4, XMMWORD PTR 16[rdx]
	movups	XMMWORD PTR 16[rdx], xmm6
	movaps	XMMWORD PTR 64[rsp], xmm2
	test	r9, r9
	movaps	XMMWORD PTR 80[rsp], xmm4
	je	.L37
	lea	r13, 64[rsp]
	mov	r8d, 3
	mov	rdx, r13
	mov	rcx, r13
	call	r9
	mov	ecx, DWORD PTR 2052[rbx]
	mov	eax, DWORD PTR 2056[rbx]
	mov	r9, QWORD PTR 48[rsp]
	lea	edx, 1[rcx]
	mov	ecx, edx
	add	eax, 1
	sar	ecx, 31
	movd	xmm5, eax
	shr	ecx, 26
	add	edx, ecx
	and	edx, 63
	sub	edx, ecx
	test	r9, r9
	movd	xmm0, edx
	punpckldq	xmm0, xmm5
	movq	QWORD PTR 2052[rbx], xmm0
	jne	.L17
	lea	edx, 1[rsi]
	cmp	ebp, edx
	jne	.L27
	.p2align 4,,10
	.p2align 3
.L36:
	lea	rbp, 64[rsp]
	xor	edi, edi
	pxor	xmm6, xmm6
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L21:
	lea	edx, 1[rdi]
	cmp	esi, edi
	je	.L16
.L39:
	mov	eax, DWORD PTR 2056[rbx]
	mov	edi, edx
.L24:
	test	eax, eax
	jle	.L21
	mov	QWORD PTR 64[rsp], 0
	movsx	rcx, DWORD PTR 2048[rbx]
	mov	QWORD PTR 72[rsp], 0
	mov	QWORD PTR 80[rsp], 0
	mov	rdx, rcx
	sal	rcx, 5
	lea	r9, [rbx+rcx]
	mov	r10, QWORD PTR 16[r9]
	mov	r8, QWORD PTR 24[r9]
	test	r10, r10
	mov	QWORD PTR 88[rsp], r8
	je	.L38
	add	edx, 1
	movdqu	xmm1, XMMWORD PTR [r9]
	movups	XMMWORD PTR 16[rbx+rcx], xmm6
	sub	eax, 1
	mov	ecx, edx
	mov	QWORD PTR 80[rsp], r10
	mov	r13, rbp
	sar	ecx, 31
	movaps	XMMWORD PTR 64[rsp], xmm1
	shr	ecx, 26
	mov	DWORD PTR 2056[rbx], eax
	add	edx, ecx
	and	edx, 63
	sub	edx, ecx
	mov	rcx, rbp
	mov	DWORD PTR 2048[rbx], edx
.LEHB0:
	call	r8
.LEHE0:
	mov	rax, QWORD PTR 80[rsp]
	test	rax, rax
	je	.L21
	mov	rdx, rbp
	mov	r8d, 3
	mov	rcx, rbp
	call	rax
	lea	edx, 1[rdi]
	cmp	esi, edi
	jne	.L39
.L16:
	mov	eax, DWORD PTR _ZL9g_counter[rip]
	movaps	xmm6, XMMWORD PTR 96[rsp]
	movaps	xmm7, XMMWORD PTR 112[rsp]
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L38:
	lea	r13, 64[rsp]
	add	edx, 1
	sub	eax, 1
	mov	ecx, edx
	mov	DWORD PTR 2056[rbx], eax
	sar	ecx, 31
	shr	ecx, 26
	add	edx, ecx
	and	edx, 63
	sub	edx, ecx
	mov	DWORD PTR 2048[rbx], edx
.LEHB1:
	call	_ZSt25__throw_bad_function_callv
.LEHE1:
	.p2align 4,,10
	.p2align 3
.L37:
	add	ecx, 1
	add	eax, 1
	mov	edx, ecx
	movd	xmm5, eax
	sar	edx, 31
	shr	edx, 26
	add	ecx, edx
	and	ecx, 63
	sub	ecx, edx
	movd	xmm0, ecx
	punpckldq	xmm0, xmm5
	movq	QWORD PTR 2052[rbx], xmm0
	jmp	.L19
.L28:
	mov	rbx, rax
	mov	rcx, r13
	call	_ZNSt14_Function_baseD2Ev
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2185:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2185-.LLSDACSB2185
.LLSDACSB2185:
	.uleb128 .LEHB0-.LFB2185
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L28-.LFB2185
	.uleb128 0
	.uleb128 .LEHB1-.LFB2185
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L28-.LFB2185
	.uleb128 0
	.uleb128 .LEHB2-.LFB2185
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE2185:
	.text
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2189:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 2096
	.seh_stackalloc	2096
	.seh_endprologue
	call	__main
	lea	rsi, 32[rsp]
	lea	rbx, 2080[rsp]
	mov	rax, rsi
	.p2align 4,,10
	.p2align 3
.L41:
	mov	QWORD PTR [rax], 0
	add	rax, 32
	mov	QWORD PTR -24[rax], 0
	mov	QWORD PTR -16[rax], 0
	mov	QWORD PTR -8[rax], 0
	cmp	rax, rbx
	jne	.L41
	mov	edx, 8
	mov	rcx, rsi
	mov	QWORD PTR 2080[rsp], 0
	mov	DWORD PTR 2088[rsp], 0
.LEHB3:
	call	_Z8run_loopR10TaskRunneri
.LEHE3:
	lea	rbx, 2048[rsp]
	mov	edi, eax
	jmp	.L46
	.p2align 4,,10
	.p2align 3
.L48:
	mov	rbx, rax
.L46:
	mov	rax, QWORD PTR 16[rbx]
	test	rax, rax
	je	.L45
	mov	r8d, 3
	mov	rdx, rbx
	mov	rcx, rbx
	call	rax
.L45:
	lea	rax, -32[rbx]
	cmp	rbx, rsi
	jne	.L48
	mov	eax, edi
	add	rsp, 2096
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L49:
	mov	rdi, rax
.L44:
	sub	rbx, 32
	mov	rcx, rbx
	call	_ZNSt14_Function_baseD2Ev
	cmp	rbx, rsi
	jne	.L44
	mov	rcx, rdi
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2189:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2189-.LLSDACSB2189
.LLSDACSB2189:
	.uleb128 .LEHB3-.LFB2189
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L49-.LFB2189
	.uleb128 0
	.uleb128 .LEHB4-.LFB2189
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE2189:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 8
_ZTIZ8run_loopR10TaskRunneriEUlvE_:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSZ8run_loopR10TaskRunneriEUlvE_
	.align 32
_ZTSZ8run_loopR10TaskRunneriEUlvE_:
	.ascii "*Z8run_loopR10TaskRunneriEUlvE_\0"
.lcomm _ZL9g_counter,4,4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZSt25__throw_bad_function_callv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
