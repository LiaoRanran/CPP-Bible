	.file	"_ch151_virtual.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK1A1fEi,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK1A1fEi
	.def	_ZNK1A1fEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK1A1fEi
_ZNK1A1fEi:
.LFB5564:
	.seh_endprologue
	lea	eax, [rdx+rdx]
	ret
	.seh_endproc
	.section	.text$_ZN1AD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1AD1Ev
	.def	_ZN1AD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1AD1Ev
_ZN1AD1Ev:
.LFB5579:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN1AD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1AD0Ev
	.def	_ZN1AD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1AD0Ev
_ZN1AD0Ev:
.LFB5580:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
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
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC1:
	.ascii "virtual: ms=%.3f r=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5566:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	xor	ebx, ebx
	call	__main
	lea	rax, _ZTV1A[rip+16]
	mov	QWORD PTR 40[rsp], rax
	lea	rsi, 40[rsp]
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	DWORD PTR 36[rsp], 0
	mov	rdi, rax
	.p2align 4,,10
	.p2align 3
.L7:
	mov	rax, QWORD PTR 40[rsp]
	mov	edx, ebx
	mov	rcx, rsi
	add	ebx, 1
	call	[QWORD PTR 16[rax]]
	mov	edx, eax
	mov	eax, DWORD PTR 36[rsp]
	add	eax, edx
	cmp	ebx, 100000000
	mov	DWORD PTR 36[rsp], eax
	jne	.L7
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r8d, DWORD PTR 36[rsp]
	lea	rcx, .LC1[rip]
	pxor	xmm1, xmm1
	sub	rax, rdi
	cvtsi2sd	xmm1, rax
	divsd	xmm1, QWORD PTR .LC0[rip]
	movq	rdx, xmm1
	call	_Z6printfPKcz
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.globl	_ZTS4Base
	.section	.rdata$_ZTS4Base,"dr"
	.linkonce same_size
_ZTS4Base:
	.ascii "4Base\0"
	.globl	_ZTI4Base
	.section	.rdata$_ZTI4Base,"dr"
	.linkonce same_size
	.align 8
_ZTI4Base:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS4Base
	.globl	_ZTS1A
	.section	.rdata$_ZTS1A,"dr"
	.linkonce same_size
_ZTS1A:
	.ascii "1A\0"
	.globl	_ZTI1A
	.section	.rdata$_ZTI1A,"dr"
	.linkonce same_size
	.align 8
_ZTI1A:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS1A
	.quad	_ZTI4Base
	.globl	_ZTV1A
	.section	.rdata$_ZTV1A,"dr"
	.linkonce same_size
	.align 8
_ZTV1A:
	.quad	0
	.quad	_ZTI1A
	.quad	_ZN1AD1Ev
	.quad	_ZN1AD0Ev
	.quad	_ZNK1A1fEi
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1093567616
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
