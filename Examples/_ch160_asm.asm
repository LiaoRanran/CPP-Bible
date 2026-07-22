	.file	"_ch160_asm.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN4PoolD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN4PoolD1Ev
	.def	_ZN4PoolD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4PoolD1Ev
_ZN4PoolD1Ev:
.LFB1740:
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
	je	.L2
	.p2align 4
	.p2align 3
.L3:
	mov	rcx, QWORD PTR [rbx]
	add	rbx, 8
	call	_ZdlPv
	cmp	rsi, rbx
	jne	.L3
	mov	rbx, QWORD PTR 8[rdi]
.L2:
	test	rbx, rbx
	je	.L1
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
.L1:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_append\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	_Z12hot_allocateR4Pool
	.def	_Z12hot_allocateR4Pool;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12hot_allocateR4Pool
_Z12hot_allocateR4Pool:
.LFB1742:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	r10, rcx
	test	rax, rax
	je	.L8
	mov	rcx, QWORD PTR [rax]
	mov	QWORD PTR [r10], rcx
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L8:
	mov	rcx, QWORD PTR 32[rcx]
	mov	QWORD PTR 96[rsp], r10
	sal	rcx, 12
	call	_Znwy
	mov	r10, QWORD PTR 96[rsp]
	mov	r11, rax
	mov	r9, QWORD PTR 24[r10]
	mov	rax, QWORD PTR 16[r10]
	cmp	rax, r9
	je	.L10
	mov	QWORD PTR [rax], r11
	add	QWORD PTR 16[r10], 8
.L11:
	mov	r9, QWORD PTR 32[r10]
	mov	r8, QWORD PTR [r10]
	mov	rax, r11
	mov	edx, 4096
	.p2align 5
	.p2align 4
	.p2align 3
.L15:
	mov	rcx, r8
	mov	r8, rax
	mov	QWORD PTR [rax], rcx
	add	rax, r9
	sub	rdx, 1
	jne	.L15
	mov	rax, r9
	mov	QWORD PTR [r10], rcx
	sal	rax, 12
	sub	rax, r9
	add	rax, r11
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L10:
	mov	rdx, QWORD PTR 8[r10]
	sub	rax, rdx
	mov	rbx, rdx
	mov	rdx, rax
	mov	r8, rax
	movabs	rax, 1152921504606846975
	sar	rdx, 3
	cmp	rdx, rax
	je	.L23
	test	rdx, rdx
	mov	eax, 1
	mov	QWORD PTR 56[rsp], r11
	cmovne	rax, rdx
	mov	QWORD PTR 96[rsp], r10
	mov	QWORD PTR 48[rsp], r8
	add	rax, rdx
	mov	QWORD PTR 40[rsp], r9
	movabs	rdx, 1152921504606846975
	cmp	rax, rdx
	cmova	rax, rdx
	lea	rcx, 0[0+rax*8]
	lea	rdi, 0[0+rax*8]
	call	_Znwy
	mov	r8, QWORD PTR 48[rsp]
	mov	r11, QWORD PTR 56[rsp]
	mov	r9, QWORD PTR 40[rsp]
	mov	r10, QWORD PTR 96[rsp]
	mov	rcx, rax
	mov	rsi, rax
	test	r8, r8
	mov	QWORD PTR [rax+r8], r11
	je	.L13
	mov	rdx, rbx
	mov	QWORD PTR 48[rsp], r9
	mov	QWORD PTR 40[rsp], r8
	call	memcpy
	mov	r11, QWORD PTR 56[rsp]
	mov	r10, QWORD PTR 96[rsp]
	mov	r9, QWORD PTR 48[rsp]
	mov	r8, QWORD PTR 40[rsp]
.L13:
	lea	rax, 8[rsi+r8]
	mov	rcx, rbx
	test	rbx, rbx
	je	.L14
	mov	rdx, r9
	mov	QWORD PTR 48[rsp], r11
	sub	rdx, rbx
	mov	QWORD PTR 96[rsp], r10
	mov	QWORD PTR 40[rsp], rax
	call	_ZdlPvy
	mov	r11, QWORD PTR 48[rsp]
	mov	r10, QWORD PTR 96[rsp]
	mov	rax, QWORD PTR 40[rsp]
.L14:
	mov	QWORD PTR 16[r10], rax
	lea	rax, [rsi+rdi]
	mov	QWORD PTR 8[r10], rsi
	mov	QWORD PTR 24[r10], rax
	jmp	.L11
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z12hot_allocateR4Pool.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z12hot_allocateR4Pool.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 64
	.seh_savereg	rsi, 72
	.seh_savereg	rdi, 80
	.seh_endprologue
_Z12hot_allocateR4Pool.cold:
.L23:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text.unlikely,"x"
.LCOLDB2:
	.section	.text.startup,"x"
.LHOTB2:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1743:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	call	__main
	pxor	xmm0, xmm0
	mov	ecx, 262144
	mov	QWORD PTR 56[rsp], 0
	mov	QWORD PTR 64[rsp], 64
	movups	XMMWORD PTR 40[rsp], xmm0
.LEHB0:
	call	_Znwy
	mov	ecx, 8
	mov	rbx, rax
	call	_Znwy
.LEHE0:
	lea	rdx, 8[rax]
	mov	QWORD PTR [rax], rbx
	lea	r8, 262144[rbx]
	xor	ecx, ecx
	mov	QWORD PTR 48[rsp], rdx
	mov	QWORD PTR 56[rsp], rdx
	mov	QWORD PTR 40[rsp], rax
	mov	rax, rbx
	.p2align 5
	.p2align 4
	.p2align 3
.L25:
	mov	rdx, rcx
	mov	rcx, rax
	add	rax, 64
	mov	QWORD PTR -64[rax], rdx
	cmp	rax, r8
	jne	.L25
	lea	rcx, 32[rsp]
	mov	QWORD PTR 32[rsp], rdx
	call	_ZN4PoolD1Ev
	xor	eax, eax
	add	rsp, 80
	pop	rbx
	ret
.L27:
	mov	rbx, rax
	jmp	.L26
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1743:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1743-.LLSDACSB1743
.LLSDACSB1743:
	.uleb128 .LEHB0-.LFB1743
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L27-.LFB1743
	.uleb128 0
.LLSDACSE1743:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 80
	.seh_endprologue
main.cold:
.L26:
	xor	eax, eax
	lea	rcx, 32[rsp]
	mov	QWORD PTR 32[rsp], rax
	call	_ZN4PoolD1Ev
	mov	rcx, rbx
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC1743:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC1743-.LLSDACSBC1743
.LLSDACSBC1743:
	.uleb128 .LEHB1-.LCOLDB2
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSEC1743:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE2:
	.section	.text.startup,"x"
.LHOTE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
