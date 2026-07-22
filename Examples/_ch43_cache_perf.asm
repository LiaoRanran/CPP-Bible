	.file	"_ch43_cache_perf.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZL5chasePyy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL5chasePyy
_ZL5chasePyy:
.LFB12706:
	.seh_endprologue
	test	rdx, rdx
	je	.L4
	mov	rcx, QWORD PTR [rcx]
	xor	eax, eax
	xor	r8d, r8d
	.p2align 4
	.p2align 4
	.p2align 3
.L3:
	mov	rcx, QWORD PTR [rcx]
	add	rax, 1
	add	r8, rcx
	cmp	rdx, rax
	jne	.L3
	mov	rax, r8
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	xor	r8d, r8d
	mov	rax, r8
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt12_Vector_baseIySaIyEED2Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIySaIyEED2Ev.isra.0
_ZNSt12_Vector_baseIySaIyEED2Ev.isra.0:
.LFB13570:
	.seh_endprologue
	test	rcx, rcx
	je	.L7
	sub	rdx, rcx
	jmp	_ZdlPvy
.L7:
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "cannot create std::vector larger than max_size()\0"
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB1:
	.text
.LHOTB1:
	.align 2
	.p2align 4
	.def	_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0
_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0:
.LFB13571:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	rax, rdx
	mov	rbx, rcx
	shr	rax, 60
	jne	.L16
	test	rdx, rdx
	je	.L17
	lea	r8, 0[0+rdx*8]
	mov	QWORD PTR 72[rsp], rdx
	mov	rcx, r8
	mov	QWORD PTR 32[rsp], r8
	call	_Znwy
	mov	r8, QWORD PTR 32[rsp]
	xor	edx, edx
	mov	QWORD PTR [rbx], rax
	lea	rcx, 8[rax]
	lea	r10, [rax+r8]
	mov	QWORD PTR [rax], rdx
	mov	QWORD PTR 16[rbx], r10
	cmp	QWORD PTR 72[rsp], 1
	je	.L12
	sub	r8, 8
	xor	edx, edx
	mov	QWORD PTR 40[rsp], r10
	mov	QWORD PTR 32[rsp], rax
	call	memset
	mov	r10, QWORD PTR 40[rsp]
	lea	rcx, -8[r10+rax]
	sub	rcx, QWORD PTR 32[rsp]
.L12:
	mov	QWORD PTR 8[rbx], rcx
	add	rsp, 48
	pop	rbx
	ret
.L17:
	xor	ecx, ecx
	mov	QWORD PTR [rbx], rcx
	mov	QWORD PTR 16[rbx], rcx
	xor	ecx, ecx
	jmp	.L12
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0.cold
	.seh_stackalloc	56
	.seh_savereg	rbx, 48
	.seh_endprologue
_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0.cold:
.L16:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text$_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv
	.def	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv
_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv:
.LFB13500:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	movabs	r11, -5403634167711393303
	mov	r10, QWORD PTR [rcx]
	mov	r8, rcx
	mov	rdx, rcx
	lea	rbx, 1248[rcx]
	.p2align 6
	.p2align 4
	.p2align 3
.L19:
	and	r10, -2147483648
	add	rcx, 8
	mov	r9, r10
	mov	r10, QWORD PTR [rcx]
	mov	rax, r10
	and	eax, 2147483647
	or	rax, r9
	mov	r9, rax
	and	eax, 1
	neg	rax
	shr	r9
	xor	r9, QWORD PTR 1240[rcx]
	and	rax, r11
	xor	rax, r9
	mov	QWORD PTR -8[rcx], rax
	cmp	rcx, rbx
	jne	.L19
	mov	r9, QWORD PTR 1248[r8]
	lea	r11, 1240[r8]
	movabs	r10, -5403634167711393303
	.p2align 4
	.p2align 3
.L20:
	mov	rcx, r9
	mov	r9, QWORD PTR 1256[rdx]
	add	rdx, 8
	and	rcx, -2147483648
	mov	rax, r9
	and	eax, 2147483647
	or	rax, rcx
	mov	rcx, rax
	and	eax, 1
	neg	rax
	shr	rcx
	xor	rcx, QWORD PTR -8[rdx]
	and	rax, r10
	xor	rax, rcx
	mov	QWORD PTR 1240[rdx], rax
	cmp	r11, rdx
	jne	.L20
	mov	rax, QWORD PTR 2488[r8]
	mov	rdx, QWORD PTR [r8]
	mov	QWORD PTR 2496[r8], 0
	and	edx, 2147483647
	and	rax, -2147483648
	or	rax, rdx
	mov	rdx, rax
	and	eax, 1
	neg	rax
	shr	rdx
	xor	rdx, QWORD PTR 1240[r8]
	and	rax, r10
	xor	rax, rdx
	mov	QWORD PTR 2488[r8], rax
	pop	rbx
	ret
	.seh_endproc
	.section	.text$_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv
	.def	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv
_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv:
.LFB13407:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR 2496[rcx]
	cmp	rax, 311
	ja	.L25
.L24:
	lea	rdx, 1[rax]
	mov	rax, QWORD PTR [rcx+rax*8]
	mov	QWORD PTR 2496[rcx], rdx
	movabs	rcx, 6148914691236517205
	mov	rdx, rax
	shr	rdx, 29
	and	rdx, rcx
	movabs	rcx, 8202884508482404352
	xor	rdx, rax
	mov	rax, rdx
	sal	rax, 17
	and	rax, rcx
	movabs	rcx, -2270628950310912
	xor	rax, rdx
	mov	rdx, rax
	sal	rdx, 37
	and	rdx, rcx
	xor	rdx, rax
	mov	rax, rdx
	shr	rax, 43
	xor	rax, rdx
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L25:
	mov	QWORD PTR 48[rsp], rcx
	call	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv
	mov	rcx, QWORD PTR 48[rsp]
	mov	rax, QWORD PTR 2496[rcx]
	jmp	.L24
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNSt24uniform_int_distributionIyEclISt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEEyRT_RKNS0_10param_typeE.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt24uniform_int_distributionIyEclISt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEEyRT_RKNS0_10param_typeE.isra.0
_ZNSt24uniform_int_distributionIyEclISt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEEyRT_RKNS0_10param_typeE.isra.0:
.LFB13574:
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
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rsi, r8
	mov	rbx, rcx
	mov	rdi, rdx
	mov	rbp, r8
	sub	rsi, rdx
	cmp	rsi, -1
	je	.L27
	call	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv
	add	rsi, 1
	mul	rsi
	mov	r10, rax
	mov	r11, rdx
	cmp	rax, rsi
	jnb	.L28
	lea	rax, -1[rdi]
	xor	edx, edx
	sub	rax, rbp
	div	rsi
	mov	rbp, rdx
	cmp	r10, rdx
	jnb	.L28
	mov	rcx, QWORD PTR 2496[rbx]
	movabs	r14, 6148914691236517205
	movabs	r13, 8202884508482404352
	movabs	r12, -2270628950310912
	jmp	.L30
	.p2align 4,,10
	.p2align 3
.L29:
	mov	r10, QWORD PTR [rbx+rax*8]
	lea	rcx, 1[rax]
	mov	QWORD PTR 2496[rbx], rcx
	mov	rax, r10
	shr	rax, 29
	and	rax, r14
	xor	r10, rax
	mov	rax, r10
	sal	rax, 17
	and	rax, r13
	xor	r10, rax
	mov	rax, r10
	sal	rax, 37
	and	rax, r12
	xor	r10, rax
	mov	rax, r10
	shr	rax, 43
	xor	r10, rax
	mov	rax, r10
	mul	rsi
	mov	r11, rdx
	cmp	rax, rbp
	jnb	.L28
.L30:
	mov	rax, rcx
	cmp	rcx, 311
	jbe	.L29
	mov	rcx, rbx
	call	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv
	mov	rax, QWORD PTR 2496[rbx]
	jmp	.L29
	.p2align 4,,10
	.p2align 3
.L28:
	mov	rax, r11
.L31:
	add	rax, rdi
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L27:
	call	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv
	jmp	.L31
	.seh_endproc
	.section	.text$_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_
	.def	_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_
_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_:
.LFB13073:
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
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rsi, rcx
	mov	rdi, rdx
	mov	rbp, r8
	cmp	rdx, rcx
	je	.L34
	mov	rcx, rdx
	lea	rbx, 8[rsi]
	sub	rcx, rsi
	sar	rcx, 3
	mov	rax, rcx
	mul	rcx
	seto	al
	movzx	eax, al
	test	rax, rax
	jne	.L47
	jmp	.L48
	.p2align 4,,10
	.p2align 3
.L42:
	mov	r8, rbx
	xor	edx, edx
	mov	rcx, rbp
	add	rbx, 8
	sub	r8, rsi
	sar	r8, 3
	call	_ZNSt24uniform_int_distributionIyEclISt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEEyRT_RKNS0_10param_typeE.isra.0
	mov	rdx, QWORD PTR -8[rbx]
	mov	rcx, QWORD PTR [rsi+rax*8]
	mov	QWORD PTR -8[rbx], rcx
	mov	QWORD PTR [rsi+rax*8], rdx
.L47:
	cmp	rdi, rbx
	jne	.L42
.L34:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L48:
	and	ecx, 1
	je	.L49
.L39:
	cmp	rdi, rbx
	je	.L34
	.p2align 4
	.p2align 3
.L40:
	mov	rax, rbx
	xor	edx, edx
	mov	rcx, rbp
	add	rbx, 16
	sub	rax, rsi
	sar	rax, 3
	lea	r12, 2[rax]
	add	rax, 1
	imul	rax, r12
	lea	r8, -1[rax]
	call	_ZNSt24uniform_int_distributionIyEclISt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEEyRT_RKNS0_10param_typeE.isra.0
	xor	edx, edx
	mov	rcx, QWORD PTR -16[rbx]
	div	r12
	mov	r8, QWORD PTR [rsi+rax*8]
	mov	QWORD PTR -16[rbx], r8
	mov	QWORD PTR [rsi+rax*8], rcx
	lea	rax, [rsi+rdx*8]
	mov	rdx, QWORD PTR -8[rbx]
	mov	rcx, QWORD PTR [rax]
	mov	QWORD PTR -8[rbx], rcx
	mov	QWORD PTR [rax], rdx
	cmp	rdi, rbx
	jne	.L40
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L49:
	mov	rcx, r8
	lea	rbx, 16[rsi]
	call	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv
	mov	edx, 2
	mul	rdx
	lea	rax, [rsi+rdx*8]
	mov	rdx, QWORD PTR 8[rsi]
	mov	rcx, QWORD PTR [rax]
	mov	QWORD PTR 8[rsi], rcx
	mov	QWORD PTR [rax], rdx
	jmp	.L39
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "\0"
	.section	.text.unlikely,"x"
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4
	.def	_ZL7measureydi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL7measureydi
_ZL7measureydi:
.LFB12707:
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
	sub	rsp, 2664
	.seh_stackalloc	2664
	movaps	XMMWORD PTR 2640[rsp], xmm6
	.seh_savexmm	xmm6, 2640
	.seh_endprologue
	mov	rsi, rdx
	mov	rdi, rdx
	mov	r12, rcx
	mov	ebp, r9d
	shr	rsi, 3
	lea	rcx, 64[rsp]
	movapd	xmm6, xmm2
	mov	rdx, rsi
.LEHB0:
	call	_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0
.LEHE0:
	mov	rbx, QWORD PTR 64[rsp]
	mov	rax, QWORD PTR 80[rsp]
	lea	rcx, [rdi+rbx]
	and	edi, 8
	mov	QWORD PTR 40[rsp], rax
	mov	rax, rbx
	je	.L51
	lea	rax, 8[rbx]
	mov	QWORD PTR [rbx], rbx
	cmp	rcx, rax
	je	.L81
	.p2align 5
	.p2align 4
	.p2align 3
.L51:
	mov	QWORD PTR [rax], rax
	lea	rdx, 8[rax]
	add	rax, 16
	mov	QWORD PTR [rdx], rdx
	cmp	rcx, rax
	jne	.L51
.L81:
	lea	rcx, 96[rsp]
	mov	rdx, rsi
.LEHB1:
	call	_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0
.LEHE1:
	mov	rax, QWORD PTR 112[rsp]
	mov	rdi, QWORD PTR 96[rsp]
	mov	QWORD PTR 32[rsp], rax
	xor	eax, eax
	test	sil, 1
	je	.L52
	xor	eax, eax
	mov	QWORD PTR [rdi], rax
	mov	eax, 1
	cmp	rsi, 1
	je	.L80
	.p2align 5
	.p2align 4
	.p2align 3
.L52:
	mov	QWORD PTR [rdi+rax*8], rax
	lea	rdx, 1[rax]
	add	rax, 2
	mov	QWORD PTR [rdi+rdx*8], rdx
	cmp	rsi, rax
	jne	.L52
.L80:
	movabs	rax, -7046029254386353131
	mov	edx, 1
	lea	r8, 136[rsp]
	movabs	r9, 6364136223846793005
	mov	QWORD PTR 128[rsp], rax
	mov	rcx, rax
	.p2align 6
	.p2align 4
	.p2align 3
.L53:
	mov	rax, rcx
	add	r8, 8
	shr	rax, 62
	xor	rax, rcx
	imul	rax, r9
	lea	rcx, [rax+rdx]
	add	rdx, 1
	mov	QWORD PTR -8[r8], rcx
	cmp	rdx, 312
	jne	.L53
	mov	rdx, QWORD PTR 104[rsp]
	mov	rcx, rdi
	lea	r8, 128[rsp]
	mov	QWORD PTR 2624[rsp], 312
	call	_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L54:
	mov	rdx, QWORD PTR [rdi+rax*8]
	lea	rdx, [rbx+rdx*8]
	mov	QWORD PTR [rbx+rax*8], rdx
	add	rax, 1
	cmp	rsi, rax
	jne	.L54
	mov	QWORD PTR 56[rsp], 0
	xor	r14d, r14d
	mov	r13, -1
	.p2align 4
	.p2align 3
.L55:
/APP
 # 20 "Examples\_ch43_cache_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	mov	rdx, rsi
	mov	rcx, rbx
	mov	r15, rax
.LEHB2:
	call	_ZL5chasePyy
	mov	rdx, rax
	mov	rax, QWORD PTR 56[rsp]
	add	rax, rdx
	mov	QWORD PTR 56[rsp], rax
/APP
 # 20 "Examples\_ch43_cache_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sub	rax, r15
	cmp	r13, rax
	cmova	r13, rax
	add	r14d, 1
	cmp	ebp, r14d
	jne	.L55
	mov	rax, QWORD PTR 56[rsp]
	test	rax, rax
	jne	.L59
	lea	rcx, .LC2[rip]
	call	__mingw_printf
.LEHE2:
.L59:
	test	r13, r13
	js	.L57
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, r13
.L58:
	pxor	xmm1, xmm1
	mov	rdx, QWORD PTR 32[rsp]
	mov	rcx, rdi
	cvtsi2sd	xmm1, rsi
	divsd	xmm0, xmm1
	movapd	xmm1, xmm0
	divsd	xmm1, xmm6
	unpcklpd	xmm0, xmm1
	movups	XMMWORD PTR [r12], xmm0
	call	_ZNSt12_Vector_baseIySaIyEED2Ev.isra.0
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, rbx
	call	_ZNSt12_Vector_baseIySaIyEED2Ev.isra.0
	nop
	movaps	xmm6, XMMWORD PTR 2640[rsp]
	mov	rax, r12
	add	rsp, 2664
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L57:
	mov	rax, r13
	mov	r8, r13
	pxor	xmm0, xmm0
	shr	rax
	and	r8d, 1
	or	rax, r8
	cvtsi2sd	xmm0, rax
	addsd	xmm0, xmm0
	jmp	.L58
.L63:
	mov	rsi, rax
	jmp	.L60
.L62:
	mov	rsi, rax
	jmp	.L61
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA12707:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE12707-.LLSDACSB12707
.LLSDACSB12707:
	.uleb128 .LEHB0-.LFB12707
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB12707
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L62-.LFB12707
	.uleb128 0
	.uleb128 .LEHB2-.LFB12707
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L63-.LFB12707
	.uleb128 0
.LLSDACSE12707:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZL7measureydi.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL7measureydi.cold
	.seh_stackalloc	2728
	.seh_savereg	rbx, 2664
	.seh_savereg	rsi, 2672
	.seh_savereg	rdi, 2680
	.seh_savereg	rbp, 2688
	.seh_savexmm	xmm6, 2640
	.seh_savereg	r12, 2696
	.seh_savereg	r13, 2704
	.seh_savereg	r14, 2712
	.seh_savereg	r15, 2720
	.seh_endprologue
_ZL7measureydi.cold:
.L60:
	mov	rdx, QWORD PTR 32[rsp]
	mov	rcx, rdi
	call	_ZNSt12_Vector_baseIySaIyEED2Ev.isra.0
.L61:
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, rbx
	call	_ZNSt12_Vector_baseIySaIyEED2Ev.isra.0
	mov	rcx, rsi
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC12707:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC12707-.LLSDACSBC12707
.LLSDACSBC12707:
	.uleb128 .LEHB3-.LCOLDB3
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSEC12707:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.text
.LHOTE3:
	.section .rdata,"dr"
	.align 8
.LC5:
	.ascii "TSC = %.3f GHz   (MinGW GCC 13.1.0 -O2, x86_64)\12\0"
.LC6:
	.ascii "cyc/step\0"
.LC7:
	.ascii "nodes\0"
.LC8:
	.ascii "work_set\0"
.LC9:
	.ascii "%-10s %12s %14s %14s\12\0"
.LC10:
	.ascii "ns/step\0"
.LC11:
	.ascii "16KB(L1)\0"
.LC12:
	.ascii "%-10s %12zu %14.2f %14.3f\12\0"
.LC13:
	.ascii "256KB(L2)\0"
.LC14:
	.ascii "8MB(L3)\0"
.LC15:
	.ascii "64MB(DRAM)\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB12720:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	call	__main
	lea	rcx, 88[rsp]
	call	[QWORD PTR __imp_QueryPerformanceFrequency[rip]]
	mov	rsi, QWORD PTR __imp_QueryPerformanceCounter[rip]
	lea	rcx, 96[rsp]
	call	rsi
/APP
 # 20 "Examples\_ch43_cache_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	mov	ecx, 100
	mov	rbx, rax
	call	[QWORD PTR __imp_Sleep[rip]]
	lea	rcx, 104[rsp]
	call	rsi
/APP
 # 20 "Examples\_ch43_cache_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sub	rax, rbx
	js	.L83
	pxor	xmm2, xmm2
	cvtsi2sd	xmm2, rax
.L84:
	mov	rax, QWORD PTR 104[rsp]
	pxor	xmm0, xmm0
	sub	rax, QWORD PTR 96[rsp]
	pxor	xmm1, xmm1
	cvtsi2sd	xmm0, rax
	cvtsi2sd	xmm1, QWORD PTR 88[rsp]
	divsd	xmm0, xmm1
	lea	rcx, .LC5[rip]
	divsd	xmm2, xmm0
	divsd	xmm2, QWORD PTR .LC4[rip]
	movapd	xmm1, xmm2
	movq	rdx, xmm2
	movsd	QWORD PTR 56[rsp], xmm2
	call	__mingw_printf
	lea	rax, .LC10[rip]
	lea	r8, .LC7[rip]
	mov	QWORD PTR 32[rsp], rax
	lea	r9, .LC6[rip]
	lea	rdx, .LC8[rip]
	lea	rcx, .LC9[rip]
	call	__mingw_printf
	movsd	xmm2, QWORD PTR 56[rsp]
	lea	rcx, 64[rsp]
	mov	r9d, 50
	mov	edx, 16384
	call	_ZL7measureydi
	movsd	xmm4, QWORD PTR 72[rsp]
	movsd	xmm3, QWORD PTR 64[rsp]
	mov	r8d, 2048
	lea	rdx, .LC11[rip]
	lea	rcx, .LC12[rip]
	movsd	QWORD PTR 32[rsp], xmm4
	movq	r9, xmm3
	call	__mingw_printf
	movsd	xmm2, QWORD PTR 56[rsp]
	lea	rcx, 64[rsp]
	mov	r9d, 30
	mov	edx, 262144
	call	_ZL7measureydi
	movsd	xmm5, QWORD PTR 72[rsp]
	movsd	xmm3, QWORD PTR 64[rsp]
	mov	r8d, 32768
	lea	rdx, .LC13[rip]
	lea	rcx, .LC12[rip]
	movsd	QWORD PTR 32[rsp], xmm5
	movq	r9, xmm3
	call	__mingw_printf
	movsd	xmm2, QWORD PTR 56[rsp]
	lea	rcx, 64[rsp]
	mov	r9d, 20
	mov	edx, 8388608
	call	_ZL7measureydi
	movsd	xmm4, QWORD PTR 72[rsp]
	movsd	xmm3, QWORD PTR 64[rsp]
	mov	r8d, 1048576
	lea	rdx, .LC14[rip]
	lea	rcx, .LC12[rip]
	movsd	QWORD PTR 32[rsp], xmm4
	movq	r9, xmm3
	call	__mingw_printf
	movsd	xmm2, QWORD PTR 56[rsp]
	lea	rcx, 64[rsp]
	mov	r9d, 10
	mov	edx, 67108864
	call	_ZL7measureydi
	movsd	xmm5, QWORD PTR 72[rsp]
	movsd	xmm3, QWORD PTR 64[rsp]
	mov	r8d, 8388608
	lea	rdx, .LC15[rip]
	lea	rcx, .LC12[rip]
	movsd	QWORD PTR 32[rsp], xmm5
	movq	r9, xmm3
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 120
	pop	rbx
	pop	rsi
	ret
.L83:
	mov	rdx, rax
	and	eax, 1
	pxor	xmm2, xmm2
	shr	rdx
	or	rdx, rax
	cvtsi2sd	xmm2, rdx
	addsd	xmm2, xmm2
	jmp	.L84
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC4:
	.long	0
	.long	1104006501
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
