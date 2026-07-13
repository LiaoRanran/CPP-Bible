	.file	"_ch147_sec.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt12format_errorD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12format_errorD1Ev
	.def	_ZNSt12format_errorD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12format_errorD1Ev
_ZNSt12format_errorD1Ev:
.LFB3272:
	.seh_endprologue
	lea	rax, _ZTVSt12format_error[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt13runtime_errorD2Ev
	.seh_endproc
	.section	.text$_ZNSt12format_errorD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12format_errorD0Ev
	.def	_ZNSt12format_errorD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12format_errorD0Ev
_ZNSt12format_errorD0Ev:
.LFB3273:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rax, _ZTVSt12format_error[rip+16]
	mov	rbx, rcx
	mov	QWORD PTR [rcx], rax
	call	_ZNSt13runtime_errorD2Ev
	mov	edx, 16
	mov	rcx, rbx
	add	rsp, 32
	pop	rbx
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEE11_M_overflowEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEE11_M_overflowEv
	.def	_ZNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEE11_M_overflowEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEE11_M_overflowEv
_ZNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEE11_M_overflowEv:
.LFB4742:
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	r13, QWORD PTR 24[rcx]
	mov	rbx, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR 296[rcx]
	mov	r12, r13
	mov	rdi, rcx
	sub	r12, rbx
	test	rbp, rbp
	js	.L16
	mov	rax, QWORD PTR 304[rcx]
	cmp	rax, rbp
	jnb	.L9
	sub	rbp, rax
	mov	rsi, QWORD PTR 288[rcx]
	cmp	r12, rbp
	cmovbe	rbp, r12
	test	rbp, rbp
	jle	.L11
	add	rbp, rbx
	.p2align 4,,10
	.p2align 3
.L13:
	mov	rax, QWORD PTR 24[rsi]
	movzx	edx, BYTE PTR [rbx]
	lea	rcx, 1[rax]
	mov	QWORD PTR 24[rsi], rcx
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[rsi]
	sub	rax, QWORD PTR 8[rsi]
	cmp	rax, QWORD PTR 16[rsi]
	je	.L17
.L12:
	add	rbx, 1
	cmp	rbx, rbp
	jne	.L13
	mov	rbx, QWORD PTR 8[rdi]
	mov	rax, QWORD PTR 304[rdi]
.L11:
	mov	QWORD PTR 288[rdi], rsi
.L9:
	add	rax, r12
	mov	QWORD PTR 24[rdi], rbx
	mov	QWORD PTR 304[rdi], rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L17:
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	call	[QWORD PTR [rax]]
	jmp	.L12
	.p2align 4,,10
	.p2align 3
.L16:
	test	r12, r12
	mov	rsi, QWORD PTR 288[rcx]
	jle	.L6
	.p2align 4,,10
	.p2align 3
.L8:
	mov	rax, QWORD PTR 24[rsi]
	movzx	edx, BYTE PTR [rbx]
	lea	rcx, 1[rax]
	mov	QWORD PTR 24[rsi], rcx
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[rsi]
	sub	rax, QWORD PTR 8[rsi]
	cmp	rax, QWORD PTR 16[rsi]
	je	.L18
.L7:
	add	rbx, 1
	cmp	r13, rbx
	jne	.L8
	mov	rbx, QWORD PTR 8[rdi]
.L6:
	mov	rax, QWORD PTR 304[rdi]
	mov	QWORD PTR 288[rdi], rsi
	jmp	.L9
	.p2align 4,,10
	.p2align 3
.L18:
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	call	[QWORD PTR [rax]]
	jmp	.L7
	.seh_endproc
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB11:
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
	.section .rdata,"dr"
.LC0:
	.ascii "user=%s\12\0"
	.text
	.p2align 4
	.globl	_Z8log_userRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.def	_Z8log_userRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8log_userRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_Z8log_userRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:
.LFB1951:
	.seh_endprologue
	mov	rdx, QWORD PTR [rcx]
	lea	rcx, .LC0[rip]
	jmp	_Z6printfPKcz
	.seh_endproc
	.section	.text$_ZSt20__throw_format_errorPKc,"x"
	.linkonce discard
	.globl	_ZSt20__throw_format_errorPKc
	.def	_ZSt20__throw_format_errorPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt20__throw_format_errorPKc
_ZSt20__throw_format_errorPKc:
.LFB3269:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rsi, rcx
	mov	ecx, 16
	call	__cxa_allocate_exception
	mov	rdx, rsi
	mov	rcx, rax
	mov	rbx, rax
.LEHB0:
	call	_ZNSt13runtime_errorC2EPKc
.LEHE0:
	lea	rax, _ZTVSt12format_error[rip+16]
	mov	rcx, rbx
	lea	r8, _ZNSt12format_errorD1Ev[rip]
	mov	QWORD PTR [rbx], rax
	lea	rdx, _ZTISt12format_error[rip]
.LEHB1:
	call	__cxa_throw
.L23:
	mov	rsi, rax
	mov	rcx, rbx
	call	__cxa_free_exception
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3269:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3269-.LLSDACSB3269
.LLSDACSB3269:
	.uleb128 .LEHB0-.LFB3269
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L23-.LFB3269
	.uleb128 0
	.uleb128 .LEHB1-.LFB3269
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE3269:
	.section	.text$_ZSt20__throw_format_errorPKc,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC1:
	.ascii "format error: conflicting indexing style in format string\0"
	.section	.text$_ZNSt8__format39__conflicting_indexing_in_format_stringEv,"x"
	.linkonce discard
	.globl	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
	.def	_ZNSt8__format39__conflicting_indexing_in_format_stringEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
_ZNSt8__format39__conflicting_indexing_in_format_stringEv:
.LFB3276:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC2:
	.ascii "format error: invalid arg-id in format string\0"
	.section	.text$_ZNSt8__format33__invalid_arg_id_in_format_stringEv,"x"
	.linkonce discard
	.globl	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.def	_ZNSt8__format33__invalid_arg_id_in_format_stringEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
_ZNSt8__format33__invalid_arg_id_in_format_stringEv:
.LFB3277:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC3:
	.ascii "format error: failed to parse format-spec\0"
	.section	.text$_ZNSt8__format29__failed_to_parse_format_specEv,"x"
	.linkonce discard
	.globl	_ZNSt8__format29__failed_to_parse_format_specEv
	.def	_ZNSt8__format29__failed_to_parse_format_specEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format29__failed_to_parse_format_specEv
_ZNSt8__format29__failed_to_parse_format_specEv:
.LFB3278:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, .LC3[rip]
	call	_ZSt20__throw_format_errorPKc
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
.LFB3988:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L27
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L27:
	ret
	.seh_endproc
	.section	.text$_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	.def	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_:
.LFB4144:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	xor	eax, eax
	mov	r10d, 32
	mov	r11, rcx
	mov	rbx, rdx
	mov	r9, rdx
	jmp	.L38
	.p2align 4,,10
	.p2align 3
.L43:
	lea	eax, [rax+rax*4]
	add	r9, 1
	movzx	ecx, cl
	lea	eax, [rcx+rax*2]
	cmp	r8, r9
	je	.L30
.L38:
	movzx	edx, BYTE PTR [r9]
	lea	ecx, -48[rdx]
	cmp	cl, 9
	ja	.L30
	sub	r10d, 4
	jns	.L43
	mov	edx, 10
	mul	edx
	jo	.L35
	movzx	ecx, cl
	add	ecx, eax
	jc	.L35
	add	r9, 1
	mov	eax, ecx
	cmp	r8, r9
	jne	.L38
.L30:
	cmp	rbx, r9
	je	.L35
	cmp	eax, 65535
	ja	.L35
	mov	WORD PTR [r11], ax
	mov	rax, r11
	mov	QWORD PTR 8[r11], r9
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L35:
	mov	rax, r11
	mov	QWORD PTR [r11], 0
	mov	QWORD PTR 8[r11], 0
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC4:
	.ascii "format error: unmatched '{' in format string\0"
	.align 8
.LC5:
	.ascii "format error: unmatched '}' in format string\0"
	.section	.text$_ZNSt8__format8_ScannerIcE7_M_scanEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format8_ScannerIcE7_M_scanEv
	.def	_ZNSt8__format8_ScannerIcE7_M_scanEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format8_ScannerIcE7_M_scanEv
_ZNSt8__format8_ScannerIcE7_M_scanEv:
.LFB3547:
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
	.seh_endprologue
	mov	r15, QWORD PTR 16[rcx]
	mov	rbx, QWORD PTR 8[rcx]
	mov	rdi, r15
	mov	r13, rcx
	sub	rdi, rbx
	cmp	rdi, 2
	je	.L111
	test	rdi, rdi
	jne	.L46
.L44:
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
.L111:
	cmp	BYTE PTR [rbx], 123
	je	.L112
.L46:
	mov	r8, rdi
	mov	edx, 123
	mov	rcx, rbx
	call	memchr
	mov	r8, rdi
	mov	edx, 125
	mov	rcx, rbx
	mov	r14, rax
	mov	rbp, -1
	mov	r12, -1
	sub	r14, rbx
	test	rax, rax
	cmove	r14, rbp
	call	memchr
	mov	rsi, rax
	sub	rsi, rbx
	test	rax, rax
	cmove	rsi, rbp
	cmp	rsi, r14
	je	.L53
	.p2align 4,,10
	.p2align 3
.L52:
	cmp	r14, rsi
	jnb	.L113
	lea	rax, 1[r14]
	cmp	rax, rdi
	je	.L57
	cmp	rsi, -1
	movzx	ebp, BYTE PTR 1[rbx+r14]
	je	.L114
	xor	edi, edi
	cmp	bpl, 123
	mov	rax, QWORD PTR 0[r13]
	mov	rcx, r13
	sete	dil
	add	rdi, r14
	add	rdi, QWORD PTR 8[r13]
	lea	rbx, 1[rdi]
	mov	rdx, rdi
	call	[QWORD PTR [rax]]
	cmp	bpl, 123
	mov	r15, QWORD PTR 16[r13]
	mov	QWORD PTR 8[r13], rbx
	je	.L115
	movzx	eax, BYTE PTR 1[rdi]
	cmp	al, 125
	je	.L116
	cmp	al, 58
	je	.L117
	lea	rcx, 2[rdi]
	xor	edx, edx
	cmp	al, 48
	je	.L66
	lea	edx, -49[rax]
	cmp	dl, 8
	ja	.L67
	lea	rcx, 2[rdi]
	movzx	edx, BYTE PTR 2[rdi]
	cmp	r15, rcx
	je	.L68
	sub	edx, 48
	cmp	dl, 9
	jbe	.L69
.L68:
	movsx	dx, al
	sub	edx, 48
.L66:
	movzx	eax, BYTE PTR [rcx]
	cmp	al, 125
	jne	.L118
.L72:
	cmp	DWORD PTR 24[r13], 2
	movzx	edx, dx
	je	.L47
	xor	eax, eax
	mov	DWORD PTR 24[r13], 1
	cmp	BYTE PTR [rcx], 58
	sete	al
	add	rcx, rax
	mov	QWORD PTR 8[r13], rcx
.L63:
	mov	rax, QWORD PTR 0[r13]
	mov	rcx, r13
	call	[QWORD PTR 8[rax]]
	mov	rax, QWORD PTR 8[r13]
	mov	r15, QWORD PTR 16[r13]
	lea	rbx, 1[rax]
	mov	rdi, r15
	mov	QWORD PTR 8[r13], rbx
	sub	rdi, rbx
	je	.L44
	mov	r8, rdi
	mov	edx, 123
	mov	rcx, rbx
	call	memchr
	test	rax, rax
	mov	r14, rax
	je	.L74
	sub	r14, rbx
.L110:
	mov	r8, rdi
	mov	edx, 125
	mov	rcx, rbx
	call	memchr
	test	rax, rax
	mov	rsi, rax
	je	.L88
.L83:
	sub	rsi, rbx
.L61:
	cmp	rsi, r14
	jne	.L52
.L53:
	mov	rax, QWORD PTR 0[r13]
	mov	rdx, r15
	mov	rcx, r13
	call	[QWORD PTR [rax]]
	mov	rax, QWORD PTR 16[r13]
	mov	QWORD PTR 8[r13], rax
	jmp	.L44
	.p2align 4,,10
	.p2align 3
.L113:
	lea	rbp, 1[rsi]
	cmp	rbp, rdi
	je	.L75
	cmp	BYTE PTR 1[rbx+rsi], 125
	jne	.L75
	mov	rbx, QWORD PTR 8[r13]
	mov	rcx, r13
	mov	rax, QWORD PTR 0[r13]
	add	rbx, rbp
	mov	rdx, rbx
	add	rbx, 1
	call	[QWORD PTR [rax]]
	mov	r15, QWORD PTR 16[r13]
	mov	QWORD PTR 8[r13], rbx
	mov	rdi, r15
	sub	rdi, rbx
	cmp	r14, -1
	je	.L119
	test	rdi, rdi
	je	.L44
	sub	r14, 1
	sub	r14, rbp
	jmp	.L110
	.p2align 4,,10
	.p2align 3
.L119:
	test	rdi, rdi
	je	.L44
	mov	r8, rdi
	mov	edx, 125
	mov	rcx, rbx
	call	memchr
	test	rax, rax
	mov	rsi, rax
	jne	.L83
	jmp	.L53
	.p2align 4,,10
	.p2align 3
.L114:
	cmp	bpl, 123
	jne	.L57
	add	rax, QWORD PTR 8[r13]
	mov	rcx, r13
	mov	rbx, rax
	mov	rax, QWORD PTR 0[r13]
	mov	rdx, rbx
	add	rbx, 1
	call	[QWORD PTR [rax]]
	mov	r15, QWORD PTR 16[r13]
	mov	QWORD PTR 8[r13], rbx
.L80:
	mov	rdi, r15
	sub	rdi, rbx
	je	.L44
	mov	r8, rdi
	mov	edx, 123
	mov	rcx, rbx
	call	memchr
	mov	r14, rax
	sub	r14, rbx
	test	rax, rax
	cmove	r14, r12
	jmp	.L61
	.p2align 4,,10
	.p2align 3
.L115:
	sub	rsi, 2
	sub	rsi, r14
	jmp	.L80
	.p2align 4,,10
	.p2align 3
.L88:
	mov	rsi, -1
	jmp	.L61
	.p2align 4,,10
	.p2align 3
.L118:
	cmp	al, 58
	je	.L72
.L67:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L116:
	cmp	DWORD PTR 24[r13], 1
	je	.L47
	mov	rdx, QWORD PTR 32[r13]
	mov	DWORD PTR 24[r13], 2
	lea	rax, 1[rdx]
	mov	QWORD PTR 32[r13], rax
	jmp	.L63
	.p2align 4,,10
	.p2align 3
.L117:
	cmp	DWORD PTR 24[r13], 1
	je	.L47
	mov	rdx, QWORD PTR 32[r13]
	add	rdi, 2
	mov	DWORD PTR 24[r13], 2
	mov	QWORD PTR 8[r13], rdi
	lea	rax, 1[rdx]
	mov	QWORD PTR 32[r13], rax
	jmp	.L63
	.p2align 4,,10
	.p2align 3
.L112:
	cmp	BYTE PTR 1[rbx], 125
	jne	.L46
	add	rbx, 1
	mov	rax, QWORD PTR [rcx]
	cmp	DWORD PTR 24[rcx], 1
	mov	QWORD PTR 8[rcx], rbx
	mov	rax, QWORD PTR 8[rax]
	je	.L47
	mov	rdx, QWORD PTR 32[rcx]
	mov	DWORD PTR 24[rcx], 2
	lea	rcx, 1[rdx]
	mov	QWORD PTR 32[r13], rcx
	mov	rcx, r13
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L69:
	lea	rcx, 32[rsp]
	mov	rdx, rbx
	mov	r8, r15
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	mov	rcx, QWORD PTR 40[rsp]
	movzx	edx, WORD PTR 32[rsp]
	test	rcx, rcx
	je	.L67
	movzx	eax, BYTE PTR [rcx]
	cmp	al, 125
	je	.L72
	jmp	.L118
	.p2align 4,,10
	.p2align 3
.L74:
	mov	r8, rdi
	mov	edx, 125
	mov	rcx, rbx
	call	memchr
	test	rax, rax
	mov	rsi, rax
	je	.L53
	mov	r14, -1
	jmp	.L83
.L57:
	lea	rcx, .LC4[rip]
	call	_ZSt20__throw_format_errorPKc
.L47:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L75:
	lea	rcx, .LC5[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC6:
	.ascii "format error: width must be non-zero in format string\0"
	.align 8
.LC7:
	.ascii "format error: invalid width or precision in format-spec\0"
	.section	.text$_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	.def	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE:
.LFB3957:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rbx, rdx
	movzx	edx, BYTE PTR [rdx]
	mov	rsi, rcx
	cmp	dl, 48
	je	.L139
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	movzx	eax, dl
	cmp	BYTE PTR [rcx+rax], 9
	ja	.L122
	lea	rcx, 32[rsp]
	mov	rdx, rbx
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	mov	rax, QWORD PTR 40[rsp]
	mov	rdx, QWORD PTR 32[rsp]
	test	rax, rax
	je	.L140
	cmp	rbx, rax
	mov	WORD PTR 4[rsi], dx
	mov	ecx, 1
	je	.L120
.L124:
	movzx	edx, WORD PTR [rsi]
	and	ecx, 3
	sal	ecx, 7
	and	dx, -385
	or	edx, ecx
	mov	WORD PTR [rsi], dx
.L120:
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L122:
	cmp	dl, 123
	mov	rax, rbx
	jne	.L120
	lea	rax, 1[rbx]
	cmp	r8, rax
	je	.L141
	movsx	dx, BYTE PTR 1[rbx]
	cmp	dl, 125
	je	.L142
	cmp	dl, 48
	je	.L143
	lea	ecx, -49[rdx]
	cmp	cl, 8
	ja	.L133
	lea	r10, 2[rbx]
	cmp	r8, r10
	je	.L133
	movzx	ecx, BYTE PTR 2[rbx]
	sub	ecx, 48
	cmp	cl, 9
	ja	.L134
	lea	rcx, 32[rsp]
	mov	rdx, rax
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 96[rsp], r8
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzx	edx, WORD PTR 32[rsp]
	mov	rax, QWORD PTR 40[rsp]
	mov	r9, QWORD PTR 104[rsp]
	mov	r8, QWORD PTR 96[rsp]
.L131:
	cmp	r8, rax
	je	.L133
	test	rax, rax
	je	.L133
.L136:
	cmp	BYTE PTR [rax], 125
	jne	.L133
	cmp	DWORD PTR 16[r9], 2
	je	.L135
	mov	DWORD PTR 16[r9], 1
	mov	WORD PTR 4[rsi], dx
	jmp	.L129
	.p2align 4,,10
	.p2align 3
.L142:
	cmp	DWORD PTR 16[r9], 1
	je	.L135
	mov	rdx, QWORD PTR 24[r9]
	mov	DWORD PTR 16[r9], 2
	lea	rcx, 1[rdx]
	mov	QWORD PTR 24[r9], rcx
	mov	WORD PTR 4[rsi], dx
.L129:
	add	rax, 1
	cmp	rbx, rax
	je	.L120
	mov	ecx, 2
	jmp	.L124
	.p2align 4,,10
	.p2align 3
.L143:
	lea	rax, 2[rbx]
	xor	edx, edx
	jmp	.L131
	.p2align 4,,10
	.p2align 3
.L134:
	sub	edx, 48
	mov	rax, r10
	jmp	.L136
.L141:
	lea	rcx, .LC4[rip]
	call	_ZSt20__throw_format_errorPKc
.L140:
	lea	rcx, .LC7[rip]
	call	_ZSt20__throw_format_errorPKc
.L139:
	lea	rcx, .LC6[rip]
	call	_ZSt20__throw_format_errorPKc
.L135:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L133:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC8:
	.ascii "format error: missing precision after '.' in format string\0"
	.section	.text$_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE
	.def	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE
_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE:
.LFB3583:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	rsi, QWORD PTR [rdx]
	mov	rax, QWORD PTR 8[rdx]
	mov	DWORD PTR 76[rsp], 0
	mov	rdi, rcx
	mov	rbx, rdx
	cmp	rsi, rax
	mov	BYTE PTR 76[rsp], 32
	mov	QWORD PTR 68[rsp], 0
	je	.L145
	movzx	ecx, BYTE PTR [rsi]
	cmp	cl, 125
	je	.L187
	cmp	cl, 123
	je	.L146
	mov	rdx, rax
	sub	rdx, rsi
	cmp	rdx, 1
	jle	.L147
	movzx	edx, BYTE PTR 1[rsi]
	cmp	dl, 62
	je	.L188
	cmp	dl, 94
	je	.L189
	cmp	dl, 60
	mov	r8d, 1
	jne	.L215
.L148:
	mov	BYTE PTR 76[rsp], cl
	add	rsi, 2
.L150:
	movzx	edx, BYTE PTR 68[rsp]
	and	edx, -4
	or	edx, r8d
	cmp	rax, rsi
	mov	BYTE PTR 68[rsp], dl
	je	.L187
.L152:
	movzx	ecx, BYTE PTR [rsi]
	cmp	cl, 125
	je	.L187
.L154:
	cmp	cl, 48
	je	.L216
	lea	r8, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	movzx	edx, cl
	cmp	BYTE PTR [r8+rdx], 9
	ja	.L156
	lea	rcx, 48[rsp]
	mov	r8, rax
	mov	rdx, rsi
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	mov	rdx, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 48[rsp]
	mov	rax, QWORD PTR 40[rsp]
	test	rdx, rdx
	je	.L175
	cmp	rsi, rdx
	mov	WORD PTR 72[rsp], cx
	mov	r8d, 1
	je	.L159
.L158:
	movzx	ecx, WORD PTR 68[rsp]
	and	r8d, 3
	sal	r8d, 7
	and	cx, -385
	or	ecx, r8d
	mov	WORD PTR 68[rsp], cx
.L159:
	cmp	rax, rdx
	je	.L145
	movzx	ecx, BYTE PTR [rdx]
	cmp	cl, 125
	je	.L199
.L160:
	cmp	cl, 46
	je	.L171
.L214:
	cmp	cl, 115
	je	.L217
.L173:
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L187:
	mov	rax, rsi
.L145:
	mov	rdx, QWORD PTR 68[rsp]
	mov	QWORD PTR [rdi], rdx
	movzx	edx, BYTE PTR 76[rsp]
	mov	BYTE PTR 8[rdi], dl
	add	rsp, 80
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L147:
	cmp	cl, 62
	je	.L200
	cmp	cl, 94
	je	.L201
	cmp	cl, 60
	je	.L202
	jmp	.L154
	.p2align 4,,10
	.p2align 3
.L171:
	movzx	r8d, BYTE PTR 1[rdx]
	lea	r9, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	lea	rsi, 1[rdx]
	cmp	BYTE PTR [r9+r8], 9
	ja	.L174
	lea	rcx, 48[rsp]
	mov	rdx, rsi
	mov	r8, rax
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	mov	rdx, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 48[rsp]
	test	rdx, rdx
	je	.L175
	cmp	rsi, rdx
	mov	rax, QWORD PTR 40[rsp]
	mov	WORD PTR 74[rsp], cx
	je	.L177
	mov	r8d, 1
.L176:
	movzx	ecx, BYTE PTR 69[rsp]
	add	r8d, r8d
	and	ecx, -7
	or	ecx, r8d
	cmp	rax, rdx
	mov	BYTE PTR 69[rsp], cl
	je	.L145
	movzx	ecx, BYTE PTR [rdx]
	cmp	cl, 125
	jne	.L214
.L199:
	mov	rax, rdx
	jmp	.L145
.L156:
	cmp	cl, 123
	mov	rdx, rsi
	jne	.L160
	.p2align 4,,10
	.p2align 3
.L146:
	lea	rdx, 1[rsi]
	cmp	rax, rdx
	je	.L178
	movsx	cx, BYTE PTR 1[rsi]
	cmp	cl, 125
	je	.L218
	cmp	cl, 48
	je	.L219
	lea	r8d, -49[rcx]
	cmp	r8b, 8
	jbe	.L167
.L168:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L215:
	cmp	cl, 62
	je	.L200
	cmp	cl, 94
	je	.L201
	cmp	cl, 60
	jne	.L152
.L202:
	mov	r8d, 1
.L151:
	add	rsi, 1
	jmp	.L150
	.p2align 4,,10
	.p2align 3
.L174:
	cmp	r8b, 123
	je	.L220
.L177:
	lea	rcx, .LC8[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L189:
	mov	r8d, 3
	jmp	.L148
	.p2align 4,,10
	.p2align 3
.L188:
	mov	r8d, 2
	jmp	.L148
	.p2align 4,,10
	.p2align 3
.L200:
	mov	r8d, 2
	jmp	.L151
	.p2align 4,,10
	.p2align 3
.L201:
	mov	r8d, 3
	jmp	.L151
	.p2align 4,,10
	.p2align 3
.L217:
	lea	rcx, 1[rdx]
	cmp	rcx, rax
	je	.L145
	cmp	BYTE PTR 1[rdx], 125
	jne	.L173
	mov	rax, rcx
	jmp	.L145
	.p2align 4,,10
	.p2align 3
.L218:
	cmp	DWORD PTR 16[rbx], 1
	je	.L170
	mov	rcx, QWORD PTR 24[rbx]
	mov	DWORD PTR 16[rbx], 2
	lea	r8, 1[rcx]
	mov	WORD PTR 72[rsp], cx
	mov	QWORD PTR 24[rbx], r8
.L164:
	add	rdx, 1
	cmp	rsi, rdx
	je	.L159
	mov	r8d, 2
	jmp	.L158
.L219:
	lea	rdx, 2[rsi]
	xor	ecx, ecx
.L166:
	cmp	rax, rdx
	je	.L168
	test	rdx, rdx
	je	.L168
.L186:
	cmp	BYTE PTR [rdx], 125
	jne	.L168
	cmp	DWORD PTR 16[rbx], 2
	je	.L170
	mov	DWORD PTR 16[rbx], 1
	mov	WORD PTR 72[rsp], cx
	jmp	.L164
.L220:
	lea	rcx, 2[rdx]
	cmp	rax, rcx
	je	.L178
	movzx	r8d, BYTE PTR 2[rdx]
	cmp	r8b, 125
	je	.L221
	cmp	r8b, 48
	je	.L222
	lea	r9d, -49[r8]
	cmp	r9b, 8
	ja	.L168
	lea	r9, 3[rdx]
	cmp	rax, r9
	je	.L168
	movzx	edx, BYTE PTR 3[rdx]
	sub	edx, 48
	cmp	dl, 9
	ja	.L183
	lea	r9, 48[rsp]
	mov	rdx, rcx
	mov	r8, rax
	mov	QWORD PTR 40[rsp], rax
	mov	rcx, r9
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzx	edx, WORD PTR 48[rsp]
	mov	rcx, QWORD PTR 56[rsp]
	mov	rax, QWORD PTR 40[rsp]
.L182:
	test	rcx, rcx
	je	.L168
	cmp	rax, rcx
	je	.L168
.L185:
	cmp	BYTE PTR [rcx], 125
	jne	.L168
	cmp	DWORD PTR 16[rbx], 2
	je	.L170
	mov	DWORD PTR 16[rbx], 1
	mov	WORD PTR 74[rsp], dx
.L180:
	lea	rdx, 1[rcx]
	cmp	rsi, rdx
	je	.L177
	mov	r8d, 2
	jmp	.L176
.L167:
	lea	r9, 2[rsi]
	cmp	rax, r9
	je	.L168
	movzx	r10d, BYTE PTR 2[rsi]
	lea	r8d, -48[r10]
	cmp	r8b, 9
	ja	.L169
	lea	rcx, 48[rsp]
	mov	r8, rax
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzx	ecx, WORD PTR 48[rsp]
	mov	rdx, QWORD PTR 56[rsp]
	mov	rax, QWORD PTR 40[rsp]
	jmp	.L166
.L169:
	sub	ecx, 48
	mov	rdx, r9
	jmp	.L186
.L221:
	cmp	DWORD PTR 16[rbx], 1
	je	.L170
	mov	rdx, QWORD PTR 24[rbx]
	mov	DWORD PTR 16[rbx], 2
	lea	r8, 1[rdx]
	mov	WORD PTR 74[rsp], dx
	mov	QWORD PTR 24[rbx], r8
	jmp	.L180
.L222:
	lea	rcx, 3[rdx]
	xor	edx, edx
	jmp	.L182
.L183:
	movsx	dx, r8b
	mov	rcx, r9
	sub	edx, 48
	jmp	.L185
.L216:
	lea	rcx, .LC6[rip]
	call	_ZSt20__throw_format_errorPKc
.L170:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L175:
	lea	rcx, .LC7[rip]
	call	_ZSt20__throw_format_errorPKc
.L178:
	lea	rcx, .LC4[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC9:
	.ascii "basic_string::_M_create\0"
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy:
.LFB4498:
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	rsi, QWORD PTR 144[rsp]
	lea	r13, [rdx+r8]
	mov	r15, rax
	mov	rbx, rcx
	sub	rsi, r8
	sub	r15, r13
	mov	r12, rdx
	lea	r14, 16[rcx]
	add	rsi, rax
	cmp	r14, QWORD PTR [rcx]
	mov	rbp, r9
	je	.L236
	mov	rax, QWORD PTR 16[rcx]
.L224:
	test	rsi, rsi
	js	.L249
	cmp	rax, rsi
	jnb	.L226
	add	rax, rax
	cmp	rsi, rax
	jnb	.L226
	test	rax, rax
	js	.L227
	lea	rcx, 1[rax]
	mov	rsi, rax
	call	_Znwy
	test	r12, r12
	mov	rdi, rax
	je	.L229
	cmp	r12, 1
	mov	rdx, QWORD PTR [rbx]
	je	.L250
	.p2align 4,,10
	.p2align 3
.L230:
	mov	r8, r12
	mov	rcx, rax
	call	memcpy
.L229:
	test	rbp, rbp
	je	.L231
	cmp	QWORD PTR 144[rsp], 0
	je	.L231
	cmp	QWORD PTR 144[rsp], 1
	lea	rcx, [rdi+r12]
	je	.L251
	mov	r8, QWORD PTR 144[rsp]
	mov	rdx, rbp
	call	memcpy
.L231:
	test	r15, r15
	mov	rbp, QWORD PTR [rbx]
	jne	.L252
.L233:
	cmp	rbp, r14
	je	.L235
	mov	rax, QWORD PTR 16[rbx]
	mov	rcx, rbp
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L235:
	mov	QWORD PTR [rbx], rdi
	mov	QWORD PTR 16[rbx], rsi
	add	rsp, 40
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
.L226:
	mov	rcx, rsi
	add	rcx, 1
	js	.L227
	call	_Znwy
	test	r12, r12
	mov	rdi, rax
	je	.L229
	cmp	r12, 1
	mov	rdx, QWORD PTR [rbx]
	jne	.L230
.L250:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rdi], al
	jmp	.L229
	.p2align 4,,10
	.p2align 3
.L252:
	mov	r10, QWORD PTR 144[rsp]
	lea	rdx, 0[rbp+r13]
	add	r10, r12
	cmp	r15, 1
	lea	rcx, [rdi+r10]
	je	.L253
	mov	r8, r15
	call	memcpy
	jmp	.L233
	.p2align 4,,10
	.p2align 3
.L227:
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L236:
	mov	eax, 15
	jmp	.L224
	.p2align 4,,10
	.p2align 3
.L251:
	movzx	eax, BYTE PTR 0[rbp]
	test	r15, r15
	mov	rbp, QWORD PTR [rbx]
	mov	BYTE PTR [rcx], al
	je	.L233
	jmp	.L252
	.p2align 4,,10
	.p2align 3
.L253:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rcx], al
	jmp	.L233
.L249:
	lea	rcx, .LC9[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC10:
	.ascii "basic_string::append\0"
	.section	.text$_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv
	.def	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv
_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv:
.LFB4114:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	movabs	rax, 9223372036854775807
	mov	r9, QWORD PTR 8[rcx]
	mov	r8, QWORD PTR 24[rcx]
	mov	rdx, QWORD PTR 296[rcx]
	mov	rbx, rcx
	sub	r8, r9
	sub	rax, rdx
	cmp	rax, r8
	jb	.L264
	mov	rcx, QWORD PTR 288[rcx]
	lea	rax, 304[rbx]
	lea	rsi, [r8+rdx]
	cmp	rcx, rax
	je	.L260
	mov	rax, QWORD PTR 304[rbx]
.L256:
	cmp	rax, rsi
	jb	.L257
	test	r8, r8
	je	.L258
	add	rcx, rdx
	cmp	r8, 1
	je	.L265
	mov	rdx, r9
	call	memcpy
	mov	rcx, QWORD PTR 288[rbx]
.L258:
	mov	QWORD PTR 296[rbx], rsi
	mov	BYTE PTR [rcx+rsi], 0
	mov	rax, QWORD PTR 8[rbx]
	mov	QWORD PTR 24[rbx], rax
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L257:
	lea	rcx, 288[rbx]
	mov	QWORD PTR 32[rsp], r8
	xor	r8d, r8d
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rcx, QWORD PTR 288[rbx]
	jmp	.L258
	.p2align 4,,10
	.p2align 3
.L260:
	mov	eax, 15
	jmp	.L256
	.p2align 4,,10
	.p2align 3
.L265:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	mov	rcx, QWORD PTR 288[rbx]
	jmp	.L258
.L264:
	lea	rcx, .LC10[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE
	.def	_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE
_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE:
.LFB3467:
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
	sub	rsp, 800
	.seh_stackalloc	800
	.seh_endprologue
	lea	rdi, _ZTVNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE[rip+16]
	lea	r11, _ZTVNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE[rip+16]
	movq	xmm0, rdi
	mov	rax, QWORD PTR 8[rdx]
	movdqu	xmm1, XMMWORD PTR [r8]
	mov	QWORD PTR 104[rsp], rax
	add	rax, QWORD PTR [rdx]
	lea	r8, 512[rsp]
	mov	rbx, rcx
	movq	xmm2, r8
	mov	QWORD PTR 504[rsp], r8
	lea	r8, 192[rsp]
	punpcklqdq	xmm0, xmm2
	movaps	XMMWORD PTR 480[rsp], xmm0
	movq	xmm0, r11
	movq	xmm3, r8
	movaps	XMMWORD PTR 48[rsp], xmm1
	lea	rcx, 480[rsp]
	punpcklqdq	xmm0, xmm3
	mov	QWORD PTR 112[rsp], rax
	movaps	XMMWORD PTR 160[rsp], xmm0
	lea	rax, _ZTVNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE[rip+16]
	movdqa	xmm0, XMMWORD PTR .LC11[rip]
	lea	rsi, 784[rsp]
	mov	QWORD PTR 448[rsp], rcx
	mov	QWORD PTR 64[rsp], rcx
	lea	rcx, 96[rsp]
	mov	QWORD PTR 96[rsp], rax
	lea	rax, 48[rsp]
	mov	QWORD PTR 496[rsp], 256
	mov	QWORD PTR 768[rsp], rsi
	mov	QWORD PTR 776[rsp], 0
	mov	BYTE PTR 784[rsp], 0
	mov	QWORD PTR 176[rsp], 256
	mov	QWORD PTR 184[rsp], r8
	mov	QWORD PTR 456[rsp], -1
	mov	QWORD PTR 464[rsp], 0
	mov	QWORD PTR 72[rsp], 0
	mov	BYTE PTR 80[rsp], 0
	mov	DWORD PTR 120[rsp], 0
	movaps	XMMWORD PTR 128[rsp], xmm0
	mov	QWORD PTR 144[rsp], rax
.LEHB2:
	call	_ZNSt8__format8_ScannerIcE7_M_scanEv
.LEHE2:
	cmp	BYTE PTR 80[rsp], 0
	jne	.L297
.L267:
	mov	r9, QWORD PTR 488[rsp]
	movabs	rax, 9223372036854775807
	mov	r8, QWORD PTR 504[rsp]
	mov	rdx, QWORD PTR 776[rsp]
	sub	r8, r9
	sub	rax, rdx
	cmp	rax, r8
	jb	.L298
	mov	rcx, QWORD PTR 768[rsp]
	lea	rbp, [r8+rdx]
	cmp	rcx, rsi
	je	.L285
	mov	rax, QWORD PTR 784[rsp]
.L273:
	cmp	rax, rbp
	jb	.L274
	test	r8, r8
	jne	.L299
.L275:
	mov	QWORD PTR 776[rsp], rbp
	lea	rdx, 16[rbx]
	mov	BYTE PTR [rcx+rbp], 0
	mov	rax, QWORD PTR 488[rsp]
	mov	QWORD PTR [rbx], rdx
	mov	QWORD PTR 504[rsp], rax
	mov	rax, QWORD PTR 768[rsp]
	cmp	rax, rsi
	je	.L300
	mov	QWORD PTR [rbx], rax
	mov	rax, QWORD PTR 784[rsp]
	mov	rcx, QWORD PTR 776[rsp]
	mov	QWORD PTR 16[rbx], rax
.L284:
	mov	rax, rbx
	mov	QWORD PTR 8[rbx], rcx
	add	rsp, 800
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L299:
	add	rcx, rdx
	cmp	r8, 1
	je	.L301
	mov	rdx, r9
	call	memcpy
	mov	rcx, QWORD PTR 768[rsp]
	jmp	.L275
	.p2align 4,,10
	.p2align 3
.L297:
	lea	rcx, 72[rsp]
	call	_ZNSt6localeD1Ev
	jmp	.L267
	.p2align 4,,10
	.p2align 3
.L274:
	lea	r12, 768[rsp]
	mov	QWORD PTR 32[rsp], r8
	xor	r8d, r8d
	mov	rcx, r12
.LEHB3:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rcx, QWORD PTR 768[rsp]
	jmp	.L275
	.p2align 4,,10
	.p2align 3
.L285:
	mov	eax, 15
	jmp	.L273
	.p2align 4,,10
	.p2align 3
.L300:
	mov	rcx, QWORD PTR 776[rsp]
	lea	r8, 1[rcx]
	cmp	r8d, 8
	jnb	.L278
	test	r8b, 4
	jne	.L302
	test	r8d, r8d
	je	.L284
	movzx	eax, BYTE PTR [rsi]
	test	r8b, 2
	mov	BYTE PTR 16[rbx], al
	je	.L284
	mov	r8d, r8d
	movzx	eax, WORD PTR -2[rsi+r8]
	mov	WORD PTR -2[rdx+r8], ax
	jmp	.L284
	.p2align 4,,10
	.p2align 3
.L301:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	mov	rcx, QWORD PTR 768[rsp]
	jmp	.L275
	.p2align 4,,10
	.p2align 3
.L278:
	mov	r9d, r8d
	sub	r8d, 1
	mov	r10, QWORD PTR -8[rsi+r9]
	cmp	r8d, 8
	mov	QWORD PTR -8[rdx+r9], r10
	jb	.L284
	and	r8d, -8
	xor	r9d, r9d
.L282:
	mov	r10d, r9d
	add	r9d, 8
	mov	r11, QWORD PTR [rax+r10]
	cmp	r9d, r8d
	mov	QWORD PTR [rdx+r10], r11
	jb	.L282
	jmp	.L284
.L302:
	mov	eax, DWORD PTR [rsi]
	mov	r8d, r8d
	mov	DWORD PTR 16[rbx], eax
	mov	eax, DWORD PTR -4[rsi+r8]
	mov	DWORD PTR -4[rdx+r8], eax
	jmp	.L284
.L298:
	lea	rcx, .LC10[rip]
	lea	r12, 768[rsp]
	call	_ZSt20__throw_length_errorPKc
.LEHE3:
.L286:
	mov	rbx, rax
.L272:
	mov	rcx, r12
	mov	QWORD PTR 480[rsp], rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
.LEHE4:
.L287:
	cmp	BYTE PTR 80[rsp], 0
	mov	rbx, rax
	je	.L271
	lea	rcx, 72[rsp]
	call	_ZNSt6localeD1Ev
.L271:
	lea	r12, 768[rsp]
	jmp	.L272
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3467:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3467-.LLSDACSB3467
.LLSDACSB3467:
	.uleb128 .LEHB2-.LFB3467
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L287-.LFB3467
	.uleb128 0
	.uleb128 .LEHB3-.LFB3467
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L286-.LFB3467
	.uleb128 0
	.uleb128 .LEHB4-.LFB3467
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE3467:
	.section	.text$_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC12:
	.ascii "user={}\0"
	.text
	.p2align 4
	.globl	_Z8safe_logRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.def	_Z8safe_logRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8safe_logRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_Z8safe_logRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:
.LFB3527:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	rax, QWORD PTR [rdx]
	mov	rdx, QWORD PTR 8[rdx]
	mov	QWORD PTR 72[rsp], rax
	mov	rbx, rcx
	lea	rcx, .LC12[rip]
	mov	QWORD PTR 64[rsp], rdx
	lea	rax, 64[rsp]
	mov	QWORD PTR 56[rsp], rcx
	mov	rcx, rbx
	lea	rdx, 48[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	QWORD PTR 48[rsp], 7
	lea	r8, 32[rsp]
	mov	QWORD PTR 32[rsp], 177
	call	_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE
	mov	rax, rbx
	add	rsp, 80
	pop	rbx
	ret
	.seh_endproc
	.section	.text$_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	.def	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE:
.LFB4793:
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
	mov	rdi, QWORD PTR [rdx]
	mov	rbp, QWORD PTR 8[rdx]
	test	rdi, rdi
	mov	rsi, rcx
	jne	.L319
.L305:
	mov	rax, rsi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L319:
	mov	rcx, QWORD PTR 24[rcx]
	mov	rbx, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	rbx, rax
	cmp	rdi, rbx
	jb	.L306
	.p2align 4,,10
	.p2align 3
.L308:
	test	rbx, rbx
	je	.L307
	mov	r8, rbx
	mov	rdx, rbp
	call	memcpy
.L307:
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	add	rbp, rbx
	sub	rdi, rbx
	add	QWORD PTR 24[rsi], rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rsi]
	mov	rbx, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	rbx, rax
	cmp	rdi, rbx
	jnb	.L308
	test	rdi, rdi
	je	.L305
.L306:
	mov	r8, rdi
	mov	rdx, rbp
	call	memcpy
	mov	rax, rsi
	add	QWORD PTR 24[rsi], rdi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc
	.def	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc
_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc:
.LFB4673:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	rbx, QWORD PTR 48[rcx]
	mov	rax, QWORD PTR 8[rcx]
	mov	rcx, QWORD PTR 16[rbx]
	sub	rdx, rax
	mov	QWORD PTR 40[rsp], rax
	mov	QWORD PTR 32[rsp], rdx
	lea	rdx, 32[rsp]
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 48
	pop	rbx
	ret
	.seh_endproc
	.section	.text$_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE
	.def	_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE
_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE:
.LFB4819:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rdx]
	mov	rax, QWORD PTR [rdx]
	mov	DWORD PTR 44[rsp], 0
	mov	rbx, rcx
	mov	r9, rdx
	cmp	rsi, rax
	mov	BYTE PTR 44[rsp], 32
	mov	QWORD PTR 36[rsp], 0
	je	.L322
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L322
	cmp	dl, 123
	je	.L323
	mov	rcx, rsi
	sub	rcx, rax
	cmp	rcx, 1
	jle	.L324
	movzx	ecx, BYTE PTR 1[rax]
	cmp	cl, 62
	je	.L336
	cmp	cl, 94
	je	.L337
	cmp	cl, 60
	je	.L354
	cmp	dl, 62
	je	.L343
	cmp	dl, 94
	je	.L344
	cmp	dl, 60
	jne	.L329
.L345:
	mov	ecx, 1
.L328:
	add	rax, 1
	jmp	.L327
	.p2align 4,,10
	.p2align 3
.L354:
	mov	ecx, 1
.L325:
	mov	BYTE PTR 44[rsp], dl
	add	rax, 2
.L327:
	movzx	edx, BYTE PTR 36[rsp]
	and	edx, -4
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 36[rsp], dl
	je	.L322
.L329:
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	jne	.L353
.L322:
	mov	rdx, QWORD PTR 36[rsp]
	mov	QWORD PTR [rbx], rdx
	movzx	edx, BYTE PTR 44[rsp]
	mov	BYTE PTR 8[rbx], dl
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L324:
	cmp	dl, 62
	je	.L343
	cmp	dl, 94
	je	.L344
	cmp	dl, 60
	je	.L345
.L353:
	cmp	dl, 48
	mov	rcx, rax
	je	.L355
	.p2align 4,,10
	.p2align 3
.L323:
	lea	rcx, 36[rsp]
	mov	r8, rsi
	mov	rdx, rax
	call	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	cmp	rsi, rax
	je	.L322
	movzx	edx, BYTE PTR [rax]
	mov	ecx, edx
	and	ecx, -33
	cmp	cl, 80
	jne	.L333
	cmp	dl, 80
	jne	.L334
	movzx	edx, BYTE PTR 37[rsp]
	and	edx, -121
	or	edx, 8
	mov	BYTE PTR 37[rsp], dl
.L334:
	lea	rcx, 1[rax]
	cmp	rcx, rsi
	je	.L342
	movzx	edx, BYTE PTR 1[rax]
	mov	rax, rcx
.L333:
	cmp	dl, 125
	je	.L322
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L355:
	or	BYTE PTR 36[rsp], 64
	add	rax, 1
	cmp	rsi, rax
	je	.L322
	cmp	BYTE PTR 1[rcx], 125
	jne	.L323
	jmp	.L322
	.p2align 4,,10
	.p2align 3
.L337:
	mov	ecx, 3
	jmp	.L325
	.p2align 4,,10
	.p2align 3
.L336:
	mov	ecx, 2
	jmp	.L325
	.p2align 4,,10
	.p2align 3
.L344:
	mov	ecx, 3
	jmp	.L328
	.p2align 4,,10
	.p2align 3
.L343:
	mov	ecx, 2
	jmp	.L328
.L342:
	mov	rax, rsi
	jmp	.L322
	.seh_endproc
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc:
.LFB4865:
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rdi, QWORD PTR [rcx]
	mov	rsi, QWORD PTR 8[rcx]
	lea	r12, 16[rcx]
	mov	rbx, rcx
	mov	r13d, edx
	lea	rbp, 1[rsi]
	cmp	r12, rdi
	je	.L369
	mov	rax, QWORD PTR 16[rcx]
	cmp	rax, rbp
	jb	.L370
.L358:
	mov	BYTE PTR [rdi+rsi], r13b
	mov	rax, QWORD PTR [rbx]
	mov	QWORD PTR 8[rbx], rbp
	mov	BYTE PTR 1[rax+rsi], 0
	add	rsp, 40
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
.L370:
	test	rbp, rbp
	js	.L371
	lea	r14, [rax+rax]
	cmp	rbp, r14
	jb	.L372
	mov	rcx, rsi
	mov	r14, rbp
	add	rcx, 2
	js	.L362
.L363:
	call	_Znwy
	test	rsi, rsi
	mov	rdi, rax
	jne	.L359
	mov	r15, QWORD PTR [rbx]
.L364:
	cmp	r12, r15
	je	.L367
	mov	rax, QWORD PTR 16[rbx]
	mov	rcx, r15
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L367:
	mov	QWORD PTR [rbx], rdi
	mov	QWORD PTR 16[rbx], r14
	jmp	.L358
	.p2align 4,,10
	.p2align 3
.L369:
	cmp	rbp, 16
	jne	.L358
	mov	ecx, 31
	mov	r14d, 30
	call	_Znwy
	mov	rdi, rax
.L359:
	cmp	rsi, 1
	mov	r15, QWORD PTR [rbx]
	je	.L373
	mov	r8, rsi
	mov	rdx, r15
	mov	rcx, rdi
	call	memcpy
	jmp	.L364
	.p2align 4,,10
	.p2align 3
.L373:
	movzx	eax, BYTE PTR [r15]
	mov	BYTE PTR [rdi], al
	jmp	.L364
	.p2align 4,,10
	.p2align 3
.L372:
	lea	rcx, 1[r14]
	test	r14, r14
	jns	.L363
.L362:
	call	_ZSt17__throw_bad_allocv
.L371:
	lea	rcx, .LC9[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	.def	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE:
.LFB4911:
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
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rdx]
	mov	rax, QWORD PTR [rdx]
	mov	DWORD PTR 60[rsp], 0
	mov	rdi, rcx
	mov	rbx, rdx
	cmp	rsi, rax
	mov	BYTE PTR 60[rsp], 32
	mov	QWORD PTR 52[rsp], 0
	je	.L375
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L375
	cmp	dl, 123
	je	.L376
	mov	rcx, rsi
	sub	rcx, rax
	cmp	rcx, 1
	jle	.L377
	movzx	ecx, BYTE PTR 1[rax]
	cmp	cl, 62
	je	.L422
	cmp	cl, 94
	je	.L423
	cmp	cl, 60
	je	.L473
	cmp	dl, 62
	je	.L432
	cmp	dl, 94
	je	.L433
	cmp	dl, 60
	jne	.L382
.L434:
	mov	ecx, 1
.L381:
	add	rax, 1
	jmp	.L380
	.p2align 4,,10
	.p2align 3
.L473:
	mov	ecx, 1
.L378:
	mov	BYTE PTR 60[rsp], dl
	add	rax, 2
.L380:
	movzx	edx, BYTE PTR 52[rsp]
	and	edx, -4
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 52[rsp], dl
	je	.L375
.L382:
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	jne	.L471
.L375:
	mov	rdx, QWORD PTR 52[rsp]
	mov	QWORD PTR [rdi], rdx
	movzx	edx, BYTE PTR 60[rsp]
	mov	BYTE PTR 8[rdi], dl
	add	rsp, 72
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L377:
	cmp	dl, 62
	je	.L432
	cmp	dl, 94
	je	.L433
	cmp	dl, 60
	je	.L434
.L471:
	lea	ecx, -32[rdx]
	mov	r9, rax
	cmp	cl, 13
	ja	.L472
	lea	r8, CSWTCH.756[rip]
	movzx	ecx, cl
	mov	ecx, DWORD PTR [r8+rcx*4]
	test	ecx, ecx
	jne	.L386
	cmp	dl, 35
	jne	.L391
.L387:
	or	BYTE PTR 52[rsp], 16
	add	rax, 1
	cmp	rsi, rax
	je	.L375
	movzx	edx, BYTE PTR 1[r9]
	cmp	dl, 125
	je	.L375
.L472:
	cmp	dl, 48
	mov	r9, rax
	je	.L474
.L391:
	cmp	dl, 46
	jne	.L376
.L392:
	movzx	ecx, BYTE PTR 1[rax]
	lea	r8, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	lea	rbp, 1[rax]
	cmp	BYTE PTR [r8+rcx], 9
	ja	.L394
	lea	rcx, 32[rsp]
	mov	rdx, rbp
	mov	r8, rsi
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	mov	rax, QWORD PTR 40[rsp]
	mov	rdx, QWORD PTR 32[rsp]
	test	rax, rax
	je	.L475
	cmp	rbp, rax
	mov	WORD PTR 58[rsp], dx
	je	.L397
	mov	ecx, 1
.L396:
	movzx	edx, BYTE PTR 53[rsp]
	add	ecx, ecx
	and	edx, -7
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 53[rsp], dl
	je	.L375
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L375
	cmp	dl, 76
	je	.L431
	sub	edx, 65
	cmp	dl, 38
	ja	.L409
	lea	rcx, .L411[rip]
	movzx	edx, dl
	movsx	rdx, DWORD PTR [rcx+rdx*4]
	add	rdx, rcx
	jmp	rdx
	.section .rdata,"dr"
	.align 4
.L411:
	.long	.L417-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L416-.L411
	.long	.L412-.L411
	.long	.L415-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L414-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L409-.L411
	.long	.L413-.L411
	.long	.L412-.L411
	.long	.L410-.L411
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L386:
	movzx	edx, BYTE PTR 52[rsp]
	and	ecx, 3
	add	rax, 1
	sal	ecx, 2
	and	edx, -13
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 52[rsp], dl
	je	.L375
	movzx	edx, BYTE PTR 1[r9]
	cmp	dl, 125
	je	.L375
	cmp	dl, 35
	mov	r9, rax
	je	.L387
	jmp	.L472
	.p2align 4,,10
	.p2align 3
.L376:
	lea	rcx, 52[rsp]
	mov	r9, rbx
	mov	r8, rsi
	mov	rdx, rax
	call	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	cmp	rsi, rax
	je	.L375
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L375
	cmp	dl, 46
	je	.L392
	cmp	dl, 76
	je	.L431
.L420:
	sub	edx, 65
	cmp	dl, 38
	ja	.L418
	lea	rcx, .L419[rip]
	movzx	edx, dl
	movsx	rdx, DWORD PTR [rcx+rdx*4]
	add	rdx, rcx
	jmp	rdx
	.section .rdata,"dr"
	.align 4
.L419:
	.long	.L417-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L416-.L419
	.long	.L412-.L419
	.long	.L415-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L414-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L418-.L419
	.long	.L413-.L419
	.long	.L412-.L419
	.long	.L410-.L419
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
.L414:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 8
	mov	BYTE PTR 53[rsp], dl
	.p2align 4,,10
	.p2align 3
.L418:
	cmp	rsi, rax
	je	.L375
.L409:
	cmp	BYTE PTR [rax], 125
	je	.L375
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L412:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 40
	mov	BYTE PTR 53[rsp], dl
	jmp	.L418
.L416:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 32
	mov	BYTE PTR 53[rsp], dl
	jmp	.L418
.L415:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 56
	mov	BYTE PTR 53[rsp], dl
	jmp	.L418
.L417:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 16
	mov	BYTE PTR 53[rsp], dl
	jmp	.L418
.L410:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 48
	mov	BYTE PTR 53[rsp], dl
	jmp	.L418
.L413:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 24
	mov	BYTE PTR 53[rsp], dl
	jmp	.L418
	.p2align 4,,10
	.p2align 3
.L474:
	or	BYTE PTR 52[rsp], 64
	add	rax, 1
	cmp	rsi, rax
	je	.L375
	movzx	edx, BYTE PTR 1[r9]
	cmp	dl, 125
	je	.L375
	jmp	.L391
	.p2align 4,,10
	.p2align 3
.L423:
	mov	ecx, 3
	jmp	.L378
	.p2align 4,,10
	.p2align 3
.L422:
	mov	ecx, 2
	jmp	.L378
	.p2align 4,,10
	.p2align 3
.L433:
	mov	ecx, 3
	jmp	.L381
	.p2align 4,,10
	.p2align 3
.L432:
	mov	ecx, 2
	jmp	.L381
	.p2align 4,,10
	.p2align 3
.L431:
	or	BYTE PTR 52[rsp], 32
	mov	rdx, rax
	add	rax, 1
	cmp	rsi, rax
	je	.L375
	movzx	edx, BYTE PTR 1[rdx]
	cmp	dl, 125
	je	.L375
	jmp	.L420
	.p2align 4,,10
	.p2align 3
.L394:
	cmp	cl, 123
	je	.L476
.L397:
	lea	rcx, .LC8[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L476:
	lea	rdx, 2[rax]
	cmp	rsi, rdx
	je	.L477
	movzx	ecx, BYTE PTR 2[rax]
	cmp	cl, 125
	je	.L478
	cmp	cl, 48
	je	.L479
	lea	r8d, -49[rcx]
	cmp	r8b, 8
	jbe	.L404
.L405:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L478:
	cmp	DWORD PTR 16[rbx], 1
	je	.L407
	mov	rax, QWORD PTR 24[rbx]
	mov	DWORD PTR 16[rbx], 2
	lea	rcx, 1[rax]
	mov	WORD PTR 58[rsp], ax
	mov	QWORD PTR 24[rbx], rcx
.L401:
	lea	rax, 1[rdx]
	cmp	rbp, rax
	je	.L397
	mov	ecx, 2
	jmp	.L396
.L479:
	lea	rdx, 3[rax]
	xor	eax, eax
.L403:
	cmp	rsi, rdx
	je	.L405
	test	rdx, rdx
	je	.L405
.L421:
	cmp	BYTE PTR [rdx], 125
	jne	.L405
	cmp	DWORD PTR 16[rbx], 2
	je	.L407
	mov	DWORD PTR 16[rbx], 1
	mov	WORD PTR 58[rsp], ax
	jmp	.L401
.L404:
	lea	r8, 3[rax]
	cmp	rsi, r8
	je	.L405
	movzx	eax, BYTE PTR 3[rax]
	sub	eax, 48
	cmp	al, 9
	ja	.L406
	lea	rcx, 32[rsp]
	mov	r8, rsi
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzx	eax, WORD PTR 32[rsp]
	mov	rdx, QWORD PTR 40[rsp]
	jmp	.L403
.L406:
	movsx	ax, cl
	mov	rdx, r8
	sub	eax, 48
	jmp	.L421
.L475:
	lea	rcx, .LC7[rip]
	call	_ZSt20__throw_format_errorPKc
.L477:
	lea	rcx, .LC4[rip]
	call	_ZSt20__throw_format_errorPKc
.L407:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
	nop
	.seh_endproc
	.section	.text$_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	.def	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE:
.LFB5002:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rdx]
	mov	eax, r8d
	mov	DWORD PTR 44[rsp], 0
	mov	rbx, rcx
	mov	r9, rdx
	and	eax, 15
	mov	edi, r8d
	mov	BYTE PTR 44[rsp], 32
	mov	QWORD PTR 36[rsp], 0
	sal	eax, 3
	mov	BYTE PTR 37[rsp], al
	mov	rax, QWORD PTR [rdx]
	cmp	rsi, rax
	je	.L481
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L481
	cmp	dl, 123
	je	.L496
	mov	rcx, rsi
	sub	rcx, rax
	cmp	rcx, 1
	jle	.L483
	movzx	ecx, BYTE PTR 1[rax]
	cmp	cl, 62
	je	.L511
	cmp	cl, 94
	je	.L512
	cmp	cl, 60
	je	.L549
	cmp	dl, 62
	je	.L520
	cmp	dl, 94
	je	.L521
	cmp	dl, 60
	jne	.L488
.L522:
	mov	ecx, 1
.L487:
	add	rax, 1
	jmp	.L486
	.p2align 4,,10
	.p2align 3
.L549:
	mov	ecx, 1
.L484:
	mov	BYTE PTR 44[rsp], dl
	add	rax, 2
.L486:
	movzx	edx, BYTE PTR 36[rsp]
	and	edx, -4
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 36[rsp], dl
	je	.L481
.L488:
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	jne	.L547
.L481:
	mov	rdx, QWORD PTR 36[rsp]
	mov	QWORD PTR [rbx], rdx
	movzx	edx, BYTE PTR 44[rsp]
	mov	BYTE PTR 8[rbx], dl
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L483:
	cmp	dl, 62
	je	.L520
	cmp	dl, 94
	je	.L521
	cmp	dl, 60
	je	.L522
.L547:
	lea	ecx, -32[rdx]
	mov	r10, rax
	cmp	cl, 13
	ja	.L548
	lea	r8, CSWTCH.756[rip]
	movzx	ecx, cl
	mov	ecx, DWORD PTR [r8+rcx*4]
	test	ecx, ecx
	jne	.L492
	cmp	dl, 35
	jne	.L496
.L493:
	or	BYTE PTR 36[rsp], 16
	add	rax, 1
	cmp	rsi, rax
	je	.L481
	movzx	edx, BYTE PTR 1[r10]
	cmp	dl, 125
	je	.L481
.L548:
	cmp	dl, 48
	mov	rcx, rax
	jne	.L496
	or	BYTE PTR 36[rsp], 64
	add	rax, 1
	cmp	rsi, rax
	je	.L481
	cmp	BYTE PTR 1[rcx], 125
	je	.L481
	.p2align 4,,10
	.p2align 3
.L496:
	lea	rcx, 36[rsp]
	mov	r8, rsi
	mov	rdx, rax
	call	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	cmp	rsi, rax
	je	.L481
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L481
	cmp	dl, 76
	je	.L550
.L497:
	sub	edx, 66
	cmp	dl, 54
	ja	.L509
	lea	rcx, .L510[rip]
	movzx	edx, dl
	movsx	rdx, DWORD PTR [rcx+rdx*4]
	add	rdx, rcx
	jmp	rdx
	.section .rdata,"dr"
	.align 4
.L510:
	.long	.L500-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L506-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L498-.L510
	.long	.L501-.L510
	.long	.L503-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L504-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L507-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L509-.L510
	.long	.L505-.L510
	.section	.text$_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L492:
	movzx	edx, BYTE PTR 36[rsp]
	and	ecx, 3
	add	rax, 1
	sal	ecx, 2
	and	edx, -13
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 36[rsp], dl
	je	.L481
	movzx	edx, BYTE PTR 1[r10]
	cmp	dl, 125
	je	.L481
	cmp	dl, 35
	mov	r10, rax
	je	.L493
	jmp	.L548
	.p2align 4,,10
	.p2align 3
.L506:
	add	rax, 1
	mov	edx, 6
	.p2align 4,,10
	.p2align 3
.L499:
	movzx	ecx, BYTE PTR 37[rsp]
	sal	edx, 3
	and	ecx, -121
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 37[rsp], dl
	je	.L481
	.p2align 4,,10
	.p2align 3
.L509:
	cmp	BYTE PTR [rax], 125
	je	.L481
.L502:
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L500:
	add	rax, 1
	mov	edx, 3
	jmp	.L499
.L505:
	add	rax, 1
	mov	edx, 5
	jmp	.L499
.L504:
	add	rax, 1
	mov	edx, 4
	jmp	.L499
.L503:
	add	rax, 1
	mov	edx, 1
	jmp	.L499
.L498:
	add	rax, 1
	mov	edx, 2
	jmp	.L499
.L501:
	test	edi, edi
	je	.L502
	add	rax, 1
	mov	edx, 7
	jmp	.L499
.L507:
	test	edi, edi
	jne	.L502
	add	rax, 1
	xor	edx, edx
	jmp	.L499
	.p2align 4,,10
	.p2align 3
.L512:
	mov	ecx, 3
	jmp	.L484
	.p2align 4,,10
	.p2align 3
.L511:
	mov	ecx, 2
	jmp	.L484
	.p2align 4,,10
	.p2align 3
.L521:
	mov	ecx, 3
	jmp	.L487
	.p2align 4,,10
	.p2align 3
.L520:
	mov	ecx, 2
	jmp	.L487
	.p2align 4,,10
	.p2align 3
.L550:
	or	BYTE PTR 36[rsp], 32
	lea	rcx, 1[rax]
	cmp	rsi, rcx
	jne	.L551
	mov	rax, rsi
	jmp	.L481
.L551:
	movzx	edx, BYTE PTR 1[rax]
	mov	rax, rcx
	cmp	dl, 125
	je	.L481
	jmp	.L497
	.seh_endproc
	.section	.text$_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
	.def	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_:
.LFB5034:
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
	sub	rsp, 104
	.seh_stackalloc	104
	movaps	XMMWORD PTR 80[rsp], xmm6
	.seh_savexmm	xmm6, 80
	.seh_endprologue
	movdqu	xmm6, XMMWORD PTR [rdx]
	mov	edx, DWORD PTR 192[rsp]
	cmp	r8d, 3
	mov	rbx, rcx
	mov	rsi, r9
	je	.L596
	cmp	r8d, 2
	je	.L574
	cmp	r9, 31
	ja	.L597
	test	r9, r9
	jne	.L598
	lea	rdx, 32[rsp]
	movaps	XMMWORD PTR 32[rsp], xmm6
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	rbx, rax
	jmp	.L559
	.p2align 4,,10
	.p2align 3
.L574:
	mov	rdi, r9
	xor	r12d, r12d
.L554:
	cmp	rsi, 31
	ja	.L575
	test	rsi, rsi
	jne	.L560
	test	rdi, rdi
	je	.L595
	lea	r13, 48[rsp]
	jmp	.L562
	.p2align 4,,10
	.p2align 3
.L575:
	mov	esi, 32
.L560:
	lea	r13, 48[rsp]
	cmp	esi, 8
	movsx	ecx, dl
	mov	r8d, esi
	mov	rdx, r13
	jnb	.L599
.L563:
	and	r8d, 7
	je	.L567
	xor	eax, eax
.L566:
	mov	r9d, eax
	add	eax, 1
	cmp	eax, r8d
	mov	BYTE PTR [rdx+r9], cl
	jb	.L566
.L567:
	test	rdi, rdi
	je	.L595
	lea	rbp, 32[rsp]
	cmp	rsi, rdi
	jnb	.L570
.L562:
	lea	rbp, 32[rsp]
	.p2align 4,,10
	.p2align 3
.L571:
	mov	rcx, rbx
	mov	rdx, rbp
	sub	rdi, rsi
	mov	QWORD PTR 32[rsp], rsi
	mov	QWORD PTR 40[rsp], r13
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	cmp	rsi, rdi
	mov	rbx, rax
	jb	.L571
	test	rdi, rdi
	jne	.L570
.L569:
	mov	rcx, rbx
	mov	rdx, rbp
	movaps	XMMWORD PTR 32[rsp], xmm6
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	test	r12, r12
	mov	rbx, rax
	je	.L559
.L556:
	lea	r13, 48[rsp]
	cmp	rsi, r12
	jnb	.L558
	.p2align 4,,10
	.p2align 3
.L572:
	mov	rcx, rbx
	mov	rdx, rbp
	sub	r12, rsi
	mov	QWORD PTR 32[rsp], rsi
	mov	QWORD PTR 40[rsp], r13
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	cmp	rsi, r12
	mov	rbx, rax
	jb	.L572
	test	r12, r12
	jne	.L558
.L559:
	movaps	xmm6, XMMWORD PTR 80[rsp]
	mov	rax, rbx
	add	rsp, 104
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L596:
	mov	rdi, r9
	and	esi, 1
	shr	rdi
	add	rsi, rdi
	mov	r12, rsi
	jmp	.L554
	.p2align 4,,10
	.p2align 3
.L598:
	lea	r13, 48[rsp]
	movsx	edx, dl
	mov	r8, r9
	lea	rbp, 32[rsp]
	mov	rcx, r13
	mov	r12, rsi
	call	memset
	mov	rcx, rbx
	mov	rdx, rbp
	movaps	XMMWORD PTR 32[rsp], xmm6
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	rbx, rax
.L558:
	mov	rcx, rbx
	mov	rdx, rbp
	mov	QWORD PTR 32[rsp], r12
	mov	QWORD PTR 40[rsp], r13
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	rbx, rax
	jmp	.L559
	.p2align 4,,10
	.p2align 3
.L570:
	mov	rcx, rbx
	mov	rdx, rbp
	mov	QWORD PTR 32[rsp], rdi
	mov	QWORD PTR 40[rsp], r13
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	rbx, rax
	jmp	.L569
	.p2align 4,,10
	.p2align 3
.L599:
	movabs	rax, 72340172838076673
	movzx	r9d, cl
	mov	r10d, esi
	imul	r9, rax
	and	r10d, -8
	xor	eax, eax
.L564:
	mov	edx, eax
	add	eax, 8
	cmp	eax, r10d
	mov	QWORD PTR 0[r13+rdx], r9
	jb	.L564
	lea	rdx, 0[r13+rax]
	jmp	.L563
	.p2align 4,,10
	.p2align 3
.L597:
	lea	rbp, 32[rsp]
	movzx	edx, dl
	movaps	XMMWORD PTR 32[rsp], xmm6
	mov	r12, rsi
	movabs	rax, 72340172838076673
	mov	esi, 32
	imul	rdx, rax
	mov	QWORD PTR 48[rsp], rdx
	mov	QWORD PTR 56[rsp], rdx
	mov	QWORD PTR 64[rsp], rdx
	mov	QWORD PTR 72[rsp], rdx
	mov	rdx, rbp
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	rbx, rax
	jmp	.L556
.L595:
	lea	rbp, 32[rsp]
	jmp	.L569
	.seh_endproc
	.section	.text$_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	.def	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_:
.LFB5119:
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
	.seh_endprologue
	movsx	rax, BYTE PTR [r8]
	lea	ebx, -1[rax]
	mov	r10, rcx
	mov	r11d, edx
	mov	rcx, QWORD PTR 96[rsp]
	cmp	bl, 125
	mov	rdx, QWORD PTR 88[rsp]
	ja	.L601
	mov	rbx, rcx
	sub	rbx, rdx
	cmp	rbx, rax
	jle	.L601
	lea	rbx, -1[r9]
	xor	r12d, r12d
	xor	esi, esi
	jmp	.L604
	.p2align 4,,10
	.p2align 3
.L643:
	add	rsi, 1
.L603:
	lea	rbp, [r8+rsi]
	movsx	rax, BYTE PTR 0[rbp]
	lea	r9d, -1[rax]
	cmp	r9b, 125
	ja	.L621
	mov	r9, rcx
	sub	r9, rdx
	cmp	r9, rax
	jle	.L621
.L604:
	sub	rcx, rax
	cmp	rsi, rbx
	jb	.L643
	add	r12, 1
	jmp	.L603
	.p2align 4,,10
	.p2align 3
.L621:
	lea	rdi, -1[r12]
	cmp	rdx, rcx
	lea	rbx, -1[rsi]
	je	.L644
.L616:
	mov	r13, rcx
	xor	eax, eax
	sub	r13, rdx
	.p2align 4,,10
	.p2align 3
.L607:
	movzx	r9d, BYTE PTR [rdx+rax]
	mov	BYTE PTR [r10+rax], r9b
	add	rax, 1
	cmp	rax, r13
	jne	.L607
	lea	rdx, [r10+rax]
.L606:
	test	r12, r12
	je	.L608
	.p2align 4,,10
	.p2align 3
.L611:
	mov	BYTE PTR [rdx], r11b
	movzx	r10d, BYTE PTR 0[rbp]
	lea	r12, 1[rdx]
	test	r10b, r10b
	jle	.L618
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L610:
	movzx	r9d, BYTE PTR [rcx+rax]
	mov	BYTE PTR 1[rdx+rax], r9b
	add	rax, 1
	cmp	rax, r10
	jne	.L610
	lea	rdx, [r12+rax]
	add	rcx, rax
.L609:
	sub	rdi, 1
	jnb	.L611
.L608:
	test	rsi, rsi
	je	.L600
	.p2align 4,,10
	.p2align 3
.L615:
	mov	BYTE PTR [rdx], r11b
	movzx	r10d, BYTE PTR [r8+rbx]
	lea	rsi, 1[rdx]
	test	r10b, r10b
	jle	.L619
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L614:
	movzx	r9d, BYTE PTR [rcx+rax]
	mov	BYTE PTR 1[rdx+rax], r9b
	add	rax, 1
	cmp	r10, rax
	jne	.L614
	lea	rdx, [rsi+r10]
	add	rcx, r10
.L613:
	sub	rbx, 1
	jnb	.L615
.L600:
	mov	rax, rdx
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L619:
	mov	rdx, rsi
	jmp	.L613
	.p2align 4,,10
	.p2align 3
.L618:
	mov	rdx, r12
	jmp	.L609
.L601:
	cmp	rcx, rdx
	je	.L645
	mov	rbp, r8
	mov	rbx, -1
	mov	rdi, -1
	xor	r12d, r12d
	xor	esi, esi
	jmp	.L616
.L644:
	mov	rdx, r10
	jmp	.L606
.L645:
	mov	rdx, r10
	jmp	.L600
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC13:
	.ascii "format error: argument used for width or precision must be a non-negative integer\0"
	.section	.text$_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
	.def	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E:
.LFB5121:
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	lea	rdx, .L649[rip]
	mov	rax, QWORD PTR [rcx]
	mov	QWORD PTR 32[rsp], rax
	movzx	eax, BYTE PTR 16[rcx]
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L649:
	.long	.L654-.L649
	.long	.L655-.L649
	.long	.L655-.L649
	.long	.L653-.L649
	.long	.L652-.L649
	.long	.L651-.L649
	.long	.L650-.L649
	.long	.L655-.L649
	.long	.L655-.L649
	.long	.L655-.L649
	.long	.L655-.L649
	.long	.L655-.L649
	.long	.L655-.L649
	.long	.L655-.L649
	.long	.L655-.L649
	.long	.L655-.L649
	.section	.text$_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L651:
	mov	rax, QWORD PTR 32[rsp]
	test	rax, rax
	js	.L655
.L646:
	add	rsp, 72
	ret
	.p2align 4,,10
	.p2align 3
.L652:
	mov	eax, DWORD PTR 32[rsp]
	add	rsp, 72
	ret
	.p2align 4,,10
	.p2align 3
.L653:
	movsx	rax, DWORD PTR 32[rsp]
	test	eax, eax
	jns	.L646
.L655:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L650:
	mov	rax, QWORD PTR 32[rsp]
	add	rsp, 72
	ret
.L654:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	nop
	.seh_endproc
	.section	.text$_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	.def	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE:
.LFB4926:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 112
	.seh_stackalloc	112
	movaps	XMMWORD PTR 96[rsp], xmm6
	.seh_savexmm	xmm6, 96
	.seh_endprologue
	movzx	eax, WORD PTR [r9]
	movdqu	xmm6, XMMWORD PTR [rcx]
	and	ax, 384
	mov	rsi, r8
	mov	rdi, rdx
	mov	r8d, DWORD PTR 176[rsp]
	cmp	ax, 128
	mov	rbx, r9
	je	.L668
	cmp	ax, 256
	je	.L660
.L664:
	mov	rcx, QWORD PTR 16[rsi]
	lea	rdx, 48[rsp]
	movaps	XMMWORD PTR 48[rsp], xmm6
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	nop
	movaps	xmm6, XMMWORD PTR 96[rsp]
	add	rsp, 112
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L668:
	movzx	r9d, WORD PTR 4[r9]
.L659:
	cmp	rdi, r9
	jnb	.L664
	movzx	edx, BYTE PTR [rbx]
	mov	rcx, QWORD PTR 16[rsi]
	mov	eax, edx
	and	eax, 3
	and	edx, 3
	cmovne	r8d, eax
	movsx	eax, BYTE PTR 8[rbx]
	sub	r9, rdi
	movaps	XMMWORD PTR 48[rsp], xmm6
	lea	rdx, 48[rsp]
	mov	DWORD PTR 32[rsp], eax
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
	nop
	movaps	xmm6, XMMWORD PTR 96[rsp]
	add	rsp, 112
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L660:
	movzx	edx, BYTE PTR [rsi]
	mov	BYTE PTR 80[rsp], 0
	movzx	eax, WORD PTR 4[r9]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L669
	test	cl, cl
	jne	.L663
	mov	rdx, QWORD PTR [rsi]
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L663
	sal	rax, 5
	add	rax, QWORD PTR 8[rsi]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 64[rsp], rdx
	mov	rdx, QWORD PTR 8[rax]
	movzx	eax, BYTE PTR 16[rax]
	mov	QWORD PTR 72[rsp], rdx
	mov	BYTE PTR 80[rsp], al
	.p2align 4,,10
	.p2align 3
.L663:
	lea	rcx, 64[rsp]
	mov	DWORD PTR 176[rsp], r8d
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
	mov	r8d, DWORD PTR 176[rsp]
	mov	r9, rax
	jmp	.L659
	.p2align 4,,10
	.p2align 3
.L669:
	mov	rdx, QWORD PTR [rsi]
	lea	rcx, [rax+rax*4]
	sal	rax, 4
	add	rax, QWORD PTR 8[rsi]
	shr	rdx, 4
	shr	rdx, cl
	and	edx, 31
	mov	BYTE PTR 80[rsp], dl
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR 64[rsp], rdx
	mov	QWORD PTR 72[rsp], rax
	jmp	.L663
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
	.def	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE:
.LFB4924:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	mov	rbx, QWORD PTR [rdx]
	test	WORD PTR [rcx], 1920
	mov	rsi, QWORD PTR 8[rdx]
	movzx	edx, BYTE PTR 1[rcx]
	mov	r9, rcx
	mov	rax, rbx
	je	.L681
	and	edx, 6
	jne	.L682
.L673:
	lea	rcx, 48[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	rdx, rax
	mov	QWORD PTR 48[rsp], rax
	mov	QWORD PTR 56[rsp], rsi
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	add	rsp, 104
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L682:
	cmp	dl, 2
	je	.L683
	cmp	dl, 4
	jne	.L673
	movzx	edx, BYTE PTR [r8]
	mov	BYTE PTR 80[rsp], 0
	movzx	eax, WORD PTR 6[rcx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L684
	test	cl, cl
	jne	.L677
	mov	rdx, QWORD PTR [r8]
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L677
	sal	rax, 5
	add	rax, QWORD PTR 8[r8]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 64[rsp], rdx
	mov	rdx, QWORD PTR 8[rax]
	movzx	eax, BYTE PTR 16[rax]
	mov	QWORD PTR 72[rsp], rdx
	mov	BYTE PTR 80[rsp], al
	.p2align 4,,10
	.p2align 3
.L677:
	lea	rcx, 64[rsp]
	mov	QWORD PTR 144[rsp], r8
	mov	QWORD PTR 128[rsp], r9
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
	mov	r8, QWORD PTR 144[rsp]
	mov	r9, QWORD PTR 128[rsp]
	jmp	.L675
	.p2align 4,,10
	.p2align 3
.L681:
	mov	rcx, QWORD PTR 16[r8]
	lea	rdx, 48[rsp]
	mov	QWORD PTR 48[rsp], rbx
	mov	QWORD PTR 56[rsp], rsi
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	add	rsp, 104
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L683:
	movzx	eax, WORD PTR 6[rcx]
.L675:
	cmp	rbx, rax
	cmovbe	rax, rbx
	jmp	.L673
	.p2align 4,,10
	.p2align 3
.L684:
	mov	rdx, QWORD PTR [r8]
	lea	rcx, [rax+rax*4]
	sal	rax, 4
	add	rax, QWORD PTR 8[r8]
	shr	rdx, 4
	shr	rdx, cl
	and	edx, 31
	mov	BYTE PTR 80[rsp], dl
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR 64[rsp], rdx
	mov	QWORD PTR 72[rsp], rax
	jmp	.L677
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	.def	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_:
.LFB5016:
	push	rbp
	.seh_pushreg	rbp
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 168
	.seh_stackalloc	168
	lea	rbp, 160[rsp]
	.seh_setframe	rbp, 160
	.seh_endprologue
	movzx	eax, WORD PTR [rcx]
	mov	r15, QWORD PTR [rdx]
	mov	r14, QWORD PTR 8[rdx]
	and	ax, 384
	mov	rbx, rcx
	mov	rdi, r8
	cmp	ax, 128
	mov	rsi, r9
	mov	r12, r15
	mov	r13, r14
	je	.L737
	cmp	ax, 256
	je	.L738
	test	BYTE PTR [rcx], 32
	mov	QWORD PTR -48[rbp], 0
	mov	BYTE PTR -40[rbp], 0
	jne	.L719
	mov	rcx, QWORD PTR 16[r9]
.L716:
	lea	rdx, -64[rbp]
	mov	QWORD PTR -64[rbp], r12
	mov	QWORD PTR -56[rbp], r13
.LEHB5:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L708:
	cmp	BYTE PTR -40[rbp], 0
	jne	.L739
.L725:
	lea	rsp, 8[rbp]
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L737:
	movzx	eax, WORD PTR 4[rcx]
	mov	QWORD PTR -72[rbp], rax
.L687:
	test	BYTE PTR [rbx], 32
	mov	QWORD PTR -48[rbp], 0
	mov	BYTE PTR -40[rbp], 0
	jne	.L715
.L691:
	mov	rax, QWORD PTR -72[rbp]
	mov	rcx, QWORD PTR 16[rsi]
	cmp	r12, rax
	jnb	.L716
	movzx	edx, BYTE PTR [rbx]
	mov	rax, rcx
	movzx	r9d, BYTE PTR 8[rbx]
	mov	rbx, QWORD PTR -72[rbp]
	mov	r8d, edx
	sub	rbx, r12
	and	r8d, 3
	jne	.L740
	and	edx, 64
	je	.L717
	test	rdi, rdi
	jne	.L741
	lea	rsi, -64[rbp]
	mov	edx, 48
	mov	r8d, 2
	jmp	.L710
	.p2align 4,,10
	.p2align 3
.L739:
	lea	rcx, -48[rbp]
	mov	QWORD PTR -72[rbp], rax
	call	_ZNSt6localeD1Ev
	mov	rax, QWORD PTR -72[rbp]
	jmp	.L725
	.p2align 4,,10
	.p2align 3
.L719:
	mov	QWORD PTR -72[rbp], 0
.L715:
	cmp	BYTE PTR 32[rsi], 0
	lea	rdx, 24[rsi]
	je	.L742
.L692:
	lea	rax, -32[rbp]
	mov	rcx, rax
	mov	QWORD PTR -80[rbp], rax
	call	_ZNSt6localeC1ERKS_
	cmp	BYTE PTR -40[rbp], 0
	jne	.L743
	mov	rdx, QWORD PTR -80[rbp]
	lea	rax, -48[rbp]
	mov	rcx, rax
	mov	QWORD PTR -88[rbp], rax
	call	_ZNSt6localeC1ERKS_
	mov	rcx, QWORD PTR -80[rbp]
	mov	BYTE PTR -40[rbp], 1
	call	_ZNSt6localeD1Ev
	cmp	BYTE PTR -40[rbp], 0
	je	.L744
.L695:
	mov	rdx, QWORD PTR -88[rbp]
	mov	rcx, QWORD PTR -80[rbp]
	call	_ZNKSt6locale4nameB5cxx11Ev
	cmp	QWORD PTR -24[rbp], 1
	lea	rax, -16[rbp]
	mov	rcx, QWORD PTR -32[rbp]
	je	.L745
.L697:
	cmp	rcx, rax
	mov	QWORD PTR -88[rbp], rax
	je	.L700
	mov	rax, QWORD PTR -16[rbp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L700:
	mov	rcx, QWORD PTR .refptr._ZNSt7__cxx118numpunctIcE2idE[rip]
	call	_ZNKSt6locale2id5_M_idEv
	mov	rdx, rax
	mov	rax, QWORD PTR -48[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	rdx, QWORD PTR [rax+rdx*8]
	test	rdx, rdx
	mov	QWORD PTR -104[rbp], rdx
	je	.L702
	mov	rax, QWORD PTR [rdx]
	mov	rcx, QWORD PTR -80[rbp]
	call	[QWORD PTR 32[rax]]
.LEHE5:
	mov	rax, QWORD PTR -24[rbp]
	test	rax, rax
	mov	QWORD PTR -96[rbp], rax
	je	.L704
	mov	rax, r15
	sub	rax, rdi
	lea	rax, 15[rdi+rax*2]
	and	rax, -16
	call	___chkstk_ms
	sub	rsp, rax
	test	rdi, rdi
	lea	r13, 48[rsp]
	jne	.L746
.L705:
	mov	rcx, QWORD PTR -104[rbp]
	lea	r12, [r14+rdi]
	add	r14, r15
	mov	r15, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR [rcx]
.LEHB6:
	call	[QWORD PTR 24[rax]]
.LEHE6:
	mov	QWORD PTR 32[rsp], r12
	lea	rcx, 0[r13+rdi]
	movsx	edx, al
	mov	r8, r15
	mov	QWORD PTR 40[rsp], r14
	mov	r9, QWORD PTR -96[rbp]
	call	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	sub	rax, r13
	mov	r12, rax
.L704:
	mov	rcx, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR -88[rbp]
.L736:
	cmp	rcx, rax
	je	.L691
	mov	rax, QWORD PTR -16[rbp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L691
	.p2align 4,,10
	.p2align 3
.L717:
	lea	rsi, -64[rbp]
	mov	edx, 32
	mov	r8d, 2
.L710:
	mov	QWORD PTR -64[rbp], r12
	mov	r9, rbx
	mov	rcx, rax
	mov	QWORD PTR -56[rbp], r13
	mov	DWORD PTR 32[rsp], edx
	mov	rdx, rsi
.LEHB7:
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
	jmp	.L708
	.p2align 4,,10
	.p2align 3
.L740:
	lea	rsi, -64[rbp]
	movsx	edx, r9b
	jmp	.L710
	.p2align 4,,10
	.p2align 3
.L743:
	lea	rdx, -48[rbp]
	mov	r10, rdx
	mov	QWORD PTR -88[rbp], rdx
	mov	rdx, QWORD PTR -80[rbp]
	mov	rcx, r10
	call	_ZNSt6localeaSERKS_
	mov	rcx, QWORD PTR -80[rbp]
	call	_ZNSt6localeD1Ev
	cmp	BYTE PTR -40[rbp], 0
	jne	.L695
.L744:
	mov	rcx, QWORD PTR -88[rbp]
	call	_ZNSt6localeC1Ev
	mov	BYTE PTR -40[rbp], 1
	jmp	.L695
	.p2align 4,,10
	.p2align 3
.L741:
	lea	rsi, -64[rbp]
	cmp	rdi, r12
	mov	rax, r12
	mov	QWORD PTR -56[rbp], r13
	cmovbe	rax, rdi
	mov	rdx, rsi
	mov	QWORD PTR -64[rbp], rax
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.LEHE7:
	add	r13, rdi
	sub	r12, rdi
	mov	edx, 48
	mov	r8d, 2
	jmp	.L710
	.p2align 4,,10
	.p2align 3
.L738:
	movzx	edx, BYTE PTR [r9]
	mov	BYTE PTR -16[rbp], 0
	movzx	eax, WORD PTR 4[rcx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L747
	test	cl, cl
	jne	.L690
	mov	rdx, QWORD PTR [r9]
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L690
	sal	rax, 5
	add	rax, QWORD PTR 8[r9]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR -32[rbp], rdx
	mov	rdx, QWORD PTR 8[rax]
	mov	QWORD PTR -24[rbp], rdx
	movzx	eax, BYTE PTR 16[rax]
	mov	BYTE PTR -16[rbp], al
	.p2align 4,,10
	.p2align 3
.L690:
	lea	rcx, -32[rbp]
.LEHB8:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE8:
	mov	QWORD PTR -72[rbp], rax
	jmp	.L687
	.p2align 4,,10
	.p2align 3
.L745:
	cmp	BYTE PTR [rcx], 67
	jne	.L697
	jmp	.L736
	.p2align 4,,10
	.p2align 3
.L742:
	mov	rcx, rdx
	mov	QWORD PTR -80[rbp], rdx
	call	_ZNSt6localeC1Ev
	mov	rdx, QWORD PTR -80[rbp]
	mov	BYTE PTR 32[rsi], 1
	jmp	.L692
	.p2align 4,,10
	.p2align 3
.L746:
	mov	r8, rdi
	mov	rdx, r14
	mov	rcx, r13
	call	memcpy
	jmp	.L705
	.p2align 4,,10
	.p2align 3
.L747:
	mov	rdx, QWORD PTR [r9]
	lea	rcx, [rax+rax*4]
	sal	rax, 4
	add	rax, QWORD PTR 8[r9]
	shr	rdx, 4
	shr	rdx, cl
	and	edx, 31
	mov	BYTE PTR -16[rbp], dl
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR -32[rbp], rdx
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR -24[rbp], rax
	jmp	.L690
.L702:
.LEHB9:
	call	_ZSt16__throw_bad_castv
.LEHE9:
.L721:
	mov	rcx, QWORD PTR -80[rbp]
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L713:
	cmp	BYTE PTR -40[rbp], 0
	je	.L714
	lea	rcx, -48[rbp]
	call	_ZNSt6localeD1Ev
.L714:
	mov	rcx, rbx
.LEHB10:
	call	_Unwind_Resume
.LEHE10:
.L720:
	mov	rbx, rax
	jmp	.L713
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5016:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5016-.LLSDACSB5016
.LLSDACSB5016:
	.uleb128 .LEHB5-.LFB5016
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L720-.LFB5016
	.uleb128 0
	.uleb128 .LEHB6-.LFB5016
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L721-.LFB5016
	.uleb128 0
	.uleb128 .LEHB7-.LFB5016
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L720-.LFB5016
	.uleb128 0
	.uleb128 .LEHB8-.LFB5016
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB9-.LFB5016
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L720-.LFB5016
	.uleb128 0
	.uleb128 .LEHB10-.LFB5016
	.uleb128 .LEHE10-.LEHB10
	.uleb128 0
	.uleb128 0
.LLSDACSE5016:
	.section	.text$_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC14:
	.ascii "0b\0"
.LC15:
	.ascii "0B\0"
.LC16:
	.ascii "0\0"
.LC17:
	.ascii "0X\0"
.LC18:
	.ascii "0x\0"
	.align 8
.LC19:
	.ascii "format error: integer not representable as character\0"
	.align 8
.LC20:
	.ascii "00010203040506070809101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899\0"
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5005:
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
	sub	rsp, 296
	.seh_stackalloc	296
	.seh_endprologue
	mov	eax, edx
	mov	rsi, r8
	mov	r8d, edx
	movzx	edx, BYTE PTR 1[rcx]
	mov	rbx, rcx
	mov	ecx, edx
	and	ecx, 120
	cmp	cl, 56
	je	.L808
	shr	dl, 3
	and	edx, 15
	cmp	dl, 4
	je	.L752
	ja	.L753
	cmp	dl, 1
	jbe	.L754
	lea	rbp, .LC14[rip]
	cmp	cl, 16
	lea	rdx, .LC15[rip]
	cmovne	rbp, rdx
	test	al, al
	jne	.L809
	lea	r12, 72[rsp]
	mov	eax, 48
	lea	r13, 71[rsp]
.L759:
	mov	BYTE PTR 71[rsp], al
	movzx	eax, BYTE PTR [rbx]
	test	al, 16
	je	.L795
.L794:
	mov	rdx, -2
	mov	ecx, 2
.L763:
	add	rdx, r13
	test	ecx, ecx
	mov	r10d, ecx
	je	.L764
	xor	ecx, ecx
.L781:
	mov	r8d, ecx
	add	ecx, 1
	movzx	r9d, BYTE PTR 0[rbp+r8]
	cmp	ecx, r10d
	mov	BYTE PTR [rdx+r8], r9b
	jb	.L781
	jmp	.L764
	.p2align 4,,10
	.p2align 3
.L808:
	test	al, al
	js	.L750
	mov	BYTE PTR 80[rsp], al
	lea	rcx, 48[rsp]
	mov	r9, rbx
	mov	r8, rsi
	lea	rax, 80[rsp]
	mov	edx, 1
	mov	DWORD PTR 32[rsp], 1
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	add	rsp, 296
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L754:
	test	al, al
	movzx	edi, al
	jne	.L765
	mov	BYTE PTR 71[rsp], 48
	lea	r12, 72[rsp]
	lea	r13, 71[rsp]
.L766:
	movzx	eax, BYTE PTR [rbx]
	mov	rdx, r13
.L764:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L810
.L783:
	cmp	eax, 3
	je	.L796
.L784:
	mov	rax, r12
	mov	r8, r13
	mov	QWORD PTR 56[rsp], rdx
	mov	r9, rsi
	sub	rax, rdx
	sub	r8, rdx
	mov	rcx, rbx
	mov	QWORD PTR 48[rsp], rax
	lea	rax, 48[rsp]
	mov	rdx, rax
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	add	rsp, 296
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L752:
	test	al, al
	je	.L789
	movzx	edx, al
	bsr	ecx, edx
	lea	r12d, 3[rcx]
	mov	ecx, 2863311531
	imul	r12, rcx
	shr	r12, 33
	cmp	edx, 63
	jbe	.L771
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 73[rsp], al
	mov	eax, edx
	shr	edx, 6
	shr	eax, 3
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 72[rsp], al
.L772:
	add	edx, 48
.L773:
	lea	r13, 71[rsp]
	mov	r12d, r12d
	mov	r8d, 1
	lea	rbp, .LC16[rip]
	add	r12, r13
	mov	ecx, 1
.L770:
	mov	BYTE PTR 71[rsp], dl
.L774:
	movzx	eax, BYTE PTR [rbx]
	test	al, 16
	je	.L795
	mov	rdx, rcx
	neg	rdx
	test	r8b, r8b
	jne	.L763
.L795:
	shr	al, 2
	mov	rdx, r13
	and	eax, 3
	cmp	eax, 1
	jne	.L783
.L810:
	mov	eax, 43
.L785:
	mov	BYTE PTR -1[rdx], al
	sub	rdx, 1
	jmp	.L784
	.p2align 4,,10
	.p2align 3
.L765:
	cmp	edi, 9
	jbe	.L788
	lea	rcx, 80[rsp]
	cmp	edi, 99
	mov	r8d, 201
	lea	rdx, .LC20[rip]
	jbe	.L811
	call	memcpy
	mov	r8d, edi
	imul	r8, r8, 1374389535
	shr	r8, 37
	imul	eax, r8d, 100
	sub	edi, eax
	lea	eax, 1[rdi+rdi]
	movzx	eax, WORD PTR 79[rsp+rax]
	mov	WORD PTR 72[rsp], ax
	mov	eax, 3
.L767:
	add	r8d, 48
.L769:
	lea	r13, 71[rsp]
	mov	BYTE PTR 71[rsp], r8b
	lea	r12, 0[r13+rax]
	jmp	.L766
	.p2align 4,,10
	.p2align 3
.L753:
	cmp	cl, 40
	je	.L812
	test	al, al
	jne	.L791
	mov	BYTE PTR 71[rsp], 48
	lea	rbp, .LC17[rip]
	cmp	cl, 48
	lea	r12, 72[rsp]
	lea	r13, 71[rsp]
	je	.L777
.L776:
	movzx	eax, BYTE PTR [rbx]
	test	al, 16
	jne	.L794
	jmp	.L795
	.p2align 4,,10
	.p2align 3
.L777:
	mov	rdi, r13
	.p2align 4,,10
	.p2align 3
.L780:
	movsx	ecx, BYTE PTR [rdi]
	add	rdi, 1
	call	toupper
	mov	BYTE PTR -1[rdi], al
	cmp	rdi, r12
	jne	.L780
	mov	r8d, 1
	mov	ecx, 2
	jmp	.L774
	.p2align 4,,10
	.p2align 3
.L796:
	mov	eax, 32
	jmp	.L785
	.p2align 4,,10
	.p2align 3
.L789:
	mov	edx, 48
	xor	r8d, r8d
	xor	ecx, ecx
	lea	r12, 72[rsp]
	xor	ebp, ebp
	lea	r13, 71[rsp]
	jmp	.L770
	.p2align 4,,10
	.p2align 3
.L809:
	movzx	eax, al
	mov	r12d, 32
	mov	edx, 31
	bsr	r9d, eax
	xor	r9d, 31
	sub	r12d, r9d
	sub	edx, r9d
	je	.L762
	mov	ecx, edx
	lea	r8, 70[rsp+rcx]
	lea	rdx, 71[rsp+rcx]
	mov	ecx, 30
	sub	ecx, r9d
	sub	r8, rcx
	.p2align 4,,10
	.p2align 3
.L761:
	mov	ecx, eax
	sub	rdx, 1
	shr	eax
	and	ecx, 1
	add	ecx, 48
	mov	BYTE PTR 1[rdx], cl
	cmp	rdx, r8
	jne	.L761
.L762:
	lea	r13, 71[rsp]
	movsx	r12, r12d
	mov	eax, 49
	add	r12, r13
	jmp	.L759
	.p2align 4,,10
	.p2align 3
.L812:
	test	al, al
	jne	.L790
	mov	BYTE PTR 71[rsp], 48
	lea	rbp, .LC18[rip]
	lea	r12, 72[rsp]
	lea	r13, 71[rsp]
	jmp	.L776
	.p2align 4,,10
	.p2align 3
.L791:
	lea	rbp, .LC17[rip]
.L775:
	movabs	rdi, 3978425819141910832
	movzx	edx, al
	bsr	r8d, edx
	mov	QWORD PTR 80[rsp], rdi
	movabs	rdi, 7378413942531504440
	add	r8d, 4
	mov	QWORD PTR 88[rsp], rdi
	shr	r8d, 2
	cmp	edx, 15
	ja	.L813
	movzx	eax, BYTE PTR 80[rsp+rdx]
.L779:
	mov	BYTE PTR 71[rsp], al
	lea	r13, 71[rsp]
	mov	eax, r8d
	cmp	cl, 48
	lea	r12, 0[r13+rax]
	jne	.L776
	test	r8d, r8d
	jne	.L777
	mov	r8d, 1
	mov	ecx, 2
	mov	r12, r13
	jmp	.L774
	.p2align 4,,10
	.p2align 3
.L813:
	and	eax, 15
	shr	edx, 4
	movzx	eax, BYTE PTR 80[rsp+rax]
	mov	BYTE PTR 72[rsp], al
	movzx	eax, BYTE PTR 80[rsp+rdx]
	jmp	.L779
	.p2align 4,,10
	.p2align 3
.L790:
	lea	rbp, .LC18[rip]
	jmp	.L775
	.p2align 4,,10
	.p2align 3
.L811:
	call	memcpy
	add	edi, edi
	lea	eax, 1[rdi]
	movzx	r8d, BYTE PTR 80[rsp+rdi]
	movzx	eax, BYTE PTR 80[rsp+rax]
	mov	BYTE PTR 72[rsp], al
	mov	eax, 2
	jmp	.L769
	.p2align 4,,10
	.p2align 3
.L788:
	mov	eax, 1
	jmp	.L767
.L771:
	cmp	edx, 7
	jbe	.L772
	and	eax, 7
	shr	edx, 3
	add	eax, 48
	add	edx, 48
	mov	BYTE PTR 72[rsp], al
	jmp	.L773
.L750:
	lea	rcx, .LC19[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC21:
	.ascii "true\0"
.LC22:
	.ascii "false\0"
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_:
.LFB4896:
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
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	and	eax, 120
	mov	rbx, rcx
	mov	esi, edx
	cmp	al, 56
	mov	rdi, r8
	je	.L863
	test	al, al
	jne	.L864
	test	BYTE PTR [rcx], 32
	lea	rbp, 80[rsp]
	mov	BYTE PTR 80[rsp], 0
	mov	QWORD PTR 64[rsp], rbp
	mov	QWORD PTR 72[rsp], 0
	jne	.L865
	lea	rsi, 64[rsp]
	mov	eax, edx
	neg	al
	lea	rax, .LC21[rip]
	sbb	r12, r12
	add	r12, 5
	test	dl, dl
	lea	rdx, .LC22[rip]
	cmove	rax, rdx
	cmp	rax, rbp
	je	.L835
	xor	edx, edx
	test	r12b, 4
	mov	ecx, r12d
	jne	.L866
	test	cl, 2
	jne	.L867
.L837:
	and	ecx, 1
	jne	.L868
.L838:
	mov	rax, rbp
.L839:
	mov	QWORD PTR 72[rsp], r12
	mov	BYTE PTR [rax+r12], 0
.L862:
	mov	rdx, QWORD PTR 72[rsp]
	lea	rcx, 48[rsp]
	mov	r9, rbx
	mov	r8, rdi
	mov	rax, QWORD PTR 64[rsp]
	mov	DWORD PTR 32[rsp], 1
	lea	rsi, 64[rsp]
	mov	QWORD PTR 48[rsp], rdx
	mov	QWORD PTR 56[rsp], rax
.LEHB11:
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.LEHE11:
	mov	rcx, QWORD PTR 64[rsp]
	mov	rbx, rax
	cmp	rcx, rbp
	je	.L850
	mov	rax, QWORD PTR 80[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L850:
	mov	rax, rbx
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
.L864:
	movzx	edx, dl
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
.LEHB12:
	jmp	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.p2align 4,,10
	.p2align 3
.L863:
	mov	BYTE PTR 96[rsp], dl
	lea	rax, 96[rsp]
	mov	r9, rbx
	mov	edx, 1
	lea	rcx, 48[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.LEHE12:
	mov	rbx, rax
	jmp	.L850
	.p2align 4,,10
	.p2align 3
.L868:
	movzx	eax, BYTE PTR [rax+rdx]
	mov	BYTE PTR 80[rsp+rdx], al
	jmp	.L838
	.p2align 4,,10
	.p2align 3
.L867:
	movzx	r8d, WORD PTR [rax+rdx]
	mov	WORD PTR 80[rsp+rdx], r8w
	add	rdx, 2
	and	ecx, 1
	je	.L838
	jmp	.L868
	.p2align 4,,10
	.p2align 3
.L866:
	mov	edx, DWORD PTR [rax]
	test	cl, 2
	mov	DWORD PTR 80[rsp], edx
	mov	edx, 4
	je	.L837
	jmp	.L867
	.p2align 4,,10
	.p2align 3
.L865:
	cmp	BYTE PTR 32[r8], 0
	lea	r13, 24[r8]
	je	.L869
.L819:
	lea	r12, 96[rsp]
	mov	rdx, r13
	mov	rcx, r12
	call	_ZNSt6localeC1ERKS_
	mov	rcx, QWORD PTR .refptr._ZNSt7__cxx118numpunctIcE2idE[rip]
	call	_ZNKSt6locale2id5_M_idEv
	mov	rdx, rax
	mov	rax, QWORD PTR 96[rsp]
	mov	rax, QWORD PTR 8[rax]
	mov	r13, QWORD PTR [rax+rdx*8]
	test	r13, r13
	je	.L820
	mov	rcx, r12
	call	_ZNSt6localeD1Ev
	test	sil, sil
	jne	.L821
	mov	rax, QWORD PTR 0[r13]
	lea	rsi, 64[rsp]
	mov	rdx, r13
	mov	rcx, r12
.LEHB13:
	call	[QWORD PTR 48[rax]]
.L823:
	mov	rax, QWORD PTR 96[rsp]
	lea	rsi, 112[rsp]
	mov	rcx, QWORD PTR 64[rsp]
	mov	r8, QWORD PTR 104[rsp]
	cmp	rax, rsi
	je	.L870
	movq	xmm0, r8
	cmp	rcx, rbp
	movhps	xmm0, QWORD PTR 112[rsp]
	je	.L871
	test	rcx, rcx
	mov	rdx, QWORD PTR 80[rsp]
	mov	QWORD PTR 64[rsp], rax
	movups	XMMWORD PTR 72[rsp], xmm0
	je	.L831
	mov	QWORD PTR 96[rsp], rcx
	mov	QWORD PTR 112[rsp], rdx
.L830:
	mov	QWORD PTR 104[rsp], 0
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 96[rsp]
	cmp	rcx, rsi
	je	.L862
	mov	rax, QWORD PTR 112[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L862
	.p2align 4,,10
	.p2align 3
.L821:
	mov	rax, QWORD PTR 0[r13]
	lea	rsi, 64[rsp]
	mov	rdx, r13
	mov	rcx, r12
	call	[QWORD PTR 40[rax]]
.LEHE13:
	jmp	.L823
	.p2align 4,,10
	.p2align 3
.L869:
	mov	rcx, r13
	call	_ZNSt6localeC1Ev
	mov	BYTE PTR 32[rdi], 1
	jmp	.L819
.L871:
	mov	QWORD PTR 64[rsp], rax
	movups	XMMWORD PTR 72[rsp], xmm0
.L831:
	mov	QWORD PTR 96[rsp], rsi
	lea	rsi, 112[rsp]
	mov	rcx, rsi
	jmp	.L830
.L870:
	test	r8, r8
	je	.L826
	cmp	r8, 1
	je	.L872
	mov	rdx, rsi
	call	memcpy
	mov	r8, QWORD PTR 104[rsp]
	mov	rcx, QWORD PTR 64[rsp]
.L826:
	mov	QWORD PTR 72[rsp], r8
	mov	BYTE PTR [rcx+r8], 0
	mov	rcx, QWORD PTR 96[rsp]
	jmp	.L830
.L872:
	movzx	eax, BYTE PTR 112[rsp]
	mov	BYTE PTR [rcx], al
	mov	r8, QWORD PTR 104[rsp]
	mov	rcx, QWORD PTR 64[rsp]
	jmp	.L826
.L820:
.LEHB14:
	call	_ZSt16__throw_bad_castv
.LEHE14:
.L845:
	mov	rbx, rax
.L842:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB15:
	call	_Unwind_Resume
.LEHE15:
.L835:
	xor	eax, eax
	mov	QWORD PTR 32[rsp], r12
	mov	r9, rbp
	xor	r8d, r8d
	mov	QWORD PTR 40[rsp], rax
	mov	rdx, rbp
	mov	rcx, rsi
.LEHB16:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
.LEHE16:
	mov	rax, QWORD PTR 64[rsp]
	jmp	.L839
.L844:
	lea	rsi, 64[rsp]
	mov	rcx, r12
	mov	rbx, rax
	call	_ZNSt6localeD1Ev
	jmp	.L842
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4896:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4896-.LLSDACSB4896
.LLSDACSB4896:
	.uleb128 .LEHB11-.LFB4896
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L845-.LFB4896
	.uleb128 0
	.uleb128 .LEHB12-.LFB4896
	.uleb128 .LEHE12-.LEHB12
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB13-.LFB4896
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L845-.LFB4896
	.uleb128 0
	.uleb128 .LEHB14-.LFB4896
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L844-.LFB4896
	.uleb128 0
	.uleb128 .LEHB15-.LFB4896
	.uleb128 .LEHE15-.LEHB15
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB16-.LFB4896
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L845-.LFB4896
	.uleb128 0
.LLSDACSE4896:
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIcNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIcNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIcNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIcNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIcNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB4902:
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
	sub	rsp, 288
	.seh_stackalloc	288
	.seh_endprologue
	mov	ebx, edx
	movzx	edx, BYTE PTR 1[rcx]
	mov	rsi, rcx
	mov	rdi, r8
	mov	ecx, edx
	and	ecx, 120
	cmp	cl, 56
	je	.L945
	shr	dl, 3
	mov	eax, ebx
	and	edx, 15
	test	bl, bl
	js	.L946
	cmp	dl, 4
	je	.L882
	ja	.L883
	cmp	dl, 1
	jbe	.L884
	lea	rbp, .LC14[rip]
	cmp	cl, 16
	lea	rdx, .LC15[rip]
	cmovne	rbp, rdx
	test	bl, bl
	jne	.L880
	lea	r12, 73[rsp]
	mov	eax, 48
	lea	r13, 72[rsp]
.L889:
	mov	BYTE PTR 72[rsp], al
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	je	.L930
.L929:
	mov	rdx, -2
	mov	ecx, 2
.L893:
	add	rdx, r13
	test	ecx, ecx
	mov	r10d, ecx
	je	.L894
	xor	ecx, ecx
.L911:
	mov	r8d, ecx
	add	ecx, 1
	movzx	r9d, BYTE PTR 0[rbp+r8]
	cmp	ecx, r10d
	mov	BYTE PTR [rdx+r8], r9b
	jb	.L911
	.p2align 4,,10
	.p2align 3
.L894:
	lea	rcx, -1[rdx]
	shr	al, 2
	and	eax, 3
	test	bl, bl
	jns	.L896
	mov	BYTE PTR -1[rdx], 45
	mov	rdx, rcx
	jmp	.L913
	.p2align 4,,10
	.p2align 3
.L946:
	neg	eax
	cmp	dl, 4
	je	.L877
	ja	.L878
	cmp	dl, 1
	jbe	.L879
	lea	rbp, .LC14[rip]
	cmp	cl, 16
	lea	rdx, .LC15[rip]
	cmovne	rbp, rdx
.L880:
	movzx	eax, al
	mov	r12d, 32
	bsr	r9d, eax
	mov	edx, 31
	xor	r9d, 31
	sub	r12d, r9d
	sub	edx, r9d
	je	.L892
	mov	ecx, edx
	lea	r8, 71[rsp+rcx]
	lea	rdx, 72[rsp+rcx]
	mov	ecx, 30
	sub	ecx, r9d
	sub	r8, rcx
	.p2align 4,,10
	.p2align 3
.L891:
	mov	ecx, eax
	sub	rdx, 1
	shr	eax
	and	ecx, 1
	add	ecx, 48
	mov	BYTE PTR 1[rdx], cl
	cmp	rdx, r8
	jne	.L891
.L892:
	lea	r13, 72[rsp]
	movsx	r12, r12d
	mov	eax, 49
	add	r12, r13
	jmp	.L889
	.p2align 4,,10
	.p2align 3
.L945:
	lea	rax, 80[rsp]
	mov	r9, rsi
	mov	edx, 1
	mov	BYTE PTR 80[rsp], bl
	lea	rcx, 48[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L943:
	add	rsp, 288
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
.L884:
	test	bl, bl
	jne	.L895
	movzx	eax, BYTE PTR [rsi]
	lea	r13, 72[rsp]
	mov	BYTE PTR 72[rsp], 48
	lea	r12, 73[rsp]
	mov	rdx, r13
	lea	rcx, 71[rsp]
	shr	al, 2
	and	eax, 3
.L896:
	movzx	eax, al
	cmp	eax, 1
	je	.L947
	cmp	eax, 3
	je	.L948
.L913:
	mov	rax, r12
	mov	r8, r13
	mov	QWORD PTR 56[rsp], rdx
	mov	r9, rdi
	sub	rax, rdx
	sub	r8, rdx
	mov	rcx, rsi
	mov	QWORD PTR 48[rsp], rax
	lea	rax, 48[rsp]
	mov	rdx, rax
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L943
	.p2align 4,,10
	.p2align 3
.L878:
	lea	rbp, .LC18[rip]
	cmp	cl, 40
	lea	rdx, .LC17[rip]
	cmovne	rbp, rdx
.L881:
	movabs	r11, 3978425819141910832
	movzx	edx, al
	bsr	r8d, edx
	mov	QWORD PTR 80[rsp], r11
	movabs	r11, 7378413942531504440
	add	r8d, 4
	mov	QWORD PTR 88[rsp], r11
	shr	r8d, 2
	cmp	al, 15
	ja	.L949
	movzx	eax, BYTE PTR 80[rsp+rdx]
.L909:
	lea	r13, 72[rsp]
	mov	r12d, r8d
	mov	BYTE PTR 72[rsp], al
	add	r12, r13
	cmp	cl, 48
	je	.L950
.L906:
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	jne	.L929
.L930:
	mov	rdx, r13
	jmp	.L894
	.p2align 4,,10
	.p2align 3
.L947:
	mov	BYTE PTR -1[rdx], 43
.L916:
	mov	rdx, rcx
	jmp	.L913
	.p2align 4,,10
	.p2align 3
.L882:
	test	bl, bl
	jne	.L877
	xor	r8d, r8d
	xor	ecx, ecx
	xor	ebp, ebp
	lea	r12, 73[rsp]
	mov	edx, 48
	lea	r13, 72[rsp]
.L901:
	mov	BYTE PTR 72[rsp], dl
.L905:
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	je	.L930
	mov	rdx, rcx
	neg	rdx
	test	r8b, r8b
	jne	.L893
	mov	rdx, r13
	jmp	.L894
	.p2align 4,,10
	.p2align 3
.L883:
	cmp	cl, 40
	je	.L951
	test	bl, bl
	jne	.L926
	cmp	cl, 48
	mov	BYTE PTR 72[rsp], 48
	je	.L927
	lea	rbp, .LC17[rip]
	lea	r12, 73[rsp]
	lea	r13, 72[rsp]
	jmp	.L906
	.p2align 4,,10
	.p2align 3
.L948:
	mov	BYTE PTR -1[rdx], 32
	jmp	.L916
	.p2align 4,,10
	.p2align 3
.L877:
	movzx	edx, al
	bsr	ecx, edx
	lea	r12d, 3[rcx]
	mov	ecx, 2863311531
	imul	r12, rcx
	shr	r12, 33
	cmp	al, 63
	jbe	.L902
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 74[rsp], al
	mov	eax, edx
	shr	edx, 6
	shr	eax, 3
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 73[rsp], al
.L903:
	add	edx, 48
.L904:
	lea	r13, 72[rsp]
	mov	r12d, r12d
	mov	r8d, 1
	lea	rbp, .LC16[rip]
	add	r12, r13
	mov	ecx, 1
	jmp	.L901
	.p2align 4,,10
	.p2align 3
.L879:
	movzx	r14d, al
.L917:
	cmp	al, 9
	jbe	.L922
	cmp	al, 100
	sbb	ebp, ebp
	add	ebp, 2
	cmp	al, 100
	sbb	r12, r12
	add	r12, 3
	cmp	al, 100
	sbb	r13d, r13d
	add	r13d, 3
.L897:
	lea	rcx, 80[rsp]
	mov	r8d, 201
	lea	rdx, .LC20[rip]
	call	memcpy
	cmp	r14d, 99
	jbe	.L952
	mov	eax, r14d
	mov	edx, ebp
	imul	rax, rax, 1374389535
	shr	rax, 37
	imul	eax, eax, 100
	sub	r14d, eax
	add	r14d, r14d
	lea	eax, 1[r14]
	movzx	eax, BYTE PTR 80[rsp+rax]
	mov	BYTE PTR 72[rsp+rdx], al
	movzx	edx, BYTE PTR 80[rsp+r14]
	lea	eax, -2[r13]
	mov	r14d, 1
	mov	BYTE PTR 72[rsp+rax], dl
.L899:
	add	r14d, 48
.L900:
	lea	r13, 72[rsp]
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR 72[rsp], r14b
	add	r12, r13
	mov	rdx, r13
	jmp	.L894
	.p2align 4,,10
	.p2align 3
.L949:
	and	eax, 15
	shr	edx, 4
	movzx	eax, BYTE PTR 80[rsp+rax]
	mov	BYTE PTR 73[rsp], al
	movzx	eax, BYTE PTR 80[rsp+rdx]
	jmp	.L909
	.p2align 4,,10
	.p2align 3
.L927:
	lea	r12, 73[rsp]
	lea	rbp, .LC17[rip]
	lea	r13, 72[rsp]
.L907:
	mov	r14, r13
	.p2align 4,,10
	.p2align 3
.L910:
	movsx	ecx, BYTE PTR [r14]
	add	r14, 1
	call	toupper
	mov	BYTE PTR -1[r14], al
	cmp	r14, r12
	jne	.L910
	mov	r8d, 1
	mov	ecx, 2
	jmp	.L905
	.p2align 4,,10
	.p2align 3
.L950:
	test	r8d, r8d
	jne	.L907
	mov	r8d, 1
	mov	ecx, 2
	mov	r12, r13
	jmp	.L905
	.p2align 4,,10
	.p2align 3
.L951:
	test	bl, bl
	jne	.L925
	mov	BYTE PTR 72[rsp], 48
	lea	rbp, .LC18[rip]
	lea	r12, 73[rsp]
	lea	r13, 72[rsp]
	jmp	.L906
	.p2align 4,,10
	.p2align 3
.L922:
	xor	ebp, ebp
	mov	r12d, 1
	mov	r13d, 1
	jmp	.L897
	.p2align 4,,10
	.p2align 3
.L895:
	movsx	r14d, bl
	jmp	.L917
	.p2align 4,,10
	.p2align 3
.L926:
	lea	rbp, .LC17[rip]
	jmp	.L881
	.p2align 4,,10
	.p2align 3
.L952:
	cmp	r14d, 9
	jbe	.L899
	add	r14d, r14d
	lea	eax, 1[r14]
	movzx	r14d, BYTE PTR 80[rsp+r14]
	movzx	eax, BYTE PTR 80[rsp+rax]
	mov	BYTE PTR 73[rsp], al
	jmp	.L900
.L925:
	lea	rbp, .LC18[rip]
	jmp	.L881
.L902:
	cmp	al, 7
	jbe	.L903
	and	eax, 7
	shr	edx, 3
	add	eax, 48
	add	edx, 48
	mov	BYTE PTR 73[rsp], al
	jmp	.L904
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB4904:
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
	sub	rsp, 328
	.seh_stackalloc	328
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	esi, edx
	mov	edx, eax
	mov	rdi, rcx
	and	edx, 120
	mov	rbp, r8
	mov	ebx, esi
	cmp	dl, 56
	je	.L1041
	shr	al, 3
	and	eax, 15
	test	esi, esi
	js	.L1042
	cmp	al, 4
	je	.L963
	ja	.L964
	cmp	al, 1
	jbe	.L965
	lea	r14, .LC14[rip]
	cmp	dl, 16
	lea	rax, .LC15[rip]
	cmovne	r14, rax
	test	esi, esi
	jne	.L961
	lea	r12, 68[rsp]
	mov	eax, 48
	lea	r13, 67[rsp]
.L970:
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], al
	test	bl, 16
	je	.L1023
.L1022:
	mov	rdx, -2
	mov	eax, 2
.L974:
	add	rdx, r13
	test	eax, eax
	mov	r9d, eax
	je	.L975
	xor	eax, eax
.L1001:
	mov	ecx, eax
	add	eax, 1
	movzx	r8d, BYTE PTR [r14+rcx]
	cmp	eax, r9d
	mov	BYTE PTR [rdx+rcx], r8b
	jb	.L1001
.L975:
	lea	rcx, -1[rdx]
	mov	eax, ebx
	shr	al, 2
	and	eax, 3
	test	esi, esi
	jns	.L976
.L1044:
	mov	BYTE PTR -1[rdx], 45
	mov	rdx, rcx
.L1003:
	lea	rax, 48[rsp]
	mov	r8, r13
	sub	r12, rdx
	mov	QWORD PTR 56[rsp], rdx
	sub	r8, rdx
	mov	r9, rbp
	mov	rdx, rax
	mov	QWORD PTR 48[rsp], r12
	mov	rcx, rdi
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L956
	.p2align 4,,10
	.p2align 3
.L1042:
	mov	ebx, esi
	neg	ebx
	cmp	al, 4
	je	.L958
	ja	.L959
	cmp	al, 1
	jbe	.L960
	lea	r14, .LC14[rip]
	cmp	dl, 16
	lea	rax, .LC15[rip]
	cmovne	r14, rax
.L961:
	bsr	r8d, ebx
	mov	r12d, 32
	xor	r8d, 31
	mov	eax, 31
	sub	r12d, r8d
	sub	eax, r8d
	je	.L973
	mov	edx, eax
	lea	rcx, 63[rsp+rdx]
	lea	rax, 64[rsp+rdx]
	mov	edx, 30
	sub	edx, r8d
	sub	rcx, rdx
	.p2align 4,,10
	.p2align 3
.L972:
	mov	edx, ebx
	sub	rax, 1
	shr	ebx
	and	edx, 1
	add	edx, 48
	mov	BYTE PTR 4[rax], dl
	cmp	rax, rcx
	jne	.L972
.L973:
	lea	r13, 67[rsp]
	movsx	r12, r12d
	mov	eax, 49
	add	r12, r13
	jmp	.L970
	.p2align 4,,10
	.p2align 3
.L1041:
	lea	eax, 128[rsi]
	cmp	eax, 255
	ja	.L955
	lea	rax, 112[rsp]
	mov	r9, rdi
	mov	edx, 1
	mov	BYTE PTR 112[rsp], sil
	lea	rcx, 48[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L956:
	add	rsp, 328
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
.L964:
	cmp	dl, 40
	je	.L1043
	test	esi, esi
	jne	.L1019
	movzx	ebx, BYTE PTR [rcx]
	mov	BYTE PTR 67[rsp], 48
	lea	r12, 68[rsp]
	cmp	dl, 48
	lea	r14, .LC17[rip]
	lea	r13, 67[rsp]
	je	.L994
.L995:
	test	bl, 16
	jne	.L1022
	.p2align 4,,10
	.p2align 3
.L1023:
	mov	rdx, r13
.L1047:
	lea	rcx, -1[rdx]
	mov	eax, ebx
	shr	al, 2
	and	eax, 3
	test	esi, esi
	js	.L1044
.L976:
	movzx	eax, al
	cmp	eax, 1
	je	.L1045
	cmp	eax, 3
	jne	.L1003
	mov	BYTE PTR -1[rdx], 32
.L1006:
	mov	rdx, rcx
	jmp	.L1003
	.p2align 4,,10
	.p2align 3
.L959:
	lea	r14, .LC18[rip]
	cmp	dl, 40
	lea	rax, .LC17[rip]
	cmovne	r14, rax
.L962:
	bsr	eax, ebx
	lea	r9d, 4[rax]
	movabs	rax, 3978425819141910832
	shr	r9d, 2
	mov	QWORD PTR 112[rsp], rax
	cmp	ebx, 255
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 120[rsp], rax
	lea	eax, -1[r9]
	jbe	.L996
	.p2align 4,,10
	.p2align 3
.L997:
	mov	r8d, ebx
	mov	ecx, eax
	and	r8d, 15
	movzx	r8d, BYTE PTR 112[rsp+r8]
	mov	BYTE PTR 67[rsp+rcx], r8b
	lea	r8d, -1[rax]
	mov	ecx, ebx
	shr	ebx, 8
	shr	ecx, 4
	sub	eax, 2
	and	ecx, 15
	cmp	ebx, 255
	movzx	ecx, BYTE PTR 112[rsp+rcx]
	mov	BYTE PTR 67[rsp+r8], cl
	ja	.L997
.L996:
	cmp	ebx, 15
	ja	.L1046
	movzx	eax, BYTE PTR 112[rsp+rbx]
.L999:
	lea	r13, 67[rsp]
	mov	r12d, r9d
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], al
	add	r12, r13
	cmp	dl, 48
	jne	.L995
	test	r9d, r9d
	jne	.L994
	mov	ecx, 1
	mov	eax, 2
	mov	r12, r13
	jmp	.L993
	.p2align 4,,10
	.p2align 3
.L994:
	mov	r15, r13
	.p2align 4,,10
	.p2align 3
.L1000:
	movsx	ecx, BYTE PTR [r15]
	add	r15, 1
	call	toupper
	mov	BYTE PTR -1[r15], al
	cmp	r15, r12
	jne	.L1000
	mov	ecx, 1
	mov	eax, 2
	jmp	.L993
	.p2align 4,,10
	.p2align 3
.L1045:
	mov	BYTE PTR -1[rdx], 43
	jmp	.L1006
	.p2align 4,,10
	.p2align 3
.L965:
	test	esi, esi
	jne	.L960
	movzx	eax, BYTE PTR [rcx]
	lea	r13, 67[rsp]
	mov	BYTE PTR 67[rsp], 48
	lea	r12, 68[rsp]
	mov	rdx, r13
	lea	rcx, 66[rsp]
	shr	al, 2
	and	eax, 3
	jmp	.L976
	.p2align 4,,10
	.p2align 3
.L963:
	test	esi, esi
	jne	.L958
	xor	ecx, ecx
	xor	eax, eax
	xor	r14d, r14d
	lea	r12, 68[rsp]
	mov	edx, 48
	lea	r13, 67[rsp]
.L988:
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], dl
.L993:
	test	bl, 16
	je	.L1023
	mov	rdx, rax
	neg	rdx
	test	cl, cl
	jne	.L974
	mov	rdx, r13
	jmp	.L1047
	.p2align 4,,10
	.p2align 3
.L960:
	cmp	ebx, 9
	jbe	.L1011
	cmp	ebx, 99
	jbe	.L1048
	cmp	ebx, 999
	jbe	.L1012
	cmp	ebx, 9999
	jbe	.L1049
	cmp	ebx, 99999
	mov	r12d, 5
	jbe	.L983
	cmp	ebx, 999999
	jbe	.L1050
	cmp	ebx, 9999999
	jbe	.L1014
	cmp	ebx, 99999999
	jbe	.L1015
	cmp	ebx, 999999999
	jbe	.L1016
	mov	r12d, 5
.L984:
	add	r12d, 5
.L983:
	lea	r13d, -1[r12]
.L980:
	lea	rcx, 112[rsp]
	mov	r8d, 201
	lea	rdx, .LC20[rip]
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L986:
	mov	edx, ebx
	mov	eax, ebx
	imul	rdx, rdx, 1374389535
	shr	rdx, 37
	imul	ecx, edx, 100
	sub	eax, ecx
	mov	ecx, ebx
	mov	ebx, edx
	add	eax, eax
	mov	edx, r13d
	lea	r8d, 1[rax]
	movzx	eax, BYTE PTR 112[rsp+rax]
	movzx	r8d, BYTE PTR 112[rsp+r8]
	mov	BYTE PTR 67[rsp+rdx], r8b
	lea	edx, -1[r13]
	sub	r13d, 2
	cmp	ecx, 9999
	mov	BYTE PTR 67[rsp+rdx], al
	ja	.L986
	cmp	ecx, 999
	ja	.L979
.L977:
	add	ebx, 48
.L987:
	lea	r13, 67[rsp]
	mov	BYTE PTR 67[rsp], bl
	movzx	ebx, BYTE PTR [rdi]
	add	r12, r13
	mov	rdx, r13
	jmp	.L975
	.p2align 4,,10
	.p2align 3
.L958:
	bsr	eax, ebx
	lea	r12d, 3[rax]
	mov	eax, 2863311531
	imul	r12, rax
	shr	r12, 33
	cmp	ebx, 63
	lea	edx, -1[r12]
	jbe	.L989
	.p2align 4,,10
	.p2align 3
.L990:
	mov	eax, ebx
	mov	ecx, edx
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 67[rsp+rcx], al
	lea	ecx, -1[rdx]
	mov	eax, ebx
	shr	ebx, 6
	shr	eax, 3
	sub	edx, 2
	and	eax, 7
	add	eax, 48
	cmp	ebx, 63
	mov	BYTE PTR 67[rsp+rcx], al
	ja	.L990
.L989:
	lea	edx, 48[rbx]
	cmp	ebx, 7
	jbe	.L992
	mov	eax, ebx
	shr	ebx, 3
	and	eax, 7
	mov	edx, ebx
	add	eax, 48
	add	edx, 48
	mov	BYTE PTR 68[rsp], al
.L992:
	lea	r13, 67[rsp]
	mov	r12d, r12d
	mov	ecx, 1
	lea	r14, .LC16[rip]
	add	r12, r13
	mov	eax, 1
	jmp	.L988
	.p2align 4,,10
	.p2align 3
.L1046:
	mov	eax, ebx
	shr	ebx, 4
	and	eax, 15
	movzx	eax, BYTE PTR 112[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	movzx	eax, BYTE PTR 112[rsp+rbx]
	jmp	.L999
.L1048:
	lea	rcx, 112[rsp]
	mov	r8d, 201
	mov	r12d, 2
	lea	rdx, .LC20[rip]
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L979:
	add	ebx, ebx
	lea	eax, 1[rbx]
	movzx	ebx, BYTE PTR 112[rsp+rbx]
	movzx	eax, BYTE PTR 112[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	jmp	.L987
	.p2align 4,,10
	.p2align 3
.L1043:
	test	esi, esi
	jne	.L1018
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], 48
	mov	ecx, 1
	mov	eax, 2
	lea	r14, .LC18[rip]
	lea	r12, 68[rsp]
	lea	r13, 67[rsp]
	jmp	.L993
	.p2align 4,,10
	.p2align 3
.L1014:
	mov	r12d, 7
	jmp	.L983
	.p2align 4,,10
	.p2align 3
.L1015:
	mov	r12d, 8
	jmp	.L983
	.p2align 4,,10
	.p2align 3
.L1016:
	mov	r12d, 9
	jmp	.L983
	.p2align 4,,10
	.p2align 3
.L1019:
	lea	r14, .LC17[rip]
	jmp	.L962
.L1018:
	lea	r14, .LC18[rip]
	jmp	.L962
.L1011:
	mov	r12d, 1
	jmp	.L977
.L1049:
	mov	r12d, 4
	mov	r13d, 3
	jmp	.L980
.L1012:
	mov	r12d, 3
	mov	r13d, 2
	jmp	.L980
.L1050:
	mov	r12d, 1
	jmp	.L984
.L955:
	lea	rcx, .LC19[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIjNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIjNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIjNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIjNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIjNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB4906:
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
	sub	rsp, 328
	.seh_stackalloc	328
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	ebx, edx
	mov	edx, eax
	mov	rsi, rcx
	and	edx, 120
	mov	rdi, r8
	cmp	dl, 56
	je	.L1131
	shr	al, 3
	and	eax, 15
	cmp	al, 4
	je	.L1055
	ja	.L1056
	cmp	al, 1
	jbe	.L1057
	lea	rbp, .LC14[rip]
	cmp	dl, 16
	lea	rax, .LC15[rip]
	cmovne	rbp, rax
	test	ebx, ebx
	jne	.L1132
	lea	rbx, 68[rsp]
	mov	eax, 48
	lea	r12, 67[rsp]
.L1062:
	mov	BYTE PTR 67[rsp], al
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	je	.L1114
.L1113:
	mov	rdx, -2
	mov	ecx, 2
.L1066:
	add	rdx, r12
	test	ecx, ecx
	mov	r10d, ecx
	je	.L1067
	xor	ecx, ecx
.L1095:
	mov	r8d, ecx
	add	ecx, 1
	movzx	r9d, BYTE PTR 0[rbp+r8]
	cmp	ecx, r10d
	mov	BYTE PTR [rdx+r8], r9b
	jb	.L1095
	jmp	.L1067
	.p2align 4,,10
	.p2align 3
.L1131:
	cmp	ebx, 127
	ja	.L1053
	lea	rax, 112[rsp]
	mov	r9, rsi
	mov	edx, 1
	mov	BYTE PTR 112[rsp], bl
	lea	rcx, 48[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	add	rsp, 328
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L1057:
	test	ebx, ebx
	jne	.L1068
	mov	BYTE PTR 67[rsp], 48
	lea	rbx, 68[rsp]
	lea	r12, 67[rsp]
.L1069:
	movzx	eax, BYTE PTR [rsi]
	mov	rdx, r12
.L1067:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L1133
.L1097:
	cmp	eax, 3
	je	.L1115
.L1098:
	lea	rax, 48[rsp]
	mov	r8, r12
	sub	rbx, rdx
	mov	QWORD PTR 56[rsp], rdx
	sub	r8, rdx
	mov	r9, rdi
	mov	rdx, rax
	mov	QWORD PTR 48[rsp], rbx
	mov	rcx, rsi
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	add	rsp, 328
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L1055:
	test	ebx, ebx
	je	.L1108
	bsr	eax, ebx
	lea	r8d, 3[rax]
	mov	eax, 2863311531
	imul	r8, rax
	shr	r8, 33
	cmp	ebx, 63
	lea	edx, -1[r8]
	jbe	.L1082
	.p2align 4,,10
	.p2align 3
.L1083:
	mov	eax, ebx
	mov	ecx, edx
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 67[rsp+rcx], al
	lea	ecx, -1[rdx]
	mov	eax, ebx
	shr	ebx, 6
	shr	eax, 3
	sub	edx, 2
	and	eax, 7
	add	eax, 48
	cmp	ebx, 63
	mov	BYTE PTR 67[rsp+rcx], al
	ja	.L1083
.L1082:
	lea	eax, 48[rbx]
	cmp	ebx, 7
	ja	.L1134
.L1085:
	lea	r12, 67[rsp]
	mov	ebx, r8d
	mov	edx, 1
	lea	rbp, .LC16[rip]
	add	rbx, r12
	mov	ecx, 1
.L1081:
	mov	BYTE PTR 67[rsp], al
.L1086:
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	je	.L1114
	test	dl, dl
	jne	.L1135
.L1114:
	shr	al, 2
	mov	rdx, r12
	and	eax, 3
	cmp	eax, 1
	jne	.L1097
.L1133:
	mov	eax, 43
.L1099:
	mov	BYTE PTR -1[rdx], al
	sub	rdx, 1
	jmp	.L1098
	.p2align 4,,10
	.p2align 3
.L1056:
	cmp	dl, 40
	je	.L1136
	test	ebx, ebx
	jne	.L1110
	cmp	dl, 48
	mov	BYTE PTR 67[rsp], 48
	je	.L1111
	lea	rbp, .LC17[rip]
	lea	rbx, 68[rsp]
	lea	r12, 67[rsp]
	jmp	.L1088
	.p2align 4,,10
	.p2align 3
.L1115:
	mov	eax, 32
	jmp	.L1099
	.p2align 4,,10
	.p2align 3
.L1068:
	cmp	ebx, 9
	jbe	.L1102
	cmp	ebx, 99
	jbe	.L1137
	cmp	ebx, 999
	jbe	.L1103
	cmp	ebx, 9999
	jbe	.L1138
	cmp	ebx, 99999
	mov	ebp, 5
	jbe	.L1076
	cmp	ebx, 999999
	jbe	.L1139
	cmp	ebx, 9999999
	jbe	.L1105
	cmp	ebx, 99999999
	jbe	.L1106
	cmp	ebx, 999999999
	jbe	.L1107
	mov	ebp, 5
.L1077:
	add	ebp, 5
.L1076:
	lea	r12d, -1[rbp]
.L1073:
	lea	rcx, 112[rsp]
	mov	r8d, 201
	lea	rdx, .LC20[rip]
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L1079:
	mov	edx, ebx
	mov	eax, ebx
	imul	rdx, rdx, 1374389535
	shr	rdx, 37
	imul	ecx, edx, 100
	sub	eax, ecx
	mov	ecx, ebx
	mov	ebx, edx
	add	eax, eax
	mov	edx, r12d
	lea	r8d, 1[rax]
	movzx	eax, BYTE PTR 112[rsp+rax]
	movzx	r8d, BYTE PTR 112[rsp+r8]
	mov	BYTE PTR 67[rsp+rdx], r8b
	lea	edx, -1[r12]
	sub	r12d, 2
	cmp	ecx, 9999
	mov	BYTE PTR 67[rsp+rdx], al
	ja	.L1079
	cmp	ecx, 999
	jbe	.L1070
.L1072:
	add	ebx, ebx
	lea	eax, 1[rbx]
	movzx	ebx, BYTE PTR 112[rsp+rbx]
	movzx	eax, BYTE PTR 112[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	jmp	.L1080
	.p2align 4,,10
	.p2align 3
.L1132:
	bsr	r8d, ebx
	mov	r9d, 32
	mov	eax, 31
	xor	r8d, 31
	sub	r9d, r8d
	sub	eax, r8d
	je	.L1065
	mov	edx, eax
	lea	rcx, 63[rsp+rdx]
	lea	rax, 64[rsp+rdx]
	mov	edx, 30
	sub	edx, r8d
	sub	rcx, rdx
	.p2align 4,,10
	.p2align 3
.L1064:
	mov	edx, ebx
	sub	rax, 1
	shr	ebx
	and	edx, 1
	add	edx, 48
	mov	BYTE PTR 4[rax], dl
	cmp	rax, rcx
	jne	.L1064
.L1065:
	lea	r12, 67[rsp]
	movsx	rbx, r9d
	mov	eax, 49
	add	rbx, r12
	jmp	.L1062
	.p2align 4,,10
	.p2align 3
.L1108:
	mov	eax, 48
	xor	edx, edx
	xor	ebp, ebp
	lea	rbx, 68[rsp]
	xor	ecx, ecx
	lea	r12, 67[rsp]
	jmp	.L1081
	.p2align 4,,10
	.p2align 3
.L1136:
	test	ebx, ebx
	jne	.L1109
	mov	BYTE PTR 67[rsp], 48
	lea	rbp, .LC18[rip]
	lea	rbx, 68[rsp]
	lea	r12, 67[rsp]
	jmp	.L1088
	.p2align 4,,10
	.p2align 3
.L1110:
	lea	rbp, .LC17[rip]
.L1087:
	bsr	eax, ebx
	lea	r9d, 4[rax]
	movabs	rax, 3978425819141910832
	shr	r9d, 2
	mov	QWORD PTR 112[rsp], rax
	cmp	ebx, 255
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 120[rsp], rax
	lea	eax, -1[r9]
	jbe	.L1090
	.p2align 4,,10
	.p2align 3
.L1091:
	mov	r8d, ebx
	mov	ecx, eax
	and	r8d, 15
	movzx	r8d, BYTE PTR 112[rsp+r8]
	mov	BYTE PTR 67[rsp+rcx], r8b
	lea	r8d, -1[rax]
	mov	ecx, ebx
	shr	ebx, 8
	shr	ecx, 4
	sub	eax, 2
	and	ecx, 15
	cmp	ebx, 255
	movzx	ecx, BYTE PTR 112[rsp+rcx]
	mov	BYTE PTR 67[rsp+r8], cl
	ja	.L1091
.L1090:
	cmp	ebx, 15
	ja	.L1140
	movzx	eax, BYTE PTR 112[rsp+rbx]
.L1093:
	lea	r12, 67[rsp]
	mov	ebx, r9d
	mov	BYTE PTR 67[rsp], al
	add	rbx, r12
	cmp	dl, 48
	je	.L1141
.L1088:
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	jne	.L1113
	jmp	.L1114
	.p2align 4,,10
	.p2align 3
.L1140:
	mov	eax, ebx
	shr	ebx, 4
	and	eax, 15
	movzx	eax, BYTE PTR 112[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	movzx	eax, BYTE PTR 112[rsp+rbx]
	jmp	.L1093
	.p2align 4,,10
	.p2align 3
.L1134:
	mov	eax, ebx
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 68[rsp], al
	mov	eax, ebx
	shr	eax, 3
	add	eax, 48
	jmp	.L1085
.L1102:
	mov	ebp, 1
	.p2align 4,,10
	.p2align 3
.L1070:
	add	ebx, 48
.L1080:
	lea	r12, 67[rsp]
	mov	BYTE PTR 67[rsp], bl
	lea	rbx, [r12+rbp]
	jmp	.L1069
	.p2align 4,,10
	.p2align 3
.L1109:
	lea	rbp, .LC18[rip]
	jmp	.L1087
	.p2align 4,,10
	.p2align 3
.L1111:
	lea	rbx, 68[rsp]
	lea	rbp, .LC17[rip]
	lea	r12, 67[rsp]
.L1089:
	mov	r13, r12
	.p2align 4,,10
	.p2align 3
.L1094:
	movsx	ecx, BYTE PTR 0[r13]
	add	r13, 1
	call	toupper
	mov	BYTE PTR -1[r13], al
	cmp	r13, rbx
	jne	.L1094
	mov	edx, 1
	mov	ecx, 2
	jmp	.L1086
	.p2align 4,,10
	.p2align 3
.L1141:
	test	r9d, r9d
	jne	.L1089
	mov	edx, 1
	mov	ecx, 2
	mov	rbx, r12
	jmp	.L1086
	.p2align 4,,10
	.p2align 3
.L1105:
	mov	ebp, 7
	jmp	.L1076
	.p2align 4,,10
	.p2align 3
.L1106:
	mov	ebp, 8
	jmp	.L1076
	.p2align 4,,10
	.p2align 3
.L1107:
	mov	ebp, 9
	jmp	.L1076
	.p2align 4,,10
	.p2align 3
.L1135:
	mov	rdx, rcx
	neg	rdx
	jmp	.L1066
.L1137:
	lea	rcx, 112[rsp]
	mov	r8d, 201
	mov	ebp, 2
	lea	rdx, .LC20[rip]
	call	memcpy
	jmp	.L1072
.L1103:
	mov	ebp, 3
	mov	r12d, 2
	jmp	.L1073
.L1138:
	mov	ebp, 4
	mov	r12d, 3
	jmp	.L1073
.L1139:
	mov	ebp, 1
	jmp	.L1077
.L1053:
	lea	rcx, .LC19[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIxNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIxNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIxNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIxNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIxNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB4908:
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
	sub	rsp, 360
	.seh_stackalloc	360
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	r12, rdx
	mov	edx, eax
	mov	rdi, rcx
	and	edx, 120
	mov	rbp, r8
	mov	rbx, r12
	cmp	dl, 56
	je	.L1229
	shr	al, 3
	and	eax, 15
	test	r12, r12
	js	.L1230
	cmp	al, 4
	je	.L1152
	ja	.L1153
	cmp	al, 1
	jbe	.L1154
	lea	r14, .LC14[rip]
	cmp	dl, 16
	lea	rax, .LC15[rip]
	cmovne	r14, rax
	test	r12, r12
	jne	.L1150
	lea	rsi, 68[rsp]
	mov	eax, 48
	lea	r13, 67[rsp]
.L1159:
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], al
	test	bl, 16
	je	.L1211
.L1210:
	mov	rdx, -2
	mov	eax, 2
.L1163:
	add	rdx, r13
	test	eax, eax
	mov	r9d, eax
	je	.L1164
	xor	eax, eax
.L1191:
	mov	ecx, eax
	add	eax, 1
	movzx	r8d, BYTE PTR [r14+rcx]
	cmp	eax, r9d
	mov	BYTE PTR [rdx+rcx], r8b
	jb	.L1191
	.p2align 4,,10
	.p2align 3
.L1164:
	lea	rcx, -1[rdx]
	mov	eax, ebx
	shr	al, 2
	and	eax, 3
	test	r12, r12
	jns	.L1165
	mov	BYTE PTR -1[rdx], 45
	mov	rdx, rcx
.L1193:
	lea	rax, 48[rsp]
	mov	r8, r13
	sub	rsi, rdx
	mov	QWORD PTR 56[rsp], rdx
	sub	r8, rdx
	mov	r9, rbp
	mov	rdx, rax
	mov	QWORD PTR 48[rsp], rsi
	mov	rcx, rdi
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L1145
	.p2align 4,,10
	.p2align 3
.L1230:
	neg	rbx
	cmp	al, 4
	je	.L1147
	ja	.L1148
	cmp	al, 1
	jbe	.L1149
	lea	r14, .LC14[rip]
	cmp	dl, 16
	lea	rax, .LC15[rip]
	cmovne	r14, rax
.L1150:
	bsr	r8, rbx
	mov	esi, 64
	xor	r8, 63
	mov	eax, 63
	sub	esi, r8d
	sub	eax, r8d
	je	.L1162
	mov	edx, eax
	lea	rcx, 63[rsp+rdx]
	lea	rax, 64[rsp+rdx]
	mov	edx, 62
	sub	edx, r8d
	sub	rcx, rdx
	.p2align 4,,10
	.p2align 3
.L1161:
	mov	edx, ebx
	sub	rax, 1
	shr	rbx
	and	edx, 1
	add	edx, 48
	mov	BYTE PTR 4[rax], dl
	cmp	rax, rcx
	jne	.L1161
.L1162:
	lea	r13, 67[rsp]
	movsx	rsi, esi
	mov	eax, 49
	add	rsi, r13
	jmp	.L1159
	.p2align 4,,10
	.p2align 3
.L1229:
	lea	rax, 128[r12]
	cmp	rax, 255
	ja	.L1144
	lea	rax, 144[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	r9, rdi
	mov	edx, 1
	lea	rcx, 48[rsp]
	mov	BYTE PTR 144[rsp], r12b
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1145:
	add	rsp, 360
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
.L1153:
	cmp	dl, 40
	je	.L1231
	test	r12, r12
	jne	.L1207
	movzx	ebx, BYTE PTR [rcx]
	mov	BYTE PTR 67[rsp], 48
	lea	rsi, 68[rsp]
	cmp	dl, 48
	lea	r14, .LC17[rip]
	lea	r13, 67[rsp]
	je	.L1184
.L1185:
	test	bl, 16
	jne	.L1210
	.p2align 4,,10
	.p2align 3
.L1211:
	mov	rdx, r13
	jmp	.L1164
	.p2align 4,,10
	.p2align 3
.L1148:
	lea	r14, .LC18[rip]
	cmp	dl, 40
	lea	rax, .LC17[rip]
	cmovne	r14, rax
.L1151:
	bsr	rax, rbx
	lea	r9d, 4[rax]
	movabs	rax, 3978425819141910832
	shr	r9d, 2
	mov	QWORD PTR 144[rsp], rax
	cmp	rbx, 255
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 152[rsp], rax
	lea	eax, -1[r9]
	jbe	.L1186
	.p2align 4,,10
	.p2align 3
.L1187:
	mov	r8, rbx
	mov	ecx, eax
	and	r8d, 15
	movzx	r8d, BYTE PTR 144[rsp+r8]
	mov	BYTE PTR 67[rsp+rcx], r8b
	lea	r8d, -1[rax]
	mov	rcx, rbx
	shr	rbx, 8
	shr	rcx, 4
	sub	eax, 2
	and	ecx, 15
	cmp	rbx, 255
	movzx	ecx, BYTE PTR 144[rsp+rcx]
	mov	BYTE PTR 67[rsp+r8], cl
	ja	.L1187
.L1186:
	cmp	rbx, 15
	ja	.L1232
	movzx	eax, BYTE PTR 144[rsp+rbx]
.L1189:
	lea	r13, 67[rsp]
	mov	esi, r9d
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], al
	add	rsi, r13
	cmp	dl, 48
	jne	.L1185
	test	r9d, r9d
	jne	.L1184
	mov	ecx, 1
	mov	eax, 2
	mov	rsi, r13
	jmp	.L1183
	.p2align 4,,10
	.p2align 3
.L1184:
	mov	r15, r13
	.p2align 4,,10
	.p2align 3
.L1190:
	movsx	ecx, BYTE PTR [r15]
	add	r15, 1
	call	toupper
	mov	BYTE PTR -1[r15], al
	cmp	rsi, r15
	jne	.L1190
	mov	ecx, 1
	mov	eax, 2
	jmp	.L1183
	.p2align 4,,10
	.p2align 3
.L1154:
	test	r12, r12
	jne	.L1149
	movzx	eax, BYTE PTR [rcx]
	lea	r13, 67[rsp]
	mov	BYTE PTR 67[rsp], 48
	lea	rsi, 68[rsp]
	mov	rdx, r13
	lea	rcx, 66[rsp]
	shr	al, 2
	and	eax, 3
.L1165:
	movzx	eax, al
	cmp	eax, 1
	je	.L1233
	cmp	eax, 3
	jne	.L1193
	mov	BYTE PTR -1[rdx], 32
.L1196:
	mov	rdx, rcx
	jmp	.L1193
	.p2align 4,,10
	.p2align 3
.L1233:
	mov	BYTE PTR -1[rdx], 43
	jmp	.L1196
	.p2align 4,,10
	.p2align 3
.L1152:
	test	r12, r12
	jne	.L1147
	xor	ecx, ecx
	xor	eax, eax
	xor	r14d, r14d
	lea	rsi, 68[rsp]
	mov	edx, 48
	lea	r13, 67[rsp]
.L1178:
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], dl
.L1183:
	test	bl, 16
	je	.L1211
	mov	rdx, rax
	neg	rdx
	test	cl, cl
	jne	.L1163
	mov	rdx, r13
	jmp	.L1164
	.p2align 4,,10
	.p2align 3
.L1149:
	cmp	rbx, 9
	jbe	.L1201
	cmp	rbx, 99
	jbe	.L1234
	cmp	rbx, 999
	jbe	.L1202
	cmp	rbx, 9999
	jbe	.L1203
	mov	rdx, rbx
	mov	esi, 1
	movabs	r8, 3777893186295716171
	jmp	.L1170
	.p2align 4,,10
	.p2align 3
.L1174:
	cmp	rcx, 999999
	jbe	.L1235
	cmp	rcx, 9999999
	jbe	.L1236
	cmp	rcx, 99999999
	jbe	.L1237
.L1170:
	mov	rax, rdx
	mov	rcx, rdx
	mul	r8
	mov	eax, esi
	add	esi, 4
	shr	rdx, 11
	cmp	rcx, 99999
	ja	.L1174
.L1172:
	cmp	esi, 64
	ja	.L1204
	lea	r13d, -1[rsi]
.L1169:
	lea	rcx, 144[rsp]
	mov	r8d, 201
	lea	rdx, .LC20[rip]
	call	memcpy
	movabs	r8, 2951479051793528259
	.p2align 4,,10
	.p2align 3
.L1176:
	mov	rdx, rbx
	shr	rdx, 2
	mov	rax, rdx
	mul	r8
	mov	rax, rbx
	shr	rdx, 2
	imul	rcx, rdx, 100
	sub	rax, rcx
	mov	rcx, rbx
	mov	rbx, rdx
	add	rax, rax
	mov	edx, r13d
	movzx	r9d, BYTE PTR 145[rsp+rax]
	movzx	eax, BYTE PTR 144[rsp+rax]
	mov	BYTE PTR 67[rsp+rdx], r9b
	lea	edx, -1[r13]
	sub	r13d, 2
	cmp	rcx, 9999
	mov	BYTE PTR 67[rsp+rdx], al
	ja	.L1176
	cmp	rcx, 999
	ja	.L1168
.L1166:
	add	ebx, 48
.L1177:
	lea	r13, 67[rsp]
	mov	BYTE PTR 67[rsp], bl
	add	rsi, r13
.L1175:
	movzx	ebx, BYTE PTR [rdi]
	mov	rdx, r13
	jmp	.L1164
	.p2align 4,,10
	.p2align 3
.L1147:
	bsr	rax, rbx
	lea	esi, 3[rax]
	mov	eax, 2863311531
	imul	rsi, rax
	shr	rsi, 33
	cmp	rbx, 63
	lea	edx, -1[rsi]
	jbe	.L1179
	.p2align 4,,10
	.p2align 3
.L1180:
	mov	rax, rbx
	mov	ecx, edx
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 67[rsp+rcx], al
	lea	ecx, -1[rdx]
	mov	rax, rbx
	shr	rbx, 6
	shr	rax, 3
	sub	edx, 2
	and	eax, 7
	add	eax, 48
	cmp	rbx, 63
	mov	BYTE PTR 67[rsp+rcx], al
	ja	.L1180
.L1179:
	lea	edx, 48[rbx]
	cmp	rbx, 7
	jbe	.L1182
	mov	rax, rbx
	shr	rbx, 3
	and	eax, 7
	mov	rdx, rbx
	add	eax, 48
	add	edx, 48
	mov	BYTE PTR 68[rsp], al
.L1182:
	lea	r13, 67[rsp]
	mov	esi, esi
	mov	ecx, 1
	lea	r14, .LC16[rip]
	add	rsi, r13
	mov	eax, 1
	jmp	.L1178
	.p2align 4,,10
	.p2align 3
.L1232:
	mov	rax, rbx
	shr	rbx, 4
	and	eax, 15
	movzx	eax, BYTE PTR 144[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	movzx	eax, BYTE PTR 144[rsp+rbx]
	jmp	.L1189
.L1234:
	lea	rcx, 144[rsp]
	mov	r8d, 201
	mov	esi, 2
	lea	rdx, .LC20[rip]
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L1168:
	add	rbx, rbx
	movzx	eax, BYTE PTR 145[rsp+rbx]
	movzx	ebx, BYTE PTR 144[rsp+rbx]
	mov	BYTE PTR 68[rsp], al
	jmp	.L1177
	.p2align 4,,10
	.p2align 3
.L1231:
	test	r12, r12
	jne	.L1206
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], 48
	mov	ecx, 1
	mov	eax, 2
	lea	r14, .LC18[rip]
	lea	rsi, 68[rsp]
	lea	r13, 67[rsp]
	jmp	.L1183
	.p2align 4,,10
	.p2align 3
.L1235:
	lea	esi, 5[rax]
	jmp	.L1172
	.p2align 4,,10
	.p2align 3
.L1236:
	lea	esi, 6[rax]
	jmp	.L1172
	.p2align 4,,10
	.p2align 3
.L1237:
	lea	esi, 7[rax]
	jmp	.L1172
	.p2align 4,,10
	.p2align 3
.L1207:
	lea	r14, .LC17[rip]
	jmp	.L1151
.L1204:
	lea	rsi, 131[rsp]
	lea	r13, 67[rsp]
	jmp	.L1175
.L1206:
	lea	r14, .LC18[rip]
	jmp	.L1151
.L1201:
	mov	esi, 1
	jmp	.L1166
.L1203:
	mov	esi, 4
	mov	r13d, 3
	jmp	.L1169
.L1202:
	mov	esi, 3
	mov	r13d, 2
	jmp	.L1169
.L1144:
	lea	rcx, .LC19[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIyNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIyNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIyNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIyNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIyNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB4910:
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
	sub	rsp, 360
	.seh_stackalloc	360
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	rbx, rdx
	mov	edx, eax
	mov	rdi, rcx
	and	edx, 120
	mov	rbp, r8
	cmp	dl, 56
	je	.L1316
	shr	al, 3
	and	eax, 15
	cmp	al, 4
	je	.L1242
	ja	.L1243
	cmp	al, 1
	jbe	.L1244
	lea	r13, .LC14[rip]
	cmp	dl, 16
	lea	rax, .LC15[rip]
	cmovne	r13, rax
	test	rbx, rbx
	jne	.L1317
	lea	rsi, 68[rsp]
	mov	eax, 48
	lea	r12, 67[rsp]
.L1249:
	mov	BYTE PTR 67[rsp], al
	movzx	eax, BYTE PTR [rdi]
	test	al, 16
	je	.L1299
.L1298:
	mov	rdx, -2
	mov	ebx, 2
.L1253:
	add	rdx, r12
	test	ebx, ebx
	mov	r10d, ebx
	je	.L1254
	xor	ecx, ecx
.L1282:
	mov	r8d, ecx
	add	ecx, 1
	movzx	r9d, BYTE PTR 0[r13+r8]
	cmp	ecx, r10d
	mov	BYTE PTR [rdx+r8], r9b
	jb	.L1282
	jmp	.L1254
	.p2align 4,,10
	.p2align 3
.L1316:
	cmp	rbx, 127
	ja	.L1240
	lea	rax, 144[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	r9, rdi
	mov	edx, 1
	lea	rcx, 48[rsp]
	mov	BYTE PTR 144[rsp], bl
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	add	rsp, 360
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L1244:
	test	rbx, rbx
	jne	.L1255
	mov	BYTE PTR 67[rsp], 48
	lea	rsi, 68[rsp]
	lea	r12, 67[rsp]
.L1256:
	movzx	eax, BYTE PTR [rdi]
	mov	rdx, r12
.L1254:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L1318
.L1284:
	cmp	eax, 3
	je	.L1300
.L1285:
	lea	rax, 48[rsp]
	mov	r8, r12
	sub	rsi, rdx
	mov	QWORD PTR 56[rsp], rdx
	sub	r8, rdx
	mov	r9, rbp
	mov	rdx, rax
	mov	QWORD PTR 48[rsp], rsi
	mov	rcx, rdi
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	add	rsp, 360
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L1242:
	test	rbx, rbx
	je	.L1293
	bsr	rax, rbx
	lea	esi, 3[rax]
	mov	eax, 2863311531
	imul	rsi, rax
	shr	rsi, 33
	cmp	rbx, 63
	lea	edx, -1[rsi]
	jbe	.L1269
	.p2align 4,,10
	.p2align 3
.L1270:
	mov	rax, rbx
	mov	ecx, edx
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 67[rsp+rcx], al
	lea	ecx, -1[rdx]
	mov	rax, rbx
	shr	rbx, 6
	shr	rax, 3
	sub	edx, 2
	and	eax, 7
	add	eax, 48
	cmp	rbx, 63
	mov	BYTE PTR 67[rsp+rcx], al
	ja	.L1270
.L1269:
	lea	eax, 48[rbx]
	cmp	rbx, 7
	ja	.L1319
.L1272:
	lea	r12, 67[rsp]
	mov	esi, esi
	mov	edx, 1
	lea	r13, .LC16[rip]
	add	rsi, r12
	mov	ebx, 1
.L1268:
	mov	BYTE PTR 67[rsp], al
.L1273:
	movzx	eax, BYTE PTR [rdi]
	test	al, 16
	je	.L1299
	test	dl, dl
	jne	.L1320
.L1299:
	shr	al, 2
	mov	rdx, r12
	and	eax, 3
	cmp	eax, 1
	jne	.L1284
.L1318:
	mov	eax, 43
.L1286:
	mov	BYTE PTR -1[rdx], al
	sub	rdx, 1
	jmp	.L1285
	.p2align 4,,10
	.p2align 3
.L1243:
	cmp	dl, 40
	je	.L1321
	test	rbx, rbx
	jne	.L1295
	cmp	dl, 48
	mov	BYTE PTR 67[rsp], 48
	je	.L1296
	lea	r13, .LC17[rip]
	lea	rsi, 68[rsp]
	lea	r12, 67[rsp]
	jmp	.L1275
	.p2align 4,,10
	.p2align 3
.L1300:
	mov	eax, 32
	jmp	.L1286
	.p2align 4,,10
	.p2align 3
.L1255:
	cmp	rbx, 9
	jbe	.L1289
	cmp	rbx, 99
	jbe	.L1322
	cmp	rbx, 999
	jbe	.L1290
	cmp	rbx, 9999
	jbe	.L1291
	mov	rdx, rbx
	mov	esi, 1
	movabs	r8, 3777893186295716171
	jmp	.L1261
	.p2align 4,,10
	.p2align 3
.L1265:
	cmp	rcx, 999999
	jbe	.L1323
	cmp	rcx, 9999999
	jbe	.L1324
	cmp	rcx, 99999999
	jbe	.L1325
.L1261:
	mov	rax, rdx
	mov	rcx, rdx
	mul	r8
	mov	eax, esi
	add	esi, 4
	shr	rdx, 11
	cmp	rcx, 99999
	ja	.L1265
.L1263:
	cmp	esi, 64
	ja	.L1292
	lea	r12d, -1[rsi]
.L1260:
	lea	rcx, 144[rsp]
	mov	r8d, 201
	lea	rdx, .LC20[rip]
	call	memcpy
	movabs	r8, 2951479051793528259
	.p2align 4,,10
	.p2align 3
.L1266:
	mov	rdx, rbx
	shr	rdx, 2
	mov	rax, rdx
	mul	r8
	mov	rax, rbx
	shr	rdx, 2
	imul	rcx, rdx, 100
	sub	rax, rcx
	mov	rcx, rbx
	mov	rbx, rdx
	add	rax, rax
	mov	edx, r12d
	movzx	r9d, BYTE PTR 145[rsp+rax]
	movzx	eax, BYTE PTR 144[rsp+rax]
	mov	BYTE PTR 67[rsp+rdx], r9b
	lea	edx, -1[r12]
	sub	r12d, 2
	cmp	rcx, 9999
	mov	BYTE PTR 67[rsp+rdx], al
	ja	.L1266
	cmp	rcx, 999
	jbe	.L1257
.L1259:
	add	rbx, rbx
	movzx	eax, BYTE PTR 145[rsp+rbx]
	movzx	ebx, BYTE PTR 144[rsp+rbx]
	mov	BYTE PTR 68[rsp], al
	jmp	.L1267
	.p2align 4,,10
	.p2align 3
.L1317:
	bsr	r8, rbx
	mov	esi, 64
	mov	eax, 63
	xor	r8, 63
	sub	esi, r8d
	sub	eax, r8d
	je	.L1252
	mov	edx, eax
	lea	rcx, 63[rsp+rdx]
	lea	rax, 64[rsp+rdx]
	mov	edx, 62
	sub	edx, r8d
	sub	rcx, rdx
	.p2align 4,,10
	.p2align 3
.L1251:
	mov	edx, ebx
	sub	rax, 1
	shr	rbx
	and	edx, 1
	add	edx, 48
	mov	BYTE PTR 4[rax], dl
	cmp	rax, rcx
	jne	.L1251
.L1252:
	lea	r12, 67[rsp]
	movsx	rsi, esi
	mov	eax, 49
	add	rsi, r12
	jmp	.L1249
	.p2align 4,,10
	.p2align 3
.L1293:
	mov	eax, 48
	xor	edx, edx
	xor	r13d, r13d
	lea	rsi, 68[rsp]
	lea	r12, 67[rsp]
	jmp	.L1268
	.p2align 4,,10
	.p2align 3
.L1321:
	test	rbx, rbx
	jne	.L1294
	mov	BYTE PTR 67[rsp], 48
	lea	r13, .LC18[rip]
	lea	rsi, 68[rsp]
	lea	r12, 67[rsp]
	jmp	.L1275
	.p2align 4,,10
	.p2align 3
.L1295:
	lea	r13, .LC17[rip]
.L1274:
	bsr	rax, rbx
	lea	r9d, 4[rax]
	movabs	rax, 3978425819141910832
	shr	r9d, 2
	mov	QWORD PTR 144[rsp], rax
	cmp	rbx, 255
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 152[rsp], rax
	lea	eax, -1[r9]
	jbe	.L1277
	.p2align 4,,10
	.p2align 3
.L1278:
	mov	r8, rbx
	mov	ecx, eax
	and	r8d, 15
	movzx	r8d, BYTE PTR 144[rsp+r8]
	mov	BYTE PTR 67[rsp+rcx], r8b
	lea	r8d, -1[rax]
	mov	rcx, rbx
	shr	rbx, 8
	shr	rcx, 4
	sub	eax, 2
	and	ecx, 15
	cmp	rbx, 255
	movzx	ecx, BYTE PTR 144[rsp+rcx]
	mov	BYTE PTR 67[rsp+r8], cl
	ja	.L1278
.L1277:
	cmp	rbx, 15
	ja	.L1326
	movzx	eax, BYTE PTR 144[rsp+rbx]
.L1280:
	lea	r12, 67[rsp]
	mov	esi, r9d
	mov	BYTE PTR 67[rsp], al
	add	rsi, r12
	cmp	dl, 48
	je	.L1327
.L1275:
	movzx	eax, BYTE PTR [rdi]
	test	al, 16
	jne	.L1298
	jmp	.L1299
	.p2align 4,,10
	.p2align 3
.L1326:
	mov	rax, rbx
	shr	rbx, 4
	and	eax, 15
	movzx	eax, BYTE PTR 144[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	movzx	eax, BYTE PTR 144[rsp+rbx]
	jmp	.L1280
	.p2align 4,,10
	.p2align 3
.L1319:
	mov	rax, rbx
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 68[rsp], al
	mov	rax, rbx
	shr	rax, 3
	add	eax, 48
	jmp	.L1272
.L1289:
	mov	esi, 1
	.p2align 4,,10
	.p2align 3
.L1257:
	add	ebx, 48
.L1267:
	lea	r12, 67[rsp]
	mov	BYTE PTR 67[rsp], bl
	add	rsi, r12
	jmp	.L1256
	.p2align 4,,10
	.p2align 3
.L1294:
	lea	r13, .LC18[rip]
	jmp	.L1274
	.p2align 4,,10
	.p2align 3
.L1296:
	lea	rsi, 68[rsp]
	lea	r13, .LC17[rip]
	lea	r12, 67[rsp]
.L1276:
	mov	rbx, r12
	.p2align 4,,10
	.p2align 3
.L1281:
	movsx	ecx, BYTE PTR [rbx]
	add	rbx, 1
	call	toupper
	mov	BYTE PTR -1[rbx], al
	cmp	rbx, rsi
	jne	.L1281
	mov	edx, 1
	mov	ebx, 2
	jmp	.L1273
	.p2align 4,,10
	.p2align 3
.L1327:
	test	r9d, r9d
	jne	.L1276
	mov	edx, 1
	mov	ebx, 2
	mov	rsi, r12
	jmp	.L1273
	.p2align 4,,10
	.p2align 3
.L1323:
	lea	esi, 5[rax]
	jmp	.L1263
	.p2align 4,,10
	.p2align 3
.L1324:
	lea	esi, 6[rax]
	jmp	.L1263
	.p2align 4,,10
	.p2align 3
.L1325:
	lea	esi, 7[rax]
	jmp	.L1263
	.p2align 4,,10
	.p2align 3
.L1320:
	mov	rdx, rbx
	neg	rdx
	jmp	.L1253
.L1292:
	lea	rsi, 131[rsp]
	lea	r12, 67[rsp]
	jmp	.L1256
.L1322:
	lea	rcx, 144[rsp]
	mov	r8d, 201
	mov	esi, 2
	lea	rdx, .LC20[rip]
	call	memcpy
	jmp	.L1259
.L1290:
	mov	esi, 3
	mov	r12d, 2
	jmp	.L1260
.L1291:
	mov	esi, 4
	mov	r12d, 3
	jmp	.L1260
.L1240:
	lea	rcx, .LC19[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.def	__udivti3;	.scl	2;	.type	32;	.endef
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB4928:
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
	sub	rsp, 504
	.seh_stackalloc	504
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	r12, QWORD PTR [rdx]
	mov	r13, QWORD PTR 8[rdx]
	mov	edx, eax
	mov	QWORD PTR 576[rsp], rcx
	and	edx, 120
	mov	QWORD PTR 592[rsp], r8
	cmp	dl, 56
	je	.L1422
	shr	al, 3
	mov	rsi, r12
	mov	rdi, r13
	and	eax, 15
	test	r13, r13
	js	.L1423
	cmp	al, 4
	je	.L1338
	ja	.L1339
	cmp	al, 1
	jbe	.L1340
	lea	rax, .LC15[rip]
	cmp	dl, 16
	lea	rbx, .LC14[rip]
	cmovne	rbx, rax
	mov	rax, r12
	or	rax, r13
	jne	.L1336
	lea	rdi, 148[rsp]
	mov	eax, 48
	lea	r8, 147[rsp]
.L1345:
	mov	BYTE PTR 147[rsp], al
	mov	rax, QWORD PTR 576[rsp]
	movzx	edx, BYTE PTR [rax]
	test	dl, 16
	je	.L1403
.L1402:
	mov	rcx, -2
	mov	eax, 2
.L1350:
	add	rcx, r8
	test	eax, eax
	mov	r11d, eax
	je	.L1351
	xor	eax, eax
.L1382:
	mov	r9d, eax
	add	eax, 1
	movzx	r10d, BYTE PTR [rbx+r9]
	cmp	eax, r11d
	mov	BYTE PTR [rcx+r9], r10b
	jb	.L1382
.L1351:
	lea	rax, -1[rcx]
	shr	dl, 2
	and	edx, 3
	test	r13, r13
	jns	.L1352
.L1430:
	mov	BYTE PTR -1[rcx], 45
	mov	rcx, rax
.L1384:
	sub	rdi, rcx
	mov	QWORD PTR 136[rsp], rcx
	sub	r8, rcx
	mov	r9, QWORD PTR 592[rsp]
	mov	rcx, QWORD PTR 576[rsp]
	lea	rdx, 128[rsp]
	mov	QWORD PTR 128[rsp], rdi
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L1331
	.p2align 4,,10
	.p2align 3
.L1423:
	neg	rsi
	adc	rdi, 0
	neg	rdi
	cmp	al, 4
	je	.L1333
	ja	.L1334
	cmp	al, 1
	jbe	.L1335
	lea	rbx, .LC14[rip]
	cmp	dl, 16
	lea	rax, .LC15[rip]
	cmovne	rbx, rax
.L1336:
	test	rdi, rdi
	jne	.L1424
	bsr	rdx, rsi
	mov	eax, 128
	mov	ecx, 127
	xor	rdx, 63
	add	edx, 64
	sub	eax, edx
	sub	ecx, edx
	je	.L1391
.L1347:
	mov	r8d, ecx
	sub	ecx, 1
	lea	rdx, 144[rsp+r8]
	lea	r8, 143[rsp+r8]
	sub	r8, rcx
	.p2align 4,,10
	.p2align 3
.L1349:
	mov	ecx, esi
	sub	rdx, 1
	shrd	rsi, rdi, 1
	and	ecx, 1
	shr	rdi
	add	ecx, 48
	mov	BYTE PTR 4[rdx], cl
	cmp	rdx, r8
	jne	.L1349
.L1348:
	lea	r8, 147[rsp]
	cdqe
	lea	rdi, [r8+rax]
	mov	eax, 49
	jmp	.L1345
	.p2align 4,,10
	.p2align 3
.L1422:
	mov	eax, 127
	cmp	rax, r12
	mov	eax, 0
	sbb	rax, r13
	jl	.L1330
	mov	r9, QWORD PTR 576[rsp]
	lea	rax, 288[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	edx, 1
	lea	rcx, 128[rsp]
	mov	BYTE PTR 288[rsp], r12b
	mov	QWORD PTR 128[rsp], 1
	mov	QWORD PTR 136[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1331:
	add	rsp, 504
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
.L1339:
	cmp	dl, 40
	je	.L1425
	mov	rax, r12
	or	rax, r13
	jne	.L1399
	cmp	dl, 48
	mov	BYTE PTR 147[rsp], 48
	je	.L1400
	lea	rbx, .LC17[rip]
	lea	rdi, 148[rsp]
	lea	r8, 147[rsp]
	jmp	.L1373
	.p2align 4,,10
	.p2align 3
.L1334:
	lea	rbx, .LC18[rip]
	cmp	dl, 40
	lea	rax, .LC17[rip]
	cmovne	rbx, rax
.L1337:
	test	rdi, rdi
	jne	.L1426
	bsr	rax, rsi
	mov	ecx, 255
	lea	ebp, 4[rax]
	movabs	rax, 3978425819141910832
	shr	ebp, 2
	mov	QWORD PTR 288[rsp], rax
	cmp	rcx, rsi
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 296[rsp], rax
	lea	eax, -1[rbp]
	jnb	.L1427
.L1376:
	lea	rcx, 288[rsp]
	mov	r11d, 255
	xor	r10d, r10d
	.p2align 4,,10
	.p2align 3
.L1378:
	mov	r8, rsi
	mov	r14d, eax
	mov	r15, r10
	lea	r9d, -1[rax]
	and	r8d, 15
	sub	eax, 2
	add	r8, rcx
	movzx	r8d, BYTE PTR [r8]
	mov	BYTE PTR 147[rsp+r14], r8b
	mov	r8, rsi
	shrd	rsi, rdi, 8
	shrd	r8, rdi, 4
	shr	rdi, 8
	mov	r14, r8
	and	r14d, 15
	cmp	r11, rsi
	lea	r8, [r14+rcx]
	sbb	r15, rdi
	movzx	r8d, BYTE PTR [r8]
	mov	BYTE PTR 147[rsp+r9], r8b
	jc	.L1378
.L1377:
	mov	eax, 15
	cmp	rax, rsi
	mov	eax, 0
	sbb	rax, rdi
	jc	.L1428
	add	rcx, rsi
	movzx	eax, BYTE PTR [rcx]
.L1380:
	lea	r8, 147[rsp]
	mov	edi, ebp
	mov	BYTE PTR 147[rsp], al
	add	rdi, r8
	cmp	dl, 48
	je	.L1429
.L1373:
	mov	rax, QWORD PTR 576[rsp]
	movzx	edx, BYTE PTR [rax]
	test	dl, 16
	jne	.L1402
	.p2align 4,,10
	.p2align 3
.L1403:
	shr	dl, 2
	mov	rcx, r8
	lea	rax, -1[rcx]
	and	edx, 3
	test	r13, r13
	js	.L1430
.L1352:
	movzx	edx, dl
	cmp	edx, 1
	je	.L1431
	cmp	edx, 3
	jne	.L1384
	mov	BYTE PTR -1[rcx], 32
.L1387:
	mov	rcx, rax
	jmp	.L1384
	.p2align 4,,10
	.p2align 3
.L1431:
	mov	BYTE PTR -1[rcx], 43
	jmp	.L1387
	.p2align 4,,10
	.p2align 3
.L1338:
	mov	rax, r12
	or	rax, r13
	jne	.L1333
	xor	ecx, ecx
	xor	eax, eax
	xor	ebx, ebx
	lea	rdi, 148[rsp]
	mov	esi, 48
	lea	r8, 147[rsp]
.L1365:
	mov	BYTE PTR 147[rsp], sil
.L1372:
	mov	rsi, QWORD PTR 576[rsp]
	movzx	edx, BYTE PTR [rsi]
	test	dl, 16
	je	.L1403
	test	cl, cl
	je	.L1403
	mov	rcx, rax
	neg	rcx
	jmp	.L1350
	.p2align 4,,10
	.p2align 3
.L1340:
	mov	rax, r12
	or	rax, r13
	jne	.L1335
	mov	rax, QWORD PTR 576[rsp]
	lea	r8, 147[rsp]
	mov	BYTE PTR 147[rsp], 48
	lea	rdi, 148[rsp]
	mov	rcx, r8
	movzx	eax, BYTE PTR [rax]
	mov	edx, eax
	mov	BYTE PTR 48[rsp], al
	lea	rax, 146[rsp]
	shr	dl, 2
	and	edx, 3
	jmp	.L1352
	.p2align 4,,10
	.p2align 3
.L1335:
	xor	eax, eax
	mov	edx, 9
	cmp	rdx, rsi
	mov	rbx, rax
	sbb	rbx, rdi
	jnc	.L1393
	mov	edx, 99
	mov	rbx, rax
	cmp	rdx, rsi
	sbb	rbx, rdi
	jnc	.L1432
	mov	edx, 999
	mov	rbx, rax
	cmp	rdx, rsi
	sbb	rbx, rdi
	jnc	.L1394
	mov	edx, 9999
	cmp	rdx, rsi
	sbb	rax, rdi
	jnc	.L1395
	lea	rax, 112[rsp]
	mov	rdx, rdi
	mov	QWORD PTR 72[rsp], rdi
	mov	rcx, rsi
	lea	rbx, 96[rsp]
	mov	QWORD PTR 88[rsp], r13
	xor	r15d, r15d
	mov	r13, rax
	mov	r14d, 1
	mov	QWORD PTR 64[rsp], rsi
	mov	rdi, rbx
	mov	QWORD PTR 80[rsp], r12
	jmp	.L1357
	.p2align 4,,10
	.p2align 3
.L1361:
	mov	eax, 999999
	cmp	rax, rbp
	mov	rax, r15
	sbb	rax, rbx
	jnc	.L1433
	mov	eax, 9999999
	cmp	rax, rbp
	mov	rax, r15
	sbb	rax, rbx
	jnc	.L1434
	mov	eax, 99999999
	cmp	rax, rbp
	mov	rax, r15
	sbb	rax, rbx
	jnc	.L1435
.L1357:
	mov	rbp, rcx
	mov	rbx, rdx
	mov	QWORD PTR 112[rsp], rcx
	mov	rcx, r13
	mov	QWORD PTR 120[rsp], rdx
	mov	rdx, rdi
	mov	QWORD PTR 96[rsp], 10000
	mov	QWORD PTR 104[rsp], 0
	call	__udivti3
	mov	eax, 99999
	mov	r9d, r14d
	add	r14d, 4
	cmp	rax, rbp
	mov	rax, r15
	movaps	XMMWORD PTR 48[rsp], xmm0
	mov	rcx, QWORD PTR 48[rsp]
	sbb	rax, rbx
	mov	rdx, QWORD PTR 56[rsp]
	jc	.L1361
	mov	rsi, QWORD PTR 64[rsp]
	mov	rdi, QWORD PTR 72[rsp]
	mov	r12, QWORD PTR 80[rsp]
	mov	r13, QWORD PTR 88[rsp]
.L1359:
	cmp	r14d, 128
	ja	.L1396
	lea	ebx, -1[r14]
	mov	ebp, r14d
.L1356:
	lea	rcx, 288[rsp]
	mov	r8d, 201
	movabs	r14, 1152921504606846975
	lea	rdx, .LC20[rip]
	movabs	r15, -8116567392432202711
	call	memcpy
	mov	QWORD PTR 72[rsp], r13
	mov	r9d, ebx
	mov	r13, rbp
	mov	QWORD PTR 64[rsp], r12
	mov	rbp, rax
	.p2align 4,,10
	.p2align 3
.L1363:
	mov	rax, rsi
	mov	rcx, rsi
	xor	ebx, ebx
	shrd	rax, rdi, 60
	and	rcx, r14
	mov	r12d, 25
	and	rax, r14
	add	rcx, rax
	mov	rax, rdi
	shr	rax, 56
	add	rcx, rax
	movabs	rax, 5165088340638674453
	mul	rcx
	mov	rax, rcx
	sub	rax, rdx
	shr	rax
	add	rdx, rax
	shr	rdx, 4
	lea	rax, [rdx+rdx*4]
	mov	rdx, rdi
	lea	rax, [rax+rax*4]
	sub	rcx, rax
	mov	rax, rsi
	sub	rax, rcx
	sbb	rdx, rbx
	mov	r8, rdx
	movabs	rdx, 2951479051793528258
	imul	rdx, rax
	imul	r8, r15
	add	r8, rdx
	mul	r15
	mov	r10, rax
	mov	r11, rdx
	and	eax, 3
	xor	edx, edx
	add	r11, r8
	imul	r8, rdx, 25
	mul	r12
	add	rdx, r8
	add	rax, rcx
	mov	r8, rsi
	adc	rdx, rbx
	mov	rsi, r10
	mov	ecx, r9d
	shld	rdx, rax, 1
	add	rax, rax
	shrd	rsi, r11, 2
	mov	QWORD PTR 48[rsp], rax
	mov	rax, QWORD PTR 48[rsp]
	mov	QWORD PTR 56[rsp], rdx
	mov	rdx, rdi
	mov	rdi, r11
	shr	rdi, 2
	lea	r10, 0[rbp+rax]
	add	rax, rbp
	movzx	r10d, BYTE PTR 1[r10]
	movzx	eax, BYTE PTR [rax]
	mov	BYTE PTR 147[rsp+rcx], r10b
	lea	ecx, -1[r9]
	sub	r9d, 2
	mov	BYTE PTR 147[rsp+rcx], al
	mov	eax, 9999
	cmp	rax, r8
	mov	eax, 0
	sbb	rax, rdx
	jc	.L1363
	mov	eax, 999
	mov	rcx, rbp
	mov	rbp, r13
	mov	r13, QWORD PTR 72[rsp]
	cmp	rax, r8
	mov	eax, 0
	sbb	rax, rdx
	jnc	.L1353
.L1355:
	add	rsi, rsi
	lea	rax, [rcx+rsi]
	add	rsi, rcx
	movzx	eax, BYTE PTR 1[rax]
	movzx	esi, BYTE PTR [rsi]
	mov	BYTE PTR 148[rsp], al
.L1364:
	lea	r8, 147[rsp]
	mov	BYTE PTR 147[rsp], sil
	lea	rdi, [r8+rbp]
.L1362:
	mov	rax, QWORD PTR 576[rsp]
	mov	rcx, r8
	movzx	edx, BYTE PTR [rax]
	jmp	.L1351
	.p2align 4,,10
	.p2align 3
.L1333:
	test	rdi, rdi
	jne	.L1436
	bsr	rax, rsi
	mov	edx, 2863311531
	mov	ecx, 63
	add	eax, 3
	imul	rax, rdx
	shr	rax, 33
	cmp	rcx, rsi
	lea	edx, -1[rax]
	jnb	.L1368
.L1367:
	mov	r9d, 63
	xor	r8d, r8d
	.p2align 4,,10
	.p2align 3
.L1369:
	mov	rcx, rsi
	mov	r10d, edx
	mov	rbx, r8
	and	ecx, 7
	add	ecx, 48
	mov	BYTE PTR 147[rsp+r10], cl
	lea	r10d, -1[rdx]
	mov	rcx, rsi
	shrd	rsi, rdi, 6
	shrd	rcx, rdi, 3
	sub	edx, 2
	shr	rdi, 6
	and	ecx, 7
	add	ecx, 48
	cmp	r9, rsi
	sbb	rbx, rdi
	mov	BYTE PTR 147[rsp+r10], cl
	jc	.L1369
.L1368:
	mov	edx, 7
	cmp	rdx, rsi
	mov	edx, 0
	sbb	rdx, rdi
	jc	.L1437
	add	esi, 48
.L1371:
	lea	r8, 147[rsp]
	mov	eax, eax
	mov	ecx, 1
	lea	rdi, [r8+rax]
	mov	eax, 1
	lea	rbx, .LC16[rip]
	jmp	.L1365
	.p2align 4,,10
	.p2align 3
.L1437:
	mov	rcx, rsi
	shrd	rsi, rdi, 3
	and	ecx, 7
	add	esi, 48
	add	ecx, 48
	mov	BYTE PTR 148[rsp], cl
	jmp	.L1371
	.p2align 4,,10
	.p2align 3
.L1428:
	mov	r8, rsi
	shrd	rsi, rdi, 4
	and	r8d, 15
	add	rsi, rcx
	add	r8, rcx
	movzx	eax, BYTE PTR [r8]
	mov	BYTE PTR 148[rsp], al
	movzx	eax, BYTE PTR [rsi]
	jmp	.L1380
	.p2align 4,,10
	.p2align 3
.L1400:
	lea	rdi, 148[rsp]
	lea	rbx, .LC17[rip]
	lea	r8, 147[rsp]
.L1374:
	mov	rsi, r8
	mov	rbp, r8
	.p2align 4,,10
	.p2align 3
.L1381:
	movsx	ecx, BYTE PTR [rsi]
	add	rsi, 1
	call	toupper
	mov	BYTE PTR -1[rsi], al
	cmp	rsi, rdi
	jne	.L1381
	mov	r8, rbp
	mov	ecx, 1
	mov	eax, 2
	jmp	.L1372
	.p2align 4,,10
	.p2align 3
.L1426:
	bsr	rax, rdi
	lea	ebp, 68[rax]
	movabs	rax, 3978425819141910832
	shr	ebp, 2
	mov	QWORD PTR 288[rsp], rax
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 296[rsp], rax
	lea	eax, -1[rbp]
	jmp	.L1376
	.p2align 4,,10
	.p2align 3
.L1424:
	bsr	rdx, rdi
	mov	eax, 128
	mov	ecx, 127
	xor	rdx, 63
	sub	eax, edx
	sub	ecx, edx
	jmp	.L1347
	.p2align 4,,10
	.p2align 3
.L1436:
	bsr	rax, rdi
	mov	edx, 2863311531
	add	eax, 67
	imul	rax, rdx
	shr	rax, 33
	lea	edx, -1[rax]
	jmp	.L1367
.L1391:
	mov	eax, 1
	jmp	.L1348
.L1393:
	mov	ebp, 1
	.p2align 4,,10
	.p2align 3
.L1353:
	add	esi, 48
	jmp	.L1364
	.p2align 4,,10
	.p2align 3
.L1429:
	test	ebp, ebp
	jne	.L1374
	mov	ecx, 1
	mov	eax, 2
	mov	rdi, r8
	jmp	.L1372
	.p2align 4,,10
	.p2align 3
.L1425:
	mov	rax, r12
	or	rax, r13
	jne	.L1398
	mov	BYTE PTR 147[rsp], 48
	lea	rbx, .LC18[rip]
	lea	rdi, 148[rsp]
	lea	r8, 147[rsp]
	jmp	.L1373
	.p2align 4,,10
	.p2align 3
.L1433:
	mov	rsi, QWORD PTR 64[rsp]
	lea	r14d, 5[r9]
	mov	rdi, QWORD PTR 72[rsp]
	mov	r12, QWORD PTR 80[rsp]
	mov	r13, QWORD PTR 88[rsp]
	jmp	.L1359
	.p2align 4,,10
	.p2align 3
.L1434:
	mov	rsi, QWORD PTR 64[rsp]
	lea	r14d, 6[r9]
	mov	rdi, QWORD PTR 72[rsp]
	mov	r12, QWORD PTR 80[rsp]
	mov	r13, QWORD PTR 88[rsp]
	jmp	.L1359
	.p2align 4,,10
	.p2align 3
.L1435:
	mov	rsi, QWORD PTR 64[rsp]
	lea	r14d, 7[r9]
	mov	rdi, QWORD PTR 72[rsp]
	mov	r12, QWORD PTR 80[rsp]
	mov	r13, QWORD PTR 88[rsp]
	jmp	.L1359
	.p2align 4,,10
	.p2align 3
.L1399:
	lea	rbx, .LC17[rip]
	jmp	.L1337
	.p2align 4,,10
	.p2align 3
.L1427:
	lea	rcx, 288[rsp]
	jmp	.L1377
.L1396:
	lea	rdi, 275[rsp]
	lea	r8, 147[rsp]
	jmp	.L1362
.L1398:
	lea	rbx, .LC18[rip]
	jmp	.L1337
.L1432:
	lea	rcx, 288[rsp]
	mov	r8d, 201
	mov	ebp, 2
	lea	rdx, .LC20[rip]
	call	memcpy
	mov	rcx, rax
	jmp	.L1355
.L1395:
	mov	ebp, 4
	mov	ebx, 3
	jmp	.L1356
.L1394:
	mov	ebp, 3
	mov	ebx, 2
	jmp	.L1356
.L1330:
	lea	rcx, .LC19[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIoNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIoNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIoNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIoNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIoNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB4930:
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
	sub	rsp, 488
	.seh_stackalloc	488
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	rsi, QWORD PTR [rdx]
	mov	rdi, QWORD PTR 8[rdx]
	mov	edx, eax
	mov	r12, rcx
	mov	r13, r8
	and	edx, 120
	cmp	dl, 56
	je	.L1523
	shr	al, 3
	and	eax, 15
	cmp	al, 4
	je	.L1442
	ja	.L1443
	cmp	al, 1
	ja	.L1524
	mov	rax, rsi
	or	rax, rdi
	jne	.L1456
	mov	BYTE PTR 131[rsp], 48
	lea	rdi, 132[rsp]
	lea	r8, 131[rsp]
.L1457:
	movzx	eax, BYTE PTR [r12]
	mov	rdx, r8
.L1455:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L1525
.L1489:
	cmp	eax, 3
	je	.L1506
.L1490:
	lea	rax, 112[rsp]
	sub	rdi, rdx
	mov	QWORD PTR 120[rsp], rdx
	sub	r8, rdx
	mov	r9, r13
	mov	rdx, rax
	mov	rcx, r12
	mov	QWORD PTR 112[rsp], rdi
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L1441
	.p2align 4,,10
	.p2align 3
.L1523:
	mov	eax, 127
	cmp	rax, rsi
	mov	eax, 0
	sbb	rax, rdi
	jc	.L1440
	lea	rax, 272[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	r9, r12
	mov	edx, 1
	lea	rcx, 112[rsp]
	mov	BYTE PTR 272[rsp], sil
	mov	QWORD PTR 112[rsp], 1
	mov	QWORD PTR 120[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1441:
	add	rsp, 488
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
.L1524:
	lea	rax, .LC15[rip]
	cmp	dl, 16
	lea	rbx, .LC14[rip]
	cmovne	rbx, rax
	mov	rax, rsi
	or	rax, rdi
	je	.L1492
	test	rdi, rdi
	jne	.L1526
	bsr	rax, rsi
	mov	r9d, 128
	mov	edx, 127
	xor	rax, 63
	add	eax, 64
	sub	r9d, eax
	sub	edx, eax
	je	.L1493
.L1451:
	mov	ecx, edx
	sub	edx, 1
	lea	rax, 128[rsp+rcx]
	lea	rcx, 127[rsp+rcx]
	sub	rcx, rdx
	.p2align 4,,10
	.p2align 3
.L1453:
	mov	edx, esi
	sub	rax, 1
	shrd	rsi, rdi, 1
	and	edx, 1
	shr	rdi
	add	edx, 48
	mov	BYTE PTR 4[rax], dl
	cmp	rax, rcx
	jne	.L1453
.L1452:
	lea	r8, 131[rsp]
	movsx	rdi, r9d
	mov	eax, 49
	add	rdi, r8
.L1449:
	mov	BYTE PTR 131[rsp], al
	movzx	eax, BYTE PTR [r12]
	test	al, 16
	je	.L1505
.L1504:
	mov	rdx, -2
	mov	ecx, 2
.L1454:
	add	rdx, r8
	test	ecx, ecx
	mov	r11d, ecx
	je	.L1455
	xor	ecx, ecx
.L1487:
	mov	r9d, ecx
	add	ecx, 1
	movzx	r10d, BYTE PTR [rbx+r9]
	cmp	ecx, r11d
	mov	BYTE PTR [rdx+r9], r10b
	jb	.L1487
	jmp	.L1455
	.p2align 4,,10
	.p2align 3
.L1442:
	mov	rax, rsi
	or	rax, rdi
	je	.L1499
	test	rdi, rdi
	jne	.L1527
	bsr	rax, rsi
	mov	edx, 2863311531
	mov	ecx, 63
	add	eax, 3
	imul	rax, rdx
	shr	rax, 33
	cmp	rcx, rsi
	lea	edx, -1[rax]
	jnb	.L1472
.L1471:
	mov	r9d, 63
	xor	r8d, r8d
	.p2align 4,,10
	.p2align 3
.L1473:
	mov	rcx, rsi
	mov	r10d, edx
	mov	rbx, r8
	and	ecx, 7
	add	ecx, 48
	mov	BYTE PTR 131[rsp+r10], cl
	lea	r10d, -1[rdx]
	mov	rcx, rsi
	shrd	rsi, rdi, 6
	shrd	rcx, rdi, 3
	sub	edx, 2
	shr	rdi, 6
	and	ecx, 7
	add	ecx, 48
	cmp	r9, rsi
	sbb	rbx, rdi
	mov	BYTE PTR 131[rsp+r10], cl
	jc	.L1473
.L1472:
	mov	edx, 7
	cmp	rdx, rsi
	mov	edx, 0
	sbb	rdx, rdi
	jc	.L1528
	add	esi, 48
.L1475:
	lea	r8, 131[rsp]
	mov	edi, eax
	mov	edx, 1
	lea	rbx, .LC16[rip]
	add	rdi, r8
	mov	ecx, 1
	jmp	.L1469
	.p2align 4,,10
	.p2align 3
.L1499:
	mov	esi, 48
	xor	edx, edx
	xor	ebx, ebx
	lea	rdi, 132[rsp]
	xor	ecx, ecx
	lea	r8, 131[rsp]
.L1469:
	mov	BYTE PTR 131[rsp], sil
.L1476:
	movzx	eax, BYTE PTR [r12]
	test	al, 16
	je	.L1505
	test	dl, dl
	jne	.L1529
.L1505:
	shr	al, 2
	mov	rdx, r8
	and	eax, 3
	cmp	eax, 1
	jne	.L1489
.L1525:
	mov	eax, 43
.L1491:
	mov	BYTE PTR -1[rdx], al
	sub	rdx, 1
	jmp	.L1490
	.p2align 4,,10
	.p2align 3
.L1443:
	cmp	dl, 40
	je	.L1530
	mov	rax, rsi
	or	rax, rdi
	jne	.L1501
	cmp	dl, 48
	mov	BYTE PTR 131[rsp], 48
	je	.L1502
	lea	rbx, .LC17[rip]
	lea	rdi, 132[rsp]
	lea	r8, 131[rsp]
	jmp	.L1478
	.p2align 4,,10
	.p2align 3
.L1506:
	mov	eax, 32
	jmp	.L1491
	.p2align 4,,10
	.p2align 3
.L1492:
	lea	rdi, 132[rsp]
	mov	eax, 48
	lea	r8, 131[rsp]
	jmp	.L1449
	.p2align 4,,10
	.p2align 3
.L1456:
	xor	eax, eax
	mov	edx, 9
	cmp	rdx, rsi
	mov	rbx, rax
	sbb	rbx, rdi
	jnc	.L1495
	mov	edx, 99
	mov	rbx, rax
	cmp	rdx, rsi
	sbb	rbx, rdi
	jnc	.L1531
	mov	edx, 999
	mov	rbx, rax
	cmp	rdx, rsi
	sbb	rbx, rdi
	jnc	.L1496
	mov	edx, 9999
	cmp	rdx, rsi
	sbb	rax, rdi
	jnc	.L1497
	mov	ebp, 1
	mov	rdx, rdi
	mov	QWORD PTR 72[rsp], rdi
	mov	r13, r12
	lea	r15, 96[rsp]
	mov	edi, ebp
	mov	rcx, rsi
	mov	QWORD PTR 64[rsp], rsi
	lea	rax, 80[rsp]
	xor	r14d, r14d
	mov	QWORD PTR 576[rsp], r8
	mov	r12, r15
	mov	rbp, rax
	jmp	.L1462
	.p2align 4,,10
	.p2align 3
.L1466:
	mov	eax, 999999
	cmp	rax, r15
	mov	rax, r14
	sbb	rax, rbx
	jnc	.L1532
	mov	eax, 9999999
	cmp	rax, r15
	mov	rax, r14
	sbb	rax, rbx
	jnc	.L1533
	mov	eax, 99999999
	cmp	rax, r15
	mov	rax, r14
	sbb	rax, rbx
	jnc	.L1534
.L1462:
	mov	r15, rcx
	mov	rbx, rdx
	mov	QWORD PTR 96[rsp], rcx
	mov	rcx, r12
	mov	QWORD PTR 104[rsp], rdx
	mov	rdx, rbp
	mov	QWORD PTR 80[rsp], 10000
	mov	QWORD PTR 88[rsp], 0
	call	__udivti3
	mov	eax, 99999
	mov	r9d, edi
	add	edi, 4
	cmp	rax, r15
	mov	rax, r14
	movaps	XMMWORD PTR 48[rsp], xmm0
	mov	rcx, QWORD PTR 48[rsp]
	sbb	rax, rbx
	mov	rdx, QWORD PTR 56[rsp]
	jc	.L1466
	mov	ebp, edi
	mov	r12, r13
	mov	rsi, QWORD PTR 64[rsp]
	mov	rdi, QWORD PTR 72[rsp]
	mov	r13, QWORD PTR 576[rsp]
.L1464:
	cmp	ebp, 128
	ja	.L1498
	lea	ebx, -1[rbp]
.L1461:
	lea	rcx, 272[rsp]
	mov	r8d, 201
	movabs	r15, 1152921504606846975
	lea	rdx, .LC20[rip]
	movabs	r14, -8116567392432202711
	call	memcpy
	mov	QWORD PTR 64[rsp], rbp
	mov	rcx, rax
	mov	QWORD PTR 560[rsp], r12
	.p2align 4,,10
	.p2align 3
.L1467:
	mov	rax, rsi
	mov	r8, rsi
	xor	r9d, r9d
	shrd	rax, rdi, 60
	and	r8, r15
	mov	r12d, 25
	and	rax, r15
	add	r8, rax
	mov	rax, rdi
	shr	rax, 56
	add	r8, rax
	movabs	rax, 5165088340638674453
	mul	r8
	mov	rax, r8
	sub	rax, rdx
	shr	rax
	add	rdx, rax
	shr	rdx, 4
	lea	rax, [rdx+rdx*4]
	mov	rdx, rdi
	lea	rax, [rax+rax*4]
	sub	r8, rax
	mov	rax, rsi
	sub	rax, r8
	sbb	rdx, r9
	mov	rbp, rdx
	movabs	rdx, 2951479051793528258
	imul	rdx, rax
	imul	rbp, r14
	add	rbp, rdx
	mul	r14
	mov	r10, rax
	mov	r11, rdx
	and	eax, 3
	xor	edx, edx
	add	r11, rbp
	imul	rbp, rdx, 25
	mul	r12
	add	rdx, rbp
	add	rax, r8
	mov	r8, rsi
	adc	rdx, r9
	mov	rsi, r10
	mov	r9d, ebx
	shld	rdx, rax, 1
	add	rax, rax
	shrd	rsi, r11, 2
	mov	QWORD PTR 48[rsp], rax
	mov	rax, QWORD PTR 48[rsp]
	mov	QWORD PTR 56[rsp], rdx
	mov	rdx, rdi
	mov	rdi, r11
	shr	rdi, 2
	lea	r10, [rcx+rax]
	add	rax, rcx
	movzx	r10d, BYTE PTR 1[r10]
	movzx	eax, BYTE PTR [rax]
	mov	BYTE PTR 131[rsp+r9], r10b
	lea	r9d, -1[rbx]
	sub	ebx, 2
	mov	BYTE PTR 131[rsp+r9], al
	mov	eax, 9999
	cmp	rax, r8
	mov	eax, 0
	sbb	rax, rdx
	jc	.L1467
	mov	eax, 999
	mov	rbp, QWORD PTR 64[rsp]
	cmp	rax, r8
	mov	eax, 0
	mov	r12, QWORD PTR 560[rsp]
	sbb	rax, rdx
	jnc	.L1458
.L1460:
	add	rsi, rsi
	lea	rax, [rcx+rsi]
	add	rsi, rcx
	movzx	eax, BYTE PTR 1[rax]
	movzx	esi, BYTE PTR [rsi]
	mov	BYTE PTR 132[rsp], al
.L1468:
	lea	r8, 131[rsp]
	mov	BYTE PTR 131[rsp], sil
	lea	rdi, [r8+rbp]
	jmp	.L1457
	.p2align 4,,10
	.p2align 3
.L1530:
	mov	rax, rsi
	or	rax, rdi
	jne	.L1500
	mov	BYTE PTR 131[rsp], 48
	lea	rbx, .LC18[rip]
	lea	rdi, 132[rsp]
	lea	r8, 131[rsp]
	jmp	.L1478
	.p2align 4,,10
	.p2align 3
.L1501:
	lea	rbx, .LC17[rip]
.L1477:
	test	rdi, rdi
	jne	.L1535
	bsr	rax, rsi
	mov	ecx, 255
	lea	ebp, 4[rax]
	movabs	rax, 3978425819141910832
	shr	ebp, 2
	mov	QWORD PTR 272[rsp], rax
	cmp	rcx, rsi
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 280[rsp], rax
	lea	eax, -1[rbp]
	jnb	.L1536
.L1481:
	lea	rcx, 272[rsp]
	mov	r11d, 255
	xor	r10d, r10d
	.p2align 4,,10
	.p2align 3
.L1483:
	mov	r8, rsi
	mov	r14d, eax
	mov	r15, r10
	lea	r9d, -1[rax]
	and	r8d, 15
	sub	eax, 2
	add	r8, rcx
	movzx	r8d, BYTE PTR [r8]
	mov	BYTE PTR 131[rsp+r14], r8b
	mov	r8, rsi
	shrd	rsi, rdi, 8
	shrd	r8, rdi, 4
	shr	rdi, 8
	mov	r14, r8
	and	r14d, 15
	cmp	r11, rsi
	lea	r8, [r14+rcx]
	sbb	r15, rdi
	movzx	r8d, BYTE PTR [r8]
	mov	BYTE PTR 131[rsp+r9], r8b
	jc	.L1483
.L1482:
	mov	eax, 15
	cmp	rax, rsi
	mov	eax, 0
	sbb	rax, rdi
	jc	.L1537
	add	rcx, rsi
	movzx	eax, BYTE PTR [rcx]
.L1485:
	lea	r8, 131[rsp]
	mov	edi, ebp
	mov	BYTE PTR 131[rsp], al
	add	rdi, r8
	cmp	dl, 48
	je	.L1538
.L1478:
	movzx	eax, BYTE PTR [r12]
	test	al, 16
	jne	.L1504
	jmp	.L1505
	.p2align 4,,10
	.p2align 3
.L1537:
	mov	r8, rsi
	shrd	rsi, rdi, 4
	and	r8d, 15
	add	rsi, rcx
	add	r8, rcx
	movzx	eax, BYTE PTR [r8]
	mov	BYTE PTR 132[rsp], al
	movzx	eax, BYTE PTR [rsi]
	jmp	.L1485
	.p2align 4,,10
	.p2align 3
.L1528:
	mov	rcx, rsi
	shrd	rsi, rdi, 3
	and	ecx, 7
	add	esi, 48
	add	ecx, 48
	mov	BYTE PTR 132[rsp], cl
	jmp	.L1475
	.p2align 4,,10
	.p2align 3
.L1500:
	lea	rbx, .LC18[rip]
	jmp	.L1477
	.p2align 4,,10
	.p2align 3
.L1502:
	lea	rdi, 132[rsp]
	lea	rbx, .LC17[rip]
	lea	r8, 131[rsp]
.L1479:
	mov	rsi, r8
	mov	rbp, r8
	.p2align 4,,10
	.p2align 3
.L1486:
	movsx	ecx, BYTE PTR [rsi]
	add	rsi, 1
	call	toupper
	mov	BYTE PTR -1[rsi], al
	cmp	rsi, rdi
	jne	.L1486
	mov	r8, rbp
	mov	edx, 1
	mov	ecx, 2
	jmp	.L1476
	.p2align 4,,10
	.p2align 3
.L1535:
	bsr	rax, rdi
	lea	ebp, 68[rax]
	movabs	rax, 3978425819141910832
	shr	ebp, 2
	mov	QWORD PTR 272[rsp], rax
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 280[rsp], rax
	lea	eax, -1[rbp]
	jmp	.L1481
	.p2align 4,,10
	.p2align 3
.L1526:
	bsr	rax, rdi
	mov	r9d, 128
	mov	edx, 127
	xor	rax, 63
	sub	r9d, eax
	sub	edx, eax
	jmp	.L1451
	.p2align 4,,10
	.p2align 3
.L1529:
	mov	rdx, rcx
	neg	rdx
	jmp	.L1454
.L1493:
	mov	r9d, 1
	jmp	.L1452
.L1495:
	mov	ebp, 1
	.p2align 4,,10
	.p2align 3
.L1458:
	add	esi, 48
	jmp	.L1468
	.p2align 4,,10
	.p2align 3
.L1538:
	test	ebp, ebp
	jne	.L1479
	mov	edx, 1
	mov	ecx, 2
	mov	rdi, r8
	jmp	.L1476
	.p2align 4,,10
	.p2align 3
.L1527:
	bsr	rax, rdi
	mov	edx, 2863311531
	add	eax, 67
	imul	rax, rdx
	shr	rax, 33
	lea	edx, -1[rax]
	jmp	.L1471
	.p2align 4,,10
	.p2align 3
.L1532:
	mov	rsi, QWORD PTR 64[rsp]
	lea	ebp, 5[r9]
	mov	r12, r13
	mov	rdi, QWORD PTR 72[rsp]
	mov	r13, QWORD PTR 576[rsp]
	jmp	.L1464
	.p2align 4,,10
	.p2align 3
.L1533:
	mov	rsi, QWORD PTR 64[rsp]
	lea	ebp, 6[r9]
	mov	r12, r13
	mov	rdi, QWORD PTR 72[rsp]
	mov	r13, QWORD PTR 576[rsp]
	jmp	.L1464
	.p2align 4,,10
	.p2align 3
.L1534:
	mov	rsi, QWORD PTR 64[rsp]
	lea	ebp, 7[r9]
	mov	r12, r13
	mov	rdi, QWORD PTR 72[rsp]
	mov	r13, QWORD PTR 576[rsp]
	jmp	.L1464
	.p2align 4,,10
	.p2align 3
.L1536:
	lea	rcx, 272[rsp]
	jmp	.L1482
.L1498:
	lea	rdi, 259[rsp]
	lea	r8, 131[rsp]
	jmp	.L1457
.L1531:
	lea	rcx, 272[rsp]
	mov	r8d, 201
	mov	ebp, 2
	lea	rdx, .LC20[rip]
	call	memcpy
	mov	rcx, rax
	jmp	.L1460
.L1496:
	mov	ebp, 3
	mov	ebx, 2
	jmp	.L1461
.L1497:
	mov	ebp, 4
	mov	ebx, 3
	jmp	.L1461
.L1440:
	lea	rcx, .LC19[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC23:
	.ascii "basic_string_view::copy\0"
	.align 8
.LC24:
	.ascii "%s: __pos (which is %zu) > __size (which is %zu)\0"
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_:
.LFB5205:
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
	.seh_endprologue
	mov	rdi, QWORD PTR [rcx]
	lea	r12, 16[rcx]
	mov	rbx, rcx
	mov	rbp, rdx
	cmp	rdi, r12
	mov	rsi, r8
	je	.L1556
	mov	rax, QWORD PTR 16[rcx]
.L1540:
	cmp	rax, rbp
	jb	.L1567
.L1541:
	mov	rax, QWORD PTR 8[rsi]
	mov	r13, QWORD PTR 16[rsi]
	mov	r12, QWORD PTR 24[rsi]
	mov	rcx, QWORD PTR [rsi]
	mov	r15, QWORD PTR 8[rax]
	mov	rax, QWORD PTR [rax]
	mov	rbp, QWORD PTR 8[r13]
	mov	r14, QWORD PTR [r12]
	mov	QWORD PTR 56[rsp], rax
	mov	rax, QWORD PTR [rcx]
	add	r14, rbp
.LEHB17:
	call	[QWORD PTR 24[rax]]
.LEHE17:
	mov	r8, QWORD PTR 56[rsp]
	movsx	edx, al
	mov	rcx, rdi
	mov	QWORD PTR 40[rsp], r14
	mov	QWORD PTR 32[rsp], rbp
	mov	r9, r15
	call	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	mov	rdx, QWORD PTR 32[rsi]
	mov	rcx, rax
	mov	rax, QWORD PTR [rdx]
	test	rax, rax
	je	.L1551
	mov	r8, QWORD PTR 40[rsi]
	cmp	QWORD PTR [r8], -1
	je	.L1552
	mov	rax, QWORD PTR 48[rsi]
	add	rcx, 1
	movzx	eax, BYTE PTR [rax]
	mov	BYTE PTR -1[rcx], al
	add	QWORD PTR [r12], 1
	mov	rax, QWORD PTR [rdx]
.L1552:
	cmp	rax, 1
	jbe	.L1551
	mov	rax, QWORD PTR [r12]
	mov	rsi, QWORD PTR 0[r13]
	mov	rdx, QWORD PTR 8[r13]
	cmp	rsi, rax
	jb	.L1568
	sub	rsi, rax
	je	.L1551
	add	rdx, rax
	mov	r8, rsi
	call	memcpy
	mov	rcx, rax
	add	rcx, rsi
.L1551:
	mov	rax, QWORD PTR [rbx]
	sub	rcx, rdi
	mov	QWORD PTR 8[rbx], rcx
	mov	BYTE PTR [rax+rcx], 0
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
.L1567:
	test	rbp, rbp
	js	.L1569
	add	rax, rax
	cmp	rbp, rax
	jb	.L1570
	mov	rcx, rbp
	add	rcx, 1
	js	.L1544
.L1545:
.LEHB18:
	call	_Znwy
	mov	r8, QWORD PTR 8[rbx]
	mov	r13, QWORD PTR [rbx]
	mov	rdi, rax
	cmp	r8, 1
	je	.L1571
	test	r8, r8
	je	.L1566
	mov	rdx, r13
	mov	rcx, rax
	call	memcpy
.L1566:
	cmp	r12, r13
	je	.L1548
	mov	rax, QWORD PTR 16[rbx]
	mov	rcx, r13
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1548:
	mov	QWORD PTR [rbx], rdi
	mov	QWORD PTR 16[rbx], rbp
	jmp	.L1541
	.p2align 4,,10
	.p2align 3
.L1571:
	movzx	eax, BYTE PTR 0[r13]
	mov	BYTE PTR [rdi], al
	jmp	.L1566
	.p2align 4,,10
	.p2align 3
.L1570:
	test	rax, rax
	js	.L1544
	lea	rcx, 1[rax]
	mov	rbp, rax
	jmp	.L1545
	.p2align 4,,10
	.p2align 3
.L1556:
	mov	eax, 15
	jmp	.L1540
	.p2align 4,,10
	.p2align 3
.L1544:
	call	_ZSt17__throw_bad_allocv
.L1569:
	lea	rcx, .LC9[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE18:
.L1568:
	lea	rdx, .LC23[rip]
	mov	r9, rsi
	mov	r8, rax
	lea	rcx, .LC24[rip]
.LEHB19:
	call	_ZSt24__throw_out_of_range_fmtPKcz
.LEHE19:
.L1557:
	mov	rcx, rax
	xor	eax, eax
	mov	QWORD PTR 8[rbx], rax
	mov	rax, QWORD PTR [rbx]
	mov	BYTE PTR [rax], 0
.LEHB20:
	call	_Unwind_Resume
	nop
.LEHE20:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5205:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5205-.LLSDACSB5205
.LLSDACSB5205:
	.uleb128 .LEHB17-.LFB5205
	.uleb128 .LEHE17-.LEHB17
	.uleb128 .L1557-.LFB5205
	.uleb128 0
	.uleb128 .LEHB18-.LFB5205
	.uleb128 .LEHE18-.LEHB18
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB19-.LFB5205
	.uleb128 .LEHE19-.LEHB19
	.uleb128 .L1557-.LFB5205
	.uleb128 0
	.uleb128 .LEHB20-.LFB5205
	.uleb128 .LEHE20-.LEHB20
	.uleb128 0
	.uleb128 0
.LLSDACSE5205:
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_,"x"
	.linkonce discard
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0:
.LFB5276:
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
	sub	rsp, 248
	.seh_stackalloc	248
	.seh_endprologue
	movdqu	xmm0, XMMWORD PTR [rdx]
	lea	rax, 16[rcx]
	mov	BYTE PTR 16[rcx], 0
	mov	rbx, rcx
	mov	edi, r8d
	mov	QWORD PTR [rcx], rax
	mov	rsi, r9
	mov	QWORD PTR 8[rcx], 0
	movaps	XMMWORD PTR 96[rsp], xmm0
.LEHB21:
	call	_ZNSt6locale7classicEv
	mov	rdx, rax
	mov	rcx, rsi
	call	_ZNKSt6localeeqERKS_
	test	al, al
	je	.L1599
.L1572:
	mov	rax, rbx
	add	rsp, 248
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L1599:
	mov	rcx, QWORD PTR .refptr._ZNSt7__cxx118numpunctIcE2idE[rip]
	call	_ZNKSt6locale2id5_M_idEv
	mov	rdx, rax
	mov	rax, QWORD PTR [rsi]
	mov	rax, QWORD PTR 8[rax]
	mov	rsi, QWORD PTR [rax+rdx*8]
	test	rsi, rsi
	je	.L1574
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	call	[QWORD PTR 16[rax]]
	mov	BYTE PTR 119[rsp], al
	mov	rax, QWORD PTR [rsi]
	lea	r12, 144[rsp]
	mov	rdx, rsi
	mov	rcx, r12
	call	[QWORD PTR 32[rax]]
.LEHE21:
	cmp	QWORD PTR 152[rsp], 0
	jne	.L1576
	cmp	BYTE PTR 119[rsp], 46
	je	.L1577
.L1576:
	mov	rbp, QWORD PTR 96[rsp]
	mov	r13, QWORD PTR 104[rsp]
	test	rbp, rbp
	je	.L1600
	mov	edx, 46
	mov	r8, rbp
	mov	rcx, r13
	call	memchr
	movsx	edx, dil
	test	rax, rax
	je	.L1580
	sub	rax, r13
	mov	r8, rbp
	mov	rcx, r13
	mov	rdi, rax
	mov	QWORD PTR 120[rsp], rax
	call	memchr
	test	rax, rax
	je	.L1581
	sub	rax, r13
	cmp	rax, rdi
	jnb	.L1581
.L1586:
	mov	QWORD PTR 128[rsp], rax
	sub	rbp, rax
.L1582:
	lea	r8, 136[rsp]
	mov	QWORD PTR 136[rsp], rbp
	lea	rcx, 120[rsp]
	mov	QWORD PTR 64[rsp], r8
	lea	rdx, 119[rsp]
	mov	QWORD PTR 72[rsp], rcx
	mov	rcx, rbx
	lea	r10, 96[rsp]
	mov	QWORD PTR 80[rsp], rdx
	lea	r9, 128[rsp]
	mov	QWORD PTR 32[rsp], rsi
	lea	rdx, 0[rbp+rax*2]
	mov	QWORD PTR 40[rsp], r12
	lea	r8, 32[rsp]
	mov	QWORD PTR 48[rsp], r10
	mov	QWORD PTR 56[rsp], r9
.LEHB22:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_
.LEHE22:
.L1577:
	mov	rcx, QWORD PTR 144[rsp]
	lea	rax, 160[rsp]
	cmp	rcx, rax
	je	.L1572
	mov	rax, QWORD PTR 160[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L1572
	.p2align 4,,10
	.p2align 3
.L1600:
	mov	QWORD PTR 120[rsp], -1
.L1579:
	mov	QWORD PTR 128[rsp], rbp
	mov	rax, rbp
	xor	ebp, ebp
	jmp	.L1582
	.p2align 4,,10
	.p2align 3
.L1581:
	cmp	rdi, -1
	mov	QWORD PTR 128[rsp], rdi
	je	.L1579
	sub	rbp, rdi
	mov	rax, rdi
	jmp	.L1582
	.p2align 4,,10
	.p2align 3
.L1580:
	mov	QWORD PTR 120[rsp], -1
	mov	r8, rbp
	mov	rcx, r13
	call	memchr
	test	rax, rax
	je	.L1579
	sub	rax, r13
	cmp	rax, -1
	jne	.L1586
	jmp	.L1579
.L1574:
.LEHB23:
	call	_ZSt16__throw_bad_castv
.LEHE23:
.L1587:
	mov	rsi, rax
	jmp	.L1585
.L1588:
	mov	rcx, r12
	mov	rsi, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L1585:
	mov	rcx, rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rsi
.LEHB24:
	call	_Unwind_Resume
	nop
.LEHE24:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5276:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5276-.LLSDACSB5276
.LLSDACSB5276:
	.uleb128 .LEHB21-.LFB5276
	.uleb128 .LEHE21-.LEHB21
	.uleb128 .L1587-.LFB5276
	.uleb128 0
	.uleb128 .LEHB22-.LFB5276
	.uleb128 .LEHE22-.LEHB22
	.uleb128 .L1588-.LFB5276
	.uleb128 0
	.uleb128 .LEHB23-.LFB5276
	.uleb128 .LEHE23-.LEHB23
	.uleb128 .L1587-.LFB5276
	.uleb128 0
	.uleb128 .LEHB24-.LFB5276
	.uleb128 .LEHE24-.LEHB24
	.uleb128 0
	.uleb128 0
.LLSDACSE5276:
	.text
	.seh_endproc
	.section .rdata,"dr"
.LC26:
	.ascii "basic_string::_M_replace\0"
.LC27:
	.ascii "basic_string::_M_replace_aux\0"
.LC28:
	.ascii "basic_string::insert\0"
	.align 8
.LC29:
	.ascii "%s: __pos (which is %zu) > this->size() (which is %zu)\0"
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB4921:
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
	sub	rsp, 424
	.seh_stackalloc	424
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	fld	TBYTE PTR [rdx]
	mov	edx, eax
	mov	rbx, rcx
	mov	r15, r8
	mov	BYTE PTR 208[rsp], 0
	fstp	TBYTE PTR 48[rsp]
	and	edx, 6
	lea	rbp, 208[rsp]
	mov	QWORD PTR 192[rsp], rbp
	mov	QWORD PTR 200[rsp], 0
	jne	.L1840
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L1621
	lea	rdx, .L1745[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L1745:
	.long	.L1621-.L1745
	.long	.L1746-.L1745
	.long	.L1776-.L1745
	.long	.L1777-.L1745
	.long	.L1778-.L1745
	.long	.L1779-.L1745
	.long	.L1780-.L1745
	.long	.L1775-.L1745
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1621:
	fld	TBYTE PTR 48[rsp]
	xor	r13d, r13d
	xor	edi, edi
	xor	r12d, r12d
	lea	rax, 128[rsp]
	lea	r14, 144[rsp]
	mov	r9, rax
	mov	QWORD PTR 80[rsp], rax
	lea	rdx, 289[rsp]
	mov	rcx, r14
	fstp	TBYTE PTR 128[rsp]
	lea	r8, 416[rsp]
	call	_ZSt8to_charsPcS_e
	mov	rsi, QWORD PTR 144[rsp]
	mov	rax, QWORD PTR 152[rsp]
.L1620:
	cmp	eax, 132
	mov	BYTE PTR 72[rsp], 0
	mov	QWORD PTR 64[rsp], 6
	je	.L1774
	lea	rax, 416[rsp]
	mov	QWORD PTR 80[rsp], rax
	lea	r13, 289[rsp]
.L1618:
	test	r12b, r12b
	je	.L1648
	cmp	r13, rsi
	mov	r12, QWORD PTR __imp_toupper[rip]
	mov	r14, r13
	je	.L1650
	.p2align 4,,10
	.p2align 3
.L1649:
	movsx	ecx, BYTE PTR [r14]
	add	r14, 1
	call	r12
	mov	BYTE PTR -1[r14], al
	cmp	rsi, r14
	jne	.L1649
.L1650:
	movsx	ecx, dil
	call	r12
	mov	edi, eax
.L1648:
	fld	TBYTE PTR 48[rsp]
	movzx	r9d, BYTE PTR [rbx]
	fxam
	fnstsw	ax
	fstp	st(0)
	test	ah, 2
	jne	.L1651
	mov	eax, r9d
	and	eax, 12
	cmp	al, 4
	je	.L1841
	cmp	al, 12
	jne	.L1651
	mov	BYTE PTR -1[r13], 32
	movzx	r9d, BYTE PTR [rbx]
	sub	r13, 1
	.p2align 4,,10
	.p2align 3
.L1651:
	mov	r12, rsi
	sub	r12, r13
	test	r9b, 16
	je	.L1653
	fld	TBYTE PTR 48[rsp]
	fabs
	fld	TBYTE PTR .LC25[rip]
	fucomip	st, st(1)
	fstp	st(0)
	jb	.L1653
	test	r12, r12
	je	.L1757
	mov	r8, r12
	mov	edx, 46
	mov	rcx, r13
	mov	BYTE PTR 88[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 88[rsp]
	test	rax, rax
	mov	r14, rax
	je	.L1655
	sub	r14, r13
	cmp	r14, -1
	je	.L1655
	lea	rax, 1[r14]
	mov	QWORD PTR 88[rsp], r12
	cmp	rax, r12
	jnb	.L1656
	mov	r8, r12
	movsx	edx, dil
	mov	BYTE PTR 103[rsp], r9b
	lea	rcx, 0[r13+rax]
	sub	r8, rax
	call	memchr
	movzx	r9d, BYTE PTR 103[rsp]
	test	rax, rax
	je	.L1656
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	mov	QWORD PTR 88[rsp], rax
.L1656:
	cmp	QWORD PTR 88[rsp], r14
	sete	BYTE PTR 103[rsp]
	sete	r14b
	cmp	BYTE PTR 72[rsp], 0
	movzx	r14d, r14b
	jne	.L1657
	mov	QWORD PTR 72[rsp], 0
.L1658:
	test	r14, r14
	je	.L1653
.L1742:
	mov	r9, QWORD PTR 200[rsp]
	lea	rax, [r12+r14]
	mov	QWORD PTR 64[rsp], rax
	test	r9, r9
	jne	.L1660
	mov	rax, QWORD PTR 80[rsp]
	sub	rax, rsi
	cmp	rax, r14
	jnb	.L1842
	cmp	QWORD PTR 192[rsp], rbp
	je	.L1843
	mov	rax, QWORD PTR 208[rsp]
	mov	rsi, QWORD PTR 64[rsp]
	cmp	rax, rsi
	jnb	.L1669
.L1668:
	cmp	QWORD PTR 64[rsp], 0
	js	.L1738
	add	rax, rax
	cmp	QWORD PTR 64[rsp], rax
	jnb	.L1671
	test	rax, rax
	jns	.L1844
.L1672:
	lea	rsi, 192[rsp]
.LEHB25:
	call	_ZSt17__throw_bad_allocv
.L1683:
	mov	rcx, r12
	mov	r14, r12
	add	rcx, 1
	js	.L1690
.L1691:
	lea	rsi, 192[rsp]
	call	_Znwy
.LEHE25:
	cmp	r14, 1
	mov	r10, rax
	je	.L1845
.L1684:
	mov	rcx, r10
	mov	r8, r14
	mov	rdx, r13
	call	memcpy
	mov	rsi, r12
	mov	r12, r14
	mov	r10, rax
.L1692:
	mov	rcx, QWORD PTR 192[rsp]
	cmp	rcx, rbp
	je	.L1693
	mov	rax, QWORD PTR 208[rsp]
	mov	QWORD PTR 64[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 64[rsp]
.L1693:
	mov	QWORD PTR 192[rsp], r10
	mov	QWORD PTR 208[rsp], rsi
.L1688:
	cmp	BYTE PTR 103[rsp], 0
	mov	QWORD PTR 200[rsp], r12
	mov	BYTE PTR [r10+r12], 0
	jne	.L1846
.L1694:
	cmp	QWORD PTR 72[rsp], 0
	mov	r12, QWORD PTR 200[rsp]
	jne	.L1847
.L1696:
	mov	r13, QWORD PTR 192[rsp]
	movzx	r9d, BYTE PTR [rbx]
	.p2align 4,,10
	.p2align 3
.L1653:
	lea	rsi, 240[rsp]
	and	r9d, 32
	mov	QWORD PTR 176[rsp], 0
	mov	BYTE PTR 184[rsp], 0
	mov	QWORD PTR 224[rsp], rsi
	mov	QWORD PTR 232[rsp], 0
	mov	BYTE PTR 240[rsp], 0
	je	.L1767
	cmp	BYTE PTR 32[r15], 0
	lea	rdx, 24[r15]
	je	.L1848
.L1711:
	lea	r14, 168[rsp]
	mov	rcx, r14
	call	_ZNSt6localeC1ERKS_
	lea	rcx, 256[rsp]
	mov	r9, r14
	movsx	r8d, dil
	lea	rdx, 112[rsp]
	mov	QWORD PTR 112[rsp], r12
	mov	QWORD PTR 120[rsp], r13
.LEHB26:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE26:
	mov	rax, QWORD PTR 256[rsp]
	lea	rdi, 272[rsp]
	mov	rcx, QWORD PTR 224[rsp]
	mov	r8, QWORD PTR 264[rsp]
	cmp	rax, rdi
	je	.L1849
	movq	xmm0, r8
	cmp	rcx, rsi
	movhps	xmm0, QWORD PTR 272[rsp]
	je	.L1850
	test	rcx, rcx
	mov	rdx, QWORD PTR 240[rsp]
	mov	QWORD PTR 224[rsp], rax
	movups	XMMWORD PTR 232[rsp], xmm0
	je	.L1719
	mov	QWORD PTR 256[rsp], rcx
	mov	QWORD PTR 272[rsp], rdx
.L1718:
	mov	QWORD PTR 264[rsp], 0
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 256[rsp]
	cmp	rcx, rdi
	je	.L1720
	mov	rax, QWORD PTR 272[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1720:
	mov	rcx, r14
	call	_ZNSt6localeD1Ev
	movzx	eax, WORD PTR [rbx]
	mov	r12, QWORD PTR 232[rsp]
	mov	rdi, QWORD PTR 224[rsp]
	and	ax, 384
	cmp	ax, 128
	je	.L1851
.L1721:
	cmp	ax, 256
	je	.L1723
	mov	r14, QWORD PTR 16[r15]
.L1727:
	lea	rdx, 112[rsp]
	mov	rcx, r14
	mov	QWORD PTR 112[rsp], r12
	mov	QWORD PTR 120[rsp], rdi
.LEHB27:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L1836:
	mov	rcx, QWORD PTR 224[rsp]
	mov	rbx, rax
	cmp	rcx, rsi
	je	.L1731
	mov	rax, QWORD PTR 240[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1731:
	cmp	BYTE PTR 184[rsp], 0
	jne	.L1852
.L1732:
	mov	rcx, QWORD PTR 192[rsp]
	cmp	rcx, rbp
	je	.L1796
	mov	rax, QWORD PTR 208[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1796:
	mov	rax, rbx
	add	rsp, 424
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
.L1767:
	movzx	eax, WORD PTR [rbx]
	mov	rdi, r13
	and	ax, 384
	cmp	ax, 128
	jne	.L1721
.L1851:
	movzx	eax, WORD PTR 4[rbx]
.L1722:
	cmp	r12, rax
	mov	r14, QWORD PTR 16[r15]
	jnb	.L1727
	movzx	edx, BYTE PTR [rbx]
	sub	rax, r12
	movzx	ecx, BYTE PTR 8[rbx]
	mov	rbx, rax
	mov	r8d, edx
	and	r8d, 3
	movsx	eax, cl
	jne	.L1729
	and	edx, 64
	je	.L1769
	fld	TBYTE PTR 48[rsp]
	fabs
	fld	TBYTE PTR .LC25[rip]
	fucomip	st, st(1)
	fstp	st(0)
	jnb	.L1853
.L1769:
	mov	eax, 32
	mov	r8d, 2
.L1729:
	lea	rdx, 112[rsp]
	mov	DWORD PTR 32[rsp], eax
	mov	r9, rbx
	mov	rcx, r14
	mov	QWORD PTR 112[rsp], r12
	mov	QWORD PTR 120[rsp], rdi
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
.LEHE27:
	jmp	.L1836
	.p2align 4,,10
	.p2align 3
.L1840:
	cmp	dl, 2
	je	.L1854
	mov	QWORD PTR 64[rsp], -1
	cmp	dl, 4
	je	.L1855
.L1604:
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L1607
	lea	rdx, .L1609[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L1609:
	.long	.L1616-.L1609
	.long	.L1748-.L1609
	.long	.L1614-.L1609
	.long	.L1613-.L1609
	.long	.L1830-.L1609
	.long	.L1832-.L1609
	.long	.L1610-.L1609
	.long	.L1831-.L1609
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1852:
	lea	rcx, 176[rsp]
	call	_ZNSt6localeD1Ev
	jmp	.L1732
	.p2align 4,,10
	.p2align 3
.L1776:
	mov	r12d, 1
.L1619:
	fld	TBYTE PTR 48[rsp]
	mov	DWORD PTR 32[rsp], 4
	mov	r13d, 4
	mov	edi, 112
	lea	rax, 128[rsp]
	lea	r14, 144[rsp]
	mov	r9, rax
	mov	QWORD PTR 80[rsp], rax
	lea	rdx, 289[rsp]
	mov	rcx, r14
	fstp	TBYTE PTR 128[rsp]
	lea	r8, 416[rsp]
	call	_ZSt8to_charsPcS_eSt12chars_format
	mov	rsi, QWORD PTR 144[rsp]
	mov	rax, QWORD PTR 152[rsp]
	jmp	.L1620
	.p2align 4,,10
	.p2align 3
.L1853:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	eax, 48
	mov	r8d, 2
	cmp	BYTE PTR [rcx+rdx], 15
	jbe	.L1729
	mov	rax, QWORD PTR 24[r14]
	movzx	edx, BYTE PTR [rdi]
	lea	rcx, 1[rax]
	mov	QWORD PTR 24[r14], rcx
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[r14]
	sub	rax, QWORD PTR 8[r14]
	cmp	rax, QWORD PTR 16[r14]
	je	.L1856
.L1730:
	add	rdi, 1
	sub	r12, 1
	mov	eax, 48
	mov	r8d, 2
	jmp	.L1729
	.p2align 4,,10
	.p2align 3
.L1757:
	xor	eax, eax
.L1654:
	cmp	BYTE PTR 72[rsp], 0
	je	.L1857
	movzx	edx, BYTE PTR 72[rsp]
	mov	QWORD PTR 88[rsp], rax
	mov	r14d, 1
	mov	BYTE PTR 103[rsp], dl
	jmp	.L1741
	.p2align 4,,10
	.p2align 3
.L1777:
	mov	QWORD PTR 64[rsp], 6
.L1613:
	xor	r12d, r12d
.L1612:
	mov	r13d, 1
	mov	edi, 101
	mov	BYTE PTR 72[rsp], 0
.L1615:
	mov	esi, DWORD PTR 64[rsp]
	lea	rax, 128[rsp]
	mov	DWORD PTR 32[rsp], r13d
	fld	TBYTE PTR 48[rsp]
	mov	r9, rax
	mov	QWORD PTR 80[rsp], rax
	lea	r14, 144[rsp]
	lea	rax, 289[rsp]
	mov	DWORD PTR 40[rsp], esi
	mov	rcx, r14
	lea	r8, 416[rsp]
	mov	rdx, rax
	mov	QWORD PTR 88[rsp], rax
	fstp	TBYTE PTR 128[rsp]
	call	_ZSt8to_charsPcS_eSt12chars_formati
	mov	rsi, QWORD PTR 144[rsp]
	cmp	DWORD PTR 152[rsp], 132
	je	.L1617
	lea	rax, 416[rsp]
	mov	r13, QWORD PTR 88[rsp]
	mov	QWORD PTR 80[rsp], rax
	jmp	.L1618
	.p2align 4,,10
	.p2align 3
.L1778:
	mov	QWORD PTR 64[rsp], 6
.L1830:
	mov	r12d, 1
	jmp	.L1612
	.p2align 4,,10
	.p2align 3
.L1779:
	mov	QWORD PTR 64[rsp], 6
.L1832:
	mov	r13d, 2
	xor	edi, edi
	mov	BYTE PTR 72[rsp], 0
	xor	r12d, r12d
	jmp	.L1615
	.p2align 4,,10
	.p2align 3
.L1775:
	mov	QWORD PTR 64[rsp], 6
.L1831:
	mov	r12d, 1
.L1608:
	mov	r13d, 3
	mov	edi, 101
	mov	BYTE PTR 72[rsp], 1
	jmp	.L1615
	.p2align 4,,10
	.p2align 3
.L1780:
	mov	QWORD PTR 64[rsp], 6
.L1610:
	xor	r12d, r12d
	jmp	.L1608
	.p2align 4,,10
	.p2align 3
.L1746:
	xor	r12d, r12d
	jmp	.L1619
	.p2align 4,,10
	.p2align 3
.L1855:
	movzx	edx, BYTE PTR [r8]
	mov	BYTE PTR 240[rsp], 0
	movzx	eax, WORD PTR 6[rcx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L1858
	test	cl, cl
	jne	.L1606
	mov	rdx, QWORD PTR [r8]
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L1606
	sal	rax, 5
	add	rax, QWORD PTR 8[r8]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 224[rsp], rdx
	mov	rdx, QWORD PTR 8[rax]
	mov	QWORD PTR 232[rsp], rdx
	movzx	eax, BYTE PTR 16[rax]
	mov	BYTE PTR 240[rsp], al
	.p2align 4,,10
	.p2align 3
.L1606:
	lea	rcx, 224[rsp]
	lea	rsi, 192[rsp]
.LEHB28:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE28:
	mov	QWORD PTR 64[rsp], rax
	movzx	eax, BYTE PTR 1[rbx]
	jmp	.L1604
	.p2align 4,,10
	.p2align 3
.L1841:
	mov	BYTE PTR -1[r13], 43
	sub	r13, 1
	movzx	r9d, BYTE PTR [rbx]
	jmp	.L1651
	.p2align 4,,10
	.p2align 3
.L1848:
	mov	rcx, rdx
	mov	QWORD PTR 64[rsp], rdx
	call	_ZNSt6localeC1Ev
	mov	rdx, QWORD PTR 64[rsp]
	mov	BYTE PTR 32[r15], 1
	jmp	.L1711
	.p2align 4,,10
	.p2align 3
.L1723:
	movzx	edx, BYTE PTR [r15]
	mov	BYTE PTR 272[rsp], 0
	movzx	eax, WORD PTR 4[rbx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L1859
	test	cl, cl
	jne	.L1726
	mov	rdx, QWORD PTR [r15]
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L1726
	sal	rax, 5
	add	rax, QWORD PTR 8[r15]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 256[rsp], rdx
	mov	rdx, QWORD PTR 8[rax]
	mov	QWORD PTR 264[rsp], rdx
	movzx	eax, BYTE PTR 16[rax]
	mov	BYTE PTR 272[rsp], al
	.p2align 4,,10
	.p2align 3
.L1726:
	lea	rcx, 256[rsp]
.LEHB29:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE29:
	jmp	.L1722
	.p2align 4,,10
	.p2align 3
.L1850:
	mov	QWORD PTR 224[rsp], rax
	movups	XMMWORD PTR 232[rsp], xmm0
.L1719:
	mov	QWORD PTR 256[rsp], rdi
	lea	rdi, 272[rsp]
	mov	rcx, rdi
	jmp	.L1718
	.p2align 4,,10
	.p2align 3
.L1854:
	movzx	edi, WORD PTR 6[rcx]
	mov	QWORD PTR 64[rsp], rdi
	jmp	.L1604
	.p2align 4,,10
	.p2align 3
.L1849:
	test	r8, r8
	je	.L1714
	cmp	r8, 1
	je	.L1860
	mov	rdx, rdi
	call	memcpy
	mov	r8, QWORD PTR 264[rsp]
	mov	rcx, QWORD PTR 224[rsp]
.L1714:
	mov	QWORD PTR 232[rsp], r8
	mov	BYTE PTR [rcx+r8], 0
	mov	rcx, QWORD PTR 256[rsp]
	jmp	.L1718
	.p2align 4,,10
	.p2align 3
.L1657:
	mov	rax, QWORD PTR 88[rsp]
	sub	rax, 1
.L1741:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	cmp	BYTE PTR [rcx+rdx], 16
	mov	rdx, QWORD PTR 64[rsp]
	adc	rax, -1
	sub	rdx, rax
	mov	QWORD PTR 72[rsp], rdx
	add	r14, rdx
	jmp	.L1658
	.p2align 4,,10
	.p2align 3
.L1774:
	mov	BYTE PTR 103[rsp], 0
	mov	QWORD PTR 88[rsp], 134
.L1622:
	mov	r10, QWORD PTR 192[rsp]
	cmp	r10, rbp
	je	.L1754
	mov	rax, QWORD PTR 208[rsp]
.L1624:
	mov	rsi, QWORD PTR 88[rsp]
	cmp	rax, rsi
	jb	.L1861
.L1647:
	cmp	r10, rbp
	je	.L1755
	mov	rax, QWORD PTR 208[rsp]
	lea	rsi, [rax+rax]
	cmp	rax, rsi
	mov	QWORD PTR 88[rsp], rsi
	jb	.L1862
.L1636:
	mov	rax, QWORD PTR 88[rsp]
	lea	rdx, 1[r10]
	mov	QWORD PTR 88[rsp], r10
	cmp	BYTE PTR 103[rsp], 0
	fld	TBYTE PTR 48[rsp]
	lea	r8, -1[r10+rax]
	fstp	TBYTE PTR 128[rsp]
	jne	.L1863
	test	r13d, r13d
	jne	.L1864
	mov	r9, QWORD PTR 80[rsp]
	mov	rcx, r14
	call	_ZSt8to_charsPcS_e
	mov	rsi, QWORD PTR 144[rsp]
	mov	rax, QWORD PTR 152[rsp]
	mov	r10, QWORD PTR 88[rsp]
.L1644:
	test	eax, eax
	jne	.L1646
	mov	rdx, QWORD PTR 192[rsp]
	mov	rax, rsi
	sub	rax, r10
	mov	QWORD PTR 200[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rax, QWORD PTR 192[rsp]
	lea	r13, 1[rax]
	add	rax, QWORD PTR 200[rsp]
	mov	QWORD PTR 80[rsp], rax
	jmp	.L1618
	.p2align 4,,10
	.p2align 3
.L1655:
	movsx	edx, dil
	mov	r8, r12
	mov	rcx, r13
	mov	BYTE PTR 88[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 88[rsp]
	test	rax, rax
	je	.L1761
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	jmp	.L1654
.L1748:
	mov	r13d, 4
	mov	edi, 112
	mov	BYTE PTR 72[rsp], 0
	xor	r12d, r12d
	jmp	.L1615
.L1614:
	mov	r13d, 4
	mov	edi, 112
	mov	BYTE PTR 72[rsp], 0
	mov	r12d, 1
	jmp	.L1615
.L1616:
	mov	r13d, 3
	xor	edi, edi
	mov	BYTE PTR 72[rsp], 0
	xor	r12d, r12d
	jmp	.L1615
.L1857:
	mov	QWORD PTR 88[rsp], rax
	mov	r14d, 1
	mov	QWORD PTR 72[rsp], 0
	mov	BYTE PTR 103[rsp], 1
	jmp	.L1742
.L1864:
	mov	r9, QWORD PTR 80[rsp]
	mov	DWORD PTR 32[rsp], r13d
	mov	rcx, r14
	call	_ZSt8to_charsPcS_eSt12chars_format
	mov	rsi, QWORD PTR 144[rsp]
	mov	rax, QWORD PTR 152[rsp]
	mov	r10, QWORD PTR 88[rsp]
	jmp	.L1644
.L1858:
	mov	rdx, QWORD PTR [r8]
	lea	rcx, [rax+rax*4]
	sal	rax, 4
	add	rax, QWORD PTR 8[r8]
	shr	rdx, 4
	shr	rdx, cl
	and	edx, 31
	mov	BYTE PTR 240[rsp], dl
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 224[rsp], rdx
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR 232[rsp], rax
	jmp	.L1606
.L1761:
	mov	rax, r12
	jmp	.L1654
.L1843:
	mov	rax, QWORD PTR 64[rsp]
	cmp	rax, 15
	ja	.L1839
	mov	rax, QWORD PTR 88[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L1676
	mov	r10, rbp
.L1743:
	cmp	r12, 15
	ja	.L1865
.L1682:
	cmp	r13, r10
	jb	.L1686
	cmp	r10, r13
	jb	.L1686
	xor	eax, eax
	mov	QWORD PTR 32[rsp], r12
	mov	r9, r13
	xor	r8d, r8d
	lea	rsi, 192[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	rdx, r10
	mov	rcx, rsi
.LEHB30:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	r10, QWORD PTR 192[rsp]
	jmp	.L1688
	.p2align 4,,10
	.p2align 3
.L1646:
	mov	rdx, QWORD PTR 192[rsp]
	cmp	eax, 132
	mov	QWORD PTR 200[rsp], 0
	mov	BYTE PTR [rdx], 0
	mov	r10, QWORD PTR 192[rsp]
	mov	rdx, QWORD PTR 200[rsp]
	je	.L1647
	lea	rax, [r10+rdx]
	lea	r13, 1[r10]
	mov	QWORD PTR 80[rsp], rax
	jmp	.L1618
	.p2align 4,,10
	.p2align 3
.L1861:
	test	rsi, rsi
	js	.L1866
	add	rax, rax
	cmp	QWORD PTR 88[rsp], rax
	jnb	.L1627
	test	rax, rax
	js	.L1628
	lea	rcx, 1[rax]
	mov	QWORD PTR 88[rsp], rax
.L1629:
	lea	rsi, 192[rsp]
	call	_Znwy
	mov	r10, rax
	mov	rax, QWORD PTR 200[rsp]
	mov	rsi, QWORD PTR 192[rsp]
	lea	r8, 1[rax]
	test	rax, rax
	je	.L1867
	test	r8, r8
	je	.L1833
	mov	rcx, r10
	mov	rdx, rsi
	call	memcpy
	mov	r10, rax
.L1833:
	cmp	rsi, rbp
	je	.L1632
	mov	rax, QWORD PTR 208[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 104[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 104[rsp]
.L1632:
	mov	rax, QWORD PTR 88[rsp]
	mov	QWORD PTR 192[rsp], r10
	mov	QWORD PTR 208[rsp], rax
	jmp	.L1647
.L1859:
	mov	rdx, QWORD PTR [r15]
	lea	rcx, [rax+rax*4]
	sal	rax, 4
	add	rax, QWORD PTR 8[r15]
	shr	rdx, 4
	shr	rdx, cl
	and	edx, 31
	mov	BYTE PTR 272[rsp], dl
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 256[rsp], rdx
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR 264[rsp], rax
	jmp	.L1726
.L1660:
	cmp	QWORD PTR 192[rsp], rbp
	je	.L1666
	mov	rax, QWORD PTR 208[rsp]
	mov	rsi, QWORD PTR 64[rsp]
	cmp	rax, rsi
	jb	.L1668
.L1667:
	mov	rax, QWORD PTR 88[rsp]
	cmp	r9, rax
	jb	.L1868
.L1679:
	movabs	rax, 9223372036854775807
	sub	rax, r9
	cmp	rax, r14
	jb	.L1869
	mov	rax, QWORD PTR 192[rsp]
	lea	r12, [r9+r14]
	cmp	rax, rbp
	je	.L1766
	mov	rdx, QWORD PTR 208[rsp]
.L1703:
	cmp	rdx, r12
	jb	.L1704
	mov	rsi, QWORD PTR 88[rsp]
	lea	rcx, [rax+rsi]
	sub	r9, rsi
	je	.L1705
	lea	rax, [rcx+r14]
	cmp	r9, 1
	je	.L1870
	mov	rdx, rcx
	mov	r8, r9
	mov	rcx, rax
	call	memmove
	mov	rcx, QWORD PTR 88[rsp]
	add	rcx, QWORD PTR 192[rsp]
.L1705:
	cmp	r14, 1
	je	.L1871
	mov	r8, r14
	mov	edx, 48
	call	memset
.L1708:
	mov	rax, QWORD PTR 192[rsp]
	mov	QWORD PTR 200[rsp], r12
	cmp	BYTE PTR 103[rsp], 0
	mov	BYTE PTR [rax+r12], 0
	mov	r12, QWORD PTR 200[rsp]
	je	.L1696
	mov	rax, QWORD PTR 192[rsp]
	mov	rsi, QWORD PTR 88[rsp]
	mov	BYTE PTR [rax+rsi], 46
	mov	r12, QWORD PTR 200[rsp]
	jmp	.L1696
.L1671:
	mov	rcx, QWORD PTR 64[rsp]
	add	rcx, 1
	js	.L1672
.L1673:
	lea	rsi, 192[rsp]
	call	_Znwy
	mov	r9, QWORD PTR 200[rsp]
	mov	rsi, rax
	mov	r10, QWORD PTR 192[rsp]
	lea	r8, 1[r9]
	test	r9, r9
	je	.L1872
	test	r8, r8
	jne	.L1678
	cmp	r10, rbp
	je	.L1873
.L1675:
	mov	rax, QWORD PTR 208[rsp]
	mov	rcx, r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 200[rsp]
	mov	QWORD PTR 192[rsp], rsi
	mov	rax, QWORD PTR 64[rsp]
	test	r9, r9
	mov	QWORD PTR 208[rsp], rax
	jne	.L1667
.L1669:
	mov	rax, QWORD PTR 88[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L1676
	mov	r10, QWORD PTR 192[rsp]
	cmp	r10, rbp
	je	.L1743
.L1681:
	mov	rax, QWORD PTR 208[rsp]
	cmp	rax, r12
	jnb	.L1682
	add	rax, rax
	cmp	r12, rax
	jnb	.L1683
	lea	rcx, 1[rax]
	test	rax, rax
	mov	r14, r12
	mov	r12, rax
	jns	.L1691
.L1690:
	lea	rsi, 192[rsp]
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L1627:
	mov	rcx, QWORD PTR 88[rsp]
	add	rcx, 1
	jns	.L1629
.L1628:
	lea	rsi, 192[rsp]
	call	_ZSt17__throw_bad_allocv
.L1863:
	mov	eax, DWORD PTR 64[rsp]
	mov	DWORD PTR 32[rsp], r13d
	mov	rcx, r14
	mov	r9, QWORD PTR 80[rsp]
	mov	DWORD PTR 40[rsp], eax
	call	_ZSt8to_charsPcS_eSt12chars_formati
	mov	rsi, QWORD PTR 144[rsp]
	mov	rax, QWORD PTR 152[rsp]
	mov	r10, QWORD PTR 88[rsp]
	jmp	.L1644
.L1617:
	mov	rax, QWORD PTR 64[rsp]
	cmp	r13d, 2
	mov	BYTE PTR 103[rsp], 1
	lea	rsi, 128[rax]
	mov	QWORD PTR 88[rsp], rsi
	jne	.L1622
	fld	TBYTE PTR 48[rsp]
	pxor	xmm0, xmm0
	fisttp	DWORD PTR 88[rsp]
	mov	eax, DWORD PTR 88[rsp]
	cdq
	xor	eax, edx
	sub	eax, edx
	cvtsi2sd	xmm0, eax
	call	log10
	cvttsd2si	edx, xmm0
	mov	eax, edx
	sar	eax
	cmp	edx, 1
	mov	edx, 1
	cdqe
	cmovle	rax, rdx
	add	rsi, rax
	mov	QWORD PTR 88[rsp], rsi
	jmp	.L1622
.L1686:
	test	r12, r12
	je	.L1688
	cmp	r12, 1
	je	.L1874
	mov	rcx, r10
	mov	r8, r12
	mov	rdx, r13
	call	memcpy
	mov	r10, QWORD PTR 192[rsp]
	jmp	.L1688
.L1842:
	mov	rax, QWORD PTR 88[rsp]
	mov	r8, r12
	lea	rsi, 0[r13+rax]
	sub	r8, rax
	lea	rcx, [rax+r14]
	mov	rdx, rsi
	add	rcx, r13
	call	memmove
	cmp	BYTE PTR 103[rsp], 0
	je	.L1663
	mov	rax, QWORD PTR 88[rsp]
	mov	BYTE PTR [rsi], 46
	lea	rsi, 1[r13+rax]
.L1663:
	mov	r8, QWORD PTR 72[rsp]
	mov	edx, 48
	mov	rcx, rsi
	call	memset
	movzx	r9d, BYTE PTR [rbx]
	mov	r12, QWORD PTR 64[rsp]
	jmp	.L1653
.L1755:
	mov	QWORD PTR 88[rsp], 30
	mov	ecx, 31
.L1635:
	lea	rsi, 192[rsp]
	call	_Znwy
	mov	r8, QWORD PTR 200[rsp]
	mov	r10, rax
	mov	rsi, QWORD PTR 192[rsp]
	cmp	r8, 1
	je	.L1875
	test	r8, r8
	je	.L1835
	mov	rdx, rsi
	mov	rcx, rax
	call	memcpy
	mov	r10, rax
.L1835:
	cmp	rsi, rbp
	je	.L1640
	mov	rax, QWORD PTR 208[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 104[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 104[rsp]
.L1640:
	mov	rax, QWORD PTR 88[rsp]
	mov	QWORD PTR 192[rsp], r10
	mov	QWORD PTR 208[rsp], rax
	jmp	.L1636
.L1754:
	mov	eax, 15
	jmp	.L1624
.L1862:
	test	rsi, rsi
	js	.L1637
	lea	rcx, 1[rsi]
	jmp	.L1635
.L1704:
	mov	r13, QWORD PTR 88[rsp]
	mov	QWORD PTR 32[rsp], r14
	xor	r9d, r9d
	xor	r8d, r8d
	lea	rsi, 192[rsp]
	mov	rcx, rsi
	mov	rdx, r13
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rcx, QWORD PTR 192[rsp]
	add	rcx, r13
	jmp	.L1705
.L1867:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r10], al
	jmp	.L1833
.L1872:
	movzx	eax, BYTE PTR [r10]
	cmp	r10, rbp
	mov	BYTE PTR [rsi], al
	jne	.L1675
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 192[rsp], rsi
	mov	QWORD PTR 208[rsp], rax
	mov	rax, QWORD PTR 88[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L1676
	mov	r10, rsi
	jmp	.L1681
.L1847:
	movabs	rax, 9223372036854775807
	mov	rsi, QWORD PTR 72[rsp]
	sub	rax, r12
	cmp	rax, rsi
	jb	.L1876
	mov	rax, QWORD PTR 72[rsp]
	lea	r13, [r12+rax]
	mov	rax, QWORD PTR 192[rsp]
	cmp	rax, rbp
	je	.L1765
	mov	rdx, QWORD PTR 208[rsp]
.L1698:
	cmp	rdx, r13
	jb	.L1877
.L1699:
	cmp	QWORD PTR 72[rsp], 1
	lea	rcx, [rax+r12]
	je	.L1878
	mov	r8, QWORD PTR 72[rsp]
	mov	edx, 48
	call	memset
.L1701:
	mov	rax, QWORD PTR 192[rsp]
	mov	QWORD PTR 200[rsp], r13
	mov	BYTE PTR [rax+r13], 0
	mov	r12, QWORD PTR 200[rsp]
	jmp	.L1696
.L1678:
	mov	rdx, r10
	mov	rcx, rax
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 80[rsp], r10
	call	memcpy
	mov	r10, QWORD PTR 80[rsp]
	mov	r9, QWORD PTR 104[rsp]
	cmp	r10, rbp
	jne	.L1675
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 192[rsp], rsi
	mov	QWORD PTR 208[rsp], rax
	jmp	.L1667
.L1860:
	movzx	eax, BYTE PTR 272[rsp]
	mov	BYTE PTR [rcx], al
	mov	r8, QWORD PTR 264[rsp]
	mov	rcx, QWORD PTR 224[rsp]
	jmp	.L1714
.L1875:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r10], al
	jmp	.L1835
.L1846:
	lea	rsi, 192[rsp]
	mov	edx, 46
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	jmp	.L1694
.L1666:
	mov	rax, QWORD PTR 64[rsp]
	cmp	rax, 15
	jbe	.L1667
.L1839:
	test	rax, rax
	js	.L1738
	cmp	rax, 29
	ja	.L1671
	mov	QWORD PTR 64[rsp], 30
.L1739:
	mov	rax, QWORD PTR 64[rsp]
	lea	rcx, 1[rax]
	jmp	.L1673
.L1766:
	mov	edx, 15
	jmp	.L1703
.L1871:
	mov	BYTE PTR [rcx], 48
	jmp	.L1708
.L1870:
	movzx	edx, BYTE PTR [rcx]
	mov	BYTE PTR [rax], dl
	mov	rcx, QWORD PTR 192[rsp]
	add	rcx, rsi
	jmp	.L1705
.L1874:
	movzx	eax, BYTE PTR 0[r13]
	mov	BYTE PTR [r10], al
	mov	r10, QWORD PTR 192[rsp]
	jmp	.L1688
.L1877:
	mov	rax, QWORD PTR 72[rsp]
	xor	r9d, r9d
	xor	r8d, r8d
	mov	rdx, r12
	lea	rsi, 192[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 32[rsp], rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE30:
	mov	rax, QWORD PTR 192[rsp]
	jmp	.L1699
.L1856:
	mov	rax, QWORD PTR [r14]
	mov	rcx, r14
.LEHB31:
	call	[QWORD PTR [rax]]
.LEHE31:
	jmp	.L1730
.L1865:
	cmp	r12, 29
	ja	.L1683
	lea	rsi, 192[rsp]
	mov	ecx, 31
.LEHB32:
	call	_Znwy
	mov	r14, r12
	mov	r10, rax
	mov	r12d, 30
	jmp	.L1684
.L1878:
	mov	BYTE PTR [rcx], 48
	jmp	.L1701
.L1765:
	mov	edx, 15
	jmp	.L1698
.L1873:
	mov	QWORD PTR 192[rsp], rax
	mov	rax, QWORD PTR 64[rsp]
	mov	r9, -1
	mov	QWORD PTR 208[rsp], rax
	jmp	.L1679
.L1845:
	movzx	eax, BYTE PTR 0[r13]
	mov	rsi, r12
	mov	r12d, 1
	mov	BYTE PTR [r10], al
	jmp	.L1692
.L1844:
	mov	QWORD PTR 64[rsp], rax
	jmp	.L1739
.L1866:
	lea	rcx, .LC9[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1637:
	lea	rcx, .LC9[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1738:
	lea	rcx, .LC9[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1869:
	lea	rcx, .LC27[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1868:
	lea	rdx, .LC28[rip]
	mov	r8, rax
	lea	rcx, .LC29[rip]
	lea	rsi, 192[rsp]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L1676:
	lea	rcx, .LC26[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1876:
	lea	rcx, .LC27[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.LEHE32:
.L1607:
	xor	r13d, r13d
	xor	edi, edi
	mov	BYTE PTR 72[rsp], 0
	xor	r12d, r12d
	jmp	.L1615
.L1781:
	mov	rbx, rax
.L1737:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB33:
	call	_Unwind_Resume
.LEHE33:
.L1783:
	mov	rbx, rax
	jmp	.L1735
.L1782:
	mov	rcx, r14
	mov	rbx, rax
	call	_ZNSt6localeD1Ev
.L1735:
	lea	rcx, 224[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	cmp	BYTE PTR 184[rsp], 0
	je	.L1736
	lea	rcx, 176[rsp]
	call	_ZNSt6localeD1Ev
.L1736:
	lea	rsi, 192[rsp]
	jmp	.L1737
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4921:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4921-.LLSDACSB4921
.LLSDACSB4921:
	.uleb128 .LEHB25-.LFB4921
	.uleb128 .LEHE25-.LEHB25
	.uleb128 .L1781-.LFB4921
	.uleb128 0
	.uleb128 .LEHB26-.LFB4921
	.uleb128 .LEHE26-.LEHB26
	.uleb128 .L1782-.LFB4921
	.uleb128 0
	.uleb128 .LEHB27-.LFB4921
	.uleb128 .LEHE27-.LEHB27
	.uleb128 .L1783-.LFB4921
	.uleb128 0
	.uleb128 .LEHB28-.LFB4921
	.uleb128 .LEHE28-.LEHB28
	.uleb128 .L1781-.LFB4921
	.uleb128 0
	.uleb128 .LEHB29-.LFB4921
	.uleb128 .LEHE29-.LEHB29
	.uleb128 .L1783-.LFB4921
	.uleb128 0
	.uleb128 .LEHB30-.LFB4921
	.uleb128 .LEHE30-.LEHB30
	.uleb128 .L1781-.LFB4921
	.uleb128 0
	.uleb128 .LEHB31-.LFB4921
	.uleb128 .LEHE31-.LEHB31
	.uleb128 .L1783-.LFB4921
	.uleb128 0
	.uleb128 .LEHB32-.LFB4921
	.uleb128 .LEHE32-.LEHB32
	.uleb128 .L1781-.LFB4921
	.uleb128 0
	.uleb128 .LEHB33-.LFB4921
	.uleb128 .LEHE33-.LEHB33
	.uleb128 0
	.uleb128 0
.LLSDACSE4921:
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB4918:
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
	sub	rsp, 408
	.seh_stackalloc	408
	movaps	XMMWORD PTR 384[rsp], xmm6
	.seh_savexmm	xmm6, 384
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	edx, eax
	mov	rbx, rcx
	movapd	xmm6, xmm1
	mov	QWORD PTR 496[rsp], r8
	lea	rbp, 176[rsp]
	and	edx, 6
	mov	QWORD PTR 168[rsp], 0
	mov	QWORD PTR 160[rsp], rbp
	mov	BYTE PTR 176[rsp], 0
	jne	.L2118
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L1899
	lea	rdx, .L2023[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2023:
	.long	.L1899-.L2023
	.long	.L2024-.L2023
	.long	.L2054-.L2023
	.long	.L2055-.L2023
	.long	.L2056-.L2023
	.long	.L2057-.L2023
	.long	.L2058-.L2023
	.long	.L2053-.L2023
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1899:
	lea	r13, 112[rsp]
	movapd	xmm3, xmm6
	xor	r14d, r14d
	lea	rdx, 257[rsp]
	mov	rcx, r13
	xor	edi, edi
	lea	r8, 384[rsp]
	xor	r12d, r12d
	call	_ZSt8to_charsPcS_d
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
.L1898:
	mov	QWORD PTR 56[rsp], 6
	xor	r15d, r15d
	cmp	eax, 132
	je	.L2052
	lea	rax, 384[rsp]
	mov	QWORD PTR 64[rsp], rax
	lea	r13, 257[rsp]
.L1896:
	test	r12b, r12b
	je	.L1926
	cmp	r13, rsi
	mov	r12, QWORD PTR __imp_toupper[rip]
	mov	r14, r13
	je	.L1928
	.p2align 4,,10
	.p2align 3
.L1927:
	movsx	ecx, BYTE PTR [r14]
	add	r14, 1
	call	r12
	mov	BYTE PTR -1[r14], al
	cmp	rsi, r14
	jne	.L1927
.L1928:
	movsx	ecx, dil
	call	r12
	mov	edi, eax
.L1926:
	movmskpd	eax, xmm6
	movzx	r9d, BYTE PTR [rbx]
	test	al, 1
	jne	.L1929
	mov	eax, r9d
	and	eax, 12
	cmp	al, 4
	je	.L2119
	cmp	al, 12
	jne	.L1929
	mov	BYTE PTR -1[r13], 32
	movzx	r9d, BYTE PTR [rbx]
	sub	r13, 1
	.p2align 4,,10
	.p2align 3
.L1929:
	mov	r12, rsi
	sub	r12, r13
	test	r9b, 16
	je	.L1931
	movsd	xmm1, QWORD PTR .LC32[rip]
	movapd	xmm0, xmm6
	andpd	xmm0, XMMWORD PTR .LC31[rip]
	ucomisd	xmm1, xmm0
	jb	.L1931
	test	r12, r12
	je	.L2035
	mov	r8, r12
	mov	edx, 46
	mov	rcx, r13
	mov	BYTE PTR 72[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	mov	r10, rax
	je	.L1933
	sub	r10, r13
	cmp	r10, -1
	je	.L1933
	lea	rax, 1[r10]
	mov	QWORD PTR 80[rsp], r12
	cmp	rax, r12
	jnb	.L1934
	mov	r8, r12
	movsx	edx, dil
	mov	QWORD PTR 88[rsp], r10
	lea	rcx, 0[r13+rax]
	sub	r8, rax
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	mov	r10, QWORD PTR 88[rsp]
	je	.L1934
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	mov	QWORD PTR 80[rsp], rax
.L1934:
	cmp	QWORD PTR 80[rsp], r10
	sete	BYTE PTR 88[rsp]
	sete	al
	test	r15b, r15b
	movzx	eax, al
	mov	QWORD PTR 72[rsp], rax
	jne	.L1935
	xor	r15d, r15d
.L1936:
	cmp	QWORD PTR 72[rsp], 0
	je	.L1931
.L2020:
	mov	r9, QWORD PTR 168[rsp]
	mov	rdx, QWORD PTR 72[rsp]
	test	r9, r9
	lea	rax, [r12+rdx]
	mov	QWORD PTR 56[rsp], rax
	jne	.L1938
	mov	rax, QWORD PTR 64[rsp]
	sub	rax, rsi
	cmp	rax, rdx
	jnb	.L2120
	cmp	QWORD PTR 160[rsp], rbp
	je	.L2121
	mov	rax, QWORD PTR 176[rsp]
	mov	rsi, QWORD PTR 56[rsp]
	cmp	rax, rsi
	jnb	.L1947
.L1946:
	cmp	QWORD PTR 56[rsp], 0
	js	.L2016
	add	rax, rax
	cmp	QWORD PTR 56[rsp], rax
	jnb	.L1949
	test	rax, rax
	jns	.L2122
.L1950:
	lea	rsi, 160[rsp]
.LEHB34:
	call	_ZSt17__throw_bad_allocv
.L1961:
	mov	rcx, r12
	mov	r14, r12
	add	rcx, 1
	js	.L1968
.L1969:
	lea	rsi, 160[rsp]
	call	_Znwy
.LEHE34:
	cmp	r14, 1
	mov	r10, rax
	je	.L2123
.L1962:
	mov	rcx, r10
	mov	r8, r14
	mov	rdx, r13
	call	memcpy
	mov	rsi, r12
	mov	r12, r14
	mov	r10, rax
.L1970:
	mov	rcx, QWORD PTR 160[rsp]
	cmp	rcx, rbp
	je	.L1971
	mov	rax, QWORD PTR 176[rsp]
	mov	QWORD PTR 56[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 56[rsp]
.L1971:
	mov	QWORD PTR 160[rsp], r10
	mov	QWORD PTR 176[rsp], rsi
.L1966:
	cmp	BYTE PTR 88[rsp], 0
	mov	QWORD PTR 168[rsp], r12
	mov	BYTE PTR [r10+r12], 0
	jne	.L2124
.L1972:
	test	r15, r15
	mov	r12, QWORD PTR 168[rsp]
	jne	.L2125
.L1974:
	mov	r13, QWORD PTR 160[rsp]
	movzx	r9d, BYTE PTR [rbx]
	.p2align 4,,10
	.p2align 3
.L1931:
	lea	rsi, 208[rsp]
	and	r9d, 32
	mov	QWORD PTR 144[rsp], 0
	mov	BYTE PTR 152[rsp], 0
	mov	QWORD PTR 192[rsp], rsi
	mov	QWORD PTR 200[rsp], 0
	mov	BYTE PTR 208[rsp], 0
	je	.L2045
	mov	rax, QWORD PTR 496[rsp]
	cmp	BYTE PTR 32[rax], 0
	lea	r15, 24[rax]
	je	.L2126
.L1989:
	lea	r14, 136[rsp]
	mov	rdx, r15
	mov	rcx, r14
	call	_ZNSt6localeC1ERKS_
	lea	rcx, 224[rsp]
	mov	r9, r14
	movsx	r8d, dil
	lea	rdx, 96[rsp]
	mov	QWORD PTR 96[rsp], r12
	mov	QWORD PTR 104[rsp], r13
.LEHB35:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE35:
	mov	rax, QWORD PTR 224[rsp]
	lea	rdi, 240[rsp]
	mov	rcx, QWORD PTR 192[rsp]
	mov	r8, QWORD PTR 232[rsp]
	cmp	rax, rdi
	je	.L2127
	movq	xmm0, r8
	cmp	rcx, rsi
	movhps	xmm0, QWORD PTR 240[rsp]
	je	.L2128
	test	rcx, rcx
	mov	rdx, QWORD PTR 208[rsp]
	mov	QWORD PTR 192[rsp], rax
	movups	XMMWORD PTR 200[rsp], xmm0
	je	.L1997
	mov	QWORD PTR 224[rsp], rcx
	mov	QWORD PTR 240[rsp], rdx
.L1996:
	mov	QWORD PTR 232[rsp], 0
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 224[rsp]
	cmp	rcx, rdi
	je	.L1998
	mov	rax, QWORD PTR 240[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1998:
	mov	rcx, r14
	call	_ZNSt6localeD1Ev
	movzx	eax, WORD PTR [rbx]
	mov	r12, QWORD PTR 200[rsp]
	mov	rdi, QWORD PTR 192[rsp]
	and	ax, 384
	cmp	ax, 128
	je	.L2129
.L1999:
	cmp	ax, 256
	je	.L2001
	mov	rax, QWORD PTR 496[rsp]
	mov	r14, QWORD PTR 16[rax]
.L2005:
	lea	rdx, 96[rsp]
	mov	rcx, r14
	mov	QWORD PTR 96[rsp], r12
	mov	QWORD PTR 104[rsp], rdi
.LEHB36:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L2114:
	mov	rcx, QWORD PTR 192[rsp]
	mov	rbx, rax
	cmp	rcx, rsi
	je	.L2009
	mov	rax, QWORD PTR 208[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2009:
	cmp	BYTE PTR 152[rsp], 0
	jne	.L2130
.L2010:
	mov	rcx, QWORD PTR 160[rsp]
	cmp	rcx, rbp
	je	.L2074
	mov	rax, QWORD PTR 176[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	nop
.L2074:
	movaps	xmm6, XMMWORD PTR 384[rsp]
	mov	rax, rbx
	add	rsp, 408
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
.L2045:
	movzx	eax, WORD PTR [rbx]
	mov	rdi, r13
	and	ax, 384
	cmp	ax, 128
	jne	.L1999
.L2129:
	movzx	eax, WORD PTR 4[rbx]
.L2000:
	mov	rdx, QWORD PTR 496[rsp]
	cmp	r12, rax
	mov	r14, QWORD PTR 16[rdx]
	jnb	.L2005
	movzx	edx, BYTE PTR [rbx]
	sub	rax, r12
	movzx	ecx, BYTE PTR 8[rbx]
	mov	rbx, rax
	mov	r8d, edx
	and	r8d, 3
	movsx	eax, cl
	jne	.L2007
	and	edx, 64
	je	.L2047
	movsd	xmm0, QWORD PTR .LC32[rip]
	andpd	xmm6, XMMWORD PTR .LC31[rip]
	ucomisd	xmm0, xmm6
	jnb	.L2131
.L2047:
	mov	eax, 32
	mov	r8d, 2
.L2007:
	lea	rdx, 96[rsp]
	mov	DWORD PTR 32[rsp], eax
	mov	r9, rbx
	mov	rcx, r14
	mov	QWORD PTR 96[rsp], r12
	mov	QWORD PTR 104[rsp], rdi
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
.LEHE36:
	jmp	.L2114
	.p2align 4,,10
	.p2align 3
.L2118:
	cmp	dl, 2
	je	.L2132
	mov	QWORD PTR 56[rsp], -1
	cmp	dl, 4
	je	.L2133
.L1882:
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L1885
	lea	rdx, .L1887[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L1887:
	.long	.L1894-.L1887
	.long	.L2026-.L1887
	.long	.L1892-.L1887
	.long	.L1891-.L1887
	.long	.L2108-.L1887
	.long	.L2110-.L1887
	.long	.L1888-.L1887
	.long	.L2109-.L1887
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2130:
	lea	rcx, 144[rsp]
	call	_ZNSt6localeD1Ev
	jmp	.L2010
	.p2align 4,,10
	.p2align 3
.L2054:
	mov	r12d, 1
.L1897:
	lea	r13, 112[rsp]
	mov	DWORD PTR 32[rsp], 4
	movapd	xmm3, xmm6
	mov	r14d, 4
	lea	rdx, 257[rsp]
	mov	rcx, r13
	mov	edi, 112
	lea	r8, 384[rsp]
	call	_ZSt8to_charsPcS_dSt12chars_format
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	jmp	.L1898
	.p2align 4,,10
	.p2align 3
.L2131:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	eax, 48
	mov	r8d, 2
	cmp	BYTE PTR [rcx+rdx], 15
	jbe	.L2007
	mov	rax, QWORD PTR 24[r14]
	movzx	edx, BYTE PTR [rdi]
	lea	rcx, 1[rax]
	mov	QWORD PTR 24[r14], rcx
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[r14]
	sub	rax, QWORD PTR 8[r14]
	cmp	rax, QWORD PTR 16[r14]
	je	.L2134
.L2008:
	add	rdi, 1
	sub	r12, 1
	mov	eax, 48
	mov	r8d, 2
	jmp	.L2007
	.p2align 4,,10
	.p2align 3
.L2035:
	xor	eax, eax
.L1932:
	test	r15b, r15b
	je	.L2135
	mov	BYTE PTR 88[rsp], r15b
	mov	QWORD PTR 80[rsp], rax
	mov	QWORD PTR 72[rsp], 1
	jmp	.L2019
	.p2align 4,,10
	.p2align 3
.L2055:
	mov	QWORD PTR 56[rsp], 6
.L1891:
	xor	r12d, r12d
.L1890:
	mov	r14d, 1
	mov	edi, 101
	xor	r15d, r15d
.L1893:
	mov	esi, DWORD PTR 56[rsp]
	lea	r13, 112[rsp]
	mov	DWORD PTR 32[rsp], r14d
	movapd	xmm3, xmm6
	lea	rax, 257[rsp]
	mov	rcx, r13
	lea	r8, 384[rsp]
	mov	rdx, rax
	mov	QWORD PTR 72[rsp], rax
	mov	DWORD PTR 40[rsp], esi
	call	_ZSt8to_charsPcS_dSt12chars_formati
	cmp	DWORD PTR 120[rsp], 132
	mov	rsi, QWORD PTR 112[rsp]
	je	.L1895
	lea	rax, 384[rsp]
	mov	r13, QWORD PTR 72[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L1896
	.p2align 4,,10
	.p2align 3
.L2056:
	mov	QWORD PTR 56[rsp], 6
.L2108:
	mov	r12d, 1
	jmp	.L1890
	.p2align 4,,10
	.p2align 3
.L2057:
	mov	QWORD PTR 56[rsp], 6
.L2110:
	mov	r14d, 2
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L1893
	.p2align 4,,10
	.p2align 3
.L2053:
	mov	QWORD PTR 56[rsp], 6
.L2109:
	mov	r12d, 1
.L1886:
	mov	r14d, 3
	mov	edi, 101
	mov	r15d, 1
	jmp	.L1893
	.p2align 4,,10
	.p2align 3
.L2058:
	mov	QWORD PTR 56[rsp], 6
.L1888:
	xor	r12d, r12d
	jmp	.L1886
	.p2align 4,,10
	.p2align 3
.L2024:
	xor	r12d, r12d
	jmp	.L1897
	.p2align 4,,10
	.p2align 3
.L2133:
	mov	rdi, QWORD PTR 496[rsp]
	mov	BYTE PTR 208[rsp], 0
	movzx	eax, WORD PTR 6[rcx]
	movzx	edx, BYTE PTR [rdi]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L2136
	test	cl, cl
	jne	.L1884
	mov	rdi, QWORD PTR 496[rsp]
	mov	rdi, QWORD PTR [rdi]
	mov	rdx, rdi
	mov	QWORD PTR 56[rsp], rdi
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L1884
	mov	rdi, QWORD PTR 496[rsp]
	sal	rax, 5
	add	rax, QWORD PTR 8[rdi]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 192[rsp], rdx
	mov	rdx, QWORD PTR 8[rax]
	mov	QWORD PTR 200[rsp], rdx
	movzx	eax, BYTE PTR 16[rax]
	mov	BYTE PTR 208[rsp], al
	.p2align 4,,10
	.p2align 3
.L1884:
	lea	rcx, 192[rsp]
	lea	rsi, 160[rsp]
.LEHB37:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE37:
	mov	QWORD PTR 56[rsp], rax
	movzx	eax, BYTE PTR 1[rbx]
	jmp	.L1882
	.p2align 4,,10
	.p2align 3
.L2119:
	mov	BYTE PTR -1[r13], 43
	sub	r13, 1
	movzx	r9d, BYTE PTR [rbx]
	jmp	.L1929
	.p2align 4,,10
	.p2align 3
.L2126:
	mov	rcx, r15
	call	_ZNSt6localeC1Ev
	mov	rax, QWORD PTR 496[rsp]
	mov	BYTE PTR 32[rax], 1
	jmp	.L1989
	.p2align 4,,10
	.p2align 3
.L2001:
	mov	rdx, QWORD PTR 496[rsp]
	mov	BYTE PTR 240[rsp], 0
	movzx	eax, WORD PTR 4[rbx]
	movzx	edx, BYTE PTR [rdx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L2137
	test	cl, cl
	jne	.L2004
	mov	rdx, QWORD PTR 496[rsp]
	mov	rdx, QWORD PTR [rdx]
	mov	QWORD PTR 56[rsp], rdx
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L2004
	mov	rdx, QWORD PTR 496[rsp]
	sal	rax, 5
	add	rax, QWORD PTR 8[rdx]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 224[rsp], rdx
	mov	rdx, QWORD PTR 8[rax]
	mov	QWORD PTR 232[rsp], rdx
	movzx	eax, BYTE PTR 16[rax]
	mov	BYTE PTR 240[rsp], al
	.p2align 4,,10
	.p2align 3
.L2004:
	lea	rcx, 224[rsp]
.LEHB38:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE38:
	jmp	.L2000
	.p2align 4,,10
	.p2align 3
.L2128:
	mov	QWORD PTR 192[rsp], rax
	movups	XMMWORD PTR 200[rsp], xmm0
.L1997:
	mov	QWORD PTR 224[rsp], rdi
	lea	rdi, 240[rsp]
	mov	rcx, rdi
	jmp	.L1996
	.p2align 4,,10
	.p2align 3
.L2132:
	movzx	edi, WORD PTR 6[rcx]
	mov	QWORD PTR 56[rsp], rdi
	jmp	.L1882
	.p2align 4,,10
	.p2align 3
.L2127:
	test	r8, r8
	je	.L1992
	cmp	r8, 1
	je	.L2138
	mov	rdx, rdi
	call	memcpy
	mov	r8, QWORD PTR 232[rsp]
	mov	rcx, QWORD PTR 192[rsp]
.L1992:
	mov	QWORD PTR 200[rsp], r8
	mov	BYTE PTR [rcx+r8], 0
	mov	rcx, QWORD PTR 224[rsp]
	jmp	.L1996
	.p2align 4,,10
	.p2align 3
.L1935:
	mov	rax, QWORD PTR 80[rsp]
	sub	rax, 1
.L2019:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	r15, QWORD PTR 56[rsp]
	cmp	BYTE PTR [rcx+rdx], 16
	adc	rax, -1
	sub	r15, rax
	add	QWORD PTR 72[rsp], r15
	jmp	.L1936
	.p2align 4,,10
	.p2align 3
.L2052:
	mov	BYTE PTR 72[rsp], 0
	mov	QWORD PTR 64[rsp], 134
.L1900:
	mov	r9, QWORD PTR 160[rsp]
	cmp	r9, rbp
	je	.L2032
	mov	rax, QWORD PTR 176[rsp]
.L1902:
	mov	rsi, QWORD PTR 64[rsp]
	cmp	rax, rsi
	jb	.L2139
.L1925:
	cmp	r9, rbp
	je	.L2033
	mov	rax, QWORD PTR 176[rsp]
	lea	rsi, [rax+rax]
	cmp	rax, rsi
	mov	QWORD PTR 64[rsp], rsi
	jb	.L2140
.L1914:
	mov	rax, QWORD PTR 64[rsp]
	lea	rdx, 1[r9]
	mov	QWORD PTR 64[rsp], r9
	cmp	BYTE PTR 72[rsp], 0
	lea	r8, -1[r9+rax]
	jne	.L2141
	test	r14d, r14d
	jne	.L2142
	movapd	xmm3, xmm6
	mov	rcx, r13
	call	_ZSt8to_charsPcS_d
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
.L1922:
	test	eax, eax
	jne	.L1924
	mov	rdx, QWORD PTR 160[rsp]
	mov	rax, rsi
	sub	rax, r9
	mov	QWORD PTR 168[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rax, QWORD PTR 160[rsp]
	lea	r13, 1[rax]
	add	rax, QWORD PTR 168[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L1896
	.p2align 4,,10
	.p2align 3
.L1933:
	movsx	edx, dil
	mov	r8, r12
	mov	rcx, r13
	mov	BYTE PTR 72[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	je	.L2039
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	jmp	.L1932
.L2026:
	mov	r14d, 4
	mov	edi, 112
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L1893
.L1892:
	mov	r14d, 4
	mov	edi, 112
	xor	r15d, r15d
	mov	r12d, 1
	jmp	.L1893
.L1894:
	mov	r14d, 3
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L1893
.L2135:
	mov	QWORD PTR 80[rsp], rax
	xor	r15d, r15d
	mov	QWORD PTR 72[rsp], 1
	mov	BYTE PTR 88[rsp], 1
	jmp	.L2020
.L2142:
	mov	DWORD PTR 32[rsp], r14d
	movapd	xmm3, xmm6
	mov	rcx, r13
	call	_ZSt8to_charsPcS_dSt12chars_format
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
	jmp	.L1922
.L2136:
	mov	rdi, QWORD PTR [rdi]
	lea	rcx, [rax+rax*4]
	sal	rax, 4
	mov	rdx, rdi
	mov	QWORD PTR 56[rsp], rdi
	mov	rdi, QWORD PTR 496[rsp]
	shr	rdx, 4
	shr	rdx, cl
	and	edx, 31
	add	rax, QWORD PTR 8[rdi]
	mov	BYTE PTR 208[rsp], dl
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 192[rsp], rdx
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR 200[rsp], rax
	jmp	.L1884
.L2039:
	mov	rax, r12
	jmp	.L1932
.L2121:
	mov	rax, QWORD PTR 56[rsp]
	cmp	rax, 15
	ja	.L2117
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L1954
	mov	r10, rbp
.L2021:
	cmp	r12, 15
	ja	.L2143
.L1960:
	cmp	r13, r10
	jb	.L1964
	cmp	r10, r13
	jb	.L1964
	xor	eax, eax
	mov	QWORD PTR 32[rsp], r12
	mov	r9, r13
	xor	r8d, r8d
	lea	rsi, 160[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	rdx, r10
	mov	rcx, rsi
.LEHB39:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L1966
	.p2align 4,,10
	.p2align 3
.L1924:
	mov	rdx, QWORD PTR 160[rsp]
	cmp	eax, 132
	mov	QWORD PTR 168[rsp], 0
	mov	BYTE PTR [rdx], 0
	mov	r9, QWORD PTR 160[rsp]
	mov	rdx, QWORD PTR 168[rsp]
	je	.L1925
	lea	rax, [r9+rdx]
	lea	r13, 1[r9]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L1896
	.p2align 4,,10
	.p2align 3
.L2139:
	test	rsi, rsi
	js	.L2144
	add	rax, rax
	cmp	QWORD PTR 64[rsp], rax
	jnb	.L1905
	test	rax, rax
	js	.L1906
	lea	rcx, 1[rax]
	mov	QWORD PTR 64[rsp], rax
.L1907:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r9, rax
	mov	rax, QWORD PTR 168[rsp]
	mov	rsi, QWORD PTR 160[rsp]
	lea	r8, 1[rax]
	test	rax, rax
	je	.L2145
	test	r8, r8
	je	.L2111
	mov	rcx, r9
	mov	rdx, rsi
	call	memcpy
	mov	r9, rax
.L2111:
	cmp	rsi, rbp
	je	.L1910
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 80[rsp]
.L1910:
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 160[rsp], r9
	mov	QWORD PTR 176[rsp], rax
	jmp	.L1925
.L2137:
	mov	rdx, QWORD PTR 496[rsp]
	lea	rcx, [rax+rax*4]
	sal	rax, 4
	mov	rdx, QWORD PTR [rdx]
	mov	QWORD PTR 56[rsp], rdx
	shr	rdx, 4
	shr	rdx, cl
	and	edx, 31
	mov	BYTE PTR 240[rsp], dl
	mov	rdx, QWORD PTR 496[rsp]
	add	rax, QWORD PTR 8[rdx]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 224[rsp], rdx
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR 232[rsp], rax
	jmp	.L2004
.L1938:
	cmp	QWORD PTR 160[rsp], rbp
	je	.L1944
	mov	rax, QWORD PTR 176[rsp]
	mov	rsi, QWORD PTR 56[rsp]
	cmp	rax, rsi
	jb	.L1946
.L1945:
	mov	rax, QWORD PTR 80[rsp]
	cmp	r9, rax
	jb	.L2146
.L1957:
	movabs	rax, 9223372036854775807
	mov	rsi, QWORD PTR 72[rsp]
	sub	rax, r9
	cmp	rax, rsi
	jb	.L2147
	mov	rax, QWORD PTR 72[rsp]
	lea	r12, [r9+rax]
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, rbp
	je	.L2044
	mov	rdx, QWORD PTR 176[rsp]
.L1981:
	cmp	rdx, r12
	jb	.L1982
	mov	rsi, QWORD PTR 80[rsp]
	lea	rcx, [rax+rsi]
	sub	r9, rsi
	je	.L1983
	mov	rax, QWORD PTR 72[rsp]
	add	rax, rcx
	cmp	r9, 1
	je	.L2148
	mov	rdx, rcx
	mov	r8, r9
	mov	rcx, rax
	call	memmove
	mov	rcx, QWORD PTR 80[rsp]
	add	rcx, QWORD PTR 160[rsp]
.L1983:
	cmp	QWORD PTR 72[rsp], 1
	je	.L2149
	mov	r8, QWORD PTR 72[rsp]
	mov	edx, 48
	call	memset
.L1986:
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 168[rsp], r12
	cmp	BYTE PTR 88[rsp], 0
	mov	BYTE PTR [rax+r12], 0
	mov	r12, QWORD PTR 168[rsp]
	je	.L1974
	mov	rax, QWORD PTR 160[rsp]
	mov	rsi, QWORD PTR 80[rsp]
	mov	BYTE PTR [rax+rsi], 46
	mov	r12, QWORD PTR 168[rsp]
	jmp	.L1974
.L1949:
	mov	rcx, QWORD PTR 56[rsp]
	add	rcx, 1
	js	.L1950
.L1951:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r9, QWORD PTR 168[rsp]
	mov	rsi, rax
	mov	r14, QWORD PTR 160[rsp]
	lea	r8, 1[r9]
	test	r9, r9
	je	.L2150
	test	r8, r8
	jne	.L1956
	cmp	r14, rbp
	je	.L2151
.L1953:
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, r14
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 168[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	rax, QWORD PTR 56[rsp]
	test	r9, r9
	mov	QWORD PTR 176[rsp], rax
	jne	.L1945
.L1947:
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L1954
	mov	r10, QWORD PTR 160[rsp]
	cmp	r10, rbp
	je	.L2021
.L1959:
	mov	rax, QWORD PTR 176[rsp]
	cmp	rax, r12
	jnb	.L1960
	add	rax, rax
	cmp	r12, rax
	jnb	.L1961
	lea	rcx, 1[rax]
	test	rax, rax
	mov	r14, r12
	mov	r12, rax
	jns	.L1969
.L1968:
	lea	rsi, 160[rsp]
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L1905:
	mov	rcx, QWORD PTR 64[rsp]
	add	rcx, 1
	jns	.L1907
.L1906:
	lea	rsi, 160[rsp]
	call	_ZSt17__throw_bad_allocv
.L2141:
	mov	eax, DWORD PTR 56[rsp]
	mov	DWORD PTR 32[rsp], r14d
	movapd	xmm3, xmm6
	mov	rcx, r13
	mov	DWORD PTR 40[rsp], eax
	call	_ZSt8to_charsPcS_dSt12chars_formati
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
	jmp	.L1922
.L1895:
	mov	rax, QWORD PTR 56[rsp]
	cmp	r14d, 2
	mov	BYTE PTR 72[rsp], 1
	lea	rsi, 128[rax]
	mov	QWORD PTR 64[rsp], rsi
	jne	.L1900
	cvttsd2si	eax, xmm6
	pxor	xmm0, xmm0
	cdq
	xor	eax, edx
	sub	eax, edx
	cvtsi2sd	xmm0, eax
	call	log10
	cvttsd2si	edx, xmm0
	mov	eax, edx
	sar	eax
	cmp	edx, 1
	mov	edx, 1
	cdqe
	cmovle	rax, rdx
	add	rsi, rax
	mov	QWORD PTR 64[rsp], rsi
	jmp	.L1900
.L1964:
	test	r12, r12
	je	.L1966
	cmp	r12, 1
	je	.L2152
	mov	rcx, r10
	mov	r8, r12
	mov	rdx, r13
	call	memcpy
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L1966
.L2120:
	mov	rax, QWORD PTR 80[rsp]
	mov	rcx, rdx
	mov	r8, r12
	lea	rsi, 0[r13+rax]
	add	rcx, rax
	sub	r8, rax
	add	rcx, r13
	mov	rdx, rsi
	call	memmove
	cmp	BYTE PTR 88[rsp], 0
	je	.L1941
	mov	rax, QWORD PTR 80[rsp]
	mov	BYTE PTR [rsi], 46
	lea	rsi, 1[r13+rax]
.L1941:
	mov	r8, r15
	mov	edx, 48
	mov	rcx, rsi
	call	memset
	movzx	r9d, BYTE PTR [rbx]
	mov	r12, QWORD PTR 56[rsp]
	jmp	.L1931
.L2033:
	mov	QWORD PTR 64[rsp], 30
	mov	ecx, 31
.L1913:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r8, QWORD PTR 168[rsp]
	mov	r9, rax
	mov	rsi, QWORD PTR 160[rsp]
	cmp	r8, 1
	je	.L2153
	test	r8, r8
	je	.L2113
	mov	rdx, rsi
	mov	rcx, rax
	call	memcpy
	mov	r9, rax
.L2113:
	cmp	rsi, rbp
	je	.L1918
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 80[rsp]
.L1918:
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 160[rsp], r9
	mov	QWORD PTR 176[rsp], rax
	jmp	.L1914
.L2032:
	mov	eax, 15
	jmp	.L1902
.L2140:
	test	rsi, rsi
	js	.L1915
	lea	rcx, 1[rsi]
	jmp	.L1913
.L1982:
	mov	rax, QWORD PTR 72[rsp]
	lea	rsi, 160[rsp]
	xor	r9d, r9d
	xor	r8d, r8d
	mov	r15, QWORD PTR 80[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 32[rsp], rax
	mov	rdx, r15
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rcx, QWORD PTR 160[rsp]
	add	rcx, r15
	jmp	.L1983
.L2145:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r9], al
	jmp	.L2111
.L2150:
	movzx	eax, BYTE PTR [r14]
	cmp	r14, rbp
	mov	BYTE PTR [rsi], al
	jne	.L1953
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	QWORD PTR 176[rsp], rax
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L1954
	mov	r10, rsi
	jmp	.L1959
.L2125:
	movabs	rax, 9223372036854775807
	sub	rax, r12
	cmp	rax, r15
	jb	.L2154
	mov	rax, QWORD PTR 160[rsp]
	lea	r13, [r12+r15]
	cmp	rax, rbp
	je	.L2043
	mov	rdx, QWORD PTR 176[rsp]
.L1976:
	cmp	rdx, r13
	jb	.L2155
.L1977:
	lea	rcx, [rax+r12]
	cmp	r15, 1
	je	.L2156
	mov	r8, r15
	mov	edx, 48
	call	memset
.L1979:
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 168[rsp], r13
	mov	BYTE PTR [rax+r13], 0
	mov	r12, QWORD PTR 168[rsp]
	jmp	.L1974
.L1956:
	mov	rdx, r14
	mov	rcx, rax
	mov	QWORD PTR 64[rsp], r9
	call	memcpy
	cmp	r14, rbp
	mov	r9, QWORD PTR 64[rsp]
	jne	.L1953
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	QWORD PTR 176[rsp], rax
	jmp	.L1945
.L2138:
	movzx	eax, BYTE PTR 240[rsp]
	mov	BYTE PTR [rcx], al
	mov	r8, QWORD PTR 232[rsp]
	mov	rcx, QWORD PTR 192[rsp]
	jmp	.L1992
.L2153:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r9], al
	jmp	.L2113
.L2124:
	lea	rsi, 160[rsp]
	mov	edx, 46
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	jmp	.L1972
.L1944:
	mov	rax, QWORD PTR 56[rsp]
	cmp	rax, 15
	jbe	.L1945
.L2117:
	test	rax, rax
	js	.L2016
	cmp	rax, 29
	ja	.L1949
	mov	QWORD PTR 56[rsp], 30
.L2017:
	mov	rax, QWORD PTR 56[rsp]
	lea	rcx, 1[rax]
	jmp	.L1951
.L2044:
	mov	edx, 15
	jmp	.L1981
.L2149:
	mov	BYTE PTR [rcx], 48
	jmp	.L1986
.L2148:
	movzx	edx, BYTE PTR [rcx]
	mov	BYTE PTR [rax], dl
	mov	rcx, QWORD PTR 160[rsp]
	add	rcx, rsi
	jmp	.L1983
.L2152:
	movzx	eax, BYTE PTR 0[r13]
	mov	BYTE PTR [r10], al
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L1966
.L2155:
	mov	QWORD PTR 32[rsp], r15
	xor	r9d, r9d
	xor	r8d, r8d
	mov	rdx, r12
	lea	rsi, 160[rsp]
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE39:
	mov	rax, QWORD PTR 160[rsp]
	jmp	.L1977
.L2134:
	mov	rax, QWORD PTR [r14]
	mov	rcx, r14
.LEHB40:
	call	[QWORD PTR [rax]]
.LEHE40:
	jmp	.L2008
.L2143:
	cmp	r12, 29
	ja	.L1961
	lea	rsi, 160[rsp]
	mov	ecx, 31
.LEHB41:
	call	_Znwy
	mov	r14, r12
	mov	r10, rax
	mov	r12d, 30
	jmp	.L1962
.L2156:
	mov	BYTE PTR [rcx], 48
	jmp	.L1979
.L2043:
	mov	edx, 15
	jmp	.L1976
.L2151:
	mov	QWORD PTR 160[rsp], rax
	mov	rax, QWORD PTR 56[rsp]
	mov	r9, -1
	mov	QWORD PTR 176[rsp], rax
	jmp	.L1957
.L2123:
	movzx	eax, BYTE PTR 0[r13]
	mov	rsi, r12
	mov	r12d, 1
	mov	BYTE PTR [r10], al
	jmp	.L1970
.L2122:
	mov	QWORD PTR 56[rsp], rax
	jmp	.L2017
.L2144:
	lea	rcx, .LC9[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1915:
	lea	rcx, .LC9[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2016:
	lea	rcx, .LC9[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2147:
	lea	rcx, .LC27[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2146:
	lea	rdx, .LC28[rip]
	mov	r8, rax
	lea	rcx, .LC29[rip]
	lea	rsi, 160[rsp]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L1954:
	lea	rcx, .LC26[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2154:
	lea	rcx, .LC27[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.LEHE41:
.L1885:
	xor	r14d, r14d
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L1893
.L2059:
	mov	rbx, rax
.L2015:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB42:
	call	_Unwind_Resume
.LEHE42:
.L2061:
	mov	rbx, rax
	jmp	.L2013
.L2060:
	mov	rcx, r14
	mov	rbx, rax
	call	_ZNSt6localeD1Ev
.L2013:
	lea	rcx, 192[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	cmp	BYTE PTR 152[rsp], 0
	je	.L2014
	lea	rcx, 144[rsp]
	call	_ZNSt6localeD1Ev
.L2014:
	lea	rsi, 160[rsp]
	jmp	.L2015
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4918:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4918-.LLSDACSB4918
.LLSDACSB4918:
	.uleb128 .LEHB34-.LFB4918
	.uleb128 .LEHE34-.LEHB34
	.uleb128 .L2059-.LFB4918
	.uleb128 0
	.uleb128 .LEHB35-.LFB4918
	.uleb128 .LEHE35-.LEHB35
	.uleb128 .L2060-.LFB4918
	.uleb128 0
	.uleb128 .LEHB36-.LFB4918
	.uleb128 .LEHE36-.LEHB36
	.uleb128 .L2061-.LFB4918
	.uleb128 0
	.uleb128 .LEHB37-.LFB4918
	.uleb128 .LEHE37-.LEHB37
	.uleb128 .L2059-.LFB4918
	.uleb128 0
	.uleb128 .LEHB38-.LFB4918
	.uleb128 .LEHE38-.LEHB38
	.uleb128 .L2061-.LFB4918
	.uleb128 0
	.uleb128 .LEHB39-.LFB4918
	.uleb128 .LEHE39-.LEHB39
	.uleb128 .L2059-.LFB4918
	.uleb128 0
	.uleb128 .LEHB40-.LFB4918
	.uleb128 .LEHE40-.LEHB40
	.uleb128 .L2061-.LFB4918
	.uleb128 0
	.uleb128 .LEHB41-.LFB4918
	.uleb128 .LEHE41-.LEHB41
	.uleb128 .L2059-.LFB4918
	.uleb128 0
	.uleb128 .LEHB42-.LFB4918
	.uleb128 .LEHE42-.LEHB42
	.uleb128 0
	.uleb128 0
.LLSDACSE4918:
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB4914:
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
	sub	rsp, 408
	.seh_stackalloc	408
	movaps	XMMWORD PTR 384[rsp], xmm6
	.seh_savexmm	xmm6, 384
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	edx, eax
	mov	rbx, rcx
	movaps	xmm6, xmm1
	mov	QWORD PTR 496[rsp], r8
	lea	rbp, 176[rsp]
	and	edx, 6
	mov	QWORD PTR 168[rsp], 0
	mov	QWORD PTR 160[rsp], rbp
	mov	BYTE PTR 176[rsp], 0
	jne	.L2396
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L2177
	lea	rdx, .L2301[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2301:
	.long	.L2177-.L2301
	.long	.L2302-.L2301
	.long	.L2332-.L2301
	.long	.L2333-.L2301
	.long	.L2334-.L2301
	.long	.L2335-.L2301
	.long	.L2336-.L2301
	.long	.L2331-.L2301
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2177:
	lea	r13, 112[rsp]
	movaps	xmm3, xmm6
	xor	r14d, r14d
	lea	rdx, 257[rsp]
	mov	rcx, r13
	xor	edi, edi
	lea	r8, 384[rsp]
	xor	r12d, r12d
	call	_ZSt8to_charsPcS_f
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
.L2176:
	mov	QWORD PTR 56[rsp], 6
	xor	r15d, r15d
	cmp	eax, 132
	je	.L2330
	lea	rax, 384[rsp]
	mov	QWORD PTR 64[rsp], rax
	lea	r13, 257[rsp]
.L2174:
	test	r12b, r12b
	je	.L2204
	cmp	r13, rsi
	mov	r12, QWORD PTR __imp_toupper[rip]
	mov	r14, r13
	je	.L2206
	.p2align 4,,10
	.p2align 3
.L2205:
	movsx	ecx, BYTE PTR [r14]
	add	r14, 1
	call	r12
	mov	BYTE PTR -1[r14], al
	cmp	rsi, r14
	jne	.L2205
.L2206:
	movsx	ecx, dil
	call	r12
	mov	edi, eax
.L2204:
	movd	eax, xmm6
	movzx	r9d, BYTE PTR [rbx]
	test	eax, eax
	js	.L2207
	mov	eax, r9d
	and	eax, 12
	cmp	al, 4
	je	.L2397
	cmp	al, 12
	jne	.L2207
	mov	BYTE PTR -1[r13], 32
	movzx	r9d, BYTE PTR [rbx]
	sub	r13, 1
	.p2align 4,,10
	.p2align 3
.L2207:
	mov	r12, rsi
	sub	r12, r13
	test	r9b, 16
	je	.L2209
	movss	xmm1, DWORD PTR .LC34[rip]
	movaps	xmm0, xmm6
	andps	xmm0, XMMWORD PTR .LC33[rip]
	ucomiss	xmm1, xmm0
	jb	.L2209
	test	r12, r12
	je	.L2313
	mov	r8, r12
	mov	edx, 46
	mov	rcx, r13
	mov	BYTE PTR 72[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	mov	r10, rax
	je	.L2211
	sub	r10, r13
	cmp	r10, -1
	je	.L2211
	lea	rax, 1[r10]
	mov	QWORD PTR 80[rsp], r12
	cmp	rax, r12
	jnb	.L2212
	mov	r8, r12
	movsx	edx, dil
	mov	QWORD PTR 88[rsp], r10
	lea	rcx, 0[r13+rax]
	sub	r8, rax
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	mov	r10, QWORD PTR 88[rsp]
	je	.L2212
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	mov	QWORD PTR 80[rsp], rax
.L2212:
	cmp	QWORD PTR 80[rsp], r10
	sete	BYTE PTR 88[rsp]
	sete	al
	test	r15b, r15b
	movzx	eax, al
	mov	QWORD PTR 72[rsp], rax
	jne	.L2213
	xor	r15d, r15d
.L2214:
	cmp	QWORD PTR 72[rsp], 0
	je	.L2209
.L2298:
	mov	r9, QWORD PTR 168[rsp]
	mov	rdx, QWORD PTR 72[rsp]
	test	r9, r9
	lea	rax, [r12+rdx]
	mov	QWORD PTR 56[rsp], rax
	jne	.L2216
	mov	rax, QWORD PTR 64[rsp]
	sub	rax, rsi
	cmp	rax, rdx
	jnb	.L2398
	cmp	QWORD PTR 160[rsp], rbp
	je	.L2399
	mov	rax, QWORD PTR 176[rsp]
	mov	rsi, QWORD PTR 56[rsp]
	cmp	rax, rsi
	jnb	.L2225
.L2224:
	cmp	QWORD PTR 56[rsp], 0
	js	.L2294
	add	rax, rax
	cmp	QWORD PTR 56[rsp], rax
	jnb	.L2227
	test	rax, rax
	jns	.L2400
.L2228:
	lea	rsi, 160[rsp]
.LEHB43:
	call	_ZSt17__throw_bad_allocv
.L2239:
	mov	rcx, r12
	mov	r14, r12
	add	rcx, 1
	js	.L2246
.L2247:
	lea	rsi, 160[rsp]
	call	_Znwy
.LEHE43:
	cmp	r14, 1
	mov	r10, rax
	je	.L2401
.L2240:
	mov	rcx, r10
	mov	r8, r14
	mov	rdx, r13
	call	memcpy
	mov	rsi, r12
	mov	r12, r14
	mov	r10, rax
.L2248:
	mov	rcx, QWORD PTR 160[rsp]
	cmp	rcx, rbp
	je	.L2249
	mov	rax, QWORD PTR 176[rsp]
	mov	QWORD PTR 56[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 56[rsp]
.L2249:
	mov	QWORD PTR 160[rsp], r10
	mov	QWORD PTR 176[rsp], rsi
.L2244:
	cmp	BYTE PTR 88[rsp], 0
	mov	QWORD PTR 168[rsp], r12
	mov	BYTE PTR [r10+r12], 0
	jne	.L2402
.L2250:
	test	r15, r15
	mov	r12, QWORD PTR 168[rsp]
	jne	.L2403
.L2252:
	mov	r13, QWORD PTR 160[rsp]
	movzx	r9d, BYTE PTR [rbx]
	.p2align 4,,10
	.p2align 3
.L2209:
	lea	rsi, 208[rsp]
	and	r9d, 32
	mov	QWORD PTR 144[rsp], 0
	mov	BYTE PTR 152[rsp], 0
	mov	QWORD PTR 192[rsp], rsi
	mov	QWORD PTR 200[rsp], 0
	mov	BYTE PTR 208[rsp], 0
	je	.L2323
	mov	rax, QWORD PTR 496[rsp]
	cmp	BYTE PTR 32[rax], 0
	lea	r15, 24[rax]
	je	.L2404
.L2267:
	lea	r14, 136[rsp]
	mov	rdx, r15
	mov	rcx, r14
	call	_ZNSt6localeC1ERKS_
	lea	rcx, 224[rsp]
	mov	r9, r14
	movsx	r8d, dil
	lea	rdx, 96[rsp]
	mov	QWORD PTR 96[rsp], r12
	mov	QWORD PTR 104[rsp], r13
.LEHB44:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE44:
	mov	rax, QWORD PTR 224[rsp]
	lea	rdi, 240[rsp]
	mov	rcx, QWORD PTR 192[rsp]
	mov	r8, QWORD PTR 232[rsp]
	cmp	rax, rdi
	je	.L2405
	movq	xmm0, r8
	cmp	rcx, rsi
	movhps	xmm0, QWORD PTR 240[rsp]
	je	.L2406
	test	rcx, rcx
	mov	rdx, QWORD PTR 208[rsp]
	mov	QWORD PTR 192[rsp], rax
	movups	XMMWORD PTR 200[rsp], xmm0
	je	.L2275
	mov	QWORD PTR 224[rsp], rcx
	mov	QWORD PTR 240[rsp], rdx
.L2274:
	mov	QWORD PTR 232[rsp], 0
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 224[rsp]
	cmp	rcx, rdi
	je	.L2276
	mov	rax, QWORD PTR 240[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2276:
	mov	rcx, r14
	call	_ZNSt6localeD1Ev
	movzx	eax, WORD PTR [rbx]
	mov	r12, QWORD PTR 200[rsp]
	mov	rdi, QWORD PTR 192[rsp]
	and	ax, 384
	cmp	ax, 128
	je	.L2407
.L2277:
	cmp	ax, 256
	je	.L2279
	mov	rax, QWORD PTR 496[rsp]
	mov	r14, QWORD PTR 16[rax]
.L2283:
	lea	rdx, 96[rsp]
	mov	rcx, r14
	mov	QWORD PTR 96[rsp], r12
	mov	QWORD PTR 104[rsp], rdi
.LEHB45:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L2392:
	mov	rcx, QWORD PTR 192[rsp]
	mov	rbx, rax
	cmp	rcx, rsi
	je	.L2287
	mov	rax, QWORD PTR 208[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2287:
	cmp	BYTE PTR 152[rsp], 0
	jne	.L2408
.L2288:
	mov	rcx, QWORD PTR 160[rsp]
	cmp	rcx, rbp
	je	.L2352
	mov	rax, QWORD PTR 176[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	nop
.L2352:
	movaps	xmm6, XMMWORD PTR 384[rsp]
	mov	rax, rbx
	add	rsp, 408
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
.L2323:
	movzx	eax, WORD PTR [rbx]
	mov	rdi, r13
	and	ax, 384
	cmp	ax, 128
	jne	.L2277
.L2407:
	movzx	eax, WORD PTR 4[rbx]
.L2278:
	mov	rdx, QWORD PTR 496[rsp]
	cmp	r12, rax
	mov	r14, QWORD PTR 16[rdx]
	jnb	.L2283
	movzx	edx, BYTE PTR [rbx]
	sub	rax, r12
	movzx	ecx, BYTE PTR 8[rbx]
	mov	rbx, rax
	mov	r8d, edx
	and	r8d, 3
	movsx	eax, cl
	jne	.L2285
	and	edx, 64
	je	.L2325
	movss	xmm0, DWORD PTR .LC34[rip]
	andps	xmm6, XMMWORD PTR .LC33[rip]
	ucomiss	xmm0, xmm6
	jnb	.L2409
.L2325:
	mov	eax, 32
	mov	r8d, 2
.L2285:
	lea	rdx, 96[rsp]
	mov	DWORD PTR 32[rsp], eax
	mov	r9, rbx
	mov	rcx, r14
	mov	QWORD PTR 96[rsp], r12
	mov	QWORD PTR 104[rsp], rdi
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
.LEHE45:
	jmp	.L2392
	.p2align 4,,10
	.p2align 3
.L2396:
	cmp	dl, 2
	je	.L2410
	mov	QWORD PTR 56[rsp], -1
	cmp	dl, 4
	je	.L2411
.L2160:
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L2163
	lea	rdx, .L2165[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2165:
	.long	.L2172-.L2165
	.long	.L2304-.L2165
	.long	.L2170-.L2165
	.long	.L2169-.L2165
	.long	.L2386-.L2165
	.long	.L2388-.L2165
	.long	.L2166-.L2165
	.long	.L2387-.L2165
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2408:
	lea	rcx, 144[rsp]
	call	_ZNSt6localeD1Ev
	jmp	.L2288
	.p2align 4,,10
	.p2align 3
.L2332:
	mov	r12d, 1
.L2175:
	lea	r13, 112[rsp]
	mov	DWORD PTR 32[rsp], 4
	movaps	xmm3, xmm6
	mov	edi, 112
	lea	rdx, 257[rsp]
	mov	rcx, r13
	mov	r14d, 4
	lea	r8, 384[rsp]
	call	_ZSt8to_charsPcS_fSt12chars_format
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	jmp	.L2176
	.p2align 4,,10
	.p2align 3
.L2409:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	eax, 48
	mov	r8d, 2
	cmp	BYTE PTR [rcx+rdx], 15
	jbe	.L2285
	mov	rax, QWORD PTR 24[r14]
	movzx	edx, BYTE PTR [rdi]
	lea	rcx, 1[rax]
	mov	QWORD PTR 24[r14], rcx
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[r14]
	sub	rax, QWORD PTR 8[r14]
	cmp	rax, QWORD PTR 16[r14]
	je	.L2412
.L2286:
	add	rdi, 1
	sub	r12, 1
	mov	eax, 48
	mov	r8d, 2
	jmp	.L2285
	.p2align 4,,10
	.p2align 3
.L2313:
	xor	eax, eax
.L2210:
	test	r15b, r15b
	je	.L2413
	mov	BYTE PTR 88[rsp], r15b
	mov	QWORD PTR 80[rsp], rax
	mov	QWORD PTR 72[rsp], 1
	jmp	.L2297
	.p2align 4,,10
	.p2align 3
.L2333:
	mov	QWORD PTR 56[rsp], 6
.L2169:
	xor	r12d, r12d
.L2168:
	mov	r14d, 1
	mov	edi, 101
	xor	r15d, r15d
.L2171:
	mov	esi, DWORD PTR 56[rsp]
	lea	rax, 257[rsp]
	mov	DWORD PTR 32[rsp], r14d
	movaps	xmm3, xmm6
	lea	r13, 112[rsp]
	mov	rdx, rax
	mov	QWORD PTR 72[rsp], rax
	lea	r8, 384[rsp]
	mov	rcx, r13
	mov	DWORD PTR 40[rsp], esi
	call	_ZSt8to_charsPcS_fSt12chars_formati
	cmp	DWORD PTR 120[rsp], 132
	mov	rsi, QWORD PTR 112[rsp]
	je	.L2173
	lea	rax, 384[rsp]
	mov	r13, QWORD PTR 72[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L2174
	.p2align 4,,10
	.p2align 3
.L2334:
	mov	QWORD PTR 56[rsp], 6
.L2386:
	mov	r12d, 1
	jmp	.L2168
	.p2align 4,,10
	.p2align 3
.L2335:
	mov	QWORD PTR 56[rsp], 6
.L2388:
	mov	r14d, 2
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L2171
	.p2align 4,,10
	.p2align 3
.L2331:
	mov	QWORD PTR 56[rsp], 6
.L2387:
	mov	r12d, 1
.L2164:
	mov	r14d, 3
	mov	edi, 101
	mov	r15d, 1
	jmp	.L2171
	.p2align 4,,10
	.p2align 3
.L2336:
	mov	QWORD PTR 56[rsp], 6
.L2166:
	xor	r12d, r12d
	jmp	.L2164
	.p2align 4,,10
	.p2align 3
.L2302:
	xor	r12d, r12d
	jmp	.L2175
	.p2align 4,,10
	.p2align 3
.L2411:
	mov	rdi, QWORD PTR 496[rsp]
	mov	BYTE PTR 208[rsp], 0
	movzx	eax, WORD PTR 6[rcx]
	movzx	edx, BYTE PTR [rdi]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L2414
	test	cl, cl
	jne	.L2162
	mov	rdi, QWORD PTR 496[rsp]
	mov	rdi, QWORD PTR [rdi]
	mov	rdx, rdi
	mov	QWORD PTR 56[rsp], rdi
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L2162
	mov	rdi, QWORD PTR 496[rsp]
	sal	rax, 5
	add	rax, QWORD PTR 8[rdi]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 192[rsp], rdx
	mov	rdx, QWORD PTR 8[rax]
	mov	QWORD PTR 200[rsp], rdx
	movzx	eax, BYTE PTR 16[rax]
	mov	BYTE PTR 208[rsp], al
	.p2align 4,,10
	.p2align 3
.L2162:
	lea	rcx, 192[rsp]
	lea	rsi, 160[rsp]
.LEHB46:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE46:
	mov	QWORD PTR 56[rsp], rax
	movzx	eax, BYTE PTR 1[rbx]
	jmp	.L2160
	.p2align 4,,10
	.p2align 3
.L2397:
	mov	BYTE PTR -1[r13], 43
	sub	r13, 1
	movzx	r9d, BYTE PTR [rbx]
	jmp	.L2207
	.p2align 4,,10
	.p2align 3
.L2404:
	mov	rcx, r15
	call	_ZNSt6localeC1Ev
	mov	rax, QWORD PTR 496[rsp]
	mov	BYTE PTR 32[rax], 1
	jmp	.L2267
	.p2align 4,,10
	.p2align 3
.L2279:
	mov	rdx, QWORD PTR 496[rsp]
	mov	BYTE PTR 240[rsp], 0
	movzx	eax, WORD PTR 4[rbx]
	movzx	edx, BYTE PTR [rdx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L2415
	test	cl, cl
	jne	.L2282
	mov	rdx, QWORD PTR 496[rsp]
	mov	rdx, QWORD PTR [rdx]
	mov	QWORD PTR 56[rsp], rdx
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L2282
	mov	rdx, QWORD PTR 496[rsp]
	sal	rax, 5
	add	rax, QWORD PTR 8[rdx]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 224[rsp], rdx
	mov	rdx, QWORD PTR 8[rax]
	mov	QWORD PTR 232[rsp], rdx
	movzx	eax, BYTE PTR 16[rax]
	mov	BYTE PTR 240[rsp], al
	.p2align 4,,10
	.p2align 3
.L2282:
	lea	rcx, 224[rsp]
.LEHB47:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE47:
	jmp	.L2278
	.p2align 4,,10
	.p2align 3
.L2406:
	mov	QWORD PTR 192[rsp], rax
	movups	XMMWORD PTR 200[rsp], xmm0
.L2275:
	mov	QWORD PTR 224[rsp], rdi
	lea	rdi, 240[rsp]
	mov	rcx, rdi
	jmp	.L2274
	.p2align 4,,10
	.p2align 3
.L2410:
	movzx	edi, WORD PTR 6[rcx]
	mov	QWORD PTR 56[rsp], rdi
	jmp	.L2160
	.p2align 4,,10
	.p2align 3
.L2405:
	test	r8, r8
	je	.L2270
	cmp	r8, 1
	je	.L2416
	mov	rdx, rdi
	call	memcpy
	mov	r8, QWORD PTR 232[rsp]
	mov	rcx, QWORD PTR 192[rsp]
.L2270:
	mov	QWORD PTR 200[rsp], r8
	mov	BYTE PTR [rcx+r8], 0
	mov	rcx, QWORD PTR 224[rsp]
	jmp	.L2274
	.p2align 4,,10
	.p2align 3
.L2213:
	mov	rax, QWORD PTR 80[rsp]
	sub	rax, 1
.L2297:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	r15, QWORD PTR 56[rsp]
	cmp	BYTE PTR [rcx+rdx], 16
	adc	rax, -1
	sub	r15, rax
	add	QWORD PTR 72[rsp], r15
	jmp	.L2214
	.p2align 4,,10
	.p2align 3
.L2330:
	mov	BYTE PTR 72[rsp], 0
	mov	QWORD PTR 64[rsp], 134
.L2178:
	mov	r9, QWORD PTR 160[rsp]
	cmp	r9, rbp
	je	.L2310
	mov	rax, QWORD PTR 176[rsp]
.L2180:
	mov	rsi, QWORD PTR 64[rsp]
	cmp	rax, rsi
	jb	.L2417
.L2203:
	cmp	r9, rbp
	je	.L2311
	mov	rax, QWORD PTR 176[rsp]
	lea	rsi, [rax+rax]
	cmp	rax, rsi
	mov	QWORD PTR 64[rsp], rsi
	jb	.L2418
.L2192:
	mov	rax, QWORD PTR 64[rsp]
	lea	rdx, 1[r9]
	mov	QWORD PTR 64[rsp], r9
	cmp	BYTE PTR 72[rsp], 0
	lea	r8, -1[r9+rax]
	jne	.L2419
	test	r14d, r14d
	jne	.L2420
	movaps	xmm3, xmm6
	mov	rcx, r13
	call	_ZSt8to_charsPcS_f
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
.L2200:
	test	eax, eax
	jne	.L2202
	mov	rdx, QWORD PTR 160[rsp]
	mov	rax, rsi
	sub	rax, r9
	mov	QWORD PTR 168[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rax, QWORD PTR 160[rsp]
	lea	r13, 1[rax]
	add	rax, QWORD PTR 168[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L2174
	.p2align 4,,10
	.p2align 3
.L2211:
	movsx	edx, dil
	mov	r8, r12
	mov	rcx, r13
	mov	BYTE PTR 72[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	je	.L2317
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	jmp	.L2210
.L2304:
	mov	r14d, 4
	mov	edi, 112
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L2171
.L2170:
	mov	r14d, 4
	mov	edi, 112
	xor	r15d, r15d
	mov	r12d, 1
	jmp	.L2171
.L2172:
	mov	r14d, 3
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L2171
.L2413:
	mov	QWORD PTR 80[rsp], rax
	xor	r15d, r15d
	mov	QWORD PTR 72[rsp], 1
	mov	BYTE PTR 88[rsp], 1
	jmp	.L2298
.L2420:
	mov	DWORD PTR 32[rsp], r14d
	movaps	xmm3, xmm6
	mov	rcx, r13
	call	_ZSt8to_charsPcS_fSt12chars_format
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
	jmp	.L2200
.L2414:
	mov	rdi, QWORD PTR [rdi]
	lea	rcx, [rax+rax*4]
	sal	rax, 4
	mov	rdx, rdi
	mov	QWORD PTR 56[rsp], rdi
	mov	rdi, QWORD PTR 496[rsp]
	shr	rdx, 4
	shr	rdx, cl
	and	edx, 31
	add	rax, QWORD PTR 8[rdi]
	mov	BYTE PTR 208[rsp], dl
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 192[rsp], rdx
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR 200[rsp], rax
	jmp	.L2162
.L2317:
	mov	rax, r12
	jmp	.L2210
.L2399:
	mov	rax, QWORD PTR 56[rsp]
	cmp	rax, 15
	ja	.L2395
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L2232
	mov	r10, rbp
.L2299:
	cmp	r12, 15
	ja	.L2421
.L2238:
	cmp	r13, r10
	jb	.L2242
	cmp	r10, r13
	jb	.L2242
	xor	eax, eax
	mov	QWORD PTR 32[rsp], r12
	mov	r9, r13
	xor	r8d, r8d
	lea	rsi, 160[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	rdx, r10
	mov	rcx, rsi
.LEHB48:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L2244
	.p2align 4,,10
	.p2align 3
.L2202:
	mov	rdx, QWORD PTR 160[rsp]
	cmp	eax, 132
	mov	QWORD PTR 168[rsp], 0
	mov	BYTE PTR [rdx], 0
	mov	r9, QWORD PTR 160[rsp]
	mov	rdx, QWORD PTR 168[rsp]
	je	.L2203
	lea	rax, [r9+rdx]
	lea	r13, 1[r9]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L2174
	.p2align 4,,10
	.p2align 3
.L2417:
	test	rsi, rsi
	js	.L2422
	add	rax, rax
	cmp	QWORD PTR 64[rsp], rax
	jnb	.L2183
	test	rax, rax
	js	.L2184
	lea	rcx, 1[rax]
	mov	QWORD PTR 64[rsp], rax
.L2185:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r9, rax
	mov	rax, QWORD PTR 168[rsp]
	mov	rsi, QWORD PTR 160[rsp]
	lea	r8, 1[rax]
	test	rax, rax
	je	.L2423
	test	r8, r8
	je	.L2389
	mov	rcx, r9
	mov	rdx, rsi
	call	memcpy
	mov	r9, rax
.L2389:
	cmp	rsi, rbp
	je	.L2188
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 80[rsp]
.L2188:
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 160[rsp], r9
	mov	QWORD PTR 176[rsp], rax
	jmp	.L2203
.L2415:
	mov	rdx, QWORD PTR 496[rsp]
	lea	rcx, [rax+rax*4]
	sal	rax, 4
	mov	rdx, QWORD PTR [rdx]
	mov	QWORD PTR 56[rsp], rdx
	shr	rdx, 4
	shr	rdx, cl
	and	edx, 31
	mov	BYTE PTR 240[rsp], dl
	mov	rdx, QWORD PTR 496[rsp]
	add	rax, QWORD PTR 8[rdx]
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 224[rsp], rdx
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR 232[rsp], rax
	jmp	.L2282
.L2216:
	cmp	QWORD PTR 160[rsp], rbp
	je	.L2222
	mov	rax, QWORD PTR 176[rsp]
	mov	rsi, QWORD PTR 56[rsp]
	cmp	rax, rsi
	jb	.L2224
.L2223:
	mov	rax, QWORD PTR 80[rsp]
	cmp	r9, rax
	jb	.L2424
.L2235:
	movabs	rax, 9223372036854775807
	mov	rsi, QWORD PTR 72[rsp]
	sub	rax, r9
	cmp	rax, rsi
	jb	.L2425
	mov	rax, QWORD PTR 72[rsp]
	lea	r12, [r9+rax]
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, rbp
	je	.L2322
	mov	rdx, QWORD PTR 176[rsp]
.L2259:
	cmp	rdx, r12
	jb	.L2260
	mov	rsi, QWORD PTR 80[rsp]
	lea	rcx, [rax+rsi]
	sub	r9, rsi
	je	.L2261
	mov	rax, QWORD PTR 72[rsp]
	add	rax, rcx
	cmp	r9, 1
	je	.L2426
	mov	rdx, rcx
	mov	r8, r9
	mov	rcx, rax
	call	memmove
	mov	rcx, QWORD PTR 80[rsp]
	add	rcx, QWORD PTR 160[rsp]
.L2261:
	cmp	QWORD PTR 72[rsp], 1
	je	.L2427
	mov	r8, QWORD PTR 72[rsp]
	mov	edx, 48
	call	memset
.L2264:
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 168[rsp], r12
	cmp	BYTE PTR 88[rsp], 0
	mov	BYTE PTR [rax+r12], 0
	mov	r12, QWORD PTR 168[rsp]
	je	.L2252
	mov	rax, QWORD PTR 160[rsp]
	mov	rsi, QWORD PTR 80[rsp]
	mov	BYTE PTR [rax+rsi], 46
	mov	r12, QWORD PTR 168[rsp]
	jmp	.L2252
.L2227:
	mov	rcx, QWORD PTR 56[rsp]
	add	rcx, 1
	js	.L2228
.L2229:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r9, QWORD PTR 168[rsp]
	mov	rsi, rax
	mov	r14, QWORD PTR 160[rsp]
	lea	r8, 1[r9]
	test	r9, r9
	je	.L2428
	test	r8, r8
	jne	.L2234
	cmp	r14, rbp
	je	.L2429
.L2231:
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, r14
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 168[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	rax, QWORD PTR 56[rsp]
	test	r9, r9
	mov	QWORD PTR 176[rsp], rax
	jne	.L2223
.L2225:
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L2232
	mov	r10, QWORD PTR 160[rsp]
	cmp	r10, rbp
	je	.L2299
.L2237:
	mov	rax, QWORD PTR 176[rsp]
	cmp	rax, r12
	jnb	.L2238
	add	rax, rax
	cmp	r12, rax
	jnb	.L2239
	lea	rcx, 1[rax]
	test	rax, rax
	mov	r14, r12
	mov	r12, rax
	jns	.L2247
.L2246:
	lea	rsi, 160[rsp]
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L2183:
	mov	rcx, QWORD PTR 64[rsp]
	add	rcx, 1
	jns	.L2185
.L2184:
	lea	rsi, 160[rsp]
	call	_ZSt17__throw_bad_allocv
.L2419:
	mov	eax, DWORD PTR 56[rsp]
	mov	DWORD PTR 32[rsp], r14d
	movaps	xmm3, xmm6
	mov	rcx, r13
	mov	DWORD PTR 40[rsp], eax
	call	_ZSt8to_charsPcS_fSt12chars_formati
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
	jmp	.L2200
.L2173:
	mov	rax, QWORD PTR 56[rsp]
	cmp	r14d, 2
	mov	BYTE PTR 72[rsp], 1
	lea	rsi, 128[rax]
	mov	QWORD PTR 64[rsp], rsi
	jne	.L2178
	cvttss2si	eax, xmm6
	pxor	xmm0, xmm0
	cdq
	xor	eax, edx
	sub	eax, edx
	cvtsi2sd	xmm0, eax
	call	log10
	cvttsd2si	edx, xmm0
	mov	eax, edx
	sar	eax
	cmp	edx, 1
	mov	edx, 1
	cdqe
	cmovle	rax, rdx
	add	rsi, rax
	mov	QWORD PTR 64[rsp], rsi
	jmp	.L2178
.L2242:
	test	r12, r12
	je	.L2244
	cmp	r12, 1
	je	.L2430
	mov	rcx, r10
	mov	r8, r12
	mov	rdx, r13
	call	memcpy
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L2244
.L2398:
	mov	rax, QWORD PTR 80[rsp]
	mov	rcx, rdx
	mov	r8, r12
	lea	rsi, 0[r13+rax]
	add	rcx, rax
	sub	r8, rax
	add	rcx, r13
	mov	rdx, rsi
	call	memmove
	cmp	BYTE PTR 88[rsp], 0
	je	.L2219
	mov	rax, QWORD PTR 80[rsp]
	mov	BYTE PTR [rsi], 46
	lea	rsi, 1[r13+rax]
.L2219:
	mov	r8, r15
	mov	edx, 48
	mov	rcx, rsi
	call	memset
	movzx	r9d, BYTE PTR [rbx]
	mov	r12, QWORD PTR 56[rsp]
	jmp	.L2209
.L2311:
	mov	QWORD PTR 64[rsp], 30
	mov	ecx, 31
.L2191:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r8, QWORD PTR 168[rsp]
	mov	r9, rax
	mov	rsi, QWORD PTR 160[rsp]
	cmp	r8, 1
	je	.L2431
	test	r8, r8
	je	.L2391
	mov	rdx, rsi
	mov	rcx, rax
	call	memcpy
	mov	r9, rax
.L2391:
	cmp	rsi, rbp
	je	.L2196
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 80[rsp]
.L2196:
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 160[rsp], r9
	mov	QWORD PTR 176[rsp], rax
	jmp	.L2192
.L2310:
	mov	eax, 15
	jmp	.L2180
.L2418:
	test	rsi, rsi
	js	.L2193
	lea	rcx, 1[rsi]
	jmp	.L2191
.L2260:
	mov	rax, QWORD PTR 72[rsp]
	lea	rsi, 160[rsp]
	xor	r9d, r9d
	xor	r8d, r8d
	mov	r15, QWORD PTR 80[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 32[rsp], rax
	mov	rdx, r15
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rcx, QWORD PTR 160[rsp]
	add	rcx, r15
	jmp	.L2261
.L2423:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r9], al
	jmp	.L2389
.L2428:
	movzx	eax, BYTE PTR [r14]
	cmp	r14, rbp
	mov	BYTE PTR [rsi], al
	jne	.L2231
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	QWORD PTR 176[rsp], rax
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L2232
	mov	r10, rsi
	jmp	.L2237
.L2403:
	movabs	rax, 9223372036854775807
	sub	rax, r12
	cmp	rax, r15
	jb	.L2432
	mov	rax, QWORD PTR 160[rsp]
	lea	r13, [r12+r15]
	cmp	rax, rbp
	je	.L2321
	mov	rdx, QWORD PTR 176[rsp]
.L2254:
	cmp	rdx, r13
	jb	.L2433
.L2255:
	lea	rcx, [rax+r12]
	cmp	r15, 1
	je	.L2434
	mov	r8, r15
	mov	edx, 48
	call	memset
.L2257:
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 168[rsp], r13
	mov	BYTE PTR [rax+r13], 0
	mov	r12, QWORD PTR 168[rsp]
	jmp	.L2252
.L2234:
	mov	rdx, r14
	mov	rcx, rax
	mov	QWORD PTR 64[rsp], r9
	call	memcpy
	cmp	r14, rbp
	mov	r9, QWORD PTR 64[rsp]
	jne	.L2231
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	QWORD PTR 176[rsp], rax
	jmp	.L2223
.L2416:
	movzx	eax, BYTE PTR 240[rsp]
	mov	BYTE PTR [rcx], al
	mov	r8, QWORD PTR 232[rsp]
	mov	rcx, QWORD PTR 192[rsp]
	jmp	.L2270
.L2431:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r9], al
	jmp	.L2391
.L2402:
	lea	rsi, 160[rsp]
	mov	edx, 46
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	jmp	.L2250
.L2222:
	mov	rax, QWORD PTR 56[rsp]
	cmp	rax, 15
	jbe	.L2223
.L2395:
	test	rax, rax
	js	.L2294
	cmp	rax, 29
	ja	.L2227
	mov	QWORD PTR 56[rsp], 30
.L2295:
	mov	rax, QWORD PTR 56[rsp]
	lea	rcx, 1[rax]
	jmp	.L2229
.L2322:
	mov	edx, 15
	jmp	.L2259
.L2427:
	mov	BYTE PTR [rcx], 48
	jmp	.L2264
.L2426:
	movzx	edx, BYTE PTR [rcx]
	mov	BYTE PTR [rax], dl
	mov	rcx, QWORD PTR 160[rsp]
	add	rcx, rsi
	jmp	.L2261
.L2430:
	movzx	eax, BYTE PTR 0[r13]
	mov	BYTE PTR [r10], al
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L2244
.L2433:
	mov	QWORD PTR 32[rsp], r15
	xor	r9d, r9d
	xor	r8d, r8d
	mov	rdx, r12
	lea	rsi, 160[rsp]
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE48:
	mov	rax, QWORD PTR 160[rsp]
	jmp	.L2255
.L2412:
	mov	rax, QWORD PTR [r14]
	mov	rcx, r14
.LEHB49:
	call	[QWORD PTR [rax]]
.LEHE49:
	jmp	.L2286
.L2421:
	cmp	r12, 29
	ja	.L2239
	lea	rsi, 160[rsp]
	mov	ecx, 31
.LEHB50:
	call	_Znwy
	mov	r14, r12
	mov	r10, rax
	mov	r12d, 30
	jmp	.L2240
.L2434:
	mov	BYTE PTR [rcx], 48
	jmp	.L2257
.L2321:
	mov	edx, 15
	jmp	.L2254
.L2429:
	mov	QWORD PTR 160[rsp], rax
	mov	rax, QWORD PTR 56[rsp]
	mov	r9, -1
	mov	QWORD PTR 176[rsp], rax
	jmp	.L2235
.L2401:
	movzx	eax, BYTE PTR 0[r13]
	mov	rsi, r12
	mov	r12d, 1
	mov	BYTE PTR [r10], al
	jmp	.L2248
.L2400:
	mov	QWORD PTR 56[rsp], rax
	jmp	.L2295
.L2422:
	lea	rcx, .LC9[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2193:
	lea	rcx, .LC9[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2294:
	lea	rcx, .LC9[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2425:
	lea	rcx, .LC27[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2424:
	lea	rdx, .LC28[rip]
	mov	r8, rax
	lea	rcx, .LC29[rip]
	lea	rsi, 160[rsp]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L2232:
	lea	rcx, .LC26[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2432:
	lea	rcx, .LC27[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.LEHE50:
.L2163:
	xor	r14d, r14d
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L2171
.L2337:
	mov	rbx, rax
.L2293:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB51:
	call	_Unwind_Resume
.LEHE51:
.L2339:
	mov	rbx, rax
	jmp	.L2291
.L2338:
	mov	rcx, r14
	mov	rbx, rax
	call	_ZNSt6localeD1Ev
.L2291:
	lea	rcx, 192[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	cmp	BYTE PTR 152[rsp], 0
	je	.L2292
	lea	rcx, 144[rsp]
	call	_ZNSt6localeD1Ev
.L2292:
	lea	rsi, 160[rsp]
	jmp	.L2293
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4914:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4914-.LLSDACSB4914
.LLSDACSB4914:
	.uleb128 .LEHB43-.LFB4914
	.uleb128 .LEHE43-.LEHB43
	.uleb128 .L2337-.LFB4914
	.uleb128 0
	.uleb128 .LEHB44-.LFB4914
	.uleb128 .LEHE44-.LEHB44
	.uleb128 .L2338-.LFB4914
	.uleb128 0
	.uleb128 .LEHB45-.LFB4914
	.uleb128 .LEHE45-.LEHB45
	.uleb128 .L2339-.LFB4914
	.uleb128 0
	.uleb128 .LEHB46-.LFB4914
	.uleb128 .LEHE46-.LEHB46
	.uleb128 .L2337-.LFB4914
	.uleb128 0
	.uleb128 .LEHB47-.LFB4914
	.uleb128 .LEHE47-.LEHB47
	.uleb128 .L2339-.LFB4914
	.uleb128 0
	.uleb128 .LEHB48-.LFB4914
	.uleb128 .LEHE48-.LEHB48
	.uleb128 .L2337-.LFB4914
	.uleb128 0
	.uleb128 .LEHB49-.LFB4914
	.uleb128 .LEHE49-.LEHB49
	.uleb128 .L2339-.LFB4914
	.uleb128 0
	.uleb128 .LEHB50-.LFB4914
	.uleb128 .LEHE50-.LEHB50
	.uleb128 .L2337-.LFB4914
	.uleb128 0
	.uleb128 .LEHB51-.LFB4914
	.uleb128 .LEHE51-.LEHB51
	.uleb128 0
	.uleb128 0
.LLSDACSE4914:
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC35:
	.ascii "format error: format-spec contains invalid formatting options for 'bool'\0"
	.align 8
.LC36:
	.ascii "format error: format-spec contains invalid formatting options for 'charT'\0"
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
	.def	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE:
.LFB4677:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 168
	.seh_stackalloc	168
	.seh_endprologue
	mov	rbx, rdx
	movzx	r8d, r8b
	mov	rsi, rcx
	lea	rdx, .L2438[rip]
	movsx	rax, DWORD PTR [rdx+r8*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2438:
	.long	.L2453-.L2438
	.long	.L2452-.L2438
	.long	.L2451-.L2438
	.long	.L2450-.L2438
	.long	.L2449-.L2438
	.long	.L2448-.L2438
	.long	.L2447-.L2438
	.long	.L2446-.L2438
	.long	.L2445-.L2438
	.long	.L2444-.L2438
	.long	.L2443-.L2438
	.long	.L2442-.L2438
	.long	.L2441-.L2438
	.long	.L2440-.L2438
	.long	.L2439-.L2438
	.long	.L2437-.L2438
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2439:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	r8d, 1
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	movdqa	xmm2, XMMWORD PTR [rsi]
	lea	rdx, 48[rsp]
	mov	rcx, rdi
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	movaps	XMMWORD PTR 48[rsp], xmm2
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
.L2435:
	add	rsp, 168
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L2437:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	r8d, 1
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	movdqa	xmm3, XMMWORD PTR [rsi]
	lea	rdx, 48[rsp]
	mov	rcx, rdi
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	movaps	XMMWORD PTR 48[rsp], xmm3
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatIoNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
.L2473:
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 168
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L2452:
	mov	rbp, QWORD PTR [rbx]
	xor	r8d, r8d
	mov	DWORD PTR 136[rsp], 0
	lea	rdi, 128[rsp]
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	mov	rcx, rdi
	lea	rdx, 8[rbp]
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	test	BYTE PTR 129[rsp], 120
	jne	.L2454
	test	BYTE PTR 128[rsp], 92
	jne	.L2475
.L2454:
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rdi
	movzx	edx, BYTE PTR [rsi]
	mov	rbx, QWORD PTR 48[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L2435
	.p2align 4,,10
	.p2align 3
.L2451:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	r8d, 7
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	movzx	edx, BYTE PTR 129[rsp]
	mov	ecx, edx
	not	edx
	and	ecx, 120
	and	edx, 56
	jne	.L2456
	test	BYTE PTR 128[rsp], 92
	jne	.L2476
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	cmp	cl, 120
	mov	rbx, QWORD PTR 48[rax]
	jne	.L2477
	mov	rax, QWORD PTR 16[rbx]
	jmp	.L2473
	.p2align 4,,10
	.p2align 3
.L2449:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	r8d, 1
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	edx, DWORD PTR [rsi]
	mov	rcx, rdi
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatIjNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L2435
	.p2align 4,,10
	.p2align 3
.L2448:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	r8d, 1
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	rdx, QWORD PTR [rsi]
	mov	rcx, rdi
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatIxNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L2435
	.p2align 4,,10
	.p2align 3
.L2450:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	r8d, 1
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	edx, DWORD PTR [rsi]
	mov	rcx, rdi
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L2435
	.p2align 4,,10
	.p2align 3
.L2447:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	r8d, 1
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	rdx, QWORD PTR [rsi]
	mov	rcx, rdi
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatIyNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L2435
	.p2align 4,,10
	.p2align 3
.L2446:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	movss	xmm1, DWORD PTR [rsi]
	mov	rcx, rdi
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	mov	r8, rbx
	call	_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L2435
	.p2align 4,,10
	.p2align 3
.L2445:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	movsd	xmm1, QWORD PTR [rsi]
	mov	rcx, rdi
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	mov	r8, rbx
	call	_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L2435
	.p2align 4,,10
	.p2align 3
.L2444:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	lea	rdx, 64[rsp]
	mov	rcx, rdi
	fld	TBYTE PTR [rsi]
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	fstp	TBYTE PTR 64[rsp]
	mov	r8, rbx
	call	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L2435
	.p2align 4,,10
	.p2align 3
.L2443:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE
	mov	QWORD PTR 8[rbp], rax
	mov	rsi, QWORD PTR [rsi]
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rsi
	mov	rbx, QWORD PTR 48[rax]
	call	strlen
	mov	QWORD PTR 88[rsp], rsi
	mov	QWORD PTR 80[rsp], rax
.L2474:
	lea	rdx, 80[rsp]
	mov	r8, rbx
	mov	rcx, rdi
	call	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 168
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L2442:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 128[rsp]
	mov	DWORD PTR 136[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 136[rsp], 32
	mov	QWORD PTR 128[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE
	movdqu	xmm0, XMMWORD PTR [rsi]
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	movaps	XMMWORD PTR 80[rsp], xmm0
	jmp	.L2474
	.p2align 4,,10
	.p2align 3
.L2441:
	mov	rbp, QWORD PTR [rbx]
	lea	rdi, 100[rsp]
	mov	DWORD PTR 108[rsp], 0
	mov	rcx, rdi
	mov	BYTE PTR 108[rsp], 32
	mov	QWORD PTR 100[rsp], 0
	lea	rdx, 8[rbp]
	call	_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 48[rax]
	mov	rax, QWORD PTR [rsi]
	test	rax, rax
	jne	.L2462
	mov	BYTE PTR 130[rsp], 48
	mov	edx, 3
.L2463:
	mov	eax, 30768
	mov	r9, rdi
	mov	r8, rbx
	mov	QWORD PTR 80[rsp], rdx
	mov	WORD PTR 128[rsp], ax
	lea	rcx, 80[rsp]
	lea	rax, 128[rsp]
	mov	DWORD PTR 32[rsp], 2
	mov	QWORD PTR 88[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	mov	QWORD PTR 16[rbx], rax
	jmp	.L2435
	.p2align 4,,10
	.p2align 3
.L2440:
	mov	rcx, QWORD PTR [rbx]
	mov	rax, QWORD PTR 8[rsi]
	mov	r8, QWORD PTR [rsi]
	mov	rdx, QWORD PTR 48[rcx]
	add	rcx, 8
	add	rsp, 168
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L2462:
	movabs	rsi, 3978425819141910832
	bsr	rdx, rax
	lea	r8d, 4[rdx]
	mov	QWORD PTR 112[rsp], rsi
	movabs	rsi, 7378413942531504440
	shr	r8d, 2
	cmp	rax, 255
	mov	QWORD PTR 120[rsp], rsi
	lea	edx, -1[r8]
	jbe	.L2464
	.p2align 4,,10
	.p2align 3
.L2465:
	mov	r10, rax
	mov	ecx, edx
	and	r10d, 15
	movzx	r10d, BYTE PTR 112[rsp+r10]
	mov	BYTE PTR 130[rsp+rcx], r10b
	lea	r10d, -1[rdx]
	mov	rcx, rax
	shr	rax, 8
	shr	rcx, 4
	sub	edx, 2
	and	ecx, 15
	cmp	rax, 255
	movzx	ecx, BYTE PTR 112[rsp+rcx]
	mov	BYTE PTR 130[rsp+r10], cl
	ja	.L2465
.L2464:
	cmp	rax, 15
	jbe	.L2466
	mov	rdx, rax
	shr	rax, 4
	and	edx, 15
	movzx	edx, BYTE PTR 112[rsp+rdx]
	mov	BYTE PTR 131[rsp], dl
	movzx	eax, BYTE PTR 112[rsp+rax]
.L2467:
	mov	BYTE PTR 130[rsp], al
	lea	edx, 2[r8]
	jmp	.L2463
	.p2align 4,,10
	.p2align 3
.L2456:
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	test	cl, cl
	movsx	edx, BYTE PTR [rsi]
	mov	rbx, QWORD PTR 48[rax]
	jne	.L2460
	mov	BYTE PTR 112[rsp], dl
	lea	rax, 112[rsp]
	mov	r9, rdi
	mov	r8, rbx
	lea	rcx, 80[rsp]
	mov	edx, 1
	mov	DWORD PTR 32[rsp], 1
	mov	QWORD PTR 80[rsp], 1
	mov	QWORD PTR 88[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	jmp	.L2473
.L2477:
	movsx	edx, BYTE PTR [rsi]
.L2460:
	mov	r8, rbx
	mov	rcx, rdi
	call	_ZNKSt8__format15__formatter_intIcE6formatIcNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	jmp	.L2473
	.p2align 4,,10
	.p2align 3
.L2466:
	movzx	eax, BYTE PTR 112[rsp+rax]
	jmp	.L2467
.L2476:
	lea	rcx, .LC36[rip]
	call	_ZSt20__throw_format_errorPKc
.L2453:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
.L2475:
	lea	rcx, .LC35[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEy
	.def	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEy
_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEy:
.LFB4674:
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	mov	r9, QWORD PTR 48[rcx]
	mov	rax, rcx
	movzx	ecx, BYTE PTR [r9]
	mov	r8d, ecx
	and	ecx, 15
	and	r8d, 15
	cmp	rdx, rcx
	jb	.L2482
	test	r8b, r8b
	je	.L2483
	xor	r8d, r8d
.L2480:
	mov	QWORD PTR 40[rsp], rax
	mov	rax, QWORD PTR 48[rsp]
	lea	rdx, 40[rsp]
	mov	BYTE PTR 64[rsp], r8b
	lea	rcx, 80[rsp]
	movzx	r8d, r8b
	mov	QWORD PTR 80[rsp], rax
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 88[rsp], rax
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 96[rsp], rax
	mov	rax, QWORD PTR 72[rsp]
	mov	QWORD PTR 104[rsp], rax
	call	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
	nop
	add	rsp, 120
	ret
	.p2align 4,,10
	.p2align 3
.L2483:
	mov	rcx, QWORD PTR [r9]
	shr	rcx, 4
	cmp	rdx, rcx
	jnb	.L2480
	sal	rdx, 5
	add	rdx, QWORD PTR 8[r9]
	mov	rcx, QWORD PTR [rdx]
	movzx	r8d, BYTE PTR 16[rdx]
	mov	QWORD PTR 48[rsp], rcx
	mov	rcx, QWORD PTR 8[rdx]
	mov	QWORD PTR 56[rsp], rcx
	jmp	.L2480
	.p2align 4,,10
	.p2align 3
.L2482:
	mov	r8, QWORD PTR [r9]
	lea	rcx, [rdx+rdx*4]
	sal	rdx, 4
	add	rdx, QWORD PTR 8[r9]
	shr	r8, 4
	shr	r8, cl
	mov	rcx, QWORD PTR [rdx]
	mov	rdx, QWORD PTR 8[rdx]
	and	r8d, 31
	mov	QWORD PTR 48[rsp], rcx
	mov	QWORD PTR 56[rsp], rdx
	jmp	.L2480
	.seh_endproc
	.section .rdata,"dr"
	.align 32
CSWTCH.756:
	.long	3
	.long	0
	.long	0
	.long	0
	.long	0
	.long	0
	.long	0
	.long	0
	.long	0
	.long	0
	.long	0
	.long	1
	.long	0
	.long	2
	.globl	_ZTSSt9exception
	.section	.rdata$_ZTSSt9exception,"dr"
	.linkonce same_size
	.align 8
_ZTSSt9exception:
	.ascii "St9exception\0"
	.globl	_ZTISt9exception
	.section	.rdata$_ZTISt9exception,"dr"
	.linkonce same_size
	.align 8
_ZTISt9exception:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSSt9exception
	.globl	_ZTSSt13runtime_error
	.section	.rdata$_ZTSSt13runtime_error,"dr"
	.linkonce same_size
	.align 16
_ZTSSt13runtime_error:
	.ascii "St13runtime_error\0"
	.globl	_ZTISt13runtime_error
	.section	.rdata$_ZTISt13runtime_error,"dr"
	.linkonce same_size
	.align 8
_ZTISt13runtime_error:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt13runtime_error
	.quad	_ZTISt9exception
	.globl	_ZTSSt12format_error
	.section	.rdata$_ZTSSt12format_error,"dr"
	.linkonce same_size
	.align 16
_ZTSSt12format_error:
	.ascii "St12format_error\0"
	.globl	_ZTISt12format_error
	.section	.rdata$_ZTISt12format_error,"dr"
	.linkonce same_size
	.align 8
_ZTISt12format_error:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt12format_error
	.quad	_ZTISt13runtime_error
	.globl	_ZTSNSt8__format5_SinkIcEE
	.section	.rdata$_ZTSNSt8__format5_SinkIcEE,"dr"
	.linkonce same_size
	.align 16
_ZTSNSt8__format5_SinkIcEE:
	.ascii "NSt8__format5_SinkIcEE\0"
	.globl	_ZTINSt8__format5_SinkIcEE
	.section	.rdata$_ZTINSt8__format5_SinkIcEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt8__format5_SinkIcEE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSNSt8__format5_SinkIcEE
	.globl	_ZTSNSt8__format9_Buf_sinkIcEE
	.section	.rdata$_ZTSNSt8__format9_Buf_sinkIcEE,"dr"
	.linkonce same_size
	.align 16
_ZTSNSt8__format9_Buf_sinkIcEE:
	.ascii "NSt8__format9_Buf_sinkIcEE\0"
	.globl	_ZTINSt8__format9_Buf_sinkIcEE
	.section	.rdata$_ZTINSt8__format9_Buf_sinkIcEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt8__format9_Buf_sinkIcEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt8__format9_Buf_sinkIcEE
	.quad	_ZTINSt8__format5_SinkIcEE
	.globl	_ZTSNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE
	.section	.rdata$_ZTSNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE,"dr"
	.linkonce same_size
	.align 32
_ZTSNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE:
	.ascii "NSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE\0"
	.globl	_ZTINSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE
	.section	.rdata$_ZTINSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE
	.quad	_ZTINSt8__format9_Buf_sinkIcEE
	.globl	_ZTSNSt8__format8_ScannerIcEE
	.section	.rdata$_ZTSNSt8__format8_ScannerIcEE,"dr"
	.linkonce same_size
	.align 16
_ZTSNSt8__format8_ScannerIcEE:
	.ascii "NSt8__format8_ScannerIcEE\0"
	.globl	_ZTINSt8__format8_ScannerIcEE
	.section	.rdata$_ZTINSt8__format8_ScannerIcEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt8__format8_ScannerIcEE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSNSt8__format8_ScannerIcEE
	.globl	_ZTSNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE
	.section	.rdata$_ZTSNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE,"dr"
	.linkonce same_size
	.align 32
_ZTSNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE:
	.ascii "NSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE\0"
	.globl	_ZTINSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE
	.section	.rdata$_ZTINSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE
	.quad	_ZTINSt8__format9_Buf_sinkIcEE
	.globl	_ZTSNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE
	.section	.rdata$_ZTSNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE,"dr"
	.linkonce same_size
	.align 32
_ZTSNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE:
	.ascii "NSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE\0"
	.globl	_ZTINSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE
	.section	.rdata$_ZTINSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE
	.quad	_ZTINSt8__format8_ScannerIcEE
	.globl	_ZTVSt12format_error
	.section	.rdata$_ZTVSt12format_error,"dr"
	.linkonce same_size
	.align 8
_ZTVSt12format_error:
	.quad	0
	.quad	_ZTISt12format_error
	.quad	_ZNSt12format_errorD1Ev
	.quad	_ZNSt12format_errorD0Ev
	.quad	_ZNKSt13runtime_error4whatEv
	.globl	_ZTVNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE
	.section	.rdata$_ZTVNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTVNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE:
	.quad	0
	.quad	_ZTINSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE
	.quad	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv
	.globl	_ZTVNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE
	.section	.rdata$_ZTVNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTVNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE:
	.quad	0
	.quad	_ZTINSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE
	.quad	_ZNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEE11_M_overflowEv
	.globl	_ZTVNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE
	.section	.rdata$_ZTVNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE,"dr"
	.linkonce same_size
	.align 8
_ZTVNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE:
	.quad	0
	.quad	_ZTINSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE
	.quad	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc
	.quad	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEy
	.globl	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE
	.section	.rdata$_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE,"dr"
	.linkonce same_size
	.align 32
_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE:
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	0
	.byte	1
	.byte	2
	.byte	3
	.byte	4
	.byte	5
	.byte	6
	.byte	7
	.byte	8
	.byte	9
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	10
	.byte	11
	.byte	12
	.byte	13
	.byte	14
	.byte	15
	.byte	16
	.byte	17
	.byte	18
	.byte	19
	.byte	20
	.byte	21
	.byte	22
	.byte	23
	.byte	24
	.byte	25
	.byte	26
	.byte	27
	.byte	28
	.byte	29
	.byte	30
	.byte	31
	.byte	32
	.byte	33
	.byte	34
	.byte	35
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	10
	.byte	11
	.byte	12
	.byte	13
	.byte	14
	.byte	15
	.byte	16
	.byte	17
	.byte	18
	.byte	19
	.byte	20
	.byte	21
	.byte	22
	.byte	23
	.byte	24
	.byte	25
	.byte	26
	.byte	27
	.byte	28
	.byte	29
	.byte	30
	.byte	31
	.byte	32
	.byte	33
	.byte	34
	.byte	35
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.byte	127
	.section .rdata,"dr"
	.align 16
.LC11:
	.quad	0
	.quad	-1
	.align 16
.LC25:
	.long	-1
	.long	-1
	.long	32766
	.long	0
	.align 16
.LC31:
	.long	-1
	.long	2147483647
	.long	0
	.long	0
	.align 8
.LC32:
	.long	-1
	.long	2146435071
	.align 16
.LC33:
	.long	2147483647
	.long	0
	.long	0
	.long	0
	.align 4
.LC34:
	.long	2139095039
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSt13runtime_errorD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	_ZNSt13runtime_errorC2EPKc;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.def	__cxa_free_exception;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	memchr;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6localeD1Ev;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6localeC1ERKS_;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt6locale4nameB5cxx11Ev;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt6locale2id5_M_idEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6localeaSERKS_;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6localeC1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	toupper;	.scl	2;	.type	32;	.endef
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy;	.scl	2;	.type	32;	.endef
	.def	_ZSt24__throw_out_of_range_fmtPKcz;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6locale7classicEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt6localeeqERKS_;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_e;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_eSt12chars_format;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_eSt12chars_formati;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	log10;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_d;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_dSt12chars_format;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_dSt12chars_formati;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_f;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_fSt12chars_format;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_fSt12chars_formati;	.scl	2;	.type	32;	.endef
	.def	strlen;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt13runtime_error4whatEv;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZNSt7__cxx118numpunctIcE2idE, "dr"
	.globl	.refptr._ZNSt7__cxx118numpunctIcE2idE
	.linkonce	discard
.refptr._ZNSt7__cxx118numpunctIcE2idE:
	.quad	_ZNSt7__cxx118numpunctIcE2idE
