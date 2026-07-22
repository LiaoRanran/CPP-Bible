	.file	"_ch140_smart_ptr_policy.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch140_smart_ptr_policy.cpp"
	.section	.text$_ZN11MallocAlloc5allocEy,"x"
	.linkonce discard
	.globl	_ZN11MallocAlloc5allocEy
	.def	_ZN11MallocAlloc5allocEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN11MallocAlloc5allocEy
_ZN11MallocAlloc5allocEy:
.LFB53:
	.file 1 "Examples/_ch140_smart_ptr_policy.cpp"
	.loc 1 5 18
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
	.loc 1 5 59
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	malloc
	.loc 1 5 64
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE53:
	.seh_endproc
	.section	.text$_ZN11MallocAlloc7deallocEPv,"x"
	.linkonce discard
	.globl	_ZN11MallocAlloc7deallocEPv
	.def	_ZN11MallocAlloc7deallocEPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN11MallocAlloc7deallocEPv
_ZN11MallocAlloc7deallocEPv:
.LFB54:
	.loc 1 6 18
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
	.loc 1 6 46
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	free
	.loc 1 6 51
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE54:
	.seh_endproc
	.section	.text$_ZN8NewAlloc5allocEy,"x"
	.linkonce discard
	.globl	_ZN8NewAlloc5allocEy
	.def	_ZN8NewAlloc5allocEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN8NewAlloc5allocEy
_ZN8NewAlloc5allocEy:
.LFB55:
	.loc 1 9 18
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
	.loc 1 9 62
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_Znwy
	.loc 1 9 67
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE55:
	.seh_endproc
	.section	.text$_ZN8NewAlloc7deallocEPv,"x"
	.linkonce discard
	.globl	_ZN8NewAlloc7deallocEPv
	.def	_ZN8NewAlloc7deallocEPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN8NewAlloc7deallocEPv
_ZN8NewAlloc7deallocEPv:
.LFB56:
	.loc 1 10 18
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
	.loc 1 10 54
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZdlPv
	.loc 1 10 59
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE56:
	.seh_endproc
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB60:
	.loc 1 25 12
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	sub	rsp, 88
	.seh_stackalloc	88
	.cfi_def_cfa_offset 112
	lea	rbp, 80[rsp]
	.seh_setframe	rbp, 80
	.cfi_def_cfa 6, 32
	.seh_endprologue
	.loc 1 25 12
	call	__main
	.loc 1 26 33
	mov	QWORD PTR -32[rbp], 0
	mov	QWORD PTR -24[rbp], 0
	.loc 1 27 30
	mov	QWORD PTR -48[rbp], 0
	mov	QWORD PTR -40[rbp], 0
	.loc 1 28 17
	mov	DWORD PTR -8[rbp], 1
	.loc 1 28 16
	lea	rdx, -8[rbp]
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZN9PodVectorIi11MallocAllocE9push_backERKi
	.loc 1 28 33 discriminator 1
	mov	DWORD PTR -4[rbp], 2
	.loc 1 28 32 discriminator 1
	lea	rdx, -4[rbp]
	lea	rax, -48[rbp]
	mov	rcx, rax
.LEHB0:
	call	_ZN9PodVectorIi8NewAllocE9push_backERKi
.LEHE0:
	.loc 1 29 23
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZNK9PodVectorIi11MallocAllocE4sizeEv
	.loc 1 29 26 discriminator 1
	mov	ebx, eax
	.loc 1 29 39 discriminator 1
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZNK9PodVectorIi8NewAllocE4sizeEv
	.loc 1 29 40 discriminator 2
	add	ebx, eax
	.loc 1 30 1
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZN9PodVectorIi8NewAllocED1Ev
	.loc 1 30 1 is_stmt 0 discriminator 2
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZN9PodVectorIi11MallocAllocED1Ev
	.loc 1 30 1
	mov	eax, ebx
	jmp	.L11
.L10:
	mov	rbx, rax
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZN9PodVectorIi8NewAllocED1Ev
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZN9PodVectorIi11MallocAllocED1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB1:
	call	_Unwind_Resume
.LEHE1:
.L11:
	add	rsp, 88
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -72
	ret
	.cfi_endproc
.LFE60:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA60:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE60-.LLSDACSB60
.LLSDACSB60:
	.uleb128 .LEHB0-.LFB60
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L10-.LFB60
	.uleb128 0
	.uleb128 .LEHB1-.LFB60
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE60:
	.text
	.seh_endproc
	.section	.text$_ZN9PodVectorIi11MallocAllocED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9PodVectorIi11MallocAllocED1Ev
	.def	_ZN9PodVectorIi11MallocAllocED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9PodVectorIi11MallocAllocED1Ev
_ZN9PodVectorIi11MallocAllocED1Ev:
.LFB69:
	.loc 1 22 5 is_stmt 1
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
.LBB2:
	.loc 1 22 24
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 1 22 20
	test	rax, rax
	je	.L14
	.loc 1 22 51 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 1 22 50 discriminator 1
	mov	rcx, rax
	call	_ZN11MallocAlloc7deallocEPv
.L14:
.LBE2:
	.loc 1 22 58
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE69:
	.seh_endproc
	.section	.text$_ZN9PodVectorIi8NewAllocED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9PodVectorIi8NewAllocED1Ev
	.def	_ZN9PodVectorIi8NewAllocED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9PodVectorIi8NewAllocED1Ev
_ZN9PodVectorIi8NewAllocED1Ev:
.LFB72:
	.loc 1 22 5
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
	.loc 1 22 24
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 1 22 20
	test	rax, rax
	je	.L17
	.loc 1 22 51 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 1 22 50 discriminator 1
	mov	rcx, rax
	call	_ZN8NewAlloc7deallocEPv
.L17:
.LBE3:
	.loc 1 22 58
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE72:
	.seh_endproc
	.section	.text$_ZN9PodVectorIi11MallocAllocE9push_backERKi,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9PodVectorIi11MallocAllocE9push_backERKi
	.def	_ZN9PodVectorIi11MallocAllocE9push_backERKi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9PodVectorIi11MallocAllocE9push_backERKi
_ZN9PodVectorIi11MallocAllocE9push_backERKi:
.LFB73:
	.loc 1 17 10
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
	mov	QWORD PTR 24[rbp], rdx
	.loc 1 18 52
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	.loc 1 18 54
	add	rax, 1
	.loc 1 18 50
	sal	rax, 2
	mov	rcx, rax
	call	_ZN11MallocAlloc5allocEy
	.loc 1 18 14 discriminator 1
	mov	rdx, QWORD PTR 16[rbp]
	mov	QWORD PTR [rdx], rax
	.loc 1 19 19
	mov	rax, QWORD PTR 24[rbp]
	mov	edx, DWORD PTR [rax]
	.loc 1 19 9
	mov	rax, QWORD PTR 16[rbp]
	mov	r9, QWORD PTR [rax]
	.loc 1 19 14
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	.loc 1 19 13
	lea	r8, 1[rax]
	mov	rcx, QWORD PTR 16[rbp]
	mov	QWORD PTR 8[rcx], r8
	sal	rax, 2
	add	rax, r9
	.loc 1 19 19
	mov	DWORD PTR [rax], edx
	.loc 1 20 5
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE73:
	.seh_endproc
	.section	.text$_ZN9PodVectorIi8NewAllocE9push_backERKi,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9PodVectorIi8NewAllocE9push_backERKi
	.def	_ZN9PodVectorIi8NewAllocE9push_backERKi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9PodVectorIi8NewAllocE9push_backERKi
_ZN9PodVectorIi8NewAllocE9push_backERKi:
.LFB74:
	.loc 1 17 10
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
	mov	QWORD PTR 24[rbp], rdx
	.loc 1 18 52
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	.loc 1 18 54
	add	rax, 1
	.loc 1 18 50
	sal	rax, 2
	mov	rcx, rax
	call	_ZN8NewAlloc5allocEy
	.loc 1 18 14 discriminator 1
	mov	rdx, QWORD PTR 16[rbp]
	mov	QWORD PTR [rdx], rax
	.loc 1 19 19
	mov	rax, QWORD PTR 24[rbp]
	mov	edx, DWORD PTR [rax]
	.loc 1 19 9
	mov	rax, QWORD PTR 16[rbp]
	mov	r9, QWORD PTR [rax]
	.loc 1 19 14
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	.loc 1 19 13
	lea	r8, 1[rax]
	mov	rcx, QWORD PTR 16[rbp]
	mov	QWORD PTR 8[rcx], r8
	sal	rax, 2
	add	rax, r9
	.loc 1 19 19
	mov	DWORD PTR [rax], edx
	.loc 1 20 5
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE74:
	.seh_endproc
	.section	.text$_ZNK9PodVectorIi11MallocAllocE4sizeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK9PodVectorIi11MallocAllocE4sizeEv
	.def	_ZNK9PodVectorIi11MallocAllocE4sizeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK9PodVectorIi11MallocAllocE4sizeEv
_ZNK9PodVectorIi11MallocAllocE4sizeEv:
.LFB75:
	.loc 1 21 17
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
	.loc 1 21 39
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	.loc 1 21 42
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE75:
	.seh_endproc
	.section	.text$_ZNK9PodVectorIi8NewAllocE4sizeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK9PodVectorIi8NewAllocE4sizeEv
	.def	_ZNK9PodVectorIi8NewAllocE4sizeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK9PodVectorIi8NewAllocE4sizeEv
_ZNK9PodVectorIi8NewAllocE4sizeEv:
.LFB76:
	.loc 1 21 17
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
	.loc 1 21 39
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	.loc 1 21 42
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE76:
	.seh_endproc
	.text
.Letext0:
	.file 2 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/stddef.h"
	.file 3 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/cstddef"
	.file 4 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/cstdlib"
	.file 5 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/corecrt.h"
	.file 6 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/x86_64-w64-mingw32/bits/c++config.h"
	.file 7 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/stdlib.h"
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0xd16
	.word	0x5
	.byte	0x1
	.byte	0x8
	.secrel32	.Ldebug_abbrev0
	.uleb128 0x23
	.ascii "GNU C++23 15.3.0 -masm=intel -mtune=generic -march=x86-64 -g -O0 -std=c++23\0"
	.byte	0x21
	.byte	0x4
	.long	0x3163e
	.secrel32	.LASF0
	.secrel32	.LASF1
	.secrel32	.LLRL0
	.quad	0
	.secrel32	.Ldebug_line0
	.uleb128 0x4
	.byte	0x1
	.byte	0x6
	.ascii "char\0"
	.uleb128 0x6
	.long	0x77
	.uleb128 0xe
	.ascii "size_t\0"
	.byte	0x5
	.byte	0x23
	.byte	0x2c
	.long	0x93
	.uleb128 0x4
	.byte	0x8
	.byte	0x7
	.ascii "long long unsigned int\0"
	.uleb128 0x4
	.byte	0x8
	.byte	0x5
	.ascii "long long int\0"
	.uleb128 0x4
	.byte	0x2
	.byte	0x7
	.ascii "short unsigned int\0"
	.uleb128 0x4
	.byte	0x4
	.byte	0x5
	.ascii "int\0"
	.uleb128 0x6
	.long	0xd4
	.uleb128 0x4
	.byte	0x4
	.byte	0x5
	.ascii "long int\0"
	.uleb128 0x5
	.long	0x77
	.uleb128 0x5
	.long	0xf6
	.uleb128 0x4
	.byte	0x2
	.byte	0x7
	.ascii "wchar_t\0"
	.uleb128 0x6
	.long	0xf6
	.uleb128 0x5
	.long	0xd4
	.uleb128 0x4
	.byte	0x4
	.byte	0x7
	.ascii "unsigned int\0"
	.uleb128 0x4
	.byte	0x4
	.byte	0x7
	.ascii "long unsigned int\0"
	.uleb128 0x4
	.byte	0x1
	.byte	0x8
	.ascii "unsigned char\0"
	.uleb128 0x24
	.byte	0x20
	.byte	0x10
	.byte	0x2
	.word	0x1a8
	.byte	0x10
	.ascii "11max_align_t\0"
	.long	0x18d
	.uleb128 0x10
	.ascii "__max_align_ll\0"
	.word	0x1a9
	.byte	0xd
	.long	0xad
	.byte	0x8
	.byte	0
	.uleb128 0x10
	.ascii "__max_align_ld\0"
	.word	0x1aa
	.byte	0xf
	.long	0x18d
	.byte	0x10
	.byte	0x10
	.byte	0
	.uleb128 0x4
	.byte	0x10
	.byte	0x4
	.ascii "long double\0"
	.uleb128 0x25
	.ascii "max_align_t\0"
	.byte	0x2
	.word	0x1ab
	.byte	0x3
	.long	0x141
	.byte	0x10
	.uleb128 0x11
	.ascii "std\0"
	.word	0x150
	.long	0x2bf
	.uleb128 0x2
	.byte	0x3
	.byte	0x42
	.byte	0xb
	.long	0x19c
	.uleb128 0x2
	.byte	0x4
	.byte	0x89
	.byte	0xb
	.long	0x2eb
	.uleb128 0x2
	.byte	0x4
	.byte	0x8a
	.byte	0xb
	.long	0x326
	.uleb128 0x2
	.byte	0x4
	.byte	0x90
	.byte	0xb
	.long	0x38f
	.uleb128 0x2
	.byte	0x4
	.byte	0x96
	.byte	0xb
	.long	0x3a8
	.uleb128 0x2
	.byte	0x4
	.byte	0x97
	.byte	0xb
	.long	0x3c4
	.uleb128 0x2
	.byte	0x4
	.byte	0x98
	.byte	0xb
	.long	0x3db
	.uleb128 0x2
	.byte	0x4
	.byte	0x99
	.byte	0xb
	.long	0x3f2
	.uleb128 0x2
	.byte	0x4
	.byte	0x9b
	.byte	0xb
	.long	0x441
	.uleb128 0x2
	.byte	0x4
	.byte	0x9e
	.byte	0xb
	.long	0x45c
	.uleb128 0x2
	.byte	0x4
	.byte	0xa0
	.byte	0xb
	.long	0x475
	.uleb128 0x2
	.byte	0x4
	.byte	0xa3
	.byte	0xb
	.long	0x491
	.uleb128 0x2
	.byte	0x4
	.byte	0xa4
	.byte	0xb
	.long	0x4ae
	.uleb128 0x2
	.byte	0x4
	.byte	0xa5
	.byte	0xb
	.long	0x4d3
	.uleb128 0x2
	.byte	0x4
	.byte	0xa7
	.byte	0xb
	.long	0x4f6
	.uleb128 0x2
	.byte	0x4
	.byte	0xad
	.byte	0xb
	.long	0x518
	.uleb128 0x2
	.byte	0x4
	.byte	0xaf
	.byte	0xb
	.long	0x526
	.uleb128 0x2
	.byte	0x4
	.byte	0xb0
	.byte	0xb
	.long	0x539
	.uleb128 0x2
	.byte	0x4
	.byte	0xb1
	.byte	0xb
	.long	0x55c
	.uleb128 0x2
	.byte	0x4
	.byte	0xb2
	.byte	0xb
	.long	0x57f
	.uleb128 0x2
	.byte	0x4
	.byte	0xb3
	.byte	0xb
	.long	0x5a3
	.uleb128 0x2
	.byte	0x4
	.byte	0xb5
	.byte	0xb
	.long	0x5bc
	.uleb128 0x2
	.byte	0x4
	.byte	0xb6
	.byte	0xb
	.long	0x5e1
	.uleb128 0x2
	.byte	0x4
	.byte	0xfd
	.byte	0x16
	.long	0x37e
	.uleb128 0x8
	.word	0x102
	.long	0x648
	.uleb128 0x8
	.word	0x103
	.long	0x675
	.uleb128 0x8
	.word	0x105
	.long	0x692
	.uleb128 0x8
	.word	0x106
	.long	0x6f3
	.uleb128 0x8
	.word	0x107
	.long	0x6aa
	.uleb128 0x8
	.word	0x108
	.long	0x6ce
	.uleb128 0x8
	.word	0x109
	.long	0x711
	.uleb128 0x12
	.ascii "size_t\0"
	.byte	0x6
	.word	0x152
	.byte	0x1a
	.long	0x93
	.byte	0
	.uleb128 0xb
	.ascii "_div_t\0"
	.byte	0x8
	.byte	0x7
	.byte	0x3c
	.byte	0x12
	.long	0x2eb
	.uleb128 0x7
	.ascii "quot\0"
	.byte	0x7
	.byte	0x3d
	.byte	0x9
	.long	0xd4
	.byte	0
	.uleb128 0x7
	.ascii "rem\0"
	.byte	0x7
	.byte	0x3e
	.byte	0x9
	.long	0xd4
	.byte	0x4
	.byte	0
	.uleb128 0xe
	.ascii "div_t\0"
	.byte	0x7
	.byte	0x3f
	.byte	0x5
	.long	0x2bf
	.uleb128 0xb
	.ascii "_ldiv_t\0"
	.byte	0x8
	.byte	0x7
	.byte	0x41
	.byte	0x12
	.long	0x326
	.uleb128 0x7
	.ascii "quot\0"
	.byte	0x7
	.byte	0x42
	.byte	0xa
	.long	0xe0
	.byte	0
	.uleb128 0x7
	.ascii "rem\0"
	.byte	0x7
	.byte	0x43
	.byte	0xa
	.long	0xe0
	.byte	0x4
	.byte	0
	.uleb128 0xe
	.ascii "ldiv_t\0"
	.byte	0x7
	.byte	0x44
	.byte	0x5
	.long	0x2f9
	.uleb128 0x4
	.byte	0x8
	.byte	0x4
	.ascii "double\0"
	.uleb128 0x4
	.byte	0x4
	.byte	0x4
	.ascii "float\0"
	.uleb128 0x5
	.long	0x34d
	.uleb128 0x26
	.uleb128 0x5
	.long	0x101
	.uleb128 0x27
	.byte	0x10
	.byte	0x7
	.word	0x2ab
	.byte	0x12
	.ascii "7lldiv_t\0"
	.long	0x37e
	.uleb128 0x13
	.ascii "quot\0"
	.byte	0x30
	.long	0xad
	.byte	0
	.uleb128 0x13
	.ascii "rem\0"
	.byte	0x36
	.long	0xad
	.byte	0x8
	.byte	0
	.uleb128 0x12
	.ascii "lldiv_t\0"
	.byte	0x7
	.word	0x2ab
	.byte	0x3d
	.long	0x353
	.uleb128 0x3
	.ascii "atexit\0"
	.word	0x137
	.byte	0xf
	.long	0xd4
	.long	0x3a8
	.uleb128 0x1
	.long	0x348
	.byte	0
	.uleb128 0x3
	.ascii "atof\0"
	.word	0x13d
	.byte	0x12
	.long	0x335
	.long	0x3bf
	.uleb128 0x1
	.long	0x3bf
	.byte	0
	.uleb128 0x5
	.long	0x7f
	.uleb128 0x3
	.ascii "atoi\0"
	.word	0x140
	.byte	0xf
	.long	0xd4
	.long	0x3db
	.uleb128 0x1
	.long	0x3bf
	.byte	0
	.uleb128 0x3
	.ascii "atol\0"
	.word	0x142
	.byte	0x10
	.long	0xe0
	.long	0x3f2
	.uleb128 0x1
	.long	0x3bf
	.byte	0
	.uleb128 0x3
	.ascii "bsearch\0"
	.word	0x146
	.byte	0x11
	.long	0x420
	.long	0x420
	.uleb128 0x1
	.long	0x422
	.uleb128 0x1
	.long	0x422
	.uleb128 0x1
	.long	0x84
	.uleb128 0x1
	.long	0x84
	.uleb128 0x1
	.long	0x428
	.byte	0
	.uleb128 0x28
	.byte	0x8
	.uleb128 0x5
	.long	0x427
	.uleb128 0x29
	.uleb128 0x5
	.long	0x42d
	.uleb128 0x2a
	.long	0xd4
	.long	0x441
	.uleb128 0x1
	.long	0x422
	.uleb128 0x1
	.long	0x422
	.byte	0
	.uleb128 0x3
	.ascii "div\0"
	.word	0x14c
	.byte	0x11
	.long	0x2eb
	.long	0x45c
	.uleb128 0x1
	.long	0xd4
	.uleb128 0x1
	.long	0xd4
	.byte	0
	.uleb128 0x3
	.ascii "getenv\0"
	.word	0x14d
	.byte	0x11
	.long	0xec
	.long	0x475
	.uleb128 0x1
	.long	0x3bf
	.byte	0
	.uleb128 0x3
	.ascii "ldiv\0"
	.word	0x157
	.byte	0x12
	.long	0x326
	.long	0x491
	.uleb128 0x1
	.long	0xe0
	.uleb128 0x1
	.long	0xe0
	.byte	0
	.uleb128 0x3
	.ascii "mblen\0"
	.word	0x159
	.byte	0x17
	.long	0xd4
	.long	0x4ae
	.uleb128 0x1
	.long	0x3bf
	.uleb128 0x1
	.long	0x84
	.byte	0
	.uleb128 0x3
	.ascii "mbstowcs\0"
	.word	0x163
	.byte	0x1a
	.long	0x84
	.long	0x4d3
	.uleb128 0x1
	.long	0xf1
	.uleb128 0x1
	.long	0x3bf
	.uleb128 0x1
	.long	0x84
	.byte	0
	.uleb128 0x3
	.ascii "mbtowc\0"
	.word	0x161
	.byte	0x17
	.long	0xd4
	.long	0x4f6
	.uleb128 0x1
	.long	0xf1
	.uleb128 0x1
	.long	0x3bf
	.uleb128 0x1
	.long	0x84
	.byte	0
	.uleb128 0xf
	.ascii "qsort\0"
	.word	0x147
	.long	0x518
	.uleb128 0x1
	.long	0x420
	.uleb128 0x1
	.long	0x84
	.uleb128 0x1
	.long	0x84
	.uleb128 0x1
	.long	0x428
	.byte	0
	.uleb128 0x2b
	.ascii "rand\0"
	.byte	0x7
	.word	0x167
	.byte	0xf
	.long	0xd4
	.uleb128 0xf
	.ascii "srand\0"
	.word	0x169
	.long	0x539
	.uleb128 0x1
	.long	0x10b
	.byte	0
	.uleb128 0x3
	.ascii "strtod\0"
	.word	0x175
	.byte	0x20
	.long	0x335
	.long	0x557
	.uleb128 0x1
	.long	0x3bf
	.uleb128 0x1
	.long	0x557
	.byte	0
	.uleb128 0x5
	.long	0xec
	.uleb128 0x3
	.ascii "strtol\0"
	.word	0x199
	.byte	0x10
	.long	0xe0
	.long	0x57f
	.uleb128 0x1
	.long	0x3bf
	.uleb128 0x1
	.long	0x557
	.uleb128 0x1
	.long	0xd4
	.byte	0
	.uleb128 0x3
	.ascii "strtoul\0"
	.word	0x19b
	.byte	0x19
	.long	0x11b
	.long	0x5a3
	.uleb128 0x1
	.long	0x3bf
	.uleb128 0x1
	.long	0x557
	.uleb128 0x1
	.long	0xd4
	.byte	0
	.uleb128 0x3
	.ascii "system\0"
	.word	0x19f
	.byte	0xf
	.long	0xd4
	.long	0x5bc
	.uleb128 0x1
	.long	0x3bf
	.byte	0
	.uleb128 0x3
	.ascii "wcstombs\0"
	.word	0x1a4
	.byte	0x1a
	.long	0x84
	.long	0x5e1
	.uleb128 0x1
	.long	0xec
	.uleb128 0x1
	.long	0x34e
	.uleb128 0x1
	.long	0x84
	.byte	0
	.uleb128 0x3
	.ascii "wctomb\0"
	.word	0x1a2
	.byte	0x17
	.long	0xd4
	.long	0x5ff
	.uleb128 0x1
	.long	0xec
	.uleb128 0x1
	.long	0xf6
	.byte	0
	.uleb128 0x11
	.ascii "__gnu_cxx\0"
	.word	0x175
	.long	0x675
	.uleb128 0x2
	.byte	0x4
	.byte	0xd2
	.byte	0xb
	.long	0x37e
	.uleb128 0x2
	.byte	0x4
	.byte	0xe4
	.byte	0xb
	.long	0x675
	.uleb128 0x2
	.byte	0x4
	.byte	0xf0
	.byte	0xb
	.long	0x692
	.uleb128 0x2
	.byte	0x4
	.byte	0xf1
	.byte	0xb
	.long	0x6aa
	.uleb128 0x2
	.byte	0x4
	.byte	0xf2
	.byte	0xb
	.long	0x6ce
	.uleb128 0x2
	.byte	0x4
	.byte	0xf4
	.byte	0xb
	.long	0x6f3
	.uleb128 0x2
	.byte	0x4
	.byte	0xf5
	.byte	0xb
	.long	0x711
	.uleb128 0x2c
	.ascii "div\0"
	.byte	0x4
	.byte	0xe1
	.byte	0x3
	.ascii "_ZN9__gnu_cxx3divExx\0"
	.long	0x37e
	.uleb128 0x1
	.long	0xad
	.uleb128 0x1
	.long	0xad
	.byte	0
	.byte	0
	.uleb128 0x3
	.ascii "lldiv\0"
	.word	0x2ad
	.byte	0x25
	.long	0x37e
	.long	0x692
	.uleb128 0x1
	.long	0xad
	.uleb128 0x1
	.long	0xad
	.byte	0
	.uleb128 0x3
	.ascii "atoll\0"
	.word	0x2b8
	.byte	0x28
	.long	0xad
	.long	0x6aa
	.uleb128 0x1
	.long	0x3bf
	.byte	0
	.uleb128 0x3
	.ascii "strtoll\0"
	.word	0x2b4
	.byte	0x28
	.long	0xad
	.long	0x6ce
	.uleb128 0x1
	.long	0x3bf
	.uleb128 0x1
	.long	0x557
	.uleb128 0x1
	.long	0xd4
	.byte	0
	.uleb128 0x3
	.ascii "strtoull\0"
	.word	0x2b5
	.byte	0x31
	.long	0x93
	.long	0x6f3
	.uleb128 0x1
	.long	0x3bf
	.uleb128 0x1
	.long	0x557
	.uleb128 0x1
	.long	0xd4
	.byte	0
	.uleb128 0x3
	.ascii "strtof\0"
	.word	0x17c
	.byte	0x1f
	.long	0x33f
	.long	0x711
	.uleb128 0x1
	.long	0x3bf
	.uleb128 0x1
	.long	0x557
	.byte	0
	.uleb128 0x3
	.ascii "strtold\0"
	.word	0x187
	.byte	0x27
	.long	0x18d
	.long	0x730
	.uleb128 0x1
	.long	0x3bf
	.uleb128 0x1
	.long	0x557
	.byte	0
	.uleb128 0xb
	.ascii "MallocAlloc\0"
	.byte	0x1
	.byte	0x1
	.byte	0x4
	.byte	0x8
	.long	0x7a1
	.uleb128 0x14
	.ascii "alloc\0"
	.byte	0x5
	.ascii "_ZN11MallocAlloc5allocEy\0"
	.long	0x420
	.long	0x774
	.uleb128 0x1
	.long	0x2ae
	.byte	0
	.uleb128 0x15
	.ascii "dealloc\0"
	.byte	0x6
	.ascii "_ZN11MallocAlloc7deallocEPv\0"
	.uleb128 0x1
	.long	0x420
	.byte	0
	.byte	0
	.uleb128 0xb
	.ascii "NewAlloc\0"
	.byte	0x1
	.byte	0x1
	.byte	0x8
	.byte	0x8
	.long	0x807
	.uleb128 0x14
	.ascii "alloc\0"
	.byte	0x9
	.ascii "_ZN8NewAlloc5allocEy\0"
	.long	0x420
	.long	0x7de
	.uleb128 0x1
	.long	0x2ae
	.byte	0
	.uleb128 0x15
	.ascii "dealloc\0"
	.byte	0xa
	.ascii "_ZN8NewAlloc7deallocEPv\0"
	.uleb128 0x1
	.long	0x420
	.byte	0
	.byte	0
	.uleb128 0x16
	.ascii "PodVector<int, MallocAlloc>\0"
	.long	0x90d
	.uleb128 0x7
	.ascii "data\0"
	.byte	0x1
	.byte	0xf
	.byte	0x8
	.long	0x106
	.byte	0
	.uleb128 0x7
	.ascii "n\0"
	.byte	0x1
	.byte	0xf
	.byte	0x24
	.long	0x2ae
	.byte	0x8
	.uleb128 0xc
	.secrel32	.LASF2
	.byte	0x11
	.byte	0xa
	.ascii "_ZN9PodVectorIi11MallocAllocE9push_backERKi\0"
	.long	0x87c
	.long	0x887
	.uleb128 0x9
	.long	0x912
	.uleb128 0x1
	.long	0x91c
	.byte	0
	.uleb128 0x17
	.ascii "size\0"
	.ascii "_ZNK9PodVectorIi11MallocAllocE4sizeEv\0"
	.long	0x2ae
	.long	0x8bf
	.long	0x8c5
	.uleb128 0x9
	.long	0x922
	.byte	0
	.uleb128 0xc
	.secrel32	.LASF3
	.byte	0x16
	.byte	0x5
	.ascii "_ZN9PodVectorIi11MallocAllocED4Ev\0"
	.long	0x8f6
	.long	0x8fc
	.uleb128 0x9
	.long	0x912
	.byte	0
	.uleb128 0x18
	.ascii "T\0"
	.long	0xd4
	.uleb128 0x19
	.secrel32	.LASF4
	.long	0x730
	.byte	0
	.uleb128 0x6
	.long	0x807
	.uleb128 0x5
	.long	0x807
	.uleb128 0x6
	.long	0x912
	.uleb128 0x2d
	.byte	0x8
	.long	0xdb
	.uleb128 0x5
	.long	0x90d
	.uleb128 0x6
	.long	0x922
	.uleb128 0x16
	.ascii "PodVector<int, NewAlloc>\0"
	.long	0xa23
	.uleb128 0x7
	.ascii "data\0"
	.byte	0x1
	.byte	0xf
	.byte	0x8
	.long	0x106
	.byte	0
	.uleb128 0x7
	.ascii "n\0"
	.byte	0x1
	.byte	0xf
	.byte	0x24
	.long	0x2ae
	.byte	0x8
	.uleb128 0xc
	.secrel32	.LASF2
	.byte	0x11
	.byte	0xa
	.ascii "_ZN9PodVectorIi8NewAllocE9push_backERKi\0"
	.long	0x99a
	.long	0x9a5
	.uleb128 0x9
	.long	0xa28
	.uleb128 0x1
	.long	0x91c
	.byte	0
	.uleb128 0x17
	.ascii "size\0"
	.ascii "_ZNK9PodVectorIi8NewAllocE4sizeEv\0"
	.long	0x2ae
	.long	0x9d9
	.long	0x9df
	.uleb128 0x9
	.long	0xa32
	.byte	0
	.uleb128 0xc
	.secrel32	.LASF3
	.byte	0x16
	.byte	0x5
	.ascii "_ZN9PodVectorIi8NewAllocED4Ev\0"
	.long	0xa0c
	.long	0xa12
	.uleb128 0x9
	.long	0xa28
	.byte	0
	.uleb128 0x18
	.ascii "T\0"
	.long	0xd4
	.uleb128 0x19
	.secrel32	.LASF4
	.long	0x7a1
	.byte	0
	.uleb128 0x6
	.long	0x92c
	.uleb128 0x5
	.long	0x92c
	.uleb128 0x6
	.long	0xa28
	.uleb128 0x5
	.long	0xa23
	.uleb128 0x6
	.long	0xa32
	.uleb128 0xf
	.ascii "free\0"
	.word	0x1c8
	.long	0xa4e
	.uleb128 0x1
	.long	0x420
	.byte	0
	.uleb128 0x3
	.ascii "malloc\0"
	.word	0x1c9
	.byte	0x11
	.long	0x420
	.long	0xa67
	.uleb128 0x1
	.long	0x84
	.byte	0
	.uleb128 0x1a
	.long	0x9a5
	.long	0xa86
	.quad	.LFB76
	.quad	.LFE76-.LFB76
	.uleb128 0x1
	.byte	0x9c
	.long	0xa93
	.uleb128 0xd
	.secrel32	.LASF5
	.long	0xa37
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x1a
	.long	0x887
	.long	0xab2
	.quad	.LFB75
	.quad	.LFE75-.LFB75
	.uleb128 0x1
	.byte	0x9c
	.long	0xabf
	.uleb128 0xd
	.secrel32	.LASF5
	.long	0x927
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x1b
	.long	0x963
	.long	0xade
	.quad	.LFB74
	.quad	.LFE74-.LFB74
	.uleb128 0x1
	.byte	0x9c
	.long	0xaf7
	.uleb128 0xd
	.secrel32	.LASF5
	.long	0xa2d
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xa
	.ascii "v\0"
	.byte	0x11
	.byte	0x1d
	.long	0x91c
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x1b
	.long	0x841
	.long	0xb16
	.quad	.LFB73
	.quad	.LFE73-.LFB73
	.uleb128 0x1
	.byte	0x9c
	.long	0xb2f
	.uleb128 0xd
	.secrel32	.LASF5
	.long	0x917
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xa
	.ascii "v\0"
	.byte	0x11
	.byte	0x1d
	.long	0x91c
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x1c
	.long	0x9df
	.long	0xb3c
	.long	0xb46
	.uleb128 0x1d
	.secrel32	.LASF5
	.long	0xa2d
	.byte	0
	.uleb128 0x1e
	.long	0xb2f
	.ascii "_ZN9PodVectorIi8NewAllocED1Ev\0"
	.long	0xb83
	.quad	.LFB72
	.quad	.LFE72-.LFB72
	.uleb128 0x1
	.byte	0x9c
	.long	0xb8c
	.uleb128 0x1f
	.long	0xb3c
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x1c
	.long	0x8c5
	.long	0xb99
	.long	0xba3
	.uleb128 0x1d
	.secrel32	.LASF5
	.long	0x917
	.byte	0
	.uleb128 0x1e
	.long	0xb8c
	.ascii "_ZN9PodVectorIi11MallocAllocED1Ev\0"
	.long	0xbe4
	.quad	.LFB69
	.quad	.LFE69-.LFB69
	.uleb128 0x1
	.byte	0x9c
	.long	0xbed
	.uleb128 0x1f
	.long	0xb99
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x2e
	.ascii "main\0"
	.byte	0x1
	.byte	0x19
	.byte	0x5
	.long	0xd4
	.quad	.LFB60
	.quad	.LFE60-.LFB60
	.uleb128 0x1
	.byte	0x9c
	.long	0xc2a
	.uleb128 0x20
	.ascii "a\0"
	.byte	0x1a
	.byte	0x21
	.long	0x807
	.uleb128 0x2
	.byte	0x91
	.sleb128 -64
	.uleb128 0x20
	.ascii "b\0"
	.byte	0x1b
	.byte	0x1e
	.long	0x92c
	.uleb128 0x3
	.byte	0x91
	.sleb128 -80
	.byte	0
	.uleb128 0x21
	.long	0x7de
	.quad	.LFB56
	.quad	.LFE56-.LFB56
	.uleb128 0x1
	.byte	0x9c
	.long	0xc52
	.uleb128 0xa
	.ascii "p\0"
	.byte	0xa
	.byte	0x20
	.long	0x420
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x22
	.long	0x7b3
	.long	0x420
	.quad	.LFB55
	.quad	.LFE55-.LFB55
	.uleb128 0x1
	.byte	0x9c
	.long	0xc7e
	.uleb128 0xa
	.ascii "n\0"
	.byte	0x9
	.byte	0x24
	.long	0x2ae
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x21
	.long	0x774
	.quad	.LFB54
	.quad	.LFE54-.LFB54
	.uleb128 0x1
	.byte	0x9c
	.long	0xca6
	.uleb128 0xa
	.ascii "p\0"
	.byte	0x6
	.byte	0x20
	.long	0x420
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x22
	.long	0x745
	.long	0x420
	.quad	.LFB53
	.quad	.LFE53-.LFB53
	.uleb128 0x1
	.byte	0x9c
	.long	0xcd2
	.uleb128 0xa
	.ascii "n\0"
	.byte	0x5
	.byte	0x24
	.long	0x2ae
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x4
	.byte	0x1
	.byte	0x2
	.ascii "bool\0"
	.uleb128 0x4
	.byte	0x1
	.byte	0x6
	.ascii "signed char\0"
	.uleb128 0x4
	.byte	0x1
	.byte	0x10
	.ascii "char8_t\0"
	.uleb128 0x4
	.byte	0x2
	.byte	0x10
	.ascii "char16_t\0"
	.uleb128 0x4
	.byte	0x4
	.byte	0x10
	.ascii "char32_t\0"
	.uleb128 0x4
	.byte	0x2
	.byte	0x5
	.ascii "short int\0"
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
	.uleb128 0xb
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
	.sleb128 7
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
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0xd
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
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0x8
	.byte	0
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 4
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 22
	.uleb128 0x18
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0xa
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
	.uleb128 0xb
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
	.uleb128 0xc
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xd
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
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
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
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
	.uleb128 0x10
	.uleb128 0xd
	.byte	0
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
	.uleb128 0x88
	.uleb128 0xb
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x11
	.uleb128 0x39
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 6
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x12
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x13
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 683
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x14
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
	.sleb128 18
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
	.uleb128 0x15
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
	.sleb128 18
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x16
	.uleb128 0x2
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 16
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 14
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x17
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
	.uleb128 0x21
	.sleb128 21
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 17
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x18
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x19
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1a
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
	.uleb128 0x1b
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
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1c
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x20
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1d
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x1e
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
	.uleb128 0x1f
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x20
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
	.uleb128 0x21
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
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
	.uleb128 0x22
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
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
	.uleb128 0x23
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
	.uleb128 0x24
	.uleb128 0x13
	.byte	0x1
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x88
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x25
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x88
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x26
	.uleb128 0x15
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x27
	.uleb128 0x13
	.byte	0x1
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x28
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x29
	.uleb128 0x26
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x2a
	.uleb128 0x15
	.byte	0x1
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2b
	.uleb128 0x2e
	.byte	0
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
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
	.uleb128 0x2c
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
	.byte	0
	.byte	0
	.uleb128 0x2d
	.uleb128 0x10
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2e
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
	.byte	0
	.section	.debug_aranges,"dr"
	.long	0xcc
	.word	0x2
	.secrel32	.Ldebug_info0
	.byte	0x8
	.byte	0
	.word	0
	.word	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	.LFB53
	.quad	.LFE53-.LFB53
	.quad	.LFB54
	.quad	.LFE54-.LFB54
	.quad	.LFB55
	.quad	.LFE55-.LFB55
	.quad	.LFB56
	.quad	.LFE56-.LFB56
	.quad	.LFB69
	.quad	.LFE69-.LFB69
	.quad	.LFB72
	.quad	.LFE72-.LFB72
	.quad	.LFB73
	.quad	.LFE73-.LFB73
	.quad	.LFB74
	.quad	.LFE74-.LFB74
	.quad	.LFB75
	.quad	.LFE75-.LFB75
	.quad	.LFB76
	.quad	.LFE76-.LFB76
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
	.quad	.LFB53
	.uleb128 .LFE53-.LFB53
	.byte	0x7
	.quad	.LFB54
	.uleb128 .LFE54-.LFB54
	.byte	0x7
	.quad	.LFB55
	.uleb128 .LFE55-.LFB55
	.byte	0x7
	.quad	.LFB56
	.uleb128 .LFE56-.LFB56
	.byte	0x7
	.quad	.LFB69
	.uleb128 .LFE69-.LFB69
	.byte	0x7
	.quad	.LFB72
	.uleb128 .LFE72-.LFB72
	.byte	0x7
	.quad	.LFB73
	.uleb128 .LFE73-.LFB73
	.byte	0x7
	.quad	.LFB74
	.uleb128 .LFE74-.LFB74
	.byte	0x7
	.quad	.LFB75
	.uleb128 .LFE75-.LFB75
	.byte	0x7
	.quad	.LFB76
	.uleb128 .LFE76-.LFB76
	.byte	0
.Ldebug_ranges3:
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
.LASF4:
	.ascii "AllocPolicy\0"
.LASF3:
	.ascii "~PodVector\0"
.LASF5:
	.ascii "this\0"
.LASF2:
	.ascii "push_back\0"
	.section	.debug_line_str,"dr"
.LASF1:
	.ascii "C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible\0"
.LASF0:
	.ascii "Examples\\_ch140_smart_ptr_policy.cpp\0"
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
