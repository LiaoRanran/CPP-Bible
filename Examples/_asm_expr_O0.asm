	.file	"_asm_expr.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN5NaiveC1Ey,"x"
	.linkonce discard
	.align 2
	.globl	_ZN5NaiveC1Ey
	.def	_ZN5NaiveC1Ey;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN5NaiveC1Ey
_ZN5NaiveC1Ey:
.LFB42:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	movabs	rdx, 1152921504606846975
	cmp	rdx, rax
	jb	.L2
	sal	rax, 3
	jmp	.L4
.L2:
	call	__cxa_throw_bad_array_new_length
.L4:
	mov	rcx, rax
	call	_Znay
	mov	rdx, rax
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR 8[rax], rdx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN5NaiveD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN5NaiveD1Ev
	.def	_ZN5NaiveD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN5NaiveD1Ev
_ZN5NaiveD1Ev:
.LFB45:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	je	.L7
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rcx, rax
	call	_ZdaPv
.L7:
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK5NaiveplERKS_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK5NaiveplERKS_
	.def	_ZNK5NaiveplERKS_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK5NaiveplERKS_
_ZNK5NaiveplERKS_:
.LFB46:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	rax, QWORD PTR 24[rbp]
	mov	rdx, QWORD PTR 8[rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN5NaiveC1Ey
	mov	QWORD PTR -8[rbp], 0
	jmp	.L9
.L10:
	mov	rax, QWORD PTR 24[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR -8[rbp]
	sal	rax, 3
	add	rax, rdx
	movsd	xmm1, QWORD PTR [rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR -8[rbp]
	sal	rax, 3
	add	rax, rdx
	movsd	xmm0, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR -8[rbp]
	sal	rax, 3
	add	rax, rdx
	addsd	xmm0, xmm1
	movsd	QWORD PTR [rax], xmm0
	add	QWORD PTR -8[rbp], 1
.L9:
	mov	rax, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 8[rax]
	cmp	QWORD PTR -8[rbp], rax
	jb	.L10
	nop
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4FastC1Ey,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4FastC1Ey
	.def	_ZN4FastC1Ey;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4FastC1Ey
_ZN4FastC1Ey:
.LFB51:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	movabs	rdx, 1152921504606846975
	cmp	rdx, rax
	jb	.L13
	sal	rax, 3
	jmp	.L15
.L13:
	call	__cxa_throw_bad_array_new_length
.L15:
	mov	rcx, rax
	call	_Znay
	mov	rdx, rax
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR 8[rax], rdx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4FastD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4FastD1Ev
	.def	_ZN4FastD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4FastD1Ev
_ZN4FastD1Ev:
.LFB54:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	je	.L18
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rcx, rax
	call	_ZdaPv
.L18:
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK4FastixEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK4FastixEy
	.def	_ZNK4FastixEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK4FastixEy
_ZNK4FastixEy:
.LFB55:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 24[rbp]
	sal	rax, 3
	add	rax, rdx
	movsd	xmm0, QWORD PTR [rax]
	movq	rax, xmm0
	movq	xmm0, rax
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK4Fast4sizeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK4Fast4sizeEv
	.def	_ZNK4Fast4sizeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK4Fast4sizeEv
_ZNK4Fast4sizeEv:
.LFB56:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z9use_naivei
	.def	_Z9use_naivei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9use_naivei
_Z9use_naivei:
.LFB62:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 136
	.seh_stackalloc	136
	lea	rbp, 128[rsp]
	.seh_setframe	rbp, 128
	.seh_endprologue
	mov	DWORD PTR 32[rbp], ecx
	mov	eax, DWORD PTR 32[rbp]
	movsx	rdx, eax
	lea	rax, -48[rbp]
	mov	rcx, rax
.LEHB0:
	call	_ZN5NaiveC1Ey
.LEHE0:
	mov	eax, DWORD PTR 32[rbp]
	movsx	rdx, eax
	lea	rax, -64[rbp]
	mov	rcx, rax
.LEHB1:
	call	_ZN5NaiveC1Ey
.LEHE1:
	mov	eax, DWORD PTR 32[rbp]
	movsx	rdx, eax
	lea	rax, -80[rbp]
	mov	rcx, rax
.LEHB2:
	call	_ZN5NaiveC1Ey
.LEHE2:
	mov	DWORD PTR -4[rbp], 0
	jmp	.L24
.L25:
	mov	rdx, QWORD PTR -48[rbp]
	mov	eax, DWORD PTR -4[rbp]
	cdqe
	sal	rax, 3
	add	rax, rdx
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, DWORD PTR -4[rbp]
	movsd	QWORD PTR [rax], xmm0
	mov	eax, DWORD PTR -4[rbp]
	lea	ecx, 1[rax]
	mov	rdx, QWORD PTR -64[rbp]
	mov	eax, DWORD PTR -4[rbp]
	cdqe
	sal	rax, 3
	add	rax, rdx
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, ecx
	movsd	QWORD PTR [rax], xmm0
	mov	eax, DWORD PTR -4[rbp]
	lea	ecx, 2[rax]
	mov	rdx, QWORD PTR -80[rbp]
	mov	eax, DWORD PTR -4[rbp]
	cdqe
	sal	rax, 3
	add	rax, rdx
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, ecx
	movsd	QWORD PTR [rax], xmm0
	add	DWORD PTR -4[rbp], 1
.L24:
	mov	eax, DWORD PTR -4[rbp]
	cmp	eax, DWORD PTR 32[rbp]
	jl	.L25
	lea	rax, -32[rbp]
	lea	rcx, -64[rbp]
	lea	rdx, -48[rbp]
	mov	r8, rcx
	mov	rcx, rax
.LEHB3:
	call	_ZNK5NaiveplERKS_
.LEHE3:
	lea	rax, -96[rbp]
	lea	rcx, -80[rbp]
	lea	rdx, -32[rbp]
	mov	r8, rcx
	mov	rcx, rax
.LEHB4:
	call	_ZNK5NaiveplERKS_
.LEHE4:
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZN5NaiveD1Ev
	mov	rdx, QWORD PTR -96[rbp]
	mov	eax, DWORD PTR 32[rbp]
	cdqe
	sal	rax, 3
	sub	rax, 8
	add	rax, rdx
	movsd	xmm0, QWORD PTR [rax]
	cvttsd2si	ebx, xmm0
	lea	rax, -96[rbp]
	mov	rcx, rax
	call	_ZN5NaiveD1Ev
	lea	rax, -80[rbp]
	mov	rcx, rax
	call	_ZN5NaiveD1Ev
	lea	rax, -64[rbp]
	mov	rcx, rax
	call	_ZN5NaiveD1Ev
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZN5NaiveD1Ev
	mov	eax, ebx
	jmp	.L35
.L34:
	mov	rbx, rax
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZN5NaiveD1Ev
	jmp	.L28
.L33:
	mov	rbx, rax
.L28:
	lea	rax, -80[rbp]
	mov	rcx, rax
	call	_ZN5NaiveD1Ev
	jmp	.L29
.L32:
	mov	rbx, rax
.L29:
	lea	rax, -64[rbp]
	mov	rcx, rax
	call	_ZN5NaiveD1Ev
	jmp	.L30
.L31:
	mov	rbx, rax
.L30:
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZN5NaiveD1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB5:
	call	_Unwind_Resume
.LEHE5:
.L35:
	add	rsp, 136
	pop	rbx
	pop	rbp
	ret
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA62:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE62-.LLSDACSB62
.LLSDACSB62:
	.uleb128 .LEHB0-.LFB62
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB62
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L31-.LFB62
	.uleb128 0
	.uleb128 .LEHB2-.LFB62
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L32-.LFB62
	.uleb128 0
	.uleb128 .LEHB3-.LFB62
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L33-.LFB62
	.uleb128 0
	.uleb128 .LEHB4-.LFB62
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L34-.LFB62
	.uleb128 0
	.uleb128 .LEHB5-.LFB62
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSE62:
	.text
	.seh_endproc
	.globl	_Z8use_expri
	.def	_Z8use_expri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8use_expri
_Z8use_expri:
.LFB63:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 152
	.seh_stackalloc	152
	lea	rbp, 144[rsp]
	.seh_setframe	rbp, 144
	.seh_endprologue
	mov	DWORD PTR 32[rbp], ecx
	mov	eax, DWORD PTR 32[rbp]
	movsx	rdx, eax
	lea	rax, -64[rbp]
	mov	rcx, rax
.LEHB6:
	call	_ZN4FastC1Ey
.LEHE6:
	mov	eax, DWORD PTR 32[rbp]
	movsx	rdx, eax
	lea	rax, -80[rbp]
	mov	rcx, rax
.LEHB7:
	call	_ZN4FastC1Ey
.LEHE7:
	mov	eax, DWORD PTR 32[rbp]
	movsx	rdx, eax
	lea	rax, -96[rbp]
	mov	rcx, rax
.LEHB8:
	call	_ZN4FastC1Ey
.LEHE8:
	mov	DWORD PTR -4[rbp], 0
	jmp	.L37
.L38:
	mov	rdx, QWORD PTR -64[rbp]
	mov	eax, DWORD PTR -4[rbp]
	cdqe
	sal	rax, 3
	add	rax, rdx
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, DWORD PTR -4[rbp]
	movsd	QWORD PTR [rax], xmm0
	mov	eax, DWORD PTR -4[rbp]
	lea	ecx, 1[rax]
	mov	rdx, QWORD PTR -80[rbp]
	mov	eax, DWORD PTR -4[rbp]
	cdqe
	sal	rax, 3
	add	rax, rdx
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, ecx
	movsd	QWORD PTR [rax], xmm0
	mov	eax, DWORD PTR -4[rbp]
	lea	ecx, 2[rax]
	mov	rdx, QWORD PTR -96[rbp]
	mov	eax, DWORD PTR -4[rbp]
	cdqe
	sal	rax, 3
	add	rax, rdx
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, ecx
	movsd	QWORD PTR [rax], xmm0
	add	DWORD PTR -4[rbp], 1
.L37:
	mov	eax, DWORD PTR -4[rbp]
	cmp	eax, DWORD PTR 32[rbp]
	jl	.L38
	mov	eax, DWORD PTR 32[rbp]
	movsx	rdx, eax
	lea	rax, -112[rbp]
	mov	rcx, rax
.LEHB9:
	call	_ZN4FastC1Ey
.LEHE9:
	lea	rax, -32[rbp]
	lea	rcx, -80[rbp]
	lea	rdx, -64[rbp]
	mov	r8, rcx
	mov	rcx, rax
.LEHB10:
	call	_ZplI4FastS0_E3SumIT_T0_ERK4ExprIS2_ERKS5_IS3_E
	lea	rax, -48[rbp]
	lea	rcx, -96[rbp]
	lea	rdx, -32[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZplI3SumI4FastS1_ES1_ES0_IT_T0_ERK4ExprIS3_ERKS6_IS4_E
	lea	rdx, -48[rbp]
	lea	rax, -112[rbp]
	mov	rcx, rax
	call	_ZN4FastaSI3SumIS1_IS_S_ES_EEERS_RK4ExprIT_E
.LEHE10:
	mov	rdx, QWORD PTR -112[rbp]
	mov	eax, DWORD PTR 32[rbp]
	cdqe
	sal	rax, 3
	sub	rax, 8
	add	rax, rdx
	movsd	xmm0, QWORD PTR [rax]
	cvttsd2si	ebx, xmm0
	lea	rax, -112[rbp]
	mov	rcx, rax
	call	_ZN4FastD1Ev
	lea	rax, -96[rbp]
	mov	rcx, rax
	call	_ZN4FastD1Ev
	lea	rax, -80[rbp]
	mov	rcx, rax
	call	_ZN4FastD1Ev
	lea	rax, -64[rbp]
	mov	rcx, rax
	call	_ZN4FastD1Ev
	mov	eax, ebx
	jmp	.L48
.L47:
	mov	rbx, rax
	lea	rax, -112[rbp]
	mov	rcx, rax
	call	_ZN4FastD1Ev
	jmp	.L41
.L46:
	mov	rbx, rax
.L41:
	lea	rax, -96[rbp]
	mov	rcx, rax
	call	_ZN4FastD1Ev
	jmp	.L42
.L45:
	mov	rbx, rax
.L42:
	lea	rax, -80[rbp]
	mov	rcx, rax
	call	_ZN4FastD1Ev
	jmp	.L43
.L44:
	mov	rbx, rax
.L43:
	lea	rax, -64[rbp]
	mov	rcx, rax
	call	_ZN4FastD1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB11:
	call	_Unwind_Resume
.LEHE11:
.L48:
	add	rsp, 152
	pop	rbx
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA63:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE63-.LLSDACSB63
.LLSDACSB63:
	.uleb128 .LEHB6-.LFB63
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB7-.LFB63
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L44-.LFB63
	.uleb128 0
	.uleb128 .LEHB8-.LFB63
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L45-.LFB63
	.uleb128 0
	.uleb128 .LEHB9-.LFB63
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L46-.LFB63
	.uleb128 0
	.uleb128 .LEHB10-.LFB63
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L47-.LFB63
	.uleb128 0
	.uleb128 .LEHB11-.LFB63
	.uleb128 .LEHE11-.LEHB11
	.uleb128 0
	.uleb128 0
.LLSDACSE63:
	.text
	.seh_endproc
	.section	.text$_ZplI4FastS0_E3SumIT_T0_ERK4ExprIS2_ERKS5_IS3_E,"x"
	.linkonce discard
	.globl	_ZplI4FastS0_E3SumIT_T0_ERK4ExprIS2_ERKS5_IS3_E
	.def	_ZplI4FastS0_E3SumIT_T0_ERK4ExprIS2_ERKS5_IS3_E;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZplI4FastS0_E3SumIT_T0_ERK4ExprIS2_ERKS5_IS3_E
_ZplI4FastS0_E3SumIT_T0_ERK4ExprIS2_ERKS5_IS3_E:
.LFB64:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	rcx, QWORD PTR 32[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZN3SumI4FastS0_EC1ERKS0_S3_
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZplI3SumI4FastS1_ES1_ES0_IT_T0_ERK4ExprIS3_ERKS6_IS4_E,"x"
	.linkonce discard
	.globl	_ZplI3SumI4FastS1_ES1_ES0_IT_T0_ERK4ExprIS3_ERKS6_IS4_E
	.def	_ZplI3SumI4FastS1_ES1_ES0_IT_T0_ERK4ExprIS3_ERKS6_IS4_E;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZplI3SumI4FastS1_ES1_ES0_IT_T0_ERK4ExprIS3_ERKS6_IS4_E
_ZplI3SumI4FastS1_ES1_ES0_IT_T0_ERK4ExprIS3_ERKS6_IS4_E:
.LFB65:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	rcx, QWORD PTR 32[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZN3SumIS_I4FastS0_ES0_EC1ERKS1_RKS0_
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4FastaSI3SumIS1_IS_S_ES_EEERS_RK4ExprIT_E,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4FastaSI3SumIS1_IS_S_ES_EEERS_RK4ExprIT_E
	.def	_ZN4FastaSI3SumIS1_IS_S_ES_EEERS_RK4ExprIT_E;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4FastaSI3SumIS1_IS_S_ES_EEERS_RK4ExprIT_E
_ZN4FastaSI3SumIS1_IS_S_ES_EEERS_RK4ExprIT_E:
.LFB66:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	QWORD PTR 40[rbp], rdx
	mov	QWORD PTR -8[rbp], 0
	jmp	.L54
.L55:
	mov	rax, QWORD PTR 32[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR -8[rbp]
	sal	rax, 3
	lea	rbx, [rdx+rax]
	mov	rdx, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR 40[rbp]
	mov	rcx, rax
	call	_ZNK4ExprI3SumIS0_I4FastS1_ES1_EEixEy
	movq	rax, xmm0
	mov	QWORD PTR [rbx], rax
	add	QWORD PTR -8[rbp], 1
.L54:
	mov	rax, QWORD PTR 40[rbp]
	mov	rcx, rax
	call	_ZNK4ExprI3SumIS0_I4FastS1_ES1_EE4sizeEv
	cmp	QWORD PTR -8[rbp], rax
	setb	al
	test	al, al
	jne	.L55
	mov	rax, QWORD PTR 32[rbp]
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3SumI4FastS0_EC1ERKS0_S3_,"x"
	.linkonce discard
	.align 2
	.globl	_ZN3SumI4FastS0_EC1ERKS0_S3_
	.def	_ZN3SumI4FastS0_EC1ERKS0_S3_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3SumI4FastS0_EC1ERKS0_S3_
_ZN3SumI4FastS0_EC1ERKS0_S3_:
.LFB69:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 32[rbp]
	mov	QWORD PTR 8[rax], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3SumIS_I4FastS0_ES0_EC1ERKS1_RKS0_,"x"
	.linkonce discard
	.align 2
	.globl	_ZN3SumIS_I4FastS0_ES0_EC1ERKS1_RKS0_
	.def	_ZN3SumIS_I4FastS0_ES0_EC1ERKS1_RKS0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3SumIS_I4FastS0_ES0_EC1ERKS1_RKS0_
_ZN3SumIS_I4FastS0_ES0_EC1ERKS1_RKS0_:
.LFB72:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 32[rbp]
	mov	QWORD PTR 8[rax], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK4ExprI3SumIS0_I4FastS1_ES1_EE4sizeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK4ExprI3SumIS0_I4FastS1_ES1_EE4sizeEv
	.def	_ZNK4ExprI3SumIS0_I4FastS1_ES1_EE4sizeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK4ExprI3SumIS0_I4FastS1_ES1_EE4sizeEv
_ZNK4ExprI3SumIS0_I4FastS1_ES1_EE4sizeEv:
.LFB73:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNK3SumIS_I4FastS0_ES0_E4sizeEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK4ExprI3SumIS0_I4FastS1_ES1_EEixEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK4ExprI3SumIS0_I4FastS1_ES1_EEixEy
	.def	_ZNK4ExprI3SumIS0_I4FastS1_ES1_EEixEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK4ExprI3SumIS0_I4FastS1_ES1_EEixEy
_ZNK4ExprI3SumIS0_I4FastS1_ES1_EEixEy:
.LFB74:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNK3SumIS_I4FastS0_ES0_EixEy
	movq	rax, xmm0
	movq	xmm0, rax
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK3SumIS_I4FastS0_ES0_E4sizeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK3SumIS_I4FastS0_ES0_E4sizeEv
	.def	_ZNK3SumIS_I4FastS0_ES0_E4sizeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK3SumIS_I4FastS0_ES0_E4sizeEv
_ZNK3SumIS_I4FastS0_ES0_E4sizeEv:
.LFB75:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rcx, rax
	call	_ZNK3SumI4FastS0_E4sizeEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK3SumIS_I4FastS0_ES0_EixEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK3SumIS_I4FastS0_ES0_EixEy
	.def	_ZNK3SumIS_I4FastS0_ES0_EixEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK3SumIS_I4FastS0_ES0_EixEy
_ZNK3SumIS_I4FastS0_ES0_EixEy:
.LFB76:
	push	rbp
	.seh_pushreg	rbp
	sub	rsp, 48
	.seh_stackalloc	48
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	movaps	XMMWORD PTR 0[rbp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	QWORD PTR 40[rbp], rdx
	mov	rax, QWORD PTR 32[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR 40[rbp]
	mov	rcx, rax
	call	_ZNK3SumI4FastS0_EixEy
	movapd	xmm6, xmm0
	mov	rax, QWORD PTR 32[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	rdx, QWORD PTR 40[rbp]
	mov	rcx, rax
	call	_ZNK4FastixEy
	addsd	xmm0, xmm6
	movq	rax, xmm0
	movq	xmm0, rax
	movaps	xmm6, XMMWORD PTR 0[rbp]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK3SumI4FastS0_E4sizeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK3SumI4FastS0_E4sizeEv
	.def	_ZNK3SumI4FastS0_E4sizeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK3SumI4FastS0_E4sizeEv
_ZNK3SumI4FastS0_E4sizeEv:
.LFB77:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rcx, rax
	call	_ZNK4Fast4sizeEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK3SumI4FastS0_EixEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK3SumI4FastS0_EixEy
	.def	_ZNK3SumI4FastS0_EixEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK3SumI4FastS0_EixEy
_ZNK3SumI4FastS0_EixEy:
.LFB78:
	push	rbp
	.seh_pushreg	rbp
	sub	rsp, 48
	.seh_stackalloc	48
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	movaps	XMMWORD PTR 0[rbp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	QWORD PTR 40[rbp], rdx
	mov	rax, QWORD PTR 32[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR 40[rbp]
	mov	rcx, rax
	call	_ZNK4FastixEy
	movapd	xmm6, xmm0
	mov	rax, QWORD PTR 32[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	rdx, QWORD PTR 40[rbp]
	mov	rcx, rax
	call	_ZNK4FastixEy
	addsd	xmm0, xmm6
	movq	rax, xmm0
	movq	xmm0, rax
	movaps	xmm6, XMMWORD PTR 0[rbp]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__cxa_throw_bad_array_new_length;	.scl	2;	.type	32;	.endef
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
