	.file	"_atom_perf_move.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Znay
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znay
_Znay:
.LFB4089:
	.seh_endprologue
	mov	eax, DWORD PTR g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdaPv
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdaPv
_ZdaPv:
.LFB4090:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "Value32 sizeof=\0"
.LC1:
	.ascii " move_eq_copy_bytes\12\0"
.LC2:
	.ascii "heap copy_allocs=\0"
.LC3:
	.ascii " move_allocs=\0"
.LC4:
	.ascii "\12\0"
.LC5:
	.ascii "value move source intact=\0"
	.section	.text.unlikely,"x"
.LCOLDB6:
	.section	.text.startup,"x"
.LHOTB6:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4103:
	push	r14
	.seh_pushreg	r14
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
	movsxd	rbx, ecx
	call	__main
	add	rbx, rbx
	mov	ecx, 32
	mov	QWORD PTR 40[rsp], rbx
	mov	rax, QWORD PTR 40[rsp]
	mov	eax, DWORD PTR g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	edi, DWORD PTR g_allocs[rip]
	mov	ecx, 32
	mov	rsi, rax
	mov	eax, DWORD PTR g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	rbx, rax
	xor	eax, eax
.L5:
	mov	rdx, QWORD PTR [rsi+rax]
	mov	QWORD PTR [rbx+rax], rdx
	add	rax, 8
	cmp	rax, 32
	jne	.L5
	mov	ebp, DWORD PTR g_allocs[rip]
	mov	eax, DWORD PTR g_allocs[rip]
	lea	rdx, .LC0[rip]
	mov	r14, QWORD PTR .refptr._ZSt4cout[rip]
	sub	ebp, edi
	mov	edi, DWORD PTR g_allocs[rip]
	mov	rcx, r14
	sub	edi, eax
	xor	eax, eax
	cmp	rbx, rsi
	setne	al
	mov	DWORD PTR 36[rsp], eax
	mov	eax, DWORD PTR 36[rsp]
.LEHB0:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 32
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC2[rip]
	mov	rcx, r14
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, ebp
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC3[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, edi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC5[rip]
	mov	rcx, r14
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 1
	mov	rcx, rax
	call	_ZNSo9_M_insertIbEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE0:
	mov	rcx, rsi
	call	free
	mov	rcx, rbx
	call	free
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r14
	ret
.L7:
	mov	rdi, rax
	jmp	.L6
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4103:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4103-.LLSDACSB4103
.LLSDACSB4103:
	.uleb128 .LEHB0-.LFB4103
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L7-.LFB4103
	.uleb128 0
.LLSDACSE4103:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_savereg	rbp, 72
	.seh_savereg	r14, 80
	.seh_endprologue
main.cold:
.L6:
	mov	rcx, rsi
	call	free
	mov	rcx, rbx
	call	free
	mov	rcx, rdi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4103:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4103-.LLSDACSBC4103
.LLSDACSBC4103:
	.uleb128 .LEHB1-.LCOLDB6
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSEC4103:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE6:
	.section	.text.startup,"x"
.LHOTE6:
	.globl	g_allocs
	.bss
	.align 4
g_allocs:
	.space 4
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIbEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
