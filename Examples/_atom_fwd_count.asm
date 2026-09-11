	.file	"_atom_fwd_count.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "forward rvalue: copies=\0"
.LC1:
	.ascii " moves=\0"
.LC2:
	.ascii "\12\0"
.LC3:
	.ascii "forward lvalue: copies=\0"
.LC4:
	.ascii "no-forward rvalue: copies=\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4097:
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
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	lea	ebx, 3[rcx]
	call	__main
	lea	rdx, .LC0[rip]
	mov	DWORD PTR g_copies[rip], 0
	mov	DWORD PTR g_moves[rip], 0
	mov	eax, DWORD PTR g_moves[rip]
	add	eax, 1
	mov	DWORD PTR g_moves[rip], eax
	mov	r14d, DWORD PTR g_copies[rip]
	mov	r13d, DWORD PTR g_moves[rip]
	mov	DWORD PTR g_copies[rip], 0
	mov	DWORD PTR g_moves[rip], 0
	mov	eax, DWORD PTR g_copies[rip]
	add	eax, 1
	mov	DWORD PTR g_copies[rip], eax
	mov	r12d, DWORD PTR g_copies[rip]
	mov	ebp, DWORD PTR g_moves[rip]
	mov	DWORD PTR g_copies[rip], 0
	mov	DWORD PTR g_moves[rip], 0
	mov	eax, DWORD PTR g_copies[rip]
	add	eax, 1
	mov	DWORD PTR g_copies[rip], eax
	mov	edi, DWORD PTR g_copies[rip]
	mov	esi, DWORD PTR g_moves[rip]
	mov	DWORD PTR 44[rsp], ebx
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	eax, DWORD PTR 44[rsp]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, r14d
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, r13d
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC3[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, r12d
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, ebp
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC4[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, edi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, esi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
	.seh_endproc
	.globl	g_moves
	.bss
	.align 4
g_moves:
	.space 4
	.globl	g_copies
	.align 4
g_copies:
	.space 4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
