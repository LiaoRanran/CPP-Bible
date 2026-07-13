	.file	"_ch83_map_asm.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.def	_ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE8_M_eraseEPSt13_Rb_tree_nodeIS2_E.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE8_M_eraseEPSt13_Rb_tree_nodeIS2_E.isra.0
_ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE8_M_eraseEPSt13_Rb_tree_nodeIS2_E.isra.0:
.LFB3458:
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
	test	rcx, rcx
	mov	QWORD PTR 112[rsp], rcx
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
	mov	rsi, QWORD PTR 24[rbx]
	test	rsi, rsi
	je	.L7
.L14:
	mov	rbp, QWORD PTR 24[rsi]
	test	rbp, rbp
	je	.L8
.L13:
	mov	rdi, QWORD PTR 24[rbp]
	test	rdi, rdi
	je	.L9
.L12:
	mov	r12, QWORD PTR 24[rdi]
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
	mov	r12, QWORD PTR 16[rdi]
	mov	edx, 40
	mov	rcx, rdi
	call	_ZdlPvy
	test	r12, r12
	je	.L9
	mov	rdi, r12
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
	mov	rdi, QWORD PTR 16[rsi]
	mov	edx, 40
	mov	rcx, rsi
	call	_ZdlPvy
	test	rdi, rdi
	je	.L7
	mov	rsi, rdi
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
	mov	rdi, QWORD PTR 16[rbp]
	mov	edx, 40
	mov	rcx, rbp
	call	_ZdlPvy
	test	rdi, rdi
	je	.L8
	mov	rbp, rdi
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
.LFB3277:
	.seh_endprologue
	mov	rax, QWORD PTR 16[rcx]
	lea	r10, 8[rcx]
	test	rax, rax
	je	.L62
	mov	r9, r10
	jmp	.L60
	.p2align 4,,10
	.p2align 3
.L67:
	mov	r9, rax
	mov	rax, r8
	test	rax, rax
	je	.L66
.L60:
	cmp	DWORD PTR 32[rax], edx
	mov	r8, QWORD PTR 16[rax]
	mov	rcx, QWORD PTR 24[rax]
	jge	.L67
	mov	rax, rcx
	test	rax, rax
	jne	.L60
.L66:
	cmp	r10, r9
	je	.L57
	cmp	DWORD PTR 32[r9], edx
	jle	.L61
.L57:
	ret
	.p2align 4,,10
	.p2align 3
.L61:
	mov	eax, DWORD PTR 36[r9]
	ret
	.p2align 4,,10
	.p2align 3
.L62:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi
	.def	_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi
_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi:
.LFB3281:
	.seh_endprologue
	mov	r10, QWORD PTR 8[rcx]
	mov	r9, QWORD PTR [rcx]
	mov	rcx, r10
	sub	rcx, r9
	mov	rax, rcx
	sar	rax, 3
	test	rcx, rcx
	jg	.L73
	jmp	.L69
	.p2align 4,,10
	.p2align 3
.L70:
	jle	.L75
.L71:
	lea	r9, 8[rcx]
	sub	rax, r8
	sub	rax, 1
	test	rax, rax
	jle	.L69
.L73:
	mov	r8, rax
	sar	r8
	lea	rcx, [r9+r8*8]
	cmp	edx, DWORD PTR [rcx]
	jne	.L70
	mov	r11d, DWORD PTR 4[rcx]
	test	r11d, r11d
	js	.L71
.L75:
	mov	rax, r8
	test	rax, rax
	jg	.L73
.L69:
	xor	eax, eax
	cmp	r10, r9
	je	.L68
	cmp	DWORD PTR [r9], edx
	je	.L79
.L68:
	ret
	.p2align 4,,10
	.p2align 3
.L79:
	mov	eax, DWORD PTR 4[r9]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi
	.def	_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi
_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi:
.LFB3291:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	cmp	QWORD PTR 24[rcx], 0
	mov	r8d, edx
	jne	.L81
	mov	rax, QWORD PTR 16[rcx]
	test	rax, rax
	jne	.L84
.L91:
	xor	eax, eax
.L80:
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L94:
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	je	.L80
.L84:
	cmp	DWORD PTR 8[rax], r8d
	jne	.L94
	mov	eax, DWORD PTR 12[rax]
.L96:
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L81:
	mov	r10, QWORD PTR 8[rcx]
	movsx	rax, edx
	xor	edx, edx
	div	r10
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rdx
	mov	r11, QWORD PTR [rax+rdx*8]
	test	r11, r11
	je	.L91
	mov	rax, QWORD PTR [r11]
	mov	ecx, DWORD PTR 8[rax]
	cmp	r8d, ecx
	je	.L85
.L95:
	mov	r9, QWORD PTR [rax]
	test	r9, r9
	je	.L91
	mov	ecx, DWORD PTR 8[r9]
	xor	edx, edx
	mov	r11, rax
	movsx	rax, ecx
	div	r10
	cmp	rbx, rdx
	jne	.L91
	cmp	r8d, ecx
	mov	rax, r9
	jne	.L95
.L85:
	mov	rax, QWORD PTR [r11]
	test	rax, rax
	je	.L91
	mov	eax, DWORD PTR 12[rax]
	jmp	.L96
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3292:
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
