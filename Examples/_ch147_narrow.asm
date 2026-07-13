	.file	"_ch147_narrow.cpp"
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
	.ascii "%f\12\0"
	.text
	.p2align 4
	.globl	_Z4sinkd
	.def	_Z4sinkd;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4sinkd
_Z4sinkd:
.LFB49:
	.seh_endprologue
	lea	rcx, .LC0[rip]
	movq	rdx, xmm0
	movapd	xmm1, xmm0
	jmp	_Z6printfPKcz
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC1:
	.ascii "%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB50:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	lea	rcx, .LC0[rip]
	movabs	rdx, 4679546776582094848
	movq	xmm1, rdx
	call	_Z6printfPKcz
	mov	edx, 3
	lea	rcx, .LC1[rip]
	call	_Z6printfPKcz
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
