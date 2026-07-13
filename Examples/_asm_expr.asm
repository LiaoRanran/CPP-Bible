	.file	"_asm_expr.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z9use_naivei
	.def	_Z9use_naivei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9use_naivei
_Z9use_naivei:
.LFB64:
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
	movabs	rax, 1152921504606846975
	movsx	r14, ecx
	cmp	rax, r14
	jb	.L2
	lea	r13, 0[0+r14*8]
	mov	rcx, r13
.LEHB0:
	call	_Znay
.LEHE0:
	mov	rcx, r13
	mov	rsi, rax
.LEHB1:
	call	_Znay
.LEHE1:
	mov	rcx, r13
	mov	rdi, rax
.LEHB2:
	call	_Znay
.LEHE2:
	test	r14d, r14d
	mov	rbp, rax
	je	.L4
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L5:
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, eax
	lea	edx, 1[rax]
	movsd	QWORD PTR [rsi+rax*8], xmm0
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, edx
	lea	edx, 2[rax]
	movsd	QWORD PTR [rdi+rax*8], xmm0
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, edx
	movsd	QWORD PTR 0[rbp+rax*8], xmm0
	add	rax, 1
	cmp	r14, rax
	jne	.L5
	mov	rcx, r13
.LEHB3:
	call	_Znay
.LEHE3:
	mov	r12, rax
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L6:
	movsd	xmm0, QWORD PTR [rsi+rax*8]
	mov	rbx, rax
	addsd	xmm0, QWORD PTR [rdi+rax*8]
	movsd	QWORD PTR [r12+rax*8], xmm0
	lea	rax, 1[rax]
	cmp	r14, rax
	jne	.L6
	mov	rcx, r13
.LEHB4:
	call	_Znay
.LEHE4:
	mov	r14, rax
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L10:
	movsd	xmm0, QWORD PTR [r12+rdx*8]
	mov	rcx, rdx
	addsd	xmm0, QWORD PTR 0[rbp+rdx*8]
	movsd	QWORD PTR [r14+rdx*8], xmm0
	add	rdx, 1
	cmp	rbx, rcx
	jne	.L10
.L9:
	mov	rcx, r12
	call	_ZdaPv
	mov	rcx, r14
	cvttsd2si	ebx, QWORD PTR -8[r14+r13]
	call	_ZdaPv
	mov	rcx, rbp
	call	_ZdaPv
	mov	rcx, rdi
	call	_ZdaPv
	mov	rcx, rsi
	call	_ZdaPv
	mov	eax, ebx
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
.L4:
	xor	ecx, ecx
.LEHB5:
	call	_Znay
.LEHE5:
	xor	ecx, ecx
	mov	r12, rax
.LEHB6:
	call	_Znay
.LEHE6:
	mov	r14, rax
	jmp	.L9
.L18:
	mov	rbx, rax
.L12:
	mov	rcx, rbp
	call	_ZdaPv
.L13:
	mov	rcx, rdi
	call	_ZdaPv
.L14:
	mov	rcx, rsi
	call	_ZdaPv
	mov	rcx, rbx
.LEHB7:
	call	_Unwind_Resume
.L17:
	mov	rbx, rax
	jmp	.L13
.L2:
	call	__cxa_throw_bad_array_new_length
.LEHE7:
.L16:
	mov	rbx, rax
	jmp	.L14
.L19:
	mov	rcx, r12
	mov	rbx, rax
	call	_ZdaPv
	jmp	.L12
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA64:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE64-.LLSDACSB64
.LLSDACSB64:
	.uleb128 .LEHB0-.LFB64
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB64
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L16-.LFB64
	.uleb128 0
	.uleb128 .LEHB2-.LFB64
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L17-.LFB64
	.uleb128 0
	.uleb128 .LEHB3-.LFB64
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L18-.LFB64
	.uleb128 0
	.uleb128 .LEHB4-.LFB64
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L19-.LFB64
	.uleb128 0
	.uleb128 .LEHB5-.LFB64
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L18-.LFB64
	.uleb128 0
	.uleb128 .LEHB6-.LFB64
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L19-.LFB64
	.uleb128 0
	.uleb128 .LEHB7-.LFB64
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSE64:
	.text
	.seh_endproc
	.p2align 4
	.globl	_Z8use_expri
	.def	_Z8use_expri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8use_expri
_Z8use_expri:
.LFB65:
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
	movabs	rax, 1152921504606846975
	movsx	rbp, ecx
	cmp	rax, rbp
	jb	.L29
	lea	r12, 0[0+rbp*8]
	mov	rcx, r12
.LEHB8:
	call	_Znay
.LEHE8:
	mov	rcx, r12
	mov	rbx, rax
.LEHB9:
	call	_Znay
.LEHE9:
	mov	rcx, r12
	mov	rsi, rax
.LEHB10:
	call	_Znay
.LEHE10:
	test	ebp, ebp
	mov	rdi, rax
	je	.L31
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L32:
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, eax
	lea	edx, 1[rax]
	movsd	QWORD PTR [rbx+rax*8], xmm0
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, edx
	lea	edx, 2[rax]
	movsd	QWORD PTR [rsi+rax*8], xmm0
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, edx
	movsd	QWORD PTR [rdi+rax*8], xmm0
	add	rax, 1
	cmp	rbp, rax
	jne	.L32
	mov	rcx, r12
.LEHB11:
	call	_Znay
	mov	rcx, rax
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L33:
	movsd	xmm0, QWORD PTR [rbx+rdx*8]
	addsd	xmm0, QWORD PTR [rsi+rdx*8]
	addsd	xmm0, QWORD PTR [rdi+rdx*8]
	movsd	QWORD PTR [rcx+rdx*8], xmm0
	add	rdx, 1
	cmp	rbp, rdx
	jne	.L33
.L34:
	cvttsd2si	ebp, QWORD PTR -8[rcx+r12]
	call	_ZdaPv
	mov	rcx, rdi
	call	_ZdaPv
	mov	rcx, rsi
	call	_ZdaPv
	mov	rcx, rbx
	call	_ZdaPv
	mov	eax, ebp
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
.L31:
	xor	ecx, ecx
	call	_Znay
.LEHE11:
	mov	rcx, rax
	jmp	.L34
.L41:
	mov	rbp, rax
	mov	rcx, rdi
	call	_ZdaPv
	mov	rdi, rbp
.L36:
	mov	rcx, rsi
	call	_ZdaPv
.L37:
	mov	rcx, rbx
	call	_ZdaPv
	mov	rcx, rdi
.LEHB12:
	call	_Unwind_Resume
.L40:
	mov	rdi, rax
	jmp	.L36
.L39:
	mov	rdi, rax
	jmp	.L37
.L29:
	call	__cxa_throw_bad_array_new_length
	nop
.LEHE12:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA65:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE65-.LLSDACSB65
.LLSDACSB65:
	.uleb128 .LEHB8-.LFB65
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB9-.LFB65
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L39-.LFB65
	.uleb128 0
	.uleb128 .LEHB10-.LFB65
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L40-.LFB65
	.uleb128 0
	.uleb128 .LEHB11-.LFB65
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L41-.LFB65
	.uleb128 0
	.uleb128 .LEHB12-.LFB65
	.uleb128 .LEHE12-.LEHB12
	.uleb128 0
	.uleb128 0
.LLSDACSE65:
	.text
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw_bad_array_new_length;	.scl	2;	.type	32;	.endef
