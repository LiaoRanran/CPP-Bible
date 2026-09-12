	.file	"_atom_unique_noatomic.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "sizeof unique_ptr=%d\12\0"
.LC1:
	.ascii "copyable=%d\12\0"
.LC2:
	.ascii "movable=%d\12\0"
	.align 8
.LC3:
	.ascii "value=%d dtor during lifetime=%d\12\0"
.LC4:
	.ascii "moves=%d dtor after scope=%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB5:
	.section	.text.startup,"x"
.LHOTB5:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3623:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	edx, 8
	lea	rcx, .LC0[rip]
.LEHB0:
	call	__mingw_printf
	xor	edx, edx
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	mov	edx, 1
	lea	rcx, .LC2[rip]
	call	__mingw_printf
	mov	ecx, 4
	call	_Znwy
.LEHE0:
	mov	edx, 7
	lea	rcx, .LC3[rip]
	mov	DWORD PTR [rax], 7
	mov	rbx, rax
	mov	eax, DWORD PTR _ZL7g_moves[rip]
	add	eax, 1
	mov	DWORD PTR _ZL7g_moves[rip], eax
	mov	eax, DWORD PTR _ZL7g_moves[rip]
	add	eax, 1
	mov	DWORD PTR _ZL7g_moves[rip], eax
	mov	r8d, DWORD PTR _ZL6g_dtor[rip]
.LEHB1:
	call	__mingw_printf
.LEHE1:
	mov	eax, DWORD PTR _ZL6g_dtor[rip]
	mov	rcx, rbx
	mov	edx, 4
	add	eax, 1
	mov	DWORD PTR _ZL6g_dtor[rip], eax
	call	_ZdlPvy
	mov	r8d, DWORD PTR _ZL6g_dtor[rip]
	mov	edx, DWORD PTR _ZL7g_moves[rip]
	lea	rcx, .LC4[rip]
.LEHB2:
	call	__mingw_printf
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
.LLSDA3623:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3623-.LLSDACSB3623
.LLSDACSB3623:
	.uleb128 .LEHB0-.LFB3623
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB3623
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L3-.LFB3623
	.uleb128 0
	.uleb128 .LEHB2-.LFB3623
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE3623:
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
	mov	eax, DWORD PTR _ZL6g_dtor[rip]
	mov	rcx, rbx
	mov	edx, 4
	add	eax, 1
	mov	DWORD PTR _ZL6g_dtor[rip], eax
	call	_ZdlPvy
	mov	rcx, rsi
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC3623:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC3623-.LLSDACSBC3623
.LLSDACSBC3623:
	.uleb128 .LEHB3-.LCOLDB5
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSEC3623:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE5:
	.section	.text.startup,"x"
.LHOTE5:
.lcomm _ZL7g_moves,4,4
.lcomm _ZL6g_dtor,4,4
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
