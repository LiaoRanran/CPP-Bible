	.file	"_ch131_format_check.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "%s\0"
.LC1:
	.ascii "%g\0"
.LC2:
	.ascii "fmt\0"
.LC3:
	.ascii "%d\0"
	.text
	.p2align 4
	.globl	_Z4demov
	.def	_Z4demov;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4demov
_Z4demov:
.LFB30:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rdx, _ZTAXtl12fixed_stringILy19EEtlA19_cLc112ELc105ELc61ELc123ELc125ELc32ELc110ELc97ELc109ELc101ELc61ELc123ELc125ELc32ELc110ELc61ELc123ELc125EEEE[rip]
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	lea	rcx, .LC1[rip]
	movabs	rdx, 4614253070214989087
	movq	xmm1, rdx
	call	__mingw_printf
	lea	rdx, .LC2[rip]
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	mov	edx, 42
	lea	rcx, .LC3[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB37:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	lea	rdx, _ZTAXtl12fixed_stringILy19EEtlA19_cLc112ELc105ELc61ELc123ELc125ELc32ELc110ELc97ELc109ELc101ELc61ELc123ELc125ELc32ELc110ELc61ELc123ELc125EEEE[rip]
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	lea	rcx, .LC1[rip]
	movabs	rdx, 4614253070214989087
	movq	xmm1, rdx
	call	__mingw_printf
	lea	rdx, .LC2[rip]
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	mov	edx, 42
	lea	rcx, .LC3[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.globl	_ZTAXtl12fixed_stringILy19EEtlA19_cLc112ELc105ELc61ELc123ELc125ELc32ELc110ELc97ELc109ELc101ELc61ELc123ELc125ELc32ELc110ELc61ELc123ELc125EEEE
	.section	.rdata$_ZTAXtl12fixed_stringILy19EEtlA19_cLc112ELc105ELc61ELc123ELc125ELc32ELc110ELc97ELc109ELc101ELc61ELc123ELc125ELc32ELc110ELc61ELc123ELc125EEEE,"dr"
	.linkonce same_size
	.align 16
_ZTAXtl12fixed_stringILy19EEtlA19_cLc112ELc105ELc61ELc123ELc125ELc32ELc110ELc97ELc109ELc101ELc61ELc123ELc125ELc32ELc110ELc61ELc123ELc125EEEE:
	.ascii "pi={} name={} n={}\0"
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
