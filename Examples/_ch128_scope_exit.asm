	.file	"_ch128_scope_exit.cpp"
	.intel_syntax noprefix
	.text
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "w\0"
.LC1:
	.ascii "/tmp/x.log\0"
.LC2:
	.ascii "hi\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB53:
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
	test	rax, rax
	mov	rbx, rax
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
	mov	rcx, rbx
	call	fclose
	mov	rcx, rsi
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA53:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE53-.LLSDACSB53
.LLSDACSB53:
	.uleb128 .LEHB0-.LFB53
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB53
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L5-.LFB53
	.uleb128 0
	.uleb128 .LEHB2-.LFB53
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE53:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	fopen;	.scl	2;	.type	32;	.endef
	.def	fwrite;	.scl	2;	.type	32;	.endef
	.def	fclose;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
