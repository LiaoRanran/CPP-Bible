	.file	"ch79_list_test.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.unlikely,"x"
.LCOLDB0:
	.section	.text.startup,"x"
.LHOTB0:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1400:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	xor	ebx, ebx
	call	__main
	lea	rsi, 48[rsp]
	mov	QWORD PTR 64[rsp], 0
	movq	xmm0, rsi
	punpcklqdq	xmm0, xmm0
	movaps	XMMWORD PTR 48[rsp], xmm0
	.p2align 4
	.p2align 3
.L2:
	mov	ecx, 24
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	DWORD PTR 16[rax], ebx
	mov	rdx, rsi
	mov	rcx, rax
	add	ebx, 1
	call	_ZNSt8__detail15_List_node_base7_M_hookEPS0_
	add	QWORD PTR 64[rsp], 1
	cmp	ebx, 100
	jne	.L2
	mov	rbx, QWORD PTR 48[rsp]
	cmp	rbx, rsi
	je	.L3
	mov	rax, rbx
	xor	edx, edx
	.p2align 4
	.p2align 4
	.p2align 3
.L4:
	add	edx, DWORD PTR 16[rax]
	mov	rax, QWORD PTR [rax]
	cmp	rax, rsi
	jne	.L4
	mov	DWORD PTR 44[rsp], edx
	mov	eax, DWORD PTR 44[rsp]
	.p2align 4
	.p2align 3
.L5:
	mov	rcx, rbx
	mov	rbx, QWORD PTR [rbx]
	mov	edx, 24
	call	_ZdlPvy
	cmp	rbx, rsi
	jne	.L5
.L14:
	xor	eax, eax
	add	rsp, 80
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L3:
	xor	eax, eax
	mov	DWORD PTR 44[rsp], eax
	mov	eax, DWORD PTR 44[rsp]
	jmp	.L14
.L10:
	mov	rdi, rax
	jmp	.L6
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1400:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1400-.LLSDACSB1400
.LLSDACSB1400:
	.uleb128 .LEHB0-.LFB1400
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L10-.LFB1400
	.uleb128 0
.LLSDACSE1400:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 80
	.seh_savereg	rsi, 88
	.seh_savereg	rdi, 96
	.seh_endprologue
main.cold:
.L6:
	mov	rcx, QWORD PTR 48[rsp]
.L7:
	cmp	rcx, rsi
	je	.L16
	mov	rbx, QWORD PTR [rcx]
	mov	edx, 24
	call	_ZdlPvy
	mov	rcx, rbx
	jmp	.L7
.L16:
	mov	rcx, rdi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC1400:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC1400-.LLSDACSBC1400
.LLSDACSBC1400:
	.uleb128 .LEHB1-.LCOLDB0
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSEC1400:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.section	.text.startup,"x"
.LHOTE0:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt8__detail15_List_node_base7_M_hookEPS0_;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
