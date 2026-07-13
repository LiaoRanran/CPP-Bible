	.file	"_ch128_shared_ptr.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN13my_shared_ptrI6WidgetED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN13my_shared_ptrI6WidgetED1Ev
	.def	_ZN13my_shared_ptrI6WidgetED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13my_shared_ptrI6WidgetED1Ev
_ZN13my_shared_ptrI6WidgetED1Ev:
.LFB829:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	test	rax, rax
	mov	rbx, rcx
	je	.L1
	lock sub	DWORD PTR [rax], 1
	jne	.L1
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L5
	mov	edx, 4
	call	_ZdlPvy
.L5:
	mov	rcx, QWORD PTR 8[rbx]
	test	rcx, rcx
	je	.L1
	mov	edx, 8
	add	rsp, 32
	pop	rbx
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L1:
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB715:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	call	__main
	mov	ecx, 4
	call	_Znwy
	mov	ecx, 8
	mov	DWORD PTR [rax], 42
	mov	rbx, rax
	mov	QWORD PTR 32[rsp], rax
	call	_Znwy
	movq	xmm0, rbx
	movq	xmm1, rax
	mov	QWORD PTR [rax], 1
	punpcklqdq	xmm0, xmm1
	mov	QWORD PTR 40[rsp], rax
	movaps	XMMWORD PTR 48[rsp], xmm0
	lock add	DWORD PTR [rax], 1
	xor	eax, eax
	mov	rdx, QWORD PTR 40[rsp]
	test	rdx, rdx
	je	.L17
	mov	eax, DWORD PTR [rdx]
.L17:
	mov	rdx, QWORD PTR 48[rsp]
	lea	rcx, 48[rsp]
	add	eax, DWORD PTR [rdx]
	mov	ebx, eax
	call	_ZN13my_shared_ptrI6WidgetED1Ev
	lea	rcx, 32[rsp]
	call	_ZN13my_shared_ptrI6WidgetED1Ev
	mov	eax, ebx
	add	rsp, 64
	pop	rbx
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
