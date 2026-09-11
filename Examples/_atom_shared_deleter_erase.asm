	.file	"_atom_shared_deleter_erase.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED1Ev
	.def	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED1Ev
_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED1Ev:
.LFB4479:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.def	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev:
.LFB4483:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:
.LFB4485:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.def	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev:
.LFB4490:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.def	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:
.LFB4497:
	.seh_endprologue
	xor	eax, eax
	ret
	.seh_endproc
	.section	.text$_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.def	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:
.LFB4495:
	.seh_endprologue
	mov	rcx, QWORD PTR 16[rcx]
	test	rcx, rcx
	je	.L7
	jmp	free
	.p2align 4,,10
	.p2align 3
.L7:
	ret
	.seh_endproc
	.section	.text$_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED0Ev
	.def	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED0Ev
_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED0Ev:
.LFB4480:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section	.text$_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.def	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:
.LFB4496:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.def	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev:
.LFB4484:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section	.text$_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.def	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev:
.LFB4491:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:
.LFB4486:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section	.text$_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.def	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:
.LFB4493:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.def	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:
.LFB4487:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rax, _ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag[rip]
	mov	r8, rcx
	mov	rcx, rdx
	cmp	rdx, rax
	je	.L18
	lea	rax, _ZTSSt19_Sp_make_shared_tag[rip]
	cmp	QWORD PTR 8[rdx], rax
	je	.L18
	lea	rdx, _ZTISt19_Sp_make_shared_tag[rip]
	mov	QWORD PTR 48[rsp], r8
	call	_ZNKSt9type_info7__equalERKS_
	mov	r8, QWORD PTR 48[rsp]
	test	al, al
	je	.L19
.L18:
	lea	rax, 16[r8]
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text$_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.def	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:
.LFB4494:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rax, _ZTS6TagDel[rip]
	mov	rbx, rcx
	mov	rcx, rdx
	cmp	QWORD PTR 8[rdx], rax
	je	.L23
	lea	rdx, _ZTI6TagDel[rip]
	call	_ZNKSt9type_info7__equalERKS_
	test	al, al
	je	.L24
.L23:
	lea	rax, 16[rbx]
	add	rsp, 32
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L24:
	xor	eax, eax
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPi6TagDelSaIvEvEET_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPi6TagDelSaIvEvEET_T0_T1_.isra.0
_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPi6TagDelSaIvEvEET_T0_T1_.isra.0:
.LFB4510:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	mov	rbx, rcx
	mov	ecx, 32
	mov	rsi, rdx
	mov	edi, r8d
	call	malloc
	mov	rdx, QWORD PTR .LC0[rip]
	lea	rcx, _ZTVSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	QWORD PTR [rax], rcx
	mov	QWORD PTR 8[rax], rdx
	mov	DWORD PTR 16[rax], edi
	mov	QWORD PTR 24[rax], rsi
	mov	QWORD PTR [rbx], rax
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_.isra.0
_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_.isra.0:
.LFB4511:
	.seh_endprologue
	mov	QWORD PTR [rcx], rdx
	test	rdx, rdx
	je	.L26
	lock add	DWORD PTR 8[rdx], 1
.L26:
	ret
	.seh_endproc
	.section	.text$_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.def	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:
.LFB4492:
	.seh_endprologue
	mov	eax, DWORD PTR _ZL15g_deleter_calls[rip]
	mov	rdx, QWORD PTR 24[rcx]
	mov	ecx, DWORD PTR 16[rcx]
	add	eax, 1
	mov	DWORD PTR _ZL15g_deleter_calls[rip], eax
	mov	DWORD PTR _ZL10g_tag_seen[rip], ecx
	test	rdx, rdx
	je	.L31
	mov	rcx, rdx
	jmp	free
	.p2align 4,,10
	.p2align 3
.L31:
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB3551:
	.seh_endprologue
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdlPv
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPv
_ZdlPv:
.LFB3552:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB3553:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv:
.LFB3897:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rcx
	call	[QWORD PTR 16[rax]]
	lock sub	DWORD PTR 12[rbx], 1
	jne	.L36
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	mov	rax, QWORD PTR 24[rax]
	add	rsp, 32
	pop	rbx
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L36:
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
	je	.L41
	lock sub	DWORD PTR [rax], 1
	je	.L42
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L41:
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
.L42:
	add	rsp, 56
	jmp	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	.seh_endproc
	.section	.text$_ZNSt12__shared_ptrIiLN9__gnu_cxx12_Lock_policyE2EE5resetEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12__shared_ptrIiLN9__gnu_cxx12_Lock_policyE2EE5resetEv
	.def	_ZNSt12__shared_ptrIiLN9__gnu_cxx12_Lock_policyE2EE5resetEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12__shared_ptrIiLN9__gnu_cxx12_Lock_policyE2EE5resetEv
_ZNSt12__shared_ptrIiLN9__gnu_cxx12_Lock_policyE2EE5resetEv:
.LFB3925:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	pxor	xmm0, xmm0
	mov	rax, rcx
	mov	rcx, QWORD PTR 8[rcx]
	movups	XMMWORD PTR [rax], xmm0
	test	rcx, rcx
	je	.L43
	mov	r8, QWORD PTR 8[rcx]
	lea	rax, 8[rcx]
	movabs	rdx, 4294967297
	cmp	r8, rdx
	je	.L51
	lock sub	DWORD PTR [rax], 1
	je	.L52
.L43:
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L51:
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
.L52:
	add	rsp, 56
	jmp	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	.seh_endproc
	.section	.text$_ZNSt10unique_ptrIi6TagDelED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrIi6TagDelED1Ev
	.def	_ZNSt10unique_ptrIi6TagDelED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrIi6TagDelED1Ev
_ZNSt10unique_ptrIi6TagDelED1Ev:
.LFB3940:
	.seh_endprologue
	mov	rax, rcx
	mov	rcx, QWORD PTR 8[rcx]
	test	rcx, rcx
	je	.L53
	mov	edx, DWORD PTR [rax]
	mov	eax, DWORD PTR _ZL15g_deleter_calls[rip]
	add	eax, 1
	mov	DWORD PTR _ZL15g_deleter_calls[rip], eax
	mov	DWORD PTR _ZL10g_tag_seen[rip], edx
	jmp	free
	.p2align 4,,10
	.p2align 3
.L53:
	ret
	.seh_endproc
	.section	.text$_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPiEET_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPiEET_
	.def	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPiEET_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPiEET_
_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPiEET_:
.LFB4308:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	mov	rbx, rcx
	mov	ecx, 24
	mov	rsi, rdx
	call	malloc
	mov	rdx, QWORD PTR .LC0[rip]
	lea	rcx, _ZTVSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	QWORD PTR [rax], rcx
	mov	QWORD PTR 8[rax], rdx
	mov	QWORD PTR 16[rax], rsi
	mov	QWORD PTR [rbx], rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "sizeof shared_ptr default=%d\12\0"
	.align 8
.LC2:
	.ascii "sizeof shared_ptr with stateful deleter=%d\12\0"
.LC3:
	.ascii "shared_ptr sizes equal=%d\12\0"
.LC4:
	.ascii "deleter copies on ctor=%d\12\0"
.LC5:
	.ascii "deleter copies on share=%d\12\0"
	.align 8
.LC6:
	.ascii "deleter calls after all reset=%d\12\0"
.LC7:
	.ascii "deleter tag seen=%d\12\0"
	.align 8
.LC8:
	.ascii "shared_ptr from raw ptr allocs=%d\12\0"
.LC9:
	.ascii "make_shared allocs=%d\12\0"
.LC10:
	.ascii "unique_ptr allocs=%d\12\0"
.LC11:
	.ascii "tag seen after reset #1=%d\12\0"
.LC12:
	.ascii "tag seen after reset #2=%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB14:
	.section	.text.startup,"x"
.LHOTB14:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3564:
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
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	call	__main
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	mov	ecx, 4
	lea	rbp, 56[rsp]
	lea	rbx, 72[rsp]
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	call	malloc
	mov	rcx, rbp
	mov	DWORD PTR [rax], 1
	mov	rdx, rax
	mov	QWORD PTR 48[rsp], rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPiEET_
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	mov	ecx, 4
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	call	malloc
	mov	rcx, rbx
	mov	r8d, 5
	mov	DWORD PTR [rax], 2
	mov	rdx, rax
	mov	QWORD PTR 64[rsp], rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPi6TagDelSaIvEvEET_T0_T1_.isra.0
	mov	edx, 16
	lea	rcx, .LC1[rip]
.LEHB0:
	call	__mingw_printf
	mov	edx, 16
	lea	rcx, .LC2[rip]
	call	__mingw_printf
	mov	edx, 1
	lea	rcx, .LC3[rip]
	call	__mingw_printf
.LEHE0:
	mov	rcx, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L57
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L57:
	mov	rcx, QWORD PTR 56[rsp]
	test	rcx, rcx
	je	.L58
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L58:
	mov	r13d, DWORD PTR _ZL16g_deleter_copies[rip]
	mov	r12d, DWORD PTR _ZL15g_deleter_calls[rip]
	mov	ecx, 4
	mov	eax, DWORD PTR _ZL16g_deleter_copies[rip]
	add	eax, 1
	mov	DWORD PTR _ZL16g_deleter_copies[rip], eax
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	call	malloc
	lea	rcx, 40[rsp]
	mov	r8d, 99
	mov	DWORD PTR [rax], 3
	mov	rdx, rax
	mov	rsi, rax
	mov	QWORD PTR 32[rsp], rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPi6TagDelSaIvEvEET_T0_T1_.isra.0
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, rbp
	mov	QWORD PTR 48[rsp], rsi
	mov	edi, DWORD PTR _ZL16g_deleter_copies[rip]
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_.isra.0
	mov	rax, QWORD PTR 32[rsp]
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, rbx
	mov	QWORD PTR 64[rsp], rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_.isra.0
	mov	edx, edi
	lea	rcx, .LC4[rip]
	mov	esi, DWORD PTR _ZL16g_deleter_copies[rip]
	sub	edx, r13d
.LEHB1:
	call	__mingw_printf
	sub	esi, edi
	lea	rcx, .LC5[rip]
	mov	edx, esi
	call	__mingw_printf
	lea	rcx, 32[rsp]
	lea	rdi, 48[rsp]
	call	_ZNSt12__shared_ptrIiLN9__gnu_cxx12_Lock_policyE2EE5resetEv
	mov	rcx, rdi
	call	_ZNSt12__shared_ptrIiLN9__gnu_cxx12_Lock_policyE2EE5resetEv
	lea	rcx, 64[rsp]
	call	_ZNSt12__shared_ptrIiLN9__gnu_cxx12_Lock_policyE2EE5resetEv
	mov	edx, DWORD PTR _ZL15g_deleter_calls[rip]
	lea	rcx, .LC6[rip]
	sub	edx, r12d
	call	__mingw_printf
	mov	edx, DWORD PTR _ZL10g_tag_seen[rip]
	lea	rcx, .LC7[rip]
	call	__mingw_printf
.LEHE1:
	mov	rcx, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L59
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L59:
	mov	rcx, QWORD PTR 56[rsp]
	test	rcx, rcx
	je	.L60
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L60:
	mov	rcx, QWORD PTR 40[rsp]
	test	rcx, rcx
	je	.L61
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L61:
	mov	r13d, DWORD PTR _ZL9g_obj_new[rip]
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	mov	ecx, 4
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	call	malloc
	mov	rcx, rbp
	mov	DWORD PTR [rax], 4
	mov	rdx, rax
	mov	rsi, rax
	mov	QWORD PTR 48[rsp], rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPiEET_
	mov	rdx, QWORD PTR 56[rsp]
	mov	rcx, rbx
	mov	QWORD PTR 64[rsp], rsi
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_.isra.0
	mov	rcx, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L62
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L62:
	mov	rcx, QWORD PTR 56[rsp]
	test	rcx, rcx
	je	.L63
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L63:
	mov	r12d, DWORD PTR _ZL9g_obj_new[rip]
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	mov	ecx, 24
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	call	malloc
	mov	rcx, rbx
	mov	rsi, rax
	mov	rax, QWORD PTR .LC0[rip]
	mov	DWORD PTR 16[rsi], 5
	mov	rdx, rsi
	mov	QWORD PTR 8[rsi], rax
	lea	rax, _ZTVSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	QWORD PTR [rsi], rax
	lea	rax, 16[rsi]
	mov	QWORD PTR 64[rsp], rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_.isra.0
	mov	rcx, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L64
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L64:
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	ebp, DWORD PTR _ZL9g_obj_new[rip]
	mov	ecx, 4
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	call	malloc
	lea	rcx, 64[rsp]
	mov	DWORD PTR [rax], 6
	mov	QWORD PTR 72[rsp], rax
	mov	DWORD PTR 48[rsp], 7
	mov	DWORD PTR 64[rsp], 7
	mov	QWORD PTR 56[rsp], 0
	call	_ZNSt10unique_ptrIi6TagDelED1Ev
	mov	rcx, rdi
	call	_ZNSt10unique_ptrIi6TagDelED1Ev
	mov	edx, r12d
	mov	esi, DWORD PTR _ZL9g_obj_new[rip]
	lea	rcx, .LC8[rip]
	sub	edx, r13d
.LEHB2:
	call	__mingw_printf
	mov	edx, ebp
	lea	rcx, .LC9[rip]
	sub	esi, ebp
	sub	edx, r12d
	call	__mingw_printf
	mov	edx, esi
	lea	rcx, .LC10[rip]
	call	__mingw_printf
.LEHE2:
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	mov	ecx, 4
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	call	malloc
	mov	r8d, 11
	mov	rcx, rbx
	mov	DWORD PTR [rax], 8
	mov	rdx, rax
	mov	rsi, rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPi6TagDelSaIvEvEET_T0_T1_.isra.0
	mov	rcx, rdi
	movq	xmm0, rsi
	movhps	xmm0, QWORD PTR 72[rsp]
	movaps	XMMWORD PTR 48[rsp], xmm0
	call	_ZNSt12__shared_ptrIiLN9__gnu_cxx12_Lock_policyE2EE5resetEv
	mov	edx, DWORD PTR _ZL10g_tag_seen[rip]
	lea	rcx, .LC11[rip]
.LEHB3:
	call	__mingw_printf
	mov	eax, DWORD PTR _ZL9g_obj_new[rip]
	mov	ecx, 4
	add	eax, 1
	mov	DWORD PTR _ZL9g_obj_new[rip], eax
	call	malloc
	mov	rcx, rbx
	mov	r8d, 22
	mov	DWORD PTR [rax], 9
	mov	rdx, rax
	mov	rsi, rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1IPi6TagDelSaIvEvEET_T0_T1_.isra.0
	mov	rcx, QWORD PTR 56[rsp]
	pxor	xmm1, xmm1
	movq	xmm0, rsi
	movhps	xmm0, QWORD PTR 72[rsp]
	movaps	XMMWORD PTR 64[rsp], xmm1
	movaps	XMMWORD PTR 48[rsp], xmm0
	test	rcx, rcx
	je	.L66
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	rcx, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L66
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L66:
	mov	rcx, rdi
	call	_ZNSt12__shared_ptrIiLN9__gnu_cxx12_Lock_policyE2EE5resetEv
	mov	edx, DWORD PTR _ZL10g_tag_seen[rip]
	lea	rcx, .LC12[rip]
	call	__mingw_printf
.LEHE3:
	mov	rcx, QWORD PTR 56[rsp]
	test	rcx, rcx
	je	.L97
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L97:
	xor	eax, eax
	add	rsp, 80
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
.L78:
	mov	rbx, rax
	jmp	.L69
.L80:
	mov	rbx, rax
	jmp	.L76
.L79:
	mov	rbx, rax
	jmp	.L72
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3564:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3564-.LLSDACSB3564
.LLSDACSB3564:
	.uleb128 .LEHB0-.LFB3564
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L78-.LFB3564
	.uleb128 0
	.uleb128 .LEHB1-.LFB3564
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L79-.LFB3564
	.uleb128 0
	.uleb128 .LEHB2-.LFB3564
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB3-.LFB3564
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L80-.LFB3564
	.uleb128 0
.LLSDACSE3564:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	136
	.seh_savereg	rbx, 80
	.seh_savereg	rsi, 88
	.seh_savereg	rdi, 96
	.seh_savereg	rbp, 104
	.seh_savereg	r12, 112
	.seh_savereg	r13, 120
	.seh_savereg	r14, 128
	.seh_endprologue
main.cold:
.L69:
	mov	rcx, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L70
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L70:
	mov	rcx, QWORD PTR 56[rsp]
	test	rcx, rcx
	je	.L71
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L71:
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
.L76:
	mov	rcx, QWORD PTR 56[rsp]
	test	rcx, rcx
	je	.L77
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L77:
	mov	rcx, rbx
	call	_Unwind_Resume
.L72:
	mov	rcx, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L73
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L73:
	mov	rcx, QWORD PTR 56[rsp]
	test	rcx, rcx
	je	.L74
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L74:
	mov	rcx, QWORD PTR 40[rsp]
	test	rcx, rcx
	je	.L75
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L75:
	mov	rcx, rbx
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC3564:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC3564-.LLSDACSBC3564
.LLSDACSBC3564:
	.uleb128 .LEHB4-.LCOLDB14
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSEC3564:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE14:
	.section	.text.startup,"x"
.LHOTE14:
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
	.globl	_ZTS6TagDel
	.section	.rdata$_ZTS6TagDel,"dr"
	.linkonce same_size
	.align 8
_ZTS6TagDel:
	.ascii "6TagDel\0"
	.globl	_ZTI6TagDel
	.section	.rdata$_ZTI6TagDel,"dr"
	.linkonce same_size
	.align 8
_ZTI6TagDel:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS6TagDel
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
	.globl	_ZTSSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTSSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 32
_ZTSSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "St15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE\0"
	.globl	_ZTISt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTISt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTISt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.globl	_ZTSSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTSSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 32
_ZTSSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "St19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE\0"
	.globl	_ZTISt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTISt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTISt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.globl	_ZTSSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTSSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 32
_ZTSSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "St23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE\0"
	.globl	_ZTISt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTISt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTISt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.globl	_ZTVSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTVSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTVSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE:
	.quad	0
	.quad	_ZTISt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED1Ev
	.quad	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EED0Ev
	.quad	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.quad	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.quad	_ZNSt15_Sp_counted_ptrIPiLN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.globl	_ZTVSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTVSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTVSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	0
	.quad	_ZTISt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.quad	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.quad	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.quad	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.quad	_ZNSt19_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.globl	_ZTVSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTVSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTVSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	0
	.quad	_ZTISt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
.lcomm _ZL9g_obj_new,4,4
	.data
	.align 4
_ZL10g_tag_seen:
	.long	-1
.lcomm _ZL15g_deleter_calls,4,4
.lcomm _ZL16g_deleter_copies,4,4
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
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt9type_info7__equalERKS_;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
