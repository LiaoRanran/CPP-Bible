	.file	"_ch142_aos.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch142_aos.cpp"
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
	.section	.text$_ZSt17__size_to_integery,"x"
	.linkonce discard
	.globl	_ZSt17__size_to_integery
	.def	_ZSt17__size_to_integery;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt17__size_to_integery
_ZSt17__size_to_integery:
.LFB564:
	.file 3 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_algobase.h"
	.loc 3 1028 45
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
	.loc 3 1028 54
	mov	rax, QWORD PTR 16[rbp]
	.loc 3 1028 59
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE564:
	.seh_endproc
	.text
	.globl	_Z13integrate_aosP8Particleif
	.def	_Z13integrate_aosP8Particleif;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13integrate_aosP8Particleif
_Z13integrate_aosP8Particleif:
.LFB1719:
	.file 4 "Examples/_ch142_aos.cpp"
	.loc 4 13 50
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
	mov	DWORD PTR 24[rbp], edx
	movss	DWORD PTR 32[rbp], xmm2
.LBB105:
	.loc 4 14 14
	mov	DWORD PTR -4[rbp], 0
	.loc 4 14 5
	jmp	.L9
.L10:
	.loc 4 15 12
	mov	eax, DWORD PTR -4[rbp]
	movsxd	rdx, eax
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
	mov	rdx, rax
	mov	rax, QWORD PTR 16[rbp]
	add	rax, rdx
	.loc 4 15 14
	movss	xmm1, DWORD PTR [rax]
	.loc 4 15 21
	mov	eax, DWORD PTR -4[rbp]
	movsxd	rdx, eax
	.loc 4 15 22
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
	mov	rdx, rax
	mov	rax, QWORD PTR 16[rbp]
	add	rax, rdx
	.loc 4 15 24
	movss	xmm0, DWORD PTR 12[rax]
	.loc 4 15 27
	mulss	xmm0, DWORD PTR 32[rbp]
	.loc 4 15 12
	mov	eax, DWORD PTR -4[rbp]
	movsxd	rdx, eax
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
	mov	rdx, rax
	mov	rax, QWORD PTR 16[rbp]
	add	rax, rdx
	.loc 4 15 16
	addss	xmm0, xmm1
	movss	DWORD PTR [rax], xmm0
	.loc 4 14 5 discriminator 3
	add	DWORD PTR -4[rbp], 1
.L9:
	.loc 4 14 23 discriminator 1
	mov	eax, DWORD PTR -4[rbp]
	cmp	eax, DWORD PTR 24[rbp]
	jl	.L10
.LBE105:
	.loc 4 17 1
	nop
	nop
	add	rsp, 16
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1719:
	.seh_endproc
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1720:
	.loc 4 19 12
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
	.loc 4 19 12
	call	__main
	lea	rax, -9[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB106:
.LBB107:
.LBB108:
.LBB109:
.LBB110:
	.file 5 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/new_allocator.h"
	.loc 5 88 49
	nop
.LBE110:
.LBE109:
.LBE108:
	.file 6 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/allocator.h"
	.loc 6 168 38
	nop
.LBE107:
.LBE106:
	.loc 4 20 34 discriminator 1
	lea	rdx, -9[rbp]
	lea	rax, -48[rbp]
	mov	r8, rdx
	mov	edx, 1024
	mov	rcx, rax
	call	_ZNSt6vectorI8ParticleSaIS0_EEC1EyRKS1_
.LBB111:
.LBB112:
	.loc 6 189 39
	nop
.LBE112:
.LBE111:
	.loc 4 21 42
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZNKSt6vectorI8ParticleSaIS0_EE4sizeEv
	.loc 4 21 18 discriminator 1
	mov	ebx, eax
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZNSt6vectorI8ParticleSaIS0_EE4dataEv
	.loc 4 21 18 is_stmt 0 discriminator 2
	movss	xmm2, DWORD PTR .LC0[rip]
	mov	edx, ebx
	mov	rcx, rax
	call	_Z13integrate_aosP8Particleif
	.loc 4 22 21 is_stmt 1
	lea	rax, -48[rbp]
	mov	edx, 0
	mov	rcx, rax
	call	_ZNSt6vectorI8ParticleSaIS0_EEixEy
	.loc 4 22 23 discriminator 1
	movss	xmm0, DWORD PTR [rax]
	cvttss2si	ebx, xmm0
	.loc 4 23 1
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_ZNSt6vectorI8ParticleSaIS0_EED1Ev
	mov	eax, ebx
	add	rsp, 88
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -72
	ret
	.cfi_endproc
.LFE1720:
	.seh_endproc
	.section	.text$_ZNSt6vectorI8ParticleSaIS0_EEC1EyRKS1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI8ParticleSaIS0_EEC1EyRKS1_
	.def	_ZNSt6vectorI8ParticleSaIS0_EEC1EyRKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8ParticleSaIS0_EEC1EyRKS1_
_ZNSt6vectorI8ParticleSaIS0_EEC1EyRKS1_:
.LFB1734:
	.file 7 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_vector.h"
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
.LBB113:
	.loc 7 587 47
	mov	rbx, QWORD PTR 32[rbp]
	mov	rdx, QWORD PTR 48[rbp]
	mov	rax, QWORD PTR 40[rbp]
	mov	rcx, rax
.LEHB0:
	call	_ZNSt6vectorI8ParticleSaIS0_EE17_S_check_init_lenEyRKS1_
	.loc 7 587 47 is_stmt 0 discriminator 1
	mov	rdx, QWORD PTR 48[rbp]
	mov	r8, rdx
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EEC2EyRKS1_
.LEHE0:
	.loc 7 588 30 is_stmt 1
	mov	rdx, QWORD PTR 40[rbp]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
.LEHB1:
	call	_ZNSt6vectorI8ParticleSaIS0_EE21_M_default_initializeEy
.LEHE1:
.LBE113:
	.loc 7 588 37
	jmp	.L16
.L15:
.LBB114:
	.loc 7 588 37 is_stmt 0 discriminator 2
	mov	rbx, rax
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EED2Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
.L16:
.LBE114:
	.loc 7 588 37
	add	rsp, 40
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -24
	ret
	.cfi_endproc
.LFE1734:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1734:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1734-.LLSDACSB1734
.LLSDACSB1734:
	.uleb128 .LEHB0-.LFB1734
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB1734
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L15-.LFB1734
	.uleb128 0
	.uleb128 .LEHB2-.LFB1734
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE1734:
	.section	.text$_ZNSt6vectorI8ParticleSaIS0_EEC1EyRKS1_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt6vectorI8ParticleSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI8ParticleSaIS0_EED1Ev
	.def	_ZNSt6vectorI8ParticleSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8ParticleSaIS0_EED1Ev
_ZNSt6vectorI8ParticleSaIS0_EED1Ev:
.LFB1737:
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
.LBB115:
	.loc 7 803 28
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EE19_M_get_Tp_allocatorEv
	.loc 7 802 54
	mov	rdx, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 8[rdx]
	.loc 7 802 30
	mov	rcx, QWORD PTR 16[rbp]
	mov	rcx, QWORD PTR [rcx]
	mov	QWORD PTR -8[rbp], rcx
	mov	QWORD PTR -16[rbp], rdx
	mov	QWORD PTR -24[rbp], rax
.LBB116:
.LBB117:
	.file 8 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/alloc_traits.h"
	.loc 8 1045 20
	mov	rdx, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZSt8_DestroyIP8ParticleEvT_S2_
	.loc 8 1046 5
	nop
.LBE117:
.LBE116:
	.loc 7 805 7
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EED2Ev
.LBE115:
	nop
	add	rsp, 64
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1737:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1737:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1737-.LLSDACSB1737
.LLSDACSB1737:
.LLSDACSE1737:
	.section	.text$_ZNSt6vectorI8ParticleSaIS0_EED1Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt6vectorI8ParticleSaIS0_EE4dataEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI8ParticleSaIS0_EE4dataEv
	.def	_ZNSt6vectorI8ParticleSaIS0_EE4dataEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8ParticleSaIS0_EE4dataEv
_ZNSt6vectorI8ParticleSaIS0_EE4dataEv:
.LFB1738:
	.loc 7 1395 7
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
	.loc 7 1396 42
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR [rax]
	.loc 7 1396 27
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt6vectorI8ParticleSaIS0_EE11_M_data_ptrIS0_EEPT_S5_
	.loc 7 1396 53
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1738:
	.seh_endproc
	.section	.text$_ZNKSt6vectorI8ParticleSaIS0_EE4sizeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6vectorI8ParticleSaIS0_EE4sizeEv
	.def	_ZNKSt6vectorI8ParticleSaIS0_EE4sizeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6vectorI8ParticleSaIS0_EE4sizeEv
_ZNKSt6vectorI8ParticleSaIS0_EE4sizeEv:
.LFB1739:
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
	sar	rdx, 3
	movabs	rax, -6148914691236517205
	imul	rax, rdx
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
.LFE1739:
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "__n < this->size()\0"
	.align 8
.LC2:
	.ascii "constexpr std::vector<_Tp, _Alloc>::reference std::vector<_Tp, _Alloc>::operator[](size_type) [with _Tp = Particle; _Alloc = std::allocator<Particle>; reference = Particle&; size_type = long long unsigned int]\0"
	.align 8
.LC3:
	.ascii "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_vector.h\0"
	.section	.text$_ZNSt6vectorI8ParticleSaIS0_EEixEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI8ParticleSaIS0_EEixEy
	.def	_ZNSt6vectorI8ParticleSaIS0_EEixEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8ParticleSaIS0_EEixEy
_ZNSt6vectorI8ParticleSaIS0_EEixEy:
.LFB1740:
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
	call	_ZNKSt6vectorI8ParticleSaIS0_EE4sizeEv
	.loc 7 1263 2 is_stmt 0 discriminator 1
	cmp	QWORD PTR 24[rbp], rax
	setnb	al
	movzx	eax, al
	.loc 7 1263 2 discriminator 2
	test	eax, eax
	setne	al
	test	al, al
	je	.L24
	.loc 7 1263 2 discriminator 3
	lea	rcx, .LC1[rip]
	lea	rdx, .LC2[rip]
	lea	rax, .LC3[rip]
	mov	r9, rcx
	mov	r8, rdx
	mov	edx, 1263
	mov	rcx, rax
	call	_ZSt21__glibcxx_assert_failPKciS0_S0_
.L24:
	.loc 7 1264 25 is_stmt 1
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, QWORD PTR [rax]
	.loc 7 1264 34
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
	.loc 7 1264 39
	add	rax, rcx
	.loc 7 1265 7
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1740:
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC4:
	.ascii "cannot create std::vector larger than max_size()\0"
	.section	.text$_ZNSt6vectorI8ParticleSaIS0_EE17_S_check_init_lenEyRKS1_,"x"
	.linkonce discard
	.globl	_ZNSt6vectorI8ParticleSaIS0_EE17_S_check_init_lenEyRKS1_
	.def	_ZNSt6vectorI8ParticleSaIS0_EE17_S_check_init_lenEyRKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8ParticleSaIS0_EE17_S_check_init_lenEyRKS1_
_ZNSt6vectorI8ParticleSaIS0_EE17_S_check_init_lenEyRKS1_:
.LFB1744:
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
.LBB118:
.LBB119:
.LBB120:
.LBB121:
.LBB122:
	.loc 5 92 71
	nop
.LBE122:
.LBE121:
.LBE120:
	.loc 6 173 38
	nop
.LBE119:
.LBE118:
	.loc 7 2215 23 discriminator 1
	lea	rax, -25[rbp]
	mov	rcx, rax
	call	_ZNSt6vectorI8ParticleSaIS0_EE11_S_max_sizeERKS1_
	.loc 7 2215 10 discriminator 2
	cmp	rax, QWORD PTR 16[rbp]
	setb	al
.LBB123:
.LBB124:
	.loc 6 189 39
	nop
.LBE124:
.LBE123:
	.loc 7 2215 2 discriminator 3
	test	al, al
	je	.L27
	.loc 7 2216 24
	lea	rax, .LC4[rip]
	mov	rcx, rax
	call	_ZSt20__throw_length_errorPKc
.L27:
	.loc 7 2218 9
	mov	rax, QWORD PTR 16[rbp]
	.loc 7 2219 7
	add	rsp, 64
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1744:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implD1Ev
	.def	_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implD1Ev
_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implD1Ev:
.LFB1748:
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
.LBB125:
.LBB126:
.LBB127:
	.loc 6 189 39
	nop
.LBE127:
.LBE126:
.LBE125:
	.loc 7 139 14
	nop
	add	rsp, 16
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1748:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EEC2EyRKS1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI8ParticleSaIS0_EEC2EyRKS1_
	.def	_ZNSt12_Vector_baseI8ParticleSaIS0_EEC2EyRKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI8ParticleSaIS0_EEC2EyRKS1_
_ZNSt12_Vector_baseI8ParticleSaIS0_EEC2EyRKS1_:
.LFB1749:
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
.LBB128:
	.loc 7 340 9
	mov	rax, QWORD PTR 32[rbp]
	mov	rdx, QWORD PTR 48[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC1ERKS1_
	.loc 7 341 26
	mov	rdx, QWORD PTR 40[rbp]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
.LEHB3:
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_M_create_storageEy
.LEHE3:
.LBE128:
	.loc 7 341 33
	jmp	.L33
.L32:
.LBB129:
	.loc 7 341 33 is_stmt 0 discriminator 2
	mov	rbx, rax
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implD1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
.L33:
.LBE129:
	.loc 7 341 33
	add	rsp, 40
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -24
	ret
	.cfi_endproc
.LFE1749:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1749:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1749-.LLSDACSB1749
.LLSDACSB1749:
	.uleb128 .LEHB3-.LFB1749
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L32-.LFB1749
	.uleb128 0
	.uleb128 .LEHB4-.LFB1749
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE1749:
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EEC2EyRKS1_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EED2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI8ParticleSaIS0_EED2Ev
	.def	_ZNSt12_Vector_baseI8ParticleSaIS0_EED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI8ParticleSaIS0_EED2Ev
_ZNSt12_Vector_baseI8ParticleSaIS0_EED2Ev:
.LFB1752:
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
.LBB130:
	.loc 7 376 17
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 16[rax]
	.loc 7 376 45
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 7 376 35
	sub	rdx, rax
	sar	rdx, 3
	movabs	rax, -6148914691236517205
	imul	rax, rdx
	.loc 7 375 15
	mov	rcx, rax
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EE13_M_deallocateEPS0_y
	.loc 7 377 7
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implD1Ev
.LBE130:
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1752:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1752:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1752-.LLSDACSB1752
.LLSDACSB1752:
.LLSDACSE1752:
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EED2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt6vectorI8ParticleSaIS0_EE21_M_default_initializeEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt6vectorI8ParticleSaIS0_EE21_M_default_initializeEy
	.def	_ZNSt6vectorI8ParticleSaIS0_EE21_M_default_initializeEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8ParticleSaIS0_EE21_M_default_initializeEy
_ZNSt6vectorI8ParticleSaIS0_EE21_M_default_initializeEy:
.LFB1754:
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
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EE19_M_get_Tp_allocatorEv
	mov	rcx, rax
	.loc 7 2011 51
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 7 2011 36
	mov	rdx, QWORD PTR 24[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZSt27__uninitialized_default_n_aIP8ParticleyS0_ET_S2_T0_RSaIT1_E
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
.LFE1754:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EE19_M_get_Tp_allocatorEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI8ParticleSaIS0_EE19_M_get_Tp_allocatorEv
	.def	_ZNSt12_Vector_baseI8ParticleSaIS0_EE19_M_get_Tp_allocatorEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI8ParticleSaIS0_EE19_M_get_Tp_allocatorEv
_ZNSt12_Vector_baseI8ParticleSaIS0_EE19_M_get_Tp_allocatorEv:
.LFB1755:
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
.LFE1755:
	.seh_endproc
	.section	.text$_ZNKSt6vectorI8ParticleSaIS0_EE11_M_data_ptrIS0_EEPT_S5_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt6vectorI8ParticleSaIS0_EE11_M_data_ptrIS0_EEPT_S5_
	.def	_ZNKSt6vectorI8ParticleSaIS0_EE11_M_data_ptrIS0_EEPT_S5_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt6vectorI8ParticleSaIS0_EE11_M_data_ptrIS0_EEPT_S5_
_ZNKSt6vectorI8ParticleSaIS0_EE11_M_data_ptrIS0_EEPT_S5_:
.LFB1757:
	.loc 7 2296 2
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
	.loc 7 2297 11
	mov	rax, QWORD PTR 24[rbp]
	.loc 7 2297 18
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1757:
	.seh_endproc
	.section	.text$_ZNSt6vectorI8ParticleSaIS0_EE11_S_max_sizeERKS1_,"x"
	.linkonce discard
	.globl	_ZNSt6vectorI8ParticleSaIS0_EE11_S_max_sizeERKS1_
	.def	_ZNSt6vectorI8ParticleSaIS0_EE11_S_max_sizeERKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8ParticleSaIS0_EE11_S_max_sizeERKS1_
_ZNSt6vectorI8ParticleSaIS0_EE11_S_max_sizeERKS1_:
.LFB1758:
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
	movabs	rax, 384307168202282325
	mov	QWORD PTR -8[rbp], rax
	.loc 7 2229 15
	movabs	rax, 768614336404564650
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
.LFE1758:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC1ERKS1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC1ERKS1_
	.def	_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC1ERKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC1ERKS1_
_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC1ERKS1_:
.LFB1765:
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
.LBB131:
.LBB132:
.LBB133:
.LBB134:
.LBB135:
.LBB136:
	.loc 5 92 71
	nop
.LBE136:
.LBE135:
.LBE134:
	.loc 6 173 38
	nop
.LBE133:
.LBE132:
	.loc 7 153 22 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_dataC2Ev
.LBE131:
	.loc 7 154 4
	nop
	add	rsp, 64
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1765:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_M_create_storageEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_M_create_storageEy
	.def	_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_M_create_storageEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_M_create_storageEy
_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_M_create_storageEy:
.LFB1766:
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
	call	_ZNSt12_Vector_baseI8ParticleSaIS0_EE11_M_allocateEy
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
	mov	rcx, QWORD PTR [rax]
	.loc 7 407 59
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
	lea	rdx, [rcx+rax]
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
.LFE1766:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EE13_M_deallocateEPS0_y,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI8ParticleSaIS0_EE13_M_deallocateEPS0_y
	.def	_ZNSt12_Vector_baseI8ParticleSaIS0_EE13_M_deallocateEPS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI8ParticleSaIS0_EE13_M_deallocateEPS0_y
_ZNSt12_Vector_baseI8ParticleSaIS0_EE13_M_deallocateEPS0_y:
.LFB1767:
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
	je	.L49
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
.LBB137:
.LBB138:
.LBB139:
.LBB140:
.LBB141:
.LBB142:
	.file 9 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/x86_64-w64-mingw32/bits/c++config.h"
	.loc 9 586 49
	mov	eax, 0
.LBE142:
.LBE141:
	.loc 6 210 2 discriminator 1
	test	al, al
	je	.L47
	.loc 6 212 23
	mov	rax, QWORD PTR -40[rbp]
	mov	rcx, rax
	call	_ZdlPv
	.loc 6 213 6
	jmp	.L48
.L47:
	.loc 6 215 35
	mov	rcx, QWORD PTR -48[rbp]
	mov	rdx, QWORD PTR -40[rbp]
	mov	rax, QWORD PTR -32[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZNSt15__new_allocatorI8ParticleE10deallocateEPS0_y
.L48:
.LBE140:
.LBE139:
	.loc 8 649 35
	nop
.L49:
.LBE138:
.LBE137:
	.loc 7 397 7
	nop
	add	rsp, 80
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1767:
	.seh_endproc
	.section	.text$_ZSt27__uninitialized_default_n_aIP8ParticleyS0_ET_S2_T0_RSaIT1_E,"x"
	.linkonce discard
	.globl	_ZSt27__uninitialized_default_n_aIP8ParticleyS0_ET_S2_T0_RSaIT1_E
	.def	_ZSt27__uninitialized_default_n_aIP8ParticleyS0_ET_S2_T0_RSaIT1_E;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt27__uninitialized_default_n_aIP8ParticleyS0_ET_S2_T0_RSaIT1_E
_ZSt27__uninitialized_default_n_aIP8ParticleyS0_ET_S2_T0_RSaIT1_E:
.LFB1768:
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
	call	_ZSt25__uninitialized_default_nIP8ParticleyET_S2_T0_
	.loc 10 1029 60
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1768:
	.seh_endproc
	.section	.text$_ZSt8_DestroyIP8ParticleEvT_S2_,"x"
	.linkonce discard
	.globl	_ZSt8_DestroyIP8ParticleEvT_S2_
	.def	_ZSt8_DestroyIP8ParticleEvT_S2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt8_DestroyIP8ParticleEvT_S2_
_ZSt8_DestroyIP8ParticleEvT_S2_:
.LFB1769:
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
.LBB143:
.LBB144:
	.loc 9 586 49
	mov	eax, 0
.LBE144:
.LBE143:
	.loc 11 228 12 discriminator 1
	test	al, al
	je	.L58
	.loc 11 229 2
	jmp	.L55
.L57:
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB145:
.LBB146:
	.file 12 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/move.h"
	.loc 12 53 37
	mov	rax, QWORD PTR -8[rbp]
.LBE146:
.LBE145:
	.loc 11 230 19 discriminator 1
	mov	rcx, rax
	call	_ZSt10destroy_atI8ParticleEvPT_
	.loc 11 229 2 discriminator 2
	add	QWORD PTR 16[rbp], 24
.L55:
	.loc 11 229 17 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	cmp	rax, QWORD PTR 24[rbp]
	jne	.L57
.L58:
	.loc 11 236 5
	nop
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1769:
	.seh_endproc
	.section	.text$_ZSt3minIyERKT_S2_S2_,"x"
	.linkonce discard
	.globl	_ZSt3minIyERKT_S2_S2_
	.def	_ZSt3minIyERKT_S2_S2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt3minIyERKT_S2_S2_
_ZSt3minIyERKT_S2_S2_:
.LFB1771:
	.loc 3 234 5
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
	.loc 3 239 15
	mov	rax, QWORD PTR 24[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 3 239 7
	cmp	rdx, rax
	jnb	.L60
	.loc 3 240 9
	mov	rax, QWORD PTR 24[rbp]
	jmp	.L61
.L60:
	.loc 3 241 14
	mov	rax, QWORD PTR 16[rbp]
.L61:
	.loc 3 242 5
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1771:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_dataC2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_dataC2Ev
	.def	_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_dataC2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_dataC2Ev
_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_dataC2Ev:
.LFB1776:
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
.LBB147:
	.loc 7 106 4
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], 0
	.loc 7 106 16
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR 8[rax], 0
	.loc 7 106 29
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR 16[rax], 0
.LBE147:
	.loc 7 107 4
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1776:
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI8ParticleSaIS0_EE11_M_allocateEy,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12_Vector_baseI8ParticleSaIS0_EE11_M_allocateEy
	.def	_ZNSt12_Vector_baseI8ParticleSaIS0_EE11_M_allocateEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI8ParticleSaIS0_EE11_M_allocateEy
_ZNSt12_Vector_baseI8ParticleSaIS0_EE11_M_allocateEy:
.LFB1778:
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
	je	.L64
	.loc 7 387 34 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR 24[rbp]
	mov	QWORD PTR -16[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -24[rbp], rax
	mov	rax, QWORD PTR -16[rbp]
	mov	QWORD PTR -32[rbp], rax
.LBB148:
.LBB149:
.LBB150:
.LBB151:
.LBB152:
.LBB153:
	.loc 9 586 49
	mov	eax, 0
.LBE153:
.LBE152:
	.loc 6 196 2 discriminator 1
	test	al, al
	je	.L66
	.loc 6 198 32
	mov	rax, QWORD PTR -32[rbp]
	mov	ecx, 0
	mov	edx, 24
	mul	rdx
	jno	.L67
	mov	ecx, 1
.L67:
	.loc 6 198 32 is_stmt 0 discriminator 1
	mov	QWORD PTR -32[rbp], rax
	mov	rax, rcx
	and	eax, 1
	.loc 6 198 6 is_stmt 1 discriminator 1
	test	al, al
	je	.L69
	.loc 6 199 41
	call	_ZSt28__throw_bad_array_new_lengthv
.L69:
	.loc 6 200 45
	mov	rax, QWORD PTR -32[rbp]
	mov	rcx, rax
	call	_Znwy
	.loc 6 200 50
	jmp	.L70
.L66:
	.loc 6 203 40
	mov	rdx, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR -24[rbp]
	mov	r8d, 0
	mov	rcx, rax
	call	_ZNSt15__new_allocatorI8ParticleE8allocateEyPKv
	.loc 6 203 47
	nop
.L70:
.LBE151:
.LBE150:
	.loc 8 614 32
	nop
	jmp	.L72
.L64:
.LBE149:
.LBE148:
	.loc 7 387 58 discriminator 2
	mov	eax, 0
.L72:
	.loc 7 388 7
	add	rsp, 64
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1778:
	.seh_endproc
	.section	.text$_ZSt25__uninitialized_default_nIP8ParticleyET_S2_T0_,"x"
	.linkonce discard
	.globl	_ZSt25__uninitialized_default_nIP8ParticleyET_S2_T0_
	.def	_ZSt25__uninitialized_default_nIP8ParticleyET_S2_T0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt25__uninitialized_default_nIP8ParticleyET_S2_T0_
_ZSt25__uninitialized_default_nIP8ParticleyET_S2_T0_:
.LFB1780:
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
	je	.L75
	.loc 10 963 22
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP8ParticleyEET_S4_T0_
	.loc 10 963 35
	jmp	.L76
.L75:
	.loc 10 969 22
	mov	BYTE PTR -1[rbp], 1
	.loc 10 974 20
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt27__uninitialized_default_n_1ILb1EE18__uninit_default_nIP8ParticleyEET_S4_T0_
	.loc 10 974 33
	nop
.L76:
	.loc 10 975 5
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1780:
	.seh_endproc
	.section	.text$_ZSt10destroy_atI8ParticleEvPT_,"x"
	.linkonce discard
	.globl	_ZSt10destroy_atI8ParticleEvPT_
	.def	_ZSt10destroy_atI8ParticleEvPT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt10destroy_atI8ParticleEvPT_
_ZSt10destroy_atI8ParticleEvPT_:
.LFB1782:
	.loc 11 80 5
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
	.loc 11 89 5
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1782:
	.seh_endproc
	.section	.text$_ZNSt19_UninitDestroyGuardIP8ParticlevEC1ERS1_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt19_UninitDestroyGuardIP8ParticlevEC1ERS1_
	.def	_ZNSt19_UninitDestroyGuardIP8ParticlevEC1ERS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_UninitDestroyGuardIP8ParticlevEC1ERS1_
_ZNSt19_UninitDestroyGuardIP8ParticlevEC1ERS1_:
.LFB1788:
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
.LBB154:
	.loc 10 114 9
	mov	rax, QWORD PTR 24[rbp]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	.loc 10 114 28
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR 8[rax], rdx
.LBE154:
	.loc 10 115 9
	nop
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1788:
	.seh_endproc
	.section	.text$_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP8ParticleyEET_S4_T0_,"x"
	.linkonce discard
	.globl	_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP8ParticleyEET_S4_T0_
	.def	_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP8ParticleyEET_S4_T0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP8ParticleyEET_S4_T0_
_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP8ParticleyEET_S4_T0_:
.LFB1785:
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
	call	_ZNSt19_UninitDestroyGuardIP8ParticlevEC1ERS1_
	.loc 10 902 4
	jmp	.L80
.L82:
	.loc 10 903 21
	mov	rax, QWORD PTR 32[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB155:
.LBB156:
	.loc 12 53 37
	mov	rax, QWORD PTR -8[rbp]
.LBE156:
.LBE155:
	.loc 10 903 21 discriminator 1
	mov	rcx, rax
	call	_ZSt10_ConstructI8ParticleJEEvPT_DpOT0_
	.loc 10 902 4 discriminator 2
	sub	QWORD PTR 40[rbp], 1
	.loc 10 902 27 discriminator 2
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 24
	mov	QWORD PTR 32[rbp], rax
.L80:
	.loc 10 902 15 discriminator 1
	cmp	QWORD PTR 40[rbp], 0
	jne	.L82
	.loc 10 904 19
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZNSt19_UninitDestroyGuardIP8ParticlevE7releaseEv
	.loc 10 905 11
	mov	rbx, QWORD PTR 32[rbp]
	.loc 10 906 2
	lea	rax, -32[rbp]
	mov	rcx, rax
	call	_ZNSt19_UninitDestroyGuardIP8ParticlevED1Ev
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
.LFE1785:
	.seh_endproc
	.section	.text$_ZNSt27__uninitialized_default_n_1ILb1EE18__uninit_default_nIP8ParticleyEET_S4_T0_,"x"
	.linkonce discard
	.globl	_ZNSt27__uninitialized_default_n_1ILb1EE18__uninit_default_nIP8ParticleyEET_S4_T0_
	.def	_ZNSt27__uninitialized_default_n_1ILb1EE18__uninit_default_nIP8ParticleyEET_S4_T0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt27__uninitialized_default_n_1ILb1EE18__uninit_default_nIP8ParticleyEET_S4_T0_
_ZNSt27__uninitialized_default_n_1ILb1EE18__uninit_default_nIP8ParticleyEET_S4_T0_:
.LFB1789:
	.loc 10 915 9
	.cfi_startproc
	push	rbp
	.seh_pushreg	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.cfi_def_cfa_register 6
	add	rsp, -128
	.seh_stackalloc	128
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
.LBB157:
	.loc 10 917 4
	cmp	QWORD PTR 24[rbp], 0
	je	.L85
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -80[rbp], rax
.LBB158:
.LBB159:
.LBB160:
	.loc 12 53 37
	mov	rax, QWORD PTR -80[rbp]
.LBE160:
.LBE159:
	.loc 10 920 21
	mov	QWORD PTR -8[rbp], rax
	.loc 10 921 23
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZSt10_ConstructI8ParticleJEEvPT_DpOT0_
	.loc 10 922 8
	add	QWORD PTR 16[rbp], 24
	.loc 10 923 29
	mov	rax, QWORD PTR 24[rbp]
	lea	rdx, -1[rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -88[rbp], rax
	mov	QWORD PTR -16[rbp], rdx
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR -24[rbp], rax
.LBB161:
.LBB162:
.LBB163:
.LBB164:
	.file 13 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_iterator_base_types.h"
	.loc 13 242 65
	nop
.LBE164:
.LBE163:
	.loc 3 1178 29
	mov	rax, QWORD PTR -16[rbp]
	mov	rcx, rax
	call	_ZSt17__size_to_integery
	.loc 3 1178 29 is_stmt 0 discriminator 1
	mov	rdx, QWORD PTR -88[rbp]
	mov	QWORD PTR -32[rbp], rdx
	mov	QWORD PTR -40[rbp], rax
	mov	rax, QWORD PTR -24[rbp]
	mov	QWORD PTR -48[rbp], rax
.LBB165:
.LBB166:
	.loc 3 1143 7 is_stmt 1
	cmp	QWORD PTR -40[rbp], 0
	jne	.L88
	.loc 3 1144 9
	mov	rax, QWORD PTR -32[rbp]
	jmp	.L89
.L88:
	.loc 3 1148 38
	mov	rdx, QWORD PTR -40[rbp]
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
	mov	rdx, rax
	.loc 3 1148 20
	mov	rax, QWORD PTR -32[rbp]
	add	rdx, rax
	mov	rax, QWORD PTR -32[rbp]
	mov	QWORD PTR -56[rbp], rax
	mov	QWORD PTR -64[rbp], rdx
	mov	rax, QWORD PTR -48[rbp]
	mov	QWORD PTR -72[rbp], rax
.LBB167:
.LBB168:
	.loc 3 979 21
	mov	rcx, QWORD PTR -72[rbp]
	mov	rdx, QWORD PTR -64[rbp]
	mov	rax, QWORD PTR -56[rbp]
	mov	r8, rcx
	mov	rcx, rax
	call	_ZSt9__fill_a1IP8ParticleS0_EvT_S2_RKT0_
	.loc 3 979 49
	nop
.LBE168:
.LBE167:
	.loc 3 1149 22
	mov	rdx, QWORD PTR -40[rbp]
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
	mov	rdx, rax
	.loc 3 1149 24
	mov	rax, QWORD PTR -32[rbp]
	add	rax, rdx
.L89:
.LBE166:
.LBE165:
	.loc 3 1179 44
	nop
.LBE162:
.LBE161:
	.loc 10 923 29 discriminator 1
	mov	QWORD PTR 16[rbp], rax
.L85:
.LBE158:
.LBE157:
	.loc 10 925 11
	mov	rax, QWORD PTR 16[rbp]
	.loc 10 926 2
	sub	rsp, -128
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1789:
	.seh_endproc
	.section	.text$_ZNSt15__new_allocatorI8ParticleE10deallocateEPS0_y,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt15__new_allocatorI8ParticleE10deallocateEPS0_y
	.def	_ZNSt15__new_allocatorI8ParticleE10deallocateEPS0_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15__new_allocatorI8ParticleE10deallocateEPS0_y
_ZNSt15__new_allocatorI8ParticleE10deallocateEPS0_y:
.LFB1791:
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
	mov	rdx, QWORD PTR 32[rbp]
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
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
.LFE1791:
	.seh_endproc
	.section	.text$_ZNSt19_UninitDestroyGuardIP8ParticlevED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt19_UninitDestroyGuardIP8ParticlevED1Ev
	.def	_ZNSt19_UninitDestroyGuardIP8ParticlevED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_UninitDestroyGuardIP8ParticlevED1Ev
_ZNSt19_UninitDestroyGuardIP8ParticlevED1Ev:
.LFB1794:
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
.LBB169:
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
	je	.L96
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
	call	_ZSt8_DestroyIP8ParticleEvT_S2_
.L96:
.LBE169:
	.loc 10 122 7
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1794:
	.seh_endproc
	.section	.text$_ZSt10_ConstructI8ParticleJEEvPT_DpOT0_,"x"
	.linkonce discard
	.globl	_ZSt10_ConstructI8ParticleJEEvPT_DpOT0_
	.def	_ZSt10_ConstructI8ParticleJEEvPT_DpOT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt10_ConstructI8ParticleJEEvPT_DpOT0_
_ZSt10_ConstructI8ParticleJEEvPT_DpOT0_:
.LFB1795:
	.loc 11 123 5
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
.LBB170:
.LBB171:
	.loc 9 586 49
	mov	eax, 0
.LBE171:
.LBE170:
	.loc 11 126 7 discriminator 1
	test	al, al
	je	.L99
	.loc 11 129 21
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZSt12construct_atI8ParticleJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
	.loc 11 130 4
	jmp	.L97
.L99:
	.loc 11 133 13
	mov	rbx, QWORD PTR 32[rbp]
	.loc 11 133 7
	mov	rdx, rbx
	mov	ecx, 24
	call	_ZnwyPv
	.loc 11 133 7 is_stmt 0 discriminator 1
	pxor	xmm0, xmm0
	movss	DWORD PTR [rax], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 4[rax], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 8[rax], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 12[rax], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 16[rax], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 20[rax], xmm0
	mov	edx, 0
	test	dl, dl
	je	.L97
	.loc 11 133 7 discriminator 2
	mov	rdx, rbx
	mov	rcx, rax
	call	_ZdlPvS_
	nop
.L97:
	.loc 11 134 5 is_stmt 1
	add	rsp, 40
	pop	rbx
	.cfi_restore 3
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, -24
	ret
	.cfi_endproc
.LFE1795:
	.seh_endproc
	.section	.text$_ZNSt19_UninitDestroyGuardIP8ParticlevE7releaseEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt19_UninitDestroyGuardIP8ParticlevE7releaseEv
	.def	_ZNSt19_UninitDestroyGuardIP8ParticlevE7releaseEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt19_UninitDestroyGuardIP8ParticlevE7releaseEv
_ZNSt19_UninitDestroyGuardIP8ParticlevE7releaseEv:
.LFB1796:
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
.LFE1796:
	.seh_endproc
	.section	.text$_ZNSt15__new_allocatorI8ParticleE8allocateEyPKv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt15__new_allocatorI8ParticleE8allocateEyPKv
	.def	_ZNSt15__new_allocatorI8ParticleE8allocateEyPKv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt15__new_allocatorI8ParticleE8allocateEyPKv
_ZNSt15__new_allocatorI8ParticleE8allocateEyPKv:
.LFB1798:
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
.LBB172:
.LBB173:
	.loc 5 233 50
	movabs	rax, 384307168202282325
.LBE173:
.LBE172:
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
	je	.L104
	.loc 5 138 6
	movabs	rax, 768614336404564650
	cmp	rax, QWORD PTR 24[rbp]
	jnb	.L105
	.loc 5 139 41
	call	_ZSt28__throw_bad_array_new_lengthv
.L105:
	.loc 5 140 28
	call	_ZSt17__throw_bad_allocv
.L104:
	.loc 5 151 66
	mov	rdx, QWORD PTR 24[rbp]
	mov	rax, rdx
	add	rax, rax
	add	rax, rdx
	sal	rax, 3
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
.LFE1798:
	.seh_endproc
	.section	.text$_ZSt12construct_atI8ParticleJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_,"x"
	.linkonce discard
	.globl	_ZSt12construct_atI8ParticleJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
	.def	_ZSt12construct_atI8ParticleJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt12construct_atI8ParticleJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
_ZSt12construct_atI8ParticleJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_:
.LFB1799:
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
	mov	ecx, 24
	call	_ZnwyPv
	mov	rbx, rax
	.loc 11 110 9 is_stmt 0 discriminator 1
	pxor	xmm0, xmm0
	movss	DWORD PTR [rbx], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 4[rbx], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 8[rbx], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 12[rbx], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 16[rbx], xmm0
	pxor	xmm0, xmm0
	movss	DWORD PTR 20[rbx], xmm0
	.loc 11 110 56 is_stmt 1 discriminator 1
	mov	eax, 0
	.loc 11 110 56 is_stmt 0 discriminator 2
	test	al, al
	je	.L109
	.loc 11 110 9 is_stmt 1 discriminator 3
	mov	rdx, rsi
	mov	rcx, rbx
	call	_ZdlPvS_
.L109:
	.loc 11 110 56 discriminator 7
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
.LFE1799:
	.seh_endproc
	.weak	_ZSt12construct_atI8ParticleJEEPT_S2_DpOT0_
	.def	_ZSt12construct_atI8ParticleJEEPT_S2_DpOT0_;	.scl	2;	.type	32;	.endef
	.set	_ZSt12construct_atI8ParticleJEEPT_S2_DpOT0_,_ZSt12construct_atI8ParticleJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_
	.section	.text$_ZSt9__fill_a1IP8ParticleS0_EvT_S2_RKT0_,"x"
	.linkonce discard
	.globl	_ZSt9__fill_a1IP8ParticleS0_EvT_S2_RKT0_
	.def	_ZSt9__fill_a1IP8ParticleS0_EvT_S2_RKT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt9__fill_a1IP8ParticleS0_EvT_S2_RKT0_
_ZSt9__fill_a1IP8ParticleS0_EvT_S2_RKT0_:
.LFB1804:
	.loc 3 897 5
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
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	.loc 3 906 18
	mov	BYTE PTR -1[rbp], 0
	.loc 3 923 11
	mov	rax, QWORD PTR 32[rbp]
	mov	QWORD PTR -16[rbp], rax
	.loc 3 924 7
	jmp	.L111
.L112:
	.loc 3 925 2
	mov	rcx, QWORD PTR 16[rbp]
	mov	r8, QWORD PTR -16[rbp]
	mov	rax, QWORD PTR [r8]
	mov	rdx, QWORD PTR 8[r8]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 8[rcx], rdx
	mov	rax, QWORD PTR 16[r8]
	mov	QWORD PTR 16[rcx], rax
	.loc 3 924 7 discriminator 2
	add	QWORD PTR 16[rbp], 24
.L111:
	.loc 3 924 22 discriminator 1
	mov	rax, QWORD PTR 16[rbp]
	cmp	rax, QWORD PTR 24[rbp]
	jne	.L112
	.loc 3 926 5
	nop
	nop
	add	rsp, 16
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1804:
	.seh_endproc
	.section .rdata,"dr"
	.align 4
.LC0:
	.long	1015222895
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
	.file 23 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/initializer_list"
	.file 24 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/functexcept.h"
	.file 25 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/predefined_ops.h"
	.file 26 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/ext/alloc_traits.h"
	.file 27 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/ext/type_traits.h"
	.file 28 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/ptr_traits.h"
	.file 29 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/stddef.h"
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0x5e82
	.word	0x5
	.byte	0x1
	.byte	0x8
	.secrel32	.Ldebug_abbrev0
	.uleb128 0x5d
	.ascii "GNU C++23 15.3.0 -masm=intel -mtune=generic -march=x86-64 -g -O0 -std=c++23\0"
	.byte	0x21
	.byte	0x4
	.long	0x3163e
	.secrel32	.LASF0
	.secrel32	.LASF1
	.secrel32	.LLRL0
	.quad	0
	.secrel32	.Ldebug_line0
	.uleb128 0x3f
	.ascii "std\0"
	.byte	0x9
	.word	0x150
	.byte	0xb
	.long	0x40d6
	.uleb128 0x11
	.ascii "integral_constant<bool, true>\0"
	.byte	0x1
	.byte	0x1
	.byte	0x5d
	.byte	0xc
	.long	0x17c
	.uleb128 0x13
	.secrel32	.LASF3
	.byte	0x1
	.byte	0x60
	.byte	0xd
	.long	0x40d6
	.uleb128 0x40
	.ascii "operator std::integral_constant<bool, true>::value_type\0"
	.byte	0x1
	.byte	0x62
	.byte	0x11
	.ascii "_ZNKSt17integral_constantIbLb1EEcvbEv\0"
	.long	0xab
	.long	0x125
	.long	0x12b
	.uleb128 0x2
	.long	0x40e3
	.byte	0
	.uleb128 0x4b
	.secrel32	.LASF2
	.byte	0x65
	.ascii "_ZNKSt17integral_constantIbLb1EEclEv\0"
	.long	0xab
	.long	0x162
	.long	0x168
	.uleb128 0x2
	.long	0x40e3
	.byte	0
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x40d6
	.uleb128 0x41
	.ascii "__v\0"
	.long	0x40d6
	.byte	0x1
	.byte	0
	.uleb128 0x5
	.long	0x84
	.uleb128 0x11
	.ascii "integral_constant<bool, false>\0"
	.byte	0x1
	.byte	0x1
	.byte	0x5d
	.byte	0xc
	.long	0x27b
	.uleb128 0x13
	.secrel32	.LASF3
	.byte	0x1
	.byte	0x60
	.byte	0xd
	.long	0x40d6
	.uleb128 0x40
	.ascii "operator std::integral_constant<bool, false>::value_type\0"
	.byte	0x1
	.byte	0x62
	.byte	0x11
	.ascii "_ZNKSt17integral_constantIbLb0EEcvbEv\0"
	.long	0x1a9
	.long	0x224
	.long	0x22a
	.uleb128 0x2
	.long	0x40e8
	.byte	0
	.uleb128 0x4b
	.secrel32	.LASF2
	.byte	0x65
	.ascii "_ZNKSt17integral_constantIbLb0EEclEv\0"
	.long	0x1a9
	.long	0x261
	.long	0x267
	.uleb128 0x2
	.long	0x40e8
	.byte	0
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x40d6
	.uleb128 0x41
	.ascii "__v\0"
	.long	0x40d6
	.byte	0
	.byte	0
	.uleb128 0x5
	.long	0x181
	.uleb128 0x21
	.ascii "size_t\0"
	.byte	0x9
	.word	0x152
	.byte	0x1a
	.long	0x40ed
	.uleb128 0x5
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
	.uleb128 0x3f
	.ascii "ranges\0"
	.byte	0xe
	.word	0x113
	.byte	0xd
	.long	0x321
	.uleb128 0x22
	.ascii "__swap\0"
	.byte	0xf
	.byte	0xbf
	.byte	0xf
	.uleb128 0x5e
	.ascii "_Cpo\0"
	.byte	0xf
	.byte	0xfc
	.byte	0x16
	.uleb128 0x22
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
	.uleb128 0x5f
	.secrel32	.LASF4
	.byte	0xe
	.word	0x113
	.byte	0x15
	.byte	0
	.uleb128 0x22
	.ascii "__cmp_cat\0"
	.byte	0x11
	.byte	0x34
	.byte	0xd
	.uleb128 0x60
	.secrel32	.LASF4
	.byte	0x1
	.byte	0xad
	.byte	0xd
	.uleb128 0x31
	.ascii "__compare\0"
	.byte	0x11
	.word	0x23e
	.byte	0xd
	.uleb128 0x61
	.ascii "_Cpo\0"
	.byte	0x11
	.word	0x4ab
	.byte	0x14
	.uleb128 0x62
	.ascii "input_iterator_tag\0"
	.byte	0x1
	.byte	0xd
	.byte	0x5f
	.byte	0xa
	.uleb128 0x11
	.ascii "forward_iterator_tag\0"
	.byte	0x1
	.byte	0xd
	.byte	0x65
	.byte	0xa
	.long	0x38c
	.uleb128 0x2a
	.long	0x350
	.byte	0
	.uleb128 0x11
	.ascii "bidirectional_iterator_tag\0"
	.byte	0x1
	.byte	0xd
	.byte	0x69
	.byte	0xa
	.long	0x3b6
	.uleb128 0x2a
	.long	0x368
	.byte	0
	.uleb128 0x11
	.ascii "random_access_iterator_tag\0"
	.byte	0x1
	.byte	0xd
	.byte	0x6d
	.byte	0xa
	.long	0x3e0
	.uleb128 0x2a
	.long	0x38c
	.byte	0
	.uleb128 0x63
	.ascii "align_val_t\0"
	.byte	0x7
	.byte	0x8
	.long	0x40ed
	.byte	0x2
	.byte	0x64
	.byte	0xe
	.uleb128 0x22
	.ascii "__debug\0"
	.byte	0x12
	.byte	0x32
	.byte	0xd
	.uleb128 0x21
	.ascii "ptrdiff_t\0"
	.byte	0x9
	.word	0x153
	.byte	0x1c
	.long	0x4187
	.uleb128 0x23
	.ascii "true_type\0"
	.byte	0x1
	.byte	0x75
	.byte	0x9
	.long	0x427
	.uleb128 0x13
	.secrel32	.LASF5
	.byte	0x1
	.byte	0x71
	.byte	0xb
	.long	0x84
	.uleb128 0x23
	.ascii "false_type\0"
	.byte	0x1
	.byte	0x78
	.byte	0x9
	.long	0x446
	.uleb128 0x13
	.secrel32	.LASF5
	.byte	0x1
	.byte	0x71
	.byte	0xb
	.long	0x181
	.uleb128 0x36
	.ascii "__uninitialized_default_n_1<true>\0"
	.byte	0xa
	.word	0x38e
	.long	0x508
	.uleb128 0x18
	.secrel32	.LASF9
	.byte	0xa
	.word	0x393
	.byte	0x9
	.ascii "_ZNSt27__uninitialized_default_n_1ILb1EE18__uninit_default_nIP8ParticleyEET_S4_T0_\0"
	.long	0x481e
	.long	0x4fd
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x40ed
	.byte	0
	.uleb128 0x4c
	.secrel32	.LASF8
	.long	0x40d6
	.byte	0x1
	.byte	0
	.uleb128 0x36
	.ascii "__uninitialized_default_n_1<false>\0"
	.byte	0xa
	.word	0x37e
	.long	0x5bf
	.uleb128 0x18
	.secrel32	.LASF9
	.byte	0xa
	.word	0x383
	.byte	0x9
	.ascii "_ZNSt27__uninitialized_default_n_1ILb0EE18__uninit_default_nIP8ParticleyEET_S4_T0_\0"
	.long	0x481e
	.long	0x5b4
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x40ed
	.byte	0
	.uleb128 0x4c
	.secrel32	.LASF8
	.long	0x40d6
	.byte	0
	.byte	0
	.uleb128 0x22
	.ascii "numbers\0"
	.byte	0x13
	.byte	0x38
	.byte	0xb
	.uleb128 0x32
	.byte	0x15
	.byte	0x42
	.byte	0xb
	.long	0x4797
	.uleb128 0x22
	.ascii "pmr\0"
	.byte	0x14
	.byte	0x37
	.byte	0xb
	.uleb128 0x42
	.ascii "__new_allocator<Particle>\0"
	.byte	0x1
	.byte	0x5
	.byte	0x3f
	.long	0x7dd
	.uleb128 0x24
	.secrel32	.LASF10
	.byte	0x5
	.byte	0x58
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI8ParticleEC4Ev\0"
	.byte	0x1
	.long	0x634
	.long	0x63a
	.uleb128 0x2
	.long	0x480a
	.byte	0
	.uleb128 0x24
	.secrel32	.LASF10
	.byte	0x5
	.byte	0x5c
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI8ParticleEC4ERKS1_\0"
	.byte	0x1
	.long	0x675
	.long	0x680
	.uleb128 0x2
	.long	0x480a
	.uleb128 0x1
	.long	0x4814
	.byte	0
	.uleb128 0x4d
	.secrel32	.LASF13
	.byte	0x5
	.byte	0x64
	.byte	0x18
	.ascii "_ZNSt15__new_allocatorI8ParticleEaSERKS1_\0"
	.long	0x4819
	.long	0x6be
	.long	0x6c9
	.uleb128 0x2
	.long	0x480a
	.uleb128 0x1
	.long	0x4814
	.byte	0
	.uleb128 0x2b
	.secrel32	.LASF14
	.byte	0x5
	.byte	0x7e
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI8ParticleE8allocateEyPKv\0"
	.long	0x481e
	.byte	0x1
	.long	0x70e
	.long	0x71e
	.uleb128 0x2
	.long	0x480a
	.uleb128 0x1
	.long	0x71e
	.uleb128 0x1
	.long	0x472e
	.byte	0
	.uleb128 0x37
	.secrel32	.LASF17
	.byte	0x5
	.byte	0x43
	.byte	0x1f
	.long	0x280
	.uleb128 0x24
	.secrel32	.LASF11
	.byte	0x5
	.byte	0x9c
	.byte	0x7
	.ascii "_ZNSt15__new_allocatorI8ParticleE10deallocateEPS0_y\0"
	.byte	0x1
	.long	0x76f
	.long	0x77f
	.uleb128 0x2
	.long	0x480a
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x71e
	.byte	0
	.uleb128 0x40
	.ascii "_M_max_size\0"
	.byte	0x5
	.byte	0xe6
	.byte	0x7
	.ascii "_ZNKSt15__new_allocatorI8ParticleE11_M_max_sizeEv\0"
	.long	0x71e
	.long	0x7cd
	.long	0x7d3
	.uleb128 0x2
	.long	0x4828
	.byte	0
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.byte	0
	.uleb128 0x5
	.long	0x5db
	.uleb128 0x42
	.ascii "allocator<Particle>\0"
	.byte	0x1
	.byte	0x6
	.byte	0x85
	.long	0x94b
	.uleb128 0x4e
	.long	0x5db
	.byte	0x1
	.uleb128 0x24
	.secrel32	.LASF12
	.byte	0x6
	.byte	0xa8
	.byte	0x7
	.ascii "_ZNSaI8ParticleEC4Ev\0"
	.byte	0x1
	.long	0x82a
	.long	0x830
	.uleb128 0x2
	.long	0x4832
	.byte	0
	.uleb128 0x24
	.secrel32	.LASF12
	.byte	0x6
	.byte	0xac
	.byte	0x7
	.ascii "_ZNSaI8ParticleEC4ERKS0_\0"
	.byte	0x1
	.long	0x85a
	.long	0x865
	.uleb128 0x2
	.long	0x4832
	.uleb128 0x1
	.long	0x483c
	.byte	0
	.uleb128 0x4d
	.secrel32	.LASF13
	.byte	0x6
	.byte	0xb1
	.byte	0x12
	.ascii "_ZNSaI8ParticleEaSERKS0_\0"
	.long	0x4841
	.long	0x892
	.long	0x89d
	.uleb128 0x2
	.long	0x4832
	.uleb128 0x1
	.long	0x483c
	.byte	0
	.uleb128 0x4f
	.ascii "~allocator\0"
	.byte	0x6
	.byte	0xbd
	.byte	0x7
	.ascii "_ZNSaI8ParticleED4Ev\0"
	.long	0x8c9
	.long	0x8cf
	.uleb128 0x2
	.long	0x4832
	.byte	0
	.uleb128 0x2b
	.secrel32	.LASF14
	.byte	0x6
	.byte	0xc2
	.byte	0x7
	.ascii "_ZNSaI8ParticleE8allocateEy\0"
	.long	0x481e
	.byte	0x1
	.long	0x900
	.long	0x90b
	.uleb128 0x2
	.long	0x4832
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x64
	.secrel32	.LASF11
	.byte	0x6
	.byte	0xd0
	.byte	0x7
	.ascii "_ZNSaI8ParticleE10deallocateEPS_y\0"
	.byte	0x1
	.long	0x93a
	.uleb128 0x2
	.long	0x4832
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x280
	.byte	0
	.byte	0
	.uleb128 0x5
	.long	0x7e2
	.uleb128 0x36
	.ascii "allocator_traits<std::allocator<Particle> >\0"
	.byte	0x8
	.word	0x230
	.long	0xbd0
	.uleb128 0x2c
	.secrel32	.LASF15
	.byte	0x8
	.word	0x239
	.byte	0xd
	.long	0x481e
	.uleb128 0x18
	.secrel32	.LASF14
	.byte	0x8
	.word	0x265
	.byte	0x7
	.ascii "_ZNSt16allocator_traitsISaI8ParticleEE8allocateERS1_y\0"
	.long	0x984
	.long	0x9e3
	.uleb128 0x1
	.long	0x4846
	.uleb128 0x1
	.long	0x9f5
	.byte	0
	.uleb128 0x2c
	.secrel32	.LASF16
	.byte	0x8
	.word	0x233
	.byte	0xd
	.long	0x7e2
	.uleb128 0x5
	.long	0x9e3
	.uleb128 0x2c
	.secrel32	.LASF17
	.byte	0x8
	.word	0x248
	.byte	0xd
	.long	0x280
	.uleb128 0x18
	.secrel32	.LASF14
	.byte	0x8
	.word	0x274
	.byte	0x7
	.ascii "_ZNSt16allocator_traitsISaI8ParticleEE8allocateERS1_yPKv\0"
	.long	0x984
	.long	0xa5c
	.uleb128 0x1
	.long	0x4846
	.uleb128 0x1
	.long	0x9f5
	.uleb128 0x1
	.long	0xa5c
	.byte	0
	.uleb128 0x21
	.ascii "const_void_pointer\0"
	.byte	0x8
	.word	0x242
	.byte	0xd
	.long	0x472e
	.uleb128 0x65
	.secrel32	.LASF11
	.byte	0x8
	.word	0x288
	.byte	0x7
	.ascii "_ZNSt16allocator_traitsISaI8ParticleEE10deallocateERS1_PS0_y\0"
	.long	0xad2
	.uleb128 0x1
	.long	0x4846
	.uleb128 0x1
	.long	0x984
	.uleb128 0x1
	.long	0x9f5
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF18
	.byte	0x8
	.word	0x2c5
	.byte	0x7
	.ascii "_ZNSt16allocator_traitsISaI8ParticleEE8max_sizeERKS1_\0"
	.long	0x9f5
	.long	0xb1f
	.uleb128 0x1
	.long	0x484b
	.byte	0
	.uleb128 0x25
	.ascii "select_on_container_copy_construction\0"
	.byte	0x8
	.word	0x2d5
	.byte	0x7
	.ascii "_ZNSt16allocator_traitsISaI8ParticleEE37select_on_container_copy_constructionERKS1_\0"
	.long	0x9e3
	.long	0xbac
	.uleb128 0x1
	.long	0x484b
	.byte	0
	.uleb128 0x2c
	.secrel32	.LASF3
	.byte	0x8
	.word	0x236
	.byte	0xd
	.long	0x47ad
	.uleb128 0x21
	.ascii "rebind_alloc\0"
	.byte	0x8
	.word	0x257
	.byte	0x8
	.long	0x7e2
	.byte	0
	.uleb128 0x11
	.ascii "_Vector_base<Particle, std::allocator<Particle> >\0"
	.byte	0x18
	.byte	0x7
	.byte	0x5b
	.byte	0xc
	.long	0x1573
	.uleb128 0x50
	.secrel32	.LASF19
	.byte	0x62
	.long	0xde1
	.uleb128 0x10
	.ascii "_M_start\0"
	.byte	0x7
	.byte	0x64
	.byte	0xa
	.long	0xde6
	.byte	0
	.uleb128 0x10
	.ascii "_M_finish\0"
	.byte	0x7
	.byte	0x65
	.byte	0xa
	.long	0xde6
	.byte	0x8
	.uleb128 0x10
	.ascii "_M_end_of_storage\0"
	.byte	0x7
	.byte	0x66
	.byte	0xa
	.long	0xde6
	.byte	0x10
	.uleb128 0x1b
	.secrel32	.LASF19
	.byte	0x7
	.byte	0x69
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_dataC4Ev\0"
	.long	0xca2
	.long	0xca8
	.uleb128 0x2
	.long	0x485f
	.byte	0
	.uleb128 0x1b
	.secrel32	.LASF19
	.byte	0x7
	.byte	0x6f
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_dataC4EOS3_\0"
	.long	0xcf8
	.long	0xd03
	.uleb128 0x2
	.long	0x485f
	.uleb128 0x1
	.long	0x4869
	.byte	0
	.uleb128 0x43
	.ascii "_M_copy_data\0"
	.byte	0x7
	.byte	0x77
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_data12_M_copy_dataERKS3_\0"
	.long	0xd69
	.long	0xd74
	.uleb128 0x2
	.long	0x485f
	.uleb128 0x1
	.long	0x486e
	.byte	0
	.uleb128 0x66
	.ascii "_M_swap_data\0"
	.byte	0x7
	.byte	0x80
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_data12_M_swap_dataERS3_\0"
	.long	0xdd5
	.uleb128 0x2
	.long	0x485f
	.uleb128 0x1
	.long	0x4873
	.byte	0
	.byte	0
	.uleb128 0x5
	.long	0xc0b
	.uleb128 0x13
	.secrel32	.LASF15
	.byte	0x7
	.byte	0x60
	.byte	0x9
	.long	0x451b
	.uleb128 0x50
	.secrel32	.LASF20
	.byte	0x8b
	.long	0x106a
	.uleb128 0x2a
	.long	0x7e2
	.uleb128 0x2a
	.long	0xc0b
	.uleb128 0x1b
	.secrel32	.LASF20
	.byte	0x7
	.byte	0x8f
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC4EvQ26is_default_constructible_vIN9__gnu_cxx14__alloc_traitsIT0_NS6_10value_typeEE6rebindIT_E5otherEE\0"
	.long	0xeb0
	.long	0xeb6
	.uleb128 0x2
	.long	0x4878
	.byte	0
	.uleb128 0x1b
	.secrel32	.LASF20
	.byte	0x7
	.byte	0x98
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC4ERKS1_\0"
	.long	0xf02
	.long	0xf0d
	.uleb128 0x2
	.long	0x4878
	.uleb128 0x1
	.long	0x4882
	.byte	0
	.uleb128 0x1b
	.secrel32	.LASF20
	.byte	0x7
	.byte	0xa0
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC4EOS3_\0"
	.long	0xf58
	.long	0xf63
	.uleb128 0x2
	.long	0x4878
	.uleb128 0x1
	.long	0x4887
	.byte	0
	.uleb128 0x1b
	.secrel32	.LASF20
	.byte	0x7
	.byte	0xa5
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC4EOS1_\0"
	.long	0xfae
	.long	0xfb9
	.uleb128 0x2
	.long	0x4878
	.uleb128 0x1
	.long	0x488c
	.byte	0
	.uleb128 0x1b
	.secrel32	.LASF20
	.byte	0x7
	.byte	0xaa
	.byte	0x2
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC4EOS1_OS3_\0"
	.long	0x1008
	.long	0x1018
	.uleb128 0x2
	.long	0x4878
	.uleb128 0x1
	.long	0x488c
	.uleb128 0x1
	.long	0x4887
	.byte	0
	.uleb128 0x67
	.ascii "~_Vector_impl\0"
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implD4Ev\0"
	.long	0x1063
	.uleb128 0x2
	.long	0x4878
	.byte	0
	.byte	0
	.uleb128 0x13
	.secrel32	.LASF21
	.byte	0x7
	.byte	0x5e
	.byte	0x15
	.long	0x4559
	.uleb128 0x5
	.long	0x106a
	.uleb128 0x51
	.secrel32	.LASF22
	.word	0x133
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE19_M_get_Tp_allocatorEv\0"
	.long	0x4891
	.long	0x10cb
	.long	0x10d1
	.uleb128 0x2
	.long	0x4896
	.byte	0
	.uleb128 0x51
	.secrel32	.LASF22
	.word	0x138
	.ascii "_ZNKSt12_Vector_baseI8ParticleSaIS0_EE19_M_get_Tp_allocatorEv\0"
	.long	0x4882
	.long	0x1122
	.long	0x1128
	.uleb128 0x2
	.long	0x48a0
	.byte	0
	.uleb128 0x2c
	.secrel32	.LASF16
	.byte	0x7
	.word	0x12f
	.byte	0x16
	.long	0x7e2
	.uleb128 0x5
	.long	0x1128
	.uleb128 0x44
	.ascii "get_allocator\0"
	.word	0x13d
	.byte	0x7
	.ascii "_ZNKSt12_Vector_baseI8ParticleSaIS0_EE13get_allocatorEv\0"
	.long	0x1128
	.long	0x1190
	.long	0x1196
	.uleb128 0x2
	.long	0x48a0
	.byte	0
	.uleb128 0x52
	.secrel32	.LASF23
	.word	0x141
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EEC4Ev\0"
	.long	0x11cf
	.long	0x11d5
	.uleb128 0x2
	.long	0x4896
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF23
	.word	0x147
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EEC4ERKS1_\0"
	.long	0x1212
	.long	0x121d
	.uleb128 0x2
	.long	0x4896
	.uleb128 0x1
	.long	0x48a5
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF23
	.word	0x14d
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EEC4Ey\0"
	.long	0x1256
	.long	0x1261
	.uleb128 0x2
	.long	0x4896
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF23
	.word	0x153
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EEC4EyRKS1_\0"
	.long	0x129f
	.long	0x12af
	.uleb128 0x2
	.long	0x4896
	.uleb128 0x1
	.long	0x280
	.uleb128 0x1
	.long	0x48a5
	.byte	0
	.uleb128 0x52
	.secrel32	.LASF23
	.word	0x158
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EEC4EOS2_\0"
	.long	0x12eb
	.long	0x12f6
	.uleb128 0x2
	.long	0x4896
	.uleb128 0x1
	.long	0x48aa
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF23
	.word	0x15d
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EEC4EOS1_\0"
	.long	0x1332
	.long	0x133d
	.uleb128 0x2
	.long	0x4896
	.uleb128 0x1
	.long	0x488c
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF23
	.word	0x161
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EEC4EOS2_RKS1_\0"
	.long	0x137e
	.long	0x138e
	.uleb128 0x2
	.long	0x4896
	.uleb128 0x1
	.long	0x48aa
	.uleb128 0x1
	.long	0x48a5
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF23
	.word	0x16f
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EEC4ERKS1_OS2_\0"
	.long	0x13cf
	.long	0x13df
	.uleb128 0x2
	.long	0x4896
	.uleb128 0x1
	.long	0x48a5
	.uleb128 0x1
	.long	0x48aa
	.byte	0
	.uleb128 0x53
	.ascii "~_Vector_base\0"
	.word	0x175
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EED4Ev\0"
	.long	0x1422
	.long	0x1428
	.uleb128 0x2
	.long	0x4896
	.byte	0
	.uleb128 0x68
	.ascii "_M_impl\0"
	.byte	0x7
	.word	0x17c
	.byte	0x14
	.long	0xdf2
	.byte	0
	.uleb128 0x44
	.ascii "_M_allocate\0"
	.word	0x180
	.byte	0x7
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE11_M_allocateEy\0"
	.long	0xde6
	.long	0x148b
	.long	0x1496
	.uleb128 0x2
	.long	0x4896
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x53
	.ascii "_M_deallocate\0"
	.word	0x188
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE13_M_deallocateEPS0_y\0"
	.long	0x14ea
	.long	0x14fa
	.uleb128 0x2
	.long	0x4896
	.uleb128 0x1
	.long	0xde6
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0xb
	.ascii "_M_create_storage\0"
	.byte	0x7
	.word	0x193
	.byte	0x7
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_M_create_storageEy\0"
	.byte	0x2
	.long	0x1555
	.long	0x1560
	.uleb128 0x2
	.long	0x4896
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x6
	.secrel32	.LASF24
	.long	0x7e2
	.byte	0
	.uleb128 0x5
	.long	0xbd0
	.uleb128 0x36
	.ascii "remove_cv<Particle>\0"
	.byte	0x1
	.word	0x6aa
	.long	0x15a3
	.uleb128 0x21
	.ascii "type\0"
	.byte	0x1
	.word	0x6ab
	.byte	0xd
	.long	0x47ad
	.byte	0
	.uleb128 0x11
	.ascii "__type_identity<std::allocator<Particle> >\0"
	.byte	0x1
	.byte	0x1
	.byte	0xa7
	.byte	0xc
	.long	0x15f0
	.uleb128 0x23
	.ascii "type\0"
	.byte	0x1
	.byte	0xa8
	.byte	0xd
	.long	0x7e2
	.uleb128 0x4
	.ascii "_Type\0"
	.long	0x7e2
	.byte	0
	.uleb128 0x69
	.ascii "vector<Particle, std::allocator<Particle> >\0"
	.byte	0x18
	.byte	0x7
	.word	0x1ca
	.byte	0xb
	.long	0x334c
	.uleb128 0x2d
	.long	0x143a
	.uleb128 0x2d
	.long	0x1496
	.uleb128 0x2d
	.long	0x1428
	.uleb128 0x2d
	.long	0x10d1
	.uleb128 0x2d
	.long	0x107b
	.uleb128 0x2d
	.long	0x113a
	.uleb128 0x4e
	.long	0xbd0
	.byte	0x2
	.uleb128 0x18
	.secrel32	.LASF25
	.byte	0x7
	.word	0x1f4
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE19_S_nothrow_relocateESt17integral_constantIbLb1EE\0"
	.long	0x40d6
	.long	0x16b2
	.uleb128 0x1
	.long	0x415
	.byte	0
	.uleb128 0x18
	.secrel32	.LASF25
	.byte	0x7
	.word	0x1fd
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE19_S_nothrow_relocateESt17integral_constantIbLb0EE\0"
	.long	0x40d6
	.long	0x171a
	.uleb128 0x1
	.long	0x433
	.byte	0
	.uleb128 0x45
	.ascii "_S_use_relocate\0"
	.byte	0x7
	.word	0x201
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE15_S_use_relocateEv\0"
	.long	0x40d6
	.uleb128 0x1c
	.secrel32	.LASF15
	.word	0x1e4
	.byte	0x29
	.long	0xde6
	.uleb128 0x18
	.secrel32	.LASF26
	.byte	0x7
	.word	0x20a
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE14_S_do_relocateEPS0_S3_S3_RS1_St17integral_constantIbLb1EE\0"
	.long	0x1765
	.long	0x17f6
	.uleb128 0x1
	.long	0x1765
	.uleb128 0x1
	.long	0x1765
	.uleb128 0x1
	.long	0x1765
	.uleb128 0x1
	.long	0x48af
	.uleb128 0x1
	.long	0x415
	.byte	0
	.uleb128 0x2c
	.secrel32	.LASF21
	.byte	0x7
	.word	0x1df
	.byte	0x2f
	.long	0x106a
	.uleb128 0x5
	.long	0x17f6
	.uleb128 0x18
	.secrel32	.LASF26
	.byte	0x7
	.word	0x211
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE14_S_do_relocateEPS0_S3_S3_RS1_St17integral_constantIbLb0EE\0"
	.long	0x1765
	.long	0x188d
	.uleb128 0x1
	.long	0x1765
	.uleb128 0x1
	.long	0x1765
	.uleb128 0x1
	.long	0x1765
	.uleb128 0x1
	.long	0x48af
	.uleb128 0x1
	.long	0x433
	.byte	0
	.uleb128 0x25
	.ascii "_S_relocate\0"
	.byte	0x7
	.word	0x216
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE11_S_relocateEPS0_S3_S3_RS1_\0"
	.long	0x1765
	.long	0x18f6
	.uleb128 0x1
	.long	0x1765
	.uleb128 0x1
	.long	0x1765
	.uleb128 0x1
	.long	0x1765
	.uleb128 0x1
	.long	0x48af
	.byte	0
	.uleb128 0x54
	.secrel32	.LASF27
	.word	0x231
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4Ev\0"
	.long	0x1928
	.long	0x192e
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x55
	.secrel32	.LASF27
	.word	0x23c
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4ERKS1_\0"
	.long	0x1964
	.long	0x196f
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48be
	.byte	0
	.uleb128 0x1c
	.secrel32	.LASF16
	.word	0x1ef
	.byte	0x1a
	.long	0x7e2
	.uleb128 0x5
	.long	0x196f
	.uleb128 0x55
	.secrel32	.LASF27
	.word	0x24a
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4EyRKS1_\0"
	.long	0x19b7
	.long	0x19c7
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.uleb128 0x1
	.long	0x48be
	.byte	0
	.uleb128 0x1c
	.secrel32	.LASF17
	.word	0x1ed
	.byte	0x1a
	.long	0x280
	.uleb128 0x26
	.secrel32	.LASF27
	.word	0x257
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4EyRKS0_RKS1_\0"
	.long	0x1a0f
	.long	0x1a24
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.uleb128 0x1
	.long	0x48c3
	.uleb128 0x1
	.long	0x48be
	.byte	0
	.uleb128 0x1c
	.secrel32	.LASF3
	.word	0x1e3
	.byte	0x17
	.long	0x47ad
	.uleb128 0x5
	.long	0x1a24
	.uleb128 0x26
	.secrel32	.LASF27
	.word	0x277
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4ERKS2_\0"
	.long	0x1a6b
	.long	0x1a76
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48c8
	.byte	0
	.uleb128 0x54
	.secrel32	.LASF27
	.word	0x28a
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4EOS2_\0"
	.long	0x1aab
	.long	0x1ab6
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48cd
	.byte	0
	.uleb128 0x26
	.secrel32	.LASF27
	.word	0x28e
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4ERKS2_RKS1_\0"
	.long	0x1af1
	.long	0x1b01
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48c8
	.uleb128 0x1
	.long	0x48d2
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF27
	.word	0x299
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4EOS2_RKS1_St17integral_constantIbLb1EE\0"
	.long	0x1b57
	.long	0x1b6c
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48cd
	.uleb128 0x1
	.long	0x48be
	.uleb128 0x1
	.long	0x415
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF27
	.word	0x29e
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4EOS2_RKS1_St17integral_constantIbLb0EE\0"
	.long	0x1bc2
	.long	0x1bd7
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48cd
	.uleb128 0x1
	.long	0x48be
	.uleb128 0x1
	.long	0x433
	.byte	0
	.uleb128 0x26
	.secrel32	.LASF27
	.word	0x2b1
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4EOS2_RKS1_\0"
	.long	0x1c11
	.long	0x1c21
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48cd
	.uleb128 0x1
	.long	0x48d2
	.byte	0
	.uleb128 0x26
	.secrel32	.LASF27
	.word	0x2c4
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC4ESt16initializer_listIS0_ERKS1_\0"
	.long	0x1c70
	.long	0x1c80
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x3370
	.uleb128 0x1
	.long	0x48be
	.byte	0
	.uleb128 0xb
	.ascii "~vector\0"
	.byte	0x7
	.word	0x320
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EED4Ev\0"
	.byte	0x1
	.long	0x1cb9
	.long	0x1cbf
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x2b
	.secrel32	.LASF13
	.byte	0x16
	.byte	0xd2
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEaSERKS2_\0"
	.long	0x48d7
	.byte	0x1
	.long	0x1cfb
	.long	0x1d06
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48c8
	.byte	0
	.uleb128 0x1d
	.secrel32	.LASF13
	.word	0x341
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEaSEOS2_\0"
	.long	0x48d7
	.long	0x1d3f
	.long	0x1d4a
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48cd
	.byte	0
	.uleb128 0x1d
	.secrel32	.LASF13
	.word	0x357
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEaSESt16initializer_listIS0_E\0"
	.long	0x48d7
	.long	0x1d98
	.long	0x1da3
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x3370
	.byte	0
	.uleb128 0xb
	.ascii "assign\0"
	.byte	0x7
	.word	0x36b
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE6assignEyRKS0_\0"
	.byte	0x1
	.long	0x1de5
	.long	0x1df5
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.uleb128 0x1
	.long	0x48c3
	.byte	0
	.uleb128 0xb
	.ascii "assign\0"
	.byte	0x7
	.word	0x39a
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE6assignESt16initializer_listIS0_E\0"
	.byte	0x1
	.long	0x1e4a
	.long	0x1e55
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x3370
	.byte	0
	.uleb128 0x1c
	.secrel32	.LASF28
	.word	0x1e8
	.byte	0x3d
	.long	0x457b
	.uleb128 0x7
	.ascii "begin\0"
	.byte	0x7
	.word	0x3e6
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE5beginEv\0"
	.long	0x1e55
	.byte	0x1
	.long	0x1ea0
	.long	0x1ea6
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x1c
	.secrel32	.LASF29
	.word	0x1ea
	.byte	0x7
	.long	0x45cc
	.uleb128 0x7
	.ascii "begin\0"
	.byte	0x7
	.word	0x3f0
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE5beginEv\0"
	.long	0x1ea6
	.byte	0x1
	.long	0x1ef2
	.long	0x1ef8
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x7
	.ascii "end\0"
	.byte	0x7
	.word	0x3fa
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE3endEv\0"
	.long	0x1e55
	.byte	0x1
	.long	0x1f33
	.long	0x1f39
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x7
	.ascii "end\0"
	.byte	0x7
	.word	0x404
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE3endEv\0"
	.long	0x1ea6
	.byte	0x1
	.long	0x1f75
	.long	0x1f7b
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x56
	.ascii "reverse_iterator\0"
	.word	0x1ec
	.byte	0x30
	.long	0x353d
	.uleb128 0x7
	.ascii "rbegin\0"
	.byte	0x7
	.word	0x40e
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE6rbeginEv\0"
	.long	0x1f7b
	.byte	0x1
	.long	0x1fd5
	.long	0x1fdb
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x56
	.ascii "const_reverse_iterator\0"
	.word	0x1eb
	.byte	0x35
	.long	0x35ac
	.uleb128 0x7
	.ascii "rbegin\0"
	.byte	0x7
	.word	0x418
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE6rbeginEv\0"
	.long	0x1fdb
	.byte	0x1
	.long	0x203c
	.long	0x2042
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x7
	.ascii "rend\0"
	.byte	0x7
	.word	0x422
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE4rendEv\0"
	.long	0x1f7b
	.byte	0x1
	.long	0x207f
	.long	0x2085
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x7
	.ascii "rend\0"
	.byte	0x7
	.word	0x42c
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE4rendEv\0"
	.long	0x1fdb
	.byte	0x1
	.long	0x20c3
	.long	0x20c9
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x7
	.ascii "cbegin\0"
	.byte	0x7
	.word	0x437
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE6cbeginEv\0"
	.long	0x1ea6
	.byte	0x1
	.long	0x210b
	.long	0x2111
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x7
	.ascii "cend\0"
	.byte	0x7
	.word	0x441
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE4cendEv\0"
	.long	0x1ea6
	.byte	0x1
	.long	0x214f
	.long	0x2155
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x7
	.ascii "crbegin\0"
	.byte	0x7
	.word	0x44b
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE7crbeginEv\0"
	.long	0x1fdb
	.byte	0x1
	.long	0x2199
	.long	0x219f
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x7
	.ascii "crend\0"
	.byte	0x7
	.word	0x455
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE5crendEv\0"
	.long	0x1fdb
	.byte	0x1
	.long	0x21df
	.long	0x21e5
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x7
	.ascii "size\0"
	.byte	0x7
	.word	0x45d
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE4sizeEv\0"
	.long	0x19c7
	.byte	0x1
	.long	0x2223
	.long	0x2229
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x1d
	.secrel32	.LASF18
	.word	0x468
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE8max_sizeEv\0"
	.long	0x19c7
	.long	0x2267
	.long	0x226d
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0xb
	.ascii "resize\0"
	.byte	0x7
	.word	0x477
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE6resizeEy\0"
	.byte	0x1
	.long	0x22aa
	.long	0x22b5
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.byte	0
	.uleb128 0xb
	.ascii "resize\0"
	.byte	0x7
	.word	0x48c
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE6resizeEyRKS0_\0"
	.byte	0x1
	.long	0x22f7
	.long	0x2307
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.uleb128 0x1
	.long	0x48c3
	.byte	0
	.uleb128 0xb
	.ascii "shrink_to_fit\0"
	.byte	0x7
	.word	0x4ae
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE13shrink_to_fitEv\0"
	.byte	0x1
	.long	0x2353
	.long	0x2359
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x7
	.ascii "capacity\0"
	.byte	0x7
	.word	0x4b8
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE8capacityEv\0"
	.long	0x19c7
	.byte	0x1
	.long	0x239f
	.long	0x23a5
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x7
	.ascii "empty\0"
	.byte	0x7
	.word	0x4c7
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE5emptyEv\0"
	.long	0x40d6
	.byte	0x1
	.long	0x23e5
	.long	0x23eb
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x4f
	.ascii "reserve\0"
	.byte	0x16
	.byte	0x43
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE7reserveEy\0"
	.long	0x2428
	.long	0x2433
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.byte	0
	.uleb128 0x1c
	.secrel32	.LASF30
	.word	0x1e6
	.byte	0x32
	.long	0x4527
	.uleb128 0x1d
	.secrel32	.LASF31
	.word	0x4ed
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEixEy\0"
	.long	0x2433
	.long	0x2475
	.long	0x2480
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.byte	0
	.uleb128 0x1c
	.secrel32	.LASF32
	.word	0x1e7
	.byte	0x37
	.long	0x4533
	.uleb128 0x1d
	.secrel32	.LASF31
	.word	0x500
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EEixEy\0"
	.long	0x2480
	.long	0x24c3
	.long	0x24ce
	.uleb128 0x2
	.long	0x48dc
	.uleb128 0x1
	.long	0x19c7
	.byte	0
	.uleb128 0xb
	.ascii "_M_range_check\0"
	.byte	0x7
	.word	0x50a
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE14_M_range_checkEy\0"
	.byte	0x2
	.long	0x251d
	.long	0x2528
	.uleb128 0x2
	.long	0x48dc
	.uleb128 0x1
	.long	0x19c7
	.byte	0
	.uleb128 0x7
	.ascii "at\0"
	.byte	0x7
	.word	0x521
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE2atEy\0"
	.long	0x2433
	.byte	0x1
	.long	0x2561
	.long	0x256c
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.byte	0
	.uleb128 0x7
	.ascii "at\0"
	.byte	0x7
	.word	0x534
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE2atEy\0"
	.long	0x2480
	.byte	0x1
	.long	0x25a6
	.long	0x25b1
	.uleb128 0x2
	.long	0x48dc
	.uleb128 0x1
	.long	0x19c7
	.byte	0
	.uleb128 0x7
	.ascii "front\0"
	.byte	0x7
	.word	0x540
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE5frontEv\0"
	.long	0x2433
	.byte	0x1
	.long	0x25f0
	.long	0x25f6
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x7
	.ascii "front\0"
	.byte	0x7
	.word	0x54c
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE5frontEv\0"
	.long	0x2480
	.byte	0x1
	.long	0x2636
	.long	0x263c
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x7
	.ascii "back\0"
	.byte	0x7
	.word	0x558
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE4backEv\0"
	.long	0x2433
	.byte	0x1
	.long	0x2679
	.long	0x267f
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x7
	.ascii "back\0"
	.byte	0x7
	.word	0x564
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE4backEv\0"
	.long	0x2480
	.byte	0x1
	.long	0x26bd
	.long	0x26c3
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x7
	.ascii "data\0"
	.byte	0x7
	.word	0x573
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE4dataEv\0"
	.long	0x481e
	.byte	0x1
	.long	0x2700
	.long	0x2706
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x7
	.ascii "data\0"
	.byte	0x7
	.word	0x578
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE4dataEv\0"
	.long	0x4850
	.byte	0x1
	.long	0x2744
	.long	0x274a
	.uleb128 0x2
	.long	0x48dc
	.byte	0
	.uleb128 0x26
	.secrel32	.LASF33
	.word	0x588
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE9push_backERKS0_\0"
	.long	0x2788
	.long	0x2793
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48c3
	.byte	0
	.uleb128 0x26
	.secrel32	.LASF33
	.word	0x599
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE9push_backEOS0_\0"
	.long	0x27d0
	.long	0x27db
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48e6
	.byte	0
	.uleb128 0xb
	.ascii "pop_back\0"
	.byte	0x7
	.word	0x5b1
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE8pop_backEv\0"
	.byte	0x1
	.long	0x281c
	.long	0x2822
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x2b
	.secrel32	.LASF34
	.byte	0x16
	.byte	0x85
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EERS5_\0"
	.long	0x1e55
	.byte	0x1
	.long	0x288b
	.long	0x289b
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1ea6
	.uleb128 0x1
	.long	0x48c3
	.byte	0
	.uleb128 0x1d
	.secrel32	.LASF34
	.word	0x5f8
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEOS0_\0"
	.long	0x1e55
	.long	0x2902
	.long	0x2912
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1ea6
	.uleb128 0x1
	.long	0x48e6
	.byte	0
	.uleb128 0x1d
	.secrel32	.LASF34
	.word	0x60a
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EESt16initializer_listIS0_E\0"
	.long	0x1e55
	.long	0x298e
	.long	0x299e
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1ea6
	.uleb128 0x1
	.long	0x3370
	.byte	0
	.uleb128 0x1d
	.secrel32	.LASF34
	.word	0x624
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE6insertEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEyRS5_\0"
	.long	0x1e55
	.long	0x2a06
	.long	0x2a1b
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1ea6
	.uleb128 0x1
	.long	0x19c7
	.uleb128 0x1
	.long	0x48c3
	.byte	0
	.uleb128 0x7
	.ascii "erase\0"
	.byte	0x7
	.word	0x700
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE5eraseEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EE\0"
	.long	0x1e55
	.byte	0x1
	.long	0x2a82
	.long	0x2a8d
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1ea6
	.byte	0
	.uleb128 0x7
	.ascii "erase\0"
	.byte	0x7
	.word	0x71c
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE5eraseEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EES7_\0"
	.long	0x1e55
	.byte	0x1
	.long	0x2af7
	.long	0x2b07
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1ea6
	.uleb128 0x1
	.long	0x1ea6
	.byte	0
	.uleb128 0xb
	.ascii "swap\0"
	.byte	0x7
	.word	0x734
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE4swapERS2_\0"
	.byte	0x1
	.long	0x2b43
	.long	0x2b4e
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48d7
	.byte	0
	.uleb128 0xb
	.ascii "clear\0"
	.byte	0x7
	.word	0x747
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE5clearEv\0"
	.byte	0x1
	.long	0x2b89
	.long	0x2b8f
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0xb
	.ascii "_M_fill_initialize\0"
	.byte	0x7
	.word	0x7cd
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE18_M_fill_initializeEyRKS0_\0"
	.byte	0x2
	.long	0x2bea
	.long	0x2bfa
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.uleb128 0x1
	.long	0x48c3
	.byte	0
	.uleb128 0xb
	.ascii "_M_default_initialize\0"
	.byte	0x7
	.word	0x7d8
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE21_M_default_initializeEy\0"
	.byte	0x2
	.long	0x2c56
	.long	0x2c61
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.byte	0
	.uleb128 0xb
	.ascii "_M_fill_assign\0"
	.byte	0x16
	.word	0x10e
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE14_M_fill_assignEyRKS0_\0"
	.byte	0x2
	.long	0x2cb4
	.long	0x2cc4
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x280
	.uleb128 0x1
	.long	0x48c3
	.byte	0
	.uleb128 0xb
	.ascii "_M_fill_insert\0"
	.byte	0x16
	.word	0x28c
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS0_S2_EEyRKS0_\0"
	.byte	0x2
	.long	0x2d3f
	.long	0x2d54
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1e55
	.uleb128 0x1
	.long	0x19c7
	.uleb128 0x1
	.long	0x48c3
	.byte	0
	.uleb128 0xb
	.ascii "_M_fill_append\0"
	.byte	0x16
	.word	0x2f6
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE14_M_fill_appendEyRKS0_\0"
	.byte	0x2
	.long	0x2da7
	.long	0x2db7
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.uleb128 0x1
	.long	0x48c3
	.byte	0
	.uleb128 0xb
	.ascii "_M_default_append\0"
	.byte	0x16
	.word	0x32d
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE17_M_default_appendEy\0"
	.byte	0x2
	.long	0x2e0b
	.long	0x2e16
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x19c7
	.byte	0
	.uleb128 0x7
	.ascii "_M_shrink_to_fit\0"
	.byte	0x16
	.word	0x389
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE16_M_shrink_to_fitEv\0"
	.long	0x40d6
	.byte	0x2
	.long	0x2e6c
	.long	0x2e72
	.uleb128 0x2
	.long	0x48b4
	.byte	0
	.uleb128 0x7
	.ascii "_M_insert_rval\0"
	.byte	0x16
	.word	0x16b
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE14_M_insert_rvalEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEOS0_\0"
	.long	0x1e55
	.byte	0x2
	.long	0x2ef0
	.long	0x2f00
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1ea6
	.uleb128 0x1
	.long	0x48e6
	.byte	0
	.uleb128 0x7
	.ascii "_M_emplace_aux\0"
	.byte	0x7
	.word	0x893
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE14_M_emplace_auxEN9__gnu_cxx17__normal_iteratorIPKS0_S2_EEOS0_\0"
	.long	0x1e55
	.byte	0x2
	.long	0x2f7e
	.long	0x2f8e
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1ea6
	.uleb128 0x1
	.long	0x48e6
	.byte	0
	.uleb128 0x7
	.ascii "_M_check_len\0"
	.byte	0x7
	.word	0x89a
	.byte	0x7
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE12_M_check_lenEyPKc\0"
	.long	0x19c7
	.byte	0x2
	.long	0x2fe0
	.long	0x2ff0
	.uleb128 0x2
	.long	0x48dc
	.uleb128 0x1
	.long	0x19c7
	.uleb128 0x1
	.long	0x48eb
	.byte	0
	.uleb128 0x57
	.ascii "_S_check_init_len\0"
	.word	0x8a5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE17_S_check_init_lenEyRKS1_\0"
	.long	0x19c7
	.long	0x3051
	.uleb128 0x1
	.long	0x19c7
	.uleb128 0x1
	.long	0x48be
	.byte	0
	.uleb128 0x57
	.ascii "_S_max_size\0"
	.word	0x8ae
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE11_S_max_sizeERKS1_\0"
	.long	0x19c7
	.long	0x30a0
	.uleb128 0x1
	.long	0x48f0
	.byte	0
	.uleb128 0xb
	.ascii "_M_erase_at_end\0"
	.byte	0x7
	.word	0x8bf
	.byte	0x7
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE15_M_erase_at_endEPS0_\0"
	.byte	0x2
	.long	0x30f3
	.long	0x30fe
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1765
	.byte	0
	.uleb128 0x2b
	.secrel32	.LASF35
	.byte	0x16
	.byte	0xb5
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE8_M_eraseEN9__gnu_cxx17__normal_iteratorIPS0_S2_EE\0"
	.long	0x1e55
	.byte	0x2
	.long	0x3164
	.long	0x316f
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1e55
	.byte	0
	.uleb128 0x2b
	.secrel32	.LASF35
	.byte	0x16
	.byte	0xc3
	.byte	0x5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE8_M_eraseEN9__gnu_cxx17__normal_iteratorIPS0_S2_EES6_\0"
	.long	0x1e55
	.byte	0x2
	.long	0x31d8
	.long	0x31e8
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x1e55
	.uleb128 0x1
	.long	0x1e55
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF36
	.word	0x8d9
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE14_M_move_assignEOS2_St17integral_constantIbLb1EE\0"
	.long	0x3247
	.long	0x3257
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48cd
	.uleb128 0x1
	.long	0x415
	.byte	0
	.uleb128 0x15
	.secrel32	.LASF36
	.word	0x8e5
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EE14_M_move_assignEOS2_St17integral_constantIbLb0EE\0"
	.long	0x32b6
	.long	0x32c6
	.uleb128 0x2
	.long	0x48b4
	.uleb128 0x1
	.long	0x48cd
	.uleb128 0x1
	.long	0x433
	.byte	0
	.uleb128 0x44
	.ascii "_M_data_ptr<Particle>\0"
	.word	0x8f8
	.byte	0x2
	.ascii "_ZNKSt6vectorI8ParticleSaIS0_EE11_M_data_ptrIS0_EEPT_S5_\0"
	.long	0x481e
	.long	0x332e
	.long	0x3339
	.uleb128 0x4
	.ascii "_Up\0"
	.long	0x47ad
	.uleb128 0x2
	.long	0x48dc
	.uleb128 0x1
	.long	0x481e
	.byte	0
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x6a
	.secrel32	.LASF24
	.long	0x7e2
	.byte	0
	.uleb128 0x5
	.long	0x15f0
	.uleb128 0x23
	.ascii "__type_identity_t\0"
	.byte	0x1
	.byte	0xab
	.byte	0xb
	.long	0x15d7
	.uleb128 0x5
	.long	0x3351
	.uleb128 0x42
	.ascii "initializer_list<Particle>\0"
	.byte	0x10
	.byte	0x17
	.byte	0x2f
	.long	0x3538
	.uleb128 0x37
	.secrel32	.LASF28
	.byte	0x17
	.byte	0x36
	.byte	0x1a
	.long	0x4850
	.uleb128 0x10
	.ascii "_M_array\0"
	.byte	0x17
	.byte	0x3a
	.byte	0x12
	.long	0x3393
	.byte	0
	.uleb128 0x37
	.secrel32	.LASF17
	.byte	0x17
	.byte	0x35
	.byte	0x18
	.long	0x280
	.uleb128 0x10
	.ascii "_M_len\0"
	.byte	0x17
	.byte	0x3b
	.byte	0x13
	.long	0x33b1
	.byte	0x8
	.uleb128 0x1b
	.secrel32	.LASF37
	.byte	0x17
	.byte	0x3e
	.byte	0x11
	.ascii "_ZNSt16initializer_listI8ParticleEC4EPKS0_y\0"
	.long	0x3409
	.long	0x3419
	.uleb128 0x2
	.long	0x48f5
	.uleb128 0x1
	.long	0x3419
	.uleb128 0x1
	.long	0x33b1
	.byte	0
	.uleb128 0x37
	.secrel32	.LASF29
	.byte	0x17
	.byte	0x37
	.byte	0x1a
	.long	0x4850
	.uleb128 0x24
	.secrel32	.LASF37
	.byte	0x17
	.byte	0x42
	.byte	0x11
	.ascii "_ZNSt16initializer_listI8ParticleEC4Ev\0"
	.byte	0x1
	.long	0x345d
	.long	0x3463
	.uleb128 0x2
	.long	0x48f5
	.byte	0
	.uleb128 0x46
	.ascii "size\0"
	.byte	0x47
	.ascii "_ZNKSt16initializer_listI8ParticleE4sizeEv\0"
	.long	0x33b1
	.long	0x34a1
	.long	0x34a7
	.uleb128 0x2
	.long	0x48fa
	.byte	0
	.uleb128 0x46
	.ascii "begin\0"
	.byte	0x4b
	.ascii "_ZNKSt16initializer_listI8ParticleE5beginEv\0"
	.long	0x3419
	.long	0x34e7
	.long	0x34ed
	.uleb128 0x2
	.long	0x48fa
	.byte	0
	.uleb128 0x46
	.ascii "end\0"
	.byte	0x4f
	.ascii "_ZNKSt16initializer_listI8ParticleE3endEv\0"
	.long	0x3419
	.long	0x3529
	.long	0x352f
	.uleb128 0x2
	.long	0x48fa
	.byte	0
	.uleb128 0x4
	.ascii "_E\0"
	.long	0x47ad
	.byte	0
	.uleb128 0x5
	.long	0x3370
	.uleb128 0x38
	.ascii "reverse_iterator<__gnu_cxx::__normal_iterator<Particle*, std::vector<Particle, std::allocator<Particle> > > >\0"
	.uleb128 0x38
	.ascii "reverse_iterator<__gnu_cxx::__normal_iterator<const Particle*, std::vector<Particle, std::allocator<Particle> > > >\0"
	.uleb128 0x11
	.ascii "iterator_traits<Particle*>\0"
	.byte	0x1
	.byte	0xd
	.byte	0xc8
	.byte	0xc
	.long	0x367b
	.uleb128 0x23
	.ascii "iterator_category\0"
	.byte	0xd
	.byte	0xcb
	.byte	0xd
	.long	0x3b6
	.uleb128 0x13
	.secrel32	.LASF3
	.byte	0xd
	.byte	0xcc
	.byte	0xd
	.long	0x367b
	.uleb128 0x4
	.ascii "_Iterator\0"
	.long	0x481e
	.byte	0
	.uleb128 0x21
	.ascii "remove_cv_t\0"
	.byte	0x1
	.word	0x6d8
	.byte	0xb
	.long	0x1594
	.uleb128 0x11
	.ascii "_UninitDestroyGuard<Particle*, void>\0"
	.byte	0x10
	.byte	0xa
	.byte	0x6d
	.byte	0xc
	.long	0x3824
	.uleb128 0x6b
	.secrel32	.LASF38
	.byte	0xa
	.byte	0x71
	.byte	0x7
	.ascii "_ZNSt19_UninitDestroyGuardIP8ParticlevEC4ERS1_\0"
	.long	0x36fd
	.long	0x3708
	.uleb128 0x2
	.long	0x4909
	.uleb128 0x1
	.long	0x4913
	.byte	0
	.uleb128 0x43
	.ascii "~_UninitDestroyGuard\0"
	.byte	0xa
	.byte	0x76
	.byte	0x7
	.ascii "_ZNSt19_UninitDestroyGuardIP8ParticlevED4Ev\0"
	.long	0x3755
	.long	0x375b
	.uleb128 0x2
	.long	0x4909
	.byte	0
	.uleb128 0x43
	.ascii "release\0"
	.byte	0xa
	.byte	0x7d
	.byte	0xc
	.ascii "_ZNSt19_UninitDestroyGuardIP8ParticlevE7releaseEv\0"
	.long	0x37a1
	.long	0x37a7
	.uleb128 0x2
	.long	0x4909
	.byte	0
	.uleb128 0x10
	.ascii "_M_first\0"
	.byte	0xa
	.byte	0x7f
	.byte	0x1e
	.long	0x4823
	.byte	0
	.uleb128 0x10
	.ascii "_M_cur\0"
	.byte	0xa
	.byte	0x80
	.byte	0x19
	.long	0x4918
	.byte	0x8
	.uleb128 0x24
	.secrel32	.LASF38
	.byte	0xa
	.byte	0x83
	.byte	0x7
	.ascii "_ZNSt19_UninitDestroyGuardIP8ParticlevEC4ERKS2_\0"
	.byte	0x3
	.long	0x380a
	.long	0x3815
	.uleb128 0x2
	.long	0x4909
	.uleb128 0x1
	.long	0x491d
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x6c
	.secrel32	.LASF24
	.byte	0
	.uleb128 0x5
	.long	0x3690
	.uleb128 0x6d
	.ascii "__glibcxx_assert_fail\0"
	.byte	0x9
	.word	0x26f
	.byte	0x3
	.ascii "_ZSt21__glibcxx_assert_failPKciS0_S0_\0"
	.long	0x3883
	.uleb128 0x1
	.long	0x48eb
	.uleb128 0x1
	.long	0x4174
	.uleb128 0x1
	.long	0x48eb
	.uleb128 0x1
	.long	0x48eb
	.byte	0
	.uleb128 0x58
	.ascii "__throw_bad_alloc\0"
	.byte	0x35
	.ascii "_ZSt17__throw_bad_allocv\0"
	.uleb128 0x58
	.ascii "__throw_bad_array_new_length\0"
	.byte	0x38
	.ascii "_ZSt28__throw_bad_array_new_lengthv\0"
	.uleb128 0x6e
	.ascii "__throw_length_error\0"
	.byte	0x18
	.byte	0x4c
	.byte	0x3
	.ascii "_ZSt20__throw_length_errorPKc\0"
	.long	0x3934
	.uleb128 0x1
	.long	0x48eb
	.byte	0
	.uleb128 0x47
	.ascii "__fill_a1<Particle*, Particle>\0"
	.byte	0x3
	.word	0x381
	.ascii "_ZSt9__fill_a1IP8ParticleS0_EvT_S2_RKT0_\0"
	.long	0x39a6
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x48ff
	.byte	0
	.uleb128 0x47
	.ascii "__fill_a<Particle*, Particle>\0"
	.byte	0x3
	.word	0x3d2
	.ascii "_ZSt8__fill_aIP8ParticleS0_EvT_S2_RKT0_\0"
	.long	0x3a18
	.uleb128 0x4
	.ascii "_FIte\0"
	.long	0x481e
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x48ff
	.byte	0
	.uleb128 0x25
	.ascii "__fill_n_a<Particle*, long long unsigned int, Particle>\0"
	.byte	0x3
	.word	0x471
	.byte	0x5
	.ascii "_ZSt10__fill_n_aIP8ParticleyS0_ET_S2_T0_RKT1_St26random_access_iterator_tag\0"
	.long	0x481e
	.long	0x3ad9
	.uleb128 0x6
	.secrel32	.LASF39
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x40ed
	.uleb128 0x1
	.long	0x48ff
	.uleb128 0x1
	.long	0x3b6
	.byte	0
	.uleb128 0x33
	.ascii "__iterator_category<Particle*>\0"
	.byte	0xd
	.byte	0xf1
	.byte	0x5
	.ascii "_ZSt19__iterator_categoryIP8ParticleENSt15iterator_traitsIT_E17iterator_categoryERKS3_\0"
	.long	0x3645
	.long	0x3b6c
	.uleb128 0x4
	.ascii "_Iter\0"
	.long	0x481e
	.uleb128 0x1
	.long	0x4abd
	.byte	0
	.uleb128 0x33
	.ascii "construct_at<Particle>\0"
	.byte	0xb
	.byte	0x60
	.byte	0x5
	.ascii "_ZSt12construct_atI8ParticleJEQaant20is_unbounded_array_vIT_ErqXgsnwcvPvLi0E_S1_pispcl7declvalIT0_EEEEEPS1_S4_DpOS3_\0"
	.long	0x481e
	.long	0x3c18
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x39
	.secrel32	.LASF40
	.uleb128 0x1
	.long	0x481e
	.byte	0
	.uleb128 0x25
	.ascii "fill_n<Particle*, long long unsigned int, Particle>\0"
	.byte	0x3
	.word	0x495
	.byte	0x5
	.ascii "_ZSt6fill_nIP8ParticleyS0_ET_S2_T0_RKT1_\0"
	.long	0x481e
	.long	0x3cad
	.uleb128 0x4
	.ascii "_OI\0"
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x40ed
	.uleb128 0x1
	.long	0x48ff
	.byte	0
	.uleb128 0x3a
	.ascii "_Construct<Particle>\0"
	.byte	0xb
	.byte	0x7b
	.byte	0x5
	.ascii "_ZSt10_ConstructI8ParticleJEEvPT_DpOT0_\0"
	.long	0x3d06
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x39
	.secrel32	.LASF40
	.uleb128 0x1
	.long	0x481e
	.byte	0
	.uleb128 0x3a
	.ascii "destroy_at<Particle>\0"
	.byte	0xb
	.byte	0x50
	.byte	0x5
	.ascii "_ZSt10destroy_atI8ParticleEvPT_\0"
	.long	0x3d52
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x1
	.long	0x481e
	.byte	0
	.uleb128 0x33
	.ascii "__addressof<Particle>\0"
	.byte	0xc
	.byte	0x34
	.byte	0x5
	.ascii "_ZSt11__addressofI8ParticleEPT_RS1_\0"
	.long	0x481e
	.long	0x3da7
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x1
	.long	0x4904
	.byte	0
	.uleb128 0x25
	.ascii "__uninitialized_default_n<Particle*, long long unsigned int>\0"
	.byte	0xa
	.word	0x3be
	.byte	0x5
	.ascii "_ZSt25__uninitialized_default_nIP8ParticleyET_S2_T0_\0"
	.long	0x481e
	.long	0x3e43
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x40ed
	.byte	0
	.uleb128 0x33
	.ascii "min<long long unsigned int>\0"
	.byte	0x3
	.byte	0xea
	.byte	0x5
	.ascii "_ZSt3minIyERKT_S2_S2_\0"
	.long	0x527e
	.long	0x3e95
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x40ed
	.uleb128 0x1
	.long	0x527e
	.uleb128 0x1
	.long	0x527e
	.byte	0
	.uleb128 0x3a
	.ascii "_Destroy<Particle*>\0"
	.byte	0xb
	.byte	0xdb
	.byte	0x5
	.ascii "_ZSt8_DestroyIP8ParticleEvT_S2_\0"
	.long	0x3ee5
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x481e
	.byte	0
	.uleb128 0x25
	.ascii "__uninitialized_default_n_a<Particle*, long long unsigned int, Particle>\0"
	.byte	0xa
	.word	0x403
	.byte	0x5
	.ascii "_ZSt27__uninitialized_default_n_aIP8ParticleyS0_ET_S2_T0_RSaIT1_E\0"
	.long	0x481e
	.long	0x3fa8
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x40ed
	.uleb128 0x1
	.long	0x4841
	.byte	0
	.uleb128 0x47
	.ascii "_Destroy<Particle*, Particle>\0"
	.byte	0x8
	.word	0x412
	.ascii "_ZSt8_DestroyIP8ParticleS0_EvT_S2_RSaIT0_E\0"
	.long	0x401b
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x481e
	.uleb128 0x1
	.long	0x4841
	.byte	0
	.uleb128 0x25
	.ascii "__size_to_integer\0"
	.byte	0x3
	.word	0x404
	.byte	0x3
	.ascii "_ZSt17__size_to_integery\0"
	.long	0x40ed
	.long	0x4059
	.uleb128 0x1
	.long	0x40ed
	.byte	0
	.uleb128 0x45
	.ascii "is_constant_evaluated\0"
	.byte	0x1
	.word	0xfa7
	.byte	0x3
	.ascii "_ZSt21is_constant_evaluatedv\0"
	.long	0x40d6
	.uleb128 0x45
	.ascii "__is_constant_evaluated\0"
	.byte	0x9
	.word	0x246
	.byte	0x3
	.ascii "_ZSt23__is_constant_evaluatedv\0"
	.long	0x40d6
	.byte	0
	.uleb128 0x8
	.byte	0x1
	.byte	0x2
	.ascii "bool\0"
	.uleb128 0x5
	.long	0x40d6
	.uleb128 0xa
	.long	0x17c
	.uleb128 0xa
	.long	0x27b
	.uleb128 0x8
	.byte	0x8
	.byte	0x7
	.ascii "long long unsigned int\0"
	.uleb128 0x5
	.long	0x40ed
	.uleb128 0x8
	.byte	0x1
	.byte	0x8
	.ascii "unsigned char\0"
	.uleb128 0x8
	.byte	0x2
	.byte	0x7
	.ascii "short unsigned int\0"
	.uleb128 0x8
	.byte	0x4
	.byte	0x7
	.ascii "unsigned int\0"
	.uleb128 0x8
	.byte	0x4
	.byte	0x7
	.ascii "long unsigned int\0"
	.uleb128 0x8
	.byte	0x1
	.byte	0x6
	.ascii "signed char\0"
	.uleb128 0x8
	.byte	0x2
	.byte	0x5
	.ascii "short int\0"
	.uleb128 0x8
	.byte	0x4
	.byte	0x5
	.ascii "int\0"
	.uleb128 0x8
	.byte	0x4
	.byte	0x5
	.ascii "long int\0"
	.uleb128 0x8
	.byte	0x8
	.byte	0x5
	.ascii "long long int\0"
	.uleb128 0x8
	.byte	0x2
	.byte	0x7
	.ascii "wchar_t\0"
	.uleb128 0x8
	.byte	0x1
	.byte	0x10
	.ascii "char8_t\0"
	.uleb128 0x8
	.byte	0x2
	.byte	0x10
	.ascii "char16_t\0"
	.uleb128 0x8
	.byte	0x4
	.byte	0x10
	.ascii "char32_t\0"
	.uleb128 0x3f
	.ascii "__gnu_cxx\0"
	.byte	0x9
	.word	0x175
	.byte	0xb
	.long	0x469b
	.uleb128 0x22
	.ascii "__ops\0"
	.byte	0x19
	.byte	0x25
	.byte	0xb
	.uleb128 0x11
	.ascii "__alloc_traits<std::allocator<Particle>, Particle>\0"
	.byte	0x1
	.byte	0x1a
	.byte	0x2f
	.byte	0xa
	.long	0x457b
	.uleb128 0x32
	.byte	0x1a
	.byte	0x2f
	.byte	0xa
	.long	0xa02
	.uleb128 0x32
	.byte	0x1a
	.byte	0x2f
	.byte	0xa
	.long	0x991
	.uleb128 0x32
	.byte	0x1a
	.byte	0x2f
	.byte	0xa
	.long	0xa78
	.uleb128 0x32
	.byte	0x1a
	.byte	0x2f
	.byte	0xa
	.long	0xad2
	.uleb128 0x2a
	.long	0x950
	.uleb128 0x33
	.ascii "_S_select_on_copy\0"
	.byte	0x1a
	.byte	0x63
	.byte	0x1d
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI8ParticleES1_E17_S_select_on_copyERKS2_\0"
	.long	0x7e2
	.long	0x42b1
	.uleb128 0x1
	.long	0x483c
	.byte	0
	.uleb128 0x3a
	.ascii "_S_on_swap\0"
	.byte	0x1a
	.byte	0x67
	.byte	0x26
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI8ParticleES1_E10_S_on_swapERS2_S4_\0"
	.long	0x4313
	.uleb128 0x1
	.long	0x4841
	.uleb128 0x1
	.long	0x4841
	.byte	0
	.uleb128 0x34
	.ascii "_S_propagate_on_copy_assign\0"
	.byte	0x6b
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI8ParticleES1_E27_S_propagate_on_copy_assignEv\0"
	.long	0x40d6
	.uleb128 0x34
	.ascii "_S_propagate_on_move_assign\0"
	.byte	0x6f
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI8ParticleES1_E27_S_propagate_on_move_assignEv\0"
	.long	0x40d6
	.uleb128 0x34
	.ascii "_S_propagate_on_swap\0"
	.byte	0x73
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI8ParticleES1_E20_S_propagate_on_swapEv\0"
	.long	0x40d6
	.uleb128 0x34
	.ascii "_S_always_equal\0"
	.byte	0x77
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI8ParticleES1_E15_S_always_equalEv\0"
	.long	0x40d6
	.uleb128 0x34
	.ascii "_S_nothrow_move\0"
	.byte	0x7b
	.ascii "_ZN9__gnu_cxx14__alloc_traitsISaI8ParticleES1_E15_S_nothrow_moveEv\0"
	.long	0x40d6
	.uleb128 0x13
	.secrel32	.LASF3
	.byte	0x1a
	.byte	0x37
	.byte	0x35
	.long	0xbac
	.uleb128 0x5
	.long	0x450a
	.uleb128 0x13
	.secrel32	.LASF15
	.byte	0x1a
	.byte	0x38
	.byte	0x35
	.long	0x984
	.uleb128 0x13
	.secrel32	.LASF30
	.byte	0x1a
	.byte	0x3d
	.byte	0x35
	.long	0x4855
	.uleb128 0x13
	.secrel32	.LASF32
	.byte	0x1a
	.byte	0x3e
	.byte	0x35
	.long	0x485a
	.uleb128 0x11
	.ascii "rebind<Particle>\0"
	.byte	0x1
	.byte	0x1a
	.byte	0x7f
	.byte	0xe
	.long	0x4571
	.uleb128 0x23
	.ascii "other\0"
	.byte	0x1a
	.byte	0x80
	.byte	0x41
	.long	0xbb9
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.byte	0
	.uleb128 0x6
	.secrel32	.LASF24
	.long	0x7e2
	.byte	0
	.uleb128 0x38
	.ascii "__normal_iterator<Particle*, std::vector<Particle, std::allocator<Particle> > >\0"
	.uleb128 0x38
	.ascii "__normal_iterator<const Particle*, std::vector<Particle, std::allocator<Particle> > >\0"
	.uleb128 0x6f
	.ascii "__conditional_type<false, const Particle, const Particle&>\0"
	.byte	0x1
	.byte	0x1b
	.byte	0x40
	.byte	0xc
	.uleb128 0x23
	.ascii "__type\0"
	.byte	0x1b
	.byte	0x41
	.byte	0x18
	.long	0x48ff
	.uleb128 0x41
	.ascii "_Cond\0"
	.long	0x40d6
	.byte	0
	.uleb128 0x4
	.ascii "_Iftrue\0"
	.long	0x4805
	.uleb128 0x4
	.ascii "_Iffalse\0"
	.long	0x48ff
	.byte	0
	.byte	0
	.uleb128 0x8
	.byte	0x10
	.byte	0x4
	.ascii "long double\0"
	.uleb128 0x8
	.byte	0x8
	.byte	0x4
	.ascii "double\0"
	.uleb128 0x8
	.byte	0x4
	.byte	0x4
	.ascii "float\0"
	.uleb128 0x8
	.byte	0x2
	.byte	0x4
	.ascii "_Float16\0"
	.uleb128 0x8
	.byte	0x4
	.byte	0x4
	.ascii "_Float32\0"
	.uleb128 0x8
	.byte	0x8
	.byte	0x4
	.ascii "_Float64\0"
	.uleb128 0x8
	.byte	0x10
	.byte	0x4
	.ascii "_Float128\0"
	.uleb128 0x8
	.byte	0x2
	.byte	0x4
	.ascii "__bf16\0"
	.uleb128 0x8
	.byte	0x10
	.byte	0x5
	.ascii "__int128\0"
	.uleb128 0x70
	.ascii "__gnu_debug\0"
	.byte	0x1c
	.byte	0x27
	.byte	0xb
	.long	0x4721
	.uleb128 0x71
	.byte	0x12
	.byte	0x3a
	.byte	0x18
	.long	0x3f6
	.byte	0
	.uleb128 0x8
	.byte	0x1
	.byte	0x6
	.ascii "char\0"
	.uleb128 0x5
	.long	0x4721
	.uleb128 0xa
	.long	0x4733
	.uleb128 0x72
	.uleb128 0x73
	.byte	0x8
	.uleb128 0x8
	.byte	0x10
	.byte	0x7
	.ascii "__int128 unsigned\0"
	.uleb128 0x74
	.byte	0x20
	.byte	0x10
	.byte	0x1d
	.word	0x1a8
	.byte	0x10
	.ascii "11max_align_t\0"
	.long	0x4797
	.uleb128 0x59
	.ascii "__max_align_ll\0"
	.word	0x1a9
	.byte	0xd
	.long	0x4187
	.byte	0x8
	.byte	0
	.uleb128 0x59
	.ascii "__max_align_ld\0"
	.word	0x1aa
	.byte	0xf
	.long	0x469b
	.byte	0x10
	.byte	0x10
	.byte	0
	.uleb128 0x75
	.ascii "max_align_t\0"
	.byte	0x1d
	.word	0x1ab
	.byte	0x3
	.long	0x474b
	.byte	0x10
	.uleb128 0x11
	.ascii "Particle\0"
	.byte	0x18
	.byte	0x4
	.byte	0x7
	.byte	0x8
	.long	0x4805
	.uleb128 0x10
	.ascii "x\0"
	.byte	0x4
	.byte	0x8
	.byte	0xb
	.long	0x46b4
	.byte	0
	.uleb128 0x10
	.ascii "y\0"
	.byte	0x4
	.byte	0x8
	.byte	0xe
	.long	0x46b4
	.byte	0x4
	.uleb128 0x10
	.ascii "z\0"
	.byte	0x4
	.byte	0x8
	.byte	0x11
	.long	0x46b4
	.byte	0x8
	.uleb128 0x10
	.ascii "vx\0"
	.byte	0x4
	.byte	0x9
	.byte	0xb
	.long	0x46b4
	.byte	0xc
	.uleb128 0x10
	.ascii "vy\0"
	.byte	0x4
	.byte	0x9
	.byte	0xf
	.long	0x46b4
	.byte	0x10
	.uleb128 0x10
	.ascii "vz\0"
	.byte	0x4
	.byte	0x9
	.byte	0x13
	.long	0x46b4
	.byte	0x14
	.byte	0
	.uleb128 0x5
	.long	0x47ad
	.uleb128 0xa
	.long	0x5db
	.uleb128 0x5
	.long	0x480a
	.uleb128 0x9
	.long	0x7dd
	.uleb128 0x9
	.long	0x5db
	.uleb128 0xa
	.long	0x47ad
	.uleb128 0x5
	.long	0x481e
	.uleb128 0xa
	.long	0x7dd
	.uleb128 0x5
	.long	0x4828
	.uleb128 0xa
	.long	0x7e2
	.uleb128 0x5
	.long	0x4832
	.uleb128 0x9
	.long	0x94b
	.uleb128 0x9
	.long	0x7e2
	.uleb128 0x9
	.long	0x9e3
	.uleb128 0x9
	.long	0x9f0
	.uleb128 0xa
	.long	0x4805
	.uleb128 0x9
	.long	0x450a
	.uleb128 0x9
	.long	0x4516
	.uleb128 0xa
	.long	0xc0b
	.uleb128 0x5
	.long	0x485f
	.uleb128 0x2e
	.long	0xc0b
	.uleb128 0x9
	.long	0xde1
	.uleb128 0x9
	.long	0xc0b
	.uleb128 0xa
	.long	0xdf2
	.uleb128 0x5
	.long	0x4878
	.uleb128 0x9
	.long	0x1076
	.uleb128 0x2e
	.long	0xdf2
	.uleb128 0x2e
	.long	0x106a
	.uleb128 0x9
	.long	0x106a
	.uleb128 0xa
	.long	0xbd0
	.uleb128 0x5
	.long	0x4896
	.uleb128 0xa
	.long	0x1573
	.uleb128 0x9
	.long	0x1135
	.uleb128 0x2e
	.long	0xbd0
	.uleb128 0x9
	.long	0x17f6
	.uleb128 0xa
	.long	0x15f0
	.uleb128 0x5
	.long	0x48b4
	.uleb128 0x9
	.long	0x197b
	.uleb128 0x9
	.long	0x1a30
	.uleb128 0x9
	.long	0x334c
	.uleb128 0x2e
	.long	0x15f0
	.uleb128 0x9
	.long	0x336b
	.uleb128 0x9
	.long	0x15f0
	.uleb128 0xa
	.long	0x334c
	.uleb128 0x5
	.long	0x48dc
	.uleb128 0x2e
	.long	0x1a24
	.uleb128 0xa
	.long	0x4729
	.uleb128 0x9
	.long	0x1803
	.uleb128 0xa
	.long	0x3370
	.uleb128 0xa
	.long	0x3538
	.uleb128 0x9
	.long	0x4805
	.uleb128 0x9
	.long	0x47ad
	.uleb128 0xa
	.long	0x3690
	.uleb128 0x5
	.long	0x4909
	.uleb128 0x9
	.long	0x481e
	.uleb128 0xa
	.long	0x481e
	.uleb128 0x9
	.long	0x3824
	.uleb128 0x5a
	.secrel32	.LASF41
	.byte	0x94
	.ascii "_ZdlPvy\0"
	.long	0x493f
	.uleb128 0x1
	.long	0x4734
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x5a
	.secrel32	.LASF41
	.byte	0x8f
	.ascii "_ZdlPv\0"
	.long	0x4956
	.uleb128 0x1
	.long	0x4734
	.byte	0
	.uleb128 0x76
	.secrel32	.LASF42
	.byte	0x2
	.byte	0x89
	.byte	0x1a
	.ascii "_Znwy\0"
	.long	0x4734
	.long	0x4972
	.uleb128 0x1
	.long	0x280
	.byte	0
	.uleb128 0x3b
	.long	0x3934
	.quad	.LFB1804
	.quad	.LFE1804-.LFB1804
	.uleb128 0x1
	.byte	0x9c
	.long	0x4a0f
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x27
	.secrel32	.LASF43
	.byte	0x3
	.word	0x381
	.byte	0x20
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x27
	.secrel32	.LASF44
	.byte	0x3
	.word	0x381
	.byte	0x3a
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x27
	.secrel32	.LASF45
	.byte	0x3
	.word	0x382
	.byte	0x13
	.long	0x48ff
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.uleb128 0x28
	.ascii "__load_outside_loop\0"
	.byte	0x3
	.word	0x38a
	.byte	0x12
	.long	0x40de
	.uleb128 0x2
	.byte	0x91
	.sleb128 -17
	.uleb128 0x21
	.ascii "_Up\0"
	.byte	0x3
	.word	0x39a
	.byte	0x20
	.long	0x4663
	.uleb128 0x28
	.ascii "__val\0"
	.byte	0x3
	.word	0x39b
	.byte	0xb
	.long	0x49ef
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.byte	0
	.uleb128 0x1e
	.long	0x39a6
	.long	0x4a54
	.uleb128 0x4
	.ascii "_FIte\0"
	.long	0x481e
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x19
	.secrel32	.LASF43
	.byte	0x3
	.word	0x3d2
	.byte	0x14
	.long	0x481e
	.uleb128 0x19
	.secrel32	.LASF44
	.byte	0x3
	.word	0x3d2
	.byte	0x23
	.long	0x481e
	.uleb128 0x19
	.secrel32	.LASF45
	.byte	0x3
	.word	0x3d2
	.byte	0x36
	.long	0x48ff
	.byte	0
	.uleb128 0xd
	.long	0x77f
	.long	0x4a62
	.byte	0x3
	.long	0x4a6c
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x482d
	.byte	0
	.uleb128 0x1e
	.long	0x3a18
	.long	0x4abd
	.uleb128 0x6
	.secrel32	.LASF39
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x19
	.secrel32	.LASF43
	.byte	0x3
	.word	0x471
	.byte	0x20
	.long	0x481e
	.uleb128 0x14
	.ascii "__n\0"
	.byte	0x3
	.word	0x471
	.byte	0x2f
	.long	0x40ed
	.uleb128 0x19
	.secrel32	.LASF45
	.byte	0x3
	.word	0x471
	.byte	0x3f
	.long	0x48ff
	.uleb128 0x1
	.long	0x3b6
	.byte	0
	.uleb128 0x9
	.long	0x4823
	.uleb128 0x1e
	.long	0x3ad9
	.long	0x4adc
	.uleb128 0x4
	.ascii "_Iter\0"
	.long	0x481e
	.uleb128 0x1
	.long	0x4abd
	.byte	0
	.uleb128 0x1a
	.long	0x3b6c
	.quad	.LFB1799
	.quad	.LFE1799-.LFB1799
	.uleb128 0x1
	.byte	0x9c
	.long	0x4b2f
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x39
	.secrel32	.LASF40
	.uleb128 0x3c
	.secrel32	.LASF46
	.byte	0x60
	.byte	0x17
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x5b
	.ascii "__args\0"
	.byte	0x60
	.byte	0x2a
	.uleb128 0x48
	.ascii "__loc\0"
	.byte	0xb
	.byte	0x63
	.byte	0xd
	.long	0x4734
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.uleb128 0x1f
	.long	0x6c9
	.long	0x4b4e
	.quad	.LFB1798
	.quad	.LFE1798-.LFB1798
	.uleb128 0x1
	.byte	0x9c
	.long	0x4ba6
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x480f
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x16
	.ascii "__n\0"
	.byte	0x5
	.byte	0x7e
	.byte	0x1a
	.long	0x71e
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x35
	.long	0x472e
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.uleb128 0x77
	.long	0x4b84
	.uleb128 0x78
	.ascii "__al\0"
	.byte	0x5
	.byte	0x92
	.byte	0x17
	.long	0x3e0
	.byte	0
	.uleb128 0x20
	.long	0x4a54
	.quad	.LBB172
	.quad	.LBE172-.LBB172
	.byte	0x5
	.byte	0x86
	.byte	0x2e
	.uleb128 0x3
	.long	0x4a62
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.byte	0
	.uleb128 0x1e
	.long	0x3c18
	.long	0x4bf2
	.uleb128 0x4
	.ascii "_OI\0"
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x19
	.secrel32	.LASF43
	.byte	0x3
	.word	0x495
	.byte	0x10
	.long	0x481e
	.uleb128 0x14
	.ascii "__n\0"
	.byte	0x3
	.word	0x495
	.byte	0x1f
	.long	0x40ed
	.uleb128 0x19
	.secrel32	.LASF45
	.byte	0x3
	.word	0x495
	.byte	0x2f
	.long	0x48ff
	.byte	0
	.uleb128 0x3d
	.long	0x375b
	.long	0x4c11
	.quad	.LFB1796
	.quad	.LFE1796-.LFB1796
	.uleb128 0x1
	.byte	0x9c
	.long	0x4c1e
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x490e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x1a
	.long	0x3cad
	.quad	.LFB1795
	.quad	.LFE1795-.LFB1795
	.uleb128 0x1
	.byte	0x9c
	.long	0x4c79
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x39
	.secrel32	.LASF40
	.uleb128 0x16
	.ascii "__p\0"
	.byte	0xb
	.byte	0x7b
	.byte	0x15
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x5b
	.ascii "__args\0"
	.byte	0x7b
	.byte	0x21
	.uleb128 0x3e
	.long	0x5e7e
	.quad	.LBB170
	.quad	.LBE170-.LBB170
	.byte	0xb
	.byte	0x7e
	.byte	0x27
	.byte	0
	.uleb128 0xd
	.long	0x3708
	.long	0x4c87
	.byte	0x2
	.long	0x4c91
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x490e
	.byte	0
	.uleb128 0x2f
	.long	0x4c79
	.ascii "_ZNSt19_UninitDestroyGuardIP8ParticlevED1Ev\0"
	.long	0x4cdc
	.quad	.LFB1794
	.quad	.LFE1794-.LFB1794
	.uleb128 0x1
	.byte	0x9c
	.long	0x4ce5
	.uleb128 0x3
	.long	0x4c87
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x1f
	.long	0x72a
	.long	0x4d04
	.quad	.LFB1791
	.quad	.LFE1791-.LFB1791
	.uleb128 0x1
	.byte	0x9c
	.long	0x4d2f
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x480f
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x16
	.ascii "__p\0"
	.byte	0x5
	.byte	0x9c
	.byte	0x17
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x16
	.ascii "__n\0"
	.byte	0x5
	.byte	0x9c
	.byte	0x26
	.long	0x71e
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.byte	0
	.uleb128 0xd
	.long	0x8cf
	.long	0x4d3d
	.byte	0x3
	.long	0x4d53
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x4837
	.uleb128 0x30
	.ascii "__n\0"
	.byte	0x6
	.byte	0xc2
	.byte	0x17
	.long	0x280
	.byte	0
	.uleb128 0x1a
	.long	0x47c
	.quad	.LFB1789
	.quad	.LFE1789-.LFB1789
	.uleb128 0x1
	.byte	0x9c
	.long	0x4eb2
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x27
	.secrel32	.LASF43
	.byte	0xa
	.word	0x393
	.byte	0x2d
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0xa
	.word	0x393
	.byte	0x3c
	.long	0x40ed
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x5c
	.quad	.LBB158
	.quad	.LBE158-.LBB158
	.uleb128 0x28
	.ascii "__val\0"
	.byte	0xa
	.word	0x397
	.byte	0x40
	.long	0x4eb2
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x49
	.long	0x5045
	.quad	.LBB159
	.quad	.LBE159-.LBB159
	.byte	0xa
	.word	0x398
	.byte	0x15
	.long	0x4dea
	.uleb128 0x3
	.long	0x5057
	.uleb128 0x3
	.byte	0x91
	.sleb128 -96
	.byte	0
	.uleb128 0x17
	.long	0x4ba6
	.quad	.LBB161
	.quad	.LBE161-.LBB161
	.byte	0xa
	.word	0x39b
	.byte	0x1d
	.uleb128 0x3
	.long	0x4bca
	.uleb128 0x3
	.byte	0x91
	.sleb128 -104
	.uleb128 0x3
	.long	0x4bd7
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x3
	.long	0x4be4
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.uleb128 0x49
	.long	0x4ac2
	.quad	.LBB163
	.quad	.LBE163-.LBB163
	.byte	0x3
	.word	0x49b
	.byte	0x23
	.long	0x4e3f
	.uleb128 0xf
	.long	0x4ad6
	.byte	0
	.uleb128 0x17
	.long	0x4a6c
	.quad	.LBB165
	.quad	.LBE165-.LBB165
	.byte	0x3
	.word	0x49a
	.byte	0x1d
	.uleb128 0x3
	.long	0x4a90
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.uleb128 0x3
	.long	0x4a9d
	.uleb128 0x2
	.byte	0x91
	.sleb128 -56
	.uleb128 0x3
	.long	0x4aaa
	.uleb128 0x2
	.byte	0x91
	.sleb128 -64
	.uleb128 0x3
	.long	0x4ab7
	.uleb128 0x3
	.byte	0x91
	.sleb128 -105
	.uleb128 0x17
	.long	0x4a0f
	.quad	.LBB167
	.quad	.LBE167-.LBB167
	.byte	0x3
	.word	0x47c
	.byte	0x14
	.uleb128 0x3
	.long	0x4a2c
	.uleb128 0x3
	.byte	0x91
	.sleb128 -72
	.uleb128 0x3
	.long	0x4a39
	.uleb128 0x3
	.byte	0x91
	.sleb128 -80
	.uleb128 0x3
	.long	0x4a46
	.uleb128 0x3
	.byte	0x91
	.sleb128 -88
	.byte	0
	.byte	0
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0xa
	.long	0x365f
	.uleb128 0x1a
	.long	0x533
	.quad	.LFB1785
	.quad	.LFE1785-.LFB1785
	.uleb128 0x1
	.byte	0x9c
	.long	0x4f3b
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x27
	.secrel32	.LASF43
	.byte	0xa
	.word	0x383
	.byte	0x2d
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0xa
	.word	0x383
	.byte	0x3c
	.long	0x40ed
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x28
	.ascii "__guard\0"
	.byte	0xa
	.word	0x385
	.byte	0x2a
	.long	0x3690
	.uleb128 0x2
	.byte	0x91
	.sleb128 -64
	.uleb128 0x17
	.long	0x5045
	.quad	.LBB155
	.quad	.LBE155-.LBB155
	.byte	0xa
	.word	0x387
	.byte	0x15
	.uleb128 0x3
	.long	0x5057
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.byte	0
	.uleb128 0xd
	.long	0x36be
	.long	0x4f49
	.byte	0x2
	.long	0x4f5f
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x490e
	.uleb128 0x79
	.secrel32	.LASF43
	.byte	0xa
	.byte	0x71
	.byte	0x2d
	.long	0x4913
	.byte	0
	.uleb128 0x4a
	.long	0x4f3b
	.ascii "_ZNSt19_UninitDestroyGuardIP8ParticlevEC1ERS1_\0"
	.long	0x4fad
	.quad	.LFB1788
	.quad	.LFE1788-.LFB1788
	.uleb128 0x1
	.byte	0x9c
	.long	0x4fbe
	.uleb128 0x3
	.long	0x4f49
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x3
	.long	0x4f52
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0xd
	.long	0x90b
	.long	0x4fcc
	.byte	0x3
	.long	0x4fee
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x4837
	.uleb128 0x30
	.ascii "__p\0"
	.byte	0x6
	.byte	0xd0
	.byte	0x17
	.long	0x481e
	.uleb128 0x30
	.ascii "__n\0"
	.byte	0x6
	.byte	0xd0
	.byte	0x23
	.long	0x280
	.byte	0
	.uleb128 0x1e
	.long	0x991
	.long	0x5012
	.uleb128 0x14
	.ascii "__a\0"
	.byte	0x8
	.word	0x265
	.byte	0x20
	.long	0x4846
	.uleb128 0x14
	.ascii "__n\0"
	.byte	0x8
	.word	0x265
	.byte	0x2f
	.long	0x9f5
	.byte	0
	.uleb128 0x3b
	.long	0x3d06
	.quad	.LFB1782
	.quad	.LFE1782-.LFB1782
	.uleb128 0x1
	.byte	0x9c
	.long	0x5045
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x3c
	.secrel32	.LASF46
	.byte	0x50
	.byte	0x15
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x1e
	.long	0x3d52
	.long	0x5064
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x30
	.ascii "__r\0"
	.byte	0xc
	.byte	0x34
	.byte	0x16
	.long	0x4904
	.byte	0
	.uleb128 0x1a
	.long	0x3da7
	.quad	.LFB1780
	.quad	.LFE1780-.LFB1780
	.uleb128 0x1
	.byte	0x9c
	.long	0x50c9
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x27
	.secrel32	.LASF43
	.byte	0xa
	.word	0x3be
	.byte	0x30
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0xa
	.word	0x3be
	.byte	0x3f
	.long	0x40ed
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x7a
	.ascii "__can_fill\0"
	.byte	0xa
	.word	0x3c9
	.byte	0x16
	.long	0x40de
	.uleb128 0x2
	.byte	0x91
	.sleb128 -17
	.byte	0
	.uleb128 0x1e
	.long	0xa78
	.long	0x50fa
	.uleb128 0x14
	.ascii "__a\0"
	.byte	0x8
	.word	0x288
	.byte	0x22
	.long	0x4846
	.uleb128 0x14
	.ascii "__p\0"
	.byte	0x8
	.word	0x288
	.byte	0x2f
	.long	0x984
	.uleb128 0x14
	.ascii "__n\0"
	.byte	0x8
	.word	0x288
	.byte	0x3e
	.long	0x9f5
	.byte	0
	.uleb128 0x1f
	.long	0x143a
	.long	0x5119
	.quad	.LFB1778
	.quad	.LFE1778-.LFB1778
	.uleb128 0x1
	.byte	0x9c
	.long	0x51a2
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x489b
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0x7
	.word	0x180
	.byte	0x1a
	.long	0x280
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x17
	.long	0x4fee
	.quad	.LBB148
	.quad	.LBE148-.LBB148
	.byte	0x7
	.word	0x183
	.byte	0x21
	.uleb128 0x3
	.long	0x4ff7
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x3
	.long	0x5004
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x17
	.long	0x4d2f
	.quad	.LBB150
	.quad	.LBE150-.LBB150
	.byte	0x8
	.word	0x266
	.byte	0x1c
	.uleb128 0x3
	.long	0x4d3d
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.uleb128 0x3
	.long	0x4d46
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.uleb128 0x3e
	.long	0x5e7e
	.quad	.LBB152
	.quad	.LBE152-.LBB152
	.byte	0x6
	.byte	0xc4
	.byte	0x22
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0xd
	.long	0xc55
	.long	0x51b0
	.byte	0x2
	.long	0x51ba
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x4864
	.byte	0
	.uleb128 0x4a
	.long	0x51a2
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE17_Vector_impl_dataC2Ev\0"
	.long	0x5216
	.quad	.LFB1776
	.quad	.LFE1776-.LFB1776
	.uleb128 0x1
	.byte	0x9c
	.long	0x521f
	.uleb128 0x3
	.long	0x51b0
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0xd
	.long	0x63a
	.long	0x522d
	.byte	0x2
	.long	0x523c
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x480f
	.uleb128 0x1
	.long	0x4814
	.byte	0
	.uleb128 0x29
	.long	0x521f
	.ascii "_ZNSt15__new_allocatorI8ParticleEC2ERKS1_\0"
	.long	0x5273
	.long	0x527e
	.uleb128 0xf
	.long	0x522d
	.uleb128 0xf
	.long	0x5236
	.byte	0
	.uleb128 0x9
	.long	0x4107
	.uleb128 0x3b
	.long	0x3e43
	.quad	.LFB1771
	.quad	.LFE1771-.LFB1771
	.uleb128 0x1
	.byte	0x9c
	.long	0x52c6
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x40ed
	.uleb128 0x16
	.ascii "__a\0"
	.byte	0x3
	.byte	0xea
	.byte	0x14
	.long	0x527e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x16
	.ascii "__b\0"
	.byte	0x3
	.byte	0xea
	.byte	0x24
	.long	0x527e
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x1a
	.long	0x3e95
	.quad	.LFB1769
	.quad	.LFE1769-.LFB1769
	.uleb128 0x1
	.byte	0x9c
	.long	0x5340
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x3c
	.secrel32	.LASF43
	.byte	0xdb
	.byte	0x1f
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x3c
	.secrel32	.LASF44
	.byte	0xdb
	.byte	0x39
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x3e
	.long	0x5e7e
	.quad	.LBB143
	.quad	.LBE143-.LBB143
	.byte	0xb
	.byte	0xe4
	.byte	0x2c
	.uleb128 0x20
	.long	0x5045
	.quad	.LBB145
	.quad	.LBE145-.LBB145
	.byte	0xb
	.byte	0xe6
	.byte	0x13
	.uleb128 0x3
	.long	0x5057
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.byte	0
	.uleb128 0x1a
	.long	0x3ee5
	.quad	.LFB1768
	.quad	.LFE1768-.LFB1768
	.uleb128 0x1
	.byte	0x9c
	.long	0x539f
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x6
	.secrel32	.LASF7
	.long	0x40ed
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x27
	.secrel32	.LASF43
	.byte	0xa
	.word	0x403
	.byte	0x32
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0xa
	.word	0x403
	.byte	0x41
	.long	0x40ed
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x35
	.long	0x4841
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.byte	0
	.uleb128 0x1f
	.long	0x1496
	.long	0x53be
	.quad	.LFB1767
	.quad	.LFE1767-.LFB1767
	.uleb128 0x1
	.byte	0x9c
	.long	0x5467
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x489b
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__p\0"
	.byte	0x7
	.word	0x188
	.byte	0x1d
	.long	0xde6
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0x7
	.word	0x188
	.byte	0x29
	.long	0x280
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.uleb128 0x17
	.long	0x50c9
	.quad	.LBB137
	.quad	.LBE137-.LBB137
	.byte	0x7
	.word	0x18c
	.byte	0x13
	.uleb128 0x3
	.long	0x50d2
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x3
	.long	0x50df
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x3
	.long	0x50ec
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.uleb128 0x17
	.long	0x4fbe
	.quad	.LBB139
	.quad	.LBE139-.LBB139
	.byte	0x8
	.word	0x289
	.byte	0x17
	.uleb128 0x3
	.long	0x4fcc
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.uleb128 0x3
	.long	0x4fd5
	.uleb128 0x2
	.byte	0x91
	.sleb128 -56
	.uleb128 0x3
	.long	0x4fe1
	.uleb128 0x2
	.byte	0x91
	.sleb128 -64
	.uleb128 0x3e
	.long	0x5e7e
	.quad	.LBB141
	.quad	.LBE141-.LBB141
	.byte	0x6
	.byte	0xd2
	.byte	0x22
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x1f
	.long	0x14fa
	.long	0x5486
	.quad	.LFB1766
	.quad	.LFE1766-.LFB1766
	.uleb128 0x1
	.byte	0x9c
	.long	0x54a3
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x489b
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0x7
	.word	0x193
	.byte	0x20
	.long	0x280
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0xd
	.long	0xeb6
	.long	0x54b1
	.byte	0x2
	.long	0x54c7
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x487d
	.uleb128 0x30
	.ascii "__a\0"
	.byte	0x7
	.byte	0x98
	.byte	0x25
	.long	0x4882
	.byte	0
	.uleb128 0x2f
	.long	0x54a3
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implC1ERKS1_\0"
	.long	0x5522
	.quad	.LFB1765
	.quad	.LFE1765-.LFB1765
	.uleb128 0x1
	.byte	0x9c
	.long	0x5585
	.uleb128 0x3
	.long	0x54b1
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x3
	.long	0x54ba
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x20
	.long	0x5585
	.quad	.LBB132
	.quad	.LBE132-.LBB132
	.byte	0x7
	.byte	0x99
	.byte	0x16
	.uleb128 0x3
	.long	0x5593
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x3
	.long	0x559c
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x20
	.long	0x521f
	.quad	.LBB135
	.quad	.LBE135-.LBB135
	.byte	0x6
	.byte	0xad
	.byte	0x22
	.uleb128 0x3
	.long	0x522d
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.uleb128 0x3
	.long	0x5236
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0xd
	.long	0x830
	.long	0x5593
	.byte	0x2
	.long	0x55a9
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x4837
	.uleb128 0x30
	.ascii "__a\0"
	.byte	0x6
	.byte	0xac
	.byte	0x22
	.long	0x483c
	.byte	0
	.uleb128 0x29
	.long	0x5585
	.ascii "_ZNSaI8ParticleEC1ERKS0_\0"
	.long	0x55cf
	.long	0x55da
	.uleb128 0xf
	.long	0x5593
	.uleb128 0xf
	.long	0x559c
	.byte	0
	.uleb128 0x29
	.long	0x5585
	.ascii "_ZNSaI8ParticleEC2ERKS0_\0"
	.long	0x5600
	.long	0x560b
	.uleb128 0xf
	.long	0x5593
	.uleb128 0xf
	.long	0x559c
	.byte	0
	.uleb128 0x1a
	.long	0x3051
	.quad	.LFB1758
	.quad	.LFE1758-.LFB1758
	.uleb128 0x1
	.byte	0x9c
	.long	0x5664
	.uleb128 0xe
	.ascii "__a\0"
	.byte	0x7
	.word	0x8ae
	.byte	0x29
	.long	0x48f0
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x28
	.ascii "__diffmax\0"
	.byte	0x7
	.word	0x8b3
	.byte	0xf
	.long	0x290
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x28
	.ascii "__allocmax\0"
	.byte	0x7
	.word	0x8b5
	.byte	0xf
	.long	0x290
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.byte	0
	.uleb128 0x3d
	.long	0x32c6
	.long	0x568c
	.quad	.LFB1757
	.quad	.LFE1757-.LFB1757
	.uleb128 0x1
	.byte	0x9c
	.long	0x56ab
	.uleb128 0x4
	.ascii "_Up\0"
	.long	0x47ad
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x48e1
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__ptr\0"
	.byte	0x7
	.word	0x8f8
	.byte	0x13
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x1e
	.long	0x3fa8
	.long	0x56e6
	.uleb128 0x6
	.secrel32	.LASF6
	.long	0x481e
	.uleb128 0x4
	.ascii "_Tp\0"
	.long	0x47ad
	.uleb128 0x19
	.secrel32	.LASF43
	.byte	0x8
	.word	0x412
	.byte	0x1f
	.long	0x481e
	.uleb128 0x19
	.secrel32	.LASF44
	.byte	0x8
	.word	0x412
	.byte	0x39
	.long	0x481e
	.uleb128 0x1
	.long	0x4841
	.byte	0
	.uleb128 0x3d
	.long	0x107b
	.long	0x5705
	.quad	.LFB1755
	.quad	.LFE1755-.LFB1755
	.uleb128 0x1
	.byte	0x9c
	.long	0x5712
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x489b
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x1f
	.long	0x2bfa
	.long	0x5731
	.quad	.LFB1754
	.quad	.LFE1754-.LFB1754
	.uleb128 0x1
	.byte	0x9c
	.long	0x574e
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x48b9
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0x7
	.word	0x7d8
	.byte	0x27
	.long	0x19c7
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0xd
	.long	0x13df
	.long	0x575c
	.byte	0x2
	.long	0x5766
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x489b
	.byte	0
	.uleb128 0x2f
	.long	0x574e
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EED2Ev\0"
	.long	0x57af
	.quad	.LFB1752
	.quad	.LFE1752-.LFB1752
	.uleb128 0x1
	.byte	0x9c
	.long	0x57b8
	.uleb128 0x3
	.long	0x575c
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0xd
	.long	0x1261
	.long	0x57c6
	.byte	0x2
	.long	0x57ea
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x489b
	.uleb128 0x14
	.ascii "__n\0"
	.byte	0x7
	.word	0x153
	.byte	0x1b
	.long	0x280
	.uleb128 0x14
	.ascii "__a\0"
	.byte	0x7
	.word	0x153
	.byte	0x36
	.long	0x48a5
	.byte	0
	.uleb128 0x2f
	.long	0x57b8
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EEC2EyRKS1_\0"
	.long	0x5838
	.quad	.LFB1749
	.quad	.LFE1749-.LFB1749
	.uleb128 0x1
	.byte	0x9c
	.long	0x5851
	.uleb128 0x3
	.long	0x57c6
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x3
	.long	0x57cf
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x3
	.long	0x57dc
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.byte	0
	.uleb128 0x7b
	.long	0x1018
	.byte	0x7
	.byte	0x8b
	.byte	0xe
	.long	0x5862
	.byte	0x2
	.long	0x586c
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x487d
	.byte	0
	.uleb128 0x4a
	.long	0x5851
	.ascii "_ZNSt12_Vector_baseI8ParticleSaIS0_EE12_Vector_implD1Ev\0"
	.long	0x58c3
	.quad	.LFB1748
	.quad	.LFE1748-.LFB1748
	.uleb128 0x1
	.byte	0x9c
	.long	0x58ed
	.uleb128 0x3
	.long	0x5862
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x20
	.long	0x5bf2
	.quad	.LBB126
	.quad	.LBE126-.LBB126
	.byte	0x7
	.byte	0x8b
	.byte	0xe
	.uleb128 0x3
	.long	0x5c00
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.byte	0
	.uleb128 0x1a
	.long	0x2ff0
	.quad	.LFB1744
	.quad	.LFE1744-.LFB1744
	.uleb128 0x1
	.byte	0x9c
	.long	0x599c
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0x7
	.word	0x8a5
	.byte	0x23
	.long	0x19c7
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__a\0"
	.byte	0x7
	.word	0x8a5
	.byte	0x3e
	.long	0x48be
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x49
	.long	0x5585
	.quad	.LBB118
	.quad	.LBE118-.LBB118
	.byte	0x7
	.word	0x8a7
	.byte	0x18
	.long	0x597c
	.uleb128 0xf
	.long	0x5593
	.uleb128 0x3
	.long	0x559c
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x20
	.long	0x521f
	.quad	.LBB121
	.quad	.LBE121-.LBB121
	.byte	0x6
	.byte	0xad
	.byte	0x22
	.uleb128 0x3
	.long	0x522d
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x3
	.long	0x5236
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.byte	0
	.uleb128 0x17
	.long	0x5bf2
	.quad	.LBB123
	.quad	.LBE123-.LBB123
	.byte	0x7
	.word	0x8a7
	.byte	0x18
	.uleb128 0xf
	.long	0x5c00
	.byte	0
	.byte	0
	.uleb128 0xd
	.long	0x5fd
	.long	0x59aa
	.byte	0x2
	.long	0x59b4
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x480f
	.byte	0
	.uleb128 0x29
	.long	0x599c
	.ascii "_ZNSt15__new_allocatorI8ParticleEC2Ev\0"
	.long	0x59e7
	.long	0x59ed
	.uleb128 0xf
	.long	0x59aa
	.byte	0
	.uleb128 0x1f
	.long	0x243f
	.long	0x5a0c
	.quad	.LFB1740
	.quad	.LFE1740-.LFB1740
	.uleb128 0x1
	.byte	0x9c
	.long	0x5a4c
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x48b9
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0x7
	.word	0x4ed
	.byte	0x1c
	.long	0x19c7
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x7c
	.ascii "__PRETTY_FUNCTION__\0"
	.long	0x5a5c
	.uleb128 0x9
	.byte	0x3
	.quad	.LC2
	.byte	0
	.uleb128 0x7d
	.long	0x4729
	.long	0x5a5c
	.uleb128 0x7e
	.long	0x40ed
	.byte	0xd1
	.byte	0
	.uleb128 0x5
	.long	0x5a4c
	.uleb128 0x3d
	.long	0x21e5
	.long	0x5a80
	.quad	.LFB1739
	.quad	.LFE1739-.LFB1739
	.uleb128 0x1
	.byte	0x9c
	.long	0x5a9f
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x48e1
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x28
	.ascii "__dif\0"
	.byte	0x7
	.word	0x45f
	.byte	0xc
	.long	0x402
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.uleb128 0x1f
	.long	0x26c3
	.long	0x5abe
	.quad	.LFB1738
	.quad	.LFE1738-.LFB1738
	.uleb128 0x1
	.byte	0x9c
	.long	0x5acb
	.uleb128 0x12
	.secrel32	.LASF47
	.long	0x48b9
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0xd
	.long	0x1c80
	.long	0x5ad9
	.byte	0x2
	.long	0x5ae3
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x48b9
	.byte	0
	.uleb128 0x2f
	.long	0x5acb
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EED1Ev\0"
	.long	0x5b25
	.quad	.LFB1737
	.quad	.LFE1737-.LFB1737
	.uleb128 0x1
	.byte	0x9c
	.long	0x5b60
	.uleb128 0x3
	.long	0x5ad9
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x17
	.long	0x56ab
	.quad	.LBB116
	.quad	.LBE116-.LBB116
	.byte	0x7
	.word	0x322
	.byte	0xf
	.uleb128 0x3
	.long	0x56c6
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x3
	.long	0x56d3
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x3
	.long	0x56e0
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.byte	0
	.uleb128 0xd
	.long	0x1980
	.long	0x5b6e
	.byte	0x2
	.long	0x5b92
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x48b9
	.uleb128 0x14
	.ascii "__n\0"
	.byte	0x7
	.word	0x24a
	.byte	0x18
	.long	0x19c7
	.uleb128 0x14
	.ascii "__a\0"
	.byte	0x7
	.word	0x24a
	.byte	0x33
	.long	0x48be
	.byte	0
	.uleb128 0x2f
	.long	0x5b60
	.ascii "_ZNSt6vectorI8ParticleSaIS0_EEC1EyRKS1_\0"
	.long	0x5bd9
	.quad	.LFB1734
	.quad	.LFE1734-.LFB1734
	.uleb128 0x1
	.byte	0x9c
	.long	0x5bf2
	.uleb128 0x3
	.long	0x5b6e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x3
	.long	0x5b77
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x3
	.long	0x5b84
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.byte	0
	.uleb128 0xd
	.long	0x89d
	.long	0x5c00
	.byte	0x2
	.long	0x5c0a
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x4837
	.byte	0
	.uleb128 0x29
	.long	0x5bf2
	.ascii "_ZNSaI8ParticleED1Ev\0"
	.long	0x5c2c
	.long	0x5c32
	.uleb128 0xf
	.long	0x5c00
	.byte	0
	.uleb128 0x29
	.long	0x5bf2
	.ascii "_ZNSaI8ParticleED2Ev\0"
	.long	0x5c54
	.long	0x5c5a
	.uleb128 0xf
	.long	0x5c00
	.byte	0
	.uleb128 0xd
	.long	0x804
	.long	0x5c68
	.byte	0x2
	.long	0x5c72
	.uleb128 0xc
	.secrel32	.LASF47
	.long	0x4837
	.byte	0
	.uleb128 0x29
	.long	0x5c5a
	.ascii "_ZNSaI8ParticleEC1Ev\0"
	.long	0x5c94
	.long	0x5c9a
	.uleb128 0xf
	.long	0x5c68
	.byte	0
	.uleb128 0x7f
	.ascii "main\0"
	.byte	0x4
	.byte	0x13
	.byte	0x5
	.long	0x4174
	.quad	.LFB1720
	.quad	.LFE1720-.LFB1720
	.uleb128 0x1
	.byte	0x9c
	.long	0x5d2f
	.uleb128 0x48
	.ascii "ps\0"
	.byte	0x4
	.byte	0x14
	.byte	0x1b
	.long	0x15f0
	.uleb128 0x3
	.byte	0x91
	.sleb128 -80
	.uleb128 0x80
	.long	0x5c5a
	.quad	.LBB106
	.quad	.LBE106-.LBB106
	.byte	0x4
	.byte	0x14
	.byte	0x22
	.long	0x5d10
	.uleb128 0xf
	.long	0x5c68
	.uleb128 0x20
	.long	0x599c
	.quad	.LBB109
	.quad	.LBE109-.LBB109
	.byte	0x6
	.byte	0xa8
	.byte	0x24
	.uleb128 0x3
	.long	0x59aa
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.byte	0
	.byte	0
	.uleb128 0x20
	.long	0x5bf2
	.quad	.LBB111
	.quad	.LBE111-.LBB111
	.byte	0x4
	.byte	0x14
	.byte	0x22
	.uleb128 0xf
	.long	0x5c00
	.byte	0
	.byte	0
	.uleb128 0x81
	.ascii "integrate_aos\0"
	.byte	0x4
	.byte	0xd
	.byte	0x6
	.ascii "_Z13integrate_aosP8Particleif\0"
	.quad	.LFB1719
	.quad	.LFE1719-.LFB1719
	.uleb128 0x1
	.byte	0x9c
	.long	0x5dbe
	.uleb128 0x16
	.ascii "p\0"
	.byte	0x4
	.byte	0xd
	.byte	0x1e
	.long	0x481e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x16
	.ascii "n\0"
	.byte	0x4
	.byte	0xd
	.byte	0x25
	.long	0x4174
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x16
	.ascii "dt\0"
	.byte	0x4
	.byte	0xd
	.byte	0x2e
	.long	0x46b4
	.uleb128 0x2
	.byte	0x91
	.sleb128 16
	.uleb128 0x5c
	.quad	.LBB105
	.quad	.LBE105-.LBB105
	.uleb128 0x48
	.ascii "i\0"
	.byte	0x4
	.byte	0xe
	.byte	0xe
	.long	0x4174
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.byte	0
	.byte	0
	.uleb128 0x3b
	.long	0x401b
	.quad	.LFB564
	.quad	.LFE564-.LFB564
	.uleb128 0x1
	.byte	0x9c
	.long	0x5dea
	.uleb128 0xe
	.ascii "__n\0"
	.byte	0x3
	.word	0x404
	.byte	0x28
	.long	0x40ed
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x82
	.secrel32	.LASF41
	.byte	0x2
	.byte	0xd9
	.byte	0xd
	.ascii "_ZdlPvS_\0"
	.quad	.LFB222
	.quad	.LFE222-.LFB222
	.uleb128 0x1
	.byte	0x9c
	.long	0x5e23
	.uleb128 0x35
	.long	0x4734
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x35
	.long	0x4734
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x83
	.secrel32	.LASF42
	.byte	0x2
	.byte	0xce
	.byte	0x7
	.ascii "_ZnwyPv\0"
	.long	0x4734
	.quad	.LFB220
	.quad	.LFE220-.LFB220
	.uleb128 0x1
	.byte	0x9c
	.long	0x5e66
	.uleb128 0x35
	.long	0x280
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x16
	.ascii "__p\0"
	.byte	0x2
	.byte	0xce
	.byte	0x27
	.long	0x4734
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x84
	.long	0x4059
	.quad	.LFB15
	.quad	.LFE15-.LFB15
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x85
	.long	0x4095
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
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
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
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7
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
	.uleb128 0x9
	.uleb128 0x10
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xa
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
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
	.uleb128 0xc
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
	.uleb128 0xd
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
	.uleb128 0xe
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
	.uleb128 0xf
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x10
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
	.uleb128 0x11
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
	.uleb128 0x12
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
	.uleb128 0x13
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
	.uleb128 0x14
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
	.uleb128 0x15
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
	.uleb128 0x16
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
	.uleb128 0x17
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
	.uleb128 0x19
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
	.uleb128 0x1a
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
	.uleb128 0x1b
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
	.uleb128 0x1c
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
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
	.uleb128 0x1d
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
	.sleb128 1
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1e
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
	.uleb128 0x1f
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
	.uleb128 0x20
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
	.uleb128 0x21
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
	.byte	0
	.byte	0
	.uleb128 0x22
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
	.uleb128 0x23
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
	.uleb128 0x24
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
	.uleb128 0x25
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
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x26
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
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x27
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
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x28
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
	.uleb128 0x29
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
	.uleb128 0x2c
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
	.uleb128 0x2d
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
	.uleb128 0x2e
	.uleb128 0x42
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2f
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
	.uleb128 0x33
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
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x34
	.uleb128 0x2e
	.byte	0
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 26
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
	.uleb128 0x35
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x36
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
	.uleb128 0x37
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
	.uleb128 0x38
	.uleb128 0x2
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x39
	.uleb128 0x4107
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.byte	0
	.byte	0
	.uleb128 0x3a
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
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3b
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
	.uleb128 0x3c
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
	.uleb128 0x3d
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
	.uleb128 0x3e
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
	.uleb128 0x3f
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
	.uleb128 0x40
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
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x41
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
	.uleb128 0x42
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
	.uleb128 0x43
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
	.uleb128 0x44
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
	.uleb128 0x45
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
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x46
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 23
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
	.uleb128 0x47
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
	.sleb128 5
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x48
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
	.uleb128 0x49
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
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4a
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
	.uleb128 0x4b
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 28
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
	.uleb128 0x4c
	.uleb128 0x30
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1c
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x4d
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
	.uleb128 0x4e
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
	.uleb128 0x4f
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
	.uleb128 0x50
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
	.uleb128 0x51
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
	.uleb128 0x52
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
	.uleb128 0x53
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
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x54
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
	.uleb128 0x55
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
	.uleb128 0x63
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x56
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 7
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
	.uleb128 0x57
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
	.uleb128 0x58
	.uleb128 0x2e
	.byte	0
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
	.sleb128 3
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x87
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x59
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
	.uleb128 0x5a
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 6
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x5b
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
	.uleb128 0x5c
	.uleb128 0xb
	.byte	0x1
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.byte	0
	.byte	0
	.uleb128 0x5d
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
	.uleb128 0x5e
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
	.uleb128 0x5f
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
	.uleb128 0x60
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
	.uleb128 0x61
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
	.uleb128 0x62
	.uleb128 0x13
	.byte	0
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
	.byte	0
	.byte	0
	.uleb128 0x63
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
	.uleb128 0x64
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
	.byte	0
	.byte	0
	.uleb128 0x65
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
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x66
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
	.uleb128 0x67
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
	.uleb128 0x68
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
	.byte	0
	.byte	0
	.uleb128 0x69
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
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x6a
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
	.uleb128 0x6b
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
	.uleb128 0x6c
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.byte	0
	.byte	0
	.uleb128 0x6d
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
	.uleb128 0x6f
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
	.byte	0
	.byte	0
	.uleb128 0x70
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
	.uleb128 0x71
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
	.uleb128 0x72
	.uleb128 0x26
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x73
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x74
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
	.uleb128 0x75
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
	.uleb128 0x76
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
	.uleb128 0x77
	.uleb128 0xb
	.byte	0x1
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x78
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
	.uleb128 0x79
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
	.uleb128 0x7a
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
	.uleb128 0x7b
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
	.uleb128 0x7c
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
	.uleb128 0x7d
	.uleb128 0x1
	.byte	0x1
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7e
	.uleb128 0x21
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2f
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x7f
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
	.uleb128 0x80
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
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x81
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
	.uleb128 0x7a
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x82
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
	.uleb128 0x83
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
	.uleb128 0x84
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
	.uleb128 0x85
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
	.long	0x27c
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
	.quad	.LFB564
	.quad	.LFE564-.LFB564
	.quad	.LFB1734
	.quad	.LFE1734-.LFB1734
	.quad	.LFB1737
	.quad	.LFE1737-.LFB1737
	.quad	.LFB1738
	.quad	.LFE1738-.LFB1738
	.quad	.LFB1739
	.quad	.LFE1739-.LFB1739
	.quad	.LFB1740
	.quad	.LFE1740-.LFB1740
	.quad	.LFB1744
	.quad	.LFE1744-.LFB1744
	.quad	.LFB1748
	.quad	.LFE1748-.LFB1748
	.quad	.LFB1749
	.quad	.LFE1749-.LFB1749
	.quad	.LFB1752
	.quad	.LFE1752-.LFB1752
	.quad	.LFB1754
	.quad	.LFE1754-.LFB1754
	.quad	.LFB1755
	.quad	.LFE1755-.LFB1755
	.quad	.LFB1757
	.quad	.LFE1757-.LFB1757
	.quad	.LFB1758
	.quad	.LFE1758-.LFB1758
	.quad	.LFB1765
	.quad	.LFE1765-.LFB1765
	.quad	.LFB1766
	.quad	.LFE1766-.LFB1766
	.quad	.LFB1767
	.quad	.LFE1767-.LFB1767
	.quad	.LFB1768
	.quad	.LFE1768-.LFB1768
	.quad	.LFB1769
	.quad	.LFE1769-.LFB1769
	.quad	.LFB1771
	.quad	.LFE1771-.LFB1771
	.quad	.LFB1776
	.quad	.LFE1776-.LFB1776
	.quad	.LFB1778
	.quad	.LFE1778-.LFB1778
	.quad	.LFB1780
	.quad	.LFE1780-.LFB1780
	.quad	.LFB1782
	.quad	.LFE1782-.LFB1782
	.quad	.LFB1788
	.quad	.LFE1788-.LFB1788
	.quad	.LFB1785
	.quad	.LFE1785-.LFB1785
	.quad	.LFB1789
	.quad	.LFE1789-.LFB1789
	.quad	.LFB1791
	.quad	.LFE1791-.LFB1791
	.quad	.LFB1794
	.quad	.LFE1794-.LFB1794
	.quad	.LFB1795
	.quad	.LFE1795-.LFB1795
	.quad	.LFB1796
	.quad	.LFE1796-.LFB1796
	.quad	.LFB1798
	.quad	.LFE1798-.LFB1798
	.quad	.LFB1799
	.quad	.LFE1799-.LFB1799
	.quad	.LFB1804
	.quad	.LFE1804-.LFB1804
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
	.quad	.LFB564
	.uleb128 .LFE564-.LFB564
	.byte	0x7
	.quad	.LFB1734
	.uleb128 .LFE1734-.LFB1734
	.byte	0x7
	.quad	.LFB1737
	.uleb128 .LFE1737-.LFB1737
	.byte	0x7
	.quad	.LFB1738
	.uleb128 .LFE1738-.LFB1738
	.byte	0x7
	.quad	.LFB1739
	.uleb128 .LFE1739-.LFB1739
	.byte	0x7
	.quad	.LFB1740
	.uleb128 .LFE1740-.LFB1740
	.byte	0x7
	.quad	.LFB1744
	.uleb128 .LFE1744-.LFB1744
	.byte	0x7
	.quad	.LFB1748
	.uleb128 .LFE1748-.LFB1748
	.byte	0x7
	.quad	.LFB1749
	.uleb128 .LFE1749-.LFB1749
	.byte	0x7
	.quad	.LFB1752
	.uleb128 .LFE1752-.LFB1752
	.byte	0x7
	.quad	.LFB1754
	.uleb128 .LFE1754-.LFB1754
	.byte	0x7
	.quad	.LFB1755
	.uleb128 .LFE1755-.LFB1755
	.byte	0x7
	.quad	.LFB1757
	.uleb128 .LFE1757-.LFB1757
	.byte	0x7
	.quad	.LFB1758
	.uleb128 .LFE1758-.LFB1758
	.byte	0x7
	.quad	.LFB1765
	.uleb128 .LFE1765-.LFB1765
	.byte	0x7
	.quad	.LFB1766
	.uleb128 .LFE1766-.LFB1766
	.byte	0x7
	.quad	.LFB1767
	.uleb128 .LFE1767-.LFB1767
	.byte	0x7
	.quad	.LFB1768
	.uleb128 .LFE1768-.LFB1768
	.byte	0x7
	.quad	.LFB1769
	.uleb128 .LFE1769-.LFB1769
	.byte	0x7
	.quad	.LFB1771
	.uleb128 .LFE1771-.LFB1771
	.byte	0x7
	.quad	.LFB1776
	.uleb128 .LFE1776-.LFB1776
	.byte	0x7
	.quad	.LFB1778
	.uleb128 .LFE1778-.LFB1778
	.byte	0x7
	.quad	.LFB1780
	.uleb128 .LFE1780-.LFB1780
	.byte	0x7
	.quad	.LFB1782
	.uleb128 .LFE1782-.LFB1782
	.byte	0x7
	.quad	.LFB1788
	.uleb128 .LFE1788-.LFB1788
	.byte	0x7
	.quad	.LFB1785
	.uleb128 .LFE1785-.LFB1785
	.byte	0x7
	.quad	.LFB1789
	.uleb128 .LFE1789-.LFB1789
	.byte	0x7
	.quad	.LFB1791
	.uleb128 .LFE1791-.LFB1791
	.byte	0x7
	.quad	.LFB1794
	.uleb128 .LFE1794-.LFB1794
	.byte	0x7
	.quad	.LFB1795
	.uleb128 .LFE1795-.LFB1795
	.byte	0x7
	.quad	.LFB1796
	.uleb128 .LFE1796-.LFB1796
	.byte	0x7
	.quad	.LFB1798
	.uleb128 .LFE1798-.LFB1798
	.byte	0x7
	.quad	.LFB1799
	.uleb128 .LFE1799-.LFB1799
	.byte	0x7
	.quad	.LFB1804
	.uleb128 .LFE1804-.LFB1804
	.byte	0
.Ldebug_ranges3:
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
.LASF17:
	.ascii "size_type\0"
.LASF29:
	.ascii "const_iterator\0"
.LASF45:
	.ascii "__value\0"
.LASF37:
	.ascii "initializer_list\0"
.LASF12:
	.ascii "allocator\0"
.LASF9:
	.ascii "__uninit_default_n<Particle*, long long unsigned int>\0"
.LASF39:
	.ascii "_OutputIterator\0"
.LASF23:
	.ascii "_Vector_base\0"
.LASF27:
	.ascii "vector\0"
.LASF35:
	.ascii "_M_erase\0"
.LASF36:
	.ascii "_M_move_assign\0"
.LASF43:
	.ascii "__first\0"
.LASF33:
	.ascii "push_back\0"
.LASF38:
	.ascii "_UninitDestroyGuard\0"
.LASF7:
	.ascii "_Size\0"
.LASF8:
	.ascii "_TrivialValueType\0"
.LASF11:
	.ascii "deallocate\0"
.LASF26:
	.ascii "_S_do_relocate\0"
.LASF21:
	.ascii "_Tp_alloc_type\0"
.LASF13:
	.ascii "operator=\0"
.LASF10:
	.ascii "__new_allocator\0"
.LASF14:
	.ascii "allocate\0"
.LASF31:
	.ascii "operator[]\0"
.LASF5:
	.ascii "__bool_constant\0"
.LASF34:
	.ascii "insert\0"
.LASF3:
	.ascii "value_type\0"
.LASF32:
	.ascii "const_reference\0"
.LASF25:
	.ascii "_S_nothrow_relocate\0"
.LASF41:
	.ascii "operator delete\0"
.LASF28:
	.ascii "iterator\0"
.LASF22:
	.ascii "_M_get_Tp_allocator\0"
.LASF30:
	.ascii "reference\0"
.LASF15:
	.ascii "pointer\0"
.LASF18:
	.ascii "max_size\0"
.LASF2:
	.ascii "operator()\0"
.LASF4:
	.ascii "__detail\0"
.LASF20:
	.ascii "_Vector_impl\0"
.LASF44:
	.ascii "__last\0"
.LASF24:
	.ascii "_Alloc\0"
.LASF42:
	.ascii "operator new\0"
.LASF6:
	.ascii "_ForwardIterator\0"
.LASF47:
	.ascii "this\0"
.LASF46:
	.ascii "__location\0"
.LASF40:
	.ascii "_Args\0"
.LASF16:
	.ascii "allocator_type\0"
.LASF19:
	.ascii "_Vector_impl_data\0"
	.section	.debug_line_str,"dr"
.LASF1:
	.ascii "C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible\0"
.LASF0:
	.ascii "Examples\\_ch142_aos.cpp\0"
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
