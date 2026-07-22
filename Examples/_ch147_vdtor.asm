	.file	"_ch147_vdtor.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch147_vdtor.cpp"
	.section	.text$_ZN4BaseD2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4BaseD2Ev
	.def	_ZN4BaseD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4BaseD2Ev
_ZN4BaseD2Ev:
.LFB1:
	.file 1 "Examples/_ch147_vdtor.cpp"
	.loc 1 1 15
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
	.loc 1 1 24
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.seh_endproc
	.section	.text$_ZN4BaseD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4BaseD1Ev
	.def	_ZN4BaseD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4BaseD1Ev
_ZN4BaseD1Ev:
.LFB2:
	.loc 1 1 15
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
	.loc 1 1 24
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.seh_endproc
	.section	.text$_ZN7DerivedC1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN7DerivedC1Ev
	.def	_ZN7DerivedC1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedC1Ev
_ZN7DerivedC1Ev:
.LFB9:
	.loc 1 2 8
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
	mov	QWORD PTR 32[rbp], rcx
.LBB2:
	.loc 1 2 8
	mov	ecx, 4
.LEHB0:
	call	_Znwy
.LEHE0:
	.loc 1 2 8 is_stmt 0 discriminator 3
	mov	DWORD PTR [rax], 0
	mov	rdx, QWORD PTR 32[rbp]
	mov	QWORD PTR [rdx], rax
.LBE2:
	.loc 1 2 8
	jmp	.L6
.L5:
.LBB3:
	.loc 1 2 8 discriminator 2
	mov	rbx, rax
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZN4BaseD2Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
.L6:
.LBE3:
	.loc 1 2 8
	add	rsp, 40
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -24
	ret
	.cfi_endproc
.LFE9:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA9:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE9-.LLSDACSB9
.LLSDACSB9:
	.uleb128 .LEHB0-.LFB9
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L5-.LFB9
	.uleb128 0
	.uleb128 .LEHB1-.LFB9
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE9:
	.section	.text$_ZN7DerivedC1Ev,"x"
	.linkonce discard
	.seh_endproc
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB6:
	.loc 1 3 11 is_stmt 1
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rdi
	.seh_pushreg	rdi
	.cfi_def_cfa_offset 24
	.cfi_offset 5, -24
	push	rsi
	.seh_pushreg	rsi
	.cfi_def_cfa_offset 32
	.cfi_offset 4, -32
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 40
	.cfi_offset 3, -40
	sub	rsp, 56
	.seh_stackalloc	56
	.cfi_def_cfa_offset 96
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.cfi_def_cfa 6, 48
	.seh_endprologue
	.loc 1 3 11
	call	__main
	.loc 1 3 27
	mov	ecx, 8
.LEHB2:
	call	_Znwy
.LEHE2:
	mov	rbx, rax
	.loc 1 3 27 is_stmt 0 discriminator 1
	mov	edi, 1
	mov	rcx, rbx
.LEHB3:
	call	_ZN7DerivedC1Ev
.LEHE3:
	.loc 1 3 27 discriminator 4
	mov	eax, 0
	mov	QWORD PTR -8[rbp], rbx
	test	al, al
	je	.L8
	.loc 1 3 27 discriminator 5
	mov	edx, 8
	mov	rcx, rbx
	call	_ZdlPvy
.L8:
	.loc 1 3 36 is_stmt 1 discriminator 8
	mov	rbx, QWORD PTR -8[rbp]
	test	rbx, rbx
	je	.L9
	.loc 1 3 43 discriminator 9
	mov	rcx, rbx
	call	_ZN4BaseD1Ev
	.loc 1 3 43 is_stmt 0 discriminator 11
	mov	edx, 1
	mov	rcx, rbx
	call	_ZdlPvy
.L9:
	.loc 1 3 46 is_stmt 1 discriminator 13
	mov	eax, 0
	.loc 1 3 46 is_stmt 0
	jmp	.L14
.L13:
	.loc 1 3 27 is_stmt 1 discriminator 3
	mov	rsi, rax
	test	dil, dil
	je	.L12
	.loc 1 3 27 is_stmt 0 discriminator 15
	mov	edx, 8
	mov	rcx, rbx
	call	_ZdlPvy
.L12:
	mov	rax, rsi
	mov	rcx, rax
.LEHB4:
	call	_Unwind_Resume
.LEHE4:
.L14:
	.loc 1 3 46 is_stmt 1
	add	rsp, 56
	pop	rbx
	.cfi_restore 3
	pop	rsi
	.cfi_restore 4
	pop	rdi
	.cfi_restore 5
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -24
	ret
	.cfi_endproc
.LFE6:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA6:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE6-.LLSDACSB6
.LLSDACSB6:
	.uleb128 .LEHB2-.LFB6
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB3-.LFB6
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L13-.LFB6
	.uleb128 0
	.uleb128 .LEHB4-.LFB6
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE6:
	.text
	.seh_endproc
.Letext0:
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0x235
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
	.uleb128 0x4
	.ascii "Base\0"
	.byte	0x1
	.byte	0x1
	.long	0xa5
	.uleb128 0x8
	.ascii "~Base\0"
	.byte	0x1
	.byte	0x1
	.byte	0xf
	.ascii "_ZN4BaseD4Ev\0"
	.long	0x9e
	.uleb128 0x1
	.long	0xa5
	.byte	0
	.byte	0
	.uleb128 0x2
	.long	0x77
	.uleb128 0x5
	.long	0xa5
	.uleb128 0x4
	.ascii "Derived\0"
	.byte	0x8
	.byte	0x2
	.long	0x11e
	.uleb128 0x9
	.long	0x77
	.byte	0
	.uleb128 0xa
	.ascii "p\0"
	.byte	0x1
	.byte	0x2
	.byte	0x1e
	.long	0x11e
	.byte	0
	.uleb128 0xb
	.ascii "~Derived\0"
	.byte	0x1
	.byte	0x2
	.byte	0x2e
	.ascii "_ZN7DerivedD4Ev\0"
	.long	0xf4
	.long	0xfa
	.uleb128 0x1
	.long	0x12a
	.byte	0
	.uleb128 0xc
	.ascii "Derived\0"
	.ascii "_ZN7DerivedC4Ev\0"
	.long	0x117
	.uleb128 0x1
	.long	0x12a
	.byte	0
	.byte	0
	.uleb128 0x2
	.long	0x123
	.uleb128 0xd
	.byte	0x4
	.byte	0x5
	.ascii "int\0"
	.uleb128 0x2
	.long	0xaf
	.uleb128 0x5
	.long	0x12a
	.uleb128 0xe
	.ascii "main\0"
	.byte	0x1
	.byte	0x3
	.byte	0x5
	.long	0x123
	.quad	.LFB6
	.quad	.LFE6-.LFB6
	.uleb128 0x1
	.byte	0x9c
	.long	0x165
	.uleb128 0xf
	.ascii "b\0"
	.byte	0x1
	.byte	0x3
	.byte	0x13
	.long	0xa5
	.uleb128 0x2
	.byte	0x91
	.sleb128 -56
	.byte	0
	.uleb128 0x10
	.long	0xfa
	.byte	0x1
	.byte	0x2
	.byte	0x8
	.long	0x176
	.byte	0x2
	.long	0x181
	.uleb128 0x6
	.ascii "this\0"
	.long	0x12f
	.byte	0
	.uleb128 0x11
	.long	0x165
	.ascii "_ZN7DerivedC1Ev\0"
	.long	0x1b0
	.quad	.LFB9
	.quad	.LFE9-.LFB9
	.uleb128 0x1
	.byte	0x9c
	.long	0x1b9
	.uleb128 0x3
	.long	0x176
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x12
	.long	0x83
	.long	0x1c7
	.byte	0x2
	.long	0x1d2
	.uleb128 0x6
	.ascii "this\0"
	.long	0xaa
	.byte	0
	.uleb128 0x13
	.long	0x1b9
	.ascii "_ZN4BaseD1Ev\0"
	.long	0x1fe
	.quad	.LFB2
	.quad	.LFE2-.LFB2
	.uleb128 0x1
	.byte	0x9c
	.long	0x207
	.uleb128 0x3
	.long	0x1c7
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x14
	.long	0x1b9
	.ascii "_ZN4BaseD2Ev\0"
	.long	0x22f
	.quad	.LFB1
	.quad	.LFE1-.LFB1
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x3
	.long	0x1c7
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
	.uleb128 0x34
	.uleb128 0x19
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
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x6
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
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0x1c
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0xa
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
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xd
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
	.uleb128 0xe
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
	.uleb128 0xf
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
	.uleb128 0x10
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
	.uleb128 0x11
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
	.uleb128 0x12
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
	.uleb128 0x13
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
	.uleb128 0x14
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
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"dr"
	.long	0x5c
	.word	0x2
	.secrel32	.Ldebug_info0
	.byte	0x8
	.byte	0
	.word	0
	.word	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	.LFB1
	.quad	.LFE1-.LFB1
	.quad	.LFB2
	.quad	.LFE2-.LFB2
	.quad	.LFB9
	.quad	.LFE9-.LFB9
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
	.quad	.LFB1
	.uleb128 .LFE1-.LFB1
	.byte	0x7
	.quad	.LFB2
	.uleb128 .LFE2-.LFB2
	.byte	0x7
	.quad	.LFB9
	.uleb128 .LFE9-.LFB9
	.byte	0
.Ldebug_ranges3:
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
	.section	.debug_line_str,"dr"
.LASF1:
	.ascii "C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible\0"
.LASF0:
	.ascii "Examples\\_ch147_vdtor.cpp\0"
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
