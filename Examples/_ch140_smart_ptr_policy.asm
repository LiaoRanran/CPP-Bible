	.file	"_ch140_smart_ptr_policy.cpp"
	.intel_syntax noprefix
	.text
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB61:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	ecx, 4
	call	malloc
	mov	ecx, 4
	mov	rbx, rax
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	rcx, rax
	mov	DWORD PTR [rax], 2
	call	_ZdlPv
	mov	rcx, rbx
	call	free
	mov	eax, 2
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
.L4:
	test	rbx, rbx
	mov	rsi, rax
	je	.L3
	mov	rcx, rbx
	call	free
.L3:
	mov	rcx, rsi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA61:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE61-.LLSDACSB61
.LLSDACSB61:
	.uleb128 .LEHB0-.LFB61
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L4-.LFB61
	.uleb128 0
	.uleb128 .LEHB1-.LFB61
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE61:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
