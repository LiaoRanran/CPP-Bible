	.file	"ch85_uset_test.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt10_HashtableIiiSaIiENSt8__detail9_IdentityESt8equal_toIiESt4hashIiENS1_18_Mod_range_hashingENS1_20_Default_ranged_hashENS1_20_Prime_rehash_policyENS1_17_Hashtable_traitsILb0ELb1ELb1EEEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10_HashtableIiiSaIiENSt8__detail9_IdentityESt8equal_toIiESt4hashIiENS1_18_Mod_range_hashingENS1_20_Default_ranged_hashENS1_20_Prime_rehash_policyENS1_17_Hashtable_traitsILb0ELb1ELb1EEEED1Ev
	.def	_ZNSt10_HashtableIiiSaIiENSt8__detail9_IdentityESt8equal_toIiESt4hashIiENS1_18_Mod_range_hashingENS1_20_Default_ranged_hashENS1_20_Prime_rehash_policyENS1_17_Hashtable_traitsILb0ELb1ELb1EEEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10_HashtableIiiSaIiENSt8__detail9_IdentityESt8equal_toIiESt4hashIiENS1_18_Mod_range_hashingENS1_20_Default_ranged_hashENS1_20_Prime_rehash_policyENS1_17_Hashtable_traitsILb0ELb1ELb1EEEED1Ev
_ZNSt10_HashtableIiiSaIiENSt8__detail9_IdentityESt8equal_toIiESt4hashIiENS1_18_Mod_range_hashingENS1_20_Default_ranged_hashENS1_20_Prime_rehash_policyENS1_17_Hashtable_traitsILb0ELb1ELb1EEEED1Ev:
.LFB1842:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rbx, QWORD PTR 16[rcx]
	mov	rsi, rcx
	test	rbx, rbx
	je	.L2
	.p2align 4
	.p2align 3
.L3:
	mov	rcx, rbx
	mov	rbx, QWORD PTR [rbx]
	mov	edx, 16
	call	_ZdlPvy
	test	rbx, rbx
	jne	.L3
.L2:
	mov	rcx, QWORD PTR [rsi]
	lea	rax, 48[rsi]
	cmp	rcx, rax
	je	.L1
	mov	rdx, QWORD PTR 8[rsi]
	sal	rdx, 3
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L1:
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB1:
	.section	.text.startup,"x"
.LHOTB1:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1791:
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
	sub	rsp, 168
	.seh_stackalloc	168
	.seh_endprologue
	xor	ebx, ebx
	xor	r13d, r13d
	lea	rsi, 144[rsp]
	lea	rbp, 128[rsp]
	call	__main
	mov	QWORD PTR 96[rsp], rsi
	mov	QWORD PTR 104[rsp], 1
	mov	QWORD PTR 112[rsp], 0
	mov	QWORD PTR 120[rsp], 0
	mov	DWORD PTR 128[rsp], 0x3f800000
	mov	QWORD PTR 136[rsp], 0
	mov	QWORD PTR 144[rsp], 0
	.p2align 4
	.p2align 3
.L35:
	test	r13, r13
	je	.L11
	mov	r10, QWORD PTR 104[rsp]
	mov	rax, rbx
	xor	edx, edx
	div	r10
	mov	rax, QWORD PTR 96[rsp]
	mov	rax, QWORD PTR [rax+rdx*8]
	mov	r9, rdx
	mov	r12, rdx
	test	rax, rax
	je	.L12
	mov	rcx, QWORD PTR [rax]
	mov	r8d, DWORD PTR 8[rcx]
.L17:
	cmp	r8d, ebx
	je	.L15
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L12
	movsxd	rax, DWORD PTR 8[rcx]
	xor	edx, edx
	mov	r8, rax
	div	r10
	cmp	rdx, r9
	je	.L17
.L12:
	mov	ecx, 16
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	QWORD PTR [rax], 0
	mov	r9, r13
	mov	rdx, rbp
	mov	r14, rax
	mov	DWORD PTR 8[rax], ebx
	mov	r8, QWORD PTR 104[rsp]
	lea	rcx, 64[rsp]
	mov	QWORD PTR 32[rsp], 1
	mov	r15, QWORD PTR 136[rsp]
.LEHB1:
	call	_ZNKSt8__detail20_Prime_rehash_policy14_M_need_rehashEyyy
	mov	r13, QWORD PTR 72[rsp]
	cmp	BYTE PTR 64[rsp], 0
	je	.L18
	cmp	r13, 1
	je	.L76
	mov	rax, r13
	shr	rax, 60
	jne	.L77
	lea	r8, 0[0+r13*8]
	mov	rcx, r8
	mov	QWORD PTR 56[rsp], r8
	call	_Znwy
	mov	r8, QWORD PTR 56[rsp]
	xor	edx, edx
	mov	rcx, rax
	mov	r12, rax
	call	memset
.L20:
	xor	eax, eax
	mov	r8, QWORD PTR 112[rsp]
	xor	r10d, r10d
	lea	r9, 112[rsp]
	mov	QWORD PTR 112[rsp], rax
.L75:
	test	r8, r8
	je	.L78
.L23:
	mov	rcx, r8
	xor	edx, edx
	mov	r8, QWORD PTR [r8]
	movsxd	rax, DWORD PTR 8[rcx]
	div	r13
	lea	rax, [r12+rdx*8]
	mov	r11, QWORD PTR [rax]
	test	r11, r11
	je	.L79
	mov	rdx, QWORD PTR [r11]
	mov	QWORD PTR [rcx], rdx
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR [rax], rcx
	test	r8, r8
	jne	.L23
.L78:
	mov	rcx, QWORD PTR 96[rsp]
	cmp	rcx, rsi
	je	.L24
	mov	rax, QWORD PTR 104[rsp]
	lea	rdx, 0[0+rax*8]
	call	_ZdlPvy
.L24:
	mov	rax, rbx
	xor	edx, edx
	mov	QWORD PTR 104[rsp], r13
	div	r13
	mov	QWORD PTR 96[rsp], r12
	mov	r12, rdx
.L18:
	mov	r8, QWORD PTR 96[rsp]
	lea	rcx, [r8+r12*8]
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L30
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR [r14], rax
	mov	rax, QWORD PTR [rcx]
	mov	QWORD PTR [rax], r14
.L31:
	mov	rax, QWORD PTR 120[rsp]
	lea	r13, 1[rax]
	mov	QWORD PTR 120[rsp], r13
.L15:
	add	rbx, 1
	cmp	rbx, 100
	jne	.L35
	test	r13, r13
	je	.L80
	mov	r10, QWORD PTR 104[rsp]
	mov	eax, 42
	xor	edx, edx
	div	r10
	mov	rax, QWORD PTR 96[rsp]
	mov	rcx, QWORD PTR [rax+rdx*8]
	mov	r11, rdx
	test	rcx, rcx
	je	.L48
	mov	rax, QWORD PTR [rcx]
	mov	r9d, DWORD PTR 8[rax]
	cmp	r9d, 42
	je	.L40
.L81:
	mov	r8, QWORD PTR [rax]
	test	r8, r8
	je	.L48
	mov	r9d, DWORD PTR 8[r8]
	mov	rcx, rax
	xor	edx, edx
	movsxd	rax, r9d
	div	r10
	cmp	r11, rdx
	jne	.L48
	mov	rax, r8
	cmp	r9d, 42
	jne	.L81
.L40:
	cmp	QWORD PTR [rcx], 0
	sete	al
.L39:
	xor	eax, 1
	lea	rcx, 96[rsp]
	mov	BYTE PTR 95[rsp], al
	movzx	eax, BYTE PTR 95[rsp]
	call	_ZNSt10_HashtableIiiSaIiENSt8__detail9_IdentityESt8equal_toIiESt4hashIiENS1_18_Mod_range_hashingENS1_20_Default_ranged_hashENS1_20_Prime_rehash_policyENS1_17_Hashtable_traitsILb0ELb1ELb1EEEED1Ev
	xor	eax, eax
	add	rsp, 168
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	mov	rax, QWORD PTR 112[rsp]
	test	rax, rax
	je	.L14
	.p2align 4
	.p2align 4
	.p2align 3
.L16:
	cmp	DWORD PTR 8[rax], ebx
	je	.L15
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	jne	.L16
.L14:
	mov	rax, rbx
	xor	edx, edx
	div	QWORD PTR 104[rsp]
	mov	r12, rdx
	jmp	.L12
	.p2align 4,,10
	.p2align 3
.L79:
	mov	r11, QWORD PTR 112[rsp]
	mov	QWORD PTR [rcx], r11
	mov	QWORD PTR 112[rsp], rcx
	mov	QWORD PTR [rax], r9
	cmp	QWORD PTR [rcx], 0
	je	.L27
	mov	QWORD PTR [r12+r10*8], rcx
.L27:
	mov	r10, rdx
	jmp	.L75
.L80:
	mov	rax, QWORD PTR 112[rsp]
	test	rax, rax
	je	.L48
	lea	rcx, 112[rsp]
	jmp	.L41
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L82:
	mov	rdx, QWORD PTR [rax]
	mov	rcx, rax
	test	rdx, rdx
	je	.L48
	mov	rax, rdx
.L41:
	cmp	DWORD PTR 8[rax], 42
	jne	.L82
	jmp	.L40
.L48:
	mov	eax, 1
	jmp	.L39
.L30:
	mov	rax, QWORD PTR 112[rsp]
	mov	QWORD PTR 112[rsp], r14
	mov	QWORD PTR [r14], rax
	test	rax, rax
	je	.L32
	movsxd	rax, DWORD PTR 8[rax]
	xor	edx, edx
	div	QWORD PTR 104[rsp]
	mov	QWORD PTR [r8+rdx*8], r14
.L32:
	lea	rax, 112[rsp]
	mov	QWORD PTR [rcx], rax
	jmp	.L31
.L76:
	xor	edx, edx
	mov	r12, rsi
	mov	QWORD PTR 144[rsp], rdx
	jmp	.L20
.L77:
	shr	r13, 61
	je	.L22
	call	_ZSt28__throw_bad_array_new_lengthv
.L22:
	call	_ZSt17__throw_bad_allocv
	nop
.LEHE1:
.L49:
	jmp	.L33
.L50:
	mov	rbx, rax
	jmp	.L34
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1791:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1791-.LLSDACSB1791
.LLSDACSB1791:
	.uleb128 .LEHB0-.LFB1791
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L50-.LFB1791
	.uleb128 0
	.uleb128 .LEHB1-.LFB1791
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L49-.LFB1791
	.uleb128 0
.LLSDACSE1791:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	232
	.seh_savereg	rbx, 168
	.seh_savereg	rsi, 176
	.seh_savereg	rdi, 184
	.seh_savereg	rbp, 192
	.seh_savereg	r12, 200
	.seh_savereg	r13, 208
	.seh_savereg	r14, 216
	.seh_savereg	r15, 224
	.seh_endprologue
main.cold:
.L33:
	mov	edx, 16
	mov	rcx, r14
	mov	QWORD PTR 136[rsp], r15
	mov	rbx, rax
	call	_ZdlPvy
.L34:
	lea	rcx, 96[rsp]
	call	_ZNSt10_HashtableIiiSaIiENSt8__detail9_IdentityESt8equal_toIiESt4hashIiENS1_18_Mod_range_hashingENS1_20_Default_ranged_hashENS1_20_Prime_rehash_policyENS1_17_Hashtable_traitsILb0ELb1ELb1EEEED1Ev
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC1791:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC1791-.LLSDACSBC1791
.LLSDACSBC1791:
	.uleb128 .LEHB2-.LCOLDB1
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC1791:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.section	.text.startup,"x"
.LHOTE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt8__detail20_Prime_rehash_policy14_M_need_rehashEyyy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZSt28__throw_bad_array_new_lengthv;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
