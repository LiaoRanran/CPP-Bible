	.file	"_atom_rule_five_noexcept.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "noexcept move: relocation copies=\0"
.LC1:
	.ascii " moves=\0"
.LC2:
	.ascii "\12\0"
	.align 8
.LC3:
	.ascii "throwing move: relocation copies=\0"
	.section	.text.unlikely,"x"
.LCOLDB4:
	.section	.text.startup,"x"
.LHOTB4:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4474:
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
	call	__main
	mov	ecx, 4
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	ecx, 64
	mov	edi, DWORD PTR g_copy[rip]
	mov	r12d, DWORD PTR g_move[rip]
	mov	rsi, rax
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	rbx, rax
	mov	edx, 4
.L2:
	mov	eax, DWORD PTR g_move[rip]
	add	eax, 1
	mov	DWORD PTR g_move[rip], eax
	sub	rdx, 1
	jne	.L2
	mov	rcx, rsi
	mov	edx, 4
	call	_ZdlPvy
	mov	ebp, DWORD PTR g_copy[rip]
	mov	ecx, 4
	sub	ebp, edi
	mov	edi, DWORD PTR g_move[rip]
	sub	edi, r12d
.LEHB2:
	call	_Znwy
.LEHE2:
	mov	ecx, 64
	mov	r14d, DWORD PTR g_copy[rip]
	mov	r12, rax
	mov	r13d, DWORD PTR g_move[rip]
.LEHB3:
	call	_Znwy
.LEHE3:
	mov	rsi, rax
	mov	edx, 4
.L5:
	mov	eax, DWORD PTR g_copy[rip]
	add	eax, 1
	mov	DWORD PTR g_copy[rip], eax
	sub	rdx, 1
	jne	.L5
	mov	rcx, r12
	mov	edx, 4
	call	_ZdlPvy
	mov	r15d, DWORD PTR g_copy[rip]
	mov	r12d, DWORD PTR g_move[rip]
	lea	rdx, .LC0[rip]
	sub	r12d, r13d
	mov	r13, QWORD PTR .refptr._ZSt4cout[rip]
	sub	r15d, r14d
	mov	rcx, r13
.LEHB4:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, ebp
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, edi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC3[rip]
	mov	rcx, r13
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, r15d
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, r12d
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE4:
	mov	rcx, rsi
	mov	edx, 64
	call	_ZdlPvy
	mov	edx, 64
	mov	rcx, rbx
	call	_ZdlPvy
	xor	eax, eax
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
.L15:
	mov	rdi, rax
	jmp	.L3
.L14:
	mov	rdi, rax
	jmp	.L9
.L17:
	mov	rdi, rax
	jmp	.L6
.L16:
	mov	rdi, rax
	jmp	.L10
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4474:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4474-.LLSDACSB4474
.LLSDACSB4474:
	.uleb128 .LEHB0-.LFB4474
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB4474
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L15-.LFB4474
	.uleb128 0
	.uleb128 .LEHB2-.LFB4474
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L16-.LFB4474
	.uleb128 0
	.uleb128 .LEHB3-.LFB4474
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L17-.LFB4474
	.uleb128 0
	.uleb128 .LEHB4-.LFB4474
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L14-.LFB4474
	.uleb128 0
.LLSDACSE4474:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 40
	.seh_savereg	rsi, 48
	.seh_savereg	rdi, 56
	.seh_savereg	rbp, 64
	.seh_savereg	r12, 72
	.seh_savereg	r13, 80
	.seh_savereg	r14, 88
	.seh_savereg	r15, 96
	.seh_endprologue
main.cold:
.L3:
	lea	rbp, 4[rsi]
	mov	rbx, rsi
.L4:
	mov	rdx, rbp
	mov	rcx, rbx
	sub	rdx, rbx
	call	_ZdlPvy
	mov	rcx, rdi
.LEHB5:
	call	_Unwind_Resume
.LEHE5:
.L9:
	lea	rax, 64[rsi]
.L7:
	sub	rax, rsi
	mov	rcx, rsi
	lea	rbp, 64[rbx]
	mov	rdx, rax
	call	_ZdlPvy
	jmp	.L4
.L6:
	lea	rax, 4[r12]
	mov	rsi, r12
	jmp	.L7
.L10:
	lea	rbp, 64[rbx]
	jmp	.L4
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4474:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4474-.LLSDACSBC4474
.LLSDACSBC4474:
	.uleb128 .LEHB5-.LCOLDB4
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSEC4474:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE4:
	.section	.text.startup,"x"
.LHOTE4:
	.globl	g_move
	.bss
	.align 4
g_move:
	.space 4
	.globl	g_copy
	.align 4
g_copy:
	.space 4
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
