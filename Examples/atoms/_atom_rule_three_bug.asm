	.file	"_atom_rule_three_bug.cpp"
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
	.ascii "buggy  : allocs=\0"
.LC1:
	.ascii " same_ptr=\0"
.LC2:
	.ascii " dtor_runs=\0"
.LC3:
	.ascii " (one buffer, two dtors)\12\0"
.LC4:
	.ascii "correct: allocs=\0"
.LC5:
	.ascii " (two buffers, two dtors)\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4093:
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
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	call	__main
	mov	ebx, DWORD PTR g_allocs[rip]
	mov	ecx, 4
	mov	edi, DWORD PTR g_dtors[rip]
	mov	eax, DWORD PTR g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	esi, DWORD PTR g_allocs[rip]
	mov	ecx, 4
	mov	DWORD PTR [rax], 42
	mov	eax, DWORD PTR g_dtors[rip]
	mov	r13d, esi
	add	eax, 1
	sub	r13d, ebx
	mov	DWORD PTR g_dtors[rip], eax
	mov	eax, DWORD PTR g_dtors[rip]
	add	eax, 1
	mov	DWORD PTR g_dtors[rip], eax
	mov	ebx, DWORD PTR g_dtors[rip]
	mov	eax, DWORD PTR g_allocs[rip]
	mov	r12d, ebx
	add	eax, 1
	sub	r12d, edi
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	ecx, 4
	mov	rdi, rax
	mov	DWORD PTR [rax], 42
	mov	eax, DWORD PTR g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	ebp, DWORD PTR g_allocs[rip]
	lea	rdx, .LC0[rip]
	mov	r14, rax
	mov	eax, DWORD PTR [rdi]
	sub	ebp, esi
	mov	DWORD PTR [r14], eax
	mov	eax, DWORD PTR g_dtors[rip]
	mov	eax, DWORD PTR g_dtors[rip]
	add	eax, 1
	mov	DWORD PTR g_dtors[rip], eax
	mov	eax, DWORD PTR g_dtors[rip]
	add	eax, 1
	mov	DWORD PTR g_dtors[rip], eax
	mov	esi, DWORD PTR g_dtors[rip]
	sub	esi, ebx
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, r13d
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 1
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, r12d
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC3[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC4[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, ebp
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	edx, edx
	cmp	r14, rdi
	sete	dl
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, esi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC5[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	eax, eax
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
	.seh_endproc
	.globl	g_dtors
	.bss
	.align 4
g_dtors:
	.space 4
	.globl	g_allocs
	.align 4
g_allocs:
	.space 4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
