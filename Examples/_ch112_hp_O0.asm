	.file	"_ch112_hp.cpp"
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
.LFB682:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
.L6:
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 2
	mov	rcx, rax
	call	_ZNKSt6atomicIPvE4loadESt12memory_order
	mov	QWORD PTR -8[rbp], rax
	mov	eax, DWORD PTR 24[rbp]
	cdqe
	lea	rdx, 0[0+rax*8]
	lea	rax, g_hp[rip]
	add	rax, rdx
	mov	rdx, QWORD PTR -8[rbp]
	mov	r8d, 5
	mov	rcx, rax
	call	_ZNSt6atomicIPvE5storeES0_St12memory_order
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 2
	mov	rcx, rax
	call	_ZNKSt6atomicIPvE4loadESt12memory_order
	cmp	QWORD PTR -8[rbp], rax
	setne	al
	test	al, al
	jne	.L6
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.globl	hp_clear
	.def	hp_clear;	.scl	2;	.type	32;	.endef
	.seh_proc	hp_clear
hp_clear:
.LFB683:
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
.LFB684:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	r8d, 2
	mov	edx, 0
	lea	rax, g_retired[rip]
	mov	rcx, rax
	call	_ZNSt6atomicIP7RetiredE8exchangeES1_St12memory_order
	mov	QWORD PTR -8[rbp], rax
	mov	QWORD PTR -16[rbp], 0
	jmp	.L10
.L18:
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR -40[rbp], rax
	mov	BYTE PTR -17[rbp], 0
	mov	DWORD PTR -24[rbp], 0
	jmp	.L11
.L14:
	mov	eax, DWORD PTR -24[rbp]
	cdqe
	lea	rdx, 0[0+rax*8]
	lea	rax, g_hp[rip]
	add	rax, rdx
	mov	edx, 2
	mov	rcx, rax
	call	_ZNKSt6atomicIPvE4loadESt12memory_order
	mov	rdx, QWORD PTR -8[rbp]
	mov	rdx, QWORD PTR [rdx]
	cmp	rax, rdx
	sete	al
	test	al, al
	je	.L12
	mov	BYTE PTR -17[rbp], 1
	jmp	.L13
.L12:
	add	DWORD PTR -24[rbp], 1
.L11:
	cmp	DWORD PTR -24[rbp], 63
	jle	.L14
.L13:
	cmp	BYTE PTR -17[rbp], 0
	je	.L15
	mov	rax, QWORD PTR -8[rbp]
	mov	rdx, QWORD PTR -16[rbp]
	mov	QWORD PTR 8[rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -16[rbp], rax
	jmp	.L16
.L15:
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	je	.L17
	mov	edx, 16
	mov	rcx, rax
	call	_ZdlPvy
.L17:
	mov	rax, QWORD PTR -8[rbp]
	test	rax, rax
	je	.L16
	mov	edx, 16
	mov	rcx, rax
	call	_ZdlPvy
.L16:
	mov	rax, QWORD PTR -40[rbp]
	mov	QWORD PTR -8[rbp], rax
.L10:
	cmp	QWORD PTR -8[rbp], 0
	jne	.L18
	cmp	QWORD PTR -16[rbp], 0
	je	.L22
	mov	rax, QWORD PTR -16[rbp]
	mov	QWORD PTR -32[rbp], rax
	jmp	.L20
.L21:
	mov	rax, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR 8[rax]
	mov	QWORD PTR -32[rbp], rax
.L20:
	mov	rax, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR 8[rax]
	test	rax, rax
	jne	.L21
	mov	edx, 0
	lea	rax, g_retired[rip]
	mov	rcx, rax
	call	_ZNKSt6atomicIP7RetiredE4loadESt12memory_order
	mov	rdx, QWORD PTR -32[rbp]
	mov	QWORD PTR 8[rdx], rax
	mov	rax, QWORD PTR -16[rbp]
	mov	r8d, 3
	mov	rdx, rax
	lea	rax, g_retired[rip]
	mov	rcx, rax
	call	_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order
.L22:
	nop
	add	rsp, 80
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt6atomicIPvE4loadESt12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6atomicIPvE4loadESt12memory_order
	.def	_ZNKSt6atomicIPvE4loadESt12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6atomicIPvE4loadESt12memory_order
_ZNKSt6atomicIPvE4loadESt12memory_order:
.LFB796:
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
	je	.L24
	cmp	DWORD PTR -16[rbp], 3
	jne	.L24
	mov	eax, 1
	jmp	.L25
.L24:
	mov	eax, 0
.L25:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L27
	cmp	DWORD PTR -16[rbp], 4
	jne	.L27
	mov	eax, 1
	jmp	.L28
.L27:
	mov	eax, 0
.L28:
	test	al, al
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt6atomicIPvE5storeES0_St12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6atomicIPvE5storeES0_St12memory_order
	.def	_ZNSt6atomicIPvE5storeES0_St12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6atomicIPvE5storeES0_St12memory_order
_ZNSt6atomicIPvE5storeES0_St12memory_order:
.LFB797:
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
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L33
	cmp	DWORD PTR -24[rbp], 2
	jne	.L33
	mov	eax, 1
	jmp	.L34
.L33:
	mov	eax, 0
.L34:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L36
	cmp	DWORD PTR -24[rbp], 4
	jne	.L36
	mov	eax, 1
	jmp	.L37
.L36:
	mov	eax, 0
.L37:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L39
	cmp	DWORD PTR -24[rbp], 1
	jne	.L39
	mov	eax, 1
	jmp	.L40
.L39:
	mov	eax, 0
.L40:
	test	al, al
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
.LFB798:
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
	mov	rax, QWORD PTR -16[rbp]
	mov	rdx, QWORD PTR -8[rbp]
	xchg	rax, QWORD PTR [rdx]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt6atomicIP7RetiredE4loadESt12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6atomicIP7RetiredE4loadESt12memory_order
	.def	_ZNKSt6atomicIP7RetiredE4loadESt12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6atomicIP7RetiredE4loadESt12memory_order
_ZNKSt6atomicIP7RetiredE4loadESt12memory_order:
.LFB799:
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
	je	.L47
	cmp	DWORD PTR -16[rbp], 3
	jne	.L47
	mov	eax, 1
	jmp	.L48
.L47:
	mov	eax, 0
.L48:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L50
	cmp	DWORD PTR -16[rbp], 4
	jne	.L50
	mov	eax, 1
	jmp	.L51
.L50:
	mov	eax, 0
.L51:
	test	al, al
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order
	.def	_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order
_ZNSt6atomicIP7RetiredE5storeES1_St12memory_order:
.LFB800:
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
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L56
	cmp	DWORD PTR -24[rbp], 2
	jne	.L56
	mov	eax, 1
	jmp	.L57
.L56:
	mov	eax, 0
.L57:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L59
	cmp	DWORD PTR -24[rbp], 4
	jne	.L59
	mov	eax, 1
	jmp	.L60
.L59:
	mov	eax, 0
.L60:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L62
	cmp	DWORD PTR -24[rbp], 1
	jne	.L62
	mov	eax, 1
	jmp	.L63
.L62:
	mov	eax, 0
.L63:
	test	al, al
	mov	rdx, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR -8[rbp]
	xchg	rdx, QWORD PTR [rax]
	nop
	nop
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
