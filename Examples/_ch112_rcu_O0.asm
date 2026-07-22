	.file	"_ch112_rcu.cpp"
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
	.globl	g_config
	.bss
	.align 8
g_config:
	.space 8
	.text
	.globl	rcu_update
	.def	rcu_update;	.scl	2;	.type	32;	.endef
	.seh_proc	rcu_update
rcu_update:
.LFB669:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	lea	rax, g_config[rip]
	mov	edx, 2
	mov	rcx, rax
	call	_ZNKSt6atomicIP6ConfigE4loadESt12memory_order
	mov	QWORD PTR -8[rbp], rax
	mov	ecx, 8
	call	_Znwy
	mov	edx, DWORD PTR 16[rbp]
	mov	DWORD PTR [rax], edx
	mov	edx, DWORD PTR 24[rbp]
	mov	DWORD PTR 4[rax], edx
	mov	edx, 0
	mov	QWORD PTR -16[rbp], rax
	test	dl, dl
	je	.L4
	mov	edx, 8
	mov	rcx, rax
	call	_ZdlPvy
.L4:
	mov	rax, QWORD PTR -16[rbp]
	lea	rcx, g_config[rip]
	mov	r8d, 3
	mov	rdx, rax
	call	_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order
	mov	rax, QWORD PTR -8[rbp]
	test	rax, rax
	je	.L6
	mov	edx, 8
	mov	rcx, rax
	call	_ZdlPvy
.L6:
	nop
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.globl	rcu_read
	.def	rcu_read;	.scl	2;	.type	32;	.endef
	.seh_proc	rcu_read
rcu_read:
.LFB670:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rax, g_config[rip]
	mov	edx, 2
	mov	rcx, rax
	call	_ZNKSt6atomicIP6ConfigE4loadESt12memory_order
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "__b != memory_order_release\0"
	.align 8
.LC1:
	.ascii "_PTp* std::__atomic_base<_PTp*>::load(std::memory_order) const [with _PTp = Config; __pointer_type = Config*]\0"
	.align 8
.LC2:
	.ascii "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/atomic_base.h\0"
.LC3:
	.ascii "__b != memory_order_acq_rel\0"
	.section	.text$_ZNKSt6atomicIP6ConfigE4loadESt12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6atomicIP6ConfigE4loadESt12memory_order
	.def	_ZNKSt6atomicIP6ConfigE4loadESt12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6atomicIP6ConfigE4loadESt12memory_order
_ZNKSt6atomicIP6ConfigE4loadESt12memory_order:
.LFB782:
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
	je	.L10
	lea	rcx, .LC0[rip]
	lea	rdx, .LC1[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 827
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L10:
	cmp	DWORD PTR -16[rbp], 4
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L11
	lea	rcx, .LC3[rip]
	lea	rdx, .LC1[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 828
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L11:
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC4:
	.ascii "__b != memory_order_acquire\0"
	.align 8
.LC5:
	.ascii "void std::__atomic_base<_PTp*>::store(__pointer_type, std::memory_order) [with _PTp = Config; __pointer_type = Config*]\0"
.LC6:
	.ascii "__b != memory_order_consume\0"
	.section	.text$_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order
	.def	_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order
_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order:
.LFB783:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	DWORD PTR 32[rbp], r8d
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR -16[rbp], rax
	mov	eax, DWORD PTR 32[rbp]
	mov	DWORD PTR -20[rbp], eax
	mov	eax, DWORD PTR -20[rbp]
	mov	edx, 65535
	mov	ecx, eax
	call	_ZStanSt12memory_orderSt23__memory_order_modifier
	mov	DWORD PTR -24[rbp], eax
	cmp	DWORD PTR -24[rbp], 2
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L15
	lea	rcx, .LC4[rip]
	lea	rdx, .LC5[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 802
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L15:
	cmp	DWORD PTR -24[rbp], 4
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L16
	lea	rcx, .LC3[rip]
	lea	rdx, .LC5[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 803
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L16:
	cmp	DWORD PTR -24[rbp], 1
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L17
	lea	rcx, .LC6[rip]
	lea	rdx, .LC5[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 804
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L17:
	mov	rdx, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR -8[rbp]
	xchg	rdx, QWORD PTR [rax]
	nop
	nop
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZSt21__glibcxx_assert_failPKciS0_S0_;	.scl	2;	.type	32;	.endef
