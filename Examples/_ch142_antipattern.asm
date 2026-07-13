	.file	"_ch142_antipattern.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN7Monster6updateEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7Monster6updateEv
	.def	_ZN7Monster6updateEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7Monster6updateEv
_ZN7Monster6updateEv:
.LFB1715:
	.seh_endprologue
	movss	xmm0, DWORD PTR .LC0[rip]
	addss	xmm0, DWORD PTR 8[rcx]
	movss	DWORD PTR 8[rcx], xmm0
	ret
	.seh_endproc
	.section	.text$_ZN7MonsterD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7MonsterD1Ev
	.def	_ZN7MonsterD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7MonsterD1Ev
_ZN7MonsterD1Ev:
.LFB1809:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN7MonsterD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7MonsterD0Ev
	.def	_ZN7MonsterD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7MonsterD0Ev
_ZN7MonsterD0Ev:
.LFB1810:
	.seh_endprologue
	mov	edx, 16
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z14monster_systemRSt6vectorI11MonsterDataSaIS0_EE
	.def	_Z14monster_systemRSt6vectorI11MonsterDataSaIS0_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14monster_systemRSt6vectorI11MonsterDataSaIS0_EE
_Z14monster_systemRSt6vectorI11MonsterDataSaIS0_EE:
.LFB1716:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rdx, QWORD PTR 8[rcx]
	cmp	rdx, rax
	je	.L5
	movss	xmm1, DWORD PTR .LC0[rip]
	.p2align 4,,10
	.p2align 3
.L7:
	movss	xmm0, DWORD PTR [rax]
	add	rax, 8
	addss	xmm0, xmm1
	movss	DWORD PTR -8[rax], xmm0
	cmp	rax, rdx
	jne	.L7
.L5:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1721:
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
	call	__main
	mov	ecx, 1024
	call	_Znwy
	lea	rcx, _ZTV7Monster[rip+16]
	mov	rdi, rax
	lea	r8, 1032[rdi]
	mov	rdx, rdi
	lea	rax, 8[rax]
	.p2align 4,,10
	.p2align 3
.L10:
	mov	QWORD PTR [rax], 0
	add	rax, 64
	mov	QWORD PTR -48[rax], 0
	mov	QWORD PTR -32[rax], 0
	mov	QWORD PTR -16[rax], 0
	mov	QWORD PTR -72[rax], rcx
	mov	QWORD PTR -56[rax], rcx
	mov	QWORD PTR -40[rax], rcx
	mov	QWORD PTR -24[rax], rcx
	cmp	rax, r8
	jne	.L10
	cvttss2si	ebp, DWORD PTR 8[rdi]
	lea	rsi, 1024[rdi]
	movss	xmm1, DWORD PTR .LC0[rip]
	.p2align 4,,10
	.p2align 3
.L11:
	movss	xmm0, DWORD PTR [rdx]
	add	rdx, 8
	addss	xmm0, xmm1
	movss	DWORD PTR -8[rdx], xmm0
	cmp	rsi, rdx
	jne	.L11
	mov	rbx, rdi
	.p2align 4,,10
	.p2align 3
.L12:
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	add	rbx, 16
	call	[QWORD PTR [rax]]
	cmp	rbx, rsi
	jne	.L12
	mov	edx, 1024
	mov	rcx, rdi
	call	_ZdlPvy
	mov	eax, ebp
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.globl	_ZTS10GameObject
	.section	.rdata$_ZTS10GameObject,"dr"
	.linkonce same_size
	.align 8
_ZTS10GameObject:
	.ascii "10GameObject\0"
	.globl	_ZTI10GameObject
	.section	.rdata$_ZTI10GameObject,"dr"
	.linkonce same_size
	.align 8
_ZTI10GameObject:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS10GameObject
	.globl	_ZTS7Monster
	.section	.rdata$_ZTS7Monster,"dr"
	.linkonce same_size
	.align 8
_ZTS7Monster:
	.ascii "7Monster\0"
	.globl	_ZTI7Monster
	.section	.rdata$_ZTI7Monster,"dr"
	.linkonce same_size
	.align 8
_ZTI7Monster:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS7Monster
	.quad	_ZTI10GameObject
	.globl	_ZTV7Monster
	.section	.rdata$_ZTV7Monster,"dr"
	.linkonce same_size
	.align 8
_ZTV7Monster:
	.quad	0
	.quad	_ZTI7Monster
	.quad	_ZN7MonsterD1Ev
	.quad	_ZN7MonsterD0Ev
	.quad	_ZN7Monster6updateEv
	.section .rdata,"dr"
	.align 4
.LC0:
	.long	1065353216
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
