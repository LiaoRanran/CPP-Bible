	.file	"_ch146_error.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10compute_eciRi
	.def	_Z10compute_eciRi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10compute_eciRi
_Z10compute_eciRi:
.LFB0:
	.seh_endprologue
	test	ecx, ecx
	je	.L3
	add	ecx, ecx
	xor	eax, eax
	mov	DWORD PTR [rdx], ecx
	ret
	.p2align 4,,10
	.p2align 3
.L3:
	mov	eax, -1
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.globl	_Z10compute_exi
	.def	_Z10compute_exi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10compute_exi
_Z10compute_exi:
.LFB1:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	test	ecx, ecx
	je	.L7
	lea	eax, [rcx+rcx]
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z10compute_exi.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z10compute_exi.cold
	.seh_stackalloc	40
	.seh_endprologue
_Z10compute_exi.cold:
.L7:
	mov	ecx, 4
	call	__cxa_allocate_exception
	mov	rdx, QWORD PTR .refptr._ZTIi[rip]
	xor	r8d, r8d
	mov	DWORD PTR [rax], 1
	mov	rcx, rax
	call	__cxa_throw
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.text
.LHOTE0:
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZTIi, "dr"
	.p2align	3, 0
	.globl	.refptr._ZTIi
	.linkonce	discard
.refptr._ZTIi:
	.quad	_ZTIi
