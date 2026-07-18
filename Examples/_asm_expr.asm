	.file	"_asm_expr.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.unlikely,"x"
.LCOLDB4:
	.text
.LHOTB4:
	.p2align 4
	.globl	_Z9use_naivei
	.def	_Z9use_naivei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9use_naivei
_Z9use_naivei:
.LFB66:
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
	sub	rsp, 48
	.seh_stackalloc	48
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	movsxd	r14, ecx
	mov	rax, r14
	mov	rbx, r14
	shr	rax, 60
	jne	.L2
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
	mov	rbp, rax
	test	r14d, r14d
	je	.L4
	lea	eax, -1[r14]
	cmp	eax, 2
	jbe	.L18
	mov	ecx, 2
	mov	edx, r14d
	pcmpeqd	xmm5, xmm5
	xor	eax, eax
	movd	xmm6, ecx
	shr	edx, 2
	mov	ecx, 4
	movdqa	xmm2, XMMWORD PTR .LC0[rip]
	movd	xmm4, ecx
	sal	rdx, 5
	psrld	xmm5, 31
	pshufd	xmm6, xmm6, 0
	pshufd	xmm4, xmm4, 0
	.p2align 4
	.p2align 3
.L6:
	movdqa	xmm1, xmm2
	cvtdq2pd	xmm3, xmm2
	movdqa	xmm0, xmm2
	movups	XMMWORD PTR [rsi+rax], xmm3
	paddd	xmm1, xmm5
	pshufd	xmm3, xmm2, 238
	paddd	xmm0, xmm6
	cvtdq2pd	xmm3, xmm3
	movups	XMMWORD PTR 16[rsi+rax], xmm3
	cvtdq2pd	xmm3, xmm1
	pshufd	xmm1, xmm1, 238
	cvtdq2pd	xmm1, xmm1
	movups	XMMWORD PTR 16[rdi+rax], xmm1
	cvtdq2pd	xmm1, xmm0
	paddd	xmm2, xmm4
	pshufd	xmm0, xmm0, 238
	movups	XMMWORD PTR [rdi+rax], xmm3
	movups	XMMWORD PTR 0[rbp+rax], xmm1
	cvtdq2pd	xmm0, xmm0
	movups	XMMWORD PTR 16[rbp+rax], xmm0
	add	rax, 32
	cmp	rdx, rax
	jne	.L6
	test	bl, 3
	je	.L7
	mov	eax, ebx
	and	eax, -4
.L5:
	cdqe
.L8:
	pxor	xmm0, xmm0
	lea	edx, 1[rax]
	cvtsi2sd	xmm0, eax
	movsd	QWORD PTR [rsi+rax*8], xmm0
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, edx
	lea	edx, 2[rax]
	movsd	QWORD PTR [rdi+rax*8], xmm0
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, edx
	movsd	QWORD PTR 0[rbp+rax*8], xmm0
	add	rax, 1
	cmp	ebx, eax
	jg	.L8
.L7:
	mov	rcx, r13
.LEHB3:
	call	_Znay
.LEHE3:
	mov	r12, rax
	xor	ebx, ebx
	.p2align 5
	.p2align 4
	.p2align 3
.L9:
	movsd	xmm0, QWORD PTR [rsi+rbx*8]
	addsd	xmm0, QWORD PTR [rdi+rbx*8]
	movsd	QWORD PTR [r12+rbx*8], xmm0
	add	rbx, 1
	cmp	r14, rbx
	jne	.L9
	mov	rcx, r13
.LEHB4:
	call	_Znay
.LEHE4:
	mov	r13, rax
	xor	edx, edx
	.p2align 5
	.p2align 4
	.p2align 3
.L13:
	movsd	xmm0, QWORD PTR [r12+rdx*8]
	addsd	xmm0, QWORD PTR 0[rbp+rdx*8]
	movsd	QWORD PTR 0[r13+rdx*8], xmm0
	add	rdx, 1
	cmp	rbx, rdx
	jne	.L13
.L12:
	mov	rcx, r12
	call	_ZdaPv
	mov	rcx, r13
	cvttsd2si	ebx, QWORD PTR -8[r13+r14*8]
	call	_ZdaPv
	mov	rcx, rbp
	call	_ZdaPv
	mov	rcx, rdi
	call	_ZdaPv
	mov	rcx, rsi
	call	_ZdaPv
	nop
	movaps	xmm6, XMMWORD PTR 32[rsp]
	mov	eax, ebx
	add	rsp, 48
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
	mov	r13, rax
	jmp	.L12
.L18:
	xor	eax, eax
	jmp	.L5
.L22:
	mov	rbx, rax
	jmp	.L15
.L21:
	mov	rbx, rax
	jmp	.L16
.L20:
	mov	rbx, rax
	jmp	.L17
.L23:
	mov	rbx, rax
	jmp	.L14
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA66:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE66-.LLSDACSB66
.LLSDACSB66:
	.uleb128 .LEHB0-.LFB66
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB66
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L20-.LFB66
	.uleb128 0
	.uleb128 .LEHB2-.LFB66
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L21-.LFB66
	.uleb128 0
	.uleb128 .LEHB3-.LFB66
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L22-.LFB66
	.uleb128 0
	.uleb128 .LEHB4-.LFB66
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L23-.LFB66
	.uleb128 0
	.uleb128 .LEHB5-.LFB66
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L22-.LFB66
	.uleb128 0
	.uleb128 .LEHB6-.LFB66
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L23-.LFB66
	.uleb128 0
.LLSDACSE66:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z9use_naivei.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z9use_naivei.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_savereg	rbp, 72
	.seh_savexmm	xmm6, 32
	.seh_savereg	r12, 80
	.seh_savereg	r13, 88
	.seh_savereg	r14, 96
	.seh_endprologue
_Z9use_naivei.cold:
.L2:
.LEHB7:
	call	__cxa_throw_bad_array_new_length
.L14:
	mov	rcx, r12
	call	_ZdaPv
.L15:
	mov	rcx, rbp
	call	_ZdaPv
.L16:
	mov	rcx, rdi
	call	_ZdaPv
.L17:
	mov	rcx, rsi
	call	_ZdaPv
	mov	rcx, rbx
	call	_Unwind_Resume
	nop
.LEHE7:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC66:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC66-.LLSDACSBC66
.LLSDACSBC66:
	.uleb128 .LEHB7-.LCOLDB4
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSEC66:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE4:
	.text
.LHOTE4:
	.section	.text.unlikely,"x"
.LCOLDB5:
	.text
.LHOTB5:
	.p2align 4
	.globl	_Z8use_expri
	.def	_Z8use_expri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8use_expri
_Z8use_expri:
.LFB67:
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
	movsxd	rbp, ecx
	mov	rax, rbp
	mov	r13, rbp
	shr	rax, 60
	jne	.L37
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
	mov	rdi, rax
	test	ebp, ebp
	je	.L67
	lea	eax, -1[rbp]
	cmp	eax, 2
	jbe	.L53
	mov	ecx, 2
	mov	edx, ebp
	pcmpeqd	xmm5, xmm5
	xor	eax, eax
	movd	xmm6, ecx
	shr	edx, 2
	mov	ecx, 4
	movdqa	xmm2, XMMWORD PTR .LC0[rip]
	movd	xmm4, ecx
	sal	rdx, 5
	psrld	xmm5, 31
	pshufd	xmm6, xmm6, 0
	pshufd	xmm4, xmm4, 0
	.p2align 4
	.p2align 3
.L42:
	movdqa	xmm1, xmm2
	cvtdq2pd	xmm3, xmm2
	movdqa	xmm0, xmm2
	movups	XMMWORD PTR [rbx+rax], xmm3
	paddd	xmm1, xmm5
	pshufd	xmm3, xmm2, 238
	paddd	xmm0, xmm6
	cvtdq2pd	xmm3, xmm3
	movups	XMMWORD PTR 16[rbx+rax], xmm3
	cvtdq2pd	xmm3, xmm1
	pshufd	xmm1, xmm1, 238
	cvtdq2pd	xmm1, xmm1
	movups	XMMWORD PTR 16[rsi+rax], xmm1
	cvtdq2pd	xmm1, xmm0
	paddd	xmm2, xmm4
	pshufd	xmm0, xmm0, 238
	movups	XMMWORD PTR [rsi+rax], xmm3
	movups	XMMWORD PTR [rdi+rax], xmm1
	cvtdq2pd	xmm0, xmm0
	movups	XMMWORD PTR 16[rdi+rax], xmm0
	add	rax, 32
	cmp	rax, rdx
	jne	.L42
	mov	eax, r13d
	and	eax, -4
	test	r13b, 3
	je	.L68
.L41:
	cdqe
.L44:
	pxor	xmm0, xmm0
	lea	edx, 1[rax]
	cvtsi2sd	xmm0, eax
	movsd	QWORD PTR [rbx+rax*8], xmm0
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, edx
	lea	edx, 2[rax]
	movsd	QWORD PTR [rsi+rax*8], xmm0
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, edx
	movsd	QWORD PTR [rdi+rax*8], xmm0
	add	rax, 1
	cmp	r13d, eax
	jg	.L44
	mov	rcx, r12
.LEHB11:
	call	_Znay
	mov	rcx, rax
	cmp	r13d, 1
	je	.L54
.L46:
	mov	rax, rbp
	xor	edx, edx
	shr	rax
	sal	rax, 4
	.p2align 6
	.p2align 4
	.p2align 3
.L48:
	movupd	xmm0, XMMWORD PTR [rbx+rdx]
	movupd	xmm4, XMMWORD PTR [rsi+rdx]
	movupd	xmm5, XMMWORD PTR [rdi+rdx]
	addpd	xmm0, xmm4
	addpd	xmm0, xmm5
	movups	XMMWORD PTR [rcx+rdx], xmm0
	add	rdx, 16
	cmp	rax, rdx
	jne	.L48
	and	r13d, 1
	je	.L40
	mov	rax, rbp
	and	rax, -2
.L47:
	movsd	xmm0, QWORD PTR [rsi+rax*8]
	addsd	xmm0, QWORD PTR [rbx+rax*8]
	addsd	xmm0, QWORD PTR [rdi+rax*8]
	movsd	QWORD PTR [rcx+rax*8], xmm0
.L40:
	cvttsd2si	ebp, QWORD PTR -8[rcx+rbp*8]
	call	_ZdaPv
	mov	rcx, rdi
	call	_ZdaPv
	mov	rcx, rsi
	call	_ZdaPv
	mov	rcx, rbx
	call	_ZdaPv
	nop
	movaps	xmm6, XMMWORD PTR 32[rsp]
	mov	eax, ebp
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L68:
	mov	rcx, r12
	call	_Znay
	mov	rcx, rax
	jmp	.L46
	.p2align 4,,10
	.p2align 3
.L67:
	xor	ecx, ecx
	call	_Znay
.LEHE11:
	mov	rcx, rax
	jmp	.L40
	.p2align 4,,10
	.p2align 3
.L54:
	xor	eax, eax
	jmp	.L47
.L53:
	xor	eax, eax
	jmp	.L41
.L56:
	mov	rdi, rax
	jmp	.L51
.L57:
	mov	rbp, rax
	jmp	.L50
.L55:
	mov	rdi, rax
	jmp	.L52
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA67:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE67-.LLSDACSB67
.LLSDACSB67:
	.uleb128 .LEHB8-.LFB67
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB9-.LFB67
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L55-.LFB67
	.uleb128 0
	.uleb128 .LEHB10-.LFB67
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L56-.LFB67
	.uleb128 0
	.uleb128 .LEHB11-.LFB67
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L57-.LFB67
	.uleb128 0
.LLSDACSE67:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z8use_expri.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8use_expri.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 56
	.seh_savereg	rsi, 64
	.seh_savereg	rdi, 72
	.seh_savereg	rbp, 80
	.seh_savexmm	xmm6, 32
	.seh_savereg	r12, 88
	.seh_savereg	r13, 96
	.seh_endprologue
_Z8use_expri.cold:
.L37:
.LEHB12:
	call	__cxa_throw_bad_array_new_length
.L50:
	mov	rcx, rdi
	mov	rdi, rbp
	call	_ZdaPv
.L51:
	mov	rcx, rsi
	call	_ZdaPv
.L52:
	mov	rcx, rbx
	call	_ZdaPv
	mov	rcx, rdi
	call	_Unwind_Resume
	nop
.LEHE12:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC67:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC67-.LLSDACSBC67
.LLSDACSBC67:
	.uleb128 .LEHB12-.LCOLDB5
	.uleb128 .LEHE12-.LEHB12
	.uleb128 0
	.uleb128 0
.LLSDACSEC67:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE5:
	.text
.LHOTE5:
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	0
	.long	1
	.long	2
	.long	3
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw_bad_array_new_length;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
