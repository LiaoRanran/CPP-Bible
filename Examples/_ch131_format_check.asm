	.file	"_ch131_format_check.cpp"
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
.LFB55:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rbx, .LC0[rip]
	lea	rdx, _ZTAXtl12fixed_stringILy19EEtlA19_cLc112ELc105ELc61ELc123ELc125ELc32ELc110ELc97ELc109ELc101ELc61ELc123ELc125ELc32ELc110ELc61ELc123ELc125EEEE[rip]
	mov	rcx, rbx
	call	_Z6printfPKcz
	lea	rcx, .LC1[rip]
	movabs	rdx, 4614253070214989087
	movq	xmm1, rdx
	call	_Z6printfPKcz
	lea	rdx, .LC2[rip]
	mov	rcx, rbx
	call	_Z6printfPKcz
	mov	edx, 42
	lea	rcx, .LC3[rip]
	call	_Z6printfPKcz
	xor	eax, eax
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
.LFB62:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rbx, .LC0[rip]
	call	__main
	lea	rdx, _ZTAXtl12fixed_stringILy19EEtlA19_cLc112ELc105ELc61ELc123ELc125ELc32ELc110ELc97ELc109ELc101ELc61ELc123ELc125ELc32ELc110ELc61ELc123ELc125EEEE[rip]
	mov	rcx, rbx
	call	_Z6printfPKcz
	lea	rcx, .LC1[rip]
	movabs	rdx, 4614253070214989087
	movq	xmm1, rdx
	call	_Z6printfPKcz
	lea	rdx, .LC2[rip]
	mov	rcx, rbx
	call	_Z6printfPKcz
	mov	edx, 42
	lea	rcx, .LC3[rip]
	call	_Z6printfPKcz
	xor	eax, eax
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.globl	_ZTAXtl12fixed_stringILy19EEtlA19_cLc112ELc105ELc61ELc123ELc125ELc32ELc110ELc97ELc109ELc101ELc61ELc123ELc125ELc32ELc110ELc61ELc123ELc125EEEE
	.section	.rdata$_ZTAXtl12fixed_stringILy19EEtlA19_cLc112ELc105ELc61ELc123ELc125ELc32ELc110ELc97ELc109ELc101ELc61ELc123ELc125ELc32ELc110ELc61ELc123ELc125EEEE,"dr"
	.linkonce same_size
	.align 16
_ZTAXtl12fixed_stringILy19EEtlA19_cLc112ELc105ELc61ELc123ELc125ELc32ELc110ELc97ELc109ELc101ELc61ELc123ELc125ELc32ELc110ELc61ELc123ELc125EEEE:
	.ascii "pi={} name={} n={}\0"
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
