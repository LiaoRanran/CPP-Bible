
app_lto.exe:     file format pei-x86-64


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
   140001072:	e8 f1 14 00 00       	call   140002568 <__set_app_type>
   140001077:	e8 74 14 00 00       	call   1400024f0 <__p__fmode>
   14000107c:	48 8b 15 1d 34 00 00 	mov    0x341d(%rip),%rdx        # 1400044a0 <.refptr._fmode>
   140001083:	8b 12                	mov    (%rdx),%edx
   140001085:	89 10                	mov    %edx,(%rax)
   140001087:	e8 74 14 00 00       	call   140002500 <__p__commode>
   14000108c:	48 8b 15 ed 33 00 00 	mov    0x33ed(%rip),%rdx        # 140004480 <.refptr._commode>
   140001093:	8b 12                	mov    (%rdx),%edx
   140001095:	89 10                	mov    %edx,(%rax)
   140001097:	e8 84 04 00 00       	call   140001520 <_setargv>
   14000109c:	48 8b 05 9d 32 00 00 	mov    0x329d(%rip),%rax        # 140004340 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   1400010a3:	83 38 01             	cmpl   $0x1,(%rax)
   1400010a6:	74 50                	je     1400010f8 <pre_c_init+0xe8>
   1400010a8:	31 c0                	xor    %eax,%eax
   1400010aa:	48 83 c4 28          	add    $0x28,%rsp
   1400010ae:	c3                   	ret
   1400010af:	90                   	nop
   1400010b0:	b9 01 00 00 00       	mov    $0x1,%ecx
   1400010b5:	e8 ae 14 00 00       	call   140002568 <__set_app_type>
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
   1400010ff:	e8 8c 0b 00 00       	call   140001c90 <__mingw_setusermatherr>
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
   14000116e:	e8 e5 13 00 00       	call   140002558 <__getmainargs>
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
   140001223:	e8 c8 06 00 00       	call   1400018f0 <_pei386_runtime_relocator>
   140001228:	48 8b 0d 81 32 00 00 	mov    0x3281(%rip),%rcx        # 1400044b0 <.refptr._gnu_exception_handler>
   14000122f:	ff 15 4f 6f 00 00    	call   *0x6f4f(%rip)        # 140008184 <__imp_SetUnhandledExceptionFilter>
   140001235:	48 8b 15 d4 31 00 00 	mov    0x31d4(%rip),%rdx        # 140004410 <.refptr.__mingw_oldexcpt_handler>
   14000123c:	48 8d 0d bd fd ff ff 	lea    -0x243(%rip),%rcx        # 140001000 <__mingw_invalidParameterHandler>
   140001243:	48 89 02             	mov    %rax,(%rdx)
   140001246:	e8 d5 12 00 00       	call   140002520 <_set_invalid_parameter_handler>
   14000124b:	e8 b0 04 00 00       	call   140001700 <_fpreset>
   140001250:	8b 1d d2 5d 00 00    	mov    0x5dd2(%rip),%ebx        # 140007028 <argc>
   140001256:	8d 7b 01             	lea    0x1(%rbx),%edi
   140001259:	48 63 ff             	movslq %edi,%rdi
   14000125c:	48 c1 e7 03          	shl    $0x3,%rdi
   140001260:	48 89 f9             	mov    %rdi,%rcx
   140001263:	e8 60 13 00 00       	call   1400025c8 <malloc>
   140001268:	85 db                	test   %ebx,%ebx
   14000126a:	48 8b 2d af 5d 00 00 	mov    0x5daf(%rip),%rbp        # 140007020 <argv>
   140001271:	49 89 c4             	mov    %rax,%r12
   140001274:	0f 8e 46 01 00 00    	jle    1400013c0 <__tmainCRTStartup+0x240>
   14000127a:	48 83 ef 08          	sub    $0x8,%rdi
   14000127e:	31 db                	xor    %ebx,%ebx
   140001280:	48 8b 4c 1d 00       	mov    0x0(%rbp,%rbx,1),%rcx
   140001285:	e8 56 13 00 00       	call   1400025e0 <strlen>
   14000128a:	48 8d 70 01          	lea    0x1(%rax),%rsi
   14000128e:	48 89 f1             	mov    %rsi,%rcx
   140001291:	e8 32 13 00 00       	call   1400025c8 <malloc>
   140001296:	49 89 f0             	mov    %rsi,%r8
   140001299:	49 89 04 1c          	mov    %rax,(%r12,%rbx,1)
   14000129d:	48 8b 54 1d 00       	mov    0x0(%rbp,%rbx,1),%rdx
   1400012a2:	48 89 c1             	mov    %rax,%rcx
   1400012a5:	48 83 c3 08          	add    $0x8,%rbx
   1400012a9:	e8 22 13 00 00       	call   1400025d0 <memcpy>
   1400012ae:	48 39 df             	cmp    %rbx,%rdi
   1400012b1:	75 cd                	jne    140001280 <__tmainCRTStartup+0x100>
   1400012b3:	4c 01 e7             	add    %r12,%rdi
   1400012b6:	48 c7 07 00 00 00 00 	movq   $0x0,(%rdi)
   1400012bd:	4c 89 25 5c 5d 00 00 	mov    %r12,0x5d5c(%rip)        # 140007020 <argv>
   1400012c4:	e8 37 02 00 00       	call   140001500 <__main>
   1400012c9:	48 8b 05 d0 30 00 00 	mov    0x30d0(%rip),%rax        # 1400043a0 <.refptr.__imp___initenv>
   1400012d0:	4c 8b 05 41 5d 00 00 	mov    0x5d41(%rip),%r8        # 140007018 <envp>
   1400012d7:	8b 0d 4b 5d 00 00    	mov    0x5d4b(%rip),%ecx        # 140007028 <argc>
   1400012dd:	48 8b 00             	mov    (%rax),%rax
   1400012e0:	4c 89 00             	mov    %r8,(%rax)
   1400012e3:	48 8b 15 36 5d 00 00 	mov    0x5d36(%rip),%rdx        # 140007020 <argv>
   1400012ea:	e8 61 13 00 00       	call   140002650 <main>
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
   14000133c:	e8 37 12 00 00       	call   140002578 <_amsg_exit>
   140001341:	8b 06                	mov    (%rsi),%eax
   140001343:	83 f8 01             	cmp    $0x1,%eax
   140001346:	0f 85 b4 fe ff ff    	jne    140001200 <__tmainCRTStartup+0x80>
   14000134c:	48 8b 15 fd 30 00 00 	mov    0x30fd(%rip),%rdx        # 140004450 <.refptr.__xc_z>
   140001353:	48 8b 0d e6 30 00 00 	mov    0x30e6(%rip),%rcx        # 140004440 <.refptr.__xc_a>
   14000135a:	e8 29 12 00 00       	call   140002588 <_initterm>
   14000135f:	85 ff                	test   %edi,%edi
   140001361:	c7 06 02 00 00 00    	movl   $0x2,(%rsi)
   140001367:	0f 85 9b fe ff ff    	jne    140001208 <__tmainCRTStartup+0x88>
   14000136d:	31 c0                	xor    %eax,%eax
   14000136f:	48 87 03             	xchg   %rax,(%rbx)
   140001372:	e9 91 fe ff ff       	jmp    140001208 <__tmainCRTStartup+0x88>
   140001377:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   14000137e:	00 00 
   140001380:	e8 fb 11 00 00       	call   140002580 <_cexit>
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
   1400013b4:	e8 cf 11 00 00       	call   140002588 <_initterm>
   1400013b9:	e9 37 fe ff ff       	jmp    1400011f5 <__tmainCRTStartup+0x75>
   1400013be:	66 90                	xchg   %ax,%ax
   1400013c0:	48 89 c7             	mov    %rax,%rdi
   1400013c3:	e9 ee fe ff ff       	jmp    1400012b6 <__tmainCRTStartup+0x136>
   1400013c8:	89 c1                	mov    %eax,%ecx
   1400013ca:	e8 d9 11 00 00       	call   1400025a8 <exit>
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
   140001414:	e8 77 11 00 00       	call   140002590 <_onexit>
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

0000000140001450 <__do_global_dtors>:
   140001450:	48 83 ec 28          	sub    $0x28,%rsp
   140001454:	48 8b 05 a5 1b 00 00 	mov    0x1ba5(%rip),%rax        # 140003000 <__data_start__>
   14000145b:	48 8b 00             	mov    (%rax),%rax
   14000145e:	48 85 c0             	test   %rax,%rax
   140001461:	74 22                	je     140001485 <__do_global_dtors+0x35>
   140001463:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001468:	ff d0                	call   *%rax
   14000146a:	48 8b 05 8f 1b 00 00 	mov    0x1b8f(%rip),%rax        # 140003000 <__data_start__>
   140001471:	48 8d 50 08          	lea    0x8(%rax),%rdx
   140001475:	48 8b 40 08          	mov    0x8(%rax),%rax
   140001479:	48 89 15 80 1b 00 00 	mov    %rdx,0x1b80(%rip)        # 140003000 <__data_start__>
   140001480:	48 85 c0             	test   %rax,%rax
   140001483:	75 e3                	jne    140001468 <__do_global_dtors+0x18>
   140001485:	48 83 c4 28          	add    $0x28,%rsp
   140001489:	c3                   	ret
   14000148a:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)

0000000140001490 <__do_global_ctors>:
   140001490:	56                   	push   %rsi
   140001491:	53                   	push   %rbx
   140001492:	48 83 ec 28          	sub    $0x28,%rsp
   140001496:	48 8b 15 b3 2e 00 00 	mov    0x2eb3(%rip),%rdx        # 140004350 <.refptr.__CTOR_LIST__>
   14000149d:	48 8b 02             	mov    (%rdx),%rax
   1400014a0:	83 f8 ff             	cmp    $0xffffffff,%eax
   1400014a3:	89 c1                	mov    %eax,%ecx
   1400014a5:	74 39                	je     1400014e0 <__do_global_ctors+0x50>
   1400014a7:	85 c9                	test   %ecx,%ecx
   1400014a9:	74 20                	je     1400014cb <__do_global_ctors+0x3b>
   1400014ab:	89 c8                	mov    %ecx,%eax
   1400014ad:	83 e9 01             	sub    $0x1,%ecx
   1400014b0:	48 8d 1c c2          	lea    (%rdx,%rax,8),%rbx
   1400014b4:	48 29 c8             	sub    %rcx,%rax
   1400014b7:	48 8d 74 c2 f8       	lea    -0x8(%rdx,%rax,8),%rsi
   1400014bc:	0f 1f 40 00          	nopl   0x0(%rax)
   1400014c0:	ff 13                	call   *(%rbx)
   1400014c2:	48 83 eb 08          	sub    $0x8,%rbx
   1400014c6:	48 39 f3             	cmp    %rsi,%rbx
   1400014c9:	75 f5                	jne    1400014c0 <__do_global_ctors+0x30>
   1400014cb:	48 8d 0d 7e ff ff ff 	lea    -0x82(%rip),%rcx        # 140001450 <__do_global_dtors>
   1400014d2:	48 83 c4 28          	add    $0x28,%rsp
   1400014d6:	5b                   	pop    %rbx
   1400014d7:	5e                   	pop    %rsi
   1400014d8:	e9 33 ff ff ff       	jmp    140001410 <atexit>
   1400014dd:	0f 1f 00             	nopl   (%rax)
   1400014e0:	31 c0                	xor    %eax,%eax
   1400014e2:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
   1400014e8:	44 8d 40 01          	lea    0x1(%rax),%r8d
   1400014ec:	89 c1                	mov    %eax,%ecx
   1400014ee:	4a 83 3c c2 00       	cmpq   $0x0,(%rdx,%r8,8)
   1400014f3:	4c 89 c0             	mov    %r8,%rax
   1400014f6:	75 f0                	jne    1400014e8 <__do_global_ctors+0x58>
   1400014f8:	eb ad                	jmp    1400014a7 <__do_global_ctors+0x17>
   1400014fa:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)

0000000140001500 <__main>:
   140001500:	8b 05 2a 5b 00 00    	mov    0x5b2a(%rip),%eax        # 140007030 <initialized>
   140001506:	85 c0                	test   %eax,%eax
   140001508:	74 06                	je     140001510 <__main+0x10>
   14000150a:	c3                   	ret
   14000150b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001510:	c7 05 16 5b 00 00 01 	movl   $0x1,0x5b16(%rip)        # 140007030 <initialized>
   140001517:	00 00 00 
   14000151a:	e9 71 ff ff ff       	jmp    140001490 <__do_global_ctors>
   14000151f:	90                   	nop

0000000140001520 <_setargv>:
   140001520:	31 c0                	xor    %eax,%eax
   140001522:	c3                   	ret
   140001523:	90                   	nop
   140001524:	90                   	nop
   140001525:	90                   	nop
   140001526:	90                   	nop
   140001527:	90                   	nop
   140001528:	90                   	nop
   140001529:	90                   	nop
   14000152a:	90                   	nop
   14000152b:	90                   	nop
   14000152c:	90                   	nop
   14000152d:	90                   	nop
   14000152e:	90                   	nop
   14000152f:	90                   	nop

0000000140001530 <__dyn_tls_dtor>:
   140001530:	48 83 ec 28          	sub    $0x28,%rsp
   140001534:	83 fa 03             	cmp    $0x3,%edx
   140001537:	74 17                	je     140001550 <__dyn_tls_dtor+0x20>
   140001539:	85 d2                	test   %edx,%edx
   14000153b:	74 13                	je     140001550 <__dyn_tls_dtor+0x20>
   14000153d:	b8 01 00 00 00       	mov    $0x1,%eax
   140001542:	48 83 c4 28          	add    $0x28,%rsp
   140001546:	c3                   	ret
   140001547:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   14000154e:	00 00 
   140001550:	e8 5b 0a 00 00       	call   140001fb0 <__mingw_TLScallback>
   140001555:	b8 01 00 00 00       	mov    $0x1,%eax
   14000155a:	48 83 c4 28          	add    $0x28,%rsp
   14000155e:	c3                   	ret
   14000155f:	90                   	nop

0000000140001560 <__dyn_tls_init>:
   140001560:	56                   	push   %rsi
   140001561:	53                   	push   %rbx
   140001562:	48 83 ec 28          	sub    $0x28,%rsp
   140001566:	48 8b 05 c3 2d 00 00 	mov    0x2dc3(%rip),%rax        # 140004330 <.refptr._CRT_MT>
   14000156d:	83 38 02             	cmpl   $0x2,(%rax)
   140001570:	74 06                	je     140001578 <__dyn_tls_init+0x18>
   140001572:	c7 00 02 00 00 00    	movl   $0x2,(%rax)
   140001578:	83 fa 02             	cmp    $0x2,%edx
   14000157b:	74 13                	je     140001590 <__dyn_tls_init+0x30>
   14000157d:	83 fa 01             	cmp    $0x1,%edx
   140001580:	74 4e                	je     1400015d0 <__dyn_tls_init+0x70>
   140001582:	b8 01 00 00 00       	mov    $0x1,%eax
   140001587:	48 83 c4 28          	add    $0x28,%rsp
   14000158b:	5b                   	pop    %rbx
   14000158c:	5e                   	pop    %rsi
   14000158d:	c3                   	ret
   14000158e:	66 90                	xchg   %ax,%ax
   140001590:	48 8d 1d c1 7a 00 00 	lea    0x7ac1(%rip),%rbx        # 140009058 <__xd_z>
   140001597:	48 8d 35 ba 7a 00 00 	lea    0x7aba(%rip),%rsi        # 140009058 <__xd_z>
   14000159e:	48 39 de             	cmp    %rbx,%rsi
   1400015a1:	74 df                	je     140001582 <__dyn_tls_init+0x22>
   1400015a3:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   1400015a8:	48 8b 03             	mov    (%rbx),%rax
   1400015ab:	48 85 c0             	test   %rax,%rax
   1400015ae:	74 02                	je     1400015b2 <__dyn_tls_init+0x52>
   1400015b0:	ff d0                	call   *%rax
   1400015b2:	48 83 c3 08          	add    $0x8,%rbx
   1400015b6:	48 39 de             	cmp    %rbx,%rsi
   1400015b9:	75 ed                	jne    1400015a8 <__dyn_tls_init+0x48>
   1400015bb:	b8 01 00 00 00       	mov    $0x1,%eax
   1400015c0:	48 83 c4 28          	add    $0x28,%rsp
   1400015c4:	5b                   	pop    %rbx
   1400015c5:	5e                   	pop    %rsi
   1400015c6:	c3                   	ret
   1400015c7:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   1400015ce:	00 00 
   1400015d0:	e8 db 09 00 00       	call   140001fb0 <__mingw_TLScallback>
   1400015d5:	b8 01 00 00 00       	mov    $0x1,%eax
   1400015da:	48 83 c4 28          	add    $0x28,%rsp
   1400015de:	5b                   	pop    %rbx
   1400015df:	5e                   	pop    %rsi
   1400015e0:	c3                   	ret
   1400015e1:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   1400015e8:	00 00 00 00 
   1400015ec:	0f 1f 40 00          	nopl   0x0(%rax)

00000001400015f0 <__tlregdtor>:
   1400015f0:	31 c0                	xor    %eax,%eax
   1400015f2:	c3                   	ret
   1400015f3:	90                   	nop
   1400015f4:	90                   	nop
   1400015f5:	90                   	nop
   1400015f6:	90                   	nop
   1400015f7:	90                   	nop
   1400015f8:	90                   	nop
   1400015f9:	90                   	nop
   1400015fa:	90                   	nop
   1400015fb:	90                   	nop
   1400015fc:	90                   	nop
   1400015fd:	90                   	nop
   1400015fe:	90                   	nop
   1400015ff:	90                   	nop

0000000140001600 <_matherr>:
   140001600:	56                   	push   %rsi
   140001601:	53                   	push   %rbx
   140001602:	48 83 ec 78          	sub    $0x78,%rsp
   140001606:	0f 29 74 24 40       	movaps %xmm6,0x40(%rsp)
   14000160b:	0f 29 7c 24 50       	movaps %xmm7,0x50(%rsp)
   140001610:	44 0f 29 44 24 60    	movaps %xmm8,0x60(%rsp)
   140001616:	83 39 06             	cmpl   $0x6,(%rcx)
   140001619:	0f 87 cd 00 00 00    	ja     1400016ec <_matherr+0xec>
   14000161f:	8b 01                	mov    (%rcx),%eax
   140001621:	48 8d 15 5c 2b 00 00 	lea    0x2b5c(%rip),%rdx        # 140004184 <.rdata+0x124>
   140001628:	48 63 04 82          	movslq (%rdx,%rax,4),%rax
   14000162c:	48 01 d0             	add    %rdx,%rax
   14000162f:	ff e0                	jmp    *%rax
   140001631:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140001638:	48 8d 1d 40 2a 00 00 	lea    0x2a40(%rip),%rbx        # 14000407f <.rdata+0x1f>
   14000163f:	48 8b 71 08          	mov    0x8(%rcx),%rsi
   140001643:	f2 44 0f 10 41 20    	movsd  0x20(%rcx),%xmm8
   140001649:	f2 0f 10 79 18       	movsd  0x18(%rcx),%xmm7
   14000164e:	f2 0f 10 71 10       	movsd  0x10(%rcx),%xmm6
   140001653:	b9 02 00 00 00       	mov    $0x2,%ecx
   140001658:	e8 d3 0e 00 00       	call   140002530 <__acrt_iob_func>
   14000165d:	f2 44 0f 11 44 24 30 	movsd  %xmm8,0x30(%rsp)
   140001664:	49 89 f1             	mov    %rsi,%r9
   140001667:	49 89 d8             	mov    %rbx,%r8
   14000166a:	f2 0f 11 7c 24 28    	movsd  %xmm7,0x28(%rsp)
   140001670:	48 89 c1             	mov    %rax,%rcx
   140001673:	f2 0f 11 74 24 20    	movsd  %xmm6,0x20(%rsp)
   140001679:	48 8d 15 d8 2a 00 00 	lea    0x2ad8(%rip),%rdx        # 140004158 <.rdata+0xf8>
   140001680:	e8 2b 0f 00 00       	call   1400025b0 <fprintf>
   140001685:	90                   	nop
   140001686:	0f 28 74 24 40       	movaps 0x40(%rsp),%xmm6
   14000168b:	31 c0                	xor    %eax,%eax
   14000168d:	0f 28 7c 24 50       	movaps 0x50(%rsp),%xmm7
   140001692:	44 0f 28 44 24 60    	movaps 0x60(%rsp),%xmm8
   140001698:	48 83 c4 78          	add    $0x78,%rsp
   14000169c:	5b                   	pop    %rbx
   14000169d:	5e                   	pop    %rsi
   14000169e:	c3                   	ret
   14000169f:	90                   	nop
   1400016a0:	48 8d 1d b9 29 00 00 	lea    0x29b9(%rip),%rbx        # 140004060 <.rdata>
   1400016a7:	eb 96                	jmp    14000163f <_matherr+0x3f>
   1400016a9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400016b0:	48 8d 1d 09 2a 00 00 	lea    0x2a09(%rip),%rbx        # 1400040c0 <.rdata+0x60>
   1400016b7:	eb 86                	jmp    14000163f <_matherr+0x3f>
   1400016b9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400016c0:	48 8d 1d d9 29 00 00 	lea    0x29d9(%rip),%rbx        # 1400040a0 <.rdata+0x40>
   1400016c7:	e9 73 ff ff ff       	jmp    14000163f <_matherr+0x3f>
   1400016cc:	0f 1f 40 00          	nopl   0x0(%rax)
   1400016d0:	48 8d 1d 39 2a 00 00 	lea    0x2a39(%rip),%rbx        # 140004110 <.rdata+0xb0>
   1400016d7:	e9 63 ff ff ff       	jmp    14000163f <_matherr+0x3f>
   1400016dc:	0f 1f 40 00          	nopl   0x0(%rax)
   1400016e0:	48 8d 1d 01 2a 00 00 	lea    0x2a01(%rip),%rbx        # 1400040e8 <.rdata+0x88>
   1400016e7:	e9 53 ff ff ff       	jmp    14000163f <_matherr+0x3f>
   1400016ec:	48 8d 1d 53 2a 00 00 	lea    0x2a53(%rip),%rbx        # 140004146 <.rdata+0xe6>
   1400016f3:	e9 47 ff ff ff       	jmp    14000163f <_matherr+0x3f>
   1400016f8:	90                   	nop
   1400016f9:	90                   	nop
   1400016fa:	90                   	nop
   1400016fb:	90                   	nop
   1400016fc:	90                   	nop
   1400016fd:	90                   	nop
   1400016fe:	90                   	nop
   1400016ff:	90                   	nop

0000000140001700 <_fpreset>:
   140001700:	db e3                	fninit
   140001702:	c3                   	ret
   140001703:	90                   	nop
   140001704:	90                   	nop
   140001705:	90                   	nop
   140001706:	90                   	nop
   140001707:	90                   	nop
   140001708:	90                   	nop
   140001709:	90                   	nop
   14000170a:	90                   	nop
   14000170b:	90                   	nop
   14000170c:	90                   	nop
   14000170d:	90                   	nop
   14000170e:	90                   	nop
   14000170f:	90                   	nop

0000000140001710 <__report_error>:
   140001710:	56                   	push   %rsi
   140001711:	53                   	push   %rbx
   140001712:	48 83 ec 38          	sub    $0x38,%rsp
   140001716:	48 8d 44 24 58       	lea    0x58(%rsp),%rax
   14000171b:	48 89 cb             	mov    %rcx,%rbx
   14000171e:	b9 02 00 00 00       	mov    $0x2,%ecx
   140001723:	48 89 54 24 58       	mov    %rdx,0x58(%rsp)
   140001728:	4c 89 44 24 60       	mov    %r8,0x60(%rsp)
   14000172d:	4c 89 4c 24 68       	mov    %r9,0x68(%rsp)
   140001732:	48 89 44 24 28       	mov    %rax,0x28(%rsp)
   140001737:	e8 f4 0d 00 00       	call   140002530 <__acrt_iob_func>
   14000173c:	41 b8 1b 00 00 00    	mov    $0x1b,%r8d
   140001742:	ba 01 00 00 00       	mov    $0x1,%edx
   140001747:	48 8d 0d 52 2a 00 00 	lea    0x2a52(%rip),%rcx        # 1400041a0 <.rdata>
   14000174e:	49 89 c1             	mov    %rax,%r9
   140001751:	e8 6a 0e 00 00       	call   1400025c0 <fwrite>
   140001756:	48 8b 74 24 28       	mov    0x28(%rsp),%rsi
   14000175b:	b9 02 00 00 00       	mov    $0x2,%ecx
   140001760:	e8 cb 0d 00 00       	call   140002530 <__acrt_iob_func>
   140001765:	48 89 da             	mov    %rbx,%rdx
   140001768:	48 89 c1             	mov    %rax,%rcx
   14000176b:	49 89 f0             	mov    %rsi,%r8
   14000176e:	e8 7d 0e 00 00       	call   1400025f0 <vfprintf>
   140001773:	e8 20 0e 00 00       	call   140002598 <abort>
   140001778:	90                   	nop
   140001779:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000140001780 <mark_section_writable>:
   140001780:	57                   	push   %rdi
   140001781:	56                   	push   %rsi
   140001782:	53                   	push   %rbx
   140001783:	48 83 ec 50          	sub    $0x50,%rsp
   140001787:	48 63 35 06 59 00 00 	movslq 0x5906(%rip),%rsi        # 140007094 <maxSections>
   14000178e:	85 f6                	test   %esi,%esi
   140001790:	48 89 cb             	mov    %rcx,%rbx
   140001793:	0f 8e 17 01 00 00    	jle    1400018b0 <mark_section_writable+0x130>
   140001799:	48 8b 05 f8 58 00 00 	mov    0x58f8(%rip),%rax        # 140007098 <the_secs>
   1400017a0:	45 31 c9             	xor    %r9d,%r9d
   1400017a3:	48 83 c0 18          	add    $0x18,%rax
   1400017a7:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   1400017ae:	00 00 
   1400017b0:	4c 8b 00             	mov    (%rax),%r8
   1400017b3:	4c 39 c3             	cmp    %r8,%rbx
   1400017b6:	72 13                	jb     1400017cb <mark_section_writable+0x4b>
   1400017b8:	48 8b 50 08          	mov    0x8(%rax),%rdx
   1400017bc:	8b 52 08             	mov    0x8(%rdx),%edx
   1400017bf:	49 01 d0             	add    %rdx,%r8
   1400017c2:	4c 39 c3             	cmp    %r8,%rbx
   1400017c5:	0f 82 8a 00 00 00    	jb     140001855 <mark_section_writable+0xd5>
   1400017cb:	41 83 c1 01          	add    $0x1,%r9d
   1400017cf:	48 83 c0 28          	add    $0x28,%rax
   1400017d3:	41 39 f1             	cmp    %esi,%r9d
   1400017d6:	75 d8                	jne    1400017b0 <mark_section_writable+0x30>
   1400017d8:	48 89 d9             	mov    %rbx,%rcx
   1400017db:	e8 f0 09 00 00       	call   1400021d0 <__mingw_GetSectionForAddress>
   1400017e0:	48 85 c0             	test   %rax,%rax
   1400017e3:	48 89 c7             	mov    %rax,%rdi
   1400017e6:	0f 84 e6 00 00 00    	je     1400018d2 <mark_section_writable+0x152>
   1400017ec:	48 8b 05 a5 58 00 00 	mov    0x58a5(%rip),%rax        # 140007098 <the_secs>
   1400017f3:	48 8d 1c b6          	lea    (%rsi,%rsi,4),%rbx
   1400017f7:	48 c1 e3 03          	shl    $0x3,%rbx
   1400017fb:	48 01 d8             	add    %rbx,%rax
   1400017fe:	48 89 78 20          	mov    %rdi,0x20(%rax)
   140001802:	c7 00 00 00 00 00    	movl   $0x0,(%rax)
   140001808:	e8 03 0b 00 00       	call   140002310 <_GetPEImageBase>
   14000180d:	8b 57 0c             	mov    0xc(%rdi),%edx
   140001810:	41 b8 30 00 00 00    	mov    $0x30,%r8d
   140001816:	48 8d 0c 10          	lea    (%rax,%rdx,1),%rcx
   14000181a:	48 8b 05 77 58 00 00 	mov    0x5877(%rip),%rax        # 140007098 <the_secs>
   140001821:	48 8d 54 24 20       	lea    0x20(%rsp),%rdx
   140001826:	48 89 4c 18 18       	mov    %rcx,0x18(%rax,%rbx,1)
   14000182b:	ff 15 73 69 00 00    	call   *0x6973(%rip)        # 1400081a4 <__imp_VirtualQuery>
   140001831:	48 85 c0             	test   %rax,%rax
   140001834:	0f 84 7d 00 00 00    	je     1400018b7 <mark_section_writable+0x137>
   14000183a:	8b 44 24 44          	mov    0x44(%rsp),%eax
   14000183e:	8d 50 c0             	lea    -0x40(%rax),%edx
   140001841:	83 e2 bf             	and    $0xffffffbf,%edx
   140001844:	74 08                	je     14000184e <mark_section_writable+0xce>
   140001846:	8d 50 fc             	lea    -0x4(%rax),%edx
   140001849:	83 e2 fb             	and    $0xfffffffb,%edx
   14000184c:	75 12                	jne    140001860 <mark_section_writable+0xe0>
   14000184e:	83 05 3f 58 00 00 01 	addl   $0x1,0x583f(%rip)        # 140007094 <maxSections>
   140001855:	48 83 c4 50          	add    $0x50,%rsp
   140001859:	5b                   	pop    %rbx
   14000185a:	5e                   	pop    %rsi
   14000185b:	5f                   	pop    %rdi
   14000185c:	c3                   	ret
   14000185d:	0f 1f 00             	nopl   (%rax)
   140001860:	83 f8 02             	cmp    $0x2,%eax
   140001863:	41 b8 40 00 00 00    	mov    $0x40,%r8d
   140001869:	b8 04 00 00 00       	mov    $0x4,%eax
   14000186e:	48 8b 4c 24 20       	mov    0x20(%rsp),%rcx
   140001873:	44 0f 44 c0          	cmove  %eax,%r8d
   140001877:	48 8b 54 24 38       	mov    0x38(%rsp),%rdx
   14000187c:	48 03 1d 15 58 00 00 	add    0x5815(%rip),%rbx        # 140007098 <the_secs>
   140001883:	49 89 d9             	mov    %rbx,%r9
   140001886:	48 89 4b 08          	mov    %rcx,0x8(%rbx)
   14000188a:	48 89 53 10          	mov    %rdx,0x10(%rbx)
   14000188e:	ff 15 08 69 00 00    	call   *0x6908(%rip)        # 14000819c <__imp_VirtualProtect>
   140001894:	85 c0                	test   %eax,%eax
   140001896:	75 b6                	jne    14000184e <mark_section_writable+0xce>
   140001898:	ff 15 ce 68 00 00    	call   *0x68ce(%rip)        # 14000816c <__imp_GetLastError>
   14000189e:	48 8d 0d 73 29 00 00 	lea    0x2973(%rip),%rcx        # 140004218 <.rdata+0x78>
   1400018a5:	89 c2                	mov    %eax,%edx
   1400018a7:	e8 64 fe ff ff       	call   140001710 <__report_error>
   1400018ac:	0f 1f 40 00          	nopl   0x0(%rax)
   1400018b0:	31 f6                	xor    %esi,%esi
   1400018b2:	e9 21 ff ff ff       	jmp    1400017d8 <mark_section_writable+0x58>
   1400018b7:	48 8b 05 da 57 00 00 	mov    0x57da(%rip),%rax        # 140007098 <the_secs>
   1400018be:	48 8d 0d 1b 29 00 00 	lea    0x291b(%rip),%rcx        # 1400041e0 <.rdata+0x40>
   1400018c5:	8b 57 08             	mov    0x8(%rdi),%edx
   1400018c8:	4c 8b 44 18 18       	mov    0x18(%rax,%rbx,1),%r8
   1400018cd:	e8 3e fe ff ff       	call   140001710 <__report_error>
   1400018d2:	48 8d 0d e7 28 00 00 	lea    0x28e7(%rip),%rcx        # 1400041c0 <.rdata+0x20>
   1400018d9:	48 89 da             	mov    %rbx,%rdx
   1400018dc:	e8 2f fe ff ff       	call   140001710 <__report_error>
   1400018e1:	90                   	nop
   1400018e2:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   1400018e9:	00 00 00 00 
   1400018ed:	0f 1f 00             	nopl   (%rax)

00000001400018f0 <_pei386_runtime_relocator>:
   1400018f0:	55                   	push   %rbp
   1400018f1:	41 57                	push   %r15
   1400018f3:	41 56                	push   %r14
   1400018f5:	41 55                	push   %r13
   1400018f7:	41 54                	push   %r12
   1400018f9:	57                   	push   %rdi
   1400018fa:	56                   	push   %rsi
   1400018fb:	53                   	push   %rbx
   1400018fc:	48 83 ec 48          	sub    $0x48,%rsp
   140001900:	48 8d 6c 24 40       	lea    0x40(%rsp),%rbp
   140001905:	8b 3d 85 57 00 00    	mov    0x5785(%rip),%edi        # 140007090 <was_init.0>
   14000190b:	85 ff                	test   %edi,%edi
   14000190d:	74 11                	je     140001920 <_pei386_runtime_relocator+0x30>
   14000190f:	48 8d 65 08          	lea    0x8(%rbp),%rsp
   140001913:	5b                   	pop    %rbx
   140001914:	5e                   	pop    %rsi
   140001915:	5f                   	pop    %rdi
   140001916:	41 5c                	pop    %r12
   140001918:	41 5d                	pop    %r13
   14000191a:	41 5e                	pop    %r14
   14000191c:	41 5f                	pop    %r15
   14000191e:	5d                   	pop    %rbp
   14000191f:	c3                   	ret
   140001920:	c7 05 66 57 00 00 01 	movl   $0x1,0x5766(%rip)        # 140007090 <was_init.0>
   140001927:	00 00 00 
   14000192a:	e8 21 09 00 00       	call   140002250 <__mingw_GetSectionCount>
   14000192f:	48 98                	cltq
   140001931:	48 8d 04 80          	lea    (%rax,%rax,4),%rax
   140001935:	48 8d 04 c5 0f 00 00 	lea    0xf(,%rax,8),%rax
   14000193c:	00 
   14000193d:	48 83 e0 f0          	and    $0xfffffffffffffff0,%rax
   140001941:	e8 6a 0b 00 00       	call   1400024b0 <___chkstk_ms>
   140001946:	4c 8b 2d 13 2a 00 00 	mov    0x2a13(%rip),%r13        # 140004360 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   14000194d:	c7 05 3d 57 00 00 00 	movl   $0x0,0x573d(%rip)        # 140007094 <maxSections>
   140001954:	00 00 00 
   140001957:	48 8b 1d 12 2a 00 00 	mov    0x2a12(%rip),%rbx        # 140004370 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000195e:	48 29 c4             	sub    %rax,%rsp
   140001961:	48 8d 44 24 30       	lea    0x30(%rsp),%rax
   140001966:	48 89 05 2b 57 00 00 	mov    %rax,0x572b(%rip)        # 140007098 <the_secs>
   14000196d:	4c 89 e8             	mov    %r13,%rax
   140001970:	48 29 d8             	sub    %rbx,%rax
   140001973:	48 83 f8 07          	cmp    $0x7,%rax
   140001977:	7e 96                	jle    14000190f <_pei386_runtime_relocator+0x1f>
   140001979:	48 83 f8 0b          	cmp    $0xb,%rax
   14000197d:	8b 13                	mov    (%rbx),%edx
   14000197f:	0f 8f 83 01 00 00    	jg     140001b08 <_pei386_runtime_relocator+0x218>
   140001985:	8b 03                	mov    (%rbx),%eax
   140001987:	85 c0                	test   %eax,%eax
   140001989:	0f 85 71 02 00 00    	jne    140001c00 <_pei386_runtime_relocator+0x310>
   14000198f:	8b 43 04             	mov    0x4(%rbx),%eax
   140001992:	85 c0                	test   %eax,%eax
   140001994:	0f 85 66 02 00 00    	jne    140001c00 <_pei386_runtime_relocator+0x310>
   14000199a:	8b 53 08             	mov    0x8(%rbx),%edx
   14000199d:	83 fa 01             	cmp    $0x1,%edx
   1400019a0:	0f 85 9c 02 00 00    	jne    140001c42 <_pei386_runtime_relocator+0x352>
   1400019a6:	48 83 c3 0c          	add    $0xc,%rbx
   1400019aa:	4c 39 eb             	cmp    %r13,%rbx
   1400019ad:	0f 83 5c ff ff ff    	jae    14000190f <_pei386_runtime_relocator+0x1f>
   1400019b3:	4c 8b 25 d6 29 00 00 	mov    0x29d6(%rip),%r12        # 140004390 <.refptr.__image_base__>
   1400019ba:	49 bf ff ff ff 7f ff 	movabs $0xffffffff7fffffff,%r15
   1400019c1:	ff ff ff 
   1400019c4:	eb 5d                	jmp    140001a23 <_pei386_runtime_relocator+0x133>
   1400019c6:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   1400019cd:	00 00 00 
   1400019d0:	41 0f b6 36          	movzbl (%r14),%esi
   1400019d4:	81 e1 c0 00 00 00    	and    $0xc0,%ecx
   1400019da:	40 84 f6             	test   %sil,%sil
   1400019dd:	0f 89 05 02 00 00    	jns    140001be8 <_pei386_runtime_relocator+0x2f8>
   1400019e3:	48 81 ce 00 ff ff ff 	or     $0xffffffffffffff00,%rsi
   1400019ea:	48 29 c6             	sub    %rax,%rsi
   1400019ed:	4c 01 ce             	add    %r9,%rsi
   1400019f0:	85 c9                	test   %ecx,%ecx
   1400019f2:	75 17                	jne    140001a0b <_pei386_runtime_relocator+0x11b>
   1400019f4:	48 81 fe ff 00 00 00 	cmp    $0xff,%rsi
   1400019fb:	0f 8f 4e 01 00 00    	jg     140001b4f <_pei386_runtime_relocator+0x25f>
   140001a01:	48 83 fe 80          	cmp    $0xffffffffffffff80,%rsi
   140001a05:	0f 8c 44 01 00 00    	jl     140001b4f <_pei386_runtime_relocator+0x25f>
   140001a0b:	4c 89 f1             	mov    %r14,%rcx
   140001a0e:	e8 6d fd ff ff       	call   140001780 <mark_section_writable>
   140001a13:	41 88 36             	mov    %sil,(%r14)
   140001a16:	48 83 c3 0c          	add    $0xc,%rbx
   140001a1a:	4c 39 eb             	cmp    %r13,%rbx
   140001a1d:	0f 83 8d 00 00 00    	jae    140001ab0 <_pei386_runtime_relocator+0x1c0>
   140001a23:	8b 4b 08             	mov    0x8(%rbx),%ecx
   140001a26:	8b 03                	mov    (%rbx),%eax
   140001a28:	44 8b 43 04          	mov    0x4(%rbx),%r8d
   140001a2c:	0f b6 d1             	movzbl %cl,%edx
   140001a2f:	4c 01 e0             	add    %r12,%rax
   140001a32:	83 fa 20             	cmp    $0x20,%edx
   140001a35:	4c 8b 08             	mov    (%rax),%r9
   140001a38:	4f 8d 34 20          	lea    (%r8,%r12,1),%r14
   140001a3c:	0f 84 26 01 00 00    	je     140001b68 <_pei386_runtime_relocator+0x278>
   140001a42:	0f 87 e8 00 00 00    	ja     140001b30 <_pei386_runtime_relocator+0x240>
   140001a48:	83 fa 08             	cmp    $0x8,%edx
   140001a4b:	74 83                	je     1400019d0 <_pei386_runtime_relocator+0xe0>
   140001a4d:	83 fa 10             	cmp    $0x10,%edx
   140001a50:	0f 85 e0 01 00 00    	jne    140001c36 <_pei386_runtime_relocator+0x346>
   140001a56:	41 0f b7 36          	movzwl (%r14),%esi
   140001a5a:	81 e1 c0 00 00 00    	and    $0xc0,%ecx
   140001a60:	66 85 f6             	test   %si,%si
   140001a63:	0f 89 67 01 00 00    	jns    140001bd0 <_pei386_runtime_relocator+0x2e0>
   140001a69:	48 81 ce 00 00 ff ff 	or     $0xffffffffffff0000,%rsi
   140001a70:	48 29 c6             	sub    %rax,%rsi
   140001a73:	4c 01 ce             	add    %r9,%rsi
   140001a76:	85 c9                	test   %ecx,%ecx
   140001a78:	75 1a                	jne    140001a94 <_pei386_runtime_relocator+0x1a4>
   140001a7a:	48 81 fe 00 80 ff ff 	cmp    $0xffffffffffff8000,%rsi
   140001a81:	0f 8c c8 00 00 00    	jl     140001b4f <_pei386_runtime_relocator+0x25f>
   140001a87:	48 81 fe ff ff 00 00 	cmp    $0xffff,%rsi
   140001a8e:	0f 8f bb 00 00 00    	jg     140001b4f <_pei386_runtime_relocator+0x25f>
   140001a94:	4c 89 f1             	mov    %r14,%rcx
   140001a97:	48 83 c3 0c          	add    $0xc,%rbx
   140001a9b:	e8 e0 fc ff ff       	call   140001780 <mark_section_writable>
   140001aa0:	4c 39 eb             	cmp    %r13,%rbx
   140001aa3:	66 41 89 36          	mov    %si,(%r14)
   140001aa7:	0f 82 76 ff ff ff    	jb     140001a23 <_pei386_runtime_relocator+0x133>
   140001aad:	0f 1f 00             	nopl   (%rax)
   140001ab0:	8b 15 de 55 00 00    	mov    0x55de(%rip),%edx        # 140007094 <maxSections>
   140001ab6:	85 d2                	test   %edx,%edx
   140001ab8:	0f 8e 51 fe ff ff    	jle    14000190f <_pei386_runtime_relocator+0x1f>
   140001abe:	48 8b 35 d7 66 00 00 	mov    0x66d7(%rip),%rsi        # 14000819c <__imp_VirtualProtect>
   140001ac5:	4c 8d 65 fc          	lea    -0x4(%rbp),%r12
   140001ac9:	31 db                	xor    %ebx,%ebx
   140001acb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001ad0:	48 8b 05 c1 55 00 00 	mov    0x55c1(%rip),%rax        # 140007098 <the_secs>
   140001ad7:	48 01 d8             	add    %rbx,%rax
   140001ada:	44 8b 00             	mov    (%rax),%r8d
   140001add:	45 85 c0             	test   %r8d,%r8d
   140001ae0:	74 0d                	je     140001aef <_pei386_runtime_relocator+0x1ff>
   140001ae2:	48 8b 50 10          	mov    0x10(%rax),%rdx
   140001ae6:	4d 89 e1             	mov    %r12,%r9
   140001ae9:	48 8b 48 08          	mov    0x8(%rax),%rcx
   140001aed:	ff d6                	call   *%rsi
   140001aef:	83 c7 01             	add    $0x1,%edi
   140001af2:	48 83 c3 28          	add    $0x28,%rbx
   140001af6:	3b 3d 98 55 00 00    	cmp    0x5598(%rip),%edi        # 140007094 <maxSections>
   140001afc:	7c d2                	jl     140001ad0 <_pei386_runtime_relocator+0x1e0>
   140001afe:	e9 0c fe ff ff       	jmp    14000190f <_pei386_runtime_relocator+0x1f>
   140001b03:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001b08:	85 d2                	test   %edx,%edx
   140001b0a:	0f 85 f0 00 00 00    	jne    140001c00 <_pei386_runtime_relocator+0x310>
   140001b10:	8b 43 04             	mov    0x4(%rbx),%eax
   140001b13:	89 c2                	mov    %eax,%edx
   140001b15:	0b 53 08             	or     0x8(%rbx),%edx
   140001b18:	0f 85 74 fe ff ff    	jne    140001992 <_pei386_runtime_relocator+0xa2>
   140001b1e:	48 83 c3 0c          	add    $0xc,%rbx
   140001b22:	e9 5e fe ff ff       	jmp    140001985 <_pei386_runtime_relocator+0x95>
   140001b27:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   140001b2e:	00 00 
   140001b30:	83 fa 40             	cmp    $0x40,%edx
   140001b33:	0f 85 fd 00 00 00    	jne    140001c36 <_pei386_runtime_relocator+0x346>
   140001b39:	49 8b 36             	mov    (%r14),%rsi
   140001b3c:	48 29 c6             	sub    %rax,%rsi
   140001b3f:	4c 01 ce             	add    %r9,%rsi
   140001b42:	81 e1 c0 00 00 00    	and    $0xc0,%ecx
   140001b48:	75 66                	jne    140001bb0 <_pei386_runtime_relocator+0x2c0>
   140001b4a:	48 85 f6             	test   %rsi,%rsi
   140001b4d:	78 61                	js     140001bb0 <_pei386_runtime_relocator+0x2c0>
   140001b4f:	48 89 74 24 20       	mov    %rsi,0x20(%rsp)
   140001b54:	48 8d 0d 4d 27 00 00 	lea    0x274d(%rip),%rcx        # 1400042a8 <.rdata+0x108>
   140001b5b:	4d 89 f0             	mov    %r14,%r8
   140001b5e:	e8 ad fb ff ff       	call   140001710 <__report_error>
   140001b63:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001b68:	41 8b 36             	mov    (%r14),%esi
   140001b6b:	81 e1 c0 00 00 00    	and    $0xc0,%ecx
   140001b71:	85 f6                	test   %esi,%esi
   140001b73:	79 4b                	jns    140001bc0 <_pei386_runtime_relocator+0x2d0>
   140001b75:	49 bb 00 00 00 00 ff 	movabs $0xffffffff00000000,%r11
   140001b7c:	ff ff ff 
   140001b7f:	4c 09 de             	or     %r11,%rsi
   140001b82:	48 29 c6             	sub    %rax,%rsi
   140001b85:	4c 01 ce             	add    %r9,%rsi
   140001b88:	85 c9                	test   %ecx,%ecx
   140001b8a:	75 0f                	jne    140001b9b <_pei386_runtime_relocator+0x2ab>
   140001b8c:	4c 39 fe             	cmp    %r15,%rsi
   140001b8f:	7e be                	jle    140001b4f <_pei386_runtime_relocator+0x25f>
   140001b91:	b8 ff ff ff ff       	mov    $0xffffffff,%eax
   140001b96:	48 39 c6             	cmp    %rax,%rsi
   140001b99:	7f b4                	jg     140001b4f <_pei386_runtime_relocator+0x25f>
   140001b9b:	4c 89 f1             	mov    %r14,%rcx
   140001b9e:	e8 dd fb ff ff       	call   140001780 <mark_section_writable>
   140001ba3:	41 89 36             	mov    %esi,(%r14)
   140001ba6:	e9 6b fe ff ff       	jmp    140001a16 <_pei386_runtime_relocator+0x126>
   140001bab:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001bb0:	4c 89 f1             	mov    %r14,%rcx
   140001bb3:	e8 c8 fb ff ff       	call   140001780 <mark_section_writable>
   140001bb8:	49 89 36             	mov    %rsi,(%r14)
   140001bbb:	e9 56 fe ff ff       	jmp    140001a16 <_pei386_runtime_relocator+0x126>
   140001bc0:	48 29 c6             	sub    %rax,%rsi
   140001bc3:	4c 01 ce             	add    %r9,%rsi
   140001bc6:	85 c9                	test   %ecx,%ecx
   140001bc8:	74 c2                	je     140001b8c <_pei386_runtime_relocator+0x29c>
   140001bca:	eb cf                	jmp    140001b9b <_pei386_runtime_relocator+0x2ab>
   140001bcc:	0f 1f 40 00          	nopl   0x0(%rax)
   140001bd0:	48 29 c6             	sub    %rax,%rsi
   140001bd3:	4c 01 ce             	add    %r9,%rsi
   140001bd6:	85 c9                	test   %ecx,%ecx
   140001bd8:	0f 84 9c fe ff ff    	je     140001a7a <_pei386_runtime_relocator+0x18a>
   140001bde:	e9 b1 fe ff ff       	jmp    140001a94 <_pei386_runtime_relocator+0x1a4>
   140001be3:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001be8:	48 29 c6             	sub    %rax,%rsi
   140001beb:	4c 01 ce             	add    %r9,%rsi
   140001bee:	85 c9                	test   %ecx,%ecx
   140001bf0:	0f 84 fe fd ff ff    	je     1400019f4 <_pei386_runtime_relocator+0x104>
   140001bf6:	e9 10 fe ff ff       	jmp    140001a0b <_pei386_runtime_relocator+0x11b>
   140001bfb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001c00:	4c 39 eb             	cmp    %r13,%rbx
   140001c03:	0f 83 06 fd ff ff    	jae    14000190f <_pei386_runtime_relocator+0x1f>
   140001c09:	4c 8b 35 80 27 00 00 	mov    0x2780(%rip),%r14        # 140004390 <.refptr.__image_base__>
   140001c10:	8b 73 04             	mov    0x4(%rbx),%esi
   140001c13:	48 83 c3 08          	add    $0x8,%rbx
   140001c17:	44 8b 63 f8          	mov    -0x8(%rbx),%r12d
   140001c1b:	4c 01 f6             	add    %r14,%rsi
   140001c1e:	44 03 26             	add    (%rsi),%r12d
   140001c21:	48 89 f1             	mov    %rsi,%rcx
   140001c24:	e8 57 fb ff ff       	call   140001780 <mark_section_writable>
   140001c29:	4c 39 eb             	cmp    %r13,%rbx
   140001c2c:	44 89 26             	mov    %r12d,(%rsi)
   140001c2f:	72 df                	jb     140001c10 <_pei386_runtime_relocator+0x320>
   140001c31:	e9 7a fe ff ff       	jmp    140001ab0 <_pei386_runtime_relocator+0x1c0>
   140001c36:	48 8d 0d 3b 26 00 00 	lea    0x263b(%rip),%rcx        # 140004278 <.rdata+0xd8>
   140001c3d:	e8 ce fa ff ff       	call   140001710 <__report_error>
   140001c42:	48 8d 0d f7 25 00 00 	lea    0x25f7(%rip),%rcx        # 140004240 <.rdata+0xa0>
   140001c49:	e8 c2 fa ff ff       	call   140001710 <__report_error>
   140001c4e:	90                   	nop
   140001c4f:	90                   	nop

0000000140001c50 <__mingw_raise_matherr>:
   140001c50:	48 83 ec 58          	sub    $0x58,%rsp
   140001c54:	48 8b 05 45 54 00 00 	mov    0x5445(%rip),%rax        # 1400070a0 <stUserMathErr>
   140001c5b:	48 85 c0             	test   %rax,%rax
   140001c5e:	66 0f 14 d3          	unpcklpd %xmm3,%xmm2
   140001c62:	74 25                	je     140001c89 <__mingw_raise_matherr+0x39>
   140001c64:	f2 0f 10 84 24 80 00 	movsd  0x80(%rsp),%xmm0
   140001c6b:	00 00 
   140001c6d:	89 4c 24 20          	mov    %ecx,0x20(%rsp)
   140001c71:	48 8d 4c 24 20       	lea    0x20(%rsp),%rcx
   140001c76:	48 89 54 24 28       	mov    %rdx,0x28(%rsp)
   140001c7b:	0f 29 54 24 30       	movaps %xmm2,0x30(%rsp)
   140001c80:	f2 0f 11 44 24 40    	movsd  %xmm0,0x40(%rsp)
   140001c86:	ff d0                	call   *%rax
   140001c88:	90                   	nop
   140001c89:	48 83 c4 58          	add    $0x58,%rsp
   140001c8d:	c3                   	ret
   140001c8e:	66 90                	xchg   %ax,%ax

0000000140001c90 <__mingw_setusermatherr>:
   140001c90:	48 89 0d 09 54 00 00 	mov    %rcx,0x5409(%rip)        # 1400070a0 <stUserMathErr>
   140001c97:	e9 d4 08 00 00       	jmp    140002570 <__setusermatherr>
   140001c9c:	90                   	nop
   140001c9d:	90                   	nop
   140001c9e:	90                   	nop
   140001c9f:	90                   	nop

0000000140001ca0 <_gnu_exception_handler>:
   140001ca0:	53                   	push   %rbx
   140001ca1:	48 83 ec 20          	sub    $0x20,%rsp
   140001ca5:	48 8b 11             	mov    (%rcx),%rdx
   140001ca8:	8b 02                	mov    (%rdx),%eax
   140001caa:	48 89 cb             	mov    %rcx,%rbx
   140001cad:	89 c1                	mov    %eax,%ecx
   140001caf:	81 e1 ff ff ff 20    	and    $0x20ffffff,%ecx
   140001cb5:	81 f9 43 43 47 20    	cmp    $0x20474343,%ecx
   140001cbb:	0f 84 9f 00 00 00    	je     140001d60 <_gnu_exception_handler+0xc0>
   140001cc1:	3d 96 00 00 c0       	cmp    $0xc0000096,%eax
   140001cc6:	77 77                	ja     140001d3f <_gnu_exception_handler+0x9f>
   140001cc8:	3d 8b 00 00 c0       	cmp    $0xc000008b,%eax
   140001ccd:	76 21                	jbe    140001cf0 <_gnu_exception_handler+0x50>
   140001ccf:	05 73 ff ff 3f       	add    $0x3fffff73,%eax
   140001cd4:	83 f8 09             	cmp    $0x9,%eax
   140001cd7:	77 54                	ja     140001d2d <_gnu_exception_handler+0x8d>
   140001cd9:	48 8d 15 20 26 00 00 	lea    0x2620(%rip),%rdx        # 140004300 <.rdata>
   140001ce0:	48 63 04 82          	movslq (%rdx,%rax,4),%rax
   140001ce4:	48 01 d0             	add    %rdx,%rax
   140001ce7:	ff e0                	jmp    *%rax
   140001ce9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140001cf0:	3d 05 00 00 c0       	cmp    $0xc0000005,%eax
   140001cf5:	0f 84 d5 00 00 00    	je     140001dd0 <_gnu_exception_handler+0x130>
   140001cfb:	76 3b                	jbe    140001d38 <_gnu_exception_handler+0x98>
   140001cfd:	3d 08 00 00 c0       	cmp    $0xc0000008,%eax
   140001d02:	74 29                	je     140001d2d <_gnu_exception_handler+0x8d>
   140001d04:	3d 1d 00 00 c0       	cmp    $0xc000001d,%eax
   140001d09:	75 34                	jne    140001d3f <_gnu_exception_handler+0x9f>
   140001d0b:	31 d2                	xor    %edx,%edx
   140001d0d:	b9 04 00 00 00       	mov    $0x4,%ecx
   140001d12:	e8 c1 08 00 00       	call   1400025d8 <signal>
   140001d17:	48 83 f8 01          	cmp    $0x1,%rax
   140001d1b:	0f 84 d6 00 00 00    	je     140001df7 <_gnu_exception_handler+0x157>
   140001d21:	48 85 c0             	test   %rax,%rax
   140001d24:	74 19                	je     140001d3f <_gnu_exception_handler+0x9f>
   140001d26:	b9 04 00 00 00       	mov    $0x4,%ecx
   140001d2b:	ff d0                	call   *%rax
   140001d2d:	b8 ff ff ff ff       	mov    $0xffffffff,%eax
   140001d32:	48 83 c4 20          	add    $0x20,%rsp
   140001d36:	5b                   	pop    %rbx
   140001d37:	c3                   	ret
   140001d38:	3d 02 00 00 80       	cmp    $0x80000002,%eax
   140001d3d:	74 ee                	je     140001d2d <_gnu_exception_handler+0x8d>
   140001d3f:	48 8b 05 7a 53 00 00 	mov    0x537a(%rip),%rax        # 1400070c0 <__mingw_oldexcpt_handler>
   140001d46:	48 85 c0             	test   %rax,%rax
   140001d49:	74 25                	je     140001d70 <_gnu_exception_handler+0xd0>
   140001d4b:	48 89 d9             	mov    %rbx,%rcx
   140001d4e:	48 83 c4 20          	add    $0x20,%rsp
   140001d52:	5b                   	pop    %rbx
   140001d53:	48 ff e0             	rex.W jmp *%rax
   140001d56:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   140001d5d:	00 00 00 
   140001d60:	f6 42 04 01          	testb  $0x1,0x4(%rdx)
   140001d64:	0f 85 57 ff ff ff    	jne    140001cc1 <_gnu_exception_handler+0x21>
   140001d6a:	eb c1                	jmp    140001d2d <_gnu_exception_handler+0x8d>
   140001d6c:	0f 1f 40 00          	nopl   0x0(%rax)
   140001d70:	31 c0                	xor    %eax,%eax
   140001d72:	48 83 c4 20          	add    $0x20,%rsp
   140001d76:	5b                   	pop    %rbx
   140001d77:	c3                   	ret
   140001d78:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   140001d7f:	00 
   140001d80:	31 d2                	xor    %edx,%edx
   140001d82:	b9 08 00 00 00       	mov    $0x8,%ecx
   140001d87:	e8 4c 08 00 00       	call   1400025d8 <signal>
   140001d8c:	48 83 f8 01          	cmp    $0x1,%rax
   140001d90:	0f 84 89 00 00 00    	je     140001e1f <_gnu_exception_handler+0x17f>
   140001d96:	48 85 c0             	test   %rax,%rax
   140001d99:	74 a4                	je     140001d3f <_gnu_exception_handler+0x9f>
   140001d9b:	b9 08 00 00 00       	mov    $0x8,%ecx
   140001da0:	ff d0                	call   *%rax
   140001da2:	eb 89                	jmp    140001d2d <_gnu_exception_handler+0x8d>
   140001da4:	0f 1f 40 00          	nopl   0x0(%rax)
   140001da8:	31 d2                	xor    %edx,%edx
   140001daa:	b9 08 00 00 00       	mov    $0x8,%ecx
   140001daf:	e8 24 08 00 00       	call   1400025d8 <signal>
   140001db4:	48 83 f8 01          	cmp    $0x1,%rax
   140001db8:	75 dc                	jne    140001d96 <_gnu_exception_handler+0xf6>
   140001dba:	ba 01 00 00 00       	mov    $0x1,%edx
   140001dbf:	b9 08 00 00 00       	mov    $0x8,%ecx
   140001dc4:	e8 0f 08 00 00       	call   1400025d8 <signal>
   140001dc9:	e9 5f ff ff ff       	jmp    140001d2d <_gnu_exception_handler+0x8d>
   140001dce:	66 90                	xchg   %ax,%ax
   140001dd0:	31 d2                	xor    %edx,%edx
   140001dd2:	b9 0b 00 00 00       	mov    $0xb,%ecx
   140001dd7:	e8 fc 07 00 00       	call   1400025d8 <signal>
   140001ddc:	48 83 f8 01          	cmp    $0x1,%rax
   140001de0:	74 29                	je     140001e0b <_gnu_exception_handler+0x16b>
   140001de2:	48 85 c0             	test   %rax,%rax
   140001de5:	0f 84 54 ff ff ff    	je     140001d3f <_gnu_exception_handler+0x9f>
   140001deb:	b9 0b 00 00 00       	mov    $0xb,%ecx
   140001df0:	ff d0                	call   *%rax
   140001df2:	e9 36 ff ff ff       	jmp    140001d2d <_gnu_exception_handler+0x8d>
   140001df7:	ba 01 00 00 00       	mov    $0x1,%edx
   140001dfc:	b9 04 00 00 00       	mov    $0x4,%ecx
   140001e01:	e8 d2 07 00 00       	call   1400025d8 <signal>
   140001e06:	e9 22 ff ff ff       	jmp    140001d2d <_gnu_exception_handler+0x8d>
   140001e0b:	ba 01 00 00 00       	mov    $0x1,%edx
   140001e10:	b9 0b 00 00 00       	mov    $0xb,%ecx
   140001e15:	e8 be 07 00 00       	call   1400025d8 <signal>
   140001e1a:	e9 0e ff ff ff       	jmp    140001d2d <_gnu_exception_handler+0x8d>
   140001e1f:	ba 01 00 00 00       	mov    $0x1,%edx
   140001e24:	b9 08 00 00 00       	mov    $0x8,%ecx
   140001e29:	e8 aa 07 00 00       	call   1400025d8 <signal>
   140001e2e:	e8 cd f8 ff ff       	call   140001700 <_fpreset>
   140001e33:	e9 f5 fe ff ff       	jmp    140001d2d <_gnu_exception_handler+0x8d>
   140001e38:	90                   	nop
   140001e39:	90                   	nop
   140001e3a:	90                   	nop
   140001e3b:	90                   	nop
   140001e3c:	90                   	nop
   140001e3d:	90                   	nop
   140001e3e:	90                   	nop
   140001e3f:	90                   	nop

0000000140001e40 <__mingwthr_run_key_dtors.part.0>:
   140001e40:	41 54                	push   %r12
   140001e42:	55                   	push   %rbp
   140001e43:	57                   	push   %rdi
   140001e44:	56                   	push   %rsi
   140001e45:	53                   	push   %rbx
   140001e46:	48 83 ec 20          	sub    $0x20,%rsp
   140001e4a:	4c 8d 25 af 52 00 00 	lea    0x52af(%rip),%r12        # 140007100 <__mingwthr_cs>
   140001e51:	4c 89 e1             	mov    %r12,%rcx
   140001e54:	ff 15 0a 63 00 00    	call   *0x630a(%rip)        # 140008164 <__imp_EnterCriticalSection>
   140001e5a:	48 8b 1d 7f 52 00 00 	mov    0x527f(%rip),%rbx        # 1400070e0 <key_dtor_list>
   140001e61:	48 85 db             	test   %rbx,%rbx
   140001e64:	74 36                	je     140001e9c <__mingwthr_run_key_dtors.part.0+0x5c>
   140001e66:	48 8b 2d 27 63 00 00 	mov    0x6327(%rip),%rbp        # 140008194 <__imp_TlsGetValue>
   140001e6d:	48 8b 3d f8 62 00 00 	mov    0x62f8(%rip),%rdi        # 14000816c <__imp_GetLastError>
   140001e74:	0f 1f 40 00          	nopl   0x0(%rax)
   140001e78:	8b 0b                	mov    (%rbx),%ecx
   140001e7a:	ff d5                	call   *%rbp
   140001e7c:	48 89 c6             	mov    %rax,%rsi
   140001e7f:	ff d7                	call   *%rdi
   140001e81:	85 c0                	test   %eax,%eax
   140001e83:	75 0e                	jne    140001e93 <__mingwthr_run_key_dtors.part.0+0x53>
   140001e85:	48 85 f6             	test   %rsi,%rsi
   140001e88:	74 09                	je     140001e93 <__mingwthr_run_key_dtors.part.0+0x53>
   140001e8a:	48 8b 43 08          	mov    0x8(%rbx),%rax
   140001e8e:	48 89 f1             	mov    %rsi,%rcx
   140001e91:	ff d0                	call   *%rax
   140001e93:	48 8b 5b 10          	mov    0x10(%rbx),%rbx
   140001e97:	48 85 db             	test   %rbx,%rbx
   140001e9a:	75 dc                	jne    140001e78 <__mingwthr_run_key_dtors.part.0+0x38>
   140001e9c:	4c 89 e1             	mov    %r12,%rcx
   140001e9f:	48 83 c4 20          	add    $0x20,%rsp
   140001ea3:	5b                   	pop    %rbx
   140001ea4:	5e                   	pop    %rsi
   140001ea5:	5f                   	pop    %rdi
   140001ea6:	5d                   	pop    %rbp
   140001ea7:	41 5c                	pop    %r12
   140001ea9:	48 ff 25 cc 62 00 00 	rex.W jmp *0x62cc(%rip)        # 14000817c <__imp_LeaveCriticalSection>

0000000140001eb0 <___w64_mingwthr_add_key_dtor>:
   140001eb0:	57                   	push   %rdi
   140001eb1:	56                   	push   %rsi
   140001eb2:	53                   	push   %rbx
   140001eb3:	48 83 ec 20          	sub    $0x20,%rsp
   140001eb7:	8b 05 2b 52 00 00    	mov    0x522b(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   140001ebd:	85 c0                	test   %eax,%eax
   140001ebf:	89 cf                	mov    %ecx,%edi
   140001ec1:	48 89 d6             	mov    %rdx,%rsi
   140001ec4:	75 0a                	jne    140001ed0 <___w64_mingwthr_add_key_dtor+0x20>
   140001ec6:	31 c0                	xor    %eax,%eax
   140001ec8:	48 83 c4 20          	add    $0x20,%rsp
   140001ecc:	5b                   	pop    %rbx
   140001ecd:	5e                   	pop    %rsi
   140001ece:	5f                   	pop    %rdi
   140001ecf:	c3                   	ret
   140001ed0:	ba 18 00 00 00       	mov    $0x18,%edx
   140001ed5:	b9 01 00 00 00       	mov    $0x1,%ecx
   140001eda:	e8 c1 06 00 00       	call   1400025a0 <calloc>
   140001edf:	48 85 c0             	test   %rax,%rax
   140001ee2:	48 89 c3             	mov    %rax,%rbx
   140001ee5:	74 33                	je     140001f1a <___w64_mingwthr_add_key_dtor+0x6a>
   140001ee7:	48 89 70 08          	mov    %rsi,0x8(%rax)
   140001eeb:	48 8d 35 0e 52 00 00 	lea    0x520e(%rip),%rsi        # 140007100 <__mingwthr_cs>
   140001ef2:	89 38                	mov    %edi,(%rax)
   140001ef4:	48 89 f1             	mov    %rsi,%rcx
   140001ef7:	ff 15 67 62 00 00    	call   *0x6267(%rip)        # 140008164 <__imp_EnterCriticalSection>
   140001efd:	48 8b 05 dc 51 00 00 	mov    0x51dc(%rip),%rax        # 1400070e0 <key_dtor_list>
   140001f04:	48 89 f1             	mov    %rsi,%rcx
   140001f07:	48 89 1d d2 51 00 00 	mov    %rbx,0x51d2(%rip)        # 1400070e0 <key_dtor_list>
   140001f0e:	48 89 43 10          	mov    %rax,0x10(%rbx)
   140001f12:	ff 15 64 62 00 00    	call   *0x6264(%rip)        # 14000817c <__imp_LeaveCriticalSection>
   140001f18:	eb ac                	jmp    140001ec6 <___w64_mingwthr_add_key_dtor+0x16>
   140001f1a:	83 c8 ff             	or     $0xffffffff,%eax
   140001f1d:	eb a9                	jmp    140001ec8 <___w64_mingwthr_add_key_dtor+0x18>
   140001f1f:	90                   	nop

0000000140001f20 <___w64_mingwthr_remove_key_dtor>:
   140001f20:	56                   	push   %rsi
   140001f21:	53                   	push   %rbx
   140001f22:	48 83 ec 28          	sub    $0x28,%rsp
   140001f26:	8b 05 bc 51 00 00    	mov    0x51bc(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   140001f2c:	85 c0                	test   %eax,%eax
   140001f2e:	89 cb                	mov    %ecx,%ebx
   140001f30:	75 0e                	jne    140001f40 <___w64_mingwthr_remove_key_dtor+0x20>
   140001f32:	31 c0                	xor    %eax,%eax
   140001f34:	48 83 c4 28          	add    $0x28,%rsp
   140001f38:	5b                   	pop    %rbx
   140001f39:	5e                   	pop    %rsi
   140001f3a:	c3                   	ret
   140001f3b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140001f40:	48 8d 35 b9 51 00 00 	lea    0x51b9(%rip),%rsi        # 140007100 <__mingwthr_cs>
   140001f47:	48 89 f1             	mov    %rsi,%rcx
   140001f4a:	ff 15 14 62 00 00    	call   *0x6214(%rip)        # 140008164 <__imp_EnterCriticalSection>
   140001f50:	48 8b 0d 89 51 00 00 	mov    0x5189(%rip),%rcx        # 1400070e0 <key_dtor_list>
   140001f57:	48 85 c9             	test   %rcx,%rcx
   140001f5a:	74 27                	je     140001f83 <___w64_mingwthr_remove_key_dtor+0x63>
   140001f5c:	31 d2                	xor    %edx,%edx
   140001f5e:	eb 0b                	jmp    140001f6b <___w64_mingwthr_remove_key_dtor+0x4b>
   140001f60:	48 85 c0             	test   %rax,%rax
   140001f63:	48 89 ca             	mov    %rcx,%rdx
   140001f66:	74 1b                	je     140001f83 <___w64_mingwthr_remove_key_dtor+0x63>
   140001f68:	48 89 c1             	mov    %rax,%rcx
   140001f6b:	8b 01                	mov    (%rcx),%eax
   140001f6d:	39 d8                	cmp    %ebx,%eax
   140001f6f:	48 8b 41 10          	mov    0x10(%rcx),%rax
   140001f73:	75 eb                	jne    140001f60 <___w64_mingwthr_remove_key_dtor+0x40>
   140001f75:	48 85 d2             	test   %rdx,%rdx
   140001f78:	74 1e                	je     140001f98 <___w64_mingwthr_remove_key_dtor+0x78>
   140001f7a:	48 89 42 10          	mov    %rax,0x10(%rdx)
   140001f7e:	e8 35 06 00 00       	call   1400025b8 <free>
   140001f83:	48 89 f1             	mov    %rsi,%rcx
   140001f86:	ff 15 f0 61 00 00    	call   *0x61f0(%rip)        # 14000817c <__imp_LeaveCriticalSection>
   140001f8c:	31 c0                	xor    %eax,%eax
   140001f8e:	48 83 c4 28          	add    $0x28,%rsp
   140001f92:	5b                   	pop    %rbx
   140001f93:	5e                   	pop    %rsi
   140001f94:	c3                   	ret
   140001f95:	0f 1f 00             	nopl   (%rax)
   140001f98:	48 89 05 41 51 00 00 	mov    %rax,0x5141(%rip)        # 1400070e0 <key_dtor_list>
   140001f9f:	eb dd                	jmp    140001f7e <___w64_mingwthr_remove_key_dtor+0x5e>
   140001fa1:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   140001fa8:	00 00 00 00 
   140001fac:	0f 1f 40 00          	nopl   0x0(%rax)

0000000140001fb0 <__mingw_TLScallback>:
   140001fb0:	53                   	push   %rbx
   140001fb1:	48 83 ec 20          	sub    $0x20,%rsp
   140001fb5:	83 fa 02             	cmp    $0x2,%edx
   140001fb8:	0f 84 b2 00 00 00    	je     140002070 <__mingw_TLScallback+0xc0>
   140001fbe:	77 30                	ja     140001ff0 <__mingw_TLScallback+0x40>
   140001fc0:	85 d2                	test   %edx,%edx
   140001fc2:	74 4c                	je     140002010 <__mingw_TLScallback+0x60>
   140001fc4:	8b 05 1e 51 00 00    	mov    0x511e(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   140001fca:	85 c0                	test   %eax,%eax
   140001fcc:	0f 84 be 00 00 00    	je     140002090 <__mingw_TLScallback+0xe0>
   140001fd2:	c7 05 0c 51 00 00 01 	movl   $0x1,0x510c(%rip)        # 1400070e8 <__mingwthr_cs_init>
   140001fd9:	00 00 00 
   140001fdc:	b8 01 00 00 00       	mov    $0x1,%eax
   140001fe1:	48 83 c4 20          	add    $0x20,%rsp
   140001fe5:	5b                   	pop    %rbx
   140001fe6:	c3                   	ret
   140001fe7:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   140001fee:	00 00 
   140001ff0:	83 fa 03             	cmp    $0x3,%edx
   140001ff3:	75 e7                	jne    140001fdc <__mingw_TLScallback+0x2c>
   140001ff5:	8b 05 ed 50 00 00    	mov    0x50ed(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   140001ffb:	85 c0                	test   %eax,%eax
   140001ffd:	74 dd                	je     140001fdc <__mingw_TLScallback+0x2c>
   140001fff:	e8 3c fe ff ff       	call   140001e40 <__mingwthr_run_key_dtors.part.0>
   140002004:	eb d6                	jmp    140001fdc <__mingw_TLScallback+0x2c>
   140002006:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000200d:	00 00 00 
   140002010:	8b 05 d2 50 00 00    	mov    0x50d2(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   140002016:	85 c0                	test   %eax,%eax
   140002018:	75 66                	jne    140002080 <__mingw_TLScallback+0xd0>
   14000201a:	8b 05 c8 50 00 00    	mov    0x50c8(%rip),%eax        # 1400070e8 <__mingwthr_cs_init>
   140002020:	83 f8 01             	cmp    $0x1,%eax
   140002023:	75 b7                	jne    140001fdc <__mingw_TLScallback+0x2c>
   140002025:	48 8b 1d b4 50 00 00 	mov    0x50b4(%rip),%rbx        # 1400070e0 <key_dtor_list>
   14000202c:	48 85 db             	test   %rbx,%rbx
   14000202f:	74 18                	je     140002049 <__mingw_TLScallback+0x99>
   140002031:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140002038:	48 89 d9             	mov    %rbx,%rcx
   14000203b:	48 8b 5b 10          	mov    0x10(%rbx),%rbx
   14000203f:	e8 74 05 00 00       	call   1400025b8 <free>
   140002044:	48 85 db             	test   %rbx,%rbx
   140002047:	75 ef                	jne    140002038 <__mingw_TLScallback+0x88>
   140002049:	48 8d 0d b0 50 00 00 	lea    0x50b0(%rip),%rcx        # 140007100 <__mingwthr_cs>
   140002050:	48 c7 05 85 50 00 00 	movq   $0x0,0x5085(%rip)        # 1400070e0 <key_dtor_list>
   140002057:	00 00 00 00 
   14000205b:	c7 05 83 50 00 00 00 	movl   $0x0,0x5083(%rip)        # 1400070e8 <__mingwthr_cs_init>
   140002062:	00 00 00 
   140002065:	ff 15 f1 60 00 00    	call   *0x60f1(%rip)        # 14000815c <__IAT_start__>
   14000206b:	e9 6c ff ff ff       	jmp    140001fdc <__mingw_TLScallback+0x2c>
   140002070:	e8 8b f6 ff ff       	call   140001700 <_fpreset>
   140002075:	b8 01 00 00 00       	mov    $0x1,%eax
   14000207a:	48 83 c4 20          	add    $0x20,%rsp
   14000207e:	5b                   	pop    %rbx
   14000207f:	c3                   	ret
   140002080:	e8 bb fd ff ff       	call   140001e40 <__mingwthr_run_key_dtors.part.0>
   140002085:	eb 93                	jmp    14000201a <__mingw_TLScallback+0x6a>
   140002087:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   14000208e:	00 00 
   140002090:	48 8d 0d 69 50 00 00 	lea    0x5069(%rip),%rcx        # 140007100 <__mingwthr_cs>
   140002097:	ff 15 d7 60 00 00    	call   *0x60d7(%rip)        # 140008174 <__imp_InitializeCriticalSection>
   14000209d:	e9 30 ff ff ff       	jmp    140001fd2 <__mingw_TLScallback+0x22>
   1400020a2:	90                   	nop
   1400020a3:	90                   	nop
   1400020a4:	90                   	nop
   1400020a5:	90                   	nop
   1400020a6:	90                   	nop
   1400020a7:	90                   	nop
   1400020a8:	90                   	nop
   1400020a9:	90                   	nop
   1400020aa:	90                   	nop
   1400020ab:	90                   	nop
   1400020ac:	90                   	nop
   1400020ad:	90                   	nop
   1400020ae:	90                   	nop
   1400020af:	90                   	nop

00000001400020b0 <_ValidateImageBase>:
   1400020b0:	31 c0                	xor    %eax,%eax
   1400020b2:	66 81 39 4d 5a       	cmpw   $0x5a4d,(%rcx)
   1400020b7:	75 0f                	jne    1400020c8 <_ValidateImageBase+0x18>
   1400020b9:	48 63 51 3c          	movslq 0x3c(%rcx),%rdx
   1400020bd:	48 01 d1             	add    %rdx,%rcx
   1400020c0:	81 39 50 45 00 00    	cmpl   $0x4550,(%rcx)
   1400020c6:	74 08                	je     1400020d0 <_ValidateImageBase+0x20>
   1400020c8:	c3                   	ret
   1400020c9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400020d0:	31 c0                	xor    %eax,%eax
   1400020d2:	66 81 79 18 0b 02    	cmpw   $0x20b,0x18(%rcx)
   1400020d8:	0f 94 c0             	sete   %al
   1400020db:	c3                   	ret
   1400020dc:	0f 1f 40 00          	nopl   0x0(%rax)

00000001400020e0 <_FindPESection>:
   1400020e0:	48 63 41 3c          	movslq 0x3c(%rcx),%rax
   1400020e4:	48 01 c1             	add    %rax,%rcx
   1400020e7:	44 0f b7 41 06       	movzwl 0x6(%rcx),%r8d
   1400020ec:	0f b7 41 14          	movzwl 0x14(%rcx),%eax
   1400020f0:	66 45 85 c0          	test   %r8w,%r8w
   1400020f4:	48 8d 44 01 18       	lea    0x18(%rcx,%rax,1),%rax
   1400020f9:	74 32                	je     14000212d <_FindPESection+0x4d>
   1400020fb:	41 8d 48 ff          	lea    -0x1(%r8),%ecx
   1400020ff:	48 8d 0c 89          	lea    (%rcx,%rcx,4),%rcx
   140002103:	4c 8d 4c c8 28       	lea    0x28(%rax,%rcx,8),%r9
   140002108:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   14000210f:	00 
   140002110:	44 8b 40 0c          	mov    0xc(%rax),%r8d
   140002114:	4c 39 c2             	cmp    %r8,%rdx
   140002117:	4c 89 c1             	mov    %r8,%rcx
   14000211a:	72 08                	jb     140002124 <_FindPESection+0x44>
   14000211c:	03 48 08             	add    0x8(%rax),%ecx
   14000211f:	48 39 ca             	cmp    %rcx,%rdx
   140002122:	72 0b                	jb     14000212f <_FindPESection+0x4f>
   140002124:	48 83 c0 28          	add    $0x28,%rax
   140002128:	4c 39 c8             	cmp    %r9,%rax
   14000212b:	75 e3                	jne    140002110 <_FindPESection+0x30>
   14000212d:	31 c0                	xor    %eax,%eax
   14000212f:	c3                   	ret

0000000140002130 <_FindPESectionByName>:
   140002130:	57                   	push   %rdi
   140002131:	56                   	push   %rsi
   140002132:	53                   	push   %rbx
   140002133:	48 83 ec 20          	sub    $0x20,%rsp
   140002137:	48 89 ce             	mov    %rcx,%rsi
   14000213a:	e8 a1 04 00 00       	call   1400025e0 <strlen>
   14000213f:	48 83 f8 08          	cmp    $0x8,%rax
   140002143:	77 7b                	ja     1400021c0 <_FindPESectionByName+0x90>
   140002145:	48 8b 15 44 22 00 00 	mov    0x2244(%rip),%rdx        # 140004390 <.refptr.__image_base__>
   14000214c:	31 db                	xor    %ebx,%ebx
   14000214e:	66 81 3a 4d 5a       	cmpw   $0x5a4d,(%rdx)
   140002153:	75 59                	jne    1400021ae <_FindPESectionByName+0x7e>
   140002155:	48 63 42 3c          	movslq 0x3c(%rdx),%rax
   140002159:	48 01 d0             	add    %rdx,%rax
   14000215c:	81 38 50 45 00 00    	cmpl   $0x4550,(%rax)
   140002162:	75 4a                	jne    1400021ae <_FindPESectionByName+0x7e>
   140002164:	66 81 78 18 0b 02    	cmpw   $0x20b,0x18(%rax)
   14000216a:	75 42                	jne    1400021ae <_FindPESectionByName+0x7e>
   14000216c:	0f b7 50 14          	movzwl 0x14(%rax),%edx
   140002170:	48 8d 5c 10 18       	lea    0x18(%rax,%rdx,1),%rbx
   140002175:	0f b7 50 06          	movzwl 0x6(%rax),%edx
   140002179:	66 85 d2             	test   %dx,%dx
   14000217c:	74 42                	je     1400021c0 <_FindPESectionByName+0x90>
   14000217e:	8d 42 ff             	lea    -0x1(%rdx),%eax
   140002181:	48 8d 04 80          	lea    (%rax,%rax,4),%rax
   140002185:	48 8d 7c c3 28       	lea    0x28(%rbx,%rax,8),%rdi
   14000218a:	eb 0d                	jmp    140002199 <_FindPESectionByName+0x69>
   14000218c:	0f 1f 40 00          	nopl   0x0(%rax)
   140002190:	48 83 c3 28          	add    $0x28,%rbx
   140002194:	48 39 fb             	cmp    %rdi,%rbx
   140002197:	74 27                	je     1400021c0 <_FindPESectionByName+0x90>
   140002199:	41 b8 08 00 00 00    	mov    $0x8,%r8d
   14000219f:	48 89 f2             	mov    %rsi,%rdx
   1400021a2:	48 89 d9             	mov    %rbx,%rcx
   1400021a5:	e8 3e 04 00 00       	call   1400025e8 <strncmp>
   1400021aa:	85 c0                	test   %eax,%eax
   1400021ac:	75 e2                	jne    140002190 <_FindPESectionByName+0x60>
   1400021ae:	48 89 d8             	mov    %rbx,%rax
   1400021b1:	48 83 c4 20          	add    $0x20,%rsp
   1400021b5:	5b                   	pop    %rbx
   1400021b6:	5e                   	pop    %rsi
   1400021b7:	5f                   	pop    %rdi
   1400021b8:	c3                   	ret
   1400021b9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400021c0:	31 db                	xor    %ebx,%ebx
   1400021c2:	48 89 d8             	mov    %rbx,%rax
   1400021c5:	48 83 c4 20          	add    $0x20,%rsp
   1400021c9:	5b                   	pop    %rbx
   1400021ca:	5e                   	pop    %rsi
   1400021cb:	5f                   	pop    %rdi
   1400021cc:	c3                   	ret
   1400021cd:	0f 1f 00             	nopl   (%rax)

00000001400021d0 <__mingw_GetSectionForAddress>:
   1400021d0:	48 8b 15 b9 21 00 00 	mov    0x21b9(%rip),%rdx        # 140004390 <.refptr.__image_base__>
   1400021d7:	31 c0                	xor    %eax,%eax
   1400021d9:	66 81 3a 4d 5a       	cmpw   $0x5a4d,(%rdx)
   1400021de:	75 10                	jne    1400021f0 <__mingw_GetSectionForAddress+0x20>
   1400021e0:	4c 63 42 3c          	movslq 0x3c(%rdx),%r8
   1400021e4:	49 01 d0             	add    %rdx,%r8
   1400021e7:	41 81 38 50 45 00 00 	cmpl   $0x4550,(%r8)
   1400021ee:	74 08                	je     1400021f8 <__mingw_GetSectionForAddress+0x28>
   1400021f0:	c3                   	ret
   1400021f1:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400021f8:	66 41 81 78 18 0b 02 	cmpw   $0x20b,0x18(%r8)
   1400021ff:	75 ef                	jne    1400021f0 <__mingw_GetSectionForAddress+0x20>
   140002201:	41 0f b7 40 14       	movzwl 0x14(%r8),%eax
   140002206:	48 29 d1             	sub    %rdx,%rcx
   140002209:	49 8d 44 00 18       	lea    0x18(%r8,%rax,1),%rax
   14000220e:	45 0f b7 40 06       	movzwl 0x6(%r8),%r8d
   140002213:	66 45 85 c0          	test   %r8w,%r8w
   140002217:	74 34                	je     14000224d <__mingw_GetSectionForAddress+0x7d>
   140002219:	41 8d 50 ff          	lea    -0x1(%r8),%edx
   14000221d:	48 8d 14 92          	lea    (%rdx,%rdx,4),%rdx
   140002221:	4c 8d 4c d0 28       	lea    0x28(%rax,%rdx,8),%r9
   140002226:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000222d:	00 00 00 
   140002230:	44 8b 40 0c          	mov    0xc(%rax),%r8d
   140002234:	4c 39 c1             	cmp    %r8,%rcx
   140002237:	4c 89 c2             	mov    %r8,%rdx
   14000223a:	72 08                	jb     140002244 <__mingw_GetSectionForAddress+0x74>
   14000223c:	03 50 08             	add    0x8(%rax),%edx
   14000223f:	48 39 d1             	cmp    %rdx,%rcx
   140002242:	72 ac                	jb     1400021f0 <__mingw_GetSectionForAddress+0x20>
   140002244:	48 83 c0 28          	add    $0x28,%rax
   140002248:	4c 39 c8             	cmp    %r9,%rax
   14000224b:	75 e3                	jne    140002230 <__mingw_GetSectionForAddress+0x60>
   14000224d:	31 c0                	xor    %eax,%eax
   14000224f:	c3                   	ret

0000000140002250 <__mingw_GetSectionCount>:
   140002250:	48 8b 05 39 21 00 00 	mov    0x2139(%rip),%rax        # 140004390 <.refptr.__image_base__>
   140002257:	31 c9                	xor    %ecx,%ecx
   140002259:	66 81 38 4d 5a       	cmpw   $0x5a4d,(%rax)
   14000225e:	75 0f                	jne    14000226f <__mingw_GetSectionCount+0x1f>
   140002260:	48 63 50 3c          	movslq 0x3c(%rax),%rdx
   140002264:	48 01 d0             	add    %rdx,%rax
   140002267:	81 38 50 45 00 00    	cmpl   $0x4550,(%rax)
   14000226d:	74 09                	je     140002278 <__mingw_GetSectionCount+0x28>
   14000226f:	89 c8                	mov    %ecx,%eax
   140002271:	c3                   	ret
   140002272:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
   140002278:	66 81 78 18 0b 02    	cmpw   $0x20b,0x18(%rax)
   14000227e:	75 ef                	jne    14000226f <__mingw_GetSectionCount+0x1f>
   140002280:	0f b7 48 06          	movzwl 0x6(%rax),%ecx
   140002284:	89 c8                	mov    %ecx,%eax
   140002286:	c3                   	ret
   140002287:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   14000228e:	00 00 

0000000140002290 <_FindPESectionExec>:
   140002290:	4c 8b 05 f9 20 00 00 	mov    0x20f9(%rip),%r8        # 140004390 <.refptr.__image_base__>
   140002297:	31 c0                	xor    %eax,%eax
   140002299:	66 41 81 38 4d 5a    	cmpw   $0x5a4d,(%r8)
   14000229f:	75 0f                	jne    1400022b0 <_FindPESectionExec+0x20>
   1400022a1:	49 63 50 3c          	movslq 0x3c(%r8),%rdx
   1400022a5:	4c 01 c2             	add    %r8,%rdx
   1400022a8:	81 3a 50 45 00 00    	cmpl   $0x4550,(%rdx)
   1400022ae:	74 08                	je     1400022b8 <_FindPESectionExec+0x28>
   1400022b0:	c3                   	ret
   1400022b1:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400022b8:	66 81 7a 18 0b 02    	cmpw   $0x20b,0x18(%rdx)
   1400022be:	75 f0                	jne    1400022b0 <_FindPESectionExec+0x20>
   1400022c0:	44 0f b7 42 06       	movzwl 0x6(%rdx),%r8d
   1400022c5:	0f b7 42 14          	movzwl 0x14(%rdx),%eax
   1400022c9:	66 45 85 c0          	test   %r8w,%r8w
   1400022cd:	48 8d 44 02 18       	lea    0x18(%rdx,%rax,1),%rax
   1400022d2:	74 2c                	je     140002300 <_FindPESectionExec+0x70>
   1400022d4:	41 8d 50 ff          	lea    -0x1(%r8),%edx
   1400022d8:	48 8d 14 92          	lea    (%rdx,%rdx,4),%rdx
   1400022dc:	48 8d 54 d0 28       	lea    0x28(%rax,%rdx,8),%rdx
   1400022e1:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   1400022e8:	f6 40 27 20          	testb  $0x20,0x27(%rax)
   1400022ec:	74 09                	je     1400022f7 <_FindPESectionExec+0x67>
   1400022ee:	48 85 c9             	test   %rcx,%rcx
   1400022f1:	74 bd                	je     1400022b0 <_FindPESectionExec+0x20>
   1400022f3:	48 83 e9 01          	sub    $0x1,%rcx
   1400022f7:	48 83 c0 28          	add    $0x28,%rax
   1400022fb:	48 39 d0             	cmp    %rdx,%rax
   1400022fe:	75 e8                	jne    1400022e8 <_FindPESectionExec+0x58>
   140002300:	31 c0                	xor    %eax,%eax
   140002302:	c3                   	ret
   140002303:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
   14000230a:	00 00 00 00 
   14000230e:	66 90                	xchg   %ax,%ax

0000000140002310 <_GetPEImageBase>:
   140002310:	48 8b 05 79 20 00 00 	mov    0x2079(%rip),%rax        # 140004390 <.refptr.__image_base__>
   140002317:	31 d2                	xor    %edx,%edx
   140002319:	66 81 38 4d 5a       	cmpw   $0x5a4d,(%rax)
   14000231e:	75 0f                	jne    14000232f <_GetPEImageBase+0x1f>
   140002320:	48 63 48 3c          	movslq 0x3c(%rax),%rcx
   140002324:	48 01 c1             	add    %rax,%rcx
   140002327:	81 39 50 45 00 00    	cmpl   $0x4550,(%rcx)
   14000232d:	74 09                	je     140002338 <_GetPEImageBase+0x28>
   14000232f:	48 89 d0             	mov    %rdx,%rax
   140002332:	c3                   	ret
   140002333:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
   140002338:	66 81 79 18 0b 02    	cmpw   $0x20b,0x18(%rcx)
   14000233e:	48 0f 44 d0          	cmove  %rax,%rdx
   140002342:	48 89 d0             	mov    %rdx,%rax
   140002345:	c3                   	ret
   140002346:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000234d:	00 00 00 

0000000140002350 <_IsNonwritableInCurrentImage>:
   140002350:	48 8b 15 39 20 00 00 	mov    0x2039(%rip),%rdx        # 140004390 <.refptr.__image_base__>
   140002357:	31 c0                	xor    %eax,%eax
   140002359:	66 81 3a 4d 5a       	cmpw   $0x5a4d,(%rdx)
   14000235e:	75 10                	jne    140002370 <_IsNonwritableInCurrentImage+0x20>
   140002360:	4c 63 42 3c          	movslq 0x3c(%rdx),%r8
   140002364:	49 01 d0             	add    %rdx,%r8
   140002367:	41 81 38 50 45 00 00 	cmpl   $0x4550,(%r8)
   14000236e:	74 08                	je     140002378 <_IsNonwritableInCurrentImage+0x28>
   140002370:	c3                   	ret
   140002371:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
   140002378:	66 41 81 78 18 0b 02 	cmpw   $0x20b,0x18(%r8)
   14000237f:	75 ef                	jne    140002370 <_IsNonwritableInCurrentImage+0x20>
   140002381:	45 0f b7 48 06       	movzwl 0x6(%r8),%r9d
   140002386:	48 29 d1             	sub    %rdx,%rcx
   140002389:	41 0f b7 50 14       	movzwl 0x14(%r8),%edx
   14000238e:	66 45 85 c9          	test   %r9w,%r9w
   140002392:	49 8d 54 10 18       	lea    0x18(%r8,%rdx,1),%rdx
   140002397:	74 d7                	je     140002370 <_IsNonwritableInCurrentImage+0x20>
   140002399:	41 8d 41 ff          	lea    -0x1(%r9),%eax
   14000239d:	48 8d 04 80          	lea    (%rax,%rax,4),%rax
   1400023a1:	4c 8d 4c c2 28       	lea    0x28(%rdx,%rax,8),%r9
   1400023a6:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   1400023ad:	00 00 00 
   1400023b0:	44 8b 42 0c          	mov    0xc(%rdx),%r8d
   1400023b4:	4c 39 c1             	cmp    %r8,%rcx
   1400023b7:	4c 89 c0             	mov    %r8,%rax
   1400023ba:	72 08                	jb     1400023c4 <_IsNonwritableInCurrentImage+0x74>
   1400023bc:	03 42 08             	add    0x8(%rdx),%eax
   1400023bf:	48 39 c1             	cmp    %rax,%rcx
   1400023c2:	72 0c                	jb     1400023d0 <_IsNonwritableInCurrentImage+0x80>
   1400023c4:	48 83 c2 28          	add    $0x28,%rdx
   1400023c8:	49 39 d1             	cmp    %rdx,%r9
   1400023cb:	75 e3                	jne    1400023b0 <_IsNonwritableInCurrentImage+0x60>
   1400023cd:	31 c0                	xor    %eax,%eax
   1400023cf:	c3                   	ret
   1400023d0:	8b 42 24             	mov    0x24(%rdx),%eax
   1400023d3:	f7 d0                	not    %eax
   1400023d5:	c1 e8 1f             	shr    $0x1f,%eax
   1400023d8:	c3                   	ret
   1400023d9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

00000001400023e0 <__mingw_enum_import_library_names>:
   1400023e0:	4c 8b 1d a9 1f 00 00 	mov    0x1fa9(%rip),%r11        # 140004390 <.refptr.__image_base__>
   1400023e7:	45 31 c9             	xor    %r9d,%r9d
   1400023ea:	66 41 81 3b 4d 5a    	cmpw   $0x5a4d,(%r11)
   1400023f0:	75 10                	jne    140002402 <__mingw_enum_import_library_names+0x22>
   1400023f2:	4d 63 43 3c          	movslq 0x3c(%r11),%r8
   1400023f6:	4d 01 d8             	add    %r11,%r8
   1400023f9:	41 81 38 50 45 00 00 	cmpl   $0x4550,(%r8)
   140002400:	74 0e                	je     140002410 <__mingw_enum_import_library_names+0x30>
   140002402:	4c 89 c8             	mov    %r9,%rax
   140002405:	c3                   	ret
   140002406:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000240d:	00 00 00 
   140002410:	66 41 81 78 18 0b 02 	cmpw   $0x20b,0x18(%r8)
   140002417:	75 e9                	jne    140002402 <__mingw_enum_import_library_names+0x22>
   140002419:	41 8b 80 90 00 00 00 	mov    0x90(%r8),%eax
   140002420:	85 c0                	test   %eax,%eax
   140002422:	74 de                	je     140002402 <__mingw_enum_import_library_names+0x22>
   140002424:	45 0f b7 50 06       	movzwl 0x6(%r8),%r10d
   140002429:	41 0f b7 50 14       	movzwl 0x14(%r8),%edx
   14000242e:	66 45 85 d2          	test   %r10w,%r10w
   140002432:	49 8d 54 10 18       	lea    0x18(%r8,%rdx,1),%rdx
   140002437:	74 c9                	je     140002402 <__mingw_enum_import_library_names+0x22>
   140002439:	45 8d 42 ff          	lea    -0x1(%r10),%r8d
   14000243d:	4f 8d 04 80          	lea    (%r8,%r8,4),%r8
   140002441:	4e 8d 54 c2 28       	lea    0x28(%rdx,%r8,8),%r10
   140002446:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
   14000244d:	00 00 00 
   140002450:	44 8b 4a 0c          	mov    0xc(%rdx),%r9d
   140002454:	4c 39 c8             	cmp    %r9,%rax
   140002457:	4d 89 c8             	mov    %r9,%r8
   14000245a:	72 09                	jb     140002465 <__mingw_enum_import_library_names+0x85>
   14000245c:	44 03 42 08          	add    0x8(%rdx),%r8d
   140002460:	4c 39 c0             	cmp    %r8,%rax
   140002463:	72 13                	jb     140002478 <__mingw_enum_import_library_names+0x98>
   140002465:	48 83 c2 28          	add    $0x28,%rdx
   140002469:	4c 39 d2             	cmp    %r10,%rdx
   14000246c:	75 e2                	jne    140002450 <__mingw_enum_import_library_names+0x70>
   14000246e:	45 31 c9             	xor    %r9d,%r9d
   140002471:	4c 89 c8             	mov    %r9,%rax
   140002474:	c3                   	ret
   140002475:	0f 1f 00             	nopl   (%rax)
   140002478:	4c 01 d8             	add    %r11,%rax
   14000247b:	eb 0a                	jmp    140002487 <__mingw_enum_import_library_names+0xa7>
   14000247d:	0f 1f 00             	nopl   (%rax)
   140002480:	83 e9 01             	sub    $0x1,%ecx
   140002483:	48 83 c0 14          	add    $0x14,%rax
   140002487:	44 8b 40 04          	mov    0x4(%rax),%r8d
   14000248b:	45 85 c0             	test   %r8d,%r8d
   14000248e:	75 07                	jne    140002497 <__mingw_enum_import_library_names+0xb7>
   140002490:	8b 50 0c             	mov    0xc(%rax),%edx
   140002493:	85 d2                	test   %edx,%edx
   140002495:	74 d7                	je     14000246e <__mingw_enum_import_library_names+0x8e>
   140002497:	85 c9                	test   %ecx,%ecx
   140002499:	7f e5                	jg     140002480 <__mingw_enum_import_library_names+0xa0>
   14000249b:	44 8b 48 0c          	mov    0xc(%rax),%r9d
   14000249f:	4d 01 d9             	add    %r11,%r9
   1400024a2:	4c 89 c8             	mov    %r9,%rax
   1400024a5:	c3                   	ret
   1400024a6:	90                   	nop
   1400024a7:	90                   	nop
   1400024a8:	90                   	nop
   1400024a9:	90                   	nop
   1400024aa:	90                   	nop
   1400024ab:	90                   	nop
   1400024ac:	90                   	nop
   1400024ad:	90                   	nop
   1400024ae:	90                   	nop
   1400024af:	90                   	nop

00000001400024b0 <___chkstk_ms>:
   1400024b0:	51                   	push   %rcx
   1400024b1:	50                   	push   %rax
   1400024b2:	48 3d 00 10 00 00    	cmp    $0x1000,%rax
   1400024b8:	48 8d 4c 24 18       	lea    0x18(%rsp),%rcx
   1400024bd:	72 19                	jb     1400024d8 <___chkstk_ms+0x28>
   1400024bf:	48 81 e9 00 10 00 00 	sub    $0x1000,%rcx
   1400024c6:	48 83 09 00          	orq    $0x0,(%rcx)
   1400024ca:	48 2d 00 10 00 00    	sub    $0x1000,%rax
   1400024d0:	48 3d 00 10 00 00    	cmp    $0x1000,%rax
   1400024d6:	77 e7                	ja     1400024bf <___chkstk_ms+0xf>
   1400024d8:	48 29 c1             	sub    %rax,%rcx
   1400024db:	48 83 09 00          	orq    $0x0,(%rcx)
   1400024df:	58                   	pop    %rax
   1400024e0:	59                   	pop    %rcx
   1400024e1:	c3                   	ret
   1400024e2:	90                   	nop
   1400024e3:	90                   	nop
   1400024e4:	90                   	nop
   1400024e5:	90                   	nop
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

00000001400024f0 <__p__fmode>:
   1400024f0:	48 8b 05 c9 1e 00 00 	mov    0x1ec9(%rip),%rax        # 1400043c0 <.refptr.__imp__fmode>
   1400024f7:	48 8b 00             	mov    (%rax),%rax
   1400024fa:	c3                   	ret
   1400024fb:	90                   	nop
   1400024fc:	90                   	nop
   1400024fd:	90                   	nop
   1400024fe:	90                   	nop
   1400024ff:	90                   	nop

0000000140002500 <__p__commode>:
   140002500:	48 8b 05 a9 1e 00 00 	mov    0x1ea9(%rip),%rax        # 1400043b0 <.refptr.__imp__commode>
   140002507:	48 8b 00             	mov    (%rax),%rax
   14000250a:	c3                   	ret
   14000250b:	90                   	nop
   14000250c:	90                   	nop
   14000250d:	90                   	nop
   14000250e:	90                   	nop
   14000250f:	90                   	nop

0000000140002510 <_get_invalid_parameter_handler>:
   140002510:	48 8b 05 59 4c 00 00 	mov    0x4c59(%rip),%rax        # 140007170 <handler>
   140002517:	c3                   	ret
   140002518:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   14000251f:	00 

0000000140002520 <_set_invalid_parameter_handler>:
   140002520:	48 89 c8             	mov    %rcx,%rax
   140002523:	48 87 05 46 4c 00 00 	xchg   %rax,0x4c46(%rip)        # 140007170 <handler>
   14000252a:	c3                   	ret
   14000252b:	90                   	nop
   14000252c:	90                   	nop
   14000252d:	90                   	nop
   14000252e:	90                   	nop
   14000252f:	90                   	nop

0000000140002530 <__acrt_iob_func>:
   140002530:	53                   	push   %rbx
   140002531:	48 83 ec 20          	sub    $0x20,%rsp
   140002535:	89 cb                	mov    %ecx,%ebx
   140002537:	e8 24 00 00 00       	call   140002560 <__iob_func>
   14000253c:	89 d9                	mov    %ebx,%ecx
   14000253e:	48 8d 14 49          	lea    (%rcx,%rcx,2),%rdx
   140002542:	48 c1 e2 04          	shl    $0x4,%rdx
   140002546:	48 01 d0             	add    %rdx,%rax
   140002549:	48 83 c4 20          	add    $0x20,%rsp
   14000254d:	5b                   	pop    %rbx
   14000254e:	c3                   	ret
   14000254f:	90                   	nop

0000000140002550 <__C_specific_handler>:
   140002550:	ff 25 5e 5c 00 00    	jmp    *0x5c5e(%rip)        # 1400081b4 <__imp___C_specific_handler>
   140002556:	90                   	nop
   140002557:	90                   	nop

0000000140002558 <__getmainargs>:
   140002558:	ff 25 5e 5c 00 00    	jmp    *0x5c5e(%rip)        # 1400081bc <__imp___getmainargs>
   14000255e:	90                   	nop
   14000255f:	90                   	nop

0000000140002560 <__iob_func>:
   140002560:	ff 25 66 5c 00 00    	jmp    *0x5c66(%rip)        # 1400081cc <__imp___iob_func>
   140002566:	90                   	nop
   140002567:	90                   	nop

0000000140002568 <__set_app_type>:
   140002568:	ff 25 66 5c 00 00    	jmp    *0x5c66(%rip)        # 1400081d4 <__imp___set_app_type>
   14000256e:	90                   	nop
   14000256f:	90                   	nop

0000000140002570 <__setusermatherr>:
   140002570:	ff 25 66 5c 00 00    	jmp    *0x5c66(%rip)        # 1400081dc <__imp___setusermatherr>
   140002576:	90                   	nop
   140002577:	90                   	nop

0000000140002578 <_amsg_exit>:
   140002578:	ff 25 66 5c 00 00    	jmp    *0x5c66(%rip)        # 1400081e4 <__imp__amsg_exit>
   14000257e:	90                   	nop
   14000257f:	90                   	nop

0000000140002580 <_cexit>:
   140002580:	ff 25 66 5c 00 00    	jmp    *0x5c66(%rip)        # 1400081ec <__imp__cexit>
   140002586:	90                   	nop
   140002587:	90                   	nop

0000000140002588 <_initterm>:
   140002588:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 140008204 <__imp__initterm>
   14000258e:	90                   	nop
   14000258f:	90                   	nop

0000000140002590 <_onexit>:
   140002590:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 14000820c <__imp__onexit>
   140002596:	90                   	nop
   140002597:	90                   	nop

0000000140002598 <abort>:
   140002598:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 140008214 <__imp_abort>
   14000259e:	90                   	nop
   14000259f:	90                   	nop

00000001400025a0 <calloc>:
   1400025a0:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 14000821c <__imp_calloc>
   1400025a6:	90                   	nop
   1400025a7:	90                   	nop

00000001400025a8 <exit>:
   1400025a8:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 140008224 <__imp_exit>
   1400025ae:	90                   	nop
   1400025af:	90                   	nop

00000001400025b0 <fprintf>:
   1400025b0:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 14000822c <__imp_fprintf>
   1400025b6:	90                   	nop
   1400025b7:	90                   	nop

00000001400025b8 <free>:
   1400025b8:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 140008234 <__imp_free>
   1400025be:	90                   	nop
   1400025bf:	90                   	nop

00000001400025c0 <fwrite>:
   1400025c0:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 14000823c <__imp_fwrite>
   1400025c6:	90                   	nop
   1400025c7:	90                   	nop

00000001400025c8 <malloc>:
   1400025c8:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 140008244 <__imp_malloc>
   1400025ce:	90                   	nop
   1400025cf:	90                   	nop

00000001400025d0 <memcpy>:
   1400025d0:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 14000824c <__imp_memcpy>
   1400025d6:	90                   	nop
   1400025d7:	90                   	nop

00000001400025d8 <signal>:
   1400025d8:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 140008254 <__imp_signal>
   1400025de:	90                   	nop
   1400025df:	90                   	nop

00000001400025e0 <strlen>:
   1400025e0:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 14000825c <__imp_strlen>
   1400025e6:	90                   	nop
   1400025e7:	90                   	nop

00000001400025e8 <strncmp>:
   1400025e8:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 140008264 <__imp_strncmp>
   1400025ee:	90                   	nop
   1400025ef:	90                   	nop

00000001400025f0 <vfprintf>:
   1400025f0:	ff 25 76 5c 00 00    	jmp    *0x5c76(%rip)        # 14000826c <__imp_vfprintf>
   1400025f6:	90                   	nop
   1400025f7:	90                   	nop
   1400025f8:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   1400025ff:	00 

0000000140002600 <VirtualQuery>:
   140002600:	ff 25 9e 5b 00 00    	jmp    *0x5b9e(%rip)        # 1400081a4 <__imp_VirtualQuery>
   140002606:	90                   	nop
   140002607:	90                   	nop

0000000140002608 <VirtualProtect>:
   140002608:	ff 25 8e 5b 00 00    	jmp    *0x5b8e(%rip)        # 14000819c <__imp_VirtualProtect>
   14000260e:	90                   	nop
   14000260f:	90                   	nop

0000000140002610 <TlsGetValue>:
   140002610:	ff 25 7e 5b 00 00    	jmp    *0x5b7e(%rip)        # 140008194 <__imp_TlsGetValue>
   140002616:	90                   	nop
   140002617:	90                   	nop

0000000140002618 <Sleep>:
   140002618:	ff 25 6e 5b 00 00    	jmp    *0x5b6e(%rip)        # 14000818c <__imp_Sleep>
   14000261e:	90                   	nop
   14000261f:	90                   	nop

0000000140002620 <SetUnhandledExceptionFilter>:
   140002620:	ff 25 5e 5b 00 00    	jmp    *0x5b5e(%rip)        # 140008184 <__imp_SetUnhandledExceptionFilter>
   140002626:	90                   	nop
   140002627:	90                   	nop

0000000140002628 <LeaveCriticalSection>:
   140002628:	ff 25 4e 5b 00 00    	jmp    *0x5b4e(%rip)        # 14000817c <__imp_LeaveCriticalSection>
   14000262e:	90                   	nop
   14000262f:	90                   	nop

0000000140002630 <InitializeCriticalSection>:
   140002630:	ff 25 3e 5b 00 00    	jmp    *0x5b3e(%rip)        # 140008174 <__imp_InitializeCriticalSection>
   140002636:	90                   	nop
   140002637:	90                   	nop

0000000140002638 <GetLastError>:
   140002638:	ff 25 2e 5b 00 00    	jmp    *0x5b2e(%rip)        # 14000816c <__imp_GetLastError>
   14000263e:	90                   	nop
   14000263f:	90                   	nop

0000000140002640 <EnterCriticalSection>:
   140002640:	ff 25 1e 5b 00 00    	jmp    *0x5b1e(%rip)        # 140008164 <__imp_EnterCriticalSection>
   140002646:	90                   	nop
   140002647:	90                   	nop

0000000140002648 <DeleteCriticalSection>:
   140002648:	ff 25 0e 5b 00 00    	jmp    *0x5b0e(%rip)        # 14000815c <__IAT_start__>
   14000264e:	90                   	nop
   14000264f:	90                   	nop

0000000140002650 <main>:
   140002650:	48 83 ec 28          	sub    $0x28,%rsp
   140002654:	e8 a7 ee ff ff       	call   140001500 <__main>
   140002659:	b8 10 00 00 00       	mov    $0x10,%eax
   14000265e:	48 83 c4 28          	add    $0x28,%rsp
   140002662:	c3                   	ret
   140002663:	90                   	nop
   140002664:	90                   	nop
   140002665:	90                   	nop
   140002666:	90                   	nop
   140002667:	90                   	nop
   140002668:	90                   	nop
   140002669:	90                   	nop
   14000266a:	90                   	nop
   14000266b:	90                   	nop
   14000266c:	90                   	nop
   14000266d:	90                   	nop
   14000266e:	90                   	nop
   14000266f:	90                   	nop

0000000140002670 <register_frame_ctor>:
   140002670:	e9 bb ed ff ff       	jmp    140001430 <__gcc_register_frame>
   140002675:	90                   	nop
   140002676:	90                   	nop
   140002677:	90                   	nop
   140002678:	90                   	nop
   140002679:	90                   	nop
   14000267a:	90                   	nop
   14000267b:	90                   	nop
   14000267c:	90                   	nop
   14000267d:	90                   	nop
   14000267e:	90                   	nop
   14000267f:	90                   	nop

0000000140002680 <__CTOR_LIST__>:
   140002680:	ff                   	(bad)
   140002681:	ff                   	(bad)
   140002682:	ff                   	(bad)
   140002683:	ff                   	(bad)
   140002684:	ff                   	(bad)
   140002685:	ff                   	(bad)
   140002686:	ff                   	(bad)
   140002687:	ff                   	.byte 0xff

0000000140002688 <.ctors.65535>:
   140002688:	70 26                	jo     1400026b0 <__DTOR_LIST__+0x18>
   14000268a:	00 40 01             	add    %al,0x1(%rax)
	...

0000000140002698 <__DTOR_LIST__>:
   140002698:	ff                   	(bad)
   140002699:	ff                   	(bad)
   14000269a:	ff                   	(bad)
   14000269b:	ff                   	(bad)
   14000269c:	ff                   	(bad)
   14000269d:	ff                   	(bad)
   14000269e:	ff                   	(bad)
   14000269f:	ff 00                	incl   (%rax)
   1400026a1:	00 00                	add    %al,(%rax)
   1400026a3:	00 00                	add    %al,(%rax)
   1400026a5:	00 00                	add    %al,(%rax)
	...
