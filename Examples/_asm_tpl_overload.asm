	.file	"_asm_tpl_overload.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z1fi
	.def	_Z1fi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1fi
_Z1fi:
.LFB191:
	.seh_endprologue
	movsx	rax, DWORD PTR g_i[rip]
	lea	edx, 1[rax]
	mov	DWORD PTR g_i[rip], edx
	lea	rdx, g_log[rip]
	mov	DWORD PTR [rdx+rax*4], 100
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z1gi
	.def	_Z1gi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1gi
_Z1gi:
.LFB194:
	.seh_endprologue
	movsx	rax, DWORD PTR g_i[rip]
	lea	edx, 1[rax]
	mov	DWORD PTR g_i[rip], edx
	lea	rdx, g_log[rip]
	mov	DWORD PTR [rdx+rax*4], 11
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB196:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	movsx	rax, DWORD PTR g_i[rip]
	lea	r9, g_log[rip]
	mov	DWORD PTR [r9+rax*4], 100
	lea	edx, 1[rax]
	mov	rcx, rax
	lea	eax, 2[rax]
	movsx	rdx, edx
	cdqe
	mov	DWORD PTR [r9+rdx*4], 100
	mov	DWORD PTR [r9+rax*4], 300
	lea	edx, 3[rcx]
	lea	eax, 4[rcx]
	add	ecx, 5
	movsx	rdx, edx
	cdqe
	test	ecx, ecx
	mov	DWORD PTR [r9+rdx*4], 22
	mov	DWORD PTR g_i[rip], ecx
	mov	DWORD PTR [r9+rax*4], 11
	jle	.L7
	xor	eax, eax
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L6:
	movsx	r8, eax
	add	eax, 1
	mov	r8d, DWORD PTR [r9+r8*4]
	add	edx, r8d
	cmp	eax, ecx
	jne	.L6
.L4:
	mov	eax, edx
	add	rsp, 40
	ret
.L7:
	xor	edx, edx
	jmp	.L4
	.seh_endproc
	.globl	g_i
	.bss
	.align 4
g_i:
	.space 4
	.globl	g_log
	.align 32
g_log:
	.space 32
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
