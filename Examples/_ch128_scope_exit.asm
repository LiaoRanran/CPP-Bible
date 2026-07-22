	.file	"_ch128_scope_exit.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "w\0"
.LC1:
	.ascii "/tmp/x.log\0"
.LC2:
	.ascii "hi\0"
	.section	.text.unlikely,"x"
.LCOLDB3:
	.section	.text.startup,"x"
.LHOTB3:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB28:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	lea	rdx, .LC0[rip]
	lea	rcx, .LC1[rip]
.LEHB0:
	call	fopen
.LEHE0:
	mov	rbx, rax
	test	rax, rax
	je	.L4
	mov	r9, rax
	mov	r8d, 2
	mov	edx, 1
	lea	rcx, .LC2[rip]
.LEHB1:
	call	fwrite
.LEHE1:
	mov	rcx, rbx
	call	fclose
	xor	eax, eax
.L1:
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
.L4:
	mov	eax, 1
	jmp	.L1
.L5:
	mov	rsi, rax
	jmp	.L3
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA28:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE28-.LLSDACSB28
.LLSDACSB28:
	.uleb128 .LEHB0-.LFB28
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB28
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L5-.LFB28
	.uleb128 0
.LLSDACSE28:
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
.L3:
	mov	rcx, rbx
	call	fclose
	mov	rcx, rsi
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC28:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC28-.LLSDACSBC28
.LLSDACSBC28:
	.uleb128 .LEHB2-.LCOLDB3
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC28:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.section	.text.startup,"x"
.LHOTE3:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	fopen;	.scl	2;	.type	32;	.endef
	.def	fwrite;	.scl	2;	.type	32;	.endef
	.def	fclose;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
