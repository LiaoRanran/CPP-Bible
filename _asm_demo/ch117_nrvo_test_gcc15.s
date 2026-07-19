	.file	"ch117_nrvo_test.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12make_prvaluev
	.def	_Z12make_prvaluev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12make_prvaluev
_Z12make_prvaluev:
.LFB33:
	.seh_endprologue
	mov	rax, rcx
	mov	DWORD PTR [rcx], 42
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9make_nrvov
	.def	_Z9make_nrvov;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9make_nrvov
_Z9make_nrvov:
.LFB34:
	.seh_endprologue
	mov	rax, rcx
	mov	DWORD PTR [rcx], 7
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "move\0"
	.text
	.p2align 4
	.globl	_Z14make_nrvo_failb
	.def	_Z14make_nrvo_failb;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14make_nrvo_failb
_Z14make_nrvo_failb:
.LFB35:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	test	dl, dl
	je	.L5
	mov	DWORD PTR [rcx], 1
	lea	rcx, .LC0[rip]
	call	puts
	mov	rax, rbx
	add	rsp, 32
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	mov	DWORD PTR [rcx], 2
	lea	rcx, .LC0[rip]
	call	puts
	mov	rax, rbx
	add	rsp, 32
	pop	rbx
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA35:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE35-.LLSDACSB35
.LLSDACSB35:
.LLSDACSE35:
	.text
	.seh_endproc
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	puts;	.scl	2;	.type	32;	.endef
