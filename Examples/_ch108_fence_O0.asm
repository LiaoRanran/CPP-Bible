	.file	"_ch108_fence.cpp"
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
	.globl	flag
	.bss
	.align 4
flag:
	.space 4
	.globl	data
	.align 4
data:
	.space 4
	.section .rdata,"dr"
.LC0:
	.ascii "__b != memory_order_acquire\0"
	.align 8
.LC1:
	.ascii "void std::__atomic_base<_IntTp>::store(__int_type, std::memory_order) [with _ITp = int; __int_type = int]\0"
	.align 8
.LC2:
	.ascii "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/atomic_base.h\0"
.LC3:
	.ascii "__b != memory_order_acq_rel\0"
.LC4:
	.ascii "__b != memory_order_consume\0"
	.text
	.globl	_Z8producerv
	.def	_Z8producerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8producerv
_Z8producerv:
.LFB666:
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
	cmp	DWORD PTR -12[rbp], 2
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L4
	lea	rcx, .LC0[rip]
	lea	rdx, .LC1[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 473
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L4:
	cmp	DWORD PTR -12[rbp], 4
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L5
	lea	rcx, .LC3[rip]
	lea	rdx, .LC1[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 474
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L5:
	cmp	DWORD PTR -12[rbp], 1
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L6
	lea	rcx, .LC4[rip]
	lea	rdx, .LC1[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 475
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L6:
	mov	eax, DWORD PTR -4[rbp]
	lea	rdx, flag[rip]
	xchg	eax, DWORD PTR [rdx]
	nop
	nop
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC5:
	.ascii "__b != memory_order_release\0"
	.align 8
.LC6:
	.ascii "std::__atomic_base<_IntTp>::__int_type std::__atomic_base<_IntTp>::load(std::memory_order) const [with _ITp = int; __int_type = int]\0"
	.text
	.globl	_Z8consumerv
	.def	_Z8consumerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8consumerv
_Z8consumerv:
.LFB667:
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
	cmp	DWORD PTR -8[rbp], 3
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L8
	lea	rcx, .LC5[rip]
	lea	rdx, .LC6[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 498
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L8:
	cmp	DWORD PTR -8[rbp], 4
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L9
	lea	rcx, .LC3[rip]
	lea	rdx, .LC6[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 499
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L9:
	lea	rax, flag[rip]
	mov	eax, DWORD PTR [rax]
	test	eax, eax
	setne	al
	test	al, al
	je	.L12
	mov	DWORD PTR -12[rbp], 2
	lock or	QWORD PTR [rsp], 0
	nop
.L12:
	nop
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZSt21__glibcxx_assert_failPKciS0_S0_;	.scl	2;	.type	32;	.endef
