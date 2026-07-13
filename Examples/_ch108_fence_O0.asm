	.file	"_ch108_fence.cpp"
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
	.globl	flag
	.bss
	.align 4
flag:
	.space 4
	.globl	data
	.align 4
data:
	.space 4
	.text
	.globl	_Z8producerv
	.def	_Z8producerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8producerv
_Z8producerv:
.LFB661:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	DWORD PTR data[rip], 42
	mov	DWORD PTR -16[rbp], 3
	lock or	QWORD PTR [rsp], 0
	nop
	mov	DWORD PTR -4[rbp], 1
	mov	DWORD PTR -8[rbp], 0
	mov	eax, DWORD PTR -8[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	mov	DWORD PTR -12[rbp], eax
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L6
	cmp	DWORD PTR -12[rbp], 2
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
	cmp	DWORD PTR -12[rbp], 4
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
	cmp	DWORD PTR -12[rbp], 1
	jne	.L12
	mov	eax, 1
	jmp	.L13
.L12:
	mov	eax, 0
.L13:
	test	al, al
	mov	edx, DWORD PTR -4[rbp]
	lea	rax, flag[rip]
	xchg	edx, DWORD PTR [rax]
	nop
	nop
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z8consumerv
	.def	_Z8consumerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8consumerv
_Z8consumerv:
.LFB662:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	DWORD PTR -4[rbp], 0
	mov	eax, DWORD PTR -4[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	mov	DWORD PTR -8[rbp], eax
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L16
	cmp	DWORD PTR -8[rbp], 3
	jne	.L16
	mov	eax, 1
	jmp	.L17
.L16:
	mov	eax, 0
.L17:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L19
	cmp	DWORD PTR -8[rbp], 4
	jne	.L19
	mov	eax, 1
	jmp	.L20
.L19:
	mov	eax, 0
.L20:
	test	al, al
	lea	rax, flag[rip]
	mov	eax, DWORD PTR [rax]
	test	eax, eax
	setne	al
	test	al, al
	je	.L24
	mov	DWORD PTR -12[rbp], 2
	lock or	QWORD PTR [rsp], 0
	nop
.L24:
	nop
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
