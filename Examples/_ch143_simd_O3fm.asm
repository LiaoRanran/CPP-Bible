	.file	"_ch143_simd.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch143_simd.cpp"
	.globl	_Z5scalePfPKfif
	.def	_Z5scalePfPKfif;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5scalePfPKfif
_Z5scalePfPKfif:
.LFB0:
	.file 1 "Examples/_ch143_simd.cpp"
	.loc 1 3 76
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	DWORD PTR 32[rbp], r8d
	movss	DWORD PTR 40[rbp], xmm3
.LBB2:
	.loc 1 4 14
	mov	DWORD PTR -4[rbp], 0
	.loc 1 4 5
	jmp	.L2
.L3:
	.loc 1 5 18
	mov	eax, DWORD PTR -4[rbp]
	cdqe
	.loc 1 5 19
	lea	rdx, 0[0+rax*4]
	mov	rax, QWORD PTR 24[rbp]
	add	rax, rdx
	movss	xmm0, DWORD PTR [rax]
	.loc 1 5 11
	mov	eax, DWORD PTR -4[rbp]
	cdqe
	.loc 1 5 12
	lea	rdx, 0[0+rax*4]
	mov	rax, QWORD PTR 16[rbp]
	add	rax, rdx
	.loc 1 5 21
	mulss	xmm0, DWORD PTR 40[rbp]
	.loc 1 5 14
	movss	DWORD PTR [rax], xmm0
	.loc 1 4 5 discriminator 3
	add	DWORD PTR -4[rbp], 1
.L2:
	.loc 1 4 23 discriminator 1
	mov	eax, DWORD PTR -4[rbp]
	cmp	eax, DWORD PTR 32[rbp]
	jl	.L3
.LBE2:
	.loc 1 6 1
	nop
	nop
	add	rsp, 16
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.seh_endproc
.Letext0:
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0x11b
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
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.secrel32	.Ldebug_line0
	.uleb128 0x6
	.ascii "scale\0"
	.byte	0x1
	.byte	0x3
	.byte	0x6
	.ascii "_Z5scalePfPKfif\0"
	.quad	.LFB0
	.quad	.LFE0-.LFB0
	.uleb128 0x1
	.byte	0x9c
	.long	0xf7
	.uleb128 0x1
	.ascii "a\0"
	.byte	0x1e
	.long	0xfc
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1
	.ascii "b\0"
	.byte	0x39
	.long	0x113
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x1
	.ascii "n\0"
	.byte	0x40
	.long	0x118
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.uleb128 0x1
	.ascii "k\0"
	.byte	0x49
	.long	0x101
	.uleb128 0x2
	.byte	0x91
	.sleb128 24
	.uleb128 0x7
	.quad	.LBB2
	.quad	.LBE2-.LBB2
	.uleb128 0x8
	.ascii "i\0"
	.byte	0x1
	.byte	0x4
	.byte	0xe
	.long	0x118
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.byte	0
	.byte	0
	.uleb128 0x2
	.long	0x101
	.uleb128 0x3
	.long	0xf7
	.uleb128 0x4
	.byte	0x4
	.ascii "float\0"
	.uleb128 0x9
	.long	0x101
	.uleb128 0x2
	.long	0x109
	.uleb128 0x3
	.long	0x10e
	.uleb128 0x4
	.byte	0x5
	.ascii "int\0"
	.byte	0
	.section	.debug_abbrev,"dr"
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 3
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3
	.uleb128 0x37
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 4
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x8
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
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x10
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x6
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
	.uleb128 0x7
	.uleb128 0xb
	.byte	0x1
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.byte	0
	.byte	0
	.uleb128 0x8
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
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"dr"
	.long	0x2c
	.word	0x2
	.secrel32	.Ldebug_info0
	.byte	0x8
	.byte	0
	.word	0
	.word	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	0
	.quad	0
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
	.section	.debug_line_str,"dr"
.LASF1:
	.ascii "C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible\0"
.LASF0:
	.ascii "Examples\\_ch143_simd.cpp\0"
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
