	.file	"_ch141_perf.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK10MemStorage3getEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK10MemStorage3getEv
	.def	_ZNK10MemStorage3getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK10MemStorage3getEv
_ZNK10MemStorage3getEv:
.LFB47:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	eax, 42
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z11via_virtualRK8IStorage
	.def	_Z11via_virtualRK8IStorage;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11via_virtualRK8IStorage
_Z11via_virtualRK8IStorage:
.LFB48:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	add	rax, 16
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK11FastStorage3getEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK11FastStorage3getEv
	.def	_ZNK11FastStorage3getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK11FastStorage3getEv
_ZNK11FastStorage3getEv:
.LFB49:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	eax, 42
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN8IStorageD2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN8IStorageD2Ev
	.def	_ZN8IStorageD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN8IStorageD2Ev
_ZN8IStorageD2Ev:
.LFB57:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTV8IStorage[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN10MemStorageD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN10MemStorageD1Ev
	.def	_ZN10MemStorageD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN10MemStorageD1Ev
_ZN10MemStorageD1Ev:
.LFB64:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTV10MemStorage[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN8IStorageD2Ev
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN10MemStorageD0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN10MemStorageD0Ev
	.def	_ZN10MemStorageD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN10MemStorageD0Ev
_ZN10MemStorageD0Ev:
.LFB65:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN10MemStorageD1Ev
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 8
	mov	rcx, rax
	call	_ZdlPvy
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB51:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 72
	.seh_stackalloc	72
	lea	rbp, 64[rsp]
	.seh_setframe	rbp, 64
	.seh_endprologue
	call	__main
	lea	rax, _ZTV10MemStorage[rip+16]
	mov	QWORD PTR -8[rbp], rax
	lea	rax, -8[rbp]
	mov	rcx, rax
.LEHB0:
	call	_Z11via_virtualRK8IStorage
.LEHE0:
	mov	DWORD PTR -16[rbp], eax
	lea	rax, -9[rbp]
	mov	rcx, rax
	call	_Z12via_templateI11FastStorageEiRKT_
	mov	DWORD PTR -20[rbp], eax
	mov	edx, DWORD PTR -16[rbp]
	mov	eax, DWORD PTR -20[rbp]
	lea	ebx, [rdx+rax]
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZN10MemStorageD1Ev
	mov	eax, ebx
	jmp	.L14
.L13:
	mov	rbx, rax
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZN10MemStorageD1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB1:
	call	_Unwind_Resume
.LEHE1:
.L14:
	add	rsp, 72
	pop	rbx
	pop	rbp
	ret
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA51:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE51-.LLSDACSB51
.LLSDACSB51:
	.uleb128 .LEHB0-.LFB51
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L13-.LFB51
	.uleb128 0
	.uleb128 .LEHB1-.LFB51
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE51:
	.text
	.seh_endproc
	.section	.text$_Z12via_templateI11FastStorageEiRKT_,"x"
	.linkonce discard
	.globl	_Z12via_templateI11FastStorageEiRKT_
	.def	_Z12via_templateI11FastStorageEiRKT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12via_templateI11FastStorageEiRKT_
_Z12via_templateI11FastStorageEiRKT_:
.LFB66:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNK11FastStorage3getEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	_ZTV10MemStorage
	.section	.rdata$_ZTV10MemStorage,"dr"
	.linkonce same_size
	.align 8
_ZTV10MemStorage:
	.quad	0
	.quad	_ZTI10MemStorage
	.quad	_ZN10MemStorageD1Ev
	.quad	_ZN10MemStorageD0Ev
	.quad	_ZNK10MemStorage3getEv
	.globl	_ZTV8IStorage
	.section	.rdata$_ZTV8IStorage,"dr"
	.linkonce same_size
	.align 8
_ZTV8IStorage:
	.quad	0
	.quad	_ZTI8IStorage
	.quad	0
	.quad	0
	.quad	__cxa_pure_virtual
	.globl	_ZTI10MemStorage
	.section	.rdata$_ZTI10MemStorage,"dr"
	.linkonce same_size
	.align 8
_ZTI10MemStorage:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS10MemStorage
	.quad	_ZTI8IStorage
	.globl	_ZTS10MemStorage
	.section	.rdata$_ZTS10MemStorage,"dr"
	.linkonce same_size
	.align 8
_ZTS10MemStorage:
	.ascii "10MemStorage\0"
	.globl	_ZTI8IStorage
	.section	.rdata$_ZTI8IStorage,"dr"
	.linkonce same_size
	.align 8
_ZTI8IStorage:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS8IStorage
	.globl	_ZTS8IStorage
	.section	.rdata$_ZTS8IStorage,"dr"
	.linkonce same_size
	.align 8
_ZTS8IStorage:
	.ascii "8IStorage\0"
	.weak	__cxa_pure_virtual
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__cxa_pure_virtual;	.scl	2;	.type	32;	.endef
