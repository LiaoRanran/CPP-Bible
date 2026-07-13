	.file	"_ch133_eventloop.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z14process_eventsP9FileEventy
	.def	_Z14process_eventsP9FileEventy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14process_eventsP9FileEventy
_Z14process_eventsP9FileEventy:
.LFB16:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	test	rdx, rdx
	mov	rdi, rdx
	je	.L1
	mov	rbx, rcx
	xor	esi, esi
	.p2align 4,,10
	.p2align 3
.L4:
	mov	rax, QWORD PTR 8[rbx]
	test	rax, rax
	je	.L3
	mov	rdx, QWORD PTR 16[rbx]
	mov	ecx, DWORD PTR [rbx]
	call	rax
.L3:
	add	rsi, 1
	add	rbx, 24
	cmp	rdi, rsi
	jne	.L4
.L1:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB17:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, 1
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
