	.file	"_atom_leak_tree_ok.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZL11scrub_stackv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL11scrub_stackv
_ZL11scrub_stackv:
.LFB3902:
	mov	eax, 8200
	call	___chkstk_ms
	sub	rsp, rax
	.seh_stackalloc	8200
	.seh_endprologue
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L2:
	mov	BYTE PTR [rsp+rax], 0
	mov	BYTE PTR 1[rsp+rax], 0
	add	rax, 2
	cmp	rax, 8192
	jne	.L2
	add	rsp, 8200
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.def	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev:
.LFB4776:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.def	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:
.LFB4780:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rax, _ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag[rip]
	mov	r8, rcx
	mov	rcx, rdx
	cmp	rdx, rax
	je	.L10
	lea	rax, _ZTSSt19_Sp_make_shared_tag[rip]
	cmp	QWORD PTR 8[rdx], rax
	je	.L10
	lea	rdx, _ZTISt19_Sp_make_shared_tag[rip]
	mov	QWORD PTR 48[rsp], r8
	call	_ZNKSt9type_info7__equalERKS_
	mov	r8, QWORD PTR 48[rsp]
	test	al, al
	je	.L11
.L10:
	lea	rax, 16[r8]
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.def	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev:
.LFB4777:
	.seh_endprologue
	mov	edx, 64
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:
.LFB4779:
	.seh_endprologue
	mov	edx, 64
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv:
.LFB4182:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rcx
	call	[QWORD PTR 16[rax]]
	lock sub	DWORD PTR 12[rbx], 1
	jne	.L14
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	mov	rax, QWORD PTR 24[rax]
	add	rsp, 32
	pop	rbx
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L14:
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv:
.LFB2807:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	movabs	rdx, 4294967297
	mov	r8, QWORD PTR 8[rcx]
	lea	rax, 8[rcx]
	cmp	r8, rdx
	je	.L19
	lock sub	DWORD PTR [rax], 1
	je	.L20
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	mov	rax, QWORD PTR [rcx]
	mov	QWORD PTR 40[rsp], rcx
	mov	QWORD PTR 8[rcx], 0
	call	[QWORD PTR 16[rax]]
	mov	rcx, QWORD PTR 40[rsp]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR 24[rax]
	add	rsp, 56
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L20:
	add	rsp, 56
	jmp	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:
.LFB4778:
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
	mov	eax, DWORD PTR _ZL11g_destroyed[rip]
	add	eax, 1
	mov	DWORD PTR _ZL11g_destroyed[rip], eax
	mov	rbp, rcx
	mov	rcx, QWORD PTR 56[rcx]
	test	rcx, rcx
	je	.L23
	lock sub	DWORD PTR 12[rcx], 1
	je	.L39
.L23:
	mov	rdi, QWORD PTR 32[rbp]
	mov	rbx, QWORD PTR 24[rbp]
	cmp	rdi, rbx
	je	.L25
	movabs	r12, 4294967297
	jmp	.L30
	.p2align 4,,10
	.p2align 3
.L28:
	lock sub	DWORD PTR [rax], 1
	je	.L40
.L27:
	add	rbx, 16
	cmp	rdi, rbx
	je	.L41
.L30:
	mov	rsi, QWORD PTR 8[rbx]
	test	rsi, rsi
	je	.L27
	mov	rdx, QWORD PTR 8[rsi]
	lea	rax, 8[rsi]
	cmp	rdx, r12
	jne	.L28
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	mov	QWORD PTR 8[rsi], 0
	add	rbx, 16
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	call	[QWORD PTR 24[rax]]
	cmp	rdi, rbx
	jne	.L30
	.p2align 4
	.p2align 3
.L41:
	mov	rbx, QWORD PTR 24[rbp]
.L25:
	test	rbx, rbx
	je	.L21
	mov	rdx, QWORD PTR 40[rbp]
	mov	rcx, rbx
	sub	rdx, rbx
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L39:
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 24[rax]]
	jmp	.L23
	.p2align 4,,10
	.p2align 3
.L21:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L40:
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	jmp	.L27
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "vector::_M_realloc_append\0"
.LC2:
	.ascii "root children=%d\12\0"
.LC3:
	.ascii "parent reachable=%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB5:
	.text
.LHOTB5:
	.p2align 4
	.def	_ZL10build_treev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL10build_treev
_ZL10build_treev:
.LFB3893:
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
	sub	rsp, 104
	.seh_stackalloc	104
	movaps	XMMWORD PTR 64[rsp], xmm6
	.seh_savexmm	xmm6, 64
	movaps	XMMWORD PTR 80[rsp], xmm7
	.seh_savexmm	xmm7, 80
	.seh_endprologue
	mov	ecx, 64
	lea	r13, _ZTVSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	ebp, 2
.LEHB0:
	call	_Znwy
.LEHE0:
	pxor	xmm0, xmm0
	movq	xmm6, QWORD PTR .LC0[rip]
	mov	rsi, rax
	mov	QWORD PTR [rax], r13
	movdqa	xmm7, xmm0
	mov	QWORD PTR 16[rax], 1
	lea	r14, 16[rsi]
	mov	QWORD PTR 56[rax], 0
	movq	QWORD PTR 8[rax], xmm6
	movups	XMMWORD PTR 24[rax], xmm0
	movups	XMMWORD PTR 40[rax], xmm0
	mov	eax, DWORD PTR _ZL13g_constructed[rip]
	add	eax, 1
	mov	DWORD PTR _ZL13g_constructed[rip], eax
	jmp	.L55
	.p2align 4,,10
	.p2align 3
.L94:
	mov	QWORD PTR [r8], r15
	mov	QWORD PTR 8[r8], rbx
	lock add	DWORD PTR 8[rbx], 1
	add	QWORD PTR 32[rsi], 16
.L47:
	movabs	rdi, 4294967297
	mov	rax, QWORD PTR 8[rbx]
	cmp	rax, rdi
	je	.L91
	lock sub	DWORD PTR [r12], 1
	je	.L92
.L54:
	lea	eax, 1[rbp]
	mov	ebp, 3
	cmp	eax, 4
	je	.L93
.L55:
	mov	ecx, 64
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	rbx, rax
	mov	QWORD PTR [rax], r13
	lea	r12, 8[rax]
	mov	DWORD PTR 16[rax], ebp
	lea	r15, 16[rbx]
	mov	QWORD PTR 40[rax], 0
	mov	QWORD PTR 56[rax], 0
	movq	QWORD PTR 8[rax], xmm6
	movups	XMMWORD PTR 24[rax], xmm7
	mov	eax, DWORD PTR _ZL13g_constructed[rip]
	mov	QWORD PTR 48[rbx], r14
	add	eax, 1
	mov	DWORD PTR _ZL13g_constructed[rip], eax
	lock add	DWORD PTR 12[rsi], 1
	mov	rcx, QWORD PTR 56[rbx]
	test	rcx, rcx
	je	.L44
	lock sub	DWORD PTR 12[rcx], 1
	jne	.L44
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 24[rax]]
.L44:
	mov	QWORD PTR 56[rbx], rsi
	mov	r8, QWORD PTR 32[rsi]
	cmp	r8, QWORD PTR 40[rsi]
	jne	.L94
	mov	r9, QWORD PTR 24[rsi]
	mov	r11, r8
	movabs	rdi, 576460752303423487
	sub	r11, r9
	mov	rax, r11
	sar	rax, 4
	cmp	rax, rdi
	je	.L88
	test	rax, rax
	mov	edi, 1
	mov	QWORD PTR 56[rsp], r11
	cmovne	rdi, rax
	mov	QWORD PTR 48[rsp], r9
	mov	QWORD PTR 40[rsp], r8
	add	rdi, rax
	movabs	rax, 576460752303423487
	cmp	rdi, rax
	cmova	rdi, rax
	sal	rdi, 4
	mov	rcx, rdi
.LEHB2:
	call	_Znwy
.LEHE2:
	mov	r11, QWORD PTR 56[rsp]
	mov	r10, rax
	mov	QWORD PTR [rax+r11], r15
	mov	QWORD PTR 8[rax+r11], rbx
	lock add	DWORD PTR 8[rbx], 1
	mov	r8, QWORD PTR 40[rsp]
	mov	r9, QWORD PTR 48[rsp]
	cmp	r8, r9
	je	.L49
	lea	rcx, -16[r8]
	xor	eax, eax
	xor	edx, edx
	sub	rcx, r9
	shr	rcx, 4
	add	rcx, 1
	.p2align 5
	.p2align 4
	.p2align 3
.L50:
	movdqu	xmm0, XMMWORD PTR [r9+rax]
	add	rdx, 1
	movups	XMMWORD PTR [r10+rax], xmm0
	add	rax, 16
	cmp	rdx, rcx
	jb	.L50
	sub	r8, r9
	lea	rax, 16[r10+r8]
.L51:
	mov	rdx, QWORD PTR 40[rsi]
	mov	rcx, r9
	mov	QWORD PTR 48[rsp], r10
	mov	QWORD PTR 40[rsp], rax
	sub	rdx, r9
	call	_ZdlPvy
	mov	r10, QWORD PTR 48[rsp]
	mov	rax, QWORD PTR 40[rsp]
.L52:
	mov	QWORD PTR 24[rsi], r10
	add	r10, rdi
	mov	QWORD PTR 32[rsi], rax
	mov	QWORD PTR 40[rsi], r10
	jmp	.L47
	.p2align 4,,10
	.p2align 3
.L91:
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	mov	QWORD PTR 8[rbx], 0
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	call	[QWORD PTR 24[rax]]
	lea	eax, 1[rbp]
	mov	ebp, 3
	cmp	eax, 4
	jne	.L55
	.p2align 4
	.p2align 3
.L93:
	mov	rdx, QWORD PTR 32[rsi]
	sub	rdx, QWORD PTR 24[rsi]
	lea	rcx, .LC2[rip]
	sar	rdx, 4
.LEHB3:
	call	__mingw_printf
.LEHE3:
	mov	rax, QWORD PTR 24[rsi]
	mov	rdx, QWORD PTR [rax]
	mov	rbx, QWORD PTR 40[rdx]
	test	rbx, rbx
	je	.L56
	mov	eax, DWORD PTR 8[rbx]
	lea	rcx, 8[rbx]
.L58:
	test	eax, eax
	je	.L56
	lea	r8d, 1[rax]
	lock cmpxchg	DWORD PTR [rcx], r8d
	jne	.L58
	mov	eax, DWORD PTR 8[rbx]
	test	eax, eax
	je	.L95
	cmp	QWORD PTR 32[rdx], 0
	lea	rcx, .LC3[rip]
	setne	dl
	movzx	edx, dl
.LEHB4:
	call	__mingw_printf
.LEHE4:
.L59:
	mov	rcx, rbx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	nop
.L60:
	movaps	xmm6, XMMWORD PTR 64[rsp]
	movaps	xmm7, XMMWORD PTR 80[rsp]
	mov	rcx, rsi
	add	rsp, 104
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
.LEHB5:
	jmp	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.LEHE5:
.L95:
	xor	edx, edx
	lea	rcx, .LC3[rip]
.LEHB6:
	call	__mingw_printf
.LEHE6:
	jmp	.L59
.L56:
	xor	edx, edx
	lea	rcx, .LC3[rip]
.LEHB7:
	call	__mingw_printf
.LEHE7:
	jmp	.L60
.L92:
	mov	rcx, rbx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	jmp	.L54
.L49:
	lea	rax, 16[rax]
	test	r9, r9
	je	.L52
	jmp	.L51
.L86:
	jmp	.L87
.L67:
	mov	rdi, rax
	jmp	.L62
.L68:
	mov	rdi, rax
	jmp	.L61
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3893:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3893-.LLSDACSB3893
.LLSDACSB3893:
	.uleb128 .LEHB0-.LFB3893
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB3893
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L67-.LFB3893
	.uleb128 0
	.uleb128 .LEHB2-.LFB3893
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L86-.LFB3893
	.uleb128 0
	.uleb128 .LEHB3-.LFB3893
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L67-.LFB3893
	.uleb128 0
	.uleb128 .LEHB4-.LFB3893
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L68-.LFB3893
	.uleb128 0
	.uleb128 .LEHB5-.LFB3893
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LFB3893
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L68-.LFB3893
	.uleb128 0
	.uleb128 .LEHB7-.LFB3893
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L67-.LFB3893
	.uleb128 0
.LLSDACSE3893:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZL10build_treev.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL10build_treev.cold
	.seh_stackalloc	168
	.seh_savereg	rbx, 104
	.seh_savereg	rsi, 112
	.seh_savereg	rdi, 120
	.seh_savereg	rbp, 128
	.seh_savexmm	xmm6, 64
	.seh_savexmm	xmm7, 80
	.seh_savereg	r12, 136
	.seh_savereg	r13, 144
	.seh_savereg	r14, 152
	.seh_savereg	r15, 160
	.seh_endprologue
_ZL10build_treev.cold:
.L88:
	lea	rcx, .LC1[rip]
.LEHB8:
	call	_ZSt20__throw_length_errorPKc
.LEHE8:
.L66:
.L87:
	mov	rcx, rbx
	mov	rdi, rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L62:
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	rcx, rdi
.LEHB9:
	call	_Unwind_Resume
.LEHE9:
.L61:
	mov	rcx, rbx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	jmp	.L62
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC3893:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC3893-.LLSDACSBC3893
.LLSDACSBC3893:
	.uleb128 .LEHB8-.LCOLDB5
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L66-.LCOLDB5
	.uleb128 0
	.uleb128 .LEHB9-.LCOLDB5
	.uleb128 .LEHE9-.LEHB9
	.uleb128 0
	.uleb128 0
.LLSDACSEC3893:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE5:
	.text
.LHOTE5:
	.section .rdata,"dr"
.LC6:
	.ascii "constructed=%d\12\0"
.LC7:
	.ascii "destroyed after scope=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3903:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	call	_ZL10build_treev
	lea	rcx, .LC6[rip]
	call	_ZL11scrub_stackv
	mov	edx, DWORD PTR _ZL13g_constructed[rip]
	call	__mingw_printf
	mov	edx, DWORD PTR _ZL11g_destroyed[rip]
	lea	rcx, .LC7[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.globl	_ZTSSt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTSSt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 32
_ZTSSt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "St11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE\0"
	.globl	_ZTISt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTISt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTISt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSSt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE
	.globl	_ZTSSt19_Sp_make_shared_tag
	.section	.rdata$_ZTSSt19_Sp_make_shared_tag,"dr"
	.linkonce same_size
	.align 16
_ZTSSt19_Sp_make_shared_tag:
	.ascii "St19_Sp_make_shared_tag\0"
	.globl	_ZTISt19_Sp_make_shared_tag
	.section	.rdata$_ZTISt19_Sp_make_shared_tag,"dr"
	.linkonce same_size
	.align 8
_ZTISt19_Sp_make_shared_tag:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSSt19_Sp_make_shared_tag
	.globl	_ZTSSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTSSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 32
_ZTSSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "St16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE\0"
	.globl	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZTISt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE
	.globl	_ZTSSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTSSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 32
_ZTSSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "St23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE\0"
	.globl	_ZTISt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTISt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTISt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.globl	_ZTVSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTVSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTVSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	0
	.quad	_ZTISt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
.lcomm _ZL11g_destroyed,4,4
.lcomm _ZL13g_constructed,4,4
	.globl	_ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag
	.section	.rdata$_ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag,"dr"
	.linkonce same_size
	.align 8
_ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag:
	.space 16
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	1
	.long	1
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNKSt9type_info7__equalERKS_;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
