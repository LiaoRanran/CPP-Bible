
app_nolto.exe:     file format pei-x86-64


Disassembly of section .text:

0000000140001000 <__mingw_invalidParameterHandler>:
   140001000:	c3                   	ret
   140001001:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   140001008:	00 00 00 00 
   14000100c:	0f 1f 40 00          	nopl   0x0(%rax)

0000000140001010 <pre_c_init>:
   140001010:	48 83 ec 28          	sub    $0x28,%rsp
   140001014:	48 8b 05 c5 33 00 00 	mov    0x33c5(%rip),%rax        # 1400043e0 <.refptr.__mingw_initltsdrot_force>
   14000101b:	31 c9                	xor    %ecx,%ecx
   14000101d:	c7 00 01 00 00 00    	movl   $0x1,(%rax)
   140001023:	48 8b 05 c6 33 00 00 	mov    0x33c6(%rip),%rax        # 1400043f0 <.refptr.__mingw_initltsdyn_force>
   14000102a:	c7 00 01 00 00 00    	movl   $0x1,(%rax)
   140001030:	48 8b 05 c9 33 00 00 	mov    0x33c9(%rip),%rax        # 140004400 <.refptr.__mingw_initltssuo_force>
   140001037:	c7 00 01 00 00 00    	movl   $0x1,(%rax)
   14000103d:	48 8b 05 4c 33 00 00 	mov    0x334c(%rip),%rax        # 140004390 <.refptr.__image_base__>
   140001044:	66 81 38 4d 5a       	cmpw   $0x5a4d,(%rax)
   140001049:	75 0f                	jne    14000105a <pre_c_init+0x4a>
   14000104b:	48 63 50 3c          	movslq 0x3c(%rax),%rdx
   14000104f:	48 01 d0             	add    %rdx,%rax
   140001052:	81 38 50 45 00 00    	cmpl   $0x4550,(%rax)
   140001058:	74 66                	je     1400010c0 <pre_c_init+0xb0>
   14000105a:	48 8b 05 6f 33 00 00 	mov    0x336f(%rip),%rax        # 1400043d0 <.refptr.__mingw_app_type>
   140001061:	89 0d a5 5f 00 00    	mov    %ecx,0x5fa5(%rip)        # 14000700c <managedapp>
   140001067:	8b 00                	mov    (%rax),%eax
   140001069:	85 c0                	test   %eax,%eax
   14000106b:	74 43                	je     1400010b0 <pre_c_init+0xa0>
   14000106d:	b9 02 00 00 00       	mov    $0x2,%ecx
   140001072:	e8 31 15 00 00       	call   1400025a8 <__set_app_type>
   140001077:	e8 b4 14 00 00       	call   140002530 <__p__fmode>
   14000107c:	48 8b 15 1d 34 00 00 	mov    0x341d(%rip),%rdx        # 1400044a0 <.refptr._fmode>
   140001083:	8b 12                	mov    (%rdx),%edx
   140001085:	89 10                	mov    %edx,(%rax)
   140001087:	e8 b4 14 00 00       	call   140002540 <__p__commode>
   14000108c:	48 8b 15 ed 33 00 00 	mov    0x33ed(%rip),%rdx        # 140004480 <.refptr._commode>
   140001093:	8b 12                	mov    (%rdx),%edx
   140001095:	89 10                	mov    %edx,(%rax)
   140001097:	e8 c4 04 00 00       	call   140001560 <_setargv>
   14000109c:	48 8b 05 9d 32 00 00 	mov    0x329d(%rip),%rax        # 140004340 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   1400010a3:	83 38 01             	cmpl   $0x1,(%rax)
   1400010a6:	74 50                	je     1400010f8 <pre_c_init+0xe8>
   1400010a8:	31 c0                	xor    %eax,%eax
   1400010aa:	48 83 c4 28          	add    $0x28,%rsp
   1400010ae:	c3                   	ret
   1400010af:	90                   	nop
   1400010b0:	b9 01 00 00 00       	mov    $0x1,%ecx
   1400010b5:	e8 ee 14 00 00       	call   1400025a8 <__set_app_type>
   1400010ba:	eb bb                	jmp    140001077 <pre_c_init+0x67>
   1400010bc:	0f 1f 40 00          	nopl   0x0(%rax)
   1400010c0:	0f b7 50 18          	movzwl 0x18(%rax),%edx
   1400010c4:	66 81 fa 0b 01       	cmp    $0x10b,%dx
   1400010c9:	74 45                	je     140001110 <pre_c_init+0x100>
   1400010cb:	66 81 fa 0b 02       	cmp    $0x20b,%dx
   1400010d0:	75 88                	jne    14000105a <pre_c_init+0x4a>
   1400010d2:	83 b8 84 00 00 00 0e 	cmpl   $0xe,0x84(%rax)
   1400010d9:	0f 86 7b ff ff ff    	jbe    14000105a <pre_c_init+0x4a>
   1400010df:	8b 90 f8 00 00 00    	mov    0xf8(%rax),%edx
   1400010e5:	31 c9                	xor    %ecx,%ecx
   1400010e7:	85 d2                	test   %edx,%edx
   1400010e9:	0f 95 c1             	setne  %cl
   1400010ec:	e9 69 ff ff ff       	jmp    14000105a <pre_c_init+0x4a>
   1400010f1:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400010f8:	48 8b 0d c1 33 00 00 	mov    0x33c1(%rip),%rcx        # 1400044c0 <.refptr._matherr>
   1400010ff:	e8 cc 0b 00 00       	call   140001cd0 <__mingw_setusermatherr>
   140001104:	31 c0                	xor    %eax,%eax
   140001106:	48 83 c4 28          	add    $0x28,%rsp
   14000110a:	c3                   	ret
   14000110b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001110:	83 78 74 0e          	cmpl   $0xe,0x74(%rax)
   140001114:	0f 86 40 ff ff ff    	jbe    14000105a <pre_c_init+0x4a>
   14000111a:	44 8b 80 e8 00 00 00 	mov    0xe8(%rax),%r8d
   140001121:	31 c9                	xor    %ecx,%ecx
   140001123:	45 85 c0             	test   %r8d,%r8d
   140001126:	0f 95 c1             	setne  %cl
   140001129:	e9 2c ff ff ff       	jmp    14000105a <pre_c_init+0x4a>
   14000112e:	66 90                	xchg   %ax,%ax

0000000140001130 <pre_cpp_init>:
   140001130:	48 83 ec 38          	sub    $0x38,%rsp
   140001134:	48 8b 05 95 33 00 00 	mov    0x3395(%rip),%rax        # 1400044d0 <.refptr._newmode>
   14000113b:	4c 8d 05 d6 5e 00 00 	lea    0x5ed6(%rip),%r8        # 140007018 <envp>
   140001142:	48 8d 15 d7 5e 00 00 	lea    0x5ed7(%rip),%rdx        # 140007020 <argv>
   140001149:	48 8d 0d d8 5e 00 00 	lea    0x5ed8(%rip),%rcx        # 140007028 <argc>
   140001150:	8b 00                	mov    (%rax),%eax
   140001152:	89 05 ac 5e 00 00    	mov    %eax,0x5eac(%rip)        # 140007004 <startinfo>
   140001158:	48 8b 05 31 33 00 00 	mov    0x3331(%rip),%rax        # 140004490 <.refptr._dowildcard>
   14000115f:	44 8b 08             	mov    (%rax),%r9d
   140001162:	48 8d 05 9b 5e 00 00 	lea    0x5e9b(%rip),%rax        # 140007004 <startinfo>
   140001169:	48 89 44 24 20       	mov    %rax,0x20(%rsp)
   14000116e:	e8 25 14 00 00       	call   140002598 <__getmainargs>
   140001173:	90                   	nop
   140001174:	48 83 c4 38          	add    $0x38,%rsp
   140001178:	c3                   	ret
   140001179:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000140001180 <__tmainCRTStartup>:
   140001180:	41 54                	push   %r12
   140001182:	55                   	push   %rbp
   140001183:	57                   	push   %rdi
   140001184:	56                   	push   %rsi
   140001185:	53                   	push   %rbx
   140001186:	48 83 ec 20          	sub    $0x20,%rsp
   14000118a:	48 8b 1d 8f 32 00 00 	mov    0x328f(%rip),%rbx        # 140004420 <.refptr.__native_startup_lock>
   140001191:	31 ff                	xor    %edi,%edi
   140001193:	65 48 8b 04 25 30 00 	mov    %gs:0x30,%rax
   14000119a:	00 00 
   14000119c:	48 8b 2d e9 6f 00 00 	mov    0x6fe9(%rip),%rbp        # 14000818c <__imp_Sleep>
   1400011a3:	48 8b 70 08          	mov    0x8(%rax),%rsi
   1400011a7:	eb 17                	jmp    1400011c0 <__tmainCRTStartup+0x40>
   1400011a9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400011b0:	48 39 c6             	cmp    %rax,%rsi
   1400011b3:	0f 84 67 01 00 00    	je     140001320 <__tmainCRTStartup+0x1a0>
   1400011b9:	b9 e8 03 00 00       	mov    $0x3e8,%ecx
   1400011be:	ff d5                	call   *%rbp
   1400011c0:	48 89 f8             	mov    %rdi,%rax
   1400011c3:	f0 48 0f b1 33       	lock cmpxchg %rsi,(%rbx)
   1400011c8:	48 85 c0             	test   %rax,%rax
   1400011cb:	75 e3                	jne    1400011b0 <__tmainCRTStartup+0x30>
   1400011cd:	48 8b 35 5c 32 00 00 	mov    0x325c(%rip),%rsi        # 140004430 <.refptr.__native_startup_state>
   1400011d4:	31 ff                	xor    %edi,%edi
   1400011d6:	8b 06                	mov    (%rsi),%eax
   1400011d8:	83 f8 01             	cmp    $0x1,%eax
   1400011db:	0f 84 56 01 00 00    	je     140001337 <__tmainCRTStartup+0x1b7>
   1400011e1:	8b 06                	mov    (%rsi),%eax
   1400011e3:	85 c0                	test   %eax,%eax
   1400011e5:	0f 84 b5 01 00 00    	je     1400013a0 <__tmainCRTStartup+0x220>
   1400011eb:	c7 05 13 5e 00 00 01 	movl   $0x1,0x5e13(%rip)        # 140007008 <has_cctor>
   1400011f2:	00 00 00 
   1400011f5:	8b 06                	mov    (%rsi),%eax
   1400011f7:	83 f8 01             	cmp    $0x1,%eax
   1400011fa:	0f 84 4c 01 00 00    	je     14000134c <__tmainCRTStartup+0x1cc>
   140001200:	85 ff                	test   %edi,%edi
   140001202:	0f 84 65 01 00 00    	je     14000136d <__tmainCRTStartup+0x1ed>
   140001208:	48 8b 05 71 31 00 00 	mov    0x3171(%rip),%rax        # 140004380 <.refptr.__dyn_tls_init_callback>
   14000120f:	48 8b 00             	mov    (%rax),%rax
   140001212:	48 85 c0             	test   %rax,%rax
   140001215:	74 0c                	je     140001223 <__tmainCRTStartup+0xa3>
   140001217:	45 31 c0             	xor    %r8d,%r8d
   14000121a:	ba 02 00 00 00       	mov    $0x2,%edx
   14000121f:	31 c9                	xor    %ecx,%ecx
   140001221:	ff d0                	call   *%rax
   140001223:	e8 08 07 00 00       	call   140001930 <_pei386_runtime_relocator>
   140001228:	48 8b 0d 81 32 00 00 	mov    0x3281(%rip),%rcx        # 1400044b0 <.refptr._gnu_exception_handler>
   14000122f:	ff 15 4f 6f 00 00    	call   *0x6f4f(%rip)        # 140008184 <__imp_SetUnhandledExceptionFilter>
   140001235:	48 8b 15 d4 31 00 00 	mov    0x31d4(%rip),%rdx        # 140004410 <.refptr.__mingw_oldexcpt_handler>
   14000123c:	48 8d 0d bd fd ff ff 	lea    -0x243(%rip),%rcx        # 140001000 <__mingw_invalidParameterHandler>
   140001243:	48 89 02             	mov    %rax,(%rdx)
   140001246:	e8 15 13 00 00       	call   140002560 <_set_invalid_parameter_handler>
   14000124b:	e8 f0 04 00 00       	call   140001740 <_fpreset>
   140001250:	8b 1d d2 5d 00 00    	mov    0x5dd2(%rip),%ebx        # 140007028 <argc>
   140001256:	8d 7b 01             	lea    0x1(%rbx),%edi
   140001259:	48 63 ff             	movslq %edi,%rdi
   14000125c:	48 c1 e7 03          	shl    $0x3,%rdi
   140001260:	48 89 f9             	mov    %rdi,%rcx
   140001263:	e8 a0 13 00 00       	call   140002608 <malloc>
   140001268:	85 db                	test   %ebx,%ebx
   14000126a:	48 8b 2d af 5d 00 00 	mov    0x5daf(%rip),%rbp        # 140007020 <argv>
   140001271:	49 89 c4             	mov    %rax,%r12
   140001274:	0f 8e 46 01 00 00    	jle    1400013c0 <__tmainCRTStartup+0x240>
   14000127a:	48 83 ef 08          	sub    $0x8,%rdi
   14000127e:	31 db                	xor    %ebx,%ebx
   140001280:	48 8b 4c 1d 00       	mov    0x0(%rbp,%rbx,1),%rcx
   140001285:	e8 96 13 00 00       	call   140002620 <strlen>
   14000128a:	48 8d 70 01          	lea    0x1(%rax),%rsi
   14000128e:	48 89 f1             	mov    %rsi,%rcx
   140001291:	e8 72 13 00 00       	call   140002608 <malloc>
   140001296:	49 89 f0             	mov    %rsi,%r8
   140001299:	49 89 04 1c          	mov    %rax,(%r12,%rbx,1)
   14000129d:	48 8b 54 1d 00       	mov    0x0(%rbp,%rbx,1),%rdx
   1400012a2:	48 89 c1             	mov    %rax,%rcx
   1400012a5:	48 83 c3 08          	add    $0x8,%rbx
   1400012a9:	e8 62 13 00 00       	call   140002610 <memcpy>
   1400012ae:	48 39 df             	cmp    %rbx,%rdi
   1400012b1:	75 cd                	jne    140001280 <__tmainCRTStartup+0x100>
   1400012b3:	4c 01 e7             	add    %r12,%rdi
   1400012b6:	48 c7 07 00 00 00 00 	movq   $0x0,(%rdi)
   1400012bd:	4c 89 25 5c 5d 00 00 	mov    %r12,0x5d5c(%rip)        # 140007020 <argv>
   1400012c4:	e8 77 02 00 00       	call   140001540 <__main>
   1400012c9:	48 8b 05 d0 30 00 00 	mov    0x30d0(%rip),%rax        # 1400043a0 <.refptr.__imp___initenv>
   1400012d0:	4c 8b 05 41 5d 00 00 	mov    0x5d41(%rip),%r8        # 140007018 <envp>
   1400012d7:	8b 0d 4b 5d 00 00    	mov    0x5d4b(%rip),%ecx        # 140007028 <argc>
   1400012dd:	48 8b 00             	mov    (%rax),%rax
   1400012e0:	4c 89 00             	mov    %r8,(%rax)
   1400012e3:	48 8b 15 36 5d 00 00 	mov    0x5d36(%rip),%rdx        # 140007020 <argv>
   1400012ea:	e8 a1 13 00 00       	call   140002690 <main>
   1400012ef:	8b 0d 17 5d 00 00    	mov    0x5d17(%rip),%ecx        # 14000700c <managedapp>
   1400012f5:	89 05 15 5d 00 00    	mov    %eax,0x5d15(%rip)        # 140007010 <mainret>
   1400012fb:	85 c9                	test   %ecx,%ecx
   1400012fd:	0f 84 c5 00 00 00    	je     1400013c8 <__tmainCRTStartup+0x248>
   140001303:	8b 15 ff 5c 00 00    	mov    0x5cff(%rip),%edx        # 140007008 <has_cctor>
   140001309:	85 d2                	test   %edx,%edx
   14000130b:	74 73                	je     140001380 <__tmainCRTStartup+0x200>
   14000130d:	48 83 c4 20          	add    $0x20,%rsp
   140001311:	5b                   	pop    %rbx
   140001312:	5e                   	pop    %rsi
   140001313:	5f                   	pop    %rdi
   140001314:	5d                   	pop    %rbp
   140001315:	41 5c                	pop    %r12
   140001317:	c3                   	ret
   140001318:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   14000131f:	00 
   140001320:	48 8b 35 09 31 00 00 	mov    0x3109(%rip),%rsi        # 140004430 <.refptr.__native_startup_state>
   140001327:	bf 01 00 00 00       	mov    $0x1,%edi
   14000132c:	8b 06                	mov    (%rsi),%eax
   14000132e:	83 f8 01             	cmp    $0x1,%eax
   140001331:	0f 85 aa fe ff ff    	jne    1400011e1 <__tmainCRTStartup+0x61>
   140001337:	b9 1f 00 00 00       	mov    $0x1f,%ecx
   14000133c:	e8 77 12 00 00       	call   1400025b8 <_amsg_exit>
   140001341:	8b 06                	mov    (%rsi),%eax
   140001343:	83 f8 01             	cmp    $0x1,%eax
   140001346:	0f 85 b4 fe ff ff    	jne    140001200 <__tmainCRTStartup+0x80>
   14000134c:	48 8b 15 fd 30 00 00 	mov    0x30fd(%rip),%rdx        # 140004450 <.refptr.__xc_z>
   140001353:	48 8b 0d e6 30 00 00 	mov    0x30e6(%rip),%rcx        # 140004440 <.refptr.__xc_a>
   14000135a:	e8 69 12 00 00       	call   1400025c8 <_initterm>
   14000135f:	85 ff                	test   %edi,%edi
   140001361:	c7 06 02 00 00 00    	movl   $0x2,(%rsi)
   140001367:	0f 85 9b fe ff ff    	jne    140001208 <__tmainCRTStartup+0x88>
   14000136d:	31 c0                	xor    %eax,%eax
   14000136f:	48 87 03             	xchg   %rax,(%rbx)
   140001372:	e9 91 fe ff ff       	jmp    140001208 <__tmainCRTStartup+0x88>
   140001377:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   14000137e:	00 00 
   140001380:	e8 3b 12 00 00       	call   1400025c0 <_cexit>
   140001385:	8b 05 85 5c 00 00    	mov    0x5c85(%rip),%eax        # 140007010 <mainret>
   14000138b:	48 83 c4 20          	add    $0x20,%rsp
   14000138f:	5b                   	pop    %rbx
   140001390:	5e                   	pop    %rsi
   140001391:	5f                   	pop    %rdi
   140001392:	5d                   	pop    %rbp
   140001393:	41 5c                	pop    %r12
   140001395:	c3                   	ret
   140001396:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000139d:	00 00 00 
   1400013a0:	48 8b 15 c9 30 00 00 	mov    0x30c9(%rip),%rdx        # 140004470 <.refptr.__xi_z>
   1400013a7:	c7 06 01 00 00 00    	movl   $0x1,(%rsi)
   1400013ad:	48 8b 0d ac 30 00 00 	mov    0x30ac(%rip),%rcx        # 140004460 <.refptr.__xi_a>
   1400013b4:	e8 0f 12 00 00       	call   1400025c8 <_initterm>
   1400013b9:	e9 37 fe ff ff       	jmp    1400011f5 <__tmainCRTStartup+0x75>
   1400013be:	66 90                	xchg   %ax,%ax
   1400013c0:	48 89 c7             	mov    %rax,%rdi
   1400013c3:	e9 ee fe ff ff       	jmp    1400012b6 <__tmainCRTStartup+0x136>
   1400013c8:	89 c1                	mov    %eax,%ecx
   1400013ca:	e8 19 12 00 00       	call   1400025e8 <exit>
   1400013cf:	90                   	nop

00000001400013d0 <WinMainCRTStartup>:
   1400013d0:	48 83 ec 28          	sub    $0x28,%rsp

00000001400013d4 <.l_startw>:
   1400013d4:	48 8b 05 f5 2f 00 00 	mov    0x2ff5(%rip),%rax        # 1400043d0 <.refptr.__mingw_app_type>
   1400013db:	c7 00 01 00 00 00    	movl   $0x1,(%rax)
   1400013e1:	e8 9a fd ff ff       	call   140001180 <__tmainCRTStartup>
   1400013e6:	90                   	nop

00000001400013e7 <.l_endw>:
   1400013e7:	90                   	nop
   1400013e8:	48 83 c4 28          	add    $0x28,%rsp
   1400013ec:	c3                   	ret
   1400013ed:	0f 1f 00             	nopl   (%rax)

00000001400013f0 <mainCRTStartup>:
   1400013f0:	48 83 ec 28          	sub    $0x28,%rsp

00000001400013f4 <.l_start>:
   1400013f4:	48 8b 05 d5 2f 00 00 	mov    0x2fd5(%rip),%rax        # 1400043d0 <.refptr.__mingw_app_type>
   1400013fb:	c7 00 00 00 00 00    	movl   $0x0,(%rax)
   140001401:	e8 7a fd ff ff       	call   140001180 <__tmainCRTStartup>
   140001406:	90                   	nop

0000000140001407 <.l_end>:
   140001407:	90                   	nop
   140001408:	48 83 c4 28          	add    $0x28,%rsp
   14000140c:	c3                   	ret
   14000140d:	0f 1f 00             	nopl   (%rax)

0000000140001410 <atexit>:
   140001410:	48 83 ec 28          	sub    $0x28,%rsp
   140001414:	e8 b7 11 00 00       	call   1400025d0 <_onexit>
   140001419:	48 83 f8 01          	cmp    $0x1,%rax
   14000141d:	19 c0                	sbb    %eax,%eax
   14000141f:	48 83 c4 28          	add    $0x28,%rsp
   140001423:	c3                   	ret
   140001424:	90                   	nop
   140001425:	90                   	nop
   140001426:	90                   	nop
   140001427:	90                   	nop
   140001428:	90                   	nop
   140001429:	90                   	nop
   14000142a:	90                   	nop
   14000142b:	90                   	nop
   14000142c:	90                   	nop
   14000142d:	90                   	nop
   14000142e:	90                   	nop
   14000142f:	90                   	nop

0000000140001430 <__gcc_register_frame>:
   140001430:	48 8d 0d 09 00 00 00 	lea    0x9(%rip),%rcx        # 140001440 <__gcc_deregister_frame>
   140001437:	e9 d4 ff ff ff       	jmp    140001410 <atexit>
   14000143c:	0f 1f 40 00          	nopl   0x0(%rax)

0000000140001440 <__gcc_deregister_frame>:
   140001440:	c3                   	ret
   140001441:	90                   	nop
   140001442:	90                   	nop
   140001443:	90                   	nop
   140001444:	90                   	nop
   140001445:	90                   	nop
   140001446:	90                   	nop
   140001447:	90                   	nop
   140001448:	90                   	nop
   140001449:	90                   	nop
   14000144a:	90                   	nop
   14000144b:	90                   	nop
   14000144c:	90                   	nop
   14000144d:	90                   	nop
   14000144e:	90                   	nop
   14000144f:	90                   	nop

0000000140001450 <_Z6driveri>:
   140001450:	56                   	push   %rsi
   140001451:	53                   	push   %rbx
   140001452:	48 83 ec 28          	sub    $0x28,%rsp
   140001456:	89 cb                	mov    %ecx,%ebx
   140001458:	e8 23 00 00 00       	call   140001480 <_Z7computei>
   14000145d:	8d 4b 01             	lea    0x1(%rbx),%ecx
   140001460:	89 c6                	mov    %eax,%esi
   140001462:	e8 19 00 00 00       	call   140001480 <_Z7computei>
   140001467:	01 f0                	add    %esi,%eax
   140001469:	48 83 c4 28          	add    $0x28,%rsp
   14000146d:	5b                   	pop    %rbx
   14000146e:	5e                   	pop    %rsi
   14000146f:	c3                   	ret

0000000140001470 <_Z6helperi>:
   140001470:	8d 44 09 01          	lea    0x1(%rcx,%rcx,1),%eax
   140001474:	c3                   	ret
   140001475:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   14000147c:	00 00 00 00 

0000000140001480 <_Z7computei>:
   140001480:	8d 04 8d 02 00 00 00 	lea    0x2(,%rcx,4),%eax
   140001487:	c3                   	ret
   140001488:	90                   	nop
   140001489:	90                   	nop
   14000148a:	90                   	nop
   14000148b:	90                   	nop
   14000148c:	90                   	nop
   14000148d:	90                   	nop
   14000148e:	90                   	nop
   14000148f:	90                   	nop

0000000140001490 <__do_global_dtors>:
   140001490:	48 83 ec 28          	sub    $0x28,%rsp
   140001494:	48 8b 05 65 1b 00 00 	mov    0x1b65(%rip),%rax        # 140003000 <__data_start__>
   14000149b:	48 8b 00             	mov    (%rax),%rax
   14000149e:	48 85 c0             	test   %rax,%rax
   1400014a1:	74 22                	je     1400014c5 <__do_global_dtors+0x35>
   1400014a3:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   1400014a8:	ff d0                	call   *%rax
   1400014aa:	48 8b 05 4f 1b 00 00 	mov    0x1b4f(%rip),%rax        # 140003000 <__data_start__>
   1400014b1:	48 8d 50 08          	lea    0x8(%rax),%rdx
   1400014b5:	48 8b 40 08          	mov    0x8(%rax),%rax
   1400014b9:	48 89 15 40 1b 00 00 	mov    %rdx,0x1b40(%rip)        # 140003000 <__data_start__>
   1400014c0:	48 85 c0             	test   %rax,%rax
   1400014c3:	75 e3                	jne    1400014a8 <__do_global_dtors+0x18>
   1400014c5:	48 83 c4 28          	add    $0x28,%rsp
   1400014c9:	c3                   	ret
   1400014ca:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)

00000001400014d0 <__do_global_ctors>:
   1400014d0:	56                   	push   %rsi
   1400014d1:	53                   	push   %rbx
   1400014d2:	48 83 ec 28          	sub    $0x28,%rsp
   1400014d6:	48 8b 15 73 2e 00 00 	mov    0x2e73(%rip),%rdx        # 140004350 <.refptr.__CTOR_LIST__>
   1400014dd:	48 8b 02             	mov    (%rdx),%rax
   1400014e0:	83 f8 ff             	cmp    $0xffffffff,%eax
   1400014e3:	89 c1                	mov    %eax,%ecx
   1400014e5:	74 39                	je     140001520 <__do_global_ctors+0x50>
   1400014e7:	85 c9                	test   %ecx,%ecx
   1400014e9:	74 20                	je     14000150b <__do_global_ctors+0x3b>
   1400014eb:	89 c8                	mov    %ecx,%eax
   1400014ed:	83 e9 01             	sub    $0x1,%ecx
   1400014f0:	48 8d 1c c2          	lea    (%rdx,%rax,8),%rbx
   1400014f4:	48 29 c8             	sub    %rcx,%rax
   1400014f7:	48 8d 74 c2 f8       	lea    -0x8(%rdx,%rax,8),%rsi
   1400014fc:	0f 1f 40 00          	nopl   0x0(%rax)
   140001500:	ff 13                	call   *(%rbx)
   140001502:	48 83 eb 08          	sub    $0x8,%rbx
   140001506:	48 39 f3             	cmp    %rsi,%rbx
   140001509:	75 f5                	jne    140001500 <__do_global_ctors+0x30>
   14000150b:	48 8d 0d 7e ff ff ff 	lea    -0x82(%rip),%rcx        # 140001490 <__do_global_dtors>
   140001512:	48 83 c4 28          	add    $0x28,%rsp
   140001516:	5b                   	pop    %rbx
   140001517:	5e                   	pop    %rsi
   140001518:	e9 f3 fe ff ff       	jmp    140001410 <atexit>
   14000151d:	0f 1f 00             	nopl   (%rax)
   140001520:	31 c0                	xor    %eax,%eax
   140001522:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
   140001528:	44 8d 40 01          	lea    0x1(%rax),%r8d
   14000152c:	89 c1                	mov    %eax,%ecx
   14000152e:	4a 83 3c c2 00       	cmpq   $0x0,(%rdx,%r8,8)
   140001533:	4c 89 c0             	mov    %r8,%rax
   140001536:	75 f0                	jne    140001528 <__do_global_ctors+0x58>
   140001538:	eb ad                	jmp    1400014e7 <__do_global_ctors+0x17>
   14000153a:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)

0000000140001540 <__main>:
   140001540:	8b 05 ea 5a 00 00    	mov    0x5aea(%rip),%eax        # 140007030 <initialized>
   140001546:	85 c0                	test   %eax,%eax
   140001548:	74 06                	je     140001550 <__main+0x10>
   14000154a:	c3                   	ret
   14000154b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001550:	c7 05 d6 5a 00 00 01 	movl   $0x1,0x5ad6(%rip)        # 140007030 <initialized>
   140001557:	00 00 00 
   14000155a:	e9 71 ff ff ff       	jmp    1400014d0 <__do_global_ctors>
   14000155f:	90                   	nop

0000000140001560 <_setargv>:
   140001560:	31 c0                	xor    %eax,%eax
   140001562:	c3                   	ret
   140001563:	90                   	nop
   140001564:	90                   	nop
   140001565:	90                   	nop
   140001566:	90                   	nop
   140001567:	90                   	nop
   140001568:	90                   	nop
   140001569:	90                   	nop
   14000156a:	90                   	nop
   14000156b:	90                   	nop
   14000156c:	90                   	nop
   14000156d:	90                   	nop
   14000156e:	90                   	nop
   14000156f:	90                   	nop

0000000140001570 <__dyn_tls_dtor>:
   140001570:	48 83 ec 28          	sub    $0x28,%rsp
   140001574:	83 fa 03             	cmp    $0x3,%edx
   140001577:	74 17                	je     140001590 <__dyn_tls_dtor+0x20>
   140001579:	85 d2                	test   %edx,%edx
   14000157b:	74 13                	je     140001590 <__dyn_tls_dtor+0x20>
   14000157d:	b8 01 00 00 00       	mov    $0x1,%eax
   140001582:	48 83 c4 28          	add    $0x28,%rsp
   140001586:	c3                   	ret
   140001587:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   14000158e:	00 00 
   140001590:	e8 5b 0a 00 00       	call   140001ff0 <__mingw_TLScallback>
   140001595:	b8 01 00 00 00       	mov    $0x1,%eax
   14000159a:	48 83 c4 28          	add    $0x28,%rsp
   14000159e:	c3                   	ret
   14000159f:	90                   	nop

00000001400015a0 <__dyn_tls_init>:
   1400015a0:	56                   	push   %rsi
   1400015a1:	53                   	push   %rbx
   1400015a2:	48 83 ec 28          	sub    $0x28,%rsp
   1400015a6:	48 8b 05 83 2d 00 00 	mov    0x2d83(%rip),%rax        # 140004330 <.refptr._CRT_MT>
   1400015ad:	83 38 02             	cmpl   $0x2,(%rax)
   1400015b0:	74 06                	je     1400015b8 <__dyn_tls_init+0x18>
   1400015b2:	c7 00 02 00 00 00    	movl   $0x2,(%rax)
   1400015b8:	83 fa 02             	cmp    $0x2,%edx
   1400015bb:	74 13                	je     1400015d0 <__dyn_tls_init+0x30>
   1400015bd:	83 fa 01             	cmp    $0x1,%edx
   1400015c0:	74 4e                	je     140001610 <__dyn_tls_init+0x70>
   1400015c2:	b8 01 00 00 00       	mov    $0x1,%eax
   1400015c7:	48 83 c4 28          	add    $0x28,%rsp
   1400015cb:	5b                   	pop    %rbx
   1400015cc:	5e                   	pop    %rsi
   1400015cd:	c3                   	ret
   1400015ce:	66 90                	xchg   %ax,%ax
   1400015d0:	48 8d 1d 81 7a 00 00 	lea    0x7a81(%rip),%rbx        # 140009058 <__xd_z>
   1400015d7:	48 8d 35 7a 7a 00 00 	lea    0x7a7a(%rip),%rsi        # 140009058 <__xd_z>
   1400015de:	48 39 de             	cmp    %rbx,%rsi
   1400015e1:	74 df                	je     1400015c2 <__dyn_tls_init+0x22>
   1400015e3:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   1400015e8:	48 8b 03             	mov    (%rbx),%rax
   1400015eb:	48 85 c0             	test   %rax,%rax
   1400015ee:	74 02                	je     1400015f2 <__dyn_tls_init+0x52>
   1400015f0:	ff d0                	call   *%rax
   1400015f2:	48 83 c3 08          	add    $0x8,%rbx
   1400015f6:	48 39 de             	cmp    %rbx,%rsi
   1400015f9:	75 ed                	jne    1400015e8 <__dyn_tls_init+0x48>
   1400015fb:	b8 01 00 00 00       	mov    $0x1,%eax
   140001600:	48 83 c4 28          	add    $0x28,%rsp
   140001604:	5b                   	pop    %rbx
   140001605:	5e                   	pop    %rsi
   140001606:	c3                   	ret
   140001607:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   14000160e:	00 00 
   140001610:	e8 db 09 00 00       	call   140001ff0 <__mingw_TLScallback>
   140001615:	b8 01 00 00 00       	mov    $0x1,%eax
   14000161a:	48 83 c4 28          	add    $0x28,%rsp
   14000161e:	5b                   	pop    %rbx
   14000161f:	5e                   	pop    %rsi
   140001620:	c3                   	ret
   140001621:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   140001628:	00 00 00 00 
   14000162c:	0f 1f 40 00          	nopl   0x0(%rax)

0000000140001630 <__tlregdtor>:
   140001630:	31 c0                	xor    %eax,%eax
   140001632:	c3                   	ret
   140001633:	90                   	nop
   140001634:	90                   	nop
   140001635:	90                   	nop
   140001636:	90                   	nop
   140001637:	90                   	nop
   140001638:	90                   	nop
   140001639:	90                   	nop
   14000163a:	90                   	nop
   14000163b:	90                   	nop
   14000163c:	90                   	nop
   14000163d:	90                   	nop
   14000163e:	90                   	nop
   14000163f:	90                   	nop

0000000140001640 <_matherr>:
   140001640:	56                   	push   %rsi
   140001641:	53                   	push   %rbx
   140001642:	48 83 ec 78          	sub    $0x78,%rsp
   140001646:	0f 29 74 24 40       	movaps %xmm6,0x40(%rsp)
   14000164b:	0f 29 7c 24 50       	movaps %xmm7,0x50(%rsp)
   140001650:	44 0f 29 44 24 60    	movaps %xmm8,0x60(%rsp)
   140001656:	83 39 06             	cmpl   $0x6,(%rcx)
   140001659:	0f 87 cd 00 00 00    	ja     14000172c <_matherr+0xec>
   14000165f:	8b 01                	mov    (%rcx),%eax
   140001661:	48 8d 15 1c 2b 00 00 	lea    0x2b1c(%rip),%rdx        # 140004184 <.rdata+0x124>
   140001668:	48 63 04 82          	movslq (%rdx,%rax,4),%rax
   14000166c:	48 01 d0             	add    %rdx,%rax
   14000166f:	ff e0                	jmp    *%rax
   140001671:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140001678:	48 8d 1d 00 2a 00 00 	lea    0x2a00(%rip),%rbx        # 14000407f <.rdata+0x1f>
   14000167f:	48 8b 71 08          	mov    0x8(%rcx),%rsi
   140001683:	f2 44 0f 10 41 20    	movsd  0x20(%rcx),%xmm8
   140001689:	f2 0f 10 79 18       	movsd  0x18(%rcx),%xmm7
   14000168e:	f2 0f 10 71 10       	movsd  0x10(%rcx),%xmm6
   140001693:	b9 02 00 00 00       	mov    $0x2,%ecx
   140001698:	e8 d3 0e 00 00       	call   140002570 <__acrt_iob_func>
   14000169d:	f2 44 0f 11 44 24 30 	movsd  %xmm8,0x30(%rsp)
   1400016a4:	49 89 f1             	mov    %rsi,%r9
   1400016a7:	49 89 d8             	mov    %rbx,%r8
   1400016aa:	f2 0f 11 7c 24 28    	movsd  %xmm7,0x28(%rsp)
   1400016b0:	48 89 c1             	mov    %rax,%rcx
   1400016b3:	f2 0f 11 74 24 20    	movsd  %xmm6,0x20(%rsp)
   1400016b9:	48 8d 15 98 2a 00 00 	lea    0x2a98(%rip),%rdx        # 140004158 <.rdata+0xf8>
   1400016c0:	e8 2b 0f 00 00       	call   1400025f0 <fprintf>
   1400016c5:	90                   	nop
   1400016c6:	0f 28 74 24 40       	movaps 0x40(%rsp),%xmm6
   1400016cb:	31 c0                	xor    %eax,%eax
   1400016cd:	0f 28 7c 24 50       	movaps 0x50(%rsp),%xmm7
   1400016d2:	44 0f 28 44 24 60    	movaps 0x60(%rsp),%xmm8
   1400016d8:	48 83 c4 78          	add    $0x78,%rsp
   1400016dc:	5b                   	pop    %rbx
   1400016dd:	5e                   	pop    %rsi
   1400016de:	c3                   	ret
   1400016df:	90                   	nop
   1400016e0:	48 8d 1d 79 29 00 00 	lea    0x2979(%rip),%rbx        # 140004060 <.rdata>
   1400016e7:	eb 96                	jmp    14000167f <_matherr+0x3f>
   1400016e9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400016f0:	48 8d 1d c9 29 00 00 	lea    0x29c9(%rip),%rbx        # 1400040c0 <.rdata+0x60>
   1400016f7:	eb 86                	jmp    14000167f <_matherr+0x3f>
   1400016f9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140001700:	48 8d 1d 99 29 00 00 	lea    0x2999(%rip),%rbx        # 1400040a0 <.rdata+0x40>
   140001707:	e9 73 ff ff ff       	jmp    14000167f <_matherr+0x3f>
   14000170c:	0f 1f 40 00          	nopl   0x0(%rax)
   140001710:	48 8d 1d f9 29 00 00 	lea    0x29f9(%rip),%rbx        # 140004110 <.rdata+0xb0>
   140001717:	e9 63 ff ff ff       	jmp    14000167f <_matherr+0x3f>
   14000171c:	0f 1f 40 00          	nopl   0x0(%rax)
   140001720:	48 8d 1d c1 29 00 00 	lea    0x29c1(%rip),%rbx        # 1400040e8 <.rdata+0x88>
   140001727:	e9 53 ff ff ff       	jmp    14000167f <_matherr+0x3f>
   14000172c:	48 8d 1d 13 2a 00 00 	lea    0x2a13(%rip),%rbx        # 140004146 <.rdata+0xe6>
   140001733:	e9 47 ff ff ff       	jmp    14000167f <_matherr+0x3f>
   140001738:	90                   	nop
   140001739:	90                   	nop
   14000173a:	90                   	nop
   14000173b:	90                   	nop
   14000173c:	90                   	nop
   14000173d:	90                   	nop
   14000173e:	90                   	nop
   14000173f:	90                   	nop

0000000140001740 <_fpreset>:
   140001740:	db e3                	fninit
   140001742:	c3                   	ret
   140001743:	90                   	nop
   140001744:	90                   	nop
   140001745:	90                   	nop
   140001746:	90                   	nop
   140001747:	90                   	nop
   140001748:	90                   	nop
   140001749:	90                   	nop
   14000174a:	90                   	nop
   14000174b:	90                   	nop
   14000174c:	90                   	nop
   14000174d:	90                   	nop
   14000174e:	90                   	nop
   14000174f:	90                   	nop

0000000140001750 <__report_error>:
   140001750:	56                   	push   %rsi
   140001751:	53                   	push   %rbx
   140001752:	48 83 ec 38          	sub    $0x38,%rsp
   140001756:	48 8d 44 24 58       	lea    0x58(%rsp),%rax
   14000175b:	48 89 cb             	mov    %rcx,%rbx
   14000175e:	b9 02 00 00 00       	mov    $0x2,%ecx
   140001763:	48 89 54 24 58       	mov    %rdx,0x58(%rsp)
   140001768:	4c 89 44 24 60       	mov    %r8,0x60(%rsp)
   14000176d:	4c 89 4c 24 68       	mov    %r9,0x68(%rsp)
   140001772:	48 89 44 24 28       	mov    %rax,0x28(%rsp)
   140001777:	e8 f4 0d 00 00       	call   140002570 <__acrt_iob_func>
   14000177c:	41 b8 1b 00 00 00    	mov    $0x1b,%r8d
   140001782:	ba 01 00 00 00       	mov    $0x1,%edx
   140001787:	48 8d 0d 12 2a 00 00 	lea    0x2a12(%rip),%rcx        # 1400041a0 <.rdata>
   14000178e:	49 89 c1             	mov    %rax,%r9
   140001791:	e8 6a 0e 00 00       	call   140002600 <fwrite>
   140001796:	48 8b 74 24 28       	mov    0x28(%rsp),%rsi
   14000179b:	b9 02 00 00 00       	mov    $0x2,%ecx
   1400017a0:	e8 cb 0d 00 00       	call   140002570 <__acrt_iob_func>
   1400017a5:	48 89 da             	mov    %rbx,%rdx
   1400017a8:	48 89 c1             	mov    %rax,%rcx
   1400017ab:	49 89 f0             	mov    %rsi,%r8
   1400017ae:	e8 7d 0e 00 00       	call   140002630 <vfprintf>
   1400017b3:	e8 20 0e 00 00       	call   1400025d8 <abort>
   1400017b8:	90                   	nop
   1400017b9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

00000001400017c0 <mark_section_writable>:
   1400017c0:	57                   	push   %rdi
   1400017c1:	56                   	push   %rsi
   1400017c2:	53                   	push   %rbx
   1400017c3:	48 83 ec 50          	sub    $0x50,%rsp
   1400017c7:	48 63 35 c6 58 00 00 	movslq 0x58c6(%rip),%rsi        # 140007094 <maxSections>
   1400017ce:	85 f6                	test   %esi,%esi
   1400017d0:	48 89 cb             	mov    %rcx,%rbx
   1400017d3:	0f 8e 17 01 00 00    	jle    1400018f0 <mark_section_writable+0x130>
   1400017d9:	48 8b 05 b8 58 00 00 	mov    0x58b8(%rip),%rax        # 140007098 <the_secs>
   1400017e0:	45 31 c9             	xor    %r9d,%r9d
   1400017e3:	48 83 c0 18          	add    $0x18,%rax
   1400017e7:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   1400017ee:	00 00 
   1400017f0:	4c 8b 00             	mov    (%rax),%r8
   1400017f3:	4c 39 c3             	cmp    %r8,%rbx
   1400017f6:	72 13                	jb     14000180b <mark_section_writable+0x4b>
   1400017f8:	48 8b 50 08          	mov    0x8(%rax),%rdx
   1400017fc:	8b 52 08             	mov    0x8(%rdx),%edx
   1400017ff:	49 01 d0             	add    %rdx,%r8
   140001802:	4c 39 c3             	cmp    %r8,%rbx
   140001805:	0f 82 8a 00 00 00    	jb     140001895 <mark_section_writable+0xd5>
   14000180b:	41 83 c1 01          	add    $0x1,%r9d
   14000180f:	48 83 c0 28          	add    $0x28,%rax
   140001813:	41 39 f1             	cmp    %esi,%r9d
   140001816:	75 d8                	jne    1400017f0 <mark_section_writable+0x30>
   140001818:	48 89 d9             	mov    %rbx,%rcx
   14000181b:	e8 f0 09 00 00       	call   140002210 <__mingw_GetSectionForAddress>
   140001820:	48 85 c0             	test   %rax,%rax
   140001823:	48 89 c7             	mov    %rax,%rdi
   140001826:	0f 84 e6 00 00 00    	je     140001912 <mark_section_writable+0x152>
   14000182c:	48 8b 05 65 58 00 00 	mov    0x5865(%rip),%rax        # 140007098 <the_secs>
   140001833:	48 8d 1c b6          	lea    (%rsi,%rsi,4),%rbx
   140001837:	48 c1 e3 03          	shl    $0x3,%rbx
   14000183b:	48 01 d8             	add    %rbx,%rax
   14000183e:	48 89 78 20          	mov    %rdi,0x20(%rax)
   140001842:	c7 00 00 00 00 00    	movl   $0x0,(%rax)
   140001848:	e8 03 0b 00 00       	call   140002350 <_GetPEImageBase>
   14000184d:	8b 57 0c             	mov    0xc(%rdi),%edx
   140001850:	41 b8 30 00 00 00    	mov    $0x30,%r8d
   140001856:	48 8d 0c 10          	lea    (%rax,%rdx,1),%rcx
   14000185a:	48 8b 05 37 58 00 00 	mov    0x5837(%rip),%rax        # 140007098 <the_secs>
   140001861:	48 8d 54 24 20       	lea    0x20(%rsp),%rdx
   140001866:	48 89 4c 18 18       	mov    %rcx,0x18(%rax,%rbx,1)
   14000186b:	ff 15 33 69 00 00    	call   *0x6933(%rip)        # 1400081a4 <__imp_VirtualQuery>
   140001871:	48 85 c0             	test   %rax,%rax
   140001874:	0f 84 7d 00 00 00    	je     1400018f7 <mark_section_writable+0x137>
   14000187a:	8b 44 24 44          	mov    0x44(%rsp),%eax
   14000187e:	8d 50 c0             	lea    -0x40(%rax),%edx
   140001881:	83 e2 bf             	and    $0xffffffbf,%edx
   140001884:	74 08                	je     14000188e <mark_section_writable+0xce>
   140001886:	8d 50 fc             	lea    -0x4(%rax),%edx
   140001889:	83 e2 fb             	and    $0xfffffffb,%edx
   14000188c:	75 12                	jne    1400018a0 <mark_section_writable+0xe0>
   14000188e:	83 05 ff 57 00 00 01 	addl   $0x1,0x57ff(%rip)        # 140007094 <maxSections>
   140001895:	48 83 c4 50          	add    $0x50,%rsp
   140001899:	5b                   	pop    %rbx
   14000189a:	5e                   	pop    %rsi
   14000189b:	5f                   	pop    %rdi
   14000189c:	c3                   	ret
   14000189d:	0f 1f 00             	nopl   (%rax)
   1400018a0:	83 f8 02             	cmp    $0x2,%eax
   1400018a3:	41 b8 40 00 00 00    	mov    $0x40,%r8d
   1400018a9:	b8 04 00 00 00       	mov    $0x4,%eax
   1400018ae:	48 8b 4c 24 20       	mov    0x20(%rsp),%rcx
   1400018b3:	44 0f 44 c0          	cmove  %eax,%r8d
   1400018b7:	48 8b 54 24 38       	mov    0x38(%rsp),%rdx
   1400018bc:	48 03 1d d5 57 00 00 	add    0x57d5(%rip),%rbx        # 140007098 <the_secs>
   1400018c3:	49 89 d9             	mov    %rbx,%r9
   1400018c6:	48 89 4b 08          	mov    %rcx,0x8(%rbx)
   1400018ca:	48 89 53 10          	mov    %rdx,0x10(%rbx)
   1400018ce:	ff 15 c8 68 00 00    	call   *0x68c8(%rip)        # 14000819c <__imp_VirtualProtect>
   1400018d4:	85 c0                	test   %eax,%eax
   1400018d6:	75 b6                	jne    14000188e <mark_section_writable+0xce>
   1400018d8:	ff 15 8e 68 00 00    	call   *0x688e(%rip)        # 14000816c <__imp_GetLastError>
   1400018de:	48 8d 0d 33 29 00 00 	lea    0x2933(%rip),%rcx        # 140004218 <.rdata+0x78>
   1400018e5:	89 c2                	mov    %eax,%edx
   1400018e7:	e8 64 fe ff ff       	call   140001750 <__report_error>
   1400018ec:	0f 1f 40 00          	nopl   0x0(%rax)
   1400018f0:	31 f6                	xor    %esi,%esi
   1400018f2:	e9 21 ff ff ff       	jmp    140001818 <mark_section_writable+0x58>
   1400018f7:	48 8b 05 9a 57 00 00 	mov    0x579a(%rip),%rax        # 140007098 <the_secs>
   1400018fe:	48 8d 0d db 28 00 00 	lea    0x28db(%rip),%rcx        # 1400041e0 <.rdata+0x40>
   140001905:	8b 57 08             	mov    0x8(%rdi),%edx
   140001908:	4c 8b 44 18 18       	mov    0x18(%rax,%rbx,1),%r8
   14000190d:	e8 3e fe ff ff       	call   140001750 <__report_error>
   140001912:	48 8d 0d a7 28 00 00 	lea    0x28a7(%rip),%rcx        # 1400041c0 <.rdata+0x20>
   140001919:	48 89 da             	mov    %rbx,%rdx
   14000191c:	e8 2f fe ff ff       	call   140001750 <__report_error>
   140001921:	90                   	nop
   140001922:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   140001929:	00 00 00 00 
   14000192d:	0f 1f 00             	nopl   (%rax)

0000000140001930 <_pei386_runtime_relocator>:
   140001930:	55                   	push   %rbp
   140001931:	41 57                	push   %r15
   140001933:	41 56                	push   %r14
   140001935:	41 55                	push   %r13
   140001937:	41 54                	push   %r12
   140001939:	57                   	push   %rdi
   14000193a:	56                   	push   %rsi
   14000193b:	53                   	push   %rbx
   14000193c:	48 83 ec 48          	sub    $0x48,%rsp
   140001940:	48 8d 6c 24 40       	lea    0x40(%rsp),%rbp
   140001945:	8b 3d 45 57 00 00    	mov    0x5745(%rip),%edi        # 140007090 <was_init.0>
   14000194b:	85 ff                	test   %edi,%edi
   14000194d:	74 11                	je     140001960 <_pei386_runtime_relocator+0x30>
   14000194f:	48 8d 65 08          	lea    0x8(%rbp),%rsp
   140001953:	5b                   	pop    %rbx
   140001954:	5e                   	pop    %rsi
   140001955:	5f                   	pop    %rdi
   140001956:	41 5c                	pop    %r12
   140001958:	41 5d                	pop    %r13
   14000195a:	41 5e                	pop    %r14
   14000195c:	41 5f                	pop    %r15
   14000195e:	5d                   	pop    %rbp
   14000195f:	c3                   	ret
   140001960:	c7 05 26 57 00 00 01 	movl   $0x1,0x5726(%rip)        # 140007090 <was_init.0>
   140001967:	00 00 00 
   14000196a:	e8 21 09 00 00       	call   140002290 <__mingw_GetSectionCount>
   14000196f:	48 98                	cltq
   140001971:	48 8d 04 80          	lea    (%rax,%rax,4),%rax
   140001975:	48 8d 04 c5 0f 00 00 	lea    0xf(,%rax,8),%rax
   14000197c:	00 
   14000197d:	48 83 e0 f0          	and    $0xfffffffffffffff0,%rax
   140001981:	e8 6a 0b 00 00       	call   1400024f0 <___chkstk_ms>
   140001986:	4c 8b 2d d3 29 00 00 	mov    0x29d3(%rip),%r13        # 140004360 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   14000198d:	c7 05 fd 56 00 00 00 	movl   $0x0,0x56fd(%rip)        # 140007094 <maxSections>
   140001994:	00 00 00 
   140001997:	48 8b 1d d2 29 00 00 	mov    0x29d2(%rip),%rbx        # 140004370 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000199e:	48 29 c4             	sub    %rax,%rsp
   1400019a1:	48 8d 44 24 30       	lea    0x30(%rsp),%rax
   1400019a6:	48 89 05 eb 56 00 00 	mov    %rax,0x56eb(%rip)        # 140007098 <the_secs>
   1400019ad:	4c 89 e8             	mov    %r13,%rax
   1400019b0:	48 29 d8             	sub    %rbx,%rax
   1400019b3:	48 83 f8 07          	cmp    $0x7,%rax
   1400019b7:	7e 96                	jle    14000194f <_pei386_runtime_relocator+0x1f>
   1400019b9:	48 83 f8 0b          	cmp    $0xb,%rax
   1400019bd:	8b 13                	mov    (%rbx),%edx
   1400019bf:	0f 8f 83 01 00 00    	jg     140001b48 <_pei386_runtime_relocator+0x218>
   1400019c5:	8b 03                	mov    (%rbx),%eax
   1400019c7:	85 c0                	test   %eax,%eax
   1400019c9:	0f 85 71 02 00 00    	jne    140001c40 <_pei386_runtime_relocator+0x310>
   1400019cf:	8b 43 04             	mov    0x4(%rbx),%eax
   1400019d2:	85 c0                	test   %eax,%eax
   1400019d4:	0f 85 66 02 00 00    	jne    140001c40 <_pei386_runtime_relocator+0x310>
   1400019da:	8b 53 08             	mov    0x8(%rbx),%edx
   1400019dd:	83 fa 01             	cmp    $0x1,%edx
   1400019e0:	0f 85 9c 02 00 00    	jne    140001c82 <_pei386_runtime_relocator+0x352>
   1400019e6:	48 83 c3 0c          	add    $0xc,%rbx
   1400019ea:	4c 39 eb             	cmp    %r13,%rbx
   1400019ed:	0f 83 5c ff ff ff    	jae    14000194f <_pei386_runtime_relocator+0x1f>
   1400019f3:	4c 8b 25 96 29 00 00 	mov    0x2996(%rip),%r12        # 140004390 <.refptr.__image_base__>
   1400019fa:	49 bf ff ff ff 7f ff 	movabs $0xffffffff7fffffff,%r15
   140001a01:	ff ff ff 
   140001a04:	eb 5d                	jmp    140001a63 <_pei386_runtime_relocator+0x133>
   140001a06:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   140001a0d:	00 00 00 
   140001a10:	41 0f b6 36          	movzbl (%r14),%esi
   140001a14:	81 e1 c0 00 00 00    	and    $0xc0,%ecx
   140001a1a:	40 84 f6             	test   %sil,%sil
   140001a1d:	0f 89 05 02 00 00    	jns    140001c28 <_pei386_runtime_relocator+0x2f8>
   140001a23:	48 81 ce 00 ff ff ff 	or     $0xffffffffffffff00,%rsi
   140001a2a:	48 29 c6             	sub    %rax,%rsi
   140001a2d:	4c 01 ce             	add    %r9,%rsi
   140001a30:	85 c9                	test   %ecx,%ecx
   140001a32:	75 17                	jne    140001a4b <_pei386_runtime_relocator+0x11b>
   140001a34:	48 81 fe ff 00 00 00 	cmp    $0xff,%rsi
   140001a3b:	0f 8f 4e 01 00 00    	jg     140001b8f <_pei386_runtime_relocator+0x25f>
   140001a41:	48 83 fe 80          	cmp    $0xffffffffffffff80,%rsi
   140001a45:	0f 8c 44 01 00 00    	jl     140001b8f <_pei386_runtime_relocator+0x25f>
   140001a4b:	4c 89 f1             	mov    %r14,%rcx
   140001a4e:	e8 6d fd ff ff       	call   1400017c0 <mark_section_writable>
   140001a53:	41 88 36             	mov    %sil,(%r14)
   140001a56:	48 83 c3 0c          	add    $0xc,%rbx
   140001a5a:	4c 39 eb             	cmp    %r13,%rbx
   140001a5d:	0f 83 8d 00 00 00    	jae    140001af0 <_pei386_runtime_relocator+0x1c0>
   140001a63:	8b 4b 08             	mov    0x8(%rbx),%ecx
   140001a66:	8b 03                	mov    (%rbx),%eax
   140001a68:	44 8b 43 04          	mov    0x4(%rbx),%r8d
   140001a6c:	0f b6 d1             	movzbl %cl,%edx
   140001a6f:	4c 01 e0             	add    %r12,%rax
   140001a72:	83 fa 20             	cmp    $0x20,%edx
   140001a75:	4c 8b 08             	mov    (%rax),%r9
   140001a78:	4f 8d 34 20          	lea    (%r8,%r12,1),%r14
   140001a7c:	0f 84 26 01 00 00    	je     140001ba8 <_pei386_runtime_relocator+0x278>
   140001a82:	0f 87 e8 00 00 00    	ja     140001b70 <_pei386_runtime_relocator+0x240>
   140001a88:	83 fa 08             	cmp    $0x8,%edx
   140001a8b:	74 83                	je     140001a10 <_pei386_runtime_relocator+0xe0>
   140001a8d:	83 fa 10             	cmp    $0x10,%edx
   140001a90:	0f 85 e0 01 00 00    	jne    140001c76 <_pei386_runtime_relocator+0x346>
   140001a96:	41 0f b7 36          	movzwl (%r14),%esi
   140001a9a:	81 e1 c0 00 00 00    	and    $0xc0,%ecx
   140001aa0:	66 85 f6             	test   %si,%si
   140001aa3:	0f 89 67 01 00 00    	jns    140001c10 <_pei386_runtime_relocator+0x2e0>
   140001aa9:	48 81 ce 00 00 ff ff 	or     $0xffffffffffff0000,%rsi
   140001ab0:	48 29 c6             	sub    %rax,%rsi
   140001ab3:	4c 01 ce             	add    %r9,%rsi
   140001ab6:	85 c9                	test   %ecx,%ecx
   140001ab8:	75 1a                	jne    140001ad4 <_pei386_runtime_relocator+0x1a4>
   140001aba:	48 81 fe 00 80 ff ff 	cmp    $0xffffffffffff8000,%rsi
   140001ac1:	0f 8c c8 00 00 00    	jl     140001b8f <_pei386_runtime_relocator+0x25f>
   140001ac7:	48 81 fe ff ff 00 00 	cmp    $0xffff,%rsi
   140001ace:	0f 8f bb 00 00 00    	jg     140001b8f <_pei386_runtime_relocator+0x25f>
   140001ad4:	4c 89 f1             	mov    %r14,%rcx
   140001ad7:	48 83 c3 0c          	add    $0xc,%rbx
   140001adb:	e8 e0 fc ff ff       	call   1400017c0 <mark_section_writable>
   140001ae0:	4c 39 eb             	cmp    %r13,%rbx
   140001ae3:	66 41 89 36          	mov    %si,(%r14)
   140001ae7:	0f 82 76 ff ff ff    	jb     140001a63 <_pei386_runtime_relocator+0x133>
   140001aed:	0f 1f 00             	nopl   (%rax)
   140001af0:	8b 15 9e 55 00 00    	mov    0x559e(%rip),%edx        # 140007094 <maxSections>
   140001af6:	85 d2                	test   %edx,%edx
   140001af8:	0f 8e 51 fe ff ff    	jle    14000194f <_pei386_runtime_relocator+0x1f>
   140001afe:	48 8b 35 97 66 00 00 	mov    0x6697(%rip),%rsi        # 14000819c <__imp_VirtualProtect>
   140001b05:	4c 8d 65 fc          	lea    -0x4(%rbp),%r12
   140001b09:	31 db                	xor    %ebx,%ebx
   140001b0b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001b10:	48 8b 05 81 55 00 00 	mov    0x5581(%rip),%rax        # 140007098 <the_secs>
   140001b17:	48 01 d8             	add    %rbx,%rax
   140001b1a:	44 8b 00             	mov    (%rax),%r8d
   140001b1d:	45 85 c0             	test   %r8d,%r8d
   140001b20:	74 0d                	je     140001b2f <_pei386_runtime_relocator+0x1ff>
   140001b22:	48 8b 50 10          	mov    0x10(%rax),%rdx
   140001b26:	4d 89 e1             	mov    %r12,%r9
   140001b29:	48 8b 48 08          	mov    0x8(%rax),%rcx
   140001b2d:	ff d6                	call   *%rsi
   140001b2f:	83 c7 01             	add    $0x1,%edi
   140001b32:	48 83 c3 28          	add    $0x28,%rbx
   140001b36:	3b 3d 58 55 00 00    	cmp    0x5558(%rip),%edi        # 140007094 <maxSections>
   140001b3c:	7c d2                	jl     140001b10 <_pei386_runtime_relocator+0x1e0>
   140001b3e:	e9 0c fe ff ff       	jmp    14000194f <_pei386_runtime_relocator+0x1f>
   140001b43:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001b48:	85 d2                	test   %edx,%edx
   140001b4a:	0f 85 f0 00 00 00    	jne    140001c40 <_pei386_runtime_relocator+0x310>
   140001b50:	8b 43 04             	mov    0x4(%rbx),%eax
   140001b53:	89 c2                	mov    %eax,%edx
   140001b55:	0b 53 08             	or     0x8(%rbx),%edx
   140001b58:	0f 85 74 fe ff ff    	jne    1400019d2 <_pei386_runtime_relocator+0xa2>
   140001b5e:	48 83 c3 0c          	add    $0xc,%rbx
   140001b62:	e9 5e fe ff ff       	jmp    1400019c5 <_pei386_runtime_relocator+0x95>
   140001b67:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   140001b6e:	00 00 
   140001b70:	83 fa 40             	cmp    $0x40,%edx
   140001b73:	0f 85 fd 00 00 00    	jne    140001c76 <_pei386_runtime_relocator+0x346>
   140001b79:	49 8b 36             	mov    (%r14),%rsi
   140001b7c:	48 29 c6             	sub    %rax,%rsi
   140001b7f:	4c 01 ce             	add    %r9,%rsi
   140001b82:	81 e1 c0 00 00 00    	and    $0xc0,%ecx
   140001b88:	75 66                	jne    140001bf0 <_pei386_runtime_relocator+0x2c0>
   140001b8a:	48 85 f6             	test   %rsi,%rsi
   140001b8d:	78 61                	js     140001bf0 <_pei386_runtime_relocator+0x2c0>
   140001b8f:	48 89 74 24 20       	mov    %rsi,0x20(%rsp)
   140001b94:	48 8d 0d 0d 27 00 00 	lea    0x270d(%rip),%rcx        # 1400042a8 <.rdata+0x108>
   140001b9b:	4d 89 f0             	mov    %r14,%r8
   140001b9e:	e8 ad fb ff ff       	call   140001750 <__report_error>
   140001ba3:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001ba8:	41 8b 36             	mov    (%r14),%esi
   140001bab:	81 e1 c0 00 00 00    	and    $0xc0,%ecx
   140001bb1:	85 f6                	test   %esi,%esi
   140001bb3:	79 4b                	jns    140001c00 <_pei386_runtime_relocator+0x2d0>
   140001bb5:	49 bb 00 00 00 00 ff 	movabs $0xffffffff00000000,%r11
   140001bbc:	ff ff ff 
   140001bbf:	4c 09 de             	or     %r11,%rsi
   140001bc2:	48 29 c6             	sub    %rax,%rsi
   140001bc5:	4c 01 ce             	add    %r9,%rsi
   140001bc8:	85 c9                	test   %ecx,%ecx
   140001bca:	75 0f                	jne    140001bdb <_pei386_runtime_relocator+0x2ab>
   140001bcc:	4c 39 fe             	cmp    %r15,%rsi
   140001bcf:	7e be                	jle    140001b8f <_pei386_runtime_relocator+0x25f>
   140001bd1:	b8 ff ff ff ff       	mov    $0xffffffff,%eax
   140001bd6:	48 39 c6             	cmp    %rax,%rsi
   140001bd9:	7f b4                	jg     140001b8f <_pei386_runtime_relocator+0x25f>
   140001bdb:	4c 89 f1             	mov    %r14,%rcx
   140001bde:	e8 dd fb ff ff       	call   1400017c0 <mark_section_writable>
   140001be3:	41 89 36             	mov    %esi,(%r14)
   140001be6:	e9 6b fe ff ff       	jmp    140001a56 <_pei386_runtime_relocator+0x126>
   140001beb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001bf0:	4c 89 f1             	mov    %r14,%rcx
   140001bf3:	e8 c8 fb ff ff       	call   1400017c0 <mark_section_writable>
   140001bf8:	49 89 36             	mov    %rsi,(%r14)
   140001bfb:	e9 56 fe ff ff       	jmp    140001a56 <_pei386_runtime_relocator+0x126>
   140001c00:	48 29 c6             	sub    %rax,%rsi
   140001c03:	4c 01 ce             	add    %r9,%rsi
   140001c06:	85 c9                	test   %ecx,%ecx
   140001c08:	74 c2                	je     140001bcc <_pei386_runtime_relocator+0x29c>
   140001c0a:	eb cf                	jmp    140001bdb <_pei386_runtime_relocator+0x2ab>
   140001c0c:	0f 1f 40 00          	nopl   0x0(%rax)
   140001c10:	48 29 c6             	sub    %rax,%rsi
   140001c13:	4c 01 ce             	add    %r9,%rsi
   140001c16:	85 c9                	test   %ecx,%ecx
   140001c18:	0f 84 9c fe ff ff    	je     140001aba <_pei386_runtime_relocator+0x18a>
   140001c1e:	e9 b1 fe ff ff       	jmp    140001ad4 <_pei386_runtime_relocator+0x1a4>
   140001c23:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001c28:	48 29 c6             	sub    %rax,%rsi
   140001c2b:	4c 01 ce             	add    %r9,%rsi
   140001c2e:	85 c9                	test   %ecx,%ecx
   140001c30:	0f 84 fe fd ff ff    	je     140001a34 <_pei386_runtime_relocator+0x104>
   140001c36:	e9 10 fe ff ff       	jmp    140001a4b <_pei386_runtime_relocator+0x11b>
   140001c3b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001c40:	4c 39 eb             	cmp    %r13,%rbx
   140001c43:	0f 83 06 fd ff ff    	jae    14000194f <_pei386_runtime_relocator+0x1f>
   140001c49:	4c 8b 35 40 27 00 00 	mov    0x2740(%rip),%r14        # 140004390 <.refptr.__image_base__>
   140001c50:	8b 73 04             	mov    0x4(%rbx),%esi
   140001c53:	48 83 c3 08          	add    $0x8,%rbx
   140001c57:	44 8b 63 f8          	mov    -0x8(%rbx),%r12d
   140001c5b:	4c 01 f6             	add    %r14,%rsi
   140001c5e:	44 03 26             	add    (%rsi),%r12d
   140001c61:	48 89 f1             	mov    %rsi,%rcx
   140001c64:	e8 57 fb ff ff       	call   1400017c0 <mark_section_writable>
   140001c69:	4c 39 eb             	cmp    %r13,%rbx
   140001c6c:	44 89 26             	mov    %r12d,(%rsi)
   140001c6f:	72 df                	jb     140001c50 <_pei386_runtime_relocator+0x320>
   140001c71:	e9 7a fe ff ff       	jmp    140001af0 <_pei386_runtime_relocator+0x1c0>
   140001c76:	48 8d 0d fb 25 00 00 	lea    0x25fb(%rip),%rcx        # 140004278 <.rdata+0xd8>
   140001c7d:	e8 ce fa ff ff       	call   140001750 <__report_error>
   140001c82:	48 8d 0d b7 25 00 00 	lea    0x25b7(%rip),%rcx        # 140004240 <.rdata+0xa0>
   140001c89:	e8 c2 fa ff ff       	call   140001750 <__report_error>
   140001c8e:	90                   	nop
   140001c8f:	90                   	nop

0000000140001c90 <__mingw_raise_matherr>:
   140001c90:	48 83 ec 58          	sub    $0x58,%rsp
   140001c94:	48 8b 05 05 54 00 00 	mov    0x5405(%rip),%rax        # 1400070a0 <stUserMathErr>
   140001c9b:	48 85 c0             	test   %rax,%rax
   140001c9e:	66 0f 14 d3          	unpcklpd %xmm3,%xmm2
   140001ca2:	74 25                	je     140001cc9 <__mingw_raise_matherr+0x39>
   140001ca4:	f2 0f 10 84 24 80 00 	movsd  0x80(%rsp),%xmm0
   140001cab:	00 00 
   140001cad:	89 4c 24 20          	mov    %ecx,0x20(%rsp)
   140001cb1:	48 8d 4c 24 20       	lea    0x20(%rsp),%rcx
   140001cb6:	48 89 54 24 28       	mov    %rdx,0x28(%rsp)
   140001cbb:	0f 29 54 24 30       	movaps %xmm2,0x30(%rsp)
   140001cc0:	f2 0f 11 44 24 40    	movsd  %xmm0,0x40(%rsp)
   140001cc6:	ff d0                	call   *%rax
   140001cc8:	90                   	nop
   140001cc9:	48 83 c4 58          	add    $0x58,%rsp
   140001ccd:	c3                   	ret
   140001cce:	66 90                	xchg   %ax,%ax

0000000140001cd0 <__mingw_setusermatherr>:
   140001cd0:	48 89 0d c9 53 00 00 	mov    %rcx,0x53c9(%rip)        # 1400070a0 <stUserMathErr>
   140001cd7:	e9 d4 08 00 00       	jmp    1400025b0 <__setusermatherr>
   140001cdc:	90                   	nop
   140001cdd:	90                   	nop
   140001cde:	90                   	nop
   140001cdf:	90                   	nop

0000000140001ce0 <_gnu_exception_handler>:
   140001ce0:	53                   	push   %rbx
   140001ce1:	48 83 ec 20          	sub    $0x20,%rsp
   140001ce5:	48 8b 11             	mov    (%rcx),%rdx
   140001ce8:	8b 02                	mov    (%rdx),%eax
   140001cea:	48 89 cb             	mov    %rcx,%rbx
   140001ced:	89 c1                	mov    %eax,%ecx
   140001cef:	81 e1 ff ff ff 20    	and    $0x20ffffff,%ecx
   140001cf5:	81 f9 43 43 47 20    	cmp    $0x20474343,%ecx
   140001cfb:	0f 84 9f 00 00 00    	je     140001da0 <_gnu_exception_handler+0xc0>
   140001d01:	3d 96 00 00 c0       	cmp    $0xc0000096,%eax
   140001d06:	77 77                	ja     140001d7f <_gnu_exception_handler+0x9f>
   140001d08:	3d 8b 00 00 c0       	cmp    $0xc000008b,%eax
   140001d0d:	76 21                	jbe    140001d30 <_gnu_exception_handler+0x50>
   140001d0f:	05 73 ff ff 3f       	add    $0x3fffff73,%eax
   140001d14:	83 f8 09             	cmp    $0x9,%eax
   140001d17:	77 54                	ja     140001d6d <_gnu_exception_handler+0x8d>
   140001d19:	48 8d 15 e0 25 00 00 	lea    0x25e0(%rip),%rdx        # 140004300 <.rdata>
   140001d20:	48 63 04 82          	movslq (%rdx,%rax,4),%rax
   140001d24:	48 01 d0             	add    %rdx,%rax
   140001d27:	ff e0                	jmp    *%rax
   140001d29:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140001d30:	3d 05 00 00 c0       	cmp    $0xc0000005,%eax
   140001d35:	0f 84 d5 00 00 00    	je     140001e10 <_gnu_exception_handler+0x130>
   140001d3b:	76 3b                	jbe    140001d78 <_gnu_exception_handler+0x98>
   140001d3d:	3d 08 00 00 c0       	cmp    $0xc0000008,%eax
   140001d42:	74 29                	je     140001d6d <_gnu_exception_handler+0x8d>
   140001d44:	3d 1d 00 00 c0       	cmp    $0xc000001d,%eax
   140001d49:	75 34                	jne    140001d7f <_gnu_exception_handler+0x9f>
   140001d4b:	31 d2                	xor    %edx,%edx
   140001d4d:	b9 04 00 00 00       	mov    $0x4,%ecx
   140001d52:	e8 c1 08 00 00       	call   140002618 <signal>
   140001d57:	48 83 f8 01          	cmp    $0x1,%rax
   140001d5b:	0f 84 d6 00 00 00    	je     140001e37 <_gnu_exception_handler+0x157>
   140001d61:	48 85 c0             	test   %rax,%rax
   140001d64:	74 19                	je     140001d7f <_gnu_exception_handler+0x9f>
   140001d66:	b9 04 00 00 00       	mov    $0x4,%ecx
   140001d6b:	ff d0                	call   *%rax
   140001d6d:	b8 ff ff ff ff       	mov    $0xffffffff,%eax
   140001d72:	48 83 c4 20          	add    $0x20,%rsp
   140001d76:	5b                   	pop    %rbx
   140001d77:	c3                   	ret
   140001d78:	3d 02 00 00 80       	cmp    $0x80000002,%eax
   140001d7d:	74 ee                	je     140001d6d <_gnu_exception_handler+0x8d>
   140001d7f:	48 8b 05 3a 53 00 00 	mov    0x533a(%rip),%rax        # 1400070c0 <__mingw_oldexcpt_handler>
   140001d86:	48 85 c0             	test   %rax,%rax
   140001d89:	74 25                	je     140001db0 <_gnu_exception_handler+0xd0>
   140001d8b:	48 89 d9             	mov    %rbx,%rcx
   140001d8e:	48 83 c4 20          	add    $0x20,%rsp
   140001d92:	5b                   	pop    %rbx
   140001d93:	48 ff e0             	rex.W jmp *%rax
   140001d96:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   140001d9d:	00 00 00 
   140001da0:	f6 42 04 01          	testb  $0x1,0x4(%rdx)
   140001da4:	0f 85 57 ff ff ff    	jne    140001d01 <_gnu_exception_handler+0x21>
   140001daa:	eb c1                	jmp    140001d6d <_gnu_exception_handler+0x8d>
   140001dac:	0f 1f 40 00          	nopl   0x0(%rax)
   140001db0:	31 c0                	xor    %eax,%eax
   140001db2:	48 83 c4 20          	add    $0x20,%rsp
   140001db6:	5b                   	pop    %rbx
   140001db7:	c3                   	ret
   140001db8:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   140001dbf:	00 
   140001dc0:	31 d2                	xor    %edx,%edx
   140001dc2:	b9 08 00 00 00       	mov    $0x8,%ecx
   140001dc7:	e8 4c 08 00 00       	call   140002618 <signal>
   140001dcc:	48 83 f8 01          	cmp    $0x1,%rax
   140001dd0:	0f 84 89 00 00 00    	je     140001e5f <_gnu_exception_handler+0x17f>
   140001dd6:	48 85 c0             	test   %rax,%rax
   140001dd9:	74 a4                	je     140001d7f <_gnu_exception_handler+0x9f>
   140001ddb:	b9 08 00 00 00       	mov    $0x8,%ecx
   140001de0:	ff d0                	call   *%rax
   140001de2:	eb 89                	jmp    140001d6d <_gnu_exception_handler+0x8d>
   140001de4:	0f 1f 40 00          	nopl   0x0(%rax)
   140001de8:	31 d2                	xor    %edx,%edx
   140001dea:	b9 08 00 00 00       	mov    $0x8,%ecx
   140001def:	e8 24 08 00 00       	call   140002618 <signal>
   140001df4:	48 83 f8 01          	cmp    $0x1,%rax
   140001df8:	75 dc                	jne    140001dd6 <_gnu_exception_handler+0xf6>
   140001dfa:	ba 01 00 00 00       	mov    $0x1,%edx
   140001dff:	b9 08 00 00 00       	mov    $0x8,%ecx
   140001e04:	e8 0f 08 00 00       	call   140002618 <signal>
   140001e09:	e9 5f ff ff ff       	jmp    140001d6d <_gnu_exception_handler+0x8d>
   140001e0e:	66 90                	xchg   %ax,%ax
   140001e10:	31 d2                	xor    %edx,%edx
   140001e12:	b9 0b 00 00 00       	mov    $0xb,%ecx
   140001e17:	e8 fc 07 00 00       	call   140002618 <signal>
   140001e1c:	48 83 f8 01          	cmp    $0x1,%rax
   140001e20:	74 29                	je     140001e4b <_gnu_exception_handler+0x16b>
   140001e22:	48 85 c0             	test   %rax,%rax
   140001e25:	0f 84 54 ff ff ff    	je     140001d7f <_gnu_exception_handler+0x9f>
   140001e2b:	b9 0b 00 00 00       	mov    $0xb,%ecx
   140001e30:	ff d0                	call   *%rax
   140001e32:	e9 36 ff ff ff       	jmp    140001d6d <_gnu_exception_handler+0x8d>
   140001e37:	ba 01 00 00 00       	mov    $0x1,%edx
   140001e3c:	b9 04 00 00 00       	mov    $0x4,%ecx
   140001e41:	e8 d2 07 00 00       	call   140002618 <signal>
   140001e46:	e9 22 ff ff ff       	jmp    140001d6d <_gnu_exception_handler+0x8d>
   140001e4b:	ba 01 00 00 00       	mov    $0x1,%edx
   140001e50:	b9 0b 00 00 00       	mov    $0xb,%ecx
   140001e55:	e8 be 07 00 00       	call   140002618 <signal>
   140001e5a:	e9 0e ff ff ff       	jmp    140001d6d <_gnu_exception_handler+0x8d>
   140001e5f:	ba 01 00 00 00       	mov    $0x1,%edx
   140001e64:	b9 08 00 00 00       	mov    $0x8,%ecx
   140001e69:	e8 aa 07 00 00       	call   140002618 <signal>
   140001e6e:	e8 cd f8 ff ff       	call   140001740 <_fpreset>
   140001e73:	e9 f5 fe ff ff       	jmp    140001d6d <_gnu_exception_handler+0x8d>
   140001e78:	90                   	nop
   140001e79:	90                   	nop
   140001e7a:	90                   	nop
   140001e7b:	90                   	nop
   140001e7c:	90                   	nop
   140001e7d:	90                   	nop
   140001e7e:	90                   	nop
   140001e7f:	90                   	nop

0000000140001e80 <__mingwthr_run_key_dtors.part.0>:
   140001e80:	41 54                	push   %r12
   140001e82:	55                   	push   %rbp
   140001e83:	57                   	push   %rdi
   140001e84:	56                   	push   %rsi
   140001e85:	53                   	push   %rbx
   140001e86:	48 83 ec 20          	sub    $0x20,%rsp
   140001e8a:	4c 8d 25 6f 52 00 00 	lea    0x526f(%rip),%r12        # 140007100 <__mingwthr_cs>
   140001e91:	4c 89 e1             	mov    %r12,%rcx
   140001e94:	ff 15 ca 62 00 00    	call   *0x62ca(%rip)        # 140008164 <__imp_EnterCriticalSection>
   140001e9a:	48 8b 1d 3f 52 00 00 	mov    0x523f(%rip),%rbx        # 1400070e0 <key_dtor_list>
   140001ea1:	48 85 db             	test   %rbx,%rbx
   140001ea4:	74 36                	je     140001edc <__mingwthr_run_key_dtors.part.0+0x5c>
   140001ea6:	48 8b 2d e7 62 00 00 	mov    0x62e7(%rip),%rbp        # 140008194 <__imp_TlsGetValue>
   140001ead:	48 8b 3d b8 62 00 00 	mov    0x62b8(%rip),%rdi        # 14000816c <__imp_GetLastError>
   140001eb4:	0f 1f 40 00          	nopl   0x0(%rax)
   140001eb8:	8b 0b                	mov    (%rbx),%ecx
   140001eba:	ff d5                	call   *%rbp
   140001ebc:	48 89 c6             	mov    %rax,%rsi
   140001ebf:	ff d7                	call   *%rdi
   140001ec1:	85 c0                	test   %eax,%eax
   140001ec3:	75 0e                	jne    140001ed3 <__mingwthr_run_key_dtors.part.0+0x53>
   140001ec5:	48 85 f6             	test   %rsi,%rsi
   140001ec8:	74 09                	je     140001ed3 <__mingwthr_run_key_dtors.part.0+0x53>
   140001eca:	48 8b 43 08          	mov    0x8(%rbx),%rax
   140001ece:	48 89 f1             	mov    %rsi,%rcx
   140001ed1:	ff d0                	call   *%rax
   140001ed3:	48 8b 5b 10          	mov    0x10(%rbx),%rbx
   140001ed7:	48 85 db             	test   %rbx,%rbx
   140001eda:	75 dc                	jne    140001eb8 <__mingwthr_run_key_dtors.part.0+0x38>
   140001edc:	4c 89 e1             	mov    %r12,%rcx
   140001edf:	48 83 c4 20          	add    $0x20,%rsp
   140001ee3:	5b                   	pop    %rbx
   140001ee4:	5e                   	pop    %rsi
   140001ee5:	5f                   	pop    %rdi
   140001ee6:	5d                   	pop    %rbp
   140001ee7:	41 5c                	pop    %r12
   140001ee9:	48 ff 25 8c 62 00 00 	rex.W jmp *0x628c(%rip)        # 14000817c <__imp_LeaveCriticalSection>

0000000140001ef0 <___w64_mingwthr_add_key_dtor>:
   140001ef0:	57                   	push   %rdi
   140001ef1:	56                   	push   %rsi
   140001ef2:	53                   	push   %rbx
   140001ef3:	48 83 ec 20          	sub    $0x20,%rsp
   140001ef7:	8b 05 eb 51 00 00    	mov    0x51eb(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   140001efd:	85 c0                	test   %eax,%eax
   140001eff:	89 cf                	mov    %ecx,%edi
   140001f01:	48 89 d6             	mov    %rdx,%rsi
   140001f04:	75 0a                	jne    140001f10 <___w64_mingwthr_add_key_dtor+0x20>
   140001f06:	31 c0                	xor    %eax,%eax
   140001f08:	48 83 c4 20          	add    $0x20,%rsp
   140001f0c:	5b                   	pop    %rbx
   140001f0d:	5e                   	pop    %rsi
   140001f0e:	5f                   	pop    %rdi
   140001f0f:	c3                   	ret
   140001f10:	ba 18 00 00 00       	mov    $0x18,%edx
   140001f15:	b9 01 00 00 00       	mov    $0x1,%ecx
   140001f1a:	e8 c1 06 00 00       	call   1400025e0 <calloc>
   140001f1f:	48 85 c0             	test   %rax,%rax
   140001f22:	48 89 c3             	mov    %rax,%rbx
   140001f25:	74 33                	je     140001f5a <___w64_mingwthr_add_key_dtor+0x6a>
   140001f27:	48 89 70 08          	mov    %rsi,0x8(%rax)
   140001f2b:	48 8d 35 ce 51 00 00 	lea    0x51ce(%rip),%rsi        # 140007100 <__mingwthr_cs>
   140001f32:	89 38                	mov    %edi,(%rax)
   140001f34:	48 89 f1             	mov    %rsi,%rcx
   140001f37:	ff 15 27 62 00 00    	call   *0x6227(%rip)        # 140008164 <__imp_EnterCriticalSection>
   140001f3d:	48 8b 05 9c 51 00 00 	mov    0x519c(%rip),%rax        # 1400070e0 <key_dtor_list>
   140001f44:	48 89 f1             	mov    %rsi,%rcx
   140001f47:	48 89 1d 92 51 00 00 	mov    %rbx,0x5192(%rip)        # 1400070e0 <key_dtor_list>
   140001f4e:	48 89 43 10          	mov    %rax,0x10(%rbx)
   140001f52:	ff 15 24 62 00 00    	call   *0x6224(%rip)        # 14000817c <__imp_LeaveCriticalSection>
   140001f58:	eb ac                	jmp    140001f06 <___w64_mingwthr_add_key_dtor+0x16>
   140001f5a:	83 c8 ff             	or     $0xffffffff,%eax
   140001f5d:	eb a9                	jmp    140001f08 <___w64_mingwthr_add_key_dtor+0x18>
   140001f5f:	90                   	nop

0000000140001f60 <___w64_mingwthr_remove_key_dtor>:
   140001f60:	56                   	push   %rsi
   140001f61:	53                   	push   %rbx
   140001f62:	48 83 ec 28          	sub    $0x28,%rsp
   140001f66:	8b 05 7c 51 00 00    	mov    0x517c(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   140001f6c:	85 c0                	test   %eax,%eax
   140001f6e:	89 cb                	mov    %ecx,%ebx
   140001f70:	75 0e                	jne    140001f80 <___w64_mingwthr_remove_key_dtor+0x20>
   140001f72:	31 c0                	xor    %eax,%eax
   140001f74:	48 83 c4 28          	add    $0x28,%rsp
   140001f78:	5b                   	pop    %rbx
   140001f79:	5e                   	pop    %rsi
   140001f7a:	c3                   	ret
   140001f7b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001f80:	48 8d 35 79 51 00 00 	lea    0x5179(%rip),%rsi        # 140007100 <__mingwthr_cs>
   140001f87:	48 89 f1             	mov    %rsi,%rcx
   140001f8a:	ff 15 d4 61 00 00    	call   *0x61d4(%rip)        # 140008164 <__imp_EnterCriticalSection>
   140001f90:	48 8b 0d 49 51 00 00 	mov    0x5149(%rip),%rcx        # 1400070e0 <key_dtor_list>
   140001f97:	48 85 c9             	test   %rcx,%rcx
   140001f9a:	74 27                	je     140001fc3 <___w64_mingwthr_remove_key_dtor+0x63>
   140001f9c:	31 d2                	xor    %edx,%edx
   140001f9e:	eb 0b                	jmp    140001fab <___w64_mingwthr_remove_key_dtor+0x4b>
   140001fa0:	48 85 c0             	test   %rax,%rax
   140001fa3:	48 89 ca             	mov    %rcx,%rdx
   140001fa6:	74 1b                	je     140001fc3 <___w64_mingwthr_remove_key_dtor+0x63>
   140001fa8:	48 89 c1             	mov    %rax,%rcx
   140001fab:	8b 01                	mov    (%rcx),%eax
   140001fad:	39 d8                	cmp    %ebx,%eax
   140001faf:	48 8b 41 10          	mov    0x10(%rcx),%rax
   140001fb3:	75 eb                	jne    140001fa0 <___w64_mingwthr_remove_key_dtor+0x40>
   140001fb5:	48 85 d2             	test   %rdx,%rdx
   140001fb8:	74 1e                	je     140001fd8 <___w64_mingwthr_remove_key_dtor+0x78>
   140001fba:	48 89 42 10          	mov    %rax,0x10(%rdx)
   140001fbe:	e8 35 06 00 00       	call   1400025f8 <free>
   140001fc3:	48 89 f1             	mov    %rsi,%rcx
   140001fc6:	ff 15 b0 61 00 00    	call   *0x61b0(%rip)        # 14000817c <__imp_LeaveCriticalSection>
   140001fcc:	31 c0                	xor    %eax,%eax
   140001fce:	48 83 c4 28          	add    $0x28,%rsp
   140001fd2:	5b                   	pop    %rbx
   140001fd3:	5e                   	pop    %rsi
   140001fd4:	c3                   	ret
   140001fd5:	0f 1f 00             	nopl   (%rax)
   140001fd8:	48 89 05 01 51 00 00 	mov    %rax,0x5101(%rip)        # 1400070e0 <key_dtor_list>
   140001fdf:	eb dd                	jmp    140001fbe <___w64_mingwthr_remove_key_dtor+0x5e>
   140001fe1:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   140001fe8:	00 00 00 00 
   140001fec:	0f 1f 40 00          	nopl   0x0(%rax)

0000000140001ff0 <__mingw_TLScallback>:
   140001ff0:	53                   	push   %rbx
   140001ff1:	48 83 ec 20          	sub    $0x20,%rsp
   140001ff5:	83 fa 02             	cmp    $0x2,%edx
   140001ff8:	0f 84 b2 00 00 00    	je     1400020b0 <__mingw_TLScallback+0xc0>
   140001ffe:	77 30                	ja     140002030 <__mingw_TLScallback+0x40>
   140002000:	85 d2                	test   %edx,%edx
   140002002:	74 4c                	je     140002050 <__mingw_TLScallback+0x60>
   140002004:	8b 05 de 50 00 00    	mov    0x50de(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   14000200a:	85 c0                	test   %eax,%eax
   14000200c:	0f 84 be 00 00 00    	je     1400020d0 <__mingw_TLScallback+0xe0>
   140002012:	c7 05 cc 50 00 00 01 	movl   $0x1,0x50cc(%rip)        # 1400070e8 <__mingwthr_cs_init>
   140002019:	00 00 00 
   14000201c:	b8 01 00 00 00       	mov    $0x1,%eax
   140002021:	48 83 c4 20          	add    $0x20,%rsp
   140002025:	5b                   	pop    %rbx
   140002026:	c3                   	ret
   140002027:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   14000202e:	00 00 
   140002030:	83 fa 03             	cmp    $0x3,%edx
   140002033:	75 e7                	jne    14000201c <__mingw_TLScallback+0x2c>
   140002035:	8b 05 ad 50 00 00    	mov    0x50ad(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   14000203b:	85 c0                	test   %eax,%eax
   14000203d:	74 dd                	je     14000201c <__mingw_TLScallback+0x2c>
   14000203f:	e8 3c fe ff ff       	call   140001e80 <__mingwthr_run_key_dtors.part.0>
   140002044:	eb d6                	jmp    14000201c <__mingw_TLScallback+0x2c>
   140002046:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000204d:	00 00 00 
   140002050:	8b 05 92 50 00 00    	mov    0x5092(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   140002056:	85 c0                	test   %eax,%eax
   140002058:	75 66                	jne    1400020c0 <__mingw_TLScallback+0xd0>
   14000205a:	8b 05 88 50 00 00    	mov    0x5088(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   140002060:	83 f8 01             	cmp    $0x1,%eax
   140002063:	75 b7                	jne    14000201c <__mingw_TLScallback+0x2c>
   140002065:	48 8b 1d 74 50 00 00 	mov    0x5074(%rip),%rbx        # 1400070e0 <key_dtor_list>
   14000206c:	48 85 db             	test   %rbx,%rbx
   14000206f:	74 18                	je     140002089 <__mingw_TLScallback+0x99>
   140002071:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140002078:	48 89 d9             	mov    %rbx,%rcx
   14000207b:	48 8b 5b 10          	mov    0x10(%rbx),%rbx
   14000207f:	e8 74 05 00 00       	call   1400025f8 <free>
   140002084:	48 85 db             	test   %rbx,%rbx
   140002087:	75 ef                	jne    140002078 <__mingw_TLScallback+0x88>
   140002089:	48 8d 0d 70 50 00 00 	lea    0x5070(%rip),%rcx        # 140007100 <__mingwthr_cs>
   140002090:	48 c7 05 45 50 00 00 	movq   $0x0,0x5045(%rip)        # 1400070e0 <key_dtor_list>
   140002097:	00 00 00 00 
   14000209b:	c7 05 43 50 00 00 00 	movl   $0x0,0x5043(%rip)        # 1400070e8 <__mingwthr_cs_init>
   1400020a2:	00 00 00 
   1400020a5:	ff 15 b1 60 00 00    	call   *0x60b1(%rip)        # 14000815c <__IAT_start__>
   1400020ab:	e9 6c ff ff ff       	jmp    14000201c <__mingw_TLScallback+0x2c>
   1400020b0:	e8 8b f6 ff ff       	call   140001740 <_fpreset>
   1400020b5:	b8 01 00 00 00       	mov    $0x1,%eax
   1400020ba:	48 83 c4 20          	add    $0x20,%rsp
   1400020be:	5b                   	pop    %rbx
   1400020bf:	c3                   	ret
   1400020c0:	e8 bb fd ff ff       	call   140001e80 <__mingwthr_run_key_dtors.part.0>
   1400020c5:	eb 93                	jmp    14000205a <__mingw_TLScallback+0x6a>
   1400020c7:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   1400020ce:	00 00 
   1400020d0:	48 8d 0d 29 50 00 00 	lea    0x5029(%rip),%rcx        # 140007100 <__mingwthr_cs>
   1400020d7:	ff 15 97 60 00 00    	call   *0x6097(%rip)        # 140008174 <__imp_InitializeCriticalSection>
   1400020dd:	e9 30 ff ff ff       	jmp    140002012 <__mingw_TLScallback+0x22>
   1400020e2:	90                   	nop
   1400020e3:	90                   	nop
   1400020e4:	90                   	nop
   1400020e5:	90                   	nop
   1400020e6:	90                   	nop
   1400020e7:	90                   	nop
   1400020e8:	90                   	nop
   1400020e9:	90                   	nop
   1400020ea:	90                   	nop
   1400020eb:	90                   	nop
   1400020ec:	90                   	nop
   1400020ed:	90                   	nop
   1400020ee:	90                   	nop
   1400020ef:	90                   	nop

00000001400020f0 <_ValidateImageBase>:
   1400020f0:	31 c0                	xor    %eax,%eax
   1400020f2:	66 81 39 4d 5a       	cmpw   $0x5a4d,(%rcx)
   1400020f7:	75 0f                	jne    140002108 <_ValidateImageBase+0x18>
   1400020f9:	48 63 51 3c          	movslq 0x3c(%rcx),%rdx
   1400020fd:	48 01 d1             	add    %rdx,%rcx
   140002100:	81 39 50 45 00 00    	cmpl   $0x4550,(%rcx)
   140002106:	74 08                	je     140002110 <_ValidateImageBase+0x20>
   140002108:	c3                   	ret
   140002109:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140002110:	31 c0                	xor    %eax,%eax
   140002112:	66 81 79 18 0b 02    	cmpw   $0x20b,0x18(%rcx)
   140002118:	0f 94 c0             	sete   %al
   14000211b:	c3                   	ret
   14000211c:	0f 1f 40 00          	nopl   0x0(%rax)

0000000140002120 <_FindPESection>:
   140002120:	48 63 41 3c          	movslq 0x3c(%rcx),%rax
   140002124:	48 01 c1             	add    %rax,%rcx
   140002127:	44 0f b7 41 06       	movzwl 0x6(%rcx),%r8d
   14000212c:	0f b7 41 14          	movzwl 0x14(%rcx),%eax
   140002130:	66 45 85 c0          	test   %r8w,%r8w
   140002134:	48 8d 44 01 18       	lea    0x18(%rcx,%rax,1),%rax
   140002139:	74 32                	je     14000216d <_FindPESection+0x4d>
   14000213b:	41 8d 48 ff          	lea    -0x1(%r8),%ecx
   14000213f:	48 8d 0c 89          	lea    (%rcx,%rcx,4),%rcx
   140002143:	4c 8d 4c c8 28       	lea    0x28(%rax,%rcx,8),%r9
   140002148:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   14000214f:	00 
   140002150:	44 8b 40 0c          	mov    0xc(%rax),%r8d
   140002154:	4c 39 c2             	cmp    %r8,%rdx
   140002157:	4c 89 c1             	mov    %r8,%rcx
   14000215a:	72 08                	jb     140002164 <_FindPESection+0x44>
   14000215c:	03 48 08             	add    0x8(%rax),%ecx
   14000215f:	48 39 ca             	cmp    %rcx,%rdx
   140002162:	72 0b                	jb     14000216f <_FindPESection+0x4f>
   140002164:	48 83 c0 28          	add    $0x28,%rax
   140002168:	4c 39 c8             	cmp    %r9,%rax
   14000216b:	75 e3                	jne    140002150 <_FindPESection+0x30>
   14000216d:	31 c0                	xor    %eax,%eax
   14000216f:	c3                   	ret

0000000140002170 <_FindPESectionByName>:
   140002170:	57                   	push   %rdi
   140002171:	56                   	push   %rsi
   140002172:	53                   	push   %rbx
   140002173:	48 83 ec 20          	sub    $0x20,%rsp
   140002177:	48 89 ce             	mov    %rcx,%rsi
   14000217a:	e8 a1 04 00 00       	call   140002620 <strlen>
   14000217f:	48 83 f8 08          	cmp    $0x8,%rax
   140002183:	77 7b                	ja     140002200 <_FindPESectionByName+0x90>
   140002185:	48 8b 15 04 22 00 00 	mov    0x2204(%rip),%rdx        # 140004390 <.refptr.__image_base__>
   14000218c:	31 db                	xor    %ebx,%ebx
   14000218e:	66 81 3a 4d 5a       	cmpw   $0x5a4d,(%rdx)
   140002193:	75 59                	jne    1400021ee <_FindPESectionByName+0x7e>
   140002195:	48 63 42 3c          	movslq 0x3c(%rdx),%rax
   140002199:	48 01 d0             	add    %rdx,%rax
   14000219c:	81 38 50 45 00 00    	cmpl   $0x4550,(%rax)
   1400021a2:	75 4a                	jne    1400021ee <_FindPESectionByName+0x7e>
   1400021a4:	66 81 78 18 0b 02    	cmpw   $0x20b,0x18(%rax)
   1400021aa:	75 42                	jne    1400021ee <_FindPESectionByName+0x7e>
   1400021ac:	0f b7 50 14          	movzwl 0x14(%rax),%edx
   1400021b0:	48 8d 5c 10 18       	lea    0x18(%rax,%rdx,1),%rbx
   1400021b5:	0f b7 50 06          	movzwl 0x6(%rax),%edx
   1400021b9:	66 85 d2             	test   %dx,%dx
   1400021bc:	74 42                	je     140002200 <_FindPESectionByName+0x90>
   1400021be:	8d 42 ff             	lea    -0x1(%rdx),%eax
   1400021c1:	48 8d 04 80          	lea    (%rax,%rax,4),%rax
   1400021c5:	48 8d 7c c3 28       	lea    0x28(%rbx,%rax,8),%rdi
   1400021ca:	eb 0d                	jmp    1400021d9 <_FindPESectionByName+0x69>
   1400021cc:	0f 1f 40 00          	nopl   0x0(%rax)
   1400021d0:	48 83 c3 28          	add    $0x28,%rbx
   1400021d4:	48 39 fb             	cmp    %rdi,%rbx
   1400021d7:	74 27                	je     140002200 <_FindPESectionByName+0x90>
   1400021d9:	41 b8 08 00 00 00    	mov    $0x8,%r8d
   1400021df:	48 89 f2             	mov    %rsi,%rdx
   1400021e2:	48 89 d9             	mov    %rbx,%rcx
   1400021e5:	e8 3e 04 00 00       	call   140002628 <strncmp>
   1400021ea:	85 c0                	test   %eax,%eax
   1400021ec:	75 e2                	jne    1400021d0 <_FindPESectionByName+0x60>
   1400021ee:	48 89 d8             	mov    %rbx,%rax
   1400021f1:	48 83 c4 20          	add    $0x20,%rsp
   1400021f5:	5b                   	pop    %rbx
   1400021f6:	5e                   	pop    %rsi
   1400021f7:	5f                   	pop    %rdi
   1400021f8:	c3                   	ret
   1400021f9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140002200:	31 db                	xor    %ebx,%ebx
   140002202:	48 89 d8             	mov    %rbx,%rax
   140002205:	48 83 c4 20          	add    $0x20,%rsp
   140002209:	5b                   	pop    %rbx
   14000220a:	5e                   	pop    %rsi
   14000220b:	5f                   	pop    %rdi
   14000220c:	c3                   	ret
   14000220d:	0f 1f 00             	nopl   (%rax)

0000000140002210 <__mingw_GetSectionForAddress>:
   140002210:	48 8b 15 79 21 00 00 	mov    0x2179(%rip),%rdx        # 140004390 <.refptr.__image_base__>
   140002217:	31 c0                	xor    %eax,%eax
   140002219:	66 81 3a 4d 5a       	cmpw   $0x5a4d,(%rdx)
   14000221e:	75 10                	jne    140002230 <__mingw_GetSectionForAddress+0x20>
   140002220:	4c 63 42 3c          	movslq 0x3c(%rdx),%r8
   140002224:	49 01 d0             	add    %rdx,%r8
   140002227:	41 81 38 50 45 00 00 	cmpl   $0x4550,(%r8)
   14000222e:	74 08                	je     140002238 <__mingw_GetSectionForAddress+0x28>
   140002230:	c3                   	ret
   140002231:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140002238:	66 41 81 78 18 0b 02 	cmpw   $0x20b,0x18(%r8)
   14000223f:	75 ef                	jne    140002230 <__mingw_GetSectionForAddress+0x20>
   140002241:	41 0f b7 40 14       	movzwl 0x14(%r8),%eax
   140002246:	48 29 d1             	sub    %rdx,%rcx
   140002249:	49 8d 44 00 18       	lea    0x18(%r8,%rax,1),%rax
   14000224e:	45 0f b7 40 06       	movzwl 0x6(%r8),%r8d
   140002253:	66 45 85 c0          	test   %r8w,%r8w
   140002257:	74 34                	je     14000228d <__mingw_GetSectionForAddress+0x7d>
   140002259:	41 8d 50 ff          	lea    -0x1(%r8),%edx
   14000225d:	48 8d 14 92          	lea    (%rdx,%rdx,4),%rdx
   140002261:	4c 8d 4c d0 28       	lea    0x28(%rax,%rdx,8),%r9
   140002266:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000226d:	00 00 00 
   140002270:	44 8b 40 0c          	mov    0xc(%rax),%r8d
   140002274:	4c 39 c1             	cmp    %r8,%rcx
   140002277:	4c 89 c2             	mov    %r8,%rdx
   14000227a:	72 08                	jb     140002284 <__mingw_GetSectionForAddress+0x74>
   14000227c:	03 50 08             	add    0x8(%rax),%edx
   14000227f:	48 39 d1             	cmp    %rdx,%rcx
   140002282:	72 ac                	jb     140002230 <__mingw_GetSectionForAddress+0x20>
   140002284:	48 83 c0 28          	add    $0x28,%rax
   140002288:	4c 39 c8             	cmp    %r9,%rax
   14000228b:	75 e3                	jne    140002270 <__mingw_GetSectionForAddress+0x60>
   14000228d:	31 c0                	xor    %eax,%eax
   14000228f:	c3                   	ret

0000000140002290 <__mingw_GetSectionCount>:
   140002290:	48 8b 05 f9 20 00 00 	mov    0x20f9(%rip),%rax        # 140004390 <.refptr.__image_base__>
   140002297:	31 c9                	xor    %ecx,%ecx
   140002299:	66 81 38 4d 5a       	cmpw   $0x5a4d,(%rax)
   14000229e:	75 0f                	jne    1400022af <__mingw_GetSectionCount+0x1f>
   1400022a0:	48 63 50 3c          	movslq 0x3c(%rax),%rdx
   1400022a4:	48 01 d0             	add    %rdx,%rax
   1400022a7:	81 38 50 45 00 00    	cmpl   $0x4550,(%rax)
   1400022ad:	74 09                	je     1400022b8 <__mingw_GetSectionCount+0x28>
   1400022af:	89 c8                	mov    %ecx,%eax
   1400022b1:	c3                   	ret
   1400022b2:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
   1400022b8:	66 81 78 18 0b 02    	cmpw   $0x20b,0x18(%rax)
   1400022be:	75 ef                	jne    1400022af <__mingw_GetSectionCount+0x1f>
   1400022c0:	0f b7 48 06          	movzwl 0x6(%rax),%ecx
   1400022c4:	89 c8                	mov    %ecx,%eax
   1400022c6:	c3                   	ret
   1400022c7:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   1400022ce:	00 00 

00000001400022d0 <_FindPESectionExec>:
   1400022d0:	4c 8b 05 b9 20 00 00 	mov    0x20b9(%rip),%r8        # 140004390 <.refptr.__image_base__>
   1400022d7:	31 c0                	xor    %eax,%eax
   1400022d9:	66 41 81 38 4d 5a    	cmpw   $0x5a4d,(%r8)
   1400022df:	75 0f                	jne    1400022f0 <_FindPESectionExec+0x20>
   1400022e1:	49 63 50 3c          	movslq 0x3c(%r8),%rdx
   1400022e5:	4c 01 c2             	add    %r8,%rdx
   1400022e8:	81 3a 50 45 00 00    	cmpl   $0x4550,(%rdx)
   1400022ee:	74 08                	je     1400022f8 <_FindPESectionExec+0x28>
   1400022f0:	c3                   	ret
   1400022f1:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400022f8:	66 81 7a 18 0b 02    	cmpw   $0x20b,0x18(%rdx)
   1400022fe:	75 f0                	jne    1400022f0 <_FindPESectionExec+0x20>
   140002300:	44 0f b7 42 06       	movzwl 0x6(%rdx),%r8d
   140002305:	0f b7 42 14          	movzwl 0x14(%rdx),%eax
   140002309:	66 45 85 c0          	test   %r8w,%r8w
   14000230d:	48 8d 44 02 18       	lea    0x18(%rdx,%rax,1),%rax
   140002312:	74 2c                	je     140002340 <_FindPESectionExec+0x70>
   140002314:	41 8d 50 ff          	lea    -0x1(%r8),%edx
   140002318:	48 8d 14 92          	lea    (%rdx,%rdx,4),%rdx
   14000231c:	48 8d 54 d0 28       	lea    0x28(%rax,%rdx,8),%rdx
   140002321:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140002328:	f6 40 27 20          	testb  $0x20,0x27(%rax)
   14000232c:	74 09                	je     140002337 <_FindPESectionExec+0x67>
   14000232e:	48 85 c9             	test   %rcx,%rcx
   140002331:	74 bd                	je     1400022f0 <_FindPESectionExec+0x20>
   140002333:	48 83 e9 01          	sub    $0x1,%rcx
   140002337:	48 83 c0 28          	add    $0x28,%rax
   14000233b:	48 39 d0             	cmp    %rdx,%rax
   14000233e:	75 e8                	jne    140002328 <_FindPESectionExec+0x58>
   140002340:	31 c0                	xor    %eax,%eax
   140002342:	c3                   	ret
   140002343:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   14000234a:	00 00 00 00 
   14000234e:	66 90                	xchg   %ax,%ax

0000000140002350 <_GetPEImageBase>:
   140002350:	48 8b 05 39 20 00 00 	mov    0x2039(%rip),%rax        # 140004390 <.refptr.__image_base__>
   140002357:	31 d2                	xor    %edx,%edx
   140002359:	66 81 38 4d 5a       	cmpw   $0x5a4d,(%rax)
   14000235e:	75 0f                	jne    14000236f <_GetPEImageBase+0x1f>
   140002360:	48 63 48 3c          	movslq 0x3c(%rax),%rcx
   140002364:	48 01 c1             	add    %rax,%rcx
   140002367:	81 39 50 45 00 00    	cmpl   $0x4550,(%rcx)
   14000236d:	74 09                	je     140002378 <_GetPEImageBase+0x28>
   14000236f:	48 89 d0             	mov    %rdx,%rax
   140002372:	c3                   	ret
   140002373:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140002378:	66 81 79 18 0b 02    	cmpw   $0x20b,0x18(%rcx)
   14000237e:	48 0f 44 d0          	cmove  %rax,%rdx
   140002382:	48 89 d0             	mov    %rdx,%rax
   140002385:	c3                   	ret
   140002386:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000238d:	00 00 00 

0000000140002390 <_IsNonwritableInCurrentImage>:
   140002390:	48 8b 15 f9 1f 00 00 	mov    0x1ff9(%rip),%rdx        # 140004390 <.refptr.__image_base__>
   140002397:	31 c0                	xor    %eax,%eax
   140002399:	66 81 3a 4d 5a       	cmpw   $0x5a4d,(%rdx)
   14000239e:	75 10                	jne    1400023b0 <_IsNonwritableInCurrentImage+0x20>
   1400023a0:	4c 63 42 3c          	movslq 0x3c(%rdx),%r8
   1400023a4:	49 01 d0             	add    %rdx,%r8
   1400023a7:	41 81 38 50 45 00 00 	cmpl   $0x4550,(%r8)
   1400023ae:	74 08                	je     1400023b8 <_IsNonwritableInCurrentImage+0x28>
   1400023b0:	c3                   	ret
   1400023b1:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400023b8:	66 41 81 78 18 0b 02 	cmpw   $0x20b,0x18(%r8)
   1400023bf:	75 ef                	jne    1400023b0 <_IsNonwritableInCurrentImage+0x20>
   1400023c1:	45 0f b7 48 06       	movzwl 0x6(%r8),%r9d
   1400023c6:	48 29 d1             	sub    %rdx,%rcx
   1400023c9:	41 0f b7 50 14       	movzwl 0x14(%r8),%edx
   1400023ce:	66 45 85 c9          	test   %r9w,%r9w
   1400023d2:	49 8d 54 10 18       	lea    0x18(%r8,%rdx,1),%rdx
   1400023d7:	74 d7                	je     1400023b0 <_IsNonwritableInCurrentImage+0x20>
   1400023d9:	41 8d 41 ff          	lea    -0x1(%r9),%eax
   1400023dd:	48 8d 04 80          	lea    (%rax,%rax,4),%rax
   1400023e1:	4c 8d 4c c2 28       	lea    0x28(%rdx,%rax,8),%r9
   1400023e6:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   1400023ed:	00 00 00 
   1400023f0:	44 8b 42 0c          	mov    0xc(%rdx),%r8d
   1400023f4:	4c 39 c1             	cmp    %r8,%rcx
   1400023f7:	4c 89 c0             	mov    %r8,%rax
   1400023fa:	72 08                	jb     140002404 <_IsNonwritableInCurrentImage+0x74>
   1400023fc:	03 42 08             	add    0x8(%rdx),%eax
   1400023ff:	48 39 c1             	cmp    %rax,%rcx
   140002402:	72 0c                	jb     140002410 <_IsNonwritableInCurrentImage+0x80>
   140002404:	48 83 c2 28          	add    $0x28,%rdx
   140002408:	49 39 d1             	cmp    %rdx,%r9
   14000240b:	75 e3                	jne    1400023f0 <_IsNonwritableInCurrentImage+0x60>
   14000240d:	31 c0                	xor    %eax,%eax
   14000240f:	c3                   	ret
   140002410:	8b 42 24             	mov    0x24(%rdx),%eax
   140002413:	f7 d0                	not    %eax
   140002415:	c1 e8 1f             	shr    $0x1f,%eax
   140002418:	c3                   	ret
   140002419:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000140002420 <__mingw_enum_import_library_names>:
   140002420:	4c 8b 1d 69 1f 00 00 	mov    0x1f69(%rip),%r11        # 140004390 <.refptr.__image_base__>
   140002427:	45 31 c9             	xor    %r9d,%r9d
   14000242a:	66 41 81 3b 4d 5a    	cmpw   $0x5a4d,(%r11)
   140002430:	75 10                	jne    140002442 <__mingw_enum_import_library_names+0x22>
   140002432:	4d 63 43 3c          	movslq 0x3c(%r11),%r8
   140002436:	4d 01 d8             	add    %r11,%r8
   140002439:	41 81 38 50 45 00 00 	cmpl   $0x4550,(%r8)
   140002440:	74 0e                	je     140002450 <__mingw_enum_import_library_names+0x30>
   140002442:	4c 89 c8             	mov    %r9,%rax
   140002445:	c3                   	ret
   140002446:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000244d:	00 00 00 
   140002450:	66 41 81 78 18 0b 02 	cmpw   $0x20b,0x18(%r8)
   140002457:	75 e9                	jne    140002442 <__mingw_enum_import_library_names+0x22>
   140002459:	41 8b 80 90 00 00 00 	mov    0x90(%r8),%eax
   140002460:	85 c0                	test   %eax,%eax
   140002462:	74 de                	je     140002442 <__mingw_enum_import_library_names+0x22>
   140002464:	45 0f b7 50 06       	movzwl 0x6(%r8),%r10d
   140002469:	41 0f b7 50 14       	movzwl 0x14(%r8),%edx
   14000246e:	66 45 85 d2          	test   %r10w,%r10w
   140002472:	49 8d 54 10 18       	lea    0x18(%r8,%rdx,1),%rdx
   140002477:	74 c9                	je     140002442 <__mingw_enum_import_library_names+0x22>
   140002479:	45 8d 42 ff          	lea    -0x1(%r10),%r8d
   14000247d:	4f 8d 04 80          	lea    (%r8,%r8,4),%r8
   140002481:	4e 8d 54 c2 28       	lea    0x28(%rdx,%r8,8),%r10
   140002486:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000248d:	00 00 00 
   140002490:	44 8b 4a 0c          	mov    0xc(%rdx),%r9d
   140002494:	4c 39 c8             	cmp    %r9,%rax
   140002497:	4d 89 c8             	mov    %r9,%r8
   14000249a:	72 09                	jb     1400024a5 <__mingw_enum_import_library_names+0x85>
   14000249c:	44 03 42 08          	add    0x8(%rdx),%r8d
   1400024a0:	4c 39 c0             	cmp    %r8,%rax
   1400024a3:	72 13                	jb     1400024b8 <__mingw_enum_import_library_names+0x98>
   1400024a5:	48 83 c2 28          	add    $0x28,%rdx
   1400024a9:	4c 39 d2             	cmp    %r10,%rdx
   1400024ac:	75 e2                	jne    140002490 <__mingw_enum_import_library_names+0x70>
   1400024ae:	45 31 c9             	xor    %r9d,%r9d
   1400024b1:	4c 89 c8             	mov    %r9,%rax
   1400024b4:	c3                   	ret
   1400024b5:	0f 1f 00             	nopl   (%rax)
   1400024b8:	4c 01 d8             	add    %r11,%rax
   1400024bb:	eb 0a                	jmp    1400024c7 <__mingw_enum_import_library_names+0xa7>
   1400024bd:	0f 1f 00             	nopl   (%rax)
   1400024c0:	83 e9 01             	sub    $0x1,%ecx
   1400024c3:	48 83 c0 14          	add    $0x14,%rax
   1400024c7:	44 8b 40 04          	mov    0x4(%rax),%r8d
   1400024cb:	45 85 c0             	test   %r8d,%r8d
   1400024ce:	75 07                	jne    1400024d7 <__mingw_enum_import_library_names+0xb7>
   1400024d0:	8b 50 0c             	mov    0xc(%rax),%edx
   1400024d3:	85 d2                	test   %edx,%edx
   1400024d5:	74 d7                	je     1400024ae <__mingw_enum_import_library_names+0x8e>
   1400024d7:	85 c9                	test   %ecx,%ecx
   1400024d9:	7f e5                	jg     1400024c0 <__mingw_enum_import_library_names+0xa0>
   1400024db:	44 8b 48 0c          	mov    0xc(%rax),%r9d
   1400024df:	4d 01 d9             	add    %r11,%r9
   1400024e2:	4c 89 c8             	mov    %r9,%rax
   1400024e5:	c3                   	ret
   1400024e6:	90                   	nop
   1400024e7:	90                   	nop
   1400024e8:	90                   	nop
   1400024e9:	90                   	nop
   1400024ea:	90                   	nop
   1400024eb:	90                   	nop
   1400024ec:	90                   	nop
   1400024ed:	90                   	nop
   1400024ee:	90                   	nop
   1400024ef:	90                   	nop

00000001400024f0 <___chkstk_ms>:
   1400024f0:	51                   	push   %rcx
   1400024f1:	50                   	push   %rax
   1400024f2:	48 3d 00 10 00 00    	cmp    $0x1000,%rax
   1400024f8:	48 8d 4c 24 18       	lea    0x18(%rsp),%rcx
   1400024fd:	72 19                	jb     140002518 <___chkstk_ms+0x28>
   1400024ff:	48 81 e9 00 10 00 00 	sub    $0x1000,%rcx
   140002506:	48 83 09 00          	orq    $0x0,(%rcx)
   14000250a:	48 2d 00 10 00 00    	sub    $0x1000,%rax
   140002510:	48 3d 00 10 00 00    	cmp    $0x1000,%rax
   140002516:	77 e7                	ja     1400024ff <___chkstk_ms+0xf>
   140002518:	48 29 c1             	sub    %rax,%rcx
   14000251b:	48 83 09 00          	orq    $0x0,(%rcx)
   14000251f:	58                   	pop    %rax
   140002520:	59                   	pop    %rcx
   140002521:	c3                   	ret
   140002522:	90                   	nop
   140002523:	90                   	nop
   140002524:	90                   	nop
   140002525:	90                   	nop
   140002526:	90                   	nop
   140002527:	90                   	nop
   140002528:	90                   	nop
   140002529:	90                   	nop
   14000252a:	90                   	nop
   14000252b:	90                   	nop
   14000252c:	90                   	nop
   14000252d:	90                   	nop
   14000252e:	90                   	nop
   14000252f:	90                   	nop

0000000140002530 <__p__fmode>:
   140002530:	48 8b 05 89 1e 00 00 	mov    0x1e89(%rip),%rax        # 1400043c0 <.refptr.__imp__fmode>
   140002537:	48 8b 00             	mov    (%rax),%rax
   14000253a:	c3                   	ret
   14000253b:	90                   	nop
   14000253c:	90                   	nop
   14000253d:	90                   	nop
   14000253e:	90                   	nop
   14000253f:	90                   	nop

0000000140002540 <__p__commode>:
   140002540:	48 8b 05 69 1e 00 00 	mov    0x1e69(%rip),%rax        # 1400043b0 <.refptr.__imp__commode>
   140002547:	48 8b 00             	mov    (%rax),%rax
   14000254a:	c3                   	ret
   14000254b:	90                   	nop
   14000254c:	90                   	nop
   14000254d:	90                   	nop
   14000254e:	90                   	nop
   14000254f:	90                   	nop

0000000140002550 <_get_invalid_parameter_handler>:
   140002550:	48 8b 05 19 4c 00 00 	mov    0x4c19(%rip),%rax        # 140007170 <handler>
   140002557:	c3                   	ret
   140002558:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   14000255f:	00 

0000000140002560 <_set_invalid_parameter_handler>:
   140002560:	48 89 c8             	mov    %rcx,%rax
   140002563:	48 87 05 06 4c 00 00 	xchg   %rax,0x4c06(%rip)        # 140007170 <handler>
   14000256a:	c3                   	ret
   14000256b:	90                   	nop
   14000256c:	90                   	nop
   14000256d:	90                   	nop
   14000256e:	90                   	nop
   14000256f:	90                   	nop

0000000140002570 <__acrt_iob_func>:
   140002570:	53                   	push   %rbx
   140002571:	48 83 ec 20          	sub    $0x20,%rsp
   140002575:	89 cb                	mov    %ecx,%ebx
   140002577:	e8 24 00 00 00       	call   1400025a0 <__iob_func>
   14000257c:	89 d9                	mov    %ebx,%ecx
   14000257e:	48 8d 14 49          	lea    (%rcx,%rcx,2),%rdx
   140002582:	48 c1 e2 04          	shl    $0x4,%rdx
   140002586:	48 01 d0             	add    %rdx,%rax
   140002589:	48 83 c4 20          	add    $0x20,%rsp
   14000258d:	5b                   	pop    %rbx
   14000258e:	c3                   	ret
   14000258f:	90                   	nop

0000000140002590 <__C_specific_handler>:
   140002590:	ff 25 1e 5c 00 00    	jmp    *0x5c1e(%rip)        # 1400081b4 <__imp___C_specific_handler>
   140002596:	90                   	nop
   140002597:	90                   	nop

0000000140002598 <__getmainargs>:
   140002598:	ff 25 1e 5c 00 00    	jmp    *0x5c1e(%rip)        # 1400081bc <__imp___getmainargs>
   14000259e:	90                   	nop
   14000259f:	90                   	nop

00000001400025a0 <__iob_func>:
   1400025a0:	ff 25 26 5c 00 00    	jmp    *0x5c26(%rip)        # 1400081cc <__imp___iob_func>
   1400025a6:	90                   	nop
   1400025a7:	90                   	nop

00000001400025a8 <__set_app_type>:
   1400025a8:	ff 25 26 5c 00 00    	jmp    *0x5c26(%rip)        # 1400081d4 <__imp___set_app_type>
   1400025ae:	90                   	nop
   1400025af:	90                   	nop

00000001400025b0 <__setusermatherr>:
   1400025b0:	ff 25 26 5c 00 00    	jmp    *0x5c26(%rip)        # 1400081dc <__imp___setusermatherr>
   1400025b6:	90                   	nop
   1400025b7:	90                   	nop

00000001400025b8 <_amsg_exit>:
   1400025b8:	ff 25 26 5c 00 00    	jmp    *0x5c26(%rip)        # 1400081e4 <__imp__amsg_exit>
   1400025be:	90                   	nop
   1400025bf:	90                   	nop

00000001400025c0 <_cexit>:
   1400025c0:	ff 25 26 5c 00 00    	jmp    *0x5c26(%rip)        # 1400081ec <__imp__cexit>
   1400025c6:	90                   	nop
   1400025c7:	90                   	nop

00000001400025c8 <_initterm>:
   1400025c8:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 140008204 <__imp__initterm>
   1400025ce:	90                   	nop
   1400025cf:	90                   	nop

00000001400025d0 <_onexit>:
   1400025d0:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 14000820c <__imp__onexit>
   1400025d6:	90                   	nop
   1400025d7:	90                   	nop

00000001400025d8 <abort>:
   1400025d8:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 140008214 <__imp_abort>
   1400025de:	90                   	nop
   1400025df:	90                   	nop

00000001400025e0 <calloc>:
   1400025e0:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 14000821c <__imp_calloc>
   1400025e6:	90                   	nop
   1400025e7:	90                   	nop

00000001400025e8 <exit>:
   1400025e8:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 140008224 <__imp_exit>
   1400025ee:	90                   	nop
   1400025ef:	90                   	nop

00000001400025f0 <fprintf>:
   1400025f0:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 14000822c <__imp_fprintf>
   1400025f6:	90                   	nop
   1400025f7:	90                   	nop

00000001400025f8 <free>:
   1400025f8:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 140008234 <__imp_free>
   1400025fe:	90                   	nop
   1400025ff:	90                   	nop

0000000140002600 <fwrite>:
   140002600:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 14000823c <__imp_fwrite>
   140002606:	90                   	nop
   140002607:	90                   	nop

0000000140002608 <malloc>:
   140002608:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 140008244 <__imp_malloc>
   14000260e:	90                   	nop
   14000260f:	90                   	nop

0000000140002610 <memcpy>:
   140002610:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 14000824c <__imp_memcpy>
   140002616:	90                   	nop
   140002617:	90                   	nop

0000000140002618 <signal>:
   140002618:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 140008254 <__imp_signal>
   14000261e:	90                   	nop
   14000261f:	90                   	nop

0000000140002620 <strlen>:
   140002620:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 14000825c <__imp_strlen>
   140002626:	90                   	nop
   140002627:	90                   	nop

0000000140002628 <strncmp>:
   140002628:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 140008264 <__imp_strncmp>
   14000262e:	90                   	nop
   14000262f:	90                   	nop

0000000140002630 <vfprintf>:
   140002630:	ff 25 36 5c 00 00    	jmp    *0x5c36(%rip)        # 14000826c <__imp_vfprintf>
   140002636:	90                   	nop
   140002637:	90                   	nop
   140002638:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   14000263f:	00 

0000000140002640 <VirtualQuery>:
   140002640:	ff 25 5e 5b 00 00    	jmp    *0x5b5e(%rip)        # 1400081a4 <__imp_VirtualQuery>
   140002646:	90                   	nop
   140002647:	90                   	nop

0000000140002648 <VirtualProtect>:
   140002648:	ff 25 4e 5b 00 00    	jmp    *0x5b4e(%rip)        # 14000819c <__imp_VirtualProtect>
   14000264e:	90                   	nop
   14000264f:	90                   	nop

0000000140002650 <TlsGetValue>:
   140002650:	ff 25 3e 5b 00 00    	jmp    *0x5b3e(%rip)        # 140008194 <__imp_TlsGetValue>
   140002656:	90                   	nop
   140002657:	90                   	nop

0000000140002658 <Sleep>:
   140002658:	ff 25 2e 5b 00 00    	jmp    *0x5b2e(%rip)        # 14000818c <__imp_Sleep>
   14000265e:	90                   	nop
   14000265f:	90                   	nop

0000000140002660 <SetUnhandledExceptionFilter>:
   140002660:	ff 25 1e 5b 00 00    	jmp    *0x5b1e(%rip)        # 140008184 <__imp_SetUnhandledExceptionFilter>
   140002666:	90                   	nop
   140002667:	90                   	nop

0000000140002668 <LeaveCriticalSection>:
   140002668:	ff 25 0e 5b 00 00    	jmp    *0x5b0e(%rip)        # 14000817c <__imp_LeaveCriticalSection>
   14000266e:	90                   	nop
   14000266f:	90                   	nop

0000000140002670 <InitializeCriticalSection>:
   140002670:	ff 25 fe 5a 00 00    	jmp    *0x5afe(%rip)        # 140008174 <__imp_InitializeCriticalSection>
   140002676:	90                   	nop
   140002677:	90                   	nop

0000000140002678 <GetLastError>:
   140002678:	ff 25 ee 5a 00 00    	jmp    *0x5aee(%rip)        # 14000816c <__imp_GetLastError>
   14000267e:	90                   	nop
   14000267f:	90                   	nop

0000000140002680 <EnterCriticalSection>:
   140002680:	ff 25 de 5a 00 00    	jmp    *0x5ade(%rip)        # 140008164 <__imp_EnterCriticalSection>
   140002686:	90                   	nop
   140002687:	90                   	nop

0000000140002688 <DeleteCriticalSection>:
   140002688:	ff 25 ce 5a 00 00    	jmp    *0x5ace(%rip)        # 14000815c <__IAT_start__>
   14000268e:	90                   	nop
   14000268f:	90                   	nop

0000000140002690 <main>:
   140002690:	48 83 ec 28          	sub    $0x28,%rsp
   140002694:	e8 a7 ee ff ff       	call   140001540 <__main>
   140002699:	b9 01 00 00 00       	mov    $0x1,%ecx
   14000269e:	48 83 c4 28          	add    $0x28,%rsp
   1400026a2:	e9 a9 ed ff ff       	jmp    140001450 <_Z6driveri>
   1400026a7:	90                   	nop
   1400026a8:	90                   	nop
   1400026a9:	90                   	nop
   1400026aa:	90                   	nop
   1400026ab:	90                   	nop
   1400026ac:	90                   	nop
   1400026ad:	90                   	nop
   1400026ae:	90                   	nop
   1400026af:	90                   	nop

00000001400026b0 <register_frame_ctor>:
   1400026b0:	e9 7b ed ff ff       	jmp    140001430 <__gcc_register_frame>
   1400026b5:	90                   	nop
   1400026b6:	90                   	nop
   1400026b7:	90                   	nop
   1400026b8:	90                   	nop
   1400026b9:	90                   	nop
   1400026ba:	90                   	nop
   1400026bb:	90                   	nop
   1400026bc:	90                   	nop
   1400026bd:	90                   	nop
   1400026be:	90                   	nop
   1400026bf:	90                   	nop

00000001400026c0 <__CTOR_LIST__>:
   1400026c0:	ff                   	(bad)
   1400026c1:	ff                   	(bad)
   1400026c2:	ff                   	(bad)
   1400026c3:	ff                   	(bad)
   1400026c4:	ff                   	(bad)
   1400026c5:	ff                   	(bad)
   1400026c6:	ff                   	(bad)
   1400026c7:	ff                   	.byte 0xff

00000001400026c8 <.ctors.65535>:
   1400026c8:	b0 26                	mov    $0x26,%al
   1400026ca:	00 40 01             	add    %al,0x1(%rax)
	...

00000001400026d8 <__DTOR_LIST__>:
   1400026d8:	ff                   	(bad)
   1400026d9:	ff                   	(bad)
   1400026da:	ff                   	(bad)
   1400026db:	ff                   	(bad)
   1400026dc:	ff                   	(bad)
   1400026dd:	ff                   	(bad)
   1400026de:	ff                   	(bad)
   1400026df:	ff 00                	incl   (%rax)
   1400026e1:	00 00                	add    %al,(%rax)
   1400026e3:	00 00                	add    %al,(%rax)
   1400026e5:	00 00                	add    %al,(%rax)
	...
