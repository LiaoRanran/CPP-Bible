	.file	"_ch142_archetype.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt13_Bvector_baseISaIbEE13_M_deallocateEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt13_Bvector_baseISaIbEE13_M_deallocateEv
	.def	_ZNSt13_Bvector_baseISaIbEE13_M_deallocateEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt13_Bvector_baseISaIbEE13_M_deallocateEv
_ZNSt13_Bvector_baseISaIbEE13_M_deallocateEv:
.LFB1795:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L1
	mov	rdx, QWORD PTR 32[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
	mov	QWORD PTR [rbx], 0
	mov	DWORD PTR 8[rbx], 0
	mov	QWORD PTR 16[rbx], 0
	mov	DWORD PTR 24[rbx], 0
	mov	QWORD PTR 32[rbx], 0
.L1:
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector<bool>::_M_fill_insert\0"
	.section	.text$_ZNSt6vectorIbSaIbEE14_M_fill_insertESt13_Bit_iteratoryb,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIbSaIbEE14_M_fill_insertESt13_Bit_iteratoryb
	.def	_ZNSt6vectorIbSaIbEE14_M_fill_insertESt13_Bit_iteratoryb;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIbSaIbEE14_M_fill_insertESt13_Bit_iteratoryb
_ZNSt6vectorIbSaIbEE14_M_fill_insertESt13_Bit_iteratoryb:
.LFB1836:
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
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	mov	r13, QWORD PTR [rdx]
	mov	ebx, DWORD PTR 8[rdx]
	test	r8, r8
	mov	rsi, rcx
	mov	r12, r8
	mov	DWORD PTR 40[rsp], r9d
	je	.L7
	mov	r8, QWORD PTR 16[rsi]
	mov	r9, QWORD PTR [rcx]
	mov	rdx, QWORD PTR 32[rsi]
	mov	ecx, DWORD PTR 24[rcx]
	mov	rax, r8
	sub	rax, r9
	sub	rdx, r9
	lea	rax, [rcx+rax*8]
	sal	rdx, 3
	mov	r10, rcx
	sub	rdx, rax
	cmp	rdx, r12
	jnb	.L88
	movabs	rdx, 9223372036854775776
	sub	rdx, rax
	cmp	rdx, r12
	jb	.L89
	cmp	r12, rax
	mov	rdx, rax
	cmovnb	rdx, r12
	add	rax, rdx
	jc	.L35
	movabs	rdx, 9223372036854775776
	cmp	rax, rdx
	cmova	rax, rdx
	add	rax, 31
	shr	rax, 5
	sal	rax, 2
	mov	QWORD PTR 48[rsp], rax
.L36:
	mov	rcx, QWORD PTR 48[rsp]
	mov	r14, r13
	call	_Znwy
	mov	rbp, QWORD PTR [rsi]
	mov	rdi, rax
	sub	r14, rbp
	cmp	r14, 4
	jle	.L37
	mov	r8, r14
	mov	rdx, rbp
	mov	rcx, rax
	call	memmove
.L38:
	lea	r9, [rdi+r14]
	mov	r15d, ebx
	test	r15, r15
	je	.L72
	xor	edx, edx
	mov	r11, r13
	mov	r8, r15
	mov	DWORD PTR 56[rsp], ebx
	mov	r14d, 1
	mov	ecx, edx
	jmp	.L46
	.p2align 4,,10
	.p2align 3
.L91:
	add	ecx, 1
	sub	r8, 1
	je	.L90
.L46:
	mov	edx, DWORD PTR [r9]
	mov	eax, r14d
	mov	ebx, DWORD PTR [r11]
	sal	eax, cl
	mov	r10d, edx
	or	r10d, eax
	and	ebx, eax
	not	eax
	and	eax, edx
	test	ebx, ebx
	cmovne	eax, r10d
	cmp	ecx, 31
	mov	DWORD PTR [r9], eax
	jne	.L91
	add	r11, 4
	add	r9, 4
	xor	ecx, ecx
	sub	r8, 1
	jne	.L46
.L90:
	mov	ebx, DWORD PTR 56[rsp]
	mov	r10d, ecx
	mov	rdx, r10
.L41:
	add	r10, r12
	lea	rax, 31[r10]
	cmovns	rax, r10
	sar	rax, 5
	lea	r14, [r9+rax*4]
	mov	rax, r10
	sar	rax, 63
	shr	rax, 59
	add	r10, rax
	and	r10d, 31
	sub	r10, rax
	js	.L92
.L47:
	cmp	r14, r9
	mov	r12d, r10d
	je	.L48
	test	edx, edx
	je	.L49
	mov	ebp, -1
	mov	ecx, edx
	mov	r8, r14
	lea	rax, 4[r9]
	mov	r11d, ebp
	sal	r11d, cl
	sub	r8, rax
	cmp	BYTE PTR 40[rsp], 0
	mov	QWORD PTR 40[rsp], r10
	mov	ecx, DWORD PTR [r9]
	mov	edx, r11d
	je	.L50
	or	edx, ecx
	mov	rcx, rax
	mov	DWORD PTR [r9], edx
	mov	edx, -1
	call	memset
	mov	r10, QWORD PTR 40[rsp]
	test	r10, r10
	jne	.L51
	.p2align 4,,10
	.p2align 3
.L87:
	mov	rbp, QWORD PTR [rsi]
.L52:
	mov	rax, QWORD PTR 16[rsi]
	mov	edx, DWORD PTR 24[rsi]
	sub	rax, r13
	lea	r8, [rdx+rax*8]
	sub	r8, r15
	test	r8, r8
	jle	.L59
	mov	r9d, 1
	jmp	.L66
	.p2align 4,,10
	.p2align 3
.L93:
	add	ebx, 1
	cmp	r12d, 31
	je	.L64
.L94:
	add	r12d, 1
	sub	r8, 1
	je	.L59
.L66:
	mov	r10d, DWORD PTR [r14]
	mov	ecx, r12d
	mov	eax, r9d
	mov	edx, r9d
	sal	eax, cl
	mov	ecx, ebx
	sal	edx, cl
	and	edx, DWORD PTR 0[r13]
	mov	ecx, r10d
	or	ecx, eax
	not	eax
	and	eax, r10d
	test	edx, edx
	cmovne	eax, ecx
	cmp	ebx, 31
	mov	DWORD PTR [r14], eax
	jne	.L93
	add	r13, 4
	xor	ebx, ebx
	cmp	r12d, 31
	jne	.L94
.L64:
	add	r14, 4
	xor	r12d, r12d
	sub	r8, 1
	jne	.L66
.L59:
	test	rbp, rbp
	je	.L67
	mov	rdx, QWORD PTR 32[rsi]
	mov	rcx, rbp
	sub	rdx, rbp
	call	_ZdlPvy
.L67:
	mov	rax, QWORD PTR 48[rsp]
	mov	QWORD PTR [rsi], rdi
	mov	DWORD PTR 8[rsi], 0
	mov	QWORD PTR 16[rsi], r14
	mov	DWORD PTR 24[rsi], r12d
	add	rax, rdi
	mov	QWORD PTR 32[rsi], rax
.L7:
	add	rsp, 72
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
.L88:
	lea	rbp, [r12+rcx]
	lea	rax, 31[rbp]
	test	rbp, rbp
	cmovns	rax, rbp
	sar	rax, 5
	lea	rdx, [r8+rax*4]
	mov	rax, rbp
	sar	rax, 63
	mov	rdi, rdx
	shr	rax, 59
	add	rbp, rax
	and	ebp, 31
	sub	rbp, rax
	mov	r11, rbp
	js	.L95
.L10:
	mov	rax, r8
	mov	r15d, ebx
	mov	r14d, 1
	sub	rax, r13
	lea	r9, [rcx+rax*8]
	sub	r9, r15
	test	r9, r9
	jle	.L20
	mov	QWORD PTR 48[rsp], rbp
	mov	QWORD PTR 56[rsp], r15
	jmp	.L11
	.p2align 4,,10
	.p2align 3
.L97:
	sub	r10d, 1
	mov	r15d, r14d
	mov	ecx, r10d
	sal	r15d, cl
	test	r11d, r11d
	je	.L16
.L98:
	sub	r11d, 1
	mov	eax, r14d
	mov	ecx, r11d
	sal	eax, cl
.L17:
	mov	ebp, DWORD PTR [rdi]
	mov	ecx, DWORD PTR [r8]
	and	ecx, r15d
	mov	r15d, ebp
	or	r15d, eax
	not	eax
	and	eax, ebp
	test	ecx, ecx
	cmovne	eax, r15d
	sub	r9, 1
	mov	DWORD PTR [rdi], eax
	je	.L96
.L11:
	test	r10d, r10d
	jne	.L97
	sub	r8, 4
	test	r11d, r11d
	mov	r15d, -2147483648
	mov	r10d, 31
	jne	.L98
.L16:
	sub	rdi, 4
	mov	eax, -2147483648
	mov	r11d, 31
	jmp	.L17
	.p2align 4,,10
	.p2align 3
.L96:
	mov	rbp, QWORD PTR 48[rsp]
	mov	r15, QWORD PTR 56[rsp]
.L20:
	lea	rax, [r12+r15]
	lea	rcx, 31[rax]
	test	rax, rax
	cmovns	rcx, rax
	sar	rcx, 5
	lea	r14, 0[r13+rcx*4]
	mov	rcx, rax
	sar	rcx, 63
	shr	rcx, 59
	lea	rdi, [rax+rcx]
	and	edi, 31
	sub	rdi, rcx
	js	.L99
.L13:
	cmp	r13, r14
	je	.L21
	test	ebx, ebx
	je	.L22
	mov	ebp, -1
	mov	ecx, ebx
	mov	r8, r14
	mov	edx, DWORD PTR 0[r13]
	lea	r9, 4[r13]
	mov	eax, ebp
	sal	eax, cl
	sub	r8, r9
	cmp	BYTE PTR 40[rsp], 0
	je	.L23
	or	eax, edx
	mov	rcx, r9
	mov	edx, -1
	mov	DWORD PTR 0[r13], eax
	call	memset
	test	rdi, rdi
	jne	.L24
	.p2align 4,,10
	.p2align 3
.L85:
	mov	eax, DWORD PTR 24[rsi]
	mov	rcx, QWORD PTR 16[rsi]
	add	rax, r12
	lea	rdx, 31[rax]
	cmovns	rdx, rax
	sar	rdx, 5
	lea	rdx, [rcx+rdx*4]
	mov	rcx, rax
	sar	rcx, 63
	shr	rcx, 59
	lea	rbp, [rax+rcx]
	and	ebp, 31
	sub	rbp, rcx
.L25:
	test	rbp, rbp
	jns	.L32
	add	rbp, 32
	sub	rdx, 4
.L32:
	mov	QWORD PTR 16[rsi], rdx
	mov	DWORD PTR 24[rsi], ebp
	jmp	.L7
	.p2align 4,,10
	.p2align 3
.L99:
	add	rdi, 32
	sub	r14, 4
	jmp	.L13
	.p2align 4,,10
	.p2align 3
.L95:
	lea	r11, 32[rbp]
	lea	rdi, -4[rdx]
	jmp	.L10
	.p2align 4,,10
	.p2align 3
.L92:
	add	r10, 32
	sub	r14, 4
	jmp	.L47
	.p2align 4,,10
	.p2align 3
.L22:
	movzx	edx, BYTE PTR 40[rsp]
	mov	r8, r14
	mov	rcx, r13
	sub	r8, r13
	neg	edx
	call	memset
	test	rdi, rdi
	je	.L85
	mov	ecx, 32
	mov	ebp, -1
	sub	ecx, edi
	shr	ebp, cl
	cmp	BYTE PTR 40[rsp], 0
	je	.L28
.L68:
	or	DWORD PTR [r14], ebp
	jmp	.L85
	.p2align 4,,10
	.p2align 3
.L49:
	movzx	edx, BYTE PTR 40[rsp]
	mov	r8, r14
	mov	rcx, r9
	mov	QWORD PTR 56[rsp], r10
	sub	r8, r9
	neg	edx
	call	memset
	mov	r10, QWORD PTR 56[rsp]
	test	r10, r10
	je	.L87
	mov	ecx, 32
	mov	ebp, -1
	sub	ecx, r12d
	shr	ebp, cl
	cmp	BYTE PTR 40[rsp], 0
	je	.L55
.L69:
	or	DWORD PTR [r14], ebp
	mov	rbp, QWORD PTR [rsi]
	jmp	.L52
	.p2align 4,,10
	.p2align 3
.L23:
	not	eax
	mov	rcx, r9
	and	eax, edx
	xor	edx, edx
	mov	DWORD PTR 0[r13], eax
	call	memset
	test	rdi, rdi
	je	.L85
	mov	ecx, 32
	sub	ecx, edi
	shr	ebp, cl
.L28:
	not	ebp
	and	DWORD PTR [r14], ebp
	jmp	.L85
	.p2align 4,,10
	.p2align 3
.L50:
	not	edx
	and	edx, ecx
	mov	rcx, rax
	mov	DWORD PTR [r9], edx
	xor	edx, edx
	call	memset
	mov	r10, QWORD PTR 40[rsp]
	test	r10, r10
	je	.L87
	mov	ecx, 32
	sub	ecx, r12d
	shr	ebp, cl
.L55:
	not	ebp
	and	DWORD PTR [r14], ebp
	jmp	.L87
	.p2align 4,,10
	.p2align 3
.L21:
	cmp	edi, ebx
	je	.L25
	mov	r8d, -1
	mov	ecx, 32
	sub	ecx, edi
	mov	eax, r8d
	shr	eax, cl
	mov	ecx, ebx
	sal	r8d, cl
	and	eax, r8d
	mov	r8d, DWORD PTR 0[r13]
	mov	ecx, eax
	not	ecx
	and	ecx, r8d
	or	eax, r8d
	cmp	BYTE PTR 40[rsp], 0
	cmove	eax, ecx
	mov	DWORD PTR 0[r13], eax
	jmp	.L25
	.p2align 4,,10
	.p2align 3
.L48:
	cmp	edx, r10d
	je	.L52
	mov	r8d, -1
	mov	ecx, 32
	sub	ecx, r10d
	mov	eax, r8d
	shr	eax, cl
	mov	ecx, edx
	sal	r8d, cl
	mov	ecx, DWORD PTR [r14]
	and	eax, r8d
	mov	edx, eax
	not	edx
	and	edx, ecx
	or	eax, ecx
	cmp	BYTE PTR 40[rsp], 0
	cmove	eax, edx
	mov	DWORD PTR [r14], eax
	jmp	.L52
.L24:
	mov	ecx, 32
	sub	ecx, edi
	shr	ebp, cl
	jmp	.L68
.L51:
	mov	ecx, 32
	sub	ecx, r12d
	shr	ebp, cl
	jmp	.L69
	.p2align 4,,10
	.p2align 3
.L72:
	xor	r10d, r10d
	xor	edx, edx
	jmp	.L41
	.p2align 4,,10
	.p2align 3
.L37:
	jne	.L38
	mov	eax, DWORD PTR 0[rbp]
	mov	DWORD PTR [rdi], eax
	jmp	.L38
.L35:
	movabs	rax, 1152921504606846972
	mov	QWORD PTR 48[rsp], rax
	jmp	.L36
.L89:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1716:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 152
	.seh_stackalloc	152
	.seh_endprologue
	call	__main
	mov	ecx, 1536
	pxor	xmm0, xmm0
	mov	DWORD PTR 104[rsp], 0
	movups	XMMWORD PTR 72[rsp], xmm0
	lea	rbx, 96[rsp]
	movups	XMMWORD PTR 88[rsp], xmm0
	mov	QWORD PTR 112[rsp], 0
	mov	DWORD PTR 120[rsp], 0
	mov	QWORD PTR 128[rsp], 0
	mov	QWORD PTR 64[rsp], 24
.LEHB0:
	call	_Znwy
	lea	rcx, 1[rax]
	mov	r8d, 1535
	xor	edx, edx
	mov	BYTE PTR [rax], 0
	lea	rsi, 1536[rax]
	mov	rbx, rax
	call	memset
	mov	DWORD PTR 56[rsp], 0
	mov	rax, QWORD PTR 56[rsp]
	movq	xmm0, rbx
	lea	rbx, 96[rsp]
	movq	xmm1, rsi
	xor	r9d, r9d
	mov	QWORD PTR 88[rsp], rsi
	lea	rdx, 32[rsp]
	mov	r8d, 64
	mov	rcx, rbx
	punpcklqdq	xmm0, xmm1
	mov	QWORD PTR 32[rsp], 0
	movups	XMMWORD PTR 72[rsp], xmm0
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt6vectorIbSaIbEE14_M_fill_insertESt13_Bit_iteratoryb
.LEHE0:
	mov	rcx, rbx
	mov	esi, DWORD PTR 64[rsp]
	call	_ZNSt13_Bvector_baseISaIbEE13_M_deallocateEv
	mov	rcx, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L100
	mov	rdx, QWORD PTR 88[rsp]
	sub	rdx, rcx
	call	_ZdlPvy
.L100:
	mov	eax, esi
	add	rsp, 152
	pop	rbx
	pop	rsi
	ret
.L104:
	mov	rcx, rbx
	mov	rsi, rax
	call	_ZNSt13_Bvector_baseISaIbEE13_M_deallocateEv
	mov	rcx, QWORD PTR 72[rsp]
	mov	rdx, QWORD PTR 88[rsp]
	sub	rdx, rcx
	test	rcx, rcx
	je	.L103
	call	_ZdlPvy
.L103:
	mov	rcx, rsi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1716:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1716-.LLSDACSB1716
.LLSDACSB1716:
	.uleb128 .LEHB0-.LFB1716
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L104-.LFB1716
	.uleb128 0
	.uleb128 .LEHB1-.LFB1716
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE1716:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
