	.file	"_ch117_move_trap.cpp"
	.intel_syntax noprefix
	.text
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
	.section .rdata,"dr"
.LC0:
	.ascii "move!\12\0"
	.text
	.p2align 4
	.globl	_Z3badv
	.def	_Z3badv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3badv
_Z3badv:
.LFB247:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	lea	rcx, .LC0[rip]
	call	_Z6printfPKcz
	mov	rax, rbx
	mov	DWORD PTR [rbx], 1
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z4goodv
	.def	_Z4goodv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4goodv
_Z4goodv:
.LFB248:
	.seh_endprologue
	mov	rax, rcx
	mov	DWORD PTR [rcx], 1
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB249:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	lea	rcx, .LC0[rip]
	call	_Z6printfPKcz
	mov	eax, 2
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
