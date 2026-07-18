	.file	"_ch115_buf_gcc15_noinline.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB0:
	.text
.LHOTB0:
	.align 2
	.p2align 4
	.def	_ZN3BufaSERKS_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN3BufaSERKS_.isra.0
_ZN3BufaSERKS_.isra.0:
.LFB6241:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rbx, rcx
	mov	rsi, rdx
	cmp	rcx, rdx
	je	.L1
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L4
	call	_ZdaPv
.L4:
	mov	r8, QWORD PTR 8[rsi]
	cmp	QWORD PTR [rsi], 0
	je	.L5
	movabs	rax, 2305843009213693950
	cmp	rax, r8
	jb	.L6
	lea	rcx, 0[0+r8*4]
	mov	QWORD PTR 40[rsp], r8
	call	_Znay
	mov	r8, QWORD PTR 40[rsp]
	mov	QWORD PTR [rbx], rax
	mov	rcx, rax
	mov	QWORD PTR 8[rbx], r8
	test	r8, r8
	je	.L1
	mov	r9, QWORD PTR [rsi]
	xor	eax, eax
	.p2align 4
	.p2align 4
	.p2align 3
.L9:
	mov	edx, DWORD PTR [r9+rax*4]
	mov	DWORD PTR [rcx+rax*4], edx
	add	rax, 1
	cmp	r8, rax
	jne	.L9
.L1:
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
.L5:
	xor	eax, eax
	mov	QWORD PTR 8[rbx], r8
	mov	QWORD PTR [rbx], rax
	jmp	.L1
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZN3BufaSERKS_.isra.0.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN3BufaSERKS_.isra.0.cold
	.seh_stackalloc	72
	.seh_savereg	rbx, 56
	.seh_savereg	rsi, 64
	.seh_endprologue
_ZN3BufaSERKS_.isra.0.cold:
.L6:
	call	__cxa_throw_bad_array_new_length
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.text
.LHOTE0:
	.align 2
	.p2align 4
	.def	_ZN3BufaSEOS_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN3BufaSEOS_.isra.0
_ZN3BufaSEOS_.isra.0:
.LFB6242:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, rcx
	cmp	rcx, rdx
	je	.L15
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L17
	mov	QWORD PTR 56[rsp], rdx
	mov	QWORD PTR 48[rsp], rax
	call	_ZdaPv
	mov	rdx, QWORD PTR 56[rsp]
	mov	rax, QWORD PTR 48[rsp]
.L17:
	mov	rcx, QWORD PTR [rdx]
	mov	QWORD PTR [rax], rcx
	mov	rcx, QWORD PTR 8[rdx]
	mov	QWORD PTR 8[rax], rcx
	mov	QWORD PTR [rdx], 0
	mov	QWORD PTR 8[rdx], 0
.L15:
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB1:
	.section	.text.startup,"x"
.LHOTB1:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4130:
	push	r14
	.seh_pushreg	r14
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	call	__main
	lea	rdx, 48[rsp]
	lea	rcx, 64[rsp]
	mov	QWORD PTR 56[rsp], 0
	mov	QWORD PTR 72[rsp], 0
	mov	QWORD PTR 64[rsp], 0
	mov	QWORD PTR 48[rsp], 0
	call	_ZN3BufaSEOS_.isra.0
	lea	rcx, 80[rsp]
	lea	rdx, 64[rsp]
	mov	QWORD PTR 80[rsp], 0
	mov	QWORD PTR 88[rsp], 0
	mov	rdi, QWORD PTR 64[rsp]
	mov	rsi, QWORD PTR 48[rsp]
.LEHB0:
	call	_ZN3BufaSERKS_.isra.0
.LEHE0:
	mov	rdx, QWORD PTR 88[rsp]
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	rbx, QWORD PTR 80[rsp]
.LEHB1:
	call	_ZNSo9_M_insertIyEERSoT_
	mov	rdx, QWORD PTR [rax]
	mov	BYTE PTR 47[rsp], 10
	mov	rdx, QWORD PTR -24[rdx]
	cmp	QWORD PTR 16[rax+rdx], 0
	je	.L22
	lea	rdx, 47[rsp]
	mov	r8d, 1
	mov	rcx, rax
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
.L25:
	test	rbx, rbx
	je	.L24
	mov	rcx, rbx
	call	_ZdaPv
.L24:
	test	rdi, rdi
	je	.L26
	mov	rcx, rdi
	call	_ZdaPv
.L26:
	test	rsi, rsi
	je	.L40
	mov	rcx, rsi
	call	_ZdaPv
.L40:
	xor	eax, eax
	add	rsp, 104
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
.L22:
	mov	edx, 10
	mov	rcx, rax
	call	_ZNSo3putEc
.LEHE1:
	jmp	.L25
.L33:
	mov	r14, rax
	jmp	.L28
.L34:
	mov	r14, rax
	jmp	.L29
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4130:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4130-.LLSDACSB4130
.LLSDACSB4130:
	.uleb128 .LEHB0-.LFB4130
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L33-.LFB4130
	.uleb128 0
	.uleb128 .LEHB1-.LFB4130
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L34-.LFB4130
	.uleb128 0
.LLSDACSE4130:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	136
	.seh_savereg	rbx, 104
	.seh_savereg	rsi, 112
	.seh_savereg	rdi, 120
	.seh_savereg	r14, 128
	.seh_endprologue
main.cold:
.L28:
	mov	rbx, QWORD PTR 80[rsp]
.L29:
	test	rbx, rbx
	je	.L30
	mov	rcx, rbx
	call	_ZdaPv
.L30:
	test	rdi, rdi
	je	.L31
	mov	rcx, rdi
	call	_ZdaPv
.L31:
	test	rsi, rsi
	je	.L32
	mov	rcx, rsi
	call	_ZdaPv
.L32:
	mov	rcx, r14
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4130:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4130-.LLSDACSBC4130
.LLSDACSBC4130:
	.uleb128 .LEHB2-.LCOLDB1
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC4130:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.section	.text.startup,"x"
.LHOTE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw_bad_array_new_length;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
