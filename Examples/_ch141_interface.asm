	.file	"_ch141_interface.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN13EmailNotifierD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN13EmailNotifierD1Ev
	.def	_ZN13EmailNotifierD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13EmailNotifierD1Ev
_ZN13EmailNotifierD1Ev:
.LFB4130:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN11SmsNotifierD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN11SmsNotifierD1Ev
	.def	_ZN11SmsNotifierD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN11SmsNotifierD1Ev
_ZN11SmsNotifierD1Ev:
.LFB4155:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN13EmailNotifierD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN13EmailNotifierD0Ev
	.def	_ZN13EmailNotifierD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13EmailNotifierD0Ev
_ZN13EmailNotifierD0Ev:
.LFB4131:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZN11SmsNotifierD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN11SmsNotifierD0Ev
	.def	_ZN11SmsNotifierD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN11SmsNotifierD0Ev
_ZN11SmsNotifierD0Ev:
.LFB4156:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "sms:\0"
.LC1:
	.ascii "\12\0"
	.section	.text$_ZN11SmsNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN11SmsNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.def	_ZN11SmsNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN11SmsNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_ZN11SmsNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:
.LFB3553:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	r8d, 4
	mov	rbx, rdx
	lea	rdx, .LC0[rip]
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	rdx, QWORD PTR [rbx]
	mov	r8, QWORD PTR 8[rbx]
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	r8d, 1
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	add	rsp, 32
	pop	rbx
	jmp	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "email:\0"
	.section	.text$_ZN13EmailNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN13EmailNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.def	_ZN13EmailNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13EmailNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_ZN13EmailNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:
.LFB3552:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	r8d, 6
	mov	rbx, rdx
	lea	rdx, .LC2[rip]
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	rdx, QWORD PTR [rbx]
	mov	r8, QWORD PTR 8[rbx]
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	r8d, 1
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	add	rsp, 32
	pop	rbx
	jmp	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	.seh_endproc
	.section	.text$_ZN12OrderService5placeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN12OrderService5placeEv
	.def	_ZN12OrderService5placeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN12OrderService5placeEv
_ZN12OrderService5placeEv:
.LFB3571:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	mov	rcx, QWORD PTR [rcx]
	mov	rax, QWORD PTR [rcx]
	lea	rbx, 48[rsp]
	mov	QWORD PTR 40[rsp], 7
	lea	rdx, 32[rsp]
	mov	QWORD PTR 32[rsp], rbx
	mov	rax, QWORD PTR 16[rax]
	mov	DWORD PTR 48[rsp], 1701081711
	mov	BYTE PTR 55[rsp], 0
	mov	DWORD PTR 51[rsp], 1684370021
.LEHB0:
	call	rax
.LEHE0:
	mov	rcx, QWORD PTR 32[rsp]
	cmp	rcx, rbx
	je	.L8
	mov	rax, QWORD PTR 48[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	nop
.L8:
	add	rsp, 72
	pop	rbx
	pop	rsi
	ret
.L12:
	mov	rcx, QWORD PTR 32[rsp]
	mov	rsi, rax
	cmp	rcx, rbx
	jne	.L13
.L11:
	mov	rcx, rsi
.LEHB1:
	call	_Unwind_Resume
.LEHE1:
.L13:
	mov	rax, QWORD PTR 48[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L11
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3571:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3571-.LLSDACSB3571
.LLSDACSB3571:
	.uleb128 .LEHB0-.LFB3571
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L12-.LFB3571
	.uleb128 0
	.uleb128 .LEHB1-.LFB3571
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE3571:
	.section	.text$_ZN12OrderService5placeEv,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt10unique_ptrI9INotifierSt14default_deleteIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrI9INotifierSt14default_deleteIS0_EED1Ev
	.def	_ZNSt10unique_ptrI9INotifierSt14default_deleteIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrI9INotifierSt14default_deleteIS0_EED1Ev
_ZNSt10unique_ptrI9INotifierSt14default_deleteIS0_EED1Ev:
.LFB3923:
	.seh_endprologue
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L14
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 8[rax]]
	.p2align 4,,10
	.p2align 3
.L14:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3572:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	call	__main
	mov	ecx, 8
.LEHB2:
	call	_Znwy
.LEHE2:
	lea	rdx, _ZTV13EmailNotifier[rip+16]
	mov	ecx, 8
	mov	QWORD PTR [rax], rdx
	mov	QWORD PTR 32[rsp], rax
.LEHB3:
	call	_Znwy
.LEHE3:
	lea	rdi, _ZTV11SmsNotifier[rip+16]
	mov	QWORD PTR 40[rsp], rax
	lea	rsi, 32[rsp]
	mov	QWORD PTR [rax], rdi
	lea	rbx, 40[rsp]
	mov	rcx, rsi
.LEHB4:
	call	_ZN12OrderService5placeEv
	mov	rcx, rbx
	call	_ZN12OrderService5placeEv
.LEHE4:
	mov	rcx, rbx
	call	_ZNSt10unique_ptrI9INotifierSt14default_deleteIS0_EED1Ev
	mov	rcx, rsi
	call	_ZNSt10unique_ptrI9INotifierSt14default_deleteIS0_EED1Ev
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L19:
	lea	rsi, 32[rsp]
	mov	rbx, rax
.L18:
	mov	rcx, rsi
	call	_ZNSt10unique_ptrI9INotifierSt14default_deleteIS0_EED1Ev
	mov	rcx, rbx
.LEHB5:
	call	_Unwind_Resume
.LEHE5:
.L20:
	mov	rdi, rax
	mov	rcx, rbx
	call	_ZNSt10unique_ptrI9INotifierSt14default_deleteIS0_EED1Ev
	mov	rbx, rdi
	jmp	.L18
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3572:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3572-.LLSDACSB3572
.LLSDACSB3572:
	.uleb128 .LEHB2-.LFB3572
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB3-.LFB3572
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L19-.LFB3572
	.uleb128 0
	.uleb128 .LEHB4-.LFB3572
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L20-.LFB3572
	.uleb128 0
	.uleb128 .LEHB5-.LFB3572
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSE3572:
	.section	.text.startup,"x"
	.seh_endproc
	.globl	_ZTS9INotifier
	.section	.rdata$_ZTS9INotifier,"dr"
	.linkonce same_size
	.align 8
_ZTS9INotifier:
	.ascii "9INotifier\0"
	.globl	_ZTI9INotifier
	.section	.rdata$_ZTI9INotifier,"dr"
	.linkonce same_size
	.align 8
_ZTI9INotifier:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS9INotifier
	.globl	_ZTS13EmailNotifier
	.section	.rdata$_ZTS13EmailNotifier,"dr"
	.linkonce same_size
	.align 16
_ZTS13EmailNotifier:
	.ascii "13EmailNotifier\0"
	.globl	_ZTI13EmailNotifier
	.section	.rdata$_ZTI13EmailNotifier,"dr"
	.linkonce same_size
	.align 8
_ZTI13EmailNotifier:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS13EmailNotifier
	.quad	_ZTI9INotifier
	.globl	_ZTS11SmsNotifier
	.section	.rdata$_ZTS11SmsNotifier,"dr"
	.linkonce same_size
	.align 8
_ZTS11SmsNotifier:
	.ascii "11SmsNotifier\0"
	.globl	_ZTI11SmsNotifier
	.section	.rdata$_ZTI11SmsNotifier,"dr"
	.linkonce same_size
	.align 8
_ZTI11SmsNotifier:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS11SmsNotifier
	.quad	_ZTI9INotifier
	.globl	_ZTV13EmailNotifier
	.section	.rdata$_ZTV13EmailNotifier,"dr"
	.linkonce same_size
	.align 8
_ZTV13EmailNotifier:
	.quad	0
	.quad	_ZTI13EmailNotifier
	.quad	_ZN13EmailNotifierD1Ev
	.quad	_ZN13EmailNotifierD0Ev
	.quad	_ZN13EmailNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.globl	_ZTV11SmsNotifier
	.section	.rdata$_ZTV11SmsNotifier,"dr"
	.linkonce same_size
	.align 8
_ZTV11SmsNotifier:
	.quad	0
	.quad	_ZTI11SmsNotifier
	.quad	_ZN11SmsNotifierD1Ev
	.quad	_ZN11SmsNotifierD0Ev
	.quad	_ZN11SmsNotifier4sendERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
