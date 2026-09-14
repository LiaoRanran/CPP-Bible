	.file	"_atom_sso_threshold.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB4074:
	.seh_endprologue
	mov	eax, DWORD PTR g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdlPv
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPv
_ZdlPv:
.LFB4075:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB4076:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "basic_string::_M_create\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	_Z10allocs_fory
	.def	_Z10allocs_fory;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10allocs_fory
_Z10allocs_fory:
.LFB4082:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	mov	DWORD PTR g_allocs[rip], 0
	lea	rsi, 48[rsp]
	mov	rbx, rcx
	mov	QWORD PTR 32[rsp], rsi
	cmp	rcx, 15
	ja	.L13
	mov	rax, rsi
	cmp	rcx, 1
	ja	.L14
.L9:
	mov	BYTE PTR [rax+rbx], 0
	mov	rcx, QWORD PTR 32[rsp]
	cmp	rcx, rsi
	je	.L10
	call	free
.L10:
	movsxd	rax, DWORD PTR g_allocs[rip]
	add	rsp, 72
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L13:
	movabs	rax, 9223372036854775806
	cmp	rax, rcx
	jb	.L12
	mov	eax, DWORD PTR g_allocs[rip]
	lea	rcx, 1[rcx]
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	QWORD PTR 32[rsp], rax
	mov	rcx, rax
.L8:
	mov	r8, rbx
	mov	edx, 120
	call	memset
	mov	rax, QWORD PTR 32[rsp]
	jmp	.L9
	.p2align 4,,10
	.p2align 3
.L14:
	mov	rcx, rsi
	jmp	.L8
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z10allocs_fory.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z10allocs_fory.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 72
	.seh_savereg	rsi, 80
	.seh_endprologue
_Z10allocs_fory.cold:
.L12:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc:
.LFB4090:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rsi, rcx
	mov	rbx, rdx
	cmp	rdx, 15
	ja	.L23
	test	rdx, rdx
	je	.L19
	mov	rcx, QWORD PTR [rcx]
	cmp	rdx, 1
	je	.L24
	movsx	edx, r8b
	mov	r8, rbx
	call	memset
.L19:
	mov	rax, QWORD PTR [rsi]
	mov	QWORD PTR 8[rsi], rbx
	mov	BYTE PTR [rax+rbx], 0
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L23:
	movabs	rax, 9223372036854775806
	cmp	rax, rdx
	jb	.L25
	mov	eax, DWORD PTR g_allocs[rip]
	lea	rcx, 1[rdx]
	mov	DWORD PTR 44[rsp], r8d
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	r8d, DWORD PTR 44[rsp]
	mov	QWORD PTR 16[rsi], rbx
	mov	QWORD PTR [rsi], rax
	mov	rcx, rax
	movsx	edx, r8b
	mov	r8, rbx
	call	memset
	jmp	.L19
	.p2align 4,,10
	.p2align 3
.L24:
	mov	BYTE PTR [rcx], r8b
	jmp	.L19
.L25:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "len=\0"
.LC3:
	.ascii " allocs=\0"
.LC4:
	.ascii "\12\0"
.LC5:
	.ascii "sso: max_zero_alloc_len=\0"
.LC6:
	.ascii " first_heap_len=\0"
.LC7:
	.ascii "std-string: len=15 allocs=\0"
.LC8:
	.ascii " len=16 allocs=\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4083:
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
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	xor	ebx, ebx
	xor	esi, esi
	mov	ebp, 12697601
	call	__main
	mov	r13, QWORD PTR .refptr._ZSt4cout[rip]
	jmp	.L30
	.p2align 4,,10
	.p2align 3
.L29:
	add	rbx, 1
	cmp	rbx, 25
	je	.L41
.L30:
	mov	rcx, rbx
	call	_Z10allocs_fory
	mov	rdi, rax
	test	rax, rax
	je	.L27
	test	rsi, rsi
	cmove	rsi, rbx
.L27:
	bt	rbp, rbx
	jnc	.L29
	mov	r8d, 4
	lea	rdx, .LC2[rip]
	mov	rcx, r13
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	rdx, rbx
	mov	rcx, r13
	add	rbx, 1
	call	_ZNSo9_M_insertIyEERSoT_
	mov	r8d, 8
	lea	rdx, .LC3[rip]
	mov	r12, rax
	mov	rcx, rax
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	rdx, rdi
	mov	rcx, r12
	call	_ZNSo9_M_insertIyEERSoT_
	mov	r8d, 1
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	cmp	rbx, 25
	jne	.L30
.L41:
	lea	rdx, .LC5[rip]
	mov	rcx, r13
	lea	rbx, 48[rsp]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, -1[rsi]
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC6[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rdx, rsi
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rcx, 32[rsp]
	mov	r8d, 120
	mov	edx, 15
	mov	DWORD PTR g_allocs[rip], 0
	mov	QWORD PTR 32[rsp], rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
	mov	rcx, QWORD PTR 32[rsp]
	cmp	rcx, rbx
	je	.L31
	call	free
.L31:
	lea	rcx, 32[rsp]
	mov	edx, 16
	mov	QWORD PTR 32[rsp], rbx
	mov	r8d, 120
	mov	edi, DWORD PTR g_allocs[rip]
	mov	DWORD PTR g_allocs[rip], 0
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
	mov	rcx, QWORD PTR 32[rsp]
	cmp	rcx, rbx
	je	.L32
	call	free
.L32:
	mov	rcx, r13
	lea	rdx, .LC7[rip]
	mov	ebx, DWORD PTR g_allocs[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, edi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC8[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, ebx
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	eax, eax
	add	rsp, 72
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.seh_endproc
	.globl	g_allocs
	.bss
	.align 4
g_allocs:
	.space 4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
