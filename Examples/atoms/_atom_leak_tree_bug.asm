	.file	"_atom_leak_tree_bug.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZL11scrub_stackv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL11scrub_stackv
_ZL11scrub_stackv:
.LFB3894:
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
.LFB4749:
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
.LFB4753:
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
.LFB4750:
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
.LFB4752:
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
.LFB4174:
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
	.section .rdata,"dr"
.LC1:
	.ascii "vector::_M_realloc_append\0"
.LC2:
	.ascii "root children=%d\12\0"
.LC3:
	.ascii "root use_count=%ld\12\0"
	.section	.text.unlikely,"x"
.LCOLDB5:
	.text
.LHOTB5:
	.p2align 4
	.def	_ZL10build_treev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL10build_treev
_ZL10build_treev:
.LFB3890:
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
	lea	r12, 8[rax]
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
	jmp	.L35
	.p2align 4,,10
	.p2align 3
.L59:
	mov	QWORD PTR [rdx], r10
	mov	QWORD PTR 8[rdx], rbx
	lock add	DWORD PTR 8[rbx], 1
	add	QWORD PTR 32[rsi], 16
.L27:
	movabs	rdi, 4294967297
	mov	rax, QWORD PTR 8[rbx]
	cmp	rax, rdi
	je	.L54
	lock sub	DWORD PTR [r15], 1
	je	.L55
.L34:
	lea	eax, 1[rbp]
	mov	ebp, 3
	cmp	eax, 4
	je	.L56
.L35:
	mov	ecx, 64
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	rbx, rax
	mov	QWORD PTR [rax], r13
	lea	r15, 8[rax]
	mov	DWORD PTR 16[rax], ebp
	lea	r10, 16[rbx]
	mov	QWORD PTR 40[rax], 0
	mov	QWORD PTR 56[rax], 0
	movq	QWORD PTR 8[rax], xmm6
	movups	XMMWORD PTR 24[rax], xmm7
	mov	eax, DWORD PTR _ZL13g_constructed[rip]
	mov	QWORD PTR 48[rbx], r14
	add	eax, 1
	mov	DWORD PTR _ZL13g_constructed[rip], eax
	lock add	DWORD PTR [r12], 1
	mov	rdi, QWORD PTR 56[rbx]
	test	rdi, rdi
	je	.L23
	mov	rdx, QWORD PTR 8[rdi]
	lea	rax, 8[rdi]
	movabs	rcx, 4294967297
	cmp	rdx, rcx
	je	.L57
	lock sub	DWORD PTR [rax], 1
	je	.L58
.L23:
	mov	QWORD PTR 56[rbx], rsi
	mov	rdx, QWORD PTR 32[rsi]
	cmp	rdx, QWORD PTR 40[rsi]
	jne	.L59
	mov	r8, QWORD PTR 24[rsi]
	mov	r11, rdx
	movabs	rdi, 576460752303423487
	sub	r11, r8
	mov	rax, r11
	sar	rax, 4
	cmp	rax, rdi
	je	.L53
	test	rax, rax
	mov	edi, 1
	mov	QWORD PTR 56[rsp], r11
	cmovne	rdi, rax
	mov	QWORD PTR 48[rsp], r8
	mov	QWORD PTR 40[rsp], rdx
	add	rdi, rax
	mov	QWORD PTR 32[rsp], r10
	movabs	rax, 576460752303423487
	cmp	rdi, rax
	cmova	rdi, rax
	sal	rdi, 4
	mov	rcx, rdi
.LEHB2:
	call	_Znwy
.LEHE2:
	mov	r11, QWORD PTR 56[rsp]
	mov	r10, QWORD PTR 32[rsp]
	mov	QWORD PTR 8[rax+r11], rbx
	mov	QWORD PTR [rax+r11], r10
	lock add	DWORD PTR 8[rbx], 1
	mov	rdx, QWORD PTR 40[rsp]
	mov	r8, QWORD PTR 48[rsp]
	cmp	rdx, r8
	je	.L29
	lea	r11, -16[rdx]
	xor	ecx, ecx
	xor	r10d, r10d
	sub	r11, r8
	shr	r11, 4
	add	r11, 1
	.p2align 5
	.p2align 4
	.p2align 3
.L30:
	movdqu	xmm0, XMMWORD PTR [r8+rcx]
	add	r10, 1
	movups	XMMWORD PTR [rax+rcx], xmm0
	add	rcx, 16
	cmp	r10, r11
	jb	.L30
	sub	rdx, r8
	lea	r10, 16[rax+rdx]
.L31:
	mov	rdx, QWORD PTR 40[rsi]
	mov	rcx, r8
	mov	QWORD PTR 40[rsp], rax
	mov	QWORD PTR 32[rsp], r10
	sub	rdx, r8
	call	_ZdlPvy
	mov	rax, QWORD PTR 40[rsp]
	mov	r10, QWORD PTR 32[rsp]
.L32:
	mov	QWORD PTR 24[rsi], rax
	add	rax, rdi
	mov	QWORD PTR 32[rsi], r10
	mov	QWORD PTR 40[rsi], rax
	jmp	.L27
	.p2align 4,,10
	.p2align 3
.L54:
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
	jne	.L35
	.p2align 4
	.p2align 3
.L56:
	mov	rdx, QWORD PTR 32[rsi]
	sub	rdx, QWORD PTR 24[rsi]
	lea	rcx, .LC2[rip]
	sar	rdx, 4
.LEHB3:
	call	__mingw_printf
	mov	edx, DWORD PTR 8[rsi]
	lea	rcx, .LC3[rip]
	call	__mingw_printf
.LEHE3:
	nop
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
.LEHB4:
	jmp	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.LEHE4:
	.p2align 4,,10
	.p2align 3
.L57:
	mov	rax, QWORD PTR [rdi]
	mov	QWORD PTR 32[rsp], r10
	mov	rcx, rdi
	mov	QWORD PTR 8[rdi], 0
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR [rdi]
	mov	rcx, rdi
	call	[QWORD PTR 24[rax]]
	mov	r10, QWORD PTR 32[rsp]
	jmp	.L23
.L55:
	mov	rcx, rbx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	jmp	.L34
.L29:
	lea	r10, 16[rax]
	test	r8, r8
	je	.L32
	jmp	.L31
.L58:
	mov	rcx, rdi
	mov	QWORD PTR 32[rsp], r10
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	mov	r10, QWORD PTR 32[rsp]
	jmp	.L23
.L39:
	mov	rdi, rax
	jmp	.L37
.L51:
	jmp	.L52
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3890:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3890-.LLSDACSB3890
.LLSDACSB3890:
	.uleb128 .LEHB0-.LFB3890
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB3890
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L39-.LFB3890
	.uleb128 0
	.uleb128 .LEHB2-.LFB3890
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L51-.LFB3890
	.uleb128 0
	.uleb128 .LEHB3-.LFB3890
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L39-.LFB3890
	.uleb128 0
	.uleb128 .LEHB4-.LFB3890
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE3890:
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
.L53:
	lea	rcx, .LC1[rip]
.LEHB5:
	call	_ZSt20__throw_length_errorPKc
.LEHE5:
.L38:
.L52:
	mov	rcx, rbx
	mov	rdi, rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L37:
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	rcx, rdi
.LEHB6:
	call	_Unwind_Resume
	nop
.LEHE6:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC3890:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC3890-.LLSDACSBC3890
.LLSDACSBC3890:
	.uleb128 .LEHB5-.LCOLDB5
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L38-.LCOLDB5
	.uleb128 0
	.uleb128 .LEHB6-.LCOLDB5
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSEC3890:
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
.LFB3895:
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
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:
.LFB4751:
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
	mov	rbx, QWORD PTR 56[rcx]
	add	eax, 1
	mov	DWORD PTR _ZL11g_destroyed[rip], eax
	mov	rbp, rcx
	test	rbx, rbx
	je	.L63
	mov	rcx, QWORD PTR 8[rbx]
	lea	rax, 8[rbx]
	movabs	rdx, 4294967297
	cmp	rcx, rdx
	je	.L80
	lock sub	DWORD PTR [rax], 1
	je	.L81
.L63:
	mov	rdi, QWORD PTR 32[rbp]
	mov	rbx, QWORD PTR 24[rbp]
	cmp	rdi, rbx
	je	.L66
	movabs	r12, 4294967297
	jmp	.L71
	.p2align 4,,10
	.p2align 3
.L69:
	lock sub	DWORD PTR [rax], 1
	je	.L82
.L68:
	add	rbx, 16
	cmp	rdi, rbx
	je	.L83
.L71:
	mov	rsi, QWORD PTR 8[rbx]
	test	rsi, rsi
	je	.L68
	mov	rdx, QWORD PTR 8[rsi]
	lea	rax, 8[rsi]
	cmp	rdx, r12
	jne	.L69
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	mov	QWORD PTR 8[rsi], 0
	add	rbx, 16
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	call	[QWORD PTR 24[rax]]
	cmp	rdi, rbx
	jne	.L71
	.p2align 4
	.p2align 3
.L83:
	mov	rbx, QWORD PTR 24[rbp]
.L66:
	test	rbx, rbx
	je	.L61
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
.L61:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L82:
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	jmp	.L68
	.p2align 4,,10
	.p2align 3
.L80:
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	mov	QWORD PTR 8[rbx], 0
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	call	[QWORD PTR 24[rax]]
	jmp	.L63
.L81:
	mov	rcx, rbx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	jmp	.L63
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
