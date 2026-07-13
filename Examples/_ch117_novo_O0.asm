	.file	"_ch117_novo.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB11:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	QWORD PTR 40[rbp], rdx
	mov	QWORD PTR 48[rbp], r8
	mov	QWORD PTR 56[rbp], r9
	lea	rax, 40[rbp]
	mov	QWORD PTR -16[rbp], rax
	mov	rbx, QWORD PTR -16[rbp]
	mov	ecx, 1
	mov	rax, QWORD PTR __imp___acrt_iob_func[rip]
	call	rax
	mov	rcx, rax
	mov	rax, QWORD PTR 32[rbp]
	mov	r8, rbx
	mov	rdx, rax
	call	__mingw_vfprintf
	mov	DWORD PTR -4[rbp], eax
	mov	eax, DWORD PTR -4[rbp]
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3BigC1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN3BigC1Ev
	.def	_ZN3BigC1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3BigC1Ev
_ZN3BigC1Ev:
.LFB49:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR [rax], 1
	nop
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "copy ctor!\12\0"
	.section	.text$_ZN3BigC1ERKS_,"x"
	.linkonce discard
	.align 2
	.globl	_ZN3BigC1ERKS_
	.def	_ZN3BigC1ERKS_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3BigC1ERKS_
_ZN3BigC1ERKS_:
.LFB52:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	lea	rax, .LC0[rip]
	mov	rcx, rax
	call	_Z6printfPKcz
	mov	rax, QWORD PTR 24[rbp]
	mov	edx, DWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR [rax], edx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z9make_copyv
	.def	_Z9make_copyv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9make_copyv
_Z9make_copyv:
.LFB53:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZN3BigC1Ev
	lea	rax, -32[rbp]
	mov	rcx, QWORD PTR 16[rbp]
	mov	rdx, rax
	call	_ZN3BigC1ERKS_
	nop
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z11make_forcedRK3Big
	.def	_Z11make_forcedRK3Big;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11make_forcedRK3Big
_Z11make_forcedRK3Big:
.LFB54:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN3BigC1ERKS_
	nop
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB55:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 96
	.seh_stackalloc	96
	.seh_endprologue
	call	__main
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZN3BigC1Ev
	lea	rax, -64[rbp]
	lea	rdx, -32[rbp]
	mov	rcx, rax
	call	_Z11make_forcedRK3Big
	mov	eax, DWORD PTR -64[rbp]
	add	rsp, 96
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
