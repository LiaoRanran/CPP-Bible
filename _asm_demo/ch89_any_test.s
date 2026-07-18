	.file	"ch89_any_test.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "bad any_cast\0"
	.section	.text$_ZNKSt12bad_any_cast4whatEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt12bad_any_cast4whatEv
	.def	_ZNKSt12bad_any_cast4whatEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt12bad_any_cast4whatEv
_ZNKSt12bad_any_cast4whatEv:
.LFB63:
	.seh_endprologue
	lea	rax, .LC0[rip]
	ret
	.seh_endproc
	.section	.text$_ZNSt12bad_any_castD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12bad_any_castD1Ev
	.def	_ZNSt12bad_any_castD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12bad_any_castD1Ev
_ZNSt12bad_any_castD1Ev:
.LFB70:
	.seh_endprologue
	lea	rax, _ZTVSt12bad_any_cast[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt8bad_castD2Ev
	.seh_endproc
	.section	.text$_ZNSt12bad_any_castD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12bad_any_castD0Ev
	.def	_ZNSt12bad_any_castD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12bad_any_castD0Ev
_ZNSt12bad_any_castD0Ev:
.LFB71:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rax, _ZTVSt12bad_any_cast[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 40[rsp], rcx
	call	_ZNSt8bad_castD2Ev
	mov	rcx, QWORD PTR 40[rsp]
	mov	edx, 8
	add	rsp, 56
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZNSt3any17_Manager_internalIiE9_S_manageENS_3_OpEPKS_PNS_4_ArgE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt3any17_Manager_internalIiE9_S_manageENS_3_OpEPKS_PNS_4_ArgE
	.def	_ZNSt3any17_Manager_internalIiE9_S_manageENS_3_OpEPKS_PNS_4_ArgE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt3any17_Manager_internalIiE9_S_manageENS_3_OpEPKS_PNS_4_ArgE
_ZNSt3any17_Manager_internalIiE9_S_manageENS_3_OpEPKS_PNS_4_ArgE:
.LFB2587:
	.seh_endprologue
	cmp	ecx, 4
	ja	.L5
	lea	r9, .L8[rip]
	mov	ecx, ecx
	movsxd	rax, DWORD PTR [r9+rcx*4]
	add	rax, r9
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L8:
	.long	.L12-.L8
	.long	.L11-.L8
	.long	.L10-.L8
	.long	.L5-.L8
	.long	.L7-.L8
	.section	.text$_ZNSt3any17_Manager_internalIiE9_S_manageENS_3_OpEPKS_PNS_4_ArgE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L7:
	mov	rax, QWORD PTR [r8]
	mov	ecx, DWORD PTR 8[rdx]
	mov	DWORD PTR 8[rax], ecx
	mov	rcx, QWORD PTR [rdx]
	mov	QWORD PTR [rax], rcx
	mov	QWORD PTR [rdx], 0
.L5:
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	mov	ecx, DWORD PTR 8[rdx]
	mov	rax, QWORD PTR [r8]
	mov	rdx, QWORD PTR [rdx]
	mov	DWORD PTR 8[rax], ecx
	mov	QWORD PTR [rax], rdx
	ret
	.p2align 4,,10
	.p2align 3
.L12:
	add	rdx, 8
	mov	QWORD PTR [r8], rdx
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	mov	rax, QWORD PTR .refptr._ZTIi[rip]
	mov	QWORD PTR [r8], rax
	ret
	.seh_endproc
	.section	.text$_ZNSt3any17_Manager_externalINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE9_S_manageENS_3_OpEPKS_PNS_4_ArgE,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt3any17_Manager_externalINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE9_S_manageENS_3_OpEPKS_PNS_4_ArgE
	.def	_ZNSt3any17_Manager_externalINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE9_S_manageENS_3_OpEPKS_PNS_4_ArgE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt3any17_Manager_externalINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE9_S_manageENS_3_OpEPKS_PNS_4_ArgE
_ZNSt3any17_Manager_externalINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE9_S_manageENS_3_OpEPKS_PNS_4_ArgE:
.LFB2591:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	mov	r10, r8
	mov	r9, rdx
	mov	r8, QWORD PTR 8[rdx]
	cmp	ecx, 4
	ja	.L13
	lea	rdx, .L16[rip]
	mov	ecx, ecx
	movsxd	rax, DWORD PTR [rdx+rcx*4]
	add	rax, rdx
	jmp	rax
	.section .rdata,"dr"
	.align 4
.L16:
	.long	.L20-.L16
	.long	.L19-.L16
	.long	.L18-.L16
	.long	.L17-.L16
	.long	.L15-.L16
	.section	.text$_ZNSt3any17_Manager_externalINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE9_S_manageENS_3_OpEPKS_PNS_4_ArgE,"x"
	.linkonce discard
	.p2align 4,,10
	.p2align 3
.L20:
	mov	QWORD PTR [r10], r8
.L13:
	add	rsp, 88
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L17:
	test	r8, r8
	je	.L13
	mov	rcx, QWORD PTR [r8]
	lea	rax, 16[r8]
	cmp	rcx, rax
	je	.L24
	mov	rax, QWORD PTR 16[r8]
	mov	QWORD PTR 40[rsp], r8
	lea	rdx, 1[rax]
	call	_ZdlPvy
	mov	r8, QWORD PTR 40[rsp]
.L24:
	mov	edx, 32
	mov	rcx, r8
	add	rsp, 88
	pop	rbx
	pop	rsi
.LEHB0:
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L15:
	mov	rax, QWORD PTR [r10]
	mov	QWORD PTR 8[rax], r8
	mov	rax, QWORD PTR [r10]
	mov	rdx, QWORD PTR [r9]
	mov	QWORD PTR [rax], rdx
	mov	QWORD PTR [r9], 0
	add	rsp, 88
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	lea	rax, _ZTINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE[rip]
	mov	QWORD PTR [r10], rax
	add	rsp, 88
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L18:
	mov	ecx, 32
	mov	QWORD PTR 56[rsp], r10
	mov	QWORD PTR 48[rsp], r9
	mov	QWORD PTR 40[rsp], r8
	call	_Znwy
.LEHE0:
	mov	r8, QWORD PTR 40[rsp]
	mov	r9, QWORD PTR 48[rsp]
	lea	rcx, 16[rax]
	mov	r10, QWORD PTR 56[rsp]
	mov	rbx, rax
	mov	r11, QWORD PTR 8[r8]
	mov	QWORD PTR [rax], rcx
	mov	rdx, QWORD PTR [r8]
	cmp	r11, 15
	lea	r8, 1[r11]
	ja	.L30
	test	r11, r11
	jne	.L22
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR 16[rbx], al
.L23:
	mov	rax, QWORD PTR [r10]
	mov	QWORD PTR 8[rbx], r11
	mov	QWORD PTR 8[rax], rbx
	mov	rax, QWORD PTR [r10]
	mov	rdx, QWORD PTR [r9]
	mov	QWORD PTR [rax], rdx
	add	rsp, 88
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L30:
	mov	rcx, r8
	mov	QWORD PTR 72[rsp], r10
	mov	QWORD PTR 64[rsp], r9
	mov	QWORD PTR 56[rsp], rdx
	mov	QWORD PTR 48[rsp], r11
	mov	QWORD PTR 40[rsp], r8
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	r11, QWORD PTR 48[rsp]
	mov	r8, QWORD PTR 40[rsp]
	mov	QWORD PTR [rbx], rax
	mov	rcx, rax
	mov	rdx, QWORD PTR 56[rsp]
	mov	r9, QWORD PTR 64[rsp]
	mov	QWORD PTR 16[rbx], r11
	mov	r10, QWORD PTR 72[rsp]
.L22:
	mov	QWORD PTR 56[rsp], r10
	mov	QWORD PTR 48[rsp], r9
	mov	QWORD PTR 40[rsp], r11
	call	memcpy
	mov	r10, QWORD PTR 56[rsp]
	mov	r9, QWORD PTR 48[rsp]
	mov	r11, QWORD PTR 40[rsp]
	jmp	.L23
.L26:
	mov	rsi, rax
.L25:
	mov	rcx, rbx
	mov	edx, 32
	call	_ZdlPvy
	mov	rcx, rsi
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2591:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2591-.LLSDACSB2591
.LLSDACSB2591:
	.uleb128 .LEHB0-.LFB2591
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB2591
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L26-.LFB2591
	.uleb128 0
	.uleb128 .LEHB2-.LFB2591
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE2591:
	.section	.text$_ZNSt3any17_Manager_externalINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE9_S_manageENS_3_OpEPKS_PNS_4_ArgE,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt3any5resetEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt3any5resetEv
	.def	_ZNSt3any5resetEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt3any5resetEv
_ZNSt3any5resetEv:
.LFB97:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rcx
	test	rax, rax
	je	.L31
	mov	rdx, rcx
	xor	r8d, r8d
	mov	ecx, 3
	call	rax
	mov	QWORD PTR [rbx], 0
.L31:
	add	rsp, 32
	pop	rbx
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA97:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE97-.LLSDACSB97
.LLSDACSB97:
.LLSDACSE97:
	.section	.text$_ZNSt3any5resetEv,"x"
	.linkonce discard
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB2:
	.section	.text.startup,"x"
.LHOTB2:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2137:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 96
	.seh_stackalloc	96
	.seh_endprologue
	call	__main
	lea	rax, _ZNSt3any17_Manager_internalIiE9_S_manageENS_3_OpEPKS_PNS_4_ArgE[rip]
	mov	ecx, 40
	mov	DWORD PTR 60[rsp], 42
	mov	QWORD PTR 64[rsp], rax
	mov	eax, DWORD PTR 60[rsp]
	mov	QWORD PTR 72[rsp], 42
.LEHB3:
	call	_Znwy
.LEHE3:
	mov	rbx, rax
	mov	ecx, 32
	movabs	rax, 8247343400834656372
	movabs	rdx, 7791354250703367785
	mov	QWORD PTR [rbx], rax
	movabs	rax, 7526676552942579311
	mov	QWORD PTR 8[rbx], rdx
	movabs	rdx, 8746588843431456353
	mov	QWORD PTR 16[rbx], rax
	movabs	rax, 5711218676299297913
	mov	QWORD PTR 24[rbx], rdx
	mov	BYTE PTR 39[rbx], 0
	mov	QWORD PTR 31[rbx], rax
	lea	rax, _ZNSt3any17_Manager_externalINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEE9_S_manageENS_3_OpEPKS_PNS_4_ArgE[rip]
	mov	QWORD PTR 80[rsp], rax
	mov	QWORD PTR 88[rsp], 0
.LEHB4:
	call	_Znwy
.LEHE4:
	mov	edx, 39
	mov	QWORD PTR [rax], rbx
	lea	rcx, 80[rsp]
	movq	xmm0, rdx
	mov	QWORD PTR 88[rsp], rax
	punpcklqdq	xmm0, xmm0
	mov	BYTE PTR 59[rsp], 1
	movups	XMMWORD PTR 8[rax], xmm0
	movzx	eax, BYTE PTR 59[rsp]
	call	_ZNSt3any5resetEv
	lea	rcx, 64[rsp]
	call	_ZNSt3any5resetEv
	xor	eax, eax
	add	rsp, 96
	pop	rbx
	ret
.L39:
	mov	rbx, rax
	jmp	.L38
.L40:
	jmp	.L37
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2137:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2137-.LLSDACSB2137
.LLSDACSB2137:
	.uleb128 .LEHB3-.LFB2137
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L39-.LFB2137
	.uleb128 0
	.uleb128 .LEHB4-.LFB2137
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L40-.LFB2137
	.uleb128 0
.LLSDACSE2137:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 96
	.seh_endprologue
main.cold:
.L37:
	mov	rcx, rbx
	mov	edx, 40
	mov	QWORD PTR 40[rsp], rax
	call	_ZdlPvy
	mov	rbx, QWORD PTR 40[rsp]
.L38:
	lea	rcx, 64[rsp]
	call	_ZNSt3any5resetEv
	mov	rcx, rbx
.LEHB5:
	call	_Unwind_Resume
	nop
.LEHE5:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2137:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2137-.LLSDACSBC2137
.LLSDACSBC2137:
	.uleb128 .LEHB5-.LCOLDB2
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSEC2137:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE2:
	.section	.text.startup,"x"
.LHOTE2:
	.globl	_ZTSSt9exception
	.section	.rdata$_ZTSSt9exception,"dr"
	.linkonce same_size
	.align 8
_ZTSSt9exception:
	.ascii "St9exception\0"
	.globl	_ZTISt9exception
	.section	.rdata$_ZTISt9exception,"dr"
	.linkonce same_size
	.align 8
_ZTISt9exception:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSSt9exception
	.globl	_ZTSSt8bad_cast
	.section	.rdata$_ZTSSt8bad_cast,"dr"
	.linkonce same_size
	.align 8
_ZTSSt8bad_cast:
	.ascii "St8bad_cast\0"
	.globl	_ZTISt8bad_cast
	.section	.rdata$_ZTISt8bad_cast,"dr"
	.linkonce same_size
	.align 8
_ZTISt8bad_cast:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt8bad_cast
	.quad	_ZTISt9exception
	.globl	_ZTSSt12bad_any_cast
	.section	.rdata$_ZTSSt12bad_any_cast,"dr"
	.linkonce same_size
	.align 16
_ZTSSt12bad_any_cast:
	.ascii "St12bad_any_cast\0"
	.globl	_ZTISt12bad_any_cast
	.section	.rdata$_ZTISt12bad_any_cast,"dr"
	.linkonce same_size
	.align 8
_ZTISt12bad_any_cast:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt12bad_any_cast
	.quad	_ZTISt8bad_cast
	.globl	_ZTSNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.section	.rdata$_ZTSNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE,"dr"
	.linkonce same_size
	.align 32
_ZTSNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:
	.ascii "NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE\0"
	.globl	_ZTINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.section	.rdata$_ZTINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.globl	_ZTVSt12bad_any_cast
	.section	.rdata$_ZTVSt12bad_any_cast,"dr"
	.linkonce same_size
	.align 8
_ZTVSt12bad_any_cast:
	.quad	0
	.quad	_ZTISt12bad_any_cast
	.quad	_ZNSt12bad_any_castD1Ev
	.quad	_ZNSt12bad_any_castD0Ev
	.quad	_ZNKSt12bad_any_cast4whatEv
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt8bad_castD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZTIi, "dr"
	.p2align	3, 0
	.globl	.refptr._ZTIi
	.linkonce	discard
.refptr._ZTIi:
	.quad	_ZTIi
