	.file	"_atom_alloc_strategies.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.def	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0:
.LFB2023:
	.seh_endprologue
	test	rcx, rcx
	je	.L1
	sub	rdx, rcx
	jmp	_ZdlPvy
.L1:
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt12_Vector_baseIPvSaIS0_EED2Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIPvSaIS0_EED2Ev.isra.0
_ZNSt12_Vector_baseIPvSaIS0_EED2Ev.isra.0:
.LFB2024:
	.seh_endprologue
	test	rcx, rcx
	je	.L4
	sub	rdx, rcx
	jmp	_ZdlPvy
.L4:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_append\0"
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB1:
	.text
.LHOTB1:
	.align 2
	.p2align 4
	.def	_ZN12_GLOBAL__N_14Pool5init_Ev.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_14Pool5init_Ev.constprop.0
_ZN12_GLOBAL__N_14Pool5init_Ev.constprop.0:
.LFB2025:
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rcx]
	sub	rsi, QWORD PTR [rcx]
	mov	rbp, QWORD PTR 24[rcx]
	shr	rsi, 5
	mov	rbx, rcx
	cmp	rbp, QWORD PTR 32[rcx]
	je	.L7
	mov	QWORD PTR 32[rcx], rbp
.L7:
	mov	rdi, QWORD PTR 40[rbx]
	mov	r13, rdi
	sub	r13, rbp
	mov	rax, r13
	sar	rax, 3
	cmp	rax, rsi
	jnb	.L8
	mov	r12, QWORD PTR 32[rbx]
	lea	r14, 0[0+rsi*8]
	mov	rcx, r14
	call	_Znwy
	sub	r12, rbp
	mov	rdi, rax
	test	r12, r12
	jne	.L33
.L9:
	test	rbp, rbp
	je	.L10
	mov	rdx, r13
	mov	rcx, rbp
	call	_ZdlPvy
.L10:
	add	r12, rdi
	mov	QWORD PTR 24[rbx], rdi
	add	rdi, r14
	mov	QWORD PTR 32[rbx], r12
	mov	QWORD PTR 40[rbx], rdi
.L11:
	sub	rsi, 1
	sal	rsi, 5
	jmp	.L17
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L34:
	sub	rsi, 32
	mov	QWORD PTR [rax], rbp
	add	QWORD PTR 32[rbx], 8
	cmp	rsi, -32
	je	.L6
.L35:
	mov	rdi, QWORD PTR 40[rbx]
.L17:
	mov	rbp, QWORD PTR [rbx]
	mov	rax, QWORD PTR 32[rbx]
	add	rbp, rsi
	cmp	rax, rdi
	jne	.L34
	mov	r15, QWORD PTR 24[rbx]
	mov	r13, rdi
	movabs	rax, 1152921504606846975
	sub	r13, r15
	mov	rdx, r13
	sar	rdx, 3
	cmp	rdx, rax
	je	.L32
	test	rdx, rdx
	mov	eax, 1
	cmovne	rax, rdx
	add	rax, rdx
	movabs	rdx, 1152921504606846975
	cmp	rax, rdx
	cmova	rax, rdx
	lea	r12, 0[0+rax*8]
	mov	rcx, r12
	call	_Znwy
	mov	QWORD PTR [rax+r13], rbp
	mov	r14, rax
	test	r13, r13
	je	.L15
	mov	r8, r13
	mov	rdx, r15
	mov	rcx, rax
	call	memcpy
.L15:
	lea	rbp, 8[r14+r13]
	test	r15, r15
	je	.L16
	mov	rdx, rdi
	mov	rcx, r15
	sub	rdx, r15
	call	_ZdlPvy
.L16:
	mov	QWORD PTR 24[rbx], r14
	sub	rsi, 32
	add	r14, r12
	mov	QWORD PTR 32[rbx], rbp
	mov	QWORD PTR 40[rbx], r14
	cmp	rsi, -32
	jne	.L35
.L6:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L8:
	test	rsi, rsi
	jne	.L11
	jmp	.L6
.L33:
	mov	r8, r12
	mov	rdx, rbp
	mov	rcx, rax
	call	memcpy
	jmp	.L9
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZN12_GLOBAL__N_14Pool5init_Ev.constprop.0.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_14Pool5init_Ev.constprop.0.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 40
	.seh_savereg	rsi, 48
	.seh_savereg	rdi, 56
	.seh_savereg	rbp, 64
	.seh_savereg	r12, 72
	.seh_savereg	r13, 80
	.seh_savereg	r14, 88
	.seh_savereg	r15, 96
	.seh_endprologue
_ZN12_GLOBAL__N_14Pool5init_Ev.constprop.0.cold:
.L32:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text$_ZNSt12_Vector_baseIhSaIhEE17_M_create_storageEy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12_Vector_baseIhSaIhEE17_M_create_storageEy
	.def	_ZNSt12_Vector_baseIhSaIhEE17_M_create_storageEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIhSaIhEE17_M_create_storageEy
_ZNSt12_Vector_baseIhSaIhEE17_M_create_storageEy:
.LFB1933:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rsi, rcx
	mov	rbx, rdx
	test	rdx, rdx
	je	.L39
	js	.L40
	mov	rcx, rdx
	call	_Znwy
.L37:
	movq	xmm0, rax
	add	rax, rbx
	punpcklqdq	xmm0, xmm0
	mov	QWORD PTR 16[rsi], rax
	movups	XMMWORD PTR [rsi], xmm0
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L39:
	xor	eax, eax
	jmp	.L37
	.p2align 4,,10
	.p2align 3
.L40:
	call	_ZSt17__throw_bad_allocv
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC2:
	.ascii "cannot create std::vector larger than max_size()\0"
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB3:
	.text
.LHOTB3:
	.align 2
	.p2align 4
	.def	_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0
_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0:
.LFB2031:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rbx, rcx
	mov	rsi, rdx
	test	rdx, rdx
	js	.L48
	mov	QWORD PTR 16[rcx], 0
	pxor	xmm0, xmm0
	movups	XMMWORD PTR [rcx], xmm0
	call	_ZNSt12_Vector_baseIhSaIhEE17_M_create_storageEy
	mov	r9, QWORD PTR [rbx]
	test	rsi, rsi
	je	.L43
	mov	BYTE PTR [r9], 0
	lea	rcx, 1[r9]
	cmp	rsi, 1
	jne	.L49
	mov	r9, rcx
.L43:
	mov	QWORD PTR 8[rbx], r9
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
.L49:
	add	r9, rsi
	lea	r8, -1[rsi]
	xor	edx, edx
	mov	QWORD PTR 40[rsp], r9
	call	memset
	mov	r9, QWORD PTR 40[rsp]
	jmp	.L43
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0.cold
	.seh_stackalloc	72
	.seh_savereg	rbx, 56
	.seh_savereg	rsi, 64
	.seh_endprologue
_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0.cold:
.L48:
	lea	rcx, .LC2[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.text
.LHOTE3:
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB4:
	.text
.LHOTB4:
	.align 2
	.p2align 4
	.def	_ZN12_GLOBAL__N_16BitmapC2Ey;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_16BitmapC2Ey
_ZN12_GLOBAL__N_16BitmapC2Ey:
.LFB1774:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rsi, rcx
	mov	rbx, rdx
	sal	rdx, 5
.LEHB0:
	call	_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0
.LEHE0:
	add	rbx, 7
	pxor	xmm0, xmm0
	mov	QWORD PTR 40[rsi], 0
	shr	rbx, 3
	movups	XMMWORD PTR 24[rsi], xmm0
	lea	rcx, 24[rsi]
	mov	rdx, rbx
.LEHB1:
	call	_ZNSt12_Vector_baseIhSaIhEE17_M_create_storageEy
.LEHE1:
	mov	rdx, QWORD PTR 24[rsi]
	mov	eax, ebx
	lea	r8, 8[rdx]
	mov	rcx, rdx
	mov	QWORD PTR [rdx], 0
	mov	QWORD PTR -8[rdx+rax], 0
	and	r8, -8
	xor	eax, eax
	add	rdx, rbx
	sub	rcx, r8
	mov	rdi, r8
	add	ecx, ebx
	shr	ecx, 3
	rep stosq
	mov	QWORD PTR 32[rsi], rdx
	mov	QWORD PTR 48[rsi], 0
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L52:
	mov	rbx, rax
	jmp	.L51
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1774:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1774-.LLSDACSB1774
.LLSDACSB1774:
	.uleb128 .LEHB0-.LFB1774
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB1774
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L52-.LFB1774
	.uleb128 0
.LLSDACSE1774:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZN12_GLOBAL__N_16BitmapC2Ey.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_16BitmapC2Ey.cold
	.seh_stackalloc	56
	.seh_savereg	rbx, 32
	.seh_savereg	rsi, 40
	.seh_savereg	rdi, 48
	.seh_endprologue
_ZN12_GLOBAL__N_16BitmapC2Ey.cold:
.L51:
	mov	rcx, QWORD PTR [rsi]
	mov	rdx, QWORD PTR 16[rsi]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC1774:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC1774-.LLSDACSBC1774
.LLSDACSBC1774:
	.uleb128 .LEHB2-.LCOLDB4
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC1774:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE4:
	.text
.LHOTE4:
	.def	_ZN12_GLOBAL__N_16BitmapC1Ey;	.scl	3;	.type	32;	.endef
	.set	_ZN12_GLOBAL__N_16BitmapC1Ey,_ZN12_GLOBAL__N_16BitmapC2Ey
	.section .rdata,"dr"
.LC5:
	.ascii "req_bytes=%zu\12\0"
.LC6:
	.ascii "block_bytes=%zu\12\0"
.LC7:
	.ascii "internal_frag_per_block=%zu\12\0"
.LC8:
	.ascii "scale_n1=%zu\12\0"
.LC9:
	.ascii "scale_n2=%zu\12\0"
	.align 8
.LC10:
	.ascii "arena_single_free_supported=%d\12\0"
.LC11:
	.ascii "arena_n1\0"
.LC12:
	.ascii "%s_served_first=%zu\12\0"
.LC13:
	.ascii "%s_served_second=%zu\12\0"
.LC14:
	.ascii "%s_peak_after_first=%zu\12\0"
.LC15:
	.ascii "%s_meta_struct_bytes=%zu\12\0"
	.align 8
.LC16:
	.ascii "%s_meta_bookkeeping_bytes=%zu\12\0"
.LC17:
	.ascii "%s_meta_total_bytes=%zu\12\0"
.LC18:
	.ascii "arena_n2\0"
.LC19:
	.ascii "pool_n1\0"
.LC20:
	.ascii "pool_n2\0"
.LC21:
	.ascii "bitmap_n1\0"
.LC22:
	.ascii "bitmap_n2\0"
.LC23:
	.ascii "scale_ratio=%zu\12\0"
	.section	.text.unlikely,"x"
.LCOLDB24:
	.section	.text.startup,"x"
.LHOTB24:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1783:
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
	sub	rsp, 552
	.seh_stackalloc	552
	.seh_endprologue
	call	__main
	mov	edx, 24
	lea	rcx, .LC5[rip]
.LEHB3:
	call	__mingw_printf
	mov	edx, 32
	lea	rcx, .LC6[rip]
	call	__mingw_printf
	mov	edx, 8
	lea	rcx, .LC7[rip]
	call	__mingw_printf
	mov	edx, 1000
	lea	rcx, .LC8[rip]
	call	__mingw_printf
	mov	edx, 8000
	lea	rcx, .LC9[rip]
	call	__mingw_printf
	xor	edx, edx
	lea	rcx, .LC10[rip]
	call	__mingw_printf
	lea	rcx, 224[rsp]
	mov	edx, 24000
	mov	QWORD PTR 224[rsp], 0
	mov	QWORD PTR 232[rsp], 0
	mov	QWORD PTR 240[rsp], 0
	mov	QWORD PTR 248[rsp], 0
	call	_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0
.LEHE3:
	mov	rdi, QWORD PTR 224[rsp]
	mov	edx, 192000
	mov	rax, QWORD PTR 240[rsp]
	lea	rcx, 256[rsp]
	mov	QWORD PTR 256[rsp], 0
	mov	rbx, QWORD PTR 232[rsp]
	mov	QWORD PTR 128[rsp], rdi
	mov	QWORD PTR 160[rsp], rax
	mov	QWORD PTR 264[rsp], 0
	mov	QWORD PTR 272[rsp], 0
	mov	QWORD PTR 280[rsp], 0
.LEHB4:
	call	_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0
.LEHE4:
	mov	rax, QWORD PTR 256[rsp]
	sub	rbx, rdi
	mov	r10, rdi
	xor	r8d, r8d
	mov	rsi, QWORD PTR 264[rsp]
	mov	rcx, rbx
	xor	edi, edi
	mov	QWORD PTR 104[rsp], rax
	mov	rax, QWORD PTR 272[rsp]
	mov	QWORD PTR 152[rsp], rax
	mov	eax, 1000
.L58:
	lea	rdx, 24[rdi]
	cmp	rcx, rdx
	jb	.L55
	lea	r9, [r10+rdi]
	mov	rdi, rdx
	test	r9, r9
	jne	.L275
.L55:
	sub	rax, 1
	jne	.L58
.L56:
	mov	r10, QWORD PTR 128[rsp]
	mov	ebx, 1000
	xor	eax, eax
	xor	ebp, ebp
	.p2align 5
	.p2align 4
	.p2align 3
.L60:
	lea	rdx, 24[rax]
	cmp	rcx, rdx
	jb	.L59
	add	rax, r10
	lea	r9, 1[rbp]
	mov	rax, rdx
	cmovne	rbp, r9
.L59:
	sub	rbx, 1
	jne	.L60
	lea	rdx, .LC11[rip]
	lea	rcx, .LC12[rip]
.LEHB5:
	call	__mingw_printf
	mov	r8, rbp
	lea	rdx, .LC11[rip]
	lea	rcx, .LC13[rip]
	call	__mingw_printf
	mov	r8, rdi
	lea	rdx, .LC11[rip]
	lea	rcx, .LC14[rip]
	call	__mingw_printf
	mov	r8d, 32
	lea	rdx, .LC11[rip]
	lea	rcx, .LC15[rip]
	call	__mingw_printf
	xor	r8d, r8d
	lea	rdx, .LC11[rip]
	lea	rcx, .LC16[rip]
	call	__mingw_printf
	mov	r8d, 32
	lea	rdx, .LC11[rip]
	lea	rcx, .LC17[rip]
	call	__mingw_printf
	mov	r9, QWORD PTR 104[rsp]
	xor	edi, edi
	xor	r8d, r8d
	mov	eax, 8000
	sub	rsi, r9
.L64:
	lea	rdx, 24[rdi]
	cmp	rsi, rdx
	jb	.L61
	lea	rcx, [r9+rdi]
	mov	rdi, rdx
	test	rcx, rcx
	jne	.L276
.L61:
	sub	rax, 1
	jne	.L64
.L62:
	mov	r9, QWORD PTR 104[rsp]
	xor	eax, eax
	mov	r14d, 8000
	.p2align 5
	.p2align 4
	.p2align 3
.L66:
	lea	rdx, 24[rax]
	cmp	rsi, rdx
	jb	.L65
	add	rax, r9
	lea	rcx, 1[rbx]
	mov	rax, rdx
	cmovne	rbx, rcx
.L65:
	sub	r14, 1
	jne	.L66
	lea	rdx, .LC18[rip]
	lea	rcx, .LC12[rip]
	call	__mingw_printf
	mov	r8, rbx
	lea	rdx, .LC18[rip]
	lea	rcx, .LC13[rip]
	call	__mingw_printf
	mov	r8, rdi
	lea	rdx, .LC18[rip]
	lea	rcx, .LC14[rip]
	call	__mingw_printf
	mov	r8d, 32
	lea	rdx, .LC18[rip]
	lea	rcx, .LC15[rip]
	call	__mingw_printf
	xor	r8d, r8d
	lea	rdx, .LC18[rip]
	lea	rcx, .LC16[rip]
	call	__mingw_printf
	mov	r8d, 32
	lea	rdx, .LC18[rip]
	lea	rcx, .LC17[rip]
	call	__mingw_printf
	lea	rbx, 288[rsp]
	mov	edx, 32000
	mov	QWORD PTR 288[rsp], 0
	mov	rcx, rbx
	mov	QWORD PTR 304[rsp], 0
	mov	QWORD PTR 312[rsp], 0
	mov	QWORD PTR 320[rsp], 0
	mov	QWORD PTR 328[rsp], 0
	mov	QWORD PTR 336[rsp], 0
	mov	QWORD PTR 80[rsp], rbx
	call	_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0
.LEHE5:
	pxor	xmm0, xmm0
	mov	rcx, rbx
	mov	QWORD PTR 328[rsp], 0
	mov	QWORD PTR 336[rsp], 0
	movups	XMMWORD PTR 312[rsp], xmm0
.LEHB6:
	call	_ZN12_GLOBAL__N_14Pool5init_Ev.constprop.0
.LEHE6:
	mov	rax, QWORD PTR 288[rsp]
	lea	rdi, 352[rsp]
	mov	edx, 256000
	mov	QWORD PTR 352[rsp], 0
	mov	rcx, rdi
	mov	QWORD PTR 368[rsp], 0
	mov	r15, QWORD PTR 312[rsp]
	mov	QWORD PTR 64[rsp], rax
	mov	rax, QWORD PTR 304[rsp]
	mov	QWORD PTR 376[rsp], 0
	mov	r13, QWORD PTR 320[rsp]
	mov	QWORD PTR 112[rsp], rax
	mov	rax, QWORD PTR 328[rsp]
	mov	QWORD PTR 88[rsp], rdi
	mov	rbp, QWORD PTR 336[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	QWORD PTR 384[rsp], 0
	mov	QWORD PTR 392[rsp], 0
	mov	QWORD PTR 400[rsp], 0
.LEHB7:
	call	_ZNSt6vectorIhSaIhEEC1EyRKS0_.isra.0
.LEHE7:
	pxor	xmm0, xmm0
	mov	rcx, rdi
	mov	QWORD PTR 392[rsp], 0
	mov	QWORD PTR 400[rsp], 0
	movups	XMMWORD PTR 376[rsp], xmm0
.LEHB8:
	call	_ZN12_GLOBAL__N_14Pool5init_Ev.constprop.0
.LEHE8:
	mov	rax, QWORD PTR 352[rsp]
	mov	rbx, QWORD PTR 384[rsp]
	mov	edx, 1000
	mov	rdi, QWORD PTR 400[rsp]
	mov	QWORD PTR 56[rsp], rax
	mov	rax, QWORD PTR 368[rsp]
	mov	QWORD PTR 120[rsp], rax
	mov	rax, QWORD PTR 376[rsp]
	mov	QWORD PTR 72[rsp], rax
	mov	rax, QWORD PTR 392[rsp]
	mov	QWORD PTR 48[rsp], rax
	.p2align 5
	.p2align 4
	.p2align 3
.L70:
	cmp	r13, r15
	je	.L73
	mov	rax, QWORD PTR -8[r13]
	add	rbp, 1
	sub	r13, 8
	cmp	rax, 1
	sbb	r14, -1
.L73:
	sub	rdx, 1
	jne	.L70
	mov	esi, 1000
	jmp	.L79
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L278:
	mov	rax, QWORD PTR 64[rsp]
	add	r13, 8
	mov	QWORD PTR -8[r13], rax
	sub	rsi, 1
	je	.L277
.L79:
	cmp	r13, QWORD PTR 40[rsp]
	jne	.L278
	movabs	rcx, 1152921504606846975
	mov	r13, QWORD PTR 40[rsp]
	sub	r13, r15
	mov	rax, r13
	sar	rax, 3
	cmp	rax, rcx
	je	.L247
	test	rax, rax
	mov	r12d, 1
	cmovne	r12, rax
	add	r12, rax
	movabs	rax, 1152921504606846975
	cmp	r12, rax
	cmova	r12, rax
	sal	r12, 3
	mov	rcx, r12
.LEHB9:
	call	_Znwy
.LEHE9:
	mov	r9, rax
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR [r9+r13], rax
	test	r13, r13
	je	.L77
	mov	rcx, r9
	mov	r8, r13
	mov	rdx, r15
	call	memcpy
	mov	r9, rax
.L77:
	lea	r13, 8[r9+r13]
	test	r15, r15
	je	.L78
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, r15
	mov	QWORD PTR 96[rsp], r9
	sub	rdx, r15
	call	_ZdlPvy
	mov	r9, QWORD PTR 96[rsp]
.L78:
	lea	rax, [r9+r12]
	mov	r15, r9
	mov	QWORD PTR 40[rsp], rax
	sub	rsi, 1
	jne	.L79
	.p2align 4
	.p2align 3
.L277:
	mov	rax, QWORD PTR 40[rsp]
	sal	rbp, 5
	movq	xmm0, r15
	mov	rcx, QWORD PTR 80[rsp]
	mov	QWORD PTR 336[rsp], 0
	punpcklqdq	xmm0, xmm0
	mov	QWORD PTR 328[rsp], rax
	movups	XMMWORD PTR 312[rsp], xmm0
.LEHB10:
	call	_ZN12_GLOBAL__N_14Pool5init_Ev.constprop.0
.LEHE10:
	mov	rax, QWORD PTR 288[rsp]
	mov	rcx, QWORD PTR 328[rsp]
	mov	r13d, 1000
	mov	r15, QWORD PTR 312[rsp]
	mov	QWORD PTR 64[rsp], rax
	mov	rax, QWORD PTR 304[rsp]
	mov	QWORD PTR 40[rsp], rcx
	mov	QWORD PTR 112[rsp], rax
	mov	rax, QWORD PTR 320[rsp]
	.p2align 5
	.p2align 4
	.p2align 3
.L81:
	cmp	rax, r15
	je	.L80
	mov	rdx, QWORD PTR -8[rax]
	sub	rax, 8
	cmp	rdx, 1
	sbb	rsi, -1
.L80:
	sub	r13, 1
	jne	.L81
	mov	r12, QWORD PTR 40[rsp]
	mov	r8, r14
	lea	rdx, .LC19[rip]
	lea	rcx, .LC12[rip]
	sub	r12, r15
.LEHB11:
	call	__mingw_printf
	mov	r8, rsi
	lea	rdx, .LC19[rip]
	lea	rcx, .LC13[rip]
	call	__mingw_printf
	mov	r8, rbp
	lea	rdx, .LC19[rip]
	lea	rcx, .LC14[rip]
	call	__mingw_printf
	mov	r8d, 56
	lea	rdx, .LC19[rip]
	lea	rcx, .LC15[rip]
	call	__mingw_printf
	mov	r8, r12
	lea	rdx, .LC19[rip]
	lea	rcx, .LC16[rip]
	call	__mingw_printf
	lea	r8, 56[r12]
	lea	rdx, .LC19[rip]
	lea	rcx, .LC17[rip]
	call	__mingw_printf
	mov	rcx, QWORD PTR 72[rsp]
	mov	eax, 8000
	.p2align 5
	.p2align 4
	.p2align 3
.L83:
	cmp	rbx, rcx
	je	.L82
	mov	rdx, QWORD PTR -8[rbx]
	add	rdi, 1
	sub	rbx, 8
	cmp	rdx, 1
	sbb	r13, -1
.L82:
	sub	rax, 1
	jne	.L83
	movabs	rbp, 1152921504606846975
	mov	r12d, 8000
	jmp	.L89
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L280:
	mov	rax, QWORD PTR 56[rsp]
	add	rbx, 8
	mov	QWORD PTR -8[rbx], rax
	sub	r12, 1
	je	.L279
.L89:
	cmp	QWORD PTR 48[rsp], rbx
	jne	.L280
	mov	rbx, QWORD PTR 48[rsp]
	sub	rbx, QWORD PTR 72[rsp]
	mov	rax, rbx
	sar	rax, 3
	cmp	rax, rbp
	je	.L248
	test	rax, rax
	mov	esi, 1
	cmovne	rsi, rax
	add	rsi, rax
	movabs	rax, 1152921504606846975
	cmp	rsi, rax
	cmova	rsi, rax
	sal	rsi, 3
	mov	rcx, rsi
	call	_Znwy
.LEHE11:
	mov	r14, rax
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR [r14+rbx], rax
	test	rbx, rbx
	je	.L87
	mov	rdx, QWORD PTR 72[rsp]
	mov	r8, rbx
	mov	rcx, r14
	call	memcpy
.L87:
	mov	rcx, QWORD PTR 72[rsp]
	lea	rbx, 8[r14+rbx]
	test	rcx, rcx
	je	.L88
	mov	rdx, QWORD PTR 48[rsp]
	sub	rdx, rcx
	call	_ZdlPvy
.L88:
	lea	rax, [r14+rsi]
	mov	QWORD PTR 72[rsp], r14
	mov	QWORD PTR 48[rsp], rax
	sub	r12, 1
	jne	.L89
	.p2align 4
	.p2align 3
.L279:
	movq	xmm0, QWORD PTR 72[rsp]
	sal	rdi, 5
	mov	rax, QWORD PTR 48[rsp]
	mov	QWORD PTR 400[rsp], 0
	mov	rcx, QWORD PTR 88[rsp]
	punpcklqdq	xmm0, xmm0
	mov	QWORD PTR 392[rsp], rax
	movups	XMMWORD PTR 376[rsp], xmm0
.LEHB12:
	call	_ZN12_GLOBAL__N_14Pool5init_Ev.constprop.0
.LEHE12:
	mov	rax, QWORD PTR 352[rsp]
	mov	r8, QWORD PTR 376[rsp]
	mov	edx, 8000
	mov	rbx, QWORD PTR 392[rsp]
	mov	QWORD PTR 56[rsp], rax
	mov	rax, QWORD PTR 368[rsp]
	mov	QWORD PTR 72[rsp], r8
	mov	QWORD PTR 48[rsp], rbx
	mov	QWORD PTR 120[rsp], rax
	mov	rax, QWORD PTR 384[rsp]
	.p2align 5
	.p2align 4
	.p2align 3
.L94:
	cmp	rax, r8
	je	.L93
	mov	rcx, QWORD PTR -8[rax]
	sub	rax, 8
	cmp	rcx, 1
	sbb	r12, -1
.L93:
	sub	rdx, 1
	jne	.L94
	mov	r8, r13
	lea	rdx, .LC20[rip]
	mov	rbx, QWORD PTR 48[rsp]
	lea	rcx, .LC12[rip]
	sub	rbx, QWORD PTR 72[rsp]
.LEHB13:
	call	__mingw_printf
	mov	r8, r12
	lea	rdx, .LC20[rip]
	lea	rcx, .LC13[rip]
	call	__mingw_printf
	mov	r8, rdi
	lea	rdx, .LC20[rip]
	lea	rcx, .LC14[rip]
	call	__mingw_printf
	mov	r8d, 56
	lea	rdx, .LC20[rip]
	lea	rcx, .LC15[rip]
	call	__mingw_printf
	mov	r8, rbx
	lea	rdx, .LC20[rip]
	lea	rcx, .LC16[rip]
	call	__mingw_printf
	lea	r8, 56[rbx]
	lea	rdx, .LC20[rip]
	lea	rcx, .LC17[rip]
	call	__mingw_printf
	lea	rcx, 416[rsp]
	mov	edx, 1000
	mov	QWORD PTR 416[rsp], 0
	mov	QWORD PTR 424[rsp], 0
	mov	QWORD PTR 432[rsp], 0
	mov	QWORD PTR 440[rsp], 0
	mov	QWORD PTR 448[rsp], 0
	mov	QWORD PTR 456[rsp], 0
	mov	QWORD PTR 464[rsp], 0
	call	_ZN12_GLOBAL__N_16BitmapC1Ey
.LEHE13:
	mov	rax, QWORD PTR 432[rsp]
	mov	rsi, QWORD PTR 416[rsp]
	lea	rcx, 480[rsp]
	mov	edx, 8000
	mov	r9, QWORD PTR 424[rsp]
	mov	QWORD PTR 480[rsp], 0
	mov	QWORD PTR 168[rsp], rax
	mov	rax, QWORD PTR 456[rsp]
	mov	QWORD PTR 96[rsp], rsi
	mov	rbx, QWORD PTR 440[rsp]
	mov	QWORD PTR 200[rsp], r9
	mov	rdi, QWORD PTR 448[rsp]
	mov	QWORD PTR 136[rsp], rax
	mov	r13, QWORD PTR 464[rsp]
	mov	QWORD PTR 488[rsp], 0
	mov	QWORD PTR 496[rsp], 0
	mov	QWORD PTR 504[rsp], 0
	mov	QWORD PTR 512[rsp], 0
	mov	QWORD PTR 520[rsp], 0
	mov	QWORD PTR 528[rsp], 0
.LEHB14:
	call	_ZN12_GLOBAL__N_16BitmapC1Ey
.LEHE14:
	mov	rax, QWORD PTR 480[rsp]
	sub	rdi, rbx
	xor	r12d, r12d
	mov	ebp, 1000
	mov	r14, QWORD PTR 528[rsp]
	mov	r9, QWORD PTR 200[rsp]
	mov	QWORD PTR 200[rsp], r15
	mov	r8, rdi
	mov	QWORD PTR 80[rsp], rax
	mov	rax, QWORD PTR 488[rsp]
	lea	r11, 0[0+rdi*8]
	mov	QWORD PTR 208[rsp], r14
	mov	rdi, r9
	mov	QWORD PTR 144[rsp], rax
	mov	rax, QWORD PTR 496[rsp]
	sub	rdi, rsi
	mov	QWORD PTR 216[rsp], r8
	mov	r8, rsi
	mov	QWORD PTR 176[rsp], rax
	mov	rax, QWORD PTR 504[rsp]
	mov	QWORD PTR 88[rsp], rax
	mov	rax, QWORD PTR 512[rsp]
	mov	QWORD PTR 192[rsp], rax
	mov	rax, QWORD PTR 520[rsp]
	mov	QWORD PTR 184[rsp], rax
	.p2align 4
	.p2align 3
.L95:
	xor	esi, esi
	xor	eax, eax
	jmp	.L101
	.p2align 4,,10
	.p2align 3
.L99:
	cmp	rsi, rdi
	jnb	.L96
	mov	rdx, rax
	mov	ecx, eax
	shr	rdx, 3
	and	ecx, 7
	add	rdx, rbx
	movzx	r15d, BYTE PTR [rdx]
	bt	r15d, ecx
	mov	r14d, r15d
	jnc	.L281
	add	rsi, 32
	add	rax, 1
.L101:
	cmp	rax, r11
	jne	.L99
.L96:
	sub	rbp, 1
	jne	.L95
.L100:
	mov	r8, QWORD PTR 216[rsp]
	mov	rsi, r13
	and	BYTE PTR [rbx], -2
	mov	r15, QWORD PTR 200[rsp]
	mov	r14, QWORD PTR 208[rsp]
	sal	rsi, 5
	test	r8, r8
	je	.L102
	lea	rax, -1[r8]
	cmp	rax, 14
	jbe	.L159
	mov	rax, r8
	mov	rdx, rbx
	pxor	xmm0, xmm0
	and	rax, -16
	lea	rcx, [rbx+rax]
	test	al, 16
	je	.L104
	lea	rdx, 16[rbx]
	movups	XMMWORD PTR [rbx], xmm0
	cmp	rcx, rdx
	je	.L259
	.p2align 4
	.p2align 4
	.p2align 3
.L104:
	movups	XMMWORD PTR [rdx], xmm0
	add	rdx, 32
	movups	XMMWORD PTR -16[rdx], xmm0
	cmp	rcx, rdx
	jne	.L104
.L259:
	cmp	rax, r8
	je	.L102
.L252:
	mov	rdx, rax
	mov	BYTE PTR [rbx+rax], 0
	add	rax, 1
	not	rdx
	add	rdx, r8
	cmp	rax, r8
	jnb	.L102
	and	edx, 1
	je	.L106
	mov	BYTE PTR [rbx+rax], 0
	add	rax, 1
	cmp	rax, r8
	jnb	.L102
	.p2align 5
	.p2align 4
	.p2align 3
.L106:
	mov	BYTE PTR [rbx+rax], 0
	mov	BYTE PTR 1[rbx+rax], 0
	add	rax, 2
	cmp	rax, r8
	jb	.L106
.L102:
	mov	edi, 1000
	test	r11, r11
	je	.L241
	mov	QWORD PTR 200[rsp], r12
	mov	r10, r9
	xor	ebp, ebp
	sub	r10, QWORD PTR 96[rsp]
	.p2align 4
	.p2align 3
.L113:
	xor	r8d, r8d
	xor	eax, eax
	jmp	.L112
	.p2align 4,,10
	.p2align 3
.L283:
	mov	rdx, rax
	mov	ecx, eax
	shr	rdx, 3
	and	ecx, 7
	add	rdx, rbx
	movzx	r12d, BYTE PTR [rdx]
	bt	r12d, ecx
	mov	r9d, r12d
	jnc	.L282
	add	rax, 1
	add	r8, 32
	cmp	r11, rax
	je	.L108
.L112:
	cmp	r8, r10
	jb	.L283
.L108:
	sub	rdi, 1
	jne	.L113
	mov	r12, QWORD PTR 200[rsp]
	mov	rdi, rbp
.L116:
	mov	rbp, QWORD PTR 136[rsp]
	mov	r8, r12
	lea	rdx, .LC21[rip]
	lea	rcx, .LC12[rip]
	sub	rbp, rbx
.LEHB15:
	call	__mingw_printf
	mov	r8, rdi
	lea	rdx, .LC21[rip]
	lea	rcx, .LC13[rip]
	call	__mingw_printf
	mov	r8, rsi
	lea	rdx, .LC21[rip]
	lea	rcx, .LC14[rip]
	call	__mingw_printf
	mov	r8d, 56
	lea	rdx, .LC21[rip]
	lea	rcx, .LC15[rip]
	call	__mingw_printf
	mov	r8, rbp
	lea	rdx, .LC21[rip]
	lea	rcx, .LC16[rip]
	call	__mingw_printf
	lea	r8, 56[rbp]
	lea	rdx, .LC21[rip]
	lea	rcx, .LC17[rip]
	call	__mingw_printf
	mov	rdi, QWORD PTR 192[rsp]
	mov	rsi, QWORD PTR 88[rsp]
	mov	QWORD PTR 200[rsp], rbx
	xor	r8d, r8d
	mov	rax, QWORD PTR 80[rsp]
	mov	rbp, QWORD PTR 144[rsp]
	mov	r12d, 8000
	sub	rdi, rsi
	mov	QWORD PTR 192[rsp], rdi
	lea	r11, 0[0+rdi*8]
	sub	rbp, rax
	mov	rbx, rax
	.p2align 4
	.p2align 3
.L119:
	xor	r9d, r9d
	xor	eax, eax
	jmp	.L125
	.p2align 4,,10
	.p2align 3
.L123:
	cmp	r9, rbp
	jnb	.L120
	mov	rdx, rax
	mov	ecx, eax
	shr	rdx, 3
	and	ecx, 7
	add	rdx, rsi
	movzx	edi, BYTE PTR [rdx]
	bt	edi, ecx
	mov	r10d, edi
	jnc	.L284
	add	r9, 32
	add	rax, 1
.L125:
	cmp	r11, rax
	jne	.L123
.L120:
	sub	r12, 1
	jne	.L119
.L124:
	mov	rsi, QWORD PTR 88[rsp]
	mov	rdi, QWORD PTR 192[rsp]
	sal	r14, 5
	mov	rbx, QWORD PTR 200[rsp]
	and	BYTE PTR [rsi], -2
	test	rdi, rdi
	je	.L126
	lea	rax, -1[rdi]
	cmp	rax, 14
	jbe	.L161
	mov	rax, rdi
	mov	rdx, rsi
	pxor	xmm0, xmm0
	and	rax, -16
	lea	rcx, [rax+rsi]
	test	al, 16
	je	.L128
	mov	rsi, QWORD PTR 88[rsp]
	lea	rdx, 16[rsi]
	movups	XMMWORD PTR [rsi], xmm0
	cmp	rcx, rdx
	je	.L258
	.p2align 4
	.p2align 4
	.p2align 3
.L128:
	movups	XMMWORD PTR [rdx], xmm0
	add	rdx, 32
	movups	XMMWORD PTR -16[rdx], xmm0
	cmp	rcx, rdx
	jne	.L128
.L258:
	cmp	rax, rdi
	je	.L126
.L255:
	mov	rsi, QWORD PTR 88[rsp]
	mov	rdx, rax
	not	rdx
	mov	BYTE PTR [rsi+rax], 0
	add	rax, 1
	add	rdx, rdi
	cmp	rax, rdi
	jnb	.L126
	and	edx, 1
	je	.L263
	mov	rsi, QWORD PTR 88[rsp]
	mov	BYTE PTR [rsi+rax], 0
	add	rax, 1
	cmp	rax, rdi
	jnb	.L126
.L263:
	mov	rdx, QWORD PTR 88[rsp]
.L130:
	mov	BYTE PTR [rdx+rax], 0
	mov	BYTE PTR 1[rdx+rax], 0
	add	rax, 2
	cmp	rax, rdi
	jb	.L130
.L126:
	mov	edi, 8000
	test	r11, r11
	je	.L242
	mov	rbp, QWORD PTR 144[rsp]
	mov	r10, QWORD PTR 88[rsp]
	xor	r12d, r12d
	mov	QWORD PTR 144[rsp], r8
	sub	rbp, QWORD PTR 80[rsp]
	.p2align 4
	.p2align 3
.L137:
	xor	r8d, r8d
	xor	eax, eax
	jmp	.L136
	.p2align 4,,10
	.p2align 3
.L286:
	mov	rdx, rax
	mov	ecx, eax
	shr	rdx, 3
	and	ecx, 7
	add	rdx, r10
	movzx	esi, BYTE PTR [rdx]
	bt	esi, ecx
	mov	r9d, esi
	jnc	.L285
	add	rax, 1
	add	r8, 32
	cmp	r11, rax
	je	.L132
.L136:
	cmp	r8, rbp
	jb	.L286
.L132:
	sub	rdi, 1
	jne	.L137
	mov	r8, QWORD PTR 144[rsp]
	mov	rdi, r12
.L140:
	mov	rsi, QWORD PTR 184[rsp]
	mov	r13, QWORD PTR 88[rsp]
	lea	rdx, .LC22[rip]
	lea	rcx, .LC12[rip]
	mov	rbp, rsi
	sub	rbp, r13
	call	__mingw_printf
	mov	r8, rdi
	lea	rdx, .LC22[rip]
	lea	rcx, .LC13[rip]
	call	__mingw_printf
	mov	r8, r14
	lea	rdx, .LC22[rip]
	lea	rcx, .LC14[rip]
	call	__mingw_printf
	mov	r8d, 56
	lea	rdx, .LC22[rip]
	lea	rcx, .LC15[rip]
	call	__mingw_printf
	mov	r8, rbp
	lea	rdx, .LC22[rip]
	lea	rcx, .LC16[rip]
	call	__mingw_printf
	lea	r8, 56[rbp]
	lea	rdx, .LC22[rip]
	lea	rcx, .LC17[rip]
	call	__mingw_printf
	mov	edx, 8
	lea	rcx, .LC23[rip]
	call	__mingw_printf
.LEHE15:
	mov	rdx, rsi
	mov	rcx, r13
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rdx, QWORD PTR 176[rsp]
	mov	rcx, QWORD PTR 80[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rdx, QWORD PTR 136[rsp]
	mov	rcx, rbx
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rdx, QWORD PTR 168[rsp]
	mov	rcx, QWORD PTR 96[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rdx, QWORD PTR 48[rsp]
	mov	rcx, QWORD PTR 72[rsp]
	call	_ZNSt12_Vector_baseIPvSaIS0_EED2Ev.isra.0
	mov	rdx, QWORD PTR 120[rsp]
	mov	rcx, QWORD PTR 56[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, r15
	call	_ZNSt12_Vector_baseIPvSaIS0_EED2Ev.isra.0
	mov	rdx, QWORD PTR 112[rsp]
	mov	rcx, QWORD PTR 64[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rdx, QWORD PTR 152[rsp]
	mov	rcx, QWORD PTR 104[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rdx, QWORD PTR 160[rsp]
	mov	rcx, QWORD PTR 128[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	xor	eax, eax
	add	rsp, 552
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
.L275:
	add	r8, 1
	sub	rax, 1
	je	.L148
.L288:
	lea	r9, 24[rdx]
	cmp	rcx, r9
	jb	.L287
	mov	rdx, r9
	add	r8, 1
	sub	rax, 1
	jne	.L288
.L148:
	mov	rdi, rdx
	jmp	.L56
	.p2align 4,,10
	.p2align 3
.L276:
	add	r8, 1
	sub	rax, 1
	je	.L152
.L290:
	lea	rcx, 24[rdx]
	cmp	rsi, rcx
	jb	.L289
	mov	rdx, rcx
	add	r8, 1
	sub	rax, 1
	jne	.L290
.L152:
	mov	rdi, rdx
	jmp	.L62
	.p2align 4,,10
	.p2align 3
.L281:
	mov	eax, 1
	add	rsi, r8
	add	r13, 1
	sal	eax, cl
	or	r14d, eax
	cmp	rsi, 1
	mov	BYTE PTR [rdx], r14b
	sbb	r12, -1
	sub	rbp, 1
	jne	.L95
	jmp	.L100
	.p2align 4,,10
	.p2align 3
.L282:
	mov	eax, 1
	sal	eax, cl
	or	r9d, eax
	add	r8, QWORD PTR 96[rsp]
	mov	BYTE PTR [rdx], r9b
	je	.L108
	add	rbp, 1
	sub	rdi, 1
	jne	.L113
	mov	r12, QWORD PTR 200[rsp]
	mov	rdi, rbp
	jmp	.L116
.L287:
	mov	rdi, rdx
	jmp	.L55
.L289:
	mov	rdi, rdx
	jmp	.L61
.L242:
	sub	rdi, 1
	jne	.L242
	jmp	.L140
.L241:
	sub	rdi, 1
	jne	.L241
	jmp	.L116
	.p2align 4,,10
	.p2align 3
.L284:
	mov	eax, 1
	add	r9, rbx
	add	r14, 1
	sal	eax, cl
	or	r10d, eax
	cmp	r9, 1
	mov	BYTE PTR [rdx], r10b
	sbb	r8, -1
	sub	r12, 1
	jne	.L119
	jmp	.L124
	.p2align 4,,10
	.p2align 3
.L285:
	mov	eax, 1
	sal	eax, cl
	or	r9d, eax
	add	r8, QWORD PTR 80[rsp]
	mov	BYTE PTR [rdx], r9b
	je	.L132
	add	r12, 1
	sub	rdi, 1
	jne	.L137
	mov	r8, QWORD PTR 144[rsp]
	mov	rdi, r12
	jmp	.L140
.L161:
	xor	eax, eax
	jmp	.L255
.L159:
	xor	eax, eax
	jmp	.L252
.L165:
	mov	rbx, rax
	jmp	.L72
.L166:
	mov	rdi, rax
	jmp	.L144
.L171:
	mov	rbx, rax
	jmp	.L91
.L170:
	mov	rbx, rax
	jmp	.L145
.L167:
	mov	rdi, rax
	jmp	.L143
.L164:
	mov	rbx, rax
	jmp	.L69
.L169:
	mov	rdi, rax
	jmp	.L71
.L245:
	jmp	.L246
.L168:
	mov	rbx, rax
	jmp	.L68
.L163:
	mov	rbx, rax
	jmp	.L146
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1783:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1783-.LLSDACSB1783
.LLSDACSB1783:
	.uleb128 .LEHB3-.LFB1783
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB4-.LFB1783
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L163-.LFB1783
	.uleb128 0
	.uleb128 .LEHB5-.LFB1783
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L164-.LFB1783
	.uleb128 0
	.uleb128 .LEHB6-.LFB1783
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L168-.LFB1783
	.uleb128 0
	.uleb128 .LEHB7-.LFB1783
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L165-.LFB1783
	.uleb128 0
	.uleb128 .LEHB8-.LFB1783
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L169-.LFB1783
	.uleb128 0
	.uleb128 .LEHB9-.LFB1783
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L245-.LFB1783
	.uleb128 0
	.uleb128 .LEHB10-.LFB1783
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L170-.LFB1783
	.uleb128 0
	.uleb128 .LEHB11-.LFB1783
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L245-.LFB1783
	.uleb128 0
	.uleb128 .LEHB12-.LFB1783
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L171-.LFB1783
	.uleb128 0
	.uleb128 .LEHB13-.LFB1783
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L245-.LFB1783
	.uleb128 0
	.uleb128 .LEHB14-.LFB1783
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L166-.LFB1783
	.uleb128 0
	.uleb128 .LEHB15-.LFB1783
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L167-.LFB1783
	.uleb128 0
.LLSDACSE1783:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	616
	.seh_savereg	rbx, 552
	.seh_savereg	rsi, 560
	.seh_savereg	rdi, 568
	.seh_savereg	rbp, 576
	.seh_savereg	r12, 584
	.seh_savereg	r13, 592
	.seh_savereg	r14, 600
	.seh_savereg	r15, 608
	.seh_endprologue
main.cold:
.L71:
	mov	rbx, QWORD PTR 352[rsp]
	mov	rsi, QWORD PTR 368[rsp]
	mov	rdx, QWORD PTR 392[rsp]
	mov	rcx, QWORD PTR 376[rsp]
	call	_ZNSt12_Vector_baseIPvSaIS0_EED2Ev.isra.0
	mov	rcx, rbx
	mov	rdx, rsi
	mov	rbx, rdi
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
.L72:
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, r15
	call	_ZNSt12_Vector_baseIPvSaIS0_EED2Ev.isra.0
	mov	rdx, QWORD PTR 112[rsp]
	mov	rcx, QWORD PTR 64[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
.L69:
	mov	rdx, QWORD PTR 152[rsp]
	mov	rcx, QWORD PTR 104[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
.L146:
	mov	rcx, QWORD PTR 128[rsp]
	mov	rdx, QWORD PTR 160[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rcx, rbx
.LEHB16:
	call	_Unwind_Resume
.LEHE16:
.L143:
	mov	rdx, QWORD PTR 184[rsp]
	mov	rcx, QWORD PTR 88[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rdx, QWORD PTR 176[rsp]
	mov	rcx, QWORD PTR 80[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
.L144:
	mov	rdx, QWORD PTR 136[rsp]
	mov	rcx, rbx
	mov	rbx, rdi
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	mov	rdx, QWORD PTR 168[rsp]
	mov	rcx, QWORD PTR 96[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
.L92:
	mov	rdx, QWORD PTR 48[rsp]
	mov	rcx, QWORD PTR 72[rsp]
	call	_ZNSt12_Vector_baseIPvSaIS0_EED2Ev.isra.0
	mov	rdx, QWORD PTR 120[rsp]
	mov	rcx, QWORD PTR 56[rsp]
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	jmp	.L72
.L248:
	lea	rcx, .LC0[rip]
.LEHB17:
	call	_ZSt20__throw_length_errorPKc
.L91:
	mov	rax, QWORD PTR 352[rsp]
	mov	QWORD PTR 56[rsp], rax
	mov	rax, QWORD PTR 368[rsp]
	mov	QWORD PTR 120[rsp], rax
	mov	rax, QWORD PTR 376[rsp]
	mov	QWORD PTR 72[rsp], rax
	mov	rax, QWORD PTR 392[rsp]
	mov	QWORD PTR 48[rsp], rax
	jmp	.L92
.L172:
.L246:
	mov	rbx, rax
	jmp	.L92
.L247:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE17:
.L145:
	mov	rax, QWORD PTR 288[rsp]
	mov	r15, QWORD PTR 312[rsp]
	mov	QWORD PTR 64[rsp], rax
	mov	rax, QWORD PTR 304[rsp]
	mov	QWORD PTR 112[rsp], rax
	mov	rax, QWORD PTR 328[rsp]
	mov	QWORD PTR 40[rsp], rax
	jmp	.L92
.L68:
	mov	rsi, QWORD PTR 288[rsp]
	mov	rdi, QWORD PTR 304[rsp]
	mov	rdx, QWORD PTR 328[rsp]
	mov	rcx, QWORD PTR 312[rsp]
	call	_ZNSt12_Vector_baseIPvSaIS0_EED2Ev.isra.0
	mov	rdx, rdi
	mov	rcx, rsi
	call	_ZNSt12_Vector_baseIhSaIhEED2Ev.isra.0
	jmp	.L69
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC1783:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC1783-.LLSDACSBC1783
.LLSDACSBC1783:
	.uleb128 .LEHB16-.LCOLDB24
	.uleb128 .LEHE16-.LEHB16
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB17-.LCOLDB24
	.uleb128 .LEHE17-.LEHB17
	.uleb128 .L172-.LCOLDB24
	.uleb128 0
.LLSDACSEC1783:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE24:
	.section	.text.startup,"x"
.LHOTE24:
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
