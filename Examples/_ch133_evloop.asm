	.file	"_ch133_evloop.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E9_M_invokeERKSt9_Any_dataOi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E9_M_invokeERKSt9_Any_dataOi
_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E9_M_invokeERKSt9_Any_dataOi:
.LFB2716:
	.seh_endprologue
	mov	eax, DWORD PTR [rdx]
	add	DWORD PTR g_counter[rip], eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E9_M_invokeERKSt9_Any_dataOi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E9_M_invokeERKSt9_Any_dataOi
_ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E9_M_invokeERKSt9_Any_dataOi:
.LFB2725:
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
.LFB2728:
	.seh_endprologue
	test	r8d, r8d
	je	.L5
	cmp	r8d, 1
	je	.L6
	xor	eax, eax
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	xor	eax, eax
	mov	QWORD PTR [rcx], rdx
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	lea	rax, _ZTIZ8run_loopEUliE0_[rip]
	mov	QWORD PTR [rcx], rax
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation
_ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation:
.LFB2721:
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
	lea	rax, _ZTIZ8run_loopEUliE_[rip]
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
.LFB1647:
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
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1647:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1647-.LLSDACSB1647
.LLSDACSB1647:
.LLSDACSE1647:
	.section	.text$_ZNSt14_Function_baseD2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_insert\0"
	.section	.text$_ZN9EventLoop3addEiSt8functionIFviEE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN9EventLoop3addEiSt8functionIFviEE
	.def	_ZN9EventLoop3addEiSt8functionIFviEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9EventLoop3addEiSt8functionIFviEE
_ZN9EventLoop3addEiSt8functionIFviEE:
.LFB2565:
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
	movaps	XMMWORD PTR 80[rsp], xmm6
	.seh_savexmm	xmm6, 80
	.seh_endprologue
	mov	rsi, rcx
	mov	rcx, QWORD PTR 16[r8]
	mov	eax, edx
	mov	DWORD PTR 32[rsp], edx
	mov	QWORD PTR 40[rsp], 0
	mov	rdx, QWORD PTR 24[r8]
	mov	QWORD PTR 48[rsp], 0
	mov	QWORD PTR 56[rsp], 0
	test	rcx, rcx
	mov	QWORD PTR 64[rsp], rdx
	je	.L18
	movdqu	xmm2, XMMWORD PTR [r8]
	pxor	xmm0, xmm0
	mov	QWORD PTR 56[rsp], rcx
	movups	XMMWORD PTR 16[r8], xmm0
	movups	XMMWORD PTR 40[rsp], xmm2
.L18:
	mov	rbx, QWORD PTR 8[rsi]
	mov	r8, QWORD PTR 16[rsi]
	cmp	rbx, r8
	je	.L19
	mov	DWORD PTR [rbx], eax
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 8[rbx], 0
	mov	QWORD PTR 16[rbx], 0
	mov	QWORD PTR 24[rbx], 0
	test	rax, rax
	mov	QWORD PTR 32[rbx], rdx
	je	.L54
	movdqu	xmm3, XMMWORD PTR 40[rsp]
	mov	QWORD PTR 24[rbx], rax
	movups	XMMWORD PTR 8[rbx], xmm3
.L54:
	add	QWORD PTR 8[rsi], 40
.L17:
	movaps	xmm6, XMMWORD PTR 80[rsp]
	add	rsp, 96
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	movabs	r9, -3689348814741910323
	mov	rdi, QWORD PTR [rsi]
	mov	r12, rbx
	sub	r12, rdi
	mov	rcx, r12
	sar	rcx, 3
	imul	rcx, r9
	movabs	r9, 230584300921369395
	cmp	rcx, r9
	je	.L55
	cmp	rbx, rdi
	je	.L56
	lea	r9, [rcx+rcx]
	cmp	r9, rcx
	jb	.L35
	test	r9, r9
	jne	.L57
	mov	ecx, 40
	xor	ebp, ebp
	xor	r9d, r9d
.L27:
	add	r12, r9
	mov	DWORD PTR [r12], eax
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 8[r12], 0
	mov	QWORD PTR 16[r12], 0
	mov	QWORD PTR 24[r12], 0
	test	rax, rax
	mov	QWORD PTR 32[r12], rdx
	je	.L28
	movdqu	xmm5, XMMWORD PTR 40[rsp]
	pxor	xmm0, xmm0
	mov	QWORD PTR 24[r12], rax
	movups	XMMWORD PTR 56[rsp], xmm0
	movups	XMMWORD PTR 8[r12], xmm5
.L28:
	cmp	rbx, rdi
	je	.L29
	mov	rdx, rdi
	mov	rax, r9
	.p2align 4,,10
	.p2align 3
.L33:
	mov	ecx, DWORD PTR [rdx]
	mov	QWORD PTR 8[rax], 0
	mov	QWORD PTR 16[rax], 0
	mov	QWORD PTR 24[rax], 0
	mov	DWORD PTR [rax], ecx
	mov	rcx, QWORD PTR 32[rdx]
	mov	QWORD PTR 32[rax], rcx
	mov	rcx, QWORD PTR 24[rdx]
	test	rcx, rcx
	je	.L30
	movdqu	xmm1, XMMWORD PTR 8[rdx]
	mov	QWORD PTR 24[rax], rcx
	movups	XMMWORD PTR 8[rax], xmm1
.L30:
	add	rdx, 40
	add	rax, 40
	cmp	rbx, rdx
	jne	.L33
	lea	rax, -40[rbx]
	movabs	rdx, 922337203685477581
	sub	rax, rdi
	shr	rax, 3
	imul	rax, rdx
	movabs	rdx, 2305843009213693951
	and	rax, rdx
	lea	rax, [rax+rax*4]
	lea	rcx, 80[r9+rax*8]
.L29:
	movq	xmm6, r9
	movq	xmm4, rcx
	test	rdi, rdi
	punpcklqdq	xmm6, xmm4
	je	.L31
	mov	rdx, r8
	mov	rcx, rdi
	sub	rdx, rdi
	call	_ZdlPvy
.L31:
	mov	rax, QWORD PTR 56[rsp]
	movups	XMMWORD PTR [rsi], xmm6
	mov	QWORD PTR 16[rsi], rbp
	test	rax, rax
	je	.L17
	lea	rcx, 40[rsp]
	mov	r8d, 3
	mov	rdx, rcx
	call	rax
	nop
	movaps	xmm6, XMMWORD PTR 80[rsp]
	add	rsp, 96
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L56:
	add	rcx, 1
	jc	.L35
	movabs	rax, 230584300921369395
	cmp	rcx, rax
	cmova	rcx, rax
	lea	rbp, [rcx+rcx*4]
	sal	rbp, 3
.L26:
	mov	rcx, rbp
.LEHB0:
	call	_Znwy
	mov	r9, rax
	mov	r8, QWORD PTR 16[rsi]
	mov	eax, DWORD PTR 32[rsp]
	lea	rcx, 40[r9]
	add	rbp, r9
	mov	rdx, QWORD PTR 64[rsp]
	jmp	.L27
	.p2align 4,,10
	.p2align 3
.L35:
	movabs	rbp, 9223372036854775800
	jmp	.L26
.L57:
	movabs	rax, 230584300921369395
	cmp	r9, rax
	cmovbe	rax, r9
	imul	rbp, rax, 40
	jmp	.L26
.L55:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE0:
.L37:
	lea	rcx, 40[rsp]
	mov	rbx, rax
	call	_ZNSt14_Function_baseD2Ev
	mov	rcx, rbx
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2565:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2565-.LLSDACSB2565
.LLSDACSB2565:
	.uleb128 .LEHB0-.LFB2565
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L37-.LFB2565
	.uleb128 0
	.uleb128 .LEHB1-.LFB2565
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE2565:
	.section	.text$_ZN9EventLoop3addEiSt8functionIFviEE,"x"
	.linkonce discard
	.seh_endproc
	.text
	.p2align 4
	.globl	run_loop
	.def	run_loop;	.scl	2;	.type	32;	.endef
	.seh_proc	run_loop
run_loop:
.LFB2577:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	lea	rdi, _ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation[rip]
	mov	edx, 3
	lea	rax, _ZNSt17_Function_handlerIFviEZ8run_loopEUliE_E9_M_invokeERKSt9_Any_dataOi[rip]
	movq	xmm0, rdi
	movq	xmm1, rax
	punpcklqdq	xmm0, xmm1
	lea	rdi, 64[rsp]
	movaps	XMMWORD PTR 80[rsp], xmm0
	lea	rbx, 32[rsp]
	mov	r8, rdi
	mov	QWORD PTR 32[rsp], 0
	mov	QWORD PTR 40[rsp], 0
	mov	rcx, rbx
	mov	QWORD PTR 48[rsp], 0
	mov	QWORD PTR 56[rsp], 0
	mov	QWORD PTR 64[rsp], 0
	mov	QWORD PTR 72[rsp], 0
.LEHB2:
	call	_ZN9EventLoop3addEiSt8functionIFviEE
.LEHE2:
	mov	rax, QWORD PTR 80[rsp]
	test	rax, rax
	je	.L59
	mov	r8d, 3
	mov	rdx, rdi
	mov	rcx, rdi
	call	rax
.L59:
	lea	rdx, _ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E10_M_managerERSt9_Any_dataRKS3_St18_Manager_operation[rip]
	mov	r8, rdi
	mov	rcx, rbx
	mov	QWORD PTR 64[rsp], 0
	lea	rax, _ZNSt17_Function_handlerIFviEZ8run_loopEUliE0_E9_M_invokeERKSt9_Any_dataOi[rip]
	movq	xmm0, rdx
	mov	edx, 5
	mov	QWORD PTR 72[rsp], 0
	movq	xmm2, rax
	punpcklqdq	xmm0, xmm2
	movaps	XMMWORD PTR 80[rsp], xmm0
.LEHB3:
	call	_ZN9EventLoop3addEiSt8functionIFviEE
.LEHE3:
	mov	rax, QWORD PTR 80[rsp]
	test	rax, rax
	je	.L60
	mov	r8d, 3
	mov	rdx, rdi
	mov	rcx, rdi
	call	rax
.L60:
	mov	rbp, QWORD PTR 32[rsp]
	mov	rsi, QWORD PTR 40[rsp]
	cmp	rbp, rsi
	je	.L61
	mov	rbx, rbp
	.p2align 4,,10
	.p2align 3
.L63:
	cmp	QWORD PTR 24[rbx], 0
	je	.L62
	mov	eax, DWORD PTR [rbx]
	lea	rcx, 8[rbx]
	mov	rdx, rdi
	mov	DWORD PTR 64[rsp], eax
.LEHB4:
	call	[QWORD PTR 32[rbx]]
.LEHE4:
.L62:
	add	rbx, 40
	cmp	rsi, rbx
	jne	.L63
	mov	edi, DWORD PTR g_counter[rip]
	mov	rbx, rbp
	.p2align 4,,10
	.p2align 3
.L65:
	mov	rax, QWORD PTR 24[rbx]
	test	rax, rax
	je	.L64
	lea	rcx, 8[rbx]
	mov	r8d, 3
	mov	rdx, rcx
	call	rax
.L64:
	add	rbx, 40
	cmp	rsi, rbx
	jne	.L65
.L74:
	test	rbp, rbp
	je	.L58
	mov	rdx, QWORD PTR 48[rsp]
	mov	rcx, rbp
	sub	rdx, rbp
	call	_ZdlPvy
.L58:
	mov	eax, edi
	add	rsp, 104
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L61:
	mov	edi, DWORD PTR g_counter[rip]
	jmp	.L74
.L76:
	mov	rbx, rax
.L68:
	mov	rdi, QWORD PTR 32[rsp]
	mov	rbp, QWORD PTR 40[rsp]
	mov	rsi, rdi
.L70:
	cmp	rbp, rsi
	je	.L99
	mov	rax, QWORD PTR 24[rsi]
	test	rax, rax
	je	.L71
	lea	rcx, 8[rsi]
	mov	r8d, 3
	mov	rdx, rcx
	call	rax
.L71:
	add	rsi, 40
	jmp	.L70
.L77:
.L98:
	mov	rcx, rdi
	mov	rbx, rax
	call	_ZNSt14_Function_baseD2Ev
	jmp	.L68
.L75:
	jmp	.L98
.L99:
	mov	rdx, QWORD PTR 48[rsp]
	sub	rdx, rdi
	test	rdi, rdi
	je	.L73
	mov	rcx, rdi
	call	_ZdlPvy
.L73:
	mov	rcx, rbx
.LEHB5:
	call	_Unwind_Resume
	nop
.LEHE5:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2577:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2577-.LLSDACSB2577
.LLSDACSB2577:
	.uleb128 .LEHB2-.LFB2577
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L75-.LFB2577
	.uleb128 0
	.uleb128 .LEHB3-.LFB2577
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L77-.LFB2577
	.uleb128 0
	.uleb128 .LEHB4-.LFB2577
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L76-.LFB2577
	.uleb128 0
	.uleb128 .LEHB5-.LFB2577
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSE2577:
	.text
	.seh_endproc
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB2623:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rsi, 88[rsp]
	mov	rbx, rcx
	mov	QWORD PTR 88[rsp], rdx
	mov	ecx, 1
	mov	QWORD PTR 96[rsp], r8
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 40[rsp], rsi
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	mov	r8, rsi
	mov	rdx, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC1:
	.ascii "g_counter=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2661:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	call	run_loop
	lea	rcx, .LC1[rip]
	mov	edx, eax
	call	_Z6printfPKcz
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
