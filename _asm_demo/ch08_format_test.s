	.file	"ch08_format_test.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt8__format5_SinkIcE10_M_reserveEy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format5_SinkIcE10_M_reserveEy
	.def	_ZNSt8__format5_SinkIcE10_M_reserveEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format5_SinkIcE10_M_reserveEy
_ZNSt8__format5_SinkIcE10_M_reserveEy:
.LFB4761:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	r8, QWORD PTR 16[rcx]
	mov	r9, r8
	mov	rax, rcx
	mov	rcx, QWORD PTR 24[rcx]
	sub	rcx, QWORD PTR 8[rax]
	sub	r9, rcx
	cmp	r9, rdx
	jnb	.L3
	cmp	r8, rdx
	jb	.L4
	mov	r8, QWORD PTR [rax]
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], rax
	mov	QWORD PTR 56[rsp], rdx
	call	[QWORD PTR [r8]]
	mov	rax, QWORD PTR 48[rsp]
	mov	rcx, QWORD PTR 16[rax]
	mov	r8, QWORD PTR 24[rax]
	sub	r8, QWORD PTR 8[rax]
	sub	rcx, r8
	cmp	rcx, QWORD PTR 56[rsp]
	jb	.L4
.L3:
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text$_ZNSt8__format5_SinkIcE7_M_bumpEy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format5_SinkIcE7_M_bumpEy
	.def	_ZNSt8__format5_SinkIcE7_M_bumpEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format5_SinkIcE7_M_bumpEy
_ZNSt8__format5_SinkIcE7_M_bumpEy:
.LFB4948:
	.seh_endprologue
	add	QWORD PTR 24[rcx], rdx
	ret
	.seh_endproc
	.section	.text$_ZNSt8__format14_Fixedbuf_sinkIcE11_M_overflowEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format14_Fixedbuf_sinkIcE11_M_overflowEv
	.def	_ZNSt8__format14_Fixedbuf_sinkIcE11_M_overflowEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14_Fixedbuf_sinkIcE11_M_overflowEv
_ZNSt8__format14_Fixedbuf_sinkIcE11_M_overflowEv:
.LFB6101:
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	QWORD PTR 24[rcx], rax
	ret
	.seh_endproc
	.section	.text$_ZNSt12format_errorD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12format_errorD1Ev
	.def	_ZNSt12format_errorD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12format_errorD1Ev
_ZNSt12format_errorD1Ev:
.LFB3559:
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
.LFB3560:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rax, _ZTVSt12format_error[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 40[rsp], rcx
	call	_ZNSt13runtime_errorD2Ev
	mov	rcx, QWORD PTR 40[rsp]
	mov	edx, 16
	add	rsp, 56
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc
	.def	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc
_ZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE11_M_on_charsEPKc:
.LFB5258:
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
	mov	rbp, QWORD PTR 8[rcx]
	mov	r12, QWORD PTR 56[rcx]
	mov	rsi, QWORD PTR 16[r12]
	sub	rdx, rbp
	mov	rdi, rdx
	jne	.L26
.L12:
	mov	QWORD PTR 16[r12], rsi
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L26:
	mov	rcx, QWORD PTR 24[rsi]
	mov	rbx, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	rbx, rax
	cmp	rdx, rbx
	jb	.L13
	.p2align 4
	.p2align 3
.L15:
	test	rbx, rbx
	je	.L14
	mov	r8, rbx
	mov	rdx, rbp
	call	memcpy
.L14:
	mov	rax, QWORD PTR [rsi]
	add	QWORD PTR 24[rsi], rbx
	mov	rcx, rsi
	add	rbp, rbx
	sub	rdi, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rsi]
	mov	rbx, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	rbx, rax
	cmp	rdi, rbx
	jnb	.L15
	test	rdi, rdi
	je	.L12
.L13:
	mov	r8, rdi
	mov	rdx, rbp
	call	memcpy
	add	QWORD PTR 24[rsi], rdi
	mov	QWORD PTR 16[r12], rsi
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.seh_endproc
	.section	.text$_ZSt20__throw_format_errorPKc,"x"
	.linkonce discard
	.globl	_ZSt20__throw_format_errorPKc
	.def	_ZSt20__throw_format_errorPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt20__throw_format_errorPKc
_ZSt20__throw_format_errorPKc:
.LFB3556:
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
	lea	r8, _ZNSt12format_errorD1Ev[rip]
	mov	rcx, rbx
	mov	QWORD PTR [rbx], rax
	lea	rdx, _ZTISt12format_error[rip]
.LEHB1:
	call	__cxa_throw
.L29:
	mov	rsi, rax
.L28:
	mov	rcx, rbx
	call	__cxa_free_exception
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3556:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3556-.LLSDACSB3556
.LLSDACSB3556:
	.uleb128 .LEHB0-.LFB3556
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L29-.LFB3556
	.uleb128 0
	.uleb128 .LEHB1-.LFB3556
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE3556:
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
.LFB3563:
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
.LFB3564:
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
	.ascii "format error: argument used for width or precision must be a non-negative integer\0"
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB3:
	.text
.LHOTB3:
	.align 2
	.p2align 4
	.def	_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0
_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0:
.LFB6138:
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	movzx	eax, cx
	movzx	ecx, BYTE PTR [rdx]
	mov	r8, rcx
	and	r8d, 15
	cmp	rax, r8
	jnb	.L33
	mov	r8, QWORD PTR [rdx]
	lea	rcx, [rax+rax*4]
	sal	rax, 4
	add	rax, QWORD PTR 8[rdx]
	movdqa	xmm1, XMMWORD PTR [rax]
	shr	r8, 4
	shr	r8, cl
	movaps	XMMWORD PTR 32[rsp], xmm1
	mov	rcx, r8
	and	ecx, 31
.L34:
	lea	rdx, .L38[rip]
	mov	BYTE PTR 48[rsp], cl
	movzx	ecx, cl
	movdqa	xmm0, XMMWORD PTR 32[rsp]
	movsxd	rax, DWORD PTR [rdx+rcx*4]
	movaps	XMMWORD PTR 64[rsp], xmm0
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L38:
	.long	.L35-.L38
	.long	.L37-.L38
	.long	.L37-.L38
	.long	.L42-.L38
	.long	.L41-.L38
	.long	.L40-.L38
	.long	.L39-.L38
	.long	.L37-.L38
	.long	.L37-.L38
	.long	.L37-.L38
	.long	.L37-.L38
	.long	.L37-.L38
	.long	.L37-.L38
	.long	.L37-.L38
	.long	.L37-.L38
	.long	.L37-.L38
	.text
	.p2align 4,,10
	.p2align 3
.L33:
	and	ecx, 15
	jne	.L35
	mov	rcx, QWORD PTR [rdx]
	shr	rcx, 4
	cmp	rax, rcx
	jnb	.L35
	sal	rax, 5
	add	rax, QWORD PTR 8[rdx]
	movdqu	xmm2, XMMWORD PTR [rax]
	movzx	ecx, BYTE PTR 16[rax]
	movaps	XMMWORD PTR 32[rsp], xmm2
	jmp	.L34
	.p2align 4,,10
	.p2align 3
.L40:
	mov	rax, QWORD PTR 64[rsp]
	test	rax, rax
	js	.L43
	add	rsp, 104
	ret
	.p2align 4,,10
	.p2align 3
.L41:
	mov	eax, DWORD PTR 64[rsp]
	add	rsp, 104
	ret
	.p2align 4,,10
	.p2align 3
.L42:
	movsxd	rax, DWORD PTR 64[rsp]
	test	eax, eax
	js	.L43
	add	rsp, 104
	ret
	.p2align 4,,10
	.p2align 3
.L39:
	mov	rax, QWORD PTR 64[rsp]
	add	rsp, 104
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0.cold
	.seh_stackalloc	104
	.seh_endprologue
_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0.cold:
.L35:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
.L43:
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_format_errorPKc
.L37:
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.text
.LHOTE3:
	.section .rdata,"dr"
	.align 8
.LC4:
	.ascii "format error: failed to parse format-spec\0"
	.section	.text$_ZNSt8__format29__failed_to_parse_format_specEv,"x"
	.linkonce discard
	.globl	_ZNSt8__format29__failed_to_parse_format_specEv
	.def	_ZNSt8__format29__failed_to_parse_format_specEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format29__failed_to_parse_format_specEv
_ZNSt8__format29__failed_to_parse_format_specEv:
.LFB3565:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, .LC4[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC5:
	.ascii "format error: unmatched '{' in format string\0"
	.align 8
.LC6:
	.ascii "format error: unmatched '}' in format string\0"
	.section	.text$_ZNSt8__format8_ScannerIcE7_M_scanEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format8_ScannerIcE7_M_scanEv
	.def	_ZNSt8__format8_ScannerIcE7_M_scanEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format8_ScannerIcE7_M_scanEv
_ZNSt8__format8_ScannerIcE7_M_scanEv:
.LFB3947:
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
	mov	r14, QWORD PTR 16[rcx]
	mov	rbx, QWORD PTR 8[rcx]
	mov	rbp, r14
	sub	rbp, rbx
	mov	r13, rcx
	cmp	rbp, 2
	je	.L122
	test	rbp, rbp
	jne	.L48
.L46:
	add	rsp, 32
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
.L122:
	cmp	BYTE PTR [rbx], 123
	je	.L123
.L48:
	mov	r8, rbp
	mov	edx, 123
	mov	rcx, rbx
	mov	r12, -1
	call	memchr
	mov	r8, rbp
	mov	edx, 125
	mov	rcx, rbx
	mov	rsi, rax
	sub	rsi, rbx
	test	rax, rax
	cmove	rsi, r12
	call	memchr
	mov	rdi, rax
	sub	rdi, rbx
	test	rax, rax
	cmove	rdi, r12
	.p2align 4
	.p2align 3
.L54:
	cmp	rdi, rsi
	je	.L55
	cmp	rsi, rdi
	jb	.L56
.L57:
	lea	r12, 1[rdi]
	cmp	r12, rbp
	je	.L88
	cmp	BYTE PTR 1[rbx+rdi], 125
	jne	.L88
	mov	rbx, QWORD PTR 8[r13]
	mov	rax, QWORD PTR 0[r13]
	mov	rcx, r13
	add	rbx, r12
	mov	rdx, rbx
	add	rbx, 1
	call	[QWORD PTR [rax]]
	mov	r14, QWORD PTR 16[r13]
	lea	rax, -1[rsi]
	mov	QWORD PTR 8[r13], rbx
	sub	rax, r12
	cmp	rsi, -1
	mov	rbp, r14
	cmovne	rsi, rax
	sub	rbp, rbx
	je	.L46
	mov	r8, rbp
	mov	edx, 125
	mov	rcx, rbx
	call	memchr
	mov	rdi, rax
	sub	rdi, rbx
	test	rax, rax
	jne	.L54
	mov	rdi, -1
	cmp	rsi, -1
	je	.L55
	.p2align 4
	.p2align 3
.L56:
	lea	rax, 1[rsi]
	cmp	rax, rbp
	je	.L61
	movzx	r12d, BYTE PTR 1[rbx+rsi]
	cmp	rdi, -1
	je	.L87
	xor	ebp, ebp
	cmp	r12b, 123
	mov	rax, QWORD PTR 0[r13]
	mov	rcx, r13
	sete	bpl
	add	rbp, rsi
	add	rbp, QWORD PTR 8[r13]
	lea	rbx, 1[rbp]
	mov	rdx, rbp
	call	[QWORD PTR [rax]]
	mov	QWORD PTR 8[r13], rbx
	mov	r14, QWORD PTR 16[r13]
	cmp	r12b, 123
	je	.L124
	movzx	eax, BYTE PTR 1[rbp]
	cmp	al, 125
	je	.L125
	cmp	al, 58
	je	.L126
	cmp	al, 48
	je	.L127
	lea	edx, -49[rax]
	cmp	dl, 8
	ja	.L72
	movsx	dx, al
	lea	rcx, 2[rbp]
	movzx	eax, BYTE PTR 2[rbp]
	sub	edx, 48
	cmp	r14, rcx
	je	.L71
	lea	r8d, -48[rax]
	cmp	r8b, 9
	ja	.L71
	mov	rcx, rbx
	xor	edx, edx
	mov	r9d, 16
	jmp	.L81
	.p2align 4,,10
	.p2align 3
.L128:
	lea	edx, [rdx+rdx*4]
	movzx	r8d, r8b
	lea	edx, [r8+rdx*2]
.L76:
	add	rcx, 1
	cmp	r14, rcx
	je	.L82
.L81:
	movzx	eax, BYTE PTR [rcx]
	lea	r8d, -48[rax]
	cmp	r8b, 9
	ja	.L74
	sub	r9d, 4
	jns	.L128
	mov	r10d, 10
	mov	eax, edx
	mul	r10w
	jo	.L72
	movzx	r8d, r8b
	add	r8w, ax
	jc	.L72
	mov	edx, r8d
	jmp	.L76
	.p2align 4,,10
	.p2align 3
.L55:
	mov	rax, QWORD PTR 0[r13]
	mov	rdx, r14
	mov	rcx, r13
	call	[QWORD PTR [rax]]
	mov	rax, QWORD PTR 16[r13]
	mov	QWORD PTR 8[r13], rax
	add	rsp, 32
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
.L130:
	cmp	rsi, -1
	je	.L55
	lea	rax, 1[rsi]
	cmp	rbp, rax
	je	.L61
	movzx	r12d, BYTE PTR 1[r12+rax]
	.p2align 4
	.p2align 3
.L87:
	cmp	r12b, 123
	jne	.L61
	add	rax, QWORD PTR 8[r13]
	mov	rcx, r13
	mov	rdi, -1
	lea	rbx, 1[rax]
	mov	rdx, rax
	mov	rax, QWORD PTR 0[r13]
	call	[QWORD PTR [rax]]
	mov	r14, QWORD PTR 16[r13]
	mov	QWORD PTR 8[r13], rbx
	mov	rbp, r14
	sub	rbp, rbx
.L92:
	test	rbp, rbp
	je	.L46
	mov	r8, rbp
	mov	edx, 123
	mov	rcx, rbx
	call	memchr
	mov	rsi, rax
	sub	rsi, rbx
	test	rax, rax
	jne	.L54
	cmp	rdi, -1
	je	.L55
	mov	rsi, -1
	jmp	.L57
	.p2align 4,,10
	.p2align 3
.L124:
	mov	rbp, r14
	sub	rdi, 2
	sub	rbp, rbx
	sub	rdi, rsi
	jmp	.L92
	.p2align 4,,10
	.p2align 3
.L127:
	movzx	eax, BYTE PTR 2[rbp]
	lea	rcx, 2[rbp]
	xor	edx, edx
.L71:
	cmp	al, 125
	je	.L83
	cmp	al, 58
	jne	.L72
.L83:
	movzx	edx, dx
	cmp	DWORD PTR 24[r13], 2
	je	.L49
	xor	eax, eax
	mov	DWORD PTR 24[r13], 1
	cmp	BYTE PTR [rcx], 58
	sete	al
	add	rcx, rax
	mov	QWORD PTR 8[r13], rcx
.L68:
	mov	rax, QWORD PTR 0[r13]
	mov	rcx, r13
	call	[QWORD PTR 8[rax]]
	mov	r12, QWORD PTR 8[r13]
	mov	r14, QWORD PTR 16[r13]
	cmp	r12, r14
	je	.L61
	cmp	BYTE PTR [r12], 125
	jne	.L61
	lea	rbx, 1[r12]
	mov	rbp, r14
	mov	QWORD PTR 8[r13], rbx
	sub	rbp, rbx
	je	.L46
	mov	r8, rbp
	mov	edx, 123
	mov	rcx, rbx
	call	memchr
	test	rax, rax
	je	.L129
	sub	rax, rbx
	mov	r8, rbp
	mov	edx, 125
	mov	rcx, rbx
	mov	rsi, rax
	call	memchr
	mov	rdi, rax
	test	rax, rax
	je	.L130
.L86:
	sub	rdi, rbx
	jmp	.L54
	.p2align 4,,10
	.p2align 3
.L125:
	cmp	DWORD PTR 24[r13], 1
	je	.L49
	mov	rdx, QWORD PTR 32[r13]
	mov	DWORD PTR 24[r13], 2
	lea	rax, 1[rdx]
	mov	QWORD PTR 32[r13], rax
	jmp	.L68
	.p2align 4,,10
	.p2align 3
.L126:
	cmp	DWORD PTR 24[r13], 1
	je	.L49
	mov	rdx, QWORD PTR 32[r13]
	add	rbp, 2
	mov	DWORD PTR 24[r13], 2
	mov	QWORD PTR 8[r13], rbp
	lea	rax, 1[rdx]
	mov	QWORD PTR 32[r13], rax
	jmp	.L68
	.p2align 4,,10
	.p2align 3
.L123:
	cmp	BYTE PTR 1[rbx], 125
	jne	.L48
	mov	rax, QWORD PTR [rcx]
	add	rbx, 1
	mov	QWORD PTR 8[rcx], rbx
	mov	rax, QWORD PTR 8[rax]
	cmp	DWORD PTR 24[rcx], 1
	je	.L49
	mov	rdx, QWORD PTR 32[rcx]
	mov	DWORD PTR 24[rcx], 2
	lea	rcx, 1[rdx]
	mov	QWORD PTR 32[r13], rcx
	mov	rcx, r13
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L129:
	mov	r8, rbp
	mov	edx, 125
	mov	rcx, rbx
	call	memchr
	mov	rdi, rax
	test	rax, rax
	je	.L55
	mov	rsi, -1
	jmp	.L86
.L74:
	cmp	rbx, rcx
	je	.L72
.L82:
	movzx	eax, BYTE PTR [rcx]
	jmp	.L71
.L72:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
.L49:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L61:
	lea	rcx, .LC5[rip]
	call	_ZSt20__throw_format_errorPKc
.L88:
	lea	rcx, .LC6[rip]
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
.LFB4423:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L131
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L131:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC7:
	.ascii "false\0"
.LC8:
	.ascii "true\0"
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_15__do_vformat_toIS3_cS4_EET_S8_St17basic_string_viewIT0_St11char_traitsISA_EERKSt17basic_format_argsIT1_EPKSt6localeEUlRS8_E_EEDcOS8_NS1_6_Arg_tE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_15__do_vformat_toIS3_cS4_EET_S8_St17basic_string_viewIT0_St11char_traitsISA_EERKSt17basic_format_argsIT1_EPKSt6localeEUlRS8_E_EEDcOS8_NS1_6_Arg_tE
	.def	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_15__do_vformat_toIS3_cS4_EET_S8_St17basic_string_viewIT0_St11char_traitsISA_EERKSt17basic_format_argsIT1_EPKSt6localeEUlRS8_E_EEDcOS8_NS1_6_Arg_tE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_15__do_vformat_toIS3_cS4_EET_S8_St17basic_string_viewIT0_St11char_traitsISA_EERKSt17basic_format_argsIT1_EPKSt6localeEUlRS8_E_EEDcOS8_NS1_6_Arg_tE
_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_15__do_vformat_toIS3_cS4_EET_S8_St17basic_string_viewIT0_St11char_traitsISA_EERKSt17basic_format_argsIT1_EPKSt6localeEUlRS8_E_EEDcOS8_NS1_6_Arg_tE:
.LFB4543:
	push	r14
	.seh_pushreg	r14
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 280
	.seh_stackalloc	280
	.seh_endprologue
	mov	rbx, rdx
	movzx	r8d, r8b
	lea	rdx, .L136[rip]
	mov	rsi, rcx
	movsxd	rax, DWORD PTR [rdx+r8*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L136:
	.long	.L133-.L136
	.long	.L144-.L136
	.long	.L143-.L136
	.long	.L142-.L136
	.long	.L141-.L136
	.long	.L140-.L136
	.long	.L139-.L136
	.long	.L133-.L136
	.long	.L133-.L136
	.long	.L133-.L136
	.long	.L138-.L136
	.long	.L137-.L136
	.long	.L133-.L136
	.long	.L133-.L136
	.long	.L133-.L136
	.long	.L133-.L136
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_15__do_vformat_toIS3_cS4_EET_S8_St17basic_string_viewIT0_St11char_traitsISA_EERKSt17basic_format_argsIT1_EPKSt6localeEUlRS8_E_EEDcOS8_NS1_6_Arg_tE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L138:
	mov	r9, QWORD PTR [rcx]
	mov	rcx, r9
	mov	QWORD PTR 40[rsp], r9
	call	strlen
	mov	rdi, rax
	mov	rax, QWORD PTR [rbx]
	mov	rdx, rdi
	mov	rcx, QWORD PTR [rax]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
	mov	rsi, rax
	test	rax, rax
	je	.L133
	mov	rcx, QWORD PTR 24[rax]
	mov	rdx, QWORD PTR 40[rsp]
	mov	r8, rdi
.L232:
	call	memcpy
	mov	rax, QWORD PTR [rsi]
	mov	rdx, rdi
	mov	rcx, rsi
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR 8[rbx]
	mov	BYTE PTR [rax], 1
.L133:
	add	rsp, 280
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L137:
	mov	rax, QWORD PTR [rbx]
	mov	rdi, QWORD PTR [rcx]
	mov	r14, QWORD PTR 8[rcx]
	mov	rcx, QWORD PTR [rax]
	mov	rdx, rdi
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
	mov	rsi, rax
	test	rax, rax
	je	.L133
	mov	rcx, QWORD PTR 24[rax]
	mov	r8, rdi
	mov	rdx, r14
	jmp	.L232
	.p2align 4,,10
	.p2align 3
.L144:
	lea	rax, .LC7[rip]
	movzx	r8d, BYTE PTR [rcx]
	mov	QWORD PTR 64[rsp], rax
	lea	rax, .LC8[rip]
	mov	QWORD PTR 72[rsp], rax
	mov	rax, QWORD PTR [rbx]
	xor	r8d, 1
	movzx	r8d, r8b
	mov	rcx, QWORD PTR [rax]
	lea	edi, 4[r8]
	movsxd	rdx, edi
	mov	rax, QWORD PTR [rcx]
	mov	r14, rdx
	call	[QWORD PTR 8[rax]]
	test	rax, rax
	je	.L133
	movzx	ecx, BYTE PTR [rsi]
	mov	rdx, QWORD PTR 24[rax]
	mov	rcx, QWORD PTR 64[rsp+rcx*8]
	cmp	edi, 8
	jnb	.L146
	test	dil, 4
	jne	.L234
	test	edi, edi
	je	.L147
	movzx	r9d, BYTE PTR [rcx]
	mov	BYTE PTR [rdx], r9b
	test	dil, 2
	jne	.L235
.L147:
	mov	r8, QWORD PTR [rax]
	mov	rcx, rax
	mov	rdx, r14
	call	[QWORD PTR 16[r8]]
	mov	rax, QWORD PTR 8[rbx]
	mov	BYTE PTR [rax], 1
	jmp	.L133
	.p2align 4,,10
	.p2align 3
.L143:
	mov	rax, QWORD PTR [rbx]
	mov	edx, 1
	mov	rcx, QWORD PTR [rax]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
	test	rax, rax
	je	.L133
	mov	rdx, QWORD PTR 24[rax]
	movzx	ecx, BYTE PTR [rsi]
	mov	BYTE PTR [rdx], cl
	mov	r8, QWORD PTR [rax]
	mov	rcx, rax
	mov	edx, 1
	call	[QWORD PTR 16[r8]]
	mov	rax, QWORD PTR 8[rbx]
	mov	BYTE PTR [rax], 1
	jmp	.L133
	.p2align 4,,10
	.p2align 3
.L142:
	mov	edx, DWORD PTR [rcx]
	mov	esi, edx
	mov	eax, edx
	shr	esi, 31
	neg	eax
	cmovns	edx, eax
	mov	r8d, edx
	cmp	edx, 9
	jbe	.L194
	mov	eax, edx
	mov	edi, 1
	mov	ecx, 3518437209
	jmp	.L157
	.p2align 4,,10
	.p2align 3
.L154:
	cmp	eax, 999
	jbe	.L236
	cmp	eax, 9999
	jbe	.L237
	mov	edx, eax
	add	edi, 4
	imul	rdx, rcx
	shr	rdx, 45
	cmp	eax, 99999
	jbe	.L153
	mov	eax, edx
.L157:
	cmp	eax, 99
	ja	.L154
	add	edi, 1
.L153:
	mov	rax, QWORD PTR [rbx]
	lea	r10d, [rsi+rdi]
	mov	DWORD PTR 48[rsp], r8d
	mov	QWORD PTR 40[rsp], r10
	mov	rdx, r10
	mov	rcx, QWORD PTR [rax]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
	mov	rcx, rax
	test	rax, rax
	je	.L133
	mov	r11, QWORD PTR 24[rax]
	mov	r8d, DWORD PTR 48[rsp]
	movzx	esi, sil
	movabs	rax, 3688503277381496880
	movabs	rdx, 3976738051646829616
	mov	QWORD PTR 64[rsp], rax
	mov	r10, QWORD PTR 40[rsp]
	movabs	rax, 3544667369688283184
	mov	QWORD PTR 72[rsp], rdx
	movabs	rdx, 3832902143785906737
	mov	QWORD PTR 80[rsp], rax
	movabs	rax, 4121136918051239473
	mov	QWORD PTR 88[rsp], rdx
	movabs	rdx, 3689066235924983858
	mov	QWORD PTR 96[rsp], rax
	movabs	rax, 3977301010190316594
	mov	QWORD PTR 104[rsp], rdx
	movabs	rdx, 3545230328231770162
	mov	QWORD PTR 112[rsp], rax
	movabs	rax, 3833465102329393715
	mov	QWORD PTR 120[rsp], rdx
	movabs	rdx, 4121699876594726451
	mov	QWORD PTR 128[rsp], rax
	movabs	rax, 3689629194468470836
	mov	QWORD PTR 136[rsp], rdx
	movabs	rdx, 3977863968733803572
	mov	QWORD PTR 144[rsp], rax
	movabs	rax, 3545793286775257140
	mov	QWORD PTR 152[rsp], rdx
	movabs	rdx, 3834028060872880693
	mov	QWORD PTR 160[rsp], rax
	movabs	rax, 4122262835138213429
	mov	QWORD PTR 168[rsp], rdx
	movabs	rdx, 3690192153011957814
	mov	QWORD PTR 176[rsp], rax
	movabs	rax, 3978426927277290550
	mov	QWORD PTR 184[rsp], rdx
	movabs	rdx, 3546356245318744118
	mov	QWORD PTR 192[rsp], rax
	movabs	rax, 3834591019416367671
	mov	QWORD PTR 200[rsp], rdx
	movabs	rdx, 4122825793681700407
	mov	QWORD PTR 208[rsp], rax
	movabs	rax, 3690755111555444792
	mov	QWORD PTR 216[rsp], rdx
	movabs	rdx, 3978989885820777528
	mov	QWORD PTR 224[rsp], rax
	movabs	rax, 3546919203862231096
	mov	QWORD PTR 232[rsp], rdx
	movabs	rdx, 3835153977959854649
	mov	QWORD PTR 248[rsp], rdx
	movabs	rdx, 16106987313379638
	mov	BYTE PTR [r11], 45
	add	r11, rsi
	cmp	r8d, 99
	mov	QWORD PTR 240[rsp], rax
	movabs	rax, 4122263930388298034
	mov	QWORD PTR 249[rsp], rax
	mov	QWORD PTR 257[rsp], rdx
	jbe	.L159
	lea	r9d, -1[rdi]
	.p2align 4
	.p2align 3
.L160:
	mov	edx, r8d
	mov	eax, r8d
	imul	rdx, rdx, 1374389535
	shr	rdx, 37
	imul	esi, edx, 100
	sub	eax, esi
	mov	esi, r8d
	mov	r8d, edx
	mov	edx, r9d
	add	eax, eax
	lea	edi, 1[rax]
	movzx	eax, BYTE PTR 64[rsp+rax]
	movzx	edi, BYTE PTR 64[rsp+rdi]
	mov	BYTE PTR [r11+rdx], dil
	lea	edx, -1[r9]
	sub	r9d, 2
	mov	BYTE PTR [r11+rdx], al
	cmp	esi, 9999
	ja	.L160
.L159:
	lea	eax, 48[r8]
	cmp	r8d, 9
	jbe	.L162
	lea	eax, [r8+r8]
	lea	edx, 1[rax]
	movzx	eax, BYTE PTR 64[rsp+rax]
	movzx	edx, BYTE PTR 64[rsp+rdx]
	mov	BYTE PTR 1[r11], dl
.L162:
	mov	BYTE PTR [r11], al
	mov	rax, QWORD PTR [rcx]
	mov	rdx, r10
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR 8[rbx]
	mov	BYTE PTR [rax], 1
	jmp	.L133
	.p2align 4,,10
	.p2align 3
.L141:
	mov	r8d, DWORD PTR [rcx]
	cmp	r8d, 9
	jbe	.L163
	mov	eax, r8d
	mov	esi, 1
	mov	ecx, 3518437209
	jmp	.L168
	.p2align 4,,10
	.p2align 3
.L164:
	cmp	eax, 999
	jbe	.L238
	cmp	eax, 9999
	jbe	.L239
	mov	edx, eax
	add	esi, 4
	imul	rdx, rcx
	shr	rdx, 45
	cmp	eax, 99999
	jbe	.L165
	mov	eax, edx
.L168:
	cmp	eax, 99
	ja	.L164
	add	esi, 1
.L165:
	mov	rax, QWORD PTR [rbx]
	mov	r11d, esi
	mov	DWORD PTR 48[rsp], r8d
	mov	QWORD PTR 40[rsp], r11
	mov	rdx, r11
	mov	rcx, QWORD PTR [rax]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
	mov	rdi, rax
	test	rax, rax
	je	.L133
	movabs	rdx, 3976738051646829616
	mov	rcx, QWORD PTR 24[rax]
	mov	r8d, DWORD PTR 48[rsp]
	movabs	rax, 3688503277381496880
	mov	QWORD PTR 64[rsp], rax
	mov	r11, QWORD PTR 40[rsp]
	movabs	rax, 3544667369688283184
	mov	QWORD PTR 72[rsp], rdx
	cmp	r8d, 99
	movabs	rdx, 3832902143785906737
	mov	QWORD PTR 80[rsp], rax
	movabs	rax, 4121136918051239473
	mov	QWORD PTR 88[rsp], rdx
	movabs	rdx, 3689066235924983858
	mov	QWORD PTR 96[rsp], rax
	movabs	rax, 3977301010190316594
	mov	QWORD PTR 104[rsp], rdx
	movabs	rdx, 3545230328231770162
	mov	QWORD PTR 112[rsp], rax
	movabs	rax, 3833465102329393715
	mov	QWORD PTR 120[rsp], rdx
	movabs	rdx, 4121699876594726451
	mov	QWORD PTR 128[rsp], rax
	movabs	rax, 3689629194468470836
	mov	QWORD PTR 136[rsp], rdx
	movabs	rdx, 3977863968733803572
	mov	QWORD PTR 144[rsp], rax
	movabs	rax, 3545793286775257140
	mov	QWORD PTR 152[rsp], rdx
	movabs	rdx, 3834028060872880693
	mov	QWORD PTR 160[rsp], rax
	movabs	rax, 4122262835138213429
	mov	QWORD PTR 168[rsp], rdx
	movabs	rdx, 3690192153011957814
	mov	QWORD PTR 176[rsp], rax
	movabs	rax, 3978426927277290550
	mov	QWORD PTR 184[rsp], rdx
	movabs	rdx, 3546356245318744118
	mov	QWORD PTR 192[rsp], rax
	movabs	rax, 3834591019416367671
	mov	QWORD PTR 200[rsp], rdx
	movabs	rdx, 4122825793681700407
	mov	QWORD PTR 208[rsp], rax
	movabs	rax, 3690755111555444792
	mov	QWORD PTR 216[rsp], rdx
	movabs	rdx, 3978989885820777528
	mov	QWORD PTR 224[rsp], rax
	movabs	rax, 3546919203862231096
	mov	QWORD PTR 232[rsp], rdx
	movabs	rdx, 3835153977959854649
	mov	QWORD PTR 248[rsp], rdx
	movabs	rdx, 16106987313379638
	mov	QWORD PTR 240[rsp], rax
	movabs	rax, 4122263930388298034
	mov	QWORD PTR 249[rsp], rax
	mov	QWORD PTR 257[rsp], rdx
	jbe	.L169
	lea	r9d, -1[rsi]
	.p2align 4
	.p2align 3
.L170:
	mov	edx, r8d
	mov	eax, r8d
	imul	rdx, rdx, 1374389535
	shr	rdx, 37
	imul	r10d, edx, 100
	sub	eax, r10d
	mov	r10d, r8d
	mov	r8d, edx
	mov	edx, r9d
	add	eax, eax
	lea	esi, 1[rax]
	movzx	eax, BYTE PTR 64[rsp+rax]
	movzx	esi, BYTE PTR 64[rsp+rsi]
	mov	BYTE PTR [rcx+rdx], sil
	lea	edx, -1[r9]
	sub	r9d, 2
	mov	BYTE PTR [rcx+rdx], al
	cmp	r10d, 9999
	ja	.L170
	cmp	r10d, 999
	ja	.L169
.L171:
	add	r8d, 48
.L172:
	mov	BYTE PTR [rcx], r8b
	jmp	.L233
	.p2align 4,,10
	.p2align 3
.L140:
	mov	rax, QWORD PTR [rcx]
	mov	rsi, rax
	mov	r9, rax
	shr	rsi, 63
	neg	r9
	cmovs	r9, rax
	cmp	r9, 9
	jbe	.L197
	mov	rcx, r9
	mov	r8d, 1
	movabs	r10, 3777893186295716171
	jmp	.L177
	.p2align 4,,10
	.p2align 3
.L174:
	cmp	rcx, 999
	jbe	.L240
	cmp	rcx, 9999
	jbe	.L241
	mov	rax, rcx
	add	r8d, 4
	mul	r10
	cmp	rcx, 99999
	jbe	.L173
	mov	rcx, rdx
	shr	rcx, 11
.L177:
	cmp	rcx, 99
	ja	.L174
	add	r8d, 1
.L173:
	mov	rax, QWORD PTR [rbx]
	lea	r11d, [r8+rsi]
	mov	QWORD PTR 48[rsp], r9
	mov	DWORD PTR 60[rsp], r8d
	mov	rdx, r11
	mov	rcx, QWORD PTR [rax]
	mov	QWORD PTR 40[rsp], r11
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
	mov	rdi, rax
	test	rax, rax
	je	.L133
	mov	rcx, QWORD PTR 24[rax]
	mov	r9, QWORD PTR 48[rsp]
	movabs	rax, 3688503277381496880
	movabs	rdx, 3976738051646829616
	mov	QWORD PTR 64[rsp], rax
	mov	r11, QWORD PTR 40[rsp]
	movabs	rax, 3544667369688283184
	mov	QWORD PTR 72[rsp], rdx
	movabs	rdx, 3832902143785906737
	mov	QWORD PTR 80[rsp], rax
	movabs	rax, 4121136918051239473
	mov	QWORD PTR 88[rsp], rdx
	movabs	rdx, 3689066235924983858
	mov	QWORD PTR 96[rsp], rax
	movabs	rax, 3977301010190316594
	mov	QWORD PTR 104[rsp], rdx
	movabs	rdx, 3545230328231770162
	mov	QWORD PTR 112[rsp], rax
	movabs	rax, 3833465102329393715
	mov	QWORD PTR 120[rsp], rdx
	movabs	rdx, 4121699876594726451
	mov	QWORD PTR 128[rsp], rax
	movabs	rax, 3689629194468470836
	mov	QWORD PTR 136[rsp], rdx
	movabs	rdx, 3977863968733803572
	mov	QWORD PTR 144[rsp], rax
	movabs	rax, 3545793286775257140
	mov	QWORD PTR 152[rsp], rdx
	movabs	rdx, 3834028060872880693
	mov	QWORD PTR 160[rsp], rax
	movabs	rax, 4122262835138213429
	mov	QWORD PTR 168[rsp], rdx
	movabs	rdx, 3690192153011957814
	mov	QWORD PTR 176[rsp], rax
	movabs	rax, 3978426927277290550
	mov	QWORD PTR 184[rsp], rdx
	movabs	rdx, 3546356245318744118
	mov	QWORD PTR 192[rsp], rax
	movabs	rax, 3834591019416367671
	mov	QWORD PTR 200[rsp], rdx
	movabs	rdx, 4122825793681700407
	mov	QWORD PTR 208[rsp], rax
	movabs	rax, 3690755111555444792
	mov	QWORD PTR 216[rsp], rdx
	movabs	rdx, 3978989885820777528
	mov	QWORD PTR 224[rsp], rax
	movabs	rax, 3546919203862231096
	mov	QWORD PTR 232[rsp], rdx
	movabs	rdx, 3835153977959854649
	mov	QWORD PTR 248[rsp], rdx
	movabs	rdx, 16106987313379638
	mov	BYTE PTR [rcx], 45
	add	rcx, rsi
	cmp	r9, 99
	mov	QWORD PTR 240[rsp], rax
	movabs	rax, 4122263930388298034
	mov	QWORD PTR 249[rsp], rax
	mov	QWORD PTR 257[rsp], rdx
	jbe	.L178
	movabs	rsi, 2951479051793528259
	mov	r8d, DWORD PTR 60[rsp]
	sub	r8d, 1
	.p2align 4
	.p2align 3
.L179:
	mov	rdx, r9
	shr	rdx, 2
	mov	rax, rdx
	mul	rsi
	mov	rax, r9
	shr	rdx, 2
	imul	r10, rdx, 100
	sub	rax, r10
	mov	r10, r9
	mov	r9, rdx
	mov	edx, r8d
	movzx	r14d, BYTE PTR 65[rsp+rax*2]
	movzx	eax, BYTE PTR 64[rsp+rax*2]
	mov	BYTE PTR [rcx+rdx], r14b
	lea	edx, -1[r8]
	sub	r8d, 2
	mov	BYTE PTR [rcx+rdx], al
	cmp	r10, 9999
	ja	.L179
.L178:
	lea	eax, 48[r9]
	cmp	r9, 9
	ja	.L242
.L181:
	mov	BYTE PTR [rcx], al
.L233:
	mov	rax, QWORD PTR [rdi]
	mov	rdx, r11
	mov	rcx, rdi
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR 8[rbx]
	mov	BYTE PTR [rax], 1
	add	rsp, 280
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L139:
	mov	rdi, QWORD PTR [rcx]
	cmp	rdi, 9
	jbe	.L182
	mov	rcx, rdi
	mov	r8d, 1
	movabs	r10, 3777893186295716171
	jmp	.L187
	.p2align 4,,10
	.p2align 3
.L183:
	cmp	rcx, 999
	jbe	.L243
	cmp	rcx, 9999
	jbe	.L244
	mov	rax, rcx
	add	r8d, 4
	mul	r10
	cmp	rcx, 99999
	jbe	.L184
	mov	rcx, rdx
	shr	rcx, 11
.L187:
	cmp	rcx, 99
	ja	.L183
	add	r8d, 1
.L184:
	mov	rax, QWORD PTR [rbx]
	mov	r11d, r8d
	mov	DWORD PTR 48[rsp], r8d
	mov	QWORD PTR 40[rsp], r11
	mov	rdx, r11
	mov	rcx, QWORD PTR [rax]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
	mov	rsi, rax
	test	rax, rax
	je	.L133
	mov	rcx, QWORD PTR 24[rax]
	cmp	rdi, 99
	mov	r11, QWORD PTR 40[rsp]
	movabs	rax, 3688503277381496880
	movabs	rdx, 3976738051646829616
	mov	QWORD PTR 64[rsp], rax
	movabs	rax, 3544667369688283184
	mov	QWORD PTR 72[rsp], rdx
	movabs	rdx, 3832902143785906737
	mov	QWORD PTR 80[rsp], rax
	movabs	rax, 4121136918051239473
	mov	QWORD PTR 88[rsp], rdx
	movabs	rdx, 3689066235924983858
	mov	QWORD PTR 96[rsp], rax
	movabs	rax, 3977301010190316594
	mov	QWORD PTR 104[rsp], rdx
	movabs	rdx, 3545230328231770162
	mov	QWORD PTR 112[rsp], rax
	movabs	rax, 3833465102329393715
	mov	QWORD PTR 120[rsp], rdx
	movabs	rdx, 4121699876594726451
	mov	QWORD PTR 128[rsp], rax
	movabs	rax, 3689629194468470836
	mov	QWORD PTR 136[rsp], rdx
	movabs	rdx, 3977863968733803572
	mov	QWORD PTR 144[rsp], rax
	movabs	rax, 3545793286775257140
	mov	QWORD PTR 152[rsp], rdx
	movabs	rdx, 3834028060872880693
	mov	QWORD PTR 160[rsp], rax
	movabs	rax, 4122262835138213429
	mov	QWORD PTR 168[rsp], rdx
	movabs	rdx, 3690192153011957814
	mov	QWORD PTR 176[rsp], rax
	movabs	rax, 3978426927277290550
	mov	QWORD PTR 184[rsp], rdx
	movabs	rdx, 3546356245318744118
	mov	QWORD PTR 192[rsp], rax
	movabs	rax, 3834591019416367671
	mov	QWORD PTR 200[rsp], rdx
	movabs	rdx, 4122825793681700407
	mov	QWORD PTR 208[rsp], rax
	movabs	rax, 3690755111555444792
	mov	QWORD PTR 216[rsp], rdx
	movabs	rdx, 3978989885820777528
	mov	QWORD PTR 224[rsp], rax
	movabs	rax, 3546919203862231096
	mov	QWORD PTR 232[rsp], rdx
	movabs	rdx, 3835153977959854649
	mov	QWORD PTR 248[rsp], rdx
	movabs	rdx, 16106987313379638
	mov	QWORD PTR 240[rsp], rax
	movabs	rax, 4122263930388298034
	mov	QWORD PTR 249[rsp], rax
	mov	QWORD PTR 257[rsp], rdx
	jbe	.L188
	movabs	r9, 2951479051793528259
	mov	r8d, DWORD PTR 48[rsp]
	sub	r8d, 1
	.p2align 4
	.p2align 3
.L189:
	mov	rdx, rdi
	shr	rdx, 2
	mov	rax, rdx
	mul	r9
	mov	rax, rdi
	shr	rdx, 2
	imul	r10, rdx, 100
	sub	rax, r10
	mov	r10, rdi
	mov	rdi, rdx
	mov	edx, r8d
	movzx	r14d, BYTE PTR 65[rsp+rax*2]
	movzx	eax, BYTE PTR 64[rsp+rax*2]
	mov	BYTE PTR [rcx+rdx], r14b
	lea	edx, -1[r8]
	sub	r8d, 2
	mov	BYTE PTR [rcx+rdx], al
	cmp	r10, 9999
	ja	.L189
	cmp	r10, 999
	ja	.L188
.L190:
	lea	r9d, 48[rdi]
.L191:
	mov	BYTE PTR [rcx], r9b
	mov	rax, QWORD PTR [rsi]
	mov	rdx, r11
	mov	rcx, rsi
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR 8[rbx]
	mov	BYTE PTR [rax], 1
	jmp	.L133
	.p2align 4,,10
	.p2align 3
.L242:
	movzx	eax, BYTE PTR 65[rsp+r9*2]
	mov	BYTE PTR 1[rcx], al
	movzx	eax, BYTE PTR 64[rsp+r9*2]
	jmp	.L181
	.p2align 4,,10
	.p2align 3
.L146:
	mov	r9, QWORD PTR [rcx]
	mov	QWORD PTR [rdx], r9
	mov	r9d, edi
	mov	r10, QWORD PTR -8[rcx+r9]
	mov	QWORD PTR -8[rdx+r9], r10
	lea	r9, 8[rdx]
	and	r9, -8
	sub	rdx, r9
	lea	r8d, [rdi+rdx]
	sub	rcx, rdx
	and	r8d, -8
	cmp	r8d, 8
	jb	.L147
	and	r8d, -8
	xor	edx, edx
.L150:
	mov	r10d, edx
	add	edx, 8
	mov	r11, QWORD PTR [rcx+r10]
	mov	QWORD PTR [r9+r10], r11
	cmp	edx, r8d
	jb	.L150
	jmp	.L147
	.p2align 4,,10
	.p2align 3
.L169:
	add	r8d, r8d
	lea	eax, 1[r8]
	movzx	r8d, BYTE PTR 64[rsp+r8]
	movzx	eax, BYTE PTR 64[rsp+rax]
	mov	BYTE PTR 1[rcx], al
	jmp	.L172
	.p2align 4,,10
	.p2align 3
.L188:
	movzx	eax, BYTE PTR 65[rsp+rdi*2]
	movzx	r9d, BYTE PTR 64[rsp+rdi*2]
	mov	BYTE PTR 1[rcx], al
	jmp	.L191
	.p2align 4,,10
	.p2align 3
.L243:
	add	r8d, 2
	jmp	.L184
	.p2align 4,,10
	.p2align 3
.L236:
	add	edi, 2
	jmp	.L153
	.p2align 4,,10
	.p2align 3
.L240:
	add	r8d, 2
	jmp	.L173
	.p2align 4,,10
	.p2align 3
.L238:
	add	esi, 2
	jmp	.L165
	.p2align 4,,10
	.p2align 3
.L241:
	add	r8d, 3
	jmp	.L173
	.p2align 4,,10
	.p2align 3
.L239:
	add	esi, 3
	jmp	.L165
	.p2align 4,,10
	.p2align 3
.L244:
	add	r8d, 3
	jmp	.L184
	.p2align 4,,10
	.p2align 3
.L237:
	add	edi, 3
	jmp	.L153
.L197:
	mov	r8d, 1
	jmp	.L173
.L163:
	mov	rax, QWORD PTR [rbx]
	mov	DWORD PTR 40[rsp], r8d
	mov	edx, 1
	mov	rcx, QWORD PTR [rax]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
	mov	r8d, DWORD PTR 40[rsp]
	test	rax, rax
	mov	rdi, rax
	je	.L133
	mov	rcx, QWORD PTR 24[rdi]
	mov	r11d, 1
	jmp	.L171
.L182:
	mov	rax, QWORD PTR [rbx]
	mov	edx, 1
	mov	rcx, QWORD PTR [rax]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
	mov	rsi, rax
	test	rax, rax
	je	.L133
	mov	rcx, QWORD PTR 24[rsi]
	mov	r11d, 1
	jmp	.L190
.L194:
	mov	edi, 1
	jmp	.L153
.L234:
	mov	r9d, DWORD PTR [rcx]
	mov	r8d, edi
	mov	DWORD PTR [rdx], r9d
	mov	ecx, DWORD PTR -4[rcx+r8]
	mov	DWORD PTR -4[rdx+r8], ecx
	jmp	.L147
.L235:
	mov	r8d, edi
	movzx	ecx, WORD PTR -2[rcx+r8]
	mov	WORD PTR -2[rdx+r8], cx
	jmp	.L147
	.seh_endproc
	.section .rdata,"dr"
.LC9:
	.ascii "({}, {})\0"
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE6handle9_S_formatIK5PointEEvRSt26basic_format_parse_contextIcERS4_PKv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE6handle9_S_formatIK5PointEEvRSt26basic_format_parse_contextIcERS4_PKv
	.def	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE6handle9_S_formatIK5PointEEvRSt26basic_format_parse_contextIcERS4_PKv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE6handle9_S_formatIK5PointEEvRSt26basic_format_parse_contextIcERS4_PKv
_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE6handle9_S_formatIK5PointEEvRSt26basic_format_parse_contextIcERS4_PKv:
.LFB5137:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 192
	.seh_stackalloc	192
	.seh_endprologue
	movdqa	xmm0, XMMWORD PTR .LC10[rip]
	mov	rax, QWORD PTR 16[rdx]
	mov	QWORD PTR 96[rsp], rax
	lea	rax, .LC9[rip+8]
	mov	rbx, rdx
	mov	edx, DWORD PTR [r8]
	mov	QWORD PTR 144[rsp], rax
	sub	rax, 8
	lea	rcx, 128[rsp]
	movaps	XMMWORD PTR 160[rsp], xmm0
	movq	xmm1, rax
	movq	xmm0, QWORD PTR .LC11[rip]
	lea	rax, 80[rsp]
	mov	DWORD PTR 48[rsp], edx
	mov	edx, DWORD PTR 4[r8]
	movq	xmm2, rax
	punpcklqdq	xmm0, xmm1
	mov	BYTE PTR 112[rsp], 0
	movaps	XMMWORD PTR 128[rsp], xmm0
	pxor	xmm0, xmm0
	mov	DWORD PTR 64[rsp], edx
	punpcklqdq	xmm0, xmm2
	lea	rdx, 48[rsp]
	mov	QWORD PTR 80[rsp], 1586
	mov	QWORD PTR 88[rsp], rdx
	mov	QWORD PTR 104[rsp], 0
	mov	DWORD PTR 152[rsp], 0
	movaps	XMMWORD PTR 176[rsp], xmm0
.LEHB2:
	call	_ZNSt8__format8_ScannerIcE7_M_scanEv
.LEHE2:
	mov	rax, QWORD PTR 96[rsp]
	cmp	BYTE PTR 112[rsp], 0
	jne	.L251
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 192
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L251:
	lea	rcx, 104[rsp]
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt6localeD1Ev
	mov	rax, QWORD PTR 40[rsp]
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 192
	pop	rbx
	ret
.L249:
	mov	rbx, rax
.L247:
	cmp	BYTE PTR 112[rsp], 0
	je	.L248
	lea	rcx, 104[rsp]
	call	_ZNSt6localeD1Ev
.L248:
	mov	rcx, rbx
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5137:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5137-.LLSDACSB5137
.LLSDACSB5137:
	.uleb128 .LEHB2-.LFB5137
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L249-.LFB5137
	.uleb128 0
	.uleb128 .LEHB3-.LFB5137
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSE5137:
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE6handle9_S_formatIK5PointEEvRSt26basic_format_parse_contextIcERS4_PKv,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC12:
	.ascii "format error: invalid width or precision in format-spec\0"
	.section	.text$_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE
	.def	_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE
_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE:
.LFB4639:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	r11, rdx
	movzx	edx, BYTE PTR [rcx]
	mov	rbx, rcx
	lea	rcx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	mov	r10, rbx
	cmp	BYTE PTR [rcx+rdx], 9
	ja	.L253
	xor	eax, eax
	mov	r9d, 16
	jmp	.L262
	.p2align 4,,10
	.p2align 3
.L287:
	lea	eax, [rax+rax*4]
	movzx	ecx, cl
	add	r10, 1
	lea	eax, [rcx+rax*2]
	cmp	r11, r10
	je	.L263
.L262:
	movzx	edx, BYTE PTR [r10]
	lea	ecx, -48[rdx]
	cmp	cl, 9
	ja	.L254
	sub	r9d, 4
	jns	.L287
	mov	edx, 10
	mul	dx
	jo	.L259
	movzx	ecx, cl
	add	cx, ax
	jc	.L259
	add	r10, 1
	mov	eax, ecx
	cmp	r11, r10
	jne	.L262
	.p2align 4
	.p2align 3
.L263:
	mov	WORD PTR [r8], ax
.L252:
	mov	rax, r10
	add	rsp, 32
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L253:
	cmp	dl, 123
	jne	.L252
	lea	r10, 1[rbx]
	mov	BYTE PTR [r9], 1
	cmp	r10, r11
	je	.L288
	movsx	ax, BYTE PTR 1[rbx]
	cmp	al, 125
	je	.L289
	cmp	al, 48
	je	.L290
	lea	edx, -49[rax]
	cmp	dl, 8
	ja	.L271
	lea	rcx, 2[rbx]
	cmp	r11, rcx
	je	.L271
	movzx	edx, BYTE PTR 2[rbx]
	sub	edx, 48
	cmp	dl, 9
	ja	.L272
	mov	r9, r10
	xor	eax, eax
	mov	ebx, 16
	jmp	.L280
	.p2align 4,,10
	.p2align 3
.L292:
	lea	eax, [rax+rax*4]
	movzx	ecx, cl
	lea	eax, [rcx+rax*2]
.L275:
	add	r9, 1
	cmp	r11, r9
	je	.L291
.L280:
	movzx	edx, BYTE PTR [r9]
	lea	ecx, -48[rdx]
	cmp	cl, 9
	ja	.L273
	sub	ebx, 4
	jns	.L292
	mov	edx, 10
	mul	dx
	jo	.L271
	movzx	ecx, cl
	add	cx, ax
	jc	.L271
	mov	eax, ecx
	jmp	.L275
	.p2align 4,,10
	.p2align 3
.L254:
	cmp	rbx, r10
	jne	.L263
.L259:
	lea	rcx, .LC12[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L289:
	mov	rax, QWORD PTR 80[rsp]
	cmp	DWORD PTR 16[rax], 1
	je	.L282
	mov	rax, QWORD PTR 80[rsp]
	mov	rbx, QWORD PTR 80[rsp]
	mov	DWORD PTR 16[rax], 2
	mov	rax, QWORD PTR 24[rax]
	lea	rdx, 1[rax]
	mov	QWORD PTR 24[rbx], rdx
.L268:
	add	r10, 1
	mov	WORD PTR [r8], ax
	mov	rax, r10
	add	rsp, 32
	pop	rbx
	ret
.L290:
	lea	r10, 2[rbx]
	xor	eax, eax
.L270:
	cmp	r11, r10
	je	.L271
.L283:
	cmp	BYTE PTR [r10], 125
	jne	.L271
	mov	rbx, QWORD PTR 80[rsp]
	cmp	DWORD PTR 16[rbx], 2
	je	.L282
	mov	DWORD PTR 16[rbx], 1
	jmp	.L268
.L272:
	sub	eax, 48
	mov	r10, rcx
	jmp	.L283
.L273:
	cmp	r10, r9
	je	.L271
	mov	r10, r9
	jmp	.L270
.L291:
	mov	r10, r11
	jmp	.L270
.L288:
	lea	rcx, .LC5[rip]
	call	_ZSt20__throw_format_errorPKc
.L282:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L271:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC13:
	.ascii "basic_string::_M_create\0"
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy:
.LFB5020:
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
	mov	rbp, QWORD PTR 8[rcx]
	mov	rdi, QWORD PTR [rcx]
	mov	r12, r9
	lea	r14, 16[rcx]
	mov	rbx, rcx
	mov	rsi, rdx
	mov	r9, QWORD PTR 160[rsp]
	sub	r9, r8
	lea	r15, [r9+rbp]
	cmp	r14, rdi
	je	.L324
	movabs	rdx, 9223372036854775806
	mov	rax, QWORD PTR 16[rcx]
	cmp	rdx, r15
	jb	.L295
	lea	rcx, 1[r15]
	cmp	rax, r15
	jnb	.L301
	add	rax, rax
	cmp	r15, rax
	jnb	.L301
	lea	rcx, 1[rax]
	mov	r15, rax
	cmp	rdx, rax
	jnb	.L301
	movabs	rcx, 9223372036854775807
	mov	r15, rdx
	.p2align 4
	.p2align 3
.L301:
	lea	rax, [rsi+r8]
	mov	QWORD PTR 40[rsp], rax
	sub	rbp, rax
	call	_Znwy
	mov	r13, rax
	test	rsi, rsi
	je	.L302
	cmp	rsi, 1
	je	.L325
	mov	r8, rsi
	mov	rdx, rdi
	mov	rcx, rax
	call	memcpy
.L302:
	test	r12, r12
	je	.L304
	cmp	QWORD PTR 160[rsp], 0
	je	.L304
	lea	rcx, 0[r13+rsi]
	cmp	QWORD PTR 160[rsp], 1
	je	.L326
	mov	r8, QWORD PTR 160[rsp]
	mov	rdx, r12
	call	memcpy
.L304:
	test	rbp, rbp
	jne	.L327
.L306:
	cmp	r14, rdi
	je	.L308
	mov	rax, QWORD PTR 16[rbx]
	mov	rcx, rdi
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L308:
	mov	QWORD PTR [rbx], r13
	mov	QWORD PTR 16[rbx], r15
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
.L327:
	mov	rdx, QWORD PTR 40[rsp]
	add	rsi, QWORD PTR 160[rsp]
	lea	rcx, 0[r13+rsi]
	add	rdx, rdi
	cmp	rbp, 1
	je	.L328
	mov	r8, rbp
	call	memcpy
	jmp	.L306
	.p2align 4,,10
	.p2align 3
.L324:
	movabs	rax, 9223372036854775806
	cmp	rax, r15
	jb	.L295
	lea	rax, -16[r15]
	lea	rcx, 1[r15]
	cmp	rax, 13
	ja	.L301
	mov	ecx, 31
	mov	r15d, 30
	jmp	.L301
	.p2align 4,,10
	.p2align 3
.L325:
	movzx	eax, BYTE PTR [rdi]
	mov	BYTE PTR 0[r13], al
	jmp	.L302
	.p2align 4,,10
	.p2align 3
.L326:
	movzx	eax, BYTE PTR [r12]
	mov	BYTE PTR [rcx], al
	test	rbp, rbp
	je	.L306
	jmp	.L327
	.p2align 4,,10
	.p2align 3
.L328:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rcx], al
	jmp	.L306
.L295:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC14:
	.ascii "basic_string::append\0"
	.section	.text$_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv
	.def	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv
_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE11_M_overflowEv:
.LFB4566:
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	mov	r9, QWORD PTR 8[rcx]
	mov	r8, QWORD PTR 24[rcx]
	mov	r10, rcx
	sub	r8, r9
	je	.L329
	mov	rdx, QWORD PTR 296[rcx]
	movabs	rax, 9223372036854775806
	sub	rax, rdx
	cmp	rax, r8
	jb	.L340
	mov	rcx, QWORD PTR 288[rcx]
	lea	rax, 304[r10]
	cmp	rcx, rax
	je	.L336
	mov	rax, QWORD PTR 304[r10]
.L332:
	lea	r11, [r8+rdx]
	cmp	rax, r11
	jb	.L333
	add	rcx, rdx
	cmp	r8, 1
	je	.L341
	mov	rdx, r9
	mov	QWORD PTR 80[rsp], r10
	mov	QWORD PTR 56[rsp], r11
	call	memcpy
	mov	r11, QWORD PTR 56[rsp]
	mov	r10, QWORD PTR 80[rsp]
	jmp	.L335
	.p2align 4,,10
	.p2align 3
.L333:
	mov	QWORD PTR 32[rsp], r8
	lea	rcx, 288[r10]
	xor	r8d, r8d
	mov	QWORD PTR 56[rsp], r11
	mov	QWORD PTR 80[rsp], r10
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	r11, QWORD PTR 56[rsp]
	mov	r10, QWORD PTR 80[rsp]
.L335:
	mov	rax, QWORD PTR 288[r10]
	mov	QWORD PTR 296[r10], r11
	mov	BYTE PTR [rax+r11], 0
	mov	rax, QWORD PTR 8[r10]
	mov	QWORD PTR 24[r10], rax
.L329:
	add	rsp, 72
	ret
	.p2align 4,,10
	.p2align 3
.L341:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	jmp	.L335
	.p2align 4,,10
	.p2align 3
.L336:
	mov	eax, 15
	jmp	.L332
.L340:
	lea	rcx, .LC14[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC16:
	.ascii "p={}\0"
.LC17:
	.ascii "%s\12\0"
	.section	.text.unlikely,"x"
.LCOLDB19:
	.section	.text.startup,"x"
.LHOTB19:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3986:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 528
	.seh_stackalloc	528
	.seh_endprologue
	call	__main
	mov	rax, QWORD PTR .LC15[rip]
	movq	xmm0, QWORD PTR .LC18[rip]
	lea	rcx, 80[rsp]
	lea	rbx, 144[rsp]
	mov	QWORD PTR 104[rsp], rcx
	lea	rdx, 208[rsp]
	mov	QWORD PTR 72[rsp], rax
	mov	rcx, rbx
	lea	rax, 72[rsp]
	lea	rsi, 512[rsp]
	mov	QWORD PTR 80[rsp], rax
	lea	rax, _ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE6handle9_S_formatIK5PointEEvRSt26basic_format_parse_contextIcERS4_PKv[rip]
	mov	QWORD PTR 88[rsp], rax
	lea	rax, 240[rsp]
	movq	xmm1, rax
	mov	QWORD PTR 232[rsp], rax
	lea	rax, .LC16[rip+4]
	punpcklqdq	xmm0, xmm1
	mov	QWORD PTR 160[rsp], rax
	sub	rax, 4
	movaps	XMMWORD PTR 208[rsp], xmm0
	movdqa	xmm0, XMMWORD PTR .LC10[rip]
	movq	xmm2, rax
	lea	rax, 96[rsp]
	movq	xmm3, rax
	mov	QWORD PTR 224[rsp], 256
	movaps	XMMWORD PTR 176[rsp], xmm0
	movq	xmm0, QWORD PTR .LC11[rip]
	mov	QWORD PTR 496[rsp], rsi
	punpcklqdq	xmm0, xmm2
	mov	QWORD PTR 112[rsp], rdx
	movaps	XMMWORD PTR 144[rsp], xmm0
	pxor	xmm0, xmm0
	punpcklqdq	xmm0, xmm3
	mov	QWORD PTR 504[rsp], 0
	mov	BYTE PTR 512[rsp], 0
	mov	QWORD PTR 96[rsp], 209
	mov	QWORD PTR 120[rsp], 0
	mov	BYTE PTR 128[rsp], 0
	mov	DWORD PTR 168[rsp], 0
	movaps	XMMWORD PTR 192[rsp], xmm0
.LEHB4:
	call	_ZNSt8__format8_ScannerIcE7_M_scanEv
.LEHE4:
	cmp	BYTE PTR 128[rsp], 0
	jne	.L371
	mov	r9, QWORD PTR 216[rsp]
	mov	r8, QWORD PTR 232[rsp]
	cmp	r9, r8
	je	.L345
.L344:
	mov	rdx, QWORD PTR 504[rsp]
	sub	r8, r9
	movabs	rax, 9223372036854775806
	sub	rax, rdx
	cmp	rax, r8
	jb	.L368
	mov	rcx, QWORD PTR 496[rsp]
	mov	eax, 15
	lea	r10, [r8+rdx]
	cmp	rcx, rsi
	cmovne	rax, QWORD PTR 512[rsp]
	cmp	rax, r10
	jb	.L351
	add	rcx, rdx
	cmp	r8, 1
	je	.L372
	mov	rdx, r9
	mov	QWORD PTR 56[rsp], r10
	call	memcpy
	mov	r10, QWORD PTR 56[rsp]
.L353:
	mov	rax, QWORD PTR 496[rsp]
	mov	QWORD PTR 504[rsp], r10
	mov	BYTE PTR [rax+r10], 0
.L345:
	mov	rdx, QWORD PTR 496[rsp]
	lea	rax, 160[rsp]
	mov	QWORD PTR 144[rsp], rax
	cmp	rdx, rsi
	je	.L373
	mov	rax, QWORD PTR 512[rsp]
	mov	QWORD PTR 144[rsp], rdx
	mov	r8, QWORD PTR 504[rsp]
	mov	QWORD PTR 160[rsp], rax
.L355:
	lea	rcx, .LC17[rip]
	mov	QWORD PTR 152[rsp], r8
.LEHB5:
	call	__mingw_printf
.LEHE5:
	mov	rcx, rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	xor	eax, eax
	add	rsp, 528
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L371:
	lea	rcx, 120[rsp]
	call	_ZNSt6localeD1Ev
	mov	r9, QWORD PTR 216[rsp]
	mov	r8, QWORD PTR 232[rsp]
	cmp	r9, r8
	jne	.L344
	jmp	.L345
.L351:
	mov	QWORD PTR 32[rsp], r8
	lea	rcx, 496[rsp]
	xor	r8d, r8d
	lea	rdi, 496[rsp]
	mov	QWORD PTR 56[rsp], r10
.LEHB6:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE6:
	mov	r10, QWORD PTR 56[rsp]
	jmp	.L353
.L373:
	mov	r8, QWORD PTR 504[rsp]
	mov	rdi, rax
	lea	rdx, 160[rsp]
	lea	ecx, 1[r8]
	rep movsb
	jmp	.L355
.L372:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	jmp	.L353
.L366:
	jmp	.L367
.L365:
	mov	rbx, rax
	jmp	.L346
.L363:
	mov	rsi, rax
	jmp	.L357
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3986:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3986-.LLSDACSB3986
.LLSDACSB3986:
	.uleb128 .LEHB4-.LFB3986
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L365-.LFB3986
	.uleb128 0
	.uleb128 .LEHB5-.LFB3986
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L363-.LFB3986
	.uleb128 0
	.uleb128 .LEHB6-.LFB3986
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L366-.LFB3986
	.uleb128 0
.LLSDACSE3986:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	552
	.seh_savereg	rbx, 528
	.seh_savereg	rsi, 536
	.seh_savereg	rdi, 544
	.seh_endprologue
main.cold:
.L368:
	lea	rcx, .LC14[rip]
	lea	rdi, 496[rsp]
.LEHB7:
	call	_ZSt20__throw_length_errorPKc
.LEHE7:
.L364:
.L367:
	mov	rbx, rax
.L348:
	lea	rax, _ZTVNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE[rip+16]
	mov	rcx, rdi
	mov	QWORD PTR 208[rsp], rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB8:
	call	_Unwind_Resume
.L346:
	cmp	BYTE PTR 128[rsp], 0
	je	.L347
	lea	rcx, 120[rsp]
	call	_ZNSt6localeD1Ev
.L347:
	lea	rdi, 496[rsp]
	jmp	.L348
.L357:
	mov	rcx, rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE8:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC3986:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC3986-.LLSDACSBC3986
.LLSDACSBC3986:
	.uleb128 .LEHB7-.LCOLDB19
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L364-.LCOLDB19
	.uleb128 0
	.uleb128 .LEHB8-.LCOLDB19
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
.LLSDACSEC3986:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE19:
	.section	.text.startup,"x"
.LHOTE19:
	.section .rdata,"dr"
.LC20:
	.ascii "basic_string::_M_replace_aux\0"
	.section	.text$_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE7_M_bumpEy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE7_M_bumpEy
	.def	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE7_M_bumpEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE7_M_bumpEy
_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE7_M_bumpEy:
.LFB5376:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	r11, QWORD PTR 24[rcx]
	mov	rax, QWORD PTR 296[rcx]
	sub	r11, QWORD PTR 8[rcx]
	add	r11, rdx
	mov	r10, rcx
	cmp	rax, r11
	jb	.L384
	cmp	r11, rax
	jnb	.L381
.L383:
	mov	rax, QWORD PTR 288[r10]
	mov	QWORD PTR 296[r10], r11
	mov	BYTE PTR [rax+r11], 0
.L381:
	lea	rax, 32[r10]
	mov	QWORD PTR 16[r10], 256
	mov	QWORD PTR 8[r10], rax
	mov	QWORD PTR 24[r10], rax
	add	rsp, 64
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L384:
	movabs	rdx, 9223372036854775806
	mov	rcx, r11
	sub	rcx, rax
	sub	rdx, rax
	mov	rbx, rcx
	cmp	rdx, rcx
	jb	.L385
	mov	rcx, QWORD PTR 288[r10]
	lea	rdx, 304[r10]
	cmp	rcx, rdx
	je	.L382
	mov	rdx, QWORD PTR 304[r10]
.L377:
	cmp	rdx, r11
	jb	.L386
.L378:
	add	rcx, rax
	cmp	rbx, 1
	je	.L387
	mov	r8, rbx
	xor	edx, edx
	mov	QWORD PTR 80[rsp], r10
	mov	QWORD PTR 48[rsp], r11
	call	memset
	mov	r10, QWORD PTR 80[rsp]
	mov	r11, QWORD PTR 48[rsp]
	jmp	.L383
	.p2align 4,,10
	.p2align 3
.L387:
	mov	BYTE PTR [rcx], 0
	jmp	.L383
	.p2align 4,,10
	.p2align 3
.L386:
	mov	QWORD PTR 32[rsp], rbx
	mov	rdx, rax
	xor	r9d, r9d
	xor	r8d, r8d
	lea	rcx, 288[r10]
	mov	QWORD PTR 56[rsp], r11
	mov	QWORD PTR 80[rsp], r10
	mov	QWORD PTR 48[rsp], rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	r10, QWORD PTR 80[rsp]
	mov	r11, QWORD PTR 56[rsp]
	mov	rax, QWORD PTR 48[rsp]
	mov	rcx, QWORD PTR 288[r10]
	jmp	.L378
	.p2align 4,,10
	.p2align 3
.L382:
	mov	edx, 15
	jmp	.L377
.L385:
	lea	rcx, .LC20[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE10_M_reserveEy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE10_M_reserveEy
	.def	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE10_M_reserveEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE10_M_reserveEy
_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE10_M_reserveEy:
.LFB5360:
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
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	r9, QWORD PTR 8[rcx]
	mov	r8, QWORD PTR 24[rcx]
	mov	rbp, QWORD PTR 296[rcx]
	mov	rbx, rcx
	mov	rsi, rdx
	lea	r13, 304[rcx]
	cmp	r8, r9
	jne	.L418
.L389:
	mov	rdi, QWORD PTR 288[rbx]
	add	rsi, rbp
	cmp	rdi, r13
	je	.L419
	mov	rdx, QWORD PTR 304[rbx]
	cmp	rdx, rsi
	jb	.L420
.L396:
	mov	QWORD PTR 296[rbx], rsi
	mov	BYTE PTR [rdi+rsi], 0
	mov	rax, QWORD PTR 288[rbx]
	mov	rdx, QWORD PTR 296[rbx]
	mov	QWORD PTR 8[rbx], rax
	add	rax, rbp
	mov	QWORD PTR 24[rbx], rax
	mov	rax, rbx
	mov	QWORD PTR 16[rbx], rdx
	add	rsp, 64
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
.L420:
	movabs	r9, 9223372036854775806
	cmp	r9, rsi
	jb	.L397
	lea	rax, [rdx+rdx]
	mov	r14, rax
	cmp	rsi, rax
	jb	.L401
.L399:
	lea	rcx, 1[rsi]
	mov	r14, rsi
.L402:
	call	_Znwy
	lea	r8, 1[rbp]
	mov	r12, rax
	test	rbp, rbp
	je	.L421
	mov	rdx, rdi
	mov	rcx, rax
	call	memcpy
	cmp	rdi, r13
	je	.L417
.L415:
	mov	rdx, QWORD PTR 304[rbx]
.L409:
	add	rdx, 1
	mov	rcx, rdi
	call	_ZdlPvy
.L417:
	mov	QWORD PTR 288[rbx], r12
	mov	rdi, r12
	mov	QWORD PTR 304[rbx], r14
	jmp	.L396
	.p2align 4,,10
	.p2align 3
.L401:
	lea	rcx, 1[rax]
	cmp	r9, rax
	jnb	.L402
	movabs	rcx, 9223372036854775807
	mov	QWORD PTR 56[rsp], rdx
	call	_Znwy
	test	rbp, rbp
	mov	rdx, QWORD PTR 56[rsp]
	mov	r12, rax
	je	.L410
	lea	r8, 1[rbp]
	mov	rdx, rdi
	mov	rcx, rax
	movabs	r14, 9223372036854775806
	call	memcpy
	jmp	.L415
	.p2align 4,,10
	.p2align 3
.L419:
	cmp	rsi, 15
	jbe	.L396
	movabs	rax, 9223372036854775806
	cmp	rax, rsi
	jb	.L397
	cmp	rsi, 29
	ja	.L399
	mov	ecx, 31
	mov	r14d, 30
	jmp	.L402
	.p2align 4,,10
	.p2align 3
.L421:
	movzx	eax, BYTE PTR [rdi]
	mov	BYTE PTR [r12], al
	cmp	rdi, r13
	jne	.L415
	jmp	.L417
	.p2align 4,,10
	.p2align 3
.L418:
	movabs	rax, 9223372036854775806
	sub	r8, r9
	sub	rax, rbp
	cmp	rax, r8
	jb	.L422
	mov	rcx, QWORD PTR 288[rcx]
	cmp	rcx, r13
	je	.L411
	mov	rax, QWORD PTR 304[rbx]
.L391:
	lea	rdi, 0[rbp+r8]
	cmp	rax, rdi
	jb	.L392
	add	rcx, rbp
	cmp	r8, 1
	je	.L423
	mov	rdx, r9
	call	memcpy
.L394:
	mov	rax, QWORD PTR 288[rbx]
	mov	QWORD PTR 296[rbx], rdi
	mov	BYTE PTR [rax+rdi], 0
	mov	rax, QWORD PTR 8[rbx]
	mov	rbp, QWORD PTR 296[rbx]
	mov	QWORD PTR 24[rbx], rax
	jmp	.L389
	.p2align 4,,10
	.p2align 3
.L410:
	movabs	r14, 9223372036854775806
	movzx	eax, BYTE PTR [rdi]
	mov	BYTE PTR [r12], al
	jmp	.L409
	.p2align 4,,10
	.p2align 3
.L423:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	jmp	.L394
	.p2align 4,,10
	.p2align 3
.L392:
	mov	QWORD PTR 32[rsp], r8
	lea	rcx, 288[rbx]
	xor	r8d, r8d
	mov	rdx, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	jmp	.L394
	.p2align 4,,10
	.p2align 3
.L411:
	mov	eax, 15
	jmp	.L391
.L397:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L422:
	lea	rcx, .LC14[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	.def	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev:
.LFB5079:
	.seh_endprologue
	mov	r8, QWORD PTR 16[rcx]
	mov	rax, rcx
	lea	rcx, 1[r8]
	mov	QWORD PTR 16[rax], rcx
	movsx	edx, BYTE PTR [r8]
	test	dl, dl
	js	.L425
	mov	ecx, 1
.L426:
	mov	DWORD PTR [rax], edx
	mov	edx, 256
	mov	BYTE PTR 26[rax], cl
	mov	WORD PTR 24[rax], dx
	mov	QWORD PTR 16[rax], r8
	ret
	.p2align 4,,10
	.p2align 3
.L425:
	cmp	dl, -63
	jbe	.L442
	mov	r9, QWORD PTR 32[rax]
	cmp	rcx, r9
	je	.L442
	cmp	dl, -33
	jbe	.L445
	cmp	dl, -17
	ja	.L428
	cmp	dl, -32
	je	.L436
	cmp	dl, -19
	mov	r10d, -65
	mov	ecx, -97
	mov	r11d, -128
	cmove	r10d, ecx
.L429:
	movzx	ecx, BYTE PTR 1[r8]
	cmp	cl, r11b
	jb	.L442
	cmp	r10b, cl
	jb	.L442
	lea	r10, 2[r8]
	mov	QWORD PTR 16[rax], r10
	cmp	r9, r10
	je	.L431
	movzx	r9d, BYTE PTR 2[r8]
	lea	r10d, -128[r9]
	cmp	r10b, 63
	ja	.L431
	and	edx, 15
	and	ecx, 63
	and	r9d, 63
	sal	edx, 6
	or	ecx, edx
	mov	edx, r9d
	sal	ecx, 6
	or	edx, ecx
	mov	ecx, 3
	jmp	.L426
	.p2align 4,,10
	.p2align 3
.L445:
	movzx	ecx, BYTE PTR 1[r8]
	lea	r9d, -128[rcx]
	cmp	r9b, 63
	ja	.L442
	and	edx, 31
	and	ecx, 63
	sal	edx, 6
	or	edx, ecx
	mov	ecx, 2
	jmp	.L426
	.p2align 4,,10
	.p2align 3
.L442:
	mov	ecx, 1
	mov	edx, 65533
	jmp	.L426
	.p2align 4,,10
	.p2align 3
.L428:
	cmp	dl, -12
	ja	.L442
	cmp	dl, -16
	je	.L440
	cmp	dl, -12
	mov	r10d, -65
	mov	ecx, -113
	mov	r11d, -128
	cmove	r10d, ecx
.L432:
	movzx	ecx, BYTE PTR 1[r8]
	cmp	cl, r11b
	jb	.L442
	cmp	r10b, cl
	jb	.L442
	lea	r10, 2[r8]
	mov	QWORD PTR 16[rax], r10
	cmp	r9, r10
	je	.L431
	movzx	r10d, BYTE PTR 2[r8]
	lea	r11d, -128[r10]
	cmp	r11b, 63
	ja	.L431
	lea	r11, 3[r8]
	mov	QWORD PTR 16[rax], r11
	cmp	r9, r11
	je	.L444
	movzx	r9d, BYTE PTR 3[r8]
	lea	r11d, -128[r9]
	cmp	r11b, 63
	ja	.L444
	and	edx, 7
	and	ecx, 63
	and	r10d, 63
	and	r9d, 63
	sal	edx, 6
	or	ecx, edx
	mov	edx, r9d
	sal	ecx, 6
	or	r10d, ecx
	mov	ecx, 4
	sal	r10d, 6
	or	edx, r10d
	jmp	.L426
.L436:
	mov	r11d, -96
	mov	r10d, -65
	jmp	.L429
.L431:
	mov	ecx, 2
	mov	edx, 65533
	jmp	.L426
.L440:
	mov	r11d, -112
	mov	r10d, -65
	jmp	.L432
.L444:
	mov	ecx, 3
	mov	edx, 65533
	jmp	.L426
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC22:
	.ascii "format error: width must be non-zero in format string\0"
	.section	.text$_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	.def	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE:
.LFB3982:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 184
	.seh_stackalloc	184
	.seh_endprologue
	movdqu	xmm0, XMMWORD PTR [rdx]
	mov	rsi, QWORD PTR 8[rdx]
	movq	rbx, xmm0
	mov	edi, r8d
	mov	r11, rcx
	mov	r10d, r8d
	mov	QWORD PTR 68[rsp], 0
	and	edi, 15
	cmp	rsi, rbx
	je	.L447
	movzx	eax, BYTE PTR [rbx]
	cmp	al, 125
	je	.L447
	cmp	al, 123
	je	.L450
	mov	QWORD PTR 248[rsp], rdx
	punpcklqdq	xmm0, xmm0
	xor	edx, edx
	mov	QWORD PTR 240[rsp], rcx
	lea	rcx, 80[rsp]
	mov	DWORD PTR 256[rsp], r8d
	mov	rbp, rcx
	mov	WORD PTR 104[rsp], dx
	mov	BYTE PTR 63[rsp], al
	mov	BYTE PTR 106[rsp], 0
	mov	QWORD PTR 112[rsp], rsi
	movups	XMMWORD PTR 88[rsp], xmm0
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	movzx	eax, BYTE PTR 104[rsp]
	mov	rcx, QWORD PTR 112[rsp]
	movzx	r9d, BYTE PTR 105[rsp]
	movdqa	xmm1, XMMWORD PTR 80[rsp]
	mov	QWORD PTR 160[rsp], rcx
	movzx	ecx, al
	mov	r14d, eax
	mov	r8, QWORD PTR 96[rsp]
	movdqa	xmm2, XMMWORD PTR 96[rsp]
	add	ecx, 1
	movzx	r15d, BYTE PTR 106[rsp]
	movaps	XMMWORD PTR 128[rsp], xmm1
	cmp	ecx, r9d
	mov	r11, QWORD PTR 240[rsp]
	mov	rdx, QWORD PTR 248[rsp]
	mov	r10d, DWORD PTR 256[rsp]
	movzx	eax, BYTE PTR 63[rsp]
	movaps	XMMWORD PTR 144[rsp], xmm2
	je	.L534
.L451:
	movzx	ecx, r14b
	mov	r9d, DWORD PTR 128[rsp+rcx*4]
	cmp	r9d, 55295
	ja	.L535
.L454:
	cmp	rsi, r8
	je	.L458
	movzx	ecx, BYTE PTR [r8]
	cmp	cl, 62
	je	.L497
	cmp	cl, 94
	je	.L498
	mov	r14d, 1
	cmp	cl, 60
	jne	.L458
.L457:
	lea	rbx, 1[r8]
	jmp	.L459
	.p2align 4,,10
	.p2align 3
.L447:
	movzx	eax, BYTE PTR 69[rsp]
	sal	edi, 3
	mov	DWORD PTR 76[rsp], 32
	and	eax, -121
	or	eax, edi
	mov	BYTE PTR 69[rsp], al
.L449:
	mov	rax, QWORD PTR 68[rsp]
	mov	QWORD PTR [r11], rax
	mov	eax, DWORD PTR 76[rsp]
	mov	DWORD PTR 8[r11], eax
	mov	rax, rbx
	add	rsp, 184
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L458:
	cmp	al, 62
	je	.L460
	cmp	al, 94
	je	.L461
	cmp	al, 60
	je	.L462
	.p2align 4
	.p2align 3
.L450:
	xor	r14d, r14d
	mov	r9d, 32
.L463:
	movzx	eax, BYTE PTR [rbx]
	cmp	al, 125
	je	.L465
.L466:
	lea	ecx, -32[rax]
	cmp	cl, 13
	ja	.L499
	movzx	ecx, cl
	lea	r8, CSWTCH.641[rip]
	mov	r8d, DWORD PTR [r8+rcx*4]
	test	r8d, r8d
	jne	.L468
	xor	ecx, ecx
	cmp	al, 35
	je	.L536
.L470:
	mov	BYTE PTR 128[rsp], 0
	xor	r15d, r15d
.L475:
	movzx	eax, cl
	movzx	ecx, r14b
	mov	QWORD PTR 32[rsp], rdx
	mov	rdx, rsi
	sal	eax, 2
	mov	DWORD PTR 76[rsp], r9d
	lea	r9, 128[rsp]
	or	eax, ecx
	movzx	ecx, r8b
	movzx	r8d, r15b
	mov	QWORD PTR 240[rsp], r11
	sal	ecx, 4
	sal	r8d, 6
	mov	DWORD PTR 256[rsp], r10d
	or	eax, ecx
	mov	ecx, r10d
	and	ecx, 15
	or	eax, r8d
	lea	r8, 72[rsp]
	sal	ecx, 11
	or	eax, ecx
	movzx	ecx, WORD PTR 68[rsp]
	and	cx, -31232
	or	eax, ecx
	mov	rcx, rbx
	mov	WORD PTR 68[rsp], ax
	call	_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE
	mov	r10d, DWORD PTR 256[rsp]
	mov	r11, QWORD PTR 240[rsp]
	mov	rdx, rax
	xor	eax, eax
	cmp	rbx, rdx
	je	.L478
	movzx	eax, BYTE PTR 128[rsp]
	add	eax, 1
	and	eax, 3
.L478:
	cmp	rsi, rdx
	je	.L479
	movzx	ecx, BYTE PTR [rdx]
	cmp	cl, 125
	je	.L479
	xor	r8d, r8d
	cmp	cl, 76
	je	.L537
.L481:
	sub	ecx, 63
	cmp	cl, 57
	ja	.L495
	lea	r9, .L496[rip]
	movzx	ecx, cl
	movsxd	rcx, DWORD PTR [r9+rcx*4]
	add	rcx, r9
	jmp	rcx
	.section .rdata,"dr"
	.align 4
.L496:
	.long	.L493-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L485-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L491-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L483-.L496
	.long	.L486-.L496
	.long	.L488-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L489-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L492-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L495-.L496
	.long	.L490-.L496
	.section	.text$_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L499:
	xor	r8d, r8d
	xor	ecx, ecx
.L467:
	cmp	al, 48
	jne	.L470
	lea	rax, 1[rbx]
	mov	r15, rax
	cmp	rsi, rax
	jne	.L538
.L476:
	movzx	eax, cl
	movzx	edx, r14b
	movzx	ecx, r8b
	sal	eax, 2
	or	edx, 64
	sal	ecx, 4
	or	eax, edx
	or	eax, ecx
	jmp	.L533
	.p2align 4,,10
	.p2align 3
.L462:
	mov	r14d, 1
.L464:
	add	rbx, 1
	mov	r9d, 32
.L459:
	cmp	rsi, rbx
	jne	.L463
.L465:
	and	r10d, 15
	movzx	eax, r14b
	mov	DWORD PTR 76[rsp], r9d
	sal	r10d, 11
	or	r10d, eax
	movzx	eax, WORD PTR 68[rsp]
	and	ax, -31232
	or	r10d, eax
	mov	WORD PTR 68[rsp], r10w
	jmp	.L449
	.p2align 4,,10
	.p2align 3
.L468:
	mov	ecx, r8d
	lea	rax, 1[rbx]
	and	ecx, 3
	mov	r15, rax
	cmp	rsi, rax
	jne	.L539
.L471:
	and	r8d, 3
	movzx	edx, r14b
	lea	eax, 0[0+r8*4]
	or	eax, edx
.L533:
	movzx	edx, WORD PTR 68[rsp]
	and	r10d, 15
	mov	DWORD PTR 76[rsp], r9d
	mov	rbx, r15
	sal	r10d, 11
	or	eax, r10d
	and	dx, -31232
	or	eax, edx
	mov	WORD PTR 68[rsp], ax
	jmp	.L449
	.p2align 4,,10
	.p2align 3
.L534:
	cmp	rsi, r8
	je	.L453
	movzx	ecx, r15b
	add	rcx, r8
	cmp	rsi, rcx
	je	.L453
	mov	QWORD PTR 96[rsp], rcx
	mov	rcx, rbp
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	r8, QWORD PTR 96[rsp]
	mov	r10d, DWORD PTR 256[rsp]
	mov	rdx, QWORD PTR 248[rsp]
	mov	r11, QWORD PTR 240[rsp]
	movzx	eax, BYTE PTR 63[rsp]
	jmp	.L451
.L498:
	mov	r14d, 3
	jmp	.L457
.L479:
	movzx	ecx, WORD PTR 68[rsp]
	and	eax, 3
	mov	rbx, rdx
	sal	eax, 7
	and	cx, -385
	or	eax, ecx
	mov	WORD PTR 68[rsp], ax
	jmp	.L449
.L541:
	mov	rdx, rbx
.L495:
	cmp	BYTE PTR [rdx], 125
	je	.L540
.L487:
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L489:
	lea	rbx, 1[rdx]
	mov	edi, 4
.L484:
	cmp	rsi, rbx
	jne	.L541
.L494:
	movzx	eax, al
	movzx	edx, r8b
	sal	edi, 11
	sal	edx, 5
	sal	eax, 7
	or	eax, edx
	movzx	edx, WORD PTR 68[rsp]
	or	eax, edi
	and	ax, 31136
	and	dx, -31137
	or	eax, edx
	mov	WORD PTR 68[rsp], ax
	jmp	.L449
.L490:
	lea	rbx, 1[rdx]
	mov	edi, 5
	jmp	.L484
.L488:
	lea	rbx, 1[rdx]
	mov	edi, 1
	jmp	.L484
.L483:
	lea	rbx, 1[rdx]
	mov	edi, 2
	jmp	.L484
.L491:
	lea	rbx, 1[rdx]
	mov	edi, 6
	jmp	.L484
.L485:
	lea	rbx, 1[rdx]
	mov	edi, 3
	jmp	.L484
.L492:
	test	r10d, r10d
	jne	.L487
	lea	rbx, 1[rdx]
	xor	edi, edi
	jmp	.L484
.L486:
	test	r10d, r10d
	je	.L487
	lea	rbx, 1[rdx]
	mov	edi, 7
	jmp	.L484
.L493:
	cmp	r10d, 7
	jne	.L487
	lea	rbx, 1[rdx]
	mov	edi, 15
	jmp	.L484
	.p2align 4,,10
	.p2align 3
.L461:
	mov	r14d, 3
	jmp	.L464
	.p2align 4,,10
	.p2align 3
.L460:
	mov	r14d, 2
	jmp	.L464
.L536:
	mov	r15, rbx
	xor	ecx, ecx
.L469:
	lea	rbx, 1[r15]
	cmp	rsi, rbx
	jne	.L542
.L473:
	movzx	eax, cl
	movzx	edx, r14b
	and	r10d, 15
	mov	DWORD PTR 76[rsp], r9d
	sal	eax, 2
	or	edx, 16
	sal	r10d, 11
	or	eax, edx
	movzx	edx, WORD PTR 68[rsp]
	or	eax, r10d
	and	dx, -31232
	or	eax, edx
	mov	WORD PTR 68[rsp], ax
	jmp	.L449
.L542:
	movzx	eax, BYTE PTR 1[r15]
	mov	r8d, 1
	cmp	al, 125
	jne	.L467
	jmp	.L473
.L453:
	movzx	ecx, r14b
	mov	ecx, DWORD PTR 128[rsp+rcx*4]
	cmp	ecx, 55295
	jbe	.L458
	sub	ecx, 57344
	cmp	ecx, 1056767
	jbe	.L458
.L455:
	cmp	al, 62
	je	.L460
	cmp	al, 94
	je	.L461
	cmp	al, 60
	je	.L462
	mov	r9d, 32
	xor	r14d, r14d
	jmp	.L466
	.p2align 4,,10
	.p2align 3
.L497:
	mov	r14d, 2
	jmp	.L457
.L538:
	movzx	eax, BYTE PTR 1[rbx]
	cmp	al, 125
	je	.L476
	mov	BYTE PTR 128[rsp], 0
	cmp	al, 48
	je	.L543
	mov	rbx, r15
	mov	r15d, 1
	jmp	.L475
.L537:
	lea	rbx, 1[rdx]
	cmp	rsi, rbx
	jne	.L544
.L482:
	or	BYTE PTR 68[rsp], 32
	movzx	edx, WORD PTR 68[rsp]
	and	eax, 3
	sal	eax, 7
	and	dx, -385
	or	eax, edx
	mov	WORD PTR 68[rsp], ax
	jmp	.L449
.L535:
	lea	ecx, -57344[r9]
	cmp	ecx, 1056767
	ja	.L455
	jmp	.L454
.L544:
	movzx	ecx, BYTE PTR 1[rdx]
	cmp	cl, 125
	je	.L482
	mov	rdx, rbx
	mov	r8d, 1
	jmp	.L481
	.p2align 4,,10
	.p2align 3
.L540:
	mov	rbx, rdx
	jmp	.L494
.L539:
	movzx	eax, BYTE PTR 1[rbx]
	cmp	al, 125
	je	.L471
	cmp	al, 35
	je	.L469
	mov	rbx, r15
	xor	r8d, r8d
	jmp	.L467
.L543:
	lea	rcx, .LC22[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE
	.def	_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE
_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE:
.LFB5446:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 192
	.seh_stackalloc	192
	.seh_endprologue
	movdqu	xmm0, XMMWORD PTR [rdx]
	mov	rbx, QWORD PTR 8[rdx]
	movq	r10, xmm0
	mov	QWORD PTR 84[rsp], 0
	mov	r11, rcx
	cmp	rbx, r10
	je	.L546
	movzx	eax, BYTE PTR [r10]
	cmp	al, 125
	je	.L546
	cmp	al, 123
	je	.L549
	mov	QWORD PTR 232[rsp], rdx
	xor	edx, edx
	mov	QWORD PTR 224[rsp], rcx
	lea	rcx, 96[rsp]
	movq	QWORD PTR 56[rsp], xmm0
	punpcklqdq	xmm0, xmm0
	mov	rdi, rcx
	mov	WORD PTR 120[rsp], dx
	mov	BYTE PTR 71[rsp], al
	mov	BYTE PTR 122[rsp], 0
	mov	QWORD PTR 128[rsp], rbx
	movups	XMMWORD PTR 104[rsp], xmm0
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	movzx	r8d, BYTE PTR 120[rsp]
	mov	r9, QWORD PTR 112[rsp]
	mov	rcx, QWORD PTR 128[rsp]
	movdqa	xmm1, XMMWORD PTR 96[rsp]
	movdqa	xmm2, XMMWORD PTR 112[rsp]
	movzx	esi, BYTE PTR 122[rsp]
	mov	QWORD PTR 176[rsp], rcx
	movzx	ecx, r8b
	mov	r10, QWORD PTR 56[rsp]
	lea	eax, 1[rcx]
	movzx	ecx, BYTE PTR 121[rsp]
	mov	r11, QWORD PTR 224[rsp]
	movaps	XMMWORD PTR 144[rsp], xmm1
	mov	rdx, QWORD PTR 232[rsp]
	movaps	XMMWORD PTR 160[rsp], xmm2
	cmp	eax, ecx
	movzx	eax, BYTE PTR 71[rsp]
	je	.L606
.L550:
	mov	r8d, DWORD PTR 144[rsp+r8*4]
	cmp	r8d, 55295
	ja	.L607
.L553:
	cmp	rbx, r9
	je	.L557
	movzx	ecx, BYTE PTR [r9]
	cmp	cl, 62
	je	.L576
	cmp	cl, 94
	je	.L577
	cmp	cl, 60
	jne	.L557
	mov	ecx, 1
.L556:
	lea	r10, 1[r9]
	jmp	.L558
	.p2align 4,,10
	.p2align 3
.L546:
	mov	DWORD PTR 92[rsp], 32
.L548:
	mov	rax, QWORD PTR 84[rsp]
	mov	QWORD PTR [r11], rax
	mov	eax, DWORD PTR 92[rsp]
	mov	DWORD PTR 8[r11], eax
	mov	rax, r10
	add	rsp, 192
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L557:
	cmp	al, 62
	je	.L559
	cmp	al, 94
	je	.L560
	cmp	al, 60
	je	.L561
	.p2align 4
	.p2align 3
.L549:
	mov	r8d, 32
	xor	ecx, ecx
.L562:
	movzx	eax, BYTE PTR [r10]
	cmp	al, 125
	je	.L564
.L565:
	cmp	al, 48
	je	.L566
	mov	BYTE PTR 144[rsp], 0
	xor	eax, eax
.L567:
	sal	eax, 6
	mov	QWORD PTR 32[rsp], rdx
	lea	r9, 144[rsp]
	mov	rdx, rbx
	or	eax, ecx
	movzx	ecx, WORD PTR 84[rsp]
	mov	DWORD PTR 92[rsp], r8d
	lea	r8, 88[rsp]
	mov	QWORD PTR 224[rsp], r11
	and	cx, -31172
	mov	QWORD PTR 56[rsp], r10
	or	eax, ecx
	mov	rcx, r10
	mov	WORD PTR 84[rsp], ax
	call	_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE
	xor	edx, edx
	cmp	QWORD PTR 56[rsp], rax
	mov	r11, QWORD PTR 224[rsp]
	je	.L570
	movzx	edx, BYTE PTR 144[rsp]
	add	edx, 1
	and	edx, 3
.L570:
	cmp	rbx, rax
	je	.L580
	movzx	r8d, BYTE PTR [rax]
	lea	r9, 1[rax]
	xor	ecx, ecx
	cmp	r8b, 112
	je	.L573
	xor	ecx, ecx
	cmp	r8b, 80
	jne	.L574
	lea	r9, 1[rax]
	mov	ecx, 1
.L573:
	cmp	rbx, r9
	je	.L582
	movzx	r8d, BYTE PTR 1[rax]
	mov	rax, r9
.L574:
	cmp	r8b, 125
	je	.L571
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L561:
	mov	ecx, 1
.L563:
	add	r10, 1
	mov	r8d, 32
.L558:
	cmp	rbx, r10
	jne	.L562
.L564:
	movzx	eax, WORD PTR 84[rsp]
	and	ecx, 3
	mov	DWORD PTR 92[rsp], r8d
	and	ax, -31172
	or	eax, ecx
	mov	WORD PTR 84[rsp], ax
	jmp	.L548
	.p2align 4,,10
	.p2align 3
.L566:
	lea	r9, 1[r10]
	cmp	rbx, r9
	jne	.L608
.L568:
	movzx	eax, WORD PTR 84[rsp]
	or	ecx, 64
	mov	DWORD PTR 92[rsp], r8d
	mov	r10, r9
	and	ax, -31172
	or	eax, ecx
	mov	WORD PTR 84[rsp], ax
	jmp	.L548
	.p2align 4,,10
	.p2align 3
.L608:
	movzx	eax, BYTE PTR 1[r10]
	cmp	al, 125
	je	.L568
	cmp	al, 48
	mov	BYTE PTR 144[rsp], 0
	mov	r10, r9
	mov	eax, 1
	jne	.L567
	lea	rcx, .LC22[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L606:
	cmp	rbx, r9
	je	.L552
	movzx	ecx, sil
	add	rcx, r9
	cmp	rbx, rcx
	je	.L552
	mov	QWORD PTR 112[rsp], rcx
	mov	rcx, rdi
	mov	QWORD PTR 72[rsp], r10
	mov	BYTE PTR 71[rsp], r8b
	mov	BYTE PTR 56[rsp], al
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	r9, QWORD PTR 112[rsp]
	mov	r10, QWORD PTR 72[rsp]
	mov	rdx, QWORD PTR 232[rsp]
	mov	r11, QWORD PTR 224[rsp]
	movzx	r8d, BYTE PTR 71[rsp]
	movzx	eax, BYTE PTR 56[rsp]
	jmp	.L550
.L577:
	mov	ecx, 3
	jmp	.L556
	.p2align 4,,10
	.p2align 3
.L560:
	mov	ecx, 3
	jmp	.L563
	.p2align 4,,10
	.p2align 3
.L559:
	mov	ecx, 2
	jmp	.L563
.L580:
	xor	ecx, ecx
.L571:
	movzx	edx, dl
	sal	ecx, 11
	mov	r10, rax
	sal	edx, 7
	or	edx, ecx
	movzx	ecx, WORD PTR 84[rsp]
	and	dx, 31104
	and	cx, -31105
	or	edx, ecx
	mov	WORD PTR 84[rsp], dx
	jmp	.L548
.L552:
	mov	ecx, DWORD PTR 144[rsp+r8*4]
	cmp	ecx, 55295
	jbe	.L557
	sub	ecx, 57344
	cmp	ecx, 1056767
	jbe	.L557
.L554:
	cmp	al, 62
	je	.L559
	cmp	al, 94
	je	.L560
	cmp	al, 60
	je	.L561
	xor	ecx, ecx
	mov	r8d, 32
	jmp	.L565
	.p2align 4,,10
	.p2align 3
.L576:
	mov	ecx, 2
	jmp	.L556
.L607:
	lea	ecx, -57344[r8]
	cmp	ecx, 1056767
	ja	.L554
	jmp	.L553
.L582:
	mov	rax, rbx
	jmp	.L571
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC23:
	.ascii "format error: missing precision after '.' in format string\0"
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	.def	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE:
.LFB5600:
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
	sub	rsp, 216
	.seh_stackalloc	216
	.seh_endprologue
	mov	QWORD PTR 100[rsp], 0
	mov	r11, rdx
	mov	rdx, QWORD PTR 8[rdx]
	mov	rbx, rcx
	movdqu	xmm0, XMMWORD PTR [r11]
	movq	r10, xmm0
	cmp	rdx, r10
	je	.L610
	movzx	eax, BYTE PTR [r10]
	cmp	al, 125
	je	.L610
	cmp	al, 123
	je	.L613
	xor	ecx, ecx
	movq	QWORD PTR 64[rsp], xmm0
	punpcklqdq	xmm0, xmm0
	mov	WORD PTR 136[rsp], cx
	lea	rcx, 112[rsp]
	mov	QWORD PTR 296[rsp], r11
	mov	rsi, rcx
	mov	QWORD PTR 144[rsp], rdx
	mov	QWORD PTR 56[rsp], rdx
	mov	BYTE PTR 78[rsp], al
	mov	BYTE PTR 138[rsp], 0
	movups	XMMWORD PTR 120[rsp], xmm0
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	movdqa	xmm1, XMMWORD PTR 112[rsp]
	mov	rcx, QWORD PTR 144[rsp]
	movzx	r8d, BYTE PTR 136[rsp]
	mov	r9, QWORD PTR 128[rsp]
	mov	QWORD PTR 192[rsp], rcx
	movzx	edi, BYTE PTR 138[rsp]
	movzx	ecx, r8b
	mov	rdx, QWORD PTR 56[rsp]
	movdqa	xmm2, XMMWORD PTR 128[rsp]
	movaps	XMMWORD PTR 160[rsp], xmm1
	lea	eax, 1[rcx]
	movzx	ecx, BYTE PTR 137[rsp]
	mov	r10, QWORD PTR 64[rsp]
	mov	r11, QWORD PTR 296[rsp]
	movaps	XMMWORD PTR 176[rsp], xmm2
	cmp	eax, ecx
	movzx	eax, BYTE PTR 78[rsp]
	je	.L715
.L614:
	mov	ecx, DWORD PTR 160[rsp+r8*4]
	mov	esi, ecx
	cmp	ecx, 55295
	ja	.L716
.L617:
	cmp	rdx, r9
	je	.L621
	movzx	ecx, BYTE PTR [r9]
	cmp	cl, 62
	je	.L666
	cmp	cl, 94
	je	.L667
	mov	edi, 1
	cmp	cl, 60
	jne	.L621
.L620:
	lea	r10, 1[r9]
	jmp	.L622
	.p2align 4,,10
	.p2align 3
.L610:
	mov	DWORD PTR 108[rsp], 32
.L612:
	mov	rax, QWORD PTR 100[rsp]
	mov	QWORD PTR [rbx], rax
	mov	eax, DWORD PTR 108[rsp]
	mov	DWORD PTR 8[rbx], eax
	mov	rax, r10
	add	rsp, 216
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
.L621:
	cmp	al, 62
	je	.L623
	cmp	al, 94
	je	.L624
	cmp	al, 60
	je	.L625
	.p2align 4
	.p2align 3
.L613:
	mov	esi, 32
	xor	edi, edi
.L626:
	movzx	eax, BYTE PTR [r10]
	cmp	al, 125
	je	.L628
.L629:
	lea	ecx, -32[rax]
	cmp	cl, 13
	ja	.L668
	movzx	ecx, cl
	lea	r8, CSWTCH.641[rip]
	mov	ecx, DWORD PTR [r8+rcx*4]
	test	ecx, ecx
	jne	.L631
	cmp	al, 35
	je	.L669
	xor	r15d, r15d
	xor	r14d, r14d
.L633:
	mov	BYTE PTR 160[rsp], 0
	xor	r12d, r12d
.L639:
	movzx	eax, r14b
	movzx	ecx, dil
	mov	QWORD PTR 32[rsp], r11
	xor	ebp, ebp
	mov	WORD PTR 64[rsp], ax
	sal	eax, 2
	lea	r8, 104[rsp]
	lea	r9, 160[rsp]
	or	eax, ecx
	mov	WORD PTR 56[rsp], cx
	movzx	ecx, r15b
	mov	r13d, ecx
	sal	ecx, 4
	mov	QWORD PTR 296[rsp], r11
	or	eax, ecx
	movzx	ecx, r12b
	mov	QWORD PTR 88[rsp], rdx
	mov	WORD PTR 78[rsp], cx
	sal	ecx, 6
	or	eax, ecx
	movzx	ecx, WORD PTR 100[rsp]
	mov	DWORD PTR 108[rsp], esi
	mov	QWORD PTR 80[rsp], r10
	and	cx, -32768
	or	eax, ecx
	mov	rcx, r10
	mov	WORD PTR 100[rsp], ax
	call	_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE
	cmp	rax, QWORD PTR 80[rsp]
	mov	rdx, QWORD PTR 88[rsp]
	mov	r11, QWORD PTR 296[rsp]
	je	.L642
	movzx	ecx, BYTE PTR 160[rsp]
	add	ecx, 1
	and	ecx, 3
	mov	ebp, ecx
.L642:
	cmp	rdx, rax
	je	.L643
	movzx	r8d, BYTE PTR [rax]
	cmp	r8b, 125
	je	.L643
	cmp	r8b, 46
	je	.L688
	cmp	r8b, 76
	je	.L689
	xor	r9d, r9d
	xor	ecx, ecx
.L661:
	sub	r8d, 65
	cmp	r8b, 38
	ja	.L687
	lea	r10, .L663[rip]
	movzx	r8d, r8b
	movsxd	r8, DWORD PTR [r10+r8*4]
	add	r8, r10
	jmp	r8
	.section .rdata,"dr"
	.align 4
.L663:
	.long	.L659-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L658-.L663
	.long	.L657-.L663
	.long	.L656-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L655-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L687-.L663
	.long	.L654-.L663
	.long	.L653-.L663
	.long	.L651-.L663
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L668:
	xor	r14d, r14d
	xor	r15d, r15d
.L630:
	cmp	al, 48
	je	.L637
	xor	r12d, r12d
	xor	ebp, ebp
	cmp	al, 46
	jne	.L633
.L638:
	lea	rcx, 1[r10]
	mov	BYTE PTR 160[rsp], 0
	cmp	rdx, rcx
	je	.L646
	movzx	eax, r14b
	movzx	r9d, dil
	movzx	r8d, r15b
	mov	DWORD PTR 108[rsp], esi
	mov	WORD PTR 64[rsp], ax
	sal	eax, 2
	sal	r8d, 4
	movzx	r13d, r15b
	mov	WORD PTR 56[rsp], r9w
	or	eax, r9d
	movzx	r9d, r12b
	or	eax, r8d
	mov	r8d, r9d
	mov	QWORD PTR 32[rsp], r11
	sal	r8d, 6
	mov	WORD PTR 78[rsp], r9w
	lea	r9, 160[rsp]
	or	eax, r8d
	movzx	r8d, bpl
	mov	QWORD PTR 80[rsp], rdx
	sal	r8d, 7
	mov	QWORD PTR 88[rsp], rcx
	or	eax, r8d
	movzx	r8d, WORD PTR 100[rsp]
	and	r8w, -32768
	or	eax, r8d
	lea	r8, 106[rsp]
	mov	WORD PTR 100[rsp], ax
	call	_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE
	mov	r10, rax
	cmp	QWORD PTR 88[rsp], rax
	je	.L646
	movzx	eax, BYTE PTR 160[rsp]
	mov	rdx, QWORD PTR 80[rsp]
	lea	ecx, 1[rax]
	and	ecx, 3
	cmp	rdx, r10
	je	.L647
	movzx	eax, BYTE PTR [r10]
	cmp	al, 125
	je	.L647
	cmp	al, 76
	je	.L676
	sub	eax, 65
	cmp	al, 38
	ja	.L677
	lea	r8, .L652[rip]
	movzx	eax, al
	movsxd	rax, DWORD PTR [r8+rax*4]
	add	rax, r8
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L652:
	.long	.L678-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L679-.L652
	.long	.L680-.L652
	.long	.L681-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L682-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L677-.L652
	.long	.L683-.L652
	.long	.L684-.L652
	.long	.L685-.L652
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L625:
	mov	edi, 1
.L627:
	add	r10, 1
	mov	esi, 32
.L622:
	cmp	rdx, r10
	jne	.L626
.L628:
	movzx	eax, WORD PTR 100[rsp]
	mov	edx, edi
	mov	DWORD PTR 108[rsp], esi
	and	edx, 3
	and	ax, -32768
	or	eax, edx
	mov	WORD PTR 100[rsp], ax
	jmp	.L612
	.p2align 4,,10
	.p2align 3
.L631:
	mov	eax, ecx
	lea	r8, 1[r10]
	and	eax, 3
	mov	r14d, eax
	cmp	rdx, r8
	jne	.L717
.L634:
	and	ecx, 3
	movzx	edx, dil
	mov	DWORD PTR 108[rsp], esi
	mov	r10, r8
	lea	eax, 0[0+rcx*4]
	or	eax, edx
	movzx	edx, WORD PTR 100[rsp]
	and	dx, -32768
	or	eax, edx
	mov	WORD PTR 100[rsp], ax
	jmp	.L612
	.p2align 4,,10
	.p2align 3
.L715:
	cmp	rdx, r9
	je	.L616
	movzx	ecx, dil
	add	rcx, r9
	cmp	rdx, rcx
	je	.L616
	mov	QWORD PTR 128[rsp], rcx
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r10
	mov	BYTE PTR 64[rsp], r8b
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	r10, QWORD PTR 80[rsp]
	movzx	eax, BYTE PTR 78[rsp]
	mov	r9, QWORD PTR 128[rsp]
	mov	r11, QWORD PTR 296[rsp]
	movzx	r8d, BYTE PTR 64[rsp]
	mov	rdx, QWORD PTR 56[rsp]
	jmp	.L614
.L667:
	mov	edi, 3
	jmp	.L620
.L687:
	xor	r8d, r8d
.L662:
	mov	r10, rax
	cmp	rdx, rax
	je	.L664
.L650:
	cmp	BYTE PTR [r10], 125
	je	.L718
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L677:
	xor	r9d, r9d
	xor	r8d, r8d
	jmp	.L650
.L685:
	mov	rax, r10
	xor	r9d, r9d
.L651:
	add	rax, 1
	mov	r8d, 7
	jmp	.L662
.L684:
	mov	rax, r10
	xor	r9d, r9d
.L653:
	add	rax, 1
	mov	r8d, 5
	jmp	.L662
.L683:
	mov	rax, r10
	xor	r9d, r9d
.L654:
	add	rax, 1
	mov	r8d, 3
	jmp	.L662
.L682:
	mov	rax, r10
	xor	r9d, r9d
.L655:
	add	rax, 1
	mov	r8d, 1
	jmp	.L662
.L681:
	mov	rax, r10
	xor	r9d, r9d
.L656:
	add	rax, 1
	mov	r8d, 8
	jmp	.L662
.L680:
	mov	rax, r10
	xor	r9d, r9d
.L657:
	add	rax, 1
	mov	r8d, 6
	jmp	.L662
.L679:
	mov	rax, r10
	xor	r9d, r9d
.L658:
	add	rax, 1
	mov	r8d, 4
	jmp	.L662
.L678:
	mov	rax, r10
	xor	r9d, r9d
.L659:
	add	rax, 1
	mov	r8d, 2
	jmp	.L662
	.p2align 4,,10
	.p2align 3
.L637:
	lea	rcx, 1[r10]
	cmp	rdx, rcx
	jne	.L719
.L640:
	movzx	eax, r14b
	movzx	edx, dil
	mov	DWORD PTR 108[rsp], esi
	mov	r10, rcx
	or	edx, 64
	sal	eax, 2
	or	eax, edx
	movzx	edx, r15b
	sal	edx, 4
	or	eax, edx
	movzx	edx, WORD PTR 100[rsp]
	and	dx, -32768
	or	eax, edx
	mov	WORD PTR 100[rsp], ax
	jmp	.L612
	.p2align 4,,10
	.p2align 3
.L624:
	mov	edi, 3
	jmp	.L627
	.p2align 4,,10
	.p2align 3
.L623:
	mov	edi, 2
	jmp	.L627
.L669:
	mov	r8, r10
	xor	r14d, r14d
.L632:
	lea	r10, 1[r8]
	cmp	rdx, r10
	jne	.L720
.L636:
	movzx	eax, r14b
	movzx	edx, dil
	sal	eax, 2
	or	edx, 16
	or	eax, edx
.L714:
	movzx	edx, WORD PTR 100[rsp]
	mov	DWORD PTR 108[rsp], esi
	and	dx, -32768
	or	eax, edx
	mov	WORD PTR 100[rsp], ax
	jmp	.L612
.L720:
	movzx	eax, BYTE PTR 1[r8]
	mov	r15d, 1
	cmp	al, 125
	jne	.L630
	jmp	.L636
.L616:
	mov	ecx, DWORD PTR 160[rsp+r8*4]
	cmp	ecx, 55295
	jbe	.L621
	sub	ecx, 57344
	cmp	ecx, 1056767
	jbe	.L621
.L618:
	cmp	al, 62
	je	.L623
	cmp	al, 94
	je	.L624
	cmp	al, 60
	je	.L625
	mov	esi, 32
	xor	edi, edi
	jmp	.L629
	.p2align 4,,10
	.p2align 3
.L647:
	movzx	eax, WORD PTR 100[rsp]
	sal	ecx, 9
	and	cx, 32288
	and	ax, -32289
	or	eax, ecx
	mov	WORD PTR 100[rsp], ax
	jmp	.L612
.L719:
	movzx	eax, BYTE PTR 1[r10]
	cmp	al, 125
	je	.L640
	cmp	al, 46
	je	.L673
	mov	BYTE PTR 160[rsp], 0
	cmp	al, 48
	je	.L721
	mov	r10, rcx
	mov	r12d, 1
	jmp	.L639
.L666:
	mov	edi, 2
	jmp	.L620
.L643:
	movzx	edx, WORD PTR 100[rsp]
	mov	ecx, ebp
	mov	r10, rax
	and	ecx, 3
	sal	ecx, 7
	and	dx, -385
	or	edx, ecx
	mov	WORD PTR 100[rsp], dx
	jmp	.L612
.L716:
	sub	ecx, 57344
	cmp	ecx, 1056767
	ja	.L618
	jmp	.L617
.L689:
	xor	ecx, ecx
.L649:
	lea	r10, 1[rax]
	cmp	rdx, r10
	jne	.L722
.L660:
	movzx	eax, WORD PTR 64[rsp]
	movzx	edx, WORD PTR 56[rsp]
	sal	ecx, 9
	or	edx, 32
	sal	eax, 2
	or	eax, edx
	mov	edx, r13d
	sal	edx, 4
	or	eax, edx
	movzx	edx, WORD PTR 78[rsp]
	sal	edx, 6
	or	eax, edx
	movzx	edx, bpl
	sal	edx, 7
	or	eax, edx
	or	eax, ecx
	and	ax, 32767
	jmp	.L714
.L673:
	mov	r10, rcx
	mov	r12d, 1
	xor	ebp, ebp
	jmp	.L638
.L718:
	mov	rax, r10
.L664:
	movzx	edx, WORD PTR 64[rsp]
	mov	r10d, r13d
	sal	r9d, 5
	mov	DWORD PTR 108[rsp], esi
	sal	r10d, 4
	sal	ecx, 9
	sal	edx, 2
	or	dx, WORD PTR 56[rsp]
	sal	r8d, 11
	or	edx, r10d
	mov	r10, rax
	or	edx, r9d
	movzx	r9d, WORD PTR 78[rsp]
	sal	r9d, 6
	or	edx, r9d
	movzx	r9d, bpl
	sal	r9d, 7
	or	edx, r9d
	or	edx, ecx
	movzx	ecx, WORD PTR 100[rsp]
	or	edx, r8d
	and	dx, 32767
	and	cx, -32768
	or	edx, ecx
	mov	WORD PTR 100[rsp], dx
	jmp	.L612
.L722:
	movzx	r8d, BYTE PTR 1[rax]
	cmp	r8b, 125
	je	.L660
	mov	rax, r10
	mov	r9d, 1
	jmp	.L661
	.p2align 4,,10
	.p2align 3
.L676:
	mov	rax, r10
	jmp	.L649
.L688:
	mov	r10, rax
	jmp	.L638
.L717:
	movzx	eax, BYTE PTR 1[r10]
	cmp	al, 125
	je	.L634
	cmp	al, 35
	je	.L632
	mov	r10, r8
	xor	r15d, r15d
	jmp	.L630
.L721:
	lea	rcx, .LC22[rip]
	call	_ZSt20__throw_format_errorPKc
.L646:
	lea	rcx, .LC23[rip]
	call	_ZSt20__throw_format_errorPKc
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
.LFB5615:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 192
	.seh_stackalloc	192
	.seh_endprologue
	movdqu	xmm0, XMMWORD PTR [rdx]
	movq	r10, xmm0
	mov	QWORD PTR 84[rsp], 0
	mov	r11, rdx
	mov	rdx, QWORD PTR 8[rdx]
	mov	rbx, rcx
	cmp	rdx, r10
	je	.L724
	movzx	eax, BYTE PTR [r10]
	cmp	al, 125
	je	.L724
	cmp	al, 123
	je	.L727
	xor	ecx, ecx
	movq	QWORD PTR 56[rsp], xmm0
	punpcklqdq	xmm0, xmm0
	mov	WORD PTR 120[rsp], cx
	lea	rcx, 96[rsp]
	mov	QWORD PTR 232[rsp], r11
	mov	QWORD PTR 128[rsp], rdx
	mov	QWORD PTR 48[rsp], rdx
	mov	BYTE PTR 64[rsp], al
	mov	BYTE PTR 122[rsp], 0
	movups	XMMWORD PTR 104[rsp], xmm0
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	movzx	r8d, BYTE PTR 120[rsp]
	mov	r9, QWORD PTR 112[rsp]
	mov	rcx, QWORD PTR 128[rsp]
	movdqa	xmm1, XMMWORD PTR 96[rsp]
	movdqa	xmm2, XMMWORD PTR 112[rsp]
	movzx	esi, BYTE PTR 122[rsp]
	mov	QWORD PTR 176[rsp], rcx
	movzx	ecx, r8b
	mov	rdx, QWORD PTR 48[rsp]
	lea	eax, 1[rcx]
	movzx	ecx, BYTE PTR 121[rsp]
	mov	r10, QWORD PTR 56[rsp]
	movaps	XMMWORD PTR 144[rsp], xmm1
	mov	r11, QWORD PTR 232[rsp]
	movaps	XMMWORD PTR 160[rsp], xmm2
	cmp	eax, ecx
	movzx	eax, BYTE PTR 64[rsp]
	je	.L789
.L728:
	mov	r8d, DWORD PTR 144[rsp+r8*4]
	cmp	r8d, 55295
	ja	.L790
.L731:
	cmp	rdx, r9
	je	.L735
	movzx	ecx, BYTE PTR [r9]
	cmp	cl, 62
	je	.L759
	cmp	cl, 94
	je	.L760
	cmp	cl, 60
	jne	.L735
	mov	ecx, 1
.L734:
	lea	r10, 1[r9]
	jmp	.L736
	.p2align 4,,10
	.p2align 3
.L724:
	mov	DWORD PTR 92[rsp], 32
.L726:
	mov	rax, QWORD PTR 84[rsp]
	mov	QWORD PTR [rbx], rax
	mov	eax, DWORD PTR 92[rsp]
	mov	DWORD PTR 8[rbx], eax
	mov	rax, r10
	add	rsp, 192
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L735:
	cmp	al, 62
	je	.L737
	cmp	al, 94
	je	.L738
	cmp	al, 60
	je	.L739
	.p2align 4
	.p2align 3
.L727:
	mov	r8d, 32
	xor	ecx, ecx
.L740:
	movzx	eax, BYTE PTR [r10]
	cmp	al, 125
	je	.L742
.L743:
	mov	BYTE PTR 144[rsp], 0
	cmp	al, 48
	je	.L791
	movzx	eax, WORD PTR 84[rsp]
	mov	QWORD PTR 32[rsp], r11
	and	ecx, 3
	xor	esi, esi
	lea	r9, 144[rsp]
	mov	DWORD PTR 92[rsp], r8d
	lea	r8, 88[rsp]
	and	ax, -32644
	mov	QWORD PTR 232[rsp], r11
	or	eax, ecx
	mov	rcx, r10
	mov	QWORD PTR 64[rsp], r9
	mov	QWORD PTR 56[rsp], rdx
	mov	WORD PTR 84[rsp], ax
	mov	QWORD PTR 48[rsp], r10
	call	_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE
	cmp	rax, QWORD PTR 48[rsp]
	mov	rdx, QWORD PTR 56[rsp]
	mov	r9, QWORD PTR 64[rsp]
	mov	r11, QWORD PTR 232[rsp]
	je	.L745
	movzx	ecx, BYTE PTR 144[rsp]
	add	ecx, 1
	and	ecx, 3
	mov	esi, ecx
.L745:
	cmp	rdx, rax
	je	.L746
	movzx	ecx, BYTE PTR [rax]
	cmp	cl, 125
	je	.L746
	cmp	cl, 46
	je	.L748
	cmp	cl, 115
	je	.L792
	cmp	cl, 63
	jne	.L756
	xor	ecx, ecx
.L755:
	lea	r10, 1[rax]
	mov	r8d, 15
.L757:
	cmp	rdx, r10
	je	.L758
	cmp	BYTE PTR 1[rax], 125
	jne	.L756
.L758:
	sal	ecx, 9
	movzx	eax, sil
	movzx	edx, WORD PTR 84[rsp]
	sal	r8d, 11
	sal	eax, 7
	or	eax, ecx
	and	dx, -32641
	or	eax, r8d
	and	ax, 32640
	or	eax, edx
	mov	WORD PTR 84[rsp], ax
	jmp	.L726
	.p2align 4,,10
	.p2align 3
.L746:
	movzx	edx, WORD PTR 84[rsp]
	mov	ecx, esi
	mov	r10, rax
	and	ecx, 3
	sal	ecx, 7
	and	dx, -385
	or	edx, ecx
	mov	WORD PTR 84[rsp], dx
	jmp	.L726
	.p2align 4,,10
	.p2align 3
.L739:
	mov	ecx, 1
.L741:
	add	r10, 1
	mov	r8d, 32
.L736:
	cmp	rdx, r10
	jne	.L740
.L742:
	movzx	eax, WORD PTR 84[rsp]
	and	ecx, 3
	mov	DWORD PTR 92[rsp], r8d
	and	ax, -32644
	or	eax, ecx
	mov	WORD PTR 84[rsp], ax
	jmp	.L726
	.p2align 4,,10
	.p2align 3
.L748:
	lea	rcx, 1[rax]
	mov	BYTE PTR 144[rsp], 0
	cmp	rdx, rcx
	je	.L752
	movzx	eax, WORD PTR 84[rsp]
	mov	r8d, esi
	mov	QWORD PTR 32[rsp], r11
	and	r8d, 3
	mov	QWORD PTR 56[rsp], rdx
	sal	r8d, 7
	and	ax, -385
	mov	QWORD PTR 48[rsp], rcx
	or	eax, r8d
	lea	r8, 90[rsp]
	mov	WORD PTR 84[rsp], ax
	call	_ZNSt8__format5_SpecIcE27_S_parse_width_or_precisionEPKcS3_RtRbRSt26basic_format_parse_contextIcE
	mov	r10, rax
	cmp	QWORD PTR 48[rsp], rax
	je	.L752
	movzx	eax, BYTE PTR 144[rsp]
	mov	rdx, QWORD PTR 56[rsp]
	lea	ecx, 1[rax]
	and	ecx, 3
	cmp	rdx, r10
	je	.L753
	movzx	eax, BYTE PTR [r10]
	cmp	al, 125
	je	.L753
	cmp	al, 115
	je	.L763
	cmp	al, 63
	je	.L793
.L756:
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L789:
	cmp	rdx, r9
	je	.L730
	movzx	ecx, sil
	add	rcx, r9
	cmp	rdx, rcx
	je	.L730
	mov	QWORD PTR 112[rsp], rcx
	lea	rcx, 96[rsp]
	mov	QWORD PTR 72[rsp], r10
	mov	BYTE PTR 56[rsp], r8b
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	r9, QWORD PTR 112[rsp]
	mov	r10, QWORD PTR 72[rsp]
	mov	r11, QWORD PTR 232[rsp]
	movzx	eax, BYTE PTR 64[rsp]
	movzx	r8d, BYTE PTR 56[rsp]
	mov	rdx, QWORD PTR 48[rsp]
	jmp	.L728
.L760:
	mov	ecx, 3
	jmp	.L734
.L753:
	movzx	edx, BYTE PTR 85[rsp]
	and	ecx, 3
	lea	eax, [rcx+rcx]
	and	edx, -7
	or	eax, edx
	mov	BYTE PTR 85[rsp], al
	jmp	.L726
	.p2align 4,,10
	.p2align 3
.L738:
	mov	ecx, 3
	jmp	.L741
	.p2align 4,,10
	.p2align 3
.L737:
	mov	ecx, 2
	jmp	.L741
.L730:
	mov	ecx, DWORD PTR 144[rsp+r8*4]
	cmp	ecx, 55295
	jbe	.L735
	sub	ecx, 57344
	cmp	ecx, 1056767
	jbe	.L735
.L732:
	cmp	al, 62
	je	.L737
	cmp	al, 94
	je	.L738
	cmp	al, 60
	je	.L739
	mov	r8d, 32
	xor	ecx, ecx
	jmp	.L743
	.p2align 4,,10
	.p2align 3
.L792:
	xor	ecx, ecx
.L749:
	lea	r10, 1[rax]
	xor	r8d, r8d
	jmp	.L757
.L759:
	mov	ecx, 2
	jmp	.L734
.L790:
	lea	ecx, -57344[r8]
	cmp	ecx, 1056767
	ja	.L732
	jmp	.L731
.L763:
	mov	rax, r10
	jmp	.L749
.L793:
	mov	rax, r10
	jmp	.L755
.L791:
	lea	rcx, .LC22[rip]
	call	_ZSt20__throw_format_errorPKc
.L752:
	lea	rcx, .LC23[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi
	.def	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi
_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi:
.LFB5622:
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
	sub	rsp, 232
	.seh_stackalloc	232
	.seh_endprologue
	mov	rax, QWORD PTR 8[rdx]
	mov	r12, QWORD PTR [rdx]
	mov	rbx, rcx
	mov	QWORD PTR 48[rsp], rax
	mov	rdi, r9
	mov	ecx, DWORD PTR 336[rsp]
	mov	BYTE PTR 112[rsp], 0
	cmp	r8d, 3
	je	.L1080
	cmp	r8d, 2
	je	.L926
	cmp	ecx, 126
	ja	.L927
	cmp	r9, 31
	jbe	.L798
	movd	xmm0, ecx
	mov	QWORD PTR 40[rsp], r9
	mov	rbp, r12
	mov	edi, 32
	punpcklbw	xmm0, xmm0
	punpcklwd	xmm0, xmm0
	pshufd	xmm0, xmm0, 0
	movaps	XMMWORD PTR 112[rsp], xmm0
	movaps	XMMWORD PTR 128[rsp], xmm0
	test	r12, r12
	jne	.L799
.L800:
	mov	rax, QWORD PTR 40[rsp]
	cmp	rdi, rax
	jnb	.L944
	test	rdi, rdi
	je	.L973
	lea	rsi, 112[rsp]
	mov	r14, rax
.L920:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rbp, QWORD PTR 16[rbx]
	mov	r12, rdi
	mov	r13, rsi
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rbp, rax
	cmp	rdi, rbp
	jb	.L916
	.p2align 4
	.p2align 3
.L918:
	test	rbp, rbp
	je	.L917
	mov	r8, rbp
	mov	rdx, r13
	call	memcpy
.L917:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rbp
	mov	rcx, rbx
	add	r13, rbp
	sub	r12, rbp
.LEHB9:
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	rbp, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rbp, rax
	cmp	r12, rbp
	jnb	.L918
	test	r12, r12
	jne	.L916
.L919:
	sub	r14, rdi
	cmp	rdi, r14
	jb	.L920
	mov	QWORD PTR 40[rsp], r14
	test	r14, r14
	jne	.L1081
.L980:
	mov	rax, rbx
	add	rsp, 232
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
.L926:
	mov	QWORD PTR 40[rsp], 0
	mov	rbp, r9
.L796:
	cmp	ecx, 126
	ja	.L797
	cmp	rdi, 31
	ja	.L939
	test	rdi, rdi
	jne	.L888
	test	rbp, rbp
	je	.L1082
.L963:
.L898:
	jmp	.L898
	.p2align 4,,10
	.p2align 3
.L939:
	mov	edi, 32
.L888:
	lea	rsi, 112[rsp]
	mov	edx, edi
	mov	rax, rsi
	cmp	edi, 8
	jnb	.L1083
.L891:
	and	edx, 7
	je	.L895
	xor	r8d, r8d
.L894:
	mov	r9d, r8d
	add	r8d, 1
	mov	BYTE PTR [rax+r9], cl
	cmp	r8d, edx
	jb	.L894
.L895:
	test	rbp, rbp
	je	.L904
	cmp	rdi, rbp
	jnb	.L897
	test	rdi, rdi
	je	.L963
.L903:
	mov	rcx, QWORD PTR 24[rbx]
	mov	r13, QWORD PTR 16[rbx]
	mov	r14, rdi
	mov	r15, rsi
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r13, rax
	cmp	rdi, r13
	jb	.L899
	.p2align 4
	.p2align 3
.L901:
	test	r13, r13
	je	.L900
	mov	r8, r13
	mov	rdx, r15
	call	memcpy
.L900:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r13
	mov	rcx, rbx
	add	r15, r13
	sub	r14, r13
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	r13, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r13, rax
	cmp	r14, r13
	jnb	.L901
	test	r14, r14
	jne	.L899
.L902:
	sub	rbp, rdi
	cmp	rdi, rbp
	jb	.L903
	test	rbp, rbp
	jne	.L897
.L904:
	mov	rbp, r12
	test	r12, r12
	jne	.L799
.L909:
	cmp	QWORD PTR 40[rsp], 0
	jne	.L800
	jmp	.L980
	.p2align 4,,10
	.p2align 3
.L1080:
	mov	rbp, r9
	and	edi, 1
	shr	rbp
	add	rdi, rbp
	mov	QWORD PTR 40[rsp], rdi
	jmp	.L796
	.p2align 4,,10
	.p2align 3
.L798:
	test	r9, r9
	je	.L801
	lea	rsi, 112[rsp]
	mov	edx, ecx
	mov	r8, r9
	mov	rbp, r12
	mov	rcx, rsi
	call	memset
	test	r12, r12
	jne	.L1084
.L802:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rbp, QWORD PTR 16[rbx]
	mov	QWORD PTR 40[rsp], rdi
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rbp, rax
	cmp	rdi, rbp
	jb	.L922
.L921:
	mov	rdi, QWORD PTR 40[rsp]
.L924:
	test	rbp, rbp
	je	.L923
	mov	r8, rbp
	mov	rdx, rsi
	call	memcpy
.L923:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rbp
	mov	rcx, rbx
	add	rsi, rbp
	sub	rdi, rbp
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	rbp, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rbp, rax
	cmp	rdi, rbp
	jnb	.L924
	mov	QWORD PTR 40[rsp], rdi
	test	rdi, rdi
	je	.L980
.L922:
	mov	rdi, QWORD PTR 40[rsp]
	mov	rdx, rsi
	mov	r8, rdi
	call	memcpy
	add	QWORD PTR 24[rbx], rdi
	jmp	.L980
	.p2align 4,,10
	.p2align 3
.L899:
	mov	r8, r14
	mov	rdx, r15
	call	memcpy
	add	QWORD PTR 24[rbx], r14
	jmp	.L902
	.p2align 4,,10
	.p2align 3
.L916:
	mov	r8, r12
	mov	rdx, r13
	call	memcpy
	add	QWORD PTR 24[rbx], r12
	jmp	.L919
.L1084:
	mov	QWORD PTR 40[rsp], rdi
	.p2align 4
	.p2align 3
.L799:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	r13, QWORD PTR 48[rsp]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	r12, rsi
	jb	.L911
	.p2align 4
	.p2align 3
.L913:
	test	rsi, rsi
	je	.L912
	mov	r8, rsi
	mov	rdx, r13
	call	memcpy
.L912:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rsi
	mov	rcx, rbx
	add	r13, rsi
	sub	rbp, rsi
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	rbp, rsi
	jnb	.L913
	test	rbp, rbp
	je	.L909
.L911:
	mov	r8, rbp
	mov	rdx, r13
	call	memcpy
	add	QWORD PTR 24[rbx], rbp
	jmp	.L909
	.p2align 4,,10
	.p2align 3
.L897:
	mov	rcx, QWORD PTR 24[rbx]
	mov	r13, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r13, rax
	cmp	rbp, r13
	jb	.L906
.L908:
	test	r13, r13
	je	.L907
	mov	r8, r13
	mov	rdx, rsi
	call	memcpy
.L907:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r13
	mov	rcx, rbx
	add	rsi, r13
	sub	rbp, r13
	call	[QWORD PTR [rax]]
.LEHE9:
	mov	rcx, QWORD PTR 24[rbx]
	mov	r13, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r13, rax
	cmp	rbp, r13
	jnb	.L908
	test	rbp, rbp
	je	.L904
.L906:
	mov	r8, rbp
	mov	rdx, rsi
	call	memcpy
	add	QWORD PTR 24[rbx], rbp
	jmp	.L904
	.p2align 4,,10
	.p2align 3
.L1083:
	movabs	rax, 72340172838076673
	movzx	r8d, cl
	mov	r10d, edi
	imul	r8, rax
	and	r10d, -8
	xor	eax, eax
.L892:
	mov	r9d, eax
	add	eax, 8
	mov	QWORD PTR [rsi+r9], r8
	cmp	eax, r10d
	jb	.L892
	add	rax, rsi
	jmp	.L891
	.p2align 4,,10
	.p2align 3
.L1081:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rbp, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rbp, rax
	cmp	r14, rbp
	jnb	.L921
	jmp	.L922
.L927:
	mov	QWORD PTR 40[rsp], r9
	xor	ebp, ebp
.L797:
	lea	r8, 108[rsp]
	mov	DWORD PTR 108[rsp], ecx
	movq	xmm0, r8
	punpcklqdq	xmm0, xmm0
	cmp	ecx, 55295
	ja	.L806
	bsr	eax, ecx
	mov	edx, eax
	xor	edx, 31
	cmp	eax, 6
	jne	.L1085
	mov	r10d, ecx
	mov	r9d, 1
	xor	eax, eax
	xor	r11d, r11d
	xor	edx, edx
.L811:
	movzx	eax, al
	movzx	r11d, r11b
	movzx	edx, dl
	xor	r13d, r13d
	sal	eax, 8
	lea	rdi, 160[rsp]
	lea	rcx, 144[rsp]
	mov	QWORD PTR 152[rsp], 0
	or	eax, r11d
	lea	rsi, 112[rsp]
	mov	QWORD PTR 88[rsp], rcx
	sal	eax, 8
	mov	QWORD PTR 64[rsp], rdi
	or	eax, edx
	movzx	edx, r10b
	mov	QWORD PTR 144[rsp], rdi
	sal	eax, 8
	mov	BYTE PTR 200[rsp], 0
	or	eax, edx
	mov	BYTE PTR 201[rsp], r9b
	xor	edx, edx
	mov	DWORD PTR 176[rsp], eax
	mov	BYTE PTR 202[rsp], 1
	mov	QWORD PTR 208[rsp], rsi
	movups	XMMWORD PTR 184[rsp], xmm0
	jmp	.L812
	.p2align 4,,10
	.p2align 3
.L818:
	jge	.L819
.L821:
	mov	r14, QWORD PTR 192[rsp]
	add	r13d, 1
	mov	r8, r14
.L833:
	cmp	rdx, 15
	je	.L828
	movzx	eax, r13b
	add	rcx, 1
	movzx	r10d, BYTE PTR 176[rsp+rax]
.L812:
	lea	eax, 1[r13]
	mov	BYTE PTR 16[rcx], r10b
	movzx	r10d, r9b
	add	rdx, 1
	movzx	eax, al
	cmp	eax, r10d
	jne	.L818
.L832:
	cmp	r8, rsi
	je	.L819
	lea	r14, 4[r8]
	mov	QWORD PTR 192[rsp], r14
	cmp	r14, rsi
	je	.L813
	mov	eax, DWORD PTR 4[r8]
	cmp	eax, 55295
	ja	.L1086
	test	eax, eax
	je	.L933
	bsr	r8d, eax
	xor	r8d, 31
	cmp	r8d, 24
	jle	.L826
.L825:
	xor	r10d, r10d
	mov	BYTE PTR 176[rsp], al
	mov	BYTE PTR 177[rsp], 0
	mov	WORD PTR 178[rsp], r10w
	cmp	rdx, 15
	je	.L1087
	add	rcx, 1
	add	rdx, 1
	mov	r8, r14
	xor	r13d, r13d
	mov	r9d, 1
	mov	BYTE PTR 16[rcx], al
	jmp	.L832
	.p2align 4,,10
	.p2align 3
.L819:
	mov	r14, QWORD PTR 192[rsp]
	mov	r8, r14
	cmp	r14, rsi
	jne	.L833
	test	r13b, r13b
	jne	.L833
.L813:
	mov	QWORD PTR 152[rsp], rdx
	mov	BYTE PTR 160[rsp+rdx], 0
	mov	r14, QWORD PTR 152[rsp]
	jmp	.L859
.L801:
	mov	rbp, r12
	test	r12, r12
	je	.L980
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	QWORD PTR 40[rsp], 0
	mov	r13, QWORD PTR 48[rsp]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	r12, rsi
	jnb	.L913
	mov	r8, r12
	mov	rdx, r13
	call	memcpy
	add	QWORD PTR 24[rbx], r12
	jmp	.L980
.L1087:
	mov	r14, QWORD PTR 192[rsp]
	xor	r13d, r13d
	mov	r9d, 1
.L828:
	mov	BYTE PTR 200[rsp], r13b
	mov	BYTE PTR 201[rsp], r9b
	cmp	r14, rsi
	je	.L1088
.L949:
	mov	r9d, 15
	mov	r15d, 15
	mov	r8d, 15
	jmp	.L817
	.p2align 4,,10
	.p2align 3
.L1091:
	mov	r10, QWORD PTR 144[rsp]
.L858:
	movzx	eax, r13b
	movzx	edx, BYTE PTR 201[rsp]
	movzx	eax, BYTE PTR 176[rsp+rax]
	mov	BYTE PTR [r10+r8], al
	movzx	eax, r13b
	add	eax, 1
	cmp	eax, edx
	je	.L1089
	mov	r14, QWORD PTR 192[rsp]
	jge	.L1090
	add	r13d, 1
	add	r9, 1
	mov	BYTE PTR 200[rsp], r13b
.L856:
	mov	r8, rdi
.L817:
	lea	rdi, 1[r8]
	cmp	r15, r9
	jne	.L1091
	movabs	rax, 9223372036854775806
	cmp	rax, rdi
	jb	.L1092
	cmp	r9, rdi
	jb	.L835
	mov	ecx, 1
	mov	QWORD PTR 72[rsp], r8
	mov	QWORD PTR 56[rsp], r9
.LEHB10:
	call	_Znwy
	mov	r9, QWORD PTR 56[rsp]
	mov	r8, QWORD PTR 72[rsp]
	mov	r10, rax
	xor	r15d, r15d
	mov	rcx, QWORD PTR 144[rsp]
.L836:
	mov	rdx, rcx
	mov	rcx, r10
	mov	QWORD PTR 72[rsp], r9
	mov	QWORD PTR 56[rsp], r8
	call	memcpy
	mov	r9, QWORD PTR 72[rsp]
	mov	r8, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 144[rsp]
	mov	r10, rax
.L840:
	cmp	rcx, QWORD PTR 64[rsp]
	je	.L841
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 80[rsp], r10
	mov	QWORD PTR 72[rsp], r8
	lea	rdx, 1[rax]
	mov	QWORD PTR 56[rsp], r9
	call	_ZdlPvy
	mov	r10, QWORD PTR 80[rsp]
	mov	r8, QWORD PTR 72[rsp]
	mov	r9, QWORD PTR 56[rsp]
.L841:
	mov	QWORD PTR 144[rsp], r10
	mov	QWORD PTR 160[rsp], r15
	jmp	.L858
	.p2align 4,,10
	.p2align 3
.L1089:
	cmp	r14, rsi
	je	.L1093
	lea	rdx, 4[r14]
	mov	QWORD PTR 192[rsp], rdx
	cmp	rdx, rsi
	je	.L845
	mov	eax, DWORD PTR 4[r14]
	cmp	eax, 55295
	ja	.L1094
	mov	BYTE PTR 200[rsp], 0
	test	eax, eax
	je	.L936
	bsr	ecx, eax
	xor	ecx, 31
	cmp	ecx, 24
	jle	.L854
.L853:
	xor	ecx, ecx
	mov	BYTE PTR 177[rsp], 0
	mov	WORD PTR 178[rsp], cx
	mov	BYTE PTR 176[rsp], al
	mov	eax, 1
.L855:
	mov	BYTE PTR 201[rsp], al
	add	r9, 1
	mov	r14, rdx
	xor	r13d, r13d
	jmp	.L856
	.p2align 4,,10
	.p2align 3
.L1090:
	movzx	r13d, BYTE PTR 200[rsp]
.L1076:
	cmp	r14, rsi
	sete	al
	test	r13b, r13b
	sete	dl
	and	eax, edx
	test	al, al
	jne	.L845
	add	r9, 1
	jmp	.L856
.L835:
	add	r15, r15
	cmp	rdi, r15
	jb	.L837
	lea	rcx, 2[r8]
	mov	r15, rdi
.L838:
	mov	QWORD PTR 72[rsp], r8
	mov	QWORD PTR 56[rsp], r9
	call	_Znwy
.LEHE10:
	mov	r9, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 144[rsp]
	mov	r10, rax
	mov	r8, QWORD PTR 72[rsp]
	cmp	r9, 1
	jne	.L839
	movzx	eax, BYTE PTR [rcx]
	mov	BYTE PTR [r10], al
	mov	rcx, QWORD PTR 144[rsp]
	jmp	.L840
.L1093:
	movzx	r13d, BYTE PTR 200[rsp]
	mov	r14, QWORD PTR 192[rsp]
	jmp	.L1076
.L845:
	mov	rax, QWORD PTR 144[rsp]
	mov	QWORD PTR 152[rsp], rdi
	mov	BYTE PTR [rax+rdi], 0
	mov	r14, QWORD PTR 152[rsp]
.L859:
	mov	rax, QWORD PTR 144[rsp]
	lea	r13, -1[rbp]
	mov	QWORD PTR 56[rsp], rax
	test	rbp, rbp
	je	.L870
	test	r14, r14
	jne	.L1077
.L1059:
	sub	r13, 1
	jnb	.L1059
.L870:
	test	r12, r12
	jne	.L1095
.L863:
	mov	rax, QWORD PTR 40[rsp]
	lea	rbp, -1[rax]
	test	rax, rax
	je	.L885
	test	r14, r14
	jne	.L1078
.L1060:
	sub	rbp, 1
	jnb	.L1060
.L885:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, QWORD PTR 64[rsp]
	je	.L980
	mov	rax, QWORD PTR 160[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L980
.L866:
	mov	r8, rsi
	mov	rdx, rbp
	call	memcpy
	add	QWORD PTR 24[rbx], rsi
	sub	r13, 1
	jb	.L870
.L1077:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rax, QWORD PTR 16[rbx]
.L864:
	mov	rdx, rcx
	sub	rdx, QWORD PTR 8[rbx]
	mov	rbp, QWORD PTR 56[rsp]
	mov	rsi, r14
	sub	rax, rdx
	mov	r15, rax
	cmp	r14, rax
	jb	.L866
	.p2align 4
	.p2align 3
.L868:
	test	r15, r15
	je	.L867
	mov	r8, r15
	mov	rdx, rbp
	call	memcpy
.L867:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r15
	add	rbp, r15
	sub	rsi, r15
	mov	rcx, rbx
.LEHB11:
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	rax, QWORD PTR 16[rbx]
	mov	rdx, rcx
	mov	r15, rax
	sub	rdx, QWORD PTR 8[rbx]
	sub	r15, rdx
	cmp	rsi, r15
	jnb	.L868
	test	rsi, rsi
	jne	.L866
	sub	r13, 1
	jnb	.L864
	jmp	.L870
.L938:
	mov	rdi, QWORD PTR 56[rsp]
	mov	rsi, r14
.L880:
	mov	r8, rsi
	mov	rdx, rdi
	call	memcpy
	add	QWORD PTR 24[rbx], rsi
	sub	rbp, 1
	jb	.L885
.L1078:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rax, QWORD PTR 16[rbx]
.L878:
	mov	rdx, rcx
	sub	rdx, QWORD PTR 8[rbx]
	sub	rax, rdx
	mov	r12, rax
	cmp	r14, rax
	jb	.L938
	mov	rdi, QWORD PTR 56[rsp]
	mov	rsi, r14
	.p2align 4
	.p2align 3
.L882:
	test	r12, r12
	je	.L881
	mov	r8, r12
	mov	rdx, rdi
	call	memcpy
.L881:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r12
	add	rdi, r12
	sub	rsi, r12
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	rax, QWORD PTR 16[rbx]
	mov	rdx, rcx
	mov	r12, rax
	sub	rdx, QWORD PTR 8[rbx]
	sub	r12, rdx
	cmp	rsi, r12
	jnb	.L882
	test	rsi, rsi
	jne	.L880
	sub	rbp, 1
	jnb	.L878
	jmp	.L885
.L837:
	movabs	rax, 9223372036854775806
	cmp	rax, r15
	jnb	.L1096
	movabs	r15, 9223372036854775806
	movabs	rcx, 9223372036854775807
	jmp	.L838
.L1088:
	test	r13b, r13b
	jne	.L949
	mov	edx, 15
	jmp	.L813
	.p2align 4,,10
	.p2align 3
.L1096:
	lea	rcx, -1[rdi+rdi]
	jmp	.L838
.L936:
	xor	eax, eax
	jmp	.L853
.L1082:
	test	r12, r12
	jne	.L940
	cmp	QWORD PTR 40[rsp], 0
	je	.L980
.L973:
.L915:
	jmp	.L915
	.p2align 4,,10
	.p2align 3
.L1086:
	lea	r8d, -57344[rax]
	cmp	r8d, 1056767
	ja	.L932
	bsr	r8d, eax
	cmp	r8d, 15
	je	.L823
	mov	r10d, eax
	mov	r8d, eax
	mov	r9d, eax
	and	eax, 63
	shr	r10d, 6
	sal	eax, 8
	mov	edi, DWORD PTR .LC24[rip]
	shr	r9d, 12
	and	r10d, 63
	shr	r8d, 18
	or	eax, r10d
	and	r9d, 63
	movzx	r8d, r8b
	sal	eax, 8
	or	eax, r9d
	sal	eax, 8
	or	eax, r8d
	or	eax, edi
	mov	DWORD PTR 176[rsp], eax
	cmp	rdx, 15
	je	.L934
	movzx	eax, BYTE PTR 176[rsp]
	add	rcx, 1
	add	rdx, 1
	mov	r9d, 4
	mov	BYTE PTR 16[rcx], al
.L831:
	xor	r13d, r13d
	jmp	.L821
	.p2align 4,,10
	.p2align 3
.L839:
	test	r9, r9
	je	.L840
	jmp	.L836
.L1095:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rbp, QWORD PTR 16[rbx]
	mov	rsi, QWORD PTR 48[rsp]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rbp, rax
	cmp	r12, rbp
	jb	.L872
	.p2align 4
	.p2align 3
.L874:
	test	rbp, rbp
	je	.L873
	mov	r8, rbp
	mov	rdx, rsi
	call	memcpy
.L873:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rbp
	add	rsi, rbp
	sub	r12, rbp
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
.LEHE11:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rax, QWORD PTR 16[rbx]
	mov	rdx, rcx
	sub	rdx, QWORD PTR 8[rbx]
	sub	rax, rdx
	mov	rbp, rax
	cmp	r12, rax
	jnb	.L874
	test	r12, r12
	je	.L863
.L872:
	mov	r8, r12
	mov	rdx, rsi
	call	memcpy
	add	QWORD PTR 24[rbx], r12
	jmp	.L863
.L933:
	xor	eax, eax
	jmp	.L825
.L806:
	lea	eax, -57344[rcx]
	cmp	eax, 1056767
	ja	.L930
	bsr	eax, ecx
	cmp	eax, 15
	je	.L809
	mov	r11d, ecx
	mov	edx, ecx
	mov	eax, ecx
	mov	r10d, ecx
	shr	r11d, 6
	shr	edx, 12
	and	eax, 63
	mov	r9d, 4
	and	r11d, 63
	shr	r10d, 18
	and	edx, 63
	or	eax, -128
	or	r11d, -128
	or	r10d, -16
	or	edx, -128
	jmp	.L811
.L1094:
	lea	ecx, -57344[rax]
	mov	BYTE PTR 200[rsp], 0
	cmp	ecx, 1056767
	ja	.L1097
	bsr	ecx, eax
	cmp	ecx, 15
	je	.L850
	mov	r8d, eax
	mov	r10d, eax
	mov	ecx, eax
	and	eax, 63
	shr	r8d, 6
	sal	eax, 8
	shr	ecx, 12
	and	r8d, 63
	shr	r10d, 18
	or	eax, r8d
	and	ecx, 63
	movzx	r10d, r10b
	sal	eax, 8
	or	eax, ecx
	mov	ecx, DWORD PTR .LC24[rip]
	sal	eax, 8
	or	eax, r10d
	or	eax, ecx
	mov	DWORD PTR 176[rsp], eax
	mov	eax, 4
	jmp	.L855
.L1097:
	mov	eax, 65533
.L850:
	mov	ecx, eax
	mov	BYTE PTR 179[rsp], 0
	shr	ecx, 12
	or	ecx, -32
	mov	BYTE PTR 176[rsp], cl
	mov	ecx, eax
	and	eax, 63
	shr	ecx, 6
	or	eax, -128
	and	ecx, 63
	mov	BYTE PTR 178[rsp], al
	mov	eax, 3
	or	ecx, -128
	mov	BYTE PTR 177[rsp], cl
	jmp	.L855
.L944:
	mov	rdi, QWORD PTR 40[rsp]
	lea	rsi, 112[rsp]
	jmp	.L802
.L930:
	mov	ecx, 65533
.L809:
	mov	edx, ecx
	mov	r10d, ecx
	mov	r11d, ecx
	mov	r9d, 3
	shr	edx, 6
	shr	r10d, 12
	and	r11d, 63
	xor	eax, eax
	and	edx, 63
	or	r10d, -32
	or	r11d, -128
	or	edx, -128
	jmp	.L811
.L940:
	mov	rbp, r12
	jmp	.L799
.L932:
	mov	eax, 65533
.L823:
	mov	r8d, eax
	mov	r9d, eax
	and	eax, 63
	mov	BYTE PTR 179[rsp], 0
	shr	r8d, 6
	shr	r9d, 12
	or	eax, -128
	and	r8d, 63
	or	r9d, -32
	mov	BYTE PTR 178[rsp], al
	or	r8d, -128
	mov	BYTE PTR 176[rsp], r9b
	mov	BYTE PTR 177[rsp], r8b
	cmp	rdx, 15
	je	.L1098
	add	rcx, 1
	mov	BYTE PTR 16[rcx], r9b
	add	rdx, 1
	mov	r9d, 3
	jmp	.L831
.L934:
	xor	r13d, r13d
	mov	r9d, 4
	jmp	.L828
.L1098:
	mov	r14, QWORD PTR 192[rsp]
	xor	r13d, r13d
	mov	r9d, 3
	jmp	.L828
.L826:
	cmp	r8d, 20
	jle	.L823
	mov	r8d, eax
	and	eax, 63
	xor	r9d, r9d
	mov	WORD PTR 178[rsp], r9w
	shr	r8d, 6
	or	eax, -128
	or	r8d, -64
	mov	BYTE PTR 177[rsp], al
	mov	BYTE PTR 176[rsp], r8b
	cmp	rdx, 15
	je	.L1099
	add	rcx, 1
	add	rdx, 1
	mov	r9d, 2
	mov	BYTE PTR 16[rcx], r8b
	jmp	.L831
.L1085:
	cmp	edx, 20
	jle	.L809
	mov	edx, ecx
	shr	ecx, 6
	mov	r9d, 2
	xor	eax, eax
	and	edx, 63
	mov	r10d, ecx
	xor	r11d, r11d
	or	edx, -128
	or	r10d, -64
	jmp	.L811
.L854:
	cmp	ecx, 20
	jle	.L850
	mov	ecx, eax
	and	eax, 63
	or	eax, -128
	shr	ecx, 6
	mov	BYTE PTR 177[rsp], al
	or	ecx, -64
	xor	eax, eax
	mov	WORD PTR 178[rsp], ax
	mov	eax, 2
	mov	BYTE PTR 176[rsp], cl
	jmp	.L855
.L1099:
	xor	r13d, r13d
	mov	r9d, 2
	jmp	.L828
.L947:
.L1079:
	mov	rbx, rax
	jmp	.L925
.L948:
	jmp	.L1079
.L1092:
	lea	rcx, .LC13[rip]
.LEHB12:
	call	_ZSt20__throw_length_errorPKc
.LEHE12:
.L925:
	mov	rcx, QWORD PTR 88[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB13:
	call	_Unwind_Resume
	nop
.LEHE13:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5622:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5622-.LLSDACSB5622
.LLSDACSB5622:
	.uleb128 .LEHB9-.LFB5622
	.uleb128 .LEHE9-.LEHB9
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB10-.LFB5622
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L948-.LFB5622
	.uleb128 0
	.uleb128 .LEHB11-.LFB5622
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L947-.LFB5622
	.uleb128 0
	.uleb128 .LEHB12-.LFB5622
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L948-.LFB5622
	.uleb128 0
	.uleb128 .LEHB13-.LFB5622
	.uleb128 .LEHE13-.LEHB13
	.uleb128 0
	.uleb128 0
.LLSDACSE5622:
	.section	.text$_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	.def	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE:
.LFB5637:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 144
	.seh_stackalloc	144
	.seh_endprologue
	mov	rsi, QWORD PTR [rcx]
	mov	rdi, QWORD PTR 8[rcx]
	mov	r11, rdx
	movzx	edx, WORD PTR [r9]
	mov	r10, r8
	mov	rax, r9
	mov	r8d, DWORD PTR 208[rsp]
	and	dx, 384
	cmp	dx, 128
	je	.L1135
	cmp	dx, 256
	je	.L1103
.L1118:
	mov	rbx, QWORD PTR 16[r10]
	test	rsi, rsi
	jne	.L1136
.L1105:
	mov	rax, rbx
	add	rsp, 144
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L1135:
	movzx	r9d, WORD PTR 4[r9]
.L1102:
	cmp	r11, r9
	jnb	.L1118
	movzx	edx, BYTE PTR [rax]
	mov	eax, DWORD PTR 8[rax]
	mov	QWORD PTR 64[rsp], rsi
	mov	QWORD PTR 72[rsp], rdi
	mov	ecx, edx
	mov	DWORD PTR 32[rsp], eax
	and	ecx, 3
	and	edx, 3
	lea	rdx, 64[rsp]
	cmovne	r8d, ecx
	mov	rcx, QWORD PTR 16[r10]
	sub	r9, r11
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi
	add	rsp, 144
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L1136:
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	rsi, r8
	jb	.L1120
	.p2align 4
	.p2align 3
.L1122:
	test	r8, r8
	je	.L1121
	mov	rdx, rdi
	mov	QWORD PTR 56[rsp], r8
	call	memcpy
	mov	r8, QWORD PTR 56[rsp]
.L1121:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r8
	add	rdi, r8
	sub	rsi, r8
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	rsi, r8
	jnb	.L1122
	test	rsi, rsi
	je	.L1105
.L1120:
	mov	r8, rsi
	mov	rdx, rdi
	call	memcpy
	add	QWORD PTR 24[rbx], rsi
	jmp	.L1105
	.p2align 4,,10
	.p2align 3
.L1103:
	movzx	edx, BYTE PTR [r10]
	movzx	r9d, WORD PTR 4[r9]
	mov	rcx, rdx
	and	ecx, 15
	cmp	r9, rcx
	jnb	.L1106
	mov	rdx, QWORD PTR [r10]
	lea	rcx, [r9+r9*4]
	sal	r9, 4
	add	r9, QWORD PTR 8[r10]
	movdqa	xmm2, XMMWORD PTR [r9]
	shr	rdx, 4
	shr	rdx, cl
	movaps	XMMWORD PTR 80[rsp], xmm2
	and	edx, 31
.L1107:
	mov	BYTE PTR 96[rsp], dl
	lea	rcx, .L1111[rip]
	movzx	edx, dl
	movdqa	xmm0, XMMWORD PTR 80[rsp]
	movsxd	rdx, DWORD PTR [rcx+rdx*4]
	movdqa	xmm1, XMMWORD PTR 96[rsp]
	movaps	XMMWORD PTR 112[rsp], xmm0
	add	rdx, rcx
	movaps	XMMWORD PTR 128[rsp], xmm1
	jmp	rdx
	.section .rdata,"dr"
	.align 4
.L1111:
	.long	.L1108-.L1111
	.long	.L1116-.L1111
	.long	.L1116-.L1111
	.long	.L1115-.L1111
	.long	.L1114-.L1111
	.long	.L1113-.L1111
	.long	.L1112-.L1111
	.long	.L1116-.L1111
	.long	.L1116-.L1111
	.long	.L1116-.L1111
	.long	.L1116-.L1111
	.long	.L1116-.L1111
	.long	.L1116-.L1111
	.long	.L1116-.L1111
	.long	.L1116-.L1111
	.long	.L1116-.L1111
	.section	.text$_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1106:
	and	edx, 15
	jne	.L1108
	mov	rdx, QWORD PTR [r10]
	shr	rdx, 4
	cmp	r9, rdx
	jb	.L1137
.L1108:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L1112:
	mov	r9, QWORD PTR 112[rsp]
	jmp	.L1102
.L1113:
	mov	r9, QWORD PTR 112[rsp]
	test	r9, r9
	jns	.L1102
.L1116:
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L1114:
	mov	r9d, DWORD PTR 112[rsp]
	jmp	.L1102
.L1115:
	movsxd	r9, DWORD PTR 112[rsp]
	test	r9d, r9d
	jns	.L1102
	jmp	.L1116
	.p2align 4,,10
	.p2align 3
.L1137:
	sal	r9, 5
	add	r9, QWORD PTR 8[r10]
	movdqu	xmm3, XMMWORD PTR [r9]
	movzx	edx, BYTE PTR 16[r9]
	movaps	XMMWORD PTR 80[rsp], xmm3
	jmp	.L1107
	.seh_endproc
	.section	.text$_ZNKSt9formatterIPKvcE6formatINSt8__format10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorES1_RS9_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt9formatterIPKvcE6formatINSt8__format10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorES1_RS9_
	.def	_ZNKSt9formatterIPKvcE6formatINSt8__format10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorES1_RS9_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt9formatterIPKvcE6formatINSt8__format10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorES1_RS9_
_ZNKSt9formatterIPKvcE6formatINSt8__format10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorES1_RS9_:
.LFB5449:
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
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	mov	rdi, rcx
	mov	rsi, r8
	test	rdx, rdx
	jne	.L1139
	movzx	eax, BYTE PTR 1[rcx]
	mov	edx, 30768
	mov	BYTE PTR 82[rsp], 48
	mov	ebp, 3
	mov	WORD PTR 80[rsp], dx
	and	eax, 120
	cmp	al, 8
	je	.L1190
.L1141:
	test	BYTE PTR [rdi], 64
	je	.L1191
	movzx	eax, WORD PTR [rdi]
	and	ax, 384
	cmp	ax, 128
	je	.L1192
	cmp	ax, 256
	je	.L1152
.L1155:
	mov	rbx, QWORD PTR 16[rsi]
	test	rbp, rbp
	jne	.L1193
.L1154:
	mov	rax, rbx
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L1191:
	lea	rax, 80[rsp]
	lea	rcx, 48[rsp]
	mov	r9, rdi
	mov	r8, rsi
	mov	DWORD PTR 32[rsp], 2
	mov	rdx, rbp
	mov	QWORD PTR 48[rsp], rbp
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L1139:
	movabs	rcx, 7378413942531504440
	mov	rax, rdx
	bsr	rdx, rdx
	lea	r12d, 4[rdx]
	mov	QWORD PTR 72[rsp], rcx
	movabs	rdx, 3978425819141910832
	mov	QWORD PTR 64[rsp], rdx
	shr	r12d, 2
	cmp	rax, 255
	jbe	.L1142
	lea	edx, -1[r12]
	.p2align 6
	.p2align 4
	.p2align 3
.L1143:
	mov	r8, rax
	mov	ecx, edx
	lea	r10d, -1[rdx]
	sub	edx, 2
	and	r8d, 15
	movzx	r8d, BYTE PTR 64[rsp+r8]
	mov	BYTE PTR 82[rsp+rcx], r8b
	mov	rcx, rax
	shr	rax, 8
	shr	rcx, 4
	and	ecx, 15
	movzx	ecx, BYTE PTR 64[rsp+rcx]
	mov	BYTE PTR 82[rsp+r10], cl
	cmp	rax, 255
	ja	.L1143
.L1142:
	cmp	rax, 15
	jbe	.L1144
	mov	rdx, rax
	shr	rax, 4
	and	edx, 15
	movzx	edx, BYTE PTR 64[rsp+rdx]
	mov	BYTE PTR 83[rsp], dl
	movzx	eax, BYTE PTR 64[rsp+rax]
.L1145:
	mov	BYTE PTR 82[rsp], al
	mov	eax, 30768
	lea	ebp, 2[r12]
	mov	WORD PTR 80[rsp], ax
	movzx	eax, BYTE PTR 1[rdi]
	movsxd	rbp, ebp
	and	eax, 120
	cmp	al, 8
	jne	.L1141
	lea	rbx, 82[rsp]
	add	r12, rbx
.L1140:
	mov	BYTE PTR 81[rsp], 88
	.p2align 4
	.p2align 3
.L1149:
	movsx	ecx, BYTE PTR [rbx]
	add	rbx, 1
	call	toupper
	mov	BYTE PTR -1[rbx], al
	cmp	r12, rbx
	jne	.L1149
	jmp	.L1141
	.p2align 4,,10
	.p2align 3
.L1144:
	movzx	eax, BYTE PTR 64[rsp+rax]
	jmp	.L1145
	.p2align 4,,10
	.p2align 3
.L1190:
	lea	r12, 83[rsp]
	mov	ebp, 3
	lea	rbx, 82[rsp]
	jmp	.L1140
	.p2align 4,,10
	.p2align 3
.L1192:
	movzx	eax, WORD PTR 4[rdi]
	mov	r14, rax
.L1151:
	cmp	rbp, r14
	jnb	.L1155
	mov	rsi, QWORD PTR 16[rsi]
	test	rbp, rbp
	jne	.L1194
.L1161:
	lea	rdx, 82[rsp]
	mov	r9, r14
	lea	rax, -2[rbp]
	mov	rcx, rsi
	mov	QWORD PTR 56[rsp], rdx
	sub	r9, rbp
	lea	rdx, 48[rsp]
	mov	r8d, 2
	mov	DWORD PTR 32[rsp], 48
	mov	QWORD PTR 48[rsp], rax
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L1193:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	lea	rdi, 80[rsp]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	rbp, rsi
	jb	.L1157
	.p2align 4
	.p2align 3
.L1159:
	test	rsi, rsi
	je	.L1158
	mov	r8, rsi
	mov	rdx, rdi
	call	memcpy
.L1158:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rsi
	mov	rcx, rbx
	add	rdi, rsi
	sub	rbp, rsi
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	rbp, rsi
	jnb	.L1159
	test	rbp, rbp
	je	.L1154
.L1157:
	mov	r8, rbp
	mov	rdx, rdi
	call	memcpy
	add	QWORD PTR 24[rbx], rbp
	jmp	.L1154
	.p2align 4,,10
	.p2align 3
.L1194:
	mov	edi, 2
	mov	rcx, QWORD PTR 24[rsi]
	mov	rbx, QWORD PTR 16[rsi]
	lea	r12, 80[rsp]
	cmp	rbp, rdi
	cmovbe	rdi, rbp
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	rbx, rax
	cmp	rdi, rbx
	jb	.L1162
	.p2align 4
	.p2align 3
.L1164:
	test	rbx, rbx
	je	.L1163
	mov	r8, rbx
	mov	rdx, r12
	call	memcpy
.L1163:
	mov	rax, QWORD PTR [rsi]
	add	QWORD PTR 24[rsi], rbx
	mov	rcx, rsi
	add	r12, rbx
	sub	rdi, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rsi]
	mov	rbx, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	rbx, rax
	cmp	rdi, rbx
	jnb	.L1164
	test	rdi, rdi
	je	.L1161
.L1162:
	mov	r8, rdi
	mov	rdx, r12
	call	memcpy
	add	QWORD PTR 24[rsi], rdi
	jmp	.L1161
	.p2align 4,,10
	.p2align 3
.L1152:
	movzx	ecx, WORD PTR 4[rdi]
	mov	rdx, rsi
	call	_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0
	mov	r14, rax
	jmp	.L1151
	.seh_endproc
	.section	.text$_ZNKSt8__format5_SpecIcE16_M_get_precisionISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format5_SpecIcE16_M_get_precisionISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_
	.def	_ZNKSt8__format5_SpecIcE16_M_get_precisionISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format5_SpecIcE16_M_get_precisionISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_
_ZNKSt8__format5_SpecIcE16_M_get_precisionISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_:
.LFB5761:
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	movzx	r8d, BYTE PTR 1[rcx]
	and	r8d, 6
	cmp	r8b, 2
	je	.L1211
	mov	rax, -1
	cmp	r8b, 4
	je	.L1212
.L1195:
	add	rsp, 104
	ret
	.p2align 4,,10
	.p2align 3
.L1212:
	movzx	eax, BYTE PTR [rdx]
	movzx	r8d, WORD PTR 6[rcx]
	mov	rcx, rax
	and	ecx, 15
	cmp	r8, rcx
	jnb	.L1198
	mov	rax, QWORD PTR [rdx]
	lea	rcx, [r8+r8*4]
	sal	r8, 4
	add	r8, QWORD PTR 8[rdx]
	movdqa	xmm1, XMMWORD PTR [r8]
	shr	rax, 4
	shr	rax, cl
	movaps	XMMWORD PTR 32[rsp], xmm1
	and	eax, 31
.L1199:
	lea	rdx, .L1203[rip]
	mov	BYTE PTR 48[rsp], al
	movzx	eax, al
	movdqa	xmm0, XMMWORD PTR 32[rsp]
	movsxd	rax, DWORD PTR [rdx+rax*4]
	movaps	XMMWORD PTR 64[rsp], xmm0
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L1203:
	.long	.L1200-.L1203
	.long	.L1208-.L1203
	.long	.L1208-.L1203
	.long	.L1207-.L1203
	.long	.L1206-.L1203
	.long	.L1205-.L1203
	.long	.L1204-.L1203
	.long	.L1208-.L1203
	.long	.L1208-.L1203
	.long	.L1208-.L1203
	.long	.L1208-.L1203
	.long	.L1208-.L1203
	.long	.L1208-.L1203
	.long	.L1208-.L1203
	.long	.L1208-.L1203
	.long	.L1208-.L1203
	.section	.text$_ZNKSt8__format5_SpecIcE16_M_get_precisionISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1211:
	movzx	eax, WORD PTR 6[rcx]
	add	rsp, 104
	ret
	.p2align 4,,10
	.p2align 3
.L1198:
	test	al, 15
	je	.L1213
.L1200:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L1205:
	mov	rax, QWORD PTR 64[rsp]
	test	rax, rax
	jns	.L1195
.L1208:
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L1206:
	mov	eax, DWORD PTR 64[rsp]
	jmp	.L1195
	.p2align 4,,10
	.p2align 3
.L1207:
	movsxd	rax, DWORD PTR 64[rsp]
	test	eax, eax
	jns	.L1195
	jmp	.L1208
	.p2align 4,,10
	.p2align 3
.L1204:
	mov	rax, QWORD PTR 64[rsp]
	jmp	.L1195
	.p2align 4,,10
	.p2align 3
.L1213:
	mov	rax, QWORD PTR [rdx]
	shr	rax, 4
	cmp	r8, rax
	jnb	.L1200
	sal	r8, 5
	add	r8, QWORD PTR 8[rdx]
	movdqu	xmm2, XMMWORD PTR [r8]
	movzx	eax, BYTE PTR 16[r8]
	movaps	XMMWORD PTR 32[rsp], xmm2
	jmp	.L1199
	.seh_endproc
	.section	.text$_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	.def	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_:
.LFB5923:
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
	movsx	r10, BYTE PTR [r8]
	mov	rax, r10
	mov	r12, rcx
	mov	rcx, QWORD PTR 96[rsp]
	mov	rsi, r9
	mov	r9, QWORD PTR 88[rsp]
	mov	ebx, edx
	mov	rdx, rcx
	sub	rdx, r9
	cmp	rdx, r10
	jle	.L1215
	sub	eax, 1
	cmp	al, 125
	ja	.L1215
	sub	rsi, 1
	xor	r13d, r13d
	xor	r11d, r11d
	jmp	.L1218
	.p2align 4,,10
	.p2align 3
.L1257:
	add	r11, 1
	lea	rbp, [r8+r11]
	movzx	eax, BYTE PTR 0[rbp]
	lea	edx, -1[rax]
	cmp	dl, 125
	ja	.L1220
.L1258:
	mov	rdx, rcx
	movsx	r10, al
	sub	rdx, r9
	cmp	rdx, r10
	jle	.L1220
.L1218:
	sub	rcx, r10
	cmp	r11, rsi
	jb	.L1257
	lea	rbp, [r8+r11]
	add	r13, 1
	movzx	eax, BYTE PTR 0[rbp]
	lea	edx, -1[rax]
	cmp	dl, 125
	jbe	.L1258
.L1220:
	lea	rdi, -1[r13]
	lea	rsi, -1[r11]
	cmp	r9, rcx
	je	.L1259
.L1221:
	mov	r10, rcx
	xor	eax, eax
	sub	r10, r9
	.p2align 5
	.p2align 4
	.p2align 3
.L1224:
	movzx	edx, BYTE PTR [r9+rax]
	mov	BYTE PTR [r12+rax], dl
	add	rax, 1
	cmp	rax, r10
	jne	.L1224
	mov	rdx, r12
	sub	rdx, r9
	add	rdx, rcx
.L1223:
	test	r13, r13
	je	.L1225
	.p2align 4
	.p2align 3
.L1228:
	mov	BYTE PTR [rdx], bl
	movzx	r10d, BYTE PTR 0[rbp]
	lea	r12, 1[rdx]
	test	r10b, r10b
	jle	.L1234
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L1227:
	movzx	r9d, BYTE PTR [rcx+rax]
	mov	BYTE PTR 1[rdx+rax], r9b
	add	rax, 1
	cmp	rax, r10
	jne	.L1227
	lea	rdx, [r12+rax]
	add	rcx, rax
.L1226:
	sub	rdi, 1
	jnb	.L1228
.L1225:
	test	r11, r11
	je	.L1214
	.p2align 4
	.p2align 3
.L1231:
	mov	BYTE PTR [rdx], bl
	movzx	r10d, BYTE PTR [r8+rsi]
	lea	rdi, 1[rdx]
	test	r10b, r10b
	jle	.L1235
	lea	r11d, -1[r10]
	xor	eax, eax
	movzx	r11d, r11b
	.p2align 5
	.p2align 4
	.p2align 3
.L1230:
	movzx	r9d, BYTE PTR [rcx+rax]
	mov	BYTE PTR 1[rdx+rax], r9b
	add	rax, 1
	cmp	r10, rax
	jne	.L1230
	lea	rdx, 1[rdi+r11]
	lea	rcx, 1[rcx+r11]
.L1229:
	sub	rsi, 1
	jnb	.L1231
.L1214:
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
.L1235:
	mov	rdx, rdi
	jmp	.L1229
	.p2align 4,,10
	.p2align 3
.L1234:
	mov	rdx, r12
	jmp	.L1226
.L1215:
	mov	rdx, r12
	cmp	rcx, r9
	je	.L1214
	mov	rbp, r8
	mov	rsi, -1
	xor	r13d, r13d
	xor	r11d, r11d
	mov	rdi, -1
	jmp	.L1221
.L1259:
	mov	rdx, r12
	jmp	.L1223
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	.def	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_:
.LFB5753:
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
	sub	rsp, 184
	.seh_stackalloc	184
	lea	rbp, 176[rsp]
	.seh_setframe	rbp, 176
	.seh_endprologue
	movzx	eax, WORD PTR [rcx]
	mov	r14, QWORD PTR [rdx]
	mov	r12, QWORD PTR 8[rdx]
	and	ax, 384
	mov	QWORD PTR 96[rbp], r8
	mov	r15, rcx
	mov	rsi, r9
	cmp	ax, 128
	je	.L1347
	cmp	ax, 256
	je	.L1263
	mov	rbx, r14
	mov	rdi, r12
	test	BYTE PTR [rcx], 32
	jne	.L1348
.L1265:
	mov	rsi, QWORD PTR 16[rsi]
	test	rbx, rbx
	jne	.L1349
.L1293:
	mov	rax, rsi
.L1345:
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
.L1347:
	movzx	r13d, WORD PTR 4[rcx]
.L1262:
	mov	rbx, r14
	mov	rdi, r12
	test	BYTE PTR [r15], 32
	jne	.L1264
.L1278:
	cmp	rbx, r13
	jnb	.L1265
	movzx	eax, BYTE PTR [r15]
	mov	r9, r13
	mov	rsi, QWORD PTR 16[rsi]
	sub	r9, rbx
	mov	r8d, eax
	and	r8d, 3
	je	.L1298
	mov	eax, DWORD PTR 8[r15]
.L1299:
	mov	QWORD PTR -80[rbp], rbx
	lea	rdx, -80[rbp]
	mov	rcx, rsi
	mov	QWORD PTR -72[rbp], rdi
	mov	DWORD PTR 32[rsp], eax
.LEHB14:
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi
.LEHE14:
	jmp	.L1345
	.p2align 4,,10
	.p2align 3
.L1298:
	mov	r8d, 2
	test	al, 64
	je	.L1309
	mov	eax, 48
	cmp	QWORD PTR 96[rbp], 0
	je	.L1299
	cmp	QWORD PTR 96[rbp], rbx
	mov	r15, rbx
	cmovbe	r15, QWORD PTR 96[rbp]
	test	r15, r15
	jne	.L1350
.L1300:
	add	rdi, QWORD PTR 96[rbp]
	sub	rbx, QWORD PTR 96[rbp]
	mov	r8d, 2
	mov	eax, 48
	jmp	.L1299
	.p2align 4,,10
	.p2align 3
.L1348:
	xor	r13d, r13d
.L1264:
	lea	rdx, 24[rsi]
	cmp	BYTE PTR 32[rsi], 0
	je	.L1351
.L1279:
	lea	rax, -64[rbp]
	mov	rcx, rax
	mov	QWORD PTR -88[rbp], rax
	call	_ZNSt6localeC1ERKS_
	lea	rax, -32[rbp]
	mov	rdx, QWORD PTR -88[rbp]
	mov	rcx, rax
	mov	QWORD PTR -96[rbp], rax
.LEHB15:
	call	_ZNKSt6locale4nameB5cxx11Ev
	mov	rcx, QWORD PTR -32[rbp]
	lea	rax, -16[rbp]
	cmp	QWORD PTR -24[rbp], 1
	je	.L1352
.L1281:
	mov	QWORD PTR -104[rbp], rax
	cmp	rcx, rax
	je	.L1284
	mov	rax, QWORD PTR -16[rbp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1284:
	mov	rcx, QWORD PTR .refptr._ZNSt7__cxx118numpunctIcE2idE[rip]
	call	_ZNKSt6locale2id5_M_idEv
	mov	rdx, rax
	mov	rax, QWORD PTR -64[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	r9, QWORD PTR [rax+rdx*8]
	test	r9, r9
	je	.L1287
	mov	rax, QWORD PTR [r9]
	mov	rcx, QWORD PTR -96[rbp]
	mov	QWORD PTR -112[rbp], r9
	mov	rdx, r9
	call	[QWORD PTR 32[rax]]
.LEHE15:
	mov	r11, QWORD PTR -24[rbp]
	mov	r9, QWORD PTR -112[rbp]
	test	r11, r11
	je	.L1289
	mov	rdi, QWORD PTR 96[rbp]
	mov	rax, r14
	sub	rax, QWORD PTR 96[rbp]
	lea	rax, 15[rdi+rax*2]
	and	rax, -16
	call	___chkstk_ms
	sub	rsp, rax
	lea	rdi, 48[rsp]
	mov	QWORD PTR -112[rbp], rdi
	cmp	QWORD PTR 96[rbp], 0
	je	.L1290
	mov	r8, QWORD PTR 96[rbp]
	mov	rdx, r12
	mov	rcx, rdi
	mov	QWORD PTR -128[rbp], r9
	mov	QWORD PTR -120[rbp], r11
	call	memcpy
	mov	r9, QWORD PTR -128[rbp]
	mov	r11, QWORD PTR -120[rbp]
.L1290:
	mov	rbx, QWORD PTR 96[rbp]
	mov	rax, QWORD PTR [r9]
	mov	QWORD PTR -120[rbp], r11
	mov	rcx, r9
	add	rbx, r12
	add	r12, r14
	mov	r14, QWORD PTR -32[rbp]
.LEHB16:
	call	[QWORD PTR 24[rax]]
.LEHE16:
	mov	rcx, QWORD PTR 96[rbp]
	mov	QWORD PTR 32[rsp], rbx
	movsx	edx, al
	mov	r8, r14
	mov	QWORD PTR 40[rsp], r12
	mov	r9, QWORD PTR -120[rbp]
	add	rcx, rdi
	call	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	mov	rcx, QWORD PTR -32[rbp]
	sub	rax, rdi
	mov	rbx, rax
	cmp	rcx, QWORD PTR -104[rbp]
	je	.L1286
.L1306:
	mov	rax, QWORD PTR -16[rbp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	rdi, QWORD PTR -112[rbp]
.L1286:
	mov	rcx, QWORD PTR -88[rbp]
	call	_ZNSt6localeD1Ev
	jmp	.L1278
	.p2align 4,,10
	.p2align 3
.L1309:
	mov	eax, 32
	jmp	.L1299
	.p2align 4,,10
	.p2align 3
.L1263:
	movzx	eax, BYTE PTR [r9]
	movzx	edx, WORD PTR 4[rcx]
	mov	rcx, rax
	and	ecx, 15
	cmp	rdx, rcx
	jnb	.L1266
	mov	rax, QWORD PTR [r9]
	lea	rcx, [rdx+rdx*4]
	sal	rdx, 4
	add	rdx, QWORD PTR 8[r9]
	movdqa	xmm2, XMMWORD PTR [rdx]
	shr	rax, 4
	shr	rax, cl
	movaps	XMMWORD PTR -64[rbp], xmm2
	and	eax, 31
.L1267:
	mov	BYTE PTR -48[rbp], al
	lea	rdx, .L1271[rip]
	movzx	eax, al
	movdqa	xmm0, XMMWORD PTR -64[rbp]
	movsxd	rax, DWORD PTR [rdx+rax*4]
	movdqa	xmm1, XMMWORD PTR -48[rbp]
	movaps	XMMWORD PTR -32[rbp], xmm0
	add	rax, rdx
	movaps	XMMWORD PTR -16[rbp], xmm1
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L1271:
	.long	.L1268-.L1271
	.long	.L1276-.L1271
	.long	.L1276-.L1271
	.long	.L1275-.L1271
	.long	.L1274-.L1271
	.long	.L1273-.L1271
	.long	.L1272-.L1271
	.long	.L1276-.L1271
	.long	.L1276-.L1271
	.long	.L1276-.L1271
	.long	.L1276-.L1271
	.long	.L1276-.L1271
	.long	.L1276-.L1271
	.long	.L1276-.L1271
	.long	.L1276-.L1271
	.long	.L1276-.L1271
	.section	.text$_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1352:
	cmp	BYTE PTR [rcx], 67
	jne	.L1281
	cmp	rcx, rax
	je	.L1286
	mov	rax, QWORD PTR -16[rbp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L1286
	.p2align 4,,10
	.p2align 3
.L1349:
	mov	rcx, QWORD PTR 24[rsi]
	mov	r12, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	r12, rax
	cmp	rbx, r12
	jb	.L1294
	.p2align 4
	.p2align 3
.L1296:
	test	r12, r12
	je	.L1295
	mov	r8, r12
	mov	rdx, rdi
	call	memcpy
.L1295:
	mov	rax, QWORD PTR [rsi]
	add	QWORD PTR 24[rsi], r12
	mov	rcx, rsi
	add	rdi, r12
	sub	rbx, r12
.LEHB17:
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rsi]
	mov	r12, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	r12, rax
	cmp	rbx, r12
	jnb	.L1296
	test	rbx, rbx
	je	.L1293
.L1294:
	mov	r8, rbx
	mov	rdx, rdi
	call	memcpy
	add	QWORD PTR 24[rsi], rbx
	jmp	.L1293
	.p2align 4,,10
	.p2align 3
.L1351:
	mov	rcx, rdx
	mov	QWORD PTR -88[rbp], rdx
	call	_ZNSt6localeC1Ev
	mov	BYTE PTR 32[rsi], 1
	mov	rdx, QWORD PTR -88[rbp]
	jmp	.L1279
	.p2align 4,,10
	.p2align 3
.L1266:
	test	al, 15
	jne	.L1268
	mov	rax, QWORD PTR [r9]
	shr	rax, 4
	cmp	rdx, rax
	jb	.L1353
.L1268:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L1289:
	mov	rcx, QWORD PTR -32[rbp]
	cmp	rcx, QWORD PTR -104[rbp]
	je	.L1286
	mov	QWORD PTR -112[rbp], r12
	jmp	.L1306
	.p2align 4,,10
	.p2align 3
.L1350:
	mov	rcx, QWORD PTR 24[rsi]
	mov	r13, QWORD PTR 16[rsi]
	mov	r14, rdi
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	r13, rax
	cmp	r15, r13
	jb	.L1301
	mov	r12, r9
	.p2align 4
	.p2align 3
.L1303:
	test	r13, r13
	je	.L1302
	mov	r8, r13
	mov	rdx, r14
	call	memcpy
.L1302:
	mov	rax, QWORD PTR [rsi]
	add	QWORD PTR 24[rsi], r13
	mov	rcx, rsi
	add	r14, r13
	sub	r15, r13
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rsi]
	mov	r13, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	r13, rax
	cmp	r15, r13
	jnb	.L1303
	mov	r9, r12
	test	r15, r15
	je	.L1300
.L1301:
	mov	r8, r15
	mov	rdx, r14
	mov	QWORD PTR -88[rbp], r9
	call	memcpy
	add	QWORD PTR 24[rsi], r15
	mov	r9, QWORD PTR -88[rbp]
	jmp	.L1300
.L1273:
	mov	r13, QWORD PTR -32[rbp]
	test	r13, r13
	jns	.L1262
.L1276:
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_format_errorPKc
.LEHE17:
	.p2align 4,,10
	.p2align 3
.L1274:
	mov	r13d, DWORD PTR -32[rbp]
	jmp	.L1262
.L1275:
	movsxd	r13, DWORD PTR -32[rbp]
	test	r13d, r13d
	jns	.L1262
	jmp	.L1276
	.p2align 4,,10
	.p2align 3
.L1272:
	mov	r13, QWORD PTR -32[rbp]
	jmp	.L1262
	.p2align 4,,10
	.p2align 3
.L1353:
	sal	rdx, 5
	add	rdx, QWORD PTR 8[r9]
	movdqu	xmm3, XMMWORD PTR [rdx]
	movaps	XMMWORD PTR -64[rbp], xmm3
	movzx	eax, BYTE PTR 16[rdx]
	mov	BYTE PTR -48[rbp], al
	movzx	eax, BYTE PTR 16[rdx]
	jmp	.L1267
.L1313:
	mov	rbx, rax
	jmp	.L1304
.L1312:
	mov	rbx, rax
	jmp	.L1305
.L1287:
.LEHB18:
	call	_ZSt16__throw_bad_castv
.LEHE18:
.L1304:
	mov	rcx, QWORD PTR -96[rbp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L1305:
	mov	rcx, QWORD PTR -88[rbp]
	call	_ZNSt6localeD1Ev
	mov	rcx, rbx
.LEHB19:
	call	_Unwind_Resume
	nop
.LEHE19:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5753:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5753-.LLSDACSB5753
.LLSDACSB5753:
	.uleb128 .LEHB14-.LFB5753
	.uleb128 .LEHE14-.LEHB14
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB15-.LFB5753
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L1312-.LFB5753
	.uleb128 0
	.uleb128 .LEHB16-.LFB5753
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L1313-.LFB5753
	.uleb128 0
	.uleb128 .LEHB17-.LFB5753
	.uleb128 .LEHE17-.LEHB17
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB18-.LFB5753
	.uleb128 .LEHE18-.LEHB18
	.uleb128 .L1312-.LFB5753
	.uleb128 0
	.uleb128 .LEHB19-.LFB5753
	.uleb128 .LEHE19-.LEHB19
	.uleb128 0
	.uleb128 0
.LLSDACSE5753:
	.section	.text$_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC26:
	.ascii "0b\0"
.LC27:
	.ascii "0B\0"
.LC28:
	.ascii "0X\0"
.LC29:
	.ascii "0x\0"
.LC30:
	.ascii "0\0"
	.align 8
.LC31:
	.ascii "format error: integer not representable as character\0"
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5592:
	push	r12
	.seh_pushreg	r12
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 312
	.seh_stackalloc	312
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	r10, rcx
	mov	ecx, eax
	mov	r11d, edx
	and	ecx, 120
	cmp	cl, 56
	je	.L1411
	shr	al, 3
	and	eax, 15
	cmp	al, 4
	je	.L1358
	ja	.L1359
	cmp	al, 1
	jbe	.L1360
	lea	rbx, .LC26[rip]
	cmp	cl, 16
	lea	rax, .LC27[rip]
	cmove	rax, rbx
	mov	rsi, rax
	test	dl, dl
	jne	.L1412
	mov	eax, 48
	lea	r9, 88[rsp]
	lea	rbx, 87[rsp]
.L1365:
	mov	BYTE PTR 87[rsp], al
	movzx	eax, BYTE PTR [r10]
	test	al, 16
	je	.L1410
.L1399:
	mov	rdx, -2
	mov	ecx, 2
.L1369:
	add	rdx, rbx
	mov	edi, ecx
	test	ecx, ecx
	je	.L1370
	xor	ecx, ecx
.L1388:
	mov	r11d, ecx
	add	ecx, 1
	movzx	r12d, BYTE PTR [rsi+r11]
	mov	BYTE PTR [rdx+r11], r12b
	cmp	ecx, edi
	jb	.L1388
	jmp	.L1370
	.p2align 4,,10
	.p2align 3
.L1411:
	test	dl, dl
	js	.L1356
	mov	DWORD PTR 32[rsp], 1
	lea	rax, 96[rsp]
	lea	rcx, 64[rsp]
	mov	r9, r10
	mov	BYTE PTR 96[rsp], dl
	mov	edx, 1
	mov	QWORD PTR 64[rsp], 1
	mov	QWORD PTR 72[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	add	rsp, 312
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L1360:
	test	dl, dl
	je	.L1376
	movzx	eax, dl
	cmp	dl, 9
	jbe	.L1395
	movabs	rcx, 3688503277381496880
	movabs	rbx, 3976738051646829616
	mov	QWORD PTR 96[rsp], rcx
	movabs	rcx, 3544667369688283184
	mov	QWORD PTR 104[rsp], rbx
	movabs	rbx, 3832902143785906737
	mov	QWORD PTR 112[rsp], rcx
	movabs	rcx, 4121136918051239473
	mov	QWORD PTR 120[rsp], rbx
	movabs	rbx, 3689066235924983858
	mov	QWORD PTR 128[rsp], rcx
	movabs	rcx, 3977301010190316594
	mov	QWORD PTR 136[rsp], rbx
	movabs	rbx, 3545230328231770162
	mov	QWORD PTR 144[rsp], rcx
	movabs	rcx, 3833465102329393715
	mov	QWORD PTR 152[rsp], rbx
	movabs	rbx, 4121699876594726451
	mov	QWORD PTR 160[rsp], rcx
	movabs	rcx, 3689629194468470836
	mov	QWORD PTR 168[rsp], rbx
	movabs	rbx, 3977863968733803572
	mov	QWORD PTR 176[rsp], rcx
	movabs	rcx, 3545793286775257140
	mov	QWORD PTR 184[rsp], rbx
	movabs	rbx, 3834028060872880693
	mov	QWORD PTR 192[rsp], rcx
	movabs	rcx, 4122262835138213429
	mov	QWORD PTR 200[rsp], rbx
	movabs	rbx, 3690192153011957814
	mov	QWORD PTR 208[rsp], rcx
	movabs	rcx, 3978426927277290550
	mov	QWORD PTR 216[rsp], rbx
	movabs	rbx, 3546356245318744118
	mov	QWORD PTR 224[rsp], rcx
	movabs	rcx, 3834591019416367671
	mov	QWORD PTR 232[rsp], rbx
	movabs	rbx, 4122825793681700407
	mov	QWORD PTR 240[rsp], rcx
	movabs	rcx, 3690755111555444792
	mov	QWORD PTR 248[rsp], rbx
	movabs	rbx, 3978989885820777528
	mov	QWORD PTR 256[rsp], rcx
	movabs	rcx, 3546919203862231096
	mov	QWORD PTR 264[rsp], rbx
	movabs	rbx, 3835153977959854649
	mov	QWORD PTR 280[rsp], rbx
	movabs	rbx, 16106987313379638
	mov	QWORD PTR 272[rsp], rcx
	movabs	rcx, 4122263930388298034
	mov	QWORD PTR 281[rsp], rcx
	mov	QWORD PTR 289[rsp], rbx
	cmp	eax, 99
	jbe	.L1413
	mov	r11d, eax
	imul	r11, r11, 1374389535
	shr	r11, 37
	imul	edx, r11d, 100
	sub	eax, edx
	lea	eax, 1[rax+rax]
	movzx	eax, WORD PTR 95[rsp+rax]
	mov	WORD PTR 88[rsp], ax
	mov	eax, 3
.L1373:
	add	r11d, 48
.L1375:
	mov	BYTE PTR 87[rsp], r11b
	lea	rbx, 87[rsp]
	lea	r9, [rbx+rax]
.L1409:
	movzx	eax, BYTE PTR [r10]
	mov	rdx, rbx
.L1370:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L1414
	cmp	eax, 3
	je	.L1401
.L1391:
	sub	rbx, rdx
	mov	rax, r9
	mov	QWORD PTR 72[rsp], rdx
	mov	r9, r8
	sub	rax, rdx
	mov	r8, rbx
	lea	rdx, 64[rsp]
	mov	rcx, r10
	mov	QWORD PTR 64[rsp], rax
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	add	rsp, 312
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L1358:
	test	dl, dl
	je	.L1376
	movzx	ecx, dl
	bsr	eax, ecx
	lea	r9d, 3[rax]
	mov	eax, 2863311531
	imul	r9, rax
	shr	r9, 33
	cmp	ecx, 63
	jbe	.L1415
	mov	eax, ecx
	and	edx, 7
	shr	ecx, 6
	shr	eax, 3
	add	edx, 48
	and	eax, 7
	mov	BYTE PTR 89[rsp], dl
	add	eax, 48
	mov	BYTE PTR 88[rsp], al
.L1379:
	add	ecx, 48
.L1380:
	lea	rbx, 87[rsp]
	mov	BYTE PTR 87[rsp], cl
	lea	rsi, .LC30[rip]
	mov	ecx, 1
	add	r9, rbx
.L1381:
	movzx	eax, BYTE PTR [r10]
	mov	rdx, rbx
	test	al, 16
	je	.L1370
	mov	rdx, rcx
	neg	rdx
	jmp	.L1369
	.p2align 4,,10
	.p2align 3
.L1414:
	mov	eax, 43
.L1392:
	mov	BYTE PTR -1[rdx], al
	sub	rdx, 1
	jmp	.L1391
	.p2align 4,,10
	.p2align 3
.L1376:
	mov	BYTE PTR 87[rsp], 48
	lea	r9, 88[rsp]
	lea	rbx, 87[rsp]
	jmp	.L1409
	.p2align 4,,10
	.p2align 3
.L1359:
	cmp	cl, 40
	je	.L1416
	test	dl, dl
	jne	.L1397
	mov	BYTE PTR 87[rsp], 48
	cmp	cl, 48
	je	.L1398
	lea	rsi, .LC28[rip]
	lea	r9, 88[rsp]
	lea	rbx, 87[rsp]
	jmp	.L1383
	.p2align 4,,10
	.p2align 3
.L1401:
	mov	eax, 32
	jmp	.L1392
	.p2align 4,,10
	.p2align 3
.L1397:
	lea	rsi, .LC28[rip]
.L1382:
	movabs	r11, 3978425819141910832
	movzx	ebx, dl
	movabs	r12, 7378413942531504440
	bsr	eax, ebx
	mov	QWORD PTR 96[rsp], r11
	add	eax, 4
	mov	QWORD PTR 104[rsp], r12
	shr	eax, 2
	cmp	ebx, 15
	ja	.L1417
	movzx	edx, BYTE PTR 96[rsp+rbx]
.L1386:
	lea	rbx, 87[rsp]
	mov	BYTE PTR 87[rsp], dl
	lea	r9, [rbx+rax]
	cmp	cl, 48
	je	.L1384
.L1383:
	movzx	eax, BYTE PTR [r10]
	test	al, 16
	jne	.L1399
.L1410:
	mov	rdx, rbx
	jmp	.L1370
	.p2align 4,,10
	.p2align 3
.L1412:
	movzx	edx, dl
	mov	eax, 32
	bsr	r9d, edx
	xor	r9d, 31
	sub	eax, r9d
	cdqe
	cmp	edx, 1
	je	.L1368
	mov	ebx, 31
	mov	r11d, 30
	sub	ebx, r9d
	sub	r11d, r9d
	lea	rcx, 84[rsp+rbx]
	lea	rbx, 83[rsp+rbx]
	sub	rbx, r11
	.p2align 5
	.p2align 4
	.p2align 3
.L1367:
	mov	r9d, edx
	sub	rcx, 1
	shr	edx
	and	r9d, 1
	add	r9d, 48
	mov	BYTE PTR 4[rcx], r9b
	cmp	rcx, rbx
	jne	.L1367
.L1368:
	lea	rbx, 87[rsp]
	lea	r9, [rbx+rax]
	mov	eax, 49
	jmp	.L1365
	.p2align 4,,10
	.p2align 3
.L1416:
	test	dl, dl
	jne	.L1396
	mov	BYTE PTR 87[rsp], 48
	lea	r9, 88[rsp]
	lea	rbx, 87[rsp]
	lea	rsi, .LC29[rip]
	jmp	.L1383
	.p2align 4,,10
	.p2align 3
.L1417:
	and	edx, 15
	shr	ebx, 4
	movzx	edx, BYTE PTR 96[rsp+rdx]
	mov	BYTE PTR 88[rsp], dl
	movzx	edx, BYTE PTR 96[rsp+rbx]
	jmp	.L1386
	.p2align 4,,10
	.p2align 3
.L1396:
	lea	rsi, .LC29[rip]
	jmp	.L1382
	.p2align 4,,10
	.p2align 3
.L1398:
	lea	r9, 88[rsp]
	lea	rsi, .LC28[rip]
	lea	rbx, 87[rsp]
.L1384:
	mov	rdx, rbx
	.p2align 4
	.p2align 3
.L1387:
	movsx	ecx, BYTE PTR [rdx]
	mov	QWORD PTR 368[rsp], r8
	mov	QWORD PTR 352[rsp], r10
	mov	QWORD PTR 56[rsp], r9
	mov	QWORD PTR 48[rsp], rdx
	call	toupper
	mov	rdx, QWORD PTR 48[rsp]
	mov	r9, QWORD PTR 56[rsp]
	mov	r10, QWORD PTR 352[rsp]
	mov	r8, QWORD PTR 368[rsp]
	mov	BYTE PTR [rdx], al
	add	rdx, 1
	cmp	rdx, r9
	jne	.L1387
	mov	ecx, 2
	jmp	.L1381
.L1413:
	add	eax, eax
	lea	edx, 1[rax]
	movzx	r11d, BYTE PTR 96[rsp+rax]
	mov	eax, 2
	movzx	edx, BYTE PTR 96[rsp+rdx]
	mov	BYTE PTR 88[rsp], dl
	jmp	.L1375
.L1395:
	mov	eax, 1
	jmp	.L1373
.L1415:
	cmp	ecx, 7
	jbe	.L1379
	and	edx, 7
	shr	ecx, 3
	add	edx, 48
	add	ecx, 48
	mov	BYTE PTR 88[rsp], dl
	jmp	.L1380
.L1356:
	lea	rcx, .LC31[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_:
.LFB5575:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 160
	.seh_stackalloc	160
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	and	eax, 120
	mov	r10, rcx
	mov	r9d, edx
	mov	r11, r8
	cmp	al, 56
	je	.L1488
	test	al, al
	jne	.L1489
	lea	rbx, 112[rsp]
	mov	BYTE PTR 112[rsp], 0
	mov	QWORD PTR 96[rsp], rbx
	mov	QWORD PTR 104[rsp], 0
	test	BYTE PTR [rcx], 32
	jne	.L1490
	test	dl, dl
	jne	.L1456
	mov	eax, 5
	lea	rdx, .LC7[rip]
.L1443:
	lea	rcx, 96[rsp]
	mov	rsi, rcx
	cmp	rdx, rbx
	je	.L1491
	mov	r8d, eax
	xor	ecx, ecx
	test	al, 4
	jne	.L1492
	and	r8d, 1
	jne	.L1493
.L1448:
	mov	rdx, rbx
.L1445:
	mov	QWORD PTR 104[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
.L1487:
	mov	rdx, QWORD PTR 104[rsp]
	mov	rax, QWORD PTR 96[rsp]
	mov	r9, r10
	mov	r8, r11
	mov	DWORD PTR 32[rsp], 1
	lea	rcx, 80[rsp]
	lea	rsi, 96[rsp]
	mov	QWORD PTR 80[rsp], rdx
	mov	QWORD PTR 88[rsp], rax
.LEHB20:
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.LEHE20:
	mov	rcx, QWORD PTR 96[rsp]
	cmp	rcx, rbx
	je	.L1465
	mov	QWORD PTR 48[rsp], rax
	mov	rax, QWORD PTR 112[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	rax, QWORD PTR 48[rsp]
.L1465:
	add	rsp, 160
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L1489:
	movzx	edx, dl
	add	rsp, 160
	pop	rbx
	pop	rsi
	pop	rdi
.LEHB21:
	jmp	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.p2align 4,,10
	.p2align 3
.L1456:
	mov	eax, 4
	lea	rdx, .LC8[rip]
	jmp	.L1443
	.p2align 4,,10
	.p2align 3
.L1488:
	mov	DWORD PTR 32[rsp], 1
	lea	rax, 128[rsp]
	lea	rcx, 80[rsp]
	mov	r9, r10
	mov	BYTE PTR 128[rsp], dl
	mov	edx, 1
	mov	QWORD PTR 80[rsp], 1
	mov	QWORD PTR 88[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.LEHE21:
	add	rsp, 160
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L1493:
	movzx	edx, BYTE PTR [rdx+rcx]
	mov	BYTE PTR 112[rsp+rcx], dl
	jmp	.L1448
	.p2align 4,,10
	.p2align 3
.L1492:
	mov	ecx, DWORD PTR [rdx]
	and	r8d, 1
	mov	DWORD PTR 112[rsp], ecx
	mov	ecx, 4
	je	.L1448
	jmp	.L1493
	.p2align 4,,10
	.p2align 3
.L1490:
	lea	rdx, 24[r8]
	cmp	BYTE PTR 32[r8], 0
	je	.L1494
.L1423:
	lea	rcx, 128[rsp]
	mov	QWORD PTR 72[rsp], r11
	lea	rdi, 128[rsp]
	mov	DWORD PTR 64[rsp], r9d
	mov	QWORD PTR 56[rsp], r10
	call	_ZNSt6localeC1ERKS_
	mov	rcx, QWORD PTR .refptr._ZNSt7__cxx118numpunctIcE2idE[rip]
	call	_ZNKSt6locale2id5_M_idEv
	mov	rdx, rax
	mov	rax, QWORD PTR 128[rsp]
	mov	rax, QWORD PTR 8[rax]
	mov	rdx, QWORD PTR [rax+rdx*8]
	test	rdx, rdx
	je	.L1424
	lea	rcx, 128[rsp]
	mov	QWORD PTR 48[rsp], rdx
	call	_ZNSt6localeD1Ev
	mov	rdx, QWORD PTR 48[rsp]
	cmp	BYTE PTR 64[rsp], 0
	mov	r10, QWORD PTR 56[rsp]
	mov	r11, QWORD PTR 72[rsp]
	mov	rax, QWORD PTR [rdx]
	jne	.L1425
	mov	QWORD PTR 56[rsp], r11
	lea	rsi, 96[rsp]
	mov	rcx, rdi
	mov	QWORD PTR 48[rsp], r10
.LEHB22:
	call	[QWORD PTR 48[rax]]
	mov	r11, QWORD PTR 56[rsp]
	mov	r10, QWORD PTR 48[rsp]
.L1427:
	mov	rax, QWORD PTR 96[rsp]
	mov	r9, rax
	cmp	rax, rbx
	je	.L1495
	mov	r8, QWORD PTR 128[rsp]
	lea	rdx, 144[rsp]
	mov	rcx, QWORD PTR 136[rsp]
	cmp	r8, rdx
	je	.L1453
	mov	r9, QWORD PTR 112[rsp]
	movq	xmm0, rcx
	mov	QWORD PTR 96[rsp], r8
	movhps	xmm0, QWORD PTR 144[rsp]
	movups	XMMWORD PTR 104[rsp], xmm0
	test	rax, rax
	je	.L1440
	mov	QWORD PTR 128[rsp], rax
	mov	QWORD PTR 144[rsp], r9
.L1439:
	mov	BYTE PTR [rax], 0
	mov	rcx, QWORD PTR 128[rsp]
	cmp	rcx, rdx
	je	.L1487
	mov	rax, QWORD PTR 144[rsp]
	mov	QWORD PTR 56[rsp], r11
	mov	QWORD PTR 48[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r11, QWORD PTR 56[rsp]
	mov	r10, QWORD PTR 48[rsp]
	jmp	.L1487
	.p2align 4,,10
	.p2align 3
.L1425:
	mov	QWORD PTR 56[rsp], r11
	lea	rsi, 96[rsp]
	mov	rcx, rdi
	mov	QWORD PTR 48[rsp], r10
	call	[QWORD PTR 40[rax]]
.LEHE22:
	mov	r10, QWORD PTR 48[rsp]
	mov	r11, QWORD PTR 56[rsp]
	jmp	.L1427
	.p2align 4,,10
	.p2align 3
.L1494:
	mov	QWORD PTR 56[rsp], rcx
	mov	rcx, rdx
	mov	DWORD PTR 64[rsp], r9d
	mov	QWORD PTR 48[rsp], rdx
	mov	QWORD PTR 72[rsp], r8
	call	_ZNSt6localeC1Ev
	mov	r11, QWORD PTR 72[rsp]
	mov	r9d, DWORD PTR 64[rsp]
	mov	r10, QWORD PTR 56[rsp]
	mov	rdx, QWORD PTR 48[rsp]
	mov	BYTE PTR 32[r11], 1
	jmp	.L1423
.L1495:
	mov	rax, QWORD PTR 128[rsp]
	lea	rdx, 144[rsp]
	mov	rcx, QWORD PTR 136[rsp]
	cmp	rax, rdx
	je	.L1453
	movq	xmm0, QWORD PTR 136[rsp]
	mov	QWORD PTR 96[rsp], rax
	movhps	xmm0, QWORD PTR 144[rsp]
	movups	XMMWORD PTR 104[rsp], xmm0
.L1440:
	mov	QWORD PTR 128[rsp], rdx
	lea	rdx, 144[rsp]
	mov	rax, rdx
	jmp	.L1439
.L1453:
	test	rcx, rcx
	je	.L1430
	cmp	rcx, 1
	je	.L1496
	mov	eax, ecx
	cmp	ecx, 8
	jnb	.L1433
	test	cl, 4
	jne	.L1497
	test	ecx, ecx
	je	.L1430
	movzx	ecx, BYTE PTR 144[rsp]
	mov	BYTE PTR [r9], cl
	test	al, 2
	jne	.L1482
.L1486:
	mov	r9, QWORD PTR 96[rsp]
	mov	rcx, QWORD PTR 136[rsp]
.L1430:
	mov	QWORD PTR 104[rsp], rcx
	mov	BYTE PTR [r9+rcx], 0
	mov	rax, QWORD PTR 128[rsp]
	jmp	.L1439
.L1433:
	mov	rax, QWORD PTR 144[rsp]
	mov	rsi, rdx
	mov	QWORD PTR [r9], rax
	mov	eax, ecx
	mov	r8, QWORD PTR -8[rdx+rax]
	mov	QWORD PTR -8[r9+rax], r8
	lea	r8, 8[r9]
	mov	rax, r9
	and	r8, -8
	sub	rax, r8
	sub	rsi, rax
	add	eax, ecx
	and	eax, -8
	mov	rdi, rsi
	cmp	eax, 8
	jb	.L1486
	and	eax, -8
	xor	ecx, ecx
.L1437:
	mov	r9d, ecx
	add	ecx, 8
	mov	rsi, QWORD PTR [rdi+r9]
	mov	QWORD PTR [r8+r9], rsi
	cmp	ecx, eax
	jb	.L1437
	jmp	.L1486
.L1496:
	movzx	eax, BYTE PTR 144[rsp]
	mov	BYTE PTR [r9], al
	mov	r9, QWORD PTR 96[rsp]
	mov	rcx, QWORD PTR 136[rsp]
	jmp	.L1430
.L1497:
	mov	ecx, DWORD PTR 144[rsp]
	mov	DWORD PTR [r9], ecx
	mov	ecx, DWORD PTR -4[rdx+rax]
	mov	DWORD PTR -4[r9+rax], ecx
	mov	r9, QWORD PTR 96[rsp]
	mov	rcx, QWORD PTR 136[rsp]
	jmp	.L1430
.L1482:
	movzx	ecx, WORD PTR -2[rdx+rax]
	mov	WORD PTR -2[r9+rax], cx
	mov	r9, QWORD PTR 96[rsp]
	mov	rcx, QWORD PTR 136[rsp]
	jmp	.L1430
.L1424:
.LEHB23:
	call	_ZSt16__throw_bad_castv
.LEHE23:
.L1458:
	mov	rbx, rax
	jmp	.L1451
.L1491:
	xor	edx, edx
	mov	QWORD PTR 32[rsp], rax
	mov	r9, rbx
	xor	r8d, r8d
	mov	QWORD PTR 40[rsp], rdx
	mov	rdx, rbx
	mov	QWORD PTR 64[rsp], r11
	mov	QWORD PTR 56[rsp], r10
	mov	QWORD PTR 48[rsp], rax
.LEHB24:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
.LEHE24:
	mov	r11, QWORD PTR 64[rsp]
	mov	r10, QWORD PTR 56[rsp]
	mov	rax, QWORD PTR 48[rsp]
	mov	rdx, QWORD PTR 96[rsp]
	jmp	.L1445
.L1457:
	mov	rbx, rax
.L1450:
	mov	rcx, rdi
	lea	rsi, 96[rsp]
	call	_ZNSt6localeD1Ev
.L1451:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB25:
	call	_Unwind_Resume
	nop
.LEHE25:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5575:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5575-.LLSDACSB5575
.LLSDACSB5575:
	.uleb128 .LEHB20-.LFB5575
	.uleb128 .LEHE20-.LEHB20
	.uleb128 .L1458-.LFB5575
	.uleb128 0
	.uleb128 .LEHB21-.LFB5575
	.uleb128 .LEHE21-.LEHB21
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB22-.LFB5575
	.uleb128 .LEHE22-.LEHB22
	.uleb128 .L1458-.LFB5575
	.uleb128 0
	.uleb128 .LEHB23-.LFB5575
	.uleb128 .LEHE23-.LEHB23
	.uleb128 .L1457-.LFB5575
	.uleb128 0
	.uleb128 .LEHB24-.LFB5575
	.uleb128 .LEHE24-.LEHB24
	.uleb128 .L1458-.LFB5575
	.uleb128 0
	.uleb128 .LEHB25-.LFB5575
	.uleb128 .LEHE25-.LEHB25
	.uleb128 0
	.uleb128 0
.LLSDACSE5575:
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5593:
	push	r14
	.seh_pushreg	r14
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 328
	.seh_stackalloc	328
	.seh_endprologue
	mov	r10, rcx
	movzx	ecx, BYTE PTR 1[rcx]
	mov	eax, edx
	mov	ebx, ecx
	and	ebx, 120
	cmp	bl, 56
	je	.L1579
	shr	cl, 3
	and	ecx, 15
	test	edx, edx
	js	.L1580
	cmp	cl, 4
	je	.L1508
	ja	.L1509
	cmp	cl, 1
	jbe	.L1510
	lea	rdi, .LC26[rip]
	cmp	bl, 16
	lea	rcx, .LC27[rip]
	cmove	rcx, rdi
	mov	r14, rcx
	test	edx, edx
	jne	.L1506
	mov	eax, 48
	lea	rsi, 68[rsp]
	lea	rdi, 67[rsp]
.L1515:
	mov	BYTE PTR 67[rsp], al
	test	BYTE PTR [r10], 16
	je	.L1577
.L1562:
	mov	rax, -2
	mov	ecx, 2
.L1519:
	add	rax, rdi
	mov	r9d, ecx
	test	ecx, ecx
	je	.L1520
	xor	ecx, ecx
.L1544:
	mov	ebx, ecx
	add	ecx, 1
	movzx	r11d, BYTE PTR [r14+rbx]
	mov	BYTE PTR [rax+rbx], r11b
	cmp	ecx, r9d
	jb	.L1544
	.p2align 4
	.p2align 3
.L1520:
	lea	rbx, -1[rax]
	test	edx, edx
	js	.L1576
.L1586:
	movzx	ecx, BYTE PTR [r10]
.L1546:
	mov	edx, ecx
	shr	dl, 2
	and	edx, 3
	cmp	edx, 1
	je	.L1581
	cmp	edx, 3
	je	.L1582
.L1547:
	sub	rdi, rax
	sub	rsi, rax
	mov	r9, r8
	mov	rcx, r10
	lea	rdx, 48[rsp]
	mov	r8, rdi
	mov	QWORD PTR 48[rsp], rsi
	mov	QWORD PTR 56[rsp], rax
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	add	rsp, 328
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L1580:
	mov	eax, edx
	neg	eax
	cmp	cl, 4
	je	.L1503
	ja	.L1504
	cmp	cl, 1
	jbe	.L1505
	lea	rdi, .LC27[rip]
	cmp	bl, 16
	lea	rcx, .LC26[rip]
	cmovne	rcx, rdi
	mov	r14, rcx
.L1506:
	bsr	ebx, eax
	mov	r9d, 32
	xor	ebx, 31
	sub	r9d, ebx
	movsxd	r9, r9d
	cmp	eax, 1
	je	.L1583
	mov	esi, 31
	lea	rdi, 67[rsp]
	mov	r11d, 30
	sub	esi, ebx
	sub	r11d, ebx
	lea	rcx, [rdi+rsi]
	lea	rsi, 66[rsp+rsi]
	sub	rsi, r11
	.p2align 5
	.p2align 4
	.p2align 3
.L1517:
	mov	ebx, eax
	sub	rcx, 1
	shr	eax
	and	ebx, 1
	add	ebx, 48
	mov	BYTE PTR 1[rcx], bl
	cmp	rcx, rsi
	jne	.L1517
.L1518:
	lea	rsi, [rdi+r9]
	mov	eax, 49
	jmp	.L1515
	.p2align 4,,10
	.p2align 3
.L1579:
	lea	eax, 128[rdx]
	cmp	eax, 255
	ja	.L1500
	mov	DWORD PTR 32[rsp], 1
	lea	rax, 112[rsp]
	lea	rcx, 48[rsp]
	mov	r9, r10
	mov	BYTE PTR 112[rsp], dl
	mov	edx, 1
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	add	rsp, 328
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L1509:
	cmp	bl, 40
	je	.L1584
	test	edx, edx
	jne	.L1560
	mov	BYTE PTR 67[rsp], 48
	cmp	bl, 48
	je	.L1561
	lea	r14, .LC28[rip]
	lea	rsi, 68[rsp]
	lea	rdi, 67[rsp]
	jmp	.L1538
	.p2align 4,,10
	.p2align 3
.L1504:
	lea	rdi, .LC29[rip]
	cmp	bl, 40
	lea	rcx, .LC28[rip]
	cmove	rcx, rdi
	mov	r14, rcx
.L1507:
	movabs	rsi, 3978425819141910832
	bsr	ecx, eax
	movabs	rdi, 7378413942531504440
	add	ecx, 4
	mov	QWORD PTR 112[rsp], rsi
	shr	ecx, 2
	mov	QWORD PTR 120[rsp], rdi
	mov	r9d, ecx
	cmp	eax, 255
	jbe	.L1539
	sub	ecx, 1
	.p2align 6
	.p2align 4
	.p2align 3
.L1540:
	mov	esi, eax
	mov	r11d, ecx
	and	esi, 15
	movzx	esi, BYTE PTR 112[rsp+rsi]
	mov	BYTE PTR 67[rsp+r11], sil
	mov	r11d, eax
	lea	esi, -1[rcx]
	shr	eax, 8
	shr	r11d, 4
	sub	ecx, 2
	and	r11d, 15
	movzx	r11d, BYTE PTR 112[rsp+r11]
	mov	BYTE PTR 67[rsp+rsi], r11b
	cmp	eax, 255
	ja	.L1540
.L1539:
	cmp	eax, 15
	ja	.L1585
	movzx	eax, BYTE PTR 112[rsp+rax]
.L1542:
	lea	rdi, 67[rsp]
	mov	BYTE PTR 67[rsp], al
	lea	rsi, [rdi+r9]
	cmp	bl, 48
	je	.L1537
.L1538:
	test	BYTE PTR [r10], 16
	jne	.L1562
	.p2align 4
	.p2align 3
.L1577:
	mov	rax, rdi
	lea	rbx, -1[rax]
	test	edx, edx
	jns	.L1586
.L1576:
	mov	BYTE PTR -1[rax], 45
.L1549:
	mov	rax, rbx
	jmp	.L1547
	.p2align 4,,10
	.p2align 3
.L1581:
	mov	BYTE PTR -1[rax], 43
	jmp	.L1549
	.p2align 4,,10
	.p2align 3
.L1510:
	test	edx, edx
	jne	.L1505
.L1578:
	mov	BYTE PTR 67[rsp], 48
	movzx	ecx, BYTE PTR [r10]
.L1521:
	lea	rdi, 67[rsp]
	lea	rsi, 68[rsp]
	mov	rax, rdi
	lea	rbx, 66[rsp]
	jmp	.L1546
	.p2align 4,,10
	.p2align 3
.L1508:
	test	edx, edx
	je	.L1578
	.p2align 4
	.p2align 3
.L1503:
	bsr	ecx, eax
	lea	r11d, 3[rcx]
	mov	ecx, 2863311531
	imul	r11, rcx
	shr	r11, 33
	mov	r9d, r11d
	cmp	eax, 63
	jbe	.L1532
	sub	r11d, 1
	.p2align 6
	.p2align 4
	.p2align 3
.L1533:
	mov	ecx, eax
	mov	ebx, r11d
	and	ecx, 7
	add	ecx, 48
	mov	BYTE PTR 67[rsp+rbx], cl
	mov	ecx, eax
	lea	ebx, -1[r11]
	shr	eax, 6
	shr	ecx, 3
	sub	r11d, 2
	and	ecx, 7
	add	ecx, 48
	mov	BYTE PTR 67[rsp+rbx], cl
	cmp	eax, 63
	ja	.L1533
.L1532:
	lea	ecx, 48[rax]
	cmp	eax, 7
	ja	.L1587
.L1535:
	lea	rdi, 67[rsp]
	mov	BYTE PTR 67[rsp], cl
	lea	r14, .LC30[rip]
	mov	ecx, 1
	lea	rsi, [rdi+r9]
.L1536:
	mov	rax, rdi
	test	BYTE PTR [r10], 16
	je	.L1520
	mov	rax, rcx
	neg	rax
	jmp	.L1519
	.p2align 4,,10
	.p2align 3
.L1582:
	mov	BYTE PTR -1[rax], 32
	jmp	.L1549
	.p2align 4,,10
	.p2align 3
.L1505:
	cmp	eax, 9
	jbe	.L1555
	mov	ecx, eax
	mov	r11d, 1
	mov	ebx, 3518437209
	jmp	.L1527
	.p2align 4,,10
	.p2align 3
.L1523:
	cmp	ecx, 999
	jbe	.L1588
	cmp	ecx, 9999
	jbe	.L1589
	mov	r9d, ecx
	add	r11d, 4
	imul	r9, rbx
	shr	r9, 45
	cmp	ecx, 99999
	jbe	.L1524
	mov	ecx, r9d
.L1527:
	cmp	ecx, 99
	ja	.L1523
	add	r11d, 1
.L1524:
	mov	ebx, r11d
	cmp	r11d, 32
	ja	.L1557
	movabs	rsi, 3688503277381496880
	movabs	rdi, 3976738051646829616
	mov	QWORD PTR 112[rsp], rsi
	movabs	rsi, 3544667369688283184
	mov	QWORD PTR 120[rsp], rdi
	movabs	rdi, 3832902143785906737
	mov	QWORD PTR 128[rsp], rsi
	movabs	rsi, 4121136918051239473
	mov	QWORD PTR 136[rsp], rdi
	movabs	rdi, 3689066235924983858
	mov	QWORD PTR 144[rsp], rsi
	movabs	rsi, 3977301010190316594
	mov	QWORD PTR 152[rsp], rdi
	movabs	rdi, 3545230328231770162
	mov	QWORD PTR 160[rsp], rsi
	movabs	rsi, 3833465102329393715
	mov	QWORD PTR 168[rsp], rdi
	movabs	rdi, 4121699876594726451
	mov	QWORD PTR 176[rsp], rsi
	movabs	rsi, 3689629194468470836
	mov	QWORD PTR 184[rsp], rdi
	movabs	rdi, 3977863968733803572
	mov	QWORD PTR 192[rsp], rsi
	movabs	rsi, 3545793286775257140
	mov	QWORD PTR 200[rsp], rdi
	movabs	rdi, 3834028060872880693
	mov	QWORD PTR 208[rsp], rsi
	movabs	rsi, 4122262835138213429
	mov	QWORD PTR 216[rsp], rdi
	movabs	rdi, 3690192153011957814
	mov	QWORD PTR 224[rsp], rsi
	movabs	rsi, 3978426927277290550
	mov	QWORD PTR 232[rsp], rdi
	movabs	rdi, 3546356245318744118
	mov	QWORD PTR 240[rsp], rsi
	movabs	rsi, 3834591019416367671
	mov	QWORD PTR 248[rsp], rdi
	movabs	rdi, 4122825793681700407
	mov	QWORD PTR 256[rsp], rsi
	movabs	rsi, 3690755111555444792
	mov	QWORD PTR 264[rsp], rdi
	movabs	rdi, 3978989885820777528
	mov	QWORD PTR 272[rsp], rsi
	movabs	rsi, 3546919203862231096
	mov	QWORD PTR 280[rsp], rdi
	movabs	rdi, 3835153977959854649
	mov	QWORD PTR 296[rsp], rdi
	movabs	rdi, 16106987313379638
	mov	QWORD PTR 288[rsp], rsi
	movabs	rsi, 4122263930388298034
	mov	QWORD PTR 297[rsp], rsi
	mov	QWORD PTR 305[rsp], rdi
	cmp	eax, 99
	jbe	.L1529
	lea	ecx, -1[r11]
	.p2align 4
	.p2align 3
.L1530:
	mov	r9d, eax
	mov	r11d, eax
	imul	r9, r9, 1374389535
	shr	r9, 37
	imul	esi, r9d, 100
	sub	r11d, esi
	mov	esi, eax
	mov	eax, r9d
	mov	r9d, ecx
	add	r11d, r11d
	lea	edi, 1[r11]
	movzx	r11d, BYTE PTR 112[rsp+r11]
	movzx	edi, BYTE PTR 112[rsp+rdi]
	mov	BYTE PTR 67[rsp+r9], dil
	lea	r9d, -1[rcx]
	sub	ecx, 2
	mov	BYTE PTR 67[rsp+r9], r11b
	cmp	esi, 9999
	ja	.L1530
	cmp	esi, 999
	ja	.L1529
.L1522:
	add	eax, 48
.L1531:
	lea	rdi, 67[rsp]
	mov	BYTE PTR 67[rsp], al
	lea	rsi, [rdi+rbx]
	jmp	.L1577
	.p2align 4,,10
	.p2align 3
.L1587:
	mov	ecx, eax
	shr	eax, 3
	and	ecx, 7
	add	ecx, 48
	mov	BYTE PTR 68[rsp], cl
	lea	ecx, 48[rax]
	jmp	.L1535
	.p2align 4,,10
	.p2align 3
.L1585:
	mov	ecx, eax
	shr	eax, 4
	and	ecx, 15
	movzx	ecx, BYTE PTR 112[rsp+rcx]
	mov	BYTE PTR 68[rsp], cl
	movzx	eax, BYTE PTR 112[rsp+rax]
	jmp	.L1542
	.p2align 4,,10
	.p2align 3
.L1529:
	add	eax, eax
	lea	ecx, 1[rax]
	movzx	eax, BYTE PTR 112[rsp+rax]
	movzx	ecx, BYTE PTR 112[rsp+rcx]
	mov	BYTE PTR 68[rsp], cl
	jmp	.L1531
	.p2align 4,,10
	.p2align 3
.L1561:
	lea	rsi, 68[rsp]
	lea	r14, .LC28[rip]
	lea	rdi, 67[rsp]
.L1537:
	mov	rbx, rdi
	.p2align 4
	.p2align 3
.L1543:
	movsx	ecx, BYTE PTR [rbx]
	mov	QWORD PTR 384[rsp], r8
	add	rbx, 1
	mov	DWORD PTR 376[rsp], edx
	mov	QWORD PTR 368[rsp], r10
	call	toupper
	mov	r10, QWORD PTR 368[rsp]
	mov	edx, DWORD PTR 376[rsp]
	mov	BYTE PTR -1[rbx], al
	cmp	rbx, rsi
	mov	r8, QWORD PTR 384[rsp]
	jne	.L1543
	mov	ecx, 2
	jmp	.L1536
	.p2align 4,,10
	.p2align 3
.L1584:
	test	edx, edx
	jne	.L1558
	movzx	ecx, BYTE PTR [r10]
	mov	BYTE PTR 67[rsp], 48
	test	cl, 16
	je	.L1521
	lea	rsi, 68[rsp]
	mov	ecx, 2
	lea	rdi, 67[rsp]
	mov	rax, -2
	lea	r14, .LC29[rip]
	jmp	.L1519
	.p2align 4,,10
	.p2align 3
.L1588:
	add	r11d, 2
	jmp	.L1524
	.p2align 4,,10
	.p2align 3
.L1589:
	add	r11d, 3
	jmp	.L1524
.L1560:
	lea	r14, .LC28[rip]
	jmp	.L1507
.L1583:
	lea	rdi, 67[rsp]
	jmp	.L1518
.L1557:
	lea	rsi, 99[rsp]
	lea	rdi, 67[rsp]
	jmp	.L1577
.L1558:
	lea	r14, .LC29[rip]
	jmp	.L1507
.L1555:
	mov	ebx, 1
	jmp	.L1522
.L1500:
	lea	rcx, .LC31[rip]
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
.LFB5595:
	push	r12
	.seh_pushreg	r12
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 344
	.seh_stackalloc	344
	.seh_endprologue
	mov	eax, edx
	movzx	edx, BYTE PTR 1[rcx]
	mov	r10, rcx
	mov	esi, edx
	and	esi, 120
	cmp	sil, 56
	je	.L1660
	shr	dl, 3
	and	edx, 15
	cmp	dl, 4
	je	.L1594
	ja	.L1595
	cmp	dl, 1
	jbe	.L1596
	lea	rbx, .LC26[rip]
	cmp	sil, 16
	lea	rdx, .LC27[rip]
	cmove	rdx, rbx
	mov	rdi, rdx
	test	eax, eax
	jne	.L1661
	mov	eax, 48
	lea	rdx, 84[rsp]
	lea	rbx, 83[rsp]
.L1601:
	mov	BYTE PTR 83[rsp], al
	movzx	eax, BYTE PTR [r10]
	test	al, 16
	je	.L1659
.L1646:
	mov	rcx, -2
	mov	r9d, 2
.L1605:
	add	rcx, rbx
	mov	r11d, r9d
	test	r9d, r9d
	je	.L1606
	xor	r9d, r9d
.L1633:
	mov	esi, r9d
	add	r9d, 1
	movzx	r12d, BYTE PTR [rdi+rsi]
	mov	BYTE PTR [rcx+rsi], r12b
	cmp	r9d, r11d
	jb	.L1633
	jmp	.L1606
	.p2align 4,,10
	.p2align 3
.L1660:
	cmp	eax, 127
	ja	.L1592
	mov	DWORD PTR 32[rsp], 1
	lea	rcx, 64[rsp]
	mov	r9, r10
	mov	edx, 1
	mov	BYTE PTR 128[rsp], al
	lea	rax, 128[rsp]
	mov	QWORD PTR 64[rsp], 1
	mov	QWORD PTR 72[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	add	rsp, 344
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L1596:
	test	eax, eax
	jne	.L1607
	mov	BYTE PTR 83[rsp], 48
	lea	rdx, 84[rsp]
	lea	rbx, 83[rsp]
.L1608:
	movzx	eax, BYTE PTR [r10]
	mov	rcx, rbx
.L1606:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L1662
	cmp	eax, 3
	je	.L1648
.L1636:
	sub	rdx, rcx
	sub	rbx, rcx
	mov	QWORD PTR 72[rsp], rcx
	mov	r9, r8
	mov	QWORD PTR 64[rsp], rdx
	mov	r8, rbx
	lea	rdx, 64[rsp]
	mov	rcx, r10
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	add	rsp, 344
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L1594:
	test	eax, eax
	je	.L1618
	bsr	edx, eax
	lea	ecx, 3[rdx]
	mov	edx, 2863311531
	imul	rcx, rdx
	shr	rcx, 33
	mov	esi, ecx
	sub	ecx, 1
	cmp	eax, 63
	jbe	.L1620
	.p2align 6
	.p2align 4
	.p2align 3
.L1621:
	mov	r9d, eax
	mov	edx, eax
	mov	r11d, ecx
	shr	eax, 6
	and	r9d, 7
	shr	edx, 3
	add	r9d, 48
	and	edx, 7
	mov	BYTE PTR 83[rsp+r11], r9b
	add	edx, 48
	lea	r9d, -1[rcx]
	sub	ecx, 2
	mov	BYTE PTR 83[rsp+r9], dl
	cmp	eax, 63
	ja	.L1621
.L1620:
	lea	ecx, 48[rax]
	cmp	eax, 7
	ja	.L1663
.L1623:
	mov	BYTE PTR 83[rsp], cl
	lea	rbx, 83[rsp]
	lea	rdi, .LC30[rip]
	mov	r9d, 1
	lea	rdx, [rbx+rsi]
.L1624:
	movzx	eax, BYTE PTR [r10]
	mov	rcx, rbx
	test	al, 16
	je	.L1606
	mov	rcx, r9
	neg	rcx
	jmp	.L1605
	.p2align 4,,10
	.p2align 3
.L1662:
	mov	eax, 43
.L1637:
	mov	BYTE PTR -1[rcx], al
	sub	rcx, 1
	jmp	.L1636
	.p2align 4,,10
	.p2align 3
.L1595:
	cmp	sil, 40
	je	.L1664
	test	eax, eax
	jne	.L1644
	mov	BYTE PTR 83[rsp], 48
	cmp	sil, 48
	je	.L1645
	lea	rdi, .LC28[rip]
	lea	rdx, 84[rsp]
	lea	rbx, 83[rsp]
	jmp	.L1626
	.p2align 4,,10
	.p2align 3
.L1648:
	mov	eax, 32
	jmp	.L1637
	.p2align 4,,10
	.p2align 3
.L1644:
	lea	rdi, .LC28[rip]
.L1625:
	movabs	r11, 3978425819141910832
	bsr	edx, eax
	movabs	r12, 7378413942531504440
	lea	ecx, 4[rdx]
	mov	QWORD PTR 128[rsp], r11
	shr	ecx, 2
	mov	QWORD PTR 136[rsp], r12
	mov	edx, ecx
	cmp	eax, 255
	jbe	.L1628
	sub	ecx, 1
	.p2align 6
	.p2align 4
	.p2align 3
.L1629:
	mov	ebx, eax
	mov	r9d, ecx
	and	ebx, 15
	movzx	ebx, BYTE PTR 128[rsp+rbx]
	mov	BYTE PTR 83[rsp+r9], bl
	mov	r9d, eax
	lea	ebx, -1[rcx]
	shr	eax, 8
	shr	r9d, 4
	sub	ecx, 2
	and	r9d, 15
	movzx	r9d, BYTE PTR 128[rsp+r9]
	mov	BYTE PTR 83[rsp+rbx], r9b
	cmp	eax, 255
	ja	.L1629
.L1628:
	cmp	eax, 15
	ja	.L1665
	movzx	eax, BYTE PTR 128[rsp+rax]
.L1631:
	lea	rbx, 83[rsp]
	mov	BYTE PTR 83[rsp], al
	add	rdx, rbx
	cmp	sil, 48
	je	.L1627
.L1626:
	movzx	eax, BYTE PTR [r10]
	test	al, 16
	jne	.L1646
.L1659:
	mov	rcx, rbx
	jmp	.L1606
	.p2align 4,,10
	.p2align 3
.L1618:
	lea	rbx, 83[rsp]
	mov	BYTE PTR 83[rsp], 48
	movzx	eax, BYTE PTR [r10]
	lea	rdx, 84[rsp]
	mov	rcx, rbx
	jmp	.L1606
	.p2align 4,,10
	.p2align 3
.L1607:
	cmp	eax, 9
	jbe	.L1640
	mov	edx, eax
	mov	r9d, 1
	mov	r11d, 3518437209
	jmp	.L1614
	.p2align 4,,10
	.p2align 3
.L1610:
	cmp	edx, 999
	jbe	.L1666
	cmp	edx, 9999
	jbe	.L1667
	mov	ecx, edx
	add	r9d, 4
	imul	rcx, r11
	shr	rcx, 45
	cmp	edx, 99999
	jbe	.L1611
	mov	edx, ecx
.L1614:
	cmp	edx, 99
	ja	.L1610
	add	r9d, 1
.L1611:
	mov	r11d, r9d
	cmp	r9d, 32
	ja	.L1642
	movabs	rbx, 3688503277381496880
	movabs	rsi, 3976738051646829616
	mov	QWORD PTR 128[rsp], rbx
	movabs	rbx, 3544667369688283184
	mov	QWORD PTR 136[rsp], rsi
	movabs	rsi, 3832902143785906737
	mov	QWORD PTR 144[rsp], rbx
	movabs	rbx, 4121136918051239473
	mov	QWORD PTR 152[rsp], rsi
	movabs	rsi, 3689066235924983858
	mov	QWORD PTR 160[rsp], rbx
	movabs	rbx, 3977301010190316594
	mov	QWORD PTR 168[rsp], rsi
	movabs	rsi, 3545230328231770162
	mov	QWORD PTR 176[rsp], rbx
	movabs	rbx, 3833465102329393715
	mov	QWORD PTR 184[rsp], rsi
	movabs	rsi, 4121699876594726451
	mov	QWORD PTR 192[rsp], rbx
	movabs	rbx, 3689629194468470836
	mov	QWORD PTR 200[rsp], rsi
	movabs	rsi, 3977863968733803572
	mov	QWORD PTR 208[rsp], rbx
	movabs	rbx, 3545793286775257140
	mov	QWORD PTR 216[rsp], rsi
	movabs	rsi, 3834028060872880693
	mov	QWORD PTR 224[rsp], rbx
	movabs	rbx, 4122262835138213429
	mov	QWORD PTR 232[rsp], rsi
	movabs	rsi, 3690192153011957814
	mov	QWORD PTR 240[rsp], rbx
	movabs	rbx, 3978426927277290550
	mov	QWORD PTR 248[rsp], rsi
	movabs	rsi, 3546356245318744118
	mov	QWORD PTR 256[rsp], rbx
	movabs	rbx, 3834591019416367671
	mov	QWORD PTR 264[rsp], rsi
	movabs	rsi, 4122825793681700407
	mov	QWORD PTR 272[rsp], rbx
	movabs	rbx, 3690755111555444792
	mov	QWORD PTR 280[rsp], rsi
	movabs	rsi, 3978989885820777528
	mov	QWORD PTR 288[rsp], rbx
	movabs	rbx, 3546919203862231096
	mov	QWORD PTR 296[rsp], rsi
	movabs	rsi, 3835153977959854649
	mov	QWORD PTR 312[rsp], rsi
	movabs	rsi, 16106987313379638
	mov	QWORD PTR 304[rsp], rbx
	movabs	rbx, 4122263930388298034
	mov	QWORD PTR 313[rsp], rbx
	mov	QWORD PTR 321[rsp], rsi
	cmp	eax, 99
	jbe	.L1615
	lea	edx, -1[r9]
	.p2align 4
	.p2align 3
.L1616:
	mov	r9d, eax
	mov	ecx, eax
	imul	r9, r9, 1374389535
	shr	r9, 37
	imul	ebx, r9d, 100
	sub	ecx, ebx
	mov	ebx, eax
	mov	eax, r9d
	mov	r9d, edx
	add	ecx, ecx
	lea	esi, 1[rcx]
	movzx	ecx, BYTE PTR 128[rsp+rcx]
	movzx	esi, BYTE PTR 128[rsp+rsi]
	mov	BYTE PTR 83[rsp+r9], sil
	lea	r9d, -1[rdx]
	sub	edx, 2
	mov	BYTE PTR 83[rsp+r9], cl
	cmp	ebx, 9999
	ja	.L1616
	cmp	ebx, 999
	ja	.L1615
.L1609:
	add	eax, 48
.L1617:
	lea	rbx, 83[rsp]
	mov	BYTE PTR 83[rsp], al
	lea	rdx, [rbx+r11]
	jmp	.L1608
	.p2align 4,,10
	.p2align 3
.L1661:
	bsr	r9d, eax
	mov	edx, 32
	xor	r9d, 31
	sub	edx, r9d
	movsxd	rdx, edx
	cmp	eax, 1
	je	.L1668
	mov	esi, 31
	lea	rbx, 83[rsp]
	mov	r11d, 30
	sub	esi, r9d
	sub	r11d, r9d
	lea	rcx, [rbx+rsi]
	lea	rsi, 82[rsp+rsi]
	sub	rsi, r11
	.p2align 5
	.p2align 4
	.p2align 3
.L1603:
	mov	r9d, eax
	sub	rcx, 1
	shr	eax
	and	r9d, 1
	add	r9d, 48
	mov	BYTE PTR 1[rcx], r9b
	cmp	rsi, rcx
	jne	.L1603
.L1604:
	add	rdx, rbx
	mov	eax, 49
	jmp	.L1601
	.p2align 4,,10
	.p2align 3
.L1664:
	test	eax, eax
	jne	.L1643
	mov	BYTE PTR 83[rsp], 48
	lea	rdx, 84[rsp]
	lea	rbx, 83[rsp]
	lea	rdi, .LC29[rip]
	jmp	.L1626
	.p2align 4,,10
	.p2align 3
.L1665:
	mov	ecx, eax
	shr	eax, 4
	and	ecx, 15
	movzx	ecx, BYTE PTR 128[rsp+rcx]
	mov	BYTE PTR 84[rsp], cl
	movzx	eax, BYTE PTR 128[rsp+rax]
	jmp	.L1631
	.p2align 4,,10
	.p2align 3
.L1663:
	mov	edx, eax
	shr	eax, 3
	and	edx, 7
	lea	ecx, 48[rax]
	add	edx, 48
	mov	BYTE PTR 84[rsp], dl
	jmp	.L1623
	.p2align 4,,10
	.p2align 3
.L1615:
	add	eax, eax
	lea	edx, 1[rax]
	movzx	eax, BYTE PTR 128[rsp+rax]
	movzx	edx, BYTE PTR 128[rsp+rdx]
	mov	BYTE PTR 84[rsp], dl
	jmp	.L1617
	.p2align 4,,10
	.p2align 3
.L1643:
	lea	rdi, .LC29[rip]
	jmp	.L1625
	.p2align 4,,10
	.p2align 3
.L1645:
	lea	rdx, 84[rsp]
	lea	rdi, .LC28[rip]
	lea	rbx, 83[rsp]
.L1627:
	mov	rsi, rbx
	.p2align 4
	.p2align 3
.L1632:
	movsx	ecx, BYTE PTR [rsi]
	mov	QWORD PTR 56[rsp], rdx
	add	rsi, 1
	mov	QWORD PTR 400[rsp], r8
	mov	QWORD PTR 384[rsp], r10
	call	toupper
	mov	rdx, QWORD PTR 56[rsp]
	mov	r10, QWORD PTR 384[rsp]
	mov	BYTE PTR -1[rsi], al
	mov	r8, QWORD PTR 400[rsp]
	cmp	rsi, rdx
	jne	.L1632
	mov	r9d, 2
	jmp	.L1624
	.p2align 4,,10
	.p2align 3
.L1666:
	add	r9d, 2
	jmp	.L1611
	.p2align 4,,10
	.p2align 3
.L1667:
	add	r9d, 3
	jmp	.L1611
.L1668:
	lea	rbx, 83[rsp]
	jmp	.L1604
.L1642:
	lea	rdx, 115[rsp]
	lea	rbx, 83[rsp]
	jmp	.L1608
.L1640:
	mov	r11d, 1
	jmp	.L1609
.L1592:
	lea	rcx, .LC31[rip]
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
.LFB5597:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 368
	.seh_stackalloc	368
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	edi, eax
	and	edi, 120
	mov	rbx, rcx
	mov	r11, rdx
	mov	r10, rdx
	cmp	dil, 56
	je	.L1750
	shr	al, 3
	and	eax, 15
	test	rdx, rdx
	js	.L1751
	cmp	al, 4
	je	.L1679
	ja	.L1680
	cmp	al, 1
	jbe	.L1681
	lea	r9, .LC26[rip]
	cmp	dil, 16
	lea	rax, .LC27[rip]
	cmovne	r9, rax
	test	rdx, rdx
	jne	.L1677
	lea	rdx, 84[rsp]
	lea	rsi, 83[rsp]
	mov	eax, 48
.L1686:
	mov	BYTE PTR 83[rsp], al
	test	BYTE PTR [rbx], 16
	je	.L1748
.L1733:
	mov	rax, -2
	mov	ecx, 2
.L1690:
	add	rax, rsi
	mov	edi, ecx
	test	ecx, ecx
	je	.L1691
	xor	ecx, ecx
.L1715:
	mov	r10d, ecx
	add	ecx, 1
	movzx	r15d, BYTE PTR [r9+r10]
	mov	BYTE PTR [rax+r10], r15b
	cmp	ecx, edi
	jb	.L1715
	.p2align 4
	.p2align 3
.L1691:
	lea	r9, -1[rax]
	test	r11, r11
	js	.L1747
.L1757:
	movzx	ecx, BYTE PTR [rbx]
.L1717:
	shr	cl, 2
	and	ecx, 3
	cmp	ecx, 1
	je	.L1752
	cmp	ecx, 3
	je	.L1753
.L1718:
	sub	rdx, rax
	sub	rsi, rax
	mov	r9, r8
	mov	rcx, rbx
	mov	QWORD PTR 64[rsp], rdx
	mov	r8, rsi
	lea	rdx, 64[rsp]
	mov	QWORD PTR 72[rsp], rax
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	add	rsp, 368
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L1751:
	neg	r10
	cmp	al, 4
	je	.L1674
	ja	.L1675
	cmp	al, 1
	jbe	.L1676
	lea	r9, .LC27[rip]
	cmp	dil, 16
	lea	rax, .LC26[rip]
	cmove	r9, rax
.L1677:
	bsr	rcx, r10
	mov	edx, 64
	xor	rcx, 63
	sub	edx, ecx
	movsxd	rdx, edx
	cmp	r10, 1
	je	.L1754
	mov	edi, 63
	lea	rsi, 83[rsp]
	mov	r15d, 62
	sub	edi, ecx
	sub	r15d, ecx
	lea	rax, [rsi+rdi]
	lea	rdi, 82[rsp+rdi]
	sub	rdi, r15
	.p2align 5
	.p2align 4
	.p2align 3
.L1688:
	mov	ecx, r10d
	sub	rax, 1
	shr	r10
	and	ecx, 1
	add	ecx, 48
	mov	BYTE PTR 1[rax], cl
	cmp	rax, rdi
	jne	.L1688
.L1689:
	add	rdx, rsi
	mov	eax, 49
	jmp	.L1686
	.p2align 4,,10
	.p2align 3
.L1750:
	lea	rax, 128[rdx]
	cmp	rax, 255
	ja	.L1671
	mov	DWORD PTR 32[rsp], 1
	lea	rax, 160[rsp]
	lea	rcx, 64[rsp]
	mov	r9, rbx
	mov	BYTE PTR 160[rsp], dl
	mov	edx, 1
	mov	QWORD PTR 64[rsp], 1
	mov	QWORD PTR 72[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	add	rsp, 368
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L1680:
	cmp	dil, 40
	je	.L1755
	test	rdx, rdx
	jne	.L1731
	mov	BYTE PTR 83[rsp], 48
	cmp	dil, 48
	je	.L1732
	lea	r9, .LC28[rip]
	lea	rdx, 84[rsp]
	lea	rsi, 83[rsp]
	jmp	.L1709
	.p2align 4,,10
	.p2align 3
.L1675:
	lea	r9, .LC29[rip]
	cmp	dil, 40
	lea	rax, .LC28[rip]
	cmovne	r9, rax
.L1678:
	movabs	r14, 3978425819141910832
	bsr	rax, r10
	movabs	r15, 7378413942531504440
	add	eax, 4
	mov	QWORD PTR 160[rsp], r14
	shr	eax, 2
	mov	QWORD PTR 168[rsp], r15
	mov	edx, eax
	cmp	r10, 255
	jbe	.L1710
	sub	eax, 1
	.p2align 6
	.p2align 4
	.p2align 3
.L1711:
	mov	rsi, r10
	mov	ecx, eax
	and	esi, 15
	movzx	esi, BYTE PTR 160[rsp+rsi]
	mov	BYTE PTR 83[rsp+rcx], sil
	mov	rcx, r10
	lea	esi, -1[rax]
	shr	r10, 8
	shr	rcx, 4
	sub	eax, 2
	and	ecx, 15
	movzx	ecx, BYTE PTR 160[rsp+rcx]
	mov	BYTE PTR 83[rsp+rsi], cl
	cmp	r10, 255
	ja	.L1711
.L1710:
	cmp	r10, 15
	ja	.L1756
	movzx	eax, BYTE PTR 160[rsp+r10]
.L1713:
	lea	rsi, 83[rsp]
	mov	BYTE PTR 83[rsp], al
	add	rdx, rsi
	cmp	dil, 48
	je	.L1708
.L1709:
	test	BYTE PTR [rbx], 16
	jne	.L1733
	.p2align 4
	.p2align 3
.L1748:
	mov	rax, rsi
	lea	r9, -1[rax]
	test	r11, r11
	jns	.L1757
.L1747:
	mov	BYTE PTR -1[rax], 45
.L1720:
	mov	rax, r9
	jmp	.L1718
	.p2align 4,,10
	.p2align 3
.L1752:
	mov	BYTE PTR -1[rax], 43
	jmp	.L1720
	.p2align 4,,10
	.p2align 3
.L1681:
	test	rdx, rdx
	jne	.L1676
.L1749:
	mov	BYTE PTR 83[rsp], 48
	movzx	ecx, BYTE PTR [rbx]
.L1692:
	lea	rsi, 83[rsp]
	lea	rdx, 84[rsp]
	mov	rax, rsi
	lea	r9, 82[rsp]
	jmp	.L1717
	.p2align 4,,10
	.p2align 3
.L1679:
	test	rdx, rdx
	je	.L1749
	.p2align 4
	.p2align 3
.L1674:
	bsr	rax, r10
	lea	ecx, 3[rax]
	mov	eax, 2863311531
	imul	rcx, rax
	shr	rcx, 33
	mov	edx, ecx
	cmp	r10, 63
	jbe	.L1703
	sub	ecx, 1
	.p2align 6
	.p2align 4
	.p2align 3
.L1704:
	mov	rax, r10
	mov	r9d, ecx
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 83[rsp+r9], al
	mov	rax, r10
	lea	r9d, -1[rcx]
	shr	r10, 6
	shr	rax, 3
	sub	ecx, 2
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 83[rsp+r9], al
	cmp	r10, 63
	ja	.L1704
.L1703:
	lea	eax, 48[r10]
	cmp	r10, 7
	ja	.L1758
.L1706:
	mov	BYTE PTR 83[rsp], al
	lea	rsi, 83[rsp]
	mov	ecx, 1
	lea	r9, .LC30[rip]
	add	rdx, rsi
.L1707:
	mov	rax, rsi
	test	BYTE PTR [rbx], 16
	je	.L1691
	mov	rax, rcx
	neg	rax
	jmp	.L1690
	.p2align 4,,10
	.p2align 3
.L1753:
	mov	BYTE PTR -1[rax], 32
	jmp	.L1720
	.p2align 4,,10
	.p2align 3
.L1676:
	cmp	r10, 9
	jbe	.L1726
	mov	rcx, r10
	mov	r9d, 1
	movabs	rsi, 3777893186295716171
	jmp	.L1698
	.p2align 4,,10
	.p2align 3
.L1694:
	cmp	rcx, 999
	jbe	.L1759
	cmp	rcx, 9999
	jbe	.L1760
	mov	rax, rcx
	add	r9d, 4
	mul	rsi
	cmp	rcx, 99999
	jbe	.L1695
	shr	rdx, 11
	mov	rcx, rdx
.L1698:
	cmp	rcx, 99
	ja	.L1694
	add	r9d, 1
.L1695:
	mov	edi, r9d
	cmp	r9d, 64
	ja	.L1728
	movabs	rax, 3688503277381496880
	movabs	rdx, 3976738051646829616
	mov	QWORD PTR 160[rsp], rax
	movabs	rax, 3544667369688283184
	mov	QWORD PTR 168[rsp], rdx
	movabs	rdx, 3832902143785906737
	mov	QWORD PTR 176[rsp], rax
	movabs	rax, 4121136918051239473
	mov	QWORD PTR 184[rsp], rdx
	movabs	rdx, 3689066235924983858
	mov	QWORD PTR 192[rsp], rax
	movabs	rax, 3977301010190316594
	mov	QWORD PTR 200[rsp], rdx
	movabs	rdx, 3545230328231770162
	mov	QWORD PTR 208[rsp], rax
	movabs	rax, 3833465102329393715
	mov	QWORD PTR 216[rsp], rdx
	movabs	rdx, 4121699876594726451
	mov	QWORD PTR 224[rsp], rax
	movabs	rax, 3689629194468470836
	mov	QWORD PTR 232[rsp], rdx
	movabs	rdx, 3977863968733803572
	mov	QWORD PTR 240[rsp], rax
	movabs	rax, 3545793286775257140
	mov	QWORD PTR 248[rsp], rdx
	movabs	rdx, 3834028060872880693
	mov	QWORD PTR 256[rsp], rax
	movabs	rax, 4122262835138213429
	mov	QWORD PTR 264[rsp], rdx
	movabs	rdx, 3690192153011957814
	mov	QWORD PTR 272[rsp], rax
	movabs	rax, 3978426927277290550
	mov	QWORD PTR 280[rsp], rdx
	movabs	rdx, 3546356245318744118
	mov	QWORD PTR 288[rsp], rax
	movabs	rax, 3834591019416367671
	mov	QWORD PTR 296[rsp], rdx
	movabs	rdx, 4122825793681700407
	mov	QWORD PTR 304[rsp], rax
	movabs	rax, 3690755111555444792
	mov	QWORD PTR 312[rsp], rdx
	movabs	rdx, 3978989885820777528
	mov	QWORD PTR 320[rsp], rax
	movabs	rax, 3546919203862231096
	mov	QWORD PTR 328[rsp], rdx
	movabs	rdx, 3835153977959854649
	mov	QWORD PTR 344[rsp], rdx
	movabs	rdx, 16106987313379638
	mov	QWORD PTR 336[rsp], rax
	movabs	rax, 4122263930388298034
	mov	QWORD PTR 345[rsp], rax
	mov	QWORD PTR 353[rsp], rdx
	cmp	r10, 99
	jbe	.L1700
	movabs	rsi, 2951479051793528259
	lea	ecx, -1[r9]
	.p2align 4
	.p2align 3
.L1701:
	mov	rdx, r10
	shr	rdx, 2
	mov	rax, rdx
	mul	rsi
	mov	rax, r10
	shr	rdx, 2
	imul	r9, rdx, 100
	sub	rax, r9
	mov	r9, r10
	mov	r10, rdx
	mov	edx, ecx
	movzx	r14d, BYTE PTR 161[rsp+rax*2]
	movzx	eax, BYTE PTR 160[rsp+rax*2]
	mov	BYTE PTR 83[rsp+rdx], r14b
	lea	edx, -1[rcx]
	sub	ecx, 2
	mov	BYTE PTR 83[rsp+rdx], al
	cmp	r9, 9999
	ja	.L1701
	cmp	r9, 999
	ja	.L1700
.L1693:
	add	r10d, 48
.L1702:
	lea	rsi, 83[rsp]
	mov	BYTE PTR 83[rsp], r10b
	lea	rdx, [rsi+rdi]
	jmp	.L1748
	.p2align 4,,10
	.p2align 3
.L1758:
	mov	rax, r10
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 84[rsp], al
	mov	rax, r10
	shr	rax, 3
	add	eax, 48
	jmp	.L1706
	.p2align 4,,10
	.p2align 3
.L1756:
	mov	rax, r10
	shr	r10, 4
	and	eax, 15
	movzx	eax, BYTE PTR 160[rsp+rax]
	mov	BYTE PTR 84[rsp], al
	movzx	eax, BYTE PTR 160[rsp+r10]
	jmp	.L1713
	.p2align 4,,10
	.p2align 3
.L1700:
	movzx	eax, BYTE PTR 161[rsp+r10*2]
	movzx	r10d, BYTE PTR 160[rsp+r10*2]
	mov	BYTE PTR 84[rsp], al
	jmp	.L1702
	.p2align 4,,10
	.p2align 3
.L1732:
	lea	rdx, 84[rsp]
	lea	r9, .LC28[rip]
	lea	rsi, 83[rsp]
.L1708:
	mov	rdi, rsi
	.p2align 4
	.p2align 3
.L1714:
	movsx	ecx, BYTE PTR [rdi]
	mov	QWORD PTR 56[rsp], rdx
	add	rdi, 1
	mov	QWORD PTR 432[rsp], r8
	mov	QWORD PTR 424[rsp], r11
	mov	QWORD PTR 48[rsp], r9
	call	toupper
	mov	rdx, QWORD PTR 56[rsp]
	mov	r9, QWORD PTR 48[rsp]
	mov	BYTE PTR -1[rdi], al
	mov	r11, QWORD PTR 424[rsp]
	cmp	rdx, rdi
	mov	r8, QWORD PTR 432[rsp]
	jne	.L1714
	mov	ecx, 2
	jmp	.L1707
	.p2align 4,,10
	.p2align 3
.L1755:
	test	rdx, rdx
	jne	.L1729
	movzx	ecx, BYTE PTR [rcx]
	mov	BYTE PTR 83[rsp], 48
	test	cl, 16
	je	.L1692
	lea	rdx, 84[rsp]
	mov	ecx, 2
	lea	rsi, 83[rsp]
	mov	rax, -2
	lea	r9, .LC29[rip]
	jmp	.L1690
	.p2align 4,,10
	.p2align 3
.L1759:
	add	r9d, 2
	jmp	.L1695
	.p2align 4,,10
	.p2align 3
.L1760:
	add	r9d, 3
	jmp	.L1695
.L1731:
	lea	r9, .LC28[rip]
	jmp	.L1678
.L1754:
	lea	rsi, 83[rsp]
	jmp	.L1689
.L1728:
	lea	rdx, 147[rsp]
	lea	rsi, 83[rsp]
	jmp	.L1748
.L1729:
	lea	r9, .LC29[rip]
	jmp	.L1678
.L1726:
	mov	edi, 1
	jmp	.L1693
.L1671:
	lea	rcx, .LC31[rip]
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
.LFB5599:
	push	r14
	.seh_pushreg	r14
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 376
	.seh_stackalloc	376
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	esi, eax
	and	esi, 120
	mov	r11, rcx
	mov	r10, rdx
	cmp	sil, 56
	je	.L1831
	shr	al, 3
	and	eax, 15
	cmp	al, 4
	je	.L1765
	ja	.L1766
	cmp	al, 1
	jbe	.L1767
	lea	rdi, .LC26[rip]
	cmp	sil, 16
	lea	rax, .LC27[rip]
	cmove	rax, rdi
	mov	r14, rax
	test	rdx, rdx
	jne	.L1832
	mov	eax, 48
	lea	rdx, 84[rsp]
	lea	rbx, 83[rsp]
.L1772:
	mov	BYTE PTR 83[rsp], al
	movzx	eax, BYTE PTR [r11]
	test	al, 16
	je	.L1830
.L1817:
	mov	rcx, -2
	mov	r10d, 2
.L1776:
	add	rcx, rbx
	mov	r9d, r10d
	test	r10d, r10d
	je	.L1777
	xor	r10d, r10d
.L1804:
	mov	esi, r10d
	add	r10d, 1
	movzx	edi, BYTE PTR [r14+rsi]
	mov	BYTE PTR [rcx+rsi], dil
	cmp	r10d, r9d
	jb	.L1804
	jmp	.L1777
	.p2align 4,,10
	.p2align 3
.L1831:
	cmp	rdx, 127
	ja	.L1763
	mov	DWORD PTR 32[rsp], 1
	lea	rax, 160[rsp]
	lea	rcx, 64[rsp]
	mov	r9, r11
	mov	BYTE PTR 160[rsp], dl
	mov	edx, 1
	mov	QWORD PTR 64[rsp], 1
	mov	QWORD PTR 72[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	add	rsp, 376
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L1767:
	test	rdx, rdx
	jne	.L1778
	mov	BYTE PTR 83[rsp], 48
	lea	rdx, 84[rsp]
	lea	rbx, 83[rsp]
.L1779:
	movzx	eax, BYTE PTR [r11]
	mov	rcx, rbx
.L1777:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L1833
	cmp	eax, 3
	je	.L1819
.L1807:
	sub	rdx, rcx
	sub	rbx, rcx
	mov	QWORD PTR 72[rsp], rcx
	mov	r9, r8
	mov	QWORD PTR 64[rsp], rdx
	mov	r8, rbx
	lea	rdx, 64[rsp]
	mov	rcx, r11
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	add	rsp, 376
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L1765:
	test	rdx, rdx
	je	.L1789
	bsr	rax, rdx
	lea	ecx, 3[rax]
	mov	eax, 2863311531
	imul	rcx, rax
	shr	rcx, 33
	mov	edx, ecx
	sub	ecx, 1
	cmp	r10, 63
	jbe	.L1791
	.p2align 6
	.p2align 4
	.p2align 3
.L1792:
	mov	rax, r10
	mov	r9d, ecx
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 83[rsp+r9], al
	mov	rax, r10
	lea	r9d, -1[rcx]
	shr	r10, 6
	shr	rax, 3
	sub	ecx, 2
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 83[rsp+r9], al
	cmp	r10, 63
	ja	.L1792
.L1791:
	lea	eax, 48[r10]
	cmp	r10, 7
	ja	.L1834
.L1794:
	mov	BYTE PTR 83[rsp], al
	lea	rbx, 83[rsp]
	lea	r14, .LC30[rip]
	mov	r10d, 1
	add	rdx, rbx
.L1795:
	movzx	eax, BYTE PTR [r11]
	mov	rcx, rbx
	test	al, 16
	je	.L1777
	mov	rcx, r10
	neg	rcx
	jmp	.L1776
	.p2align 4,,10
	.p2align 3
.L1833:
	mov	eax, 43
.L1808:
	mov	BYTE PTR -1[rcx], al
	sub	rcx, 1
	jmp	.L1807
	.p2align 4,,10
	.p2align 3
.L1766:
	cmp	sil, 40
	je	.L1835
	test	rdx, rdx
	jne	.L1815
	mov	BYTE PTR 83[rsp], 48
	cmp	sil, 48
	je	.L1816
	lea	r14, .LC28[rip]
	lea	rdx, 84[rsp]
	lea	rbx, 83[rsp]
	jmp	.L1797
	.p2align 4,,10
	.p2align 3
.L1819:
	mov	eax, 32
	jmp	.L1808
	.p2align 4,,10
	.p2align 3
.L1815:
	lea	r14, .LC28[rip]
.L1796:
	movabs	rcx, 3978425819141910832
	bsr	rax, r10
	movabs	rbx, 7378413942531504440
	add	eax, 4
	mov	QWORD PTR 160[rsp], rcx
	shr	eax, 2
	mov	QWORD PTR 168[rsp], rbx
	mov	edx, eax
	cmp	r10, 255
	jbe	.L1799
	sub	eax, 1
	.p2align 6
	.p2align 4
	.p2align 3
.L1800:
	mov	rbx, r10
	mov	ecx, eax
	and	ebx, 15
	movzx	ebx, BYTE PTR 160[rsp+rbx]
	mov	BYTE PTR 83[rsp+rcx], bl
	mov	rcx, r10
	lea	ebx, -1[rax]
	shr	r10, 8
	shr	rcx, 4
	sub	eax, 2
	and	ecx, 15
	movzx	ecx, BYTE PTR 160[rsp+rcx]
	mov	BYTE PTR 83[rsp+rbx], cl
	cmp	r10, 255
	ja	.L1800
.L1799:
	cmp	r10, 15
	ja	.L1836
	movzx	eax, BYTE PTR 160[rsp+r10]
.L1802:
	lea	rbx, 83[rsp]
	mov	BYTE PTR 83[rsp], al
	add	rdx, rbx
	cmp	sil, 48
	je	.L1798
.L1797:
	movzx	eax, BYTE PTR [r11]
	test	al, 16
	jne	.L1817
.L1830:
	mov	rcx, rbx
	jmp	.L1777
	.p2align 4,,10
	.p2align 3
.L1789:
	lea	rbx, 83[rsp]
	mov	BYTE PTR 83[rsp], 48
	movzx	eax, BYTE PTR [r11]
	lea	rdx, 84[rsp]
	mov	rcx, rbx
	jmp	.L1777
	.p2align 4,,10
	.p2align 3
.L1778:
	cmp	rdx, 9
	jbe	.L1811
	mov	rcx, rdx
	mov	r9d, 1
	movabs	rbx, 3777893186295716171
	jmp	.L1785
	.p2align 4,,10
	.p2align 3
.L1781:
	cmp	rcx, 999
	jbe	.L1837
	cmp	rcx, 9999
	jbe	.L1838
	mov	rax, rcx
	add	r9d, 4
	mul	rbx
	cmp	rcx, 99999
	jbe	.L1782
	shr	rdx, 11
	mov	rcx, rdx
.L1785:
	cmp	rcx, 99
	ja	.L1781
	add	r9d, 1
.L1782:
	mov	esi, r9d
	cmp	r9d, 64
	ja	.L1813
	movabs	rax, 3688503277381496880
	movabs	rdx, 3976738051646829616
	mov	QWORD PTR 160[rsp], rax
	movabs	rax, 3544667369688283184
	mov	QWORD PTR 168[rsp], rdx
	movabs	rdx, 3832902143785906737
	mov	QWORD PTR 176[rsp], rax
	movabs	rax, 4121136918051239473
	mov	QWORD PTR 184[rsp], rdx
	movabs	rdx, 3689066235924983858
	mov	QWORD PTR 192[rsp], rax
	movabs	rax, 3977301010190316594
	mov	QWORD PTR 200[rsp], rdx
	movabs	rdx, 3545230328231770162
	mov	QWORD PTR 208[rsp], rax
	movabs	rax, 3833465102329393715
	mov	QWORD PTR 216[rsp], rdx
	movabs	rdx, 4121699876594726451
	mov	QWORD PTR 224[rsp], rax
	movabs	rax, 3689629194468470836
	mov	QWORD PTR 232[rsp], rdx
	movabs	rdx, 3977863968733803572
	mov	QWORD PTR 240[rsp], rax
	movabs	rax, 3545793286775257140
	mov	QWORD PTR 248[rsp], rdx
	movabs	rdx, 3834028060872880693
	mov	QWORD PTR 256[rsp], rax
	movabs	rax, 4122262835138213429
	mov	QWORD PTR 264[rsp], rdx
	movabs	rdx, 3690192153011957814
	mov	QWORD PTR 272[rsp], rax
	movabs	rax, 3978426927277290550
	mov	QWORD PTR 280[rsp], rdx
	movabs	rdx, 3546356245318744118
	mov	QWORD PTR 288[rsp], rax
	movabs	rax, 3834591019416367671
	mov	QWORD PTR 296[rsp], rdx
	movabs	rdx, 4122825793681700407
	mov	QWORD PTR 304[rsp], rax
	movabs	rax, 3690755111555444792
	mov	QWORD PTR 312[rsp], rdx
	movabs	rdx, 3978989885820777528
	mov	QWORD PTR 320[rsp], rax
	movabs	rax, 3546919203862231096
	mov	QWORD PTR 328[rsp], rdx
	movabs	rdx, 3835153977959854649
	mov	QWORD PTR 344[rsp], rdx
	movabs	rdx, 16106987313379638
	mov	QWORD PTR 336[rsp], rax
	movabs	rax, 4122263930388298034
	mov	QWORD PTR 345[rsp], rax
	mov	QWORD PTR 353[rsp], rdx
	cmp	r10, 99
	jbe	.L1786
	movabs	rbx, 2951479051793528259
	lea	ecx, -1[r9]
	.p2align 4
	.p2align 3
.L1787:
	mov	rdx, r10
	shr	rdx, 2
	mov	rax, rdx
	mul	rbx
	mov	rax, r10
	shr	rdx, 2
	imul	r9, rdx, 100
	sub	rax, r9
	mov	r9, r10
	mov	r10, rdx
	mov	edx, ecx
	movzx	edi, BYTE PTR 161[rsp+rax*2]
	movzx	eax, BYTE PTR 160[rsp+rax*2]
	mov	BYTE PTR 83[rsp+rdx], dil
	lea	edx, -1[rcx]
	sub	ecx, 2
	mov	BYTE PTR 83[rsp+rdx], al
	cmp	r9, 9999
	ja	.L1787
	cmp	r9, 999
	ja	.L1786
.L1780:
	add	r10d, 48
.L1788:
	lea	rbx, 83[rsp]
	mov	BYTE PTR 83[rsp], r10b
	lea	rdx, [rbx+rsi]
	jmp	.L1779
	.p2align 4,,10
	.p2align 3
.L1832:
	bsr	rcx, rdx
	mov	edx, 64
	xor	rcx, 63
	sub	edx, ecx
	movsxd	rdx, edx
	cmp	r10, 1
	je	.L1839
	mov	esi, 63
	lea	rbx, 83[rsp]
	mov	r9d, 62
	sub	esi, ecx
	sub	r9d, ecx
	lea	rax, [rbx+rsi]
	lea	rsi, 82[rsp+rsi]
	sub	rsi, r9
	.p2align 5
	.p2align 4
	.p2align 3
.L1774:
	mov	ecx, r10d
	sub	rax, 1
	shr	r10
	and	ecx, 1
	add	ecx, 48
	mov	BYTE PTR 1[rax], cl
	cmp	rsi, rax
	jne	.L1774
.L1775:
	add	rdx, rbx
	mov	eax, 49
	jmp	.L1772
	.p2align 4,,10
	.p2align 3
.L1835:
	test	rdx, rdx
	jne	.L1814
	mov	BYTE PTR 83[rsp], 48
	lea	rdx, 84[rsp]
	lea	rbx, 83[rsp]
	lea	r14, .LC29[rip]
	jmp	.L1797
	.p2align 4,,10
	.p2align 3
.L1836:
	mov	rax, r10
	shr	r10, 4
	and	eax, 15
	movzx	eax, BYTE PTR 160[rsp+rax]
	mov	BYTE PTR 84[rsp], al
	movzx	eax, BYTE PTR 160[rsp+r10]
	jmp	.L1802
	.p2align 4,,10
	.p2align 3
.L1834:
	mov	rax, r10
	and	eax, 7
	add	eax, 48
	mov	BYTE PTR 84[rsp], al
	mov	rax, r10
	shr	rax, 3
	add	eax, 48
	jmp	.L1794
	.p2align 4,,10
	.p2align 3
.L1786:
	movzx	eax, BYTE PTR 161[rsp+r10*2]
	movzx	r10d, BYTE PTR 160[rsp+r10*2]
	mov	BYTE PTR 84[rsp], al
	jmp	.L1788
	.p2align 4,,10
	.p2align 3
.L1814:
	lea	r14, .LC29[rip]
	jmp	.L1796
	.p2align 4,,10
	.p2align 3
.L1816:
	lea	rdx, 84[rsp]
	lea	r14, .LC28[rip]
	lea	rbx, 83[rsp]
.L1798:
	mov	rsi, rbx
	.p2align 4
	.p2align 3
.L1803:
	movsx	ecx, BYTE PTR [rsi]
	mov	QWORD PTR 56[rsp], rdx
	add	rsi, 1
	mov	QWORD PTR 432[rsp], r8
	mov	QWORD PTR 416[rsp], r11
	call	toupper
	mov	rdx, QWORD PTR 56[rsp]
	mov	r11, QWORD PTR 416[rsp]
	mov	BYTE PTR -1[rsi], al
	mov	r8, QWORD PTR 432[rsp]
	cmp	rsi, rdx
	jne	.L1803
	mov	r10d, 2
	jmp	.L1795
	.p2align 4,,10
	.p2align 3
.L1837:
	add	r9d, 2
	jmp	.L1782
	.p2align 4,,10
	.p2align 3
.L1838:
	add	r9d, 3
	jmp	.L1782
.L1839:
	lea	rbx, 83[rsp]
	jmp	.L1775
.L1813:
	lea	rdx, 147[rsp]
	lea	rbx, 83[rsp]
	jmp	.L1779
.L1811:
	mov	esi, 1
	jmp	.L1780
.L1763:
	lea	rcx, .LC31[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5639:
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
	sub	rsp, 520
	.seh_stackalloc	520
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	r14, QWORD PTR [rdx]
	mov	r15, QWORD PTR 8[rdx]
	mov	r9d, eax
	and	r9d, 120
	mov	QWORD PTR 592[rsp], rcx
	mov	rbp, r8
	cmp	r9b, 56
	je	.L1931
	shr	al, 3
	mov	r10, r14
	mov	r11, r15
	and	eax, 15
	test	r15, r15
	js	.L1932
	cmp	al, 4
	je	.L1850
	ja	.L1851
	cmp	al, 1
	jbe	.L1852
	cmp	r9b, 16
	lea	rax, .LC27[rip]
	lea	r13, .LC26[rip]
	cmovne	r13, rax
	mov	rax, r14
	or	rax, r15
	jne	.L1848
	mov	eax, 48
	lea	rsi, 164[rsp]
	lea	rdi, 163[rsp]
.L1857:
	mov	BYTE PTR 163[rsp], al
	mov	rax, QWORD PTR 592[rsp]
	test	BYTE PTR [rax], 16
	je	.L1929
.L1910:
	mov	rdx, -2
	mov	eax, 2
.L1862:
	add	rdx, rdi
	mov	r9d, eax
	test	eax, eax
	je	.L1863
	xor	eax, eax
.L1891:
	mov	ecx, eax
	add	eax, 1
	movzx	r8d, BYTE PTR 0[r13+rcx]
	mov	BYTE PTR [rdx+rcx], r8b
	cmp	eax, r9d
	jb	.L1891
	.p2align 4
	.p2align 3
.L1863:
	lea	rcx, -1[rdx]
	test	r15, r15
	js	.L1927
.L1938:
	mov	rax, QWORD PTR 592[rsp]
	movzx	eax, BYTE PTR [rax]
.L1893:
	shr	al, 2
	and	eax, 3
	cmp	eax, 1
	je	.L1933
	cmp	eax, 3
	je	.L1934
.L1894:
	sub	rdi, rdx
	mov	rax, rsi
	mov	r9, rbp
	mov	rcx, QWORD PTR 592[rsp]
	sub	rax, rdx
	mov	QWORD PTR 152[rsp], rdx
	mov	r8, rdi
	lea	rdx, 144[rsp]
	mov	QWORD PTR 144[rsp], rax
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L1843
	.p2align 4,,10
	.p2align 3
.L1932:
	neg	r10
	adc	r11, 0
	neg	r11
	cmp	al, 4
	je	.L1845
	ja	.L1846
	cmp	al, 1
	jbe	.L1847
	lea	r13, .LC27[rip]
	cmp	r9b, 16
	lea	rax, .LC26[rip]
	cmove	r13, rax
.L1848:
	test	r11, r11
	jne	.L1935
	bsr	rax, r10
	xor	rax, 63
	lea	edx, 64[rax]
	cmp	eax, 63
	je	.L1901
.L1928:
	mov	ecx, 127
	mov	eax, 128
	lea	rdi, 163[rsp]
	sub	ecx, edx
	sub	eax, edx
	mov	r9d, ecx
	sub	ecx, 1
	cdqe
	lea	rdx, [rdi+r9]
	lea	r9, 162[rsp+r9]
	sub	r9, rcx
	.p2align 5
	.p2align 4
	.p2align 3
.L1861:
	mov	ecx, r10d
	sub	rdx, 1
	shrd	r10, r11, 1
	and	ecx, 1
	shr	r11
	add	ecx, 48
	mov	BYTE PTR 1[rdx], cl
	cmp	rdx, r9
	jne	.L1861
.L1860:
	lea	rsi, [rdi+rax]
	mov	eax, 49
	jmp	.L1857
	.p2align 4,,10
	.p2align 3
.L1931:
	mov	eax, 127
	cmp	rax, r14
	mov	eax, 0
	sbb	rax, r15
	jl	.L1842
	mov	DWORD PTR 32[rsp], 1
	mov	r9, QWORD PTR 592[rsp]
	lea	rax, 304[rsp]
	lea	rcx, 144[rsp]
	mov	edx, 1
	mov	BYTE PTR 304[rsp], r14b
	mov	QWORD PTR 144[rsp], 1
	mov	QWORD PTR 152[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1843:
	add	rsp, 520
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
.L1851:
	cmp	r9b, 40
	je	.L1936
	mov	rax, r14
	or	rax, r15
	jne	.L1908
	mov	BYTE PTR 163[rsp], 48
	cmp	r9b, 48
	je	.L1909
	lea	r13, .LC28[rip]
	lea	rsi, 164[rsp]
	lea	rdi, 163[rsp]
	jmp	.L1883
	.p2align 4,,10
	.p2align 3
.L1846:
	lea	r13, .LC29[rip]
	cmp	r9b, 40
	lea	rax, .LC28[rip]
	cmovne	r13, rax
.L1849:
	test	r11, r11
	jne	.L1937
	bsr	rax, r10
	mov	ecx, 255
	movabs	rbx, 3978425819141910832
	movabs	rsi, 7378413942531504440
	lea	edx, 4[rax]
	mov	QWORD PTR 304[rsp], rbx
	shr	edx, 2
	cmp	rcx, r10
	mov	QWORD PTR 312[rsp], rsi
	lea	rcx, 304[rsp]
	mov	r8d, edx
	jnb	.L1886
	sub	edx, 1
.L1885:
	lea	rcx, 304[rsp]
	mov	eax, 255
	xor	r12d, r12d
	.p2align 4
	.p2align 3
.L1887:
	mov	rsi, r10
	mov	ebx, edx
	and	esi, 15
	movzx	esi, BYTE PTR [rcx+rsi]
	mov	BYTE PTR 163[rsp+rbx], sil
	mov	rsi, r10
	lea	ebx, -1[rdx]
	shrd	r10, r11, 8
	shrd	rsi, r11, 4
	sub	edx, 2
	shr	r11, 8
	and	esi, 15
	cmp	rax, r10
	movzx	esi, BYTE PTR [rcx+rsi]
	mov	BYTE PTR 163[rsp+rbx], sil
	mov	rbx, r12
	sbb	rbx, r11
	jc	.L1887
.L1886:
	mov	edx, 15
	cmp	rdx, r10
	mov	edx, 0
	sbb	rdx, r11
	jnc	.L1888
	mov	rsi, r10
	and	esi, 15
	movzx	edx, BYTE PTR [rcx+rsi]
	mov	BYTE PTR 164[rsp], dl
	mov	rdx, r10
	shrd	rdx, r11, 4
	movzx	edx, BYTE PTR [rdx+rcx]
.L1889:
	lea	rdi, 163[rsp]
	mov	BYTE PTR 163[rsp], dl
	lea	rsi, [rdi+r8]
	cmp	r9b, 48
	je	.L1882
.L1883:
	mov	rax, QWORD PTR 592[rsp]
	test	BYTE PTR [rax], 16
	jne	.L1910
	.p2align 4
	.p2align 3
.L1929:
	mov	rdx, rdi
	lea	rcx, -1[rdx]
	test	r15, r15
	jns	.L1938
.L1927:
	mov	BYTE PTR -1[rdx], 45
.L1896:
	mov	rdx, rcx
	jmp	.L1894
	.p2align 4,,10
	.p2align 3
.L1933:
	mov	BYTE PTR -1[rdx], 43
	jmp	.L1896
	.p2align 4,,10
	.p2align 3
.L1852:
	mov	rax, r14
	or	rax, r15
	jne	.L1847
.L1930:
	mov	rax, QWORD PTR 592[rsp]
	mov	BYTE PTR 163[rsp], 48
	movzx	eax, BYTE PTR [rax]
.L1864:
	lea	rdi, 163[rsp]
	lea	rsi, 164[rsp]
	mov	rdx, rdi
	lea	rcx, 162[rsp]
	jmp	.L1893
	.p2align 4,,10
	.p2align 3
.L1850:
	mov	rax, r14
	or	rax, r15
	je	.L1930
	.p2align 4
	.p2align 3
.L1845:
	test	r11, r11
	jne	.L1939
	bsr	rax, r10
	mov	ecx, 63
	lea	edx, 3[rax]
	mov	eax, 2863311531
	imul	rdx, rax
	shr	rdx, 33
	mov	eax, edx
	cmp	rcx, r10
	jnb	.L1877
	sub	edx, 1
.L1876:
	mov	r9d, 63
	xor	r8d, r8d
	.p2align 4
	.p2align 3
.L1878:
	mov	rcx, r10
	mov	esi, edx
	lea	ebx, -1[rdx]
	sub	edx, 2
	and	ecx, 7
	add	ecx, 48
	mov	BYTE PTR 163[rsp+rsi], cl
	mov	rcx, r10
	shrd	r10, r11, 6
	shrd	rcx, r11, 3
	shr	r11, 6
	and	ecx, 7
	cmp	r9, r10
	lea	ecx, 48[rcx]
	mov	BYTE PTR 163[rsp+rbx], cl
	mov	rbx, r8
	sbb	rbx, r11
	jc	.L1878
.L1877:
	mov	edx, 7
	cmp	rdx, r10
	mov	edx, 0
	sbb	rdx, r11
	jnc	.L1879
	mov	r8, r10
	shrd	r10, r11, 3
	and	r8d, 7
	add	r10d, 48
	add	r8d, 48
	mov	BYTE PTR 164[rsp], r8b
.L1880:
	mov	BYTE PTR 163[rsp], r10b
	lea	rdi, 163[rsp]
	lea	r13, .LC30[rip]
	lea	rsi, [rdi+rax]
	mov	eax, 1
.L1881:
	mov	rbx, QWORD PTR 592[rsp]
	mov	rdx, rdi
	test	BYTE PTR [rbx], 16
	je	.L1863
	mov	rdx, rax
	neg	rdx
	jmp	.L1862
	.p2align 4,,10
	.p2align 3
.L1934:
	mov	BYTE PTR -1[rdx], 32
	jmp	.L1896
	.p2align 4,,10
	.p2align 3
.L1847:
	mov	eax, 9
	cmp	rax, r10
	mov	eax, 0
	sbb	rax, r11
	jnc	.L1903
	mov	QWORD PTR 104[rsp], r15
	mov	r13, r10
	mov	r15, rbp
	mov	edi, 1
	mov	QWORD PTR 80[rsp], r10
	xor	esi, esi
	mov	ebx, 999
	lea	rbp, 112[rsp]
	mov	QWORD PTR 88[rsp], r11
	mov	QWORD PTR 96[rsp], r14
	jmp	.L1870
	.p2align 4,,10
	.p2align 3
.L1866:
	cmp	rbx, r13
	mov	rax, rsi
	sbb	rax, r11
	jnc	.L1940
	mov	eax, 9999
	cmp	rax, r13
	mov	rax, rsi
	sbb	rax, r11
	jnc	.L1941
	mov	rdx, rbp
	mov	QWORD PTR 64[rsp], r11
	add	edi, 4
	lea	rcx, 128[rsp]
	mov	QWORD PTR 128[rsp], r13
	mov	QWORD PTR 136[rsp], r11
	mov	QWORD PTR 112[rsp], 10000
	mov	QWORD PTR 120[rsp], 0
	call	__udivti3
	mov	eax, 99999
	cmp	rax, r13
	mov	rax, rsi
	sbb	rax, QWORD PTR 64[rsp]
	movaps	XMMWORD PTR 48[rsp], xmm0
	jnc	.L1942
	mov	r13, QWORD PTR 48[rsp]
	mov	r11, QWORD PTR 56[rsp]
.L1870:
	mov	eax, 99
	cmp	rax, r13
	mov	rax, rsi
	sbb	rax, r11
	jc	.L1866
	mov	rbp, r15
	mov	r10, QWORD PTR 80[rsp]
	mov	r11, QWORD PTR 88[rsp]
	add	edi, 1
	mov	r14, QWORD PTR 96[rsp]
	mov	r15, QWORD PTR 104[rsp]
.L1867:
	mov	r9d, edi
	cmp	edi, 128
	ja	.L1905
	movabs	rax, 3688503277381496880
	lea	rcx, 304[rsp]
	movabs	rdx, 3976738051646829616
	mov	QWORD PTR 304[rsp], rax
	movabs	rax, 3544667369688283184
	mov	QWORD PTR 312[rsp], rdx
	movabs	rdx, 3832902143785906737
	mov	QWORD PTR 320[rsp], rax
	movabs	rax, 4121136918051239473
	mov	QWORD PTR 328[rsp], rdx
	movabs	rdx, 3689066235924983858
	mov	QWORD PTR 336[rsp], rax
	movabs	rax, 3977301010190316594
	mov	QWORD PTR 344[rsp], rdx
	movabs	rdx, 3545230328231770162
	mov	QWORD PTR 352[rsp], rax
	movabs	rax, 3833465102329393715
	mov	QWORD PTR 360[rsp], rdx
	movabs	rdx, 4121699876594726451
	mov	QWORD PTR 368[rsp], rax
	movabs	rax, 3689629194468470836
	mov	QWORD PTR 376[rsp], rdx
	movabs	rdx, 3977863968733803572
	mov	QWORD PTR 384[rsp], rax
	movabs	rax, 3545793286775257140
	mov	QWORD PTR 392[rsp], rdx
	movabs	rdx, 3834028060872880693
	mov	QWORD PTR 400[rsp], rax
	movabs	rax, 4122262835138213429
	mov	QWORD PTR 408[rsp], rdx
	movabs	rdx, 3690192153011957814
	mov	QWORD PTR 416[rsp], rax
	movabs	rax, 3978426927277290550
	mov	QWORD PTR 424[rsp], rdx
	movabs	rdx, 3546356245318744118
	mov	QWORD PTR 432[rsp], rax
	movabs	rax, 3834591019416367671
	mov	QWORD PTR 440[rsp], rdx
	movabs	rdx, 4122825793681700407
	mov	QWORD PTR 448[rsp], rax
	movabs	rax, 3690755111555444792
	mov	QWORD PTR 456[rsp], rdx
	movabs	rdx, 3978989885820777528
	mov	QWORD PTR 464[rsp], rax
	movabs	rax, 3546919203862231096
	mov	QWORD PTR 472[rsp], rdx
	movabs	rdx, 3835153977959854649
	mov	QWORD PTR 480[rsp], rax
	movabs	rax, 4122263930388298034
	mov	QWORD PTR 488[rsp], rdx
	movabs	rdx, 16106987313379638
	mov	QWORD PTR 489[rsp], rax
	mov	eax, 99
	cmp	rax, r10
	mov	eax, 0
	mov	QWORD PTR 497[rsp], rdx
	sbb	rax, r11
	jnc	.L1872
	mov	QWORD PTR 64[rsp], r14
	lea	ebx, -1[rdi]
	mov	r12, rbp
	movabs	r13, 1152921504606846975
	mov	QWORD PTR 72[rsp], r15
	mov	r15, r9
	.p2align 4
	.p2align 3
.L1873:
	mov	rax, r10
	mov	r8, r10
	mov	rsi, r10
	xor	r9d, r9d
	shrd	rax, r11, 60
	and	r8, r13
	mov	rdi, r11
	movabs	rbp, -8116567392432202711
	and	rax, r13
	mov	r14d, 25
	add	r8, rax
	mov	rax, r11
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
	lea	rax, [rax+rax*4]
	sub	r8, rax
	movabs	rax, 2951479051793528258
	sub	rsi, r8
	sbb	rdi, r9
	imul	rax, rsi
	mov	r9d, ebx
	imul	rbp, rdi
	add	rbp, rax
	movabs	rax, -8116567392432202711
	mul	rsi
	mov	rsi, rax
	and	eax, 3
	add	rbp, rdx
	mul	r14
	mov	rdi, rbp
	add	rax, r8
	xor	edx, edx
	mov	r8, r10
	add	rax, rax
	adc	rdx, rdx
	shr	rdi, 2
	mov	QWORD PTR 48[rsp], rax
	mov	QWORD PTR 56[rsp], rdx
	mov	rdx, r11
	mov	r11, rdi
	mov	rdi, QWORD PTR 48[rsp]
	shrd	rsi, rbp, 2
	mov	r10, rsi
	movzx	esi, BYTE PTR 1[rcx+rdi]
	movzx	eax, BYTE PTR [rcx+rdi]
	mov	BYTE PTR 163[rsp+r9], sil
	lea	r9d, -1[rbx]
	sub	ebx, 2
	mov	BYTE PTR 163[rsp+r9], al
	mov	eax, 9999
	cmp	rax, r8
	mov	eax, 0
	sbb	rax, rdx
	jc	.L1873
	mov	eax, 999
	mov	r9, r15
	mov	rbp, r12
	mov	r15, QWORD PTR 72[rsp]
	cmp	rax, r8
	mov	eax, 0
	sbb	rax, rdx
	jc	.L1872
.L1865:
	add	r10d, 48
.L1874:
	lea	rdi, 163[rsp]
	mov	BYTE PTR 163[rsp], r10b
	lea	rsi, [rdi+r9]
	jmp	.L1929
	.p2align 4,,10
	.p2align 3
.L1939:
	bsr	rax, r11
	lea	edx, 67[rax]
	mov	eax, 2863311531
	imul	rdx, rax
	shr	rdx, 33
	mov	eax, edx
	sub	edx, 1
	jmp	.L1876
	.p2align 4,,10
	.p2align 3
.L1937:
	movabs	rbx, 3978425819141910832
	bsr	rax, r11
	movabs	rsi, 7378413942531504440
	lea	edx, 68[rax]
	mov	QWORD PTR 304[rsp], rbx
	shr	edx, 2
	mov	QWORD PTR 312[rsp], rsi
	mov	r8d, edx
	sub	edx, 1
	jmp	.L1885
	.p2align 4,,10
	.p2align 3
.L1935:
	bsr	rdx, r11
	xor	rdx, 63
	jmp	.L1928
	.p2align 4,,10
	.p2align 3
.L1909:
	lea	rsi, 164[rsp]
	lea	r13, .LC28[rip]
	lea	rdi, 163[rsp]
.L1882:
	mov	r12, rdi
	.p2align 4
	.p2align 3
.L1890:
	movsx	ecx, BYTE PTR [r12]
	add	r12, 1
	call	toupper
	mov	BYTE PTR -1[r12], al
	cmp	r12, rsi
	jne	.L1890
	mov	eax, 2
	jmp	.L1881
	.p2align 4,,10
	.p2align 3
.L1888:
	movzx	edx, BYTE PTR [rcx+r10]
	jmp	.L1889
	.p2align 4,,10
	.p2align 3
.L1879:
	add	r10d, 48
	jmp	.L1880
	.p2align 4,,10
	.p2align 3
.L1872:
	add	r10, r10
	movzx	eax, BYTE PTR 1[rcx+r10]
	movzx	r10d, BYTE PTR [rcx+r10]
	mov	BYTE PTR 164[rsp], al
	jmp	.L1874
	.p2align 4,,10
	.p2align 3
.L1936:
	mov	rax, r14
	or	rax, r15
	jne	.L1906
	mov	rax, QWORD PTR 592[rsp]
	mov	BYTE PTR 163[rsp], 48
	movzx	eax, BYTE PTR [rax]
	test	al, 16
	je	.L1864
	mov	rdx, -2
	lea	rsi, 164[rsp]
	lea	r13, .LC29[rip]
	mov	eax, 2
	lea	rdi, 163[rsp]
	jmp	.L1862
	.p2align 4,,10
	.p2align 3
.L1940:
	mov	rbp, r15
	mov	r10, QWORD PTR 80[rsp]
	mov	r11, QWORD PTR 88[rsp]
	add	edi, 2
	mov	r14, QWORD PTR 96[rsp]
	mov	r15, QWORD PTR 104[rsp]
	jmp	.L1867
	.p2align 4,,10
	.p2align 3
.L1941:
	mov	rbp, r15
	mov	r10, QWORD PTR 80[rsp]
	mov	r11, QWORD PTR 88[rsp]
	add	edi, 3
	mov	r14, QWORD PTR 96[rsp]
	mov	r15, QWORD PTR 104[rsp]
	jmp	.L1867
	.p2align 4,,10
	.p2align 3
.L1942:
	mov	rbp, r15
	mov	r10, QWORD PTR 80[rsp]
	mov	r11, QWORD PTR 88[rsp]
	mov	r14, QWORD PTR 96[rsp]
	mov	r15, QWORD PTR 104[rsp]
	jmp	.L1867
	.p2align 4,,10
	.p2align 3
.L1901:
	mov	eax, 1
	lea	rdi, 163[rsp]
	jmp	.L1860
.L1908:
	lea	r13, .LC28[rip]
	jmp	.L1849
.L1905:
	lea	rsi, 291[rsp]
	lea	rdi, 163[rsp]
	jmp	.L1929
.L1906:
	lea	r13, .LC29[rip]
	jmp	.L1849
.L1903:
	mov	r9d, 1
	jmp	.L1865
.L1842:
	lea	rcx, .LC31[rip]
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
.LFB5641:
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
	sub	rsp, 472
	.seh_stackalloc	472
	.seh_endprologue
	movzx	eax, BYTE PTR 1[rcx]
	mov	r10, QWORD PTR [rdx]
	mov	r11, QWORD PTR 8[rdx]
	mov	r9d, eax
	and	r9d, 120
	mov	r12, r8
	cmp	r9b, 56
	je	.L2023
	shr	al, 3
	and	eax, 15
	cmp	al, 4
	je	.L1947
	ja	.L1948
	cmp	al, 1
	jbe	.L1949
	cmp	r9b, 16
	lea	rax, .LC27[rip]
	lea	rbp, .LC26[rip]
	cmovne	rbp, rax
	mov	rax, r10
	or	rax, r11
	jne	.L2024
	mov	eax, 48
	lea	rbx, 116[rsp]
	lea	rsi, 115[rsp]
.L1954:
	movzx	edx, BYTE PTR [rcx]
	mov	BYTE PTR 115[rsp], al
	test	dl, 16
	je	.L2022
.L2005:
	mov	r10, -2
	mov	eax, 2
.L1959:
	add	r10, rsi
	mov	r11d, eax
	test	eax, eax
	je	.L1960
	xor	eax, eax
.L1991:
	mov	r8d, eax
	add	eax, 1
	movzx	r9d, BYTE PTR 0[rbp+r8]
	mov	BYTE PTR [r10+r8], r9b
	cmp	eax, r11d
	jb	.L1991
	jmp	.L1960
	.p2align 4,,10
	.p2align 3
.L2023:
	mov	eax, 127
	cmp	rax, r10
	mov	eax, 0
	sbb	rax, r11
	jc	.L1945
	mov	DWORD PTR 32[rsp], 1
	lea	rax, 256[rsp]
	mov	r9, rcx
	mov	edx, 1
	lea	rcx, 96[rsp]
	mov	BYTE PTR 256[rsp], r10b
	mov	QWORD PTR 96[rsp], 1
	mov	QWORD PTR 104[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1946:
	add	rsp, 472
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
.L1949:
	mov	rax, r10
	or	rax, r11
	jne	.L1961
	mov	BYTE PTR 115[rsp], 48
	lea	rbx, 116[rsp]
	lea	rsi, 115[rsp]
.L1962:
	movzx	edx, BYTE PTR [rcx]
	mov	r10, rsi
.L1960:
	shr	dl, 2
	mov	eax, 43
	and	edx, 3
	cmp	edx, 1
	je	.L1995
	cmp	edx, 3
	je	.L2007
.L1994:
	mov	rax, rbx
	sub	rsi, r10
	lea	rdx, 96[rsp]
	mov	r9, r12
	sub	rax, r10
	mov	r8, rsi
	mov	QWORD PTR 104[rsp], r10
	mov	QWORD PTR 96[rsp], rax
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L1946
	.p2align 4,,10
	.p2align 3
.L1947:
	mov	rax, r10
	or	rax, r11
	je	.L1972
	test	r11, r11
	jne	.L1973
	bsr	rax, r10
	mov	r8d, 63
	lea	edx, 3[rax]
	mov	eax, 2863311531
	imul	rdx, rax
	shr	rdx, 33
	mov	eax, edx
	cmp	r8, r10
	jnb	.L1976
	sub	edx, 1
.L1975:
	mov	esi, 63
	xor	ebx, ebx
	.p2align 4
	.p2align 3
.L1977:
	mov	r8, r10
	mov	edi, edx
	lea	r9d, -1[rdx]
	sub	edx, 2
	and	r8d, 7
	add	r8d, 48
	mov	BYTE PTR 115[rsp+rdi], r8b
	mov	r8, r10
	shrd	r10, r11, 6
	shrd	r8, r11, 3
	shr	r11, 6
	mov	rdi, r8
	and	edi, 7
	cmp	rsi, r10
	lea	r8d, 48[rdi]
	mov	rdi, rbx
	sbb	rdi, r11
	mov	BYTE PTR 115[rsp+r9], r8b
	jc	.L1977
.L1976:
	mov	edx, 7
	cmp	rdx, r10
	mov	edx, 0
	sbb	rdx, r11
	jnc	.L1978
	mov	r8, r10
	shrd	r10, r11, 3
	and	r8d, 7
	add	r10d, 48
	add	r8d, 48
	mov	BYTE PTR 116[rsp], r8b
.L1979:
	mov	BYTE PTR 115[rsp], r10b
	lea	rsi, 115[rsp]
	lea	rbp, .LC30[rip]
	lea	rbx, [rsi+rax]
	mov	eax, 1
.L1980:
	movzx	edx, BYTE PTR [rcx]
	mov	r10, rsi
	test	dl, 16
	je	.L1960
	mov	r10, rax
	neg	r10
	jmp	.L1959
	.p2align 4,,10
	.p2align 3
.L1948:
	cmp	r9b, 40
	je	.L2025
	mov	rax, r10
	or	rax, r11
	jne	.L2003
	mov	BYTE PTR 115[rsp], 48
	cmp	r9b, 48
	je	.L2004
	lea	rbp, .LC28[rip]
	lea	rbx, 116[rsp]
	lea	rsi, 115[rsp]
	jmp	.L1982
	.p2align 4,,10
	.p2align 3
.L2007:
	mov	eax, 32
.L1995:
	mov	BYTE PTR -1[r10], al
	sub	r10, 1
	jmp	.L1994
	.p2align 4,,10
	.p2align 3
.L2003:
	lea	rbp, .LC28[rip]
.L1981:
	test	r11, r11
	jne	.L2026
	movabs	rbx, 3978425819141910832
	bsr	rax, r10
	movabs	rsi, 7378413942531504440
	mov	QWORD PTR 256[rsp], rbx
	lea	edx, 4[rax]
	mov	ebx, 255
	shr	edx, 2
	cmp	rbx, r10
	mov	QWORD PTR 264[rsp], rsi
	lea	rbx, 256[rsp]
	mov	r8d, edx
	jnb	.L1986
	sub	edx, 1
.L1985:
	lea	rbx, 256[rsp]
	xor	eax, eax
	.p2align 4
	.p2align 3
.L1987:
	mov	rsi, r10
	mov	r13d, edx
	lea	edi, -1[rdx]
	sub	edx, 2
	and	esi, 15
	movzx	esi, BYTE PTR [rbx+rsi]
	mov	BYTE PTR 115[rsp+r13], sil
	mov	rsi, r10
	shrd	r10, r11, 8
	shrd	rsi, r11, 4
	shr	r11, 8
	and	esi, 15
	movzx	esi, BYTE PTR [rbx+rsi]
	mov	BYTE PTR 115[rsp+rdi], sil
	mov	edi, 255
	cmp	rdi, r10
	mov	rdi, rax
	sbb	rdi, r11
	jc	.L1987
.L1986:
	mov	edx, 15
	cmp	rdx, r10
	mov	edx, 0
	sbb	rdx, r11
	jnc	.L1988
	mov	rsi, r10
	and	esi, 15
	movzx	edx, BYTE PTR [rbx+rsi]
	mov	BYTE PTR 116[rsp], dl
	mov	rdx, r10
	shrd	rdx, r11, 4
	movzx	edx, BYTE PTR [rdx+rbx]
.L1989:
	lea	rsi, 115[rsp]
	mov	BYTE PTR 115[rsp], dl
	lea	rbx, [rsi+r8]
	cmp	r9b, 48
	je	.L1983
.L1982:
	movzx	edx, BYTE PTR [rcx]
	test	dl, 16
	jne	.L2005
.L2022:
	mov	r10, rsi
	jmp	.L1960
	.p2align 4,,10
	.p2align 3
.L2024:
	test	r11, r11
	jne	.L2027
	bsr	rax, r10
	xor	rax, 63
	lea	edx, 64[rax]
	cmp	eax, 63
	je	.L1997
.L2021:
	mov	r9d, 127
	mov	eax, 128
	lea	rsi, 115[rsp]
	sub	r9d, edx
	sub	eax, edx
	mov	ebx, r9d
	sub	r9d, 1
	cdqe
	lea	rdi, 114[rsp+rbx]
	lea	rdx, [rsi+rbx]
	sub	rdi, r9
	.p2align 5
	.p2align 4
	.p2align 3
.L1958:
	mov	r8d, r10d
	sub	rdx, 1
	shrd	r10, r11, 1
	and	r8d, 1
	shr	r11
	add	r8d, 48
	mov	BYTE PTR 1[rdx], r8b
	cmp	rdi, rdx
	jne	.L1958
.L1957:
	lea	rbx, [rsi+rax]
	mov	eax, 49
	jmp	.L1954
	.p2align 4,,10
	.p2align 3
.L1961:
	mov	eax, 9
	cmp	rax, r10
	mov	eax, 0
	sbb	rax, r11
	jnc	.L1999
	mov	QWORD PTR 544[rsp], rcx
	mov	rsi, r10
	mov	rbx, r11
	xor	edi, edi
	mov	ebp, 1
	lea	r13, 80[rsp]
	mov	r14, r10
	mov	r15, r11
	mov	QWORD PTR 560[rsp], r8
	jmp	.L1968
	.p2align 4,,10
	.p2align 3
.L1964:
	mov	eax, 999
	cmp	rax, rsi
	mov	rax, rdi
	sbb	rax, rbx
	jnc	.L2028
	mov	eax, 9999
	cmp	rax, rsi
	mov	rax, rdi
	sbb	rax, rbx
	jnc	.L2029
	mov	rcx, r13
	lea	rdx, 64[rsp]
	mov	QWORD PTR 80[rsp], rsi
	add	ebp, 4
	mov	QWORD PTR 88[rsp], rbx
	mov	QWORD PTR 64[rsp], 10000
	mov	QWORD PTR 72[rsp], 0
	call	__udivti3
	mov	ecx, 99999
	cmp	rcx, rsi
	mov	rcx, rdi
	movaps	XMMWORD PTR 48[rsp], xmm0
	sbb	rcx, rbx
	jnc	.L2030
	mov	rsi, QWORD PTR 48[rsp]
	mov	rbx, QWORD PTR 56[rsp]
.L1968:
	mov	eax, 99
	cmp	rax, rsi
	mov	rax, rdi
	sbb	rax, rbx
	jc	.L1964
	mov	rcx, QWORD PTR 544[rsp]
	mov	r10, r14
	mov	r11, r15
	add	ebp, 1
	mov	r12, QWORD PTR 560[rsp]
.L1965:
	mov	r9d, ebp
	cmp	ebp, 128
	ja	.L2001
	movabs	rax, 3688503277381496880
	lea	rbx, 256[rsp]
	movabs	rdx, 3976738051646829616
	mov	QWORD PTR 256[rsp], rax
	movabs	rax, 3544667369688283184
	mov	QWORD PTR 264[rsp], rdx
	movabs	rdx, 3832902143785906737
	mov	QWORD PTR 272[rsp], rax
	movabs	rax, 4121136918051239473
	mov	QWORD PTR 280[rsp], rdx
	movabs	rdx, 3689066235924983858
	mov	QWORD PTR 288[rsp], rax
	movabs	rax, 3977301010190316594
	mov	QWORD PTR 296[rsp], rdx
	movabs	rdx, 3545230328231770162
	mov	QWORD PTR 304[rsp], rax
	movabs	rax, 3833465102329393715
	mov	QWORD PTR 312[rsp], rdx
	movabs	rdx, 4121699876594726451
	mov	QWORD PTR 320[rsp], rax
	movabs	rax, 3689629194468470836
	mov	QWORD PTR 328[rsp], rdx
	movabs	rdx, 3977863968733803572
	mov	QWORD PTR 336[rsp], rax
	movabs	rax, 3545793286775257140
	mov	QWORD PTR 344[rsp], rdx
	movabs	rdx, 3834028060872880693
	mov	QWORD PTR 352[rsp], rax
	movabs	rax, 4122262835138213429
	mov	QWORD PTR 360[rsp], rdx
	movabs	rdx, 3690192153011957814
	mov	QWORD PTR 368[rsp], rax
	movabs	rax, 3978426927277290550
	mov	QWORD PTR 376[rsp], rdx
	movabs	rdx, 3546356245318744118
	mov	QWORD PTR 384[rsp], rax
	movabs	rax, 3834591019416367671
	mov	QWORD PTR 392[rsp], rdx
	movabs	rdx, 4122825793681700407
	mov	QWORD PTR 400[rsp], rax
	movabs	rax, 3690755111555444792
	mov	QWORD PTR 408[rsp], rdx
	movabs	rdx, 3978989885820777528
	mov	QWORD PTR 416[rsp], rax
	movabs	rax, 3546919203862231096
	mov	QWORD PTR 424[rsp], rdx
	movabs	rdx, 3835153977959854649
	mov	QWORD PTR 432[rsp], rax
	movabs	rax, 4122263930388298034
	mov	QWORD PTR 440[rsp], rdx
	movabs	rdx, 16106987313379638
	mov	QWORD PTR 441[rsp], rax
	mov	eax, 99
	cmp	rax, r10
	mov	eax, 0
	mov	QWORD PTR 449[rsp], rdx
	sbb	rax, r11
	jnc	.L1969
	mov	QWORD PTR 560[rsp], r12
	sub	ebp, 1
	mov	r15, r9
	mov	r12, rcx
	lea	r13, 256[rsp]
	.p2align 4
	.p2align 3
.L1970:
	mov	rax, r10
	mov	rcx, r10
	xor	edi, edi
	movabs	rbx, 1152921504606846975
	movabs	rsi, 1152921504606846975
	shrd	rax, r11, 60
	movabs	r8, -8116567392432202711
	and	rax, rbx
	and	rsi, r10
	mov	rbx, r11
	add	rsi, rax
	mov	rax, r11
	shr	rax, 56
	add	rsi, rax
	movabs	rax, 5165088340638674453
	mul	rsi
	mov	rax, rsi
	sub	rax, rdx
	shr	rax
	add	rdx, rax
	shr	rdx, 4
	lea	rax, [rdx+rdx*4]
	lea	rax, [rax+rax*4]
	sub	rsi, rax
	movabs	rax, 2951479051793528258
	sub	rcx, rsi
	sbb	rbx, rdi
	imul	rax, rcx
	imul	r8, rbx
	add	r8, rax
	movabs	rax, -8116567392432202711
	mul	rcx
	add	r8, rdx
	mov	rcx, rax
	and	eax, 3
	mov	rbx, r8
	mov	r8d, 25
	mul	r8
	mov	r8, r10
	mov	rdx, r11
	add	rax, rsi
	add	rax, rax
	shrd	rcx, rbx, 2
	movzx	r9d, BYTE PTR 1[r13+rax]
	mov	r10, rcx
	mov	ecx, ebp
	shr	rbx, 2
	movzx	eax, BYTE PTR 0[r13+rax]
	mov	r11, rbx
	mov	BYTE PTR 115[rsp+rcx], r9b
	lea	ecx, -1[rbp]
	sub	ebp, 2
	mov	BYTE PTR 115[rsp+rcx], al
	mov	eax, 9999
	cmp	rax, r8
	mov	eax, 0
	sbb	rax, rdx
	jc	.L1970
	mov	eax, 999
	mov	rcx, r12
	mov	r9, r15
	mov	rbx, r13
	cmp	rax, r8
	mov	eax, 0
	mov	r12, QWORD PTR 560[rsp]
	sbb	rax, rdx
	jc	.L1969
.L1963:
	add	r10d, 48
.L1971:
	lea	rsi, 115[rsp]
	mov	BYTE PTR 115[rsp], r10b
	lea	rbx, [rsi+r9]
	jmp	.L1962
	.p2align 4,,10
	.p2align 3
.L1972:
	lea	rsi, 115[rsp]
	mov	BYTE PTR 115[rsp], 48
	movzx	edx, BYTE PTR [rcx]
	lea	rbx, 116[rsp]
	mov	r10, rsi
	jmp	.L1960
	.p2align 4,,10
	.p2align 3
.L2025:
	mov	rax, r10
	or	rax, r11
	jne	.L2002
	mov	BYTE PTR 115[rsp], 48
	lea	rbx, 116[rsp]
	lea	rsi, 115[rsp]
	lea	rbp, .LC29[rip]
	jmp	.L1982
	.p2align 4,,10
	.p2align 3
.L2026:
	movabs	rbx, 3978425819141910832
	bsr	rax, r11
	movabs	rsi, 7378413942531504440
	lea	edx, 68[rax]
	mov	QWORD PTR 256[rsp], rbx
	shr	edx, 2
	mov	QWORD PTR 264[rsp], rsi
	mov	r8d, edx
	sub	edx, 1
	jmp	.L1985
	.p2align 4,,10
	.p2align 3
.L2027:
	bsr	rdx, r11
	xor	rdx, 63
	jmp	.L2021
	.p2align 4,,10
	.p2align 3
.L1973:
	bsr	rax, r11
	lea	edx, 67[rax]
	mov	eax, 2863311531
	imul	rdx, rax
	shr	rdx, 33
	mov	eax, edx
	sub	edx, 1
	jmp	.L1975
	.p2align 4,,10
	.p2align 3
.L2002:
	lea	rbp, .LC29[rip]
	jmp	.L1981
	.p2align 4,,10
	.p2align 3
.L2004:
	lea	rbx, 116[rsp]
	lea	rbp, .LC28[rip]
	lea	rsi, 115[rsp]
.L1983:
	mov	rdi, rsi
	mov	r15, rsi
	mov	rsi, rcx
	.p2align 4
	.p2align 3
.L1990:
	movsx	ecx, BYTE PTR [rdi]
	add	rdi, 1
	call	toupper
	mov	BYTE PTR -1[rdi], al
	cmp	rdi, rbx
	jne	.L1990
	mov	rcx, rsi
	mov	eax, 2
	mov	rsi, r15
	jmp	.L1980
	.p2align 4,,10
	.p2align 3
.L1988:
	movzx	edx, BYTE PTR [rbx+r10]
	jmp	.L1989
	.p2align 4,,10
	.p2align 3
.L1978:
	add	r10d, 48
	jmp	.L1979
	.p2align 4,,10
	.p2align 3
.L1969:
	add	r10, r10
	movzx	eax, BYTE PTR 1[rbx+r10]
	movzx	r10d, BYTE PTR [rbx+r10]
	mov	BYTE PTR 116[rsp], al
	jmp	.L1971
	.p2align 4,,10
	.p2align 3
.L2028:
	mov	rcx, QWORD PTR 544[rsp]
	mov	r10, r14
	mov	r11, r15
	add	ebp, 2
	mov	r12, QWORD PTR 560[rsp]
	jmp	.L1965
	.p2align 4,,10
	.p2align 3
.L2029:
	mov	rcx, QWORD PTR 544[rsp]
	mov	r10, r14
	mov	r11, r15
	add	ebp, 3
	mov	r12, QWORD PTR 560[rsp]
	jmp	.L1965
	.p2align 4,,10
	.p2align 3
.L2030:
	mov	rcx, QWORD PTR 544[rsp]
	mov	r12, QWORD PTR 560[rsp]
	mov	r10, r14
	mov	r11, r15
	jmp	.L1965
	.p2align 4,,10
	.p2align 3
.L1997:
	mov	eax, 1
	lea	rsi, 115[rsp]
	jmp	.L1957
.L2001:
	lea	rbx, 243[rsp]
	lea	rsi, 115[rsp]
	jmp	.L1962
.L1999:
	mov	r9d, 1
	jmp	.L1963
.L1945:
	lea	rcx, .LC31[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB32:
	.text
.LHOTB32:
	.align 2
	.p2align 4
	.def	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0:
.LFB6175:
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
	sub	rsp, 152
	.seh_stackalloc	152
	.seh_endprologue
	mov	rdi, QWORD PTR [rdx]
	mov	rsi, QWORD PTR 8[rdx]
	lea	rbp, 16[rcx]
	mov	BYTE PTR 16[rcx], 0
	mov	rbx, rcx
	mov	r14d, r8d
	mov	QWORD PTR [rcx], rbp
	mov	r12, r9
	mov	QWORD PTR 8[rcx], 0
.LEHB26:
	call	_ZNSt6locale7classicEv
	mov	rdx, rax
	mov	rcx, r12
	call	_ZNKSt6localeeqERKS_
	test	al, al
	je	.L2097
.L2031:
	mov	rax, rbx
	add	rsp, 152
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
.L2097:
	mov	rcx, QWORD PTR .refptr._ZNSt7__cxx118numpunctIcE2idE[rip]
	call	_ZNKSt6locale2id5_M_idEv
	mov	rdx, rax
	mov	rax, QWORD PTR [r12]
	mov	rax, QWORD PTR 8[rax]
	mov	r12, QWORD PTR [rax+rdx*8]
	test	r12, r12
	je	.L2033
	mov	rax, QWORD PTR [r12]
	mov	rcx, r12
	call	[QWORD PTR 16[rax]]
	mov	BYTE PTR 63[rsp], al
	mov	rax, QWORD PTR [r12]
	lea	rcx, 112[rsp]
	mov	rdx, r12
	mov	QWORD PTR 104[rsp], rcx
	call	[QWORD PTR 32[rax]]
.LEHE26:
	cmp	QWORD PTR 120[rsp], 0
	jne	.L2076
	cmp	BYTE PTR 63[rsp], 46
	jne	.L2076
	mov	rcx, QWORD PTR 112[rsp]
	lea	rax, 128[rsp]
	cmp	rcx, rax
	jne	.L2059
	jmp	.L2031
	.p2align 4,,10
	.p2align 3
.L2076:
	test	rdi, rdi
	je	.L2037
	mov	r8, rdi
	mov	edx, 46
	mov	rcx, rsi
	call	memchr
	movsx	edx, r14b
	mov	r8, rdi
	mov	rcx, rsi
	mov	QWORD PTR 64[rsp], rax
	call	memchr
	mov	r9, QWORD PTR 64[rsp]
	test	r9, r9
	je	.L2038
	sub	r9, rsi
	mov	QWORD PTR 64[rsp], r9
	test	rax, rax
	je	.L2065
.L2064:
	mov	rdx, QWORD PTR 64[rsp]
	sub	rax, rsi
	cmp	rax, rdx
	cmova	rax, rdx
	mov	r14, rax
.L2039:
	cmp	r14, -1
	je	.L2040
	mov	rdx, rdi
	sub	rdx, r14
	mov	r13, rdx
.L2041:
	mov	r10, QWORD PTR [rbx]
	lea	r9, 0[r13+r14*2]
	cmp	rbp, r10
	je	.L2098
	mov	rax, QWORD PTR 16[rbx]
	cmp	rax, r9
	jnb	.L2068
	movabs	rdx, 9223372036854775806
	cmp	rdx, r9
	jb	.L2044
	add	rax, rax
	cmp	r9, rax
	jb	.L2048
.L2046:
	lea	rcx, 1[r9]
.L2049:
	mov	QWORD PTR 80[rsp], r10
	mov	QWORD PTR 72[rsp], r9
.LEHB27:
	call	_Znwy
.LEHE27:
	mov	r15, rax
	mov	rax, QWORD PTR 8[rbx]
	mov	r9, QWORD PTR 72[rsp]
	mov	r10, QWORD PTR 80[rsp]
	test	rax, rax
	lea	r8, 1[rax]
	je	.L2099
	mov	rdx, r10
	mov	rcx, r15
	mov	QWORD PTR 80[rsp], r9
	mov	QWORD PTR 72[rsp], r10
	call	memcpy
	mov	r10, QWORD PTR 72[rsp]
	mov	r9, QWORD PTR 80[rsp]
	cmp	rbp, r10
	je	.L2052
.L2051:
	mov	rax, QWORD PTR 16[rbx]
	mov	rcx, r10
	mov	QWORD PTR 72[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 72[rsp]
.L2052:
	mov	QWORD PTR [rbx], r15
	mov	QWORD PTR 16[rbx], r9
	jmp	.L2042
	.p2align 4,,10
	.p2align 3
.L2037:
	mov	QWORD PTR 64[rsp], -1
	mov	r15, QWORD PTR [rbx]
	xor	r14d, r14d
	xor	r13d, r13d
.L2042:
	movzx	edx, BYTE PTR [rsi]
	lea	eax, -32[rdx]
	cmp	al, 13
	ja	.L2071
	mov	ecx, 10241
	bt	rcx, rax
	jnc	.L2071
	mov	BYTE PTR [r15], dl
	lea	r10, 1[rsi]
	mov	QWORD PTR 72[rsp], 1
.L2054:
	mov	r9, QWORD PTR 120[rsp]
	mov	rax, QWORD PTR [r12]
	lea	rbp, [rsi+r14]
	mov	rcx, r12
	mov	r8, QWORD PTR 112[rsp]
	mov	QWORD PTR 96[rsp], r10
	mov	QWORD PTR 88[rsp], r9
	mov	QWORD PTR 80[rsp], r8
.LEHB28:
	call	[QWORD PTR 24[rax]]
.LEHE28:
	mov	r10, QWORD PTR 96[rsp]
	mov	rcx, QWORD PTR 72[rsp]
	mov	QWORD PTR 40[rsp], rbp
	movsx	edx, al
	mov	r9, QWORD PTR 88[rsp]
	mov	r8, QWORD PTR 80[rsp]
	mov	QWORD PTR 32[rsp], r10
	add	rcx, r15
	call	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	mov	rcx, rax
	test	r13, r13
	je	.L2055
	cmp	QWORD PTR 64[rsp], -1
	je	.L2056
	movzx	eax, BYTE PTR 63[rsp]
	add	rcx, 1
	mov	BYTE PTR -1[rcx], al
	lea	rax, 1[r14]
	sub	rdi, rax
	mov	r13, rdi
	jne	.L2100
.L2057:
	add	rcx, r13
.L2055:
	mov	rax, QWORD PTR [rbx]
	sub	rcx, r15
	mov	QWORD PTR 8[rbx], rcx
	mov	BYTE PTR [rax+rcx], 0
	mov	rcx, QWORD PTR 112[rsp]
	lea	rax, 128[rsp]
	cmp	rcx, rax
	je	.L2031
.L2059:
	mov	rax, QWORD PTR 128[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L2031
	.p2align 4,,10
	.p2align 3
.L2071:
	mov	QWORD PTR 72[rsp], 0
	mov	r10, rsi
	jmp	.L2054
	.p2align 4,,10
	.p2align 3
.L2100:
	lea	rbp, [rsi+rax]
.L2056:
	mov	r8, r13
	mov	rdx, rbp
	call	memcpy
	mov	rcx, rax
	jmp	.L2057
	.p2align 4,,10
	.p2align 3
.L2048:
	cmp	rdx, rax
	lea	r8, 1[rax]
	movabs	rcx, 9223372036854775807
	cmovb	rax, rdx
	cmovnb	rcx, r8
	mov	r9, rax
	jmp	.L2049
	.p2align 4,,10
	.p2align 3
.L2099:
	movzx	eax, BYTE PTR [r10]
	mov	BYTE PTR [r15], al
	cmp	rbp, r10
	jne	.L2051
	jmp	.L2052
	.p2align 4,,10
	.p2align 3
.L2068:
	mov	r15, r10
	jmp	.L2042
	.p2align 4,,10
	.p2align 3
.L2038:
	mov	QWORD PTR 64[rsp], -1
	test	rax, rax
	jne	.L2064
.L2040:
	mov	r14, rdi
	xor	r13d, r13d
	jmp	.L2041
	.p2align 4,,10
	.p2align 3
.L2098:
	cmp	r9, 15
	jbe	.L2066
	movabs	rax, 9223372036854775806
	cmp	rax, r9
	jb	.L2044
	cmp	r9, 29
	ja	.L2046
	mov	ecx, 31
	mov	r9d, 30
	jmp	.L2049
	.p2align 4,,10
	.p2align 3
.L2065:
	mov	r14, QWORD PTR 64[rsp]
	jmp	.L2039
.L2066:
	mov	r15, rbp
	jmp	.L2042
.L2075:
	jmp	.L2060
.L2094:
	jmp	.L2095
.L2092:
	jmp	.L2093
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA6175:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE6175-.LLSDACSB6175
.LLSDACSB6175:
	.uleb128 .LEHB26-.LFB6175
	.uleb128 .LEHE26-.LEHB26
	.uleb128 .L2092-.LFB6175
	.uleb128 0
	.uleb128 .LEHB27-.LFB6175
	.uleb128 .LEHE27-.LEHB27
	.uleb128 .L2094-.LFB6175
	.uleb128 0
	.uleb128 .LEHB28-.LFB6175
	.uleb128 .LEHE28-.LEHB28
	.uleb128 .L2075-.LFB6175
	.uleb128 0
.LLSDACSE6175:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0.cold
	.seh_stackalloc	216
	.seh_savereg	rbx, 152
	.seh_savereg	rsi, 160
	.seh_savereg	rdi, 168
	.seh_savereg	rbp, 176
	.seh_savereg	r12, 184
	.seh_savereg	r13, 192
	.seh_savereg	r14, 200
	.seh_savereg	r15, 208
	.seh_endprologue
_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0.cold:
.L2044:
	lea	rcx, .LC13[rip]
.LEHB29:
	call	_ZSt20__throw_length_errorPKc
.LEHE29:
.L2033:
.LEHB30:
	call	_ZSt16__throw_bad_castv
.LEHE30:
.L2060:
	xor	edx, edx
	mov	rsi, rax
	mov	QWORD PTR 8[rbx], rdx
	mov	rdx, QWORD PTR [rbx]
	mov	BYTE PTR [rdx], 0
.L2061:
	mov	rcx, QWORD PTR 104[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L2063:
	mov	rcx, rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rsi
.LEHB31:
	call	_Unwind_Resume
.LEHE31:
.L2074:
.L2095:
	mov	rsi, rax
	jmp	.L2061
.L2073:
.L2093:
	mov	rsi, rax
	jmp	.L2063
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC6175:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC6175-.LLSDACSBC6175
.LLSDACSBC6175:
	.uleb128 .LEHB29-.LCOLDB32
	.uleb128 .LEHE29-.LEHB29
	.uleb128 .L2074-.LCOLDB32
	.uleb128 0
	.uleb128 .LEHB30-.LCOLDB32
	.uleb128 .LEHE30-.LEHB30
	.uleb128 .L2073-.LCOLDB32
	.uleb128 0
	.uleb128 .LEHB31-.LCOLDB32
	.uleb128 .LEHE31-.LEHB31
	.uleb128 0
	.uleb128 0
.LLSDACSEC6175:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE32:
	.text
.LHOTE32:
	.section .rdata,"dr"
.LC34:
	.ascii "basic_string::_M_replace\0"
.LC35:
	.ascii "basic_string_view::substr\0"
	.align 8
.LC36:
	.ascii "%s: __pos (which is %zu) > __size (which is %zu)\0"
.LC37:
	.ascii "basic_string::insert\0"
	.align 8
.LC38:
	.ascii "%s: __pos (which is %zu) > this->size() (which is %zu)\0"
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5612:
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
	fld	TBYTE PTR [rdx]
	mov	BYTE PTR 208[rsp], 0
	movzx	edx, BYTE PTR 1[rcx]
	mov	rsi, rcx
	mov	r12, r8
	lea	r13, 208[rsp]
	fstp	TBYTE PTR 48[rsp]
	mov	QWORD PTR 192[rsp], r13
	mov	QWORD PTR 200[rsp], 0
	test	dl, 6
	jne	.L2422
	mov	eax, edx
	shr	al, 3
	and	eax, 15
	cmp	al, 8
	ja	.L2103
	lea	rcx, .L2295[rip]
	movzx	eax, al
	movsxd	rax, DWORD PTR [rcx+rax*4]
	add	rax, rcx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2295:
	.long	.L2119-.L2295
	.long	.L2115-.L2295
	.long	.L2296-.L2295
	.long	.L2339-.L2295
	.long	.L2340-.L2295
	.long	.L2341-.L2295
	.long	.L2342-.L2295
	.long	.L2343-.L2295
	.long	.L2344-.L2295
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2119:
	fld	TBYTE PTR 48[rsp]
	lea	rbx, 160[rsp]
	lea	rdi, 144[rsp]
	mov	r9, rdi
	lea	r8, 416[rsp]
	mov	rcx, rbx
	lea	rdx, 289[rsp]
	fstp	TBYTE PTR 144[rsp]
	call	_ZSt8to_charsPcS_e
	mov	rbp, QWORD PTR 160[rsp]
	cmp	DWORD PTR 168[rsp], 132
	mov	QWORD PTR 64[rsp], 6
	je	.L2305
	lea	rax, 416[rsp]
	mov	BYTE PTR 72[rsp], 0
	lea	rbx, 289[rsp]
	mov	BYTE PTR 110[rsp], 101
	mov	QWORD PTR 80[rsp], rax
.L2120:
	fld	TBYTE PTR 48[rsp]
	movzx	r9d, BYTE PTR [rsi]
	fxam
	fnstsw	ax
	fstp	st(0)
	test	ah, 2
	jne	.L2415
	mov	eax, r9d
	and	eax, 12
	cmp	al, 4
	je	.L2423
	xor	r11d, r11d
	cmp	al, 12
	je	.L2424
.L2147:
	mov	rdi, rbp
	sub	rdi, rbx
	test	r9b, 16
	je	.L2151
	fld	TBYTE PTR 48[rsp]
	fabs
	fld	TBYTE PTR .LC33[rip]
	fucomip	st, st(1)
	fstp	st(0)
	jb	.L2151
	test	rdi, rdi
	je	.L2312
	mov	r8, rdi
	mov	edx, 46
	mov	rcx, rbx
	mov	BYTE PTR 96[rsp], r9b
	mov	BYTE PTR 88[rsp], r11b
	call	memchr
	movzx	r11d, BYTE PTR 88[rsp]
	movzx	r9d, BYTE PTR 96[rsp]
	test	rax, rax
	je	.L2153
	sub	rax, rbx
	mov	QWORD PTR 88[rsp], rax
	cmp	rax, -1
	je	.L2153
	lea	r14, 1[rax]
	cmp	r14, rdi
	jnb	.L2425
	movsx	edx, BYTE PTR 110[rsp]
	mov	r8, rdi
	lea	rcx, [rbx+r14]
	mov	BYTE PTR 111[rsp], r9b
	sub	r8, r14
	mov	BYTE PTR 96[rsp], r11b
	call	memchr
	movzx	r11d, BYTE PTR 96[rsp]
	movzx	r9d, BYTE PTR 111[rsp]
	test	rax, rax
	je	.L2315
	sub	rax, rbx
	mov	r10, rax
	cmp	rax, -1
	cmove	r10, rdi
.L2158:
	xor	r15d, r15d
	cmp	r10, QWORD PTR 88[rsp]
	sete	r15b
	cmp	BYTE PTR 72[rsp], 0
	je	.L2317
	cmp	BYTE PTR [rbx+r11], 48
	je	.L2159
.L2156:
	mov	rax, r10
	sub	rax, r11
	sub	rax, 1
.L2160:
	cmp	QWORD PTR 64[rsp], 0
	jne	.L2162
	.p2align 4
	.p2align 3
.L2155:
	test	r15, r15
	je	.L2151
.L2161:
	mov	r9, QWORD PTR 200[rsp]
	lea	r14, [rdi+r15]
	test	r9, r9
	jne	.L2163
	mov	rax, QWORD PTR 80[rsp]
	sub	rax, rbp
	cmp	rax, r15
	jnb	.L2164
	mov	rdx, QWORD PTR 192[rsp]
	cmp	rdx, r13
	je	.L2426
	mov	rax, QWORD PTR 208[rsp]
	cmp	rax, r14
	jnb	.L2170
.L2174:
	movabs	rcx, 9223372036854775806
	cmp	rcx, r14
	jb	.L2171
	add	rax, rax
	lea	r8, 1[r14]
	cmp	r14, rax
	jnb	.L2178
	cmp	rcx, rax
	lea	r11, 1[rax]
	movabs	r8, 9223372036854775807
	cmovb	rax, rcx
	cmovnb	r8, r11
	mov	r14, rax
.L2178:
	mov	rcx, r8
	mov	QWORD PTR 96[rsp], r9
	mov	QWORD PTR 80[rsp], rdx
	mov	QWORD PTR 72[rsp], r10
.LEHB32:
	call	_Znwy
.LEHE32:
	mov	r9, QWORD PTR 96[rsp]
	mov	rdx, QWORD PTR 80[rsp]
	mov	rbp, rax
	mov	r10, QWORD PTR 72[rsp]
.L2173:
	lea	r8, 1[r9]
	test	r9, r9
	je	.L2427
	mov	rcx, rbp
	mov	QWORD PTR 72[rsp], r10
	call	memcpy
	mov	r10, QWORD PTR 72[rsp]
.L2180:
	mov	rcx, QWORD PTR 192[rsp]
	cmp	rcx, r13
	je	.L2428
	mov	rax, QWORD PTR 208[rsp]
	mov	QWORD PTR 72[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 200[rsp]
	mov	r10, QWORD PTR 72[rsp]
	mov	QWORD PTR 192[rsp], rbp
	mov	QWORD PTR 208[rsp], r14
	test	r9, r9
	je	.L2170
.L2168:
	cmp	r9, r10
	jb	.L2429
	movabs	rax, 9223372036854775806
	mov	rdx, rax
	sub	rdx, r9
	cmp	rdx, r15
	jb	.L2430
	mov	rbp, QWORD PTR 192[rsp]
	lea	rdi, [r9+r15]
	cmp	rbp, r13
	je	.L2431
	mov	rbx, QWORD PTR 208[rsp]
	cmp	rbx, rdi
	jb	.L2236
.L2232:
	lea	rcx, 0[rbp+r10]
	sub	r9, r10
	je	.L2237
	cmp	r9, 1
	je	.L2432
	mov	rdx, rcx
	mov	r8, r9
	add	rcx, r15
	mov	QWORD PTR 64[rsp], r10
	call	memmove
	mov	r10, QWORD PTR 64[rsp]
	mov	rcx, QWORD PTR 192[rsp]
	add	rcx, r10
.L2237:
	cmp	r15, 1
	je	.L2433
	mov	r8, r15
	mov	edx, 48
	mov	QWORD PTR 64[rsp], r10
	call	memset
	mov	r10, QWORD PTR 64[rsp]
.L2248:
	mov	rax, QWORD PTR 192[rsp]
	mov	QWORD PTR 200[rsp], rdi
	mov	BYTE PTR [rax+rdi], 0
	cmp	r10, QWORD PTR 88[rsp]
	jne	.L2228
	mov	rax, QWORD PTR 192[rsp]
	mov	BYTE PTR [rax+r10], 46
	.p2align 4
	.p2align 3
.L2228:
	mov	rdi, QWORD PTR 200[rsp]
	mov	rbx, QWORD PTR 192[rsp]
.L2183:
	lea	rbp, 240[rsp]
	mov	BYTE PTR 240[rsp], 0
	mov	QWORD PTR 224[rsp], rbp
	mov	QWORD PTR 232[rsp], 0
	test	BYTE PTR [rsi], 32
	je	.L2251
.L2291:
	lea	r15, 24[r12]
	cmp	BYTE PTR 32[r12], 0
	je	.L2434
.L2252:
	mov	rdx, r15
	lea	rcx, 184[rsp]
	call	_ZNSt6localeC1ERKS_
	movzx	r8d, BYTE PTR 110[rsp]
	lea	rcx, 256[rsp]
	lea	rdx, 112[rsp]
	lea	r9, 184[rsp]
	mov	QWORD PTR 112[rsp], rdi
	mov	QWORD PTR 120[rsp], rbx
.LEHB33:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE33:
	lea	rcx, 184[rsp]
	call	_ZNSt6localeD1Ev
	mov	r8, QWORD PTR 264[rsp]
	test	r8, r8
	je	.L2253
	mov	rcx, QWORD PTR 224[rsp]
	cmp	rcx, rbp
	je	.L2435
	mov	rax, QWORD PTR 256[rsp]
	lea	r14, 272[rsp]
	cmp	rax, r14
	je	.L2280
	mov	rdx, QWORD PTR 240[rsp]
	movq	xmm0, r8
	mov	QWORD PTR 224[rsp], rax
	movhps	xmm0, QWORD PTR 272[rsp]
	movups	XMMWORD PTR 232[rsp], xmm0
	test	rcx, rcx
	je	.L2259
	mov	QWORD PTR 256[rsp], rcx
	mov	QWORD PTR 272[rsp], rdx
.L2258:
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 256[rsp]
	mov	rdi, QWORD PTR 232[rsp]
	mov	r15, QWORD PTR 224[rsp]
	cmp	rcx, r14
	jne	.L2279
	jmp	.L2260
	.p2align 4,,10
	.p2align 3
.L2151:
	lea	rbp, 240[rsp]
	and	r9d, 32
	mov	QWORD PTR 232[rsp], 0
	mov	QWORD PTR 224[rsp], rbp
	mov	BYTE PTR 240[rsp], 0
	je	.L2251
	fld	TBYTE PTR 48[rsp]
	fabs
	fld	TBYTE PTR .LC33[rip]
	fucomip	st, st(1)
	fstp	st(0)
	jnb	.L2291
.L2251:
	mov	r14, rbx
.L2250:
	movzx	eax, WORD PTR [rsi]
	and	ax, 384
	cmp	ax, 128
	je	.L2436
	cmp	ax, 256
	je	.L2263
.L2266:
	mov	rsi, QWORD PTR 16[r12]
	test	rdi, rdi
	jne	.L2437
.L2271:
	mov	rcx, QWORD PTR 224[rsp]
	cmp	rcx, rbp
	je	.L2274
	mov	rax, QWORD PTR 240[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2274:
	mov	rcx, QWORD PTR 192[rsp]
	cmp	rcx, r13
	je	.L2364
	mov	rax, QWORD PTR 208[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2364:
	mov	rax, rsi
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
.L2424:
	mov	BYTE PTR -1[rbx], 32
	movzx	r9d, BYTE PTR [rsi]
	sub	rbx, 1
	.p2align 4
	.p2align 3
.L2415:
	mov	r11d, 1
	jmp	.L2147
	.p2align 4,,10
	.p2align 3
.L2436:
	movzx	r9d, WORD PTR 4[rsi]
.L2262:
	cmp	rdi, r9
	jnb	.L2266
	movzx	eax, BYTE PTR [rsi]
	mov	rcx, QWORD PTR 16[r12]
	mov	edx, DWORD PTR 8[rsi]
	mov	r8d, eax
	and	r8d, 3
	jne	.L2334
	test	al, 64
	je	.L2336
	fld	TBYTE PTR 48[rsp]
	fabs
	fld	TBYTE PTR .LC33[rip]
	fucomip	st, st(1)
	fstp	st(0)
	jnb	.L2438
.L2336:
	mov	rax, rdi
	mov	r8d, 2
	mov	edx, 32
.L2272:
	mov	DWORD PTR 32[rsp], edx
	sub	r9, rdi
	lea	rdx, 112[rsp]
	mov	QWORD PTR 112[rsp], rax
	mov	QWORD PTR 120[rsp], rbx
.LEHB34:
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi
.LEHE34:
	mov	rsi, rax
	jmp	.L2271
	.p2align 4,,10
	.p2align 3
.L2422:
	mov	rdx, r8
.LEHB35:
	call	_ZNKSt8__format5_SpecIcE16_M_get_precisionISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_
.LEHE35:
	movzx	edx, BYTE PTR 1[rsi]
	mov	QWORD PTR 64[rsp], rax
	lea	rcx, .L2105[rip]
	mov	eax, edx
	shr	al, 3
	and	eax, 15
	movsxd	rax, DWORD PTR [rcx+rax*4]
	add	rax, rcx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2105:
	.long	.L2298-.L2105
	.long	.L2112-.L2105
	.long	.L2111-.L2105
	.long	.L2110-.L2105
	.long	.L2411-.L2105
	.long	.L2108-.L2105
	.long	.L2412-.L2105
	.long	.L2106-.L2105
	.long	.L2413-.L2105
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2334:
	mov	rax, rdi
	jmp	.L2272
	.p2align 4
	.p2align 4,,10
	.p2align 3
.L2439:
	add	r14, 1
	cmp	r14, rdi
	jnb	.L2416
.L2159:
	cmp	BYTE PTR [rbx+r14], 48
	je	.L2439
	jmp	.L2157
	.p2align 4,,10
	.p2align 3
.L2438:
	movzx	eax, BYTE PTR [r14]
	lea	rdx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	cmp	BYTE PTR [rdx+rax], 15
	ja	.L2440
	mov	rax, rdi
	mov	r8d, 2
	mov	edx, 48
	jmp	.L2272
	.p2align 4,,10
	.p2align 3
.L2253:
	mov	rcx, QWORD PTR 256[rsp]
	lea	rax, 272[rsp]
	mov	r15, rbx
	cmp	rcx, rax
	je	.L2260
.L2279:
	mov	rax, QWORD PTR 272[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2260:
	mov	r14, rbx
	mov	rbx, r15
	jmp	.L2250
	.p2align 4,,10
	.p2align 3
.L2312:
	mov	QWORD PTR 88[rsp], 0
.L2152:
	mov	r10, QWORD PTR 88[rsp]
	cmp	BYTE PTR 72[rsp], 0
	je	.L2320
	cmp	QWORD PTR 64[rsp], 0
	je	.L2321
	mov	rax, r10
	mov	r15d, 1
	sub	rax, r11
.L2162:
	sub	QWORD PTR 64[rsp], rax
	add	r15, QWORD PTR 64[rsp]
	jmp	.L2155
	.p2align 4,,10
	.p2align 3
.L2340:
	mov	QWORD PTR 64[rsp], 6
.L2411:
	mov	BYTE PTR 110[rsp], 69
	mov	r14d, 1
.L2109:
	mov	BYTE PTR 72[rsp], 0
	mov	r15d, 1
.L2113:
	mov	edx, DWORD PTR 64[rsp]
	fld	TBYTE PTR 48[rsp]
	mov	DWORD PTR 32[rsp], r15d
	lea	rax, 289[rsp]
	lea	rbx, 160[rsp]
	lea	rdi, 144[rsp]
	mov	QWORD PTR 88[rsp], rax
	mov	DWORD PTR 40[rsp], edx
	mov	r9, rdi
	mov	rdx, rax
	mov	rcx, rbx
	lea	r8, 416[rsp]
	fstp	TBYTE PTR 144[rsp]
	call	_ZSt8to_charsPcS_eSt12chars_formati
	mov	rbp, QWORD PTR 160[rsp]
	cmp	DWORD PTR 168[rsp], 132
	je	.L2290
	lea	rax, 416[rsp]
	mov	rbx, QWORD PTR 88[rsp]
	mov	QWORD PTR 80[rsp], rax
.L2118:
	test	r14b, r14b
	je	.L2120
	cmp	rbx, rbp
	je	.L2120
	mov	rdi, QWORD PTR __imp_toupper[rip]
	mov	r14, rbx
	.p2align 4
	.p2align 3
.L2148:
	movsx	ecx, BYTE PTR [r14]
	add	r14, 1
	call	rdi
	mov	BYTE PTR -1[r14], al
	cmp	r14, rbp
	jne	.L2148
	jmp	.L2120
	.p2align 4,,10
	.p2align 3
.L2341:
	mov	QWORD PTR 64[rsp], 6
.L2108:
	xor	r14d, r14d
.L2107:
	mov	BYTE PTR 110[rsp], 101
	mov	r15d, 2
	mov	BYTE PTR 72[rsp], 0
	jmp	.L2113
	.p2align 4,,10
	.p2align 3
.L2342:
	mov	QWORD PTR 64[rsp], 6
.L2412:
	mov	r14d, 1
	jmp	.L2107
	.p2align 4,,10
	.p2align 3
.L2343:
	mov	QWORD PTR 64[rsp], 6
.L2106:
	mov	BYTE PTR 110[rsp], 101
	xor	r14d, r14d
.L2104:
	mov	BYTE PTR 72[rsp], 1
	mov	r15d, 3
	jmp	.L2113
	.p2align 4,,10
	.p2align 3
.L2344:
	mov	QWORD PTR 64[rsp], 6
.L2413:
	mov	BYTE PTR 110[rsp], 69
	mov	r14d, 1
	jmp	.L2104
	.p2align 4,,10
	.p2align 3
.L2115:
	and	edx, 120
	mov	eax, 112
	cmp	dl, 16
	mov	edx, 101
	cmove	eax, edx
	xor	r14d, r14d
	mov	BYTE PTR 110[rsp], al
.L2116:
	fld	TBYTE PTR 48[rsp]
	mov	DWORD PTR 32[rsp], 4
	lea	rbx, 160[rsp]
	lea	rdi, 144[rsp]
	mov	r9, rdi
	lea	r8, 416[rsp]
	mov	rcx, rbx
	lea	rdx, 289[rsp]
	fstp	TBYTE PTR 144[rsp]
	call	_ZSt8to_charsPcS_eSt12chars_format
	mov	rbp, QWORD PTR 160[rsp]
	cmp	DWORD PTR 168[rsp], 132
	mov	QWORD PTR 64[rsp], 6
	mov	BYTE PTR 72[rsp], 0
	je	.L2304
.L2414:
	lea	rax, 416[rsp]
	lea	rbx, 289[rsp]
	mov	QWORD PTR 80[rsp], rax
	jmp	.L2118
	.p2align 4,,10
	.p2align 3
.L2296:
	and	edx, 120
	mov	eax, 112
	mov	r14d, 1
	cmp	dl, 16
	mov	edx, 80
	cmove	eax, edx
	mov	BYTE PTR 110[rsp], al
	jmp	.L2116
	.p2align 4,,10
	.p2align 3
.L2339:
	mov	QWORD PTR 64[rsp], 6
.L2110:
	mov	BYTE PTR 110[rsp], 101
	xor	r14d, r14d
	jmp	.L2109
	.p2align 4,,10
	.p2align 3
.L2434:
	mov	rcx, r15
	call	_ZNSt6localeC1Ev
	mov	BYTE PTR 32[r12], 1
	jmp	.L2252
	.p2align 4,,10
	.p2align 3
.L2298:
	mov	BYTE PTR 110[rsp], 101
	mov	r15d, 3
	xor	r14d, r14d
	mov	BYTE PTR 72[rsp], 0
	jmp	.L2113
	.p2align 4,,10
	.p2align 3
.L2423:
	mov	BYTE PTR -1[rbx], 43
	mov	r11d, 1
	movzx	r9d, BYTE PTR [rsi]
	sub	rbx, 1
	jmp	.L2147
	.p2align 4,,10
	.p2align 3
.L2263:
	movzx	ecx, WORD PTR 4[rsi]
	mov	rdx, r12
.LEHB36:
	call	_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0
	mov	r9, rax
	jmp	.L2262
	.p2align 4,,10
	.p2align 3
.L2437:
	mov	rcx, QWORD PTR 24[rsi]
	mov	r12, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	r12, rax
	cmp	rdi, r12
	jb	.L2268
	.p2align 4
	.p2align 3
.L2270:
	test	r12, r12
	je	.L2269
	mov	r8, r12
	mov	rdx, rbx
	call	memcpy
.L2269:
	mov	rax, QWORD PTR [rsi]
	add	QWORD PTR 24[rsi], r12
	add	rbx, r12
	sub	rdi, r12
	mov	rcx, rsi
	call	[QWORD PTR [rax]]
.LEHE36:
	mov	rcx, QWORD PTR 24[rsi]
	mov	r12, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	r12, rax
	cmp	rdi, r12
	jnb	.L2270
	test	rdi, rdi
	je	.L2271
.L2268:
	mov	r8, rdi
	mov	rdx, rbx
	call	memcpy
	add	QWORD PTR 24[rsi], rdi
	jmp	.L2271
	.p2align 4,,10
	.p2align 3
.L2425:
	xor	r15d, r15d
	cmp	rdi, rax
	mov	r10, rdi
	sete	r15b
	cmp	BYTE PTR 72[rsp], 0
	jne	.L2441
.L2317:
	mov	QWORD PTR 64[rsp], 0
	jmp	.L2155
	.p2align 4,,10
	.p2align 3
.L2153:
	movsx	edx, BYTE PTR 110[rsp]
	mov	r8, rdi
	mov	rcx, rbx
	mov	BYTE PTR 96[rsp], r9b
	mov	BYTE PTR 88[rsp], r11b
	call	memchr
	movzx	r11d, BYTE PTR 88[rsp]
	movzx	r9d, BYTE PTR 96[rsp]
	test	rax, rax
	je	.L2318
	sub	rax, rbx
	cmp	rax, -1
	cmove	rax, rdi
	mov	QWORD PTR 88[rsp], rax
	jmp	.L2152
	.p2align 4,,10
	.p2align 3
.L2320:
	mov	QWORD PTR 64[rsp], 0
	mov	r15d, 1
	jmp	.L2161
.L2112:
	and	edx, 120
	mov	eax, 101
	cmp	dl, 16
	mov	edx, 112
	cmovne	eax, edx
	xor	r14d, r14d
	mov	BYTE PTR 110[rsp], al
.L2114:
	mov	eax, DWORD PTR 64[rsp]
	fld	TBYTE PTR 48[rsp]
	mov	DWORD PTR 32[rsp], 4
	lea	rbx, 160[rsp]
	lea	rdi, 144[rsp]
	lea	r8, 416[rsp]
	mov	rcx, rbx
	mov	DWORD PTR 40[rsp], eax
	mov	r9, rdi
	lea	rdx, 289[rsp]
	fstp	TBYTE PTR 144[rsp]
	call	_ZSt8to_charsPcS_eSt12chars_formati
	mov	rbp, QWORD PTR 160[rsp]
	cmp	DWORD PTR 168[rsp], 132
	je	.L2294
	mov	BYTE PTR 72[rsp], 0
	jmp	.L2414
	.p2align 4,,10
	.p2align 3
.L2111:
	and	edx, 120
	mov	eax, 112
	mov	r14d, 1
	cmp	dl, 16
	mov	edx, 80
	cmove	eax, edx
	mov	BYTE PTR 110[rsp], al
	jmp	.L2114
.L2441:
	cmp	BYTE PTR [rbx+r11], 48
	jne	.L2156
.L2416:
	mov	r14, -1
.L2157:
	mov	rax, r10
	sub	rax, r14
	jmp	.L2160
.L2318:
	mov	QWORD PTR 88[rsp], rdi
	jmp	.L2152
.L2426:
	cmp	r14, 15
	jbe	.L2170
.L2169:
	movabs	rax, 9223372036854775806
	cmp	rax, r14
	jb	.L2171
	mov	QWORD PTR 80[rsp], r9
	mov	QWORD PTR 72[rsp], r10
	cmp	r14, 29
	ja	.L2172
	mov	ecx, 31
.LEHB37:
	call	_Znwy
	mov	r10, QWORD PTR 72[rsp]
	mov	r9, QWORD PTR 80[rsp]
	mov	rbp, rax
	mov	rdx, r13
	mov	r14d, 30
	jmp	.L2173
.L2428:
	mov	r9, QWORD PTR 200[rsp]
	mov	QWORD PTR 192[rsp], rbp
	mov	QWORD PTR 208[rsp], r14
	test	r9, r9
	jne	.L2168
	.p2align 4
	.p2align 3
.L2170:
	movabs	rax, 9223372036854775806
	cmp	rdi, r10
	mov	rbp, r10
	cmovbe	rbp, rdi
	cmp	rax, rbp
	jb	.L2442
	mov	r15, QWORD PTR 192[rsp]
	cmp	r15, r13
	je	.L2443
	mov	rdx, QWORD PTR 208[rsp]
	cmp	rdx, rbp
	jb	.L2189
.L2186:
	cmp	rbx, r15
	je	.L2190
	test	rbp, rbp
	je	.L2192
	cmp	rbp, 1
	je	.L2444
	mov	rcx, r15
	mov	r8, rbp
	mov	rdx, rbx
	mov	QWORD PTR 72[rsp], r10
	call	memcpy
	mov	r15, QWORD PTR 192[rsp]
	mov	r10, QWORD PTR 72[rsp]
.L2192:
	mov	QWORD PTR 200[rsp], rbp
	mov	BYTE PTR [r15+rbp], 0
	cmp	r10, QWORD PTR 88[rsp]
	je	.L2445
.L2419:
	cmp	QWORD PTR 64[rsp], 0
	je	.L2421
	mov	r8, QWORD PTR 200[rsp]
	movabs	rax, 9223372036854775806
	mov	rdx, rax
	sub	rdx, r8
	cmp	rdx, QWORD PTR 64[rsp]
	jb	.L2446
	mov	rdx, QWORD PTR 64[rsp]
	mov	r14, QWORD PTR 192[rsp]
	lea	rbp, [r8+rdx]
	cmp	r14, r13
	je	.L2447
	mov	r15, QWORD PTR 208[rsp]
	cmp	r15, rbp
	jb	.L2448
.L2208:
	lea	rcx, [r14+r8]
	cmp	QWORD PTR 64[rsp], 1
	je	.L2449
	mov	r8, QWORD PTR 64[rsp]
	mov	edx, 48
	mov	QWORD PTR 72[rsp], r10
	call	memset
	mov	r10, QWORD PTR 72[rsp]
.L2221:
	mov	rax, QWORD PTR 192[rsp]
	mov	QWORD PTR 200[rsp], rbp
	mov	BYTE PTR [rax+rbp], 0
.L2421:
	cmp	rdi, r10
	jb	.L2450
	mov	rdx, QWORD PTR 200[rsp]
	sub	rdi, r10
	lea	r9, [rbx+r10]
	movabs	rax, 9223372036854775806
	sub	rax, rdx
	cmp	rax, rdi
	jb	.L2451
	mov	rax, QWORD PTR 192[rsp]
	mov	ecx, 15
	lea	rbx, [rdi+rdx]
	cmp	rax, r13
	cmovne	rcx, QWORD PTR 208[rsp]
	cmp	rcx, rbx
	jb	.L2225
	test	rdi, rdi
	je	.L2226
	lea	rcx, [rax+rdx]
	cmp	rdi, 1
	je	.L2452
	mov	r8, rdi
	mov	rdx, r9
	call	memcpy
	mov	rax, QWORD PTR 192[rsp]
.L2226:
	mov	QWORD PTR 200[rsp], rbx
	mov	BYTE PTR [rax+rbx], 0
	jmp	.L2228
	.p2align 4,,10
	.p2align 3
.L2163:
	mov	rdx, QWORD PTR 192[rsp]
	cmp	rdx, r13
	je	.L2453
	mov	rax, QWORD PTR 208[rsp]
	cmp	rax, r14
	jnb	.L2168
	jmp	.L2174
.L2440:
	mov	rax, QWORD PTR 24[rcx]
	movzx	edx, BYTE PTR [rbx]
	lea	r8, 1[rax]
	mov	QWORD PTR 24[rcx], r8
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[rcx]
	sub	rax, QWORD PTR 8[rcx]
	cmp	rax, QWORD PTR 16[rcx]
	je	.L2454
.L2273:
	add	rbx, 1
	lea	rax, -1[rdi]
	mov	r8d, 2
	mov	edx, 48
	jmp	.L2272
.L2305:
	mov	BYTE PTR 72[rsp], 0
	xor	r14d, r14d
	xor	r15d, r15d
	mov	ebp, 14
	mov	BYTE PTR 110[rsp], 101
	mov	BYTE PTR 80[rsp], 0
.L2117:
	mov	r10, QWORD PTR 192[rsp]
	cmp	rbp, 128
	jbe	.L2455
	cmp	r10, r13
	je	.L2456
	mov	rax, QWORD PTR 208[rsp]
	cmp	rax, rbp
	jb	.L2457
.L2289:
	cmp	r10, r13
	je	.L2309
	mov	rax, QWORD PTR 208[rsp]
	lea	rbp, [rax+rax]
	cmp	rax, rbp
	jnb	.L2136
	movabs	rax, 9223372036854775806
	cmp	rax, rbp
	jb	.L2458
	lea	rcx, 1[rbp]
.L2135:
	mov	QWORD PTR 88[rsp], r10
	call	_Znwy
	mov	r9, rax
	mov	rax, QWORD PTR 200[rsp]
	mov	r10, QWORD PTR 88[rsp]
	test	rax, rax
	lea	r8, 1[rax]
	je	.L2459
	mov	rcx, r9
	mov	rdx, r10
	call	memcpy
	mov	r9, rax
.L2139:
	mov	rcx, QWORD PTR 192[rsp]
	cmp	rcx, r13
	je	.L2140
	mov	rax, QWORD PTR 208[rsp]
	mov	QWORD PTR 88[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 88[rsp]
.L2140:
	mov	QWORD PTR 192[rsp], r9
	mov	r10, r9
	mov	QWORD PTR 208[rsp], rbp
.L2136:
	fld	TBYTE PTR 48[rsp]
	cmp	BYTE PTR 80[rsp], 0
	mov	QWORD PTR 88[rsp], r10
	lea	r8, -1[r10+rbp]
	lea	rdx, 1[r10]
	fstp	TBYTE PTR 144[rsp]
	jne	.L2460
	test	r15d, r15d
	je	.L2143
	mov	DWORD PTR 32[rsp], r15d
	mov	r9, rdi
	mov	rcx, rbx
	call	_ZSt8to_charsPcS_eSt12chars_format
	mov	rbp, QWORD PTR 160[rsp]
	mov	r10, QWORD PTR 88[rsp]
	mov	rax, QWORD PTR 168[rsp]
.L2142:
	test	eax, eax
	jne	.L2144
	mov	rdx, QWORD PTR 192[rsp]
	mov	rax, rbp
	sub	rax, r10
	mov	QWORD PTR 200[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rax, QWORD PTR 192[rsp]
	lea	rbx, 1[rax]
	add	rax, QWORD PTR 200[rsp]
	mov	QWORD PTR 80[rsp], rax
	jmp	.L2118
	.p2align 4,,10
	.p2align 3
.L2144:
	mov	rdx, QWORD PTR 192[rsp]
	mov	QWORD PTR 200[rsp], 0
	mov	BYTE PTR [rdx], 0
	mov	r10, QWORD PTR 192[rsp]
	cmp	eax, 132
	je	.L2289
	lea	rbx, 1[r10]
	add	r10, QWORD PTR 200[rsp]
	mov	QWORD PTR 80[rsp], r10
	jmp	.L2118
.L2143:
	mov	r9, rdi
	mov	rcx, rbx
	call	_ZSt8to_charsPcS_e
	mov	rbp, QWORD PTR 160[rsp]
	mov	r10, QWORD PTR 88[rsp]
	mov	rax, QWORD PTR 168[rsp]
	jmp	.L2142
.L2304:
	mov	BYTE PTR 80[rsp], 0
	mov	r15d, 4
	mov	ebp, 14
	jmp	.L2117
.L2290:
	mov	rax, QWORD PTR 64[rsp]
	mov	BYTE PTR 80[rsp], 1
	lea	rbp, 8[rax]
	cmp	r15d, 2
	jne	.L2117
	fld	TBYTE PTR 48[rsp]
	lea	rdx, 128[rsp]
	lea	r8, 256[rsp]
	mov	rcx, rdi
	mov	DWORD PTR 256[rsp], 0
	fstp	TBYTE PTR 128[rsp]
	call	frexpl
	mov	eax, DWORD PTR 256[rsp]
	test	eax, eax
	jle	.L2121
	imul	edx, eax, 4004
	mov	rax, rdx
	imul	rdx, rdx, 995517945
	shr	rdx, 32
	sub	eax, edx
	shr	eax
	add	eax, edx
	shr	eax, 13
	add	eax, 1
	add	rbp, rax
.L2121:
	mov	BYTE PTR 80[rsp], 1
	jmp	.L2117
.L2460:
	mov	eax, DWORD PTR 64[rsp]
	mov	DWORD PTR 32[rsp], r15d
	mov	r9, rdi
	mov	rcx, rbx
	mov	DWORD PTR 40[rsp], eax
	call	_ZSt8to_charsPcS_eSt12chars_formati
	mov	rbp, QWORD PTR 160[rsp]
	mov	r10, QWORD PTR 88[rsp]
	mov	rax, QWORD PTR 168[rsp]
	jmp	.L2142
.L2457:
	movabs	rcx, 9223372036854775806
	cmp	rcx, rbp
	jb	.L2126
	add	rax, rax
	cmp	rbp, rax
	jnb	.L2293
	cmp	rcx, rax
	jnb	.L2292
	mov	rbp, rcx
	mov	rdx, r10
	movabs	rcx, 9223372036854775807
.L2131:
	mov	QWORD PTR 88[rsp], rdx
	call	_Znwy
	mov	r10, rax
	mov	rax, QWORD PTR 200[rsp]
	mov	rdx, QWORD PTR 88[rsp]
	test	rax, rax
	lea	r8, 1[rax]
	je	.L2461
	mov	rcx, r10
	call	memcpy
	mov	r10, rax
.L2133:
	mov	rcx, QWORD PTR 192[rsp]
	cmp	rcx, r13
	je	.L2134
	mov	rax, QWORD PTR 208[rsp]
	mov	QWORD PTR 88[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 88[rsp]
.L2134:
	mov	QWORD PTR 192[rsp], r10
	mov	QWORD PTR 208[rsp], rbp
	jmp	.L2289
.L2164:
	lea	rbp, [rbx+r10]
	lea	rcx, [r10+r15]
	sub	rdi, r10
	mov	QWORD PTR 72[rsp], r10
	add	rcx, rbx
	mov	r8, rdi
	mov	rdx, rbp
	call	memmove
	mov	r10, QWORD PTR 72[rsp]
	cmp	r10, QWORD PTR 88[rsp]
	jne	.L2182
	mov	BYTE PTR 0[rbp], 46
	lea	rbp, 1[rbx+r10]
.L2182:
	mov	r8, QWORD PTR 64[rsp]
	mov	edx, 48
	mov	rcx, rbp
	mov	rdi, r14
	call	memset
	jmp	.L2183
.L2435:
	mov	rax, QWORD PTR 256[rsp]
	lea	r14, 272[rsp]
	cmp	rax, r14
	je	.L2280
	mov	QWORD PTR 224[rsp], rax
	movq	xmm0, r8
	movhps	xmm0, QWORD PTR 272[rsp]
	movups	XMMWORD PTR 232[rsp], xmm0
.L2259:
	mov	QWORD PTR 256[rsp], r14
	lea	r14, 272[rsp]
	mov	rcx, r14
	jmp	.L2258
.L2321:
	mov	r15d, 1
	jmp	.L2161
.L2315:
	mov	r10, rdi
	jmp	.L2158
.L2309:
	mov	ecx, 31
	mov	ebp, 30
	jmp	.L2135
.L2456:
	movabs	rax, 9223372036854775806
	cmp	rax, rbp
	jb	.L2126
	lea	rcx, 1[rbp]
	mov	rdx, r13
	jmp	.L2131
.L2459:
	movzx	eax, BYTE PTR [r10]
	mov	BYTE PTR [r9], al
	jmp	.L2139
.L2461:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [r10], al
	jmp	.L2133
.L2236:
	sub	r9, r10
	mov	QWORD PTR 64[rsp], r9
	cmp	rax, rdi
	jb	.L2233
	add	rbx, rbx
	cmp	rdi, rbx
	jb	.L2240
.L2235:
	lea	rcx, 1[rdi]
	mov	rbx, rdi
.L2241:
	mov	QWORD PTR 72[rsp], r10
	call	_Znwy
	mov	r10, QWORD PTR 72[rsp]
	mov	r14, rax
	test	r10, r10
	je	.L2242
	cmp	r10, 1
	je	.L2462
	mov	r8, r10
	mov	rdx, rbp
	mov	rcx, rax
	mov	QWORD PTR 72[rsp], r10
	call	memcpy
	mov	rbp, QWORD PTR 192[rsp]
	mov	r10, QWORD PTR 72[rsp]
.L2242:
	mov	rax, QWORD PTR 64[rsp]
	test	rax, rax
	je	.L2244
	lea	rcx, [r10+r15]
	lea	rdx, 0[rbp+r10]
	add	rcx, r14
	cmp	rax, 1
	je	.L2463
	mov	r8, QWORD PTR 64[rsp]
	mov	QWORD PTR 72[rsp], r10
	call	memcpy
	mov	rbp, QWORD PTR 192[rsp]
	mov	r10, QWORD PTR 72[rsp]
.L2244:
	cmp	rbp, r13
	je	.L2246
	mov	rax, QWORD PTR 208[rsp]
	mov	rcx, rbp
	mov	QWORD PTR 64[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 64[rsp]
.L2246:
	mov	QWORD PTR 192[rsp], r14
	lea	rcx, [r14+r10]
	mov	QWORD PTR 208[rsp], rbx
	jmp	.L2237
.L2427:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR 0[rbp], al
	jmp	.L2180
.L2225:
	mov	QWORD PTR 32[rsp], rdi
	lea	rcx, 192[rsp]
	xor	r8d, r8d
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rax, QWORD PTR 192[rsp]
	jmp	.L2226
.L2455:
	cmp	r10, r13
	je	.L2464
	mov	rax, QWORD PTR 208[rsp]
	cmp	rax, 255
	ja	.L2289
	add	rax, rax
	cmp	rax, 256
	jbe	.L2465
.L2292:
	lea	rcx, 1[rax]
	mov	rdx, r10
	mov	rbp, rax
	jmp	.L2131
.L2280:
	cmp	r8, 1
	je	.L2466
	mov	rdx, r14
	call	memcpy
.L2257:
	mov	rax, QWORD PTR 264[rsp]
	mov	rdx, QWORD PTR 224[rsp]
	mov	QWORD PTR 232[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rcx, QWORD PTR 256[rsp]
	jmp	.L2258
.L2445:
	mov	rbp, QWORD PTR 200[rsp]
	mov	rdx, QWORD PTR 192[rsp]
	lea	r15, 1[rbp]
	cmp	rdx, r13
	je	.L2467
	mov	r14, QWORD PTR 208[rsp]
	cmp	r14, r15
	jb	.L2468
.L2200:
	mov	BYTE PTR [rdx+rbp], 46
	mov	rax, QWORD PTR 192[rsp]
	mov	QWORD PTR 200[rsp], r15
	mov	BYTE PTR 1[rax+rbp], 0
	jmp	.L2419
.L2431:
	cmp	rdi, 15
	jbe	.L2232
	sub	r9, r10
	mov	QWORD PTR 64[rsp], r9
	cmp	rax, rdi
	jb	.L2233
	cmp	rdi, 29
	ja	.L2235
	mov	ebx, 30
.L2234:
	lea	rcx, 1[rbx]
	jmp	.L2241
.L2443:
	cmp	rbp, 15
	jbe	.L2186
	cmp	rbp, 29
	ja	.L2188
	mov	r14d, 30
.L2187:
	lea	rcx, 1[r14]
.L2195:
	mov	QWORD PTR 72[rsp], r10
	call	_Znwy
	mov	rcx, rax
	mov	r8, rbp
	mov	rdx, rbx
	mov	r15, rax
	call	memcpy
	mov	rcx, QWORD PTR 192[rsp]
	mov	r10, QWORD PTR 72[rsp]
	cmp	rcx, r13
	je	.L2196
	mov	rax, QWORD PTR 208[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 72[rsp]
.L2196:
	mov	QWORD PTR 192[rsp], r15
	mov	QWORD PTR 208[rsp], r14
	jmp	.L2192
.L2433:
	mov	BYTE PTR [rcx], 48
	jmp	.L2248
.L2453:
	cmp	r14, 15
	jbe	.L2168
	jmp	.L2169
.L2189:
	lea	r14, [rdx+rdx]
	cmp	rbp, r14
	jb	.L2194
.L2188:
	lea	rcx, 1[rbp]
	mov	r14, rbp
	jmp	.L2195
.L2448:
	cmp	rax, rbp
	jb	.L2209
	add	r15, r15
	cmp	rbp, r15
	jb	.L2213
.L2211:
	lea	rcx, 1[rbp]
	mov	r15, rbp
.L2214:
	mov	QWORD PTR 80[rsp], r10
	mov	QWORD PTR 72[rsp], r8
	call	_Znwy
	mov	r8, QWORD PTR 72[rsp]
	mov	r10, QWORD PTR 80[rsp]
	mov	r9, rax
	test	r8, r8
	je	.L2418
	cmp	r8, 1
	je	.L2469
	mov	rdx, r14
	mov	rcx, rax
	mov	QWORD PTR 80[rsp], r10
	mov	QWORD PTR 72[rsp], r8
	call	memcpy
	mov	r10, QWORD PTR 80[rsp]
	mov	r8, QWORD PTR 72[rsp]
	mov	r9, rax
.L2217:
	mov	r14, QWORD PTR 192[rsp]
.L2418:
	cmp	r14, r13
	je	.L2219
	mov	rax, QWORD PTR 208[rsp]
	mov	rcx, r14
	mov	QWORD PTR 88[rsp], r9
	mov	QWORD PTR 80[rsp], r10
	lea	rdx, 1[rax]
	mov	QWORD PTR 72[rsp], r8
	call	_ZdlPvy
	mov	r9, QWORD PTR 88[rsp]
	mov	r10, QWORD PTR 80[rsp]
	mov	r8, QWORD PTR 72[rsp]
.L2219:
	mov	QWORD PTR 192[rsp], r9
	mov	r14, r9
	mov	QWORD PTR 208[rsp], r15
	jmp	.L2208
.L2444:
	movzx	eax, BYTE PTR [rbx]
	mov	BYTE PTR [r15], al
	mov	r15, QWORD PTR 192[rsp]
	jmp	.L2192
.L2432:
	movzx	edx, BYTE PTR [rcx]
	mov	BYTE PTR [rcx+r15], dl
	mov	rcx, QWORD PTR 192[rsp]
	add	rcx, r10
	jmp	.L2237
.L2452:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	mov	rax, QWORD PTR 192[rsp]
	jmp	.L2226
.L2172:
	lea	rcx, 1[r14]
	call	_Znwy
.LEHE37:
	mov	r10, QWORD PTR 72[rsp]
	mov	r9, QWORD PTR 80[rsp]
	mov	rbp, rax
	mov	rdx, r13
	jmp	.L2173
.L2447:
	cmp	rbp, 15
	jbe	.L2208
	cmp	rax, rbp
	jb	.L2209
	cmp	rbp, 29
	ja	.L2211
	mov	r15d, 30
.L2210:
	lea	rcx, 1[r15]
	jmp	.L2214
.L2194:
	cmp	rax, r14
	jnb	.L2187
	movabs	rcx, 9223372036854775807
	mov	r14, rax
	jmp	.L2195
.L2449:
	mov	BYTE PTR [rcx], 48
	jmp	.L2221
.L2454:
	mov	rax, QWORD PTR [rcx]
	mov	QWORD PTR 64[rsp], r9
	mov	QWORD PTR 48[rsp], rcx
.LEHB38:
	call	[QWORD PTR [rax]]
.LEHE38:
	mov	r9, QWORD PTR 64[rsp]
	mov	rcx, QWORD PTR 48[rsp]
	jmp	.L2273
.L2240:
	cmp	rax, rbx
	jnb	.L2234
	movabs	rcx, 9223372036854775807
	mov	rbx, rax
	jmp	.L2241
.L2466:
	movzx	eax, BYTE PTR 272[rsp]
	mov	BYTE PTR [rcx], al
	jmp	.L2257
.L2462:
	movzx	eax, BYTE PTR 0[rbp]
	mov	BYTE PTR [r14], al
	mov	rbp, QWORD PTR 192[rsp]
	jmp	.L2242
.L2463:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rcx], al
	mov	rbp, QWORD PTR 192[rsp]
	jmp	.L2244
.L2468:
	movabs	rcx, 9223372036854775807
	cmp	r15, rcx
	je	.L2470
	add	r14, r14
	cmp	r15, r14
	jb	.L2202
	lea	rcx, 2[rbp]
	mov	r14, r15
.L2203:
	mov	QWORD PTR 88[rsp], rdx
	mov	QWORD PTR 80[rsp], r10
.LEHB39:
	call	_Znwy
	mov	rdx, QWORD PTR 88[rsp]
	mov	rcx, rax
	mov	r8, rbp
	mov	QWORD PTR 72[rsp], rax
	call	memcpy
	mov	rcx, QWORD PTR 192[rsp]
	mov	r10, QWORD PTR 80[rsp]
	cmp	rcx, r13
	je	.L2204
	mov	rax, QWORD PTR 208[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 80[rsp]
.L2204:
	mov	rax, QWORD PTR 72[rsp]
	mov	QWORD PTR 208[rsp], r14
	mov	QWORD PTR 192[rsp], rax
	mov	rdx, rax
	jmp	.L2200
.L2464:
	mov	ecx, 257
	mov	rdx, r13
	mov	ebp, 256
	jmp	.L2131
.L2467:
	cmp	r15, 16
	jne	.L2200
	mov	r14d, 30
.L2199:
	lea	rcx, 1[r14]
	jmp	.L2203
.L2213:
	cmp	rax, r15
	jnb	.L2210
	movabs	rcx, 9223372036854775807
	mov	r15, rax
	jmp	.L2214
.L2469:
	movzx	eax, BYTE PTR [r14]
	mov	BYTE PTR [r9], al
	jmp	.L2217
.L2202:
	movabs	rax, 9223372036854775806
	cmp	rax, r14
	jnb	.L2199
	mov	r14, rax
	jmp	.L2203
.L2294:
	mov	rax, QWORD PTR 64[rsp]
	mov	BYTE PTR 72[rsp], 0
	mov	r15d, 4
	mov	BYTE PTR 80[rsp], 1
	lea	rbp, 8[rax]
	jmp	.L2117
.L2465:
	mov	ebp, 256
.L2293:
	lea	rcx, 1[rbp]
	mov	rdx, r10
	jmp	.L2131
.L2126:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2233:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2190:
	xor	eax, eax
	mov	QWORD PTR 32[rsp], rbp
	mov	r9, rbx
	xor	r8d, r8d
	mov	QWORD PTR 40[rsp], rax
	lea	rcx, 192[rsp]
	mov	rdx, rbx
	mov	QWORD PTR 72[rsp], r10
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	r10, QWORD PTR 72[rsp]
	mov	r15, QWORD PTR 192[rsp]
	jmp	.L2192
.L2103:
.L2348:
	mov	rbx, rax
	jmp	.L2277
.L2429:
	mov	r8, r10
	lea	rdx, .LC37[rip]
	lea	rcx, .LC38[rip]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.LEHE39:
.L2346:
	mov	rbx, rax
	jmp	.L2278
.L2347:
	mov	rbx, rax
.L2276:
	lea	rcx, 184[rsp]
	call	_ZNSt6localeD1Ev
.L2277:
	lea	rcx, 224[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L2278:
	lea	rcx, 192[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB40:
	call	_Unwind_Resume
.LEHE40:
.L2430:
	lea	rcx, .LC20[rip]
.LEHB41:
	call	_ZSt20__throw_length_errorPKc
.L2470:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2209:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2442:
	lea	rcx, .LC34[rip]
	call	_ZSt20__throw_length_errorPKc
.L2451:
	lea	rcx, .LC14[rip]
	call	_ZSt20__throw_length_errorPKc
.L2446:
	lea	rcx, .LC20[rip]
	call	_ZSt20__throw_length_errorPKc
.L2458:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2450:
	mov	r9, rdi
	mov	r8, r10
	lea	rdx, .LC35[rip]
	lea	rcx, .LC36[rip]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L2171:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
.LEHE41:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5612:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5612-.LLSDACSB5612
.LLSDACSB5612:
	.uleb128 .LEHB32-.LFB5612
	.uleb128 .LEHE32-.LEHB32
	.uleb128 .L2346-.LFB5612
	.uleb128 0
	.uleb128 .LEHB33-.LFB5612
	.uleb128 .LEHE33-.LEHB33
	.uleb128 .L2347-.LFB5612
	.uleb128 0
	.uleb128 .LEHB34-.LFB5612
	.uleb128 .LEHE34-.LEHB34
	.uleb128 .L2348-.LFB5612
	.uleb128 0
	.uleb128 .LEHB35-.LFB5612
	.uleb128 .LEHE35-.LEHB35
	.uleb128 .L2346-.LFB5612
	.uleb128 0
	.uleb128 .LEHB36-.LFB5612
	.uleb128 .LEHE36-.LEHB36
	.uleb128 .L2348-.LFB5612
	.uleb128 0
	.uleb128 .LEHB37-.LFB5612
	.uleb128 .LEHE37-.LEHB37
	.uleb128 .L2346-.LFB5612
	.uleb128 0
	.uleb128 .LEHB38-.LFB5612
	.uleb128 .LEHE38-.LEHB38
	.uleb128 .L2348-.LFB5612
	.uleb128 0
	.uleb128 .LEHB39-.LFB5612
	.uleb128 .LEHE39-.LEHB39
	.uleb128 .L2346-.LFB5612
	.uleb128 0
	.uleb128 .LEHB40-.LFB5612
	.uleb128 .LEHE40-.LEHB40
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB41-.LFB5612
	.uleb128 .LEHE41-.LEHB41
	.uleb128 .L2346-.LFB5612
	.uleb128 0
.LLSDACSE5612:
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
.LFB5609:
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
	sub	rsp, 392
	.seh_stackalloc	392
	movaps	XMMWORD PTR 368[rsp], xmm6
	.seh_savexmm	xmm6, 368
	.seh_endprologue
	mov	BYTE PTR 160[rsp], 0
	movzx	edx, BYTE PTR 1[rcx]
	mov	rbx, rcx
	movapd	xmm6, xmm1
	lea	rdi, 160[rsp]
	mov	rsi, r8
	mov	QWORD PTR 152[rsp], 0
	mov	QWORD PTR 144[rsp], rdi
	test	dl, 6
	jne	.L2792
	mov	eax, edx
	shr	al, 3
	and	eax, 15
	cmp	al, 8
	ja	.L2473
	lea	rcx, .L2665[rip]
	movzx	eax, al
	movsxd	rax, DWORD PTR [rcx+rax*4]
	add	rax, rcx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2665:
	.long	.L2489-.L2665
	.long	.L2485-.L2665
	.long	.L2666-.L2665
	.long	.L2709-.L2665
	.long	.L2710-.L2665
	.long	.L2711-.L2665
	.long	.L2712-.L2665
	.long	.L2713-.L2665
	.long	.L2714-.L2665
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2489:
	lea	r12, 112[rsp]
	movapd	xmm3, xmm6
	lea	r8, 368[rsp]
	mov	ebp, 6
	lea	rdx, 241[rsp]
	mov	rcx, r12
	call	_ZSt8to_charsPcS_d
	mov	r14, QWORD PTR 112[rsp]
	cmp	DWORD PTR 120[rsp], 132
	je	.L2675
	lea	rax, 368[rsp]
	mov	BYTE PTR 48[rsp], 0
	lea	r12, 241[rsp]
	mov	BYTE PTR 56[rsp], 101
	mov	QWORD PTR 64[rsp], rax
.L2490:
	movmskpd	eax, xmm6
	movzx	r15d, BYTE PTR [rbx]
	test	al, 1
	jne	.L2785
	mov	eax, r15d
	and	eax, 12
	cmp	al, 4
	je	.L2793
	xor	r11d, r11d
	cmp	al, 12
	je	.L2794
.L2517:
	mov	r13, r14
	sub	r13, r12
	test	r15b, 16
	je	.L2521
	movsd	xmm1, QWORD PTR .LC41[rip]
	movapd	xmm0, xmm6
	andpd	xmm0, XMMWORD PTR .LC40[rip]
	ucomisd	xmm1, xmm0
	jb	.L2521
	test	r13, r13
	je	.L2682
	mov	r8, r13
	mov	edx, 46
	mov	rcx, r12
	mov	BYTE PTR 72[rsp], r11b
	call	memchr
	movzx	r11d, BYTE PTR 72[rsp]
	test	rax, rax
	je	.L2523
	sub	rax, r12
	mov	QWORD PTR 80[rsp], rax
	cmp	rax, -1
	je	.L2523
	lea	r9, 1[rax]
	cmp	r9, r13
	jnb	.L2795
	movsx	edx, BYTE PTR 56[rsp]
	mov	r8, r13
	lea	rcx, [r12+r9]
	mov	BYTE PTR 88[rsp], r11b
	sub	r8, r9
	mov	QWORD PTR 72[rsp], r9
	call	memchr
	mov	r9, QWORD PTR 72[rsp]
	movzx	r11d, BYTE PTR 88[rsp]
	test	rax, rax
	je	.L2685
	sub	rax, r12
	mov	r10, rax
	cmp	rax, -1
	cmove	r10, r13
.L2528:
	xor	eax, eax
	cmp	r10, QWORD PTR 80[rsp]
	sete	al
	mov	QWORD PTR 72[rsp], rax
	cmp	BYTE PTR 48[rsp], 0
	je	.L2687
	cmp	BYTE PTR [r12+r11], 48
	je	.L2529
.L2526:
	mov	rax, r10
	sub	rax, r11
	sub	rax, 1
.L2530:
	test	rbp, rbp
	jne	.L2532
	.p2align 4
	.p2align 3
.L2525:
	cmp	QWORD PTR 72[rsp], 0
	je	.L2521
.L2531:
	mov	rdx, QWORD PTR 72[rsp]
	mov	r9, QWORD PTR 152[rsp]
	lea	r15, 0[r13+rdx]
	test	r9, r9
	jne	.L2533
	mov	rax, QWORD PTR 64[rsp]
	sub	rax, r14
	cmp	rax, rdx
	jnb	.L2534
	mov	rdx, QWORD PTR 144[rsp]
	cmp	rdx, rdi
	je	.L2796
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, r15
	jnb	.L2540
.L2544:
	movabs	r8, 9223372036854775806
	cmp	r8, r15
	jb	.L2541
	add	rax, rax
	lea	rcx, 1[r15]
	cmp	r15, rax
	jnb	.L2548
	cmp	r8, rax
	lea	r11, 1[rax]
	movabs	rcx, 9223372036854775807
	cmovb	rax, r8
	cmovnb	rcx, r11
	mov	r15, rax
.L2548:
	mov	QWORD PTR 88[rsp], r9
	mov	QWORD PTR 64[rsp], rdx
	mov	QWORD PTR 48[rsp], r10
.LEHB42:
	call	_Znwy
.LEHE42:
	mov	r9, QWORD PTR 88[rsp]
	mov	rdx, QWORD PTR 64[rsp]
	mov	r14, rax
	mov	r10, QWORD PTR 48[rsp]
.L2543:
	lea	r8, 1[r9]
	test	r9, r9
	je	.L2797
	mov	rcx, r14
	mov	QWORD PTR 48[rsp], r10
	call	memcpy
	mov	r10, QWORD PTR 48[rsp]
.L2550:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rdi
	je	.L2798
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 48[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 152[rsp]
	mov	r10, QWORD PTR 48[rsp]
	mov	QWORD PTR 144[rsp], r14
	mov	QWORD PTR 160[rsp], r15
	test	r9, r9
	je	.L2540
.L2538:
	cmp	r9, r10
	jb	.L2799
	movabs	rax, 9223372036854775806
	mov	rdx, rax
	sub	rdx, r9
	cmp	rdx, QWORD PTR 72[rsp]
	jb	.L2800
	mov	rdx, QWORD PTR 72[rsp]
	mov	r14, QWORD PTR 144[rsp]
	lea	r13, [r9+rdx]
	cmp	r14, rdi
	je	.L2801
	mov	r12, QWORD PTR 160[rsp]
	cmp	r12, r13
	jb	.L2606
.L2602:
	lea	rcx, [r14+r10]
	sub	r9, r10
	je	.L2607
	mov	rax, QWORD PTR 72[rsp]
	add	rax, rcx
	cmp	r9, 1
	je	.L2802
	mov	rdx, rcx
	mov	r8, r9
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], r10
	call	memmove
	mov	r10, QWORD PTR 48[rsp]
	mov	rcx, QWORD PTR 144[rsp]
	add	rcx, r10
.L2607:
	cmp	QWORD PTR 72[rsp], 1
	je	.L2803
	mov	r8, QWORD PTR 72[rsp]
	mov	edx, 48
	mov	QWORD PTR 48[rsp], r10
	call	memset
	mov	r10, QWORD PTR 48[rsp]
.L2618:
	mov	rax, QWORD PTR 144[rsp]
	mov	QWORD PTR 152[rsp], r13
	mov	BYTE PTR [rax+r13], 0
	cmp	r10, QWORD PTR 80[rsp]
	jne	.L2598
	mov	rax, QWORD PTR 144[rsp]
	mov	BYTE PTR [rax+r10], 46
	.p2align 4
	.p2align 3
.L2598:
	mov	r13, QWORD PTR 152[rsp]
	mov	r12, QWORD PTR 144[rsp]
.L2553:
	lea	rbp, 192[rsp]
	mov	BYTE PTR 192[rsp], 0
	mov	QWORD PTR 176[rsp], rbp
	mov	QWORD PTR 184[rsp], 0
	test	BYTE PTR [rbx], 32
	je	.L2621
.L2661:
	lea	r15, 24[rsi]
	cmp	BYTE PTR 32[rsi], 0
	je	.L2804
.L2622:
	mov	rdx, r15
	lea	rcx, 136[rsp]
	call	_ZNSt6localeC1ERKS_
	movzx	r8d, BYTE PTR 56[rsp]
	lea	rcx, 208[rsp]
	lea	rdx, 96[rsp]
	lea	r9, 136[rsp]
	mov	QWORD PTR 96[rsp], r13
	mov	QWORD PTR 104[rsp], r12
.LEHB43:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE43:
	lea	rcx, 136[rsp]
	call	_ZNSt6localeD1Ev
	mov	r8, QWORD PTR 216[rsp]
	test	r8, r8
	je	.L2623
	mov	rcx, QWORD PTR 176[rsp]
	cmp	rcx, rbp
	je	.L2805
	mov	rax, QWORD PTR 208[rsp]
	lea	r14, 224[rsp]
	cmp	rax, r14
	je	.L2650
	mov	rdx, QWORD PTR 192[rsp]
	movq	xmm0, r8
	mov	QWORD PTR 176[rsp], rax
	movhps	xmm0, QWORD PTR 224[rsp]
	movups	XMMWORD PTR 184[rsp], xmm0
	test	rcx, rcx
	je	.L2629
	mov	QWORD PTR 208[rsp], rcx
	mov	QWORD PTR 224[rsp], rdx
.L2628:
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 208[rsp]
	mov	r13, QWORD PTR 184[rsp]
	mov	r15, QWORD PTR 176[rsp]
	cmp	rcx, r14
	jne	.L2649
	jmp	.L2630
	.p2align 4,,10
	.p2align 3
.L2521:
	lea	rbp, 192[rsp]
	and	r15d, 32
	mov	QWORD PTR 184[rsp], 0
	mov	QWORD PTR 176[rsp], rbp
	mov	BYTE PTR 192[rsp], 0
	je	.L2621
	movsd	xmm1, QWORD PTR .LC41[rip]
	movapd	xmm0, xmm6
	andpd	xmm0, XMMWORD PTR .LC40[rip]
	ucomisd	xmm1, xmm0
	jnb	.L2661
.L2621:
	mov	r14, r12
.L2620:
	movzx	eax, WORD PTR [rbx]
	and	ax, 384
	cmp	ax, 128
	je	.L2806
	cmp	ax, 256
	je	.L2633
.L2636:
	mov	rbx, QWORD PTR 16[rsi]
	test	r13, r13
	jne	.L2807
.L2641:
	mov	rcx, QWORD PTR 176[rsp]
	cmp	rcx, rbp
	je	.L2644
	mov	rax, QWORD PTR 192[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2644:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rdi
	je	.L2734
	mov	rax, QWORD PTR 160[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	nop
.L2734:
	movaps	xmm6, XMMWORD PTR 368[rsp]
	mov	rax, rbx
	add	rsp, 392
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
.L2794:
	mov	BYTE PTR -1[r12], 32
	movzx	r15d, BYTE PTR [rbx]
	sub	r12, 1
	.p2align 4
	.p2align 3
.L2785:
	mov	r11d, 1
	jmp	.L2517
	.p2align 4,,10
	.p2align 3
.L2806:
	movzx	r9d, WORD PTR 4[rbx]
.L2632:
	cmp	r13, r9
	jnb	.L2636
	movzx	eax, BYTE PTR [rbx]
	mov	rcx, QWORD PTR 16[rsi]
	mov	edx, DWORD PTR 8[rbx]
	mov	r8d, eax
	and	r8d, 3
	jne	.L2704
	test	al, 64
	je	.L2706
	andpd	xmm6, XMMWORD PTR .LC40[rip]
	movsd	xmm0, QWORD PTR .LC41[rip]
	ucomisd	xmm0, xmm6
	jnb	.L2808
.L2706:
	mov	rax, r13
	mov	r8d, 2
	mov	edx, 32
.L2642:
	mov	DWORD PTR 32[rsp], edx
	sub	r9, r13
	lea	rdx, 96[rsp]
	mov	QWORD PTR 96[rsp], rax
	mov	QWORD PTR 104[rsp], r12
.LEHB44:
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi
.LEHE44:
	mov	rbx, rax
	jmp	.L2641
	.p2align 4,,10
	.p2align 3
.L2792:
	mov	rdx, r8
.LEHB45:
	call	_ZNKSt8__format5_SpecIcE16_M_get_precisionISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_
.LEHE45:
	movzx	edx, BYTE PTR 1[rbx]
	mov	rbp, rax
	lea	rcx, .L2475[rip]
	mov	eax, edx
	shr	al, 3
	and	eax, 15
	movsxd	rax, DWORD PTR [rcx+rax*4]
	add	rax, rcx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2475:
	.long	.L2668-.L2475
	.long	.L2482-.L2475
	.long	.L2481-.L2475
	.long	.L2480-.L2475
	.long	.L2781-.L2475
	.long	.L2478-.L2475
	.long	.L2782-.L2475
	.long	.L2476-.L2475
	.long	.L2783-.L2475
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2704:
	mov	rax, r13
	jmp	.L2642
	.p2align 4
	.p2align 4,,10
	.p2align 3
.L2809:
	add	r9, 1
	cmp	r9, r13
	jnb	.L2786
.L2529:
	cmp	BYTE PTR [r12+r9], 48
	je	.L2809
	jmp	.L2527
	.p2align 4,,10
	.p2align 3
.L2808:
	movzx	eax, BYTE PTR [r14]
	lea	rdx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	cmp	BYTE PTR [rdx+rax], 15
	ja	.L2810
	mov	rax, r13
	mov	r8d, 2
	mov	edx, 48
	jmp	.L2642
	.p2align 4,,10
	.p2align 3
.L2623:
	mov	rcx, QWORD PTR 208[rsp]
	lea	rax, 224[rsp]
	mov	r15, r12
	cmp	rcx, rax
	je	.L2630
.L2649:
	mov	rax, QWORD PTR 224[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L2630:
	mov	r14, r12
	mov	r12, r15
	jmp	.L2620
	.p2align 4,,10
	.p2align 3
.L2682:
	mov	QWORD PTR 80[rsp], 0
.L2522:
	mov	r10, QWORD PTR 80[rsp]
	cmp	BYTE PTR 48[rsp], 0
	je	.L2690
	test	rbp, rbp
	je	.L2691
	mov	QWORD PTR 72[rsp], 1
	mov	rax, r10
	sub	rax, r11
.L2532:
	sub	rbp, rax
	add	QWORD PTR 72[rsp], rbp
	jmp	.L2525
	.p2align 4,,10
	.p2align 3
.L2710:
	mov	ebp, 6
.L2781:
	mov	BYTE PTR 56[rsp], 69
	mov	r13d, 1
.L2479:
	mov	BYTE PTR 48[rsp], 0
	mov	r15d, 1
.L2483:
	mov	DWORD PTR 40[rsp], ebp
	lea	r12, 112[rsp]
	lea	rax, 241[rsp]
	movapd	xmm3, xmm6
	mov	DWORD PTR 32[rsp], r15d
	lea	r8, 368[rsp]
	mov	rdx, rax
	mov	rcx, r12
	mov	QWORD PTR 72[rsp], rax
	call	_ZSt8to_charsPcS_dSt12chars_formati
	mov	r14, QWORD PTR 112[rsp]
	cmp	DWORD PTR 120[rsp], 132
	je	.L2660
	lea	rax, 368[rsp]
	mov	r12, QWORD PTR 72[rsp]
	mov	QWORD PTR 64[rsp], rax
.L2488:
	test	r13b, r13b
	je	.L2490
	cmp	r12, r14
	je	.L2490
	mov	r13, QWORD PTR __imp_toupper[rip]
	mov	r15, r12
	.p2align 4
	.p2align 3
.L2518:
	movsx	ecx, BYTE PTR [r15]
	add	r15, 1
	call	r13
	mov	BYTE PTR -1[r15], al
	cmp	r15, r14
	jne	.L2518
	jmp	.L2490
	.p2align 4,,10
	.p2align 3
.L2711:
	mov	ebp, 6
.L2478:
	xor	r13d, r13d
.L2477:
	mov	BYTE PTR 56[rsp], 101
	mov	r15d, 2
	mov	BYTE PTR 48[rsp], 0
	jmp	.L2483
	.p2align 4,,10
	.p2align 3
.L2712:
	mov	ebp, 6
.L2782:
	mov	r13d, 1
	jmp	.L2477
	.p2align 4,,10
	.p2align 3
.L2713:
	mov	ebp, 6
.L2476:
	mov	BYTE PTR 56[rsp], 101
	xor	r13d, r13d
.L2474:
	mov	BYTE PTR 48[rsp], 1
	mov	r15d, 3
	jmp	.L2483
	.p2align 4,,10
	.p2align 3
.L2714:
	mov	ebp, 6
.L2783:
	mov	BYTE PTR 56[rsp], 69
	mov	r13d, 1
	jmp	.L2474
	.p2align 4,,10
	.p2align 3
.L2485:
	and	edx, 120
	mov	eax, 112
	cmp	dl, 16
	mov	edx, 101
	cmove	eax, edx
	xor	r13d, r13d
	mov	BYTE PTR 56[rsp], al
.L2486:
	lea	r12, 112[rsp]
	mov	DWORD PTR 32[rsp], 4
	movapd	xmm3, xmm6
	lea	r8, 368[rsp]
	lea	rdx, 241[rsp]
	mov	rcx, r12
	mov	ebp, 6
	call	_ZSt8to_charsPcS_dSt12chars_format
	mov	BYTE PTR 48[rsp], 0
	mov	r14, QWORD PTR 112[rsp]
	cmp	DWORD PTR 120[rsp], 132
	je	.L2674
.L2784:
	lea	rax, 368[rsp]
	lea	r12, 241[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L2488
	.p2align 4,,10
	.p2align 3
.L2666:
	and	edx, 120
	mov	eax, 112
	mov	r13d, 1
	cmp	dl, 16
	mov	edx, 80
	cmove	eax, edx
	mov	BYTE PTR 56[rsp], al
	jmp	.L2486
	.p2align 4,,10
	.p2align 3
.L2709:
	mov	ebp, 6
.L2480:
	mov	BYTE PTR 56[rsp], 101
	xor	r13d, r13d
	jmp	.L2479
	.p2align 4,,10
	.p2align 3
.L2804:
	mov	rcx, r15
	call	_ZNSt6localeC1Ev
	mov	BYTE PTR 32[rsi], 1
	jmp	.L2622
	.p2align 4,,10
	.p2align 3
.L2668:
	mov	BYTE PTR 56[rsp], 101
	mov	r15d, 3
	xor	r13d, r13d
	mov	BYTE PTR 48[rsp], 0
	jmp	.L2483
	.p2align 4,,10
	.p2align 3
.L2793:
	mov	BYTE PTR -1[r12], 43
	mov	r11d, 1
	movzx	r15d, BYTE PTR [rbx]
	sub	r12, 1
	jmp	.L2517
	.p2align 4,,10
	.p2align 3
.L2633:
	movzx	ecx, WORD PTR 4[rbx]
	mov	rdx, rsi
.LEHB46:
	call	_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0
	mov	r9, rax
	jmp	.L2632
	.p2align 4,,10
	.p2align 3
.L2807:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	r13, rsi
	jb	.L2638
	.p2align 4
	.p2align 3
.L2640:
	test	rsi, rsi
	je	.L2639
	mov	r8, rsi
	mov	rdx, r12
	call	memcpy
.L2639:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rsi
	add	r12, rsi
	sub	r13, rsi
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
.LEHE46:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	r13, rsi
	jnb	.L2640
	test	r13, r13
	je	.L2641
.L2638:
	mov	r8, r13
	mov	rdx, r12
	call	memcpy
	add	QWORD PTR 24[rbx], r13
	jmp	.L2641
	.p2align 4,,10
	.p2align 3
.L2795:
	cmp	r13, rax
	mov	r10, r13
	sete	al
	movzx	eax, al
	mov	QWORD PTR 72[rsp], rax
	cmp	BYTE PTR 48[rsp], 0
	jne	.L2811
.L2687:
	xor	ebp, ebp
	jmp	.L2525
	.p2align 4,,10
	.p2align 3
.L2523:
	movsx	edx, BYTE PTR 56[rsp]
	mov	r8, r13
	mov	rcx, r12
	mov	BYTE PTR 72[rsp], r11b
	call	memchr
	movzx	r11d, BYTE PTR 72[rsp]
	test	rax, rax
	je	.L2688
	sub	rax, r12
	cmp	rax, -1
	cmove	rax, r13
	mov	QWORD PTR 80[rsp], rax
	jmp	.L2522
	.p2align 4,,10
	.p2align 3
.L2690:
	mov	QWORD PTR 72[rsp], 1
	xor	ebp, ebp
	jmp	.L2531
.L2482:
	and	edx, 120
	mov	eax, 101
	cmp	dl, 16
	mov	edx, 112
	cmovne	eax, edx
	xor	r13d, r13d
	mov	BYTE PTR 56[rsp], al
.L2484:
	mov	DWORD PTR 40[rsp], ebp
	lea	r12, 112[rsp]
	movapd	xmm3, xmm6
	lea	r8, 368[rsp]
	mov	DWORD PTR 32[rsp], 4
	lea	rdx, 241[rsp]
	mov	rcx, r12
	call	_ZSt8to_charsPcS_dSt12chars_formati
	mov	r14, QWORD PTR 112[rsp]
	cmp	DWORD PTR 120[rsp], 132
	je	.L2664
	mov	BYTE PTR 48[rsp], 0
	jmp	.L2784
	.p2align 4,,10
	.p2align 3
.L2481:
	and	edx, 120
	mov	eax, 112
	mov	r13d, 1
	cmp	dl, 16
	mov	edx, 80
	cmove	eax, edx
	mov	BYTE PTR 56[rsp], al
	jmp	.L2484
.L2811:
	cmp	BYTE PTR [r12+r11], 48
	jne	.L2526
.L2786:
	mov	r9, -1
.L2527:
	mov	rax, r10
	sub	rax, r9
	jmp	.L2530
.L2688:
	mov	QWORD PTR 80[rsp], r13
	jmp	.L2522
.L2796:
	cmp	r15, 15
	jbe	.L2540
.L2539:
	movabs	rax, 9223372036854775806
	cmp	rax, r15
	jb	.L2541
	mov	QWORD PTR 64[rsp], r9
	mov	QWORD PTR 48[rsp], r10
	cmp	r15, 29
	ja	.L2542
	mov	ecx, 31
.LEHB47:
	call	_Znwy
	mov	r10, QWORD PTR 48[rsp]
	mov	r9, QWORD PTR 64[rsp]
	mov	r14, rax
	mov	rdx, rdi
	mov	r15d, 30
	jmp	.L2543
.L2798:
	mov	r9, QWORD PTR 152[rsp]
	mov	QWORD PTR 144[rsp], r14
	mov	QWORD PTR 160[rsp], r15
	test	r9, r9
	jne	.L2538
	.p2align 4
	.p2align 3
.L2540:
	movabs	rax, 9223372036854775806
	cmp	r13, r10
	mov	r14, r10
	cmovbe	r14, r13
	cmp	rax, r14
	jb	.L2812
	mov	r15, QWORD PTR 144[rsp]
	cmp	r15, rdi
	je	.L2813
	mov	rdx, QWORD PTR 160[rsp]
	cmp	rdx, r14
	jb	.L2559
.L2556:
	cmp	r12, r15
	je	.L2560
	test	r14, r14
	je	.L2562
	cmp	r14, 1
	je	.L2814
	mov	rcx, r15
	mov	r8, r14
	mov	rdx, r12
	mov	QWORD PTR 48[rsp], r10
	call	memcpy
	mov	r15, QWORD PTR 144[rsp]
	mov	r10, QWORD PTR 48[rsp]
.L2562:
	mov	QWORD PTR 152[rsp], r14
	mov	BYTE PTR [r15+r14], 0
	cmp	r10, QWORD PTR 80[rsp]
	je	.L2815
.L2789:
	test	rbp, rbp
	je	.L2791
	mov	r8, QWORD PTR 152[rsp]
	movabs	rax, 9223372036854775806
	mov	rdx, rax
	sub	rdx, r8
	cmp	rdx, rbp
	jb	.L2816
	mov	r15, QWORD PTR 144[rsp]
	lea	r14, [r8+rbp]
	cmp	r15, rdi
	je	.L2817
	mov	r9, QWORD PTR 160[rsp]
	cmp	r9, r14
	jb	.L2818
.L2578:
	lea	rcx, [r15+r8]
	cmp	rbp, 1
	je	.L2819
	mov	r8, rbp
	mov	edx, 48
	mov	QWORD PTR 48[rsp], r10
	call	memset
	mov	r10, QWORD PTR 48[rsp]
.L2591:
	mov	rax, QWORD PTR 144[rsp]
	mov	QWORD PTR 152[rsp], r14
	mov	BYTE PTR [rax+r14], 0
.L2791:
	cmp	r13, r10
	jb	.L2820
	mov	rdx, QWORD PTR 152[rsp]
	sub	r13, r10
	lea	r9, [r12+r10]
	movabs	rax, 9223372036854775806
	sub	rax, rdx
	cmp	rax, r13
	jb	.L2821
	mov	rax, QWORD PTR 144[rsp]
	mov	ecx, 15
	lea	rbp, 0[r13+rdx]
	cmp	rax, rdi
	cmovne	rcx, QWORD PTR 160[rsp]
	cmp	rcx, rbp
	jb	.L2595
	test	r13, r13
	je	.L2596
	lea	rcx, [rax+rdx]
	cmp	r13, 1
	je	.L2822
	mov	r8, r13
	mov	rdx, r9
	call	memcpy
	mov	rax, QWORD PTR 144[rsp]
.L2596:
	mov	QWORD PTR 152[rsp], rbp
	mov	BYTE PTR [rax+rbp], 0
	jmp	.L2598
	.p2align 4,,10
	.p2align 3
.L2533:
	mov	rdx, QWORD PTR 144[rsp]
	cmp	rdx, rdi
	je	.L2823
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, r15
	jnb	.L2538
	jmp	.L2544
.L2810:
	mov	rax, QWORD PTR 24[rcx]
	movzx	edx, BYTE PTR [r12]
	lea	r8, 1[rax]
	mov	QWORD PTR 24[rcx], r8
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[rcx]
	sub	rax, QWORD PTR 8[rcx]
	cmp	rax, QWORD PTR 16[rcx]
	je	.L2824
.L2643:
	add	r12, 1
	lea	rax, -1[r13]
	mov	r8d, 2
	mov	edx, 48
	jmp	.L2642
.L2675:
	mov	BYTE PTR 48[rsp], 0
	xor	r13d, r13d
	xor	r15d, r15d
	mov	r14d, 14
	mov	BYTE PTR 56[rsp], 101
	mov	BYTE PTR 64[rsp], 0
.L2487:
	mov	r9, QWORD PTR 144[rsp]
	cmp	r14, 128
	jbe	.L2825
	cmp	r9, rdi
	je	.L2826
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, r14
	jb	.L2827
.L2659:
	cmp	r9, rdi
	je	.L2679
	mov	rax, QWORD PTR 160[rsp]
	lea	r14, [rax+rax]
	cmp	rax, r14
	jnb	.L2506
	movabs	rax, 9223372036854775806
	cmp	rax, r14
	jb	.L2828
	lea	rcx, 1[r14]
.L2505:
	mov	QWORD PTR 72[rsp], r9
	call	_Znwy
	mov	r11, rax
	mov	rax, QWORD PTR 152[rsp]
	mov	r9, QWORD PTR 72[rsp]
	test	rax, rax
	lea	r8, 1[rax]
	je	.L2829
	mov	rcx, r11
	mov	rdx, r9
	call	memcpy
	mov	r11, rax
.L2509:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rdi
	je	.L2510
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 72[rsp], r11
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r11, QWORD PTR 72[rsp]
.L2510:
	mov	QWORD PTR 144[rsp], r11
	mov	r9, r11
	mov	QWORD PTR 160[rsp], r14
.L2506:
	cmp	BYTE PTR 64[rsp], 0
	mov	QWORD PTR 72[rsp], r9
	lea	r8, -1[r9+r14]
	lea	rdx, 1[r9]
	jne	.L2830
	test	r15d, r15d
	je	.L2513
	mov	DWORD PTR 32[rsp], r15d
	movapd	xmm3, xmm6
	mov	rcx, r12
	call	_ZSt8to_charsPcS_dSt12chars_format
	mov	r10, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 72[rsp]
.L2512:
	mov	r14, r10
	test	eax, eax
	jne	.L2514
	mov	rdx, QWORD PTR 144[rsp]
	mov	rax, r10
	sub	rax, r9
	mov	QWORD PTR 152[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rax, QWORD PTR 144[rsp]
	lea	r12, 1[rax]
	add	rax, QWORD PTR 152[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L2488
	.p2align 4,,10
	.p2align 3
.L2514:
	mov	rdx, QWORD PTR 144[rsp]
	mov	QWORD PTR 152[rsp], 0
	mov	BYTE PTR [rdx], 0
	mov	r9, QWORD PTR 144[rsp]
	cmp	eax, 132
	je	.L2659
	lea	r12, 1[r9]
	add	r9, QWORD PTR 152[rsp]
	mov	QWORD PTR 64[rsp], r9
	jmp	.L2488
.L2513:
	movapd	xmm3, xmm6
	mov	rcx, r12
	call	_ZSt8to_charsPcS_d
	mov	r10, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 72[rsp]
	jmp	.L2512
.L2674:
	mov	BYTE PTR 64[rsp], 0
	mov	r15d, 4
	mov	r14d, 14
	jmp	.L2487
.L2660:
	mov	BYTE PTR 64[rsp], 1
	lea	r14, 8[rbp]
	cmp	r15d, 2
	jne	.L2487
	lea	rdx, 208[rsp]
	movapd	xmm0, xmm6
	mov	DWORD PTR 208[rsp], 0
	call	frexp
	mov	eax, DWORD PTR 208[rsp]
	test	eax, eax
	jle	.L2491
	imul	edx, eax, 4004
	mov	rax, rdx
	imul	rdx, rdx, 995517945
	shr	rdx, 32
	sub	eax, edx
	shr	eax
	add	eax, edx
	shr	eax, 13
	add	eax, 1
	add	r14, rax
.L2491:
	mov	BYTE PTR 64[rsp], 1
	jmp	.L2487
.L2830:
	mov	DWORD PTR 40[rsp], ebp
	movapd	xmm3, xmm6
	mov	rcx, r12
	mov	DWORD PTR 32[rsp], r15d
	call	_ZSt8to_charsPcS_dSt12chars_formati
	mov	r10, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 72[rsp]
	jmp	.L2512
.L2827:
	movabs	rcx, 9223372036854775806
	cmp	rcx, r14
	jb	.L2496
	add	rax, rax
	cmp	r14, rax
	jnb	.L2663
	cmp	rcx, rax
	jnb	.L2662
	mov	r14, rcx
	mov	rdx, r9
	movabs	rcx, 9223372036854775807
.L2501:
	mov	QWORD PTR 72[rsp], rdx
	call	_Znwy
	mov	r9, rax
	mov	rax, QWORD PTR 152[rsp]
	mov	rdx, QWORD PTR 72[rsp]
	test	rax, rax
	lea	r8, 1[rax]
	je	.L2831
	mov	rcx, r9
	call	memcpy
	mov	r9, rax
.L2503:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rdi
	je	.L2504
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 72[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 72[rsp]
.L2504:
	mov	QWORD PTR 144[rsp], r9
	mov	QWORD PTR 160[rsp], r14
	jmp	.L2659
.L2534:
	mov	rcx, QWORD PTR 72[rsp]
	lea	r14, [r12+r10]
	mov	r8, r13
	mov	QWORD PTR 48[rsp], r10
	sub	r8, r10
	mov	rdx, r14
	add	rcx, r10
	add	rcx, r12
	call	memmove
	mov	r10, QWORD PTR 48[rsp]
	cmp	r10, QWORD PTR 80[rsp]
	jne	.L2552
	mov	BYTE PTR [r14], 46
	lea	r14, 1[r12+r10]
.L2552:
	mov	r8, rbp
	mov	edx, 48
	mov	rcx, r14
	mov	r13, r15
	call	memset
	jmp	.L2553
.L2805:
	mov	rax, QWORD PTR 208[rsp]
	lea	r14, 224[rsp]
	cmp	rax, r14
	je	.L2650
	mov	QWORD PTR 176[rsp], rax
	movq	xmm0, r8
	movhps	xmm0, QWORD PTR 224[rsp]
	movups	XMMWORD PTR 184[rsp], xmm0
.L2629:
	mov	QWORD PTR 208[rsp], r14
	lea	r14, 224[rsp]
	mov	rcx, r14
	jmp	.L2628
.L2691:
	mov	QWORD PTR 72[rsp], 1
	jmp	.L2531
.L2685:
	mov	r10, r13
	jmp	.L2528
.L2679:
	mov	ecx, 31
	mov	r14d, 30
	jmp	.L2505
.L2826:
	movabs	rax, 9223372036854775806
	cmp	rax, r14
	jb	.L2496
	lea	rcx, 1[r14]
	mov	rdx, rdi
	jmp	.L2501
.L2829:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [r11], al
	jmp	.L2509
.L2831:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [r9], al
	jmp	.L2503
.L2606:
	sub	r9, r10
	mov	rbp, r9
	cmp	rax, r13
	jb	.L2603
	add	r12, r12
	cmp	r13, r12
	jb	.L2610
.L2605:
	lea	rcx, 1[r13]
	mov	r12, r13
.L2611:
	mov	QWORD PTR 48[rsp], r10
	call	_Znwy
	mov	r10, QWORD PTR 48[rsp]
	mov	r15, rax
	test	r10, r10
	je	.L2612
	cmp	r10, 1
	je	.L2832
	mov	r8, r10
	mov	rdx, r14
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], r10
	call	memcpy
	mov	r14, QWORD PTR 144[rsp]
	mov	r10, QWORD PTR 48[rsp]
.L2612:
	test	rbp, rbp
	je	.L2614
	mov	rax, QWORD PTR 72[rsp]
	lea	rdx, [r14+r10]
	lea	rcx, [r10+rax]
	add	rcx, r15
	cmp	rbp, 1
	je	.L2833
	mov	r8, rbp
	mov	QWORD PTR 48[rsp], r10
	call	memcpy
	mov	r14, QWORD PTR 144[rsp]
	mov	r10, QWORD PTR 48[rsp]
.L2614:
	cmp	r14, rdi
	je	.L2616
	mov	rax, QWORD PTR 160[rsp]
	mov	rcx, r14
	mov	QWORD PTR 48[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 48[rsp]
.L2616:
	mov	QWORD PTR 144[rsp], r15
	lea	rcx, [r15+r10]
	mov	QWORD PTR 160[rsp], r12
	jmp	.L2607
.L2797:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [r14], al
	jmp	.L2550
.L2595:
	mov	QWORD PTR 32[rsp], r13
	lea	rcx, 144[rsp]
	xor	r8d, r8d
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rax, QWORD PTR 144[rsp]
	jmp	.L2596
.L2825:
	cmp	r9, rdi
	je	.L2834
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, 255
	ja	.L2659
	add	rax, rax
	cmp	rax, 256
	jbe	.L2835
.L2662:
	lea	rcx, 1[rax]
	mov	rdx, r9
	mov	r14, rax
	jmp	.L2501
.L2650:
	cmp	r8, 1
	je	.L2836
	mov	rdx, r14
	call	memcpy
.L2627:
	mov	rax, QWORD PTR 216[rsp]
	mov	rdx, QWORD PTR 176[rsp]
	mov	QWORD PTR 184[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rcx, QWORD PTR 208[rsp]
	jmp	.L2628
.L2815:
	mov	r14, QWORD PTR 152[rsp]
	mov	rdx, QWORD PTR 144[rsp]
	lea	r9, 1[r14]
	cmp	rdx, rdi
	je	.L2837
	mov	r15, QWORD PTR 160[rsp]
	cmp	r15, r9
	jb	.L2838
.L2570:
	mov	BYTE PTR [rdx+r14], 46
	mov	rax, QWORD PTR 144[rsp]
	mov	QWORD PTR 152[rsp], r9
	mov	BYTE PTR 1[rax+r14], 0
	jmp	.L2789
.L2801:
	cmp	r13, 15
	jbe	.L2602
	sub	r9, r10
	mov	rbp, r9
	cmp	rax, r13
	jb	.L2603
	cmp	r13, 29
	ja	.L2605
	mov	r12d, 30
.L2604:
	lea	rcx, 1[r12]
	jmp	.L2611
.L2813:
	cmp	r14, 15
	jbe	.L2556
	cmp	r14, 29
	ja	.L2558
	mov	QWORD PTR 48[rsp], 30
.L2557:
	mov	rax, QWORD PTR 48[rsp]
	lea	rcx, 1[rax]
.L2565:
	mov	QWORD PTR 64[rsp], r10
	call	_Znwy
	mov	rcx, rax
	mov	r8, r14
	mov	rdx, r12
	mov	r15, rax
	call	memcpy
	mov	rcx, QWORD PTR 144[rsp]
	mov	r10, QWORD PTR 64[rsp]
	cmp	rcx, rdi
	je	.L2566
	mov	rax, QWORD PTR 160[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 64[rsp]
.L2566:
	mov	rax, QWORD PTR 48[rsp]
	mov	QWORD PTR 144[rsp], r15
	mov	QWORD PTR 160[rsp], rax
	jmp	.L2562
.L2803:
	mov	BYTE PTR [rcx], 48
	jmp	.L2618
.L2823:
	cmp	r15, 15
	jbe	.L2538
	jmp	.L2539
.L2559:
	add	rdx, rdx
	mov	QWORD PTR 48[rsp], rdx
	cmp	r14, rdx
	jb	.L2564
.L2558:
	mov	QWORD PTR 48[rsp], r14
	lea	rcx, 1[r14]
	jmp	.L2565
.L2818:
	cmp	rax, r14
	jb	.L2579
	add	r9, r9
	cmp	r14, r9
	jb	.L2583
.L2581:
	lea	rcx, 1[r14]
	mov	r9, r14
.L2584:
	mov	QWORD PTR 72[rsp], r9
	mov	QWORD PTR 64[rsp], r10
	mov	QWORD PTR 48[rsp], r8
	call	_Znwy
	mov	r8, QWORD PTR 48[rsp]
	mov	r10, QWORD PTR 64[rsp]
	mov	r11, rax
	mov	r9, QWORD PTR 72[rsp]
	test	r8, r8
	je	.L2788
	cmp	r8, 1
	je	.L2839
	mov	rdx, r15
	mov	rcx, rax
	mov	QWORD PTR 72[rsp], r9
	mov	QWORD PTR 64[rsp], r10
	mov	QWORD PTR 48[rsp], r8
	call	memcpy
	mov	r9, QWORD PTR 72[rsp]
	mov	r10, QWORD PTR 64[rsp]
	mov	r8, QWORD PTR 48[rsp]
	mov	r11, rax
.L2587:
	mov	r15, QWORD PTR 144[rsp]
.L2788:
	cmp	r15, rdi
	je	.L2589
	mov	rax, QWORD PTR 160[rsp]
	mov	rcx, r15
	mov	QWORD PTR 80[rsp], r11
	mov	QWORD PTR 72[rsp], r9
	lea	rdx, 1[rax]
	mov	QWORD PTR 64[rsp], r10
	mov	QWORD PTR 48[rsp], r8
	call	_ZdlPvy
	mov	r11, QWORD PTR 80[rsp]
	mov	r9, QWORD PTR 72[rsp]
	mov	r10, QWORD PTR 64[rsp]
	mov	r8, QWORD PTR 48[rsp]
.L2589:
	mov	QWORD PTR 144[rsp], r11
	mov	r15, r11
	mov	QWORD PTR 160[rsp], r9
	jmp	.L2578
.L2814:
	movzx	eax, BYTE PTR [r12]
	mov	BYTE PTR [r15], al
	mov	r15, QWORD PTR 144[rsp]
	jmp	.L2562
.L2802:
	movzx	edx, BYTE PTR [rcx]
	mov	BYTE PTR [rax], dl
	mov	rcx, QWORD PTR 144[rsp]
	add	rcx, r10
	jmp	.L2607
.L2822:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	mov	rax, QWORD PTR 144[rsp]
	jmp	.L2596
.L2542:
	lea	rcx, 1[r15]
	call	_Znwy
.LEHE47:
	mov	r10, QWORD PTR 48[rsp]
	mov	r9, QWORD PTR 64[rsp]
	mov	r14, rax
	mov	rdx, rdi
	jmp	.L2543
.L2817:
	cmp	r14, 15
	jbe	.L2578
	cmp	rax, r14
	jb	.L2579
	cmp	r14, 29
	ja	.L2581
	mov	r9d, 30
.L2580:
	lea	rcx, 1[r9]
	jmp	.L2584
.L2564:
	cmp	rax, QWORD PTR 48[rsp]
	jnb	.L2557
	movabs	rcx, 9223372036854775807
	mov	QWORD PTR 48[rsp], rax
	jmp	.L2565
.L2819:
	mov	BYTE PTR [rcx], 48
	jmp	.L2591
.L2824:
	mov	rax, QWORD PTR [rcx]
	mov	QWORD PTR 56[rsp], r9
	mov	QWORD PTR 48[rsp], rcx
.LEHB48:
	call	[QWORD PTR [rax]]
.LEHE48:
	mov	r9, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 48[rsp]
	jmp	.L2643
.L2610:
	cmp	rax, r12
	jnb	.L2604
	movabs	rcx, 9223372036854775807
	mov	r12, rax
	jmp	.L2611
.L2836:
	movzx	eax, BYTE PTR 224[rsp]
	mov	BYTE PTR [rcx], al
	jmp	.L2627
.L2832:
	movzx	eax, BYTE PTR [r14]
	mov	BYTE PTR [r15], al
	mov	r14, QWORD PTR 144[rsp]
	jmp	.L2612
.L2833:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rcx], al
	mov	r14, QWORD PTR 144[rsp]
	jmp	.L2614
.L2838:
	movabs	rcx, 9223372036854775807
	cmp	r9, rcx
	je	.L2840
	add	r15, r15
	cmp	r9, r15
	jb	.L2572
	lea	rcx, 2[r14]
	mov	r15, r9
.L2573:
	mov	QWORD PTR 80[rsp], r9
	mov	QWORD PTR 72[rsp], rdx
	mov	QWORD PTR 64[rsp], r10
.LEHB49:
	call	_Znwy
	mov	rdx, QWORD PTR 72[rsp]
	mov	rcx, rax
	mov	r8, r14
	mov	QWORD PTR 48[rsp], rax
	call	memcpy
	mov	r10, QWORD PTR 64[rsp]
	mov	r9, QWORD PTR 80[rsp]
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rdi
	je	.L2574
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 72[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 72[rsp]
	mov	r10, QWORD PTR 64[rsp]
.L2574:
	mov	rax, QWORD PTR 48[rsp]
	mov	QWORD PTR 160[rsp], r15
	mov	QWORD PTR 144[rsp], rax
	mov	rdx, rax
	jmp	.L2570
.L2834:
	mov	ecx, 257
	mov	rdx, rdi
	mov	r14d, 256
	jmp	.L2501
.L2837:
	cmp	r9, 16
	jne	.L2570
	mov	r15d, 30
.L2569:
	lea	rcx, 1[r15]
	jmp	.L2573
.L2583:
	cmp	rax, r9
	jnb	.L2580
	movabs	rcx, 9223372036854775807
	mov	r9, rax
	jmp	.L2584
.L2839:
	movzx	eax, BYTE PTR [r15]
	mov	BYTE PTR [r11], al
	jmp	.L2587
.L2572:
	movabs	rax, 9223372036854775806
	cmp	rax, r15
	jnb	.L2569
	mov	r15, rax
	jmp	.L2573
.L2664:
	mov	BYTE PTR 48[rsp], 0
	lea	r14, 8[rbp]
	mov	r15d, 4
	mov	BYTE PTR 64[rsp], 1
	jmp	.L2487
.L2835:
	mov	r14d, 256
.L2663:
	lea	rcx, 1[r14]
	mov	rdx, r9
	jmp	.L2501
.L2496:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2603:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2560:
	xor	eax, eax
	mov	QWORD PTR 32[rsp], r14
	mov	r9, r12
	xor	r8d, r8d
	mov	QWORD PTR 40[rsp], rax
	lea	rcx, 144[rsp]
	mov	rdx, r12
	mov	QWORD PTR 48[rsp], r10
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	r10, QWORD PTR 48[rsp]
	mov	r15, QWORD PTR 144[rsp]
	jmp	.L2562
.L2473:
.L2718:
	mov	rbx, rax
	jmp	.L2647
.L2799:
	mov	r8, r10
	lea	rdx, .LC37[rip]
	lea	rcx, .LC38[rip]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.LEHE49:
.L2716:
	mov	rbx, rax
	jmp	.L2648
.L2717:
	mov	rbx, rax
.L2646:
	lea	rcx, 136[rsp]
	call	_ZNSt6localeD1Ev
.L2647:
	lea	rcx, 176[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L2648:
	lea	rcx, 144[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB50:
	call	_Unwind_Resume
.LEHE50:
.L2800:
	lea	rcx, .LC20[rip]
.LEHB51:
	call	_ZSt20__throw_length_errorPKc
.L2840:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2579:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2812:
	lea	rcx, .LC34[rip]
	call	_ZSt20__throw_length_errorPKc
.L2821:
	lea	rcx, .LC14[rip]
	call	_ZSt20__throw_length_errorPKc
.L2816:
	lea	rcx, .LC20[rip]
	call	_ZSt20__throw_length_errorPKc
.L2828:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2820:
	mov	r9, r13
	mov	r8, r10
	lea	rdx, .LC35[rip]
	lea	rcx, .LC36[rip]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L2541:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
.LEHE51:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5609:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5609-.LLSDACSB5609
.LLSDACSB5609:
	.uleb128 .LEHB42-.LFB5609
	.uleb128 .LEHE42-.LEHB42
	.uleb128 .L2716-.LFB5609
	.uleb128 0
	.uleb128 .LEHB43-.LFB5609
	.uleb128 .LEHE43-.LEHB43
	.uleb128 .L2717-.LFB5609
	.uleb128 0
	.uleb128 .LEHB44-.LFB5609
	.uleb128 .LEHE44-.LEHB44
	.uleb128 .L2718-.LFB5609
	.uleb128 0
	.uleb128 .LEHB45-.LFB5609
	.uleb128 .LEHE45-.LEHB45
	.uleb128 .L2716-.LFB5609
	.uleb128 0
	.uleb128 .LEHB46-.LFB5609
	.uleb128 .LEHE46-.LEHB46
	.uleb128 .L2718-.LFB5609
	.uleb128 0
	.uleb128 .LEHB47-.LFB5609
	.uleb128 .LEHE47-.LEHB47
	.uleb128 .L2716-.LFB5609
	.uleb128 0
	.uleb128 .LEHB48-.LFB5609
	.uleb128 .LEHE48-.LEHB48
	.uleb128 .L2718-.LFB5609
	.uleb128 0
	.uleb128 .LEHB49-.LFB5609
	.uleb128 .LEHE49-.LEHB49
	.uleb128 .L2716-.LFB5609
	.uleb128 0
	.uleb128 .LEHB50-.LFB5609
	.uleb128 .LEHE50-.LEHB50
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB51-.LFB5609
	.uleb128 .LEHE51-.LEHB51
	.uleb128 .L2716-.LFB5609
	.uleb128 0
.LLSDACSE5609:
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
.LFB5603:
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
	sub	rsp, 392
	.seh_stackalloc	392
	movaps	XMMWORD PTR 368[rsp], xmm6
	.seh_savexmm	xmm6, 368
	.seh_endprologue
	mov	BYTE PTR 160[rsp], 0
	movzx	edx, BYTE PTR 1[rcx]
	mov	rbx, rcx
	movaps	xmm6, xmm1
	lea	rdi, 160[rsp]
	mov	rsi, r8
	mov	QWORD PTR 152[rsp], 0
	mov	QWORD PTR 144[rsp], rdi
	test	dl, 6
	jne	.L3162
	mov	eax, edx
	shr	al, 3
	and	eax, 15
	cmp	al, 8
	ja	.L2843
	lea	rcx, .L3035[rip]
	movzx	eax, al
	movsxd	rax, DWORD PTR [rcx+rax*4]
	add	rax, rcx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L3035:
	.long	.L2859-.L3035
	.long	.L2855-.L3035
	.long	.L3036-.L3035
	.long	.L3079-.L3035
	.long	.L3080-.L3035
	.long	.L3081-.L3035
	.long	.L3082-.L3035
	.long	.L3083-.L3035
	.long	.L3084-.L3035
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2859:
	lea	r12, 112[rsp]
	movaps	xmm3, xmm6
	lea	r8, 368[rsp]
	mov	ebp, 6
	lea	rdx, 241[rsp]
	mov	rcx, r12
	call	_ZSt8to_charsPcS_f
	mov	r14, QWORD PTR 112[rsp]
	cmp	DWORD PTR 120[rsp], 132
	je	.L3045
	lea	rax, 368[rsp]
	mov	BYTE PTR 48[rsp], 0
	lea	r12, 241[rsp]
	mov	BYTE PTR 56[rsp], 101
	mov	QWORD PTR 64[rsp], rax
.L2860:
	movd	eax, xmm6
	movzx	r15d, BYTE PTR [rbx]
	test	eax, eax
	js	.L3155
	mov	eax, r15d
	and	eax, 12
	cmp	al, 4
	je	.L3163
	xor	r11d, r11d
	cmp	al, 12
	je	.L3164
.L2887:
	mov	r13, r14
	sub	r13, r12
	test	r15b, 16
	je	.L2891
	movss	xmm1, DWORD PTR .LC43[rip]
	movaps	xmm0, xmm6
	andps	xmm0, XMMWORD PTR .LC42[rip]
	ucomiss	xmm1, xmm0
	jb	.L2891
	test	r13, r13
	je	.L3052
	mov	r8, r13
	mov	edx, 46
	mov	rcx, r12
	mov	BYTE PTR 72[rsp], r11b
	call	memchr
	movzx	r11d, BYTE PTR 72[rsp]
	test	rax, rax
	je	.L2893
	sub	rax, r12
	mov	QWORD PTR 80[rsp], rax
	cmp	rax, -1
	je	.L2893
	lea	r9, 1[rax]
	cmp	r9, r13
	jnb	.L3165
	movsx	edx, BYTE PTR 56[rsp]
	mov	r8, r13
	lea	rcx, [r12+r9]
	mov	BYTE PTR 88[rsp], r11b
	sub	r8, r9
	mov	QWORD PTR 72[rsp], r9
	call	memchr
	mov	r9, QWORD PTR 72[rsp]
	movzx	r11d, BYTE PTR 88[rsp]
	test	rax, rax
	je	.L3055
	sub	rax, r12
	mov	r10, rax
	cmp	rax, -1
	cmove	r10, r13
.L2898:
	xor	eax, eax
	cmp	r10, QWORD PTR 80[rsp]
	sete	al
	mov	QWORD PTR 72[rsp], rax
	cmp	BYTE PTR 48[rsp], 0
	je	.L3057
	cmp	BYTE PTR [r12+r11], 48
	je	.L2899
.L2896:
	mov	rax, r10
	sub	rax, r11
	sub	rax, 1
.L2900:
	test	rbp, rbp
	jne	.L2902
	.p2align 4
	.p2align 3
.L2895:
	cmp	QWORD PTR 72[rsp], 0
	je	.L2891
.L2901:
	mov	rdx, QWORD PTR 72[rsp]
	mov	r9, QWORD PTR 152[rsp]
	lea	r15, 0[r13+rdx]
	test	r9, r9
	jne	.L2903
	mov	rax, QWORD PTR 64[rsp]
	sub	rax, r14
	cmp	rax, rdx
	jnb	.L2904
	mov	rdx, QWORD PTR 144[rsp]
	cmp	rdx, rdi
	je	.L3166
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, r15
	jnb	.L2910
.L2914:
	movabs	r8, 9223372036854775806
	cmp	r8, r15
	jb	.L2911
	add	rax, rax
	lea	rcx, 1[r15]
	cmp	r15, rax
	jnb	.L2918
	cmp	r8, rax
	lea	r11, 1[rax]
	movabs	rcx, 9223372036854775807
	cmovb	rax, r8
	cmovnb	rcx, r11
	mov	r15, rax
.L2918:
	mov	QWORD PTR 88[rsp], r9
	mov	QWORD PTR 64[rsp], rdx
	mov	QWORD PTR 48[rsp], r10
.LEHB52:
	call	_Znwy
.LEHE52:
	mov	r9, QWORD PTR 88[rsp]
	mov	rdx, QWORD PTR 64[rsp]
	mov	r14, rax
	mov	r10, QWORD PTR 48[rsp]
.L2913:
	lea	r8, 1[r9]
	test	r9, r9
	je	.L3167
	mov	rcx, r14
	mov	QWORD PTR 48[rsp], r10
	call	memcpy
	mov	r10, QWORD PTR 48[rsp]
.L2920:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rdi
	je	.L3168
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 48[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 152[rsp]
	mov	r10, QWORD PTR 48[rsp]
	mov	QWORD PTR 144[rsp], r14
	mov	QWORD PTR 160[rsp], r15
	test	r9, r9
	je	.L2910
.L2908:
	cmp	r9, r10
	jb	.L3169
	movabs	rax, 9223372036854775806
	mov	rdx, rax
	sub	rdx, r9
	cmp	rdx, QWORD PTR 72[rsp]
	jb	.L3170
	mov	rdx, QWORD PTR 72[rsp]
	mov	r14, QWORD PTR 144[rsp]
	lea	r13, [r9+rdx]
	cmp	r14, rdi
	je	.L3171
	mov	r12, QWORD PTR 160[rsp]
	cmp	r12, r13
	jb	.L2976
.L2972:
	lea	rcx, [r14+r10]
	sub	r9, r10
	je	.L2977
	mov	rax, QWORD PTR 72[rsp]
	add	rax, rcx
	cmp	r9, 1
	je	.L3172
	mov	rdx, rcx
	mov	r8, r9
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], r10
	call	memmove
	mov	r10, QWORD PTR 48[rsp]
	mov	rcx, QWORD PTR 144[rsp]
	add	rcx, r10
.L2977:
	cmp	QWORD PTR 72[rsp], 1
	je	.L3173
	mov	r8, QWORD PTR 72[rsp]
	mov	edx, 48
	mov	QWORD PTR 48[rsp], r10
	call	memset
	mov	r10, QWORD PTR 48[rsp]
.L2988:
	mov	rax, QWORD PTR 144[rsp]
	mov	QWORD PTR 152[rsp], r13
	mov	BYTE PTR [rax+r13], 0
	cmp	r10, QWORD PTR 80[rsp]
	jne	.L2968
	mov	rax, QWORD PTR 144[rsp]
	mov	BYTE PTR [rax+r10], 46
	.p2align 4
	.p2align 3
.L2968:
	mov	r13, QWORD PTR 152[rsp]
	mov	r12, QWORD PTR 144[rsp]
.L2923:
	lea	rbp, 192[rsp]
	mov	BYTE PTR 192[rsp], 0
	mov	QWORD PTR 176[rsp], rbp
	mov	QWORD PTR 184[rsp], 0
	test	BYTE PTR [rbx], 32
	je	.L2991
.L3031:
	lea	r15, 24[rsi]
	cmp	BYTE PTR 32[rsi], 0
	je	.L3174
.L2992:
	mov	rdx, r15
	lea	rcx, 136[rsp]
	call	_ZNSt6localeC1ERKS_
	movzx	r8d, BYTE PTR 56[rsp]
	lea	rcx, 208[rsp]
	lea	rdx, 96[rsp]
	lea	r9, 136[rsp]
	mov	QWORD PTR 96[rsp], r13
	mov	QWORD PTR 104[rsp], r12
.LEHB53:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE53:
	lea	rcx, 136[rsp]
	call	_ZNSt6localeD1Ev
	mov	r8, QWORD PTR 216[rsp]
	test	r8, r8
	je	.L2993
	mov	rcx, QWORD PTR 176[rsp]
	cmp	rcx, rbp
	je	.L3175
	mov	rax, QWORD PTR 208[rsp]
	lea	r14, 224[rsp]
	cmp	rax, r14
	je	.L3020
	mov	rdx, QWORD PTR 192[rsp]
	movq	xmm0, r8
	mov	QWORD PTR 176[rsp], rax
	movhps	xmm0, QWORD PTR 224[rsp]
	movups	XMMWORD PTR 184[rsp], xmm0
	test	rcx, rcx
	je	.L2999
	mov	QWORD PTR 208[rsp], rcx
	mov	QWORD PTR 224[rsp], rdx
.L2998:
	mov	BYTE PTR [rcx], 0
	mov	rcx, QWORD PTR 208[rsp]
	mov	r13, QWORD PTR 184[rsp]
	mov	r15, QWORD PTR 176[rsp]
	cmp	rcx, r14
	jne	.L3019
	jmp	.L3000
	.p2align 4,,10
	.p2align 3
.L2891:
	lea	rbp, 192[rsp]
	and	r15d, 32
	mov	QWORD PTR 184[rsp], 0
	mov	QWORD PTR 176[rsp], rbp
	mov	BYTE PTR 192[rsp], 0
	je	.L2991
	movss	xmm1, DWORD PTR .LC43[rip]
	movaps	xmm0, xmm6
	andps	xmm0, XMMWORD PTR .LC42[rip]
	ucomiss	xmm1, xmm0
	jnb	.L3031
.L2991:
	mov	r14, r12
.L2990:
	movzx	eax, WORD PTR [rbx]
	and	ax, 384
	cmp	ax, 128
	je	.L3176
	cmp	ax, 256
	je	.L3003
.L3006:
	mov	rbx, QWORD PTR 16[rsi]
	test	r13, r13
	jne	.L3177
.L3011:
	mov	rcx, QWORD PTR 176[rsp]
	cmp	rcx, rbp
	je	.L3014
	mov	rax, QWORD PTR 192[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L3014:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rdi
	je	.L3104
	mov	rax, QWORD PTR 160[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	nop
.L3104:
	movaps	xmm6, XMMWORD PTR 368[rsp]
	mov	rax, rbx
	add	rsp, 392
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
.L3164:
	mov	BYTE PTR -1[r12], 32
	movzx	r15d, BYTE PTR [rbx]
	sub	r12, 1
	.p2align 4
	.p2align 3
.L3155:
	mov	r11d, 1
	jmp	.L2887
	.p2align 4,,10
	.p2align 3
.L3176:
	movzx	r9d, WORD PTR 4[rbx]
.L3002:
	cmp	r13, r9
	jnb	.L3006
	movzx	eax, BYTE PTR [rbx]
	mov	rcx, QWORD PTR 16[rsi]
	mov	edx, DWORD PTR 8[rbx]
	mov	r8d, eax
	and	r8d, 3
	jne	.L3074
	test	al, 64
	je	.L3076
	andps	xmm6, XMMWORD PTR .LC42[rip]
	movss	xmm0, DWORD PTR .LC43[rip]
	ucomiss	xmm0, xmm6
	jnb	.L3178
.L3076:
	mov	rax, r13
	mov	r8d, 2
	mov	edx, 32
.L3012:
	mov	DWORD PTR 32[rsp], edx
	sub	r9, r13
	lea	rdx, 96[rsp]
	mov	QWORD PTR 96[rsp], rax
	mov	QWORD PTR 104[rsp], r12
.LEHB54:
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyDi
.LEHE54:
	mov	rbx, rax
	jmp	.L3011
	.p2align 4,,10
	.p2align 3
.L3162:
	mov	rdx, r8
.LEHB55:
	call	_ZNKSt8__format5_SpecIcE16_M_get_precisionISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_
.LEHE55:
	movzx	edx, BYTE PTR 1[rbx]
	mov	rbp, rax
	lea	rcx, .L2845[rip]
	mov	eax, edx
	shr	al, 3
	and	eax, 15
	movsxd	rax, DWORD PTR [rcx+rax*4]
	add	rax, rcx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L2845:
	.long	.L3038-.L2845
	.long	.L2852-.L2845
	.long	.L2851-.L2845
	.long	.L2850-.L2845
	.long	.L3151-.L2845
	.long	.L2848-.L2845
	.long	.L3152-.L2845
	.long	.L2846-.L2845
	.long	.L3153-.L2845
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L3074:
	mov	rax, r13
	jmp	.L3012
	.p2align 4
	.p2align 4,,10
	.p2align 3
.L3179:
	add	r9, 1
	cmp	r9, r13
	jnb	.L3156
.L2899:
	cmp	BYTE PTR [r12+r9], 48
	je	.L3179
	jmp	.L2897
	.p2align 4,,10
	.p2align 3
.L3178:
	movzx	eax, BYTE PTR [r14]
	lea	rdx, _ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE[rip]
	cmp	BYTE PTR [rdx+rax], 15
	ja	.L3180
	mov	rax, r13
	mov	r8d, 2
	mov	edx, 48
	jmp	.L3012
	.p2align 4,,10
	.p2align 3
.L2993:
	mov	rcx, QWORD PTR 208[rsp]
	lea	rax, 224[rsp]
	mov	r15, r12
	cmp	rcx, rax
	je	.L3000
.L3019:
	mov	rax, QWORD PTR 224[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L3000:
	mov	r14, r12
	mov	r12, r15
	jmp	.L2990
	.p2align 4,,10
	.p2align 3
.L3052:
	mov	QWORD PTR 80[rsp], 0
.L2892:
	mov	r10, QWORD PTR 80[rsp]
	cmp	BYTE PTR 48[rsp], 0
	je	.L3060
	test	rbp, rbp
	je	.L3061
	mov	QWORD PTR 72[rsp], 1
	mov	rax, r10
	sub	rax, r11
.L2902:
	sub	rbp, rax
	add	QWORD PTR 72[rsp], rbp
	jmp	.L2895
	.p2align 4,,10
	.p2align 3
.L3080:
	mov	ebp, 6
.L3151:
	mov	BYTE PTR 56[rsp], 69
	mov	r13d, 1
.L2849:
	mov	BYTE PTR 48[rsp], 0
	mov	r15d, 1
.L2853:
	mov	DWORD PTR 40[rsp], ebp
	lea	rax, 241[rsp]
	movaps	xmm3, xmm6
	lea	r12, 112[rsp]
	mov	DWORD PTR 32[rsp], r15d
	lea	r8, 368[rsp]
	mov	rdx, rax
	mov	rcx, r12
	mov	QWORD PTR 72[rsp], rax
	call	_ZSt8to_charsPcS_fSt12chars_formati
	mov	r14, QWORD PTR 112[rsp]
	cmp	DWORD PTR 120[rsp], 132
	je	.L3030
	lea	rax, 368[rsp]
	mov	r12, QWORD PTR 72[rsp]
	mov	QWORD PTR 64[rsp], rax
.L2858:
	test	r13b, r13b
	je	.L2860
	cmp	r12, r14
	je	.L2860
	mov	r13, QWORD PTR __imp_toupper[rip]
	mov	r15, r12
	.p2align 4
	.p2align 3
.L2888:
	movsx	ecx, BYTE PTR [r15]
	add	r15, 1
	call	r13
	mov	BYTE PTR -1[r15], al
	cmp	r15, r14
	jne	.L2888
	jmp	.L2860
	.p2align 4,,10
	.p2align 3
.L3081:
	mov	ebp, 6
.L2848:
	xor	r13d, r13d
.L2847:
	mov	BYTE PTR 56[rsp], 101
	mov	r15d, 2
	mov	BYTE PTR 48[rsp], 0
	jmp	.L2853
	.p2align 4,,10
	.p2align 3
.L3082:
	mov	ebp, 6
.L3152:
	mov	r13d, 1
	jmp	.L2847
	.p2align 4,,10
	.p2align 3
.L3083:
	mov	ebp, 6
.L2846:
	mov	BYTE PTR 56[rsp], 101
	xor	r13d, r13d
.L2844:
	mov	BYTE PTR 48[rsp], 1
	mov	r15d, 3
	jmp	.L2853
	.p2align 4,,10
	.p2align 3
.L3084:
	mov	ebp, 6
.L3153:
	mov	BYTE PTR 56[rsp], 69
	mov	r13d, 1
	jmp	.L2844
	.p2align 4,,10
	.p2align 3
.L2855:
	and	edx, 120
	mov	eax, 112
	cmp	dl, 16
	mov	edx, 101
	cmove	eax, edx
	xor	r13d, r13d
	mov	BYTE PTR 56[rsp], al
.L2856:
	mov	DWORD PTR 32[rsp], 4
	lea	r12, 112[rsp]
	movaps	xmm3, xmm6
	lea	r8, 368[rsp]
	lea	rdx, 241[rsp]
	mov	rcx, r12
	mov	ebp, 6
	call	_ZSt8to_charsPcS_fSt12chars_format
	mov	BYTE PTR 48[rsp], 0
	mov	r14, QWORD PTR 112[rsp]
	cmp	DWORD PTR 120[rsp], 132
	je	.L3044
.L3154:
	lea	rax, 368[rsp]
	lea	r12, 241[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L2858
	.p2align 4,,10
	.p2align 3
.L3036:
	and	edx, 120
	mov	eax, 112
	mov	r13d, 1
	cmp	dl, 16
	mov	edx, 80
	cmove	eax, edx
	mov	BYTE PTR 56[rsp], al
	jmp	.L2856
	.p2align 4,,10
	.p2align 3
.L3079:
	mov	ebp, 6
.L2850:
	mov	BYTE PTR 56[rsp], 101
	xor	r13d, r13d
	jmp	.L2849
	.p2align 4,,10
	.p2align 3
.L3174:
	mov	rcx, r15
	call	_ZNSt6localeC1Ev
	mov	BYTE PTR 32[rsi], 1
	jmp	.L2992
	.p2align 4,,10
	.p2align 3
.L3038:
	mov	BYTE PTR 56[rsp], 101
	mov	r15d, 3
	xor	r13d, r13d
	mov	BYTE PTR 48[rsp], 0
	jmp	.L2853
	.p2align 4,,10
	.p2align 3
.L3163:
	mov	BYTE PTR -1[r12], 43
	mov	r11d, 1
	movzx	r15d, BYTE PTR [rbx]
	sub	r12, 1
	jmp	.L2887
	.p2align 4,,10
	.p2align 3
.L3003:
	movzx	ecx, WORD PTR 4[rbx]
	mov	rdx, rsi
.LEHB56:
	call	_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0
	mov	r9, rax
	jmp	.L3002
	.p2align 4,,10
	.p2align 3
.L3177:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	r13, rsi
	jb	.L3008
	.p2align 4
	.p2align 3
.L3010:
	test	rsi, rsi
	je	.L3009
	mov	r8, rsi
	mov	rdx, r12
	call	memcpy
.L3009:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rsi
	add	r12, rsi
	sub	r13, rsi
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
.LEHE56:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	r13, rsi
	jnb	.L3010
	test	r13, r13
	je	.L3011
.L3008:
	mov	r8, r13
	mov	rdx, r12
	call	memcpy
	add	QWORD PTR 24[rbx], r13
	jmp	.L3011
	.p2align 4,,10
	.p2align 3
.L3165:
	cmp	r13, rax
	mov	r10, r13
	sete	al
	movzx	eax, al
	mov	QWORD PTR 72[rsp], rax
	cmp	BYTE PTR 48[rsp], 0
	jne	.L3181
.L3057:
	xor	ebp, ebp
	jmp	.L2895
	.p2align 4,,10
	.p2align 3
.L2893:
	movsx	edx, BYTE PTR 56[rsp]
	mov	r8, r13
	mov	rcx, r12
	mov	BYTE PTR 72[rsp], r11b
	call	memchr
	movzx	r11d, BYTE PTR 72[rsp]
	test	rax, rax
	je	.L3058
	sub	rax, r12
	cmp	rax, -1
	cmove	rax, r13
	mov	QWORD PTR 80[rsp], rax
	jmp	.L2892
	.p2align 4,,10
	.p2align 3
.L3060:
	mov	QWORD PTR 72[rsp], 1
	xor	ebp, ebp
	jmp	.L2901
.L2852:
	and	edx, 120
	mov	eax, 101
	cmp	dl, 16
	mov	edx, 112
	cmovne	eax, edx
	xor	r13d, r13d
	mov	BYTE PTR 56[rsp], al
.L2854:
	mov	DWORD PTR 40[rsp], ebp
	lea	r12, 112[rsp]
	movaps	xmm3, xmm6
	lea	r8, 368[rsp]
	mov	DWORD PTR 32[rsp], 4
	lea	rdx, 241[rsp]
	mov	rcx, r12
	call	_ZSt8to_charsPcS_fSt12chars_formati
	mov	r14, QWORD PTR 112[rsp]
	cmp	DWORD PTR 120[rsp], 132
	je	.L3034
	mov	BYTE PTR 48[rsp], 0
	jmp	.L3154
	.p2align 4,,10
	.p2align 3
.L2851:
	and	edx, 120
	mov	eax, 112
	mov	r13d, 1
	cmp	dl, 16
	mov	edx, 80
	cmove	eax, edx
	mov	BYTE PTR 56[rsp], al
	jmp	.L2854
.L3181:
	cmp	BYTE PTR [r12+r11], 48
	jne	.L2896
.L3156:
	mov	r9, -1
.L2897:
	mov	rax, r10
	sub	rax, r9
	jmp	.L2900
.L3058:
	mov	QWORD PTR 80[rsp], r13
	jmp	.L2892
.L3166:
	cmp	r15, 15
	jbe	.L2910
.L2909:
	movabs	rax, 9223372036854775806
	cmp	rax, r15
	jb	.L2911
	mov	QWORD PTR 64[rsp], r9
	mov	QWORD PTR 48[rsp], r10
	cmp	r15, 29
	ja	.L2912
	mov	ecx, 31
.LEHB57:
	call	_Znwy
	mov	r10, QWORD PTR 48[rsp]
	mov	r9, QWORD PTR 64[rsp]
	mov	r14, rax
	mov	rdx, rdi
	mov	r15d, 30
	jmp	.L2913
.L3168:
	mov	r9, QWORD PTR 152[rsp]
	mov	QWORD PTR 144[rsp], r14
	mov	QWORD PTR 160[rsp], r15
	test	r9, r9
	jne	.L2908
	.p2align 4
	.p2align 3
.L2910:
	movabs	rax, 9223372036854775806
	cmp	r13, r10
	mov	r14, r10
	cmovbe	r14, r13
	cmp	rax, r14
	jb	.L3182
	mov	r15, QWORD PTR 144[rsp]
	cmp	r15, rdi
	je	.L3183
	mov	rdx, QWORD PTR 160[rsp]
	cmp	rdx, r14
	jb	.L2929
.L2926:
	cmp	r12, r15
	je	.L2930
	test	r14, r14
	je	.L2932
	cmp	r14, 1
	je	.L3184
	mov	rcx, r15
	mov	r8, r14
	mov	rdx, r12
	mov	QWORD PTR 48[rsp], r10
	call	memcpy
	mov	r15, QWORD PTR 144[rsp]
	mov	r10, QWORD PTR 48[rsp]
.L2932:
	mov	QWORD PTR 152[rsp], r14
	mov	BYTE PTR [r15+r14], 0
	cmp	r10, QWORD PTR 80[rsp]
	je	.L3185
.L3159:
	test	rbp, rbp
	je	.L3161
	mov	r8, QWORD PTR 152[rsp]
	movabs	rax, 9223372036854775806
	mov	rdx, rax
	sub	rdx, r8
	cmp	rdx, rbp
	jb	.L3186
	mov	r15, QWORD PTR 144[rsp]
	lea	r14, [r8+rbp]
	cmp	r15, rdi
	je	.L3187
	mov	r9, QWORD PTR 160[rsp]
	cmp	r9, r14
	jb	.L3188
.L2948:
	lea	rcx, [r15+r8]
	cmp	rbp, 1
	je	.L3189
	mov	r8, rbp
	mov	edx, 48
	mov	QWORD PTR 48[rsp], r10
	call	memset
	mov	r10, QWORD PTR 48[rsp]
.L2961:
	mov	rax, QWORD PTR 144[rsp]
	mov	QWORD PTR 152[rsp], r14
	mov	BYTE PTR [rax+r14], 0
.L3161:
	cmp	r13, r10
	jb	.L3190
	mov	rdx, QWORD PTR 152[rsp]
	sub	r13, r10
	lea	r9, [r12+r10]
	movabs	rax, 9223372036854775806
	sub	rax, rdx
	cmp	rax, r13
	jb	.L3191
	mov	rax, QWORD PTR 144[rsp]
	mov	ecx, 15
	lea	rbp, 0[r13+rdx]
	cmp	rax, rdi
	cmovne	rcx, QWORD PTR 160[rsp]
	cmp	rcx, rbp
	jb	.L2965
	test	r13, r13
	je	.L2966
	lea	rcx, [rax+rdx]
	cmp	r13, 1
	je	.L3192
	mov	r8, r13
	mov	rdx, r9
	call	memcpy
	mov	rax, QWORD PTR 144[rsp]
.L2966:
	mov	QWORD PTR 152[rsp], rbp
	mov	BYTE PTR [rax+rbp], 0
	jmp	.L2968
	.p2align 4,,10
	.p2align 3
.L2903:
	mov	rdx, QWORD PTR 144[rsp]
	cmp	rdx, rdi
	je	.L3193
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, r15
	jnb	.L2908
	jmp	.L2914
.L3180:
	mov	rax, QWORD PTR 24[rcx]
	movzx	edx, BYTE PTR [r12]
	lea	r8, 1[rax]
	mov	QWORD PTR 24[rcx], r8
	mov	BYTE PTR [rax], dl
	mov	rax, QWORD PTR 24[rcx]
	sub	rax, QWORD PTR 8[rcx]
	cmp	rax, QWORD PTR 16[rcx]
	je	.L3194
.L3013:
	add	r12, 1
	lea	rax, -1[r13]
	mov	r8d, 2
	mov	edx, 48
	jmp	.L3012
.L3045:
	mov	BYTE PTR 48[rsp], 0
	xor	r13d, r13d
	xor	r15d, r15d
	mov	r14d, 14
	mov	BYTE PTR 56[rsp], 101
	mov	BYTE PTR 64[rsp], 0
.L2857:
	mov	r9, QWORD PTR 144[rsp]
	cmp	r14, 128
	jbe	.L3195
	cmp	r9, rdi
	je	.L3196
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, r14
	jb	.L3197
.L3029:
	cmp	r9, rdi
	je	.L3049
	mov	rax, QWORD PTR 160[rsp]
	lea	r14, [rax+rax]
	cmp	rax, r14
	jnb	.L2876
	movabs	rax, 9223372036854775806
	cmp	rax, r14
	jb	.L3198
	lea	rcx, 1[r14]
.L2875:
	mov	QWORD PTR 72[rsp], r9
	call	_Znwy
	mov	r11, rax
	mov	rax, QWORD PTR 152[rsp]
	mov	r9, QWORD PTR 72[rsp]
	test	rax, rax
	lea	r8, 1[rax]
	je	.L3199
	mov	rcx, r11
	mov	rdx, r9
	call	memcpy
	mov	r11, rax
.L2879:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rdi
	je	.L2880
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 72[rsp], r11
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r11, QWORD PTR 72[rsp]
.L2880:
	mov	QWORD PTR 144[rsp], r11
	mov	r9, r11
	mov	QWORD PTR 160[rsp], r14
.L2876:
	cmp	BYTE PTR 64[rsp], 0
	mov	QWORD PTR 72[rsp], r9
	lea	r8, -1[r9+r14]
	lea	rdx, 1[r9]
	jne	.L3200
	test	r15d, r15d
	je	.L2883
	mov	DWORD PTR 32[rsp], r15d
	movaps	xmm3, xmm6
	mov	rcx, r12
	call	_ZSt8to_charsPcS_fSt12chars_format
	mov	r10, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 72[rsp]
.L2882:
	mov	r14, r10
	test	eax, eax
	jne	.L2884
	mov	rdx, QWORD PTR 144[rsp]
	mov	rax, r10
	sub	rax, r9
	mov	QWORD PTR 152[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rax, QWORD PTR 144[rsp]
	lea	r12, 1[rax]
	add	rax, QWORD PTR 152[rsp]
	mov	QWORD PTR 64[rsp], rax
	jmp	.L2858
	.p2align 4,,10
	.p2align 3
.L2884:
	mov	rdx, QWORD PTR 144[rsp]
	mov	QWORD PTR 152[rsp], 0
	mov	BYTE PTR [rdx], 0
	mov	r9, QWORD PTR 144[rsp]
	cmp	eax, 132
	je	.L3029
	lea	r12, 1[r9]
	add	r9, QWORD PTR 152[rsp]
	mov	QWORD PTR 64[rsp], r9
	jmp	.L2858
.L2883:
	movaps	xmm3, xmm6
	mov	rcx, r12
	call	_ZSt8to_charsPcS_f
	mov	r10, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 72[rsp]
	jmp	.L2882
.L3044:
	mov	BYTE PTR 64[rsp], 0
	mov	r15d, 4
	mov	r14d, 14
	jmp	.L2857
.L3030:
	mov	BYTE PTR 64[rsp], 1
	lea	r14, 8[rbp]
	cmp	r15d, 2
	jne	.L2857
	lea	rdx, 208[rsp]
	movaps	xmm0, xmm6
	mov	DWORD PTR 208[rsp], 0
	call	frexpf
	mov	eax, DWORD PTR 208[rsp]
	test	eax, eax
	jle	.L2861
	imul	edx, eax, 4004
	mov	rax, rdx
	imul	rdx, rdx, 995517945
	shr	rdx, 32
	sub	eax, edx
	shr	eax
	add	eax, edx
	shr	eax, 13
	add	eax, 1
	add	r14, rax
.L2861:
	mov	BYTE PTR 64[rsp], 1
	jmp	.L2857
.L3200:
	mov	DWORD PTR 40[rsp], ebp
	movaps	xmm3, xmm6
	mov	rcx, r12
	mov	DWORD PTR 32[rsp], r15d
	call	_ZSt8to_charsPcS_fSt12chars_formati
	mov	r10, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
	mov	r9, QWORD PTR 72[rsp]
	jmp	.L2882
.L3197:
	movabs	rcx, 9223372036854775806
	cmp	rcx, r14
	jb	.L2866
	add	rax, rax
	cmp	r14, rax
	jnb	.L3033
	cmp	rcx, rax
	jnb	.L3032
	mov	r14, rcx
	mov	rdx, r9
	movabs	rcx, 9223372036854775807
.L2871:
	mov	QWORD PTR 72[rsp], rdx
	call	_Znwy
	mov	r9, rax
	mov	rax, QWORD PTR 152[rsp]
	mov	rdx, QWORD PTR 72[rsp]
	test	rax, rax
	lea	r8, 1[rax]
	je	.L3201
	mov	rcx, r9
	call	memcpy
	mov	r9, rax
.L2873:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rdi
	je	.L2874
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 72[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 72[rsp]
.L2874:
	mov	QWORD PTR 144[rsp], r9
	mov	QWORD PTR 160[rsp], r14
	jmp	.L3029
.L2904:
	mov	rcx, QWORD PTR 72[rsp]
	lea	r14, [r12+r10]
	mov	r8, r13
	mov	QWORD PTR 48[rsp], r10
	sub	r8, r10
	mov	rdx, r14
	add	rcx, r10
	add	rcx, r12
	call	memmove
	mov	r10, QWORD PTR 48[rsp]
	cmp	r10, QWORD PTR 80[rsp]
	jne	.L2922
	mov	BYTE PTR [r14], 46
	lea	r14, 1[r12+r10]
.L2922:
	mov	r8, rbp
	mov	edx, 48
	mov	rcx, r14
	mov	r13, r15
	call	memset
	jmp	.L2923
.L3175:
	mov	rax, QWORD PTR 208[rsp]
	lea	r14, 224[rsp]
	cmp	rax, r14
	je	.L3020
	mov	QWORD PTR 176[rsp], rax
	movq	xmm0, r8
	movhps	xmm0, QWORD PTR 224[rsp]
	movups	XMMWORD PTR 184[rsp], xmm0
.L2999:
	mov	QWORD PTR 208[rsp], r14
	lea	r14, 224[rsp]
	mov	rcx, r14
	jmp	.L2998
.L3061:
	mov	QWORD PTR 72[rsp], 1
	jmp	.L2901
.L3055:
	mov	r10, r13
	jmp	.L2898
.L3049:
	mov	ecx, 31
	mov	r14d, 30
	jmp	.L2875
.L3196:
	movabs	rax, 9223372036854775806
	cmp	rax, r14
	jb	.L2866
	lea	rcx, 1[r14]
	mov	rdx, rdi
	jmp	.L2871
.L3199:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [r11], al
	jmp	.L2879
.L3201:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [r9], al
	jmp	.L2873
.L2976:
	sub	r9, r10
	mov	rbp, r9
	cmp	rax, r13
	jb	.L2973
	add	r12, r12
	cmp	r13, r12
	jb	.L2980
.L2975:
	lea	rcx, 1[r13]
	mov	r12, r13
.L2981:
	mov	QWORD PTR 48[rsp], r10
	call	_Znwy
	mov	r10, QWORD PTR 48[rsp]
	mov	r15, rax
	test	r10, r10
	je	.L2982
	cmp	r10, 1
	je	.L3202
	mov	r8, r10
	mov	rdx, r14
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], r10
	call	memcpy
	mov	r14, QWORD PTR 144[rsp]
	mov	r10, QWORD PTR 48[rsp]
.L2982:
	test	rbp, rbp
	je	.L2984
	mov	rax, QWORD PTR 72[rsp]
	lea	rdx, [r14+r10]
	lea	rcx, [r10+rax]
	add	rcx, r15
	cmp	rbp, 1
	je	.L3203
	mov	r8, rbp
	mov	QWORD PTR 48[rsp], r10
	call	memcpy
	mov	r14, QWORD PTR 144[rsp]
	mov	r10, QWORD PTR 48[rsp]
.L2984:
	cmp	r14, rdi
	je	.L2986
	mov	rax, QWORD PTR 160[rsp]
	mov	rcx, r14
	mov	QWORD PTR 48[rsp], r10
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 48[rsp]
.L2986:
	mov	QWORD PTR 144[rsp], r15
	lea	rcx, [r15+r10]
	mov	QWORD PTR 160[rsp], r12
	jmp	.L2977
.L3167:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [r14], al
	jmp	.L2920
.L2965:
	mov	QWORD PTR 32[rsp], r13
	lea	rcx, 144[rsp]
	xor	r8d, r8d
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rax, QWORD PTR 144[rsp]
	jmp	.L2966
.L3195:
	cmp	r9, rdi
	je	.L3204
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, 255
	ja	.L3029
	add	rax, rax
	cmp	rax, 256
	jbe	.L3205
.L3032:
	lea	rcx, 1[rax]
	mov	rdx, r9
	mov	r14, rax
	jmp	.L2871
.L3020:
	cmp	r8, 1
	je	.L3206
	mov	rdx, r14
	call	memcpy
.L2997:
	mov	rax, QWORD PTR 216[rsp]
	mov	rdx, QWORD PTR 176[rsp]
	mov	QWORD PTR 184[rsp], rax
	mov	BYTE PTR [rdx+rax], 0
	mov	rcx, QWORD PTR 208[rsp]
	jmp	.L2998
.L3185:
	mov	r14, QWORD PTR 152[rsp]
	mov	rdx, QWORD PTR 144[rsp]
	lea	r9, 1[r14]
	cmp	rdx, rdi
	je	.L3207
	mov	r15, QWORD PTR 160[rsp]
	cmp	r15, r9
	jb	.L3208
.L2940:
	mov	BYTE PTR [rdx+r14], 46
	mov	rax, QWORD PTR 144[rsp]
	mov	QWORD PTR 152[rsp], r9
	mov	BYTE PTR 1[rax+r14], 0
	jmp	.L3159
.L3171:
	cmp	r13, 15
	jbe	.L2972
	sub	r9, r10
	mov	rbp, r9
	cmp	rax, r13
	jb	.L2973
	cmp	r13, 29
	ja	.L2975
	mov	r12d, 30
.L2974:
	lea	rcx, 1[r12]
	jmp	.L2981
.L3183:
	cmp	r14, 15
	jbe	.L2926
	cmp	r14, 29
	ja	.L2928
	mov	QWORD PTR 48[rsp], 30
.L2927:
	mov	rax, QWORD PTR 48[rsp]
	lea	rcx, 1[rax]
.L2935:
	mov	QWORD PTR 64[rsp], r10
	call	_Znwy
	mov	rcx, rax
	mov	r8, r14
	mov	rdx, r12
	mov	r15, rax
	call	memcpy
	mov	rcx, QWORD PTR 144[rsp]
	mov	r10, QWORD PTR 64[rsp]
	cmp	rcx, rdi
	je	.L2936
	mov	rax, QWORD PTR 160[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r10, QWORD PTR 64[rsp]
.L2936:
	mov	rax, QWORD PTR 48[rsp]
	mov	QWORD PTR 144[rsp], r15
	mov	QWORD PTR 160[rsp], rax
	jmp	.L2932
.L3173:
	mov	BYTE PTR [rcx], 48
	jmp	.L2988
.L3193:
	cmp	r15, 15
	jbe	.L2908
	jmp	.L2909
.L2929:
	add	rdx, rdx
	mov	QWORD PTR 48[rsp], rdx
	cmp	r14, rdx
	jb	.L2934
.L2928:
	mov	QWORD PTR 48[rsp], r14
	lea	rcx, 1[r14]
	jmp	.L2935
.L3188:
	cmp	rax, r14
	jb	.L2949
	add	r9, r9
	cmp	r14, r9
	jb	.L2953
.L2951:
	lea	rcx, 1[r14]
	mov	r9, r14
.L2954:
	mov	QWORD PTR 72[rsp], r9
	mov	QWORD PTR 64[rsp], r10
	mov	QWORD PTR 48[rsp], r8
	call	_Znwy
	mov	r8, QWORD PTR 48[rsp]
	mov	r10, QWORD PTR 64[rsp]
	mov	r11, rax
	mov	r9, QWORD PTR 72[rsp]
	test	r8, r8
	je	.L3158
	cmp	r8, 1
	je	.L3209
	mov	rdx, r15
	mov	rcx, rax
	mov	QWORD PTR 72[rsp], r9
	mov	QWORD PTR 64[rsp], r10
	mov	QWORD PTR 48[rsp], r8
	call	memcpy
	mov	r9, QWORD PTR 72[rsp]
	mov	r10, QWORD PTR 64[rsp]
	mov	r8, QWORD PTR 48[rsp]
	mov	r11, rax
.L2957:
	mov	r15, QWORD PTR 144[rsp]
.L3158:
	cmp	r15, rdi
	je	.L2959
	mov	rax, QWORD PTR 160[rsp]
	mov	rcx, r15
	mov	QWORD PTR 80[rsp], r11
	mov	QWORD PTR 72[rsp], r9
	lea	rdx, 1[rax]
	mov	QWORD PTR 64[rsp], r10
	mov	QWORD PTR 48[rsp], r8
	call	_ZdlPvy
	mov	r11, QWORD PTR 80[rsp]
	mov	r9, QWORD PTR 72[rsp]
	mov	r10, QWORD PTR 64[rsp]
	mov	r8, QWORD PTR 48[rsp]
.L2959:
	mov	QWORD PTR 144[rsp], r11
	mov	r15, r11
	mov	QWORD PTR 160[rsp], r9
	jmp	.L2948
.L3184:
	movzx	eax, BYTE PTR [r12]
	mov	BYTE PTR [r15], al
	mov	r15, QWORD PTR 144[rsp]
	jmp	.L2932
.L3172:
	movzx	edx, BYTE PTR [rcx]
	mov	BYTE PTR [rax], dl
	mov	rcx, QWORD PTR 144[rsp]
	add	rcx, r10
	jmp	.L2977
.L3192:
	movzx	eax, BYTE PTR [r9]
	mov	BYTE PTR [rcx], al
	mov	rax, QWORD PTR 144[rsp]
	jmp	.L2966
.L2912:
	lea	rcx, 1[r15]
	call	_Znwy
.LEHE57:
	mov	r10, QWORD PTR 48[rsp]
	mov	r9, QWORD PTR 64[rsp]
	mov	r14, rax
	mov	rdx, rdi
	jmp	.L2913
.L3187:
	cmp	r14, 15
	jbe	.L2948
	cmp	rax, r14
	jb	.L2949
	cmp	r14, 29
	ja	.L2951
	mov	r9d, 30
.L2950:
	lea	rcx, 1[r9]
	jmp	.L2954
.L2934:
	cmp	rax, QWORD PTR 48[rsp]
	jnb	.L2927
	movabs	rcx, 9223372036854775807
	mov	QWORD PTR 48[rsp], rax
	jmp	.L2935
.L3189:
	mov	BYTE PTR [rcx], 48
	jmp	.L2961
.L3194:
	mov	rax, QWORD PTR [rcx]
	mov	QWORD PTR 56[rsp], r9
	mov	QWORD PTR 48[rsp], rcx
.LEHB58:
	call	[QWORD PTR [rax]]
.LEHE58:
	mov	r9, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 48[rsp]
	jmp	.L3013
.L2980:
	cmp	rax, r12
	jnb	.L2974
	movabs	rcx, 9223372036854775807
	mov	r12, rax
	jmp	.L2981
.L3206:
	movzx	eax, BYTE PTR 224[rsp]
	mov	BYTE PTR [rcx], al
	jmp	.L2997
.L3202:
	movzx	eax, BYTE PTR [r14]
	mov	BYTE PTR [r15], al
	mov	r14, QWORD PTR 144[rsp]
	jmp	.L2982
.L3203:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rcx], al
	mov	r14, QWORD PTR 144[rsp]
	jmp	.L2984
.L3208:
	movabs	rcx, 9223372036854775807
	cmp	r9, rcx
	je	.L3210
	add	r15, r15
	cmp	r9, r15
	jb	.L2942
	lea	rcx, 2[r14]
	mov	r15, r9
.L2943:
	mov	QWORD PTR 80[rsp], r9
	mov	QWORD PTR 72[rsp], rdx
	mov	QWORD PTR 64[rsp], r10
.LEHB59:
	call	_Znwy
	mov	rdx, QWORD PTR 72[rsp]
	mov	rcx, rax
	mov	r8, r14
	mov	QWORD PTR 48[rsp], rax
	call	memcpy
	mov	r10, QWORD PTR 64[rsp]
	mov	r9, QWORD PTR 80[rsp]
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rdi
	je	.L2944
	mov	rax, QWORD PTR 160[rsp]
	mov	QWORD PTR 72[rsp], r9
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 72[rsp]
	mov	r10, QWORD PTR 64[rsp]
.L2944:
	mov	rax, QWORD PTR 48[rsp]
	mov	QWORD PTR 160[rsp], r15
	mov	QWORD PTR 144[rsp], rax
	mov	rdx, rax
	jmp	.L2940
.L3204:
	mov	ecx, 257
	mov	rdx, rdi
	mov	r14d, 256
	jmp	.L2871
.L3207:
	cmp	r9, 16
	jne	.L2940
	mov	r15d, 30
.L2939:
	lea	rcx, 1[r15]
	jmp	.L2943
.L2953:
	cmp	rax, r9
	jnb	.L2950
	movabs	rcx, 9223372036854775807
	mov	r9, rax
	jmp	.L2954
.L3209:
	movzx	eax, BYTE PTR [r15]
	mov	BYTE PTR [r11], al
	jmp	.L2957
.L2942:
	movabs	rax, 9223372036854775806
	cmp	rax, r15
	jnb	.L2939
	mov	r15, rax
	jmp	.L2943
.L3034:
	mov	BYTE PTR 48[rsp], 0
	lea	r14, 8[rbp]
	mov	r15d, 4
	mov	BYTE PTR 64[rsp], 1
	jmp	.L2857
.L3205:
	mov	r14d, 256
.L3033:
	lea	rcx, 1[r14]
	mov	rdx, r9
	jmp	.L2871
.L2866:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2973:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2930:
	xor	eax, eax
	mov	QWORD PTR 32[rsp], r14
	mov	r9, r12
	xor	r8d, r8d
	mov	QWORD PTR 40[rsp], rax
	lea	rcx, 144[rsp]
	mov	rdx, r12
	mov	QWORD PTR 48[rsp], r10
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	r10, QWORD PTR 48[rsp]
	mov	r15, QWORD PTR 144[rsp]
	jmp	.L2932
.L2843:
.L3088:
	mov	rbx, rax
	jmp	.L3017
.L3169:
	mov	r8, r10
	lea	rdx, .LC37[rip]
	lea	rcx, .LC38[rip]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.LEHE59:
.L3086:
	mov	rbx, rax
	jmp	.L3018
.L3087:
	mov	rbx, rax
.L3016:
	lea	rcx, 136[rsp]
	call	_ZNSt6localeD1Ev
.L3017:
	lea	rcx, 176[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L3018:
	lea	rcx, 144[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB60:
	call	_Unwind_Resume
.LEHE60:
.L3170:
	lea	rcx, .LC20[rip]
.LEHB61:
	call	_ZSt20__throw_length_errorPKc
.L3210:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L2949:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L3182:
	lea	rcx, .LC34[rip]
	call	_ZSt20__throw_length_errorPKc
.L3191:
	lea	rcx, .LC14[rip]
	call	_ZSt20__throw_length_errorPKc
.L3186:
	lea	rcx, .LC20[rip]
	call	_ZSt20__throw_length_errorPKc
.L3198:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
.L3190:
	mov	r9, r13
	mov	r8, r10
	lea	rdx, .LC35[rip]
	lea	rcx, .LC36[rip]
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L2911:
	lea	rcx, .LC13[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
.LEHE61:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5603:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5603-.LLSDACSB5603
.LLSDACSB5603:
	.uleb128 .LEHB52-.LFB5603
	.uleb128 .LEHE52-.LEHB52
	.uleb128 .L3086-.LFB5603
	.uleb128 0
	.uleb128 .LEHB53-.LFB5603
	.uleb128 .LEHE53-.LEHB53
	.uleb128 .L3087-.LFB5603
	.uleb128 0
	.uleb128 .LEHB54-.LFB5603
	.uleb128 .LEHE54-.LEHB54
	.uleb128 .L3088-.LFB5603
	.uleb128 0
	.uleb128 .LEHB55-.LFB5603
	.uleb128 .LEHE55-.LEHB55
	.uleb128 .L3086-.LFB5603
	.uleb128 0
	.uleb128 .LEHB56-.LFB5603
	.uleb128 .LEHE56-.LEHB56
	.uleb128 .L3088-.LFB5603
	.uleb128 0
	.uleb128 .LEHB57-.LFB5603
	.uleb128 .LEHE57-.LEHB57
	.uleb128 .L3086-.LFB5603
	.uleb128 0
	.uleb128 .LEHB58-.LFB5603
	.uleb128 .LEHE58-.LEHB58
	.uleb128 .L3088-.LFB5603
	.uleb128 0
	.uleb128 .LEHB59-.LFB5603
	.uleb128 .LEHE59-.LEHB59
	.uleb128 .L3086-.LFB5603
	.uleb128 0
	.uleb128 .LEHB60-.LFB5603
	.uleb128 .LEHE60-.LEHB60
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB61-.LFB5603
	.uleb128 .LEHE61-.LEHB61
	.uleb128 .L3086-.LFB5603
	.uleb128 0
.LLSDACSE5603:
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt8__format18__write_escape_seqINS_10_Sink_iterIcEEcEET_S3_jSt17basic_string_viewIT0_St11char_traitsIS5_EE,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format18__write_escape_seqINS_10_Sink_iterIcEEcEET_S3_jSt17basic_string_viewIT0_St11char_traitsIS5_EE
	.def	_ZNSt8__format18__write_escape_seqINS_10_Sink_iterIcEEcEET_S3_jSt17basic_string_viewIT0_St11char_traitsIS5_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format18__write_escape_seqINS_10_Sink_iterIcEEcEET_S3_jSt17basic_string_viewIT0_St11char_traitsIS5_EE
_ZNSt8__format18__write_escape_seqINS_10_Sink_iterIcEEcEET_S3_jSt17basic_string_viewIT0_St11char_traitsIS5_EE:
.LFB6036:
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
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	rbp, QWORD PTR [r8]
	mov	r8, QWORD PTR 8[r8]
	mov	eax, edx
	mov	rbx, rcx
	test	eax, eax
	jne	.L3212
	mov	BYTE PTR 40[rsp], 48
	mov	rcx, QWORD PTR 24[rbx]
	mov	edi, 1
	test	rbp, rbp
	jne	.L3252
.L3218:
	lea	rax, 1[rcx]
	mov	QWORD PTR 24[rbx], rax
	mov	BYTE PTR [rcx], 123
	mov	rcx, QWORD PTR 24[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	cmp	rax, QWORD PTR 16[rbx]
	je	.L3253
.L3223:
	test	rdi, rdi
	jne	.L3254
.L3224:
	lea	rax, 1[rcx]
	mov	QWORD PTR 24[rbx], rax
	mov	BYTE PTR [rcx], 125
	mov	rax, QWORD PTR 24[rbx]
	sub	rax, QWORD PTR 8[rbx]
	cmp	rax, QWORD PTR 16[rbx]
	je	.L3255
	mov	rax, rbx
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L3212:
	movabs	rcx, 7378413942531504440
	bsr	edx, eax
	lea	edi, 4[rdx]
	mov	QWORD PTR 56[rsp], rcx
	movabs	rdx, 3978425819141910832
	mov	QWORD PTR 48[rsp], rdx
	shr	edi, 2
	cmp	eax, 255
	jbe	.L3214
	lea	edx, -1[rdi]
	.p2align 6
	.p2align 4
	.p2align 3
.L3215:
	mov	r9d, eax
	mov	ecx, edx
	and	r9d, 15
	movzx	r9d, BYTE PTR 48[rsp+r9]
	mov	BYTE PTR 40[rsp+rcx], r9b
	mov	ecx, eax
	lea	r9d, -1[rdx]
	shr	eax, 8
	shr	ecx, 4
	sub	edx, 2
	and	ecx, 15
	movzx	ecx, BYTE PTR 48[rsp+rcx]
	mov	BYTE PTR 40[rsp+r9], cl
	cmp	eax, 255
	ja	.L3215
.L3214:
	cmp	eax, 15
	jbe	.L3216
	mov	edx, eax
	shr	eax, 4
	and	edx, 15
	movzx	edx, BYTE PTR 48[rsp+rdx]
	mov	BYTE PTR 41[rsp], dl
	movzx	eax, BYTE PTR 48[rsp+rax]
.L3217:
	mov	BYTE PTR 40[rsp], al
	mov	rcx, QWORD PTR 24[rbx]
	test	rbp, rbp
	je	.L3218
.L3252:
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	mov	r12, r8
	sub	rsi, rax
	cmp	rbp, rsi
	jb	.L3219
	.p2align 4
	.p2align 3
.L3221:
	test	rsi, rsi
	je	.L3220
	mov	r8, rsi
	mov	rdx, r12
	call	memcpy
.L3220:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rsi
	mov	rcx, rbx
	add	r12, rsi
	sub	rbp, rsi
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	rbp, rsi
	jnb	.L3221
	test	rbp, rbp
	je	.L3218
.L3219:
	mov	r8, rbp
	mov	rdx, r12
	call	memcpy
	mov	rcx, QWORD PTR 24[rbx]
	add	rcx, rbp
	jmp	.L3218
	.p2align 4,,10
	.p2align 3
.L3254:
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	lea	rbp, 40[rsp]
	sub	rsi, rax
	cmp	rdi, rsi
	jb	.L3225
	.p2align 4
	.p2align 3
.L3227:
	test	rsi, rsi
	je	.L3226
	mov	r8, rsi
	mov	rdx, rbp
	call	memcpy
.L3226:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rsi
	mov	rcx, rbx
	add	rbp, rsi
	sub	rdi, rsi
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	rdi, rsi
	jnb	.L3227
	test	rdi, rdi
	je	.L3224
.L3225:
	mov	r8, rdi
	mov	rdx, rbp
	call	memcpy
	add	rdi, QWORD PTR 24[rbx]
	mov	rcx, rdi
	jmp	.L3224
	.p2align 4,,10
	.p2align 3
.L3216:
	movzx	eax, BYTE PTR 48[rsp+rax]
	jmp	.L3217
	.p2align 4,,10
	.p2align 3
.L3255:
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
	mov	rax, rbx
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L3253:
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	jmp	.L3223
	.seh_endproc
	.section .rdata,"dr"
.LC44:
	.ascii "\11\\t\12\\n\15\\r\\\\\\\"\\\"'\\'\\u\\x\0"
	.section	.text$_ZNSt8__format20__write_escaped_charINS_10_Sink_iterIcEEcEET_S3_T0_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format20__write_escaped_charINS_10_Sink_iterIcEEcEET_S3_T0_
	.def	_ZNSt8__format20__write_escaped_charINS_10_Sink_iterIcEEcEET_S3_T0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format20__write_escaped_charINS_10_Sink_iterIcEEcEET_S3_T0_
_ZNSt8__format20__write_escaped_charINS_10_Sink_iterIcEEcEET_S3_T0_:
.LFB6035:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	rbx, rcx
	cmp	dl, 39
	jg	.L3257
	cmp	dl, 8
	jle	.L3258
	lea	eax, -9[rdx]
	cmp	al, 30
	ja	.L3258
	lea	rcx, .L3260[rip]
	movzx	eax, al
	movsxd	rax, DWORD PTR [rcx+rax*4]
	add	rax, rcx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L3260:
	.long	.L3264-.L3260
	.long	.L3263-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3262-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3261-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3258-.L3260
	.long	.L3259-.L3260
	.section	.text$_ZNSt8__format20__write_escaped_charINS_10_Sink_iterIcEEcEET_S3_T0_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L3257:
	cmp	dl, 92
	jne	.L3258
	mov	rcx, QWORD PTR 24[rcx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	r8, 2
	ja	.L3294
	lea	rdi, .LC44[rip+10]
	mov	esi, 2
.L3281:
	test	r8, r8
	je	.L3280
	mov	rdx, rdi
	mov	QWORD PTR 40[rsp], r8
	call	memcpy
	mov	r8, QWORD PTR 40[rsp]
.L3280:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r8
	add	rdi, r8
	sub	rsi, r8
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	rsi, r8
	jnb	.L3281
	.p2align 4
	.p2align 3
.L3340:
	test	rsi, rsi
	jne	.L3287
.L3290:
	mov	rax, rbx
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L3258:
	lea	rax, .LC44[rip+18]
	movzx	edx, dl
	lea	r8, 48[rsp]
	mov	rcx, rbx
	mov	QWORD PTR 48[rsp], 2
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format18__write_escape_seqINS_10_Sink_iterIcEEcEET_S3_jSt17basic_string_viewIT0_St11char_traitsIS5_EE
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L3264:
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	r8, 2
	ja	.L3291
	lea	rdi, .LC44[rip+1]
	mov	esi, 2
.L3268:
	test	r8, r8
	je	.L3267
	mov	rdx, rdi
	mov	QWORD PTR 40[rsp], r8
	call	memcpy
	mov	r8, QWORD PTR 40[rsp]
.L3267:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r8
	add	rdi, r8
	sub	rsi, r8
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	rsi, r8
	jnb	.L3268
	jmp	.L3340
	.p2align 4,,10
	.p2align 3
.L3259:
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	esi, 2
	lea	rdi, .LC44[rip+16]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	r8, 2
	ja	.L3287
.L3289:
	test	r8, r8
	je	.L3288
	mov	rdx, rdi
	mov	QWORD PTR 40[rsp], r8
	call	memcpy
	mov	r8, QWORD PTR 40[rsp]
.L3288:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r8
	add	rdi, r8
	sub	rsi, r8
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	rsi, r8
	jnb	.L3289
	jmp	.L3340
	.p2align 4,,10
	.p2align 3
.L3261:
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	esi, 2
	lea	rdi, .LC44[rip+13]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	r8, 2
	ja	.L3287
.L3285:
	test	r8, r8
	je	.L3284
	mov	rdx, rdi
	mov	QWORD PTR 40[rsp], r8
	call	memcpy
	mov	r8, QWORD PTR 40[rsp]
.L3284:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r8
	add	rdi, r8
	sub	rsi, r8
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	rsi, r8
	jnb	.L3285
	jmp	.L3340
	.p2align 4,,10
	.p2align 3
.L3262:
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	r8, 2
	ja	.L3293
	lea	rdi, .LC44[rip+7]
	mov	esi, 2
.L3277:
	test	r8, r8
	je	.L3276
	mov	rdx, rdi
	mov	QWORD PTR 40[rsp], r8
	call	memcpy
	mov	r8, QWORD PTR 40[rsp]
.L3276:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r8
	add	rdi, r8
	sub	rsi, r8
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	rsi, r8
	jnb	.L3277
	jmp	.L3340
	.p2align 4,,10
	.p2align 3
.L3263:
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	esi, 2
	lea	rdi, .LC44[rip+4]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	r8, 2
	ja	.L3287
.L3273:
	test	r8, r8
	je	.L3272
	mov	rdx, rdi
	mov	QWORD PTR 40[rsp], r8
	call	memcpy
	mov	r8, QWORD PTR 40[rsp]
.L3272:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], r8
	add	rdi, r8
	sub	rsi, r8
	mov	rcx, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	r8, rax
	cmp	rsi, r8
	jnb	.L3273
	jmp	.L3340
	.p2align 4,,10
	.p2align 3
.L3294:
	mov	esi, 2
	lea	rdi, .LC44[rip+10]
	.p2align 4
	.p2align 3
.L3287:
	mov	r8, rsi
	mov	rdx, rdi
	call	memcpy
	add	QWORD PTR 24[rbx], rsi
	jmp	.L3290
	.p2align 4,,10
	.p2align 3
.L3293:
	mov	esi, 2
	lea	rdi, .LC44[rip+7]
	jmp	.L3287
	.p2align 4,,10
	.p2align 3
.L3291:
	mov	esi, 2
	lea	rdi, .LC44[rip+1]
	jmp	.L3287
	.seh_endproc
	.section .rdata,"dr"
.LC45:
	.ascii "\357\277\275\0"
	.section	.text$_ZNSt8__format23__write_escaped_unicodeIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format23__write_escaped_unicodeIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE
	.def	_ZNSt8__format23__write_escaped_unicodeIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format23__write_escaped_unicodeIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE
_ZNSt8__format23__write_escaped_unicodeIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE:
.LFB5903:
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
	sub	rsp, 184
	.seh_stackalloc	184
	.seh_endprologue
	mov	rax, QWORD PTR 8[rdx]
	mov	r14, QWORD PTR [rdx]
	xor	edx, edx
	movq	xmm0, rax
	add	r14, rax
	punpcklqdq	xmm0, xmm0
	mov	DWORD PTR 44[rsp], r8d
	mov	rsi, rcx
	mov	WORD PTR 104[rsp], dx
	mov	BYTE PTR 106[rsp], 0
	mov	QWORD PTR 112[rsp], r14
	movups	XMMWORD PTR 88[rsp], xmm0
	cmp	rax, r14
	je	.L3414
	lea	rax, 80[rsp]
	mov	rcx, rax
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	r15, QWORD PTR 96[rsp]
	cmp	BYTE PTR 104[rsp], 0
	sete	dl
	cmp	r14, r15
	sete	al
	test	dl, al
	jne	.L3414
	.p2align 4
	.p2align 3
.L3347:
	mov	rax, QWORD PTR 96[rsp]
	movdqa	xmm1, XMMWORD PTR 80[rsp]
	mov	rbx, rax
	mov	QWORD PTR 144[rsp], rax
	mov	rax, QWORD PTR 104[rsp]
	movaps	XMMWORD PTR 128[rsp], xmm1
	mov	QWORD PTR 152[rsp], rax
	movzx	ebp, BYTE PTR 152[rsp]
	mov	rax, QWORD PTR 112[rsp]
	test	bpl, bpl
	sete	r12b
	cmp	rbx, r14
	mov	QWORD PTR 160[rsp], rax
	sete	al
	and	r12b, al
	jne	.L3394
	mov	r8d, 1
	jmp	.L3395
	.p2align 4,,10
	.p2align 3
.L3438:
	movzx	eax, BYTE PTR [rbx]
	cmp	al, 34
	je	.L3351
	jle	.L3434
	cmp	BYTE PTR 44[rsp], 15
	sete	dl
	cmp	al, 39
	jne	.L3435
.L3356:
	test	dl, dl
	jne	.L3407
.L3357:
	movzx	eax, bpl
	movzx	edx, BYTE PTR 153[rsp]
	add	eax, 1
	cmp	eax, edx
	je	.L3436
	jge	.L3437
	add	ebp, 1
	mov	rbx, QWORD PTR 144[rsp]
	mov	BYTE PTR 152[rsp], bpl
.L3376:
	xor	r8d, r8d
.L3395:
	movzx	eax, bpl
	mov	ecx, DWORD PTR 128[rsp+rax*4]
	cmp	ecx, 127
	jbe	.L3438
	lea	r10d, 2[rcx+rcx]
	mov	eax, 1473
	lea	r9, _ZNSt9__unicode9__v16_0_014__escape_edgesE[rip]
	.p2align 4
	.p2align 3
.L3359:
	test	rax, rax
	jle	.L3439
.L3360:
	mov	rdx, rax
	sar	rdx
	cmp	DWORD PTR [r9+rdx*4], r10d
	jnb	.L3402
	sub	rax, rdx
	lea	r9, 4[r9+rdx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3360
.L3439:
	mov	r13d, DWORD PTR -4[r9]
	and	r13d, 1
	jne	.L3349
	test	r8b, r8b
	je	.L3361
	mov	r11d, ecx
	mov	eax, 1717
	lea	r10, _ZNSt9__unicode9__v16_0_011__gcb_edgesE[rip]
	sal	r11d, 4
	or	r11d, 15
	.p2align 4
	.p2align 3
.L3363:
	test	rax, rax
	jle	.L3440
.L3364:
	mov	rdx, rax
	sar	rdx
	cmp	DWORD PTR [r10+rdx*4], r11d
	jnb	.L3403
	sub	rax, rdx
	lea	r10, 4[r10+rdx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3364
.L3440:
	mov	eax, DWORD PTR -4[r10]
	and	eax, 15
	cmp	eax, 4
	je	.L3404
.L3361:
	cmp	ecx, 65533
	jne	.L3357
	cmp	BYTE PTR 154[rsp], 3
	je	.L3441
.L3405:
	xor	r12d, r12d
	.p2align 4
	.p2align 3
.L3349:
	cmp	r15, rbx
	je	.L3367
.L3396:
	mov	rcx, QWORD PTR 24[rsi]
	mov	r8, QWORD PTR 16[rsi]
	mov	rdi, rbx
	sub	rdi, r15
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	r8, rax
	cmp	rdi, r8
	jb	.L3369
	mov	QWORD PTR 48[rsp], rbx
	mov	rbx, r8
.L3368:
	test	rbx, rbx
	je	.L3377
	mov	r8, rbx
	mov	rdx, r15
	call	memcpy
.L3377:
	mov	rax, QWORD PTR [rsi]
	add	QWORD PTR 24[rsi], rbx
	mov	rcx, rsi
	add	r15, rbx
	sub	rdi, rbx
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rsi]
	mov	rbx, QWORD PTR 16[rsi]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rsi]
	sub	rbx, rax
	cmp	rdi, rbx
	jnb	.L3368
	mov	rbx, QWORD PTR 48[rsp]
	test	rdi, rdi
	jne	.L3369
.L3367:
	cmp	r14, rbx
	jne	.L3408
	test	bpl, bpl
	je	.L3414
.L3408:
	movdqa	xmm2, XMMWORD PTR 128[rsp]
	mov	rax, QWORD PTR 160[rsp]
	movdqa	xmm3, XMMWORD PTR 144[rsp]
	mov	QWORD PTR 112[rsp], rax
	movaps	XMMWORD PTR 80[rsp], xmm2
	movaps	XMMWORD PTR 96[rsp], xmm3
	test	r12b, r12b
	jne	.L3442
	test	r13b, r13b
	je	.L3385
	movzx	ebp, bpl
	lea	rax, .LC44[rip+18]
	mov	rcx, rsi
	mov	edx, DWORD PTR 80[rsp+rbp*4]
	lea	r8, 64[rsp]
	mov	QWORD PTR 72[rsp], rax
	mov	QWORD PTR 64[rsp], 2
	call	_ZNSt8__format18__write_escape_seqINS_10_Sink_iterIcEEcEET_S3_jSt17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	rsi, rax
.L3384:
	movzx	eax, BYTE PTR 104[rsp]
	movzx	ecx, BYTE PTR 105[rsp]
	mov	r15, QWORD PTR 96[rsp]
	mov	edx, eax
	add	eax, 1
	cmp	eax, ecx
	je	.L3443
	jge	.L3444
	add	edx, 1
	mov	BYTE PTR 104[rsp], dl
	jmp	.L3347
	.p2align 4,,10
	.p2align 3
.L3402:
	mov	rax, rdx
	jmp	.L3359
	.p2align 4,,10
	.p2align 3
.L3403:
	mov	rax, rdx
	jmp	.L3363
	.p2align 4,,10
	.p2align 3
.L3436:
	mov	rax, QWORD PTR 160[rsp]
	cmp	rax, rbx
	je	.L3371
	movzx	edx, BYTE PTR 154[rsp]
	add	rbx, rdx
	mov	QWORD PTR 144[rsp], rbx
	cmp	rax, rbx
	je	.L3445
	lea	rcx, 128[rsp]
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
.L3371:
	movzx	ebp, BYTE PTR 152[rsp]
	mov	rbx, QWORD PTR 144[rsp]
	test	bpl, bpl
	sete	al
	cmp	rbx, r14
	sete	dl
	and	eax, edx
.L3375:
	test	al, al
	je	.L3376
.L3406:
	xor	r13d, r13d
	xor	ebp, ebp
	jmp	.L3349
	.p2align 4,,10
	.p2align 3
.L3437:
	mov	rbx, QWORD PTR 144[rsp]
	movzx	ebp, BYTE PTR 152[rsp]
	cmp	rbx, r14
	sete	al
	test	bpl, bpl
	sete	dl
	and	eax, edx
	jmp	.L3375
	.p2align 4,,10
	.p2align 3
.L3434:
	cmp	al, 10
	jg	.L3353
	cmp	al, 8
	jle	.L3354
.L3400:
	xor	r13d, r13d
	mov	r12d, 1
	jmp	.L3349
	.p2align 4,,10
	.p2align 3
.L3351:
	cmp	BYTE PTR 44[rsp], 12
	sete	dl
	jmp	.L3356
	.p2align 4,,10
	.p2align 3
.L3435:
	cmp	al, 92
	je	.L3400
.L3354:
	cmp	al, 31
	setbe	dl
	cmp	al, 127
	sete	al
	or	dl, al
	je	.L3357
.L3407:
	xor	r13d, r13d
	mov	r12d, edx
	jmp	.L3349
	.p2align 4,,10
	.p2align 3
.L3445:
	mov	BYTE PTR 152[rsp], 0
	cmp	r14, rbx
	je	.L3406
	xor	ebp, ebp
	jmp	.L3376
	.p2align 4,,10
	.p2align 3
.L3404:
	xor	r12d, r12d
	mov	r13d, r8d
	jmp	.L3349
	.p2align 4,,10
	.p2align 3
.L3353:
	cmp	al, 13
	je	.L3400
	cmp	al, 31
	setbe	dl
	cmp	al, 127
	sete	al
	or	dl, al
	je	.L3357
	jmp	.L3407
	.p2align 4,,10
	.p2align 3
.L3443:
	mov	rax, QWORD PTR 112[rsp]
	cmp	rax, r15
	je	.L3446
	movzx	edx, BYTE PTR 106[rsp]
	add	r15, rdx
	mov	QWORD PTR 96[rsp], r15
	cmp	rax, r15
	je	.L3447
	mov	rcx, QWORD PTR 56[rsp]
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	r15, QWORD PTR 96[rsp]
	cmp	BYTE PTR 104[rsp], 0
	sete	al
	cmp	r15, r14
	sete	dl
	and	eax, edx
	test	al, al
	je	.L3347
.L3414:
	mov	rax, rsi
	add	rsp, 184
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
.L3442:
	movsx	edx, BYTE PTR [rbx]
	mov	rcx, rsi
	call	_ZNSt8__format20__write_escaped_charINS_10_Sink_iterIcEEcEET_S3_T0_
	mov	rsi, rax
	jmp	.L3384
.L3385:
	movzx	r12d, BYTE PTR 106[rsp]
	add	r12, rbx
	cmp	r12, rbx
	je	.L3384
	lea	rbp, 64[rsp]
	mov	rcx, rsi
	.p2align 4
	.p2align 3
.L3386:
	movzx	edx, BYTE PTR [rbx]
	lea	rax, .LC44[rip+20]
	mov	r8, rbp
	add	rbx, 1
	mov	QWORD PTR 64[rsp], 2
	mov	QWORD PTR 72[rsp], rax
	call	_ZNSt8__format18__write_escape_seqINS_10_Sink_iterIcEEcEET_S3_jSt17basic_string_viewIT0_St11char_traitsIS5_EE
	mov	rcx, rax
	cmp	r12, rbx
	jne	.L3386
	mov	rsi, rax
	jmp	.L3384
.L3444:
	cmp	r14, r15
	sete	al
	test	dl, dl
	sete	dl
	and	eax, edx
.L3389:
	test	al, al
	je	.L3347
	jmp	.L3414
.L3441:
	cmp	WORD PTR [rbx], -16401
	jne	.L3405
	cmp	BYTE PTR 2[rbx], -67
	jne	.L3405
	jmp	.L3357
.L3446:
	test	dl, dl
	sete	al
	cmp	r14, r15
	sete	dl
	and	eax, edx
	jmp	.L3389
.L3447:
	cmp	r14, r15
	mov	BYTE PTR 104[rsp], 0
	sete	al
	jmp	.L3389
.L3394:
	cmp	rbx, r15
	je	.L3414
	xor	r13d, r13d
	xor	r12d, r12d
	xor	ebp, ebp
	jmp	.L3396
.L3369:
	mov	r8, rdi
	mov	rdx, r15
	call	memcpy
	add	QWORD PTR 24[rsi], rdi
	jmp	.L3367
	.seh_endproc
	.section	.text$_ZNSt8__format15__write_escapedIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format15__write_escapedIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE
	.def	_ZNSt8__format15__write_escapedIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format15__write_escapedIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE
_ZNSt8__format15__write_escapedIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE:
.LFB5747:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	r10, QWORD PTR [rdx]
	mov	r11, QWORD PTR 8[rdx]
	lea	rdx, .LC44[rip]
	movzx	eax, r8b
	movzx	ebx, BYTE PTR [rdx+rax]
	mov	rax, QWORD PTR 24[rcx]
	lea	rdx, 1[rax]
	mov	QWORD PTR 24[rcx], rdx
	mov	BYTE PTR [rax], bl
	mov	rax, QWORD PTR 24[rcx]
	sub	rax, QWORD PTR 8[rcx]
	cmp	rax, QWORD PTR 16[rcx]
	je	.L3451
.L3449:
	lea	rdx, 64[rsp]
	mov	QWORD PTR 64[rsp], r10
	mov	QWORD PTR 72[rsp], r11
	call	_ZNSt8__format23__write_escaped_unicodeIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE
	mov	rdx, QWORD PTR 24[rax]
	lea	rcx, 1[rdx]
	mov	QWORD PTR 24[rax], rcx
	mov	BYTE PTR [rdx], bl
	mov	rdx, QWORD PTR 24[rax]
	sub	rdx, QWORD PTR 8[rax]
	cmp	rdx, QWORD PTR 16[rax]
	je	.L3452
	add	rsp, 80
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L3451:
	mov	rax, QWORD PTR [rcx]
	mov	DWORD PTR 60[rsp], r8d
	mov	QWORD PTR 32[rsp], r10
	mov	QWORD PTR 40[rsp], r11
	mov	QWORD PTR 96[rsp], rcx
	call	[QWORD PTR [rax]]
	mov	r8d, DWORD PTR 60[rsp]
	mov	r10, QWORD PTR 32[rsp]
	mov	r11, QWORD PTR 40[rsp]
	mov	rcx, QWORD PTR 96[rsp]
	jmp	.L3449
	.p2align 4,,10
	.p2align 3
.L3452:
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 32[rsp], rax
	mov	rcx, rax
	call	[QWORD PTR [rdx]]
	mov	rax, QWORD PTR 32[rsp]
	add	rsp, 80
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC46:
	.ascii "format error: format-spec contains invalid formatting options for 'charT'\0"
	.section	.text$_ZZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEyENKUlRT_E_clIcEEDaS5_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEyENKUlRT_E_clIcEEDaS5_
	.def	_ZZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEyENKUlRT_E_clIcEEDaS5_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEyENKUlRT_E_clIcEEDaS5_
_ZZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEyENKUlRT_E_clIcEEDaS5_:
.LFB5268:
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
	mov	r8d, 7
	mov	rdi, QWORD PTR [rcx]
	lea	rbp, 72[rsp]
	mov	rbx, rcx
	mov	rsi, rdx
	mov	QWORD PTR 72[rsp], 0
	lea	rdx, 8[rdi]
	mov	rcx, rbp
	mov	DWORD PTR 80[rsp], 32
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	rdx, rax
	movzx	eax, BYTE PTR 73[rsp]
	mov	ecx, eax
	not	eax
	and	ecx, 120
	test	al, 56
	jne	.L3454
	movzx	eax, WORD PTR 76[rsp]
	test	BYTE PTR 72[rsp], 92
	jne	.L3469
	mov	QWORD PTR 8[rdi], rdx
	mov	rdx, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rdx]
	movzx	edx, BYTE PTR [rsi]
	cmp	cl, 56
	je	.L3464
	mov	BYTE PTR 71[rsp], dl
	lea	rdx, 71[rsp]
	mov	esi, 1
	mov	rdi, rdx
	movzx	edx, WORD PTR 72[rsp]
	and	dx, 384
	cmp	dx, 128
	je	.L3459
	cmp	dx, 256
	je	.L3460
.L3462:
	mov	rcx, QWORD PTR 16[rbx]
	lea	rdx, 48[rsp]
	mov	r8d, 15
	mov	QWORD PTR 48[rsp], rsi
	mov	QWORD PTR 56[rsp], rdi
	call	_ZNSt8__format15__write_escapedIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L3454:
	mov	rax, QWORD PTR [rbx]
	mov	QWORD PTR 8[rdi], rdx
	movzx	edx, BYTE PTR [rsi]
	mov	rbx, QWORD PTR 56[rax]
	test	cl, cl
	je	.L3464
	cmp	cl, 56
	je	.L3464
	mov	r8, rbx
	mov	rcx, rbp
	call	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L3464:
	mov	BYTE PTR 96[rsp], dl
	lea	rax, 96[rsp]
	mov	r9, rbp
	mov	r8, rbx
	lea	rcx, 48[rsp]
	mov	edx, 1
	mov	DWORD PTR 32[rsp], 1
	mov	QWORD PTR 48[rsp], 1
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L3460:
	mov	rdx, rbx
	mov	ecx, eax
	call	_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0
.L3459:
	cmp	rax, 3
	jbe	.L3462
	lea	rax, 84[rsp]
	lea	rdx, 48[rsp]
	mov	QWORD PTR 48[rsp], rsi
	mov	r8d, 15
	lea	rcx, _ZTVNSt8__format14_Fixedbuf_sinkIcEE[rip+16]
	movq	xmm1, rax
	mov	QWORD PTR 120[rsp], rax
	movq	xmm0, rcx
	lea	rcx, 96[rsp]
	mov	QWORD PTR 56[rsp], rdi
	mov	QWORD PTR 112[rsp], 12
	punpcklqdq	xmm0, xmm1
	movaps	XMMWORD PTR 96[rsp], xmm0
	call	_ZNSt8__format15__write_escapedIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE
	mov	rax, QWORD PTR 104[rsp]
	mov	rdx, QWORD PTR 120[rsp]
	lea	rcx, 48[rsp]
	sub	rdx, rax
	mov	r9, rax
	cmp	BYTE PTR 1[rax], 92
	mov	eax, 3
	mov	DWORD PTR 32[rsp], 1
	mov	r8, rdx
	cmovne	rdx, rax
	mov	QWORD PTR 48[rsp], r8
	mov	r8, rbx
	mov	QWORD PTR 56[rsp], r9
	mov	r9, rbp
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L3469:
	lea	rcx, .LC46[rip]
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNKSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_Iterator11_M_is_breakENS0_13_Gcb_propertyES8_NS_13_Utf_iteratorIcDiPKcSB_NS_5_ReplEEE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_Iterator11_M_is_breakENS0_13_Gcb_propertyES8_NS_13_Utf_iteratorIcDiPKcSB_NS_5_ReplEEE
	.def	_ZNKSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_Iterator11_M_is_breakENS0_13_Gcb_propertyES8_NS_13_Utf_iteratorIcDiPKcSB_NS_5_ReplEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_Iterator11_M_is_breakENS0_13_Gcb_propertyES8_NS_13_Utf_iteratorIcDiPKcSB_NS_5_ReplEEE
_ZNKSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_Iterator11_M_is_breakENS0_13_Gcb_propertyES8_NS_13_Utf_iteratorIcDiPKcSB_NS_5_ReplEEE:
.LFB6057:
	push	r15
	.seh_pushreg	r15
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
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	eax, edx
	lea	edx, -1[rdx]
	mov	r10, rcx
	cmp	edx, 1
	jbe	.L3482
	cmp	eax, 3
	je	.L3533
	lea	edx, -1[r8]
	cmp	edx, 2
	jbe	.L3482
	lea	edx, -7[rax]
	cmp	edx, 5
	ja	.L3475
	lea	rcx, .L3477[rip]
	movsxd	rdx, DWORD PTR [rcx+rdx*4]
	add	rdx, rcx
	jmp	rdx
	.section .rdata,"dr"
	.align 4
.L3477:
	.long	.L3479-.L3477
	.long	.L3478-.L3477
	.long	.L3476-.L3477
	.long	.L3475-.L3477
	.long	.L3478-.L3477
	.long	.L3476-.L3477
	.section	.text$_ZNKSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_Iterator11_M_is_breakENS0_13_Gcb_propertyES8_NS_13_Utf_iteratorIcDiPKcSB_NS_5_ReplEEE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L3476:
	cmp	r8d, 9
	setne	al
.L3470:
	add	rsp, 80
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L3478:
	sub	r8d, 8
	cmp	r8d, 1
	seta	al
	jmp	.L3470
	.p2align 4,,10
	.p2align 3
.L3479:
	cmp	r8d, 8
	jg	.L3480
	cmp	r8d, 6
	jg	.L3481
	.p2align 4
	.p2align 3
.L3482:
	mov	eax, 1
	jmp	.L3470
	.p2align 4,,10
	.p2align 3
.L3475:
	mov	edx, r8d
	and	edx, -3
	cmp	edx, 4
	sete	dl
	cmp	eax, 5
	sete	cl
	or	edx, ecx
	cmp	r8d, 10
	sete	cl
	or	dl, cl
	mov	esi, edx
	je	.L3534
.L3481:
	xor	eax, eax
	jmp	.L3470
	.p2align 4,,10
	.p2align 3
.L3533:
	cmp	r8d, 2
	setne	al
	add	rsp, 80
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L3480:
	sub	r8d, 11
	cmp	r8d, 1
	ja	.L3482
	xor	eax, eax
	jmp	.L3470
	.p2align 4,,10
	.p2align 3
.L3534:
	movzx	ecx, BYTE PTR 10[r10]
	mov	r14d, ecx
	test	cl, cl
	je	.L3483
	mov	ecx, DWORD PTR [r10]
	sal	ecx, 2
	cmp	ecx, 3073
	ja	.L3535
.L3483:
	cmp	eax, 10
	je	.L3536
	cmp	eax, 13
	jne	.L3482
	cmp	eax, r8d
	jne	.L3482
	movzx	eax, BYTE PTR 9[r10]
	not	eax
	and	eax, 1
	jmp	.L3470
	.p2align 4,,10
	.p2align 3
.L3536:
	cmp	BYTE PTR 8[r10], 2
	setne	al
	jmp	.L3470
.L3535:
	or	ecx, 3
	mov	r11d, 790
	lea	rdi, _ZNSt9__unicode9__v16_0_012__incb_edgesE[rip]
	mov	r15d, ecx
.L3485:
	test	r11, r11
	jle	.L3537
.L3486:
	mov	rdx, r11
	sar	rdx
	cmp	DWORD PTR [rdi+rdx*4], r15d
	jnb	.L3508
	sub	r11, rdx
	lea	rdi, 4[rdi+rdx*4]
	sub	r11, 1
	test	r11, r11
	jg	.L3486
.L3537:
	mov	ecx, DWORD PTR -4[rdi]
	and	ecx, 3
	cmp	ecx, 1
	jne	.L3483
	movzx	ecx, BYTE PTR 24[r9]
	mov	r12d, ecx
	mov	ecx, DWORD PTR [r9+rcx*4]
	sal	ecx, 2
	cmp	ecx, 3073
	jbe	.L3483
	or	ecx, 3
	mov	r11d, 790
	lea	rdi, _ZNSt9__unicode9__v16_0_012__incb_edgesE[rip]
	mov	r15d, ecx
.L3488:
	test	r11, r11
	jle	.L3538
.L3489:
	mov	rdx, r11
	sar	rdx
	cmp	DWORD PTR [rdi+rdx*4], r15d
	jnb	.L3509
	sub	r11, rdx
	lea	rdi, 4[rdi+rdx*4]
	sub	r11, 1
	test	r11, r11
	jg	.L3489
.L3538:
	mov	ecx, DWORD PTR -4[rdi]
	and	ecx, 3
	sub	ecx, 1
	jne	.L3483
	mov	rcx, QWORD PTR 48[r10]
	movdqu	xmm0, XMMWORD PTR 16[r10]
	movdqu	xmm1, XMMWORD PTR 32[r10]
	mov	QWORD PTR 64[rsp], rcx
	movaps	XMMWORD PTR 32[rsp], xmm0
	movaps	XMMWORD PTR 48[rsp], xmm1
.L3490:
	mov	rbp, QWORD PTR 16[r9]
	movzx	edi, BYTE PTR 56[rsp]
	mov	r15, QWORD PTR 48[rsp]
.L3494:
	movzx	ecx, dil
	movzx	r11d, BYTE PTR 57[rsp]
	add	ecx, 1
	cmp	ecx, r11d
	je	.L3539
	jge	.L3501
	lea	ebx, 1[rdi]
	mov	BYTE PTR 56[rsp], bl
	mov	edi, ebx
.L3501:
	cmp	rbp, r15
	sete	r11b
	cmp	r12b, dil
	sete	cl
	test	r11b, cl
	jne	.L3505
	movzx	ecx, dil
	mov	r11d, DWORD PTR 32[rsp+rcx*4]
	cmp	DWORD PTR _ZNSt9__unicode9__v16_0_014__incb_linkersE[rip], r11d
	lea	rcx, _ZNSt9__unicode9__v16_0_014__incb_linkersE[rip]
	je	.L3491
	add	rcx, 4
	cmp	DWORD PTR [rcx], r11d
	je	.L3491
	add	rcx, 4
.L3492:
	cmp	DWORD PTR [rcx], r11d
	je	.L3491
	lea	rdx, 4[rcx]
	mov	rcx, rdx
	cmp	DWORD PTR [rdx], r11d
	je	.L3491
	add	rcx, 4
	cmp	DWORD PTR [rcx], r11d
	je	.L3491
	lea	rcx, 8[rdx]
	cmp	DWORD PTR 8[rdx], r11d
	je	.L3491
	lea	rcx, 12[rdx]
	lea	rdx, _ZNSt9__unicode9__v16_0_014__incb_linkersE[rip+24]
	cmp	rcx, rdx
	jne	.L3492
.L3493:
	sal	r11d, 2
	cmp	r11d, 3073
	jbe	.L3483
	mov	edx, r11d
	mov	ecx, 790
	lea	rdi, _ZNSt9__unicode9__v16_0_012__incb_edgesE[rip]
	or	edx, 3
.L3497:
	test	rcx, rcx
	jle	.L3540
.L3498:
	mov	r11, rcx
	sar	r11
	cmp	DWORD PTR [rdi+r11*4], edx
	jnb	.L3511
	sub	rcx, r11
	lea	rdi, 4[rdi+r11*4]
	sub	rcx, 1
	test	rcx, rcx
	jg	.L3498
.L3540:
	mov	ecx, DWORD PTR -4[rdi]
	and	ecx, 3
	cmp	ecx, 1
	je	.L3512
	cmp	ecx, 2
	je	.L3490
	jmp	.L3483
	.p2align 4,,10
	.p2align 3
.L3491:
	lea	rbx, _ZNSt9__unicode9__v16_0_014__incb_linkersE[rip+24]
	cmp	rcx, rbx
	je	.L3493
	mov	esi, r14d
	jmp	.L3494
.L3508:
	mov	r11, rdx
	jmp	.L3485
.L3539:
	mov	rcx, QWORD PTR 64[rsp]
	cmp	r15, rcx
	je	.L3501
	movzx	r11d, BYTE PTR 58[rsp]
	lea	rbx, [r15+r11]
	mov	QWORD PTR 48[rsp], rbx
	mov	r15, rbx
	cmp	rbx, rcx
	je	.L3541
	lea	rcx, 32[rsp]
	mov	QWORD PTR 168[rsp], r9
	mov	DWORD PTR 160[rsp], r8d
	mov	DWORD PTR 152[rsp], eax
	mov	QWORD PTR 144[rsp], r10
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	r15, QWORD PTR 48[rsp]
	movzx	edi, BYTE PTR 56[rsp]
	mov	r10, QWORD PTR 144[rsp]
	mov	eax, DWORD PTR 152[rsp]
	mov	r8d, DWORD PTR 160[rsp]
	mov	r9, QWORD PTR 168[rsp]
	jmp	.L3501
.L3509:
	mov	r11, rdx
	jmp	.L3488
.L3511:
	mov	rcx, r11
	jmp	.L3497
.L3505:
	test	sil, sil
	je	.L3483
	xor	eax, eax
	jmp	.L3470
.L3541:
	mov	BYTE PTR 56[rsp], 0
	xor	edi, edi
	jmp	.L3501
.L3512:
	xor	esi, esi
	jmp	.L3490
	.seh_endproc
	.section	.text$_ZNSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_IteratorppEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_IteratorppEv
	.def	_ZNSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_IteratorppEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_IteratorppEv
_ZNSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_IteratorppEv:
.LFB5951:
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
	sub	rsp, 136
	.seh_stackalloc	136
	.seh_endprologue
	mov	rsi, QWORD PTR 48[rcx]
	mov	rdi, QWORD PTR 32[rcx]
	mov	r12, rcx
	cmp	rsi, rdi
	je	.L3543
	movdqu	xmm3, XMMWORD PTR 32[rcx]
	movdqu	xmm2, XMMWORD PTR 16[rcx]
	mov	QWORD PTR 112[rsp], rsi
	lea	rbp, _ZNSt9__unicode9__v16_0_011__gcb_edgesE[rip]
	mov	r14d, DWORD PTR 4[rcx]
	movaps	XMMWORD PTR 96[rsp], xmm3
	movzx	r13d, BYTE PTR 104[rsp]
	movzx	edx, BYTE PTR 105[rsp]
	movaps	XMMWORD PTR 80[rsp], xmm2
	movzx	eax, r13b
	add	eax, 1
	cmp	eax, edx
	je	.L3598
	.p2align 4
	.p2align 3
.L3567:
	jge	.L3572
	add	r13d, 1
	mov	BYTE PTR 104[rsp], r13b
.L3572:
	cmp	rsi, rdi
	je	.L3566
	movzx	eax, BYTE PTR 104[rsp]
	mov	r8, rbp
	mov	ebx, DWORD PTR 80[rsp+rax*4]
	mov	r13, rax
	mov	eax, 1717
	mov	r9d, ebx
	sal	r9d, 4
	or	r9d, 15
	.p2align 4
	.p2align 3
.L3546:
	test	rax, rax
	jle	.L3599
.L3547:
	mov	rdx, rax
	sar	rdx
	cmp	DWORD PTR [r8+rdx*4], r9d
	jnb	.L3575
	sub	rax, rdx
	lea	r8, 4[r8+rdx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3547
.L3599:
	mov	r15d, DWORD PTR -4[r8]
	movzx	eax, BYTE PTR 8[r12]
	and	r15d, 15
	cmp	al, 3
	je	.L3548
	cmp	al, 1
	je	.L3549
	cmp	r15d, 10
	je	.L3600
	cmp	r15d, 4
	je	.L3553
.L3557:
	mov	BYTE PTR 8[r12], 3
.L3548:
	cmp	r15d, 13
	jne	.L3553
	movzx	eax, BYTE PTR 9[r12]
	add	eax, 1
.L3561:
	mov	BYTE PTR 9[r12], al
	lea	rax, _ZNSt9__unicode9__v16_0_014__incb_linkersE[rip]
	cmp	DWORD PTR _ZNSt9__unicode9__v16_0_014__incb_linkersE[rip], ebx
	lea	rcx, 24[rax]
	je	.L3563
	add	rax, 4
	cmp	DWORD PTR [rax], ebx
	je	.L3563
	add	rax, 4
.L3564:
	cmp	DWORD PTR [rax], ebx
	je	.L3563
	lea	rdx, 4[rax]
	mov	rax, rdx
	cmp	DWORD PTR [rdx], ebx
	je	.L3563
	add	rax, 4
	cmp	DWORD PTR [rax], ebx
	je	.L3563
	lea	rax, 8[rdx]
	cmp	DWORD PTR 8[rdx], ebx
	je	.L3563
	lea	rax, 12[rdx]
	cmp	rax, rcx
	jne	.L3564
	.p2align 4
	.p2align 3
.L3565:
	movdqa	xmm0, XMMWORD PTR 80[rsp]
	mov	r8d, r15d
	mov	edx, r14d
	mov	rcx, r12
	movdqa	xmm1, XMMWORD PTR 96[rsp]
	mov	rax, QWORD PTR 112[rsp]
	lea	r9, 32[rsp]
	movaps	XMMWORD PTR 32[rsp], xmm0
	mov	QWORD PTR 64[rsp], rax
	movaps	XMMWORD PTR 48[rsp], xmm1
	call	_ZNKSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_Iterator11_M_is_breakENS0_13_Gcb_propertyES8_NS_13_Utf_iteratorIcDiPKcSB_NS_5_ReplEEE
	test	al, al
	jne	.L3601
	movzx	eax, r13b
	movzx	edx, BYTE PTR 105[rsp]
	mov	r14d, r15d
	add	eax, 1
	cmp	eax, edx
	jne	.L3567
.L3598:
	cmp	rsi, rdi
	je	.L3566
	movzx	eax, BYTE PTR 106[rsp]
	add	rax, rdi
	mov	QWORD PTR 96[rsp], rax
	cmp	rsi, rax
	je	.L3602
	lea	rcx, 80[rsp]
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	rdi, QWORD PTR 96[rsp]
	jmp	.L3572
	.p2align 4,,10
	.p2align 3
.L3575:
	mov	rax, rdx
	jmp	.L3546
	.p2align 4,,10
	.p2align 3
.L3563:
	cmp	rax, rcx
	je	.L3565
	mov	BYTE PTR 10[r12], 1
	jmp	.L3565
	.p2align 4,,10
	.p2align 3
.L3549:
	test	r15d, r15d
	jne	.L3557
	cmp	ebx, 168
	ja	.L3603
.L3556:
	mov	BYTE PTR 8[r12], 3
.L3553:
	xor	eax, eax
	jmp	.L3561
	.p2align 4,,10
	.p2align 3
.L3600:
	cmp	al, 2
	je	.L3551
	mov	edx, DWORD PTR [r12]
	cmp	edx, 168
	jbe	.L3556
	lea	rcx, _ZNSt9__unicode9__v16_0_014__xpicto_edgesE[rip]
	mov	eax, 156
	mov	r10, rcx
.L3554:
	test	rax, rax
	jle	.L3604
.L3555:
	mov	r8, rax
	sar	r8
	cmp	edx, DWORD PTR [r10+r8*4]
	jb	.L3577
	sub	rax, r8
	lea	r10, 4[r10+r8*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3555
.L3604:
	sub	r10, rcx
	and	r10d, 4
	je	.L3556
.L3551:
	mov	BYTE PTR 8[r12], 1
	xor	eax, eax
	jmp	.L3561
.L3602:
	mov	BYTE PTR 104[rsp], 0
.L3566:
	mov	rax, QWORD PTR 112[rsp]
	movdqa	xmm4, XMMWORD PTR 80[rsp]
	movdqa	xmm5, XMMWORD PTR 96[rsp]
	mov	QWORD PTR 48[r12], rax
	movups	XMMWORD PTR 16[r12], xmm4
	movups	XMMWORD PTR 32[r12], xmm5
.L3543:
	mov	rax, r12
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L3601:
	xor	eax, eax
	mov	DWORD PTR [r12], ebx
	mov	DWORD PTR 4[r12], r15d
	mov	WORD PTR 8[r12], ax
	mov	BYTE PTR 10[r12], 0
	jmp	.L3566
.L3577:
	mov	rax, r8
	jmp	.L3554
.L3603:
	lea	rcx, _ZNSt9__unicode9__v16_0_014__xpicto_edgesE[rip]
	mov	eax, 156
	mov	r9, rcx
.L3559:
	test	rax, rax
	jle	.L3605
.L3560:
	mov	rdx, rax
	sar	rdx
	cmp	ebx, DWORD PTR [r9+rdx*4]
	jb	.L3578
	sub	rax, rdx
	lea	r9, 4[r9+rdx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3560
.L3605:
	sub	r9, rcx
	and	r9d, 4
	je	.L3556
	mov	BYTE PTR 8[r12], 2
	xor	eax, eax
	jmp	.L3561
.L3578:
	mov	rax, rdx
	jmp	.L3559
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
	.def	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE:
.LFB5618:
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
	sub	rsp, 744
	.seh_stackalloc	744
	.seh_endprologue
	mov	r10, QWORD PTR [rdx]
	mov	r15, r10
	mov	rbx, rcx
	mov	rcx, QWORD PTR 8[rdx]
	mov	QWORD PTR 832[rsp], r8
	movzx	edx, BYTE PTR 1[rbx]
	movzx	r14d, WORD PTR [rbx]
	movq	xmm0, rcx
	mov	rbp, rcx
	mov	r8d, edx
	punpcklqdq	xmm0, xmm0
	and	r8d, 6
	and	r14w, 384
	jne	.L3607
	test	r8b, r8b
	je	.L3608
	cmp	r8b, 2
	je	.L3609
	cmp	r8b, 4
	je	.L3610
	test	r10, r10
	jne	.L3611
	xor	edi, edi
	mov	rsi, -1
	jmp	.L3675
	.p2align 4,,10
	.p2align 3
.L3607:
	test	r8b, r8b
	jne	.L3796
.L3620:
	test	r15, r15
	je	.L3735
.L3611:
	lea	rsi, 0[rbp+r15]
	cmp	rbp, rsi
	je	.L3654
	xor	r12d, r12d
	lea	rcx, 144[rsp]
	movups	XMMWORD PTR 152[rsp], xmm0
	mov	WORD PTR 168[rsp], r12w
	mov	BYTE PTR 170[rsp], 0
	mov	QWORD PTR 176[rsp], rsi
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	rdx, QWORD PTR 160[rsp]
	movq	xmm0, rbp
	mov	r10, QWORD PTR 144[rsp]
	mov	r9, QWORD PTR 168[rsp]
	mov	QWORD PTR 176[rsp], rsi
	movq	xmm5, rdx
	mov	QWORD PTR 416[rsp], r10
	movzx	eax, WORD PTR 168[rsp]
	punpcklqdq	xmm0, xmm5
	mov	QWORD PTR 440[rsp], r9
	movups	XMMWORD PTR 152[rsp], xmm0
	mov	r11, QWORD PTR 152[rsp]
	mov	r8, QWORD PTR 160[rsp]
	mov	QWORD PTR 448[rsp], rsi
	mov	QWORD PTR 424[rsp], r11
	mov	QWORD PTR 432[rsp], r8
	mov	QWORD PTR 368[rsp], r10
	mov	QWORD PTR 376[rsp], r11
	mov	QWORD PTR 384[rsp], r8
	mov	QWORD PTR 392[rsp], r9
	mov	QWORD PTR 400[rsp], rsi
	cmp	rsi, rdx
	je	.L3656
	movzx	eax, al
	lea	r8, _ZNSt9__unicode9__v16_0_011__gcb_edgesE[rip]
	mov	r13d, DWORD PTR 416[rsp+rax*4]
	mov	eax, 1717
	mov	r9d, r13d
	sal	r9d, 4
	or	r9d, 15
	.p2align 4
	.p2align 3
.L3659:
	test	rax, rax
	jle	.L3797
.L3660:
	mov	rdx, rax
	sar	rdx
	cmp	DWORD PTR [r8+rdx*4], r9d
	jnb	.L3736
	sub	rax, rdx
	lea	r8, 4[r8+rdx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3660
.L3797:
	mov	edi, DWORD PTR -4[r8]
	and	edi, 15
.L3656:
	xor	r10d, r10d
	mov	DWORD PTR 356[rsp], edi
	movdqa	xmm2, XMMWORD PTR 368[rsp]
	mov	edi, 1
	mov	DWORD PTR 352[rsp], r13d
	movdqa	xmm3, XMMWORD PTR 384[rsp]
	mov	WORD PTR 360[rsp], r10w
	mov	BYTE PTR 362[rsp], 0
	movdqa	xmm1, XMMWORD PTR 352[rsp]
	mov	QWORD PTR 400[rsp], rsi
	mov	QWORD PTR 464[rsp], rsi
	movaps	XMMWORD PTR 416[rsp], xmm1
	movaps	XMMWORD PTR 432[rsp], xmm2
	movaps	XMMWORD PTR 448[rsp], xmm3
	cmp	r13d, 4351
	jbe	.L3665
	jmp	.L3798
	.p2align 4,,10
	.p2align 3
.L3670:
	mov	edx, DWORD PTR 416[rsp]
	mov	eax, 1
	cmp	edx, 4351
	ja	.L3799
.L3666:
	add	rdi, rax
.L3665:
	lea	rcx, 416[rsp]
	call	_ZNSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_IteratorppEv
	cmp	QWORD PTR 32[rax], rsi
	jne	.L3670
.L3653:
	mov	rsi, -1
.L3652:
	cmp	r14w, 128
	je	.L3800
	cmp	r14w, 256
	je	.L3672
.L3792:
	movzx	edx, BYTE PTR 1[rbx]
.L3675:
	mov	eax, edx
	test	dl, 6
	je	.L3801
	not	eax
	test	al, 120
	je	.L3682
.L3803:
	lea	rcx, 80[rsp]
	mov	r9, rbx
	mov	rdx, rdi
	mov	QWORD PTR 80[rsp], r15
	mov	DWORD PTR 32[rsp], 1
	mov	r8, QWORD PTR 832[rsp]
	mov	QWORD PTR 88[rsp], rbp
.LEHB62:
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.LEHE62:
.L3768:
	add	rsp, 744
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
.L3736:
	mov	rax, rdx
	jmp	.L3659
	.p2align 4,,10
	.p2align 3
.L3799:
	lea	r8, _ZNSt9__unicode9__v16_0_013__width_edgesE[rip]
	mov	eax, 206
	mov	r9, r8
	.p2align 4
	.p2align 3
.L3668:
	test	rax, rax
	jle	.L3802
.L3669:
	mov	rcx, rax
	sar	rcx
	cmp	edx, DWORD PTR [r9+rcx*4]
	jb	.L3740
	sub	rax, rcx
	lea	r9, 4[r9+rcx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3669
.L3802:
	sub	r9, r8
	mov	rax, r9
	shr	r9, 63
	sar	rax, 2
	add	rax, r9
	and	eax, 1
	sub	rax, r9
	add	eax, 1
	jmp	.L3666
	.p2align 4,,10
	.p2align 3
.L3740:
	mov	rax, rcx
	jmp	.L3668
	.p2align 4,,10
	.p2align 3
.L3800:
	movzx	eax, WORD PTR 4[rbx]
.L3671:
	cmp	rdi, rax
	jnb	.L3792
	movzx	eax, BYTE PTR 1[rbx]
	not	eax
	test	al, 120
	jne	.L3803
.L3682:
	lea	rax, 448[rsp]
	lea	r12, _ZTVNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE[rip+16]
	mov	QWORD PTR 88[rsp], rbp
	mov	r8d, 12
	movq	xmm2, rax
	mov	QWORD PTR 440[rsp], rax
	lea	rax, 720[rsp]
	movq	xmm0, r12
	mov	QWORD PTR 48[rsp], rax
	punpcklqdq	xmm0, xmm2
	lea	rcx, 416[rsp]
	lea	rbp, 704[rsp]
	mov	QWORD PTR 704[rsp], rax
	lea	rax, 80[rsp]
	mov	rdx, rax
	mov	BYTE PTR 720[rsp], 0
	mov	QWORD PTR 432[rsp], 256
	mov	QWORD PTR 712[rsp], 0
	mov	QWORD PTR 80[rsp], r15
	mov	QWORD PTR 56[rsp], rax
	movaps	XMMWORD PTR 416[rsp], xmm0
.LEHB63:
	call	_ZNSt8__format15__write_escapedIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE
	mov	r15, QWORD PTR 424[rsp]
	mov	r13, QWORD PTR 440[rsp]
	mov	rdx, QWORD PTR 712[rsp]
	sub	r13, r15
	test	rdx, rdx
	jne	.L3804
	movq	xmm0, r15
	punpcklqdq	xmm0, xmm0
	cmp	rsi, -1
	jne	.L3805
	test	r13, r13
	je	.L3752
.L3686:
	xor	ecx, ecx
	lea	rsi, [r15+r13]
	mov	BYTE PTR 266[rsp], 0
	mov	WORD PTR 264[rsp], cx
	lea	rcx, 240[rsp]
	mov	QWORD PTR 272[rsp], rsi
	movups	XMMWORD PTR 248[rsp], xmm0
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	r8, QWORD PTR 240[rsp]
	mov	r10, QWORD PTR 256[rsp]
	mov	QWORD PTR 248[rsp], r15
	mov	r11, QWORD PTR 264[rsp]
	mov	r9, QWORD PTR 248[rsp]
	mov	QWORD PTR 272[rsp], rsi
	mov	QWORD PTR 352[rsp], r8
	movzx	eax, WORD PTR 264[rsp]
	mov	QWORD PTR 360[rsp], r9
	mov	QWORD PTR 368[rsp], r10
	mov	QWORD PTR 376[rsp], r11
	mov	QWORD PTR 384[rsp], rsi
	mov	QWORD PTR 304[rsp], r8
	mov	QWORD PTR 312[rsp], r9
	mov	QWORD PTR 320[rsp], r10
	mov	QWORD PTR 328[rsp], r11
	mov	QWORD PTR 336[rsp], rsi
	cmp	QWORD PTR 256[rsp], rsi
	je	.L3711
	movzx	eax, al
	lea	r10, _ZNSt9__unicode9__v16_0_011__gcb_edgesE[rip]
	mov	eax, DWORD PTR 352[rsp+rax*4]
	mov	r11d, eax
	mov	DWORD PTR 64[rsp], eax
	mov	eax, 1717
	sal	r11d, 4
	or	r11d, 15
	.p2align 4
	.p2align 3
.L3713:
	test	rax, rax
	jle	.L3806
.L3714:
	mov	rdx, rax
	sar	rdx
	cmp	DWORD PTR [r10+rdx*4], r11d
	jnb	.L3753
	sub	rax, rdx
	lea	r10, 4[r10+rdx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3714
.L3806:
	mov	eax, DWORD PTR -4[r10]
	and	eax, 15
	mov	DWORD PTR 72[rsp], eax
.L3711:
	mov	edi, DWORD PTR 72[rsp]
	mov	eax, DWORD PTR 64[rsp]
	xor	edx, edx
	mov	BYTE PTR 298[rsp], 0
	mov	WORD PTR 296[rsp], dx
	movdqa	xmm2, XMMWORD PTR 304[rsp]
	movdqa	xmm5, XMMWORD PTR 320[rsp]
	mov	DWORD PTR 292[rsp], edi
	mov	edi, 1
	mov	DWORD PTR 288[rsp], eax
	movdqa	xmm3, XMMWORD PTR 288[rsp]
	mov	QWORD PTR 336[rsp], rsi
	mov	QWORD PTR 400[rsp], rsi
	movaps	XMMWORD PTR 352[rsp], xmm3
	movaps	XMMWORD PTR 368[rsp], xmm2
	movaps	XMMWORD PTR 384[rsp], xmm5
	cmp	eax, 4351
	ja	.L3807
.L3715:
	lea	rbp, 352[rsp]
	jmp	.L3719
	.p2align 4,,10
	.p2align 3
.L3724:
	mov	edx, DWORD PTR 352[rsp]
	mov	eax, 1
	cmp	edx, 4351
	ja	.L3808
.L3720:
	add	rdi, rax
.L3719:
	mov	rcx, rbp
	call	_ZNSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_IteratorppEv
	cmp	QWORD PTR 32[rax], rsi
	jne	.L3724
.L3710:
	mov	rcx, QWORD PTR 56[rsp]
	mov	r9, rbx
	mov	rdx, rdi
	mov	QWORD PTR 80[rsp], r13
	mov	DWORD PTR 32[rsp], 1
	mov	r8, QWORD PTR 832[rsp]
	lea	rbp, 704[rsp]
	mov	QWORD PTR 88[rsp], r15
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.LEHE63:
	mov	rcx, QWORD PTR 704[rsp]
	cmp	rcx, QWORD PTR 48[rsp]
	je	.L3768
	mov	QWORD PTR 48[rsp], rax
	mov	rax, QWORD PTR 720[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	rax, QWORD PTR 48[rsp]
	jmp	.L3768
	.p2align 4,,10
	.p2align 3
.L3654:
	movq	xmm0, rbp
	xor	r11d, r11d
	mov	DWORD PTR 144[rsp], 0
	punpcklqdq	xmm0, xmm0
	mov	BYTE PTR 170[rsp], 0
	movups	XMMWORD PTR 152[rsp], xmm0
	movdqa	xmm3, XMMWORD PTR 144[rsp]
	mov	WORD PTR 168[rsp], r11w
	movdqa	xmm2, XMMWORD PTR 160[rsp]
	mov	QWORD PTR 176[rsp], rbp
	movaps	XMMWORD PTR 368[rsp], xmm3
	movaps	XMMWORD PTR 384[rsp], xmm2
	jmp	.L3656
	.p2align 4,,10
	.p2align 3
.L3608:
	mov	rax, QWORD PTR 832[rsp]
	not	edx
	and	edx, 120
	mov	rbx, QWORD PTR 16[rax]
	je	.L3809
	test	r10, r10
	jne	.L3810
.L3677:
	mov	rax, rbx
	jmp	.L3768
	.p2align 4,,10
	.p2align 3
.L3804:
	test	r13, r13
	jne	.L3684
	mov	r15, QWORD PTR 704[rsp]
	mov	r13, rdx
	movq	xmm0, r15
	punpcklqdq	xmm0, xmm0
	cmp	rsi, -1
	je	.L3686
.L3685:
	lea	r14, [r15+r13]
	xor	r9d, r9d
	lea	rcx, 192[rsp]
	movups	XMMWORD PTR 200[rsp], xmm0
	mov	WORD PTR 216[rsp], r9w
	mov	BYTE PTR 218[rsp], 0
	mov	QWORD PTR 224[rsp], r14
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	r8, QWORD PTR 208[rsp]
	mov	r9, QWORD PTR 216[rsp]
	mov	QWORD PTR 200[rsp], r15
	mov	QWORD PTR 224[rsp], r14
	movzx	eax, WORD PTR 216[rsp]
	movdqa	xmm0, XMMWORD PTR 192[rsp]
	mov	QWORD PTR 368[rsp], r8
	mov	QWORD PTR 376[rsp], r9
	mov	QWORD PTR 384[rsp], r14
	mov	QWORD PTR 320[rsp], r8
	mov	QWORD PTR 328[rsp], r9
	mov	QWORD PTR 336[rsp], r14
	movaps	XMMWORD PTR 352[rsp], xmm0
	movaps	XMMWORD PTR 304[rsp], xmm0
	cmp	r14, QWORD PTR 208[rsp]
	je	.L3696
	movzx	eax, al
	lea	rcx, _ZNSt9__unicode9__v16_0_011__gcb_edgesE[rip]
	mov	eax, DWORD PTR 352[rsp+rax*4]
	mov	r11d, eax
	mov	DWORD PTR 68[rsp], eax
	mov	eax, 1717
	sal	r11d, 4
	or	r11d, 15
	.p2align 4
	.p2align 3
.L3698:
	test	rax, rax
	jle	.L3811
.L3699:
	mov	rdx, rax
	sar	rdx
	cmp	DWORD PTR [rcx+rdx*4], r11d
	jnb	.L3745
	sub	rax, rdx
	lea	rcx, 4[rcx+rdx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3699
.L3811:
	mov	eax, DWORD PTR -4[rcx]
	and	eax, 15
	mov	DWORD PTR 76[rsp], eax
.L3696:
	mov	edi, DWORD PTR 76[rsp]
	mov	eax, DWORD PTR 68[rsp]
	xor	r8d, r8d
	mov	BYTE PTR 298[rsp], 0
	mov	WORD PTR 296[rsp], r8w
	movdqa	xmm3, XMMWORD PTR 304[rsp]
	movdqa	xmm4, XMMWORD PTR 320[rsp]
	mov	DWORD PTR 292[rsp], edi
	mov	edi, 1
	mov	DWORD PTR 288[rsp], eax
	movdqa	xmm1, XMMWORD PTR 288[rsp]
	mov	QWORD PTR 336[rsp], r14
	mov	QWORD PTR 400[rsp], r14
	movaps	XMMWORD PTR 352[rsp], xmm1
	movaps	XMMWORD PTR 368[rsp], xmm3
	movaps	XMMWORD PTR 384[rsp], xmm4
	cmp	eax, 4351
	ja	.L3812
.L3700:
	lea	rbp, 352[rsp]
	cmp	rsi, rdi
	jnb	.L3704
	jmp	.L3813
	.p2align 4,,10
	.p2align 3
.L3705:
	add	rax, rdi
	cmp	rsi, rax
	jb	.L3814
	mov	rdi, rax
.L3704:
	mov	rcx, rbp
	call	_ZNSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_IteratorppEv
	cmp	QWORD PTR 32[rax], r14
	je	.L3710
	mov	edx, DWORD PTR 352[rsp]
	mov	eax, 1
	cmp	edx, 4351
	jbe	.L3705
	lea	r8, _ZNSt9__unicode9__v16_0_013__width_edgesE[rip]
	mov	eax, 206
	mov	r9, r8
	.p2align 4
	.p2align 3
.L3707:
	test	rax, rax
	jle	.L3815
.L3708:
	mov	rcx, rax
	sar	rcx
	cmp	edx, DWORD PTR [r9+rcx*4]
	jb	.L3750
	sub	rax, rcx
	lea	r9, 4[r9+rcx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3708
.L3815:
	sub	r9, r8
	mov	rax, r9
	shr	r9, 63
	sar	rax, 2
	add	rax, r9
	and	eax, 1
	sub	rax, r9
	add	eax, 1
	jmp	.L3705
	.p2align 4,,10
	.p2align 3
.L3609:
	movzx	esi, WORD PTR 6[rbx]
.L3622:
	test	r15, r15
	je	.L3791
	lea	r12, 0[rbp+r15]
	cmp	r12, rbp
	je	.L3635
	xor	ecx, ecx
	mov	DWORD PTR 56[rsp], r9d
	mov	WORD PTR 120[rsp], cx
	lea	rcx, 96[rsp]
	mov	DWORD PTR 48[rsp], eax
	movups	XMMWORD PTR 104[rsp], xmm0
	mov	BYTE PTR 122[rsp], 0
	mov	QWORD PTR 128[rsp], r12
	call	_ZNSt9__unicode13_Utf_iteratorIcDiPKcS2_NS_5_ReplEE12_M_read_utf8Ev
	mov	rcx, QWORD PTR 112[rsp]
	movq	xmm0, rbp
	mov	r11, QWORD PTR 120[rsp]
	mov	QWORD PTR 128[rsp], r12
	movzx	edx, WORD PTR 120[rsp]
	movq	xmm1, rcx
	cmp	r12, rcx
	mov	QWORD PTR 440[rsp], r11
	mov	eax, DWORD PTR 48[rsp]
	punpcklqdq	xmm0, xmm1
	mov	QWORD PTR 448[rsp], r12
	mov	r9d, DWORD PTR 56[rsp]
	movups	XMMWORD PTR 104[rsp], xmm0
	movdqa	xmm0, XMMWORD PTR 96[rsp]
	mov	r10, QWORD PTR 112[rsp]
	mov	QWORD PTR 392[rsp], r11
	mov	QWORD PTR 432[rsp], r10
	mov	QWORD PTR 384[rsp], r10
	mov	QWORD PTR 400[rsp], r12
	movaps	XMMWORD PTR 416[rsp], xmm0
	movaps	XMMWORD PTR 368[rsp], xmm0
	je	.L3637
	movzx	eax, dl
	lea	r10, _ZNSt9__unicode9__v16_0_011__gcb_edgesE[rip]
	mov	edx, 1717
	mov	eax, DWORD PTR 416[rsp+rax*4]
	mov	r11d, eax
	sal	r11d, 4
	or	r11d, 15
	.p2align 4
	.p2align 3
.L3640:
	test	rdx, rdx
	jle	.L3816
.L3641:
	mov	rcx, rdx
	sar	rcx
	cmp	DWORD PTR [r10+rcx*4], r11d
	jnb	.L3728
	sub	rdx, rcx
	lea	r10, 4[r10+rcx*4]
	sub	rdx, 1
	test	rdx, rdx
	jg	.L3641
.L3816:
	mov	r9d, DWORD PTR -4[r10]
	and	r9d, 15
.L3637:
	xor	r13d, r13d
	mov	DWORD PTR 352[rsp], eax
	movdqa	xmm5, XMMWORD PTR 368[rsp]
	mov	edi, 1
	mov	DWORD PTR 356[rsp], r9d
	mov	WORD PTR 360[rsp], r13w
	mov	BYTE PTR 362[rsp], 0
	movdqa	xmm4, XMMWORD PTR 352[rsp]
	mov	QWORD PTR 400[rsp], r12
	movaps	XMMWORD PTR 416[rsp], xmm4
	movdqa	xmm4, XMMWORD PTR 384[rsp]
	mov	QWORD PTR 464[rsp], r12
	movaps	XMMWORD PTR 432[rsp], xmm5
	movaps	XMMWORD PTR 448[rsp], xmm4
	cmp	eax, 4351
	ja	.L3817
.L3642:
	cmp	rsi, rdi
	jnb	.L3646
	jmp	.L3731
	.p2align 4,,10
	.p2align 3
.L3647:
	add	rax, rdi
	cmp	rsi, rax
	jb	.L3818
.L3734:
	mov	rdi, rax
.L3646:
	lea	rcx, 416[rsp]
	call	_ZNSt9__unicode9__v16_0_022_Grapheme_cluster_viewISt17basic_string_viewIcSt11char_traitsIcEEE9_IteratorppEv
	cmp	QWORD PTR 32[rax], r12
	je	.L3652
	mov	edx, DWORD PTR 416[rsp]
	mov	eax, 1
	cmp	edx, 4351
	jbe	.L3647
	lea	r8, _ZNSt9__unicode9__v16_0_013__width_edgesE[rip]
	mov	eax, 206
	mov	r9, r8
	.p2align 4
	.p2align 3
.L3649:
	test	rax, rax
	jle	.L3819
.L3650:
	mov	rcx, rax
	sar	rcx
	cmp	edx, DWORD PTR [r9+rcx*4]
	jb	.L3733
	sub	rax, rcx
	lea	r9, 4[r9+rcx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3650
.L3819:
	sub	r9, r8
	mov	rax, r9
	shr	r9, 63
	sar	rax, 2
	add	rax, r9
	and	eax, 1
	sub	rax, r9
	add	eax, 1
	add	rax, rdi
	cmp	rsi, rax
	jnb	.L3734
	.p2align 4
	.p2align 3
.L3818:
	mov	r15, QWORD PTR 448[rsp]
	sub	r15, rbp
	jmp	.L3652
	.p2align 4,,10
	.p2align 3
.L3728:
	mov	rdx, rcx
	jmp	.L3640
	.p2align 4,,10
	.p2align 3
.L3733:
	mov	rax, rcx
	jmp	.L3649
	.p2align 4,,10
	.p2align 3
.L3753:
	mov	rax, rdx
	jmp	.L3713
	.p2align 4,,10
	.p2align 3
.L3745:
	mov	rax, rdx
	jmp	.L3698
	.p2align 4,,10
	.p2align 3
.L3750:
	mov	rax, rcx
	jmp	.L3707
	.p2align 4,,10
	.p2align 3
.L3635:
	movq	xmm0, rbp
	xor	edx, edx
	mov	DWORD PTR 96[rsp], 0
	punpcklqdq	xmm0, xmm0
	mov	WORD PTR 120[rsp], dx
	movups	XMMWORD PTR 104[rsp], xmm0
	movdqa	xmm1, XMMWORD PTR 96[rsp]
	mov	BYTE PTR 122[rsp], 0
	movdqa	xmm4, XMMWORD PTR 112[rsp]
	mov	QWORD PTR 128[rsp], rbp
	movaps	XMMWORD PTR 368[rsp], xmm1
	movaps	XMMWORD PTR 384[rsp], xmm4
	jmp	.L3637
	.p2align 4,,10
	.p2align 3
.L3731:
	xor	ebp, ebp
	xor	r15d, r15d
.L3791:
	xor	edi, edi
	jmp	.L3652
	.p2align 4,,10
	.p2align 3
.L3801:
	mov	rax, QWORD PTR 832[rsp]
	not	edx
	and	edx, 120
	mov	rbx, QWORD PTR 16[rax]
	je	.L3820
	test	r15, r15
	je	.L3677
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	r15, rsi
	jb	.L3679
	.p2align 4
	.p2align 3
.L3681:
	test	rsi, rsi
	je	.L3680
	mov	r8, rsi
	mov	rdx, rbp
	call	memcpy
.L3680:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rsi
	mov	rcx, rbx
	add	rbp, rsi
	sub	r15, rsi
.LEHB64:
	call	[QWORD PTR [rax]]
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	r15, rsi
	jnb	.L3681
.L3795:
	test	r15, r15
	je	.L3677
.L3679:
	mov	r8, r15
	mov	rdx, rbp
	call	memcpy
	add	QWORD PTR 24[rbx], r15
	jmp	.L3677
	.p2align 4,,10
	.p2align 3
.L3672:
	movzx	ecx, WORD PTR 4[rbx]
	mov	rdx, QWORD PTR 832[rsp]
	call	_ZNKSt8__format5_SpecIcE12_M_get_widthISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRT_.part.0.isra.0
	jmp	.L3671
	.p2align 4,,10
	.p2align 3
.L3808:
	lea	r8, _ZNSt9__unicode9__v16_0_013__width_edgesE[rip]
	mov	eax, 206
	mov	r9, r8
	.p2align 4
	.p2align 3
.L3722:
	test	rax, rax
	jle	.L3821
.L3723:
	mov	rcx, rax
	sar	rcx
	cmp	edx, DWORD PTR [r9+rcx*4]
	jb	.L3757
	sub	rax, rcx
	lea	r9, 4[r9+rcx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3723
.L3821:
	sub	r9, r8
	mov	rax, r9
	shr	r9, 63
	sar	rax, 2
	add	rax, r9
	and	eax, 1
	sub	rax, r9
	add	eax, 1
	jmp	.L3720
	.p2align 4,,10
	.p2align 3
.L3757:
	mov	rax, rcx
	jmp	.L3722
	.p2align 4,,10
	.p2align 3
.L3805:
	test	r13, r13
	jne	.L3685
.L3752:
	xor	edi, edi
	jmp	.L3710
.L3796:
	cmp	r8b, 2
	je	.L3609
	cmp	r8b, 4
	jne	.L3620
	.p2align 4
	.p2align 3
.L3610:
	mov	rsi, QWORD PTR 832[rsp]
	movzx	r8d, WORD PTR 6[rbx]
	movzx	edx, BYTE PTR [rsi]
	mov	rcx, rdx
	and	ecx, 15
	cmp	r8, rcx
	jnb	.L3623
	mov	rsi, QWORD PTR [rsi]
	lea	rcx, [r8+r8*4]
	sal	r8, 4
	mov	rdx, rsi
	mov	QWORD PTR 48[rsp], rsi
	mov	rsi, QWORD PTR 832[rsp]
	shr	rdx, 4
	add	r8, QWORD PTR 8[rsi]
	shr	rdx, cl
	movdqa	xmm5, XMMWORD PTR [r8]
	and	edx, 31
	movaps	XMMWORD PTR 352[rsp], xmm5
.L3624:
	mov	BYTE PTR 368[rsp], dl
	lea	rcx, .L3628[rip]
	movzx	edx, dl
	movdqa	xmm2, XMMWORD PTR 352[rsp]
	movdqa	xmm1, XMMWORD PTR 368[rsp]
	movsxd	rdx, DWORD PTR [rcx+rdx*4]
	movaps	XMMWORD PTR 416[rsp], xmm2
	add	rdx, rcx
	movaps	XMMWORD PTR 432[rsp], xmm1
	jmp	rdx
	.section .rdata,"dr"
	.align 4
.L3628:
	.long	.L3625-.L3628
	.long	.L3633-.L3628
	.long	.L3633-.L3628
	.long	.L3632-.L3628
	.long	.L3631-.L3628
	.long	.L3630-.L3628
	.long	.L3629-.L3628
	.long	.L3633-.L3628
	.long	.L3633-.L3628
	.long	.L3633-.L3628
	.long	.L3633-.L3628
	.long	.L3633-.L3628
	.long	.L3633-.L3628
	.long	.L3633-.L3628
	.long	.L3633-.L3628
	.long	.L3633-.L3628
	.section	.text$_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L3809:
	mov	QWORD PTR 80[rsp], r10
	mov	QWORD PTR 88[rsp], rcx
.L3793:
	mov	rcx, rbx
	lea	rdx, 80[rsp]
	mov	r8d, 12
	call	_ZNSt8__format15__write_escapedIcNS_10_Sink_iterIcEEEET0_S3_St17basic_string_viewIT_St11char_traitsIS5_EENS_10_Term_charE
	mov	rbx, rax
	jmp	.L3677
	.p2align 4,,10
	.p2align 3
.L3735:
	xor	edi, edi
	jmp	.L3653
.L3623:
	and	edx, 15
	je	.L3822
.L3625:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L3630:
	mov	rsi, QWORD PTR 416[rsp]
	test	rsi, rsi
	jns	.L3622
.L3633:
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L3631:
	mov	esi, DWORD PTR 416[rsp]
	jmp	.L3622
.L3632:
	movsxd	rsi, DWORD PTR 416[rsp]
	test	esi, esi
	jns	.L3622
	jmp	.L3633
	.p2align 4,,10
	.p2align 3
.L3629:
	mov	rsi, QWORD PTR 416[rsp]
	cmp	rsi, -1
	jne	.L3622
	jmp	.L3620
	.p2align 4,,10
	.p2align 3
.L3820:
	mov	QWORD PTR 80[rsp], r15
	mov	QWORD PTR 88[rsp], rbp
	jmp	.L3793
	.p2align 4,,10
	.p2align 3
.L3798:
	lea	rdx, _ZNSt9__unicode9__v16_0_013__width_edgesE[rip]
	mov	eax, 206
	mov	r9, rdx
	.p2align 4
	.p2align 3
.L3663:
	test	rax, rax
	jle	.L3823
.L3664:
	mov	rcx, rax
	sar	rcx
	cmp	r13d, DWORD PTR [r9+rcx*4]
	jb	.L3738
	sub	rax, rcx
	lea	r9, 4[r9+rcx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3664
.L3823:
	sub	r9, rdx
	mov	rax, r9
	shr	r9, 63
	sar	rax, 2
	add	rax, r9
	and	eax, 1
	sub	rax, r9
	lea	edi, 1[rax]
	jmp	.L3665
	.p2align 4,,10
	.p2align 3
.L3738:
	mov	rax, rcx
	jmp	.L3663
	.p2align 4,,10
	.p2align 3
.L3817:
	lea	rdx, _ZNSt9__unicode9__v16_0_013__width_edgesE[rip]
	mov	ecx, 206
	mov	r11, rdx
	.p2align 4
	.p2align 3
.L3644:
	test	rcx, rcx
	jle	.L3824
.L3645:
	mov	r8, rcx
	sar	r8
	cmp	eax, DWORD PTR [r11+r8*4]
	jb	.L3730
	sub	rcx, r8
	lea	r11, 4[r11+r8*4]
	sub	rcx, 1
	test	rcx, rcx
	jg	.L3645
.L3824:
	sub	r11, rdx
	mov	rax, r11
	shr	r11, 63
	sar	rax, 2
	add	rax, r11
	and	eax, 1
	sub	rax, r11
	lea	edi, 1[rax]
	jmp	.L3642
	.p2align 4,,10
	.p2align 3
.L3730:
	mov	rcx, r8
	jmp	.L3644
	.p2align 4,,10
	.p2align 3
.L3810:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	r10, rsi
	jb	.L3679
	.p2align 4
	.p2align 3
.L3618:
	test	rsi, rsi
	je	.L3617
	mov	r8, rsi
	mov	rdx, rbp
	call	memcpy
.L3617:
	mov	rax, QWORD PTR [rbx]
	add	QWORD PTR 24[rbx], rsi
	mov	rcx, rbx
	add	rbp, rsi
	sub	r15, rsi
	call	[QWORD PTR [rax]]
.LEHE64:
	mov	rcx, QWORD PTR 24[rbx]
	mov	rsi, QWORD PTR 16[rbx]
	mov	rax, rcx
	sub	rax, QWORD PTR 8[rbx]
	sub	rsi, rax
	cmp	r15, rsi
	jnb	.L3618
	jmp	.L3795
	.p2align 4,,10
	.p2align 3
.L3813:
	xor	r15d, r15d
	xor	r13d, r13d
	xor	edi, edi
	jmp	.L3710
	.p2align 4,,10
	.p2align 3
.L3684:
	movabs	rax, 9223372036854775806
	sub	rax, rdx
	cmp	rax, r13
	jb	.L3825
	mov	rcx, QWORD PTR 704[rsp]
	mov	eax, 15
	cmp	rcx, QWORD PTR 48[rsp]
	lea	rdi, 0[r13+rdx]
	cmovne	rax, QWORD PTR 720[rsp]
	cmp	rax, rdi
	jb	.L3689
	add	rcx, rdx
	cmp	r13, 1
	je	.L3826
	mov	r8, r13
	mov	rdx, r15
	call	memcpy
.L3691:
	mov	rax, QWORD PTR 704[rsp]
	mov	QWORD PTR 712[rsp], rdi
	mov	BYTE PTR [rax+rdi], 0
	mov	r15, QWORD PTR 424[rsp]
	mov	r13, QWORD PTR 712[rsp]
	mov	QWORD PTR 440[rsp], r15
	test	r13, r13
	je	.L3752
	mov	r15, QWORD PTR 704[rsp]
	movq	xmm0, r15
	punpcklqdq	xmm0, xmm0
	cmp	rsi, -1
	je	.L3686
	jmp	.L3685
.L3814:
	mov	r13, QWORD PTR 384[rsp]
	sub	r13, r15
	jmp	.L3710
.L3822:
	mov	rsi, QWORD PTR 832[rsp]
	mov	rsi, QWORD PTR [rsi]
	mov	rdx, rsi
	mov	QWORD PTR 48[rsp], rsi
	shr	rdx, 4
	cmp	r8, rdx
	jnb	.L3625
	mov	rsi, QWORD PTR 832[rsp]
	sal	r8, 5
	add	r8, QWORD PTR 8[rsi]
	movdqu	xmm5, XMMWORD PTR [r8]
	movzx	edx, BYTE PTR 16[r8]
	movaps	XMMWORD PTR 352[rsp], xmm5
	jmp	.L3624
.L3689:
	mov	QWORD PTR 32[rsp], r13
	lea	rbp, 704[rsp]
	mov	r9, r15
	xor	r8d, r8d
	mov	rcx, rbp
.LEHB65:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	jmp	.L3691
.L3807:
	lea	rdx, _ZNSt9__unicode9__v16_0_013__width_edgesE[rip]
	mov	eax, 206
	mov	r11, rdx
	.p2align 4
	.p2align 3
.L3717:
	test	rax, rax
	jle	.L3827
.L3718:
	mov	rcx, rax
	mov	edi, DWORD PTR 64[rsp]
	sar	rcx
	cmp	edi, DWORD PTR [r11+rcx*4]
	jb	.L3755
	sub	rax, rcx
	lea	r11, 4[r11+rcx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3718
.L3827:
	sub	r11, rdx
	mov	rax, r11
	shr	r11, 63
	sar	rax, 2
	add	rax, r11
	and	eax, 1
	sub	rax, r11
	lea	edi, 1[rax]
	jmp	.L3715
	.p2align 4,,10
	.p2align 3
.L3755:
	mov	rax, rcx
	jmp	.L3717
.L3812:
	lea	rdx, _ZNSt9__unicode9__v16_0_013__width_edgesE[rip]
	mov	eax, 206
	mov	r11, rdx
	.p2align 4
	.p2align 3
.L3702:
	test	rax, rax
	jle	.L3828
.L3703:
	mov	rcx, rax
	mov	edi, DWORD PTR 68[rsp]
	sar	rcx
	cmp	edi, DWORD PTR [r11+rcx*4]
	jb	.L3747
	sub	rax, rcx
	lea	r11, 4[r11+rcx*4]
	sub	rax, 1
	test	rax, rax
	jg	.L3703
.L3828:
	sub	r11, rdx
	mov	rax, r11
	shr	r11, 63
	sar	rax, 2
	add	rax, r11
	and	eax, 1
	sub	rax, r11
	lea	edi, 1[rax]
	jmp	.L3700
	.p2align 4,,10
	.p2align 3
.L3747:
	mov	rax, rcx
	jmp	.L3702
.L3826:
	movzx	eax, BYTE PTR [r15]
	mov	BYTE PTR [rcx], al
	jmp	.L3691
.L3825:
	lea	rcx, .LC14[rip]
	lea	rbp, 704[rsp]
	call	_ZSt20__throw_length_errorPKc
.LEHE65:
.L3758:
	mov	rbx, rax
.L3726:
	mov	rcx, rbp
	mov	QWORD PTR 416[rsp], r12
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB66:
	call	_Unwind_Resume
	nop
.LEHE66:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5618:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5618-.LLSDACSB5618
.LLSDACSB5618:
	.uleb128 .LEHB62-.LFB5618
	.uleb128 .LEHE62-.LEHB62
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB63-.LFB5618
	.uleb128 .LEHE63-.LEHB63
	.uleb128 .L3758-.LFB5618
	.uleb128 0
	.uleb128 .LEHB64-.LFB5618
	.uleb128 .LEHE64-.LEHB64
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB65-.LFB5618
	.uleb128 .LEHE65-.LEHB65
	.uleb128 .L3758-.LFB5618
	.uleb128 0
	.uleb128 .LEHB66-.LFB5618
	.uleb128 .LEHE66-.LEHB66
	.uleb128 0
	.uleb128 0
.LLSDACSE5618:
	.section	.text$_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC47:
	.ascii "format error: format-spec contains invalid formatting options for 'bool'\0"
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
	.def	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE:
.LFB5262:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	mov	rbx, rdx
	movzx	r8d, r8b
	lea	rdx, .L3832[rip]
	mov	rsi, rcx
	movsxd	rax, DWORD PTR [rdx+r8*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L3832:
	.long	.L3847-.L3832
	.long	.L3846-.L3832
	.long	.L3845-.L3832
	.long	.L3844-.L3832
	.long	.L3843-.L3832
	.long	.L3842-.L3832
	.long	.L3841-.L3832
	.long	.L3840-.L3832
	.long	.L3839-.L3832
	.long	.L3838-.L3832
	.long	.L3837-.L3832
	.long	.L3836-.L3832
	.long	.L3835-.L3832
	.long	.L3834-.L3832
	.long	.L3833-.L3832
	.long	.L3831-.L3832
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L3833:
	mov	r9, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	r8d, 1
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r9]
	mov	QWORD PTR 40[rsp], r9
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	r9, QWORD PTR 40[rsp]
	movdqa	xmm2, XMMWORD PTR [rsi]
	lea	rdx, 48[rsp]
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[r9], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rax]
	movaps	XMMWORD PTR 48[rsp], xmm2
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
.L3829:
	add	rsp, 120
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L3831:
	mov	r9, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	r8d, 1
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r9]
	mov	QWORD PTR 40[rsp], r9
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	r9, QWORD PTR 40[rsp]
	movdqa	xmm3, XMMWORD PTR [rsi]
	lea	rdx, 48[rsp]
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[r9], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rax]
	movaps	XMMWORD PTR 48[rsp], xmm3
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatIoNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L3829
	.p2align 4,,10
	.p2align 3
.L3846:
	mov	r9, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	xor	r8d, r8d
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r9]
	mov	QWORD PTR 40[rsp], r9
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	test	BYTE PTR 101[rsp], 120
	mov	rcx, QWORD PTR 32[rsp]
	mov	r9, QWORD PTR 40[rsp]
	jne	.L3848
	test	BYTE PTR 100[rsp], 92
	jne	.L3854
.L3848:
	mov	QWORD PTR 8[r9], rax
	mov	rax, QWORD PTR [rbx]
	movzx	edx, BYTE PTR [rsi]
	mov	rbx, QWORD PTR 56[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L3829
	.p2align 4,,10
	.p2align 3
.L3845:
	mov	rdx, rcx
	mov	rcx, rbx
	add	rsp, 120
	pop	rbx
	pop	rsi
	jmp	_ZZNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcE13_M_format_argEyENKUlRT_E_clIcEEDaS5_
	.p2align 4,,10
	.p2align 3
.L3843:
	mov	r9, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	r8d, 1
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r9]
	mov	QWORD PTR 40[rsp], r9
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	r9, QWORD PTR 40[rsp]
	mov	edx, DWORD PTR [rsi]
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[r9], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatIjNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L3829
	.p2align 4,,10
	.p2align 3
.L3842:
	mov	r9, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	r8d, 1
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r9]
	mov	QWORD PTR 40[rsp], r9
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	r9, QWORD PTR 40[rsp]
	mov	rdx, QWORD PTR [rsi]
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[r9], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatIxNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L3829
	.p2align 4,,10
	.p2align 3
.L3844:
	mov	r9, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	r8d, 1
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r9]
	mov	QWORD PTR 40[rsp], r9
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	r9, QWORD PTR 40[rsp]
	mov	edx, DWORD PTR [rsi]
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[r9], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L3829
	.p2align 4,,10
	.p2align 3
.L3841:
	mov	r9, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	r8d, 1
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r9]
	mov	QWORD PTR 40[rsp], r9
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	mov	r9, QWORD PTR 40[rsp]
	mov	rdx, QWORD PTR [rsi]
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[r9], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rax]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_intIcE6formatIyNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L3829
	.p2align 4,,10
	.p2align 3
.L3840:
	mov	r8, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r8]
	mov	QWORD PTR 40[rsp], r8
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	mov	r8, QWORD PTR 40[rsp]
	movss	xmm1, DWORD PTR [rsi]
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[r8], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rax]
	mov	r8, rbx
	call	_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L3829
	.p2align 4,,10
	.p2align 3
.L3839:
	mov	r8, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r8]
	mov	QWORD PTR 40[rsp], r8
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	mov	r8, QWORD PTR 40[rsp]
	movsd	xmm1, QWORD PTR [rsi]
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[r8], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rax]
	mov	r8, rbx
	call	_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L3829
	.p2align 4,,10
	.p2align 3
.L3838:
	mov	r8, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r8]
	mov	QWORD PTR 40[rsp], r8
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	mov	r8, QWORD PTR 40[rsp]
	fld	TBYTE PTR [rsi]
	lea	rdx, 80[rsp]
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[r8], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rax]
	fstp	TBYTE PTR 80[rsp]
	mov	r8, rbx
	call	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L3829
	.p2align 4,,10
	.p2align 3
.L3837:
	mov	r8, QWORD PTR [rbx]
	lea	r9, 100[rsp]
	mov	QWORD PTR 100[rsp], 0
	mov	rcx, r9
	mov	QWORD PTR 32[rsp], r9
	lea	rdx, 8[r8]
	mov	QWORD PTR 40[rsp], r8
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE
	mov	r8, QWORD PTR 40[rsp]
	mov	QWORD PTR 8[r8], rax
	mov	rsi, QWORD PTR [rsi]
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rsi
	mov	rbx, QWORD PTR 56[rax]
	call	strlen
	mov	QWORD PTR 72[rsp], rsi
	mov	QWORD PTR 64[rsp], rax
.L3853:
	mov	rcx, QWORD PTR 32[rsp]
	lea	rdx, 64[rsp]
	mov	r8, rbx
	call	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
	mov	QWORD PTR 16[rbx], rax
	add	rsp, 120
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L3836:
	mov	r8, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	QWORD PTR 100[rsp], 0
	mov	DWORD PTR 108[rsp], 32
	lea	rdx, 8[r8]
	mov	QWORD PTR 40[rsp], r8
	mov	QWORD PTR 32[rsp], rcx
	call	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE
	mov	r8, QWORD PTR 40[rsp]
	movdqu	xmm0, XMMWORD PTR [rsi]
	mov	QWORD PTR 8[r8], rax
	mov	rax, QWORD PTR [rbx]
	mov	rbx, QWORD PTR 56[rax]
	movaps	XMMWORD PTR 64[rsp], xmm0
	jmp	.L3853
	.p2align 4,,10
	.p2align 3
.L3835:
	mov	r8, QWORD PTR [rbx]
	lea	rcx, 100[rsp]
	mov	QWORD PTR 100[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, 8[r8]
	mov	QWORD PTR 40[rsp], r8
	mov	DWORD PTR 108[rsp], 32
	call	_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE
	mov	r8, QWORD PTR 40[rsp]
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[r8], rax
	mov	rax, QWORD PTR [rbx]
	mov	rdx, QWORD PTR [rsi]
	mov	rbx, QWORD PTR 56[rax]
	mov	r8, rbx
	call	_ZNKSt9formatterIPKvcE6formatINSt8__format10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorES1_RS9_
	mov	QWORD PTR 16[rbx], rax
	jmp	.L3829
	.p2align 4,,10
	.p2align 3
.L3834:
	mov	rcx, QWORD PTR [rbx]
	mov	rax, QWORD PTR 8[rsi]
	mov	r8, QWORD PTR [rsi]
	mov	rdx, QWORD PTR 56[rcx]
	add	rcx, 8
	add	rsp, 120
	pop	rbx
	pop	rsi
	rex.W jmp	rax
.L3847:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
.L3854:
	lea	rcx, .LC47[rip]
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
.LFB5259:
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	mov	r10, QWORD PTR 56[rcx]
	movzx	eax, BYTE PTR [r10]
	mov	r9, rcx
	mov	rcx, rax
	and	ecx, 15
	cmp	rdx, rcx
	jnb	.L3856
	mov	r8, QWORD PTR [r10]
	lea	rcx, [rdx+rdx*4]
	sal	rdx, 4
	add	rdx, QWORD PTR 8[r10]
	movdqa	xmm2, XMMWORD PTR [rdx]
	shr	r8, 4
	shr	r8, cl
	movaps	XMMWORD PTR 48[rsp], xmm2
	mov	eax, r8d
	and	r8d, 31
	and	eax, 31
.L3857:
	mov	BYTE PTR 64[rsp], al
	movdqa	xmm0, XMMWORD PTR 48[rsp]
	lea	rdx, 40[rsp]
	lea	rcx, 80[rsp]
	movdqa	xmm1, XMMWORD PTR 64[rsp]
	mov	QWORD PTR 40[rsp], r9
	movaps	XMMWORD PTR 80[rsp], xmm0
	movaps	XMMWORD PTR 96[rsp], xmm1
	call	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
	nop
	add	rsp, 120
	ret
	.p2align 4,,10
	.p2align 3
.L3856:
	and	eax, 15
	test	al, al
	jne	.L3858
	mov	rcx, QWORD PTR [r10]
	xor	r8d, r8d
	shr	rcx, 4
	cmp	rdx, rcx
	jnb	.L3857
	sal	rdx, 5
	add	rdx, QWORD PTR 8[r10]
	movdqu	xmm3, XMMWORD PTR [rdx]
	movzx	r8d, BYTE PTR 16[rdx]
	movaps	XMMWORD PTR 48[rsp], xmm3
	mov	eax, r8d
	jmp	.L3857
	.p2align 4,,10
	.p2align 3
.L3858:
	xor	r8d, r8d
	xor	eax, eax
	jmp	.L3857
	.seh_endproc
	.section .rdata,"dr"
	.align 32
CSWTCH.641:
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
	.globl	_ZTSNSt8__format14_Fixedbuf_sinkIcEE
	.section	.rdata$_ZTSNSt8__format14_Fixedbuf_sinkIcEE,"dr"
	.linkonce same_size
	.align 32
_ZTSNSt8__format14_Fixedbuf_sinkIcEE:
	.ascii "NSt8__format14_Fixedbuf_sinkIcEE\0"
	.globl	_ZTINSt8__format14_Fixedbuf_sinkIcEE
	.section	.rdata$_ZTINSt8__format14_Fixedbuf_sinkIcEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt8__format14_Fixedbuf_sinkIcEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt8__format14_Fixedbuf_sinkIcEE
	.quad	_ZTINSt8__format5_SinkIcEE
	.globl	_ZTVNSt8__format14_Fixedbuf_sinkIcEE
	.section	.rdata$_ZTVNSt8__format14_Fixedbuf_sinkIcEE,"dr"
	.linkonce same_size
	.align 8
_ZTVNSt8__format14_Fixedbuf_sinkIcEE:
	.quad	0
	.quad	_ZTINSt8__format14_Fixedbuf_sinkIcEE
	.quad	_ZNSt8__format14_Fixedbuf_sinkIcE11_M_overflowEv
	.quad	_ZNSt8__format5_SinkIcE10_M_reserveEy
	.quad	_ZNSt8__format5_SinkIcE7_M_bumpEy
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
	.quad	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE10_M_reserveEy
	.quad	_ZNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE7_M_bumpEy
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
	.globl	_ZNSt9__unicode9__v16_0_014__xpicto_edgesE
	.section	.rdata$_ZNSt9__unicode9__v16_0_014__xpicto_edgesE,"dr"
	.linkonce same_size
	.align 32
_ZNSt9__unicode9__v16_0_014__xpicto_edgesE:
	.long	169
	.long	170
	.long	174
	.long	175
	.long	8252
	.long	8253
	.long	8265
	.long	8266
	.long	8482
	.long	8483
	.long	8505
	.long	8506
	.long	8596
	.long	8602
	.long	8617
	.long	8619
	.long	8986
	.long	8988
	.long	9000
	.long	9001
	.long	9096
	.long	9097
	.long	9167
	.long	9168
	.long	9193
	.long	9204
	.long	9208
	.long	9211
	.long	9410
	.long	9411
	.long	9642
	.long	9644
	.long	9654
	.long	9655
	.long	9664
	.long	9665
	.long	9723
	.long	9727
	.long	9728
	.long	9734
	.long	9735
	.long	9747
	.long	9748
	.long	9862
	.long	9872
	.long	9990
	.long	9992
	.long	10003
	.long	10004
	.long	10005
	.long	10006
	.long	10007
	.long	10013
	.long	10014
	.long	10017
	.long	10018
	.long	10024
	.long	10025
	.long	10035
	.long	10037
	.long	10052
	.long	10053
	.long	10055
	.long	10056
	.long	10060
	.long	10061
	.long	10062
	.long	10063
	.long	10067
	.long	10070
	.long	10071
	.long	10072
	.long	10083
	.long	10088
	.long	10133
	.long	10136
	.long	10145
	.long	10146
	.long	10160
	.long	10161
	.long	10175
	.long	10176
	.long	10548
	.long	10550
	.long	11013
	.long	11016
	.long	11035
	.long	11037
	.long	11088
	.long	11089
	.long	11093
	.long	11094
	.long	12336
	.long	12337
	.long	12349
	.long	12350
	.long	12951
	.long	12952
	.long	12953
	.long	12954
	.long	126976
	.long	127232
	.long	127245
	.long	127248
	.long	127279
	.long	127280
	.long	127340
	.long	127346
	.long	127358
	.long	127360
	.long	127374
	.long	127375
	.long	127377
	.long	127387
	.long	127405
	.long	127462
	.long	127489
	.long	127504
	.long	127514
	.long	127515
	.long	127535
	.long	127536
	.long	127538
	.long	127547
	.long	127548
	.long	127552
	.long	127561
	.long	127995
	.long	128000
	.long	128318
	.long	128326
	.long	128592
	.long	128640
	.long	128768
	.long	128884
	.long	128896
	.long	128981
	.long	129024
	.long	129036
	.long	129040
	.long	129096
	.long	129104
	.long	129114
	.long	129120
	.long	129160
	.long	129168
	.long	129198
	.long	129280
	.long	129292
	.long	129339
	.long	129340
	.long	129350
	.long	129351
	.long	129792
	.long	130048
	.long	131070
	.globl	_ZNSt9__unicode9__v16_0_012__incb_edgesE
	.section	.rdata$_ZNSt9__unicode9__v16_0_012__incb_edgesE,"dr"
	.linkonce same_size
	.align 32
_ZNSt9__unicode9__v16_0_012__incb_edgesE:
	.long	3074
	.long	3520
	.long	4622
	.long	4648
	.long	5702
	.long	5880
	.long	5886
	.long	5888
	.long	5894
	.long	5900
	.long	5906
	.long	5912
	.long	5918
	.long	5920
	.long	6210
	.long	6252
	.long	6446
	.long	6528
	.long	6594
	.long	6596
	.long	7002
	.long	7028
	.long	7038
	.long	7060
	.long	7070
	.long	7076
	.long	7082
	.long	7096
	.long	7238
	.long	7240
	.long	7362
	.long	7468
	.long	7834
	.long	7876
	.long	8110
	.long	8144
	.long	8182
	.long	8184
	.long	8282
	.long	8296
	.long	8302
	.long	8336
	.long	8342
	.long	8352
	.long	8358
	.long	8376
	.long	8550
	.long	8560
	.long	8798
	.long	8832
	.long	9002
	.long	9096
	.long	9102
	.long	9228
	.long	9301
	.long	9450
	.long	9452
	.long	9458
	.long	9460
	.long	9478
	.long	9508
	.long	9542
	.long	9569
	.long	9600
	.long	9610
	.long	9616
	.long	9697
	.long	9728
	.long	9734
	.long	9736
	.long	9813
	.long	9892
	.long	9897
	.long	9924
	.long	9929
	.long	9932
	.long	9945
	.long	9960
	.long	9970
	.long	9972
	.long	9978
	.long	9980
	.long	9990
	.long	10004
	.long	10078
	.long	10080
	.long	10097
	.long	10104
	.long	10109
	.long	10112
	.long	10122
	.long	10128
	.long	10177
	.long	10184
	.long	10234
	.long	10236
	.long	10246
	.long	10252
	.long	10482
	.long	10484
	.long	10502
	.long	10508
	.long	10526
	.long	10532
	.long	10542
	.long	10552
	.long	10566
	.long	10568
	.long	10690
	.long	10696
	.long	10710
	.long	10712
	.long	10758
	.long	10764
	.long	10837
	.long	10916
	.long	10921
	.long	10948
	.long	10953
	.long	10960
	.long	10965
	.long	10984
	.long	10994
	.long	10996
	.long	11014
	.long	11032
	.long	11038
	.long	11044
	.long	11146
	.long	11152
	.long	11237
	.long	11242
	.long	11264
	.long	11270
	.long	11272
	.long	11349
	.long	11428
	.long	11433
	.long	11460
	.long	11465
	.long	11472
	.long	11477
	.long	11496
	.long	11506
	.long	11508
	.long	11514
	.long	11520
	.long	11526
	.long	11540
	.long	11606
	.long	11616
	.long	11633
	.long	11640
	.long	11645
	.long	11648
	.long	11658
	.long	11664
	.long	11717
	.long	11720
	.long	11786
	.long	11788
	.long	12026
	.long	12028
	.long	12034
	.long	12036
	.long	12086
	.long	12088
	.long	12126
	.long	12128
	.long	12290
	.long	12292
	.long	12306
	.long	12308
	.long	12373
	.long	12452
	.long	12457
	.long	12520
	.long	12530
	.long	12532
	.long	12538
	.long	12548
	.long	12570
	.long	12580
	.long	12586
	.long	12596
	.long	12630
	.long	12636
	.long	12641
	.long	12652
	.long	12682
	.long	12688
	.long	12806
	.long	12808
	.long	13042
	.long	13044
	.long	13054
	.long	13060
	.long	13066
	.long	13068
	.long	13082
	.long	13092
	.long	13098
	.long	13112
	.long	13142
	.long	13148
	.long	13194
	.long	13200
	.long	13314
	.long	13320
	.long	13397
	.long	13550
	.long	13556
	.long	13562
	.long	13564
	.long	13574
	.long	13588
	.long	13662
	.long	13664
	.long	13706
	.long	13712
	.long	13830
	.long	13832
	.long	14122
	.long	14124
	.long	14142
	.long	14144
	.long	14154
	.long	14164
	.long	14170
	.long	14172
	.long	14206
	.long	14208
	.long	14534
	.long	14536
	.long	14546
	.long	14572
	.long	14622
	.long	14652
	.long	15046
	.long	15048
	.long	15058
	.long	15092
	.long	15138
	.long	15164
	.long	15458
	.long	15464
	.long	15574
	.long	15576
	.long	15582
	.long	15584
	.long	15590
	.long	15592
	.long	15814
	.long	15868
	.long	15874
	.long	15892
	.long	15898
	.long	15904
	.long	15926
	.long	15968
	.long	15974
	.long	16116
	.long	16154
	.long	16156
	.long	16566
	.long	16580
	.long	16586
	.long	16608
	.long	16614
	.long	16620
	.long	16630
	.long	16636
	.long	16738
	.long	16744
	.long	16762
	.long	16772
	.long	16838
	.long	16852
	.long	16906
	.long	16908
	.long	16918
	.long	16924
	.long	16950
	.long	16952
	.long	17014
	.long	17016
	.long	19830
	.long	19840
	.long	23626
	.long	23640
	.long	23754
	.long	23764
	.long	23882
	.long	23888
	.long	24010
	.long	24016
	.long	24274
	.long	24280
	.long	24286
	.long	24312
	.long	24346
	.long	24348
	.long	24358
	.long	24400
	.long	24438
	.long	24440
	.long	24622
	.long	24632
	.long	24638
	.long	24640
	.long	25110
	.long	25116
	.long	25254
	.long	25256
	.long	25730
	.long	25740
	.long	25758
	.long	25764
	.long	25802
	.long	25804
	.long	25830
	.long	25840
	.long	26718
	.long	26724
	.long	26734
	.long	26736
	.long	26970
	.long	26972
	.long	26978
	.long	27004
	.long	27010
	.long	27012
	.long	27018
	.long	27020
	.long	27030
	.long	27060
	.long	27086
	.long	27124
	.long	27134
	.long	27136
	.long	27330
	.long	27452
	.long	27650
	.long	27664
	.long	27858
	.long	27896
	.long	27914
	.long	27924
	.long	28078
	.long	28112
	.long	28162
	.long	28168
	.long	28298
	.long	28312
	.long	28322
	.long	28344
	.long	28570
	.long	28572
	.long	28578
	.long	28584
	.long	28598
	.long	28600
	.long	28606
	.long	28624
	.long	28850
	.long	28880
	.long	28890
	.long	28896
	.long	29506
	.long	29516
	.long	29522
	.long	29572
	.long	29578
	.long	29604
	.long	29622
	.long	29624
	.long	29650
	.long	29652
	.long	29666
	.long	29672
	.long	30466
	.long	30720
	.long	32822
	.long	32824
	.long	33602
	.long	33732
	.long	46014
	.long	46024
	.long	46590
	.long	46592
	.long	46978
	.long	47104
	.long	49322
	.long	49344
	.long	49766
	.long	49772
	.long	170430
	.long	170444
	.long	170450
	.long	170488
	.long	170618
	.long	170624
	.long	170946
	.long	170952
	.long	172042
	.long	172044
	.long	172058
	.long	172060
	.long	172078
	.long	172080
	.long	172182
	.long	172188
	.long	172210
	.long	172212
	.long	172818
	.long	172824
	.long	172930
	.long	173000
	.long	173054
	.long	173056
	.long	173210
	.long	173240
	.long	173342
	.long	173384
	.long	173390
	.long	173392
	.long	173570
	.long	173580
	.long	173774
	.long	173776
	.long	173786
	.long	173800
	.long	173810
	.long	173816
	.long	173826
	.long	173828
	.long	173974
	.long	173976
	.long	174246
	.long	174268
	.long	174278
	.long	174284
	.long	174294
	.long	174300
	.long	174350
	.long	174352
	.long	174386
	.long	174388
	.long	174578
	.long	174580
	.long	174786
	.long	174788
	.long	174794
	.long	174804
	.long	174814
	.long	174820
	.long	174842
	.long	174848
	.long	174854
	.long	174856
	.long	175026
	.long	175032
	.long	175066
	.long	175068
	.long	176022
	.long	176024
	.long	176034
	.long	176036
	.long	176054
	.long	176056
	.long	257146
	.long	257148
	.long	260098
	.long	260160
	.long	260226
	.long	260288
	.long	261754
	.long	261760
	.long	264182
	.long	264184
	.long	265090
	.long	265092
	.long	265690
	.long	265708
	.long	272390
	.long	272400
	.long	272406
	.long	272412
	.long	272434
	.long	272448
	.long	272610
	.long	272620
	.long	272638
	.long	272640
	.long	273302
	.long	273308
	.long	275602
	.long	275616
	.long	275878
	.long	275896
	.long	277166
	.long	277172
	.long	277490
	.long	277504
	.long	277786
	.long	277828
	.long	278026
	.long	278040
	.long	278534
	.long	278536
	.long	278754
	.long	278812
	.long	278978
	.long	278980
	.long	278990
	.long	278996
	.long	279038
	.long	279048
	.long	279246
	.long	279260
	.long	279270
	.long	279276
	.long	279306
	.long	279308
	.long	279554
	.long	279564
	.long	279710
	.long	279728
	.long	279734
	.long	279764
	.long	280014
	.long	280016
	.long	280066
	.long	280072
	.long	280282
	.long	280316
	.long	280322
	.long	280324
	.long	280358
	.long	280372
	.long	280382
	.long	280384
	.long	280766
	.long	280776
	.long	280786
	.long	280800
	.long	280826
	.long	280828
	.long	280838
	.long	280840
	.long	281470
	.long	281472
	.long	281486
	.long	281516
	.long	281602
	.long	281608
	.long	281838
	.long	281844
	.long	281850
	.long	281852
	.long	281858
	.long	281860
	.long	281910
	.long	281912
	.long	281950
	.long	281952
	.long	282010
	.long	282036
	.long	282050
	.long	282068
	.long	282338
	.long	282340
	.long	282350
	.long	282372
	.long	282378
	.long	282380
	.long	282390
	.long	282392
	.long	282398
	.long	282408
	.long	282426
	.long	282436
	.long	282442
	.long	282444
	.long	282502
	.long	282508
	.long	282850
	.long	282880
	.long	282890
	.long	282900
	.long	282906
	.long	282908
	.long	283002
	.long	283004
	.long	283330
	.long	283332
	.long	283342
	.long	283364
	.long	283370
	.long	283372
	.long	283382
	.long	283384
	.long	283390
	.long	283396
	.long	283402
	.long	283408
	.long	284350
	.long	284352
	.long	284362
	.long	284376
	.long	284402
	.long	284408
	.long	284414
	.long	284420
	.long	284530
	.long	284536
	.long	284878
	.long	284908
	.long	284918
	.long	284920
	.long	284926
	.long	284932
	.long	285358
	.long	285360
	.long	285366
	.long	285368
	.long	285378
	.long	285408
	.long	285814
	.long	285816
	.long	285822
	.long	285824
	.long	285834
	.long	285848
	.long	285854
	.long	285872
	.long	286910
	.long	286944
	.long	286950
	.long	286956
	.long	287938
	.long	287940
	.long	287982
	.long	287996
	.long	288014
	.long	288016
	.long	288594
	.long	288608
	.long	288618
	.long	288624
	.long	288642
	.long	288644
	.long	288774
	.long	288812
	.long	288974
	.long	288996
	.long	289006
	.long	289020
	.long	289054
	.long	289056
	.long	289094
	.long	289116
	.long	289126
	.long	289136
	.long	289322
	.long	289372
	.long	289378
	.long	289384
	.long	291010
	.long	291036
	.long	291042
	.long	291064
	.long	291070
	.long	291072
	.long	291402
	.long	291488
	.long	291498
	.long	291524
	.long	291530
	.long	291536
	.long	291542
	.long	291548
	.long	292038
	.long	292060
	.long	292074
	.long	292076
	.long	292082
	.long	292088
	.long	292094
	.long	292120
	.long	292126
	.long	292128
	.long	292418
	.long	292424
	.long	292438
	.long	292440
	.long	292446
	.long	292448
	.long	293838
	.long	293844
	.long	293890
	.long	293896
	.long	294106
	.long	294124
	.long	294146
	.long	294156
	.long	294250
	.long	294252
	.long	315650
	.long	315652
	.long	315678
	.long	315736
	.long	361594
	.long	361640
	.long	361654
	.long	361664
	.long	371650
	.long	371668
	.long	371906
	.long	371932
	.long	376126
	.long	376128
	.long	376382
	.long	376396
	.long	376722
	.long	376724
	.long	376770
	.long	376776
	.long	455286
	.long	455292
	.long	474114
	.long	474296
	.long	474306
	.long	474396
	.long	476566
	.long	476584
	.long	476598
	.long	476620
	.long	476654
	.long	476684
	.long	476694
	.long	476720
	.long	476842
	.long	476856
	.long	477450
	.long	477460
	.long	485378
	.long	485596
	.long	485614
	.long	485812
	.long	485846
	.long	485848
	.long	485906
	.long	485908
	.long	485998
	.long	486016
	.long	486022
	.long	486080
	.long	491522
	.long	491548
	.long	491554
	.long	491620
	.long	491630
	.long	491656
	.long	491662
	.long	491668
	.long	491674
	.long	491692
	.long	492094
	.long	492096
	.long	492738
	.long	492764
	.long	494266
	.long	494268
	.long	494514
	.long	494528
	.long	496562
	.long	496576
	.long	497594
	.long	497600
	.long	500546
	.long	500572
	.long	501010
	.long	501036
	.long	511982
	.long	512000
	.long	3670146
	.long	3670528
	.long	3671042
	.long	3672000
	.globl	_ZNSt9__unicode9__v16_0_014__incb_linkersE
	.section	.rdata$_ZNSt9__unicode9__v16_0_014__incb_linkersE,"dr"
	.linkonce same_size
	.align 16
_ZNSt9__unicode9__v16_0_014__incb_linkersE:
	.long	2381
	.long	2509
	.long	2765
	.long	2893
	.long	3149
	.long	3405
	.globl	_ZNSt9__unicode9__v16_0_011__gcb_edgesE
	.section	.rdata$_ZNSt9__unicode9__v16_0_011__gcb_edgesE,"dr"
	.linkonce same_size
	.align 32
_ZNSt9__unicode9__v16_0_011__gcb_edgesE:
	.long	1
	.long	162
	.long	177
	.long	211
	.long	225
	.long	512
	.long	2033
	.long	2560
	.long	2769
	.long	2784
	.long	12292
	.long	14080
	.long	18484
	.long	18592
	.long	22804
	.long	23520
	.long	23540
	.long	23552
	.long	23572
	.long	23600
	.long	23620
	.long	23648
	.long	23668
	.long	23680
	.long	24581
	.long	24672
	.long	24836
	.long	25008
	.long	25025
	.long	25040
	.long	25780
	.long	26112
	.long	26372
	.long	26384
	.long	28004
	.long	28117
	.long	28128
	.long	28148
	.long	28240
	.long	28276
	.long	28304
	.long	28324
	.long	28384
	.long	28917
	.long	28928
	.long	28948
	.long	28960
	.long	29444
	.long	29872
	.long	31332
	.long	31504
	.long	32436
	.long	32576
	.long	32724
	.long	32736
	.long	33124
	.long	33184
	.long	33204
	.long	33344
	.long	33364
	.long	33408
	.long	33428
	.long	33504
	.long	34196
	.long	34240
	.long	35077
	.long	35104
	.long	35188
	.long	35328
	.long	36004
	.long	36389
	.long	36404
	.long	36918
	.long	36928
	.long	37796
	.long	37814
	.long	37828
	.long	37840
	.long	37862
	.long	37908
	.long	38038
	.long	38100
	.long	38118
	.long	38144
	.long	38164
	.long	38272
	.long	38436
	.long	38464
	.long	38932
	.long	38950
	.long	38976
	.long	39876
	.long	39888
	.long	39908
	.long	39926
	.long	39956
	.long	40016
	.long	40054
	.long	40080
	.long	40118
	.long	40148
	.long	40160
	.long	40308
	.long	40320
	.long	40484
	.long	40512
	.long	40932
	.long	40944
	.long	40980
	.long	41014
	.long	41024
	.long	41924
	.long	41936
	.long	41958
	.long	42004
	.long	42032
	.long	42100
	.long	42128
	.long	42164
	.long	42208
	.long	42260
	.long	42272
	.long	42756
	.long	42784
	.long	42836
	.long	42848
	.long	43028
	.long	43062
	.long	43072
	.long	43972
	.long	43984
	.long	44006
	.long	44052
	.long	44128
	.long	44148
	.long	44182
	.long	44192
	.long	44214
	.long	44244
	.long	44256
	.long	44580
	.long	44608
	.long	44964
	.long	45056
	.long	45076
	.long	45094
	.long	45120
	.long	46020
	.long	46032
	.long	46052
	.long	46086
	.long	46100
	.long	46160
	.long	46198
	.long	46224
	.long	46262
	.long	46292
	.long	46304
	.long	46420
	.long	46464
	.long	46628
	.long	46656
	.long	47140
	.long	47152
	.long	48100
	.long	48118
	.long	48132
	.long	48150
	.long	48176
	.long	48230
	.long	48272
	.long	48294
	.long	48340
	.long	48352
	.long	48500
	.long	48512
	.long	49156
	.long	49174
	.long	49220
	.long	49232
	.long	50116
	.long	50128
	.long	50148
	.long	50198
	.long	50256
	.long	50276
	.long	50320
	.long	50340
	.long	50400
	.long	50516
	.long	50544
	.long	50724
	.long	50752
	.long	51220
	.long	51238
	.long	51264
	.long	52164
	.long	52176
	.long	52198
	.long	52212
	.long	52246
	.long	52260
	.long	52278
	.long	52304
	.long	52324
	.long	52368
	.long	52388
	.long	52448
	.long	52564
	.long	52592
	.long	52772
	.long	52800
	.long	53046
	.long	53056
	.long	53252
	.long	53286
	.long	53312
	.long	54196
	.long	54224
	.long	54244
	.long	54262
	.long	54292
	.long	54352
	.long	54374
	.long	54416
	.long	54438
	.long	54484
	.long	54501
	.long	54512
	.long	54644
	.long	54656
	.long	54820
	.long	54848
	.long	55316
	.long	55334
	.long	55360
	.long	56484
	.long	56496
	.long	56564
	.long	56582
	.long	56612
	.long	56656
	.long	56676
	.long	56688
	.long	56710
	.long	56820
	.long	56832
	.long	57126
	.long	57152
	.long	58132
	.long	58144
	.long	58166
	.long	58180
	.long	58288
	.long	58484
	.long	58608
	.long	60180
	.long	60192
	.long	60214
	.long	60228
	.long	60368
	.long	60548
	.long	60656
	.long	61828
	.long	61856
	.long	62292
	.long	62304
	.long	62324
	.long	62336
	.long	62356
	.long	62368
	.long	62438
	.long	62464
	.long	63252
	.long	63478
	.long	63492
	.long	63568
	.long	63588
	.long	63616
	.long	63700
	.long	63872
	.long	63892
	.long	64464
	.long	64612
	.long	64624
	.long	66260
	.long	66326
	.long	66340
	.long	66432
	.long	66452
	.long	66486
	.long	66516
	.long	66544
	.long	66918
	.long	66948
	.long	66976
	.long	67044
	.long	67088
	.long	67348
	.long	67408
	.long	67620
	.long	67632
	.long	67654
	.long	67668
	.long	67696
	.long	67796
	.long	67808
	.long	68052
	.long	68064
	.long	69639
	.long	71176
	.long	72329
	.long	73728
	.long	79316
	.long	79360
	.long	94500
	.long	94560
	.long	95012
	.long	95056
	.long	95524
	.long	95552
	.long	96036
	.long	96064
	.long	97092
	.long	97126
	.long	97140
	.long	97254
	.long	97380
	.long	97398
	.long	97428
	.long	97600
	.long	97748
	.long	97760
	.long	98484
	.long	98529
	.long	98548
	.long	98560
	.long	100436
	.long	100464
	.long	101012
	.long	101024
	.long	102916
	.long	102966
	.long	103028
	.long	103062
	.long	103104
	.long	103174
	.long	103204
	.long	103222
	.long	103316
	.long	103360
	.long	106868
	.long	106902
	.long	106932
	.long	106944
	.long	107862
	.long	107876
	.long	107894
	.long	107908
	.long	108016
	.long	108036
	.long	108048
	.long	108068
	.long	108080
	.long	108116
	.long	108246
	.long	108340
	.long	108496
	.long	108532
	.long	108544
	.long	109316
	.long	109808
	.long	110596
	.long	110662
	.long	110672
	.long	111428
	.long	111590
	.long	111652
	.long	111696
	.long	112308
	.long	112448
	.long	112644
	.long	112678
	.long	112688
	.long	113174
	.long	113188
	.long	113254
	.long	113284
	.long	113376
	.long	114276
	.long	114294
	.long	114308
	.long	114342
	.long	114388
	.long	114406
	.long	114420
	.long	114496
	.long	115270
	.long	115396
	.long	115526
	.long	115556
	.long	115584
	.long	118020
	.long	118064
	.long	118084
	.long	118294
	.long	118308
	.long	118416
	.long	118484
	.long	118496
	.long	118596
	.long	118608
	.long	118646
	.long	118660
	.long	118688
	.long	121860
	.long	122880
	.long	131249
	.long	131268
	.long	131290
	.long	131297
	.long	131328
	.long	131713
	.long	131824
	.long	132609
	.long	132864
	.long	134404
	.long	134928
	.long	184052
	.long	184096
	.long	186356
	.long	186368
	.long	187908
	.long	188416
	.long	197284
	.long	197376
	.long	199060
	.long	199088
	.long	681716
	.long	681776
	.long	681796
	.long	681952
	.long	682468
	.long	682496
	.long	683780
	.long	683808
	.long	688164
	.long	688176
	.long	688228
	.long	688240
	.long	688308
	.long	688320
	.long	688694
	.long	688724
	.long	688758
	.long	688768
	.long	688836
	.long	688848
	.long	690182
	.long	690208
	.long	691014
	.long	691268
	.long	691296
	.long	691716
	.long	692000
	.long	692212
	.long	692224
	.long	692836
	.long	692960
	.long	693364
	.long	693542
	.long	693556
	.long	693568
	.long	693767
	.long	694224
	.long	694276
	.long	694326
	.long	694336
	.long	695092
	.long	695110
	.long	695140
	.long	695206
	.long	695236
	.long	695270
	.long	695300
	.long	695312
	.long	695892
	.long	695904
	.long	696980
	.long	697078
	.long	697108
	.long	697142
	.long	697172
	.long	697200
	.long	697396
	.long	697408
	.long	697540
	.long	697558
	.long	697568
	.long	698308
	.long	698320
	.long	699140
	.long	699152
	.long	699172
	.long	699216
	.long	699252
	.long	699280
	.long	699364
	.long	699392
	.long	699412
	.long	699424
	.long	700086
	.long	700100
	.long	700134
	.long	700160
	.long	700246
	.long	700260
	.long	700272
	.long	704054
	.long	704084
	.long	704102
	.long	704132
	.long	704150
	.long	704176
	.long	704198
	.long	704212
	.long	704224
	.long	704523
	.long	704540
	.long	704971
	.long	704988
	.long	705419
	.long	705436
	.long	705867
	.long	705884
	.long	706315
	.long	706332
	.long	706763
	.long	706780
	.long	707211
	.long	707228
	.long	707659
	.long	707676
	.long	708107
	.long	708124
	.long	708555
	.long	708572
	.long	709003
	.long	709020
	.long	709451
	.long	709468
	.long	709899
	.long	709916
	.long	710347
	.long	710364
	.long	710795
	.long	710812
	.long	711243
	.long	711260
	.long	711691
	.long	711708
	.long	712139
	.long	712156
	.long	712587
	.long	712604
	.long	713035
	.long	713052
	.long	713483
	.long	713500
	.long	713931
	.long	713948
	.long	714379
	.long	714396
	.long	714827
	.long	714844
	.long	715275
	.long	715292
	.long	715723
	.long	715740
	.long	716171
	.long	716188
	.long	716619
	.long	716636
	.long	717067
	.long	717084
	.long	717515
	.long	717532
	.long	717963
	.long	717980
	.long	718411
	.long	718428
	.long	718859
	.long	718876
	.long	719307
	.long	719324
	.long	719755
	.long	719772
	.long	720203
	.long	720220
	.long	720651
	.long	720668
	.long	721099
	.long	721116
	.long	721547
	.long	721564
	.long	721995
	.long	722012
	.long	722443
	.long	722460
	.long	722891
	.long	722908
	.long	723339
	.long	723356
	.long	723787
	.long	723804
	.long	724235
	.long	724252
	.long	724683
	.long	724700
	.long	725131
	.long	725148
	.long	725579
	.long	725596
	.long	726027
	.long	726044
	.long	726475
	.long	726492
	.long	726923
	.long	726940
	.long	727371
	.long	727388
	.long	727819
	.long	727836
	.long	728267
	.long	728284
	.long	728715
	.long	728732
	.long	729163
	.long	729180
	.long	729611
	.long	729628
	.long	730059
	.long	730076
	.long	730507
	.long	730524
	.long	730955
	.long	730972
	.long	731403
	.long	731420
	.long	731851
	.long	731868
	.long	732299
	.long	732316
	.long	732747
	.long	732764
	.long	733195
	.long	733212
	.long	733643
	.long	733660
	.long	734091
	.long	734108
	.long	734539
	.long	734556
	.long	734987
	.long	735004
	.long	735435
	.long	735452
	.long	735883
	.long	735900
	.long	736331
	.long	736348
	.long	736779
	.long	736796
	.long	737227
	.long	737244
	.long	737675
	.long	737692
	.long	738123
	.long	738140
	.long	738571
	.long	738588
	.long	739019
	.long	739036
	.long	739467
	.long	739484
	.long	739915
	.long	739932
	.long	740363
	.long	740380
	.long	740811
	.long	740828
	.long	741259
	.long	741276
	.long	741707
	.long	741724
	.long	742155
	.long	742172
	.long	742603
	.long	742620
	.long	743051
	.long	743068
	.long	743499
	.long	743516
	.long	743947
	.long	743964
	.long	744395
	.long	744412
	.long	744843
	.long	744860
	.long	745291
	.long	745308
	.long	745739
	.long	745756
	.long	746187
	.long	746204
	.long	746635
	.long	746652
	.long	747083
	.long	747100
	.long	747531
	.long	747548
	.long	747979
	.long	747996
	.long	748427
	.long	748444
	.long	748875
	.long	748892
	.long	749323
	.long	749340
	.long	749771
	.long	749788
	.long	750219
	.long	750236
	.long	750667
	.long	750684
	.long	751115
	.long	751132
	.long	751563
	.long	751580
	.long	752011
	.long	752028
	.long	752459
	.long	752476
	.long	752907
	.long	752924
	.long	753355
	.long	753372
	.long	753803
	.long	753820
	.long	754251
	.long	754268
	.long	754699
	.long	754716
	.long	755147
	.long	755164
	.long	755595
	.long	755612
	.long	756043
	.long	756060
	.long	756491
	.long	756508
	.long	756939
	.long	756956
	.long	757387
	.long	757404
	.long	757835
	.long	757852
	.long	758283
	.long	758300
	.long	758731
	.long	758748
	.long	759179
	.long	759196
	.long	759627
	.long	759644
	.long	760075
	.long	760092
	.long	760523
	.long	760540
	.long	760971
	.long	760988
	.long	761419
	.long	761436
	.long	761867
	.long	761884
	.long	762315
	.long	762332
	.long	762763
	.long	762780
	.long	763211
	.long	763228
	.long	763659
	.long	763676
	.long	764107
	.long	764124
	.long	764555
	.long	764572
	.long	765003
	.long	765020
	.long	765451
	.long	765468
	.long	765899
	.long	765916
	.long	766347
	.long	766364
	.long	766795
	.long	766812
	.long	767243
	.long	767260
	.long	767691
	.long	767708
	.long	768139
	.long	768156
	.long	768587
	.long	768604
	.long	769035
	.long	769052
	.long	769483
	.long	769500
	.long	769931
	.long	769948
	.long	770379
	.long	770396
	.long	770827
	.long	770844
	.long	771275
	.long	771292
	.long	771723
	.long	771740
	.long	772171
	.long	772188
	.long	772619
	.long	772636
	.long	773067
	.long	773084
	.long	773515
	.long	773532
	.long	773963
	.long	773980
	.long	774411
	.long	774428
	.long	774859
	.long	774876
	.long	775307
	.long	775324
	.long	775755
	.long	775772
	.long	776203
	.long	776220
	.long	776651
	.long	776668
	.long	777099
	.long	777116
	.long	777547
	.long	777564
	.long	777995
	.long	778012
	.long	778443
	.long	778460
	.long	778891
	.long	778908
	.long	779339
	.long	779356
	.long	779787
	.long	779804
	.long	780235
	.long	780252
	.long	780683
	.long	780700
	.long	781131
	.long	781148
	.long	781579
	.long	781596
	.long	782027
	.long	782044
	.long	782475
	.long	782492
	.long	782923
	.long	782940
	.long	783371
	.long	783388
	.long	783819
	.long	783836
	.long	784267
	.long	784284
	.long	784715
	.long	784732
	.long	785163
	.long	785180
	.long	785611
	.long	785628
	.long	786059
	.long	786076
	.long	786507
	.long	786524
	.long	786955
	.long	786972
	.long	787403
	.long	787420
	.long	787851
	.long	787868
	.long	788299
	.long	788316
	.long	788747
	.long	788764
	.long	789195
	.long	789212
	.long	789643
	.long	789660
	.long	790091
	.long	790108
	.long	790539
	.long	790556
	.long	790987
	.long	791004
	.long	791435
	.long	791452
	.long	791883
	.long	791900
	.long	792331
	.long	792348
	.long	792779
	.long	792796
	.long	793227
	.long	793244
	.long	793675
	.long	793692
	.long	794123
	.long	794140
	.long	794571
	.long	794588
	.long	795019
	.long	795036
	.long	795467
	.long	795484
	.long	795915
	.long	795932
	.long	796363
	.long	796380
	.long	796811
	.long	796828
	.long	797259
	.long	797276
	.long	797707
	.long	797724
	.long	798155
	.long	798172
	.long	798603
	.long	798620
	.long	799051
	.long	799068
	.long	799499
	.long	799516
	.long	799947
	.long	799964
	.long	800395
	.long	800412
	.long	800843
	.long	800860
	.long	801291
	.long	801308
	.long	801739
	.long	801756
	.long	802187
	.long	802204
	.long	802635
	.long	802652
	.long	803083
	.long	803100
	.long	803531
	.long	803548
	.long	803979
	.long	803996
	.long	804427
	.long	804444
	.long	804875
	.long	804892
	.long	805323
	.long	805340
	.long	805771
	.long	805788
	.long	806219
	.long	806236
	.long	806667
	.long	806684
	.long	807115
	.long	807132
	.long	807563
	.long	807580
	.long	808011
	.long	808028
	.long	808459
	.long	808476
	.long	808907
	.long	808924
	.long	809355
	.long	809372
	.long	809803
	.long	809820
	.long	810251
	.long	810268
	.long	810699
	.long	810716
	.long	811147
	.long	811164
	.long	811595
	.long	811612
	.long	812043
	.long	812060
	.long	812491
	.long	812508
	.long	812939
	.long	812956
	.long	813387
	.long	813404
	.long	813835
	.long	813852
	.long	814283
	.long	814300
	.long	814731
	.long	814748
	.long	815179
	.long	815196
	.long	815627
	.long	815644
	.long	816075
	.long	816092
	.long	816523
	.long	816540
	.long	816971
	.long	816988
	.long	817419
	.long	817436
	.long	817867
	.long	817884
	.long	818315
	.long	818332
	.long	818763
	.long	818780
	.long	819211
	.long	819228
	.long	819659
	.long	819676
	.long	820107
	.long	820124
	.long	820555
	.long	820572
	.long	821003
	.long	821020
	.long	821451
	.long	821468
	.long	821899
	.long	821916
	.long	822347
	.long	822364
	.long	822795
	.long	822812
	.long	823243
	.long	823260
	.long	823691
	.long	823708
	.long	824139
	.long	824156
	.long	824587
	.long	824604
	.long	825035
	.long	825052
	.long	825483
	.long	825500
	.long	825931
	.long	825948
	.long	826379
	.long	826396
	.long	826827
	.long	826844
	.long	827275
	.long	827292
	.long	827723
	.long	827740
	.long	828171
	.long	828188
	.long	828619
	.long	828636
	.long	829067
	.long	829084
	.long	829515
	.long	829532
	.long	829963
	.long	829980
	.long	830411
	.long	830428
	.long	830859
	.long	830876
	.long	831307
	.long	831324
	.long	831755
	.long	831772
	.long	832203
	.long	832220
	.long	832651
	.long	832668
	.long	833099
	.long	833116
	.long	833547
	.long	833564
	.long	833995
	.long	834012
	.long	834443
	.long	834460
	.long	834891
	.long	834908
	.long	835339
	.long	835356
	.long	835787
	.long	835804
	.long	836235
	.long	836252
	.long	836683
	.long	836700
	.long	837131
	.long	837148
	.long	837579
	.long	837596
	.long	838027
	.long	838044
	.long	838475
	.long	838492
	.long	838923
	.long	838940
	.long	839371
	.long	839388
	.long	839819
	.long	839836
	.long	840267
	.long	840284
	.long	840715
	.long	840732
	.long	841163
	.long	841180
	.long	841611
	.long	841628
	.long	842059
	.long	842076
	.long	842507
	.long	842524
	.long	842955
	.long	842972
	.long	843403
	.long	843420
	.long	843851
	.long	843868
	.long	844299
	.long	844316
	.long	844747
	.long	844764
	.long	845195
	.long	845212
	.long	845643
	.long	845660
	.long	846091
	.long	846108
	.long	846539
	.long	846556
	.long	846987
	.long	847004
	.long	847435
	.long	847452
	.long	847883
	.long	847900
	.long	848331
	.long	848348
	.long	848779
	.long	848796
	.long	849227
	.long	849244
	.long	849675
	.long	849692
	.long	850123
	.long	850140
	.long	850571
	.long	850588
	.long	851019
	.long	851036
	.long	851467
	.long	851484
	.long	851915
	.long	851932
	.long	852363
	.long	852380
	.long	852811
	.long	852828
	.long	853259
	.long	853276
	.long	853707
	.long	853724
	.long	854155
	.long	854172
	.long	854603
	.long	854620
	.long	855051
	.long	855068
	.long	855499
	.long	855516
	.long	855947
	.long	855964
	.long	856395
	.long	856412
	.long	856843
	.long	856860
	.long	857291
	.long	857308
	.long	857739
	.long	857756
	.long	858187
	.long	858204
	.long	858635
	.long	858652
	.long	859083
	.long	859100
	.long	859531
	.long	859548
	.long	859979
	.long	859996
	.long	860427
	.long	860444
	.long	860875
	.long	860892
	.long	861323
	.long	861340
	.long	861771
	.long	861788
	.long	862219
	.long	862236
	.long	862667
	.long	862684
	.long	863115
	.long	863132
	.long	863563
	.long	863580
	.long	864011
	.long	864028
	.long	864459
	.long	864476
	.long	864907
	.long	864924
	.long	865355
	.long	865372
	.long	865803
	.long	865820
	.long	866251
	.long	866268
	.long	866699
	.long	866716
	.long	867147
	.long	867164
	.long	867595
	.long	867612
	.long	868043
	.long	868060
	.long	868491
	.long	868508
	.long	868939
	.long	868956
	.long	869387
	.long	869404
	.long	869835
	.long	869852
	.long	870283
	.long	870300
	.long	870731
	.long	870748
	.long	871179
	.long	871196
	.long	871627
	.long	871644
	.long	872075
	.long	872092
	.long	872523
	.long	872540
	.long	872971
	.long	872988
	.long	873419
	.long	873436
	.long	873867
	.long	873884
	.long	874315
	.long	874332
	.long	874763
	.long	874780
	.long	875211
	.long	875228
	.long	875659
	.long	875676
	.long	876107
	.long	876124
	.long	876555
	.long	876572
	.long	877003
	.long	877020
	.long	877451
	.long	877468
	.long	877899
	.long	877916
	.long	878347
	.long	878364
	.long	878795
	.long	878812
	.long	879243
	.long	879260
	.long	879691
	.long	879708
	.long	880139
	.long	880156
	.long	880587
	.long	880604
	.long	881035
	.long	881052
	.long	881483
	.long	881500
	.long	881931
	.long	881948
	.long	882379
	.long	882396
	.long	882827
	.long	882844
	.long	883264
	.long	883464
	.long	883824
	.long	883897
	.long	884672
	.long	1028580
	.long	1028592
	.long	1040388
	.long	1040640
	.long	1040900
	.long	1041152
	.long	1044465
	.long	1044480
	.long	1047012
	.long	1047040
	.long	1048321
	.long	1048512
	.long	1056724
	.long	1056736
	.long	1060356
	.long	1060368
	.long	1062756
	.long	1062832
	.long	1089556
	.long	1089600
	.long	1089620
	.long	1089648
	.long	1089732
	.long	1089792
	.long	1090436
	.long	1090480
	.long	1090548
	.long	1090560
	.long	1093204
	.long	1093232
	.long	1102404
	.long	1102464
	.long	1103508
	.long	1103584
	.long	1108660
	.long	1108688
	.long	1109956
	.long	1110016
	.long	1111140
	.long	1111312
	.long	1112100
	.long	1112160
	.long	1114118
	.long	1114132
	.long	1114150
	.long	1114160
	.long	1115012
	.long	1115248
	.long	1115908
	.long	1115920
	.long	1115956
	.long	1115984
	.long	1116148
	.long	1116198
	.long	1116208
	.long	1116934
	.long	1116980
	.long	1117046
	.long	1117076
	.long	1117104
	.long	1117141
	.long	1117152
	.long	1117220
	.long	1117232
	.long	1117397
	.long	1117408
	.long	1118212
	.long	1118256
	.long	1118836
	.long	1118918
	.long	1118932
	.long	1119056
	.long	1119318
	.long	1119344
	.long	1120052
	.long	1120064
	.long	1120260
	.long	1120294
	.long	1120304
	.long	1121078
	.long	1121124
	.long	1121270
	.long	1121284
	.long	1121296
	.long	1121317
	.long	1121344
	.long	1121428
	.long	1121488
	.long	1121510
	.long	1121524
	.long	1121536
	.long	1123014
	.long	1123060
	.long	1123110
	.long	1123140
	.long	1123200
	.long	1123300
	.long	1123312
	.long	1123348
	.long	1123360
	.long	1125876
	.long	1125894
	.long	1125940
	.long	1126064
	.long	1126404
	.long	1126438
	.long	1126464
	.long	1127348
	.long	1127376
	.long	1127396
	.long	1127414
	.long	1127428
	.long	1127446
	.long	1127504
	.long	1127542
	.long	1127568
	.long	1127606
	.long	1127636
	.long	1127648
	.long	1127796
	.long	1127808
	.long	1127974
	.long	1128000
	.long	1128036
	.long	1128144
	.long	1128196
	.long	1128272
	.long	1129348
	.long	1129366
	.long	1129396
	.long	1129488
	.long	1129508
	.long	1129520
	.long	1129556
	.long	1129568
	.long	1129588
	.long	1129638
	.long	1129648
	.long	1129670
	.long	1129700
	.long	1129749
	.long	1129764
	.long	1129776
	.long	1130004
	.long	1130032
	.long	1131350
	.long	1131396
	.long	1131526
	.long	1131556
	.long	1131606
	.long	1131620
	.long	1131632
	.long	1132004
	.long	1132016
	.long	1133316
	.long	1133334
	.long	1133364
	.long	1133462
	.long	1133476
	.long	1133494
	.long	1133524
	.long	1133542
	.long	1133556
	.long	1133590
	.long	1133604
	.long	1133632
	.long	1137396
	.long	1137414
	.long	1137444
	.long	1137504
	.long	1137542
	.long	1137604
	.long	1137638
	.long	1137652
	.long	1137680
	.long	1138116
	.long	1138144
	.long	1139462
	.long	1139508
	.long	1139638
	.long	1139668
	.long	1139686
	.long	1139700
	.long	1139728
	.long	1141428
	.long	1141446
	.long	1141460
	.long	1141478
	.long	1141508
	.long	1141632
	.long	1143252
	.long	1143270
	.long	1143284
	.long	1143296
	.long	1143332
	.long	1143398
	.long	1143412
	.long	1143488
	.long	1147590
	.long	1147636
	.long	1147782
	.long	1147796
	.long	1147824
	.long	1151748
	.long	1151766
	.long	1151840
	.long	1151862
	.long	1151888
	.long	1151924
	.long	1151989
	.long	1152006
	.long	1152021
	.long	1152038
	.long	1152052
	.long	1152064
	.long	1154326
	.long	1154372
	.long	1154432
	.long	1154468
	.long	1154502
	.long	1154564
	.long	1154576
	.long	1154630
	.long	1154640
	.long	1155092
	.long	1155248
	.long	1155892
	.long	1155990
	.long	1156005
	.long	1156020
	.long	1156080
	.long	1156212
	.long	1156224
	.long	1156372
	.long	1156470
	.long	1156500
	.long	1156544
	.long	1157189
	.long	1157284
	.long	1157494
	.long	1157508
	.long	1157536
	.long	1164022
	.long	1164036
	.long	1164144
	.long	1164164
	.long	1164262
	.long	1164276
	.long	1164288
	.long	1165604
	.long	1165952
	.long	1165974
	.long	1165988
	.long	1166102
	.long	1166116
	.long	1166150
	.long	1166164
	.long	1166192
	.long	1168148
	.long	1168240
	.long	1168292
	.long	1168304
	.long	1168324
	.long	1168352
	.long	1168372
	.long	1168485
	.long	1168500
	.long	1168512
	.long	1169574
	.long	1169648
	.long	1169668
	.long	1169696
	.long	1169718
	.long	1169748
	.long	1169766
	.long	1169780
	.long	1169792
	.long	1175348
	.long	1175382
	.long	1175408
	.long	1175556
	.long	1175589
	.long	1175606
	.long	1175616
	.long	1176390
	.long	1176420
	.long	1176496
	.long	1176550
	.long	1176580
	.long	1176624
	.long	1176996
	.long	1177008
	.long	1262337
	.long	1262596
	.long	1262608
	.long	1262708
	.long	1262944
	.long	1446372
	.long	1446566
	.long	1446612
	.long	1446656
	.long	1486596
	.long	1486672
	.long	1487620
	.long	1487728
	.long	1496632
	.long	1496640
	.long	1496696
	.long	1496752
	.long	1504500
	.long	1504512
	.long	1504534
	.long	1505408
	.long	1505524
	.long	1505584
	.long	1506884
	.long	1506896
	.long	1507076
	.long	1507104
	.long	1821140
	.long	1821168
	.long	1821185
	.long	1821248
	.long	1896452
	.long	1897184
	.long	1897220
	.long	1897584
	.long	1906260
	.long	1906336
	.long	1906388
	.long	1906481
	.long	1906612
	.long	1906736
	.long	1906772
	.long	1906880
	.long	1907364
	.long	1907424
	.long	1909796
	.long	1909840
	.long	1941508
	.long	1942384
	.long	1942452
	.long	1943248
	.long	1943380
	.long	1943392
	.long	1943620
	.long	1943632
	.long	1943988
	.long	1944064
	.long	1944084
	.long	1944320
	.long	1966084
	.long	1966192
	.long	1966212
	.long	1966480
	.long	1966516
	.long	1966624
	.long	1966644
	.long	1966672
	.long	1966692
	.long	1966768
	.long	1968372
	.long	1968384
	.long	1970948
	.long	1971056
	.long	1977060
	.long	1977072
	.long	1978052
	.long	1978112
	.long	1986244
	.long	1986304
	.long	1990372
	.long	1990400
	.long	2002180
	.long	2002288
	.long	2004036
	.long	2004144
	.long	2039405
	.long	2039808
	.long	2047924
	.long	2048000
	.long	14680065
	.long	14680580
	.long	14682113
	.long	14684164
	.long	14688001
	.long	14745600
	.globl	_ZNSt9__unicode9__v16_0_014__escape_edgesE
	.section	.rdata$_ZNSt9__unicode9__v16_0_014__escape_edgesE,"dr"
	.linkonce same_size
	.align 32
_ZNSt9__unicode9__v16_0_014__escape_edgesE:
	.long	1
	.long	66
	.long	255
	.long	322
	.long	347
	.long	348
	.long	1777
	.long	1780
	.long	1793
	.long	1800
	.long	1815
	.long	1816
	.long	1819
	.long	1820
	.long	1861
	.long	1862
	.long	2657
	.long	2658
	.long	2735
	.long	2738
	.long	2839
	.long	2842
	.long	2849
	.long	2850
	.long	2961
	.long	2976
	.long	3031
	.long	3038
	.long	3051
	.long	3084
	.long	3129
	.long	3130
	.long	3515
	.long	3516
	.long	3613
	.long	3616
	.long	3735
	.long	3738
	.long	3941
	.long	3968
	.long	4087
	.long	4090
	.long	4189
	.long	4192
	.long	4223
	.long	4224
	.long	4281
	.long	4284
	.long	4287
	.long	4288
	.long	4311
	.long	4320
	.long	4383
	.long	4398
	.long	4549
	.long	4550
	.long	4873
	.long	4874
	.long	4891
	.long	4894
	.long	4899
	.long	4902
	.long	4947
	.long	4948
	.long	4963
	.long	4964
	.long	4967
	.long	4972
	.long	4981
	.long	4984
	.long	5003
	.long	5006
	.long	5011
	.long	5014
	.long	5023
	.long	5038
	.long	5041
	.long	5048
	.long	5053
	.long	5054
	.long	5065
	.long	5068
	.long	5119
	.long	5122
	.long	5129
	.long	5130
	.long	5143
	.long	5150
	.long	5155
	.long	5158
	.long	5203
	.long	5204
	.long	5219
	.long	5220
	.long	5225
	.long	5226
	.long	5231
	.long	5232
	.long	5237
	.long	5240
	.long	5243
	.long	5244
	.long	5255
	.long	5262
	.long	5267
	.long	5270
	.long	5277
	.long	5282
	.long	5285
	.long	5298
	.long	5307
	.long	5308
	.long	5311
	.long	5324
	.long	5359
	.long	5378
	.long	5385
	.long	5386
	.long	5405
	.long	5406
	.long	5413
	.long	5414
	.long	5459
	.long	5460
	.long	5475
	.long	5476
	.long	5481
	.long	5482
	.long	5493
	.long	5496
	.long	5517
	.long	5518
	.long	5525
	.long	5526
	.long	5533
	.long	5536
	.long	5539
	.long	5568
	.long	5577
	.long	5580
	.long	5605
	.long	5618
	.long	5633
	.long	5634
	.long	5641
	.long	5642
	.long	5659
	.long	5662
	.long	5667
	.long	5670
	.long	5715
	.long	5716
	.long	5731
	.long	5732
	.long	5737
	.long	5738
	.long	5749
	.long	5752
	.long	5771
	.long	5774
	.long	5779
	.long	5782
	.long	5789
	.long	5802
	.long	5809
	.long	5816
	.long	5821
	.long	5822
	.long	5833
	.long	5836
	.long	5873
	.long	5892
	.long	5897
	.long	5898
	.long	5911
	.long	5916
	.long	5923
	.long	5924
	.long	5933
	.long	5938
	.long	5943
	.long	5944
	.long	5947
	.long	5948
	.long	5953
	.long	5958
	.long	5963
	.long	5968
	.long	5975
	.long	5980
	.long	6005
	.long	6012
	.long	6023
	.long	6028
	.long	6035
	.long	6036
	.long	6045
	.long	6048
	.long	6051
	.long	6062
	.long	6065
	.long	6092
	.long	6135
	.long	6144
	.long	6171
	.long	6172
	.long	6179
	.long	6180
	.long	6227
	.long	6228
	.long	6261
	.long	6264
	.long	6283
	.long	6284
	.long	6291
	.long	6292
	.long	6301
	.long	6314
	.long	6319
	.long	6320
	.long	6327
	.long	6330
	.long	6333
	.long	6336
	.long	6345
	.long	6348
	.long	6369
	.long	6382
	.long	6427
	.long	6428
	.long	6435
	.long	6436
	.long	6483
	.long	6484
	.long	6505
	.long	6506
	.long	6517
	.long	6520
	.long	6539
	.long	6540
	.long	6547
	.long	6548
	.long	6557
	.long	6570
	.long	6575
	.long	6586
	.long	6591
	.long	6592
	.long	6601
	.long	6604
	.long	6625
	.long	6626
	.long	6633
	.long	6656
	.long	6683
	.long	6684
	.long	6691
	.long	6692
	.long	6795
	.long	6796
	.long	6803
	.long	6804
	.long	6817
	.long	6824
	.long	6857
	.long	6860
	.long	6913
	.long	6914
	.long	6921
	.long	6922
	.long	6959
	.long	6964
	.long	7013
	.long	7014
	.long	7033
	.long	7034
	.long	7037
	.long	7040
	.long	7055
	.long	7060
	.long	7063
	.long	7070
	.long	7083
	.long	7084
	.long	7087
	.long	7088
	.long	7105
	.long	7116
	.long	7137
	.long	7140
	.long	7147
	.long	7170
	.long	7287
	.long	7294
	.long	7353
	.long	7426
	.long	7431
	.long	7432
	.long	7435
	.long	7436
	.long	7447
	.long	7448
	.long	7497
	.long	7498
	.long	7501
	.long	7502
	.long	7549
	.long	7552
	.long	7563
	.long	7564
	.long	7567
	.long	7568
	.long	7583
	.long	7584
	.long	7605
	.long	7608
	.long	7617
	.long	7680
	.long	7825
	.long	7826
	.long	7899
	.long	7906
	.long	7985
	.long	7986
	.long	8059
	.long	8060
	.long	8091
	.long	8092
	.long	8119
	.long	8192
	.long	8589
	.long	8590
	.long	8593
	.long	8602
	.long	8605
	.long	8608
	.long	9363
	.long	9364
	.long	9373
	.long	9376
	.long	9391
	.long	9392
	.long	9395
	.long	9396
	.long	9405
	.long	9408
	.long	9491
	.long	9492
	.long	9501
	.long	9504
	.long	9571
	.long	9572
	.long	9581
	.long	9584
	.long	9599
	.long	9600
	.long	9603
	.long	9604
	.long	9613
	.long	9616
	.long	9647
	.long	9648
	.long	9763
	.long	9764
	.long	9773
	.long	9776
	.long	9911
	.long	9914
	.long	9979
	.long	9984
	.long	10037
	.long	10048
	.long	10221
	.long	10224
	.long	10237
	.long	10240
	.long	11521
	.long	11522
	.long	11579
	.long	11584
	.long	11763
	.long	11776
	.long	11821
	.long	11838
	.long	11887
	.long	11904
	.long	11945
	.long	11968
	.long	11995
	.long	11996
	.long	12003
	.long	12004
	.long	12009
	.long	12032
	.long	12221
	.long	12224
	.long	12245
	.long	12256
	.long	12277
	.long	12288
	.long	12317
	.long	12318
	.long	12341
	.long	12352
	.long	12531
	.long	12544
	.long	12631
	.long	12640
	.long	12781
	.long	12800
	.long	12863
	.long	12864
	.long	12889
	.long	12896
	.long	12921
	.long	12928
	.long	12931
	.long	12936
	.long	13021
	.long	13024
	.long	13035
	.long	13056
	.long	13145
	.long	13152
	.long	13205
	.long	13216
	.long	13239
	.long	13244
	.long	13369
	.long	13372
	.long	13503
	.long	13504
	.long	13563
	.long	13566
	.long	13589
	.long	13600
	.long	13621
	.long	13632
	.long	13661
	.long	13664
	.long	13727
	.long	13824
	.long	13979
	.long	13980
	.long	14313
	.long	14328
	.long	14449
	.long	14454
	.long	14485
	.long	14490
	.long	14615
	.long	14624
	.long	14711
	.long	14714
	.long	14737
	.long	14752
	.long	14839
	.long	14848
	.long	15917
	.long	15920
	.long	15933
	.long	15936
	.long	16013
	.long	16016
	.long	16029
	.long	16032
	.long	16049
	.long	16050
	.long	16053
	.long	16054
	.long	16057
	.long	16058
	.long	16061
	.long	16062
	.long	16125
	.long	16128
	.long	16235
	.long	16236
	.long	16267
	.long	16268
	.long	16297
	.long	16300
	.long	16313
	.long	16314
	.long	16353
	.long	16356
	.long	16363
	.long	16364
	.long	16383
	.long	16416
	.long	16465
	.long	16480
	.long	16575
	.long	16608
	.long	16613
	.long	16616
	.long	16671
	.long	16672
	.long	16699
	.long	16704
	.long	16771
	.long	16800
	.long	16867
	.long	16896
	.long	17177
	.long	17184
	.long	18517
	.long	18560
	.long	18583
	.long	18624
	.long	22249
	.long	22252
	.long	22317
	.long	22318
	.long	23017
	.long	23026
	.long	23117
	.long	23118
	.long	23121
	.long	23130
	.long	23133
	.long	23136
	.long	23249
	.long	23262
	.long	23267
	.long	23294
	.long	23343
	.long	23360
	.long	23375
	.long	23376
	.long	23391
	.long	23392
	.long	23407
	.long	23408
	.long	23423
	.long	23424
	.long	23439
	.long	23440
	.long	23455
	.long	23456
	.long	23471
	.long	23472
	.long	23487
	.long	23488
	.long	23741
	.long	23808
	.long	23861
	.long	23862
	.long	24041
	.long	24064
	.long	24493
	.long	24544
	.long	24577
	.long	24578
	.long	24705
	.long	24706
	.long	24879
	.long	24882
	.long	25089
	.long	25098
	.long	25185
	.long	25186
	.long	25375
	.long	25376
	.long	25549
	.long	25566
	.long	25663
	.long	25664
	.long	84251
	.long	84256
	.long	84367
	.long	84384
	.long	85081
	.long	85120
	.long	85489
	.long	85504
	.long	85917
	.long	85920
	.long	85925
	.long	85926
	.long	85929
	.long	85930
	.long	85947
	.long	85988
	.long	86107
	.long	86112
	.long	86133
	.long	86144
	.long	86257
	.long	86272
	.long	86413
	.long	86428
	.long	86453
	.long	86464
	.long	86697
	.long	86718
	.long	86779
	.long	86784
	.long	86941
	.long	86942
	.long	86965
	.long	86972
	.long	87039
	.long	87040
	.long	87151
	.long	87168
	.long	87197
	.long	87200
	.long	87221
	.long	87224
	.long	87431
	.long	87478
	.long	87535
	.long	87554
	.long	87567
	.long	87570
	.long	87583
	.long	87586
	.long	87599
	.long	87616
	.long	87631
	.long	87632
	.long	87647
	.long	87648
	.long	87769
	.long	87776
	.long	88029
	.long	88032
	.long	88053
	.long	88064
	.long	110409
	.long	110432
	.long	110479
	.long	110486
	.long	110585
	.long	127488
	.long	128221
	.long	128224
	.long	128437
	.long	128512
	.long	128527
	.long	128550
	.long	128561
	.long	128570
	.long	128623
	.long	128624
	.long	128635
	.long	128636
	.long	128639
	.long	128640
	.long	128645
	.long	128646
	.long	128651
	.long	128652
	.long	128903
	.long	128934
	.long	129825
	.long	129828
	.long	129937
	.long	129950
	.long	129953
	.long	130016
	.long	130101
	.long	130112
	.long	130215
	.long	130216
	.long	130255
	.long	130256
	.long	130265
	.long	130272
	.long	130283
	.long	130284
	.long	130555
	.long	130562
	.long	130943
	.long	130948
	.long	130961
	.long	130964
	.long	130977
	.long	130980
	.long	130993
	.long	130996
	.long	131003
	.long	131008
	.long	131023
	.long	131024
	.long	131039
	.long	131064
	.long	131069
	.long	131072
	.long	131097
	.long	131098
	.long	131151
	.long	131152
	.long	131191
	.long	131192
	.long	131197
	.long	131198
	.long	131229
	.long	131232
	.long	131261
	.long	131328
	.long	131575
	.long	131584
	.long	131591
	.long	131598
	.long	131689
	.long	131694
	.long	131871
	.long	131872
	.long	131899
	.long	131904
	.long	131907
	.long	132000
	.long	132093
	.long	132352
	.long	132411
	.long	132416
	.long	132515
	.long	132544
	.long	132601
	.long	132608
	.long	132681
	.long	132698
	.long	132759
	.long	132768
	.long	132855
	.long	132864
	.long	132925
	.long	132926
	.long	133001
	.long	133008
	.long	133037
	.long	133120
	.long	133437
	.long	133440
	.long	133461
	.long	133472
	.long	133545
	.long	133552
	.long	133625
	.long	133632
	.long	133713
	.long	133728
	.long	133833
	.long	133854
	.long	133879
	.long	133880
	.long	133911
	.long	133912
	.long	133927
	.long	133928
	.long	133933
	.long	133934
	.long	133957
	.long	133958
	.long	133989
	.long	133990
	.long	134005
	.long	134006
	.long	134011
	.long	134016
	.long	134121
	.long	134144
	.long	134767
	.long	134784
	.long	134829
	.long	134848
	.long	134865
	.long	134912
	.long	134925
	.long	134926
	.long	135011
	.long	135012
	.long	135031
	.long	135168
	.long	135181
	.long	135184
	.long	135187
	.long	135188
	.long	135277
	.long	135278
	.long	135283
	.long	135288
	.long	135291
	.long	135294
	.long	135341
	.long	135342
	.long	135487
	.long	135502
	.long	135521
	.long	135616
	.long	135655
	.long	135656
	.long	135661
	.long	135670
	.long	135737
	.long	135742
	.long	135797
	.long	135806
	.long	135809
	.long	135936
	.long	136049
	.long	136056
	.long	136097
	.long	136100
	.long	136201
	.long	136202
	.long	136207
	.long	136216
	.long	136233
	.long	136234
	.long	136241
	.long	136242
	.long	136301
	.long	136304
	.long	136311
	.long	136318
	.long	136339
	.long	136352
	.long	136371
	.long	136384
	.long	136513
	.long	136576
	.long	136655
	.long	136662
	.long	136687
	.long	136704
	.long	136813
	.long	136818
	.long	136877
	.long	136880
	.long	136935
	.long	136944
	.long	136997
	.long	137010
	.long	137019
	.long	137042
	.long	137057
	.long	137216
	.long	137363
	.long	137472
	.long	137575
	.long	137600
	.long	137703
	.long	137716
	.long	137809
	.long	137824
	.long	137845
	.long	137856
	.long	137933
	.long	137938
	.long	137997
	.long	138012
	.long	138017
	.long	138432
	.long	138495
	.long	138496
	.long	138581
	.long	138582
	.long	138589
	.long	138592
	.long	138597
	.long	138628
	.long	138635
	.long	138744
	.long	138833
	.long	138848
	.long	138933
	.long	138976
	.long	139029
	.long	139104
	.long	139161
	.long	139200
	.long	139247
	.long	139264
	.long	139421
	.long	139428
	.long	139501
	.long	139518
	.long	139643
	.long	139644
	.long	139655
	.long	139680
	.long	139731
	.long	139744
	.long	139765
	.long	139776
	.long	139883
	.long	139884
	.long	139921
	.long	139936
	.long	140015
	.long	140032
	.long	140225
	.long	140226
	.long	140267
	.long	140288
	.long	140325
	.long	140326
	.long	140421
	.long	140544
	.long	140559
	.long	140560
	.long	140563
	.long	140564
	.long	140573
	.long	140574
	.long	140605
	.long	140606
	.long	140629
	.long	140640
	.long	140759
	.long	140768
	.long	140789
	.long	140800
	.long	140809
	.long	140810
	.long	140827
	.long	140830
	.long	140835
	.long	140838
	.long	140883
	.long	140884
	.long	140899
	.long	140900
	.long	140905
	.long	140906
	.long	140917
	.long	140918
	.long	140939
	.long	140942
	.long	140947
	.long	140950
	.long	140957
	.long	140960
	.long	140963
	.long	140974
	.long	140977
	.long	140986
	.long	141001
	.long	141004
	.long	141019
	.long	141024
	.long	141035
	.long	141056
	.long	141077
	.long	141078
	.long	141081
	.long	141084
	.long	141087
	.long	141088
	.long	141165
	.long	141166
	.long	141187
	.long	141188
	.long	141191
	.long	141194
	.long	141197
	.long	141198
	.long	141207
	.long	141208
	.long	141229
	.long	141230
	.long	141235
	.long	141250
	.long	141255
	.long	141312
	.long	141497
	.long	141498
	.long	141509
	.long	141568
	.long	141713
	.long	141728
	.long	141749
	.long	142080
	.long	142189
	.long	142192
	.long	142269
	.long	142336
	.long	142475
	.long	142496
	.long	142517
	.long	142528
	.long	142555
	.long	142592
	.long	142709
	.long	142720
	.long	142741
	.long	142752
	.long	142793
	.long	142848
	.long	142903
	.long	142906
	.long	142937
	.long	142944
	.long	142991
	.long	143360
	.long	143481
	.long	143680
	.long	143847
	.long	143870
	.long	143887
	.long	143890
	.long	143893
	.long	143896
	.long	143913
	.long	143914
	.long	143919
	.long	143920
	.long	143981
	.long	143982
	.long	143987
	.long	143990
	.long	144015
	.long	144032
	.long	144053
	.long	144192
	.long	144209
	.long	144212
	.long	144305
	.long	144308
	.long	144331
	.long	144384
	.long	144529
	.long	144544
	.long	144711
	.long	144736
	.long	144883
	.long	144896
	.long	144917
	.long	145280
	.long	145349
	.long	145376
	.long	145397
	.long	145408
	.long	145427
	.long	145428
	.long	145519
	.long	145520
	.long	145549
	.long	145568
	.long	145627
	.long	145632
	.long	145697
	.long	145700
	.long	145745
	.long	145746
	.long	145775
	.long	145920
	.long	145935
	.long	145936
	.long	145941
	.long	145942
	.long	146031
	.long	146036
	.long	146039
	.long	146040
	.long	146045
	.long	146046
	.long	146065
	.long	146080
	.long	146101
	.long	146112
	.long	146125
	.long	146126
	.long	146131
	.long	146132
	.long	146207
	.long	146208
	.long	146213
	.long	146214
	.long	146227
	.long	146240
	.long	146261
	.long	146880
	.long	146931
	.long	146944
	.long	146979
	.long	146980
	.long	147063
	.long	147068
	.long	147127
	.long	147296
	.long	147299
	.long	147328
	.long	147429
	.long	147454
	.long	149301
	.long	149504
	.long	149727
	.long	149728
	.long	149739
	.long	149760
	.long	150153
	.long	155424
	.long	155623
	.long	155648
	.long	157793
	.long	157824
	.long	157869
	.long	157888
	.long	165879
	.long	165888
	.long	167055
	.long	180736
	.long	180853
	.long	184320
	.long	185459
	.long	185472
	.long	185535
	.long	185536
	.long	185557
	.long	185564
	.long	185727
	.long	185728
	.long	185749
	.long	185760
	.long	185821
	.long	185824
	.long	185837
	.long	185856
	.long	185997
	.long	186016
	.long	186037
	.long	186038
	.long	186053
	.long	186054
	.long	186097
	.long	186106
	.long	186145
	.long	187008
	.long	187125
	.long	187520
	.long	187703
	.long	187904
	.long	188055
	.long	188062
	.long	188177
	.long	188190
	.long	188225
	.long	188352
	.long	188363
	.long	188384
	.long	188389
	.long	188416
	.long	200689
	.long	200704
	.long	203181
	.long	203262
	.long	203283
	.long	221152
	.long	221161
	.long	221162
	.long	221177
	.long	221178
	.long	221183
	.long	221184
	.long	221767
	.long	221796
	.long	221799
	.long	221856
	.long	221863
	.long	221866
	.long	221869
	.long	221896
	.long	221905
	.long	221920
	.long	222713
	.long	227328
	.long	227543
	.long	227552
	.long	227579
	.long	227584
	.long	227603
	.long	227616
	.long	227637
	.long	227640
	.long	227649
	.long	235520
	.long	236021
	.long	236032
	.long	236905
	.long	237056
	.long	237149
	.long	237152
	.long	237199
	.long	237216
	.long	237449
	.long	237568
	.long	238061
	.long	238080
	.long	238159
	.long	238162
	.long	238311
	.long	238326
	.long	238551
	.long	238592
	.long	238733
	.long	238976
	.long	239017
	.long	239040
	.long	239081
	.long	239104
	.long	239279
	.long	239296
	.long	239347
	.long	239616
	.long	239787
	.long	239788
	.long	239931
	.long	239932
	.long	239937
	.long	239940
	.long	239943
	.long	239946
	.long	239951
	.long	239954
	.long	239963
	.long	239964
	.long	239989
	.long	239990
	.long	239993
	.long	239994
	.long	240009
	.long	240010
	.long	240141
	.long	240142
	.long	240151
	.long	240154
	.long	240171
	.long	240172
	.long	240187
	.long	240188
	.long	240245
	.long	240246
	.long	240255
	.long	240256
	.long	240267
	.long	240268
	.long	240271
	.long	240276
	.long	240291
	.long	240292
	.long	240973
	.long	240976
	.long	241561
	.long	241564
	.long	242969
	.long	242998
	.long	243009
	.long	243010
	.long	243041
	.long	245248
	.long	245311
	.long	245322
	.long	245335
	.long	245760
	.long	245775
	.long	245776
	.long	245811
	.long	245814
	.long	245829
	.long	245830
	.long	245835
	.long	245836
	.long	245847
	.long	245856
	.long	245981
	.long	246046
	.long	246049
	.long	246272
	.long	246363
	.long	246368
	.long	246397
	.long	246400
	.long	246421
	.long	246428
	.long	246433
	.long	247072
	.long	247135
	.long	247168
	.long	247285
	.long	247294
	.long	247297
	.long	248224
	.long	248309
	.long	248736
	.long	248823
	.long	248830
	.long	248833
	.long	249792
	.long	249807
	.long	249808
	.long	249817
	.long	249818
	.long	249823
	.long	249824
	.long	249855
	.long	249856
	.long	250251
	.long	250254
	.long	250287
	.long	250368
	.long	250521
	.long	250528
	.long	250549
	.long	250556
	.long	250561
	.long	252130
	.long	252267
	.long	252418
	.long	252541
	.long	252928
	.long	252937
	.long	252938
	.long	252993
	.long	252994
	.long	252999
	.long	253000
	.long	253003
	.long	253006
	.long	253009
	.long	253010
	.long	253031
	.long	253032
	.long	253041
	.long	253042
	.long	253045
	.long	253046
	.long	253049
	.long	253060
	.long	253063
	.long	253070
	.long	253073
	.long	253074
	.long	253077
	.long	253078
	.long	253081
	.long	253082
	.long	253089
	.long	253090
	.long	253095
	.long	253096
	.long	253099
	.long	253102
	.long	253105
	.long	253106
	.long	253109
	.long	253110
	.long	253113
	.long	253114
	.long	253117
	.long	253118
	.long	253121
	.long	253122
	.long	253127
	.long	253128
	.long	253131
	.long	253134
	.long	253143
	.long	253144
	.long	253159
	.long	253160
	.long	253169
	.long	253170
	.long	253179
	.long	253180
	.long	253183
	.long	253184
	.long	253205
	.long	253206
	.long	253241
	.long	253250
	.long	253257
	.long	253258
	.long	253269
	.long	253270
	.long	253305
	.long	253408
	.long	253413
	.long	253952
	.long	254041
	.long	254048
	.long	254249
	.long	254272
	.long	254303
	.long	254306
	.long	254337
	.long	254338
	.long	254369
	.long	254370
	.long	254445
	.long	254464
	.long	254813
	.long	254924
	.long	254983
	.long	255008
	.long	255097
	.long	255104
	.long	255123
	.long	255136
	.long	255141
	.long	255168
	.long	255181
	.long	255488
	.long	257457
	.long	257464
	.long	257499
	.long	257504
	.long	257531
	.long	257536
	.long	257775
	.long	257782
	.long	257973
	.long	257984
	.long	258009
	.long	258016
	.long	258019
	.long	258048
	.long	258073
	.long	258080
	.long	258193
	.long	258208
	.long	258229
	.long	258240
	.long	258321
	.long	258336
	.long	258397
	.long	258400
	.long	258425
	.long	258432
	.long	258437
	.long	258560
	.long	259241
	.long	259264
	.long	259293
	.long	259296
	.long	259323
	.long	259328
	.long	259349
	.long	259358
	.long	259471
	.long	259484
	.long	259515
	.long	259518
	.long	259541
	.long	259552
	.long	259571
	.long	259584
	.long	259879
	.long	259880
	.long	260085
	.long	262144
	.long	347585
	.long	347648
	.long	355957
	.long	355968
	.long	356413
	.long	356416
	.long	367941
	.long	367968
	.long	382915
	.long	382944
	.long	384189
	.long	389120
	.long	390205
	.long	393216
	.long	403095
	.long	403104
	.long	411489
	.long	1835520
	.long	1836001
	.globl	_ZNSt9__unicode9__v16_0_013__width_edgesE
	.section	.rdata$_ZNSt9__unicode9__v16_0_013__width_edgesE,"dr"
	.linkonce same_size
	.align 32
_ZNSt9__unicode9__v16_0_013__width_edgesE:
	.long	4352
	.long	4448
	.long	8986
	.long	8988
	.long	9001
	.long	9003
	.long	9193
	.long	9197
	.long	9200
	.long	9201
	.long	9203
	.long	9204
	.long	9725
	.long	9727
	.long	9748
	.long	9750
	.long	9776
	.long	9784
	.long	9800
	.long	9812
	.long	9855
	.long	9856
	.long	9866
	.long	9872
	.long	9875
	.long	9876
	.long	9889
	.long	9890
	.long	9898
	.long	9900
	.long	9917
	.long	9919
	.long	9924
	.long	9926
	.long	9934
	.long	9935
	.long	9940
	.long	9941
	.long	9962
	.long	9963
	.long	9970
	.long	9972
	.long	9973
	.long	9974
	.long	9978
	.long	9979
	.long	9981
	.long	9982
	.long	9989
	.long	9990
	.long	9994
	.long	9996
	.long	10024
	.long	10025
	.long	10060
	.long	10061
	.long	10062
	.long	10063
	.long	10067
	.long	10070
	.long	10071
	.long	10072
	.long	10133
	.long	10136
	.long	10160
	.long	10161
	.long	10175
	.long	10176
	.long	11035
	.long	11037
	.long	11088
	.long	11089
	.long	11093
	.long	11094
	.long	11904
	.long	11930
	.long	11931
	.long	12020
	.long	12032
	.long	12246
	.long	12272
	.long	12351
	.long	12353
	.long	12439
	.long	12441
	.long	12544
	.long	12549
	.long	12592
	.long	12593
	.long	12687
	.long	12688
	.long	12774
	.long	12783
	.long	12831
	.long	12832
	.long	12872
	.long	12880
	.long	42125
	.long	42128
	.long	42183
	.long	43360
	.long	43389
	.long	44032
	.long	55204
	.long	63744
	.long	64256
	.long	65040
	.long	65050
	.long	65072
	.long	65107
	.long	65108
	.long	65127
	.long	65128
	.long	65132
	.long	65281
	.long	65377
	.long	65504
	.long	65511
	.long	94176
	.long	94181
	.long	94192
	.long	94194
	.long	94208
	.long	100344
	.long	100352
	.long	101590
	.long	101631
	.long	101641
	.long	110576
	.long	110580
	.long	110581
	.long	110588
	.long	110589
	.long	110591
	.long	110592
	.long	110883
	.long	110898
	.long	110899
	.long	110928
	.long	110931
	.long	110933
	.long	110934
	.long	110948
	.long	110952
	.long	110960
	.long	111356
	.long	119552
	.long	119639
	.long	119648
	.long	119671
	.long	126980
	.long	126981
	.long	127183
	.long	127184
	.long	127374
	.long	127375
	.long	127377
	.long	127387
	.long	127488
	.long	127491
	.long	127504
	.long	127548
	.long	127552
	.long	127561
	.long	127568
	.long	127570
	.long	127584
	.long	127590
	.long	127744
	.long	128592
	.long	128640
	.long	128710
	.long	128716
	.long	128717
	.long	128720
	.long	128723
	.long	128725
	.long	128728
	.long	128732
	.long	128736
	.long	128747
	.long	128749
	.long	128756
	.long	128765
	.long	128992
	.long	129004
	.long	129008
	.long	129009
	.long	129280
	.long	129536
	.long	129648
	.long	129661
	.long	129664
	.long	129674
	.long	129679
	.long	129735
	.long	129742
	.long	129757
	.long	129759
	.long	129770
	.long	129776
	.long	129785
	.long	131072
	.long	196606
	.long	196608
	.long	262142
	.section .rdata,"dr"
	.align 16
.LC10:
	.quad	0
	.quad	-1
	.align 8
.LC11:
	.quad	_ZTVNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE+16
	.align 8
.LC15:
	.long	3
	.long	4
	.align 8
.LC18:
	.quad	_ZTVNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE+16
	.align 4
.LC24:
	.byte	-16
	.byte	-128
	.byte	-128
	.byte	-128
	.align 16
.LC33:
	.long	-1
	.long	-1
	.long	32766
	.long	0
	.align 16
.LC40:
	.long	-1
	.long	2147483647
	.long	0
	.long	0
	.align 8
.LC41:
	.long	-1
	.long	2146435071
	.align 16
.LC42:
	.long	2147483647
	.long	0
	.long	0
	.long	0
	.align 4
.LC43:
	.long	2139095039
	.def	__udivti3;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt13runtime_errorD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	_ZNSt13runtime_errorC2EPKc;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.def	__cxa_free_exception;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	memchr;	.scl	2;	.type	32;	.endef
	.def	strlen;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6localeD1Ev;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	toupper;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6localeC1ERKS_;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt6locale4nameB5cxx11Ev;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt6locale2id5_M_idEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6localeC1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6locale7classicEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt6localeeqERKS_;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_e;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_eSt12chars_formati;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_eSt12chars_format;	.scl	2;	.type	32;	.endef
	.def	frexpl;	.scl	2;	.type	32;	.endef
	.def	_ZSt24__throw_out_of_range_fmtPKcz;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_d;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_dSt12chars_formati;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_dSt12chars_format;	.scl	2;	.type	32;	.endef
	.def	frexp;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_f;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_fSt12chars_formati;	.scl	2;	.type	32;	.endef
	.def	_ZSt8to_charsPcS_fSt12chars_format;	.scl	2;	.type	32;	.endef
	.def	frexpf;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt13runtime_error4whatEv;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZNSt7__cxx118numpunctIcE2idE, "dr"
	.p2align	3, 0
	.globl	.refptr._ZNSt7__cxx118numpunctIcE2idE
	.linkonce	discard
.refptr._ZNSt7__cxx118numpunctIcE2idE:
	.quad	_ZNSt7__cxx118numpunctIcE2idE
