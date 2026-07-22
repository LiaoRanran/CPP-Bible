	.file	"_ch112_hp.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	hp_protect
	.def	hp_protect;	.scl	2;	.type	32;	.endef
	.seh_proc	hp_protect
hp_protect:
.LFB689:
	.seh_endprologue
	lea	rax, g_hp[rip]
	movsxd	rdx, edx
	lea	rdx, [rax+rdx*8]
	.p2align 5
	.p2align 4
	.p2align 3
.L2:
	mov	rax, QWORD PTR [rcx]
	mov	r9, rax
	xchg	r9, QWORD PTR [rdx]
	mov	r8, QWORD PTR [rcx]
	cmp	rax, r8
	jne	.L2
	ret
	.seh_endproc
	.p2align 4
	.globl	hp_clear
	.def	hp_clear;	.scl	2;	.type	32;	.endef
	.seh_proc	hp_clear
hp_clear:
.LFB690:
	.seh_endprologue
	lea	rax, g_hp[rip]
	movsxd	rcx, ecx
	mov	QWORD PTR [rax+rcx*8], 0
	ret
	.seh_endproc
	.p2align 4
	.globl	hp_scan_and_reclaim
	.def	hp_scan_and_reclaim;	.scl	2;	.type	32;	.endef
	.seh_proc	hp_scan_and_reclaim
hp_scan_and_reclaim:
.LFB691:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	xor	edi, edi
	xchg	rdi, QWORD PTR g_retired[rip]
	test	rdi, rdi
	je	.L6
	xor	ebp, ebp
	lea	rsi, g_hp[rip+512]
	.p2align 4
	.p2align 3
.L11:
	mov	rbx, rdi
	lea	rax, g_hp[rip]
	mov	rdi, QWORD PTR 8[rdi]
	jmp	.L9
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L29:
	add	rax, 8
	cmp	rax, rsi
	je	.L28
.L9:
	mov	rdx, QWORD PTR [rax]
	mov	rcx, QWORD PTR [rbx]
	cmp	rcx, rdx
	jne	.L29
	mov	QWORD PTR 8[rbx], rbp
	mov	rbp, rbx
.L15:
	test	rdi, rdi
	jne	.L11
	test	rbp, rbp
	je	.L6
	mov	rax, rbp
	.p2align 4
	.p2align 4
	.p2align 3
.L14:
	mov	rdx, rax
	mov	rax, QWORD PTR 8[rax]
	test	rax, rax
	jne	.L14
	mov	rax, QWORD PTR g_retired[rip]
	mov	QWORD PTR 8[rdx], rax
	mov	QWORD PTR g_retired[rip], rbp
.L6:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L28:
	test	rcx, rcx
	je	.L17
	mov	edx, 16
	call	_ZdlPvy
.L17:
	mov	edx, 16
	mov	rcx, rbx
	call	_ZdlPvy
	jmp	.L15
	.seh_endproc
	.globl	g_retired
	.bss
	.align 8
g_retired:
	.space 8
	.globl	g_hp
	.align 64
g_hp:
	.space 512
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
