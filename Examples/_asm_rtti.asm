	.file	"_asm_rtti.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK3Der1fEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK3Der1fEv
	.def	_ZNK3Der1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK3Der1fEv
_ZNK3Der1fEv:
.LFB65:
	.seh_endprologue
	mov	eax, 2
	ret
	.seh_endproc
	.section	.text$_ZN3DerD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3DerD1Ev
	.def	_ZN3DerD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3DerD1Ev
_ZN3DerD1Ev:
.LFB82:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN3DerD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3DerD0Ev
	.def	_ZN3DerD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3DerD0Ev
_ZN3DerD0Ev:
.LFB83:
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
.LFB26:
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
	.text
	.p2align 4
	.globl	_Z8get_nameRK4Base
	.def	_Z8get_nameRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8get_nameRK4Base
_Z8get_nameRK4Base:
.LFB66:
	.seh_endprologue
	xor	edx, edx
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR -8[rax]
	mov	rax, QWORD PTR 8[rax]
	cmp	BYTE PTR [rax], 42
	sete	dl
	add	rax, rdx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9down_castPK4Base
	.def	_Z9down_castPK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9down_castPK4Base
_Z9down_castPK4Base:
.LFB67:
	.seh_endprologue
	test	rcx, rcx
	je	.L9
	lea	r8, _ZTI3Der[rip]
	xor	r9d, r9d
	lea	rdx, _ZTI4Base[rip]
	jmp	__dynamic_cast
	.p2align 4,,10
	.p2align 3
.L9:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z13down_cast_refRK4Base
	.def	_Z13down_cast_refRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13down_cast_refRK4Base
_Z13down_cast_refRK4Base:
.LFB68:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	r8, _ZTI3Der[rip]
	xor	r9d, r9d
	lea	rdx, _ZTI4Base[rip]
	call	__dynamic_cast
	test	rax, rax
	je	.L13
	add	rsp, 40
	ret
.L13:
	call	__cxa_bad_cast
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "%s\12\0"
.LC1:
	.ascii "ok %d\12\0"
.LC2:
	.ascii "%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB69:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	call	__main
	lea	rax, _ZTV3Der[rip+16]
	mov	QWORD PTR 40[rsp], rax
	mov	rax, QWORD PTR _ZTV3Der[rip+8]
	lea	rbx, 40[rsp]
	lea	rcx, .LC0[rip]
	mov	rdx, QWORD PTR 8[rax]
	xor	eax, eax
	cmp	BYTE PTR [rdx], 42
	sete	al
	add	rdx, rax
	call	_Z6printfPKcz
	mov	rcx, rbx
	call	_Z9down_castPK4Base
	test	rax, rax
	mov	rcx, rax
	je	.L16
	mov	rax, QWORD PTR [rax]
	call	[QWORD PTR 16[rax]]
	lea	rcx, .LC1[rip]
	mov	edx, eax
	call	_Z6printfPKcz
.L16:
	mov	rcx, rbx
	call	_Z13down_cast_refRK4Base
	mov	rcx, rax
	mov	rax, QWORD PTR [rax]
	call	[QWORD PTR 16[rax]]
	lea	rcx, .LC2[rip]
	mov	edx, eax
	call	_Z6printfPKcz
	xor	eax, eax
	add	rsp, 48
	pop	rbx
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
	.globl	_ZTS3Der
	.section	.rdata$_ZTS3Der,"dr"
	.linkonce same_size
_ZTS3Der:
	.ascii "3Der\0"
	.globl	_ZTI3Der
	.section	.rdata$_ZTI3Der,"dr"
	.linkonce same_size
	.align 8
_ZTI3Der:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS3Der
	.quad	_ZTI4Base
	.globl	_ZTV3Der
	.section	.rdata$_ZTV3Der,"dr"
	.linkonce same_size
	.align 8
_ZTV3Der:
	.quad	0
	.quad	_ZTI3Der
	.quad	_ZN3DerD1Ev
	.quad	_ZN3DerD0Ev
	.quad	_ZNK3Der1fEv
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	__dynamic_cast;	.scl	2;	.type	32;	.endef
	.def	__cxa_bad_cast;	.scl	2;	.type	32;	.endef
