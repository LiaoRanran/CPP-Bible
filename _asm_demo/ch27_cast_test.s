	.file	"ch27_cast_test.cpp"
	.text
	.p2align 4
	.globl	_Z25static_cast_double_to_intd
	.def	_Z25static_cast_double_to_intd;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z25static_cast_double_to_intd
_Z25static_cast_double_to_intd:
.LFB19:
	.seh_endprologue
	cvttsd2sil	%xmm0, %eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z17const_cast_removePKi
	.def	_Z17const_cast_removePKi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17const_cast_removePKi
_Z17const_cast_removePKi:
.LFB20:
	.seh_endprologue
	movq	%rcx, %rax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z27reinterpret_cast_ptr_to_intPv
	.def	_Z27reinterpret_cast_ptr_to_intPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z27reinterpret_cast_ptr_to_intPv
_Z27reinterpret_cast_ptr_to_intPv:
.LFB21:
	.seh_endprologue
	movq	%rcx, %rax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z19static_cast_to_voidPi
	.def	_Z19static_cast_to_voidPi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z19static_cast_to_voidPi
_Z19static_cast_to_voidPi:
.LFB31:
	.seh_endprologue
	movq	%rcx, %rax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z17dynamic_cast_downP4Base
	.def	_Z17dynamic_cast_downP4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17dynamic_cast_downP4Base
_Z17dynamic_cast_downP4Base:
.LFB26:
	.seh_endprologue
	testq	%rcx, %rcx
	je	.L7
	xorl	%r9d, %r9d
	leaq	_ZTI7Derived(%rip), %r8
	leaq	_ZTI4Base(%rip), %rdx
	jmp	__dynamic_cast
	.p2align 4,,10
	.p2align 3
.L7:
	xorl	%eax, %eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z24implicit_int_from_doubled
	.def	_Z24implicit_int_from_doubled;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z24implicit_int_from_doubled
_Z24implicit_int_from_doubled:
.LFB29:
	.seh_endprologue
	cvttsd2sil	%xmm0, %eax
	ret
	.seh_endproc
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
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	__dynamic_cast;	.scl	2;	.type	32;	.endef
