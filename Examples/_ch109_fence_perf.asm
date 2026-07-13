	.file	"_ch109_fence_perf.cpp"
	.text
	.p2align 4
	.globl	_Z13relaxed_storeRSt6atomicIiEi
	.def	_Z13relaxed_storeRSt6atomicIiEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13relaxed_storeRSt6atomicIiEi
_Z13relaxed_storeRSt6atomicIiEi:
.LFB315:
	.seh_endprologue
	movl	%edx, (%rcx)
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12relaxed_loadRSt6atomicIiE
	.def	_Z12relaxed_loadRSt6atomicIiE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12relaxed_loadRSt6atomicIiE
_Z12relaxed_loadRSt6atomicIiE:
.LFB316:
	.seh_endprologue
	movl	(%rcx), %eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12seqcst_storeRSt6atomicIiEi
	.def	_Z12seqcst_storeRSt6atomicIiEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12seqcst_storeRSt6atomicIiEi
_Z12seqcst_storeRSt6atomicIiEi:
.LFB317:
	.seh_endprologue
	xchgl	(%rcx), %edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12seqcst_fencev
	.def	_Z12seqcst_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12seqcst_fencev
_Z12seqcst_fencev:
.LFB318:
	.seh_endprologue
	lock orq	$0, (%rsp)
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z13acquire_fencev
	.def	_Z13acquire_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13acquire_fencev
_Z13acquire_fencev:
.LFB319:
	.seh_endprologue
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z13release_fencev
	.def	_Z13release_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13release_fencev
_Z13release_fencev:
.LFB320:
	.seh_endprologue
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB321:
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	movl	$1, 44(%rsp)
	movl	44(%rsp), %eax
	movl	$2, %eax
	xchgl	44(%rsp), %eax
	lock orq	$0, (%rsp)
	movl	44(%rsp), %eax
	addq	$56, %rsp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
