	.file	"_ch112_hp.cpp"
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
	.section .rdata,"dr"
	.align 4
_ZL6MAX_HP:
	.long	64
	.globl	g_hp
	.bss
	.align 64
g_hp:
	.space 512
	.globl	g_retired
	.align 8
g_retired:
	.space 8
	.text
	.globl	hp_protect
	.def	hp_protect;	.scl	2;	.type	32;	.endef
	.seh_proc	hp_protect
hp_protect:
.LFB687:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
.L4:
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 2
	mov	rcx, rax
	call	_ZNKSt6atomicIPvE4loadESt12memory_order
	mov	QWORD PTR -8[rbp], rax
	mov	eax, DWORD PTR 24[rbp]
	cdqe
	lea	rdx, 0[0+rax*8]
	lea	rax, g_hp[rip]
	lea	rcx, [rdx+rax]
	mov	rax, QWORD PTR -8[rbp]
	mov	r8d, 5
	mov	rdx, rax
	call	_ZNSt6atomicIPvE5storeES0_St12memory_order
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 2
	mov	rcx, rax
	call	_ZNKSt6atomicIPvE4loadESt12memory_order
	cmp	QWORD PTR -8[rbp], rax
	setne	al
	test	al, al
	jne	.L4
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.globl	hp_clear
	.def	hp_clear;	.scl	2;	.type	32;	.endef
	.seh_proc	hp_clear
hp_clear:
.LFB688:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	eax, DWORD PTR 16[rbp]
	cdqe
	lea	rdx, 0[0+rax*8]
	lea	rax, g_hp[rip]
	add	rax, rdx
	mov	r8d, 3
	mov	edx, 0
	mov	rcx, rax
	call	_ZNSt6atomicIPvE5storeES0_St12memory_order
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	hp_scan_and_reclaim
	.def	hp_scan_and_reclaim;	.scl	2;	.type	32;	.endef
	.seh_proc	hp_scan_and_reclaim
hp_scan_and_reclaim:
.LFB689:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	lea	rax, g_retired[rip]
	mov	r8d, 2
	mov	edx, 0
	mov	rcx, rax
	call	_ZNSt6atomicIP7RetiredE8exchangeES1_St12memory_order
	mov	QWORD PTR -8[rbp], rax
	mov	QWORD PTR -16[rbp], 0
	jmp	.L8
.L16:
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR -40[rbp], rax
	mov	BYTE PTR -17[rbp], 0
	mov	DWORD PTR -24[rbp], 0
	jmp	.L9
.L12:
	mov	eax, DWORD PTR -24[rbp]
	cdqe
	lea	rdx, 0[0+rax*8]
	lea	rax, g_hp[rip]
	add	rax, rdx
	mov	edx, 2
	mov	rcx, rax
	call	_ZNKSt6atomicIPvE4loadESt12memory_order
	mov	rdx, rax
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	cmp	rdx, rax
	sete	al
	test	al, al
	je	.L10
	mov	BYTE PTR -17[rbp], 1
	jmp	.L11
.L10:
	add	DWORD PTR -24[rbp], 1
.L9:
	cmp	DWORD PTR -24[rbp], 63
	jle	.L12
.L11:
	cmp	BYTE PTR -17[rbp], 0
	je	.L13
	mov	rax, QWORD PTR -8[rbp]
	mov	rdx, QWORD PTR -16[rbp]
	mov	QWORD PTR 8[rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -16[rbp], rax
	jmp	.L14
.L13:
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	je	.L15
	mov	edx, 16
	mov	rcx, rax
	call	_ZdlPvy
.L15:
	mov	rax, QWORD PTR -8[rbp]
	test	rax, rax
	je	.L14
	mov	edx, 16
	mov	rcx, rax
	call	_ZdlPvy
.L14:
	mov	rax, QWORD PTR -40[rbp]
	mov	QWORD PTR -8[rbp], rax
.L8:
	cmp	QWORD PTR -8[rbp], 0
	jne	.L16
	cmp	QWORD PTR -16[rbp], 0
	je	.L20
	mov	rax, QWORD PTR -16[rbp]
	mov	QWORD PTR -32[rbp], rax
	jmp	.L18
.L19:
	mov	rax, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR -32[rbp], rax
.L18:
	mov	rax, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR 8[rax]
	test	rax, rax
	jne	.L19
	lea	rax, g_retired[rip]
	mov	edx, 0
	mov	rcx, rax
	call	_ZNKSt6atomicIP7RetiredE4loadESt12memory_order
	mov	rdx, QWORD PTR -32[rbp]
	mov	QWORD PTR 8[rdx], rax
	mov	rax, QWORD PTR -16[rbp]
	lea	rcx, g_retired[rip]
	mov	r8d, 3
	mov	rdx, rax
	call	_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order
.L20:
	nop
	add	rsp, 80
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "__b != memory_order_release\0"
	.align 8
.LC1:
	.ascii "_PTp* std::__atomic_base<_PTp*>::load(std::memory_order) const [with _PTp = void; __pointer_type = void*]\0"
	.align 8
.LC2:
	.ascii "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/atomic_base.h\0"
.LC3:
	.ascii "__b != memory_order_acq_rel\0"
	.section	.text$_ZNKSt6atomicIPvE4loadESt12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6atomicIPvE4loadESt12memory_order
	.def	_ZNKSt6atomicIPvE4loadESt12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6atomicIPvE4loadESt12memory_order
_ZNKSt6atomicIPvE4loadESt12memory_order:
.LFB801:
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
	je	.L22
	lea	rcx, .LC0[rip]
	lea	rdx, .LC1[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 827
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L22:
	cmp	DWORD PTR -16[rbp], 4
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L23
	lea	rcx, .LC3[rip]
	lea	rdx, .LC1[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 828
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L23:
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
	.ascii "void std::__atomic_base<_PTp*>::store(__pointer_type, std::memory_order) [with _PTp = void; __pointer_type = void*]\0"
.LC6:
	.ascii "__b != memory_order_consume\0"
	.section	.text$_ZNSt6atomicIPvE5storeES0_St12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6atomicIPvE5storeES0_St12memory_order
	.def	_ZNSt6atomicIPvE5storeES0_St12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6atomicIPvE5storeES0_St12memory_order
_ZNSt6atomicIPvE5storeES0_St12memory_order:
.LFB802:
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
	je	.L27
	lea	rcx, .LC4[rip]
	lea	rdx, .LC5[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 802
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L27:
	cmp	DWORD PTR -24[rbp], 4
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L28
	lea	rcx, .LC3[rip]
	lea	rdx, .LC5[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 803
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L28:
	cmp	DWORD PTR -24[rbp], 1
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L29
	lea	rcx, .LC6[rip]
	lea	rdx, .LC5[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 804
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L29:
	mov	rdx, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR -8[rbp]
	xchg	rdx, QWORD PTR [rax]
	nop
	nop
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt6atomicIP7RetiredE8exchangeES1_St12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6atomicIP7RetiredE8exchangeES1_St12memory_order
	.def	_ZNSt6atomicIP7RetiredE8exchangeES1_St12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6atomicIP7RetiredE8exchangeES1_St12memory_order
_ZNSt6atomicIP7RetiredE8exchangeES1_St12memory_order:
.LFB803:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
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
	mov	rdx, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR -8[rbp]
	xchg	rdx, QWORD PTR [rax]
	mov	rax, rdx
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC7:
	.ascii "_PTp* std::__atomic_base<_PTp*>::load(std::memory_order) const [with _PTp = Retired; __pointer_type = Retired*]\0"
	.section	.text$_ZNKSt6atomicIP7RetiredE4loadESt12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6atomicIP7RetiredE4loadESt12memory_order
	.def	_ZNKSt6atomicIP7RetiredE4loadESt12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6atomicIP7RetiredE4loadESt12memory_order
_ZNKSt6atomicIP7RetiredE4loadESt12memory_order:
.LFB804:
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
	je	.L35
	lea	rcx, .LC0[rip]
	lea	rdx, .LC7[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 827
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L35:
	cmp	DWORD PTR -16[rbp], 4
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L36
	lea	rcx, .LC3[rip]
	lea	rdx, .LC7[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 828
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L36:
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC8:
	.ascii "void std::__atomic_base<_PTp*>::store(__pointer_type, std::memory_order) [with _PTp = Retired; __pointer_type = Retired*]\0"
	.section	.text$_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order
	.def	_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order
_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order:
.LFB805:
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
	je	.L40
	lea	rcx, .LC4[rip]
	lea	rdx, .LC8[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 802
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L40:
	cmp	DWORD PTR -24[rbp], 4
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L41
	lea	rcx, .LC3[rip]
	lea	rdx, .LC8[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 803
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L41:
	cmp	DWORD PTR -24[rbp], 1
	sete	al
	movzx	eax, al
	test	eax, eax
	je	.L42
	lea	rcx, .LC6[rip]
	lea	rdx, .LC8[rip]
	lea	rax, .LC2[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 804
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L42:
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
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZSt21__glibcxx_assert_failPKciS0_S0_;	.scl	2;	.type	32;	.endef
