	.file	"_atom_weak_cycle.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.def	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev:
.LFB6325:
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
.LFB6329:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rax, _ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag[rip]
	mov	r8, rcx
	mov	rcx, rdx
	cmp	rdx, rax
	je	.L6
	lea	rax, _ZTSSt19_Sp_make_shared_tag[rip]
	cmp	QWORD PTR 8[rdx], rax
	je	.L6
	lea	rdx, _ZTISt19_Sp_make_shared_tag[rip]
	mov	QWORD PTR 48[rsp], r8
	call	_ZNKSt9type_info7__equalERKS_
	mov	r8, QWORD PTR 48[rsp]
	test	al, al
	je	.L7
.L6:
	lea	rax, 16[r8]
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L7:
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
.LFB6326:
	.seh_endprologue
	mov	edx, 48
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
.LFB6328:
	.seh_endprologue
	mov	edx, 48
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
.LFB5348:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rcx
	call	[QWORD PTR 16[rax]]
	lock sub	DWORD PTR 12[rbx], 1
	jne	.L10
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	mov	rax, QWORD PTR 24[rax]
	add	rsp, 32
	pop	rbx
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L10:
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
.LFB2805:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	movabs	rdx, 4294967297
	mov	r8, QWORD PTR 8[rcx]
	lea	rax, 8[rcx]
	cmp	r8, rdx
	je	.L15
	lock sub	DWORD PTR [rax], 1
	je	.L16
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L15:
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
.L16:
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
.LFB6327:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	eax, DWORD PTR g_destroy[rip]
	add	eax, 1
	mov	DWORD PTR g_destroy[rip], eax
	mov	rdx, rcx
	mov	rcx, QWORD PTR 40[rcx]
	test	rcx, rcx
	je	.L19
	mov	r9, QWORD PTR 8[rcx]
	lea	rax, 8[rcx]
	movabs	r8, 4294967297
	cmp	r9, r8
	je	.L31
	lock sub	DWORD PTR [rax], 1
	je	.L32
.L19:
	mov	rcx, QWORD PTR 24[rdx]
	test	rcx, rcx
	je	.L17
	lock sub	DWORD PTR 12[rcx], 1
	jne	.L17
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR 24[rax]
	add	rsp, 56
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L17:
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L31:
	mov	rax, QWORD PTR [rcx]
	mov	QWORD PTR 40[rsp], rdx
	mov	QWORD PTR 8[rcx], 0
	mov	QWORD PTR 32[rsp], rcx
	call	[QWORD PTR 16[rax]]
	mov	rcx, QWORD PTR 32[rsp]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 24[rax]]
	mov	rdx, QWORD PTR 40[rsp]
	jmp	.L19
	.p2align 4,,10
	.p2align 3
.L32:
	mov	QWORD PTR 32[rsp], rdx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	mov	rdx, QWORD PTR 32[rsp]
	jmp	.L19
	.seh_endproc
	.section	.text$_ZNSt10shared_ptrI4NodeEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10shared_ptrI4NodeEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_
	.def	_ZNSt10shared_ptrI4NodeEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10shared_ptrI4NodeEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_
_ZNSt10shared_ptrI4NodeEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_:
.LFB5710:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	mov	ecx, 48
	call	_Znwy
	mov	rdx, QWORD PTR .LC0[rip]
	pxor	xmm0, xmm0
	movups	XMMWORD PTR 16[rax], xmm0
	mov	QWORD PTR 8[rax], rdx
	lea	rdx, _ZTVSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	QWORD PTR [rax], rdx
	movups	XMMWORD PTR 32[rax], xmm0
	mov	QWORD PTR 8[rbx], rax
	add	rax, 16
	mov	QWORD PTR [rbx], rax
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "a use_count=\0"
.LC3:
	.ascii "\12\0"
.LC4:
	.ascii "b use_count=\0"
.LC5:
	.ascii "nodes destroyed count=\0"
	.section	.text.unlikely,"x"
.LCOLDB6:
	.section	.text.startup,"x"
.LHOTB6:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5064:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 96
	.seh_stackalloc	96
	.seh_endprologue
	call	__main
	lea	rcx, 64[rsp]
	lea	rdx, 80[rsp]
.LEHB0:
	call	_ZNSt10shared_ptrI4NodeEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_
.LEHE0:
	lea	rdx, 63[rsp]
	lea	rcx, 80[rsp]
.LEHB1:
	call	_ZNSt10shared_ptrI4NodeEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_
.LEHE1:
	mov	rax, QWORD PTR 64[rsp]
	mov	rdx, QWORD PTR 80[rsp]
	mov	rbx, QWORD PTR 88[rsp]
	mov	QWORD PTR 16[rax], rdx
	cmp	rbx, QWORD PTR 24[rax]
	je	.L35
	test	rbx, rbx
	je	.L36
	lock add	DWORD PTR 8[rbx], 1
.L36:
	mov	rcx, QWORD PTR 24[rax]
	test	rcx, rcx
	je	.L37
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	rax, QWORD PTR 40[rsp]
.L37:
	mov	QWORD PTR 24[rax], rbx
	mov	rax, QWORD PTR 64[rsp]
.L35:
	mov	rbx, QWORD PTR 80[rsp]
	mov	QWORD PTR [rbx], rax
	mov	rax, QWORD PTR 72[rsp]
	test	rax, rax
	je	.L38
	lock add	DWORD PTR 12[rax], 1
.L38:
	mov	rcx, QWORD PTR 8[rbx]
	test	rcx, rcx
	je	.L40
	lock sub	DWORD PTR 12[rcx], 1
	je	.L82
.L40:
	mov	QWORD PTR 8[rbx], rax
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC2[rip]
	mov	rcx, rbx
.LEHB2:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	rax, QWORD PTR 72[rsp]
	xor	edx, edx
	test	rax, rax
	je	.L43
	mov	edx, DWORD PTR 8[rax]
.L43:
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC3[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC4[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	rax, QWORD PTR 88[rsp]
	xor	edx, edx
	test	rax, rax
	je	.L44
	mov	edx, DWORD PTR 8[rax]
.L44:
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC3[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE2:
	mov	rcx, QWORD PTR 88[rsp]
	test	rcx, rcx
	je	.L45
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L45:
	mov	rcx, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L46
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L46:
	mov	rcx, rbx
	lea	rdx, .LC5[rip]
.LEHB3:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_destroy[rip]
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC3[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE3:
	xor	eax, eax
	add	rsp, 96
	pop	rbx
	ret
.L82:
	mov	r8, QWORD PTR [rcx]
	lea	r9, _ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv[rip]
	mov	QWORD PTR 40[rsp], rax
	mov	r8, QWORD PTR 24[r8]
	cmp	r8, r9
	jne	.L42
	call	_ZNSt23_Sp_counted_ptr_inplaceI4NodeSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	mov	rax, QWORD PTR 40[rsp]
	jmp	.L40
.L42:
	call	r8
	mov	rax, QWORD PTR 40[rsp]
	jmp	.L40
.L54:
	mov	rbx, rax
	jmp	.L47
.L53:
	mov	rbx, rax
	jmp	.L49
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5064:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5064-.LLSDACSB5064
.LLSDACSB5064:
	.uleb128 .LEHB0-.LFB5064
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5064
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L53-.LFB5064
	.uleb128 0
	.uleb128 .LEHB2-.LFB5064
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L54-.LFB5064
	.uleb128 0
	.uleb128 .LEHB3-.LFB5064
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSE5064:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 96
	.seh_endprologue
main.cold:
.L47:
	mov	rcx, QWORD PTR 88[rsp]
	test	rcx, rcx
	je	.L49
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L49:
	mov	rcx, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L50
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L50:
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5064:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5064-.LLSDACSBC5064
.LLSDACSBC5064:
	.uleb128 .LEHB4-.LCOLDB6
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSEC5064:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE6:
	.section	.text.startup,"x"
.LHOTE6:
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
	.globl	g_destroy
	.bss
	.align 4
g_destroy:
	.space 4
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
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNKSt9type_info7__equalERKS_;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
