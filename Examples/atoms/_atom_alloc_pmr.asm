	.file	"_atom_alloc_pmr.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK13TrackUpstream11do_is_equalERKNSt3pmr15memory_resourceE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK13TrackUpstream11do_is_equalERKNSt3pmr15memory_resourceE
	.def	_ZNK13TrackUpstream11do_is_equalERKNSt3pmr15memory_resourceE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK13TrackUpstream11do_is_equalERKNSt3pmr15memory_resourceE
_ZNK13TrackUpstream11do_is_equalERKNSt3pmr15memory_resourceE:
.LFB4723:
	.seh_endprologue
	cmp	rcx, rdx
	sete	al
	ret
	.seh_endproc
	.section	.text$_ZNK15CountDelegating11do_is_equalERKNSt3pmr15memory_resourceE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK15CountDelegating11do_is_equalERKNSt3pmr15memory_resourceE
	.def	_ZNK15CountDelegating11do_is_equalERKNSt3pmr15memory_resourceE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK15CountDelegating11do_is_equalERKNSt3pmr15memory_resourceE
_ZNK15CountDelegating11do_is_equalERKNSt3pmr15memory_resourceE:
.LFB4726:
	.seh_endprologue
	cmp	rcx, rdx
	sete	al
	ret
	.seh_endproc
	.section	.text$_ZN15CountDelegating11do_allocateEyy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN15CountDelegating11do_allocateEyy
	.def	_ZN15CountDelegating11do_allocateEyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN15CountDelegating11do_allocateEyy
_ZN15CountDelegating11do_allocateEyy:
.LFB4724:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	eax, DWORD PTR g_res_calls[rip]
	add	eax, 1
	mov	DWORD PTR g_res_calls[rip], eax
	mov	rax, QWORD PTR g_res_bytes[rip]
	add	rax, rdx
	mov	QWORD PTR 40[rsp], r8
	mov	QWORD PTR 32[rsp], rdx
	mov	QWORD PTR g_res_bytes[rip], rax
	call	_ZNSt3pmr19new_delete_resourceEv
	mov	r8, QWORD PTR 40[rsp]
	mov	rdx, QWORD PTR 32[rsp]
	mov	rcx, QWORD PTR [rax]
	mov	r9, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rsp, 56
	rex.W jmp	r9
	.seh_endproc
	.section	.text$_ZN13TrackUpstream11do_allocateEyy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN13TrackUpstream11do_allocateEyy
	.def	_ZN13TrackUpstream11do_allocateEyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13TrackUpstream11do_allocateEyy
_ZN13TrackUpstream11do_allocateEyy:
.LFB4721:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	eax, DWORD PTR g_upstream_calls[rip]
	add	eax, 1
	mov	DWORD PTR g_upstream_calls[rip], eax
	mov	QWORD PTR 40[rsp], rdx
	mov	QWORD PTR 32[rsp], r8
	call	_ZNSt3pmr19new_delete_resourceEv
	mov	r8, QWORD PTR 32[rsp]
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, QWORD PTR [rax]
	mov	r9, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rsp, 56
	rex.W jmp	r9
	.seh_endproc
	.section	.text$_ZN15CountDelegating13do_deallocateEPvyy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN15CountDelegating13do_deallocateEPvyy
	.def	_ZN15CountDelegating13do_deallocateEPvyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN15CountDelegating13do_deallocateEPvyy
_ZN15CountDelegating13do_deallocateEPvyy:
.LFB4725:
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	mov	QWORD PTR 56[rsp], rdx
	mov	QWORD PTR 48[rsp], r8
	mov	QWORD PTR 40[rsp], r9
	call	_ZNSt3pmr19new_delete_resourceEv
	mov	r9, QWORD PTR 40[rsp]
	mov	r8, QWORD PTR 48[rsp]
	mov	rcx, QWORD PTR [rax]
	mov	rdx, QWORD PTR 56[rsp]
	mov	r10, QWORD PTR 24[rcx]
	mov	rcx, rax
	add	rsp, 72
	rex.W jmp	r10
	.seh_endproc
	.section	.text$_ZN13TrackUpstream13do_deallocateEPvyy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN13TrackUpstream13do_deallocateEPvyy
	.def	_ZN13TrackUpstream13do_deallocateEPvyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13TrackUpstream13do_deallocateEPvyy
_ZN13TrackUpstream13do_deallocateEPvyy:
.LFB4722:
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	mov	QWORD PTR 56[rsp], rdx
	mov	QWORD PTR 48[rsp], r8
	mov	QWORD PTR 40[rsp], r9
	call	_ZNSt3pmr19new_delete_resourceEv
	mov	r9, QWORD PTR 40[rsp]
	mov	r8, QWORD PTR 48[rsp]
	mov	rcx, QWORD PTR [rax]
	mov	rdx, QWORD PTR 56[rsp]
	mov	r10, QWORD PTR 24[rcx]
	mov	rcx, rax
	add	rsp, 72
	rex.W jmp	r10
	.seh_endproc
	.section	.text$_ZN15CountDelegatingD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN15CountDelegatingD1Ev
	.def	_ZN15CountDelegatingD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN15CountDelegatingD1Ev
_ZN15CountDelegatingD1Ev:
.LFB4740:
	.seh_endprologue
	lea	rax, _ZTV15CountDelegating[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt3pmr15memory_resourceD2Ev
	.seh_endproc
	.section	.text$_ZN15CountDelegatingD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN15CountDelegatingD0Ev
	.def	_ZN15CountDelegatingD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN15CountDelegatingD0Ev
_ZN15CountDelegatingD0Ev:
.LFB4741:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rax, _ZTV15CountDelegating[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 40[rsp], rcx
	call	_ZNSt3pmr15memory_resourceD2Ev
	mov	rcx, QWORD PTR 40[rsp]
	mov	edx, 8
	add	rsp, 56
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZN13TrackUpstreamD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN13TrackUpstreamD1Ev
	.def	_ZN13TrackUpstreamD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13TrackUpstreamD1Ev
_ZN13TrackUpstreamD1Ev:
.LFB4733:
	.seh_endprologue
	lea	rax, _ZTV13TrackUpstream[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt3pmr15memory_resourceD2Ev
	.seh_endproc
	.section	.text$_ZN13TrackUpstreamD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN13TrackUpstreamD0Ev
	.def	_ZN13TrackUpstreamD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13TrackUpstreamD0Ev
_ZN13TrackUpstreamD0Ev:
.LFB4734:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rax, _ZTV13TrackUpstream[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 40[rsp], rcx
	call	_ZNSt3pmr15memory_resourceD2Ev
	mov	rcx, QWORD PTR 40[rsp]
	mov	edx, 8
	add	rsp, 56
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseIiNSt3pmr21polymorphic_allocatorIiEEED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12_Vector_baseIiNSt3pmr21polymorphic_allocatorIiEEED2Ev
	.def	_ZNSt12_Vector_baseIiNSt3pmr21polymorphic_allocatorIiEEED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIiNSt3pmr21polymorphic_allocatorIiEEED2Ev
_ZNSt12_Vector_baseIiNSt3pmr21polymorphic_allocatorIiEEED2Ev:
.LFB5364:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	test	rdx, rdx
	je	.L12
	mov	rax, QWORD PTR [rcx]
	mov	r8, QWORD PTR 24[rcx]
	mov	r9d, 4
	mov	r10, QWORD PTR [rax]
	sub	r8, rdx
	mov	rcx, rax
	call	[QWORD PTR 24[r10]]
	nop
.L12:
	add	rsp, 40
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5364:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5364-.LLSDACSB5364
.LLSDACSB5364:
.LLSDACSE5364:
	.section	.text$_ZNSt12_Vector_baseIiNSt3pmr21polymorphic_allocatorIiEEED2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "vector::_M_realloc_append\0"
.LC2:
	.ascii "monotonic: upstream_allocs=\0"
	.align 8
.LC3:
	.ascii " (zero heap: buffer served everything)\12\0"
.LC4:
	.ascii "delegating: res_calls=\0"
.LC5:
	.ascii " bytes=\0"
.LC6:
	.ascii " (growth path, heap-backed)\12\0"
	.section	.text.unlikely,"x"
.LCOLDB9:
	.section	.text.startup,"x"
.LHOTB9:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4727:
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
	sub	rsp, 168
	.seh_stackalloc	168
	.seh_endprologue
	xor	ebx, ebx
	xor	esi, esi
	movabs	r13, 2305843009213693951
	call	__main
	lea	rax, _ZZ4mainE3buf[rip]
	lea	rdi, 96[rsp]
	mov	QWORD PTR 144[rsp], 1024
	movq	xmm1, rax
	lea	rax, _ZTV13TrackUpstream[rip+16]
	mov	QWORD PTR 152[rsp], 0
	mov	QWORD PTR 48[rsp], rax
	mov	rax, QWORD PTR .refptr._ZTVNSt3pmr25monotonic_buffer_resourceE[rip]
	add	rax, 16
	movq	xmm0, rax
	lea	rax, 48[rsp]
	punpcklqdq	xmm0, xmm1
	mov	QWORD PTR 32[rsp], rax
	movaps	XMMWORD PTR 96[rsp], xmm0
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	movaps	XMMWORD PTR 112[rsp], xmm0
	movq	xmm0, rax
	xor	eax, eax
	punpcklqdq	xmm0, xmm1
	movaps	XMMWORD PTR 128[rsp], xmm0
	movq	xmm0, rdi
	movaps	XMMWORD PTR 64[rsp], xmm0
	pxor	xmm0, xmm0
	movaps	XMMWORD PTR 80[rsp], xmm0
	jmp	.L26
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L58:
	mov	DWORD PTR [rbx], esi
	add	rbx, 4
	add	esi, 1
	mov	QWORD PTR 80[rsp], rbx
	cmp	esi, 16
	je	.L25
.L59:
	mov	rbx, QWORD PTR 80[rsp]
	mov	rax, QWORD PTR 88[rsp]
.L26:
	cmp	rbx, rax
	jne	.L58
	mov	r15, QWORD PTR 72[rsp]
	mov	rbp, rbx
	sub	rbp, r15
	mov	rax, rbp
	sar	rax, 2
	cmp	rax, r13
	je	.L54
	test	rax, rax
	mov	r12d, 1
	mov	rcx, QWORD PTR 64[rsp]
	mov	r8d, 4
	cmovne	r12, rax
	add	r12, rax
	movabs	rax, 2305843009213693951
	cmp	r12, rax
	cmova	r12, rax
	mov	rax, QWORD PTR [rcx]
	sal	r12, 2
	mov	rdx, r12
.LEHB0:
	call	[QWORD PTR 16[rax]]
.LEHE0:
	mov	DWORD PTR [rax+rbp], esi
	mov	r14, rax
	cmp	rbx, r15
	je	.L21
	sub	rbx, r15
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L22:
	mov	edx, DWORD PTR [r15+rax]
	mov	DWORD PTR [r14+rax], edx
	add	rax, 4
	cmp	rax, rbx
	jne	.L22
	lea	rbx, 4[r14+rax]
.L23:
	mov	rcx, QWORD PTR 64[rsp]
	mov	r8, QWORD PTR 88[rsp]
	mov	r9d, 4
	mov	rdx, r15
	mov	rax, QWORD PTR [rcx]
	sub	r8, r15
	call	[QWORD PTR 24[rax]]
.L24:
	mov	QWORD PTR 72[rsp], r14
	add	esi, 1
	add	r14, r12
	mov	QWORD PTR 80[rsp], rbx
	mov	QWORD PTR 88[rsp], r14
	cmp	esi, 16
	jne	.L59
	.p2align 4
	.p2align 3
.L25:
	lea	rcx, 64[rsp]
	lea	r13, 56[rsp]
	xor	ebx, ebx
	xor	esi, esi
	call	_ZNSt12_Vector_baseIiNSt3pmr21polymorphic_allocatorIiEEED2Ev
	mov	rcx, rdi
	movabs	r14, 2305843009213693951
	call	_ZNSt3pmr25monotonic_buffer_resourceD1Ev
	movq	xmm0, r13
	lea	rax, _ZTV15CountDelegating[rip+16]
	movaps	XMMWORD PTR 96[rsp], xmm0
	pxor	xmm0, xmm0
	mov	QWORD PTR 56[rsp], rax
	xor	eax, eax
	movaps	XMMWORD PTR 112[rsp], xmm0
	jmp	.L35
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L60:
	mov	DWORD PTR [rbx], esi
	add	rbx, 4
	add	esi, 1
	mov	QWORD PTR 112[rsp], rbx
	cmp	esi, 16
	je	.L34
.L61:
	mov	rbx, QWORD PTR 112[rsp]
	mov	rax, QWORD PTR 120[rsp]
.L35:
	cmp	rbx, rax
	jne	.L60
	mov	r15, QWORD PTR 104[rsp]
	mov	rbp, rbx
	sub	rbp, r15
	mov	rax, rbp
	sar	rax, 2
	cmp	rax, r14
	je	.L55
	test	rax, rax
	mov	r12d, 1
	mov	rcx, QWORD PTR 96[rsp]
	mov	r8d, 4
	cmovne	r12, rax
	add	r12, rax
	movabs	rax, 2305843009213693951
	cmp	r12, rax
	cmova	r12, rax
	mov	rax, QWORD PTR [rcx]
	sal	r12, 2
	mov	rdx, r12
.LEHB1:
	call	[QWORD PTR 16[rax]]
.LEHE1:
	mov	DWORD PTR [rax+rbp], esi
	mov	r10, rax
	cmp	r15, rbx
	je	.L30
	sub	rbx, r15
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L31:
	mov	edx, DWORD PTR [r15+rax]
	mov	DWORD PTR [r10+rax], edx
	add	rax, 4
	cmp	rbx, rax
	jne	.L31
	lea	rbx, 4[r10+rbx]
.L32:
	mov	rcx, QWORD PTR 96[rsp]
	mov	r8, QWORD PTR 120[rsp]
	mov	QWORD PTR 40[rsp], r10
	mov	rdx, r15
	mov	r9d, 4
	mov	rax, QWORD PTR [rcx]
	sub	r8, r15
	call	[QWORD PTR 24[rax]]
	mov	r10, QWORD PTR 40[rsp]
.L33:
	mov	QWORD PTR 104[rsp], r10
	add	esi, 1
	add	r10, r12
	mov	QWORD PTR 112[rsp], rbx
	mov	QWORD PTR 120[rsp], r10
	cmp	esi, 16
	jne	.L61
	.p2align 4
	.p2align 3
.L34:
	mov	rcx, rdi
	call	_ZNSt12_Vector_baseIiNSt3pmr21polymorphic_allocatorIiEEED2Ev
	lea	rax, _ZTV15CountDelegating[rip+16]
	mov	rcx, r13
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt3pmr15memory_resourceD2Ev
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC2[rip]
	mov	rcx, rbx
.LEHB2:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_upstream_calls[rip]
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC3[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC4[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_res_calls[rip]
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC5[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rdx, QWORD PTR g_res_bytes[rip]
	mov	rcx, rax
	call	_ZNSo9_M_insertIxEERSoT_
	lea	rdx, .LC6[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE2:
	mov	rcx, QWORD PTR 32[rsp]
	lea	rax, _ZTV13TrackUpstream[rip+16]
	mov	QWORD PTR 48[rsp], rax
	call	_ZNSt3pmr15memory_resourceD2Ev
	xor	eax, eax
	add	rsp, 168
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L21:
	lea	rbx, 4[rax]
	test	r15, r15
	je	.L24
	jmp	.L23
.L30:
	lea	rbx, 4[rax]
	test	r15, r15
	je	.L33
	jmp	.L32
.L40:
	mov	rbx, rax
	jmp	.L37
.L50:
	jmp	.L51
.L52:
	jmp	.L53
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4727:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4727-.LLSDACSB4727
.LLSDACSB4727:
	.uleb128 .LEHB0-.LFB4727
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L50-.LFB4727
	.uleb128 0
	.uleb128 .LEHB1-.LFB4727
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L52-.LFB4727
	.uleb128 0
	.uleb128 .LEHB2-.LFB4727
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L40-.LFB4727
	.uleb128 0
.LLSDACSE4727:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	232
	.seh_savereg	rbx, 168
	.seh_savereg	rsi, 176
	.seh_savereg	rdi, 184
	.seh_savereg	rbp, 192
	.seh_savereg	r12, 200
	.seh_savereg	r13, 208
	.seh_savereg	r14, 216
	.seh_savereg	r15, 224
	.seh_endprologue
main.cold:
.L54:
	lea	rcx, .LC1[rip]
.LEHB3:
	call	_ZSt20__throw_length_errorPKc
.LEHE3:
.L55:
	lea	rcx, .LC1[rip]
.LEHB4:
	call	_ZSt20__throw_length_errorPKc
.LEHE4:
.L39:
.L51:
	lea	rcx, 64[rsp]
	mov	rbx, rax
	call	_ZNSt12_Vector_baseIiNSt3pmr21polymorphic_allocatorIiEEED2Ev
	mov	rcx, rdi
	call	_ZNSt3pmr25monotonic_buffer_resourceD1Ev
.L37:
	mov	rcx, QWORD PTR 32[rsp]
	lea	rax, _ZTV13TrackUpstream[rip+16]
	mov	QWORD PTR 48[rsp], rax
	call	_ZNSt3pmr15memory_resourceD2Ev
	mov	rcx, rbx
.LEHB5:
	call	_Unwind_Resume
.LEHE5:
.L41:
.L53:
	mov	rcx, rdi
	mov	rbx, rax
	call	_ZNSt12_Vector_baseIiNSt3pmr21polymorphic_allocatorIiEEED2Ev
	lea	rax, _ZTV15CountDelegating[rip+16]
	mov	rcx, r13
	mov	QWORD PTR 56[rsp], rax
	call	_ZNSt3pmr15memory_resourceD2Ev
	jmp	.L37
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4727:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4727-.LLSDACSBC4727
.LLSDACSBC4727:
	.uleb128 .LEHB3-.LCOLDB9
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L39-.LCOLDB9
	.uleb128 0
	.uleb128 .LEHB4-.LCOLDB9
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L41-.LCOLDB9
	.uleb128 0
	.uleb128 .LEHB5-.LCOLDB9
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSEC4727:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE9:
	.section	.text.startup,"x"
.LHOTE9:
	.globl	_ZTSNSt3pmr15memory_resourceE
	.section	.rdata$_ZTSNSt3pmr15memory_resourceE,"dr"
	.linkonce same_size
	.align 16
_ZTSNSt3pmr15memory_resourceE:
	.ascii "NSt3pmr15memory_resourceE\0"
	.globl	_ZTINSt3pmr15memory_resourceE
	.section	.rdata$_ZTINSt3pmr15memory_resourceE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt3pmr15memory_resourceE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSNSt3pmr15memory_resourceE
	.globl	_ZTS13TrackUpstream
	.section	.rdata$_ZTS13TrackUpstream,"dr"
	.linkonce same_size
	.align 16
_ZTS13TrackUpstream:
	.ascii "13TrackUpstream\0"
	.globl	_ZTI13TrackUpstream
	.section	.rdata$_ZTI13TrackUpstream,"dr"
	.linkonce same_size
	.align 8
_ZTI13TrackUpstream:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS13TrackUpstream
	.quad	_ZTINSt3pmr15memory_resourceE
	.globl	_ZTS15CountDelegating
	.section	.rdata$_ZTS15CountDelegating,"dr"
	.linkonce same_size
	.align 16
_ZTS15CountDelegating:
	.ascii "15CountDelegating\0"
	.globl	_ZTI15CountDelegating
	.section	.rdata$_ZTI15CountDelegating,"dr"
	.linkonce same_size
	.align 8
_ZTI15CountDelegating:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS15CountDelegating
	.quad	_ZTINSt3pmr15memory_resourceE
	.globl	_ZTV13TrackUpstream
	.section	.rdata$_ZTV13TrackUpstream,"dr"
	.linkonce same_size
	.align 8
_ZTV13TrackUpstream:
	.quad	0
	.quad	_ZTI13TrackUpstream
	.quad	_ZN13TrackUpstreamD1Ev
	.quad	_ZN13TrackUpstreamD0Ev
	.quad	_ZN13TrackUpstream11do_allocateEyy
	.quad	_ZN13TrackUpstream13do_deallocateEPvyy
	.quad	_ZNK13TrackUpstream11do_is_equalERKNSt3pmr15memory_resourceE
	.globl	_ZTV15CountDelegating
	.section	.rdata$_ZTV15CountDelegating,"dr"
	.linkonce same_size
	.align 8
_ZTV15CountDelegating:
	.quad	0
	.quad	_ZTI15CountDelegating
	.quad	_ZN15CountDelegatingD1Ev
	.quad	_ZN15CountDelegatingD0Ev
	.quad	_ZN15CountDelegating11do_allocateEyy
	.quad	_ZN15CountDelegating13do_deallocateEPvyy
	.quad	_ZNK15CountDelegating11do_is_equalERKNSt3pmr15memory_resourceE
.lcomm _ZZ4mainE3buf,1024,16
	.globl	g_res_bytes
	.bss
	.align 8
g_res_bytes:
	.space 8
	.globl	g_res_calls
	.align 4
g_res_calls:
	.space 4
	.globl	g_upstream_calls
	.align 4
g_upstream_calls:
	.space 4
	.section .rdata,"dr"
	.align 16
.LC0:
	.quad	1024
	.quad	1536
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt3pmr19new_delete_resourceEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr15memory_resourceD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr25monotonic_buffer_resourceD1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIxEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
	.section	.rdata$.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE, "dr"
	.p2align	3, 0
	.globl	.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE
	.linkonce	discard
.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE:
	.quad	_ZTVNSt3pmr25monotonic_buffer_resourceE
