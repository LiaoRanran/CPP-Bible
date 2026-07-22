	.file	"_ch141_perf.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch141_perf.cpp"
	.section	.text$_ZNK10MemStorage3getEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK10MemStorage3getEv
	.def	_ZNK10MemStorage3getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK10MemStorage3getEv
_ZNK10MemStorage3getEv:
.LFB21:
	.file 1 "Examples/_ch141_perf.cpp"
	.loc 1 9 36
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 1 9 66
	mov	eax, 42
	.loc 1 9 70
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE21:
	.seh_endproc
	.text
	.globl	_Z11via_virtualRK8IStorage
	.def	_Z11via_virtualRK8IStorage;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11via_virtualRK8IStorage
_Z11via_virtualRK8IStorage:
.LFB22:
	.loc 1 10 36
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 1 10 50
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	add	rax, 16
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
.LVL0:
	.loc 1 10 54
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE22:
	.seh_endproc
	.section	.text$_ZNK11FastStorage3getEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK11FastStorage3getEv
	.def	_ZNK11FastStorage3getEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK11FastStorage3getEv
_ZNK11FastStorage3getEv:
.LFB23:
	.loc 1 13 26
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 1 13 47
	mov	eax, 42
	.loc 1 13 51
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE23:
	.seh_endproc
	.section	.text$_ZN8IStorageD2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN8IStorageD2Ev
	.def	_ZN8IStorageD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN8IStorageD2Ev
_ZN8IStorageD2Ev:
.LFB31:
	.loc 1 8 27
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB2:
	.loc 1 8 27
	lea	rdx, _ZTV8IStorage[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
.LBE2:
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE31:
	.seh_endproc
	.section	.text$_ZN10MemStorageD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN10MemStorageD1Ev
	.def	_ZN10MemStorageD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN10MemStorageD1Ev
_ZN10MemStorageD1Ev:
.LFB38:
	.loc 1 9 8
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB3:
	.loc 1 9 8
	lea	rdx, _ZTV10MemStorage[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN8IStorageD2Ev
.LBE3:
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE38:
	.seh_endproc
	.section	.text$_ZN10MemStorageD0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN10MemStorageD0Ev
	.def	_ZN10MemStorageD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN10MemStorageD0Ev
_ZN10MemStorageD0Ev:
.LFB39:
	.loc 1 9 8
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 1 9 8
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN10MemStorageD1Ev
	.loc 1 9 8 is_stmt 0 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 8
	mov	rcx, rax
	call	_ZdlPvy
	nop
	.loc 1 9 8
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE39:
	.seh_endproc
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB25:
	.loc 1 17 12 is_stmt 1
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	sub	rsp, 72
	.seh_stackalloc	72
	.cfi_def_cfa_offset 96
	lea	rbp, 64[rsp]
	.seh_setframe	rbp, 64
	.cfi_def_cfa 6, 32
	.seh_endprologue
	.loc 1 17 12
	call	__main
	.loc 1 18 16
	lea	rax, _ZTV10MemStorage[rip+16]
	mov	QWORD PTR -8[rbp], rax
	.loc 1 20 33
	lea	rax, -8[rbp]
	mov	rcx, rax
.LEHB0:
	call	_Z11via_virtualRK8IStorage
.LEHE0:
	.loc 1 20 36 discriminator 2
	mov	DWORD PTR -16[rbp], eax
	.loc 1 21 34
	lea	rax, -9[rbp]
	mov	rcx, rax
	call	_Z12via_templateI11FastStorageEiRKT_
	.loc 1 21 37 discriminator 1
	mov	DWORD PTR -20[rbp], eax
	.loc 1 22 12
	mov	edx, DWORD PTR -16[rbp]
	.loc 1 22 16
	mov	eax, DWORD PTR -20[rbp]
	lea	ebx, [rdx+rax]
	.loc 1 23 1
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
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -56
	ret
	.cfi_endproc
.LFE25:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA25:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE25-.LLSDACSB25
.LLSDACSB25:
	.uleb128 .LEHB0-.LFB25
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L13-.LFB25
	.uleb128 0
	.uleb128 .LEHB1-.LFB25
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE25:
	.text
	.seh_endproc
	.section	.text$_Z12via_templateI11FastStorageEiRKT_,"x"
	.linkonce discard
	.globl	_Z12via_templateI11FastStorageEiRKT_
	.def	_Z12via_templateI11FastStorageEiRKT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12via_templateI11FastStorageEiRKT_
_Z12via_templateI11FastStorageEiRKT_:
.LFB40:
	.loc 1 15 5
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 1 15 44
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNK11FastStorage3getEv
	.loc 1 15 48
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE40:
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
	.text
.Letext0:
	.file 2 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/stdio.h"
	.file 3 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/corecrt.h"
	.file 4 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/cstdio"
	.file 5 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/x86_64-w64-mingw32/bits/c++config.h"
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0xd93
	.word	0x5
	.byte	0x1
	.byte	0x8
	.secrel32	.Ldebug_abbrev0
	.uleb128 0x1b
	.ascii "GNU C++23 15.3.0 -masm=intel -mtune=generic -march=x86-64 -g -O0 -std=c++23\0"
	.byte	0x21
	.byte	0x4
	.long	0x3163e
	.secrel32	.LASF0
	.secrel32	.LASF1
	.secrel32	.LLRL0
	.quad	0
	.secrel32	.Ldebug_line0
	.uleb128 0x11
	.ascii "__builtin_va_list\0"
	.long	0x8e
	.uleb128 0x6
	.byte	0x1
	.byte	0x6
	.ascii "char\0"
	.uleb128 0x8
	.long	0x8e
	.uleb128 0xe
	.ascii "size_t\0"
	.byte	0x3
	.byte	0x23
	.byte	0x2c
	.long	0xaa
	.uleb128 0x6
	.byte	0x8
	.byte	0x7
	.ascii "long long unsigned int\0"
	.uleb128 0x6
	.byte	0x8
	.byte	0x5
	.ascii "long long int\0"
	.uleb128 0x6
	.byte	0x2
	.byte	0x7
	.ascii "short unsigned int\0"
	.uleb128 0x6
	.byte	0x4
	.byte	0x5
	.ascii "int\0"
	.uleb128 0x1c
	.long	0xeb
	.uleb128 0x6
	.byte	0x4
	.byte	0x5
	.ascii "long int\0"
	.uleb128 0x5
	.long	0x8e
	.uleb128 0x6
	.byte	0x2
	.byte	0x7
	.ascii "wchar_t\0"
	.uleb128 0x6
	.byte	0x4
	.byte	0x7
	.ascii "unsigned int\0"
	.uleb128 0x6
	.byte	0x4
	.byte	0x7
	.ascii "long unsigned int\0"
	.uleb128 0x6
	.byte	0x1
	.byte	0x8
	.ascii "unsigned char\0"
	.uleb128 0x12
	.ascii "_iobuf\0"
	.byte	0x30
	.byte	0x2
	.byte	0x21
	.byte	0xa
	.long	0x1d1
	.uleb128 0x9
	.ascii "_ptr\0"
	.byte	0x25
	.byte	0xb
	.long	0x103
	.byte	0
	.uleb128 0x9
	.ascii "_cnt\0"
	.byte	0x26
	.byte	0x9
	.long	0xeb
	.byte	0x8
	.uleb128 0x9
	.ascii "_base\0"
	.byte	0x27
	.byte	0xb
	.long	0x103
	.byte	0x10
	.uleb128 0x9
	.ascii "_flag\0"
	.byte	0x28
	.byte	0x9
	.long	0xeb
	.byte	0x18
	.uleb128 0x9
	.ascii "_file\0"
	.byte	0x29
	.byte	0x9
	.long	0xeb
	.byte	0x1c
	.uleb128 0x9
	.ascii "_charbuf\0"
	.byte	0x2a
	.byte	0x9
	.long	0xeb
	.byte	0x20
	.uleb128 0x9
	.ascii "_bufsiz\0"
	.byte	0x2b
	.byte	0x9
	.long	0xeb
	.byte	0x24
	.uleb128 0x9
	.ascii "_tmpfname\0"
	.byte	0x2c
	.byte	0xb
	.long	0x103
	.byte	0x28
	.byte	0
	.uleb128 0xe
	.ascii "FILE\0"
	.byte	0x2
	.byte	0x2f
	.byte	0x19
	.long	0x149
	.uleb128 0xe
	.ascii "fpos_t\0"
	.byte	0x2
	.byte	0x70
	.byte	0x25
	.long	0xc4
	.uleb128 0x8
	.long	0x1de
	.uleb128 0x13
	.ascii "std\0"
	.word	0x150
	.long	0x31d
	.uleb128 0x2
	.byte	0x64
	.byte	0xb
	.long	0x1d1
	.uleb128 0x2
	.byte	0x65
	.byte	0xb
	.long	0x1de
	.uleb128 0x2
	.byte	0x67
	.byte	0xb
	.long	0x31d
	.uleb128 0x2
	.byte	0x68
	.byte	0xb
	.long	0x338
	.uleb128 0x2
	.byte	0x69
	.byte	0xb
	.long	0x351
	.uleb128 0x2
	.byte	0x6a
	.byte	0xb
	.long	0x368
	.uleb128 0x2
	.byte	0x6b
	.byte	0xb
	.long	0x381
	.uleb128 0x2
	.byte	0x6c
	.byte	0xb
	.long	0x39a
	.uleb128 0x2
	.byte	0x6d
	.byte	0xb
	.long	0x3b2
	.uleb128 0x2
	.byte	0x6e
	.byte	0xb
	.long	0x3d6
	.uleb128 0x2
	.byte	0x6f
	.byte	0xb
	.long	0x3f8
	.uleb128 0x2
	.byte	0x70
	.byte	0xb
	.long	0x41a
	.uleb128 0x2
	.byte	0x73
	.byte	0xb
	.long	0x449
	.uleb128 0x2
	.byte	0x74
	.byte	0xb
	.long	0x472
	.uleb128 0x2
	.byte	0x75
	.byte	0xb
	.long	0x496
	.uleb128 0x2
	.byte	0x76
	.byte	0xb
	.long	0x4c3
	.uleb128 0x2
	.byte	0x77
	.byte	0xb
	.long	0x4e5
	.uleb128 0x2
	.byte	0x78
	.byte	0xb
	.long	0x509
	.uleb128 0x2
	.byte	0x7a
	.byte	0xb
	.long	0x521
	.uleb128 0x2
	.byte	0x7b
	.byte	0xb
	.long	0x538
	.uleb128 0x2
	.byte	0x80
	.byte	0xb
	.long	0x548
	.uleb128 0x2
	.byte	0x81
	.byte	0xb
	.long	0x55c
	.uleb128 0x2
	.byte	0x85
	.byte	0xb
	.long	0x584
	.uleb128 0x2
	.byte	0x86
	.byte	0xb
	.long	0x59d
	.uleb128 0x2
	.byte	0x87
	.byte	0xb
	.long	0x5bb
	.uleb128 0x2
	.byte	0x88
	.byte	0xb
	.long	0x5cf
	.uleb128 0x2
	.byte	0x89
	.byte	0xb
	.long	0x5f5
	.uleb128 0x2
	.byte	0x8a
	.byte	0xb
	.long	0x60e
	.uleb128 0x2
	.byte	0x8b
	.byte	0xb
	.long	0x637
	.uleb128 0x2
	.byte	0x8c
	.byte	0xb
	.long	0x666
	.uleb128 0x2
	.byte	0x8d
	.byte	0xb
	.long	0x693
	.uleb128 0x2
	.byte	0x8f
	.byte	0xb
	.long	0x6a3
	.uleb128 0x2
	.byte	0x91
	.byte	0xb
	.long	0x6bc
	.uleb128 0x2
	.byte	0x92
	.byte	0xb
	.long	0x6da
	.uleb128 0x2
	.byte	0x93
	.byte	0xb
	.long	0x70f
	.uleb128 0x2
	.byte	0x94
	.byte	0xb
	.long	0x73d
	.uleb128 0x2
	.byte	0xbb
	.byte	0x16
	.long	0x7a9
	.uleb128 0x2
	.byte	0xbc
	.byte	0x16
	.long	0x7df
	.uleb128 0x2
	.byte	0xbd
	.byte	0x16
	.long	0x812
	.uleb128 0x2
	.byte	0xbe
	.byte	0x16
	.long	0x83e
	.uleb128 0x2
	.byte	0xbf
	.byte	0x16
	.long	0x87d
	.byte	0
	.uleb128 0xc
	.ascii "clearerr\0"
	.word	0x21e
	.long	0x333
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x5
	.long	0x1d1
	.uleb128 0x3
	.ascii "fclose\0"
	.word	0x21f
	.byte	0xf
	.long	0xeb
	.long	0x351
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x3
	.ascii "feof\0"
	.word	0x226
	.byte	0xf
	.long	0xeb
	.long	0x368
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x3
	.ascii "ferror\0"
	.word	0x227
	.byte	0xf
	.long	0xeb
	.long	0x381
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x3
	.ascii "fflush\0"
	.word	0x228
	.byte	0xf
	.long	0xeb
	.long	0x39a
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x3
	.ascii "fgetc\0"
	.word	0x229
	.byte	0xf
	.long	0xeb
	.long	0x3b2
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x3
	.ascii "fgetpos\0"
	.word	0x22b
	.byte	0xf
	.long	0xeb
	.long	0x3d1
	.uleb128 0x1
	.long	0x333
	.uleb128 0x1
	.long	0x3d1
	.byte	0
	.uleb128 0x5
	.long	0x1de
	.uleb128 0x3
	.ascii "fgets\0"
	.word	0x22d
	.byte	0x11
	.long	0x103
	.long	0x3f8
	.uleb128 0x1
	.long	0x103
	.uleb128 0x1
	.long	0xeb
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x3
	.ascii "fopen\0"
	.word	0x23b
	.byte	0x11
	.long	0x333
	.long	0x415
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x415
	.byte	0
	.uleb128 0x5
	.long	0x96
	.uleb128 0x4
	.ascii "fprintf\0"
	.word	0x15a
	.ascii "__mingw_fprintf\0"
	.long	0xeb
	.long	0x449
	.uleb128 0x1
	.long	0x333
	.uleb128 0x1
	.long	0x415
	.uleb128 0xa
	.byte	0
	.uleb128 0x3
	.ascii "fread\0"
	.word	0x240
	.byte	0x12
	.long	0x9b
	.long	0x470
	.uleb128 0x1
	.long	0x470
	.uleb128 0x1
	.long	0x9b
	.uleb128 0x1
	.long	0x9b
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x1d
	.byte	0x8
	.uleb128 0x3
	.ascii "freopen\0"
	.word	0x241
	.byte	0x11
	.long	0x333
	.long	0x496
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x4
	.ascii "fscanf\0"
	.word	0x13d
	.ascii "__mingw_fscanf\0"
	.long	0xeb
	.long	0x4c3
	.uleb128 0x1
	.long	0x333
	.uleb128 0x1
	.long	0x415
	.uleb128 0xa
	.byte	0
	.uleb128 0x3
	.ascii "fseek\0"
	.word	0x245
	.byte	0xf
	.long	0xeb
	.long	0x4e5
	.uleb128 0x1
	.long	0x333
	.uleb128 0x1
	.long	0xf7
	.uleb128 0x1
	.long	0xeb
	.byte	0
	.uleb128 0x3
	.ascii "fsetpos\0"
	.word	0x243
	.byte	0xf
	.long	0xeb
	.long	0x504
	.uleb128 0x1
	.long	0x333
	.uleb128 0x1
	.long	0x504
	.byte	0
	.uleb128 0x5
	.long	0x1ed
	.uleb128 0x3
	.ascii "ftell\0"
	.word	0x246
	.byte	0x10
	.long	0xf7
	.long	0x521
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x3
	.ascii "getc\0"
	.word	0x258
	.byte	0xf
	.long	0xeb
	.long	0x538
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x14
	.ascii "getchar\0"
	.word	0x259
	.byte	0xf
	.long	0xeb
	.uleb128 0xc
	.ascii "perror\0"
	.word	0x263
	.long	0x55c
	.uleb128 0x1
	.long	0x415
	.byte	0
	.uleb128 0x4
	.ascii "printf\0"
	.word	0x15e
	.ascii "__mingw_printf\0"
	.long	0xeb
	.long	0x584
	.uleb128 0x1
	.long	0x415
	.uleb128 0xa
	.byte	0
	.uleb128 0x3
	.ascii "remove\0"
	.word	0x273
	.byte	0xf
	.long	0xeb
	.long	0x59d
	.uleb128 0x1
	.long	0x415
	.byte	0
	.uleb128 0x3
	.ascii "rename\0"
	.word	0x274
	.byte	0xf
	.long	0xeb
	.long	0x5bb
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x415
	.byte	0
	.uleb128 0xc
	.ascii "rewind\0"
	.word	0x27a
	.long	0x5cf
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x4
	.ascii "scanf\0"
	.word	0x139
	.ascii "__mingw_scanf\0"
	.long	0xeb
	.long	0x5f5
	.uleb128 0x1
	.long	0x415
	.uleb128 0xa
	.byte	0
	.uleb128 0xc
	.ascii "setbuf\0"
	.word	0x27c
	.long	0x60e
	.uleb128 0x1
	.long	0x333
	.uleb128 0x1
	.long	0x103
	.byte	0
	.uleb128 0x3
	.ascii "setvbuf\0"
	.word	0x280
	.byte	0xf
	.long	0xeb
	.long	0x637
	.uleb128 0x1
	.long	0x333
	.uleb128 0x1
	.long	0x103
	.uleb128 0x1
	.long	0xeb
	.uleb128 0x1
	.long	0x9b
	.byte	0
	.uleb128 0x4
	.ascii "sprintf\0"
	.word	0x162
	.ascii "__mingw_sprintf\0"
	.long	0xeb
	.long	0x666
	.uleb128 0x1
	.long	0x103
	.uleb128 0x1
	.long	0x415
	.uleb128 0xa
	.byte	0
	.uleb128 0x4
	.ascii "sscanf\0"
	.word	0x135
	.ascii "__mingw_sscanf\0"
	.long	0xeb
	.long	0x693
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x415
	.uleb128 0xa
	.byte	0
	.uleb128 0x14
	.ascii "tmpfile\0"
	.word	0x291
	.byte	0x11
	.long	0x333
	.uleb128 0x3
	.ascii "tmpnam\0"
	.word	0x293
	.byte	0x11
	.long	0x103
	.long	0x6bc
	.uleb128 0x1
	.long	0x103
	.byte	0
	.uleb128 0x3
	.ascii "ungetc\0"
	.word	0x294
	.byte	0xf
	.long	0xeb
	.long	0x6da
	.uleb128 0x1
	.long	0xeb
	.uleb128 0x1
	.long	0x333
	.byte	0
	.uleb128 0x4
	.ascii "vfprintf\0"
	.word	0x177
	.ascii "__mingw_vfprintf\0"
	.long	0xeb
	.long	0x70f
	.uleb128 0x1
	.long	0x333
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x4
	.ascii "vprintf\0"
	.word	0x17b
	.ascii "__mingw_vprintf\0"
	.long	0xeb
	.long	0x73d
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x4
	.ascii "vsprintf\0"
	.word	0x180
	.ascii "_Z8vsprintfPcPKcS_\0"
	.long	0xeb
	.long	0x774
	.uleb128 0x1
	.long	0x103
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x13
	.ascii "__gnu_cxx\0"
	.word	0x175
	.long	0x7a9
	.uleb128 0x2
	.byte	0xb1
	.byte	0xb
	.long	0x7a9
	.uleb128 0x2
	.byte	0xb2
	.byte	0xb
	.long	0x7df
	.uleb128 0x2
	.byte	0xb3
	.byte	0xb
	.long	0x812
	.uleb128 0x2
	.byte	0xb4
	.byte	0xb
	.long	0x83e
	.uleb128 0x2
	.byte	0xb5
	.byte	0xb
	.long	0x87d
	.byte	0
	.uleb128 0x4
	.ascii "snprintf\0"
	.word	0x18f
	.ascii "__mingw_snprintf\0"
	.long	0xeb
	.long	0x7df
	.uleb128 0x1
	.long	0x103
	.uleb128 0x1
	.long	0x9b
	.uleb128 0x1
	.long	0x415
	.uleb128 0xa
	.byte	0
	.uleb128 0x4
	.ascii "vfscanf\0"
	.word	0x14f
	.ascii "__mingw_vfscanf\0"
	.long	0xeb
	.long	0x812
	.uleb128 0x1
	.long	0x333
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x4
	.ascii "vscanf\0"
	.word	0x14b
	.ascii "__mingw_vscanf\0"
	.long	0xeb
	.long	0x83e
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x4
	.ascii "vsnprintf\0"
	.word	0x1a0
	.ascii "_Z9vsnprintfPcyPKcS_\0"
	.long	0xeb
	.long	0x87d
	.uleb128 0x1
	.long	0x103
	.uleb128 0x1
	.long	0x9b
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x4
	.ascii "vsscanf\0"
	.word	0x147
	.ascii "__mingw_vsscanf\0"
	.long	0xeb
	.long	0x8b0
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x415
	.uleb128 0x1
	.long	0x77
	.byte	0
	.uleb128 0x12
	.ascii "FastStorage\0"
	.byte	0x1
	.byte	0x1
	.byte	0xd
	.byte	0x8
	.long	0x8f4
	.uleb128 0x1e
	.ascii "get\0"
	.byte	0x1
	.byte	0xd
	.byte	0x1a
	.ascii "_ZNK11FastStorage3getEv\0"
	.long	0xeb
	.long	0x8ed
	.uleb128 0x7
	.long	0x8f9
	.byte	0
	.byte	0
	.uleb128 0x8
	.long	0x8b0
	.uleb128 0x5
	.long	0x8f4
	.uleb128 0x8
	.long	0x8f9
	.uleb128 0x15
	.secrel32	.LASF2
	.byte	0x9
	.long	0xa0a
	.long	0xa05
	.uleb128 0x1f
	.long	0xa0a
	.byte	0
	.uleb128 0xb
	.secrel32	.LASF2
	.ascii "_ZN10MemStorageC4EOS_\0"
	.long	0x93a
	.long	0x945
	.uleb128 0x7
	.long	0xae8
	.uleb128 0x1
	.long	0xaf2
	.byte	0
	.uleb128 0xb
	.secrel32	.LASF2
	.ascii "_ZN10MemStorageC4ERKS_\0"
	.long	0x969
	.long	0x974
	.uleb128 0x7
	.long	0xae8
	.uleb128 0x1
	.long	0xaf8
	.byte	0
	.uleb128 0xb
	.secrel32	.LASF2
	.ascii "_ZN10MemStorageC4Ev\0"
	.long	0x995
	.long	0x99b
	.uleb128 0x7
	.long	0xae8
	.byte	0
	.uleb128 0x20
	.ascii "get\0"
	.byte	0x1
	.byte	0x9
	.byte	0x24
	.ascii "_ZNK10MemStorage3getEv\0"
	.long	0xeb
	.byte	0x1
	.uleb128 0x2
	.byte	0x10
	.uleb128 0x2
	.long	0x903
	.long	0x9ce
	.long	0x9d4
	.uleb128 0x7
	.long	0xafd
	.byte	0
	.uleb128 0x21
	.ascii "~MemStorage\0"
	.ascii "_ZN10MemStorageD4Ev\0"
	.byte	0x1
	.long	0x903
	.long	0x9fe
	.uleb128 0x7
	.long	0xae8
	.byte	0
	.byte	0
	.uleb128 0x8
	.long	0x903
	.uleb128 0x15
	.secrel32	.LASF3
	.byte	0x8
	.long	0xa0a
	.long	0xae3
	.uleb128 0xb
	.secrel32	.LASF3
	.ascii "_ZN8IStorageC4ERKS_\0"
	.long	0xa39
	.long	0xa44
	.uleb128 0x7
	.long	0xb07
	.uleb128 0x1
	.long	0xb11
	.byte	0
	.uleb128 0xb
	.secrel32	.LASF3
	.ascii "_ZN8IStorageC4Ev\0"
	.long	0xa62
	.long	0xa68
	.uleb128 0x7
	.long	0xb07
	.byte	0
	.uleb128 0x22
	.ascii "_vptr.IStorage\0"
	.long	0xb21
	.byte	0
	.uleb128 0x23
	.ascii "~IStorage\0"
	.byte	0x1
	.byte	0x8
	.byte	0x1b
	.ascii "_ZN8IStorageD4Ev\0"
	.byte	0x1
	.long	0xa0a
	.byte	0x1
	.long	0xaaa
	.long	0xab0
	.uleb128 0x7
	.long	0xb07
	.byte	0
	.uleb128 0x24
	.ascii "get\0"
	.byte	0x1
	.byte	0x8
	.byte	0x3e
	.ascii "_ZNK8IStorage3getEv\0"
	.long	0xeb
	.byte	0x1
	.uleb128 0x2
	.byte	0x10
	.uleb128 0x2
	.long	0xa0a
	.long	0xadc
	.uleb128 0x7
	.long	0xb3b
	.byte	0
	.byte	0
	.uleb128 0x8
	.long	0xa0a
	.uleb128 0x5
	.long	0x903
	.uleb128 0x8
	.long	0xae8
	.uleb128 0x25
	.byte	0x8
	.long	0x903
	.uleb128 0xf
	.long	0xa05
	.uleb128 0x5
	.long	0xa05
	.uleb128 0x8
	.long	0xafd
	.uleb128 0x5
	.long	0xa0a
	.uleb128 0x8
	.long	0xb07
	.uleb128 0xf
	.long	0xae3
	.uleb128 0x26
	.long	0xeb
	.long	0xb21
	.uleb128 0xa
	.byte	0
	.uleb128 0x5
	.long	0xb26
	.uleb128 0x11
	.ascii "__vtbl_ptr_type\0"
	.long	0xb16
	.uleb128 0x5
	.long	0xae3
	.uleb128 0x16
	.ascii "via_template<FastStorage>\0"
	.byte	0xf
	.ascii "_Z12via_templateI11FastStorageEiRKT_\0"
	.long	0xeb
	.quad	.LFB40
	.quad	.LFE40-.LFB40
	.uleb128 0x1
	.byte	0x9c
	.long	0xbaf
	.uleb128 0x27
	.ascii "S\0"
	.long	0x8b0
	.uleb128 0x17
	.ascii "s\0"
	.byte	0xf
	.byte	0x1b
	.long	0xbaf
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0xf
	.long	0x8f4
	.uleb128 0x28
	.ascii "main\0"
	.byte	0x1
	.byte	0x11
	.byte	0x5
	.long	0xeb
	.quad	.LFB25
	.quad	.LFE25-.LFB25
	.uleb128 0x1
	.byte	0x9c
	.long	0xc0a
	.uleb128 0xd
	.ascii "ms\0"
	.byte	0x12
	.byte	0x10
	.long	0x903
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.uleb128 0xd
	.ascii "fs\0"
	.byte	0x13
	.byte	0x11
	.long	0x8b0
	.uleb128 0x2
	.byte	0x91
	.sleb128 -41
	.uleb128 0xd
	.ascii "a\0"
	.byte	0x14
	.byte	0x12
	.long	0xf2
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.uleb128 0xd
	.ascii "b\0"
	.byte	0x15
	.byte	0x12
	.long	0xf2
	.uleb128 0x2
	.byte	0x91
	.sleb128 -52
	.byte	0
	.uleb128 0x29
	.long	0x9d4
	.byte	0x1
	.byte	0x9
	.byte	0x8
	.long	0xc1b
	.byte	0x2
	.long	0xc26
	.uleb128 0x18
	.ascii "this\0"
	.long	0xaed
	.byte	0
	.uleb128 0x19
	.long	0xc0a
	.ascii "_ZN10MemStorageD0Ev\0"
	.long	0xc59
	.quad	.LFB39
	.quad	.LFE39-.LFB39
	.uleb128 0x1
	.byte	0x9c
	.long	0xc62
	.uleb128 0x10
	.long	0xc1b
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x19
	.long	0xc0a
	.ascii "_ZN10MemStorageD1Ev\0"
	.long	0xc95
	.quad	.LFB38
	.quad	.LFE38-.LFB38
	.uleb128 0x1
	.byte	0x9c
	.long	0xc9e
	.uleb128 0x10
	.long	0xc1b
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x2a
	.long	0xa7d
	.long	0xcac
	.byte	0x2
	.long	0xcb7
	.uleb128 0x18
	.ascii "this\0"
	.long	0xb0c
	.byte	0
	.uleb128 0x2b
	.long	0xc9e
	.ascii "_ZN8IStorageD2Ev\0"
	.long	0xce7
	.quad	.LFB31
	.quad	.LFE31-.LFB31
	.uleb128 0x1
	.byte	0x9c
	.long	0xcf0
	.uleb128 0x10
	.long	0xcac
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x2c
	.long	0x8c5
	.long	0xd0f
	.quad	.LFB23
	.quad	.LFE23-.LFB23
	.uleb128 0x1
	.byte	0x9c
	.long	0xd1d
	.uleb128 0x1a
	.ascii "this\0"
	.long	0x8fe
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x16
	.ascii "via_virtual\0"
	.byte	0xa
	.ascii "_Z11via_virtualRK8IStorage\0"
	.long	0xeb
	.quad	.LFB22
	.quad	.LFE22-.LFB22
	.uleb128 0x1
	.byte	0x9c
	.long	0xd6d
	.uleb128 0x17
	.ascii "s\0"
	.byte	0xa
	.byte	0x21
	.long	0xb11
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x2d
	.long	0x99b
	.long	0xd88
	.quad	.LFB21
	.quad	.LFE21-.LFB21
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x1a
	.ascii "this\0"
	.long	0xb02
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.byte	0
	.section	.debug_abbrev,"dr"
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0x8
	.byte	0
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 4
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x18
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 5
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x8
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0xa
	.uleb128 0x18
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0xb
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xc
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 16
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xd
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0xe
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xf
	.uleb128 0x10
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x10
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x11
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x12
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x13
	.uleb128 0x39
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 5
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x14
	.uleb128 0x2e
	.byte	0
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x15
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x16
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 5
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x17
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x18
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x19
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1a
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x1b
	.uleb128 0x11
	.byte	0x1
	.uleb128 0x25
	.uleb128 0x8
	.uleb128 0x13
	.uleb128 0xb
	.uleb128 0x90
	.uleb128 0xb
	.uleb128 0x91
	.uleb128 0x6
	.uleb128 0x3
	.uleb128 0x1f
	.uleb128 0x1b
	.uleb128 0x1f
	.uleb128 0x55
	.uleb128 0x17
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x10
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x1c
	.uleb128 0x35
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1d
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x1e
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1f
	.uleb128 0x1c
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x20
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x4c
	.uleb128 0xb
	.uleb128 0x4d
	.uleb128 0x18
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x21
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x4c
	.uleb128 0xb
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x22
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x23
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x4c
	.uleb128 0xb
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x8b
	.uleb128 0xb
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x24
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x4c
	.uleb128 0xb
	.uleb128 0x4d
	.uleb128 0x18
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x25
	.uleb128 0x42
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x26
	.uleb128 0x15
	.byte	0x1
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x27
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x28
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x29
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x20
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2a
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x20
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2b
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7a
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2c
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7a
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2d
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7a
	.uleb128 0x19
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"dr"
	.long	0x8c
	.word	0x2
	.secrel32	.Ldebug_info0
	.byte	0x8
	.byte	0
	.word	0
	.word	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	.LFB21
	.quad	.LFE21-.LFB21
	.quad	.LFB23
	.quad	.LFE23-.LFB23
	.quad	.LFB31
	.quad	.LFE31-.LFB31
	.quad	.LFB38
	.quad	.LFE38-.LFB38
	.quad	.LFB39
	.quad	.LFE39-.LFB39
	.quad	.LFB40
	.quad	.LFE40-.LFB40
	.quad	0
	.quad	0
	.section	.debug_rnglists,"dr"
.Ldebug_ranges0:
	.long	.Ldebug_ranges3-.Ldebug_ranges2
.Ldebug_ranges2:
	.word	0x5
	.byte	0x8
	.byte	0
	.long	0
.LLRL0:
	.byte	0x7
	.quad	.Ltext0
	.uleb128 .Letext0-.Ltext0
	.byte	0x7
	.quad	.LFB21
	.uleb128 .LFE21-.LFB21
	.byte	0x7
	.quad	.LFB23
	.uleb128 .LFE23-.LFB23
	.byte	0x7
	.quad	.LFB31
	.uleb128 .LFE31-.LFB31
	.byte	0x7
	.quad	.LFB38
	.uleb128 .LFE38-.LFB38
	.byte	0x7
	.quad	.LFB39
	.uleb128 .LFE39-.LFB39
	.byte	0x7
	.quad	.LFB40
	.uleb128 .LFE40-.LFB40
	.byte	0
.Ldebug_ranges3:
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
.LASF2:
	.ascii "MemStorage\0"
.LASF3:
	.ascii "IStorage\0"
	.section	.debug_line_str,"dr"
.LASF1:
	.ascii "C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible\0"
.LASF0:
	.ascii "Examples\\_ch141_perf.cpp\0"
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__cxa_pure_virtual;	.scl	2;	.type	32;	.endef
