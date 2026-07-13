	.file	"_ch142_stl.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	__tcf_0;	.scl	3;	.type	32;	.endef
	.seh_proc	__tcf_0
__tcf_0:
.LFB2448:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, QWORD PTR g_transforms[rip+16]
	test	rbx, rbx
	je	.L2
	.p2align 4,,10
	.p2align 3
.L3:
	mov	rcx, rbx
	mov	rbx, QWORD PTR [rbx]
	mov	edx, 24
	call	_ZdlPvy
	test	rbx, rbx
	jne	.L3
.L2:
	mov	rax, QWORD PTR g_transforms[rip+8]
	xor	edx, edx
	mov	rcx, QWORD PTR g_transforms[rip]
	lea	r8, 0[0+rax*8]
	call	memset
	mov	rcx, QWORD PTR g_transforms[rip]
	lea	rax, g_transforms[rip+48]
	mov	QWORD PTR g_transforms[rip+24], 0
	mov	rdx, QWORD PTR g_transforms[rip+8]
	mov	QWORD PTR g_transforms[rip+16], 0
	cmp	rcx, rax
	je	.L1
	sal	rdx, 3
	add	rsp, 32
	pop	rbx
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L1:
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section	.text$_ZNSt10_HashtableIjSt4pairIKj9TransformESaIS3_ENSt8__detail10_Select1stESt8equal_toIjESt4hashIjENS5_18_Mod_range_hashingENS5_20_Default_ranged_hashENS5_20_Prime_rehash_policyENS5_17_Hashtable_traitsILb0ELb0ELb1EEEE9_M_rehashEyRKy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10_HashtableIjSt4pairIKj9TransformESaIS3_ENSt8__detail10_Select1stESt8equal_toIjESt4hashIjENS5_18_Mod_range_hashingENS5_20_Default_ranged_hashENS5_20_Prime_rehash_policyENS5_17_Hashtable_traitsILb0ELb0ELb1EEEE9_M_rehashEyRKy
	.def	_ZNSt10_HashtableIjSt4pairIKj9TransformESaIS3_ENSt8__detail10_Select1stESt8equal_toIjESt4hashIjENS5_18_Mod_range_hashingENS5_20_Default_ranged_hashENS5_20_Prime_rehash_policyENS5_17_Hashtable_traitsILb0ELb0ELb1EEEE9_M_rehashEyRKy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10_HashtableIjSt4pairIKj9TransformESaIS3_ENSt8__detail10_Select1stESt8equal_toIjESt4hashIjENS5_18_Mod_range_hashingENS5_20_Default_ranged_hashENS5_20_Prime_rehash_policyENS5_17_Hashtable_traitsILb0ELb0ELb1EEEE9_M_rehashEyRKy
_ZNSt10_HashtableIjSt4pairIKj9TransformESaIS3_ENSt8__detail10_Select1stESt8equal_toIjESt4hashIjENS5_18_Mod_range_hashingENS5_20_Default_ranged_hashENS5_20_Prime_rehash_policyENS5_17_Hashtable_traitsILb0ELb0ELb1EEEE9_M_rehashEyRKy:
.LFB2357:
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
	cmp	rdx, 1
	mov	rsi, rcx
	mov	rbx, rdx
	mov	rdi, r8
	je	.L30
	movabs	rax, 1152921504606846975
	cmp	rax, rdx
	jb	.L31
	lea	rbp, 0[0+rdx*8]
	mov	rcx, rbp
.LEHB0:
	call	_Znwy
	mov	r8, rbp
	xor	edx, edx
	mov	rcx, rax
	lea	rbp, 48[rsi]
	mov	rdi, rax
	call	memset
.L12:
	mov	r8, QWORD PTR 16[rsi]
	mov	QWORD PTR 16[rsi], 0
	test	r8, r8
	je	.L15
	lea	r11, 16[rsi]
	xor	r10d, r10d
	jmp	.L19
	.p2align 4,,10
	.p2align 3
.L16:
	mov	rdx, QWORD PTR [r9]
	test	r8, r8
	mov	QWORD PTR [rcx], rdx
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR [rax], rcx
	je	.L15
.L19:
	mov	rcx, r8
	xor	edx, edx
	mov	r8, QWORD PTR [r8]
	mov	eax, DWORD PTR 8[rcx]
	div	rbx
	lea	rax, [rdi+rdx*8]
	mov	r9, QWORD PTR [rax]
	test	r9, r9
	jne	.L16
	mov	r9, QWORD PTR 16[rsi]
	mov	QWORD PTR [rcx], r9
	mov	QWORD PTR 16[rsi], rcx
	mov	QWORD PTR [rax], r11
	cmp	QWORD PTR [rcx], 0
	je	.L17
	mov	QWORD PTR [rdi+r10*8], rcx
.L17:
	test	r8, r8
	mov	r10, rdx
	jne	.L19
.L15:
	mov	rcx, QWORD PTR [rsi]
	mov	rdx, QWORD PTR 8[rsi]
	cmp	rcx, rbp
	je	.L20
	sal	rdx, 3
	call	_ZdlPvy
.L20:
	mov	QWORD PTR 8[rsi], rbx
	mov	QWORD PTR [rsi], rdi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L30:
	lea	rbp, 48[rcx]
	mov	QWORD PTR 48[rcx], 0
	mov	rdi, rbp
	jmp	.L12
	.p2align 4,,10
	.p2align 3
.L31:
	movabs	rax, 2305843009213693951
	cmp	rax, rdx
	jnb	.L14
	call	_ZSt28__throw_bad_array_new_lengthv
.L14:
	call	_ZSt17__throw_bad_allocv
.LEHE0:
.L23:
	mov	rcx, rax
	call	__cxa_begin_catch
	mov	rax, QWORD PTR [rdi]
	mov	QWORD PTR 40[rsi], rax
.LEHB1:
	call	__cxa_rethrow
.LEHE1:
.L24:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA2357:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT2357-.LLSDATTD2357
.LLSDATTD2357:
	.byte	0x1
	.uleb128 .LLSDACSE2357-.LLSDACSB2357
.LLSDACSB2357:
	.uleb128 .LEHB0-.LFB2357
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L23-.LFB2357
	.uleb128 0x1
	.uleb128 .LEHB1-.LFB2357
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L24-.LFB2357
	.uleb128 0
	.uleb128 .LEHB2-.LFB2357
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE2357:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT2357:
	.section	.text$_ZNSt10_HashtableIjSt4pairIKj9TransformESaIS3_ENSt8__detail10_Select1stESt8equal_toIjESt4hashIjENS5_18_Mod_range_hashingENS5_20_Default_ranged_hashENS5_20_Prime_rehash_policyENS5_17_Hashtable_traitsILb0ELb0ELb1EEEE9_M_rehashEyRKy,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt8__detail9_Map_baseIjSt4pairIKj9TransformESaIS4_ENS_10_Select1stESt8equal_toIjESt4hashIjENS_18_Mod_range_hashingENS_20_Default_ranged_hashENS_20_Prime_rehash_policyENS_17_Hashtable_traitsILb0ELb0ELb1EEELb1EEixEOj,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8__detail9_Map_baseIjSt4pairIKj9TransformESaIS4_ENS_10_Select1stESt8equal_toIjESt4hashIjENS_18_Mod_range_hashingENS_20_Default_ranged_hashENS_20_Prime_rehash_policyENS_17_Hashtable_traitsILb0ELb0ELb1EEELb1EEixEOj
	.def	_ZNSt8__detail9_Map_baseIjSt4pairIKj9TransformESaIS4_ENS_10_Select1stESt8equal_toIjESt4hashIjENS_18_Mod_range_hashingENS_20_Default_ranged_hashENS_20_Prime_rehash_policyENS_17_Hashtable_traitsILb0ELb0ELb1EEELb1EEixEOj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8__detail9_Map_baseIjSt4pairIKj9TransformESaIS4_ENS_10_Select1stESt8equal_toIjESt4hashIjENS_18_Mod_range_hashingENS_20_Default_ranged_hashENS_20_Prime_rehash_policyENS_17_Hashtable_traitsILb0ELb0ELb1EEELb1EEixEOj
_ZNSt8__detail9_Map_baseIjSt4pairIKj9TransformESaIS4_ENS_10_Select1stESt8equal_toIjESt4hashIjENS_18_Mod_range_hashingENS_20_Default_ranged_hashENS_20_Prime_rehash_policyENS_17_Hashtable_traitsILb0ELb0ELb1EEELb1EEixEOj:
.LFB2301:
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
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	mov	esi, DWORD PTR [rdx]
	mov	r10, QWORD PTR 8[rcx]
	mov	r12, rdx
	mov	rax, rsi
	xor	edx, edx
	div	r10
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rcx
	mov	r13, rsi
	lea	rdi, 0[0+rdx*8]
	mov	rbp, rdx
	mov	r11, QWORD PTR [rax+rdx*8]
	test	r11, r11
	je	.L33
	mov	rcx, QWORD PTR [r11]
	mov	r8d, DWORD PTR 8[rcx]
	cmp	r13d, r8d
	je	.L34
.L53:
	mov	r9, QWORD PTR [rcx]
	test	r9, r9
	je	.L33
	mov	eax, DWORD PTR 8[r9]
	xor	edx, edx
	mov	r11, rcx
	mov	r8, rax
	div	r10
	cmp	rbp, rdx
	jne	.L33
	cmp	r13d, r8d
	mov	rcx, r9
	jne	.L53
.L34:
	mov	rax, QWORD PTR [r11]
	lea	r13, 12[rax]
	test	rax, rax
	je	.L33
	mov	rax, r13
	add	rsp, 88
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L33:
	mov	ecx, 24
.LEHB3:
	call	_Znwy
.LEHE3:
	lea	rcx, 48[rsp]
	mov	QWORD PTR [rax], 0
	lea	rdx, 32[rbx]
	mov	rbp, rax
	mov	eax, DWORD PTR [r12]
	mov	QWORD PTR 12[rbp], 0
	lea	r13, 12[rbp]
	mov	DWORD PTR 20[rbp], 0x00000000
	mov	DWORD PTR 8[rbp], eax
	mov	rax, QWORD PTR 40[rbx]
	mov	QWORD PTR 32[rsp], 1
	mov	r9, QWORD PTR 24[rbx]
	mov	r8, QWORD PTR 8[rbx]
	mov	QWORD PTR 72[rsp], rax
.LEHB4:
	call	_ZNKSt8__detail20_Prime_rehash_policy14_M_need_rehashEyyy
	cmp	BYTE PTR 48[rsp], 0
	mov	rdx, QWORD PTR 56[rsp]
	jne	.L54
	mov	rcx, QWORD PTR [rbx]
	add	rdi, rcx
	mov	rax, QWORD PTR [rdi]
	test	rax, rax
	je	.L38
.L55:
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR 0[rbp], rax
	mov	rax, QWORD PTR [rdi]
	mov	QWORD PTR [rax], rbp
.L39:
	add	QWORD PTR 24[rbx], 1
	mov	rax, r13
	add	rsp, 88
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L54:
	lea	r8, 72[rsp]
	mov	rcx, rbx
	call	_ZNSt10_HashtableIjSt4pairIKj9TransformESaIS3_ENSt8__detail10_Select1stESt8equal_toIjESt4hashIjENS5_18_Mod_range_hashingENS5_20_Default_ranged_hashENS5_20_Prime_rehash_policyENS5_17_Hashtable_traitsILb0ELb0ELb1EEEE9_M_rehashEyRKy
.LEHE4:
	mov	rcx, QWORD PTR [rbx]
	xor	edx, edx
	mov	rax, rsi
	div	QWORD PTR 8[rbx]
	lea	rdi, 0[0+rdx*8]
	add	rdi, rcx
	mov	rax, QWORD PTR [rdi]
	test	rax, rax
	jne	.L55
.L38:
	mov	rax, QWORD PTR 16[rbx]
	mov	QWORD PTR 16[rbx], rbp
	test	rax, rax
	mov	QWORD PTR 0[rbp], rax
	je	.L40
	mov	eax, DWORD PTR 8[rax]
	xor	edx, edx
	div	QWORD PTR 8[rbx]
	mov	QWORD PTR [rcx+rdx*8], rbp
.L40:
	lea	rax, 16[rbx]
	mov	QWORD PTR [rdi], rax
	jmp	.L39
.L43:
	mov	rbx, rax
	mov	rcx, rbp
	mov	edx, 24
	call	_ZdlPvy
	mov	rcx, rbx
.LEHB5:
	call	_Unwind_Resume
	nop
.LEHE5:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2301:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2301-.LLSDACSB2301
.LLSDACSB2301:
	.uleb128 .LEHB3-.LFB2301
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB4-.LFB2301
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L43-.LFB2301
	.uleb128 0
	.uleb128 .LEHB5-.LFB2301
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSE2301:
	.section	.text$_ZNSt8__detail9_Map_baseIjSt4pairIKj9TransformESaIS4_ENS_10_Select1stESt8equal_toIjESt4hashIjENS_18_Mod_range_hashingENS_20_Default_ranged_hashENS_20_Prime_rehash_policyENS_17_Hashtable_traitsILb0ELb0ELb1EEELb1EEixEOj,"x"
	.linkonce discard
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2255:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rbx, g_transforms[rip]
	call	__main
	lea	rsi, 44[rsp]
	mov	rcx, rbx
	mov	DWORD PTR 44[rsp], 1
	mov	rdx, rsi
	call	_ZNSt8__detail9_Map_baseIjSt4pairIKj9TransformESaIS4_ENS_10_Select1stESt8equal_toIjESt4hashIjENS_18_Mod_range_hashingENS_20_Default_ranged_hashENS_20_Prime_rehash_policyENS_17_Hashtable_traitsILb0ELb0ELb1EEELb1EEixEOj
	mov	rdx, QWORD PTR .LC1[rip]
	mov	rcx, rbx
	mov	DWORD PTR 44[rsp], 2
	mov	DWORD PTR 8[rax], 0x40400000
	mov	QWORD PTR [rax], rdx
	mov	rdx, rsi
	call	_ZNSt8__detail9_Map_baseIjSt4pairIKj9TransformESaIS4_ENS_10_Select1stESt8equal_toIjESt4hashIjENS_18_Mod_range_hashingENS_20_Default_ranged_hashENS_20_Prime_rehash_policyENS_17_Hashtable_traitsILb0ELb0ELb1EEELb1EEixEOj
	mov	rdx, QWORD PTR .LC3[rip]
	pxor	xmm1, xmm1
	mov	DWORD PTR 8[rax], 0x40c00000
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR g_transforms[rip+16]
	test	rax, rax
	je	.L57
	movss	xmm2, DWORD PTR .LC5[rip]
	.p2align 4,,10
	.p2align 3
.L58:
	movss	xmm0, DWORD PTR 12[rax]
	addss	xmm0, xmm2
	movss	DWORD PTR 12[rax], xmm0
	mov	rax, QWORD PTR [rax]
	addss	xmm1, xmm0
	test	rax, rax
	jne	.L58
.L57:
	cvttss2si	eax, xmm1
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.p2align 4
	.def	_GLOBAL__sub_I_g_transforms;	.scl	3;	.type	32;	.endef
	.seh_proc	_GLOBAL__sub_I_g_transforms
_GLOBAL__sub_I_g_transforms:
.LFB2449:
	.seh_endprologue
	lea	rax, g_transforms[rip+48]
	mov	QWORD PTR g_transforms[rip+8], 1
	lea	rcx, __tcf_0[rip]
	mov	QWORD PTR g_transforms[rip], rax
	mov	QWORD PTR g_transforms[rip+16], 0
	mov	QWORD PTR g_transforms[rip+24], 0
	mov	DWORD PTR g_transforms[rip+32], 0x3f800000
	mov	QWORD PTR g_transforms[rip+40], 0
	mov	QWORD PTR g_transforms[rip+48], 0
	jmp	atexit
	.seh_endproc
	.section	.ctors,"w"
	.align 8
	.quad	_GLOBAL__sub_I_g_transforms
	.globl	g_transforms
	.bss
	.align 32
g_transforms:
	.space 56
	.section .rdata,"dr"
	.align 8
.LC1:
	.long	1065353216
	.long	1073741824
	.align 8
.LC3:
	.long	1082130432
	.long	1084227584
	.align 4
.LC5:
	.long	1036831949
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt28__throw_bad_array_new_lengthv;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_rethrow;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt8__detail20_Prime_rehash_policy14_M_need_rehashEyyy;	.scl	2;	.type	32;	.endef
	.def	atexit;	.scl	2;	.type	32;	.endef
