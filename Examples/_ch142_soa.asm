	.file	"_ch142_soa.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z13integrate_soaR12ParticlesSoAf
	.def	_Z13integrate_soaR12ParticlesSoAf;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13integrate_soaR12ParticlesSoAf
_Z13integrate_soaR12ParticlesSoAf:
.LFB1715:
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	rdx, QWORD PTR [rcx]
	mov	r8, rax
	sub	r8, rdx
	sar	r8, 2
	cmp	rax, rdx
	je	.L1
	mov	rcx, QWORD PTR 72[rcx]
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L3:
	movss	xmm0, DWORD PTR [rcx+rax*4]
	mulss	xmm0, xmm1
	addss	xmm0, DWORD PTR [rdx+rax*4]
	movss	DWORD PTR [rdx+rax*4], xmm0
	add	rax, 1
	cmp	rax, r8
	jb	.L3
.L1:
	ret
	.seh_endproc
	.section	.text$_ZN12ParticlesSoAD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN12ParticlesSoAD1Ev
	.def	_ZN12ParticlesSoAD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN12ParticlesSoAD1Ev
_ZN12ParticlesSoAD1Ev:
.LFB1744:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	mov	rcx, QWORD PTR 120[rcx]
	test	rcx, rcx
	je	.L7
	mov	rdx, QWORD PTR 136[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L7:
	mov	rcx, QWORD PTR 96[rbx]
	test	rcx, rcx
	je	.L8
	mov	rdx, QWORD PTR 112[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L8:
	mov	rcx, QWORD PTR 72[rbx]
	test	rcx, rcx
	je	.L9
	mov	rdx, QWORD PTR 88[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L9:
	mov	rcx, QWORD PTR 48[rbx]
	test	rcx, rcx
	je	.L10
	mov	rdx, QWORD PTR 64[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L10:
	mov	rcx, QWORD PTR 24[rbx]
	test	rcx, rcx
	je	.L11
	mov	rdx, QWORD PTR 40[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L11:
	mov	rcx, QWORD PTR [rbx]
	test	rcx, rcx
	je	.L6
	mov	rdx, QWORD PTR 16[rbx]
	sub	rdx, rcx
	add	rsp, 32
	pop	rbx
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L6:
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "cannot create std::vector larger than max_size()\0"
	.section	.text$_ZNSt6vectorIfSaIfEE14_M_fill_assignEyRKf,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIfSaIfEE14_M_fill_assignEyRKf
	.def	_ZNSt6vectorIfSaIfEE14_M_fill_assignEyRKf;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIfSaIfEE14_M_fill_assignEyRKf
_ZNSt6vectorIfSaIfEE14_M_fill_assignEyRKf:
.LFB1765:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rsi, rcx
	mov	rcx, QWORD PTR 16[rcx]
	mov	rdi, r8
	sub	rcx, rax
	sar	rcx, 2
	cmp	rcx, rdx
	jb	.L76
	mov	rcx, QWORD PTR 8[rsi]
	mov	r9, rcx
	sub	r9, rax
	mov	r8, r9
	sar	r8, 2
	cmp	r8, rdx
	jnb	.L34
	cmp	rax, rcx
	movss	xmm0, DWORD PTR [rdi]
	je	.L35
	and	r9d, 4
	je	.L36
	movss	DWORD PTR [rax], xmm0
	add	rax, 4
	cmp	rcx, rax
	je	.L73
	.p2align 4,,10
	.p2align 3
.L36:
	movss	DWORD PTR [rax], xmm0
	add	rax, 8
	movss	DWORD PTR -4[rax], xmm0
	cmp	rcx, rax
	jne	.L36
.L73:
	movss	xmm0, DWORD PTR [rdi]
.L35:
	sub	rdx, r8
	lea	rax, [rcx+rdx*4]
	cmp	rcx, rax
	je	.L74
	mov	rdx, rax
	sub	rdx, rcx
	and	edx, 4
	je	.L37
	movss	DWORD PTR [rcx], xmm0
	add	rcx, 4
	cmp	rax, rcx
	je	.L74
	.p2align 4,,10
	.p2align 3
.L37:
	movss	DWORD PTR [rcx], xmm0
	add	rcx, 8
	movss	DWORD PTR -4[rcx], xmm0
	cmp	rax, rcx
	jne	.L37
.L74:
	mov	QWORD PTR 8[rsi], rax
.L28:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L34:
	test	rdx, rdx
	je	.L39
	lea	rdx, [rax+rdx*4]
	movss	xmm0, DWORD PTR [rdi]
	cmp	rax, rdx
	je	.L40
	mov	r8, rdx
	sub	r8, rax
	and	r8d, 4
	je	.L41
	movss	DWORD PTR [rax], xmm0
	add	rax, 4
	cmp	rdx, rax
	je	.L40
	.p2align 4,,10
	.p2align 3
.L41:
	movss	DWORD PTR [rax], xmm0
	add	rax, 8
	movss	DWORD PTR -4[rax], xmm0
	cmp	rdx, rax
	jne	.L41
.L40:
	mov	rax, rdx
.L39:
	cmp	rcx, rax
	jne	.L74
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L76:
	movabs	rax, 2305843009213693951
	cmp	rax, rdx
	jb	.L77
	lea	rbx, 0[0+rdx*4]
	mov	rcx, rbx
	call	_Znwy
	movss	xmm0, DWORD PTR [rdi]
	lea	rcx, [rax+rbx]
	movq	xmm1, rax
	mov	rdx, rcx
	movq	xmm2, rcx
	sub	rdx, rax
	punpcklqdq	xmm1, xmm2
	and	edx, 4
	je	.L31
	movss	DWORD PTR [rax], xmm0
	add	rax, 4
	cmp	rcx, rax
	je	.L72
	.p2align 4,,10
	.p2align 3
.L31:
	movss	DWORD PTR [rax], xmm0
	add	rax, 8
	movss	DWORD PTR -4[rax], xmm0
	cmp	rcx, rax
	jne	.L31
.L72:
	mov	rax, QWORD PTR [rsi]
	movups	XMMWORD PTR [rsi], xmm1
	mov	rdx, QWORD PTR 16[rsi]
	mov	QWORD PTR 16[rsi], rcx
	test	rax, rax
	je	.L28
	sub	rdx, rax
	mov	rcx, rax
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	jmp	_ZdlPvy
.L77:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1716:
	push	rdi
	.seh_pushreg	rdi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 200
	.seh_stackalloc	200
	.seh_endprologue
	call	__main
	lea	rdi, 48[rsp]
	mov	ecx, 18
	xor	eax, eax
	rep stosq
	lea	rbx, 48[rsp]
	mov	edx, 1024
	mov	DWORD PTR 44[rsp], 0x00000000
	lea	rdi, 44[rsp]
	mov	rcx, rbx
	mov	r8, rdi
.LEHB0:
	call	_ZNSt6vectorIfSaIfEE14_M_fill_assignEyRKf
	lea	rcx, 120[rsp]
	mov	r8, rdi
	mov	edx, 1024
	mov	DWORD PTR 44[rsp], 0x3f800000
	call	_ZNSt6vectorIfSaIfEE14_M_fill_assignEyRKf
.LEHE0:
	movss	xmm1, DWORD PTR .LC3[rip]
	mov	rcx, rbx
	call	_Z13integrate_soaR12ParticlesSoAf
	mov	rax, QWORD PTR 48[rsp]
	mov	rcx, rbx
	cvttss2si	edi, DWORD PTR [rax]
	call	_ZN12ParticlesSoAD1Ev
	mov	eax, edi
	add	rsp, 200
	pop	rbx
	pop	rdi
	ret
.L80:
	mov	rdi, rax
	mov	rcx, rbx
	call	_ZN12ParticlesSoAD1Ev
	mov	rcx, rdi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1716:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1716-.LLSDACSB1716
.LLSDACSB1716:
	.uleb128 .LEHB0-.LFB1716
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L80-.LFB1716
	.uleb128 0
	.uleb128 .LEHB1-.LFB1716
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE1716:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 4
.LC3:
	.long	1015222895
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
