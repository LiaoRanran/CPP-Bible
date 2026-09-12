	.file	"_atom_unique_move.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "after move a empty=\0"
.LC1:
	.ascii "\12\0"
.LC2:
	.ascii "b->v=\0"
.LC3:
	.ascii "box destroyed count=\0"
	.section	.text.unlikely,"x"
.LCOLDB4:
	.section	.text.startup,"x"
.LHOTB4:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5055:
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
	mov	rsi, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC0[rip]
	mov	DWORD PTR [rax], 7
	mov	rbx, rax
	mov	rcx, rsi
.LEHB1:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 1
	mov	rcx, rax
	call	_ZNSo9_M_insertIbEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC2[rip]
	mov	rcx, rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR [rbx]
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE1:
	mov	eax, DWORD PTR g_destroy[rip]
	mov	rcx, rbx
	mov	edx, 4
	add	eax, 1
	mov	DWORD PTR g_destroy[rip], eax
	call	_ZdlPvy
	mov	rcx, rsi
	lea	rdx, .LC3[rip]
.LEHB2:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_destroy[rip]
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE2:
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
.L3:
	mov	rsi, rax
	jmp	.L2
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5055:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5055-.LLSDACSB5055
.LLSDACSB5055:
	.uleb128 .LEHB0-.LFB5055
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5055
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L3-.LFB5055
	.uleb128 0
	.uleb128 .LEHB2-.LFB5055
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE5055:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	56
	.seh_savereg	rbx, 40
	.seh_savereg	rsi, 48
	.seh_endprologue
main.cold:
.L2:
	mov	eax, DWORD PTR g_destroy[rip]
	mov	rcx, rbx
	mov	edx, 4
	add	eax, 1
	mov	DWORD PTR g_destroy[rip], eax
	call	_ZdlPvy
	mov	rcx, rsi
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5055:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5055-.LLSDACSBC5055
.LLSDACSBC5055:
	.uleb128 .LEHB3-.LCOLDB4
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSEC5055:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE4:
	.section	.text.startup,"x"
.LHOTE4:
	.globl	g_destroy
	.bss
	.align 4
g_destroy:
	.space 4
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIbEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
