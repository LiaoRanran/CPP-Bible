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
.LFB806:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	r8, rcx
	test	rax, rax
	je	.L1
	lock sub	DWORD PTR [rax], 1
	jne	.L1
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L5
	mov	edx, 4
	mov	QWORD PTR 40[rsp], r8
	call	_ZdlPvy
	mov	r8, QWORD PTR 40[rsp]
.L5:
	mov	rcx, QWORD PTR 8[r8]
	test	rcx, rcx
	je	.L1
	mov	edx, 8
	add	rsp, 56
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L1:
	add	rsp, 56
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB692:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
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
	mov	rsi, rax
	mov	QWORD PTR 32[rsp], rax
	call	_Znwy
	mov	rbx, rax
	mov	QWORD PTR [rax], 1
	mov	QWORD PTR 56[rsp], rax
	lock add	DWORD PTR [rax], 1
	mov	edi, DWORD PTR [rax]
	add	edi, DWORD PTR [rsi]
	lea	rcx, 48[rsp]
	mov	QWORD PTR 48[rsp], rsi
	call	_ZN13my_shared_ptrI6WidgetED1Ev
	lea	rcx, 32[rsp]
	mov	QWORD PTR 40[rsp], rbx
	call	_ZN13my_shared_ptrI6WidgetED1Ev
	mov	eax, edi
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
