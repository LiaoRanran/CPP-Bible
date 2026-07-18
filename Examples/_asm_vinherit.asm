	.file	"_asm_vinherit.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10read_vbaseRK1D
	.def	_Z10read_vbaseRK1D;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10read_vbaseRK1D
_Z10read_vbaseRK1D:
.LFB25:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR -24[rax]
	mov	eax, DWORD PTR 8[rcx+rax]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10cross_castP2M1
	.def	_Z10cross_castP2M1;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10cross_castP2M1
_Z10cross_castP2M1:
.LFB26:
	.seh_endprologue
	test	rcx, rcx
	je	.L5
	mov	rax, QWORD PTR [rcx]
	add	rcx, QWORD PTR -24[rax]
	mov	rax, rcx
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	xor	eax, eax
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "%d %d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB27:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	r8d, 1
	mov	edx, 1
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
