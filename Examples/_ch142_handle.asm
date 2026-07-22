	.file	"_ch142_handle.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch142_handle.cpp"
	.section	.text$_Z6idx_ofj,"x"
	.linkonce discard
	.globl	_Z6idx_ofj
	.def	_Z6idx_ofj;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6idx_ofj
_Z6idx_ofj:
.LFB5:
	.file 1 "Examples/_ch142_handle.cpp"
	.loc 1 16 50
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	.loc 1 16 63
	mov	eax, DWORD PTR 16[rbp]
	and	eax, 1048575
	.loc 1 16 73
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.seh_endproc
	.section	.text$_Z6gen_ofj,"x"
	.linkonce discard
	.globl	_Z6gen_ofj
	.def	_Z6gen_ofj;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6gen_ofj
_Z6gen_ofj:
.LFB6:
	.loc 1 17 50
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	.loc 1 17 64
	mov	eax, DWORD PTR 16[rbp]
	shr	eax, 20
	.loc 1 17 68
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.seh_endproc
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB7:
	.loc 1 19 12
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	sub	rsp, 56
	.seh_stackalloc	56
	.cfi_def_cfa_offset 80
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.cfi_def_cfa 6, 32
	.seh_endprologue
	.loc 1 19 12
	call	__main
	.loc 1 20 18
	mov	DWORD PTR -12[rbp], 42
	mov	DWORD PTR -8[rbp], 7
	.loc 1 21 19
	mov	DWORD PTR -4[rbp], 7340074
	.loc 1 22 20
	mov	ebx, DWORD PTR -12[rbp]
	.loc 1 22 34
	mov	eax, DWORD PTR -4[rbp]
	mov	ecx, eax
	call	_Z6idx_ofj
	.loc 1 22 26 discriminator 1
	add	ebx, eax
	.loc 1 22 51 discriminator 1
	mov	eax, DWORD PTR -4[rbp]
	mov	ecx, eax
	call	_Z6gen_ofj
	.loc 1 22 43 discriminator 2
	add	eax, ebx
	.loc 1 23 1
	add	rsp, 56
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -40
	ret
	.cfi_endproc
.LFE7:
	.seh_endproc
.Letext0:
	.file 2 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/corecrt.h"
	.file 3 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/stdint.h"
	.file 4 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/cstdint"
	.file 5 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/x86_64-w64-mingw32/bits/c++config.h"
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0x4fe
	.word	0x5
	.byte	0x1
	.byte	0x8
	.secrel32	.Ldebug_abbrev0
	.uleb128 0x7
	.ascii "GNU C++23 15.3.0 -masm=intel -mtune=generic -march=x86-64 -g -O0 -std=c++23\0"
	.byte	0x21
	.byte	0x4
	.long	0x3163e
	.secrel32	.LASF0
	.secrel32	.LASF1
	.secrel32	.LLRL0
	.quad	0
	.secrel32	.Ldebug_line0
	.uleb128 0x3
	.byte	0x1
	.byte	0x6
	.ascii "char\0"
	.uleb128 0x3
	.byte	0x8
	.byte	0x7
	.ascii "long long unsigned int\0"
	.uleb128 0x3
	.byte	0x8
	.byte	0x5
	.ascii "long long int\0"
	.uleb128 0x1
	.ascii "intptr_t\0"
	.byte	0x2
	.byte	0x3e
	.byte	0x23
	.long	0x99
	.uleb128 0x1
	.ascii "uintptr_t\0"
	.byte	0x2
	.byte	0x4b
	.byte	0x2c
	.long	0x7f
	.uleb128 0x3
	.byte	0x2
	.byte	0x7
	.ascii "short unsigned int\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x5
	.ascii "int\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x5
	.ascii "long int\0"
	.uleb128 0x3
	.byte	0x2
	.byte	0x7
	.ascii "wchar_t\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x7
	.ascii "unsigned int\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x7
	.ascii "long unsigned int\0"
	.uleb128 0x3
	.byte	0x1
	.byte	0x8
	.ascii "unsigned char\0"
	.uleb128 0x3
	.byte	0x10
	.byte	0x4
	.ascii "long double\0"
	.uleb128 0x1
	.ascii "int8_t\0"
	.byte	0x3
	.byte	0x23
	.byte	0x15
	.long	0x155
	.uleb128 0x3
	.byte	0x1
	.byte	0x6
	.ascii "signed char\0"
	.uleb128 0x1
	.ascii "uint8_t\0"
	.byte	0x3
	.byte	0x24
	.byte	0x19
	.long	0x126
	.uleb128 0x1
	.ascii "int16_t\0"
	.byte	0x3
	.byte	0x25
	.byte	0x10
	.long	0x184
	.uleb128 0x3
	.byte	0x2
	.byte	0x5
	.ascii "short int\0"
	.uleb128 0x1
	.ascii "uint16_t\0"
	.byte	0x3
	.byte	0x26
	.byte	0x19
	.long	0xcd
	.uleb128 0x1
	.ascii "int32_t\0"
	.byte	0x3
	.byte	0x27
	.byte	0xe
	.long	0xe3
	.uleb128 0x1
	.ascii "uint32_t\0"
	.byte	0x3
	.byte	0x28
	.byte	0x14
	.long	0x101
	.uleb128 0x1
	.ascii "int64_t\0"
	.byte	0x3
	.byte	0x29
	.byte	0x26
	.long	0x99
	.uleb128 0x1
	.ascii "uint64_t\0"
	.byte	0x3
	.byte	0x2a
	.byte	0x30
	.long	0x7f
	.uleb128 0x1
	.ascii "int_least8_t\0"
	.byte	0x3
	.byte	0x2d
	.byte	0x15
	.long	0x155
	.uleb128 0x1
	.ascii "uint_least8_t\0"
	.byte	0x3
	.byte	0x2e
	.byte	0x19
	.long	0x126
	.uleb128 0x1
	.ascii "int_least16_t\0"
	.byte	0x3
	.byte	0x2f
	.byte	0x10
	.long	0x184
	.uleb128 0x1
	.ascii "uint_least16_t\0"
	.byte	0x3
	.byte	0x30
	.byte	0x19
	.long	0xcd
	.uleb128 0x1
	.ascii "int_least32_t\0"
	.byte	0x3
	.byte	0x31
	.byte	0xe
	.long	0xe3
	.uleb128 0x1
	.ascii "uint_least32_t\0"
	.byte	0x3
	.byte	0x32
	.byte	0x14
	.long	0x101
	.uleb128 0x1
	.ascii "int_least64_t\0"
	.byte	0x3
	.byte	0x33
	.byte	0x26
	.long	0x99
	.uleb128 0x1
	.ascii "uint_least64_t\0"
	.byte	0x3
	.byte	0x34
	.byte	0x30
	.long	0x7f
	.uleb128 0x1
	.ascii "int_fast8_t\0"
	.byte	0x3
	.byte	0x3a
	.byte	0x15
	.long	0x155
	.uleb128 0x1
	.ascii "uint_fast8_t\0"
	.byte	0x3
	.byte	0x3b
	.byte	0x17
	.long	0x126
	.uleb128 0x1
	.ascii "int_fast16_t\0"
	.byte	0x3
	.byte	0x3c
	.byte	0x10
	.long	0x184
	.uleb128 0x1
	.ascii "uint_fast16_t\0"
	.byte	0x3
	.byte	0x3d
	.byte	0x19
	.long	0xcd
	.uleb128 0x1
	.ascii "int_fast32_t\0"
	.byte	0x3
	.byte	0x3e
	.byte	0xe
	.long	0xe3
	.uleb128 0x1
	.ascii "uint_fast32_t\0"
	.byte	0x3
	.byte	0x3f
	.byte	0x18
	.long	0x101
	.uleb128 0x1
	.ascii "int_fast64_t\0"
	.byte	0x3
	.byte	0x40
	.byte	0x26
	.long	0x99
	.uleb128 0x1
	.ascii "uint_fast64_t\0"
	.byte	0x3
	.byte	0x41
	.byte	0x30
	.long	0x7f
	.uleb128 0x1
	.ascii "intmax_t\0"
	.byte	0x3
	.byte	0x44
	.byte	0x26
	.long	0x99
	.uleb128 0x1
	.ascii "uintmax_t\0"
	.byte	0x3
	.byte	0x45
	.byte	0x30
	.long	0x7f
	.uleb128 0x8
	.ascii "std\0"
	.byte	0x5
	.word	0x150
	.byte	0xb
	.long	0x419
	.uleb128 0x2
	.byte	0x35
	.long	0x146
	.uleb128 0x2
	.byte	0x36
	.long	0x174
	.uleb128 0x2
	.byte	0x37
	.long	0x1a2
	.uleb128 0x2
	.byte	0x38
	.long	0x1c3
	.uleb128 0x2
	.byte	0x3a
	.long	0x296
	.uleb128 0x2
	.byte	0x3b
	.long	0x2bf
	.uleb128 0x2
	.byte	0x3c
	.long	0x2ea
	.uleb128 0x2
	.byte	0x3d
	.long	0x315
	.uleb128 0x2
	.byte	0x3f
	.long	0x1e4
	.uleb128 0x2
	.byte	0x40
	.long	0x20f
	.uleb128 0x2
	.byte	0x41
	.long	0x23c
	.uleb128 0x2
	.byte	0x42
	.long	0x269
	.uleb128 0x2
	.byte	0x44
	.long	0x340
	.uleb128 0x2
	.byte	0x45
	.long	0xaa
	.uleb128 0x2
	.byte	0x47
	.long	0x164
	.uleb128 0x2
	.byte	0x48
	.long	0x191
	.uleb128 0x2
	.byte	0x49
	.long	0x1b2
	.uleb128 0x2
	.byte	0x4a
	.long	0x1d3
	.uleb128 0x2
	.byte	0x4c
	.long	0x2aa
	.uleb128 0x2
	.byte	0x4d
	.long	0x2d4
	.uleb128 0x2
	.byte	0x4e
	.long	0x2ff
	.uleb128 0x2
	.byte	0x4f
	.long	0x32a
	.uleb128 0x2
	.byte	0x51
	.long	0x1f9
	.uleb128 0x2
	.byte	0x52
	.long	0x225
	.uleb128 0x2
	.byte	0x53
	.long	0x252
	.uleb128 0x2
	.byte	0x54
	.long	0x27f
	.uleb128 0x2
	.byte	0x56
	.long	0x351
	.uleb128 0x2
	.byte	0x57
	.long	0xbb
	.byte	0
	.uleb128 0x9
	.ascii "EntityHandle\0"
	.byte	0x8
	.byte	0x1
	.byte	0x7
	.byte	0x8
	.long	0x44c
	.uleb128 0x4
	.ascii "index\0"
	.byte	0x8
	.long	0x1b2
	.byte	0
	.uleb128 0x4
	.ascii "version\0"
	.byte	0x9
	.long	0x1b2
	.byte	0x4
	.byte	0
	.uleb128 0xa
	.ascii "main\0"
	.byte	0x1
	.byte	0x13
	.byte	0x5
	.long	0xe3
	.quad	.LFB7
	.quad	.LFE7-.LFB7
	.uleb128 0x1
	.byte	0x9c
	.long	0x48d
	.uleb128 0x5
	.ascii "h\0"
	.byte	0x14
	.byte	0x12
	.long	0x419
	.uleb128 0x2
	.byte	0x91
	.sleb128 -44
	.uleb128 0x5
	.ascii "packed\0"
	.byte	0x15
	.byte	0x13
	.long	0x1b2
	.uleb128 0x2
	.byte	0x91
	.sleb128 -36
	.byte	0
	.uleb128 0xb
	.ascii "gen_of\0"
	.byte	0x1
	.byte	0x11
	.byte	0x19
	.ascii "_Z6gen_ofj\0"
	.long	0x1b2
	.quad	.LFB6
	.quad	.LFE6-.LFB6
	.uleb128 0x1
	.byte	0x9c
	.long	0x4c9
	.uleb128 0x6
	.ascii "h\0"
	.byte	0x11
	.long	0x1b2
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0xc
	.ascii "idx_of\0"
	.byte	0x1
	.byte	0x10
	.byte	0x19
	.ascii "_Z6idx_ofj\0"
	.long	0x1b2
	.quad	.LFB5
	.quad	.LFE5-.LFB5
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x6
	.ascii "h\0"
	.byte	0x10
	.long	0x1b2
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.byte	0
	.section	.debug_abbrev,"dr"
.Ldebug_abbrev0:
	.uleb128 0x1
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
	.uleb128 0x2
	.uleb128 0x8
	.byte	0
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 4
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x18
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3
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
	.uleb128 0x4
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x5
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
	.uleb128 0x6
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
	.uleb128 0x21
	.sleb128 46
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x7
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
	.uleb128 0x8
	.uleb128 0x39
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x9
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
	.uleb128 0xa
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
	.uleb128 0xb
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
	.uleb128 0xc
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
	.long	0x4c
	.word	0x2
	.secrel32	.Ldebug_info0
	.byte	0x8
	.byte	0
	.word	0
	.word	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	.LFB5
	.quad	.LFE5-.LFB5
	.quad	.LFB6
	.quad	.LFE6-.LFB6
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
	.quad	.LFB5
	.uleb128 .LFE5-.LFB5
	.byte	0x7
	.quad	.LFB6
	.uleb128 .LFE6-.LFB6
	.byte	0
.Ldebug_ranges3:
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
	.section	.debug_line_str,"dr"
.LASF1:
	.ascii "C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible\0"
.LASF0:
	.ascii "Examples\\_ch142_handle.cpp\0"
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
