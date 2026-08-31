	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNKSt5ctypeIcE8do_widenEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt5ctypeIcE8do_widenEc
	.def	_ZNKSt5ctypeIcE8do_widenEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt5ctypeIcE8do_widenEc
_ZNKSt5ctypeIcE8do_widenEc:
.LFB2312:
	.seh_endprologue
	mov	eax, edx
	ret
	.seh_endproc
	.text
	.p2align 4
	.def	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB3698:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR -24[rax]
	mov	rbx, rcx
	mov	rsi, QWORD PTR 240[rcx+rax]
	test	rsi, rsi
	je	.L8
	cmp	BYTE PTR 56[rsi], 0
	je	.L5
	movsx	edx, BYTE PTR 67[rsi]
.L6:
	mov	rcx, rbx
	call	_ZNSo3putEc
	mov	rcx, rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZNSo5flushEv
.L5:
	mov	rcx, rsi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rsi]
	mov	edx, 10
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L6
	mov	edx, 10
	mov	rcx, rsi
	call	rax
	movsx	edx, al
	jmp	.L6
.L8:
	call	_ZSt16__throw_bad_castv
	nop
	.seh_endproc
	.section	.text$_ZN4PoolD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN4PoolD1Ev
	.def	_ZN4PoolD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4PoolD1Ev
_ZN4PoolD1Ev:
.LFB2956:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, QWORD PTR 8[rcx]
	mov	rsi, QWORD PTR 16[rcx]
	mov	rdi, rcx
	cmp	rsi, rbx
	je	.L10
	.p2align 4,,10
	.p2align 3
.L11:
	mov	rcx, QWORD PTR [rbx]
	add	rbx, 8
	call	free
	cmp	rbx, rsi
	jne	.L11
	mov	rbx, QWORD PTR 8[rdi]
.L10:
	test	rbx, rbx
	je	.L9
	mov	rdx, QWORD PTR 24[rdi]
	mov	rcx, rbx
	sub	rdx, rbx
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L9:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorIPvSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIPvSaIS0_EED1Ev
	.def	_ZNSt6vectorIPvSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIPvSaIS0_EED1Ev
_ZNSt6vectorIPvSaIS0_EED1Ev:
.LFB3274:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L14
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L14:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::reserve\0"
.LC1:
	.ascii "vector::_M_realloc_insert\0"
	.section	.text$_ZN4PoolC1Ey,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN4PoolC1Ey
	.def	_ZN4PoolC1Ey;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4PoolC1Ey
_ZN4PoolC1Ey:
.LFB2947:
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
	sub	rsp, 56
	.seh_stackalloc	56
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	pxor	xmm0, xmm0
	movabs	rax, 1152921504606846975
	cmp	rax, rdx
	mov	rbx, rcx
	mov	rbp, rdx
	movups	XMMWORD PTR [rcx], xmm0
	movups	XMMWORD PTR 16[rcx], xmm0
	jb	.L48
	test	rdx, rdx
	jne	.L49
.L16:
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 56
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
.L49:
	lea	r12, 0[0+rdx*8]
	mov	rcx, r12
.LEHB0:
	call	_Znwy
	mov	rdi, QWORD PTR 8[rbx]
	movq	xmm2, rax
	mov	rsi, rax
	mov	r8, QWORD PTR 16[rbx]
	movddup	xmm6, xmm2
	sub	r8, rdi
	test	r8, r8
	jg	.L50
	test	rdi, rdi
	jne	.L51
.L21:
	add	rsi, r12
	movups	XMMWORD PTR 8[rbx], xmm6
	xor	edi, edi
	movabs	r12, 1152921504606846975
	mov	QWORD PTR 24[rbx], rsi
	jmp	.L33
	.p2align 4,,10
	.p2align 3
.L52:
	mov	QWORD PTR [rax], rsi
	add	rax, 8
	mov	QWORD PTR 16[rbx], rax
.L23:
	add	rdi, 1
	cmp	rbp, rdi
	je	.L16
.L33:
	mov	ecx, 16
	call	malloc
	mov	rsi, rax
	mov	rax, QWORD PTR [rbx]
	mov	QWORD PTR [rbx], rsi
	mov	QWORD PTR [rsi], rax
	mov	rax, QWORD PTR 16[rbx]
	cmp	rax, QWORD PTR 24[rbx]
	jne	.L52
	mov	r13, QWORD PTR 8[rbx]
	mov	r14, rax
	sub	r14, r13
	mov	rdx, r14
	sar	rdx, 3
	cmp	rdx, r12
	je	.L53
	cmp	rax, r13
	je	.L54
	lea	rax, [rdx+rdx]
	cmp	rax, rdx
	jb	.L37
	xor	r15d, r15d
	xor	ecx, ecx
	test	rax, rax
	jne	.L55
.L29:
	lea	rax, 8[rcx+r14]
	movq	xmm6, rcx
	test	r14, r14
	mov	QWORD PTR [rcx+r14], rsi
	movq	xmm1, rax
	punpcklqdq	xmm6, xmm1
	jg	.L56
	test	r13, r13
	jne	.L57
.L32:
	movups	XMMWORD PTR 8[rbx], xmm6
	mov	QWORD PTR 24[rbx], r15
	jmp	.L23
	.p2align 4,,10
	.p2align 3
.L50:
	mov	rdx, rdi
	mov	rcx, rax
	call	memmove
	mov	rdx, QWORD PTR 24[rbx]
	sub	rdx, rdi
.L20:
	mov	rcx, rdi
	call	_ZdlPvy
	jmp	.L21
	.p2align 4,,10
	.p2align 3
.L56:
	mov	rdx, r13
	mov	r8, r14
	call	memmove
	mov	rdx, QWORD PTR 24[rbx]
	sub	rdx, r13
.L31:
	mov	rcx, r13
	call	_ZdlPvy
	jmp	.L32
	.p2align 4,,10
	.p2align 3
.L54:
	add	rdx, 1
	jc	.L37
	movabs	rax, 1152921504606846975
	cmp	rdx, rax
	cmova	rdx, rax
	lea	r15, 0[0+rdx*8]
.L28:
	mov	rcx, r15
	call	_Znwy
	mov	rcx, rax
	add	r15, rax
	jmp	.L29
	.p2align 4,,10
	.p2align 3
.L37:
	movabs	r15, 9223372036854775800
	jmp	.L28
	.p2align 4,,10
	.p2align 3
.L57:
	mov	rdx, QWORD PTR 24[rbx]
	sub	rdx, r13
	jmp	.L31
.L55:
	movabs	rdx, 1152921504606846975
	cmp	rax, rdx
	cmova	rax, rdx
	lea	r15, 0[0+rax*8]
	jmp	.L28
.L51:
	mov	rdx, QWORD PTR 24[rbx]
	sub	rdx, rdi
	jmp	.L20
.L53:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
.L48:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE0:
.L39:
	lea	rcx, 8[rbx]
	mov	rsi, rax
	call	_ZNSt6vectorIPvSaIS0_EED1Ev
	mov	rcx, rsi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2947:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2947-.LLSDACSB2947
.LLSDACSB2947:
	.uleb128 .LEHB0-.LFB2947
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L39-.LFB2947
	.uleb128 0
	.uleb128 .LEHB1-.LFB2947
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE2947:
	.section	.text$_ZN4PoolC1Ey,"x"
	.linkonce discard
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC2:
	.ascii "C:\\Users\\ASUS\\AppData\\Local\\Temp\\tmp40r8z951\\s.cpp\0"
.LC3:
	.ascii "p != nullptr\0"
.LC4:
	.ascii "pool.free_list == nullptr\0"
	.align 8
.LC5:
	.ascii "static_cast<Node*>(ptrs[i])->tag == i\0"
.LC6:
	.ascii "pool.free_list != nullptr\0"
.LC7:
	.ascii "all functional checks passed\0"
.LC8:
	.ascii "ok\0"
.LC9:
	.ascii "pool reused addr : \0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2957:
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
	sub	rsp, 136
	.seh_stackalloc	136
	movaps	XMMWORD PTR 112[rsp], xmm6
	.seh_savexmm	xmm6, 112
	.seh_endprologue
	call	__main
	lea	rax, 80[rsp]
	mov	edx, 1000
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], rax
.LEHB2:
	call	_ZN4PoolC1Ey
.LEHE2:
	mov	ecx, 8000
	mov	QWORD PTR 48[rsp], 0
	mov	QWORD PTR 56[rsp], 0
	mov	QWORD PTR 64[rsp], 0
.LEHB3:
	call	_Znwy
	movq	xmm2, rax
	add	rax, 8000
	xor	edi, edi
	mov	rsi, QWORD PTR 80[rsp]
	movddup	xmm0, xmm2
	mov	QWORD PTR 64[rsp], rax
	movabs	r15, 1152921504606846975
	movaps	XMMWORD PTR 48[rsp], xmm0
	jmp	.L71
	.p2align 4,,10
	.p2align 3
.L59:
	mov	rbx, QWORD PTR 56[rsp]
	mov	DWORD PTR 8[rsi], edi
	mov	r12, QWORD PTR 64[rsp]
	mov	rbp, QWORD PTR [rsi]
	cmp	rbx, r12
	mov	QWORD PTR 80[rsp], rbp
	je	.L60
	add	edi, 1
	mov	QWORD PTR [rbx], rsi
	add	rbx, 8
	cmp	edi, 1000
	mov	QWORD PTR 56[rsp], rbx
	je	.L99
.L85:
	mov	rsi, rbp
.L71:
	test	rsi, rsi
	jne	.L59
	lea	rdx, .LC2[rip]
	mov	r8d, 30
	lea	rcx, .LC3[rip]
	call	[QWORD PTR __imp__assert[rip]]
	.p2align 4,,10
	.p2align 3
.L60:
	mov	r14, QWORD PTR 48[rsp]
	sub	rbx, r14
	mov	r13, rbx
	sar	r13, 3
	cmp	r13, r15
	je	.L100
	cmp	r12, r14
	je	.L101
	lea	rax, [r13+r13]
	cmp	rax, r13
	jb	.L83
	xor	r13d, r13d
	xor	ecx, ecx
	test	rax, rax
	jne	.L102
.L67:
	lea	rax, 8[rcx+rbx]
	movq	xmm6, rcx
	test	rbx, rbx
	mov	QWORD PTR [rcx+rbx], rsi
	movq	xmm1, rax
	punpcklqdq	xmm6, xmm1
	jg	.L103
	test	r14, r14
	jne	.L69
.L70:
	add	edi, 1
	movaps	XMMWORD PTR 48[rsp], xmm6
	cmp	edi, 1000
	mov	QWORD PTR 64[rsp], r13
	jne	.L85
.L99:
	test	rbp, rbp
	jne	.L104
	mov	rcx, QWORD PTR 48[rsp]
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L74:
	mov	rdx, QWORD PTR [rcx+rax*8]
	cmp	DWORD PTR 8[rdx], eax
	jne	.L105
	add	rax, 1
	cmp	rax, 1000
	jne	.L74
	mov	rdx, QWORD PTR 56[rsp]
	mov	rax, rcx
	cmp	rcx, rdx
	je	.L106
	.p2align 4,,10
	.p2align 3
.L76:
	mov	r8, rbp
	mov	rbp, QWORD PTR [rax]
	add	rax, 8
	cmp	rdx, rax
	mov	QWORD PTR 0[rbp], r8
	jne	.L76
	mov	QWORD PTR 80[rsp], r8
	jmp	.L78
	.p2align 4,,10
	.p2align 3
.L108:
	add	rcx, 8
	cmp	rdx, rcx
	je	.L107
.L78:
	cmp	QWORD PTR [rcx], rbp
	jne	.L108
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC9[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	edx, 1
	call	_ZNSo9_M_insertIbEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC7[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rcx, 48[rsp]
	call	_ZNSt6vectorIPvSaIS0_EED1Ev
	mov	rcx, QWORD PTR 40[rsp]
	call	_ZN4PoolD1Ev
	nop
	movaps	xmm6, XMMWORD PTR 112[rsp]
	xor	eax, eax
	add	rsp, 136
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
.L103:
	mov	r8, rbx
	mov	rdx, r14
	call	memmove
.L69:
	mov	rdx, r12
	mov	rcx, r14
	sub	rdx, r14
	call	_ZdlPvy
	jmp	.L70
	.p2align 4,,10
	.p2align 3
.L101:
	add	r13, 1
	jc	.L83
	movabs	rax, 1152921504606846975
	cmp	r13, rax
	cmova	r13, rax
	sal	r13, 3
.L66:
	mov	rcx, r13
	call	_Znwy
	mov	rcx, rax
	add	r13, rax
	jmp	.L67
	.p2align 4,,10
	.p2align 3
.L83:
	movabs	r13, 9223372036854775800
	jmp	.L66
.L102:
	movabs	rdx, 1152921504606846975
	cmp	rax, rdx
	cmova	rax, rdx
	lea	r13, 0[0+rax*8]
	jmp	.L66
.L106:
	lea	rdx, .LC2[rip]
	mov	r8d, 40
	lea	rcx, .LC6[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L105:
	lea	rdx, .LC2[rip]
	mov	r8d, 37
	lea	rcx, .LC5[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L100:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
.L107:
	lea	rdx, .LC2[rip]
	mov	r8d, 44
	lea	rcx, .LC8[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L104:
	lea	rdx, .LC2[rip]
	mov	r8d, 34
	lea	rcx, .LC4[rip]
	call	[QWORD PTR __imp__assert[rip]]
.LEHE3:
.L86:
	lea	rcx, 48[rsp]
	mov	rbx, rax
	call	_ZNSt6vectorIPvSaIS0_EED1Ev
	mov	rcx, QWORD PTR 40[rsp]
	call	_ZN4PoolD1Ev
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2957:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2957-.LLSDACSB2957
.LLSDACSB2957:
	.uleb128 .LEHB2-.LFB2957
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB3-.LFB2957
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L86-.LFB2957
	.uleb128 0
	.uleb128 .LEHB4-.LFB2957
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE2957:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIbEERSoT_;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
