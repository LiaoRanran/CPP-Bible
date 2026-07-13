	.file	"_ch13_use.cpp"
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
	leaq	16+_ZTVSt12format_error(%rip), %rax
	movq	%rax, (%rcx)
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
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	leaq	16+_ZTVSt12format_error(%rip), %rax
	movq	%rcx, %rbx
	movq	%rax, (%rcx)
	call	_ZNSt13runtime_errorD2Ev
	movl	$16, %edx
	movq	%rbx, %rcx
	addq	$32, %rsp
	popq	%rbx
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
.LFB4936:
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movq	24(%rcx), %r13
	movq	8(%rcx), %rbx
	movq	296(%rcx), %rbp
	movq	%r13, %r12
	movq	%rcx, %rdi
	subq	%rbx, %r12
	testq	%rbp, %rbp
	js	.L16
	movq	304(%rcx), %rax
	cmpq	%rbp, %rax
	jnb	.L9
	subq	%rax, %rbp
	movq	288(%rcx), %rsi
	cmpq	%rbp, %r12
	cmovbe	%r12, %rbp
	testq	%rbp, %rbp
	jle	.L11
	addq	%rbx, %rbp
	.p2align 4,,10
	.p2align 3
.L13:
	movq	24(%rsi), %rax
	movzbl	(%rbx), %edx
	leaq	1(%rax), %rcx
	movq	%rcx, 24(%rsi)
	movb	%dl, (%rax)
	movq	24(%rsi), %rax
	subq	8(%rsi), %rax
	cmpq	16(%rsi), %rax
	je	.L17
.L12:
	addq	$1, %rbx
	cmpq	%rbp, %rbx
	jne	.L13
	movq	8(%rdi), %rbx
	movq	304(%rdi), %rax
.L11:
	movq	%rsi, 288(%rdi)
.L9:
	addq	%r12, %rax
	movq	%rbx, 24(%rdi)
	movq	%rax, 304(%rdi)
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L17:
	movq	(%rsi), %rax
	movq	%rsi, %rcx
	call	*(%rax)
	jmp	.L12
	.p2align 4,,10
	.p2align 3
.L16:
	testq	%r12, %r12
	movq	288(%rcx), %rsi
	jle	.L6
	.p2align 4,,10
	.p2align 3
.L8:
	movq	24(%rsi), %rax
	movzbl	(%rbx), %edx
	leaq	1(%rax), %rcx
	movq	%rcx, 24(%rsi)
	movb	%dl, (%rax)
	movq	24(%rsi), %rax
	subq	8(%rsi), %rax
	cmpq	16(%rsi), %rax
	je	.L18
.L7:
	addq	$1, %rbx
	cmpq	%rbx, %r13
	jne	.L8
	movq	8(%rdi), %rbx
.L6:
	movq	304(%rdi), %rax
	movq	%rsi, 288(%rdi)
	jmp	.L9
	.p2align 4,,10
	.p2align 3
.L18:
	movq	(%rsi), %rax
	movq	%rsi, %rcx
	call	*(%rax)
	jmp	.L7
	.seh_endproc
	.section	.text$_ZSt20__throw_format_errorPKc,"x"
	.linkonce discard
	.globl	_ZSt20__throw_format_errorPKc
	.def	_ZSt20__throw_format_errorPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt20__throw_format_errorPKc
_ZSt20__throw_format_errorPKc:
.LFB3268:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movq	%rcx, %rsi
	movl	$16, %ecx
	call	__cxa_allocate_exception
	movq	%rsi, %rdx
	movq	%rax, %rcx
	movq	%rax, %rbx
.LEHB0:
	call	_ZNSt13runtime_errorC2EPKc
.LEHE0:
	leaq	16+_ZTVSt12format_error(%rip), %rax
	movq	%rbx, %rcx
	leaq	_ZNSt12format_errorD1Ev(%rip), %r8
	movq	%rax, (%rbx)
	leaq	_ZTISt12format_error(%rip), %rdx
.LEHB1:
	call	__cxa_throw
.L21:
	movq	%rax, %rsi
	movq	%rbx, %rcx
	call	__cxa_free_exception
	movq	%rsi, %rcx
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
	.uleb128 .L21-.LFB3268
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
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	leaq	.LC0(%rip), %rcx
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
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	leaq	.LC1(%rip), %rcx
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
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	leaq	.LC2(%rip), %rcx
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
.LFB4182:
	.seh_endprologue
	movq	(%rcx), %rax
	leaq	16(%rcx), %rdx
	cmpq	%rdx, %rax
	je	.L25
	movq	16(%rcx), %rdx
	movq	%rax, %rcx
	addq	$1, %rdx
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L25:
	ret
	.seh_endproc
	.section	.text$_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	.def	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_:
.LFB4326:
	pushq	%rbx
	.seh_pushreg	%rbx
	.seh_endprologue
	xorl	%eax, %eax
	movl	$32, %r10d
	movq	%rcx, %r11
	movq	%rdx, %rbx
	movq	%rdx, %r9
	jmp	.L36
	.p2align 4,,10
	.p2align 3
.L41:
	leal	(%rax,%rax,4), %eax
	addq	$1, %r9
	movzbl	%cl, %ecx
	leal	(%rcx,%rax,2), %eax
	cmpq	%r9, %r8
	je	.L28
.L36:
	movzbl	(%r9), %edx
	leal	-48(%rdx), %ecx
	cmpb	$9, %cl
	ja	.L28
	subl	$4, %r10d
	jns	.L41
	movl	$10, %edx
	mull	%edx
	jo	.L33
	movzbl	%cl, %ecx
	addl	%eax, %ecx
	jc	.L33
	addq	$1, %r9
	movl	%ecx, %eax
	cmpq	%r9, %r8
	jne	.L36
.L28:
	cmpq	%r9, %rbx
	je	.L33
	cmpl	$65535, %eax
	ja	.L33
	movw	%ax, (%r11)
	movq	%r11, %rax
	movq	%r9, 8(%r11)
	popq	%rbx
	ret
	.p2align 4,,10
	.p2align 3
.L33:
	movq	%r11, %rax
	movq	$0, (%r11)
	movq	$0, 8(%r11)
	popq	%rbx
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
.LFB3720:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	16(%rcx), %r15
	movq	8(%rcx), %rbx
	movq	%r15, %rdi
	movq	%rcx, %r13
	subq	%rbx, %rdi
	cmpq	$2, %rdi
	je	.L109
	testq	%rdi, %rdi
	jne	.L44
.L42:
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L109:
	cmpb	$123, (%rbx)
	je	.L110
.L44:
	movq	%rdi, %r8
	movl	$123, %edx
	movq	%rbx, %rcx
	call	memchr
	movq	%rdi, %r8
	movl	$125, %edx
	movq	%rbx, %rcx
	movq	%rax, %r14
	movq	$-1, %rbp
	movq	$-1, %r12
	subq	%rbx, %r14
	testq	%rax, %rax
	cmove	%rbp, %r14
	call	memchr
	movq	%rax, %rsi
	subq	%rbx, %rsi
	testq	%rax, %rax
	cmove	%rbp, %rsi
	cmpq	%r14, %rsi
	je	.L51
	.p2align 4,,10
	.p2align 3
.L50:
	cmpq	%rsi, %r14
	jnb	.L111
	leaq	1(%r14), %rax
	cmpq	%rdi, %rax
	je	.L55
	cmpq	$-1, %rsi
	movzbl	1(%rbx,%r14), %ebp
	je	.L112
	xorl	%edi, %edi
	cmpb	$123, %bpl
	movq	0(%r13), %rax
	movq	%r13, %rcx
	sete	%dil
	addq	%r14, %rdi
	addq	8(%r13), %rdi
	leaq	1(%rdi), %rbx
	movq	%rdi, %rdx
	call	*(%rax)
	cmpb	$123, %bpl
	movq	16(%r13), %r15
	movq	%rbx, 8(%r13)
	je	.L113
	movzbl	1(%rdi), %eax
	cmpb	$125, %al
	je	.L114
	cmpb	$58, %al
	je	.L115
	leaq	2(%rdi), %rcx
	xorl	%edx, %edx
	cmpb	$48, %al
	je	.L64
	leal	-49(%rax), %edx
	cmpb	$8, %dl
	ja	.L65
	leaq	2(%rdi), %rcx
	movzbl	2(%rdi), %edx
	cmpq	%rcx, %r15
	je	.L66
	subl	$48, %edx
	cmpb	$9, %dl
	jbe	.L67
.L66:
	movsbw	%al, %dx
	subl	$48, %edx
.L64:
	movzbl	(%rcx), %eax
	cmpb	$125, %al
	jne	.L116
.L70:
	cmpl	$2, 24(%r13)
	movzwl	%dx, %edx
	je	.L45
	xorl	%eax, %eax
	movl	$1, 24(%r13)
	cmpb	$58, (%rcx)
	sete	%al
	addq	%rax, %rcx
	movq	%rcx, 8(%r13)
.L61:
	movq	0(%r13), %rax
	movq	%r13, %rcx
	call	*8(%rax)
	movq	8(%r13), %rax
	movq	16(%r13), %r15
	leaq	1(%rax), %rbx
	movq	%r15, %rdi
	movq	%rbx, 8(%r13)
	subq	%rbx, %rdi
	je	.L42
	movq	%rdi, %r8
	movl	$123, %edx
	movq	%rbx, %rcx
	call	memchr
	testq	%rax, %rax
	movq	%rax, %r14
	je	.L72
	subq	%rbx, %r14
.L108:
	movq	%rdi, %r8
	movl	$125, %edx
	movq	%rbx, %rcx
	call	memchr
	testq	%rax, %rax
	movq	%rax, %rsi
	je	.L86
.L81:
	subq	%rbx, %rsi
.L59:
	cmpq	%r14, %rsi
	jne	.L50
.L51:
	movq	0(%r13), %rax
	movq	%r15, %rdx
	movq	%r13, %rcx
	call	*(%rax)
	movq	16(%r13), %rax
	movq	%rax, 8(%r13)
	jmp	.L42
	.p2align 4,,10
	.p2align 3
.L111:
	leaq	1(%rsi), %rbp
	cmpq	%rdi, %rbp
	je	.L73
	cmpb	$125, 1(%rbx,%rsi)
	jne	.L73
	movq	8(%r13), %rbx
	movq	%r13, %rcx
	movq	0(%r13), %rax
	addq	%rbp, %rbx
	movq	%rbx, %rdx
	addq	$1, %rbx
	call	*(%rax)
	movq	16(%r13), %r15
	movq	%rbx, 8(%r13)
	movq	%r15, %rdi
	subq	%rbx, %rdi
	cmpq	$-1, %r14
	je	.L117
	testq	%rdi, %rdi
	je	.L42
	subq	$1, %r14
	subq	%rbp, %r14
	jmp	.L108
	.p2align 4,,10
	.p2align 3
.L117:
	testq	%rdi, %rdi
	je	.L42
	movq	%rdi, %r8
	movl	$125, %edx
	movq	%rbx, %rcx
	call	memchr
	testq	%rax, %rax
	movq	%rax, %rsi
	jne	.L81
	jmp	.L51
	.p2align 4,,10
	.p2align 3
.L112:
	cmpb	$123, %bpl
	jne	.L55
	addq	8(%r13), %rax
	movq	%r13, %rcx
	movq	%rax, %rbx
	movq	0(%r13), %rax
	movq	%rbx, %rdx
	addq	$1, %rbx
	call	*(%rax)
	movq	16(%r13), %r15
	movq	%rbx, 8(%r13)
.L78:
	movq	%r15, %rdi
	subq	%rbx, %rdi
	je	.L42
	movq	%rdi, %r8
	movl	$123, %edx
	movq	%rbx, %rcx
	call	memchr
	movq	%rax, %r14
	subq	%rbx, %r14
	testq	%rax, %rax
	cmove	%r12, %r14
	jmp	.L59
	.p2align 4,,10
	.p2align 3
.L113:
	subq	$2, %rsi
	subq	%r14, %rsi
	jmp	.L78
	.p2align 4,,10
	.p2align 3
.L86:
	movq	$-1, %rsi
	jmp	.L59
	.p2align 4,,10
	.p2align 3
.L116:
	cmpb	$58, %al
	je	.L70
.L65:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L114:
	cmpl	$1, 24(%r13)
	je	.L45
	movq	32(%r13), %rdx
	movl	$2, 24(%r13)
	leaq	1(%rdx), %rax
	movq	%rax, 32(%r13)
	jmp	.L61
	.p2align 4,,10
	.p2align 3
.L115:
	cmpl	$1, 24(%r13)
	je	.L45
	movq	32(%r13), %rdx
	addq	$2, %rdi
	movl	$2, 24(%r13)
	movq	%rdi, 8(%r13)
	leaq	1(%rdx), %rax
	movq	%rax, 32(%r13)
	jmp	.L61
	.p2align 4,,10
	.p2align 3
.L110:
	cmpb	$125, 1(%rbx)
	jne	.L44
	addq	$1, %rbx
	movq	(%rcx), %rax
	cmpl	$1, 24(%rcx)
	movq	%rbx, 8(%rcx)
	movq	8(%rax), %rax
	je	.L45
	movq	32(%rcx), %rdx
	movl	$2, 24(%rcx)
	leaq	1(%rdx), %rcx
	movq	%rcx, 32(%r13)
	movq	%r13, %rcx
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	rex.W jmp	*%rax
	.p2align 4,,10
	.p2align 3
.L67:
	leaq	32(%rsp), %rcx
	movq	%rbx, %rdx
	movq	%r15, %r8
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movq	40(%rsp), %rcx
	movzwl	32(%rsp), %edx
	testq	%rcx, %rcx
	je	.L65
	movzbl	(%rcx), %eax
	cmpb	$125, %al
	je	.L70
	jmp	.L116
	.p2align 4,,10
	.p2align 3
.L72:
	movq	%rdi, %r8
	movl	$125, %edx
	movq	%rbx, %rcx
	call	memchr
	testq	%rax, %rax
	movq	%rax, %rsi
	je	.L51
	movq	$-1, %r14
	jmp	.L81
.L55:
	leaq	.LC3(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
.L45:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L73:
	leaq	.LC4(%rip), %rcx
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
.LFB4142:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	%rdx, %rbx
	movzbl	(%rdx), %edx
	movq	%rcx, %rsi
	cmpb	$48, %dl
	je	.L137
	leaq	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE(%rip), %rcx
	movzbl	%dl, %eax
	cmpb	$9, (%rcx,%rax)
	ja	.L120
	leaq	32(%rsp), %rcx
	movq	%rbx, %rdx
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movq	40(%rsp), %rax
	movq	32(%rsp), %rdx
	testq	%rax, %rax
	je	.L138
	cmpq	%rax, %rbx
	movw	%dx, 4(%rsi)
	movl	$1, %ecx
	je	.L118
.L122:
	movzwl	(%rsi), %edx
	andl	$3, %ecx
	sall	$7, %ecx
	andw	$-385, %dx
	orl	%ecx, %edx
	movw	%dx, (%rsi)
.L118:
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.p2align 4,,10
	.p2align 3
.L120:
	cmpb	$123, %dl
	movq	%rbx, %rax
	jne	.L118
	leaq	1(%rbx), %rax
	cmpq	%rax, %r8
	je	.L139
	movsbw	1(%rbx), %dx
	cmpb	$125, %dl
	je	.L140
	cmpb	$48, %dl
	je	.L141
	leal	-49(%rdx), %ecx
	cmpb	$8, %cl
	ja	.L131
	leaq	2(%rbx), %r10
	cmpq	%r10, %r8
	je	.L131
	movzbl	2(%rbx), %ecx
	subl	$48, %ecx
	cmpb	$9, %cl
	ja	.L132
	leaq	32(%rsp), %rcx
	movq	%rax, %rdx
	movq	%r9, 104(%rsp)
	movq	%r8, 96(%rsp)
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzwl	32(%rsp), %edx
	movq	40(%rsp), %rax
	movq	104(%rsp), %r9
	movq	96(%rsp), %r8
.L129:
	cmpq	%rax, %r8
	je	.L131
	testq	%rax, %rax
	je	.L131
.L134:
	cmpb	$125, (%rax)
	jne	.L131
	cmpl	$2, 16(%r9)
	je	.L133
	movl	$1, 16(%r9)
	movw	%dx, 4(%rsi)
	jmp	.L127
	.p2align 4,,10
	.p2align 3
.L140:
	cmpl	$1, 16(%r9)
	je	.L133
	movq	24(%r9), %rdx
	movl	$2, 16(%r9)
	leaq	1(%rdx), %rcx
	movq	%rcx, 24(%r9)
	movw	%dx, 4(%rsi)
.L127:
	addq	$1, %rax
	cmpq	%rax, %rbx
	je	.L118
	movl	$2, %ecx
	jmp	.L122
	.p2align 4,,10
	.p2align 3
.L141:
	leaq	2(%rbx), %rax
	xorl	%edx, %edx
	jmp	.L129
	.p2align 4,,10
	.p2align 3
.L132:
	subl	$48, %edx
	movq	%r10, %rax
	jmp	.L134
.L139:
	leaq	.LC3(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
.L138:
	leaq	.LC6(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
.L137:
	leaq	.LC5(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
.L133:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L131:
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
.LFB3757:
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	movq	8(%rdx), %rsi
	movl	%r8d, %eax
	movl	$0, 44(%rsp)
	movq	%rcx, %rbx
	movq	%rdx, %r9
	andl	$15, %eax
	movl	%r8d, %edi
	movb	$32, 44(%rsp)
	movq	$0, 36(%rsp)
	sall	$3, %eax
	movb	%al, 37(%rsp)
	movq	(%rdx), %rax
	cmpq	%rax, %rsi
	je	.L143
	movzbl	(%rax), %edx
	cmpb	$125, %dl
	je	.L143
	cmpb	$123, %dl
	je	.L158
	movq	%rsi, %rcx
	subq	%rax, %rcx
	cmpq	$1, %rcx
	jle	.L145
	movzbl	1(%rax), %ecx
	cmpb	$62, %cl
	je	.L173
	cmpb	$94, %cl
	je	.L174
	cmpb	$60, %cl
	je	.L211
	cmpb	$62, %dl
	je	.L182
	cmpb	$94, %dl
	je	.L183
	cmpb	$60, %dl
	jne	.L150
.L184:
	movl	$1, %ecx
.L149:
	addq	$1, %rax
	jmp	.L148
	.p2align 4,,10
	.p2align 3
.L211:
	movl	$1, %ecx
.L146:
	movb	%dl, 44(%rsp)
	addq	$2, %rax
.L148:
	movzbl	36(%rsp), %edx
	andl	$-4, %edx
	orl	%ecx, %edx
	cmpq	%rax, %rsi
	movb	%dl, 36(%rsp)
	je	.L143
.L150:
	movzbl	(%rax), %edx
	cmpb	$125, %dl
	jne	.L209
.L143:
	movq	36(%rsp), %rdx
	movq	%rdx, (%rbx)
	movzbl	44(%rsp), %edx
	movb	%dl, 8(%rbx)
	addq	$48, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	ret
	.p2align 4,,10
	.p2align 3
.L145:
	cmpb	$62, %dl
	je	.L182
	cmpb	$94, %dl
	je	.L183
	cmpb	$60, %dl
	je	.L184
.L209:
	leal	-32(%rdx), %ecx
	movq	%rax, %r10
	cmpb	$13, %cl
	ja	.L210
	leaq	CSWTCH.514(%rip), %r8
	movzbl	%cl, %ecx
	movl	(%r8,%rcx,4), %ecx
	testl	%ecx, %ecx
	jne	.L154
	cmpb	$35, %dl
	jne	.L158
.L155:
	orb	$16, 36(%rsp)
	addq	$1, %rax
	cmpq	%rax, %rsi
	je	.L143
	movzbl	1(%r10), %edx
	cmpb	$125, %dl
	je	.L143
.L210:
	cmpb	$48, %dl
	movq	%rax, %rcx
	jne	.L158
	orb	$64, 36(%rsp)
	addq	$1, %rax
	cmpq	%rax, %rsi
	je	.L143
	cmpb	$125, 1(%rcx)
	je	.L143
	.p2align 4,,10
	.p2align 3
.L158:
	leaq	36(%rsp), %rcx
	movq	%rsi, %r8
	movq	%rax, %rdx
	call	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	cmpq	%rax, %rsi
	je	.L143
	movzbl	(%rax), %edx
	cmpb	$125, %dl
	je	.L143
	cmpb	$76, %dl
	je	.L212
.L159:
	subl	$66, %edx
	cmpb	$54, %dl
	ja	.L171
	leaq	.L172(%rip), %rcx
	movzbl	%dl, %edx
	movslq	(%rcx,%rdx,4), %rdx
	addq	%rcx, %rdx
	jmp	*%rdx
	.section .rdata,"dr"
	.align 4
.L172:
	.long	.L162-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L168-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L160-.L172
	.long	.L163-.L172
	.long	.L165-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L166-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L169-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L171-.L172
	.long	.L167-.L172
	.section	.text$_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L154:
	movzbl	36(%rsp), %edx
	andl	$3, %ecx
	addq	$1, %rax
	sall	$2, %ecx
	andl	$-13, %edx
	orl	%ecx, %edx
	cmpq	%rax, %rsi
	movb	%dl, 36(%rsp)
	je	.L143
	movzbl	1(%r10), %edx
	cmpb	$125, %dl
	je	.L143
	cmpb	$35, %dl
	movq	%rax, %r10
	je	.L155
	jmp	.L210
	.p2align 4,,10
	.p2align 3
.L168:
	addq	$1, %rax
	movl	$6, %edx
	.p2align 4,,10
	.p2align 3
.L161:
	movzbl	37(%rsp), %ecx
	sall	$3, %edx
	andl	$-121, %ecx
	orl	%ecx, %edx
	cmpq	%rax, %rsi
	movb	%dl, 37(%rsp)
	je	.L143
	.p2align 4,,10
	.p2align 3
.L171:
	cmpb	$125, (%rax)
	je	.L143
.L164:
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L162:
	addq	$1, %rax
	movl	$3, %edx
	jmp	.L161
.L167:
	addq	$1, %rax
	movl	$5, %edx
	jmp	.L161
.L166:
	addq	$1, %rax
	movl	$4, %edx
	jmp	.L161
.L165:
	addq	$1, %rax
	movl	$1, %edx
	jmp	.L161
.L160:
	addq	$1, %rax
	movl	$2, %edx
	jmp	.L161
.L163:
	testl	%edi, %edi
	je	.L164
	addq	$1, %rax
	movl	$7, %edx
	jmp	.L161
.L169:
	testl	%edi, %edi
	jne	.L164
	addq	$1, %rax
	xorl	%edx, %edx
	jmp	.L161
	.p2align 4,,10
	.p2align 3
.L174:
	movl	$3, %ecx
	jmp	.L146
	.p2align 4,,10
	.p2align 3
.L173:
	movl	$2, %ecx
	jmp	.L146
	.p2align 4,,10
	.p2align 3
.L183:
	movl	$3, %ecx
	jmp	.L149
	.p2align 4,,10
	.p2align 3
.L182:
	movl	$2, %ecx
	jmp	.L149
	.p2align 4,,10
	.p2align 3
.L212:
	orb	$32, 36(%rsp)
	leaq	1(%rax), %rcx
	cmpq	%rcx, %rsi
	jne	.L213
	movq	%rsi, %rax
	jmp	.L143
.L213:
	movzbl	1(%rax), %edx
	movq	%rcx, %rax
	cmpb	$125, %dl
	je	.L143
	jmp	.L159
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
.LFB4690:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movq	8(%rcx), %rax
	movq	144(%rsp), %rsi
	leaq	(%rdx,%r8), %r13
	movq	%rax, %r15
	movq	%rcx, %rbx
	subq	%r8, %rsi
	subq	%r13, %r15
	movq	%rdx, %r12
	leaq	16(%rcx), %r14
	addq	%rax, %rsi
	cmpq	(%rcx), %r14
	movq	%r9, %rbp
	je	.L227
	movq	16(%rcx), %rax
.L215:
	testq	%rsi, %rsi
	js	.L240
	cmpq	%rsi, %rax
	jnb	.L217
	addq	%rax, %rax
	cmpq	%rax, %rsi
	jnb	.L217
	testq	%rax, %rax
	js	.L218
	leaq	1(%rax), %rcx
	movq	%rax, %rsi
	call	_Znwy
	testq	%r12, %r12
	movq	%rax, %rdi
	je	.L220
	cmpq	$1, %r12
	movq	(%rbx), %rdx
	je	.L241
	.p2align 4,,10
	.p2align 3
.L221:
	movq	%r12, %r8
	movq	%rax, %rcx
	call	memcpy
.L220:
	testq	%rbp, %rbp
	je	.L222
	cmpq	$0, 144(%rsp)
	je	.L222
	cmpq	$1, 144(%rsp)
	leaq	(%rdi,%r12), %rcx
	je	.L242
	movq	144(%rsp), %r8
	movq	%rbp, %rdx
	call	memcpy
.L222:
	testq	%r15, %r15
	movq	(%rbx), %rbp
	jne	.L243
.L224:
	cmpq	%r14, %rbp
	je	.L226
	movq	16(%rbx), %rax
	movq	%rbp, %rcx
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L226:
	movq	%rdi, (%rbx)
	movq	%rsi, 16(%rbx)
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L217:
	movq	%rsi, %rcx
	addq	$1, %rcx
	js	.L218
	call	_Znwy
	testq	%r12, %r12
	movq	%rax, %rdi
	je	.L220
	cmpq	$1, %r12
	movq	(%rbx), %rdx
	jne	.L221
.L241:
	movzbl	(%rdx), %eax
	movb	%al, (%rdi)
	jmp	.L220
	.p2align 4,,10
	.p2align 3
.L243:
	movq	144(%rsp), %r10
	leaq	0(%rbp,%r13), %rdx
	addq	%r12, %r10
	cmpq	$1, %r15
	leaq	(%rdi,%r10), %rcx
	je	.L244
	movq	%r15, %r8
	call	memcpy
	jmp	.L224
	.p2align 4,,10
	.p2align 3
.L218:
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L227:
	movl	$15, %eax
	jmp	.L215
	.p2align 4,,10
	.p2align 3
.L242:
	movzbl	0(%rbp), %eax
	testq	%r15, %r15
	movq	(%rbx), %rbp
	movb	%al, (%rcx)
	je	.L224
	jmp	.L243
	.p2align 4,,10
	.p2align 3
.L244:
	movzbl	(%rdx), %eax
	movb	%al, (%rcx)
	jmp	.L224
.L240:
	leaq	.LC7(%rip), %rcx
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
.LFB4296:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movabsq	$9223372036854775807, %rax
	movq	8(%rcx), %r9
	movq	24(%rcx), %r8
	movq	296(%rcx), %rdx
	movq	%rcx, %rbx
	subq	%r9, %r8
	subq	%rdx, %rax
	cmpq	%r8, %rax
	jb	.L255
	movq	288(%rcx), %rcx
	leaq	304(%rbx), %rax
	leaq	(%r8,%rdx), %rsi
	cmpq	%rax, %rcx
	je	.L251
	movq	304(%rbx), %rax
.L247:
	cmpq	%rsi, %rax
	jb	.L248
	testq	%r8, %r8
	je	.L249
	addq	%rdx, %rcx
	cmpq	$1, %r8
	je	.L256
	movq	%r9, %rdx
	call	memcpy
	movq	288(%rbx), %rcx
.L249:
	movq	%rsi, 296(%rbx)
	movb	$0, (%rcx,%rsi)
	movq	8(%rbx), %rax
	movq	%rax, 24(%rbx)
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.p2align 4,,10
	.p2align 3
.L248:
	leaq	288(%rbx), %rcx
	movq	%r8, 32(%rsp)
	xorl	%r8d, %r8d
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	movq	288(%rbx), %rcx
	jmp	.L249
	.p2align 4,,10
	.p2align 3
.L251:
	movl	$15, %eax
	jmp	.L247
	.p2align 4,,10
	.p2align 3
.L256:
	movzbl	(%r9), %eax
	movb	%al, (%rcx)
	movq	288(%rbx), %rcx
	jmp	.L249
.L255:
	leaq	.LC8(%rip), %rcx
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
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$800, %rsp
	.seh_stackalloc	800
	.seh_endprologue
	leaq	16+_ZTVNSt8__format9_Seq_sinkINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE(%rip), %rdi
	leaq	16+_ZTVNSt8__format10_Iter_sinkIcNS_10_Sink_iterIcEEEE(%rip), %r11
	movq	%rdi, %xmm0
	movq	8(%rdx), %rax
	movdqu	(%r8), %xmm1
	movq	%rax, 104(%rsp)
	addq	(%rdx), %rax
	leaq	512(%rsp), %r8
	movq	%rcx, %rbx
	movq	%r8, %xmm2
	movq	%r8, 504(%rsp)
	leaq	192(%rsp), %r8
	punpcklqdq	%xmm2, %xmm0
	movaps	%xmm0, 480(%rsp)
	movq	%r11, %xmm0
	movq	%r8, %xmm3
	movaps	%xmm1, 48(%rsp)
	leaq	480(%rsp), %rcx
	punpcklqdq	%xmm3, %xmm0
	movq	%rax, 112(%rsp)
	movaps	%xmm0, 160(%rsp)
	leaq	16+_ZTVNSt8__format19_Formatting_scannerINS_10_Sink_iterIcEEcEE(%rip), %rax
	movdqa	.LC9(%rip), %xmm0
	leaq	784(%rsp), %rsi
	movq	%rcx, 448(%rsp)
	movq	%rcx, 64(%rsp)
	leaq	96(%rsp), %rcx
	movq	%rax, 96(%rsp)
	leaq	48(%rsp), %rax
	movq	$256, 496(%rsp)
	movq	%rsi, 768(%rsp)
	movq	$0, 776(%rsp)
	movb	$0, 784(%rsp)
	movq	$256, 176(%rsp)
	movq	%r8, 184(%rsp)
	movq	$-1, 456(%rsp)
	movq	$0, 464(%rsp)
	movq	$0, 72(%rsp)
	movb	$0, 80(%rsp)
	movl	$0, 120(%rsp)
	movaps	%xmm0, 128(%rsp)
	movq	%rax, 144(%rsp)
.LEHB2:
	call	_ZNSt8__format8_ScannerIcE7_M_scanEv
.LEHE2:
	cmpb	$0, 80(%rsp)
	jne	.L288
.L258:
	movq	488(%rsp), %r9
	movabsq	$9223372036854775807, %rax
	movq	504(%rsp), %r8
	movq	776(%rsp), %rdx
	subq	%r9, %r8
	subq	%rdx, %rax
	cmpq	%r8, %rax
	jb	.L289
	movq	768(%rsp), %rcx
	leaq	(%r8,%rdx), %rbp
	cmpq	%rsi, %rcx
	je	.L276
	movq	784(%rsp), %rax
.L264:
	cmpq	%rbp, %rax
	jb	.L265
	testq	%r8, %r8
	jne	.L290
.L266:
	movq	%rbp, 776(%rsp)
	leaq	16(%rbx), %rdx
	movb	$0, (%rcx,%rbp)
	movq	488(%rsp), %rax
	movq	%rdx, (%rbx)
	movq	%rax, 504(%rsp)
	movq	768(%rsp), %rax
	cmpq	%rsi, %rax
	je	.L291
	movq	%rax, (%rbx)
	movq	784(%rsp), %rax
	movq	776(%rsp), %rcx
	movq	%rax, 16(%rbx)
.L275:
	movq	%rbx, %rax
	movq	%rcx, 8(%rbx)
	addq	$800, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	ret
	.p2align 4,,10
	.p2align 3
.L290:
	addq	%rdx, %rcx
	cmpq	$1, %r8
	je	.L292
	movq	%r9, %rdx
	call	memcpy
	movq	768(%rsp), %rcx
	jmp	.L266
	.p2align 4,,10
	.p2align 3
.L288:
	leaq	72(%rsp), %rcx
	call	_ZNSt6localeD1Ev
	jmp	.L258
	.p2align 4,,10
	.p2align 3
.L265:
	leaq	768(%rsp), %r12
	movq	%r8, 32(%rsp)
	xorl	%r8d, %r8d
	movq	%r12, %rcx
.LEHB3:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	movq	768(%rsp), %rcx
	jmp	.L266
	.p2align 4,,10
	.p2align 3
.L276:
	movl	$15, %eax
	jmp	.L264
	.p2align 4,,10
	.p2align 3
.L291:
	movq	776(%rsp), %rcx
	leaq	1(%rcx), %r8
	cmpl	$8, %r8d
	jnb	.L269
	testb	$4, %r8b
	jne	.L293
	testl	%r8d, %r8d
	je	.L275
	movzbl	(%rsi), %eax
	testb	$2, %r8b
	movb	%al, 16(%rbx)
	je	.L275
	movl	%r8d, %r8d
	movzwl	-2(%rsi,%r8), %eax
	movw	%ax, -2(%rdx,%r8)
	jmp	.L275
	.p2align 4,,10
	.p2align 3
.L292:
	movzbl	(%r9), %eax
	movb	%al, (%rcx)
	movq	768(%rsp), %rcx
	jmp	.L266
	.p2align 4,,10
	.p2align 3
.L269:
	movl	%r8d, %r9d
	subl	$1, %r8d
	movq	-8(%rsi,%r9), %r10
	cmpl	$8, %r8d
	movq	%r10, -8(%rdx,%r9)
	jb	.L275
	andl	$-8, %r8d
	xorl	%r9d, %r9d
.L273:
	movl	%r9d, %r10d
	addl	$8, %r9d
	movq	(%rax,%r10), %r11
	cmpl	%r8d, %r9d
	movq	%r11, (%rdx,%r10)
	jb	.L273
	jmp	.L275
.L293:
	movl	(%rsi), %eax
	movl	%r8d, %r8d
	movl	%eax, 16(%rbx)
	movl	-4(%rsi,%r8), %eax
	movl	%eax, -4(%rdx,%r8)
	jmp	.L275
.L289:
	leaq	.LC8(%rip), %rcx
	leaq	768(%rsp), %r12
	call	_ZSt20__throw_length_errorPKc
.LEHE3:
.L277:
	movq	%rax, %rbx
.L263:
	movq	%r12, %rcx
	movq	%rdi, 480(%rsp)
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	%rbx, %rcx
.LEHB4:
	call	_Unwind_Resume
.LEHE4:
.L278:
	cmpb	$0, 80(%rsp)
	movq	%rax, %rbx
	je	.L262
	leaq	72(%rsp), %rcx
	call	_ZNSt6localeD1Ev
.L262:
	leaq	768(%rsp), %r12
	jmp	.L263
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
	.uleb128 .L278-.LFB3466
	.uleb128 0
	.uleb128 .LEHB3-.LFB3466
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L277-.LFB3466
	.uleb128 0
	.uleb128 .LEHB4-.LFB3466
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE3466:
	.section	.text$_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZN3pkg7printlnIJRiyEEEvSt19basic_format_stringIcJDpNSt13type_identityIT_E4typeEEEDpOS4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN3pkg7printlnIJRiyEEEvSt19basic_format_stringIcJDpNSt13type_identityIT_E4typeEEEDpOS4_
	.def	_ZN3pkg7printlnIJRiyEEEvSt19basic_format_stringIcJDpNSt13type_identityIT_E4typeEEEDpOS4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3pkg7printlnIJRiyEEEvSt19basic_format_stringIcJDpNSt13type_identityIT_E4typeEEEDpOS4_
_ZN3pkg7printlnIJRiyEEEvSt19basic_format_stringIcJDpNSt13type_identityIT_E4typeEEEDpOS4_:
.LFB4144:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$136, %rsp
	.seh_stackalloc	136
	.seh_endprologue
	movl	(%rdx), %edx
	movq	(%rcx), %r9
	movq	8(%rcx), %rax
	movl	%edx, 96(%rsp)
	movq	(%r8), %rdx
	leaq	64(%rsp), %rsi
	leaq	32(%rsp), %r8
	movq	%rsi, %rcx
	movq	%r9, 48(%rsp)
	leaq	96(%rsp), %rbx
	movq	%rax, 56(%rsp)
	movq	$3122, 32(%rsp)
	movq	%rdx, 112(%rsp)
	leaq	48(%rsp), %rdx
	movq	%rbx, 40(%rsp)
.LEHB5:
	call	_ZSt7vformatB5cxx11St17basic_string_viewIcSt11char_traitsIcEESt17basic_format_argsISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE
.LEHE5:
	movq	72(%rsp), %r8
	movq	64(%rsp), %rdx
	movq	.refptr._ZSt4cout(%rip), %rcx
.LEHB6:
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	movb	$10, 96(%rsp)
	movq	%rax, %rcx
	movq	(%rax), %rax
	movq	-24(%rax), %rax
	cmpq	$0, 16(%rcx,%rax)
	je	.L295
	movl	$1, %r8d
	movq	%rbx, %rdx
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
.L298:
	movq	64(%rsp), %rcx
	leaq	80(%rsp), %rax
	cmpq	%rax, %rcx
	je	.L294
	movq	80(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	nop
.L294:
	addq	$136, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.p2align 4,,10
	.p2align 3
.L295:
	movl	$10, %edx
	call	_ZNSo3putEc
.LEHE6:
	jmp	.L298
.L300:
	movq	%rax, %rbx
	movq	%rsi, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	%rbx, %rcx
.LEHB7:
	call	_Unwind_Resume
	nop
.LEHE7:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4144:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4144-.LLSDACSB4144
.LLSDACSB4144:
	.uleb128 .LEHB5-.LFB4144
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LFB4144
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L300-.LFB4144
	.uleb128 0
	.uleb128 .LEHB7-.LFB4144
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSE4144:
	.section	.text$_ZN3pkg7printlnIJRiyEEEvSt19basic_format_stringIcJDpNSt13type_identityIT_E4typeEEEDpOS4_,"x"
	.linkonce discard
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC10:
	.ascii "sum={}, n={}\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3695:
	subq	$72, %rsp
	.seh_stackalloc	72
	.seh_endprologue
	call	__main
	leaq	.LC10(%rip), %rax
	movl	$10, 52(%rsp)
	leaq	52(%rsp), %rdx
	movq	%rax, 40(%rsp)
	movq	$4, 56(%rsp)
	leaq	32(%rsp), %rcx
	movq	$12, 32(%rsp)
	leaq	56(%rsp), %r8
	call	_ZN3pkg7printlnIJRiyEEEvSt19basic_format_stringIcJDpNSt13type_identityIT_E4typeEEEDpOS4_
	movl	$10, %eax
	addq	$72, %rsp
	ret
	.seh_endproc
	.section	.text$_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	.def	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE:
.LFB4987:
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movq	(%rdx), %rdi
	movq	8(%rdx), %rbp
	testq	%rdi, %rdi
	movq	%rcx, %rsi
	jne	.L318
.L304:
	movq	%rsi, %rax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.p2align 4,,10
	.p2align 3
.L318:
	movq	24(%rcx), %rcx
	movq	16(%rsi), %rbx
	movq	%rcx, %rax
	subq	8(%rsi), %rax
	subq	%rax, %rbx
	cmpq	%rbx, %rdi
	jb	.L305
	.p2align 4,,10
	.p2align 3
.L307:
	testq	%rbx, %rbx
	je	.L306
	movq	%rbx, %r8
	movq	%rbp, %rdx
	call	memcpy
.L306:
	movq	(%rsi), %rax
	movq	%rsi, %rcx
	addq	%rbx, %rbp
	subq	%rbx, %rdi
	addq	%rbx, 24(%rsi)
	call	*(%rax)
	movq	24(%rsi), %rcx
	movq	16(%rsi), %rbx
	movq	%rcx, %rax
	subq	8(%rsi), %rax
	subq	%rax, %rbx
	cmpq	%rbx, %rdi
	jnb	.L307
	testq	%rdi, %rdi
	je	.L304
.L305:
	movq	%rdi, %r8
	movq	%rbp, %rdx
	call	memcpy
	movq	%rsi, %rax
	addq	%rdi, 24(%rsi)
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
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
.LFB4873:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	movq	48(%rcx), %rbx
	movq	8(%rcx), %rax
	movq	16(%rbx), %rcx
	subq	%rax, %rdx
	movq	%rax, 40(%rsp)
	movq	%rdx, 32(%rsp)
	leaq	32(%rsp), %rdx
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	movq	%rax, 16(%rbx)
	addq	$48, %rsp
	popq	%rbx
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
.LFB5011:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	8(%rdx), %rsi
	movq	(%rdx), %rax
	movl	$0, 44(%rsp)
	movq	%rcx, %rbx
	movq	%rdx, %r9
	cmpq	%rax, %rsi
	movb	$32, 44(%rsp)
	movq	$0, 36(%rsp)
	je	.L321
	movzbl	(%rax), %edx
	cmpb	$125, %dl
	je	.L321
	cmpb	$123, %dl
	je	.L322
	movq	%rsi, %rcx
	subq	%rax, %rcx
	cmpq	$1, %rcx
	jle	.L323
	movzbl	1(%rax), %ecx
	cmpb	$62, %cl
	je	.L335
	cmpb	$94, %cl
	je	.L336
	cmpb	$60, %cl
	je	.L353
	cmpb	$62, %dl
	je	.L342
	cmpb	$94, %dl
	je	.L343
	cmpb	$60, %dl
	jne	.L328
.L344:
	movl	$1, %ecx
.L327:
	addq	$1, %rax
	jmp	.L326
	.p2align 4,,10
	.p2align 3
.L353:
	movl	$1, %ecx
.L324:
	movb	%dl, 44(%rsp)
	addq	$2, %rax
.L326:
	movzbl	36(%rsp), %edx
	andl	$-4, %edx
	orl	%ecx, %edx
	cmpq	%rax, %rsi
	movb	%dl, 36(%rsp)
	je	.L321
.L328:
	movzbl	(%rax), %edx
	cmpb	$125, %dl
	jne	.L352
.L321:
	movq	36(%rsp), %rdx
	movq	%rdx, (%rbx)
	movzbl	44(%rsp), %edx
	movb	%dl, 8(%rbx)
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.p2align 4,,10
	.p2align 3
.L323:
	cmpb	$62, %dl
	je	.L342
	cmpb	$94, %dl
	je	.L343
	cmpb	$60, %dl
	je	.L344
.L352:
	cmpb	$48, %dl
	movq	%rax, %rcx
	je	.L354
	.p2align 4,,10
	.p2align 3
.L322:
	leaq	36(%rsp), %rcx
	movq	%rsi, %r8
	movq	%rax, %rdx
	call	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	cmpq	%rax, %rsi
	je	.L321
	movzbl	(%rax), %edx
	movl	%edx, %ecx
	andl	$-33, %ecx
	cmpb	$80, %cl
	jne	.L332
	cmpb	$80, %dl
	jne	.L333
	movzbl	37(%rsp), %edx
	andl	$-121, %edx
	orl	$8, %edx
	movb	%dl, 37(%rsp)
.L333:
	leaq	1(%rax), %rcx
	cmpq	%rsi, %rcx
	je	.L341
	movzbl	1(%rax), %edx
	movq	%rcx, %rax
.L332:
	cmpb	$125, %dl
	je	.L321
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L354:
	orb	$64, 36(%rsp)
	addq	$1, %rax
	cmpq	%rax, %rsi
	je	.L321
	cmpb	$125, 1(%rcx)
	jne	.L322
	jmp	.L321
	.p2align 4,,10
	.p2align 3
.L336:
	movl	$3, %ecx
	jmp	.L324
	.p2align 4,,10
	.p2align 3
.L335:
	movl	$2, %ecx
	jmp	.L324
	.p2align 4,,10
	.p2align 3
.L343:
	movl	$3, %ecx
	jmp	.L327
	.p2align 4,,10
	.p2align 3
.L342:
	movl	$2, %ecx
	jmp	.L327
.L341:
	movq	%rsi, %rax
	jmp	.L321
	.seh_endproc
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc:
.LFB5057:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movq	(%rcx), %rdi
	movq	8(%rcx), %rsi
	leaq	16(%rcx), %r12
	movq	%rcx, %rbx
	movl	%edx, %r13d
	leaq	1(%rsi), %rbp
	cmpq	%rdi, %r12
	je	.L368
	movq	16(%rcx), %rax
	cmpq	%rbp, %rax
	jb	.L369
.L357:
	movb	%r13b, (%rdi,%rsi)
	movq	(%rbx), %rax
	movq	%rbp, 8(%rbx)
	movb	$0, 1(%rax,%rsi)
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L369:
	testq	%rbp, %rbp
	js	.L370
	leaq	(%rax,%rax), %r14
	cmpq	%r14, %rbp
	jb	.L371
	movq	%rsi, %rcx
	movq	%rbp, %r14
	addq	$2, %rcx
	js	.L361
.L362:
	call	_Znwy
	testq	%rsi, %rsi
	movq	%rax, %rdi
	jne	.L358
	movq	(%rbx), %r15
.L363:
	cmpq	%r15, %r12
	je	.L366
	movq	16(%rbx), %rax
	movq	%r15, %rcx
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L366:
	movq	%rdi, (%rbx)
	movq	%r14, 16(%rbx)
	jmp	.L357
	.p2align 4,,10
	.p2align 3
.L368:
	cmpq	$16, %rbp
	jne	.L357
	movl	$31, %ecx
	movl	$30, %r14d
	call	_Znwy
	movq	%rax, %rdi
.L358:
	cmpq	$1, %rsi
	movq	(%rbx), %r15
	je	.L372
	movq	%rsi, %r8
	movq	%r15, %rdx
	movq	%rdi, %rcx
	call	memcpy
	jmp	.L363
	.p2align 4,,10
	.p2align 3
.L372:
	movzbl	(%r15), %eax
	movb	%al, (%rdi)
	jmp	.L363
	.p2align 4,,10
	.p2align 3
.L371:
	leaq	1(%r14), %rcx
	testq	%r14, %r14
	jns	.L362
.L361:
	call	_ZSt17__throw_bad_allocv
.L370:
	leaq	.LC7(%rip), %rcx
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC11:
	.ascii "format error: missing precision after '.' in format string\0"
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	.def	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE:
.LFB5101:
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$72, %rsp
	.seh_stackalloc	72
	.seh_endprologue
	movq	8(%rdx), %rsi
	movq	(%rdx), %rax
	movl	$0, 60(%rsp)
	movq	%rcx, %rdi
	movq	%rdx, %rbx
	cmpq	%rax, %rsi
	movb	$32, 60(%rsp)
	movq	$0, 52(%rsp)
	je	.L374
	movzbl	(%rax), %edx
	cmpb	$125, %dl
	je	.L374
	cmpb	$123, %dl
	je	.L375
	movq	%rsi, %rcx
	subq	%rax, %rcx
	cmpq	$1, %rcx
	jle	.L376
	movzbl	1(%rax), %ecx
	cmpb	$62, %cl
	je	.L421
	cmpb	$94, %cl
	je	.L422
	cmpb	$60, %cl
	je	.L472
	cmpb	$62, %dl
	je	.L431
	cmpb	$94, %dl
	je	.L432
	cmpb	$60, %dl
	jne	.L381
.L433:
	movl	$1, %ecx
.L380:
	addq	$1, %rax
	jmp	.L379
	.p2align 4,,10
	.p2align 3
.L472:
	movl	$1, %ecx
.L377:
	movb	%dl, 60(%rsp)
	addq	$2, %rax
.L379:
	movzbl	52(%rsp), %edx
	andl	$-4, %edx
	orl	%ecx, %edx
	cmpq	%rax, %rsi
	movb	%dl, 52(%rsp)
	je	.L374
.L381:
	movzbl	(%rax), %edx
	cmpb	$125, %dl
	jne	.L470
.L374:
	movq	52(%rsp), %rdx
	movq	%rdx, (%rdi)
	movzbl	60(%rsp), %edx
	movb	%dl, 8(%rdi)
	addq	$72, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.p2align 4,,10
	.p2align 3
.L376:
	cmpb	$62, %dl
	je	.L431
	cmpb	$94, %dl
	je	.L432
	cmpb	$60, %dl
	je	.L433
.L470:
	leal	-32(%rdx), %ecx
	movq	%rax, %r9
	cmpb	$13, %cl
	ja	.L471
	leaq	CSWTCH.514(%rip), %r8
	movzbl	%cl, %ecx
	movl	(%r8,%rcx,4), %ecx
	testl	%ecx, %ecx
	jne	.L385
	cmpb	$35, %dl
	jne	.L390
.L386:
	orb	$16, 52(%rsp)
	addq	$1, %rax
	cmpq	%rax, %rsi
	je	.L374
	movzbl	1(%r9), %edx
	cmpb	$125, %dl
	je	.L374
.L471:
	cmpb	$48, %dl
	movq	%rax, %r9
	je	.L473
.L390:
	cmpb	$46, %dl
	jne	.L375
.L391:
	movzbl	1(%rax), %ecx
	leaq	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE(%rip), %r8
	leaq	1(%rax), %rbp
	cmpb	$9, (%r8,%rcx)
	ja	.L393
	leaq	32(%rsp), %rcx
	movq	%rbp, %rdx
	movq	%rsi, %r8
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movq	40(%rsp), %rax
	movq	32(%rsp), %rdx
	testq	%rax, %rax
	je	.L474
	cmpq	%rax, %rbp
	movw	%dx, 58(%rsp)
	je	.L396
	movl	$1, %ecx
.L395:
	movzbl	53(%rsp), %edx
	addl	%ecx, %ecx
	andl	$-7, %edx
	orl	%ecx, %edx
	cmpq	%rax, %rsi
	movb	%dl, 53(%rsp)
	je	.L374
	movzbl	(%rax), %edx
	cmpb	$125, %dl
	je	.L374
	cmpb	$76, %dl
	je	.L430
	subl	$65, %edx
	cmpb	$38, %dl
	ja	.L408
	leaq	.L410(%rip), %rcx
	movzbl	%dl, %edx
	movslq	(%rcx,%rdx,4), %rdx
	addq	%rcx, %rdx
	jmp	*%rdx
	.section .rdata,"dr"
	.align 4
.L410:
	.long	.L416-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L415-.L410
	.long	.L411-.L410
	.long	.L414-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L413-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L408-.L410
	.long	.L412-.L410
	.long	.L411-.L410
	.long	.L409-.L410
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L385:
	movzbl	52(%rsp), %edx
	andl	$3, %ecx
	addq	$1, %rax
	sall	$2, %ecx
	andl	$-13, %edx
	orl	%ecx, %edx
	cmpq	%rax, %rsi
	movb	%dl, 52(%rsp)
	je	.L374
	movzbl	1(%r9), %edx
	cmpb	$125, %dl
	je	.L374
	cmpb	$35, %dl
	movq	%rax, %r9
	je	.L386
	jmp	.L471
	.p2align 4,,10
	.p2align 3
.L375:
	leaq	52(%rsp), %rcx
	movq	%rbx, %r9
	movq	%rsi, %r8
	movq	%rax, %rdx
	call	_ZNSt8__format5_SpecIcE14_M_parse_widthEPKcS3_RSt26basic_format_parse_contextIcE
	cmpq	%rax, %rsi
	je	.L374
	movzbl	(%rax), %edx
	cmpb	$125, %dl
	je	.L374
	cmpb	$46, %dl
	je	.L391
	cmpb	$76, %dl
	je	.L430
.L419:
	subl	$65, %edx
	cmpb	$38, %dl
	ja	.L417
	leaq	.L418(%rip), %rcx
	movzbl	%dl, %edx
	movslq	(%rcx,%rdx,4), %rdx
	addq	%rcx, %rdx
	jmp	*%rdx
	.section .rdata,"dr"
	.align 4
.L418:
	.long	.L416-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L415-.L418
	.long	.L411-.L418
	.long	.L414-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L413-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L417-.L418
	.long	.L412-.L418
	.long	.L411-.L418
	.long	.L409-.L418
	.section	.text$_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE,"x"
	.linkonce discard
.L413:
	movzbl	53(%rsp), %edx
	addq	$1, %rax
	andl	$-121, %edx
	orl	$8, %edx
	movb	%dl, 53(%rsp)
	.p2align 4,,10
	.p2align 3
.L417:
	cmpq	%rax, %rsi
	je	.L374
.L408:
	cmpb	$125, (%rax)
	je	.L374
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L411:
	movzbl	53(%rsp), %edx
	addq	$1, %rax
	andl	$-121, %edx
	orl	$40, %edx
	movb	%dl, 53(%rsp)
	jmp	.L417
.L415:
	movzbl	53(%rsp), %edx
	addq	$1, %rax
	andl	$-121, %edx
	orl	$32, %edx
	movb	%dl, 53(%rsp)
	jmp	.L417
.L414:
	movzbl	53(%rsp), %edx
	addq	$1, %rax
	andl	$-121, %edx
	orl	$56, %edx
	movb	%dl, 53(%rsp)
	jmp	.L417
.L416:
	movzbl	53(%rsp), %edx
	addq	$1, %rax
	andl	$-121, %edx
	orl	$16, %edx
	movb	%dl, 53(%rsp)
	jmp	.L417
.L409:
	movzbl	53(%rsp), %edx
	addq	$1, %rax
	andl	$-121, %edx
	orl	$48, %edx
	movb	%dl, 53(%rsp)
	jmp	.L417
.L412:
	movzbl	53(%rsp), %edx
	addq	$1, %rax
	andl	$-121, %edx
	orl	$24, %edx
	movb	%dl, 53(%rsp)
	jmp	.L417
	.p2align 4,,10
	.p2align 3
.L473:
	orb	$64, 52(%rsp)
	addq	$1, %rax
	cmpq	%rax, %rsi
	je	.L374
	movzbl	1(%r9), %edx
	cmpb	$125, %dl
	je	.L374
	jmp	.L390
	.p2align 4,,10
	.p2align 3
.L422:
	movl	$3, %ecx
	jmp	.L377
	.p2align 4,,10
	.p2align 3
.L421:
	movl	$2, %ecx
	jmp	.L377
	.p2align 4,,10
	.p2align 3
.L432:
	movl	$3, %ecx
	jmp	.L380
	.p2align 4,,10
	.p2align 3
.L431:
	movl	$2, %ecx
	jmp	.L380
	.p2align 4,,10
	.p2align 3
.L430:
	orb	$32, 52(%rsp)
	movq	%rax, %rdx
	addq	$1, %rax
	cmpq	%rax, %rsi
	je	.L374
	movzbl	1(%rdx), %edx
	cmpb	$125, %dl
	je	.L374
	jmp	.L419
	.p2align 4,,10
	.p2align 3
.L393:
	cmpb	$123, %cl
	je	.L475
.L396:
	leaq	.LC11(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L475:
	leaq	2(%rax), %rdx
	cmpq	%rdx, %rsi
	je	.L476
	movzbl	2(%rax), %ecx
	cmpb	$125, %cl
	je	.L477
	cmpb	$48, %cl
	je	.L478
	leal	-49(%rcx), %r8d
	cmpb	$8, %r8b
	jbe	.L403
.L404:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L477:
	cmpl	$1, 16(%rbx)
	je	.L406
	movq	24(%rbx), %rax
	movl	$2, 16(%rbx)
	leaq	1(%rax), %rcx
	movw	%ax, 58(%rsp)
	movq	%rcx, 24(%rbx)
.L400:
	leaq	1(%rdx), %rax
	cmpq	%rax, %rbp
	je	.L396
	movl	$2, %ecx
	jmp	.L395
.L478:
	leaq	3(%rax), %rdx
	xorl	%eax, %eax
.L402:
	cmpq	%rdx, %rsi
	je	.L404
	testq	%rdx, %rdx
	je	.L404
.L420:
	cmpb	$125, (%rdx)
	jne	.L404
	cmpl	$2, 16(%rbx)
	je	.L406
	movl	$1, 16(%rbx)
	movw	%ax, 58(%rsp)
	jmp	.L400
.L403:
	leaq	3(%rax), %r8
	cmpq	%r8, %rsi
	je	.L404
	movzbl	3(%rax), %eax
	subl	$48, %eax
	cmpb	$9, %al
	ja	.L405
	leaq	32(%rsp), %rcx
	movq	%rsi, %r8
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzwl	32(%rsp), %eax
	movq	40(%rsp), %rdx
	jmp	.L402
.L405:
	movsbw	%cl, %ax
	movq	%r8, %rdx
	subl	$48, %eax
	jmp	.L420
.L474:
	leaq	.LC6(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
.L476:
	leaq	.LC3(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
.L406:
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
.LFB5114:
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$80, %rsp
	.seh_stackalloc	80
	.seh_endprologue
	movq	(%rdx), %rsi
	movq	8(%rdx), %rax
	movl	$0, 76(%rsp)
	movq	%rcx, %rdi
	movq	%rdx, %rbx
	cmpq	%rax, %rsi
	movb	$32, 76(%rsp)
	movq	$0, 68(%rsp)
	je	.L480
	movzbl	(%rsi), %ecx
	cmpb	$125, %cl
	je	.L522
	cmpb	$123, %cl
	je	.L481
	movq	%rax, %rdx
	subq	%rsi, %rdx
	cmpq	$1, %rdx
	jle	.L482
	movzbl	1(%rsi), %edx
	cmpb	$62, %dl
	je	.L523
	cmpb	$94, %dl
	je	.L524
	cmpb	$60, %dl
	movl	$1, %r8d
	jne	.L550
.L483:
	movb	%cl, 76(%rsp)
	addq	$2, %rsi
.L485:
	movzbl	68(%rsp), %edx
	andl	$-4, %edx
	orl	%r8d, %edx
	cmpq	%rsi, %rax
	movb	%dl, 68(%rsp)
	je	.L522
.L487:
	movzbl	(%rsi), %ecx
	cmpb	$125, %cl
	je	.L522
.L489:
	cmpb	$48, %cl
	je	.L551
	leaq	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE(%rip), %r8
	movzbl	%cl, %edx
	cmpb	$9, (%r8,%rdx)
	ja	.L491
	leaq	48(%rsp), %rcx
	movq	%rax, %r8
	movq	%rsi, %rdx
	movq	%rax, 40(%rsp)
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movq	56(%rsp), %rdx
	movq	48(%rsp), %rcx
	movq	40(%rsp), %rax
	testq	%rdx, %rdx
	je	.L510
	cmpq	%rdx, %rsi
	movw	%cx, 72(%rsp)
	movl	$1, %r8d
	je	.L494
.L493:
	movzwl	68(%rsp), %ecx
	andl	$3, %r8d
	sall	$7, %r8d
	andw	$-385, %cx
	orl	%r8d, %ecx
	movw	%cx, 68(%rsp)
.L494:
	cmpq	%rdx, %rax
	je	.L480
	movzbl	(%rdx), %ecx
	cmpb	$125, %cl
	je	.L534
.L495:
	cmpb	$46, %cl
	je	.L506
.L549:
	cmpb	$115, %cl
	je	.L552
.L508:
	call	_ZNSt8__format29__failed_to_parse_format_specEv
	.p2align 4,,10
	.p2align 3
.L522:
	movq	%rsi, %rax
.L480:
	movq	68(%rsp), %rdx
	movq	%rdx, (%rdi)
	movzbl	76(%rsp), %edx
	movb	%dl, 8(%rdi)
	addq	$80, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	ret
	.p2align 4,,10
	.p2align 3
.L482:
	cmpb	$62, %cl
	je	.L535
	cmpb	$94, %cl
	je	.L536
	cmpb	$60, %cl
	je	.L537
	jmp	.L489
	.p2align 4,,10
	.p2align 3
.L506:
	movzbl	1(%rdx), %r8d
	leaq	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE(%rip), %r9
	leaq	1(%rdx), %rsi
	cmpb	$9, (%r9,%r8)
	ja	.L509
	leaq	48(%rsp), %rcx
	movq	%rsi, %rdx
	movq	%rax, %r8
	movq	%rax, 40(%rsp)
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movq	56(%rsp), %rdx
	movq	48(%rsp), %rcx
	testq	%rdx, %rdx
	je	.L510
	cmpq	%rdx, %rsi
	movq	40(%rsp), %rax
	movw	%cx, 74(%rsp)
	je	.L512
	movl	$1, %r8d
.L511:
	movzbl	69(%rsp), %ecx
	addl	%r8d, %r8d
	andl	$-7, %ecx
	orl	%r8d, %ecx
	cmpq	%rdx, %rax
	movb	%cl, 69(%rsp)
	je	.L480
	movzbl	(%rdx), %ecx
	cmpb	$125, %cl
	jne	.L549
.L534:
	movq	%rdx, %rax
	jmp	.L480
.L491:
	cmpb	$123, %cl
	movq	%rsi, %rdx
	jne	.L495
	.p2align 4,,10
	.p2align 3
.L481:
	leaq	1(%rsi), %rdx
	cmpq	%rdx, %rax
	je	.L513
	movsbw	1(%rsi), %cx
	cmpb	$125, %cl
	je	.L553
	cmpb	$48, %cl
	je	.L554
	leal	-49(%rcx), %r8d
	cmpb	$8, %r8b
	jbe	.L502
.L503:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
	.p2align 4,,10
	.p2align 3
.L550:
	cmpb	$62, %cl
	je	.L535
	cmpb	$94, %cl
	je	.L536
	cmpb	$60, %cl
	jne	.L487
.L537:
	movl	$1, %r8d
.L486:
	addq	$1, %rsi
	jmp	.L485
	.p2align 4,,10
	.p2align 3
.L509:
	cmpb	$123, %r8b
	je	.L555
.L512:
	leaq	.LC11(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L524:
	movl	$3, %r8d
	jmp	.L483
	.p2align 4,,10
	.p2align 3
.L523:
	movl	$2, %r8d
	jmp	.L483
	.p2align 4,,10
	.p2align 3
.L535:
	movl	$2, %r8d
	jmp	.L486
	.p2align 4,,10
	.p2align 3
.L536:
	movl	$3, %r8d
	jmp	.L486
	.p2align 4,,10
	.p2align 3
.L552:
	leaq	1(%rdx), %rcx
	cmpq	%rax, %rcx
	je	.L480
	cmpb	$125, 1(%rdx)
	jne	.L508
	movq	%rcx, %rax
	jmp	.L480
	.p2align 4,,10
	.p2align 3
.L553:
	cmpl	$1, 16(%rbx)
	je	.L505
	movq	24(%rbx), %rcx
	movl	$2, 16(%rbx)
	leaq	1(%rcx), %r8
	movw	%cx, 72(%rsp)
	movq	%r8, 24(%rbx)
.L499:
	addq	$1, %rdx
	cmpq	%rdx, %rsi
	je	.L494
	movl	$2, %r8d
	jmp	.L493
.L554:
	leaq	2(%rsi), %rdx
	xorl	%ecx, %ecx
.L501:
	cmpq	%rdx, %rax
	je	.L503
	testq	%rdx, %rdx
	je	.L503
.L521:
	cmpb	$125, (%rdx)
	jne	.L503
	cmpl	$2, 16(%rbx)
	je	.L505
	movl	$1, 16(%rbx)
	movw	%cx, 72(%rsp)
	jmp	.L499
.L555:
	leaq	2(%rdx), %rcx
	cmpq	%rcx, %rax
	je	.L513
	movzbl	2(%rdx), %r8d
	cmpb	$125, %r8b
	je	.L556
	cmpb	$48, %r8b
	je	.L557
	leal	-49(%r8), %r9d
	cmpb	$8, %r9b
	ja	.L503
	leaq	3(%rdx), %r9
	cmpq	%r9, %rax
	je	.L503
	movzbl	3(%rdx), %edx
	subl	$48, %edx
	cmpb	$9, %dl
	ja	.L518
	leaq	48(%rsp), %r9
	movq	%rcx, %rdx
	movq	%rax, %r8
	movq	%rax, 40(%rsp)
	movq	%r9, %rcx
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzwl	48(%rsp), %edx
	movq	56(%rsp), %rcx
	movq	40(%rsp), %rax
.L517:
	testq	%rcx, %rcx
	je	.L503
	cmpq	%rcx, %rax
	je	.L503
.L520:
	cmpb	$125, (%rcx)
	jne	.L503
	cmpl	$2, 16(%rbx)
	je	.L505
	movl	$1, 16(%rbx)
	movw	%dx, 74(%rsp)
.L515:
	leaq	1(%rcx), %rdx
	cmpq	%rdx, %rsi
	je	.L512
	movl	$2, %r8d
	jmp	.L511
.L502:
	leaq	2(%rsi), %r9
	cmpq	%r9, %rax
	je	.L503
	movzbl	2(%rsi), %r10d
	leal	-48(%r10), %r8d
	cmpb	$9, %r8b
	ja	.L504
	leaq	48(%rsp), %rcx
	movq	%rax, %r8
	movq	%rax, 40(%rsp)
	call	_ZNSt8__format15__parse_integerIcEESt4pairItPKT_ES4_S4_
	movzwl	48(%rsp), %ecx
	movq	56(%rsp), %rdx
	movq	40(%rsp), %rax
	jmp	.L501
.L504:
	subl	$48, %ecx
	movq	%r9, %rdx
	jmp	.L521
.L556:
	cmpl	$1, 16(%rbx)
	je	.L505
	movq	24(%rbx), %rdx
	movl	$2, 16(%rbx)
	leaq	1(%rdx), %r8
	movw	%dx, 74(%rsp)
	movq	%r8, 24(%rbx)
	jmp	.L515
.L557:
	leaq	3(%rdx), %rcx
	xorl	%edx, %edx
	jmp	.L517
.L518:
	movsbw	%r8b, %dx
	movq	%r9, %rcx
	subl	$48, %edx
	jmp	.L520
.L551:
	leaq	.LC5(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
.L505:
	call	_ZNSt8__format39__conflicting_indexing_in_format_stringEv
.L510:
	leaq	.LC6(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
.L513:
	leaq	.LC3(%rip), %rcx
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
.LFB5221:
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$104, %rsp
	.seh_stackalloc	104
	movaps	%xmm6, 80(%rsp)
	.seh_savexmm	%xmm6, 80
	.seh_endprologue
	movdqu	(%rdx), %xmm6
	movl	192(%rsp), %edx
	cmpl	$3, %r8d
	movq	%rcx, %rbx
	movq	%r9, %rsi
	je	.L602
	cmpl	$2, %r8d
	je	.L580
	cmpq	$31, %r9
	ja	.L603
	testq	%r9, %r9
	jne	.L604
	leaq	32(%rsp), %rdx
	movaps	%xmm6, 32(%rsp)
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	movq	%rax, %rbx
	jmp	.L565
	.p2align 4,,10
	.p2align 3
.L580:
	movq	%r9, %rdi
	xorl	%r12d, %r12d
.L560:
	cmpq	$31, %rsi
	ja	.L581
	testq	%rsi, %rsi
	jne	.L566
	testq	%rdi, %rdi
	je	.L601
	leaq	48(%rsp), %r13
	jmp	.L568
	.p2align 4,,10
	.p2align 3
.L581:
	movl	$32, %esi
.L566:
	leaq	48(%rsp), %r13
	cmpl	$8, %esi
	movsbl	%dl, %ecx
	movl	%esi, %r8d
	movq	%r13, %rdx
	jnb	.L605
.L569:
	andl	$7, %r8d
	je	.L573
	xorl	%eax, %eax
.L572:
	movl	%eax, %r9d
	addl	$1, %eax
	cmpl	%r8d, %eax
	movb	%cl, (%rdx,%r9)
	jb	.L572
.L573:
	testq	%rdi, %rdi
	je	.L601
	leaq	32(%rsp), %rbp
	cmpq	%rdi, %rsi
	jnb	.L576
.L568:
	leaq	32(%rsp), %rbp
	.p2align 4,,10
	.p2align 3
.L577:
	movq	%rbx, %rcx
	movq	%rbp, %rdx
	subq	%rsi, %rdi
	movq	%rsi, 32(%rsp)
	movq	%r13, 40(%rsp)
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	cmpq	%rdi, %rsi
	movq	%rax, %rbx
	jb	.L577
	testq	%rdi, %rdi
	jne	.L576
.L575:
	movq	%rbx, %rcx
	movq	%rbp, %rdx
	movaps	%xmm6, 32(%rsp)
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	testq	%r12, %r12
	movq	%rax, %rbx
	je	.L565
.L562:
	leaq	48(%rsp), %r13
	cmpq	%r12, %rsi
	jnb	.L564
	.p2align 4,,10
	.p2align 3
.L578:
	movq	%rbx, %rcx
	movq	%rbp, %rdx
	subq	%rsi, %r12
	movq	%rsi, 32(%rsp)
	movq	%r13, 40(%rsp)
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	cmpq	%r12, %rsi
	movq	%rax, %rbx
	jb	.L578
	testq	%r12, %r12
	jne	.L564
.L565:
	movaps	80(%rsp), %xmm6
	movq	%rbx, %rax
	addq	$104, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L602:
	movq	%r9, %rdi
	andl	$1, %esi
	shrq	%rdi
	addq	%rdi, %rsi
	movq	%rsi, %r12
	jmp	.L560
	.p2align 4,,10
	.p2align 3
.L604:
	leaq	48(%rsp), %r13
	movsbl	%dl, %edx
	movq	%r9, %r8
	leaq	32(%rsp), %rbp
	movq	%r13, %rcx
	movq	%rsi, %r12
	call	memset
	movq	%rbx, %rcx
	movq	%rbp, %rdx
	movaps	%xmm6, 32(%rsp)
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	movq	%rax, %rbx
.L564:
	movq	%rbx, %rcx
	movq	%rbp, %rdx
	movq	%r12, 32(%rsp)
	movq	%r13, 40(%rsp)
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	movq	%rax, %rbx
	jmp	.L565
	.p2align 4,,10
	.p2align 3
.L576:
	movq	%rbx, %rcx
	movq	%rbp, %rdx
	movq	%rdi, 32(%rsp)
	movq	%r13, 40(%rsp)
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	movq	%rax, %rbx
	jmp	.L575
	.p2align 4,,10
	.p2align 3
.L605:
	movabsq	$72340172838076673, %rax
	movzbl	%cl, %r9d
	movl	%esi, %r10d
	imulq	%rax, %r9
	andl	$-8, %r10d
	xorl	%eax, %eax
.L570:
	movl	%eax, %edx
	addl	$8, %eax
	cmpl	%r10d, %eax
	movq	%r9, 0(%r13,%rdx)
	jb	.L570
	leaq	0(%r13,%rax), %rdx
	jmp	.L569
	.p2align 4,,10
	.p2align 3
.L603:
	leaq	32(%rsp), %rbp
	movzbl	%dl, %edx
	movaps	%xmm6, 32(%rsp)
	movq	%rsi, %r12
	movabsq	$72340172838076673, %rax
	movl	$32, %esi
	imulq	%rax, %rdx
	movq	%rdx, 48(%rsp)
	movq	%rdx, 56(%rsp)
	movq	%rdx, 64(%rsp)
	movq	%rdx, 72(%rsp)
	movq	%rbp, %rdx
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	movq	%rax, %rbx
	jmp	.L562
.L601:
	leaq	32(%rsp), %rbp
	jmp	.L575
	.seh_endproc
	.section	.text$_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	.def	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_:
.LFB5306:
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	.seh_endprologue
	movsbq	(%r8), %rax
	leal	-1(%rax), %ebx
	movq	%rcx, %r10
	movl	%edx, %r11d
	movq	96(%rsp), %rcx
	cmpb	$125, %bl
	movq	88(%rsp), %rdx
	ja	.L607
	movq	%rcx, %rbx
	subq	%rdx, %rbx
	cmpq	%rax, %rbx
	jle	.L607
	leaq	-1(%r9), %rbx
	xorl	%r12d, %r12d
	xorl	%esi, %esi
	jmp	.L610
	.p2align 4,,10
	.p2align 3
.L649:
	addq	$1, %rsi
.L609:
	leaq	(%r8,%rsi), %rbp
	movsbq	0(%rbp), %rax
	leal	-1(%rax), %r9d
	cmpb	$125, %r9b
	ja	.L627
	movq	%rcx, %r9
	subq	%rdx, %r9
	cmpq	%rax, %r9
	jle	.L627
.L610:
	subq	%rax, %rcx
	cmpq	%rbx, %rsi
	jb	.L649
	addq	$1, %r12
	jmp	.L609
	.p2align 4,,10
	.p2align 3
.L627:
	leaq	-1(%r12), %rdi
	cmpq	%rcx, %rdx
	leaq	-1(%rsi), %rbx
	je	.L650
.L622:
	movq	%rcx, %r13
	xorl	%eax, %eax
	subq	%rdx, %r13
	.p2align 4,,10
	.p2align 3
.L613:
	movzbl	(%rdx,%rax), %r9d
	movb	%r9b, (%r10,%rax)
	addq	$1, %rax
	cmpq	%r13, %rax
	jne	.L613
	leaq	(%r10,%rax), %rdx
.L612:
	testq	%r12, %r12
	je	.L614
	.p2align 4,,10
	.p2align 3
.L617:
	movb	%r11b, (%rdx)
	movzbl	0(%rbp), %r10d
	leaq	1(%rdx), %r12
	testb	%r10b, %r10b
	jle	.L624
	xorl	%eax, %eax
	.p2align 4,,10
	.p2align 3
.L616:
	movzbl	(%rcx,%rax), %r9d
	movb	%r9b, 1(%rdx,%rax)
	addq	$1, %rax
	cmpq	%r10, %rax
	jne	.L616
	leaq	(%r12,%rax), %rdx
	addq	%rax, %rcx
.L615:
	subq	$1, %rdi
	jnb	.L617
.L614:
	testq	%rsi, %rsi
	je	.L606
	.p2align 4,,10
	.p2align 3
.L621:
	movb	%r11b, (%rdx)
	movzbl	(%r8,%rbx), %r10d
	leaq	1(%rdx), %rsi
	testb	%r10b, %r10b
	jle	.L625
	xorl	%eax, %eax
	.p2align 4,,10
	.p2align 3
.L620:
	movzbl	(%rcx,%rax), %r9d
	movb	%r9b, 1(%rdx,%rax)
	addq	$1, %rax
	cmpq	%rax, %r10
	jne	.L620
	leaq	(%rsi,%r10), %rdx
	addq	%r10, %rcx
.L619:
	subq	$1, %rbx
	jnb	.L621
.L606:
	movq	%rdx, %rax
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L625:
	movq	%rsi, %rdx
	jmp	.L619
	.p2align 4,,10
	.p2align 3
.L624:
	movq	%r12, %rdx
	jmp	.L615
.L607:
	cmpq	%rdx, %rcx
	je	.L651
	movq	%r8, %rbp
	movq	$-1, %rbx
	movq	$-1, %rdi
	xorl	%r12d, %r12d
	xorl	%esi, %esi
	jmp	.L622
.L650:
	movq	%r10, %rdx
	jmp	.L612
.L651:
	movq	%r10, %rdx
	jmp	.L606
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC12:
	.ascii "format error: argument used for width or precision must be a non-negative integer\0"
	.section	.text$_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
	.def	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E:
.LFB5307:
	subq	$72, %rsp
	.seh_stackalloc	72
	.seh_endprologue
	leaq	.L655(%rip), %rdx
	movq	(%rcx), %rax
	movq	%rax, 32(%rsp)
	movzbl	16(%rcx), %eax
	movslq	(%rdx,%rax,4), %rax
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L655:
	.long	.L660-.L655
	.long	.L661-.L655
	.long	.L661-.L655
	.long	.L659-.L655
	.long	.L658-.L655
	.long	.L657-.L655
	.long	.L656-.L655
	.long	.L661-.L655
	.long	.L661-.L655
	.long	.L661-.L655
	.long	.L661-.L655
	.long	.L661-.L655
	.long	.L661-.L655
	.long	.L661-.L655
	.long	.L661-.L655
	.long	.L661-.L655
	.section	.text$_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L657:
	movq	32(%rsp), %rax
	testq	%rax, %rax
	js	.L661
.L652:
	addq	$72, %rsp
	ret
	.p2align 4,,10
	.p2align 3
.L658:
	movl	32(%rsp), %eax
	addq	$72, %rsp
	ret
	.p2align 4,,10
	.p2align 3
.L659:
	movslq	32(%rsp), %rax
	testl	%eax, %eax
	jns	.L652
.L661:
	leaq	.LC12(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
	.p2align 4,,10
	.p2align 3
.L656:
	movq	32(%rsp), %rax
	addq	$72, %rsp
	ret
.L660:
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
.LFB5118:
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$112, %rsp
	.seh_stackalloc	112
	movaps	%xmm6, 96(%rsp)
	.seh_savexmm	%xmm6, 96
	.seh_endprologue
	movzwl	(%r9), %eax
	movdqu	(%rcx), %xmm6
	andw	$384, %ax
	movq	%r8, %rsi
	movq	%rdx, %rdi
	movl	176(%rsp), %r8d
	cmpw	$128, %ax
	movq	%r9, %rbx
	je	.L674
	cmpw	$256, %ax
	je	.L666
.L670:
	movq	16(%rsi), %rcx
	leaq	48(%rsp), %rdx
	movaps	%xmm6, 48(%rsp)
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	nop
	movaps	96(%rsp), %xmm6
	addq	$112, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	ret
	.p2align 4,,10
	.p2align 3
.L674:
	movzwl	4(%r9), %r9d
.L665:
	cmpq	%r9, %rdi
	jnb	.L670
	movzbl	(%rbx), %edx
	movq	16(%rsi), %rcx
	movl	%edx, %eax
	andl	$3, %eax
	andl	$3, %edx
	cmovne	%eax, %r8d
	movsbl	8(%rbx), %eax
	subq	%rdi, %r9
	movaps	%xmm6, 48(%rsp)
	leaq	48(%rsp), %rdx
	movl	%eax, 32(%rsp)
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
	nop
	movaps	96(%rsp), %xmm6
	addq	$112, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	ret
	.p2align 4,,10
	.p2align 3
.L666:
	movzbl	(%rsi), %edx
	movb	$0, 80(%rsp)
	movzwl	4(%r9), %eax
	movl	%edx, %ecx
	andl	$15, %edx
	andl	$15, %ecx
	cmpq	%rdx, %rax
	jb	.L675
	testb	%cl, %cl
	jne	.L669
	movq	(%rsi), %rdx
	shrq	$4, %rdx
	cmpq	%rdx, %rax
	jnb	.L669
	salq	$5, %rax
	addq	8(%rsi), %rax
	movq	(%rax), %rdx
	movq	%rdx, 64(%rsp)
	movq	8(%rax), %rdx
	movzbl	16(%rax), %eax
	movq	%rdx, 72(%rsp)
	movb	%al, 80(%rsp)
	.p2align 4,,10
	.p2align 3
.L669:
	leaq	64(%rsp), %rcx
	movl	%r8d, 176(%rsp)
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
	movl	176(%rsp), %r8d
	movq	%rax, %r9
	jmp	.L665
	.p2align 4,,10
	.p2align 3
.L675:
	movq	(%rsi), %rdx
	leaq	(%rax,%rax,4), %rcx
	salq	$4, %rax
	addq	8(%rsi), %rax
	shrq	$4, %rdx
	shrq	%cl, %rdx
	andl	$31, %edx
	movb	%dl, 80(%rsp)
	movq	(%rax), %rdx
	movq	8(%rax), %rax
	movq	%rdx, 64(%rsp)
	movq	%rax, 72(%rsp)
	jmp	.L669
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
	.def	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE:
.LFB5117:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$104, %rsp
	.seh_stackalloc	104
	.seh_endprologue
	movq	(%rdx), %rbx
	testw	$1920, (%rcx)
	movq	8(%rdx), %rsi
	movzbl	1(%rcx), %edx
	movq	%rcx, %r9
	movq	%rbx, %rax
	je	.L687
	andl	$6, %edx
	jne	.L688
.L679:
	leaq	48(%rsp), %rcx
	movl	$1, 32(%rsp)
	movq	%rax, %rdx
	movq	%rax, 48(%rsp)
	movq	%rsi, 56(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	addq	$104, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.p2align 4,,10
	.p2align 3
.L688:
	cmpb	$2, %dl
	je	.L689
	cmpb	$4, %dl
	jne	.L679
	movzbl	(%r8), %edx
	movb	$0, 80(%rsp)
	movzwl	6(%rcx), %eax
	movl	%edx, %ecx
	andl	$15, %edx
	andl	$15, %ecx
	cmpq	%rdx, %rax
	jb	.L690
	testb	%cl, %cl
	jne	.L683
	movq	(%r8), %rdx
	shrq	$4, %rdx
	cmpq	%rdx, %rax
	jnb	.L683
	salq	$5, %rax
	addq	8(%r8), %rax
	movq	(%rax), %rdx
	movq	%rdx, 64(%rsp)
	movq	8(%rax), %rdx
	movzbl	16(%rax), %eax
	movq	%rdx, 72(%rsp)
	movb	%al, 80(%rsp)
	.p2align 4,,10
	.p2align 3
.L683:
	leaq	64(%rsp), %rcx
	movq	%r8, 144(%rsp)
	movq	%r9, 128(%rsp)
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
	movq	144(%rsp), %r8
	movq	128(%rsp), %r9
	jmp	.L681
	.p2align 4,,10
	.p2align 3
.L687:
	movq	16(%r8), %rcx
	leaq	48(%rsp), %rdx
	movq	%rbx, 48(%rsp)
	movq	%rsi, 56(%rsp)
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
	addq	$104, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.p2align 4,,10
	.p2align 3
.L689:
	movzwl	6(%rcx), %eax
.L681:
	cmpq	%rax, %rbx
	cmovbe	%rbx, %rax
	jmp	.L679
	.p2align 4,,10
	.p2align 3
.L690:
	movq	(%r8), %rdx
	leaq	(%rax,%rax,4), %rcx
	salq	$4, %rax
	addq	8(%r8), %rax
	shrq	$4, %rdx
	shrq	%cl, %rdx
	andl	$31, %edx
	movb	%dl, 80(%rsp)
	movq	(%rax), %rdx
	movq	8(%rax), %rax
	movq	%rdx, 64(%rsp)
	movq	%rax, 72(%rsp)
	jmp	.L683
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	.def	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_:
.LFB5205:
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$168, %rsp
	.seh_stackalloc	168
	leaq	160(%rsp), %rbp
	.seh_setframe	%rbp, 160
	.seh_endprologue
	movzwl	(%rcx), %eax
	movq	(%rdx), %r15
	movq	8(%rdx), %r14
	andw	$384, %ax
	movq	%rcx, %rbx
	movq	%r8, %rdi
	cmpw	$128, %ax
	movq	%r9, %rsi
	movq	%r15, %r12
	movq	%r14, %r13
	je	.L743
	cmpw	$256, %ax
	je	.L744
	testb	$32, (%rcx)
	movq	$0, -48(%rbp)
	movb	$0, -40(%rbp)
	jne	.L725
	movq	16(%r9), %rcx
.L722:
	leaq	-64(%rbp), %rdx
	movq	%r12, -64(%rbp)
	movq	%r13, -56(%rbp)
.LEHB8:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L714:
	cmpb	$0, -40(%rbp)
	jne	.L745
.L731:
	leaq	8(%rbp), %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	ret
	.p2align 4,,10
	.p2align 3
.L743:
	movzwl	4(%rcx), %eax
	movq	%rax, -72(%rbp)
.L693:
	testb	$32, (%rbx)
	movq	$0, -48(%rbp)
	movb	$0, -40(%rbp)
	jne	.L721
.L697:
	movq	-72(%rbp), %rax
	movq	16(%rsi), %rcx
	cmpq	%rax, %r12
	jnb	.L722
	movzbl	(%rbx), %edx
	movq	%rcx, %rax
	movzbl	8(%rbx), %r9d
	movq	-72(%rbp), %rbx
	movl	%edx, %r8d
	subq	%r12, %rbx
	andl	$3, %r8d
	jne	.L746
	andl	$64, %edx
	je	.L723
	testq	%rdi, %rdi
	jne	.L747
	leaq	-64(%rbp), %rsi
	movl	$48, %edx
	movl	$2, %r8d
	jmp	.L716
	.p2align 4,,10
	.p2align 3
.L745:
	leaq	-48(%rbp), %rcx
	movq	%rax, -72(%rbp)
	call	_ZNSt6localeD1Ev
	movq	-72(%rbp), %rax
	jmp	.L731
	.p2align 4,,10
	.p2align 3
.L725:
	movq	$0, -72(%rbp)
.L721:
	cmpb	$0, 32(%rsi)
	leaq	24(%rsi), %rdx
	je	.L748
.L698:
	leaq	-32(%rbp), %rax
	movq	%rax, %rcx
	movq	%rax, -80(%rbp)
	call	_ZNSt6localeC1ERKS_
	cmpb	$0, -40(%rbp)
	jne	.L749
	movq	-80(%rbp), %rdx
	leaq	-48(%rbp), %rax
	movq	%rax, %rcx
	movq	%rax, -88(%rbp)
	call	_ZNSt6localeC1ERKS_
	movq	-80(%rbp), %rcx
	movb	$1, -40(%rbp)
	call	_ZNSt6localeD1Ev
	cmpb	$0, -40(%rbp)
	je	.L750
.L701:
	movq	-88(%rbp), %rdx
	movq	-80(%rbp), %rcx
	call	_ZNKSt6locale4nameB5cxx11Ev
	cmpq	$1, -24(%rbp)
	leaq	-16(%rbp), %rax
	movq	-32(%rbp), %rcx
	je	.L751
.L703:
	cmpq	%rax, %rcx
	movq	%rax, -88(%rbp)
	je	.L706
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L706:
	movq	.refptr._ZNSt7__cxx118numpunctIcE2idE(%rip), %rcx
	call	_ZNKSt6locale2id5_M_idEv
	movq	%rax, %rdx
	movq	-48(%rbp), %rax
	movq	8(%rax), %rax
	movq	(%rax,%rdx,8), %rdx
	testq	%rdx, %rdx
	movq	%rdx, -104(%rbp)
	je	.L708
	movq	(%rdx), %rax
	movq	-80(%rbp), %rcx
	call	*32(%rax)
.LEHE8:
	movq	-24(%rbp), %rax
	testq	%rax, %rax
	movq	%rax, -96(%rbp)
	je	.L710
	movq	%r15, %rax
	subq	%rdi, %rax
	leaq	15(%rdi,%rax,2), %rax
	andq	$-16, %rax
	call	___chkstk_ms
	subq	%rax, %rsp
	testq	%rdi, %rdi
	leaq	48(%rsp), %r13
	jne	.L752
.L711:
	movq	-104(%rbp), %rcx
	leaq	(%r14,%rdi), %r12
	addq	%r15, %r14
	movq	-32(%rbp), %r15
	movq	(%rcx), %rax
.LEHB9:
	call	*24(%rax)
.LEHE9:
	movq	%r12, 32(%rsp)
	leaq	0(%r13,%rdi), %rcx
	movsbl	%al, %edx
	movq	%r15, %r8
	movq	%r14, 40(%rsp)
	movq	-96(%rbp), %r9
	call	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	subq	%r13, %rax
	movq	%rax, %r12
.L710:
	movq	-32(%rbp), %rcx
	movq	-88(%rbp), %rax
.L742:
	cmpq	%rax, %rcx
	je	.L697
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	jmp	.L697
	.p2align 4,,10
	.p2align 3
.L723:
	leaq	-64(%rbp), %rsi
	movl	$32, %edx
	movl	$2, %r8d
.L716:
	movq	%r12, -64(%rbp)
	movq	%rbx, %r9
	movq	%rax, %rcx
	movq	%r13, -56(%rbp)
	movl	%edx, 32(%rsp)
	movq	%rsi, %rdx
.LEHB10:
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
	jmp	.L714
	.p2align 4,,10
	.p2align 3
.L746:
	leaq	-64(%rbp), %rsi
	movsbl	%r9b, %edx
	jmp	.L716
	.p2align 4,,10
	.p2align 3
.L749:
	leaq	-48(%rbp), %rdx
	movq	%rdx, %r10
	movq	%rdx, -88(%rbp)
	movq	-80(%rbp), %rdx
	movq	%r10, %rcx
	call	_ZNSt6localeaSERKS_
	movq	-80(%rbp), %rcx
	call	_ZNSt6localeD1Ev
	cmpb	$0, -40(%rbp)
	jne	.L701
.L750:
	movq	-88(%rbp), %rcx
	call	_ZNSt6localeC1Ev
	movb	$1, -40(%rbp)
	jmp	.L701
	.p2align 4,,10
	.p2align 3
.L747:
	leaq	-64(%rbp), %rsi
	cmpq	%r12, %rdi
	movq	%r12, %rax
	movq	%r13, -56(%rbp)
	cmovbe	%rdi, %rax
	movq	%rsi, %rdx
	movq	%rax, -64(%rbp)
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.LEHE10:
	addq	%rdi, %r13
	subq	%rdi, %r12
	movl	$48, %edx
	movl	$2, %r8d
	jmp	.L716
	.p2align 4,,10
	.p2align 3
.L744:
	movzbl	(%r9), %edx
	movb	$0, -16(%rbp)
	movzwl	4(%rcx), %eax
	movl	%edx, %ecx
	andl	$15, %edx
	andl	$15, %ecx
	cmpq	%rdx, %rax
	jb	.L753
	testb	%cl, %cl
	jne	.L696
	movq	(%r9), %rdx
	shrq	$4, %rdx
	cmpq	%rdx, %rax
	jnb	.L696
	salq	$5, %rax
	addq	8(%r9), %rax
	movq	(%rax), %rdx
	movq	%rdx, -32(%rbp)
	movq	8(%rax), %rdx
	movq	%rdx, -24(%rbp)
	movzbl	16(%rax), %eax
	movb	%al, -16(%rbp)
	.p2align 4,,10
	.p2align 3
.L696:
	leaq	-32(%rbp), %rcx
.LEHB11:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE11:
	movq	%rax, -72(%rbp)
	jmp	.L693
	.p2align 4,,10
	.p2align 3
.L751:
	cmpb	$67, (%rcx)
	jne	.L703
	jmp	.L742
	.p2align 4,,10
	.p2align 3
.L748:
	movq	%rdx, %rcx
	movq	%rdx, -80(%rbp)
	call	_ZNSt6localeC1Ev
	movq	-80(%rbp), %rdx
	movb	$1, 32(%rsi)
	jmp	.L698
	.p2align 4,,10
	.p2align 3
.L752:
	movq	%rdi, %r8
	movq	%r14, %rdx
	movq	%r13, %rcx
	call	memcpy
	jmp	.L711
	.p2align 4,,10
	.p2align 3
.L753:
	movq	(%r9), %rdx
	leaq	(%rax,%rax,4), %rcx
	salq	$4, %rax
	addq	8(%r9), %rax
	shrq	$4, %rdx
	shrq	%cl, %rdx
	andl	$31, %edx
	movb	%dl, -16(%rbp)
	movq	(%rax), %rdx
	movq	%rdx, -32(%rbp)
	movq	8(%rax), %rax
	movq	%rax, -24(%rbp)
	jmp	.L696
.L708:
.LEHB12:
	call	_ZSt16__throw_bad_castv
.LEHE12:
.L727:
	movq	-80(%rbp), %rcx
	movq	%rax, %rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L719:
	cmpb	$0, -40(%rbp)
	je	.L720
	leaq	-48(%rbp), %rcx
	call	_ZNSt6localeD1Ev
.L720:
	movq	%rbx, %rcx
.LEHB13:
	call	_Unwind_Resume
.LEHE13:
.L726:
	movq	%rax, %rbx
	jmp	.L719
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5205:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5205-.LLSDACSB5205
.LLSDACSB5205:
	.uleb128 .LEHB8-.LFB5205
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L726-.LFB5205
	.uleb128 0
	.uleb128 .LEHB9-.LFB5205
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L727-.LFB5205
	.uleb128 0
	.uleb128 .LEHB10-.LFB5205
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L726-.LFB5205
	.uleb128 0
	.uleb128 .LEHB11-.LFB5205
	.uleb128 .LEHE11-.LEHB11
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB12-.LFB5205
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L726-.LFB5205
	.uleb128 0
	.uleb128 .LEHB13-.LFB5205
	.uleb128 .LEHE13-.LEHB13
	.uleb128 0
	.uleb128 0
.LLSDACSE5205:
	.section	.text$_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC13:
	.ascii "0b\0"
.LC14:
	.ascii "0B\0"
.LC15:
	.ascii "0\0"
.LC16:
	.ascii "0X\0"
.LC17:
	.ascii "0x\0"
	.align 8
.LC18:
	.ascii "format error: integer not representable as character\0"
	.align 8
.LC19:
	.ascii "00010203040506070809101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899\0"
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5194:
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$296, %rsp
	.seh_stackalloc	296
	.seh_endprologue
	movl	%edx, %eax
	movq	%r8, %rsi
	movl	%edx, %r8d
	movzbl	1(%rcx), %edx
	movq	%rcx, %rbx
	movl	%edx, %ecx
	andl	$120, %ecx
	cmpb	$56, %cl
	je	.L814
	shrb	$3, %dl
	andl	$15, %edx
	cmpb	$4, %dl
	je	.L758
	ja	.L759
	cmpb	$1, %dl
	jbe	.L760
	leaq	.LC13(%rip), %rbp
	cmpb	$16, %cl
	leaq	.LC14(%rip), %rdx
	cmovne	%rdx, %rbp
	testb	%al, %al
	jne	.L815
	leaq	72(%rsp), %r12
	movl	$48, %eax
	leaq	71(%rsp), %r13
.L765:
	movb	%al, 71(%rsp)
	movzbl	(%rbx), %eax
	testb	$16, %al
	je	.L801
.L800:
	movq	$-2, %rdx
	movl	$2, %ecx
.L769:
	addq	%r13, %rdx
	testl	%ecx, %ecx
	movl	%ecx, %r10d
	je	.L770
	xorl	%ecx, %ecx
.L787:
	movl	%ecx, %r8d
	addl	$1, %ecx
	movzbl	0(%rbp,%r8), %r9d
	cmpl	%r10d, %ecx
	movb	%r9b, (%rdx,%r8)
	jb	.L787
	jmp	.L770
	.p2align 4,,10
	.p2align 3
.L814:
	testb	%al, %al
	js	.L756
	movb	%al, 80(%rsp)
	leaq	48(%rsp), %rcx
	movq	%rbx, %r9
	movq	%rsi, %r8
	leaq	80(%rsp), %rax
	movl	$1, %edx
	movl	$1, 32(%rsp)
	movq	$1, 48(%rsp)
	movq	%rax, 56(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	addq	$296, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L760:
	testb	%al, %al
	movzbl	%al, %edi
	jne	.L771
	movb	$48, 71(%rsp)
	leaq	72(%rsp), %r12
	leaq	71(%rsp), %r13
.L772:
	movzbl	(%rbx), %eax
	movq	%r13, %rdx
.L770:
	shrb	$2, %al
	andl	$3, %eax
	cmpl	$1, %eax
	je	.L816
.L789:
	cmpl	$3, %eax
	je	.L802
.L790:
	movq	%r12, %rax
	movq	%r13, %r8
	movq	%rdx, 56(%rsp)
	movq	%rsi, %r9
	subq	%rdx, %rax
	subq	%rdx, %r8
	movq	%rbx, %rcx
	movq	%rax, 48(%rsp)
	leaq	48(%rsp), %rax
	movq	%rax, %rdx
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	addq	$296, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L758:
	testb	%al, %al
	je	.L795
	movzbl	%al, %edx
	bsrl	%edx, %ecx
	leal	3(%rcx), %r12d
	movl	$2863311531, %ecx
	imulq	%rcx, %r12
	shrq	$33, %r12
	cmpl	$63, %edx
	jbe	.L777
	andl	$7, %eax
	addl	$48, %eax
	movb	%al, 73(%rsp)
	movl	%edx, %eax
	shrl	$6, %edx
	shrl	$3, %eax
	andl	$7, %eax
	addl	$48, %eax
	movb	%al, 72(%rsp)
.L778:
	addl	$48, %edx
.L779:
	leaq	71(%rsp), %r13
	movl	%r12d, %r12d
	movl	$1, %r8d
	leaq	.LC15(%rip), %rbp
	addq	%r13, %r12
	movl	$1, %ecx
.L776:
	movb	%dl, 71(%rsp)
.L780:
	movzbl	(%rbx), %eax
	testb	$16, %al
	je	.L801
	movq	%rcx, %rdx
	negq	%rdx
	testb	%r8b, %r8b
	jne	.L769
.L801:
	shrb	$2, %al
	movq	%r13, %rdx
	andl	$3, %eax
	cmpl	$1, %eax
	jne	.L789
.L816:
	movl	$43, %eax
.L791:
	movb	%al, -1(%rdx)
	subq	$1, %rdx
	jmp	.L790
	.p2align 4,,10
	.p2align 3
.L771:
	cmpl	$9, %edi
	jbe	.L794
	leaq	80(%rsp), %rcx
	cmpl	$99, %edi
	movl	$201, %r8d
	leaq	.LC19(%rip), %rdx
	jbe	.L817
	call	memcpy
	movl	%edi, %r8d
	imulq	$1374389535, %r8, %r8
	shrq	$37, %r8
	imull	$100, %r8d, %eax
	subl	%eax, %edi
	leal	1(%rdi,%rdi), %eax
	movzwl	79(%rsp,%rax), %eax
	movw	%ax, 72(%rsp)
	movl	$3, %eax
.L773:
	addl	$48, %r8d
.L775:
	leaq	71(%rsp), %r13
	movb	%r8b, 71(%rsp)
	leaq	0(%r13,%rax), %r12
	jmp	.L772
	.p2align 4,,10
	.p2align 3
.L759:
	cmpb	$40, %cl
	je	.L818
	testb	%al, %al
	jne	.L797
	movb	$48, 71(%rsp)
	leaq	.LC16(%rip), %rbp
	cmpb	$48, %cl
	leaq	72(%rsp), %r12
	leaq	71(%rsp), %r13
	je	.L783
.L782:
	movzbl	(%rbx), %eax
	testb	$16, %al
	jne	.L800
	jmp	.L801
	.p2align 4,,10
	.p2align 3
.L783:
	movq	%r13, %rdi
	.p2align 4,,10
	.p2align 3
.L786:
	movsbl	(%rdi), %ecx
	addq	$1, %rdi
	call	toupper
	movb	%al, -1(%rdi)
	cmpq	%r12, %rdi
	jne	.L786
	movl	$1, %r8d
	movl	$2, %ecx
	jmp	.L780
	.p2align 4,,10
	.p2align 3
.L802:
	movl	$32, %eax
	jmp	.L791
	.p2align 4,,10
	.p2align 3
.L795:
	movl	$48, %edx
	xorl	%r8d, %r8d
	xorl	%ecx, %ecx
	leaq	72(%rsp), %r12
	xorl	%ebp, %ebp
	leaq	71(%rsp), %r13
	jmp	.L776
	.p2align 4,,10
	.p2align 3
.L815:
	movzbl	%al, %eax
	movl	$32, %r12d
	movl	$31, %edx
	bsrl	%eax, %r9d
	xorl	$31, %r9d
	subl	%r9d, %r12d
	subl	%r9d, %edx
	je	.L768
	movl	%edx, %ecx
	leaq	70(%rsp,%rcx), %r8
	leaq	71(%rsp,%rcx), %rdx
	movl	$30, %ecx
	subl	%r9d, %ecx
	subq	%rcx, %r8
	.p2align 4,,10
	.p2align 3
.L767:
	movl	%eax, %ecx
	subq	$1, %rdx
	shrl	%eax
	andl	$1, %ecx
	addl	$48, %ecx
	movb	%cl, 1(%rdx)
	cmpq	%r8, %rdx
	jne	.L767
.L768:
	leaq	71(%rsp), %r13
	movslq	%r12d, %r12
	movl	$49, %eax
	addq	%r13, %r12
	jmp	.L765
	.p2align 4,,10
	.p2align 3
.L818:
	testb	%al, %al
	jne	.L796
	movb	$48, 71(%rsp)
	leaq	.LC17(%rip), %rbp
	leaq	72(%rsp), %r12
	leaq	71(%rsp), %r13
	jmp	.L782
	.p2align 4,,10
	.p2align 3
.L797:
	leaq	.LC16(%rip), %rbp
.L781:
	movabsq	$3978425819141910832, %rdi
	movzbl	%al, %edx
	bsrl	%edx, %r8d
	movq	%rdi, 80(%rsp)
	movabsq	$7378413942531504440, %rdi
	addl	$4, %r8d
	movq	%rdi, 88(%rsp)
	shrl	$2, %r8d
	cmpl	$15, %edx
	ja	.L819
	movzbl	80(%rsp,%rdx), %eax
.L785:
	movb	%al, 71(%rsp)
	leaq	71(%rsp), %r13
	movl	%r8d, %eax
	cmpb	$48, %cl
	leaq	0(%r13,%rax), %r12
	jne	.L782
	testl	%r8d, %r8d
	jne	.L783
	movl	$1, %r8d
	movl	$2, %ecx
	movq	%r13, %r12
	jmp	.L780
	.p2align 4,,10
	.p2align 3
.L819:
	andl	$15, %eax
	shrl	$4, %edx
	movzbl	80(%rsp,%rax), %eax
	movb	%al, 72(%rsp)
	movzbl	80(%rsp,%rdx), %eax
	jmp	.L785
	.p2align 4,,10
	.p2align 3
.L796:
	leaq	.LC17(%rip), %rbp
	jmp	.L781
	.p2align 4,,10
	.p2align 3
.L817:
	call	memcpy
	addl	%edi, %edi
	leal	1(%rdi), %eax
	movzbl	80(%rsp,%rdi), %r8d
	movzbl	80(%rsp,%rax), %eax
	movb	%al, 72(%rsp)
	movl	$2, %eax
	jmp	.L775
	.p2align 4,,10
	.p2align 3
.L794:
	movl	$1, %eax
	jmp	.L773
.L777:
	cmpl	$7, %edx
	jbe	.L778
	andl	$7, %eax
	shrl	$3, %edx
	addl	$48, %eax
	addl	$48, %edx
	movb	%al, 72(%rsp)
	jmp	.L779
.L756:
	leaq	.LC18(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC20:
	.ascii "true\0"
.LC21:
	.ascii "false\0"
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_:
.LFB5088:
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$136, %rsp
	.seh_stackalloc	136
	.seh_endprologue
	movzbl	1(%rcx), %eax
	andl	$120, %eax
	movq	%rcx, %rbx
	movl	%edx, %esi
	cmpb	$56, %al
	movq	%r8, %rdi
	je	.L869
	testb	%al, %al
	jne	.L870
	testb	$32, (%rcx)
	leaq	80(%rsp), %rbp
	movb	$0, 80(%rsp)
	movq	%rbp, 64(%rsp)
	movq	$0, 72(%rsp)
	jne	.L871
	leaq	64(%rsp), %rsi
	movl	%edx, %eax
	negb	%al
	leaq	.LC20(%rip), %rax
	sbbq	%r12, %r12
	addq	$5, %r12
	testb	%dl, %dl
	leaq	.LC21(%rip), %rdx
	cmove	%rdx, %rax
	cmpq	%rbp, %rax
	je	.L841
	xorl	%edx, %edx
	testb	$4, %r12b
	movl	%r12d, %ecx
	jne	.L872
	testb	$2, %cl
	jne	.L873
.L843:
	andl	$1, %ecx
	jne	.L874
.L844:
	movq	%rbp, %rax
.L845:
	movq	%r12, 72(%rsp)
	movb	$0, (%rax,%r12)
.L868:
	movq	72(%rsp), %rdx
	leaq	48(%rsp), %rcx
	movq	%rbx, %r9
	movq	%rdi, %r8
	movq	64(%rsp), %rax
	movl	$1, 32(%rsp)
	leaq	64(%rsp), %rsi
	movq	%rdx, 48(%rsp)
	movq	%rax, 56(%rsp)
.LEHB14:
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.LEHE14:
	movq	64(%rsp), %rcx
	movq	%rax, %rbx
	cmpq	%rbp, %rcx
	je	.L856
	movq	80(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L856:
	movq	%rbx, %rax
	addq	$136, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L870:
	movzbl	%dl, %edx
	addq	$136, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
.LEHB15:
	jmp	_ZNKSt8__format15__formatter_intIcE6formatIhNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.p2align 4,,10
	.p2align 3
.L869:
	movb	%dl, 96(%rsp)
	leaq	96(%rsp), %rax
	movq	%rbx, %r9
	movl	$1, %edx
	leaq	48(%rsp), %rcx
	movl	$1, 32(%rsp)
	movq	$1, 48(%rsp)
	movq	%rax, 56(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.LEHE15:
	movq	%rax, %rbx
	jmp	.L856
	.p2align 4,,10
	.p2align 3
.L874:
	movzbl	(%rax,%rdx), %eax
	movb	%al, 80(%rsp,%rdx)
	jmp	.L844
	.p2align 4,,10
	.p2align 3
.L873:
	movzwl	(%rax,%rdx), %r8d
	movw	%r8w, 80(%rsp,%rdx)
	addq	$2, %rdx
	andl	$1, %ecx
	je	.L844
	jmp	.L874
	.p2align 4,,10
	.p2align 3
.L872:
	movl	(%rax), %edx
	testb	$2, %cl
	movl	%edx, 80(%rsp)
	movl	$4, %edx
	je	.L843
	jmp	.L873
	.p2align 4,,10
	.p2align 3
.L871:
	cmpb	$0, 32(%r8)
	leaq	24(%r8), %r13
	je	.L875
.L825:
	leaq	96(%rsp), %r12
	movq	%r13, %rdx
	movq	%r12, %rcx
	call	_ZNSt6localeC1ERKS_
	movq	.refptr._ZNSt7__cxx118numpunctIcE2idE(%rip), %rcx
	call	_ZNKSt6locale2id5_M_idEv
	movq	%rax, %rdx
	movq	96(%rsp), %rax
	movq	8(%rax), %rax
	movq	(%rax,%rdx,8), %r13
	testq	%r13, %r13
	je	.L826
	movq	%r12, %rcx
	call	_ZNSt6localeD1Ev
	testb	%sil, %sil
	jne	.L827
	movq	0(%r13), %rax
	leaq	64(%rsp), %rsi
	movq	%r13, %rdx
	movq	%r12, %rcx
.LEHB16:
	call	*48(%rax)
.L829:
	movq	96(%rsp), %rax
	leaq	112(%rsp), %rsi
	movq	64(%rsp), %rcx
	movq	104(%rsp), %r8
	cmpq	%rsi, %rax
	je	.L876
	movq	%r8, %xmm0
	cmpq	%rbp, %rcx
	movhps	112(%rsp), %xmm0
	je	.L877
	testq	%rcx, %rcx
	movq	80(%rsp), %rdx
	movq	%rax, 64(%rsp)
	movups	%xmm0, 72(%rsp)
	je	.L837
	movq	%rcx, 96(%rsp)
	movq	%rdx, 112(%rsp)
.L836:
	movq	$0, 104(%rsp)
	movb	$0, (%rcx)
	movq	96(%rsp), %rcx
	cmpq	%rsi, %rcx
	je	.L868
	movq	112(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	jmp	.L868
	.p2align 4,,10
	.p2align 3
.L827:
	movq	0(%r13), %rax
	leaq	64(%rsp), %rsi
	movq	%r13, %rdx
	movq	%r12, %rcx
	call	*40(%rax)
.LEHE16:
	jmp	.L829
	.p2align 4,,10
	.p2align 3
.L875:
	movq	%r13, %rcx
	call	_ZNSt6localeC1Ev
	movb	$1, 32(%rdi)
	jmp	.L825
.L877:
	movq	%rax, 64(%rsp)
	movups	%xmm0, 72(%rsp)
.L837:
	movq	%rsi, 96(%rsp)
	leaq	112(%rsp), %rsi
	movq	%rsi, %rcx
	jmp	.L836
.L876:
	testq	%r8, %r8
	je	.L832
	cmpq	$1, %r8
	je	.L878
	movq	%rsi, %rdx
	call	memcpy
	movq	104(%rsp), %r8
	movq	64(%rsp), %rcx
.L832:
	movq	%r8, 72(%rsp)
	movb	$0, (%rcx,%r8)
	movq	96(%rsp), %rcx
	jmp	.L836
.L878:
	movzbl	112(%rsp), %eax
	movb	%al, (%rcx)
	movq	104(%rsp), %r8
	movq	64(%rsp), %rcx
	jmp	.L832
.L826:
.LEHB17:
	call	_ZSt16__throw_bad_castv
.LEHE17:
.L851:
	movq	%rax, %rbx
.L848:
	movq	%rsi, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	%rbx, %rcx
.LEHB18:
	call	_Unwind_Resume
.LEHE18:
.L841:
	xorl	%eax, %eax
	movq	%r12, 32(%rsp)
	movq	%rbp, %r9
	xorl	%r8d, %r8d
	movq	%rax, 40(%rsp)
	movq	%rbp, %rdx
	movq	%rsi, %rcx
.LEHB19:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
.LEHE19:
	movq	64(%rsp), %rax
	jmp	.L845
.L850:
	leaq	64(%rsp), %rsi
	movq	%r12, %rcx
	movq	%rax, %rbx
	call	_ZNSt6localeD1Ev
	jmp	.L848
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5088:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5088-.LLSDACSB5088
.LLSDACSB5088:
	.uleb128 .LEHB14-.LFB5088
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L851-.LFB5088
	.uleb128 0
	.uleb128 .LEHB15-.LFB5088
	.uleb128 .LEHE15-.LEHB15
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB16-.LFB5088
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L851-.LFB5088
	.uleb128 0
	.uleb128 .LEHB17-.LFB5088
	.uleb128 .LEHE17-.LEHB17
	.uleb128 .L850-.LFB5088
	.uleb128 0
	.uleb128 .LEHB18-.LFB5088
	.uleb128 .LEHE18-.LEHB18
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB19-.LFB5088
	.uleb128 .LEHE19-.LEHB19
	.uleb128 .L851-.LFB5088
	.uleb128 0
.LLSDACSE5088:
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
.LFB5094:
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$288, %rsp
	.seh_stackalloc	288
	.seh_endprologue
	movl	%edx, %ebx
	movzbl	1(%rcx), %edx
	movq	%rcx, %rsi
	movq	%r8, %rdi
	movl	%edx, %ecx
	andl	$120, %ecx
	cmpb	$56, %cl
	je	.L951
	shrb	$3, %dl
	movl	%ebx, %eax
	andl	$15, %edx
	testb	%bl, %bl
	js	.L952
	cmpb	$4, %dl
	je	.L888
	ja	.L889
	cmpb	$1, %dl
	jbe	.L890
	leaq	.LC13(%rip), %rbp
	cmpb	$16, %cl
	leaq	.LC14(%rip), %rdx
	cmovne	%rdx, %rbp
	testb	%bl, %bl
	jne	.L886
	leaq	73(%rsp), %r12
	movl	$48, %eax
	leaq	72(%rsp), %r13
.L895:
	movb	%al, 72(%rsp)
	movzbl	(%rsi), %eax
	testb	$16, %al
	je	.L936
.L935:
	movq	$-2, %rdx
	movl	$2, %ecx
.L899:
	addq	%r13, %rdx
	testl	%ecx, %ecx
	movl	%ecx, %r10d
	je	.L900
	xorl	%ecx, %ecx
.L917:
	movl	%ecx, %r8d
	addl	$1, %ecx
	movzbl	0(%rbp,%r8), %r9d
	cmpl	%r10d, %ecx
	movb	%r9b, (%rdx,%r8)
	jb	.L917
	.p2align 4,,10
	.p2align 3
.L900:
	leaq	-1(%rdx), %rcx
	shrb	$2, %al
	andl	$3, %eax
	testb	%bl, %bl
	jns	.L902
	movb	$45, -1(%rdx)
	movq	%rcx, %rdx
	jmp	.L919
	.p2align 4,,10
	.p2align 3
.L952:
	negl	%eax
	cmpb	$4, %dl
	je	.L883
	ja	.L884
	cmpb	$1, %dl
	jbe	.L885
	leaq	.LC13(%rip), %rbp
	cmpb	$16, %cl
	leaq	.LC14(%rip), %rdx
	cmovne	%rdx, %rbp
.L886:
	movzbl	%al, %eax
	movl	$32, %r12d
	bsrl	%eax, %r9d
	movl	$31, %edx
	xorl	$31, %r9d
	subl	%r9d, %r12d
	subl	%r9d, %edx
	je	.L898
	movl	%edx, %ecx
	leaq	71(%rsp,%rcx), %r8
	leaq	72(%rsp,%rcx), %rdx
	movl	$30, %ecx
	subl	%r9d, %ecx
	subq	%rcx, %r8
	.p2align 4,,10
	.p2align 3
.L897:
	movl	%eax, %ecx
	subq	$1, %rdx
	shrl	%eax
	andl	$1, %ecx
	addl	$48, %ecx
	movb	%cl, 1(%rdx)
	cmpq	%r8, %rdx
	jne	.L897
.L898:
	leaq	72(%rsp), %r13
	movslq	%r12d, %r12
	movl	$49, %eax
	addq	%r13, %r12
	jmp	.L895
	.p2align 4,,10
	.p2align 3
.L951:
	leaq	80(%rsp), %rax
	movq	%rsi, %r9
	movl	$1, %edx
	movb	%bl, 80(%rsp)
	leaq	48(%rsp), %rcx
	movl	$1, 32(%rsp)
	movq	$1, 48(%rsp)
	movq	%rax, 56(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L949:
	addq	$288, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	ret
	.p2align 4,,10
	.p2align 3
.L890:
	testb	%bl, %bl
	jne	.L901
	movzbl	(%rsi), %eax
	leaq	72(%rsp), %r13
	movb	$48, 72(%rsp)
	leaq	73(%rsp), %r12
	movq	%r13, %rdx
	leaq	71(%rsp), %rcx
	shrb	$2, %al
	andl	$3, %eax
.L902:
	movzbl	%al, %eax
	cmpl	$1, %eax
	je	.L953
	cmpl	$3, %eax
	je	.L954
.L919:
	movq	%r12, %rax
	movq	%r13, %r8
	movq	%rdx, 56(%rsp)
	movq	%rdi, %r9
	subq	%rdx, %rax
	subq	%rdx, %r8
	movq	%rsi, %rcx
	movq	%rax, 48(%rsp)
	leaq	48(%rsp), %rax
	movq	%rax, %rdx
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L949
	.p2align 4,,10
	.p2align 3
.L884:
	leaq	.LC17(%rip), %rbp
	cmpb	$40, %cl
	leaq	.LC16(%rip), %rdx
	cmovne	%rdx, %rbp
.L887:
	movabsq	$3978425819141910832, %r11
	movzbl	%al, %edx
	bsrl	%edx, %r8d
	movq	%r11, 80(%rsp)
	movabsq	$7378413942531504440, %r11
	addl	$4, %r8d
	movq	%r11, 88(%rsp)
	shrl	$2, %r8d
	cmpb	$15, %al
	ja	.L955
	movzbl	80(%rsp,%rdx), %eax
.L915:
	leaq	72(%rsp), %r13
	movl	%r8d, %r12d
	movb	%al, 72(%rsp)
	addq	%r13, %r12
	cmpb	$48, %cl
	je	.L956
.L912:
	movzbl	(%rsi), %eax
	testb	$16, %al
	jne	.L935
.L936:
	movq	%r13, %rdx
	jmp	.L900
	.p2align 4,,10
	.p2align 3
.L953:
	movb	$43, -1(%rdx)
.L922:
	movq	%rcx, %rdx
	jmp	.L919
	.p2align 4,,10
	.p2align 3
.L888:
	testb	%bl, %bl
	jne	.L883
	xorl	%r8d, %r8d
	xorl	%ecx, %ecx
	xorl	%ebp, %ebp
	leaq	73(%rsp), %r12
	movl	$48, %edx
	leaq	72(%rsp), %r13
.L907:
	movb	%dl, 72(%rsp)
.L911:
	movzbl	(%rsi), %eax
	testb	$16, %al
	je	.L936
	movq	%rcx, %rdx
	negq	%rdx
	testb	%r8b, %r8b
	jne	.L899
	movq	%r13, %rdx
	jmp	.L900
	.p2align 4,,10
	.p2align 3
.L889:
	cmpb	$40, %cl
	je	.L957
	testb	%bl, %bl
	jne	.L932
	cmpb	$48, %cl
	movb	$48, 72(%rsp)
	je	.L933
	leaq	.LC16(%rip), %rbp
	leaq	73(%rsp), %r12
	leaq	72(%rsp), %r13
	jmp	.L912
	.p2align 4,,10
	.p2align 3
.L954:
	movb	$32, -1(%rdx)
	jmp	.L922
	.p2align 4,,10
	.p2align 3
.L883:
	movzbl	%al, %edx
	bsrl	%edx, %ecx
	leal	3(%rcx), %r12d
	movl	$2863311531, %ecx
	imulq	%rcx, %r12
	shrq	$33, %r12
	cmpb	$63, %al
	jbe	.L908
	andl	$7, %eax
	addl	$48, %eax
	movb	%al, 74(%rsp)
	movl	%edx, %eax
	shrl	$6, %edx
	shrl	$3, %eax
	andl	$7, %eax
	addl	$48, %eax
	movb	%al, 73(%rsp)
.L909:
	addl	$48, %edx
.L910:
	leaq	72(%rsp), %r13
	movl	%r12d, %r12d
	movl	$1, %r8d
	leaq	.LC15(%rip), %rbp
	addq	%r13, %r12
	movl	$1, %ecx
	jmp	.L907
	.p2align 4,,10
	.p2align 3
.L885:
	movzbl	%al, %r14d
.L923:
	cmpb	$9, %al
	jbe	.L928
	cmpb	$100, %al
	sbbl	%ebp, %ebp
	addl	$2, %ebp
	cmpb	$100, %al
	sbbq	%r12, %r12
	addq	$3, %r12
	cmpb	$100, %al
	sbbl	%r13d, %r13d
	addl	$3, %r13d
.L903:
	leaq	80(%rsp), %rcx
	movl	$201, %r8d
	leaq	.LC19(%rip), %rdx
	call	memcpy
	cmpl	$99, %r14d
	jbe	.L958
	movl	%r14d, %eax
	movl	%ebp, %edx
	imulq	$1374389535, %rax, %rax
	shrq	$37, %rax
	imull	$100, %eax, %eax
	subl	%eax, %r14d
	addl	%r14d, %r14d
	leal	1(%r14), %eax
	movzbl	80(%rsp,%rax), %eax
	movb	%al, 72(%rsp,%rdx)
	movzbl	80(%rsp,%r14), %edx
	leal	-2(%r13), %eax
	movl	$1, %r14d
	movb	%dl, 72(%rsp,%rax)
.L905:
	addl	$48, %r14d
.L906:
	leaq	72(%rsp), %r13
	movzbl	(%rsi), %eax
	movb	%r14b, 72(%rsp)
	addq	%r13, %r12
	movq	%r13, %rdx
	jmp	.L900
	.p2align 4,,10
	.p2align 3
.L955:
	andl	$15, %eax
	shrl	$4, %edx
	movzbl	80(%rsp,%rax), %eax
	movb	%al, 73(%rsp)
	movzbl	80(%rsp,%rdx), %eax
	jmp	.L915
	.p2align 4,,10
	.p2align 3
.L933:
	leaq	73(%rsp), %r12
	leaq	.LC16(%rip), %rbp
	leaq	72(%rsp), %r13
.L913:
	movq	%r13, %r14
	.p2align 4,,10
	.p2align 3
.L916:
	movsbl	(%r14), %ecx
	addq	$1, %r14
	call	toupper
	movb	%al, -1(%r14)
	cmpq	%r12, %r14
	jne	.L916
	movl	$1, %r8d
	movl	$2, %ecx
	jmp	.L911
	.p2align 4,,10
	.p2align 3
.L956:
	testl	%r8d, %r8d
	jne	.L913
	movl	$1, %r8d
	movl	$2, %ecx
	movq	%r13, %r12
	jmp	.L911
	.p2align 4,,10
	.p2align 3
.L957:
	testb	%bl, %bl
	jne	.L931
	movb	$48, 72(%rsp)
	leaq	.LC17(%rip), %rbp
	leaq	73(%rsp), %r12
	leaq	72(%rsp), %r13
	jmp	.L912
	.p2align 4,,10
	.p2align 3
.L928:
	xorl	%ebp, %ebp
	movl	$1, %r12d
	movl	$1, %r13d
	jmp	.L903
	.p2align 4,,10
	.p2align 3
.L901:
	movsbl	%bl, %r14d
	jmp	.L923
	.p2align 4,,10
	.p2align 3
.L932:
	leaq	.LC16(%rip), %rbp
	jmp	.L887
	.p2align 4,,10
	.p2align 3
.L958:
	cmpl	$9, %r14d
	jbe	.L905
	addl	%r14d, %r14d
	leal	1(%r14), %eax
	movzbl	80(%rsp,%r14), %r14d
	movzbl	80(%rsp,%rax), %eax
	movb	%al, 73(%rsp)
	jmp	.L906
.L931:
	leaq	.LC17(%rip), %rbp
	jmp	.L887
.L908:
	cmpb	$7, %al
	jbe	.L909
	andl	$7, %eax
	shrl	$3, %edx
	addl	$48, %eax
	addl	$48, %edx
	movb	%al, 73(%rsp)
	jmp	.L910
	.seh_endproc
	.section	.text$_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5095:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$328, %rsp
	.seh_stackalloc	328
	.seh_endprologue
	movzbl	1(%rcx), %eax
	movl	%edx, %esi
	movl	%eax, %edx
	movq	%rcx, %rdi
	andl	$120, %edx
	movq	%r8, %rbp
	movl	%esi, %ebx
	cmpb	$56, %dl
	je	.L1047
	shrb	$3, %al
	andl	$15, %eax
	testl	%esi, %esi
	js	.L1048
	cmpb	$4, %al
	je	.L969
	ja	.L970
	cmpb	$1, %al
	jbe	.L971
	leaq	.LC13(%rip), %r14
	cmpb	$16, %dl
	leaq	.LC14(%rip), %rax
	cmovne	%rax, %r14
	testl	%esi, %esi
	jne	.L967
	leaq	68(%rsp), %r12
	movl	$48, %eax
	leaq	67(%rsp), %r13
.L976:
	movzbl	(%rdi), %ebx
	movb	%al, 67(%rsp)
	testb	$16, %bl
	je	.L1029
.L1028:
	movq	$-2, %rdx
	movl	$2, %eax
.L980:
	addq	%r13, %rdx
	testl	%eax, %eax
	movl	%eax, %r9d
	je	.L981
	xorl	%eax, %eax
.L1007:
	movl	%eax, %ecx
	addl	$1, %eax
	movzbl	(%r14,%rcx), %r8d
	cmpl	%r9d, %eax
	movb	%r8b, (%rdx,%rcx)
	jb	.L1007
.L981:
	leaq	-1(%rdx), %rcx
	movl	%ebx, %eax
	shrb	$2, %al
	andl	$3, %eax
	testl	%esi, %esi
	jns	.L982
.L1050:
	movb	$45, -1(%rdx)
	movq	%rcx, %rdx
.L1009:
	leaq	48(%rsp), %rax
	movq	%r13, %r8
	subq	%rdx, %r12
	movq	%rdx, 56(%rsp)
	subq	%rdx, %r8
	movq	%rbp, %r9
	movq	%rax, %rdx
	movq	%r12, 48(%rsp)
	movq	%rdi, %rcx
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L962
	.p2align 4,,10
	.p2align 3
.L1048:
	movl	%esi, %ebx
	negl	%ebx
	cmpb	$4, %al
	je	.L964
	ja	.L965
	cmpb	$1, %al
	jbe	.L966
	leaq	.LC13(%rip), %r14
	cmpb	$16, %dl
	leaq	.LC14(%rip), %rax
	cmovne	%rax, %r14
.L967:
	bsrl	%ebx, %r8d
	movl	$32, %r12d
	xorl	$31, %r8d
	movl	$31, %eax
	subl	%r8d, %r12d
	subl	%r8d, %eax
	je	.L979
	movl	%eax, %edx
	leaq	63(%rsp,%rdx), %rcx
	leaq	64(%rsp,%rdx), %rax
	movl	$30, %edx
	subl	%r8d, %edx
	subq	%rdx, %rcx
	.p2align 4,,10
	.p2align 3
.L978:
	movl	%ebx, %edx
	subq	$1, %rax
	shrl	%ebx
	andl	$1, %edx
	addl	$48, %edx
	movb	%dl, 4(%rax)
	cmpq	%rcx, %rax
	jne	.L978
.L979:
	leaq	67(%rsp), %r13
	movslq	%r12d, %r12
	movl	$49, %eax
	addq	%r13, %r12
	jmp	.L976
	.p2align 4,,10
	.p2align 3
.L1047:
	leal	128(%rsi), %eax
	cmpl	$255, %eax
	ja	.L961
	leaq	112(%rsp), %rax
	movq	%rdi, %r9
	movl	$1, %edx
	movb	%sil, 112(%rsp)
	leaq	48(%rsp), %rcx
	movl	$1, 32(%rsp)
	movq	$1, 48(%rsp)
	movq	%rax, 56(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L962:
	addq	$328, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L970:
	cmpb	$40, %dl
	je	.L1049
	testl	%esi, %esi
	jne	.L1025
	movzbl	(%rcx), %ebx
	movb	$48, 67(%rsp)
	leaq	68(%rsp), %r12
	cmpb	$48, %dl
	leaq	.LC16(%rip), %r14
	leaq	67(%rsp), %r13
	je	.L1000
.L1001:
	testb	$16, %bl
	jne	.L1028
	.p2align 4,,10
	.p2align 3
.L1029:
	movq	%r13, %rdx
.L1053:
	leaq	-1(%rdx), %rcx
	movl	%ebx, %eax
	shrb	$2, %al
	andl	$3, %eax
	testl	%esi, %esi
	js	.L1050
.L982:
	movzbl	%al, %eax
	cmpl	$1, %eax
	je	.L1051
	cmpl	$3, %eax
	jne	.L1009
	movb	$32, -1(%rdx)
.L1012:
	movq	%rcx, %rdx
	jmp	.L1009
	.p2align 4,,10
	.p2align 3
.L965:
	leaq	.LC17(%rip), %r14
	cmpb	$40, %dl
	leaq	.LC16(%rip), %rax
	cmovne	%rax, %r14
.L968:
	bsrl	%ebx, %eax
	leal	4(%rax), %r9d
	movabsq	$3978425819141910832, %rax
	shrl	$2, %r9d
	movq	%rax, 112(%rsp)
	cmpl	$255, %ebx
	movabsq	$7378413942531504440, %rax
	movq	%rax, 120(%rsp)
	leal	-1(%r9), %eax
	jbe	.L1002
	.p2align 4,,10
	.p2align 3
.L1003:
	movl	%ebx, %r8d
	movl	%eax, %ecx
	andl	$15, %r8d
	movzbl	112(%rsp,%r8), %r8d
	movb	%r8b, 67(%rsp,%rcx)
	leal	-1(%rax), %r8d
	movl	%ebx, %ecx
	shrl	$8, %ebx
	shrl	$4, %ecx
	subl	$2, %eax
	andl	$15, %ecx
	cmpl	$255, %ebx
	movzbl	112(%rsp,%rcx), %ecx
	movb	%cl, 67(%rsp,%r8)
	ja	.L1003
.L1002:
	cmpl	$15, %ebx
	ja	.L1052
	movzbl	112(%rsp,%rbx), %eax
.L1005:
	leaq	67(%rsp), %r13
	movl	%r9d, %r12d
	movzbl	(%rdi), %ebx
	movb	%al, 67(%rsp)
	addq	%r13, %r12
	cmpb	$48, %dl
	jne	.L1001
	testl	%r9d, %r9d
	jne	.L1000
	movl	$1, %ecx
	movl	$2, %eax
	movq	%r13, %r12
	jmp	.L999
	.p2align 4,,10
	.p2align 3
.L1000:
	movq	%r13, %r15
	.p2align 4,,10
	.p2align 3
.L1006:
	movsbl	(%r15), %ecx
	addq	$1, %r15
	call	toupper
	movb	%al, -1(%r15)
	cmpq	%r12, %r15
	jne	.L1006
	movl	$1, %ecx
	movl	$2, %eax
	jmp	.L999
	.p2align 4,,10
	.p2align 3
.L1051:
	movb	$43, -1(%rdx)
	jmp	.L1012
	.p2align 4,,10
	.p2align 3
.L971:
	testl	%esi, %esi
	jne	.L966
	movzbl	(%rcx), %eax
	leaq	67(%rsp), %r13
	movb	$48, 67(%rsp)
	leaq	68(%rsp), %r12
	movq	%r13, %rdx
	leaq	66(%rsp), %rcx
	shrb	$2, %al
	andl	$3, %eax
	jmp	.L982
	.p2align 4,,10
	.p2align 3
.L969:
	testl	%esi, %esi
	jne	.L964
	xorl	%ecx, %ecx
	xorl	%eax, %eax
	xorl	%r14d, %r14d
	leaq	68(%rsp), %r12
	movl	$48, %edx
	leaq	67(%rsp), %r13
.L994:
	movzbl	(%rdi), %ebx
	movb	%dl, 67(%rsp)
.L999:
	testb	$16, %bl
	je	.L1029
	movq	%rax, %rdx
	negq	%rdx
	testb	%cl, %cl
	jne	.L980
	movq	%r13, %rdx
	jmp	.L1053
	.p2align 4,,10
	.p2align 3
.L966:
	cmpl	$9, %ebx
	jbe	.L1017
	cmpl	$99, %ebx
	jbe	.L1054
	cmpl	$999, %ebx
	jbe	.L1018
	cmpl	$9999, %ebx
	jbe	.L1055
	cmpl	$99999, %ebx
	movl	$5, %r12d
	jbe	.L989
	cmpl	$999999, %ebx
	jbe	.L1056
	cmpl	$9999999, %ebx
	jbe	.L1020
	cmpl	$99999999, %ebx
	jbe	.L1021
	cmpl	$999999999, %ebx
	jbe	.L1022
	movl	$5, %r12d
.L990:
	addl	$5, %r12d
.L989:
	leal	-1(%r12), %r13d
.L986:
	leaq	112(%rsp), %rcx
	movl	$201, %r8d
	leaq	.LC19(%rip), %rdx
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L992:
	movl	%ebx, %edx
	movl	%ebx, %eax
	imulq	$1374389535, %rdx, %rdx
	shrq	$37, %rdx
	imull	$100, %edx, %ecx
	subl	%ecx, %eax
	movl	%ebx, %ecx
	movl	%edx, %ebx
	addl	%eax, %eax
	movl	%r13d, %edx
	leal	1(%rax), %r8d
	movzbl	112(%rsp,%rax), %eax
	movzbl	112(%rsp,%r8), %r8d
	movb	%r8b, 67(%rsp,%rdx)
	leal	-1(%r13), %edx
	subl	$2, %r13d
	cmpl	$9999, %ecx
	movb	%al, 67(%rsp,%rdx)
	ja	.L992
	cmpl	$999, %ecx
	ja	.L985
.L983:
	addl	$48, %ebx
.L993:
	leaq	67(%rsp), %r13
	movb	%bl, 67(%rsp)
	movzbl	(%rdi), %ebx
	addq	%r13, %r12
	movq	%r13, %rdx
	jmp	.L981
	.p2align 4,,10
	.p2align 3
.L964:
	bsrl	%ebx, %eax
	leal	3(%rax), %r12d
	movl	$2863311531, %eax
	imulq	%rax, %r12
	shrq	$33, %r12
	cmpl	$63, %ebx
	leal	-1(%r12), %edx
	jbe	.L995
	.p2align 4,,10
	.p2align 3
.L996:
	movl	%ebx, %eax
	movl	%edx, %ecx
	andl	$7, %eax
	addl	$48, %eax
	movb	%al, 67(%rsp,%rcx)
	leal	-1(%rdx), %ecx
	movl	%ebx, %eax
	shrl	$6, %ebx
	shrl	$3, %eax
	subl	$2, %edx
	andl	$7, %eax
	addl	$48, %eax
	cmpl	$63, %ebx
	movb	%al, 67(%rsp,%rcx)
	ja	.L996
.L995:
	leal	48(%rbx), %edx
	cmpl	$7, %ebx
	jbe	.L998
	movl	%ebx, %eax
	shrl	$3, %ebx
	andl	$7, %eax
	movl	%ebx, %edx
	addl	$48, %eax
	addl	$48, %edx
	movb	%al, 68(%rsp)
.L998:
	leaq	67(%rsp), %r13
	movl	%r12d, %r12d
	movl	$1, %ecx
	leaq	.LC15(%rip), %r14
	addq	%r13, %r12
	movl	$1, %eax
	jmp	.L994
	.p2align 4,,10
	.p2align 3
.L1052:
	movl	%ebx, %eax
	shrl	$4, %ebx
	andl	$15, %eax
	movzbl	112(%rsp,%rax), %eax
	movb	%al, 68(%rsp)
	movzbl	112(%rsp,%rbx), %eax
	jmp	.L1005
.L1054:
	leaq	112(%rsp), %rcx
	movl	$201, %r8d
	movl	$2, %r12d
	leaq	.LC19(%rip), %rdx
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L985:
	addl	%ebx, %ebx
	leal	1(%rbx), %eax
	movzbl	112(%rsp,%rbx), %ebx
	movzbl	112(%rsp,%rax), %eax
	movb	%al, 68(%rsp)
	jmp	.L993
	.p2align 4,,10
	.p2align 3
.L1049:
	testl	%esi, %esi
	jne	.L1024
	movzbl	(%rdi), %ebx
	movb	$48, 67(%rsp)
	movl	$1, %ecx
	movl	$2, %eax
	leaq	.LC17(%rip), %r14
	leaq	68(%rsp), %r12
	leaq	67(%rsp), %r13
	jmp	.L999
	.p2align 4,,10
	.p2align 3
.L1020:
	movl	$7, %r12d
	jmp	.L989
	.p2align 4,,10
	.p2align 3
.L1021:
	movl	$8, %r12d
	jmp	.L989
	.p2align 4,,10
	.p2align 3
.L1022:
	movl	$9, %r12d
	jmp	.L989
	.p2align 4,,10
	.p2align 3
.L1025:
	leaq	.LC16(%rip), %r14
	jmp	.L968
.L1024:
	leaq	.LC17(%rip), %r14
	jmp	.L968
.L1017:
	movl	$1, %r12d
	jmp	.L983
.L1055:
	movl	$4, %r12d
	movl	$3, %r13d
	jmp	.L986
.L1018:
	movl	$3, %r12d
	movl	$2, %r13d
	jmp	.L986
.L1056:
	movl	$1, %r12d
	jmp	.L990
.L961:
	leaq	.LC18(%rip), %rcx
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
.LFB5097:
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$328, %rsp
	.seh_stackalloc	328
	.seh_endprologue
	movzbl	1(%rcx), %eax
	movl	%edx, %ebx
	movl	%eax, %edx
	movq	%rcx, %rsi
	andl	$120, %edx
	movq	%r8, %rdi
	cmpb	$56, %dl
	je	.L1137
	shrb	$3, %al
	andl	$15, %eax
	cmpb	$4, %al
	je	.L1061
	ja	.L1062
	cmpb	$1, %al
	jbe	.L1063
	leaq	.LC13(%rip), %rbp
	cmpb	$16, %dl
	leaq	.LC14(%rip), %rax
	cmovne	%rax, %rbp
	testl	%ebx, %ebx
	jne	.L1138
	leaq	68(%rsp), %rbx
	movl	$48, %eax
	leaq	67(%rsp), %r12
.L1068:
	movb	%al, 67(%rsp)
	movzbl	(%rsi), %eax
	testb	$16, %al
	je	.L1120
.L1119:
	movq	$-2, %rdx
	movl	$2, %ecx
.L1072:
	addq	%r12, %rdx
	testl	%ecx, %ecx
	movl	%ecx, %r10d
	je	.L1073
	xorl	%ecx, %ecx
.L1101:
	movl	%ecx, %r8d
	addl	$1, %ecx
	movzbl	0(%rbp,%r8), %r9d
	cmpl	%r10d, %ecx
	movb	%r9b, (%rdx,%r8)
	jb	.L1101
	jmp	.L1073
	.p2align 4,,10
	.p2align 3
.L1137:
	cmpl	$127, %ebx
	ja	.L1059
	leaq	112(%rsp), %rax
	movq	%rsi, %r9
	movl	$1, %edx
	movb	%bl, 112(%rsp)
	leaq	48(%rsp), %rcx
	movl	$1, 32(%rsp)
	movq	$1, 48(%rsp)
	movq	%rax, 56(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	addq	$328, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L1063:
	testl	%ebx, %ebx
	jne	.L1074
	movb	$48, 67(%rsp)
	leaq	68(%rsp), %rbx
	leaq	67(%rsp), %r12
.L1075:
	movzbl	(%rsi), %eax
	movq	%r12, %rdx
.L1073:
	shrb	$2, %al
	andl	$3, %eax
	cmpl	$1, %eax
	je	.L1139
.L1103:
	cmpl	$3, %eax
	je	.L1121
.L1104:
	leaq	48(%rsp), %rax
	movq	%r12, %r8
	subq	%rdx, %rbx
	movq	%rdx, 56(%rsp)
	subq	%rdx, %r8
	movq	%rdi, %r9
	movq	%rax, %rdx
	movq	%rbx, 48(%rsp)
	movq	%rsi, %rcx
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	addq	$328, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L1061:
	testl	%ebx, %ebx
	je	.L1114
	bsrl	%ebx, %eax
	leal	3(%rax), %r8d
	movl	$2863311531, %eax
	imulq	%rax, %r8
	shrq	$33, %r8
	cmpl	$63, %ebx
	leal	-1(%r8), %edx
	jbe	.L1088
	.p2align 4,,10
	.p2align 3
.L1089:
	movl	%ebx, %eax
	movl	%edx, %ecx
	andl	$7, %eax
	addl	$48, %eax
	movb	%al, 67(%rsp,%rcx)
	leal	-1(%rdx), %ecx
	movl	%ebx, %eax
	shrl	$6, %ebx
	shrl	$3, %eax
	subl	$2, %edx
	andl	$7, %eax
	addl	$48, %eax
	cmpl	$63, %ebx
	movb	%al, 67(%rsp,%rcx)
	ja	.L1089
.L1088:
	leal	48(%rbx), %eax
	cmpl	$7, %ebx
	ja	.L1140
.L1091:
	leaq	67(%rsp), %r12
	movl	%r8d, %ebx
	movl	$1, %edx
	leaq	.LC15(%rip), %rbp
	addq	%r12, %rbx
	movl	$1, %ecx
.L1087:
	movb	%al, 67(%rsp)
.L1092:
	movzbl	(%rsi), %eax
	testb	$16, %al
	je	.L1120
	testb	%dl, %dl
	jne	.L1141
.L1120:
	shrb	$2, %al
	movq	%r12, %rdx
	andl	$3, %eax
	cmpl	$1, %eax
	jne	.L1103
.L1139:
	movl	$43, %eax
.L1105:
	movb	%al, -1(%rdx)
	subq	$1, %rdx
	jmp	.L1104
	.p2align 4,,10
	.p2align 3
.L1062:
	cmpb	$40, %dl
	je	.L1142
	testl	%ebx, %ebx
	jne	.L1116
	cmpb	$48, %dl
	movb	$48, 67(%rsp)
	je	.L1117
	leaq	.LC16(%rip), %rbp
	leaq	68(%rsp), %rbx
	leaq	67(%rsp), %r12
	jmp	.L1094
	.p2align 4,,10
	.p2align 3
.L1121:
	movl	$32, %eax
	jmp	.L1105
	.p2align 4,,10
	.p2align 3
.L1074:
	cmpl	$9, %ebx
	jbe	.L1108
	cmpl	$99, %ebx
	jbe	.L1143
	cmpl	$999, %ebx
	jbe	.L1109
	cmpl	$9999, %ebx
	jbe	.L1144
	cmpl	$99999, %ebx
	movl	$5, %ebp
	jbe	.L1082
	cmpl	$999999, %ebx
	jbe	.L1145
	cmpl	$9999999, %ebx
	jbe	.L1111
	cmpl	$99999999, %ebx
	jbe	.L1112
	cmpl	$999999999, %ebx
	jbe	.L1113
	movl	$5, %ebp
.L1083:
	addl	$5, %ebp
.L1082:
	leal	-1(%rbp), %r12d
.L1079:
	leaq	112(%rsp), %rcx
	movl	$201, %r8d
	leaq	.LC19(%rip), %rdx
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L1085:
	movl	%ebx, %edx
	movl	%ebx, %eax
	imulq	$1374389535, %rdx, %rdx
	shrq	$37, %rdx
	imull	$100, %edx, %ecx
	subl	%ecx, %eax
	movl	%ebx, %ecx
	movl	%edx, %ebx
	addl	%eax, %eax
	movl	%r12d, %edx
	leal	1(%rax), %r8d
	movzbl	112(%rsp,%rax), %eax
	movzbl	112(%rsp,%r8), %r8d
	movb	%r8b, 67(%rsp,%rdx)
	leal	-1(%r12), %edx
	subl	$2, %r12d
	cmpl	$9999, %ecx
	movb	%al, 67(%rsp,%rdx)
	ja	.L1085
	cmpl	$999, %ecx
	jbe	.L1076
.L1078:
	addl	%ebx, %ebx
	leal	1(%rbx), %eax
	movzbl	112(%rsp,%rbx), %ebx
	movzbl	112(%rsp,%rax), %eax
	movb	%al, 68(%rsp)
	jmp	.L1086
	.p2align 4,,10
	.p2align 3
.L1138:
	bsrl	%ebx, %r8d
	movl	$32, %r9d
	movl	$31, %eax
	xorl	$31, %r8d
	subl	%r8d, %r9d
	subl	%r8d, %eax
	je	.L1071
	movl	%eax, %edx
	leaq	63(%rsp,%rdx), %rcx
	leaq	64(%rsp,%rdx), %rax
	movl	$30, %edx
	subl	%r8d, %edx
	subq	%rdx, %rcx
	.p2align 4,,10
	.p2align 3
.L1070:
	movl	%ebx, %edx
	subq	$1, %rax
	shrl	%ebx
	andl	$1, %edx
	addl	$48, %edx
	movb	%dl, 4(%rax)
	cmpq	%rcx, %rax
	jne	.L1070
.L1071:
	leaq	67(%rsp), %r12
	movslq	%r9d, %rbx
	movl	$49, %eax
	addq	%r12, %rbx
	jmp	.L1068
	.p2align 4,,10
	.p2align 3
.L1114:
	movl	$48, %eax
	xorl	%edx, %edx
	xorl	%ebp, %ebp
	leaq	68(%rsp), %rbx
	xorl	%ecx, %ecx
	leaq	67(%rsp), %r12
	jmp	.L1087
	.p2align 4,,10
	.p2align 3
.L1142:
	testl	%ebx, %ebx
	jne	.L1115
	movb	$48, 67(%rsp)
	leaq	.LC17(%rip), %rbp
	leaq	68(%rsp), %rbx
	leaq	67(%rsp), %r12
	jmp	.L1094
	.p2align 4,,10
	.p2align 3
.L1116:
	leaq	.LC16(%rip), %rbp
.L1093:
	bsrl	%ebx, %eax
	leal	4(%rax), %r9d
	movabsq	$3978425819141910832, %rax
	shrl	$2, %r9d
	movq	%rax, 112(%rsp)
	cmpl	$255, %ebx
	movabsq	$7378413942531504440, %rax
	movq	%rax, 120(%rsp)
	leal	-1(%r9), %eax
	jbe	.L1096
	.p2align 4,,10
	.p2align 3
.L1097:
	movl	%ebx, %r8d
	movl	%eax, %ecx
	andl	$15, %r8d
	movzbl	112(%rsp,%r8), %r8d
	movb	%r8b, 67(%rsp,%rcx)
	leal	-1(%rax), %r8d
	movl	%ebx, %ecx
	shrl	$8, %ebx
	shrl	$4, %ecx
	subl	$2, %eax
	andl	$15, %ecx
	cmpl	$255, %ebx
	movzbl	112(%rsp,%rcx), %ecx
	movb	%cl, 67(%rsp,%r8)
	ja	.L1097
.L1096:
	cmpl	$15, %ebx
	ja	.L1146
	movzbl	112(%rsp,%rbx), %eax
.L1099:
	leaq	67(%rsp), %r12
	movl	%r9d, %ebx
	movb	%al, 67(%rsp)
	addq	%r12, %rbx
	cmpb	$48, %dl
	je	.L1147
.L1094:
	movzbl	(%rsi), %eax
	testb	$16, %al
	jne	.L1119
	jmp	.L1120
	.p2align 4,,10
	.p2align 3
.L1146:
	movl	%ebx, %eax
	shrl	$4, %ebx
	andl	$15, %eax
	movzbl	112(%rsp,%rax), %eax
	movb	%al, 68(%rsp)
	movzbl	112(%rsp,%rbx), %eax
	jmp	.L1099
	.p2align 4,,10
	.p2align 3
.L1140:
	movl	%ebx, %eax
	andl	$7, %eax
	addl	$48, %eax
	movb	%al, 68(%rsp)
	movl	%ebx, %eax
	shrl	$3, %eax
	addl	$48, %eax
	jmp	.L1091
.L1108:
	movl	$1, %ebp
	.p2align 4,,10
	.p2align 3
.L1076:
	addl	$48, %ebx
.L1086:
	leaq	67(%rsp), %r12
	movb	%bl, 67(%rsp)
	leaq	(%r12,%rbp), %rbx
	jmp	.L1075
	.p2align 4,,10
	.p2align 3
.L1115:
	leaq	.LC17(%rip), %rbp
	jmp	.L1093
	.p2align 4,,10
	.p2align 3
.L1117:
	leaq	68(%rsp), %rbx
	leaq	.LC16(%rip), %rbp
	leaq	67(%rsp), %r12
.L1095:
	movq	%r12, %r13
	.p2align 4,,10
	.p2align 3
.L1100:
	movsbl	0(%r13), %ecx
	addq	$1, %r13
	call	toupper
	movb	%al, -1(%r13)
	cmpq	%rbx, %r13
	jne	.L1100
	movl	$1, %edx
	movl	$2, %ecx
	jmp	.L1092
	.p2align 4,,10
	.p2align 3
.L1147:
	testl	%r9d, %r9d
	jne	.L1095
	movl	$1, %edx
	movl	$2, %ecx
	movq	%r12, %rbx
	jmp	.L1092
	.p2align 4,,10
	.p2align 3
.L1111:
	movl	$7, %ebp
	jmp	.L1082
	.p2align 4,,10
	.p2align 3
.L1112:
	movl	$8, %ebp
	jmp	.L1082
	.p2align 4,,10
	.p2align 3
.L1113:
	movl	$9, %ebp
	jmp	.L1082
	.p2align 4,,10
	.p2align 3
.L1141:
	movq	%rcx, %rdx
	negq	%rdx
	jmp	.L1072
.L1143:
	leaq	112(%rsp), %rcx
	movl	$201, %r8d
	movl	$2, %ebp
	leaq	.LC19(%rip), %rdx
	call	memcpy
	jmp	.L1078
.L1109:
	movl	$3, %ebp
	movl	$2, %r12d
	jmp	.L1079
.L1144:
	movl	$4, %ebp
	movl	$3, %r12d
	jmp	.L1079
.L1145:
	movl	$1, %ebp
	jmp	.L1083
.L1059:
	leaq	.LC18(%rip), %rcx
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
.LFB5099:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$360, %rsp
	.seh_stackalloc	360
	.seh_endprologue
	movzbl	1(%rcx), %eax
	movq	%rdx, %r12
	movl	%eax, %edx
	movq	%rcx, %rdi
	andl	$120, %edx
	movq	%r8, %rbp
	movq	%r12, %rbx
	cmpb	$56, %dl
	je	.L1235
	shrb	$3, %al
	andl	$15, %eax
	testq	%r12, %r12
	js	.L1236
	cmpb	$4, %al
	je	.L1158
	ja	.L1159
	cmpb	$1, %al
	jbe	.L1160
	leaq	.LC13(%rip), %r14
	cmpb	$16, %dl
	leaq	.LC14(%rip), %rax
	cmovne	%rax, %r14
	testq	%r12, %r12
	jne	.L1156
	leaq	68(%rsp), %rsi
	movl	$48, %eax
	leaq	67(%rsp), %r13
.L1165:
	movzbl	(%rdi), %ebx
	movb	%al, 67(%rsp)
	testb	$16, %bl
	je	.L1217
.L1216:
	movq	$-2, %rdx
	movl	$2, %eax
.L1169:
	addq	%r13, %rdx
	testl	%eax, %eax
	movl	%eax, %r9d
	je	.L1170
	xorl	%eax, %eax
.L1197:
	movl	%eax, %ecx
	addl	$1, %eax
	movzbl	(%r14,%rcx), %r8d
	cmpl	%r9d, %eax
	movb	%r8b, (%rdx,%rcx)
	jb	.L1197
	.p2align 4,,10
	.p2align 3
.L1170:
	leaq	-1(%rdx), %rcx
	movl	%ebx, %eax
	shrb	$2, %al
	andl	$3, %eax
	testq	%r12, %r12
	jns	.L1171
	movb	$45, -1(%rdx)
	movq	%rcx, %rdx
.L1199:
	leaq	48(%rsp), %rax
	movq	%r13, %r8
	subq	%rdx, %rsi
	movq	%rdx, 56(%rsp)
	subq	%rdx, %r8
	movq	%rbp, %r9
	movq	%rax, %rdx
	movq	%rsi, 48(%rsp)
	movq	%rdi, %rcx
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L1151
	.p2align 4,,10
	.p2align 3
.L1236:
	negq	%rbx
	cmpb	$4, %al
	je	.L1153
	ja	.L1154
	cmpb	$1, %al
	jbe	.L1155
	leaq	.LC13(%rip), %r14
	cmpb	$16, %dl
	leaq	.LC14(%rip), %rax
	cmovne	%rax, %r14
.L1156:
	bsrq	%rbx, %r8
	movl	$64, %esi
	xorq	$63, %r8
	movl	$63, %eax
	subl	%r8d, %esi
	subl	%r8d, %eax
	je	.L1168
	movl	%eax, %edx
	leaq	63(%rsp,%rdx), %rcx
	leaq	64(%rsp,%rdx), %rax
	movl	$62, %edx
	subl	%r8d, %edx
	subq	%rdx, %rcx
	.p2align 4,,10
	.p2align 3
.L1167:
	movl	%ebx, %edx
	subq	$1, %rax
	shrq	%rbx
	andl	$1, %edx
	addl	$48, %edx
	movb	%dl, 4(%rax)
	cmpq	%rcx, %rax
	jne	.L1167
.L1168:
	leaq	67(%rsp), %r13
	movslq	%esi, %rsi
	movl	$49, %eax
	addq	%r13, %rsi
	jmp	.L1165
	.p2align 4,,10
	.p2align 3
.L1235:
	leaq	128(%r12), %rax
	cmpq	$255, %rax
	ja	.L1150
	leaq	144(%rsp), %rax
	movl	$1, 32(%rsp)
	movq	%rdi, %r9
	movl	$1, %edx
	leaq	48(%rsp), %rcx
	movb	%r12b, 144(%rsp)
	movq	$1, 48(%rsp)
	movq	%rax, 56(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1151:
	addq	$360, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L1159:
	cmpb	$40, %dl
	je	.L1237
	testq	%r12, %r12
	jne	.L1213
	movzbl	(%rcx), %ebx
	movb	$48, 67(%rsp)
	leaq	68(%rsp), %rsi
	cmpb	$48, %dl
	leaq	.LC16(%rip), %r14
	leaq	67(%rsp), %r13
	je	.L1190
.L1191:
	testb	$16, %bl
	jne	.L1216
	.p2align 4,,10
	.p2align 3
.L1217:
	movq	%r13, %rdx
	jmp	.L1170
	.p2align 4,,10
	.p2align 3
.L1154:
	leaq	.LC17(%rip), %r14
	cmpb	$40, %dl
	leaq	.LC16(%rip), %rax
	cmovne	%rax, %r14
.L1157:
	bsrq	%rbx, %rax
	leal	4(%rax), %r9d
	movabsq	$3978425819141910832, %rax
	shrl	$2, %r9d
	movq	%rax, 144(%rsp)
	cmpq	$255, %rbx
	movabsq	$7378413942531504440, %rax
	movq	%rax, 152(%rsp)
	leal	-1(%r9), %eax
	jbe	.L1192
	.p2align 4,,10
	.p2align 3
.L1193:
	movq	%rbx, %r8
	movl	%eax, %ecx
	andl	$15, %r8d
	movzbl	144(%rsp,%r8), %r8d
	movb	%r8b, 67(%rsp,%rcx)
	leal	-1(%rax), %r8d
	movq	%rbx, %rcx
	shrq	$8, %rbx
	shrq	$4, %rcx
	subl	$2, %eax
	andl	$15, %ecx
	cmpq	$255, %rbx
	movzbl	144(%rsp,%rcx), %ecx
	movb	%cl, 67(%rsp,%r8)
	ja	.L1193
.L1192:
	cmpq	$15, %rbx
	ja	.L1238
	movzbl	144(%rsp,%rbx), %eax
.L1195:
	leaq	67(%rsp), %r13
	movl	%r9d, %esi
	movzbl	(%rdi), %ebx
	movb	%al, 67(%rsp)
	addq	%r13, %rsi
	cmpb	$48, %dl
	jne	.L1191
	testl	%r9d, %r9d
	jne	.L1190
	movl	$1, %ecx
	movl	$2, %eax
	movq	%r13, %rsi
	jmp	.L1189
	.p2align 4,,10
	.p2align 3
.L1190:
	movq	%r13, %r15
	.p2align 4,,10
	.p2align 3
.L1196:
	movsbl	(%r15), %ecx
	addq	$1, %r15
	call	toupper
	movb	%al, -1(%r15)
	cmpq	%r15, %rsi
	jne	.L1196
	movl	$1, %ecx
	movl	$2, %eax
	jmp	.L1189
	.p2align 4,,10
	.p2align 3
.L1160:
	testq	%r12, %r12
	jne	.L1155
	movzbl	(%rcx), %eax
	leaq	67(%rsp), %r13
	movb	$48, 67(%rsp)
	leaq	68(%rsp), %rsi
	movq	%r13, %rdx
	leaq	66(%rsp), %rcx
	shrb	$2, %al
	andl	$3, %eax
.L1171:
	movzbl	%al, %eax
	cmpl	$1, %eax
	je	.L1239
	cmpl	$3, %eax
	jne	.L1199
	movb	$32, -1(%rdx)
.L1202:
	movq	%rcx, %rdx
	jmp	.L1199
	.p2align 4,,10
	.p2align 3
.L1239:
	movb	$43, -1(%rdx)
	jmp	.L1202
	.p2align 4,,10
	.p2align 3
.L1158:
	testq	%r12, %r12
	jne	.L1153
	xorl	%ecx, %ecx
	xorl	%eax, %eax
	xorl	%r14d, %r14d
	leaq	68(%rsp), %rsi
	movl	$48, %edx
	leaq	67(%rsp), %r13
.L1184:
	movzbl	(%rdi), %ebx
	movb	%dl, 67(%rsp)
.L1189:
	testb	$16, %bl
	je	.L1217
	movq	%rax, %rdx
	negq	%rdx
	testb	%cl, %cl
	jne	.L1169
	movq	%r13, %rdx
	jmp	.L1170
	.p2align 4,,10
	.p2align 3
.L1155:
	cmpq	$9, %rbx
	jbe	.L1207
	cmpq	$99, %rbx
	jbe	.L1240
	cmpq	$999, %rbx
	jbe	.L1208
	cmpq	$9999, %rbx
	jbe	.L1209
	movq	%rbx, %rdx
	movl	$1, %esi
	movabsq	$3777893186295716171, %r8
	jmp	.L1176
	.p2align 4,,10
	.p2align 3
.L1180:
	cmpq	$999999, %rcx
	jbe	.L1241
	cmpq	$9999999, %rcx
	jbe	.L1242
	cmpq	$99999999, %rcx
	jbe	.L1243
.L1176:
	movq	%rdx, %rax
	movq	%rdx, %rcx
	mulq	%r8
	movl	%esi, %eax
	addl	$4, %esi
	shrq	$11, %rdx
	cmpq	$99999, %rcx
	ja	.L1180
.L1178:
	cmpl	$64, %esi
	ja	.L1210
	leal	-1(%rsi), %r13d
.L1175:
	leaq	144(%rsp), %rcx
	movl	$201, %r8d
	leaq	.LC19(%rip), %rdx
	call	memcpy
	movabsq	$2951479051793528259, %r8
	.p2align 4,,10
	.p2align 3
.L1182:
	movq	%rbx, %rdx
	shrq	$2, %rdx
	movq	%rdx, %rax
	mulq	%r8
	movq	%rbx, %rax
	shrq	$2, %rdx
	imulq	$100, %rdx, %rcx
	subq	%rcx, %rax
	movq	%rbx, %rcx
	movq	%rdx, %rbx
	addq	%rax, %rax
	movl	%r13d, %edx
	movzbl	145(%rsp,%rax), %r9d
	movzbl	144(%rsp,%rax), %eax
	movb	%r9b, 67(%rsp,%rdx)
	leal	-1(%r13), %edx
	subl	$2, %r13d
	cmpq	$9999, %rcx
	movb	%al, 67(%rsp,%rdx)
	ja	.L1182
	cmpq	$999, %rcx
	ja	.L1174
.L1172:
	addl	$48, %ebx
.L1183:
	leaq	67(%rsp), %r13
	movb	%bl, 67(%rsp)
	addq	%r13, %rsi
.L1181:
	movzbl	(%rdi), %ebx
	movq	%r13, %rdx
	jmp	.L1170
	.p2align 4,,10
	.p2align 3
.L1153:
	bsrq	%rbx, %rax
	leal	3(%rax), %esi
	movl	$2863311531, %eax
	imulq	%rax, %rsi
	shrq	$33, %rsi
	cmpq	$63, %rbx
	leal	-1(%rsi), %edx
	jbe	.L1185
	.p2align 4,,10
	.p2align 3
.L1186:
	movq	%rbx, %rax
	movl	%edx, %ecx
	andl	$7, %eax
	addl	$48, %eax
	movb	%al, 67(%rsp,%rcx)
	leal	-1(%rdx), %ecx
	movq	%rbx, %rax
	shrq	$6, %rbx
	shrq	$3, %rax
	subl	$2, %edx
	andl	$7, %eax
	addl	$48, %eax
	cmpq	$63, %rbx
	movb	%al, 67(%rsp,%rcx)
	ja	.L1186
.L1185:
	leal	48(%rbx), %edx
	cmpq	$7, %rbx
	jbe	.L1188
	movq	%rbx, %rax
	shrq	$3, %rbx
	andl	$7, %eax
	movq	%rbx, %rdx
	addl	$48, %eax
	addl	$48, %edx
	movb	%al, 68(%rsp)
.L1188:
	leaq	67(%rsp), %r13
	movl	%esi, %esi
	movl	$1, %ecx
	leaq	.LC15(%rip), %r14
	addq	%r13, %rsi
	movl	$1, %eax
	jmp	.L1184
	.p2align 4,,10
	.p2align 3
.L1238:
	movq	%rbx, %rax
	shrq	$4, %rbx
	andl	$15, %eax
	movzbl	144(%rsp,%rax), %eax
	movb	%al, 68(%rsp)
	movzbl	144(%rsp,%rbx), %eax
	jmp	.L1195
.L1240:
	leaq	144(%rsp), %rcx
	movl	$201, %r8d
	movl	$2, %esi
	leaq	.LC19(%rip), %rdx
	call	memcpy
	.p2align 4,,10
	.p2align 3
.L1174:
	addq	%rbx, %rbx
	movzbl	145(%rsp,%rbx), %eax
	movzbl	144(%rsp,%rbx), %ebx
	movb	%al, 68(%rsp)
	jmp	.L1183
	.p2align 4,,10
	.p2align 3
.L1237:
	testq	%r12, %r12
	jne	.L1212
	movzbl	(%rdi), %ebx
	movb	$48, 67(%rsp)
	movl	$1, %ecx
	movl	$2, %eax
	leaq	.LC17(%rip), %r14
	leaq	68(%rsp), %rsi
	leaq	67(%rsp), %r13
	jmp	.L1189
	.p2align 4,,10
	.p2align 3
.L1241:
	leal	5(%rax), %esi
	jmp	.L1178
	.p2align 4,,10
	.p2align 3
.L1242:
	leal	6(%rax), %esi
	jmp	.L1178
	.p2align 4,,10
	.p2align 3
.L1243:
	leal	7(%rax), %esi
	jmp	.L1178
	.p2align 4,,10
	.p2align 3
.L1213:
	leaq	.LC16(%rip), %r14
	jmp	.L1157
.L1210:
	leaq	131(%rsp), %rsi
	leaq	67(%rsp), %r13
	jmp	.L1181
.L1212:
	leaq	.LC17(%rip), %r14
	jmp	.L1157
.L1207:
	movl	$1, %esi
	jmp	.L1172
.L1209:
	movl	$4, %esi
	movl	$3, %r13d
	jmp	.L1175
.L1208:
	movl	$3, %esi
	movl	$2, %r13d
	jmp	.L1175
.L1150:
	leaq	.LC18(%rip), %rcx
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
.LFB5100:
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$360, %rsp
	.seh_stackalloc	360
	.seh_endprologue
	movzbl	1(%rcx), %eax
	movq	%rdx, %rbx
	movl	%eax, %edx
	movq	%rcx, %rdi
	andl	$120, %edx
	movq	%r8, %rbp
	cmpb	$56, %dl
	je	.L1322
	shrb	$3, %al
	andl	$15, %eax
	cmpb	$4, %al
	je	.L1248
	ja	.L1249
	cmpb	$1, %al
	jbe	.L1250
	leaq	.LC13(%rip), %r13
	cmpb	$16, %dl
	leaq	.LC14(%rip), %rax
	cmovne	%rax, %r13
	testq	%rbx, %rbx
	jne	.L1323
	leaq	68(%rsp), %rsi
	movl	$48, %eax
	leaq	67(%rsp), %r12
.L1255:
	movb	%al, 67(%rsp)
	movzbl	(%rdi), %eax
	testb	$16, %al
	je	.L1305
.L1304:
	movq	$-2, %rdx
	movl	$2, %ebx
.L1259:
	addq	%r12, %rdx
	testl	%ebx, %ebx
	movl	%ebx, %r10d
	je	.L1260
	xorl	%ecx, %ecx
.L1288:
	movl	%ecx, %r8d
	addl	$1, %ecx
	movzbl	0(%r13,%r8), %r9d
	cmpl	%r10d, %ecx
	movb	%r9b, (%rdx,%r8)
	jb	.L1288
	jmp	.L1260
	.p2align 4,,10
	.p2align 3
.L1322:
	cmpq	$127, %rbx
	ja	.L1246
	leaq	144(%rsp), %rax
	movl	$1, 32(%rsp)
	movq	%rdi, %r9
	movl	$1, %edx
	leaq	48(%rsp), %rcx
	movb	%bl, 144(%rsp)
	movq	$1, 48(%rsp)
	movq	%rax, 56(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	addq	$360, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L1250:
	testq	%rbx, %rbx
	jne	.L1261
	movb	$48, 67(%rsp)
	leaq	68(%rsp), %rsi
	leaq	67(%rsp), %r12
.L1262:
	movzbl	(%rdi), %eax
	movq	%r12, %rdx
.L1260:
	shrb	$2, %al
	andl	$3, %eax
	cmpl	$1, %eax
	je	.L1324
.L1290:
	cmpl	$3, %eax
	je	.L1306
.L1291:
	leaq	48(%rsp), %rax
	movq	%r12, %r8
	subq	%rdx, %rsi
	movq	%rdx, 56(%rsp)
	subq	%rdx, %r8
	movq	%rbp, %r9
	movq	%rax, %rdx
	movq	%rsi, 48(%rsp)
	movq	%rdi, %rcx
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	addq	$360, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L1248:
	testq	%rbx, %rbx
	je	.L1299
	bsrq	%rbx, %rax
	leal	3(%rax), %esi
	movl	$2863311531, %eax
	imulq	%rax, %rsi
	shrq	$33, %rsi
	cmpq	$63, %rbx
	leal	-1(%rsi), %edx
	jbe	.L1275
	.p2align 4,,10
	.p2align 3
.L1276:
	movq	%rbx, %rax
	movl	%edx, %ecx
	andl	$7, %eax
	addl	$48, %eax
	movb	%al, 67(%rsp,%rcx)
	leal	-1(%rdx), %ecx
	movq	%rbx, %rax
	shrq	$6, %rbx
	shrq	$3, %rax
	subl	$2, %edx
	andl	$7, %eax
	addl	$48, %eax
	cmpq	$63, %rbx
	movb	%al, 67(%rsp,%rcx)
	ja	.L1276
.L1275:
	leal	48(%rbx), %eax
	cmpq	$7, %rbx
	ja	.L1325
.L1278:
	leaq	67(%rsp), %r12
	movl	%esi, %esi
	movl	$1, %edx
	leaq	.LC15(%rip), %r13
	addq	%r12, %rsi
	movl	$1, %ebx
.L1274:
	movb	%al, 67(%rsp)
.L1279:
	movzbl	(%rdi), %eax
	testb	$16, %al
	je	.L1305
	testb	%dl, %dl
	jne	.L1326
.L1305:
	shrb	$2, %al
	movq	%r12, %rdx
	andl	$3, %eax
	cmpl	$1, %eax
	jne	.L1290
.L1324:
	movl	$43, %eax
.L1292:
	movb	%al, -1(%rdx)
	subq	$1, %rdx
	jmp	.L1291
	.p2align 4,,10
	.p2align 3
.L1249:
	cmpb	$40, %dl
	je	.L1327
	testq	%rbx, %rbx
	jne	.L1301
	cmpb	$48, %dl
	movb	$48, 67(%rsp)
	je	.L1302
	leaq	.LC16(%rip), %r13
	leaq	68(%rsp), %rsi
	leaq	67(%rsp), %r12
	jmp	.L1281
	.p2align 4,,10
	.p2align 3
.L1306:
	movl	$32, %eax
	jmp	.L1292
	.p2align 4,,10
	.p2align 3
.L1261:
	cmpq	$9, %rbx
	jbe	.L1295
	cmpq	$99, %rbx
	jbe	.L1328
	cmpq	$999, %rbx
	jbe	.L1296
	cmpq	$9999, %rbx
	jbe	.L1297
	movq	%rbx, %rdx
	movl	$1, %esi
	movabsq	$3777893186295716171, %r8
	jmp	.L1267
	.p2align 4,,10
	.p2align 3
.L1271:
	cmpq	$999999, %rcx
	jbe	.L1329
	cmpq	$9999999, %rcx
	jbe	.L1330
	cmpq	$99999999, %rcx
	jbe	.L1331
.L1267:
	movq	%rdx, %rax
	movq	%rdx, %rcx
	mulq	%r8
	movl	%esi, %eax
	addl	$4, %esi
	shrq	$11, %rdx
	cmpq	$99999, %rcx
	ja	.L1271
.L1269:
	cmpl	$64, %esi
	ja	.L1298
	leal	-1(%rsi), %r12d
.L1266:
	leaq	144(%rsp), %rcx
	movl	$201, %r8d
	leaq	.LC19(%rip), %rdx
	call	memcpy
	movabsq	$2951479051793528259, %r8
	.p2align 4,,10
	.p2align 3
.L1272:
	movq	%rbx, %rdx
	shrq	$2, %rdx
	movq	%rdx, %rax
	mulq	%r8
	movq	%rbx, %rax
	shrq	$2, %rdx
	imulq	$100, %rdx, %rcx
	subq	%rcx, %rax
	movq	%rbx, %rcx
	movq	%rdx, %rbx
	addq	%rax, %rax
	movl	%r12d, %edx
	movzbl	145(%rsp,%rax), %r9d
	movzbl	144(%rsp,%rax), %eax
	movb	%r9b, 67(%rsp,%rdx)
	leal	-1(%r12), %edx
	subl	$2, %r12d
	cmpq	$9999, %rcx
	movb	%al, 67(%rsp,%rdx)
	ja	.L1272
	cmpq	$999, %rcx
	jbe	.L1263
.L1265:
	addq	%rbx, %rbx
	movzbl	145(%rsp,%rbx), %eax
	movzbl	144(%rsp,%rbx), %ebx
	movb	%al, 68(%rsp)
	jmp	.L1273
	.p2align 4,,10
	.p2align 3
.L1323:
	bsrq	%rbx, %r8
	movl	$64, %esi
	movl	$63, %eax
	xorq	$63, %r8
	subl	%r8d, %esi
	subl	%r8d, %eax
	je	.L1258
	movl	%eax, %edx
	leaq	63(%rsp,%rdx), %rcx
	leaq	64(%rsp,%rdx), %rax
	movl	$62, %edx
	subl	%r8d, %edx
	subq	%rdx, %rcx
	.p2align 4,,10
	.p2align 3
.L1257:
	movl	%ebx, %edx
	subq	$1, %rax
	shrq	%rbx
	andl	$1, %edx
	addl	$48, %edx
	movb	%dl, 4(%rax)
	cmpq	%rcx, %rax
	jne	.L1257
.L1258:
	leaq	67(%rsp), %r12
	movslq	%esi, %rsi
	movl	$49, %eax
	addq	%r12, %rsi
	jmp	.L1255
	.p2align 4,,10
	.p2align 3
.L1299:
	movl	$48, %eax
	xorl	%edx, %edx
	xorl	%r13d, %r13d
	leaq	68(%rsp), %rsi
	leaq	67(%rsp), %r12
	jmp	.L1274
	.p2align 4,,10
	.p2align 3
.L1327:
	testq	%rbx, %rbx
	jne	.L1300
	movb	$48, 67(%rsp)
	leaq	.LC17(%rip), %r13
	leaq	68(%rsp), %rsi
	leaq	67(%rsp), %r12
	jmp	.L1281
	.p2align 4,,10
	.p2align 3
.L1301:
	leaq	.LC16(%rip), %r13
.L1280:
	bsrq	%rbx, %rax
	leal	4(%rax), %r9d
	movabsq	$3978425819141910832, %rax
	shrl	$2, %r9d
	movq	%rax, 144(%rsp)
	cmpq	$255, %rbx
	movabsq	$7378413942531504440, %rax
	movq	%rax, 152(%rsp)
	leal	-1(%r9), %eax
	jbe	.L1283
	.p2align 4,,10
	.p2align 3
.L1284:
	movq	%rbx, %r8
	movl	%eax, %ecx
	andl	$15, %r8d
	movzbl	144(%rsp,%r8), %r8d
	movb	%r8b, 67(%rsp,%rcx)
	leal	-1(%rax), %r8d
	movq	%rbx, %rcx
	shrq	$8, %rbx
	shrq	$4, %rcx
	subl	$2, %eax
	andl	$15, %ecx
	cmpq	$255, %rbx
	movzbl	144(%rsp,%rcx), %ecx
	movb	%cl, 67(%rsp,%r8)
	ja	.L1284
.L1283:
	cmpq	$15, %rbx
	ja	.L1332
	movzbl	144(%rsp,%rbx), %eax
.L1286:
	leaq	67(%rsp), %r12
	movl	%r9d, %esi
	movb	%al, 67(%rsp)
	addq	%r12, %rsi
	cmpb	$48, %dl
	je	.L1333
.L1281:
	movzbl	(%rdi), %eax
	testb	$16, %al
	jne	.L1304
	jmp	.L1305
	.p2align 4,,10
	.p2align 3
.L1332:
	movq	%rbx, %rax
	shrq	$4, %rbx
	andl	$15, %eax
	movzbl	144(%rsp,%rax), %eax
	movb	%al, 68(%rsp)
	movzbl	144(%rsp,%rbx), %eax
	jmp	.L1286
	.p2align 4,,10
	.p2align 3
.L1325:
	movq	%rbx, %rax
	andl	$7, %eax
	addl	$48, %eax
	movb	%al, 68(%rsp)
	movq	%rbx, %rax
	shrq	$3, %rax
	addl	$48, %eax
	jmp	.L1278
.L1295:
	movl	$1, %esi
	.p2align 4,,10
	.p2align 3
.L1263:
	addl	$48, %ebx
.L1273:
	leaq	67(%rsp), %r12
	movb	%bl, 67(%rsp)
	addq	%r12, %rsi
	jmp	.L1262
	.p2align 4,,10
	.p2align 3
.L1300:
	leaq	.LC17(%rip), %r13
	jmp	.L1280
	.p2align 4,,10
	.p2align 3
.L1302:
	leaq	68(%rsp), %rsi
	leaq	.LC16(%rip), %r13
	leaq	67(%rsp), %r12
.L1282:
	movq	%r12, %rbx
	.p2align 4,,10
	.p2align 3
.L1287:
	movsbl	(%rbx), %ecx
	addq	$1, %rbx
	call	toupper
	movb	%al, -1(%rbx)
	cmpq	%rsi, %rbx
	jne	.L1287
	movl	$1, %edx
	movl	$2, %ebx
	jmp	.L1279
	.p2align 4,,10
	.p2align 3
.L1333:
	testl	%r9d, %r9d
	jne	.L1282
	movl	$1, %edx
	movl	$2, %ebx
	movq	%r12, %rsi
	jmp	.L1279
	.p2align 4,,10
	.p2align 3
.L1329:
	leal	5(%rax), %esi
	jmp	.L1269
	.p2align 4,,10
	.p2align 3
.L1330:
	leal	6(%rax), %esi
	jmp	.L1269
	.p2align 4,,10
	.p2align 3
.L1331:
	leal	7(%rax), %esi
	jmp	.L1269
	.p2align 4,,10
	.p2align 3
.L1326:
	movq	%rbx, %rdx
	negq	%rdx
	jmp	.L1259
.L1298:
	leaq	131(%rsp), %rsi
	leaq	67(%rsp), %r12
	jmp	.L1262
.L1328:
	leaq	144(%rsp), %rcx
	movl	$201, %r8d
	movl	$2, %esi
	leaq	.LC19(%rip), %rdx
	call	memcpy
	jmp	.L1265
.L1296:
	movl	$3, %esi
	movl	$2, %r12d
	jmp	.L1266
.L1297:
	movl	$4, %esi
	movl	$3, %r12d
	jmp	.L1266
.L1246:
	leaq	.LC18(%rip), %rcx
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
.LFB5120:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$504, %rsp
	.seh_stackalloc	504
	.seh_endprologue
	movzbl	1(%rcx), %eax
	movq	(%rdx), %r12
	movq	8(%rdx), %r13
	movl	%eax, %edx
	movq	%rcx, 576(%rsp)
	andl	$120, %edx
	movq	%r8, 592(%rsp)
	cmpb	$56, %dl
	je	.L1428
	shrb	$3, %al
	movq	%r12, %rsi
	movq	%r13, %rdi
	andl	$15, %eax
	testq	%r13, %r13
	js	.L1429
	cmpb	$4, %al
	je	.L1344
	ja	.L1345
	cmpb	$1, %al
	jbe	.L1346
	leaq	.LC14(%rip), %rax
	cmpb	$16, %dl
	leaq	.LC13(%rip), %rbx
	cmovne	%rax, %rbx
	movq	%r12, %rax
	orq	%r13, %rax
	jne	.L1342
	leaq	148(%rsp), %rdi
	movl	$48, %eax
	leaq	147(%rsp), %r8
.L1351:
	movb	%al, 147(%rsp)
	movq	576(%rsp), %rax
	movzbl	(%rax), %edx
	testb	$16, %dl
	je	.L1409
.L1408:
	movq	$-2, %rcx
	movl	$2, %eax
.L1356:
	addq	%r8, %rcx
	testl	%eax, %eax
	movl	%eax, %r11d
	je	.L1357
	xorl	%eax, %eax
.L1388:
	movl	%eax, %r9d
	addl	$1, %eax
	movzbl	(%rbx,%r9), %r10d
	cmpl	%r11d, %eax
	movb	%r10b, (%rcx,%r9)
	jb	.L1388
.L1357:
	leaq	-1(%rcx), %rax
	shrb	$2, %dl
	andl	$3, %edx
	testq	%r13, %r13
	jns	.L1358
.L1436:
	movb	$45, -1(%rcx)
	movq	%rax, %rcx
.L1390:
	subq	%rcx, %rdi
	movq	%rcx, 136(%rsp)
	subq	%rcx, %r8
	movq	592(%rsp), %r9
	movq	576(%rsp), %rcx
	leaq	128(%rsp), %rdx
	movq	%rdi, 128(%rsp)
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L1337
	.p2align 4,,10
	.p2align 3
.L1429:
	negq	%rsi
	adcq	$0, %rdi
	negq	%rdi
	cmpb	$4, %al
	je	.L1339
	ja	.L1340
	cmpb	$1, %al
	jbe	.L1341
	leaq	.LC13(%rip), %rbx
	cmpb	$16, %dl
	leaq	.LC14(%rip), %rax
	cmovne	%rax, %rbx
.L1342:
	testq	%rdi, %rdi
	jne	.L1430
	bsrq	%rsi, %rdx
	movl	$128, %eax
	movl	$127, %ecx
	xorq	$63, %rdx
	addl	$64, %edx
	subl	%edx, %eax
	subl	%edx, %ecx
	je	.L1397
.L1353:
	movl	%ecx, %r8d
	subl	$1, %ecx
	leaq	144(%rsp,%r8), %rdx
	leaq	143(%rsp,%r8), %r8
	subq	%rcx, %r8
	.p2align 4,,10
	.p2align 3
.L1355:
	movl	%esi, %ecx
	subq	$1, %rdx
	shrdq	$1, %rdi, %rsi
	andl	$1, %ecx
	shrq	%rdi
	addl	$48, %ecx
	movb	%cl, 4(%rdx)
	cmpq	%r8, %rdx
	jne	.L1355
.L1354:
	leaq	147(%rsp), %r8
	cltq
	leaq	(%r8,%rax), %rdi
	movl	$49, %eax
	jmp	.L1351
	.p2align 4,,10
	.p2align 3
.L1428:
	movl	$127, %eax
	cmpq	%r12, %rax
	movl	$0, %eax
	sbbq	%r13, %rax
	jl	.L1336
	movq	576(%rsp), %r9
	leaq	288(%rsp), %rax
	movl	$1, 32(%rsp)
	movl	$1, %edx
	leaq	128(%rsp), %rcx
	movb	%r12b, 288(%rsp)
	movq	$1, 128(%rsp)
	movq	%rax, 136(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1337:
	addq	$504, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L1345:
	cmpb	$40, %dl
	je	.L1431
	movq	%r12, %rax
	orq	%r13, %rax
	jne	.L1405
	cmpb	$48, %dl
	movb	$48, 147(%rsp)
	je	.L1406
	leaq	.LC16(%rip), %rbx
	leaq	148(%rsp), %rdi
	leaq	147(%rsp), %r8
	jmp	.L1379
	.p2align 4,,10
	.p2align 3
.L1340:
	leaq	.LC17(%rip), %rbx
	cmpb	$40, %dl
	leaq	.LC16(%rip), %rax
	cmovne	%rax, %rbx
.L1343:
	testq	%rdi, %rdi
	jne	.L1432
	bsrq	%rsi, %rax
	movl	$255, %ecx
	leal	4(%rax), %ebp
	movabsq	$3978425819141910832, %rax
	shrl	$2, %ebp
	movq	%rax, 288(%rsp)
	cmpq	%rsi, %rcx
	movabsq	$7378413942531504440, %rax
	movq	%rax, 296(%rsp)
	leal	-1(%rbp), %eax
	jnb	.L1433
.L1382:
	leaq	288(%rsp), %rcx
	movl	$255, %r11d
	xorl	%r10d, %r10d
	.p2align 4,,10
	.p2align 3
.L1384:
	movq	%rsi, %r8
	movl	%eax, %r14d
	movq	%r10, %r15
	leal	-1(%rax), %r9d
	andl	$15, %r8d
	subl	$2, %eax
	addq	%rcx, %r8
	movzbl	(%r8), %r8d
	movb	%r8b, 147(%rsp,%r14)
	movq	%rsi, %r8
	shrdq	$8, %rdi, %rsi
	shrdq	$4, %rdi, %r8
	shrq	$8, %rdi
	movq	%r8, %r14
	andl	$15, %r14d
	cmpq	%rsi, %r11
	leaq	(%r14,%rcx), %r8
	sbbq	%rdi, %r15
	movzbl	(%r8), %r8d
	movb	%r8b, 147(%rsp,%r9)
	jc	.L1384
.L1383:
	movl	$15, %eax
	cmpq	%rsi, %rax
	movl	$0, %eax
	sbbq	%rdi, %rax
	jc	.L1434
	addq	%rsi, %rcx
	movzbl	(%rcx), %eax
.L1386:
	leaq	147(%rsp), %r8
	movl	%ebp, %edi
	movb	%al, 147(%rsp)
	addq	%r8, %rdi
	cmpb	$48, %dl
	je	.L1435
.L1379:
	movq	576(%rsp), %rax
	movzbl	(%rax), %edx
	testb	$16, %dl
	jne	.L1408
	.p2align 4,,10
	.p2align 3
.L1409:
	shrb	$2, %dl
	movq	%r8, %rcx
	leaq	-1(%rcx), %rax
	andl	$3, %edx
	testq	%r13, %r13
	js	.L1436
.L1358:
	movzbl	%dl, %edx
	cmpl	$1, %edx
	je	.L1437
	cmpl	$3, %edx
	jne	.L1390
	movb	$32, -1(%rcx)
.L1393:
	movq	%rax, %rcx
	jmp	.L1390
	.p2align 4,,10
	.p2align 3
.L1437:
	movb	$43, -1(%rcx)
	jmp	.L1393
	.p2align 4,,10
	.p2align 3
.L1344:
	movq	%r12, %rax
	orq	%r13, %rax
	jne	.L1339
	xorl	%ecx, %ecx
	xorl	%eax, %eax
	xorl	%ebx, %ebx
	leaq	148(%rsp), %rdi
	movl	$48, %esi
	leaq	147(%rsp), %r8
.L1371:
	movb	%sil, 147(%rsp)
.L1378:
	movq	576(%rsp), %rsi
	movzbl	(%rsi), %edx
	testb	$16, %dl
	je	.L1409
	testb	%cl, %cl
	je	.L1409
	movq	%rax, %rcx
	negq	%rcx
	jmp	.L1356
	.p2align 4,,10
	.p2align 3
.L1346:
	movq	%r12, %rax
	orq	%r13, %rax
	jne	.L1341
	movq	576(%rsp), %rax
	leaq	147(%rsp), %r8
	movb	$48, 147(%rsp)
	leaq	148(%rsp), %rdi
	movq	%r8, %rcx
	movzbl	(%rax), %eax
	movl	%eax, %edx
	movb	%al, 48(%rsp)
	leaq	146(%rsp), %rax
	shrb	$2, %dl
	andl	$3, %edx
	jmp	.L1358
	.p2align 4,,10
	.p2align 3
.L1341:
	xorl	%eax, %eax
	movl	$9, %edx
	cmpq	%rsi, %rdx
	movq	%rax, %rbx
	sbbq	%rdi, %rbx
	jnc	.L1399
	movl	$99, %edx
	movq	%rax, %rbx
	cmpq	%rsi, %rdx
	sbbq	%rdi, %rbx
	jnc	.L1438
	movl	$999, %edx
	movq	%rax, %rbx
	cmpq	%rsi, %rdx
	sbbq	%rdi, %rbx
	jnc	.L1400
	movl	$9999, %edx
	cmpq	%rsi, %rdx
	sbbq	%rdi, %rax
	jnc	.L1401
	leaq	112(%rsp), %rax
	movq	%rdi, %rdx
	movq	%rdi, 72(%rsp)
	movq	%rsi, %rcx
	leaq	96(%rsp), %rbx
	movq	%r13, 88(%rsp)
	xorl	%r15d, %r15d
	movq	%rax, %r13
	movl	$1, %r14d
	movq	%rsi, 64(%rsp)
	movq	%rbx, %rdi
	movq	%r12, 80(%rsp)
	jmp	.L1363
	.p2align 4,,10
	.p2align 3
.L1367:
	movl	$999999, %eax
	cmpq	%rbp, %rax
	movq	%r15, %rax
	sbbq	%rbx, %rax
	jnc	.L1439
	movl	$9999999, %eax
	cmpq	%rbp, %rax
	movq	%r15, %rax
	sbbq	%rbx, %rax
	jnc	.L1440
	movl	$99999999, %eax
	cmpq	%rbp, %rax
	movq	%r15, %rax
	sbbq	%rbx, %rax
	jnc	.L1441
.L1363:
	movq	%rcx, %rbp
	movq	%rdx, %rbx
	movq	%rcx, 112(%rsp)
	movq	%r13, %rcx
	movq	%rdx, 120(%rsp)
	movq	%rdi, %rdx
	movq	$10000, 96(%rsp)
	movq	$0, 104(%rsp)
	call	__udivti3
	movl	$99999, %eax
	movl	%r14d, %r9d
	addl	$4, %r14d
	cmpq	%rbp, %rax
	movq	%r15, %rax
	movaps	%xmm0, 48(%rsp)
	movq	48(%rsp), %rcx
	sbbq	%rbx, %rax
	movq	56(%rsp), %rdx
	jc	.L1367
	movq	64(%rsp), %rsi
	movq	72(%rsp), %rdi
	movq	80(%rsp), %r12
	movq	88(%rsp), %r13
.L1365:
	cmpl	$128, %r14d
	ja	.L1402
	leal	-1(%r14), %ebx
	movl	%r14d, %ebp
.L1362:
	leaq	288(%rsp), %rcx
	movl	$201, %r8d
	movabsq	$1152921504606846975, %r14
	leaq	.LC19(%rip), %rdx
	movabsq	$-8116567392432202711, %r15
	call	memcpy
	movq	%r13, 72(%rsp)
	movl	%ebx, %r9d
	movq	%rbp, %r13
	movq	%r12, 64(%rsp)
	movq	%rax, %rbp
	.p2align 4,,10
	.p2align 3
.L1369:
	movq	%rsi, %rax
	movq	%rsi, %rcx
	xorl	%ebx, %ebx
	shrdq	$60, %rdi, %rax
	andq	%r14, %rcx
	movl	$25, %r12d
	andq	%r14, %rax
	addq	%rax, %rcx
	movq	%rdi, %rax
	shrq	$56, %rax
	addq	%rax, %rcx
	movabsq	$5165088340638674453, %rax
	mulq	%rcx
	movq	%rcx, %rax
	subq	%rdx, %rax
	shrq	%rax
	addq	%rax, %rdx
	shrq	$4, %rdx
	leaq	(%rdx,%rdx,4), %rax
	movq	%rdi, %rdx
	leaq	(%rax,%rax,4), %rax
	subq	%rax, %rcx
	movq	%rsi, %rax
	subq	%rcx, %rax
	sbbq	%rbx, %rdx
	movq	%rdx, %r8
	movabsq	$2951479051793528258, %rdx
	imulq	%rax, %rdx
	imulq	%r15, %r8
	addq	%rdx, %r8
	mulq	%r15
	movq	%rax, %r10
	movq	%rdx, %r11
	andl	$3, %eax
	xorl	%edx, %edx
	addq	%r8, %r11
	imulq	$25, %rdx, %r8
	mulq	%r12
	addq	%r8, %rdx
	addq	%rcx, %rax
	movq	%rsi, %r8
	adcq	%rbx, %rdx
	movq	%r10, %rsi
	movl	%r9d, %ecx
	shldq	$1, %rax, %rdx
	addq	%rax, %rax
	shrdq	$2, %r11, %rsi
	movq	%rax, 48(%rsp)
	movq	48(%rsp), %rax
	movq	%rdx, 56(%rsp)
	movq	%rdi, %rdx
	movq	%r11, %rdi
	shrq	$2, %rdi
	leaq	0(%rbp,%rax), %r10
	addq	%rbp, %rax
	movzbl	1(%r10), %r10d
	movzbl	(%rax), %eax
	movb	%r10b, 147(%rsp,%rcx)
	leal	-1(%r9), %ecx
	subl	$2, %r9d
	movb	%al, 147(%rsp,%rcx)
	movl	$9999, %eax
	cmpq	%r8, %rax
	movl	$0, %eax
	sbbq	%rdx, %rax
	jc	.L1369
	movl	$999, %eax
	movq	%rbp, %rcx
	movq	%r13, %rbp
	movq	72(%rsp), %r13
	cmpq	%r8, %rax
	movl	$0, %eax
	sbbq	%rdx, %rax
	jnc	.L1359
.L1361:
	addq	%rsi, %rsi
	leaq	(%rcx,%rsi), %rax
	addq	%rcx, %rsi
	movzbl	1(%rax), %eax
	movzbl	(%rsi), %esi
	movb	%al, 148(%rsp)
.L1370:
	leaq	147(%rsp), %r8
	movb	%sil, 147(%rsp)
	leaq	(%r8,%rbp), %rdi
.L1368:
	movq	576(%rsp), %rax
	movq	%r8, %rcx
	movzbl	(%rax), %edx
	jmp	.L1357
	.p2align 4,,10
	.p2align 3
.L1339:
	testq	%rdi, %rdi
	jne	.L1442
	bsrq	%rsi, %rax
	movl	$2863311531, %edx
	movl	$63, %ecx
	addl	$3, %eax
	imulq	%rdx, %rax
	shrq	$33, %rax
	cmpq	%rsi, %rcx
	leal	-1(%rax), %edx
	jnb	.L1374
.L1373:
	movl	$63, %r9d
	xorl	%r8d, %r8d
	.p2align 4,,10
	.p2align 3
.L1375:
	movq	%rsi, %rcx
	movl	%edx, %r10d
	movq	%r8, %rbx
	andl	$7, %ecx
	addl	$48, %ecx
	movb	%cl, 147(%rsp,%r10)
	leal	-1(%rdx), %r10d
	movq	%rsi, %rcx
	shrdq	$6, %rdi, %rsi
	shrdq	$3, %rdi, %rcx
	subl	$2, %edx
	shrq	$6, %rdi
	andl	$7, %ecx
	addl	$48, %ecx
	cmpq	%rsi, %r9
	sbbq	%rdi, %rbx
	movb	%cl, 147(%rsp,%r10)
	jc	.L1375
.L1374:
	movl	$7, %edx
	cmpq	%rsi, %rdx
	movl	$0, %edx
	sbbq	%rdi, %rdx
	jc	.L1443
	addl	$48, %esi
.L1377:
	leaq	147(%rsp), %r8
	movl	%eax, %eax
	movl	$1, %ecx
	leaq	(%r8,%rax), %rdi
	movl	$1, %eax
	leaq	.LC15(%rip), %rbx
	jmp	.L1371
	.p2align 4,,10
	.p2align 3
.L1443:
	movq	%rsi, %rcx
	shrdq	$3, %rdi, %rsi
	andl	$7, %ecx
	addl	$48, %esi
	addl	$48, %ecx
	movb	%cl, 148(%rsp)
	jmp	.L1377
	.p2align 4,,10
	.p2align 3
.L1434:
	movq	%rsi, %r8
	shrdq	$4, %rdi, %rsi
	andl	$15, %r8d
	addq	%rcx, %rsi
	addq	%rcx, %r8
	movzbl	(%r8), %eax
	movb	%al, 148(%rsp)
	movzbl	(%rsi), %eax
	jmp	.L1386
	.p2align 4,,10
	.p2align 3
.L1406:
	leaq	148(%rsp), %rdi
	leaq	.LC16(%rip), %rbx
	leaq	147(%rsp), %r8
.L1380:
	movq	%r8, %rsi
	movq	%r8, %rbp
	.p2align 4,,10
	.p2align 3
.L1387:
	movsbl	(%rsi), %ecx
	addq	$1, %rsi
	call	toupper
	movb	%al, -1(%rsi)
	cmpq	%rdi, %rsi
	jne	.L1387
	movq	%rbp, %r8
	movl	$1, %ecx
	movl	$2, %eax
	jmp	.L1378
	.p2align 4,,10
	.p2align 3
.L1432:
	bsrq	%rdi, %rax
	leal	68(%rax), %ebp
	movabsq	$3978425819141910832, %rax
	shrl	$2, %ebp
	movq	%rax, 288(%rsp)
	movabsq	$7378413942531504440, %rax
	movq	%rax, 296(%rsp)
	leal	-1(%rbp), %eax
	jmp	.L1382
	.p2align 4,,10
	.p2align 3
.L1430:
	bsrq	%rdi, %rdx
	movl	$128, %eax
	movl	$127, %ecx
	xorq	$63, %rdx
	subl	%edx, %eax
	subl	%edx, %ecx
	jmp	.L1353
	.p2align 4,,10
	.p2align 3
.L1442:
	bsrq	%rdi, %rax
	movl	$2863311531, %edx
	addl	$67, %eax
	imulq	%rdx, %rax
	shrq	$33, %rax
	leal	-1(%rax), %edx
	jmp	.L1373
.L1397:
	movl	$1, %eax
	jmp	.L1354
.L1399:
	movl	$1, %ebp
	.p2align 4,,10
	.p2align 3
.L1359:
	addl	$48, %esi
	jmp	.L1370
	.p2align 4,,10
	.p2align 3
.L1435:
	testl	%ebp, %ebp
	jne	.L1380
	movl	$1, %ecx
	movl	$2, %eax
	movq	%r8, %rdi
	jmp	.L1378
	.p2align 4,,10
	.p2align 3
.L1431:
	movq	%r12, %rax
	orq	%r13, %rax
	jne	.L1404
	movb	$48, 147(%rsp)
	leaq	.LC17(%rip), %rbx
	leaq	148(%rsp), %rdi
	leaq	147(%rsp), %r8
	jmp	.L1379
	.p2align 4,,10
	.p2align 3
.L1439:
	movq	64(%rsp), %rsi
	leal	5(%r9), %r14d
	movq	72(%rsp), %rdi
	movq	80(%rsp), %r12
	movq	88(%rsp), %r13
	jmp	.L1365
	.p2align 4,,10
	.p2align 3
.L1440:
	movq	64(%rsp), %rsi
	leal	6(%r9), %r14d
	movq	72(%rsp), %rdi
	movq	80(%rsp), %r12
	movq	88(%rsp), %r13
	jmp	.L1365
	.p2align 4,,10
	.p2align 3
.L1441:
	movq	64(%rsp), %rsi
	leal	7(%r9), %r14d
	movq	72(%rsp), %rdi
	movq	80(%rsp), %r12
	movq	88(%rsp), %r13
	jmp	.L1365
	.p2align 4,,10
	.p2align 3
.L1405:
	leaq	.LC16(%rip), %rbx
	jmp	.L1343
	.p2align 4,,10
	.p2align 3
.L1433:
	leaq	288(%rsp), %rcx
	jmp	.L1383
.L1402:
	leaq	275(%rsp), %rdi
	leaq	147(%rsp), %r8
	jmp	.L1368
.L1404:
	leaq	.LC17(%rip), %rbx
	jmp	.L1343
.L1438:
	leaq	288(%rsp), %rcx
	movl	$201, %r8d
	movl	$2, %ebp
	leaq	.LC19(%rip), %rdx
	call	memcpy
	movq	%rax, %rcx
	jmp	.L1361
.L1401:
	movl	$4, %ebp
	movl	$3, %ebx
	jmp	.L1362
.L1400:
	movl	$3, %ebp
	movl	$2, %ebx
	jmp	.L1362
.L1336:
	leaq	.LC18(%rip), %rcx
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
.LFB5122:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$488, %rsp
	.seh_stackalloc	488
	.seh_endprologue
	movzbl	1(%rcx), %eax
	movq	(%rdx), %rsi
	movq	8(%rdx), %rdi
	movl	%eax, %edx
	movq	%rcx, %r12
	movq	%r8, %r13
	andl	$120, %edx
	cmpb	$56, %dl
	je	.L1529
	shrb	$3, %al
	andl	$15, %eax
	cmpb	$4, %al
	je	.L1448
	ja	.L1449
	cmpb	$1, %al
	ja	.L1530
	movq	%rsi, %rax
	orq	%rdi, %rax
	jne	.L1462
	movb	$48, 131(%rsp)
	leaq	132(%rsp), %rdi
	leaq	131(%rsp), %r8
.L1463:
	movzbl	(%r12), %eax
	movq	%r8, %rdx
.L1461:
	shrb	$2, %al
	andl	$3, %eax
	cmpl	$1, %eax
	je	.L1531
.L1495:
	cmpl	$3, %eax
	je	.L1512
.L1496:
	leaq	112(%rsp), %rax
	subq	%rdx, %rdi
	movq	%rdx, 120(%rsp)
	subq	%rdx, %r8
	movq	%r13, %r9
	movq	%rax, %rdx
	movq	%r12, %rcx
	movq	%rdi, 112(%rsp)
	call	_ZNKSt8__format15__formatter_intIcE13_M_format_intINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorESt17basic_string_viewIcSt11char_traitsIcEEyRS7_
	jmp	.L1447
	.p2align 4,,10
	.p2align 3
.L1529:
	movl	$127, %eax
	cmpq	%rsi, %rax
	movl	$0, %eax
	sbbq	%rdi, %rax
	jc	.L1446
	leaq	272(%rsp), %rax
	movl	$1, 32(%rsp)
	movq	%r12, %r9
	movl	$1, %edx
	leaq	112(%rsp), %rcx
	movb	%sil, 272(%rsp)
	movq	$1, 112(%rsp)
	movq	%rax, 120(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
.L1447:
	addq	$488, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L1530:
	leaq	.LC14(%rip), %rax
	cmpb	$16, %dl
	leaq	.LC13(%rip), %rbx
	cmovne	%rax, %rbx
	movq	%rsi, %rax
	orq	%rdi, %rax
	je	.L1498
	testq	%rdi, %rdi
	jne	.L1532
	bsrq	%rsi, %rax
	movl	$128, %r9d
	movl	$127, %edx
	xorq	$63, %rax
	addl	$64, %eax
	subl	%eax, %r9d
	subl	%eax, %edx
	je	.L1499
.L1457:
	movl	%edx, %ecx
	subl	$1, %edx
	leaq	128(%rsp,%rcx), %rax
	leaq	127(%rsp,%rcx), %rcx
	subq	%rdx, %rcx
	.p2align 4,,10
	.p2align 3
.L1459:
	movl	%esi, %edx
	subq	$1, %rax
	shrdq	$1, %rdi, %rsi
	andl	$1, %edx
	shrq	%rdi
	addl	$48, %edx
	movb	%dl, 4(%rax)
	cmpq	%rcx, %rax
	jne	.L1459
.L1458:
	leaq	131(%rsp), %r8
	movslq	%r9d, %rdi
	movl	$49, %eax
	addq	%r8, %rdi
.L1455:
	movb	%al, 131(%rsp)
	movzbl	(%r12), %eax
	testb	$16, %al
	je	.L1511
.L1510:
	movq	$-2, %rdx
	movl	$2, %ecx
.L1460:
	addq	%r8, %rdx
	testl	%ecx, %ecx
	movl	%ecx, %r11d
	je	.L1461
	xorl	%ecx, %ecx
.L1493:
	movl	%ecx, %r9d
	addl	$1, %ecx
	movzbl	(%rbx,%r9), %r10d
	cmpl	%r11d, %ecx
	movb	%r10b, (%rdx,%r9)
	jb	.L1493
	jmp	.L1461
	.p2align 4,,10
	.p2align 3
.L1448:
	movq	%rsi, %rax
	orq	%rdi, %rax
	je	.L1505
	testq	%rdi, %rdi
	jne	.L1533
	bsrq	%rsi, %rax
	movl	$2863311531, %edx
	movl	$63, %ecx
	addl	$3, %eax
	imulq	%rdx, %rax
	shrq	$33, %rax
	cmpq	%rsi, %rcx
	leal	-1(%rax), %edx
	jnb	.L1478
.L1477:
	movl	$63, %r9d
	xorl	%r8d, %r8d
	.p2align 4,,10
	.p2align 3
.L1479:
	movq	%rsi, %rcx
	movl	%edx, %r10d
	movq	%r8, %rbx
	andl	$7, %ecx
	addl	$48, %ecx
	movb	%cl, 131(%rsp,%r10)
	leal	-1(%rdx), %r10d
	movq	%rsi, %rcx
	shrdq	$6, %rdi, %rsi
	shrdq	$3, %rdi, %rcx
	subl	$2, %edx
	shrq	$6, %rdi
	andl	$7, %ecx
	addl	$48, %ecx
	cmpq	%rsi, %r9
	sbbq	%rdi, %rbx
	movb	%cl, 131(%rsp,%r10)
	jc	.L1479
.L1478:
	movl	$7, %edx
	cmpq	%rsi, %rdx
	movl	$0, %edx
	sbbq	%rdi, %rdx
	jc	.L1534
	addl	$48, %esi
.L1481:
	leaq	131(%rsp), %r8
	movl	%eax, %edi
	movl	$1, %edx
	leaq	.LC15(%rip), %rbx
	addq	%r8, %rdi
	movl	$1, %ecx
	jmp	.L1475
	.p2align 4,,10
	.p2align 3
.L1505:
	movl	$48, %esi
	xorl	%edx, %edx
	xorl	%ebx, %ebx
	leaq	132(%rsp), %rdi
	xorl	%ecx, %ecx
	leaq	131(%rsp), %r8
.L1475:
	movb	%sil, 131(%rsp)
.L1482:
	movzbl	(%r12), %eax
	testb	$16, %al
	je	.L1511
	testb	%dl, %dl
	jne	.L1535
.L1511:
	shrb	$2, %al
	movq	%r8, %rdx
	andl	$3, %eax
	cmpl	$1, %eax
	jne	.L1495
.L1531:
	movl	$43, %eax
.L1497:
	movb	%al, -1(%rdx)
	subq	$1, %rdx
	jmp	.L1496
	.p2align 4,,10
	.p2align 3
.L1449:
	cmpb	$40, %dl
	je	.L1536
	movq	%rsi, %rax
	orq	%rdi, %rax
	jne	.L1507
	cmpb	$48, %dl
	movb	$48, 131(%rsp)
	je	.L1508
	leaq	.LC16(%rip), %rbx
	leaq	132(%rsp), %rdi
	leaq	131(%rsp), %r8
	jmp	.L1484
	.p2align 4,,10
	.p2align 3
.L1512:
	movl	$32, %eax
	jmp	.L1497
	.p2align 4,,10
	.p2align 3
.L1498:
	leaq	132(%rsp), %rdi
	movl	$48, %eax
	leaq	131(%rsp), %r8
	jmp	.L1455
	.p2align 4,,10
	.p2align 3
.L1462:
	xorl	%eax, %eax
	movl	$9, %edx
	cmpq	%rsi, %rdx
	movq	%rax, %rbx
	sbbq	%rdi, %rbx
	jnc	.L1501
	movl	$99, %edx
	movq	%rax, %rbx
	cmpq	%rsi, %rdx
	sbbq	%rdi, %rbx
	jnc	.L1537
	movl	$999, %edx
	movq	%rax, %rbx
	cmpq	%rsi, %rdx
	sbbq	%rdi, %rbx
	jnc	.L1502
	movl	$9999, %edx
	cmpq	%rsi, %rdx
	sbbq	%rdi, %rax
	jnc	.L1503
	movl	$1, %ebp
	movq	%rdi, %rdx
	movq	%rdi, 72(%rsp)
	movq	%r12, %r13
	leaq	96(%rsp), %r15
	movl	%ebp, %edi
	movq	%rsi, %rcx
	movq	%rsi, 64(%rsp)
	leaq	80(%rsp), %rax
	xorl	%r14d, %r14d
	movq	%r8, 576(%rsp)
	movq	%r15, %r12
	movq	%rax, %rbp
	jmp	.L1468
	.p2align 4,,10
	.p2align 3
.L1472:
	movl	$999999, %eax
	cmpq	%r15, %rax
	movq	%r14, %rax
	sbbq	%rbx, %rax
	jnc	.L1538
	movl	$9999999, %eax
	cmpq	%r15, %rax
	movq	%r14, %rax
	sbbq	%rbx, %rax
	jnc	.L1539
	movl	$99999999, %eax
	cmpq	%r15, %rax
	movq	%r14, %rax
	sbbq	%rbx, %rax
	jnc	.L1540
.L1468:
	movq	%rcx, %r15
	movq	%rdx, %rbx
	movq	%rcx, 96(%rsp)
	movq	%r12, %rcx
	movq	%rdx, 104(%rsp)
	movq	%rbp, %rdx
	movq	$10000, 80(%rsp)
	movq	$0, 88(%rsp)
	call	__udivti3
	movl	$99999, %eax
	movl	%edi, %r9d
	addl	$4, %edi
	cmpq	%r15, %rax
	movq	%r14, %rax
	movaps	%xmm0, 48(%rsp)
	movq	48(%rsp), %rcx
	sbbq	%rbx, %rax
	movq	56(%rsp), %rdx
	jc	.L1472
	movl	%edi, %ebp
	movq	%r13, %r12
	movq	64(%rsp), %rsi
	movq	72(%rsp), %rdi
	movq	576(%rsp), %r13
.L1470:
	cmpl	$128, %ebp
	ja	.L1504
	leal	-1(%rbp), %ebx
.L1467:
	leaq	272(%rsp), %rcx
	movl	$201, %r8d
	movabsq	$1152921504606846975, %r15
	leaq	.LC19(%rip), %rdx
	movabsq	$-8116567392432202711, %r14
	call	memcpy
	movq	%rbp, 64(%rsp)
	movq	%rax, %rcx
	movq	%r12, 560(%rsp)
	.p2align 4,,10
	.p2align 3
.L1473:
	movq	%rsi, %rax
	movq	%rsi, %r8
	xorl	%r9d, %r9d
	shrdq	$60, %rdi, %rax
	andq	%r15, %r8
	movl	$25, %r12d
	andq	%r15, %rax
	addq	%rax, %r8
	movq	%rdi, %rax
	shrq	$56, %rax
	addq	%rax, %r8
	movabsq	$5165088340638674453, %rax
	mulq	%r8
	movq	%r8, %rax
	subq	%rdx, %rax
	shrq	%rax
	addq	%rax, %rdx
	shrq	$4, %rdx
	leaq	(%rdx,%rdx,4), %rax
	movq	%rdi, %rdx
	leaq	(%rax,%rax,4), %rax
	subq	%rax, %r8
	movq	%rsi, %rax
	subq	%r8, %rax
	sbbq	%r9, %rdx
	movq	%rdx, %rbp
	movabsq	$2951479051793528258, %rdx
	imulq	%rax, %rdx
	imulq	%r14, %rbp
	addq	%rdx, %rbp
	mulq	%r14
	movq	%rax, %r10
	movq	%rdx, %r11
	andl	$3, %eax
	xorl	%edx, %edx
	addq	%rbp, %r11
	imulq	$25, %rdx, %rbp
	mulq	%r12
	addq	%rbp, %rdx
	addq	%r8, %rax
	movq	%rsi, %r8
	adcq	%r9, %rdx
	movq	%r10, %rsi
	movl	%ebx, %r9d
	shldq	$1, %rax, %rdx
	addq	%rax, %rax
	shrdq	$2, %r11, %rsi
	movq	%rax, 48(%rsp)
	movq	48(%rsp), %rax
	movq	%rdx, 56(%rsp)
	movq	%rdi, %rdx
	movq	%r11, %rdi
	shrq	$2, %rdi
	leaq	(%rcx,%rax), %r10
	addq	%rcx, %rax
	movzbl	1(%r10), %r10d
	movzbl	(%rax), %eax
	movb	%r10b, 131(%rsp,%r9)
	leal	-1(%rbx), %r9d
	subl	$2, %ebx
	movb	%al, 131(%rsp,%r9)
	movl	$9999, %eax
	cmpq	%r8, %rax
	movl	$0, %eax
	sbbq	%rdx, %rax
	jc	.L1473
	movl	$999, %eax
	movq	64(%rsp), %rbp
	cmpq	%r8, %rax
	movl	$0, %eax
	movq	560(%rsp), %r12
	sbbq	%rdx, %rax
	jnc	.L1464
.L1466:
	addq	%rsi, %rsi
	leaq	(%rcx,%rsi), %rax
	addq	%rcx, %rsi
	movzbl	1(%rax), %eax
	movzbl	(%rsi), %esi
	movb	%al, 132(%rsp)
.L1474:
	leaq	131(%rsp), %r8
	movb	%sil, 131(%rsp)
	leaq	(%r8,%rbp), %rdi
	jmp	.L1463
	.p2align 4,,10
	.p2align 3
.L1536:
	movq	%rsi, %rax
	orq	%rdi, %rax
	jne	.L1506
	movb	$48, 131(%rsp)
	leaq	.LC17(%rip), %rbx
	leaq	132(%rsp), %rdi
	leaq	131(%rsp), %r8
	jmp	.L1484
	.p2align 4,,10
	.p2align 3
.L1507:
	leaq	.LC16(%rip), %rbx
.L1483:
	testq	%rdi, %rdi
	jne	.L1541
	bsrq	%rsi, %rax
	movl	$255, %ecx
	leal	4(%rax), %ebp
	movabsq	$3978425819141910832, %rax
	shrl	$2, %ebp
	movq	%rax, 272(%rsp)
	cmpq	%rsi, %rcx
	movabsq	$7378413942531504440, %rax
	movq	%rax, 280(%rsp)
	leal	-1(%rbp), %eax
	jnb	.L1542
.L1487:
	leaq	272(%rsp), %rcx
	movl	$255, %r11d
	xorl	%r10d, %r10d
	.p2align 4,,10
	.p2align 3
.L1489:
	movq	%rsi, %r8
	movl	%eax, %r14d
	movq	%r10, %r15
	leal	-1(%rax), %r9d
	andl	$15, %r8d
	subl	$2, %eax
	addq	%rcx, %r8
	movzbl	(%r8), %r8d
	movb	%r8b, 131(%rsp,%r14)
	movq	%rsi, %r8
	shrdq	$8, %rdi, %rsi
	shrdq	$4, %rdi, %r8
	shrq	$8, %rdi
	movq	%r8, %r14
	andl	$15, %r14d
	cmpq	%rsi, %r11
	leaq	(%r14,%rcx), %r8
	sbbq	%rdi, %r15
	movzbl	(%r8), %r8d
	movb	%r8b, 131(%rsp,%r9)
	jc	.L1489
.L1488:
	movl	$15, %eax
	cmpq	%rsi, %rax
	movl	$0, %eax
	sbbq	%rdi, %rax
	jc	.L1543
	addq	%rsi, %rcx
	movzbl	(%rcx), %eax
.L1491:
	leaq	131(%rsp), %r8
	movl	%ebp, %edi
	movb	%al, 131(%rsp)
	addq	%r8, %rdi
	cmpb	$48, %dl
	je	.L1544
.L1484:
	movzbl	(%r12), %eax
	testb	$16, %al
	jne	.L1510
	jmp	.L1511
	.p2align 4,,10
	.p2align 3
.L1543:
	movq	%rsi, %r8
	shrdq	$4, %rdi, %rsi
	andl	$15, %r8d
	addq	%rcx, %rsi
	addq	%rcx, %r8
	movzbl	(%r8), %eax
	movb	%al, 132(%rsp)
	movzbl	(%rsi), %eax
	jmp	.L1491
	.p2align 4,,10
	.p2align 3
.L1534:
	movq	%rsi, %rcx
	shrdq	$3, %rdi, %rsi
	andl	$7, %ecx
	addl	$48, %esi
	addl	$48, %ecx
	movb	%cl, 132(%rsp)
	jmp	.L1481
	.p2align 4,,10
	.p2align 3
.L1506:
	leaq	.LC17(%rip), %rbx
	jmp	.L1483
	.p2align 4,,10
	.p2align 3
.L1508:
	leaq	132(%rsp), %rdi
	leaq	.LC16(%rip), %rbx
	leaq	131(%rsp), %r8
.L1485:
	movq	%r8, %rsi
	movq	%r8, %rbp
	.p2align 4,,10
	.p2align 3
.L1492:
	movsbl	(%rsi), %ecx
	addq	$1, %rsi
	call	toupper
	movb	%al, -1(%rsi)
	cmpq	%rdi, %rsi
	jne	.L1492
	movq	%rbp, %r8
	movl	$1, %edx
	movl	$2, %ecx
	jmp	.L1482
	.p2align 4,,10
	.p2align 3
.L1541:
	bsrq	%rdi, %rax
	leal	68(%rax), %ebp
	movabsq	$3978425819141910832, %rax
	shrl	$2, %ebp
	movq	%rax, 272(%rsp)
	movabsq	$7378413942531504440, %rax
	movq	%rax, 280(%rsp)
	leal	-1(%rbp), %eax
	jmp	.L1487
	.p2align 4,,10
	.p2align 3
.L1532:
	bsrq	%rdi, %rax
	movl	$128, %r9d
	movl	$127, %edx
	xorq	$63, %rax
	subl	%eax, %r9d
	subl	%eax, %edx
	jmp	.L1457
	.p2align 4,,10
	.p2align 3
.L1535:
	movq	%rcx, %rdx
	negq	%rdx
	jmp	.L1460
.L1499:
	movl	$1, %r9d
	jmp	.L1458
.L1501:
	movl	$1, %ebp
	.p2align 4,,10
	.p2align 3
.L1464:
	addl	$48, %esi
	jmp	.L1474
	.p2align 4,,10
	.p2align 3
.L1544:
	testl	%ebp, %ebp
	jne	.L1485
	movl	$1, %edx
	movl	$2, %ecx
	movq	%r8, %rdi
	jmp	.L1482
	.p2align 4,,10
	.p2align 3
.L1533:
	bsrq	%rdi, %rax
	movl	$2863311531, %edx
	addl	$67, %eax
	imulq	%rdx, %rax
	shrq	$33, %rax
	leal	-1(%rax), %edx
	jmp	.L1477
	.p2align 4,,10
	.p2align 3
.L1538:
	movq	64(%rsp), %rsi
	leal	5(%r9), %ebp
	movq	%r13, %r12
	movq	72(%rsp), %rdi
	movq	576(%rsp), %r13
	jmp	.L1470
	.p2align 4,,10
	.p2align 3
.L1539:
	movq	64(%rsp), %rsi
	leal	6(%r9), %ebp
	movq	%r13, %r12
	movq	72(%rsp), %rdi
	movq	576(%rsp), %r13
	jmp	.L1470
	.p2align 4,,10
	.p2align 3
.L1540:
	movq	64(%rsp), %rsi
	leal	7(%r9), %ebp
	movq	%r13, %r12
	movq	72(%rsp), %rdi
	movq	576(%rsp), %r13
	jmp	.L1470
	.p2align 4,,10
	.p2align 3
.L1542:
	leaq	272(%rsp), %rcx
	jmp	.L1488
.L1504:
	leaq	259(%rsp), %rdi
	leaq	131(%rsp), %r8
	jmp	.L1463
.L1537:
	leaq	272(%rsp), %rcx
	movl	$201, %r8d
	movl	$2, %ebp
	leaq	.LC19(%rip), %rdx
	call	memcpy
	movq	%rax, %rcx
	jmp	.L1466
.L1502:
	movl	$3, %ebp
	movl	$2, %ebx
	jmp	.L1467
.L1503:
	movl	$4, %ebp
	movl	$3, %ebx
	jmp	.L1467
.L1446:
	leaq	.LC18(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC22:
	.ascii "basic_string_view::copy\0"
	.align 8
.LC23:
	.ascii "%s: __pos (which is %zu) > __size (which is %zu)\0"
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_:
.LFB5391:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$72, %rsp
	.seh_stackalloc	72
	.seh_endprologue
	movq	(%rcx), %rdi
	leaq	16(%rcx), %r12
	movq	%rcx, %rbx
	movq	%rdx, %rbp
	cmpq	%r12, %rdi
	movq	%r8, %rsi
	je	.L1562
	movq	16(%rcx), %rax
.L1546:
	cmpq	%rbp, %rax
	jb	.L1573
.L1547:
	movq	8(%rsi), %rax
	movq	16(%rsi), %r13
	movq	24(%rsi), %r12
	movq	(%rsi), %rcx
	movq	8(%rax), %r15
	movq	(%rax), %rax
	movq	8(%r13), %rbp
	movq	(%r12), %r14
	movq	%rax, 56(%rsp)
	movq	(%rcx), %rax
	addq	%rbp, %r14
.LEHB20:
	call	*24(%rax)
.LEHE20:
	movq	56(%rsp), %r8
	movsbl	%al, %edx
	movq	%rdi, %rcx
	movq	%r14, 40(%rsp)
	movq	%rbp, 32(%rsp)
	movq	%r15, %r9
	call	_ZSt14__add_groupingIcEPT_S1_S0_PKcyPKS0_S5_
	movq	32(%rsi), %rdx
	movq	%rax, %rcx
	movq	(%rdx), %rax
	testq	%rax, %rax
	je	.L1557
	movq	40(%rsi), %r8
	cmpq	$-1, (%r8)
	je	.L1558
	movq	48(%rsi), %rax
	addq	$1, %rcx
	movzbl	(%rax), %eax
	movb	%al, -1(%rcx)
	addq	$1, (%r12)
	movq	(%rdx), %rax
.L1558:
	cmpq	$1, %rax
	jbe	.L1557
	movq	(%r12), %rax
	movq	0(%r13), %rsi
	movq	8(%r13), %rdx
	cmpq	%rax, %rsi
	jb	.L1574
	subq	%rax, %rsi
	je	.L1557
	addq	%rax, %rdx
	movq	%rsi, %r8
	call	memcpy
	movq	%rax, %rcx
	addq	%rsi, %rcx
.L1557:
	movq	(%rbx), %rax
	subq	%rdi, %rcx
	movq	%rcx, 8(%rbx)
	movb	$0, (%rax,%rcx)
	addq	$72, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L1573:
	testq	%rbp, %rbp
	js	.L1575
	addq	%rax, %rax
	cmpq	%rax, %rbp
	jb	.L1576
	movq	%rbp, %rcx
	addq	$1, %rcx
	js	.L1550
.L1551:
.LEHB21:
	call	_Znwy
	movq	8(%rbx), %r8
	movq	(%rbx), %r13
	movq	%rax, %rdi
	cmpq	$1, %r8
	je	.L1577
	testq	%r8, %r8
	je	.L1572
	movq	%r13, %rdx
	movq	%rax, %rcx
	call	memcpy
.L1572:
	cmpq	%r13, %r12
	je	.L1554
	movq	16(%rbx), %rax
	movq	%r13, %rcx
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L1554:
	movq	%rdi, (%rbx)
	movq	%rbp, 16(%rbx)
	jmp	.L1547
	.p2align 4,,10
	.p2align 3
.L1577:
	movzbl	0(%r13), %eax
	movb	%al, (%rdi)
	jmp	.L1572
	.p2align 4,,10
	.p2align 3
.L1576:
	testq	%rax, %rax
	js	.L1550
	leaq	1(%rax), %rcx
	movq	%rax, %rbp
	jmp	.L1551
	.p2align 4,,10
	.p2align 3
.L1562:
	movl	$15, %eax
	jmp	.L1546
	.p2align 4,,10
	.p2align 3
.L1550:
	call	_ZSt17__throw_bad_allocv
.L1575:
	leaq	.LC7(%rip), %rcx
	call	_ZSt20__throw_length_errorPKc
.LEHE21:
.L1574:
	leaq	.LC22(%rip), %rdx
	movq	%rsi, %r9
	movq	%rax, %r8
	leaq	.LC23(%rip), %rcx
.LEHB22:
	call	_ZSt24__throw_out_of_range_fmtPKcz
.LEHE22:
.L1563:
	movq	%rax, %rcx
	xorl	%eax, %eax
	movq	%rax, 8(%rbx)
	movq	(%rbx), %rax
	movb	$0, (%rax)
.LEHB23:
	call	_Unwind_Resume
	nop
.LEHE23:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5391:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5391-.LLSDACSB5391
.LLSDACSB5391:
	.uleb128 .LEHB20-.LFB5391
	.uleb128 .LEHE20-.LEHB20
	.uleb128 .L1563-.LFB5391
	.uleb128 0
	.uleb128 .LEHB21-.LFB5391
	.uleb128 .LEHE21-.LEHB21
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB22-.LFB5391
	.uleb128 .LEHE22-.LEHB22
	.uleb128 .L1563-.LFB5391
	.uleb128 0
	.uleb128 .LEHB23-.LFB5391
	.uleb128 .LEHE23-.LEHB23
	.uleb128 0
	.uleb128 0
.LLSDACSE5391:
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_,"x"
	.linkonce discard
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0:
.LFB5465:
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$248, %rsp
	.seh_stackalloc	248
	.seh_endprologue
	movdqu	(%rdx), %xmm0
	leaq	16(%rcx), %rax
	movb	$0, 16(%rcx)
	movq	%rcx, %rbx
	movl	%r8d, %edi
	movq	%rax, (%rcx)
	movq	%r9, %rsi
	movq	$0, 8(%rcx)
	movaps	%xmm0, 96(%rsp)
.LEHB24:
	call	_ZNSt6locale7classicEv
	movq	%rax, %rdx
	movq	%rsi, %rcx
	call	_ZNKSt6localeeqERKS_
	testb	%al, %al
	je	.L1605
.L1578:
	movq	%rbx, %rax
	addq	$248, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L1605:
	movq	.refptr._ZNSt7__cxx118numpunctIcE2idE(%rip), %rcx
	call	_ZNKSt6locale2id5_M_idEv
	movq	%rax, %rdx
	movq	(%rsi), %rax
	movq	8(%rax), %rax
	movq	(%rax,%rdx,8), %rsi
	testq	%rsi, %rsi
	je	.L1580
	movq	(%rsi), %rax
	movq	%rsi, %rcx
	call	*16(%rax)
	movb	%al, 119(%rsp)
	movq	(%rsi), %rax
	leaq	144(%rsp), %r12
	movq	%rsi, %rdx
	movq	%r12, %rcx
	call	*32(%rax)
.LEHE24:
	cmpq	$0, 152(%rsp)
	jne	.L1582
	cmpb	$46, 119(%rsp)
	je	.L1583
.L1582:
	movq	96(%rsp), %rbp
	movq	104(%rsp), %r13
	testq	%rbp, %rbp
	je	.L1606
	movl	$46, %edx
	movq	%rbp, %r8
	movq	%r13, %rcx
	call	memchr
	movsbl	%dil, %edx
	testq	%rax, %rax
	je	.L1586
	subq	%r13, %rax
	movq	%rbp, %r8
	movq	%r13, %rcx
	movq	%rax, %rdi
	movq	%rax, 120(%rsp)
	call	memchr
	testq	%rax, %rax
	je	.L1587
	subq	%r13, %rax
	cmpq	%rdi, %rax
	jnb	.L1587
.L1592:
	movq	%rax, 128(%rsp)
	subq	%rax, %rbp
.L1588:
	leaq	136(%rsp), %r8
	movq	%rbp, 136(%rsp)
	leaq	120(%rsp), %rcx
	movq	%r8, 64(%rsp)
	leaq	119(%rsp), %rdx
	movq	%rcx, 72(%rsp)
	movq	%rbx, %rcx
	leaq	96(%rsp), %r10
	movq	%rdx, 80(%rsp)
	leaq	128(%rsp), %r9
	movq	%rsi, 32(%rsp)
	leaq	0(%rbp,%rax,2), %rdx
	movq	%r12, 40(%rsp)
	leaq	32(%rsp), %r8
	movq	%r10, 48(%rsp)
	movq	%r9, 56(%rsp)
.LEHB25:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE20resize_and_overwriteIZNKSt8__format14__formatter_fpIcE11_M_localizeESt17basic_string_viewIcS2_EcRKSt6localeEUlPcyE_EEvyT_
.LEHE25:
.L1583:
	movq	144(%rsp), %rcx
	leaq	160(%rsp), %rax
	cmpq	%rax, %rcx
	je	.L1578
	movq	160(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	jmp	.L1578
	.p2align 4,,10
	.p2align 3
.L1606:
	movq	$-1, 120(%rsp)
.L1585:
	movq	%rbp, 128(%rsp)
	movq	%rbp, %rax
	xorl	%ebp, %ebp
	jmp	.L1588
	.p2align 4,,10
	.p2align 3
.L1587:
	cmpq	$-1, %rdi
	movq	%rdi, 128(%rsp)
	je	.L1585
	subq	%rdi, %rbp
	movq	%rdi, %rax
	jmp	.L1588
	.p2align 4,,10
	.p2align 3
.L1586:
	movq	$-1, 120(%rsp)
	movq	%rbp, %r8
	movq	%r13, %rcx
	call	memchr
	testq	%rax, %rax
	je	.L1585
	subq	%r13, %rax
	cmpq	$-1, %rax
	jne	.L1592
	jmp	.L1585
.L1580:
.LEHB26:
	call	_ZSt16__throw_bad_castv
.LEHE26:
.L1593:
	movq	%rax, %rsi
	jmp	.L1591
.L1594:
	movq	%r12, %rcx
	movq	%rax, %rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L1591:
	movq	%rbx, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	%rsi, %rcx
.LEHB27:
	call	_Unwind_Resume
	nop
.LEHE27:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5465:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5465-.LLSDACSB5465
.LLSDACSB5465:
	.uleb128 .LEHB24-.LFB5465
	.uleb128 .LEHE24-.LEHB24
	.uleb128 .L1593-.LFB5465
	.uleb128 0
	.uleb128 .LEHB25-.LFB5465
	.uleb128 .LEHE25-.LEHB25
	.uleb128 .L1594-.LFB5465
	.uleb128 0
	.uleb128 .LEHB26-.LFB5465
	.uleb128 .LEHE26-.LEHB26
	.uleb128 .L1593-.LFB5465
	.uleb128 0
	.uleb128 .LEHB27-.LFB5465
	.uleb128 .LEHE27-.LEHB27
	.uleb128 0
	.uleb128 0
.LLSDACSE5465:
	.text
	.seh_endproc
	.section .rdata,"dr"
.LC25:
	.ascii "basic_string::_M_replace\0"
.LC26:
	.ascii "basic_string::_M_replace_aux\0"
.LC27:
	.ascii "basic_string::insert\0"
	.align 8
.LC28:
	.ascii "%s: __pos (which is %zu) > this->size() (which is %zu)\0"
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	.def	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_:
.LFB5111:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$424, %rsp
	.seh_stackalloc	424
	.seh_endprologue
	movzbl	1(%rcx), %eax
	fldt	(%rdx)
	movl	%eax, %edx
	movq	%rcx, %rbx
	movq	%r8, %r15
	movb	$0, 208(%rsp)
	fstpt	48(%rsp)
	andl	$6, %edx
	leaq	208(%rsp), %rbp
	movq	%rbp, 192(%rsp)
	movq	$0, 200(%rsp)
	jne	.L1846
	shrb	$3, %al
	andl	$15, %eax
	cmpb	$7, %al
	ja	.L1627
	leaq	.L1751(%rip), %rdx
	movzbl	%al, %eax
	movslq	(%rdx,%rax,4), %rax
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L1751:
	.long	.L1627-.L1751
	.long	.L1752-.L1751
	.long	.L1782-.L1751
	.long	.L1783-.L1751
	.long	.L1784-.L1751
	.long	.L1785-.L1751
	.long	.L1786-.L1751
	.long	.L1781-.L1751
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1627:
	fldt	48(%rsp)
	xorl	%r13d, %r13d
	xorl	%edi, %edi
	xorl	%r12d, %r12d
	leaq	128(%rsp), %rax
	leaq	144(%rsp), %r14
	movq	%rax, %r9
	movq	%rax, 80(%rsp)
	leaq	289(%rsp), %rdx
	movq	%r14, %rcx
	fstpt	128(%rsp)
	leaq	416(%rsp), %r8
	call	_ZSt8to_charsPcS_e
	movq	144(%rsp), %rsi
	movq	152(%rsp), %rax
.L1626:
	cmpl	$132, %eax
	movb	$0, 72(%rsp)
	movq	$6, 64(%rsp)
	je	.L1780
	leaq	416(%rsp), %rax
	movq	%rax, 80(%rsp)
	leaq	289(%rsp), %r13
.L1624:
	testb	%r12b, %r12b
	je	.L1654
	cmpq	%rsi, %r13
	movq	__imp_toupper(%rip), %r12
	movq	%r13, %r14
	je	.L1656
	.p2align 4,,10
	.p2align 3
.L1655:
	movsbl	(%r14), %ecx
	addq	$1, %r14
	call	*%r12
	movb	%al, -1(%r14)
	cmpq	%r14, %rsi
	jne	.L1655
.L1656:
	movsbl	%dil, %ecx
	call	*%r12
	movl	%eax, %edi
.L1654:
	fldt	48(%rsp)
	movzbl	(%rbx), %r9d
	fxam
	fnstsw	%ax
	fstp	%st(0)
	testb	$2, %ah
	jne	.L1657
	movl	%r9d, %eax
	andl	$12, %eax
	cmpb	$4, %al
	je	.L1847
	cmpb	$12, %al
	jne	.L1657
	movb	$32, -1(%r13)
	movzbl	(%rbx), %r9d
	subq	$1, %r13
	.p2align 4,,10
	.p2align 3
.L1657:
	movq	%rsi, %r12
	subq	%r13, %r12
	testb	$16, %r9b
	je	.L1659
	fldt	48(%rsp)
	fabs
	fldt	.LC24(%rip)
	fucomip	%st(1), %st
	fstp	%st(0)
	jb	.L1659
	testq	%r12, %r12
	je	.L1763
	movq	%r12, %r8
	movl	$46, %edx
	movq	%r13, %rcx
	movb	%r9b, 88(%rsp)
	call	memchr
	movzbl	88(%rsp), %r9d
	testq	%rax, %rax
	movq	%rax, %r14
	je	.L1661
	subq	%r13, %r14
	cmpq	$-1, %r14
	je	.L1661
	leaq	1(%r14), %rax
	movq	%r12, 88(%rsp)
	cmpq	%r12, %rax
	jnb	.L1662
	movq	%r12, %r8
	movsbl	%dil, %edx
	movb	%r9b, 103(%rsp)
	leaq	0(%r13,%rax), %rcx
	subq	%rax, %r8
	call	memchr
	movzbl	103(%rsp), %r9d
	testq	%rax, %rax
	je	.L1662
	subq	%r13, %rax
	cmpq	$-1, %rax
	cmove	%r12, %rax
	movq	%rax, 88(%rsp)
.L1662:
	cmpq	%r14, 88(%rsp)
	sete	103(%rsp)
	sete	%r14b
	cmpb	$0, 72(%rsp)
	movzbl	%r14b, %r14d
	jne	.L1663
	movq	$0, 72(%rsp)
.L1664:
	testq	%r14, %r14
	je	.L1659
.L1748:
	movq	200(%rsp), %r9
	leaq	(%r12,%r14), %rax
	movq	%rax, 64(%rsp)
	testq	%r9, %r9
	jne	.L1666
	movq	80(%rsp), %rax
	subq	%rsi, %rax
	cmpq	%r14, %rax
	jnb	.L1848
	cmpq	%rbp, 192(%rsp)
	je	.L1849
	movq	208(%rsp), %rax
	movq	64(%rsp), %rsi
	cmpq	%rsi, %rax
	jnb	.L1675
.L1674:
	cmpq	$0, 64(%rsp)
	js	.L1744
	addq	%rax, %rax
	cmpq	%rax, 64(%rsp)
	jnb	.L1677
	testq	%rax, %rax
	jns	.L1850
.L1678:
	leaq	192(%rsp), %rsi
.LEHB28:
	call	_ZSt17__throw_bad_allocv
.L1689:
	movq	%r12, %rcx
	movq	%r12, %r14
	addq	$1, %rcx
	js	.L1696
.L1697:
	leaq	192(%rsp), %rsi
	call	_Znwy
.LEHE28:
	cmpq	$1, %r14
	movq	%rax, %r10
	je	.L1851
.L1690:
	movq	%r10, %rcx
	movq	%r14, %r8
	movq	%r13, %rdx
	call	memcpy
	movq	%r12, %rsi
	movq	%r14, %r12
	movq	%rax, %r10
.L1698:
	movq	192(%rsp), %rcx
	cmpq	%rbp, %rcx
	je	.L1699
	movq	208(%rsp), %rax
	movq	%r10, 64(%rsp)
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	64(%rsp), %r10
.L1699:
	movq	%r10, 192(%rsp)
	movq	%rsi, 208(%rsp)
.L1694:
	cmpb	$0, 103(%rsp)
	movq	%r12, 200(%rsp)
	movb	$0, (%r10,%r12)
	jne	.L1852
.L1700:
	cmpq	$0, 72(%rsp)
	movq	200(%rsp), %r12
	jne	.L1853
.L1702:
	movq	192(%rsp), %r13
	movzbl	(%rbx), %r9d
	.p2align 4,,10
	.p2align 3
.L1659:
	leaq	240(%rsp), %rsi
	andl	$32, %r9d
	movq	$0, 176(%rsp)
	movb	$0, 184(%rsp)
	movq	%rsi, 224(%rsp)
	movq	$0, 232(%rsp)
	movb	$0, 240(%rsp)
	je	.L1773
	cmpb	$0, 32(%r15)
	leaq	24(%r15), %rdx
	je	.L1854
.L1717:
	leaq	168(%rsp), %r14
	movq	%r14, %rcx
	call	_ZNSt6localeC1ERKS_
	leaq	256(%rsp), %rcx
	movq	%r14, %r9
	movsbl	%dil, %r8d
	leaq	112(%rsp), %rdx
	movq	%r12, 112(%rsp)
	movq	%r13, 120(%rsp)
.LEHB29:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE29:
	movq	256(%rsp), %rax
	leaq	272(%rsp), %rdi
	movq	224(%rsp), %rcx
	movq	264(%rsp), %r8
	cmpq	%rdi, %rax
	je	.L1855
	movq	%r8, %xmm0
	cmpq	%rsi, %rcx
	movhps	272(%rsp), %xmm0
	je	.L1856
	testq	%rcx, %rcx
	movq	240(%rsp), %rdx
	movq	%rax, 224(%rsp)
	movups	%xmm0, 232(%rsp)
	je	.L1725
	movq	%rcx, 256(%rsp)
	movq	%rdx, 272(%rsp)
.L1724:
	movq	$0, 264(%rsp)
	movb	$0, (%rcx)
	movq	256(%rsp), %rcx
	cmpq	%rdi, %rcx
	je	.L1726
	movq	272(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L1726:
	movq	%r14, %rcx
	call	_ZNSt6localeD1Ev
	movzwl	(%rbx), %eax
	movq	232(%rsp), %r12
	movq	224(%rsp), %rdi
	andw	$384, %ax
	cmpw	$128, %ax
	je	.L1857
.L1727:
	cmpw	$256, %ax
	je	.L1729
	movq	16(%r15), %r14
.L1733:
	leaq	112(%rsp), %rdx
	movq	%r14, %rcx
	movq	%r12, 112(%rsp)
	movq	%rdi, 120(%rsp)
.LEHB30:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L1842:
	movq	224(%rsp), %rcx
	movq	%rax, %rbx
	cmpq	%rsi, %rcx
	je	.L1737
	movq	240(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L1737:
	cmpb	$0, 184(%rsp)
	jne	.L1858
.L1738:
	movq	192(%rsp), %rcx
	cmpq	%rbp, %rcx
	je	.L1802
	movq	208(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L1802:
	movq	%rbx, %rax
	addq	$424, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L1773:
	movzwl	(%rbx), %eax
	movq	%r13, %rdi
	andw	$384, %ax
	cmpw	$128, %ax
	jne	.L1727
.L1857:
	movzwl	4(%rbx), %eax
.L1728:
	cmpq	%rax, %r12
	movq	16(%r15), %r14
	jnb	.L1733
	movzbl	(%rbx), %edx
	subq	%r12, %rax
	movzbl	8(%rbx), %ecx
	movq	%rax, %rbx
	movl	%edx, %r8d
	andl	$3, %r8d
	movsbl	%cl, %eax
	jne	.L1735
	andl	$64, %edx
	je	.L1775
	fldt	48(%rsp)
	fabs
	fldt	.LC24(%rip)
	fucomip	%st(1), %st
	fstp	%st(0)
	jnb	.L1859
.L1775:
	movl	$32, %eax
	movl	$2, %r8d
.L1735:
	leaq	112(%rsp), %rdx
	movl	%eax, 32(%rsp)
	movq	%rbx, %r9
	movq	%r14, %rcx
	movq	%r12, 112(%rsp)
	movq	%rdi, 120(%rsp)
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
.LEHE30:
	jmp	.L1842
	.p2align 4,,10
	.p2align 3
.L1846:
	cmpb	$2, %dl
	je	.L1860
	movq	$-1, 64(%rsp)
	cmpb	$4, %dl
	je	.L1861
.L1610:
	shrb	$3, %al
	andl	$15, %eax
	cmpb	$7, %al
	ja	.L1613
	leaq	.L1615(%rip), %rdx
	movzbl	%al, %eax
	movslq	(%rdx,%rax,4), %rax
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L1615:
	.long	.L1622-.L1615
	.long	.L1754-.L1615
	.long	.L1620-.L1615
	.long	.L1619-.L1615
	.long	.L1836-.L1615
	.long	.L1838-.L1615
	.long	.L1616-.L1615
	.long	.L1837-.L1615
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1858:
	leaq	176(%rsp), %rcx
	call	_ZNSt6localeD1Ev
	jmp	.L1738
	.p2align 4,,10
	.p2align 3
.L1782:
	movl	$1, %r12d
.L1625:
	fldt	48(%rsp)
	movl	$4, 32(%rsp)
	movl	$4, %r13d
	movl	$112, %edi
	leaq	128(%rsp), %rax
	leaq	144(%rsp), %r14
	movq	%rax, %r9
	movq	%rax, 80(%rsp)
	leaq	289(%rsp), %rdx
	movq	%r14, %rcx
	fstpt	128(%rsp)
	leaq	416(%rsp), %r8
	call	_ZSt8to_charsPcS_eSt12chars_format
	movq	144(%rsp), %rsi
	movq	152(%rsp), %rax
	jmp	.L1626
	.p2align 4,,10
	.p2align 3
.L1859:
	movzbl	0(%r13), %edx
	leaq	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE(%rip), %rcx
	movl	$48, %eax
	movl	$2, %r8d
	cmpb	$15, (%rcx,%rdx)
	jbe	.L1735
	movq	24(%r14), %rax
	movzbl	(%rdi), %edx
	leaq	1(%rax), %rcx
	movq	%rcx, 24(%r14)
	movb	%dl, (%rax)
	movq	24(%r14), %rax
	subq	8(%r14), %rax
	cmpq	16(%r14), %rax
	je	.L1862
.L1736:
	addq	$1, %rdi
	subq	$1, %r12
	movl	$48, %eax
	movl	$2, %r8d
	jmp	.L1735
	.p2align 4,,10
	.p2align 3
.L1763:
	xorl	%eax, %eax
.L1660:
	cmpb	$0, 72(%rsp)
	je	.L1863
	movzbl	72(%rsp), %edx
	movq	%rax, 88(%rsp)
	movl	$1, %r14d
	movb	%dl, 103(%rsp)
	jmp	.L1747
	.p2align 4,,10
	.p2align 3
.L1783:
	movq	$6, 64(%rsp)
.L1619:
	xorl	%r12d, %r12d
.L1618:
	movl	$1, %r13d
	movl	$101, %edi
	movb	$0, 72(%rsp)
.L1621:
	movl	64(%rsp), %esi
	leaq	128(%rsp), %rax
	movl	%r13d, 32(%rsp)
	fldt	48(%rsp)
	movq	%rax, %r9
	movq	%rax, 80(%rsp)
	leaq	144(%rsp), %r14
	leaq	289(%rsp), %rax
	movl	%esi, 40(%rsp)
	movq	%r14, %rcx
	leaq	416(%rsp), %r8
	movq	%rax, %rdx
	movq	%rax, 88(%rsp)
	fstpt	128(%rsp)
	call	_ZSt8to_charsPcS_eSt12chars_formati
	movq	144(%rsp), %rsi
	cmpl	$132, 152(%rsp)
	je	.L1623
	leaq	416(%rsp), %rax
	movq	88(%rsp), %r13
	movq	%rax, 80(%rsp)
	jmp	.L1624
	.p2align 4,,10
	.p2align 3
.L1784:
	movq	$6, 64(%rsp)
.L1836:
	movl	$1, %r12d
	jmp	.L1618
	.p2align 4,,10
	.p2align 3
.L1785:
	movq	$6, 64(%rsp)
.L1838:
	movl	$2, %r13d
	xorl	%edi, %edi
	movb	$0, 72(%rsp)
	xorl	%r12d, %r12d
	jmp	.L1621
	.p2align 4,,10
	.p2align 3
.L1781:
	movq	$6, 64(%rsp)
.L1837:
	movl	$1, %r12d
.L1614:
	movl	$3, %r13d
	movl	$101, %edi
	movb	$1, 72(%rsp)
	jmp	.L1621
	.p2align 4,,10
	.p2align 3
.L1786:
	movq	$6, 64(%rsp)
.L1616:
	xorl	%r12d, %r12d
	jmp	.L1614
	.p2align 4,,10
	.p2align 3
.L1752:
	xorl	%r12d, %r12d
	jmp	.L1625
	.p2align 4,,10
	.p2align 3
.L1861:
	movzbl	(%r8), %edx
	movb	$0, 240(%rsp)
	movzwl	6(%rcx), %eax
	movl	%edx, %ecx
	andl	$15, %edx
	andl	$15, %ecx
	cmpq	%rdx, %rax
	jb	.L1864
	testb	%cl, %cl
	jne	.L1612
	movq	(%r8), %rdx
	shrq	$4, %rdx
	cmpq	%rdx, %rax
	jnb	.L1612
	salq	$5, %rax
	addq	8(%r8), %rax
	movq	(%rax), %rdx
	movq	%rdx, 224(%rsp)
	movq	8(%rax), %rdx
	movq	%rdx, 232(%rsp)
	movzbl	16(%rax), %eax
	movb	%al, 240(%rsp)
	.p2align 4,,10
	.p2align 3
.L1612:
	leaq	224(%rsp), %rcx
	leaq	192(%rsp), %rsi
.LEHB31:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE31:
	movq	%rax, 64(%rsp)
	movzbl	1(%rbx), %eax
	jmp	.L1610
	.p2align 4,,10
	.p2align 3
.L1847:
	movb	$43, -1(%r13)
	subq	$1, %r13
	movzbl	(%rbx), %r9d
	jmp	.L1657
	.p2align 4,,10
	.p2align 3
.L1854:
	movq	%rdx, %rcx
	movq	%rdx, 64(%rsp)
	call	_ZNSt6localeC1Ev
	movq	64(%rsp), %rdx
	movb	$1, 32(%r15)
	jmp	.L1717
	.p2align 4,,10
	.p2align 3
.L1729:
	movzbl	(%r15), %edx
	movb	$0, 272(%rsp)
	movzwl	4(%rbx), %eax
	movl	%edx, %ecx
	andl	$15, %edx
	andl	$15, %ecx
	cmpq	%rdx, %rax
	jb	.L1865
	testb	%cl, %cl
	jne	.L1732
	movq	(%r15), %rdx
	shrq	$4, %rdx
	cmpq	%rdx, %rax
	jnb	.L1732
	salq	$5, %rax
	addq	8(%r15), %rax
	movq	(%rax), %rdx
	movq	%rdx, 256(%rsp)
	movq	8(%rax), %rdx
	movq	%rdx, 264(%rsp)
	movzbl	16(%rax), %eax
	movb	%al, 272(%rsp)
	.p2align 4,,10
	.p2align 3
.L1732:
	leaq	256(%rsp), %rcx
.LEHB32:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE32:
	jmp	.L1728
	.p2align 4,,10
	.p2align 3
.L1856:
	movq	%rax, 224(%rsp)
	movups	%xmm0, 232(%rsp)
.L1725:
	movq	%rdi, 256(%rsp)
	leaq	272(%rsp), %rdi
	movq	%rdi, %rcx
	jmp	.L1724
	.p2align 4,,10
	.p2align 3
.L1860:
	movzwl	6(%rcx), %edi
	movq	%rdi, 64(%rsp)
	jmp	.L1610
	.p2align 4,,10
	.p2align 3
.L1855:
	testq	%r8, %r8
	je	.L1720
	cmpq	$1, %r8
	je	.L1866
	movq	%rdi, %rdx
	call	memcpy
	movq	264(%rsp), %r8
	movq	224(%rsp), %rcx
.L1720:
	movq	%r8, 232(%rsp)
	movb	$0, (%rcx,%r8)
	movq	256(%rsp), %rcx
	jmp	.L1724
	.p2align 4,,10
	.p2align 3
.L1663:
	movq	88(%rsp), %rax
	subq	$1, %rax
.L1747:
	movzbl	0(%r13), %edx
	leaq	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE(%rip), %rcx
	cmpb	$16, (%rcx,%rdx)
	movq	64(%rsp), %rdx
	adcq	$-1, %rax
	subq	%rax, %rdx
	movq	%rdx, 72(%rsp)
	addq	%rdx, %r14
	jmp	.L1664
	.p2align 4,,10
	.p2align 3
.L1780:
	movb	$0, 103(%rsp)
	movq	$134, 88(%rsp)
.L1628:
	movq	192(%rsp), %r10
	cmpq	%rbp, %r10
	je	.L1760
	movq	208(%rsp), %rax
.L1630:
	movq	88(%rsp), %rsi
	cmpq	%rsi, %rax
	jb	.L1867
.L1653:
	cmpq	%rbp, %r10
	je	.L1761
	movq	208(%rsp), %rax
	leaq	(%rax,%rax), %rsi
	cmpq	%rsi, %rax
	movq	%rsi, 88(%rsp)
	jb	.L1868
.L1642:
	movq	88(%rsp), %rax
	leaq	1(%r10), %rdx
	movq	%r10, 88(%rsp)
	cmpb	$0, 103(%rsp)
	fldt	48(%rsp)
	leaq	-1(%r10,%rax), %r8
	fstpt	128(%rsp)
	jne	.L1869
	testl	%r13d, %r13d
	jne	.L1870
	movq	80(%rsp), %r9
	movq	%r14, %rcx
	call	_ZSt8to_charsPcS_e
	movq	144(%rsp), %rsi
	movq	152(%rsp), %rax
	movq	88(%rsp), %r10
.L1650:
	testl	%eax, %eax
	jne	.L1652
	movq	192(%rsp), %rdx
	movq	%rsi, %rax
	subq	%r10, %rax
	movq	%rax, 200(%rsp)
	movb	$0, (%rdx,%rax)
	movq	192(%rsp), %rax
	leaq	1(%rax), %r13
	addq	200(%rsp), %rax
	movq	%rax, 80(%rsp)
	jmp	.L1624
	.p2align 4,,10
	.p2align 3
.L1661:
	movsbl	%dil, %edx
	movq	%r12, %r8
	movq	%r13, %rcx
	movb	%r9b, 88(%rsp)
	call	memchr
	movzbl	88(%rsp), %r9d
	testq	%rax, %rax
	je	.L1767
	subq	%r13, %rax
	cmpq	$-1, %rax
	cmove	%r12, %rax
	jmp	.L1660
.L1754:
	movl	$4, %r13d
	movl	$112, %edi
	movb	$0, 72(%rsp)
	xorl	%r12d, %r12d
	jmp	.L1621
.L1620:
	movl	$4, %r13d
	movl	$112, %edi
	movb	$0, 72(%rsp)
	movl	$1, %r12d
	jmp	.L1621
.L1622:
	movl	$3, %r13d
	xorl	%edi, %edi
	movb	$0, 72(%rsp)
	xorl	%r12d, %r12d
	jmp	.L1621
.L1863:
	movq	%rax, 88(%rsp)
	movl	$1, %r14d
	movq	$0, 72(%rsp)
	movb	$1, 103(%rsp)
	jmp	.L1748
.L1870:
	movq	80(%rsp), %r9
	movl	%r13d, 32(%rsp)
	movq	%r14, %rcx
	call	_ZSt8to_charsPcS_eSt12chars_format
	movq	144(%rsp), %rsi
	movq	152(%rsp), %rax
	movq	88(%rsp), %r10
	jmp	.L1650
.L1864:
	movq	(%r8), %rdx
	leaq	(%rax,%rax,4), %rcx
	salq	$4, %rax
	addq	8(%r8), %rax
	shrq	$4, %rdx
	shrq	%cl, %rdx
	andl	$31, %edx
	movb	%dl, 240(%rsp)
	movq	(%rax), %rdx
	movq	%rdx, 224(%rsp)
	movq	8(%rax), %rax
	movq	%rax, 232(%rsp)
	jmp	.L1612
.L1767:
	movq	%r12, %rax
	jmp	.L1660
.L1849:
	movq	64(%rsp), %rax
	cmpq	$15, %rax
	ja	.L1845
	movq	88(%rsp), %rax
	cmpq	%rax, %r12
	cmova	%rax, %r12
	testq	%r12, %r12
	js	.L1682
	movq	%rbp, %r10
.L1749:
	cmpq	$15, %r12
	ja	.L1871
.L1688:
	cmpq	%r10, %r13
	jb	.L1692
	cmpq	%r13, %r10
	jb	.L1692
	xorl	%eax, %eax
	movq	%r12, 32(%rsp)
	movq	%r13, %r9
	xorl	%r8d, %r8d
	leaq	192(%rsp), %rsi
	movq	%rax, 40(%rsp)
	movq	%r10, %rdx
	movq	%rsi, %rcx
.LEHB33:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	movq	192(%rsp), %r10
	jmp	.L1694
	.p2align 4,,10
	.p2align 3
.L1652:
	movq	192(%rsp), %rdx
	cmpl	$132, %eax
	movq	$0, 200(%rsp)
	movb	$0, (%rdx)
	movq	192(%rsp), %r10
	movq	200(%rsp), %rdx
	je	.L1653
	leaq	(%r10,%rdx), %rax
	leaq	1(%r10), %r13
	movq	%rax, 80(%rsp)
	jmp	.L1624
	.p2align 4,,10
	.p2align 3
.L1867:
	testq	%rsi, %rsi
	js	.L1872
	addq	%rax, %rax
	cmpq	%rax, 88(%rsp)
	jnb	.L1633
	testq	%rax, %rax
	js	.L1634
	leaq	1(%rax), %rcx
	movq	%rax, 88(%rsp)
.L1635:
	leaq	192(%rsp), %rsi
	call	_Znwy
	movq	%rax, %r10
	movq	200(%rsp), %rax
	movq	192(%rsp), %rsi
	leaq	1(%rax), %r8
	testq	%rax, %rax
	je	.L1873
	testq	%r8, %r8
	je	.L1839
	movq	%r10, %rcx
	movq	%rsi, %rdx
	call	memcpy
	movq	%rax, %r10
.L1839:
	cmpq	%rbp, %rsi
	je	.L1638
	movq	208(%rsp), %rax
	movq	%rsi, %rcx
	movq	%r10, 104(%rsp)
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	104(%rsp), %r10
.L1638:
	movq	88(%rsp), %rax
	movq	%r10, 192(%rsp)
	movq	%rax, 208(%rsp)
	jmp	.L1653
.L1865:
	movq	(%r15), %rdx
	leaq	(%rax,%rax,4), %rcx
	salq	$4, %rax
	addq	8(%r15), %rax
	shrq	$4, %rdx
	shrq	%cl, %rdx
	andl	$31, %edx
	movb	%dl, 272(%rsp)
	movq	(%rax), %rdx
	movq	%rdx, 256(%rsp)
	movq	8(%rax), %rax
	movq	%rax, 264(%rsp)
	jmp	.L1732
.L1666:
	cmpq	%rbp, 192(%rsp)
	je	.L1672
	movq	208(%rsp), %rax
	movq	64(%rsp), %rsi
	cmpq	%rsi, %rax
	jb	.L1674
.L1673:
	movq	88(%rsp), %rax
	cmpq	%rax, %r9
	jb	.L1874
.L1685:
	movabsq	$9223372036854775807, %rax
	subq	%r9, %rax
	cmpq	%r14, %rax
	jb	.L1875
	movq	192(%rsp), %rax
	leaq	(%r9,%r14), %r12
	cmpq	%rbp, %rax
	je	.L1772
	movq	208(%rsp), %rdx
.L1709:
	cmpq	%r12, %rdx
	jb	.L1710
	movq	88(%rsp), %rsi
	leaq	(%rax,%rsi), %rcx
	subq	%rsi, %r9
	je	.L1711
	leaq	(%rcx,%r14), %rax
	cmpq	$1, %r9
	je	.L1876
	movq	%rcx, %rdx
	movq	%r9, %r8
	movq	%rax, %rcx
	call	memmove
	movq	88(%rsp), %rcx
	addq	192(%rsp), %rcx
.L1711:
	cmpq	$1, %r14
	je	.L1877
	movq	%r14, %r8
	movl	$48, %edx
	call	memset
.L1714:
	movq	192(%rsp), %rax
	movq	%r12, 200(%rsp)
	cmpb	$0, 103(%rsp)
	movb	$0, (%rax,%r12)
	movq	200(%rsp), %r12
	je	.L1702
	movq	192(%rsp), %rax
	movq	88(%rsp), %rsi
	movb	$46, (%rax,%rsi)
	movq	200(%rsp), %r12
	jmp	.L1702
.L1677:
	movq	64(%rsp), %rcx
	addq	$1, %rcx
	js	.L1678
.L1679:
	leaq	192(%rsp), %rsi
	call	_Znwy
	movq	200(%rsp), %r9
	movq	%rax, %rsi
	movq	192(%rsp), %r10
	leaq	1(%r9), %r8
	testq	%r9, %r9
	je	.L1878
	testq	%r8, %r8
	jne	.L1684
	cmpq	%rbp, %r10
	je	.L1879
.L1681:
	movq	208(%rsp), %rax
	movq	%r10, %rcx
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	200(%rsp), %r9
	movq	%rsi, 192(%rsp)
	movq	64(%rsp), %rax
	testq	%r9, %r9
	movq	%rax, 208(%rsp)
	jne	.L1673
.L1675:
	movq	88(%rsp), %rax
	cmpq	%rax, %r12
	cmova	%rax, %r12
	testq	%r12, %r12
	js	.L1682
	movq	192(%rsp), %r10
	cmpq	%rbp, %r10
	je	.L1749
.L1687:
	movq	208(%rsp), %rax
	cmpq	%r12, %rax
	jnb	.L1688
	addq	%rax, %rax
	cmpq	%rax, %r12
	jnb	.L1689
	leaq	1(%rax), %rcx
	testq	%rax, %rax
	movq	%r12, %r14
	movq	%rax, %r12
	jns	.L1697
.L1696:
	leaq	192(%rsp), %rsi
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L1633:
	movq	88(%rsp), %rcx
	addq	$1, %rcx
	jns	.L1635
.L1634:
	leaq	192(%rsp), %rsi
	call	_ZSt17__throw_bad_allocv
.L1869:
	movl	64(%rsp), %eax
	movl	%r13d, 32(%rsp)
	movq	%r14, %rcx
	movq	80(%rsp), %r9
	movl	%eax, 40(%rsp)
	call	_ZSt8to_charsPcS_eSt12chars_formati
	movq	144(%rsp), %rsi
	movq	152(%rsp), %rax
	movq	88(%rsp), %r10
	jmp	.L1650
.L1623:
	movq	64(%rsp), %rax
	cmpl	$2, %r13d
	movb	$1, 103(%rsp)
	leaq	128(%rax), %rsi
	movq	%rsi, 88(%rsp)
	jne	.L1628
	fldt	48(%rsp)
	pxor	%xmm0, %xmm0
	fisttpl	88(%rsp)
	movl	88(%rsp), %eax
	cltd
	xorl	%edx, %eax
	subl	%edx, %eax
	cvtsi2sdl	%eax, %xmm0
	call	log10
	cvttsd2sil	%xmm0, %edx
	movl	%edx, %eax
	sarl	%eax
	cmpl	$1, %edx
	movl	$1, %edx
	cltq
	cmovle	%rdx, %rax
	addq	%rax, %rsi
	movq	%rsi, 88(%rsp)
	jmp	.L1628
.L1692:
	testq	%r12, %r12
	je	.L1694
	cmpq	$1, %r12
	je	.L1880
	movq	%r10, %rcx
	movq	%r12, %r8
	movq	%r13, %rdx
	call	memcpy
	movq	192(%rsp), %r10
	jmp	.L1694
.L1848:
	movq	88(%rsp), %rax
	movq	%r12, %r8
	leaq	0(%r13,%rax), %rsi
	subq	%rax, %r8
	leaq	(%rax,%r14), %rcx
	movq	%rsi, %rdx
	addq	%r13, %rcx
	call	memmove
	cmpb	$0, 103(%rsp)
	je	.L1669
	movq	88(%rsp), %rax
	movb	$46, (%rsi)
	leaq	1(%r13,%rax), %rsi
.L1669:
	movq	72(%rsp), %r8
	movl	$48, %edx
	movq	%rsi, %rcx
	call	memset
	movzbl	(%rbx), %r9d
	movq	64(%rsp), %r12
	jmp	.L1659
.L1761:
	movq	$30, 88(%rsp)
	movl	$31, %ecx
.L1641:
	leaq	192(%rsp), %rsi
	call	_Znwy
	movq	200(%rsp), %r8
	movq	%rax, %r10
	movq	192(%rsp), %rsi
	cmpq	$1, %r8
	je	.L1881
	testq	%r8, %r8
	je	.L1841
	movq	%rsi, %rdx
	movq	%rax, %rcx
	call	memcpy
	movq	%rax, %r10
.L1841:
	cmpq	%rbp, %rsi
	je	.L1646
	movq	208(%rsp), %rax
	movq	%rsi, %rcx
	movq	%r10, 104(%rsp)
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	104(%rsp), %r10
.L1646:
	movq	88(%rsp), %rax
	movq	%r10, 192(%rsp)
	movq	%rax, 208(%rsp)
	jmp	.L1642
.L1760:
	movl	$15, %eax
	jmp	.L1630
.L1868:
	testq	%rsi, %rsi
	js	.L1643
	leaq	1(%rsi), %rcx
	jmp	.L1641
.L1710:
	movq	88(%rsp), %r13
	movq	%r14, 32(%rsp)
	xorl	%r9d, %r9d
	xorl	%r8d, %r8d
	leaq	192(%rsp), %rsi
	movq	%rsi, %rcx
	movq	%r13, %rdx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	movq	192(%rsp), %rcx
	addq	%r13, %rcx
	jmp	.L1711
.L1873:
	movzbl	(%rsi), %eax
	movb	%al, (%r10)
	jmp	.L1839
.L1878:
	movzbl	(%r10), %eax
	cmpq	%rbp, %r10
	movb	%al, (%rsi)
	jne	.L1681
	movq	64(%rsp), %rax
	movq	%rsi, 192(%rsp)
	movq	%rax, 208(%rsp)
	movq	88(%rsp), %rax
	cmpq	%rax, %r12
	cmova	%rax, %r12
	testq	%r12, %r12
	js	.L1682
	movq	%rsi, %r10
	jmp	.L1687
.L1853:
	movabsq	$9223372036854775807, %rax
	movq	72(%rsp), %rsi
	subq	%r12, %rax
	cmpq	%rsi, %rax
	jb	.L1882
	movq	72(%rsp), %rax
	leaq	(%r12,%rax), %r13
	movq	192(%rsp), %rax
	cmpq	%rbp, %rax
	je	.L1771
	movq	208(%rsp), %rdx
.L1704:
	cmpq	%r13, %rdx
	jb	.L1883
.L1705:
	cmpq	$1, 72(%rsp)
	leaq	(%rax,%r12), %rcx
	je	.L1884
	movq	72(%rsp), %r8
	movl	$48, %edx
	call	memset
.L1707:
	movq	192(%rsp), %rax
	movq	%r13, 200(%rsp)
	movb	$0, (%rax,%r13)
	movq	200(%rsp), %r12
	jmp	.L1702
.L1684:
	movq	%r10, %rdx
	movq	%rax, %rcx
	movq	%r9, 104(%rsp)
	movq	%r10, 80(%rsp)
	call	memcpy
	movq	80(%rsp), %r10
	movq	104(%rsp), %r9
	cmpq	%rbp, %r10
	jne	.L1681
	movq	64(%rsp), %rax
	movq	%rsi, 192(%rsp)
	movq	%rax, 208(%rsp)
	jmp	.L1673
.L1866:
	movzbl	272(%rsp), %eax
	movb	%al, (%rcx)
	movq	264(%rsp), %r8
	movq	224(%rsp), %rcx
	jmp	.L1720
.L1881:
	movzbl	(%rsi), %eax
	movb	%al, (%r10)
	jmp	.L1841
.L1852:
	leaq	192(%rsp), %rsi
	movl	$46, %edx
	movq	%rsi, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	jmp	.L1700
.L1672:
	movq	64(%rsp), %rax
	cmpq	$15, %rax
	jbe	.L1673
.L1845:
	testq	%rax, %rax
	js	.L1744
	cmpq	$29, %rax
	ja	.L1677
	movq	$30, 64(%rsp)
.L1745:
	movq	64(%rsp), %rax
	leaq	1(%rax), %rcx
	jmp	.L1679
.L1772:
	movl	$15, %edx
	jmp	.L1709
.L1877:
	movb	$48, (%rcx)
	jmp	.L1714
.L1876:
	movzbl	(%rcx), %edx
	movb	%dl, (%rax)
	movq	192(%rsp), %rcx
	addq	%rsi, %rcx
	jmp	.L1711
.L1880:
	movzbl	0(%r13), %eax
	movb	%al, (%r10)
	movq	192(%rsp), %r10
	jmp	.L1694
.L1883:
	movq	72(%rsp), %rax
	xorl	%r9d, %r9d
	xorl	%r8d, %r8d
	movq	%r12, %rdx
	leaq	192(%rsp), %rsi
	movq	%rsi, %rcx
	movq	%rax, 32(%rsp)
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE33:
	movq	192(%rsp), %rax
	jmp	.L1705
.L1862:
	movq	(%r14), %rax
	movq	%r14, %rcx
.LEHB34:
	call	*(%rax)
.LEHE34:
	jmp	.L1736
.L1871:
	cmpq	$29, %r12
	ja	.L1689
	leaq	192(%rsp), %rsi
	movl	$31, %ecx
.LEHB35:
	call	_Znwy
	movq	%r12, %r14
	movq	%rax, %r10
	movl	$30, %r12d
	jmp	.L1690
.L1884:
	movb	$48, (%rcx)
	jmp	.L1707
.L1771:
	movl	$15, %edx
	jmp	.L1704
.L1879:
	movq	%rax, 192(%rsp)
	movq	64(%rsp), %rax
	movq	$-1, %r9
	movq	%rax, 208(%rsp)
	jmp	.L1685
.L1851:
	movzbl	0(%r13), %eax
	movq	%r12, %rsi
	movl	$1, %r12d
	movb	%al, (%r10)
	jmp	.L1698
.L1850:
	movq	%rax, 64(%rsp)
	jmp	.L1745
.L1872:
	leaq	.LC7(%rip), %rcx
	leaq	192(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L1643:
	leaq	.LC7(%rip), %rcx
	leaq	192(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L1744:
	leaq	.LC7(%rip), %rcx
	leaq	192(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L1875:
	leaq	.LC26(%rip), %rcx
	leaq	192(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L1874:
	leaq	.LC27(%rip), %rdx
	movq	%rax, %r8
	leaq	.LC28(%rip), %rcx
	leaq	192(%rsp), %rsi
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L1682:
	leaq	.LC25(%rip), %rcx
	leaq	192(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L1882:
	leaq	.LC26(%rip), %rcx
	leaq	192(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.LEHE35:
.L1613:
	xorl	%r13d, %r13d
	xorl	%edi, %edi
	movb	$0, 72(%rsp)
	xorl	%r12d, %r12d
	jmp	.L1621
.L1787:
	movq	%rax, %rbx
.L1743:
	movq	%rsi, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	%rbx, %rcx
.LEHB36:
	call	_Unwind_Resume
.LEHE36:
.L1789:
	movq	%rax, %rbx
	jmp	.L1741
.L1788:
	movq	%r14, %rcx
	movq	%rax, %rbx
	call	_ZNSt6localeD1Ev
.L1741:
	leaq	224(%rsp), %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	cmpb	$0, 184(%rsp)
	je	.L1742
	leaq	176(%rsp), %rcx
	call	_ZNSt6localeD1Ev
.L1742:
	leaq	192(%rsp), %rsi
	jmp	.L1743
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5111:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5111-.LLSDACSB5111
.LLSDACSB5111:
	.uleb128 .LEHB28-.LFB5111
	.uleb128 .LEHE28-.LEHB28
	.uleb128 .L1787-.LFB5111
	.uleb128 0
	.uleb128 .LEHB29-.LFB5111
	.uleb128 .LEHE29-.LEHB29
	.uleb128 .L1788-.LFB5111
	.uleb128 0
	.uleb128 .LEHB30-.LFB5111
	.uleb128 .LEHE30-.LEHB30
	.uleb128 .L1789-.LFB5111
	.uleb128 0
	.uleb128 .LEHB31-.LFB5111
	.uleb128 .LEHE31-.LEHB31
	.uleb128 .L1787-.LFB5111
	.uleb128 0
	.uleb128 .LEHB32-.LFB5111
	.uleb128 .LEHE32-.LEHB32
	.uleb128 .L1789-.LFB5111
	.uleb128 0
	.uleb128 .LEHB33-.LFB5111
	.uleb128 .LEHE33-.LEHB33
	.uleb128 .L1787-.LFB5111
	.uleb128 0
	.uleb128 .LEHB34-.LFB5111
	.uleb128 .LEHE34-.LEHB34
	.uleb128 .L1789-.LFB5111
	.uleb128 0
	.uleb128 .LEHB35-.LFB5111
	.uleb128 .LEHE35-.LEHB35
	.uleb128 .L1787-.LFB5111
	.uleb128 0
	.uleb128 .LEHB36-.LFB5111
	.uleb128 .LEHE36-.LEHB36
	.uleb128 0
	.uleb128 0
.LLSDACSE5111:
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
.LFB5108:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$408, %rsp
	.seh_stackalloc	408
	movaps	%xmm6, 384(%rsp)
	.seh_savexmm	%xmm6, 384
	.seh_endprologue
	movzbl	1(%rcx), %eax
	movl	%eax, %edx
	movq	%rcx, %rbx
	movapd	%xmm1, %xmm6
	movq	%r8, 496(%rsp)
	leaq	176(%rsp), %rbp
	andl	$6, %edx
	movq	$0, 168(%rsp)
	movq	%rbp, 160(%rsp)
	movb	$0, 176(%rsp)
	jne	.L2124
	shrb	$3, %al
	andl	$15, %eax
	cmpb	$7, %al
	ja	.L1905
	leaq	.L2029(%rip), %rdx
	movzbl	%al, %eax
	movslq	(%rdx,%rax,4), %rax
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L2029:
	.long	.L1905-.L2029
	.long	.L2030-.L2029
	.long	.L2060-.L2029
	.long	.L2061-.L2029
	.long	.L2062-.L2029
	.long	.L2063-.L2029
	.long	.L2064-.L2029
	.long	.L2059-.L2029
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L1905:
	leaq	112(%rsp), %r13
	movapd	%xmm6, %xmm3
	xorl	%r14d, %r14d
	leaq	257(%rsp), %rdx
	movq	%r13, %rcx
	xorl	%edi, %edi
	leaq	384(%rsp), %r8
	xorl	%r12d, %r12d
	call	_ZSt8to_charsPcS_d
	movq	112(%rsp), %rsi
	movq	120(%rsp), %rax
.L1904:
	movq	$6, 56(%rsp)
	xorl	%r15d, %r15d
	cmpl	$132, %eax
	je	.L2058
	leaq	384(%rsp), %rax
	movq	%rax, 64(%rsp)
	leaq	257(%rsp), %r13
.L1902:
	testb	%r12b, %r12b
	je	.L1932
	cmpq	%rsi, %r13
	movq	__imp_toupper(%rip), %r12
	movq	%r13, %r14
	je	.L1934
	.p2align 4,,10
	.p2align 3
.L1933:
	movsbl	(%r14), %ecx
	addq	$1, %r14
	call	*%r12
	movb	%al, -1(%r14)
	cmpq	%r14, %rsi
	jne	.L1933
.L1934:
	movsbl	%dil, %ecx
	call	*%r12
	movl	%eax, %edi
.L1932:
	movmskpd	%xmm6, %eax
	movzbl	(%rbx), %r9d
	testb	$1, %al
	jne	.L1935
	movl	%r9d, %eax
	andl	$12, %eax
	cmpb	$4, %al
	je	.L2125
	cmpb	$12, %al
	jne	.L1935
	movb	$32, -1(%r13)
	movzbl	(%rbx), %r9d
	subq	$1, %r13
	.p2align 4,,10
	.p2align 3
.L1935:
	movq	%rsi, %r12
	subq	%r13, %r12
	testb	$16, %r9b
	je	.L1937
	movsd	.LC31(%rip), %xmm1
	movapd	%xmm6, %xmm0
	andpd	.LC30(%rip), %xmm0
	ucomisd	%xmm0, %xmm1
	jb	.L1937
	testq	%r12, %r12
	je	.L2041
	movq	%r12, %r8
	movl	$46, %edx
	movq	%r13, %rcx
	movb	%r9b, 72(%rsp)
	call	memchr
	movzbl	72(%rsp), %r9d
	testq	%rax, %rax
	movq	%rax, %r10
	je	.L1939
	subq	%r13, %r10
	cmpq	$-1, %r10
	je	.L1939
	leaq	1(%r10), %rax
	movq	%r12, 80(%rsp)
	cmpq	%r12, %rax
	jnb	.L1940
	movq	%r12, %r8
	movsbl	%dil, %edx
	movq	%r10, 88(%rsp)
	leaq	0(%r13,%rax), %rcx
	subq	%rax, %r8
	call	memchr
	movzbl	72(%rsp), %r9d
	testq	%rax, %rax
	movq	88(%rsp), %r10
	je	.L1940
	subq	%r13, %rax
	cmpq	$-1, %rax
	cmove	%r12, %rax
	movq	%rax, 80(%rsp)
.L1940:
	cmpq	%r10, 80(%rsp)
	sete	88(%rsp)
	sete	%al
	testb	%r15b, %r15b
	movzbl	%al, %eax
	movq	%rax, 72(%rsp)
	jne	.L1941
	xorl	%r15d, %r15d
.L1942:
	cmpq	$0, 72(%rsp)
	je	.L1937
.L2026:
	movq	168(%rsp), %r9
	movq	72(%rsp), %rdx
	testq	%r9, %r9
	leaq	(%r12,%rdx), %rax
	movq	%rax, 56(%rsp)
	jne	.L1944
	movq	64(%rsp), %rax
	subq	%rsi, %rax
	cmpq	%rdx, %rax
	jnb	.L2126
	cmpq	%rbp, 160(%rsp)
	je	.L2127
	movq	176(%rsp), %rax
	movq	56(%rsp), %rsi
	cmpq	%rsi, %rax
	jnb	.L1953
.L1952:
	cmpq	$0, 56(%rsp)
	js	.L2022
	addq	%rax, %rax
	cmpq	%rax, 56(%rsp)
	jnb	.L1955
	testq	%rax, %rax
	jns	.L2128
.L1956:
	leaq	160(%rsp), %rsi
.LEHB37:
	call	_ZSt17__throw_bad_allocv
.L1967:
	movq	%r12, %rcx
	movq	%r12, %r14
	addq	$1, %rcx
	js	.L1974
.L1975:
	leaq	160(%rsp), %rsi
	call	_Znwy
.LEHE37:
	cmpq	$1, %r14
	movq	%rax, %r10
	je	.L2129
.L1968:
	movq	%r10, %rcx
	movq	%r14, %r8
	movq	%r13, %rdx
	call	memcpy
	movq	%r12, %rsi
	movq	%r14, %r12
	movq	%rax, %r10
.L1976:
	movq	160(%rsp), %rcx
	cmpq	%rbp, %rcx
	je	.L1977
	movq	176(%rsp), %rax
	movq	%r10, 56(%rsp)
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	56(%rsp), %r10
.L1977:
	movq	%r10, 160(%rsp)
	movq	%rsi, 176(%rsp)
.L1972:
	cmpb	$0, 88(%rsp)
	movq	%r12, 168(%rsp)
	movb	$0, (%r10,%r12)
	jne	.L2130
.L1978:
	testq	%r15, %r15
	movq	168(%rsp), %r12
	jne	.L2131
.L1980:
	movq	160(%rsp), %r13
	movzbl	(%rbx), %r9d
	.p2align 4,,10
	.p2align 3
.L1937:
	leaq	208(%rsp), %rsi
	andl	$32, %r9d
	movq	$0, 144(%rsp)
	movb	$0, 152(%rsp)
	movq	%rsi, 192(%rsp)
	movq	$0, 200(%rsp)
	movb	$0, 208(%rsp)
	je	.L2051
	movq	496(%rsp), %rax
	cmpb	$0, 32(%rax)
	leaq	24(%rax), %r15
	je	.L2132
.L1995:
	leaq	136(%rsp), %r14
	movq	%r15, %rdx
	movq	%r14, %rcx
	call	_ZNSt6localeC1ERKS_
	leaq	224(%rsp), %rcx
	movq	%r14, %r9
	movsbl	%dil, %r8d
	leaq	96(%rsp), %rdx
	movq	%r12, 96(%rsp)
	movq	%r13, 104(%rsp)
.LEHB38:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE38:
	movq	224(%rsp), %rax
	leaq	240(%rsp), %rdi
	movq	192(%rsp), %rcx
	movq	232(%rsp), %r8
	cmpq	%rdi, %rax
	je	.L2133
	movq	%r8, %xmm0
	cmpq	%rsi, %rcx
	movhps	240(%rsp), %xmm0
	je	.L2134
	testq	%rcx, %rcx
	movq	208(%rsp), %rdx
	movq	%rax, 192(%rsp)
	movups	%xmm0, 200(%rsp)
	je	.L2003
	movq	%rcx, 224(%rsp)
	movq	%rdx, 240(%rsp)
.L2002:
	movq	$0, 232(%rsp)
	movb	$0, (%rcx)
	movq	224(%rsp), %rcx
	cmpq	%rdi, %rcx
	je	.L2004
	movq	240(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L2004:
	movq	%r14, %rcx
	call	_ZNSt6localeD1Ev
	movzwl	(%rbx), %eax
	movq	200(%rsp), %r12
	movq	192(%rsp), %rdi
	andw	$384, %ax
	cmpw	$128, %ax
	je	.L2135
.L2005:
	cmpw	$256, %ax
	je	.L2007
	movq	496(%rsp), %rax
	movq	16(%rax), %r14
.L2011:
	leaq	96(%rsp), %rdx
	movq	%r14, %rcx
	movq	%r12, 96(%rsp)
	movq	%rdi, 104(%rsp)
.LEHB39:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L2120:
	movq	192(%rsp), %rcx
	movq	%rax, %rbx
	cmpq	%rsi, %rcx
	je	.L2015
	movq	208(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L2015:
	cmpb	$0, 152(%rsp)
	jne	.L2136
.L2016:
	movq	160(%rsp), %rcx
	cmpq	%rbp, %rcx
	je	.L2080
	movq	176(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	nop
.L2080:
	movaps	384(%rsp), %xmm6
	movq	%rbx, %rax
	addq	$408, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L2051:
	movzwl	(%rbx), %eax
	movq	%r13, %rdi
	andw	$384, %ax
	cmpw	$128, %ax
	jne	.L2005
.L2135:
	movzwl	4(%rbx), %eax
.L2006:
	movq	496(%rsp), %rdx
	cmpq	%rax, %r12
	movq	16(%rdx), %r14
	jnb	.L2011
	movzbl	(%rbx), %edx
	subq	%r12, %rax
	movzbl	8(%rbx), %ecx
	movq	%rax, %rbx
	movl	%edx, %r8d
	andl	$3, %r8d
	movsbl	%cl, %eax
	jne	.L2013
	andl	$64, %edx
	je	.L2053
	movsd	.LC31(%rip), %xmm0
	andpd	.LC30(%rip), %xmm6
	ucomisd	%xmm6, %xmm0
	jnb	.L2137
.L2053:
	movl	$32, %eax
	movl	$2, %r8d
.L2013:
	leaq	96(%rsp), %rdx
	movl	%eax, 32(%rsp)
	movq	%rbx, %r9
	movq	%r14, %rcx
	movq	%r12, 96(%rsp)
	movq	%rdi, 104(%rsp)
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
.LEHE39:
	jmp	.L2120
	.p2align 4,,10
	.p2align 3
.L2124:
	cmpb	$2, %dl
	je	.L2138
	movq	$-1, 56(%rsp)
	cmpb	$4, %dl
	je	.L2139
.L1888:
	shrb	$3, %al
	andl	$15, %eax
	cmpb	$7, %al
	ja	.L1891
	leaq	.L1893(%rip), %rdx
	movzbl	%al, %eax
	movslq	(%rdx,%rax,4), %rax
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L1893:
	.long	.L1900-.L1893
	.long	.L2032-.L1893
	.long	.L1898-.L1893
	.long	.L1897-.L1893
	.long	.L2114-.L1893
	.long	.L2116-.L1893
	.long	.L1894-.L1893
	.long	.L2115-.L1893
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2136:
	leaq	144(%rsp), %rcx
	call	_ZNSt6localeD1Ev
	jmp	.L2016
	.p2align 4,,10
	.p2align 3
.L2060:
	movl	$1, %r12d
.L1903:
	leaq	112(%rsp), %r13
	movl	$4, 32(%rsp)
	movapd	%xmm6, %xmm3
	movl	$4, %r14d
	leaq	257(%rsp), %rdx
	movq	%r13, %rcx
	movl	$112, %edi
	leaq	384(%rsp), %r8
	call	_ZSt8to_charsPcS_dSt12chars_format
	movq	112(%rsp), %rsi
	movq	120(%rsp), %rax
	jmp	.L1904
	.p2align 4,,10
	.p2align 3
.L2137:
	movzbl	0(%r13), %edx
	leaq	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE(%rip), %rcx
	movl	$48, %eax
	movl	$2, %r8d
	cmpb	$15, (%rcx,%rdx)
	jbe	.L2013
	movq	24(%r14), %rax
	movzbl	(%rdi), %edx
	leaq	1(%rax), %rcx
	movq	%rcx, 24(%r14)
	movb	%dl, (%rax)
	movq	24(%r14), %rax
	subq	8(%r14), %rax
	cmpq	16(%r14), %rax
	je	.L2140
.L2014:
	addq	$1, %rdi
	subq	$1, %r12
	movl	$48, %eax
	movl	$2, %r8d
	jmp	.L2013
	.p2align 4,,10
	.p2align 3
.L2041:
	xorl	%eax, %eax
.L1938:
	testb	%r15b, %r15b
	je	.L2141
	movb	%r15b, 88(%rsp)
	movq	%rax, 80(%rsp)
	movq	$1, 72(%rsp)
	jmp	.L2025
	.p2align 4,,10
	.p2align 3
.L2061:
	movq	$6, 56(%rsp)
.L1897:
	xorl	%r12d, %r12d
.L1896:
	movl	$1, %r14d
	movl	$101, %edi
	xorl	%r15d, %r15d
.L1899:
	movl	56(%rsp), %esi
	leaq	112(%rsp), %r13
	movl	%r14d, 32(%rsp)
	movapd	%xmm6, %xmm3
	leaq	257(%rsp), %rax
	movq	%r13, %rcx
	leaq	384(%rsp), %r8
	movq	%rax, %rdx
	movq	%rax, 72(%rsp)
	movl	%esi, 40(%rsp)
	call	_ZSt8to_charsPcS_dSt12chars_formati
	cmpl	$132, 120(%rsp)
	movq	112(%rsp), %rsi
	je	.L1901
	leaq	384(%rsp), %rax
	movq	72(%rsp), %r13
	movq	%rax, 64(%rsp)
	jmp	.L1902
	.p2align 4,,10
	.p2align 3
.L2062:
	movq	$6, 56(%rsp)
.L2114:
	movl	$1, %r12d
	jmp	.L1896
	.p2align 4,,10
	.p2align 3
.L2063:
	movq	$6, 56(%rsp)
.L2116:
	movl	$2, %r14d
	xorl	%edi, %edi
	xorl	%r15d, %r15d
	xorl	%r12d, %r12d
	jmp	.L1899
	.p2align 4,,10
	.p2align 3
.L2059:
	movq	$6, 56(%rsp)
.L2115:
	movl	$1, %r12d
.L1892:
	movl	$3, %r14d
	movl	$101, %edi
	movl	$1, %r15d
	jmp	.L1899
	.p2align 4,,10
	.p2align 3
.L2064:
	movq	$6, 56(%rsp)
.L1894:
	xorl	%r12d, %r12d
	jmp	.L1892
	.p2align 4,,10
	.p2align 3
.L2030:
	xorl	%r12d, %r12d
	jmp	.L1903
	.p2align 4,,10
	.p2align 3
.L2139:
	movq	496(%rsp), %rdi
	movb	$0, 208(%rsp)
	movzwl	6(%rcx), %eax
	movzbl	(%rdi), %edx
	movl	%edx, %ecx
	andl	$15, %edx
	andl	$15, %ecx
	cmpq	%rdx, %rax
	jb	.L2142
	testb	%cl, %cl
	jne	.L1890
	movq	496(%rsp), %rdi
	movq	(%rdi), %rdi
	movq	%rdi, %rdx
	movq	%rdi, 56(%rsp)
	shrq	$4, %rdx
	cmpq	%rdx, %rax
	jnb	.L1890
	movq	496(%rsp), %rdi
	salq	$5, %rax
	addq	8(%rdi), %rax
	movq	(%rax), %rdx
	movq	%rdx, 192(%rsp)
	movq	8(%rax), %rdx
	movq	%rdx, 200(%rsp)
	movzbl	16(%rax), %eax
	movb	%al, 208(%rsp)
	.p2align 4,,10
	.p2align 3
.L1890:
	leaq	192(%rsp), %rcx
	leaq	160(%rsp), %rsi
.LEHB40:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE40:
	movq	%rax, 56(%rsp)
	movzbl	1(%rbx), %eax
	jmp	.L1888
	.p2align 4,,10
	.p2align 3
.L2125:
	movb	$43, -1(%r13)
	subq	$1, %r13
	movzbl	(%rbx), %r9d
	jmp	.L1935
	.p2align 4,,10
	.p2align 3
.L2132:
	movq	%r15, %rcx
	call	_ZNSt6localeC1Ev
	movq	496(%rsp), %rax
	movb	$1, 32(%rax)
	jmp	.L1995
	.p2align 4,,10
	.p2align 3
.L2007:
	movq	496(%rsp), %rdx
	movb	$0, 240(%rsp)
	movzwl	4(%rbx), %eax
	movzbl	(%rdx), %edx
	movl	%edx, %ecx
	andl	$15, %edx
	andl	$15, %ecx
	cmpq	%rdx, %rax
	jb	.L2143
	testb	%cl, %cl
	jne	.L2010
	movq	496(%rsp), %rdx
	movq	(%rdx), %rdx
	movq	%rdx, 56(%rsp)
	shrq	$4, %rdx
	cmpq	%rdx, %rax
	jnb	.L2010
	movq	496(%rsp), %rdx
	salq	$5, %rax
	addq	8(%rdx), %rax
	movq	(%rax), %rdx
	movq	%rdx, 224(%rsp)
	movq	8(%rax), %rdx
	movq	%rdx, 232(%rsp)
	movzbl	16(%rax), %eax
	movb	%al, 240(%rsp)
	.p2align 4,,10
	.p2align 3
.L2010:
	leaq	224(%rsp), %rcx
.LEHB41:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE41:
	jmp	.L2006
	.p2align 4,,10
	.p2align 3
.L2134:
	movq	%rax, 192(%rsp)
	movups	%xmm0, 200(%rsp)
.L2003:
	movq	%rdi, 224(%rsp)
	leaq	240(%rsp), %rdi
	movq	%rdi, %rcx
	jmp	.L2002
	.p2align 4,,10
	.p2align 3
.L2138:
	movzwl	6(%rcx), %edi
	movq	%rdi, 56(%rsp)
	jmp	.L1888
	.p2align 4,,10
	.p2align 3
.L2133:
	testq	%r8, %r8
	je	.L1998
	cmpq	$1, %r8
	je	.L2144
	movq	%rdi, %rdx
	call	memcpy
	movq	232(%rsp), %r8
	movq	192(%rsp), %rcx
.L1998:
	movq	%r8, 200(%rsp)
	movb	$0, (%rcx,%r8)
	movq	224(%rsp), %rcx
	jmp	.L2002
	.p2align 4,,10
	.p2align 3
.L1941:
	movq	80(%rsp), %rax
	subq	$1, %rax
.L2025:
	movzbl	0(%r13), %edx
	leaq	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE(%rip), %rcx
	movq	56(%rsp), %r15
	cmpb	$16, (%rcx,%rdx)
	adcq	$-1, %rax
	subq	%rax, %r15
	addq	%r15, 72(%rsp)
	jmp	.L1942
	.p2align 4,,10
	.p2align 3
.L2058:
	movb	$0, 72(%rsp)
	movq	$134, 64(%rsp)
.L1906:
	movq	160(%rsp), %r9
	cmpq	%rbp, %r9
	je	.L2038
	movq	176(%rsp), %rax
.L1908:
	movq	64(%rsp), %rsi
	cmpq	%rsi, %rax
	jb	.L2145
.L1931:
	cmpq	%rbp, %r9
	je	.L2039
	movq	176(%rsp), %rax
	leaq	(%rax,%rax), %rsi
	cmpq	%rsi, %rax
	movq	%rsi, 64(%rsp)
	jb	.L2146
.L1920:
	movq	64(%rsp), %rax
	leaq	1(%r9), %rdx
	movq	%r9, 64(%rsp)
	cmpb	$0, 72(%rsp)
	leaq	-1(%r9,%rax), %r8
	jne	.L2147
	testl	%r14d, %r14d
	jne	.L2148
	movapd	%xmm6, %xmm3
	movq	%r13, %rcx
	call	_ZSt8to_charsPcS_d
	movq	112(%rsp), %rsi
	movq	120(%rsp), %rax
	movq	64(%rsp), %r9
.L1928:
	testl	%eax, %eax
	jne	.L1930
	movq	160(%rsp), %rdx
	movq	%rsi, %rax
	subq	%r9, %rax
	movq	%rax, 168(%rsp)
	movb	$0, (%rdx,%rax)
	movq	160(%rsp), %rax
	leaq	1(%rax), %r13
	addq	168(%rsp), %rax
	movq	%rax, 64(%rsp)
	jmp	.L1902
	.p2align 4,,10
	.p2align 3
.L1939:
	movsbl	%dil, %edx
	movq	%r12, %r8
	movq	%r13, %rcx
	movb	%r9b, 72(%rsp)
	call	memchr
	movzbl	72(%rsp), %r9d
	testq	%rax, %rax
	je	.L2045
	subq	%r13, %rax
	cmpq	$-1, %rax
	cmove	%r12, %rax
	jmp	.L1938
.L2032:
	movl	$4, %r14d
	movl	$112, %edi
	xorl	%r15d, %r15d
	xorl	%r12d, %r12d
	jmp	.L1899
.L1898:
	movl	$4, %r14d
	movl	$112, %edi
	xorl	%r15d, %r15d
	movl	$1, %r12d
	jmp	.L1899
.L1900:
	movl	$3, %r14d
	xorl	%edi, %edi
	xorl	%r15d, %r15d
	xorl	%r12d, %r12d
	jmp	.L1899
.L2141:
	movq	%rax, 80(%rsp)
	xorl	%r15d, %r15d
	movq	$1, 72(%rsp)
	movb	$1, 88(%rsp)
	jmp	.L2026
.L2148:
	movl	%r14d, 32(%rsp)
	movapd	%xmm6, %xmm3
	movq	%r13, %rcx
	call	_ZSt8to_charsPcS_dSt12chars_format
	movq	112(%rsp), %rsi
	movq	120(%rsp), %rax
	movq	64(%rsp), %r9
	jmp	.L1928
.L2142:
	movq	(%rdi), %rdi
	leaq	(%rax,%rax,4), %rcx
	salq	$4, %rax
	movq	%rdi, %rdx
	movq	%rdi, 56(%rsp)
	movq	496(%rsp), %rdi
	shrq	$4, %rdx
	shrq	%cl, %rdx
	andl	$31, %edx
	addq	8(%rdi), %rax
	movb	%dl, 208(%rsp)
	movq	(%rax), %rdx
	movq	%rdx, 192(%rsp)
	movq	8(%rax), %rax
	movq	%rax, 200(%rsp)
	jmp	.L1890
.L2045:
	movq	%r12, %rax
	jmp	.L1938
.L2127:
	movq	56(%rsp), %rax
	cmpq	$15, %rax
	ja	.L2123
	movq	80(%rsp), %rax
	cmpq	%rax, %r12
	cmova	%rax, %r12
	testq	%r12, %r12
	js	.L1960
	movq	%rbp, %r10
.L2027:
	cmpq	$15, %r12
	ja	.L2149
.L1966:
	cmpq	%r10, %r13
	jb	.L1970
	cmpq	%r13, %r10
	jb	.L1970
	xorl	%eax, %eax
	movq	%r12, 32(%rsp)
	movq	%r13, %r9
	xorl	%r8d, %r8d
	leaq	160(%rsp), %rsi
	movq	%rax, 40(%rsp)
	movq	%r10, %rdx
	movq	%rsi, %rcx
.LEHB42:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	movq	160(%rsp), %r10
	jmp	.L1972
	.p2align 4,,10
	.p2align 3
.L1930:
	movq	160(%rsp), %rdx
	cmpl	$132, %eax
	movq	$0, 168(%rsp)
	movb	$0, (%rdx)
	movq	160(%rsp), %r9
	movq	168(%rsp), %rdx
	je	.L1931
	leaq	(%r9,%rdx), %rax
	leaq	1(%r9), %r13
	movq	%rax, 64(%rsp)
	jmp	.L1902
	.p2align 4,,10
	.p2align 3
.L2145:
	testq	%rsi, %rsi
	js	.L2150
	addq	%rax, %rax
	cmpq	%rax, 64(%rsp)
	jnb	.L1911
	testq	%rax, %rax
	js	.L1912
	leaq	1(%rax), %rcx
	movq	%rax, 64(%rsp)
.L1913:
	leaq	160(%rsp), %rsi
	call	_Znwy
	movq	%rax, %r9
	movq	168(%rsp), %rax
	movq	160(%rsp), %rsi
	leaq	1(%rax), %r8
	testq	%rax, %rax
	je	.L2151
	testq	%r8, %r8
	je	.L2117
	movq	%r9, %rcx
	movq	%rsi, %rdx
	call	memcpy
	movq	%rax, %r9
.L2117:
	cmpq	%rbp, %rsi
	je	.L1916
	movq	176(%rsp), %rax
	movq	%rsi, %rcx
	movq	%r9, 80(%rsp)
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	80(%rsp), %r9
.L1916:
	movq	64(%rsp), %rax
	movq	%r9, 160(%rsp)
	movq	%rax, 176(%rsp)
	jmp	.L1931
.L2143:
	movq	496(%rsp), %rdx
	leaq	(%rax,%rax,4), %rcx
	salq	$4, %rax
	movq	(%rdx), %rdx
	movq	%rdx, 56(%rsp)
	shrq	$4, %rdx
	shrq	%cl, %rdx
	andl	$31, %edx
	movb	%dl, 240(%rsp)
	movq	496(%rsp), %rdx
	addq	8(%rdx), %rax
	movq	(%rax), %rdx
	movq	%rdx, 224(%rsp)
	movq	8(%rax), %rax
	movq	%rax, 232(%rsp)
	jmp	.L2010
.L1944:
	cmpq	%rbp, 160(%rsp)
	je	.L1950
	movq	176(%rsp), %rax
	movq	56(%rsp), %rsi
	cmpq	%rsi, %rax
	jb	.L1952
.L1951:
	movq	80(%rsp), %rax
	cmpq	%rax, %r9
	jb	.L2152
.L1963:
	movabsq	$9223372036854775807, %rax
	movq	72(%rsp), %rsi
	subq	%r9, %rax
	cmpq	%rsi, %rax
	jb	.L2153
	movq	72(%rsp), %rax
	leaq	(%r9,%rax), %r12
	movq	160(%rsp), %rax
	cmpq	%rbp, %rax
	je	.L2050
	movq	176(%rsp), %rdx
.L1987:
	cmpq	%r12, %rdx
	jb	.L1988
	movq	80(%rsp), %rsi
	leaq	(%rax,%rsi), %rcx
	subq	%rsi, %r9
	je	.L1989
	movq	72(%rsp), %rax
	addq	%rcx, %rax
	cmpq	$1, %r9
	je	.L2154
	movq	%rcx, %rdx
	movq	%r9, %r8
	movq	%rax, %rcx
	call	memmove
	movq	80(%rsp), %rcx
	addq	160(%rsp), %rcx
.L1989:
	cmpq	$1, 72(%rsp)
	je	.L2155
	movq	72(%rsp), %r8
	movl	$48, %edx
	call	memset
.L1992:
	movq	160(%rsp), %rax
	movq	%r12, 168(%rsp)
	cmpb	$0, 88(%rsp)
	movb	$0, (%rax,%r12)
	movq	168(%rsp), %r12
	je	.L1980
	movq	160(%rsp), %rax
	movq	80(%rsp), %rsi
	movb	$46, (%rax,%rsi)
	movq	168(%rsp), %r12
	jmp	.L1980
.L1955:
	movq	56(%rsp), %rcx
	addq	$1, %rcx
	js	.L1956
.L1957:
	leaq	160(%rsp), %rsi
	call	_Znwy
	movq	168(%rsp), %r9
	movq	%rax, %rsi
	movq	160(%rsp), %r14
	leaq	1(%r9), %r8
	testq	%r9, %r9
	je	.L2156
	testq	%r8, %r8
	jne	.L1962
	cmpq	%rbp, %r14
	je	.L2157
.L1959:
	movq	176(%rsp), %rax
	movq	%r14, %rcx
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	168(%rsp), %r9
	movq	%rsi, 160(%rsp)
	movq	56(%rsp), %rax
	testq	%r9, %r9
	movq	%rax, 176(%rsp)
	jne	.L1951
.L1953:
	movq	80(%rsp), %rax
	cmpq	%rax, %r12
	cmova	%rax, %r12
	testq	%r12, %r12
	js	.L1960
	movq	160(%rsp), %r10
	cmpq	%rbp, %r10
	je	.L2027
.L1965:
	movq	176(%rsp), %rax
	cmpq	%r12, %rax
	jnb	.L1966
	addq	%rax, %rax
	cmpq	%rax, %r12
	jnb	.L1967
	leaq	1(%rax), %rcx
	testq	%rax, %rax
	movq	%r12, %r14
	movq	%rax, %r12
	jns	.L1975
.L1974:
	leaq	160(%rsp), %rsi
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L1911:
	movq	64(%rsp), %rcx
	addq	$1, %rcx
	jns	.L1913
.L1912:
	leaq	160(%rsp), %rsi
	call	_ZSt17__throw_bad_allocv
.L2147:
	movl	56(%rsp), %eax
	movl	%r14d, 32(%rsp)
	movapd	%xmm6, %xmm3
	movq	%r13, %rcx
	movl	%eax, 40(%rsp)
	call	_ZSt8to_charsPcS_dSt12chars_formati
	movq	112(%rsp), %rsi
	movq	120(%rsp), %rax
	movq	64(%rsp), %r9
	jmp	.L1928
.L1901:
	movq	56(%rsp), %rax
	cmpl	$2, %r14d
	movb	$1, 72(%rsp)
	leaq	128(%rax), %rsi
	movq	%rsi, 64(%rsp)
	jne	.L1906
	cvttsd2sil	%xmm6, %eax
	pxor	%xmm0, %xmm0
	cltd
	xorl	%edx, %eax
	subl	%edx, %eax
	cvtsi2sdl	%eax, %xmm0
	call	log10
	cvttsd2sil	%xmm0, %edx
	movl	%edx, %eax
	sarl	%eax
	cmpl	$1, %edx
	movl	$1, %edx
	cltq
	cmovle	%rdx, %rax
	addq	%rax, %rsi
	movq	%rsi, 64(%rsp)
	jmp	.L1906
.L1970:
	testq	%r12, %r12
	je	.L1972
	cmpq	$1, %r12
	je	.L2158
	movq	%r10, %rcx
	movq	%r12, %r8
	movq	%r13, %rdx
	call	memcpy
	movq	160(%rsp), %r10
	jmp	.L1972
.L2126:
	movq	80(%rsp), %rax
	movq	%rdx, %rcx
	movq	%r12, %r8
	leaq	0(%r13,%rax), %rsi
	addq	%rax, %rcx
	subq	%rax, %r8
	addq	%r13, %rcx
	movq	%rsi, %rdx
	call	memmove
	cmpb	$0, 88(%rsp)
	je	.L1947
	movq	80(%rsp), %rax
	movb	$46, (%rsi)
	leaq	1(%r13,%rax), %rsi
.L1947:
	movq	%r15, %r8
	movl	$48, %edx
	movq	%rsi, %rcx
	call	memset
	movzbl	(%rbx), %r9d
	movq	56(%rsp), %r12
	jmp	.L1937
.L2039:
	movq	$30, 64(%rsp)
	movl	$31, %ecx
.L1919:
	leaq	160(%rsp), %rsi
	call	_Znwy
	movq	168(%rsp), %r8
	movq	%rax, %r9
	movq	160(%rsp), %rsi
	cmpq	$1, %r8
	je	.L2159
	testq	%r8, %r8
	je	.L2119
	movq	%rsi, %rdx
	movq	%rax, %rcx
	call	memcpy
	movq	%rax, %r9
.L2119:
	cmpq	%rbp, %rsi
	je	.L1924
	movq	176(%rsp), %rax
	movq	%rsi, %rcx
	movq	%r9, 80(%rsp)
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	80(%rsp), %r9
.L1924:
	movq	64(%rsp), %rax
	movq	%r9, 160(%rsp)
	movq	%rax, 176(%rsp)
	jmp	.L1920
.L2038:
	movl	$15, %eax
	jmp	.L1908
.L2146:
	testq	%rsi, %rsi
	js	.L1921
	leaq	1(%rsi), %rcx
	jmp	.L1919
.L1988:
	movq	72(%rsp), %rax
	leaq	160(%rsp), %rsi
	xorl	%r9d, %r9d
	xorl	%r8d, %r8d
	movq	80(%rsp), %r15
	movq	%rsi, %rcx
	movq	%rax, 32(%rsp)
	movq	%r15, %rdx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	movq	160(%rsp), %rcx
	addq	%r15, %rcx
	jmp	.L1989
.L2151:
	movzbl	(%rsi), %eax
	movb	%al, (%r9)
	jmp	.L2117
.L2156:
	movzbl	(%r14), %eax
	cmpq	%rbp, %r14
	movb	%al, (%rsi)
	jne	.L1959
	movq	56(%rsp), %rax
	movq	%rsi, 160(%rsp)
	movq	%rax, 176(%rsp)
	movq	80(%rsp), %rax
	cmpq	%rax, %r12
	cmova	%rax, %r12
	testq	%r12, %r12
	js	.L1960
	movq	%rsi, %r10
	jmp	.L1965
.L2131:
	movabsq	$9223372036854775807, %rax
	subq	%r12, %rax
	cmpq	%r15, %rax
	jb	.L2160
	movq	160(%rsp), %rax
	leaq	(%r12,%r15), %r13
	cmpq	%rbp, %rax
	je	.L2049
	movq	176(%rsp), %rdx
.L1982:
	cmpq	%r13, %rdx
	jb	.L2161
.L1983:
	leaq	(%rax,%r12), %rcx
	cmpq	$1, %r15
	je	.L2162
	movq	%r15, %r8
	movl	$48, %edx
	call	memset
.L1985:
	movq	160(%rsp), %rax
	movq	%r13, 168(%rsp)
	movb	$0, (%rax,%r13)
	movq	168(%rsp), %r12
	jmp	.L1980
.L1962:
	movq	%r14, %rdx
	movq	%rax, %rcx
	movq	%r9, 64(%rsp)
	call	memcpy
	cmpq	%rbp, %r14
	movq	64(%rsp), %r9
	jne	.L1959
	movq	56(%rsp), %rax
	movq	%rsi, 160(%rsp)
	movq	%rax, 176(%rsp)
	jmp	.L1951
.L2144:
	movzbl	240(%rsp), %eax
	movb	%al, (%rcx)
	movq	232(%rsp), %r8
	movq	192(%rsp), %rcx
	jmp	.L1998
.L2159:
	movzbl	(%rsi), %eax
	movb	%al, (%r9)
	jmp	.L2119
.L2130:
	leaq	160(%rsp), %rsi
	movl	$46, %edx
	movq	%rsi, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	jmp	.L1978
.L1950:
	movq	56(%rsp), %rax
	cmpq	$15, %rax
	jbe	.L1951
.L2123:
	testq	%rax, %rax
	js	.L2022
	cmpq	$29, %rax
	ja	.L1955
	movq	$30, 56(%rsp)
.L2023:
	movq	56(%rsp), %rax
	leaq	1(%rax), %rcx
	jmp	.L1957
.L2050:
	movl	$15, %edx
	jmp	.L1987
.L2155:
	movb	$48, (%rcx)
	jmp	.L1992
.L2154:
	movzbl	(%rcx), %edx
	movb	%dl, (%rax)
	movq	160(%rsp), %rcx
	addq	%rsi, %rcx
	jmp	.L1989
.L2158:
	movzbl	0(%r13), %eax
	movb	%al, (%r10)
	movq	160(%rsp), %r10
	jmp	.L1972
.L2161:
	movq	%r15, 32(%rsp)
	xorl	%r9d, %r9d
	xorl	%r8d, %r8d
	movq	%r12, %rdx
	leaq	160(%rsp), %rsi
	movq	%rsi, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE42:
	movq	160(%rsp), %rax
	jmp	.L1983
.L2140:
	movq	(%r14), %rax
	movq	%r14, %rcx
.LEHB43:
	call	*(%rax)
.LEHE43:
	jmp	.L2014
.L2149:
	cmpq	$29, %r12
	ja	.L1967
	leaq	160(%rsp), %rsi
	movl	$31, %ecx
.LEHB44:
	call	_Znwy
	movq	%r12, %r14
	movq	%rax, %r10
	movl	$30, %r12d
	jmp	.L1968
.L2162:
	movb	$48, (%rcx)
	jmp	.L1985
.L2049:
	movl	$15, %edx
	jmp	.L1982
.L2157:
	movq	%rax, 160(%rsp)
	movq	56(%rsp), %rax
	movq	$-1, %r9
	movq	%rax, 176(%rsp)
	jmp	.L1963
.L2129:
	movzbl	0(%r13), %eax
	movq	%r12, %rsi
	movl	$1, %r12d
	movb	%al, (%r10)
	jmp	.L1976
.L2128:
	movq	%rax, 56(%rsp)
	jmp	.L2023
.L2150:
	leaq	.LC7(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L1921:
	leaq	.LC7(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L2022:
	leaq	.LC7(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L2153:
	leaq	.LC26(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L2152:
	leaq	.LC27(%rip), %rdx
	movq	%rax, %r8
	leaq	.LC28(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L1960:
	leaq	.LC25(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L2160:
	leaq	.LC26(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.LEHE44:
.L1891:
	xorl	%r14d, %r14d
	xorl	%edi, %edi
	xorl	%r15d, %r15d
	xorl	%r12d, %r12d
	jmp	.L1899
.L2065:
	movq	%rax, %rbx
.L2021:
	movq	%rsi, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	%rbx, %rcx
.LEHB45:
	call	_Unwind_Resume
.LEHE45:
.L2067:
	movq	%rax, %rbx
	jmp	.L2019
.L2066:
	movq	%r14, %rcx
	movq	%rax, %rbx
	call	_ZNSt6localeD1Ev
.L2019:
	leaq	192(%rsp), %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	cmpb	$0, 152(%rsp)
	je	.L2020
	leaq	144(%rsp), %rcx
	call	_ZNSt6localeD1Ev
.L2020:
	leaq	160(%rsp), %rsi
	jmp	.L2021
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5108:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5108-.LLSDACSB5108
.LLSDACSB5108:
	.uleb128 .LEHB37-.LFB5108
	.uleb128 .LEHE37-.LEHB37
	.uleb128 .L2065-.LFB5108
	.uleb128 0
	.uleb128 .LEHB38-.LFB5108
	.uleb128 .LEHE38-.LEHB38
	.uleb128 .L2066-.LFB5108
	.uleb128 0
	.uleb128 .LEHB39-.LFB5108
	.uleb128 .LEHE39-.LEHB39
	.uleb128 .L2067-.LFB5108
	.uleb128 0
	.uleb128 .LEHB40-.LFB5108
	.uleb128 .LEHE40-.LEHB40
	.uleb128 .L2065-.LFB5108
	.uleb128 0
	.uleb128 .LEHB41-.LFB5108
	.uleb128 .LEHE41-.LEHB41
	.uleb128 .L2067-.LFB5108
	.uleb128 0
	.uleb128 .LEHB42-.LFB5108
	.uleb128 .LEHE42-.LEHB42
	.uleb128 .L2065-.LFB5108
	.uleb128 0
	.uleb128 .LEHB43-.LFB5108
	.uleb128 .LEHE43-.LEHB43
	.uleb128 .L2067-.LFB5108
	.uleb128 0
	.uleb128 .LEHB44-.LFB5108
	.uleb128 .LEHE44-.LEHB44
	.uleb128 .L2065-.LFB5108
	.uleb128 0
	.uleb128 .LEHB45-.LFB5108
	.uleb128 .LEHE45-.LEHB45
	.uleb128 0
	.uleb128 0
.LLSDACSE5108:
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
.LFB5104:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$408, %rsp
	.seh_stackalloc	408
	movaps	%xmm6, 384(%rsp)
	.seh_savexmm	%xmm6, 384
	.seh_endprologue
	movzbl	1(%rcx), %eax
	movl	%eax, %edx
	movq	%rcx, %rbx
	movaps	%xmm1, %xmm6
	movq	%r8, 496(%rsp)
	leaq	176(%rsp), %rbp
	andl	$6, %edx
	movq	$0, 168(%rsp)
	movq	%rbp, 160(%rsp)
	movb	$0, 176(%rsp)
	jne	.L2402
	shrb	$3, %al
	andl	$15, %eax
	cmpb	$7, %al
	ja	.L2183
	leaq	.L2307(%rip), %rdx
	movzbl	%al, %eax
	movslq	(%rdx,%rax,4), %rax
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L2307:
	.long	.L2183-.L2307
	.long	.L2308-.L2307
	.long	.L2338-.L2307
	.long	.L2339-.L2307
	.long	.L2340-.L2307
	.long	.L2341-.L2307
	.long	.L2342-.L2307
	.long	.L2337-.L2307
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2183:
	leaq	112(%rsp), %r13
	movaps	%xmm6, %xmm3
	xorl	%r14d, %r14d
	leaq	257(%rsp), %rdx
	movq	%r13, %rcx
	xorl	%edi, %edi
	leaq	384(%rsp), %r8
	xorl	%r12d, %r12d
	call	_ZSt8to_charsPcS_f
	movq	112(%rsp), %rsi
	movq	120(%rsp), %rax
.L2182:
	movq	$6, 56(%rsp)
	xorl	%r15d, %r15d
	cmpl	$132, %eax
	je	.L2336
	leaq	384(%rsp), %rax
	movq	%rax, 64(%rsp)
	leaq	257(%rsp), %r13
.L2180:
	testb	%r12b, %r12b
	je	.L2210
	cmpq	%rsi, %r13
	movq	__imp_toupper(%rip), %r12
	movq	%r13, %r14
	je	.L2212
	.p2align 4,,10
	.p2align 3
.L2211:
	movsbl	(%r14), %ecx
	addq	$1, %r14
	call	*%r12
	movb	%al, -1(%r14)
	cmpq	%r14, %rsi
	jne	.L2211
.L2212:
	movsbl	%dil, %ecx
	call	*%r12
	movl	%eax, %edi
.L2210:
	movd	%xmm6, %eax
	movzbl	(%rbx), %r9d
	testl	%eax, %eax
	js	.L2213
	movl	%r9d, %eax
	andl	$12, %eax
	cmpb	$4, %al
	je	.L2403
	cmpb	$12, %al
	jne	.L2213
	movb	$32, -1(%r13)
	movzbl	(%rbx), %r9d
	subq	$1, %r13
	.p2align 4,,10
	.p2align 3
.L2213:
	movq	%rsi, %r12
	subq	%r13, %r12
	testb	$16, %r9b
	je	.L2215
	movss	.LC33(%rip), %xmm1
	movaps	%xmm6, %xmm0
	andps	.LC32(%rip), %xmm0
	ucomiss	%xmm0, %xmm1
	jb	.L2215
	testq	%r12, %r12
	je	.L2319
	movq	%r12, %r8
	movl	$46, %edx
	movq	%r13, %rcx
	movb	%r9b, 72(%rsp)
	call	memchr
	movzbl	72(%rsp), %r9d
	testq	%rax, %rax
	movq	%rax, %r10
	je	.L2217
	subq	%r13, %r10
	cmpq	$-1, %r10
	je	.L2217
	leaq	1(%r10), %rax
	movq	%r12, 80(%rsp)
	cmpq	%r12, %rax
	jnb	.L2218
	movq	%r12, %r8
	movsbl	%dil, %edx
	movq	%r10, 88(%rsp)
	leaq	0(%r13,%rax), %rcx
	subq	%rax, %r8
	call	memchr
	movzbl	72(%rsp), %r9d
	testq	%rax, %rax
	movq	88(%rsp), %r10
	je	.L2218
	subq	%r13, %rax
	cmpq	$-1, %rax
	cmove	%r12, %rax
	movq	%rax, 80(%rsp)
.L2218:
	cmpq	%r10, 80(%rsp)
	sete	88(%rsp)
	sete	%al
	testb	%r15b, %r15b
	movzbl	%al, %eax
	movq	%rax, 72(%rsp)
	jne	.L2219
	xorl	%r15d, %r15d
.L2220:
	cmpq	$0, 72(%rsp)
	je	.L2215
.L2304:
	movq	168(%rsp), %r9
	movq	72(%rsp), %rdx
	testq	%r9, %r9
	leaq	(%r12,%rdx), %rax
	movq	%rax, 56(%rsp)
	jne	.L2222
	movq	64(%rsp), %rax
	subq	%rsi, %rax
	cmpq	%rdx, %rax
	jnb	.L2404
	cmpq	%rbp, 160(%rsp)
	je	.L2405
	movq	176(%rsp), %rax
	movq	56(%rsp), %rsi
	cmpq	%rsi, %rax
	jnb	.L2231
.L2230:
	cmpq	$0, 56(%rsp)
	js	.L2300
	addq	%rax, %rax
	cmpq	%rax, 56(%rsp)
	jnb	.L2233
	testq	%rax, %rax
	jns	.L2406
.L2234:
	leaq	160(%rsp), %rsi
.LEHB46:
	call	_ZSt17__throw_bad_allocv
.L2245:
	movq	%r12, %rcx
	movq	%r12, %r14
	addq	$1, %rcx
	js	.L2252
.L2253:
	leaq	160(%rsp), %rsi
	call	_Znwy
.LEHE46:
	cmpq	$1, %r14
	movq	%rax, %r10
	je	.L2407
.L2246:
	movq	%r10, %rcx
	movq	%r14, %r8
	movq	%r13, %rdx
	call	memcpy
	movq	%r12, %rsi
	movq	%r14, %r12
	movq	%rax, %r10
.L2254:
	movq	160(%rsp), %rcx
	cmpq	%rbp, %rcx
	je	.L2255
	movq	176(%rsp), %rax
	movq	%r10, 56(%rsp)
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	56(%rsp), %r10
.L2255:
	movq	%r10, 160(%rsp)
	movq	%rsi, 176(%rsp)
.L2250:
	cmpb	$0, 88(%rsp)
	movq	%r12, 168(%rsp)
	movb	$0, (%r10,%r12)
	jne	.L2408
.L2256:
	testq	%r15, %r15
	movq	168(%rsp), %r12
	jne	.L2409
.L2258:
	movq	160(%rsp), %r13
	movzbl	(%rbx), %r9d
	.p2align 4,,10
	.p2align 3
.L2215:
	leaq	208(%rsp), %rsi
	andl	$32, %r9d
	movq	$0, 144(%rsp)
	movb	$0, 152(%rsp)
	movq	%rsi, 192(%rsp)
	movq	$0, 200(%rsp)
	movb	$0, 208(%rsp)
	je	.L2329
	movq	496(%rsp), %rax
	cmpb	$0, 32(%rax)
	leaq	24(%rax), %r15
	je	.L2410
.L2273:
	leaq	136(%rsp), %r14
	movq	%r15, %rdx
	movq	%r14, %rcx
	call	_ZNSt6localeC1ERKS_
	leaq	224(%rsp), %rcx
	movq	%r14, %r9
	movsbl	%dil, %r8d
	leaq	96(%rsp), %rdx
	movq	%r12, 96(%rsp)
	movq	%r13, 104(%rsp)
.LEHB47:
	call	_ZNKSt8__format14__formatter_fpIcE11_M_localizeB5cxx11ESt17basic_string_viewIcSt11char_traitsIcEEcRKSt6locale.isra.0
.LEHE47:
	movq	224(%rsp), %rax
	leaq	240(%rsp), %rdi
	movq	192(%rsp), %rcx
	movq	232(%rsp), %r8
	cmpq	%rdi, %rax
	je	.L2411
	movq	%r8, %xmm0
	cmpq	%rsi, %rcx
	movhps	240(%rsp), %xmm0
	je	.L2412
	testq	%rcx, %rcx
	movq	208(%rsp), %rdx
	movq	%rax, 192(%rsp)
	movups	%xmm0, 200(%rsp)
	je	.L2281
	movq	%rcx, 224(%rsp)
	movq	%rdx, 240(%rsp)
.L2280:
	movq	$0, 232(%rsp)
	movb	$0, (%rcx)
	movq	224(%rsp), %rcx
	cmpq	%rdi, %rcx
	je	.L2282
	movq	240(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L2282:
	movq	%r14, %rcx
	call	_ZNSt6localeD1Ev
	movzwl	(%rbx), %eax
	movq	200(%rsp), %r12
	movq	192(%rsp), %rdi
	andw	$384, %ax
	cmpw	$128, %ax
	je	.L2413
.L2283:
	cmpw	$256, %ax
	je	.L2285
	movq	496(%rsp), %rax
	movq	16(%rax), %r14
.L2289:
	leaq	96(%rsp), %rdx
	movq	%r14, %rcx
	movq	%r12, 96(%rsp)
	movq	%rdi, 104(%rsp)
.LEHB48:
	call	_ZNSt8__format7__writeINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EE
.L2398:
	movq	192(%rsp), %rcx
	movq	%rax, %rbx
	cmpq	%rsi, %rcx
	je	.L2293
	movq	208(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L2293:
	cmpb	$0, 152(%rsp)
	jne	.L2414
.L2294:
	movq	160(%rsp), %rcx
	cmpq	%rbp, %rcx
	je	.L2358
	movq	176(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	nop
.L2358:
	movaps	384(%rsp), %xmm6
	movq	%rbx, %rax
	addq	$408, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L2329:
	movzwl	(%rbx), %eax
	movq	%r13, %rdi
	andw	$384, %ax
	cmpw	$128, %ax
	jne	.L2283
.L2413:
	movzwl	4(%rbx), %eax
.L2284:
	movq	496(%rsp), %rdx
	cmpq	%rax, %r12
	movq	16(%rdx), %r14
	jnb	.L2289
	movzbl	(%rbx), %edx
	subq	%r12, %rax
	movzbl	8(%rbx), %ecx
	movq	%rax, %rbx
	movl	%edx, %r8d
	andl	$3, %r8d
	movsbl	%cl, %eax
	jne	.L2291
	andl	$64, %edx
	je	.L2331
	movss	.LC33(%rip), %xmm0
	andps	.LC32(%rip), %xmm6
	ucomiss	%xmm6, %xmm0
	jnb	.L2415
.L2331:
	movl	$32, %eax
	movl	$2, %r8d
.L2291:
	leaq	96(%rsp), %rdx
	movl	%eax, 32(%rsp)
	movq	%rbx, %r9
	movq	%r14, %rcx
	movq	%r12, 96(%rsp)
	movq	%rdi, 104(%rsp)
	call	_ZNSt8__format14__write_paddedINS_10_Sink_iterIcEEcEET_S3_St17basic_string_viewIT0_St11char_traitsIS5_EENS_6_AlignEyS5_
.LEHE48:
	jmp	.L2398
	.p2align 4,,10
	.p2align 3
.L2402:
	cmpb	$2, %dl
	je	.L2416
	movq	$-1, 56(%rsp)
	cmpb	$4, %dl
	je	.L2417
.L2166:
	shrb	$3, %al
	andl	$15, %eax
	cmpb	$7, %al
	ja	.L2169
	leaq	.L2171(%rip), %rdx
	movzbl	%al, %eax
	movslq	(%rdx,%rax,4), %rax
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L2171:
	.long	.L2178-.L2171
	.long	.L2310-.L2171
	.long	.L2176-.L2171
	.long	.L2175-.L2171
	.long	.L2392-.L2171
	.long	.L2394-.L2171
	.long	.L2172-.L2171
	.long	.L2393-.L2171
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2414:
	leaq	144(%rsp), %rcx
	call	_ZNSt6localeD1Ev
	jmp	.L2294
	.p2align 4,,10
	.p2align 3
.L2338:
	movl	$1, %r12d
.L2181:
	leaq	112(%rsp), %r13
	movl	$4, 32(%rsp)
	movaps	%xmm6, %xmm3
	movl	$112, %edi
	leaq	257(%rsp), %rdx
	movq	%r13, %rcx
	movl	$4, %r14d
	leaq	384(%rsp), %r8
	call	_ZSt8to_charsPcS_fSt12chars_format
	movq	112(%rsp), %rsi
	movq	120(%rsp), %rax
	jmp	.L2182
	.p2align 4,,10
	.p2align 3
.L2415:
	movzbl	0(%r13), %edx
	leaq	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE(%rip), %rcx
	movl	$48, %eax
	movl	$2, %r8d
	cmpb	$15, (%rcx,%rdx)
	jbe	.L2291
	movq	24(%r14), %rax
	movzbl	(%rdi), %edx
	leaq	1(%rax), %rcx
	movq	%rcx, 24(%r14)
	movb	%dl, (%rax)
	movq	24(%r14), %rax
	subq	8(%r14), %rax
	cmpq	16(%r14), %rax
	je	.L2418
.L2292:
	addq	$1, %rdi
	subq	$1, %r12
	movl	$48, %eax
	movl	$2, %r8d
	jmp	.L2291
	.p2align 4,,10
	.p2align 3
.L2319:
	xorl	%eax, %eax
.L2216:
	testb	%r15b, %r15b
	je	.L2419
	movb	%r15b, 88(%rsp)
	movq	%rax, 80(%rsp)
	movq	$1, 72(%rsp)
	jmp	.L2303
	.p2align 4,,10
	.p2align 3
.L2339:
	movq	$6, 56(%rsp)
.L2175:
	xorl	%r12d, %r12d
.L2174:
	movl	$1, %r14d
	movl	$101, %edi
	xorl	%r15d, %r15d
.L2177:
	movl	56(%rsp), %esi
	leaq	257(%rsp), %rax
	movl	%r14d, 32(%rsp)
	movaps	%xmm6, %xmm3
	leaq	112(%rsp), %r13
	movq	%rax, %rdx
	movq	%rax, 72(%rsp)
	leaq	384(%rsp), %r8
	movq	%r13, %rcx
	movl	%esi, 40(%rsp)
	call	_ZSt8to_charsPcS_fSt12chars_formati
	cmpl	$132, 120(%rsp)
	movq	112(%rsp), %rsi
	je	.L2179
	leaq	384(%rsp), %rax
	movq	72(%rsp), %r13
	movq	%rax, 64(%rsp)
	jmp	.L2180
	.p2align 4,,10
	.p2align 3
.L2340:
	movq	$6, 56(%rsp)
.L2392:
	movl	$1, %r12d
	jmp	.L2174
	.p2align 4,,10
	.p2align 3
.L2341:
	movq	$6, 56(%rsp)
.L2394:
	movl	$2, %r14d
	xorl	%edi, %edi
	xorl	%r15d, %r15d
	xorl	%r12d, %r12d
	jmp	.L2177
	.p2align 4,,10
	.p2align 3
.L2337:
	movq	$6, 56(%rsp)
.L2393:
	movl	$1, %r12d
.L2170:
	movl	$3, %r14d
	movl	$101, %edi
	movl	$1, %r15d
	jmp	.L2177
	.p2align 4,,10
	.p2align 3
.L2342:
	movq	$6, 56(%rsp)
.L2172:
	xorl	%r12d, %r12d
	jmp	.L2170
	.p2align 4,,10
	.p2align 3
.L2308:
	xorl	%r12d, %r12d
	jmp	.L2181
	.p2align 4,,10
	.p2align 3
.L2417:
	movq	496(%rsp), %rdi
	movb	$0, 208(%rsp)
	movzwl	6(%rcx), %eax
	movzbl	(%rdi), %edx
	movl	%edx, %ecx
	andl	$15, %edx
	andl	$15, %ecx
	cmpq	%rdx, %rax
	jb	.L2420
	testb	%cl, %cl
	jne	.L2168
	movq	496(%rsp), %rdi
	movq	(%rdi), %rdi
	movq	%rdi, %rdx
	movq	%rdi, 56(%rsp)
	shrq	$4, %rdx
	cmpq	%rdx, %rax
	jnb	.L2168
	movq	496(%rsp), %rdi
	salq	$5, %rax
	addq	8(%rdi), %rax
	movq	(%rax), %rdx
	movq	%rdx, 192(%rsp)
	movq	8(%rax), %rdx
	movq	%rdx, 200(%rsp)
	movzbl	16(%rax), %eax
	movb	%al, 208(%rsp)
	.p2align 4,,10
	.p2align 3
.L2168:
	leaq	192(%rsp), %rcx
	leaq	160(%rsp), %rsi
.LEHB49:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE49:
	movq	%rax, 56(%rsp)
	movzbl	1(%rbx), %eax
	jmp	.L2166
	.p2align 4,,10
	.p2align 3
.L2403:
	movb	$43, -1(%r13)
	subq	$1, %r13
	movzbl	(%rbx), %r9d
	jmp	.L2213
	.p2align 4,,10
	.p2align 3
.L2410:
	movq	%r15, %rcx
	call	_ZNSt6localeC1Ev
	movq	496(%rsp), %rax
	movb	$1, 32(%rax)
	jmp	.L2273
	.p2align 4,,10
	.p2align 3
.L2285:
	movq	496(%rsp), %rdx
	movb	$0, 240(%rsp)
	movzwl	4(%rbx), %eax
	movzbl	(%rdx), %edx
	movl	%edx, %ecx
	andl	$15, %edx
	andl	$15, %ecx
	cmpq	%rdx, %rax
	jb	.L2421
	testb	%cl, %cl
	jne	.L2288
	movq	496(%rsp), %rdx
	movq	(%rdx), %rdx
	movq	%rdx, 56(%rsp)
	shrq	$4, %rdx
	cmpq	%rdx, %rax
	jnb	.L2288
	movq	496(%rsp), %rdx
	salq	$5, %rax
	addq	8(%rdx), %rax
	movq	(%rax), %rdx
	movq	%rdx, 224(%rsp)
	movq	8(%rax), %rdx
	movq	%rdx, 232(%rsp)
	movzbl	16(%rax), %eax
	movb	%al, 240(%rsp)
	.p2align 4,,10
	.p2align 3
.L2288:
	leaq	224(%rsp), %rcx
.LEHB50:
	call	_ZNSt8__format14__int_from_argISt20basic_format_contextINS_10_Sink_iterIcEEcEEEyRKSt16basic_format_argIT_E
.LEHE50:
	jmp	.L2284
	.p2align 4,,10
	.p2align 3
.L2412:
	movq	%rax, 192(%rsp)
	movups	%xmm0, 200(%rsp)
.L2281:
	movq	%rdi, 224(%rsp)
	leaq	240(%rsp), %rdi
	movq	%rdi, %rcx
	jmp	.L2280
	.p2align 4,,10
	.p2align 3
.L2416:
	movzwl	6(%rcx), %edi
	movq	%rdi, 56(%rsp)
	jmp	.L2166
	.p2align 4,,10
	.p2align 3
.L2411:
	testq	%r8, %r8
	je	.L2276
	cmpq	$1, %r8
	je	.L2422
	movq	%rdi, %rdx
	call	memcpy
	movq	232(%rsp), %r8
	movq	192(%rsp), %rcx
.L2276:
	movq	%r8, 200(%rsp)
	movb	$0, (%rcx,%r8)
	movq	224(%rsp), %rcx
	jmp	.L2280
	.p2align 4,,10
	.p2align 3
.L2219:
	movq	80(%rsp), %rax
	subq	$1, %rax
.L2303:
	movzbl	0(%r13), %edx
	leaq	_ZNSt8__detail31__from_chars_alnum_to_val_tableILb0EE5valueE(%rip), %rcx
	movq	56(%rsp), %r15
	cmpb	$16, (%rcx,%rdx)
	adcq	$-1, %rax
	subq	%rax, %r15
	addq	%r15, 72(%rsp)
	jmp	.L2220
	.p2align 4,,10
	.p2align 3
.L2336:
	movb	$0, 72(%rsp)
	movq	$134, 64(%rsp)
.L2184:
	movq	160(%rsp), %r9
	cmpq	%rbp, %r9
	je	.L2316
	movq	176(%rsp), %rax
.L2186:
	movq	64(%rsp), %rsi
	cmpq	%rsi, %rax
	jb	.L2423
.L2209:
	cmpq	%rbp, %r9
	je	.L2317
	movq	176(%rsp), %rax
	leaq	(%rax,%rax), %rsi
	cmpq	%rsi, %rax
	movq	%rsi, 64(%rsp)
	jb	.L2424
.L2198:
	movq	64(%rsp), %rax
	leaq	1(%r9), %rdx
	movq	%r9, 64(%rsp)
	cmpb	$0, 72(%rsp)
	leaq	-1(%r9,%rax), %r8
	jne	.L2425
	testl	%r14d, %r14d
	jne	.L2426
	movaps	%xmm6, %xmm3
	movq	%r13, %rcx
	call	_ZSt8to_charsPcS_f
	movq	112(%rsp), %rsi
	movq	120(%rsp), %rax
	movq	64(%rsp), %r9
.L2206:
	testl	%eax, %eax
	jne	.L2208
	movq	160(%rsp), %rdx
	movq	%rsi, %rax
	subq	%r9, %rax
	movq	%rax, 168(%rsp)
	movb	$0, (%rdx,%rax)
	movq	160(%rsp), %rax
	leaq	1(%rax), %r13
	addq	168(%rsp), %rax
	movq	%rax, 64(%rsp)
	jmp	.L2180
	.p2align 4,,10
	.p2align 3
.L2217:
	movsbl	%dil, %edx
	movq	%r12, %r8
	movq	%r13, %rcx
	movb	%r9b, 72(%rsp)
	call	memchr
	movzbl	72(%rsp), %r9d
	testq	%rax, %rax
	je	.L2323
	subq	%r13, %rax
	cmpq	$-1, %rax
	cmove	%r12, %rax
	jmp	.L2216
.L2310:
	movl	$4, %r14d
	movl	$112, %edi
	xorl	%r15d, %r15d
	xorl	%r12d, %r12d
	jmp	.L2177
.L2176:
	movl	$4, %r14d
	movl	$112, %edi
	xorl	%r15d, %r15d
	movl	$1, %r12d
	jmp	.L2177
.L2178:
	movl	$3, %r14d
	xorl	%edi, %edi
	xorl	%r15d, %r15d
	xorl	%r12d, %r12d
	jmp	.L2177
.L2419:
	movq	%rax, 80(%rsp)
	xorl	%r15d, %r15d
	movq	$1, 72(%rsp)
	movb	$1, 88(%rsp)
	jmp	.L2304
.L2426:
	movl	%r14d, 32(%rsp)
	movaps	%xmm6, %xmm3
	movq	%r13, %rcx
	call	_ZSt8to_charsPcS_fSt12chars_format
	movq	112(%rsp), %rsi
	movq	120(%rsp), %rax
	movq	64(%rsp), %r9
	jmp	.L2206
.L2420:
	movq	(%rdi), %rdi
	leaq	(%rax,%rax,4), %rcx
	salq	$4, %rax
	movq	%rdi, %rdx
	movq	%rdi, 56(%rsp)
	movq	496(%rsp), %rdi
	shrq	$4, %rdx
	shrq	%cl, %rdx
	andl	$31, %edx
	addq	8(%rdi), %rax
	movb	%dl, 208(%rsp)
	movq	(%rax), %rdx
	movq	%rdx, 192(%rsp)
	movq	8(%rax), %rax
	movq	%rax, 200(%rsp)
	jmp	.L2168
.L2323:
	movq	%r12, %rax
	jmp	.L2216
.L2405:
	movq	56(%rsp), %rax
	cmpq	$15, %rax
	ja	.L2401
	movq	80(%rsp), %rax
	cmpq	%rax, %r12
	cmova	%rax, %r12
	testq	%r12, %r12
	js	.L2238
	movq	%rbp, %r10
.L2305:
	cmpq	$15, %r12
	ja	.L2427
.L2244:
	cmpq	%r10, %r13
	jb	.L2248
	cmpq	%r13, %r10
	jb	.L2248
	xorl	%eax, %eax
	movq	%r12, 32(%rsp)
	movq	%r13, %r9
	xorl	%r8d, %r8d
	leaq	160(%rsp), %rsi
	movq	%rax, 40(%rsp)
	movq	%r10, %rdx
	movq	%rsi, %rcx
.LEHB51:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	movq	160(%rsp), %r10
	jmp	.L2250
	.p2align 4,,10
	.p2align 3
.L2208:
	movq	160(%rsp), %rdx
	cmpl	$132, %eax
	movq	$0, 168(%rsp)
	movb	$0, (%rdx)
	movq	160(%rsp), %r9
	movq	168(%rsp), %rdx
	je	.L2209
	leaq	(%r9,%rdx), %rax
	leaq	1(%r9), %r13
	movq	%rax, 64(%rsp)
	jmp	.L2180
	.p2align 4,,10
	.p2align 3
.L2423:
	testq	%rsi, %rsi
	js	.L2428
	addq	%rax, %rax
	cmpq	%rax, 64(%rsp)
	jnb	.L2189
	testq	%rax, %rax
	js	.L2190
	leaq	1(%rax), %rcx
	movq	%rax, 64(%rsp)
.L2191:
	leaq	160(%rsp), %rsi
	call	_Znwy
	movq	%rax, %r9
	movq	168(%rsp), %rax
	movq	160(%rsp), %rsi
	leaq	1(%rax), %r8
	testq	%rax, %rax
	je	.L2429
	testq	%r8, %r8
	je	.L2395
	movq	%r9, %rcx
	movq	%rsi, %rdx
	call	memcpy
	movq	%rax, %r9
.L2395:
	cmpq	%rbp, %rsi
	je	.L2194
	movq	176(%rsp), %rax
	movq	%rsi, %rcx
	movq	%r9, 80(%rsp)
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	80(%rsp), %r9
.L2194:
	movq	64(%rsp), %rax
	movq	%r9, 160(%rsp)
	movq	%rax, 176(%rsp)
	jmp	.L2209
.L2421:
	movq	496(%rsp), %rdx
	leaq	(%rax,%rax,4), %rcx
	salq	$4, %rax
	movq	(%rdx), %rdx
	movq	%rdx, 56(%rsp)
	shrq	$4, %rdx
	shrq	%cl, %rdx
	andl	$31, %edx
	movb	%dl, 240(%rsp)
	movq	496(%rsp), %rdx
	addq	8(%rdx), %rax
	movq	(%rax), %rdx
	movq	%rdx, 224(%rsp)
	movq	8(%rax), %rax
	movq	%rax, 232(%rsp)
	jmp	.L2288
.L2222:
	cmpq	%rbp, 160(%rsp)
	je	.L2228
	movq	176(%rsp), %rax
	movq	56(%rsp), %rsi
	cmpq	%rsi, %rax
	jb	.L2230
.L2229:
	movq	80(%rsp), %rax
	cmpq	%rax, %r9
	jb	.L2430
.L2241:
	movabsq	$9223372036854775807, %rax
	movq	72(%rsp), %rsi
	subq	%r9, %rax
	cmpq	%rsi, %rax
	jb	.L2431
	movq	72(%rsp), %rax
	leaq	(%r9,%rax), %r12
	movq	160(%rsp), %rax
	cmpq	%rbp, %rax
	je	.L2328
	movq	176(%rsp), %rdx
.L2265:
	cmpq	%r12, %rdx
	jb	.L2266
	movq	80(%rsp), %rsi
	leaq	(%rax,%rsi), %rcx
	subq	%rsi, %r9
	je	.L2267
	movq	72(%rsp), %rax
	addq	%rcx, %rax
	cmpq	$1, %r9
	je	.L2432
	movq	%rcx, %rdx
	movq	%r9, %r8
	movq	%rax, %rcx
	call	memmove
	movq	80(%rsp), %rcx
	addq	160(%rsp), %rcx
.L2267:
	cmpq	$1, 72(%rsp)
	je	.L2433
	movq	72(%rsp), %r8
	movl	$48, %edx
	call	memset
.L2270:
	movq	160(%rsp), %rax
	movq	%r12, 168(%rsp)
	cmpb	$0, 88(%rsp)
	movb	$0, (%rax,%r12)
	movq	168(%rsp), %r12
	je	.L2258
	movq	160(%rsp), %rax
	movq	80(%rsp), %rsi
	movb	$46, (%rax,%rsi)
	movq	168(%rsp), %r12
	jmp	.L2258
.L2233:
	movq	56(%rsp), %rcx
	addq	$1, %rcx
	js	.L2234
.L2235:
	leaq	160(%rsp), %rsi
	call	_Znwy
	movq	168(%rsp), %r9
	movq	%rax, %rsi
	movq	160(%rsp), %r14
	leaq	1(%r9), %r8
	testq	%r9, %r9
	je	.L2434
	testq	%r8, %r8
	jne	.L2240
	cmpq	%rbp, %r14
	je	.L2435
.L2237:
	movq	176(%rsp), %rax
	movq	%r14, %rcx
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	168(%rsp), %r9
	movq	%rsi, 160(%rsp)
	movq	56(%rsp), %rax
	testq	%r9, %r9
	movq	%rax, 176(%rsp)
	jne	.L2229
.L2231:
	movq	80(%rsp), %rax
	cmpq	%rax, %r12
	cmova	%rax, %r12
	testq	%r12, %r12
	js	.L2238
	movq	160(%rsp), %r10
	cmpq	%rbp, %r10
	je	.L2305
.L2243:
	movq	176(%rsp), %rax
	cmpq	%r12, %rax
	jnb	.L2244
	addq	%rax, %rax
	cmpq	%rax, %r12
	jnb	.L2245
	leaq	1(%rax), %rcx
	testq	%rax, %rax
	movq	%r12, %r14
	movq	%rax, %r12
	jns	.L2253
.L2252:
	leaq	160(%rsp), %rsi
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L2189:
	movq	64(%rsp), %rcx
	addq	$1, %rcx
	jns	.L2191
.L2190:
	leaq	160(%rsp), %rsi
	call	_ZSt17__throw_bad_allocv
.L2425:
	movl	56(%rsp), %eax
	movl	%r14d, 32(%rsp)
	movaps	%xmm6, %xmm3
	movq	%r13, %rcx
	movl	%eax, 40(%rsp)
	call	_ZSt8to_charsPcS_fSt12chars_formati
	movq	112(%rsp), %rsi
	movq	120(%rsp), %rax
	movq	64(%rsp), %r9
	jmp	.L2206
.L2179:
	movq	56(%rsp), %rax
	cmpl	$2, %r14d
	movb	$1, 72(%rsp)
	leaq	128(%rax), %rsi
	movq	%rsi, 64(%rsp)
	jne	.L2184
	cvttss2sil	%xmm6, %eax
	pxor	%xmm0, %xmm0
	cltd
	xorl	%edx, %eax
	subl	%edx, %eax
	cvtsi2sdl	%eax, %xmm0
	call	log10
	cvttsd2sil	%xmm0, %edx
	movl	%edx, %eax
	sarl	%eax
	cmpl	$1, %edx
	movl	$1, %edx
	cltq
	cmovle	%rdx, %rax
	addq	%rax, %rsi
	movq	%rsi, 64(%rsp)
	jmp	.L2184
.L2248:
	testq	%r12, %r12
	je	.L2250
	cmpq	$1, %r12
	je	.L2436
	movq	%r10, %rcx
	movq	%r12, %r8
	movq	%r13, %rdx
	call	memcpy
	movq	160(%rsp), %r10
	jmp	.L2250
.L2404:
	movq	80(%rsp), %rax
	movq	%rdx, %rcx
	movq	%r12, %r8
	leaq	0(%r13,%rax), %rsi
	addq	%rax, %rcx
	subq	%rax, %r8
	addq	%r13, %rcx
	movq	%rsi, %rdx
	call	memmove
	cmpb	$0, 88(%rsp)
	je	.L2225
	movq	80(%rsp), %rax
	movb	$46, (%rsi)
	leaq	1(%r13,%rax), %rsi
.L2225:
	movq	%r15, %r8
	movl	$48, %edx
	movq	%rsi, %rcx
	call	memset
	movzbl	(%rbx), %r9d
	movq	56(%rsp), %r12
	jmp	.L2215
.L2317:
	movq	$30, 64(%rsp)
	movl	$31, %ecx
.L2197:
	leaq	160(%rsp), %rsi
	call	_Znwy
	movq	168(%rsp), %r8
	movq	%rax, %r9
	movq	160(%rsp), %rsi
	cmpq	$1, %r8
	je	.L2437
	testq	%r8, %r8
	je	.L2397
	movq	%rsi, %rdx
	movq	%rax, %rcx
	call	memcpy
	movq	%rax, %r9
.L2397:
	cmpq	%rbp, %rsi
	je	.L2202
	movq	176(%rsp), %rax
	movq	%rsi, %rcx
	movq	%r9, 80(%rsp)
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	80(%rsp), %r9
.L2202:
	movq	64(%rsp), %rax
	movq	%r9, 160(%rsp)
	movq	%rax, 176(%rsp)
	jmp	.L2198
.L2316:
	movl	$15, %eax
	jmp	.L2186
.L2424:
	testq	%rsi, %rsi
	js	.L2199
	leaq	1(%rsi), %rcx
	jmp	.L2197
.L2266:
	movq	72(%rsp), %rax
	leaq	160(%rsp), %rsi
	xorl	%r9d, %r9d
	xorl	%r8d, %r8d
	movq	80(%rsp), %r15
	movq	%rsi, %rcx
	movq	%rax, 32(%rsp)
	movq	%r15, %rdx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	movq	160(%rsp), %rcx
	addq	%r15, %rcx
	jmp	.L2267
.L2429:
	movzbl	(%rsi), %eax
	movb	%al, (%r9)
	jmp	.L2395
.L2434:
	movzbl	(%r14), %eax
	cmpq	%rbp, %r14
	movb	%al, (%rsi)
	jne	.L2237
	movq	56(%rsp), %rax
	movq	%rsi, 160(%rsp)
	movq	%rax, 176(%rsp)
	movq	80(%rsp), %rax
	cmpq	%rax, %r12
	cmova	%rax, %r12
	testq	%r12, %r12
	js	.L2238
	movq	%rsi, %r10
	jmp	.L2243
.L2409:
	movabsq	$9223372036854775807, %rax
	subq	%r12, %rax
	cmpq	%r15, %rax
	jb	.L2438
	movq	160(%rsp), %rax
	leaq	(%r12,%r15), %r13
	cmpq	%rbp, %rax
	je	.L2327
	movq	176(%rsp), %rdx
.L2260:
	cmpq	%r13, %rdx
	jb	.L2439
.L2261:
	leaq	(%rax,%r12), %rcx
	cmpq	$1, %r15
	je	.L2440
	movq	%r15, %r8
	movl	$48, %edx
	call	memset
.L2263:
	movq	160(%rsp), %rax
	movq	%r13, 168(%rsp)
	movb	$0, (%rax,%r13)
	movq	168(%rsp), %r12
	jmp	.L2258
.L2240:
	movq	%r14, %rdx
	movq	%rax, %rcx
	movq	%r9, 64(%rsp)
	call	memcpy
	cmpq	%rbp, %r14
	movq	64(%rsp), %r9
	jne	.L2237
	movq	56(%rsp), %rax
	movq	%rsi, 160(%rsp)
	movq	%rax, 176(%rsp)
	jmp	.L2229
.L2422:
	movzbl	240(%rsp), %eax
	movb	%al, (%rcx)
	movq	232(%rsp), %r8
	movq	192(%rsp), %rcx
	jmp	.L2276
.L2437:
	movzbl	(%rsi), %eax
	movb	%al, (%r9)
	jmp	.L2397
.L2408:
	leaq	160(%rsp), %rsi
	movl	$46, %edx
	movq	%rsi, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9push_backEc
	jmp	.L2256
.L2228:
	movq	56(%rsp), %rax
	cmpq	$15, %rax
	jbe	.L2229
.L2401:
	testq	%rax, %rax
	js	.L2300
	cmpq	$29, %rax
	ja	.L2233
	movq	$30, 56(%rsp)
.L2301:
	movq	56(%rsp), %rax
	leaq	1(%rax), %rcx
	jmp	.L2235
.L2328:
	movl	$15, %edx
	jmp	.L2265
.L2433:
	movb	$48, (%rcx)
	jmp	.L2270
.L2432:
	movzbl	(%rcx), %edx
	movb	%dl, (%rax)
	movq	160(%rsp), %rcx
	addq	%rsi, %rcx
	jmp	.L2267
.L2436:
	movzbl	0(%r13), %eax
	movb	%al, (%r10)
	movq	160(%rsp), %r10
	jmp	.L2250
.L2439:
	movq	%r15, 32(%rsp)
	xorl	%r9d, %r9d
	xorl	%r8d, %r8d
	movq	%r12, %rdx
	leaq	160(%rsp), %rsi
	movq	%rsi, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
.LEHE51:
	movq	160(%rsp), %rax
	jmp	.L2261
.L2418:
	movq	(%r14), %rax
	movq	%r14, %rcx
.LEHB52:
	call	*(%rax)
.LEHE52:
	jmp	.L2292
.L2427:
	cmpq	$29, %r12
	ja	.L2245
	leaq	160(%rsp), %rsi
	movl	$31, %ecx
.LEHB53:
	call	_Znwy
	movq	%r12, %r14
	movq	%rax, %r10
	movl	$30, %r12d
	jmp	.L2246
.L2440:
	movb	$48, (%rcx)
	jmp	.L2263
.L2327:
	movl	$15, %edx
	jmp	.L2260
.L2435:
	movq	%rax, 160(%rsp)
	movq	56(%rsp), %rax
	movq	$-1, %r9
	movq	%rax, 176(%rsp)
	jmp	.L2241
.L2407:
	movzbl	0(%r13), %eax
	movq	%r12, %rsi
	movl	$1, %r12d
	movb	%al, (%r10)
	jmp	.L2254
.L2406:
	movq	%rax, 56(%rsp)
	jmp	.L2301
.L2428:
	leaq	.LC7(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L2199:
	leaq	.LC7(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L2300:
	leaq	.LC7(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L2431:
	leaq	.LC26(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L2430:
	leaq	.LC27(%rip), %rdx
	movq	%rax, %r8
	leaq	.LC28(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt24__throw_out_of_range_fmtPKcz
.L2238:
	leaq	.LC25(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.L2438:
	leaq	.LC26(%rip), %rcx
	leaq	160(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
.LEHE53:
.L2169:
	xorl	%r14d, %r14d
	xorl	%edi, %edi
	xorl	%r15d, %r15d
	xorl	%r12d, %r12d
	jmp	.L2177
.L2343:
	movq	%rax, %rbx
.L2299:
	movq	%rsi, %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	%rbx, %rcx
.LEHB54:
	call	_Unwind_Resume
.LEHE54:
.L2345:
	movq	%rax, %rbx
	jmp	.L2297
.L2344:
	movq	%r14, %rcx
	movq	%rax, %rbx
	call	_ZNSt6localeD1Ev
.L2297:
	leaq	192(%rsp), %rcx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	cmpb	$0, 152(%rsp)
	je	.L2298
	leaq	144(%rsp), %rcx
	call	_ZNSt6localeD1Ev
.L2298:
	leaq	160(%rsp), %rsi
	jmp	.L2299
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5104:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5104-.LLSDACSB5104
.LLSDACSB5104:
	.uleb128 .LEHB46-.LFB5104
	.uleb128 .LEHE46-.LEHB46
	.uleb128 .L2343-.LFB5104
	.uleb128 0
	.uleb128 .LEHB47-.LFB5104
	.uleb128 .LEHE47-.LEHB47
	.uleb128 .L2344-.LFB5104
	.uleb128 0
	.uleb128 .LEHB48-.LFB5104
	.uleb128 .LEHE48-.LEHB48
	.uleb128 .L2345-.LFB5104
	.uleb128 0
	.uleb128 .LEHB49-.LFB5104
	.uleb128 .LEHE49-.LEHB49
	.uleb128 .L2343-.LFB5104
	.uleb128 0
	.uleb128 .LEHB50-.LFB5104
	.uleb128 .LEHE50-.LEHB50
	.uleb128 .L2345-.LFB5104
	.uleb128 0
	.uleb128 .LEHB51-.LFB5104
	.uleb128 .LEHE51-.LEHB51
	.uleb128 .L2343-.LFB5104
	.uleb128 0
	.uleb128 .LEHB52-.LFB5104
	.uleb128 .LEHE52-.LEHB52
	.uleb128 .L2345-.LFB5104
	.uleb128 0
	.uleb128 .LEHB53-.LFB5104
	.uleb128 .LEHE53-.LEHB53
	.uleb128 .L2343-.LFB5104
	.uleb128 0
	.uleb128 .LEHB54-.LFB5104
	.uleb128 .LEHE54-.LEHB54
	.uleb128 0
	.uleb128 0
.LLSDACSE5104:
	.section	.text$_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC34:
	.ascii "format error: format-spec contains invalid formatting options for 'bool'\0"
	.align 8
.LC35:
	.ascii "format error: format-spec contains invalid formatting options for 'charT'\0"
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
	.def	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE:
.LFB4877:
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$168, %rsp
	.seh_stackalloc	168
	.seh_endprologue
	movq	%rdx, %rbx
	movzbl	%r8b, %r8d
	movq	%rcx, %rsi
	leaq	.L2444(%rip), %rdx
	movslq	(%rdx,%r8,4), %rax
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L2444:
	.long	.L2459-.L2444
	.long	.L2458-.L2444
	.long	.L2457-.L2444
	.long	.L2456-.L2444
	.long	.L2455-.L2444
	.long	.L2454-.L2444
	.long	.L2453-.L2444
	.long	.L2452-.L2444
	.long	.L2451-.L2444
	.long	.L2450-.L2444
	.long	.L2449-.L2444
	.long	.L2448-.L2444
	.long	.L2447-.L2444
	.long	.L2446-.L2444
	.long	.L2445-.L2444
	.long	.L2443-.L2444
	.section	.text$_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L2445:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$1, %r8d
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	movdqa	(%rsi), %xmm2
	leaq	48(%rsp), %rdx
	movq	%rdi, %rcx
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	movaps	%xmm2, 48(%rsp)
	movq	%rbx, %r8
	call	_ZNKSt8__format15__formatter_intIcE6formatInNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	movq	%rax, 16(%rbx)
.L2441:
	addq	$168, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.p2align 4,,10
	.p2align 3
.L2443:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$1, %r8d
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	movdqa	(%rsi), %xmm3
	leaq	48(%rsp), %rdx
	movq	%rdi, %rcx
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	movaps	%xmm3, 48(%rsp)
	movq	%rbx, %r8
	call	_ZNKSt8__format15__formatter_intIcE6formatIoNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
.L2479:
	movq	%rax, 16(%rbx)
	addq	$168, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.p2align 4,,10
	.p2align 3
.L2458:
	movq	(%rbx), %rbp
	xorl	%r8d, %r8d
	movl	$0, 136(%rsp)
	leaq	128(%rsp), %rdi
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	movq	%rdi, %rcx
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	testb	$120, 129(%rsp)
	jne	.L2460
	testb	$92, 128(%rsp)
	jne	.L2481
.L2460:
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	%rdi, %rcx
	movzbl	(%rsi), %edx
	movq	48(%rax), %rbx
	movq	%rbx, %r8
	call	_ZNKSt8__format15__formatter_intIcE6formatINS_10_Sink_iterIcEEEENSt20basic_format_contextIT_cE8iteratorEbRS7_
	movq	%rax, 16(%rbx)
	jmp	.L2441
	.p2align 4,,10
	.p2align 3
.L2457:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$7, %r8d
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	movzbl	129(%rsp), %edx
	movl	%edx, %ecx
	notl	%edx
	andl	$120, %ecx
	andl	$56, %edx
	jne	.L2462
	testb	$92, 128(%rsp)
	jne	.L2482
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	cmpb	$120, %cl
	movq	48(%rax), %rbx
	jne	.L2483
	movq	16(%rbx), %rax
	jmp	.L2479
	.p2align 4,,10
	.p2align 3
.L2455:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$1, %r8d
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	movl	(%rsi), %edx
	movq	%rdi, %rcx
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	movq	%rbx, %r8
	call	_ZNKSt8__format15__formatter_intIcE6formatIjNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	movq	%rax, 16(%rbx)
	jmp	.L2441
	.p2align 4,,10
	.p2align 3
.L2454:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$1, %r8d
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	movq	(%rsi), %rdx
	movq	%rdi, %rcx
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	movq	%rbx, %r8
	call	_ZNKSt8__format15__formatter_intIcE6formatIxNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	movq	%rax, 16(%rbx)
	jmp	.L2441
	.p2align 4,,10
	.p2align 3
.L2456:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$1, %r8d
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	movl	(%rsi), %edx
	movq	%rdi, %rcx
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	movq	%rbx, %r8
	call	_ZNKSt8__format15__formatter_intIcE6formatIiNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	movq	%rax, 16(%rbx)
	jmp	.L2441
	.p2align 4,,10
	.p2align 3
.L2453:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$1, %r8d
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format15__formatter_intIcE11_M_do_parseERSt26basic_format_parse_contextIcENS_10_Pres_typeE
	movq	(%rsi), %rdx
	movq	%rdi, %rcx
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	movq	%rbx, %r8
	call	_ZNKSt8__format15__formatter_intIcE6formatIyNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	movq	%rax, 16(%rbx)
	jmp	.L2441
	.p2align 4,,10
	.p2align 3
.L2452:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	movss	(%rsi), %xmm1
	movq	%rdi, %rcx
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	movq	%rbx, %r8
	call	_ZNKSt8__format14__formatter_fpIcE6formatIfNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	movq	%rax, 16(%rbx)
	jmp	.L2441
	.p2align 4,,10
	.p2align 3
.L2451:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	movsd	(%rsi), %xmm1
	movq	%rdi, %rcx
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	movq	%rbx, %r8
	call	_ZNKSt8__format14__formatter_fpIcE6formatIdNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	movq	%rax, 16(%rbx)
	jmp	.L2441
	.p2align 4,,10
	.p2align 3
.L2450:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format14__formatter_fpIcE5parseERSt26basic_format_parse_contextIcE
	leaq	64(%rsp), %rdx
	movq	%rdi, %rcx
	fldt	(%rsi)
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	fstpt	64(%rsp)
	movq	%rbx, %r8
	call	_ZNKSt8__format14__formatter_fpIcE6formatIeNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	movq	%rax, 16(%rbx)
	jmp	.L2441
	.p2align 4,,10
	.p2align 3
.L2449:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE
	movq	%rax, 8(%rbp)
	movq	(%rsi), %rsi
	movq	(%rbx), %rax
	movq	%rsi, %rcx
	movq	48(%rax), %rbx
	call	strlen
	movq	%rsi, 88(%rsp)
	movq	%rax, 80(%rsp)
.L2480:
	leaq	80(%rsp), %rdx
	movq	%rbx, %r8
	movq	%rdi, %rcx
	call	_ZNKSt8__format15__formatter_strIcE6formatINS_10_Sink_iterIcEEEET_St17basic_string_viewIcSt11char_traitsIcEERSt20basic_format_contextIS5_cE
	movq	%rax, 16(%rbx)
	addq	$168, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.p2align 4,,10
	.p2align 3
.L2448:
	movq	(%rbx), %rbp
	leaq	128(%rsp), %rdi
	movl	$0, 136(%rsp)
	movq	%rdi, %rcx
	movb	$32, 136(%rsp)
	movq	$0, 128(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt8__format15__formatter_strIcE5parseERSt26basic_format_parse_contextIcE
	movdqu	(%rsi), %xmm0
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	movaps	%xmm0, 80(%rsp)
	jmp	.L2480
	.p2align 4,,10
	.p2align 3
.L2447:
	movq	(%rbx), %rbp
	leaq	100(%rsp), %rdi
	movl	$0, 108(%rsp)
	movq	%rdi, %rcx
	movb	$32, 108(%rsp)
	movq	$0, 100(%rsp)
	leaq	8(%rbp), %rdx
	call	_ZNSt9formatterIPKvcE5parseERSt26basic_format_parse_contextIcE
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	movq	48(%rax), %rbx
	movq	(%rsi), %rax
	testq	%rax, %rax
	jne	.L2468
	movb	$48, 130(%rsp)
	movl	$3, %edx
.L2469:
	movl	$30768, %eax
	movq	%rdi, %r9
	movq	%rbx, %r8
	movq	%rdx, 80(%rsp)
	movw	%ax, 128(%rsp)
	leaq	80(%rsp), %rcx
	leaq	128(%rsp), %rax
	movl	$2, 32(%rsp)
	movq	%rax, 88(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	movq	%rax, 16(%rbx)
	jmp	.L2441
	.p2align 4,,10
	.p2align 3
.L2446:
	movq	(%rbx), %rcx
	movq	8(%rsi), %rax
	movq	(%rsi), %r8
	movq	48(%rcx), %rdx
	addq	$8, %rcx
	addq	$168, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	rex.W jmp	*%rax
	.p2align 4,,10
	.p2align 3
.L2468:
	movabsq	$3978425819141910832, %rsi
	bsrq	%rax, %rdx
	leal	4(%rdx), %r8d
	movq	%rsi, 112(%rsp)
	movabsq	$7378413942531504440, %rsi
	shrl	$2, %r8d
	cmpq	$255, %rax
	movq	%rsi, 120(%rsp)
	leal	-1(%r8), %edx
	jbe	.L2470
	.p2align 4,,10
	.p2align 3
.L2471:
	movq	%rax, %r10
	movl	%edx, %ecx
	andl	$15, %r10d
	movzbl	112(%rsp,%r10), %r10d
	movb	%r10b, 130(%rsp,%rcx)
	leal	-1(%rdx), %r10d
	movq	%rax, %rcx
	shrq	$8, %rax
	shrq	$4, %rcx
	subl	$2, %edx
	andl	$15, %ecx
	cmpq	$255, %rax
	movzbl	112(%rsp,%rcx), %ecx
	movb	%cl, 130(%rsp,%r10)
	ja	.L2471
.L2470:
	cmpq	$15, %rax
	jbe	.L2472
	movq	%rax, %rdx
	shrq	$4, %rax
	andl	$15, %edx
	movzbl	112(%rsp,%rdx), %edx
	movb	%dl, 131(%rsp)
	movzbl	112(%rsp,%rax), %eax
.L2473:
	movb	%al, 130(%rsp)
	leal	2(%r8), %edx
	jmp	.L2469
	.p2align 4,,10
	.p2align 3
.L2462:
	movq	%rax, 8(%rbp)
	movq	(%rbx), %rax
	testb	%cl, %cl
	movsbl	(%rsi), %edx
	movq	48(%rax), %rbx
	jne	.L2466
	movb	%dl, 112(%rsp)
	leaq	112(%rsp), %rax
	movq	%rdi, %r9
	movq	%rbx, %r8
	leaq	80(%rsp), %rcx
	movl	$1, %edx
	movl	$1, 32(%rsp)
	movq	$1, 80(%rsp)
	movq	%rax, 88(%rsp)
	call	_ZNSt8__format22__write_padded_as_specIcNS_10_Sink_iterIcEEEET0_St17basic_string_viewINSt13type_identityIT_E4typeESt11char_traitsIS8_EEyRSt20basic_format_contextIS3_S6_ERKNS_5_SpecIS6_EENS_6_AlignE
	jmp	.L2479
.L2483:
	movsbl	(%rsi), %edx
.L2466:
	movq	%rbx, %r8
	movq	%rdi, %rcx
	call	_ZNKSt8__format15__formatter_intIcE6formatIcNS_10_Sink_iterIcEEEENSt20basic_format_contextIT0_cE8iteratorET_RS7_
	jmp	.L2479
	.p2align 4,,10
	.p2align 3
.L2472:
	movzbl	112(%rsp,%rax), %eax
	jmp	.L2473
.L2482:
	leaq	.LC35(%rip), %rcx
	call	_ZSt20__throw_format_errorPKc
.L2459:
	call	_ZNSt8__format33__invalid_arg_id_in_format_stringEv
.L2481:
	leaq	.LC34(%rip), %rcx
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
.LFB4874:
	subq	$120, %rsp
	.seh_stackalloc	120
	.seh_endprologue
	movq	48(%rcx), %r9
	movq	%rcx, %rax
	movzbl	(%r9), %ecx
	movl	%ecx, %r8d
	andl	$15, %ecx
	andl	$15, %r8d
	cmpq	%rcx, %rdx
	jb	.L2488
	testb	%r8b, %r8b
	je	.L2489
	xorl	%r8d, %r8d
.L2486:
	movq	%rax, 40(%rsp)
	movq	48(%rsp), %rax
	leaq	40(%rsp), %rdx
	movb	%r8b, 64(%rsp)
	leaq	80(%rsp), %rcx
	movzbl	%r8b, %r8d
	movq	%rax, 80(%rsp)
	movq	56(%rsp), %rax
	movq	%rax, 88(%rsp)
	movq	64(%rsp), %rax
	movq	%rax, 96(%rsp)
	movq	72(%rsp), %rax
	movq	%rax, 104(%rsp)
	call	_ZNSt16basic_format_argISt20basic_format_contextINSt8__format10_Sink_iterIcEEcEE8_M_visitIZNS1_19_Formatting_scannerIS3_cE13_M_format_argEyEUlRT_E_EEDcOS9_NS1_6_Arg_tE
	nop
	addq	$120, %rsp
	ret
	.p2align 4,,10
	.p2align 3
.L2489:
	movq	(%r9), %rcx
	shrq	$4, %rcx
	cmpq	%rcx, %rdx
	jnb	.L2486
	salq	$5, %rdx
	addq	8(%r9), %rdx
	movq	(%rdx), %rcx
	movzbl	16(%rdx), %r8d
	movq	%rcx, 48(%rsp)
	movq	8(%rdx), %rcx
	movq	%rcx, 56(%rsp)
	jmp	.L2486
	.p2align 4,,10
	.p2align 3
.L2488:
	movq	(%r9), %r8
	leaq	(%rdx,%rdx,4), %rcx
	salq	$4, %rdx
	addq	8(%r9), %rdx
	shrq	$4, %r8
	shrq	%cl, %r8
	movq	(%rdx), %rcx
	movq	8(%rdx), %rdx
	andl	$31, %r8d
	movq	%rcx, 48(%rsp)
	movq	%rdx, 56(%rsp)
	jmp	.L2486
	.seh_endproc
	.section .rdata,"dr"
	.align 32
CSWTCH.514:
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
.LC24:
	.long	-1
	.long	-1
	.long	32766
	.long	0
	.align 16
.LC30:
	.long	-1
	.long	2147483647
	.long	0
	.long	0
	.align 8
.LC31:
	.long	-1
	.long	2146435071
	.align 16
.LC32:
	.long	2147483647
	.long	0
	.long	0
	.long	0
	.align 4
.LC33:
	.long	2139095039
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSt13runtime_errorD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
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
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
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
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
