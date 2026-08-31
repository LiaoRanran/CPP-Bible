	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNKSt5ctypeIcE8do_widenEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt5ctypeIcE8do_widenEc
	.def	_ZNKSt5ctypeIcE8do_widenEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt5ctypeIcE8do_widenEc
_ZNKSt5ctypeIcE8do_widenEc:
.LFB3035:
	.seh_endprologue
	mov	eax, edx
	ret
	.seh_endproc
	.text
	.p2align 4
	.def	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB7558:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR -24[rax]
	mov	rbx, rcx
	mov	rsi, QWORD PTR 240[rcx+rax]
	test	rsi, rsi
	je	.L8
	cmp	BYTE PTR 56[rsi], 0
	je	.L5
	movsx	edx, BYTE PTR 67[rsi]
.L6:
	mov	rcx, rbx
	call	_ZNSo3putEc
	mov	rcx, rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZNSo5flushEv
.L5:
	mov	rcx, rsi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rsi]
	mov	edx, 10
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L6
	mov	edx, 10
	mov	rcx, rsi
	call	rax
	movsx	edx, al
	jmp	.L6
.L8:
	call	_ZSt16__throw_bad_castv
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "basic_string::_M_create\0"
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc:
.LFB5641:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	cmp	rdx, 15
	mov	rsi, rcx
	mov	rbx, rdx
	mov	edi, r8d
	ja	.L18
	test	rdx, rdx
	jne	.L19
.L14:
	mov	rax, QWORD PTR [rsi]
	mov	QWORD PTR 8[rsi], rbx
	mov	BYTE PTR [rax+rbx], 0
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L18:
	test	rdx, rdx
	js	.L20
	mov	rcx, rdx
	add	rcx, 1
	js	.L21
	call	_Znwy
	mov	QWORD PTR 16[rsi], rbx
	mov	rcx, rax
	mov	QWORD PTR [rsi], rax
.L13:
	movsx	edx, dil
	mov	r8, rbx
	call	memset
	jmp	.L14
	.p2align 4,,10
	.p2align 3
.L19:
	cmp	rdx, 1
	mov	rcx, QWORD PTR [rcx]
	jne	.L13
	mov	BYTE PTR [rcx], r8b
	jmp	.L14
	.p2align 4,,10
	.p2align 3
.L21:
	call	_ZSt17__throw_bad_allocv
.L20:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv:
.LFB5671:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L22
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L22:
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC1:
	.ascii "cannot create std::vector larger than max_size()\0"
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EEC1EyRKS5_RKS6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EEC1EyRKS5_RKS6_.isra.0
_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EEC1EyRKS5_RKS6_.isra.0:
.LFB7564:
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
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	movabs	rax, 288230376151711743
	cmp	rax, rdx
	mov	r13, rcx
	mov	rdi, rdx
	mov	rbp, r8
	jb	.L51
	test	rdx, rdx
	pxor	xmm0, xmm0
	mov	QWORD PTR 16[rcx], 0
	movups	XMMWORD PTR [rcx], xmm0
	je	.L52
	mov	rbx, rdx
	sal	rbx, 5
	mov	rcx, rbx
.LEHB0:
	call	_Znwy
.LEHE0:
	movq	xmm1, rax
	add	rbx, rax
	mov	r14, rax
	movddup	xmm0, xmm1
	mov	QWORD PTR 16[r13], rbx
	mov	rsi, rax
	movups	XMMWORD PTR 0[r13], xmm0
	jmp	.L35
	.p2align 4,,10
	.p2align 3
.L28:
	cmp	rbx, 1
	jne	.L32
	movzx	eax, BYTE PTR [r12]
	mov	BYTE PTR 16[rsi], al
.L33:
	mov	QWORD PTR 8[rsi], rbx
	add	rsi, 32
	sub	rdi, 1
	mov	BYTE PTR [rcx+rbx], 0
	je	.L27
.L35:
	mov	rbx, QWORD PTR 8[rbp]
	lea	rcx, 16[rsi]
	mov	r12, QWORD PTR 0[rbp]
	mov	QWORD PTR [rsi], rcx
	cmp	rbx, 15
	jbe	.L28
	test	rbx, rbx
	js	.L53
	mov	rcx, rbx
	add	rcx, 1
	js	.L54
.LEHB1:
	call	_Znwy
	mov	rcx, rax
	mov	QWORD PTR [rsi], rax
	mov	QWORD PTR 16[rsi], rbx
.L31:
	mov	r8, rbx
	mov	rdx, r12
	call	memcpy
	mov	rcx, QWORD PTR [rsi]
	jmp	.L33
	.p2align 4,,10
	.p2align 3
.L32:
	test	rbx, rbx
	je	.L33
	jmp	.L31
.L52:
	xor	eax, eax
	xor	esi, esi
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 16[rcx], rax
.L27:
	mov	QWORD PTR 8[r13], rsi
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
.L54:
	call	_ZSt17__throw_bad_allocv
.LEHE1:
.L51:
	lea	rcx, .LC1[rip]
.LEHB2:
	call	_ZSt20__throw_length_errorPKc
.LEHE2:
.L53:
	lea	rcx, .LC0[rip]
.LEHB3:
	call	_ZSt20__throw_length_errorPKc
.LEHE3:
.L42:
	mov	rcx, rax
	call	__cxa_begin_catch
.L37:
	cmp	rsi, r14
	je	.L55
	mov	rcx, r14
	add	r14, 32
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	jmp	.L37
.L55:
.LEHB4:
	call	__cxa_rethrow
.LEHE4:
.L41:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rcx, QWORD PTR 0[r13]
	mov	rdx, QWORD PTR 16[r13]
	sub	rdx, rcx
	test	rcx, rcx
	je	.L40
	call	_ZdlPvy
.L40:
	mov	rcx, rbx
.LEHB5:
	call	_Unwind_Resume
	nop
.LEHE5:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA7564:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT7564-.LLSDATTD7564
.LLSDATTD7564:
	.byte	0x1
	.uleb128 .LLSDACSE7564-.LLSDACSB7564
.LLSDACSB7564:
	.uleb128 .LEHB0-.LFB7564
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB7564
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L42-.LFB7564
	.uleb128 0x1
	.uleb128 .LEHB2-.LFB7564
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB3-.LFB7564
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L42-.LFB7564
	.uleb128 0x1
	.uleb128 .LEHB4-.LFB7564
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L41-.LFB7564
	.uleb128 0
	.uleb128 .LEHB5-.LFB7564
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSE7564:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT7564:
	.text
	.seh_endproc
	.section	.text$_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	.def	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev:
.LFB6131:
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
	je	.L57
	.p2align 4,,10
	.p2align 3
.L59:
	mov	rcx, QWORD PTR [rbx]
	lea	rax, 16[rbx]
	cmp	rcx, rax
	je	.L58
	mov	rax, QWORD PTR 16[rbx]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L58:
	add	rbx, 32
	cmp	rsi, rbx
	jne	.L59
	mov	rbx, QWORD PTR [rdi]
.L57:
	test	rbx, rbx
	je	.L56
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
.L56:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "vector::reserve\0"
	.section	.text$_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE7reserveEy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE7reserveEy
	.def	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE7reserveEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE7reserveEy
_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE7reserveEy:
.LFB6135:
	push	r14
	.seh_pushreg	r14
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	movabs	rax, 288230376151711743
	cmp	rax, rdx
	mov	rbx, rcx
	jb	.L86
	mov	rcx, QWORD PTR [rcx]
	mov	rax, QWORD PTR 16[rbx]
	sub	rax, rcx
	sar	rax, 5
	cmp	rax, rdx
	jb	.L87
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L87:
	mov	rsi, QWORD PTR 8[rbx]
	mov	rdi, rdx
	sal	rdi, 5
	sub	rsi, rcx
	mov	rcx, rdi
	call	_Znwy
	mov	rdx, QWORD PTR 8[rbx]
	mov	r11, QWORD PTR [rbx]
	mov	rbp, rax
	cmp	rdx, r11
	je	.L77
	lea	rcx, 16[r11]
	sub	rdx, r11
	add	rdx, rax
	jmp	.L76
	.p2align 4,,10
	.p2align 3
.L68:
	mov	QWORD PTR [rax], r8
	mov	r8, QWORD PTR [rcx]
	mov	QWORD PTR 16[rax], r8
.L75:
	mov	QWORD PTR 8[rax], r10
	add	rax, 32
	add	rcx, 32
	cmp	rax, rdx
	je	.L77
.L76:
	lea	r9, 16[rax]
	mov	r10, QWORD PTR -8[rcx]
	mov	QWORD PTR [rax], r9
	mov	r8, QWORD PTR -16[rcx]
	cmp	rcx, r8
	jne	.L68
	lea	r8, 1[r10]
	cmp	r8d, 8
	jnb	.L69
	test	r8b, 4
	jne	.L88
	test	r8d, r8d
	je	.L75
	movzx	r10d, BYTE PTR [rcx]
	test	r8b, 2
	mov	BYTE PTR [r9], r10b
	jne	.L83
.L85:
	mov	r10, QWORD PTR -8[rcx]
	jmp	.L75
	.p2align 4,,10
	.p2align 3
.L77:
	test	r11, r11
	je	.L67
	mov	rdx, QWORD PTR 16[rbx]
	mov	rcx, r11
	sub	rdx, r11
	call	_ZdlPvy
.L67:
	add	rsi, rbp
	movq	xmm0, rbp
	add	rbp, rdi
	movq	xmm1, rsi
	mov	QWORD PTR 16[rbx], rbp
	punpcklqdq	xmm0, xmm1
	movups	XMMWORD PTR [rbx], xmm0
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L69:
	mov	r10d, r8d
	sub	r8d, 1
	mov	r12, QWORD PTR -8[rcx+r10]
	cmp	r8d, 8
	mov	QWORD PTR -8[r9+r10], r12
	jb	.L85
	and	r8d, -8
	xor	r10d, r10d
.L73:
	mov	r12d, r10d
	add	r10d, 8
	mov	r14, QWORD PTR [rcx+r12]
	cmp	r10d, r8d
	mov	QWORD PTR [r9+r12], r14
	jb	.L73
	mov	r10, QWORD PTR -8[rcx]
	jmp	.L75
.L88:
	mov	r10d, DWORD PTR [rcx]
	mov	r8d, r8d
	mov	DWORD PTR [r9], r10d
	mov	r10d, DWORD PTR -4[rcx+r8]
	mov	DWORD PTR -4[r9+r8], r10d
	mov	r10, QWORD PTR -8[rcx]
	jmp	.L75
.L83:
	mov	r8d, r8d
	movzx	r10d, WORD PTR -2[rcx+r8]
	mov	WORD PTR -2[r9+r8], r10w
	mov	r10, QWORD PTR -8[rcx]
	jmp	.L75
.L86:
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC3:
	.ascii "vector::_M_realloc_insert\0"
	.section	.text$_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE17_M_realloc_insertIJRKS5_EEEvN9__gnu_cxx17__normal_iteratorIPS5_S7_EEDpOT_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE17_M_realloc_insertIJRKS5_EEEvN9__gnu_cxx17__normal_iteratorIPS5_S7_EEDpOT_
	.def	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE17_M_realloc_insertIJRKS5_EEEvN9__gnu_cxx17__normal_iteratorIPS5_S7_EEDpOT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE17_M_realloc_insertIJRKS5_EEEvN9__gnu_cxx17__normal_iteratorIPS5_S7_EEDpOT_
_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE17_M_realloc_insertIJRKS5_EEEvN9__gnu_cxx17__normal_iteratorIPS5_S7_EEDpOT_:
.LFB6377:
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
	sub	rsp, 72
	.seh_stackalloc	72
	movaps	XMMWORD PTR 48[rsp], xmm6
	.seh_savexmm	xmm6, 48
	.seh_endprologue
	mov	rbp, QWORD PTR 8[rcx]
	mov	rsi, QWORD PTR [rcx]
	mov	rax, rbp
	mov	rbx, rdx
	mov	rdi, rcx
	movabs	rdx, 288230376151711743
	sub	rax, rsi
	mov	r14, r8
	sar	rax, 5
	cmp	rax, rdx
	je	.L154
	mov	r12, rbx
	sub	r12, rsi
	cmp	rsi, rbp
	je	.L155
	lea	r15, [rax+rax]
	cmp	r15, rax
	jb	.L129
	test	r15, r15
	jne	.L156
	xor	r13d, r13d
.L95:
	mov	rax, QWORD PTR [r14]
	add	r12, r13
	mov	r14, QWORD PTR 8[r14]
	lea	rcx, 16[r12]
	mov	QWORD PTR [r12], rcx
	mov	QWORD PTR 40[rsp], rax
	cmp	r14, 15
	ja	.L157
	cmp	r14, 1
	je	.L158
	test	r14, r14
	jne	.L99
.L101:
	cmp	rbx, rsi
	mov	QWORD PTR 8[r12], r14
	mov	BYTE PTR [rcx+r14], 0
	je	.L131
.L165:
	lea	rax, 16[rsi]
	mov	rdx, r13
	lea	r10, 16[rbx]
	jmp	.L112
	.p2align 4,,10
	.p2align 3
.L104:
	mov	QWORD PTR [rdx], rcx
	mov	rcx, QWORD PTR [rax]
	mov	QWORD PTR 16[rdx], rcx
.L111:
	add	rax, 32
	mov	QWORD PTR 8[rdx], r9
	add	rdx, 32
	cmp	r10, rax
	je	.L159
.L112:
	lea	r8, 16[rdx]
	mov	r9, QWORD PTR -8[rax]
	mov	QWORD PTR [rdx], r8
	mov	rcx, QWORD PTR -16[rax]
	cmp	rcx, rax
	jne	.L104
	lea	rcx, 1[r9]
	cmp	ecx, 8
	jnb	.L105
	test	cl, 4
	jne	.L160
	test	ecx, ecx
	je	.L111
	movzx	r9d, BYTE PTR [rax]
	test	cl, 2
	mov	BYTE PTR [r8], r9b
	jne	.L150
.L153:
	mov	r9, QWORD PTR -8[rax]
	jmp	.L111
	.p2align 4,,10
	.p2align 3
.L129:
	movabs	rcx, 9223372036854775776
	mov	r15, rdx
.L94:
.LEHB6:
	call	_Znwy
.LEHE6:
	mov	r13, rax
	jmp	.L95
	.p2align 4,,10
	.p2align 3
.L159:
	mov	rcx, rbx
	sub	rcx, rsi
	add	rcx, r13
.L103:
	add	rcx, 32
	cmp	rbx, rbp
	je	.L113
	lea	rax, 16[rbx]
	mov	rdx, rcx
	lea	r10, 16[rbp]
	jmp	.L122
	.p2align 4,,10
	.p2align 3
.L114:
	mov	r8, QWORD PTR [rax]
	mov	QWORD PTR [rdx], r11
	mov	QWORD PTR 16[rdx], r8
.L121:
	add	rax, 32
	mov	QWORD PTR 8[rdx], r9
	add	rdx, 32
	cmp	rax, r10
	je	.L161
.L122:
	mov	r11, QWORD PTR -16[rax]
	lea	r8, 16[rdx]
	mov	r9, QWORD PTR -8[rax]
	mov	QWORD PTR [rdx], r8
	cmp	r11, rax
	jne	.L114
	lea	r11, 1[r9]
	cmp	r11d, 8
	jnb	.L115
	test	r11b, 4
	jne	.L162
	test	r11d, r11d
	je	.L121
	movzx	r12d, BYTE PTR [rax]
	test	r11b, 2
	mov	BYTE PTR [r8], r12b
	je	.L121
	mov	r11d, r11d
	movzx	r12d, WORD PTR -2[rax+r11]
	mov	WORD PTR -2[r8+r11], r12w
	jmp	.L121
	.p2align 4,,10
	.p2align 3
.L161:
	sub	rbp, rbx
	add	rcx, rbp
.L113:
	movq	xmm6, r13
	movq	xmm0, rcx
	test	rsi, rsi
	punpcklqdq	xmm6, xmm0
	je	.L123
	mov	rdx, QWORD PTR 16[rdi]
	mov	rcx, rsi
	sub	rdx, rsi
	call	_ZdlPvy
.L123:
	mov	rax, r15
	movups	XMMWORD PTR [rdi], xmm6
	sal	rax, 5
	add	rax, r13
	mov	QWORD PTR 16[rdi], rax
	movaps	xmm6, XMMWORD PTR 48[rsp]
	add	rsp, 72
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
.L115:
	mov	r12d, r11d
	sub	r11d, 1
	mov	r14, QWORD PTR -8[rax+r12]
	cmp	r11d, 8
	mov	QWORD PTR -8[r8+r12], r14
	jb	.L121
	and	r11d, -8
	xor	r12d, r12d
	mov	QWORD PTR 40[rsp], rdx
.L119:
	mov	r14d, r12d
	add	r12d, 8
	mov	rdx, QWORD PTR [rax+r14]
	cmp	r12d, r11d
	mov	QWORD PTR [r8+r14], rdx
	jb	.L119
	mov	rdx, QWORD PTR 40[rsp]
	jmp	.L121
	.p2align 4,,10
	.p2align 3
.L105:
	mov	r9d, ecx
	sub	ecx, 1
	mov	r11, QWORD PTR -8[rax+r9]
	cmp	ecx, 8
	mov	QWORD PTR -8[r8+r9], r11
	jb	.L153
	and	ecx, -8
	xor	r9d, r9d
.L109:
	mov	r11d, r9d
	add	r9d, 8
	mov	r12, QWORD PTR [rax+r11]
	cmp	r9d, ecx
	mov	QWORD PTR [r8+r11], r12
	jb	.L109
	jmp	.L153
	.p2align 4,,10
	.p2align 3
.L155:
	add	rax, 1
	jc	.L129
	movabs	rdx, 288230376151711743
	cmp	rax, rdx
	cmovbe	rdx, rax
	mov	rcx, rdx
	mov	r15, rdx
	sal	rcx, 5
	jmp	.L94
	.p2align 4,,10
	.p2align 3
.L157:
	test	r14, r14
	js	.L163
	mov	rcx, r14
	add	rcx, 1
	js	.L164
.LEHB7:
	call	_Znwy
	mov	rcx, rax
	mov	QWORD PTR [r12], rax
	mov	QWORD PTR 16[r12], r14
.L99:
	mov	rdx, QWORD PTR 40[rsp]
	mov	r8, r14
	call	memcpy
	mov	rcx, QWORD PTR [r12]
	cmp	rbx, rsi
	mov	QWORD PTR 8[r12], r14
	mov	BYTE PTR [rcx+r14], 0
	jne	.L165
.L131:
	mov	rcx, r13
	jmp	.L103
	.p2align 4,,10
	.p2align 3
.L158:
	mov	rax, QWORD PTR 40[rsp]
	movzx	eax, BYTE PTR [rax]
	mov	BYTE PTR 16[r12], al
	jmp	.L101
.L162:
	mov	r12d, DWORD PTR [rax]
	mov	r11d, r11d
	mov	DWORD PTR [r8], r12d
	mov	r12d, DWORD PTR -4[rax+r11]
	mov	DWORD PTR -4[r8+r11], r12d
	jmp	.L121
.L160:
	mov	r9d, DWORD PTR [rax]
	mov	ecx, ecx
	mov	DWORD PTR [r8], r9d
	mov	r9d, DWORD PTR -4[rax+rcx]
	mov	DWORD PTR -4[r8+rcx], r9d
	mov	r9, QWORD PTR -8[rax]
	jmp	.L111
.L164:
	call	_ZSt17__throw_bad_allocv
.L150:
	mov	ecx, ecx
	movzx	r9d, WORD PTR -2[rax+rcx]
	mov	WORD PTR -2[r8+rcx], r9w
	mov	r9, QWORD PTR -8[rax]
	jmp	.L111
.L156:
	movabs	rax, 288230376151711743
	cmp	r15, rax
	cmova	r15, rax
	mov	rcx, r15
	sal	rcx, 5
	jmp	.L94
.L163:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE7:
.L154:
	lea	rcx, .LC3[rip]
.LEHB8:
	call	_ZSt20__throw_length_errorPKc
.LEHE8:
.L132:
	mov	rcx, rax
	call	__cxa_begin_catch
	test	r13, r13
	jne	.L125
	mov	rcx, r12
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L126:
.LEHB9:
	call	__cxa_rethrow
.LEHE9:
.L125:
	mov	rdx, r15
	mov	rcx, r13
	sal	rdx, 5
	call	_ZdlPvy
	jmp	.L126
.L133:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rcx, rbx
.LEHB10:
	call	_Unwind_Resume
	nop
.LEHE10:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA6377:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT6377-.LLSDATTD6377
.LLSDATTD6377:
	.byte	0x1
	.uleb128 .LLSDACSE6377-.LLSDACSB6377
.LLSDACSB6377:
	.uleb128 .LEHB6-.LFB6377
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB7-.LFB6377
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L132-.LFB6377
	.uleb128 0x1
	.uleb128 .LEHB8-.LFB6377
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB9-.LFB6377
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L133-.LFB6377
	.uleb128 0
	.uleb128 .LEHB10-.LFB6377
	.uleb128 .LEHE10-.LEHB10
	.uleb128 0
	.uleb128 0
.LLSDACSE6377:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT6377:
	.section	.text$_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE17_M_realloc_insertIJRKS5_EEEvN9__gnu_cxx17__normal_iteratorIPS5_S7_EEDpOT_,"x"
	.linkonce discard
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC4:
	.ascii "SSO capacity (string().capacity()) = \0"
.LC5:
	.ascii "build len15 ms = \0"
.LC7:
	.ascii "build len16 ms = \0"
	.align 8
.LC8:
	.ascii "C:\\Users\\ASUS\\AppData\\Local\\Temp\\tmpap_yas17\\s.cpp\0"
	.align 8
.LC9:
	.ascii "dst15.size() == M && dst16.size() == M\0"
.LC10:
	.ascii "copy len15 ms = \0"
.LC11:
	.ascii "copy len16 ms = \0"
	.align 8
.LC12:
	.ascii "o15.size() == M && o64.size() == M\0"
.LC13:
	.ascii "move len15 ms = \0"
.LC14:
	.ascii "move len64 ms = \0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5579:
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
	sub	rsp, 440
	.seh_stackalloc	440
	movaps	XMMWORD PTR 400[rsp], xmm6
	.seh_savexmm	xmm6, 400
	movaps	XMMWORD PTR 416[rsp], xmm7
	.seh_savexmm	xmm7, 416
	.seh_endprologue
	mov	r14d, 200000
	call	__main
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC4[rip]
	lea	r13, 384[rsp]
	mov	r12, r13
.LEHB11:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 15
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
.LEHE11:
	mov	DWORD PTR 140[rsp], 0
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	QWORD PTR 40[rsp], r13
	mov	QWORD PTR 56[rsp], rax
.L182:
	mov	QWORD PTR 368[rsp], r13
	mov	r15, QWORD PTR 40[rsp]
	mov	r13, r12
	xor	edi, edi
	mov	BYTE PTR 384[rsp], 0
	mov	esi, 97
	mov	QWORD PTR 376[rsp], 0
	jmp	.L179
	.p2align 4,,10
	.p2align 3
.L168:
	mov	BYTE PTR [r15+rdi], sil
	mov	rax, QWORD PTR 368[rsp]
	add	esi, 1
	cmp	sil, 112
	mov	QWORD PTR 376[rsp], rbx
	mov	BYTE PTR [rax+rbx], 0
	je	.L178
	mov	rdi, QWORD PTR 376[rsp]
	mov	r15, QWORD PTR 368[rsp]
.L179:
	lea	rbx, 1[rdi]
	cmp	r15, r12
	je	.L321
	mov	rbp, QWORD PTR 384[rsp]
	cmp	rbp, rbx
	jnb	.L168
	test	rbx, rbx
	js	.L322
	add	rbp, rbp
	cmp	rbx, rbp
	jb	.L323
	mov	rcx, rdi
	add	rcx, 2
	js	.L172
	mov	rbp, rbx
.L173:
.LEHB12:
	call	_Znwy
	test	rdi, rdi
	mov	r10, QWORD PTR 368[rsp]
	mov	r15, rax
	jne	.L169
.L174:
	cmp	r10, r12
	je	.L177
	mov	rax, QWORD PTR 384[rsp]
	mov	rcx, r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L177:
	mov	QWORD PTR 368[rsp], r15
	mov	QWORD PTR 384[rsp], rbp
	jmp	.L168
	.p2align 4,,10
	.p2align 3
.L321:
	cmp	rbx, 16
	jne	.L168
	mov	ecx, 31
	call	_Znwy
.LEHE12:
	mov	r10, QWORD PTR 368[rsp]
	mov	r15, rax
	mov	ebp, 30
.L169:
	cmp	rdi, 1
	je	.L324
	mov	rdx, r10
	mov	r8, rdi
	mov	rcx, r15
	mov	QWORD PTR 48[rsp], r10
	call	memcpy
	mov	r10, QWORD PTR 48[rsp]
	jmp	.L174
	.p2align 4,,10
	.p2align 3
.L178:
	mov	rcx, QWORD PTR 368[rsp]
	mov	eax, DWORD PTR 140[rsp]
	add	eax, DWORD PTR 376[rsp]
	cmp	rcx, r12
	mov	DWORD PTR 140[rsp], eax
	je	.L181
	mov	rax, QWORD PTR 384[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L181:
	sub	r14d, 1
	jne	.L182
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r14d, 200000
	mov	QWORD PTR 40[rsp], rax
.L199:
	xor	r10d, r10d
	mov	ecx, 31
	mov	QWORD PTR 368[rsp], r12
	mov	QWORD PTR 376[rsp], r10
	mov	BYTE PTR 384[rsp], 0
.LEHB13:
	call	_Znwy
	mov	rbx, rax
	mov	rax, QWORD PTR 376[rsp]
	mov	rsi, QWORD PTR 368[rsp]
	lea	r8, 1[rax]
	test	rax, rax
	je	.L325
	test	r8, r8
	je	.L184
	mov	rdx, rsi
	mov	rcx, rbx
	call	memcpy
.L184:
	cmp	rsi, r12
	je	.L185
	mov	rax, QWORD PTR 384[rsp]
	mov	rcx, rsi
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L185:
	mov	QWORD PTR 368[rsp], rbx
	mov	esi, 97
	mov	QWORD PTR 384[rsp], 30
	jmp	.L195
	.p2align 4,,10
	.p2align 3
.L188:
	mov	rax, QWORD PTR 368[rsp]
	mov	BYTE PTR [rax+rbx], sil
	mov	rax, QWORD PTR 368[rsp]
	add	esi, 1
	cmp	sil, 113
	mov	QWORD PTR 376[rsp], rdi
	mov	BYTE PTR 1[rax+rbx], 0
	je	.L326
.L195:
	mov	rbx, QWORD PTR 376[rsp]
	cmp	QWORD PTR 368[rsp], r12
	lea	rdi, 1[rbx]
	je	.L327
	mov	rax, QWORD PTR 384[rsp]
	cmp	rax, rdi
	jnb	.L188
	test	rdi, rdi
	js	.L328
	add	rax, rax
	mov	r13, rdi
	cmp	rdi, rax
	jb	.L187
.L190:
	mov	rcx, r13
	add	rcx, 1
	js	.L329
	call	_Znwy
.LEHE13:
	test	rbx, rbx
	mov	r15, QWORD PTR 368[rsp]
	mov	rbp, rax
	je	.L192
	cmp	rbx, 1
	je	.L330
	mov	r8, rbx
	mov	rdx, r15
	mov	rcx, rax
	call	memcpy
.L192:
	cmp	r15, r12
	je	.L194
	mov	rax, QWORD PTR 384[rsp]
	mov	rcx, r15
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L194:
	mov	QWORD PTR 368[rsp], rbp
	mov	QWORD PTR 384[rsp], r13
	jmp	.L188
	.p2align 4,,10
	.p2align 3
.L324:
	movzx	eax, BYTE PTR [r10]
	mov	BYTE PTR [r15], al
	jmp	.L174
.L323:
	test	rbp, rbp
	jns	.L331
.L172:
.LEHB14:
	call	_ZSt17__throw_bad_allocv
.LEHE14:
.L331:
	lea	rcx, 1[rbp]
	jmp	.L173
.L327:
	cmp	rdi, 16
	jne	.L188
	mov	eax, 30
.L187:
	movabs	r13, 9223372036854775807
	cmp	rax, r13
	cmovbe	r13, rax
	jmp	.L190
.L326:
	mov	rcx, QWORD PTR 368[rsp]
	mov	eax, DWORD PTR 140[rsp]
	add	eax, DWORD PTR 376[rsp]
	cmp	rcx, r12
	mov	DWORD PTR 140[rsp], eax
	je	.L198
	mov	rax, QWORD PTR 384[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L198:
	sub	r14d, 1
	jne	.L199
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC5[rip]
	lea	r15, 368[rsp]
	mov	rbx, rax
.LEHB15:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rsi, QWORD PTR 40[rsp]
	pxor	xmm1, xmm1
	mov	rdx, QWORD PTR 56[rsp]
	mov	rcx, rax
	movsd	xmm6, QWORD PTR .LC6[rip]
	mov	rax, rsi
	sub	rbx, rsi
	sub	rax, rdx
	cvtsi2sd	xmm1, rax
	divsd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC7[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	pxor	xmm1, xmm1
	cvtsi2sd	xmm1, rbx
	mov	rcx, rax
	divsd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	r8d, 120
	mov	rcx, r15
	mov	edx, 15
	mov	QWORD PTR 368[rsp], r12
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE15:
	lea	rax, 144[rsp]
	mov	r8, r15
	mov	edx, 100000
	mov	rcx, rax
	mov	QWORD PTR 56[rsp], rax
.LEHB16:
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EEC1EyRKS5_RKS6_.isra.0
.LEHE16:
	mov	rcx, r15
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	r8d, 120
	mov	rcx, r15
	mov	edx, 16
	mov	QWORD PTR 368[rsp], r12
.LEHB17:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE17:
	lea	rax, 176[rsp]
	mov	r8, r15
	mov	edx, 100000
	mov	rcx, rax
	mov	QWORD PTR 64[rsp], rax
.LEHB18:
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EEC1EyRKS5_RKS6_.isra.0
.LEHE18:
	lea	rdi, 208[rsp]
	mov	rcx, r15
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	xor	eax, eax
	mov	ecx, 6
	mov	edx, 100000
	rep stosd
	lea	rdi, 240[rsp]
	mov	ecx, 6
	mov	rsi, rdi
	mov	QWORD PTR 48[rsp], rdi
	rep stosd
	lea	rax, 208[rsp]
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], rax
.LEHB19:
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE7reserveEy
	mov	edx, 100000
	mov	rcx, rsi
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE7reserveEy
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r14, QWORD PTR 152[rsp]
	mov	rdi, QWORD PTR 144[rsp]
	mov	r13, rax
	jmp	.L200
.L334:
	mov	rsi, QWORD PTR 8[rdi]
	lea	rcx, 16[rbx]
	mov	QWORD PTR [rbx], rcx
	mov	rbp, QWORD PTR [rdi]
	cmp	rsi, 15
	ja	.L332
	cmp	rsi, 1
	jne	.L206
	movzx	eax, BYTE PTR 0[rbp]
	mov	BYTE PTR 16[rbx], al
.L207:
	mov	rax, QWORD PTR [rbx]
	mov	QWORD PTR 8[rbx], rsi
	add	rbx, 32
	mov	QWORD PTR 216[rsp], rbx
	mov	BYTE PTR [rax+rsi], 0
.L208:
	add	rdi, 32
.L200:
	cmp	rdi, r14
	je	.L333
	mov	rbx, QWORD PTR 216[rsp]
	cmp	rbx, QWORD PTR 224[rsp]
	jne	.L334
	mov	rcx, QWORD PTR 40[rsp]
	mov	r8, rdi
	mov	rdx, rbx
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE17_M_realloc_insertIJRKS5_EEEvN9__gnu_cxx17__normal_iteratorIPS5_S7_EEDpOT_
.LEHE19:
	jmp	.L208
.L330:
	movzx	eax, BYTE PTR [r15]
	mov	BYTE PTR 0[rbp], al
	jmp	.L192
.L329:
.LEHB20:
	call	_ZSt17__throw_bad_allocv
.LEHE20:
.L325:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [rbx], al
	jmp	.L184
.L322:
	lea	rcx, .LC0[rip]
.LEHB21:
	call	_ZSt20__throw_length_errorPKc
.LEHE21:
.L206:
	test	rsi, rsi
	je	.L207
.L205:
	mov	r8, rsi
	mov	rdx, rbp
	call	memcpy
	jmp	.L207
.L332:
	test	rsi, rsi
	js	.L335
	mov	rcx, rsi
	add	rcx, 1
	js	.L336
.LEHB22:
	call	_Znwy
	mov	rcx, rax
	mov	QWORD PTR [rbx], rax
	mov	QWORD PTR 16[rbx], rsi
	jmp	.L205
.L333:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rdi, QWORD PTR 176[rsp]
	mov	rbp, rax
	mov	rax, QWORD PTR 184[rsp]
	mov	QWORD PTR 72[rsp], rax
	jmp	.L210
.L339:
	mov	rsi, QWORD PTR 8[rdi]
	lea	rcx, 16[rbx]
	mov	QWORD PTR [rbx], rcx
	mov	r14, QWORD PTR [rdi]
	cmp	rsi, 15
	ja	.L337
	cmp	rsi, 1
	jne	.L216
	movzx	eax, BYTE PTR [r14]
	mov	BYTE PTR 16[rbx], al
.L217:
	mov	rax, QWORD PTR [rbx]
	mov	QWORD PTR 8[rbx], rsi
	add	rbx, 32
	mov	QWORD PTR 248[rsp], rbx
	mov	BYTE PTR [rax+rsi], 0
.L218:
	add	rdi, 32
.L210:
	cmp	QWORD PTR 72[rsp], rdi
	je	.L338
	mov	rbx, QWORD PTR 248[rsp]
	cmp	rbx, QWORD PTR 256[rsp]
	jne	.L339
	mov	rcx, QWORD PTR 48[rsp]
	mov	r8, rdi
	mov	rdx, rbx
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE17_M_realloc_insertIJRKS5_EEEvN9__gnu_cxx17__normal_iteratorIPS5_S7_EEDpOT_
	jmp	.L218
.L216:
	test	rsi, rsi
	je	.L217
.L215:
	mov	r8, rsi
	mov	rdx, r14
	call	memcpy
	jmp	.L217
.L337:
	test	rsi, rsi
	js	.L340
	mov	rcx, rsi
	add	rcx, 1
	js	.L341
	call	_Znwy
	mov	rcx, rax
	mov	QWORD PTR [rbx], rax
	mov	QWORD PTR 16[rbx], rsi
	jmp	.L215
.L338:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rbx, rax
	mov	rax, QWORD PTR 216[rsp]
	sub	rax, QWORD PTR 208[rsp]
	cmp	rax, 3200000
	jne	.L220
	mov	rax, QWORD PTR 248[rsp]
	sub	rax, QWORD PTR 240[rsp]
	cmp	rax, 3200000
	jne	.L220
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC10[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	rax, rbp
	pxor	xmm1, xmm1
	sub	rax, r13
	cvtsi2sd	xmm1, rax
	divsd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC11[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	sub	rbx, rbp
	pxor	xmm1, xmm1
	mov	rcx, rax
	cvtsi2sd	xmm1, rbx
	divsd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	r8d, 120
	mov	edx, 15
	mov	rcx, r15
	mov	QWORD PTR 368[rsp], r12
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE22:
	lea	rax, 272[rsp]
	mov	r8, r15
	mov	edx, 100000
	mov	rcx, rax
	mov	QWORD PTR 72[rsp], rax
.LEHB23:
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EEC1EyRKS5_RKS6_.isra.0
.LEHE23:
	mov	rcx, r15
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	r8d, 120
	mov	rcx, r15
	mov	edx, 64
	mov	QWORD PTR 368[rsp], r12
.LEHB24:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE24:
	lea	rax, 304[rsp]
	mov	r8, r15
	mov	edx, 100000
	mov	rcx, rax
	mov	QWORD PTR 80[rsp], rax
.LEHB25:
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EEC1EyRKS5_RKS6_.isra.0
.LEHE25:
	lea	rdi, 336[rsp]
	mov	rcx, r15
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	xor	eax, eax
	mov	ecx, 6
	mov	edx, 100000
	rep stosd
	mov	ecx, 6
	mov	rdi, r15
	rep stosd
	lea	rax, 336[rsp]
	mov	rcx, rax
	mov	QWORD PTR 88[rsp], rax
.LEHB26:
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE7reserveEy
	mov	edx, 100000
	mov	rcx, r15
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE7reserveEy
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	QWORD PTR 112[rsp], rax
	mov	rax, QWORD PTR 280[rsp]
	mov	QWORD PTR 96[rsp], rax
	mov	rax, QWORD PTR 272[rsp]
	lea	rbx, 16[rax]
	jmp	.L222
.L344:
	lea	rdx, 16[rbp]
	mov	rax, QWORD PTR -8[rbx]
	mov	QWORD PTR 0[rbp], rdx
	mov	rcx, QWORD PTR -16[rbx]
	cmp	rbx, rcx
	je	.L342
	mov	rdx, QWORD PTR [rbx]
	mov	QWORD PTR 0[rbp], rcx
	mov	QWORD PTR 16[rbp], rdx
.L225:
	mov	QWORD PTR 8[rbp], rax
	xor	r9d, r9d
	add	rbp, 32
	mov	QWORD PTR -16[rbx], rbx
	mov	QWORD PTR -8[rbx], r9
	mov	BYTE PTR [rbx], 0
	mov	QWORD PTR 344[rsp], rbp
.L226:
	add	rbx, 32
.L222:
	lea	rax, -16[rbx]
	cmp	QWORD PTR 96[rsp], rax
	je	.L343
	mov	rbp, QWORD PTR 344[rsp]
	mov	r14, QWORD PTR 352[rsp]
	cmp	rbp, r14
	jne	.L344
	mov	r13, QWORD PTR 336[rsp]
	mov	rsi, rbp
	movabs	rdx, 288230376151711743
	sub	rsi, r13
	mov	rax, rsi
	sar	rax, 5
	cmp	rax, rdx
	je	.L345
	cmp	rbp, r13
	je	.L228
	lea	r12, [rax+rax]
	cmp	r12, rax
	jb	.L279
	xor	eax, eax
	test	r12, r12
	jne	.L268
.L230:
	lea	rdx, [rax+rsi]
	mov	rcx, QWORD PTR -8[rbx]
	lea	r8, 16[rdx]
	mov	QWORD PTR [rdx], r8
	mov	r9, QWORD PTR -16[rbx]
	cmp	rbx, r9
	je	.L346
	mov	r8, QWORD PTR [rbx]
	mov	QWORD PTR [rdx], r9
	mov	QWORD PTR 16[rdx], r8
.L232:
	xor	r8d, r8d
	mov	QWORD PTR 8[rdx], rcx
	mov	rdx, r13
	mov	QWORD PTR -8[rbx], r8
	mov	r8, rax
	mov	QWORD PTR -16[rbx], rbx
	mov	BYTE PTR [rbx], 0
	jmp	.L233
.L234:
	mov	r9, QWORD PTR 16[rdx]
	mov	QWORD PTR [r8], rsi
	mov	QWORD PTR 16[r8], r9
.L235:
	mov	QWORD PTR 8[r8], rcx
	add	rdx, 32
	add	r8, 32
.L233:
	cmp	rbp, rdx
	je	.L347
	lea	r9, 16[r8]
	mov	rcx, QWORD PTR 8[rdx]
	mov	QWORD PTR [r8], r9
	mov	rsi, QWORD PTR [rdx]
	lea	r10, 16[rdx]
	cmp	rsi, r10
	jne	.L234
	add	ecx, 1
	mov	rdi, r9
	rep movsb
	mov	rcx, QWORD PTR 8[rdx]
	jmp	.L235
.L347:
	sub	rbp, r13
	movq	xmm7, rax
	test	r13, r13
	lea	rdx, 32[rax+rbp]
	movq	xmm0, rdx
	punpcklqdq	xmm7, xmm0
	je	.L237
	mov	rdx, r14
	mov	rcx, r13
	mov	QWORD PTR 104[rsp], rax
	sub	rdx, r13
	call	_ZdlPvy
	mov	rax, QWORD PTR 104[rsp]
.L237:
	sal	r12, 5
	movaps	XMMWORD PTR 336[rsp], xmm7
	add	rax, r12
	mov	QWORD PTR 352[rsp], rax
	jmp	.L226
.L346:
	add	ecx, 1
	mov	rdi, r8
	mov	rsi, rbx
	rep movsb
	mov	rcx, QWORD PTR -8[rbx]
	jmp	.L232
.L228:
	add	rax, 1
	mov	r12, rax
	jc	.L279
.L268:
	movabs	rax, 288230376151711743
	cmp	r12, rax
	cmova	r12, rax
.L229:
	mov	rcx, r12
	sal	rcx, 5
	call	_Znwy
	jmp	.L230
.L279:
	movabs	r12, 288230376151711743
	jmp	.L229
.L345:
	lea	rcx, .LC3[rip]
	call	_ZSt20__throw_length_errorPKc
.L343:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	QWORD PTR 96[rsp], rax
	mov	rax, QWORD PTR 312[rsp]
	mov	QWORD PTR 104[rsp], rax
	mov	rax, QWORD PTR 304[rsp]
	lea	rbx, 16[rax]
	jmp	.L239
.L350:
	lea	rdx, 16[rbp]
	mov	rax, QWORD PTR -8[rbx]
	mov	QWORD PTR 0[rbp], rdx
	mov	rcx, QWORD PTR -16[rbx]
	cmp	rcx, rbx
	je	.L348
	mov	rdx, QWORD PTR [rbx]
	mov	QWORD PTR 0[rbp], rcx
	mov	QWORD PTR 16[rbp], rdx
.L242:
	mov	QWORD PTR 8[rbp], rax
	xor	ecx, ecx
	add	rbp, 32
	mov	QWORD PTR -16[rbx], rbx
	mov	QWORD PTR -8[rbx], rcx
	mov	BYTE PTR [rbx], 0
	mov	QWORD PTR 376[rsp], rbp
.L243:
	add	rbx, 32
.L239:
	lea	rax, -16[rbx]
	cmp	QWORD PTR 104[rsp], rax
	je	.L349
	mov	rbp, QWORD PTR 376[rsp]
	mov	r14, QWORD PTR 384[rsp]
	cmp	rbp, r14
	jne	.L350
	mov	r13, QWORD PTR 368[rsp]
	mov	rsi, rbp
	movabs	rdx, 288230376151711743
	sub	rsi, r13
	mov	rax, rsi
	sar	rax, 5
	cmp	rax, rdx
	je	.L351
	cmp	rbp, r13
	je	.L245
	lea	r12, [rax+rax]
	cmp	r12, rax
	jb	.L280
	xor	eax, eax
	test	r12, r12
	jne	.L271
.L247:
	lea	rdx, [rax+rsi]
	mov	rcx, QWORD PTR -8[rbx]
	lea	r8, 16[rdx]
	mov	QWORD PTR [rdx], r8
	mov	r9, QWORD PTR -16[rbx]
	cmp	r9, rbx
	je	.L352
	mov	r8, QWORD PTR [rbx]
	mov	QWORD PTR [rdx], r9
	mov	QWORD PTR 16[rdx], r8
.L249:
	mov	QWORD PTR 8[rdx], rcx
	xor	edx, edx
	mov	r8, rax
	mov	QWORD PTR -8[rbx], rdx
	mov	rdx, r13
	mov	QWORD PTR -16[rbx], rbx
	mov	BYTE PTR [rbx], 0
	jmp	.L250
.L251:
	mov	r9, QWORD PTR 16[rdx]
	mov	QWORD PTR [r8], rsi
	mov	QWORD PTR 16[r8], r9
.L252:
	mov	QWORD PTR 8[r8], rcx
	add	rdx, 32
	add	r8, 32
.L250:
	cmp	rbp, rdx
	je	.L353
	lea	r9, 16[r8]
	mov	rcx, QWORD PTR 8[rdx]
	mov	QWORD PTR [r8], r9
	mov	rsi, QWORD PTR [rdx]
	lea	r10, 16[rdx]
	cmp	rsi, r10
	jne	.L251
	add	ecx, 1
	mov	rdi, r9
	rep movsb
	mov	rcx, QWORD PTR 8[rdx]
	jmp	.L252
.L353:
	sub	rbp, r13
	movq	xmm7, rax
	test	r13, r13
	lea	rdx, 32[rax+rbp]
	movq	xmm2, rdx
	punpcklqdq	xmm7, xmm2
	je	.L254
	mov	rdx, r14
	mov	rcx, r13
	mov	QWORD PTR 120[rsp], rax
	sub	rdx, r13
	call	_ZdlPvy
	mov	rax, QWORD PTR 120[rsp]
.L254:
	sal	r12, 5
	movaps	XMMWORD PTR 368[rsp], xmm7
	add	rax, r12
	mov	QWORD PTR 384[rsp], rax
	jmp	.L243
.L352:
	add	ecx, 1
	mov	rdi, r8
	mov	rsi, rbx
	rep movsb
	mov	rcx, QWORD PTR -8[rbx]
	jmp	.L249
.L245:
	add	rax, 1
	mov	r12, rax
	jc	.L280
.L271:
	movabs	rax, 288230376151711743
	cmp	r12, rax
	cmova	r12, rax
.L246:
	mov	rcx, r12
	sal	rcx, 5
	call	_Znwy
	jmp	.L247
.L280:
	movabs	r12, 288230376151711743
	jmp	.L246
.L351:
	lea	rcx, .LC3[rip]
	call	_ZSt20__throw_length_errorPKc
.L349:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rbx, rax
	mov	rax, QWORD PTR 344[rsp]
	sub	rax, QWORD PTR 336[rsp]
	cmp	rax, 3200000
	jne	.L256
	mov	rax, QWORD PTR 376[rsp]
	sub	rax, QWORD PTR 368[rsp]
	cmp	rax, 3200000
	jne	.L256
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC13[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rsi, QWORD PTR 96[rsp]
	mov	rcx, rax
	pxor	xmm1, xmm1
	mov	rdx, QWORD PTR 112[rsp]
	mov	rax, rsi
	sub	rax, rdx
	cvtsi2sd	xmm1, rax
	divsd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC14[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	sub	rbx, rsi
	pxor	xmm1, xmm1
	mov	rcx, rax
	cvtsi2sd	xmm1, rbx
	divsd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, r15
	mov	eax, DWORD PTR 140[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 88[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 80[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 72[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 48[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 40[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 64[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 56[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	nop
	movaps	xmm6, XMMWORD PTR 400[rsp]
	xor	eax, eax
	movaps	xmm7, XMMWORD PTR 416[rsp]
	add	rsp, 440
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L348:
	lea	ecx, 1[rax]
	mov	rdi, rdx
	mov	rsi, rbx
	rep movsb
	mov	rax, QWORD PTR -8[rbx]
	jmp	.L242
.L256:
	lea	rdx, .LC8[rip]
	mov	r8d, 65
	lea	rcx, .LC12[rip]
	call	[QWORD PTR __imp__assert[rip]]
.LEHE26:
.L220:
	lea	rdx, .LC8[rip]
	mov	r8d, 47
	lea	rcx, .LC9[rip]
.LEHB27:
	call	[QWORD PTR __imp__assert[rip]]
.L341:
	call	_ZSt17__throw_bad_allocv
.L340:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE27:
.L342:
	lea	ecx, 1[rax]
	mov	rdi, rdx
	mov	rsi, rbx
	rep movsb
	mov	rax, QWORD PTR -8[rbx]
	jmp	.L225
.L328:
	lea	rcx, .LC0[rip]
.LEHB28:
	call	_ZSt20__throw_length_errorPKc
.LEHE28:
.L336:
.LEHB29:
	call	_ZSt17__throw_bad_allocv
.L335:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE29:
.L289:
.L320:
	lea	rcx, 368[rsp]
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB30:
	call	_Unwind_Resume
.L290:
	jmp	.L320
.L288:
	mov	rcx, r15
	mov	rbx, rax
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 88[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 80[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
.L264:
	mov	rcx, QWORD PTR 72[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
.L262:
	mov	rcx, QWORD PTR 48[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 40[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, QWORD PTR 64[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
.L260:
	mov	rcx, QWORD PTR 56[rsp]
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EED1Ev
	mov	rcx, rbx
	call	_Unwind_Resume
.L285:
	mov	rcx, r15
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	jmp	.L262
.L286:
	mov	rcx, r15
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	jmp	.L264
.L287:
	mov	rbx, rax
	jmp	.L264
.L284:
	mov	rbx, rax
	jmp	.L262
.L281:
	mov	rbx, rax
	mov	rcx, r15
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
	call	_Unwind_Resume
.LEHE30:
.L282:
	mov	rcx, r15
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	jmp	.L260
.L283:
	mov	rbx, rax
	jmp	.L260
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5579:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5579-.LLSDACSB5579
.LLSDACSB5579:
	.uleb128 .LEHB11-.LFB5579
	.uleb128 .LEHE11-.LEHB11
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB12-.LFB5579
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L290-.LFB5579
	.uleb128 0
	.uleb128 .LEHB13-.LFB5579
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L289-.LFB5579
	.uleb128 0
	.uleb128 .LEHB14-.LFB5579
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L290-.LFB5579
	.uleb128 0
	.uleb128 .LEHB15-.LFB5579
	.uleb128 .LEHE15-.LEHB15
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB16-.LFB5579
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L281-.LFB5579
	.uleb128 0
	.uleb128 .LEHB17-.LFB5579
	.uleb128 .LEHE17-.LEHB17
	.uleb128 .L283-.LFB5579
	.uleb128 0
	.uleb128 .LEHB18-.LFB5579
	.uleb128 .LEHE18-.LEHB18
	.uleb128 .L282-.LFB5579
	.uleb128 0
	.uleb128 .LEHB19-.LFB5579
	.uleb128 .LEHE19-.LEHB19
	.uleb128 .L284-.LFB5579
	.uleb128 0
	.uleb128 .LEHB20-.LFB5579
	.uleb128 .LEHE20-.LEHB20
	.uleb128 .L289-.LFB5579
	.uleb128 0
	.uleb128 .LEHB21-.LFB5579
	.uleb128 .LEHE21-.LEHB21
	.uleb128 .L290-.LFB5579
	.uleb128 0
	.uleb128 .LEHB22-.LFB5579
	.uleb128 .LEHE22-.LEHB22
	.uleb128 .L284-.LFB5579
	.uleb128 0
	.uleb128 .LEHB23-.LFB5579
	.uleb128 .LEHE23-.LEHB23
	.uleb128 .L285-.LFB5579
	.uleb128 0
	.uleb128 .LEHB24-.LFB5579
	.uleb128 .LEHE24-.LEHB24
	.uleb128 .L287-.LFB5579
	.uleb128 0
	.uleb128 .LEHB25-.LFB5579
	.uleb128 .LEHE25-.LEHB25
	.uleb128 .L286-.LFB5579
	.uleb128 0
	.uleb128 .LEHB26-.LFB5579
	.uleb128 .LEHE26-.LEHB26
	.uleb128 .L288-.LFB5579
	.uleb128 0
	.uleb128 .LEHB27-.LFB5579
	.uleb128 .LEHE27-.LEHB27
	.uleb128 .L284-.LFB5579
	.uleb128 0
	.uleb128 .LEHB28-.LFB5579
	.uleb128 .LEHE28-.LEHB28
	.uleb128 .L289-.LFB5579
	.uleb128 0
	.uleb128 .LEHB29-.LFB5579
	.uleb128 .LEHE29-.LEHB29
	.uleb128 .L284-.LFB5579
	.uleb128 0
	.uleb128 .LEHB30-.LFB5579
	.uleb128 .LEHE30-.LEHB30
	.uleb128 0
	.uleb128 0
.LLSDACSE5579:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC6:
	.long	0
	.long	1093567616
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_rethrow;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
