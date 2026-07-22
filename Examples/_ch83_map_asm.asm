	.file	"_ch83_map_asm.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.def	_ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE8_M_eraseEPSt13_Rb_tree_nodeIS2_E.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE8_M_eraseEPSt13_Rb_tree_nodeIS2_E.isra.0
_ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE8_M_eraseEPSt13_Rb_tree_nodeIS2_E.isra.0:
.LFB3429:
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
	call	_ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE8_M_eraseEPSt13_Rb_tree_nodeIS2_E.isra.0
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
	.p2align 4
	.globl	_Z14probe_map_findRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi
	.def	_Z14probe_map_findRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14probe_map_findRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi
_Z14probe_map_findRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi:
.LFB3249:
	.seh_endprologue
	mov	rax, QWORD PTR 16[rcx]
	test	rax, rax
	je	.L61
	add	rcx, 8
	mov	r10, rcx
	jmp	.L60
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L67:
	mov	rax, r9
	test	rax, rax
	je	.L66
.L60:
	mov	r8, QWORD PTR 16[rax]
	mov	r9, QWORD PTR 24[rax]
	cmp	DWORD PTR 32[rax], edx
	jl	.L67
	mov	r10, rax
	mov	rax, r8
	test	rax, rax
	jne	.L60
.L66:
	cmp	rcx, r10
	je	.L57
	cmp	DWORD PTR 32[r10], edx
	jle	.L68
.L57:
	ret
	.p2align 4,,10
	.p2align 3
.L68:
	mov	eax, DWORD PTR 36[r10]
	ret
	.p2align 4,,10
	.p2align 3
.L61:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi
	.def	_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi
_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi:
.LFB3255:
	.seh_endprologue
	mov	r10, QWORD PTR 8[rcx]
	mov	r9, QWORD PTR [rcx]
	mov	rax, r10
	sub	rax, r9
	test	rax, rax
	jle	.L70
	sar	rax, 3
	jmp	.L74
	.p2align 4,,10
	.p2align 3
.L71:
	jle	.L76
.L72:
	sub	rax, rcx
	lea	r9, 8[r8]
	sub	rax, 1
	test	rax, rax
	jle	.L70
.L74:
	mov	rcx, rax
	sar	rcx
	lea	r8, [r9+rcx*8]
	cmp	edx, DWORD PTR [r8]
	jne	.L71
	mov	r11d, DWORD PTR 4[r8]
	test	r11d, r11d
	js	.L72
.L76:
	mov	rax, rcx
	test	rax, rax
	jg	.L74
.L70:
	xor	eax, eax
	cmp	r10, r9
	je	.L69
	cmp	DWORD PTR [r9], edx
	je	.L80
.L69:
	ret
	.p2align 4,,10
	.p2align 3
.L80:
	mov	eax, DWORD PTR 4[r9]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi
	.def	_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi
_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi:
.LFB3271:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	mov	r8d, edx
	cmp	QWORD PTR 24[rcx], 0
	je	.L82
	mov	r11, QWORD PTR 8[rcx]
	movsxd	rax, edx
	xor	edx, edx
	div	r11
	mov	rax, QWORD PTR [rcx]
	mov	rcx, QWORD PTR [rax+rdx*8]
	mov	rbx, rdx
	test	rcx, rcx
	je	.L92
	mov	rax, QWORD PTR [rcx]
	mov	r10d, DWORD PTR 8[rax]
	cmp	r10d, r8d
	je	.L85
.L96:
	mov	r9, QWORD PTR [rax]
	test	r9, r9
	je	.L92
	mov	r10d, DWORD PTR 8[r9]
	mov	rcx, rax
	xor	edx, edx
	movsxd	rax, r10d
	div	r11
	cmp	rdx, rbx
	jne	.L92
	mov	rax, r9
	cmp	r10d, r8d
	jne	.L96
	.p2align 4
	.p2align 3
.L85:
	mov	rdx, QWORD PTR [rcx]
	xor	eax, eax
	test	rdx, rdx
	je	.L81
	mov	eax, DWORD PTR 12[rdx]
.L81:
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L82:
	mov	rax, QWORD PTR 16[rcx]
	test	rax, rax
	jne	.L97
.L92:
	xor	eax, eax
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L97:
	add	rcx, 16
	jmp	.L86
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L98:
	mov	rdx, QWORD PTR [rax]
	mov	rcx, rax
	test	rdx, rdx
	je	.L92
	mov	rax, rdx
.L86:
	cmp	DWORD PTR 8[rax], r8d
	jne	.L98
	jmp	.L85
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3273:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	xor	ecx, ecx
	call	_ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE8_M_eraseEPSt13_Rb_tree_nodeIS2_E.isra.0
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
