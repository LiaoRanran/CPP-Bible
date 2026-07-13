	.file	"_ch11_mangle.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z1gid
	.def	_Z1gid;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1gid
_Z1gid:
.LFB0:
	.seh_endprologue
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z1hc
	.def	_Z1hc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1hc
_Z1hc:
.LFB1:
	.seh_endprologue
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z1ksPil
	.def	_Z1ksPil;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1ksPil
_Z1ksPil:
.LFB2:
	.seh_endprologue
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z14area_of_circled
	.def	_Z14area_of_circled;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14area_of_circled
_Z14area_of_circled:
.LFB3:
	.seh_endprologue
	movapd	xmm1, xmm0
	movsd	xmm0, QWORD PTR .LC0[rip]
	mulsd	xmm0, xmm1
	mulsd	xmm0, xmm1
	ret
	.seh_endproc
	.p2align 4
	.globl	_ZN2ns1qEi
	.def	_ZN2ns1qEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ns1qEi
_ZN2ns1qEi:
.LFB4:
	.seh_endprologue
	mov	eax, ecx
	ret
	.seh_endproc
	.section	.text$_Z2idIiET_S0_,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z2idIiET_S0_
	.def	_Z2idIiET_S0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z2idIiET_S0_
_Z2idIiET_S0_:
.LFB6:
	.seh_endprologue
	mov	eax, ecx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	1413754136
	.long	1074340347
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
