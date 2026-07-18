	.file	"ch78_deque_test.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt11_Deque_baseIiSaIiEED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt11_Deque_baseIiSaIiEED2Ev
	.def	_ZNSt11_Deque_baseIiSaIiEED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt11_Deque_baseIiSaIiEED2Ev
_ZNSt11_Deque_baseIiSaIiEED2Ev:
.LFB1575:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rdi, rcx
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L1
	mov	rax, QWORD PTR 72[rdi]
	mov	rbx, QWORD PTR 40[rdi]
	lea	rsi, 8[rax]
	cmp	rbx, rsi
	jnb	.L3
	.p2align 4
	.p2align 3
.L4:
	mov	rcx, QWORD PTR [rbx]
	mov	edx, 512
	add	rbx, 8
	call	_ZdlPvy
	cmp	rbx, rsi
	jb	.L4
	mov	rcx, QWORD PTR [rdi]
.L3:
	mov	rdx, QWORD PTR 8[rdi]
	sal	rdx, 3
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
	.align 8
.LC0:
	.ascii "cannot create std::deque larger than max_size()\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.section	.text.startup,"x"
.LHOTB1:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1559:
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
	sub	rsp, 200
	.seh_stackalloc	200
	.seh_endprologue
	call	__main
	mov	ecx, 64
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	ecx, 512
	mov	r14, rax
	lea	rbx, 24[rax]
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	r12, rax
	mov	QWORD PTR 24[r14], rax
	lea	rax, 512[rax]
	xor	esi, esi
	mov	QWORD PTR 48[rsp], rax
	mov	rbp, rbx
	mov	r13, rax
	mov	r15, r12
	mov	QWORD PTR 128[rsp], r12
	mov	rdi, r12
	mov	QWORD PTR 56[rsp], r12
	mov	QWORD PTR 40[rsp], 8
	jmp	.L8
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L46:
	mov	DWORD PTR [rdi], esi
	add	esi, 1
	lea	r10, 4[rdi]
	cmp	esi, 200
	je	.L45
.L35:
	mov	rdi, r10
.L8:
	lea	rax, -4[r13]
	cmp	rdi, rax
	jne	.L46
	mov	r9, rbp
	mov	rcx, rdi
	sub	r9, rbx
	mov	rdx, r9
	sar	rdx, 3
	cmp	rbp, 1
	mov	rax, rdx
	adc	rax, -1
	sub	rcx, r15
	sar	rcx, 2
	sal	rax, 7
	add	rax, rcx
	mov	rcx, QWORD PTR 48[rsp]
	sub	rcx, r12
	sar	rcx, 2
	add	rax, rcx
	movabs	rcx, 4611686018427387903
	cmp	rax, rcx
	je	.L43
	mov	rax, rbp
	mov	rcx, QWORD PTR 40[rsp]
	sub	rax, r14
	sar	rax, 3
	sub	rcx, rax
	cmp	rcx, 1
	jbe	.L47
.L15:
	mov	ecx, 512
.LEHB2:
	call	_Znwy
	mov	DWORD PTR [rdi], esi
	add	esi, 1
	mov	r10, rax
	add	rbp, 8
	mov	QWORD PTR 0[rbp], rax
	lea	r13, 512[rax]
	mov	r15, rax
	cmp	esi, 200
	jne	.L35
	.p2align 4
	.p2align 3
.L45:
	mov	r11, r12
	sub	r11, QWORD PTR 56[rsp]
	mov	rcx, r12
	xor	r8d, r8d
	sar	r11, 2
	mov	rax, r11
	lea	rsi, 200[r11]
	jmp	.L29
	.p2align 4,,10
	.p2align 3
.L49:
	mov	rdx, rcx
	cmp	rax, 127
	jle	.L27
	mov	rdx, rax
	sar	rdx, 7
.L28:
	mov	rdi, rdx
	mov	r9, rax
	mov	rdx, QWORD PTR [rbx+rdx*8]
	sal	rdi, 7
	sub	r9, rdi
	lea	rdx, [rdx+r9*4]
.L27:
	add	r8d, DWORD PTR [rdx]
	add	rax, 1
	add	rcx, 4
	mov	edx, r8d
	cmp	rsi, rax
	je	.L48
.L29:
	test	rax, rax
	jns	.L49
	mov	rdx, rax
	not	rdx
	shr	rdx, 7
	not	rdx
	jmp	.L28
	.p2align 4,,10
	.p2align 3
.L48:
	add	r11, 42
	js	.L30
	add	r12, 168
	cmp	r11, 127
	jle	.L32
	mov	rax, r11
	sar	rax, 7
.L33:
	mov	rcx, rax
	mov	rax, QWORD PTR [rbx+rax*8]
	sal	rcx, 7
	sub	r11, rcx
	lea	r12, [rax+r11*4]
.L32:
	add	edx, DWORD PTR [r12]
	lea	rcx, 112[rsp]
	mov	QWORD PTR 112[rsp], r14
	mov	DWORD PTR 108[rsp], edx
	mov	eax, DWORD PTR 108[rsp]
	mov	rax, QWORD PTR 40[rsp]
	mov	QWORD PTR 152[rsp], rbx
	mov	QWORD PTR 160[rsp], r10
	mov	QWORD PTR 120[rsp], rax
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 168[rsp], r15
	mov	QWORD PTR 136[rsp], rax
	mov	rax, QWORD PTR 48[rsp]
	mov	QWORD PTR 176[rsp], r13
	mov	QWORD PTR 144[rsp], rax
	mov	QWORD PTR 184[rsp], rbp
	call	_ZNSt11_Deque_baseIiSaIiEED2Ev
	xor	eax, eax
	add	rsp, 200
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L47:
	lea	rax, 2[rdx]
	mov	r11, QWORD PTR 40[rsp]
	lea	rcx, [rax+rax]
	cmp	rcx, r11
	jnb	.L16
	mov	rdx, r11
	lea	r8, 8[rbp]
	sub	rdx, rax
	sub	r8, rbx
	mov	rax, rdx
	shr	rax
	lea	r10, [r14+rax*8]
	cmp	r10, rbx
	jnb	.L17
	cmp	r8, 8
	jle	.L18
	mov	rcx, r10
	mov	rdx, rbx
	mov	QWORD PTR 48[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 48[rsp]
	mov	r10, rax
	jmp	.L22
.L30:
	mov	rax, r11
	not	rax
	shr	rax, 7
	not	rax
	jmp	.L33
.L16:
	mov	rax, QWORD PTR 40[rsp]
	mov	r8d, 1
	mov	QWORD PTR 88[rsp], rdx
	mov	QWORD PTR 80[rsp], r9
	test	rax, rax
	cmovne	r8, rax
	add	r8, rax
	lea	rax, 2[r8]
	mov	QWORD PTR 72[rsp], r8
	lea	rcx, 0[0+rax*8]
	mov	QWORD PTR 64[rsp], rax
	call	_Znwy
.LEHE2:
	mov	r8, QWORD PTR 72[rsp]
	sub	r8, QWORD PTR 88[rsp]
	mov	r13, rax
	shr	r8
	mov	r9, QWORD PTR 80[rsp]
	lea	r10, [rax+r8*8]
	lea	r8, 8[rbp]
	sub	r8, rbx
	cmp	r8, 8
	jle	.L23
	mov	rcx, r10
	mov	rdx, rbx
	mov	QWORD PTR 48[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 48[rsp]
	mov	r10, rax
.L24:
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, r14
	mov	QWORD PTR 56[rsp], r10
	mov	r14, r13
	mov	QWORD PTR 48[rsp], r9
	sal	rdx, 3
	call	_ZdlPvy
	mov	rax, QWORD PTR 64[rsp]
	mov	r10, QWORD PTR 56[rsp]
	mov	r9, QWORD PTR 48[rsp]
	mov	QWORD PTR 40[rsp], rax
.L22:
	mov	rax, QWORD PTR [r10]
	lea	rbp, [r10+r9]
	mov	rbx, r10
	mov	r15, QWORD PTR 0[rbp]
	mov	QWORD PTR 56[rsp], rax
	add	rax, 512
	mov	QWORD PTR 48[rsp], rax
	lea	r13, 512[r15]
	jmp	.L15
.L17:
	mov	rax, r8
	sal	rax, 61
	sub	rax, r8
	lea	rcx, 8[r9+rax]
	add	rcx, r10
	cmp	r8, 8
	jle	.L20
	mov	rdx, rbx
	mov	QWORD PTR 56[rsp], r10
	mov	QWORD PTR 48[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 48[rsp]
	mov	r10, QWORD PTR 56[rsp]
	jmp	.L22
.L23:
	jne	.L24
	mov	rax, QWORD PTR [rbx]
	mov	QWORD PTR [r10], rax
	jmp	.L24
.L18:
	jne	.L22
	mov	rax, QWORD PTR [rbx]
	mov	QWORD PTR [r10], rax
	jmp	.L22
.L20:
	jne	.L22
	mov	rax, QWORD PTR [rbx]
	mov	QWORD PTR [rcx], rax
	jmp	.L22
.L38:
	jmp	.L9
.L41:
	jmp	.L42
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA1559:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT1559-.LLSDATTD1559
.LLSDATTD1559:
	.byte	0x1
	.uleb128 .LLSDACSE1559-.LLSDACSB1559
.LLSDACSB1559:
	.uleb128 .LEHB0-.LFB1559
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB1559
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L38-.LFB1559
	.uleb128 0x1
	.uleb128 .LEHB2-.LFB1559
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L41-.LFB1559
	.uleb128 0
.LLSDACSE1559:
	.byte	0x1
	.byte	0
	.byte	0
	.byte	0x7d
	.align 4
	.long	0

.LLSDATT1559:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	264
	.seh_savereg	rbx, 200
	.seh_savereg	rsi, 208
	.seh_savereg	rdi, 216
	.seh_savereg	rbp, 224
	.seh_savereg	r12, 232
	.seh_savereg	r13, 240
	.seh_savereg	r14, 248
	.seh_savereg	r15, 256
	.seh_endprologue
main.cold:
.L43:
	lea	rcx, .LC0[rip]
.LEHB3:
	call	_ZSt20__throw_length_errorPKc
.LEHE3:
.L36:
.L42:
	mov	rsi, rax
	mov	rax, QWORD PTR 40[rsp]
	lea	rcx, 112[rsp]
	mov	QWORD PTR 112[rsp], r14
	mov	QWORD PTR 152[rsp], rbx
	mov	QWORD PTR 120[rsp], rax
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 160[rsp], rdi
	mov	QWORD PTR 136[rsp], rax
	mov	rax, QWORD PTR 48[rsp]
	mov	QWORD PTR 168[rsp], r15
	mov	QWORD PTR 144[rsp], rax
	mov	QWORD PTR 176[rsp], r13
	mov	QWORD PTR 184[rsp], rbp
	call	_ZNSt11_Deque_baseIiSaIiEED2Ev
	mov	rcx, rsi
.LEHB4:
	call	_Unwind_Resume
.LEHE4:
.L9:
	mov	rcx, rax
	call	__cxa_begin_catch
.LEHB5:
	call	__cxa_rethrow
.LEHE5:
.L39:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rcx, rbx
	call	__cxa_begin_catch
	mov	edx, 64
	mov	rcx, r14
	call	_ZdlPvy
.LEHB6:
	call	__cxa_rethrow
.LEHE6:
.L37:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rcx, rbx
.LEHB7:
	call	_Unwind_Resume
	nop
.LEHE7:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDAC1559:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATTC1559-.LLSDATTDC1559
.LLSDATTDC1559:
	.byte	0x1
	.uleb128 .LLSDACSEC1559-.LLSDACSBC1559
.LLSDACSBC1559:
	.uleb128 .LEHB3-.LCOLDB1
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L36-.LCOLDB1
	.uleb128 0
	.uleb128 .LEHB4-.LCOLDB1
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB5-.LCOLDB1
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L39-.LCOLDB1
	.uleb128 0x3
	.uleb128 .LEHB6-.LCOLDB1
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L37-.LCOLDB1
	.uleb128 0
	.uleb128 .LEHB7-.LCOLDB1
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSEC1559:
	.byte	0x1
	.byte	0
	.byte	0
	.byte	0x7d
	.align 4
	.long	0

.LLSDATTC1559:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.section	.text.startup,"x"
.LHOTE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_rethrow;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
