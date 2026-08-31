	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNKSt5ctypeIcE8do_widenEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt5ctypeIcE8do_widenEc
	.def	_ZNKSt5ctypeIcE8do_widenEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt5ctypeIcE8do_widenEc
_ZNKSt5ctypeIcE8do_widenEc:
.LFB2312:
	.seh_endprologue
	mov	eax, edx
	ret
	.seh_endproc
	.text
	.p2align 4
	.def	_ZL6op_addi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL6op_addi
_ZL6op_addi:
.LFB2935:
	.seh_endprologue
	lea	eax, 7[rcx]
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL6op_muli;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL6op_muli
_ZL6op_muli:
.LFB2936:
	.seh_endprologue
	lea	eax, [rcx+rcx*2]
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "cannot create std::vector larger than max_size()\0"
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6vectorIiSaIiEE19_M_range_initializeIPKiEEvT_S5_St20forward_iterator_tag.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIiSaIiEE19_M_range_initializeIPKiEEvT_S5_St20forward_iterator_tag.isra.0
_ZNSt6vectorIiSaIiEE19_M_range_initializeIPKiEEvT_S5_St20forward_iterator_tag.isra.0:
.LFB3693:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	movabs	rax, 9223372036854775804
	sub	r8, rdx
	mov	rsi, rcx
	mov	rdi, rdx
	cmp	rax, r8
	jb	.L11
	test	r8, r8
	je	.L12
	mov	rcx, r8
	mov	QWORD PTR 40[rsp], r8
	call	_Znwy
	mov	r8, QWORD PTR 40[rsp]
	mov	rcx, rax
	mov	QWORD PTR [rsi], rax
	lea	rbp, [rax+r8]
	cmp	r8, 4
	mov	QWORD PTR 16[rsi], rbp
	jle	.L9
	mov	rdx, rdi
	call	memcpy
.L8:
	mov	QWORD PTR 8[rsi], rbp
	add	rsp, 48
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L12:
	xor	eax, eax
	xor	ebp, ebp
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 16[rcx], rax
	jmp	.L8
.L9:
	mov	eax, DWORD PTR [rdi]
	mov	DWORD PTR [rcx], eax
	jmp	.L8
.L11:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.p2align 4
	.globl	_Z12run_ptrtableRKSt6vectorIiSaIiEES3_
	.def	_Z12run_ptrtableRKSt6vectorIiSaIiEES3_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12run_ptrtableRKSt6vectorIiSaIiEES3_
_Z12run_ptrtableRKSt6vectorIiSaIiEES3_:
.LFB2938:
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rdi, rdx
	mov	rdx, QWORD PTR [rcx]
	mov	r12, rcx
	cmp	QWORD PTR 8[rcx], rdx
	je	.L16
	lea	rbp, _ZL5table[rip]
	xor	ebx, ebx
	xor	esi, esi
	.p2align 4,,10
	.p2align 3
.L15:
	mov	rax, QWORD PTR [rdi]
	mov	ecx, DWORD PTR [rdx+rbx*4]
	movsx	rax, DWORD PTR [rax+rbx*4]
	add	rbx, 1
	call	[QWORD PTR 0[rbp+rax*8]]
	mov	rdx, QWORD PTR [r12]
	cdqe
	add	rsi, rax
	mov	rax, QWORD PTR 8[r12]
	sub	rax, rdx
	sar	rax, 2
	cmp	rbx, rax
	jb	.L15
	mov	rax, rsi
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L16:
	xor	esi, esi
	mov	rax, rsi
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseIiSaIiEED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12_Vector_baseIiSaIiEED2Ev
	.def	_ZNSt12_Vector_baseIiSaIiEED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIiSaIiEED2Ev
_ZNSt12_Vector_baseIiSaIiEED2Ev:
.LFB3284:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L18
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L18:
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorIiSaIiEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIiSaIiEED1Ev
	.def	_ZNSt6vectorIiSaIiEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIiSaIiEED1Ev
_ZNSt6vectorIiSaIiEED1Ev:
.LFB3290:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L20
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L20:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC3:
	.ascii "constexpr=\0"
.LC4:
	.ascii " ptrtable=\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2939:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 136
	.seh_stackalloc	136
	.seh_endprologue
	call	__main
	lea	rbx, 96[rsp]
	movdqa	xmm0, XMMWORD PTR .LC1[rip]
	mov	DWORD PTR 112[rsp], 5
	lea	rsi, 64[rsp]
	mov	rdx, rbx
	mov	QWORD PTR 80[rsp], 0
	lea	r8, 116[rsp]
	mov	rcx, rsi
	movaps	XMMWORD PTR 96[rsp], xmm0
	pxor	xmm0, xmm0
	movaps	XMMWORD PTR 64[rsp], xmm0
.LEHB0:
	call	_ZNSt6vectorIiSaIiEE19_M_range_initializeIPKiEEvT_S5_St20forward_iterator_tag.isra.0
.LEHE0:
	movdqa	xmm0, XMMWORD PTR .LC2[rip]
	lea	rdx, 32[rsp]
	mov	rcx, rbx
	mov	DWORD PTR 48[rsp], 0
	mov	QWORD PTR 112[rsp], 0
	lea	r8, 52[rsp]
	movaps	XMMWORD PTR 32[rsp], xmm0
	pxor	xmm0, xmm0
	movaps	XMMWORD PTR 96[rsp], xmm0
.LEHB1:
	call	_ZNSt6vectorIiSaIiEE19_M_range_initializeIPKiEEvT_S5_St20forward_iterator_tag.isra.0
.LEHE1:
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC3[rip]
.LEHB2:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, QWORD PTR 64[rsp]
	mov	r9, rax
	mov	r11, QWORD PTR 72[rsp]
	cmp	rcx, r11
	je	.L35
	mov	rdx, rcx
	xor	r10d, r10d
	.p2align 4,,10
	.p2align 3
.L29:
	mov	eax, DWORD PTR [rdx]
	mov	r8, rdx
	lea	rdx, 4[rdx]
	add	eax, 7
	cdqe
	add	r10, rax
	cmp	r11, rdx
	jne	.L29
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L30:
	mov	eax, DWORD PTR [rcx]
	lea	eax, [rax+rax*2]
	cdqe
	add	rdx, rax
	mov	rax, rcx
	add	rcx, 4
	cmp	r8, rax
	jne	.L30
.L28:
	add	rdx, r10
	mov	rcx, r9
	call	_ZNSo9_M_insertIxEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rdx, rbx
	mov	rcx, rsi
	mov	rdi, rax
	call	_Z12run_ptrtableRKSt6vectorIiSaIiEES3_
	mov	rdx, rax
	mov	rcx, rdi
	call	_ZNSo9_M_insertIxEERSoT_
	mov	rdi, rax
	mov	rax, QWORD PTR [rax]
	mov	rax, QWORD PTR -24[rax]
	mov	rbp, QWORD PTR 240[rdi+rax]
	test	rbp, rbp
	je	.L46
	cmp	BYTE PTR 56[rbp], 0
	je	.L32
	movsx	edx, BYTE PTR 67[rbp]
.L33:
	mov	rcx, rdi
	call	_ZNSo3putEc
	mov	rcx, rax
	call	_ZNSo5flushEv
	mov	rcx, rbx
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, rsi
	call	_ZNSt6vectorIiSaIiEED1Ev
	xor	eax, eax
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L32:
	mov	rcx, rbp
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR 0[rbp]
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	edx, 10
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L33
	mov	edx, 10
	mov	rcx, rbp
	call	rax
	movsx	edx, al
	jmp	.L33
.L35:
	xor	r10d, r10d
	xor	edx, edx
	jmp	.L28
.L46:
	call	_ZSt16__throw_bad_castv
.LEHE2:
.L37:
	mov	rcx, rbx
	mov	rdi, rax
	call	_ZNSt6vectorIiSaIiEED1Ev
.L27:
	mov	rcx, rsi
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, rdi
.LEHB3:
	call	_Unwind_Resume
.L38:
	mov	rcx, rbx
	mov	rdi, rax
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	jmp	.L27
.L39:
	mov	rbx, rax
	mov	rcx, rsi
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	mov	rcx, rbx
	call	_Unwind_Resume
	nop
.LEHE3:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2939:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2939-.LLSDACSB2939
.LLSDACSB2939:
	.uleb128 .LEHB0-.LFB2939
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L39-.LFB2939
	.uleb128 0
	.uleb128 .LEHB1-.LFB2939
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L38-.LFB2939
	.uleb128 0
	.uleb128 .LEHB2-.LFB2939
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L37-.LFB2939
	.uleb128 0
	.uleb128 .LEHB3-.LFB2939
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSE2939:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 16
_ZL5table:
	.quad	_ZL6op_addi
	.quad	_ZL6op_muli
	.align 16
.LC1:
	.long	1
	.long	2
	.long	3
	.long	4
	.align 16
.LC2:
	.long	0
	.long	1
	.long	0
	.long	1
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIxEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
