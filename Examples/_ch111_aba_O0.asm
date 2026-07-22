	.file	"_ch111_aba.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZStanSt12memory_orderSt23__memory_order_modifier,"x"
	.linkonce discard
	.globl	_ZStanSt12memory_orderSt23__memory_order_modifier
	.def	_ZStanSt12memory_orderSt23__memory_order_modifier;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZStanSt12memory_orderSt23__memory_order_modifier
_ZStanSt12memory_orderSt23__memory_order_modifier:
.LFB183:
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
.LFB186:
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
	je	.L4
	mov	eax, DWORD PTR 16[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	cmp	eax, 4
	je	.L4
	mov	eax, 1
	jmp	.L5
.L4:
	mov	eax, 0
.L5:
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
.LFB669:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	lea	rax, top[rip]
	mov	edx, 2
	mov	rcx, rax
	call	_ZNKSt6atomicIP4NodeE4loadESt12memory_order
	mov	QWORD PTR -16[rbp], rax
	jmp	.L8
.L10:
	mov	rax, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR -8[rbp], rax
	mov	rdx, QWORD PTR -8[rbp]
	lea	rax, -16[rbp]
	lea	rcx, top[rip]
	mov	DWORD PTR 32[rsp], 2
	mov	r9d, 4
	mov	r8, rdx
	mov	rdx, rax
	call	_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_
	test	al, al
	je	.L8
	mov	rax, QWORD PTR -16[rbp]
	jmp	.L11
.L8:
	mov	rax, QWORD PTR -16[rbp]
	test	rax, rax
	jne	.L10
	mov	eax, 0
.L11:
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "__b != memory_order_release\0"
	.align 8
.LC1:
	.ascii "_PTp* std::__atomic_base<_PTp*>::load(std::memory_order) const [with _PTp = Node; __pointer_type = Node*]\0"
	.align 8
.LC2:
	.ascii "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/atomic_base.h\0"
.LC3:
	.ascii "__b != memory_order_acq_rel\0"
	.section	.text$_ZNKSt6atomicIP4NodeE4loadESt12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6atomicIP4NodeE4loadESt12memory_order
	.def	_ZNKSt6atomicIP4NodeE4loadESt12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6atomicIP4NodeE4loadESt12memory_order
_ZNKSt6atomicIP4NodeE4loadESt12memory_order:
.LFB781:
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
	cmp	DWORD PTR -16[rbp], 3
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L13
	lea	rcx, .LC0[rip]
	lea	rdx, .LC1[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 827
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L13:
	cmp	DWORD PTR -16[rbp], 4
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L14
	lea	rcx, .LC3[rip]
	lea	rdx, .LC1[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 828
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L14:
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC4:
	.ascii "__is_valid_cmpexch_failure_order(__m2)\0"
	.align 8
.LC5:
	.ascii "bool std::__atomic_base<_PTp*>::compare_exchange_strong(_PTp*&, __pointer_type, std::memory_order, std::memory_order) [with _PTp = Node; __pointer_type = Node*]\0"
	.section	.text$_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_
	.def	_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_
_ZNSt6atomicIP4NodeE23compare_exchange_strongERS1_S1_St12memory_orderS4_:
.LFB782:
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
	mov	eax, DWORD PTR -32[rbp]
	mov	ecx, eax
	call	_ZSt32__is_valid_cmpexch_failure_orderSt12memory_order
	xor	eax, 1
	movzx	eax, al
	test	eax, eax
	setne	al
	test	al, al
	je	.L18
	lea	rcx, .LC4[rip]
	lea	rdx, .LC5[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 886
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L18:
	mov	rcx, QWORD PTR -24[rbp]
	mov	rdx, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR [rax]
	lock cmpxchg	QWORD PTR [rdx], rcx
	mov	rcx, rax
	sete	al
	test	al, al
	jne	.L23
	mov	rdx, QWORD PTR -16[rbp]
	mov	QWORD PTR [rdx], rcx
	nop
.L23:
	nop
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZSt21__glibcxx_assert_failPKciS0_S0_;	.scl	2;	.type	32;	.endef
