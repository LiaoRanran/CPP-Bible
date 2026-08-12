	.file	"_ch158_vcall.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.globl	_ZNK6Circle4areaEv
	.def	_ZNK6Circle4areaEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK6Circle4areaEv
_ZNK6Circle4areaEv:
.LFB0:
	.seh_endprologue
	movsd	xmm0, QWORD PTR .LC0[rip]
	movsd	xmm1, QWORD PTR 8[rcx]
	mulsd	xmm0, xmm1
	mulsd	xmm0, xmm1
	ret
	.seh_endproc
	.section	.text$_ZN6CircleD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN6CircleD1Ev
	.def	_ZN6CircleD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6CircleD1Ev
_ZN6CircleD1Ev:
.LFB8:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN6CircleD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN6CircleD0Ev
	.def	_ZN6CircleD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6CircleD0Ev
_ZN6CircleD0Ev:
.LFB9:
	.seh_endprologue
	mov	edx, 16
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z12compute_areaRK5Shape
	.def	_Z12compute_areaRK5Shape;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12compute_areaRK5Shape
_Z12compute_areaRK5Shape:
.LFB1:
	.seh_endprologue
	lea	rdx, _ZNK6Circle4areaEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR 16[rax]
	cmp	rax, rdx
	jne	.L10
	movsd	xmm1, QWORD PTR 8[rcx]
	movsd	xmm0, QWORD PTR .LC0[rip]
	mulsd	xmm0, xmm1
	mulsd	xmm0, xmm1
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	rex.W jmp	rax
	.seh_endproc
	.globl	_ZTS5Shape
	.section	.rdata$_ZTS5Shape,"dr"
	.linkonce same_size
_ZTS5Shape:
	.ascii "5Shape\0"
	.globl	_ZTI5Shape
	.section	.rdata$_ZTI5Shape,"dr"
	.linkonce same_size
	.align 8
_ZTI5Shape:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS5Shape
	.globl	_ZTS6Circle
	.section	.rdata$_ZTS6Circle,"dr"
	.linkonce same_size
	.align 8
_ZTS6Circle:
	.ascii "6Circle\0"
	.globl	_ZTI6Circle
	.section	.rdata$_ZTI6Circle,"dr"
	.linkonce same_size
	.align 8
_ZTI6Circle:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS6Circle
	.quad	_ZTI5Shape
	.globl	_ZTV6Circle
	.section	.rdata$_ZTV6Circle,"dr"
	.linkonce same_size
	.align 8
_ZTV6Circle:
	.quad	0
	.quad	_ZTI6Circle
	.quad	_ZN6CircleD1Ev
	.quad	_ZN6CircleD0Ev
	.quad	_ZNK6Circle4areaEv
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	1413754136
	.long	1074340347
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
