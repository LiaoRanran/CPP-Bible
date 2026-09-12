	.file	"_atom_auto_ptr.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.def	_ZNSt8auto_ptrIiED1Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt8auto_ptrIiED1Ev.isra.0
_ZNSt8auto_ptrIiED1Ev.isra.0:
.LFB2195:
	.seh_endprologue
	test	rcx, rcx
	je	.L1
	mov	edx, 4
	jmp	_ZdlPvy
.L1:
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorISt8auto_ptrIiESaIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorISt8auto_ptrIiESaIS1_EED1Ev
	.def	_ZNSt6vectorISt8auto_ptrIiESaIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt8auto_ptrIiESaIS1_EED1Ev
_ZNSt6vectorISt8auto_ptrIiESaIS1_EED1Ev:
.LFB2013:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbx, QWORD PTR [rcx]
	mov	rdi, rcx
	cmp	rsi, rbx
	je	.L5
	.p2align 4
	.p2align 3
.L7:
	mov	rcx, QWORD PTR [rbx]
	test	rcx, rcx
	je	.L6
	mov	edx, 4
	call	_ZdlPvy
.L6:
	add	rbx, 8
	cmp	rsi, rbx
	jne	.L7
	mov	rbx, QWORD PTR [rdi]
.L5:
	test	rbx, rbx
	je	.L4
	mov	rdx, QWORD PTR 16[rdi]
	mov	rcx, rbx
	sub	rdx, rbx
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L4:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "\346\230\257\0"
	.align 8
.LC1:
	.ascii "auto_ptr \346\213\267\350\264\235\345\220\216\346\272\220\344\270\272\347\251\272=%s \347\233\256\346\240\207\345\200\274=%d\12\0"
	.align 8
.LC2:
	.ascii "\344\273\216\345\256\271\345\231\250\350\257\273\345\205\203\347\264\240\345\220\216\346\272\220\344\270\272\347\251\272=%s \345\201\267\345\210\260\345\200\274=%d\12\0"
	.align 8
.LC3:
	.ascii "unique_ptr \347\247\273\345\212\250\345\220\216\346\272\220\344\270\272\347\251\272=%s \347\233\256\346\240\207\345\200\274=%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB4:
	.section	.text.startup,"x"
.LHOTB4:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1955:
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
	mov	ecx, 4
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r8d, 42
	lea	rdx, .LC0[rip]
	lea	rcx, .LC1[rip]
	mov	rdi, rax
.LEHB1:
	call	__mingw_printf
.LEHE1:
	pxor	xmm0, xmm0
	mov	ecx, 4
	movups	XMMWORD PTR 56[rsp], xmm0
.LEHB2:
	call	_Znwy
.LEHE2:
	mov	DWORD PTR [rax], 7
	mov	ecx, 8
	mov	rsi, rax
.LEHB3:
	call	_Znwy
.LEHE3:
	mov	rbx, rax
	lea	rax, 8[rax]
	xor	ecx, ecx
	movq	xmm0, rax
	punpcklqdq	xmm0, xmm0
	movups	XMMWORD PTR 56[rsp], xmm0
	call	_ZNSt8auto_ptrIiED1Ev.isra.0
	mov	QWORD PTR [rbx], 0
	mov	r8d, 7
	lea	rdx, .LC0[rip]
	lea	rcx, .LC2[rip]
.LEHB4:
	call	__mingw_printf
	mov	r8d, 9
	lea	rdx, .LC0[rip]
	lea	rcx, .LC3[rip]
	call	__mingw_printf
.LEHE4:
	mov	rcx, rsi
	call	_ZNSt8auto_ptrIiED1Ev.isra.0
	lea	rcx, 48[rsp]
	mov	QWORD PTR 48[rsp], rbx
	call	_ZNSt6vectorISt8auto_ptrIiESaIS1_EED1Ev
	mov	rcx, rdi
	call	_ZNSt8auto_ptrIiED1Ev.isra.0
	xor	eax, eax
	add	rsp, 80
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L20:
	mov	rsi, rax
	jmp	.L19
.L23:
	jmp	.L18
.L21:
	jmp	.L17
.L22:
	mov	rsi, rax
	jmp	.L27
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1955:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1955-.LLSDACSB1955
.LLSDACSB1955:
	.uleb128 .LEHB0-.LFB1955
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB1955
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L20-.LFB1955
	.uleb128 0
	.uleb128 .LEHB2-.LFB1955
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L22-.LFB1955
	.uleb128 0
	.uleb128 .LEHB3-.LFB1955
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L21-.LFB1955
	.uleb128 0
	.uleb128 .LEHB4-.LFB1955
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L23-.LFB1955
	.uleb128 0
.LLSDACSE1955:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 80
	.seh_savereg	rsi, 88
	.seh_savereg	rdi, 96
	.seh_endprologue
main.cold:
.L17:
	mov	rcx, rsi
	mov	rsi, rax
	call	_ZNSt8auto_ptrIiED1Ev.isra.0
.L27:
	xor	ebx, ebx
.L16:
	lea	rcx, 48[rsp]
	mov	QWORD PTR 48[rsp], rbx
	call	_ZNSt6vectorISt8auto_ptrIiESaIS1_EED1Ev
.L19:
	mov	rcx, rdi
	call	_ZNSt8auto_ptrIiED1Ev.isra.0
	mov	rcx, rsi
.LEHB5:
	call	_Unwind_Resume
.LEHE5:
.L18:
	mov	rcx, rsi
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt8auto_ptrIiED1Ev.isra.0
	mov	rsi, QWORD PTR 40[rsp]
	jmp	.L16
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC1955:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC1955-.LLSDACSBC1955
.LLSDACSBC1955:
	.uleb128 .LEHB5-.LCOLDB4
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSEC1955:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE4:
	.section	.text.startup,"x"
.LHOTE4:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
