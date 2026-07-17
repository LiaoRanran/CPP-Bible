	.file	"ch122_pmr_test.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt3pmr25monotonic_buffer_resource13do_deallocateEPvyy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt3pmr25monotonic_buffer_resource13do_deallocateEPvyy
	.def	_ZNSt3pmr25monotonic_buffer_resource13do_deallocateEPvyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt3pmr25monotonic_buffer_resource13do_deallocateEPvyy
_ZNSt3pmr25monotonic_buffer_resource13do_deallocateEPvyy:
.LFB2285:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt3pmr25monotonic_buffer_resource11do_allocateEyy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt3pmr25monotonic_buffer_resource11do_allocateEyy
	.def	_ZNSt3pmr25monotonic_buffer_resource11do_allocateEyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt3pmr25monotonic_buffer_resource11do_allocateEyy
_ZNSt3pmr25monotonic_buffer_resource11do_allocateEyy:
.LFB2284:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	eax, 1
	test	rdx, rdx
	cmovne	rax, rdx
	mov	rdx, QWORD PTR 16[rcx]
	mov	r9, rax
	cmp	rdx, rax
	jb	.L6
	mov	r10, QWORD PTR 8[rcx]
	mov	r11, r8
	mov	rbx, rdx
	neg	r11
	sub	rbx, r9
	lea	rax, -1[r10+r8]
	and	rax, r11
	mov	r11, rax
	sub	r11, r10
	cmp	rbx, r11
	jb	.L6
	add	rdx, r10
	mov	QWORD PTR 8[rcx], rax
	sub	rdx, rax
	mov	QWORD PTR 16[rcx], rdx
	test	rax, rax
	je	.L6
.L5:
	lea	r8, [rax+r9]
	sub	rdx, r9
	mov	QWORD PTR 8[rcx], r8
	mov	QWORD PTR 16[rcx], rdx
	add	rsp, 48
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	mov	rdx, r9
	mov	QWORD PTR 40[rsp], r9
	mov	QWORD PTR 64[rsp], rcx
	call	_ZNSt3pmr25monotonic_buffer_resource13_M_new_bufferEyy
	mov	rcx, QWORD PTR 64[rsp]
	mov	r9, QWORD PTR 40[rsp]
	mov	rax, QWORD PTR 8[rcx]
	mov	rdx, QWORD PTR 16[rcx]
	jmp	.L5
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_append\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	_Z12default_pushv
	.def	_Z12default_pushv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12default_pushv
_Z12default_pushv:
.LFB2288:
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
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	xor	ebp, ebp
	xor	esi, esi
	xor	r12d, r12d
	movabs	r13, 2305843009213693951
	xor	ebx, ebx
	jmp	.L16
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L35:
	mov	DWORD PTR [rsi], ebx
	add	ebx, 1
	add	rsi, 4
	cmp	ebx, 16
	je	.L34
.L16:
	cmp	rsi, rbp
	jne	.L35
	mov	rsi, rbp
	sub	rsi, r12
	mov	rdx, rsi
	sar	rdx, 2
	cmp	rdx, r13
	je	.L33
	test	rdx, rdx
	mov	eax, 1
	cmovne	rax, rdx
	add	rax, rdx
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	cmova	rax, rdx
	lea	rdi, 0[0+rax*4]
	mov	rcx, rdi
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	DWORD PTR [rax+rsi], ebx
	mov	r14, rax
	test	rsi, rsi
	je	.L14
	mov	r8, rsi
	mov	rdx, r12
	mov	rcx, rax
	call	memcpy
.L14:
	lea	rsi, 4[r14+rsi]
	test	r12, r12
	je	.L15
	mov	rdx, rbp
	mov	rcx, r12
	sub	rdx, r12
	call	_ZdlPvy
.L15:
	add	ebx, 1
	lea	rbp, [r14+rdi]
	mov	r12, r14
	cmp	ebx, 16
	jne	.L16
	.p2align 4
	.p2align 3
.L34:
	test	r12, r12
	je	.L10
	mov	rdx, rbp
	mov	rcx, r12
	sub	rdx, r12
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
.LEHB1:
	jmp	_ZdlPvy
.LEHE1:
	.p2align 4,,10
	.p2align 3
.L10:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
.L31:
	jmp	.L32
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2288:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2288-.LLSDACSB2288
.LLSDACSB2288:
	.uleb128 .LEHB0-.LFB2288
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L31-.LFB2288
	.uleb128 0
	.uleb128 .LEHB1-.LFB2288
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE2288:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z12default_pushv.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z12default_pushv.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 32
	.seh_savereg	rsi, 40
	.seh_savereg	rdi, 48
	.seh_savereg	rbp, 56
	.seh_savereg	r12, 64
	.seh_savereg	r13, 72
	.seh_savereg	r14, 80
	.seh_endprologue
_Z12default_pushv.cold:
.L33:
	lea	rcx, .LC0[rip]
.LEHB2:
	call	_ZSt20__throw_length_errorPKc
.LEHE2:
.L20:
.L32:
	mov	rbx, rax
	test	r12, r12
	je	.L19
	mov	rdx, rbp
	mov	rcx, r12
	sub	rdx, r12
	call	_ZdlPvy
.L19:
	mov	rcx, rbx
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2288:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2288-.LLSDACSBC2288
.LLSDACSBC2288:
	.uleb128 .LEHB2-.LCOLDB1
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L20-.LCOLDB1
	.uleb128 0
	.uleb128 .LEHB3-.LCOLDB1
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSEC2288:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text.unlikely,"x"
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4
	.globl	_Z8pmr_pushv
	.def	_Z8pmr_pushv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8pmr_pushv
_Z8pmr_pushv:
.LFB2311:
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
	sub	rsp, 1168
	.seh_stackalloc	1168
	movaps	XMMWORD PTR 1152[rsp], xmm6
	.seh_savexmm	xmm6, 1152
	.seh_endprologue
	mov	rax, QWORD PTR .refptr._ZTVNSt3pmr25monotonic_buffer_resourceE[rip]
	movabs	rsi, 2305843009213693951
	add	rax, 16
	movq	xmm6, rax
	lea	rbx, 128[rsp]
	movq	xmm1, rbx
	punpcklqdq	xmm6, xmm1
	call	_ZNSt3pmr20get_default_resourceEv
	mov	QWORD PTR 104[rsp], rbx
	xor	r8d, r8d
	xor	r9d, r9d
	mov	QWORD PTR 96[rsp], rax
	xor	r11d, r11d
	xor	r10d, r10d
	lea	rbx, 64[rsp]
	movdqa	xmm0, XMMWORD PTR .LC2[rip]
	movaps	XMMWORD PTR 64[rsp], xmm6
	mov	QWORD PTR 112[rsp], 1024
	mov	QWORD PTR 120[rsp], 0
	movaps	XMMWORD PTR 80[rsp], xmm0
	jmp	.L46
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L62:
	mov	DWORD PTR [r9], r10d
	add	r10d, 1
	add	r9, 4
	cmp	r10d, 16
	je	.L61
.L46:
	cmp	r8, r9
	jne	.L62
	mov	rdi, r8
	sub	rdi, r11
	mov	rdx, rdi
	sar	rdx, 2
	cmp	rdx, rsi
	je	.L57
	test	rdx, rdx
	mov	eax, 1
	cmovne	rax, rdx
	add	rax, rdx
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	cmova	rax, rdx
	lea	rbp, 0[0+rax*4]
	mov	rax, QWORD PTR 80[rsp]
	cmp	rax, rbp
	jb	.L42
	mov	rcx, QWORD PTR 72[rsp]
	mov	r12, rax
	sub	r12, rbp
	lea	rdx, 3[rcx]
	and	rdx, -4
	mov	r8, rdx
	sub	r8, rcx
	cmp	r12, r8
	jb	.L42
	add	rax, rcx
	mov	QWORD PTR 72[rsp], rdx
	sub	rax, rdx
	mov	QWORD PTR 80[rsp], rax
	test	rdx, rdx
	je	.L42
.L43:
	lea	r8, [rdx+rbp]
	sub	rax, rbp
	mov	QWORD PTR 72[rsp], r8
	mov	QWORD PTR 80[rsp], rax
	mov	DWORD PTR [rdx+rdi], r10d
	cmp	r9, r11
	je	.L48
	sub	r9, r11
	xor	eax, eax
	.p2align 4
	.p2align 4
	.p2align 3
.L45:
	mov	ecx, DWORD PTR [r11+rax]
	mov	DWORD PTR [rdx+rax], ecx
	add	rax, 4
	cmp	rax, r9
	jne	.L45
	add	rax, rdx
.L44:
	add	r10d, 1
	lea	r9, 4[rax]
	mov	r11, rdx
	cmp	r10d, 16
	jne	.L46
.L61:
	mov	rcx, rbx
	call	_ZNSt3pmr25monotonic_buffer_resourceD1Ev
	nop
	movaps	xmm6, XMMWORD PTR 1152[rsp]
	add	rsp, 1168
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L42:
	mov	r8d, 4
	mov	rdx, rbp
	mov	rcx, rbx
	mov	QWORD PTR 56[rsp], r9
	mov	QWORD PTR 48[rsp], r11
	mov	DWORD PTR 44[rsp], r10d
.LEHB4:
	call	_ZNSt3pmr25monotonic_buffer_resource13_M_new_bufferEyy
.LEHE4:
	mov	r10d, DWORD PTR 44[rsp]
	mov	r11, QWORD PTR 48[rsp]
	mov	r9, QWORD PTR 56[rsp]
	mov	rdx, QWORD PTR 72[rsp]
	mov	rax, QWORD PTR 80[rsp]
	jmp	.L43
	.p2align 4,,10
	.p2align 3
.L48:
	mov	rax, rdx
	jmp	.L44
.L55:
	jmp	.L56
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2311:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2311-.LLSDACSB2311
.LLSDACSB2311:
	.uleb128 .LEHB4-.LFB2311
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L55-.LFB2311
	.uleb128 0
.LLSDACSE2311:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z8pmr_pushv.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8pmr_pushv.cold
	.seh_stackalloc	1208
	.seh_savereg	rbx, 1168
	.seh_savereg	rsi, 1176
	.seh_savereg	rdi, 1184
	.seh_savereg	rbp, 1192
	.seh_savexmm	xmm6, 1152
	.seh_savereg	r12, 1200
	.seh_endprologue
_Z8pmr_pushv.cold:
.L57:
	lea	rcx, .LC0[rip]
.LEHB5:
	call	_ZSt20__throw_length_errorPKc
.LEHE5:
.L49:
.L56:
	mov	rsi, rax
	mov	rcx, rbx
	call	_ZNSt3pmr25monotonic_buffer_resourceD1Ev
	mov	rcx, rsi
.LEHB6:
	call	_Unwind_Resume
	nop
.LEHE6:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2311:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2311-.LLSDACSBC2311
.LLSDACSBC2311:
	.uleb128 .LEHB5-.LCOLDB3
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L49-.LCOLDB3
	.uleb128 0
	.uleb128 .LEHB6-.LCOLDB3
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSEC2311:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.text
.LHOTE3:
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2312:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	call	_Z12default_pushv
	call	_Z8pmr_pushv
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC2:
	.quad	1024
	.quad	1536
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt3pmr25monotonic_buffer_resource13_M_new_bufferEyy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr20get_default_resourceEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr25monotonic_buffer_resourceD1Ev;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE, "dr"
	.p2align	3, 0
	.globl	.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE
	.linkonce	discard
.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE:
	.quad	_ZTVNSt3pmr25monotonic_buffer_resourceE
