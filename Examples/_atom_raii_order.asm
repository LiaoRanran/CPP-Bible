	.file	"_atom_raii_order.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "ctor \0"
.LC1:
	.ascii "\12\0"
	.section	.text$_ZN3TagC1EPKc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3TagC1EPKc
	.def	_ZN3TagC1EPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3TagC1EPKc
_ZN3TagC1EPKc:
.LFB4076:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	r8d, 5
	mov	QWORD PTR [rcx], rdx
	mov	rsi, rcx
	lea	rdx, .LC0[rip]
	mov	rcx, rbx
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	rsi, QWORD PTR [rsi]
	test	rsi, rsi
	je	.L5
	mov	rcx, rsi
	call	strlen
	mov	rdx, rsi
	mov	rcx, rbx
	mov	r8, rax
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
.L3:
	mov	r8d, 1
	lea	rdx, .LC1[rip]
	mov	rcx, rbx
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	.p2align 4,,10
	.p2align 3
.L5:
	mov	rax, QWORD PTR [rbx]
	mov	rcx, QWORD PTR -24[rax]
	add	rcx, rbx
	mov	edx, DWORD PTR 32[rcx]
	or	edx, 1
	call	_ZNSt9basic_iosIcSt11char_traitsIcEE5clearESt12_Ios_Iostate
	jmp	.L3
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "dtor \0"
	.section	.text$_ZN3TagD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3TagD1Ev
	.def	_ZN3TagD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3TagD1Ev
_ZN3TagD1Ev:
.LFB4079:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	r8d, 5
	lea	rdx, .LC2[rip]
	mov	rsi, rcx
	mov	rcx, rbx
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	rsi, QWORD PTR [rsi]
	test	rsi, rsi
	je	.L9
	mov	rcx, rsi
	call	strlen
	mov	rdx, rsi
	mov	rcx, rbx
	mov	r8, rax
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
.L8:
	mov	r8d, 1
	lea	rdx, .LC1[rip]
	mov	rcx, rbx
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	nop
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L9:
	mov	rax, QWORD PTR [rbx]
	mov	rcx, QWORD PTR -24[rax]
	add	rcx, rbx
	mov	edx, DWORD PTR 32[rcx]
	or	edx, 1
	call	_ZNSt9basic_iosIcSt11char_traitsIcEE5clearESt12_Ios_Iostate
	jmp	.L8
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4079:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4079-.LLSDACSB4079
.LLSDACSB4079:
.LLSDACSE4079:
	.section	.text$_ZN3TagD1Ev,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC3:
	.ascii "A\0"
.LC4:
	.ascii "B\0"
.LC5:
	.ascii "C\0"
	.section	.text.unlikely,"x"
.LCOLDB6:
	.text
.LHOTB6:
	.p2align 4
	.globl	_Z1fv
	.def	_Z1fv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1fv
_Z1fv:
.LFB4080:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	lea	rdx, .LC3[rip]
	lea	rcx, 56[rsp]
.LEHB0:
	call	_ZN3TagC1EPKc
.LEHE0:
	lea	rdx, .LC4[rip]
	lea	rcx, 64[rsp]
.LEHB1:
	call	_ZN3TagC1EPKc
.LEHE1:
	lea	rdx, .LC5[rip]
	lea	rcx, 72[rsp]
.LEHB2:
	call	_ZN3TagC1EPKc
	nop
.LEHE2:
	jmp	.L17
.L14:
	mov	rdi, rax
	jmp	.L13
.L15:
	mov	rdi, rax
	jmp	.L12
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4080:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4080-.LLSDACSB4080
.LLSDACSB4080:
	.uleb128 .LEHB0-.LFB4080
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB4080
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L14-.LFB4080
	.uleb128 0
	.uleb128 .LEHB2-.LFB4080
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L15-.LFB4080
	.uleb128 0
.LLSDACSE4080:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z1fv.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z1fv.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 80
	.seh_savereg	rsi, 88
	.seh_savereg	rdi, 96
	.seh_endprologue
_Z1fv.cold:
.L17:
	mov	ecx, 4
	call	__cxa_allocate_exception
	xor	edx, edx
	xor	r8d, r8d
	mov	DWORD PTR [rax], edx
	mov	rdx, QWORD PTR .refptr._ZTIi[rip]
	mov	rcx, rax
.LEHB3:
	call	__cxa_throw
.LEHE3:
.L16:
	lea	rcx, 72[rsp]
	mov	QWORD PTR 40[rsp], rax
	call	_ZN3TagD1Ev
	mov	rdi, QWORD PTR 40[rsp]
.L12:
	lea	rcx, 64[rsp]
	call	_ZN3TagD1Ev
.L13:
	lea	rcx, 56[rsp]
	call	_ZN3TagD1Ev
	mov	rcx, rdi
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4080:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4080-.LLSDACSBC4080
.LLSDACSBC4080:
	.uleb128 .LEHB3-.LCOLDB6
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L16-.LCOLDB6
	.uleb128 0
	.uleb128 .LEHB4-.LCOLDB6
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSEC4080:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE6:
	.text
.LHOTE6:
	.section	.text.unlikely,"x"
.LCOLDB7:
	.section	.text.startup,"x"
.LHOTB7:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4081:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
.LEHB5:
	call	_Z1fv
	nop
.LEHE5:
.L20:
	jmp	.L19
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA4081:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT4081-.LLSDATTD4081
.LLSDATTD4081:
	.byte	0x1
	.uleb128 .LLSDACSE4081-.LLSDACSB4081
.LLSDACSB4081:
	.uleb128 .LEHB5-.LFB4081
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L20-.LFB4081
	.uleb128 0x1
.LLSDACSE4081:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT4081:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	40
	.seh_endprologue
main.cold:
.L19:
	mov	rcx, rax
	call	__cxa_begin_catch
.LEHB6:
	call	__cxa_end_catch
.LEHE6:
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDAC4081:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATTC4081-.LLSDATTDC4081
.LLSDATTDC4081:
	.byte	0x1
	.uleb128 .LLSDACSEC4081-.LLSDACSBC4081
.LLSDACSBC4081:
	.uleb128 .LEHB6-.LCOLDB7
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSEC4081:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATTC4081:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE7:
	.section	.text.startup,"x"
.LHOTE7:
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	strlen;	.scl	2;	.type	32;	.endef
	.def	_ZNSt9basic_iosIcSt11char_traitsIcEE5clearESt12_Ios_Iostate;	.scl	2;	.type	32;	.endef
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZTIi, "dr"
	.p2align	3, 0
	.globl	.refptr._ZTIi
	.linkonce	discard
.refptr._ZTIi:
	.quad	_ZTIi
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
