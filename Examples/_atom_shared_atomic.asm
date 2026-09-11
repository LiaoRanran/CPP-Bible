	.file	"_atom_shared_atomic.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB3768:
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
.LFB7578:
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
.LFB7580:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.def	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev:
.LFB7579:
	.seh_endprologue
	mov	edx, 24
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.def	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:
.LFB7582:
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
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
_ZNSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:
.LFB7581:
	.seh_endprologue
	mov	edx, 24
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
.LFB6207:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rcx
	call	[QWORD PTR 16[rax]]
	lock sub	DWORD PTR 12[rbx], 1
	jne	.L12
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	mov	rax, QWORD PTR 24[rax]
	add	rsp, 32
	pop	rbx
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L12:
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
	je	.L17
	lock sub	DWORD PTR [rax], 1
	je	.L18
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L17:
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
.L18:
	add	rsp, 56
	jmp	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv:
.LFB7575:
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
	mov	esi, 2000
	movabs	rbp, 4294967297
	mov	rdi, rcx
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L22:
	lock sub	DWORD PTR [rax], 1
	je	.L29
.L21:
	sub	esi, 1
	je	.L30
.L24:
	mov	rbx, QWORD PTR 16[rdi]
	test	rbx, rbx
	je	.L21
	lea	rax, 8[rbx]
	lock add	DWORD PTR 8[rbx], 1
	mov	rdx, QWORD PTR 8[rbx]
	cmp	rdx, rbp
	jne	.L22
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	mov	QWORD PTR 8[rbx], 0
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	call	[QWORD PTR 24[rax]]
	sub	esi, 1
	jne	.L24
.L30:
	mov	rax, QWORD PTR 32[rdi]
	movsxd	rdx, DWORD PTR 40[rdi]
	mov	rax, QWORD PTR [rax]
	mov	DWORD PTR [rax+rdx*4], 2000
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L29:
	mov	rcx, rbx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	jmp	.L21
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev:
.LFB7572:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rdx, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rdx
	mov	rax, rcx
	mov	rcx, QWORD PTR 16[rcx]
	test	rcx, rcx
	je	.L33
	mov	r9, QWORD PTR 8[rcx]
	lea	rdx, 8[rcx]
	movabs	r8, 4294967297
	cmp	r9, r8
	je	.L39
	lock sub	DWORD PTR [rdx], 1
	je	.L40
.L33:
	mov	rcx, rax
	add	rsp, 56
	jmp	_ZNSt6thread6_StateD2Ev
	.p2align 4,,10
	.p2align 3
.L39:
	mov	rdx, QWORD PTR [rcx]
	mov	QWORD PTR 40[rsp], rax
	mov	QWORD PTR 32[rsp], rcx
	mov	QWORD PTR 8[rcx], 0
	call	[QWORD PTR 16[rdx]]
	mov	rcx, QWORD PTR 32[rsp]
	mov	rdx, QWORD PTR [rcx]
	call	[QWORD PTR 24[rdx]]
	mov	rax, QWORD PTR 40[rsp]
	mov	rcx, rax
	add	rsp, 56
	jmp	_ZNSt6thread6_StateD2Ev
	.p2align 4,,10
	.p2align 3
.L40:
	mov	QWORD PTR 32[rsp], rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	mov	rax, QWORD PTR 32[rsp]
	jmp	.L33
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev:
.LFB7574:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	rbx, rcx
	mov	rcx, QWORD PTR 16[rcx]
	test	rcx, rcx
	je	.L43
	mov	r8, QWORD PTR 8[rcx]
	lea	rax, 8[rcx]
	movabs	rdx, 4294967297
	cmp	r8, rdx
	je	.L49
	lock sub	DWORD PTR [rax], 1
	je	.L50
.L43:
	mov	rcx, rbx
	call	_ZNSt6thread6_StateD2Ev
	mov	edx, 48
	mov	rcx, rbx
	add	rsp, 48
	pop	rbx
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L49:
	mov	rax, QWORD PTR [rcx]
	mov	QWORD PTR 40[rsp], rcx
	mov	QWORD PTR 8[rcx], 0
	call	[QWORD PTR 16[rax]]
	mov	rcx, QWORD PTR 40[rsp]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 24[rax]]
	jmp	.L43
	.p2align 4,,10
	.p2align 3
.L50:
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	jmp	.L43
	.seh_endproc
	.section	.text$_ZNSt6vectorISt6threadSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	.def	_ZNSt6vectorISt6threadSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt6threadSaIS0_EED1Ev
_ZNSt6vectorISt6threadSaIS0_EED1Ev:
.LFB6451:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	mov	r8, rcx
	mov	rcx, QWORD PTR [rcx]
	cmp	rdx, rcx
	je	.L52
	mov	rax, rcx
	.p2align 4
	.p2align 4
	.p2align 3
.L54:
	cmp	QWORD PTR [rax], 0
	jne	.L57
	add	rax, 8
	cmp	rdx, rax
	jne	.L54
.L52:
	test	rcx, rcx
	je	.L51
	mov	rdx, QWORD PTR 16[r8]
	sub	rdx, rcx
	add	rsp, 40
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L51:
	add	rsp, 40
	ret
.L57:
	call	_ZSt9terminatev
	nop
	.seh_endproc
	.section	.text$_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	.def	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev:
.LFB7405:
	.seh_endprologue
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L58
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 8[rax]]
	.p2align 4,,10
	.p2align 3
.L58:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "threads=%d iterations=%d\12\0"
.LC1:
	.ascii "sizeof shared_ptr=%d\12\0"
.LC2:
	.ascii "shared_ptr copyable=%d\12\0"
.LC3:
	.ascii "unique_ptr copyable=%d\12\0"
.LC5:
	.ascii "use_count before copies=%ld\12\0"
.LC6:
	.ascii "use_count after one copy=%ld\12\0"
.LC7:
	.ascii "vector::_M_realloc_append\0"
.LC8:
	.ascii "copies observed=%ld\12\0"
.LC9:
	.ascii "use_count after join=%ld\12\0"
.LC10:
	.ascii "value=%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB12:
	.section	.text.startup,"x"
.LHOTB12:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5864:
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
	sub	rsp, 152
	.seh_stackalloc	152
	movaps	XMMWORD PTR 128[rsp], xmm6
	.seh_savexmm	xmm6, 128
	.seh_endprologue
	call	__main
	mov	ecx, 16
.LEHB0:
	call	_Znwy
.LEHE0:
	pxor	xmm0, xmm0
	mov	r8d, 2000
	lea	rcx, .LC0[rip]
	lea	rdx, 16[rax]
	movups	XMMWORD PTR [rax], xmm0
	mov	QWORD PTR 80[rsp], rdx
	mov	QWORD PTR 72[rsp], rdx
	mov	edx, 4
	mov	QWORD PTR 64[rsp], rax
.LEHB1:
	call	__mingw_printf
	mov	edx, 16
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	mov	edx, 1
	lea	rcx, .LC2[rip]
	call	__mingw_printf
	xor	edx, edx
	lea	rcx, .LC3[rip]
	call	__mingw_printf
	mov	ecx, 24
	call	_Znwy
.LEHE1:
	mov	rsi, rax
	lea	r13, 8[rax]
	mov	rax, QWORD PTR .LC4[rip]
	lea	rcx, .LC5[rip]
	mov	DWORD PTR 16[rsi], 42
	lea	r14, 16[rsi]
	mov	QWORD PTR 8[rsi], rax
	lea	rax, _ZTVSt23_Sp_counted_ptr_inplaceIiSaIvELN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	QWORD PTR [rsi], rax
	mov	edx, DWORD PTR 8[rsi]
.LEHB2:
	call	__mingw_printf
.LEHE2:
	lock add	DWORD PTR 8[rsi], 1
	lea	rcx, .LC6[rip]
	mov	edx, DWORD PTR 8[rsi]
.LEHB3:
	call	__mingw_printf
.LEHE3:
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	ecx, 32
.LEHB4:
	call	_Znwy
.LEHE4:
	mov	rbx, rax
	lea	r12, 32[rax]
	mov	rbp, rax
	xor	edi, edi
	lea	rax, 96[rsp]
	movq	xmm1, r14
	lea	r15, 64[rsp]
	mov	QWORD PTR 32[rsp], rax
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE[rip+16]
	movq	xmm6, rax
	lea	rax, _ZNSt6thread24_M_thread_deps_never_runEv[rip]
	mov	QWORD PTR 40[rsp], rax
	punpcklqdq	xmm6, xmm1
.L80:
	lock add	DWORD PTR 0[r13], 1
	cmp	r12, rbx
	je	.L64
	mov	QWORD PTR [rbx], 0
	mov	ecx, 48
.LEHB5:
	call	_Znwy
.LEHE5:
	mov	QWORD PTR 16[rax], rsi
	mov	r8, QWORD PTR 40[rsp]
	mov	rcx, rbx
	mov	DWORD PTR 24[rax], 2000
	mov	rdx, QWORD PTR 32[rsp]
	mov	QWORD PTR 32[rax], r15
	mov	DWORD PTR 40[rax], edi
	movups	XMMWORD PTR [rax], xmm6
	mov	QWORD PTR 96[rsp], rax
.LEHB6:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE6:
	mov	rcx, QWORD PTR 96[rsp]
	add	rbx, 8
	test	rcx, rcx
	je	.L66
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
.L66:
	add	edi, 1
	cmp	edi, 4
	jne	.L80
	mov	rdi, rbp
	cmp	rbp, rbx
	je	.L85
	.p2align 4
	.p2align 3
.L84:
	mov	rcx, rdi
.LEHB7:
	call	_ZNSt6thread4joinEv
	add	rdi, 8
	cmp	rbx, rdi
	jne	.L84
.L85:
	mov	rcx, QWORD PTR 72[rsp]
	mov	rax, QWORD PTR 64[rsp]
	xor	edx, edx
	cmp	rcx, rax
	je	.L83
	.p2align 4
	.p2align 4
	.p2align 3
.L86:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rcx, rax
	jne	.L86
.L83:
	lea	rcx, .LC8[rip]
	call	__mingw_printf
	mov	edx, DWORD PTR 8[rsi]
	lea	rcx, .LC9[rip]
	call	__mingw_printf
	mov	edx, DWORD PTR 16[rsi]
	lea	rcx, .LC10[rip]
	call	__mingw_printf
.LEHE7:
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 96[rsp], rbp
	mov	QWORD PTR 104[rsp], rbx
	mov	QWORD PTR 112[rsp], r12
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	rcx, QWORD PTR 64[rsp]
	test	rcx, rcx
	je	.L106
	mov	rdx, QWORD PTR 80[rsp]
	sub	rdx, rcx
	call	_ZdlPvy
	nop
.L106:
	movaps	xmm6, XMMWORD PTR 128[rsp]
	xor	eax, eax
	add	rsp, 152
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L64:
	movabs	rax, 1152921504606846975
	mov	r9, r12
	sub	r9, rbp
	mov	rdx, r9
	sar	rdx, 3
	cmp	rdx, rax
	je	.L123
	test	rdx, rdx
	mov	eax, 1
	mov	QWORD PTR 56[rsp], r9
	cmovne	rax, rdx
	add	rax, rdx
	movabs	rdx, 1152921504606846975
	cmp	rax, rdx
	cmova	rax, rdx
	sal	rax, 3
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], rax
.LEHB8:
	call	_Znwy
.LEHE8:
	mov	r9, QWORD PTR 56[rsp]
	mov	ecx, 48
	mov	r14, rax
	add	r9, rax
	mov	QWORD PTR [r9], 0
	mov	QWORD PTR 56[rsp], r9
.LEHB9:
	call	_Znwy
.LEHE9:
	mov	QWORD PTR 16[rax], rsi
	mov	r8, QWORD PTR 40[rsp]
	mov	rdx, QWORD PTR 32[rsp]
	mov	rcx, QWORD PTR 56[rsp]
	mov	QWORD PTR 32[rax], r15
	mov	DWORD PTR 24[rax], 2000
	mov	DWORD PTR 40[rax], edi
	movups	XMMWORD PTR [rax], xmm6
	mov	QWORD PTR 96[rsp], rax
.LEHB10:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE10:
	mov	rcx, QWORD PTR 96[rsp]
	test	rcx, rcx
	je	.L71
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
.L71:
	cmp	rbx, rbp
	je	.L125
	mov	r8, rbx
	mov	rdx, rbp
	mov	rax, r14
	sub	r8, rbp
	add	r8, r14
	.p2align 5
	.p2align 4
	.p2align 3
.L76:
	mov	rcx, QWORD PTR [rdx]
	add	rax, 8
	add	rdx, 8
	mov	QWORD PTR -8[rax], rcx
	cmp	rax, r8
	jne	.L76
	sub	rbx, rbp
	lea	rbx, 8[r14+rbx]
	test	rbp, rbp
	je	.L77
.L73:
	mov	rdx, r12
	mov	rcx, rbp
	sub	rdx, rbp
	call	_ZdlPvy
.L77:
	mov	r12, QWORD PTR 48[rsp]
	mov	rbp, r14
	add	r12, r14
	jmp	.L66
.L125:
	lea	rbx, 8[r14]
	jmp	.L73
.L93:
	mov	rbx, rax
	jmp	.L90
.L99:
	mov	rdi, rax
	jmp	.L74
.L98:
	mov	rdi, rax
	jmp	.L78
.L121:
	jmp	.L122
.L96:
	mov	rdi, rax
	jmp	.L63
.L97:
	mov	rdi, rax
	jmp	.L68
.L95:
	mov	rbx, rax
	jmp	.L88
.L94:
	mov	rbx, rax
	jmp	.L89
.L101:
	mov	rdi, rax
	jmp	.L62
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5864:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5864-.LLSDACSB5864
.LLSDACSB5864:
	.uleb128 .LEHB0-.LFB5864
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5864
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L93-.LFB5864
	.uleb128 0
	.uleb128 .LEHB2-.LFB5864
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L94-.LFB5864
	.uleb128 0
	.uleb128 .LEHB3-.LFB5864
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L95-.LFB5864
	.uleb128 0
	.uleb128 .LEHB4-.LFB5864
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L101-.LFB5864
	.uleb128 0
	.uleb128 .LEHB5-.LFB5864
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L121-.LFB5864
	.uleb128 0
	.uleb128 .LEHB6-.LFB5864
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L97-.LFB5864
	.uleb128 0
	.uleb128 .LEHB7-.LFB5864
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L96-.LFB5864
	.uleb128 0
	.uleb128 .LEHB8-.LFB5864
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L121-.LFB5864
	.uleb128 0
	.uleb128 .LEHB9-.LFB5864
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L98-.LFB5864
	.uleb128 0
	.uleb128 .LEHB10-.LFB5864
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L99-.LFB5864
	.uleb128 0
.LLSDACSE5864:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	216
	.seh_savereg	rbx, 152
	.seh_savereg	rsi, 160
	.seh_savereg	rdi, 168
	.seh_savereg	rbp, 176
	.seh_savexmm	xmm6, 128
	.seh_savereg	r12, 184
	.seh_savereg	r13, 192
	.seh_savereg	r14, 200
	.seh_savereg	r15, 208
	.seh_endprologue
main.cold:
.L88:
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L89:
	mov	rcx, rsi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L90:
	mov	rcx, QWORD PTR 64[rsp]
	test	rcx, rcx
	je	.L91
	mov	rdx, QWORD PTR 80[rsp]
	sub	rdx, rcx
	call	_ZdlPvy
.L91:
	mov	rcx, rbx
.LEHB11:
	call	_Unwind_Resume
.LEHE11:
.L74:
	mov	rcx, QWORD PTR 32[rsp]
	xor	r13d, r13d
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
.L75:
	mov	rdx, QWORD PTR 48[rsp]
	mov	rcx, r14
	call	_ZdlPvy
	test	r13, r13
	je	.L63
.L79:
	mov	rcx, r13
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L63:
	mov	rcx, QWORD PTR 32[rsp]
	mov	QWORD PTR 104[rsp], rbx
	mov	rbx, rdi
	mov	QWORD PTR 96[rsp], rbp
	mov	QWORD PTR 112[rsp], r12
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	jmp	.L89
.L123:
	lea	rcx, .LC7[rip]
.LEHB12:
	call	_ZSt20__throw_length_errorPKc
.LEHE12:
.L78:
	mov	r13, rsi
	jmp	.L75
.L100:
.L122:
	mov	rdi, rax
	mov	r13, rsi
	jmp	.L79
.L68:
	mov	rcx, QWORD PTR 32[rsp]
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	jmp	.L63
.L62:
	lea	rax, 96[rsp]
	xor	r12d, r12d
	xor	ebx, ebx
	xor	ebp, ebp
	mov	QWORD PTR 32[rsp], rax
	jmp	.L63
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5864:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5864-.LLSDACSBC5864
.LLSDACSBC5864:
	.uleb128 .LEHB11-.LCOLDB12
	.uleb128 .LEHE11-.LEHB11
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB12-.LCOLDB12
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L100-.LCOLDB12
	.uleb128 0
.LLSDACSEC5864:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE12:
	.section	.text.startup,"x"
.LHOTE12:
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
	.globl	_ZTSNSt6thread6_StateE
	.section	.rdata$_ZTSNSt6thread6_StateE,"dr"
	.linkonce same_size
	.align 16
_ZTSNSt6thread6_StateE:
	.ascii "NSt6thread6_StateE\0"
	.globl	_ZTINSt6thread6_StateE
	.section	.rdata$_ZTINSt6thread6_StateE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt6thread6_StateE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSNSt6thread6_StateE
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
	.section .rdata,"dr"
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE
	.quad	_ZTINSt6thread6_StateE
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE:
	.ascii "*NSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE\0"
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
	.section .rdata,"dr"
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv
	.globl	_ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag
	.section	.rdata$_ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag,"dr"
	.linkonce same_size
	.align 8
_ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag:
	.space 16
	.section .rdata,"dr"
	.align 8
.LC4:
	.long	1
	.long	1
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt9type_info7__equalERKS_;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread4joinEv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
