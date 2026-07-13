	.file	"_ch145_noexcept2.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.unlikely,"x"
	.globl	_Z4sinkv
	.def	_Z4sinkv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4sinkv
_Z4sinkv:
.LFB0:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 4
	call	__cxa_allocate_exception
	mov	rdx, QWORD PTR .refptr._ZTIi[rip]
	xor	r8d, r8d
	mov	rcx, rax
	mov	DWORD PTR [rax], 1
	call	__cxa_throw
	nop
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA0:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE0-.LLSDACSB0
.LLSDACSB0:
.LLSDACSE0:
	.section	.text.unlikely,"x"
	.seh_endproc
	.globl	_Z4boomv
	.def	_Z4boomv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4boomv
_Z4boomv:
.LFB1:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 4
	call	__cxa_allocate_exception
	mov	rdx, QWORD PTR .refptr._ZTIi[rip]
	xor	r8d, r8d
	mov	rcx, rax
	mov	DWORD PTR [rax], 2
	call	__cxa_throw
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	call	_Z4sinkv
	nop
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZTIi, "dr"
	.globl	.refptr._ZTIi
	.linkonce	discard
.refptr._ZTIi:
	.quad	_ZTIi
