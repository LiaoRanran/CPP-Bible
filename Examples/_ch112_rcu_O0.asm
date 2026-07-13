	.file	"_ch112_rcu.cpp"
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
.LFB664:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	mov	edx, 2
	lea	rax, g_config[rip]
	mov	rcx, rax
	call	_ZNKSt6atomicIP6ConfigE4loadESt12memory_order
	mov	QWORD PTR -8[rbp], rax
	mov	ecx, 8
	call	_Znwy
	mov	edx, DWORD PTR 16[rbp]
	mov	DWORD PTR [rax], edx
	mov	edx, DWORD PTR 24[rbp]
	mov	DWORD PTR 4[rax], edx
	mov	QWORD PTR -16[rbp], rax
	mov	rax, QWORD PTR -16[rbp]
	mov	r8d, 3
	mov	rdx, rax
	lea	rax, g_config[rip]
	mov	rcx, rax
	call	_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order
	mov	rax, QWORD PTR -8[rbp]
	test	rax, rax
	je	.L7
	mov	edx, 8
	mov	rcx, rax
	call	_ZdlPvy
.L7:
	nop
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.globl	rcu_read
	.def	rcu_read;	.scl	2;	.type	32;	.endef
	.seh_proc	rcu_read
rcu_read:
.LFB665:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	edx, 2
	lea	rax, g_config[rip]
	mov	rcx, rax
	call	_ZNKSt6atomicIP6ConfigE4loadESt12memory_order
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt6atomicIP6ConfigE4loadESt12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6atomicIP6ConfigE4loadESt12memory_order
	.def	_ZNKSt6atomicIP6ConfigE4loadESt12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6atomicIP6ConfigE4loadESt12memory_order
_ZNKSt6atomicIP6ConfigE4loadESt12memory_order:
.LFB777:
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
	je	.L11
	cmp	DWORD PTR -16[rbp], 3
	jne	.L11
	mov	eax, 1
	jmp	.L12
.L11:
	mov	eax, 0
.L12:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L14
	cmp	DWORD PTR -16[rbp], 4
	jne	.L14
	mov	eax, 1
	jmp	.L15
.L14:
	mov	eax, 0
.L15:
	test	al, al
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order
	.def	_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order
_ZNSt6atomicIP6ConfigE5storeES1_St12memory_order:
.LFB778:
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
	je	.L20
	cmp	DWORD PTR -24[rbp], 2
	jne	.L20
	mov	eax, 1
	jmp	.L21
.L20:
	mov	eax, 0
.L21:
	test	al, al
	call	_ZSt23__is_constant_evaluatedv
	test	al, al
	je	.L23
	cmp	DWORD PTR -24[rbp], 4
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
	cmp	DWORD PTR -24[rbp], 1
	jne	.L26
	mov	eax, 1
	jmp	.L27
.L26:
	mov	eax, 0
.L27:
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
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
