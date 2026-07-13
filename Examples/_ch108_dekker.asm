	.file	"_ch108_dekker.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZSt23__is_constant_evaluatedv,"x"
	.linkonce discard
	.globl	_ZSt23__is_constant_evaluatedv
	.def	_ZSt23__is_constant_evaluatedv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt23__is_constant_evaluatedv
_ZSt23__is_constant_evaluatedv:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	eax, 0
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZStanSt12memory_orderSt23__memory_order_modifier,"x"
	.linkonce discard
	.globl	_ZStanSt12memory_orderSt23__memory_order_modifier
	.def	_ZStanSt12memory_orderSt23__memory_order_modifier;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZStanSt12memory_orderSt23__memory_order_modifier
_ZStanSt12memory_orderSt23__memory_order_modifier:
.LFB178:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	mov	eax, DWORD PTR 24[rbp]
	and	eax, DWORD PTR 16[rbp]
	pop	rbp
	ret
	.seh_endproc
	.globl	flag0
	.bss
	.align 4
flag0:
	.space 4
	.globl	flag1
	.align 4
flag1:
	.space 4
	.globl	turn
	.align 4
turn:
	.space 4
	.text
	.globl	_Z8thread_av
	.def	_Z8thread_av;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8thread_av
_Z8thread_av:
.LFB661:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	DWORD PTR -12[rbp], 1
	mov	DWORD PTR -16[rbp], 5
	mov	eax, DWORD PTR -16[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	mov	DWORD PTR -20[rbp], eax
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L6
	cmp	DWORD PTR -20[rbp], 2
	jne	.L6
	mov	eax, 1
	jmp	.L7
.L6:
	mov	eax, 0
.L7:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L9
	cmp	DWORD PTR -20[rbp], 4
	jne	.L9
	mov	eax, 1
	jmp	.L10
.L9:
	mov	eax, 0
.L10:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L12
	cmp	DWORD PTR -20[rbp], 1
	jne	.L12
	mov	eax, 1
	jmp	.L13
.L12:
	mov	eax, 0
.L13:
	test	al, al
	mov	edx, DWORD PTR -12[rbp]
	lea	rax, flag0[rip]
	xchg	edx, DWORD PTR [rax]
	nop
	mov	DWORD PTR -4[rbp], 5
	mov	eax, DWORD PTR -4[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	mov	DWORD PTR -8[rbp], eax
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L15
	cmp	DWORD PTR -8[rbp], 3
	jne	.L15
	mov	eax, 1
	jmp	.L16
.L15:
	mov	eax, 0
.L16:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L18
	cmp	DWORD PTR -8[rbp], 4
	jne	.L18
	mov	eax, 1
	jmp	.L19
.L18:
	mov	eax, 0
.L19:
	test	al, al
	lea	rax, flag1[rip]
	mov	eax, DWORD PTR [rax]
	test	eax, eax
	nop
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z8thread_bv
	.def	_Z8thread_bv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8thread_bv
_Z8thread_bv:
.LFB662:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	DWORD PTR -12[rbp], 1
	mov	DWORD PTR -16[rbp], 5
	mov	eax, DWORD PTR -16[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	mov	DWORD PTR -20[rbp], eax
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L23
	cmp	DWORD PTR -20[rbp], 2
	jne	.L23
	mov	eax, 1
	jmp	.L24
.L23:
	mov	eax, 0
.L24:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L26
	cmp	DWORD PTR -20[rbp], 4
	jne	.L26
	mov	eax, 1
	jmp	.L27
.L26:
	mov	eax, 0
.L27:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L29
	cmp	DWORD PTR -20[rbp], 1
	jne	.L29
	mov	eax, 1
	jmp	.L30
.L29:
	mov	eax, 0
.L30:
	test	al, al
	mov	edx, DWORD PTR -12[rbp]
	lea	rax, flag1[rip]
	xchg	edx, DWORD PTR [rax]
	nop
	mov	DWORD PTR -4[rbp], 5
	mov	eax, DWORD PTR -4[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	mov	DWORD PTR -8[rbp], eax
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L32
	cmp	DWORD PTR -8[rbp], 3
	jne	.L32
	mov	eax, 1
	jmp	.L33
.L32:
	mov	eax, 0
.L33:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L35
	cmp	DWORD PTR -8[rbp], 4
	jne	.L35
	mov	eax, 1
	jmp	.L36
.L35:
	mov	eax, 0
.L36:
	test	al, al
	lea	rax, flag0[rip]
	mov	eax, DWORD PTR [rax]
	test	eax, eax
	nop
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
