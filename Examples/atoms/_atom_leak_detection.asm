	.file	"_atom_leak_detection.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZN12_GLOBAL__N_1L10run_scopedEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_1L10run_scopedEv
_ZN12_GLOBAL__N_1L10run_scopedEv:
.LFB3910:
	.seh_endprologue
	mov	eax, DWORD PTR _ZN12_GLOBAL__N_1L13g_scoped_dtorE[rip]
	add	eax, 1
	mov	DWORD PTR _ZN12_GLOBAL__N_1L13g_scoped_dtorE[rip], eax
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED2Ev
_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED2Ev:
.LFB4798:
	.seh_endprologue
	ret
	.seh_endproc
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev,_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:
.LFB4801:
	.seh_endprologue
	mov	eax, DWORD PTR _ZN12_GLOBAL__N_1L12g_owned_dtorE[rip]
	add	eax, 1
	mov	DWORD PTR _ZN12_GLOBAL__N_1L12g_owned_dtorE[rip], eax
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED2Ev
_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED2Ev:
.LFB4805:
	.seh_endprologue
	ret
	.seh_endproc
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev,_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:
.LFB4810:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rax, _ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag[rip]
	mov	r8, rcx
	mov	rcx, rdx
	cmp	rdx, rax
	je	.L9
	lea	rax, _ZTSSt19_Sp_make_shared_tag[rip]
	cmp	QWORD PTR 8[rdx], rax
	je	.L9
	lea	rdx, _ZTISt19_Sp_make_shared_tag[rip]
	mov	QWORD PTR 48[rsp], r8
	call	_ZNKSt9type_info7__equalERKS_
	mov	r8, QWORD PTR 48[rsp]
	test	al, al
	je	.L10
.L9:
	lea	rax, 16[r8]
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info;	.scl	3;	.type	32;	.endef
	.set	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info,_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.align 2
	.p2align 4
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev:
.LFB4807:
	.seh_endprologue
	mov	edx, 32
	jmp	_ZdlPvy
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev:
.LFB4800:
	.seh_endprologue
	mov	edx, 24
	jmp	_ZdlPvy
	.seh_endproc
	.p2align 4
	.def	_ZN12_GLOBAL__N_1L8registryEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_1L8registryEv
_ZN12_GLOBAL__N_1L8registryEv:
.LFB3886:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	movzx	eax, BYTE PTR _ZGVZN12_GLOBAL__N_1L8registryEvE1r[rip]
	test	al, al
	je	.L20
.L15:
	lea	rax, _ZZN12_GLOBAL__N_1L8registryEvE1r[rip]
	add	rsp, 40
	ret
.L20:
	lea	rcx, _ZGVZN12_GLOBAL__N_1L8registryEvE1r[rip]
	call	__cxa_guard_acquire
	test	eax, eax
	je	.L15
	lea	rcx, __tcf_ZZN12_GLOBAL__N_1L8registryEvE1r[rip]
	call	atexit
	lea	rcx, _ZGVZN12_GLOBAL__N_1L8registryEvE1r[rip]
	call	__cxa_guard_release
	jmp	.L15
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:
.LFB4802:
	.seh_endprologue
	mov	edx, 24
	jmp	_ZdlPvy
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:
.LFB4809:
	.seh_endprologue
	mov	edx, 32
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
.LFB4201:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rcx
	call	[QWORD PTR 16[rax]]
	lock sub	DWORD PTR 12[rbx], 1
	jne	.L23
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	mov	rax, QWORD PTR 24[rax]
	add	rsp, 32
	pop	rbx
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L23:
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
	je	.L28
	lock sub	DWORD PTR [rax], 1
	je	.L29
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L28:
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
.L29:
	add	rsp, 56
	jmp	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "vector::_M_realloc_append\0"
	.section	.text.unlikely,"x"
.LCOLDB2:
	.text
.LHOTB2:
	.p2align 4
	.def	_ZN12_GLOBAL__N_1L9run_ownedEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_1L9run_ownedEv
_ZN12_GLOBAL__N_1L9run_ownedEv:
.LFB3915:
	push	r14
	.seh_pushreg	r14
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	call	_ZN12_GLOBAL__N_1L8registryEv
	mov	ecx, 24
	mov	rsi, rax
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r8, QWORD PTR 8[rsi]
	mov	rdx, QWORD PTR 16[rsi]
	mov	rbx, rax
	mov	rax, QWORD PTR .LC0[rip]
	mov	DWORD PTR 16[rbx], 0
	lea	r11, 16[rbx]
	mov	QWORD PTR 8[rbx], rax
	lea	rax, _ZTVSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	QWORD PTR [rbx], rax
	cmp	r8, rdx
	je	.L31
	mov	QWORD PTR [r8], r11
	add	r8, 16
	mov	QWORD PTR -8[r8], rbx
	mov	QWORD PTR 8[rsi], r8
.L30:
	add	rsp, 72
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
.L31:
	mov	r10, QWORD PTR [rsi]
	mov	rax, r8
	sub	rax, r10
	mov	rcx, rax
	mov	rdi, rax
	movabs	rax, 576460752303423487
	sar	rcx, 4
	cmp	rcx, rax
	je	.L46
	test	rcx, rcx
	mov	eax, 1
	mov	QWORD PTR 56[rsp], r10
	cmovne	rax, rcx
	mov	QWORD PTR 48[rsp], r11
	mov	QWORD PTR 40[rsp], rdx
	add	rax, rcx
	mov	QWORD PTR 32[rsp], r8
	movabs	rcx, 576460752303423487
	cmp	rax, rcx
	cmova	rax, rcx
	sal	rax, 4
	mov	rcx, rax
	mov	r14, rax
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	r8, QWORD PTR 32[rsp]
	mov	r10, QWORD PTR 56[rsp]
	mov	QWORD PTR 8[rax+rdi], rbx
	mov	r9, rax
	mov	r11, QWORD PTR 48[rsp]
	mov	rdx, QWORD PTR 40[rsp]
	cmp	r8, r10
	mov	QWORD PTR [rax+rdi], r11
	je	.L34
	lea	r11, -16[r8]
	xor	eax, eax
	xor	ecx, ecx
	sub	r11, r10
	shr	r11, 4
	add	r11, 1
	.p2align 5
	.p2align 4
	.p2align 3
.L35:
	movdqu	xmm0, XMMWORD PTR [r10+rax]
	add	rcx, 1
	movups	XMMWORD PTR [r9+rax], xmm0
	add	rax, 16
	cmp	rcx, r11
	jb	.L35
	sub	r8, r10
	lea	rbx, 16[r9+r8]
.L36:
	sub	rdx, r10
	mov	rcx, r10
	mov	QWORD PTR 32[rsp], r9
	call	_ZdlPvy
	mov	r9, QWORD PTR 32[rsp]
.L37:
	mov	QWORD PTR [rsi], r9
	add	r9, r14
	mov	QWORD PTR 8[rsi], rbx
	mov	QWORD PTR 16[rsi], r9
	jmp	.L30
.L34:
	lea	rbx, 16[rax]
	test	r10, r10
	je	.L37
	jmp	.L36
.L44:
	jmp	.L45
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3915:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3915-.LLSDACSB3915
.LLSDACSB3915:
	.uleb128 .LEHB0-.LFB3915
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB3915
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L44-.LFB3915
	.uleb128 0
.LLSDACSE3915:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZN12_GLOBAL__N_1L9run_ownedEv.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_1L9run_ownedEv.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 72
	.seh_savereg	rsi, 80
	.seh_savereg	rdi, 88
	.seh_savereg	r14, 96
	.seh_endprologue
_ZN12_GLOBAL__N_1L9run_ownedEv.cold:
.L46:
	lea	rcx, .LC1[rip]
.LEHB2:
	call	_ZSt20__throw_length_errorPKc
.LEHE2:
.L39:
.L45:
	mov	rsi, rax
	mov	rcx, rbx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	rcx, rsi
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC3915:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC3915-.LLSDACSBC3915
.LLSDACSBC3915:
	.uleb128 .LEHB2-.LCOLDB2
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L39-.LCOLDB2
	.uleb128 0
	.uleb128 .LEHB3-.LCOLDB2
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSEC3915:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE2:
	.text
.LHOTE2:
	.align 2
	.p2align 4
	.def	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEaSERKS2_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEaSERKS2_.isra.0
_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEaSERKS2_.isra.0:
.LFB4833:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, rcx
	cmp	QWORD PTR [rcx], rdx
	je	.L47
	test	rdx, rdx
	je	.L49
	lock add	DWORD PTR 8[rdx], 1
.L49:
	mov	rcx, QWORD PTR [rax]
	test	rcx, rcx
	je	.L50
	mov	QWORD PTR 56[rsp], rdx
	mov	QWORD PTR 48[rsp], rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	rdx, QWORD PTR 56[rsp]
	mov	rax, QWORD PTR 48[rsp]
.L50:
	mov	QWORD PTR [rax], rdx
.L47:
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB4:
	.text
.LHOTB4:
	.p2align 4
	.def	_ZN12_GLOBAL__N_1L9run_cycleEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_1L9run_cycleEv
_ZN12_GLOBAL__N_1L9run_cycleEv:
.LFB3911:
	push	r14
	.seh_pushreg	r14
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
	mov	ecx, 32
	lea	r14, _ZTVSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE[rip+16]
.LEHB4:
	call	_Znwy
.LEHE4:
	mov	rdi, QWORD PTR .LC0[rip]
	pxor	xmm0, xmm0
	mov	ecx, 32
	mov	QWORD PTR [rax], r14
	mov	rbx, rax
	lea	rbp, 16[rax]
	mov	QWORD PTR 8[rax], rdi
	movups	XMMWORD PTR 16[rax], xmm0
	mov	eax, DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_ctorE[rip]
	add	eax, 1
	mov	DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_ctorE[rip], eax
.LEHB5:
	call	_Znwy
.LEHE5:
	pxor	xmm0, xmm0
	mov	rsi, rax
	mov	QWORD PTR 8[rax], rdi
	lea	rcx, 24[rbx]
	movups	XMMWORD PTR 16[rax], xmm0
	mov	rdx, rsi
	mov	QWORD PTR [rax], r14
	mov	eax, DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_ctorE[rip]
	add	eax, 1
	mov	DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_ctorE[rip], eax
	lea	rax, 16[rsi]
	mov	QWORD PTR 16[rbx], rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEaSERKS2_.isra.0
	mov	QWORD PTR 16[rsi], rbp
	lea	rcx, 24[rsi]
	mov	rdx, rbx
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEaSERKS2_.isra.0
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	rcx, rbx
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r14
.LEHB6:
	jmp	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.LEHE6:
.L59:
	mov	rsi, rax
	jmp	.L58
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3911:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3911-.LLSDACSB3911
.LLSDACSB3911:
	.uleb128 .LEHB4-.LFB3911
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB5-.LFB3911
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L59-.LFB3911
	.uleb128 0
	.uleb128 .LEHB6-.LFB3911
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSE3911:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZN12_GLOBAL__N_1L9run_cycleEv.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_1L9run_cycleEv.cold
	.seh_stackalloc	72
	.seh_savereg	rbx, 32
	.seh_savereg	rsi, 40
	.seh_savereg	rdi, 48
	.seh_savereg	rbp, 56
	.seh_savereg	r14, 64
	.seh_endprologue
_ZN12_GLOBAL__N_1L9run_cycleEv.cold:
.L58:
	mov	rcx, rbx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	rcx, rsi
.LEHB7:
	call	_Unwind_Resume
	nop
.LEHE7:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC3911:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC3911-.LLSDACSBC3911
.LLSDACSBC3911:
	.uleb128 .LEHB7-.LCOLDB4
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSEC3911:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE4:
	.text
.LHOTE4:
	.section .rdata,"dr"
.LC5:
	.ascii "scoped_dtor_count=%d\12\0"
.LC6:
	.ascii "cycle_dtor_count=%d\12\0"
.LC7:
	.ascii "owned_dtor_count=%d\12\0"
.LC8:
	.ascii "owned_registry_size=%zu\12\0"
.LC9:
	.ascii "scoped_is_clean=%d\12\0"
.LC10:
	.ascii "cycle_allocated=%d\12\0"
.LC11:
	.ascii "cycle_destroyed=%d\12\0"
.LC12:
	.ascii "cycle_live_objects=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3922:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	call	_ZN12_GLOBAL__N_1L10run_scopedEv
	call	_ZN12_GLOBAL__N_1L9run_cycleEv
	call	_ZN12_GLOBAL__N_1L9run_ownedEv
	mov	edx, DWORD PTR _ZN12_GLOBAL__N_1L13g_scoped_dtorE[rip]
	lea	rcx, .LC5[rip]
	call	__mingw_printf
	mov	edx, DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_dtorE[rip]
	lea	rcx, .LC6[rip]
	call	__mingw_printf
	mov	edx, DWORD PTR _ZN12_GLOBAL__N_1L12g_owned_dtorE[rip]
	lea	rcx, .LC7[rip]
	call	__mingw_printf
	call	_ZN12_GLOBAL__N_1L8registryEv
	lea	rcx, .LC8[rip]
	mov	rdx, QWORD PTR 8[rax]
	sub	rdx, QWORD PTR [rax]
	sar	rdx, 4
	call	__mingw_printf
	mov	eax, DWORD PTR _ZN12_GLOBAL__N_1L13g_scoped_dtorE[rip]
	xor	edx, edx
	lea	rcx, .LC9[rip]
	cmp	eax, 1
	sete	dl
	call	__mingw_printf
	mov	edx, DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_ctorE[rip]
	lea	rcx, .LC10[rip]
	call	__mingw_printf
	mov	edx, DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_dtorE[rip]
	lea	rcx, .LC11[rip]
	call	__mingw_printf
	mov	edx, DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_ctorE[rip]
	mov	eax, DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_dtorE[rip]
	lea	rcx, .LC12[rip]
	sub	edx, eax
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.text
	.p2align 4
	.def	__tcf_ZZN12_GLOBAL__N_1L8registryEvE1r;	.scl	3;	.type	32;	.endef
	.seh_proc	__tcf_ZZN12_GLOBAL__N_1L8registryEvE1r
__tcf_ZZN12_GLOBAL__N_1L8registryEvE1r:
.LFB3909:
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
	mov	rdi, QWORD PTR _ZZN12_GLOBAL__N_1L8registryEvE1r[rip+8]
	mov	rbx, QWORD PTR _ZZN12_GLOBAL__N_1L8registryEvE1r[rip]
	cmp	rdi, rbx
	je	.L62
	movabs	rbp, 4294967297
	jmp	.L67
	.p2align 4,,10
	.p2align 3
.L65:
	lock sub	DWORD PTR [rax], 1
	je	.L73
.L64:
	add	rbx, 16
	cmp	rdi, rbx
	je	.L74
.L67:
	mov	rsi, QWORD PTR 8[rbx]
	test	rsi, rsi
	je	.L64
	mov	rdx, QWORD PTR 8[rsi]
	lea	rax, 8[rsi]
	cmp	rdx, rbp
	jne	.L65
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	mov	QWORD PTR 8[rsi], 0
	add	rbx, 16
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR [rsi]
	mov	rcx, rsi
	call	[QWORD PTR 24[rax]]
	cmp	rdi, rbx
	jne	.L67
	.p2align 4
	.p2align 3
.L74:
	mov	rbx, QWORD PTR _ZZN12_GLOBAL__N_1L8registryEvE1r[rip]
.L62:
	test	rbx, rbx
	je	.L61
	mov	rdx, QWORD PTR _ZZN12_GLOBAL__N_1L8registryEvE1r[rip+16]
	mov	rcx, rbx
	sub	rdx, rbx
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L61:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L73:
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	jmp	.L64
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:
.LFB4808:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	eax, DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_dtorE[rip]
	mov	rcx, QWORD PTR 24[rcx]
	add	eax, 1
	mov	DWORD PTR _ZN12_GLOBAL__N_1L12g_cycle_dtorE[rip], eax
	test	rcx, rcx
	je	.L75
	mov	r8, QWORD PTR 8[rcx]
	lea	rax, 8[rcx]
	movabs	rdx, 4294967297
	cmp	r8, rdx
	je	.L83
	lock sub	DWORD PTR [rax], 1
	je	.L84
.L75:
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L83:
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
.L84:
	add	rsp, 56
	jmp	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
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
	.section .rdata,"dr"
	.align 8
_ZTISt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.align 32
_ZTSSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "*St23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE\0"
	.align 8
_ZTISt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.align 32
_ZTSSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "*St23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE\0"
	.align 8
_ZTVSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	0
	.quad	_ZTISt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_14NodeESaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.align 8
_ZTVSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	0
	.quad	_ZTISt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIN12_GLOBAL__N_15OwnedESaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
.lcomm _ZGVZN12_GLOBAL__N_1L8registryEvE1r,8,8
.lcomm _ZZN12_GLOBAL__N_1L8registryEvE1r,24,16
.lcomm _ZN12_GLOBAL__N_1L12g_cycle_ctorE,4,4
.lcomm _ZN12_GLOBAL__N_1L12g_owned_dtorE,4,4
.lcomm _ZN12_GLOBAL__N_1L12g_cycle_dtorE,4,4
.lcomm _ZN12_GLOBAL__N_1L13g_scoped_dtorE,4,4
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
	.def	__cxa_guard_acquire;	.scl	2;	.type	32;	.endef
	.def	atexit;	.scl	2;	.type	32;	.endef
	.def	__cxa_guard_release;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
