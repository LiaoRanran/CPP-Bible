	.file	"_ch142_antipattern.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch142_antipattern.cpp"
	.section	.text$_ZSt21is_constant_evaluatedv,"x"
	.linkonce discard
	.globl	_ZSt21is_constant_evaluatedv
	.def	_ZSt21is_constant_evaluatedv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt21is_constant_evaluatedv
_ZSt21is_constant_evaluatedv:
.LFB15:
	.file 1 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/type_traits"
	.loc 1 4008 3
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	.seh_endprologue
	.loc 1 4010 49
	mov	eax, 0
	.loc 1 4014 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE15:
	.seh_endproc
	.section	.text$_ZnwyPv,"x"
	.linkonce discard
	.globl	_ZnwyPv
	.def	_ZnwyPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZnwyPv
_ZnwyPv:
.LFB220:
	.file 2 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/new"
	.loc 2 208 1
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
	mov	QWORD PTR 24[rbp], rdx
	.loc 2 208 10
	mov	rax, QWORD PTR 24[rbp]
	.loc 2 208 15
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE220:
	.seh_endproc
	.section	.text$_ZdlPvS_,"x"
	.linkonce discard
	.globl	_ZdlPvS_
	.def	_ZdlPvS_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvS_
_ZdlPvS_:
.LFB222:
	.loc 2 219 1
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
	mov	QWORD PTR 24[rbp], rdx
	.loc 2 219 3
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE222:
	.seh_endproc
	.section	.text$_ZN7Monster6updateEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN7Monster6updateEv
	.def	_ZN7Monster6updateEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7Monster6updateEv
_ZN7Monster6updateEv:
.LFB1719:
	.file 3 "Examples/_ch142_antipattern.cpp"
	.loc 3 14 10
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
	.loc 3 14 30
	mov	rax, QWORD PTR 16[rbp]
	movss	xmm1, DWORD PTR 8[rax]
	.loc 3 14 32
	movss	xmm0, DWORD PTR .LC0[rip]
	addss	xmm0, xmm1
	mov	rax, QWORD PTR 16[rbp]
	movss	DWORD PTR 8[rax], xmm0
	.loc 3 14 41
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1719:
	.seh_endproc
	.text
	.globl	_Z14monster_systemRSt6vectorI11MonsterDataSaIS0_EE
	.def	_Z14monster_systemRSt6vectorI11MonsterDataSaIS0_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14monster_systemRSt6vectorI11MonsterDataSaIS0_EE
_Z14monster_systemRSt6vectorI11MonsterDataSaIS0_EE:
.LFB1720:
	.loc 3 19 50
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB104:
	.loc 3 20 20
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZNSt6vectorI11MonsterDataSaIS0_EE5beginEv
	mov	QWORD PTR -40[rbp], rax
	.loc 3 20 20 is_stmt 0 discriminator 1
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZNSt6vectorI11MonsterDataSaIS0_EE3endEv
	mov	QWORD PTR -48[rbp], rax
	.loc 3 20 5 is_stmt 1
	jmp	.L8
.L14:
.LBB105:
.LBB106:
	.file 4 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_iterator.h"
	.loc 4 1090 17
	mov	rax, QWORD PTR -40[rbp]
.LBE106:
.LBE105:
	.loc 3 20 20 discriminator 8
	mov	QWORD PTR -16[rbp], rax
	.loc 3 20 25 discriminator 8
	mov	rax, QWORD PTR -16[rbp]
	movss	xmm1, DWORD PTR [rax]
	.loc 3 20 27 discriminator 8
	movss	xmm0, DWORD PTR .LC0[rip]
	addss	xmm0, xmm1
	mov	rax, QWORD PTR -16[rbp]
	movss	DWORD PTR [rax], xmm0
.LBB107:
.LBB108:
	.loc 4 1103 4
	mov	rax, QWORD PTR -40[rbp]
	.loc 4 1103 2
	add	rax, 8
	mov	QWORD PTR -40[rbp], rax
	.loc 4 1104 10
	nop
.L8:
	lea	rax, -40[rbp]
	mov	QWORD PTR -24[rbp], rax
.LBE108:
.LBE107:
.LBB109:
.LBB110:
.LBB111:
.LBB112:
	.loc 4 1166 16
	mov	rax, QWORD PTR -24[rbp]
.LBE112:
.LBE111:
	.loc 4 1206 27 discriminator 1
	mov	rdx, QWORD PTR [rax]
	lea	rax, -48[rbp]
	mov	QWORD PTR -32[rbp], rax
.LBB113:
.LBB114:
	.loc 4 1166 16
	mov	rax, QWORD PTR -32[rbp]
.LBE114:
.LBE113:
	.loc 4 1206 27 discriminator 2
	mov	rax, QWORD PTR [rax]
	.loc 4 1206 41 discriminator 2
	cmp	rdx, rax
	sete	al
.LBE110:
.LBE109:
	.loc 3 20 20 discriminator 7
	xor	eax, 1
	test	al, al
	jne	.L14
.LBE104:
	.loc 3 21 1
	nop
	nop
	add	rsp, 80
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1720:
	.seh_endproc
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1724:
	.loc 3 23 12
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	sub	rsp, 88
	.seh_stackalloc	88
	.cfi_def_cfa_offset 112
	lea	rbp, 80[rsp]
	.seh_setframe	rbp, 80
	.cfi_def_cfa 6, 32
	.seh_endprologue
	.loc 3 23 12
	call	__main
	lea	rax, -9[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB115:
.LBB116:
.LBB117:
.LBB118:
.LBB119:
	.file 5 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/new_allocator.h"
	.loc 5 88 49
	nop
.LBE119:
.LBE118:
.LBE117:
	.file 6 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/allocator.h"
	.loc 6 168 38
	nop
.LBE116:
.LBE115:
	.loc 3 24 31 discriminator 1
	lea	rdx, -9[rbp]
	lea	rax, -48[rbp]
	mov	r8, rdx
	mov	edx, 64
	mov	rcx, rax
	call	_ZNSt6vectorI7MonsterSaIS0_EEC1EyRKS1_
.LBB120:
.LBB121:
	.loc 6 189 39
	nop
.LBE121:
.LBE120:
	.loc 3 25 19
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_Z14monster_systemRSt6vectorI11MonsterDataSaIS0_EE
	.loc 3 26 21
	lea	rax, -48[rbp]
	mov	edx, 0
	mov	rcx, rax
	call	_ZNSt6vectorI7MonsterSaIS0_EEixEy
	.loc 3 26 23 discriminator 1
	movss	xmm0, DWORD PTR 8[rax]
	cvttss2si	ebx, xmm0
	.loc 3 27 1
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZNSt6vectorI7MonsterSaIS0_EED1Ev
	mov	eax, ebx
	add	rsp, 88
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -72
	ret
	.cfi_endproc
.LFE1724:
	.seh_endproc
	.section	.text$_ZNSt6vectorI11MonsterDataSaIS0_EE5beginEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI11MonsterDataSaIS0_EE5beginEv
	.def	_ZNSt6vectorI11MonsterDataSaIS0_EE5beginEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI11MonsterDataSaIS0_EE5beginEv
_ZNSt6vectorI11MonsterDataSaIS0_EE5beginEv:
.LFB1730:
	.file 7 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_vector.h"
	.loc 7 998 7
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
	.loc 7 999 39
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB122:
.LBB123:
.LBB124:
	.loc 4 1059 9
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR -16[rbp], rax
.LBE124:
	.loc 4 1059 27
	nop
.LBE123:
.LBE122:
	.loc 7 999 47 discriminator 1
	mov	rax, QWORD PTR -16[rbp]
	.loc 7 999 50
	add	rsp, 16
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1730:
	.seh_endproc
	.section	.text$_ZNSt6vectorI11MonsterDataSaIS0_EE3endEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI11MonsterDataSaIS0_EE3endEv
	.def	_ZNSt6vectorI11MonsterDataSaIS0_EE3endEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI11MonsterDataSaIS0_EE3endEv
_ZNSt6vectorI11MonsterDataSaIS0_EE3endEv:
.LFB1731:
	.loc 7 1018 7
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
	.loc 7 1019 39
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	QWORD PTR -8[rbp], rax
.LBB125:
.LBB126:
.LBB127:
	.loc 4 1059 9
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR -16[rbp], rax
.LBE127:
	.loc 4 1059 27
	nop
.LBE126:
.LBE125:
	.loc 7 1019 48 discriminator 1
	mov	rax, QWORD PTR -16[rbp]
	.loc 7 1019 51
	add	rsp, 16
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1731:
	.seh_endproc
	.section	.text$_ZNSt6vectorI7MonsterSaIS0_EEC1EyRKS1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI7MonsterSaIS0_EEC1EyRKS1_
	.def	_ZNSt6vectorI7MonsterSaIS0_EEC1EyRKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI7MonsterSaIS0_EEC1EyRKS1_
_ZNSt6vectorI7MonsterSaIS0_EEC1EyRKS1_:
.LFB1741:
	.loc 7 586 7
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
	mov	QWORD PTR 40[rbp], rdx
	mov	QWORD PTR 48[rbp], r8
.LBB128:
	.loc 7 587 47
	mov	rbx, QWORD PTR 32[rbp]
	mov	rdx, QWORD PTR 48[rbp]
	mov	rax, QWORD PTR 40[rbp]
	mov	rcx, rax
.LEHB0:
	call	_ZNSt6vectorI7MonsterSaIS0_EE17_S_check_init_lenEyRKS1_
	.loc 7 587 47 is_stmt 0 discriminator 1
	mov	rdx, QWORD PTR 48[rbp]
	mov	r8, rdx
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EEC2EyRKS1_
.LEHE0:
	.loc 7 588 30 is_stmt 1
	mov	rdx, QWORD PTR 40[rbp]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
.LEHB1:
	call	_ZNSt6vectorI7MonsterSaIS0_EE21_M_default_initializeEy
.LEHE1:
.LBE128:
	.loc 7 588 37
	jmp	.L24
.L23:
.LBB129:
	.loc 7 588 37 is_stmt 0 discriminator 2
	mov	rbx, rax
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EED2Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
.L24:
.LBE129:
	.loc 7 588 37
	add	rsp, 40
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -24
	ret
	.cfi_endproc
.LFE1741:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1741:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1741-.LLSDACSB1741
.LLSDACSB1741:
	.uleb128 .LEHB0-.LFB1741
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB1741
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L23-.LFB1741
	.uleb128 0
	.uleb128 .LEHB2-.LFB1741
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE1741:
	.section	.text$_ZNSt6vectorI7MonsterSaIS0_EEC1EyRKS1_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt6vectorI7MonsterSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI7MonsterSaIS0_EED1Ev
	.def	_ZNSt6vectorI7MonsterSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI7MonsterSaIS0_EED1Ev
_ZNSt6vectorI7MonsterSaIS0_EED1Ev:
.LFB1744:
	.loc 7 800 7 is_stmt 1
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB130:
	.loc 7 803 28
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EE19_M_get_Tp_allocatorEv
	.loc 7 802 54
	mov	rdx, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 8[rdx]
	.loc 7 802 30
	mov	rcx, QWORD PTR 16[rbp]
	mov	rcx, QWORD PTR [rcx]
	mov	QWORD PTR -8[rbp], rcx
	mov	QWORD PTR -16[rbp], rdx
	mov	QWORD PTR -24[rbp], rax
.LBB131:
.LBB132:
	.file 8 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/alloc_traits.h"
	.loc 8 1045 20
	mov	rdx, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZSt8_DestroyIP7MonsterEvT_S2_
	.loc 8 1046 5
	nop
.LBE132:
.LBE131:
	.loc 7 805 7
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EED2Ev
.LBE130:
	nop
	add	rsp, 64
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1744:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1744:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1744-.LLSDACSB1744
.LLSDACSB1744:
.LLSDACSE1744:
	.section	.text$_ZNSt6vectorI7MonsterSaIS0_EED1Ev,"x"
	.linkonce discard
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "__n < this->size()\0"
	.align 8
.LC2:
	.ascii "constexpr std::vector<_Tp, _Alloc>::reference std::vector<_Tp, _Alloc>::operator[](size_type) [with _Tp = Monster; _Alloc = std::allocator<Monster>; reference = Monster&; size_type = long long unsigned int]\0"
	.align 8
.LC3:
	.ascii "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_vector.h\0"
	.section	.text$_ZNSt6vectorI7MonsterSaIS0_EEixEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI7MonsterSaIS0_EEixEy
	.def	_ZNSt6vectorI7MonsterSaIS0_EEixEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI7MonsterSaIS0_EEixEy
_ZNSt6vectorI7MonsterSaIS0_EEixEy:
.LFB1745:
	.loc 7 1261 7
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	.loc 7 1263 2
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt6vectorI7MonsterSaIS0_EE4sizeEv
	.loc 7 1263 2 is_stmt 0 discriminator 1
	cmp	QWORD PTR 24[rbp], rax
	setnb	al
	movzx	eax, al
	.loc 7 1263 2 discriminator 2
	test	eax, eax
	setne	al
	test	al, al
	je	.L27
	.loc 7 1263 2 discriminator 3
	lea	rcx, .LC1[rip]
	lea	rdx, .LC2[rip]
	lea	rax, .LC3[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 1263
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L27:
	.loc 7 1264 25 is_stmt 1
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 7 1264 34
	mov	rdx, QWORD PTR 24[rbp]
	sal	rdx, 4
	.loc 7 1264 39
	add	rax, rdx
	.loc 7 1265 7
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1745:
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC4:
	.ascii "cannot create std::vector larger than max_size()\0"
	.section	.text$_ZNSt6vectorI7MonsterSaIS0_EE17_S_check_init_lenEyRKS1_,"x"
	.linkonce discard
	.globl	_ZNSt6vectorI7MonsterSaIS0_EE17_S_check_init_lenEyRKS1_
	.def	_ZNSt6vectorI7MonsterSaIS0_EE17_S_check_init_lenEyRKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI7MonsterSaIS0_EE17_S_check_init_lenEyRKS1_
_ZNSt6vectorI7MonsterSaIS0_EE17_S_check_init_lenEyRKS1_:
.LFB1752:
	.loc 7 2213 7
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR -8[rbp], rax
	lea	rax, -25[rbp]
	mov	QWORD PTR -16[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -24[rbp], rax
.LBB133:
.LBB134:
.LBB135:
.LBB136:
.LBB137:
	.loc 5 92 71
	nop
.LBE137:
.LBE136:
.LBE135:
	.loc 6 173 38
	nop
.LBE134:
.LBE133:
	.loc 7 2215 23 discriminator 1
	lea	rax, -25[rbp]
	mov	rcx, rax
	call	_ZNSt6vectorI7MonsterSaIS0_EE11_S_max_sizeERKS1_
	.loc 7 2215 10 discriminator 2
	cmp	rax, QWORD PTR 16[rbp]
	setb	al
.LBB138:
.LBB139:
	.loc 6 189 39
	nop
.LBE139:
.LBE138:
	.loc 7 2215 2 discriminator 3
	test	al, al
	je	.L30
	.loc 7 2216 24
	lea	rax, .LC4[rip]
	mov	rcx, rax
	call	_ZSt20__throw_length_errorPKc
.L30:
	.loc 7 2218 9
	mov	rax, QWORD PTR 16[rbp]
	.loc 7 2219 7
	add	rsp, 64
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1752:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implD1Ev
	.def	_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implD1Ev
_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implD1Ev:
.LFB1756:
	.loc 7 139 14
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
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB140:
.LBB141:
.LBB142:
	.loc 6 189 39
	nop
.LBE142:
.LBE141:
.LBE140:
	.loc 7 139 14
	nop
	add	rsp, 16
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1756:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EEC2EyRKS1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI7MonsterSaIS0_EEC2EyRKS1_
	.def	_ZNSt12_Vector_baseI7MonsterSaIS0_EEC2EyRKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI7MonsterSaIS0_EEC2EyRKS1_
_ZNSt12_Vector_baseI7MonsterSaIS0_EEC2EyRKS1_:
.LFB1757:
	.loc 7 339 7
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
	mov	QWORD PTR 40[rbp], rdx
	mov	QWORD PTR 48[rbp], r8
.LBB143:
	.loc 7 340 9
	mov	rax, QWORD PTR 32[rbp]
	mov	rdx, QWORD PTR 48[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC1ERKS1_
	.loc 7 341 26
	mov	rdx, QWORD PTR 40[rbp]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
.LEHB3:
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_M_create_storageEy
.LEHE3:
.LBE143:
	.loc 7 341 33
	jmp	.L36
.L35:
.LBB144:
	.loc 7 341 33 is_stmt 0 discriminator 2
	mov	rbx, rax
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implD1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
.L36:
.LBE144:
	.loc 7 341 33
	add	rsp, 40
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -24
	ret
	.cfi_endproc
.LFE1757:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1757:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1757-.LLSDACSB1757
.LLSDACSB1757:
	.uleb128 .LEHB3-.LFB1757
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L35-.LFB1757
	.uleb128 0
	.uleb128 .LEHB4-.LFB1757
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE1757:
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EEC2EyRKS1_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EED2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI7MonsterSaIS0_EED2Ev
	.def	_ZNSt12_Vector_baseI7MonsterSaIS0_EED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI7MonsterSaIS0_EED2Ev
_ZNSt12_Vector_baseI7MonsterSaIS0_EED2Ev:
.LFB1760:
	.loc 7 373 7 is_stmt 1
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB145:
	.loc 7 376 17
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 16[rax]
	.loc 7 376 45
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 7 376 35
	sub	rdx, rax
	mov	rax, rdx
	sar	rax, 4
	.loc 7 375 15
	mov	rcx, rax
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EE13_M_deallocateEPS0_y
	.loc 7 377 7
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implD1Ev
.LBE145:
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1760:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1760:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1760-.LLSDACSB1760
.LLSDACSB1760:
.LLSDACSE1760:
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EED2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt6vectorI7MonsterSaIS0_EE21_M_default_initializeEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI7MonsterSaIS0_EE21_M_default_initializeEy
	.def	_ZNSt6vectorI7MonsterSaIS0_EE21_M_default_initializeEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI7MonsterSaIS0_EE21_M_default_initializeEy
_ZNSt6vectorI7MonsterSaIS0_EE21_M_default_initializeEy:
.LFB1762:
	.loc 7 2008 7
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	.loc 7 2012 28
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EE19_M_get_Tp_allocatorEv
	mov	rcx, rax
	.loc 7 2011 51
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 7 2011 36
	mov	rdx, QWORD PTR 24[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZSt27__uninitialized_default_n_aIP7MonsteryS0_ET_S2_T0_RSaIT1_E
	.loc 7 2010 26
	mov	rdx, QWORD PTR 16[rbp]
	mov	QWORD PTR 8[rdx], rax
	.loc 7 2013 7
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1762:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EE19_M_get_Tp_allocatorEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI7MonsterSaIS0_EE19_M_get_Tp_allocatorEv
	.def	_ZNSt12_Vector_baseI7MonsterSaIS0_EE19_M_get_Tp_allocatorEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI7MonsterSaIS0_EE19_M_get_Tp_allocatorEv
_ZNSt12_Vector_baseI7MonsterSaIS0_EE19_M_get_Tp_allocatorEv:
.LFB1763:
	.loc 7 307 7
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
	.loc 7 308 22
	mov	rax, QWORD PTR 16[rbp]
	.loc 7 308 31
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1763:
	.seh_endproc
	.section	.text$_ZNKSt6vectorI7MonsterSaIS0_EE4sizeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6vectorI7MonsterSaIS0_EE4sizeEv
	.def	_ZNKSt6vectorI7MonsterSaIS0_EE4sizeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6vectorI7MonsterSaIS0_EE4sizeEv
_ZNKSt6vectorI7MonsterSaIS0_EE4sizeEv:
.LFB1765:
	.loc 7 1117 7
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
	.loc 7 1119 34
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 8[rax]
	.loc 7 1119 60
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 7 1119 44
	sub	rdx, rax
	.loc 7 1119 12
	mov	rax, rdx
	sar	rax, 4
	mov	QWORD PTR -8[rbp], rax
	.loc 7 1120 2
	cmp	QWORD PTR -8[rbp], 0
	.loc 7 1122 24
	mov	rax, QWORD PTR -8[rbp]
	.loc 7 1123 7
	add	rsp, 16
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1765:
	.seh_endproc
	.section	.text$_ZNSt6vectorI7MonsterSaIS0_EE11_S_max_sizeERKS1_,"x"
	.linkonce discard
	.globl	_ZNSt6vectorI7MonsterSaIS0_EE11_S_max_sizeERKS1_
	.def	_ZNSt6vectorI7MonsterSaIS0_EE11_S_max_sizeERKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI7MonsterSaIS0_EE11_S_max_sizeERKS1_
_ZNSt6vectorI7MonsterSaIS0_EE11_S_max_sizeERKS1_:
.LFB1766:
	.loc 7 2222 7
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 7 2227 15
	movabs	rax, 576460752303423487
	mov	QWORD PTR -8[rbp], rax
	.loc 7 2229 15
	movabs	rax, 1152921504606846975
	mov	QWORD PTR -16[rbp], rax
	.loc 7 2230 19
	lea	rdx, -16[rbp]
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZSt3minIyERKT_S2_S2_
	.loc 7 2230 41 discriminator 1
	mov	rax, QWORD PTR [rax]
	.loc 7 2231 7
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1766:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC1ERKS1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC1ERKS1_
	.def	_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC1ERKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC1ERKS1_
_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC1ERKS1_:
.LFB1773:
	.loc 7 152 2
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR -16[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -24[rbp], rax
	mov	rax, QWORD PTR -16[rbp]
	mov	QWORD PTR -32[rbp], rax
.LBB146:
.LBB147:
.LBB148:
.LBB149:
.LBB150:
.LBB151:
	.loc 5 92 71
	nop
.LBE151:
.LBE150:
.LBE149:
	.loc 6 173 38
	nop
.LBE148:
.LBE147:
	.loc 7 153 22 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_dataC2Ev
.LBE146:
	.loc 7 154 4
	nop
	add	rsp, 64
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1773:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_M_create_storageEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_M_create_storageEy
	.def	_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_M_create_storageEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_M_create_storageEy
_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_M_create_storageEy:
.LFB1774:
	.loc 7 403 7
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	.loc 7 405 44
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI7MonsterSaIS0_EE11_M_allocateEy
	.loc 7 405 25 discriminator 1
	mov	rdx, QWORD PTR 16[rbp]
	mov	QWORD PTR [rdx], rax
	.loc 7 406 42
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR [rax]
	.loc 7 406 26
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR 8[rax], rdx
	.loc 7 407 50
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 7 407 59
	mov	rdx, QWORD PTR 24[rbp]
	sal	rdx, 4
	add	rdx, rax
	.loc 7 407 34
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR 16[rax], rdx
	.loc 7 408 7
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1774:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EE13_M_deallocateEPS0_y,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI7MonsterSaIS0_EE13_M_deallocateEPS0_y
	.def	_ZNSt12_Vector_baseI7MonsterSaIS0_EE13_M_deallocateEPS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI7MonsterSaIS0_EE13_M_deallocateEPS0_y
_ZNSt12_Vector_baseI7MonsterSaIS0_EE13_M_deallocateEPS0_y:
.LFB1775:
	.loc 7 392 7
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	.loc 7 395 2
	cmp	QWORD PTR 24[rbp], 0
	je	.L53
	.loc 7 396 20
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR -16[rbp], rax
	mov	rax, QWORD PTR 32[rbp]
	mov	QWORD PTR -24[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -32[rbp], rax
	mov	rax, QWORD PTR -16[rbp]
	mov	QWORD PTR -40[rbp], rax
	mov	rax, QWORD PTR -24[rbp]
	mov	QWORD PTR -48[rbp], rax
.LBB152:
.LBB153:
.LBB154:
.LBB155:
.LBB156:
.LBB157:
	.file 9 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/x86_64-w64-mingw32/bits/c++config.h"
	.loc 9 586 49
	mov	eax, 0
.LBE157:
.LBE156:
	.loc 6 210 2 discriminator 1
	test	al, al
	je	.L51
	.loc 6 212 23
	mov	rax, QWORD PTR -40[rbp]
	mov	rcx, rax
	call	_ZdlPv
	.loc 6 213 6
	jmp	.L52
.L51:
	.loc 6 215 35
	mov	rcx, QWORD PTR -48[rbp]
	mov	rdx, QWORD PTR -40[rbp]
	mov	rax, QWORD PTR -32[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZNSt15__new_allocatorI7MonsterE10deallocateEPS0_y
.L52:
.LBE155:
.LBE154:
	.loc 8 649 35
	nop
.L53:
.LBE153:
.LBE152:
	.loc 7 397 7
	nop
	add	rsp, 80
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1775:
	.seh_endproc
	.section	.text$_ZSt27__uninitialized_default_n_aIP7MonsteryS0_ET_S2_T0_RSaIT1_E,"x"
	.linkonce discard
	.globl	_ZSt27__uninitialized_default_n_aIP7MonsteryS0_ET_S2_T0_RSaIT1_E
	.def	_ZSt27__uninitialized_default_n_aIP7MonsteryS0_ET_S2_T0_RSaIT1_E;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt27__uninitialized_default_n_aIP7MonsteryS0_ET_S2_T0_RSaIT1_E
_ZSt27__uninitialized_default_n_aIP7MonsteryS0_ET_S2_T0_RSaIT1_E:
.LFB1776:
	.file 10 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_uninitialized.h"
	.loc 10 1027 5
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	.loc 10 1029 44
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZSt25__uninitialized_default_nIP7MonsteryET_S2_T0_
	.loc 10 1029 60
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1776:
	.seh_endproc
	.section	.text$_ZSt8_DestroyIP7MonsterEvT_S2_,"x"
	.linkonce discard
	.globl	_ZSt8_DestroyIP7MonsterEvT_S2_
	.def	_ZSt8_DestroyIP7MonsterEvT_S2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt8_DestroyIP7MonsterEvT_S2_
_ZSt8_DestroyIP7MonsterEvT_S2_:
.LFB1777:
	.file 11 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_construct.h"
	.loc 11 219 5
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	.loc 11 225 2
	jmp	.L57
.L59:
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB158:
.LBB159:
	.file 12 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/move.h"
	.loc 12 53 37
	mov	rax, QWORD PTR -8[rbp]
.LBE159:
.LBE158:
	.loc 11 226 17 discriminator 1
	mov	rcx, rax
	call	_ZSt8_DestroyI7MonsterEvPT_
	.loc 11 225 2 discriminator 2
	add	QWORD PTR 16[rbp], 16
.L57:
	.loc 11 225 17 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	cmp	rax, QWORD PTR 24[rbp]
	jne	.L59
	.loc 11 236 5
	nop
	nop
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1777:
	.seh_endproc
	.section	.text$_ZSt3minIyERKT_S2_S2_,"x"
	.linkonce discard
	.globl	_ZSt3minIyERKT_S2_S2_
	.def	_ZSt3minIyERKT_S2_S2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt3minIyERKT_S2_S2_
_ZSt3minIyERKT_S2_S2_:
.LFB1779:
	.file 13 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_algobase.h"
	.loc 13 234 5
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
	mov	QWORD PTR 24[rbp], rdx
	.loc 13 239 15
	mov	rax, QWORD PTR 24[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 13 239 7
	cmp	rdx, rax
	jnb	.L61
	.loc 13 240 9
	mov	rax, QWORD PTR 24[rbp]
	jmp	.L62
.L61:
	.loc 13 241 14
	mov	rax, QWORD PTR 16[rbp]
.L62:
	.loc 13 242 5
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1779:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_dataC2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_dataC2Ev
	.def	_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_dataC2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_dataC2Ev
_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_dataC2Ev:
.LFB1784:
	.loc 7 105 2
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
.LBB160:
	.loc 7 106 4
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], 0
	.loc 7 106 16
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR 8[rax], 0
	.loc 7 106 29
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR 16[rax], 0
.LBE160:
	.loc 7 107 4
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1784:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI7MonsterSaIS0_EE11_M_allocateEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI7MonsterSaIS0_EE11_M_allocateEy
	.def	_ZNSt12_Vector_baseI7MonsterSaIS0_EE11_M_allocateEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI7MonsterSaIS0_EE11_M_allocateEy
_ZNSt12_Vector_baseI7MonsterSaIS0_EE11_M_allocateEy:
.LFB1786:
	.loc 7 384 7
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	.loc 7 387 18
	cmp	QWORD PTR 24[rbp], 0
	je	.L65
	.loc 7 387 34 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR -16[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -24[rbp], rax
	mov	rax, QWORD PTR -16[rbp]
	mov	QWORD PTR -32[rbp], rax
.LBB161:
.LBB162:
.LBB163:
.LBB164:
.LBB165:
.LBB166:
	.loc 9 586 49
	mov	eax, 0
.LBE166:
.LBE165:
	.loc 6 196 2 discriminator 1
	test	al, al
	je	.L67
	.loc 6 198 32
	mov	rax, QWORD PTR -32[rbp]
	mov	ecx, 0
	mov	rdx, rax
	sal	rdx, 4
	shr	rax, 60
	test	rax, rax
	je	.L68
	mov	ecx, 1
.L68:
	mov	rax, rdx
	.loc 6 198 32 is_stmt 0 discriminator 1
	mov	QWORD PTR -32[rbp], rax
	mov	rax, rcx
	and	eax, 1
	.loc 6 198 6 is_stmt 1 discriminator 1
	test	al, al
	je	.L70
	.loc 6 199 41
	call	_ZSt28__throw_bad_array_new_lengthv
.L70:
	.loc 6 200 45
	mov	rax, QWORD PTR -32[rbp]
	mov	rcx, rax
	call	_Znwy
	.loc 6 200 50
	jmp	.L71
.L67:
	.loc 6 203 40
	mov	rdx, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR -24[rbp]
	mov	r8d, 0
	mov	rcx, rax
	call	_ZNSt15__new_allocatorI7MonsterE8allocateEyPKv
	.loc 6 203 47
	nop
.L71:
.LBE164:
.LBE163:
	.loc 8 614 32
	nop
	jmp	.L73
.L65:
.LBE162:
.LBE161:
	.loc 7 387 58 discriminator 2
	mov	eax, 0
.L73:
	.loc 7 388 7
	add	rsp, 64
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1786:
	.seh_endproc
	.section	.text$_ZSt25__uninitialized_default_nIP7MonsteryET_S2_T0_,"x"
	.linkonce discard
	.globl	_ZSt25__uninitialized_default_nIP7MonsteryET_S2_T0_
	.def	_ZSt25__uninitialized_default_nIP7MonsteryET_S2_T0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt25__uninitialized_default_nIP7MonsteryET_S2_T0_
_ZSt25__uninitialized_default_nIP7MonsteryET_S2_T0_:
.LFB1788:
	.loc 10 958 5
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	.loc 10 961 37
	call	_ZSt21is_constant_evaluatedv
	.loc 10 961 7 discriminator 1
	test	al, al
	je	.L76
	.loc 10 963 22
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP7MonsteryEET_S4_T0_
	.loc 10 963 35
	jmp	.L77
.L76:
	.loc 10 969 22
	mov	BYTE PTR -1[rbp], 1
	.loc 10 974 20
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP7MonsteryEET_S4_T0_
	.loc 10 974 33
	nop
.L77:
	.loc 10 975 5
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1788:
	.seh_endproc
	.section	.text$_ZSt8_DestroyI7MonsterEvPT_,"x"
	.linkonce discard
	.globl	_ZSt8_DestroyI7MonsterEvPT_
	.def	_ZSt8_DestroyI7MonsterEvPT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt8_DestroyI7MonsterEvPT_
_ZSt8_DestroyI7MonsterEvPT_:
.LFB1790:
	.loc 11 161 5
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 11 164 22
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZSt10destroy_atI7MonsterEvPT_
	.loc 11 168 5
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1790:
	.seh_endproc
	.section	.text$_ZNSt19_UninitDestroyGuardIP7MonstervEC1ERS1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt19_UninitDestroyGuardIP7MonstervEC1ERS1_
	.def	_ZNSt19_UninitDestroyGuardIP7MonstervEC1ERS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_UninitDestroyGuardIP7MonstervEC1ERS1_
_ZNSt19_UninitDestroyGuardIP7MonstervEC1ERS1_:
.LFB1796:
	.loc 10 113 7
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
	mov	QWORD PTR 24[rbp], rdx
.LBB167:
	.loc 10 114 9
	mov	rax, QWORD PTR 24[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	.loc 10 114 28
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR 8[rax], rdx
.LBE167:
	.loc 10 115 9
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1796:
	.seh_endproc
	.section	.text$_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP7MonsteryEET_S4_T0_,"x"
	.linkonce discard
	.globl	_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP7MonsteryEET_S4_T0_
	.def	_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP7MonsteryEET_S4_T0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP7MonsteryEET_S4_T0_
_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP7MonsteryEET_S4_T0_:
.LFB1793:
	.loc 10 899 9
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	sub	rsp, 72
	.seh_stackalloc	72
	.cfi_def_cfa_offset 96
	lea	rbp, 64[rsp]
	.seh_setframe	rbp, 64
	.cfi_def_cfa 6, 32
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	QWORD PTR 40[rbp], rdx
	.loc 10 901 42
	lea	rax, -32[rbp]
	lea	rdx, 32[rbp]
	mov	rcx, rax
	call	_ZNSt19_UninitDestroyGuardIP7MonstervEC1ERS1_
	.loc 10 902 4
	jmp	.L81
.L83:
	.loc 10 903 21
	mov	rax, QWORD PTR 32[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB168:
.LBB169:
	.loc 12 53 37
	mov	rax, QWORD PTR -8[rbp]
.LBE169:
.LBE168:
	.loc 10 903 21 discriminator 1
	mov	rcx, rax
	call	_ZSt10_ConstructI7MonsterJEEvPT_DpOT0_
	.loc 10 902 4 discriminator 2
	sub	QWORD PTR 40[rbp], 1
	.loc 10 902 27 discriminator 2
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	QWORD PTR 32[rbp], rax
.L81:
	.loc 10 902 15 discriminator 1
	cmp	QWORD PTR 40[rbp], 0
	jne	.L83
	.loc 10 904 19
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZNSt19_UninitDestroyGuardIP7MonstervE7releaseEv
	.loc 10 905 11
	mov	rbx, QWORD PTR 32[rbp]
	.loc 10 906 2
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZNSt19_UninitDestroyGuardIP7MonstervED1Ev
	.loc 10 905 11
	mov	rax, rbx
	.loc 10 906 2
	add	rsp, 72
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -56
	ret
	.cfi_endproc
.LFE1793:
	.seh_endproc
	.section	.text$_ZN10GameObjectD2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN10GameObjectD2Ev
	.def	_ZN10GameObjectD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN10GameObjectD2Ev
_ZN10GameObjectD2Ev:
.LFB1800:
	.loc 3 8 13
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
.LBB170:
	.loc 3 8 13
	lea	rdx, _ZTV10GameObject[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
.LBE170:
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1800:
	.seh_endproc
	.section	.text$_ZN7MonsterD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN7MonsterD1Ev
	.def	_ZN7MonsterD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7MonsterD1Ev
_ZN7MonsterD1Ev:
.LFB1804:
	.loc 3 13 8
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB171:
	.loc 3 13 8
	lea	rdx, _ZTV7Monster[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN10GameObjectD2Ev
.LBE171:
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1804:
	.seh_endproc
	.section	.text$_ZN7MonsterD0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN7MonsterD0Ev
	.def	_ZN7MonsterD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7MonsterD0Ev
_ZN7MonsterD0Ev:
.LFB1805:
	.loc 3 13 8
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 3 13 8
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN7MonsterD1Ev
	.loc 3 13 8 is_stmt 0 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 16
	mov	rcx, rax
	call	_ZdlPvy
	nop
	.loc 3 13 8
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1805:
	.seh_endproc
	.section	.text$_ZSt10destroy_atI7MonsterEvPT_,"x"
	.linkonce discard
	.globl	_ZSt10destroy_atI7MonsterEvPT_
	.def	_ZSt10destroy_atI7MonsterEvPT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt10destroy_atI7MonsterEvPT_
_ZSt10destroy_atI7MonsterEvPT_:
.LFB1797:
	.loc 11 80 5 is_stmt 1
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	.loc 11 88 18
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
.LVL0:
	.loc 11 89 5
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1797:
	.seh_endproc
	.section	.text$_ZNSt15__new_allocatorI7MonsterE10deallocateEPS0_y,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt15__new_allocatorI7MonsterE10deallocateEPS0_y
	.def	_ZNSt15__new_allocatorI7MonsterE10deallocateEPS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15__new_allocatorI7MonsterE10deallocateEPS0_y
_ZNSt15__new_allocatorI7MonsterE10deallocateEPS0_y:
.LFB1807:
	.loc 5 156 7
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	.loc 5 172 59
	mov	rax, QWORD PTR 32[rbp]
	sal	rax, 4
	mov	rdx, rax
	mov	rax, QWORD PTR 24[rbp]
	mov	rcx, rax
	call	_ZdlPvy
	nop
	.loc 5 173 7
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1807:
	.seh_endproc
	.section	.text$_ZNSt19_UninitDestroyGuardIP7MonstervED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt19_UninitDestroyGuardIP7MonstervED1Ev
	.def	_ZNSt19_UninitDestroyGuardIP7MonstervED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_UninitDestroyGuardIP7MonstervED1Ev
_ZNSt19_UninitDestroyGuardIP7MonstervED1Ev:
.LFB1810:
	.loc 10 118 7
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB172:
	.loc 10 120 23
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	.loc 10 120 30
	test	rax, rax
	setne	al
	.loc 10 120 22
	movzx	eax, al
	.loc 10 120 2 discriminator 1
	test	eax, eax
	je	.L93
	.loc 10 121 29
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR 8[rax]
	.loc 10 121 17
	mov	rdx, QWORD PTR [rax]
	.loc 10 121 18
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 10 121 17
	mov	rcx, rax
	call	_ZSt8_DestroyIP7MonsterEvT_S2_
.L93:
.LBE172:
	.loc 10 122 7
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1810:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1810:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1810-.LLSDACSB1810
.LLSDACSB1810:
.LLSDACSE1810:
	.section	.text$_ZNSt19_UninitDestroyGuardIP7MonstervED1Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZN10GameObjectC2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN10GameObjectC2Ev
	.def	_ZN10GameObjectC2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN10GameObjectC2Ev
_ZN10GameObjectC2Ev:
.LFB1814:
	.loc 3 7 8
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
.LBB173:
	.loc 3 7 8
	lea	rdx, _ZTV10GameObject[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
.LBE173:
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1814:
	.seh_endproc
	.section	.text$_ZN7MonsterC1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN7MonsterC1Ev
	.def	_ZN7MonsterC1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7MonsterC1Ev
_ZN7MonsterC1Ev:
.LFB1817:
	.loc 3 13 8
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
.LBB174:
	.loc 3 13 8
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN10GameObjectC2Ev
	.loc 3 13 8 is_stmt 0 discriminator 1
	lea	rdx, _ZTV7Monster[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
.LBE174:
	.loc 3 13 8
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1817:
	.seh_endproc
	.section	.text$_ZSt10_ConstructI7MonsterJEEvPT_DpOT0_,"x"
	.linkonce discard
	.globl	_ZSt10_ConstructI7MonsterJEEvPT_DpOT0_
	.def	_ZSt10_ConstructI7MonsterJEEvPT_DpOT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt10_ConstructI7MonsterJEEvPT_DpOT0_
_ZSt10_ConstructI7MonsterJEEvPT_DpOT0_:
.LFB1811:
	.loc 11 123 5 is_stmt 1
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rsi
	.seh_pushreg	rsi
	.cfi_def_cfa_offset 24
	.cfi_offset 4, -24
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	sub	rsp, 32
	.seh_stackalloc	32
	.cfi_def_cfa_offset 64
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.cfi_def_cfa 6, 32
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
.LBB175:
.LBB176:
	.loc 9 586 49
	mov	eax, 0
.LBE176:
.LBE175:
	.loc 11 126 7 discriminator 1
	test	al, al
	je	.L98
	.loc 11 129 21
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZSt12construct_atI7MonsterJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
	.loc 11 130 4
	jmp	.L96
.L98:
	.loc 11 133 13
	mov	rsi, QWORD PTR 32[rbp]
	.loc 11 133 7
	mov	rdx, rsi
	mov	ecx, 16
	call	_ZnwyPv
	mov	rbx, rax
	.loc 11 133 7 is_stmt 0 discriminator 1
	mov	QWORD PTR [rbx], 0
	pxor	xmm0, xmm0
	movss	DWORD PTR 8[rbx], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 12[rbx], xmm0
	mov	rcx, rbx
	call	_ZN7MonsterC1Ev
	.loc 11 133 7 discriminator 2
	mov	eax, 0
	test	al, al
	je	.L96
	.loc 11 133 7 discriminator 3
	mov	rdx, rsi
	mov	rcx, rbx
	call	_ZdlPvS_
	nop
.L96:
	.loc 11 134 5 is_stmt 1
	add	rsp, 32
	pop	rbx
	.cfi_restore 3
	pop	rsi
	.cfi_restore 4
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -8
	ret
	.cfi_endproc
.LFE1811:
	.seh_endproc
	.section	.text$_ZNSt19_UninitDestroyGuardIP7MonstervE7releaseEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt19_UninitDestroyGuardIP7MonstervE7releaseEv
	.def	_ZNSt19_UninitDestroyGuardIP7MonstervE7releaseEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_UninitDestroyGuardIP7MonstervE7releaseEv
_ZNSt19_UninitDestroyGuardIP7MonstervE7releaseEv:
.LFB1818:
	.loc 10 125 12
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
	.loc 10 125 31
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR 8[rax], 0
	.loc 10 125 36
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1818:
	.seh_endproc
	.section	.text$_ZNSt15__new_allocatorI7MonsterE8allocateEyPKv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt15__new_allocatorI7MonsterE8allocateEyPKv
	.def	_ZNSt15__new_allocatorI7MonsterE8allocateEyPKv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15__new_allocatorI7MonsterE8allocateEyPKv
_ZNSt15__new_allocatorI7MonsterE8allocateEyPKv:
.LFB1819:
	.loc 5 126 7
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB177:
.LBB178:
	.loc 5 233 50
	movabs	rax, 576460752303423487
.LBE178:
.LBE177:
	.loc 5 134 27 discriminator 1
	cmp	rax, QWORD PTR 24[rbp]
	setb	al
	.loc 5 134 22 discriminator 1
	movzx	eax, al
	.loc 5 134 22 is_stmt 0 discriminator 2
	test	eax, eax
	setne	al
	.loc 5 134 2 is_stmt 1 discriminator 2
	test	al, al
	je	.L103
	.loc 5 138 6
	movabs	rax, 1152921504606846975
	cmp	rax, QWORD PTR 24[rbp]
	jnb	.L104
	.loc 5 139 41
	call	_ZSt28__throw_bad_array_new_lengthv
.L104:
	.loc 5 140 28
	call	_ZSt17__throw_bad_allocv
.L103:
	.loc 5 151 66
	mov	rax, QWORD PTR 24[rbp]
	sal	rax, 4
	mov	rcx, rax
	call	_Znwy
	.loc 5 151 67
	nop
	.loc 5 152 7
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1819:
	.seh_endproc
	.section	.text$_ZSt12construct_atI7MonsterJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_,"x"
	.linkonce discard
	.globl	_ZSt12construct_atI7MonsterJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
	.def	_ZSt12construct_atI7MonsterJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt12construct_atI7MonsterJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
_ZSt12construct_atI7MonsterJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_:
.LFB1820:
	.loc 11 96 5
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	push	rsi
	.seh_pushreg	rsi
	.cfi_def_cfa_offset 24
	.cfi_offset 4, -24
	push	rbx
	.seh_pushreg	rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	sub	rsp, 48
	.seh_stackalloc	48
	.cfi_def_cfa_offset 80
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.cfi_def_cfa 6, 32
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	.loc 11 99 13
	mov	rax, QWORD PTR 32[rbp]
	mov	QWORD PTR -8[rbp], rax
	.loc 11 110 15
	mov	rsi, QWORD PTR -8[rbp]
	.loc 11 110 9
	mov	rdx, rsi
	mov	ecx, 16
	call	_ZnwyPv
	mov	rbx, rax
	.loc 11 110 9 is_stmt 0 discriminator 1
	mov	QWORD PTR [rbx], 0
	pxor	xmm0, xmm0
	movss	DWORD PTR 8[rbx], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 12[rbx], xmm0
	mov	rcx, rbx
	call	_ZN7MonsterC1Ev
	.loc 11 110 56 is_stmt 1 discriminator 2
	mov	eax, 0
	.loc 11 110 56 is_stmt 0 discriminator 3
	test	al, al
	je	.L108
	.loc 11 110 9 is_stmt 1 discriminator 4
	mov	rdx, rsi
	mov	rcx, rbx
	call	_ZdlPvS_
.L108:
	.loc 11 110 56 discriminator 8
	mov	rax, rbx
	.loc 11 111 5
	add	rsp, 48
	pop	rbx
	.cfi_restore 3
	pop	rsi
	.cfi_restore 4
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -24
	ret
	.cfi_endproc
.LFE1820:
	.seh_endproc
	.weak	_ZSt12construct_atI7MonsterJEEPT_S2_DpOT0_
	.def	_ZSt12construct_atI7MonsterJEEPT_S2_DpOT0_;	.scl	2;	.type	32;	.endef
	.set	_ZSt12construct_atI7MonsterJEEPT_S2_DpOT0_,_ZSt12construct_atI7MonsterJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
	.globl	_ZTV7Monster
	.section	.rdata$_ZTV7Monster,"dr"
	.linkonce same_size
	.align 8
_ZTV7Monster:
	.quad	0
	.quad	_ZTI7Monster
	.quad	_ZN7MonsterD1Ev
	.quad	_ZN7MonsterD0Ev
	.quad	_ZN7Monster6updateEv
	.globl	_ZTV10GameObject
	.section	.rdata$_ZTV10GameObject,"dr"
	.linkonce same_size
	.align 8
_ZTV10GameObject:
	.quad	0
	.quad	_ZTI10GameObject
	.quad	0
	.quad	0
	.quad	__cxa_pure_virtual
	.globl	_ZTI7Monster
	.section	.rdata$_ZTI7Monster,"dr"
	.linkonce same_size
	.align 8
_ZTI7Monster:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS7Monster
	.quad	_ZTI10GameObject
	.globl	_ZTS7Monster
	.section	.rdata$_ZTS7Monster,"dr"
	.linkonce same_size
	.align 8
_ZTS7Monster:
	.ascii "7Monster\0"
	.globl	_ZTI10GameObject
	.section	.rdata$_ZTI10GameObject,"dr"
	.linkonce same_size
	.align 8
_ZTI10GameObject:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS10GameObject
	.globl	_ZTS10GameObject
	.section	.rdata$_ZTS10GameObject,"dr"
	.linkonce same_size
	.align 8
_ZTS10GameObject:
	.ascii "10GameObject\0"
	.section .rdata,"dr"
	.align 4
.LC0:
	.long	1065353216
	.weak	__cxa_pure_virtual
	.text
.Letext0:
	.file 14 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/utility.h"
	.file 15 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/concepts"
	.file 16 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/iterator_concepts.h"
	.file 17 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/compare"
	.file 18 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/debug/debug.h"
	.file 19 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/numbers"
	.file 20 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/memory_resource.h"
	.file 21 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/cstddef"
	.file 22 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/vector.tcc"
	.file 23 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_iterator_base_types.h"
	.file 24 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/initializer_list"
	.file 25 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/functexcept.h"
	.file 26 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/predefined_ops.h"
	.file 27 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/ext/alloc_traits.h"
	.file 28 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/ptr_traits.h"
	.file 29 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/stddef.h"
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0x93ca
	.word	0x5
	.byte	0x1
	.byte	0x8
	.secrel32	.Ldebug_abbrev0
	.uleb128 0x65
	.ascii "GNU C++23 15.3.0 -masm=intel -mtune=generic -march=x86-64 -g -O0 -std=c++23\0"
	.byte	0x21
	.byte	0x4
	.long	0x3163e
	.secrel32	.LASF0
	.secrel32	.LASF1
	.secrel32	.LLRL0
	.quad	0
	.secrel32	.Ldebug_line0
	.uleb128 0x45
	.ascii "std\0"
	.byte	0x9
	.word	0x150
	.byte	0xb
	.long	0x679c
	.uleb128 0x17
	.ascii "integral_constant<bool, true>\0"
	.byte	0x1
	.byte	0x1
	.byte	0x5d
	.byte	0xc
	.long	0x17c
	.uleb128 0x11
	.secrel32	.LASF3
	.byte	0x1
	.byte	0x60
	.byte	0xd
	.long	0x679c
	.uleb128 0x54
	.ascii "operator std::integral_constant<bool, true>::value_type\0"
	.byte	0x62
	.ascii "_ZNKSt17integral_constantIbLb1EEcvbEv\0"
	.long	0xab
	.long	0x123
	.long	0x129
	.uleb128 0x2
	.long	0x67a9
	.byte	0
	.uleb128 0x39
	.secrel32	.LASF2
	.byte	0x1
	.byte	0x65
	.byte	0x1c
	.ascii "_ZNKSt17integral_constantIbLb1EEclEv\0"
	.long	0xab
	.long	0x162
	.long	0x168
	.uleb128 0x2
	.long	0x67a9
	.byte	0
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x679c
	.uleb128 0x46
	.ascii "__v\0"
	.long	0x679c
	.byte	0x1
	.byte	0
	.uleb128 0x3
	.long	0x84
	.uleb128 0x17
	.ascii "integral_constant<bool, false>\0"
	.byte	0x1
	.byte	0x1
	.byte	0x5d
	.byte	0xc
	.long	0x27b
	.uleb128 0x11
	.secrel32	.LASF3
	.byte	0x1
	.byte	0x60
	.byte	0xd
	.long	0x679c
	.uleb128 0x54
	.ascii "operator std::integral_constant<bool, false>::value_type\0"
	.byte	0x62
	.ascii "_ZNKSt17integral_constantIbLb0EEcvbEv\0"
	.long	0x1a9
	.long	0x222
	.long	0x228
	.uleb128 0x2
	.long	0x67ae
	.byte	0
	.uleb128 0x39
	.secrel32	.LASF2
	.byte	0x1
	.byte	0x65
	.byte	0x1c
	.ascii "_ZNKSt17integral_constantIbLb0EEclEv\0"
	.long	0x1a9
	.long	0x261
	.long	0x267
	.uleb128 0x2
	.long	0x67ae
	.byte	0
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x679c
	.uleb128 0x46
	.ascii "__v\0"
	.long	0x679c
	.byte	0
	.byte	0
	.uleb128 0x3
	.long	0x181
	.uleb128 0x55
	.ascii "size_t\0"
	.word	0x152
	.byte	0x1a
	.long	0x67b3
	.uleb128 0x3
	.long	0x280
	.uleb128 0x31
	.ascii "__swappable_details\0"
	.byte	0x1
	.word	0xb93
	.byte	0xd
	.uleb128 0x31
	.ascii "__swappable_with_details\0"
	.byte	0x1
	.word	0xbe8
	.byte	0xd
	.uleb128 0x45
	.ascii "ranges\0"
	.byte	0xe
	.word	0x113
	.byte	0xd
	.long	0x320
	.uleb128 0x29
	.ascii "__swap\0"
	.byte	0xf
	.byte	0xbf
	.byte	0xf
	.uleb128 0x66
	.ascii "_Cpo\0"
	.byte	0xf
	.byte	0xfc
	.byte	0x16
	.uleb128 0x29
	.ascii "__imove\0"
	.byte	0x10
	.byte	0x6b
	.byte	0xf
	.uleb128 0x31
	.ascii "__iswap\0"
	.byte	0x10
	.word	0x37b
	.byte	0xd
	.uleb128 0x31
	.ascii "__access\0"
	.byte	0x10
	.word	0x3fd
	.byte	0x15
	.uleb128 0x67
	.secrel32	.LASF4
	.byte	0xe
	.word	0x113
	.byte	0x15
	.byte	0
	.uleb128 0x29
	.ascii "__cmp_cat\0"
	.byte	0x11
	.byte	0x34
	.byte	0xd
	.uleb128 0x68
	.secrel32	.LASF4
	.byte	0x1
	.byte	0xad
	.byte	0xd
	.uleb128 0x31
	.ascii "__compare\0"
	.byte	0x11
	.word	0x23e
	.byte	0xd
	.uleb128 0x69
	.ascii "_Cpo\0"
	.byte	0x11
	.word	0x4ab
	.byte	0x14
	.uleb128 0x6a
	.ascii "align_val_t\0"
	.byte	0x7
	.byte	0x8
	.long	0x67b3
	.byte	0x2
	.byte	0x64
	.byte	0xe
	.uleb128 0x29
	.ascii "__debug\0"
	.byte	0x12
	.byte	0x32
	.byte	0xd
	.uleb128 0x55
	.ascii "ptrdiff_t\0"
	.word	0x153
	.byte	0x1c
	.long	0x684d
	.uleb128 0x2c
	.ascii "true_type\0"
	.byte	0x1
	.byte	0x75
	.byte	0x9
	.long	0x395
	.uleb128 0x11
	.secrel32	.LASF5
	.byte	0x1
	.byte	0x71
	.byte	0xb
	.long	0x84
	.uleb128 0x2c
	.ascii "false_type\0"
	.byte	0x1
	.byte	0x78
	.byte	0x9
	.long	0x3b4
	.uleb128 0x11
	.secrel32	.LASF5
	.byte	0x1
	.byte	0x71
	.byte	0xb
	.long	0x181
	.uleb128 0x47
	.ascii "__uninitialized_default_n_1<false>\0"
	.byte	0xa
	.word	0x37e
	.long	0x4b4
	.uleb128 0x48
	.ascii "__uninit_default_n<Monster*, long long unsigned int>\0"
	.word	0x383
	.byte	0x9
	.ascii "_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP7MonsteryEET_S4_T0_\0"
	.long	0x7b28
	.long	0x49b
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0xb
	.secrel32	.LASF7
	.long	0x67b3
	.uleb128 0x1
	.long	0x7b28
	.uleb128 0x1
	.long	0x67b3
	.byte	0
	.uleb128 0x46
	.ascii "_TrivialValueType\0"
	.long	0x679c
	.byte	0
	.byte	0
	.uleb128 0x29
	.ascii "numbers\0"
	.byte	0x13
	.byte	0x38
	.byte	0xb
	.uleb128 0x22
	.byte	0x15
	.byte	0x42
	.byte	0xb
	.long	0x7897
	.uleb128 0x29
	.ascii "pmr\0"
	.byte	0x14
	.byte	0x37
	.byte	0xb
	.uleb128 0x32
	.ascii "__new_allocator<MonsterData>\0"
	.byte	0x1
	.byte	0x5
	.byte	0x3f
	.long	0x6e5
	.uleb128 0x16
	.secrel32	.LASF8
	.byte	0x5
	.byte	0x58
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI11MonsterDataEC4Ev\0"
	.byte	0x1
	.long	0x530
	.long	0x536
	.uleb128 0x2
	.long	0x78de
	.byte	0
	.uleb128 0x16
	.secrel32	.LASF8
	.byte	0x5
	.byte	0x5c
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI11MonsterDataEC4ERKS1_\0"
	.byte	0x1
	.long	0x575
	.long	0x580
	.uleb128 0x2
	.long	0x78de
	.uleb128 0x1
	.long	0x78e3
	.byte	0
	.uleb128 0x3a
	.secrel32	.LASF12
	.byte	0x5
	.byte	0x64
	.byte	0x18
	.ascii "_ZNSt15__new_allocatorI11MonsterDataEaSERKS1_\0"
	.long	0x78e8
	.long	0x5c2
	.long	0x5cd
	.uleb128 0x2
	.long	0x78de
	.uleb128 0x1
	.long	0x78e3
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF14
	.byte	0x5
	.byte	0x7e
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI11MonsterDataE8allocateEyPKv\0"
	.long	0x78ed
	.byte	0x1
	.long	0x616
	.long	0x626
	.uleb128 0x2
	.long	0x78de
	.uleb128 0x1
	.long	0x626
	.uleb128 0x1
	.long	0x782e
	.byte	0
	.uleb128 0x33
	.secrel32	.LASF17
	.byte	0x5
	.byte	0x43
	.byte	0x1f
	.long	0x280
	.uleb128 0x16
	.secrel32	.LASF9
	.byte	0x5
	.byte	0x9c
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI11MonsterDataE10deallocateEPS0_y\0"
	.byte	0x1
	.long	0x67b
	.long	0x68b
	.uleb128 0x2
	.long	0x78de
	.uleb128 0x1
	.long	0x78ed
	.uleb128 0x1
	.long	0x626
	.byte	0
	.uleb128 0x39
	.secrel32	.LASF10
	.byte	0x5
	.byte	0xe6
	.byte	0x7
	.ascii "_ZNKSt15__new_allocatorI11MonsterDataE11_M_max_sizeEv\0"
	.long	0x626
	.long	0x6d5
	.long	0x6db
	.uleb128 0x2
	.long	0x78f7
	.byte	0
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x78ad
	.byte	0
	.uleb128 0x3
	.long	0x4d0
	.uleb128 0x32
	.ascii "allocator<MonsterData>\0"
	.byte	0x1
	.byte	0x6
	.byte	0x85
	.long	0x865
	.uleb128 0x3b
	.long	0x4d0
	.byte	0x1
	.uleb128 0x16
	.secrel32	.LASF11
	.byte	0x6
	.byte	0xa8
	.byte	0x7
	.ascii "_ZNSaI11MonsterDataEC4Ev\0"
	.byte	0x1
	.long	0x739
	.long	0x73f
	.uleb128 0x2
	.long	0x78fc
	.byte	0
	.uleb128 0x16
	.secrel32	.LASF11
	.byte	0x6
	.byte	0xac
	.byte	0x7
	.ascii "_ZNSaI11MonsterDataEC4ERKS0_\0"
	.byte	0x1
	.long	0x76d
	.long	0x778
	.uleb128 0x2
	.long	0x78fc
	.uleb128 0x1
	.long	0x7901
	.byte	0
	.uleb128 0x3a
	.secrel32	.LASF12
	.byte	0x6
	.byte	0xb1
	.byte	0x12
	.ascii "_ZNSaI11MonsterDataEaSERKS0_\0"
	.long	0x7906
	.long	0x7a9
	.long	0x7b4
	.uleb128 0x2
	.long	0x78fc
	.uleb128 0x1
	.long	0x7901
	.byte	0
	.uleb128 0x16
	.secrel32	.LASF13
	.byte	0x6
	.byte	0xbd
	.byte	0x7
	.ascii "_ZNSaI11MonsterDataED4Ev\0"
	.byte	0x1
	.long	0x7de
	.long	0x7e4
	.uleb128 0x2
	.long	0x78fc
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF14
	.byte	0x6
	.byte	0xc2
	.byte	0x7
	.ascii "_ZNSaI11MonsterDataE8allocateEy\0"
	.long	0x78ed
	.byte	0x1
	.long	0x819
	.long	0x824
	.uleb128 0x2
	.long	0x78fc
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x56
	.secrel32	.LASF9
	.byte	0xd0
	.ascii "_ZNSaI11MonsterDataE10deallocateEPS_y\0"
	.long	0x854
	.uleb128 0x2
	.long	0x78fc
	.uleb128 0x1
	.long	0x78ed
	.uleb128 0x1
	.long	0x280
	.byte	0
	.byte	0
	.uleb128 0x3
	.long	0x6ea
	.uleb128 0x47
	.ascii "allocator_traits<std::allocator<MonsterData> >\0"
	.byte	0x8
	.word	0x230
	.long	0xabf
	.uleb128 0x14
	.secrel32	.LASF15
	.byte	0x8
	.word	0x239
	.byte	0xd
	.long	0x78ed
	.uleb128 0x13
	.secrel32	.LASF14
	.byte	0x8
	.word	0x265
	.ascii "_ZNSt16allocator_traitsISaI11MonsterDataEE8allocateERS1_y\0"
	.long	0x8a1
	.long	0x903
	.uleb128 0x1
	.long	0x790b
	.uleb128 0x1
	.long	0x915
	.byte	0
	.uleb128 0x14
	.secrel32	.LASF16
	.byte	0x8
	.word	0x233
	.byte	0xd
	.long	0x6ea
	.uleb128 0x3
	.long	0x903
	.uleb128 0x14
	.secrel32	.LASF17
	.byte	0x8
	.word	0x248
	.byte	0xd
	.long	0x280
	.uleb128 0x13
	.secrel32	.LASF14
	.byte	0x8
	.word	0x274
	.ascii "_ZNSt16allocator_traitsISaI11MonsterDataEE8allocateERS1_yPKv\0"
	.long	0x8a1
	.long	0x97f
	.uleb128 0x1
	.long	0x790b
	.uleb128 0x1
	.long	0x915
	.uleb128 0x1
	.long	0x97f
	.byte	0
	.uleb128 0x14
	.secrel32	.LASF18
	.byte	0x8
	.word	0x242
	.byte	0xd
	.long	0x782e
	.uleb128 0x57
	.secrel32	.LASF9
	.ascii "_ZNSt16allocator_traitsISaI11MonsterDataEE10deallocateERS1_PS0_y\0"
	.long	0x9e6
	.uleb128 0x1
	.long	0x790b
	.uleb128 0x1
	.long	0x8a1
	.uleb128 0x1
	.long	0x915
	.byte	0
	.uleb128 0x13
	.secrel32	.LASF19
	.byte	0x8
	.word	0x2c5
	.ascii "_ZNSt16allocator_traitsISaI11MonsterDataEE8max_sizeERKS1_\0"
	.long	0x915
	.long	0xa36
	.uleb128 0x1
	.long	0x7910
	.byte	0
	.uleb128 0x13
	.secrel32	.LASF20
	.byte	0x8
	.word	0x2d5
	.ascii "_ZNSt16allocator_traitsISaI11MonsterDataEE37select_on_container_copy_constructionERKS1_\0"
	.long	0x903
	.long	0xaa4
	.uleb128 0x1
	.long	0x7910
	.byte	0
	.uleb128 0x14
	.secrel32	.LASF3
	.byte	0x8
	.word	0x236
	.byte	0xd
	.long	0x78ad
	.uleb128 0x14
	.secrel32	.LASF21
	.byte	0x8
	.word	0x257
	.byte	0x8
	.long	0x6ea
	.byte	0
	.uleb128 0x17
	.ascii "_Vector_base<MonsterData, std::allocator<MonsterData> >\0"
	.byte	0x18
	.byte	0x7
	.byte	0x5b
	.byte	0xc
	.long	0x1403
	.uleb128 0x3c
	.secrel32	.LASF22
	.byte	0x62
	.long	0xcb3
	.uleb128 0x2d
	.secrel32	.LASF23
	.byte	0x64
	.long	0xcb8
	.byte	0
	.uleb128 0x2d
	.secrel32	.LASF24
	.byte	0x65
	.long	0xcb8
	.byte	0x8
	.uleb128 0x2d
	.secrel32	.LASF25
	.byte	0x66
	.long	0xcb8
	.byte	0x10
	.uleb128 0x15
	.secrel32	.LASF22
	.byte	0x7
	.byte	0x69
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE17_Vector_impl_dataC4Ev\0"
	.long	0xb7c
	.long	0xb82
	.uleb128 0x2
	.long	0x7924
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF22
	.byte	0x7
	.byte	0x6f
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE17_Vector_impl_dataC4EOS3_\0"
	.long	0xbd6
	.long	0xbe1
	.uleb128 0x2
	.long	0x7924
	.uleb128 0x1
	.long	0x7929
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF26
	.byte	0x7
	.byte	0x77
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE17_Vector_impl_data12_M_copy_dataERKS3_\0"
	.long	0xc42
	.long	0xc4d
	.uleb128 0x2
	.long	0x7924
	.uleb128 0x1
	.long	0x792e
	.byte	0
	.uleb128 0x49
	.secrel32	.LASF27
	.byte	0x80
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE17_Vector_impl_data12_M_swap_dataERS3_\0"
	.long	0xca7
	.uleb128 0x2
	.long	0x7924
	.uleb128 0x1
	.long	0x7933
	.byte	0
	.byte	0
	.uleb128 0x3
	.long	0xb00
	.uleb128 0x11
	.secrel32	.LASF15
	.byte	0x7
	.byte	0x60
	.byte	0x9
	.long	0x6b95
	.uleb128 0x3c
	.secrel32	.LASF28
	.byte	0x8b
	.long	0xef9
	.uleb128 0x2a
	.long	0x6ea
	.uleb128 0x2a
	.long	0xb00
	.uleb128 0x15
	.secrel32	.LASF28
	.byte	0x7
	.byte	0x8f
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE12_Vector_implC4EvQ26is_default_constructible_vIN9__gnu_cxx14__alloc_traitsIT0_NS6_10value_typeEE6rebindIT_E5otherEE\0"
	.long	0xd86
	.long	0xd8c
	.uleb128 0x2
	.long	0x7938
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF28
	.byte	0x7
	.byte	0x98
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE12_Vector_implC4ERKS1_\0"
	.long	0xddc
	.long	0xde7
	.uleb128 0x2
	.long	0x7938
	.uleb128 0x1
	.long	0x793d
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF28
	.byte	0x7
	.byte	0xa0
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE12_Vector_implC4EOS3_\0"
	.long	0xe36
	.long	0xe41
	.uleb128 0x2
	.long	0x7938
	.uleb128 0x1
	.long	0x7942
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF28
	.byte	0x7
	.byte	0xa5
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE12_Vector_implC4EOS1_\0"
	.long	0xe90
	.long	0xe9b
	.uleb128 0x2
	.long	0x7938
	.uleb128 0x1
	.long	0x7947
	.byte	0
	.uleb128 0x49
	.secrel32	.LASF28
	.byte	0xaa
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE12_Vector_implC4EOS1_OS3_\0"
	.long	0xee8
	.uleb128 0x2
	.long	0x7938
	.uleb128 0x1
	.long	0x7947
	.uleb128 0x1
	.long	0x7942
	.byte	0
	.byte	0
	.uleb128 0x11
	.secrel32	.LASF29
	.byte	0x7
	.byte	0x5e
	.byte	0x15
	.long	0x6bd6
	.uleb128 0x3
	.long	0xef9
	.uleb128 0x25
	.secrel32	.LASF30
	.word	0x133
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE19_M_get_Tp_allocatorEv\0"
	.long	0x794c
	.long	0xf5e
	.long	0xf64
	.uleb128 0x2
	.long	0x7951
	.byte	0
	.uleb128 0x25
	.secrel32	.LASF30
	.word	0x138
	.ascii "_ZNKSt12_Vector_baseI11MonsterDataSaIS0_EE19_M_get_Tp_allocatorEv\0"
	.long	0x793d
	.long	0xfb9
	.long	0xfbf
	.uleb128 0x2
	.long	0x7956
	.byte	0
	.uleb128 0x14
	.secrel32	.LASF16
	.byte	0x7
	.word	0x12f
	.byte	0x16
	.long	0x6ea
	.uleb128 0x3
	.long	0xfbf
	.uleb128 0x25
	.secrel32	.LASF31
	.word	0x13d
	.ascii "_ZNKSt12_Vector_baseI11MonsterDataSaIS0_EE13get_allocatorEv\0"
	.long	0xfbf
	.long	0x1020
	.long	0x1026
	.uleb128 0x2
	.long	0x7956
	.byte	0
	.uleb128 0x3d
	.secrel32	.LASF32
	.word	0x141
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EEC4Ev\0"
	.long	0x1063
	.long	0x1069
	.uleb128 0x2
	.long	0x7951
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x147
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EEC4ERKS1_\0"
	.long	0x10aa
	.long	0x10b5
	.uleb128 0x2
	.long	0x7951
	.uleb128 0x1
	.long	0x795b
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x14d
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EEC4Ey\0"
	.long	0x10f2
	.long	0x10fd
	.uleb128 0x2
	.long	0x7951
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x153
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EEC4EyRKS1_\0"
	.long	0x113f
	.long	0x114f
	.uleb128 0x2
	.long	0x7951
	.uleb128 0x1
	.long	0x280
	.uleb128 0x1
	.long	0x795b
	.byte	0
	.uleb128 0x3d
	.secrel32	.LASF32
	.word	0x158
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EEC4EOS2_\0"
	.long	0x118f
	.long	0x119a
	.uleb128 0x2
	.long	0x7951
	.uleb128 0x1
	.long	0x7960
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x15d
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EEC4EOS1_\0"
	.long	0x11da
	.long	0x11e5
	.uleb128 0x2
	.long	0x7951
	.uleb128 0x1
	.long	0x7947
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x161
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EEC4EOS2_RKS1_\0"
	.long	0x122a
	.long	0x123a
	.uleb128 0x2
	.long	0x7951
	.uleb128 0x1
	.long	0x7960
	.uleb128 0x1
	.long	0x795b
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x16f
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EEC4ERKS1_OS2_\0"
	.long	0x127f
	.long	0x128f
	.uleb128 0x2
	.long	0x7951
	.uleb128 0x1
	.long	0x795b
	.uleb128 0x1
	.long	0x7960
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF33
	.word	0x175
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EED4Ev\0"
	.long	0x12cc
	.long	0x12d2
	.uleb128 0x2
	.long	0x7951
	.byte	0
	.uleb128 0x58
	.ascii "_M_impl\0"
	.long	0xcc4
	.uleb128 0x25
	.secrel32	.LASF34
	.word	0x180
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE11_M_allocateEy\0"
	.long	0xcb8
	.long	0x132b
	.long	0x1336
	.uleb128 0x2
	.long	0x7951
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF35
	.word	0x188
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE13_M_deallocateEPS0_y\0"
	.long	0x1384
	.long	0x1394
	.uleb128 0x2
	.long	0x7951
	.uleb128 0x1
	.long	0xcb8
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF36
	.byte	0x7
	.word	0x193
	.byte	0x7
	.ascii "_ZNSt12_Vector_baseI11MonsterDataSaIS0_EE17_M_create_storageEy\0"
	.byte	0x2
	.long	0x13e5
	.long	0x13f0
	.uleb128 0x2
	.long	0x7951
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x78ad
	.uleb128 0xb
	.secrel32	.LASF37
	.long	0x6ea
	.byte	0
	.uleb128 0x3
	.long	0xabf
	.uleb128 0x17
	.ascii "__type_identity<std::allocator<MonsterData> >\0"
	.byte	0x1
	.byte	0x1
	.byte	0xa7
	.byte	0xc
	.long	0x1458
	.uleb128 0x2c
	.ascii "type\0"
	.byte	0x1
	.byte	0xa8
	.byte	0xd
	.long	0x6ea
	.uleb128 0xa
	.ascii "_Type\0"
	.long	0x6ea
	.byte	0
	.uleb128 0x4a
	.ascii "vector<MonsterData, std::allocator<MonsterData> >\0"
	.byte	0x18
	.byte	0x7
	.word	0x1ca
	.long	0x3184
	.uleb128 0x1c
	.long	0x12df
	.uleb128 0x1c
	.long	0x1336
	.uleb128 0x1c
	.long	0x12d2
	.uleb128 0x1c
	.long	0xf64
	.uleb128 0x1c
	.long	0xf0a
	.uleb128 0x1c
	.long	0xfd1
	.uleb128 0x3b
	.long	0xabf
	.byte	0x2
	.uleb128 0x13
	.secrel32	.LASF38
	.byte	0x7
	.word	0x1f4
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE19_S_nothrow_relocateESt17integral_constantIbLb1EE\0"
	.long	0x679c
	.long	0x1522
	.uleb128 0x1
	.long	0x383
	.byte	0
	.uleb128 0x13
	.secrel32	.LASF38
	.byte	0x7
	.word	0x1fd
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE19_S_nothrow_relocateESt17integral_constantIbLb0EE\0"
	.long	0x679c
	.long	0x158d
	.uleb128 0x1
	.long	0x3a1
	.byte	0
	.uleb128 0x59
	.secrel32	.LASF79
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE15_S_use_relocateEv\0"
	.long	0x679c
	.uleb128 0xf
	.secrel32	.LASF15
	.byte	0x7
	.word	0x1e4
	.byte	0x29
	.long	0xcb8
	.uleb128 0x13
	.secrel32	.LASF39
	.byte	0x7
	.word	0x20a
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE14_S_do_relocateEPS0_S3_S3_RS1_St17integral_constantIbLb1EE\0"
	.long	0x15cc
	.long	0x1661
	.uleb128 0x1
	.long	0x15cc
	.uleb128 0x1
	.long	0x15cc
	.uleb128 0x1
	.long	0x15cc
	.uleb128 0x1
	.long	0x7965
	.uleb128 0x1
	.long	0x383
	.byte	0
	.uleb128 0x14
	.secrel32	.LASF29
	.byte	0x7
	.word	0x1df
	.byte	0x2f
	.long	0xef9
	.uleb128 0x3
	.long	0x1661
	.uleb128 0x13
	.secrel32	.LASF39
	.byte	0x7
	.word	0x211
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE14_S_do_relocateEPS0_S3_S3_RS1_St17integral_constantIbLb0EE\0"
	.long	0x15cc
	.long	0x16fb
	.uleb128 0x1
	.long	0x15cc
	.uleb128 0x1
	.long	0x15cc
	.uleb128 0x1
	.long	0x15cc
	.uleb128 0x1
	.long	0x7965
	.uleb128 0x1
	.long	0x3a1
	.byte	0
	.uleb128 0x13
	.secrel32	.LASF40
	.byte	0x7
	.word	0x216
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE11_S_relocateEPS0_S3_S3_RS1_\0"
	.long	0x15cc
	.long	0x175f
	.uleb128 0x1
	.long	0x15cc
	.uleb128 0x1
	.long	0x15cc
	.uleb128 0x1
	.long	0x15cc
	.uleb128 0x1
	.long	0x7965
	.byte	0
	.uleb128 0x3e
	.secrel32	.LASF41
	.word	0x231
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4Ev\0"
	.long	0x1795
	.long	0x179b
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x34
	.secrel32	.LASF41
	.byte	0x7
	.word	0x23c
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4ERKS1_\0"
	.long	0x17d6
	.long	0x17e1
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x7974
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF16
	.byte	0x7
	.word	0x1ef
	.byte	0x1a
	.long	0x6ea
	.uleb128 0x3
	.long	0x17e1
	.uleb128 0x34
	.secrel32	.LASF41
	.byte	0x7
	.word	0x24a
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4EyRKS1_\0"
	.long	0x182f
	.long	0x183f
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.uleb128 0x1
	.long	0x7974
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF17
	.byte	0x7
	.word	0x1ed
	.byte	0x1a
	.long	0x280
	.uleb128 0x7
	.secrel32	.LASF41
	.byte	0x7
	.word	0x257
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4EyRKS0_RKS1_\0"
	.byte	0x1
	.long	0x188f
	.long	0x18a4
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.uleb128 0x1
	.long	0x7979
	.uleb128 0x1
	.long	0x7974
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF3
	.byte	0x7
	.word	0x1e3
	.byte	0x17
	.long	0x78ad
	.uleb128 0x3
	.long	0x18a4
	.uleb128 0x7
	.secrel32	.LASF41
	.byte	0x7
	.word	0x277
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4ERKS2_\0"
	.byte	0x1
	.long	0x18f3
	.long	0x18fe
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x797e
	.byte	0
	.uleb128 0x3e
	.secrel32	.LASF41
	.word	0x28a
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4EOS2_\0"
	.long	0x1937
	.long	0x1942
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x7983
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF41
	.byte	0x7
	.word	0x28e
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4ERKS2_RKS1_\0"
	.byte	0x1
	.long	0x1984
	.long	0x1994
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x797e
	.uleb128 0x1
	.long	0x7988
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF41
	.word	0x299
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4EOS2_RKS1_St17integral_constantIbLb1EE\0"
	.long	0x19ee
	.long	0x1a03
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x7983
	.uleb128 0x1
	.long	0x7974
	.uleb128 0x1
	.long	0x383
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF41
	.word	0x29e
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4EOS2_RKS1_St17integral_constantIbLb0EE\0"
	.long	0x1a5d
	.long	0x1a72
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x7983
	.uleb128 0x1
	.long	0x7974
	.uleb128 0x1
	.long	0x3a1
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF41
	.byte	0x7
	.word	0x2b1
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4EOS2_RKS1_\0"
	.byte	0x1
	.long	0x1ab3
	.long	0x1ac3
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x7983
	.uleb128 0x1
	.long	0x7988
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF41
	.byte	0x7
	.word	0x2c4
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEC4ESt16initializer_listIS0_ERKS1_\0"
	.byte	0x1
	.long	0x1b19
	.long	0x1b29
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x319a
	.uleb128 0x1
	.long	0x7974
	.byte	0
	.uleb128 0x2e
	.ascii "~vector\0"
	.word	0x320
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EED4Ev\0"
	.long	0x1b63
	.long	0x1b69
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF12
	.byte	0x16
	.byte	0xd2
	.byte	0x5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEaSERKS2_\0"
	.long	0x798d
	.byte	0x1
	.long	0x1ba9
	.long	0x1bb4
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x797e
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF12
	.byte	0x7
	.word	0x341
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEaSEOS2_\0"
	.long	0x798d
	.byte	0x1
	.long	0x1bf4
	.long	0x1bff
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x7983
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF12
	.byte	0x7
	.word	0x357
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEaSESt16initializer_listIS0_E\0"
	.long	0x798d
	.byte	0x1
	.long	0x1c54
	.long	0x1c5f
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x319a
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF42
	.byte	0x7
	.word	0x36b
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE6assignEyRKS0_\0"
	.byte	0x1
	.long	0x1ca2
	.long	0x1cb2
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.uleb128 0x1
	.long	0x7979
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF42
	.byte	0x7
	.word	0x39a
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE6assignESt16initializer_listIS0_E\0"
	.byte	0x1
	.long	0x1d08
	.long	0x1d13
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x319a
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF43
	.byte	0x7
	.word	0x1e8
	.byte	0x3d
	.long	0x6bf8
	.uleb128 0x6
	.secrel32	.LASF44
	.byte	0x7
	.word	0x3e6
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE5beginEv\0"
	.long	0x1d13
	.byte	0x1
	.long	0x1d61
	.long	0x1d67
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF45
	.byte	0x7
	.word	0x1ea
	.byte	0x7
	.long	0x7288
	.uleb128 0x6
	.secrel32	.LASF44
	.byte	0x7
	.word	0x3f0
	.byte	0x7
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE5beginEv\0"
	.long	0x1d67
	.byte	0x1
	.long	0x1db6
	.long	0x1dbc
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x8
	.ascii "end\0"
	.byte	0x7
	.word	0x3fa
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE3endEv\0"
	.long	0x1d13
	.long	0x1df9
	.long	0x1dff
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x8
	.ascii "end\0"
	.byte	0x7
	.word	0x404
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE3endEv\0"
	.long	0x1d67
	.long	0x1e3d
	.long	0x1e43
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF46
	.byte	0x7
	.word	0x1ec
	.byte	0x30
	.long	0x31b9
	.uleb128 0x6
	.secrel32	.LASF47
	.byte	0x7
	.word	0x40e
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE6rbeginEv\0"
	.long	0x1e43
	.byte	0x1
	.long	0x1e92
	.long	0x1e98
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF48
	.byte	0x7
	.word	0x1eb
	.byte	0x35
	.long	0x3231
	.uleb128 0x6
	.secrel32	.LASF47
	.byte	0x7
	.word	0x418
	.byte	0x7
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE6rbeginEv\0"
	.long	0x1e98
	.byte	0x1
	.long	0x1ee8
	.long	0x1eee
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x8
	.ascii "rend\0"
	.byte	0x7
	.word	0x422
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE4rendEv\0"
	.long	0x1e43
	.long	0x1f2d
	.long	0x1f33
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x8
	.ascii "rend\0"
	.byte	0x7
	.word	0x42c
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE4rendEv\0"
	.long	0x1e98
	.long	0x1f73
	.long	0x1f79
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x8
	.ascii "cbegin\0"
	.byte	0x7
	.word	0x437
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE6cbeginEv\0"
	.long	0x1d67
	.long	0x1fbd
	.long	0x1fc3
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x8
	.ascii "cend\0"
	.byte	0x7
	.word	0x441
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE4cendEv\0"
	.long	0x1d67
	.long	0x2003
	.long	0x2009
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x8
	.ascii "crbegin\0"
	.byte	0x7
	.word	0x44b
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE7crbeginEv\0"
	.long	0x1e98
	.long	0x204f
	.long	0x2055
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x8
	.ascii "crend\0"
	.byte	0x7
	.word	0x455
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE5crendEv\0"
	.long	0x1e98
	.long	0x2097
	.long	0x209d
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x8
	.ascii "size\0"
	.byte	0x7
	.word	0x45d
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE4sizeEv\0"
	.long	0x183f
	.long	0x20dd
	.long	0x20e3
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF19
	.byte	0x7
	.word	0x468
	.byte	0x7
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE8max_sizeEv\0"
	.long	0x183f
	.byte	0x1
	.long	0x2128
	.long	0x212e
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF49
	.byte	0x7
	.word	0x477
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE6resizeEy\0"
	.byte	0x1
	.long	0x216c
	.long	0x2177
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF49
	.byte	0x7
	.word	0x48c
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE6resizeEyRKS0_\0"
	.byte	0x1
	.long	0x21ba
	.long	0x21ca
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.uleb128 0x1
	.long	0x7979
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF50
	.byte	0x7
	.word	0x4ae
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE13shrink_to_fitEv\0"
	.byte	0x1
	.long	0x2210
	.long	0x2216
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF51
	.byte	0x7
	.word	0x4b8
	.byte	0x7
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE8capacityEv\0"
	.long	0x183f
	.byte	0x1
	.long	0x225b
	.long	0x2261
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x8
	.ascii "empty\0"
	.byte	0x7
	.word	0x4c7
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE5emptyEv\0"
	.long	0x679c
	.long	0x22a3
	.long	0x22a9
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x5a
	.ascii "reserve\0"
	.byte	0x43
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE7reserveEy\0"
	.long	0x22e8
	.long	0x22f3
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF52
	.byte	0x7
	.word	0x1e6
	.byte	0x32
	.long	0x6ba1
	.uleb128 0x6
	.secrel32	.LASF53
	.byte	0x7
	.word	0x4ed
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EEixEy\0"
	.long	0x22f3
	.byte	0x1
	.long	0x233d
	.long	0x2348
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF54
	.byte	0x7
	.word	0x1e7
	.byte	0x37
	.long	0x6bad
	.uleb128 0x6
	.secrel32	.LASF53
	.byte	0x7
	.word	0x500
	.byte	0x7
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EEixEy\0"
	.long	0x2348
	.byte	0x1
	.long	0x2393
	.long	0x239e
	.uleb128 0x2
	.long	0x7992
	.uleb128 0x1
	.long	0x183f
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF55
	.byte	0x7
	.word	0x50a
	.byte	0x7
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE14_M_range_checkEy\0"
	.byte	0x2
	.long	0x23e6
	.long	0x23f1
	.uleb128 0x2
	.long	0x7992
	.uleb128 0x1
	.long	0x183f
	.byte	0
	.uleb128 0x8
	.ascii "at\0"
	.byte	0x7
	.word	0x521
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE2atEy\0"
	.long	0x22f3
	.long	0x242c
	.long	0x2437
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.byte	0
	.uleb128 0x8
	.ascii "at\0"
	.byte	0x7
	.word	0x534
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE2atEy\0"
	.long	0x2348
	.long	0x2473
	.long	0x247e
	.uleb128 0x2
	.long	0x7992
	.uleb128 0x1
	.long	0x183f
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF56
	.byte	0x7
	.word	0x540
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE5frontEv\0"
	.long	0x22f3
	.byte	0x1
	.long	0x24bf
	.long	0x24c5
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF56
	.byte	0x7
	.word	0x54c
	.byte	0x7
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE5frontEv\0"
	.long	0x2348
	.byte	0x1
	.long	0x2507
	.long	0x250d
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x8
	.ascii "back\0"
	.byte	0x7
	.word	0x558
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE4backEv\0"
	.long	0x22f3
	.long	0x254c
	.long	0x2552
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x8
	.ascii "back\0"
	.byte	0x7
	.word	0x564
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE4backEv\0"
	.long	0x2348
	.long	0x2592
	.long	0x2598
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x8
	.ascii "data\0"
	.byte	0x7
	.word	0x573
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE4dataEv\0"
	.long	0x78ed
	.long	0x25d7
	.long	0x25dd
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x8
	.ascii "data\0"
	.byte	0x7
	.word	0x578
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE4dataEv\0"
	.long	0x7915
	.long	0x261d
	.long	0x2623
	.uleb128 0x2
	.long	0x7992
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF57
	.byte	0x7
	.word	0x588
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE9push_backERKS0_\0"
	.byte	0x1
	.long	0x2668
	.long	0x2673
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x7979
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF57
	.byte	0x7
	.word	0x599
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE9push_backEOS0_\0"
	.byte	0x1
	.long	0x26b7
	.long	0x26c2
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x7997
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF58
	.byte	0x7
	.word	0x5b1
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE8pop_backEv\0"
	.byte	0x1
	.long	0x2702
	.long	0x2708
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF59
	.byte	0x16
	.byte	0x85
	.byte	0x5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EERS5_\0"
	.long	0x1d13
	.byte	0x1
	.long	0x2775
	.long	0x2785
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d67
	.uleb128 0x1
	.long	0x7979
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF59
	.byte	0x7
	.word	0x5f8
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEOS0_\0"
	.long	0x1d13
	.byte	0x1
	.long	0x27f3
	.long	0x2803
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d67
	.uleb128 0x1
	.long	0x7997
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF59
	.byte	0x7
	.word	0x60a
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EESt16initializer_listIS0_E\0"
	.long	0x1d13
	.byte	0x1
	.long	0x2886
	.long	0x2896
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d67
	.uleb128 0x1
	.long	0x319a
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF59
	.byte	0x7
	.word	0x624
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEyRS5_\0"
	.long	0x1d13
	.byte	0x1
	.long	0x2905
	.long	0x291a
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d67
	.uleb128 0x1
	.long	0x183f
	.uleb128 0x1
	.long	0x7979
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF60
	.byte	0x7
	.word	0x700
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE5eraseEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EE\0"
	.long	0x1d13
	.byte	0x1
	.long	0x2983
	.long	0x298e
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d67
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF60
	.byte	0x7
	.word	0x71c
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE5eraseEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EES7_\0"
	.long	0x1d13
	.byte	0x1
	.long	0x29fa
	.long	0x2a0a
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d67
	.uleb128 0x1
	.long	0x1d67
	.byte	0
	.uleb128 0x2e
	.ascii "swap\0"
	.word	0x734
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE4swapERS2_\0"
	.long	0x2a47
	.long	0x2a52
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x798d
	.byte	0
	.uleb128 0x2e
	.ascii "clear\0"
	.word	0x747
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE5clearEv\0"
	.long	0x2a8e
	.long	0x2a94
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF61
	.byte	0x7
	.word	0x7cd
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE18_M_fill_initializeEyRKS0_\0"
	.byte	0x2
	.long	0x2ae4
	.long	0x2af4
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.uleb128 0x1
	.long	0x7979
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF62
	.byte	0x7
	.word	0x7d8
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE21_M_default_initializeEy\0"
	.byte	0x2
	.long	0x2b42
	.long	0x2b4d
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF63
	.byte	0x16
	.word	0x10e
	.byte	0x5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE14_M_fill_assignEyRKS0_\0"
	.byte	0x2
	.long	0x2b99
	.long	0x2ba9
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x280
	.uleb128 0x1
	.long	0x7979
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF64
	.byte	0x16
	.word	0x28c
	.byte	0x5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS0_S2_EEyRKS0_\0"
	.byte	0x2
	.long	0x2c1d
	.long	0x2c32
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d13
	.uleb128 0x1
	.long	0x183f
	.uleb128 0x1
	.long	0x7979
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF65
	.byte	0x16
	.word	0x2f6
	.byte	0x5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE14_M_fill_appendEyRKS0_\0"
	.byte	0x2
	.long	0x2c7e
	.long	0x2c8e
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.uleb128 0x1
	.long	0x7979
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF66
	.byte	0x16
	.word	0x32d
	.byte	0x5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE17_M_default_appendEy\0"
	.byte	0x2
	.long	0x2cd8
	.long	0x2ce3
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x183f
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF67
	.byte	0x16
	.word	0x389
	.byte	0x5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE16_M_shrink_to_fitEv\0"
	.long	0x679c
	.byte	0x2
	.long	0x2d30
	.long	0x2d36
	.uleb128 0x2
	.long	0x796a
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF68
	.byte	0x16
	.word	0x16b
	.byte	0x5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE14_M_insert_rvalEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEOS0_\0"
	.long	0x1d13
	.byte	0x2
	.long	0x2dad
	.long	0x2dbd
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d67
	.uleb128 0x1
	.long	0x7997
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF69
	.byte	0x7
	.word	0x893
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE14_M_emplace_auxEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEOS0_\0"
	.long	0x1d13
	.byte	0x2
	.long	0x2e34
	.long	0x2e44
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d67
	.uleb128 0x1
	.long	0x7997
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF70
	.byte	0x7
	.word	0x89a
	.byte	0x7
	.ascii "_ZNKSt6vectorI11MonsterDataSaIS0_EE12_M_check_lenEyPKc\0"
	.long	0x183f
	.byte	0x2
	.long	0x2e91
	.long	0x2ea1
	.uleb128 0x2
	.long	0x7992
	.uleb128 0x1
	.long	0x183f
	.uleb128 0x1
	.long	0x799c
	.byte	0
	.uleb128 0x3f
	.secrel32	.LASF71
	.word	0x8a5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE17_S_check_init_lenEyRKS1_\0"
	.long	0x183f
	.long	0x2ef8
	.uleb128 0x1
	.long	0x183f
	.uleb128 0x1
	.long	0x7974
	.byte	0
	.uleb128 0x3f
	.secrel32	.LASF72
	.word	0x8ae
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE11_S_max_sizeERKS1_\0"
	.long	0x183f
	.long	0x2f43
	.uleb128 0x1
	.long	0x79a1
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF73
	.byte	0x7
	.word	0x8bf
	.byte	0x7
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE15_M_erase_at_endEPS0_\0"
	.byte	0x2
	.long	0x2f8e
	.long	0x2f99
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x15cc
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF74
	.byte	0x16
	.byte	0xb5
	.byte	0x5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE8_M_eraseEN9__gnu_cxx17__normal_iteratorIPS0_S2_EE\0"
	.long	0x1d13
	.byte	0x2
	.long	0x3003
	.long	0x300e
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d13
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF74
	.byte	0x16
	.byte	0xc3
	.byte	0x5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE8_M_eraseEN9__gnu_cxx17__normal_iteratorIPS0_S2_EES6_\0"
	.long	0x1d13
	.byte	0x2
	.long	0x307b
	.long	0x308b
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x1d13
	.uleb128 0x1
	.long	0x1d13
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF75
	.word	0x8d9
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE14_M_move_assignEOS2_St17integral_constantIbLb1EE\0"
	.long	0x30ee
	.long	0x30fe
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x7983
	.uleb128 0x1
	.long	0x383
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF75
	.word	0x8e5
	.ascii "_ZNSt6vectorI11MonsterDataSaIS0_EE14_M_move_assignEOS2_St17integral_constantIbLb0EE\0"
	.long	0x3161
	.long	0x3171
	.uleb128 0x2
	.long	0x796a
	.uleb128 0x1
	.long	0x7983
	.uleb128 0x1
	.long	0x3a1
	.byte	0
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x78ad
	.uleb128 0x5b
	.secrel32	.LASF37
	.long	0x6ea
	.byte	0
	.uleb128 0x3
	.long	0x1458
	.uleb128 0x11
	.secrel32	.LASF76
	.byte	0x1
	.byte	0xab
	.byte	0xb
	.long	0x143f
	.uleb128 0x3
	.long	0x3189
	.uleb128 0x26
	.ascii "initializer_list<MonsterData>\0"
	.uleb128 0x26
	.ascii "reverse_iterator<__gnu_cxx::__normal_iterator<MonsterData*, std::vector<MonsterData, std::allocator<MonsterData> > > >\0"
	.uleb128 0x26
	.ascii "reverse_iterator<__gnu_cxx::__normal_iterator<const MonsterData*, std::vector<MonsterData, std::allocator<MonsterData> > > >\0"
	.uleb128 0x17
	.ascii "iterator_traits<MonsterData*>\0"
	.byte	0x1
	.byte	0x17
	.byte	0xc8
	.byte	0xc
	.long	0x3304
	.uleb128 0x11
	.secrel32	.LASF77
	.byte	0x17
	.byte	0xcd
	.byte	0xd
	.long	0x371
	.uleb128 0x11
	.secrel32	.LASF15
	.byte	0x17
	.byte	0xce
	.byte	0xd
	.long	0x78ed
	.uleb128 0x11
	.secrel32	.LASF52
	.byte	0x17
	.byte	0xcf
	.byte	0xd
	.long	0x79a6
	.uleb128 0xb
	.secrel32	.LASF78
	.long	0x78ed
	.byte	0
	.uleb128 0x32
	.ascii "__new_allocator<Monster>\0"
	.byte	0x1
	.byte	0x5
	.byte	0x3f
	.long	0x34f7
	.uleb128 0x16
	.secrel32	.LASF8
	.byte	0x5
	.byte	0x58
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI7MonsterEC4Ev\0"
	.byte	0x1
	.long	0x335b
	.long	0x3361
	.uleb128 0x2
	.long	0x79c9
	.byte	0
	.uleb128 0x16
	.secrel32	.LASF8
	.byte	0x5
	.byte	0x5c
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI7MonsterEC4ERKS1_\0"
	.byte	0x1
	.long	0x339b
	.long	0x33a6
	.uleb128 0x2
	.long	0x79c9
	.uleb128 0x1
	.long	0x79d3
	.byte	0
	.uleb128 0x3a
	.secrel32	.LASF12
	.byte	0x5
	.byte	0x64
	.byte	0x18
	.ascii "_ZNSt15__new_allocatorI7MonsterEaSERKS1_\0"
	.long	0x79d8
	.long	0x33e3
	.long	0x33ee
	.uleb128 0x2
	.long	0x79c9
	.uleb128 0x1
	.long	0x79d3
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF14
	.byte	0x5
	.byte	0x7e
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI7MonsterE8allocateEyPKv\0"
	.long	0x7b28
	.byte	0x1
	.long	0x3432
	.long	0x3442
	.uleb128 0x2
	.long	0x79c9
	.uleb128 0x1
	.long	0x3442
	.uleb128 0x1
	.long	0x782e
	.byte	0
	.uleb128 0x33
	.secrel32	.LASF17
	.byte	0x5
	.byte	0x43
	.byte	0x1f
	.long	0x280
	.uleb128 0x16
	.secrel32	.LASF9
	.byte	0x5
	.byte	0x9c
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI7MonsterE10deallocateEPS0_y\0"
	.byte	0x1
	.long	0x3492
	.long	0x34a2
	.uleb128 0x2
	.long	0x79c9
	.uleb128 0x1
	.long	0x7b28
	.uleb128 0x1
	.long	0x3442
	.byte	0
	.uleb128 0x39
	.secrel32	.LASF10
	.byte	0x5
	.byte	0xe6
	.byte	0x7
	.ascii "_ZNKSt15__new_allocatorI7MonsterE11_M_max_sizeEv\0"
	.long	0x3442
	.long	0x34e7
	.long	0x34ed
	.uleb128 0x2
	.long	0x7b32
	.byte	0
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.byte	0
	.uleb128 0x3
	.long	0x3304
	.uleb128 0x32
	.ascii "allocator<Monster>\0"
	.byte	0x1
	.byte	0x6
	.byte	0x85
	.long	0x3655
	.uleb128 0x3b
	.long	0x3304
	.byte	0x1
	.uleb128 0x16
	.secrel32	.LASF11
	.byte	0x6
	.byte	0xa8
	.byte	0x7
	.ascii "_ZNSaI7MonsterEC4Ev\0"
	.byte	0x1
	.long	0x3542
	.long	0x3548
	.uleb128 0x2
	.long	0x7b3c
	.byte	0
	.uleb128 0x16
	.secrel32	.LASF11
	.byte	0x6
	.byte	0xac
	.byte	0x7
	.ascii "_ZNSaI7MonsterEC4ERKS0_\0"
	.byte	0x1
	.long	0x3571
	.long	0x357c
	.uleb128 0x2
	.long	0x7b3c
	.uleb128 0x1
	.long	0x7b46
	.byte	0
	.uleb128 0x3a
	.secrel32	.LASF12
	.byte	0x6
	.byte	0xb1
	.byte	0x12
	.ascii "_ZNSaI7MonsterEaSERKS0_\0"
	.long	0x7b4b
	.long	0x35a8
	.long	0x35b3
	.uleb128 0x2
	.long	0x7b3c
	.uleb128 0x1
	.long	0x7b46
	.byte	0
	.uleb128 0x16
	.secrel32	.LASF13
	.byte	0x6
	.byte	0xbd
	.byte	0x7
	.ascii "_ZNSaI7MonsterED4Ev\0"
	.byte	0x1
	.long	0x35d8
	.long	0x35de
	.uleb128 0x2
	.long	0x7b3c
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF14
	.byte	0x6
	.byte	0xc2
	.byte	0x7
	.ascii "_ZNSaI7MonsterE8allocateEy\0"
	.long	0x7b28
	.byte	0x1
	.long	0x360e
	.long	0x3619
	.uleb128 0x2
	.long	0x7b3c
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x56
	.secrel32	.LASF9
	.byte	0xd0
	.ascii "_ZNSaI7MonsterE10deallocateEPS_y\0"
	.long	0x3644
	.uleb128 0x2
	.long	0x7b3c
	.uleb128 0x1
	.long	0x7b28
	.uleb128 0x1
	.long	0x280
	.byte	0
	.byte	0
	.uleb128 0x3
	.long	0x34fc
	.uleb128 0x47
	.ascii "allocator_traits<std::allocator<Monster> >\0"
	.byte	0x8
	.word	0x230
	.long	0x3892
	.uleb128 0x14
	.secrel32	.LASF15
	.byte	0x8
	.word	0x239
	.byte	0xd
	.long	0x7b28
	.uleb128 0x13
	.secrel32	.LASF14
	.byte	0x8
	.word	0x265
	.ascii "_ZNSt16allocator_traitsISaI7MonsterEE8allocateERS1_y\0"
	.long	0x368d
	.long	0x36ea
	.uleb128 0x1
	.long	0x7b50
	.uleb128 0x1
	.long	0x36fc
	.byte	0
	.uleb128 0x14
	.secrel32	.LASF16
	.byte	0x8
	.word	0x233
	.byte	0xd
	.long	0x34fc
	.uleb128 0x3
	.long	0x36ea
	.uleb128 0x14
	.secrel32	.LASF17
	.byte	0x8
	.word	0x248
	.byte	0xd
	.long	0x280
	.uleb128 0x13
	.secrel32	.LASF14
	.byte	0x8
	.word	0x274
	.ascii "_ZNSt16allocator_traitsISaI7MonsterEE8allocateERS1_yPKv\0"
	.long	0x368d
	.long	0x3761
	.uleb128 0x1
	.long	0x7b50
	.uleb128 0x1
	.long	0x36fc
	.uleb128 0x1
	.long	0x3761
	.byte	0
	.uleb128 0x14
	.secrel32	.LASF18
	.byte	0x8
	.word	0x242
	.byte	0xd
	.long	0x782e
	.uleb128 0x57
	.secrel32	.LASF9
	.ascii "_ZNSt16allocator_traitsISaI7MonsterEE10deallocateERS1_PS0_y\0"
	.long	0x37c3
	.uleb128 0x1
	.long	0x7b50
	.uleb128 0x1
	.long	0x368d
	.uleb128 0x1
	.long	0x36fc
	.byte	0
	.uleb128 0x13
	.secrel32	.LASF19
	.byte	0x8
	.word	0x2c5
	.ascii "_ZNSt16allocator_traitsISaI7MonsterEE8max_sizeERKS1_\0"
	.long	0x36fc
	.long	0x380e
	.uleb128 0x1
	.long	0x7b55
	.byte	0
	.uleb128 0x13
	.secrel32	.LASF20
	.byte	0x8
	.word	0x2d5
	.ascii "_ZNSt16allocator_traitsISaI7MonsterEE37select_on_container_copy_constructionERKS1_\0"
	.long	0x36ea
	.long	0x3877
	.uleb128 0x1
	.long	0x7b55
	.byte	0
	.uleb128 0x14
	.secrel32	.LASF3
	.byte	0x8
	.word	0x236
	.byte	0xd
	.long	0x79dd
	.uleb128 0x14
	.secrel32	.LASF21
	.byte	0x8
	.word	0x257
	.byte	0x8
	.long	0x34fc
	.byte	0
	.uleb128 0x17
	.ascii "_Vector_base<Monster, std::allocator<Monster> >\0"
	.byte	0x18
	.byte	0x7
	.byte	0x5b
	.byte	0xc
	.long	0x41ac
	.uleb128 0x3c
	.secrel32	.LASF22
	.byte	0x62
	.long	0x3a6a
	.uleb128 0x2d
	.secrel32	.LASF23
	.byte	0x64
	.long	0x3a6f
	.byte	0
	.uleb128 0x2d
	.secrel32	.LASF24
	.byte	0x65
	.long	0x3a6f
	.byte	0x8
	.uleb128 0x2d
	.secrel32	.LASF25
	.byte	0x66
	.long	0x3a6f
	.byte	0x10
	.uleb128 0x15
	.secrel32	.LASF22
	.byte	0x7
	.byte	0x69
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_dataC4Ev\0"
	.long	0x3942
	.long	0x3948
	.uleb128 0x2
	.long	0x7b69
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF22
	.byte	0x7
	.byte	0x6f
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_dataC4EOS3_\0"
	.long	0x3997
	.long	0x39a2
	.uleb128 0x2
	.long	0x7b69
	.uleb128 0x1
	.long	0x7b73
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF26
	.byte	0x7
	.byte	0x77
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_data12_M_copy_dataERKS3_\0"
	.long	0x39fe
	.long	0x3a09
	.uleb128 0x2
	.long	0x7b69
	.uleb128 0x1
	.long	0x7b78
	.byte	0
	.uleb128 0x49
	.secrel32	.LASF27
	.byte	0x80
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_data12_M_swap_dataERS3_\0"
	.long	0x3a5e
	.uleb128 0x2
	.long	0x7b69
	.uleb128 0x1
	.long	0x7b7d
	.byte	0
	.byte	0
	.uleb128 0x3
	.long	0x38cb
	.uleb128 0x11
	.secrel32	.LASF15
	.byte	0x7
	.byte	0x60
	.byte	0x9
	.long	0x75a9
	.uleb128 0x3c
	.secrel32	.LASF28
	.byte	0x8b
	.long	0x3ced
	.uleb128 0x2a
	.long	0x34fc
	.uleb128 0x2a
	.long	0x38cb
	.uleb128 0x15
	.secrel32	.LASF28
	.byte	0x7
	.byte	0x8f
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC4EvQ26is_default_constructible_vIN9__gnu_cxx14__alloc_traitsIT0_NS6_10value_typeEE6rebindIT_E5otherEE\0"
	.long	0x3b38
	.long	0x3b3e
	.uleb128 0x2
	.long	0x7b82
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF28
	.byte	0x7
	.byte	0x98
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC4ERKS1_\0"
	.long	0x3b89
	.long	0x3b94
	.uleb128 0x2
	.long	0x7b82
	.uleb128 0x1
	.long	0x7b8c
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF28
	.byte	0x7
	.byte	0xa0
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC4EOS3_\0"
	.long	0x3bde
	.long	0x3be9
	.uleb128 0x2
	.long	0x7b82
	.uleb128 0x1
	.long	0x7b91
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF28
	.byte	0x7
	.byte	0xa5
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC4EOS1_\0"
	.long	0x3c33
	.long	0x3c3e
	.uleb128 0x2
	.long	0x7b82
	.uleb128 0x1
	.long	0x7b96
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF28
	.byte	0x7
	.byte	0xaa
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC4EOS1_OS3_\0"
	.long	0x3c8c
	.long	0x3c9c
	.uleb128 0x2
	.long	0x7b82
	.uleb128 0x1
	.long	0x7b96
	.uleb128 0x1
	.long	0x7b91
	.byte	0
	.uleb128 0x6b
	.ascii "~_Vector_impl\0"
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implD4Ev\0"
	.long	0x3ce6
	.uleb128 0x2
	.long	0x7b82
	.byte	0
	.byte	0
	.uleb128 0x11
	.secrel32	.LASF29
	.byte	0x7
	.byte	0x5e
	.byte	0x15
	.long	0x75e6
	.uleb128 0x3
	.long	0x3ced
	.uleb128 0x25
	.secrel32	.LASF30
	.word	0x133
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE19_M_get_Tp_allocatorEv\0"
	.long	0x7b9b
	.long	0x3d4d
	.long	0x3d53
	.uleb128 0x2
	.long	0x7ba0
	.byte	0
	.uleb128 0x25
	.secrel32	.LASF30
	.word	0x138
	.ascii "_ZNKSt12_Vector_baseI7MonsterSaIS0_EE19_M_get_Tp_allocatorEv\0"
	.long	0x7b8c
	.long	0x3da3
	.long	0x3da9
	.uleb128 0x2
	.long	0x7baa
	.byte	0
	.uleb128 0x14
	.secrel32	.LASF16
	.byte	0x7
	.word	0x12f
	.byte	0x16
	.long	0x34fc
	.uleb128 0x3
	.long	0x3da9
	.uleb128 0x25
	.secrel32	.LASF31
	.word	0x13d
	.ascii "_ZNKSt12_Vector_baseI7MonsterSaIS0_EE13get_allocatorEv\0"
	.long	0x3da9
	.long	0x3e05
	.long	0x3e0b
	.uleb128 0x2
	.long	0x7baa
	.byte	0
	.uleb128 0x3d
	.secrel32	.LASF32
	.word	0x141
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EEC4Ev\0"
	.long	0x3e43
	.long	0x3e49
	.uleb128 0x2
	.long	0x7ba0
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x147
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EEC4ERKS1_\0"
	.long	0x3e85
	.long	0x3e90
	.uleb128 0x2
	.long	0x7ba0
	.uleb128 0x1
	.long	0x7baf
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x14d
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EEC4Ey\0"
	.long	0x3ec8
	.long	0x3ed3
	.uleb128 0x2
	.long	0x7ba0
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x153
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EEC4EyRKS1_\0"
	.long	0x3f10
	.long	0x3f20
	.uleb128 0x2
	.long	0x7ba0
	.uleb128 0x1
	.long	0x280
	.uleb128 0x1
	.long	0x7baf
	.byte	0
	.uleb128 0x3d
	.secrel32	.LASF32
	.word	0x158
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EEC4EOS2_\0"
	.long	0x3f5b
	.long	0x3f66
	.uleb128 0x2
	.long	0x7ba0
	.uleb128 0x1
	.long	0x7bb4
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x15d
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EEC4EOS1_\0"
	.long	0x3fa1
	.long	0x3fac
	.uleb128 0x2
	.long	0x7ba0
	.uleb128 0x1
	.long	0x7b96
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x161
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EEC4EOS2_RKS1_\0"
	.long	0x3fec
	.long	0x3ffc
	.uleb128 0x2
	.long	0x7ba0
	.uleb128 0x1
	.long	0x7bb4
	.uleb128 0x1
	.long	0x7baf
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF32
	.word	0x16f
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EEC4ERKS1_OS2_\0"
	.long	0x403c
	.long	0x404c
	.uleb128 0x2
	.long	0x7ba0
	.uleb128 0x1
	.long	0x7baf
	.uleb128 0x1
	.long	0x7bb4
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF33
	.word	0x175
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EED4Ev\0"
	.long	0x4084
	.long	0x408a
	.uleb128 0x2
	.long	0x7ba0
	.byte	0
	.uleb128 0x58
	.ascii "_M_impl\0"
	.long	0x3a7b
	.uleb128 0x25
	.secrel32	.LASF34
	.word	0x180
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE11_M_allocateEy\0"
	.long	0x3a6f
	.long	0x40de
	.long	0x40e9
	.uleb128 0x2
	.long	0x7ba0
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF35
	.word	0x188
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE13_M_deallocateEPS0_y\0"
	.long	0x4132
	.long	0x4142
	.uleb128 0x2
	.long	0x7ba0
	.uleb128 0x1
	.long	0x3a6f
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF36
	.byte	0x7
	.word	0x193
	.byte	0x7
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_M_create_storageEy\0"
	.byte	0x2
	.long	0x418e
	.long	0x4199
	.uleb128 0x2
	.long	0x7ba0
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0xb
	.secrel32	.LASF37
	.long	0x34fc
	.byte	0
	.uleb128 0x3
	.long	0x3892
	.uleb128 0x17
	.ascii "__type_identity<std::allocator<Monster> >\0"
	.byte	0x1
	.byte	0x1
	.byte	0xa7
	.byte	0xc
	.long	0x41fd
	.uleb128 0x2c
	.ascii "type\0"
	.byte	0x1
	.byte	0xa8
	.byte	0xd
	.long	0x34fc
	.uleb128 0xa
	.ascii "_Type\0"
	.long	0x34fc
	.byte	0
	.uleb128 0x4a
	.ascii "vector<Monster, std::allocator<Monster> >\0"
	.byte	0x18
	.byte	0x7
	.word	0x1ca
	.long	0x5d87
	.uleb128 0x1c
	.long	0x4097
	.uleb128 0x1c
	.long	0x40e9
	.uleb128 0x1c
	.long	0x408a
	.uleb128 0x1c
	.long	0x3d53
	.uleb128 0x1c
	.long	0x3cfe
	.uleb128 0x1c
	.long	0x3dbb
	.uleb128 0x3b
	.long	0x3892
	.byte	0x2
	.uleb128 0x13
	.secrel32	.LASF38
	.byte	0x7
	.word	0x1f4
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE19_S_nothrow_relocateESt17integral_constantIbLb1EE\0"
	.long	0x679c
	.long	0x42ba
	.uleb128 0x1
	.long	0x383
	.byte	0
	.uleb128 0x13
	.secrel32	.LASF38
	.byte	0x7
	.word	0x1fd
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE19_S_nothrow_relocateESt17integral_constantIbLb0EE\0"
	.long	0x679c
	.long	0x4320
	.uleb128 0x1
	.long	0x3a1
	.byte	0
	.uleb128 0x59
	.secrel32	.LASF79
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE15_S_use_relocateEv\0"
	.long	0x679c
	.uleb128 0xf
	.secrel32	.LASF15
	.byte	0x7
	.word	0x1e4
	.byte	0x29
	.long	0x3a6f
	.uleb128 0x13
	.secrel32	.LASF39
	.byte	0x7
	.word	0x20a
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE14_S_do_relocateEPS0_S3_S3_RS1_St17integral_constantIbLb1EE\0"
	.long	0x435a
	.long	0x43ea
	.uleb128 0x1
	.long	0x435a
	.uleb128 0x1
	.long	0x435a
	.uleb128 0x1
	.long	0x435a
	.uleb128 0x1
	.long	0x7bb9
	.uleb128 0x1
	.long	0x383
	.byte	0
	.uleb128 0x14
	.secrel32	.LASF29
	.byte	0x7
	.word	0x1df
	.byte	0x2f
	.long	0x3ced
	.uleb128 0x3
	.long	0x43ea
	.uleb128 0x13
	.secrel32	.LASF39
	.byte	0x7
	.word	0x211
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE14_S_do_relocateEPS0_S3_S3_RS1_St17integral_constantIbLb0EE\0"
	.long	0x435a
	.long	0x447f
	.uleb128 0x1
	.long	0x435a
	.uleb128 0x1
	.long	0x435a
	.uleb128 0x1
	.long	0x435a
	.uleb128 0x1
	.long	0x7bb9
	.uleb128 0x1
	.long	0x3a1
	.byte	0
	.uleb128 0x13
	.secrel32	.LASF40
	.byte	0x7
	.word	0x216
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE11_S_relocateEPS0_S3_S3_RS1_\0"
	.long	0x435a
	.long	0x44de
	.uleb128 0x1
	.long	0x435a
	.uleb128 0x1
	.long	0x435a
	.uleb128 0x1
	.long	0x435a
	.uleb128 0x1
	.long	0x7bb9
	.byte	0
	.uleb128 0x3e
	.secrel32	.LASF41
	.word	0x231
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4Ev\0"
	.long	0x450f
	.long	0x4515
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x34
	.secrel32	.LASF41
	.byte	0x7
	.word	0x23c
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4ERKS1_\0"
	.long	0x454b
	.long	0x4556
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bc8
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF16
	.byte	0x7
	.word	0x1ef
	.byte	0x1a
	.long	0x34fc
	.uleb128 0x3
	.long	0x4556
	.uleb128 0x34
	.secrel32	.LASF41
	.byte	0x7
	.word	0x24a
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4EyRKS1_\0"
	.long	0x459f
	.long	0x45af
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.uleb128 0x1
	.long	0x7bc8
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF17
	.byte	0x7
	.word	0x1ed
	.byte	0x1a
	.long	0x280
	.uleb128 0x7
	.secrel32	.LASF41
	.byte	0x7
	.word	0x257
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4EyRKS0_RKS1_\0"
	.byte	0x1
	.long	0x45fa
	.long	0x460f
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.uleb128 0x1
	.long	0x7bcd
	.uleb128 0x1
	.long	0x7bc8
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF3
	.byte	0x7
	.word	0x1e3
	.byte	0x17
	.long	0x79dd
	.uleb128 0x3
	.long	0x460f
	.uleb128 0x7
	.secrel32	.LASF41
	.byte	0x7
	.word	0x277
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4ERKS2_\0"
	.byte	0x1
	.long	0x4659
	.long	0x4664
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bd2
	.byte	0
	.uleb128 0x3e
	.secrel32	.LASF41
	.word	0x28a
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4EOS2_\0"
	.long	0x4698
	.long	0x46a3
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bd7
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF41
	.byte	0x7
	.word	0x28e
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4ERKS2_RKS1_\0"
	.byte	0x1
	.long	0x46e0
	.long	0x46f0
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bd2
	.uleb128 0x1
	.long	0x7bdc
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF41
	.word	0x299
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4EOS2_RKS1_St17integral_constantIbLb1EE\0"
	.long	0x4745
	.long	0x475a
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bd7
	.uleb128 0x1
	.long	0x7bc8
	.uleb128 0x1
	.long	0x383
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF41
	.word	0x29e
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4EOS2_RKS1_St17integral_constantIbLb0EE\0"
	.long	0x47af
	.long	0x47c4
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bd7
	.uleb128 0x1
	.long	0x7bc8
	.uleb128 0x1
	.long	0x3a1
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF41
	.byte	0x7
	.word	0x2b1
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4EOS2_RKS1_\0"
	.byte	0x1
	.long	0x4800
	.long	0x4810
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bd7
	.uleb128 0x1
	.long	0x7bdc
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF41
	.byte	0x7
	.word	0x2c4
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC4ESt16initializer_listIS0_ERKS1_\0"
	.byte	0x1
	.long	0x4861
	.long	0x4871
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x5d9d
	.uleb128 0x1
	.long	0x7bc8
	.byte	0
	.uleb128 0x2e
	.ascii "~vector\0"
	.word	0x320
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EED4Ev\0"
	.long	0x48a6
	.long	0x48ac
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF12
	.byte	0x16
	.byte	0xd2
	.byte	0x5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEaSERKS2_\0"
	.long	0x7be1
	.byte	0x1
	.long	0x48e7
	.long	0x48f2
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bd2
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF12
	.byte	0x7
	.word	0x341
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEaSEOS2_\0"
	.long	0x7be1
	.byte	0x1
	.long	0x492d
	.long	0x4938
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bd7
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF12
	.byte	0x7
	.word	0x357
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEaSESt16initializer_listIS0_E\0"
	.long	0x7be1
	.byte	0x1
	.long	0x4988
	.long	0x4993
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x5d9d
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF42
	.byte	0x7
	.word	0x36b
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE6assignEyRKS0_\0"
	.byte	0x1
	.long	0x49d1
	.long	0x49e1
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.uleb128 0x1
	.long	0x7bcd
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF42
	.byte	0x7
	.word	0x39a
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE6assignESt16initializer_listIS0_E\0"
	.byte	0x1
	.long	0x4a32
	.long	0x4a3d
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x5d9d
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF43
	.byte	0x7
	.word	0x1e8
	.byte	0x3d
	.long	0x7608
	.uleb128 0x6
	.secrel32	.LASF44
	.byte	0x7
	.word	0x3e6
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE5beginEv\0"
	.long	0x4a3d
	.byte	0x1
	.long	0x4a86
	.long	0x4a8c
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF45
	.byte	0x7
	.word	0x1ea
	.byte	0x7
	.long	0x7656
	.uleb128 0x6
	.secrel32	.LASF44
	.byte	0x7
	.word	0x3f0
	.byte	0x7
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE5beginEv\0"
	.long	0x4a8c
	.byte	0x1
	.long	0x4ad6
	.long	0x4adc
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x8
	.ascii "end\0"
	.byte	0x7
	.word	0x3fa
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE3endEv\0"
	.long	0x4a3d
	.long	0x4b14
	.long	0x4b1a
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x8
	.ascii "end\0"
	.byte	0x7
	.word	0x404
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE3endEv\0"
	.long	0x4a8c
	.long	0x4b53
	.long	0x4b59
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF46
	.byte	0x7
	.word	0x1ec
	.byte	0x30
	.long	0x5f65
	.uleb128 0x6
	.secrel32	.LASF47
	.byte	0x7
	.word	0x40e
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE6rbeginEv\0"
	.long	0x4b59
	.byte	0x1
	.long	0x4ba3
	.long	0x4ba9
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF48
	.byte	0x7
	.word	0x1eb
	.byte	0x35
	.long	0x5fd1
	.uleb128 0x6
	.secrel32	.LASF47
	.byte	0x7
	.word	0x418
	.byte	0x7
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE6rbeginEv\0"
	.long	0x4ba9
	.byte	0x1
	.long	0x4bf4
	.long	0x4bfa
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x8
	.ascii "rend\0"
	.byte	0x7
	.word	0x422
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE4rendEv\0"
	.long	0x4b59
	.long	0x4c34
	.long	0x4c3a
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x8
	.ascii "rend\0"
	.byte	0x7
	.word	0x42c
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE4rendEv\0"
	.long	0x4ba9
	.long	0x4c75
	.long	0x4c7b
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x8
	.ascii "cbegin\0"
	.byte	0x7
	.word	0x437
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE6cbeginEv\0"
	.long	0x4a8c
	.long	0x4cba
	.long	0x4cc0
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x8
	.ascii "cend\0"
	.byte	0x7
	.word	0x441
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE4cendEv\0"
	.long	0x4a8c
	.long	0x4cfb
	.long	0x4d01
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x8
	.ascii "crbegin\0"
	.byte	0x7
	.word	0x44b
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE7crbeginEv\0"
	.long	0x4ba9
	.long	0x4d42
	.long	0x4d48
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x8
	.ascii "crend\0"
	.byte	0x7
	.word	0x455
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE5crendEv\0"
	.long	0x4ba9
	.long	0x4d85
	.long	0x4d8b
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x8
	.ascii "size\0"
	.byte	0x7
	.word	0x45d
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE4sizeEv\0"
	.long	0x45af
	.long	0x4dc6
	.long	0x4dcc
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF19
	.byte	0x7
	.word	0x468
	.byte	0x7
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE8max_sizeEv\0"
	.long	0x45af
	.byte	0x1
	.long	0x4e0c
	.long	0x4e12
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF49
	.byte	0x7
	.word	0x477
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE6resizeEy\0"
	.byte	0x1
	.long	0x4e4b
	.long	0x4e56
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF49
	.byte	0x7
	.word	0x48c
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE6resizeEyRKS0_\0"
	.byte	0x1
	.long	0x4e94
	.long	0x4ea4
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.uleb128 0x1
	.long	0x7bcd
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF50
	.byte	0x7
	.word	0x4ae
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE13shrink_to_fitEv\0"
	.byte	0x1
	.long	0x4ee5
	.long	0x4eeb
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF51
	.byte	0x7
	.word	0x4b8
	.byte	0x7
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE8capacityEv\0"
	.long	0x45af
	.byte	0x1
	.long	0x4f2b
	.long	0x4f31
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x8
	.ascii "empty\0"
	.byte	0x7
	.word	0x4c7
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE5emptyEv\0"
	.long	0x679c
	.long	0x4f6e
	.long	0x4f74
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x5a
	.ascii "reserve\0"
	.byte	0x43
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE7reserveEy\0"
	.long	0x4fae
	.long	0x4fb9
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF52
	.byte	0x7
	.word	0x1e6
	.byte	0x32
	.long	0x75b5
	.uleb128 0x6
	.secrel32	.LASF53
	.byte	0x7
	.word	0x4ed
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEixEy\0"
	.long	0x4fb9
	.byte	0x1
	.long	0x4ffe
	.long	0x5009
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF54
	.byte	0x7
	.word	0x1e7
	.byte	0x37
	.long	0x75c1
	.uleb128 0x6
	.secrel32	.LASF53
	.byte	0x7
	.word	0x500
	.byte	0x7
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EEixEy\0"
	.long	0x5009
	.byte	0x1
	.long	0x504f
	.long	0x505a
	.uleb128 0x2
	.long	0x7be6
	.uleb128 0x1
	.long	0x45af
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF55
	.byte	0x7
	.word	0x50a
	.byte	0x7
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE14_M_range_checkEy\0"
	.byte	0x2
	.long	0x509d
	.long	0x50a8
	.uleb128 0x2
	.long	0x7be6
	.uleb128 0x1
	.long	0x45af
	.byte	0
	.uleb128 0x8
	.ascii "at\0"
	.byte	0x7
	.word	0x521
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE2atEy\0"
	.long	0x4fb9
	.long	0x50de
	.long	0x50e9
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.byte	0
	.uleb128 0x8
	.ascii "at\0"
	.byte	0x7
	.word	0x534
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE2atEy\0"
	.long	0x5009
	.long	0x5120
	.long	0x512b
	.uleb128 0x2
	.long	0x7be6
	.uleb128 0x1
	.long	0x45af
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF56
	.byte	0x7
	.word	0x540
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE5frontEv\0"
	.long	0x4fb9
	.byte	0x1
	.long	0x5167
	.long	0x516d
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF56
	.byte	0x7
	.word	0x54c
	.byte	0x7
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE5frontEv\0"
	.long	0x5009
	.byte	0x1
	.long	0x51aa
	.long	0x51b0
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x8
	.ascii "back\0"
	.byte	0x7
	.word	0x558
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE4backEv\0"
	.long	0x4fb9
	.long	0x51ea
	.long	0x51f0
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x8
	.ascii "back\0"
	.byte	0x7
	.word	0x564
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE4backEv\0"
	.long	0x5009
	.long	0x522b
	.long	0x5231
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x8
	.ascii "data\0"
	.byte	0x7
	.word	0x573
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE4dataEv\0"
	.long	0x7b28
	.long	0x526b
	.long	0x5271
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x8
	.ascii "data\0"
	.byte	0x7
	.word	0x578
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE4dataEv\0"
	.long	0x7b5a
	.long	0x52ac
	.long	0x52b2
	.uleb128 0x2
	.long	0x7be6
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF57
	.byte	0x7
	.word	0x588
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE9push_backERKS0_\0"
	.byte	0x1
	.long	0x52f2
	.long	0x52fd
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bcd
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF57
	.byte	0x7
	.word	0x599
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE9push_backEOS0_\0"
	.byte	0x1
	.long	0x533c
	.long	0x5347
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bf0
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF58
	.byte	0x7
	.word	0x5b1
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE8pop_backEv\0"
	.byte	0x1
	.long	0x5382
	.long	0x5388
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF59
	.byte	0x16
	.byte	0x85
	.byte	0x5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EERS5_\0"
	.long	0x4a3d
	.byte	0x1
	.long	0x53f0
	.long	0x5400
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a8c
	.uleb128 0x1
	.long	0x7bcd
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF59
	.byte	0x7
	.word	0x5f8
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEOS0_\0"
	.long	0x4a3d
	.byte	0x1
	.long	0x5469
	.long	0x5479
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a8c
	.uleb128 0x1
	.long	0x7bf0
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF59
	.byte	0x7
	.word	0x60a
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EESt16initializer_listIS0_E\0"
	.long	0x4a3d
	.byte	0x1
	.long	0x54f7
	.long	0x5507
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a8c
	.uleb128 0x1
	.long	0x5d9d
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF59
	.byte	0x7
	.word	0x624
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEyRS5_\0"
	.long	0x4a3d
	.byte	0x1
	.long	0x5571
	.long	0x5586
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a8c
	.uleb128 0x1
	.long	0x45af
	.uleb128 0x1
	.long	0x7bcd
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF60
	.byte	0x7
	.word	0x700
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE5eraseEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EE\0"
	.long	0x4a3d
	.byte	0x1
	.long	0x55ea
	.long	0x55f5
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a8c
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF60
	.byte	0x7
	.word	0x71c
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE5eraseEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EES7_\0"
	.long	0x4a3d
	.byte	0x1
	.long	0x565c
	.long	0x566c
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a8c
	.uleb128 0x1
	.long	0x4a8c
	.byte	0
	.uleb128 0x2e
	.ascii "swap\0"
	.word	0x734
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE4swapERS2_\0"
	.long	0x56a4
	.long	0x56af
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7be1
	.byte	0
	.uleb128 0x2e
	.ascii "clear\0"
	.word	0x747
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE5clearEv\0"
	.long	0x56e6
	.long	0x56ec
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF61
	.byte	0x7
	.word	0x7cd
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE18_M_fill_initializeEyRKS0_\0"
	.byte	0x2
	.long	0x5737
	.long	0x5747
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.uleb128 0x1
	.long	0x7bcd
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF62
	.byte	0x7
	.word	0x7d8
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE21_M_default_initializeEy\0"
	.byte	0x2
	.long	0x5790
	.long	0x579b
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF63
	.byte	0x16
	.word	0x10e
	.byte	0x5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE14_M_fill_assignEyRKS0_\0"
	.byte	0x2
	.long	0x57e2
	.long	0x57f2
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x280
	.uleb128 0x1
	.long	0x7bcd
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF64
	.byte	0x16
	.word	0x28c
	.byte	0x5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS0_S2_EEyRKS0_\0"
	.byte	0x2
	.long	0x5861
	.long	0x5876
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a3d
	.uleb128 0x1
	.long	0x45af
	.uleb128 0x1
	.long	0x7bcd
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF65
	.byte	0x16
	.word	0x2f6
	.byte	0x5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE14_M_fill_appendEyRKS0_\0"
	.byte	0x2
	.long	0x58bd
	.long	0x58cd
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.uleb128 0x1
	.long	0x7bcd
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF66
	.byte	0x16
	.word	0x32d
	.byte	0x5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE17_M_default_appendEy\0"
	.byte	0x2
	.long	0x5912
	.long	0x591d
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x45af
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF67
	.byte	0x16
	.word	0x389
	.byte	0x5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE16_M_shrink_to_fitEv\0"
	.long	0x679c
	.byte	0x2
	.long	0x5965
	.long	0x596b
	.uleb128 0x2
	.long	0x7bbe
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF68
	.byte	0x16
	.word	0x16b
	.byte	0x5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE14_M_insert_rvalEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEOS0_\0"
	.long	0x4a3d
	.byte	0x2
	.long	0x59dd
	.long	0x59ed
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a8c
	.uleb128 0x1
	.long	0x7bf0
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF69
	.byte	0x7
	.word	0x893
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE14_M_emplace_auxEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEOS0_\0"
	.long	0x4a3d
	.byte	0x2
	.long	0x5a5f
	.long	0x5a6f
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a8c
	.uleb128 0x1
	.long	0x7bf0
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF70
	.byte	0x7
	.word	0x89a
	.byte	0x7
	.ascii "_ZNKSt6vectorI7MonsterSaIS0_EE12_M_check_lenEyPKc\0"
	.long	0x45af
	.byte	0x2
	.long	0x5ab7
	.long	0x5ac7
	.uleb128 0x2
	.long	0x7be6
	.uleb128 0x1
	.long	0x45af
	.uleb128 0x1
	.long	0x799c
	.byte	0
	.uleb128 0x3f
	.secrel32	.LASF71
	.word	0x8a5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE17_S_check_init_lenEyRKS1_\0"
	.long	0x45af
	.long	0x5b19
	.uleb128 0x1
	.long	0x45af
	.uleb128 0x1
	.long	0x7bc8
	.byte	0
	.uleb128 0x3f
	.secrel32	.LASF72
	.word	0x8ae
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE11_S_max_sizeERKS1_\0"
	.long	0x45af
	.long	0x5b5f
	.uleb128 0x1
	.long	0x7bf5
	.byte	0
	.uleb128 0x7
	.secrel32	.LASF73
	.byte	0x7
	.word	0x8bf
	.byte	0x7
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE15_M_erase_at_endEPS0_\0"
	.byte	0x2
	.long	0x5ba5
	.long	0x5bb0
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x435a
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF74
	.byte	0x16
	.byte	0xb5
	.byte	0x5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE8_M_eraseEN9__gnu_cxx17__normal_iteratorIPS0_S2_EE\0"
	.long	0x4a3d
	.byte	0x2
	.long	0x5c15
	.long	0x5c20
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a3d
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF74
	.byte	0x16
	.byte	0xc3
	.byte	0x5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE8_M_eraseEN9__gnu_cxx17__normal_iteratorIPS0_S2_EES6_\0"
	.long	0x4a3d
	.byte	0x2
	.long	0x5c88
	.long	0x5c98
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x4a3d
	.uleb128 0x1
	.long	0x4a3d
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF75
	.word	0x8d9
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE14_M_move_assignEOS2_St17integral_constantIbLb1EE\0"
	.long	0x5cf6
	.long	0x5d06
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bd7
	.uleb128 0x1
	.long	0x383
	.byte	0
	.uleb128 0xe
	.secrel32	.LASF75
	.word	0x8e5
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EE14_M_move_assignEOS2_St17integral_constantIbLb0EE\0"
	.long	0x5d64
	.long	0x5d74
	.uleb128 0x2
	.long	0x7bbe
	.uleb128 0x1
	.long	0x7bd7
	.uleb128 0x1
	.long	0x3a1
	.byte	0
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x5b
	.secrel32	.LASF37
	.long	0x34fc
	.byte	0
	.uleb128 0x3
	.long	0x41fd
	.uleb128 0x11
	.secrel32	.LASF76
	.byte	0x1
	.byte	0xab
	.byte	0xb
	.long	0x41e4
	.uleb128 0x3
	.long	0x5d8c
	.uleb128 0x32
	.ascii "initializer_list<Monster>\0"
	.byte	0x10
	.byte	0x18
	.byte	0x2f
	.long	0x5f60
	.uleb128 0x33
	.secrel32	.LASF43
	.byte	0x18
	.byte	0x36
	.byte	0x1a
	.long	0x7b5a
	.uleb128 0x27
	.ascii "_M_array\0"
	.byte	0x18
	.byte	0x3a
	.byte	0x12
	.long	0x5dbf
	.byte	0
	.uleb128 0x33
	.secrel32	.LASF17
	.byte	0x18
	.byte	0x35
	.byte	0x18
	.long	0x280
	.uleb128 0x27
	.ascii "_M_len\0"
	.byte	0x18
	.byte	0x3b
	.byte	0x13
	.long	0x5ddd
	.byte	0x8
	.uleb128 0x15
	.secrel32	.LASF80
	.byte	0x18
	.byte	0x3e
	.byte	0x11
	.ascii "_ZNSt16initializer_listI7MonsterEC4EPKS0_y\0"
	.long	0x5e34
	.long	0x5e44
	.uleb128 0x2
	.long	0x7bfa
	.uleb128 0x1
	.long	0x5e44
	.uleb128 0x1
	.long	0x5ddd
	.byte	0
	.uleb128 0x33
	.secrel32	.LASF45
	.byte	0x18
	.byte	0x37
	.byte	0x1a
	.long	0x7b5a
	.uleb128 0x16
	.secrel32	.LASF80
	.byte	0x18
	.byte	0x42
	.byte	0x11
	.ascii "_ZNSt16initializer_listI7MonsterEC4Ev\0"
	.byte	0x1
	.long	0x5e87
	.long	0x5e8d
	.uleb128 0x2
	.long	0x7bfa
	.byte	0
	.uleb128 0x5c
	.ascii "size\0"
	.byte	0x47
	.ascii "_ZNKSt16initializer_listI7MonsterE4sizeEv\0"
	.long	0x5ddd
	.long	0x5eca
	.long	0x5ed0
	.uleb128 0x2
	.long	0x7bff
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF44
	.byte	0x18
	.byte	0x4b
	.byte	0x7
	.ascii "_ZNKSt16initializer_listI7MonsterE5beginEv\0"
	.long	0x5e44
	.byte	0x1
	.long	0x5f10
	.long	0x5f16
	.uleb128 0x2
	.long	0x7bff
	.byte	0
	.uleb128 0x5c
	.ascii "end\0"
	.byte	0x4f
	.ascii "_ZNKSt16initializer_listI7MonsterE3endEv\0"
	.long	0x5e44
	.long	0x5f51
	.long	0x5f57
	.uleb128 0x2
	.long	0x7bff
	.byte	0
	.uleb128 0xa
	.ascii "_E\0"
	.long	0x79dd
	.byte	0
	.uleb128 0x3
	.long	0x5d9d
	.uleb128 0x26
	.ascii "reverse_iterator<__gnu_cxx::__normal_iterator<Monster*, std::vector<Monster, std::allocator<Monster> > > >\0"
	.uleb128 0x26
	.ascii "reverse_iterator<__gnu_cxx::__normal_iterator<const Monster*, std::vector<Monster, std::allocator<Monster> > > >\0"
	.uleb128 0x17
	.ascii "_UninitDestroyGuard<Monster*, void>\0"
	.byte	0x10
	.byte	0xa
	.byte	0x6d
	.byte	0xc
	.long	0x61d0
	.uleb128 0x6c
	.secrel32	.LASF81
	.byte	0xa
	.byte	0x71
	.byte	0x7
	.ascii "_ZNSt19_UninitDestroyGuardIP7MonstervEC4ERS1_\0"
	.long	0x60ae
	.long	0x60b9
	.uleb128 0x2
	.long	0x7c0e
	.uleb128 0x1
	.long	0x7c18
	.byte	0
	.uleb128 0x5d
	.ascii "~_UninitDestroyGuard\0"
	.byte	0x76
	.byte	0x7
	.ascii "_ZNSt19_UninitDestroyGuardIP7MonstervED4Ev\0"
	.long	0x6104
	.long	0x610a
	.uleb128 0x2
	.long	0x7c0e
	.byte	0
	.uleb128 0x5d
	.ascii "release\0"
	.byte	0x7d
	.byte	0xc
	.ascii "_ZNSt19_UninitDestroyGuardIP7MonstervE7releaseEv\0"
	.long	0x614e
	.long	0x6154
	.uleb128 0x2
	.long	0x7c0e
	.byte	0
	.uleb128 0x27
	.ascii "_M_first\0"
	.byte	0xa
	.byte	0x7f
	.byte	0x1e
	.long	0x7b2d
	.byte	0
	.uleb128 0x27
	.ascii "_M_cur\0"
	.byte	0xa
	.byte	0x80
	.byte	0x19
	.long	0x7c1d
	.byte	0x8
	.uleb128 0x16
	.secrel32	.LASF81
	.byte	0xa
	.byte	0x83
	.byte	0x7
	.ascii "_ZNSt19_UninitDestroyGuardIP7MonstervEC4ERKS2_\0"
	.byte	0x3
	.long	0x61b6
	.long	0x61c1
	.uleb128 0x2
	.long	0x7c0e
	.uleb128 0x1
	.long	0x7c22
	.byte	0
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0x6d
	.secrel32	.LASF37
	.byte	0
	.uleb128 0x3
	.long	0x6043
	.uleb128 0x6e
	.ascii "__glibcxx_assert_fail\0"
	.byte	0x9
	.word	0x26f
	.byte	0x3
	.ascii "_ZSt21__glibcxx_assert_failPKciS0_S0_\0"
	.long	0x622f
	.uleb128 0x1
	.long	0x799c
	.uleb128 0x1
	.long	0x683a
	.uleb128 0x1
	.long	0x799c
	.uleb128 0x1
	.long	0x799c
	.byte	0
	.uleb128 0x5e
	.ascii "__throw_bad_alloc\0"
	.byte	0x35
	.ascii "_ZSt17__throw_bad_allocv\0"
	.uleb128 0x5e
	.ascii "__throw_bad_array_new_length\0"
	.byte	0x38
	.ascii "_ZSt28__throw_bad_array_new_lengthv\0"
	.uleb128 0x6f
	.ascii "__throw_length_error\0"
	.byte	0x19
	.byte	0x4c
	.byte	0x3
	.ascii "_ZSt20__throw_length_errorPKc\0"
	.long	0x62e0
	.uleb128 0x1
	.long	0x799c
	.byte	0
	.uleb128 0x4b
	.ascii "construct_at<Monster>\0"
	.byte	0xb
	.byte	0x60
	.ascii "_ZSt12construct_atI7MonsterJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_\0"
	.long	0x7b28
	.long	0x6389
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x40
	.secrel32	.LASF82
	.uleb128 0x1
	.long	0x7b28
	.byte	0
	.uleb128 0x41
	.ascii "_Construct<Monster>\0"
	.byte	0x7b
	.ascii "_ZSt10_ConstructI7MonsterJEEvPT_DpOT0_\0"
	.long	0x63de
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x40
	.secrel32	.LASF82
	.uleb128 0x1
	.long	0x7b28
	.byte	0
	.uleb128 0x41
	.ascii "destroy_at<Monster>\0"
	.byte	0x50
	.ascii "_ZSt10destroy_atI7MonsterEvPT_\0"
	.long	0x6426
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x1
	.long	0x7b28
	.byte	0
	.uleb128 0x41
	.ascii "_Destroy<Monster>\0"
	.byte	0xa1
	.ascii "_ZSt8_DestroyI7MonsterEvPT_\0"
	.long	0x6469
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x1
	.long	0x7b28
	.byte	0
	.uleb128 0x4b
	.ascii "__addressof<Monster>\0"
	.byte	0xc
	.byte	0x34
	.ascii "_ZSt11__addressofI7MonsterEPT_RS1_\0"
	.long	0x7b28
	.long	0x64bb
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x1
	.long	0x7c09
	.byte	0
	.uleb128 0x48
	.ascii "__uninitialized_default_n<Monster*, long long unsigned int>\0"
	.word	0x3be
	.byte	0x5
	.ascii "_ZSt25__uninitialized_default_nIP7MonsteryET_S2_T0_\0"
	.long	0x7b28
	.long	0x6554
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0xb
	.secrel32	.LASF7
	.long	0x67b3
	.uleb128 0x1
	.long	0x7b28
	.uleb128 0x1
	.long	0x67b3
	.byte	0
	.uleb128 0x4b
	.ascii "min<long long unsigned int>\0"
	.byte	0xd
	.byte	0xea
	.ascii "_ZSt3minIyERKT_S2_S2_\0"
	.long	0x85bb
	.long	0x65a5
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x67b3
	.uleb128 0x1
	.long	0x85bb
	.uleb128 0x1
	.long	0x85bb
	.byte	0
	.uleb128 0x41
	.ascii "_Destroy<Monster*>\0"
	.byte	0xdb
	.ascii "_ZSt8_DestroyIP7MonsterEvT_S2_\0"
	.long	0x65f1
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0x1
	.long	0x7b28
	.uleb128 0x1
	.long	0x7b28
	.byte	0
	.uleb128 0x48
	.ascii "__uninitialized_default_n_a<Monster*, long long unsigned int, Monster>\0"
	.word	0x403
	.byte	0x5
	.ascii "_ZSt27__uninitialized_default_n_aIP7MonsteryS0_ET_S2_T0_RSaIT1_E\0"
	.long	0x7b28
	.long	0x66b0
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0xb
	.secrel32	.LASF7
	.long	0x67b3
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x1
	.long	0x7b28
	.uleb128 0x1
	.long	0x67b3
	.uleb128 0x1
	.long	0x7b4b
	.byte	0
	.uleb128 0x70
	.ascii "_Destroy<Monster*, Monster>\0"
	.byte	0x8
	.word	0x412
	.byte	0x5
	.ascii "_ZSt8_DestroyIP7MonsterS0_EvT_S2_RSaIT0_E\0"
	.long	0x6721
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x1
	.long	0x7b28
	.uleb128 0x1
	.long	0x7b28
	.uleb128 0x1
	.long	0x7b4b
	.byte	0
	.uleb128 0x5f
	.ascii "is_constant_evaluated\0"
	.byte	0x1
	.word	0xfa7
	.ascii "_ZSt21is_constant_evaluatedv\0"
	.long	0x679c
	.uleb128 0x5f
	.ascii "__is_constant_evaluated\0"
	.byte	0x9
	.word	0x246
	.ascii "_ZSt23__is_constant_evaluatedv\0"
	.long	0x679c
	.byte	0
	.uleb128 0xc
	.byte	0x1
	.byte	0x2
	.ascii "bool\0"
	.uleb128 0x3
	.long	0x679c
	.uleb128 0x9
	.long	0x17c
	.uleb128 0x9
	.long	0x27b
	.uleb128 0xc
	.byte	0x8
	.byte	0x7
	.ascii "long long unsigned int\0"
	.uleb128 0x3
	.long	0x67b3
	.uleb128 0xc
	.byte	0x1
	.byte	0x8
	.ascii "unsigned char\0"
	.uleb128 0xc
	.byte	0x2
	.byte	0x7
	.ascii "short unsigned int\0"
	.uleb128 0xc
	.byte	0x4
	.byte	0x7
	.ascii "unsigned int\0"
	.uleb128 0xc
	.byte	0x4
	.byte	0x7
	.ascii "long unsigned int\0"
	.uleb128 0xc
	.byte	0x1
	.byte	0x6
	.ascii "signed char\0"
	.uleb128 0xc
	.byte	0x2
	.byte	0x5
	.ascii "short int\0"
	.uleb128 0xc
	.byte	0x4
	.byte	0x5
	.ascii "int\0"
	.uleb128 0xc
	.byte	0x4
	.byte	0x5
	.ascii "long int\0"
	.uleb128 0xc
	.byte	0x8
	.byte	0x5
	.ascii "long long int\0"
	.uleb128 0xc
	.byte	0x2
	.byte	0x7
	.ascii "wchar_t\0"
	.uleb128 0xc
	.byte	0x1
	.byte	0x10
	.ascii "char8_t\0"
	.uleb128 0xc
	.byte	0x2
	.byte	0x10
	.ascii "char16_t\0"
	.uleb128 0xc
	.byte	0x4
	.byte	0x10
	.ascii "char32_t\0"
	.uleb128 0x45
	.ascii "__gnu_cxx\0"
	.byte	0x9
	.word	0x175
	.byte	0xb
	.long	0x779b
	.uleb128 0x29
	.ascii "__ops\0"
	.byte	0x1a
	.byte	0x25
	.byte	0xb
	.uleb128 0x17
	.ascii "__alloc_traits<std::allocator<MonsterData>, MonsterData>\0"
	.byte	0x1
	.byte	0x1b
	.byte	0x2f
	.byte	0xa
	.long	0x6bf8
	.uleb128 0x22
	.byte	0x1b
	.byte	0x2f
	.byte	0xa
	.long	0x922
	.uleb128 0x22
	.byte	0x1b
	.byte	0x2f
	.byte	0xa
	.long	0x8ae
	.uleb128 0x22
	.byte	0x1b
	.byte	0x2f
	.byte	0xa
	.long	0x98c
	.uleb128 0x22
	.byte	0x1b
	.byte	0x2f
	.byte	0xa
	.long	0x9e6
	.uleb128 0x2a
	.long	0x86a
	.uleb128 0x4c
	.secrel32	.LASF83
	.byte	0x1b
	.byte	0x63
	.byte	0x1d
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI11MonsterDataES1_E17_S_select_on_copyERKS2_\0"
	.long	0x6ea
	.long	0x6973
	.uleb128 0x1
	.long	0x7901
	.byte	0
	.uleb128 0x42
	.secrel32	.LASF84
	.byte	0x1b
	.byte	0x67
	.byte	0x26
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI11MonsterDataES1_E10_S_on_swapERS2_S4_\0"
	.long	0x69d2
	.uleb128 0x1
	.long	0x7906
	.uleb128 0x1
	.long	0x7906
	.byte	0
	.uleb128 0x1e
	.secrel32	.LASF85
	.byte	0x6b
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI11MonsterDataES1_E27_S_propagate_on_copy_assignEv\0"
	.long	0x679c
	.uleb128 0x1e
	.secrel32	.LASF86
	.byte	0x6f
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI11MonsterDataES1_E27_S_propagate_on_move_assignEv\0"
	.long	0x679c
	.uleb128 0x1e
	.secrel32	.LASF87
	.byte	0x73
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI11MonsterDataES1_E20_S_propagate_on_swapEv\0"
	.long	0x679c
	.uleb128 0x1e
	.secrel32	.LASF88
	.byte	0x77
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI11MonsterDataES1_E15_S_always_equalEv\0"
	.long	0x679c
	.uleb128 0x1e
	.secrel32	.LASF89
	.byte	0x7b
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI11MonsterDataES1_E15_S_nothrow_moveEv\0"
	.long	0x679c
	.uleb128 0x11
	.secrel32	.LASF3
	.byte	0x1b
	.byte	0x37
	.byte	0x35
	.long	0xaa4
	.uleb128 0x3
	.long	0x6b84
	.uleb128 0x11
	.secrel32	.LASF15
	.byte	0x1b
	.byte	0x38
	.byte	0x35
	.long	0x8a1
	.uleb128 0x11
	.secrel32	.LASF52
	.byte	0x1b
	.byte	0x3d
	.byte	0x35
	.long	0x791a
	.uleb128 0x11
	.secrel32	.LASF54
	.byte	0x1b
	.byte	0x3e
	.byte	0x35
	.long	0x791f
	.uleb128 0x17
	.ascii "rebind<MonsterData>\0"
	.byte	0x1
	.byte	0x1b
	.byte	0x7f
	.byte	0xe
	.long	0x6bee
	.uleb128 0x2c
	.ascii "other\0"
	.byte	0x1b
	.byte	0x80
	.byte	0x41
	.long	0xab1
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x78ad
	.byte	0
	.uleb128 0xb
	.secrel32	.LASF37
	.long	0x6ea
	.byte	0
	.uleb128 0x4a
	.ascii "__normal_iterator<MonsterData*, std::vector<MonsterData, std::allocator<MonsterData> > >\0"
	.byte	0x8
	.byte	0x4
	.word	0x402
	.long	0x7283
	.uleb128 0x71
	.ascii "_M_current\0"
	.byte	0x4
	.word	0x405
	.byte	0x11
	.long	0x78ed
	.byte	0
	.byte	0x2
	.uleb128 0x7
	.secrel32	.LASF90
	.byte	0x4
	.word	0x41d
	.byte	0x7
	.ascii "_ZN9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEC4Ev\0"
	.byte	0x1
	.long	0x6ccc
	.long	0x6cd2
	.uleb128 0x2
	.long	0x79ab
	.byte	0
	.uleb128 0x34
	.secrel32	.LASF90
	.byte	0x4
	.word	0x422
	.ascii "_ZN9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEC4ERKS2_\0"
	.long	0x6d30
	.long	0x6d3b
	.uleb128 0x2
	.long	0x79ab
	.uleb128 0x1
	.long	0x79b5
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF52
	.byte	0x4
	.word	0x414
	.byte	0x32
	.long	0x32ee
	.uleb128 0x8
	.ascii "operator*\0"
	.byte	0x4
	.word	0x441
	.ascii "_ZNK9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEdeEv\0"
	.long	0x6d3b
	.long	0x6dad
	.long	0x6db3
	.uleb128 0x2
	.long	0x79ba
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF15
	.byte	0x4
	.word	0x415
	.byte	0x32
	.long	0x32e2
	.uleb128 0x8
	.ascii "operator->\0"
	.byte	0x4
	.word	0x447
	.ascii "_ZNK9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEptEv\0"
	.long	0x6db3
	.long	0x6e26
	.long	0x6e2c
	.uleb128 0x2
	.long	0x79ba
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF91
	.byte	0x4
	.word	0x44d
	.byte	0x7
	.ascii "_ZN9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEppEv\0"
	.long	0x79c4
	.byte	0x1
	.long	0x6e8c
	.long	0x6e92
	.uleb128 0x2
	.long	0x79ab
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF91
	.byte	0x4
	.word	0x456
	.byte	0x7
	.ascii "_ZN9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEppEi\0"
	.long	0x6bf8
	.byte	0x1
	.long	0x6ef2
	.long	0x6efd
	.uleb128 0x2
	.long	0x79ab
	.uleb128 0x1
	.long	0x683a
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF92
	.byte	0x4
	.word	0x45e
	.byte	0x7
	.ascii "_ZN9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEmmEv\0"
	.long	0x79c4
	.byte	0x1
	.long	0x6f5d
	.long	0x6f63
	.uleb128 0x2
	.long	0x79ab
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF92
	.byte	0x4
	.word	0x467
	.byte	0x7
	.ascii "_ZN9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEmmEi\0"
	.long	0x6bf8
	.byte	0x1
	.long	0x6fc3
	.long	0x6fce
	.uleb128 0x2
	.long	0x79ab
	.uleb128 0x1
	.long	0x683a
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF53
	.byte	0x4
	.word	0x46f
	.byte	0x7
	.ascii "_ZNK9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEixEx\0"
	.long	0x6d3b
	.byte	0x1
	.long	0x702f
	.long	0x703a
	.uleb128 0x2
	.long	0x79ba
	.uleb128 0x1
	.long	0x703a
	.byte	0
	.uleb128 0xf
	.secrel32	.LASF77
	.byte	0x4
	.word	0x413
	.byte	0x38
	.long	0x32d6
	.uleb128 0x8
	.ascii "operator+=\0"
	.byte	0x4
	.word	0x475
	.ascii "_ZN9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEpLEx\0"
	.long	0x79c4
	.long	0x70ac
	.long	0x70b7
	.uleb128 0x2
	.long	0x79ab
	.uleb128 0x1
	.long	0x703a
	.byte	0
	.uleb128 0x8
	.ascii "operator+\0"
	.byte	0x4
	.word	0x47b
	.ascii "_ZNK9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEplEx\0"
	.long	0x6bf8
	.long	0x711c
	.long	0x7127
	.uleb128 0x2
	.long	0x79ba
	.uleb128 0x1
	.long	0x703a
	.byte	0
	.uleb128 0x8
	.ascii "operator-=\0"
	.byte	0x4
	.word	0x481
	.ascii "_ZN9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEmIEx\0"
	.long	0x79c4
	.long	0x718c
	.long	0x7197
	.uleb128 0x2
	.long	0x79ab
	.uleb128 0x1
	.long	0x703a
	.byte	0
	.uleb128 0x8
	.ascii "operator-\0"
	.byte	0x4
	.word	0x487
	.ascii "_ZNK9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEmiEx\0"
	.long	0x6bf8
	.long	0x71fc
	.long	0x7207
	.uleb128 0x2
	.long	0x79ba
	.uleb128 0x1
	.long	0x703a
	.byte	0
	.uleb128 0x8
	.ascii "base\0"
	.byte	0x4
	.word	0x48d
	.ascii "_ZNK9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEE4baseEv\0"
	.long	0x79b5
	.long	0x726a
	.long	0x7270
	.uleb128 0x2
	.long	0x79ba
	.byte	0
	.uleb128 0xb
	.secrel32	.LASF78
	.long	0x78ed
	.uleb128 0xb
	.secrel32	.LASF93
	.long	0x1458
	.byte	0
	.uleb128 0x3
	.long	0x6bf8
	.uleb128 0x26
	.ascii "__normal_iterator<const MonsterData*, std::vector<MonsterData, std::allocator<MonsterData> > >\0"
	.uleb128 0x17
	.ascii "__alloc_traits<std::allocator<Monster>, Monster>\0"
	.byte	0x1
	.byte	0x1b
	.byte	0x2f
	.byte	0xa
	.long	0x7608
	.uleb128 0x22
	.byte	0x1b
	.byte	0x2f
	.byte	0xa
	.long	0x3709
	.uleb128 0x22
	.byte	0x1b
	.byte	0x2f
	.byte	0xa
	.long	0x369a
	.uleb128 0x22
	.byte	0x1b
	.byte	0x2f
	.byte	0xa
	.long	0x376e
	.uleb128 0x22
	.byte	0x1b
	.byte	0x2f
	.byte	0xa
	.long	0x37c3
	.uleb128 0x2a
	.long	0x365a
	.uleb128 0x4c
	.secrel32	.LASF83
	.byte	0x1b
	.byte	0x63
	.byte	0x1d
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI7MonsterES1_E17_S_select_on_copyERKS2_\0"
	.long	0x34fc
	.long	0x73a5
	.uleb128 0x1
	.long	0x7b46
	.byte	0
	.uleb128 0x42
	.secrel32	.LASF84
	.byte	0x1b
	.byte	0x67
	.byte	0x26
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI7MonsterES1_E10_S_on_swapERS2_S4_\0"
	.long	0x73ff
	.uleb128 0x1
	.long	0x7b4b
	.uleb128 0x1
	.long	0x7b4b
	.byte	0
	.uleb128 0x1e
	.secrel32	.LASF85
	.byte	0x6b
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI7MonsterES1_E27_S_propagate_on_copy_assignEv\0"
	.long	0x679c
	.uleb128 0x1e
	.secrel32	.LASF86
	.byte	0x6f
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI7MonsterES1_E27_S_propagate_on_move_assignEv\0"
	.long	0x679c
	.uleb128 0x1e
	.secrel32	.LASF87
	.byte	0x73
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI7MonsterES1_E20_S_propagate_on_swapEv\0"
	.long	0x679c
	.uleb128 0x1e
	.secrel32	.LASF88
	.byte	0x77
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI7MonsterES1_E15_S_always_equalEv\0"
	.long	0x679c
	.uleb128 0x1e
	.secrel32	.LASF89
	.byte	0x7b
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI7MonsterES1_E15_S_nothrow_moveEv\0"
	.long	0x679c
	.uleb128 0x11
	.secrel32	.LASF3
	.byte	0x1b
	.byte	0x37
	.byte	0x35
	.long	0x3877
	.uleb128 0x3
	.long	0x7598
	.uleb128 0x11
	.secrel32	.LASF15
	.byte	0x1b
	.byte	0x38
	.byte	0x35
	.long	0x368d
	.uleb128 0x11
	.secrel32	.LASF52
	.byte	0x1b
	.byte	0x3d
	.byte	0x35
	.long	0x7b5f
	.uleb128 0x11
	.secrel32	.LASF54
	.byte	0x1b
	.byte	0x3e
	.byte	0x35
	.long	0x7b64
	.uleb128 0x17
	.ascii "rebind<Monster>\0"
	.byte	0x1
	.byte	0x1b
	.byte	0x7f
	.byte	0xe
	.long	0x75fe
	.uleb128 0x2c
	.ascii "other\0"
	.byte	0x1b
	.byte	0x80
	.byte	0x41
	.long	0x3884
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.byte	0
	.uleb128 0xb
	.secrel32	.LASF37
	.long	0x34fc
	.byte	0
	.uleb128 0x26
	.ascii "__normal_iterator<Monster*, std::vector<Monster, std::allocator<Monster> > >\0"
	.uleb128 0x26
	.ascii "__normal_iterator<const Monster*, std::vector<Monster, std::allocator<Monster> > >\0"
	.uleb128 0x72
	.ascii "operator==<MonsterData*, std::vector<MonsterData> >\0"
	.byte	0x4
	.word	0x4b0
	.byte	0x5
	.ascii "_ZN9__gnu_cxxeqIP11MonsterDataSt6vectorIS1_SaIS1_EEEEbRKNS_17__normal_iteratorIT_T0_EESB_QrqXeqcldtfL0p_4baseEcldtfL0p0_4baseERSt14convertible_toIbEE\0"
	.long	0x679c
	.uleb128 0xb
	.secrel32	.LASF78
	.long	0x78ed
	.uleb128 0xb
	.secrel32	.LASF93
	.long	0x1458
	.uleb128 0x1
	.long	0x92c7
	.uleb128 0x1
	.long	0x92c7
	.byte	0
	.byte	0
	.uleb128 0xc
	.byte	0x10
	.byte	0x4
	.ascii "long double\0"
	.uleb128 0xc
	.byte	0x8
	.byte	0x4
	.ascii "double\0"
	.uleb128 0xc
	.byte	0x4
	.byte	0x4
	.ascii "float\0"
	.uleb128 0xc
	.byte	0x2
	.byte	0x4
	.ascii "_Float16\0"
	.uleb128 0xc
	.byte	0x4
	.byte	0x4
	.ascii "_Float32\0"
	.uleb128 0xc
	.byte	0x8
	.byte	0x4
	.ascii "_Float64\0"
	.uleb128 0xc
	.byte	0x10
	.byte	0x4
	.ascii "_Float128\0"
	.uleb128 0xc
	.byte	0x2
	.byte	0x4
	.ascii "__bf16\0"
	.uleb128 0xc
	.byte	0x10
	.byte	0x5
	.ascii "__int128\0"
	.uleb128 0x73
	.ascii "__gnu_debug\0"
	.byte	0x1c
	.byte	0x27
	.byte	0xb
	.long	0x7821
	.uleb128 0x74
	.byte	0x12
	.byte	0x3a
	.byte	0x18
	.long	0x365
	.byte	0
	.uleb128 0xc
	.byte	0x1
	.byte	0x6
	.ascii "char\0"
	.uleb128 0x3
	.long	0x7821
	.uleb128 0x9
	.long	0x7833
	.uleb128 0x75
	.uleb128 0x76
	.byte	0x8
	.uleb128 0xc
	.byte	0x10
	.byte	0x7
	.ascii "__int128 unsigned\0"
	.uleb128 0x77
	.byte	0x20
	.byte	0x10
	.byte	0x1d
	.word	0x1a8
	.byte	0x10
	.ascii "11max_align_t\0"
	.long	0x7897
	.uleb128 0x60
	.ascii "__max_align_ll\0"
	.word	0x1a9
	.byte	0xd
	.long	0x684d
	.byte	0x8
	.byte	0
	.uleb128 0x60
	.ascii "__max_align_ld\0"
	.word	0x1aa
	.byte	0xf
	.long	0x779b
	.byte	0x10
	.byte	0x10
	.byte	0
	.uleb128 0x78
	.ascii "max_align_t\0"
	.byte	0x1d
	.word	0x1ab
	.byte	0x3
	.long	0x784b
	.byte	0x10
	.uleb128 0x17
	.ascii "MonsterData\0"
	.byte	0x8
	.byte	0x3
	.byte	0x12
	.byte	0x8
	.long	0x78d9
	.uleb128 0x27
	.ascii "x\0"
	.byte	0x3
	.byte	0x12
	.byte	0x1c
	.long	0x77b4
	.byte	0
	.uleb128 0x27
	.ascii "y\0"
	.byte	0x3
	.byte	0x12
	.byte	0x1f
	.long	0x77b4
	.byte	0x4
	.byte	0
	.uleb128 0x3
	.long	0x78ad
	.uleb128 0x9
	.long	0x4d0
	.uleb128 0x4
	.long	0x6e5
	.uleb128 0x4
	.long	0x4d0
	.uleb128 0x9
	.long	0x78ad
	.uleb128 0x3
	.long	0x78ed
	.uleb128 0x9
	.long	0x6e5
	.uleb128 0x9
	.long	0x6ea
	.uleb128 0x4
	.long	0x865
	.uleb128 0x4
	.long	0x6ea
	.uleb128 0x4
	.long	0x903
	.uleb128 0x4
	.long	0x910
	.uleb128 0x9
	.long	0x78d9
	.uleb128 0x4
	.long	0x6b84
	.uleb128 0x4
	.long	0x6b90
	.uleb128 0x9
	.long	0xb00
	.uleb128 0x19
	.long	0xb00
	.uleb128 0x4
	.long	0xcb3
	.uleb128 0x4
	.long	0xb00
	.uleb128 0x9
	.long	0xcc4
	.uleb128 0x4
	.long	0xf05
	.uleb128 0x19
	.long	0xcc4
	.uleb128 0x19
	.long	0xef9
	.uleb128 0x4
	.long	0xef9
	.uleb128 0x9
	.long	0xabf
	.uleb128 0x9
	.long	0x1403
	.uleb128 0x4
	.long	0xfcc
	.uleb128 0x19
	.long	0xabf
	.uleb128 0x4
	.long	0x1661
	.uleb128 0x9
	.long	0x1458
	.uleb128 0x3
	.long	0x796a
	.uleb128 0x4
	.long	0x17ee
	.uleb128 0x4
	.long	0x18b1
	.uleb128 0x4
	.long	0x3184
	.uleb128 0x19
	.long	0x1458
	.uleb128 0x4
	.long	0x3195
	.uleb128 0x4
	.long	0x1458
	.uleb128 0x9
	.long	0x3184
	.uleb128 0x19
	.long	0x18a4
	.uleb128 0x9
	.long	0x7829
	.uleb128 0x4
	.long	0x166e
	.uleb128 0x4
	.long	0x78ad
	.uleb128 0x9
	.long	0x6bf8
	.uleb128 0x3
	.long	0x79ab
	.uleb128 0x4
	.long	0x78f2
	.uleb128 0x9
	.long	0x7283
	.uleb128 0x3
	.long	0x79ba
	.uleb128 0x4
	.long	0x6bf8
	.uleb128 0x9
	.long	0x3304
	.uleb128 0x3
	.long	0x79c9
	.uleb128 0x4
	.long	0x34f7
	.uleb128 0x4
	.long	0x3304
	.uleb128 0x61
	.secrel32	.LASF94
	.byte	0xd
	.long	0x7c27
	.long	0x7b23
	.uleb128 0x2a
	.long	0x7c27
	.uleb128 0x35
	.secrel32	.LASF94
	.ascii "_ZN7MonsterC4EOS_\0"
	.long	0x7a0f
	.long	0x7a1a
	.uleb128 0x2
	.long	0x7b28
	.uleb128 0x1
	.long	0x7d61
	.byte	0
	.uleb128 0x35
	.secrel32	.LASF94
	.ascii "_ZN7MonsterC4ERKS_\0"
	.long	0x7a3a
	.long	0x7a45
	.uleb128 0x2
	.long	0x7b28
	.uleb128 0x1
	.long	0x7c04
	.byte	0
	.uleb128 0x35
	.secrel32	.LASF94
	.ascii "_ZN7MonsterC4Ev\0"
	.long	0x7a62
	.long	0x7a68
	.uleb128 0x2
	.long	0x7b28
	.byte	0
	.uleb128 0x4d
	.secrel32	.LASF12
	.ascii "_ZN7MonsteraSEOS_\0"
	.long	0x7c09
	.long	0x7a8b
	.long	0x7a96
	.uleb128 0x2
	.long	0x7b28
	.uleb128 0x1
	.long	0x7d61
	.byte	0
	.uleb128 0x4d
	.secrel32	.LASF12
	.ascii "_ZN7MonsteraSERKS_\0"
	.long	0x7c09
	.long	0x7aba
	.long	0x7ac5
	.uleb128 0x2
	.long	0x7b28
	.uleb128 0x1
	.long	0x7c04
	.byte	0
	.uleb128 0x62
	.ascii "update\0"
	.byte	0xe
	.byte	0xa
	.ascii "_ZN7Monster6updateEv\0"
	.uleb128 0x2
	.byte	0x10
	.uleb128 0x2
	.long	0x79dd
	.long	0x7af3
	.long	0x7af9
	.uleb128 0x2
	.long	0x7b28
	.byte	0
	.uleb128 0x79
	.ascii "~Monster\0"
	.ascii "_ZN7MonsterD4Ev\0"
	.byte	0x1
	.long	0x79dd
	.long	0x7b1c
	.uleb128 0x2
	.long	0x7b28
	.byte	0
	.byte	0
	.uleb128 0x3
	.long	0x79dd
	.uleb128 0x9
	.long	0x79dd
	.uleb128 0x3
	.long	0x7b28
	.uleb128 0x9
	.long	0x34f7
	.uleb128 0x3
	.long	0x7b32
	.uleb128 0x9
	.long	0x34fc
	.uleb128 0x3
	.long	0x7b3c
	.uleb128 0x4
	.long	0x3655
	.uleb128 0x4
	.long	0x34fc
	.uleb128 0x4
	.long	0x36ea
	.uleb128 0x4
	.long	0x36f7
	.uleb128 0x9
	.long	0x7b23
	.uleb128 0x4
	.long	0x7598
	.uleb128 0x4
	.long	0x75a4
	.uleb128 0x9
	.long	0x38cb
	.uleb128 0x3
	.long	0x7b69
	.uleb128 0x19
	.long	0x38cb
	.uleb128 0x4
	.long	0x3a6a
	.uleb128 0x4
	.long	0x38cb
	.uleb128 0x9
	.long	0x3a7b
	.uleb128 0x3
	.long	0x7b82
	.uleb128 0x4
	.long	0x3cf9
	.uleb128 0x19
	.long	0x3a7b
	.uleb128 0x19
	.long	0x3ced
	.uleb128 0x4
	.long	0x3ced
	.uleb128 0x9
	.long	0x3892
	.uleb128 0x3
	.long	0x7ba0
	.uleb128 0x9
	.long	0x41ac
	.uleb128 0x4
	.long	0x3db6
	.uleb128 0x19
	.long	0x3892
	.uleb128 0x4
	.long	0x43ea
	.uleb128 0x9
	.long	0x41fd
	.uleb128 0x3
	.long	0x7bbe
	.uleb128 0x4
	.long	0x4563
	.uleb128 0x4
	.long	0x461c
	.uleb128 0x4
	.long	0x5d87
	.uleb128 0x19
	.long	0x41fd
	.uleb128 0x4
	.long	0x5d98
	.uleb128 0x4
	.long	0x41fd
	.uleb128 0x9
	.long	0x5d87
	.uleb128 0x3
	.long	0x7be6
	.uleb128 0x19
	.long	0x460f
	.uleb128 0x4
	.long	0x43f7
	.uleb128 0x9
	.long	0x5d9d
	.uleb128 0x9
	.long	0x5f60
	.uleb128 0x4
	.long	0x7b23
	.uleb128 0x4
	.long	0x79dd
	.uleb128 0x9
	.long	0x6043
	.uleb128 0x3
	.long	0x7c0e
	.uleb128 0x4
	.long	0x7b28
	.uleb128 0x9
	.long	0x7b28
	.uleb128 0x4
	.long	0x61d0
	.uleb128 0x61
	.secrel32	.LASF95
	.byte	0x7
	.long	0x7c27
	.long	0x7d5c
	.uleb128 0x35
	.secrel32	.LASF95
	.ascii "_ZN10GameObjectC4ERKS_\0"
	.long	0x7c59
	.long	0x7c64
	.uleb128 0x2
	.long	0x7d66
	.uleb128 0x1
	.long	0x7d70
	.byte	0
	.uleb128 0x35
	.secrel32	.LASF95
	.ascii "_ZN10GameObjectC4Ev\0"
	.long	0x7c85
	.long	0x7c8b
	.uleb128 0x2
	.long	0x7d66
	.byte	0
	.uleb128 0x4d
	.secrel32	.LASF12
	.ascii "_ZN10GameObjectaSERKS_\0"
	.long	0x7d75
	.long	0x7cb3
	.long	0x7cbe
	.uleb128 0x2
	.long	0x7d66
	.uleb128 0x1
	.long	0x7d70
	.byte	0
	.uleb128 0x7a
	.ascii "_vptr.GameObject\0"
	.long	0x7d85
	.byte	0
	.uleb128 0x7b
	.ascii "~GameObject\0"
	.byte	0x3
	.byte	0x8
	.byte	0xd
	.ascii "_ZN10GameObjectD4Ev\0"
	.byte	0x1
	.long	0x7c27
	.byte	0x1
	.long	0x7d07
	.long	0x7d0d
	.uleb128 0x2
	.long	0x7d66
	.byte	0
	.uleb128 0x62
	.ascii "update\0"
	.byte	0x9
	.byte	0x12
	.ascii "_ZN10GameObject6updateEv\0"
	.uleb128 0x2
	.byte	0x10
	.uleb128 0x2
	.long	0x7c27
	.long	0x7d3f
	.long	0x7d45
	.uleb128 0x2
	.long	0x7d66
	.byte	0
	.uleb128 0x27
	.ascii "x\0"
	.byte	0x3
	.byte	0xa
	.byte	0xb
	.long	0x77b4
	.byte	0x8
	.uleb128 0x27
	.ascii "y\0"
	.byte	0x3
	.byte	0xa
	.byte	0xe
	.long	0x77b4
	.byte	0xc
	.byte	0
	.uleb128 0x3
	.long	0x7c27
	.uleb128 0x19
	.long	0x79dd
	.uleb128 0x9
	.long	0x7c27
	.uleb128 0x3
	.long	0x7d66
	.uleb128 0x4
	.long	0x7d5c
	.uleb128 0x4
	.long	0x7c27
	.uleb128 0x7c
	.long	0x683a
	.long	0x7d85
	.uleb128 0x7d
	.byte	0
	.uleb128 0x9
	.long	0x7d8a
	.uleb128 0x7e
	.byte	0x8
	.ascii "__vtbl_ptr_type\0"
	.long	0x7d7a
	.uleb128 0x42
	.secrel32	.LASF96
	.byte	0x2
	.byte	0x8f
	.byte	0x6
	.ascii "_ZdlPv\0"
	.long	0x7db9
	.uleb128 0x1
	.long	0x7834
	.byte	0
	.uleb128 0x42
	.secrel32	.LASF96
	.byte	0x2
	.byte	0x94
	.byte	0x6
	.ascii "_ZdlPvy\0"
	.long	0x7dd8
	.uleb128 0x1
	.long	0x7834
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x4c
	.secrel32	.LASF97
	.byte	0x2
	.byte	0x89
	.byte	0x1a
	.ascii "_Znwy\0"
	.long	0x7834
	.long	0x7df4
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x12
	.long	0x34a2
	.long	0x7e02
	.byte	0x3
	.long	0x7e0c
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b37
	.byte	0
	.uleb128 0x1f
	.long	0x62e0
	.quad	.LFB1820
	.quad	.LFE1820-.LFB1820
	.uleb128 0x1
	.byte	0x9c
	.long	0x7e5f
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x40
	.secrel32	.LASF82
	.uleb128 0x4e
	.secrel32	.LASF98
	.byte	0x60
	.byte	0x17
	.long	0x7b28
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x63
	.ascii "__args\0"
	.byte	0x60
	.byte	0x2a
	.uleb128 0x4f
	.ascii "__loc\0"
	.byte	0xb
	.byte	0x63
	.byte	0xd
	.long	0x7834
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.uleb128 0x2b
	.long	0x33ee
	.long	0x7e7e
	.quad	.LFB1819
	.quad	.LFE1819-.LFB1819
	.uleb128 0x1
	.byte	0x9c
	.long	0x7ed7
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x79ce
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x20
	.ascii "__n\0"
	.byte	0x5
	.byte	0x7e
	.byte	0x1a
	.long	0x3442
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x36
	.long	0x782e
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.uleb128 0x7f
	.long	0x7eb5
	.uleb128 0x80
	.ascii "__al\0"
	.byte	0x5
	.byte	0x92
	.byte	0x17
	.long	0x34f
	.byte	0
	.uleb128 0x23
	.long	0x7df4
	.quad	.LBB177
	.quad	.LBE177-.LBB177
	.byte	0x5
	.byte	0x86
	.byte	0x2e
	.uleb128 0x5
	.long	0x7e02
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.byte	0
	.uleb128 0x2f
	.long	0x610a
	.long	0x7ef6
	.quad	.LFB1818
	.quad	.LFE1818-.LFB1818
	.uleb128 0x1
	.byte	0x9c
	.long	0x7f03
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x7c13
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x1f
	.long	0x6389
	.quad	.LFB1811
	.quad	.LFE1811-.LFB1811
	.uleb128 0x1
	.byte	0x9c
	.long	0x7f5e
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x40
	.secrel32	.LASF82
	.uleb128 0x20
	.ascii "__p\0"
	.byte	0xb
	.byte	0x7b
	.byte	0x15
	.long	0x7b28
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x63
	.ascii "__args\0"
	.byte	0x7b
	.byte	0x21
	.uleb128 0x50
	.long	0x93c6
	.quad	.LBB175
	.quad	.LBE175-.LBB175
	.byte	0xb
	.byte	0x7e
	.byte	0x27
	.byte	0
	.uleb128 0x43
	.long	0x7a45
	.byte	0x3
	.byte	0xd
	.byte	0x8
	.long	0x7f6e
	.long	0x7f78
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b2d
	.byte	0
	.uleb128 0x24
	.long	0x7f5e
	.ascii "_ZN7MonsterC1Ev\0"
	.long	0x7fa7
	.quad	.LFB1817
	.quad	.LFE1817-.LFB1817
	.uleb128 0x1
	.byte	0x9c
	.long	0x7fb0
	.uleb128 0x5
	.long	0x7f6e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x43
	.long	0x7c64
	.byte	0x3
	.byte	0x7
	.byte	0x8
	.long	0x7fc0
	.long	0x7fca
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7d6b
	.byte	0
	.uleb128 0x37
	.long	0x7fb0
	.ascii "_ZN10GameObjectC2Ev\0"
	.long	0x7ffd
	.quad	.LFB1814
	.quad	.LFE1814-.LFB1814
	.uleb128 0x1
	.byte	0x9c
	.long	0x8006
	.uleb128 0x5
	.long	0x7fc0
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x12
	.long	0x60b9
	.long	0x8014
	.byte	0x2
	.long	0x801e
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7c13
	.byte	0
	.uleb128 0x24
	.long	0x8006
	.ascii "_ZNSt19_UninitDestroyGuardIP7MonstervED1Ev\0"
	.long	0x8068
	.quad	.LFB1810
	.quad	.LFE1810-.LFB1810
	.uleb128 0x1
	.byte	0x9c
	.long	0x8071
	.uleb128 0x5
	.long	0x8014
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x2b
	.long	0x344e
	.long	0x8090
	.quad	.LFB1807
	.quad	.LFE1807-.LFB1807
	.uleb128 0x1
	.byte	0x9c
	.long	0x80bb
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x79ce
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x20
	.ascii "__p\0"
	.byte	0x5
	.byte	0x9c
	.byte	0x17
	.long	0x7b28
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x20
	.ascii "__n\0"
	.byte	0x5
	.byte	0x9c
	.byte	0x26
	.long	0x3442
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.byte	0
	.uleb128 0x12
	.long	0x35de
	.long	0x80c9
	.byte	0x3
	.long	0x80df
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b41
	.uleb128 0x30
	.ascii "__n\0"
	.byte	0x6
	.byte	0xc2
	.byte	0x17
	.long	0x280
	.byte	0
	.uleb128 0x1f
	.long	0x63de
	.quad	.LFB1797
	.quad	.LFE1797-.LFB1797
	.uleb128 0x1
	.byte	0x9c
	.long	0x8112
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x4e
	.secrel32	.LASF98
	.byte	0x50
	.byte	0x15
	.long	0x7b28
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x43
	.long	0x7af9
	.byte	0x3
	.byte	0xd
	.byte	0x8
	.long	0x8122
	.long	0x812c
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b2d
	.byte	0
	.uleb128 0x24
	.long	0x8112
	.ascii "_ZN7MonsterD0Ev\0"
	.long	0x815b
	.quad	.LFB1805
	.quad	.LFE1805-.LFB1805
	.uleb128 0x1
	.byte	0x9c
	.long	0x8164
	.uleb128 0x5
	.long	0x8122
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x24
	.long	0x8112
	.ascii "_ZN7MonsterD1Ev\0"
	.long	0x8193
	.quad	.LFB1804
	.quad	.LFE1804-.LFB1804
	.uleb128 0x1
	.byte	0x9c
	.long	0x819c
	.uleb128 0x5
	.long	0x8122
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x12
	.long	0x7cd5
	.long	0x81aa
	.byte	0x2
	.long	0x81b4
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7d6b
	.byte	0
	.uleb128 0x37
	.long	0x819c
	.ascii "_ZN10GameObjectD2Ev\0"
	.long	0x81e7
	.quad	.LFB1800
	.quad	.LFE1800-.LFB1800
	.uleb128 0x1
	.byte	0x9c
	.long	0x81f0
	.uleb128 0x5
	.long	0x81aa
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x1f
	.long	0x3eb
	.quad	.LFB1793
	.quad	.LFE1793-.LFB1793
	.uleb128 0x1
	.byte	0x9c
	.long	0x8273
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0xb
	.secrel32	.LASF7
	.long	0x67b3
	.uleb128 0x51
	.secrel32	.LASF100
	.word	0x383
	.byte	0x2d
	.long	0x7b28
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1d
	.ascii "__n\0"
	.byte	0xa
	.word	0x383
	.byte	0x3c
	.long	0x67b3
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x44
	.ascii "__guard\0"
	.byte	0xa
	.word	0x385
	.byte	0x2a
	.long	0x6043
	.uleb128 0x2
	.byte	0x91
	.sleb128 -64
	.uleb128 0x21
	.long	0x8384
	.quad	.LBB168
	.quad	.LBE168-.LBB168
	.byte	0xa
	.word	0x387
	.byte	0x15
	.uleb128 0x5
	.long	0x8396
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.byte	0
	.uleb128 0x12
	.long	0x6070
	.long	0x8281
	.byte	0x2
	.long	0x8298
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7c13
	.uleb128 0x81
	.secrel32	.LASF100
	.byte	0xa
	.byte	0x71
	.byte	0x2d
	.long	0x7c18
	.byte	0
	.uleb128 0x37
	.long	0x8273
	.ascii "_ZNSt19_UninitDestroyGuardIP7MonstervEC1ERS1_\0"
	.long	0x82e5
	.quad	.LFB1796
	.quad	.LFE1796-.LFB1796
	.uleb128 0x1
	.byte	0x9c
	.long	0x82f6
	.uleb128 0x5
	.long	0x8281
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x5
	.long	0x828a
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x12
	.long	0x3619
	.long	0x8304
	.byte	0x3
	.long	0x8326
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b41
	.uleb128 0x30
	.ascii "__p\0"
	.byte	0x6
	.byte	0xd0
	.byte	0x17
	.long	0x7b28
	.uleb128 0x30
	.ascii "__n\0"
	.byte	0x6
	.byte	0xd0
	.byte	0x23
	.long	0x280
	.byte	0
	.uleb128 0x38
	.long	0x369a
	.long	0x834a
	.uleb128 0x1b
	.ascii "__a\0"
	.byte	0x8
	.word	0x265
	.byte	0x20
	.long	0x7b50
	.uleb128 0x1b
	.ascii "__n\0"
	.byte	0x8
	.word	0x265
	.byte	0x2f
	.long	0x36fc
	.byte	0
	.uleb128 0x1f
	.long	0x6426
	.quad	.LFB1790
	.quad	.LFE1790-.LFB1790
	.uleb128 0x1
	.byte	0x9c
	.long	0x8384
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x20
	.ascii "__pointer\0"
	.byte	0xb
	.byte	0xa1
	.byte	0x13
	.long	0x7b28
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x38
	.long	0x6469
	.long	0x83a3
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x30
	.ascii "__r\0"
	.byte	0xc
	.byte	0x34
	.byte	0x16
	.long	0x7c09
	.byte	0
	.uleb128 0x1f
	.long	0x64bb
	.quad	.LFB1788
	.quad	.LFE1788-.LFB1788
	.uleb128 0x1
	.byte	0x9c
	.long	0x8408
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0xb
	.secrel32	.LASF7
	.long	0x67b3
	.uleb128 0x51
	.secrel32	.LASF100
	.word	0x3be
	.byte	0x30
	.long	0x7b28
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1d
	.ascii "__n\0"
	.byte	0xa
	.word	0x3be
	.byte	0x3f
	.long	0x67b3
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x82
	.ascii "__can_fill\0"
	.byte	0xa
	.word	0x3c9
	.byte	0x16
	.long	0x67a4
	.uleb128 0x2
	.byte	0x91
	.sleb128 -17
	.byte	0
	.uleb128 0x38
	.long	0x376e
	.long	0x8439
	.uleb128 0x1b
	.ascii "__a\0"
	.byte	0x8
	.word	0x288
	.byte	0x22
	.long	0x7b50
	.uleb128 0x1b
	.ascii "__p\0"
	.byte	0x8
	.word	0x288
	.byte	0x2f
	.long	0x368d
	.uleb128 0x1b
	.ascii "__n\0"
	.byte	0x8
	.word	0x288
	.byte	0x3e
	.long	0x36fc
	.byte	0
	.uleb128 0x2b
	.long	0x4097
	.long	0x8458
	.quad	.LFB1786
	.quad	.LFE1786-.LFB1786
	.uleb128 0x1
	.byte	0x9c
	.long	0x84e1
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x7ba5
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1d
	.ascii "__n\0"
	.byte	0x7
	.word	0x180
	.byte	0x1a
	.long	0x280
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x21
	.long	0x8326
	.quad	.LBB161
	.quad	.LBE161-.LBB161
	.byte	0x7
	.word	0x183
	.byte	0x21
	.uleb128 0x5
	.long	0x832f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x5
	.long	0x833c
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x21
	.long	0x80bb
	.quad	.LBB163
	.quad	.LBE163-.LBB163
	.byte	0x8
	.word	0x266
	.byte	0x1c
	.uleb128 0x5
	.long	0x80c9
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.uleb128 0x5
	.long	0x80d2
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.uleb128 0x50
	.long	0x93c6
	.quad	.LBB165
	.quad	.LBE165-.LBB165
	.byte	0x6
	.byte	0xc4
	.byte	0x22
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x12
	.long	0x38f6
	.long	0x84ef
	.byte	0x2
	.long	0x84f9
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b6e
	.byte	0
	.uleb128 0x37
	.long	0x84e1
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE17_Vector_impl_dataC2Ev\0"
	.long	0x8554
	.quad	.LFB1784
	.quad	.LFE1784-.LFB1784
	.uleb128 0x1
	.byte	0x9c
	.long	0x855d
	.uleb128 0x5
	.long	0x84ef
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x12
	.long	0x3361
	.long	0x856b
	.byte	0x2
	.long	0x857a
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x79ce
	.uleb128 0x1
	.long	0x79d3
	.byte	0
	.uleb128 0x28
	.long	0x855d
	.ascii "_ZNSt15__new_allocatorI7MonsterEC2ERKS1_\0"
	.long	0x85b0
	.long	0x85bb
	.uleb128 0x10
	.long	0x856b
	.uleb128 0x10
	.long	0x8574
	.byte	0
	.uleb128 0x4
	.long	0x67cd
	.uleb128 0x83
	.long	0x6554
	.quad	.LFB1779
	.quad	.LFE1779-.LFB1779
	.uleb128 0x1
	.byte	0x9c
	.long	0x8604
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x67b3
	.uleb128 0x20
	.ascii "__a\0"
	.byte	0xd
	.byte	0xea
	.byte	0x14
	.long	0x85bb
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x20
	.ascii "__b\0"
	.byte	0xd
	.byte	0xea
	.byte	0x24
	.long	0x85bb
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x1f
	.long	0x65a5
	.quad	.LFB1777
	.quad	.LFE1777-.LFB1777
	.uleb128 0x1
	.byte	0x9c
	.long	0x866a
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0x4e
	.secrel32	.LASF100
	.byte	0xdb
	.byte	0x1f
	.long	0x7b28
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x20
	.ascii "__last\0"
	.byte	0xb
	.byte	0xdb
	.byte	0x39
	.long	0x7b28
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x23
	.long	0x8384
	.quad	.LBB158
	.quad	.LBE158-.LBB158
	.byte	0xb
	.byte	0xe2
	.byte	0x11
	.uleb128 0x5
	.long	0x8396
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.byte	0
	.uleb128 0x1f
	.long	0x65f1
	.quad	.LFB1776
	.quad	.LFE1776-.LFB1776
	.uleb128 0x1
	.byte	0x9c
	.long	0x86c8
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0xb
	.secrel32	.LASF7
	.long	0x67b3
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x51
	.secrel32	.LASF100
	.word	0x403
	.byte	0x32
	.long	0x7b28
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1d
	.ascii "__n\0"
	.byte	0xa
	.word	0x403
	.byte	0x41
	.long	0x67b3
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x36
	.long	0x7b4b
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.byte	0
	.uleb128 0x2b
	.long	0x40e9
	.long	0x86e7
	.quad	.LFB1775
	.quad	.LFE1775-.LFB1775
	.uleb128 0x1
	.byte	0x9c
	.long	0x8790
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x7ba5
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1d
	.ascii "__p\0"
	.byte	0x7
	.word	0x188
	.byte	0x1d
	.long	0x3a6f
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x1d
	.ascii "__n\0"
	.byte	0x7
	.word	0x188
	.byte	0x29
	.long	0x280
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.uleb128 0x21
	.long	0x8408
	.quad	.LBB152
	.quad	.LBE152-.LBB152
	.byte	0x7
	.word	0x18c
	.byte	0x13
	.uleb128 0x5
	.long	0x8411
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x5
	.long	0x841e
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x5
	.long	0x842b
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.uleb128 0x21
	.long	0x82f6
	.quad	.LBB154
	.quad	.LBE154-.LBB154
	.byte	0x8
	.word	0x289
	.byte	0x17
	.uleb128 0x5
	.long	0x8304
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.uleb128 0x5
	.long	0x830d
	.uleb128 0x2
	.byte	0x91
	.sleb128 -56
	.uleb128 0x5
	.long	0x8319
	.uleb128 0x2
	.byte	0x91
	.sleb128 -64
	.uleb128 0x50
	.long	0x93c6
	.quad	.LBB156
	.quad	.LBE156-.LBB156
	.byte	0x6
	.byte	0xd2
	.byte	0x22
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x2b
	.long	0x4142
	.long	0x87af
	.quad	.LFB1774
	.quad	.LFE1774-.LFB1774
	.uleb128 0x1
	.byte	0x9c
	.long	0x87cc
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x7ba5
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1d
	.ascii "__n\0"
	.byte	0x7
	.word	0x193
	.byte	0x20
	.long	0x280
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x12
	.long	0x3b3e
	.long	0x87da
	.byte	0x2
	.long	0x87f0
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b87
	.uleb128 0x30
	.ascii "__a\0"
	.byte	0x7
	.byte	0x98
	.byte	0x25
	.long	0x7b8c
	.byte	0
	.uleb128 0x24
	.long	0x87cc
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implC1ERKS1_\0"
	.long	0x884a
	.quad	.LFB1773
	.quad	.LFE1773-.LFB1773
	.uleb128 0x1
	.byte	0x9c
	.long	0x88ad
	.uleb128 0x5
	.long	0x87da
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x5
	.long	0x87e3
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x23
	.long	0x88ad
	.quad	.LBB147
	.quad	.LBE147-.LBB147
	.byte	0x7
	.byte	0x99
	.byte	0x16
	.uleb128 0x5
	.long	0x88bb
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x5
	.long	0x88c4
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x23
	.long	0x855d
	.quad	.LBB150
	.quad	.LBE150-.LBB150
	.byte	0x6
	.byte	0xad
	.byte	0x22
	.uleb128 0x5
	.long	0x856b
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.uleb128 0x5
	.long	0x8574
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x12
	.long	0x3548
	.long	0x88bb
	.byte	0x2
	.long	0x88d1
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b41
	.uleb128 0x30
	.ascii "__a\0"
	.byte	0x6
	.byte	0xac
	.byte	0x22
	.long	0x7b46
	.byte	0
	.uleb128 0x28
	.long	0x88ad
	.ascii "_ZNSaI7MonsterEC1ERKS0_\0"
	.long	0x88f6
	.long	0x8901
	.uleb128 0x10
	.long	0x88bb
	.uleb128 0x10
	.long	0x88c4
	.byte	0
	.uleb128 0x28
	.long	0x88ad
	.ascii "_ZNSaI7MonsterEC2ERKS0_\0"
	.long	0x8926
	.long	0x8931
	.uleb128 0x10
	.long	0x88bb
	.uleb128 0x10
	.long	0x88c4
	.byte	0
	.uleb128 0x1f
	.long	0x5b19
	.quad	.LFB1766
	.quad	.LFE1766-.LFB1766
	.uleb128 0x1
	.byte	0x9c
	.long	0x898a
	.uleb128 0x1d
	.ascii "__a\0"
	.byte	0x7
	.word	0x8ae
	.byte	0x29
	.long	0x7bf5
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x44
	.ascii "__diffmax\0"
	.byte	0x7
	.word	0x8b3
	.byte	0xf
	.long	0x28f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x44
	.ascii "__allocmax\0"
	.byte	0x7
	.word	0x8b5
	.byte	0xf
	.long	0x28f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.byte	0
	.uleb128 0x2f
	.long	0x4d8b
	.long	0x89a9
	.quad	.LFB1765
	.quad	.LFE1765-.LFB1765
	.uleb128 0x1
	.byte	0x9c
	.long	0x89c8
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x7beb
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x44
	.ascii "__dif\0"
	.byte	0x7
	.word	0x45f
	.byte	0xc
	.long	0x371
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.uleb128 0x38
	.long	0x66b0
	.long	0x8a07
	.uleb128 0xb
	.secrel32	.LASF6
	.long	0x7b28
	.uleb128 0xa
	.ascii "_Tp\0"
	.long	0x79dd
	.uleb128 0x84
	.secrel32	.LASF100
	.byte	0x8
	.word	0x412
	.byte	0x1f
	.long	0x7b28
	.uleb128 0x1b
	.ascii "__last\0"
	.byte	0x8
	.word	0x412
	.byte	0x39
	.long	0x7b28
	.uleb128 0x1
	.long	0x7b4b
	.byte	0
	.uleb128 0x2f
	.long	0x3cfe
	.long	0x8a26
	.quad	.LFB1763
	.quad	.LFE1763-.LFB1763
	.uleb128 0x1
	.byte	0x9c
	.long	0x8a33
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x7ba5
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x2b
	.long	0x5747
	.long	0x8a52
	.quad	.LFB1762
	.quad	.LFE1762-.LFB1762
	.uleb128 0x1
	.byte	0x9c
	.long	0x8a6f
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x7bc3
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1d
	.ascii "__n\0"
	.byte	0x7
	.word	0x7d8
	.byte	0x27
	.long	0x45af
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x12
	.long	0x404c
	.long	0x8a7d
	.byte	0x2
	.long	0x8a87
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7ba5
	.byte	0
	.uleb128 0x24
	.long	0x8a6f
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EED2Ev\0"
	.long	0x8acf
	.quad	.LFB1760
	.quad	.LFE1760-.LFB1760
	.uleb128 0x1
	.byte	0x9c
	.long	0x8ad8
	.uleb128 0x5
	.long	0x8a7d
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x12
	.long	0x3ed3
	.long	0x8ae6
	.byte	0x2
	.long	0x8b0a
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7ba5
	.uleb128 0x1b
	.ascii "__n\0"
	.byte	0x7
	.word	0x153
	.byte	0x1b
	.long	0x280
	.uleb128 0x1b
	.ascii "__a\0"
	.byte	0x7
	.word	0x153
	.byte	0x36
	.long	0x7baf
	.byte	0
	.uleb128 0x24
	.long	0x8ad8
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EEC2EyRKS1_\0"
	.long	0x8b57
	.quad	.LFB1757
	.quad	.LFE1757-.LFB1757
	.uleb128 0x1
	.byte	0x9c
	.long	0x8b70
	.uleb128 0x5
	.long	0x8ae6
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x5
	.long	0x8aef
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x5
	.long	0x8afc
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.byte	0
	.uleb128 0x43
	.long	0x3c9c
	.byte	0x7
	.byte	0x8b
	.byte	0xe
	.long	0x8b80
	.long	0x8b8a
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b87
	.byte	0
	.uleb128 0x37
	.long	0x8b70
	.ascii "_ZNSt12_Vector_baseI7MonsterSaIS0_EE12_Vector_implD1Ev\0"
	.long	0x8be0
	.quad	.LFB1756
	.quad	.LFE1756-.LFB1756
	.uleb128 0x1
	.byte	0x9c
	.long	0x8c0a
	.uleb128 0x5
	.long	0x8b80
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x23
	.long	0x8f2f
	.quad	.LBB141
	.quad	.LBE141-.LBB141
	.byte	0x7
	.byte	0x8b
	.byte	0xe
	.uleb128 0x5
	.long	0x8f3d
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.byte	0
	.uleb128 0x1f
	.long	0x5ac7
	.quad	.LFB1752
	.quad	.LFE1752-.LFB1752
	.uleb128 0x1
	.byte	0x9c
	.long	0x8cb8
	.uleb128 0x1d
	.ascii "__n\0"
	.byte	0x7
	.word	0x8a5
	.byte	0x23
	.long	0x45af
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1d
	.ascii "__a\0"
	.byte	0x7
	.word	0x8a5
	.byte	0x3e
	.long	0x7bc8
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x64
	.long	0x88ad
	.quad	.LBB133
	.quad	.LBE133-.LBB133
	.byte	0x7
	.word	0x8a7
	.long	0x8c98
	.uleb128 0x10
	.long	0x88bb
	.uleb128 0x5
	.long	0x88c4
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x23
	.long	0x855d
	.quad	.LBB136
	.quad	.LBE136-.LBB136
	.byte	0x6
	.byte	0xad
	.byte	0x22
	.uleb128 0x5
	.long	0x856b
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x5
	.long	0x8574
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.byte	0
	.uleb128 0x21
	.long	0x8f2f
	.quad	.LBB138
	.quad	.LBE138-.LBB138
	.byte	0x7
	.word	0x8a7
	.byte	0x18
	.uleb128 0x10
	.long	0x8f3d
	.byte	0
	.byte	0
	.uleb128 0x12
	.long	0x3325
	.long	0x8cc6
	.byte	0x2
	.long	0x8cd0
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x79ce
	.byte	0
	.uleb128 0x28
	.long	0x8cb8
	.ascii "_ZNSt15__new_allocatorI7MonsterEC2Ev\0"
	.long	0x8d02
	.long	0x8d08
	.uleb128 0x10
	.long	0x8cc6
	.byte	0
	.uleb128 0x12
	.long	0x6cd2
	.long	0x8d16
	.byte	0x2
	.long	0x8d2d
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x79b0
	.uleb128 0x1b
	.ascii "__i\0"
	.byte	0x4
	.word	0x422
	.byte	0x2a
	.long	0x79b5
	.byte	0
	.uleb128 0x28
	.long	0x8d08
	.ascii "_ZN9__gnu_cxx17__normal_iteratorIP11MonsterDataSt6vectorIS1_SaIS1_EEEC1ERKS2_\0"
	.long	0x8d88
	.long	0x8d93
	.uleb128 0x10
	.long	0x8d16
	.uleb128 0x10
	.long	0x8d1f
	.byte	0
	.uleb128 0x2b
	.long	0x4fc6
	.long	0x8db2
	.quad	.LFB1745
	.quad	.LFE1745-.LFB1745
	.uleb128 0x1
	.byte	0x9c
	.long	0x8df3
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x7bc3
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1d
	.ascii "__n\0"
	.byte	0x7
	.word	0x4ed
	.byte	0x1c
	.long	0x45af
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x85
	.ascii "__PRETTY_FUNCTION__\0"
	.long	0x8e05
	.uleb128 0x9
	.byte	0x3
	.quad	.LC2
	.byte	0
	.uleb128 0x86
	.long	0x7829
	.long	0x8e05
	.uleb128 0x87
	.long	0x67b3
	.byte	0xce
	.byte	0
	.uleb128 0x3
	.long	0x8df3
	.uleb128 0x12
	.long	0x4871
	.long	0x8e18
	.byte	0x2
	.long	0x8e22
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7bc3
	.byte	0
	.uleb128 0x24
	.long	0x8e0a
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EED1Ev\0"
	.long	0x8e63
	.quad	.LFB1744
	.quad	.LFE1744-.LFB1744
	.uleb128 0x1
	.byte	0x9c
	.long	0x8e9e
	.uleb128 0x5
	.long	0x8e18
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x21
	.long	0x89c8
	.quad	.LBB131
	.quad	.LBE131-.LBB131
	.byte	0x7
	.word	0x322
	.byte	0xf
	.uleb128 0x5
	.long	0x89e3
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x5
	.long	0x89f1
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x5
	.long	0x8a01
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.byte	0
	.uleb128 0x12
	.long	0x4568
	.long	0x8eac
	.byte	0x2
	.long	0x8ed0
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7bc3
	.uleb128 0x1b
	.ascii "__n\0"
	.byte	0x7
	.word	0x24a
	.byte	0x18
	.long	0x45af
	.uleb128 0x1b
	.ascii "__a\0"
	.byte	0x7
	.word	0x24a
	.byte	0x33
	.long	0x7bc8
	.byte	0
	.uleb128 0x24
	.long	0x8e9e
	.ascii "_ZNSt6vectorI7MonsterSaIS0_EEC1EyRKS1_\0"
	.long	0x8f16
	.quad	.LFB1741
	.quad	.LFE1741-.LFB1741
	.uleb128 0x1
	.byte	0x9c
	.long	0x8f2f
	.uleb128 0x5
	.long	0x8eac
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x5
	.long	0x8eb5
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x5
	.long	0x8ec2
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.byte	0
	.uleb128 0x12
	.long	0x35b3
	.long	0x8f3d
	.byte	0x2
	.long	0x8f47
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b41
	.byte	0
	.uleb128 0x28
	.long	0x8f2f
	.ascii "_ZNSaI7MonsterED1Ev\0"
	.long	0x8f68
	.long	0x8f6e
	.uleb128 0x10
	.long	0x8f3d
	.byte	0
	.uleb128 0x28
	.long	0x8f2f
	.ascii "_ZNSaI7MonsterED2Ev\0"
	.long	0x8f8f
	.long	0x8f95
	.uleb128 0x10
	.long	0x8f3d
	.byte	0
	.uleb128 0x12
	.long	0x351d
	.long	0x8fa3
	.byte	0x2
	.long	0x8fad
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x7b41
	.byte	0
	.uleb128 0x28
	.long	0x8f95
	.ascii "_ZNSaI7MonsterEC1Ev\0"
	.long	0x8fce
	.long	0x8fd4
	.uleb128 0x10
	.long	0x8fa3
	.byte	0
	.uleb128 0x12
	.long	0x6e2c
	.long	0x8fe2
	.byte	0x3
	.long	0x8fec
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x79b0
	.byte	0
	.uleb128 0x2f
	.long	0x1dbc
	.long	0x900b
	.quad	.LFB1731
	.quad	.LFE1731-.LFB1731
	.uleb128 0x1
	.byte	0x9c
	.long	0x903f
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x796f
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x21
	.long	0x8d08
	.quad	.LBB125
	.quad	.LBE125-.LBB125
	.byte	0x7
	.word	0x3fb
	.byte	0x10
	.uleb128 0x10
	.long	0x8d16
	.uleb128 0x5
	.long	0x8d1f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.byte	0
	.uleb128 0x2f
	.long	0x1d20
	.long	0x905e
	.quad	.LFB1730
	.quad	.LFE1730-.LFB1730
	.uleb128 0x1
	.byte	0x9c
	.long	0x9092
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x796f
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x21
	.long	0x8d08
	.quad	.LBB122
	.quad	.LBE122-.LBB122
	.byte	0x7
	.word	0x3e7
	.byte	0x10
	.uleb128 0x10
	.long	0x8d16
	.uleb128 0x5
	.long	0x8d1f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.byte	0
	.uleb128 0x88
	.ascii "main\0"
	.byte	0x3
	.byte	0x17
	.byte	0x5
	.long	0x683a
	.quad	.LFB1724
	.quad	.LFE1724-.LFB1724
	.uleb128 0x1
	.byte	0x9c
	.long	0x9126
	.uleb128 0x4f
	.ascii "ms\0"
	.byte	0x3
	.byte	0x18
	.byte	0x1a
	.long	0x41fd
	.uleb128 0x3
	.byte	0x91
	.sleb128 -80
	.uleb128 0x52
	.long	0x8f95
	.quad	.LBB115
	.quad	.LBE115-.LBB115
	.byte	0x18
	.byte	0x1f
	.long	0x9107
	.uleb128 0x10
	.long	0x8fa3
	.uleb128 0x23
	.long	0x8cb8
	.quad	.LBB118
	.quad	.LBE118-.LBB118
	.byte	0x6
	.byte	0xa8
	.byte	0x24
	.uleb128 0x5
	.long	0x8cc6
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.byte	0
	.uleb128 0x23
	.long	0x8f2f
	.quad	.LBB120
	.quad	.LBE120-.LBB120
	.byte	0x3
	.byte	0x18
	.byte	0x1f
	.uleb128 0x10
	.long	0x8f3d
	.byte	0
	.byte	0
	.uleb128 0x89
	.ascii "monster_system\0"
	.byte	0x3
	.byte	0x13
	.byte	0x6
	.ascii "_Z14monster_systemRSt6vectorI11MonsterDataSaIS0_EE\0"
	.quad	.LFB1720
	.quad	.LFE1720-.LFB1720
	.uleb128 0x1
	.byte	0x9c
	.long	0x9297
	.uleb128 0x20
	.ascii "m\0"
	.byte	0x3
	.byte	0x13
	.byte	0x2f
	.long	0x798d
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x8a
	.quad	.LBB104
	.quad	.LBE104-.LBB104
	.uleb128 0x4f
	.ascii "d\0"
	.byte	0x3
	.byte	0x14
	.byte	0x10
	.long	0x79a6
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x53
	.ascii "__for_range\0"
	.long	0x798d
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x53
	.ascii "__for_begin\0"
	.long	0x1d13
	.uleb128 0x2
	.byte	0x91
	.sleb128 -56
	.uleb128 0x53
	.ascii "__for_end\0"
	.long	0x1d13
	.uleb128 0x2
	.byte	0x91
	.sleb128 -64
	.uleb128 0x52
	.long	0x9297
	.quad	.LBB105
	.quad	.LBE105-.LBB105
	.byte	0x14
	.byte	0x14
	.long	0x920a
	.uleb128 0x10
	.long	0x92a5
	.byte	0
	.uleb128 0x52
	.long	0x8fd4
	.quad	.LBB107
	.quad	.LBE107-.LBB107
	.byte	0x14
	.byte	0x14
	.long	0x922b
	.uleb128 0x10
	.long	0x8fe2
	.byte	0
	.uleb128 0x23
	.long	0x92cc
	.quad	.LBB109
	.quad	.LBE109-.LBB109
	.byte	0x3
	.byte	0x14
	.byte	0x14
	.uleb128 0x10
	.long	0x92e7
	.uleb128 0x10
	.long	0x92f6
	.uleb128 0x64
	.long	0x92af
	.quad	.LBB111
	.quad	.LBE111-.LBB111
	.byte	0x4
	.word	0x4b6
	.long	0x9272
	.uleb128 0x5
	.long	0x92bd
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.uleb128 0x21
	.long	0x92af
	.quad	.LBB113
	.quad	.LBE113-.LBB113
	.byte	0x4
	.word	0x4b6
	.byte	0x28
	.uleb128 0x5
	.long	0x92bd
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.byte	0
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x12
	.long	0x6d48
	.long	0x92a5
	.byte	0x3
	.long	0x92af
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x79bf
	.byte	0
	.uleb128 0x12
	.long	0x7207
	.long	0x92bd
	.byte	0x3
	.long	0x92c7
	.uleb128 0xd
	.secrel32	.LASF99
	.long	0x79bf
	.byte	0
	.uleb128 0x4
	.long	0x7283
	.uleb128 0x38
	.long	0x76aa
	.long	0x9306
	.uleb128 0xb
	.secrel32	.LASF78
	.long	0x78ed
	.uleb128 0xb
	.secrel32	.LASF93
	.long	0x1458
	.uleb128 0x1b
	.ascii "__lhs\0"
	.byte	0x4
	.word	0x4b0
	.byte	0x40
	.long	0x92c7
	.uleb128 0x1b
	.ascii "__rhs\0"
	.byte	0x4
	.word	0x4b1
	.byte	0x39
	.long	0x92c7
	.byte	0
	.uleb128 0x2f
	.long	0x7ac5
	.long	0x9325
	.quad	.LFB1719
	.quad	.LFE1719-.LFB1719
	.uleb128 0x1
	.byte	0x9c
	.long	0x9332
	.uleb128 0x1a
	.secrel32	.LASF99
	.long	0x7b2d
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x8b
	.secrel32	.LASF96
	.byte	0x2
	.byte	0xd9
	.byte	0xd
	.ascii "_ZdlPvS_\0"
	.quad	.LFB222
	.quad	.LFE222-.LFB222
	.uleb128 0x1
	.byte	0x9c
	.long	0x936b
	.uleb128 0x36
	.long	0x7834
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x36
	.long	0x7834
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x8c
	.secrel32	.LASF97
	.byte	0x2
	.byte	0xce
	.byte	0x7
	.ascii "_ZnwyPv\0"
	.long	0x7834
	.quad	.LFB220
	.quad	.LFE220-.LFB220
	.uleb128 0x1
	.byte	0x9c
	.long	0x93ae
	.uleb128 0x36
	.long	0x280
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x20
	.ascii "__p\0"
	.byte	0x2
	.byte	0xce
	.byte	0x27
	.long	0x7834
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x8d
	.long	0x6721
	.quad	.LFB15
	.quad	.LFE15-.LFB15
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x8e
	.long	0x675c
	.byte	0x3
	.byte	0
	.section	.debug_abbrev,"dr"
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x3
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x10
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x32
	.uleb128 0xb
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x32
	.uleb128 0xb
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
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
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xa
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xb
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xc
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
	.uleb128 0xd
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0xe
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
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
	.uleb128 0xf
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.byte	0
	.byte	0
	.uleb128 0x10
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x11
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
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
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x14
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x15
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x16
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x32
	.uleb128 0xb
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x17
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
	.uleb128 0x18
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x32
	.uleb128 0xb
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x19
	.uleb128 0x42
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1a
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x1b
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1c
	.uleb128 0x8
	.byte	0
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 458
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x18
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1d
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x1e
	.uleb128 0x2e
	.byte	0
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 27
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 27
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x1f
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
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
	.uleb128 0x20
	.uleb128 0x5
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
	.uleb128 0x21
	.uleb128 0x1d
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x58
	.uleb128 0xb
	.uleb128 0x59
	.uleb128 0x5
	.uleb128 0x57
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x22
	.uleb128 0x8
	.byte	0
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x18
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x23
	.uleb128 0x1d
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x58
	.uleb128 0xb
	.uleb128 0x59
	.uleb128 0xb
	.uleb128 0x57
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x24
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
	.uleb128 0x25
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x26
	.uleb128 0x2
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x27
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
	.uleb128 0x28
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x29
	.uleb128 0x39
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x2a
	.uleb128 0x1c
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0x21
	.sleb128 0
	.byte	0
	.byte	0
	.uleb128 0x2b
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
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
	.uleb128 0x2c
	.uleb128 0x16
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
	.byte	0
	.byte	0
	.uleb128 0x2d
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 10
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x2e
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2f
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
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
	.uleb128 0x30
	.uleb128 0x5
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
	.byte	0
	.byte	0
	.uleb128 0x31
	.uleb128 0x39
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x32
	.uleb128 0x2
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
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x33
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.byte	0
	.byte	0
	.uleb128 0x34
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x63
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x35
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x36
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x37
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
	.uleb128 0x38
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x20
	.uleb128 0x21
	.sleb128 3
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x39
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3a
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x8b
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3b
	.uleb128 0x1c
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0x21
	.sleb128 0
	.uleb128 0x32
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x3c
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 24
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 14
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3d
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x8b
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3e
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x8b
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3f
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x40
	.uleb128 0x4107
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.byte	0
	.byte	0
	.uleb128 0x41
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 5
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x42
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x43
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
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x44
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x45
	.uleb128 0x39
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x46
	.uleb128 0x30
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1c
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x47
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 12
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x48
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 10
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x49
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4a
	.uleb128 0x2
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4b
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
	.uleb128 0x21
	.sleb128 5
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4c
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4d
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4e
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 11
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
	.uleb128 0x4f
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
	.uleb128 0x50
	.uleb128 0x1d
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x58
	.uleb128 0xb
	.uleb128 0x59
	.uleb128 0xb
	.uleb128 0x57
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x51
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 10
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x52
	.uleb128 0x1d
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x58
	.uleb128 0x21
	.sleb128 3
	.uleb128 0x59
	.uleb128 0xb
	.uleb128 0x57
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x53
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x54
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 17
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x55
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 9
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x56
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 6
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x57
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 648
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x58
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 380
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 20
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0x21
	.sleb128 0
	.byte	0
	.byte	0
	.uleb128 0x59
	.uleb128 0x2e
	.byte	0
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 513
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x5a
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 22
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 5
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x5b
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1e
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x5c
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 24
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x32
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x5d
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 10
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
	.uleb128 0x5e
	.uleb128 0x2e
	.byte	0
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 25
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 3
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x87
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x5f
	.uleb128 0x2e
	.byte	0
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 3
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x60
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 29
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x88
	.uleb128 0xb
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x61
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 16
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 3
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x62
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 3
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x4c
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x4d
	.uleb128 0x18
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x63
	.uleb128 0x4108
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x64
	.uleb128 0x1d
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x58
	.uleb128 0xb
	.uleb128 0x59
	.uleb128 0x5
	.uleb128 0x57
	.uleb128 0x21
	.sleb128 24
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x65
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
	.uleb128 0x66
	.uleb128 0x39
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x89
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x67
	.uleb128 0x39
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x68
	.uleb128 0x39
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x69
	.uleb128 0x39
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x89
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x6a
	.uleb128 0x4
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x6d
	.uleb128 0x19
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x6b
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
	.uleb128 0x6c
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x63
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x6d
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.byte	0
	.byte	0
	.uleb128 0x6e
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x87
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x6f
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
	.uleb128 0x87
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x70
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x71
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.uleb128 0x32
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x72
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x73
	.uleb128 0x39
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
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
	.uleb128 0x74
	.uleb128 0x3a
	.byte	0
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x18
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x75
	.uleb128 0x26
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x76
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x77
	.uleb128 0x13
	.byte	0x1
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x88
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x78
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x88
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x79
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x4c
	.uleb128 0xb
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7a
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x7b
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
	.uleb128 0x4c
	.uleb128 0xb
	.uleb128 0x1d
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x8b
	.uleb128 0xb
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7c
	.uleb128 0x15
	.byte	0x1
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7d
	.uleb128 0x18
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x7e
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7f
	.uleb128 0xb
	.byte	0x1
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x80
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
	.byte	0
	.byte	0
	.uleb128 0x81
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x82
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x6c
	.uleb128 0x19
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x83
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
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
	.uleb128 0x84
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x85
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x6c
	.uleb128 0x19
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x86
	.uleb128 0x1
	.byte	0x1
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x87
	.uleb128 0x21
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2f
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x88
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
	.uleb128 0x89
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
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x8a
	.uleb128 0xb
	.byte	0x1
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.byte	0
	.byte	0
	.uleb128 0x8b
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x8c
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x8d
	.uleb128 0x2e
	.byte	0
	.uleb128 0x47
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
	.uleb128 0x8e
	.uleb128 0x2e
	.byte	0
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x20
	.uleb128 0xb
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"dr"
	.long	0x2bc
	.word	0x2
	.secrel32	.Ldebug_info0
	.byte	0x8
	.byte	0
	.word	0
	.word	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	.LFB15
	.quad	.LFE15-.LFB15
	.quad	.LFB220
	.quad	.LFE220-.LFB220
	.quad	.LFB222
	.quad	.LFE222-.LFB222
	.quad	.LFB1719
	.quad	.LFE1719-.LFB1719
	.quad	.LFB1730
	.quad	.LFE1730-.LFB1730
	.quad	.LFB1731
	.quad	.LFE1731-.LFB1731
	.quad	.LFB1741
	.quad	.LFE1741-.LFB1741
	.quad	.LFB1744
	.quad	.LFE1744-.LFB1744
	.quad	.LFB1745
	.quad	.LFE1745-.LFB1745
	.quad	.LFB1752
	.quad	.LFE1752-.LFB1752
	.quad	.LFB1756
	.quad	.LFE1756-.LFB1756
	.quad	.LFB1757
	.quad	.LFE1757-.LFB1757
	.quad	.LFB1760
	.quad	.LFE1760-.LFB1760
	.quad	.LFB1762
	.quad	.LFE1762-.LFB1762
	.quad	.LFB1763
	.quad	.LFE1763-.LFB1763
	.quad	.LFB1765
	.quad	.LFE1765-.LFB1765
	.quad	.LFB1766
	.quad	.LFE1766-.LFB1766
	.quad	.LFB1773
	.quad	.LFE1773-.LFB1773
	.quad	.LFB1774
	.quad	.LFE1774-.LFB1774
	.quad	.LFB1775
	.quad	.LFE1775-.LFB1775
	.quad	.LFB1776
	.quad	.LFE1776-.LFB1776
	.quad	.LFB1777
	.quad	.LFE1777-.LFB1777
	.quad	.LFB1779
	.quad	.LFE1779-.LFB1779
	.quad	.LFB1784
	.quad	.LFE1784-.LFB1784
	.quad	.LFB1786
	.quad	.LFE1786-.LFB1786
	.quad	.LFB1788
	.quad	.LFE1788-.LFB1788
	.quad	.LFB1790
	.quad	.LFE1790-.LFB1790
	.quad	.LFB1796
	.quad	.LFE1796-.LFB1796
	.quad	.LFB1793
	.quad	.LFE1793-.LFB1793
	.quad	.LFB1800
	.quad	.LFE1800-.LFB1800
	.quad	.LFB1804
	.quad	.LFE1804-.LFB1804
	.quad	.LFB1805
	.quad	.LFE1805-.LFB1805
	.quad	.LFB1797
	.quad	.LFE1797-.LFB1797
	.quad	.LFB1807
	.quad	.LFE1807-.LFB1807
	.quad	.LFB1810
	.quad	.LFE1810-.LFB1810
	.quad	.LFB1814
	.quad	.LFE1814-.LFB1814
	.quad	.LFB1817
	.quad	.LFE1817-.LFB1817
	.quad	.LFB1811
	.quad	.LFE1811-.LFB1811
	.quad	.LFB1818
	.quad	.LFE1818-.LFB1818
	.quad	.LFB1819
	.quad	.LFE1819-.LFB1819
	.quad	.LFB1820
	.quad	.LFE1820-.LFB1820
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
	.quad	.LFB15
	.uleb128 .LFE15-.LFB15
	.byte	0x7
	.quad	.LFB220
	.uleb128 .LFE220-.LFB220
	.byte	0x7
	.quad	.LFB222
	.uleb128 .LFE222-.LFB222
	.byte	0x7
	.quad	.LFB1719
	.uleb128 .LFE1719-.LFB1719
	.byte	0x7
	.quad	.LFB1730
	.uleb128 .LFE1730-.LFB1730
	.byte	0x7
	.quad	.LFB1731
	.uleb128 .LFE1731-.LFB1731
	.byte	0x7
	.quad	.LFB1741
	.uleb128 .LFE1741-.LFB1741
	.byte	0x7
	.quad	.LFB1744
	.uleb128 .LFE1744-.LFB1744
	.byte	0x7
	.quad	.LFB1745
	.uleb128 .LFE1745-.LFB1745
	.byte	0x7
	.quad	.LFB1752
	.uleb128 .LFE1752-.LFB1752
	.byte	0x7
	.quad	.LFB1756
	.uleb128 .LFE1756-.LFB1756
	.byte	0x7
	.quad	.LFB1757
	.uleb128 .LFE1757-.LFB1757
	.byte	0x7
	.quad	.LFB1760
	.uleb128 .LFE1760-.LFB1760
	.byte	0x7
	.quad	.LFB1762
	.uleb128 .LFE1762-.LFB1762
	.byte	0x7
	.quad	.LFB1763
	.uleb128 .LFE1763-.LFB1763
	.byte	0x7
	.quad	.LFB1765
	.uleb128 .LFE1765-.LFB1765
	.byte	0x7
	.quad	.LFB1766
	.uleb128 .LFE1766-.LFB1766
	.byte	0x7
	.quad	.LFB1773
	.uleb128 .LFE1773-.LFB1773
	.byte	0x7
	.quad	.LFB1774
	.uleb128 .LFE1774-.LFB1774
	.byte	0x7
	.quad	.LFB1775
	.uleb128 .LFE1775-.LFB1775
	.byte	0x7
	.quad	.LFB1776
	.uleb128 .LFE1776-.LFB1776
	.byte	0x7
	.quad	.LFB1777
	.uleb128 .LFE1777-.LFB1777
	.byte	0x7
	.quad	.LFB1779
	.uleb128 .LFE1779-.LFB1779
	.byte	0x7
	.quad	.LFB1784
	.uleb128 .LFE1784-.LFB1784
	.byte	0x7
	.quad	.LFB1786
	.uleb128 .LFE1786-.LFB1786
	.byte	0x7
	.quad	.LFB1788
	.uleb128 .LFE1788-.LFB1788
	.byte	0x7
	.quad	.LFB1790
	.uleb128 .LFE1790-.LFB1790
	.byte	0x7
	.quad	.LFB1796
	.uleb128 .LFE1796-.LFB1796
	.byte	0x7
	.quad	.LFB1793
	.uleb128 .LFE1793-.LFB1793
	.byte	0x7
	.quad	.LFB1800
	.uleb128 .LFE1800-.LFB1800
	.byte	0x7
	.quad	.LFB1804
	.uleb128 .LFE1804-.LFB1804
	.byte	0x7
	.quad	.LFB1805
	.uleb128 .LFE1805-.LFB1805
	.byte	0x7
	.quad	.LFB1797
	.uleb128 .LFE1797-.LFB1797
	.byte	0x7
	.quad	.LFB1807
	.uleb128 .LFE1807-.LFB1807
	.byte	0x7
	.quad	.LFB1810
	.uleb128 .LFE1810-.LFB1810
	.byte	0x7
	.quad	.LFB1814
	.uleb128 .LFE1814-.LFB1814
	.byte	0x7
	.quad	.LFB1817
	.uleb128 .LFE1817-.LFB1817
	.byte	0x7
	.quad	.LFB1811
	.uleb128 .LFE1811-.LFB1811
	.byte	0x7
	.quad	.LFB1818
	.uleb128 .LFE1818-.LFB1818
	.byte	0x7
	.quad	.LFB1819
	.uleb128 .LFE1819-.LFB1819
	.byte	0x7
	.quad	.LFB1820
	.uleb128 .LFE1820-.LFB1820
	.byte	0
.Ldebug_ranges3:
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
.LASF51:
	.ascii "capacity\0"
.LASF71:
	.ascii "_S_check_init_len\0"
.LASF29:
	.ascii "_Tp_alloc_type\0"
.LASF64:
	.ascii "_M_fill_insert\0"
.LASF57:
	.ascii "push_back\0"
.LASF76:
	.ascii "__type_identity_t\0"
.LASF80:
	.ascii "initializer_list\0"
.LASF94:
	.ascii "Monster\0"
.LASF2:
	.ascii "operator()\0"
.LASF41:
	.ascii "vector\0"
.LASF61:
	.ascii "_M_fill_initialize\0"
.LASF15:
	.ascii "pointer\0"
.LASF72:
	.ascii "_S_max_size\0"
.LASF81:
	.ascii "_UninitDestroyGuard\0"
.LASF17:
	.ascii "size_type\0"
.LASF54:
	.ascii "const_reference\0"
.LASF88:
	.ascii "_S_always_equal\0"
.LASF84:
	.ascii "_S_on_swap\0"
.LASF82:
	.ascii "_Args\0"
.LASF60:
	.ascii "erase\0"
.LASF86:
	.ascii "_S_propagate_on_move_assign\0"
.LASF34:
	.ascii "_M_allocate\0"
.LASF25:
	.ascii "_M_end_of_storage\0"
.LASF79:
	.ascii "_S_use_relocate\0"
.LASF58:
	.ascii "pop_back\0"
.LASF99:
	.ascii "this\0"
.LASF36:
	.ascii "_M_create_storage\0"
.LASF38:
	.ascii "_S_nothrow_relocate\0"
.LASF75:
	.ascii "_M_move_assign\0"
.LASF45:
	.ascii "const_iterator\0"
.LASF35:
	.ascii "_M_deallocate\0"
.LASF89:
	.ascii "_S_nothrow_move\0"
.LASF95:
	.ascii "GameObject\0"
.LASF7:
	.ascii "_Size\0"
.LASF4:
	.ascii "__detail\0"
.LASF28:
	.ascii "_Vector_impl\0"
.LASF77:
	.ascii "difference_type\0"
.LASF68:
	.ascii "_M_insert_rval\0"
.LASF59:
	.ascii "insert\0"
.LASF96:
	.ascii "operator delete\0"
.LASF44:
	.ascii "begin\0"
.LASF66:
	.ascii "_M_default_append\0"
.LASF23:
	.ascii "_M_start\0"
.LASF26:
	.ascii "_M_copy_data\0"
.LASF33:
	.ascii "~_Vector_base\0"
.LASF30:
	.ascii "_M_get_Tp_allocator\0"
.LASF42:
	.ascii "assign\0"
.LASF10:
	.ascii "_M_max_size\0"
.LASF5:
	.ascii "__bool_constant\0"
.LASF73:
	.ascii "_M_erase_at_end\0"
.LASF6:
	.ascii "_ForwardIterator\0"
.LASF46:
	.ascii "reverse_iterator\0"
.LASF9:
	.ascii "deallocate\0"
.LASF8:
	.ascii "__new_allocator\0"
.LASF85:
	.ascii "_S_propagate_on_copy_assign\0"
.LASF52:
	.ascii "reference\0"
.LASF100:
	.ascii "__first\0"
.LASF63:
	.ascii "_M_fill_assign\0"
.LASF91:
	.ascii "operator++\0"
.LASF22:
	.ascii "_Vector_impl_data\0"
.LASF90:
	.ascii "__normal_iterator\0"
.LASF78:
	.ascii "_Iterator\0"
.LASF65:
	.ascii "_M_fill_append\0"
.LASF62:
	.ascii "_M_default_initialize\0"
.LASF70:
	.ascii "_M_check_len\0"
.LASF31:
	.ascii "get_allocator\0"
.LASF43:
	.ascii "iterator\0"
.LASF48:
	.ascii "const_reverse_iterator\0"
.LASF98:
	.ascii "__location\0"
.LASF27:
	.ascii "_M_swap_data\0"
.LASF13:
	.ascii "~allocator\0"
.LASF83:
	.ascii "_S_select_on_copy\0"
.LASF50:
	.ascii "shrink_to_fit\0"
.LASF32:
	.ascii "_Vector_base\0"
.LASF56:
	.ascii "front\0"
.LASF12:
	.ascii "operator=\0"
.LASF20:
	.ascii "select_on_container_copy_construction\0"
.LASF39:
	.ascii "_S_do_relocate\0"
.LASF55:
	.ascii "_M_range_check\0"
.LASF47:
	.ascii "rbegin\0"
.LASF92:
	.ascii "operator--\0"
.LASF40:
	.ascii "_S_relocate\0"
.LASF21:
	.ascii "rebind_alloc\0"
.LASF11:
	.ascii "allocator\0"
.LASF24:
	.ascii "_M_finish\0"
.LASF74:
	.ascii "_M_erase\0"
.LASF18:
	.ascii "const_void_pointer\0"
.LASF93:
	.ascii "_Container\0"
.LASF16:
	.ascii "allocator_type\0"
.LASF19:
	.ascii "max_size\0"
.LASF53:
	.ascii "operator[]\0"
.LASF87:
	.ascii "_S_propagate_on_swap\0"
.LASF69:
	.ascii "_M_emplace_aux\0"
.LASF49:
	.ascii "resize\0"
.LASF97:
	.ascii "operator new\0"
.LASF37:
	.ascii "_Alloc\0"
.LASF3:
	.ascii "value_type\0"
.LASF67:
	.ascii "_M_shrink_to_fit\0"
.LASF14:
	.ascii "allocate\0"
	.section	.debug_line_str,"dr"
.LASF1:
	.ascii "C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible\0"
.LASF0:
	.ascii "Examples\\_ch142_antipattern.cpp\0"
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZSt21__glibcxx_assert_failPKciS0_S0_;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	_ZSt28__throw_bad_array_new_lengthv;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	__cxa_pure_virtual;	.scl	2;	.type	32;	.endef
