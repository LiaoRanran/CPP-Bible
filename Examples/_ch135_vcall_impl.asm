	.file	"_ch135_vcall_impl.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.globl	_ZNK3Dog5speakEv
	.def	_ZNK3Dog5speakEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK3Dog5speakEv
_ZNK3Dog5speakEv:
.LFB0:
	.seh_endprologue
	mov	eax, 42
	ret
	.seh_endproc
	.section	.text$_ZN3DogD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3DogD1Ev
	.def	_ZN3DogD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3DogD1Ev
_ZN3DogD1Ev:
.LFB8:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN3DogD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3DogD0Ev
	.def	_ZN3DogD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3DogD0Ev
_ZN3DogD0Ev:
.LFB9:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z11via_virtualRK6Animal
	.def	_Z11via_virtualRK6Animal;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11via_virtualRK6Animal
_Z11via_virtualRK6Animal:
.LFB1:
	.seh_endprologue
	lea	rdx, _ZNK3Dog5speakEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR 16[rax]
	cmp	rax, rdx
	jne	.L7
	mov	eax, 42
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	rex.W jmp	rax
	.seh_endproc
	.globl	_ZTS6Animal
	.section	.rdata$_ZTS6Animal,"dr"
	.linkonce same_size
	.align 8
_ZTS6Animal:
	.ascii "6Animal\0"
	.globl	_ZTI6Animal
	.section	.rdata$_ZTI6Animal,"dr"
	.linkonce same_size
	.align 8
_ZTI6Animal:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS6Animal
	.globl	_ZTS3Dog
	.section	.rdata$_ZTS3Dog,"dr"
	.linkonce same_size
_ZTS3Dog:
	.ascii "3Dog\0"
	.globl	_ZTI3Dog
	.section	.rdata$_ZTI3Dog,"dr"
	.linkonce same_size
	.align 8
_ZTI3Dog:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS3Dog
	.quad	_ZTI6Animal
	.globl	_ZTV3Dog
	.section	.rdata$_ZTV3Dog,"dr"
	.linkonce same_size
	.align 8
_ZTV3Dog:
	.quad	0
	.quad	_ZTI3Dog
	.quad	_ZN3DogD1Ev
	.quad	_ZN3DogD0Ev
	.quad	_ZNK3Dog5speakEv
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
