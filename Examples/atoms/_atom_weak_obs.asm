	.file	"_atom_weak_obs.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.def	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev:
.LFB6327:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:
.LFB6329:
	.seh_endprologue
	mov	eax, DWORD PTR g_destroy[rip]
	add	eax, 1
	mov	DWORD PTR g_destroy[rip], eax
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.def	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:
.LFB6331:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rax, _ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag[rip]
	mov	r8, rcx
	mov	rcx, rdx
	cmp	rdx, rax
	je	.L7
	lea	rax, _ZTSSt19_Sp_make_shared_tag[rip]
	cmp	QWORD PTR 8[rdx], rax
	je	.L7
	lea	rdx, _ZTISt19_Sp_make_shared_tag[rip]
	mov	QWORD PTR 48[rsp], r8
	call	_ZNKSt9type_info7__equalERKS_
	mov	r8, QWORD PTR 48[rsp]
	test	al, al
	je	.L8
.L7:
	lea	rax, 16[r8]
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.def	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev:
.LFB6328:
	.seh_endprologue
	mov	edx, 24
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:
.LFB6330:
	.seh_endprologue
	mov	edx, 24
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNKSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE16_M_get_use_countEv.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNKSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE16_M_get_use_countEv.isra.0
_ZNKSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE16_M_get_use_countEv.isra.0:
.LFB7327:
	.seh_endprologue
	xor	eax, eax
	test	rcx, rcx
	je	.L11
	mov	eax, DWORD PTR 8[rcx]
.L11:
	ret
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv:
.LFB5344:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rcx
	call	[QWORD PTR 16[rax]]
	lock sub	DWORD PTR 12[rbx], 1
	jne	.L15
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	mov	rax, QWORD PTR 24[rax]
	add	rsp, 32
	pop	rbx
	rex.W jmp	rax
	.p2align 4,,10
	.p2align 3
.L15:
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
	je	.L20
	lock sub	DWORD PTR [rax], 1
	je	.L21
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L20:
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
.L21:
	add	rsp, 56
	jmp	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_weak_releaseEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_weak_releaseEv
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_weak_releaseEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_weak_releaseEv
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_weak_releaseEv:
.LFB5720:
	.seh_endprologue
	lock sub	DWORD PTR 12[rcx], 1
	jne	.L22
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 24[rax]]
	.p2align 4,,10
	.p2align 3
.L22:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "use_count with weak=\0"
.LC2:
	.ascii "\12\0"
.LC3:
	.ascii "weak expired before=\0"
.LC4:
	.ascii "use_count after lock=\0"
.LC5:
	.ascii "locked bool=\0"
.LC6:
	.ascii "use_count after lock scope=\0"
.LC7:
	.ascii "weak expired after reset=\0"
.LC8:
	.ascii "box destroyed count=\0"
	.section	.text.unlikely,"x"
.LCOLDB10:
	.section	.text.startup,"x"
.LHOTB10:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5052:
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
	.seh_endprologue
	call	__main
	mov	ecx, 24
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	rbx, rax
	lea	r12, 8[rax]
	mov	rax, QWORD PTR .LC0[rip]
	mov	QWORD PTR 8[rbx], rax
	lea	rax, _ZTVSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	QWORD PTR [rbx], rax
	lock add	DWORD PTR 12[rbx], 1
	mov	rsi, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC1[rip]
	mov	rcx, rsi
.LEHB1:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE1:
	mov	rcx, rbx
	mov	r8, rax
	call	_ZNKSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE16_M_get_use_countEv.isra.0
	mov	rcx, r8
	mov	edx, eax
.LEHB2:
	call	_ZNSo9_M_insertIlEERSoT_
.LEHE2:
	lea	rdx, .LC2[rip]
	mov	rcx, rax
.LEHB3:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE3:
	lea	rdx, .LC3[rip]
	mov	rcx, rsi
.LEHB4:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE4:
	mov	edx, DWORD PTR 8[rbx]
	mov	rcx, rax
	test	edx, edx
	sete	dl
	movzx	edx, dl
.LEHB5:
	call	_ZNSo9_M_insertIbEERSoT_
.LEHE5:
	lea	rdx, .LC2[rip]
	mov	rcx, rax
.LEHB6:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE6:
	mov	eax, DWORD PTR 8[rbx]
.L39:
	test	eax, eax
	je	.L65
	lea	edx, 1[rax]
	lock cmpxchg	DWORD PTR [r12], edx
	jne	.L39
	mov	rbp, rbx
.L38:
	mov	rcx, rbp
	lea	rdi, 16[rbx]
	lea	rdx, .LC4[rip]
	call	_ZNKSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE16_M_get_use_countEv.isra.0
	mov	rcx, rsi
	test	eax, eax
	mov	eax, 0
	cmove	rdi, rax
.LEHB7:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	mov	r8, rax
	call	_ZNKSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE16_M_get_use_countEv.isra.0
	mov	rcx, r8
	mov	edx, eax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC5[rip]
	mov	rcx, rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	edx, edx
	test	rdi, rdi
	mov	rcx, rax
	setne	dl
	call	_ZNSo9_M_insertIbEERSoT_
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE7:
	test	rbp, rbp
	je	.L41
	mov	rcx, rbp
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L41:
	lea	rdx, .LC6[rip]
	mov	rcx, rsi
.LEHB8:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE8:
	mov	rcx, rbx
	mov	r8, rax
	call	_ZNKSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE16_M_get_use_countEv.isra.0
	mov	rcx, r8
	mov	edx, eax
.LEHB9:
	call	_ZNSo9_M_insertIlEERSoT_
.LEHE9:
	lea	rdx, .LC2[rip]
	mov	rcx, rax
.LEHB10:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE10:
	movabs	rax, 4294967297
	mov	rdx, QWORD PTR 8[rbx]
	cmp	rdx, rax
	je	.L109
	lock sub	DWORD PTR [r12], 1
	je	.L110
.L49:
	lea	rdx, .LC7[rip]
	mov	rcx, rsi
.LEHB11:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE11:
	mov	edx, DWORD PTR 8[rbx]
	mov	rcx, rax
	test	edx, edx
	sete	dl
	movzx	edx, dl
.LEHB12:
	call	_ZNSo9_M_insertIbEERSoT_
.LEHE12:
	lea	rdx, .LC2[rip]
	mov	rcx, rax
.LEHB13:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE13:
	lea	rdx, .LC8[rip]
	mov	rcx, rsi
.LEHB14:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE14:
	mov	edx, DWORD PTR g_destroy[rip]
	mov	rcx, rax
.LEHB15:
	call	_ZNSolsEi
.LEHE15:
	lea	rdx, .LC2[rip]
	mov	rcx, rax
.LEHB16:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE16:
	mov	rcx, rbx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_weak_releaseEv
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L109:
	xor	eax, eax
	mov	rcx, rbx
	mov	QWORD PTR 8[rbx], rax
	mov	rax, QWORD PTR [rbx]
	call	[QWORD PTR 16[rax]]
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	call	[QWORD PTR 24[rax]]
	jmp	.L49
.L110:
	mov	rcx, rbx
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	jmp	.L49
.L65:
	xor	ebp, ebp
	jmp	.L38
.L70:
	jmp	.L108
.L76:
	jmp	.L61
.L67:
	mov	rsi, rax
	jmp	.L62
.L71:
	jmp	.L61
.L81:
	jmp	.L108
.L82:
	jmp	.L108
.L80:
	jmp	.L108
.L79:
	jmp	.L108
.L69:
	jmp	.L108
.L78:
	jmp	.L108
.L77:
	jmp	.L108
.L72:
	jmp	.L61
.L73:
	jmp	.L61
.L74:
	jmp	.L61
.L75:
	jmp	.L61
.L68:
	jmp	.L108
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5052:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5052-.LLSDACSB5052
.LLSDACSB5052:
	.uleb128 .LEHB0-.LFB5052
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5052
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L77-.LFB5052
	.uleb128 0
	.uleb128 .LEHB2-.LFB5052
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L78-.LFB5052
	.uleb128 0
	.uleb128 .LEHB3-.LFB5052
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L69-.LFB5052
	.uleb128 0
	.uleb128 .LEHB4-.LFB5052
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L70-.LFB5052
	.uleb128 0
	.uleb128 .LEHB5-.LFB5052
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L80-.LFB5052
	.uleb128 0
	.uleb128 .LEHB6-.LFB5052
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L82-.LFB5052
	.uleb128 0
	.uleb128 .LEHB7-.LFB5052
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L67-.LFB5052
	.uleb128 0
	.uleb128 .LEHB8-.LFB5052
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L81-.LFB5052
	.uleb128 0
	.uleb128 .LEHB9-.LFB5052
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L68-.LFB5052
	.uleb128 0
	.uleb128 .LEHB10-.LFB5052
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L79-.LFB5052
	.uleb128 0
	.uleb128 .LEHB11-.LFB5052
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L76-.LFB5052
	.uleb128 0
	.uleb128 .LEHB12-.LFB5052
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L71-.LFB5052
	.uleb128 0
	.uleb128 .LEHB13-.LFB5052
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L75-.LFB5052
	.uleb128 0
	.uleb128 .LEHB14-.LFB5052
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L74-.LFB5052
	.uleb128 0
	.uleb128 .LEHB15-.LFB5052
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L73-.LFB5052
	.uleb128 0
	.uleb128 .LEHB16-.LFB5052
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L72-.LFB5052
	.uleb128 0
.LLSDACSE5052:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_savereg	rbp, 72
	.seh_savereg	r12, 80
	.seh_endprologue
main.cold:
.L62:
	test	rbp, rbp
	jne	.L111
.L63:
	mov	rax, rsi
.L108:
	mov	rdi, rbx
.L27:
	mov	rcx, rbx
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_weak_releaseEv
	test	rdi, rdi
	mov	rax, QWORD PTR 40[rsp]
	je	.L64
	mov	rcx, rdi
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	mov	rax, QWORD PTR 40[rsp]
.L64:
	mov	rcx, rax
.LEHB17:
	call	_Unwind_Resume
.LEHE17:
.L61:
	xor	edi, edi
	jmp	.L27
.L111:
	mov	rcx, rbp
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	jmp	.L63
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5052:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5052-.LLSDACSBC5052
.LLSDACSBC5052:
	.uleb128 .LEHB17-.LCOLDB10
	.uleb128 .LEHE17-.LEHB17
	.uleb128 0
	.uleb128 0
.LLSDACSEC5052:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE10:
	.section	.text.startup,"x"
.LHOTE10:
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
	.globl	_ZTSSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTSSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 32
_ZTSSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "St23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE\0"
	.globl	_ZTISt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTISt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTISt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.globl	_ZTVSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTVSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTVSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	0
	.quad	_ZTISt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI3BoxSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
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
	.def	_ZNSo9_M_insertIbEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
