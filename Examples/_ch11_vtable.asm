	.file	"_ch11_vtable.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.globl	_ZNK5Shape4areaEv
	.def	_ZNK5Shape4areaEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK5Shape4areaEv
_ZNK5Shape4areaEv:
.LFB0:
	.seh_endprologue
	pxor	xmm0, xmm0
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.globl	_ZNK5Shape5sidesEv
	.def	_ZNK5Shape5sidesEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK5Shape5sidesEv
_ZNK5Shape5sidesEv:
.LFB1:
	.seh_endprologue
	xor	eax, eax
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.globl	_ZN5ShapeD2Ev
	.def	_ZN5ShapeD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN5ShapeD2Ev
_ZN5ShapeD2Ev:
.LFB3:
	.seh_endprologue
	ret
	.seh_endproc
	.globl	_ZN5ShapeD1Ev
	.def	_ZN5ShapeD1Ev;	.scl	2;	.type	32;	.endef
	.set	_ZN5ShapeD1Ev,_ZN5ShapeD2Ev
	.align 2
	.p2align 4
	.globl	_ZN5ShapeD0Ev
	.def	_ZN5ShapeD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN5ShapeD0Ev
_ZN5ShapeD0Ev:
.LFB5:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.p2align 4
	.globl	_Z10total_areaRK5Shape
	.def	_Z10total_areaRK5Shape;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10total_areaRK5Shape
_Z10total_areaRK5Shape:
.LFB8:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 16[rax]]
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
	.globl	_ZTV5Shape
	.section	.rdata$_ZTV5Shape,"dr"
	.linkonce same_size
	.align 8
_ZTV5Shape:
	.quad	0
	.quad	_ZTI5Shape
	.quad	_ZN5ShapeD1Ev
	.quad	_ZN5ShapeD0Ev
	.quad	_ZNK5Shape4areaEv
	.quad	_ZNK5Shape5sidesEv
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
