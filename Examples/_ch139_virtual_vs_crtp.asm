	.file	"_ch139_virtual_vs_crtp.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK7CircleV4areaEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK7CircleV4areaEv
	.def	_ZNK7CircleV4areaEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK7CircleV4areaEv
_ZNK7CircleV4areaEv:
.LFB4084:
	.seh_endprologue
	movsd	xmm0, QWORD PTR .LC0[rip]
	movsd	xmm1, QWORD PTR 8[rcx]
	mulsd	xmm0, xmm1
	mulsd	xmm0, xmm1
	ret
	.seh_endproc
	.section	.text$_ZN7CircleVD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7CircleVD1Ev
	.def	_ZN7CircleVD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7CircleVD1Ev
_ZN7CircleVD1Ev:
.LFB4095:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN7CircleVD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7CircleVD0Ev
	.def	_ZN7CircleVD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7CircleVD0Ev
_ZN7CircleVD0Ev:
.LFB4096:
	.seh_endprologue
	mov	edx, 16
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z9process_vRK6ShapeV
	.def	_Z9process_vRK6ShapeV;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9process_vRK6ShapeV
_Z9process_vRK6ShapeV:
.LFB4090:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rdx, _ZNK7CircleV4areaEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR [rax]
	cmp	rax, rdx
	jne	.L6
	movsd	xmm1, QWORD PTR 8[rcx]
	movsd	xmm0, QWORD PTR .LC0[rip]
	mulsd	xmm0, xmm1
	mulsd	xmm0, xmm1
	addsd	xmm0, xmm0
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	call	rax
	addsd	xmm0, xmm0
	add	rsp, 40
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9process_cRK6ShapeCI7CircleCE
	.def	_Z9process_cRK6ShapeCI7CircleCE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9process_cRK6ShapeCI7CircleCE
_Z9process_cRK6ShapeCI7CircleCE:
.LFB4091:
	.seh_endprologue
	movsd	xmm0, QWORD PTR .LC0[rip]
	movsd	xmm1, QWORD PTR [rcx]
	mulsd	xmm0, xmm1
	mulsd	xmm0, xmm1
	addsd	xmm0, xmm0
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4092:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	movsd	xmm1, QWORD PTR .LC1[rip]
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	call	_ZNSo9_M_insertIdEERSoT_
	mov	r8d, 1
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	1413754136
	.long	1074340347
	.align 8
.LC1:
	.long	1413754136
	.long	1078534651
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
