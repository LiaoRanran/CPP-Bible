	.file	"ch88_variant_visit_test.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z14dispatch_visitRKSt7variantIJ1A1B1CEE
	.def	_Z14dispatch_visitRKSt7variantIJ1A1B1CEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14dispatch_visitRKSt7variantIJ1A1B1CEE
_Z14dispatch_visitRKSt7variantIJ1A1B1CEE:
.LFB341:
	.seh_endprologue
	movzx	eax, BYTE PTR 4[rcx]
	cmp	al, 1
	je	.L2
	cmp	al, 2
	mov	eax, DWORD PTR [rcx]
	jne	.L1
	lea	eax, [rax+rax*2]
.L1:
	ret
	.p2align 4,,10
	.p2align 3
.L2:
	mov	eax, DWORD PTR [rcx]
	add	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z15dispatch_manualRKSt7variantIJ1A1B1CEE
	.def	_Z15dispatch_manualRKSt7variantIJ1A1B1CEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15dispatch_manualRKSt7variantIJ1A1B1CEE
_Z15dispatch_manualRKSt7variantIJ1A1B1CEE:
.LFB348:
	.seh_endprologue
	movzx	eax, BYTE PTR 4[rcx]
	cmp	al, 1
	je	.L7
	cmp	al, 2
	je	.L8
	xor	edx, edx
	test	al, al
	jne	.L6
	mov	edx, DWORD PTR [rcx]
.L6:
	mov	eax, edx
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	mov	eax, DWORD PTR [rcx]
	lea	edx, [rax+rax*2]
	mov	eax, edx
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	mov	edx, DWORD PTR [rcx]
	add	edx, edx
	mov	eax, edx
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB349:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	lea	rcx, 40[rsp]
	mov	QWORD PTR 40[rsp], 7
	mov	DWORD PTR 36[rsp], 0
	call	_Z14dispatch_visitRKSt7variantIJ1A1B1CEE
	mov	DWORD PTR 36[rsp], eax
	call	_Z15dispatch_manualRKSt7variantIJ1A1B1CEE
	mov	DWORD PTR 36[rsp], eax
	mov	eax, DWORD PTR 36[rsp]
	add	rsp, 56
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
