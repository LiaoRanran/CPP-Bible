	.file	"_ch136_meyers_guard.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB4701:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv:
.LFB7082:
	.seh_endprologue
	mov	edx, DWORD PTR 8[rcx]
	mov	rax, QWORD PTR 16[rcx]
	mov	ecx, edx
	rex.W jmp	rax
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev:
.LFB7080:
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev:
.LFB7081:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 40[rsp], rcx
	call	_ZNSt6thread6_StateD2Ev
	mov	rcx, QWORD PTR 40[rsp]
	mov	edx, 24
	add	rsp, 56
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.def	__tcf_ZZN6Logger8instanceEvE4inst;	.scl	3;	.type	32;	.endef
	.seh_proc	__tcf_ZZN6Logger8instanceEvE4inst
__tcf_ZZN6Logger8instanceEvE4inst:
.LFB5473:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rsi, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16]
	mov	rbx, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+8]
	cmp	rsi, rbx
	je	.L7
	.p2align 4
	.p2align 3
.L9:
	mov	rcx, QWORD PTR [rbx]
	lea	rax, 16[rbx]
	cmp	rcx, rax
	je	.L8
	mov	rax, QWORD PTR 16[rbx]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L8:
	add	rbx, 32
	cmp	rsi, rbx
	jne	.L9
	mov	rbx, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+8]
.L7:
	test	rbx, rbx
	je	.L6
	mov	rdx, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+24]
	mov	rcx, rbx
	sub	rdx, rbx
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L6:
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section	.text$_ZNSt7__cxx119to_stringEi,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt7__cxx119to_stringEi
	.def	_ZNSt7__cxx119to_stringEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx119to_stringEi
_ZNSt7__cxx119to_stringEi:
.LFB1682:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 256
	.seh_stackalloc	256
	.seh_endprologue
	mov	r10d, edx
	mov	r9, rcx
	mov	esi, edx
	mov	ecx, edx
	neg	r10d
	cmovs	r10d, edx
	shr	ecx, 31
	shr	esi, 31
	cmp	r10d, 9
	jbe	.L13
	mov	eax, r10d
	mov	r8d, 1
	mov	ebx, 3518437209
	jmp	.L19
	.p2align 4,,10
	.p2align 3
.L14:
	cmp	eax, 999
	jbe	.L28
	cmp	eax, 9999
	jbe	.L29
	mov	edx, eax
	lea	r11d, 4[r8]
	imul	rdx, rbx
	shr	rdx, 45
	cmp	eax, 99999
	jbe	.L18
	mov	r8d, r11d
	mov	eax, edx
.L19:
	cmp	eax, 99
	ja	.L14
	lea	r11d, 1[r8]
.L15:
	lea	rax, 16[r9]
	lea	ebx, [r11+rcx]
	mov	BYTE PTR 16[r9], 0
	mov	QWORD PTR [r9], rax
	mov	QWORD PTR 8[r9], 0
	cmp	rbx, 15
	jbe	.L21
	cmp	rbx, 29
	jbe	.L26
	lea	rcx, 1[rbx]
	mov	rdi, rbx
.L22:
	mov	QWORD PTR 288[rsp], r9
	mov	DWORD PTR 44[rsp], r10d
	mov	DWORD PTR 40[rsp], r8d
	call	_Znwy
	mov	r10d, DWORD PTR 44[rsp]
	mov	r8d, DWORD PTR 40[rsp]
	mov	r9, QWORD PTR 288[rsp]
	mov	BYTE PTR [rax], 0
	mov	QWORD PTR [r9], rax
	mov	QWORD PTR 16[r9], rdi
.L21:
	movabs	rdx, 3976738051646829616
	mov	BYTE PTR [rax], 45
	lea	rcx, [rax+rsi]
	movabs	rax, 3688503277381496880
	mov	QWORD PTR 48[rsp], rax
	movabs	rax, 3544667369688283184
	mov	QWORD PTR 56[rsp], rdx
	movabs	rdx, 3832902143785906737
	mov	QWORD PTR 64[rsp], rax
	movabs	rax, 4121136918051239473
	mov	QWORD PTR 72[rsp], rdx
	movabs	rdx, 3689066235924983858
	mov	QWORD PTR 80[rsp], rax
	movabs	rax, 3977301010190316594
	mov	QWORD PTR 88[rsp], rdx
	movabs	rdx, 3545230328231770162
	mov	QWORD PTR 96[rsp], rax
	movabs	rax, 3833465102329393715
	mov	QWORD PTR 104[rsp], rdx
	movabs	rdx, 4121699876594726451
	mov	QWORD PTR 112[rsp], rax
	movabs	rax, 3689629194468470836
	mov	QWORD PTR 120[rsp], rdx
	movabs	rdx, 3977863968733803572
	mov	QWORD PTR 128[rsp], rax
	movabs	rax, 3545793286775257140
	mov	QWORD PTR 136[rsp], rdx
	movabs	rdx, 3834028060872880693
	mov	QWORD PTR 144[rsp], rax
	movabs	rax, 4122262835138213429
	mov	QWORD PTR 152[rsp], rdx
	movabs	rdx, 3690192153011957814
	mov	QWORD PTR 160[rsp], rax
	movabs	rax, 3978426927277290550
	mov	QWORD PTR 168[rsp], rdx
	movabs	rdx, 3546356245318744118
	mov	QWORD PTR 176[rsp], rax
	movabs	rax, 3834591019416367671
	mov	QWORD PTR 184[rsp], rdx
	movabs	rdx, 4122825793681700407
	mov	QWORD PTR 192[rsp], rax
	movabs	rax, 3690755111555444792
	mov	QWORD PTR 200[rsp], rdx
	movabs	rdx, 3978989885820777528
	mov	QWORD PTR 208[rsp], rax
	movabs	rax, 3546919203862231096
	mov	QWORD PTR 216[rsp], rdx
	movabs	rdx, 3835153977959854649
	mov	QWORD PTR 232[rsp], rdx
	movabs	rdx, 16106987313379638
	mov	QWORD PTR 224[rsp], rax
	movabs	rax, 4122263930388298034
	mov	QWORD PTR 233[rsp], rax
	mov	QWORD PTR 241[rsp], rdx
	cmp	r10d, 99
	jbe	.L23
	.p2align 4
	.p2align 3
.L24:
	mov	edx, r10d
	mov	eax, r10d
	imul	rdx, rdx, 1374389535
	shr	rdx, 37
	imul	r11d, edx, 100
	sub	eax, r11d
	mov	r11d, r10d
	mov	r10d, edx
	mov	edx, r8d
	add	eax, eax
	lea	esi, 1[rax]
	movzx	eax, BYTE PTR 48[rsp+rax]
	movzx	esi, BYTE PTR 48[rsp+rsi]
	mov	BYTE PTR [rcx+rdx], sil
	lea	edx, -1[r8]
	sub	r8d, 2
	mov	BYTE PTR [rcx+rdx], al
	cmp	r11d, 9999
	ja	.L24
	cmp	r11d, 999
	ja	.L23
.L20:
	add	r10d, 48
.L25:
	mov	BYTE PTR [rcx], r10b
	mov	rax, QWORD PTR [r9]
	mov	QWORD PTR 8[r9], rbx
	mov	BYTE PTR [rax+rbx], 0
	mov	rax, r9
	add	rsp, 256
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L23:
	add	r10d, r10d
	lea	eax, 1[r10]
	movzx	r10d, BYTE PTR 48[rsp+r10]
	movzx	eax, BYTE PTR 48[rsp+rax]
	mov	BYTE PTR 1[rcx], al
	jmp	.L25
	.p2align 4,,10
	.p2align 3
.L28:
	lea	r11d, 2[r8]
	add	r8d, 1
	jmp	.L15
	.p2align 4,,10
	.p2align 3
.L29:
	lea	r11d, 3[r8]
	add	r8d, 2
	jmp	.L15
	.p2align 4,,10
	.p2align 3
.L18:
	add	r8d, 3
	jmp	.L15
	.p2align 4,,10
	.p2align 3
.L26:
	mov	edi, 30
	mov	ecx, 31
	jmp	.L22
.L13:
	lea	rax, 16[r9]
	lea	ebx, 1[rcx]
	mov	BYTE PTR 16[r9], 45
	mov	QWORD PTR [r9], rax
	lea	rcx, [rax+rsi]
	jmp	.L20
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1682:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1682-.LLSDACSB1682
.LLSDACSB1682:
.LLSDACSE1682:
	.section	.text$_ZNSt7__cxx119to_stringEi,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZN6Logger8instanceEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN6Logger8instanceEv
	.def	_ZN6Logger8instanceEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6Logger8instanceEv
_ZN6Logger8instanceEv:
.LFB5444:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	movzx	eax, BYTE PTR _ZGVZN6Logger8instanceEvE4inst[rip]
	test	al, al
	je	.L37
.L32:
	lea	rax, _ZZN6Logger8instanceEvE4inst[rip]
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L37:
	lea	rcx, _ZGVZN6Logger8instanceEvE4inst[rip]
	call	__cxa_guard_acquire
	test	eax, eax
	je	.L32
	lea	rcx, __tcf_ZZN6Logger8instanceEvE4inst[rip]
	call	atexit
	lea	rcx, _ZGVZN6Logger8instanceEvE4inst[rip]
	call	__cxa_guard_release
	lea	rax, _ZZN6Logger8instanceEvE4inst[rip]
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorISt6threadSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	.def	_ZNSt6vectorISt6threadSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt6threadSaIS0_EED1Ev
_ZNSt6vectorISt6threadSaIS0_EED1Ev:
.LFB6058:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	mov	r8, rcx
	mov	rcx, QWORD PTR [rcx]
	cmp	rdx, rcx
	je	.L39
	mov	rax, rcx
	.p2align 4
	.p2align 4
	.p2align 3
.L41:
	cmp	QWORD PTR [rax], 0
	jne	.L44
	add	rax, 8
	cmp	rdx, rax
	jne	.L41
.L39:
	test	rcx, rcx
	je	.L38
	mov	rdx, QWORD PTR 16[r8]
	sub	rdx, rcx
	add	rsp, 40
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L38:
	add	rsp, 40
	ret
.L44:
	call	_ZSt9terminatev
	nop
	.seh_endproc
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv:
.LFB6085:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L45
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L45:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "basic_string::_M_replace\0"
.LC1:
	.ascii "worker-\0"
.LC2:
	.ascii "vector::_M_realloc_append\0"
	.section	.text.unlikely,"x"
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4
	.globl	_Z6workeri
	.def	_Z6workeri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6workeri
_Z6workeri:
.LFB5475:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	r13
	.seh_pushreg	r13
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
	sub	rsp, 152
	.seh_stackalloc	152
	.seh_endprologue
	movzx	eax, BYTE PTR _ZGVZN6Logger8instanceEvE4inst[rip]
	mov	ebx, ecx
	test	al, al
	je	.L150
.L49:
	lea	rdi, 80[rsp]
	mov	edx, ebx
	mov	rcx, rdi
	call	_ZNSt7__cxx119to_stringEi
	mov	r8, QWORD PTR 88[rsp]
	movabs	rax, -9223372036854775800
	add	rax, r8
	cmp	rax, 6
	jbe	.L143
	mov	rsi, QWORD PTR 80[rsp]
	lea	rbx, 96[rsp]
	lea	rbp, 7[r8]
	cmp	rsi, rbx
	je	.L151
	mov	rax, QWORD PTR 96[rsp]
	cmp	rax, rbp
	jb	.L54
.L52:
	lea	r9, .LC1[rip]
	cmp	r9, rsi
	jnb	.L152
	test	r8, r8
	jne	.L57
.L58:
	mov	DWORD PTR [rsi], 1802661751
	mov	DWORD PTR 3[rsi], 762471787
	mov	r9, QWORD PTR 80[rsp]
.L59:
	mov	QWORD PTR 88[rsp], rbp
	lea	rsi, 128[rsp]
	mov	BYTE PTR [r9+rbp], 0
	mov	rax, QWORD PTR 80[rsp]
	mov	QWORD PTR 112[rsp], rsi
	mov	rbp, QWORD PTR 88[rsp]
	cmp	rax, rbx
	je	.L153
	mov	QWORD PTR 112[rsp], rax
	mov	rax, QWORD PTR 96[rsp]
	mov	QWORD PTR 128[rsp], rax
.L71:
	mov	rax, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16]
	mov	rdx, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+24]
	mov	QWORD PTR 120[rsp], rbp
	add	DWORD PTR _ZZN6Logger8instanceEvE4inst[rip], 1
	mov	QWORD PTR 80[rsp], rbx
	mov	r9, rax
	mov	QWORD PTR 88[rsp], 0
	mov	BYTE PTR 96[rsp], 0
	cmp	rax, rdx
	je	.L72
	lea	rcx, 16[rax]
	mov	QWORD PTR [rax], rcx
	mov	rdx, QWORD PTR 112[rsp]
	cmp	rdx, rsi
	je	.L73
	mov	QWORD PTR [rax], rdx
	mov	rdx, QWORD PTR 128[rsp]
	mov	QWORD PTR 16[rax], rdx
	mov	r9, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16]
.L74:
	add	r9, 32
	mov	QWORD PTR 8[rax], rbp
	mov	QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16], r9
.L81:
	mov	rcx, QWORD PTR 80[rsp]
	cmp	rcx, rbx
	je	.L47
	mov	rax, QWORD PTR 96[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	nop
.L47:
	add	rsp, 152
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L57:
	cmp	r8, 1
	je	.L154
	lea	rcx, 7[rsi]
	mov	rdx, rsi
	call	memmove
	jmp	.L58
	.p2align 4,,10
	.p2align 3
.L152:
	lea	rax, [rsi+r8]
	cmp	rax, r9
	jnb	.L56
	test	r8, r8
	jne	.L57
	jmp	.L58
	.p2align 4,,10
	.p2align 3
.L150:
	lea	rcx, _ZGVZN6Logger8instanceEvE4inst[rip]
	call	__cxa_guard_acquire
	test	eax, eax
	je	.L49
	lea	rcx, __tcf_ZZN6Logger8instanceEvE4inst[rip]
	call	atexit
	lea	rcx, _ZGVZN6Logger8instanceEvE4inst[rip]
	call	__cxa_guard_release
	jmp	.L49
	.p2align 4,,10
	.p2align 3
.L72:
	mov	r10, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+8]
	mov	r8, rax
	movabs	rax, 288230376151711743
	sub	r8, r10
	mov	rcx, r8
	sar	rcx, 5
	cmp	rcx, rax
	je	.L144
	test	rcx, rcx
	mov	eax, 1
	mov	QWORD PTR 72[rsp], r9
	cmovne	rax, rcx
	mov	QWORD PTR 64[rsp], r8
	mov	QWORD PTR 56[rsp], r10
	add	rax, rcx
	mov	QWORD PTR 48[rsp], rdx
	movabs	rcx, 288230376151711743
	cmp	rax, rcx
	cmova	rax, rcx
	sal	rax, 5
	mov	rcx, rax
	mov	r15, rax
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r8, QWORD PTR 64[rsp]
	mov	rcx, QWORD PTR 112[rsp]
	mov	rdi, rax
	mov	rdx, QWORD PTR 48[rsp]
	mov	r10, QWORD PTR 56[rsp]
	lea	rax, [rax+r8]
	cmp	rcx, rsi
	mov	r9, QWORD PTR 72[rsp]
	lea	r8, 16[rax]
	mov	QWORD PTR [rax], r8
	je	.L83
	mov	QWORD PTR [rax], rcx
	mov	rcx, QWORD PTR 128[rsp]
	mov	QWORD PTR 16[rax], rcx
.L84:
	mov	QWORD PTR 8[rax], rbp
	mov	QWORD PTR 112[rsp], rsi
	mov	QWORD PTR 120[rsp], 0
	mov	BYTE PTR 128[rsp], 0
	cmp	r9, r10
	je	.L109
	lea	r8, 16[r10]
	mov	rcx, r10
	mov	rax, rdi
	mov	r12, rdi
	mov	rdi, rbx
	mov	rbx, r10
	mov	r10, rdx
	mov	rdx, r9
	jmp	.L100
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L92:
	mov	QWORD PTR [rax], r11
	mov	r11, QWORD PTR 16[rcx]
	mov	QWORD PTR 16[rax], r11
.L149:
	mov	r11, QWORD PTR 8[rcx]
.L99:
	add	rcx, 32
	mov	QWORD PTR 8[rax], r11
	add	r8, 32
	add	rax, 32
	cmp	rdx, rcx
	je	.L155
.L100:
	lea	rbp, 16[rax]
	mov	QWORD PTR [rax], rbp
	mov	r11, QWORD PTR [rcx]
	cmp	r11, r8
	jne	.L92
	mov	r11, QWORD PTR 8[rcx]
	lea	r9, 1[r11]
	cmp	r9d, 8
	jnb	.L93
	test	r9b, 4
	jne	.L156
	test	r9d, r9d
	je	.L99
	movzx	r11d, BYTE PTR [r8]
	mov	BYTE PTR 0[rbp], r11b
	test	r9b, 2
	je	.L149
	mov	r9d, r9d
	movzx	r11d, WORD PTR -2[r8+r9]
	mov	WORD PTR -2[rbp+r9], r11w
	mov	r11, QWORD PTR 8[rcx]
	jmp	.L99
	.p2align 4,,10
	.p2align 3
.L155:
	mov	rdx, r10
	mov	r10, rbx
	mov	rbx, rdi
	mov	rdi, r12
.L91:
	lea	rbp, 32[rax]
	test	r10, r10
	je	.L101
	mov	rcx, r10
	sub	rdx, r10
	call	_ZdlPvy
	mov	rcx, QWORD PTR 112[rsp]
	mov	QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+8], rdi
	add	rdi, r15
	mov	QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16], rbp
	mov	QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+24], rdi
	cmp	rcx, rsi
	je	.L81
	mov	rax, QWORD PTR 128[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L81
	.p2align 4,,10
	.p2align 3
.L54:
	add	rax, rax
	mov	r15, rax
	cmp	rbp, rax
	jb	.L61
	lea	rcx, 8[r8]
	mov	r15, rbp
.L62:
	mov	QWORD PTR 56[rsp], r8
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	DWORD PTR [rax], 1802661751
	mov	r8, QWORD PTR 56[rsp]
	lea	rcx, 7[rax]
	mov	rdx, rsi
	mov	DWORD PTR 3[rax], 762471787
	mov	QWORD PTR 48[rsp], rax
	call	memcpy
	cmp	rsi, rbx
	mov	r9, QWORD PTR 48[rsp]
	je	.L63
	mov	rax, QWORD PTR 96[rsp]
	mov	rcx, rsi
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r9, QWORD PTR 48[rsp]
.L63:
	mov	QWORD PTR 80[rsp], r9
	mov	QWORD PTR 96[rsp], r15
	jmp	.L59
	.p2align 4,,10
	.p2align 3
.L93:
	mov	r11, QWORD PTR [r8]
	mov	QWORD PTR 0[rbp], r11
	mov	r11d, r9d
	mov	r14, QWORD PTR -8[r8+r11]
	mov	QWORD PTR -8[rbp+r11], r14
	lea	r11, 24[rax]
	mov	r14, r8
	and	r11, -8
	sub	rbp, r11
	add	r9d, ebp
	sub	r14, rbp
	and	r9d, -8
	mov	r13, r14
	cmp	r9d, 8
	jb	.L149
	and	r9d, -8
	mov	QWORD PTR 48[rsp], rdi
	xor	ebp, ebp
	mov	rdi, rsi
	mov	rsi, rax
	mov	rax, r11
	mov	r11, rdx
	mov	edx, r9d
.L97:
	mov	r9d, ebp
	add	ebp, 8
	mov	r14, QWORD PTR 0[r13+r9]
	mov	QWORD PTR [rax+r9], r14
	cmp	ebp, edx
	jb	.L97
	mov	rax, rsi
	mov	rdx, r11
	mov	rsi, rdi
	mov	r11, QWORD PTR 8[rcx]
	mov	rdi, QWORD PTR 48[rsp]
	jmp	.L99
	.p2align 4,,10
	.p2align 3
.L61:
	movabs	rax, 9223372036854775806
	lea	rcx, 1[r15]
	cmp	rax, r15
	jnb	.L62
	movabs	rcx, 9223372036854775807
	mov	r15, rax
	jmp	.L62
	.p2align 4,,10
	.p2align 3
.L151:
	mov	ecx, 31
	mov	r15d, 30
	cmp	rbp, 15
	jbe	.L52
	jmp	.L62
	.p2align 4,,10
	.p2align 3
.L153:
	lea	rax, 1[rbp]
	mov	r8, rsi
	mov	rdx, rbx
	cmp	eax, 8
	jnb	.L157
.L65:
	xor	ecx, ecx
	test	al, 4
	je	.L68
	mov	ecx, DWORD PTR [rdx]
	mov	DWORD PTR [r8], ecx
	mov	ecx, 4
.L68:
	test	al, 2
	je	.L69
	movzx	r9d, WORD PTR [rdx+rcx]
	mov	WORD PTR [r8+rcx], r9w
	add	rcx, 2
.L69:
	test	al, 1
	je	.L71
	movzx	eax, BYTE PTR [rdx+rcx]
	mov	BYTE PTR [r8+rcx], al
	jmp	.L71
	.p2align 4,,10
	.p2align 3
.L73:
	lea	rdx, 1[rbp]
	cmp	edx, 8
	jnb	.L75
	test	dl, 4
	jne	.L158
	test	edx, edx
	je	.L74
	movzx	r8d, BYTE PTR [rsi]
	mov	BYTE PTR 16[rax], r8b
	mov	r9, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16]
	test	dl, 2
	je	.L74
	mov	edx, edx
	movzx	r8d, WORD PTR -2[rsi+rdx]
	mov	WORD PTR -2[rcx+rdx], r8w
	mov	r9, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16]
	jmp	.L74
	.p2align 4,,10
	.p2align 3
.L154:
	movzx	eax, BYTE PTR [rsi]
	mov	BYTE PTR 7[rsi], al
	jmp	.L58
	.p2align 4,,10
	.p2align 3
.L157:
	mov	r8d, eax
	xor	edx, edx
	and	r8d, -8
.L66:
	mov	ecx, edx
	add	edx, 8
	mov	r9, QWORD PTR [rbx+rcx]
	mov	QWORD PTR [rsi+rcx], r9
	cmp	edx, r8d
	jb	.L66
	lea	r8, [rsi+rdx]
	add	rdx, rbx
	jmp	.L65
	.p2align 4,,10
	.p2align 3
.L75:
	mov	r8, QWORD PTR [rsi]
	mov	QWORD PTR 16[rax], r8
	mov	r8d, edx
	mov	r9, QWORD PTR -8[rsi+r8]
	mov	QWORD PTR -8[rcx+r8], r9
	lea	r8, 24[rax]
	and	r8, -8
	sub	rcx, r8
	add	edx, ecx
	sub	rsi, rcx
	and	edx, -8
	cmp	edx, 8
	jb	.L148
	and	edx, -8
	xor	ecx, ecx
.L79:
	mov	r9d, ecx
	add	ecx, 8
	mov	r10, QWORD PTR [rsi+r9]
	mov	QWORD PTR [r8+r9], r10
	cmp	ecx, edx
	jb	.L79
.L148:
	mov	r9, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16]
	jmp	.L74
	.p2align 4,,10
	.p2align 3
.L83:
	lea	rcx, 1[rbp]
	cmp	ecx, 8
	jnb	.L85
	test	cl, 4
	jne	.L159
	test	ecx, ecx
	je	.L84
	movzx	r11d, BYTE PTR [rsi]
	mov	BYTE PTR 16[rax], r11b
	test	cl, 2
	je	.L84
	mov	ecx, ecx
	movzx	r11d, WORD PTR -2[rsi+rcx]
	mov	WORD PTR -2[r8+rcx], r11w
	jmp	.L84
.L101:
	mov	QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+8], rdi
	add	rdi, r15
	mov	QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16], rbp
	mov	QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+24], rdi
	jmp	.L81
	.p2align 4,,10
	.p2align 3
.L85:
	mov	r11, QWORD PTR [rsi]
	mov	QWORD PTR 16[rax], r11
	mov	r11d, ecx
	mov	r14, QWORD PTR -8[rsi+r11]
	mov	QWORD PTR -8[r8+r11], r14
	lea	r11, 24[rax]
	mov	r14, rsi
	and	r11, -8
	sub	r8, r11
	add	ecx, r8d
	sub	r14, r8
	and	ecx, -8
	mov	r13, r14
	cmp	ecx, 8
	jb	.L84
	mov	r12, rdi
	and	ecx, -8
	mov	rdi, r9
	xor	r8d, r8d
	mov	r9, rdx
	mov	rdx, rbx
	mov	rbx, r10
	mov	r10, rax
.L89:
	mov	eax, r8d
	add	r8d, 8
	mov	r14, QWORD PTR 0[r13+rax]
	mov	QWORD PTR [r11+rax], r14
	cmp	r8d, ecx
	jb	.L89
	mov	rax, r10
	mov	r10, rbx
	mov	rbx, rdx
	mov	rdx, r9
	mov	r9, rdi
	mov	rdi, r12
	jmp	.L84
.L156:
	mov	r11d, DWORD PTR [r8]
	mov	r9d, r9d
	mov	DWORD PTR 0[rbp], r11d
	mov	r11d, DWORD PTR -4[r8+r9]
	mov	DWORD PTR -4[rbp+r9], r11d
	mov	r11, QWORD PTR 8[rcx]
	jmp	.L99
	.p2align 4,,10
	.p2align 3
.L109:
	mov	rax, rdi
	jmp	.L91
.L158:
	mov	r8d, DWORD PTR [rsi]
	mov	edx, edx
	mov	DWORD PTR 16[rax], r8d
	mov	r8d, DWORD PTR -4[rsi+rdx]
	mov	DWORD PTR -4[rcx+rdx], r8d
	mov	r9, QWORD PTR _ZZN6Logger8instanceEvE4inst[rip+16]
	jmp	.L74
.L159:
	mov	r11d, DWORD PTR [rsi]
	mov	ecx, ecx
	mov	DWORD PTR 16[rax], r11d
	mov	r11d, DWORD PTR -4[rsi+rcx]
	mov	DWORD PTR -4[r8+rcx], r11d
	jmp	.L84
.L139:
	jmp	.L140
.L141:
	jmp	.L142
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5475:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5475-.LLSDACSB5475
.LLSDACSB5475:
	.uleb128 .LEHB0-.LFB5475
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L141-.LFB5475
	.uleb128 0
	.uleb128 .LEHB1-.LFB5475
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L139-.LFB5475
	.uleb128 0
.LLSDACSE5475:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z6workeri.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z6workeri.cold
	.seh_stackalloc	216
	.seh_savereg	rbx, 152
	.seh_savereg	rsi, 160
	.seh_savereg	rdi, 168
	.seh_savereg	rbp, 176
	.seh_savereg	r12, 184
	.seh_savereg	r13, 192
	.seh_savereg	r14, 200
	.seh_savereg	r15, 208
	.seh_endprologue
_Z6workeri.cold:
.L56:
	mov	QWORD PTR 40[rsp], r8
	mov	rdx, rsi
	xor	r8d, r8d
	mov	rcx, rdi
	mov	QWORD PTR 32[rsp], 7
.LEHB2:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy
	mov	r9, QWORD PTR 80[rsp]
	jmp	.L59
.L143:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE2:
.L144:
	lea	rcx, .LC2[rip]
.LEHB3:
	call	_ZSt20__throw_length_errorPKc
.LEHE3:
.L111:
.L142:
	lea	rcx, 112[rsp]
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L105:
	mov	rcx, rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
.LEHE4:
.L110:
.L140:
	mov	rbx, rax
	jmp	.L105
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5475:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5475-.LLSDACSBC5475
.LLSDACSBC5475:
	.uleb128 .LEHB2-.LCOLDB3
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L110-.LCOLDB3
	.uleb128 0
	.uleb128 .LEHB3-.LCOLDB3
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L111-.LCOLDB3
	.uleb128 0
	.uleb128 .LEHB4-.LCOLDB3
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSEC5475:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.text
.LHOTE3:
	.section	.text$_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	.def	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev:
.LFB6807:
	.seh_endprologue
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L160
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 8[rax]]
	.p2align 4,,10
	.p2align 3
.L160:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC4:
	.ascii "lines=\0"
.LC5:
	.ascii " count=\0"
.LC6:
	.ascii "\12\0"
	.section	.text.unlikely,"x"
.LCOLDB7:
	.section	.text.startup,"x"
.LHOTB7:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5476:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	r13
	.seh_pushreg	r13
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
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	xor	r12d, r12d
	xor	ebx, ebx
	xor	ebp, ebp
	xor	esi, esi
	lea	r13, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE[rip+16]
	lea	r14, _Z6workeri[rip]
	lea	r15, _ZNSt6thread24_M_thread_deps_never_runEv[rip]
	call	__main
	lea	rax, 64[rsp]
	mov	QWORD PTR 40[rsp], rax
	jmp	.L176
	.p2align 4,,10
	.p2align 3
.L225:
	mov	QWORD PTR [rbx], 0
	mov	ecx, 24
.LEHB5:
	call	_Znwy
.LEHE5:
	mov	QWORD PTR [rax], r13
	mov	rdx, QWORD PTR 40[rsp]
	mov	r8, r15
	mov	rcx, rbx
	mov	DWORD PTR 8[rax], esi
	mov	QWORD PTR 16[rax], r14
	mov	QWORD PTR 64[rsp], rax
.LEHB6:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE6:
	mov	rcx, QWORD PTR 64[rsp]
	test	rcx, rcx
	je	.L164
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
.L164:
	add	esi, 1
	add	rbx, 8
	cmp	esi, 4
	je	.L224
.L176:
	cmp	rbx, r12
	jne	.L225
	movabs	rax, 1152921504606846975
	mov	r9, rbx
	sub	r9, rbp
	mov	rdx, r9
	sar	rdx, 3
	cmp	rdx, rax
	je	.L219
	test	rdx, rdx
	mov	eax, 1
	mov	QWORD PTR 56[rsp], r9
	cmovne	rax, rdx
	add	rax, rdx
	movabs	rdx, 1152921504606846975
	cmp	rax, rdx
	cmova	rax, rdx
	sal	rax, 3
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], rax
.LEHB7:
	call	_Znwy
.LEHE7:
	mov	r9, QWORD PTR 56[rsp]
	mov	ecx, 24
	mov	rdi, rax
	add	r9, rax
	mov	QWORD PTR [r9], 0
	mov	QWORD PTR 56[rsp], r9
.LEHB8:
	call	_Znwy
.LEHE8:
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, QWORD PTR 56[rsp]
	mov	QWORD PTR [rax], r13
	mov	r8, r15
	mov	DWORD PTR 8[rax], esi
	mov	QWORD PTR 16[rax], r14
	mov	QWORD PTR 64[rsp], rax
.LEHB9:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE9:
	mov	rcx, QWORD PTR 64[rsp]
	test	rcx, rcx
	je	.L169
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
.L169:
	cmp	rbx, rbp
	je	.L226
	sub	rbx, rbp
	mov	rdx, rbp
	mov	rax, rdi
	add	rbx, rdi
	.p2align 5
	.p2align 4
	.p2align 3
.L174:
	mov	rcx, QWORD PTR [rdx]
	add	rax, 8
	add	rdx, 8
	mov	QWORD PTR -8[rax], rcx
	cmp	rbx, rax
	jne	.L174
.L171:
	add	rbx, 8
	test	rbp, rbp
	je	.L175
	mov	rdx, r12
	mov	rcx, rbp
	sub	rdx, rbp
	call	_ZdlPvy
.L175:
	mov	r12, QWORD PTR 48[rsp]
	add	esi, 1
	mov	rbp, rdi
	add	r12, rdi
	cmp	esi, 4
	jne	.L176
.L224:
	mov	rsi, rbp
	cmp	rbx, rbp
	je	.L181
	.p2align 4
	.p2align 3
.L180:
	mov	rcx, rsi
.LEHB10:
	call	_ZNSt6thread4joinEv
	add	rsi, 8
	cmp	rbx, rsi
	jne	.L180
.L181:
	call	_ZN6Logger8instanceEv
	lea	rdi, 80[rsp]
	mov	BYTE PTR 84[rsp], 0
	mov	DWORD PTR 80[rsp], 1701736292
	mov	r14, rax
	mov	r13, QWORD PTR 16[rax]
	mov	QWORD PTR 64[rsp], rdi
	mov	QWORD PTR 72[rsp], 4
	add	DWORD PTR [rax], 1
	cmp	r13, QWORD PTR 24[rax]
	je	.L227
	lea	rdx, 16[r13]
	mov	QWORD PTR 0[r13], rdx
	mov	rax, QWORD PTR 64[rsp]
	cmp	rax, rdi
	je	.L182
	mov	QWORD PTR 0[r13], rax
	mov	rax, QWORD PTR 80[rsp]
	mov	QWORD PTR 16[r13], rax
.L183:
	mov	QWORD PTR 8[r13], 4
	mov	QWORD PTR 64[rsp], rdi
	mov	QWORD PTR 72[rsp], 0
	mov	BYTE PTR 80[rsp], 0
	add	QWORD PTR 16[r14], 32
.L184:
	mov	rdi, QWORD PTR 40[rsp]
	mov	rcx, rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC4[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rsi, rax
	call	_ZN6Logger8instanceEv
	mov	rcx, rsi
	mov	rdx, QWORD PTR 16[rax]
	sub	rdx, QWORD PTR 8[rax]
	sar	rdx, 5
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC5[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rsi, rax
	call	_ZN6Logger8instanceEv
	mov	rcx, rsi
	mov	edx, DWORD PTR [rax]
	call	_ZNSolsEi
	lea	rdx, .LC6[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE10:
	mov	rcx, rdi
	mov	QWORD PTR 64[rsp], rbp
	mov	QWORD PTR 72[rsp], rbx
	mov	QWORD PTR 80[rsp], r12
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	xor	eax, eax
	add	rsp, 104
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L227:
	mov	r15, QWORD PTR 8[rax]
	mov	rsi, r13
	movabs	rax, 288230376151711743
	sub	rsi, r15
	mov	rcx, rsi
	sar	rcx, 5
	cmp	rcx, rax
	je	.L220
	test	rcx, rcx
	mov	eax, 1
	cmovne	rax, rcx
	add	rax, rcx
	movabs	rcx, 288230376151711743
	cmp	rax, rcx
	cmova	rax, rcx
	sal	rax, 5
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], rax
.LEHB11:
	call	_Znwy
.LEHE11:
	mov	ecx, DWORD PTR 80[rsp]
	mov	r10, rax
	lea	rax, 16[rax+rsi]
	mov	QWORD PTR 64[rsp], rdi
	mov	QWORD PTR [r10+rsi], rax
	xor	eax, eax
	mov	DWORD PTR 16[r10+rsi], ecx
	movzx	ecx, BYTE PTR 84[rsp]
	mov	QWORD PTR 8[r10+rsi], 4
	mov	BYTE PTR 20[r10+rsi], cl
	mov	QWORD PTR 72[rsp], rax
	mov	BYTE PTR 80[rsp], 0
	cmp	r13, r15
	je	.L192
	lea	r8, 16[r15]
	mov	rdx, r15
	mov	rax, r10
	jmp	.L189
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L187:
	mov	QWORD PTR [rax], rcx
	mov	rcx, QWORD PTR 16[rdx]
	mov	QWORD PTR 16[rax], rcx
.L188:
	mov	rcx, QWORD PTR 8[rdx]
	add	rdx, 32
	add	rax, 32
	add	r8, 32
	mov	QWORD PTR -24[rax], rcx
	cmp	r13, rdx
	je	.L186
.L189:
	lea	r9, 16[rax]
	mov	QWORD PTR [rax], r9
	mov	rcx, QWORD PTR [rdx]
	cmp	rcx, r8
	jne	.L187
	mov	rcx, QWORD PTR 8[rdx]
	mov	rdi, r9
	mov	rsi, r8
	add	ecx, 1
	rep movsb
	jmp	.L188
.L192:
	mov	rax, r10
.L186:
	lea	rdi, 32[rax]
	test	r15, r15
	je	.L190
	mov	rdx, QWORD PTR 24[r14]
	mov	rcx, r15
	mov	QWORD PTR 56[rsp], r10
	sub	rdx, r15
	call	_ZdlPvy
	mov	r10, QWORD PTR 56[rsp]
.L190:
	mov	QWORD PTR 8[r14], r10
	add	r10, QWORD PTR 48[rsp]
	mov	QWORD PTR 16[r14], rdi
	mov	QWORD PTR 24[r14], r10
	jmp	.L184
.L226:
	mov	rbx, rdi
	jmp	.L171
.L182:
	mov	eax, DWORD PTR [rdi]
	mov	DWORD PTR 16[r13], eax
	movzx	eax, BYTE PTR 4[rdi]
	mov	BYTE PTR 4[rdx], al
	jmp	.L183
.L194:
	mov	rsi, rax
	jmp	.L166
.L215:
	jmp	.L216
.L196:
	mov	rsi, rax
	jmp	.L172
.L195:
	mov	rsi, rax
	jmp	.L173
.L217:
	jmp	.L218
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5476:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5476-.LLSDACSB5476
.LLSDACSB5476:
	.uleb128 .LEHB5-.LFB5476
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L217-.LFB5476
	.uleb128 0
	.uleb128 .LEHB6-.LFB5476
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L194-.LFB5476
	.uleb128 0
	.uleb128 .LEHB7-.LFB5476
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L217-.LFB5476
	.uleb128 0
	.uleb128 .LEHB8-.LFB5476
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L195-.LFB5476
	.uleb128 0
	.uleb128 .LEHB9-.LFB5476
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L196-.LFB5476
	.uleb128 0
	.uleb128 .LEHB10-.LFB5476
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L217-.LFB5476
	.uleb128 0
	.uleb128 .LEHB11-.LFB5476
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L215-.LFB5476
	.uleb128 0
.LLSDACSE5476:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	168
	.seh_savereg	rbx, 104
	.seh_savereg	rsi, 112
	.seh_savereg	rdi, 120
	.seh_savereg	rbp, 128
	.seh_savereg	r12, 136
	.seh_savereg	r13, 144
	.seh_savereg	r14, 152
	.seh_savereg	r15, 160
	.seh_endprologue
main.cold:
.L219:
	lea	rcx, .LC2[rip]
.LEHB12:
	call	_ZSt20__throw_length_errorPKc
.LEHE12:
.L220:
	lea	rcx, .LC2[rip]
.LEHB13:
	call	_ZSt20__throw_length_errorPKc
.LEHE13:
.L197:
.L218:
	mov	rsi, rax
	jmp	.L167
.L166:
	mov	rcx, QWORD PTR 40[rsp]
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
.L167:
	mov	rcx, QWORD PTR 40[rsp]
	mov	QWORD PTR 64[rsp], rbp
	mov	QWORD PTR 72[rsp], rbx
	mov	QWORD PTR 80[rsp], r12
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	mov	rcx, rsi
.LEHB14:
	call	_Unwind_Resume
.LEHE14:
.L193:
.L216:
	mov	rcx, QWORD PTR 40[rsp]
	mov	rsi, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	jmp	.L167
.L172:
	mov	rcx, QWORD PTR 40[rsp]
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
.L173:
	mov	rdx, QWORD PTR 48[rsp]
	mov	rcx, rdi
	call	_ZdlPvy
	jmp	.L167
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5476:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5476-.LLSDACSBC5476
.LLSDACSBC5476:
	.uleb128 .LEHB12-.LCOLDB7
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L197-.LCOLDB7
	.uleb128 0
	.uleb128 .LEHB13-.LCOLDB7
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L193-.LCOLDB7
	.uleb128 0
	.uleb128 .LEHB14-.LCOLDB7
	.uleb128 .LEHE14-.LEHB14
	.uleb128 0
	.uleb128 0
.LLSDACSEC5476:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE7:
	.section	.text.startup,"x"
.LHOTE7:
	.globl	_ZTSNSt6thread6_StateE
	.section	.rdata$_ZTSNSt6thread6_StateE,"dr"
	.linkonce same_size
	.align 16
_ZTSNSt6thread6_StateE:
	.ascii "NSt6thread6_StateE\0"
	.globl	_ZTINSt6thread6_StateE
	.section	.rdata$_ZTINSt6thread6_StateE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt6thread6_StateE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSNSt6thread6_StateE
	.globl	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE
	.section	.rdata$_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE,"dr"
	.linkonce same_size
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE:
	.ascii "NSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE\0"
	.globl	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE
	.section	.rdata$_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE
	.quad	_ZTINSt6thread6_StateE
	.globl	_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE
	.section	.rdata$_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFviEiEEEEE6_M_runEv
	.globl	_ZGVZN6Logger8instanceEvE4inst
	.section	.data$_ZGVZN6Logger8instanceEvE4inst,"w"
	.linkonce same_size
	.align 8
_ZGVZN6Logger8instanceEvE4inst:
	.space 8
	.globl	_ZZN6Logger8instanceEvE4inst
	.section	.data$_ZZN6Logger8instanceEvE4inst,"w"
	.linkonce same_size
	.align 32
_ZZN6Logger8instanceEvE4inst:
	.space 32
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	__cxa_guard_acquire;	.scl	2;	.type	32;	.endef
	.def	atexit;	.scl	2;	.type	32;	.endef
	.def	__cxa_guard_release;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE15_M_replace_coldEPcyPKcyy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread4joinEv;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
