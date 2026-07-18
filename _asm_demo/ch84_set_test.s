	.file	"ch84_set_test.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.def	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0
_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0:
.LFB1832:
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	QWORD PTR 112[rsp], rcx
	test	rcx, rcx
	je	.L1
.L19:
	mov	rax, QWORD PTR 112[rsp]
	mov	r13, QWORD PTR 24[rax]
	test	r13, r13
	je	.L3
.L18:
	mov	r14, QWORD PTR 24[r13]
	test	r14, r14
	je	.L4
.L17:
	mov	r15, QWORD PTR 24[r14]
	test	r15, r15
	je	.L5
.L16:
	mov	rbx, QWORD PTR 24[r15]
	test	rbx, rbx
	je	.L6
.L15:
	mov	rdi, QWORD PTR 24[rbx]
	test	rdi, rdi
	je	.L7
.L14:
	mov	rbp, QWORD PTR 24[rdi]
	test	rbp, rbp
	je	.L8
.L13:
	mov	rsi, QWORD PTR 24[rbp]
	test	rsi, rsi
	je	.L9
.L12:
	mov	r12, QWORD PTR 24[rsi]
	test	r12, r12
	je	.L10
.L11:
	mov	rcx, QWORD PTR 24[r12]
	call	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0
	mov	rcx, r12
	mov	r12, QWORD PTR 16[r12]
	mov	edx, 40
	call	_ZdlPvy
	test	r12, r12
	jne	.L11
.L10:
	mov	r12, QWORD PTR 16[rsi]
	mov	edx, 40
	mov	rcx, rsi
	call	_ZdlPvy
	test	r12, r12
	je	.L9
	mov	rsi, r12
	jmp	.L12
.L7:
	mov	rsi, QWORD PTR 16[rbx]
	mov	edx, 40
	mov	rcx, rbx
	call	_ZdlPvy
	test	rsi, rsi
	je	.L6
	mov	rbx, rsi
	jmp	.L15
	.p2align 4,,10
	.p2align 3
.L8:
	mov	rsi, QWORD PTR 16[rdi]
	mov	edx, 40
	mov	rcx, rdi
	call	_ZdlPvy
	test	rsi, rsi
	je	.L7
	mov	rdi, rsi
	jmp	.L14
.L6:
	mov	rbx, QWORD PTR 16[r15]
	mov	edx, 40
	mov	rcx, r15
	call	_ZdlPvy
	test	rbx, rbx
	je	.L5
	mov	r15, rbx
	jmp	.L16
	.p2align 4,,10
	.p2align 3
.L9:
	mov	rsi, QWORD PTR 16[rbp]
	mov	edx, 40
	mov	rcx, rbp
	call	_ZdlPvy
	test	rsi, rsi
	je	.L8
	mov	rbp, rsi
	jmp	.L13
.L5:
	mov	rbx, QWORD PTR 16[r14]
	mov	edx, 40
	mov	rcx, r14
	call	_ZdlPvy
	test	rbx, rbx
	je	.L4
	mov	r14, rbx
	jmp	.L17
.L4:
	mov	rbx, QWORD PTR 16[r13]
	mov	edx, 40
	mov	rcx, r13
	call	_ZdlPvy
	test	rbx, rbx
	je	.L3
	mov	r13, rbx
	jmp	.L18
.L3:
	mov	rax, QWORD PTR 112[rsp]
	mov	edx, 40
	mov	rbx, QWORD PTR 16[rax]
	mov	rcx, rax
	call	_ZdlPvy
	test	rbx, rbx
	je	.L1
	mov	QWORD PTR 112[rsp], rbx
	jmp	.L19
.L1:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.section	.text.startup,"x"
.LHOTB0:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1670:
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
	sub	rsp, 96
	.seh_stackalloc	96
	.seh_endprologue
	xor	edi, edi
	xor	esi, esi
	call	__main
	lea	rbp, 56[rsp]
	pxor	xmm0, xmm0
	mov	DWORD PTR 56[rsp], 0
	movq	xmm1, rbp
	mov	QWORD PTR 80[rsp], rbp
	mov	QWORD PTR 88[rsp], 0
	punpcklqdq	xmm0, xmm1
	movaps	XMMWORD PTR 64[rsp], xmm0
	.p2align 4
	.p2align 3
.L65:
	test	rdi, rdi
	je	.L70
	mov	rbx, rdi
	jmp	.L60
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L72:
	mov	rbx, rax
.L60:
	mov	edx, DWORD PTR 32[rbx]
	mov	rax, QWORD PTR 24[rbx]
	cmp	edx, esi
	cmovg	rax, QWORD PTR 16[rbx]
	setg	cl
	test	rax, rax
	jne	.L72
	test	cl, cl
	jne	.L58
.L61:
	cmp	esi, edx
	jle	.L63
.L62:
	mov	r12d, 1
	cmp	rbx, rbp
	jne	.L85
.L64:
	mov	ecx, 40
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	DWORD PTR 32[rax], esi
	movzx	ecx, r12b
	mov	r9, rbp
	mov	r8, rbx
	mov	rdx, rax
	call	_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
	add	QWORD PTR 88[rsp], 1
	mov	rdi, QWORD PTR 64[rsp]
.L63:
	add	esi, 1
	cmp	esi, 100
	jne	.L65
	test	rdi, rdi
	je	.L74
	mov	rax, rdi
	mov	r8, rbp
	jmp	.L68
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L87:
	mov	r8, rax
	mov	rax, rcx
	test	rax, rax
	je	.L86
.L68:
	mov	rcx, QWORD PTR 16[rax]
	mov	rdx, QWORD PTR 24[rax]
	cmp	DWORD PTR 32[rax], 41
	jg	.L87
	mov	rax, rdx
	test	rax, rax
	jne	.L68
.L86:
	cmp	r8, rbp
	je	.L66
	cmp	DWORD PTR 32[r8], 43
	cmovge	r8, rbp
.L66:
	cmp	r8, rbp
	mov	rcx, rdi
	setne	al
	mov	BYTE PTR 47[rsp], al
	movzx	eax, BYTE PTR 47[rsp]
	call	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0
	xor	eax, eax
	add	rsp, 96
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L70:
	mov	rbx, rbp
.L58:
	cmp	rbx, QWORD PTR 72[rsp]
	je	.L62
	mov	rcx, rbx
	call	_ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base
	mov	edx, DWORD PTR 32[rax]
	jmp	.L61
	.p2align 4,,10
	.p2align 3
.L85:
	cmp	DWORD PTR 32[rbx], esi
	setg	r12b
	jmp	.L64
.L74:
	mov	r8, rbp
	jmp	.L66
.L78:
	mov	rbx, rax
	jmp	.L69
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1670:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1670-.LLSDACSB1670
.LLSDACSB1670:
	.uleb128 .LEHB0-.LFB1670
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L78-.LFB1670
	.uleb128 0
.LLSDACSE1670:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	136
	.seh_savereg	rbx, 96
	.seh_savereg	rsi, 104
	.seh_savereg	rdi, 112
	.seh_savereg	rbp, 120
	.seh_savereg	r12, 128
	.seh_endprologue
main.cold:
.L69:
	mov	rcx, rdi
	call	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0
	mov	rcx, rbx
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC1670:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC1670-.LLSDACSBC1670
.LLSDACSBC1670:
	.uleb128 .LEHB1-.LCOLDB0
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSEC1670:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.section	.text.startup,"x"
.LHOTE0:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_;	.scl	2;	.type	32;	.endef
	.def	_ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
