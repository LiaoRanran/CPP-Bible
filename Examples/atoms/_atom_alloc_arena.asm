	.file	"_atom_alloc_arena.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB4462:
	.seh_endprologue
	mov	eax, DWORD PTR g_heap_new[rip]
	add	eax, 1
	mov	DWORD PTR g_heap_new[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdlPv
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPv
_ZdlPv:
.LFB4463:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB4464:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_append\0"
.LC1:
	.ascii "arena: calls=\0"
.LC2:
	.ascii " bytes=\0"
.LC3:
	.ascii " heap_new=\0"
.LC4:
	.ascii "\12\0"
.LC5:
	.ascii "std  : heap_new=\0"
.LC6:
	.ascii " (growth reallocations)\12\0"
	.section	.text.unlikely,"x"
.LCOLDB7:
	.section	.text.startup,"x"
.LHOTB7:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4471:
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
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	xor	edi, edi
	lea	rbx, _ZZ4mainE3buf[rip]
	movabs	rsi, 2305843009213693951
	call	__main
	mov	eax, DWORD PTR g_heap_new[rip]
	xor	ecx, ecx
	xor	edx, edx
	xor	r8d, r8d
	mov	DWORD PTR 44[rsp], eax
	xor	eax, eax
	jmp	.L12
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L44:
	mov	DWORD PTR [rcx], r8d
	add	r8d, 1
	add	rcx, 4
	cmp	r8d, 16
	je	.L43
.L12:
	cmp	rcx, rax
	jne	.L44
	mov	r10, rcx
	sub	r10, rdx
	mov	r9, r10
	sar	r9, 2
	cmp	r9, rsi
	je	.L39
	test	r9, r9
	mov	eax, 1
	cmovne	rax, r9
	add	rax, r9
	movabs	r9, 2305843009213693951
	cmp	rax, r9
	cmova	rax, r9
	lea	r11, 0[0+rax*4]
	lea	r12, [r11+rdi]
	cmp	r12, 1024
	ja	.L40
	mov	eax, DWORD PTR g_arena_calls[rip]
	add	rdi, rbx
	add	eax, 1
	mov	DWORD PTR g_arena_calls[rip], eax
	mov	rax, QWORD PTR g_arena_bytes[rip]
	add	rax, r11
	mov	QWORD PTR g_arena_bytes[rip], rax
	mov	DWORD PTR [rdi+r10], r8d
	cmp	rcx, rdx
	je	.L22
	mov	r13, rdx
	add	r10, rdi
	mov	rax, rdi
	.p2align 5
	.p2align 4
	.p2align 3
.L11:
	mov	r9d, DWORD PTR [rdx]
	add	rax, 4
	add	rdx, 4
	mov	DWORD PTR -4[rax], r9d
	cmp	rax, r10
	jne	.L11
	mov	rax, rdi
	sub	rax, r13
	add	rax, rcx
.L10:
	add	r8d, 1
	lea	rcx, 4[rax]
	lea	rax, [rdi+r11]
	mov	rdx, rdi
	mov	rdi, r12
	cmp	r8d, 16
	jne	.L12
	.p2align 4
	.p2align 3
.L43:
	mov	r12d, DWORD PTR g_heap_new[rip]
	xor	esi, esi
	xor	ebx, ebx
	xor	edi, edi
	mov	r14d, DWORD PTR g_heap_new[rip]
	xor	r15d, r15d
	movabs	r13, 2305843009213693951
	jmp	.L18
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L46:
	mov	DWORD PTR [rbx], r15d
	add	r15d, 1
	add	rbx, 4
	cmp	r15d, 16
	je	.L45
.L18:
	cmp	rbx, rsi
	jne	.L46
	sub	rbx, rdi
	mov	rax, rbx
	sar	rax, 2
	cmp	rax, r13
	je	.L41
	test	rax, rax
	mov	esi, 1
	cmovne	rsi, rax
	add	rsi, rax
	movabs	rax, 2305843009213693951
	cmp	rsi, rax
	cmova	rsi, rax
	mov	eax, DWORD PTR g_heap_new[rip]
	sal	rsi, 2
	add	eax, 1
	mov	rcx, rsi
	mov	DWORD PTR g_heap_new[rip], eax
	call	malloc
	mov	DWORD PTR [rax+rbx], r15d
	mov	rbp, rax
	test	rbx, rbx
	je	.L16
	mov	r8, rbx
	mov	rdx, rdi
	mov	rcx, rax
	call	memcpy
.L16:
	lea	rbx, 4[rbp+rbx]
	test	rdi, rdi
	je	.L17
	mov	rcx, rdi
	call	free
.L17:
	add	r15d, 1
	add	rsi, rbp
	mov	rdi, rbp
	cmp	r15d, 16
	jne	.L18
	.p2align 4
	.p2align 3
.L45:
	sub	r12d, DWORD PTR 44[rsp]
	test	rdi, rdi
	je	.L19
	mov	rcx, rdi
	call	free
.L19:
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC1[rip]
	mov	esi, DWORD PTR g_heap_new[rip]
	mov	rcx, rbx
	sub	esi, r14d
.LEHB0:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_arena_calls[rip]
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rdx, QWORD PTR g_arena_bytes[rip]
	mov	rcx, rax
	call	_ZNSo9_M_insertIxEERSoT_
	lea	rdx, .LC3[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, r12d
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC5[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, esi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC6[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE0:
	xor	eax, eax
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L22:
	mov	rax, rdi
	jmp	.L10
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4471:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4471-.LLSDACSB4471
.LLSDACSB4471:
	.uleb128 .LEHB0-.LFB4471
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
.LLSDACSE4471:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	120
	.seh_savereg	rbx, 56
	.seh_savereg	rsi, 64
	.seh_savereg	rdi, 72
	.seh_savereg	rbp, 80
	.seh_savereg	r12, 88
	.seh_savereg	r13, 96
	.seh_savereg	r14, 104
	.seh_savereg	r15, 112
	.seh_endprologue
main.cold:
.L41:
	lea	rcx, .LC0[rip]
.LEHB1:
	call	_ZSt20__throw_length_errorPKc
.LEHE1:
.L40:
	mov	ecx, 8
	call	__cxa_allocate_exception
	lea	r8, _ZNSt9bad_allocD1Ev[rip]
	lea	rdx, _ZTISt9bad_alloc[rip]
	mov	rcx, rax
	mov	rax, QWORD PTR .refptr._ZTVSt9bad_alloc[rip]
	add	rax, 16
	mov	QWORD PTR [rcx], rax
.LEHB2:
	call	__cxa_throw
.L39:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.L23:
	mov	rbx, rax
	test	rdi, rdi
	je	.L21
	mov	rcx, rdi
	call	free
.L21:
	mov	rcx, rbx
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4471:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4471-.LLSDACSBC4471
.LLSDACSBC4471:
	.uleb128 .LEHB1-.LCOLDB7
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L23-.LCOLDB7
	.uleb128 0
	.uleb128 .LEHB2-.LCOLDB7
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC4471:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE7:
	.section	.text.startup,"x"
.LHOTE7:
	.globl	_ZTSSt9exception
	.section	.rdata$_ZTSSt9exception,"dr"
	.linkonce same_size
	.align 8
_ZTSSt9exception:
	.ascii "St9exception\0"
	.globl	_ZTISt9exception
	.section	.rdata$_ZTISt9exception,"dr"
	.linkonce same_size
	.align 8
_ZTISt9exception:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSSt9exception
	.globl	_ZTSSt9bad_alloc
	.section	.rdata$_ZTSSt9bad_alloc,"dr"
	.linkonce same_size
	.align 8
_ZTSSt9bad_alloc:
	.ascii "St9bad_alloc\0"
	.globl	_ZTISt9bad_alloc
	.section	.rdata$_ZTISt9bad_alloc,"dr"
	.linkonce same_size
	.align 8
_ZTISt9bad_alloc:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt9bad_alloc
	.quad	_ZTISt9exception
.lcomm _ZZ4mainE3buf,1024,16
	.globl	g_arena_bytes
	.bss
	.align 8
g_arena_bytes:
	.space 8
	.globl	g_arena_calls
	.align 4
g_arena_calls:
	.space 4
	.globl	g_heap_new
	.align 4
g_heap_new:
	.space 4
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIxEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	_ZNSt9bad_allocD1Ev;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
	.section	.rdata$.refptr._ZNSt9bad_allocD1Ev, "dr"
	.p2align	3, 0
	.globl	.refptr._ZNSt9bad_allocD1Ev
	.linkonce	discard
.refptr._ZNSt9bad_allocD1Ev:
	.quad	_ZNSt9bad_allocD1Ev
	.section	.rdata$.refptr._ZTVSt9bad_alloc, "dr"
	.p2align	3, 0
	.globl	.refptr._ZTVSt9bad_alloc
	.linkonce	discard
.refptr._ZTVSt9bad_alloc:
	.quad	_ZTVSt9bad_alloc
