	.file	"s.cpp"
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
.LFB3271:
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
.LFB3272:
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
.LFB5234:
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
.LFB49:
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
	.section	.text$_ZSt20__throw_format_errorPKc,"x"
	.linkonce discard
	.globl	_ZSt20__throw_format_errorPKc
	.def	_ZSt20__throw_format_errorPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt20__throw_format_errorPKc
_ZSt20__throw_format_errorPKc:
.LFB3268:
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
.L22:
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
.LLSDA3268:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3268-.LLSDACSB3268
.LLSDACSB3268:
	.uleb128 .LEHB0-.LFB3268
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L22-.LFB3268
	.uleb128 0
	.uleb128 .LEHB1-.LFB3268
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE3268:
	.section	.text$_ZSt20__throw_format_errorPKc,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "format error: conflicting indexing style in format string\0"
	.section	.text$_ZNSt8__format39__conflicting_indexing_in_format_stringEv,"x"
	.linkonce discard
	.globl	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
	.def	_ZNSt8__format39__conflicting_indexing_in_format_stringEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
_ZNSt8__format39__conflicting_indexing_in_format_stringEv:
.LFB3275:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC1:
	.ascii "format error: invalid arg-id in format string\0"
	.section	.text$_ZNSt8__format33__invalid_arg_id_in_format_stringEv,"x"
	.linkonce discard
	.globl	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.def	_ZNSt8__format33__invalid_arg_id_in_format_stringEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
_ZNSt8__format33__invalid_arg_id_in_format_stringEv:
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
	.ascii "format error: failed to parse format-spec\0"
	.section	.text$_ZNSt8__format29__failed_to_parse_format_specEv,"x"
	.linkonce discard
	.globl	_ZNSt8__format29__failed_to_parse_format_specEv
	.def	_ZNSt8__format29__failed_to_parse_format_specEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format29__failed_to_parse_format_specEv
_ZNSt8__format29__failed_to_parse_format_specEv:
.LFB3277:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, .LC2[rip]
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
.LFB4431:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L26
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L26:
	ret
	.seh_endproc
	.section	.text$_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	.def	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_:
.LFB4568:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	xor	eax, eax
	mov	r10d, 32
	mov	r11, rcx
	mov	rbx, rdx
	mov	r9, rdx
	jmp	.L37
	.p2align 4,,10
	.p2align 3
.L42:
	lea	eax, [rax+rax*4]
	add	r9, 1
	movzx	ecx, cl
	lea	eax, [rcx+rax*2]
	cmp	r8, r9
	je	.L29
.L37:
	movzx	edx, BYTE PTR [r9]
	lea	ecx, -48[rdx]
	cmp	cl, 9
	ja	.L29
	sub	r10d, 4
	jns	.L42
	mov	edx, 10
	mul	edx
	jo	.L34
	movzx	ecx, cl
	add	ecx, eax
	jc	.L34
	add	r9, 1
	mov	eax, ecx
	cmp	r8, r9
	jne	.L37
.L29:
	cmp	rbx, r9
	je	.L34
	cmp	eax, 65535
	ja	.L34
	mov	WORD PTR [r11], ax
	mov	rax, r11
	mov	QWORD PTR 8[r11], r9
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L34:
	mov	rax, r11
	mov	QWORD PTR [r11], 0
	mov	QWORD PTR 8[r11], 0
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC3:
	.ascii "format error: unmatched '{' in format string\0"
	.align 8
.LC4:
	.ascii "format error: unmatched '}' in format string\0"
	.section	.text$_ZNSt8__format8_ScannerIcE7_M_scanEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format8_ScannerIcE7_M_scanEv
	.def	_ZNSt8__format8_ScannerIcE7_M_scanEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format8_ScannerIcE7_M_scanEv
_ZNSt8__format8_ScannerIcE7_M_scanEv:
.LFB3909:
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
	je	.L110
	test	rdi, rdi
	jne	.L45
.L43:
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
.L110:
	cmp	BYTE PTR [rbx], 123
	je	.L111
.L45:
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
	je	.L52
	.p2align 4,,10
	.p2align 3
.L51:
	cmp	r14, rsi
	jnb	.L112
	lea	rax, 1[r14]
	cmp	rax, rdi
	je	.L56
	cmp	rsi, -1
	movzx	ebp, BYTE PTR 1[rbx+r14]
	je	.L113
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
	je	.L114
	movzx	eax, BYTE PTR 1[rdi]
	cmp	al, 125
	je	.L115
	cmp	al, 58
	je	.L116
	lea	rcx, 2[rdi]
	xor	edx, edx
	cmp	al, 48
	je	.L65
	lea	edx, -49[rax]
	cmp	dl, 8
	ja	.L66
	lea	rcx, 2[rdi]
	movzx	edx, BYTE PTR 2[rdi]
	cmp	r15, rcx
	je	.L67
	sub	edx, 48
	cmp	dl, 9
	jbe	.L68
.L67:
	movsx	dx, al
	sub	edx, 48
.L65:
	movzx	eax, BYTE PTR [rcx]
	cmp	al, 125
	jne	.L117
.L71:
	cmp	DWORD PTR 24[r13], 2
	movzx	edx, dx
	je	.L46
	xor	eax, eax
	mov	DWORD PTR 24[r13], 1
	cmp	BYTE PTR [rcx], 58
	sete	al
	add	rcx, rax
	mov	QWORD PTR 8[r13], rcx
.L62:
	mov	rax, QWORD PTR 0[r13]
	mov	rcx, r13
	call	[QWORD PTR 8[rax]]
	mov	rax, QWORD PTR 8[r13]
	mov	r15, QWORD PTR 16[r13]
	lea	rbx, 1[rax]
	mov	rdi, r15
	mov	QWORD PTR 8[r13], rbx
	sub	rdi, rbx
	je	.L43
	mov	r8, rdi
	mov	edx, 123
	mov	rcx, rbx
	call	memchr
	test	rax, rax
	mov	r14, rax
	je	.L73
	sub	r14, rbx
.L109:
	mov	r8, rdi
	mov	edx, 125
	mov	rcx, rbx
	call	memchr
	test	rax, rax
	mov	rsi, rax
	je	.L87
.L82:
	sub	rsi, rbx
.L60:
	cmp	rsi, r14
	jne	.L51
.L52:
	mov	rax, QWORD PTR 0[r13]
	mov	rdx, r15
	mov	rcx, r13
	call	[QWORD PTR [rax]]
	mov	rax, QWORD PTR 16[r13]
	mov	QWORD PTR 8[r13], rax
	jmp	.L43
	.p2align 4,,10
	.p2align 3
.L112:
	lea	rbp, 1[rsi]
	cmp	rbp, rdi
	je	.L74
	cmp	BYTE PTR 1[rbx+rsi], 125
	jne	.L74
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
	je	.L118
	test	rdi, rdi
	je	.L43
	sub	r14, 1
	sub	r14, rbp
	jmp	.L109
	.p2align 4,,10
	.p2align 3
.L118:
	test	rdi, rdi
	je	.L43
	mov	r8, rdi
	mov	edx, 125
	mov	rcx, rbx
	call	memchr
	test	rax, rax
	mov	rsi, rax
	jne	.L82
	jmp	.L52
	.p2align 4,,10
	.p2align 3
.L113:
	cmp	bpl, 123
	jne	.L56
	add	rax, QWORD PTR 8[r13]
	mov	rcx, r13
	mov	rbx, rax
	mov	rax, QWORD PTR 0[r13]
	mov	rdx, rbx
	add	rbx, 1
	call	[QWORD PTR [rax]]
	mov	r15, QWORD PTR 16[r13]
	mov	QWORD PTR 8[r13], rbx
.L79:
	mov	rdi, r15
	sub	rdi, rbx
	je	.L43
	mov	r8, rdi
	mov	edx, 123
	mov	rcx, rbx
	call	memchr
	mov	r14, rax
	sub	r14, rbx
	test	rax, rax
	cmove	r14, r12
	jmp	.L60
	.p2align 4,,10
	.p2align 3
.L114:
	sub	rsi, 2
	sub	rsi, r14
	jmp	.L79
	.p2align 4,,10
	.p2align 3
.L87:
	mov	rsi, -1
	jmp	.L60
	.p2align 4,,10
	.p2align 3
.L117:
	cmp	al, 58
	je	.L71
.L66:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L115:
	cmp	DWORD PTR 24[r13], 1
	je	.L46
	mov	rdx, QWORD PTR 32[r13]
	mov	DWORD PTR 24[r13], 2
	lea	rax, 1[rdx]
	mov	QWORD PTR 32[r13], rax
	jmp	.L62
	.p2align 4,,10
	.p2align 3
.L116:
	cmp	DWORD PTR 24[r13], 1
	je	.L46
	mov	rdx, QWORD PTR 32[r13]
	add	rdi, 2
	mov	DWORD PTR 24[r13], 2
	mov	QWORD PTR 8[r13], rdi
	lea	rax, 1[rdx]
	mov	QWORD PTR 32[r13], rax
	jmp	.L62
	.p2align 4,,10
	.p2align 3
.L111:
	cmp	BYTE PTR 1[rbx], 125
	jne	.L45
	add	rbx, 1
	mov	rax, QWORD PTR [rcx]
	cmp	DWORD PTR 24[rcx], 1
	mov	QWORD PTR 8[rcx], rbx
	mov	rax, QWORD PTR 8[rax]
	je	.L46
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
.L68:
	lea	rcx, 32[rsp]
	mov	rdx, rbx
	mov	r8, r15
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	mov	rcx, QWORD PTR 40[rsp]
	movzx	edx, WORD PTR 32[rsp]
	test	rcx, rcx
	je	.L66
	movzx	eax, BYTE PTR [rcx]
	cmp	al, 125
	je	.L71
	jmp	.L117
	.p2align 4,,10
	.p2align 3
.L73:
	mov	r8, rdi
	mov	edx, 125
	mov	rcx, rbx
	call	memchr
	test	rax, rax
	mov	rsi, rax
	je	.L52
	mov	r14, -1
	jmp	.L82
.L56:
	lea	rcx, .LC3[rip]
	call	_ZSt20__throw_format_errorPKc
.L46:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L74:
	lea	rcx, .LC4[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC5:
	.ascii "format error: width must be non-zero in format string\0"
	.align 8
.LC6:
	.ascii "format error: invalid width or precision in format-spec\0"
	.section	.text$_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	.def	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE:
.LFB4355:
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
	je	.L138
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	movzx	eax, dl
	cmp	BYTE PTR [rcx+rax], 9
	ja	.L121
	lea	rcx, 32[rsp]
	mov	rdx, rbx
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	mov	rax, QWORD PTR 40[rsp]
	mov	rdx, QWORD PTR 32[rsp]
	test	rax, rax
	je	.L139
	cmp	rbx, rax
	mov	WORD PTR 4[rsi], dx
	mov	ecx, 1
	je	.L119
.L123:
	movzx	edx, WORD PTR [rsi]
	and	ecx, 3
	sal	ecx, 7
	and	dx, -385
	or	edx, ecx
	mov	WORD PTR [rsi], dx
.L119:
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L121:
	cmp	dl, 123
	mov	rax, rbx
	jne	.L119
	lea	rax, 1[rbx]
	cmp	r8, rax
	je	.L140
	movsx	dx, BYTE PTR 1[rbx]
	cmp	dl, 125
	je	.L141
	cmp	dl, 48
	je	.L142
	lea	ecx, -49[rdx]
	cmp	cl, 8
	ja	.L132
	lea	r10, 2[rbx]
	cmp	r8, r10
	je	.L132
	movzx	ecx, BYTE PTR 2[rbx]
	sub	ecx, 48
	cmp	cl, 9
	ja	.L133
	lea	rcx, 32[rsp]
	mov	rdx, rax
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 96[rsp], r8
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzx	edx, WORD PTR 32[rsp]
	mov	rax, QWORD PTR 40[rsp]
	mov	r9, QWORD PTR 104[rsp]
	mov	r8, QWORD PTR 96[rsp]
.L130:
	cmp	r8, rax
	je	.L132
	test	rax, rax
	je	.L132
.L135:
	cmp	BYTE PTR [rax], 125
	jne	.L132
	cmp	DWORD PTR 16[r9], 2
	je	.L134
	mov	DWORD PTR 16[r9], 1
	mov	WORD PTR 4[rsi], dx
	jmp	.L128
	.p2align 4,,10
	.p2align 3
.L141:
	cmp	DWORD PTR 16[r9], 1
	je	.L134
	mov	rdx, QWORD PTR 24[r9]
	mov	DWORD PTR 16[r9], 2
	lea	rcx, 1[rdx]
	mov	QWORD PTR 24[r9], rcx
	mov	WORD PTR 4[rsi], dx
.L128:
	add	rax, 1
	cmp	rbx, rax
	je	.L119
	mov	ecx, 2
	jmp	.L123
	.p2align 4,,10
	.p2align 3
.L142:
	lea	rax, 2[rbx]
	xor	edx, edx
	jmp	.L130
	.p2align 4,,10
	.p2align 3
.L133:
	sub	edx, 48
	mov	rax, r10
	jmp	.L135
.L140:
	lea	rcx, .LC3[rip]
	call	_ZSt20__throw_format_errorPKc
.L139:
	lea	rcx, .LC6[rip]
	call	_ZSt20__throw_format_errorPKc
.L138:
	lea	rcx, .LC5[rip]
	call	_ZSt20__throw_format_errorPKc
.L134:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L132:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
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
.LFB3946:
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
	je	.L144
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L144
	cmp	dl, 123
	je	.L159
	mov	rcx, rsi
	sub	rcx, rax
	cmp	rcx, 1
	jle	.L146
	movzx	ecx, BYTE PTR 1[rax]
	cmp	cl, 62
	je	.L174
	cmp	cl, 94
	je	.L175
	cmp	cl, 60
	je	.L212
	cmp	dl, 62
	je	.L183
	cmp	dl, 94
	je	.L184
	cmp	dl, 60
	jne	.L151
.L185:
	mov	ecx, 1
.L150:
	add	rax, 1
	jmp	.L149
	.p2align 4,,10
	.p2align 3
.L212:
	mov	ecx, 1
.L147:
	mov	BYTE PTR 44[rsp], dl
	add	rax, 2
.L149:
	movzx	edx, BYTE PTR 36[rsp]
	and	edx, -4
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 36[rsp], dl
	je	.L144
.L151:
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	jne	.L210
.L144:
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
.L146:
	cmp	dl, 62
	je	.L183
	cmp	dl, 94
	je	.L184
	cmp	dl, 60
	je	.L185
.L210:
	lea	ecx, -32[rdx]
	mov	r10, rax
	cmp	cl, 13
	ja	.L211
	lea	r8, CSWTCH.554[rip]
	movzx	ecx, cl
	mov	ecx, DWORD PTR [r8+rcx*4]
	test	ecx, ecx
	jne	.L155
	cmp	dl, 35
	jne	.L159
.L156:
	or	BYTE PTR 36[rsp], 16
	add	rax, 1
	cmp	rsi, rax
	je	.L144
	movzx	edx, BYTE PTR 1[r10]
	cmp	dl, 125
	je	.L144
.L211:
	cmp	dl, 48
	mov	rcx, rax
	jne	.L159
	or	BYTE PTR 36[rsp], 64
	add	rax, 1
	cmp	rsi, rax
	je	.L144
	cmp	BYTE PTR 1[rcx], 125
	je	.L144
	.p2align 4,,10
	.p2align 3
.L159:
	lea	rcx, 36[rsp]
	mov	r8, rsi
	mov	rdx, rax
	call	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	cmp	rsi, rax
	je	.L144
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L144
	cmp	dl, 76
	je	.L213
.L160:
	sub	edx, 66
	cmp	dl, 54
	ja	.L172
	lea	rcx, .L173[rip]
	movzx	edx, dl
	movsx	rdx, DWORD PTR [rcx+rdx*4]
	add	rdx, rcx
	jmp	rdx
	.section .rdata,"dr"
	.align 4
.L173:
	.long	.L163-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L169-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L161-.L173
	.long	.L164-.L173
	.long	.L166-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L167-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L170-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L172-.L173
	.long	.L168-.L173
	.section	.text$_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L155:
	movzx	edx, BYTE PTR 36[rsp]
	and	ecx, 3
	add	rax, 1
	sal	ecx, 2
	and	edx, -13
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 36[rsp], dl
	je	.L144
	movzx	edx, BYTE PTR 1[r10]
	cmp	dl, 125
	je	.L144
	cmp	dl, 35
	mov	r10, rax
	je	.L156
	jmp	.L211
	.p2align 4,,10
	.p2align 3
.L169:
	add	rax, 1
	mov	edx, 6
	.p2align 4,,10
	.p2align 3
.L162:
	movzx	ecx, BYTE PTR 37[rsp]
	sal	edx, 3
	and	ecx, -121
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 37[rsp], dl
	je	.L144
	.p2align 4,,10
	.p2align 3
.L172:
	cmp	BYTE PTR [rax], 125
	je	.L144
.L165:
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L163:
	add	rax, 1
	mov	edx, 3
	jmp	.L162
.L168:
	add	rax, 1
	mov	edx, 5
	jmp	.L162
.L167:
	add	rax, 1
	mov	edx, 4
	jmp	.L162
.L166:
	add	rax, 1
	mov	edx, 1
	jmp	.L162
.L161:
	add	rax, 1
	mov	edx, 2
	jmp	.L162
.L164:
	test	edi, edi
	je	.L165
	add	rax, 1
	mov	edx, 7
	jmp	.L162
.L170:
	test	edi, edi
	jne	.L165
	add	rax, 1
	xor	edx, edx
	jmp	.L162
	.p2align 4,,10
	.p2align 3
.L175:
	mov	ecx, 3
	jmp	.L147
	.p2align 4,,10
	.p2align 3
.L174:
	mov	ecx, 2
	jmp	.L147
	.p2align 4,,10
	.p2align 3
.L184:
	mov	ecx, 3
	jmp	.L150
	.p2align 4,,10
	.p2align 3
.L183:
	mov	ecx, 2
	jmp	.L150
	.p2align 4,,10
	.p2align 3
.L213:
	or	BYTE PTR 36[rsp], 32
	lea	rcx, 1[rax]
	cmp	rsi, rcx
	jne	.L214
	mov	rax, rsi
	jmp	.L144
.L214:
	movzx	edx, BYTE PTR 1[rax]
	mov	rax, rcx
	cmp	dl, 125
	je	.L144
	jmp	.L160
	.seh_endproc
	.section .rdata,"dr"
.LC7:
	.ascii "basic_string::_M_create\0"
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy:
.LFB4985:
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
	je	.L228
	mov	rax, QWORD PTR 16[rcx]
.L216:
	test	rsi, rsi
	js	.L241
	cmp	rax, rsi
	jnb	.L218
	add	rax, rax
	cmp	rsi, rax
	jnb	.L218
	test	rax, rax
	js	.L219
	lea	rcx, 1[rax]
	mov	rsi, rax
	call	_Znwy
	test	r12, r12
	mov	rdi, rax
	je	.L221
	cmp	r12, 1
	mov	rdx, QWORD PTR [rbx]
	je	.L242
	.p2align 4,,10
	.p2align 3
.L222:
	mov	r8, r12
	mov	rcx, rax
	call	memcpy
.L221:
	test	rbp, rbp
	je	.L223
	cmp	QWORD PTR 144[rsp], 0
	je	.L223
	cmp	QWORD PTR 144[rsp], 1
	lea	rcx, [rdi+r12]
	je	.L243
	mov	r8, QWORD PTR 144[rsp]
	mov	rdx, rbp
	call	memcpy
.L223:
	test	r15, r15
	mov	rbp, QWORD PTR [rbx]
	jne	.L244
.L225:
	cmp	rbp, r14
	je	.L227
	mov	rax, QWORD PTR 16[rbx]
	mov	rcx, rbp
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L227:
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
.L218:
	mov	rcx, rsi
	add	rcx, 1
	js	.L219
	call	_Znwy
	test	r12, r12
	mov	rdi, rax
	je	.L221
	cmp	r12, 1
	mov	rdx, QWORD PTR [rbx]
	jne	.L222
.L242:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rdi], al
	jmp	.L221
	.p2align 4,,10
	.p2align 3
.L244:
	mov	r10, QWORD PTR 144[rsp]
	lea	rdx, 0[rbp+r13]
	add	r10, r12
	cmp	r15, 1
	lea	rcx, [rdi+r10]
	je	.L245
	mov	r8, r15
	call	memcpy
	jmp	.L225
	.p2align 4,,10
	.p2align 3
.L219:
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L228:
	mov	eax, 15
	jmp	.L216
	.p2align 4,,10
	.p2align 3
.L243:
	movzx	eax, BYTE PTR 0[rbp]
	test	r15, r15
	mov	rbp, QWORD PTR [rbx]
	mov	BYTE PTR [rcx], al
	je	.L225
	jmp	.L244
	.p2align 4,,10
	.p2align 3
.L245:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rcx], al
	jmp	.L225
.L241:
	lea	rcx, .LC7[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC8:
	.ascii "basic_string::append\0"
	.section	.text$_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv
	.def	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv
_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv:
.LFB4536:
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
	jb	.L256
	mov	rcx, QWORD PTR 288[rcx]
	lea	rax, 304[rbx]
	lea	rsi, [r8+rdx]
	cmp	rcx, rax
	je	.L252
	mov	rax, QWORD PTR 304[rbx]
.L248:
	cmp	rax, rsi
	jb	.L249
	test	r8, r8
	je	.L250
	add	rcx, rdx
	cmp	r8, 1
	je	.L257
	mov	rdx, r9
	call	memcpy
	mov	rcx, QWORD PTR 288[rbx]
.L250:
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
.L249:
	lea	rcx, 288[rbx]
	mov	QWORD PTR 32[rsp], r8
	xor	r8d, r8d
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rcx, QWORD PTR 288[rbx]
	jmp	.L250
	.p2align 4,,10
	.p2align 3
.L252:
	mov	eax, 15
	jmp	.L248
	.p2align 4,,10
	.p2align 3
.L257:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	mov	rcx, QWORD PTR 288[rbx]
	jmp	.L250
.L256:
	lea	rcx, .LC8[rip]
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
.LFB3466:
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
	movdqa	xmm0, XMMWORD PTR .LC9[rip]
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
	jne	.L289
.L259:
	mov	r9, QWORD PTR 488[rsp]
	movabs	rax, 9223372036854775807
	mov	r8, QWORD PTR 504[rsp]
	mov	rdx, QWORD PTR 776[rsp]
	sub	r8, r9
	sub	rax, rdx
	cmp	rax, r8
	jb	.L290
	mov	rcx, QWORD PTR 768[rsp]
	lea	rbp, [r8+rdx]
	cmp	rcx, rsi
	je	.L277
	mov	rax, QWORD PTR 784[rsp]
.L265:
	cmp	rax, rbp
	jb	.L266
	test	r8, r8
	jne	.L291
.L267:
	mov	QWORD PTR 776[rsp], rbp
	lea	rdx, 16[rbx]
	mov	BYTE PTR [rcx+rbp], 0
	mov	rax, QWORD PTR 488[rsp]
	mov	QWORD PTR [rbx], rdx
	mov	QWORD PTR 504[rsp], rax
	mov	rax, QWORD PTR 768[rsp]
	cmp	rax, rsi
	je	.L292
	mov	QWORD PTR [rbx], rax
	mov	rax, QWORD PTR 784[rsp]
	mov	rcx, QWORD PTR 776[rsp]
	mov	QWORD PTR 16[rbx], rax
.L276:
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
.L291:
	add	rcx, rdx
	cmp	r8, 1
	je	.L293
	mov	rdx, r9
	call	memcpy
	mov	rcx, QWORD PTR 768[rsp]
	jmp	.L267
	.p2align 4,,10
	.p2align 3
.L289:
	lea	rcx, 72[rsp]
	call	_ZNSt6localeD1Ev
	jmp	.L259
	.p2align 4,,10
	.p2align 3
.L266:
	lea	r12, 768[rsp]
	mov	QWORD PTR 32[rsp], r8
	xor	r8d, r8d
	mov	rcx, r12
.LEHB3:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rcx, QWORD PTR 768[rsp]
	jmp	.L267
	.p2align 4,,10
	.p2align 3
.L277:
	mov	eax, 15
	jmp	.L265
	.p2align 4,,10
	.p2align 3
.L292:
	mov	rcx, QWORD PTR 776[rsp]
	lea	r8, 1[rcx]
	cmp	r8d, 8
	jnb	.L270
	test	r8b, 4
	jne	.L294
	test	r8d, r8d
	je	.L276
	movzx	eax, BYTE PTR [rsi]
	test	r8b, 2
	mov	BYTE PTR 16[rbx], al
	je	.L276
	mov	r8d, r8d
	movzx	eax, WORD PTR -2[rsi+r8]
	mov	WORD PTR -2[rdx+r8], ax
	jmp	.L276
	.p2align 4,,10
	.p2align 3
.L293:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	mov	rcx, QWORD PTR 768[rsp]
	jmp	.L267
	.p2align 4,,10
	.p2align 3
.L270:
	mov	r9d, r8d
	sub	r8d, 1
	mov	r10, QWORD PTR -8[rsi+r9]
	cmp	r8d, 8
	mov	QWORD PTR -8[rdx+r9], r10
	jb	.L276
	and	r8d, -8
	xor	r9d, r9d
.L274:
	mov	r10d, r9d
	add	r9d, 8
	mov	r11, QWORD PTR [rax+r10]
	cmp	r9d, r8d
	mov	QWORD PTR [rdx+r10], r11
	jb	.L274
	jmp	.L276
.L294:
	mov	eax, DWORD PTR [rsi]
	mov	r8d, r8d
	mov	DWORD PTR 16[rbx], eax
	mov	eax, DWORD PTR -4[rsi+r8]
	mov	DWORD PTR -4[rdx+r8], eax
	jmp	.L276
.L290:
	lea	rcx, .LC8[rip]
	lea	r12, 768[rsp]
	call	_ZSt20__throw_length_errorPKc
.LEHE3:
.L278:
	mov	rbx, rax
.L264:
	mov	rcx, r12
	mov	QWORD PTR 480[rsp], rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
.LEHE4:
.L279:
	cmp	BYTE PTR 80[rsp], 0
	mov	rbx, rax
	je	.L263
	lea	rcx, 72[rsp]
	call	_ZNSt6localeD1Ev
.L263:
	lea	r12, 768[rsp]
	jmp	.L264
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3466:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3466-.LLSDACSB3466
.LLSDACSB3466:
	.uleb128 .LEHB2-.LFB3466
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L279-.LFB3466
	.uleb128 0
	.uleb128 .LEHB3-.LFB3466
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L278-.LFB3466
	.uleb128 0
	.uleb128 .LEHB4-.LFB3466
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE3466:
	.section	.text$_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE,"x"
	.linkonce discard
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC10:
	.ascii "id={} extra={}\0"
.LC11:
	.ascii "id=\0"
.LC12:
	.ascii " extra=\0"
	.align 8
.LC13:
	.ascii "C:\\Users\\ASUS\\AppData\\Local\\Temp\\tmp0itty2bi\\s.cpp\0"
.LC14:
	.ascii "a == os.str()\0"
.LC15:
	.ascii "line {}\12\0"
.LC16:
	.ascii "_bench_tmp_demo161.log\0"
.LC17:
	.ascii "lines == N\0"
	.align 8
.LC18:
	.ascii "demo ch161: format==ostringstream: %s, lines=%ld OK\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3889:
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
	sub	rsp, 1080
	.seh_stackalloc	1080
	.seh_endprologue
	call	__main
	lea	rax, .LC10[rip]
	mov	DWORD PTR 592[rsp], 42
	mov	QWORD PTR 120[rsp], rax
	lea	rax, 112[rsp]
	lea	rcx, 144[rsp]
	mov	rdx, rax
	mov	QWORD PTR 64[rsp], rax
	lea	r8, 96[rsp]
	mov	QWORD PTR 88[rsp], rcx
	lea	rdi, 592[rsp]
	mov	QWORD PTR 56[rsp], r8
	mov	DWORD PTR 608[rsp], 84
	mov	QWORD PTR 112[rsp], 14
	mov	QWORD PTR 96[rsp], 1586
	mov	QWORD PTR 104[rsp], rdi
.LEHB5:
	call	_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE
.LEHE5:
	lea	rax, 208[rsp]
	mov	rcx, rax
	mov	rbx, rax
	mov	QWORD PTR 80[rsp], rax
.LEHB6:
	call	_ZNSt7__cxx1119basic_ostringstreamIcSt11char_traitsIcESaIcEEC1Ev
.LEHE6:
	lea	rdx, .LC11[rip]
	mov	rcx, rbx
.LEHB7:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	edx, 42
	call	_ZNSolsEi
	lea	rdx, .LC12[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	edx, 84
	call	_ZNSolsEi
	lea	rdx, 216[rsp]
	mov	rcx, rdi
	call	_ZNKRSt7__cxx1115basic_stringbufIcSt11char_traitsIcESaIcEE3strEv
.LEHE7:
	mov	r8, QWORD PTR 152[rsp]
	cmp	r8, QWORD PTR 600[rsp]
	je	.L343
.L296:
	lea	rdx, .LC13[rip]
	mov	r8d, 17
	lea	rcx, .LC14[rip]
.LEHB8:
	call	[QWORD PTR __imp__assert[rip]]
.LEHE8:
.L343:
	test	r8, r8
	mov	rdx, QWORD PTR 592[rsp]
	mov	rcx, QWORD PTR 144[rsp]
	je	.L297
	call	memcmp
	test	eax, eax
	jne	.L296
.L297:
	lea	r12, 192[rsp]
	mov	rcx, rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	lea	rax, 176[rsp]
	mov	ecx, 32001
	mov	QWORD PTR 176[rsp], r12
	mov	QWORD PTR 184[rsp], 0
	mov	BYTE PTR 192[rsp], 0
	mov	QWORD PTR 72[rsp], rax
.LEHB9:
	call	_Znwy
	mov	rbx, rax
	mov	rax, QWORD PTR 184[rsp]
	mov	rsi, QWORD PTR 176[rsp]
	lea	r8, 1[rax]
	test	rax, rax
	je	.L344
	test	r8, r8
	jne	.L345
.L300:
	cmp	rsi, r12
	je	.L301
	mov	rax, QWORD PTR 192[rsp]
	mov	rcx, rsi
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L301:
	lea	rax, 176[rsp]
	mov	QWORD PTR 176[rsp], rbx
	movabs	r14, 9223372036854775807
	xor	ebx, ebx
	lea	rbp, 128[rsp]
	mov	QWORD PTR 72[rsp], rax
	mov	QWORD PTR 192[rsp], 32000
	lea	r13, .LC15[rip]
	lea	r15, 608[rsp]
	jmp	.L308
	.p2align 4,,10
	.p2align 3
.L349:
	test	r8, r8
	je	.L305
	add	rcx, rdx
	cmp	r8, 1
	je	.L346
	mov	rdx, r9
	call	memcpy
	mov	rcx, QWORD PTR 176[rsp]
.L305:
	mov	QWORD PTR 184[rsp], rsi
	mov	BYTE PTR [rcx+rsi], 0
	mov	rcx, QWORD PTR 592[rsp]
	cmp	rcx, r15
	je	.L307
	mov	rax, QWORD PTR 608[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L307:
	add	ebx, 1
	cmp	ebx, 1000
	je	.L347
.L308:
	mov	r8, QWORD PTR 56[rsp]
	mov	rcx, rdi
	mov	DWORD PTR 128[rsp], ebx
	mov	rdx, QWORD PTR 64[rsp]
	mov	QWORD PTR 120[rsp], r13
	mov	QWORD PTR 112[rsp], 8
	mov	QWORD PTR 96[rsp], 49
	mov	QWORD PTR 104[rsp], rbp
	call	_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE
.LEHE9:
	mov	rdx, QWORD PTR 184[rsp]
	mov	rax, r14
	mov	r8, QWORD PTR 600[rsp]
	mov	r9, QWORD PTR 592[rsp]
	sub	rax, rdx
	cmp	rax, r8
	jb	.L348
	mov	rcx, QWORD PTR 176[rsp]
	lea	rsi, [r8+rdx]
	cmp	rcx, r12
	je	.L320
	mov	rax, QWORD PTR 192[rsp]
.L303:
	cmp	rax, rsi
	jnb	.L349
	mov	rcx, QWORD PTR 72[rsp]
	mov	QWORD PTR 32[rsp], r8
	xor	r8d, r8d
.LEHB10:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE10:
	mov	rcx, QWORD PTR 176[rsp]
	jmp	.L305
	.p2align 4,,10
	.p2align 3
.L320:
	mov	eax, 15
	jmp	.L303
	.p2align 4,,10
	.p2align 3
.L347:
	lea	rsi, .LC16[rip]
	mov	r8d, 32
	mov	rcx, rdi
	mov	rdx, rsi
.LEHB11:
	call	_ZNSt14basic_ofstreamIcSt11char_traitsIcEEC1EPKcSt13_Ios_Openmode
.LEHE11:
	mov	r8, QWORD PTR 184[rsp]
	mov	rcx, rdi
	mov	rdx, QWORD PTR 176[rsp]
.LEHB12:
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
.LEHE12:
	mov	rcx, rdi
	call	_ZNSt14basic_ofstreamIcSt11char_traitsIcEED1Ev
	mov	r8d, 8
	mov	rdx, rsi
	mov	rcx, rdi
.LEHB13:
	call	_ZNSt14basic_ifstreamIcSt11char_traitsIcEEC1EPKcSt13_Ios_Openmode
.LEHE13:
	xor	ebx, ebx
	.p2align 4,,10
	.p2align 3
.L309:
	mov	rdx, rbp
	mov	rcx, rdi
.LEHB14:
	call	_ZNSi3getERc
.LEHE14:
	mov	rdx, QWORD PTR [rax]
	mov	rdx, QWORD PTR -24[rdx]
	test	BYTE PTR 32[rax+rdx], 5
	jne	.L350
	cmp	BYTE PTR 128[rsp], 10
	jne	.L309
	add	ebx, 1
	jmp	.L309
	.p2align 4,,10
	.p2align 3
.L350:
	mov	rcx, rdi
	call	_ZNSt14basic_ifstreamIcSt11char_traitsIcEED1Ev
	cmp	ebx, 1000
	jne	.L351
	mov	rcx, rsi
.LEHB15:
	call	remove
	mov	rdx, QWORD PTR 144[rsp]
	mov	r8d, 1000
	lea	rcx, .LC18[rip]
	call	_Z6printfPKcz
.LEHE15:
	mov	rcx, QWORD PTR 72[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, QWORD PTR 80[rsp]
	call	_ZNSt7__cxx1119basic_ostringstreamIcSt11char_traitsIcESaIcEED1Ev
	mov	rcx, QWORD PTR 88[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	xor	eax, eax
	add	rsp, 1080
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
.L346:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	mov	rcx, QWORD PTR 176[rsp]
	jmp	.L305
.L345:
	mov	rdx, rsi
	mov	rcx, rbx
	call	memcpy
	jmp	.L300
.L344:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [rbx], al
	jmp	.L300
.L348:
	lea	rcx, .LC8[rip]
.LEHB16:
	call	_ZSt20__throw_length_errorPKc
.LEHE16:
.L351:
	lea	rdx, .LC13[rip]
	mov	r8d, 28
	lea	rcx, .LC17[rip]
.LEHB17:
	call	[QWORD PTR __imp__assert[rip]]
.LEHE17:
.L326:
	mov	rcx, rdi
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L316:
	mov	rcx, QWORD PTR 72[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L314:
	mov	rcx, QWORD PTR 80[rsp]
	call	_ZNSt7__cxx1119basic_ostringstreamIcSt11char_traitsIcESaIcEED1Ev
.L319:
	mov	rcx, QWORD PTR 88[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB18:
	call	_Unwind_Resume
.LEHE18:
.L327:
	mov	rcx, rdi
	mov	rbx, rax
	call	_ZNSt14basic_ofstreamIcSt11char_traitsIcEED1Ev
	jmp	.L316
.L328:
	mov	rcx, rdi
	mov	rbx, rax
	call	_ZNSt14basic_ifstreamIcSt11char_traitsIcEED1Ev
	jmp	.L316
.L323:
	mov	rbx, rax
	jmp	.L314
.L322:
	mov	rbx, rax
	jmp	.L319
.L324:
	mov	rcx, rdi
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	jmp	.L314
.L325:
	mov	rbx, rax
	jmp	.L316
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3889:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3889-.LLSDACSB3889
.LLSDACSB3889:
	.uleb128 .LEHB5-.LFB3889
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LFB3889
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L322-.LFB3889
	.uleb128 0
	.uleb128 .LEHB7-.LFB3889
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L323-.LFB3889
	.uleb128 0
	.uleb128 .LEHB8-.LFB3889
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L324-.LFB3889
	.uleb128 0
	.uleb128 .LEHB9-.LFB3889
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L325-.LFB3889
	.uleb128 0
	.uleb128 .LEHB10-.LFB3889
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L326-.LFB3889
	.uleb128 0
	.uleb128 .LEHB11-.LFB3889
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L325-.LFB3889
	.uleb128 0
	.uleb128 .LEHB12-.LFB3889
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L327-.LFB3889
	.uleb128 0
	.uleb128 .LEHB13-.LFB3889
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L325-.LFB3889
	.uleb128 0
	.uleb128 .LEHB14-.LFB3889
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L328-.LFB3889
	.uleb128 0
	.uleb128 .LEHB15-.LFB3889
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L325-.LFB3889
	.uleb128 0
	.uleb128 .LEHB16-.LFB3889
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L326-.LFB3889
	.uleb128 0
	.uleb128 .LEHB17-.LFB3889
	.uleb128 .LEHE17-.LEHB17
	.uleb128 .L325-.LFB3889
	.uleb128 0
	.uleb128 .LEHB18-.LFB3889
	.uleb128 .LEHE18-.LEHB18
	.uleb128 0
	.uleb128 0
.LLSDACSE3889:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text$_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	.def	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE:
.LFB5285:
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
	jne	.L367
.L353:
	mov	rax, rsi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L367:
	mov	rcx, QWORD PTR 24[rcx]
	mov	rbx, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	rbx, rax
	cmp	rdi, rbx
	jb	.L354
	.p2align 4,,10
	.p2align 3
.L356:
	test	rbx, rbx
	je	.L355
	mov	r8, rbx
	mov	rdx, rbp
	call	memcpy
.L355:
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
	jnb	.L356
	test	rdi, rdi
	je	.L353
.L354:
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
.LFB5168:
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
.LFB5310:
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
	je	.L370
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L370
	cmp	dl, 123
	je	.L371
	mov	rcx, rsi
	sub	rcx, rax
	cmp	rcx, 1
	jle	.L372
	movzx	ecx, BYTE PTR 1[rax]
	cmp	cl, 62
	je	.L384
	cmp	cl, 94
	je	.L385
	cmp	cl, 60
	je	.L402
	cmp	dl, 62
	je	.L391
	cmp	dl, 94
	je	.L392
	cmp	dl, 60
	jne	.L377
.L393:
	mov	ecx, 1
.L376:
	add	rax, 1
	jmp	.L375
	.p2align 4,,10
	.p2align 3
.L402:
	mov	ecx, 1
.L373:
	mov	BYTE PTR 44[rsp], dl
	add	rax, 2
.L375:
	movzx	edx, BYTE PTR 36[rsp]
	and	edx, -4
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 36[rsp], dl
	je	.L370
.L377:
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	jne	.L401
.L370:
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
.L372:
	cmp	dl, 62
	je	.L391
	cmp	dl, 94
	je	.L392
	cmp	dl, 60
	je	.L393
.L401:
	cmp	dl, 48
	mov	rcx, rax
	je	.L403
	.p2align 4,,10
	.p2align 3
.L371:
	lea	rcx, 36[rsp]
	mov	r8, rsi
	mov	rdx, rax
	call	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	cmp	rsi, rax
	je	.L370
	movzx	edx, BYTE PTR [rax]
	mov	ecx, edx
	and	ecx, -33
	cmp	cl, 80
	jne	.L381
	cmp	dl, 80
	jne	.L382
	movzx	edx, BYTE PTR 37[rsp]
	and	edx, -121
	or	edx, 8
	mov	BYTE PTR 37[rsp], dl
.L382:
	lea	rcx, 1[rax]
	cmp	rcx, rsi
	je	.L390
	movzx	edx, BYTE PTR 1[rax]
	mov	rax, rcx
.L381:
	cmp	dl, 125
	je	.L370
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L403:
	or	BYTE PTR 36[rsp], 64
	add	rax, 1
	cmp	rsi, rax
	je	.L370
	cmp	BYTE PTR 1[rcx], 125
	jne	.L371
	jmp	.L370
	.p2align 4,,10
	.p2align 3
.L385:
	mov	ecx, 3
	jmp	.L373
	.p2align 4,,10
	.p2align 3
.L384:
	mov	ecx, 2
	jmp	.L373
	.p2align 4,,10
	.p2align 3
.L392:
	mov	ecx, 3
	jmp	.L376
	.p2align 4,,10
	.p2align 3
.L391:
	mov	ecx, 2
	jmp	.L376
.L390:
	mov	rax, rsi
	jmp	.L370
	.seh_endproc
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc:
.LFB5356:
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
	je	.L417
	mov	rax, QWORD PTR 16[rcx]
	cmp	rax, rbp
	jb	.L418
.L406:
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
.L418:
	test	rbp, rbp
	js	.L419
	lea	r14, [rax+rax]
	cmp	rbp, r14
	jb	.L420
	mov	rcx, rsi
	mov	r14, rbp
	add	rcx, 2
	js	.L410
.L411:
	call	_Znwy
	test	rsi, rsi
	mov	rdi, rax
	jne	.L407
	mov	r15, QWORD PTR [rbx]
.L412:
	cmp	r12, r15
	je	.L415
	mov	rax, QWORD PTR 16[rbx]
	mov	rcx, r15
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L415:
	mov	QWORD PTR [rbx], rdi
	mov	QWORD PTR 16[rbx], r14
	jmp	.L406
	.p2align 4,,10
	.p2align 3
.L417:
	cmp	rbp, 16
	jne	.L406
	mov	ecx, 31
	mov	r14d, 30
	call	_Znwy
	mov	rdi, rax
.L407:
	cmp	rsi, 1
	mov	r15, QWORD PTR [rbx]
	je	.L421
	mov	r8, rsi
	mov	rdx, r15
	mov	rcx, rdi
	call	memcpy
	jmp	.L412
	.p2align 4,,10
	.p2align 3
.L421:
	movzx	eax, BYTE PTR [r15]
	mov	BYTE PTR [rdi], al
	jmp	.L412
	.p2align 4,,10
	.p2align 3
.L420:
	lea	rcx, 1[r14]
	test	r14, r14
	jns	.L411
.L410:
	call	_ZSt17__throw_bad_allocv
.L419:
	lea	rcx, .LC7[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC19:
	.ascii "format error: missing precision after '.' in format string\0"
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	.def	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE:
.LFB5400:
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
	je	.L423
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L423
	cmp	dl, 123
	je	.L424
	mov	rcx, rsi
	sub	rcx, rax
	cmp	rcx, 1
	jle	.L425
	movzx	ecx, BYTE PTR 1[rax]
	cmp	cl, 62
	je	.L470
	cmp	cl, 94
	je	.L471
	cmp	cl, 60
	je	.L521
	cmp	dl, 62
	je	.L480
	cmp	dl, 94
	je	.L481
	cmp	dl, 60
	jne	.L430
.L482:
	mov	ecx, 1
.L429:
	add	rax, 1
	jmp	.L428
	.p2align 4,,10
	.p2align 3
.L521:
	mov	ecx, 1
.L426:
	mov	BYTE PTR 60[rsp], dl
	add	rax, 2
.L428:
	movzx	edx, BYTE PTR 52[rsp]
	and	edx, -4
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 52[rsp], dl
	je	.L423
.L430:
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	jne	.L519
.L423:
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
.L425:
	cmp	dl, 62
	je	.L480
	cmp	dl, 94
	je	.L481
	cmp	dl, 60
	je	.L482
.L519:
	lea	ecx, -32[rdx]
	mov	r9, rax
	cmp	cl, 13
	ja	.L520
	lea	r8, CSWTCH.554[rip]
	movzx	ecx, cl
	mov	ecx, DWORD PTR [r8+rcx*4]
	test	ecx, ecx
	jne	.L434
	cmp	dl, 35
	jne	.L439
.L435:
	or	BYTE PTR 52[rsp], 16
	add	rax, 1
	cmp	rsi, rax
	je	.L423
	movzx	edx, BYTE PTR 1[r9]
	cmp	dl, 125
	je	.L423
.L520:
	cmp	dl, 48
	mov	r9, rax
	je	.L522
.L439:
	cmp	dl, 46
	jne	.L424
.L440:
	movzx	ecx, BYTE PTR 1[rax]
	lea	r8, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	lea	rbp, 1[rax]
	cmp	BYTE PTR [r8+rcx], 9
	ja	.L442
	lea	rcx, 32[rsp]
	mov	rdx, rbp
	mov	r8, rsi
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	mov	rax, QWORD PTR 40[rsp]
	mov	rdx, QWORD PTR 32[rsp]
	test	rax, rax
	je	.L523
	cmp	rbp, rax
	mov	WORD PTR 58[rsp], dx
	je	.L445
	mov	ecx, 1
.L444:
	movzx	edx, BYTE PTR 53[rsp]
	add	ecx, ecx
	and	edx, -7
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 53[rsp], dl
	je	.L423
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L423
	cmp	dl, 76
	je	.L479
	sub	edx, 65
	cmp	dl, 38
	ja	.L457
	lea	rcx, .L459[rip]
	movzx	edx, dl
	movsx	rdx, DWORD PTR [rcx+rdx*4]
	add	rdx, rcx
	jmp	rdx
	.section .rdata,"dr"
	.align 4
.L459:
	.long	.L465-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L464-.L459
	.long	.L460-.L459
	.long	.L463-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L462-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L457-.L459
	.long	.L461-.L459
	.long	.L460-.L459
	.long	.L458-.L459
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L434:
	movzx	edx, BYTE PTR 52[rsp]
	and	ecx, 3
	add	rax, 1
	sal	ecx, 2
	and	edx, -13
	or	edx, ecx
	cmp	rsi, rax
	mov	BYTE PTR 52[rsp], dl
	je	.L423
	movzx	edx, BYTE PTR 1[r9]
	cmp	dl, 125
	je	.L423
	cmp	dl, 35
	mov	r9, rax
	je	.L435
	jmp	.L520
	.p2align 4,,10
	.p2align 3
.L424:
	lea	rcx, 52[rsp]
	mov	r9, rbx
	mov	r8, rsi
	mov	rdx, rax
	call	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	cmp	rsi, rax
	je	.L423
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 125
	je	.L423
	cmp	dl, 46
	je	.L440
	cmp	dl, 76
	je	.L479
.L468:
	sub	edx, 65
	cmp	dl, 38
	ja	.L466
	lea	rcx, .L467[rip]
	movzx	edx, dl
	movsx	rdx, DWORD PTR [rcx+rdx*4]
	add	rdx, rcx
	jmp	rdx
	.section .rdata,"dr"
	.align 4
.L467:
	.long	.L465-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L464-.L467
	.long	.L460-.L467
	.long	.L463-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L462-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L466-.L467
	.long	.L461-.L467
	.long	.L460-.L467
	.long	.L458-.L467
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
.L462:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 8
	mov	BYTE PTR 53[rsp], dl
	.p2align 4,,10
	.p2align 3
.L466:
	cmp	rsi, rax
	je	.L423
.L457:
	cmp	BYTE PTR [rax], 125
	je	.L423
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L460:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 40
	mov	BYTE PTR 53[rsp], dl
	jmp	.L466
.L464:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 32
	mov	BYTE PTR 53[rsp], dl
	jmp	.L466
.L463:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 56
	mov	BYTE PTR 53[rsp], dl
	jmp	.L466
.L465:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 16
	mov	BYTE PTR 53[rsp], dl
	jmp	.L466
.L458:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 48
	mov	BYTE PTR 53[rsp], dl
	jmp	.L466
.L461:
	movzx	edx, BYTE PTR 53[rsp]
	add	rax, 1
	and	edx, -121
	or	edx, 24
	mov	BYTE PTR 53[rsp], dl
	jmp	.L466
	.p2align 4,,10
	.p2align 3
.L522:
	or	BYTE PTR 52[rsp], 64
	add	rax, 1
	cmp	rsi, rax
	je	.L423
	movzx	edx, BYTE PTR 1[r9]
	cmp	dl, 125
	je	.L423
	jmp	.L439
	.p2align 4,,10
	.p2align 3
.L471:
	mov	ecx, 3
	jmp	.L426
	.p2align 4,,10
	.p2align 3
.L470:
	mov	ecx, 2
	jmp	.L426
	.p2align 4,,10
	.p2align 3
.L481:
	mov	ecx, 3
	jmp	.L429
	.p2align 4,,10
	.p2align 3
.L480:
	mov	ecx, 2
	jmp	.L429
	.p2align 4,,10
	.p2align 3
.L479:
	or	BYTE PTR 52[rsp], 32
	mov	rdx, rax
	add	rax, 1
	cmp	rsi, rax
	je	.L423
	movzx	edx, BYTE PTR 1[rdx]
	cmp	dl, 125
	je	.L423
	jmp	.L468
	.p2align 4,,10
	.p2align 3
.L442:
	cmp	cl, 123
	je	.L524
.L445:
	lea	rcx, .LC19[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L524:
	lea	rdx, 2[rax]
	cmp	rsi, rdx
	je	.L525
	movzx	ecx, BYTE PTR 2[rax]
	cmp	cl, 125
	je	.L526
	cmp	cl, 48
	je	.L527
	lea	r8d, -49[rcx]
	cmp	r8b, 8
	jbe	.L452
.L453:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L526:
	cmp	DWORD PTR 16[rbx], 1
	je	.L455
	mov	rax, QWORD PTR 24[rbx]
	mov	DWORD PTR 16[rbx], 2
	lea	rcx, 1[rax]
	mov	WORD PTR 58[rsp], ax
	mov	QWORD PTR 24[rbx], rcx
.L449:
	lea	rax, 1[rdx]
	cmp	rbp, rax
	je	.L445
	mov	ecx, 2
	jmp	.L444
.L527:
	lea	rdx, 3[rax]
	xor	eax, eax
.L451:
	cmp	rsi, rdx
	je	.L453
	test	rdx, rdx
	je	.L453
.L469:
	cmp	BYTE PTR [rdx], 125
	jne	.L453
	cmp	DWORD PTR 16[rbx], 2
	je	.L455
	mov	DWORD PTR 16[rbx], 1
	mov	WORD PTR 58[rsp], ax
	jmp	.L449
.L452:
	lea	r8, 3[rax]
	cmp	rsi, r8
	je	.L453
	movzx	eax, BYTE PTR 3[rax]
	sub	eax, 48
	cmp	al, 9
	ja	.L454
	lea	rcx, 32[rsp]
	mov	r8, rsi
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzx	eax, WORD PTR 32[rsp]
	mov	rdx, QWORD PTR 40[rsp]
	jmp	.L451
.L454:
	movsx	ax, cl
	mov	rdx, r8
	sub	eax, 48
	jmp	.L469
.L523:
	lea	rcx, .LC6[rip]
	call	_ZSt20__throw_format_errorPKc
.L525:
	lea	rcx, .LC3[rip]
	call	_ZSt20__throw_format_errorPKc
.L455:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
	nop
	.seh_endproc
	.section	.text$_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE
	.def	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE
_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE:
.LFB5413:
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
	je	.L529
	movzx	ecx, BYTE PTR [rsi]
	cmp	cl, 125
	je	.L571
	cmp	cl, 123
	je	.L530
	mov	rdx, rax
	sub	rdx, rsi
	cmp	rdx, 1
	jle	.L531
	movzx	edx, BYTE PTR 1[rsi]
	cmp	dl, 62
	je	.L572
	cmp	dl, 94
	je	.L573
	cmp	dl, 60
	mov	r8d, 1
	jne	.L599
.L532:
	mov	BYTE PTR 76[rsp], cl
	add	rsi, 2
.L534:
	movzx	edx, BYTE PTR 68[rsp]
	and	edx, -4
	or	edx, r8d
	cmp	rax, rsi
	mov	BYTE PTR 68[rsp], dl
	je	.L571
.L536:
	movzx	ecx, BYTE PTR [rsi]
	cmp	cl, 125
	je	.L571
.L538:
	cmp	cl, 48
	je	.L600
	lea	r8, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	movzx	edx, cl
	cmp	BYTE PTR [r8+rdx], 9
	ja	.L540
	lea	rcx, 48[rsp]
	mov	r8, rax
	mov	rdx, rsi
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	mov	rdx, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 48[rsp]
	mov	rax, QWORD PTR 40[rsp]
	test	rdx, rdx
	je	.L559
	cmp	rsi, rdx
	mov	WORD PTR 72[rsp], cx
	mov	r8d, 1
	je	.L543
.L542:
	movzx	ecx, WORD PTR 68[rsp]
	and	r8d, 3
	sal	r8d, 7
	and	cx, -385
	or	ecx, r8d
	mov	WORD PTR 68[rsp], cx
.L543:
	cmp	rax, rdx
	je	.L529
	movzx	ecx, BYTE PTR [rdx]
	cmp	cl, 125
	je	.L583
.L544:
	cmp	cl, 46
	je	.L555
.L598:
	cmp	cl, 115
	je	.L601
.L557:
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L571:
	mov	rax, rsi
.L529:
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
.L531:
	cmp	cl, 62
	je	.L584
	cmp	cl, 94
	je	.L585
	cmp	cl, 60
	je	.L586
	jmp	.L538
	.p2align 4,,10
	.p2align 3
.L555:
	movzx	r8d, BYTE PTR 1[rdx]
	lea	r9, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	lea	rsi, 1[rdx]
	cmp	BYTE PTR [r9+r8], 9
	ja	.L558
	lea	rcx, 48[rsp]
	mov	rdx, rsi
	mov	r8, rax
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	mov	rdx, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 48[rsp]
	test	rdx, rdx
	je	.L559
	cmp	rsi, rdx
	mov	rax, QWORD PTR 40[rsp]
	mov	WORD PTR 74[rsp], cx
	je	.L561
	mov	r8d, 1
.L560:
	movzx	ecx, BYTE PTR 69[rsp]
	add	r8d, r8d
	and	ecx, -7
	or	ecx, r8d
	cmp	rax, rdx
	mov	BYTE PTR 69[rsp], cl
	je	.L529
	movzx	ecx, BYTE PTR [rdx]
	cmp	cl, 125
	jne	.L598
.L583:
	mov	rax, rdx
	jmp	.L529
.L540:
	cmp	cl, 123
	mov	rdx, rsi
	jne	.L544
	.p2align 4,,10
	.p2align 3
.L530:
	lea	rdx, 1[rsi]
	cmp	rax, rdx
	je	.L562
	movsx	cx, BYTE PTR 1[rsi]
	cmp	cl, 125
	je	.L602
	cmp	cl, 48
	je	.L603
	lea	r8d, -49[rcx]
	cmp	r8b, 8
	jbe	.L551
.L552:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L599:
	cmp	cl, 62
	je	.L584
	cmp	cl, 94
	je	.L585
	cmp	cl, 60
	jne	.L536
.L586:
	mov	r8d, 1
.L535:
	add	rsi, 1
	jmp	.L534
	.p2align 4,,10
	.p2align 3
.L558:
	cmp	r8b, 123
	je	.L604
.L561:
	lea	rcx, .LC19[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L573:
	mov	r8d, 3
	jmp	.L532
	.p2align 4,,10
	.p2align 3
.L572:
	mov	r8d, 2
	jmp	.L532
	.p2align 4,,10
	.p2align 3
.L584:
	mov	r8d, 2
	jmp	.L535
	.p2align 4,,10
	.p2align 3
.L585:
	mov	r8d, 3
	jmp	.L535
	.p2align 4,,10
	.p2align 3
.L601:
	lea	rcx, 1[rdx]
	cmp	rcx, rax
	je	.L529
	cmp	BYTE PTR 1[rdx], 125
	jne	.L557
	mov	rax, rcx
	jmp	.L529
	.p2align 4,,10
	.p2align 3
.L602:
	cmp	DWORD PTR 16[rbx], 1
	je	.L554
	mov	rcx, QWORD PTR 24[rbx]
	mov	DWORD PTR 16[rbx], 2
	lea	r8, 1[rcx]
	mov	WORD PTR 72[rsp], cx
	mov	QWORD PTR 24[rbx], r8
.L548:
	add	rdx, 1
	cmp	rsi, rdx
	je	.L543
	mov	r8d, 2
	jmp	.L542
.L603:
	lea	rdx, 2[rsi]
	xor	ecx, ecx
.L550:
	cmp	rax, rdx
	je	.L552
	test	rdx, rdx
	je	.L552
.L570:
	cmp	BYTE PTR [rdx], 125
	jne	.L552
	cmp	DWORD PTR 16[rbx], 2
	je	.L554
	mov	DWORD PTR 16[rbx], 1
	mov	WORD PTR 72[rsp], cx
	jmp	.L548
.L604:
	lea	rcx, 2[rdx]
	cmp	rax, rcx
	je	.L562
	movzx	r8d, BYTE PTR 2[rdx]
	cmp	r8b, 125
	je	.L605
	cmp	r8b, 48
	je	.L606
	lea	r9d, -49[r8]
	cmp	r9b, 8
	ja	.L552
	lea	r9, 3[rdx]
	cmp	rax, r9
	je	.L552
	movzx	edx, BYTE PTR 3[rdx]
	sub	edx, 48
	cmp	dl, 9
	ja	.L567
	lea	r9, 48[rsp]
	mov	rdx, rcx
	mov	r8, rax
	mov	QWORD PTR 40[rsp], rax
	mov	rcx, r9
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzx	edx, WORD PTR 48[rsp]
	mov	rcx, QWORD PTR 56[rsp]
	mov	rax, QWORD PTR 40[rsp]
.L566:
	test	rcx, rcx
	je	.L552
	cmp	rax, rcx
	je	.L552
.L569:
	cmp	BYTE PTR [rcx], 125
	jne	.L552
	cmp	DWORD PTR 16[rbx], 2
	je	.L554
	mov	DWORD PTR 16[rbx], 1
	mov	WORD PTR 74[rsp], dx
.L564:
	lea	rdx, 1[rcx]
	cmp	rsi, rdx
	je	.L561
	mov	r8d, 2
	jmp	.L560
.L551:
	lea	r9, 2[rsi]
	cmp	rax, r9
	je	.L552
	movzx	r10d, BYTE PTR 2[rsi]
	lea	r8d, -48[r10]
	cmp	r8b, 9
	ja	.L553
	lea	rcx, 48[rsp]
	mov	r8, rax
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzx	ecx, WORD PTR 48[rsp]
	mov	rdx, QWORD PTR 56[rsp]
	mov	rax, QWORD PTR 40[rsp]
	jmp	.L550
.L553:
	sub	ecx, 48
	mov	rdx, r9
	jmp	.L570
.L605:
	cmp	DWORD PTR 16[rbx], 1
	je	.L554
	mov	rdx, QWORD PTR 24[rbx]
	mov	DWORD PTR 16[rbx], 2
	lea	r8, 1[rdx]
	mov	WORD PTR 74[rsp], dx
	mov	QWORD PTR 24[rbx], r8
	jmp	.L564
.L606:
	lea	rcx, 3[rdx]
	xor	edx, edx
	jmp	.L566
.L567:
	movsx	dx, r8b
	mov	rcx, r9
	sub	edx, 48
	jmp	.L569
.L600:
	lea	rcx, .LC5[rip]
	call	_ZSt20__throw_format_errorPKc
.L554:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L559:
	lea	rcx, .LC6[rip]
	call	_ZSt20__throw_format_errorPKc
.L562:
	lea	rcx, .LC3[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
	.def	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_:
.LFB5519:
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
	je	.L651
	cmp	r8d, 2
	je	.L629
	cmp	r9, 31
	ja	.L652
	test	r9, r9
	jne	.L653
	lea	rdx, 32[rsp]
	movaps	XMMWORD PTR 32[rsp], xmm6
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	rbx, rax
	jmp	.L614
	.p2align 4,,10
	.p2align 3
.L629:
	mov	rdi, r9
	xor	r12d, r12d
.L609:
	cmp	rsi, 31
	ja	.L630
	test	rsi, rsi
	jne	.L615
	test	rdi, rdi
	je	.L650
	lea	r13, 48[rsp]
	jmp	.L617
	.p2align 4,,10
	.p2align 3
.L630:
	mov	esi, 32
.L615:
	lea	r13, 48[rsp]
	cmp	esi, 8
	movsx	ecx, dl
	mov	r8d, esi
	mov	rdx, r13
	jnb	.L654
.L618:
	and	r8d, 7
	je	.L622
	xor	eax, eax
.L621:
	mov	r9d, eax
	add	eax, 1
	cmp	eax, r8d
	mov	BYTE PTR [rdx+r9], cl
	jb	.L621
.L622:
	test	rdi, rdi
	je	.L650
	lea	rbp, 32[rsp]
	cmp	rsi, rdi
	jnb	.L625
.L617:
	lea	rbp, 32[rsp]
	.p2align 4,,10
	.p2align 3
.L626:
	mov	rcx, rbx
	mov	rdx, rbp
	sub	rdi, rsi
	mov	QWORD PTR 32[rsp], rsi
	mov	QWORD PTR 40[rsp], r13
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	cmp	rsi, rdi
	mov	rbx, rax
	jb	.L626
	test	rdi, rdi
	jne	.L625
.L624:
	mov	rcx, rbx
	mov	rdx, rbp
	movaps	XMMWORD PTR 32[rsp], xmm6
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	test	r12, r12
	mov	rbx, rax
	je	.L614
.L611:
	lea	r13, 48[rsp]
	cmp	rsi, r12
	jnb	.L613
	.p2align 4,,10
	.p2align 3
.L627:
	mov	rcx, rbx
	mov	rdx, rbp
	sub	r12, rsi
	mov	QWORD PTR 32[rsp], rsi
	mov	QWORD PTR 40[rsp], r13
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	cmp	rsi, r12
	mov	rbx, rax
	jb	.L627
	test	r12, r12
	jne	.L613
.L614:
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
.L651:
	mov	rdi, r9
	and	esi, 1
	shr	rdi
	add	rsi, rdi
	mov	r12, rsi
	jmp	.L609
	.p2align 4,,10
	.p2align 3
.L653:
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
.L613:
	mov	rcx, rbx
	mov	rdx, rbp
	mov	QWORD PTR 32[rsp], r12
	mov	QWORD PTR 40[rsp], r13
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	rbx, rax
	jmp	.L614
	.p2align 4,,10
	.p2align 3
.L625:
	mov	rcx, rbx
	mov	rdx, rbp
	mov	QWORD PTR 32[rsp], rdi
	mov	QWORD PTR 40[rsp], r13
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	rbx, rax
	jmp	.L624
	.p2align 4,,10
	.p2align 3
.L654:
	movabs	rax, 72340172838076673
	movzx	r9d, cl
	mov	r10d, esi
	imul	r9, rax
	and	r10d, -8
	xor	eax, eax
.L619:
	mov	edx, eax
	add	eax, 8
	cmp	eax, r10d
	mov	QWORD PTR 0[r13+rdx], r9
	jb	.L619
	lea	rdx, 0[r13+rax]
	jmp	.L618
	.p2align 4,,10
	.p2align 3
.L652:
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
	jmp	.L611
.L650:
	lea	rbp, 32[rsp]
	jmp	.L624
	.seh_endproc
	.section	.text$_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	.def	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_:
.LFB5602:
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
	ja	.L656
	mov	rbx, rcx
	sub	rbx, rdx
	cmp	rbx, rax
	jle	.L656
	lea	rbx, -1[r9]
	xor	r12d, r12d
	xor	esi, esi
	jmp	.L659
	.p2align 4,,10
	.p2align 3
.L698:
	add	rsi, 1
.L658:
	lea	rbp, [r8+rsi]
	movsx	rax, BYTE PTR 0[rbp]
	lea	r9d, -1[rax]
	cmp	r9b, 125
	ja	.L676
	mov	r9, rcx
	sub	r9, rdx
	cmp	r9, rax
	jle	.L676
.L659:
	sub	rcx, rax
	cmp	rsi, rbx
	jb	.L698
	add	r12, 1
	jmp	.L658
	.p2align 4,,10
	.p2align 3
.L676:
	lea	rdi, -1[r12]
	cmp	rdx, rcx
	lea	rbx, -1[rsi]
	je	.L699
.L671:
	mov	r13, rcx
	xor	eax, eax
	sub	r13, rdx
	.p2align 4,,10
	.p2align 3
.L662:
	movzx	r9d, BYTE PTR [rdx+rax]
	mov	BYTE PTR [r10+rax], r9b
	add	rax, 1
	cmp	rax, r13
	jne	.L662
	lea	rdx, [r10+rax]
.L661:
	test	r12, r12
	je	.L663
	.p2align 4,,10
	.p2align 3
.L666:
	mov	BYTE PTR [rdx], r11b
	movzx	r10d, BYTE PTR 0[rbp]
	lea	r12, 1[rdx]
	test	r10b, r10b
	jle	.L673
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L665:
	movzx	r9d, BYTE PTR [rcx+rax]
	mov	BYTE PTR 1[rdx+rax], r9b
	add	rax, 1
	cmp	rax, r10
	jne	.L665
	lea	rdx, [r12+rax]
	add	rcx, rax
.L664:
	sub	rdi, 1
	jnb	.L666
.L663:
	test	rsi, rsi
	je	.L655
	.p2align 4,,10
	.p2align 3
.L670:
	mov	BYTE PTR [rdx], r11b
	movzx	r10d, BYTE PTR [r8+rbx]
	lea	rsi, 1[rdx]
	test	r10b, r10b
	jle	.L674
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L669:
	movzx	r9d, BYTE PTR [rcx+rax]
	mov	BYTE PTR 1[rdx+rax], r9b
	add	rax, 1
	cmp	r10, rax
	jne	.L669
	lea	rdx, [rsi+r10]
	add	rcx, r10
.L668:
	sub	rbx, 1
	jnb	.L670
.L655:
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
.L674:
	mov	rdx, rsi
	jmp	.L668
	.p2align 4,,10
	.p2align 3
.L673:
	mov	rdx, r12
	jmp	.L664
.L656:
	cmp	rcx, rdx
	je	.L700
	mov	rbp, r8
	mov	rbx, -1
	mov	rdi, -1
	xor	r12d, r12d
	xor	esi, esi
	jmp	.L671
.L699:
	mov	rdx, r10
	jmp	.L661
.L700:
	mov	rdx, r10
	jmp	.L655
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC20:
	.ascii "format error: argument used for width or precision must be a non-negative integer\0"
	.section	.text$_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
	.def	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E:
.LFB5603:
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	lea	rdx, .L704[rip]
	mov	rax, QWORD PTR [rcx]
	mov	QWORD PTR 32[rsp], rax
	movzx	eax, BYTE PTR 16[rcx]
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L704:
	.long	.L709-.L704
	.long	.L710-.L704
	.long	.L710-.L704
	.long	.L708-.L704
	.long	.L707-.L704
	.long	.L706-.L704
	.long	.L705-.L704
	.long	.L710-.L704
	.long	.L710-.L704
	.long	.L710-.L704
	.long	.L710-.L704
	.long	.L710-.L704
	.long	.L710-.L704
	.long	.L710-.L704
	.long	.L710-.L704
	.long	.L710-.L704
	.section	.text$_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L706:
	mov	rax, QWORD PTR 32[rsp]
	test	rax, rax
	js	.L710
.L701:
	add	rsp, 72
	ret
	.p2align 4,,10
	.p2align 3
.L707:
	mov	eax, DWORD PTR 32[rsp]
	add	rsp, 72
	ret
	.p2align 4,,10
	.p2align 3
.L708:
	movsx	rax, DWORD PTR 32[rsp]
	test	eax, eax
	jns	.L701
.L710:
	lea	rcx, .LC20[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L705:
	mov	rax, QWORD PTR 32[rsp]
	add	rsp, 72
	ret
.L709:
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
.LFB5417:
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
	je	.L723
	cmp	ax, 256
	je	.L715
.L719:
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
.L723:
	movzx	r9d, WORD PTR 4[r9]
.L714:
	cmp	rdi, r9
	jnb	.L719
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
.L715:
	movzx	edx, BYTE PTR [rsi]
	mov	BYTE PTR 80[rsp], 0
	movzx	eax, WORD PTR 4[r9]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L724
	test	cl, cl
	jne	.L718
	mov	rdx, QWORD PTR [rsi]
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L718
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
.L718:
	lea	rcx, 64[rsp]
	mov	DWORD PTR 176[rsp], r8d
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
	mov	r8d, DWORD PTR 176[rsp]
	mov	r9, rax
	jmp	.L714
	.p2align 4,,10
	.p2align 3
.L724:
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
	jmp	.L718
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
	.def	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE:
.LFB5416:
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
	je	.L736
	and	edx, 6
	jne	.L737
.L728:
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
.L737:
	cmp	dl, 2
	je	.L738
	cmp	dl, 4
	jne	.L728
	movzx	edx, BYTE PTR [r8]
	mov	BYTE PTR 80[rsp], 0
	movzx	eax, WORD PTR 6[rcx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L739
	test	cl, cl
	jne	.L732
	mov	rdx, QWORD PTR [r8]
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L732
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
.L732:
	lea	rcx, 64[rsp]
	mov	QWORD PTR 144[rsp], r8
	mov	QWORD PTR 128[rsp], r9
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
	mov	r8, QWORD PTR 144[rsp]
	mov	r9, QWORD PTR 128[rsp]
	jmp	.L730
	.p2align 4,,10
	.p2align 3
.L736:
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
.L738:
	movzx	eax, WORD PTR 6[rcx]
.L730:
	cmp	rbx, rax
	cmovbe	rax, rbx
	jmp	.L728
	.p2align 4,,10
	.p2align 3
.L739:
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
	jmp	.L732
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	.def	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_:
.LFB5503:
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
	je	.L792
	cmp	ax, 256
	je	.L793
	test	BYTE PTR [rcx], 32
	mov	QWORD PTR -48[rbp], 0
	mov	BYTE PTR -40[rbp], 0
	jne	.L774
	mov	rcx, QWORD PTR 16[r9]
.L771:
	lea	rdx, -64[rbp]
	mov	QWORD PTR -64[rbp], r12
	mov	QWORD PTR -56[rbp], r13
.LEHB19:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L763:
	cmp	BYTE PTR -40[rbp], 0
	jne	.L794
.L780:
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
.L792:
	movzx	eax, WORD PTR 4[rcx]
	mov	QWORD PTR -72[rbp], rax
.L742:
	test	BYTE PTR [rbx], 32
	mov	QWORD PTR -48[rbp], 0
	mov	BYTE PTR -40[rbp], 0
	jne	.L770
.L746:
	mov	rax, QWORD PTR -72[rbp]
	mov	rcx, QWORD PTR 16[rsi]
	cmp	r12, rax
	jnb	.L771
	movzx	edx, BYTE PTR [rbx]
	mov	rax, rcx
	movzx	r9d, BYTE PTR 8[rbx]
	mov	rbx, QWORD PTR -72[rbp]
	mov	r8d, edx
	sub	rbx, r12
	and	r8d, 3
	jne	.L795
	and	edx, 64
	je	.L772
	test	rdi, rdi
	jne	.L796
	lea	rsi, -64[rbp]
	mov	edx, 48
	mov	r8d, 2
	jmp	.L765
	.p2align 4,,10
	.p2align 3
.L794:
	lea	rcx, -48[rbp]
	mov	QWORD PTR -72[rbp], rax
	call	_ZNSt6localeD1Ev
	mov	rax, QWORD PTR -72[rbp]
	jmp	.L780
	.p2align 4,,10
	.p2align 3
.L774:
	mov	QWORD PTR -72[rbp], 0
.L770:
	cmp	BYTE PTR 32[rsi], 0
	lea	rdx, 24[rsi]
	je	.L797
.L747:
	lea	rax, -32[rbp]
	mov	rcx, rax
	mov	QWORD PTR -80[rbp], rax
	call	_ZNSt6localeC1ERKS_
	cmp	BYTE PTR -40[rbp], 0
	jne	.L798
	mov	rdx, QWORD PTR -80[rbp]
	lea	rax, -48[rbp]
	mov	rcx, rax
	mov	QWORD PTR -88[rbp], rax
	call	_ZNSt6localeC1ERKS_
	mov	rcx, QWORD PTR -80[rbp]
	mov	BYTE PTR -40[rbp], 1
	call	_ZNSt6localeD1Ev
	cmp	BYTE PTR -40[rbp], 0
	je	.L799
.L750:
	mov	rdx, QWORD PTR -88[rbp]
	mov	rcx, QWORD PTR -80[rbp]
	call	_ZNKSt6locale4nameB5cxx11Ev
	cmp	QWORD PTR -24[rbp], 1
	lea	rax, -16[rbp]
	mov	rcx, QWORD PTR -32[rbp]
	je	.L800
.L752:
	cmp	rcx, rax
	mov	QWORD PTR -88[rbp], rax
	je	.L755
	mov	rax, QWORD PTR -16[rbp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L755:
	mov	rcx, QWORD PTR .refptr._ZNSt7__cxx118numpunctIcE2idE[rip]
	call	_ZNKSt6locale2id5_M_idEv
	mov	rdx, rax
	mov	rax, QWORD PTR -48[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	rdx, QWORD PTR [rax+rdx*8]
	test	rdx, rdx
	mov	QWORD PTR -104[rbp], rdx
	je	.L757
	mov	rax, QWORD PTR [rdx]
	mov	rcx, QWORD PTR -80[rbp]
	call	[QWORD PTR 32[rax]]
.LEHE19:
	mov	rax, QWORD PTR -24[rbp]
	test	rax, rax
	mov	QWORD PTR -96[rbp], rax
	je	.L759
	mov	rax, r15
	sub	rax, rdi
	lea	rax, 15[rdi+rax*2]
	and	rax, -16
	call	___chkstk_ms
	sub	rsp, rax
	test	rdi, rdi
	lea	r13, 48[rsp]
	jne	.L801
.L760:
	mov	rcx, QWORD PTR -104[rbp]
	lea	r12, [r14+rdi]
	add	r14, r15
	mov	r15, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR [rcx]
.LEHB20:
	call	[QWORD PTR 24[rax]]
.LEHE20:
	mov	QWORD PTR 32[rsp], r12
	lea	rcx, 0[r13+rdi]
	movsx	edx, al
	mov	r8, r15
	mov	QWORD PTR 40[rsp], r14
	mov	r9, QWORD PTR -96[rbp]
	call	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	sub	rax, r13
	mov	r12, rax
.L759:
	mov	rcx, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR -88[rbp]
.L791:
	cmp	rcx, rax
	je	.L746
	mov	rax, QWORD PTR -16[rbp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L746
	.p2align 4,,10
	.p2align 3
.L772:
	lea	rsi, -64[rbp]
	mov	edx, 32
	mov	r8d, 2
.L765:
	mov	QWORD PTR -64[rbp], r12
	mov	r9, rbx
	mov	rcx, rax
	mov	QWORD PTR -56[rbp], r13
	mov	DWORD PTR 32[rsp], edx
	mov	rdx, rsi
.LEHB21:
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
	jmp	.L763
	.p2align 4,,10
	.p2align 3
.L795:
	lea	rsi, -64[rbp]
	movsx	edx, r9b
	jmp	.L765
	.p2align 4,,10
	.p2align 3
.L798:
	lea	rdx, -48[rbp]
	mov	r10, rdx
	mov	QWORD PTR -88[rbp], rdx
	mov	rdx, QWORD PTR -80[rbp]
	mov	rcx, r10
	call	_ZNSt6localeaSERKS_
	mov	rcx, QWORD PTR -80[rbp]
	call	_ZNSt6localeD1Ev
	cmp	BYTE PTR -40[rbp], 0
	jne	.L750
.L799:
	mov	rcx, QWORD PTR -88[rbp]
	call	_ZNSt6localeC1Ev
	mov	BYTE PTR -40[rbp], 1
	jmp	.L750
	.p2align 4,,10
	.p2align 3
.L796:
	lea	rsi, -64[rbp]
	cmp	rdi, r12
	mov	rax, r12
	mov	QWORD PTR -56[rbp], r13
	cmovbe	rax, rdi
	mov	rdx, rsi
	mov	QWORD PTR -64[rbp], rax
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.LEHE21:
	add	r13, rdi
	sub	r12, rdi
	mov	edx, 48
	mov	r8d, 2
	jmp	.L765
	.p2align 4,,10
	.p2align 3
.L793:
	movzx	edx, BYTE PTR [r9]
	mov	BYTE PTR -16[rbp], 0
	movzx	eax, WORD PTR 4[rcx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L802
	test	cl, cl
	jne	.L745
	mov	rdx, QWORD PTR [r9]
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L745
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
.L745:
	lea	rcx, -32[rbp]
.LEHB22:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE22:
	mov	QWORD PTR -72[rbp], rax
	jmp	.L742
	.p2align 4,,10
	.p2align 3
.L800:
	cmp	BYTE PTR [rcx], 67
	jne	.L752
	jmp	.L791
	.p2align 4,,10
	.p2align 3
.L797:
	mov	rcx, rdx
	mov	QWORD PTR -80[rbp], rdx
	call	_ZNSt6localeC1Ev
	mov	rdx, QWORD PTR -80[rbp]
	mov	BYTE PTR 32[rsi], 1
	jmp	.L747
	.p2align 4,,10
	.p2align 3
.L801:
	mov	r8, rdi
	mov	rdx, r14
	mov	rcx, r13
	call	memcpy
	jmp	.L760
	.p2align 4,,10
	.p2align 3
.L802:
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
	jmp	.L745
.L757:
.LEHB23:
	call	_ZSt16__throw_bad_castv
.LEHE23:
.L776:
	mov	rcx, QWORD PTR -80[rbp]
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L768:
	cmp	BYTE PTR -40[rbp], 0
	je	.L769
	lea	rcx, -48[rbp]
	call	_ZNSt6localeD1Ev
.L769:
	mov	rcx, rbx
.LEHB24:
	call	_Unwind_Resume
.LEHE24:
.L775:
	mov	rbx, rax
	jmp	.L768
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5503:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5503-.LLSDACSB5503
.LLSDACSB5503:
	.uleb128 .LEHB19-.LFB5503
	.uleb128 .LEHE19-.LEHB19
	.uleb128 .L775-.LFB5503
	.uleb128 0
	.uleb128 .LEHB20-.LFB5503
	.uleb128 .LEHE20-.LEHB20
	.uleb128 .L776-.LFB5503
	.uleb128 0
	.uleb128 .LEHB21-.LFB5503
	.uleb128 .LEHE21-.LEHB21
	.uleb128 .L775-.LFB5503
	.uleb128 0
	.uleb128 .LEHB22-.LFB5503
	.uleb128 .LEHE22-.LEHB22
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB23-.LFB5503
	.uleb128 .LEHE23-.LEHB23
	.uleb128 .L775-.LFB5503
	.uleb128 0
	.uleb128 .LEHB24-.LFB5503
	.uleb128 .LEHE24-.LEHB24
	.uleb128 0
	.uleb128 0
.LLSDACSE5503:
	.section	.text$_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC21:
	.ascii "0b\0"
.LC22:
	.ascii "0B\0"
.LC23:
	.ascii "0\0"
.LC24:
	.ascii "0X\0"
.LC25:
	.ascii "0x\0"
	.align 8
.LC26:
	.ascii "format error: integer not representable as character\0"
	.align 8
.LC27:
	.ascii "00010203040506070809101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899\0"
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5493:
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
	je	.L863
	shr	dl, 3
	and	edx, 15
	cmp	dl, 4
	je	.L807
	ja	.L808
	cmp	dl, 1
	jbe	.L809
	lea	rbp, .LC21[rip]
	cmp	cl, 16
	lea	rdx, .LC22[rip]
	cmovne	rbp, rdx
	test	al, al
	jne	.L864
	lea	r12, 72[rsp]
	mov	eax, 48
	lea	r13, 71[rsp]
.L814:
	mov	BYTE PTR 71[rsp], al
	movzx	eax, BYTE PTR [rbx]
	test	al, 16
	je	.L850
.L849:
	mov	rdx, -2
	mov	ecx, 2
.L818:
	add	rdx, r13
	test	ecx, ecx
	mov	r10d, ecx
	je	.L819
	xor	ecx, ecx
.L836:
	mov	r8d, ecx
	add	ecx, 1
	movzx	r9d, BYTE PTR 0[rbp+r8]
	cmp	ecx, r10d
	mov	BYTE PTR [rdx+r8], r9b
	jb	.L836
	jmp	.L819
	.p2align 4,,10
	.p2align 3
.L863:
	test	al, al
	js	.L805
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
.L809:
	test	al, al
	movzx	edi, al
	jne	.L820
	mov	BYTE PTR 71[rsp], 48
	lea	r12, 72[rsp]
	lea	r13, 71[rsp]
.L821:
	movzx	eax, BYTE PTR [rbx]
	mov	rdx, r13
.L819:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L865
.L838:
	cmp	eax, 3
	je	.L851
.L839:
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
.L807:
	test	al, al
	je	.L844
	movzx	edx, al
	bsr	ecx, edx
	lea	r12d, 3[rcx]
	mov	ecx, 2863311531
	imul	r12, rcx
	shr	r12, 33
	cmp	edx, 63
	jbe	.L826
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 73[rsp], al
	mov	eax, edx
	shr	edx, 6
	shr	eax, 3
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 72[rsp], al
.L827:
	add	edx, 48
.L828:
	lea	r13, 71[rsp]
	mov	r12d, r12d
	mov	r8d, 1
	lea	rbp, .LC23[rip]
	add	r12, r13
	mov	ecx, 1
.L825:
	mov	BYTE PTR 71[rsp], dl
.L829:
	movzx	eax, BYTE PTR [rbx]
	test	al, 16
	je	.L850
	mov	rdx, rcx
	neg	rdx
	test	r8b, r8b
	jne	.L818
.L850:
	shr	al, 2
	mov	rdx, r13
	and	eax, 3
	cmp	eax, 1
	jne	.L838
.L865:
	mov	eax, 43
.L840:
	mov	BYTE PTR -1[rdx], al
	sub	rdx, 1
	jmp	.L839
	.p2align 4,,10
	.p2align 3
.L820:
	cmp	edi, 9
	jbe	.L843
	lea	rcx, 80[rsp]
	cmp	edi, 99
	mov	r8d, 201
	lea	rdx, .LC27[rip]
	jbe	.L866
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
.L822:
	add	r8d, 48
.L824:
	lea	r13, 71[rsp]
	mov	BYTE PTR 71[rsp], r8b
	lea	r12, 0[r13+rax]
	jmp	.L821
	.p2align 4,,10
	.p2align 3
.L808:
	cmp	cl, 40
	je	.L867
	test	al, al
	jne	.L846
	mov	BYTE PTR 71[rsp], 48
	lea	rbp, .LC24[rip]
	cmp	cl, 48
	lea	r12, 72[rsp]
	lea	r13, 71[rsp]
	je	.L832
.L831:
	movzx	eax, BYTE PTR [rbx]
	test	al, 16
	jne	.L849
	jmp	.L850
	.p2align 4,,10
	.p2align 3
.L832:
	mov	rdi, r13
	.p2align 4,,10
	.p2align 3
.L835:
	movsx	ecx, BYTE PTR [rdi]
	add	rdi, 1
	call	toupper
	mov	BYTE PTR -1[rdi], al
	cmp	rdi, r12
	jne	.L835
	mov	r8d, 1
	mov	ecx, 2
	jmp	.L829
	.p2align 4,,10
	.p2align 3
.L851:
	mov	eax, 32
	jmp	.L840
	.p2align 4,,10
	.p2align 3
.L844:
	mov	edx, 48
	xor	r8d, r8d
	xor	ecx, ecx
	lea	r12, 72[rsp]
	xor	ebp, ebp
	lea	r13, 71[rsp]
	jmp	.L825
	.p2align 4,,10
	.p2align 3
.L864:
	movzx	eax, al
	mov	r12d, 32
	mov	edx, 31
	bsr	r9d, eax
	xor	r9d, 31
	sub	r12d, r9d
	sub	edx, r9d
	je	.L817
	mov	ecx, edx
	lea	r8, 70[rsp+rcx]
	lea	rdx, 71[rsp+rcx]
	mov	ecx, 30
	sub	ecx, r9d
	sub	r8, rcx
	.p2align 4,,10
	.p2align 3
.L816:
	mov	ecx, eax
	sub	rdx, 1
	shr	eax
	and	ecx, 1
	add	ecx, 48
	mov	BYTE PTR 1[rdx], cl
	cmp	rdx, r8
	jne	.L816
.L817:
	lea	r13, 71[rsp]
	movsx	r12, r12d
	mov	eax, 49
	add	r12, r13
	jmp	.L814
	.p2align 4,,10
	.p2align 3
.L867:
	test	al, al
	jne	.L845
	mov	BYTE PTR 71[rsp], 48
	lea	rbp, .LC25[rip]
	lea	r12, 72[rsp]
	lea	r13, 71[rsp]
	jmp	.L831
	.p2align 4,,10
	.p2align 3
.L846:
	lea	rbp, .LC24[rip]
.L830:
	movabs	rdi, 3978425819141910832
	movzx	edx, al
	bsr	r8d, edx
	mov	QWORD PTR 80[rsp], rdi
	movabs	rdi, 7378413942531504440
	add	r8d, 4
	mov	QWORD PTR 88[rsp], rdi
	shr	r8d, 2
	cmp	edx, 15
	ja	.L868
	movzx	eax, BYTE PTR 80[rsp+rdx]
.L834:
	mov	BYTE PTR 71[rsp], al
	lea	r13, 71[rsp]
	mov	eax, r8d
	cmp	cl, 48
	lea	r12, 0[r13+rax]
	jne	.L831
	test	r8d, r8d
	jne	.L832
	mov	r8d, 1
	mov	ecx, 2
	mov	r12, r13
	jmp	.L829
	.p2align 4,,10
	.p2align 3
.L868:
	and	eax, 15
	shr	edx, 4
	movzx	eax, BYTE PTR 80[rsp+rax]
	mov	BYTE PTR 72[rsp], al
	movzx	eax, BYTE PTR 80[rsp+rdx]
	jmp	.L834
	.p2align 4,,10
	.p2align 3
.L845:
	lea	rbp, .LC25[rip]
	jmp	.L830
	.p2align 4,,10
	.p2align 3
.L866:
	call	memcpy
	add	edi, edi
	lea	eax, 1[rdi]
	movzx	r8d, BYTE PTR 80[rsp+rdi]
	movzx	eax, BYTE PTR 80[rsp+rax]
	mov	BYTE PTR 72[rsp], al
	mov	eax, 2
	jmp	.L824
	.p2align 4,,10
	.p2align 3
.L843:
	mov	eax, 1
	jmp	.L822
.L826:
	cmp	edx, 7
	jbe	.L827
	and	eax, 7
	shr	edx, 3
	add	eax, 48
	add	edx, 48
	mov	BYTE PTR 72[rsp], al
	jmp	.L828
.L805:
	lea	rcx, .LC26[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC28:
	.ascii "true\0"
.LC29:
	.ascii "false\0"
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_:
.LFB5387:
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
	je	.L918
	test	al, al
	jne	.L919
	test	BYTE PTR [rcx], 32
	lea	rbp, 80[rsp]
	mov	BYTE PTR 80[rsp], 0
	mov	QWORD PTR 64[rsp], rbp
	mov	QWORD PTR 72[rsp], 0
	jne	.L920
	lea	rsi, 64[rsp]
	mov	eax, edx
	neg	al
	lea	rax, .LC28[rip]
	sbb	r12, r12
	add	r12, 5
	test	dl, dl
	lea	rdx, .LC29[rip]
	cmove	rax, rdx
	cmp	rax, rbp
	je	.L890
	xor	edx, edx
	test	r12b, 4
	mov	ecx, r12d
	jne	.L921
	test	cl, 2
	jne	.L922
.L892:
	and	ecx, 1
	jne	.L923
.L893:
	mov	rax, rbp
.L894:
	mov	QWORD PTR 72[rsp], r12
	mov	BYTE PTR [rax+r12], 0
.L917:
	mov	rdx, QWORD PTR 72[rsp]
	lea	rcx, 48[rsp]
	mov	r9, rbx
	mov	r8, rdi
	mov	rax, QWORD PTR 64[rsp]
	mov	DWORD PTR 32[rsp], 1
	lea	rsi, 64[rsp]
	mov	QWORD PTR 48[rsp], rdx
	mov	QWORD PTR 56[rsp], rax
.LEHB25:
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.LEHE25:
	mov	rcx, QWORD PTR 64[rsp]
	mov	rbx, rax
	cmp	rcx, rbp
	je	.L905
	mov	rax, QWORD PTR 80[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L905:
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
.L919:
	movzx	edx, dl
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
.LEHB26:
	jmp	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.p2align 4,,10
	.p2align 3
.L918:
	mov	BYTE PTR 96[rsp], dl
	lea	rax, 96[rsp]
	mov	r9, rbx
	mov	edx, 1
	lea	rcx, 48[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.LEHE26:
	mov	rbx, rax
	jmp	.L905
	.p2align 4,,10
	.p2align 3
.L923:
	movzx	eax, BYTE PTR [rax+rdx]
	mov	BYTE PTR 80[rsp+rdx], al
	jmp	.L893
	.p2align 4,,10
	.p2align 3
.L922:
	movzx	r8d, WORD PTR [rax+rdx]
	mov	WORD PTR 80[rsp+rdx], r8w
	add	rdx, 2
	and	ecx, 1
	je	.L893
	jmp	.L923
	.p2align 4,,10
	.p2align 3
.L921:
	mov	edx, DWORD PTR [rax]
	test	cl, 2
	mov	DWORD PTR 80[rsp], edx
	mov	edx, 4
	je	.L892
	jmp	.L922
	.p2align 4,,10
	.p2align 3
.L920:
	cmp	BYTE PTR 32[r8], 0
	lea	r13, 24[r8]
	je	.L924
.L874:
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
	je	.L875
	mov	rcx, r12
	call	_ZNSt6localeD1Ev
	test	sil, sil
	jne	.L876
	mov	rax, QWORD PTR 0[r13]
	lea	rsi, 64[rsp]
	mov	rdx, r13
	mov	rcx, r12
.LEHB27:
	call	[QWORD PTR 48[rax]]
.L878:
	mov	rax, QWORD PTR 96[rsp]
	lea	rsi, 112[rsp]
	mov	rcx, QWORD PTR 64[rsp]
	mov	r8, QWORD PTR 104[rsp]
	cmp	rax, rsi
	je	.L925
	movq	xmm0, r8
	cmp	rcx, rbp
	movhps	xmm0, QWORD PTR 112[rsp]
	je	.L926
	test	rcx, rcx
	mov	rdx, QWORD PTR 80[rsp]
	mov	QWORD PTR 64[rsp], rax
	movups	XMMWORD PTR 72[rsp], xmm0
	je	.L886
	mov	QWORD PTR 96[rsp], rcx
	mov	QWORD PTR 112[rsp], rdx
.L885:
	mov	QWORD PTR 104[rsp], 0
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 96[rsp]
	cmp	rcx, rsi
	je	.L917
	mov	rax, QWORD PTR 112[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L917
	.p2align 4,,10
	.p2align 3
.L876:
	mov	rax, QWORD PTR 0[r13]
	lea	rsi, 64[rsp]
	mov	rdx, r13
	mov	rcx, r12
	call	[QWORD PTR 40[rax]]
.LEHE27:
	jmp	.L878
	.p2align 4,,10
	.p2align 3
.L924:
	mov	rcx, r13
	call	_ZNSt6localeC1Ev
	mov	BYTE PTR 32[rdi], 1
	jmp	.L874
.L926:
	mov	QWORD PTR 64[rsp], rax
	movups	XMMWORD PTR 72[rsp], xmm0
.L886:
	mov	QWORD PTR 96[rsp], rsi
	lea	rsi, 112[rsp]
	mov	rcx, rsi
	jmp	.L885
.L925:
	test	r8, r8
	je	.L881
	cmp	r8, 1
	je	.L927
	mov	rdx, rsi
	call	memcpy
	mov	r8, QWORD PTR 104[rsp]
	mov	rcx, QWORD PTR 64[rsp]
.L881:
	mov	QWORD PTR 72[rsp], r8
	mov	BYTE PTR [rcx+r8], 0
	mov	rcx, QWORD PTR 96[rsp]
	jmp	.L885
.L927:
	movzx	eax, BYTE PTR 112[rsp]
	mov	BYTE PTR [rcx], al
	mov	r8, QWORD PTR 104[rsp]
	mov	rcx, QWORD PTR 64[rsp]
	jmp	.L881
.L875:
.LEHB28:
	call	_ZSt16__throw_bad_castv
.LEHE28:
.L900:
	mov	rbx, rax
.L897:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB29:
	call	_Unwind_Resume
.LEHE29:
.L890:
	xor	eax, eax
	mov	QWORD PTR 32[rsp], r12
	mov	r9, rbp
	xor	r8d, r8d
	mov	QWORD PTR 40[rsp], rax
	mov	rdx, rbp
	mov	rcx, rsi
.LEHB30:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
.LEHE30:
	mov	rax, QWORD PTR 64[rsp]
	jmp	.L894
.L899:
	lea	rsi, 64[rsp]
	mov	rcx, r12
	mov	rbx, rax
	call	_ZNSt6localeD1Ev
	jmp	.L897
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5387:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5387-.LLSDACSB5387
.LLSDACSB5387:
	.uleb128 .LEHB25-.LFB5387
	.uleb128 .LEHE25-.LEHB25
	.uleb128 .L900-.LFB5387
	.uleb128 0
	.uleb128 .LEHB26-.LFB5387
	.uleb128 .LEHE26-.LEHB26
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB27-.LFB5387
	.uleb128 .LEHE27-.LEHB27
	.uleb128 .L900-.LFB5387
	.uleb128 0
	.uleb128 .LEHB28-.LFB5387
	.uleb128 .LEHE28-.LEHB28
	.uleb128 .L899-.LFB5387
	.uleb128 0
	.uleb128 .LEHB29-.LFB5387
	.uleb128 .LEHE29-.LEHB29
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB30-.LFB5387
	.uleb128 .LEHE30-.LEHB30
	.uleb128 .L900-.LFB5387
	.uleb128 0
.LLSDACSE5387:
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
.LFB5392:
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
	je	.L1000
	shr	dl, 3
	mov	eax, ebx
	and	edx, 15
	test	bl, bl
	js	.L1001
	cmp	dl, 4
	je	.L937
	ja	.L938
	cmp	dl, 1
	jbe	.L939
	lea	rbp, .LC21[rip]
	cmp	cl, 16
	lea	rdx, .LC22[rip]
	cmovne	rbp, rdx
	test	bl, bl
	jne	.L935
	lea	r12, 73[rsp]
	mov	eax, 48
	lea	r13, 72[rsp]
.L944:
	mov	BYTE PTR 72[rsp], al
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	je	.L985
.L984:
	mov	rdx, -2
	mov	ecx, 2
.L948:
	add	rdx, r13
	test	ecx, ecx
	mov	r10d, ecx
	je	.L949
	xor	ecx, ecx
.L966:
	mov	r8d, ecx
	add	ecx, 1
	movzx	r9d, BYTE PTR 0[rbp+r8]
	cmp	ecx, r10d
	mov	BYTE PTR [rdx+r8], r9b
	jb	.L966
	.p2align 4,,10
	.p2align 3
.L949:
	lea	rcx, -1[rdx]
	shr	al, 2
	and	eax, 3
	test	bl, bl
	jns	.L951
	mov	BYTE PTR -1[rdx], 45
	mov	rdx, rcx
	jmp	.L968
	.p2align 4,,10
	.p2align 3
.L1001:
	neg	eax
	cmp	dl, 4
	je	.L932
	ja	.L933
	cmp	dl, 1
	jbe	.L934
	lea	rbp, .LC21[rip]
	cmp	cl, 16
	lea	rdx, .LC22[rip]
	cmovne	rbp, rdx
.L935:
	movzx	eax, al
	mov	r12d, 32
	bsr	r9d, eax
	mov	edx, 31
	xor	r9d, 31
	sub	r12d, r9d
	sub	edx, r9d
	je	.L947
	mov	ecx, edx
	lea	r8, 71[rsp+rcx]
	lea	rdx, 72[rsp+rcx]
	mov	ecx, 30
	sub	ecx, r9d
	sub	r8, rcx
	.p2align 4,,10
	.p2align 3
.L946:
	mov	ecx, eax
	sub	rdx, 1
	shr	eax
	and	ecx, 1
	add	ecx, 48
	mov	BYTE PTR 1[rdx], cl
	cmp	rdx, r8
	jne	.L946
.L947:
	lea	r13, 72[rsp]
	movsx	r12, r12d
	mov	eax, 49
	add	r12, r13
	jmp	.L944
	.p2align 4,,10
	.p2align 3
.L1000:
	lea	rax, 80[rsp]
	mov	r9, rsi
	mov	edx, 1
	mov	BYTE PTR 80[rsp], bl
	lea	rcx, 48[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L998:
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
.L939:
	test	bl, bl
	jne	.L950
	movzx	eax, BYTE PTR [rsi]
	lea	r13, 72[rsp]
	mov	BYTE PTR 72[rsp], 48
	lea	r12, 73[rsp]
	mov	rdx, r13
	lea	rcx, 71[rsp]
	shr	al, 2
	and	eax, 3
.L951:
	movzx	eax, al
	cmp	eax, 1
	je	.L1002
	cmp	eax, 3
	je	.L1003
.L968:
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
	jmp	.L998
	.p2align 4,,10
	.p2align 3
.L933:
	lea	rbp, .LC25[rip]
	cmp	cl, 40
	lea	rdx, .LC24[rip]
	cmovne	rbp, rdx
.L936:
	movabs	r11, 3978425819141910832
	movzx	edx, al
	bsr	r8d, edx
	mov	QWORD PTR 80[rsp], r11
	movabs	r11, 7378413942531504440
	add	r8d, 4
	mov	QWORD PTR 88[rsp], r11
	shr	r8d, 2
	cmp	al, 15
	ja	.L1004
	movzx	eax, BYTE PTR 80[rsp+rdx]
.L964:
	lea	r13, 72[rsp]
	mov	r12d, r8d
	mov	BYTE PTR 72[rsp], al
	add	r12, r13
	cmp	cl, 48
	je	.L1005
.L961:
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	jne	.L984
.L985:
	mov	rdx, r13
	jmp	.L949
	.p2align 4,,10
	.p2align 3
.L1002:
	mov	BYTE PTR -1[rdx], 43
.L971:
	mov	rdx, rcx
	jmp	.L968
	.p2align 4,,10
	.p2align 3
.L937:
	test	bl, bl
	jne	.L932
	xor	r8d, r8d
	xor	ecx, ecx
	xor	ebp, ebp
	lea	r12, 73[rsp]
	mov	edx, 48
	lea	r13, 72[rsp]
.L956:
	mov	BYTE PTR 72[rsp], dl
.L960:
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	je	.L985
	mov	rdx, rcx
	neg	rdx
	test	r8b, r8b
	jne	.L948
	mov	rdx, r13
	jmp	.L949
	.p2align 4,,10
	.p2align 3
.L938:
	cmp	cl, 40
	je	.L1006
	test	bl, bl
	jne	.L981
	cmp	cl, 48
	mov	BYTE PTR 72[rsp], 48
	je	.L982
	lea	rbp, .LC24[rip]
	lea	r12, 73[rsp]
	lea	r13, 72[rsp]
	jmp	.L961
	.p2align 4,,10
	.p2align 3
.L1003:
	mov	BYTE PTR -1[rdx], 32
	jmp	.L971
	.p2align 4,,10
	.p2align 3
.L932:
	movzx	edx, al
	bsr	ecx, edx
	lea	r12d, 3[rcx]
	mov	ecx, 2863311531
	imul	r12, rcx
	shr	r12, 33
	cmp	al, 63
	jbe	.L957
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 74[rsp], al
	mov	eax, edx
	shr	edx, 6
	shr	eax, 3
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 73[rsp], al
.L958:
	add	edx, 48
.L959:
	lea	r13, 72[rsp]
	mov	r12d, r12d
	mov	r8d, 1
	lea	rbp, .LC23[rip]
	add	r12, r13
	mov	ecx, 1
	jmp	.L956
	.p2align 4,,10
	.p2align 3
.L934:
	movzx	r14d, al
.L972:
	cmp	al, 9
	jbe	.L977
	cmp	al, 100
	sbb	ebp, ebp
	add	ebp, 2
	cmp	al, 100
	sbb	r12, r12
	add	r12, 3
	cmp	al, 100
	sbb	r13d, r13d
	add	r13d, 3
.L952:
	lea	rcx, 80[rsp]
	mov	r8d, 201
	lea	rdx, .LC27[rip]
	call	memcpy
	cmp	r14d, 99
	jbe	.L1007
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
.L954:
	add	r14d, 48
.L955:
	lea	r13, 72[rsp]
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR 72[rsp], r14b
	add	r12, r13
	mov	rdx, r13
	jmp	.L949
	.p2align 4,,10
	.p2align 3
.L1004:
	and	eax, 15
	shr	edx, 4
	movzx	eax, BYTE PTR 80[rsp+rax]
	mov	BYTE PTR 73[rsp], al
	movzx	eax, BYTE PTR 80[rsp+rdx]
	jmp	.L964
	.p2align 4,,10
	.p2align 3
.L982:
	lea	r12, 73[rsp]
	lea	rbp, .LC24[rip]
	lea	r13, 72[rsp]
.L962:
	mov	r14, r13
	.p2align 4,,10
	.p2align 3
.L965:
	movsx	ecx, BYTE PTR [r14]
	add	r14, 1
	call	toupper
	mov	BYTE PTR -1[r14], al
	cmp	r14, r12
	jne	.L965
	mov	r8d, 1
	mov	ecx, 2
	jmp	.L960
	.p2align 4,,10
	.p2align 3
.L1005:
	test	r8d, r8d
	jne	.L962
	mov	r8d, 1
	mov	ecx, 2
	mov	r12, r13
	jmp	.L960
	.p2align 4,,10
	.p2align 3
.L1006:
	test	bl, bl
	jne	.L980
	mov	BYTE PTR 72[rsp], 48
	lea	rbp, .LC25[rip]
	lea	r12, 73[rsp]
	lea	r13, 72[rsp]
	jmp	.L961
	.p2align 4,,10
	.p2align 3
.L977:
	xor	ebp, ebp
	mov	r12d, 1
	mov	r13d, 1
	jmp	.L952
	.p2align 4,,10
	.p2align 3
.L950:
	movsx	r14d, bl
	jmp	.L972
	.p2align 4,,10
	.p2align 3
.L981:
	lea	rbp, .LC24[rip]
	jmp	.L936
	.p2align 4,,10
	.p2align 3
.L1007:
	cmp	r14d, 9
	jbe	.L954
	add	r14d, r14d
	lea	eax, 1[r14]
	movzx	r14d, BYTE PTR 80[rsp+r14]
	movzx	eax, BYTE PTR 80[rsp+rax]
	mov	BYTE PTR 73[rsp], al
	jmp	.L955
.L980:
	lea	rbp, .LC25[rip]
	jmp	.L936
.L957:
	cmp	al, 7
	jbe	.L958
	and	eax, 7
	shr	edx, 3
	add	eax, 48
	add	edx, 48
	mov	BYTE PTR 73[rsp], al
	jmp	.L959
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5393:
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
	je	.L1096
	shr	al, 3
	and	eax, 15
	test	esi, esi
	js	.L1097
	cmp	al, 4
	je	.L1018
	ja	.L1019
	cmp	al, 1
	jbe	.L1020
	lea	r14, .LC21[rip]
	cmp	dl, 16
	lea	rax, .LC22[rip]
	cmovne	r14, rax
	test	esi, esi
	jne	.L1016
	lea	r12, 68[rsp]
	mov	eax, 48
	lea	r13, 67[rsp]
.L1025:
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], al
	test	bl, 16
	je	.L1078
.L1077:
	mov	rdx, -2
	mov	eax, 2
.L1029:
	add	rdx, r13
	test	eax, eax
	mov	r9d, eax
	je	.L1030
	xor	eax, eax
.L1056:
	mov	ecx, eax
	add	eax, 1
	movzx	r8d, BYTE PTR [r14+rcx]
	cmp	eax, r9d
	mov	BYTE PTR [rdx+rcx], r8b
	jb	.L1056
.L1030:
	lea	rcx, -1[rdx]
	mov	eax, ebx
	shr	al, 2
	and	eax, 3
	test	esi, esi
	jns	.L1031
.L1099:
	mov	BYTE PTR -1[rdx], 45
	mov	rdx, rcx
.L1058:
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
	jmp	.L1011
	.p2align 4,,10
	.p2align 3
.L1097:
	mov	ebx, esi
	neg	ebx
	cmp	al, 4
	je	.L1013
	ja	.L1014
	cmp	al, 1
	jbe	.L1015
	lea	r14, .LC21[rip]
	cmp	dl, 16
	lea	rax, .LC22[rip]
	cmovne	r14, rax
.L1016:
	bsr	r8d, ebx
	mov	r12d, 32
	xor	r8d, 31
	mov	eax, 31
	sub	r12d, r8d
	sub	eax, r8d
	je	.L1028
	mov	edx, eax
	lea	rcx, 63[rsp+rdx]
	lea	rax, 64[rsp+rdx]
	mov	edx, 30
	sub	edx, r8d
	sub	rcx, rdx
	.p2align 4,,10
	.p2align 3
.L1027:
	mov	edx, ebx
	sub	rax, 1
	shr	ebx
	and	edx, 1
	add	edx, 48
	mov	BYTE PTR 4[rax], dl
	cmp	rax, rcx
	jne	.L1027
.L1028:
	lea	r13, 67[rsp]
	movsx	r12, r12d
	mov	eax, 49
	add	r12, r13
	jmp	.L1025
	.p2align 4,,10
	.p2align 3
.L1096:
	lea	eax, 128[rsi]
	cmp	eax, 255
	ja	.L1010
	lea	rax, 112[rsp]
	mov	r9, rdi
	mov	edx, 1
	mov	BYTE PTR 112[rsp], sil
	lea	rcx, 48[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1011:
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
.L1019:
	cmp	dl, 40
	je	.L1098
	test	esi, esi
	jne	.L1074
	movzx	ebx, BYTE PTR [rcx]
	mov	BYTE PTR 67[rsp], 48
	lea	r12, 68[rsp]
	cmp	dl, 48
	lea	r14, .LC24[rip]
	lea	r13, 67[rsp]
	je	.L1049
.L1050:
	test	bl, 16
	jne	.L1077
	.p2align 4,,10
	.p2align 3
.L1078:
	mov	rdx, r13
.L1102:
	lea	rcx, -1[rdx]
	mov	eax, ebx
	shr	al, 2
	and	eax, 3
	test	esi, esi
	js	.L1099
.L1031:
	movzx	eax, al
	cmp	eax, 1
	je	.L1100
	cmp	eax, 3
	jne	.L1058
	mov	BYTE PTR -1[rdx], 32
.L1061:
	mov	rdx, rcx
	jmp	.L1058
	.p2align 4,,10
	.p2align 3
.L1014:
	lea	r14, .LC25[rip]
	cmp	dl, 40
	lea	rax, .LC24[rip]
	cmovne	r14, rax
.L1017:
	bsr	eax, ebx
	lea	r9d, 4[rax]
	movabs	rax, 3978425819141910832
	shr	r9d, 2
	mov	QWORD PTR 112[rsp], rax
	cmp	ebx, 255
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 120[rsp], rax
	lea	eax, -1[r9]
	jbe	.L1051
	.p2align 4,,10
	.p2align 3
.L1052:
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
	ja	.L1052
.L1051:
	cmp	ebx, 15
	ja	.L1101
	movzx	eax, BYTE PTR 112[rsp+rbx]
.L1054:
	lea	r13, 67[rsp]
	mov	r12d, r9d
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], al
	add	r12, r13
	cmp	dl, 48
	jne	.L1050
	test	r9d, r9d
	jne	.L1049
	mov	ecx, 1
	mov	eax, 2
	mov	r12, r13
	jmp	.L1048
	.p2align 4,,10
	.p2align 3
.L1049:
	mov	r15, r13
	.p2align 4,,10
	.p2align 3
.L1055:
	movsx	ecx, BYTE PTR [r15]
	add	r15, 1
	call	toupper
	mov	BYTE PTR -1[r15], al
	cmp	r15, r12
	jne	.L1055
	mov	ecx, 1
	mov	eax, 2
	jmp	.L1048
	.p2align 4,,10
	.p2align 3
.L1100:
	mov	BYTE PTR -1[rdx], 43
	jmp	.L1061
	.p2align 4,,10
	.p2align 3
.L1020:
	test	esi, esi
	jne	.L1015
	movzx	eax, BYTE PTR [rcx]
	lea	r13, 67[rsp]
	mov	BYTE PTR 67[rsp], 48
	lea	r12, 68[rsp]
	mov	rdx, r13
	lea	rcx, 66[rsp]
	shr	al, 2
	and	eax, 3
	jmp	.L1031
	.p2align 4,,10
	.p2align 3
.L1018:
	test	esi, esi
	jne	.L1013
	xor	ecx, ecx
	xor	eax, eax
	xor	r14d, r14d
	lea	r12, 68[rsp]
	mov	edx, 48
	lea	r13, 67[rsp]
.L1043:
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], dl
.L1048:
	test	bl, 16
	je	.L1078
	mov	rdx, rax
	neg	rdx
	test	cl, cl
	jne	.L1029
	mov	rdx, r13
	jmp	.L1102
	.p2align 4,,10
	.p2align 3
.L1015:
	cmp	ebx, 9
	jbe	.L1066
	cmp	ebx, 99
	jbe	.L1103
	cmp	ebx, 999
	jbe	.L1067
	cmp	ebx, 9999
	jbe	.L1104
	cmp	ebx, 99999
	mov	r12d, 5
	jbe	.L1038
	cmp	ebx, 999999
	jbe	.L1105
	cmp	ebx, 9999999
	jbe	.L1069
	cmp	ebx, 99999999
	jbe	.L1070
	cmp	ebx, 999999999
	jbe	.L1071
	mov	r12d, 5
.L1039:
	add	r12d, 5
.L1038:
	lea	r13d, -1[r12]
.L1035:
	lea	rcx, 112[rsp]
	mov	r8d, 201
	lea	rdx, .LC27[rip]
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L1041:
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
	ja	.L1041
	cmp	ecx, 999
	ja	.L1034
.L1032:
	add	ebx, 48
.L1042:
	lea	r13, 67[rsp]
	mov	BYTE PTR 67[rsp], bl
	movzx	ebx, BYTE PTR [rdi]
	add	r12, r13
	mov	rdx, r13
	jmp	.L1030
	.p2align 4,,10
	.p2align 3
.L1013:
	bsr	eax, ebx
	lea	r12d, 3[rax]
	mov	eax, 2863311531
	imul	r12, rax
	shr	r12, 33
	cmp	ebx, 63
	lea	edx, -1[r12]
	jbe	.L1044
	.p2align 4,,10
	.p2align 3
.L1045:
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
	ja	.L1045
.L1044:
	lea	edx, 48[rbx]
	cmp	ebx, 7
	jbe	.L1047
	mov	eax, ebx
	shr	ebx, 3
	and	eax, 7
	mov	edx, ebx
	add	eax, 48
	add	edx, 48
	mov	BYTE PTR 68[rsp], al
.L1047:
	lea	r13, 67[rsp]
	mov	r12d, r12d
	mov	ecx, 1
	lea	r14, .LC23[rip]
	add	r12, r13
	mov	eax, 1
	jmp	.L1043
	.p2align 4,,10
	.p2align 3
.L1101:
	mov	eax, ebx
	shr	ebx, 4
	and	eax, 15
	movzx	eax, BYTE PTR 112[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	movzx	eax, BYTE PTR 112[rsp+rbx]
	jmp	.L1054
.L1103:
	lea	rcx, 112[rsp]
	mov	r8d, 201
	mov	r12d, 2
	lea	rdx, .LC27[rip]
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L1034:
	add	ebx, ebx
	lea	eax, 1[rbx]
	movzx	ebx, BYTE PTR 112[rsp+rbx]
	movzx	eax, BYTE PTR 112[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	jmp	.L1042
	.p2align 4,,10
	.p2align 3
.L1098:
	test	esi, esi
	jne	.L1073
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], 48
	mov	ecx, 1
	mov	eax, 2
	lea	r14, .LC25[rip]
	lea	r12, 68[rsp]
	lea	r13, 67[rsp]
	jmp	.L1048
	.p2align 4,,10
	.p2align 3
.L1069:
	mov	r12d, 7
	jmp	.L1038
	.p2align 4,,10
	.p2align 3
.L1070:
	mov	r12d, 8
	jmp	.L1038
	.p2align 4,,10
	.p2align 3
.L1071:
	mov	r12d, 9
	jmp	.L1038
	.p2align 4,,10
	.p2align 3
.L1074:
	lea	r14, .LC24[rip]
	jmp	.L1017
.L1073:
	lea	r14, .LC25[rip]
	jmp	.L1017
.L1066:
	mov	r12d, 1
	jmp	.L1032
.L1104:
	mov	r12d, 4
	mov	r13d, 3
	jmp	.L1035
.L1067:
	mov	r12d, 3
	mov	r13d, 2
	jmp	.L1035
.L1105:
	mov	r12d, 1
	jmp	.L1039
.L1010:
	lea	rcx, .LC26[rip]
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
.LFB5395:
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
	je	.L1186
	shr	al, 3
	and	eax, 15
	cmp	al, 4
	je	.L1110
	ja	.L1111
	cmp	al, 1
	jbe	.L1112
	lea	rbp, .LC21[rip]
	cmp	dl, 16
	lea	rax, .LC22[rip]
	cmovne	rbp, rax
	test	ebx, ebx
	jne	.L1187
	lea	rbx, 68[rsp]
	mov	eax, 48
	lea	r12, 67[rsp]
.L1117:
	mov	BYTE PTR 67[rsp], al
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	je	.L1169
.L1168:
	mov	rdx, -2
	mov	ecx, 2
.L1121:
	add	rdx, r12
	test	ecx, ecx
	mov	r10d, ecx
	je	.L1122
	xor	ecx, ecx
.L1150:
	mov	r8d, ecx
	add	ecx, 1
	movzx	r9d, BYTE PTR 0[rbp+r8]
	cmp	ecx, r10d
	mov	BYTE PTR [rdx+r8], r9b
	jb	.L1150
	jmp	.L1122
	.p2align 4,,10
	.p2align 3
.L1186:
	cmp	ebx, 127
	ja	.L1108
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
.L1112:
	test	ebx, ebx
	jne	.L1123
	mov	BYTE PTR 67[rsp], 48
	lea	rbx, 68[rsp]
	lea	r12, 67[rsp]
.L1124:
	movzx	eax, BYTE PTR [rsi]
	mov	rdx, r12
.L1122:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L1188
.L1152:
	cmp	eax, 3
	je	.L1170
.L1153:
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
.L1110:
	test	ebx, ebx
	je	.L1163
	bsr	eax, ebx
	lea	r8d, 3[rax]
	mov	eax, 2863311531
	imul	r8, rax
	shr	r8, 33
	cmp	ebx, 63
	lea	edx, -1[r8]
	jbe	.L1137
	.p2align 4,,10
	.p2align 3
.L1138:
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
	ja	.L1138
.L1137:
	lea	eax, 48[rbx]
	cmp	ebx, 7
	ja	.L1189
.L1140:
	lea	r12, 67[rsp]
	mov	ebx, r8d
	mov	edx, 1
	lea	rbp, .LC23[rip]
	add	rbx, r12
	mov	ecx, 1
.L1136:
	mov	BYTE PTR 67[rsp], al
.L1141:
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	je	.L1169
	test	dl, dl
	jne	.L1190
.L1169:
	shr	al, 2
	mov	rdx, r12
	and	eax, 3
	cmp	eax, 1
	jne	.L1152
.L1188:
	mov	eax, 43
.L1154:
	mov	BYTE PTR -1[rdx], al
	sub	rdx, 1
	jmp	.L1153
	.p2align 4,,10
	.p2align 3
.L1111:
	cmp	dl, 40
	je	.L1191
	test	ebx, ebx
	jne	.L1165
	cmp	dl, 48
	mov	BYTE PTR 67[rsp], 48
	je	.L1166
	lea	rbp, .LC24[rip]
	lea	rbx, 68[rsp]
	lea	r12, 67[rsp]
	jmp	.L1143
	.p2align 4,,10
	.p2align 3
.L1170:
	mov	eax, 32
	jmp	.L1154
	.p2align 4,,10
	.p2align 3
.L1123:
	cmp	ebx, 9
	jbe	.L1157
	cmp	ebx, 99
	jbe	.L1192
	cmp	ebx, 999
	jbe	.L1158
	cmp	ebx, 9999
	jbe	.L1193
	cmp	ebx, 99999
	mov	ebp, 5
	jbe	.L1131
	cmp	ebx, 999999
	jbe	.L1194
	cmp	ebx, 9999999
	jbe	.L1160
	cmp	ebx, 99999999
	jbe	.L1161
	cmp	ebx, 999999999
	jbe	.L1162
	mov	ebp, 5
.L1132:
	add	ebp, 5
.L1131:
	lea	r12d, -1[rbp]
.L1128:
	lea	rcx, 112[rsp]
	mov	r8d, 201
	lea	rdx, .LC27[rip]
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L1134:
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
	ja	.L1134
	cmp	ecx, 999
	jbe	.L1125
.L1127:
	add	ebx, ebx
	lea	eax, 1[rbx]
	movzx	ebx, BYTE PTR 112[rsp+rbx]
	movzx	eax, BYTE PTR 112[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	jmp	.L1135
	.p2align 4,,10
	.p2align 3
.L1187:
	bsr	r8d, ebx
	mov	r9d, 32
	mov	eax, 31
	xor	r8d, 31
	sub	r9d, r8d
	sub	eax, r8d
	je	.L1120
	mov	edx, eax
	lea	rcx, 63[rsp+rdx]
	lea	rax, 64[rsp+rdx]
	mov	edx, 30
	sub	edx, r8d
	sub	rcx, rdx
	.p2align 4,,10
	.p2align 3
.L1119:
	mov	edx, ebx
	sub	rax, 1
	shr	ebx
	and	edx, 1
	add	edx, 48
	mov	BYTE PTR 4[rax], dl
	cmp	rax, rcx
	jne	.L1119
.L1120:
	lea	r12, 67[rsp]
	movsx	rbx, r9d
	mov	eax, 49
	add	rbx, r12
	jmp	.L1117
	.p2align 4,,10
	.p2align 3
.L1163:
	mov	eax, 48
	xor	edx, edx
	xor	ebp, ebp
	lea	rbx, 68[rsp]
	xor	ecx, ecx
	lea	r12, 67[rsp]
	jmp	.L1136
	.p2align 4,,10
	.p2align 3
.L1191:
	test	ebx, ebx
	jne	.L1164
	mov	BYTE PTR 67[rsp], 48
	lea	rbp, .LC25[rip]
	lea	rbx, 68[rsp]
	lea	r12, 67[rsp]
	jmp	.L1143
	.p2align 4,,10
	.p2align 3
.L1165:
	lea	rbp, .LC24[rip]
.L1142:
	bsr	eax, ebx
	lea	r9d, 4[rax]
	movabs	rax, 3978425819141910832
	shr	r9d, 2
	mov	QWORD PTR 112[rsp], rax
	cmp	ebx, 255
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 120[rsp], rax
	lea	eax, -1[r9]
	jbe	.L1145
	.p2align 4,,10
	.p2align 3
.L1146:
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
	ja	.L1146
.L1145:
	cmp	ebx, 15
	ja	.L1195
	movzx	eax, BYTE PTR 112[rsp+rbx]
.L1148:
	lea	r12, 67[rsp]
	mov	ebx, r9d
	mov	BYTE PTR 67[rsp], al
	add	rbx, r12
	cmp	dl, 48
	je	.L1196
.L1143:
	movzx	eax, BYTE PTR [rsi]
	test	al, 16
	jne	.L1168
	jmp	.L1169
	.p2align 4,,10
	.p2align 3
.L1195:
	mov	eax, ebx
	shr	ebx, 4
	and	eax, 15
	movzx	eax, BYTE PTR 112[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	movzx	eax, BYTE PTR 112[rsp+rbx]
	jmp	.L1148
	.p2align 4,,10
	.p2align 3
.L1189:
	mov	eax, ebx
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 68[rsp], al
	mov	eax, ebx
	shr	eax, 3
	add	eax, 48
	jmp	.L1140
.L1157:
	mov	ebp, 1
	.p2align 4,,10
	.p2align 3
.L1125:
	add	ebx, 48
.L1135:
	lea	r12, 67[rsp]
	mov	BYTE PTR 67[rsp], bl
	lea	rbx, [r12+rbp]
	jmp	.L1124
	.p2align 4,,10
	.p2align 3
.L1164:
	lea	rbp, .LC25[rip]
	jmp	.L1142
	.p2align 4,,10
	.p2align 3
.L1166:
	lea	rbx, 68[rsp]
	lea	rbp, .LC24[rip]
	lea	r12, 67[rsp]
.L1144:
	mov	r13, r12
	.p2align 4,,10
	.p2align 3
.L1149:
	movsx	ecx, BYTE PTR 0[r13]
	add	r13, 1
	call	toupper
	mov	BYTE PTR -1[r13], al
	cmp	r13, rbx
	jne	.L1149
	mov	edx, 1
	mov	ecx, 2
	jmp	.L1141
	.p2align 4,,10
	.p2align 3
.L1196:
	test	r9d, r9d
	jne	.L1144
	mov	edx, 1
	mov	ecx, 2
	mov	rbx, r12
	jmp	.L1141
	.p2align 4,,10
	.p2align 3
.L1160:
	mov	ebp, 7
	jmp	.L1131
	.p2align 4,,10
	.p2align 3
.L1161:
	mov	ebp, 8
	jmp	.L1131
	.p2align 4,,10
	.p2align 3
.L1162:
	mov	ebp, 9
	jmp	.L1131
	.p2align 4,,10
	.p2align 3
.L1190:
	mov	rdx, rcx
	neg	rdx
	jmp	.L1121
.L1192:
	lea	rcx, 112[rsp]
	mov	r8d, 201
	mov	ebp, 2
	lea	rdx, .LC27[rip]
	call	memcpy
	jmp	.L1127
.L1158:
	mov	ebp, 3
	mov	r12d, 2
	jmp	.L1128
.L1193:
	mov	ebp, 4
	mov	r12d, 3
	jmp	.L1128
.L1194:
	mov	ebp, 1
	jmp	.L1132
.L1108:
	lea	rcx, .LC26[rip]
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
.LFB5397:
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
	je	.L1284
	shr	al, 3
	and	eax, 15
	test	r12, r12
	js	.L1285
	cmp	al, 4
	je	.L1207
	ja	.L1208
	cmp	al, 1
	jbe	.L1209
	lea	r14, .LC21[rip]
	cmp	dl, 16
	lea	rax, .LC22[rip]
	cmovne	r14, rax
	test	r12, r12
	jne	.L1205
	lea	rsi, 68[rsp]
	mov	eax, 48
	lea	r13, 67[rsp]
.L1214:
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], al
	test	bl, 16
	je	.L1266
.L1265:
	mov	rdx, -2
	mov	eax, 2
.L1218:
	add	rdx, r13
	test	eax, eax
	mov	r9d, eax
	je	.L1219
	xor	eax, eax
.L1246:
	mov	ecx, eax
	add	eax, 1
	movzx	r8d, BYTE PTR [r14+rcx]
	cmp	eax, r9d
	mov	BYTE PTR [rdx+rcx], r8b
	jb	.L1246
	.p2align 4,,10
	.p2align 3
.L1219:
	lea	rcx, -1[rdx]
	mov	eax, ebx
	shr	al, 2
	and	eax, 3
	test	r12, r12
	jns	.L1220
	mov	BYTE PTR -1[rdx], 45
	mov	rdx, rcx
.L1248:
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
	jmp	.L1200
	.p2align 4,,10
	.p2align 3
.L1285:
	neg	rbx
	cmp	al, 4
	je	.L1202
	ja	.L1203
	cmp	al, 1
	jbe	.L1204
	lea	r14, .LC21[rip]
	cmp	dl, 16
	lea	rax, .LC22[rip]
	cmovne	r14, rax
.L1205:
	bsr	r8, rbx
	mov	esi, 64
	xor	r8, 63
	mov	eax, 63
	sub	esi, r8d
	sub	eax, r8d
	je	.L1217
	mov	edx, eax
	lea	rcx, 63[rsp+rdx]
	lea	rax, 64[rsp+rdx]
	mov	edx, 62
	sub	edx, r8d
	sub	rcx, rdx
	.p2align 4,,10
	.p2align 3
.L1216:
	mov	edx, ebx
	sub	rax, 1
	shr	rbx
	and	edx, 1
	add	edx, 48
	mov	BYTE PTR 4[rax], dl
	cmp	rax, rcx
	jne	.L1216
.L1217:
	lea	r13, 67[rsp]
	movsx	rsi, esi
	mov	eax, 49
	add	rsi, r13
	jmp	.L1214
	.p2align 4,,10
	.p2align 3
.L1284:
	lea	rax, 128[r12]
	cmp	rax, 255
	ja	.L1199
	lea	rax, 144[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	r9, rdi
	mov	edx, 1
	lea	rcx, 48[rsp]
	mov	BYTE PTR 144[rsp], r12b
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1200:
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
.L1208:
	cmp	dl, 40
	je	.L1286
	test	r12, r12
	jne	.L1262
	movzx	ebx, BYTE PTR [rcx]
	mov	BYTE PTR 67[rsp], 48
	lea	rsi, 68[rsp]
	cmp	dl, 48
	lea	r14, .LC24[rip]
	lea	r13, 67[rsp]
	je	.L1239
.L1240:
	test	bl, 16
	jne	.L1265
	.p2align 4,,10
	.p2align 3
.L1266:
	mov	rdx, r13
	jmp	.L1219
	.p2align 4,,10
	.p2align 3
.L1203:
	lea	r14, .LC25[rip]
	cmp	dl, 40
	lea	rax, .LC24[rip]
	cmovne	r14, rax
.L1206:
	bsr	rax, rbx
	lea	r9d, 4[rax]
	movabs	rax, 3978425819141910832
	shr	r9d, 2
	mov	QWORD PTR 144[rsp], rax
	cmp	rbx, 255
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 152[rsp], rax
	lea	eax, -1[r9]
	jbe	.L1241
	.p2align 4,,10
	.p2align 3
.L1242:
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
	ja	.L1242
.L1241:
	cmp	rbx, 15
	ja	.L1287
	movzx	eax, BYTE PTR 144[rsp+rbx]
.L1244:
	lea	r13, 67[rsp]
	mov	esi, r9d
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], al
	add	rsi, r13
	cmp	dl, 48
	jne	.L1240
	test	r9d, r9d
	jne	.L1239
	mov	ecx, 1
	mov	eax, 2
	mov	rsi, r13
	jmp	.L1238
	.p2align 4,,10
	.p2align 3
.L1239:
	mov	r15, r13
	.p2align 4,,10
	.p2align 3
.L1245:
	movsx	ecx, BYTE PTR [r15]
	add	r15, 1
	call	toupper
	mov	BYTE PTR -1[r15], al
	cmp	rsi, r15
	jne	.L1245
	mov	ecx, 1
	mov	eax, 2
	jmp	.L1238
	.p2align 4,,10
	.p2align 3
.L1209:
	test	r12, r12
	jne	.L1204
	movzx	eax, BYTE PTR [rcx]
	lea	r13, 67[rsp]
	mov	BYTE PTR 67[rsp], 48
	lea	rsi, 68[rsp]
	mov	rdx, r13
	lea	rcx, 66[rsp]
	shr	al, 2
	and	eax, 3
.L1220:
	movzx	eax, al
	cmp	eax, 1
	je	.L1288
	cmp	eax, 3
	jne	.L1248
	mov	BYTE PTR -1[rdx], 32
.L1251:
	mov	rdx, rcx
	jmp	.L1248
	.p2align 4,,10
	.p2align 3
.L1288:
	mov	BYTE PTR -1[rdx], 43
	jmp	.L1251
	.p2align 4,,10
	.p2align 3
.L1207:
	test	r12, r12
	jne	.L1202
	xor	ecx, ecx
	xor	eax, eax
	xor	r14d, r14d
	lea	rsi, 68[rsp]
	mov	edx, 48
	lea	r13, 67[rsp]
.L1233:
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], dl
.L1238:
	test	bl, 16
	je	.L1266
	mov	rdx, rax
	neg	rdx
	test	cl, cl
	jne	.L1218
	mov	rdx, r13
	jmp	.L1219
	.p2align 4,,10
	.p2align 3
.L1204:
	cmp	rbx, 9
	jbe	.L1256
	cmp	rbx, 99
	jbe	.L1289
	cmp	rbx, 999
	jbe	.L1257
	cmp	rbx, 9999
	jbe	.L1258
	mov	rdx, rbx
	mov	esi, 1
	movabs	r8, 3777893186295716171
	jmp	.L1225
	.p2align 4,,10
	.p2align 3
.L1229:
	cmp	rcx, 999999
	jbe	.L1290
	cmp	rcx, 9999999
	jbe	.L1291
	cmp	rcx, 99999999
	jbe	.L1292
.L1225:
	mov	rax, rdx
	mov	rcx, rdx
	mul	r8
	mov	eax, esi
	add	esi, 4
	shr	rdx, 11
	cmp	rcx, 99999
	ja	.L1229
.L1227:
	cmp	esi, 64
	ja	.L1259
	lea	r13d, -1[rsi]
.L1224:
	lea	rcx, 144[rsp]
	mov	r8d, 201
	lea	rdx, .LC27[rip]
	call	memcpy
	movabs	r8, 2951479051793528259
	.p2align 4,,10
	.p2align 3
.L1231:
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
	ja	.L1231
	cmp	rcx, 999
	ja	.L1223
.L1221:
	add	ebx, 48
.L1232:
	lea	r13, 67[rsp]
	mov	BYTE PTR 67[rsp], bl
	add	rsi, r13
.L1230:
	movzx	ebx, BYTE PTR [rdi]
	mov	rdx, r13
	jmp	.L1219
	.p2align 4,,10
	.p2align 3
.L1202:
	bsr	rax, rbx
	lea	esi, 3[rax]
	mov	eax, 2863311531
	imul	rsi, rax
	shr	rsi, 33
	cmp	rbx, 63
	lea	edx, -1[rsi]
	jbe	.L1234
	.p2align 4,,10
	.p2align 3
.L1235:
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
	ja	.L1235
.L1234:
	lea	edx, 48[rbx]
	cmp	rbx, 7
	jbe	.L1237
	mov	rax, rbx
	shr	rbx, 3
	and	eax, 7
	mov	rdx, rbx
	add	eax, 48
	add	edx, 48
	mov	BYTE PTR 68[rsp], al
.L1237:
	lea	r13, 67[rsp]
	mov	esi, esi
	mov	ecx, 1
	lea	r14, .LC23[rip]
	add	rsi, r13
	mov	eax, 1
	jmp	.L1233
	.p2align 4,,10
	.p2align 3
.L1287:
	mov	rax, rbx
	shr	rbx, 4
	and	eax, 15
	movzx	eax, BYTE PTR 144[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	movzx	eax, BYTE PTR 144[rsp+rbx]
	jmp	.L1244
.L1289:
	lea	rcx, 144[rsp]
	mov	r8d, 201
	mov	esi, 2
	lea	rdx, .LC27[rip]
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L1223:
	add	rbx, rbx
	movzx	eax, BYTE PTR 145[rsp+rbx]
	movzx	ebx, BYTE PTR 144[rsp+rbx]
	mov	BYTE PTR 68[rsp], al
	jmp	.L1232
	.p2align 4,,10
	.p2align 3
.L1286:
	test	r12, r12
	jne	.L1261
	movzx	ebx, BYTE PTR [rdi]
	mov	BYTE PTR 67[rsp], 48
	mov	ecx, 1
	mov	eax, 2
	lea	r14, .LC25[rip]
	lea	rsi, 68[rsp]
	lea	r13, 67[rsp]
	jmp	.L1238
	.p2align 4,,10
	.p2align 3
.L1290:
	lea	esi, 5[rax]
	jmp	.L1227
	.p2align 4,,10
	.p2align 3
.L1291:
	lea	esi, 6[rax]
	jmp	.L1227
	.p2align 4,,10
	.p2align 3
.L1292:
	lea	esi, 7[rax]
	jmp	.L1227
	.p2align 4,,10
	.p2align 3
.L1262:
	lea	r14, .LC24[rip]
	jmp	.L1206
.L1259:
	lea	rsi, 131[rsp]
	lea	r13, 67[rsp]
	jmp	.L1230
.L1261:
	lea	r14, .LC25[rip]
	jmp	.L1206
.L1256:
	mov	esi, 1
	jmp	.L1221
.L1258:
	mov	esi, 4
	mov	r13d, 3
	jmp	.L1224
.L1257:
	mov	esi, 3
	mov	r13d, 2
	jmp	.L1224
.L1199:
	lea	rcx, .LC26[rip]
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
.LFB5399:
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
	je	.L1371
	shr	al, 3
	and	eax, 15
	cmp	al, 4
	je	.L1297
	ja	.L1298
	cmp	al, 1
	jbe	.L1299
	lea	r13, .LC21[rip]
	cmp	dl, 16
	lea	rax, .LC22[rip]
	cmovne	r13, rax
	test	rbx, rbx
	jne	.L1372
	lea	rsi, 68[rsp]
	mov	eax, 48
	lea	r12, 67[rsp]
.L1304:
	mov	BYTE PTR 67[rsp], al
	movzx	eax, BYTE PTR [rdi]
	test	al, 16
	je	.L1354
.L1353:
	mov	rdx, -2
	mov	ebx, 2
.L1308:
	add	rdx, r12
	test	ebx, ebx
	mov	r10d, ebx
	je	.L1309
	xor	ecx, ecx
.L1337:
	mov	r8d, ecx
	add	ecx, 1
	movzx	r9d, BYTE PTR 0[r13+r8]
	cmp	ecx, r10d
	mov	BYTE PTR [rdx+r8], r9b
	jb	.L1337
	jmp	.L1309
	.p2align 4,,10
	.p2align 3
.L1371:
	cmp	rbx, 127
	ja	.L1295
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
.L1299:
	test	rbx, rbx
	jne	.L1310
	mov	BYTE PTR 67[rsp], 48
	lea	rsi, 68[rsp]
	lea	r12, 67[rsp]
.L1311:
	movzx	eax, BYTE PTR [rdi]
	mov	rdx, r12
.L1309:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L1373
.L1339:
	cmp	eax, 3
	je	.L1355
.L1340:
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
.L1297:
	test	rbx, rbx
	je	.L1348
	bsr	rax, rbx
	lea	esi, 3[rax]
	mov	eax, 2863311531
	imul	rsi, rax
	shr	rsi, 33
	cmp	rbx, 63
	lea	edx, -1[rsi]
	jbe	.L1324
	.p2align 4,,10
	.p2align 3
.L1325:
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
	ja	.L1325
.L1324:
	lea	eax, 48[rbx]
	cmp	rbx, 7
	ja	.L1374
.L1327:
	lea	r12, 67[rsp]
	mov	esi, esi
	mov	edx, 1
	lea	r13, .LC23[rip]
	add	rsi, r12
	mov	ebx, 1
.L1323:
	mov	BYTE PTR 67[rsp], al
.L1328:
	movzx	eax, BYTE PTR [rdi]
	test	al, 16
	je	.L1354
	test	dl, dl
	jne	.L1375
.L1354:
	shr	al, 2
	mov	rdx, r12
	and	eax, 3
	cmp	eax, 1
	jne	.L1339
.L1373:
	mov	eax, 43
.L1341:
	mov	BYTE PTR -1[rdx], al
	sub	rdx, 1
	jmp	.L1340
	.p2align 4,,10
	.p2align 3
.L1298:
	cmp	dl, 40
	je	.L1376
	test	rbx, rbx
	jne	.L1350
	cmp	dl, 48
	mov	BYTE PTR 67[rsp], 48
	je	.L1351
	lea	r13, .LC24[rip]
	lea	rsi, 68[rsp]
	lea	r12, 67[rsp]
	jmp	.L1330
	.p2align 4,,10
	.p2align 3
.L1355:
	mov	eax, 32
	jmp	.L1341
	.p2align 4,,10
	.p2align 3
.L1310:
	cmp	rbx, 9
	jbe	.L1344
	cmp	rbx, 99
	jbe	.L1377
	cmp	rbx, 999
	jbe	.L1345
	cmp	rbx, 9999
	jbe	.L1346
	mov	rdx, rbx
	mov	esi, 1
	movabs	r8, 3777893186295716171
	jmp	.L1316
	.p2align 4,,10
	.p2align 3
.L1320:
	cmp	rcx, 999999
	jbe	.L1378
	cmp	rcx, 9999999
	jbe	.L1379
	cmp	rcx, 99999999
	jbe	.L1380
.L1316:
	mov	rax, rdx
	mov	rcx, rdx
	mul	r8
	mov	eax, esi
	add	esi, 4
	shr	rdx, 11
	cmp	rcx, 99999
	ja	.L1320
.L1318:
	cmp	esi, 64
	ja	.L1347
	lea	r12d, -1[rsi]
.L1315:
	lea	rcx, 144[rsp]
	mov	r8d, 201
	lea	rdx, .LC27[rip]
	call	memcpy
	movabs	r8, 2951479051793528259
	.p2align 4,,10
	.p2align 3
.L1321:
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
	ja	.L1321
	cmp	rcx, 999
	jbe	.L1312
.L1314:
	add	rbx, rbx
	movzx	eax, BYTE PTR 145[rsp+rbx]
	movzx	ebx, BYTE PTR 144[rsp+rbx]
	mov	BYTE PTR 68[rsp], al
	jmp	.L1322
	.p2align 4,,10
	.p2align 3
.L1372:
	bsr	r8, rbx
	mov	esi, 64
	mov	eax, 63
	xor	r8, 63
	sub	esi, r8d
	sub	eax, r8d
	je	.L1307
	mov	edx, eax
	lea	rcx, 63[rsp+rdx]
	lea	rax, 64[rsp+rdx]
	mov	edx, 62
	sub	edx, r8d
	sub	rcx, rdx
	.p2align 4,,10
	.p2align 3
.L1306:
	mov	edx, ebx
	sub	rax, 1
	shr	rbx
	and	edx, 1
	add	edx, 48
	mov	BYTE PTR 4[rax], dl
	cmp	rax, rcx
	jne	.L1306
.L1307:
	lea	r12, 67[rsp]
	movsx	rsi, esi
	mov	eax, 49
	add	rsi, r12
	jmp	.L1304
	.p2align 4,,10
	.p2align 3
.L1348:
	mov	eax, 48
	xor	edx, edx
	xor	r13d, r13d
	lea	rsi, 68[rsp]
	lea	r12, 67[rsp]
	jmp	.L1323
	.p2align 4,,10
	.p2align 3
.L1376:
	test	rbx, rbx
	jne	.L1349
	mov	BYTE PTR 67[rsp], 48
	lea	r13, .LC25[rip]
	lea	rsi, 68[rsp]
	lea	r12, 67[rsp]
	jmp	.L1330
	.p2align 4,,10
	.p2align 3
.L1350:
	lea	r13, .LC24[rip]
.L1329:
	bsr	rax, rbx
	lea	r9d, 4[rax]
	movabs	rax, 3978425819141910832
	shr	r9d, 2
	mov	QWORD PTR 144[rsp], rax
	cmp	rbx, 255
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 152[rsp], rax
	lea	eax, -1[r9]
	jbe	.L1332
	.p2align 4,,10
	.p2align 3
.L1333:
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
	ja	.L1333
.L1332:
	cmp	rbx, 15
	ja	.L1381
	movzx	eax, BYTE PTR 144[rsp+rbx]
.L1335:
	lea	r12, 67[rsp]
	mov	esi, r9d
	mov	BYTE PTR 67[rsp], al
	add	rsi, r12
	cmp	dl, 48
	je	.L1382
.L1330:
	movzx	eax, BYTE PTR [rdi]
	test	al, 16
	jne	.L1353
	jmp	.L1354
	.p2align 4,,10
	.p2align 3
.L1381:
	mov	rax, rbx
	shr	rbx, 4
	and	eax, 15
	movzx	eax, BYTE PTR 144[rsp+rax]
	mov	BYTE PTR 68[rsp], al
	movzx	eax, BYTE PTR 144[rsp+rbx]
	jmp	.L1335
	.p2align 4,,10
	.p2align 3
.L1374:
	mov	rax, rbx
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 68[rsp], al
	mov	rax, rbx
	shr	rax, 3
	add	eax, 48
	jmp	.L1327
.L1344:
	mov	esi, 1
	.p2align 4,,10
	.p2align 3
.L1312:
	add	ebx, 48
.L1322:
	lea	r12, 67[rsp]
	mov	BYTE PTR 67[rsp], bl
	add	rsi, r12
	jmp	.L1311
	.p2align 4,,10
	.p2align 3
.L1349:
	lea	r13, .LC25[rip]
	jmp	.L1329
	.p2align 4,,10
	.p2align 3
.L1351:
	lea	rsi, 68[rsp]
	lea	r13, .LC24[rip]
	lea	r12, 67[rsp]
.L1331:
	mov	rbx, r12
	.p2align 4,,10
	.p2align 3
.L1336:
	movsx	ecx, BYTE PTR [rbx]
	add	rbx, 1
	call	toupper
	mov	BYTE PTR -1[rbx], al
	cmp	rbx, rsi
	jne	.L1336
	mov	edx, 1
	mov	ebx, 2
	jmp	.L1328
	.p2align 4,,10
	.p2align 3
.L1382:
	test	r9d, r9d
	jne	.L1331
	mov	edx, 1
	mov	ebx, 2
	mov	rsi, r12
	jmp	.L1328
	.p2align 4,,10
	.p2align 3
.L1378:
	lea	esi, 5[rax]
	jmp	.L1318
	.p2align 4,,10
	.p2align 3
.L1379:
	lea	esi, 6[rax]
	jmp	.L1318
	.p2align 4,,10
	.p2align 3
.L1380:
	lea	esi, 7[rax]
	jmp	.L1318
	.p2align 4,,10
	.p2align 3
.L1375:
	mov	rdx, rbx
	neg	rdx
	jmp	.L1308
.L1347:
	lea	rsi, 131[rsp]
	lea	r12, 67[rsp]
	jmp	.L1311
.L1377:
	lea	rcx, 144[rsp]
	mov	r8d, 201
	mov	esi, 2
	lea	rdx, .LC27[rip]
	call	memcpy
	jmp	.L1314
.L1345:
	mov	esi, 3
	mov	r12d, 2
	jmp	.L1315
.L1346:
	mov	esi, 4
	mov	r12d, 3
	jmp	.L1315
.L1295:
	lea	rcx, .LC26[rip]
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
.LFB5419:
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
	je	.L1477
	shr	al, 3
	mov	rsi, r12
	mov	rdi, r13
	and	eax, 15
	test	r13, r13
	js	.L1478
	cmp	al, 4
	je	.L1393
	ja	.L1394
	cmp	al, 1
	jbe	.L1395
	lea	rax, .LC22[rip]
	cmp	dl, 16
	lea	rbx, .LC21[rip]
	cmovne	rbx, rax
	mov	rax, r12
	or	rax, r13
	jne	.L1391
	lea	rdi, 148[rsp]
	mov	eax, 48
	lea	r8, 147[rsp]
.L1400:
	mov	BYTE PTR 147[rsp], al
	mov	rax, QWORD PTR 576[rsp]
	movzx	edx, BYTE PTR [rax]
	test	dl, 16
	je	.L1458
.L1457:
	mov	rcx, -2
	mov	eax, 2
.L1405:
	add	rcx, r8
	test	eax, eax
	mov	r11d, eax
	je	.L1406
	xor	eax, eax
.L1437:
	mov	r9d, eax
	add	eax, 1
	movzx	r10d, BYTE PTR [rbx+r9]
	cmp	eax, r11d
	mov	BYTE PTR [rcx+r9], r10b
	jb	.L1437
.L1406:
	lea	rax, -1[rcx]
	shr	dl, 2
	and	edx, 3
	test	r13, r13
	jns	.L1407
.L1485:
	mov	BYTE PTR -1[rcx], 45
	mov	rcx, rax
.L1439:
	sub	rdi, rcx
	mov	QWORD PTR 136[rsp], rcx
	sub	r8, rcx
	mov	r9, QWORD PTR 592[rsp]
	mov	rcx, QWORD PTR 576[rsp]
	lea	rdx, 128[rsp]
	mov	QWORD PTR 128[rsp], rdi
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L1386
	.p2align 4,,10
	.p2align 3
.L1478:
	neg	rsi
	adc	rdi, 0
	neg	rdi
	cmp	al, 4
	je	.L1388
	ja	.L1389
	cmp	al, 1
	jbe	.L1390
	lea	rbx, .LC21[rip]
	cmp	dl, 16
	lea	rax, .LC22[rip]
	cmovne	rbx, rax
.L1391:
	test	rdi, rdi
	jne	.L1479
	bsr	rdx, rsi
	mov	eax, 128
	mov	ecx, 127
	xor	rdx, 63
	add	edx, 64
	sub	eax, edx
	sub	ecx, edx
	je	.L1446
.L1402:
	mov	r8d, ecx
	sub	ecx, 1
	lea	rdx, 144[rsp+r8]
	lea	r8, 143[rsp+r8]
	sub	r8, rcx
	.p2align 4,,10
	.p2align 3
.L1404:
	mov	ecx, esi
	sub	rdx, 1
	shrd	rsi, rdi, 1
	and	ecx, 1
	shr	rdi
	add	ecx, 48
	mov	BYTE PTR 4[rdx], cl
	cmp	rdx, r8
	jne	.L1404
.L1403:
	lea	r8, 147[rsp]
	cdqe
	lea	rdi, [r8+rax]
	mov	eax, 49
	jmp	.L1400
	.p2align 4,,10
	.p2align 3
.L1477:
	mov	eax, 127
	cmp	rax, r12
	mov	eax, 0
	sbb	rax, r13
	jl	.L1385
	mov	r9, QWORD PTR 576[rsp]
	lea	rax, 288[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	edx, 1
	lea	rcx, 128[rsp]
	mov	BYTE PTR 288[rsp], r12b
	mov	QWORD PTR 128[rsp], 1
	mov	QWORD PTR 136[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1386:
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
.L1394:
	cmp	dl, 40
	je	.L1480
	mov	rax, r12
	or	rax, r13
	jne	.L1454
	cmp	dl, 48
	mov	BYTE PTR 147[rsp], 48
	je	.L1455
	lea	rbx, .LC24[rip]
	lea	rdi, 148[rsp]
	lea	r8, 147[rsp]
	jmp	.L1428
	.p2align 4,,10
	.p2align 3
.L1389:
	lea	rbx, .LC25[rip]
	cmp	dl, 40
	lea	rax, .LC24[rip]
	cmovne	rbx, rax
.L1392:
	test	rdi, rdi
	jne	.L1481
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
	jnb	.L1482
.L1431:
	lea	rcx, 288[rsp]
	mov	r11d, 255
	xor	r10d, r10d
	.p2align 4,,10
	.p2align 3
.L1433:
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
	jc	.L1433
.L1432:
	mov	eax, 15
	cmp	rax, rsi
	mov	eax, 0
	sbb	rax, rdi
	jc	.L1483
	add	rcx, rsi
	movzx	eax, BYTE PTR [rcx]
.L1435:
	lea	r8, 147[rsp]
	mov	edi, ebp
	mov	BYTE PTR 147[rsp], al
	add	rdi, r8
	cmp	dl, 48
	je	.L1484
.L1428:
	mov	rax, QWORD PTR 576[rsp]
	movzx	edx, BYTE PTR [rax]
	test	dl, 16
	jne	.L1457
	.p2align 4,,10
	.p2align 3
.L1458:
	shr	dl, 2
	mov	rcx, r8
	lea	rax, -1[rcx]
	and	edx, 3
	test	r13, r13
	js	.L1485
.L1407:
	movzx	edx, dl
	cmp	edx, 1
	je	.L1486
	cmp	edx, 3
	jne	.L1439
	mov	BYTE PTR -1[rcx], 32
.L1442:
	mov	rcx, rax
	jmp	.L1439
	.p2align 4,,10
	.p2align 3
.L1486:
	mov	BYTE PTR -1[rcx], 43
	jmp	.L1442
	.p2align 4,,10
	.p2align 3
.L1393:
	mov	rax, r12
	or	rax, r13
	jne	.L1388
	xor	ecx, ecx
	xor	eax, eax
	xor	ebx, ebx
	lea	rdi, 148[rsp]
	mov	esi, 48
	lea	r8, 147[rsp]
.L1420:
	mov	BYTE PTR 147[rsp], sil
.L1427:
	mov	rsi, QWORD PTR 576[rsp]
	movzx	edx, BYTE PTR [rsi]
	test	dl, 16
	je	.L1458
	test	cl, cl
	je	.L1458
	mov	rcx, rax
	neg	rcx
	jmp	.L1405
	.p2align 4,,10
	.p2align 3
.L1395:
	mov	rax, r12
	or	rax, r13
	jne	.L1390
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
	jmp	.L1407
	.p2align 4,,10
	.p2align 3
.L1390:
	xor	eax, eax
	mov	edx, 9
	cmp	rdx, rsi
	mov	rbx, rax
	sbb	rbx, rdi
	jnc	.L1448
	mov	edx, 99
	mov	rbx, rax
	cmp	rdx, rsi
	sbb	rbx, rdi
	jnc	.L1487
	mov	edx, 999
	mov	rbx, rax
	cmp	rdx, rsi
	sbb	rbx, rdi
	jnc	.L1449
	mov	edx, 9999
	cmp	rdx, rsi
	sbb	rax, rdi
	jnc	.L1450
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
	jmp	.L1412
	.p2align 4,,10
	.p2align 3
.L1416:
	mov	eax, 999999
	cmp	rax, rbp
	mov	rax, r15
	sbb	rax, rbx
	jnc	.L1488
	mov	eax, 9999999
	cmp	rax, rbp
	mov	rax, r15
	sbb	rax, rbx
	jnc	.L1489
	mov	eax, 99999999
	cmp	rax, rbp
	mov	rax, r15
	sbb	rax, rbx
	jnc	.L1490
.L1412:
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
	jc	.L1416
	mov	rsi, QWORD PTR 64[rsp]
	mov	rdi, QWORD PTR 72[rsp]
	mov	r12, QWORD PTR 80[rsp]
	mov	r13, QWORD PTR 88[rsp]
.L1414:
	cmp	r14d, 128
	ja	.L1451
	lea	ebx, -1[r14]
	mov	ebp, r14d
.L1411:
	lea	rcx, 288[rsp]
	mov	r8d, 201
	movabs	r14, 1152921504606846975
	lea	rdx, .LC27[rip]
	movabs	r15, -8116567392432202711
	call	memcpy
	mov	QWORD PTR 72[rsp], r13
	mov	r9d, ebx
	mov	r13, rbp
	mov	QWORD PTR 64[rsp], r12
	mov	rbp, rax
	.p2align 4,,10
	.p2align 3
.L1418:
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
	jc	.L1418
	mov	eax, 999
	mov	rcx, rbp
	mov	rbp, r13
	mov	r13, QWORD PTR 72[rsp]
	cmp	rax, r8
	mov	eax, 0
	sbb	rax, rdx
	jnc	.L1408
.L1410:
	add	rsi, rsi
	lea	rax, [rcx+rsi]
	add	rsi, rcx
	movzx	eax, BYTE PTR 1[rax]
	movzx	esi, BYTE PTR [rsi]
	mov	BYTE PTR 148[rsp], al
.L1419:
	lea	r8, 147[rsp]
	mov	BYTE PTR 147[rsp], sil
	lea	rdi, [r8+rbp]
.L1417:
	mov	rax, QWORD PTR 576[rsp]
	mov	rcx, r8
	movzx	edx, BYTE PTR [rax]
	jmp	.L1406
	.p2align 4,,10
	.p2align 3
.L1388:
	test	rdi, rdi
	jne	.L1491
	bsr	rax, rsi
	mov	edx, 2863311531
	mov	ecx, 63
	add	eax, 3
	imul	rax, rdx
	shr	rax, 33
	cmp	rcx, rsi
	lea	edx, -1[rax]
	jnb	.L1423
.L1422:
	mov	r9d, 63
	xor	r8d, r8d
	.p2align 4,,10
	.p2align 3
.L1424:
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
	jc	.L1424
.L1423:
	mov	edx, 7
	cmp	rdx, rsi
	mov	edx, 0
	sbb	rdx, rdi
	jc	.L1492
	add	esi, 48
.L1426:
	lea	r8, 147[rsp]
	mov	eax, eax
	mov	ecx, 1
	lea	rdi, [r8+rax]
	mov	eax, 1
	lea	rbx, .LC23[rip]
	jmp	.L1420
	.p2align 4,,10
	.p2align 3
.L1492:
	mov	rcx, rsi
	shrd	rsi, rdi, 3
	and	ecx, 7
	add	esi, 48
	add	ecx, 48
	mov	BYTE PTR 148[rsp], cl
	jmp	.L1426
	.p2align 4,,10
	.p2align 3
.L1483:
	mov	r8, rsi
	shrd	rsi, rdi, 4
	and	r8d, 15
	add	rsi, rcx
	add	r8, rcx
	movzx	eax, BYTE PTR [r8]
	mov	BYTE PTR 148[rsp], al
	movzx	eax, BYTE PTR [rsi]
	jmp	.L1435
	.p2align 4,,10
	.p2align 3
.L1455:
	lea	rdi, 148[rsp]
	lea	rbx, .LC24[rip]
	lea	r8, 147[rsp]
.L1429:
	mov	rsi, r8
	mov	rbp, r8
	.p2align 4,,10
	.p2align 3
.L1436:
	movsx	ecx, BYTE PTR [rsi]
	add	rsi, 1
	call	toupper
	mov	BYTE PTR -1[rsi], al
	cmp	rsi, rdi
	jne	.L1436
	mov	r8, rbp
	mov	ecx, 1
	mov	eax, 2
	jmp	.L1427
	.p2align 4,,10
	.p2align 3
.L1481:
	bsr	rax, rdi
	lea	ebp, 68[rax]
	movabs	rax, 3978425819141910832
	shr	ebp, 2
	mov	QWORD PTR 288[rsp], rax
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 296[rsp], rax
	lea	eax, -1[rbp]
	jmp	.L1431
	.p2align 4,,10
	.p2align 3
.L1479:
	bsr	rdx, rdi
	mov	eax, 128
	mov	ecx, 127
	xor	rdx, 63
	sub	eax, edx
	sub	ecx, edx
	jmp	.L1402
	.p2align 4,,10
	.p2align 3
.L1491:
	bsr	rax, rdi
	mov	edx, 2863311531
	add	eax, 67
	imul	rax, rdx
	shr	rax, 33
	lea	edx, -1[rax]
	jmp	.L1422
.L1446:
	mov	eax, 1
	jmp	.L1403
.L1448:
	mov	ebp, 1
	.p2align 4,,10
	.p2align 3
.L1408:
	add	esi, 48
	jmp	.L1419
	.p2align 4,,10
	.p2align 3
.L1484:
	test	ebp, ebp
	jne	.L1429
	mov	ecx, 1
	mov	eax, 2
	mov	rdi, r8
	jmp	.L1427
	.p2align 4,,10
	.p2align 3
.L1480:
	mov	rax, r12
	or	rax, r13
	jne	.L1453
	mov	BYTE PTR 147[rsp], 48
	lea	rbx, .LC25[rip]
	lea	rdi, 148[rsp]
	lea	r8, 147[rsp]
	jmp	.L1428
	.p2align 4,,10
	.p2align 3
.L1488:
	mov	rsi, QWORD PTR 64[rsp]
	lea	r14d, 5[r9]
	mov	rdi, QWORD PTR 72[rsp]
	mov	r12, QWORD PTR 80[rsp]
	mov	r13, QWORD PTR 88[rsp]
	jmp	.L1414
	.p2align 4,,10
	.p2align 3
.L1489:
	mov	rsi, QWORD PTR 64[rsp]
	lea	r14d, 6[r9]
	mov	rdi, QWORD PTR 72[rsp]
	mov	r12, QWORD PTR 80[rsp]
	mov	r13, QWORD PTR 88[rsp]
	jmp	.L1414
	.p2align 4,,10
	.p2align 3
.L1490:
	mov	rsi, QWORD PTR 64[rsp]
	lea	r14d, 7[r9]
	mov	rdi, QWORD PTR 72[rsp]
	mov	r12, QWORD PTR 80[rsp]
	mov	r13, QWORD PTR 88[rsp]
	jmp	.L1414
	.p2align 4,,10
	.p2align 3
.L1454:
	lea	rbx, .LC24[rip]
	jmp	.L1392
	.p2align 4,,10
	.p2align 3
.L1482:
	lea	rcx, 288[rsp]
	jmp	.L1432
.L1451:
	lea	rdi, 275[rsp]
	lea	r8, 147[rsp]
	jmp	.L1417
.L1453:
	lea	rbx, .LC25[rip]
	jmp	.L1392
.L1487:
	lea	rcx, 288[rsp]
	mov	r8d, 201
	mov	ebp, 2
	lea	rdx, .LC27[rip]
	call	memcpy
	mov	rcx, rax
	jmp	.L1410
.L1450:
	mov	ebp, 4
	mov	ebx, 3
	jmp	.L1411
.L1449:
	mov	ebp, 3
	mov	ebx, 2
	jmp	.L1411
.L1385:
	lea	rcx, .LC26[rip]
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
.LFB5421:
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
	je	.L1578
	shr	al, 3
	and	eax, 15
	cmp	al, 4
	je	.L1497
	ja	.L1498
	cmp	al, 1
	ja	.L1579
	mov	rax, rsi
	or	rax, rdi
	jne	.L1511
	mov	BYTE PTR 131[rsp], 48
	lea	rdi, 132[rsp]
	lea	r8, 131[rsp]
.L1512:
	movzx	eax, BYTE PTR [r12]
	mov	rdx, r8
.L1510:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L1580
.L1544:
	cmp	eax, 3
	je	.L1561
.L1545:
	lea	rax, 112[rsp]
	sub	rdi, rdx
	mov	QWORD PTR 120[rsp], rdx
	sub	r8, rdx
	mov	r9, r13
	mov	rdx, rax
	mov	rcx, r12
	mov	QWORD PTR 112[rsp], rdi
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L1496
	.p2align 4,,10
	.p2align 3
.L1578:
	mov	eax, 127
	cmp	rax, rsi
	mov	eax, 0
	sbb	rax, rdi
	jc	.L1495
	lea	rax, 272[rsp]
	mov	DWORD PTR 32[rsp], 1
	mov	r9, r12
	mov	edx, 1
	lea	rcx, 112[rsp]
	mov	BYTE PTR 272[rsp], sil
	mov	QWORD PTR 112[rsp], 1
	mov	QWORD PTR 120[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1496:
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
.L1579:
	lea	rax, .LC22[rip]
	cmp	dl, 16
	lea	rbx, .LC21[rip]
	cmovne	rbx, rax
	mov	rax, rsi
	or	rax, rdi
	je	.L1547
	test	rdi, rdi
	jne	.L1581
	bsr	rax, rsi
	mov	r9d, 128
	mov	edx, 127
	xor	rax, 63
	add	eax, 64
	sub	r9d, eax
	sub	edx, eax
	je	.L1548
.L1506:
	mov	ecx, edx
	sub	edx, 1
	lea	rax, 128[rsp+rcx]
	lea	rcx, 127[rsp+rcx]
	sub	rcx, rdx
	.p2align 4,,10
	.p2align 3
.L1508:
	mov	edx, esi
	sub	rax, 1
	shrd	rsi, rdi, 1
	and	edx, 1
	shr	rdi
	add	edx, 48
	mov	BYTE PTR 4[rax], dl
	cmp	rax, rcx
	jne	.L1508
.L1507:
	lea	r8, 131[rsp]
	movsx	rdi, r9d
	mov	eax, 49
	add	rdi, r8
.L1504:
	mov	BYTE PTR 131[rsp], al
	movzx	eax, BYTE PTR [r12]
	test	al, 16
	je	.L1560
.L1559:
	mov	rdx, -2
	mov	ecx, 2
.L1509:
	add	rdx, r8
	test	ecx, ecx
	mov	r11d, ecx
	je	.L1510
	xor	ecx, ecx
.L1542:
	mov	r9d, ecx
	add	ecx, 1
	movzx	r10d, BYTE PTR [rbx+r9]
	cmp	ecx, r11d
	mov	BYTE PTR [rdx+r9], r10b
	jb	.L1542
	jmp	.L1510
	.p2align 4,,10
	.p2align 3
.L1497:
	mov	rax, rsi
	or	rax, rdi
	je	.L1554
	test	rdi, rdi
	jne	.L1582
	bsr	rax, rsi
	mov	edx, 2863311531
	mov	ecx, 63
	add	eax, 3
	imul	rax, rdx
	shr	rax, 33
	cmp	rcx, rsi
	lea	edx, -1[rax]
	jnb	.L1527
.L1526:
	mov	r9d, 63
	xor	r8d, r8d
	.p2align 4,,10
	.p2align 3
.L1528:
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
	jc	.L1528
.L1527:
	mov	edx, 7
	cmp	rdx, rsi
	mov	edx, 0
	sbb	rdx, rdi
	jc	.L1583
	add	esi, 48
.L1530:
	lea	r8, 131[rsp]
	mov	edi, eax
	mov	edx, 1
	lea	rbx, .LC23[rip]
	add	rdi, r8
	mov	ecx, 1
	jmp	.L1524
	.p2align 4,,10
	.p2align 3
.L1554:
	mov	esi, 48
	xor	edx, edx
	xor	ebx, ebx
	lea	rdi, 132[rsp]
	xor	ecx, ecx
	lea	r8, 131[rsp]
.L1524:
	mov	BYTE PTR 131[rsp], sil
.L1531:
	movzx	eax, BYTE PTR [r12]
	test	al, 16
	je	.L1560
	test	dl, dl
	jne	.L1584
.L1560:
	shr	al, 2
	mov	rdx, r8
	and	eax, 3
	cmp	eax, 1
	jne	.L1544
.L1580:
	mov	eax, 43
.L1546:
	mov	BYTE PTR -1[rdx], al
	sub	rdx, 1
	jmp	.L1545
	.p2align 4,,10
	.p2align 3
.L1498:
	cmp	dl, 40
	je	.L1585
	mov	rax, rsi
	or	rax, rdi
	jne	.L1556
	cmp	dl, 48
	mov	BYTE PTR 131[rsp], 48
	je	.L1557
	lea	rbx, .LC24[rip]
	lea	rdi, 132[rsp]
	lea	r8, 131[rsp]
	jmp	.L1533
	.p2align 4,,10
	.p2align 3
.L1561:
	mov	eax, 32
	jmp	.L1546
	.p2align 4,,10
	.p2align 3
.L1547:
	lea	rdi, 132[rsp]
	mov	eax, 48
	lea	r8, 131[rsp]
	jmp	.L1504
	.p2align 4,,10
	.p2align 3
.L1511:
	xor	eax, eax
	mov	edx, 9
	cmp	rdx, rsi
	mov	rbx, rax
	sbb	rbx, rdi
	jnc	.L1550
	mov	edx, 99
	mov	rbx, rax
	cmp	rdx, rsi
	sbb	rbx, rdi
	jnc	.L1586
	mov	edx, 999
	mov	rbx, rax
	cmp	rdx, rsi
	sbb	rbx, rdi
	jnc	.L1551
	mov	edx, 9999
	cmp	rdx, rsi
	sbb	rax, rdi
	jnc	.L1552
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
	jmp	.L1517
	.p2align 4,,10
	.p2align 3
.L1521:
	mov	eax, 999999
	cmp	rax, r15
	mov	rax, r14
	sbb	rax, rbx
	jnc	.L1587
	mov	eax, 9999999
	cmp	rax, r15
	mov	rax, r14
	sbb	rax, rbx
	jnc	.L1588
	mov	eax, 99999999
	cmp	rax, r15
	mov	rax, r14
	sbb	rax, rbx
	jnc	.L1589
.L1517:
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
	jc	.L1521
	mov	ebp, edi
	mov	r12, r13
	mov	rsi, QWORD PTR 64[rsp]
	mov	rdi, QWORD PTR 72[rsp]
	mov	r13, QWORD PTR 576[rsp]
.L1519:
	cmp	ebp, 128
	ja	.L1553
	lea	ebx, -1[rbp]
.L1516:
	lea	rcx, 272[rsp]
	mov	r8d, 201
	movabs	r15, 1152921504606846975
	lea	rdx, .LC27[rip]
	movabs	r14, -8116567392432202711
	call	memcpy
	mov	QWORD PTR 64[rsp], rbp
	mov	rcx, rax
	mov	QWORD PTR 560[rsp], r12
	.p2align 4,,10
	.p2align 3
.L1522:
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
	jc	.L1522
	mov	eax, 999
	mov	rbp, QWORD PTR 64[rsp]
	cmp	rax, r8
	mov	eax, 0
	mov	r12, QWORD PTR 560[rsp]
	sbb	rax, rdx
	jnc	.L1513
.L1515:
	add	rsi, rsi
	lea	rax, [rcx+rsi]
	add	rsi, rcx
	movzx	eax, BYTE PTR 1[rax]
	movzx	esi, BYTE PTR [rsi]
	mov	BYTE PTR 132[rsp], al
.L1523:
	lea	r8, 131[rsp]
	mov	BYTE PTR 131[rsp], sil
	lea	rdi, [r8+rbp]
	jmp	.L1512
	.p2align 4,,10
	.p2align 3
.L1585:
	mov	rax, rsi
	or	rax, rdi
	jne	.L1555
	mov	BYTE PTR 131[rsp], 48
	lea	rbx, .LC25[rip]
	lea	rdi, 132[rsp]
	lea	r8, 131[rsp]
	jmp	.L1533
	.p2align 4,,10
	.p2align 3
.L1556:
	lea	rbx, .LC24[rip]
.L1532:
	test	rdi, rdi
	jne	.L1590
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
	jnb	.L1591
.L1536:
	lea	rcx, 272[rsp]
	mov	r11d, 255
	xor	r10d, r10d
	.p2align 4,,10
	.p2align 3
.L1538:
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
	jc	.L1538
.L1537:
	mov	eax, 15
	cmp	rax, rsi
	mov	eax, 0
	sbb	rax, rdi
	jc	.L1592
	add	rcx, rsi
	movzx	eax, BYTE PTR [rcx]
.L1540:
	lea	r8, 131[rsp]
	mov	edi, ebp
	mov	BYTE PTR 131[rsp], al
	add	rdi, r8
	cmp	dl, 48
	je	.L1593
.L1533:
	movzx	eax, BYTE PTR [r12]
	test	al, 16
	jne	.L1559
	jmp	.L1560
	.p2align 4,,10
	.p2align 3
.L1592:
	mov	r8, rsi
	shrd	rsi, rdi, 4
	and	r8d, 15
	add	rsi, rcx
	add	r8, rcx
	movzx	eax, BYTE PTR [r8]
	mov	BYTE PTR 132[rsp], al
	movzx	eax, BYTE PTR [rsi]
	jmp	.L1540
	.p2align 4,,10
	.p2align 3
.L1583:
	mov	rcx, rsi
	shrd	rsi, rdi, 3
	and	ecx, 7
	add	esi, 48
	add	ecx, 48
	mov	BYTE PTR 132[rsp], cl
	jmp	.L1530
	.p2align 4,,10
	.p2align 3
.L1555:
	lea	rbx, .LC25[rip]
	jmp	.L1532
	.p2align 4,,10
	.p2align 3
.L1557:
	lea	rdi, 132[rsp]
	lea	rbx, .LC24[rip]
	lea	r8, 131[rsp]
.L1534:
	mov	rsi, r8
	mov	rbp, r8
	.p2align 4,,10
	.p2align 3
.L1541:
	movsx	ecx, BYTE PTR [rsi]
	add	rsi, 1
	call	toupper
	mov	BYTE PTR -1[rsi], al
	cmp	rsi, rdi
	jne	.L1541
	mov	r8, rbp
	mov	edx, 1
	mov	ecx, 2
	jmp	.L1531
	.p2align 4,,10
	.p2align 3
.L1590:
	bsr	rax, rdi
	lea	ebp, 68[rax]
	movabs	rax, 3978425819141910832
	shr	ebp, 2
	mov	QWORD PTR 272[rsp], rax
	movabs	rax, 7378413942531504440
	mov	QWORD PTR 280[rsp], rax
	lea	eax, -1[rbp]
	jmp	.L1536
	.p2align 4,,10
	.p2align 3
.L1581:
	bsr	rax, rdi
	mov	r9d, 128
	mov	edx, 127
	xor	rax, 63
	sub	r9d, eax
	sub	edx, eax
	jmp	.L1506
	.p2align 4,,10
	.p2align 3
.L1584:
	mov	rdx, rcx
	neg	rdx
	jmp	.L1509
.L1548:
	mov	r9d, 1
	jmp	.L1507
.L1550:
	mov	ebp, 1
	.p2align 4,,10
	.p2align 3
.L1513:
	add	esi, 48
	jmp	.L1523
	.p2align 4,,10
	.p2align 3
.L1593:
	test	ebp, ebp
	jne	.L1534
	mov	edx, 1
	mov	ecx, 2
	mov	rdi, r8
	jmp	.L1531
	.p2align 4,,10
	.p2align 3
.L1582:
	bsr	rax, rdi
	mov	edx, 2863311531
	add	eax, 67
	imul	rax, rdx
	shr	rax, 33
	lea	edx, -1[rax]
	jmp	.L1526
	.p2align 4,,10
	.p2align 3
.L1587:
	mov	rsi, QWORD PTR 64[rsp]
	lea	ebp, 5[r9]
	mov	r12, r13
	mov	rdi, QWORD PTR 72[rsp]
	mov	r13, QWORD PTR 576[rsp]
	jmp	.L1519
	.p2align 4,,10
	.p2align 3
.L1588:
	mov	rsi, QWORD PTR 64[rsp]
	lea	ebp, 6[r9]
	mov	r12, r13
	mov	rdi, QWORD PTR 72[rsp]
	mov	r13, QWORD PTR 576[rsp]
	jmp	.L1519
	.p2align 4,,10
	.p2align 3
.L1589:
	mov	rsi, QWORD PTR 64[rsp]
	lea	ebp, 7[r9]
	mov	r12, r13
	mov	rdi, QWORD PTR 72[rsp]
	mov	r13, QWORD PTR 576[rsp]
	jmp	.L1519
	.p2align 4,,10
	.p2align 3
.L1591:
	lea	rcx, 272[rsp]
	jmp	.L1537
.L1553:
	lea	rdi, 259[rsp]
	lea	r8, 131[rsp]
	jmp	.L1512
.L1586:
	lea	rcx, 272[rsp]
	mov	r8d, 201
	mov	ebp, 2
	lea	rdx, .LC27[rip]
	call	memcpy
	mov	rcx, rax
	jmp	.L1515
.L1551:
	mov	ebp, 3
	mov	ebx, 2
	jmp	.L1516
.L1552:
	mov	ebp, 4
	mov	ebx, 3
	jmp	.L1516
.L1495:
	lea	rcx, .LC26[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC30:
	.ascii "basic_string_view::copy\0"
	.align 8
.LC31:
	.ascii "%s: __pos (which is %zu) > __size (which is %zu)\0"
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_:
.LFB5685:
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
	je	.L1611
	mov	rax, QWORD PTR 16[rcx]
.L1595:
	cmp	rax, rbp
	jb	.L1622
.L1596:
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
.LEHB31:
	call	[QWORD PTR 24[rax]]
.LEHE31:
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
	je	.L1606
	mov	r8, QWORD PTR 40[rsi]
	cmp	QWORD PTR [r8], -1
	je	.L1607
	mov	rax, QWORD PTR 48[rsi]
	add	rcx, 1
	movzx	eax, BYTE PTR [rax]
	mov	BYTE PTR -1[rcx], al
	add	QWORD PTR [r12], 1
	mov	rax, QWORD PTR [rdx]
.L1607:
	cmp	rax, 1
	jbe	.L1606
	mov	rax, QWORD PTR [r12]
	mov	rsi, QWORD PTR 0[r13]
	mov	rdx, QWORD PTR 8[r13]
	cmp	rsi, rax
	jb	.L1623
	sub	rsi, rax
	je	.L1606
	add	rdx, rax
	mov	r8, rsi
	call	memcpy
	mov	rcx, rax
	add	rcx, rsi
.L1606:
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
.L1622:
	test	rbp, rbp
	js	.L1624
	add	rax, rax
	cmp	rbp, rax
	jb	.L1625
	mov	rcx, rbp
	add	rcx, 1
	js	.L1599
.L1600:
.LEHB32:
	call	_Znwy
	mov	r8, QWORD PTR 8[rbx]
	mov	r13, QWORD PTR [rbx]
	mov	rdi, rax
	cmp	r8, 1
	je	.L1626
	test	r8, r8
	je	.L1621
	mov	rdx, r13
	mov	rcx, rax
	call	memcpy
.L1621:
	cmp	r12, r13
	je	.L1603
	mov	rax, QWORD PTR 16[rbx]
	mov	rcx, r13
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1603:
	mov	QWORD PTR [rbx], rdi
	mov	QWORD PTR 16[rbx], rbp
	jmp	.L1596
	.p2align 4,,10
	.p2align 3
.L1626:
	movzx	eax, BYTE PTR 0[r13]
	mov	BYTE PTR [rdi], al
	jmp	.L1621
	.p2align 4,,10
	.p2align 3
.L1625:
	test	rax, rax
	js	.L1599
	lea	rcx, 1[rax]
	mov	rbp, rax
	jmp	.L1600
	.p2align 4,,10
	.p2align 3
.L1611:
	mov	eax, 15
	jmp	.L1595
	.p2align 4,,10
	.p2align 3
.L1599:
	call	_ZSt17__throw_bad_allocv
.L1624:
	lea	rcx, .LC7[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE32:
.L1623:
	lea	rdx, .LC30[rip]
	mov	r9, rsi
	mov	r8, rax
	lea	rcx, .LC31[rip]
.LEHB33:
	call	_ZSt24__throw_out_of_range_fmtPKcz
.LEHE33:
.L1612:
	mov	rcx, rax
	xor	eax, eax
	mov	QWORD PTR 8[rbx], rax
	mov	rax, QWORD PTR [rbx]
	mov	BYTE PTR [rax], 0
.LEHB34:
	call	_Unwind_Resume
	nop
.LEHE34:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5685:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5685-.LLSDACSB5685
.LLSDACSB5685:
	.uleb128 .LEHB31-.LFB5685
	.uleb128 .LEHE31-.LEHB31
	.uleb128 .L1612-.LFB5685
	.uleb128 0
	.uleb128 .LEHB32-.LFB5685
	.uleb128 .LEHE32-.LEHB32
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB33-.LFB5685
	.uleb128 .LEHE33-.LEHB33
	.uleb128 .L1612-.LFB5685
	.uleb128 0
	.uleb128 .LEHB34-.LFB5685
	.uleb128 .LEHE34-.LEHB34
	.uleb128 0
	.uleb128 0
.LLSDACSE5685:
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_,"x"
	.linkonce discard
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0:
.LFB5760:
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
.LEHB35:
	call	_ZNSt6locale7classicEv
	mov	rdx, rax
	mov	rcx, rsi
	call	_ZNKSt6localeeqERKS_
	test	al, al
	je	.L1654
.L1627:
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
.L1654:
	mov	rcx, QWORD PTR .refptr._ZNSt7__cxx118numpunctIcE2idE[rip]
	call	_ZNKSt6locale2id5_M_idEv
	mov	rdx, rax
	mov	rax, QWORD PTR [rsi]
	mov	rax, QWORD PTR 8[rax]
	mov	rsi, QWORD PTR [rax+rdx*8]
	test	rsi, rsi
	je	.L1629
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	call	[QWORD PTR 16[rax]]
	mov	BYTE PTR 119[rsp], al
	mov	rax, QWORD PTR [rsi]
	lea	r12, 144[rsp]
	mov	rdx, rsi
	mov	rcx, r12
	call	[QWORD PTR 32[rax]]
.LEHE35:
	cmp	QWORD PTR 152[rsp], 0
	jne	.L1631
	cmp	BYTE PTR 119[rsp], 46
	je	.L1632
.L1631:
	mov	rbp, QWORD PTR 96[rsp]
	mov	r13, QWORD PTR 104[rsp]
	test	rbp, rbp
	je	.L1655
	mov	edx, 46
	mov	r8, rbp
	mov	rcx, r13
	call	memchr
	movsx	edx, dil
	test	rax, rax
	je	.L1635
	sub	rax, r13
	mov	r8, rbp
	mov	rcx, r13
	mov	rdi, rax
	mov	QWORD PTR 120[rsp], rax
	call	memchr
	test	rax, rax
	je	.L1636
	sub	rax, r13
	cmp	rax, rdi
	jnb	.L1636
.L1641:
	mov	QWORD PTR 128[rsp], rax
	sub	rbp, rax
.L1637:
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
.LEHB36:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_
.LEHE36:
.L1632:
	mov	rcx, QWORD PTR 144[rsp]
	lea	rax, 160[rsp]
	cmp	rcx, rax
	je	.L1627
	mov	rax, QWORD PTR 160[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L1627
	.p2align 4,,10
	.p2align 3
.L1655:
	mov	QWORD PTR 120[rsp], -1
.L1634:
	mov	QWORD PTR 128[rsp], rbp
	mov	rax, rbp
	xor	ebp, ebp
	jmp	.L1637
	.p2align 4,,10
	.p2align 3
.L1636:
	cmp	rdi, -1
	mov	QWORD PTR 128[rsp], rdi
	je	.L1634
	sub	rbp, rdi
	mov	rax, rdi
	jmp	.L1637
	.p2align 4,,10
	.p2align 3
.L1635:
	mov	QWORD PTR 120[rsp], -1
	mov	r8, rbp
	mov	rcx, r13
	call	memchr
	test	rax, rax
	je	.L1634
	sub	rax, r13
	cmp	rax, -1
	jne	.L1641
	jmp	.L1634
.L1629:
.LEHB37:
	call	_ZSt16__throw_bad_castv
.LEHE37:
.L1642:
	mov	rsi, rax
	jmp	.L1640
.L1643:
	mov	rcx, r12
	mov	rsi, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L1640:
	mov	rcx, rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rsi
.LEHB38:
	call	_Unwind_Resume
	nop
.LEHE38:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5760:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5760-.LLSDACSB5760
.LLSDACSB5760:
	.uleb128 .LEHB35-.LFB5760
	.uleb128 .LEHE35-.LEHB35
	.uleb128 .L1642-.LFB5760
	.uleb128 0
	.uleb128 .LEHB36-.LFB5760
	.uleb128 .LEHE36-.LEHB36
	.uleb128 .L1643-.LFB5760
	.uleb128 0
	.uleb128 .LEHB37-.LFB5760
	.uleb128 .LEHE37-.LEHB37
	.uleb128 .L1642-.LFB5760
	.uleb128 0
	.uleb128 .LEHB38-.LFB5760
	.uleb128 .LEHE38-.LEHB38
	.uleb128 0
	.uleb128 0
.LLSDACSE5760:
	.text
	.seh_endproc
	.section .rdata,"dr"
.LC33:
	.ascii "basic_string::_M_replace\0"
.LC34:
	.ascii "basic_string::_M_replace_aux\0"
.LC35:
	.ascii "basic_string::insert\0"
	.align 8
.LC36:
	.ascii "%s: __pos (which is %zu) > this->size() (which is %zu)\0"
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5410:
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
	jne	.L1895
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L1676
	lea	rdx, .L1800[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L1800:
	.long	.L1676-.L1800
	.long	.L1801-.L1800
	.long	.L1831-.L1800
	.long	.L1832-.L1800
	.long	.L1833-.L1800
	.long	.L1834-.L1800
	.long	.L1835-.L1800
	.long	.L1830-.L1800
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1676:
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
.L1675:
	cmp	eax, 132
	mov	BYTE PTR 72[rsp], 0
	mov	QWORD PTR 64[rsp], 6
	je	.L1829
	lea	rax, 416[rsp]
	mov	QWORD PTR 80[rsp], rax
	lea	r13, 289[rsp]
.L1673:
	test	r12b, r12b
	je	.L1703
	cmp	r13, rsi
	mov	r12, QWORD PTR __imp_toupper[rip]
	mov	r14, r13
	je	.L1705
	.p2align 4,,10
	.p2align 3
.L1704:
	movsx	ecx, BYTE PTR [r14]
	add	r14, 1
	call	r12
	mov	BYTE PTR -1[r14], al
	cmp	rsi, r14
	jne	.L1704
.L1705:
	movsx	ecx, dil
	call	r12
	mov	edi, eax
.L1703:
	fld	TBYTE PTR 48[rsp]
	movzx	r9d, BYTE PTR [rbx]
	fxam
	fnstsw	ax
	fstp	st(0)
	test	ah, 2
	jne	.L1706
	mov	eax, r9d
	and	eax, 12
	cmp	al, 4
	je	.L1896
	cmp	al, 12
	jne	.L1706
	mov	BYTE PTR -1[r13], 32
	movzx	r9d, BYTE PTR [rbx]
	sub	r13, 1
	.p2align 4,,10
	.p2align 3
.L1706:
	mov	r12, rsi
	sub	r12, r13
	test	r9b, 16
	je	.L1708
	fld	TBYTE PTR 48[rsp]
	fabs
	fld	TBYTE PTR .LC32[rip]
	fucomip	st, st(1)
	fstp	st(0)
	jb	.L1708
	test	r12, r12
	je	.L1812
	mov	r8, r12
	mov	edx, 46
	mov	rcx, r13
	mov	BYTE PTR 88[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 88[rsp]
	test	rax, rax
	mov	r14, rax
	je	.L1710
	sub	r14, r13
	cmp	r14, -1
	je	.L1710
	lea	rax, 1[r14]
	mov	QWORD PTR 88[rsp], r12
	cmp	rax, r12
	jnb	.L1711
	mov	r8, r12
	movsx	edx, dil
	mov	BYTE PTR 103[rsp], r9b
	lea	rcx, 0[r13+rax]
	sub	r8, rax
	call	memchr
	movzx	r9d, BYTE PTR 103[rsp]
	test	rax, rax
	je	.L1711
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	mov	QWORD PTR 88[rsp], rax
.L1711:
	cmp	QWORD PTR 88[rsp], r14
	sete	BYTE PTR 103[rsp]
	sete	r14b
	cmp	BYTE PTR 72[rsp], 0
	movzx	r14d, r14b
	jne	.L1712
	mov	QWORD PTR 72[rsp], 0
.L1713:
	test	r14, r14
	je	.L1708
.L1797:
	mov	r9, QWORD PTR 200[rsp]
	lea	rax, [r12+r14]
	mov	QWORD PTR 64[rsp], rax
	test	r9, r9
	jne	.L1715
	mov	rax, QWORD PTR 80[rsp]
	sub	rax, rsi
	cmp	rax, r14
	jnb	.L1897
	cmp	QWORD PTR 192[rsp], rbp
	je	.L1898
	mov	rax, QWORD PTR 208[rsp]
	mov	rsi, QWORD PTR 64[rsp]
	cmp	rax, rsi
	jnb	.L1724
.L1723:
	cmp	QWORD PTR 64[rsp], 0
	js	.L1793
	add	rax, rax
	cmp	QWORD PTR 64[rsp], rax
	jnb	.L1726
	test	rax, rax
	jns	.L1899
.L1727:
	lea	rsi, 192[rsp]
.LEHB39:
	call	_ZSt17__throw_bad_allocv
.L1738:
	mov	rcx, r12
	mov	r14, r12
	add	rcx, 1
	js	.L1745
.L1746:
	lea	rsi, 192[rsp]
	call	_Znwy
.LEHE39:
	cmp	r14, 1
	mov	r10, rax
	je	.L1900
.L1739:
	mov	rcx, r10
	mov	r8, r14
	mov	rdx, r13
	call	memcpy
	mov	rsi, r12
	mov	r12, r14
	mov	r10, rax
.L1747:
	mov	rcx, QWORD PTR 192[rsp]
	cmp	rcx, rbp
	je	.L1748
	mov	rax, QWORD PTR 208[rsp]
	mov	QWORD PTR 64[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 64[rsp]
.L1748:
	mov	QWORD PTR 192[rsp], r10
	mov	QWORD PTR 208[rsp], rsi
.L1743:
	cmp	BYTE PTR 103[rsp], 0
	mov	QWORD PTR 200[rsp], r12
	mov	BYTE PTR [r10+r12], 0
	jne	.L1901
.L1749:
	cmp	QWORD PTR 72[rsp], 0
	mov	r12, QWORD PTR 200[rsp]
	jne	.L1902
.L1751:
	mov	r13, QWORD PTR 192[rsp]
	movzx	r9d, BYTE PTR [rbx]
	.p2align 4,,10
	.p2align 3
.L1708:
	lea	rsi, 240[rsp]
	and	r9d, 32
	mov	QWORD PTR 176[rsp], 0
	mov	BYTE PTR 184[rsp], 0
	mov	QWORD PTR 224[rsp], rsi
	mov	QWORD PTR 232[rsp], 0
	mov	BYTE PTR 240[rsp], 0
	je	.L1822
	cmp	BYTE PTR 32[r15], 0
	lea	rdx, 24[r15]
	je	.L1903
.L1766:
	lea	r14, 168[rsp]
	mov	rcx, r14
	call	_ZNSt6localeC1ERKS_
	lea	rcx, 256[rsp]
	mov	r9, r14
	movsx	r8d, dil
	lea	rdx, 112[rsp]
	mov	QWORD PTR 112[rsp], r12
	mov	QWORD PTR 120[rsp], r13
.LEHB40:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE40:
	mov	rax, QWORD PTR 256[rsp]
	lea	rdi, 272[rsp]
	mov	rcx, QWORD PTR 224[rsp]
	mov	r8, QWORD PTR 264[rsp]
	cmp	rax, rdi
	je	.L1904
	movq	xmm0, r8
	cmp	rcx, rsi
	movhps	xmm0, QWORD PTR 272[rsp]
	je	.L1905
	test	rcx, rcx
	mov	rdx, QWORD PTR 240[rsp]
	mov	QWORD PTR 224[rsp], rax
	movups	XMMWORD PTR 232[rsp], xmm0
	je	.L1774
	mov	QWORD PTR 256[rsp], rcx
	mov	QWORD PTR 272[rsp], rdx
.L1773:
	mov	QWORD PTR 264[rsp], 0
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 256[rsp]
	cmp	rcx, rdi
	je	.L1775
	mov	rax, QWORD PTR 272[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1775:
	mov	rcx, r14
	call	_ZNSt6localeD1Ev
	movzx	eax, WORD PTR [rbx]
	mov	r12, QWORD PTR 232[rsp]
	mov	rdi, QWORD PTR 224[rsp]
	and	ax, 384
	cmp	ax, 128
	je	.L1906
.L1776:
	cmp	ax, 256
	je	.L1778
	mov	r14, QWORD PTR 16[r15]
.L1782:
	lea	rdx, 112[rsp]
	mov	rcx, r14
	mov	QWORD PTR 112[rsp], r12
	mov	QWORD PTR 120[rsp], rdi
.LEHB41:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L1891:
	mov	rcx, QWORD PTR 224[rsp]
	mov	rbx, rax
	cmp	rcx, rsi
	je	.L1786
	mov	rax, QWORD PTR 240[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1786:
	cmp	BYTE PTR 184[rsp], 0
	jne	.L1907
.L1787:
	mov	rcx, QWORD PTR 192[rsp]
	cmp	rcx, rbp
	je	.L1851
	mov	rax, QWORD PTR 208[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1851:
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
.L1822:
	movzx	eax, WORD PTR [rbx]
	mov	rdi, r13
	and	ax, 384
	cmp	ax, 128
	jne	.L1776
.L1906:
	movzx	eax, WORD PTR 4[rbx]
.L1777:
	cmp	r12, rax
	mov	r14, QWORD PTR 16[r15]
	jnb	.L1782
	movzx	edx, BYTE PTR [rbx]
	sub	rax, r12
	movzx	ecx, BYTE PTR 8[rbx]
	mov	rbx, rax
	mov	r8d, edx
	and	r8d, 3
	movsx	eax, cl
	jne	.L1784
	and	edx, 64
	je	.L1824
	fld	TBYTE PTR 48[rsp]
	fabs
	fld	TBYTE PTR .LC32[rip]
	fucomip	st, st(1)
	fstp	st(0)
	jnb	.L1908
.L1824:
	mov	eax, 32
	mov	r8d, 2
.L1784:
	lea	rdx, 112[rsp]
	mov	DWORD PTR 32[rsp], eax
	mov	r9, rbx
	mov	rcx, r14
	mov	QWORD PTR 112[rsp], r12
	mov	QWORD PTR 120[rsp], rdi
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
.LEHE41:
	jmp	.L1891
	.p2align 4,,10
	.p2align 3
.L1895:
	cmp	dl, 2
	je	.L1909
	mov	QWORD PTR 64[rsp], -1
	cmp	dl, 4
	je	.L1910
.L1659:
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L1662
	lea	rdx, .L1664[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L1664:
	.long	.L1671-.L1664
	.long	.L1803-.L1664
	.long	.L1669-.L1664
	.long	.L1668-.L1664
	.long	.L1885-.L1664
	.long	.L1887-.L1664
	.long	.L1665-.L1664
	.long	.L1886-.L1664
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1907:
	lea	rcx, 176[rsp]
	call	_ZNSt6localeD1Ev
	jmp	.L1787
	.p2align 4,,10
	.p2align 3
.L1831:
	mov	r12d, 1
.L1674:
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
	jmp	.L1675
	.p2align 4,,10
	.p2align 3
.L1908:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	eax, 48
	mov	r8d, 2
	cmp	BYTE PTR [rcx+rdx], 15
	jbe	.L1784
	mov	rax, QWORD PTR 24[r14]
	movzx	edx, BYTE PTR [rdi]
	lea	rcx, 1[rax]
	mov	QWORD PTR 24[r14], rcx
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[r14]
	sub	rax, QWORD PTR 8[r14]
	cmp	rax, QWORD PTR 16[r14]
	je	.L1911
.L1785:
	add	rdi, 1
	sub	r12, 1
	mov	eax, 48
	mov	r8d, 2
	jmp	.L1784
	.p2align 4,,10
	.p2align 3
.L1812:
	xor	eax, eax
.L1709:
	cmp	BYTE PTR 72[rsp], 0
	je	.L1912
	movzx	edx, BYTE PTR 72[rsp]
	mov	QWORD PTR 88[rsp], rax
	mov	r14d, 1
	mov	BYTE PTR 103[rsp], dl
	jmp	.L1796
	.p2align 4,,10
	.p2align 3
.L1832:
	mov	QWORD PTR 64[rsp], 6
.L1668:
	xor	r12d, r12d
.L1667:
	mov	r13d, 1
	mov	edi, 101
	mov	BYTE PTR 72[rsp], 0
.L1670:
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
	je	.L1672
	lea	rax, 416[rsp]
	mov	r13, QWORD PTR 88[rsp]
	mov	QWORD PTR 80[rsp], rax
	jmp	.L1673
	.p2align 4,,10
	.p2align 3
.L1833:
	mov	QWORD PTR 64[rsp], 6
.L1885:
	mov	r12d, 1
	jmp	.L1667
	.p2align 4,,10
	.p2align 3
.L1834:
	mov	QWORD PTR 64[rsp], 6
.L1887:
	mov	r13d, 2
	xor	edi, edi
	mov	BYTE PTR 72[rsp], 0
	xor	r12d, r12d
	jmp	.L1670
	.p2align 4,,10
	.p2align 3
.L1830:
	mov	QWORD PTR 64[rsp], 6
.L1886:
	mov	r12d, 1
.L1663:
	mov	r13d, 3
	mov	edi, 101
	mov	BYTE PTR 72[rsp], 1
	jmp	.L1670
	.p2align 4,,10
	.p2align 3
.L1835:
	mov	QWORD PTR 64[rsp], 6
.L1665:
	xor	r12d, r12d
	jmp	.L1663
	.p2align 4,,10
	.p2align 3
.L1801:
	xor	r12d, r12d
	jmp	.L1674
	.p2align 4,,10
	.p2align 3
.L1910:
	movzx	edx, BYTE PTR [r8]
	mov	BYTE PTR 240[rsp], 0
	movzx	eax, WORD PTR 6[rcx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L1913
	test	cl, cl
	jne	.L1661
	mov	rdx, QWORD PTR [r8]
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L1661
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
.L1661:
	lea	rcx, 224[rsp]
	lea	rsi, 192[rsp]
.LEHB42:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE42:
	mov	QWORD PTR 64[rsp], rax
	movzx	eax, BYTE PTR 1[rbx]
	jmp	.L1659
	.p2align 4,,10
	.p2align 3
.L1896:
	mov	BYTE PTR -1[r13], 43
	sub	r13, 1
	movzx	r9d, BYTE PTR [rbx]
	jmp	.L1706
	.p2align 4,,10
	.p2align 3
.L1903:
	mov	rcx, rdx
	mov	QWORD PTR 64[rsp], rdx
	call	_ZNSt6localeC1Ev
	mov	rdx, QWORD PTR 64[rsp]
	mov	BYTE PTR 32[r15], 1
	jmp	.L1766
	.p2align 4,,10
	.p2align 3
.L1778:
	movzx	edx, BYTE PTR [r15]
	mov	BYTE PTR 272[rsp], 0
	movzx	eax, WORD PTR 4[rbx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L1914
	test	cl, cl
	jne	.L1781
	mov	rdx, QWORD PTR [r15]
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L1781
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
.L1781:
	lea	rcx, 256[rsp]
.LEHB43:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE43:
	jmp	.L1777
	.p2align 4,,10
	.p2align 3
.L1905:
	mov	QWORD PTR 224[rsp], rax
	movups	XMMWORD PTR 232[rsp], xmm0
.L1774:
	mov	QWORD PTR 256[rsp], rdi
	lea	rdi, 272[rsp]
	mov	rcx, rdi
	jmp	.L1773
	.p2align 4,,10
	.p2align 3
.L1909:
	movzx	edi, WORD PTR 6[rcx]
	mov	QWORD PTR 64[rsp], rdi
	jmp	.L1659
	.p2align 4,,10
	.p2align 3
.L1904:
	test	r8, r8
	je	.L1769
	cmp	r8, 1
	je	.L1915
	mov	rdx, rdi
	call	memcpy
	mov	r8, QWORD PTR 264[rsp]
	mov	rcx, QWORD PTR 224[rsp]
.L1769:
	mov	QWORD PTR 232[rsp], r8
	mov	BYTE PTR [rcx+r8], 0
	mov	rcx, QWORD PTR 256[rsp]
	jmp	.L1773
	.p2align 4,,10
	.p2align 3
.L1712:
	mov	rax, QWORD PTR 88[rsp]
	sub	rax, 1
.L1796:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	cmp	BYTE PTR [rcx+rdx], 16
	mov	rdx, QWORD PTR 64[rsp]
	adc	rax, -1
	sub	rdx, rax
	mov	QWORD PTR 72[rsp], rdx
	add	r14, rdx
	jmp	.L1713
	.p2align 4,,10
	.p2align 3
.L1829:
	mov	BYTE PTR 103[rsp], 0
	mov	QWORD PTR 88[rsp], 134
.L1677:
	mov	r10, QWORD PTR 192[rsp]
	cmp	r10, rbp
	je	.L1809
	mov	rax, QWORD PTR 208[rsp]
.L1679:
	mov	rsi, QWORD PTR 88[rsp]
	cmp	rax, rsi
	jb	.L1916
.L1702:
	cmp	r10, rbp
	je	.L1810
	mov	rax, QWORD PTR 208[rsp]
	lea	rsi, [rax+rax]
	cmp	rax, rsi
	mov	QWORD PTR 88[rsp], rsi
	jb	.L1917
.L1691:
	mov	rax, QWORD PTR 88[rsp]
	lea	rdx, 1[r10]
	mov	QWORD PTR 88[rsp], r10
	cmp	BYTE PTR 103[rsp], 0
	fld	TBYTE PTR 48[rsp]
	lea	r8, -1[r10+rax]
	fstp	TBYTE PTR 128[rsp]
	jne	.L1918
	test	r13d, r13d
	jne	.L1919
	mov	r9, QWORD PTR 80[rsp]
	mov	rcx, r14
	call	_ZSt8to_charsPcS_e
	mov	rsi, QWORD PTR 144[rsp]
	mov	rax, QWORD PTR 152[rsp]
	mov	r10, QWORD PTR 88[rsp]
.L1699:
	test	eax, eax
	jne	.L1701
	mov	rdx, QWORD PTR 192[rsp]
	mov	rax, rsi
	sub	rax, r10
	mov	QWORD PTR 200[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rax, QWORD PTR 192[rsp]
	lea	r13, 1[rax]
	add	rax, QWORD PTR 200[rsp]
	mov	QWORD PTR 80[rsp], rax
	jmp	.L1673
	.p2align 4,,10
	.p2align 3
.L1710:
	movsx	edx, dil
	mov	r8, r12
	mov	rcx, r13
	mov	BYTE PTR 88[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 88[rsp]
	test	rax, rax
	je	.L1816
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	jmp	.L1709
.L1803:
	mov	r13d, 4
	mov	edi, 112
	mov	BYTE PTR 72[rsp], 0
	xor	r12d, r12d
	jmp	.L1670
.L1669:
	mov	r13d, 4
	mov	edi, 112
	mov	BYTE PTR 72[rsp], 0
	mov	r12d, 1
	jmp	.L1670
.L1671:
	mov	r13d, 3
	xor	edi, edi
	mov	BYTE PTR 72[rsp], 0
	xor	r12d, r12d
	jmp	.L1670
.L1912:
	mov	QWORD PTR 88[rsp], rax
	mov	r14d, 1
	mov	QWORD PTR 72[rsp], 0
	mov	BYTE PTR 103[rsp], 1
	jmp	.L1797
.L1919:
	mov	r9, QWORD PTR 80[rsp]
	mov	DWORD PTR 32[rsp], r13d
	mov	rcx, r14
	call	_ZSt8to_charsPcS_eSt12chars_format
	mov	rsi, QWORD PTR 144[rsp]
	mov	rax, QWORD PTR 152[rsp]
	mov	r10, QWORD PTR 88[rsp]
	jmp	.L1699
.L1913:
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
	jmp	.L1661
.L1816:
	mov	rax, r12
	jmp	.L1709
.L1898:
	mov	rax, QWORD PTR 64[rsp]
	cmp	rax, 15
	ja	.L1894
	mov	rax, QWORD PTR 88[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L1731
	mov	r10, rbp
.L1798:
	cmp	r12, 15
	ja	.L1920
.L1737:
	cmp	r13, r10
	jb	.L1741
	cmp	r10, r13
	jb	.L1741
	xor	eax, eax
	mov	QWORD PTR 32[rsp], r12
	mov	r9, r13
	xor	r8d, r8d
	lea	rsi, 192[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	rdx, r10
	mov	rcx, rsi
.LEHB44:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	r10, QWORD PTR 192[rsp]
	jmp	.L1743
	.p2align 4,,10
	.p2align 3
.L1701:
	mov	rdx, QWORD PTR 192[rsp]
	cmp	eax, 132
	mov	QWORD PTR 200[rsp], 0
	mov	BYTE PTR [rdx], 0
	mov	r10, QWORD PTR 192[rsp]
	mov	rdx, QWORD PTR 200[rsp]
	je	.L1702
	lea	rax, [r10+rdx]
	lea	r13, 1[r10]
	mov	QWORD PTR 80[rsp], rax
	jmp	.L1673
	.p2align 4,,10
	.p2align 3
.L1916:
	test	rsi, rsi
	js	.L1921
	add	rax, rax
	cmp	QWORD PTR 88[rsp], rax
	jnb	.L1682
	test	rax, rax
	js	.L1683
	lea	rcx, 1[rax]
	mov	QWORD PTR 88[rsp], rax
.L1684:
	lea	rsi, 192[rsp]
	call	_Znwy
	mov	r10, rax
	mov	rax, QWORD PTR 200[rsp]
	mov	rsi, QWORD PTR 192[rsp]
	lea	r8, 1[rax]
	test	rax, rax
	je	.L1922
	test	r8, r8
	je	.L1888
	mov	rcx, r10
	mov	rdx, rsi
	call	memcpy
	mov	r10, rax
.L1888:
	cmp	rsi, rbp
	je	.L1687
	mov	rax, QWORD PTR 208[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 104[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 104[rsp]
.L1687:
	mov	rax, QWORD PTR 88[rsp]
	mov	QWORD PTR 192[rsp], r10
	mov	QWORD PTR 208[rsp], rax
	jmp	.L1702
.L1914:
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
	jmp	.L1781
.L1715:
	cmp	QWORD PTR 192[rsp], rbp
	je	.L1721
	mov	rax, QWORD PTR 208[rsp]
	mov	rsi, QWORD PTR 64[rsp]
	cmp	rax, rsi
	jb	.L1723
.L1722:
	mov	rax, QWORD PTR 88[rsp]
	cmp	r9, rax
	jb	.L1923
.L1734:
	movabs	rax, 9223372036854775807
	sub	rax, r9
	cmp	rax, r14
	jb	.L1924
	mov	rax, QWORD PTR 192[rsp]
	lea	r12, [r9+r14]
	cmp	rax, rbp
	je	.L1821
	mov	rdx, QWORD PTR 208[rsp]
.L1758:
	cmp	rdx, r12
	jb	.L1759
	mov	rsi, QWORD PTR 88[rsp]
	lea	rcx, [rax+rsi]
	sub	r9, rsi
	je	.L1760
	lea	rax, [rcx+r14]
	cmp	r9, 1
	je	.L1925
	mov	rdx, rcx
	mov	r8, r9
	mov	rcx, rax
	call	memmove
	mov	rcx, QWORD PTR 88[rsp]
	add	rcx, QWORD PTR 192[rsp]
.L1760:
	cmp	r14, 1
	je	.L1926
	mov	r8, r14
	mov	edx, 48
	call	memset
.L1763:
	mov	rax, QWORD PTR 192[rsp]
	mov	QWORD PTR 200[rsp], r12
	cmp	BYTE PTR 103[rsp], 0
	mov	BYTE PTR [rax+r12], 0
	mov	r12, QWORD PTR 200[rsp]
	je	.L1751
	mov	rax, QWORD PTR 192[rsp]
	mov	rsi, QWORD PTR 88[rsp]
	mov	BYTE PTR [rax+rsi], 46
	mov	r12, QWORD PTR 200[rsp]
	jmp	.L1751
.L1726:
	mov	rcx, QWORD PTR 64[rsp]
	add	rcx, 1
	js	.L1727
.L1728:
	lea	rsi, 192[rsp]
	call	_Znwy
	mov	r9, QWORD PTR 200[rsp]
	mov	rsi, rax
	mov	r10, QWORD PTR 192[rsp]
	lea	r8, 1[r9]
	test	r9, r9
	je	.L1927
	test	r8, r8
	jne	.L1733
	cmp	r10, rbp
	je	.L1928
.L1730:
	mov	rax, QWORD PTR 208[rsp]
	mov	rcx, r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 200[rsp]
	mov	QWORD PTR 192[rsp], rsi
	mov	rax, QWORD PTR 64[rsp]
	test	r9, r9
	mov	QWORD PTR 208[rsp], rax
	jne	.L1722
.L1724:
	mov	rax, QWORD PTR 88[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L1731
	mov	r10, QWORD PTR 192[rsp]
	cmp	r10, rbp
	je	.L1798
.L1736:
	mov	rax, QWORD PTR 208[rsp]
	cmp	rax, r12
	jnb	.L1737
	add	rax, rax
	cmp	r12, rax
	jnb	.L1738
	lea	rcx, 1[rax]
	test	rax, rax
	mov	r14, r12
	mov	r12, rax
	jns	.L1746
.L1745:
	lea	rsi, 192[rsp]
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L1682:
	mov	rcx, QWORD PTR 88[rsp]
	add	rcx, 1
	jns	.L1684
.L1683:
	lea	rsi, 192[rsp]
	call	_ZSt17__throw_bad_allocv
.L1918:
	mov	eax, DWORD PTR 64[rsp]
	mov	DWORD PTR 32[rsp], r13d
	mov	rcx, r14
	mov	r9, QWORD PTR 80[rsp]
	mov	DWORD PTR 40[rsp], eax
	call	_ZSt8to_charsPcS_eSt12chars_formati
	mov	rsi, QWORD PTR 144[rsp]
	mov	rax, QWORD PTR 152[rsp]
	mov	r10, QWORD PTR 88[rsp]
	jmp	.L1699
.L1672:
	mov	rax, QWORD PTR 64[rsp]
	cmp	r13d, 2
	mov	BYTE PTR 103[rsp], 1
	lea	rsi, 128[rax]
	mov	QWORD PTR 88[rsp], rsi
	jne	.L1677
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
	jmp	.L1677
.L1741:
	test	r12, r12
	je	.L1743
	cmp	r12, 1
	je	.L1929
	mov	rcx, r10
	mov	r8, r12
	mov	rdx, r13
	call	memcpy
	mov	r10, QWORD PTR 192[rsp]
	jmp	.L1743
.L1897:
	mov	rax, QWORD PTR 88[rsp]
	mov	r8, r12
	lea	rsi, 0[r13+rax]
	sub	r8, rax
	lea	rcx, [rax+r14]
	mov	rdx, rsi
	add	rcx, r13
	call	memmove
	cmp	BYTE PTR 103[rsp], 0
	je	.L1718
	mov	rax, QWORD PTR 88[rsp]
	mov	BYTE PTR [rsi], 46
	lea	rsi, 1[r13+rax]
.L1718:
	mov	r8, QWORD PTR 72[rsp]
	mov	edx, 48
	mov	rcx, rsi
	call	memset
	movzx	r9d, BYTE PTR [rbx]
	mov	r12, QWORD PTR 64[rsp]
	jmp	.L1708
.L1810:
	mov	QWORD PTR 88[rsp], 30
	mov	ecx, 31
.L1690:
	lea	rsi, 192[rsp]
	call	_Znwy
	mov	r8, QWORD PTR 200[rsp]
	mov	r10, rax
	mov	rsi, QWORD PTR 192[rsp]
	cmp	r8, 1
	je	.L1930
	test	r8, r8
	je	.L1890
	mov	rdx, rsi
	mov	rcx, rax
	call	memcpy
	mov	r10, rax
.L1890:
	cmp	rsi, rbp
	je	.L1695
	mov	rax, QWORD PTR 208[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 104[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 104[rsp]
.L1695:
	mov	rax, QWORD PTR 88[rsp]
	mov	QWORD PTR 192[rsp], r10
	mov	QWORD PTR 208[rsp], rax
	jmp	.L1691
.L1809:
	mov	eax, 15
	jmp	.L1679
.L1917:
	test	rsi, rsi
	js	.L1692
	lea	rcx, 1[rsi]
	jmp	.L1690
.L1759:
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
	jmp	.L1760
.L1922:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r10], al
	jmp	.L1888
.L1927:
	movzx	eax, BYTE PTR [r10]
	cmp	r10, rbp
	mov	BYTE PTR [rsi], al
	jne	.L1730
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 192[rsp], rsi
	mov	QWORD PTR 208[rsp], rax
	mov	rax, QWORD PTR 88[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L1731
	mov	r10, rsi
	jmp	.L1736
.L1902:
	movabs	rax, 9223372036854775807
	mov	rsi, QWORD PTR 72[rsp]
	sub	rax, r12
	cmp	rax, rsi
	jb	.L1931
	mov	rax, QWORD PTR 72[rsp]
	lea	r13, [r12+rax]
	mov	rax, QWORD PTR 192[rsp]
	cmp	rax, rbp
	je	.L1820
	mov	rdx, QWORD PTR 208[rsp]
.L1753:
	cmp	rdx, r13
	jb	.L1932
.L1754:
	cmp	QWORD PTR 72[rsp], 1
	lea	rcx, [rax+r12]
	je	.L1933
	mov	r8, QWORD PTR 72[rsp]
	mov	edx, 48
	call	memset
.L1756:
	mov	rax, QWORD PTR 192[rsp]
	mov	QWORD PTR 200[rsp], r13
	mov	BYTE PTR [rax+r13], 0
	mov	r12, QWORD PTR 200[rsp]
	jmp	.L1751
.L1733:
	mov	rdx, r10
	mov	rcx, rax
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 80[rsp], r10
	call	memcpy
	mov	r10, QWORD PTR 80[rsp]
	mov	r9, QWORD PTR 104[rsp]
	cmp	r10, rbp
	jne	.L1730
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 192[rsp], rsi
	mov	QWORD PTR 208[rsp], rax
	jmp	.L1722
.L1915:
	movzx	eax, BYTE PTR 272[rsp]
	mov	BYTE PTR [rcx], al
	mov	r8, QWORD PTR 264[rsp]
	mov	rcx, QWORD PTR 224[rsp]
	jmp	.L1769
.L1930:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r10], al
	jmp	.L1890
.L1901:
	lea	rsi, 192[rsp]
	mov	edx, 46
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	jmp	.L1749
.L1721:
	mov	rax, QWORD PTR 64[rsp]
	cmp	rax, 15
	jbe	.L1722
.L1894:
	test	rax, rax
	js	.L1793
	cmp	rax, 29
	ja	.L1726
	mov	QWORD PTR 64[rsp], 30
.L1794:
	mov	rax, QWORD PTR 64[rsp]
	lea	rcx, 1[rax]
	jmp	.L1728
.L1821:
	mov	edx, 15
	jmp	.L1758
.L1926:
	mov	BYTE PTR [rcx], 48
	jmp	.L1763
.L1925:
	movzx	edx, BYTE PTR [rcx]
	mov	BYTE PTR [rax], dl
	mov	rcx, QWORD PTR 192[rsp]
	add	rcx, rsi
	jmp	.L1760
.L1929:
	movzx	eax, BYTE PTR 0[r13]
	mov	BYTE PTR [r10], al
	mov	r10, QWORD PTR 192[rsp]
	jmp	.L1743
.L1932:
	mov	rax, QWORD PTR 72[rsp]
	xor	r9d, r9d
	xor	r8d, r8d
	mov	rdx, r12
	lea	rsi, 192[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 32[rsp], rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE44:
	mov	rax, QWORD PTR 192[rsp]
	jmp	.L1754
.L1911:
	mov	rax, QWORD PTR [r14]
	mov	rcx, r14
.LEHB45:
	call	[QWORD PTR [rax]]
.LEHE45:
	jmp	.L1785
.L1920:
	cmp	r12, 29
	ja	.L1738
	lea	rsi, 192[rsp]
	mov	ecx, 31
.LEHB46:
	call	_Znwy
	mov	r14, r12
	mov	r10, rax
	mov	r12d, 30
	jmp	.L1739
.L1933:
	mov	BYTE PTR [rcx], 48
	jmp	.L1756
.L1820:
	mov	edx, 15
	jmp	.L1753
.L1928:
	mov	QWORD PTR 192[rsp], rax
	mov	rax, QWORD PTR 64[rsp]
	mov	r9, -1
	mov	QWORD PTR 208[rsp], rax
	jmp	.L1734
.L1900:
	movzx	eax, BYTE PTR 0[r13]
	mov	rsi, r12
	mov	r12d, 1
	mov	BYTE PTR [r10], al
	jmp	.L1747
.L1899:
	mov	QWORD PTR 64[rsp], rax
	jmp	.L1794
.L1921:
	lea	rcx, .LC7[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1692:
	lea	rcx, .LC7[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1793:
	lea	rcx, .LC7[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1924:
	lea	rcx, .LC34[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1923:
	lea	rdx, .LC35[rip]
	mov	r8, rax
	lea	rcx, .LC36[rip]
	lea	rsi, 192[rsp]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L1731:
	lea	rcx, .LC33[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1931:
	lea	rcx, .LC34[rip]
	lea	rsi, 192[rsp]
	call	_ZSt20__throw_length_errorPKc
.LEHE46:
.L1662:
	xor	r13d, r13d
	xor	edi, edi
	mov	BYTE PTR 72[rsp], 0
	xor	r12d, r12d
	jmp	.L1670
.L1836:
	mov	rbx, rax
.L1792:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB47:
	call	_Unwind_Resume
.LEHE47:
.L1838:
	mov	rbx, rax
	jmp	.L1790
.L1837:
	mov	rcx, r14
	mov	rbx, rax
	call	_ZNSt6localeD1Ev
.L1790:
	lea	rcx, 224[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	cmp	BYTE PTR 184[rsp], 0
	je	.L1791
	lea	rcx, 176[rsp]
	call	_ZNSt6localeD1Ev
.L1791:
	lea	rsi, 192[rsp]
	jmp	.L1792
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5410:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5410-.LLSDACSB5410
.LLSDACSB5410:
	.uleb128 .LEHB39-.LFB5410
	.uleb128 .LEHE39-.LEHB39
	.uleb128 .L1836-.LFB5410
	.uleb128 0
	.uleb128 .LEHB40-.LFB5410
	.uleb128 .LEHE40-.LEHB40
	.uleb128 .L1837-.LFB5410
	.uleb128 0
	.uleb128 .LEHB41-.LFB5410
	.uleb128 .LEHE41-.LEHB41
	.uleb128 .L1838-.LFB5410
	.uleb128 0
	.uleb128 .LEHB42-.LFB5410
	.uleb128 .LEHE42-.LEHB42
	.uleb128 .L1836-.LFB5410
	.uleb128 0
	.uleb128 .LEHB43-.LFB5410
	.uleb128 .LEHE43-.LEHB43
	.uleb128 .L1838-.LFB5410
	.uleb128 0
	.uleb128 .LEHB44-.LFB5410
	.uleb128 .LEHE44-.LEHB44
	.uleb128 .L1836-.LFB5410
	.uleb128 0
	.uleb128 .LEHB45-.LFB5410
	.uleb128 .LEHE45-.LEHB45
	.uleb128 .L1838-.LFB5410
	.uleb128 0
	.uleb128 .LEHB46-.LFB5410
	.uleb128 .LEHE46-.LEHB46
	.uleb128 .L1836-.LFB5410
	.uleb128 0
	.uleb128 .LEHB47-.LFB5410
	.uleb128 .LEHE47-.LEHB47
	.uleb128 0
	.uleb128 0
.LLSDACSE5410:
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
.LFB5407:
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
	jne	.L2173
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L1954
	lea	rdx, .L2078[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2078:
	.long	.L1954-.L2078
	.long	.L2079-.L2078
	.long	.L2109-.L2078
	.long	.L2110-.L2078
	.long	.L2111-.L2078
	.long	.L2112-.L2078
	.long	.L2113-.L2078
	.long	.L2108-.L2078
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1954:
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
.L1953:
	mov	QWORD PTR 56[rsp], 6
	xor	r15d, r15d
	cmp	eax, 132
	je	.L2107
	lea	rax, 384[rsp]
	mov	QWORD PTR 64[rsp], rax
	lea	r13, 257[rsp]
.L1951:
	test	r12b, r12b
	je	.L1981
	cmp	r13, rsi
	mov	r12, QWORD PTR __imp_toupper[rip]
	mov	r14, r13
	je	.L1983
	.p2align 4,,10
	.p2align 3
.L1982:
	movsx	ecx, BYTE PTR [r14]
	add	r14, 1
	call	r12
	mov	BYTE PTR -1[r14], al
	cmp	rsi, r14
	jne	.L1982
.L1983:
	movsx	ecx, dil
	call	r12
	mov	edi, eax
.L1981:
	movmskpd	eax, xmm6
	movzx	r9d, BYTE PTR [rbx]
	test	al, 1
	jne	.L1984
	mov	eax, r9d
	and	eax, 12
	cmp	al, 4
	je	.L2174
	cmp	al, 12
	jne	.L1984
	mov	BYTE PTR -1[r13], 32
	movzx	r9d, BYTE PTR [rbx]
	sub	r13, 1
	.p2align 4,,10
	.p2align 3
.L1984:
	mov	r12, rsi
	sub	r12, r13
	test	r9b, 16
	je	.L1986
	movsd	xmm1, QWORD PTR .LC39[rip]
	movapd	xmm0, xmm6
	andpd	xmm0, XMMWORD PTR .LC38[rip]
	ucomisd	xmm1, xmm0
	jb	.L1986
	test	r12, r12
	je	.L2090
	mov	r8, r12
	mov	edx, 46
	mov	rcx, r13
	mov	BYTE PTR 72[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	mov	r10, rax
	je	.L1988
	sub	r10, r13
	cmp	r10, -1
	je	.L1988
	lea	rax, 1[r10]
	mov	QWORD PTR 80[rsp], r12
	cmp	rax, r12
	jnb	.L1989
	mov	r8, r12
	movsx	edx, dil
	mov	QWORD PTR 88[rsp], r10
	lea	rcx, 0[r13+rax]
	sub	r8, rax
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	mov	r10, QWORD PTR 88[rsp]
	je	.L1989
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	mov	QWORD PTR 80[rsp], rax
.L1989:
	cmp	QWORD PTR 80[rsp], r10
	sete	BYTE PTR 88[rsp]
	sete	al
	test	r15b, r15b
	movzx	eax, al
	mov	QWORD PTR 72[rsp], rax
	jne	.L1990
	xor	r15d, r15d
.L1991:
	cmp	QWORD PTR 72[rsp], 0
	je	.L1986
.L2075:
	mov	r9, QWORD PTR 168[rsp]
	mov	rdx, QWORD PTR 72[rsp]
	test	r9, r9
	lea	rax, [r12+rdx]
	mov	QWORD PTR 56[rsp], rax
	jne	.L1993
	mov	rax, QWORD PTR 64[rsp]
	sub	rax, rsi
	cmp	rax, rdx
	jnb	.L2175
	cmp	QWORD PTR 160[rsp], rbp
	je	.L2176
	mov	rax, QWORD PTR 176[rsp]
	mov	rsi, QWORD PTR 56[rsp]
	cmp	rax, rsi
	jnb	.L2002
.L2001:
	cmp	QWORD PTR 56[rsp], 0
	js	.L2071
	add	rax, rax
	cmp	QWORD PTR 56[rsp], rax
	jnb	.L2004
	test	rax, rax
	jns	.L2177
.L2005:
	lea	rsi, 160[rsp]
.LEHB48:
	call	_ZSt17__throw_bad_allocv
.L2016:
	mov	rcx, r12
	mov	r14, r12
	add	rcx, 1
	js	.L2023
.L2024:
	lea	rsi, 160[rsp]
	call	_Znwy
.LEHE48:
	cmp	r14, 1
	mov	r10, rax
	je	.L2178
.L2017:
	mov	rcx, r10
	mov	r8, r14
	mov	rdx, r13
	call	memcpy
	mov	rsi, r12
	mov	r12, r14
	mov	r10, rax
.L2025:
	mov	rcx, QWORD PTR 160[rsp]
	cmp	rcx, rbp
	je	.L2026
	mov	rax, QWORD PTR 176[rsp]
	mov	QWORD PTR 56[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 56[rsp]
.L2026:
	mov	QWORD PTR 160[rsp], r10
	mov	QWORD PTR 176[rsp], rsi
.L2021:
	cmp	BYTE PTR 88[rsp], 0
	mov	QWORD PTR 168[rsp], r12
	mov	BYTE PTR [r10+r12], 0
	jne	.L2179
.L2027:
	test	r15, r15
	mov	r12, QWORD PTR 168[rsp]
	jne	.L2180
.L2029:
	mov	r13, QWORD PTR 160[rsp]
	movzx	r9d, BYTE PTR [rbx]
	.p2align 4,,10
	.p2align 3
.L1986:
	lea	rsi, 208[rsp]
	and	r9d, 32
	mov	QWORD PTR 144[rsp], 0
	mov	BYTE PTR 152[rsp], 0
	mov	QWORD PTR 192[rsp], rsi
	mov	QWORD PTR 200[rsp], 0
	mov	BYTE PTR 208[rsp], 0
	je	.L2100
	mov	rax, QWORD PTR 496[rsp]
	cmp	BYTE PTR 32[rax], 0
	lea	r15, 24[rax]
	je	.L2181
.L2044:
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
.LEHB49:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE49:
	mov	rax, QWORD PTR 224[rsp]
	lea	rdi, 240[rsp]
	mov	rcx, QWORD PTR 192[rsp]
	mov	r8, QWORD PTR 232[rsp]
	cmp	rax, rdi
	je	.L2182
	movq	xmm0, r8
	cmp	rcx, rsi
	movhps	xmm0, QWORD PTR 240[rsp]
	je	.L2183
	test	rcx, rcx
	mov	rdx, QWORD PTR 208[rsp]
	mov	QWORD PTR 192[rsp], rax
	movups	XMMWORD PTR 200[rsp], xmm0
	je	.L2052
	mov	QWORD PTR 224[rsp], rcx
	mov	QWORD PTR 240[rsp], rdx
.L2051:
	mov	QWORD PTR 232[rsp], 0
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 224[rsp]
	cmp	rcx, rdi
	je	.L2053
	mov	rax, QWORD PTR 240[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2053:
	mov	rcx, r14
	call	_ZNSt6localeD1Ev
	movzx	eax, WORD PTR [rbx]
	mov	r12, QWORD PTR 200[rsp]
	mov	rdi, QWORD PTR 192[rsp]
	and	ax, 384
	cmp	ax, 128
	je	.L2184
.L2054:
	cmp	ax, 256
	je	.L2056
	mov	rax, QWORD PTR 496[rsp]
	mov	r14, QWORD PTR 16[rax]
.L2060:
	lea	rdx, 96[rsp]
	mov	rcx, r14
	mov	QWORD PTR 96[rsp], r12
	mov	QWORD PTR 104[rsp], rdi
.LEHB50:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L2169:
	mov	rcx, QWORD PTR 192[rsp]
	mov	rbx, rax
	cmp	rcx, rsi
	je	.L2064
	mov	rax, QWORD PTR 208[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2064:
	cmp	BYTE PTR 152[rsp], 0
	jne	.L2185
.L2065:
	mov	rcx, QWORD PTR 160[rsp]
	cmp	rcx, rbp
	je	.L2129
	mov	rax, QWORD PTR 176[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	nop
.L2129:
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
.L2100:
	movzx	eax, WORD PTR [rbx]
	mov	rdi, r13
	and	ax, 384
	cmp	ax, 128
	jne	.L2054
.L2184:
	movzx	eax, WORD PTR 4[rbx]
.L2055:
	mov	rdx, QWORD PTR 496[rsp]
	cmp	r12, rax
	mov	r14, QWORD PTR 16[rdx]
	jnb	.L2060
	movzx	edx, BYTE PTR [rbx]
	sub	rax, r12
	movzx	ecx, BYTE PTR 8[rbx]
	mov	rbx, rax
	mov	r8d, edx
	and	r8d, 3
	movsx	eax, cl
	jne	.L2062
	and	edx, 64
	je	.L2102
	movsd	xmm0, QWORD PTR .LC39[rip]
	andpd	xmm6, XMMWORD PTR .LC38[rip]
	ucomisd	xmm0, xmm6
	jnb	.L2186
.L2102:
	mov	eax, 32
	mov	r8d, 2
.L2062:
	lea	rdx, 96[rsp]
	mov	DWORD PTR 32[rsp], eax
	mov	r9, rbx
	mov	rcx, r14
	mov	QWORD PTR 96[rsp], r12
	mov	QWORD PTR 104[rsp], rdi
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
.LEHE50:
	jmp	.L2169
	.p2align 4,,10
	.p2align 3
.L2173:
	cmp	dl, 2
	je	.L2187
	mov	QWORD PTR 56[rsp], -1
	cmp	dl, 4
	je	.L2188
.L1937:
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L1940
	lea	rdx, .L1942[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L1942:
	.long	.L1949-.L1942
	.long	.L2081-.L1942
	.long	.L1947-.L1942
	.long	.L1946-.L1942
	.long	.L2163-.L1942
	.long	.L2165-.L1942
	.long	.L1943-.L1942
	.long	.L2164-.L1942
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2185:
	lea	rcx, 144[rsp]
	call	_ZNSt6localeD1Ev
	jmp	.L2065
	.p2align 4,,10
	.p2align 3
.L2109:
	mov	r12d, 1
.L1952:
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
	jmp	.L1953
	.p2align 4,,10
	.p2align 3
.L2186:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	eax, 48
	mov	r8d, 2
	cmp	BYTE PTR [rcx+rdx], 15
	jbe	.L2062
	mov	rax, QWORD PTR 24[r14]
	movzx	edx, BYTE PTR [rdi]
	lea	rcx, 1[rax]
	mov	QWORD PTR 24[r14], rcx
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[r14]
	sub	rax, QWORD PTR 8[r14]
	cmp	rax, QWORD PTR 16[r14]
	je	.L2189
.L2063:
	add	rdi, 1
	sub	r12, 1
	mov	eax, 48
	mov	r8d, 2
	jmp	.L2062
	.p2align 4,,10
	.p2align 3
.L2090:
	xor	eax, eax
.L1987:
	test	r15b, r15b
	je	.L2190
	mov	BYTE PTR 88[rsp], r15b
	mov	QWORD PTR 80[rsp], rax
	mov	QWORD PTR 72[rsp], 1
	jmp	.L2074
	.p2align 4,,10
	.p2align 3
.L2110:
	mov	QWORD PTR 56[rsp], 6
.L1946:
	xor	r12d, r12d
.L1945:
	mov	r14d, 1
	mov	edi, 101
	xor	r15d, r15d
.L1948:
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
	je	.L1950
	lea	rax, 384[rsp]
	mov	r13, QWORD PTR 72[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L1951
	.p2align 4,,10
	.p2align 3
.L2111:
	mov	QWORD PTR 56[rsp], 6
.L2163:
	mov	r12d, 1
	jmp	.L1945
	.p2align 4,,10
	.p2align 3
.L2112:
	mov	QWORD PTR 56[rsp], 6
.L2165:
	mov	r14d, 2
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L1948
	.p2align 4,,10
	.p2align 3
.L2108:
	mov	QWORD PTR 56[rsp], 6
.L2164:
	mov	r12d, 1
.L1941:
	mov	r14d, 3
	mov	edi, 101
	mov	r15d, 1
	jmp	.L1948
	.p2align 4,,10
	.p2align 3
.L2113:
	mov	QWORD PTR 56[rsp], 6
.L1943:
	xor	r12d, r12d
	jmp	.L1941
	.p2align 4,,10
	.p2align 3
.L2079:
	xor	r12d, r12d
	jmp	.L1952
	.p2align 4,,10
	.p2align 3
.L2188:
	mov	rdi, QWORD PTR 496[rsp]
	mov	BYTE PTR 208[rsp], 0
	movzx	eax, WORD PTR 6[rcx]
	movzx	edx, BYTE PTR [rdi]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L2191
	test	cl, cl
	jne	.L1939
	mov	rdi, QWORD PTR 496[rsp]
	mov	rdi, QWORD PTR [rdi]
	mov	rdx, rdi
	mov	QWORD PTR 56[rsp], rdi
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L1939
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
.L1939:
	lea	rcx, 192[rsp]
	lea	rsi, 160[rsp]
.LEHB51:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE51:
	mov	QWORD PTR 56[rsp], rax
	movzx	eax, BYTE PTR 1[rbx]
	jmp	.L1937
	.p2align 4,,10
	.p2align 3
.L2174:
	mov	BYTE PTR -1[r13], 43
	sub	r13, 1
	movzx	r9d, BYTE PTR [rbx]
	jmp	.L1984
	.p2align 4,,10
	.p2align 3
.L2181:
	mov	rcx, r15
	call	_ZNSt6localeC1Ev
	mov	rax, QWORD PTR 496[rsp]
	mov	BYTE PTR 32[rax], 1
	jmp	.L2044
	.p2align 4,,10
	.p2align 3
.L2056:
	mov	rdx, QWORD PTR 496[rsp]
	mov	BYTE PTR 240[rsp], 0
	movzx	eax, WORD PTR 4[rbx]
	movzx	edx, BYTE PTR [rdx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L2192
	test	cl, cl
	jne	.L2059
	mov	rdx, QWORD PTR 496[rsp]
	mov	rdx, QWORD PTR [rdx]
	mov	QWORD PTR 56[rsp], rdx
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L2059
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
.L2059:
	lea	rcx, 224[rsp]
.LEHB52:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE52:
	jmp	.L2055
	.p2align 4,,10
	.p2align 3
.L2183:
	mov	QWORD PTR 192[rsp], rax
	movups	XMMWORD PTR 200[rsp], xmm0
.L2052:
	mov	QWORD PTR 224[rsp], rdi
	lea	rdi, 240[rsp]
	mov	rcx, rdi
	jmp	.L2051
	.p2align 4,,10
	.p2align 3
.L2187:
	movzx	edi, WORD PTR 6[rcx]
	mov	QWORD PTR 56[rsp], rdi
	jmp	.L1937
	.p2align 4,,10
	.p2align 3
.L2182:
	test	r8, r8
	je	.L2047
	cmp	r8, 1
	je	.L2193
	mov	rdx, rdi
	call	memcpy
	mov	r8, QWORD PTR 232[rsp]
	mov	rcx, QWORD PTR 192[rsp]
.L2047:
	mov	QWORD PTR 200[rsp], r8
	mov	BYTE PTR [rcx+r8], 0
	mov	rcx, QWORD PTR 224[rsp]
	jmp	.L2051
	.p2align 4,,10
	.p2align 3
.L1990:
	mov	rax, QWORD PTR 80[rsp]
	sub	rax, 1
.L2074:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	r15, QWORD PTR 56[rsp]
	cmp	BYTE PTR [rcx+rdx], 16
	adc	rax, -1
	sub	r15, rax
	add	QWORD PTR 72[rsp], r15
	jmp	.L1991
	.p2align 4,,10
	.p2align 3
.L2107:
	mov	BYTE PTR 72[rsp], 0
	mov	QWORD PTR 64[rsp], 134
.L1955:
	mov	r9, QWORD PTR 160[rsp]
	cmp	r9, rbp
	je	.L2087
	mov	rax, QWORD PTR 176[rsp]
.L1957:
	mov	rsi, QWORD PTR 64[rsp]
	cmp	rax, rsi
	jb	.L2194
.L1980:
	cmp	r9, rbp
	je	.L2088
	mov	rax, QWORD PTR 176[rsp]
	lea	rsi, [rax+rax]
	cmp	rax, rsi
	mov	QWORD PTR 64[rsp], rsi
	jb	.L2195
.L1969:
	mov	rax, QWORD PTR 64[rsp]
	lea	rdx, 1[r9]
	mov	QWORD PTR 64[rsp], r9
	cmp	BYTE PTR 72[rsp], 0
	lea	r8, -1[r9+rax]
	jne	.L2196
	test	r14d, r14d
	jne	.L2197
	movapd	xmm3, xmm6
	mov	rcx, r13
	call	_ZSt8to_charsPcS_d
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
.L1977:
	test	eax, eax
	jne	.L1979
	mov	rdx, QWORD PTR 160[rsp]
	mov	rax, rsi
	sub	rax, r9
	mov	QWORD PTR 168[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rax, QWORD PTR 160[rsp]
	lea	r13, 1[rax]
	add	rax, QWORD PTR 168[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L1951
	.p2align 4,,10
	.p2align 3
.L1988:
	movsx	edx, dil
	mov	r8, r12
	mov	rcx, r13
	mov	BYTE PTR 72[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	je	.L2094
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	jmp	.L1987
.L2081:
	mov	r14d, 4
	mov	edi, 112
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L1948
.L1947:
	mov	r14d, 4
	mov	edi, 112
	xor	r15d, r15d
	mov	r12d, 1
	jmp	.L1948
.L1949:
	mov	r14d, 3
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L1948
.L2190:
	mov	QWORD PTR 80[rsp], rax
	xor	r15d, r15d
	mov	QWORD PTR 72[rsp], 1
	mov	BYTE PTR 88[rsp], 1
	jmp	.L2075
.L2197:
	mov	DWORD PTR 32[rsp], r14d
	movapd	xmm3, xmm6
	mov	rcx, r13
	call	_ZSt8to_charsPcS_dSt12chars_format
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
	jmp	.L1977
.L2191:
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
	jmp	.L1939
.L2094:
	mov	rax, r12
	jmp	.L1987
.L2176:
	mov	rax, QWORD PTR 56[rsp]
	cmp	rax, 15
	ja	.L2172
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L2009
	mov	r10, rbp
.L2076:
	cmp	r12, 15
	ja	.L2198
.L2015:
	cmp	r13, r10
	jb	.L2019
	cmp	r10, r13
	jb	.L2019
	xor	eax, eax
	mov	QWORD PTR 32[rsp], r12
	mov	r9, r13
	xor	r8d, r8d
	lea	rsi, 160[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	rdx, r10
	mov	rcx, rsi
.LEHB53:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L2021
	.p2align 4,,10
	.p2align 3
.L1979:
	mov	rdx, QWORD PTR 160[rsp]
	cmp	eax, 132
	mov	QWORD PTR 168[rsp], 0
	mov	BYTE PTR [rdx], 0
	mov	r9, QWORD PTR 160[rsp]
	mov	rdx, QWORD PTR 168[rsp]
	je	.L1980
	lea	rax, [r9+rdx]
	lea	r13, 1[r9]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L1951
	.p2align 4,,10
	.p2align 3
.L2194:
	test	rsi, rsi
	js	.L2199
	add	rax, rax
	cmp	QWORD PTR 64[rsp], rax
	jnb	.L1960
	test	rax, rax
	js	.L1961
	lea	rcx, 1[rax]
	mov	QWORD PTR 64[rsp], rax
.L1962:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r9, rax
	mov	rax, QWORD PTR 168[rsp]
	mov	rsi, QWORD PTR 160[rsp]
	lea	r8, 1[rax]
	test	rax, rax
	je	.L2200
	test	r8, r8
	je	.L2166
	mov	rcx, r9
	mov	rdx, rsi
	call	memcpy
	mov	r9, rax
.L2166:
	cmp	rsi, rbp
	je	.L1965
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 80[rsp]
.L1965:
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 160[rsp], r9
	mov	QWORD PTR 176[rsp], rax
	jmp	.L1980
.L2192:
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
	jmp	.L2059
.L1993:
	cmp	QWORD PTR 160[rsp], rbp
	je	.L1999
	mov	rax, QWORD PTR 176[rsp]
	mov	rsi, QWORD PTR 56[rsp]
	cmp	rax, rsi
	jb	.L2001
.L2000:
	mov	rax, QWORD PTR 80[rsp]
	cmp	r9, rax
	jb	.L2201
.L2012:
	movabs	rax, 9223372036854775807
	mov	rsi, QWORD PTR 72[rsp]
	sub	rax, r9
	cmp	rax, rsi
	jb	.L2202
	mov	rax, QWORD PTR 72[rsp]
	lea	r12, [r9+rax]
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, rbp
	je	.L2099
	mov	rdx, QWORD PTR 176[rsp]
.L2036:
	cmp	rdx, r12
	jb	.L2037
	mov	rsi, QWORD PTR 80[rsp]
	lea	rcx, [rax+rsi]
	sub	r9, rsi
	je	.L2038
	mov	rax, QWORD PTR 72[rsp]
	add	rax, rcx
	cmp	r9, 1
	je	.L2203
	mov	rdx, rcx
	mov	r8, r9
	mov	rcx, rax
	call	memmove
	mov	rcx, QWORD PTR 80[rsp]
	add	rcx, QWORD PTR 160[rsp]
.L2038:
	cmp	QWORD PTR 72[rsp], 1
	je	.L2204
	mov	r8, QWORD PTR 72[rsp]
	mov	edx, 48
	call	memset
.L2041:
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 168[rsp], r12
	cmp	BYTE PTR 88[rsp], 0
	mov	BYTE PTR [rax+r12], 0
	mov	r12, QWORD PTR 168[rsp]
	je	.L2029
	mov	rax, QWORD PTR 160[rsp]
	mov	rsi, QWORD PTR 80[rsp]
	mov	BYTE PTR [rax+rsi], 46
	mov	r12, QWORD PTR 168[rsp]
	jmp	.L2029
.L2004:
	mov	rcx, QWORD PTR 56[rsp]
	add	rcx, 1
	js	.L2005
.L2006:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r9, QWORD PTR 168[rsp]
	mov	rsi, rax
	mov	r14, QWORD PTR 160[rsp]
	lea	r8, 1[r9]
	test	r9, r9
	je	.L2205
	test	r8, r8
	jne	.L2011
	cmp	r14, rbp
	je	.L2206
.L2008:
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, r14
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 168[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	rax, QWORD PTR 56[rsp]
	test	r9, r9
	mov	QWORD PTR 176[rsp], rax
	jne	.L2000
.L2002:
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L2009
	mov	r10, QWORD PTR 160[rsp]
	cmp	r10, rbp
	je	.L2076
.L2014:
	mov	rax, QWORD PTR 176[rsp]
	cmp	rax, r12
	jnb	.L2015
	add	rax, rax
	cmp	r12, rax
	jnb	.L2016
	lea	rcx, 1[rax]
	test	rax, rax
	mov	r14, r12
	mov	r12, rax
	jns	.L2024
.L2023:
	lea	rsi, 160[rsp]
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L1960:
	mov	rcx, QWORD PTR 64[rsp]
	add	rcx, 1
	jns	.L1962
.L1961:
	lea	rsi, 160[rsp]
	call	_ZSt17__throw_bad_allocv
.L2196:
	mov	eax, DWORD PTR 56[rsp]
	mov	DWORD PTR 32[rsp], r14d
	movapd	xmm3, xmm6
	mov	rcx, r13
	mov	DWORD PTR 40[rsp], eax
	call	_ZSt8to_charsPcS_dSt12chars_formati
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
	jmp	.L1977
.L1950:
	mov	rax, QWORD PTR 56[rsp]
	cmp	r14d, 2
	mov	BYTE PTR 72[rsp], 1
	lea	rsi, 128[rax]
	mov	QWORD PTR 64[rsp], rsi
	jne	.L1955
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
	jmp	.L1955
.L2019:
	test	r12, r12
	je	.L2021
	cmp	r12, 1
	je	.L2207
	mov	rcx, r10
	mov	r8, r12
	mov	rdx, r13
	call	memcpy
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L2021
.L2175:
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
	je	.L1996
	mov	rax, QWORD PTR 80[rsp]
	mov	BYTE PTR [rsi], 46
	lea	rsi, 1[r13+rax]
.L1996:
	mov	r8, r15
	mov	edx, 48
	mov	rcx, rsi
	call	memset
	movzx	r9d, BYTE PTR [rbx]
	mov	r12, QWORD PTR 56[rsp]
	jmp	.L1986
.L2088:
	mov	QWORD PTR 64[rsp], 30
	mov	ecx, 31
.L1968:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r8, QWORD PTR 168[rsp]
	mov	r9, rax
	mov	rsi, QWORD PTR 160[rsp]
	cmp	r8, 1
	je	.L2208
	test	r8, r8
	je	.L2168
	mov	rdx, rsi
	mov	rcx, rax
	call	memcpy
	mov	r9, rax
.L2168:
	cmp	rsi, rbp
	je	.L1973
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 80[rsp]
.L1973:
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 160[rsp], r9
	mov	QWORD PTR 176[rsp], rax
	jmp	.L1969
.L2087:
	mov	eax, 15
	jmp	.L1957
.L2195:
	test	rsi, rsi
	js	.L1970
	lea	rcx, 1[rsi]
	jmp	.L1968
.L2037:
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
	jmp	.L2038
.L2200:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r9], al
	jmp	.L2166
.L2205:
	movzx	eax, BYTE PTR [r14]
	cmp	r14, rbp
	mov	BYTE PTR [rsi], al
	jne	.L2008
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	QWORD PTR 176[rsp], rax
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L2009
	mov	r10, rsi
	jmp	.L2014
.L2180:
	movabs	rax, 9223372036854775807
	sub	rax, r12
	cmp	rax, r15
	jb	.L2209
	mov	rax, QWORD PTR 160[rsp]
	lea	r13, [r12+r15]
	cmp	rax, rbp
	je	.L2098
	mov	rdx, QWORD PTR 176[rsp]
.L2031:
	cmp	rdx, r13
	jb	.L2210
.L2032:
	lea	rcx, [rax+r12]
	cmp	r15, 1
	je	.L2211
	mov	r8, r15
	mov	edx, 48
	call	memset
.L2034:
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 168[rsp], r13
	mov	BYTE PTR [rax+r13], 0
	mov	r12, QWORD PTR 168[rsp]
	jmp	.L2029
.L2011:
	mov	rdx, r14
	mov	rcx, rax
	mov	QWORD PTR 64[rsp], r9
	call	memcpy
	cmp	r14, rbp
	mov	r9, QWORD PTR 64[rsp]
	jne	.L2008
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	QWORD PTR 176[rsp], rax
	jmp	.L2000
.L2193:
	movzx	eax, BYTE PTR 240[rsp]
	mov	BYTE PTR [rcx], al
	mov	r8, QWORD PTR 232[rsp]
	mov	rcx, QWORD PTR 192[rsp]
	jmp	.L2047
.L2208:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r9], al
	jmp	.L2168
.L2179:
	lea	rsi, 160[rsp]
	mov	edx, 46
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	jmp	.L2027
.L1999:
	mov	rax, QWORD PTR 56[rsp]
	cmp	rax, 15
	jbe	.L2000
.L2172:
	test	rax, rax
	js	.L2071
	cmp	rax, 29
	ja	.L2004
	mov	QWORD PTR 56[rsp], 30
.L2072:
	mov	rax, QWORD PTR 56[rsp]
	lea	rcx, 1[rax]
	jmp	.L2006
.L2099:
	mov	edx, 15
	jmp	.L2036
.L2204:
	mov	BYTE PTR [rcx], 48
	jmp	.L2041
.L2203:
	movzx	edx, BYTE PTR [rcx]
	mov	BYTE PTR [rax], dl
	mov	rcx, QWORD PTR 160[rsp]
	add	rcx, rsi
	jmp	.L2038
.L2207:
	movzx	eax, BYTE PTR 0[r13]
	mov	BYTE PTR [r10], al
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L2021
.L2210:
	mov	QWORD PTR 32[rsp], r15
	xor	r9d, r9d
	xor	r8d, r8d
	mov	rdx, r12
	lea	rsi, 160[rsp]
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE53:
	mov	rax, QWORD PTR 160[rsp]
	jmp	.L2032
.L2189:
	mov	rax, QWORD PTR [r14]
	mov	rcx, r14
.LEHB54:
	call	[QWORD PTR [rax]]
.LEHE54:
	jmp	.L2063
.L2198:
	cmp	r12, 29
	ja	.L2016
	lea	rsi, 160[rsp]
	mov	ecx, 31
.LEHB55:
	call	_Znwy
	mov	r14, r12
	mov	r10, rax
	mov	r12d, 30
	jmp	.L2017
.L2211:
	mov	BYTE PTR [rcx], 48
	jmp	.L2034
.L2098:
	mov	edx, 15
	jmp	.L2031
.L2206:
	mov	QWORD PTR 160[rsp], rax
	mov	rax, QWORD PTR 56[rsp]
	mov	r9, -1
	mov	QWORD PTR 176[rsp], rax
	jmp	.L2012
.L2178:
	movzx	eax, BYTE PTR 0[r13]
	mov	rsi, r12
	mov	r12d, 1
	mov	BYTE PTR [r10], al
	jmp	.L2025
.L2177:
	mov	QWORD PTR 56[rsp], rax
	jmp	.L2072
.L2199:
	lea	rcx, .LC7[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L1970:
	lea	rcx, .LC7[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2071:
	lea	rcx, .LC7[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2202:
	lea	rcx, .LC34[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2201:
	lea	rdx, .LC35[rip]
	mov	r8, rax
	lea	rcx, .LC36[rip]
	lea	rsi, 160[rsp]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L2009:
	lea	rcx, .LC33[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2209:
	lea	rcx, .LC34[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.LEHE55:
.L1940:
	xor	r14d, r14d
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L1948
.L2114:
	mov	rbx, rax
.L2070:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB56:
	call	_Unwind_Resume
.LEHE56:
.L2116:
	mov	rbx, rax
	jmp	.L2068
.L2115:
	mov	rcx, r14
	mov	rbx, rax
	call	_ZNSt6localeD1Ev
.L2068:
	lea	rcx, 192[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	cmp	BYTE PTR 152[rsp], 0
	je	.L2069
	lea	rcx, 144[rsp]
	call	_ZNSt6localeD1Ev
.L2069:
	lea	rsi, 160[rsp]
	jmp	.L2070
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5407:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5407-.LLSDACSB5407
.LLSDACSB5407:
	.uleb128 .LEHB48-.LFB5407
	.uleb128 .LEHE48-.LEHB48
	.uleb128 .L2114-.LFB5407
	.uleb128 0
	.uleb128 .LEHB49-.LFB5407
	.uleb128 .LEHE49-.LEHB49
	.uleb128 .L2115-.LFB5407
	.uleb128 0
	.uleb128 .LEHB50-.LFB5407
	.uleb128 .LEHE50-.LEHB50
	.uleb128 .L2116-.LFB5407
	.uleb128 0
	.uleb128 .LEHB51-.LFB5407
	.uleb128 .LEHE51-.LEHB51
	.uleb128 .L2114-.LFB5407
	.uleb128 0
	.uleb128 .LEHB52-.LFB5407
	.uleb128 .LEHE52-.LEHB52
	.uleb128 .L2116-.LFB5407
	.uleb128 0
	.uleb128 .LEHB53-.LFB5407
	.uleb128 .LEHE53-.LEHB53
	.uleb128 .L2114-.LFB5407
	.uleb128 0
	.uleb128 .LEHB54-.LFB5407
	.uleb128 .LEHE54-.LEHB54
	.uleb128 .L2116-.LFB5407
	.uleb128 0
	.uleb128 .LEHB55-.LFB5407
	.uleb128 .LEHE55-.LEHB55
	.uleb128 .L2114-.LFB5407
	.uleb128 0
	.uleb128 .LEHB56-.LFB5407
	.uleb128 .LEHE56-.LEHB56
	.uleb128 0
	.uleb128 0
.LLSDACSE5407:
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
.LFB5403:
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
	jne	.L2451
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L2232
	lea	rdx, .L2356[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2356:
	.long	.L2232-.L2356
	.long	.L2357-.L2356
	.long	.L2387-.L2356
	.long	.L2388-.L2356
	.long	.L2389-.L2356
	.long	.L2390-.L2356
	.long	.L2391-.L2356
	.long	.L2386-.L2356
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2232:
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
.L2231:
	mov	QWORD PTR 56[rsp], 6
	xor	r15d, r15d
	cmp	eax, 132
	je	.L2385
	lea	rax, 384[rsp]
	mov	QWORD PTR 64[rsp], rax
	lea	r13, 257[rsp]
.L2229:
	test	r12b, r12b
	je	.L2259
	cmp	r13, rsi
	mov	r12, QWORD PTR __imp_toupper[rip]
	mov	r14, r13
	je	.L2261
	.p2align 4,,10
	.p2align 3
.L2260:
	movsx	ecx, BYTE PTR [r14]
	add	r14, 1
	call	r12
	mov	BYTE PTR -1[r14], al
	cmp	rsi, r14
	jne	.L2260
.L2261:
	movsx	ecx, dil
	call	r12
	mov	edi, eax
.L2259:
	movd	eax, xmm6
	movzx	r9d, BYTE PTR [rbx]
	test	eax, eax
	js	.L2262
	mov	eax, r9d
	and	eax, 12
	cmp	al, 4
	je	.L2452
	cmp	al, 12
	jne	.L2262
	mov	BYTE PTR -1[r13], 32
	movzx	r9d, BYTE PTR [rbx]
	sub	r13, 1
	.p2align 4,,10
	.p2align 3
.L2262:
	mov	r12, rsi
	sub	r12, r13
	test	r9b, 16
	je	.L2264
	movss	xmm1, DWORD PTR .LC41[rip]
	movaps	xmm0, xmm6
	andps	xmm0, XMMWORD PTR .LC40[rip]
	ucomiss	xmm1, xmm0
	jb	.L2264
	test	r12, r12
	je	.L2368
	mov	r8, r12
	mov	edx, 46
	mov	rcx, r13
	mov	BYTE PTR 72[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	mov	r10, rax
	je	.L2266
	sub	r10, r13
	cmp	r10, -1
	je	.L2266
	lea	rax, 1[r10]
	mov	QWORD PTR 80[rsp], r12
	cmp	rax, r12
	jnb	.L2267
	mov	r8, r12
	movsx	edx, dil
	mov	QWORD PTR 88[rsp], r10
	lea	rcx, 0[r13+rax]
	sub	r8, rax
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	mov	r10, QWORD PTR 88[rsp]
	je	.L2267
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	mov	QWORD PTR 80[rsp], rax
.L2267:
	cmp	QWORD PTR 80[rsp], r10
	sete	BYTE PTR 88[rsp]
	sete	al
	test	r15b, r15b
	movzx	eax, al
	mov	QWORD PTR 72[rsp], rax
	jne	.L2268
	xor	r15d, r15d
.L2269:
	cmp	QWORD PTR 72[rsp], 0
	je	.L2264
.L2353:
	mov	r9, QWORD PTR 168[rsp]
	mov	rdx, QWORD PTR 72[rsp]
	test	r9, r9
	lea	rax, [r12+rdx]
	mov	QWORD PTR 56[rsp], rax
	jne	.L2271
	mov	rax, QWORD PTR 64[rsp]
	sub	rax, rsi
	cmp	rax, rdx
	jnb	.L2453
	cmp	QWORD PTR 160[rsp], rbp
	je	.L2454
	mov	rax, QWORD PTR 176[rsp]
	mov	rsi, QWORD PTR 56[rsp]
	cmp	rax, rsi
	jnb	.L2280
.L2279:
	cmp	QWORD PTR 56[rsp], 0
	js	.L2349
	add	rax, rax
	cmp	QWORD PTR 56[rsp], rax
	jnb	.L2282
	test	rax, rax
	jns	.L2455
.L2283:
	lea	rsi, 160[rsp]
.LEHB57:
	call	_ZSt17__throw_bad_allocv
.L2294:
	mov	rcx, r12
	mov	r14, r12
	add	rcx, 1
	js	.L2301
.L2302:
	lea	rsi, 160[rsp]
	call	_Znwy
.LEHE57:
	cmp	r14, 1
	mov	r10, rax
	je	.L2456
.L2295:
	mov	rcx, r10
	mov	r8, r14
	mov	rdx, r13
	call	memcpy
	mov	rsi, r12
	mov	r12, r14
	mov	r10, rax
.L2303:
	mov	rcx, QWORD PTR 160[rsp]
	cmp	rcx, rbp
	je	.L2304
	mov	rax, QWORD PTR 176[rsp]
	mov	QWORD PTR 56[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 56[rsp]
.L2304:
	mov	QWORD PTR 160[rsp], r10
	mov	QWORD PTR 176[rsp], rsi
.L2299:
	cmp	BYTE PTR 88[rsp], 0
	mov	QWORD PTR 168[rsp], r12
	mov	BYTE PTR [r10+r12], 0
	jne	.L2457
.L2305:
	test	r15, r15
	mov	r12, QWORD PTR 168[rsp]
	jne	.L2458
.L2307:
	mov	r13, QWORD PTR 160[rsp]
	movzx	r9d, BYTE PTR [rbx]
	.p2align 4,,10
	.p2align 3
.L2264:
	lea	rsi, 208[rsp]
	and	r9d, 32
	mov	QWORD PTR 144[rsp], 0
	mov	BYTE PTR 152[rsp], 0
	mov	QWORD PTR 192[rsp], rsi
	mov	QWORD PTR 200[rsp], 0
	mov	BYTE PTR 208[rsp], 0
	je	.L2378
	mov	rax, QWORD PTR 496[rsp]
	cmp	BYTE PTR 32[rax], 0
	lea	r15, 24[rax]
	je	.L2459
.L2322:
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
.LEHB58:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE58:
	mov	rax, QWORD PTR 224[rsp]
	lea	rdi, 240[rsp]
	mov	rcx, QWORD PTR 192[rsp]
	mov	r8, QWORD PTR 232[rsp]
	cmp	rax, rdi
	je	.L2460
	movq	xmm0, r8
	cmp	rcx, rsi
	movhps	xmm0, QWORD PTR 240[rsp]
	je	.L2461
	test	rcx, rcx
	mov	rdx, QWORD PTR 208[rsp]
	mov	QWORD PTR 192[rsp], rax
	movups	XMMWORD PTR 200[rsp], xmm0
	je	.L2330
	mov	QWORD PTR 224[rsp], rcx
	mov	QWORD PTR 240[rsp], rdx
.L2329:
	mov	QWORD PTR 232[rsp], 0
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 224[rsp]
	cmp	rcx, rdi
	je	.L2331
	mov	rax, QWORD PTR 240[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2331:
	mov	rcx, r14
	call	_ZNSt6localeD1Ev
	movzx	eax, WORD PTR [rbx]
	mov	r12, QWORD PTR 200[rsp]
	mov	rdi, QWORD PTR 192[rsp]
	and	ax, 384
	cmp	ax, 128
	je	.L2462
.L2332:
	cmp	ax, 256
	je	.L2334
	mov	rax, QWORD PTR 496[rsp]
	mov	r14, QWORD PTR 16[rax]
.L2338:
	lea	rdx, 96[rsp]
	mov	rcx, r14
	mov	QWORD PTR 96[rsp], r12
	mov	QWORD PTR 104[rsp], rdi
.LEHB59:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L2447:
	mov	rcx, QWORD PTR 192[rsp]
	mov	rbx, rax
	cmp	rcx, rsi
	je	.L2342
	mov	rax, QWORD PTR 208[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2342:
	cmp	BYTE PTR 152[rsp], 0
	jne	.L2463
.L2343:
	mov	rcx, QWORD PTR 160[rsp]
	cmp	rcx, rbp
	je	.L2407
	mov	rax, QWORD PTR 176[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	nop
.L2407:
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
.L2378:
	movzx	eax, WORD PTR [rbx]
	mov	rdi, r13
	and	ax, 384
	cmp	ax, 128
	jne	.L2332
.L2462:
	movzx	eax, WORD PTR 4[rbx]
.L2333:
	mov	rdx, QWORD PTR 496[rsp]
	cmp	r12, rax
	mov	r14, QWORD PTR 16[rdx]
	jnb	.L2338
	movzx	edx, BYTE PTR [rbx]
	sub	rax, r12
	movzx	ecx, BYTE PTR 8[rbx]
	mov	rbx, rax
	mov	r8d, edx
	and	r8d, 3
	movsx	eax, cl
	jne	.L2340
	and	edx, 64
	je	.L2380
	movss	xmm0, DWORD PTR .LC41[rip]
	andps	xmm6, XMMWORD PTR .LC40[rip]
	ucomiss	xmm0, xmm6
	jnb	.L2464
.L2380:
	mov	eax, 32
	mov	r8d, 2
.L2340:
	lea	rdx, 96[rsp]
	mov	DWORD PTR 32[rsp], eax
	mov	r9, rbx
	mov	rcx, r14
	mov	QWORD PTR 96[rsp], r12
	mov	QWORD PTR 104[rsp], rdi
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
.LEHE59:
	jmp	.L2447
	.p2align 4,,10
	.p2align 3
.L2451:
	cmp	dl, 2
	je	.L2465
	mov	QWORD PTR 56[rsp], -1
	cmp	dl, 4
	je	.L2466
.L2215:
	shr	al, 3
	and	eax, 15
	cmp	al, 7
	ja	.L2218
	lea	rdx, .L2220[rip]
	movzx	eax, al
	movsx	rax, DWORD PTR [rdx+rax*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2220:
	.long	.L2227-.L2220
	.long	.L2359-.L2220
	.long	.L2225-.L2220
	.long	.L2224-.L2220
	.long	.L2441-.L2220
	.long	.L2443-.L2220
	.long	.L2221-.L2220
	.long	.L2442-.L2220
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2463:
	lea	rcx, 144[rsp]
	call	_ZNSt6localeD1Ev
	jmp	.L2343
	.p2align 4,,10
	.p2align 3
.L2387:
	mov	r12d, 1
.L2230:
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
	jmp	.L2231
	.p2align 4,,10
	.p2align 3
.L2464:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	eax, 48
	mov	r8d, 2
	cmp	BYTE PTR [rcx+rdx], 15
	jbe	.L2340
	mov	rax, QWORD PTR 24[r14]
	movzx	edx, BYTE PTR [rdi]
	lea	rcx, 1[rax]
	mov	QWORD PTR 24[r14], rcx
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[r14]
	sub	rax, QWORD PTR 8[r14]
	cmp	rax, QWORD PTR 16[r14]
	je	.L2467
.L2341:
	add	rdi, 1
	sub	r12, 1
	mov	eax, 48
	mov	r8d, 2
	jmp	.L2340
	.p2align 4,,10
	.p2align 3
.L2368:
	xor	eax, eax
.L2265:
	test	r15b, r15b
	je	.L2468
	mov	BYTE PTR 88[rsp], r15b
	mov	QWORD PTR 80[rsp], rax
	mov	QWORD PTR 72[rsp], 1
	jmp	.L2352
	.p2align 4,,10
	.p2align 3
.L2388:
	mov	QWORD PTR 56[rsp], 6
.L2224:
	xor	r12d, r12d
.L2223:
	mov	r14d, 1
	mov	edi, 101
	xor	r15d, r15d
.L2226:
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
	je	.L2228
	lea	rax, 384[rsp]
	mov	r13, QWORD PTR 72[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L2229
	.p2align 4,,10
	.p2align 3
.L2389:
	mov	QWORD PTR 56[rsp], 6
.L2441:
	mov	r12d, 1
	jmp	.L2223
	.p2align 4,,10
	.p2align 3
.L2390:
	mov	QWORD PTR 56[rsp], 6
.L2443:
	mov	r14d, 2
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L2226
	.p2align 4,,10
	.p2align 3
.L2386:
	mov	QWORD PTR 56[rsp], 6
.L2442:
	mov	r12d, 1
.L2219:
	mov	r14d, 3
	mov	edi, 101
	mov	r15d, 1
	jmp	.L2226
	.p2align 4,,10
	.p2align 3
.L2391:
	mov	QWORD PTR 56[rsp], 6
.L2221:
	xor	r12d, r12d
	jmp	.L2219
	.p2align 4,,10
	.p2align 3
.L2357:
	xor	r12d, r12d
	jmp	.L2230
	.p2align 4,,10
	.p2align 3
.L2466:
	mov	rdi, QWORD PTR 496[rsp]
	mov	BYTE PTR 208[rsp], 0
	movzx	eax, WORD PTR 6[rcx]
	movzx	edx, BYTE PTR [rdi]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L2469
	test	cl, cl
	jne	.L2217
	mov	rdi, QWORD PTR 496[rsp]
	mov	rdi, QWORD PTR [rdi]
	mov	rdx, rdi
	mov	QWORD PTR 56[rsp], rdi
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L2217
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
.L2217:
	lea	rcx, 192[rsp]
	lea	rsi, 160[rsp]
.LEHB60:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE60:
	mov	QWORD PTR 56[rsp], rax
	movzx	eax, BYTE PTR 1[rbx]
	jmp	.L2215
	.p2align 4,,10
	.p2align 3
.L2452:
	mov	BYTE PTR -1[r13], 43
	sub	r13, 1
	movzx	r9d, BYTE PTR [rbx]
	jmp	.L2262
	.p2align 4,,10
	.p2align 3
.L2459:
	mov	rcx, r15
	call	_ZNSt6localeC1Ev
	mov	rax, QWORD PTR 496[rsp]
	mov	BYTE PTR 32[rax], 1
	jmp	.L2322
	.p2align 4,,10
	.p2align 3
.L2334:
	mov	rdx, QWORD PTR 496[rsp]
	mov	BYTE PTR 240[rsp], 0
	movzx	eax, WORD PTR 4[rbx]
	movzx	edx, BYTE PTR [rdx]
	mov	ecx, edx
	and	edx, 15
	and	ecx, 15
	cmp	rax, rdx
	jb	.L2470
	test	cl, cl
	jne	.L2337
	mov	rdx, QWORD PTR 496[rsp]
	mov	rdx, QWORD PTR [rdx]
	mov	QWORD PTR 56[rsp], rdx
	shr	rdx, 4
	cmp	rax, rdx
	jnb	.L2337
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
.L2337:
	lea	rcx, 224[rsp]
.LEHB61:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE61:
	jmp	.L2333
	.p2align 4,,10
	.p2align 3
.L2461:
	mov	QWORD PTR 192[rsp], rax
	movups	XMMWORD PTR 200[rsp], xmm0
.L2330:
	mov	QWORD PTR 224[rsp], rdi
	lea	rdi, 240[rsp]
	mov	rcx, rdi
	jmp	.L2329
	.p2align 4,,10
	.p2align 3
.L2465:
	movzx	edi, WORD PTR 6[rcx]
	mov	QWORD PTR 56[rsp], rdi
	jmp	.L2215
	.p2align 4,,10
	.p2align 3
.L2460:
	test	r8, r8
	je	.L2325
	cmp	r8, 1
	je	.L2471
	mov	rdx, rdi
	call	memcpy
	mov	r8, QWORD PTR 232[rsp]
	mov	rcx, QWORD PTR 192[rsp]
.L2325:
	mov	QWORD PTR 200[rsp], r8
	mov	BYTE PTR [rcx+r8], 0
	mov	rcx, QWORD PTR 224[rsp]
	jmp	.L2329
	.p2align 4,,10
	.p2align 3
.L2268:
	mov	rax, QWORD PTR 80[rsp]
	sub	rax, 1
.L2352:
	movzx	edx, BYTE PTR 0[r13]
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	r15, QWORD PTR 56[rsp]
	cmp	BYTE PTR [rcx+rdx], 16
	adc	rax, -1
	sub	r15, rax
	add	QWORD PTR 72[rsp], r15
	jmp	.L2269
	.p2align 4,,10
	.p2align 3
.L2385:
	mov	BYTE PTR 72[rsp], 0
	mov	QWORD PTR 64[rsp], 134
.L2233:
	mov	r9, QWORD PTR 160[rsp]
	cmp	r9, rbp
	je	.L2365
	mov	rax, QWORD PTR 176[rsp]
.L2235:
	mov	rsi, QWORD PTR 64[rsp]
	cmp	rax, rsi
	jb	.L2472
.L2258:
	cmp	r9, rbp
	je	.L2366
	mov	rax, QWORD PTR 176[rsp]
	lea	rsi, [rax+rax]
	cmp	rax, rsi
	mov	QWORD PTR 64[rsp], rsi
	jb	.L2473
.L2247:
	mov	rax, QWORD PTR 64[rsp]
	lea	rdx, 1[r9]
	mov	QWORD PTR 64[rsp], r9
	cmp	BYTE PTR 72[rsp], 0
	lea	r8, -1[r9+rax]
	jne	.L2474
	test	r14d, r14d
	jne	.L2475
	movaps	xmm3, xmm6
	mov	rcx, r13
	call	_ZSt8to_charsPcS_f
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
.L2255:
	test	eax, eax
	jne	.L2257
	mov	rdx, QWORD PTR 160[rsp]
	mov	rax, rsi
	sub	rax, r9
	mov	QWORD PTR 168[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rax, QWORD PTR 160[rsp]
	lea	r13, 1[rax]
	add	rax, QWORD PTR 168[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L2229
	.p2align 4,,10
	.p2align 3
.L2266:
	movsx	edx, dil
	mov	r8, r12
	mov	rcx, r13
	mov	BYTE PTR 72[rsp], r9b
	call	memchr
	movzx	r9d, BYTE PTR 72[rsp]
	test	rax, rax
	je	.L2372
	sub	rax, r13
	cmp	rax, -1
	cmove	rax, r12
	jmp	.L2265
.L2359:
	mov	r14d, 4
	mov	edi, 112
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L2226
.L2225:
	mov	r14d, 4
	mov	edi, 112
	xor	r15d, r15d
	mov	r12d, 1
	jmp	.L2226
.L2227:
	mov	r14d, 3
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L2226
.L2468:
	mov	QWORD PTR 80[rsp], rax
	xor	r15d, r15d
	mov	QWORD PTR 72[rsp], 1
	mov	BYTE PTR 88[rsp], 1
	jmp	.L2353
.L2475:
	mov	DWORD PTR 32[rsp], r14d
	movaps	xmm3, xmm6
	mov	rcx, r13
	call	_ZSt8to_charsPcS_fSt12chars_format
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
	jmp	.L2255
.L2469:
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
	jmp	.L2217
.L2372:
	mov	rax, r12
	jmp	.L2265
.L2454:
	mov	rax, QWORD PTR 56[rsp]
	cmp	rax, 15
	ja	.L2450
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L2287
	mov	r10, rbp
.L2354:
	cmp	r12, 15
	ja	.L2476
.L2293:
	cmp	r13, r10
	jb	.L2297
	cmp	r10, r13
	jb	.L2297
	xor	eax, eax
	mov	QWORD PTR 32[rsp], r12
	mov	r9, r13
	xor	r8d, r8d
	lea	rsi, 160[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	rdx, r10
	mov	rcx, rsi
.LEHB62:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L2299
	.p2align 4,,10
	.p2align 3
.L2257:
	mov	rdx, QWORD PTR 160[rsp]
	cmp	eax, 132
	mov	QWORD PTR 168[rsp], 0
	mov	BYTE PTR [rdx], 0
	mov	r9, QWORD PTR 160[rsp]
	mov	rdx, QWORD PTR 168[rsp]
	je	.L2258
	lea	rax, [r9+rdx]
	lea	r13, 1[r9]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L2229
	.p2align 4,,10
	.p2align 3
.L2472:
	test	rsi, rsi
	js	.L2477
	add	rax, rax
	cmp	QWORD PTR 64[rsp], rax
	jnb	.L2238
	test	rax, rax
	js	.L2239
	lea	rcx, 1[rax]
	mov	QWORD PTR 64[rsp], rax
.L2240:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r9, rax
	mov	rax, QWORD PTR 168[rsp]
	mov	rsi, QWORD PTR 160[rsp]
	lea	r8, 1[rax]
	test	rax, rax
	je	.L2478
	test	r8, r8
	je	.L2444
	mov	rcx, r9
	mov	rdx, rsi
	call	memcpy
	mov	r9, rax
.L2444:
	cmp	rsi, rbp
	je	.L2243
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 80[rsp]
.L2243:
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 160[rsp], r9
	mov	QWORD PTR 176[rsp], rax
	jmp	.L2258
.L2470:
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
	jmp	.L2337
.L2271:
	cmp	QWORD PTR 160[rsp], rbp
	je	.L2277
	mov	rax, QWORD PTR 176[rsp]
	mov	rsi, QWORD PTR 56[rsp]
	cmp	rax, rsi
	jb	.L2279
.L2278:
	mov	rax, QWORD PTR 80[rsp]
	cmp	r9, rax
	jb	.L2479
.L2290:
	movabs	rax, 9223372036854775807
	mov	rsi, QWORD PTR 72[rsp]
	sub	rax, r9
	cmp	rax, rsi
	jb	.L2480
	mov	rax, QWORD PTR 72[rsp]
	lea	r12, [r9+rax]
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, rbp
	je	.L2377
	mov	rdx, QWORD PTR 176[rsp]
.L2314:
	cmp	rdx, r12
	jb	.L2315
	mov	rsi, QWORD PTR 80[rsp]
	lea	rcx, [rax+rsi]
	sub	r9, rsi
	je	.L2316
	mov	rax, QWORD PTR 72[rsp]
	add	rax, rcx
	cmp	r9, 1
	je	.L2481
	mov	rdx, rcx
	mov	r8, r9
	mov	rcx, rax
	call	memmove
	mov	rcx, QWORD PTR 80[rsp]
	add	rcx, QWORD PTR 160[rsp]
.L2316:
	cmp	QWORD PTR 72[rsp], 1
	je	.L2482
	mov	r8, QWORD PTR 72[rsp]
	mov	edx, 48
	call	memset
.L2319:
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 168[rsp], r12
	cmp	BYTE PTR 88[rsp], 0
	mov	BYTE PTR [rax+r12], 0
	mov	r12, QWORD PTR 168[rsp]
	je	.L2307
	mov	rax, QWORD PTR 160[rsp]
	mov	rsi, QWORD PTR 80[rsp]
	mov	BYTE PTR [rax+rsi], 46
	mov	r12, QWORD PTR 168[rsp]
	jmp	.L2307
.L2282:
	mov	rcx, QWORD PTR 56[rsp]
	add	rcx, 1
	js	.L2283
.L2284:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r9, QWORD PTR 168[rsp]
	mov	rsi, rax
	mov	r14, QWORD PTR 160[rsp]
	lea	r8, 1[r9]
	test	r9, r9
	je	.L2483
	test	r8, r8
	jne	.L2289
	cmp	r14, rbp
	je	.L2484
.L2286:
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, r14
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 168[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	rax, QWORD PTR 56[rsp]
	test	r9, r9
	mov	QWORD PTR 176[rsp], rax
	jne	.L2278
.L2280:
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L2287
	mov	r10, QWORD PTR 160[rsp]
	cmp	r10, rbp
	je	.L2354
.L2292:
	mov	rax, QWORD PTR 176[rsp]
	cmp	rax, r12
	jnb	.L2293
	add	rax, rax
	cmp	r12, rax
	jnb	.L2294
	lea	rcx, 1[rax]
	test	rax, rax
	mov	r14, r12
	mov	r12, rax
	jns	.L2302
.L2301:
	lea	rsi, 160[rsp]
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L2238:
	mov	rcx, QWORD PTR 64[rsp]
	add	rcx, 1
	jns	.L2240
.L2239:
	lea	rsi, 160[rsp]
	call	_ZSt17__throw_bad_allocv
.L2474:
	mov	eax, DWORD PTR 56[rsp]
	mov	DWORD PTR 32[rsp], r14d
	movaps	xmm3, xmm6
	mov	rcx, r13
	mov	DWORD PTR 40[rsp], eax
	call	_ZSt8to_charsPcS_fSt12chars_formati
	mov	rsi, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 64[rsp]
	jmp	.L2255
.L2228:
	mov	rax, QWORD PTR 56[rsp]
	cmp	r14d, 2
	mov	BYTE PTR 72[rsp], 1
	lea	rsi, 128[rax]
	mov	QWORD PTR 64[rsp], rsi
	jne	.L2233
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
	jmp	.L2233
.L2297:
	test	r12, r12
	je	.L2299
	cmp	r12, 1
	je	.L2485
	mov	rcx, r10
	mov	r8, r12
	mov	rdx, r13
	call	memcpy
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L2299
.L2453:
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
	je	.L2274
	mov	rax, QWORD PTR 80[rsp]
	mov	BYTE PTR [rsi], 46
	lea	rsi, 1[r13+rax]
.L2274:
	mov	r8, r15
	mov	edx, 48
	mov	rcx, rsi
	call	memset
	movzx	r9d, BYTE PTR [rbx]
	mov	r12, QWORD PTR 56[rsp]
	jmp	.L2264
.L2366:
	mov	QWORD PTR 64[rsp], 30
	mov	ecx, 31
.L2246:
	lea	rsi, 160[rsp]
	call	_Znwy
	mov	r8, QWORD PTR 168[rsp]
	mov	r9, rax
	mov	rsi, QWORD PTR 160[rsp]
	cmp	r8, 1
	je	.L2486
	test	r8, r8
	je	.L2446
	mov	rdx, rsi
	mov	rcx, rax
	call	memcpy
	mov	r9, rax
.L2446:
	cmp	rsi, rbp
	je	.L2251
	mov	rax, QWORD PTR 176[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 80[rsp]
.L2251:
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 160[rsp], r9
	mov	QWORD PTR 176[rsp], rax
	jmp	.L2247
.L2365:
	mov	eax, 15
	jmp	.L2235
.L2473:
	test	rsi, rsi
	js	.L2248
	lea	rcx, 1[rsi]
	jmp	.L2246
.L2315:
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
	jmp	.L2316
.L2478:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r9], al
	jmp	.L2444
.L2483:
	movzx	eax, BYTE PTR [r14]
	cmp	r14, rbp
	mov	BYTE PTR [rsi], al
	jne	.L2286
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	QWORD PTR 176[rsp], rax
	mov	rax, QWORD PTR 80[rsp]
	cmp	r12, rax
	cmova	r12, rax
	test	r12, r12
	js	.L2287
	mov	r10, rsi
	jmp	.L2292
.L2458:
	movabs	rax, 9223372036854775807
	sub	rax, r12
	cmp	rax, r15
	jb	.L2487
	mov	rax, QWORD PTR 160[rsp]
	lea	r13, [r12+r15]
	cmp	rax, rbp
	je	.L2376
	mov	rdx, QWORD PTR 176[rsp]
.L2309:
	cmp	rdx, r13
	jb	.L2488
.L2310:
	lea	rcx, [rax+r12]
	cmp	r15, 1
	je	.L2489
	mov	r8, r15
	mov	edx, 48
	call	memset
.L2312:
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 168[rsp], r13
	mov	BYTE PTR [rax+r13], 0
	mov	r12, QWORD PTR 168[rsp]
	jmp	.L2307
.L2289:
	mov	rdx, r14
	mov	rcx, rax
	mov	QWORD PTR 64[rsp], r9
	call	memcpy
	cmp	r14, rbp
	mov	r9, QWORD PTR 64[rsp]
	jne	.L2286
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 160[rsp], rsi
	mov	QWORD PTR 176[rsp], rax
	jmp	.L2278
.L2471:
	movzx	eax, BYTE PTR 240[rsp]
	mov	BYTE PTR [rcx], al
	mov	r8, QWORD PTR 232[rsp]
	mov	rcx, QWORD PTR 192[rsp]
	jmp	.L2325
.L2486:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR [r9], al
	jmp	.L2446
.L2457:
	lea	rsi, 160[rsp]
	mov	edx, 46
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	jmp	.L2305
.L2277:
	mov	rax, QWORD PTR 56[rsp]
	cmp	rax, 15
	jbe	.L2278
.L2450:
	test	rax, rax
	js	.L2349
	cmp	rax, 29
	ja	.L2282
	mov	QWORD PTR 56[rsp], 30
.L2350:
	mov	rax, QWORD PTR 56[rsp]
	lea	rcx, 1[rax]
	jmp	.L2284
.L2377:
	mov	edx, 15
	jmp	.L2314
.L2482:
	mov	BYTE PTR [rcx], 48
	jmp	.L2319
.L2481:
	movzx	edx, BYTE PTR [rcx]
	mov	BYTE PTR [rax], dl
	mov	rcx, QWORD PTR 160[rsp]
	add	rcx, rsi
	jmp	.L2316
.L2485:
	movzx	eax, BYTE PTR 0[r13]
	mov	BYTE PTR [r10], al
	mov	r10, QWORD PTR 160[rsp]
	jmp	.L2299
.L2488:
	mov	QWORD PTR 32[rsp], r15
	xor	r9d, r9d
	xor	r8d, r8d
	mov	rdx, r12
	lea	rsi, 160[rsp]
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE62:
	mov	rax, QWORD PTR 160[rsp]
	jmp	.L2310
.L2467:
	mov	rax, QWORD PTR [r14]
	mov	rcx, r14
.LEHB63:
	call	[QWORD PTR [rax]]
.LEHE63:
	jmp	.L2341
.L2476:
	cmp	r12, 29
	ja	.L2294
	lea	rsi, 160[rsp]
	mov	ecx, 31
.LEHB64:
	call	_Znwy
	mov	r14, r12
	mov	r10, rax
	mov	r12d, 30
	jmp	.L2295
.L2489:
	mov	BYTE PTR [rcx], 48
	jmp	.L2312
.L2376:
	mov	edx, 15
	jmp	.L2309
.L2484:
	mov	QWORD PTR 160[rsp], rax
	mov	rax, QWORD PTR 56[rsp]
	mov	r9, -1
	mov	QWORD PTR 176[rsp], rax
	jmp	.L2290
.L2456:
	movzx	eax, BYTE PTR 0[r13]
	mov	rsi, r12
	mov	r12d, 1
	mov	BYTE PTR [r10], al
	jmp	.L2303
.L2455:
	mov	QWORD PTR 56[rsp], rax
	jmp	.L2350
.L2477:
	lea	rcx, .LC7[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2248:
	lea	rcx, .LC7[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2349:
	lea	rcx, .LC7[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2480:
	lea	rcx, .LC34[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2479:
	lea	rdx, .LC35[rip]
	mov	r8, rax
	lea	rcx, .LC36[rip]
	lea	rsi, 160[rsp]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L2287:
	lea	rcx, .LC33[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.L2487:
	lea	rcx, .LC34[rip]
	lea	rsi, 160[rsp]
	call	_ZSt20__throw_length_errorPKc
.LEHE64:
.L2218:
	xor	r14d, r14d
	xor	edi, edi
	xor	r15d, r15d
	xor	r12d, r12d
	jmp	.L2226
.L2392:
	mov	rbx, rax
.L2348:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB65:
	call	_Unwind_Resume
.LEHE65:
.L2394:
	mov	rbx, rax
	jmp	.L2346
.L2393:
	mov	rcx, r14
	mov	rbx, rax
	call	_ZNSt6localeD1Ev
.L2346:
	lea	rcx, 192[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	cmp	BYTE PTR 152[rsp], 0
	je	.L2347
	lea	rcx, 144[rsp]
	call	_ZNSt6localeD1Ev
.L2347:
	lea	rsi, 160[rsp]
	jmp	.L2348
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5403:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5403-.LLSDACSB5403
.LLSDACSB5403:
	.uleb128 .LEHB57-.LFB5403
	.uleb128 .LEHE57-.LEHB57
	.uleb128 .L2392-.LFB5403
	.uleb128 0
	.uleb128 .LEHB58-.LFB5403
	.uleb128 .LEHE58-.LEHB58
	.uleb128 .L2393-.LFB5403
	.uleb128 0
	.uleb128 .LEHB59-.LFB5403
	.uleb128 .LEHE59-.LEHB59
	.uleb128 .L2394-.LFB5403
	.uleb128 0
	.uleb128 .LEHB60-.LFB5403
	.uleb128 .LEHE60-.LEHB60
	.uleb128 .L2392-.LFB5403
	.uleb128 0
	.uleb128 .LEHB61-.LFB5403
	.uleb128 .LEHE61-.LEHB61
	.uleb128 .L2394-.LFB5403
	.uleb128 0
	.uleb128 .LEHB62-.LFB5403
	.uleb128 .LEHE62-.LEHB62
	.uleb128 .L2392-.LFB5403
	.uleb128 0
	.uleb128 .LEHB63-.LFB5403
	.uleb128 .LEHE63-.LEHB63
	.uleb128 .L2394-.LFB5403
	.uleb128 0
	.uleb128 .LEHB64-.LFB5403
	.uleb128 .LEHE64-.LEHB64
	.uleb128 .L2392-.LFB5403
	.uleb128 0
	.uleb128 .LEHB65-.LFB5403
	.uleb128 .LEHE65-.LEHB65
	.uleb128 0
	.uleb128 0
.LLSDACSE5403:
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC42:
	.ascii "format error: format-spec contains invalid formatting options for 'bool'\0"
	.align 8
.LC43:
	.ascii "format error: format-spec contains invalid formatting options for 'charT'\0"
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
	.def	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE:
.LFB5172:
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
	lea	rdx, .L2493[rip]
	movsx	rax, DWORD PTR [rdx+r8*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2493:
	.long	.L2508-.L2493
	.long	.L2507-.L2493
	.long	.L2506-.L2493
	.long	.L2505-.L2493
	.long	.L2504-.L2493
	.long	.L2503-.L2493
	.long	.L2502-.L2493
	.long	.L2501-.L2493
	.long	.L2500-.L2493
	.long	.L2499-.L2493
	.long	.L2498-.L2493
	.long	.L2497-.L2493
	.long	.L2496-.L2493
	.long	.L2495-.L2493
	.long	.L2494-.L2493
	.long	.L2492-.L2493
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2494:
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
.L2490:
	add	rsp, 168
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L2492:
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
.L2528:
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 168
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L2507:
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
	jne	.L2509
	test	BYTE PTR 128[rsp], 92
	jne	.L2530
.L2509:
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rdi
	movzx	edx, BYTE PTR [rsi]
	mov	rbx, QWORD PTR 48[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L2490
	.p2align 4,,10
	.p2align 3
.L2506:
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
	jne	.L2511
	test	BYTE PTR 128[rsp], 92
	jne	.L2531
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	cmp	cl, 120
	mov	rbx, QWORD PTR 48[rax]
	jne	.L2532
	mov	rax, QWORD PTR 16[rbx]
	jmp	.L2528
	.p2align 4,,10
	.p2align 3
.L2504:
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
	jmp	.L2490
	.p2align 4,,10
	.p2align 3
.L2503:
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
	jmp	.L2490
	.p2align 4,,10
	.p2align 3
.L2505:
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
	jmp	.L2490
	.p2align 4,,10
	.p2align 3
.L2502:
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
	jmp	.L2490
	.p2align 4,,10
	.p2align 3
.L2501:
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
	jmp	.L2490
	.p2align 4,,10
	.p2align 3
.L2500:
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
	jmp	.L2490
	.p2align 4,,10
	.p2align 3
.L2499:
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
	jmp	.L2490
	.p2align 4,,10
	.p2align 3
.L2498:
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
.L2529:
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
.L2497:
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
	jmp	.L2529
	.p2align 4,,10
	.p2align 3
.L2496:
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
	jne	.L2517
	mov	BYTE PTR 130[rsp], 48
	mov	edx, 3
.L2518:
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
	jmp	.L2490
	.p2align 4,,10
	.p2align 3
.L2495:
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
.L2517:
	movabs	rsi, 3978425819141910832
	bsr	rdx, rax
	lea	r8d, 4[rdx]
	mov	QWORD PTR 112[rsp], rsi
	movabs	rsi, 7378413942531504440
	shr	r8d, 2
	cmp	rax, 255
	mov	QWORD PTR 120[rsp], rsi
	lea	edx, -1[r8]
	jbe	.L2519
	.p2align 4,,10
	.p2align 3
.L2520:
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
	ja	.L2520
.L2519:
	cmp	rax, 15
	jbe	.L2521
	mov	rdx, rax
	shr	rax, 4
	and	edx, 15
	movzx	edx, BYTE PTR 112[rsp+rdx]
	mov	BYTE PTR 131[rsp], dl
	movzx	eax, BYTE PTR 112[rsp+rax]
.L2522:
	mov	BYTE PTR 130[rsp], al
	lea	edx, 2[r8]
	jmp	.L2518
	.p2align 4,,10
	.p2align 3
.L2511:
	mov	QWORD PTR 8[rbp], rax
	mov	rax, QWORD PTR [rbx]
	test	cl, cl
	movsx	edx, BYTE PTR [rsi]
	mov	rbx, QWORD PTR 48[rax]
	jne	.L2515
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
	jmp	.L2528
.L2532:
	movsx	edx, BYTE PTR [rsi]
.L2515:
	mov	r8, rbx
	mov	rcx, rdi
	call	_ZNKSt8__format15__formatter_intIcE6formatIcNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	jmp	.L2528
	.p2align 4,,10
	.p2align 3
.L2521:
	movzx	eax, BYTE PTR 112[rsp+rax]
	jmp	.L2522
.L2531:
	lea	rcx, .LC43[rip]
	call	_ZSt20__throw_format_errorPKc
.L2508:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
.L2530:
	lea	rcx, .LC42[rip]
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
.LFB5169:
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
	jb	.L2537
	test	r8b, r8b
	je	.L2538
	xor	r8d, r8d
.L2535:
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
.L2538:
	mov	rcx, QWORD PTR [r9]
	shr	rcx, 4
	cmp	rdx, rcx
	jnb	.L2535
	sal	rdx, 5
	add	rdx, QWORD PTR 8[r9]
	mov	rcx, QWORD PTR [rdx]
	movzx	r8d, BYTE PTR 16[rdx]
	mov	QWORD PTR 48[rsp], rcx
	mov	rcx, QWORD PTR 8[rdx]
	mov	QWORD PTR 56[rsp], rcx
	jmp	.L2535
	.p2align 4,,10
	.p2align 3
.L2537:
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
	jmp	.L2535
	.seh_endproc
	.section .rdata,"dr"
	.align 32
CSWTCH.554:
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
.LC9:
	.quad	0
	.quad	-1
	.align 16
.LC32:
	.long	-1
	.long	-1
	.long	32766
	.long	0
	.align 16
.LC38:
	.long	-1
	.long	2147483647
	.long	0
	.long	0
	.align 8
.LC39:
	.long	-1
	.long	2146435071
	.align 16
.LC40:
	.long	2147483647
	.long	0
	.long	0
	.long	0
	.align 4
.LC41:
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
	.def	_ZNSt7__cxx1119basic_ostringstreamIcSt11char_traitsIcESaIcEEC1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZNKRSt7__cxx1115basic_stringbufIcSt11char_traitsIcESaIcEE3strEv;	.scl	2;	.type	32;	.endef
	.def	memcmp;	.scl	2;	.type	32;	.endef
	.def	_ZNSt14basic_ofstreamIcSt11char_traitsIcEEC1EPKcSt13_Ios_Openmode;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSt14basic_ofstreamIcSt11char_traitsIcEED1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZNSt14basic_ifstreamIcSt11char_traitsIcEEC1EPKcSt13_Ios_Openmode;	.scl	2;	.type	32;	.endef
	.def	_ZNSi3getERc;	.scl	2;	.type	32;	.endef
	.def	_ZNSt14basic_ifstreamIcSt11char_traitsIcEED1Ev;	.scl	2;	.type	32;	.endef
	.def	remove;	.scl	2;	.type	32;	.endef
	.def	_ZNSt7__cxx1119basic_ostringstreamIcSt11char_traitsIcESaIcEED1Ev;	.scl	2;	.type	32;	.endef
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
