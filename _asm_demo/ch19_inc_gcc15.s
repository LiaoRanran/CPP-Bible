	.file	"ch19_inc_gcc15.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z3incv
	.def	_Z3incv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3incv
_Z3incv:
.LFB0:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, __emutls_v.tls_counter[rip]
	call	__emutls_get_address
	add	DWORD PTR [rax], 1
	add	rsp, 40
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 4
__emutls_t.tls_counter:
	.space 4
	.globl	__emutls_v.tls_counter
	.data
	.align 32
__emutls_v.tls_counter:
	.quad	4
	.quad	4
	.quad	0
	.quad	__emutls_t.tls_counter
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	__emutls_get_address;	.scl	2;	.type	32;	.endef
