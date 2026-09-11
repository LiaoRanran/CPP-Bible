	.file	"_atom_rule_zero.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB5049:
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
.LFB5050:
	.seh_endprologue
	test	rcx, rcx
	je	.L3
	mov	eax, DWORD PTR g_frees[rip]
	add	eax, 1
	mov	DWORD PTR g_frees[rip], eax
	jmp	free
	.p2align 4,,10
	.p2align 3
.L3:
	ret
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB5051:
	.seh_endprologue
	test	rcx, rcx
	je	.L5
	mov	eax, DWORD PTR g_frees[rip]
	add	eax, 1
	mov	DWORD PTR g_frees[rip], eax
	jmp	free
	.p2align 4,,10
	.p2align 3
.L5:
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "rule zero: move_constructible=\0"
.LC1:
	.ascii " copy_constructible=\0"
.LC2:
	.ascii " (type system)\12\0"
.LC3:
	.ascii "move transfer: owner_changed=\0"
.LC4:
	.ascii "\12\0"
.LC5:
	.ascii "allocs=\0"
.LC6:
	.ascii " dtors=\0"
.LC7:
	.ascii " frees=\0"
.LC8:
	.ascii " (exactly once, no leak)\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5068:
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
	call	__main
	mov	r8d, DWORD PTR g_allocs[rip]
	mov	ecx, DWORD PTR g_dtors[rip]
	mov	edx, DWORD PTR g_frees[rip]
	mov	eax, DWORD PTR g_allocs[rip]
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	mov	ebp, DWORD PTR g_allocs[rip]
	mov	eax, DWORD PTR g_dtors[rip]
	sub	ebp, r8d
	add	eax, 1
	mov	DWORD PTR g_dtors[rip], eax
	mov	eax, DWORD PTR g_frees[rip]
	add	eax, 1
	mov	DWORD PTR g_frees[rip], eax
	mov	edi, DWORD PTR g_dtors[rip]
	mov	esi, DWORD PTR g_frees[rip]
	sub	edi, ecx
	mov	rcx, rbx
	sub	esi, edx
	lea	rdx, .LC0[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 1
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	edx, edx
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC3[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 1
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC5[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, ebp
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC6[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, edi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC7[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, esi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC8[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.globl	g_dtors
	.bss
	.align 4
g_dtors:
	.space 4
	.globl	g_frees
	.align 4
g_frees:
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
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
