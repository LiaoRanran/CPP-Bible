	.file	"_ch35_struct_padding.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7read_idPK6Packet
	.def	_Z7read_idPK6Packet;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7read_idPK6Packet
_Z7read_idPK6Packet:
.LFB0:
	.seh_endprologue
	mov	eax, DWORD PTR 4[rcx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10read_valuePK6Packet
	.def	_Z10read_valuePK6Packet;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10read_valuePK6Packet
_Z10read_valuePK6Packet:
.LFB1:
	.seh_endprologue
	movsd	xmm0, QWORD PTR 8[rcx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7set_tagP6Packetc
	.def	_Z7set_tagP6Packetc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7set_tagP6Packetc
_Z7set_tagP6Packetc:
.LFB2:
	.seh_endprologue
	mov	BYTE PTR [rcx], dl
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
