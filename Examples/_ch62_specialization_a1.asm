	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNKSt5ctypeIcE8do_widenEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt5ctypeIcE8do_widenEc
	.def	_ZNKSt5ctypeIcE8do_widenEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt5ctypeIcE8do_widenEc
_ZNKSt5ctypeIcE8do_widenEc:
.LFB2312:
	.seh_endprologue
	mov	eax, edx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "cannot create std::vector larger than max_size()\0"
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6vectorIiSaIiEEC1ESt16initializer_listIiERKS0_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIiSaIiEEC1ESt16initializer_listIiERKS0_.isra.0
_ZNSt6vectorIiSaIiEEC1ESt16initializer_listIiERKS0_.isra.0:
.LFB3693:
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
	pxor	xmm0, xmm0
	movabs	rax, 9223372036854775804
	mov	rsi, QWORD PTR 8[rdx]
	mov	rbp, QWORD PTR [rdx]
	sal	rsi, 2
	mov	rbx, rcx
	movups	XMMWORD PTR [rcx], xmm0
	cmp	rax, rsi
	mov	QWORD PTR 16[rcx], 0
	jb	.L16
	test	rsi, rsi
	je	.L17
	mov	rcx, rsi
.LEHB0:
	call	_Znwy
	lea	rdi, [rax+rsi]
	cmp	rsi, 4
	mov	rcx, rax
	mov	QWORD PTR [rbx], rax
	mov	QWORD PTR 16[rbx], rdi
	je	.L7
	mov	r8, rsi
	mov	rdx, rbp
	call	memcpy
.L6:
	mov	QWORD PTR 8[rbx], rdi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L17:
	xor	eax, eax
	xor	edi, edi
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 16[rcx], rax
	jmp	.L6
.L7:
	mov	eax, DWORD PTR 0[rbp]
	mov	DWORD PTR [rcx], eax
	jmp	.L6
.L16:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE0:
.L11:
	mov	rcx, QWORD PTR [rbx]
	mov	rsi, rax
	mov	rdx, QWORD PTR 16[rbx]
	sub	rdx, rcx
	test	rcx, rcx
	je	.L10
	call	_ZdlPvy
.L10:
	mov	rcx, rsi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3693:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3693-.LLSDACSB3693
.LLSDACSB3693:
	.uleb128 .LEHB0-.LFB3693
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L11-.LFB3693
	.uleb128 0
	.uleb128 .LEHB1-.LFB3693
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE3693:
	.text
	.seh_endproc
	.p2align 4
	.globl	_Z16run_ifelse_chainRKSt6vectorIiSaIiEES3_
	.def	_Z16run_ifelse_chainRKSt6vectorIiSaIiEES3_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16run_ifelse_chainRKSt6vectorIiSaIiEES3_
_Z16run_ifelse_chainRKSt6vectorIiSaIiEES3_:
.LFB2938:
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	r8, QWORD PTR [rcx]
	mov	r9, rax
	sub	r9, r8
	sar	r9, 2
	cmp	rax, r8
	je	.L23
	mov	r10, QWORD PTR [rdx]
	xor	eax, eax
	xor	ecx, ecx
	jmp	.L22
	.p2align 4,,10
	.p2align 3
.L25:
	add	edx, 7
	add	rax, 1
	movsx	rdx, edx
	add	rcx, rdx
	cmp	rax, r9
	jnb	.L18
.L22:
	mov	r11d, DWORD PTR [r10+rax*4]
	mov	edx, DWORD PTR [r8+rax*4]
	test	r11d, r11d
	je	.L25
	lea	edx, [rdx+rdx*2]
	add	rax, 1
	movsx	rdx, edx
	add	rcx, rdx
	cmp	rax, r9
	jb	.L22
.L18:
	mov	rax, rcx
	ret
	.p2align 4,,10
	.p2align 3
.L23:
	xor	ecx, ecx
	mov	rax, rcx
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
.LFB3290:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L26
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L26:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC5:
	.ascii "constexpr=\0"
.LC6:
	.ascii " ifelse=\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2939:
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
	call	__main
	lea	r12, 32[rsp]
	movdqa	xmm0, XMMWORD PTR .LC1[rip]
	mov	DWORD PTR 192[rsp], 5
	lea	rsi, 80[rsp]
	mov	rdx, r12
	mov	QWORD PTR 40[rsp], 5
	movaps	XMMWORD PTR 176[rsp], xmm0
	lea	rbx, 176[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 32[rsp], rbx
	lea	rdi, 112[rsp]
.LEHB2:
	call	_ZNSt6vectorIiSaIiEEC1ESt16initializer_listIiERKS0_.isra.0
.LEHE2:
	mov	rdx, r12
	mov	rcx, rdi
	mov	QWORD PTR 32[rsp], rbx
	mov	QWORD PTR 40[rsp], 3
	mov	rax, QWORD PTR .LC2[rip]
	mov	DWORD PTR 184[rsp], 5
	mov	QWORD PTR 176[rsp], rax
.LEHB3:
	call	_ZNSt6vectorIiSaIiEEC1ESt16initializer_listIiERKS0_.isra.0
.LEHE3:
	mov	rax, QWORD PTR .LC3[rip]
	lea	rbp, 144[rsp]
	mov	rdx, r12
	mov	QWORD PTR 32[rsp], rbx
	mov	QWORD PTR 40[rsp], 2
	mov	rcx, rbp
	mov	QWORD PTR 176[rsp], rax
.LEHB4:
	call	_ZNSt6vectorIiSaIiEEC1ESt16initializer_listIiERKS0_.isra.0
.LEHE4:
	movdqa	xmm0, XMMWORD PTR .LC4[rip]
	lea	rax, 48[rsp]
	mov	rdx, r12
	mov	rcx, rbx
	mov	DWORD PTR 64[rsp], 0
	movaps	XMMWORD PTR 48[rsp], xmm0
	mov	QWORD PTR 32[rsp], rax
	mov	QWORD PTR 40[rsp], 5
.LEHB5:
	call	_ZNSt6vectorIiSaIiEEC1ESt16initializer_listIiERKS0_.isra.0
.LEHE5:
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC5[rip]
.LEHB6:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rdx, QWORD PTR 112[rsp]
	xor	r9d, r9d
	mov	r8, rax
	mov	rcx, QWORD PTR 120[rsp]
	cmp	rcx, rdx
	je	.L29
	.p2align 4,,10
	.p2align 3
.L30:
	mov	eax, DWORD PTR [rdx]
	add	rdx, 4
	add	eax, 7
	cdqe
	add	r9, rax
	cmp	rdx, rcx
	jne	.L30
.L29:
	mov	rax, QWORD PTR 144[rsp]
	xor	edx, edx
	mov	r10, QWORD PTR 152[rsp]
	cmp	rax, r10
	je	.L31
	.p2align 4,,10
	.p2align 3
.L32:
	mov	ecx, DWORD PTR [rax]
	add	rax, 4
	lea	ecx, [rcx+rcx*2]
	movsx	rcx, ecx
	add	rdx, rcx
	cmp	r10, rax
	jne	.L32
.L31:
	add	rdx, r9
	mov	rcx, r8
	call	_ZNSo9_M_insertIxEERSoT_
	lea	rdx, .LC6[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rdx, rbx
	mov	rcx, rsi
	mov	r12, rax
	call	_Z16run_ifelse_chainRKSt6vectorIiSaIiEES3_
	mov	rcx, r12
	mov	rdx, rax
	call	_ZNSo9_M_insertIxEERSoT_
	mov	r12, rax
	mov	rax, QWORD PTR [rax]
	mov	rax, QWORD PTR -24[rax]
	mov	r13, QWORD PTR 240[r12+rax]
	test	r13, r13
	je	.L51
	cmp	BYTE PTR 56[r13], 0
	je	.L34
	movsx	edx, BYTE PTR 67[r13]
.L35:
	mov	rcx, r12
	call	_ZNSo3putEc
	mov	rcx, rax
	call	_ZNSo5flushEv
	mov	rcx, rbx
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, rbp
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, rdi
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, rsi
	call	_ZNSt6vectorIiSaIiEED1Ev
	xor	eax, eax
	add	rsp, 216
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
.L34:
	mov	rcx, r13
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR 0[r13]
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	edx, 10
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L35
	mov	edx, 10
	mov	rcx, r13
	call	rax
	movsx	edx, al
	jmp	.L35
.L51:
	call	_ZSt16__throw_bad_castv
.LEHE6:
.L45:
	mov	rbx, rax
.L37:
	mov	rcx, rbp
	call	_ZNSt6vectorIiSaIiEED1Ev
.L38:
	mov	rcx, rdi
	call	_ZNSt6vectorIiSaIiEED1Ev
.L39:
	mov	rcx, rsi
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, rbx
.LEHB7:
	call	_Unwind_Resume
.LEHE7:
.L44:
	mov	rbx, rax
	jmp	.L38
.L46:
	mov	r12, rax
	mov	rcx, rbx
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rbx, r12
	jmp	.L37
.L43:
	mov	rbx, rax
	jmp	.L39
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2939:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2939-.LLSDACSB2939
.LLSDACSB2939:
	.uleb128 .LEHB2-.LFB2939
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB3-.LFB2939
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L43-.LFB2939
	.uleb128 0
	.uleb128 .LEHB4-.LFB2939
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L44-.LFB2939
	.uleb128 0
	.uleb128 .LEHB5-.LFB2939
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L45-.LFB2939
	.uleb128 0
	.uleb128 .LEHB6-.LFB2939
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L46-.LFB2939
	.uleb128 0
	.uleb128 .LEHB7-.LFB2939
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSE2939:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC1:
	.long	1
	.long	2
	.long	3
	.long	4
	.align 8
.LC2:
	.long	1
	.long	3
	.align 8
.LC3:
	.long	2
	.long	4
	.align 16
.LC4:
	.long	0
	.long	1
	.long	0
	.long	1
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIxEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
