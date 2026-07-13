	.file	"_ch111_aba.cpp"
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
	.section	.text$_ZSt32__is_valid_cmpexch_failure_orderSt12memory_order,"x"
	.linkonce discard
	.globl	_ZSt32__is_valid_cmpexch_failure_orderSt12memory_order
	.def	_ZSt32__is_valid_cmpexch_failure_orderSt12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt32__is_valid_cmpexch_failure_orderSt12memory_order
_ZSt32__is_valid_cmpexch_failure_orderSt12memory_order:
.LFB181:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	eax, DWORD PTR 16[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	cmp	eax, 3
	je	.L6
	mov	eax, DWORD PTR 16[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	cmp	eax, 4
	je	.L6
	mov	eax, 1
	jmp	.L7
.L6:
	mov	eax, 0
.L7:
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	top
	.bss
	.align 8
top:
	.space 8
	.text
	.globl	_Z10pop_unsafev
	.def	_Z10pop_unsafev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10pop_unsafev
_Z10pop_unsafev:
.LFB664:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	edx, 2
	lea	rax, top[rip]
	mov	rcx, rax
	call	_ZNKSt6atomicIP4NodeE4loadESt12memory_order
	mov	QWORD PTR -16[rbp], rax
	jmp	.L10
.L12:
	mov	rax, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR -8[rbp], rax
	mov	rdx, QWORD PTR -8[rbp]
	lea	rax, -16[rbp]
	mov	DWORD PTR 32[rsp], 2
	mov	r9d, 4
	mov	r8, rdx
	mov	rdx, rax
	lea	rax, top[rip]
	mov	rcx, rax
	call	_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_
	test	al, al
	je	.L10
	mov	rax, QWORD PTR -16[rbp]
	jmp	.L13
.L10:
	mov	rax, QWORD PTR -16[rbp]
	test	rax, rax
	jne	.L12
	mov	eax, 0
.L13:
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt6atomicIP4NodeE4loadESt12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6atomicIP4NodeE4loadESt12memory_order
	.def	_ZNKSt6atomicIP4NodeE4loadESt12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6atomicIP4NodeE4loadESt12memory_order
_ZNKSt6atomicIP4NodeE4loadESt12memory_order:
.LFB776:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	eax, DWORD PTR 24[rbp]
	mov	DWORD PTR -12[rbp], eax
	mov	eax, DWORD PTR -12[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	mov	DWORD PTR -16[rbp], eax
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L15
	cmp	DWORD PTR -16[rbp], 3
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
	cmp	DWORD PTR -16[rbp], 4
	jne	.L18
	mov	eax, 1
	jmp	.L19
.L18:
	mov	eax, 0
.L19:
	test	al, al
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_
	.def	_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_
_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_:
.LFB777:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	DWORD PTR 40[rbp], r9d
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR -16[rbp], rax
	mov	rax, QWORD PTR 32[rbp]
	mov	QWORD PTR -24[rbp], rax
	mov	eax, DWORD PTR 40[rbp]
	mov	DWORD PTR -28[rbp], eax
	mov	eax, DWORD PTR 48[rbp]
	mov	DWORD PTR -32[rbp], eax
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L24
	mov	eax, DWORD PTR -32[rbp]
	mov	ecx, eax
	call	_ZSt32__is_valid_cmpexch_failure_orderSt12memory_order
	xor	eax, 1
	test	al, al
	je	.L24
	mov	eax, 1
	jmp	.L25
.L24:
	mov	eax, 0
.L25:
	test	al, al
	mov	rdx, QWORD PTR -24[rbp]
	mov	rcx, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR [rax]
	lock cmpxchg	QWORD PTR [rcx], rdx
	mov	rdx, rax
	sete	al
	test	al, al
	jne	.L31
	mov	rcx, QWORD PTR -16[rbp]
	mov	QWORD PTR [rcx], rdx
	nop
.L31:
	nop
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
