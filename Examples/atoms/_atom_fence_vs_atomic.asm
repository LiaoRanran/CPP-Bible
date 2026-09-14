	.file	"_atom_fence_vs_atomic.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z13set_all_flagsi
	.def	_Z13set_all_flagsi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13set_all_flagsi
_Z13set_all_flagsi:
.LFB0:
	.seh_endprologue
	mov	DWORD PTR s_p_a[rip], 7
	mov	DWORD PTR s_sf_a[rip], 8
	mov	DWORD PTR s_f_a[rip], 9
	mov	DWORD PTR s_o_a[rip], 11
	mov	DWORD PTR w_sf_a[rip], 1
	mov	DWORD PTR w_tf_a[rip], 1
	mov	DWORD PTR s_v_b[rip], ecx
	mov	DWORD PTR s_p_b[rip], ecx
	mov	DWORD PTR s_sf_b[rip], ecx
	mov	DWORD PTR s_f_b[rip], ecx
	mov	DWORD PTR s_o_b[rip], ecx
	mov	DWORD PTR s_v_a[rip], 10
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z19writer_signal_fencev
	.def	_Z19writer_signal_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z19writer_signal_fencev
_Z19writer_signal_fencev:
.LFB1:
	.seh_endprologue
	mov	DWORD PTR w_sf_a[rip], 1
	mov	DWORD PTR w_sf_b[rip], 2
	mov	eax, DWORD PTR w_sf_a[rip]
	add	eax, 2
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z19writer_thread_fencev
	.def	_Z19writer_thread_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z19writer_thread_fencev
_Z19writer_thread_fencev:
.LFB2:
	.seh_endprologue
	mov	DWORD PTR w_tf_a[rip], 1
	lock or	QWORD PTR [rsp], 0
	mov	DWORD PTR w_tf_b[rip], 2
	mov	eax, DWORD PTR w_tf_a[rip]
	add	eax, 2
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10spin_plainv
	.def	_Z10spin_plainv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10spin_plainv
_Z10spin_plainv:
.LFB3:
	.seh_endprologue
	mov	eax, DWORD PTR s_p_a[rip]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z17spin_signal_fencev
	.def	_Z17spin_signal_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17spin_signal_fencev
_Z17spin_signal_fencev:
.LFB4:
	.seh_endprologue
	mov	edx, DWORD PTR s_sf_b[rip]
	test	edx, edx
	jne	.L7
	.p2align 4
	.p2align 4
	.p2align 3
.L8:
	mov	eax, DWORD PTR s_sf_b[rip]
	test	eax, eax
	je	.L8
.L7:
	mov	eax, DWORD PTR s_sf_a[rip]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z15spin_with_fencev
	.def	_Z15spin_with_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15spin_with_fencev
_Z15spin_with_fencev:
.LFB5:
	.seh_endprologue
	mov	edx, DWORD PTR s_f_b[rip]
	test	edx, edx
	jne	.L11
	.p2align 4
	.p2align 4
	.p2align 3
.L12:
	lock or	QWORD PTR [rsp], 0
	mov	eax, DWORD PTR s_f_b[rip]
	test	eax, eax
	je	.L12
.L11:
	mov	eax, DWORD PTR s_f_a[rip]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z13spin_volatilev
	.def	_Z13spin_volatilev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13spin_volatilev
_Z13spin_volatilev:
.LFB6:
	.seh_endprologue
	mov	edx, 1000000
.L16:
	mov	eax, DWORD PTR s_v_b[rip]
	test	eax, eax
	je	.L18
	mov	eax, DWORD PTR s_v_a[rip]
	ret
	.p2align 4,,10
	.p2align 3
.L18:
	sub	edx, 1
	jne	.L16
	mov	eax, DWORD PTR s_v_a[rip]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z18spin_fence_outsidev
	.def	_Z18spin_fence_outsidev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z18spin_fence_outsidev
_Z18spin_fence_outsidev:
.LFB7:
	.seh_endprologue
	mov	eax, DWORD PTR s_o_a[rip]
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "spin_plain_ret=%d|spin_signal_fence_ret=%d|spin_with_fence_ret=%d|spin_volatile_ret=%d\12\0"
	.align 8
.LC1:
	.ascii "spin_fence_outside_ret=%d|writer_signal_fence_ret=%d|writer_thread_fence_ret=%d\12\0"
	.align 8
.LC2:
	.ascii "functions_present=7|spin_volatile_engaged=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB8:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	ecx, 1
	call	_Z13set_all_flagsi
	call	_Z10spin_plainv
	mov	ecx, eax
	call	_Z17spin_signal_fencev
	mov	r8d, eax
	call	_Z15spin_with_fencev
	mov	r9d, eax
	call	_Z13spin_volatilev
	mov	edx, ecx
	lea	rcx, .LC0[rip]
	mov	ebx, eax
	call	_Z18spin_fence_outsidev
	mov	esi, eax
	call	_Z19writer_signal_fencev
	mov	edi, eax
	call	_Z19writer_thread_fencev
	mov	DWORD PTR 32[rsp], ebx
	mov	ebp, eax
	call	printf
	mov	r9d, ebp
	mov	r8d, edi
	mov	edx, esi
	lea	rcx, .LC1[rip]
	call	printf
	xor	edx, edx
	test	ebx, ebx
	lea	rcx, .LC2[rip]
	setne	dl
	call	printf
	xor	eax, eax
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.globl	s_o_b
	.bss
	.align 4
s_o_b:
	.space 4
	.globl	s_o_a
	.align 4
s_o_a:
	.space 4
	.globl	s_v_b
	.align 4
s_v_b:
	.space 4
	.globl	s_v_a
	.align 4
s_v_a:
	.space 4
	.globl	s_f_b
	.align 4
s_f_b:
	.space 4
	.globl	s_f_a
	.align 4
s_f_a:
	.space 4
	.globl	s_sf_b
	.align 4
s_sf_b:
	.space 4
	.globl	s_sf_a
	.align 4
s_sf_a:
	.space 4
	.globl	s_p_b
	.align 4
s_p_b:
	.space 4
	.globl	s_p_a
	.align 4
s_p_a:
	.space 4
	.globl	w_tf_b
	.align 4
w_tf_b:
	.space 4
	.globl	w_tf_a
	.align 4
w_tf_a:
	.space 4
	.globl	w_sf_b
	.align 4
w_sf_b:
	.space 4
	.globl	w_sf_a
	.align 4
w_sf_a:
	.space 4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	printf;	.scl	2;	.type	32;	.endef
