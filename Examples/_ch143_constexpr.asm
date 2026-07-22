	.file	"_ch143_constexpr.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch143_constexpr.cpp"
	.section	.text$_Z3fibi,"x"
	.linkonce discard
	.globl	_Z3fibi
	.def	_Z3fibi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3fibi
_Z3fibi:
.LFB0:
	.file 1 "Examples/_ch143_constexpr.cpp"
	.loc 1 2 26
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	sub	rsp, 40
	.seh_stackalloc	40
	.cfi_def_cfa_offset 64
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.cfi_def_cfa 6, 32
	.seh_endprologue
	mov	DWORD PTR 32[rbp], ecx
	.loc 1 3 18
	cmp	DWORD PTR 32[rbp], 1
	jle	.L2
	.loc 1 3 27 discriminator 1
	mov	eax, DWORD PTR 32[rbp]
	sub	eax, 1
	mov	ecx, eax
	call	_Z3fibi
	mov	ebx, eax
	.loc 1 3 40 discriminator 3
	mov	eax, DWORD PTR 32[rbp]
	sub	eax, 2
	mov	ecx, eax
	call	_Z3fibi
	.loc 1 3 46 discriminator 4
	add	eax, ebx
	.loc 1 3 46 is_stmt 0
	jmp	.L4
.L2:
	.loc 1 3 46 discriminator 2
	mov	eax, DWORD PTR 32[rbp]
.L4:
	.loc 1 4 1 is_stmt 1
	add	rsp, 40
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -24
	ret
	.cfi_endproc
.LFE0:
	.seh_endproc
	.section .rdata,"dr"
	.align 4
_ZL10kTableSize:
	.long	55
	.section	.text$_Z10make_tablei,"x"
	.linkonce discard
	.globl	_Z10make_tablei
	.def	_Z10make_tablei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10make_tablei
_Z10make_tablei:
.LFB1:
	.loc 1 10 33
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
	mov	DWORD PTR 16[rbp], ecx
	.loc 1 10 45
	mov	eax, DWORD PTR 16[rbp]
	mov	ecx, eax
	call	_Z3fibi
	.loc 1 10 50
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.seh_endproc
	.text
	.globl	_Z9use_tablev
	.def	_Z9use_tablev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9use_tablev
_Z9use_tablev:
.LFB2:
	.loc 1 12 17
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	sub	rsp, 272
	.seh_stackalloc	272
	.cfi_def_cfa_offset 288
	lea	rbp, 128[rsp]
	.seh_setframe	rbp, 128
	.cfi_def_cfa 6, 160
	.seh_endprologue
.LBB2:
	.loc 1 14 14
	mov	DWORD PTR 140[rbp], 0
	.loc 1 14 5
	jmp	.L8
.L9:
	.loc 1 14 61 discriminator 5
	mov	eax, DWORD PTR 140[rbp]
	mov	ecx, eax
	call	_Z10make_tablei
	.loc 1 14 49 discriminator 3
	mov	edx, DWORD PTR 140[rbp]
	movsxd	rdx, edx
	mov	DWORD PTR -96[rbp+rdx*4], eax
	.loc 1 14 5 discriminator 3
	add	DWORD PTR 140[rbp], 1
.L8:
	.loc 1 14 23 discriminator 4
	cmp	DWORD PTR 140[rbp], 54
	jle	.L9
.LBE2:
	.loc 1 15 9
	mov	DWORD PTR 136[rbp], 0
.LBB3:
	.loc 1 16 14
	mov	DWORD PTR 132[rbp], 0
	.loc 1 16 5
	jmp	.L10
.L11:
	.loc 1 16 52 discriminator 3
	mov	eax, DWORD PTR 132[rbp]
	cdqe
	mov	eax, DWORD PTR -96[rbp+rax*4]
	.loc 1 16 44 discriminator 3
	add	DWORD PTR 136[rbp], eax
	.loc 1 16 5 discriminator 3
	add	DWORD PTR 132[rbp], 1
.L10:
	.loc 1 16 23 discriminator 1
	cmp	DWORD PTR 132[rbp], 54
	jle	.L11
.LBE3:
	.loc 1 17 12
	mov	eax, DWORD PTR 136[rbp]
	.loc 1 18 1
	add	rsp, 272
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -264
	ret
	.cfi_endproc
.LFE2:
	.seh_endproc
.Letext0:
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0x1d0
	.word	0x5
	.byte	0x1
	.byte	0x8
	.secrel32	.Ldebug_abbrev0
	.uleb128 0x5
	.ascii "GNU C++23 15.3.0 -masm=intel -mtune=generic -march=x86-64 -g -O0 -std=c++23\0"
	.byte	0x21
	.byte	0x4
	.long	0x3163e
	.secrel32	.LASF0
	.secrel32	.LASF1
	.secrel32	.LLRL0
	.quad	0
	.secrel32	.Ldebug_line0
	.uleb128 0x6
	.ascii "kTableSize\0"
	.byte	0x1
	.byte	0x6
	.byte	0xf
	.long	0x9b
	.uleb128 0x9
	.byte	0x3
	.quad	_ZL10kTableSize
	.uleb128 0x2
	.byte	0x4
	.byte	0x5
	.ascii "int\0"
	.uleb128 0x7
	.long	0x94
	.uleb128 0x3
	.ascii "use_table\0"
	.byte	0xc
	.byte	0x5
	.ascii "_Z9use_tablev\0"
	.long	0x94
	.quad	.LFB2
	.quad	.LFE2-.LFB2
	.uleb128 0x1
	.byte	0x9c
	.long	0x131
	.uleb128 0x1
	.ascii "arr\0"
	.byte	0xd
	.byte	0x9
	.long	0x131
	.uleb128 0x3
	.byte	0x91
	.sleb128 -256
	.uleb128 0x1
	.ascii "s\0"
	.byte	0xf
	.byte	0x9
	.long	0x94
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x8
	.quad	.LBB2
	.quad	.LBE2-.LBB2
	.long	0x112
	.uleb128 0x1
	.ascii "i\0"
	.byte	0xe
	.byte	0xe
	.long	0x94
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.byte	0
	.uleb128 0x9
	.quad	.LBB3
	.quad	.LBE3-.LBB3
	.uleb128 0x1
	.ascii "i\0"
	.byte	0x10
	.byte	0xe
	.long	0x94
	.uleb128 0x2
	.byte	0x91
	.sleb128 -28
	.byte	0
	.byte	0
	.uleb128 0xa
	.long	0x94
	.long	0x141
	.uleb128 0xb
	.long	0x141
	.byte	0x36
	.byte	0
	.uleb128 0x2
	.byte	0x8
	.byte	0x7
	.ascii "long long unsigned int\0"
	.uleb128 0x3
	.ascii "make_table\0"
	.byte	0xa
	.byte	0xf
	.ascii "_Z10make_tablei\0"
	.long	0x94
	.quad	.LFB1
	.quad	.LFE1-.LFB1
	.uleb128 0x1
	.byte	0x9c
	.long	0x1a0
	.uleb128 0x4
	.ascii "i\0"
	.byte	0xa
	.byte	0x1e
	.long	0x94
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0xc
	.ascii "fib\0"
	.byte	0x1
	.byte	0x2
	.byte	0xf
	.ascii "_Z3fibi\0"
	.long	0x94
	.quad	.LFB0
	.quad	.LFE0-.LFB0
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x4
	.ascii "n\0"
	.byte	0x2
	.byte	0x17
	.long	0x94
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.byte	0
	.section	.debug_abbrev,"dr"
.Ldebug_abbrev0:
	.uleb128 0x1
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
	.uleb128 0x2
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
	.uleb128 0x3
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
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4
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
	.uleb128 0x5
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
	.uleb128 0x6
	.uleb128 0x34
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
	.uleb128 0x6c
	.uleb128 0x19
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0xb
	.byte	0x1
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0xb
	.byte	0x1
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.byte	0
	.byte	0
	.uleb128 0xa
	.uleb128 0x1
	.byte	0x1
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2f
	.uleb128 0xb
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
	.uleb128 0x7c
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
	.quad	.LFB0
	.quad	.LFE0-.LFB0
	.quad	.LFB1
	.quad	.LFE1-.LFB1
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
	.quad	.LFB0
	.uleb128 .LFE0-.LFB0
	.byte	0x7
	.quad	.LFB1
	.uleb128 .LFE1-.LFB1
	.byte	0
.Ldebug_ranges3:
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
	.section	.debug_line_str,"dr"
.LASF1:
	.ascii "C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible\0"
.LASF0:
	.ascii "Examples\\_ch143_constexpr.cpp\0"
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
