	.file	"_ch147_asm.cpp"
	.intel_syntax noprefix
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "C:/CodeLearnling/note/note/C++/CPP-Bible" "Examples/_ch147_asm.cpp"
	.section	.text$_ZNSt12__mutex_baseC2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12__mutex_baseC2Ev
	.def	_ZNSt12__mutex_baseC2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12__mutex_baseC2Ev
_ZNSt12__mutex_baseC2Ev:
.LFB1282:
	.file 1 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/std_mutex.h"
	.loc 1 73 5
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
.LBB28:
	.loc 1 76 36
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB29:
.LBB30:
.LBB31:
.LBB32:
	.file 2 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/x86_64-w64-mingw32/bits/gthr-default.h"
	.loc 2 348 10
	mov	eax, 1
.LBE32:
.LBE31:
	.loc 2 778 26 discriminator 1
	test	eax, eax
	setne	al
	.loc 2 778 3 discriminator 1
	test	al, al
	je	.L5
	.loc 2 779 34
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, 0
	mov	rcx, rax
	call	pthread_mutex_init
.L5:
	.loc 2 780 1
	nop
.LBE30:
.LBE29:
.LBE28:
	.loc 1 77 5
	nop
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1282:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1282:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1282-.LLSDACSB1282
.LLSDACSB1282:
.LLSDACSE1282:
	.section	.text$_ZNSt12__mutex_baseC2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt12__mutex_baseD2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt12__mutex_baseD2Ev
	.def	_ZNSt12__mutex_baseD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12__mutex_baseD2Ev
_ZNSt12__mutex_baseD2Ev:
.LFB1285:
	.loc 1 79 5
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
.LBB33:
	.loc 1 79 55
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB34:
.LBB35:
.LBB36:
.LBB37:
	.loc 2 348 10
	mov	eax, 1
.LBE37:
.LBE36:
	.loc 2 785 26 discriminator 1
	test	eax, eax
	setne	al
	.loc 2 785 3 discriminator 1
	test	al, al
	je	.L10
	.loc 2 786 44
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	pthread_mutex_destroy
	.loc 2 786 52
	jmp	.L9
.L10:
	.loc 2 788 12
	nop
.L9:
.LBE35:
.LBE34:
.LBE33:
	.loc 1 79 68
	nop
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1285:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1285:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1285-.LLSDACSB1285
.LLSDACSB1285:
.LLSDACSE1285:
	.section	.text$_ZNSt12__mutex_baseD2Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt5mutex4lockEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt5mutex4lockEv
	.def	_ZNSt5mutex4lockEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt5mutex4lockEv
_ZNSt5mutex4lockEv:
.LFB1287:
	.loc 1 113 5
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
	.loc 1 115 37
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -16[rbp], rax
.LBB38:
.LBB39:
.LBB40:
.LBB41:
	.loc 2 348 10
	mov	eax, 1
.LBE41:
.LBE40:
	.loc 2 794 26 discriminator 1
	test	eax, eax
	setne	al
	.loc 2 794 3 discriminator 1
	test	al, al
	je	.L13
	.loc 2 795 41
	mov	rax, QWORD PTR -16[rbp]
	mov	rcx, rax
	call	pthread_mutex_lock
	.loc 2 795 49
	jmp	.L14
.L13:
	.loc 2 797 12
	mov	eax, 0
.L14:
.LBE39:
.LBE38:
	.loc 1 115 37 discriminator 1
	mov	DWORD PTR -4[rbp], eax
	.loc 1 118 7
	cmp	DWORD PTR -4[rbp], 0
	je	.L16
	.loc 1 119 22
	mov	eax, DWORD PTR -4[rbp]
	mov	ecx, eax
	call	_ZSt20__throw_system_errori
.L16:
	.loc 1 120 5
	nop
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1287:
	.seh_endproc
	.section	.text$_ZNSt5mutex6unlockEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt5mutex6unlockEv
	.def	_ZNSt5mutex6unlockEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt5mutex6unlockEv
_ZNSt5mutex6unlockEv:
.LFB1289:
	.loc 1 131 5
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
	.loc 1 134 29
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
.LBB42:
.LBB43:
.LBB44:
.LBB45:
	.loc 2 348 10
	mov	eax, 1
.LBE45:
.LBE44:
	.loc 2 824 26 discriminator 1
	test	eax, eax
	setne	al
	.loc 2 824 3 discriminator 1
	test	al, al
	je	.L21
	.loc 2 825 43
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	pthread_mutex_unlock
	.loc 2 825 51
	jmp	.L20
.L21:
	.loc 2 827 12
	nop
.L20:
.LBE43:
.LBE42:
	.loc 1 135 5
	nop
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1289:
	.seh_endproc
	.section	.text$_ZNSt5mutexC1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt5mutexC1Ev
	.def	_ZNSt5mutexC1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt5mutexC1Ev
_ZNSt5mutexC1Ev:
.LFB1380:
	.loc 1 106 5
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
.LBB46:
	.loc 1 106 5
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12__mutex_baseC2Ev
.LBE46:
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1380:
	.seh_endproc
	.globl	g_mtx
	.bss
	.align 8
g_mtx:
	.space 8
	.text
	.globl	_Z16critical_sectionv
	.def	_Z16critical_sectionv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16critical_sectionv
_Z16critical_sectionv:
.LFB1381:
	.file 3 "Examples/_ch147_asm.cpp"
	.loc 3 8 25
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
	.loc 3 9 41
	lea	rdx, g_mtx[rip]
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZNSt10lock_guardISt5mutexEC1ERS0_
	.loc 3 11 1
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZNSt10lock_guardISt5mutexED1Ev
	nop
	add	rsp, 48
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1381:
	.seh_endproc
	.section	.text$_ZNSt10lock_guardISt5mutexEC1ERS0_,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt10lock_guardISt5mutexEC1ERS0_
	.def	_ZNSt10lock_guardISt5mutexEC1ERS0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10lock_guardISt5mutexEC1ERS0_
_ZNSt10lock_guardISt5mutexEC1ERS0_:
.LFB1415:
	.loc 1 251 16
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
.LBB47:
	.loc 1 251 46
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR [rax], rdx
	.loc 1 252 9
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 1 252 23
	mov	rcx, rax
	call	_ZNSt5mutex4lockEv
.LBE47:
	.loc 1 252 27
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1415:
	.seh_endproc
	.section	.text$_ZNSt10lock_guardISt5mutexED1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt10lock_guardISt5mutexED1Ev
	.def	_ZNSt10lock_guardISt5mutexED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10lock_guardISt5mutexED1Ev
_ZNSt10lock_guardISt5mutexED1Ev:
.LFB1418:
	.loc 1 258 7
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
.LBB48:
	.loc 1 259 9
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	.loc 1 259 25
	mov	rcx, rax
	call	_ZNSt5mutex6unlockEv
.LBE48:
	.loc 1 259 29
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1418:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1418:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1418-.LLSDACSB1418
.LLSDACSB1418:
.LLSDACSE1418:
	.section	.text$_ZNSt10lock_guardISt5mutexED1Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt5mutexD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZNSt5mutexD1Ev
	.def	_ZNSt5mutexD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt5mutexD1Ev
_ZNSt5mutexD1Ev:
.LFB1439:
	.loc 1 107 5
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
.LBB49:
	.loc 1 107 5
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNSt12__mutex_baseD2Ev
.LBE49:
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1439:
	.seh_endproc
	.text
	.def	__tcfg_mtx;	.scl	3;	.type	32;	.endef
	.seh_proc	__tcfg_mtx
__tcfg_mtx:
.LFB1440:
	.loc 3 6 12
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
	.loc 3 6 12
	lea	rax, g_mtx[rip]
	mov	rcx, rax
	call	_ZNSt5mutexD1Ev
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1440:
	.seh_endproc
	.def	_Z41__static_initialization_and_destruction_0v;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z41__static_initialization_and_destruction_0v
_Z41__static_initialization_and_destruction_0v:
.LFB1436:
	.loc 3 11 1
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
	.loc 3 6 12
	lea	rax, g_mtx[rip]
	mov	rcx, rax
	call	_ZNSt5mutexC1Ev
	.loc 3 6 12 is_stmt 0 discriminator 1
	lea	rax, __tcfg_mtx[rip]
	mov	rcx, rax
	call	atexit
	.loc 3 11 1 is_stmt 1
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1436:
	.seh_endproc
	.def	_GLOBAL__sub_I_g_mtx;	.scl	3;	.type	32;	.endef
	.seh_proc	_GLOBAL__sub_I_g_mtx
_GLOBAL__sub_I_g_mtx:
.LFB1441:
	.loc 3 11 1
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
	.loc 3 11 1
	call	_Z41__static_initialization_and_destruction_0v
	nop
	add	rsp, 32
	pop	rbp
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1441:
	.seh_endproc
	.section	.ctors,"w"
	.align 8
	.quad	_GLOBAL__sub_I_g_mtx
	.text
.Letext0:
	.file 4 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/type_traits"
	.file 5 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/x86_64-w64-mingw32/bits/c++config.h"
	.file 6 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/utility.h"
	.file 7 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/concepts"
	.file 8 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/iterator_concepts.h"
	.file 9 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/compare"
	.file 10 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/numbers"
	.file 11 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/cstdint"
	.file 12 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/ctime"
	.file 13 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/chrono.h"
	.file 14 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/corecrt.h"
	.file 15 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/stdint.h"
	.file 16 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/time.h"
	.file 17 "C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/functexcept.h"
	.file 18 "C:/Qt/Tools/mingw1530_64/x86_64-w64-mingw32/include/pthread.h"
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0x1425
	.word	0x5
	.byte	0x1
	.byte	0x8
	.secrel32	.Ldebug_abbrev0
	.uleb128 0x22
	.ascii "GNU C++23 15.3.0 -masm=intel -mtune=generic -march=x86-64 -g -O0 -std=c++23\0"
	.byte	0x21
	.byte	0x4
	.long	0x3163e
	.secrel32	.LASF0
	.secrel32	.LASF1
	.secrel32	.LLRL0
	.quad	0
	.secrel32	.Ldebug_line0
	.uleb128 0x1b
	.ascii "std\0"
	.byte	0x5
	.word	0x150
	.byte	0xb
	.long	0x798
	.uleb128 0xb
	.ascii "__swappable_details\0"
	.byte	0x4
	.word	0xb93
	.byte	0xd
	.uleb128 0xb
	.ascii "__swappable_with_details\0"
	.byte	0x4
	.word	0xbe8
	.byte	0xd
	.uleb128 0x1b
	.ascii "ranges\0"
	.byte	0x6
	.word	0x113
	.byte	0xd
	.long	0x110
	.uleb128 0xf
	.ascii "__swap\0"
	.byte	0x7
	.byte	0xbf
	.byte	0xf
	.uleb128 0x23
	.ascii "_Cpo\0"
	.byte	0x7
	.byte	0xfc
	.byte	0x16
	.uleb128 0xf
	.ascii "__imove\0"
	.byte	0x8
	.byte	0x6b
	.byte	0xf
	.uleb128 0xb
	.ascii "__iswap\0"
	.byte	0x8
	.word	0x37b
	.byte	0xd
	.uleb128 0xb
	.ascii "__access\0"
	.byte	0x8
	.word	0x3fd
	.byte	0x15
	.uleb128 0x24
	.secrel32	.LASF2
	.byte	0x6
	.word	0x113
	.byte	0x15
	.byte	0
	.uleb128 0xf
	.ascii "__cmp_cat\0"
	.byte	0x9
	.byte	0x34
	.byte	0xd
	.uleb128 0x25
	.secrel32	.LASF2
	.byte	0x4
	.byte	0xad
	.byte	0xd
	.uleb128 0xb
	.ascii "__compare\0"
	.byte	0x9
	.word	0x23e
	.byte	0xd
	.uleb128 0x14
	.ascii "_Cpo\0"
	.byte	0x9
	.word	0x4ab
	.byte	0x14
	.uleb128 0xf
	.ascii "numbers\0"
	.byte	0xa
	.byte	0x38
	.byte	0xb
	.uleb128 0x1
	.byte	0xb
	.byte	0x35
	.long	0x958
	.uleb128 0x1
	.byte	0xb
	.byte	0x36
	.long	0x977
	.uleb128 0x1
	.byte	0xb
	.byte	0x37
	.long	0x998
	.uleb128 0x1
	.byte	0xb
	.byte	0x38
	.long	0x9b9
	.uleb128 0x1
	.byte	0xb
	.byte	0x3a
	.long	0xa8c
	.uleb128 0x1
	.byte	0xb
	.byte	0x3b
	.long	0xab5
	.uleb128 0x1
	.byte	0xb
	.byte	0x3c
	.long	0xae0
	.uleb128 0x1
	.byte	0xb
	.byte	0x3d
	.long	0xb0b
	.uleb128 0x1
	.byte	0xb
	.byte	0x3f
	.long	0x9da
	.uleb128 0x1
	.byte	0xb
	.byte	0x40
	.long	0xa05
	.uleb128 0x1
	.byte	0xb
	.byte	0x41
	.long	0xa32
	.uleb128 0x1
	.byte	0xb
	.byte	0x42
	.long	0xa5f
	.uleb128 0x1
	.byte	0xb
	.byte	0x44
	.long	0xb36
	.uleb128 0x1
	.byte	0xb
	.byte	0x45
	.long	0x909
	.uleb128 0x1
	.byte	0xb
	.byte	0x47
	.long	0x967
	.uleb128 0x1
	.byte	0xb
	.byte	0x48
	.long	0x987
	.uleb128 0x1
	.byte	0xb
	.byte	0x49
	.long	0x9a8
	.uleb128 0x1
	.byte	0xb
	.byte	0x4a
	.long	0x9c9
	.uleb128 0x1
	.byte	0xb
	.byte	0x4c
	.long	0xaa0
	.uleb128 0x1
	.byte	0xb
	.byte	0x4d
	.long	0xaca
	.uleb128 0x1
	.byte	0xb
	.byte	0x4e
	.long	0xaf5
	.uleb128 0x1
	.byte	0xb
	.byte	0x4f
	.long	0xb20
	.uleb128 0x1
	.byte	0xb
	.byte	0x51
	.long	0x9ef
	.uleb128 0x1
	.byte	0xb
	.byte	0x52
	.long	0xa1b
	.uleb128 0x1
	.byte	0xb
	.byte	0x53
	.long	0xa48
	.uleb128 0x1
	.byte	0xb
	.byte	0x54
	.long	0xa75
	.uleb128 0x1
	.byte	0xb
	.byte	0x56
	.long	0xb47
	.uleb128 0x1
	.byte	0xb
	.byte	0x57
	.long	0x91a
	.uleb128 0x1
	.byte	0xc
	.byte	0x3e
	.long	0xb67
	.uleb128 0x1
	.byte	0xc
	.byte	0x3f
	.long	0x93f
	.uleb128 0x1
	.byte	0xc
	.byte	0x40
	.long	0xb77
	.uleb128 0x1
	.byte	0xc
	.byte	0x42
	.long	0xc0e
	.uleb128 0x1
	.byte	0xc
	.byte	0x43
	.long	0xc1c
	.uleb128 0x1
	.byte	0xc
	.byte	0x44
	.long	0xc47
	.uleb128 0x1
	.byte	0xc
	.byte	0x45
	.long	0xc6f
	.uleb128 0x1
	.byte	0xc
	.byte	0x46
	.long	0xc92
	.uleb128 0x1
	.byte	0xc
	.byte	0x47
	.long	0xcb1
	.uleb128 0x1
	.byte	0xc
	.byte	0x48
	.long	0xcd7
	.uleb128 0x1
	.byte	0xc
	.byte	0x49
	.long	0xcfa
	.uleb128 0x26
	.ascii "chrono\0"
	.byte	0xd
	.byte	0x3d
	.byte	0xd
	.long	0x27e
	.uleb128 0x14
	.ascii "_V2\0"
	.byte	0xd
	.word	0x4c6
	.byte	0x1
	.uleb128 0x27
	.byte	0xd
	.word	0x5aa
	.byte	0x1f
	.long	0x290
	.byte	0
	.uleb128 0x28
	.ascii "literals\0"
	.byte	0xd
	.word	0x534
	.byte	0x14
	.long	0x2a6
	.uleb128 0x14
	.ascii "chrono_literals\0"
	.byte	0xd
	.word	0x54e
	.byte	0x14
	.byte	0
	.uleb128 0xf
	.ascii "filesystem\0"
	.byte	0xd
	.byte	0x3a
	.byte	0xd
	.uleb128 0x29
	.secrel32	.LASF3
	.byte	0x8
	.byte	0x1
	.byte	0x3d
	.byte	0x9
	.long	0x3bf
	.uleb128 0x15
	.ascii "__native_type\0"
	.byte	0x40
	.byte	0x21
	.long	0xd5b
	.byte	0x2
	.uleb128 0x2a
	.ascii "_M_mutex\0"
	.byte	0x1
	.byte	0x47
	.byte	0x14
	.long	0x2c2
	.byte	0
	.byte	0x2
	.uleb128 0x1c
	.secrel32	.LASF3
	.byte	0x49
	.byte	0x5
	.ascii "_ZNSt12__mutex_baseC4Ev\0"
	.byte	0x2
	.long	0x313
	.long	0x319
	.uleb128 0x5
	.long	0xd75
	.byte	0
	.uleb128 0x16
	.ascii "~__mutex_base\0"
	.byte	0x4f
	.ascii "_ZNSt12__mutex_baseD4Ev\0"
	.byte	0x2
	.long	0x34a
	.long	0x350
	.uleb128 0x5
	.long	0xd75
	.byte	0
	.uleb128 0x2b
	.secrel32	.LASF3
	.byte	0x1
	.byte	0x52
	.byte	0x5
	.ascii "_ZNSt12__mutex_baseC4ERKS_\0"
	.byte	0x2
	.long	0x37c
	.long	0x387
	.uleb128 0x5
	.long	0xd75
	.uleb128 0x4
	.long	0xd7f
	.byte	0
	.uleb128 0x2c
	.secrel32	.LASF4
	.byte	0x1
	.byte	0x53
	.byte	0x13
	.ascii "_ZNSt12__mutex_baseaSERKS_\0"
	.long	0xd84
	.byte	0x2
	.long	0x3b3
	.uleb128 0x5
	.long	0xd75
	.uleb128 0x4
	.long	0xd7f
	.byte	0
	.byte	0
	.uleb128 0x8
	.long	0x2b5
	.uleb128 0x1d
	.ascii "mutex\0"
	.byte	0x62
	.byte	0x9
	.long	0x56f
	.uleb128 0x2d
	.long	0x2b5
	.byte	0
	.uleb128 0x1e
	.ascii "mutex\0"
	.byte	0x6a
	.ascii "_ZNSt5mutexC4Ev\0"
	.long	0x3f7
	.long	0x3fd
	.uleb128 0x5
	.long	0xd89
	.byte	0
	.uleb128 0x1e
	.ascii "~mutex\0"
	.byte	0x6b
	.ascii "_ZNSt5mutexD4Ev\0"
	.long	0x41e
	.long	0x424
	.uleb128 0x5
	.long	0xd89
	.byte	0
	.uleb128 0x2e
	.ascii "mutex\0"
	.byte	0x1
	.byte	0x6d
	.byte	0x5
	.ascii "_ZNSt5mutexC4ERKS_\0"
	.byte	0x1
	.long	0x44a
	.long	0x455
	.uleb128 0x5
	.long	0xd89
	.uleb128 0x4
	.long	0xd93
	.byte	0
	.uleb128 0x2f
	.secrel32	.LASF4
	.byte	0x1
	.byte	0x6e
	.byte	0xc
	.ascii "_ZNSt5mutexaSERKS_\0"
	.long	0xd98
	.byte	0x1
	.long	0x47d
	.long	0x488
	.uleb128 0x5
	.long	0xd89
	.uleb128 0x4
	.long	0xd93
	.byte	0
	.uleb128 0x16
	.ascii "lock\0"
	.byte	0x71
	.ascii "_ZNSt5mutex4lockEv\0"
	.byte	0x1
	.long	0x4ab
	.long	0x4b1
	.uleb128 0x5
	.long	0xd89
	.byte	0
	.uleb128 0x30
	.ascii "try_lock\0"
	.byte	0x1
	.byte	0x7c
	.byte	0x5
	.ascii "_ZNSt5mutex8try_lockEv\0"
	.long	0x798
	.byte	0x1
	.long	0x4e2
	.long	0x4e8
	.uleb128 0x5
	.long	0xd89
	.byte	0
	.uleb128 0x16
	.ascii "unlock\0"
	.byte	0x83
	.ascii "_ZNSt5mutex6unlockEv\0"
	.byte	0x1
	.long	0x50f
	.long	0x515
	.uleb128 0x5
	.long	0xd89
	.byte	0
	.uleb128 0x15
	.ascii "native_handle_type\0"
	.byte	0x65
	.byte	0x1f
	.long	0xd9d
	.byte	0x1
	.uleb128 0x31
	.ascii "native_handle\0"
	.byte	0x1
	.byte	0x8a
	.byte	0x5
	.ascii "_ZNSt5mutex13native_handleEv\0"
	.long	0x515
	.byte	0x1
	.long	0x568
	.uleb128 0x5
	.long	0xd89
	.byte	0
	.byte	0
	.uleb128 0x8
	.long	0x3c4
	.uleb128 0x32
	.secrel32	.LASF5
	.byte	0x1
	.byte	0x1
	.byte	0xe1
	.byte	0xa
	.long	0x5ad
	.uleb128 0x33
	.secrel32	.LASF5
	.byte	0x1
	.byte	0xe1
	.byte	0x22
	.ascii "_ZNSt12adopt_lock_tC4Ev\0"
	.byte	0x1
	.long	0x5a6
	.uleb128 0x5
	.long	0xda2
	.byte	0
	.byte	0
	.uleb128 0x1d
	.ascii "lock_guard<std::mutex>\0"
	.byte	0xf5
	.byte	0xb
	.long	0x757
	.uleb128 0x34
	.secrel32	.LASF6
	.byte	0x1
	.byte	0xfb
	.byte	0x10
	.ascii "_ZNSt10lock_guardISt5mutexEC4ERS0_\0"
	.byte	0x1
	.long	0x5ff
	.long	0x60a
	.uleb128 0x5
	.long	0xdbf
	.uleb128 0x4
	.long	0xdc9
	.byte	0
	.uleb128 0x15
	.ascii "mutex_type\0"
	.byte	0xf8
	.byte	0x16
	.long	0x3c4
	.byte	0x1
	.uleb128 0x1c
	.secrel32	.LASF6
	.byte	0xff
	.byte	0x7
	.ascii "_ZNSt10lock_guardISt5mutexEC4ERS0_St12adopt_lock_t\0"
	.byte	0x1
	.long	0x660
	.long	0x670
	.uleb128 0x5
	.long	0xdbf
	.uleb128 0x4
	.long	0xdc9
	.uleb128 0x4
	.long	0x574
	.byte	0
	.uleb128 0x35
	.ascii "~lock_guard\0"
	.byte	0x1
	.word	0x102
	.byte	0x7
	.ascii "_ZNSt10lock_guardISt5mutexED4Ev\0"
	.byte	0x1
	.long	0x6aa
	.long	0x6b0
	.uleb128 0x5
	.long	0xdbf
	.byte	0
	.uleb128 0x36
	.secrel32	.LASF6
	.byte	0x1
	.word	0x105
	.byte	0x7
	.ascii "_ZNSt10lock_guardISt5mutexEC4ERKS1_\0"
	.byte	0x1
	.long	0x6e6
	.long	0x6f1
	.uleb128 0x5
	.long	0xdbf
	.uleb128 0x4
	.long	0xdce
	.byte	0
	.uleb128 0x37
	.secrel32	.LASF4
	.byte	0x1
	.word	0x106
	.byte	0x13
	.ascii "_ZNSt10lock_guardISt5mutexEaSERKS1_\0"
	.long	0xdd3
	.byte	0x1
	.long	0x72b
	.long	0x736
	.uleb128 0x5
	.long	0xdbf
	.uleb128 0x4
	.long	0xdce
	.byte	0
	.uleb128 0x38
	.ascii "_M_device\0"
	.byte	0x1
	.word	0x109
	.byte	0x14
	.long	0xdc9
	.byte	0
	.uleb128 0x39
	.ascii "_Mutex\0"
	.long	0x3c4
	.byte	0
	.uleb128 0x8
	.long	0x5ad
	.uleb128 0x3a
	.ascii "__throw_system_error\0"
	.byte	0x11
	.byte	0x6a
	.byte	0x3
	.ascii "_ZSt20__throw_system_errori\0"
	.uleb128 0x4
	.long	0x822
	.byte	0
	.byte	0
	.uleb128 0x3
	.byte	0x1
	.byte	0x2
	.ascii "bool\0"
	.uleb128 0x3
	.byte	0x8
	.byte	0x7
	.ascii "long long unsigned int\0"
	.uleb128 0x3
	.byte	0x1
	.byte	0x8
	.ascii "unsigned char\0"
	.uleb128 0x3
	.byte	0x2
	.byte	0x7
	.ascii "short unsigned int\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x7
	.ascii "unsigned int\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x7
	.ascii "long unsigned int\0"
	.uleb128 0x3
	.byte	0x1
	.byte	0x6
	.ascii "signed char\0"
	.uleb128 0x3
	.byte	0x2
	.byte	0x5
	.ascii "short int\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x5
	.ascii "int\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x5
	.ascii "long int\0"
	.uleb128 0x3
	.byte	0x8
	.byte	0x5
	.ascii "long long int\0"
	.uleb128 0x3
	.byte	0x2
	.byte	0x7
	.ascii "wchar_t\0"
	.uleb128 0x3
	.byte	0x1
	.byte	0x10
	.ascii "char8_t\0"
	.uleb128 0x3
	.byte	0x2
	.byte	0x10
	.ascii "char16_t\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x10
	.ascii "char32_t\0"
	.uleb128 0x3
	.byte	0x10
	.byte	0x5
	.ascii "__int128\0"
	.uleb128 0xb
	.ascii "__gnu_cxx\0"
	.byte	0x5
	.word	0x175
	.byte	0xb
	.uleb128 0x3
	.byte	0x10
	.byte	0x4
	.ascii "long double\0"
	.uleb128 0x3
	.byte	0x8
	.byte	0x4
	.ascii "double\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x4
	.ascii "float\0"
	.uleb128 0x3
	.byte	0x2
	.byte	0x4
	.ascii "_Float16\0"
	.uleb128 0x3
	.byte	0x4
	.byte	0x4
	.ascii "_Float32\0"
	.uleb128 0x3
	.byte	0x8
	.byte	0x4
	.ascii "_Float64\0"
	.uleb128 0x3
	.byte	0x10
	.byte	0x4
	.ascii "_Float128\0"
	.uleb128 0x3
	.byte	0x2
	.byte	0x4
	.ascii "__bf16\0"
	.uleb128 0x3
	.byte	0x10
	.byte	0x7
	.ascii "__int128 unsigned\0"
	.uleb128 0x3
	.byte	0x1
	.byte	0x6
	.ascii "char\0"
	.uleb128 0x2
	.ascii "intptr_t\0"
	.byte	0xe
	.byte	0x3e
	.byte	0x23
	.long	0x835
	.uleb128 0x2
	.ascii "uintptr_t\0"
	.byte	0xe
	.byte	0x4b
	.byte	0x2c
	.long	0x7a0
	.uleb128 0x2
	.ascii "__time64_t\0"
	.byte	0xe
	.byte	0x7b
	.byte	0x23
	.long	0x835
	.uleb128 0x2
	.ascii "time_t\0"
	.byte	0xe
	.byte	0x8a
	.byte	0x14
	.long	0x92c
	.uleb128 0x8
	.long	0x93f
	.uleb128 0x6
	.long	0x901
	.uleb128 0x2
	.ascii "int8_t\0"
	.byte	0xf
	.byte	0x23
	.byte	0x15
	.long	0x806
	.uleb128 0x2
	.ascii "uint8_t\0"
	.byte	0xf
	.byte	0x24
	.byte	0x19
	.long	0x7ba
	.uleb128 0x2
	.ascii "int16_t\0"
	.byte	0xf
	.byte	0x25
	.byte	0x10
	.long	0x815
	.uleb128 0x2
	.ascii "uint16_t\0"
	.byte	0xf
	.byte	0x26
	.byte	0x19
	.long	0x7cb
	.uleb128 0x2
	.ascii "int32_t\0"
	.byte	0xf
	.byte	0x27
	.byte	0xe
	.long	0x822
	.uleb128 0x2
	.ascii "uint32_t\0"
	.byte	0xf
	.byte	0x28
	.byte	0x14
	.long	0x7e1
	.uleb128 0x2
	.ascii "int64_t\0"
	.byte	0xf
	.byte	0x29
	.byte	0x26
	.long	0x835
	.uleb128 0x2
	.ascii "uint64_t\0"
	.byte	0xf
	.byte	0x2a
	.byte	0x30
	.long	0x7a0
	.uleb128 0x2
	.ascii "int_least8_t\0"
	.byte	0xf
	.byte	0x2d
	.byte	0x15
	.long	0x806
	.uleb128 0x2
	.ascii "uint_least8_t\0"
	.byte	0xf
	.byte	0x2e
	.byte	0x19
	.long	0x7ba
	.uleb128 0x2
	.ascii "int_least16_t\0"
	.byte	0xf
	.byte	0x2f
	.byte	0x10
	.long	0x815
	.uleb128 0x2
	.ascii "uint_least16_t\0"
	.byte	0xf
	.byte	0x30
	.byte	0x19
	.long	0x7cb
	.uleb128 0x2
	.ascii "int_least32_t\0"
	.byte	0xf
	.byte	0x31
	.byte	0xe
	.long	0x822
	.uleb128 0x2
	.ascii "uint_least32_t\0"
	.byte	0xf
	.byte	0x32
	.byte	0x14
	.long	0x7e1
	.uleb128 0x2
	.ascii "int_least64_t\0"
	.byte	0xf
	.byte	0x33
	.byte	0x26
	.long	0x835
	.uleb128 0x2
	.ascii "uint_least64_t\0"
	.byte	0xf
	.byte	0x34
	.byte	0x30
	.long	0x7a0
	.uleb128 0x2
	.ascii "int_fast8_t\0"
	.byte	0xf
	.byte	0x3a
	.byte	0x15
	.long	0x806
	.uleb128 0x2
	.ascii "uint_fast8_t\0"
	.byte	0xf
	.byte	0x3b
	.byte	0x17
	.long	0x7ba
	.uleb128 0x2
	.ascii "int_fast16_t\0"
	.byte	0xf
	.byte	0x3c
	.byte	0x10
	.long	0x815
	.uleb128 0x2
	.ascii "uint_fast16_t\0"
	.byte	0xf
	.byte	0x3d
	.byte	0x19
	.long	0x7cb
	.uleb128 0x2
	.ascii "int_fast32_t\0"
	.byte	0xf
	.byte	0x3e
	.byte	0xe
	.long	0x822
	.uleb128 0x2
	.ascii "uint_fast32_t\0"
	.byte	0xf
	.byte	0x3f
	.byte	0x18
	.long	0x7e1
	.uleb128 0x2
	.ascii "int_fast64_t\0"
	.byte	0xf
	.byte	0x40
	.byte	0x26
	.long	0x835
	.uleb128 0x2
	.ascii "uint_fast64_t\0"
	.byte	0xf
	.byte	0x41
	.byte	0x30
	.long	0x7a0
	.uleb128 0x2
	.ascii "intmax_t\0"
	.byte	0xf
	.byte	0x44
	.byte	0x26
	.long	0x835
	.uleb128 0x2
	.ascii "uintmax_t\0"
	.byte	0xf
	.byte	0x45
	.byte	0x30
	.long	0x7a0
	.uleb128 0x3
	.byte	0x10
	.byte	0x4
	.ascii "__float128\0"
	.uleb128 0x2
	.ascii "clock_t\0"
	.byte	0x10
	.byte	0x3f
	.byte	0x10
	.long	0x829
	.uleb128 0x3b
	.ascii "tm\0"
	.byte	0x24
	.byte	0x10
	.byte	0x64
	.byte	0xa
	.long	0xc09
	.uleb128 0x9
	.ascii "tm_sec\0"
	.byte	0x65
	.long	0x822
	.byte	0
	.uleb128 0x9
	.ascii "tm_min\0"
	.byte	0x66
	.long	0x822
	.byte	0x4
	.uleb128 0x9
	.ascii "tm_hour\0"
	.byte	0x67
	.long	0x822
	.byte	0x8
	.uleb128 0x9
	.ascii "tm_mday\0"
	.byte	0x68
	.long	0x822
	.byte	0xc
	.uleb128 0x9
	.ascii "tm_mon\0"
	.byte	0x69
	.long	0x822
	.byte	0x10
	.uleb128 0x9
	.ascii "tm_year\0"
	.byte	0x6a
	.long	0x822
	.byte	0x14
	.uleb128 0x9
	.ascii "tm_wday\0"
	.byte	0x6b
	.long	0x822
	.byte	0x18
	.uleb128 0x9
	.ascii "tm_yday\0"
	.byte	0x6c
	.long	0x822
	.byte	0x1c
	.uleb128 0x9
	.ascii "tm_isdst\0"
	.byte	0x6d
	.long	0x822
	.byte	0x20
	.byte	0
	.uleb128 0x8
	.long	0xb77
	.uleb128 0x3c
	.ascii "clock\0"
	.byte	0x10
	.byte	0x92
	.byte	0x13
	.long	0xb67
	.uleb128 0x17
	.ascii "difftime\0"
	.byte	0xfe
	.byte	0x12
	.ascii "_difftime64\0"
	.long	0x89e
	.long	0xc47
	.uleb128 0x4
	.long	0x93f
	.uleb128 0x4
	.long	0x93f
	.byte	0
	.uleb128 0x18
	.ascii "mktime\0"
	.word	0x105
	.byte	0x12
	.ascii "_mktime64\0"
	.long	0x93f
	.long	0xc6a
	.uleb128 0x4
	.long	0xc6a
	.byte	0
	.uleb128 0x6
	.long	0xb77
	.uleb128 0x17
	.ascii "time\0"
	.byte	0xfa
	.byte	0x12
	.ascii "_time64\0"
	.long	0x93f
	.long	0xc8d
	.uleb128 0x4
	.long	0xc8d
	.byte	0
	.uleb128 0x6
	.long	0x93f
	.uleb128 0x3d
	.ascii "asctime\0"
	.byte	0x10
	.byte	0x8e
	.byte	0x11
	.long	0x953
	.long	0xcac
	.uleb128 0x4
	.long	0xcac
	.byte	0
	.uleb128 0x6
	.long	0xc09
	.uleb128 0x18
	.ascii "ctime\0"
	.word	0x103
	.byte	0x11
	.ascii "_ctime64\0"
	.long	0x953
	.long	0xcd2
	.uleb128 0x4
	.long	0xcd2
	.byte	0
	.uleb128 0x6
	.long	0x94e
	.uleb128 0x18
	.ascii "gmtime\0"
	.word	0x101
	.byte	0x16
	.ascii "_gmtime64\0"
	.long	0xc6a
	.long	0xcfa
	.uleb128 0x4
	.long	0xcd2
	.byte	0
	.uleb128 0x17
	.ascii "localtime\0"
	.byte	0xff
	.byte	0x16
	.ascii "_localtime64\0"
	.long	0xc6a
	.long	0xd22
	.uleb128 0x4
	.long	0xcd2
	.byte	0
	.uleb128 0x2
	.ascii "pthread_mutexattr_t\0"
	.byte	0x12
	.byte	0xab
	.byte	0x12
	.long	0x7e1
	.uleb128 0x8
	.long	0xd22
	.uleb128 0x2
	.ascii "pthread_mutex_t\0"
	.byte	0x12
	.byte	0xe6
	.byte	0x12
	.long	0x909
	.uleb128 0x2
	.ascii "__gthread_mutex_t\0"
	.byte	0x2
	.byte	0x41
	.byte	0x19
	.long	0xd43
	.uleb128 0x6
	.long	0x2b5
	.uleb128 0x8
	.long	0xd75
	.uleb128 0xa
	.long	0x3bf
	.uleb128 0xa
	.long	0x2b5
	.uleb128 0x6
	.long	0x3c4
	.uleb128 0x8
	.long	0xd89
	.uleb128 0xa
	.long	0x56f
	.uleb128 0xa
	.long	0x3c4
	.uleb128 0x6
	.long	0x2c2
	.uleb128 0x6
	.long	0x574
	.uleb128 0x3e
	.ascii "g_mtx\0"
	.byte	0x3
	.byte	0x6
	.byte	0xc
	.long	0x3c4
	.uleb128 0x9
	.byte	0x3
	.quad	g_mtx
	.uleb128 0x6
	.long	0x5ad
	.uleb128 0x8
	.long	0xdbf
	.uleb128 0xa
	.long	0x60a
	.uleb128 0xa
	.long	0x757
	.uleb128 0xa
	.long	0x5ad
	.uleb128 0x10
	.ascii "pthread_mutex_init\0"
	.word	0x15c
	.long	0x822
	.long	0xe01
	.uleb128 0x4
	.long	0xe01
	.uleb128 0x4
	.long	0xe06
	.byte	0
	.uleb128 0x6
	.long	0xd43
	.uleb128 0x6
	.long	0xd3e
	.uleb128 0x10
	.ascii "pthread_mutex_destroy\0"
	.word	0x15d
	.long	0x822
	.long	0xe32
	.uleb128 0x4
	.long	0xe01
	.byte	0
	.uleb128 0x10
	.ascii "pthread_mutex_unlock\0"
	.word	0x15a
	.long	0x822
	.long	0xe58
	.uleb128 0x4
	.long	0xe01
	.byte	0
	.uleb128 0x10
	.ascii "pthread_mutex_lock\0"
	.word	0x14f
	.long	0x822
	.long	0xe7c
	.uleb128 0x4
	.long	0xe01
	.byte	0
	.uleb128 0x19
	.ascii "_GLOBAL__sub_I_g_mtx\0"
	.quad	.LFB1441
	.quad	.LFE1441-.LFB1441
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x19
	.ascii "__static_initialization_and_destruction_0\0"
	.quad	.LFB1436
	.quad	.LFE1436-.LFB1436
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x19
	.ascii "__tcfg_mtx\0"
	.quad	.LFB1440
	.quad	.LFE1440-.LFB1440
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0xc
	.long	0x3fd
	.long	0xf0c
	.long	0xf16
	.uleb128 0xd
	.secrel32	.LASF7
	.long	0xd8e
	.byte	0
	.uleb128 0xe
	.long	0xeff
	.ascii "_ZNSt5mutexD1Ev\0"
	.long	0xf45
	.quad	.LFB1439
	.quad	.LFE1439-.LFB1439
	.uleb128 0x1
	.byte	0x9c
	.long	0xf4e
	.uleb128 0x7
	.long	0xf0c
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0xc
	.long	0x670
	.long	0xf5b
	.long	0xf65
	.uleb128 0xd
	.secrel32	.LASF7
	.long	0xdc4
	.byte	0
	.uleb128 0xe
	.long	0xf4e
	.ascii "_ZNSt10lock_guardISt5mutexED1Ev\0"
	.long	0xfa4
	.quad	.LFB1418
	.quad	.LFE1418-.LFB1418
	.uleb128 0x1
	.byte	0x9c
	.long	0xfad
	.uleb128 0x7
	.long	0xf5b
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0xc
	.long	0x5cb
	.long	0xfba
	.long	0xfd0
	.uleb128 0xd
	.secrel32	.LASF7
	.long	0xdc4
	.uleb128 0x3f
	.ascii "__m\0"
	.byte	0x1
	.byte	0xfb
	.byte	0x27
	.long	0xdc9
	.byte	0
	.uleb128 0xe
	.long	0xfad
	.ascii "_ZNSt10lock_guardISt5mutexEC1ERS0_\0"
	.long	0x1012
	.quad	.LFB1415
	.quad	.LFE1415-.LFB1415
	.uleb128 0x1
	.byte	0x9c
	.long	0x1023
	.uleb128 0x7
	.long	0xfba
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x7
	.long	0xfc3
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.byte	0
	.uleb128 0x40
	.ascii "critical_section\0"
	.byte	0x3
	.byte	0x8
	.byte	0x6
	.ascii "_Z16critical_sectionv\0"
	.quad	.LFB1381
	.quad	.LFE1381-.LFB1381
	.uleb128 0x1
	.byte	0x9c
	.long	0x1073
	.uleb128 0x1f
	.ascii "lk\0"
	.byte	0x3
	.byte	0x9
	.byte	0x21
	.long	0x5ad
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.byte	0
	.uleb128 0xc
	.long	0x3d7
	.long	0x1080
	.long	0x108a
	.uleb128 0xd
	.secrel32	.LASF7
	.long	0xd8e
	.byte	0
	.uleb128 0xe
	.long	0x1073
	.ascii "_ZNSt5mutexC1Ev\0"
	.long	0x10b9
	.quad	.LFB1380
	.quad	.LFE1380-.LFB1380
	.uleb128 0x1
	.byte	0x9c
	.long	0x10c2
	.uleb128 0x7
	.long	0x1080
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.byte	0
	.uleb128 0x20
	.long	0x4e8
	.long	0x10e1
	.quad	.LFB1289
	.quad	.LFE1289-.LFB1289
	.uleb128 0x1
	.byte	0x9c
	.long	0x1125
	.uleb128 0x21
	.secrel32	.LASF7
	.long	0xd8e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x11
	.long	0x12b3
	.quad	.LBB42
	.quad	.LBE42-.LBB42
	.byte	0x86
	.byte	0x1d
	.uleb128 0x7
	.long	0x12f2
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x12
	.long	0x13f3
	.quad	.LBB44
	.quad	.LBE44-.LBB44
	.word	0x338
	.byte	0
	.byte	0
	.uleb128 0x20
	.long	0x488
	.long	0x1144
	.quad	.LFB1287
	.quad	.LFE1287-.LFB1287
	.uleb128 0x1
	.byte	0x9c
	.long	0x1197
	.uleb128 0x21
	.secrel32	.LASF7
	.long	0xd8e
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x1f
	.ascii "__e\0"
	.byte	0x1
	.byte	0x73
	.byte	0xb
	.long	0x822
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.uleb128 0x11
	.long	0x1304
	.quad	.LBB38
	.quad	.LBE38-.LBB38
	.byte	0x73
	.byte	0x25
	.uleb128 0x7
	.long	0x133f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x12
	.long	0x13f3
	.quad	.LBB40
	.quad	.LBE40-.LBB40
	.word	0x31a
	.byte	0
	.byte	0
	.uleb128 0xc
	.long	0x319
	.long	0x11a4
	.long	0x11ae
	.uleb128 0xd
	.secrel32	.LASF7
	.long	0xd7a
	.byte	0
	.uleb128 0xe
	.long	0x1197
	.ascii "_ZNSt12__mutex_baseD2Ev\0"
	.long	0x11e5
	.quad	.LFB1285
	.quad	.LFE1285-.LFB1285
	.uleb128 0x1
	.byte	0x9c
	.long	0x1225
	.uleb128 0x7
	.long	0x11a4
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x11
	.long	0x134c
	.quad	.LBB34
	.quad	.LBE34-.LBB34
	.byte	0x4f
	.byte	0x37
	.uleb128 0x7
	.long	0x138d
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x12
	.long	0x13f3
	.quad	.LBB36
	.quad	.LBE36-.LBB36
	.word	0x311
	.byte	0
	.byte	0
	.uleb128 0xc
	.long	0x2eb
	.long	0x1232
	.long	0x123c
	.uleb128 0xd
	.secrel32	.LASF7
	.long	0xd7a
	.byte	0
	.uleb128 0xe
	.long	0x1225
	.ascii "_ZNSt12__mutex_baseC2Ev\0"
	.long	0x1273
	.quad	.LFB1282
	.quad	.LFE1282-.LFB1282
	.uleb128 0x1
	.byte	0x9c
	.long	0x12b3
	.uleb128 0x7
	.long	0x1232
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x11
	.long	0x139a
	.quad	.LBB29
	.quad	.LBE29-.LBB29
	.byte	0x4c
	.byte	0x24
	.uleb128 0x7
	.long	0x13e6
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x12
	.long	0x13f3
	.quad	.LBB31
	.quad	.LBE31-.LBB31
	.word	0x30a
	.byte	0
	.byte	0
	.uleb128 0x1a
	.ascii "__gthread_mutex_unlock\0"
	.word	0x336
	.ascii "_Z22__gthread_mutex_unlockPx\0"
	.long	0x822
	.long	0x12ff
	.uleb128 0x13
	.secrel32	.LASF8
	.word	0x336
	.byte	0x2c
	.long	0x12ff
	.byte	0
	.uleb128 0x6
	.long	0xd5b
	.uleb128 0x1a
	.ascii "__gthread_mutex_lock\0"
	.word	0x318
	.ascii "_Z20__gthread_mutex_lockPx\0"
	.long	0x822
	.long	0x134c
	.uleb128 0x13
	.secrel32	.LASF8
	.word	0x318
	.byte	0x2a
	.long	0x12ff
	.byte	0
	.uleb128 0x1a
	.ascii "__gthread_mutex_destroy\0"
	.word	0x30f
	.ascii "_Z23__gthread_mutex_destroyPx\0"
	.long	0x822
	.long	0x139a
	.uleb128 0x13
	.secrel32	.LASF8
	.word	0x30f
	.byte	0x2d
	.long	0x12ff
	.byte	0
	.uleb128 0x41
	.ascii "__gthread_mutex_init_function\0"
	.byte	0x2
	.word	0x308
	.byte	0x1
	.ascii "_Z29__gthread_mutex_init_functionPx\0"
	.byte	0x3
	.long	0x13f3
	.uleb128 0x13
	.secrel32	.LASF8
	.word	0x308
	.byte	0x33
	.long	0x12ff
	.byte	0
	.uleb128 0x42
	.ascii "__gthread_active_p\0"
	.byte	0x2
	.word	0x15a
	.byte	0x1
	.ascii "_Z18__gthread_active_pv\0"
	.long	0x822
	.byte	0x3
	.byte	0
	.section	.debug_abbrev,"dr"
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x8
	.byte	0
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x18
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2
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
	.uleb128 0x3
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
	.uleb128 0x4
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x34
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 16
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 9
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0xa
	.uleb128 0x10
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xb
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
	.uleb128 0xc
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x47
	.uleb128 0x13
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x20
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x1
	.uleb128 0x13
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
	.uleb128 0xf
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
	.uleb128 0x10
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 18
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 20
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x11
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
	.sleb128 1
	.uleb128 0x59
	.uleb128 0xb
	.uleb128 0x57
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x12
	.uleb128 0x1d
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x58
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x59
	.uleb128 0x5
	.uleb128 0x57
	.uleb128 0x21
	.sleb128 26
	.byte	0
	.byte	0
	.uleb128 0x13
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x14
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
	.uleb128 0x15
	.uleb128 0x16
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
	.uleb128 0x32
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x16
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
	.sleb128 5
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
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 16
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
	.uleb128 0x18
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 16
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
	.uleb128 0x2e
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x1a
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 2
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x20
	.uleb128 0x21
	.sleb128 3
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1b
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
	.uleb128 0x1c
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
	.uleb128 0x1d
	.uleb128 0x2
	.byte	0x1
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1e
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
	.sleb128 5
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
	.uleb128 0x1f
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
	.uleb128 0x20
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
	.uleb128 0x21
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
	.uleb128 0x22
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
	.uleb128 0x23
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
	.uleb128 0x24
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
	.uleb128 0x25
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
	.uleb128 0x26
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
	.uleb128 0x27
	.uleb128 0x3a
	.byte	0
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x18
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x28
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
	.uleb128 0x89
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x29
	.uleb128 0x2
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x2a
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
	.uleb128 0x32
	.uleb128 0xb
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
	.uleb128 0x32
	.uleb128 0xb
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x8a
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2c
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
	.uleb128 0x8a
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2d
	.uleb128 0x1c
	.byte	0
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
	.uleb128 0x8a
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
	.uleb128 0x8a
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x30
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
	.uleb128 0x31
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
	.uleb128 0x32
	.uleb128 0xb
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x32
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
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
	.uleb128 0x33
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
	.uleb128 0x8b
	.uleb128 0xb
	.uleb128 0x64
	.uleb128 0x13
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
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0x8
	.uleb128 0x32
	.uleb128 0xb
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
	.uleb128 0x36
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
	.uleb128 0x8a
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x37
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
	.uleb128 0x8a
	.uleb128 0x19
	.uleb128 0x64
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x38
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
	.uleb128 0x39
	.uleb128 0x2f
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x49
	.uleb128 0x13
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
	.uleb128 0x87
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x3b
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
	.uleb128 0x3c
	.uleb128 0x2e
	.byte	0
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
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x3d
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
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3e
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
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x3f
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
	.uleb128 0x41
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
	.uleb128 0x20
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x42
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
	.uleb128 0x20
	.uleb128 0xb
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"dr"
	.long	0xac
	.word	0x2
	.secrel32	.Ldebug_info0
	.byte	0x8
	.byte	0
	.word	0
	.word	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	.LFB1282
	.quad	.LFE1282-.LFB1282
	.quad	.LFB1285
	.quad	.LFE1285-.LFB1285
	.quad	.LFB1287
	.quad	.LFE1287-.LFB1287
	.quad	.LFB1289
	.quad	.LFE1289-.LFB1289
	.quad	.LFB1380
	.quad	.LFE1380-.LFB1380
	.quad	.LFB1415
	.quad	.LFE1415-.LFB1415
	.quad	.LFB1418
	.quad	.LFE1418-.LFB1418
	.quad	.LFB1439
	.quad	.LFE1439-.LFB1439
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
	.quad	.LFB1282
	.uleb128 .LFE1282-.LFB1282
	.byte	0x7
	.quad	.LFB1285
	.uleb128 .LFE1285-.LFB1285
	.byte	0x7
	.quad	.LFB1287
	.uleb128 .LFE1287-.LFB1287
	.byte	0x7
	.quad	.LFB1289
	.uleb128 .LFE1289-.LFB1289
	.byte	0x7
	.quad	.LFB1380
	.uleb128 .LFE1380-.LFB1380
	.byte	0x7
	.quad	.LFB1415
	.uleb128 .LFE1415-.LFB1415
	.byte	0x7
	.quad	.LFB1418
	.uleb128 .LFE1418-.LFB1418
	.byte	0x7
	.quad	.LFB1439
	.uleb128 .LFE1439-.LFB1439
	.byte	0
.Ldebug_ranges3:
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
.LASF2:
	.ascii "__detail\0"
.LASF3:
	.ascii "__mutex_base\0"
.LASF6:
	.ascii "lock_guard\0"
.LASF4:
	.ascii "operator=\0"
.LASF7:
	.ascii "this\0"
.LASF8:
	.ascii "__mutex\0"
.LASF5:
	.ascii "adopt_lock_t\0"
	.section	.debug_line_str,"dr"
.LASF1:
	.ascii "C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible\0"
.LASF0:
	.ascii "Examples\\_ch147_asm.cpp\0"
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	pthread_mutex_init;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_destroy;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_lock;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_system_errori;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_unlock;	.scl	2;	.type	32;	.endef
	.def	atexit;	.scl	2;	.type	32;	.endef
