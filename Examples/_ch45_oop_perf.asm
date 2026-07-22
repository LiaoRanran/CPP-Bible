	.file	"_ch45_oop_perf.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN7Derived4virtEi,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7Derived4virtEi
	.def	_ZN7Derived4virtEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7Derived4virtEi
_ZN7Derived4virtEi:
.LFB8392:
	.seh_endprologue
	lea	eax, -1[rdx]
	ret
	.seh_endproc
	.section	.text$_ZN2D24virtEi,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN2D24virtEi
	.def	_ZN2D24virtEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2D24virtEi
_ZN2D24virtEi:
.LFB8393:
	.seh_endprologue
	lea	eax, 7[rdx]
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z7free_fni
	.def	_Z7free_fni;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7free_fni
_Z7free_fni:
.LFB8394:
	.seh_endprologue
	lea	eax, 3[rcx]
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL9probe_nopi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL9probe_nopi
_ZL9probe_nopi:
.LFB8408:
	.seh_endprologue
	test	ecx, ecx
	jle	.L8
	xor	edx, edx
	xor	eax, eax
	test	cl, 1
	je	.L7
	mov	edx, 1
	cmp	ecx, 1
	je	.L15
	.p2align 4
	.p2align 4
	.p2align 3
.L7:
	lea	eax, 1[rax+rdx*2]
	add	edx, 2
	cmp	ecx, edx
	jne	.L7
.L15:
	cdqe
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	xor	eax, eax
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7DerivedD1Ev
	.def	_ZN7DerivedD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD1Ev
_ZN7DerivedD1Ev:
.LFB8412:
	.seh_endprologue
	ret
	.seh_endproc
	.text
	.p2align 4
	.def	_ZL13probe_virtuali;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL13probe_virtuali
_ZL13probe_virtuali:
.LFB8414:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ebp, ecx
	test	ecx, ecx
	jle	.L20
	mov	rdi, QWORD PTR g_obj[rip]
	xor	ebx, ebx
	xor	esi, esi
	.p2align 4
	.p2align 3
.L19:
	mov	rax, QWORD PTR [rdi]
	mov	edx, ebx
	mov	rcx, rdi
	add	ebx, 1
	call	[QWORD PTR 16[rax]]
	add	esi, eax
	cmp	ebp, ebx
	jne	.L19
	movsxd	rax, esi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L20:
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL11probe_fnptri;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL11probe_fnptri
_ZL11probe_fnptri:
.LFB8415:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	edi, ecx
	test	ecx, ecx
	jle	.L25
	mov	rbp, QWORD PTR g_fn[rip]
	xor	ebx, ebx
	xor	esi, esi
	.p2align 4
	.p2align 3
.L24:
	mov	ecx, ebx
	add	ebx, 1
	call	rbp
	add	esi, eax
	cmp	edi, ebx
	jne	.L24
	movsxd	rax, esi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L25:
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL20probe_virtual_reloadi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL20probe_virtual_reloadi
_ZL20probe_virtual_reloadi:
.LFB8416:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	edi, ecx
	test	ecx, ecx
	jle	.L30
	xor	ebx, ebx
	xor	esi, esi
	lea	rbp, g_arr[rip]
	.p2align 4
	.p2align 3
.L29:
	mov	eax, ebx
	mov	edx, ebx
	add	ebx, 1
	and	eax, 1
	mov	rcx, QWORD PTR 0[rbp+rax*8]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 16[rax]]
	add	esi, eax
	cmp	edi, ebx
	jne	.L29
	movsxd	rax, esi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L30:
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN2D2D1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN2D2D1Ev
	.def	_ZN2D2D1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2D2D1Ev
_ZN2D2D1Ev:
.LFB8444:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7DerivedD0Ev
	.def	_ZN7DerivedD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD0Ev
_ZN7DerivedD0Ev:
.LFB8413:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZN2D2D0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN2D2D0Ev
	.def	_ZN2D2D0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2D2D0Ev
_ZN2D2D0Ev:
.LFB8445:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.def	_ZL5benchPFyiEii.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL5benchPFyiEii.constprop.0
_ZL5benchPFyiEii.constprop.0:
.LFB8448:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	esi, 20
	mov	rbx, -1
	mov	rbp, rcx
	.p2align 4
	.p2align 3
.L36:
/APP
 # 15 "Examples\_ch45_oop_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	mov	ecx, 10000000
	mov	rdi, rax
	call	rbp
	mov	QWORD PTR g_sink[rip], rax
/APP
 # 15 "Examples\_ch45_oop_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sub	rax, rdi
	cmp	rbx, rax
	cmova	rbx, rax
	sub	esi, 1
	jne	.L36
	test	rbx, rbx
	js	.L37
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rbx
.L38:
	divsd	xmm0, QWORD PTR .LC0[rip]
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L37:
	mov	rax, rbx
	and	ebx, 1
	pxor	xmm0, xmm0
	shr	rax
	or	rax, rbx
	cvtsi2sd	xmm0, rax
	addsd	xmm0, xmm0
	jmp	.L38
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZN4Base8concreteEi.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN4Base8concreteEi.isra.0
_ZN4Base8concreteEi.isra.0:
.LFB8449:
	.seh_endprologue
	lea	eax, [rcx+rcx]
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL12probe_directi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL12probe_directi
_ZL12probe_directi:
.LFB8409:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	r9d, ecx
	test	ecx, ecx
	jle	.L44
	xor	edx, edx
	xor	r8d, r8d
	.p2align 4
	.p2align 3
.L43:
	mov	ecx, edx
	add	edx, 1
	call	_ZN4Base8concreteEi.isra.0
	add	r8d, eax
	cmp	r9d, edx
	jne	.L43
	movsxd	rax, r8d
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L44:
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC2:
	.ascii "TSC = %.3f GHz   (MinGW GCC 13.1.0 -O2, x86_64)\12\0"
.LC3:
	.ascii "ns/call\0"
.LC4:
	.ascii "cyc/call\0"
.LC5:
	.ascii "call\0"
.LC6:
	.ascii "%-18s %10s %10s %12s\12\0"
.LC7:
	.ascii "raw(cyc)\0"
.LC8:
	.ascii "direct\0"
.LC9:
	.ascii "%-18s %10.2f %10.3f %12.2f\12\0"
.LC10:
	.ascii "virtual(hot)\0"
.LC11:
	.ascii "fnptr\0"
.LC12:
	.ascii "virtual(reload)\0"
	.align 8
.LC13:
	.ascii "virtual(hot)-direct extra = %.2f ns (%.1f cyc)\12\0"
	.align 8
.LC14:
	.ascii "virtual(reload)-direct extra = %.2f ns (%.1f cyc)\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB8418:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 264
	.seh_stackalloc	264
	movaps	XMMWORD PTR 96[rsp], xmm6
	.seh_savexmm	xmm6, 96
	movaps	XMMWORD PTR 112[rsp], xmm7
	.seh_savexmm	xmm7, 112
	movaps	XMMWORD PTR 128[rsp], xmm8
	.seh_savexmm	xmm8, 128
	movaps	XMMWORD PTR 144[rsp], xmm9
	.seh_savexmm	xmm9, 144
	movaps	XMMWORD PTR 160[rsp], xmm10
	.seh_savexmm	xmm10, 160
	movaps	XMMWORD PTR 176[rsp], xmm11
	.seh_savexmm	xmm11, 176
	movaps	XMMWORD PTR 192[rsp], xmm12
	.seh_savexmm	xmm12, 192
	movaps	XMMWORD PTR 208[rsp], xmm13
	.seh_savexmm	xmm13, 208
	movaps	XMMWORD PTR 224[rsp], xmm14
	.seh_savexmm	xmm14, 224
	movaps	XMMWORD PTR 240[rsp], xmm15
	.seh_savexmm	xmm15, 240
	.seh_endprologue
	call	__main
	lea	rcx, 72[rsp]
	call	[QWORD PTR __imp_QueryPerformanceFrequency[rip]]
	mov	rsi, QWORD PTR __imp_QueryPerformanceCounter[rip]
	lea	rcx, 80[rsp]
	call	rsi
/APP
 # 15 "Examples\_ch45_oop_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	mov	ecx, 100
	mov	rbx, rax
	call	[QWORD PTR __imp_Sleep[rip]]
	lea	rcx, 88[rsp]
	call	rsi
/APP
 # 15 "Examples\_ch45_oop_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sub	rax, rbx
	js	.L47
	pxor	xmm1, xmm1
	cvtsi2sd	xmm1, rax
.L48:
	mov	rax, QWORD PTR 88[rsp]
	pxor	xmm0, xmm0
	sub	rax, QWORD PTR 80[rsp]
	pxor	xmm2, xmm2
	cvtsi2sd	xmm0, rax
	cvtsi2sd	xmm2, QWORD PTR 72[rsp]
	divsd	xmm0, xmm2
	lea	rcx, .LC2[rip]
	divsd	xmm1, xmm0
	divsd	xmm1, QWORD PTR .LC1[rip]
	movq	rdx, xmm1
	movsd	QWORD PTR 56[rsp], xmm1
	call	__mingw_printf
	lea	rcx, _ZL9probe_nopi[rip]
	call	_ZL5benchPFyiEii.constprop.0
	lea	rcx, _ZL12probe_directi[rip]
	movapd	xmm8, xmm0
	call	_ZL5benchPFyiEii.constprop.0
	lea	rcx, _ZL13probe_virtuali[rip]
	movapd	xmm15, xmm0
	call	_ZL5benchPFyiEii.constprop.0
	lea	rcx, _ZL11probe_fnptri[rip]
	movapd	xmm10, xmm15
	movapd	xmm14, xmm0
	call	_ZL5benchPFyiEii.constprop.0
	lea	rcx, _ZL20probe_virtual_reloadi[rip]
	movapd	xmm7, xmm14
	movapd	xmm13, xmm0
	call	_ZL5benchPFyiEii.constprop.0
	movapd	xmm12, xmm13
	subsd	xmm10, xmm8
	subsd	xmm7, xmm8
	subsd	xmm12, xmm8
	movsd	xmm1, QWORD PTR 56[rsp]
	movapd	xmm6, xmm0
	lea	rax, .LC7[rip]
	subsd	xmm6, xmm8
	mov	QWORD PTR 32[rsp], rax
	lea	r9, .LC3[rip]
	movapd	xmm11, xmm10
	movapd	xmm9, xmm7
	lea	r8, .LC4[rip]
	movsd	QWORD PTR 56[rsp], xmm0
	movapd	xmm4, xmm12
	lea	rdx, .LC5[rip]
	lea	rcx, .LC6[rip]
	divsd	xmm11, xmm1
	movapd	xmm8, xmm6
	divsd	xmm4, xmm1
	divsd	xmm9, xmm1
	movq	rbx, xmm4
	divsd	xmm8, xmm1
	call	__mingw_printf
	movapd	xmm3, xmm11
	movq	r9, xmm11
	movsd	QWORD PTR 32[rsp], xmm15
	movapd	xmm2, xmm10
	movq	r8, xmm10
	lea	rdx, .LC8[rip]
	lea	rcx, .LC9[rip]
	call	__mingw_printf
	movsd	QWORD PTR 32[rsp], xmm14
	movapd	xmm2, xmm7
	movq	r8, xmm7
	lea	rdx, .LC10[rip]
	lea	rcx, .LC9[rip]
	movapd	xmm3, xmm9
	movq	r9, xmm9
	call	__mingw_printf
	movsd	QWORD PTR 32[rsp], xmm13
	movq	xmm3, rbx
	mov	r9, rbx
	movapd	xmm2, xmm12
	movq	r8, xmm12
	lea	rdx, .LC11[rip]
	lea	rcx, .LC9[rip]
	call	__mingw_printf
	movsd	xmm0, QWORD PTR 56[rsp]
	movapd	xmm2, xmm6
	movq	r8, xmm6
	lea	rdx, .LC12[rip]
	lea	rcx, .LC9[rip]
	movsd	QWORD PTR 32[rsp], xmm0
	movapd	xmm3, xmm8
	movq	r9, xmm8
	call	__mingw_printf
	movapd	xmm1, xmm9
	subsd	xmm7, xmm10
	lea	rcx, .LC13[rip]
	subsd	xmm1, xmm11
	movq	r8, xmm7
	movapd	xmm2, xmm7
	movq	rdx, xmm1
	call	__mingw_printf
	movapd	xmm1, xmm8
	subsd	xmm6, xmm10
	lea	rcx, .LC14[rip]
	subsd	xmm1, xmm11
	movq	r8, xmm6
	movapd	xmm2, xmm6
	movq	rdx, xmm1
	call	__mingw_printf
	nop
	movaps	xmm6, XMMWORD PTR 96[rsp]
	movaps	xmm7, XMMWORD PTR 112[rsp]
	xor	eax, eax
	movaps	xmm8, XMMWORD PTR 128[rsp]
	movaps	xmm9, XMMWORD PTR 144[rsp]
	movaps	xmm10, XMMWORD PTR 160[rsp]
	movaps	xmm11, XMMWORD PTR 176[rsp]
	movaps	xmm12, XMMWORD PTR 192[rsp]
	movaps	xmm13, XMMWORD PTR 208[rsp]
	movaps	xmm14, XMMWORD PTR 224[rsp]
	movaps	xmm15, XMMWORD PTR 240[rsp]
	add	rsp, 264
	pop	rbx
	pop	rsi
	ret
.L47:
	mov	rdx, rax
	and	eax, 1
	pxor	xmm1, xmm1
	shr	rdx
	or	rdx, rax
	cvtsi2sd	xmm1, rdx
	addsd	xmm1, xmm1
	jmp	.L48
	.seh_endproc
	.p2align 4
	.def	_GLOBAL__sub_I__Z7free_fni;	.scl	3;	.type	32;	.endef
	.seh_proc	_GLOBAL__sub_I__Z7free_fni
_GLOBAL__sub_I__Z7free_fni:
.LFB8447:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	ecx, 8
	lea	rbx, _ZTV7Derived[rip+16]
	call	_Znwy
	mov	ecx, 8
	mov	QWORD PTR [rax], rbx
	mov	QWORD PTR g_obj[rip], rax
	call	_Znwy
	mov	ecx, 8
	mov	QWORD PTR [rax], rbx
	mov	QWORD PTR g_arr[rip], rax
	call	_Znwy
	lea	rdx, _ZTV2D2[rip+16]
	mov	QWORD PTR [rax], rdx
	mov	QWORD PTR g_arr[rip+8], rax
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section	.ctors,"w"
	.align 8
	.quad	_GLOBAL__sub_I__Z7free_fni
	.globl	_ZTS4Base
	.section	.rdata$_ZTS4Base,"dr"
	.linkonce same_size
_ZTS4Base:
	.ascii "4Base\0"
	.globl	_ZTI4Base
	.section	.rdata$_ZTI4Base,"dr"
	.linkonce same_size
	.align 8
_ZTI4Base:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS4Base
	.globl	_ZTS7Derived
	.section	.rdata$_ZTS7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTS7Derived:
	.ascii "7Derived\0"
	.globl	_ZTI7Derived
	.section	.rdata$_ZTI7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTI7Derived:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS7Derived
	.quad	_ZTI4Base
	.globl	_ZTS2D2
	.section	.rdata$_ZTS2D2,"dr"
	.linkonce same_size
_ZTS2D2:
	.ascii "2D2\0"
	.globl	_ZTI2D2
	.section	.rdata$_ZTI2D2,"dr"
	.linkonce same_size
	.align 8
_ZTI2D2:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS2D2
	.quad	_ZTI4Base
	.globl	_ZTV7Derived
	.section	.rdata$_ZTV7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTV7Derived:
	.quad	0
	.quad	_ZTI7Derived
	.quad	_ZN7DerivedD1Ev
	.quad	_ZN7DerivedD0Ev
	.quad	_ZN7Derived4virtEi
	.globl	_ZTV2D2
	.section	.rdata$_ZTV2D2,"dr"
	.linkonce same_size
	.align 8
_ZTV2D2:
	.quad	0
	.quad	_ZTI2D2
	.quad	_ZN2D2D1Ev
	.quad	_ZN2D2D0Ev
	.quad	_ZN2D24virtEi
	.globl	g_sink
	.bss
	.align 8
g_sink:
	.space 8
	.globl	g_fn
	.data
	.align 8
g_fn:
	.quad	_Z7free_fni
	.globl	g_arr
	.bss
	.align 16
g_arr:
	.space 16
	.globl	g_obj
	.align 8
g_obj:
	.space 8
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1097011920
	.align 8
.LC1:
	.long	0
	.long	1104006501
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
