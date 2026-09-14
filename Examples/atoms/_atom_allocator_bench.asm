	.file	"_atom_allocator_bench.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.def	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0:
.LFB8352:
	.seh_endprologue
	test	rcx, rcx
	je	.L1
	sub	rdx, rcx
	jmp	_ZdlPvy
.L1:
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorIxSaIxEEC1ERKS1_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIxSaIxEEC1ERKS1_
	.def	_ZNSt6vectorIxSaIxEEC1ERKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIxSaIxEEC1ERKS1_
_ZNSt6vectorIxSaIxEEC1ERKS1_:
.LFB6716:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	xor	r9d, r9d
	mov	rax, QWORD PTR 8[rdx]
	sub	rax, QWORD PTR [rdx]
	mov	r8, rax
	mov	rbx, rcx
	mov	rsi, rdx
	je	.L5
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], rax
	call	_Znwy
	mov	r8, QWORD PTR 40[rsp]
	mov	r9, rax
.L5:
	movq	xmm0, r9
	lea	rax, [r9+r8]
	punpcklqdq	xmm0, xmm0
	mov	QWORD PTR 16[rbx], rax
	movups	XMMWORD PTR [rbx], xmm0
	mov	rax, QWORD PTR [rsi]
	mov	rsi, QWORD PTR 8[rsi]
	sub	rsi, rax
	test	rsi, rsi
	jle	.L6
	mov	rcx, r9
	mov	r8, rsi
	mov	rdx, rax
	call	memcpy
	lea	r9, [rax+rsi]
.L6:
	mov	QWORD PTR 8[rbx], r9
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "iters_per_round=%zu\12\0"
.LC1:
	.ascii "rounds=%zu\12\0"
.LC2:
	.ascii "block_bytes=%zu\12\0"
.LC3:
	.ascii "vector::_M_realloc_append\0"
.LC5:
	.ascii "sink_nonzero=%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB8:
	.section	.text.startup,"x"
.LHOTB8:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5974:
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
	sub	rsp, 280
	.seh_stackalloc	280
	movaps	XMMWORD PTR 256[rsp], xmm6
	.seh_savexmm	xmm6, 256
	.seh_endprologue
	mov	esi, 7
	movabs	rdi, 1152921504606846975
	call	__main
	mov	edx, 10000
	lea	rcx, .LC0[rip]
.LEHB0:
	call	__mingw_printf
	mov	edx, 7
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	mov	edx, 64
	lea	rcx, .LC2[rip]
	call	__mingw_printf
.LEHE0:
	pxor	xmm0, xmm0
	mov	QWORD PTR 64[rsp], 0
	mov	QWORD PTR 96[rsp], 0
	mov	QWORD PTR 128[rsp], 0
	movaps	XMMWORD PTR 48[rsp], xmm0
	movaps	XMMWORD PTR 80[rsp], xmm0
	movaps	XMMWORD PTR 112[rsp], xmm0
.L16:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xor	ebx, ebx
	mov	rbp, rax
	.p2align 4
	.p2align 3
.L10:
	mov	ecx, 64
.LEHB1:
	call	_Znwy
	mov	BYTE PTR [rax], bl
	mov	rdx, QWORD PTR _ZN12_GLOBAL__N_1L6g_sinkE[rip]
	mov	rcx, rax
	movzx	eax, bl
	add	rbx, 1
	add	rax, rdx
	mov	QWORD PTR _ZN12_GLOBAL__N_1L6g_sinkE[rip], rax
	call	_ZdlPv
	cmp	rbx, 10000
	jne	.L10
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	sub	rax, rbp
	mov	rbp, QWORD PTR 64[rsp]
	mov	r12, rax
	mov	rax, QWORD PTR 56[rsp]
	cmp	rax, rbp
	je	.L11
	mov	QWORD PTR [rax], r12
	add	rax, 8
	mov	QWORD PTR 56[rsp], rax
.L12:
	sub	rsi, 1
	jne	.L16
	mov	rax, QWORD PTR .refptr._ZTVNSt3pmr25monotonic_buffer_resourceE[rip]
	lea	rbx, 176[rsp]
	lea	rdx, 48[rsp]
	mov	rcx, rbx
	add	rax, 16
	movq	xmm6, rax
	call	_ZNSt6vectorIxSaIxEEC1ERKS1_
.LEHE1:
	mov	rsi, QWORD PTR 176[rsp]
	mov	r9, QWORD PTR 184[rsp]
	sub	r9, rsi
	je	.L17
	mov	r11, r9
	xor	r10d, r10d
	lea	r8, 8[rsi]
	add	r9, rsi
	sar	r11, 3
	add	r10, 1
	cmp	r10, r11
	jnb	.L17
	.p2align 4
	.p2align 3
.L110:
	mov	rax, r8
	.p2align 5
	.p2align 4
	.p2align 3
.L19:
	mov	rcx, QWORD PTR [rax]
	mov	rdx, QWORD PTR -8[r8]
	cmp	rcx, rdx
	jge	.L18
	mov	QWORD PTR -8[r8], rcx
	mov	QWORD PTR [rax], rdx
.L18:
	add	rax, 8
	cmp	r9, rax
	jne	.L19
	add	r10, 1
	add	r8, 8
	cmp	r10, r11
	jb	.L110
.L17:
	mov	rdx, QWORD PTR 192[rsp]
	mov	rcx, rsi
	mov	esi, 7
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	call	_ZNSt3pmr20get_default_resourceEv
	movdqa	xmm0, XMMWORD PTR .LC4[rip]
	mov	QWORD PTR 216[rsp], 0
	mov	QWORD PTR 208[rsp], rax
	mov	QWORD PTR 224[rsp], 1048576
	mov	QWORD PTR 232[rsp], 0
	movaps	XMMWORD PTR 176[rsp], xmm6
	movaps	XMMWORD PTR 192[rsp], xmm0
.L31:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xor	r12d, r12d
	mov	rdi, rax
	jmp	.L25
	.p2align 4,,10
	.p2align 3
.L21:
	mov	rcx, QWORD PTR 184[rsp]
	lea	r9, -64[rdx]
	lea	rax, 15[rcx]
	and	rax, -16
	mov	r8, rax
	sub	r8, rcx
	cmp	r9, r8
	jb	.L23
	add	rdx, rcx
	mov	QWORD PTR 184[rsp], rax
	sub	rdx, rax
	mov	QWORD PTR 192[rsp], rdx
	test	rax, rax
	je	.L23
.L24:
	sub	rdx, 64
	lea	rcx, 64[rax]
	mov	QWORD PTR 192[rsp], rdx
	mov	rdx, QWORD PTR _ZN12_GLOBAL__N_1L6g_sinkE[rip]
	mov	QWORD PTR 184[rsp], rcx
	mov	BYTE PTR [rax], r12b
	movzx	eax, r12b
	add	r12, 1
	add	rax, rdx
	mov	QWORD PTR _ZN12_GLOBAL__N_1L6g_sinkE[rip], rax
	cmp	r12, 10000
	je	.L111
.L25:
	mov	rdx, QWORD PTR 192[rsp]
	cmp	rdx, 63
	ja	.L21
.L23:
	mov	r8d, 16
	mov	edx, 64
	mov	rcx, rbx
.LEHB2:
	call	_ZNSt3pmr25monotonic_buffer_resource13_M_new_bufferEyy
.LEHE2:
	mov	rax, QWORD PTR 184[rsp]
	mov	rdx, QWORD PTR 192[rsp]
	jmp	.L24
.L11:
	mov	r14, QWORD PTR 48[rsp]
	sub	rax, r14
	mov	rdx, rax
	mov	rbx, rax
	sar	rdx, 3
	cmp	rdx, rdi
	je	.L101
	test	rdx, rdx
	mov	eax, 1
	cmovne	rax, rdx
	add	rax, rdx
	movabs	rdx, 1152921504606846975
	cmp	rax, rdx
	cmova	rax, rdx
	lea	r13, 0[0+rax*8]
	mov	rcx, r13
.LEHB3:
	call	_Znwy
.LEHE3:
	mov	QWORD PTR [rax+rbx], r12
	mov	r15, rax
	test	rbx, rbx
	je	.L14
	mov	r8, rbx
	mov	rdx, r14
	mov	rcx, rax
	call	memcpy
	mov	rbp, QWORD PTR 64[rsp]
.L14:
	lea	rbx, 8[r15+rbx]
	test	r14, r14
	je	.L15
	mov	rdx, rbp
	mov	rcx, r14
	sub	rdx, r14
	call	_ZdlPvy
.L15:
	mov	QWORD PTR 48[rsp], r15
	add	r15, r13
	mov	QWORD PTR 56[rsp], rbx
	mov	QWORD PTR 64[rsp], r15
	jmp	.L12
.L111:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r13, QWORD PTR 96[rsp]
	sub	rax, rdi
	mov	r12, rax
	mov	rax, QWORD PTR 88[rsp]
	cmp	rax, r13
	je	.L26
	mov	QWORD PTR [rax], r12
	add	rax, 8
	mov	QWORD PTR 88[rsp], rax
.L27:
	sub	rsi, 1
	jne	.L31
	lea	rax, 144[rsp]
	lea	rdx, 80[rsp]
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], rax
.LEHB4:
	call	_ZNSt6vectorIxSaIxEEC1ERKS1_
.LEHE4:
	mov	rsi, QWORD PTR 144[rsp]
	mov	r9, QWORD PTR 152[rsp]
	sub	r9, rsi
	je	.L32
	mov	r11, r9
	xor	r10d, r10d
	lea	r8, 8[rsi]
	add	r9, rsi
	sar	r11, 3
	add	r10, 1
	cmp	r10, r11
	jnb	.L32
	.p2align 4
	.p2align 3
.L112:
	mov	rax, r8
	.p2align 5
	.p2align 4
	.p2align 3
.L34:
	mov	rcx, QWORD PTR [rax]
	mov	rdx, QWORD PTR -8[r8]
	cmp	rcx, rdx
	jge	.L33
	mov	QWORD PTR -8[r8], rcx
	mov	QWORD PTR [rax], rdx
.L33:
	add	rax, 8
	cmp	rax, r9
	jne	.L34
	add	r10, 1
	add	r8, 8
	cmp	r10, r11
	jb	.L112
.L32:
	mov	rdx, QWORD PTR 160[rsp]
	mov	rcx, rsi
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rcx, rbx
	call	_ZNSt3pmr25monotonic_buffer_resourceD1Ev
	call	_ZNSt3pmr20get_default_resourceEv
	mov	rdx, QWORD PTR 40[rsp]
	pxor	xmm0, xmm0
	mov	rcx, rbx
	mov	r8, rax
	movaps	XMMWORD PTR 144[rsp], xmm0
.LEHB5:
	call	_ZNSt3pmr28unsynchronized_pool_resourceC1ERKNS_12pool_optionsEPNS_15memory_resourceE
.LEHE5:
	mov	edi, 7
.L42:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xor	esi, esi
	mov	r12, rax
	.p2align 4
	.p2align 3
.L36:
	mov	r8d, 16
	mov	edx, 64
	mov	rcx, rbx
.LEHB6:
	call	_ZNSt3pmr28unsynchronized_pool_resource11do_allocateEyy
	mov	rcx, QWORD PTR _ZN12_GLOBAL__N_1L6g_sinkE[rip]
	mov	BYTE PTR [rax], sil
	mov	rdx, rax
	movzx	eax, sil
	mov	r9d, 16
	mov	r8d, 64
	add	rax, rcx
	mov	rcx, rbx
	mov	QWORD PTR _ZN12_GLOBAL__N_1L6g_sinkE[rip], rax
	call	_ZNSt3pmr28unsynchronized_pool_resource13do_deallocateEPvyy
	add	rsi, 1
	cmp	rsi, 10000
	jne	.L36
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r15, QWORD PTR 128[rsp]
	sub	rax, r12
	mov	r14, rax
	mov	rax, QWORD PTR 120[rsp]
	cmp	rax, r15
	je	.L37
	mov	QWORD PTR [rax], r14
	add	rax, 8
	mov	QWORD PTR 120[rsp], rax
.L38:
	sub	rdi, 1
	jne	.L42
	mov	rcx, QWORD PTR 40[rsp]
	lea	rdx, 112[rsp]
	call	_ZNSt6vectorIxSaIxEEC1ERKS1_
.LEHE6:
	mov	r11, QWORD PTR 144[rsp]
	mov	r9, QWORD PTR 152[rsp]
	sub	r9, r11
	je	.L43
	mov	r10, r9
	add	rdi, 1
	lea	r8, 8[r11]
	add	r9, r11
	sar	r10, 3
	cmp	rdi, r10
	jnb	.L43
	.p2align 4
	.p2align 3
.L113:
	mov	rax, r8
	.p2align 5
	.p2align 4
	.p2align 3
.L45:
	mov	rcx, QWORD PTR [rax]
	mov	rdx, QWORD PTR -8[r8]
	cmp	rcx, rdx
	jge	.L44
	mov	QWORD PTR -8[r8], rcx
	mov	QWORD PTR [rax], rdx
.L44:
	add	rax, 8
	cmp	rax, r9
	jne	.L45
	add	rdi, 1
	add	r8, 8
	cmp	rdi, r10
	jb	.L113
.L43:
	mov	rdx, QWORD PTR 160[rsp]
	mov	rcx, r11
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rcx, rbx
	call	_ZNSt3pmr28unsynchronized_pool_resourceD1Ev
	mov	rax, QWORD PTR _ZN12_GLOBAL__N_1L6g_sinkE[rip]
	xor	edx, edx
	lea	rcx, .LC5[rip]
	test	rax, rax
	setne	dl
.LEHB7:
	call	__mingw_printf
.LEHE7:
	mov	rdx, QWORD PTR 128[rsp]
	mov	rcx, QWORD PTR 112[rsp]
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rdx, QWORD PTR 96[rsp]
	mov	rcx, QWORD PTR 80[rsp]
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rdx, QWORD PTR 64[rsp]
	mov	rcx, QWORD PTR 48[rsp]
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	nop
	movaps	xmm6, XMMWORD PTR 256[rsp]
	xor	eax, eax
	add	rsp, 280
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L26:
	mov	r15, QWORD PTR 80[rsp]
	sub	rax, r15
	mov	rdx, rax
	mov	rdi, rax
	movabs	rax, 1152921504606846975
	sar	rdx, 3
	cmp	rdx, rax
	je	.L102
	test	rdx, rdx
	mov	eax, 1
	cmovne	rax, rdx
	add	rax, rdx
	movabs	rdx, 1152921504606846975
	cmp	rax, rdx
	cmova	rax, rdx
	lea	r14, 0[0+rax*8]
	mov	rcx, r14
.LEHB8:
	call	_Znwy
.LEHE8:
	mov	QWORD PTR [rax+rdi], r12
	mov	rbp, rax
	test	rdi, rdi
	je	.L29
	mov	r8, rdi
	mov	rdx, r15
	mov	rcx, rax
	call	memcpy
	mov	r13, QWORD PTR 96[rsp]
.L29:
	lea	rdi, 8[rbp+rdi]
	test	r15, r15
	je	.L30
	mov	rdx, r13
	mov	rcx, r15
	sub	rdx, r15
	call	_ZdlPvy
.L30:
	lea	r9, 0[rbp+r14]
	mov	QWORD PTR 80[rsp], rbp
	mov	QWORD PTR 88[rsp], rdi
	mov	QWORD PTR 96[rsp], r9
	jmp	.L27
.L37:
	movabs	rcx, 1152921504606846975
	mov	rbp, QWORD PTR 112[rsp]
	sub	rax, rbp
	mov	rsi, rax
	sar	rax, 3
	cmp	rax, rcx
	je	.L103
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
	mov	QWORD PTR [rax+rsi], r14
	mov	r13, rax
	test	rsi, rsi
	je	.L40
	mov	r8, rsi
	mov	rdx, rbp
	mov	rcx, rax
	call	memcpy
	mov	r15, QWORD PTR 128[rsp]
.L40:
	lea	rsi, 8[r13+rsi]
	test	rbp, rbp
	je	.L41
	mov	rdx, r15
	mov	rcx, rbp
	sub	rdx, rbp
	call	_ZdlPvy
.L41:
	lea	r10, 0[r13+r12]
	mov	QWORD PTR 112[rsp], r13
	mov	QWORD PTR 120[rsp], rsi
	mov	QWORD PTR 128[rsp], r10
	jmp	.L38
.L95:
	jmp	.L96
.L99:
	jmp	.L100
.L97:
	jmp	.L98
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5974:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5974-.LLSDACSB5974
.LLSDACSB5974:
	.uleb128 .LEHB0-.LFB5974
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5974
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L95-.LFB5974
	.uleb128 0
	.uleb128 .LEHB2-.LFB5974
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L97-.LFB5974
	.uleb128 0
	.uleb128 .LEHB3-.LFB5974
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L95-.LFB5974
	.uleb128 0
	.uleb128 .LEHB4-.LFB5974
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L97-.LFB5974
	.uleb128 0
	.uleb128 .LEHB5-.LFB5974
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L95-.LFB5974
	.uleb128 0
	.uleb128 .LEHB6-.LFB5974
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L99-.LFB5974
	.uleb128 0
	.uleb128 .LEHB7-.LFB5974
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L95-.LFB5974
	.uleb128 0
	.uleb128 .LEHB8-.LFB5974
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L97-.LFB5974
	.uleb128 0
	.uleb128 .LEHB9-.LFB5974
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L99-.LFB5974
	.uleb128 0
.LLSDACSE5974:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	344
	.seh_savereg	rbx, 280
	.seh_savereg	rsi, 288
	.seh_savereg	rdi, 296
	.seh_savereg	rbp, 304
	.seh_savexmm	xmm6, 256
	.seh_savereg	r12, 312
	.seh_savereg	r13, 320
	.seh_savereg	r14, 328
	.seh_savereg	r15, 336
	.seh_endprologue
main.cold:
.L103:
	lea	rcx, .LC3[rip]
.LEHB10:
	call	_ZSt20__throw_length_errorPKc
.LEHE10:
.L53:
.L96:
	mov	rsi, rax
.L48:
	mov	rdx, QWORD PTR 128[rsp]
	mov	rcx, QWORD PTR 112[rsp]
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rdx, QWORD PTR 96[rsp]
	mov	rcx, QWORD PTR 80[rsp]
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rcx, QWORD PTR 48[rsp]
	mov	rdx, QWORD PTR 64[rsp]
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rcx, rsi
.LEHB11:
	call	_Unwind_Resume
.LEHE11:
.L55:
.L100:
	mov	rcx, rbx
	mov	rsi, rax
	call	_ZNSt3pmr28unsynchronized_pool_resourceD1Ev
	jmp	.L48
.L102:
	lea	rcx, .LC3[rip]
.LEHB12:
	call	_ZSt20__throw_length_errorPKc
.LEHE12:
.L101:
	lea	rcx, .LC3[rip]
.LEHB13:
	call	_ZSt20__throw_length_errorPKc
.LEHE13:
.L54:
.L98:
	mov	rcx, rbx
	mov	rsi, rax
	call	_ZNSt3pmr25monotonic_buffer_resourceD1Ev
	jmp	.L48
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5974:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5974-.LLSDACSBC5974
.LLSDACSBC5974:
	.uleb128 .LEHB10-.LCOLDB8
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L55-.LCOLDB8
	.uleb128 0
	.uleb128 .LEHB11-.LCOLDB8
	.uleb128 .LEHE11-.LEHB11
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB12-.LCOLDB8
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L54-.LCOLDB8
	.uleb128 0
	.uleb128 .LEHB13-.LCOLDB8
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L53-.LCOLDB8
	.uleb128 0
.LLSDACSEC5974:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE8:
	.section	.text.startup,"x"
.LHOTE8:
.lcomm _ZN12_GLOBAL__N_1L6g_sinkE,8,8
	.section .rdata,"dr"
	.align 16
.LC4:
	.quad	0
	.quad	1048576
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr20get_default_resourceEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr25monotonic_buffer_resource13_M_new_bufferEyy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr25monotonic_buffer_resourceD1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr28unsynchronized_pool_resourceC1ERKNS_12pool_optionsEPNS_15memory_resourceE;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr28unsynchronized_pool_resource11do_allocateEyy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr28unsynchronized_pool_resource13do_deallocateEPvyy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr28unsynchronized_pool_resourceD1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE, "dr"
	.p2align	3, 0
	.globl	.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE
	.linkonce	discard
.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE:
	.quad	_ZTVNSt3pmr25monotonic_buffer_resourceE
