	.file	"_ch127_inline.cpp"
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
	.text
	.globl	_Z12add_noinlineii
	.def	_Z12add_noinlineii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12add_noinlineii
_Z12add_noinlineii:
.LFB47:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	mov	edx, DWORD PTR 16[rbp]
	mov	eax, DWORD PTR 24[rbp]
	add	eax, edx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z10add_inlineii,"x"
	.linkonce discard
	.globl	_Z10add_inlineii
	.def	_Z10add_inlineii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10add_inlineii
_Z10add_inlineii:
.LFB48:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	mov	edx, DWORD PTR 16[rbp]
	mov	eax, DWORD PTR 24[rbp]
	add	eax, edx
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z11use_inlinedv
	.def	_Z11use_inlinedv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11use_inlinedv
_Z11use_inlinedv:
.LFB49:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	DWORD PTR -4[rbp], 0
	mov	DWORD PTR -8[rbp], 0
	jmp	.L8
.L9:
	mov	eax, DWORD PTR -8[rbp]
	mov	edx, 1
	mov	ecx, eax
	call	_Z10add_inlineii
	add	DWORD PTR -4[rbp], eax
	add	DWORD PTR -8[rbp], 1
.L8:
	cmp	DWORD PTR -8[rbp], 3
	jle	.L9
	mov	eax, DWORD PTR -4[rbp]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z12use_noinlinev
	.def	_Z12use_noinlinev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12use_noinlinev
_Z12use_noinlinev:
.LFB50:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	edx, 4
	mov	ecx, 3
	call	_Z12add_noinlineii
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "%d %d\12\0"
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB51:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	__main
	call	_Z12use_noinlinev
	mov	ebx, eax
	call	_Z11use_inlinedv
	mov	r8d, ebx
	mov	edx, eax
	lea	rax, .LC0[rip]
	mov	rcx, rax
	call	_Z6printfPKcz
	mov	eax, 0
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
