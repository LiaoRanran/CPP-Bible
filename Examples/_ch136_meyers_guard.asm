	.file	"_ch136_meyers_guard.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB3201:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv:
.LFB5278:
	.seh_endprologue
	mov	edx, DWORD PTR 8[rcx]
	mov	rax, QWORD PTR 16[rcx]
	mov	ecx, edx
	rex.W jmp	rax
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev:
.LFB5276:
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev:
.LFB5277:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE[rip+16]
	mov	rbx, rcx
	mov	QWORD PTR [rcx], rax
	call	_ZNSt6thread6_StateD2Ev
	mov	edx, 24
	mov	rcx, rbx
	add	rsp, 32
	pop	rbx
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.def	__tcf_1;	.scl	3;	.type	32;	.endef
	.seh_proc	__tcf_1
__tcf_1:
.LFB4154:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rsi, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16]
	mov	rbx, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+8]
	cmp	rsi, rbx
	je	.L7
	.p2align 4,,10
	.p2align 3
.L9:
	mov	rcx, QWORD PTR [rbx]
	lea	rax, 16[rbx]
	cmp	rcx, rax
	je	.L8
	mov	rax, QWORD PTR 16[rbx]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L8:
	add	rbx, 32
	cmp	rsi, rbx
	jne	.L9
	mov	rbx, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+8]
.L7:
	test	rbx, rbx
	je	.L6
	mov	rdx, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+24]
	mov	rcx, rbx
	sub	rdx, rbx
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L6:
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_insert\0"
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE12emplace_backIJS5_EEERS5_DpOT_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE12emplace_backIJS5_EEERS5_DpOT_.isra.0
_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE12emplace_backIJS5_EEERS5_DpOT_.isra.0:
.LFB5306:
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
	cmp	rdi, QWORD PTR 16[rcx]
	mov	rsi, rcx
	mov	rbx, rdx
	je	.L13
	lea	rcx, 16[rdi]
	mov	r8, QWORD PTR 8[rbx]
	mov	QWORD PTR [rdi], rcx
	mov	rdx, QWORD PTR [rdx]
	lea	rax, 16[rbx]
	cmp	rdx, rax
	je	.L73
	mov	QWORD PTR [rdi], rdx
	mov	rdx, QWORD PTR 16[rbx]
	mov	QWORD PTR 16[rdi], rdx
.L21:
	mov	QWORD PTR 8[rdi], r8
	mov	QWORD PTR [rbx], rax
	mov	QWORD PTR 8[rbx], 0
	mov	BYTE PTR 16[rbx], 0
	add	QWORD PTR 8[rsi], 32
.L12:
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
.L13:
	movabs	rdx, 288230376151711743
	mov	rbp, QWORD PTR [rcx]
	mov	r13, rdi
	sub	r13, rbp
	mov	rax, r13
	sar	rax, 5
	cmp	rax, rdx
	je	.L74
	cmp	rdi, rbp
	je	.L75
	lea	rdx, [rax+rax]
	cmp	rdx, rax
	jb	.L49
	test	rdx, rdx
	jne	.L76
	mov	ecx, 32
	xor	r12d, r12d
	xor	r10d, r10d
.L28:
	mov	r8, QWORD PTR [rbx]
	lea	rax, [r10+r13]
	lea	rdx, 16[rbx]
	mov	r11, QWORD PTR 8[rbx]
	lea	r9, 16[rax]
	mov	QWORD PTR [rax], r9
	cmp	r8, rdx
	je	.L77
	mov	QWORD PTR [rax], r8
	mov	r8, QWORD PTR 16[rbx]
	mov	QWORD PTR 16[rax], r8
.L36:
	cmp	rdi, rbp
	mov	QWORD PTR 8[rax], r11
	mov	QWORD PTR [rbx], rdx
	mov	QWORD PTR 8[rbx], 0
	mov	BYTE PTR 16[rbx], 0
	je	.L37
	lea	rax, 16[rbp]
	mov	rdx, r10
	lea	r11, 16[rdi]
	jmp	.L46
	.p2align 4,,10
	.p2align 3
.L38:
	mov	QWORD PTR [rdx], rcx
	mov	rcx, QWORD PTR [rax]
	mov	QWORD PTR 16[rdx], rcx
.L45:
	add	rax, 32
	mov	QWORD PTR 8[rdx], r9
	add	rdx, 32
	cmp	rax, r11
	je	.L78
.L46:
	lea	r8, 16[rdx]
	mov	r9, QWORD PTR -8[rax]
	mov	QWORD PTR [rdx], r8
	mov	rcx, QWORD PTR -16[rax]
	cmp	rax, rcx
	jne	.L38
	lea	rcx, 1[r9]
	cmp	ecx, 8
	jnb	.L39
	test	cl, 4
	jne	.L79
	test	ecx, ecx
	je	.L45
	movzx	r9d, BYTE PTR [rax]
	test	cl, 2
	mov	BYTE PTR [r8], r9b
	jne	.L69
.L72:
	mov	r9, QWORD PTR -8[rax]
	jmp	.L45
	.p2align 4,,10
	.p2align 3
.L75:
	add	rax, 1
	jc	.L49
	movabs	rdx, 288230376151711743
	cmp	rax, rdx
	cmovbe	rdx, rax
	mov	r12, rdx
	sal	r12, 5
.L27:
	mov	rcx, r12
	call	_Znwy
	lea	rcx, 32[rax]
	mov	r10, rax
	add	r12, rax
	jmp	.L28
	.p2align 4,,10
	.p2align 3
.L78:
	sub	rdi, rbp
	lea	rcx, 32[r10+rdi]
.L37:
	movq	xmm6, r10
	movq	xmm0, rcx
	test	rbp, rbp
	punpcklqdq	xmm6, xmm0
	je	.L47
	mov	rdx, QWORD PTR 16[rsi]
	mov	rcx, rbp
	sub	rdx, rbp
	call	_ZdlPvy
.L47:
	movups	XMMWORD PTR [rsi], xmm6
	mov	QWORD PTR 16[rsi], r12
	jmp	.L12
	.p2align 4,,10
	.p2align 3
.L39:
	mov	r9d, ecx
	sub	ecx, 1
	mov	rbx, QWORD PTR -8[rax+r9]
	cmp	ecx, 8
	mov	QWORD PTR -8[r8+r9], rbx
	jb	.L72
	and	ecx, -8
	xor	r9d, r9d
.L43:
	mov	ebx, r9d
	add	r9d, 8
	mov	r13, QWORD PTR [rax+rbx]
	cmp	r9d, ecx
	mov	QWORD PTR [r8+rbx], r13
	jb	.L43
	jmp	.L72
	.p2align 4,,10
	.p2align 3
.L73:
	lea	rdx, 1[r8]
	cmp	edx, 8
	jnb	.L15
	test	dl, 4
	jne	.L80
	test	edx, edx
	je	.L21
	movzx	r8d, BYTE PTR 16[rbx]
	test	dl, 2
	mov	BYTE PTR 16[rdi], r8b
	je	.L71
	mov	edx, edx
	movzx	r8d, WORD PTR -2[rax+rdx]
	mov	WORD PTR -2[rcx+rdx], r8w
	mov	r8, QWORD PTR 8[rbx]
	jmp	.L21
	.p2align 4,,10
	.p2align 3
.L49:
	movabs	r12, 9223372036854775776
	jmp	.L27
	.p2align 4,,10
	.p2align 3
.L15:
	mov	r8d, edx
	sub	edx, 1
	mov	r9, QWORD PTR -8[rax+r8]
	cmp	edx, 8
	mov	QWORD PTR -8[rcx+r8], r9
	jb	.L71
	and	edx, -8
	xor	r8d, r8d
.L19:
	mov	r9d, r8d
	add	r8d, 8
	mov	r10, QWORD PTR [rax+r9]
	cmp	r8d, edx
	mov	QWORD PTR [rcx+r9], r10
	jb	.L19
.L71:
	mov	r8, QWORD PTR 8[rbx]
	jmp	.L21
	.p2align 4,,10
	.p2align 3
.L77:
	lea	r8, 1[r11]
	cmp	r8d, 8
	jnb	.L30
	test	r8b, 4
	jne	.L81
	test	r8d, r8d
	je	.L36
	movzx	r13d, BYTE PTR 16[rbx]
	test	r8b, 2
	mov	BYTE PTR 16[rax], r13b
	je	.L36
	mov	r8d, r8d
	movzx	r13d, WORD PTR -2[rdx+r8]
	mov	WORD PTR -2[r9+r8], r13w
	jmp	.L36
	.p2align 4,,10
	.p2align 3
.L30:
	mov	r13d, r8d
	sub	r8d, 1
	mov	r14, QWORD PTR -8[rdx+r13]
	cmp	r8d, 8
	mov	QWORD PTR -8[r9+r13], r14
	jb	.L36
	and	r8d, -8
	xor	r13d, r13d
.L34:
	mov	r14d, r13d
	add	r13d, 8
	mov	r15, QWORD PTR [rdx+r14]
	cmp	r13d, r8d
	mov	QWORD PTR [r9+r14], r15
	jb	.L34
	jmp	.L36
.L79:
	mov	r9d, DWORD PTR [rax]
	mov	ecx, ecx
	mov	DWORD PTR [r8], r9d
	mov	r9d, DWORD PTR -4[rax+rcx]
	mov	DWORD PTR -4[r8+rcx], r9d
	mov	r9, QWORD PTR -8[rax]
	jmp	.L45
.L69:
	mov	ecx, ecx
	movzx	r9d, WORD PTR -2[rax+rcx]
	mov	WORD PTR -2[r8+rcx], r9w
	mov	r9, QWORD PTR -8[rax]
	jmp	.L45
.L80:
	mov	r8d, DWORD PTR 16[rbx]
	mov	edx, edx
	mov	DWORD PTR 16[rdi], r8d
	mov	r8d, DWORD PTR -4[rax+rdx]
	mov	DWORD PTR -4[rcx+rdx], r8d
	mov	r8, QWORD PTR 8[rbx]
	jmp	.L21
.L81:
	mov	r13d, DWORD PTR 16[rbx]
	mov	r8d, r8d
	mov	DWORD PTR 16[rax], r13d
	mov	r13d, DWORD PTR -4[rdx+r8]
	mov	DWORD PTR -4[r9+r8], r13d
	jmp	.L36
.L76:
	movabs	rax, 288230376151711743
	cmp	rdx, rax
	cmova	rdx, rax
	sal	rdx, 5
	mov	r12, rdx
	jmp	.L27
.L74:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC1:
	.ascii "00010203040506070809101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899\0"
	.section	.text$_ZNSt7__cxx119to_stringEi,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt7__cxx119to_stringEi
	.def	_ZNSt7__cxx119to_stringEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx119to_stringEi
_ZNSt7__cxx119to_stringEi:
.LFB1643:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 248
	.seh_stackalloc	248
	.seh_endprologue
	test	edx, edx
	mov	rdi, rcx
	mov	ebx, edx
	js	.L83
	xor	ecx, ecx
	cmp	edx, 9
	jbe	.L120
.L84:
	cmp	ebx, 99
	jbe	.L121
	cmp	ebx, 999
	jbe	.L122
	cmp	ebx, 9999
	jbe	.L123
	cmp	ebx, 99999
	mov	eax, 5
	jbe	.L93
	cmp	ebx, 999999
	jbe	.L124
	cmp	ebx, 9999999
	jbe	.L108
	cmp	ebx, 99999999
	jbe	.L109
	cmp	ebx, 999999999
	jbe	.L110
	mov	ebp, 9
	mov	eax, 5
.L94:
	add	eax, 5
.L92:
	add	eax, ecx
	lea	rcx, 16[rdi]
	mov	eax, eax
	mov	QWORD PTR [rdi], rcx
.L86:
	movabs	r10, 3255307777713450285
	cmp	eax, 8
	mov	r8d, eax
	jnb	.L96
	test	al, 4
	jne	.L125
	test	r8d, r8d
	je	.L97
	test	r8b, 2
	mov	BYTE PTR [rcx], 45
	jne	.L126
.L97:
	mov	rcx, QWORD PTR [rdi]
	add	rcx, rax
.L85:
	mov	QWORD PTR 8[rdi], rax
	movsx	rsi, edx
	mov	r8d, 201
	mov	BYTE PTR [rcx], 0
	lea	rdx, .LC1[rip]
	shr	rsi, 63
	add	rsi, QWORD PTR [rdi]
	lea	rcx, 32[rsp]
	call	memcpy
	cmp	ebx, 99
	jbe	.L102
	.p2align 4,,10
	.p2align 3
.L103:
	mov	edx, ebx
	mov	eax, ebx
	imul	rdx, rdx, 1374389535
	shr	rdx, 37
	imul	ecx, edx, 100
	sub	eax, ecx
	mov	ecx, ebx
	mov	ebx, edx
	add	eax, eax
	mov	edx, ebp
	lea	r8d, 1[rax]
	movzx	r8d, BYTE PTR 32[rsp+r8]
	mov	BYTE PTR [rsi+rdx], r8b
	movzx	eax, BYTE PTR 32[rsp+rax]
	lea	edx, -1[rbp]
	sub	ebp, 2
	cmp	ecx, 9999
	mov	BYTE PTR [rsi+rdx], al
	ja	.L103
.L102:
	lea	eax, 48[rbx]
	cmp	ebx, 9
	jbe	.L105
	add	ebx, ebx
	lea	eax, 1[rbx]
	movzx	eax, BYTE PTR 32[rsp+rax]
	mov	BYTE PTR 1[rsi], al
	movzx	eax, BYTE PTR 32[rsp+rbx]
.L105:
	mov	BYTE PTR [rsi], al
	mov	rax, rdi
	add	rsp, 248
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L83:
	neg	ebx
	mov	ecx, 1
	cmp	ebx, 9
	ja	.L84
	lea	rcx, 16[rdi]
	xor	ebp, ebp
	mov	eax, 2
	mov	QWORD PTR [rdi], rcx
	jmp	.L86
	.p2align 4,,10
	.p2align 3
.L110:
	mov	eax, 9
.L93:
	lea	ebp, -1[rax]
	jmp	.L92
	.p2align 4,,10
	.p2align 3
.L108:
	mov	ebp, 6
	mov	eax, 7
	jmp	.L92
	.p2align 4,,10
	.p2align 3
.L109:
	mov	ebp, 7
	mov	eax, 8
	jmp	.L92
	.p2align 4,,10
	.p2align 3
.L96:
	lea	r8d, -1[rax]
	mov	QWORD PTR -8[rcx+rax], r10
	cmp	r8d, 8
	jb	.L97
	mov	r9d, r8d
	xor	r8d, r8d
	and	r9d, -8
.L100:
	mov	r11d, r8d
	add	r8d, 8
	cmp	r8d, r9d
	mov	QWORD PTR [rcx+r11], r10
	jb	.L100
	jmp	.L97
.L120:
	lea	rax, 16[rdi]
	mov	BYTE PTR 16[rdi], 45
	xor	ebp, ebp
	mov	QWORD PTR [rdi], rax
	lea	rcx, 17[rdi]
	mov	eax, 1
	jmp	.L85
.L121:
	lea	eax, 2[rcx]
	mov	ebp, 1
	lea	rcx, 16[rdi]
	mov	QWORD PTR [rdi], rcx
	jmp	.L86
.L123:
	lea	eax, 4[rcx]
	mov	ebp, 3
	lea	rcx, 16[rdi]
	mov	QWORD PTR [rdi], rcx
	jmp	.L86
.L122:
	lea	eax, 3[rcx]
	mov	ebp, 2
	lea	rcx, 16[rdi]
	mov	QWORD PTR [rdi], rcx
	jmp	.L86
.L125:
	mov	DWORD PTR [rcx], 757935405
	mov	DWORD PTR -4[rcx+r8], 757935405
	jmp	.L97
.L126:
	mov	r9d, 11565
	mov	WORD PTR -2[rcx+r8], r9w
	jmp	.L97
.L124:
	mov	ebp, 5
	mov	eax, 1
	jmp	.L94
	.seh_endproc
	.section	.text$_ZN6Logger8instanceEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN6Logger8instanceEv
	.def	_ZN6Logger8instanceEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6Logger8instanceEv
_ZN6Logger8instanceEv:
.LFB4125:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	movzx	eax, BYTE PTR _ZGVZN6Logger8instanceEvE4inst[rip]
	test	al, al
	je	.L134
.L129:
	lea	rax, _ZZN6Logger8instanceEvE4inst[rip]
	add	rsp, 32
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L134:
	lea	rbx, _ZGVZN6Logger8instanceEvE4inst[rip]
	mov	rcx, rbx
	call	__cxa_guard_acquire
	test	eax, eax
	je	.L129
	lea	rcx, __tcf_1[rip]
	call	atexit
	mov	rcx, rbx
	call	__cxa_guard_release
	lea	rax, _ZZN6Logger8instanceEvE4inst[rip]
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorISt6threadSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	.def	_ZNSt6vectorISt6threadSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt6threadSaIS0_EED1Ev
_ZNSt6vectorISt6threadSaIS0_EED1Ev:
.LFB4670:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	mov	r8, QWORD PTR [rcx]
	cmp	rdx, r8
	je	.L136
	mov	rax, r8
	.p2align 4,,10
	.p2align 3
.L138:
	cmp	QWORD PTR [rax], 0
	jne	.L141
	add	rax, 8
	cmp	rdx, rax
	jne	.L138
.L136:
	test	r8, r8
	je	.L135
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, r8
	sub	rdx, r8
	add	rsp, 40
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L135:
	add	rsp, 40
	ret
.L141:
	call	_ZSt9terminatev
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
.LFB4717:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L142
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L142:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "basic_string::_M_replace\0"
.LC3:
	.ascii "worker-\0"
.LC4:
	.ascii "basic_string::_M_create\0"
	.text
	.p2align 4
	.globl	_Z6workeri
	.def	_Z6workeri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6workeri
_Z6workeri:
.LFB4156:
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
	sub	rsp, 112
	.seh_stackalloc	112
	.seh_endprologue
	movzx	eax, BYTE PTR _ZGVZN6Logger8instanceEvE4inst[rip]
	test	al, al
	mov	ebx, ecx
	je	.L199
.L146:
	lea	r12, 48[rsp]
	mov	edx, ebx
	mov	rcx, r12
	call	_ZNSt7__cxx119to_stringEi
	mov	rbx, QWORD PTR 56[rsp]
	movabs	rax, 9223372036854775807
	sub	rax, rbx
	cmp	rax, 6
	jbe	.L200
	mov	rdi, QWORD PTR 48[rsp]
	lea	rsi, 64[rsp]
	lea	rbp, 7[rbx]
	cmp	rdi, rsi
	je	.L201
	mov	rax, QWORD PTR 64[rsp]
	cmp	rax, rbp
	jb	.L152
.L150:
	lea	r9, .LC3[rip]
	cmp	r9, rdi
	jnb	.L202
.L153:
	test	rbx, rbx
	jne	.L203
.L155:
	mov	DWORD PTR [rdi], 1802661751
	mov	DWORD PTR 3[rdi], 762471787
	mov	rdi, QWORD PTR 48[rsp]
.L157:
	mov	QWORD PTR 56[rsp], rbp
	mov	BYTE PTR 7[rdi+rbx], 0
	mov	rax, QWORD PTR 48[rsp]
	lea	rbx, 96[rsp]
	mov	QWORD PTR 80[rsp], rbx
	cmp	rax, rsi
	je	.L204
	mov	QWORD PTR 80[rsp], rax
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 96[rsp], rax
	mov	rax, QWORD PTR 56[rsp]
.L172:
	lea	rdi, 80[rsp]
	mov	QWORD PTR 88[rsp], rax
	lea	rcx, _ZZN6Logger8instanceEvE4inst[rip+8]
	mov	rdx, rdi
	mov	QWORD PTR 48[rsp], rsi
	add	DWORD PTR _ZZN6Logger8instanceEvE4inst[rip], 1
	mov	BYTE PTR 64[rsp], 0
	mov	QWORD PTR 56[rsp], 0
.LEHB0:
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE12emplace_backIJS5_EEERS5_DpOT_.isra.0
.LEHE0:
	mov	rcx, QWORD PTR 80[rsp]
	cmp	rcx, rbx
	je	.L173
	mov	rax, QWORD PTR 96[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L173:
	mov	rcx, QWORD PTR 48[rsp]
	cmp	rcx, rsi
	je	.L144
	mov	rax, QWORD PTR 64[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	nop
.L144:
	add	rsp, 112
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L203:
	cmp	rbx, 1
	je	.L205
	lea	rcx, 7[rdi]
	mov	r8, rbx
	mov	rdx, rdi
	call	memmove
	jmp	.L155
	.p2align 4,,10
	.p2align 3
.L202:
	lea	rax, [rdi+rbx]
	cmp	rax, r9
	jb	.L153
	mov	QWORD PTR 40[rsp], rbx
	xor	r8d, r8d
	mov	rdx, rdi
	mov	rcx, r12
	mov	QWORD PTR 32[rsp], 7
.LEHB1:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	rdi, QWORD PTR 48[rsp]
	jmp	.L157
	.p2align 4,,10
	.p2align 3
.L199:
	lea	rsi, _ZGVZN6Logger8instanceEvE4inst[rip]
	mov	rcx, rsi
	call	__cxa_guard_acquire
	test	eax, eax
	je	.L146
	lea	rcx, __tcf_1[rip]
	call	atexit
	mov	rcx, rsi
	call	__cxa_guard_release
	jmp	.L146
	.p2align 4,,10
	.p2align 3
.L152:
	test	rbp, rbp
	js	.L206
	lea	r13, [rax+rax]
	cmp	rbp, r13
	jb	.L207
	mov	rcx, rbx
	mov	r13, rbp
	add	rcx, 8
	js	.L160
.L161:
	call	_Znwy
	test	rbx, rbx
	mov	DWORD PTR [rax], 1802661751
	mov	r14, QWORD PTR 48[rsp]
	mov	rdi, rax
	mov	DWORD PTR 3[rax], 762471787
	jne	.L208
.L162:
	cmp	r14, rsi
	je	.L164
	mov	rax, QWORD PTR 64[rsp]
	mov	rcx, r14
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L164:
	mov	QWORD PTR 48[rsp], rdi
	mov	QWORD PTR 64[rsp], r13
	jmp	.L157
	.p2align 4,,10
	.p2align 3
.L208:
	cmp	rbx, 1
	je	.L209
	lea	rcx, 7[rax]
	mov	r8, rbx
	mov	rdx, r14
	call	memcpy
	jmp	.L162
	.p2align 4,,10
	.p2align 3
.L207:
	lea	rcx, 1[r13]
	test	r13, r13
	jns	.L161
.L160:
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L201:
	cmp	rbp, 15
	mov	ecx, 31
	mov	r13d, 30
	jbe	.L150
	jmp	.L161
	.p2align 4,,10
	.p2align 3
.L204:
	mov	rax, QWORD PTR 56[rsp]
	mov	r9, rbx
	mov	rdx, rsi
	lea	rcx, 1[rax]
	cmp	ecx, 8
	jnb	.L210
.L166:
	xor	r8d, r8d
	test	cl, 4
	je	.L169
	mov	r8d, DWORD PTR [rdx]
	mov	DWORD PTR [r9], r8d
	mov	r8d, 4
.L169:
	test	cl, 2
	je	.L170
	movzx	r10d, WORD PTR [rdx+r8]
	mov	WORD PTR [r9+r8], r10w
	add	r8, 2
.L170:
	and	ecx, 1
	je	.L172
	movzx	edx, BYTE PTR [rdx+r8]
	mov	BYTE PTR [r9+r8], dl
	jmp	.L172
	.p2align 4,,10
	.p2align 3
.L205:
	movzx	eax, BYTE PTR [rdi]
	mov	BYTE PTR 7[rdi], al
	jmp	.L155
	.p2align 4,,10
	.p2align 3
.L210:
	mov	r10d, ecx
	xor	edx, edx
	and	r10d, -8
.L167:
	mov	r8d, edx
	add	edx, 8
	mov	r9, QWORD PTR [rsi+r8]
	cmp	edx, r10d
	mov	QWORD PTR [rbx+r8], r9
	jb	.L167
	lea	r9, [rbx+rdx]
	add	rdx, rsi
	jmp	.L166
	.p2align 4,,10
	.p2align 3
.L209:
	movzx	eax, BYTE PTR [r14]
	mov	BYTE PTR 7[rdi], al
	jmp	.L162
.L200:
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_length_errorPKc
.L206:
	lea	rcx, .LC4[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE1:
.L178:
	mov	rbx, rax
	jmp	.L176
.L179:
	mov	rcx, rdi
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L176:
	mov	rcx, r12
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4156:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4156-.LLSDACSB4156
.LLSDACSB4156:
	.uleb128 .LEHB0-.LFB4156
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L179-.LFB4156
	.uleb128 0
	.uleb128 .LEHB1-.LFB4156
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L178-.LFB4156
	.uleb128 0
	.uleb128 .LEHB2-.LFB4156
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE4156:
	.text
	.seh_endproc
	.section	.text$_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	.def	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev:
.LFB5122:
	.seh_endprologue
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L211
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 8[rax]]
	.p2align 4,,10
	.p2align 3
.L211:
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFviERiEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFviERiEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
	.def	_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFviERiEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFviERiEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFviERiEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_:
.LFB4682:
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
	mov	QWORD PTR 160[rsp], r8
	movabs	rdx, 1152921504606846975
	sub	rax, rsi
	mov	r15, r9
	sar	rax, 3
	cmp	rax, rdx
	je	.L246
	mov	r13, rbx
	sub	r13, rsi
	cmp	rsi, rbp
	je	.L247
	lea	r14, [rax+rax]
	cmp	r14, rax
	jb	.L232
	test	r14, r14
	jne	.L248
	xor	r12d, r12d
.L219:
	add	r13, r12
	mov	ecx, 24
	mov	QWORD PTR 0[r13], 0
.LEHB3:
	call	_Znwy
.LEHE3:
	mov	edx, DWORD PTR [r15]
	lea	r15, 40[rsp]
	mov	QWORD PTR 40[rsp], rax
	lea	rcx, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE[rip+16]
	mov	QWORD PTR [rax], rcx
	lea	r8, _ZNSt6thread24_M_thread_deps_never_runEv[rip]
	mov	rcx, r13
	mov	DWORD PTR 8[rax], edx
	mov	rdx, QWORD PTR 160[rsp]
	mov	QWORD PTR 16[rax], rdx
	mov	rdx, r15
.LEHB4:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE4:
	mov	rcx, QWORD PTR 40[rsp]
	test	rcx, rcx
	je	.L220
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
.L220:
	mov	r8, rbx
	mov	rdx, rsi
	mov	rax, r12
	sub	r8, rsi
	cmp	rbx, rsi
	mov	rcx, r12
	je	.L222
	.p2align 4,,10
	.p2align 3
.L225:
	mov	QWORD PTR [rax], 0
	mov	rcx, QWORD PTR [rdx]
	add	rdx, 8
	add	rax, 8
	mov	QWORD PTR -8[rax], rcx
	cmp	rdx, rbx
	jne	.L225
	lea	rcx, [r12+r8]
.L222:
	add	rcx, 8
	cmp	rbx, rbp
	je	.L226
	sub	rbp, rbx
	mov	rdx, rbx
	mov	r8, rbp
	call	memcpy
	mov	rcx, rax
	add	rcx, rbp
.L226:
	movq	xmm6, r12
	movq	xmm0, rcx
	test	rsi, rsi
	punpcklqdq	xmm6, xmm0
	je	.L227
	mov	rdx, QWORD PTR 16[rdi]
	mov	rcx, rsi
	sub	rdx, rsi
	call	_ZdlPvy
.L227:
	lea	rax, [r12+r14*8]
	movups	XMMWORD PTR [rdi], xmm6
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
.L232:
	movabs	rcx, 9223372036854775800
	mov	r14, rdx
.L218:
.LEHB5:
	call	_Znwy
	mov	r12, rax
	jmp	.L219
	.p2align 4,,10
	.p2align 3
.L247:
	add	rax, 1
	jc	.L232
	movabs	r14, 1152921504606846975
	cmp	rax, r14
	cmovbe	r14, rax
	lea	rcx, 0[0+r14*8]
	jmp	.L218
.L248:
	movabs	rax, 1152921504606846975
	cmp	r14, rax
	cmova	r14, rax
	lea	rcx, 0[0+r14*8]
	jmp	.L218
.L246:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE5:
.L234:
	mov	rcx, rax
.L224:
	call	__cxa_begin_catch
	test	r12, r12
	je	.L249
	lea	rdx, 0[0+r14*8]
	mov	rcx, r12
	call	_ZdlPvy
.L229:
.LEHB6:
	call	__cxa_rethrow
.LEHE6:
.L236:
	mov	rbx, rax
	mov	rcx, r15
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	mov	rcx, rbx
	jmp	.L224
.L249:
	cmp	QWORD PTR 0[r13], 0
	je	.L229
	call	_ZSt9terminatev
.L235:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rcx, rbx
.LEHB7:
	call	_Unwind_Resume
	nop
.LEHE7:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA4682:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT4682-.LLSDATTD4682
.LLSDATTD4682:
	.byte	0x1
	.uleb128 .LLSDACSE4682-.LLSDACSB4682
.LLSDACSB4682:
	.uleb128 .LEHB3-.LFB4682
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L234-.LFB4682
	.uleb128 0x1
	.uleb128 .LEHB4-.LFB4682
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L236-.LFB4682
	.uleb128 0x3
	.uleb128 .LEHB5-.LFB4682
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LFB4682
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L235-.LFB4682
	.uleb128 0
	.uleb128 .LEHB7-.LFB4682
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSE4682:
	.byte	0x1
	.byte	0
	.byte	0
	.byte	0x7d
	.align 4
	.long	0

.LLSDATT4682:
	.section	.text$_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFviERiEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,"x"
	.linkonce discard
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC5:
	.ascii "lines=\0"
.LC6:
	.ascii " count=\0"
.LC7:
	.ascii "\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4157:
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
	sub	rsp, 112
	.seh_stackalloc	112
	.seh_endprologue
	lea	rdi, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE[rip+16]
	xor	ebx, ebx
	xor	esi, esi
	lea	rbp, _ZNSt6thread24_M_thread_deps_never_runEv[rip]
	call	__main
	lea	r12, 48[rsp]
	mov	DWORD PTR 44[rsp], 0
	xor	eax, eax
	mov	QWORD PTR 48[rsp], 0
	lea	r13, 44[rsp]
	mov	QWORD PTR 56[rsp], 0
	mov	QWORD PTR 64[rsp], 0
	jmp	.L257
	.p2align 4,,10
	.p2align 3
.L274:
	mov	QWORD PTR [rbx], 0
	mov	ecx, 24
.LEHB8:
	call	_Znwy
.LEHE8:
	lea	rdx, _Z6workeri[rip]
	mov	QWORD PTR [rax], rdi
	mov	r8, rbp
	mov	rcx, rbx
	lea	r14, 80[rsp]
	mov	QWORD PTR 16[rax], rdx
	mov	DWORD PTR 8[rax], esi
	mov	rdx, r14
	mov	QWORD PTR 80[rsp], rax
.LEHB9:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE9:
	mov	rcx, QWORD PTR 80[rsp]
	test	rcx, rcx
	je	.L252
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
.L252:
	add	esi, 1
	add	rbx, 8
	cmp	esi, 4
	mov	QWORD PTR 56[rsp], rbx
	mov	DWORD PTR 44[rsp], esi
	je	.L256
.L275:
	mov	rax, QWORD PTR 64[rsp]
.L257:
	cmp	rbx, rax
	jne	.L274
	mov	r9, r13
	mov	rdx, rbx
	mov	rcx, r12
	lea	r8, _Z6workeri[rip]
.LEHB10:
	call	_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFviERiEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
	add	esi, 1
	mov	rbx, QWORD PTR 56[rsp]
	cmp	esi, 4
	mov	DWORD PTR 44[rsp], esi
	jne	.L275
.L256:
	mov	rsi, QWORD PTR 48[rsp]
	cmp	rsi, rbx
	je	.L261
	.p2align 4,,10
	.p2align 3
.L260:
	mov	rcx, rsi
	call	_ZNSt6thread4joinEv
.LEHE10:
	add	rsi, 8
	cmp	rbx, rsi
	jne	.L260
.L261:
	call	_ZN6Logger8instanceEv
	lea	rdx, 96[rsp]
	mov	BYTE PTR 100[rsp], 0
	mov	QWORD PTR 80[rsp], rdx
	lea	r14, 80[rsp]
	mov	DWORD PTR 96[rsp], 1701736292
	lea	rcx, 8[rax]
	mov	rdx, r14
	mov	QWORD PTR 88[rsp], 4
	add	DWORD PTR [rax], 1
.LEHB11:
	call	_ZNSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS5_EE12emplace_backIJS5_EEERS5_DpOT_.isra.0
.LEHE11:
	mov	rcx, r14
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC5[rip]
.LEHB12:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rbx, rax
	call	_ZN6Logger8instanceEv
	mov	rcx, rbx
	mov	rdx, QWORD PTR 16[rax]
	sub	rdx, QWORD PTR 8[rax]
	sar	rdx, 5
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC6[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rbx, rax
	call	_ZN6Logger8instanceEv
	mov	rcx, rbx
	mov	edx, DWORD PTR [rax]
	call	_ZNSolsEi
	lea	rdx, .LC7[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE12:
	mov	rcx, r12
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	xor	eax, eax
	add	rsp, 112
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
.L263:
	mov	rbx, rax
	jmp	.L255
.L264:
	mov	rcx, r14
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L255:
	mov	rcx, r12
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	mov	rcx, rbx
.LEHB13:
	call	_Unwind_Resume
.LEHE13:
.L265:
	mov	rcx, r14
	mov	rbx, rax
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	jmp	.L255
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4157:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4157-.LLSDACSB4157
.LLSDACSB4157:
	.uleb128 .LEHB8-.LFB4157
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L263-.LFB4157
	.uleb128 0
	.uleb128 .LEHB9-.LFB4157
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L265-.LFB4157
	.uleb128 0
	.uleb128 .LEHB10-.LFB4157
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L263-.LFB4157
	.uleb128 0
	.uleb128 .LEHB11-.LFB4157
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L264-.LFB4157
	.uleb128 0
	.uleb128 .LEHB12-.LFB4157
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L263-.LFB4157
	.uleb128 0
	.uleb128 .LEHB13-.LFB4157
	.uleb128 .LEHE13-.LEHB13
	.uleb128 0
	.uleb128 0
.LLSDACSE4157:
	.section	.text.startup,"x"
	.seh_endproc
	.globl	_ZTSNSt6thread6_StateE
	.section	.rdata$_ZTSNSt6thread6_StateE,"dr"
	.linkonce same_size
	.align 16
_ZTSNSt6thread6_StateE:
	.ascii "NSt6thread6_StateE\0"
	.globl	_ZTINSt6thread6_StateE
	.section	.rdata$_ZTINSt6thread6_StateE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt6thread6_StateE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSNSt6thread6_StateE
	.globl	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE
	.section	.rdata$_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE,"dr"
	.linkonce same_size
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE:
	.ascii "NSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE\0"
	.globl	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE
	.section	.rdata$_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE
	.quad	_ZTINSt6thread6_StateE
	.globl	_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE
	.section	.rdata$_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv
	.globl	_ZGVZN6Logger8instanceEvE4inst
	.section	.data$_ZGVZN6Logger8instanceEvE4inst,"w"
	.linkonce same_size
	.align 8
_ZGVZN6Logger8instanceEvE4inst:
	.space 8
	.globl	_ZZN6Logger8instanceEvE4inst
	.section	.data$_ZZN6Logger8instanceEvE4inst,"w"
	.linkonce same_size
	.align 32
_ZZN6Logger8instanceEvE4inst:
	.space 32
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	__cxa_guard_acquire;	.scl	2;	.type	32;	.endef
	.def	atexit;	.scl	2;	.type	32;	.endef
	.def	__cxa_guard_release;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_rethrow;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread4joinEv;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
