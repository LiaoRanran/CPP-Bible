	.file	"_ch137_bridge_layout.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZnwyPv,"x"
	.linkonce discard
	.globl	_ZnwyPv
	.def	_ZnwyPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZnwyPv
_ZnwyPv:
.LFB11:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZdlPvS_,"x"
	.linkonce discard
	.globl	_ZdlPvS_
	.def	_ZdlPvS_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvS_
_ZdlPvS_:
.LFB13:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv:
.LFB2766:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 112
	.seh_stackalloc	112
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	BYTE PTR -1[rbp], 1
	mov	BYTE PTR -2[rbp], 1
	mov	BYTE PTR -3[rbp], 1
	mov	DWORD PTR -8[rbp], 32
	mov	DWORD PTR -12[rbp], 32
	movabs	rax, 4294967297
	mov	QWORD PTR -24[rbp], rax
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	QWORD PTR -32[rbp], rax
	mov	rax, QWORD PTR -32[rbp]
	mov	rdx, QWORD PTR [rax]
	movabs	rax, 4294967297
	cmp	rdx, rax
	sete	al
	test	al, al
	je	.L5
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR 8[rax], 0
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, DWORD PTR 8[rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR 12[rax], edx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	add	rax, 16
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	add	rax, 24
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
	jmp	.L4
.L5:
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	QWORD PTR -40[rbp], rax
	mov	DWORD PTR -44[rbp], -1
	mov	eax, 1
	test	eax, eax
	sete	al
	test	al, al
	je	.L9
	mov	rax, QWORD PTR -40[rbp]
	mov	QWORD PTR -56[rbp], rax
	mov	eax, DWORD PTR -44[rbp]
	mov	DWORD PTR -60[rbp], eax
	mov	rax, QWORD PTR -56[rbp]
	mov	eax, DWORD PTR [rax]
	mov	DWORD PTR -64[rbp], eax
	mov	rax, QWORD PTR -56[rbp]
	mov	edx, DWORD PTR [rax]
	mov	eax, DWORD PTR -60[rbp]
	add	edx, eax
	mov	rax, QWORD PTR -56[rbp]
	mov	DWORD PTR [rax], edx
	mov	eax, DWORD PTR -64[rbp]
	jmp	.L11
.L9:
	mov	rax, QWORD PTR -40[rbp]
	mov	QWORD PTR -72[rbp], rax
	mov	eax, DWORD PTR -44[rbp]
	mov	DWORD PTR -76[rbp], eax
	mov	edx, DWORD PTR -76[rbp]
	mov	rax, QWORD PTR -72[rbp]
	lock xadd	DWORD PTR [rax], edx
	mov	eax, edx
	nop
.L11:
	cmp	eax, 1
	sete	al
	test	al, al
	je	.L4
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	nop
.L4:
	add	rsp, 112
	pop	rbp
	ret
	.seh_endproc
	.globl	_ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag
	.section	.rdata$_ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag,"dr"
	.linkonce same_size
	.align 8
_ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag:
	.space 16
	.section	.text$_ZNSt19_Sp_make_shared_tag5_S_tiEv,"x"
	.linkonce discard
	.globl	_ZNSt19_Sp_make_shared_tag5_S_tiEv
	.def	_ZNSt19_Sp_make_shared_tag5_S_tiEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_Sp_make_shared_tag5_S_tiEv
_ZNSt19_Sp_make_shared_tag5_S_tiEv:
.LFB2792:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	lea	rax, _ZZNSt19_Sp_make_shared_tag5_S_tiEvE5__tag[rip]
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK14VectorRenderer6renderEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK14VectorRenderer6renderEv
	.def	_ZNK14VectorRenderer6renderEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK14VectorRenderer6renderEv
_ZNK14VectorRenderer6renderEv:
.LFB3495:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EED2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EED2Ev
	.def	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EED2Ev
_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EED2Ev:
.LFB3499:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	rcx, rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EED1Ev
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt10shared_ptrI8RendererED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt10shared_ptrI8RendererED1Ev
	.def	_ZNSt10shared_ptrI8RendererED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10shared_ptrI8RendererED1Ev
_ZNSt10shared_ptrI8RendererED1Ev:
.LFB3502:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EED2Ev
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN5ShapeC1ESt10shared_ptrI8RendererE,"x"
	.linkonce discard
	.align 2
	.globl	_ZN5ShapeC1ESt10shared_ptrI8RendererE
	.def	_ZN5ShapeC1ESt10shared_ptrI8RendererE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN5ShapeC1ESt10shared_ptrI8RendererE
_ZN5ShapeC1ESt10shared_ptrI8RendererE:
.LFB3504:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR -8[rbp], rdx
	mov	rdx, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZNSt10shared_ptrI8RendererEC1EOS1_
	nop
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK5Shape4drawEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK5Shape4drawEv
	.def	_ZNK5Shape4drawEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK5Shape4drawEv
_ZNK5Shape4drawEv:
.LFB3505:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EEptEv
	mov	rdx, QWORD PTR [rax]
	add	rdx, 16
	mov	rdx, QWORD PTR [rdx]
	mov	rcx, rax
	call	rdx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EED2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EED2Ev
	.def	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EED2Ev
_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EED2Ev:
.LFB3509:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	rcx, rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EED1Ev
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt10shared_ptrI14VectorRendererED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt10shared_ptrI14VectorRendererED1Ev
	.def	_ZNSt10shared_ptrI14VectorRendererED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10shared_ptrI14VectorRendererED1Ev
_ZNSt10shared_ptrI14VectorRendererED1Ev:
.LFB3512:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EED2Ev
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN5ShapeD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN5ShapeD1Ev
	.def	_ZN5ShapeD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN5ShapeD1Ev
_ZN5ShapeD1Ev:
.LFB3516:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt10shared_ptrI8RendererED1Ev
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3506:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 88
	.seh_stackalloc	88
	lea	rbp, 80[rsp]
	.seh_setframe	rbp, 80
	.seh_endprologue
	call	__main
	lea	rax, -32[rbp]
	mov	rcx, rax
.LEHB0:
	call	_ZSt11make_sharedI14VectorRendererJEESt10shared_ptrIT_EDpOT0_
.LEHE0:
	lea	rdx, -32[rbp]
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZNSt10shared_ptrI8RendererEC1I14VectorRenderervEERKS_IT_E
	lea	rdx, -16[rbp]
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZN5ShapeC1ESt10shared_ptrI8RendererE
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZNSt10shared_ptrI8RendererED1Ev
	lea	rax, -48[rbp]
	mov	rcx, rax
.LEHB1:
	call	_ZNK5Shape4drawEv
.LEHE1:
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZN5ShapeD1Ev
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZNSt10shared_ptrI14VectorRendererED1Ev
	mov	eax, 0
	jmp	.L28
.L27:
	mov	rbx, rax
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZN5ShapeD1Ev
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZNSt10shared_ptrI14VectorRendererED1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB2:
	call	_Unwind_Resume
.LEHE2:
.L28:
	add	rsp, 88
	pop	rbx
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3506:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3506-.LLSDACSB3506
.LLSDACSB3506:
	.uleb128 .LEHB0-.LFB3506
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB3506
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L27-.LFB3506
	.uleb128 0
	.uleb128 .LEHB2-.LFB3506
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE3506:
	.text
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:
.LFB3803:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	test	rax, rax
	je	.L31
	mov	rdx, QWORD PTR [rax]
	add	rdx, 8
	mov	rdx, QWORD PTR [rdx]
	mov	rcx, rax
	call	rdx
.L31:
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv:
.LFB3804:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE19_M_release_last_useEv
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt10shared_ptrI8RendererEC1EOS1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt10shared_ptrI8RendererEC1EOS1_
	.def	_ZNSt10shared_ptrI8RendererEC1EOS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10shared_ptrI8RendererEC1EOS1_
_ZNSt10shared_ptrI8RendererEC1EOS1_:
.LFB3823:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR -8[rbp], rdx
	mov	rdx, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2EOS3_
	nop
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EED1Ev
	.def	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EED1Ev
_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EED1Ev:
.LFB3826:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	je	.L37
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rcx, rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv
.L37:
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EEptEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EEptEv
	.def	_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EEptEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EEptEv
_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EEptEv:
.LFB3827:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EE6_M_getEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZSt11make_sharedI14VectorRendererJEESt10shared_ptrIT_EDpOT0_,"x"
	.linkonce discard
	.globl	_ZSt11make_sharedI14VectorRendererJEESt10shared_ptrIT_EDpOT0_
	.def	_ZSt11make_sharedI14VectorRendererJEESt10shared_ptrIT_EDpOT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt11make_sharedI14VectorRendererJEESt10shared_ptrIT_EDpOT0_
_ZSt11make_sharedI14VectorRendererJEESt10shared_ptrIT_EDpOT0_:
.LFB3828:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rax, -1[rbp]
	mov	rdx, rax
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt10shared_ptrI14VectorRendererEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt10shared_ptrI8RendererEC1I14VectorRenderervEERKS_IT_E,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt10shared_ptrI8RendererEC1I14VectorRenderervEERKS_IT_E
	.def	_ZNSt10shared_ptrI8RendererEC1I14VectorRenderervEERKS_IT_E;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10shared_ptrI8RendererEC1I14VectorRenderervEERKS_IT_E
_ZNSt10shared_ptrI8RendererEC1I14VectorRenderervEERKS_IT_E:
.LFB3831:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	rcx, rax
	call	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2I14VectorRenderervEERKS_IT_LS2_2EE
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EED2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EED2Ev
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EED2Ev
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EED2Ev:
.LFB3973:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTVSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE19_M_release_last_useEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE19_M_release_last_useEv
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE19_M_release_last_useEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE19_M_release_last_useEv
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE19_M_release_last_useEv:
.LFB3976:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	add	rax, 16
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 12
	mov	QWORD PTR -8[rbp], rax
	mov	DWORD PTR -12[rbp], -1
	mov	eax, 1
	test	eax, eax
	sete	al
	test	al, al
	je	.L47
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -24[rbp], rax
	mov	eax, DWORD PTR -12[rbp]
	mov	DWORD PTR -28[rbp], eax
	mov	rax, QWORD PTR -24[rbp]
	mov	eax, DWORD PTR [rax]
	mov	DWORD PTR -32[rbp], eax
	mov	rax, QWORD PTR -24[rbp]
	mov	edx, DWORD PTR [rax]
	mov	eax, DWORD PTR -28[rbp]
	add	edx, eax
	mov	rax, QWORD PTR -24[rbp]
	mov	DWORD PTR [rax], edx
	mov	eax, DWORD PTR -32[rbp]
	jmp	.L49
.L47:
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -40[rbp], rax
	mov	eax, DWORD PTR -12[rbp]
	mov	DWORD PTR -44[rbp], eax
	mov	edx, DWORD PTR -44[rbp]
	mov	rax, QWORD PTR -40[rbp]
	lock xadd	DWORD PTR [rax], edx
	mov	eax, edx
	nop
.L49:
	cmp	eax, 1
	sete	al
	test	al, al
	je	.L52
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	add	rax, 24
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
.L52:
	nop
	add	rsp, 80
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2EOS3_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2EOS3_
	.def	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2EOS3_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2EOS3_
_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2EOS3_:
.LFB3991:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	rcx, rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1Ev
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	rdx, QWORD PTR 24[rbp]
	add	rdx, 8
	mov	rcx, rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE7_M_swapERS2_
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR [rax], 0
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EE6_M_getEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EE6_M_getEv
	.def	_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EE6_M_getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EE6_M_getEv
_ZNKSt19__shared_ptr_accessI8RendererLN9__gnu_cxx12_Lock_policyE2ELb0ELb0EE6_M_getEv:
.LFB3993:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EE3getEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt10shared_ptrI14VectorRendererEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt10shared_ptrI14VectorRendererEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_
	.def	_ZNSt10shared_ptrI14VectorRendererEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10shared_ptrI14VectorRendererEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_
_ZNSt10shared_ptrI14VectorRendererEC1ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_:
.LFB3996:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	rcx, rax
	call	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EEC2ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2I14VectorRenderervEERKS_IT_LS2_2EE,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2I14VectorRenderervEERKS_IT_LS2_2EE
	.def	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2I14VectorRenderervEERKS_IT_LS2_2EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2I14VectorRenderervEERKS_IT_LS2_2EE
_ZNSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EEC2I14VectorRenderervEERKS_IT_LS2_2EE:
.LFB3998:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	rdx, QWORD PTR 24[rbp]
	add	rdx, 8
	mov	rcx, rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1Ev
	.def	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1Ev
_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1Ev:
.LFB4101:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], 0
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE7_M_swapERS2_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE7_M_swapERS2_
	.def	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE7_M_swapERS2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE7_M_swapERS2_
_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EE7_M_swapERS2_:
.LFB4102:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR -8[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EE3getEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EE3getEv
	.def	_ZNKSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EE3getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EE3getEv
_ZNKSt12__shared_ptrI8RendererLN9__gnu_cxx12_Lock_policyE2EE3getEv:
.LFB4103:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EEC2ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EEC2ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_
	.def	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EEC2ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EEC2ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_
_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EEC2ISaIvEJEEESt20_Sp_alloc_shared_tagIT_EDpOT0_:
.LFB4105:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], 0
	mov	rax, QWORD PTR 16[rbp]
	lea	rcx, 8[rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	r8, rdx
	mov	rdx, rax
	call	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1I14VectorRendererSaIvEJEEERPT_St20_Sp_alloc_shared_tagIT0_EDpOT1_
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EE31_M_enable_shared_from_this_withIS0_S0_EENSt9enable_ifIXntsrNS3_15__has_esft_baseIT0_vEE5valueEvE4typeEPT_
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_
	.def	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_
_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1ERKS2_:
.LFB4109:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	je	.L65
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rcx, rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_add_ref_copyEv
.L65:
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1I14VectorRendererSaIvEJEEERPT_St20_Sp_alloc_shared_tagIT0_EDpOT1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1I14VectorRendererSaIvEJEEERPT_St20_Sp_alloc_shared_tagIT0_EDpOT1_
	.def	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1I14VectorRendererSaIvEJEEERPT_St20_Sp_alloc_shared_tagIT0_EDpOT1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1I14VectorRendererSaIvEJEEERPT_St20_Sp_alloc_shared_tagIT0_EDpOT1_
_ZNSt14__shared_countILN9__gnu_cxx12_Lock_policyE2EEC1I14VectorRendererSaIvEJEEERPT_St20_Sp_alloc_shared_tagIT0_EDpOT1_:
.LFB4187:
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
	lea	rbp, 96[rsp]
	.seh_setframe	rbp, 96
	.seh_endprologue
	mov	QWORD PTR 48[rbp], rcx
	mov	QWORD PTR 56[rbp], rdx
	mov	QWORD PTR 64[rbp], r8
	mov	rax, QWORD PTR 64[rbp]
	mov	QWORD PTR -24[rbp], rax
	lea	rax, -33[rbp]
	mov	QWORD PTR -32[rbp], rax
	nop
	nop
	lea	rax, -64[rbp]
	lea	rdx, -33[rbp]
	mov	rcx, rax
	call	_ZSt18__allocate_guardedISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEESt15__allocated_ptrIT_ERS8_
	lea	rax, -64[rbp]
	mov	rcx, rax
	call	_ZNKSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEE3getEv
	mov	QWORD PTR -8[rbp], rax
	mov	rsi, QWORD PTR -8[rbp]
	mov	rdx, rsi
	mov	ecx, 24
	call	_ZnwyPv
	mov	rbx, rax
	mov	edx, edi
	mov	rcx, rbx
	call	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEC1IJEEES1_DpOT_
	mov	eax, 0
	mov	QWORD PTR -16[rbp], rbx
	test	al, al
	je	.L68
	mov	rdx, rsi
	mov	rcx, rbx
	call	_ZdlPvS_
.L68:
	nop
	lea	rax, -64[rbp]
	mov	edx, 0
	mov	rcx, rax
	call	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEaSEDn
	mov	rax, QWORD PTR 48[rbp]
	mov	rdx, QWORD PTR -16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -16[rbp]
	mov	rcx, rax
	call	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE6_M_ptrEv
	mov	rdx, QWORD PTR 56[rbp]
	mov	QWORD PTR [rdx], rax
	lea	rax, -64[rbp]
	mov	rcx, rax
	call	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEED1Ev
	nop
	nop
	add	rsp, 104
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EE31_M_enable_shared_from_this_withIS0_S0_EENSt9enable_ifIXntsrNS3_15__has_esft_baseIT0_vEE5valueEvE4typeEPT_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EE31_M_enable_shared_from_this_withIS0_S0_EENSt9enable_ifIXntsrNS3_15__has_esft_baseIT0_vEE5valueEvE4typeEPT_
	.def	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EE31_M_enable_shared_from_this_withIS0_S0_EENSt9enable_ifIXntsrNS3_15__has_esft_baseIT0_vEE5valueEvE4typeEPT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EE31_M_enable_shared_from_this_withIS0_S0_EENSt9enable_ifIXntsrNS3_15__has_esft_baseIT0_vEE5valueEvE4typeEPT_
_ZNSt12__shared_ptrI14VectorRendererLN9__gnu_cxx12_Lock_policyE2EE31_M_enable_shared_from_this_withIS0_S0_EENSt9enable_ifIXntsrNS3_15__has_esft_baseIT0_vEE5valueEvE4typeEPT_:
.LFB4188:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_add_ref_copyEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_add_ref_copyEv
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_add_ref_copyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_add_ref_copyEv
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE15_M_add_ref_copyEv:
.LFB4189:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	QWORD PTR -8[rbp], rax
	mov	DWORD PTR -12[rbp], 1
	mov	eax, 1
	test	eax, eax
	sete	al
	test	al, al
	je	.L73
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -24[rbp], rax
	mov	eax, DWORD PTR -12[rbp]
	mov	DWORD PTR -28[rbp], eax
	mov	rax, QWORD PTR -24[rbp]
	mov	edx, DWORD PTR [rax]
	mov	eax, DWORD PTR -28[rbp]
	add	edx, eax
	mov	rax, QWORD PTR -24[rbp]
	mov	DWORD PTR [rax], edx
	jmp	.L74
.L73:
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -40[rbp], rax
	mov	eax, DWORD PTR -12[rbp]
	mov	DWORD PTR -44[rbp], eax
	mov	edx, DWORD PTR -44[rbp]
	mov	rax, QWORD PTR -40[rbp]
	lock add	DWORD PTR [rax], edx
	nop
.L74:
	nop
	nop
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZSt18__allocate_guardedISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEESt15__allocated_ptrIT_ERS8_,"x"
	.linkonce discard
	.globl	_ZSt18__allocate_guardedISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEESt15__allocated_ptrIT_ERS8_
	.def	_ZSt18__allocate_guardedISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEESt15__allocated_ptrIT_ERS8_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt18__allocate_guardedISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEESt15__allocated_ptrIT_ERS8_
_ZSt18__allocate_guardedISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEESt15__allocated_ptrIT_ERS8_:
.LFB4223:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	QWORD PTR -16[rbp], 1
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -24[rbp], rax
	mov	rax, QWORD PTR -16[rbp]
	mov	QWORD PTR -32[rbp], rax
	mov	eax, 0
	test	al, al
	je	.L77
	mov	rax, QWORD PTR -32[rbp]
	mov	ecx, 0
	mov	edx, 24
	mul	rdx
	jno	.L78
	mov	ecx, 1
.L78:
	mov	QWORD PTR -32[rbp], rax
	mov	rax, rcx
	and	eax, 1
	test	al, al
	je	.L80
	call	_ZSt28__throw_bad_array_new_lengthv
.L80:
	mov	rax, QWORD PTR -32[rbp]
	mov	rcx, rax
	call	_Znwy
	mov	rcx, rax
	jmp	.L81
.L77:
	mov	rdx, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR -24[rbp]
	mov	r8d, 0
	mov	rcx, rax
	call	_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE8allocateEyPKv
	mov	rcx, rax
	nop
.L81:
	nop
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEC1ERS6_PS5_
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEED1Ev
	.def	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEED1Ev
_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEED1Ev:
.LFB4226:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	test	rax, rax
	je	.L89
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	rdx, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR [rdx]
	mov	QWORD PTR -8[rbp], rdx
	mov	QWORD PTR -16[rbp], rax
	mov	QWORD PTR -24[rbp], 1
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -32[rbp], rax
	mov	rax, QWORD PTR -16[rbp]
	mov	QWORD PTR -40[rbp], rax
	mov	rax, QWORD PTR -24[rbp]
	mov	QWORD PTR -48[rbp], rax
	mov	eax, 0
	test	al, al
	je	.L87
	mov	rax, QWORD PTR -40[rbp]
	mov	rcx, rax
	call	_ZdlPv
	jmp	.L88
.L87:
	mov	rcx, QWORD PTR -48[rbp]
	mov	rdx, QWORD PTR -40[rbp]
	mov	rax, QWORD PTR -32[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE10deallocateEPS5_y
.L88:
	nop
.L89:
	nop
	add	rsp, 80
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEE3getEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEE3getEv
	.def	_ZNKSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEE3getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEE3getEv
_ZNKSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEE3getEv:
.LFB4227:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR -16[rbp], rax
	mov	rax, QWORD PTR -16[rbp]
	nop
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEC1IJEEES1_DpOT_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEC1IJEEES1_DpOT_
	.def	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEC1IJEEES1_DpOT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEC1IJEEES1_DpOT_
_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEC1IJEEES1_DpOT_:
.LFB4232:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EEC2Ev
	lea	rdx, _ZTVSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	rax, QWORD PTR 32[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	edx, ebx
	mov	rcx, rax
	call	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_ImplC1ES1_
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE6_M_ptrEv
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZSt10_ConstructI14VectorRendererJEEvPT_DpOT0_
	nop
	nop
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEaSEDn,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEaSEDn
	.def	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEaSEDn;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEaSEDn
_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEaSEDn:
.LFB4233:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR 8[rax], 0
	mov	rax, QWORD PTR 16[rbp]
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE6_M_ptrEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE6_M_ptrEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE6_M_ptrEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE6_M_ptrEv
_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE6_M_ptrEv:
.LFB4234:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE6_M_ptrEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEC1ERS6_PS5_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEC1ERS6_PS5_
	.def	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEC1ERS6_PS5_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEC1ERS6_PS5_
_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEC1ERS6_PS5_:
.LFB4257:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rdx, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 32[rbp]
	mov	QWORD PTR 8[rax], rdx
	nop
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EEC2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EEC2Ev
	.def	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EEC2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EEC2Ev
_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EEC2Ev:
.LFB4261:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTVSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR 8[rax], 1
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR 12[rax], 1
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_ImplC1ES1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_ImplC1ES1_
	.def	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_ImplC1ES1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_ImplC1ES1_
_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_ImplC1ES1_:
.LFB4265:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EEC2ERKS0_
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE6_M_ptrEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE6_M_ptrEv
	.def	_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE6_M_ptrEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE6_M_ptrEv
_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE6_M_ptrEv:
.LFB4267:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE7_M_addrEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EEC2ERKS0_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EEC2ERKS0_
	.def	_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EEC2ERKS0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EEC2ERKS0_
_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EEC2ERKS0_:
.LFB4281:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN8RendererC2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN8RendererC2Ev
	.def	_ZN8RendererC2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN8RendererC2Ev
_ZN8RendererC2Ev:
.LFB4286:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTV8Renderer[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN8RendererD2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN8RendererD2Ev
	.def	_ZN8RendererD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN8RendererD2Ev
_ZN8RendererD2Ev:
.LFB4289:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTV8Renderer[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN14VectorRendererC1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN14VectorRendererC1Ev
	.def	_ZN14VectorRendererC1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN14VectorRendererC1Ev
_ZN14VectorRendererC1Ev:
.LFB4293:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN8RendererC2Ev
	lea	rdx, _ZTV14VectorRenderer[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZSt10_ConstructI14VectorRendererJEEvPT_DpOT0_,"x"
	.linkonce discard
	.globl	_ZSt10_ConstructI14VectorRendererJEEvPT_DpOT0_
	.def	_ZSt10_ConstructI14VectorRendererJEEvPT_DpOT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt10_ConstructI14VectorRendererJEEvPT_DpOT0_
_ZSt10_ConstructI14VectorRendererJEEvPT_DpOT0_:
.LFB4283:
	push	rbp
	.seh_pushreg	rbp
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	eax, 0
	test	al, al
	je	.L111
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZSt12construct_atI14VectorRendererJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
	jmp	.L109
.L111:
	mov	rsi, QWORD PTR 32[rbp]
	mov	rdx, rsi
	mov	ecx, 8
	call	_ZnwyPv
	mov	rbx, rax
	mov	QWORD PTR [rbx], 0
	mov	rcx, rbx
	call	_ZN14VectorRendererC1Ev
	mov	eax, 0
	test	al, al
	je	.L109
	mov	rdx, rsi
	mov	rcx, rbx
	call	_ZdlPvS_
	nop
.L109:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE7_M_addrEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE7_M_addrEv
	.def	_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE7_M_addrEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE7_M_addrEv
_ZN9__gnu_cxx16__aligned_bufferI14VectorRendererE7_M_addrEv:
.LFB4294:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE8allocateEyPKv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE8allocateEyPKv
	.def	_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE8allocateEyPKv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE8allocateEyPKv
_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE8allocateEyPKv:
.LFB4300:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	movabs	rax, 384307168202282325
	cmp	rax, QWORD PTR 24[rbp]
	setb	al
	movzx	eax, al
	test	eax, eax
	setne	al
	test	al, al
	je	.L117
	movabs	rax, 768614336404564650
	cmp	rax, QWORD PTR 24[rbp]
	jnb	.L118
	call	_ZSt28__throw_bad_array_new_lengthv
.L118:
	call	_ZSt17__throw_bad_allocv
.L117:
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
	mov	rcx, rax
	call	_Znwy
	nop
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE10deallocateEPS5_y,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE10deallocateEPS5_y
	.def	_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE10deallocateEPS5_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE10deallocateEPS5_y
_ZNSt15__new_allocatorISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEE10deallocateEPS5_y:
.LFB4301:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	rdx, QWORD PTR 32[rbp]
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
	mov	rdx, rax
	mov	rax, QWORD PTR 24[rbp]
	mov	rcx, rax
	call	_ZdlPvy
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZSt12construct_atI14VectorRendererJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_,"x"
	.linkonce discard
	.globl	_ZSt12construct_atI14VectorRendererJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
	.def	_ZSt12construct_atI14VectorRendererJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt12construct_atI14VectorRendererJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
_ZSt12construct_atI14VectorRendererJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_:
.LFB4302:
	push	rbp
	.seh_pushreg	rbp
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	rax, QWORD PTR 32[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rsi, QWORD PTR -8[rbp]
	mov	rdx, rsi
	mov	ecx, 8
	call	_ZnwyPv
	mov	rbx, rax
	mov	QWORD PTR [rbx], 0
	mov	rcx, rbx
	call	_ZN14VectorRendererC1Ev
	mov	eax, 0
	test	al, al
	je	.L124
	mov	rdx, rsi
	mov	rcx, rbx
	call	_ZdlPvS_
.L124:
	mov	rax, rbx
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rbp
	ret
	.seh_endproc
	.weak	_ZSt12construct_atI14VectorRendererJEEPT_S2_DpOT0_
	.def	_ZSt12construct_atI14VectorRendererJEEPT_S2_DpOT0_;	.scl	2;	.type	32;	.endef
	.set	_ZSt12construct_atI14VectorRendererJEEPT_S2_DpOT0_,_ZSt12construct_atI14VectorRendererJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
	.globl	_ZTVSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTVSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTVSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	0
	.quad	_ZTISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.quad	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.globl	_ZTV14VectorRenderer
	.section	.rdata$_ZTV14VectorRenderer,"dr"
	.linkonce same_size
	.align 8
_ZTV14VectorRenderer:
	.quad	0
	.quad	_ZTI14VectorRenderer
	.quad	_ZN14VectorRendererD1Ev
	.quad	_ZN14VectorRendererD0Ev
	.quad	_ZNK14VectorRenderer6renderEv
	.section	.text$_ZN14VectorRendererD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN14VectorRendererD1Ev
	.def	_ZN14VectorRendererD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN14VectorRendererD1Ev
_ZN14VectorRendererD1Ev:
.LFB4306:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTV14VectorRenderer[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN8RendererD2Ev
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN14VectorRendererD0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN14VectorRendererD0Ev
	.def	_ZN14VectorRendererD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN14VectorRendererD0Ev
_ZN14VectorRendererD0Ev:
.LFB4307:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN14VectorRendererD1Ev
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 8
	mov	rcx, rax
	call	_ZdlPvy
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	_ZTV8Renderer
	.section	.rdata$_ZTV8Renderer,"dr"
	.linkonce same_size
	.align 8
_ZTV8Renderer:
	.quad	0
	.quad	_ZTI8Renderer
	.quad	0
	.quad	0
	.quad	__cxa_pure_virtual
	.globl	_ZTVSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTVSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTVSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE:
	.quad	0
	.quad	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.quad	0
	.quad	0
	.quad	__cxa_pure_virtual
	.quad	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.quad	__cxa_pure_virtual
	.globl	_ZTISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.globl	_ZTSSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTSSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 32
_ZTSSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "St23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE\0"
	.globl	_ZTI14VectorRenderer
	.section	.rdata$_ZTI14VectorRenderer,"dr"
	.linkonce same_size
	.align 8
_ZTI14VectorRenderer:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS14VectorRenderer
	.quad	_ZTI8Renderer
	.globl	_ZTS14VectorRenderer
	.section	.rdata$_ZTS14VectorRenderer,"dr"
	.linkonce same_size
	.align 16
_ZTS14VectorRenderer:
	.ascii "14VectorRenderer\0"
	.globl	_ZTI8Renderer
	.section	.rdata$_ZTI8Renderer,"dr"
	.linkonce same_size
	.align 8
_ZTI8Renderer:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS8Renderer
	.globl	_ZTS8Renderer
	.section	.rdata$_ZTS8Renderer,"dr"
	.linkonce same_size
	.align 8
_ZTS8Renderer:
	.ascii "8Renderer\0"
	.globl	_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTISt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.quad	_ZTISt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE
	.globl	_ZTSSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTSSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 32
_ZTSSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "St16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE\0"
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	.def	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev:
.LFB4310:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTVSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EED2Ev
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
	.def	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev
_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev:
.LFB4311:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 24
	mov	rcx, rax
	call	_ZdlPvy
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv
_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:
.LFB4312:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE6_M_ptrEv
	mov	rbx, rax
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_Impl8_M_allocEv
	mov	QWORD PTR -8[rbp], rbx
	mov	QWORD PTR -16[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZSt8_DestroyI14VectorRendererEvPT_
	nop
	nop
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4312:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4312-.LLSDACSB4312
.LLSDACSB4312:
.LLSDACSE4312:
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv
_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:
.LFB4313:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_Impl8_M_allocEv
	mov	QWORD PTR -8[rbp], rax
	lea	rax, -17[rbp]
	mov	QWORD PTR -16[rbp], rax
	nop
	nop
	mov	rcx, QWORD PTR 16[rbp]
	lea	rdx, -17[rbp]
	lea	rax, -48[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEEC1ERS6_PS5_
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZNSt15__allocated_ptrISaISt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EEEED1Ev
	nop
	nop
	add	rsp, 80
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
	.def	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info
_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:
.LFB4314:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	call	_ZNSt19_Sp_make_shared_tag5_S_tiEv
	cmp	QWORD PTR 24[rbp], rax
	je	.L132
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	eax, 0
	test	al, al
	je	.L134
	lea	rax, _ZTISt19_Sp_make_shared_tag[rip]
	cmp	QWORD PTR -8[rbp], rax
	sete	al
	jmp	.L135
.L134:
	mov	rax, QWORD PTR -8[rbp]
	mov	rdx, QWORD PTR 8[rax]
	lea	rax, _ZTSSt19_Sp_make_shared_tag[rip]
	cmp	rdx, rax
	jne	.L136
	mov	eax, 1
	jmp	.L135
.L136:
	lea	rdx, _ZTISt19_Sp_make_shared_tag[rip]
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZNKSt9type_info7__equalERKS_
	nop
.L135:
	test	al, al
	je	.L137
.L132:
	mov	eax, 1
	jmp	.L138
.L137:
	mov	eax, 0
.L138:
	test	al, al
	je	.L139
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE6_M_ptrEv
	jmp	.L140
.L139:
	mov	eax, 0
.L140:
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_Impl8_M_allocEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_Impl8_M_allocEv
	.def	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_Impl8_M_allocEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_Impl8_M_allocEv
_ZNSt23_Sp_counted_ptr_inplaceI14VectorRendererSaIvELN9__gnu_cxx12_Lock_policyE2EE5_Impl8_M_allocEv:
.LFB4315:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EE6_S_getERS1_
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EE6_S_getERS1_,"x"
	.linkonce discard
	.globl	_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EE6_S_getERS1_
	.def	_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EE6_S_getERS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EE6_S_getERS1_
_ZNSt14_Sp_ebo_helperILi0ESaIvELb1EE6_S_getERS1_:
.LFB4317:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZSt8_DestroyI14VectorRendererEvPT_,"x"
	.linkonce discard
	.globl	_ZSt8_DestroyI14VectorRendererEvPT_
	.def	_ZSt8_DestroyI14VectorRendererEvPT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt8_DestroyI14VectorRendererEvPT_
_ZSt8_DestroyI14VectorRendererEvPT_:
.LFB4318:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZSt10destroy_atI14VectorRendererEvPT_
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZSt10destroy_atI14VectorRendererEvPT_,"x"
	.linkonce discard
	.globl	_ZSt10destroy_atI14VectorRendererEvPT_
	.def	_ZSt10destroy_atI14VectorRendererEvPT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt10destroy_atI14VectorRendererEvPT_
_ZSt10destroy_atI14VectorRendererEvPT_:
.LFB4319:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	_ZTISt19_Sp_make_shared_tag
	.section	.rdata$_ZTISt19_Sp_make_shared_tag,"dr"
	.linkonce same_size
	.align 8
_ZTISt19_Sp_make_shared_tag:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSSt19_Sp_make_shared_tag
	.globl	_ZTSSt19_Sp_make_shared_tag
	.section	.rdata$_ZTSSt19_Sp_make_shared_tag,"dr"
	.linkonce same_size
	.align 16
_ZTSSt19_Sp_make_shared_tag:
	.ascii "St19_Sp_make_shared_tag\0"
	.globl	_ZTISt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTISt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 8
_ZTISt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSSt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE
	.globl	_ZTSSt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE
	.section	.rdata$_ZTSSt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE,"dr"
	.linkonce same_size
	.align 32
_ZTSSt11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE:
	.ascii "St11_Mutex_baseILN9__gnu_cxx12_Lock_policyE2EE\0"
	.weak	__cxa_pure_virtual
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZSt28__throw_bad_array_new_lengthv;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	__cxa_pure_virtual;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt9type_info7__equalERKS_;	.scl	2;	.type	32;	.endef
