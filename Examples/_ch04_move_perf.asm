	.file	"_ch04_move_perf.cpp"
	.text
	.p2align 4
	.globl	_Z6mv_vecSt6vectorIiSaIiEE
	.def	_Z6mv_vecSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6mv_vecSt6vectorIiSaIiEE
_Z6mv_vecSt6vectorIiSaIiEE:
.LFB9351:
	.seh_endprologue
	pxor	%xmm0, %xmm0
	movdqu	(%rdx), %xmm1
	movq	%rcx, %rax
	movups	%xmm1, (%rcx)
	movq	16(%rdx), %rcx
	movq	$0, 16(%rdx)
	movups	%xmm0, (%rdx)
	movq	%rcx, 16(%rax)
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6cp_vecRKSt6vectorIiSaIiEE
	.def	_Z6cp_vecRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6cp_vecRKSt6vectorIiSaIiEE
_Z6cp_vecRKSt6vectorIiSaIiEE:
.LFB9361:
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	pxor	%xmm0, %xmm0
	movq	8(%rdx), %rsi
	subq	(%rdx), %rsi
	movq	%rcx, %rbx
	movq	%rdx, %rdi
	movups	%xmm0, (%rcx)
	movq	$0, 16(%rcx)
	je	.L9
	movabsq	$9223372036854775804, %rax
	cmpq	%rsi, %rax
	jb	.L10
	movq	%rsi, %rcx
	call	_Znwy
	movq	%rax, %rcx
.L4:
	addq	%rcx, %rsi
	movq	%rcx, %xmm1
	movq	%rsi, 16(%rbx)
	movddup	%xmm1, %xmm0
	movups	%xmm0, (%rbx)
	movq	(%rdi), %rdx
	movq	8(%rdi), %r8
	subq	%rdx, %r8
	cmpq	$4, %r8
	jle	.L6
	movq	%r8, %rsi
	call	memmove
	movq	%rax, %rcx
.L7:
	addq	%rsi, %rcx
	movq	%rbx, %rax
	movq	%rcx, 8(%rbx)
	addq	$32, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	ret
	.p2align 4,,10
	.p2align 3
.L9:
	xorl	%ecx, %ecx
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L6:
	movq	%r8, %rsi
	jne	.L7
	movl	(%rdx), %eax
	movl	$4, %esi
	movl	%eax, (%rcx)
	jmp	.L7
	.p2align 4,,10
	.p2align 3
.L10:
	call	_ZSt28__throw_bad_array_new_lengthv
	nop
	.seh_endproc
	.p2align 4
	.globl	_Z9mv_assignRSt6vectorIiSaIiEES2_
	.def	_Z9mv_assignRSt6vectorIiSaIiEES2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9mv_assignRSt6vectorIiSaIiEES2_
_Z9mv_assignRSt6vectorIiSaIiEES2_:
.LFB9362:
	.seh_endprologue
	pxor	%xmm0, %xmm0
	movdqu	(%rdx), %xmm1
	movq	(%rcx), %rax
	movq	16(%rcx), %r8
	movups	%xmm1, (%rcx)
	movq	16(%rdx), %r9
	testq	%rax, %rax
	movq	%r9, 16(%rcx)
	movups	%xmm0, (%rdx)
	movq	$0, 16(%rdx)
	je	.L11
	movq	%r8, %rdx
	movq	%rax, %rcx
	subq	%rax, %rdx
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L11:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.def	_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:
.LFB9366:
	pushq	%rbx
	.seh_pushreg	%rbx
	.seh_endprologue
	movq	%rcx, %r9
	movq	%rdx, %rax
	leaq	16(%rcx), %rcx
	movq	8(%rax), %r8
	movq	%rcx, (%r9)
	movq	(%rdx), %rdx
	leaq	16(%rax), %r10
	cmpq	%r10, %rdx
	je	.L29
	movq	%rdx, (%r9)
	movq	16(%rax), %rdx
	movq	%rdx, 16(%r9)
.L21:
	movq	%r8, 8(%r9)
	movq	%r10, (%rax)
	movq	$0, 8(%rax)
	movb	$0, 16(%rax)
	movq	%r9, %rax
	popq	%rbx
	ret
	.p2align 4,,10
	.p2align 3
.L29:
	leaq	1(%r8), %rdx
	cmpl	$8, %edx
	jnb	.L15
	testb	$4, %dl
	jne	.L30
	testl	%edx, %edx
	je	.L21
	movzbl	16(%rax), %r8d
	testb	$2, %dl
	movb	%r8b, 16(%r9)
	je	.L28
	movl	%edx, %edx
	movzwl	-2(%r10,%rdx), %r8d
	movw	%r8w, -2(%rcx,%rdx)
	movq	8(%rax), %r8
	jmp	.L21
	.p2align 4,,10
	.p2align 3
.L15:
	movl	%edx, %r8d
	subl	$1, %edx
	movq	-8(%r10,%r8), %r11
	cmpl	$8, %edx
	movq	%r11, -8(%rcx,%r8)
	jb	.L28
	andl	$-8, %edx
	xorl	%r8d, %r8d
.L19:
	movl	%r8d, %r11d
	addl	$8, %r8d
	movq	(%r10,%r11), %rbx
	cmpl	%edx, %r8d
	movq	%rbx, (%rcx,%r11)
	jb	.L19
.L28:
	movq	8(%rax), %r8
	jmp	.L21
.L30:
	movl	16(%rax), %r8d
	movl	%edx, %edx
	movl	%r8d, 16(%r9)
	movl	-4(%r10,%rdx), %r8d
	movl	%r8d, -4(%rcx,%rdx)
	movq	8(%rax), %r8
	jmp	.L21
	.seh_endproc
	.p2align 4
	.globl	_Z7read_tlv
	.def	_Z7read_tlv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7read_tlv
_Z7read_tlv:
.LFB9367:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	leaq	__emutls_v.tl_var(%rip), %rcx
	call	__emutls_get_address
	movl	(%rax), %eax
	addq	$40, %rsp
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8write_tli
	.def	_Z8write_tli;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8write_tli
_Z8write_tli:
.LFB9368:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movl	%ecx, %ebx
	leaq	__emutls_v.tl_var(%rip), %rcx
	call	__emutls_get_address
	movl	%ebx, (%rax)
	addq	$32, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8null_ptrv
	.def	_Z8null_ptrv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8null_ptrv
_Z8null_ptrv:
.LFB9369:
	.seh_endprologue
	xorl	%eax, %eax
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorIiSaIiEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIiSaIiEED1Ev
	.def	_ZNSt6vectorIiSaIiEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIiSaIiEED1Ev
_ZNSt6vectorIiSaIiEED1Ev:
.LFB9724:
	.seh_endprologue
	movq	(%rcx), %rax
	testq	%rax, %rax
	je	.L34
	movq	16(%rcx), %rdx
	movq	%rax, %rcx
	subq	%rax, %rdx
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L34:
	ret
	.seh_endproc
	.text
	.p2align 4
	.def	_ZL19bench_vec_move_calliiid;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL19bench_vec_move_calliiid
_ZL19bench_vec_move_calliiid:
.LFB9370:
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
	subq	$248, %rsp
	.seh_stackalloc	248
	movaps	%xmm6, 208(%rsp)
	.seh_savexmm	%xmm6, 208
	movaps	%xmm7, 224(%rsp)
	.seh_savexmm	%xmm7, 224
	.seh_endprologue
	xorl	%r9d, %r9d
	xorl	%esi, %esi
	movslq	%ecx, %r11
	movapd	%xmm3, %xmm7
	movl	%edx, %ecx
	.p2align 4,,10
	.p2align 3
.L38:
	rdtsc
	xorl	%ebx, %ebx
	movq	%rax, %r10
	salq	$32, %rdx
	orq	%rdx, %r10
	.p2align 4,,10
	.p2align 3
.L37:
	movl	%ebx, %r15d
	addl	$1, %ebx
	cmpl	%ebx, %ecx
	jne	.L37
	rdtsc
	leal	1(%r9), %edi
	salq	$32, %rdx
	subq	%r10, %rsi
	orq	%rdx, %rax
	addq	%rax, %rsi
	cmpl	%edi, %r8d
	je	.L68
	movl	%edi, %r9d
	jmp	.L38
	.p2align 4,,10
	.p2align 3
.L68:
	leaq	0(,%r11,4), %rax
	xorl	%r14d, %r14d
	movq	%rsi, 64(%rsp)
	movq	%rax, 48(%rsp)
	leaq	112(%rsp), %r13
	xorl	%eax, %eax
	leaq	176(%rsp), %rbp
	movq	%rax, %rsi
	movl	%edi, 72(%rsp)
	leaq	144(%rsp), %r12
	movl	%ebx, 76(%rsp)
	movl	%r14d, 56(%rsp)
	movl	%r9d, 60(%rsp)
	.p2align 4,,10
	.p2align 3
.L44:
	movq	48(%rsp), %rdi
	movq	%rdi, %rcx
	call	_Znwy
	addq	%rax, %rdi
	movq	%rax, %rcx
	movq	%rax, 80(%rsp)
	movq	%rdi, %rdx
	movq	%rdi, 96(%rsp)
	subq	%rax, %rdx
	andl	$4, %edx
	je	.L39
	movl	$42, (%rax)
	leaq	4(%rax), %rax
	cmpq	%rax, %rdi
	je	.L66
	.p2align 4,,10
	.p2align 3
.L39:
	movl	$42, (%rax)
	addq	$8, %rax
	movl	$42, -4(%rax)
	cmpq	%rax, %rdi
	jne	.L39
.L66:
	movq	%rdi, 88(%rsp)
	rdtsc
	xorl	%ebx, %ebx
	movq	%rax, %r9
	salq	$32, %rdx
	movq	%rcx, %xmm6
	movq	%rsi, 40(%rsp)
	orq	%rdx, %r9
	movq	%rdi, %xmm4
	movq	%r9, %r14
	punpcklqdq	%xmm4, %xmm6
	jmp	.L42
	.p2align 4,,10
	.p2align 3
.L47:
	movl	%eax, %ebx
.L42:
	movq	%r13, %rcx
	movq	%rbp, %rdx
	movaps	%xmm6, 176(%rsp)
	movq	%rdi, 192(%rsp)
	call	_Z6mv_vecSt6vectorIiSaIiEE
	movq	176(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L40
	movq	192(%rsp), %rdx
	subq	%rcx, %rdx
	call	_ZdlPvy
.L40:
	movq	128(%rsp), %rax
	movq	%rbp, %rcx
	movq	%r12, %rdx
	movdqa	112(%rsp), %xmm2
	movaps	%xmm2, 144(%rsp)
	movq	%rax, 160(%rsp)
	call	_Z6mv_vecSt6vectorIiSaIiEE
	movq	144(%rsp), %rcx
	movq	192(%rsp), %rdi
	movdqa	176(%rsp), %xmm6
	movq	176(%rsp), %rsi
	testq	%rcx, %rcx
	movaps	%xmm6, 80(%rsp)
	movq	%rdi, 96(%rsp)
	je	.L41
	movq	160(%rsp), %rdx
	subq	%rcx, %rdx
	call	_ZdlPvy
.L41:
	leal	1(%rbx), %eax
	cmpl	%ebx, %r15d
	jne	.L47
	movq	%r14, %r9
	movq	%rsi, %r14
	movq	40(%rsp), %rsi
	rdtsc
	salq	$32, %rdx
	subq	%r9, %rsi
	orq	%rdx, %rax
	addq	%rax, %rsi
	testq	%r14, %r14
	je	.L43
	subq	%r14, %rdi
	movq	%r14, %rcx
	movq	%rdi, %rdx
	call	_ZdlPvy
.L43:
	movl	56(%rsp), %edi
	movl	60(%rsp), %ebx
	leal	1(%rdi), %eax
	cmpl	%ebx, %edi
	je	.L69
	movl	%eax, 56(%rsp)
	jmp	.L44
.L69:
.L49:
	movq	%rsi, %rax
	movq	64(%rsp), %rsi
	movl	$0, %edx
	pxor	%xmm0, %xmm0
	movl	72(%rsp), %edi
	pxor	%xmm1, %xmm1
	movl	76(%rsp), %ebx
	movaps	208(%rsp), %xmm6
	subq	%rsi, %rax
	cmovs	%rdx, %rax
	imull	%ebx, %edi
	cvtsi2sdq	%rax, %xmm0
	leal	(%rdi,%rdi), %eax
	cvtsi2sdl	%eax, %xmm1
	divsd	%xmm1, %xmm0
	mulsd	%xmm7, %xmm0
	movaps	224(%rsp), %xmm7
	addq	$248, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL14bench_vec_copyii;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL14bench_vec_copyii
_ZL14bench_vec_copyii:
.LFB9375:
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
	subq	$64, %rsp
	.seh_stackalloc	64
	.seh_endprologue
	xorl	%ebp, %ebp
	xorl	%r12d, %r12d
	movslq	%ecx, %rcx
	movl	%edx, %r13d
	leaq	0(,%rcx,4), %rsi
.L72:
	movq	%rsi, %rcx
.LEHB0:
	call	_Znwy
.LEHE0:
	leaq	(%rax,%rsi), %rdx
	movq	%rax, %rbx
	movq	%rax, 32(%rsp)
	movq	%rdx, %rcx
	movq	%rdx, 48(%rsp)
	subq	%rax, %rcx
	andl	$4, %ecx
	je	.L71
	movl	$42, (%rax)
	leaq	4(%rax), %rax
	cmpq	%rax, %rdx
	je	.L83
	.p2align 4,,10
	.p2align 3
.L71:
	movl	$42, (%rax)
	addq	$8, %rax
	movl	$42, -4(%rax)
	cmpq	%rax, %rdx
	jne	.L71
.L83:
	movq	%rdx, 40(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rsi, %rcx
	movq	%rax, %r14
.LEHB1:
	call	_Znwy
.LEHE1:
	movq	%rsi, %r8
	movq	%rbx, %rdx
	movq	%rax, %rcx
	movq	%rax, %rdi
	addl	$1, %ebp
	call	memcpy
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rsi, %rdx
	movq	%rdi, %rcx
	subq	%r14, %rax
	addq	%rax, %r12
	call	_ZdlPvy
	movq	%rsi, %rdx
	movq	%rbx, %rcx
	call	_ZdlPvy
	cmpl	%ebp, %r13d
	jne	.L72
	pxor	%xmm0, %xmm0
	pxor	%xmm1, %xmm1
	cvtsi2sdq	%r12, %xmm0
	cvtsi2sdl	%r13d, %xmm1
	divsd	%xmm1, %xmm0
	addq	$64, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	ret
.L74:
	leaq	32(%rsp), %rcx
	movq	%rax, %rbx
	call	_ZNSt6vectorIiSaIiEED1Ev
	movq	%rbx, %rcx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA9375:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE9375-.LLSDACSB9375
.LLSDACSB9375:
	.uleb128 .LEHB0-.LFB9375
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB9375
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L74-.LFB9375
	.uleb128 0
	.uleb128 .LEHB2-.LFB9375
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE9375:
	.text
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_insert\0"
	.section	.text$_ZNSt6vectorI5OwnedSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorI5OwnedSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
	.def	_ZNSt6vectorI5OwnedSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI5OwnedSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
_ZNSt6vectorI5OwnedSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_:
.LFB10094:
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
	movaps	%xmm6, 32(%rsp)
	.seh_savexmm	%xmm6, 32
	.seh_endprologue
	movq	8(%rcx), %r12
	movq	(%rcx), %rdi
	movq	%r12, %rax
	movq	%rdx, %rbx
	movq	%rcx, %rbp
	movabsq	$1152921504606846975, %rdx
	subq	%rdi, %rax
	movq	%r8, %r14
	sarq	$3, %rax
	cmpq	%rdx, %rax
	je	.L106
	movq	%rbx, %r15
	subq	%rdi, %r15
	cmpq	%r12, %rdi
	je	.L107
	leaq	(%rax,%rax), %rdx
	cmpq	%rax, %rdx
	jb	.L99
	testq	%rdx, %rdx
	jne	.L108
	movq	(%r8), %rax
	xorl	%esi, %esi
	xorl	%r13d, %r13d
	cmpq	%rdi, %rbx
	movq	$0, (%r8)
	movl	$8, %ecx
	movq	%rax, (%r15)
	je	.L97
.L92:
	movq	%rbx, %r8
	movq	%rdi, %rax
	movq	%r13, %rdx
	subq	%rdi, %r8
	.p2align 4,,10
	.p2align 3
.L94:
	movq	(%rax), %rcx
	addq	$8, %rax
	addq	$8, %rdx
	movq	%rcx, -8(%rdx)
	cmpq	%rbx, %rax
	jne	.L94
	leaq	8(%r13,%r8), %rcx
.L93:
	cmpq	%r12, %rbx
	je	.L95
.L97:
	subq	%rbx, %r12
	movq	%rbx, %rdx
	movq	%r12, %r8
	call	memcpy
	movq	%rax, %rcx
	addq	%r12, %rcx
.L95:
	movq	%r13, %xmm6
	movq	%rcx, %xmm0
	testq	%rdi, %rdi
	punpcklqdq	%xmm0, %xmm6
	je	.L96
	movq	16(%rbp), %rdx
	movq	%rdi, %rcx
	subq	%rdi, %rdx
	call	_ZdlPvy
.L96:
	movups	%xmm6, 0(%rbp)
	movq	%rsi, 16(%rbp)
	movaps	32(%rsp), %xmm6
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
.L99:
	movabsq	$9223372036854775800, %rsi
.L90:
	movq	%rsi, %rcx
	call	_Znwy
	movq	%rax, %r13
	addq	%rax, %rsi
	movq	(%r14), %rax
	cmpq	%rdi, %rbx
	movq	$0, (%r14)
	leaq	8(%r13), %rcx
	movq	%rax, 0(%r13,%r15)
	jne	.L92
	jmp	.L93
	.p2align 4,,10
	.p2align 3
.L107:
	addq	$1, %rax
	jc	.L99
	movabsq	$1152921504606846975, %rdx
	cmpq	%rdx, %rax
	movq	%rdx, %rsi
	cmovbe	%rax, %rsi
	salq	$3, %rsi
	jmp	.L90
.L108:
	movabsq	$1152921504606846975, %rax
	cmpq	%rax, %rdx
	cmova	%rax, %rdx
	leaq	0(,%rdx,8), %rsi
	jmp	.L90
.L106:
	leaq	.LC0(%rip), %rcx
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt12_Destroy_auxILb0EE9__destroyIP13OwnedThrowingEEvT_S4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt12_Destroy_auxILb0EE9__destroyIP13OwnedThrowingEEvT_S4_
	.def	_ZNSt12_Destroy_auxILb0EE9__destroyIP13OwnedThrowingEEvT_S4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Destroy_auxILb0EE9__destroyIP13OwnedThrowingEEvT_S4_
_ZNSt12_Destroy_auxILb0EE9__destroyIP13OwnedThrowingEEvT_S4_:
.LFB10197:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	cmpq	%rdx, %rcx
	movq	%rcx, %rbx
	movq	%rdx, %rsi
	je	.L109
	.p2align 4,,10
	.p2align 3
.L112:
	movq	(%rbx), %rcx
	testq	%rcx, %rcx
	je	.L111
	call	_ZdaPv
.L111:
	addq	$8, %rbx
	cmpq	%rbx, %rsi
	jne	.L112
.L109:
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.seh_endproc
	.section	.text$_ZSt16__do_uninit_copyIPK13OwnedThrowingPS0_ET0_T_S5_S4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt16__do_uninit_copyIPK13OwnedThrowingPS0_ET0_T_S5_S4_
	.def	_ZSt16__do_uninit_copyIPK13OwnedThrowingPS0_ET0_T_S5_S4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt16__do_uninit_copyIPK13OwnedThrowingPS0_ET0_T_S5_S4_
_ZSt16__do_uninit_copyIPK13OwnedThrowingPS0_ET0_T_S5_S4_:
.LFB10269:
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
	cmpq	%rdx, %rcx
	movq	%rcx, %rbx
	movq	%rdx, %rdi
	movq	%r8, %rbp
	movq	%r8, %rsi
	je	.L117
	.p2align 4,,10
	.p2align 3
.L120:
	movl	$256, %ecx
.LEHB3:
	call	_Znay
.LEHE3:
	movq	(%rbx), %r8
	movq	%rax, (%rsi)
	xorl	%edx, %edx
	.p2align 4,,10
	.p2align 3
.L119:
	movl	(%r8,%rdx), %ecx
	movl	%ecx, (%rax,%rdx)
	addq	$4, %rdx
	cmpq	$256, %rdx
	jne	.L119
	addq	$8, %rbx
	addq	$8, %rsi
	cmpq	%rbx, %rdi
	jne	.L120
.L117:
	movq	%rsi, %rax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
.L124:
	movq	%rax, %rcx
	call	__cxa_begin_catch
	movq	%rsi, %rdx
	movq	%rbp, %rcx
	call	_ZNSt12_Destroy_auxILb0EE9__destroyIP13OwnedThrowingEEvT_S4_
.LEHB4:
	call	__cxa_rethrow
.LEHE4:
.L125:
	movq	%rax, %rbx
	call	__cxa_end_catch
	movq	%rbx, %rcx
.LEHB5:
	call	_Unwind_Resume
	nop
.LEHE5:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA10269:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT10269-.LLSDATTD10269
.LLSDATTD10269:
	.byte	0x1
	.uleb128 .LLSDACSE10269-.LLSDACSB10269
.LLSDACSB10269:
	.uleb128 .LEHB3-.LFB10269
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L124-.LFB10269
	.uleb128 0x1
	.uleb128 .LEHB4-.LFB10269
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L125-.LFB10269
	.uleb128 0
	.uleb128 .LEHB5-.LFB10269
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSE10269:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT10269:
	.section	.text$_ZSt16__do_uninit_copyIPK13OwnedThrowingPS0_ET0_T_S5_S4_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt6vectorI13OwnedThrowingSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorI13OwnedThrowingSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
	.def	_ZNSt6vectorI13OwnedThrowingSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI13OwnedThrowingSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
_ZNSt6vectorI13OwnedThrowingSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_:
.LFB10108:
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
	movaps	%xmm6, 32(%rsp)
	.seh_savexmm	%xmm6, 32
	.seh_endprologue
	movq	8(%rcx), %rsi
	movq	(%rcx), %rdi
	movq	%rsi, %rax
	movq	%rdx, %rbx
	movq	%rcx, %rbp
	movabsq	$1152921504606846975, %rdx
	subq	%rdi, %rax
	movq	%r8, %r14
	sarq	$3, %rax
	cmpq	%rdx, %rax
	je	.L166
	movq	%rbx, %r15
	subq	%rdi, %r15
	cmpq	%rsi, %rdi
	je	.L167
	leaq	(%rax,%rax), %r12
	cmpq	%rax, %r12
	jb	.L148
	testq	%r12, %r12
	jne	.L168
	xorl	%r13d, %r13d
.L134:
	movq	(%r14), %rax
	addq	%r13, %r15
	movq	$0, (%r14)
	movq	%r13, %r8
	movq	%rbx, %rdx
	movq	%rdi, %rcx
	movq	%rax, (%r15)
.LEHB6:
	call	_ZSt16__do_uninit_copyIPK13OwnedThrowingPS0_ET0_T_S5_S4_
.LEHE6:
	leaq	8(%rax), %r14
	movq	%rsi, %rdx
	movq	%rbx, %rcx
	movq	%r14, %r8
.LEHB7:
	call	_ZSt16__do_uninit_copyIPK13OwnedThrowingPS0_ET0_T_S5_S4_
.LEHE7:
	movq	%r13, %xmm6
	movq	%rax, %xmm0
	cmpq	%rsi, %rdi
	movq	%rdi, %rbx
	punpcklqdq	%xmm0, %xmm6
	je	.L142
	.p2align 4,,10
	.p2align 3
.L138:
	movq	(%rbx), %rcx
	testq	%rcx, %rcx
	je	.L141
	call	_ZdaPv
.L141:
	addq	$8, %rbx
	cmpq	%rbx, %rsi
	jne	.L138
.L142:
	testq	%rdi, %rdi
	je	.L140
	movq	16(%rbp), %rdx
	movq	%rdi, %rcx
	subq	%rdi, %rdx
	call	_ZdlPvy
.L140:
	leaq	0(%r13,%r12,8), %rax
	movups	%xmm6, 0(%rbp)
	movq	%rax, 16(%rbp)
	movaps	32(%rsp), %xmm6
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
.L148:
	movabsq	$9223372036854775800, %rcx
	movq	%rdx, %r12
.L133:
.LEHB8:
	call	_Znwy
	movq	%rax, %r13
	jmp	.L134
	.p2align 4,,10
	.p2align 3
.L167:
	addq	$1, %rax
	jc	.L148
	movabsq	$1152921504606846975, %r12
	cmpq	%r12, %rax
	cmovbe	%rax, %r12
	leaq	0(,%r12,8), %rcx
	jmp	.L133
.L168:
	movabsq	$1152921504606846975, %rax
	cmpq	%rax, %r12
	cmova	%rax, %r12
	leaq	0(,%r12,8), %rcx
	jmp	.L133
.L166:
	leaq	.LC0(%rip), %rcx
	call	_ZSt20__throw_length_errorPKc
.LEHE8:
.L153:
	movq	%rax, %rcx
	call	__cxa_begin_catch
	movq	(%r15), %rcx
	testq	%rcx, %rcx
	je	.L137
	call	_ZdaPv
	jmp	.L137
.L151:
	movq	%rax, %rcx
	call	__cxa_begin_catch
	movq	%r14, %rdx
	movq	%r13, %rcx
	call	_ZNSt12_Destroy_auxILb0EE9__destroyIP13OwnedThrowingEEvT_S4_
.L137:
	testq	%r13, %r13
	je	.L145
	leaq	0(,%r12,8), %rdx
	movq	%r13, %rcx
	call	_ZdlPvy
.L145:
.LEHB9:
	call	__cxa_rethrow
.LEHE9:
.L152:
	movq	%rax, %rbx
	call	__cxa_end_catch
	movq	%rbx, %rcx
.LEHB10:
	call	_Unwind_Resume
	nop
.LEHE10:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA10108:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT10108-.LLSDATTD10108
.LLSDATTD10108:
	.byte	0x1
	.uleb128 .LLSDACSE10108-.LLSDACSB10108
.LLSDACSB10108:
	.uleb128 .LEHB6-.LFB10108
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L153-.LFB10108
	.uleb128 0x1
	.uleb128 .LEHB7-.LFB10108
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L151-.LFB10108
	.uleb128 0x1
	.uleb128 .LEHB8-.LFB10108
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB9-.LFB10108
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L152-.LFB10108
	.uleb128 0
	.uleb128 .LEHB10-.LFB10108
	.uleb128 .LEHE10-.LEHB10
	.uleb128 0
	.uleb128 0
.LLSDACSE10108:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT10108:
	.section	.text$_ZNSt6vectorI13OwnedThrowingSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,"x"
	.linkonce discard
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC2:
	.ascii "=== ch04 move \350\257\255\344\271\211\347\234\237\345\256\236\345\237\272\345\207\206 (MinGW GCC 13.1.0 -O2 x86_64) ===\12\0"
.LC3:
	.ascii "[TSC] \0"
.LC5:
	.ascii " GHz | \0"
	.align 8
.LC6:
	.ascii "[\346\263\250] \346\225\260\345\200\274\351\232\217 CPU/\351\242\221\347\216\207/\345\270\246\345\256\275\345\217\230\345\214\226\357\274\214\344\273\205\344\273\243\350\241\250\346\234\254\346\234\272\357\274\233\345\200\215\346\225\260\344\274\230\345\212\277\347\250\263\345\256\232\12\12\0"
	.align 8
.LC7:
	.ascii "[vector<int>(1M)]  move(\345\220\253\350\260\203\347\224\250\345\274\200\351\224\200\344\270\212\347\225\214) = \0"
.LC8:
	.ascii " ns | copy = \0"
	.align 8
.LC9:
	.ascii " ns | (\347\272\257 move \344\273\205 3 \346\214\207\351\222\210\344\272\244\346\215\242, \350\247\201\351\231\204\345\275\225 H \346\261\207\347\274\226)\12\0"
	.align 8
.LC10:
	.ascii "[vector<int>(1K)]   move(\345\220\253\350\260\203\347\224\250\345\274\200\351\224\200\344\270\212\347\225\214) = \0"
.LC11:
	.ascii " ns\12\0"
	.align 8
.LC14:
	.ascii "[string(1KB)]      move(\345\220\253\350\260\203\347\224\250\345\274\200\351\224\200\344\270\212\347\225\214) = \0"
	.align 8
.LC17:
	.ascii "[realloc 20K \345\205\203\347\264\240] Owned(noexcept move\342\206\222\346\265\205\347\247\273\345\212\250) = \0"
.LC18:
	.ascii " ns | \0"
	.align 8
.LC19:
	.ascii "OwnedThrowing(\351\235\236noexcept\342\206\222\346\267\261\346\213\267\350\264\235) = \0"
.LC20:
	.ascii " ns | \346\257\224 \342\211\210 \0"
.LC21:
	.ascii "x\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB9423:
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
	subq	$264, %rsp
	.seh_stackalloc	264
	movaps	%xmm6, 224(%rsp)
	.seh_savexmm	%xmm6, 224
	movaps	%xmm7, 240(%rsp)
	.seh_savexmm	%xmm7, 240
	.seh_endprologue
	call	__main
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, %rsi
	rdtsc
	movq	%rax, %rdi
	salq	$32, %rdx
	orq	%rdx, %rdi
	rdtsc
	movq	%rax, %rcx
	salq	$32, %rdx
	orq	%rdx, %rcx
	.p2align 4,,10
	.p2align 3
.L170:
	rdtsc
	salq	$32, %rdx
	orq	%rdx, %rax
	subq	%rcx, %rax
	cmpq	$299999999, %rax
	jbe	.L170
	rdtsc
	salq	$32, %rdx
	movq	%rax, %rbx
	orq	%rdx, %rbx
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rdi, %rbx
	js	.L171
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rbx, %xmm0
.L172:
	subq	%rsi, %rax
	pxor	%xmm1, %xmm1
	xorl	%r13d, %r13d
	movsd	.LC1(%rip), %xmm6
	cvtsi2sdq	%rax, %xmm1
	movq	.refptr._ZSt4cout(%rip), %rcx
	leaq	.LC2(%rip), %rdx
	divsd	%xmm6, %xmm1
	divsd	%xmm1, %xmm0
	divsd	%xmm0, %xmm6
.LEHB11:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movq	.refptr._ZSt4cout(%rip), %rcx
	leaq	.LC3(%rip), %rdx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	.LC4(%rip), %xmm1
	movq	%rax, %rcx
	divsd	%xmm6, %xmm1
	call	_ZNSo9_M_insertIdEERSoT_
	leaq	.LC5(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	leaq	.LC6(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	%xmm6, %xmm3
	movl	$200, %r8d
	movl	$3000, %edx
	movl	$1000000, %ecx
	call	_ZL19bench_vec_move_calliiid
	movl	$200, %edx
	movl	$1000000, %ecx
	movsd	%xmm0, 40(%rsp)
	call	_ZL14bench_vec_copyii
	movq	.refptr._ZSt4cout(%rip), %rcx
	leaq	.LC7(%rip), %rdx
	movapd	%xmm0, %xmm7
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	40(%rsp), %xmm1
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIdEERSoT_
	leaq	.LC8(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	%xmm7, %xmm1
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIdEERSoT_
	leaq	.LC9(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movl	$150, %r8d
	movapd	%xmm6, %xmm3
	movl	$4000, %edx
	movl	$1000, %ecx
	call	_ZL19bench_vec_move_calliiid
	movl	$50000, %edx
	movl	$1000, %ecx
	movsd	%xmm0, 40(%rsp)
	call	_ZL14bench_vec_copyii
	movq	.refptr._ZSt4cout(%rip), %rcx
	leaq	.LC10(%rip), %rdx
	movapd	%xmm0, %xmm7
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	40(%rsp), %xmm1
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIdEERSoT_
	leaq	.LC8(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	%xmm7, %xmm1
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIdEERSoT_
	leaq	.LC11(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movl	$150, %r8d
	.p2align 4,,10
	.p2align 3
.L174:
	rdtsc
	movq	%rax, %rcx
	salq	$32, %rdx
	movl	$4000, %eax
	orq	%rdx, %rcx
.L173:
	subl	$2, %eax
	jne	.L173
	rdtsc
	salq	$32, %rdx
	subq	%rcx, %r13
	orq	%rdx, %rax
	addq	%rax, %r13
	subl	$1, %r8d
	jne	.L174
	leaq	96(%rsp), %rax
	xorl	%r15d, %r15d
	xorl	%r14d, %r14d
	movq	%r13, 88(%rsp)
	movq	%rax, 80(%rsp)
	leaq	128(%rsp), %rax
	movq	%rax, 48(%rsp)
	leaq	160(%rsp), %rax
	movl	$150, 76(%rsp)
	leaq	112(%rsp), %rbp
	leaq	208(%rsp), %rbx
	movq	%rax, 40(%rsp)
	leaq	192(%rsp), %rdi
	movq	%r15, 56(%rsp)
	leaq	144(%rsp), %r12
	leaq	176(%rsp), %rsi
	.p2align 4,,10
	.p2align 3
.L212:
	movq	80(%rsp), %rcx
	movl	$120, %r8d
	movl	$1024, %edx
	movq	%rbp, 96(%rsp)
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
	rdtsc
	movl	$4000, %r13d
	movq	%rax, %r8
	salq	$32, %rdx
	orq	%rdx, %r8
	movq	%r8, 64(%rsp)
	jmp	.L210
	.p2align 4,,10
	.p2align 3
.L175:
	movq	%rax, 192(%rsp)
	movq	112(%rsp), %rax
	movq	%rax, 208(%rsp)
.L182:
	movq	48(%rsp), %rcx
	movq	%rdx, 200(%rsp)
	movq	%rdi, %rdx
	movq	%rbp, 96(%rsp)
	movq	%r14, 104(%rsp)
	movb	$0, 112(%rsp)
	call	_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	movq	192(%rsp), %rcx
	cmpq	%rbx, %rcx
	je	.L183
	movq	208(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
	movq	128(%rsp), %rdx
	movq	%rbx, 192(%rsp)
	cmpq	%r12, %rdx
	je	.L380
	movq	96(%rsp), %r15
	movq	136(%rsp), %r8
.L272:
	movq	%rdx, 192(%rsp)
	movq	144(%rsp), %rdx
	movq	%r8, %rcx
	movq	%rdx, 208(%rsp)
.L186:
	movq	%rcx, 200(%rsp)
	movq	40(%rsp), %rcx
	movq	%rdi, %rdx
	movq	%r12, 128(%rsp)
	movq	%r14, 136(%rsp)
	movb	$0, 144(%rsp)
	call	_Z6mv_strNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	movq	160(%rsp), %rdx
	cmpq	%rsi, %rdx
	je	.L381
	movdqu	168(%rsp), %xmm0
	cmpq	%rbp, %r15
	je	.L382
	testq	%r15, %r15
	movq	112(%rsp), %rcx
	movq	%rdx, 96(%rsp)
	movups	%xmm0, 104(%rsp)
	je	.L206
	movq	%r15, 160(%rsp)
	movq	%rcx, 176(%rsp)
.L205:
	movq	%r14, 168(%rsp)
	movb	$0, (%r15)
	movq	160(%rsp), %rcx
	cmpq	%rsi, %rcx
	je	.L207
	movq	176(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L207:
	movq	192(%rsp), %rcx
	cmpq	%rbx, %rcx
	je	.L208
	movq	208(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L208:
	movq	128(%rsp), %rcx
	cmpq	%r12, %rcx
	je	.L209
	movq	144(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L209:
	subl	$1, %r13d
	je	.L383
.L210:
	movq	96(%rsp), %rax
	movq	%rbx, 192(%rsp)
	movq	104(%rsp), %rdx
	cmpq	%rbp, %rax
	jne	.L175
	leaq	1(%rdx), %rcx
	movq	%rbx, %r9
	movq	%rbp, %rax
	cmpl	$8, %ecx
	jnb	.L384
.L176:
	xorl	%r8d, %r8d
	testb	$4, %cl
	je	.L179
	movl	(%rax), %r8d
	movl	%r8d, (%r9)
	movl	$4, %r8d
.L179:
	testb	$2, %cl
	je	.L180
	movzwl	(%rax,%r8), %r10d
	movw	%r10w, (%r9,%r8)
	addq	$2, %r8
.L180:
	andl	$1, %ecx
	je	.L182
	movzbl	(%rax,%r8), %eax
	movb	%al, (%r9,%r8)
	jmp	.L182
	.p2align 4,,10
	.p2align 3
.L382:
	movq	%rdx, 96(%rsp)
	movups	%xmm0, 104(%rsp)
.L206:
	movq	%rsi, 160(%rsp)
	leaq	176(%rsp), %rsi
	movq	%rsi, %r15
	jmp	.L205
	.p2align 4,,10
	.p2align 3
.L381:
	movq	168(%rsp), %rcx
	testq	%rcx, %rcx
	movq	%rcx, %r8
	je	.L195
	cmpq	$1, %rcx
	je	.L385
	cmpl	$8, %r8d
	movl	%ecx, %ecx
	jnb	.L199
	testb	$4, %r8b
	jne	.L386
	testl	%ecx, %ecx
	je	.L200
	movzbl	(%rsi), %edx
	testb	$2, %cl
	movb	%dl, (%r15)
	movq	168(%rsp), %r8
	jne	.L387
.L200:
	movq	96(%rsp), %r15
	movq	%r8, %rcx
.L195:
	movq	%rcx, 104(%rsp)
	movb	$0, (%r15,%rcx)
	movq	160(%rsp), %r15
	jmp	.L205
	.p2align 4,,10
	.p2align 3
.L183:
	movq	128(%rsp), %rdx
	movq	%rbp, %r15
	movq	136(%rsp), %r8
	cmpq	%r12, %rdx
	movq	%r8, %rcx
	jne	.L272
	leaq	1(%rcx), %r8
	movq	%rbx, %r10
	movq	%r12, %rdx
	cmpl	$8, %r8d
	jnb	.L388
	.p2align 4,,10
	.p2align 3
.L187:
	xorl	%r9d, %r9d
	testb	$4, %r8b
	je	.L190
	movl	(%rdx), %r9d
	movl	%r9d, (%r10)
	movl	$4, %r9d
.L190:
	testb	$2, %r8b
	je	.L191
	movzwl	(%rdx,%r9), %r11d
	movw	%r11w, (%r10,%r9)
	addq	$2, %r9
.L191:
	andl	$1, %r8d
	je	.L186
	movzbl	(%rdx,%r9), %edx
	movb	%dl, (%r10,%r9)
	jmp	.L186
	.p2align 4,,10
	.p2align 3
.L380:
	movq	136(%rsp), %rcx
	movq	%rbx, %r10
	movq	%r12, %rdx
	movq	96(%rsp), %r15
	leaq	1(%rcx), %r8
	cmpl	$8, %r8d
	jb	.L187
.L388:
	movl	%r8d, %r11d
	xorl	%edx, %edx
	andl	$-8, %r11d
.L188:
	movl	%edx, %eax
	addl	$8, %edx
	movq	(%r12,%rax), %r9
	cmpl	%r11d, %edx
	movq	%r9, (%rbx,%rax)
	jb	.L188
	leaq	(%rbx,%rdx), %r10
	addq	%r12, %rdx
	jmp	.L187
	.p2align 4,,10
	.p2align 3
.L383:
	movq	64(%rsp), %r8
	rdtsc
	movq	96(%rsp), %rcx
	salq	$32, %rdx
	orq	%rdx, %rax
	movq	56(%rsp), %rdx
	subq	%r8, %rdx
	addq	%rdx, %rax
	cmpq	%rbp, %rcx
	movq	%rax, 56(%rsp)
	je	.L211
	movq	112(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L211:
	subl	$1, 76(%rsp)
	jne	.L212
	movq	88(%rsp), %r13
	movl	$0, %edx
	pxor	%xmm1, %xmm1
	movl	$50000, %r15d
	movq	56(%rsp), %rax
	subq	%r13, %rax
	cmovs	%rdx, %rax
	xorl	%r14d, %r14d
	cvtsi2sdq	%rax, %xmm1
	divsd	.LC12(%rip), %xmm1
	mulsd	%xmm1, %xmm6
	jmp	.L213
	.p2align 4,,10
	.p2align 3
.L215:
	cmpq	$1, %rbp
	je	.L389
	testq	%rbp, %rbp
	jne	.L390
.L219:
	movq	%rbx, %rax
.L218:
	movq	%rbp, 200(%rsp)
	movb	$0, (%rax,%rbp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	192(%rsp), %rcx
	subq	%r12, %rax
	addq	%rax, %r14
	cmpq	%rbx, %rcx
	je	.L220
	movq	208(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L220:
	movq	160(%rsp), %rcx
	cmpq	%rsi, %rcx
	je	.L221
	movq	176(%rsp), %rax
	leaq	1(%rax), %rdx
	call	_ZdlPvy
.L221:
	subl	$1, %r15d
	je	.L391
.L281:
.L213:
	movq	40(%rsp), %rcx
	movl	$120, %r8d
	movl	$1024, %edx
	movq	%rsi, 160(%rsp)
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE11:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	168(%rsp), %rbp
	movq	%rbx, 192(%rsp)
	movq	160(%rsp), %r13
	movq	%rax, %r12
	cmpq	$15, %rbp
	movq	%rbp, 128(%rsp)
	jbe	.L215
	movq	48(%rsp), %rdx
	xorl	%r8d, %r8d
	movq	%rdi, %rcx
.LEHB12:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_createERyy
.LEHE12:
	movq	%rax, %rcx
	movq	%rax, 192(%rsp)
	movq	128(%rsp), %rax
	movq	%rax, 208(%rsp)
.L216:
	movq	%rbp, %r8
	movq	%r13, %rdx
	call	memcpy
	movq	128(%rsp), %rbp
	movq	192(%rsp), %rax
	jmp	.L218
	.p2align 4,,10
	.p2align 3
.L384:
	movl	%ecx, %r10d
	xorl	%eax, %eax
	andl	$-8, %r10d
.L177:
	movl	%eax, %r8d
	addl	$8, %eax
	movq	0(%rbp,%r8), %r9
	cmpl	%r10d, %eax
	movq	%r9, (%rbx,%r8)
	jb	.L177
	leaq	(%rbx,%rax), %r9
	addq	%rbp, %rax
	jmp	.L176
	.p2align 4,,10
	.p2align 3
.L389:
	movzbl	0(%r13), %eax
	movb	%al, 208(%rsp)
	jmp	.L219
	.p2align 4,,10
	.p2align 3
.L385:
	movzbl	176(%rsp), %edx
	movb	%dl, (%r15)
	movq	168(%rsp), %rcx
	movq	96(%rsp), %r15
	jmp	.L195
	.p2align 4,,10
	.p2align 3
.L199:
	movl	%r8d, %ecx
	movq	-8(%rsi,%rcx), %r9
	movq	%r9, -8(%r15,%rcx)
	leal	-1(%r8), %ecx
	cmpl	$8, %ecx
	jb	.L366
	andl	$-8, %ecx
	movl	%ecx, %r8d
	xorl	%ecx, %ecx
.L203:
	movl	%ecx, %eax
	addl	$8, %ecx
	movq	(%rdx,%rax), %r9
	cmpl	%r8d, %ecx
	movq	%r9, (%r15,%rax)
	jb	.L203
.L366:
	movq	168(%rsp), %r8
	jmp	.L200
	.p2align 4,,10
	.p2align 3
.L391:
	movq	.refptr._ZSt4cout(%rip), %rcx
	leaq	.LC14(%rip), %rdx
	pxor	%xmm7, %xmm7
	xorl	%r13d, %r13d
	cvtsi2sdq	%r14, %xmm7
	divsd	.LC13(%rip), %xmm7
	movl	$2000, %r12d
.LEHB13:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	%xmm6, %xmm1
	pxor	%xmm6, %xmm6
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIdEERSoT_
	leaq	.LC8(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	%xmm7, %xmm1
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIdEERSoT_
	leaq	.LC11(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE13:
	.p2align 4,,10
	.p2align 3
.L222:
	movl	$160000, %ecx
	movaps	%xmm6, 192(%rsp)
	movq	$0, 208(%rsp)
.LEHB14:
	call	_Znwy
	movq	%rax, %xmm4
	movq	%rax, %rbx
	movl	$20000, %esi
	leaq	160000(%rax), %rbp
	movddup	%xmm4, %xmm0
	movaps	%xmm0, 192(%rsp)
	movq	%rbp, 208(%rsp)
	jmp	.L227
	.p2align 4,,10
	.p2align 3
.L393:
	movq	%rax, (%rbx)
	addq	$8, %rbx
	subl	$1, %esi
	movq	%rbx, 200(%rsp)
	je	.L392
.L227:
	movl	$256, %ecx
	call	_Znay
.LEHE14:
	cmpq	%rbp, %rbx
	movq	%rax, 160(%rsp)
	jne	.L393
	movq	40(%rsp), %r8
	movq	%rbx, %rdx
	movq	%rdi, %rcx
.LEHB15:
	call	_ZNSt6vectorI5OwnedSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
.LEHE15:
	movq	160(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L367
	call	_ZdaPv
.L367:
	subl	$1, %esi
	movq	200(%rsp), %rbx
	movq	208(%rsp), %rbp
	jne	.L227
.L392:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movl	$256, %ecx
	movq	%rax, %rsi
.LEHB16:
	call	_Znay
.LEHE16:
	cmpq	%rbp, %rbx
	movq	%rax, 160(%rsp)
	je	.L228
	movq	%rax, (%rbx)
	addq	$8, %rbx
	movq	%rbx, 200(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	192(%rsp), %r14
	subq	%rsi, %rax
	addq	%rax, %r13
	cmpq	%r14, %rbx
	je	.L230
.L229:
	movq	%r14, %rsi
	.p2align 4,,10
	.p2align 3
.L235:
	movq	(%rsi), %rcx
	testq	%rcx, %rcx
	je	.L234
	call	_ZdaPv
.L234:
	addq	$8, %rsi
	cmpq	%rsi, %rbx
	jne	.L235
.L236:
	testq	%r14, %r14
	je	.L233
.L230:
	movq	%rbp, %rdx
	movq	%r14, %rcx
	subq	%r14, %rdx
	call	_ZdlPvy
.L233:
	subl	$1, %r12d
	jne	.L222
	pxor	%xmm7, %xmm7
	movl	$200, %r12d
	pxor	%xmm6, %xmm6
	cvtsi2sdq	%r13, %xmm7
	xorl	%r13d, %r13d
	divsd	.LC15(%rip), %xmm7
	.p2align 4,,10
	.p2align 3
.L237:
	movl	$160000, %ecx
	movaps	%xmm6, 192(%rsp)
	movq	$0, 208(%rsp)
.LEHB17:
	call	_Znwy
.LEHE17:
	movq	%rax, %r8
	xorl	%edx, %edx
	xorl	%ecx, %ecx
	movq	%rax, %rbx
.LEHB18:
	call	_ZSt16__do_uninit_copyIPK13OwnedThrowingPS0_ET0_T_S5_S4_
.LEHE18:
	movq	%rbx, %xmm2
	movl	$20000, %esi
	leaq	160000(%rbx), %rbp
	movddup	%xmm2, %xmm0
	movaps	%xmm0, 192(%rsp)
	movq	%rbp, 208(%rsp)
	jmp	.L254
	.p2align 4,,10
	.p2align 3
.L395:
	movq	%rax, (%rbx)
	addq	$8, %rbx
	subl	$1, %esi
	movq	%rbx, 200(%rsp)
	je	.L394
.L254:
	movl	$256, %ecx
.LEHB19:
	call	_Znay
.LEHE19:
	cmpq	%rbp, %rbx
	movq	%rax, 160(%rsp)
	jne	.L395
	movq	40(%rsp), %r8
	movq	%rbx, %rdx
	movq	%rdi, %rcx
.LEHB20:
	call	_ZNSt6vectorI13OwnedThrowingSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
.LEHE20:
	movq	160(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L370
	call	_ZdaPv
.L370:
	subl	$1, %esi
	movq	200(%rsp), %rbx
	movq	208(%rsp), %rbp
	jne	.L254
.L394:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movl	$256, %ecx
	movq	%rax, %rsi
.LEHB21:
	call	_Znay
.LEHE21:
	cmpq	%rbp, %rbx
	movq	%rax, 160(%rsp)
	je	.L255
	movq	%rax, (%rbx)
	addq	$8, %rbx
	movq	%rbx, 200(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	192(%rsp), %r14
	subq	%rsi, %rax
	addq	%rax, %r13
	cmpq	%rbx, %r14
	je	.L257
.L256:
	movq	%r14, %rsi
	.p2align 4,,10
	.p2align 3
.L262:
	movq	(%rsi), %rcx
	testq	%rcx, %rcx
	je	.L261
	call	_ZdaPv
.L261:
	addq	$8, %rsi
	cmpq	%rsi, %rbx
	jne	.L262
.L263:
	testq	%r14, %r14
	je	.L260
.L257:
	movq	%rbp, %rdx
	movq	%r14, %rcx
	subq	%r14, %rdx
	call	_ZdlPvy
.L260:
	subl	$1, %r12d
	jne	.L237
	movq	.refptr._ZSt4cout(%rip), %rcx
	leaq	.LC17(%rip), %rdx
	pxor	%xmm6, %xmm6
	cvtsi2sdq	%r13, %xmm6
	divsd	.LC16(%rip), %xmm6
.LEHB22:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	%xmm7, %xmm1
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIdEERSoT_
	leaq	.LC18(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	leaq	.LC19(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	%xmm6, %xmm1
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIdEERSoT_
	leaq	.LC20(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	%xmm6, %xmm1
	divsd	%xmm7, %xmm1
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIdEERSoT_
	leaq	.LC21(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	nop
.LEHE22:
	movaps	224(%rsp), %xmm6
	xorl	%eax, %eax
	movaps	240(%rsp), %xmm7
	addq	$264, %rsp
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
.L228:
	movq	40(%rsp), %r8
	movq	%rbx, %rdx
	movq	%rdi, %rcx
.LEHB23:
	call	_ZNSt6vectorI5OwnedSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
.LEHE23:
	movq	160(%rsp), %rcx
	movq	200(%rsp), %rbx
	testq	%rcx, %rcx
	je	.L368
	call	_ZdaPv
.L368:
	movq	208(%rsp), %rbp
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	192(%rsp), %r14
	subq	%rsi, %rax
	addq	%rax, %r13
	cmpq	%r14, %rbx
	jne	.L229
	jmp	.L236
	.p2align 4,,10
	.p2align 3
.L255:
	movq	40(%rsp), %r8
	movq	%rbx, %rdx
	movq	%rdi, %rcx
.LEHB24:
	call	_ZNSt6vectorI13OwnedThrowingSaIS0_EE17_M_realloc_insertIJS0_EEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
.LEHE24:
	movq	160(%rsp), %rcx
	movq	200(%rsp), %rbx
	testq	%rcx, %rcx
	je	.L371
	call	_ZdaPv
.L371:
	movq	208(%rsp), %rbp
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	192(%rsp), %r14
	subq	%rsi, %rax
	addq	%rax, %r13
	cmpq	%r14, %rbx
	jne	.L256
	jmp	.L263
.L390:
	movq	%rbx, %rcx
	jmp	.L216
.L171:
	movq	%rbx, %rdx
	andl	$1, %ebx
	pxor	%xmm0, %xmm0
	shrq	%rdx
	orq	%rbx, %rdx
	cvtsi2sdq	%rdx, %xmm0
	addsd	%xmm0, %xmm0
	jmp	.L172
.L386:
	movl	(%rsi), %edx
	movl	%edx, (%r15)
	movl	-4(%rsi,%rcx), %edx
	movl	%edx, -4(%r15,%rcx)
	movq	168(%rsp), %r8
	jmp	.L200
.L387:
	movzwl	-2(%rsi,%rcx), %edx
	movw	%dx, -2(%r15,%rcx)
	movq	168(%rsp), %r8
	jmp	.L200
.L278:
.L374:
	movq	160(%rsp), %rcx
	movq	%rax, %rbx
	testq	%rcx, %rcx
	je	.L240
	call	_ZdaPv
.L240:
	movq	192(%rsp), %rsi
	movq	200(%rsp), %rbp
	movq	%rsi, %rdi
.L243:
	cmpq	%rdi, %rbp
	je	.L379
	movq	(%rdi), %rcx
	testq	%rcx, %rcx
	je	.L244
	call	_ZdaPv
.L244:
	addq	$8, %rdi
	jmp	.L243
.L280:
	movq	40(%rsp), %rcx
	movq	%rax, %rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	%rbx, %rcx
.LEHB25:
	call	_Unwind_Resume
.LEHE25:
.L275:
.L376:
	movq	160(%rsp), %rcx
	movq	%rax, %rbx
	testq	%rcx, %rcx
	je	.L250
	call	_ZdaPv
	jmp	.L250
.L282:
	movq	%rax, %rcx
	call	__cxa_begin_catch
	movl	$160000, %edx
	movq	%rbx, %rcx
	call	_ZdlPvy
.LEHB26:
	call	__cxa_rethrow
.LEHE26:
.L283:
	movq	%rax, %rbx
	call	__cxa_end_catch
.L250:
	movq	192(%rsp), %rsi
	movq	200(%rsp), %rbp
	movq	%rsi, %rdi
.L268:
	cmpq	%rdi, %rbp
	je	.L379
	movq	(%rdi), %rcx
	testq	%rcx, %rcx
	je	.L269
	call	_ZdaPv
.L269:
	addq	$8, %rdi
	jmp	.L268
.L379:
	movq	208(%rsp), %rdx
	subq	%rsi, %rdx
	testq	%rsi, %rsi
	je	.L271
	movq	%rsi, %rcx
	call	_ZdlPvy
.L271:
	movq	%rbx, %rcx
.LEHB27:
	call	_Unwind_Resume
.LEHE27:
.L274:
	movq	%rax, %rbx
	jmp	.L250
.L279:
	jmp	.L374
.L277:
	movq	%rax, %rbx
	jmp	.L240
.L276:
	jmp	.L376
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA9423:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT9423-.LLSDATTD9423
.LLSDATTD9423:
	.byte	0x1
	.uleb128 .LLSDACSE9423-.LLSDACSB9423
.LLSDACSB9423:
	.uleb128 .LEHB11-.LFB9423
	.uleb128 .LEHE11-.LEHB11
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB12-.LFB9423
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L280-.LFB9423
	.uleb128 0
	.uleb128 .LEHB13-.LFB9423
	.uleb128 .LEHE13-.LEHB13
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB14-.LFB9423
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L277-.LFB9423
	.uleb128 0
	.uleb128 .LEHB15-.LFB9423
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L278-.LFB9423
	.uleb128 0
	.uleb128 .LEHB16-.LFB9423
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L277-.LFB9423
	.uleb128 0
	.uleb128 .LEHB17-.LFB9423
	.uleb128 .LEHE17-.LEHB17
	.uleb128 .L274-.LFB9423
	.uleb128 0
	.uleb128 .LEHB18-.LFB9423
	.uleb128 .LEHE18-.LEHB18
	.uleb128 .L282-.LFB9423
	.uleb128 0x1
	.uleb128 .LEHB19-.LFB9423
	.uleb128 .LEHE19-.LEHB19
	.uleb128 .L274-.LFB9423
	.uleb128 0
	.uleb128 .LEHB20-.LFB9423
	.uleb128 .LEHE20-.LEHB20
	.uleb128 .L275-.LFB9423
	.uleb128 0
	.uleb128 .LEHB21-.LFB9423
	.uleb128 .LEHE21-.LEHB21
	.uleb128 .L274-.LFB9423
	.uleb128 0
	.uleb128 .LEHB22-.LFB9423
	.uleb128 .LEHE22-.LEHB22
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB23-.LFB9423
	.uleb128 .LEHE23-.LEHB23
	.uleb128 .L279-.LFB9423
	.uleb128 0
	.uleb128 .LEHB24-.LFB9423
	.uleb128 .LEHE24-.LEHB24
	.uleb128 .L276-.LFB9423
	.uleb128 0
	.uleb128 .LEHB25-.LFB9423
	.uleb128 .LEHE25-.LEHB25
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB26-.LFB9423
	.uleb128 .LEHE26-.LEHB26
	.uleb128 .L283-.LFB9423
	.uleb128 0
	.uleb128 .LEHB27-.LFB9423
	.uleb128 .LEHE27-.LEHB27
	.uleb128 0
	.uleb128 0
.LLSDACSE9423:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT9423:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 4
__emutls_t.tl_var:
	.space 4
	.globl	__emutls_v.tl_var
	.data
	.align 32
__emutls_v.tl_var:
	.quad	4
	.quad	4
	.quad	0
	.quad	__emutls_t.tl_var
	.section .rdata,"dr"
	.align 8
.LC1:
	.long	0
	.long	1104006501
	.align 8
.LC4:
	.long	0
	.long	1072693248
	.align 8
.LC12:
	.long	0
	.long	1093816192
	.align 8
.LC13:
	.long	0
	.long	1088973312
	.align 8
.LC15:
	.long	0
	.long	1084178432
	.align 8
.LC16:
	.long	0
	.long	1080623104
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt28__throw_bad_array_new_lengthv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	__emutls_get_address;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_rethrow;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc;	.scl	2;	.type	32;	.endef
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_createERyy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
