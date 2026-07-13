	.file	"_ch146_perf.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.unlikely,"x"
	.def	_Z9add_throwii.part.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z9add_throwii.part.0
_Z9add_throwii.part.0:
.LFB52:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 4
	call	__cxa_allocate_exception
	mov	rdx, QWORD PTR .refptr._ZTIi[rip]
	xor	r8d, r8d
	mov	rcx, rax
	xor	eax, eax
	mov	DWORD PTR [rcx], eax
	call	__cxa_throw
	nop
	.seh_endproc
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB11:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rsi, 88[rsp]
	mov	rbx, rcx
	mov	QWORD PTR 88[rsp], rdx
	mov	ecx, 1
	mov	QWORD PTR 96[rsp], r8
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 40[rsp], rsi
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	mov	r8, rsi
	mov	rdx, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z12add_nonthrowii
	.def	_Z12add_nonthrowii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12add_nonthrowii
_Z12add_nonthrowii:
.LFB49:
	.seh_endprologue
	lea	eax, [rcx+rdx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9add_throwii
	.def	_Z9add_throwii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9add_throwii
_Z9add_throwii:
.LFB50:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	test	edx, edx
	mov	eax, ecx
	mov	ecx, edx
	je	.L7
	cdq
	idiv	ecx
	add	rsp, 40
	ret
.L7:
	call	_Z9add_throwii.part.0
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB51:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	DWORD PTR 44[rsp], 0
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L9:
	mov	edx, DWORD PTR 44[rsp]
	add	eax, 1
	add	edx, eax
	cmp	eax, 1000000
	mov	DWORD PTR 44[rsp], edx
	jne	.L9
	mov	edx, DWORD PTR 44[rsp]
	lea	rcx, .LC0[rip]
	call	_Z6printfPKcz
	call	_Z9add_throwii.part.0
	nop
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZTIi, "dr"
	.globl	.refptr._ZTIi
	.linkonce	discard
.refptr._ZTIi:
	.quad	_ZTIi
