	.file	"_ch143_soa_loop.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch143_soa_loop.cpp"
	.globl	_Z8step_soa3SoAif
	.def	_Z8step_soa3SoAif;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8step_soa3SoAif
_Z8step_soa3SoAif:
.LFB0:
	.file 1 "Examples/_ch143_soa_loop.cpp"
	.loc 1 4 40
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	sub	rsp, 24
	.seh_stackalloc	24
	.cfi_def_cfa_offset 48
	lea	rbp, 16[rsp]
	.seh_setframe	rbp, 16
	.cfi_def_cfa 6, 32
	.seh_endprologue
	mov	rbx, rcx
	mov	DWORD PTR 40[rbp], edx
	movss	DWORD PTR 48[rbp], xmm2
	.loc 1 5 11
	pxor	xmm0, xmm0
	movss	DWORD PTR -4[rbp], xmm0
.LBB2:
	.loc 1 6 14
	mov	DWORD PTR -8[rbp], 0
	.loc 1 6 5
	jmp	.L2
.L3:
	.loc 1 7 11
	mov	rax, QWORD PTR [rbx]
	.loc 1 7 14
	mov	edx, DWORD PTR -8[rbp]
	movsxd	rdx, edx
	sal	rdx, 2
	add	rax, rdx
	movss	xmm1, DWORD PTR [rax]
	.loc 1 7 21
	mov	rax, QWORD PTR 16[rbx]
	.loc 1 7 24
	mov	edx, DWORD PTR -8[rbp]
	movsxd	rdx, edx
	.loc 1 7 25
	sal	rdx, 2
	add	rax, rdx
	movss	xmm0, DWORD PTR [rax]
	.loc 1 7 27
	mulss	xmm0, DWORD PTR 48[rbp]
	.loc 1 7 11
	mov	rax, QWORD PTR [rbx]
	.loc 1 7 14
	mov	edx, DWORD PTR -8[rbp]
	movsxd	rdx, edx
	sal	rdx, 2
	add	rax, rdx
	.loc 1 7 16
	addss	xmm0, xmm1
	movss	DWORD PTR [rax], xmm0
	.loc 1 8 11
	mov	rax, QWORD PTR 8[rbx]
	.loc 1 8 14
	mov	edx, DWORD PTR -8[rbp]
	movsxd	rdx, edx
	sal	rdx, 2
	add	rax, rdx
	movss	xmm1, DWORD PTR [rax]
	.loc 1 8 21
	mov	rax, QWORD PTR 24[rbx]
	.loc 1 8 24
	mov	edx, DWORD PTR -8[rbp]
	movsxd	rdx, edx
	.loc 1 8 25
	sal	rdx, 2
	add	rax, rdx
	movss	xmm0, DWORD PTR [rax]
	.loc 1 8 27
	mulss	xmm0, DWORD PTR 48[rbp]
	.loc 1 8 11
	mov	rax, QWORD PTR 8[rbx]
	.loc 1 8 14
	mov	edx, DWORD PTR -8[rbp]
	movsxd	rdx, edx
	sal	rdx, 2
	add	rax, rdx
	.loc 1 8 16
	addss	xmm0, xmm1
	movss	DWORD PTR [rax], xmm0
	.loc 1 9 16
	mov	rax, QWORD PTR [rbx]
	.loc 1 9 18
	mov	edx, DWORD PTR -8[rbp]
	movsxd	rdx, edx
	.loc 1 9 19
	sal	rdx, 2
	add	rax, rdx
	movss	xmm0, DWORD PTR [rax]
	.loc 1 9 11
	movss	xmm1, DWORD PTR -4[rbp]
	addss	xmm0, xmm1
	movss	DWORD PTR -4[rbp], xmm0
	.loc 1 6 5 discriminator 3
	add	DWORD PTR -8[rbp], 1
.L2:
	.loc 1 6 23 discriminator 1
	mov	eax, DWORD PTR -8[rbp]
	cmp	eax, DWORD PTR 40[rbp]
	jl	.L3
.LBE2:
	.loc 1 11 12
	movss	xmm0, DWORD PTR -4[rbp]
	.loc 1 12 1
	add	rsp, 24
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -8
	ret
	.cfi_endproc
.LFE0:
	.seh_endproc
.Letext0:
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0x146
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
	.ascii "SoA\0"
	.byte	0x20
	.byte	0x1
	.byte	0x2
	.byte	0x8
	.long	0xaf
	.uleb128 0x1
	.ascii "x\0"
	.byte	0x15
	.long	0xaf
	.byte	0
	.uleb128 0x1
	.ascii "y\0"
	.byte	0x1f
	.long	0xaf
	.byte	0x8
	.uleb128 0x1
	.ascii "vx\0"
	.byte	0x29
	.long	0xaf
	.byte	0x10
	.uleb128 0x1
	.ascii "vy\0"
	.byte	0x34
	.long	0xaf
	.byte	0x18
	.byte	0
	.uleb128 0x7
	.byte	0x8
	.long	0xb5
	.uleb128 0x3
	.byte	0x4
	.ascii "float\0"
	.uleb128 0x8
	.ascii "step_soa\0"
	.byte	0x1
	.byte	0x4
	.byte	0x7
	.ascii "_Z8step_soa3SoAif\0"
	.long	0xb5
	.quad	.LFB0
	.quad	.LFE0-.LFB0
	.uleb128 0x1
	.byte	0x9c
	.long	0x143
	.uleb128 0x2
	.ascii "p\0"
	.byte	0x14
	.long	0x7b
	.uleb128 0x2
	.byte	0x73
	.sleb128 0
	.uleb128 0x2
	.ascii "n\0"
	.byte	0x1b
	.long	0x143
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x2
	.ascii "dt\0"
	.byte	0x24
	.long	0xb5
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.uleb128 0x4
	.ascii "s\0"
	.byte	0x5
	.byte	0xb
	.long	0xb5
	.uleb128 0x2
	.byte	0x91
	.sleb128 -36
	.uleb128 0x9
	.quad	.LBB2
	.quad	.LBE2-.LBB2
	.uleb128 0x4
	.ascii "i\0"
	.byte	0x6
	.byte	0xe
	.long	0x143
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.byte	0
	.uleb128 0x3
	.byte	0x5
	.ascii "int\0"
	.byte	0
	.section	.debug_abbrev,"dr"
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 4
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x3
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
	.uleb128 0x4
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
	.uleb128 0x7
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
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
	.uleb128 0x9
	.uleb128 0xb
	.byte	0x1
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
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
	.ascii "Examples\\_ch143_soa_loop.cpp\0"
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
