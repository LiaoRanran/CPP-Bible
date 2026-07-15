
ch26_lambda_capture_test.exe:     file format pei-x86-64


Disassembly of section .text:

0000000140001000 <__mingw_invalidParameterHandler>:
   140001000:	55                   	push   rbp
   140001001:	48 89 e5             	mov    rbp,rsp
   140001004:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001008:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000100c:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001010:	44 89 4d 28          	mov    DWORD PTR [rbp+0x28],r9d
   140001014:	90                   	nop
   140001015:	5d                   	pop    rbp
   140001016:	c3                   	ret

0000000140001017 <safe_flush>:
   140001017:	55                   	push   rbp
   140001018:	48 89 e5             	mov    rbp,rsp
   14000101b:	48 83 ec 20          	sub    rsp,0x20
   14000101f:	b9 00 00 00 00       	mov    ecx,0x0
   140001024:	e8 8f 85 00 00       	call   1400095b8 <fflush>
   140001029:	90                   	nop
   14000102a:	48 83 c4 20          	add    rsp,0x20
   14000102e:	5d                   	pop    rbp
   14000102f:	c3                   	ret

0000000140001030 <WinMainCRTStartup>:
   140001030:	55                   	push   rbp
   140001031:	48 89 e5             	mov    rbp,rsp
   140001034:	48 83 ec 30          	sub    rsp,0x30
   140001038:	c7 45 fc ff 00 00 00 	mov    DWORD PTR [rbp-0x4],0xff

000000014000103f <.l_startw>:
   14000103f:	48 8b 05 ca a5 00 00 	mov    rax,QWORD PTR [rip+0xa5ca]        # 14000b610 <.refptr.__mingw_app_type>
   140001046:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000104c:	e8 3d 00 00 00       	call   14000108e <__tmainCRTStartup>
   140001051:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140001054:	90                   	nop

0000000140001055 <.l_endw>:
   140001055:	90                   	nop
   140001056:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001059:	48 83 c4 30          	add    rsp,0x30
   14000105d:	5d                   	pop    rbp
   14000105e:	c3                   	ret

000000014000105f <mainCRTStartup>:
   14000105f:	55                   	push   rbp
   140001060:	48 89 e5             	mov    rbp,rsp
   140001063:	48 83 ec 30          	sub    rsp,0x30
   140001067:	c7 45 fc ff 00 00 00 	mov    DWORD PTR [rbp-0x4],0xff

000000014000106e <.l_start>:
   14000106e:	48 8b 05 9b a5 00 00 	mov    rax,QWORD PTR [rip+0xa59b]        # 14000b610 <.refptr.__mingw_app_type>
   140001075:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   14000107b:	e8 0e 00 00 00       	call   14000108e <__tmainCRTStartup>
   140001080:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140001083:	90                   	nop

0000000140001084 <.l_end>:
   140001084:	90                   	nop
   140001085:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001088:	48 83 c4 30          	add    rsp,0x30
   14000108c:	5d                   	pop    rbp
   14000108d:	c3                   	ret

000000014000108e <__tmainCRTStartup>:
   14000108e:	55                   	push   rbp
   14000108f:	48 89 e5             	mov    rbp,rsp
   140001092:	48 81 ec 90 00 00 00 	sub    rsp,0x90
   140001099:	48 c7 45 f0 00 00 00 	mov    QWORD PTR [rbp-0x10],0x0
   1400010a0:	00 
   1400010a1:	c7 45 e0 30 00 00 00 	mov    DWORD PTR [rbp-0x20],0x30
   1400010a8:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
   1400010ab:	65 67 48 8b 00       	mov    rax,QWORD PTR gs:[eax]
   1400010b0:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   1400010b4:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   1400010b8:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   1400010bc:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400010c0:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400010c7:	c7 45 e4 00 00 00 00 	mov    DWORD PTR [rbp-0x1c],0x0
   1400010ce:	eb 21                	jmp    1400010f1 <__tmainCRTStartup+0x63>
   1400010d0:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400010d4:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   1400010d8:	75 09                	jne    1400010e3 <__tmainCRTStartup+0x55>
   1400010da:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   1400010e1:	eb 45                	jmp    140001128 <__tmainCRTStartup+0x9a>
   1400010e3:	b9 e8 03 00 00       	mov    ecx,0x3e8
   1400010e8:	48 8b 05 59 f1 00 00 	mov    rax,QWORD PTR [rip+0xf159]        # 140010248 <__imp_Sleep>
   1400010ef:	ff d0                	call   rax
   1400010f1:	48 8b 05 68 a5 00 00 	mov    rax,QWORD PTR [rip+0xa568]        # 14000b660 <.refptr.__native_startup_lock>
   1400010f8:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   1400010fc:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001100:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140001104:	48 c7 45 c0 00 00 00 	mov    QWORD PTR [rbp-0x40],0x0
   14000110b:	00 
   14000110c:	48 8b 4d c8          	mov    rcx,QWORD PTR [rbp-0x38]
   140001110:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001114:	48 8b 55 d0          	mov    rdx,QWORD PTR [rbp-0x30]
   140001118:	f0 48 0f b1 0a       	lock cmpxchg QWORD PTR [rdx],rcx
   14000111d:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001121:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001126:	75 a8                	jne    1400010d0 <__tmainCRTStartup+0x42>
   140001128:	48 8b 05 41 a5 00 00 	mov    rax,QWORD PTR [rip+0xa541]        # 14000b670 <.refptr.__native_startup_state>
   14000112f:	8b 00                	mov    eax,DWORD PTR [rax]
   140001131:	83 f8 01             	cmp    eax,0x1
   140001134:	75 0a                	jne    140001140 <__tmainCRTStartup+0xb2>
   140001136:	b9 1f 00 00 00       	mov    ecx,0x1f
   14000113b:	e8 28 84 00 00       	call   140009568 <_amsg_exit>
   140001140:	48 8b 05 29 a5 00 00 	mov    rax,QWORD PTR [rip+0xa529]        # 14000b670 <.refptr.__native_startup_state>
   140001147:	8b 00                	mov    eax,DWORD PTR [rax]
   140001149:	85 c0                	test   eax,eax
   14000114b:	0f 85 e3 01 00 00    	jne    140001334 <__tmainCRTStartup+0x2a6>
   140001151:	48 8b 05 18 a5 00 00 	mov    rax,QWORD PTR [rip+0xa518]        # 14000b670 <.refptr.__native_startup_state>
   140001158:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000115e:	b9 02 00 00 00       	mov    ecx,0x2
   140001163:	e8 28 7e 00 00       	call   140008f90 <__acrt_iob_func>
   140001168:	41 b9 00 00 00 00    	mov    r9d,0x0
   14000116e:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001174:	ba 00 00 00 00       	mov    edx,0x0
   140001179:	48 89 c1             	mov    rcx,rax
   14000117c:	e8 6f 84 00 00       	call   1400095f0 <setvbuf>
   140001181:	48 8d 05 8f fe ff ff 	lea    rax,[rip+0xfffffffffffffe8f]        # 140001017 <safe_flush>
   140001188:	48 89 c1             	mov    rcx,rax
   14000118b:	e8 9f 04 00 00       	call   14000162f <atexit>
   140001190:	85 c0                	test   eax,eax
   140001192:	74 05                	je     140001199 <__tmainCRTStartup+0x10b>
   140001194:	e8 07 84 00 00       	call   1400095a0 <abort>
   140001199:	e8 f2 10 00 00       	call   140002290 <_pei386_runtime_relocator>
   14000119e:	48 8b 05 5b a5 00 00 	mov    rax,QWORD PTR [rip+0xa55b]        # 14000b700 <.refptr._gnu_exception_handler>
   1400011a5:	48 89 c1             	mov    rcx,rax
   1400011a8:	48 8b 05 91 f0 00 00 	mov    rax,QWORD PTR [rip+0xf091]        # 140010240 <__imp_SetUnhandledExceptionFilter>
   1400011af:	ff d0                	call   rax
   1400011b1:	48 8b 15 98 a4 00 00 	mov    rdx,QWORD PTR [rip+0xa498]        # 14000b650 <.refptr.__mingw_oldexcpt_handler>
   1400011b8:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400011bb:	48 8d 05 3e fe ff ff 	lea    rax,[rip+0xfffffffffffffe3e]        # 140001000 <__mingw_invalidParameterHandler>
   1400011c2:	48 89 c1             	mov    rcx,rax
   1400011c5:	e8 66 7d 00 00       	call   140008f30 <_set_invalid_parameter_handler>
   1400011ca:	e8 d1 19 00 00       	call   140002ba0 <_fpreset>
   1400011cf:	e8 18 02 00 00       	call   1400013ec <check_managed_app>
   1400011d4:	89 05 3e de 00 00    	mov    DWORD PTR [rip+0xde3e],eax        # 14000f018 <managedapp>
   1400011da:	48 8b 05 2f a4 00 00 	mov    rax,QWORD PTR [rip+0xa42f]        # 14000b610 <.refptr.__mingw_app_type>
   1400011e1:	8b 00                	mov    eax,DWORD PTR [rax]
   1400011e3:	85 c0                	test   eax,eax
   1400011e5:	74 0c                	je     1400011f3 <__tmainCRTStartup+0x165>
   1400011e7:	b9 02 00 00 00       	mov    ecx,0x2
   1400011ec:	e8 67 83 00 00       	call   140009558 <__set_app_type>
   1400011f1:	eb 0a                	jmp    1400011fd <__tmainCRTStartup+0x16f>
   1400011f3:	b9 01 00 00 00       	mov    ecx,0x1
   1400011f8:	e8 5b 83 00 00       	call   140009558 <__set_app_type>
   1400011fd:	e8 de 7b 00 00       	call   140008de0 <__p__fmode>
   140001202:	48 8b 15 e7 a4 00 00 	mov    rdx,QWORD PTR [rip+0xa4e7]        # 14000b6f0 <.refptr._fmode>
   140001209:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000120b:	89 10                	mov    DWORD PTR [rax],edx
   14000120d:	e8 de 7b 00 00       	call   140008df0 <__p__commode>
   140001212:	48 8b 15 b7 a4 00 00 	mov    rdx,QWORD PTR [rip+0xa4b7]        # 14000b6d0 <.refptr._commode>
   140001219:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000121b:	89 10                	mov    DWORD PTR [rax],edx
   14000121d:	e8 4e 06 00 00       	call   140001870 <_setargv>
   140001222:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140001225:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140001229:	79 0a                	jns    140001235 <__tmainCRTStartup+0x1a7>
   14000122b:	b9 08 00 00 00       	mov    ecx,0x8
   140001230:	e8 33 83 00 00       	call   140009568 <_amsg_exit>
   140001235:	48 8b 05 24 a3 00 00 	mov    rax,QWORD PTR [rip+0xa324]        # 14000b560 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   14000123c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000123e:	83 f8 01             	cmp    eax,0x1
   140001241:	75 0f                	jne    140001252 <__tmainCRTStartup+0x1c4>
   140001243:	48 8b 05 c6 a4 00 00 	mov    rax,QWORD PTR [rip+0xa4c6]        # 14000b710 <.refptr._matherr>
   14000124a:	48 89 c1             	mov    rcx,rax
   14000124d:	e8 58 11 00 00       	call   1400023aa <__mingw_setusermatherr>
   140001252:	48 8b 05 77 a3 00 00 	mov    rax,QWORD PTR [rip+0xa377]        # 14000b5d0 <.refptr.__globallocalestatus>
   140001259:	8b 00                	mov    eax,DWORD PTR [rax]
   14000125b:	83 f8 ff             	cmp    eax,0xffffffff
   14000125e:	75 0a                	jne    14000126a <__tmainCRTStartup+0x1dc>
   140001260:	b9 ff ff ff ff       	mov    ecx,0xffffffff
   140001265:	e8 06 7d 00 00       	call   140008f70 <_configthreadlocale>
   14000126a:	48 8b 15 4f a4 00 00 	mov    rdx,QWORD PTR [rip+0xa44f]        # 14000b6c0 <.refptr.__xi_z>
   140001271:	48 8b 05 38 a4 00 00 	mov    rax,QWORD PTR [rip+0xa438]        # 14000b6b0 <.refptr.__xi_a>
   140001278:	48 89 c1             	mov    rcx,rax
   14000127b:	e8 00 7b 00 00       	call   140008d80 <_initterm_e>
   140001280:	85 c0                	test   eax,eax
   140001282:	74 0a                	je     14000128e <__tmainCRTStartup+0x200>
   140001284:	b9 0a 00 00 00       	mov    ecx,0xa
   140001289:	e8 da 82 00 00       	call   140009568 <_amsg_exit>
   14000128e:	48 8b 05 8b a4 00 00 	mov    rax,QWORD PTR [rip+0xa48b]        # 14000b720 <.refptr._newmode>
   140001295:	8b 00                	mov    eax,DWORD PTR [rax]
   140001297:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000129a:	48 8b 05 3f a4 00 00 	mov    rax,QWORD PTR [rip+0xa43f]        # 14000b6e0 <.refptr._dowildcard>
   1400012a1:	44 8b 00             	mov    r8d,DWORD PTR [rax]
   1400012a4:	4c 8d 15 65 dd 00 00 	lea    r10,[rip+0xdd65]        # 14000f010 <envp>
   1400012ab:	48 8d 15 56 dd 00 00 	lea    rdx,[rip+0xdd56]        # 14000f008 <argv>
   1400012b2:	48 8d 05 4b dd 00 00 	lea    rax,[rip+0xdd4b]        # 14000f004 <argc>
   1400012b9:	48 8d 4d ac          	lea    rcx,[rbp-0x54]
   1400012bd:	48 89 4c 24 20       	mov    QWORD PTR [rsp+0x20],rcx
   1400012c2:	45 89 c1             	mov    r9d,r8d
   1400012c5:	4d 89 d0             	mov    r8,r10
   1400012c8:	48 89 c1             	mov    rcx,rax
   1400012cb:	e8 78 82 00 00       	call   140009548 <__getmainargs>
   1400012d0:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012d3:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012d7:	79 0a                	jns    1400012e3 <__tmainCRTStartup+0x255>
   1400012d9:	b9 08 00 00 00       	mov    ecx,0x8
   1400012de:	e8 85 82 00 00       	call   140009568 <_amsg_exit>
   1400012e3:	8b 05 1b dd 00 00    	mov    eax,DWORD PTR [rip+0xdd1b]        # 14000f004 <argc>
   1400012e9:	48 8d 15 18 dd 00 00 	lea    rdx,[rip+0xdd18]        # 14000f008 <argv>
   1400012f0:	89 c1                	mov    ecx,eax
   1400012f2:	e8 f9 01 00 00       	call   1400014f0 <duplicate_ppstrings>
   1400012f7:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012fa:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012fe:	74 0a                	je     14000130a <__tmainCRTStartup+0x27c>
   140001300:	b9 08 00 00 00       	mov    ecx,0x8
   140001305:	e8 5e 82 00 00       	call   140009568 <_amsg_exit>
   14000130a:	48 8b 15 8f a3 00 00 	mov    rdx,QWORD PTR [rip+0xa38f]        # 14000b6a0 <.refptr.__xc_z>
   140001311:	48 8b 05 78 a3 00 00 	mov    rax,QWORD PTR [rip+0xa378]        # 14000b690 <.refptr.__xc_a>
   140001318:	48 89 c1             	mov    rcx,rax
   14000131b:	e8 60 82 00 00       	call   140009580 <_initterm>
   140001320:	e8 22 05 00 00       	call   140001847 <__main>
   140001325:	48 8b 05 44 a3 00 00 	mov    rax,QWORD PTR [rip+0xa344]        # 14000b670 <.refptr.__native_startup_state>
   14000132c:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   140001332:	eb 0a                	jmp    14000133e <__tmainCRTStartup+0x2b0>
   140001334:	c7 05 de dc 00 00 01 	mov    DWORD PTR [rip+0xdcde],0x1        # 14000f01c <has_cctor>
   14000133b:	00 00 00 
   14000133e:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140001342:	75 1e                	jne    140001362 <__tmainCRTStartup+0x2d4>
   140001344:	48 8b 05 15 a3 00 00 	mov    rax,QWORD PTR [rip+0xa315]        # 14000b660 <.refptr.__native_startup_lock>
   14000134b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000134f:	48 c7 45 b0 00 00 00 	mov    QWORD PTR [rbp-0x50],0x0
   140001356:	00 
   140001357:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   14000135b:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000135f:	48 87 10             	xchg   QWORD PTR [rax],rdx
   140001362:	48 8b 05 57 a2 00 00 	mov    rax,QWORD PTR [rip+0xa257]        # 14000b5c0 <.refptr.__dyn_tls_init_callback>
   140001369:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000136c:	48 85 c0             	test   rax,rax
   14000136f:	74 1c                	je     14000138d <__tmainCRTStartup+0x2ff>
   140001371:	48 8b 05 48 a2 00 00 	mov    rax,QWORD PTR [rip+0xa248]        # 14000b5c0 <.refptr.__dyn_tls_init_callback>
   140001378:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000137b:	41 b8 00 00 00 00    	mov    r8d,0x0
   140001381:	ba 02 00 00 00       	mov    edx,0x2
   140001386:	b9 00 00 00 00       	mov    ecx,0x0
   14000138b:	ff d0                	call   rax
   14000138d:	e8 6e 7a 00 00       	call   140008e00 <__p___initenv>
   140001392:	48 8b 15 77 dc 00 00 	mov    rdx,QWORD PTR [rip+0xdc77]        # 14000f010 <envp>
   140001399:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000139c:	48 8b 0d 6d dc 00 00 	mov    rcx,QWORD PTR [rip+0xdc6d]        # 14000f010 <envp>
   1400013a3:	48 8b 15 5e dc 00 00 	mov    rdx,QWORD PTR [rip+0xdc5e]        # 14000f008 <argv>
   1400013aa:	8b 05 54 dc 00 00    	mov    eax,DWORD PTR [rip+0xdc54]        # 14000f004 <argc>
   1400013b0:	49 89 c8             	mov    r8,rcx
   1400013b3:	89 c1                	mov    ecx,eax
   1400013b5:	e8 06 83 00 00       	call   1400096c0 <main>
   1400013ba:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400013bd:	8b 05 55 dc 00 00    	mov    eax,DWORD PTR [rip+0xdc55]        # 14000f018 <managedapp>
   1400013c3:	85 c0                	test   eax,eax
   1400013c5:	75 0a                	jne    1400013d1 <__tmainCRTStartup+0x343>
   1400013c7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013ca:	89 c1                	mov    ecx,eax
   1400013cc:	e8 df 81 00 00       	call   1400095b0 <exit>
   1400013d1:	8b 05 45 dc 00 00    	mov    eax,DWORD PTR [rip+0xdc45]        # 14000f01c <has_cctor>
   1400013d7:	85 c0                	test   eax,eax
   1400013d9:	75 05                	jne    1400013e0 <__tmainCRTStartup+0x352>
   1400013db:	e8 90 81 00 00       	call   140009570 <_cexit>
   1400013e0:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013e3:	48 81 c4 90 00 00 00 	add    rsp,0x90
   1400013ea:	5d                   	pop    rbp
   1400013eb:	c3                   	ret

00000001400013ec <check_managed_app>:
   1400013ec:	55                   	push   rbp
   1400013ed:	48 89 e5             	mov    rbp,rsp
   1400013f0:	48 83 ec 20          	sub    rsp,0x20
   1400013f4:	48 8b 05 25 a2 00 00 	mov    rax,QWORD PTR [rip+0xa225]        # 14000b620 <.refptr.__mingw_initltsdrot_force>
   1400013fb:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   140001401:	48 8b 05 28 a2 00 00 	mov    rax,QWORD PTR [rip+0xa228]        # 14000b630 <.refptr.__mingw_initltsdyn_force>
   140001408:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000140e:	48 8b 05 2b a2 00 00 	mov    rax,QWORD PTR [rip+0xa22b]        # 14000b640 <.refptr.__mingw_initltssuo_force>
   140001415:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000141b:	48 8b 05 5e a1 00 00 	mov    rax,QWORD PTR [rip+0xa15e]        # 14000b580 <.refptr.__ImageBase>
   140001422:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001426:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000142a:	0f b7 00             	movzx  eax,WORD PTR [rax]
   14000142d:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140001431:	74 0a                	je     14000143d <check_managed_app+0x51>
   140001433:	b8 00 00 00 00       	mov    eax,0x0
   140001438:	e9 ad 00 00 00       	jmp    1400014ea <check_managed_app+0xfe>
   14000143d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001441:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140001444:	48 63 d0             	movsxd rdx,eax
   140001447:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000144b:	48 01 d0             	add    rax,rdx
   14000144e:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001452:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001456:	8b 00                	mov    eax,DWORD PTR [rax]
   140001458:	3d 50 45 00 00       	cmp    eax,0x4550
   14000145d:	74 0a                	je     140001469 <check_managed_app+0x7d>
   14000145f:	b8 00 00 00 00       	mov    eax,0x0
   140001464:	e9 81 00 00 00       	jmp    1400014ea <check_managed_app+0xfe>
   140001469:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000146d:	48 83 c0 18          	add    rax,0x18
   140001471:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140001475:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001479:	0f b7 00             	movzx  eax,WORD PTR [rax]
   14000147c:	0f b7 c0             	movzx  eax,ax
   14000147f:	3d 0b 01 00 00       	cmp    eax,0x10b
   140001484:	74 09                	je     14000148f <check_managed_app+0xa3>
   140001486:	3d 0b 02 00 00       	cmp    eax,0x20b
   14000148b:	74 29                	je     1400014b6 <check_managed_app+0xca>
   14000148d:	eb 56                	jmp    1400014e5 <check_managed_app+0xf9>
   14000148f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001493:	8b 40 5c             	mov    eax,DWORD PTR [rax+0x5c]
   140001496:	83 f8 0e             	cmp    eax,0xe
   140001499:	77 07                	ja     1400014a2 <check_managed_app+0xb6>
   14000149b:	b8 00 00 00 00       	mov    eax,0x0
   1400014a0:	eb 48                	jmp    1400014ea <check_managed_app+0xfe>
   1400014a2:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400014a6:	8b 80 d0 00 00 00    	mov    eax,DWORD PTR [rax+0xd0]
   1400014ac:	85 c0                	test   eax,eax
   1400014ae:	0f 95 c0             	setne  al
   1400014b1:	0f b6 c0             	movzx  eax,al
   1400014b4:	eb 34                	jmp    1400014ea <check_managed_app+0xfe>
   1400014b6:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400014ba:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400014be:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400014c2:	8b 40 6c             	mov    eax,DWORD PTR [rax+0x6c]
   1400014c5:	83 f8 0e             	cmp    eax,0xe
   1400014c8:	77 07                	ja     1400014d1 <check_managed_app+0xe5>
   1400014ca:	b8 00 00 00 00       	mov    eax,0x0
   1400014cf:	eb 19                	jmp    1400014ea <check_managed_app+0xfe>
   1400014d1:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400014d5:	8b 80 e0 00 00 00    	mov    eax,DWORD PTR [rax+0xe0]
   1400014db:	85 c0                	test   eax,eax
   1400014dd:	0f 95 c0             	setne  al
   1400014e0:	0f b6 c0             	movzx  eax,al
   1400014e3:	eb 05                	jmp    1400014ea <check_managed_app+0xfe>
   1400014e5:	b8 00 00 00 00       	mov    eax,0x0
   1400014ea:	48 83 c4 20          	add    rsp,0x20
   1400014ee:	5d                   	pop    rbp
   1400014ef:	c3                   	ret

00000001400014f0 <duplicate_ppstrings>:
   1400014f0:	55                   	push   rbp
   1400014f1:	53                   	push   rbx
   1400014f2:	48 83 ec 48          	sub    rsp,0x48
   1400014f6:	48 8d 6c 24 40       	lea    rbp,[rsp+0x40]
   1400014fb:	89 4d 20             	mov    DWORD PTR [rbp+0x20],ecx
   1400014fe:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001502:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140001505:	83 c0 01             	add    eax,0x1
   140001508:	48 98                	cdqe
   14000150a:	48 c1 e0 03          	shl    rax,0x3
   14000150e:	48 89 c1             	mov    rcx,rax
   140001511:	e8 ca 80 00 00       	call   1400095e0 <malloc>
   140001516:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000151a:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000151f:	75 0a                	jne    14000152b <duplicate_ppstrings+0x3b>
   140001521:	b8 01 00 00 00       	mov    eax,0x1
   140001526:	e9 fd 00 00 00       	jmp    140001628 <duplicate_ppstrings+0x138>
   14000152b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000152f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001532:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140001536:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000153d:	e9 af 00 00 00       	jmp    1400015f1 <duplicate_ppstrings+0x101>
   140001542:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001545:	48 98                	cdqe
   140001547:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   14000154e:	00 
   14000154f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001553:	48 01 d0             	add    rax,rdx
   140001556:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001559:	48 89 c1             	mov    rcx,rax
   14000155c:	e8 a7 80 00 00       	call   140009608 <strlen>
   140001561:	48 83 c0 01          	add    rax,0x1
   140001565:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001569:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000156c:	48 98                	cdqe
   14000156e:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   140001575:	00 
   140001576:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000157a:	48 8d 1c 02          	lea    rbx,[rdx+rax*1]
   14000157e:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001582:	48 89 c1             	mov    rcx,rax
   140001585:	e8 56 80 00 00       	call   1400095e0 <malloc>
   14000158a:	48 89 03             	mov    QWORD PTR [rbx],rax
   14000158d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001590:	48 98                	cdqe
   140001592:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   140001599:	00 
   14000159a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000159e:	48 01 d0             	add    rax,rdx
   1400015a1:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400015a4:	48 85 c0             	test   rax,rax
   1400015a7:	75 07                	jne    1400015b0 <duplicate_ppstrings+0xc0>
   1400015a9:	b8 01 00 00 00       	mov    eax,0x1
   1400015ae:	eb 78                	jmp    140001628 <duplicate_ppstrings+0x138>
   1400015b0:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400015b3:	48 98                	cdqe
   1400015b5:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   1400015bc:	00 
   1400015bd:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400015c1:	48 01 d0             	add    rax,rdx
   1400015c4:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   1400015c7:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400015ca:	48 98                	cdqe
   1400015cc:	48 8d 0c c5 00 00 00 	lea    rcx,[rax*8+0x0]
   1400015d3:	00 
   1400015d4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400015d8:	48 01 c8             	add    rax,rcx
   1400015db:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400015de:	48 8b 4d e0          	mov    rcx,QWORD PTR [rbp-0x20]
   1400015e2:	49 89 c8             	mov    r8,rcx
   1400015e5:	48 89 c1             	mov    rcx,rax
   1400015e8:	e8 fb 7f 00 00       	call   1400095e8 <memcpy>
   1400015ed:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   1400015f1:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400015f4:	3b 45 20             	cmp    eax,DWORD PTR [rbp+0x20]
   1400015f7:	0f 8c 45 ff ff ff    	jl     140001542 <duplicate_ppstrings+0x52>
   1400015fd:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001600:	48 98                	cdqe
   140001602:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   140001609:	00 
   14000160a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000160e:	48 01 d0             	add    rax,rdx
   140001611:	48 c7 00 00 00 00 00 	mov    QWORD PTR [rax],0x0
   140001618:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000161c:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140001620:	48 89 10             	mov    QWORD PTR [rax],rdx
   140001623:	b8 00 00 00 00       	mov    eax,0x0
   140001628:	48 83 c4 48          	add    rsp,0x48
   14000162c:	5b                   	pop    rbx
   14000162d:	5d                   	pop    rbp
   14000162e:	c3                   	ret

000000014000162f <atexit>:
   14000162f:	55                   	push   rbp
   140001630:	48 89 e5             	mov    rbp,rsp
   140001633:	48 83 ec 20          	sub    rsp,0x20
   140001637:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000163b:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000163f:	48 89 c1             	mov    rcx,rax
   140001642:	e8 51 7f 00 00       	call   140009598 <_crt_atexit>
   140001647:	48 83 c4 20          	add    rsp,0x20
   14000164b:	5d                   	pop    rbp
   14000164c:	c3                   	ret
   14000164d:	90                   	nop
   14000164e:	90                   	nop
   14000164f:	90                   	nop

0000000140001650 <.weak.__register_frame_info.hmod_libgcc>:
   140001650:	c3                   	ret
   140001651:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   140001655:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000165c:	00 00 00 00 

0000000140001660 <.weak.__deregister_frame_info.hmod_libgcc>:
   140001660:	31 c0                	xor    eax,eax
   140001662:	c3                   	ret
   140001663:	66 90                	xchg   ax,ax
   140001665:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000166c:	00 00 00 00 

0000000140001670 <__gcc_register_frame>:
   140001670:	55                   	push   rbp
   140001671:	53                   	push   rbx
   140001672:	48 83 ec 38          	sub    rsp,0x38
   140001676:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   14000167b:	48 8d 0d 7e 99 00 00 	lea    rcx,[rip+0x997e]        # 14000b000 <.rdata>
   140001682:	ff 15 88 eb 00 00    	call   QWORD PTR [rip+0xeb88]        # 140010210 <__imp_GetModuleHandleA>
   140001688:	48 89 c3             	mov    rbx,rax
   14000168b:	48 85 c0             	test   rax,rax
   14000168e:	74 70                	je     140001700 <__gcc_register_frame+0x90>
   140001690:	48 8d 0d 69 99 00 00 	lea    rcx,[rip+0x9969]        # 14000b000 <.rdata>
   140001697:	ff 15 93 eb 00 00    	call   QWORD PTR [rip+0xeb93]        # 140010230 <__imp_LoadLibraryA>
   14000169d:	4c 8b 0d 74 eb 00 00 	mov    r9,QWORD PTR [rip+0xeb74]        # 140010218 <__imp_GetProcAddress>
   1400016a4:	48 8d 15 68 99 00 00 	lea    rdx,[rip+0x9968]        # 14000b013 <.rdata+0x13>
   1400016ab:	48 89 d9             	mov    rcx,rbx
   1400016ae:	48 89 05 6b d9 00 00 	mov    QWORD PTR [rip+0xd96b],rax        # 14000f020 <hmod_libgcc>
   1400016b5:	4c 89 4d f0          	mov    QWORD PTR [rbp-0x10],r9
   1400016b9:	41 ff d1             	call   r9
   1400016bc:	48 8d 15 66 99 00 00 	lea    rdx,[rip+0x9966]        # 14000b029 <.rdata+0x29>
   1400016c3:	48 89 d9             	mov    rcx,rbx
   1400016c6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400016ca:	ff 55 f0             	call   QWORD PTR [rbp-0x10]
   1400016cd:	4c 8b 45 f8          	mov    r8,QWORD PTR [rbp-0x8]
   1400016d1:	48 89 05 28 89 00 00 	mov    QWORD PTR [rip+0x8928],rax        # 14000a000 <__data_start__>
   1400016d8:	4d 85 c0             	test   r8,r8
   1400016db:	74 11                	je     1400016ee <__gcc_register_frame+0x7e>
   1400016dd:	48 8d 15 5c d9 00 00 	lea    rdx,[rip+0xd95c]        # 14000f040 <obj>
   1400016e4:	48 8d 0d 15 a9 00 00 	lea    rcx,[rip+0xa915]        # 14000c000 <__EH_FRAME_BEGIN__>
   1400016eb:	41 ff d0             	call   r8
   1400016ee:	48 8d 0d 2b 00 00 00 	lea    rcx,[rip+0x2b]        # 140001720 <__gcc_deregister_frame>
   1400016f5:	48 83 c4 38          	add    rsp,0x38
   1400016f9:	5b                   	pop    rbx
   1400016fa:	5d                   	pop    rbp
   1400016fb:	e9 2f ff ff ff       	jmp    14000162f <atexit>
   140001700:	48 8d 05 59 ff ff ff 	lea    rax,[rip+0xffffffffffffff59]        # 140001660 <.weak.__deregister_frame_info.hmod_libgcc>
   140001707:	4c 8d 05 42 ff ff ff 	lea    r8,[rip+0xffffffffffffff42]        # 140001650 <.weak.__register_frame_info.hmod_libgcc>
   14000170e:	48 89 05 eb 88 00 00 	mov    QWORD PTR [rip+0x88eb],rax        # 14000a000 <__data_start__>
   140001715:	eb c6                	jmp    1400016dd <__gcc_register_frame+0x6d>
   140001717:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000171e:	00 00 

0000000140001720 <__gcc_deregister_frame>:
   140001720:	55                   	push   rbp
   140001721:	48 89 e5             	mov    rbp,rsp
   140001724:	48 83 ec 20          	sub    rsp,0x20
   140001728:	48 8b 05 d1 88 00 00 	mov    rax,QWORD PTR [rip+0x88d1]        # 14000a000 <__data_start__>
   14000172f:	48 85 c0             	test   rax,rax
   140001732:	74 09                	je     14000173d <__gcc_deregister_frame+0x1d>
   140001734:	48 8d 0d c5 a8 00 00 	lea    rcx,[rip+0xa8c5]        # 14000c000 <__EH_FRAME_BEGIN__>
   14000173b:	ff d0                	call   rax
   14000173d:	48 8b 0d dc d8 00 00 	mov    rcx,QWORD PTR [rip+0xd8dc]        # 14000f020 <hmod_libgcc>
   140001744:	48 85 c9             	test   rcx,rcx
   140001747:	74 0f                	je     140001758 <__gcc_deregister_frame+0x38>
   140001749:	48 83 c4 20          	add    rsp,0x20
   14000174d:	5d                   	pop    rbp
   14000174e:	48 ff 25 a3 ea 00 00 	rex.W jmp QWORD PTR [rip+0xeaa3]        # 1400101f8 <__imp_FreeLibrary>
   140001755:	0f 1f 00             	nop    DWORD PTR [rax]
   140001758:	48 83 c4 20          	add    rsp,0x20
   14000175c:	5d                   	pop    rbp
   14000175d:	c3                   	ret
   14000175e:	90                   	nop
   14000175f:	90                   	nop

0000000140001760 <sink(int)>:
   140001760:	89 c8                	mov    eax,ecx
   140001762:	c3                   	ret
   140001763:	66 90                	xchg   ax,ax
   140001765:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000176c:	00 00 00 00 

0000000140001770 <get_field()>:
   140001770:	48 8d 05 99 88 00 00 	lea    rax,[rip+0x8899]        # 14000a010 <get_field()::g>
   140001777:	c3                   	ret
   140001778:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000177f:	00 

0000000140001780 <bump(int*)>:
   140001780:	83 01 64             	add    DWORD PTR [rcx],0x64
   140001783:	c3                   	ret
   140001784:	90                   	nop
   140001785:	90                   	nop
   140001786:	90                   	nop
   140001787:	90                   	nop
   140001788:	90                   	nop
   140001789:	90                   	nop
   14000178a:	90                   	nop
   14000178b:	90                   	nop
   14000178c:	90                   	nop
   14000178d:	90                   	nop
   14000178e:	90                   	nop
   14000178f:	90                   	nop

0000000140001790 <__do_global_dtors>:
   140001790:	55                   	push   rbp
   140001791:	48 89 e5             	mov    rbp,rsp
   140001794:	48 83 ec 20          	sub    rsp,0x20
   140001798:	eb 1e                	jmp    1400017b8 <__do_global_dtors+0x28>
   14000179a:	48 8b 05 7f 88 00 00 	mov    rax,QWORD PTR [rip+0x887f]        # 14000a020 <p.0>
   1400017a1:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017a4:	ff d0                	call   rax
   1400017a6:	48 8b 05 73 88 00 00 	mov    rax,QWORD PTR [rip+0x8873]        # 14000a020 <p.0>
   1400017ad:	48 83 c0 08          	add    rax,0x8
   1400017b1:	48 89 05 68 88 00 00 	mov    QWORD PTR [rip+0x8868],rax        # 14000a020 <p.0>
   1400017b8:	48 8b 05 61 88 00 00 	mov    rax,QWORD PTR [rip+0x8861]        # 14000a020 <p.0>
   1400017bf:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017c2:	48 85 c0             	test   rax,rax
   1400017c5:	75 d3                	jne    14000179a <__do_global_dtors+0xa>
   1400017c7:	90                   	nop
   1400017c8:	90                   	nop
   1400017c9:	48 83 c4 20          	add    rsp,0x20
   1400017cd:	5d                   	pop    rbp
   1400017ce:	c3                   	ret

00000001400017cf <__do_global_ctors>:
   1400017cf:	55                   	push   rbp
   1400017d0:	48 89 e5             	mov    rbp,rsp
   1400017d3:	48 83 ec 30          	sub    rsp,0x30
   1400017d7:	48 8b 05 92 9d 00 00 	mov    rax,QWORD PTR [rip+0x9d92]        # 14000b570 <.refptr.__CTOR_LIST__>
   1400017de:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017e1:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400017e4:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
   1400017e8:	75 25                	jne    14000180f <__do_global_ctors+0x40>
   1400017ea:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400017f1:	eb 04                	jmp    1400017f7 <__do_global_ctors+0x28>
   1400017f3:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   1400017f7:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400017fa:	8d 50 01             	lea    edx,[rax+0x1]
   1400017fd:	48 8b 05 6c 9d 00 00 	mov    rax,QWORD PTR [rip+0x9d6c]        # 14000b570 <.refptr.__CTOR_LIST__>
   140001804:	89 d2                	mov    edx,edx
   140001806:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   14000180a:	48 85 c0             	test   rax,rax
   14000180d:	75 e4                	jne    1400017f3 <__do_global_ctors+0x24>
   14000180f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001812:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140001815:	eb 14                	jmp    14000182b <__do_global_ctors+0x5c>
   140001817:	48 8b 05 52 9d 00 00 	mov    rax,QWORD PTR [rip+0x9d52]        # 14000b570 <.refptr.__CTOR_LIST__>
   14000181e:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140001821:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   140001825:	ff d0                	call   rax
   140001827:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   14000182b:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   14000182f:	75 e6                	jne    140001817 <__do_global_ctors+0x48>
   140001831:	48 8d 05 58 ff ff ff 	lea    rax,[rip+0xffffffffffffff58]        # 140001790 <__do_global_dtors>
   140001838:	48 89 c1             	mov    rcx,rax
   14000183b:	e8 ef fd ff ff       	call   14000162f <atexit>
   140001840:	90                   	nop
   140001841:	48 83 c4 30          	add    rsp,0x30
   140001845:	5d                   	pop    rbp
   140001846:	c3                   	ret

0000000140001847 <__main>:
   140001847:	55                   	push   rbp
   140001848:	48 89 e5             	mov    rbp,rsp
   14000184b:	48 83 ec 20          	sub    rsp,0x20
   14000184f:	8b 05 2b d8 00 00    	mov    eax,DWORD PTR [rip+0xd82b]        # 14000f080 <initialized>
   140001855:	85 c0                	test   eax,eax
   140001857:	75 0f                	jne    140001868 <__main+0x21>
   140001859:	c7 05 1d d8 00 00 01 	mov    DWORD PTR [rip+0xd81d],0x1        # 14000f080 <initialized>
   140001860:	00 00 00 
   140001863:	e8 67 ff ff ff       	call   1400017cf <__do_global_ctors>
   140001868:	90                   	nop
   140001869:	48 83 c4 20          	add    rsp,0x20
   14000186d:	5d                   	pop    rbp
   14000186e:	c3                   	ret
   14000186f:	90                   	nop

0000000140001870 <_setargv>:
   140001870:	55                   	push   rbp
   140001871:	48 89 e5             	mov    rbp,rsp
   140001874:	b8 00 00 00 00       	mov    eax,0x0
   140001879:	5d                   	pop    rbp
   14000187a:	c3                   	ret
   14000187b:	90                   	nop
   14000187c:	90                   	nop
   14000187d:	90                   	nop
   14000187e:	90                   	nop
   14000187f:	90                   	nop

0000000140001880 <__dyn_tls_init>:
   140001880:	55                   	push   rbp
   140001881:	48 89 e5             	mov    rbp,rsp
   140001884:	48 83 ec 30          	sub    rsp,0x30
   140001888:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000188c:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   14000188f:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001893:	48 8b 05 b6 9c 00 00 	mov    rax,QWORD PTR [rip+0x9cb6]        # 14000b550 <.refptr._CRT_MT>
   14000189a:	8b 00                	mov    eax,DWORD PTR [rax]
   14000189c:	83 f8 02             	cmp    eax,0x2
   14000189f:	74 0d                	je     1400018ae <__dyn_tls_init+0x2e>
   1400018a1:	48 8b 05 a8 9c 00 00 	mov    rax,QWORD PTR [rip+0x9ca8]        # 14000b550 <.refptr._CRT_MT>
   1400018a8:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   1400018ae:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   1400018b2:	74 1e                	je     1400018d2 <__dyn_tls_init+0x52>
   1400018b4:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   1400018b8:	75 5b                	jne    140001915 <__dyn_tls_init+0x95>
   1400018ba:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   1400018be:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   1400018c1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400018c5:	49 89 c8             	mov    r8,rcx
   1400018c8:	48 89 c1             	mov    rcx,rax
   1400018cb:	e8 d1 11 00 00       	call   140002aa1 <__mingw_TLScallback>
   1400018d0:	eb 43                	jmp    140001915 <__dyn_tls_init+0x95>
   1400018d2:	48 8d 05 ff 9f 00 00 	lea    rax,[rip+0x9fff]        # 14000b8d8 <___crt_xd_start__>
   1400018d9:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400018dd:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   1400018e2:	eb 22                	jmp    140001906 <__dyn_tls_init+0x86>
   1400018e4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400018e8:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400018ec:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400018f0:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400018f3:	48 85 c0             	test   rax,rax
   1400018f6:	74 09                	je     140001901 <__dyn_tls_init+0x81>
   1400018f8:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400018fc:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400018ff:	ff d0                	call   rax
   140001901:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001906:	48 8d 05 d3 9f 00 00 	lea    rax,[rip+0x9fd3]        # 14000b8e0 <__xd_z>
   14000190d:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140001911:	75 d1                	jne    1400018e4 <__dyn_tls_init+0x64>
   140001913:	eb 01                	jmp    140001916 <__dyn_tls_init+0x96>
   140001915:	90                   	nop
   140001916:	48 83 c4 30          	add    rsp,0x30
   14000191a:	5d                   	pop    rbp
   14000191b:	c3                   	ret

000000014000191c <__tlregdtor>:
   14000191c:	55                   	push   rbp
   14000191d:	48 89 e5             	mov    rbp,rsp
   140001920:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001924:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140001929:	75 07                	jne    140001932 <__tlregdtor+0x16>
   14000192b:	b8 00 00 00 00       	mov    eax,0x0
   140001930:	eb 05                	jmp    140001937 <__tlregdtor+0x1b>
   140001932:	b8 00 00 00 00       	mov    eax,0x0
   140001937:	5d                   	pop    rbp
   140001938:	c3                   	ret

0000000140001939 <__dyn_tls_dtor>:
   140001939:	55                   	push   rbp
   14000193a:	48 89 e5             	mov    rbp,rsp
   14000193d:	48 83 ec 20          	sub    rsp,0x20
   140001941:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001945:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001948:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   14000194c:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140001950:	74 06                	je     140001958 <__dyn_tls_dtor+0x1f>
   140001952:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140001956:	75 18                	jne    140001970 <__dyn_tls_dtor+0x37>
   140001958:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   14000195c:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   14000195f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001963:	49 89 c8             	mov    r8,rcx
   140001966:	48 89 c1             	mov    rcx,rax
   140001969:	e8 33 11 00 00       	call   140002aa1 <__mingw_TLScallback>
   14000196e:	eb 01                	jmp    140001971 <__dyn_tls_dtor+0x38>
   140001970:	90                   	nop
   140001971:	48 83 c4 20          	add    rsp,0x20
   140001975:	5d                   	pop    rbp
   140001976:	c3                   	ret
   140001977:	90                   	nop
   140001978:	90                   	nop
   140001979:	90                   	nop
   14000197a:	90                   	nop
   14000197b:	90                   	nop
   14000197c:	90                   	nop
   14000197d:	90                   	nop
   14000197e:	90                   	nop
   14000197f:	90                   	nop

0000000140001980 <_matherr>:
   140001980:	55                   	push   rbp
   140001981:	53                   	push   rbx
   140001982:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140001989:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   14000198e:	0f 29 75 00          	movaps XMMWORD PTR [rbp+0x0],xmm6
   140001992:	0f 29 7d 10          	movaps XMMWORD PTR [rbp+0x10],xmm7
   140001996:	44 0f 29 45 20       	movaps XMMWORD PTR [rbp+0x20],xmm8
   14000199b:	48 89 4d 50          	mov    QWORD PTR [rbp+0x50],rcx
   14000199f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   1400019a3:	8b 00                	mov    eax,DWORD PTR [rax]
   1400019a5:	83 f8 06             	cmp    eax,0x6
   1400019a8:	74 56                	je     140001a00 <_matherr+0x80>
   1400019aa:	83 f8 06             	cmp    eax,0x6
   1400019ad:	7f 78                	jg     140001a27 <_matherr+0xa7>
   1400019af:	83 f8 05             	cmp    eax,0x5
   1400019b2:	74 59                	je     140001a0d <_matherr+0x8d>
   1400019b4:	83 f8 05             	cmp    eax,0x5
   1400019b7:	7f 6e                	jg     140001a27 <_matherr+0xa7>
   1400019b9:	83 f8 04             	cmp    eax,0x4
   1400019bc:	74 5c                	je     140001a1a <_matherr+0x9a>
   1400019be:	83 f8 04             	cmp    eax,0x4
   1400019c1:	7f 64                	jg     140001a27 <_matherr+0xa7>
   1400019c3:	83 f8 03             	cmp    eax,0x3
   1400019c6:	74 2b                	je     1400019f3 <_matherr+0x73>
   1400019c8:	83 f8 03             	cmp    eax,0x3
   1400019cb:	7f 5a                	jg     140001a27 <_matherr+0xa7>
   1400019cd:	83 f8 01             	cmp    eax,0x1
   1400019d0:	74 07                	je     1400019d9 <_matherr+0x59>
   1400019d2:	83 f8 02             	cmp    eax,0x2
   1400019d5:	74 0f                	je     1400019e6 <_matherr+0x66>
   1400019d7:	eb 4e                	jmp    140001a27 <_matherr+0xa7>
   1400019d9:	48 8d 05 c0 96 00 00 	lea    rax,[rip+0x96c0]        # 14000b0a0 <.rdata>
   1400019e0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019e4:	eb 4d                	jmp    140001a33 <_matherr+0xb3>
   1400019e6:	48 8d 05 d2 96 00 00 	lea    rax,[rip+0x96d2]        # 14000b0bf <.rdata+0x1f>
   1400019ed:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019f1:	eb 40                	jmp    140001a33 <_matherr+0xb3>
   1400019f3:	48 8d 05 e6 96 00 00 	lea    rax,[rip+0x96e6]        # 14000b0e0 <.rdata+0x40>
   1400019fa:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019fe:	eb 33                	jmp    140001a33 <_matherr+0xb3>
   140001a00:	48 8d 05 f9 96 00 00 	lea    rax,[rip+0x96f9]        # 14000b100 <.rdata+0x60>
   140001a07:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a0b:	eb 26                	jmp    140001a33 <_matherr+0xb3>
   140001a0d:	48 8d 05 14 97 00 00 	lea    rax,[rip+0x9714]        # 14000b128 <.rdata+0x88>
   140001a14:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a18:	eb 19                	jmp    140001a33 <_matherr+0xb3>
   140001a1a:	48 8d 05 2f 97 00 00 	lea    rax,[rip+0x972f]        # 14000b150 <.rdata+0xb0>
   140001a21:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a25:	eb 0c                	jmp    140001a33 <_matherr+0xb3>
   140001a27:	48 8d 05 58 97 00 00 	lea    rax,[rip+0x9758]        # 14000b186 <.rdata+0xe6>
   140001a2e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a32:	90                   	nop
   140001a33:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a37:	f2 44 0f 10 40 20    	movsd  xmm8,QWORD PTR [rax+0x20]
   140001a3d:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a41:	f2 0f 10 78 18       	movsd  xmm7,QWORD PTR [rax+0x18]
   140001a46:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a4a:	f2 0f 10 70 10       	movsd  xmm6,QWORD PTR [rax+0x10]
   140001a4f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a53:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
   140001a57:	b9 02 00 00 00       	mov    ecx,0x2
   140001a5c:	e8 2f 75 00 00       	call   140008f90 <__acrt_iob_func>
   140001a61:	48 89 c1             	mov    rcx,rax
   140001a64:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140001a68:	48 8d 05 29 97 00 00 	lea    rax,[rip+0x9729]        # 14000b198 <.rdata+0xf8>
   140001a6f:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001a76:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001a7c:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001a82:	49 89 d9             	mov    r9,rbx
   140001a85:	49 89 d0             	mov    r8,rdx
   140001a88:	48 89 c2             	mov    rdx,rax
   140001a8b:	e8 30 7b 00 00       	call   1400095c0 <fprintf>
   140001a90:	b8 00 00 00 00       	mov    eax,0x0
   140001a95:	0f 28 75 00          	movaps xmm6,XMMWORD PTR [rbp+0x0]
   140001a99:	0f 28 7d 10          	movaps xmm7,XMMWORD PTR [rbp+0x10]
   140001a9d:	44 0f 28 45 20       	movaps xmm8,XMMWORD PTR [rbp+0x20]
   140001aa2:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140001aa9:	5b                   	pop    rbx
   140001aaa:	5d                   	pop    rbp
   140001aab:	c3                   	ret
   140001aac:	90                   	nop
   140001aad:	90                   	nop
   140001aae:	90                   	nop
   140001aaf:	90                   	nop

0000000140001ab0 <__report_error>:
   140001ab0:	55                   	push   rbp
   140001ab1:	53                   	push   rbx
   140001ab2:	48 83 ec 38          	sub    rsp,0x38
   140001ab6:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140001abb:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140001abf:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001ac3:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140001ac7:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140001acb:	48 8d 45 28          	lea    rax,[rbp+0x28]
   140001acf:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001ad3:	b9 02 00 00 00       	mov    ecx,0x2
   140001ad8:	e8 b3 74 00 00       	call   140008f90 <__acrt_iob_func>
   140001add:	48 89 c1             	mov    rcx,rax
   140001ae0:	48 8d 05 e9 96 00 00 	lea    rax,[rip+0x96e9]        # 14000b1d0 <.rdata>
   140001ae7:	48 89 c2             	mov    rdx,rax
   140001aea:	e8 d1 7a 00 00       	call   1400095c0 <fprintf>
   140001aef:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   140001af3:	b9 02 00 00 00       	mov    ecx,0x2
   140001af8:	e8 93 74 00 00       	call   140008f90 <__acrt_iob_func>
   140001afd:	48 89 c1             	mov    rcx,rax
   140001b00:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001b04:	49 89 d8             	mov    r8,rbx
   140001b07:	48 89 c2             	mov    rdx,rax
   140001b0a:	e8 09 7b 00 00       	call   140009618 <vfprintf>
   140001b0f:	e8 8c 7a 00 00       	call   1400095a0 <abort>
   140001b14:	90                   	nop

0000000140001b15 <mark_section_writable>:
   140001b15:	55                   	push   rbp
   140001b16:	48 89 e5             	mov    rbp,rsp
   140001b19:	48 83 ec 60          	sub    rsp,0x60
   140001b1d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001b21:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001b28:	e9 82 00 00 00       	jmp    140001baf <mark_section_writable+0x9a>
   140001b2d:	48 8b 0d ac d5 00 00 	mov    rcx,QWORD PTR [rip+0xd5ac]        # 14000f0e0 <the_secs>
   140001b34:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b37:	48 63 d0             	movsxd rdx,eax
   140001b3a:	48 89 d0             	mov    rax,rdx
   140001b3d:	48 c1 e0 02          	shl    rax,0x2
   140001b41:	48 01 d0             	add    rax,rdx
   140001b44:	48 c1 e0 03          	shl    rax,0x3
   140001b48:	48 01 c8             	add    rax,rcx
   140001b4b:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001b4f:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001b53:	72 56                	jb     140001bab <mark_section_writable+0x96>
   140001b55:	48 8b 0d 84 d5 00 00 	mov    rcx,QWORD PTR [rip+0xd584]        # 14000f0e0 <the_secs>
   140001b5c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b5f:	48 63 d0             	movsxd rdx,eax
   140001b62:	48 89 d0             	mov    rax,rdx
   140001b65:	48 c1 e0 02          	shl    rax,0x2
   140001b69:	48 01 d0             	add    rax,rdx
   140001b6c:	48 c1 e0 03          	shl    rax,0x3
   140001b70:	48 01 c8             	add    rax,rcx
   140001b73:	48 8b 48 18          	mov    rcx,QWORD PTR [rax+0x18]
   140001b77:	4c 8b 05 62 d5 00 00 	mov    r8,QWORD PTR [rip+0xd562]        # 14000f0e0 <the_secs>
   140001b7e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b81:	48 63 d0             	movsxd rdx,eax
   140001b84:	48 89 d0             	mov    rax,rdx
   140001b87:	48 c1 e0 02          	shl    rax,0x2
   140001b8b:	48 01 d0             	add    rax,rdx
   140001b8e:	48 c1 e0 03          	shl    rax,0x3
   140001b92:	4c 01 c0             	add    rax,r8
   140001b95:	48 8b 40 20          	mov    rax,QWORD PTR [rax+0x20]
   140001b99:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001b9c:	89 c0                	mov    eax,eax
   140001b9e:	48 01 c8             	add    rax,rcx
   140001ba1:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001ba5:	0f 82 41 02 00 00    	jb     140001dec <mark_section_writable+0x2d7>
   140001bab:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001baf:	8b 05 33 d5 00 00    	mov    eax,DWORD PTR [rip+0xd533]        # 14000f0e8 <maxSections>
   140001bb5:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001bb8:	0f 8c 6f ff ff ff    	jl     140001b2d <mark_section_writable+0x18>
   140001bbe:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001bc2:	48 89 c1             	mov    rcx,rax
   140001bc5:	e8 c1 11 00 00       	call   140002d8b <__mingw_GetSectionForAddress>
   140001bca:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001bce:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001bd3:	75 13                	jne    140001be8 <mark_section_writable+0xd3>
   140001bd5:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001bd9:	48 8d 0d 10 96 00 00 	lea    rcx,[rip+0x9610]        # 14000b1f0 <.rdata+0x20>
   140001be0:	48 89 c2             	mov    rdx,rax
   140001be3:	e8 c8 fe ff ff       	call   140001ab0 <__report_error>
   140001be8:	48 8b 0d f1 d4 00 00 	mov    rcx,QWORD PTR [rip+0xd4f1]        # 14000f0e0 <the_secs>
   140001bef:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001bf2:	48 63 d0             	movsxd rdx,eax
   140001bf5:	48 89 d0             	mov    rax,rdx
   140001bf8:	48 c1 e0 02          	shl    rax,0x2
   140001bfc:	48 01 d0             	add    rax,rdx
   140001bff:	48 c1 e0 03          	shl    rax,0x3
   140001c03:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001c07:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c0b:	48 89 42 20          	mov    QWORD PTR [rdx+0x20],rax
   140001c0f:	48 8b 0d ca d4 00 00 	mov    rcx,QWORD PTR [rip+0xd4ca]        # 14000f0e0 <the_secs>
   140001c16:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c19:	48 63 d0             	movsxd rdx,eax
   140001c1c:	48 89 d0             	mov    rax,rdx
   140001c1f:	48 c1 e0 02          	shl    rax,0x2
   140001c23:	48 01 d0             	add    rax,rdx
   140001c26:	48 c1 e0 03          	shl    rax,0x3
   140001c2a:	48 01 c8             	add    rax,rcx
   140001c2d:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001c33:	e8 9f 12 00 00       	call   140002ed7 <_GetPEImageBase>
   140001c38:	48 89 c1             	mov    rcx,rax
   140001c3b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c3f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140001c42:	41 89 c1             	mov    r9d,eax
   140001c45:	4c 8b 05 94 d4 00 00 	mov    r8,QWORD PTR [rip+0xd494]        # 14000f0e0 <the_secs>
   140001c4c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c4f:	48 63 d0             	movsxd rdx,eax
   140001c52:	48 89 d0             	mov    rax,rdx
   140001c55:	48 c1 e0 02          	shl    rax,0x2
   140001c59:	48 01 d0             	add    rax,rdx
   140001c5c:	48 c1 e0 03          	shl    rax,0x3
   140001c60:	4c 01 c0             	add    rax,r8
   140001c63:	4a 8d 14 09          	lea    rdx,[rcx+r9*1]
   140001c67:	48 89 50 18          	mov    QWORD PTR [rax+0x18],rdx
   140001c6b:	48 8b 0d 6e d4 00 00 	mov    rcx,QWORD PTR [rip+0xd46e]        # 14000f0e0 <the_secs>
   140001c72:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c75:	48 63 d0             	movsxd rdx,eax
   140001c78:	48 89 d0             	mov    rax,rdx
   140001c7b:	48 c1 e0 02          	shl    rax,0x2
   140001c7f:	48 01 d0             	add    rax,rdx
   140001c82:	48 c1 e0 03          	shl    rax,0x3
   140001c86:	48 01 c8             	add    rax,rcx
   140001c89:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001c8d:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140001c91:	41 b8 30 00 00 00    	mov    r8d,0x30
   140001c97:	48 89 c1             	mov    rcx,rax
   140001c9a:	48 8b 05 bf e5 00 00 	mov    rax,QWORD PTR [rip+0xe5bf]        # 140010260 <__imp_VirtualQuery>
   140001ca1:	ff d0                	call   rax
   140001ca3:	48 85 c0             	test   rax,rax
   140001ca6:	75 3f                	jne    140001ce7 <mark_section_writable+0x1d2>
   140001ca8:	48 8b 0d 31 d4 00 00 	mov    rcx,QWORD PTR [rip+0xd431]        # 14000f0e0 <the_secs>
   140001caf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001cb2:	48 63 d0             	movsxd rdx,eax
   140001cb5:	48 89 d0             	mov    rax,rdx
   140001cb8:	48 c1 e0 02          	shl    rax,0x2
   140001cbc:	48 01 d0             	add    rax,rdx
   140001cbf:	48 c1 e0 03          	shl    rax,0x3
   140001cc3:	48 01 c8             	add    rax,rcx
   140001cc6:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
   140001cca:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001cce:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001cd1:	89 c1                	mov    ecx,eax
   140001cd3:	48 8d 05 36 95 00 00 	lea    rax,[rip+0x9536]        # 14000b210 <.rdata+0x40>
   140001cda:	49 89 d0             	mov    r8,rdx
   140001cdd:	89 ca                	mov    edx,ecx
   140001cdf:	48 89 c1             	mov    rcx,rax
   140001ce2:	e8 c9 fd ff ff       	call   140001ab0 <__report_error>
   140001ce7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001cea:	83 f8 40             	cmp    eax,0x40
   140001ced:	0f 84 e8 00 00 00    	je     140001ddb <mark_section_writable+0x2c6>
   140001cf3:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001cf6:	83 f8 04             	cmp    eax,0x4
   140001cf9:	0f 84 dc 00 00 00    	je     140001ddb <mark_section_writable+0x2c6>
   140001cff:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d02:	3d 80 00 00 00       	cmp    eax,0x80
   140001d07:	0f 84 ce 00 00 00    	je     140001ddb <mark_section_writable+0x2c6>
   140001d0d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d10:	83 f8 08             	cmp    eax,0x8
   140001d13:	0f 84 c2 00 00 00    	je     140001ddb <mark_section_writable+0x2c6>
   140001d19:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d1c:	83 f8 02             	cmp    eax,0x2
   140001d1f:	75 09                	jne    140001d2a <mark_section_writable+0x215>
   140001d21:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140001d28:	eb 07                	jmp    140001d31 <mark_section_writable+0x21c>
   140001d2a:	c7 45 f8 40 00 00 00 	mov    DWORD PTR [rbp-0x8],0x40
   140001d31:	48 8b 0d a8 d3 00 00 	mov    rcx,QWORD PTR [rip+0xd3a8]        # 14000f0e0 <the_secs>
   140001d38:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d3b:	48 63 d0             	movsxd rdx,eax
   140001d3e:	48 89 d0             	mov    rax,rdx
   140001d41:	48 c1 e0 02          	shl    rax,0x2
   140001d45:	48 01 d0             	add    rax,rdx
   140001d48:	48 c1 e0 03          	shl    rax,0x3
   140001d4c:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d50:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001d54:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   140001d58:	48 8b 0d 81 d3 00 00 	mov    rcx,QWORD PTR [rip+0xd381]        # 14000f0e0 <the_secs>
   140001d5f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d62:	48 63 d0             	movsxd rdx,eax
   140001d65:	48 89 d0             	mov    rax,rdx
   140001d68:	48 c1 e0 02          	shl    rax,0x2
   140001d6c:	48 01 d0             	add    rax,rdx
   140001d6f:	48 c1 e0 03          	shl    rax,0x3
   140001d73:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d77:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140001d7b:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   140001d7f:	48 8b 0d 5a d3 00 00 	mov    rcx,QWORD PTR [rip+0xd35a]        # 14000f0e0 <the_secs>
   140001d86:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d89:	48 63 d0             	movsxd rdx,eax
   140001d8c:	48 89 d0             	mov    rax,rdx
   140001d8f:	48 c1 e0 02          	shl    rax,0x2
   140001d93:	48 01 d0             	add    rax,rdx
   140001d96:	48 c1 e0 03          	shl    rax,0x3
   140001d9a:	48 01 c8             	add    rax,rcx
   140001d9d:	49 89 c0             	mov    r8,rax
   140001da0:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   140001da4:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001da8:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   140001dab:	4d 89 c1             	mov    r9,r8
   140001dae:	41 89 c8             	mov    r8d,ecx
   140001db1:	48 89 c1             	mov    rcx,rax
   140001db4:	48 8b 05 9d e4 00 00 	mov    rax,QWORD PTR [rip+0xe49d]        # 140010258 <__imp_VirtualProtect>
   140001dbb:	ff d0                	call   rax
   140001dbd:	85 c0                	test   eax,eax
   140001dbf:	75 1a                	jne    140001ddb <mark_section_writable+0x2c6>
   140001dc1:	48 8b 05 40 e4 00 00 	mov    rax,QWORD PTR [rip+0xe440]        # 140010208 <__imp_GetLastError>
   140001dc8:	ff d0                	call   rax
   140001dca:	89 c2                	mov    edx,eax
   140001dcc:	48 8d 05 75 94 00 00 	lea    rax,[rip+0x9475]        # 14000b248 <.rdata+0x78>
   140001dd3:	48 89 c1             	mov    rcx,rax
   140001dd6:	e8 d5 fc ff ff       	call   140001ab0 <__report_error>
   140001ddb:	8b 05 07 d3 00 00    	mov    eax,DWORD PTR [rip+0xd307]        # 14000f0e8 <maxSections>
   140001de1:	83 c0 01             	add    eax,0x1
   140001de4:	89 05 fe d2 00 00    	mov    DWORD PTR [rip+0xd2fe],eax        # 14000f0e8 <maxSections>
   140001dea:	eb 01                	jmp    140001ded <mark_section_writable+0x2d8>
   140001dec:	90                   	nop
   140001ded:	48 83 c4 60          	add    rsp,0x60
   140001df1:	5d                   	pop    rbp
   140001df2:	c3                   	ret

0000000140001df3 <restore_modified_sections>:
   140001df3:	55                   	push   rbp
   140001df4:	48 89 e5             	mov    rbp,rsp
   140001df7:	48 83 ec 30          	sub    rsp,0x30
   140001dfb:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001e02:	e9 ad 00 00 00       	jmp    140001eb4 <restore_modified_sections+0xc1>
   140001e07:	48 8b 0d d2 d2 00 00 	mov    rcx,QWORD PTR [rip+0xd2d2]        # 14000f0e0 <the_secs>
   140001e0e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e11:	48 63 d0             	movsxd rdx,eax
   140001e14:	48 89 d0             	mov    rax,rdx
   140001e17:	48 c1 e0 02          	shl    rax,0x2
   140001e1b:	48 01 d0             	add    rax,rdx
   140001e1e:	48 c1 e0 03          	shl    rax,0x3
   140001e22:	48 01 c8             	add    rax,rcx
   140001e25:	8b 00                	mov    eax,DWORD PTR [rax]
   140001e27:	85 c0                	test   eax,eax
   140001e29:	0f 84 80 00 00 00    	je     140001eaf <restore_modified_sections+0xbc>
   140001e2f:	48 8b 0d aa d2 00 00 	mov    rcx,QWORD PTR [rip+0xd2aa]        # 14000f0e0 <the_secs>
   140001e36:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e39:	48 63 d0             	movsxd rdx,eax
   140001e3c:	48 89 d0             	mov    rax,rdx
   140001e3f:	48 c1 e0 02          	shl    rax,0x2
   140001e43:	48 01 d0             	add    rax,rdx
   140001e46:	48 c1 e0 03          	shl    rax,0x3
   140001e4a:	48 01 c8             	add    rax,rcx
   140001e4d:	44 8b 10             	mov    r10d,DWORD PTR [rax]
   140001e50:	48 8b 0d 89 d2 00 00 	mov    rcx,QWORD PTR [rip+0xd289]        # 14000f0e0 <the_secs>
   140001e57:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e5a:	48 63 d0             	movsxd rdx,eax
   140001e5d:	48 89 d0             	mov    rax,rdx
   140001e60:	48 c1 e0 02          	shl    rax,0x2
   140001e64:	48 01 d0             	add    rax,rdx
   140001e67:	48 c1 e0 03          	shl    rax,0x3
   140001e6b:	48 01 c8             	add    rax,rcx
   140001e6e:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   140001e72:	4c 8b 05 67 d2 00 00 	mov    r8,QWORD PTR [rip+0xd267]        # 14000f0e0 <the_secs>
   140001e79:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e7c:	48 63 d0             	movsxd rdx,eax
   140001e7f:	48 89 d0             	mov    rax,rdx
   140001e82:	48 c1 e0 02          	shl    rax,0x2
   140001e86:	48 01 d0             	add    rax,rdx
   140001e89:	48 c1 e0 03          	shl    rax,0x3
   140001e8d:	4c 01 c0             	add    rax,r8
   140001e90:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   140001e94:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   140001e98:	49 89 d1             	mov    r9,rdx
   140001e9b:	45 89 d0             	mov    r8d,r10d
   140001e9e:	48 89 ca             	mov    rdx,rcx
   140001ea1:	48 89 c1             	mov    rcx,rax
   140001ea4:	48 8b 05 ad e3 00 00 	mov    rax,QWORD PTR [rip+0xe3ad]        # 140010258 <__imp_VirtualProtect>
   140001eab:	ff d0                	call   rax
   140001ead:	eb 01                	jmp    140001eb0 <restore_modified_sections+0xbd>
   140001eaf:	90                   	nop
   140001eb0:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001eb4:	8b 05 2e d2 00 00    	mov    eax,DWORD PTR [rip+0xd22e]        # 14000f0e8 <maxSections>
   140001eba:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001ebd:	0f 8c 44 ff ff ff    	jl     140001e07 <restore_modified_sections+0x14>
   140001ec3:	90                   	nop
   140001ec4:	90                   	nop
   140001ec5:	48 83 c4 30          	add    rsp,0x30
   140001ec9:	5d                   	pop    rbp
   140001eca:	c3                   	ret

0000000140001ecb <__write_memory>:
   140001ecb:	55                   	push   rbp
   140001ecc:	48 89 e5             	mov    rbp,rsp
   140001ecf:	48 83 ec 20          	sub    rsp,0x20
   140001ed3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001ed7:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001edb:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001edf:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140001ee4:	74 25                	je     140001f0b <__write_memory+0x40>
   140001ee6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001eea:	48 89 c1             	mov    rcx,rax
   140001eed:	e8 23 fc ff ff       	call   140001b15 <mark_section_writable>
   140001ef2:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001ef6:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140001efa:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001efe:	49 89 c8             	mov    r8,rcx
   140001f01:	48 89 c1             	mov    rcx,rax
   140001f04:	e8 df 76 00 00       	call   1400095e8 <memcpy>
   140001f09:	eb 01                	jmp    140001f0c <__write_memory+0x41>
   140001f0b:	90                   	nop
   140001f0c:	48 83 c4 20          	add    rsp,0x20
   140001f10:	5d                   	pop    rbp
   140001f11:	c3                   	ret

0000000140001f12 <do_pseudo_reloc>:
   140001f12:	55                   	push   rbp
   140001f13:	48 89 e5             	mov    rbp,rsp
   140001f16:	48 83 c4 80          	add    rsp,0xffffffffffffff80
   140001f1a:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001f1e:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001f22:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001f26:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140001f2a:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   140001f2e:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001f32:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f36:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001f3a:	48 83 7d e0 07       	cmp    QWORD PTR [rbp-0x20],0x7
   140001f3f:	0f 8e 44 03 00 00    	jle    140002289 <do_pseudo_reloc+0x377>
   140001f45:	48 83 7d e0 0b       	cmp    QWORD PTR [rbp-0x20],0xb
   140001f4a:	7e 25                	jle    140001f71 <do_pseudo_reloc+0x5f>
   140001f4c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f50:	8b 00                	mov    eax,DWORD PTR [rax]
   140001f52:	85 c0                	test   eax,eax
   140001f54:	75 1b                	jne    140001f71 <do_pseudo_reloc+0x5f>
   140001f56:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f5a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f5d:	85 c0                	test   eax,eax
   140001f5f:	75 10                	jne    140001f71 <do_pseudo_reloc+0x5f>
   140001f61:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f65:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001f68:	85 c0                	test   eax,eax
   140001f6a:	75 05                	jne    140001f71 <do_pseudo_reloc+0x5f>
   140001f6c:	48 83 45 f8 0c       	add    QWORD PTR [rbp-0x8],0xc
   140001f71:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f75:	8b 00                	mov    eax,DWORD PTR [rax]
   140001f77:	85 c0                	test   eax,eax
   140001f79:	75 0b                	jne    140001f86 <do_pseudo_reloc+0x74>
   140001f7b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f7f:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f82:	85 c0                	test   eax,eax
   140001f84:	74 59                	je     140001fdf <do_pseudo_reloc+0xcd>
   140001f86:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f8a:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140001f8e:	eb 40                	jmp    140001fd0 <do_pseudo_reloc+0xbe>
   140001f90:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001f94:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f97:	89 c2                	mov    edx,eax
   140001f99:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001f9d:	48 01 d0             	add    rax,rdx
   140001fa0:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001fa4:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001fa8:	8b 10                	mov    edx,DWORD PTR [rax]
   140001faa:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fae:	8b 00                	mov    eax,DWORD PTR [rax]
   140001fb0:	01 d0                	add    eax,edx
   140001fb2:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
   140001fb5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001fb9:	48 8d 55 b4          	lea    rdx,[rbp-0x4c]
   140001fbd:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001fc3:	48 89 c1             	mov    rcx,rax
   140001fc6:	e8 00 ff ff ff       	call   140001ecb <__write_memory>
   140001fcb:	48 83 45 e8 08       	add    QWORD PTR [rbp-0x18],0x8
   140001fd0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fd4:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140001fd8:	72 b6                	jb     140001f90 <do_pseudo_reloc+0x7e>
   140001fda:	e9 ab 02 00 00       	jmp    14000228a <do_pseudo_reloc+0x378>
   140001fdf:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fe3:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001fe6:	83 f8 01             	cmp    eax,0x1
   140001fe9:	74 18                	je     140002003 <do_pseudo_reloc+0xf1>
   140001feb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fef:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001ff2:	89 c2                	mov    edx,eax
   140001ff4:	48 8d 05 75 92 00 00 	lea    rax,[rip+0x9275]        # 14000b270 <.rdata+0xa0>
   140001ffb:	48 89 c1             	mov    rcx,rax
   140001ffe:	e8 ad fa ff ff       	call   140001ab0 <__report_error>
   140002003:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002007:	48 83 c0 0c          	add    rax,0xc
   14000200b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000200f:	e9 65 02 00 00       	jmp    140002279 <do_pseudo_reloc+0x367>
   140002014:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002018:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000201b:	89 c2                	mov    edx,eax
   14000201d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002021:	48 01 d0             	add    rax,rdx
   140002024:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002028:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000202c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000202e:	89 c2                	mov    edx,eax
   140002030:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002034:	48 01 d0             	add    rax,rdx
   140002037:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000203b:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000203f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002042:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002046:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000204a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000204d:	0f b6 c0             	movzx  eax,al
   140002050:	83 f8 40             	cmp    eax,0x40
   140002053:	0f 84 b6 00 00 00    	je     14000210f <do_pseudo_reloc+0x1fd>
   140002059:	83 f8 40             	cmp    eax,0x40
   14000205c:	0f 87 ba 00 00 00    	ja     14000211c <do_pseudo_reloc+0x20a>
   140002062:	83 f8 20             	cmp    eax,0x20
   140002065:	74 77                	je     1400020de <do_pseudo_reloc+0x1cc>
   140002067:	83 f8 20             	cmp    eax,0x20
   14000206a:	0f 87 ac 00 00 00    	ja     14000211c <do_pseudo_reloc+0x20a>
   140002070:	83 f8 08             	cmp    eax,0x8
   140002073:	74 0a                	je     14000207f <do_pseudo_reloc+0x16d>
   140002075:	83 f8 10             	cmp    eax,0x10
   140002078:	74 38                	je     1400020b2 <do_pseudo_reloc+0x1a0>
   14000207a:	e9 9d 00 00 00       	jmp    14000211c <do_pseudo_reloc+0x20a>
   14000207f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002083:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140002086:	0f b6 c0             	movzx  eax,al
   140002089:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000208d:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002091:	25 80 00 00 00       	and    eax,0x80
   140002096:	48 85 c0             	test   rax,rax
   140002099:	0f 84 9d 00 00 00    	je     14000213c <do_pseudo_reloc+0x22a>
   14000209f:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020a3:	48 0d 00 ff ff ff    	or     rax,0xffffffffffffff00
   1400020a9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020ad:	e9 8a 00 00 00       	jmp    14000213c <do_pseudo_reloc+0x22a>
   1400020b2:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020b6:	0f b7 00             	movzx  eax,WORD PTR [rax]
   1400020b9:	0f b7 c0             	movzx  eax,ax
   1400020bc:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020c0:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020c4:	25 00 80 00 00       	and    eax,0x8000
   1400020c9:	48 85 c0             	test   rax,rax
   1400020cc:	74 71                	je     14000213f <do_pseudo_reloc+0x22d>
   1400020ce:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020d2:	48 0d 00 00 ff ff    	or     rax,0xffffffffffff0000
   1400020d8:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020dc:	eb 61                	jmp    14000213f <do_pseudo_reloc+0x22d>
   1400020de:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020e2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400020e4:	89 c0                	mov    eax,eax
   1400020e6:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020ea:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020ee:	25 00 00 00 80       	and    eax,0x80000000
   1400020f3:	48 85 c0             	test   rax,rax
   1400020f6:	74 4a                	je     140002142 <do_pseudo_reloc+0x230>
   1400020f8:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020fc:	48 ba 00 00 00 00 ff 	movabs rdx,0xffffffff00000000
   140002103:	ff ff ff 
   140002106:	48 09 d0             	or     rax,rdx
   140002109:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000210d:	eb 33                	jmp    140002142 <do_pseudo_reloc+0x230>
   14000210f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002113:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002116:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000211a:	eb 27                	jmp    140002143 <do_pseudo_reloc+0x231>
   14000211c:	48 c7 45 b8 00 00 00 	mov    QWORD PTR [rbp-0x48],0x0
   140002123:	00 
   140002124:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002128:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000212b:	0f b6 c0             	movzx  eax,al
   14000212e:	48 8d 0d 73 91 00 00 	lea    rcx,[rip+0x9173]        # 14000b2a8 <.rdata+0xd8>
   140002135:	89 c2                	mov    edx,eax
   140002137:	e8 74 f9 ff ff       	call   140001ab0 <__report_error>
   14000213c:	90                   	nop
   14000213d:	eb 04                	jmp    140002143 <do_pseudo_reloc+0x231>
   14000213f:	90                   	nop
   140002140:	eb 01                	jmp    140002143 <do_pseudo_reloc+0x231>
   140002142:	90                   	nop
   140002143:	48 8b 4d b8          	mov    rcx,QWORD PTR [rbp-0x48]
   140002147:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000214b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000214d:	89 c2                	mov    edx,eax
   14000214f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002153:	48 01 c2             	add    rdx,rax
   140002156:	48 89 c8             	mov    rax,rcx
   140002159:	48 29 d0             	sub    rax,rdx
   14000215c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140002160:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   140002164:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140002168:	48 01 d0             	add    rax,rdx
   14000216b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000216f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002173:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002176:	25 ff 00 00 00       	and    eax,0xff
   14000217b:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   14000217e:	83 7d d4 3f          	cmp    DWORD PTR [rbp-0x2c],0x3f
   140002182:	77 67                	ja     1400021eb <do_pseudo_reloc+0x2d9>
   140002184:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140002187:	ba 01 00 00 00       	mov    edx,0x1
   14000218c:	89 c1                	mov    ecx,eax
   14000218e:	48 d3 e2             	shl    rdx,cl
   140002191:	48 89 d0             	mov    rax,rdx
   140002194:	48 83 e8 01          	sub    rax,0x1
   140002198:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   14000219c:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   14000219f:	83 e8 01             	sub    eax,0x1
   1400021a2:	48 c7 c2 ff ff ff ff 	mov    rdx,0xffffffffffffffff
   1400021a9:	89 c1                	mov    ecx,eax
   1400021ab:	48 d3 e2             	shl    rdx,cl
   1400021ae:	48 89 d0             	mov    rax,rdx
   1400021b1:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   1400021b5:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021b9:	48 39 45 c8          	cmp    QWORD PTR [rbp-0x38],rax
   1400021bd:	7c 0a                	jl     1400021c9 <do_pseudo_reloc+0x2b7>
   1400021bf:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021c3:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   1400021c7:	7e 22                	jle    1400021eb <do_pseudo_reloc+0x2d9>
   1400021c9:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   1400021cd:	4c 8b 4d d8          	mov    r9,QWORD PTR [rbp-0x28]
   1400021d1:	4c 8b 45 e0          	mov    r8,QWORD PTR [rbp-0x20]
   1400021d5:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400021d8:	48 8d 0d f9 90 00 00 	lea    rcx,[rip+0x90f9]        # 14000b2d8 <.rdata+0x108>
   1400021df:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   1400021e4:	89 c2                	mov    edx,eax
   1400021e6:	e8 c5 f8 ff ff       	call   140001ab0 <__report_error>
   1400021eb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400021ef:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400021f2:	0f b6 c0             	movzx  eax,al
   1400021f5:	83 f8 40             	cmp    eax,0x40
   1400021f8:	74 63                	je     14000225d <do_pseudo_reloc+0x34b>
   1400021fa:	83 f8 40             	cmp    eax,0x40
   1400021fd:	77 75                	ja     140002274 <do_pseudo_reloc+0x362>
   1400021ff:	83 f8 20             	cmp    eax,0x20
   140002202:	74 41                	je     140002245 <do_pseudo_reloc+0x333>
   140002204:	83 f8 20             	cmp    eax,0x20
   140002207:	77 6b                	ja     140002274 <do_pseudo_reloc+0x362>
   140002209:	83 f8 08             	cmp    eax,0x8
   14000220c:	74 07                	je     140002215 <do_pseudo_reloc+0x303>
   14000220e:	83 f8 10             	cmp    eax,0x10
   140002211:	74 1a                	je     14000222d <do_pseudo_reloc+0x31b>
   140002213:	eb 5f                	jmp    140002274 <do_pseudo_reloc+0x362>
   140002215:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002219:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000221d:	41 b8 01 00 00 00    	mov    r8d,0x1
   140002223:	48 89 c1             	mov    rcx,rax
   140002226:	e8 a0 fc ff ff       	call   140001ecb <__write_memory>
   14000222b:	eb 47                	jmp    140002274 <do_pseudo_reloc+0x362>
   14000222d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002231:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002235:	41 b8 02 00 00 00    	mov    r8d,0x2
   14000223b:	48 89 c1             	mov    rcx,rax
   14000223e:	e8 88 fc ff ff       	call   140001ecb <__write_memory>
   140002243:	eb 2f                	jmp    140002274 <do_pseudo_reloc+0x362>
   140002245:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002249:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000224d:	41 b8 04 00 00 00    	mov    r8d,0x4
   140002253:	48 89 c1             	mov    rcx,rax
   140002256:	e8 70 fc ff ff       	call   140001ecb <__write_memory>
   14000225b:	eb 17                	jmp    140002274 <do_pseudo_reloc+0x362>
   14000225d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002261:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002265:	41 b8 08 00 00 00    	mov    r8d,0x8
   14000226b:	48 89 c1             	mov    rcx,rax
   14000226e:	e8 58 fc ff ff       	call   140001ecb <__write_memory>
   140002273:	90                   	nop
   140002274:	48 83 45 f0 0c       	add    QWORD PTR [rbp-0x10],0xc
   140002279:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000227d:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140002281:	0f 82 8d fd ff ff    	jb     140002014 <do_pseudo_reloc+0x102>
   140002287:	eb 01                	jmp    14000228a <do_pseudo_reloc+0x378>
   140002289:	90                   	nop
   14000228a:	48 83 ec 80          	sub    rsp,0xffffffffffffff80
   14000228e:	5d                   	pop    rbp
   14000228f:	c3                   	ret

0000000140002290 <_pei386_runtime_relocator>:
   140002290:	55                   	push   rbp
   140002291:	48 89 e5             	mov    rbp,rsp
   140002294:	48 83 ec 30          	sub    rsp,0x30
   140002298:	8b 05 4e ce 00 00    	mov    eax,DWORD PTR [rip+0xce4e]        # 14000f0ec <was_init.0>
   14000229e:	85 c0                	test   eax,eax
   1400022a0:	0f 85 88 00 00 00    	jne    14000232e <_pei386_runtime_relocator+0x9e>
   1400022a6:	8b 05 40 ce 00 00    	mov    eax,DWORD PTR [rip+0xce40]        # 14000f0ec <was_init.0>
   1400022ac:	83 c0 01             	add    eax,0x1
   1400022af:	89 05 37 ce 00 00    	mov    DWORD PTR [rip+0xce37],eax        # 14000f0ec <was_init.0>
   1400022b5:	e8 21 0b 00 00       	call   140002ddb <__mingw_GetSectionCount>
   1400022ba:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400022bd:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400022c0:	48 63 d0             	movsxd rdx,eax
   1400022c3:	48 89 d0             	mov    rax,rdx
   1400022c6:	48 c1 e0 02          	shl    rax,0x2
   1400022ca:	48 01 d0             	add    rax,rdx
   1400022cd:	48 c1 e0 03          	shl    rax,0x3
   1400022d1:	48 83 c0 0f          	add    rax,0xf
   1400022d5:	48 c1 e8 04          	shr    rax,0x4
   1400022d9:	48 c1 e0 04          	shl    rax,0x4
   1400022dd:	e8 7e 0d 00 00       	call   140003060 <___chkstk_ms>
   1400022e2:	48 29 c4             	sub    rsp,rax
   1400022e5:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   1400022ea:	48 83 c0 0f          	add    rax,0xf
   1400022ee:	48 c1 e8 04          	shr    rax,0x4
   1400022f2:	48 c1 e0 04          	shl    rax,0x4
   1400022f6:	48 89 05 e3 cd 00 00 	mov    QWORD PTR [rip+0xcde3],rax        # 14000f0e0 <the_secs>
   1400022fd:	c7 05 e1 cd 00 00 00 	mov    DWORD PTR [rip+0xcde1],0x0        # 14000f0e8 <maxSections>
   140002304:	00 00 00 
   140002307:	48 8b 0d 72 92 00 00 	mov    rcx,QWORD PTR [rip+0x9272]        # 14000b580 <.refptr.__ImageBase>
   14000230e:	48 8b 15 7b 92 00 00 	mov    rdx,QWORD PTR [rip+0x927b]        # 14000b590 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   140002315:	48 8b 05 84 92 00 00 	mov    rax,QWORD PTR [rip+0x9284]        # 14000b5a0 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000231c:	49 89 c8             	mov    r8,rcx
   14000231f:	48 89 c1             	mov    rcx,rax
   140002322:	e8 eb fb ff ff       	call   140001f12 <do_pseudo_reloc>
   140002327:	e8 c7 fa ff ff       	call   140001df3 <restore_modified_sections>
   14000232c:	eb 01                	jmp    14000232f <_pei386_runtime_relocator+0x9f>
   14000232e:	90                   	nop
   14000232f:	48 89 ec             	mov    rsp,rbp
   140002332:	5d                   	pop    rbp
   140002333:	c3                   	ret
   140002334:	90                   	nop
   140002335:	90                   	nop
   140002336:	90                   	nop
   140002337:	90                   	nop
   140002338:	90                   	nop
   140002339:	90                   	nop
   14000233a:	90                   	nop
   14000233b:	90                   	nop
   14000233c:	90                   	nop
   14000233d:	90                   	nop
   14000233e:	90                   	nop
   14000233f:	90                   	nop

0000000140002340 <__mingw_raise_matherr>:
   140002340:	55                   	push   rbp
   140002341:	48 89 e5             	mov    rbp,rsp
   140002344:	48 83 ec 50          	sub    rsp,0x50
   140002348:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000234b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000234f:	f2 0f 11 55 20       	movsd  QWORD PTR [rbp+0x20],xmm2
   140002354:	f2 0f 11 5d 28       	movsd  QWORD PTR [rbp+0x28],xmm3
   140002359:	48 8b 05 90 cd 00 00 	mov    rax,QWORD PTR [rip+0xcd90]        # 14000f0f0 <stUserMathErr>
   140002360:	48 85 c0             	test   rax,rax
   140002363:	74 3e                	je     1400023a3 <__mingw_raise_matherr+0x63>
   140002365:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140002368:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   14000236b:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000236f:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002373:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   140002378:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   14000237d:	f2 0f 10 45 28       	movsd  xmm0,QWORD PTR [rbp+0x28]
   140002382:	f2 0f 11 45 e8       	movsd  QWORD PTR [rbp-0x18],xmm0
   140002387:	f2 0f 10 45 30       	movsd  xmm0,QWORD PTR [rbp+0x30]
   14000238c:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   140002391:	48 8b 15 58 cd 00 00 	mov    rdx,QWORD PTR [rip+0xcd58]        # 14000f0f0 <stUserMathErr>
   140002398:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   14000239c:	48 89 c1             	mov    rcx,rax
   14000239f:	ff d2                	call   rdx
   1400023a1:	eb 01                	jmp    1400023a4 <__mingw_raise_matherr+0x64>
   1400023a3:	90                   	nop
   1400023a4:	48 83 c4 50          	add    rsp,0x50
   1400023a8:	5d                   	pop    rbp
   1400023a9:	c3                   	ret

00000001400023aa <__mingw_setusermatherr>:
   1400023aa:	55                   	push   rbp
   1400023ab:	48 89 e5             	mov    rbp,rsp
   1400023ae:	48 83 ec 20          	sub    rsp,0x20
   1400023b2:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400023b6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023ba:	48 89 05 2f cd 00 00 	mov    QWORD PTR [rip+0xcd2f],rax        # 14000f0f0 <stUserMathErr>
   1400023c1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023c5:	48 89 c1             	mov    rcx,rax
   1400023c8:	e8 93 71 00 00       	call   140009560 <__setusermatherr>
   1400023cd:	90                   	nop
   1400023ce:	48 83 c4 20          	add    rsp,0x20
   1400023d2:	5d                   	pop    rbp
   1400023d3:	c3                   	ret
   1400023d4:	90                   	nop
   1400023d5:	90                   	nop
   1400023d6:	90                   	nop
   1400023d7:	90                   	nop
   1400023d8:	90                   	nop
   1400023d9:	90                   	nop
   1400023da:	90                   	nop
   1400023db:	90                   	nop
   1400023dc:	90                   	nop
   1400023dd:	90                   	nop
   1400023de:	90                   	nop
   1400023df:	90                   	nop

00000001400023e0 <__mingw_SEH_error_handler>:
   1400023e0:	55                   	push   rbp
   1400023e1:	48 89 e5             	mov    rbp,rsp
   1400023e4:	48 83 ec 30          	sub    rsp,0x30
   1400023e8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400023ec:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400023f0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400023f4:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   1400023f8:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   1400023ff:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002406:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000240a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000240d:	83 e0 02             	and    eax,0x2
   140002410:	85 c0                	test   eax,eax
   140002412:	74 0a                	je     14000241e <__mingw_SEH_error_handler+0x3e>
   140002414:	b8 01 00 00 00       	mov    eax,0x1
   140002419:	e9 16 02 00 00       	jmp    140002634 <__mingw_SEH_error_handler+0x254>
   14000241e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002422:	8b 00                	mov    eax,DWORD PTR [rax]
   140002424:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002429:	3d 43 43 47 20       	cmp    eax,0x20474343
   14000242e:	75 18                	jne    140002448 <__mingw_SEH_error_handler+0x68>
   140002430:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002434:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002437:	83 e0 01             	and    eax,0x1
   14000243a:	85 c0                	test   eax,eax
   14000243c:	75 0a                	jne    140002448 <__mingw_SEH_error_handler+0x68>
   14000243e:	b8 00 00 00 00       	mov    eax,0x0
   140002443:	e9 ec 01 00 00       	jmp    140002634 <__mingw_SEH_error_handler+0x254>
   140002448:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000244c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000244e:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002453:	0f 84 12 01 00 00    	je     14000256b <__mingw_SEH_error_handler+0x18b>
   140002459:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000245e:	0f 87 c3 01 00 00    	ja     140002627 <__mingw_SEH_error_handler+0x247>
   140002464:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   140002469:	0f 87 b8 01 00 00    	ja     140002627 <__mingw_SEH_error_handler+0x247>
   14000246f:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   140002474:	0f 83 4c 01 00 00    	jae    1400025c6 <__mingw_SEH_error_handler+0x1e6>
   14000247a:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000247f:	0f 84 3a 01 00 00    	je     1400025bf <__mingw_SEH_error_handler+0x1df>
   140002485:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000248a:	0f 87 97 01 00 00    	ja     140002627 <__mingw_SEH_error_handler+0x247>
   140002490:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   140002495:	0f 84 83 01 00 00    	je     14000261e <__mingw_SEH_error_handler+0x23e>
   14000249b:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400024a0:	0f 87 81 01 00 00    	ja     140002627 <__mingw_SEH_error_handler+0x247>
   1400024a6:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400024ab:	0f 87 76 01 00 00    	ja     140002627 <__mingw_SEH_error_handler+0x247>
   1400024b1:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   1400024b6:	0f 83 03 01 00 00    	jae    1400025bf <__mingw_SEH_error_handler+0x1df>
   1400024bc:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400024c1:	0f 84 57 01 00 00    	je     14000261e <__mingw_SEH_error_handler+0x23e>
   1400024c7:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400024cc:	0f 87 55 01 00 00    	ja     140002627 <__mingw_SEH_error_handler+0x247>
   1400024d2:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400024d7:	0f 84 8e 00 00 00    	je     14000256b <__mingw_SEH_error_handler+0x18b>
   1400024dd:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400024e2:	0f 87 3f 01 00 00    	ja     140002627 <__mingw_SEH_error_handler+0x247>
   1400024e8:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   1400024ed:	0f 84 2b 01 00 00    	je     14000261e <__mingw_SEH_error_handler+0x23e>
   1400024f3:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   1400024f8:	0f 87 29 01 00 00    	ja     140002627 <__mingw_SEH_error_handler+0x247>
   1400024fe:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002503:	0f 84 15 01 00 00    	je     14000261e <__mingw_SEH_error_handler+0x23e>
   140002509:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000250e:	0f 85 13 01 00 00    	jne    140002627 <__mingw_SEH_error_handler+0x247>
   140002514:	ba 00 00 00 00       	mov    edx,0x0
   140002519:	b9 0b 00 00 00       	mov    ecx,0xb
   14000251e:	e8 d5 70 00 00       	call   1400095f8 <signal>
   140002523:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002527:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000252c:	75 1b                	jne    140002549 <__mingw_SEH_error_handler+0x169>
   14000252e:	ba 01 00 00 00       	mov    edx,0x1
   140002533:	b9 0b 00 00 00       	mov    ecx,0xb
   140002538:	e8 bb 70 00 00       	call   1400095f8 <signal>
   14000253d:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002544:	e9 e1 00 00 00       	jmp    14000262a <__mingw_SEH_error_handler+0x24a>
   140002549:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000254e:	0f 84 d6 00 00 00    	je     14000262a <__mingw_SEH_error_handler+0x24a>
   140002554:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002558:	b9 0b 00 00 00       	mov    ecx,0xb
   14000255d:	ff d0                	call   rax
   14000255f:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002566:	e9 bf 00 00 00       	jmp    14000262a <__mingw_SEH_error_handler+0x24a>
   14000256b:	ba 00 00 00 00       	mov    edx,0x0
   140002570:	b9 04 00 00 00       	mov    ecx,0x4
   140002575:	e8 7e 70 00 00       	call   1400095f8 <signal>
   14000257a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000257e:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002583:	75 1b                	jne    1400025a0 <__mingw_SEH_error_handler+0x1c0>
   140002585:	ba 01 00 00 00       	mov    edx,0x1
   14000258a:	b9 04 00 00 00       	mov    ecx,0x4
   14000258f:	e8 64 70 00 00       	call   1400095f8 <signal>
   140002594:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000259b:	e9 8d 00 00 00       	jmp    14000262d <__mingw_SEH_error_handler+0x24d>
   1400025a0:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400025a5:	0f 84 82 00 00 00    	je     14000262d <__mingw_SEH_error_handler+0x24d>
   1400025ab:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400025af:	b9 04 00 00 00       	mov    ecx,0x4
   1400025b4:	ff d0                	call   rax
   1400025b6:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025bd:	eb 6e                	jmp    14000262d <__mingw_SEH_error_handler+0x24d>
   1400025bf:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400025c6:	ba 00 00 00 00       	mov    edx,0x0
   1400025cb:	b9 08 00 00 00       	mov    ecx,0x8
   1400025d0:	e8 23 70 00 00       	call   1400095f8 <signal>
   1400025d5:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400025d9:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400025de:	75 23                	jne    140002603 <__mingw_SEH_error_handler+0x223>
   1400025e0:	ba 01 00 00 00       	mov    edx,0x1
   1400025e5:	b9 08 00 00 00       	mov    ecx,0x8
   1400025ea:	e8 09 70 00 00       	call   1400095f8 <signal>
   1400025ef:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   1400025f3:	74 05                	je     1400025fa <__mingw_SEH_error_handler+0x21a>
   1400025f5:	e8 a6 05 00 00       	call   140002ba0 <_fpreset>
   1400025fa:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002601:	eb 2d                	jmp    140002630 <__mingw_SEH_error_handler+0x250>
   140002603:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002608:	74 26                	je     140002630 <__mingw_SEH_error_handler+0x250>
   14000260a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000260e:	b9 08 00 00 00       	mov    ecx,0x8
   140002613:	ff d0                	call   rax
   140002615:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000261c:	eb 12                	jmp    140002630 <__mingw_SEH_error_handler+0x250>
   14000261e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002625:	eb 0a                	jmp    140002631 <__mingw_SEH_error_handler+0x251>
   140002627:	90                   	nop
   140002628:	eb 07                	jmp    140002631 <__mingw_SEH_error_handler+0x251>
   14000262a:	90                   	nop
   14000262b:	eb 04                	jmp    140002631 <__mingw_SEH_error_handler+0x251>
   14000262d:	90                   	nop
   14000262e:	eb 01                	jmp    140002631 <__mingw_SEH_error_handler+0x251>
   140002630:	90                   	nop
   140002631:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002634:	48 83 c4 30          	add    rsp,0x30
   140002638:	5d                   	pop    rbp
   140002639:	c3                   	ret

000000014000263a <_gnu_exception_handler>:
   14000263a:	55                   	push   rbp
   14000263b:	48 89 e5             	mov    rbp,rsp
   14000263e:	48 83 ec 30          	sub    rsp,0x30
   140002642:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002646:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000264d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002654:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002658:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000265b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000265d:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002662:	3d 43 43 47 20       	cmp    eax,0x20474343
   140002667:	75 1b                	jne    140002684 <_gnu_exception_handler+0x4a>
   140002669:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000266d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002670:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002673:	83 e0 01             	and    eax,0x1
   140002676:	85 c0                	test   eax,eax
   140002678:	75 0a                	jne    140002684 <_gnu_exception_handler+0x4a>
   14000267a:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000267f:	e9 14 02 00 00       	jmp    140002898 <_gnu_exception_handler+0x25e>
   140002684:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002688:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000268b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000268d:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002692:	0f 84 12 01 00 00    	je     1400027aa <_gnu_exception_handler+0x170>
   140002698:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000269d:	0f 87 c3 01 00 00    	ja     140002866 <_gnu_exception_handler+0x22c>
   1400026a3:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   1400026a8:	0f 87 b8 01 00 00    	ja     140002866 <_gnu_exception_handler+0x22c>
   1400026ae:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   1400026b3:	0f 83 4c 01 00 00    	jae    140002805 <_gnu_exception_handler+0x1cb>
   1400026b9:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400026be:	0f 84 3a 01 00 00    	je     1400027fe <_gnu_exception_handler+0x1c4>
   1400026c4:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400026c9:	0f 87 97 01 00 00    	ja     140002866 <_gnu_exception_handler+0x22c>
   1400026cf:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400026d4:	0f 84 83 01 00 00    	je     14000285d <_gnu_exception_handler+0x223>
   1400026da:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400026df:	0f 87 81 01 00 00    	ja     140002866 <_gnu_exception_handler+0x22c>
   1400026e5:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400026ea:	0f 87 76 01 00 00    	ja     140002866 <_gnu_exception_handler+0x22c>
   1400026f0:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   1400026f5:	0f 83 03 01 00 00    	jae    1400027fe <_gnu_exception_handler+0x1c4>
   1400026fb:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   140002700:	0f 84 57 01 00 00    	je     14000285d <_gnu_exception_handler+0x223>
   140002706:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   14000270b:	0f 87 55 01 00 00    	ja     140002866 <_gnu_exception_handler+0x22c>
   140002711:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002716:	0f 84 8e 00 00 00    	je     1400027aa <_gnu_exception_handler+0x170>
   14000271c:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002721:	0f 87 3f 01 00 00    	ja     140002866 <_gnu_exception_handler+0x22c>
   140002727:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000272c:	0f 84 2b 01 00 00    	je     14000285d <_gnu_exception_handler+0x223>
   140002732:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002737:	0f 87 29 01 00 00    	ja     140002866 <_gnu_exception_handler+0x22c>
   14000273d:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002742:	0f 84 15 01 00 00    	je     14000285d <_gnu_exception_handler+0x223>
   140002748:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000274d:	0f 85 13 01 00 00    	jne    140002866 <_gnu_exception_handler+0x22c>
   140002753:	ba 00 00 00 00       	mov    edx,0x0
   140002758:	b9 0b 00 00 00       	mov    ecx,0xb
   14000275d:	e8 96 6e 00 00       	call   1400095f8 <signal>
   140002762:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002766:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000276b:	75 1b                	jne    140002788 <_gnu_exception_handler+0x14e>
   14000276d:	ba 01 00 00 00       	mov    edx,0x1
   140002772:	b9 0b 00 00 00       	mov    ecx,0xb
   140002777:	e8 7c 6e 00 00       	call   1400095f8 <signal>
   14000277c:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002783:	e9 e1 00 00 00       	jmp    140002869 <_gnu_exception_handler+0x22f>
   140002788:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000278d:	0f 84 d6 00 00 00    	je     140002869 <_gnu_exception_handler+0x22f>
   140002793:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002797:	b9 0b 00 00 00       	mov    ecx,0xb
   14000279c:	ff d0                	call   rax
   14000279e:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027a5:	e9 bf 00 00 00       	jmp    140002869 <_gnu_exception_handler+0x22f>
   1400027aa:	ba 00 00 00 00       	mov    edx,0x0
   1400027af:	b9 04 00 00 00       	mov    ecx,0x4
   1400027b4:	e8 3f 6e 00 00       	call   1400095f8 <signal>
   1400027b9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400027bd:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400027c2:	75 1b                	jne    1400027df <_gnu_exception_handler+0x1a5>
   1400027c4:	ba 01 00 00 00       	mov    edx,0x1
   1400027c9:	b9 04 00 00 00       	mov    ecx,0x4
   1400027ce:	e8 25 6e 00 00       	call   1400095f8 <signal>
   1400027d3:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027da:	e9 8d 00 00 00       	jmp    14000286c <_gnu_exception_handler+0x232>
   1400027df:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400027e4:	0f 84 82 00 00 00    	je     14000286c <_gnu_exception_handler+0x232>
   1400027ea:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400027ee:	b9 04 00 00 00       	mov    ecx,0x4
   1400027f3:	ff d0                	call   rax
   1400027f5:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027fc:	eb 6e                	jmp    14000286c <_gnu_exception_handler+0x232>
   1400027fe:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140002805:	ba 00 00 00 00       	mov    edx,0x0
   14000280a:	b9 08 00 00 00       	mov    ecx,0x8
   14000280f:	e8 e4 6d 00 00       	call   1400095f8 <signal>
   140002814:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002818:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000281d:	75 23                	jne    140002842 <_gnu_exception_handler+0x208>
   14000281f:	ba 01 00 00 00       	mov    edx,0x1
   140002824:	b9 08 00 00 00       	mov    ecx,0x8
   140002829:	e8 ca 6d 00 00       	call   1400095f8 <signal>
   14000282e:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002832:	74 05                	je     140002839 <_gnu_exception_handler+0x1ff>
   140002834:	e8 67 03 00 00       	call   140002ba0 <_fpreset>
   140002839:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002840:	eb 2d                	jmp    14000286f <_gnu_exception_handler+0x235>
   140002842:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002847:	74 26                	je     14000286f <_gnu_exception_handler+0x235>
   140002849:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000284d:	b9 08 00 00 00       	mov    ecx,0x8
   140002852:	ff d0                	call   rax
   140002854:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000285b:	eb 12                	jmp    14000286f <_gnu_exception_handler+0x235>
   14000285d:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002864:	eb 0a                	jmp    140002870 <_gnu_exception_handler+0x236>
   140002866:	90                   	nop
   140002867:	eb 07                	jmp    140002870 <_gnu_exception_handler+0x236>
   140002869:	90                   	nop
   14000286a:	eb 04                	jmp    140002870 <_gnu_exception_handler+0x236>
   14000286c:	90                   	nop
   14000286d:	eb 01                	jmp    140002870 <_gnu_exception_handler+0x236>
   14000286f:	90                   	nop
   140002870:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140002874:	75 1f                	jne    140002895 <_gnu_exception_handler+0x25b>
   140002876:	48 8b 05 93 c8 00 00 	mov    rax,QWORD PTR [rip+0xc893]        # 14000f110 <__mingw_oldexcpt_handler>
   14000287d:	48 85 c0             	test   rax,rax
   140002880:	74 13                	je     140002895 <_gnu_exception_handler+0x25b>
   140002882:	48 8b 15 87 c8 00 00 	mov    rdx,QWORD PTR [rip+0xc887]        # 14000f110 <__mingw_oldexcpt_handler>
   140002889:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000288d:	48 89 c1             	mov    rcx,rax
   140002890:	ff d2                	call   rdx
   140002892:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140002895:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002898:	48 83 c4 30          	add    rsp,0x30
   14000289c:	5d                   	pop    rbp
   14000289d:	c3                   	ret
   14000289e:	90                   	nop
   14000289f:	90                   	nop

00000001400028a0 <___w64_mingwthr_add_key_dtor>:
   1400028a0:	55                   	push   rbp
   1400028a1:	48 89 e5             	mov    rbp,rsp
   1400028a4:	48 83 ec 30          	sub    rsp,0x30
   1400028a8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400028ab:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400028af:	8b 05 93 c8 00 00    	mov    eax,DWORD PTR [rip+0xc893]        # 14000f148 <__mingwthr_cs_init>
   1400028b5:	85 c0                	test   eax,eax
   1400028b7:	75 07                	jne    1400028c0 <___w64_mingwthr_add_key_dtor+0x20>
   1400028b9:	b8 00 00 00 00       	mov    eax,0x0
   1400028be:	eb 7b                	jmp    14000293b <___w64_mingwthr_add_key_dtor+0x9b>
   1400028c0:	ba 18 00 00 00       	mov    edx,0x18
   1400028c5:	b9 01 00 00 00       	mov    ecx,0x1
   1400028ca:	e8 d9 6c 00 00       	call   1400095a8 <calloc>
   1400028cf:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400028d3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400028d8:	75 07                	jne    1400028e1 <___w64_mingwthr_add_key_dtor+0x41>
   1400028da:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400028df:	eb 5a                	jmp    14000293b <___w64_mingwthr_add_key_dtor+0x9b>
   1400028e1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400028e5:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   1400028e8:	89 10                	mov    DWORD PTR [rax],edx
   1400028ea:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400028ee:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400028f2:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
   1400028f6:	48 8d 05 23 c8 00 00 	lea    rax,[rip+0xc823]        # 14000f120 <__mingwthr_cs>
   1400028fd:	48 89 c1             	mov    rcx,rax
   140002900:	48 8b 05 e9 d8 00 00 	mov    rax,QWORD PTR [rip+0xd8e9]        # 1400101f0 <__imp_EnterCriticalSection>
   140002907:	ff d0                	call   rax
   140002909:	48 8b 15 40 c8 00 00 	mov    rdx,QWORD PTR [rip+0xc840]        # 14000f150 <key_dtor_list>
   140002910:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002914:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002918:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000291c:	48 89 05 2d c8 00 00 	mov    QWORD PTR [rip+0xc82d],rax        # 14000f150 <key_dtor_list>
   140002923:	48 8d 05 f6 c7 00 00 	lea    rax,[rip+0xc7f6]        # 14000f120 <__mingwthr_cs>
   14000292a:	48 89 c1             	mov    rcx,rax
   14000292d:	48 8b 05 f4 d8 00 00 	mov    rax,QWORD PTR [rip+0xd8f4]        # 140010228 <__imp_LeaveCriticalSection>
   140002934:	ff d0                	call   rax
   140002936:	b8 00 00 00 00       	mov    eax,0x0
   14000293b:	48 83 c4 30          	add    rsp,0x30
   14000293f:	5d                   	pop    rbp
   140002940:	c3                   	ret

0000000140002941 <___w64_mingwthr_remove_key_dtor>:
   140002941:	55                   	push   rbp
   140002942:	48 89 e5             	mov    rbp,rsp
   140002945:	48 83 ec 30          	sub    rsp,0x30
   140002949:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000294c:	8b 05 f6 c7 00 00    	mov    eax,DWORD PTR [rip+0xc7f6]        # 14000f148 <__mingwthr_cs_init>
   140002952:	85 c0                	test   eax,eax
   140002954:	75 0a                	jne    140002960 <___w64_mingwthr_remove_key_dtor+0x1f>
   140002956:	b8 00 00 00 00       	mov    eax,0x0
   14000295b:	e9 9c 00 00 00       	jmp    1400029fc <___w64_mingwthr_remove_key_dtor+0xbb>
   140002960:	48 8d 05 b9 c7 00 00 	lea    rax,[rip+0xc7b9]        # 14000f120 <__mingwthr_cs>
   140002967:	48 89 c1             	mov    rcx,rax
   14000296a:	48 8b 05 7f d8 00 00 	mov    rax,QWORD PTR [rip+0xd87f]        # 1400101f0 <__imp_EnterCriticalSection>
   140002971:	ff d0                	call   rax
   140002973:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   14000297a:	00 
   14000297b:	48 8b 05 ce c7 00 00 	mov    rax,QWORD PTR [rip+0xc7ce]        # 14000f150 <key_dtor_list>
   140002982:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002986:	eb 55                	jmp    1400029dd <___w64_mingwthr_remove_key_dtor+0x9c>
   140002988:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000298c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000298e:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   140002991:	75 36                	jne    1400029c9 <___w64_mingwthr_remove_key_dtor+0x88>
   140002993:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002998:	75 11                	jne    1400029ab <___w64_mingwthr_remove_key_dtor+0x6a>
   14000299a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000299e:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   1400029a2:	48 89 05 a7 c7 00 00 	mov    QWORD PTR [rip+0xc7a7],rax        # 14000f150 <key_dtor_list>
   1400029a9:	eb 10                	jmp    1400029bb <___w64_mingwthr_remove_key_dtor+0x7a>
   1400029ab:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029af:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   1400029b3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400029b7:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   1400029bb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029bf:	48 89 c1             	mov    rcx,rax
   1400029c2:	e8 09 6c 00 00       	call   1400095d0 <free>
   1400029c7:	eb 1b                	jmp    1400029e4 <___w64_mingwthr_remove_key_dtor+0xa3>
   1400029c9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029cd:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400029d1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029d5:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   1400029d9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400029dd:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400029e2:	75 a4                	jne    140002988 <___w64_mingwthr_remove_key_dtor+0x47>
   1400029e4:	48 8d 05 35 c7 00 00 	lea    rax,[rip+0xc735]        # 14000f120 <__mingwthr_cs>
   1400029eb:	48 89 c1             	mov    rcx,rax
   1400029ee:	48 8b 05 33 d8 00 00 	mov    rax,QWORD PTR [rip+0xd833]        # 140010228 <__imp_LeaveCriticalSection>
   1400029f5:	ff d0                	call   rax
   1400029f7:	b8 00 00 00 00       	mov    eax,0x0
   1400029fc:	48 83 c4 30          	add    rsp,0x30
   140002a00:	5d                   	pop    rbp
   140002a01:	c3                   	ret

0000000140002a02 <__mingwthr_run_key_dtors>:
   140002a02:	55                   	push   rbp
   140002a03:	48 89 e5             	mov    rbp,rsp
   140002a06:	48 83 ec 30          	sub    rsp,0x30
   140002a0a:	8b 05 38 c7 00 00    	mov    eax,DWORD PTR [rip+0xc738]        # 14000f148 <__mingwthr_cs_init>
   140002a10:	85 c0                	test   eax,eax
   140002a12:	0f 84 82 00 00 00    	je     140002a9a <__mingwthr_run_key_dtors+0x98>
   140002a18:	48 8d 05 01 c7 00 00 	lea    rax,[rip+0xc701]        # 14000f120 <__mingwthr_cs>
   140002a1f:	48 89 c1             	mov    rcx,rax
   140002a22:	48 8b 05 c7 d7 00 00 	mov    rax,QWORD PTR [rip+0xd7c7]        # 1400101f0 <__imp_EnterCriticalSection>
   140002a29:	ff d0                	call   rax
   140002a2b:	48 8b 05 1e c7 00 00 	mov    rax,QWORD PTR [rip+0xc71e]        # 14000f150 <key_dtor_list>
   140002a32:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a36:	eb 46                	jmp    140002a7e <__mingwthr_run_key_dtors+0x7c>
   140002a38:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a3c:	8b 00                	mov    eax,DWORD PTR [rax]
   140002a3e:	89 c1                	mov    ecx,eax
   140002a40:	48 8b 05 09 d8 00 00 	mov    rax,QWORD PTR [rip+0xd809]        # 140010250 <__imp_TlsGetValue>
   140002a47:	ff d0                	call   rax
   140002a49:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002a4d:	48 8b 05 b4 d7 00 00 	mov    rax,QWORD PTR [rip+0xd7b4]        # 140010208 <__imp_GetLastError>
   140002a54:	ff d0                	call   rax
   140002a56:	85 c0                	test   eax,eax
   140002a58:	75 18                	jne    140002a72 <__mingwthr_run_key_dtors+0x70>
   140002a5a:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002a5f:	74 11                	je     140002a72 <__mingwthr_run_key_dtors+0x70>
   140002a61:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a65:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140002a69:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002a6d:	48 89 c1             	mov    rcx,rax
   140002a70:	ff d2                	call   rdx
   140002a72:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a76:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002a7a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a7e:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002a83:	75 b3                	jne    140002a38 <__mingwthr_run_key_dtors+0x36>
   140002a85:	48 8d 05 94 c6 00 00 	lea    rax,[rip+0xc694]        # 14000f120 <__mingwthr_cs>
   140002a8c:	48 89 c1             	mov    rcx,rax
   140002a8f:	48 8b 05 92 d7 00 00 	mov    rax,QWORD PTR [rip+0xd792]        # 140010228 <__imp_LeaveCriticalSection>
   140002a96:	ff d0                	call   rax
   140002a98:	eb 01                	jmp    140002a9b <__mingwthr_run_key_dtors+0x99>
   140002a9a:	90                   	nop
   140002a9b:	48 83 c4 30          	add    rsp,0x30
   140002a9f:	5d                   	pop    rbp
   140002aa0:	c3                   	ret

0000000140002aa1 <__mingw_TLScallback>:
   140002aa1:	55                   	push   rbp
   140002aa2:	48 89 e5             	mov    rbp,rsp
   140002aa5:	48 83 ec 30          	sub    rsp,0x30
   140002aa9:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002aad:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140002ab0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002ab4:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002ab8:	0f 84 cc 00 00 00    	je     140002b8a <__mingw_TLScallback+0xe9>
   140002abe:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002ac2:	0f 87 ca 00 00 00    	ja     140002b92 <__mingw_TLScallback+0xf1>
   140002ac8:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002acc:	0f 84 b1 00 00 00    	je     140002b83 <__mingw_TLScallback+0xe2>
   140002ad2:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002ad6:	0f 87 b6 00 00 00    	ja     140002b92 <__mingw_TLScallback+0xf1>
   140002adc:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140002ae0:	74 33                	je     140002b15 <__mingw_TLScallback+0x74>
   140002ae2:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140002ae6:	0f 85 a6 00 00 00    	jne    140002b92 <__mingw_TLScallback+0xf1>
   140002aec:	8b 05 56 c6 00 00    	mov    eax,DWORD PTR [rip+0xc656]        # 14000f148 <__mingwthr_cs_init>
   140002af2:	85 c0                	test   eax,eax
   140002af4:	75 13                	jne    140002b09 <__mingw_TLScallback+0x68>
   140002af6:	48 8d 05 23 c6 00 00 	lea    rax,[rip+0xc623]        # 14000f120 <__mingwthr_cs>
   140002afd:	48 89 c1             	mov    rcx,rax
   140002b00:	48 8b 05 19 d7 00 00 	mov    rax,QWORD PTR [rip+0xd719]        # 140010220 <__imp_InitializeCriticalSection>
   140002b07:	ff d0                	call   rax
   140002b09:	c7 05 35 c6 00 00 01 	mov    DWORD PTR [rip+0xc635],0x1        # 14000f148 <__mingwthr_cs_init>
   140002b10:	00 00 00 
   140002b13:	eb 7d                	jmp    140002b92 <__mingw_TLScallback+0xf1>
   140002b15:	e8 e8 fe ff ff       	call   140002a02 <__mingwthr_run_key_dtors>
   140002b1a:	8b 05 28 c6 00 00    	mov    eax,DWORD PTR [rip+0xc628]        # 14000f148 <__mingwthr_cs_init>
   140002b20:	83 f8 01             	cmp    eax,0x1
   140002b23:	75 6c                	jne    140002b91 <__mingw_TLScallback+0xf0>
   140002b25:	48 8b 05 24 c6 00 00 	mov    rax,QWORD PTR [rip+0xc624]        # 14000f150 <key_dtor_list>
   140002b2c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b30:	eb 20                	jmp    140002b52 <__mingw_TLScallback+0xb1>
   140002b32:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b36:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002b3a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b3e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b42:	48 89 c1             	mov    rcx,rax
   140002b45:	e8 86 6a 00 00       	call   1400095d0 <free>
   140002b4a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b4e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b52:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002b57:	75 d9                	jne    140002b32 <__mingw_TLScallback+0x91>
   140002b59:	48 c7 05 ec c5 00 00 	mov    QWORD PTR [rip+0xc5ec],0x0        # 14000f150 <key_dtor_list>
   140002b60:	00 00 00 00 
   140002b64:	c7 05 da c5 00 00 00 	mov    DWORD PTR [rip+0xc5da],0x0        # 14000f148 <__mingwthr_cs_init>
   140002b6b:	00 00 00 
   140002b6e:	48 8d 05 ab c5 00 00 	lea    rax,[rip+0xc5ab]        # 14000f120 <__mingwthr_cs>
   140002b75:	48 89 c1             	mov    rcx,rax
   140002b78:	48 8b 05 69 d6 00 00 	mov    rax,QWORD PTR [rip+0xd669]        # 1400101e8 <__IAT_start__>
   140002b7f:	ff d0                	call   rax
   140002b81:	eb 0e                	jmp    140002b91 <__mingw_TLScallback+0xf0>
   140002b83:	e8 18 00 00 00       	call   140002ba0 <_fpreset>
   140002b88:	eb 08                	jmp    140002b92 <__mingw_TLScallback+0xf1>
   140002b8a:	e8 73 fe ff ff       	call   140002a02 <__mingwthr_run_key_dtors>
   140002b8f:	eb 01                	jmp    140002b92 <__mingw_TLScallback+0xf1>
   140002b91:	90                   	nop
   140002b92:	b8 01 00 00 00       	mov    eax,0x1
   140002b97:	48 83 c4 30          	add    rsp,0x30
   140002b9b:	5d                   	pop    rbp
   140002b9c:	c3                   	ret
   140002b9d:	90                   	nop
   140002b9e:	90                   	nop
   140002b9f:	90                   	nop

0000000140002ba0 <_fpreset>:
   140002ba0:	55                   	push   rbp
   140002ba1:	48 89 e5             	mov    rbp,rsp
   140002ba4:	db e3                	fninit
   140002ba6:	90                   	nop
   140002ba7:	5d                   	pop    rbp
   140002ba8:	c3                   	ret
   140002ba9:	90                   	nop
   140002baa:	90                   	nop
   140002bab:	90                   	nop
   140002bac:	90                   	nop
   140002bad:	90                   	nop
   140002bae:	90                   	nop
   140002baf:	90                   	nop

0000000140002bb0 <_ValidateImageBase>:
   140002bb0:	55                   	push   rbp
   140002bb1:	48 89 e5             	mov    rbp,rsp
   140002bb4:	48 83 ec 20          	sub    rsp,0x20
   140002bb8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002bbc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002bc0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002bc4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bc8:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002bcb:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140002bcf:	74 07                	je     140002bd8 <_ValidateImageBase+0x28>
   140002bd1:	b8 00 00 00 00       	mov    eax,0x0
   140002bd6:	eb 4e                	jmp    140002c26 <_ValidateImageBase+0x76>
   140002bd8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bdc:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002bdf:	48 63 d0             	movsxd rdx,eax
   140002be2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002be6:	48 01 d0             	add    rax,rdx
   140002be9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002bed:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002bf1:	8b 00                	mov    eax,DWORD PTR [rax]
   140002bf3:	3d 50 45 00 00       	cmp    eax,0x4550
   140002bf8:	74 07                	je     140002c01 <_ValidateImageBase+0x51>
   140002bfa:	b8 00 00 00 00       	mov    eax,0x0
   140002bff:	eb 25                	jmp    140002c26 <_ValidateImageBase+0x76>
   140002c01:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c05:	48 83 c0 18          	add    rax,0x18
   140002c09:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002c0d:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c11:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002c14:	66 3d 0b 02          	cmp    ax,0x20b
   140002c18:	74 07                	je     140002c21 <_ValidateImageBase+0x71>
   140002c1a:	b8 00 00 00 00       	mov    eax,0x0
   140002c1f:	eb 05                	jmp    140002c26 <_ValidateImageBase+0x76>
   140002c21:	b8 01 00 00 00       	mov    eax,0x1
   140002c26:	48 83 c4 20          	add    rsp,0x20
   140002c2a:	5d                   	pop    rbp
   140002c2b:	c3                   	ret

0000000140002c2c <_FindPESection>:
   140002c2c:	55                   	push   rbp
   140002c2d:	48 89 e5             	mov    rbp,rsp
   140002c30:	48 83 ec 20          	sub    rsp,0x20
   140002c34:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002c38:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002c3c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c40:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002c43:	48 63 d0             	movsxd rdx,eax
   140002c46:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c4a:	48 01 d0             	add    rax,rdx
   140002c4d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002c51:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002c58:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c5c:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002c60:	0f b7 d0             	movzx  edx,ax
   140002c63:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c67:	48 01 d0             	add    rax,rdx
   140002c6a:	48 83 c0 18          	add    rax,0x18
   140002c6e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002c72:	eb 36                	jmp    140002caa <_FindPESection+0x7e>
   140002c74:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c78:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140002c7b:	89 c0                	mov    eax,eax
   140002c7d:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002c81:	72 1e                	jb     140002ca1 <_FindPESection+0x75>
   140002c83:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c87:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140002c8a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c8e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002c91:	01 d0                	add    eax,edx
   140002c93:	89 c0                	mov    eax,eax
   140002c95:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002c99:	73 06                	jae    140002ca1 <_FindPESection+0x75>
   140002c9b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c9f:	eb 1e                	jmp    140002cbf <_FindPESection+0x93>
   140002ca1:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002ca5:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002caa:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002cae:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002cb2:	0f b7 c0             	movzx  eax,ax
   140002cb5:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002cb8:	72 ba                	jb     140002c74 <_FindPESection+0x48>
   140002cba:	b8 00 00 00 00       	mov    eax,0x0
   140002cbf:	48 83 c4 20          	add    rsp,0x20
   140002cc3:	5d                   	pop    rbp
   140002cc4:	c3                   	ret

0000000140002cc5 <_FindPESectionByName>:
   140002cc5:	55                   	push   rbp
   140002cc6:	48 89 e5             	mov    rbp,rsp
   140002cc9:	48 83 ec 40          	sub    rsp,0x40
   140002ccd:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002cd1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002cd5:	48 89 c1             	mov    rcx,rax
   140002cd8:	e8 2b 69 00 00       	call   140009608 <strlen>
   140002cdd:	48 83 f8 08          	cmp    rax,0x8
   140002ce1:	76 0a                	jbe    140002ced <_FindPESectionByName+0x28>
   140002ce3:	b8 00 00 00 00       	mov    eax,0x0
   140002ce8:	e9 98 00 00 00       	jmp    140002d85 <_FindPESectionByName+0xc0>
   140002ced:	48 8b 05 8c 88 00 00 	mov    rax,QWORD PTR [rip+0x888c]        # 14000b580 <.refptr.__ImageBase>
   140002cf4:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002cf8:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002cfc:	48 89 c1             	mov    rcx,rax
   140002cff:	e8 ac fe ff ff       	call   140002bb0 <_ValidateImageBase>
   140002d04:	85 c0                	test   eax,eax
   140002d06:	75 07                	jne    140002d0f <_FindPESectionByName+0x4a>
   140002d08:	b8 00 00 00 00       	mov    eax,0x0
   140002d0d:	eb 76                	jmp    140002d85 <_FindPESectionByName+0xc0>
   140002d0f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d13:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002d16:	48 63 d0             	movsxd rdx,eax
   140002d19:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d1d:	48 01 d0             	add    rax,rdx
   140002d20:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002d24:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002d2b:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d2f:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002d33:	0f b7 d0             	movzx  edx,ax
   140002d36:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d3a:	48 01 d0             	add    rax,rdx
   140002d3d:	48 83 c0 18          	add    rax,0x18
   140002d41:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d45:	eb 29                	jmp    140002d70 <_FindPESectionByName+0xab>
   140002d47:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d4b:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140002d4f:	41 b8 08 00 00 00    	mov    r8d,0x8
   140002d55:	48 89 c1             	mov    rcx,rax
   140002d58:	e8 b3 68 00 00       	call   140009610 <strncmp>
   140002d5d:	85 c0                	test   eax,eax
   140002d5f:	75 06                	jne    140002d67 <_FindPESectionByName+0xa2>
   140002d61:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d65:	eb 1e                	jmp    140002d85 <_FindPESectionByName+0xc0>
   140002d67:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002d6b:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002d70:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d74:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002d78:	0f b7 c0             	movzx  eax,ax
   140002d7b:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002d7e:	72 c7                	jb     140002d47 <_FindPESectionByName+0x82>
   140002d80:	b8 00 00 00 00       	mov    eax,0x0
   140002d85:	48 83 c4 40          	add    rsp,0x40
   140002d89:	5d                   	pop    rbp
   140002d8a:	c3                   	ret

0000000140002d8b <__mingw_GetSectionForAddress>:
   140002d8b:	55                   	push   rbp
   140002d8c:	48 89 e5             	mov    rbp,rsp
   140002d8f:	48 83 ec 30          	sub    rsp,0x30
   140002d93:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002d97:	48 8b 05 e2 87 00 00 	mov    rax,QWORD PTR [rip+0x87e2]        # 14000b580 <.refptr.__ImageBase>
   140002d9e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002da2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002da6:	48 89 c1             	mov    rcx,rax
   140002da9:	e8 02 fe ff ff       	call   140002bb0 <_ValidateImageBase>
   140002dae:	85 c0                	test   eax,eax
   140002db0:	75 07                	jne    140002db9 <__mingw_GetSectionForAddress+0x2e>
   140002db2:	b8 00 00 00 00       	mov    eax,0x0
   140002db7:	eb 1c                	jmp    140002dd5 <__mingw_GetSectionForAddress+0x4a>
   140002db9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002dbd:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002dc1:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002dc5:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002dc9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002dcd:	48 89 c1             	mov    rcx,rax
   140002dd0:	e8 57 fe ff ff       	call   140002c2c <_FindPESection>
   140002dd5:	48 83 c4 30          	add    rsp,0x30
   140002dd9:	5d                   	pop    rbp
   140002dda:	c3                   	ret

0000000140002ddb <__mingw_GetSectionCount>:
   140002ddb:	55                   	push   rbp
   140002ddc:	48 89 e5             	mov    rbp,rsp
   140002ddf:	48 83 ec 30          	sub    rsp,0x30
   140002de3:	48 8b 05 96 87 00 00 	mov    rax,QWORD PTR [rip+0x8796]        # 14000b580 <.refptr.__ImageBase>
   140002dea:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002dee:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002df2:	48 89 c1             	mov    rcx,rax
   140002df5:	e8 b6 fd ff ff       	call   140002bb0 <_ValidateImageBase>
   140002dfa:	85 c0                	test   eax,eax
   140002dfc:	75 07                	jne    140002e05 <__mingw_GetSectionCount+0x2a>
   140002dfe:	b8 00 00 00 00       	mov    eax,0x0
   140002e03:	eb 20                	jmp    140002e25 <__mingw_GetSectionCount+0x4a>
   140002e05:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e09:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e0c:	48 63 d0             	movsxd rdx,eax
   140002e0f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e13:	48 01 d0             	add    rax,rdx
   140002e16:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002e1a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002e1e:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002e22:	0f b7 c0             	movzx  eax,ax
   140002e25:	48 83 c4 30          	add    rsp,0x30
   140002e29:	5d                   	pop    rbp
   140002e2a:	c3                   	ret

0000000140002e2b <_FindPESectionExec>:
   140002e2b:	55                   	push   rbp
   140002e2c:	48 89 e5             	mov    rbp,rsp
   140002e2f:	48 83 ec 40          	sub    rsp,0x40
   140002e33:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002e37:	48 8b 05 42 87 00 00 	mov    rax,QWORD PTR [rip+0x8742]        # 14000b580 <.refptr.__ImageBase>
   140002e3e:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002e42:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e46:	48 89 c1             	mov    rcx,rax
   140002e49:	e8 62 fd ff ff       	call   140002bb0 <_ValidateImageBase>
   140002e4e:	85 c0                	test   eax,eax
   140002e50:	75 07                	jne    140002e59 <_FindPESectionExec+0x2e>
   140002e52:	b8 00 00 00 00       	mov    eax,0x0
   140002e57:	eb 78                	jmp    140002ed1 <_FindPESectionExec+0xa6>
   140002e59:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e5d:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e60:	48 63 d0             	movsxd rdx,eax
   140002e63:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e67:	48 01 d0             	add    rax,rdx
   140002e6a:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002e6e:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002e75:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e79:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002e7d:	0f b7 d0             	movzx  edx,ax
   140002e80:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e84:	48 01 d0             	add    rax,rdx
   140002e87:	48 83 c0 18          	add    rax,0x18
   140002e8b:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002e8f:	eb 2b                	jmp    140002ebc <_FindPESectionExec+0x91>
   140002e91:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e95:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002e98:	25 00 00 00 20       	and    eax,0x20000000
   140002e9d:	85 c0                	test   eax,eax
   140002e9f:	74 12                	je     140002eb3 <_FindPESectionExec+0x88>
   140002ea1:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140002ea6:	75 06                	jne    140002eae <_FindPESectionExec+0x83>
   140002ea8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002eac:	eb 23                	jmp    140002ed1 <_FindPESectionExec+0xa6>
   140002eae:	48 83 6d 10 01       	sub    QWORD PTR [rbp+0x10],0x1
   140002eb3:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002eb7:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002ebc:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002ec0:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002ec4:	0f b7 c0             	movzx  eax,ax
   140002ec7:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002eca:	72 c5                	jb     140002e91 <_FindPESectionExec+0x66>
   140002ecc:	b8 00 00 00 00       	mov    eax,0x0
   140002ed1:	48 83 c4 40          	add    rsp,0x40
   140002ed5:	5d                   	pop    rbp
   140002ed6:	c3                   	ret

0000000140002ed7 <_GetPEImageBase>:
   140002ed7:	55                   	push   rbp
   140002ed8:	48 89 e5             	mov    rbp,rsp
   140002edb:	48 83 ec 30          	sub    rsp,0x30
   140002edf:	48 8b 05 9a 86 00 00 	mov    rax,QWORD PTR [rip+0x869a]        # 14000b580 <.refptr.__ImageBase>
   140002ee6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002eea:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002eee:	48 89 c1             	mov    rcx,rax
   140002ef1:	e8 ba fc ff ff       	call   140002bb0 <_ValidateImageBase>
   140002ef6:	85 c0                	test   eax,eax
   140002ef8:	75 07                	jne    140002f01 <_GetPEImageBase+0x2a>
   140002efa:	b8 00 00 00 00       	mov    eax,0x0
   140002eff:	eb 04                	jmp    140002f05 <_GetPEImageBase+0x2e>
   140002f01:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f05:	48 83 c4 30          	add    rsp,0x30
   140002f09:	5d                   	pop    rbp
   140002f0a:	c3                   	ret

0000000140002f0b <_IsNonwritableInCurrentImage>:
   140002f0b:	55                   	push   rbp
   140002f0c:	48 89 e5             	mov    rbp,rsp
   140002f0f:	48 83 ec 40          	sub    rsp,0x40
   140002f13:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002f17:	48 8b 05 62 86 00 00 	mov    rax,QWORD PTR [rip+0x8662]        # 14000b580 <.refptr.__ImageBase>
   140002f1e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f22:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f26:	48 89 c1             	mov    rcx,rax
   140002f29:	e8 82 fc ff ff       	call   140002bb0 <_ValidateImageBase>
   140002f2e:	85 c0                	test   eax,eax
   140002f30:	75 07                	jne    140002f39 <_IsNonwritableInCurrentImage+0x2e>
   140002f32:	b8 00 00 00 00       	mov    eax,0x0
   140002f37:	eb 3d                	jmp    140002f76 <_IsNonwritableInCurrentImage+0x6b>
   140002f39:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002f3d:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002f41:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f45:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002f49:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f4d:	48 89 c1             	mov    rcx,rax
   140002f50:	e8 d7 fc ff ff       	call   140002c2c <_FindPESection>
   140002f55:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002f59:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   140002f5e:	75 07                	jne    140002f67 <_IsNonwritableInCurrentImage+0x5c>
   140002f60:	b8 00 00 00 00       	mov    eax,0x0
   140002f65:	eb 0f                	jmp    140002f76 <_IsNonwritableInCurrentImage+0x6b>
   140002f67:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f6b:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002f6e:	f7 d0                	not    eax
   140002f70:	c1 e8 1f             	shr    eax,0x1f
   140002f73:	0f b6 c0             	movzx  eax,al
   140002f76:	48 83 c4 40          	add    rsp,0x40
   140002f7a:	5d                   	pop    rbp
   140002f7b:	c3                   	ret

0000000140002f7c <__mingw_enum_import_library_names>:
   140002f7c:	55                   	push   rbp
   140002f7d:	48 89 e5             	mov    rbp,rsp
   140002f80:	48 83 ec 50          	sub    rsp,0x50
   140002f84:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002f87:	48 8b 05 f2 85 00 00 	mov    rax,QWORD PTR [rip+0x85f2]        # 14000b580 <.refptr.__ImageBase>
   140002f8e:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f92:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002f96:	48 89 c1             	mov    rcx,rax
   140002f99:	e8 12 fc ff ff       	call   140002bb0 <_ValidateImageBase>
   140002f9e:	85 c0                	test   eax,eax
   140002fa0:	75 0a                	jne    140002fac <__mingw_enum_import_library_names+0x30>
   140002fa2:	b8 00 00 00 00       	mov    eax,0x0
   140002fa7:	e9 ab 00 00 00       	jmp    140003057 <__mingw_enum_import_library_names+0xdb>
   140002fac:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fb0:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002fb3:	48 63 d0             	movsxd rdx,eax
   140002fb6:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fba:	48 01 d0             	add    rax,rdx
   140002fbd:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002fc1:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002fc5:	8b 80 90 00 00 00    	mov    eax,DWORD PTR [rax+0x90]
   140002fcb:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140002fce:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140002fd2:	75 07                	jne    140002fdb <__mingw_enum_import_library_names+0x5f>
   140002fd4:	b8 00 00 00 00       	mov    eax,0x0
   140002fd9:	eb 7c                	jmp    140003057 <__mingw_enum_import_library_names+0xdb>
   140002fdb:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   140002fde:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fe2:	48 89 c1             	mov    rcx,rax
   140002fe5:	e8 42 fc ff ff       	call   140002c2c <_FindPESection>
   140002fea:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002fee:	48 83 7d d8 00       	cmp    QWORD PTR [rbp-0x28],0x0
   140002ff3:	75 07                	jne    140002ffc <__mingw_enum_import_library_names+0x80>
   140002ff5:	b8 00 00 00 00       	mov    eax,0x0
   140002ffa:	eb 5b                	jmp    140003057 <__mingw_enum_import_library_names+0xdb>
   140002ffc:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   140002fff:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003003:	48 01 d0             	add    rax,rdx
   140003006:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000300a:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   14000300f:	75 07                	jne    140003018 <__mingw_enum_import_library_names+0x9c>
   140003011:	b8 00 00 00 00       	mov    eax,0x0
   140003016:	eb 3f                	jmp    140003057 <__mingw_enum_import_library_names+0xdb>
   140003018:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000301c:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000301f:	85 c0                	test   eax,eax
   140003021:	75 0b                	jne    14000302e <__mingw_enum_import_library_names+0xb2>
   140003023:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003027:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000302a:	85 c0                	test   eax,eax
   14000302c:	74 23                	je     140003051 <__mingw_enum_import_library_names+0xd5>
   14000302e:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   140003032:	7f 12                	jg     140003046 <__mingw_enum_import_library_names+0xca>
   140003034:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003038:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000303b:	89 c2                	mov    edx,eax
   14000303d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003041:	48 01 d0             	add    rax,rdx
   140003044:	eb 11                	jmp    140003057 <__mingw_enum_import_library_names+0xdb>
   140003046:	83 6d 10 01          	sub    DWORD PTR [rbp+0x10],0x1
   14000304a:	48 83 45 f8 14       	add    QWORD PTR [rbp-0x8],0x14
   14000304f:	eb c7                	jmp    140003018 <__mingw_enum_import_library_names+0x9c>
   140003051:	90                   	nop
   140003052:	b8 00 00 00 00       	mov    eax,0x0
   140003057:	48 83 c4 50          	add    rsp,0x50
   14000305b:	5d                   	pop    rbp
   14000305c:	c3                   	ret
   14000305d:	90                   	nop
   14000305e:	90                   	nop
   14000305f:	90                   	nop

0000000140003060 <___chkstk_ms>:
   140003060:	51                   	push   rcx
   140003061:	50                   	push   rax
   140003062:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003068:	48 8d 4c 24 18       	lea    rcx,[rsp+0x18]
   14000306d:	72 19                	jb     140003088 <___chkstk_ms+0x28>
   14000306f:	48 81 e9 00 10 00 00 	sub    rcx,0x1000
   140003076:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   14000307a:	48 2d 00 10 00 00    	sub    rax,0x1000
   140003080:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003086:	77 e7                	ja     14000306f <___chkstk_ms+0xf>
   140003088:	48 29 c1             	sub    rcx,rax
   14000308b:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   14000308f:	58                   	pop    rax
   140003090:	59                   	pop    rcx
   140003091:	c3                   	ret
   140003092:	90                   	nop
   140003093:	90                   	nop
   140003094:	90                   	nop
   140003095:	90                   	nop
   140003096:	90                   	nop
   140003097:	90                   	nop
   140003098:	90                   	nop
   140003099:	90                   	nop
   14000309a:	90                   	nop
   14000309b:	90                   	nop
   14000309c:	90                   	nop
   14000309d:	90                   	nop
   14000309e:	90                   	nop
   14000309f:	90                   	nop

00000001400030a0 <__mingw_printf>:
   1400030a0:	55                   	push   rbp
   1400030a1:	53                   	push   rbx
   1400030a2:	48 83 ec 48          	sub    rsp,0x48
   1400030a6:	48 8d 6c 24 40       	lea    rbp,[rsp+0x40]
   1400030ab:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   1400030af:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   1400030b3:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   1400030b7:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   1400030bb:	48 8d 45 28          	lea    rax,[rbp+0x28]
   1400030bf:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400030c3:	b9 01 00 00 00       	mov    ecx,0x1
   1400030c8:	e8 c3 5e 00 00       	call   140008f90 <__acrt_iob_func>
   1400030cd:	48 89 c1             	mov    rcx,rax
   1400030d0:	e8 3b 5d 00 00       	call   140008e10 <_lock_file>
   1400030d5:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   1400030d9:	b9 01 00 00 00       	mov    ecx,0x1
   1400030de:	e8 ad 5e 00 00       	call   140008f90 <__acrt_iob_func>
   1400030e3:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   1400030e7:	48 89 5c 24 20       	mov    QWORD PTR [rsp+0x20],rbx
   1400030ec:	49 89 d1             	mov    r9,rdx
   1400030ef:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400030f5:	48 89 c2             	mov    rdx,rax
   1400030f8:	b9 00 60 00 00       	mov    ecx,0x6000
   1400030fd:	e8 b1 1f 00 00       	call   1400050b3 <__mingw_pformat>
   140003102:	89 c3                	mov    ebx,eax
   140003104:	b9 01 00 00 00       	mov    ecx,0x1
   140003109:	e8 82 5e 00 00       	call   140008f90 <__acrt_iob_func>
   14000310e:	48 89 c1             	mov    rcx,rax
   140003111:	e8 84 5d 00 00       	call   140008e9a <_unlock_file>
   140003116:	89 d8                	mov    eax,ebx
   140003118:	48 83 c4 48          	add    rsp,0x48
   14000311c:	5b                   	pop    rbx
   14000311d:	5d                   	pop    rbp
   14000311e:	c3                   	ret
   14000311f:	90                   	nop

0000000140003120 <__pformat_putc>:
   140003120:	55                   	push   rbp
   140003121:	48 89 e5             	mov    rbp,rsp
   140003124:	48 83 ec 20          	sub    rsp,0x20
   140003128:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000312b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000312f:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003133:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003136:	25 00 40 00 00       	and    eax,0x4000
   14000313b:	85 c0                	test   eax,eax
   14000313d:	75 12                	jne    140003151 <__pformat_putc+0x31>
   14000313f:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003143:	8b 50 28             	mov    edx,DWORD PTR [rax+0x28]
   140003146:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000314a:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   14000314d:	39 c2                	cmp    edx,eax
   14000314f:	7e 3b                	jle    14000318c <__pformat_putc+0x6c>
   140003151:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003155:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003158:	25 00 20 00 00       	and    eax,0x2000
   14000315d:	85 c0                	test   eax,eax
   14000315f:	74 13                	je     140003174 <__pformat_putc+0x54>
   140003161:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003165:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   140003168:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   14000316b:	89 c1                	mov    ecx,eax
   14000316d:	e8 56 64 00 00       	call   1400095c8 <fputc>
   140003172:	eb 18                	jmp    14000318c <__pformat_putc+0x6c>
   140003174:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003178:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   14000317b:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000317f:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140003182:	48 98                	cdqe
   140003184:	48 01 d0             	add    rax,rdx
   140003187:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   14000318a:	88 10                	mov    BYTE PTR [rax],dl
   14000318c:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003190:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140003193:	8d 50 01             	lea    edx,[rax+0x1]
   140003196:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000319a:	89 50 24             	mov    DWORD PTR [rax+0x24],edx
   14000319d:	90                   	nop
   14000319e:	48 83 c4 20          	add    rsp,0x20
   1400031a2:	5d                   	pop    rbp
   1400031a3:	c3                   	ret

00000001400031a4 <__pformat_putchars>:
   1400031a4:	55                   	push   rbp
   1400031a5:	48 89 e5             	mov    rbp,rsp
   1400031a8:	48 83 ec 20          	sub    rsp,0x20
   1400031ac:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400031b0:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   1400031b3:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400031b7:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031bb:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400031be:	85 c0                	test   eax,eax
   1400031c0:	78 16                	js     1400031d8 <__pformat_putchars+0x34>
   1400031c2:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031c6:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400031c9:	39 45 18             	cmp    DWORD PTR [rbp+0x18],eax
   1400031cc:	7e 0a                	jle    1400031d8 <__pformat_putchars+0x34>
   1400031ce:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031d2:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400031d5:	89 45 18             	mov    DWORD PTR [rbp+0x18],eax
   1400031d8:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031dc:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400031df:	39 45 18             	cmp    DWORD PTR [rbp+0x18],eax
   1400031e2:	7d 15                	jge    1400031f9 <__pformat_putchars+0x55>
   1400031e4:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031e8:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400031eb:	2b 45 18             	sub    eax,DWORD PTR [rbp+0x18]
   1400031ee:	89 c2                	mov    edx,eax
   1400031f0:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031f4:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   1400031f7:	eb 0b                	jmp    140003204 <__pformat_putchars+0x60>
   1400031f9:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031fd:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   140003204:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003208:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000320b:	85 c0                	test   eax,eax
   14000320d:	7e 57                	jle    140003266 <__pformat_putchars+0xc2>
   14000320f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003213:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003216:	25 00 04 00 00       	and    eax,0x400
   14000321b:	85 c0                	test   eax,eax
   14000321d:	75 47                	jne    140003266 <__pformat_putchars+0xc2>
   14000321f:	eb 11                	jmp    140003232 <__pformat_putchars+0x8e>
   140003221:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003225:	48 89 c2             	mov    rdx,rax
   140003228:	b9 20 00 00 00       	mov    ecx,0x20
   14000322d:	e8 ee fe ff ff       	call   140003120 <__pformat_putc>
   140003232:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003236:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003239:	8d 48 ff             	lea    ecx,[rax-0x1]
   14000323c:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   140003240:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140003243:	85 c0                	test   eax,eax
   140003245:	75 da                	jne    140003221 <__pformat_putchars+0x7d>
   140003247:	eb 1d                	jmp    140003266 <__pformat_putchars+0xc2>
   140003249:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000324d:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003251:	48 89 55 10          	mov    QWORD PTR [rbp+0x10],rdx
   140003255:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140003258:	0f be c0             	movsx  eax,al
   14000325b:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   14000325f:	89 c1                	mov    ecx,eax
   140003261:	e8 ba fe ff ff       	call   140003120 <__pformat_putc>
   140003266:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140003269:	8d 50 ff             	lea    edx,[rax-0x1]
   14000326c:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   14000326f:	85 c0                	test   eax,eax
   140003271:	75 d6                	jne    140003249 <__pformat_putchars+0xa5>
   140003273:	eb 11                	jmp    140003286 <__pformat_putchars+0xe2>
   140003275:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003279:	48 89 c2             	mov    rdx,rax
   14000327c:	b9 20 00 00 00       	mov    ecx,0x20
   140003281:	e8 9a fe ff ff       	call   140003120 <__pformat_putc>
   140003286:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000328a:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000328d:	8d 48 ff             	lea    ecx,[rax-0x1]
   140003290:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   140003294:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140003297:	85 c0                	test   eax,eax
   140003299:	7f da                	jg     140003275 <__pformat_putchars+0xd1>
   14000329b:	90                   	nop
   14000329c:	90                   	nop
   14000329d:	48 83 c4 20          	add    rsp,0x20
   1400032a1:	5d                   	pop    rbp
   1400032a2:	c3                   	ret

00000001400032a3 <__pformat_puts>:
   1400032a3:	55                   	push   rbp
   1400032a4:	48 89 e5             	mov    rbp,rsp
   1400032a7:	48 83 ec 20          	sub    rsp,0x20
   1400032ab:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400032af:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400032b3:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   1400032b8:	75 0b                	jne    1400032c5 <__pformat_puts+0x22>
   1400032ba:	48 8d 05 6f 80 00 00 	lea    rax,[rip+0x806f]        # 14000b330 <.rdata>
   1400032c1:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   1400032c5:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400032c9:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400032cc:	85 c0                	test   eax,eax
   1400032ce:	78 2f                	js     1400032ff <__pformat_puts+0x5c>
   1400032d0:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400032d4:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400032d7:	48 63 d0             	movsxd rdx,eax
   1400032da:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400032de:	48 89 c1             	mov    rcx,rax
   1400032e1:	e8 4a 5a 00 00       	call   140008d30 <strnlen>
   1400032e6:	89 c1                	mov    ecx,eax
   1400032e8:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400032ec:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400032f0:	49 89 d0             	mov    r8,rdx
   1400032f3:	89 ca                	mov    edx,ecx
   1400032f5:	48 89 c1             	mov    rcx,rax
   1400032f8:	e8 a7 fe ff ff       	call   1400031a4 <__pformat_putchars>
   1400032fd:	eb 23                	jmp    140003322 <__pformat_puts+0x7f>
   1400032ff:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140003303:	48 89 c1             	mov    rcx,rax
   140003306:	e8 fd 62 00 00       	call   140009608 <strlen>
   14000330b:	89 c1                	mov    ecx,eax
   14000330d:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140003311:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140003315:	49 89 d0             	mov    r8,rdx
   140003318:	89 ca                	mov    edx,ecx
   14000331a:	48 89 c1             	mov    rcx,rax
   14000331d:	e8 82 fe ff ff       	call   1400031a4 <__pformat_putchars>
   140003322:	90                   	nop
   140003323:	48 83 c4 20          	add    rsp,0x20
   140003327:	5d                   	pop    rbp
   140003328:	c3                   	ret

0000000140003329 <__pformat_wputchars>:
   140003329:	55                   	push   rbp
   14000332a:	48 89 e5             	mov    rbp,rsp
   14000332d:	48 83 ec 50          	sub    rsp,0x50
   140003331:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140003335:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140003338:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   14000333c:	48 c7 45 d8 00 00 00 	mov    QWORD PTR [rbp-0x28],0x0
   140003343:	00 
   140003344:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003348:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   14000334b:	85 c0                	test   eax,eax
   14000334d:	78 16                	js     140003365 <__pformat_wputchars+0x3c>
   14000334f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003353:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003356:	39 45 18             	cmp    DWORD PTR [rbp+0x18],eax
   140003359:	7e 0a                	jle    140003365 <__pformat_wputchars+0x3c>
   14000335b:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000335f:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003362:	89 45 18             	mov    DWORD PTR [rbp+0x18],eax
   140003365:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003369:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000336c:	39 45 18             	cmp    DWORD PTR [rbp+0x18],eax
   14000336f:	7d 15                	jge    140003386 <__pformat_wputchars+0x5d>
   140003371:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003375:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003378:	2b 45 18             	sub    eax,DWORD PTR [rbp+0x18]
   14000337b:	89 c2                	mov    edx,eax
   14000337d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003381:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140003384:	eb 0b                	jmp    140003391 <__pformat_wputchars+0x68>
   140003386:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000338a:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   140003391:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003395:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003398:	85 c0                	test   eax,eax
   14000339a:	7e 6e                	jle    14000340a <__pformat_wputchars+0xe1>
   14000339c:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400033a0:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400033a3:	25 00 04 00 00       	and    eax,0x400
   1400033a8:	85 c0                	test   eax,eax
   1400033aa:	75 5e                	jne    14000340a <__pformat_wputchars+0xe1>
   1400033ac:	eb 11                	jmp    1400033bf <__pformat_wputchars+0x96>
   1400033ae:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400033b2:	48 89 c2             	mov    rdx,rax
   1400033b5:	b9 20 00 00 00       	mov    ecx,0x20
   1400033ba:	e8 61 fd ff ff       	call   140003120 <__pformat_putc>
   1400033bf:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400033c3:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400033c6:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400033c9:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   1400033cd:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   1400033d0:	85 c0                	test   eax,eax
   1400033d2:	75 da                	jne    1400033ae <__pformat_wputchars+0x85>
   1400033d4:	eb 34                	jmp    14000340a <__pformat_wputchars+0xe1>
   1400033d6:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   1400033da:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400033de:	eb 1d                	jmp    1400033fd <__pformat_wputchars+0xd4>
   1400033e0:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400033e4:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400033e8:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400033ec:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400033ef:	0f be c0             	movsx  eax,al
   1400033f2:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   1400033f6:	89 c1                	mov    ecx,eax
   1400033f8:	e8 23 fd ff ff       	call   140003120 <__pformat_putc>
   1400033fd:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003400:	8d 50 ff             	lea    edx,[rax-0x1]
   140003403:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003406:	85 c0                	test   eax,eax
   140003408:	7f d6                	jg     1400033e0 <__pformat_wputchars+0xb7>
   14000340a:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   14000340d:	8d 50 ff             	lea    edx,[rax-0x1]
   140003410:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140003413:	85 c0                	test   eax,eax
   140003415:	7e 41                	jle    140003458 <__pformat_wputchars+0x12f>
   140003417:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000341b:	48 8d 50 02          	lea    rdx,[rax+0x2]
   14000341f:	48 89 55 10          	mov    QWORD PTR [rbp+0x10],rdx
   140003423:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140003426:	0f b7 d0             	movzx  edx,ax
   140003429:	48 8d 4d d8          	lea    rcx,[rbp-0x28]
   14000342d:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140003431:	49 89 c8             	mov    r8,rcx
   140003434:	48 89 c1             	mov    rcx,rax
   140003437:	e8 84 5b 00 00       	call   140008fc0 <wcrtomb>
   14000343c:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   14000343f:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003443:	7f 91                	jg     1400033d6 <__pformat_wputchars+0xad>
   140003445:	eb 11                	jmp    140003458 <__pformat_wputchars+0x12f>
   140003447:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000344b:	48 89 c2             	mov    rdx,rax
   14000344e:	b9 20 00 00 00       	mov    ecx,0x20
   140003453:	e8 c8 fc ff ff       	call   140003120 <__pformat_putc>
   140003458:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000345c:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000345f:	8d 48 ff             	lea    ecx,[rax-0x1]
   140003462:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   140003466:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140003469:	85 c0                	test   eax,eax
   14000346b:	7f da                	jg     140003447 <__pformat_wputchars+0x11e>
   14000346d:	90                   	nop
   14000346e:	90                   	nop
   14000346f:	48 83 c4 50          	add    rsp,0x50
   140003473:	5d                   	pop    rbp
   140003474:	c3                   	ret

0000000140003475 <__pformat_wcputs>:
   140003475:	55                   	push   rbp
   140003476:	48 89 e5             	mov    rbp,rsp
   140003479:	48 83 ec 20          	sub    rsp,0x20
   14000347d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140003481:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140003485:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   14000348a:	75 0b                	jne    140003497 <__pformat_wcputs+0x22>
   14000348c:	48 8d 05 a5 7e 00 00 	lea    rax,[rip+0x7ea5]        # 14000b338 <.rdata+0x8>
   140003493:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140003497:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000349b:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   14000349e:	85 c0                	test   eax,eax
   1400034a0:	78 2f                	js     1400034d1 <__pformat_wcputs+0x5c>
   1400034a2:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400034a6:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400034a9:	48 63 d0             	movsxd rdx,eax
   1400034ac:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400034b0:	48 89 c1             	mov    rcx,rax
   1400034b3:	e8 28 58 00 00       	call   140008ce0 <wcsnlen>
   1400034b8:	89 c1                	mov    ecx,eax
   1400034ba:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400034be:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400034c2:	49 89 d0             	mov    r8,rdx
   1400034c5:	89 ca                	mov    edx,ecx
   1400034c7:	48 89 c1             	mov    rcx,rax
   1400034ca:	e8 5a fe ff ff       	call   140003329 <__pformat_wputchars>
   1400034cf:	eb 23                	jmp    1400034f4 <__pformat_wcputs+0x7f>
   1400034d1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400034d5:	48 89 c1             	mov    rcx,rax
   1400034d8:	e8 43 61 00 00       	call   140009620 <wcslen>
   1400034dd:	89 c1                	mov    ecx,eax
   1400034df:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400034e3:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400034e7:	49 89 d0             	mov    r8,rdx
   1400034ea:	89 ca                	mov    edx,ecx
   1400034ec:	48 89 c1             	mov    rcx,rax
   1400034ef:	e8 35 fe ff ff       	call   140003329 <__pformat_wputchars>
   1400034f4:	90                   	nop
   1400034f5:	48 83 c4 20          	add    rsp,0x20
   1400034f9:	5d                   	pop    rbp
   1400034fa:	c3                   	ret

00000001400034fb <__pformat_int_bufsiz>:
   1400034fb:	55                   	push   rbp
   1400034fc:	48 89 e5             	mov    rbp,rsp
   1400034ff:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140003502:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140003505:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140003509:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   14000350c:	83 e8 01             	sub    eax,0x1
   14000350f:	48 98                	cdqe
   140003511:	48 83 c0 40          	add    rax,0x40
   140003515:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   140003518:	48 63 ca             	movsxd rcx,edx
   14000351b:	ba 00 00 00 00       	mov    edx,0x0
   140003520:	48 f7 f1             	div    rcx
   140003523:	89 c2                	mov    edx,eax
   140003525:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140003528:	01 d0                	add    eax,edx
   14000352a:	89 45 18             	mov    DWORD PTR [rbp+0x18],eax
   14000352d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003531:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003534:	ba 00 00 00 00       	mov    edx,0x0
   140003539:	85 c0                	test   eax,eax
   14000353b:	0f 48 c2             	cmovs  eax,edx
   14000353e:	01 45 18             	add    DWORD PTR [rbp+0x18],eax
   140003541:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003545:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003548:	25 00 10 00 00       	and    eax,0x1000
   14000354d:	85 c0                	test   eax,eax
   14000354f:	74 29                	je     14000357a <__pformat_int_bufsiz+0x7f>
   140003551:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003555:	0f b7 40 20          	movzx  eax,WORD PTR [rax+0x20]
   140003559:	66 85 c0             	test   ax,ax
   14000355c:	74 1c                	je     14000357a <__pformat_int_bufsiz+0x7f>
   14000355e:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140003561:	48 63 d0             	movsxd rdx,eax
   140003564:	48 69 d2 56 55 55 55 	imul   rdx,rdx,0x55555556
   14000356b:	48 89 d1             	mov    rcx,rdx
   14000356e:	48 c1 e9 20          	shr    rcx,0x20
   140003572:	99                   	cdq
   140003573:	89 c8                	mov    eax,ecx
   140003575:	29 d0                	sub    eax,edx
   140003577:	01 45 18             	add    DWORD PTR [rbp+0x18],eax
   14000357a:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000357e:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140003581:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140003584:	39 c2                	cmp    edx,eax
   140003586:	0f 4d c2             	cmovge eax,edx
   140003589:	5d                   	pop    rbp
   14000358a:	c3                   	ret

000000014000358b <__pformat_int>:
   14000358b:	55                   	push   rbp
   14000358c:	53                   	push   rbx
   14000358d:	48 83 ec 58          	sub    rsp,0x58
   140003591:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140003596:	48 89 cb             	mov    rbx,rcx
   140003599:	48 8b 0b             	mov    rcx,QWORD PTR [rbx]
   14000359c:	48 8b 5b 08          	mov    rbx,QWORD PTR [rbx+0x8]
   1400035a0:	48 89 4d d0          	mov    QWORD PTR [rbp-0x30],rcx
   1400035a4:	48 89 5d d8          	mov    QWORD PTR [rbp-0x28],rbx
   1400035a8:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   1400035ac:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400035b0:	49 89 c0             	mov    r8,rax
   1400035b3:	ba 03 00 00 00       	mov    edx,0x3
   1400035b8:	b9 01 00 00 00       	mov    ecx,0x1
   1400035bd:	e8 39 ff ff ff       	call   1400034fb <__pformat_int_bufsiz>
   1400035c2:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   1400035c5:	48 c7 45 e8 00 00 00 	mov    QWORD PTR [rbp-0x18],0x0
   1400035cc:	00 
   1400035cd:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   1400035d0:	48 98                	cdqe
   1400035d2:	48 83 c0 0f          	add    rax,0xf
   1400035d6:	48 c1 e8 04          	shr    rax,0x4
   1400035da:	48 c1 e0 04          	shl    rax,0x4
   1400035de:	e8 7d fa ff ff       	call   140003060 <___chkstk_ms>
   1400035e3:	48 29 c4             	sub    rsp,rax
   1400035e6:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   1400035eb:	48 83 c0 0f          	add    rax,0xf
   1400035ef:	48 c1 e8 04          	shr    rax,0x4
   1400035f3:	48 c1 e0 04          	shl    rax,0x4
   1400035f7:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400035fb:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400035ff:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003603:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003607:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000360a:	25 80 00 00 00       	and    eax,0x80
   14000360f:	85 c0                	test   eax,eax
   140003611:	0f 84 ea 00 00 00    	je     140003701 <__pformat_int+0x176>
   140003617:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   14000361b:	48 85 c0             	test   rax,rax
   14000361e:	79 10                	jns    140003630 <__pformat_int+0xa5>
   140003620:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140003624:	48 f7 d8             	neg    rax
   140003627:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   14000362b:	e9 d1 00 00 00       	jmp    140003701 <__pformat_int+0x176>
   140003630:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003634:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003637:	24 7f                	and    al,0x7f
   140003639:	89 c2                	mov    edx,eax
   14000363b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000363f:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140003642:	e9 ba 00 00 00       	jmp    140003701 <__pformat_int+0x176>
   140003647:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000364b:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   14000364f:	74 54                	je     1400036a5 <__pformat_int+0x11a>
   140003651:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003655:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003658:	25 00 10 00 00       	and    eax,0x1000
   14000365d:	85 c0                	test   eax,eax
   14000365f:	74 44                	je     1400036a5 <__pformat_int+0x11a>
   140003661:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003665:	0f b7 40 20          	movzx  eax,WORD PTR [rax+0x20]
   140003669:	66 85 c0             	test   ax,ax
   14000366c:	74 37                	je     1400036a5 <__pformat_int+0x11a>
   14000366e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003672:	48 2b 45 e8          	sub    rax,QWORD PTR [rbp-0x18]
   140003676:	48 89 c2             	mov    rdx,rax
   140003679:	48 89 d0             	mov    rax,rdx
   14000367c:	48 c1 f8 3f          	sar    rax,0x3f
   140003680:	48 c1 e8 3e          	shr    rax,0x3e
   140003684:	48 01 c2             	add    rdx,rax
   140003687:	83 e2 03             	and    edx,0x3
   14000368a:	48 29 c2             	sub    rdx,rax
   14000368d:	48 89 d0             	mov    rax,rdx
   140003690:	48 83 f8 03          	cmp    rax,0x3
   140003694:	75 0f                	jne    1400036a5 <__pformat_int+0x11a>
   140003696:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000369a:	48 8d 50 01          	lea    rdx,[rax+0x1]
   14000369e:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   1400036a2:	c6 00 2c             	mov    BYTE PTR [rax],0x2c
   1400036a5:	48 8b 4d d0          	mov    rcx,QWORD PTR [rbp-0x30]
   1400036a9:	48 ba cd cc cc cc cc 	movabs rdx,0xcccccccccccccccd
   1400036b0:	cc cc cc 
   1400036b3:	48 89 c8             	mov    rax,rcx
   1400036b6:	48 f7 e2             	mul    rdx
   1400036b9:	48 c1 ea 03          	shr    rdx,0x3
   1400036bd:	48 89 d0             	mov    rax,rdx
   1400036c0:	48 c1 e0 02          	shl    rax,0x2
   1400036c4:	48 01 d0             	add    rax,rdx
   1400036c7:	48 01 c0             	add    rax,rax
   1400036ca:	48 29 c1             	sub    rcx,rax
   1400036cd:	48 89 ca             	mov    rdx,rcx
   1400036d0:	89 d0                	mov    eax,edx
   1400036d2:	8d 48 30             	lea    ecx,[rax+0x30]
   1400036d5:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400036d9:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400036dd:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   1400036e1:	89 ca                	mov    edx,ecx
   1400036e3:	88 10                	mov    BYTE PTR [rax],dl
   1400036e5:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400036e9:	48 ba cd cc cc cc cc 	movabs rdx,0xcccccccccccccccd
   1400036f0:	cc cc cc 
   1400036f3:	48 f7 e2             	mul    rdx
   1400036f6:	48 89 d0             	mov    rax,rdx
   1400036f9:	48 c1 e8 03          	shr    rax,0x3
   1400036fd:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140003701:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140003705:	48 85 c0             	test   rax,rax
   140003708:	0f 85 39 ff ff ff    	jne    140003647 <__pformat_int+0xbc>
   14000370e:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003712:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003715:	85 c0                	test   eax,eax
   140003717:	7e 3e                	jle    140003757 <__pformat_int+0x1cc>
   140003719:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000371d:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003720:	89 c1                	mov    ecx,eax
   140003722:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003726:	48 2b 45 e8          	sub    rax,QWORD PTR [rbp-0x18]
   14000372a:	89 c2                	mov    edx,eax
   14000372c:	89 c8                	mov    eax,ecx
   14000372e:	29 d0                	sub    eax,edx
   140003730:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140003733:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   140003737:	7e 1e                	jle    140003757 <__pformat_int+0x1cc>
   140003739:	eb 0f                	jmp    14000374a <__pformat_int+0x1bf>
   14000373b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000373f:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003743:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140003747:	c6 00 30             	mov    BYTE PTR [rax],0x30
   14000374a:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000374d:	8d 50 ff             	lea    edx,[rax-0x1]
   140003750:	89 55 f4             	mov    DWORD PTR [rbp-0xc],edx
   140003753:	85 c0                	test   eax,eax
   140003755:	7f e4                	jg     14000373b <__pformat_int+0x1b0>
   140003757:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000375b:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   14000375f:	75 1a                	jne    14000377b <__pformat_int+0x1f0>
   140003761:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003765:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003768:	85 c0                	test   eax,eax
   14000376a:	74 0f                	je     14000377b <__pformat_int+0x1f0>
   14000376c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003770:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003774:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140003778:	c6 00 30             	mov    BYTE PTR [rax],0x30
   14000377b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000377f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003782:	85 c0                	test   eax,eax
   140003784:	0f 8e ce 00 00 00    	jle    140003858 <__pformat_int+0x2cd>
   14000378a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000378e:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003791:	89 c1                	mov    ecx,eax
   140003793:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003797:	48 2b 45 e8          	sub    rax,QWORD PTR [rbp-0x18]
   14000379b:	89 c2                	mov    edx,eax
   14000379d:	89 c8                	mov    eax,ecx
   14000379f:	29 d0                	sub    eax,edx
   1400037a1:	89 c2                	mov    edx,eax
   1400037a3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037a7:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   1400037aa:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037ae:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400037b1:	85 c0                	test   eax,eax
   1400037b3:	0f 8e 9f 00 00 00    	jle    140003858 <__pformat_int+0x2cd>
   1400037b9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037bd:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400037c0:	25 c0 01 00 00       	and    eax,0x1c0
   1400037c5:	85 c0                	test   eax,eax
   1400037c7:	74 11                	je     1400037da <__pformat_int+0x24f>
   1400037c9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037cd:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400037d0:	8d 50 ff             	lea    edx,[rax-0x1]
   1400037d3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037d7:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   1400037da:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037de:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400037e1:	85 c0                	test   eax,eax
   1400037e3:	79 3b                	jns    140003820 <__pformat_int+0x295>
   1400037e5:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037e9:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400037ec:	25 00 06 00 00       	and    eax,0x600
   1400037f1:	3d 00 02 00 00       	cmp    eax,0x200
   1400037f6:	75 28                	jne    140003820 <__pformat_int+0x295>
   1400037f8:	eb 0f                	jmp    140003809 <__pformat_int+0x27e>
   1400037fa:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400037fe:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003802:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140003806:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003809:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000380d:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003810:	8d 48 ff             	lea    ecx,[rax-0x1]
   140003813:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140003817:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   14000381a:	85 c0                	test   eax,eax
   14000381c:	7f dc                	jg     1400037fa <__pformat_int+0x26f>
   14000381e:	eb 38                	jmp    140003858 <__pformat_int+0x2cd>
   140003820:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003824:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003827:	25 00 04 00 00       	and    eax,0x400
   14000382c:	85 c0                	test   eax,eax
   14000382e:	75 28                	jne    140003858 <__pformat_int+0x2cd>
   140003830:	eb 11                	jmp    140003843 <__pformat_int+0x2b8>
   140003832:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003836:	48 89 c2             	mov    rdx,rax
   140003839:	b9 20 00 00 00       	mov    ecx,0x20
   14000383e:	e8 dd f8 ff ff       	call   140003120 <__pformat_putc>
   140003843:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003847:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000384a:	8d 48 ff             	lea    ecx,[rax-0x1]
   14000384d:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140003851:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140003854:	85 c0                	test   eax,eax
   140003856:	7f da                	jg     140003832 <__pformat_int+0x2a7>
   140003858:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000385c:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000385f:	25 80 00 00 00       	and    eax,0x80
   140003864:	85 c0                	test   eax,eax
   140003866:	74 11                	je     140003879 <__pformat_int+0x2ee>
   140003868:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000386c:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003870:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140003874:	c6 00 2d             	mov    BYTE PTR [rax],0x2d
   140003877:	eb 5a                	jmp    1400038d3 <__pformat_int+0x348>
   140003879:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000387d:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003880:	25 00 01 00 00       	and    eax,0x100
   140003885:	85 c0                	test   eax,eax
   140003887:	74 11                	je     14000389a <__pformat_int+0x30f>
   140003889:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000388d:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003891:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140003895:	c6 00 2b             	mov    BYTE PTR [rax],0x2b
   140003898:	eb 39                	jmp    1400038d3 <__pformat_int+0x348>
   14000389a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000389e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400038a1:	83 e0 40             	and    eax,0x40
   1400038a4:	85 c0                	test   eax,eax
   1400038a6:	74 2b                	je     1400038d3 <__pformat_int+0x348>
   1400038a8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400038ac:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400038b0:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   1400038b4:	c6 00 20             	mov    BYTE PTR [rax],0x20
   1400038b7:	eb 1a                	jmp    1400038d3 <__pformat_int+0x348>
   1400038b9:	48 83 6d f8 01       	sub    QWORD PTR [rbp-0x8],0x1
   1400038be:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400038c2:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400038c5:	0f be c0             	movsx  eax,al
   1400038c8:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400038cc:	89 c1                	mov    ecx,eax
   1400038ce:	e8 4d f8 ff ff       	call   140003120 <__pformat_putc>
   1400038d3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400038d7:	48 39 45 e8          	cmp    QWORD PTR [rbp-0x18],rax
   1400038db:	72 dc                	jb     1400038b9 <__pformat_int+0x32e>
   1400038dd:	eb 11                	jmp    1400038f0 <__pformat_int+0x365>
   1400038df:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400038e3:	48 89 c2             	mov    rdx,rax
   1400038e6:	b9 20 00 00 00       	mov    ecx,0x20
   1400038eb:	e8 30 f8 ff ff       	call   140003120 <__pformat_putc>
   1400038f0:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400038f4:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400038f7:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400038fa:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400038fe:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140003901:	85 c0                	test   eax,eax
   140003903:	7f da                	jg     1400038df <__pformat_int+0x354>
   140003905:	90                   	nop
   140003906:	90                   	nop
   140003907:	48 8d 65 08          	lea    rsp,[rbp+0x8]
   14000390b:	5b                   	pop    rbx
   14000390c:	5d                   	pop    rbp
   14000390d:	c3                   	ret

000000014000390e <__pformat_xint>:
   14000390e:	55                   	push   rbp
   14000390f:	53                   	push   rbx
   140003910:	48 83 ec 68          	sub    rsp,0x68
   140003914:	48 8d 6c 24 60       	lea    rbp,[rsp+0x60]
   140003919:	89 4d 20             	mov    DWORD PTR [rbp+0x20],ecx
   14000391c:	48 89 d3             	mov    rbx,rdx
   14000391f:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140003922:	48 8b 53 08          	mov    rdx,QWORD PTR [rbx+0x8]
   140003926:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   14000392a:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
   14000392e:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140003932:	83 7d 20 6f          	cmp    DWORD PTR [rbp+0x20],0x6f
   140003936:	74 1e                	je     140003956 <__pformat_xint+0x48>
   140003938:	83 7d 20 62          	cmp    DWORD PTR [rbp+0x20],0x62
   14000393c:	74 06                	je     140003944 <__pformat_xint+0x36>
   14000393e:	83 7d 20 42          	cmp    DWORD PTR [rbp+0x20],0x42
   140003942:	75 09                	jne    14000394d <__pformat_xint+0x3f>
   140003944:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   14000394b:	eb 10                	jmp    14000395d <__pformat_xint+0x4f>
   14000394d:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140003954:	eb 07                	jmp    14000395d <__pformat_xint+0x4f>
   140003956:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   14000395d:	48 8b 55 30          	mov    rdx,QWORD PTR [rbp+0x30]
   140003961:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003964:	49 89 d0             	mov    r8,rdx
   140003967:	89 c2                	mov    edx,eax
   140003969:	b9 02 00 00 00       	mov    ecx,0x2
   14000396e:	e8 88 fb ff ff       	call   1400034fb <__pformat_int_bufsiz>
   140003973:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140003976:	48 c7 45 e0 00 00 00 	mov    QWORD PTR [rbp-0x20],0x0
   14000397d:	00 
   14000397e:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140003981:	48 98                	cdqe
   140003983:	48 83 c0 0f          	add    rax,0xf
   140003987:	48 c1 e8 04          	shr    rax,0x4
   14000398b:	48 c1 e0 04          	shl    rax,0x4
   14000398f:	e8 cc f6 ff ff       	call   140003060 <___chkstk_ms>
   140003994:	48 29 c4             	sub    rsp,rax
   140003997:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   14000399c:	48 83 c0 0f          	add    rax,0xf
   1400039a0:	48 c1 e8 04          	shr    rax,0x4
   1400039a4:	48 c1 e0 04          	shl    rax,0x4
   1400039a8:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400039ac:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400039b0:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400039b4:	83 7d 20 6f          	cmp    DWORD PTR [rbp+0x20],0x6f
   1400039b8:	74 1e                	je     1400039d8 <__pformat_xint+0xca>
   1400039ba:	83 7d 20 62          	cmp    DWORD PTR [rbp+0x20],0x62
   1400039be:	74 06                	je     1400039c6 <__pformat_xint+0xb8>
   1400039c0:	83 7d 20 42          	cmp    DWORD PTR [rbp+0x20],0x42
   1400039c4:	75 09                	jne    1400039cf <__pformat_xint+0xc1>
   1400039c6:	c7 45 ec 01 00 00 00 	mov    DWORD PTR [rbp-0x14],0x1
   1400039cd:	eb 10                	jmp    1400039df <__pformat_xint+0xd1>
   1400039cf:	c7 45 ec 0f 00 00 00 	mov    DWORD PTR [rbp-0x14],0xf
   1400039d6:	eb 67                	jmp    140003a3f <__pformat_xint+0x131>
   1400039d8:	c7 45 ec 07 00 00 00 	mov    DWORD PTR [rbp-0x14],0x7
   1400039df:	eb 5e                	jmp    140003a3f <__pformat_xint+0x131>
   1400039e1:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   1400039e5:	89 c2                	mov    edx,eax
   1400039e7:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
   1400039ea:	21 d0                	and    eax,edx
   1400039ec:	8d 48 30             	lea    ecx,[rax+0x30]
   1400039ef:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400039f3:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400039f7:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400039fb:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   1400039ff:	89 ca                	mov    edx,ecx
   140003a01:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003a05:	88 10                	mov    BYTE PTR [rax],dl
   140003a07:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003a0b:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140003a0e:	3c 39                	cmp    al,0x39
   140003a10:	7e 1a                	jle    140003a2c <__pformat_xint+0x11e>
   140003a12:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003a16:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140003a19:	83 c0 07             	add    eax,0x7
   140003a1c:	89 c2                	mov    edx,eax
   140003a1e:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140003a21:	83 e0 20             	and    eax,0x20
   140003a24:	09 c2                	or     edx,eax
   140003a26:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003a2a:	88 10                	mov    BYTE PTR [rax],dl
   140003a2c:	48 8b 55 c0          	mov    rdx,QWORD PTR [rbp-0x40]
   140003a30:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003a33:	89 c1                	mov    ecx,eax
   140003a35:	48 d3 ea             	shr    rdx,cl
   140003a38:	48 89 d0             	mov    rax,rdx
   140003a3b:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   140003a3f:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140003a43:	48 85 c0             	test   rax,rax
   140003a46:	75 99                	jne    1400039e1 <__pformat_xint+0xd3>
   140003a48:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003a4c:	48 3b 45 e0          	cmp    rax,QWORD PTR [rbp-0x20]
   140003a50:	75 13                	jne    140003a65 <__pformat_xint+0x157>
   140003a52:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003a56:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003a59:	80 e4 f7             	and    ah,0xf7
   140003a5c:	89 c2                	mov    edx,eax
   140003a5e:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003a62:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140003a65:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003a69:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003a6c:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003a6f:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003a73:	7e 3a                	jle    140003aaf <__pformat_xint+0x1a1>
   140003a75:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   140003a78:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003a7c:	48 2b 45 e0          	sub    rax,QWORD PTR [rbp-0x20]
   140003a80:	89 c1                	mov    ecx,eax
   140003a82:	89 d0                	mov    eax,edx
   140003a84:	29 c8                	sub    eax,ecx
   140003a86:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003a89:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003a8d:	7e 20                	jle    140003aaf <__pformat_xint+0x1a1>
   140003a8f:	eb 0f                	jmp    140003aa0 <__pformat_xint+0x192>
   140003a91:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003a95:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003a99:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003a9d:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003aa0:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003aa3:	8d 50 ff             	lea    edx,[rax-0x1]
   140003aa6:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003aa9:	85 c0                	test   eax,eax
   140003aab:	7f e4                	jg     140003a91 <__pformat_xint+0x183>
   140003aad:	eb 25                	jmp    140003ad4 <__pformat_xint+0x1c6>
   140003aaf:	83 7d 20 6f          	cmp    DWORD PTR [rbp+0x20],0x6f
   140003ab3:	75 1f                	jne    140003ad4 <__pformat_xint+0x1c6>
   140003ab5:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003ab9:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003abc:	25 00 08 00 00       	and    eax,0x800
   140003ac1:	85 c0                	test   eax,eax
   140003ac3:	74 0f                	je     140003ad4 <__pformat_xint+0x1c6>
   140003ac5:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003ac9:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003acd:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003ad1:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003ad4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003ad8:	48 3b 45 e0          	cmp    rax,QWORD PTR [rbp-0x20]
   140003adc:	75 1a                	jne    140003af8 <__pformat_xint+0x1ea>
   140003ade:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003ae2:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003ae5:	85 c0                	test   eax,eax
   140003ae7:	74 0f                	je     140003af8 <__pformat_xint+0x1ea>
   140003ae9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003aed:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003af1:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003af5:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003af8:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003afc:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003aff:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140003b03:	48 2b 55 e0          	sub    rdx,QWORD PTR [rbp-0x20]
   140003b07:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003b0a:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140003b0d:	7d 15                	jge    140003b24 <__pformat_xint+0x216>
   140003b0f:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b13:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003b16:	2b 45 fc             	sub    eax,DWORD PTR [rbp-0x4]
   140003b19:	89 c2                	mov    edx,eax
   140003b1b:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b1f:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140003b22:	eb 0b                	jmp    140003b2f <__pformat_xint+0x221>
   140003b24:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b28:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   140003b2f:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b33:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003b36:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003b39:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003b3d:	7e 1a                	jle    140003b59 <__pformat_xint+0x24b>
   140003b3f:	83 7d 20 6f          	cmp    DWORD PTR [rbp+0x20],0x6f
   140003b43:	74 14                	je     140003b59 <__pformat_xint+0x24b>
   140003b45:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b49:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003b4c:	25 00 08 00 00       	and    eax,0x800
   140003b51:	85 c0                	test   eax,eax
   140003b53:	74 04                	je     140003b59 <__pformat_xint+0x24b>
   140003b55:	83 6d fc 02          	sub    DWORD PTR [rbp-0x4],0x2
   140003b59:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003b5d:	7e 3c                	jle    140003b9b <__pformat_xint+0x28d>
   140003b5f:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b63:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003b66:	85 c0                	test   eax,eax
   140003b68:	79 31                	jns    140003b9b <__pformat_xint+0x28d>
   140003b6a:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b6e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003b71:	25 00 06 00 00       	and    eax,0x600
   140003b76:	3d 00 02 00 00       	cmp    eax,0x200
   140003b7b:	75 1e                	jne    140003b9b <__pformat_xint+0x28d>
   140003b7d:	eb 0f                	jmp    140003b8e <__pformat_xint+0x280>
   140003b7f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003b83:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003b87:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003b8b:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003b8e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003b91:	8d 50 ff             	lea    edx,[rax-0x1]
   140003b94:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003b97:	85 c0                	test   eax,eax
   140003b99:	7f e4                	jg     140003b7f <__pformat_xint+0x271>
   140003b9b:	83 7d 20 6f          	cmp    DWORD PTR [rbp+0x20],0x6f
   140003b9f:	74 30                	je     140003bd1 <__pformat_xint+0x2c3>
   140003ba1:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003ba5:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003ba8:	25 00 08 00 00       	and    eax,0x800
   140003bad:	85 c0                	test   eax,eax
   140003baf:	74 20                	je     140003bd1 <__pformat_xint+0x2c3>
   140003bb1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003bb5:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003bb9:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003bbd:	8b 55 20             	mov    edx,DWORD PTR [rbp+0x20]
   140003bc0:	88 10                	mov    BYTE PTR [rax],dl
   140003bc2:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003bc6:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003bca:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003bce:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003bd1:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003bd5:	7e 4c                	jle    140003c23 <__pformat_xint+0x315>
   140003bd7:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003bdb:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003bde:	25 00 04 00 00       	and    eax,0x400
   140003be3:	85 c0                	test   eax,eax
   140003be5:	75 3c                	jne    140003c23 <__pformat_xint+0x315>
   140003be7:	eb 11                	jmp    140003bfa <__pformat_xint+0x2ec>
   140003be9:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003bed:	48 89 c2             	mov    rdx,rax
   140003bf0:	b9 20 00 00 00       	mov    ecx,0x20
   140003bf5:	e8 26 f5 ff ff       	call   140003120 <__pformat_putc>
   140003bfa:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003bfd:	8d 50 ff             	lea    edx,[rax-0x1]
   140003c00:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003c03:	85 c0                	test   eax,eax
   140003c05:	7f e2                	jg     140003be9 <__pformat_xint+0x2db>
   140003c07:	eb 1a                	jmp    140003c23 <__pformat_xint+0x315>
   140003c09:	48 83 6d f0 01       	sub    QWORD PTR [rbp-0x10],0x1
   140003c0e:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003c12:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140003c15:	0f be c0             	movsx  eax,al
   140003c18:	48 8b 55 30          	mov    rdx,QWORD PTR [rbp+0x30]
   140003c1c:	89 c1                	mov    ecx,eax
   140003c1e:	e8 fd f4 ff ff       	call   140003120 <__pformat_putc>
   140003c23:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003c27:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   140003c2b:	72 dc                	jb     140003c09 <__pformat_xint+0x2fb>
   140003c2d:	eb 11                	jmp    140003c40 <__pformat_xint+0x332>
   140003c2f:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003c33:	48 89 c2             	mov    rdx,rax
   140003c36:	b9 20 00 00 00       	mov    ecx,0x20
   140003c3b:	e8 e0 f4 ff ff       	call   140003120 <__pformat_putc>
   140003c40:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003c43:	8d 50 ff             	lea    edx,[rax-0x1]
   140003c46:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003c49:	85 c0                	test   eax,eax
   140003c4b:	7f e2                	jg     140003c2f <__pformat_xint+0x321>
   140003c4d:	90                   	nop
   140003c4e:	90                   	nop
   140003c4f:	48 8d 65 08          	lea    rsp,[rbp+0x8]
   140003c53:	5b                   	pop    rbx
   140003c54:	5d                   	pop    rbp
   140003c55:	c3                   	ret

0000000140003c56 <init_fpreg_ldouble>:
   140003c56:	55                   	push   rbp
   140003c57:	53                   	push   rbx
   140003c58:	48 83 ec 28          	sub    rsp,0x28
   140003c5c:	48 8d 6c 24 20       	lea    rbp,[rsp+0x20]
   140003c61:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140003c65:	48 89 d3             	mov    rbx,rdx
   140003c68:	db 2b                	fld    TBYTE PTR [rbx]
   140003c6a:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   140003c6d:	db 6d e0             	fld    TBYTE PTR [rbp-0x20]
   140003c70:	db 7d f0             	fstp   TBYTE PTR [rbp-0x10]
   140003c73:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140003c77:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003c7b:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140003c7f:	48 89 01             	mov    QWORD PTR [rcx],rax
   140003c82:	48 89 51 08          	mov    QWORD PTR [rcx+0x8],rdx
   140003c86:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003c8a:	48 83 c4 28          	add    rsp,0x28
   140003c8e:	5b                   	pop    rbx
   140003c8f:	5d                   	pop    rbp
   140003c90:	c3                   	ret

0000000140003c91 <__pformat_cvt>:
   140003c91:	55                   	push   rbp
   140003c92:	53                   	push   rbx
   140003c93:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140003c9a:	48 8d ac 24 80 00 00 	lea    rbp,[rsp+0x80]
   140003ca1:	00 
   140003ca2:	89 4d 20             	mov    DWORD PTR [rbp+0x20],ecx
   140003ca5:	48 89 d3             	mov    rbx,rdx
   140003ca8:	db 2b                	fld    TBYTE PTR [rbx]
   140003caa:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140003cad:	44 89 45 30          	mov    DWORD PTR [rbp+0x30],r8d
   140003cb1:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140003cb5:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140003cbc:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140003cc0:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140003cc3:	db 7d c0             	fstp   TBYTE PTR [rbp-0x40]
   140003cc6:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140003cca:	48 89 c1             	mov    rcx,rax
   140003ccd:	e8 84 ff ff ff       	call   140003c56 <init_fpreg_ldouble>
   140003cd2:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140003cd5:	db 7d c0             	fstp   TBYTE PTR [rbp-0x40]
   140003cd8:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140003cdc:	48 89 c1             	mov    rcx,rax
   140003cdf:	e8 9c 4e 00 00       	call   140008b80 <__fpclassifyl>
   140003ce4:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140003ce7:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003cea:	25 00 01 00 00       	and    eax,0x100
   140003cef:	85 c0                	test   eax,eax
   140003cf1:	74 1d                	je     140003d10 <__pformat_cvt+0x7f>
   140003cf3:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003cf6:	25 00 04 00 00       	and    eax,0x400
   140003cfb:	85 c0                	test   eax,eax
   140003cfd:	74 07                	je     140003d06 <__pformat_cvt+0x75>
   140003cff:	b8 03 00 00 00       	mov    eax,0x3
   140003d04:	eb 05                	jmp    140003d0b <__pformat_cvt+0x7a>
   140003d06:	b8 04 00 00 00       	mov    eax,0x4
   140003d0b:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140003d0e:	eb 4a                	jmp    140003d5a <__pformat_cvt+0xc9>
   140003d10:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003d13:	25 00 04 00 00       	and    eax,0x400
   140003d18:	85 c0                	test   eax,eax
   140003d1a:	74 37                	je     140003d53 <__pformat_cvt+0xc2>
   140003d1c:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003d1f:	25 00 40 00 00       	and    eax,0x4000
   140003d24:	85 c0                	test   eax,eax
   140003d26:	74 10                	je     140003d38 <__pformat_cvt+0xa7>
   140003d28:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140003d2f:	c7 45 fc c3 bf ff ff 	mov    DWORD PTR [rbp-0x4],0xffffbfc3
   140003d36:	eb 22                	jmp    140003d5a <__pformat_cvt+0xc9>
   140003d38:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140003d3f:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140003d43:	98                   	cwde
   140003d44:	25 ff 7f 00 00       	and    eax,0x7fff
   140003d49:	2d 3e 40 00 00       	sub    eax,0x403e
   140003d4e:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003d51:	eb 07                	jmp    140003d5a <__pformat_cvt+0xc9>
   140003d53:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140003d5a:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003d5d:	83 f8 04             	cmp    eax,0x4
   140003d60:	74 0e                	je     140003d70 <__pformat_cvt+0xdf>
   140003d62:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140003d66:	98                   	cwde
   140003d67:	25 00 80 00 00       	and    eax,0x8000
   140003d6c:	89 c2                	mov    edx,eax
   140003d6e:	eb 05                	jmp    140003d75 <__pformat_cvt+0xe4>
   140003d70:	ba 00 00 00 00       	mov    edx,0x0
   140003d75:	48 8b 45 40          	mov    rax,QWORD PTR [rbp+0x40]
   140003d79:	89 10                	mov    DWORD PTR [rax],edx
   140003d7b:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003d7e:	4c 8d 4d f8          	lea    r9,[rbp-0x8]
   140003d82:	4c 8d 45 e0          	lea    r8,[rbp-0x20]
   140003d86:	48 8d 0d f3 62 00 00 	lea    rcx,[rip+0x62f3]        # 14000a080 <fpi.0>
   140003d8d:	48 8d 55 f0          	lea    rdx,[rbp-0x10]
   140003d91:	48 89 54 24 38       	mov    QWORD PTR [rsp+0x38],rdx
   140003d96:	48 8b 55 38          	mov    rdx,QWORD PTR [rbp+0x38]
   140003d9a:	48 89 54 24 30       	mov    QWORD PTR [rsp+0x30],rdx
   140003d9f:	8b 55 30             	mov    edx,DWORD PTR [rbp+0x30]
   140003da2:	89 54 24 28          	mov    DWORD PTR [rsp+0x28],edx
   140003da6:	8b 55 20             	mov    edx,DWORD PTR [rbp+0x20]
   140003da9:	89 54 24 20          	mov    DWORD PTR [rsp+0x20],edx
   140003dad:	89 c2                	mov    edx,eax
   140003daf:	e8 96 24 00 00       	call   14000624a <__gdtoa>
   140003db4:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140003dbb:	5b                   	pop    rbx
   140003dbc:	5d                   	pop    rbp
   140003dbd:	c3                   	ret

0000000140003dbe <__pformat_ecvt>:
   140003dbe:	55                   	push   rbp
   140003dbf:	53                   	push   rbx
   140003dc0:	48 83 ec 58          	sub    rsp,0x58
   140003dc4:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140003dc9:	48 89 cb             	mov    rbx,rcx
   140003dcc:	db 2b                	fld    TBYTE PTR [rbx]
   140003dce:	db 7d f0             	fstp   TBYTE PTR [rbp-0x10]
   140003dd1:	89 55 28             	mov    DWORD PTR [rbp+0x28],edx
   140003dd4:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140003dd8:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140003ddc:	db 6d f0             	fld    TBYTE PTR [rbp-0x10]
   140003ddf:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   140003de2:	4c 8b 45 30          	mov    r8,QWORD PTR [rbp+0x30]
   140003de6:	8b 4d 28             	mov    ecx,DWORD PTR [rbp+0x28]
   140003de9:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140003ded:	48 8b 55 38          	mov    rdx,QWORD PTR [rbp+0x38]
   140003df1:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   140003df6:	4d 89 c1             	mov    r9,r8
   140003df9:	41 89 c8             	mov    r8d,ecx
   140003dfc:	48 89 c2             	mov    rdx,rax
   140003dff:	b9 02 00 00 00       	mov    ecx,0x2
   140003e04:	e8 88 fe ff ff       	call   140003c91 <__pformat_cvt>
   140003e09:	48 83 c4 58          	add    rsp,0x58
   140003e0d:	5b                   	pop    rbx
   140003e0e:	5d                   	pop    rbp
   140003e0f:	c3                   	ret

0000000140003e10 <__pformat_fcvt>:
   140003e10:	55                   	push   rbp
   140003e11:	53                   	push   rbx
   140003e12:	48 83 ec 58          	sub    rsp,0x58
   140003e16:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140003e1b:	48 89 cb             	mov    rbx,rcx
   140003e1e:	db 2b                	fld    TBYTE PTR [rbx]
   140003e20:	db 7d f0             	fstp   TBYTE PTR [rbp-0x10]
   140003e23:	89 55 28             	mov    DWORD PTR [rbp+0x28],edx
   140003e26:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140003e2a:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140003e2e:	db 6d f0             	fld    TBYTE PTR [rbp-0x10]
   140003e31:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   140003e34:	4c 8b 45 30          	mov    r8,QWORD PTR [rbp+0x30]
   140003e38:	8b 4d 28             	mov    ecx,DWORD PTR [rbp+0x28]
   140003e3b:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140003e3f:	48 8b 55 38          	mov    rdx,QWORD PTR [rbp+0x38]
   140003e43:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   140003e48:	4d 89 c1             	mov    r9,r8
   140003e4b:	41 89 c8             	mov    r8d,ecx
   140003e4e:	48 89 c2             	mov    rdx,rax
   140003e51:	b9 03 00 00 00       	mov    ecx,0x3
   140003e56:	e8 36 fe ff ff       	call   140003c91 <__pformat_cvt>
   140003e5b:	48 83 c4 58          	add    rsp,0x58
   140003e5f:	5b                   	pop    rbx
   140003e60:	5d                   	pop    rbp
   140003e61:	c3                   	ret

0000000140003e62 <__pformat_emit_radix_point>:
   140003e62:	55                   	push   rbp
   140003e63:	53                   	push   rbx
   140003e64:	48 83 ec 68          	sub    rsp,0x68
   140003e68:	48 8d 6c 24 60       	lea    rbp,[rsp+0x60]
   140003e6d:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140003e71:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003e75:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140003e78:	83 f8 fd             	cmp    eax,0xfffffffd
   140003e7b:	75 48                	jne    140003ec5 <__pformat_emit_radix_point+0x63>
   140003e7d:	48 c7 45 cc 00 00 00 	mov    QWORD PTR [rbp-0x34],0x0
   140003e84:	00 
   140003e85:	e8 4e 57 00 00       	call   1400095d8 <localeconv>
   140003e8a:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   140003e8d:	48 8d 4d cc          	lea    rcx,[rbp-0x34]
   140003e91:	48 8d 45 d6          	lea    rax,[rbp-0x2a]
   140003e95:	49 89 c9             	mov    r9,rcx
   140003e98:	41 b8 10 00 00 00    	mov    r8d,0x10
   140003e9e:	48 89 c1             	mov    rcx,rax
   140003ea1:	e8 6a 51 00 00       	call   140009010 <mbrtowc>
   140003ea6:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   140003ea9:	83 7d ec 00          	cmp    DWORD PTR [rbp-0x14],0x0
   140003ead:	7e 0c                	jle    140003ebb <__pformat_emit_radix_point+0x59>
   140003eaf:	0f b7 55 d6          	movzx  edx,WORD PTR [rbp-0x2a]
   140003eb3:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003eb7:	66 89 50 18          	mov    WORD PTR [rax+0x18],dx
   140003ebb:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003ebf:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   140003ec2:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140003ec5:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003ec9:	0f b7 40 18          	movzx  eax,WORD PTR [rax+0x18]
   140003ecd:	66 85 c0             	test   ax,ax
   140003ed0:	0f 84 b8 00 00 00    	je     140003f8e <__pformat_emit_radix_point+0x12c>
   140003ed6:	48 89 e0             	mov    rax,rsp
   140003ed9:	48 89 c3             	mov    rbx,rax
   140003edc:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003ee0:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140003ee3:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003ee6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003ee9:	48 63 d0             	movsxd rdx,eax
   140003eec:	48 83 ea 01          	sub    rdx,0x1
   140003ef0:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   140003ef4:	48 98                	cdqe
   140003ef6:	48 83 c0 0f          	add    rax,0xf
   140003efa:	48 c1 e8 04          	shr    rax,0x4
   140003efe:	48 c1 e0 04          	shl    rax,0x4
   140003f02:	e8 59 f1 ff ff       	call   140003060 <___chkstk_ms>
   140003f07:	48 29 c4             	sub    rsp,rax
   140003f0a:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   140003f0f:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140003f13:	48 c7 45 c4 00 00 00 	mov    QWORD PTR [rbp-0x3c],0x0
   140003f1a:	00 
   140003f1b:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003f1f:	0f b7 40 18          	movzx  eax,WORD PTR [rax+0x18]
   140003f23:	0f b7 d0             	movzx  edx,ax
   140003f26:	48 8d 4d c4          	lea    rcx,[rbp-0x3c]
   140003f2a:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003f2e:	49 89 c8             	mov    r8,rcx
   140003f31:	48 89 c1             	mov    rcx,rax
   140003f34:	e8 87 50 00 00       	call   140008fc0 <wcrtomb>
   140003f39:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003f3c:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003f40:	7e 36                	jle    140003f78 <__pformat_emit_radix_point+0x116>
   140003f42:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003f46:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140003f4a:	eb 1d                	jmp    140003f69 <__pformat_emit_radix_point+0x107>
   140003f4c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003f50:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003f54:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003f58:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140003f5b:	0f be c0             	movsx  eax,al
   140003f5e:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   140003f62:	89 c1                	mov    ecx,eax
   140003f64:	e8 b7 f1 ff ff       	call   140003120 <__pformat_putc>
   140003f69:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003f6c:	8d 50 ff             	lea    edx,[rax-0x1]
   140003f6f:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003f72:	85 c0                	test   eax,eax
   140003f74:	7f d6                	jg     140003f4c <__pformat_emit_radix_point+0xea>
   140003f76:	eb 11                	jmp    140003f89 <__pformat_emit_radix_point+0x127>
   140003f78:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003f7c:	48 89 c2             	mov    rdx,rax
   140003f7f:	b9 2e 00 00 00       	mov    ecx,0x2e
   140003f84:	e8 97 f1 ff ff       	call   140003120 <__pformat_putc>
   140003f89:	48 89 dc             	mov    rsp,rbx
   140003f8c:	eb 11                	jmp    140003f9f <__pformat_emit_radix_point+0x13d>
   140003f8e:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003f92:	48 89 c2             	mov    rdx,rax
   140003f95:	b9 2e 00 00 00       	mov    ecx,0x2e
   140003f9a:	e8 81 f1 ff ff       	call   140003120 <__pformat_putc>
   140003f9f:	90                   	nop
   140003fa0:	48 8d 65 08          	lea    rsp,[rbp+0x8]
   140003fa4:	5b                   	pop    rbx
   140003fa5:	5d                   	pop    rbp
   140003fa6:	c3                   	ret

0000000140003fa7 <__pformat_emit_numeric_value>:
   140003fa7:	55                   	push   rbp
   140003fa8:	48 89 e5             	mov    rbp,rsp
   140003fab:	48 83 ec 30          	sub    rsp,0x30
   140003faf:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140003fb2:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140003fb6:	83 7d 10 2e          	cmp    DWORD PTR [rbp+0x10],0x2e
   140003fba:	75 0e                	jne    140003fca <__pformat_emit_numeric_value+0x23>
   140003fbc:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003fc0:	48 89 c1             	mov    rcx,rax
   140003fc3:	e8 9a fe ff ff       	call   140003e62 <__pformat_emit_radix_point>
   140003fc8:	eb 43                	jmp    14000400d <__pformat_emit_numeric_value+0x66>
   140003fca:	83 7d 10 2c          	cmp    DWORD PTR [rbp+0x10],0x2c
   140003fce:	75 2f                	jne    140003fff <__pformat_emit_numeric_value+0x58>
   140003fd0:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003fd4:	0f b7 40 20          	movzx  eax,WORD PTR [rax+0x20]
   140003fd8:	66 89 45 fe          	mov    WORD PTR [rbp-0x2],ax
   140003fdc:	0f b7 45 fe          	movzx  eax,WORD PTR [rbp-0x2]
   140003fe0:	66 85 c0             	test   ax,ax
   140003fe3:	74 28                	je     14000400d <__pformat_emit_numeric_value+0x66>
   140003fe5:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140003fe9:	48 8d 45 fe          	lea    rax,[rbp-0x2]
   140003fed:	49 89 d0             	mov    r8,rdx
   140003ff0:	ba 01 00 00 00       	mov    edx,0x1
   140003ff5:	48 89 c1             	mov    rcx,rax
   140003ff8:	e8 2c f3 ff ff       	call   140003329 <__pformat_wputchars>
   140003ffd:	eb 0e                	jmp    14000400d <__pformat_emit_numeric_value+0x66>
   140003fff:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140004003:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140004006:	89 c1                	mov    ecx,eax
   140004008:	e8 13 f1 ff ff       	call   140003120 <__pformat_putc>
   14000400d:	90                   	nop
   14000400e:	48 83 c4 30          	add    rsp,0x30
   140004012:	5d                   	pop    rbp
   140004013:	c3                   	ret

0000000140004014 <__pformat_emit_inf_or_nan>:
   140004014:	55                   	push   rbp
   140004015:	48 89 e5             	mov    rbp,rsp
   140004018:	48 83 ec 40          	sub    rsp,0x40
   14000401c:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000401f:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140004023:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140004027:	48 8d 45 ec          	lea    rax,[rbp-0x14]
   14000402b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000402f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140004033:	c7 40 10 ff ff ff ff 	mov    DWORD PTR [rax+0x10],0xffffffff
   14000403a:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   14000403e:	74 11                	je     140004051 <__pformat_emit_inf_or_nan+0x3d>
   140004040:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140004044:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004048:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   14000404c:	c6 00 2d             	mov    BYTE PTR [rax],0x2d
   14000404f:	eb 3e                	jmp    14000408f <__pformat_emit_inf_or_nan+0x7b>
   140004051:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140004055:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004058:	25 00 01 00 00       	and    eax,0x100
   14000405d:	85 c0                	test   eax,eax
   14000405f:	74 11                	je     140004072 <__pformat_emit_inf_or_nan+0x5e>
   140004061:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140004065:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004069:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   14000406d:	c6 00 2b             	mov    BYTE PTR [rax],0x2b
   140004070:	eb 1d                	jmp    14000408f <__pformat_emit_inf_or_nan+0x7b>
   140004072:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140004076:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004079:	83 e0 40             	and    eax,0x40
   14000407c:	85 c0                	test   eax,eax
   14000407e:	74 0f                	je     14000408f <__pformat_emit_inf_or_nan+0x7b>
   140004080:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140004084:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004088:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   14000408c:	c6 00 20             	mov    BYTE PTR [rax],0x20
   14000408f:	c7 45 fc 03 00 00 00 	mov    DWORD PTR [rbp-0x4],0x3
   140004096:	eb 38                	jmp    1400040d0 <__pformat_emit_inf_or_nan+0xbc>
   140004098:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000409c:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400040a0:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400040a4:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400040a7:	83 e0 df             	and    eax,0xffffffdf
   1400040aa:	41 89 c0             	mov    r8d,eax
   1400040ad:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400040b1:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400040b4:	83 e0 20             	and    eax,0x20
   1400040b7:	89 c1                	mov    ecx,eax
   1400040b9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400040bd:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400040c1:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400040c5:	44 89 c2             	mov    edx,r8d
   1400040c8:	09 ca                	or     edx,ecx
   1400040ca:	88 10                	mov    BYTE PTR [rax],dl
   1400040cc:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   1400040d0:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   1400040d4:	7f c2                	jg     140004098 <__pformat_emit_inf_or_nan+0x84>
   1400040d6:	48 8d 45 ec          	lea    rax,[rbp-0x14]
   1400040da:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   1400040de:	48 29 c2             	sub    rdx,rax
   1400040e1:	89 d1                	mov    ecx,edx
   1400040e3:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   1400040e7:	48 8d 45 ec          	lea    rax,[rbp-0x14]
   1400040eb:	49 89 d0             	mov    r8,rdx
   1400040ee:	89 ca                	mov    edx,ecx
   1400040f0:	48 89 c1             	mov    rcx,rax
   1400040f3:	e8 ac f0 ff ff       	call   1400031a4 <__pformat_putchars>
   1400040f8:	90                   	nop
   1400040f9:	48 83 c4 40          	add    rsp,0x40
   1400040fd:	5d                   	pop    rbp
   1400040fe:	c3                   	ret

00000001400040ff <__pformat_emit_float>:
   1400040ff:	55                   	push   rbp
   140004100:	48 89 e5             	mov    rbp,rsp
   140004103:	48 83 ec 30          	sub    rsp,0x30
   140004107:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000410a:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000410e:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d
   140004112:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140004116:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   14000411a:	7e 2e                	jle    14000414a <__pformat_emit_float+0x4b>
   14000411c:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004120:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004123:	39 45 20             	cmp    DWORD PTR [rbp+0x20],eax
   140004126:	7f 15                	jg     14000413d <__pformat_emit_float+0x3e>
   140004128:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000412c:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000412f:	2b 45 20             	sub    eax,DWORD PTR [rbp+0x20]
   140004132:	89 c2                	mov    edx,eax
   140004134:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004138:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   14000413b:	eb 29                	jmp    140004166 <__pformat_emit_float+0x67>
   14000413d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004141:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   140004148:	eb 1c                	jmp    140004166 <__pformat_emit_float+0x67>
   14000414a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000414e:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004151:	85 c0                	test   eax,eax
   140004153:	7e 11                	jle    140004166 <__pformat_emit_float+0x67>
   140004155:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004159:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000415c:	8d 50 ff             	lea    edx,[rax-0x1]
   14000415f:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004163:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004166:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000416a:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000416d:	85 c0                	test   eax,eax
   14000416f:	78 2b                	js     14000419c <__pformat_emit_float+0x9d>
   140004171:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004175:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140004178:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000417c:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   14000417f:	39 c2                	cmp    edx,eax
   140004181:	7e 19                	jle    14000419c <__pformat_emit_float+0x9d>
   140004183:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004187:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   14000418a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000418e:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004191:	29 c2                	sub    edx,eax
   140004193:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004197:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   14000419a:	eb 0b                	jmp    1400041a7 <__pformat_emit_float+0xa8>
   14000419c:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041a0:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   1400041a7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041ab:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400041ae:	85 c0                	test   eax,eax
   1400041b0:	7e 2c                	jle    1400041de <__pformat_emit_float+0xdf>
   1400041b2:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041b6:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400041b9:	85 c0                	test   eax,eax
   1400041bb:	7f 10                	jg     1400041cd <__pformat_emit_float+0xce>
   1400041bd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041c1:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400041c4:	25 00 08 00 00       	and    eax,0x800
   1400041c9:	85 c0                	test   eax,eax
   1400041cb:	74 11                	je     1400041de <__pformat_emit_float+0xdf>
   1400041cd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041d1:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400041d4:	8d 50 ff             	lea    edx,[rax-0x1]
   1400041d7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041db:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   1400041de:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   1400041e2:	7e 64                	jle    140004248 <__pformat_emit_float+0x149>
   1400041e4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041e8:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400041eb:	25 00 10 00 00       	and    eax,0x1000
   1400041f0:	85 c0                	test   eax,eax
   1400041f2:	74 54                	je     140004248 <__pformat_emit_float+0x149>
   1400041f4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041f8:	0f b7 40 20          	movzx  eax,WORD PTR [rax+0x20]
   1400041fc:	66 85 c0             	test   ax,ax
   1400041ff:	74 47                	je     140004248 <__pformat_emit_float+0x149>
   140004201:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140004204:	83 c0 02             	add    eax,0x2
   140004207:	48 63 d0             	movsxd rdx,eax
   14000420a:	48 69 d2 56 55 55 55 	imul   rdx,rdx,0x55555556
   140004211:	48 c1 ea 20          	shr    rdx,0x20
   140004215:	c1 f8 1f             	sar    eax,0x1f
   140004218:	29 c2                	sub    edx,eax
   14000421a:	8d 42 ff             	lea    eax,[rdx-0x1]
   14000421d:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140004220:	eb 15                	jmp    140004237 <__pformat_emit_float+0x138>
   140004222:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   140004226:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000422a:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000422d:	8d 50 ff             	lea    edx,[rax-0x1]
   140004230:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004234:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004237:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   14000423b:	7e 0b                	jle    140004248 <__pformat_emit_float+0x149>
   14000423d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004241:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004244:	85 c0                	test   eax,eax
   140004246:	7f da                	jg     140004222 <__pformat_emit_float+0x123>
   140004248:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000424c:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000424f:	85 c0                	test   eax,eax
   140004251:	7e 27                	jle    14000427a <__pformat_emit_float+0x17b>
   140004253:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   140004257:	75 10                	jne    140004269 <__pformat_emit_float+0x16a>
   140004259:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000425d:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004260:	25 c0 01 00 00       	and    eax,0x1c0
   140004265:	85 c0                	test   eax,eax
   140004267:	74 11                	je     14000427a <__pformat_emit_float+0x17b>
   140004269:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000426d:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004270:	8d 50 ff             	lea    edx,[rax-0x1]
   140004273:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004277:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   14000427a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000427e:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004281:	85 c0                	test   eax,eax
   140004283:	7e 38                	jle    1400042bd <__pformat_emit_float+0x1be>
   140004285:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004289:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000428c:	25 00 06 00 00       	and    eax,0x600
   140004291:	85 c0                	test   eax,eax
   140004293:	75 28                	jne    1400042bd <__pformat_emit_float+0x1be>
   140004295:	eb 11                	jmp    1400042a8 <__pformat_emit_float+0x1a9>
   140004297:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000429b:	48 89 c2             	mov    rdx,rax
   14000429e:	b9 20 00 00 00       	mov    ecx,0x20
   1400042a3:	e8 78 ee ff ff       	call   140003120 <__pformat_putc>
   1400042a8:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400042ac:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400042af:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400042b2:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400042b6:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   1400042b9:	85 c0                	test   eax,eax
   1400042bb:	7f da                	jg     140004297 <__pformat_emit_float+0x198>
   1400042bd:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   1400042c1:	74 13                	je     1400042d6 <__pformat_emit_float+0x1d7>
   1400042c3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400042c7:	48 89 c2             	mov    rdx,rax
   1400042ca:	b9 2d 00 00 00       	mov    ecx,0x2d
   1400042cf:	e8 4c ee ff ff       	call   140003120 <__pformat_putc>
   1400042d4:	eb 42                	jmp    140004318 <__pformat_emit_float+0x219>
   1400042d6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400042da:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400042dd:	25 00 01 00 00       	and    eax,0x100
   1400042e2:	85 c0                	test   eax,eax
   1400042e4:	74 13                	je     1400042f9 <__pformat_emit_float+0x1fa>
   1400042e6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400042ea:	48 89 c2             	mov    rdx,rax
   1400042ed:	b9 2b 00 00 00       	mov    ecx,0x2b
   1400042f2:	e8 29 ee ff ff       	call   140003120 <__pformat_putc>
   1400042f7:	eb 1f                	jmp    140004318 <__pformat_emit_float+0x219>
   1400042f9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400042fd:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004300:	83 e0 40             	and    eax,0x40
   140004303:	85 c0                	test   eax,eax
   140004305:	74 11                	je     140004318 <__pformat_emit_float+0x219>
   140004307:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000430b:	48 89 c2             	mov    rdx,rax
   14000430e:	b9 20 00 00 00       	mov    ecx,0x20
   140004313:	e8 08 ee ff ff       	call   140003120 <__pformat_putc>
   140004318:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000431c:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000431f:	85 c0                	test   eax,eax
   140004321:	7e 3b                	jle    14000435e <__pformat_emit_float+0x25f>
   140004323:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004327:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000432a:	25 00 06 00 00       	and    eax,0x600
   14000432f:	3d 00 02 00 00       	cmp    eax,0x200
   140004334:	75 28                	jne    14000435e <__pformat_emit_float+0x25f>
   140004336:	eb 11                	jmp    140004349 <__pformat_emit_float+0x24a>
   140004338:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000433c:	48 89 c2             	mov    rdx,rax
   14000433f:	b9 30 00 00 00       	mov    ecx,0x30
   140004344:	e8 d7 ed ff ff       	call   140003120 <__pformat_putc>
   140004349:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000434d:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004350:	8d 48 ff             	lea    ecx,[rax-0x1]
   140004353:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004357:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   14000435a:	85 c0                	test   eax,eax
   14000435c:	7f da                	jg     140004338 <__pformat_emit_float+0x239>
   14000435e:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   140004362:	0f 8e a7 00 00 00    	jle    14000440f <__pformat_emit_float+0x310>
   140004368:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000436c:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   14000436f:	84 c0                	test   al,al
   140004371:	74 14                	je     140004387 <__pformat_emit_float+0x288>
   140004373:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140004377:	48 8d 50 01          	lea    rdx,[rax+0x1]
   14000437b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000437f:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140004382:	0f be c0             	movsx  eax,al
   140004385:	eb 05                	jmp    14000438c <__pformat_emit_float+0x28d>
   140004387:	b8 30 00 00 00       	mov    eax,0x30
   14000438c:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004390:	89 c1                	mov    ecx,eax
   140004392:	e8 89 ed ff ff       	call   140003120 <__pformat_putc>
   140004397:	83 6d 20 01          	sub    DWORD PTR [rbp+0x20],0x1
   14000439b:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   14000439f:	74 62                	je     140004403 <__pformat_emit_float+0x304>
   1400043a1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400043a5:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400043a8:	25 00 10 00 00       	and    eax,0x1000
   1400043ad:	85 c0                	test   eax,eax
   1400043af:	74 52                	je     140004403 <__pformat_emit_float+0x304>
   1400043b1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400043b5:	0f b7 40 20          	movzx  eax,WORD PTR [rax+0x20]
   1400043b9:	66 85 c0             	test   ax,ax
   1400043bc:	74 45                	je     140004403 <__pformat_emit_float+0x304>
   1400043be:	8b 4d 20             	mov    ecx,DWORD PTR [rbp+0x20]
   1400043c1:	48 63 c1             	movsxd rax,ecx
   1400043c4:	48 69 c0 56 55 55 55 	imul   rax,rax,0x55555556
   1400043cb:	48 c1 e8 20          	shr    rax,0x20
   1400043cf:	48 89 c2             	mov    rdx,rax
   1400043d2:	89 c8                	mov    eax,ecx
   1400043d4:	c1 f8 1f             	sar    eax,0x1f
   1400043d7:	29 c2                	sub    edx,eax
   1400043d9:	89 d0                	mov    eax,edx
   1400043db:	01 c0                	add    eax,eax
   1400043dd:	01 d0                	add    eax,edx
   1400043df:	29 c1                	sub    ecx,eax
   1400043e1:	89 ca                	mov    edx,ecx
   1400043e3:	85 d2                	test   edx,edx
   1400043e5:	75 1c                	jne    140004403 <__pformat_emit_float+0x304>
   1400043e7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400043eb:	48 83 c0 20          	add    rax,0x20
   1400043ef:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400043f3:	49 89 d0             	mov    r8,rdx
   1400043f6:	ba 01 00 00 00       	mov    edx,0x1
   1400043fb:	48 89 c1             	mov    rcx,rax
   1400043fe:	e8 26 ef ff ff       	call   140003329 <__pformat_wputchars>
   140004403:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   140004407:	0f 8f 5b ff ff ff    	jg     140004368 <__pformat_emit_float+0x269>
   14000440d:	eb 11                	jmp    140004420 <__pformat_emit_float+0x321>
   14000440f:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004413:	48 89 c2             	mov    rdx,rax
   140004416:	b9 30 00 00 00       	mov    ecx,0x30
   14000441b:	e8 00 ed ff ff       	call   140003120 <__pformat_putc>
   140004420:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004424:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004427:	85 c0                	test   eax,eax
   140004429:	7f 10                	jg     14000443b <__pformat_emit_float+0x33c>
   14000442b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000442f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004432:	25 00 08 00 00       	and    eax,0x800
   140004437:	85 c0                	test   eax,eax
   140004439:	74 0c                	je     140004447 <__pformat_emit_float+0x348>
   14000443b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000443f:	48 89 c1             	mov    rcx,rax
   140004442:	e8 1b fa ff ff       	call   140003e62 <__pformat_emit_radix_point>
   140004447:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   14000444b:	79 5f                	jns    1400044ac <__pformat_emit_float+0x3ad>
   14000444d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004451:	8b 50 10             	mov    edx,DWORD PTR [rax+0x10]
   140004454:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140004457:	01 c2                	add    edx,eax
   140004459:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000445d:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140004460:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004464:	48 89 c2             	mov    rdx,rax
   140004467:	b9 30 00 00 00       	mov    ecx,0x30
   14000446c:	e8 af ec ff ff       	call   140003120 <__pformat_putc>
   140004471:	83 45 20 01          	add    DWORD PTR [rbp+0x20],0x1
   140004475:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   140004479:	78 e5                	js     140004460 <__pformat_emit_float+0x361>
   14000447b:	eb 2f                	jmp    1400044ac <__pformat_emit_float+0x3ad>
   14000447d:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140004481:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140004484:	84 c0                	test   al,al
   140004486:	74 14                	je     14000449c <__pformat_emit_float+0x39d>
   140004488:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000448c:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004490:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140004494:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140004497:	0f be c0             	movsx  eax,al
   14000449a:	eb 05                	jmp    1400044a1 <__pformat_emit_float+0x3a2>
   14000449c:	b8 30 00 00 00       	mov    eax,0x30
   1400044a1:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400044a5:	89 c1                	mov    ecx,eax
   1400044a7:	e8 74 ec ff ff       	call   140003120 <__pformat_putc>
   1400044ac:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400044b0:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400044b3:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400044b6:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400044ba:	89 4a 10             	mov    DWORD PTR [rdx+0x10],ecx
   1400044bd:	85 c0                	test   eax,eax
   1400044bf:	7f bc                	jg     14000447d <__pformat_emit_float+0x37e>
   1400044c1:	90                   	nop
   1400044c2:	90                   	nop
   1400044c3:	48 83 c4 30          	add    rsp,0x30
   1400044c7:	5d                   	pop    rbp
   1400044c8:	c3                   	ret

00000001400044c9 <__pformat_emit_efloat>:
   1400044c9:	55                   	push   rbp
   1400044ca:	48 89 e5             	mov    rbp,rsp
   1400044cd:	48 83 ec 50          	sub    rsp,0x50
   1400044d1:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400044d4:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400044d8:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d
   1400044dc:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   1400044e0:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   1400044e7:	83 6d 20 01          	sub    DWORD PTR [rbp+0x20],0x1
   1400044eb:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   1400044ef:	79 09                	jns    1400044fa <__pformat_emit_efloat+0x31>
   1400044f1:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   1400044f8:	eb 05                	jmp    1400044ff <__pformat_emit_efloat+0x36>
   1400044fa:	b8 00 00 00 00       	mov    eax,0x0
   1400044ff:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140004503:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140004506:	48 98                	cdqe
   140004508:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000450c:	eb 04                	jmp    140004512 <__pformat_emit_efloat+0x49>
   14000450e:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140004512:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140004515:	48 63 d0             	movsxd rdx,eax
   140004518:	48 69 d2 67 66 66 66 	imul   rdx,rdx,0x66666667
   14000451f:	48 c1 ea 20          	shr    rdx,0x20
   140004523:	89 d1                	mov    ecx,edx
   140004525:	c1 f9 02             	sar    ecx,0x2
   140004528:	99                   	cdq
   140004529:	89 c8                	mov    eax,ecx
   14000452b:	29 d0                	sub    eax,edx
   14000452d:	89 45 20             	mov    DWORD PTR [rbp+0x20],eax
   140004530:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   140004534:	75 d8                	jne    14000450e <__pformat_emit_efloat+0x45>
   140004536:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000453a:	8b 40 2c             	mov    eax,DWORD PTR [rax+0x2c]
   14000453d:	83 f8 ff             	cmp    eax,0xffffffff
   140004540:	75 0b                	jne    14000454d <__pformat_emit_efloat+0x84>
   140004542:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004546:	c7 40 2c 02 00 00 00 	mov    DWORD PTR [rax+0x2c],0x2
   14000454d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004551:	8b 40 2c             	mov    eax,DWORD PTR [rax+0x2c]
   140004554:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140004557:	7d 0a                	jge    140004563 <__pformat_emit_efloat+0x9a>
   140004559:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000455d:	8b 40 2c             	mov    eax,DWORD PTR [rax+0x2c]
   140004560:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140004563:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004567:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000456a:	83 45 fc 02          	add    DWORD PTR [rbp-0x4],0x2
   14000456e:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140004571:	7d 15                	jge    140004588 <__pformat_emit_efloat+0xbf>
   140004573:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004577:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000457a:	2b 45 fc             	sub    eax,DWORD PTR [rbp-0x4]
   14000457d:	89 c2                	mov    edx,eax
   14000457f:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004583:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004586:	eb 0b                	jmp    140004593 <__pformat_emit_efloat+0xca>
   140004588:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000458c:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   140004593:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   140004597:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   14000459b:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   14000459e:	49 89 c9             	mov    r9,rcx
   1400045a1:	41 b8 01 00 00 00    	mov    r8d,0x1
   1400045a7:	89 c1                	mov    ecx,eax
   1400045a9:	e8 51 fb ff ff       	call   1400040ff <__pformat_emit_float>
   1400045ae:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045b2:	8b 50 2c             	mov    edx,DWORD PTR [rax+0x2c]
   1400045b5:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045b9:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   1400045bc:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045c0:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400045c3:	0d c0 01 00 00       	or     eax,0x1c0
   1400045c8:	89 c2                	mov    edx,eax
   1400045ca:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045ce:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   1400045d1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045d5:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400045d8:	83 e0 20             	and    eax,0x20
   1400045db:	83 c8 45             	or     eax,0x45
   1400045de:	89 c1                	mov    ecx,eax
   1400045e0:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045e4:	48 89 c2             	mov    rdx,rax
   1400045e7:	e8 34 eb ff ff       	call   140003120 <__pformat_putc>
   1400045ec:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045f0:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400045f3:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   1400045f6:	83 ea 01             	sub    edx,0x1
   1400045f9:	01 c2                	add    edx,eax
   1400045fb:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045ff:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004602:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140004606:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
   14000460a:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   14000460e:	48 89 55 d8          	mov    QWORD PTR [rbp-0x28],rdx
   140004612:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004616:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   14000461a:	48 89 c1             	mov    rcx,rax
   14000461d:	e8 69 ef ff ff       	call   14000358b <__pformat_int>
   140004622:	90                   	nop
   140004623:	48 83 c4 50          	add    rsp,0x50
   140004627:	5d                   	pop    rbp
   140004628:	c3                   	ret

0000000140004629 <__pformat_float>:
   140004629:	55                   	push   rbp
   14000462a:	53                   	push   rbx
   14000462b:	48 83 ec 58          	sub    rsp,0x58
   14000462f:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140004634:	48 89 cb             	mov    rbx,rcx
   140004637:	db 2b                	fld    TBYTE PTR [rbx]
   140004639:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   14000463c:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140004640:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004644:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004647:	85 c0                	test   eax,eax
   140004649:	79 0b                	jns    140004656 <__pformat_float+0x2d>
   14000464b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000464f:	c7 40 10 06 00 00 00 	mov    DWORD PTR [rax+0x10],0x6
   140004656:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000465a:	8b 50 10             	mov    edx,DWORD PTR [rax+0x10]
   14000465d:	db 6d e0             	fld    TBYTE PTR [rbp-0x20]
   140004660:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140004663:	4c 8d 45 f4          	lea    r8,[rbp-0xc]
   140004667:	48 8d 4d f0          	lea    rcx,[rbp-0x10]
   14000466b:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   14000466f:	4d 89 c1             	mov    r9,r8
   140004672:	49 89 c8             	mov    r8,rcx
   140004675:	48 89 c1             	mov    rcx,rax
   140004678:	e8 93 f7 ff ff       	call   140003e10 <__pformat_fcvt>
   14000467d:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140004681:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140004684:	3d 00 80 ff ff       	cmp    eax,0xffff8000
   140004689:	75 17                	jne    1400046a2 <__pformat_float+0x79>
   14000468b:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000468e:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   140004692:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140004696:	49 89 c8             	mov    r8,rcx
   140004699:	89 c1                	mov    ecx,eax
   14000469b:	e8 74 f9 ff ff       	call   140004014 <__pformat_emit_inf_or_nan>
   1400046a0:	eb 43                	jmp    1400046e5 <__pformat_float+0xbc>
   1400046a2:	8b 4d f0             	mov    ecx,DWORD PTR [rbp-0x10]
   1400046a5:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   1400046a8:	4c 8b 45 28          	mov    r8,QWORD PTR [rbp+0x28]
   1400046ac:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400046b0:	4d 89 c1             	mov    r9,r8
   1400046b3:	41 89 c8             	mov    r8d,ecx
   1400046b6:	89 c1                	mov    ecx,eax
   1400046b8:	e8 42 fa ff ff       	call   1400040ff <__pformat_emit_float>
   1400046bd:	eb 11                	jmp    1400046d0 <__pformat_float+0xa7>
   1400046bf:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400046c3:	48 89 c2             	mov    rdx,rax
   1400046c6:	b9 20 00 00 00       	mov    ecx,0x20
   1400046cb:	e8 50 ea ff ff       	call   140003120 <__pformat_putc>
   1400046d0:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400046d4:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400046d7:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400046da:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400046de:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   1400046e1:	85 c0                	test   eax,eax
   1400046e3:	7f da                	jg     1400046bf <__pformat_float+0x96>
   1400046e5:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400046e9:	48 89 c1             	mov    rcx,rax
   1400046ec:	e8 4e 17 00 00       	call   140005e3f <__freedtoa>
   1400046f1:	90                   	nop
   1400046f2:	48 83 c4 58          	add    rsp,0x58
   1400046f6:	5b                   	pop    rbx
   1400046f7:	5d                   	pop    rbp
   1400046f8:	c3                   	ret

00000001400046f9 <__pformat_efloat>:
   1400046f9:	55                   	push   rbp
   1400046fa:	53                   	push   rbx
   1400046fb:	48 83 ec 58          	sub    rsp,0x58
   1400046ff:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140004704:	48 89 cb             	mov    rbx,rcx
   140004707:	db 2b                	fld    TBYTE PTR [rbx]
   140004709:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   14000470c:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140004710:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004714:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004717:	85 c0                	test   eax,eax
   140004719:	79 0b                	jns    140004726 <__pformat_efloat+0x2d>
   14000471b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000471f:	c7 40 10 06 00 00 00 	mov    DWORD PTR [rax+0x10],0x6
   140004726:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000472a:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   14000472d:	8d 50 01             	lea    edx,[rax+0x1]
   140004730:	db 6d e0             	fld    TBYTE PTR [rbp-0x20]
   140004733:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140004736:	4c 8d 45 f4          	lea    r8,[rbp-0xc]
   14000473a:	48 8d 4d f0          	lea    rcx,[rbp-0x10]
   14000473e:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   140004742:	4d 89 c1             	mov    r9,r8
   140004745:	49 89 c8             	mov    r8,rcx
   140004748:	48 89 c1             	mov    rcx,rax
   14000474b:	e8 6e f6 ff ff       	call   140003dbe <__pformat_ecvt>
   140004750:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140004754:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140004757:	3d 00 80 ff ff       	cmp    eax,0xffff8000
   14000475c:	75 17                	jne    140004775 <__pformat_efloat+0x7c>
   14000475e:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140004761:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   140004765:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140004769:	49 89 c8             	mov    r8,rcx
   14000476c:	89 c1                	mov    ecx,eax
   14000476e:	e8 a1 f8 ff ff       	call   140004014 <__pformat_emit_inf_or_nan>
   140004773:	eb 1b                	jmp    140004790 <__pformat_efloat+0x97>
   140004775:	8b 4d f0             	mov    ecx,DWORD PTR [rbp-0x10]
   140004778:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000477b:	4c 8b 45 28          	mov    r8,QWORD PTR [rbp+0x28]
   14000477f:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140004783:	4d 89 c1             	mov    r9,r8
   140004786:	41 89 c8             	mov    r8d,ecx
   140004789:	89 c1                	mov    ecx,eax
   14000478b:	e8 39 fd ff ff       	call   1400044c9 <__pformat_emit_efloat>
   140004790:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004794:	48 89 c1             	mov    rcx,rax
   140004797:	e8 a3 16 00 00       	call   140005e3f <__freedtoa>
   14000479c:	90                   	nop
   14000479d:	48 83 c4 58          	add    rsp,0x58
   1400047a1:	5b                   	pop    rbx
   1400047a2:	5d                   	pop    rbp
   1400047a3:	c3                   	ret

00000001400047a4 <__pformat_gfloat>:
   1400047a4:	55                   	push   rbp
   1400047a5:	53                   	push   rbx
   1400047a6:	48 83 ec 58          	sub    rsp,0x58
   1400047aa:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   1400047af:	48 89 cb             	mov    rbx,rcx
   1400047b2:	db 2b                	fld    TBYTE PTR [rbx]
   1400047b4:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   1400047b7:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   1400047bb:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400047bf:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400047c2:	85 c0                	test   eax,eax
   1400047c4:	79 0d                	jns    1400047d3 <__pformat_gfloat+0x2f>
   1400047c6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400047ca:	c7 40 10 06 00 00 00 	mov    DWORD PTR [rax+0x10],0x6
   1400047d1:	eb 16                	jmp    1400047e9 <__pformat_gfloat+0x45>
   1400047d3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400047d7:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400047da:	85 c0                	test   eax,eax
   1400047dc:	75 0b                	jne    1400047e9 <__pformat_gfloat+0x45>
   1400047de:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400047e2:	c7 40 10 01 00 00 00 	mov    DWORD PTR [rax+0x10],0x1
   1400047e9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400047ed:	8b 50 10             	mov    edx,DWORD PTR [rax+0x10]
   1400047f0:	db 6d e0             	fld    TBYTE PTR [rbp-0x20]
   1400047f3:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   1400047f6:	4c 8d 45 f4          	lea    r8,[rbp-0xc]
   1400047fa:	48 8d 4d f0          	lea    rcx,[rbp-0x10]
   1400047fe:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   140004802:	4d 89 c1             	mov    r9,r8
   140004805:	49 89 c8             	mov    r8,rcx
   140004808:	48 89 c1             	mov    rcx,rax
   14000480b:	e8 ae f5 ff ff       	call   140003dbe <__pformat_ecvt>
   140004810:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140004814:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140004817:	3d 00 80 ff ff       	cmp    eax,0xffff8000
   14000481c:	75 1a                	jne    140004838 <__pformat_gfloat+0x94>
   14000481e:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140004821:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   140004825:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140004829:	49 89 c8             	mov    r8,rcx
   14000482c:	89 c1                	mov    ecx,eax
   14000482e:	e8 e1 f7 ff ff       	call   140004014 <__pformat_emit_inf_or_nan>
   140004833:	e9 14 01 00 00       	jmp    14000494c <__pformat_gfloat+0x1a8>
   140004838:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   14000483b:	83 f8 fd             	cmp    eax,0xfffffffd
   14000483e:	0f 8c b2 00 00 00    	jl     1400048f6 <__pformat_gfloat+0x152>
   140004844:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004848:	8b 50 10             	mov    edx,DWORD PTR [rax+0x10]
   14000484b:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   14000484e:	39 c2                	cmp    edx,eax
   140004850:	0f 8c a0 00 00 00    	jl     1400048f6 <__pformat_gfloat+0x152>
   140004856:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000485a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000485d:	25 00 08 00 00       	and    eax,0x800
   140004862:	85 c0                	test   eax,eax
   140004864:	74 15                	je     14000487b <__pformat_gfloat+0xd7>
   140004866:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000486a:	8b 50 10             	mov    edx,DWORD PTR [rax+0x10]
   14000486d:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140004870:	29 c2                	sub    edx,eax
   140004872:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004876:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140004879:	eb 20                	jmp    14000489b <__pformat_gfloat+0xf7>
   14000487b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000487f:	48 89 c1             	mov    rcx,rax
   140004882:	e8 81 4d 00 00       	call   140009608 <strlen>
   140004887:	89 c1                	mov    ecx,eax
   140004889:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   14000488c:	89 c2                	mov    edx,eax
   14000488e:	89 c8                	mov    eax,ecx
   140004890:	29 d0                	sub    eax,edx
   140004892:	89 c2                	mov    edx,eax
   140004894:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004898:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   14000489b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000489f:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400048a2:	85 c0                	test   eax,eax
   1400048a4:	79 0b                	jns    1400048b1 <__pformat_gfloat+0x10d>
   1400048a6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400048aa:	c7 40 10 00 00 00 00 	mov    DWORD PTR [rax+0x10],0x0
   1400048b1:	8b 4d f0             	mov    ecx,DWORD PTR [rbp-0x10]
   1400048b4:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   1400048b7:	4c 8b 45 28          	mov    r8,QWORD PTR [rbp+0x28]
   1400048bb:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400048bf:	4d 89 c1             	mov    r9,r8
   1400048c2:	41 89 c8             	mov    r8d,ecx
   1400048c5:	89 c1                	mov    ecx,eax
   1400048c7:	e8 33 f8 ff ff       	call   1400040ff <__pformat_emit_float>
   1400048cc:	eb 11                	jmp    1400048df <__pformat_gfloat+0x13b>
   1400048ce:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400048d2:	48 89 c2             	mov    rdx,rax
   1400048d5:	b9 20 00 00 00       	mov    ecx,0x20
   1400048da:	e8 41 e8 ff ff       	call   140003120 <__pformat_putc>
   1400048df:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400048e3:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400048e6:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400048e9:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400048ed:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   1400048f0:	85 c0                	test   eax,eax
   1400048f2:	7f da                	jg     1400048ce <__pformat_gfloat+0x12a>
   1400048f4:	eb 56                	jmp    14000494c <__pformat_gfloat+0x1a8>
   1400048f6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400048fa:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400048fd:	25 00 08 00 00       	and    eax,0x800
   140004902:	85 c0                	test   eax,eax
   140004904:	74 13                	je     140004919 <__pformat_gfloat+0x175>
   140004906:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000490a:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   14000490d:	8d 50 ff             	lea    edx,[rax-0x1]
   140004910:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004914:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140004917:	eb 18                	jmp    140004931 <__pformat_gfloat+0x18d>
   140004919:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000491d:	48 89 c1             	mov    rcx,rax
   140004920:	e8 e3 4c 00 00       	call   140009608 <strlen>
   140004925:	83 e8 01             	sub    eax,0x1
   140004928:	89 c2                	mov    edx,eax
   14000492a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000492e:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140004931:	8b 4d f0             	mov    ecx,DWORD PTR [rbp-0x10]
   140004934:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140004937:	4c 8b 45 28          	mov    r8,QWORD PTR [rbp+0x28]
   14000493b:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   14000493f:	4d 89 c1             	mov    r9,r8
   140004942:	41 89 c8             	mov    r8d,ecx
   140004945:	89 c1                	mov    ecx,eax
   140004947:	e8 7d fb ff ff       	call   1400044c9 <__pformat_emit_efloat>
   14000494c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004950:	48 89 c1             	mov    rcx,rax
   140004953:	e8 e7 14 00 00       	call   140005e3f <__freedtoa>
   140004958:	90                   	nop
   140004959:	48 83 c4 58          	add    rsp,0x58
   14000495d:	5b                   	pop    rbx
   14000495e:	5d                   	pop    rbp
   14000495f:	c3                   	ret

0000000140004960 <__pformat_emit_xfloat>:
   140004960:	55                   	push   rbp
   140004961:	53                   	push   rbx
   140004962:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140004969:	48 8d ac 24 80 00 00 	lea    rbp,[rsp+0x80]
   140004970:	00 
   140004971:	48 89 cb             	mov    rbx,rcx
   140004974:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140004978:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   14000497c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140004980:	66 c7 45 f6 02 00    	mov    WORD PTR [rbp-0xa],0x2
   140004986:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004989:	48 85 c0             	test   rax,rax
   14000498c:	75 09                	jne    140004997 <__pformat_emit_xfloat+0x37>
   14000498e:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   140004992:	66 85 c0             	test   ax,ax
   140004995:	74 0b                	je     1400049a2 <__pformat_emit_xfloat+0x42>
   140004997:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   14000499b:	83 e8 03             	sub    eax,0x3
   14000499e:	66 89 43 08          	mov    WORD PTR [rbx+0x8],ax
   1400049a2:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400049a6:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400049a9:	85 c0                	test   eax,eax
   1400049ab:	0f 88 90 00 00 00    	js     140004a41 <__pformat_emit_xfloat+0xe1>
   1400049b1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400049b5:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400049b8:	83 f8 0e             	cmp    eax,0xe
   1400049bb:	0f 8f 80 00 00 00    	jg     140004a41 <__pformat_emit_xfloat+0xe1>
   1400049c1:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   1400049c4:	48 d1 e8             	shr    rax,1
   1400049c7:	48 89 03             	mov    QWORD PTR [rbx],rax
   1400049ca:	48 8b 13             	mov    rdx,QWORD PTR [rbx]
   1400049cd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400049d1:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400049d4:	b9 0e 00 00 00       	mov    ecx,0xe
   1400049d9:	29 c1                	sub    ecx,eax
   1400049db:	8d 04 8d 00 00 00 00 	lea    eax,[rcx*4+0x0]
   1400049e2:	41 b8 04 00 00 00    	mov    r8d,0x4
   1400049e8:	89 c1                	mov    ecx,eax
   1400049ea:	49 d3 e0             	shl    r8,cl
   1400049ed:	4c 89 c0             	mov    rax,r8
   1400049f0:	48 01 d0             	add    rax,rdx
   1400049f3:	48 89 03             	mov    QWORD PTR [rbx],rax
   1400049f6:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   1400049f9:	48 85 c0             	test   rax,rax
   1400049fc:	78 0b                	js     140004a09 <__pformat_emit_xfloat+0xa9>
   1400049fe:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004a01:	48 01 c0             	add    rax,rax
   140004a04:	48 89 03             	mov    QWORD PTR [rbx],rax
   140004a07:	eb 15                	jmp    140004a1e <__pformat_emit_xfloat+0xbe>
   140004a09:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   140004a0d:	83 c0 04             	add    eax,0x4
   140004a10:	66 89 43 08          	mov    WORD PTR [rbx+0x8],ax
   140004a14:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004a17:	48 c1 e8 03          	shr    rax,0x3
   140004a1b:	48 89 03             	mov    QWORD PTR [rbx],rax
   140004a1e:	48 8b 13             	mov    rdx,QWORD PTR [rbx]
   140004a21:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004a25:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004a28:	b9 0f 00 00 00       	mov    ecx,0xf
   140004a2d:	29 c1                	sub    ecx,eax
   140004a2f:	8d 04 8d 00 00 00 00 	lea    eax,[rcx*4+0x0]
   140004a36:	89 c1                	mov    ecx,eax
   140004a38:	48 d3 ea             	shr    rdx,cl
   140004a3b:	48 89 d0             	mov    rax,rdx
   140004a3e:	48 89 03             	mov    QWORD PTR [rbx],rax
   140004a41:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004a44:	48 85 c0             	test   rax,rax
   140004a47:	75 0f                	jne    140004a58 <__pformat_emit_xfloat+0xf8>
   140004a49:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004a4d:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004a50:	85 c0                	test   eax,eax
   140004a52:	0f 8e f8 00 00 00    	jle    140004b50 <__pformat_emit_xfloat+0x1f0>
   140004a58:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004a5c:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004a5f:	83 f8 0e             	cmp    eax,0xe
   140004a62:	7f 1a                	jg     140004a7e <__pformat_emit_xfloat+0x11e>
   140004a64:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004a68:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004a6b:	85 c0                	test   eax,eax
   140004a6d:	78 0f                	js     140004a7e <__pformat_emit_xfloat+0x11e>
   140004a6f:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004a73:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004a76:	83 c0 01             	add    eax,0x1
   140004a79:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   140004a7c:	eb 07                	jmp    140004a85 <__pformat_emit_xfloat+0x125>
   140004a7e:	c7 45 f0 10 00 00 00 	mov    DWORD PTR [rbp-0x10],0x10
   140004a85:	e9 bc 00 00 00       	jmp    140004b46 <__pformat_emit_xfloat+0x1e6>
   140004a8a:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004a8d:	83 e0 0f             	and    eax,0xf
   140004a90:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140004a93:	83 7d f0 01          	cmp    DWORD PTR [rbp-0x10],0x1
   140004a97:	75 36                	jne    140004acf <__pformat_emit_xfloat+0x16f>
   140004a99:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004a9d:	48 3b 45 f8          	cmp    rax,QWORD PTR [rbp-0x8]
   140004aa1:	72 1b                	jb     140004abe <__pformat_emit_xfloat+0x15e>
   140004aa3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004aa7:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004aaa:	25 00 08 00 00       	and    eax,0x800
   140004aaf:	85 c0                	test   eax,eax
   140004ab1:	75 0b                	jne    140004abe <__pformat_emit_xfloat+0x15e>
   140004ab3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ab7:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004aba:	85 c0                	test   eax,eax
   140004abc:	7e 2d                	jle    140004aeb <__pformat_emit_xfloat+0x18b>
   140004abe:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004ac2:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004ac6:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140004aca:	c6 00 2e             	mov    BYTE PTR [rax],0x2e
   140004acd:	eb 1c                	jmp    140004aeb <__pformat_emit_xfloat+0x18b>
   140004acf:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ad3:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004ad6:	85 c0                	test   eax,eax
   140004ad8:	7e 11                	jle    140004aeb <__pformat_emit_xfloat+0x18b>
   140004ada:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ade:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004ae1:	8d 50 ff             	lea    edx,[rax-0x1]
   140004ae4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ae8:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140004aeb:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140004aef:	75 15                	jne    140004b06 <__pformat_emit_xfloat+0x1a6>
   140004af1:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004af5:	48 3b 45 f8          	cmp    rax,QWORD PTR [rbp-0x8]
   140004af9:	72 0b                	jb     140004b06 <__pformat_emit_xfloat+0x1a6>
   140004afb:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004aff:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004b02:	85 c0                	test   eax,eax
   140004b04:	78 32                	js     140004b38 <__pformat_emit_xfloat+0x1d8>
   140004b06:	83 7d e4 09          	cmp    DWORD PTR [rbp-0x1c],0x9
   140004b0a:	76 16                	jbe    140004b22 <__pformat_emit_xfloat+0x1c2>
   140004b0c:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140004b0f:	8d 50 37             	lea    edx,[rax+0x37]
   140004b12:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004b16:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004b19:	83 e0 20             	and    eax,0x20
   140004b1c:	09 d0                	or     eax,edx
   140004b1e:	89 c1                	mov    ecx,eax
   140004b20:	eb 08                	jmp    140004b2a <__pformat_emit_xfloat+0x1ca>
   140004b22:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140004b25:	83 c0 30             	add    eax,0x30
   140004b28:	89 c1                	mov    ecx,eax
   140004b2a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004b2e:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004b32:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140004b36:	88 08                	mov    BYTE PTR [rax],cl
   140004b38:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004b3b:	48 c1 e8 04          	shr    rax,0x4
   140004b3f:	48 89 03             	mov    QWORD PTR [rbx],rax
   140004b42:	83 6d f0 01          	sub    DWORD PTR [rbp-0x10],0x1
   140004b46:	83 7d f0 00          	cmp    DWORD PTR [rbp-0x10],0x0
   140004b4a:	0f 8f 3a ff ff ff    	jg     140004a8a <__pformat_emit_xfloat+0x12a>
   140004b50:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004b54:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140004b58:	75 39                	jne    140004b93 <__pformat_emit_xfloat+0x233>
   140004b5a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004b5e:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004b61:	85 c0                	test   eax,eax
   140004b63:	7f 10                	jg     140004b75 <__pformat_emit_xfloat+0x215>
   140004b65:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004b69:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004b6c:	25 00 08 00 00       	and    eax,0x800
   140004b71:	85 c0                	test   eax,eax
   140004b73:	74 0f                	je     140004b84 <__pformat_emit_xfloat+0x224>
   140004b75:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004b79:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004b7d:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140004b81:	c6 00 2e             	mov    BYTE PTR [rax],0x2e
   140004b84:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004b88:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004b8c:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140004b90:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140004b93:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004b97:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004b9a:	85 c0                	test   eax,eax
   140004b9c:	0f 8e e3 00 00 00    	jle    140004c85 <__pformat_emit_xfloat+0x325>
   140004ba2:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004ba6:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140004baa:	48 29 c2             	sub    rdx,rax
   140004bad:	89 55 ec             	mov    DWORD PTR [rbp-0x14],edx
   140004bb0:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   140004bb4:	98                   	cwde
   140004bb5:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140004bb8:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004bbc:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004bbf:	85 c0                	test   eax,eax
   140004bc1:	7e 0a                	jle    140004bcd <__pformat_emit_xfloat+0x26d>
   140004bc3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004bc7:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004bca:	01 45 ec             	add    DWORD PTR [rbp-0x14],eax
   140004bcd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004bd1:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004bd4:	25 c0 01 00 00       	and    eax,0x1c0
   140004bd9:	85 c0                	test   eax,eax
   140004bdb:	74 07                	je     140004be4 <__pformat_emit_xfloat+0x284>
   140004bdd:	b8 06 00 00 00       	mov    eax,0x6
   140004be2:	eb 05                	jmp    140004be9 <__pformat_emit_xfloat+0x289>
   140004be4:	b8 05 00 00 00       	mov    eax,0x5
   140004be9:	01 45 ec             	add    DWORD PTR [rbp-0x14],eax
   140004bec:	eb 0f                	jmp    140004bfd <__pformat_emit_xfloat+0x29d>
   140004bee:	83 45 ec 01          	add    DWORD PTR [rbp-0x14],0x1
   140004bf2:	0f b7 45 f6          	movzx  eax,WORD PTR [rbp-0xa]
   140004bf6:	83 c0 01             	add    eax,0x1
   140004bf9:	66 89 45 f6          	mov    WORD PTR [rbp-0xa],ax
   140004bfd:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140004c00:	48 63 d0             	movsxd rdx,eax
   140004c03:	48 69 d2 67 66 66 66 	imul   rdx,rdx,0x66666667
   140004c0a:	48 c1 ea 20          	shr    rdx,0x20
   140004c0e:	89 d1                	mov    ecx,edx
   140004c10:	c1 f9 02             	sar    ecx,0x2
   140004c13:	99                   	cdq
   140004c14:	89 c8                	mov    eax,ecx
   140004c16:	29 d0                	sub    eax,edx
   140004c18:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140004c1b:	83 7d e8 00          	cmp    DWORD PTR [rbp-0x18],0x0
   140004c1f:	75 cd                	jne    140004bee <__pformat_emit_xfloat+0x28e>
   140004c21:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c25:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004c28:	39 45 ec             	cmp    DWORD PTR [rbp-0x14],eax
   140004c2b:	7d 4d                	jge    140004c7a <__pformat_emit_xfloat+0x31a>
   140004c2d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c31:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004c34:	2b 45 ec             	sub    eax,DWORD PTR [rbp-0x14]
   140004c37:	89 c2                	mov    edx,eax
   140004c39:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c3d:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004c40:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c44:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004c47:	25 00 06 00 00       	and    eax,0x600
   140004c4c:	85 c0                	test   eax,eax
   140004c4e:	75 35                	jne    140004c85 <__pformat_emit_xfloat+0x325>
   140004c50:	eb 11                	jmp    140004c63 <__pformat_emit_xfloat+0x303>
   140004c52:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c56:	48 89 c2             	mov    rdx,rax
   140004c59:	b9 20 00 00 00       	mov    ecx,0x20
   140004c5e:	e8 bd e4 ff ff       	call   140003120 <__pformat_putc>
   140004c63:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c67:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004c6a:	8d 48 ff             	lea    ecx,[rax-0x1]
   140004c6d:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004c71:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140004c74:	85 c0                	test   eax,eax
   140004c76:	7f da                	jg     140004c52 <__pformat_emit_xfloat+0x2f2>
   140004c78:	eb 0b                	jmp    140004c85 <__pformat_emit_xfloat+0x325>
   140004c7a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c7e:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   140004c85:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c89:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004c8c:	25 80 00 00 00       	and    eax,0x80
   140004c91:	85 c0                	test   eax,eax
   140004c93:	74 13                	je     140004ca8 <__pformat_emit_xfloat+0x348>
   140004c95:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c99:	48 89 c2             	mov    rdx,rax
   140004c9c:	b9 2d 00 00 00       	mov    ecx,0x2d
   140004ca1:	e8 7a e4 ff ff       	call   140003120 <__pformat_putc>
   140004ca6:	eb 42                	jmp    140004cea <__pformat_emit_xfloat+0x38a>
   140004ca8:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004cac:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004caf:	25 00 01 00 00       	and    eax,0x100
   140004cb4:	85 c0                	test   eax,eax
   140004cb6:	74 13                	je     140004ccb <__pformat_emit_xfloat+0x36b>
   140004cb8:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004cbc:	48 89 c2             	mov    rdx,rax
   140004cbf:	b9 2b 00 00 00       	mov    ecx,0x2b
   140004cc4:	e8 57 e4 ff ff       	call   140003120 <__pformat_putc>
   140004cc9:	eb 1f                	jmp    140004cea <__pformat_emit_xfloat+0x38a>
   140004ccb:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ccf:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004cd2:	83 e0 40             	and    eax,0x40
   140004cd5:	85 c0                	test   eax,eax
   140004cd7:	74 11                	je     140004cea <__pformat_emit_xfloat+0x38a>
   140004cd9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004cdd:	48 89 c2             	mov    rdx,rax
   140004ce0:	b9 20 00 00 00       	mov    ecx,0x20
   140004ce5:	e8 36 e4 ff ff       	call   140003120 <__pformat_putc>
   140004cea:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004cee:	48 89 c2             	mov    rdx,rax
   140004cf1:	b9 30 00 00 00       	mov    ecx,0x30
   140004cf6:	e8 25 e4 ff ff       	call   140003120 <__pformat_putc>
   140004cfb:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004cff:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004d02:	83 e0 20             	and    eax,0x20
   140004d05:	83 c8 58             	or     eax,0x58
   140004d08:	89 c1                	mov    ecx,eax
   140004d0a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d0e:	48 89 c2             	mov    rdx,rax
   140004d11:	e8 0a e4 ff ff       	call   140003120 <__pformat_putc>
   140004d16:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d1a:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004d1d:	85 c0                	test   eax,eax
   140004d1f:	7e 54                	jle    140004d75 <__pformat_emit_xfloat+0x415>
   140004d21:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d25:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004d28:	25 00 02 00 00       	and    eax,0x200
   140004d2d:	85 c0                	test   eax,eax
   140004d2f:	74 44                	je     140004d75 <__pformat_emit_xfloat+0x415>
   140004d31:	eb 11                	jmp    140004d44 <__pformat_emit_xfloat+0x3e4>
   140004d33:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d37:	48 89 c2             	mov    rdx,rax
   140004d3a:	b9 30 00 00 00       	mov    ecx,0x30
   140004d3f:	e8 dc e3 ff ff       	call   140003120 <__pformat_putc>
   140004d44:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d48:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004d4b:	8d 48 ff             	lea    ecx,[rax-0x1]
   140004d4e:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004d52:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140004d55:	85 c0                	test   eax,eax
   140004d57:	7f da                	jg     140004d33 <__pformat_emit_xfloat+0x3d3>
   140004d59:	eb 1a                	jmp    140004d75 <__pformat_emit_xfloat+0x415>
   140004d5b:	48 83 6d f8 01       	sub    QWORD PTR [rbp-0x8],0x1
   140004d60:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004d64:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140004d67:	0f be c0             	movsx  eax,al
   140004d6a:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004d6e:	89 c1                	mov    ecx,eax
   140004d70:	e8 32 f2 ff ff       	call   140003fa7 <__pformat_emit_numeric_value>
   140004d75:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004d79:	48 3b 45 f8          	cmp    rax,QWORD PTR [rbp-0x8]
   140004d7d:	72 dc                	jb     140004d5b <__pformat_emit_xfloat+0x3fb>
   140004d7f:	eb 11                	jmp    140004d92 <__pformat_emit_xfloat+0x432>
   140004d81:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d85:	48 89 c2             	mov    rdx,rax
   140004d88:	b9 30 00 00 00       	mov    ecx,0x30
   140004d8d:	e8 8e e3 ff ff       	call   140003120 <__pformat_putc>
   140004d92:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d96:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004d99:	8d 48 ff             	lea    ecx,[rax-0x1]
   140004d9c:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004da0:	89 4a 10             	mov    DWORD PTR [rdx+0x10],ecx
   140004da3:	85 c0                	test   eax,eax
   140004da5:	7f da                	jg     140004d81 <__pformat_emit_xfloat+0x421>
   140004da7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004dab:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004dae:	83 e0 20             	and    eax,0x20
   140004db1:	83 c8 50             	or     eax,0x50
   140004db4:	89 c1                	mov    ecx,eax
   140004db6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004dba:	48 89 c2             	mov    rdx,rax
   140004dbd:	e8 5e e3 ff ff       	call   140003120 <__pformat_putc>
   140004dc2:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004dc6:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140004dc9:	0f bf 45 f6          	movsx  eax,WORD PTR [rbp-0xa]
   140004dcd:	01 c2                	add    edx,eax
   140004dcf:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004dd3:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004dd6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004dda:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004ddd:	0d c0 01 00 00       	or     eax,0x1c0
   140004de2:	89 c2                	mov    edx,eax
   140004de4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004de8:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140004deb:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   140004def:	66 85 c0             	test   ax,ax
   140004df2:	79 09                	jns    140004dfd <__pformat_emit_xfloat+0x49d>
   140004df4:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   140004dfb:	eb 05                	jmp    140004e02 <__pformat_emit_xfloat+0x4a2>
   140004dfd:	b8 00 00 00 00       	mov    eax,0x0
   140004e02:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140004e06:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   140004e0a:	48 0f bf c0          	movsx  rax,ax
   140004e0e:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140004e12:	48 8b 45 b0          	mov    rax,QWORD PTR [rbp-0x50]
   140004e16:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   140004e1a:	48 89 45 a0          	mov    QWORD PTR [rbp-0x60],rax
   140004e1e:	48 89 55 a8          	mov    QWORD PTR [rbp-0x58],rdx
   140004e22:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004e26:	48 8d 45 a0          	lea    rax,[rbp-0x60]
   140004e2a:	48 89 c1             	mov    rcx,rax
   140004e2d:	e8 59 e7 ff ff       	call   14000358b <__pformat_int>
   140004e32:	90                   	nop
   140004e33:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140004e3a:	5b                   	pop    rbx
   140004e3b:	5d                   	pop    rbp
   140004e3c:	c3                   	ret

0000000140004e3d <__pformat_xldouble>:
   140004e3d:	55                   	push   rbp
   140004e3e:	53                   	push   rbx
   140004e3f:	48 83 ec 78          	sub    rsp,0x78
   140004e43:	48 8d 6c 24 70       	lea    rbp,[rsp+0x70]
   140004e48:	48 89 cb             	mov    rbx,rcx
   140004e4b:	db 2b                	fld    TBYTE PTR [rbx]
   140004e4d:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140004e50:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140004e54:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140004e5b:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140004e5f:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140004e62:	db 7d c0             	fstp   TBYTE PTR [rbp-0x40]
   140004e65:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140004e69:	48 89 c1             	mov    rcx,rax
   140004e6c:	e8 e5 ed ff ff       	call   140003c56 <init_fpreg_ldouble>
   140004e71:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140004e74:	db 7d c0             	fstp   TBYTE PTR [rbp-0x40]
   140004e77:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004e7b:	48 89 c1             	mov    rcx,rax
   140004e7e:	e8 ed 3d 00 00       	call   140008c70 <__isnanl>
   140004e83:	85 c0                	test   eax,eax
   140004e85:	74 1d                	je     140004ea4 <__pformat_xldouble+0x67>
   140004e87:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140004e8a:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   140004e8e:	48 8d 15 b1 64 00 00 	lea    rdx,[rip+0x64b1]        # 14000b346 <.rdata+0x16>
   140004e95:	49 89 c8             	mov    r8,rcx
   140004e98:	89 c1                	mov    ecx,eax
   140004e9a:	e8 75 f1 ff ff       	call   140004014 <__pformat_emit_inf_or_nan>
   140004e9f:	e9 aa 00 00 00       	jmp    140004f4e <__pformat_xldouble+0x111>
   140004ea4:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140004ea8:	98                   	cwde
   140004ea9:	25 00 80 00 00       	and    eax,0x8000
   140004eae:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140004eb1:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140004eb5:	74 12                	je     140004ec9 <__pformat_xldouble+0x8c>
   140004eb7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ebb:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004ebe:	0c 80                	or     al,0x80
   140004ec0:	89 c2                	mov    edx,eax
   140004ec2:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ec6:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140004ec9:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140004ecc:	db 7d c0             	fstp   TBYTE PTR [rbp-0x40]
   140004ecf:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004ed3:	48 89 c1             	mov    rcx,rax
   140004ed6:	e8 a5 3c 00 00       	call   140008b80 <__fpclassifyl>
   140004edb:	3d 00 05 00 00       	cmp    eax,0x500
   140004ee0:	75 1a                	jne    140004efc <__pformat_xldouble+0xbf>
   140004ee2:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140004ee5:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   140004ee9:	48 8d 15 5a 64 00 00 	lea    rdx,[rip+0x645a]        # 14000b34a <.rdata+0x1a>
   140004ef0:	49 89 c8             	mov    r8,rcx
   140004ef3:	89 c1                	mov    ecx,eax
   140004ef5:	e8 1a f1 ff ff       	call   140004014 <__pformat_emit_inf_or_nan>
   140004efa:	eb 52                	jmp    140004f4e <__pformat_xldouble+0x111>
   140004efc:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140004f00:	66 25 ff 7f          	and    ax,0x7fff
   140004f04:	66 89 45 e8          	mov    WORD PTR [rbp-0x18],ax
   140004f08:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140004f0c:	66 85 c0             	test   ax,ax
   140004f0f:	75 11                	jne    140004f22 <__pformat_xldouble+0xe5>
   140004f11:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140004f15:	48 85 c0             	test   rax,rax
   140004f18:	74 14                	je     140004f2e <__pformat_xldouble+0xf1>
   140004f1a:	66 c7 45 e8 02 c0    	mov    WORD PTR [rbp-0x18],0xc002
   140004f20:	eb 0c                	jmp    140004f2e <__pformat_xldouble+0xf1>
   140004f22:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140004f26:	66 2d ff 3f          	sub    ax,0x3fff
   140004f2a:	66 89 45 e8          	mov    WORD PTR [rbp-0x18],ax
   140004f2e:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140004f32:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
   140004f36:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140004f3a:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
   140004f3e:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004f42:	48 8d 45 b0          	lea    rax,[rbp-0x50]
   140004f46:	48 89 c1             	mov    rcx,rax
   140004f49:	e8 12 fa ff ff       	call   140004960 <__pformat_emit_xfloat>
   140004f4e:	90                   	nop
   140004f4f:	48 83 c4 78          	add    rsp,0x78
   140004f53:	5b                   	pop    rbx
   140004f54:	5d                   	pop    rbp
   140004f55:	c3                   	ret

0000000140004f56 <__pformat_xdouble>:
   140004f56:	55                   	push   rbp
   140004f57:	48 89 e5             	mov    rbp,rsp
   140004f5a:	48 83 ec 60          	sub    rsp,0x60
   140004f5e:	f2 0f 11 45 10       	movsd  QWORD PTR [rbp+0x10],xmm0
   140004f63:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140004f67:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140004f6e:	dd 45 10             	fld    QWORD PTR [rbp+0x10]
   140004f71:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140004f75:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140004f78:	48 8d 55 d0          	lea    rdx,[rbp-0x30]
   140004f7c:	48 89 c1             	mov    rcx,rax
   140004f7f:	e8 d2 ec ff ff       	call   140003c56 <init_fpreg_ldouble>
   140004f84:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140004f88:	66 48 0f 6e c0       	movq   xmm0,rax
   140004f8d:	e8 7e 3c 00 00       	call   140008c10 <__isnan>
   140004f92:	85 c0                	test   eax,eax
   140004f94:	74 1d                	je     140004fb3 <__pformat_xdouble+0x5d>
   140004f96:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140004f99:	48 8b 4d 18          	mov    rcx,QWORD PTR [rbp+0x18]
   140004f9d:	48 8d 15 a2 63 00 00 	lea    rdx,[rip+0x63a2]        # 14000b346 <.rdata+0x16>
   140004fa4:	49 89 c8             	mov    r8,rcx
   140004fa7:	89 c1                	mov    ecx,eax
   140004fa9:	e8 66 f0 ff ff       	call   140004014 <__pformat_emit_inf_or_nan>
   140004fae:	e9 f9 00 00 00       	jmp    1400050ac <__pformat_xdouble+0x156>
   140004fb3:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140004fb7:	98                   	cwde
   140004fb8:	25 00 80 00 00       	and    eax,0x8000
   140004fbd:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140004fc0:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140004fc4:	74 12                	je     140004fd8 <__pformat_xdouble+0x82>
   140004fc6:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140004fca:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004fcd:	0c 80                	or     al,0x80
   140004fcf:	89 c2                	mov    edx,eax
   140004fd1:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140004fd5:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140004fd8:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140004fdc:	66 48 0f 6e c0       	movq   xmm0,rax
   140004fe1:	e8 1a 3b 00 00       	call   140008b00 <__fpclassify>
   140004fe6:	3d 00 05 00 00       	cmp    eax,0x500
   140004feb:	75 1d                	jne    14000500a <__pformat_xdouble+0xb4>
   140004fed:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140004ff0:	48 8b 4d 18          	mov    rcx,QWORD PTR [rbp+0x18]
   140004ff4:	48 8d 15 4f 63 00 00 	lea    rdx,[rip+0x634f]        # 14000b34a <.rdata+0x1a>
   140004ffb:	49 89 c8             	mov    r8,rcx
   140004ffe:	89 c1                	mov    ecx,eax
   140005000:	e8 0f f0 ff ff       	call   140004014 <__pformat_emit_inf_or_nan>
   140005005:	e9 a2 00 00 00       	jmp    1400050ac <__pformat_xdouble+0x156>
   14000500a:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   14000500e:	66 25 ff 7f          	and    ax,0x7fff
   140005012:	66 89 45 e8          	mov    WORD PTR [rbp-0x18],ax
   140005016:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   14000501a:	66 85 c0             	test   ax,ax
   14000501d:	74 3b                	je     14000505a <__pformat_xdouble+0x104>
   14000501f:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140005023:	66 3d 00 3c          	cmp    ax,0x3c00
   140005027:	7f 31                	jg     14000505a <__pformat_xdouble+0x104>
   140005029:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   14000502d:	98                   	cwde
   14000502e:	ba 01 3c 00 00       	mov    edx,0x3c01
   140005033:	29 c2                	sub    edx,eax
   140005035:	89 55 f8             	mov    DWORD PTR [rbp-0x8],edx
   140005038:	48 8b 55 e0          	mov    rdx,QWORD PTR [rbp-0x20]
   14000503c:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   14000503f:	89 c1                	mov    ecx,eax
   140005041:	48 d3 ea             	shr    rdx,cl
   140005044:	48 89 d0             	mov    rax,rdx
   140005047:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000504b:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   14000504f:	89 c2                	mov    edx,eax
   140005051:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140005054:	01 d0                	add    eax,edx
   140005056:	66 89 45 e8          	mov    WORD PTR [rbp-0x18],ax
   14000505a:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   14000505e:	66 85 c0             	test   ax,ax
   140005061:	75 11                	jne    140005074 <__pformat_xdouble+0x11e>
   140005063:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140005067:	48 85 c0             	test   rax,rax
   14000506a:	74 14                	je     140005080 <__pformat_xdouble+0x12a>
   14000506c:	66 c7 45 e8 05 fc    	mov    WORD PTR [rbp-0x18],0xfc05
   140005072:	eb 0c                	jmp    140005080 <__pformat_xdouble+0x12a>
   140005074:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140005078:	66 2d fc 3f          	sub    ax,0x3ffc
   14000507c:	66 89 45 e8          	mov    WORD PTR [rbp-0x18],ax
   140005080:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140005084:	48 c1 e8 03          	shr    rax,0x3
   140005088:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000508c:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140005090:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
   140005094:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   140005098:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
   14000509c:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400050a0:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   1400050a4:	48 89 c1             	mov    rcx,rax
   1400050a7:	e8 b4 f8 ff ff       	call   140004960 <__pformat_emit_xfloat>
   1400050ac:	90                   	nop
   1400050ad:	48 83 c4 60          	add    rsp,0x60
   1400050b1:	5d                   	pop    rbp
   1400050b2:	c3                   	ret

00000001400050b3 <__mingw_pformat>:
   1400050b3:	55                   	push   rbp
   1400050b4:	48 89 e5             	mov    rbp,rsp
   1400050b7:	48 81 ec d0 00 00 00 	sub    rsp,0xd0
   1400050be:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400050c1:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400050c5:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d
   1400050c9:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   1400050cd:	e8 a6 44 00 00       	call   140009578 <_errno>
   1400050d2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400050d4:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   1400050d7:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400050db:	48 89 45 a0          	mov    QWORD PTR [rbp-0x60],rax
   1400050df:	81 65 10 00 60 00 00 	and    DWORD PTR [rbp+0x10],0x6000
   1400050e6:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   1400050e9:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   1400050ec:	c7 45 ac ff ff ff ff 	mov    DWORD PTR [rbp-0x54],0xffffffff
   1400050f3:	c7 45 b0 ff ff ff ff 	mov    DWORD PTR [rbp-0x50],0xffffffff
   1400050fa:	c7 45 b4 fd ff ff ff 	mov    DWORD PTR [rbp-0x4c],0xfffffffd
   140005101:	66 c7 45 b8 00 00    	mov    WORD PTR [rbp-0x48],0x0
   140005107:	c7 45 bc 00 00 00 00 	mov    DWORD PTR [rbp-0x44],0x0
   14000510e:	66 c7 45 c0 00 00    	mov    WORD PTR [rbp-0x40],0x0
   140005114:	c7 45 c4 00 00 00 00 	mov    DWORD PTR [rbp-0x3c],0x0
   14000511b:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   14000511e:	89 45 c8             	mov    DWORD PTR [rbp-0x38],eax
   140005121:	c7 45 cc ff ff ff ff 	mov    DWORD PTR [rbp-0x34],0xffffffff
   140005128:	e9 27 0c 00 00       	jmp    140005d54 <__mingw_pformat+0xca1>
   14000512d:	83 7d e8 25          	cmp    DWORD PTR [rbp-0x18],0x25
   140005131:	0f 85 0f 0c 00 00    	jne    140005d46 <__mingw_pformat+0xc93>
   140005137:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000513e:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140005145:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005149:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000514d:	48 8d 45 a0          	lea    rax,[rbp-0x60]
   140005151:	48 83 c0 0c          	add    rax,0xc
   140005155:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005159:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   14000515c:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   14000515f:	c7 45 b0 ff ff ff ff 	mov    DWORD PTR [rbp-0x50],0xffffffff
   140005166:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140005169:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000516c:	e9 c4 0b 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005171:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005175:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140005179:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   14000517d:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005180:	0f be c0             	movsx  eax,al
   140005183:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140005186:	83 7d e8 7a          	cmp    DWORD PTR [rbp-0x18],0x7a
   14000518a:	0f 84 94 09 00 00    	je     140005b24 <__mingw_pformat+0xa71>
   140005190:	83 7d e8 7a          	cmp    DWORD PTR [rbp-0x18],0x7a
   140005194:	0f 8f 02 0b 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000519a:	83 7d e8 78          	cmp    DWORD PTR [rbp-0x18],0x78
   14000519e:	0f 84 eb 03 00 00    	je     14000558f <__mingw_pformat+0x4dc>
   1400051a4:	83 7d e8 78          	cmp    DWORD PTR [rbp-0x18],0x78
   1400051a8:	0f 8f ee 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400051ae:	83 7d e8 77          	cmp    DWORD PTR [rbp-0x18],0x77
   1400051b2:	0f 84 31 09 00 00    	je     140005ae9 <__mingw_pformat+0xa36>
   1400051b8:	83 7d e8 77          	cmp    DWORD PTR [rbp-0x18],0x77
   1400051bc:	0f 8f da 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400051c2:	83 7d e8 75          	cmp    DWORD PTR [rbp-0x18],0x75
   1400051c6:	0f 84 c3 03 00 00    	je     14000558f <__mingw_pformat+0x4dc>
   1400051cc:	83 7d e8 75          	cmp    DWORD PTR [rbp-0x18],0x75
   1400051d0:	0f 8f c6 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400051d6:	83 7d e8 74          	cmp    DWORD PTR [rbp-0x18],0x74
   1400051da:	0f 84 31 09 00 00    	je     140005b11 <__mingw_pformat+0xa5e>
   1400051e0:	83 7d e8 74          	cmp    DWORD PTR [rbp-0x18],0x74
   1400051e4:	0f 8f b2 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400051ea:	83 7d e8 73          	cmp    DWORD PTR [rbp-0x18],0x73
   1400051ee:	0f 84 31 03 00 00    	je     140005525 <__mingw_pformat+0x472>
   1400051f4:	83 7d e8 73          	cmp    DWORD PTR [rbp-0x18],0x73
   1400051f8:	0f 8f 9e 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400051fe:	83 7d e8 70          	cmp    DWORD PTR [rbp-0x18],0x70
   140005202:	0f 84 28 05 00 00    	je     140005730 <__mingw_pformat+0x67d>
   140005208:	83 7d e8 70          	cmp    DWORD PTR [rbp-0x18],0x70
   14000520c:	0f 8f 8a 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005212:	83 7d e8 6f          	cmp    DWORD PTR [rbp-0x18],0x6f
   140005216:	0f 84 73 03 00 00    	je     14000558f <__mingw_pformat+0x4dc>
   14000521c:	83 7d e8 6f          	cmp    DWORD PTR [rbp-0x18],0x6f
   140005220:	0f 8f 76 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005226:	83 7d e8 6e          	cmp    DWORD PTR [rbp-0x18],0x6e
   14000522a:	0f 84 4d 07 00 00    	je     14000597d <__mingw_pformat+0x8ca>
   140005230:	83 7d e8 6e          	cmp    DWORD PTR [rbp-0x18],0x6e
   140005234:	0f 8f 62 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000523a:	83 7d e8 6d          	cmp    DWORD PTR [rbp-0x18],0x6d
   14000523e:	0f 84 2d 03 00 00    	je     140005571 <__mingw_pformat+0x4be>
   140005244:	83 7d e8 6d          	cmp    DWORD PTR [rbp-0x18],0x6d
   140005248:	0f 8f 4e 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000524e:	83 7d e8 6c          	cmp    DWORD PTR [rbp-0x18],0x6c
   140005252:	0f 84 65 08 00 00    	je     140005abd <__mingw_pformat+0xa0a>
   140005258:	83 7d e8 6c          	cmp    DWORD PTR [rbp-0x18],0x6c
   14000525c:	0f 8f 3a 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005262:	83 7d e8 6a          	cmp    DWORD PTR [rbp-0x18],0x6a
   140005266:	0f 84 db 07 00 00    	je     140005a47 <__mingw_pformat+0x994>
   14000526c:	83 7d e8 6a          	cmp    DWORD PTR [rbp-0x18],0x6a
   140005270:	0f 8f 26 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005276:	83 7d e8 69          	cmp    DWORD PTR [rbp-0x18],0x69
   14000527a:	0f 84 ee 03 00 00    	je     14000566e <__mingw_pformat+0x5bb>
   140005280:	83 7d e8 69          	cmp    DWORD PTR [rbp-0x18],0x69
   140005284:	0f 8f 12 0a 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000528a:	83 7d e8 68          	cmp    DWORD PTR [rbp-0x18],0x68
   14000528e:	0f 84 87 07 00 00    	je     140005a1b <__mingw_pformat+0x968>
   140005294:	83 7d e8 68          	cmp    DWORD PTR [rbp-0x18],0x68
   140005298:	0f 8f fe 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000529e:	83 7d e8 67          	cmp    DWORD PTR [rbp-0x18],0x67
   1400052a2:	0f 84 f3 05 00 00    	je     14000589b <__mingw_pformat+0x7e8>
   1400052a8:	83 7d e8 67          	cmp    DWORD PTR [rbp-0x18],0x67
   1400052ac:	0f 8f ea 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400052b2:	83 7d e8 66          	cmp    DWORD PTR [rbp-0x18],0x66
   1400052b6:	0f 84 61 05 00 00    	je     14000581d <__mingw_pformat+0x76a>
   1400052bc:	83 7d e8 66          	cmp    DWORD PTR [rbp-0x18],0x66
   1400052c0:	0f 8f d6 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400052c6:	83 7d e8 65          	cmp    DWORD PTR [rbp-0x18],0x65
   1400052ca:	0f 84 cf 04 00 00    	je     14000579f <__mingw_pformat+0x6ec>
   1400052d0:	83 7d e8 65          	cmp    DWORD PTR [rbp-0x18],0x65
   1400052d4:	0f 8f c2 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400052da:	83 7d e8 64          	cmp    DWORD PTR [rbp-0x18],0x64
   1400052de:	0f 84 8a 03 00 00    	je     14000566e <__mingw_pformat+0x5bb>
   1400052e4:	83 7d e8 64          	cmp    DWORD PTR [rbp-0x18],0x64
   1400052e8:	0f 8f ae 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400052ee:	83 7d e8 63          	cmp    DWORD PTR [rbp-0x18],0x63
   1400052f2:	0f 84 b5 01 00 00    	je     1400054ad <__mingw_pformat+0x3fa>
   1400052f8:	83 7d e8 63          	cmp    DWORD PTR [rbp-0x18],0x63
   1400052fc:	0f 8f 9a 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005302:	83 7d e8 62          	cmp    DWORD PTR [rbp-0x18],0x62
   140005306:	0f 84 83 02 00 00    	je     14000558f <__mingw_pformat+0x4dc>
   14000530c:	83 7d e8 62          	cmp    DWORD PTR [rbp-0x18],0x62
   140005310:	0f 8f 86 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005316:	83 7d e8 61          	cmp    DWORD PTR [rbp-0x18],0x61
   14000531a:	0f 84 f9 05 00 00    	je     140005919 <__mingw_pformat+0x866>
   140005320:	83 7d e8 61          	cmp    DWORD PTR [rbp-0x18],0x61
   140005324:	0f 8f 72 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000532a:	83 7d e8 58          	cmp    DWORD PTR [rbp-0x18],0x58
   14000532e:	0f 84 5b 02 00 00    	je     14000558f <__mingw_pformat+0x4dc>
   140005334:	83 7d e8 58          	cmp    DWORD PTR [rbp-0x18],0x58
   140005338:	0f 8f 5e 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000533e:	83 7d e8 53          	cmp    DWORD PTR [rbp-0x18],0x53
   140005342:	0f 84 d6 01 00 00    	je     14000551e <__mingw_pformat+0x46b>
   140005348:	83 7d e8 53          	cmp    DWORD PTR [rbp-0x18],0x53
   14000534c:	0f 8f 4a 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005352:	83 7d e8 4c          	cmp    DWORD PTR [rbp-0x18],0x4c
   140005356:	0f 84 a0 07 00 00    	je     140005afc <__mingw_pformat+0xa49>
   14000535c:	83 7d e8 4c          	cmp    DWORD PTR [rbp-0x18],0x4c
   140005360:	0f 8f 36 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005366:	83 7d e8 49          	cmp    DWORD PTR [rbp-0x18],0x49
   14000536a:	0f 84 ea 06 00 00    	je     140005a5a <__mingw_pformat+0x9a7>
   140005370:	83 7d e8 49          	cmp    DWORD PTR [rbp-0x18],0x49
   140005374:	0f 8f 22 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000537a:	83 7d e8 47          	cmp    DWORD PTR [rbp-0x18],0x47
   14000537e:	0f 84 20 05 00 00    	je     1400058a4 <__mingw_pformat+0x7f1>
   140005384:	83 7d e8 47          	cmp    DWORD PTR [rbp-0x18],0x47
   140005388:	0f 8f 0e 09 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000538e:	83 7d e8 46          	cmp    DWORD PTR [rbp-0x18],0x46
   140005392:	0f 84 8e 04 00 00    	je     140005826 <__mingw_pformat+0x773>
   140005398:	83 7d e8 46          	cmp    DWORD PTR [rbp-0x18],0x46
   14000539c:	0f 8f fa 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400053a2:	83 7d e8 45          	cmp    DWORD PTR [rbp-0x18],0x45
   1400053a6:	0f 84 fc 03 00 00    	je     1400057a8 <__mingw_pformat+0x6f5>
   1400053ac:	83 7d e8 45          	cmp    DWORD PTR [rbp-0x18],0x45
   1400053b0:	0f 8f e6 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400053b6:	83 7d e8 43          	cmp    DWORD PTR [rbp-0x18],0x43
   1400053ba:	0f 84 e6 00 00 00    	je     1400054a6 <__mingw_pformat+0x3f3>
   1400053c0:	83 7d e8 43          	cmp    DWORD PTR [rbp-0x18],0x43
   1400053c4:	0f 8f d2 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400053ca:	83 7d e8 42          	cmp    DWORD PTR [rbp-0x18],0x42
   1400053ce:	0f 84 bb 01 00 00    	je     14000558f <__mingw_pformat+0x4dc>
   1400053d4:	83 7d e8 42          	cmp    DWORD PTR [rbp-0x18],0x42
   1400053d8:	0f 8f be 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400053de:	83 7d e8 41          	cmp    DWORD PTR [rbp-0x18],0x41
   1400053e2:	0f 84 3a 05 00 00    	je     140005922 <__mingw_pformat+0x86f>
   1400053e8:	83 7d e8 41          	cmp    DWORD PTR [rbp-0x18],0x41
   1400053ec:	0f 8f aa 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   1400053f2:	83 7d e8 30          	cmp    DWORD PTR [rbp-0x18],0x30
   1400053f6:	0f 84 8c 08 00 00    	je     140005c88 <__mingw_pformat+0xbd5>
   1400053fc:	83 7d e8 30          	cmp    DWORD PTR [rbp-0x18],0x30
   140005400:	0f 8f 96 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005406:	83 7d e8 2e          	cmp    DWORD PTR [rbp-0x18],0x2e
   14000540a:	0f 84 27 07 00 00    	je     140005b37 <__mingw_pformat+0xa84>
   140005410:	83 7d e8 2e          	cmp    DWORD PTR [rbp-0x18],0x2e
   140005414:	0f 8f 82 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000541a:	83 7d e8 2d          	cmp    DWORD PTR [rbp-0x18],0x2d
   14000541e:	0f 84 db 07 00 00    	je     140005bff <__mingw_pformat+0xb4c>
   140005424:	83 7d e8 2d          	cmp    DWORD PTR [rbp-0x18],0x2d
   140005428:	0f 8f 6e 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000542e:	83 7d e8 2b          	cmp    DWORD PTR [rbp-0x18],0x2b
   140005432:	0f 84 af 07 00 00    	je     140005be7 <__mingw_pformat+0xb34>
   140005438:	83 7d e8 2b          	cmp    DWORD PTR [rbp-0x18],0x2b
   14000543c:	0f 8f 5a 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005442:	83 7d e8 2a          	cmp    DWORD PTR [rbp-0x18],0x2a
   140005446:	0f 84 1c 07 00 00    	je     140005b68 <__mingw_pformat+0xab5>
   14000544c:	83 7d e8 2a          	cmp    DWORD PTR [rbp-0x18],0x2a
   140005450:	0f 8f 46 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   140005456:	83 7d e8 27          	cmp    DWORD PTR [rbp-0x18],0x27
   14000545a:	0f 84 b7 07 00 00    	je     140005c17 <__mingw_pformat+0xb64>
   140005460:	83 7d e8 27          	cmp    DWORD PTR [rbp-0x18],0x27
   140005464:	0f 8f 32 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000546a:	83 7d e8 25          	cmp    DWORD PTR [rbp-0x18],0x25
   14000546e:	74 23                	je     140005493 <__mingw_pformat+0x3e0>
   140005470:	83 7d e8 25          	cmp    DWORD PTR [rbp-0x18],0x25
   140005474:	0f 8f 22 08 00 00    	jg     140005c9c <__mingw_pformat+0xbe9>
   14000547a:	83 7d e8 20          	cmp    DWORD PTR [rbp-0x18],0x20
   14000547e:	0f 84 ec 07 00 00    	je     140005c70 <__mingw_pformat+0xbbd>
   140005484:	83 7d e8 23          	cmp    DWORD PTR [rbp-0x18],0x23
   140005488:	0f 84 41 07 00 00    	je     140005bcf <__mingw_pformat+0xb1c>
   14000548e:	e9 09 08 00 00       	jmp    140005c9c <__mingw_pformat+0xbe9>
   140005493:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005497:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   14000549a:	89 c1                	mov    ecx,eax
   14000549c:	e8 7f dc ff ff       	call   140003120 <__pformat_putc>
   1400054a1:	e9 82 fc ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   1400054a6:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   1400054ad:	c7 45 b0 ff ff ff ff 	mov    DWORD PTR [rbp-0x50],0xffffffff
   1400054b4:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   1400054b8:	74 06                	je     1400054c0 <__mingw_pformat+0x40d>
   1400054ba:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
   1400054be:	75 30                	jne    1400054f0 <__mingw_pformat+0x43d>
   1400054c0:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400054c4:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400054c8:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400054cc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400054ce:	66 89 45 8e          	mov    WORD PTR [rbp-0x72],ax
   1400054d2:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   1400054d6:	48 8d 45 8e          	lea    rax,[rbp-0x72]
   1400054da:	49 89 d0             	mov    r8,rdx
   1400054dd:	ba 01 00 00 00       	mov    edx,0x1
   1400054e2:	48 89 c1             	mov    rcx,rax
   1400054e5:	e8 3f de ff ff       	call   140003329 <__pformat_wputchars>
   1400054ea:	90                   	nop
   1400054eb:	e9 38 fc ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   1400054f0:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400054f4:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400054f8:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400054fc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400054fe:	88 45 90             	mov    BYTE PTR [rbp-0x70],al
   140005501:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005505:	48 8d 45 90          	lea    rax,[rbp-0x70]
   140005509:	49 89 d0             	mov    r8,rdx
   14000550c:	ba 01 00 00 00       	mov    edx,0x1
   140005511:	48 89 c1             	mov    rcx,rax
   140005514:	e8 8b dc ff ff       	call   1400031a4 <__pformat_putchars>
   140005519:	e9 0a fc ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000551e:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140005525:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   140005529:	74 06                	je     140005531 <__mingw_pformat+0x47e>
   14000552b:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
   14000552f:	75 20                	jne    140005551 <__mingw_pformat+0x49e>
   140005531:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005535:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005539:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000553d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140005540:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005544:	48 89 c1             	mov    rcx,rax
   140005547:	e8 29 df ff ff       	call   140003475 <__pformat_wcputs>
   14000554c:	e9 d7 fb ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   140005551:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005555:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005559:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000555d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140005560:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005564:	48 89 c1             	mov    rcx,rax
   140005567:	e8 37 dd ff ff       	call   1400032a3 <__pformat_puts>
   14000556c:	e9 b7 fb ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   140005571:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
   140005574:	89 c1                	mov    ecx,eax
   140005576:	e8 85 40 00 00       	call   140009600 <strerror>
   14000557b:	48 89 c1             	mov    rcx,rax
   14000557e:	48 8d 45 a0          	lea    rax,[rbp-0x60]
   140005582:	48 89 c2             	mov    rdx,rax
   140005585:	e8 19 dd ff ff       	call   1400032a3 <__pformat_puts>
   14000558a:	e9 99 fb ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000558f:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005592:	80 e4 fe             	and    ah,0xfe
   140005595:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005598:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
   14000559c:	75 15                	jne    1400055b3 <__mingw_pformat+0x500>
   14000559e:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400055a2:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400055a6:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400055aa:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400055ad:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400055b1:	eb 54                	jmp    140005607 <__mingw_pformat+0x554>
   1400055b3:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   1400055b7:	75 16                	jne    1400055cf <__mingw_pformat+0x51c>
   1400055b9:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400055bd:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400055c1:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400055c5:	8b 00                	mov    eax,DWORD PTR [rax]
   1400055c7:	89 c0                	mov    eax,eax
   1400055c9:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400055cd:	eb 38                	jmp    140005607 <__mingw_pformat+0x554>
   1400055cf:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400055d3:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400055d7:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400055db:	8b 00                	mov    eax,DWORD PTR [rax]
   1400055dd:	89 c0                	mov    eax,eax
   1400055df:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400055e3:	83 7d f8 01          	cmp    DWORD PTR [rbp-0x8],0x1
   1400055e7:	75 0d                	jne    1400055f6 <__mingw_pformat+0x543>
   1400055e9:	0f b7 45 90          	movzx  eax,WORD PTR [rbp-0x70]
   1400055ed:	0f b7 c0             	movzx  eax,ax
   1400055f0:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400055f4:	eb 11                	jmp    140005607 <__mingw_pformat+0x554>
   1400055f6:	83 7d f8 05          	cmp    DWORD PTR [rbp-0x8],0x5
   1400055fa:	75 0b                	jne    140005607 <__mingw_pformat+0x554>
   1400055fc:	0f b6 45 90          	movzx  eax,BYTE PTR [rbp-0x70]
   140005600:	0f b6 c0             	movzx  eax,al
   140005603:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   140005607:	83 7d e8 75          	cmp    DWORD PTR [rbp-0x18],0x75
   14000560b:	75 2e                	jne    14000563b <__mingw_pformat+0x588>
   14000560d:	48 8b 45 90          	mov    rax,QWORD PTR [rbp-0x70]
   140005611:	48 8b 55 98          	mov    rdx,QWORD PTR [rbp-0x68]
   140005615:	48 89 85 70 ff ff ff 	mov    QWORD PTR [rbp-0x90],rax
   14000561c:	48 89 95 78 ff ff ff 	mov    QWORD PTR [rbp-0x88],rdx
   140005623:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005627:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
   14000562e:	48 89 c1             	mov    rcx,rax
   140005631:	e8 55 df ff ff       	call   14000358b <__pformat_int>
   140005636:	e9 ed fa ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000563b:	48 8b 45 90          	mov    rax,QWORD PTR [rbp-0x70]
   14000563f:	48 8b 55 98          	mov    rdx,QWORD PTR [rbp-0x68]
   140005643:	48 89 85 70 ff ff ff 	mov    QWORD PTR [rbp-0x90],rax
   14000564a:	48 89 95 78 ff ff ff 	mov    QWORD PTR [rbp-0x88],rdx
   140005651:	48 8d 4d a0          	lea    rcx,[rbp-0x60]
   140005655:	48 8d 95 70 ff ff ff 	lea    rdx,[rbp-0x90]
   14000565c:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   14000565f:	49 89 c8             	mov    r8,rcx
   140005662:	89 c1                	mov    ecx,eax
   140005664:	e8 a5 e2 ff ff       	call   14000390e <__pformat_xint>
   140005669:	e9 ba fa ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000566e:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005671:	0c 80                	or     al,0x80
   140005673:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005676:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
   14000567a:	75 15                	jne    140005691 <__mingw_pformat+0x5de>
   14000567c:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005680:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005684:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005688:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000568b:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   14000568f:	eb 56                	jmp    1400056e7 <__mingw_pformat+0x634>
   140005691:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   140005695:	75 16                	jne    1400056ad <__mingw_pformat+0x5fa>
   140005697:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   14000569b:	48 8d 50 08          	lea    rdx,[rax+0x8]
   14000569f:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400056a3:	8b 00                	mov    eax,DWORD PTR [rax]
   1400056a5:	48 98                	cdqe
   1400056a7:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400056ab:	eb 3a                	jmp    1400056e7 <__mingw_pformat+0x634>
   1400056ad:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400056b1:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400056b5:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400056b9:	8b 00                	mov    eax,DWORD PTR [rax]
   1400056bb:	48 98                	cdqe
   1400056bd:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400056c1:	83 7d f8 01          	cmp    DWORD PTR [rbp-0x8],0x1
   1400056c5:	75 0e                	jne    1400056d5 <__mingw_pformat+0x622>
   1400056c7:	0f b7 45 90          	movzx  eax,WORD PTR [rbp-0x70]
   1400056cb:	48 0f bf c0          	movsx  rax,ax
   1400056cf:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400056d3:	eb 12                	jmp    1400056e7 <__mingw_pformat+0x634>
   1400056d5:	83 7d f8 05          	cmp    DWORD PTR [rbp-0x8],0x5
   1400056d9:	75 0c                	jne    1400056e7 <__mingw_pformat+0x634>
   1400056db:	0f b6 45 90          	movzx  eax,BYTE PTR [rbp-0x70]
   1400056df:	48 0f be c0          	movsx  rax,al
   1400056e3:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400056e7:	48 8b 45 90          	mov    rax,QWORD PTR [rbp-0x70]
   1400056eb:	48 85 c0             	test   rax,rax
   1400056ee:	79 09                	jns    1400056f9 <__mingw_pformat+0x646>
   1400056f0:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   1400056f7:	eb 05                	jmp    1400056fe <__mingw_pformat+0x64b>
   1400056f9:	b8 00 00 00 00       	mov    eax,0x0
   1400056fe:	48 89 45 98          	mov    QWORD PTR [rbp-0x68],rax
   140005702:	48 8b 45 90          	mov    rax,QWORD PTR [rbp-0x70]
   140005706:	48 8b 55 98          	mov    rdx,QWORD PTR [rbp-0x68]
   14000570a:	48 89 85 70 ff ff ff 	mov    QWORD PTR [rbp-0x90],rax
   140005711:	48 89 95 78 ff ff ff 	mov    QWORD PTR [rbp-0x88],rdx
   140005718:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   14000571c:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
   140005723:	48 89 c1             	mov    rcx,rax
   140005726:	e8 60 de ff ff       	call   14000358b <__pformat_int>
   14000572b:	e9 f8 f9 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   140005730:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005734:	75 18                	jne    14000574e <__mingw_pformat+0x69b>
   140005736:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005739:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   14000573c:	75 10                	jne    14000574e <__mingw_pformat+0x69b>
   14000573e:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005741:	80 cc 02             	or     ah,0x2
   140005744:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005747:	c7 45 b0 10 00 00 00 	mov    DWORD PTR [rbp-0x50],0x10
   14000574e:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005752:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005756:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000575a:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000575d:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   140005761:	48 c7 45 98 00 00 00 	mov    QWORD PTR [rbp-0x68],0x0
   140005768:	00 
   140005769:	48 8b 45 90          	mov    rax,QWORD PTR [rbp-0x70]
   14000576d:	48 8b 55 98          	mov    rdx,QWORD PTR [rbp-0x68]
   140005771:	48 89 85 70 ff ff ff 	mov    QWORD PTR [rbp-0x90],rax
   140005778:	48 89 95 78 ff ff ff 	mov    QWORD PTR [rbp-0x88],rdx
   14000577f:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005783:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
   14000578a:	49 89 d0             	mov    r8,rdx
   14000578d:	48 89 c2             	mov    rdx,rax
   140005790:	b9 78 00 00 00       	mov    ecx,0x78
   140005795:	e8 74 e1 ff ff       	call   14000390e <__pformat_xint>
   14000579a:	e9 89 f9 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000579f:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   1400057a2:	83 c8 20             	or     eax,0x20
   1400057a5:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   1400057a8:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   1400057ab:	83 e0 04             	and    eax,0x4
   1400057ae:	85 c0                	test   eax,eax
   1400057b0:	74 2f                	je     1400057e1 <__mingw_pformat+0x72e>
   1400057b2:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400057b6:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400057ba:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400057be:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400057c1:	db 28                	fld    TBYTE PTR [rax]
   1400057c3:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   1400057c9:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   1400057cd:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   1400057d4:	48 89 c1             	mov    rcx,rax
   1400057d7:	e8 1d ef ff ff       	call   1400046f9 <__pformat_efloat>
   1400057dc:	e9 47 f9 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   1400057e1:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400057e5:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400057e9:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400057ed:	f2 0f 10 08          	movsd  xmm1,QWORD PTR [rax]
   1400057f1:	f2 0f 11 8d 58 ff ff 	movsd  QWORD PTR [rbp-0xa8],xmm1
   1400057f8:	ff 
   1400057f9:	dd 85 58 ff ff ff    	fld    QWORD PTR [rbp-0xa8]
   1400057ff:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   140005805:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005809:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   140005810:	48 89 c1             	mov    rcx,rax
   140005813:	e8 e1 ee ff ff       	call   1400046f9 <__pformat_efloat>
   140005818:	e9 0b f9 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000581d:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005820:	83 c8 20             	or     eax,0x20
   140005823:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005826:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005829:	83 e0 04             	and    eax,0x4
   14000582c:	85 c0                	test   eax,eax
   14000582e:	74 2f                	je     14000585f <__mingw_pformat+0x7ac>
   140005830:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005834:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005838:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000583c:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000583f:	db 28                	fld    TBYTE PTR [rax]
   140005841:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   140005847:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   14000584b:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   140005852:	48 89 c1             	mov    rcx,rax
   140005855:	e8 cf ed ff ff       	call   140004629 <__pformat_float>
   14000585a:	e9 c9 f8 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000585f:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005863:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005867:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000586b:	f2 0f 10 10          	movsd  xmm2,QWORD PTR [rax]
   14000586f:	f2 0f 11 95 58 ff ff 	movsd  QWORD PTR [rbp-0xa8],xmm2
   140005876:	ff 
   140005877:	dd 85 58 ff ff ff    	fld    QWORD PTR [rbp-0xa8]
   14000587d:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   140005883:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005887:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   14000588e:	48 89 c1             	mov    rcx,rax
   140005891:	e8 93 ed ff ff       	call   140004629 <__pformat_float>
   140005896:	e9 8d f8 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000589b:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   14000589e:	83 c8 20             	or     eax,0x20
   1400058a1:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   1400058a4:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   1400058a7:	83 e0 04             	and    eax,0x4
   1400058aa:	85 c0                	test   eax,eax
   1400058ac:	74 2f                	je     1400058dd <__mingw_pformat+0x82a>
   1400058ae:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400058b2:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400058b6:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400058ba:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400058bd:	db 28                	fld    TBYTE PTR [rax]
   1400058bf:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   1400058c5:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   1400058c9:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   1400058d0:	48 89 c1             	mov    rcx,rax
   1400058d3:	e8 cc ee ff ff       	call   1400047a4 <__pformat_gfloat>
   1400058d8:	e9 4b f8 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   1400058dd:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400058e1:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400058e5:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400058e9:	f2 0f 10 18          	movsd  xmm3,QWORD PTR [rax]
   1400058ed:	f2 0f 11 9d 58 ff ff 	movsd  QWORD PTR [rbp-0xa8],xmm3
   1400058f4:	ff 
   1400058f5:	dd 85 58 ff ff ff    	fld    QWORD PTR [rbp-0xa8]
   1400058fb:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   140005901:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005905:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   14000590c:	48 89 c1             	mov    rcx,rax
   14000590f:	e8 90 ee ff ff       	call   1400047a4 <__pformat_gfloat>
   140005914:	e9 0f f8 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   140005919:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   14000591c:	83 c8 20             	or     eax,0x20
   14000591f:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005922:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005925:	83 e0 04             	and    eax,0x4
   140005928:	85 c0                	test   eax,eax
   14000592a:	74 2f                	je     14000595b <__mingw_pformat+0x8a8>
   14000592c:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005930:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005934:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005938:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000593b:	db 28                	fld    TBYTE PTR [rax]
   14000593d:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   140005943:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005947:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   14000594e:	48 89 c1             	mov    rcx,rax
   140005951:	e8 e7 f4 ff ff       	call   140004e3d <__pformat_xldouble>
   140005956:	e9 cd f7 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000595b:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   14000595f:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005963:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005967:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000596a:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   14000596e:	66 48 0f 6e c0       	movq   xmm0,rax
   140005973:	e8 de f5 ff ff       	call   140004f56 <__pformat_xdouble>
   140005978:	e9 ab f7 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000597d:	83 7d f8 05          	cmp    DWORD PTR [rbp-0x8],0x5
   140005981:	75 1b                	jne    14000599e <__mingw_pformat+0x8eb>
   140005983:	8b 4d c4             	mov    ecx,DWORD PTR [rbp-0x3c]
   140005986:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   14000598a:	48 8d 50 08          	lea    rdx,[rax+0x8]
   14000598e:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005992:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140005995:	89 ca                	mov    edx,ecx
   140005997:	88 10                	mov    BYTE PTR [rax],dl
   140005999:	e9 8a f7 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   14000599e:	83 7d f8 01          	cmp    DWORD PTR [rbp-0x8],0x1
   1400059a2:	75 1c                	jne    1400059c0 <__mingw_pformat+0x90d>
   1400059a4:	8b 4d c4             	mov    ecx,DWORD PTR [rbp-0x3c]
   1400059a7:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400059ab:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400059af:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400059b3:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400059b6:	89 ca                	mov    edx,ecx
   1400059b8:	66 89 10             	mov    WORD PTR [rax],dx
   1400059bb:	e9 68 f7 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   1400059c0:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   1400059c4:	75 19                	jne    1400059df <__mingw_pformat+0x92c>
   1400059c6:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400059ca:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400059ce:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400059d2:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400059d5:	8b 55 c4             	mov    edx,DWORD PTR [rbp-0x3c]
   1400059d8:	89 10                	mov    DWORD PTR [rax],edx
   1400059da:	e9 49 f7 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   1400059df:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
   1400059e3:	75 1d                	jne    140005a02 <__mingw_pformat+0x94f>
   1400059e5:	8b 4d c4             	mov    ecx,DWORD PTR [rbp-0x3c]
   1400059e8:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400059ec:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400059f0:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400059f4:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400059f7:	48 63 d1             	movsxd rdx,ecx
   1400059fa:	48 89 10             	mov    QWORD PTR [rax],rdx
   1400059fd:	e9 26 f7 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   140005a02:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005a06:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005a0a:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005a0e:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140005a11:	8b 55 c4             	mov    edx,DWORD PTR [rbp-0x3c]
   140005a14:	89 10                	mov    DWORD PTR [rax],edx
   140005a16:	e9 0d f7 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   140005a1b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005a1f:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005a22:	3c 68                	cmp    al,0x68
   140005a24:	75 0e                	jne    140005a34 <__mingw_pformat+0x981>
   140005a26:	48 83 45 28 01       	add    QWORD PTR [rbp+0x28],0x1
   140005a2b:	c7 45 f8 05 00 00 00 	mov    DWORD PTR [rbp-0x8],0x5
   140005a32:	eb 07                	jmp    140005a3b <__mingw_pformat+0x988>
   140005a34:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140005a3b:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005a42:	e9 ee 02 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005a47:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005a4e:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005a55:	e9 db 02 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005a5a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005a5e:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005a61:	3c 36                	cmp    al,0x36
   140005a63:	75 1d                	jne    140005a82 <__mingw_pformat+0x9cf>
   140005a65:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005a69:	48 83 c0 01          	add    rax,0x1
   140005a6d:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005a70:	3c 34                	cmp    al,0x34
   140005a72:	75 0e                	jne    140005a82 <__mingw_pformat+0x9cf>
   140005a74:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005a7b:	48 83 45 28 02       	add    QWORD PTR [rbp+0x28],0x2
   140005a80:	eb 2f                	jmp    140005ab1 <__mingw_pformat+0x9fe>
   140005a82:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005a86:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005a89:	3c 33                	cmp    al,0x33
   140005a8b:	75 1d                	jne    140005aaa <__mingw_pformat+0x9f7>
   140005a8d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005a91:	48 83 c0 01          	add    rax,0x1
   140005a95:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005a98:	3c 32                	cmp    al,0x32
   140005a9a:	75 0e                	jne    140005aaa <__mingw_pformat+0x9f7>
   140005a9c:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140005aa3:	48 83 45 28 02       	add    QWORD PTR [rbp+0x28],0x2
   140005aa8:	eb 07                	jmp    140005ab1 <__mingw_pformat+0x9fe>
   140005aaa:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005ab1:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005ab8:	e9 78 02 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005abd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005ac1:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005ac4:	3c 6c                	cmp    al,0x6c
   140005ac6:	75 0e                	jne    140005ad6 <__mingw_pformat+0xa23>
   140005ac8:	48 83 45 28 01       	add    QWORD PTR [rbp+0x28],0x1
   140005acd:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005ad4:	eb 07                	jmp    140005add <__mingw_pformat+0xa2a>
   140005ad6:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140005add:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005ae4:	e9 4c 02 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005ae9:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140005af0:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005af7:	e9 39 02 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005afc:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005aff:	83 c8 04             	or     eax,0x4
   140005b02:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005b05:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005b0c:	e9 24 02 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005b11:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005b18:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005b1f:	e9 11 02 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005b24:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005b2b:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005b32:	e9 fe 01 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005b37:	83 7d fc 01          	cmp    DWORD PTR [rbp-0x4],0x1
   140005b3b:	77 1f                	ja     140005b5c <__mingw_pformat+0xaa9>
   140005b3d:	c7 45 b0 00 00 00 00 	mov    DWORD PTR [rbp-0x50],0x0
   140005b44:	48 8d 45 a0          	lea    rax,[rbp-0x60]
   140005b48:	48 83 c0 10          	add    rax,0x10
   140005b4c:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005b50:	c7 45 fc 02 00 00 00 	mov    DWORD PTR [rbp-0x4],0x2
   140005b57:	e9 d9 01 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005b5c:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005b63:	e9 cd 01 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005b68:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140005b6d:	74 4c                	je     140005bbb <__mingw_pformat+0xb08>
   140005b6f:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005b73:	74 06                	je     140005b7b <__mingw_pformat+0xac8>
   140005b75:	83 7d fc 02          	cmp    DWORD PTR [rbp-0x4],0x2
   140005b79:	75 40                	jne    140005bbb <__mingw_pformat+0xb08>
   140005b7b:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005b7f:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005b83:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005b87:	8b 10                	mov    edx,DWORD PTR [rax]
   140005b89:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005b8d:	89 10                	mov    DWORD PTR [rax],edx
   140005b8f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005b93:	8b 00                	mov    eax,DWORD PTR [rax]
   140005b95:	85 c0                	test   eax,eax
   140005b97:	79 29                	jns    140005bc2 <__mingw_pformat+0xb0f>
   140005b99:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005b9d:	75 13                	jne    140005bb2 <__mingw_pformat+0xaff>
   140005b9f:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005ba2:	80 cc 04             	or     ah,0x4
   140005ba5:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005ba8:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
   140005bab:	f7 d8                	neg    eax
   140005bad:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   140005bb0:	eb 10                	jmp    140005bc2 <__mingw_pformat+0xb0f>
   140005bb2:	c7 45 b0 ff ff ff ff 	mov    DWORD PTR [rbp-0x50],0xffffffff
   140005bb9:	eb 07                	jmp    140005bc2 <__mingw_pformat+0xb0f>
   140005bbb:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005bc2:	48 c7 45 f0 00 00 00 	mov    QWORD PTR [rbp-0x10],0x0
   140005bc9:	00 
   140005bca:	e9 66 01 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005bcf:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005bd3:	0f 85 4f 01 00 00    	jne    140005d28 <__mingw_pformat+0xc75>
   140005bd9:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005bdc:	80 cc 08             	or     ah,0x8
   140005bdf:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005be2:	e9 41 01 00 00       	jmp    140005d28 <__mingw_pformat+0xc75>
   140005be7:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005beb:	0f 85 3a 01 00 00    	jne    140005d2b <__mingw_pformat+0xc78>
   140005bf1:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005bf4:	80 cc 01             	or     ah,0x1
   140005bf7:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005bfa:	e9 2c 01 00 00       	jmp    140005d2b <__mingw_pformat+0xc78>
   140005bff:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005c03:	0f 85 25 01 00 00    	jne    140005d2e <__mingw_pformat+0xc7b>
   140005c09:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005c0c:	80 cc 04             	or     ah,0x4
   140005c0f:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005c12:	e9 17 01 00 00       	jmp    140005d2e <__mingw_pformat+0xc7b>
   140005c17:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005c1b:	0f 85 10 01 00 00    	jne    140005d31 <__mingw_pformat+0xc7e>
   140005c21:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005c24:	80 cc 10             	or     ah,0x10
   140005c27:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005c2a:	48 c7 45 84 00 00 00 	mov    QWORD PTR [rbp-0x7c],0x0
   140005c31:	00 
   140005c32:	e8 a1 39 00 00       	call   1400095d8 <localeconv>
   140005c37:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140005c3b:	48 8d 4d 84          	lea    rcx,[rbp-0x7c]
   140005c3f:	48 8d 45 8c          	lea    rax,[rbp-0x74]
   140005c43:	49 89 c9             	mov    r9,rcx
   140005c46:	41 b8 10 00 00 00    	mov    r8d,0x10
   140005c4c:	48 89 c1             	mov    rcx,rax
   140005c4f:	e8 bc 33 00 00       	call   140009010 <mbrtowc>
   140005c54:	89 45 dc             	mov    DWORD PTR [rbp-0x24],eax
   140005c57:	83 7d dc 00          	cmp    DWORD PTR [rbp-0x24],0x0
   140005c5b:	7e 08                	jle    140005c65 <__mingw_pformat+0xbb2>
   140005c5d:	0f b7 45 8c          	movzx  eax,WORD PTR [rbp-0x74]
   140005c61:	66 89 45 c0          	mov    WORD PTR [rbp-0x40],ax
   140005c65:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   140005c68:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
   140005c6b:	e9 c1 00 00 00       	jmp    140005d31 <__mingw_pformat+0xc7e>
   140005c70:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005c74:	0f 85 ba 00 00 00    	jne    140005d34 <__mingw_pformat+0xc81>
   140005c7a:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005c7d:	83 c8 40             	or     eax,0x40
   140005c80:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005c83:	e9 ac 00 00 00       	jmp    140005d34 <__mingw_pformat+0xc81>
   140005c88:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005c8c:	75 0e                	jne    140005c9c <__mingw_pformat+0xbe9>
   140005c8e:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005c91:	80 cc 02             	or     ah,0x2
   140005c94:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005c97:	e9 99 00 00 00       	jmp    140005d35 <__mingw_pformat+0xc82>
   140005c9c:	83 7d fc 03          	cmp    DWORD PTR [rbp-0x4],0x3
   140005ca0:	77 68                	ja     140005d0a <__mingw_pformat+0xc57>
   140005ca2:	83 7d e8 39          	cmp    DWORD PTR [rbp-0x18],0x39
   140005ca6:	7f 62                	jg     140005d0a <__mingw_pformat+0xc57>
   140005ca8:	83 7d e8 2f          	cmp    DWORD PTR [rbp-0x18],0x2f
   140005cac:	7e 5c                	jle    140005d0a <__mingw_pformat+0xc57>
   140005cae:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005cb2:	75 09                	jne    140005cbd <__mingw_pformat+0xc0a>
   140005cb4:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   140005cbb:	eb 0d                	jmp    140005cca <__mingw_pformat+0xc17>
   140005cbd:	83 7d fc 02          	cmp    DWORD PTR [rbp-0x4],0x2
   140005cc1:	75 07                	jne    140005cca <__mingw_pformat+0xc17>
   140005cc3:	c7 45 fc 03 00 00 00 	mov    DWORD PTR [rbp-0x4],0x3
   140005cca:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140005ccf:	74 64                	je     140005d35 <__mingw_pformat+0xc82>
   140005cd1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005cd5:	8b 00                	mov    eax,DWORD PTR [rax]
   140005cd7:	85 c0                	test   eax,eax
   140005cd9:	79 0e                	jns    140005ce9 <__mingw_pformat+0xc36>
   140005cdb:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140005cde:	8d 50 d0             	lea    edx,[rax-0x30]
   140005ce1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005ce5:	89 10                	mov    DWORD PTR [rax],edx
   140005ce7:	eb 4c                	jmp    140005d35 <__mingw_pformat+0xc82>
   140005ce9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005ced:	8b 10                	mov    edx,DWORD PTR [rax]
   140005cef:	89 d0                	mov    eax,edx
   140005cf1:	c1 e0 02             	shl    eax,0x2
   140005cf4:	01 d0                	add    eax,edx
   140005cf6:	01 c0                	add    eax,eax
   140005cf8:	89 c2                	mov    edx,eax
   140005cfa:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140005cfd:	01 d0                	add    eax,edx
   140005cff:	8d 50 d0             	lea    edx,[rax-0x30]
   140005d02:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005d06:	89 10                	mov    DWORD PTR [rax],edx
   140005d08:	eb 2b                	jmp    140005d35 <__mingw_pformat+0xc82>
   140005d0a:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140005d0e:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140005d12:	48 8d 45 a0          	lea    rax,[rbp-0x60]
   140005d16:	48 89 c2             	mov    rdx,rax
   140005d19:	b9 25 00 00 00       	mov    ecx,0x25
   140005d1e:	e8 fd d3 ff ff       	call   140003120 <__pformat_putc>
   140005d23:	e9 00 f4 ff ff       	jmp    140005128 <__mingw_pformat+0x75>
   140005d28:	90                   	nop
   140005d29:	eb 0a                	jmp    140005d35 <__mingw_pformat+0xc82>
   140005d2b:	90                   	nop
   140005d2c:	eb 07                	jmp    140005d35 <__mingw_pformat+0xc82>
   140005d2e:	90                   	nop
   140005d2f:	eb 04                	jmp    140005d35 <__mingw_pformat+0xc82>
   140005d31:	90                   	nop
   140005d32:	eb 01                	jmp    140005d35 <__mingw_pformat+0xc82>
   140005d34:	90                   	nop
   140005d35:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005d39:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005d3c:	84 c0                	test   al,al
   140005d3e:	0f 85 2d f4 ff ff    	jne    140005171 <__mingw_pformat+0xbe>
   140005d44:	eb 0e                	jmp    140005d54 <__mingw_pformat+0xca1>
   140005d46:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005d4a:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140005d4d:	89 c1                	mov    ecx,eax
   140005d4f:	e8 cc d3 ff ff       	call   140003120 <__pformat_putc>
   140005d54:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005d58:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140005d5c:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140005d60:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005d63:	0f be c0             	movsx  eax,al
   140005d66:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140005d69:	83 7d e8 00          	cmp    DWORD PTR [rbp-0x18],0x0
   140005d6d:	0f 85 ba f3 ff ff    	jne    14000512d <__mingw_pformat+0x7a>
   140005d73:	8b 45 c4             	mov    eax,DWORD PTR [rbp-0x3c]
   140005d76:	48 81 c4 d0 00 00 00 	add    rsp,0xd0
   140005d7d:	5d                   	pop    rbp
   140005d7e:	c3                   	ret
   140005d7f:	90                   	nop

0000000140005d80 <__rv_alloc_D2A>:
   140005d80:	55                   	push   rbp
   140005d81:	48 89 e5             	mov    rbp,rsp
   140005d84:	48 83 ec 30          	sub    rsp,0x30
   140005d88:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140005d8b:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005d92:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140005d99:	eb 07                	jmp    140005da2 <__rv_alloc_D2A+0x22>
   140005d9b:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
   140005d9f:	d1 65 fc             	shl    DWORD PTR [rbp-0x4],1
   140005da2:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140005da5:	83 c0 17             	add    eax,0x17
   140005da8:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   140005dab:	7f ee                	jg     140005d9b <__rv_alloc_D2A+0x1b>
   140005dad:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140005db0:	89 c1                	mov    ecx,eax
   140005db2:	e8 56 1e 00 00       	call   140007c0d <__Balloc_D2A>
   140005db7:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005dbb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005dbf:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140005dc2:	89 10                	mov    DWORD PTR [rax],edx
   140005dc4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005dc8:	48 83 c0 04          	add    rax,0x4
   140005dcc:	48 83 c4 30          	add    rsp,0x30
   140005dd0:	5d                   	pop    rbp
   140005dd1:	c3                   	ret

0000000140005dd2 <__nrv_alloc_D2A>:
   140005dd2:	55                   	push   rbp
   140005dd3:	48 89 e5             	mov    rbp,rsp
   140005dd6:	48 83 ec 30          	sub    rsp,0x30
   140005dda:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140005dde:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140005de2:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d
   140005de6:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140005de9:	89 c1                	mov    ecx,eax
   140005deb:	e8 90 ff ff ff       	call   140005d80 <__rv_alloc_D2A>
   140005df0:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005df4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005df8:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140005dfc:	eb 05                	jmp    140005e03 <__nrv_alloc_D2A+0x31>
   140005dfe:	48 83 45 f8 01       	add    QWORD PTR [rbp-0x8],0x1
   140005e03:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005e07:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140005e0b:	48 89 55 10          	mov    QWORD PTR [rbp+0x10],rdx
   140005e0f:	0f b6 10             	movzx  edx,BYTE PTR [rax]
   140005e12:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e16:	88 10                	mov    BYTE PTR [rax],dl
   140005e18:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e1c:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005e1f:	84 c0                	test   al,al
   140005e21:	75 db                	jne    140005dfe <__nrv_alloc_D2A+0x2c>
   140005e23:	48 83 7d 18 00       	cmp    QWORD PTR [rbp+0x18],0x0
   140005e28:	74 0b                	je     140005e35 <__nrv_alloc_D2A+0x63>
   140005e2a:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140005e2e:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140005e32:	48 89 10             	mov    QWORD PTR [rax],rdx
   140005e35:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005e39:	48 83 c4 30          	add    rsp,0x30
   140005e3d:	5d                   	pop    rbp
   140005e3e:	c3                   	ret

0000000140005e3f <__freedtoa>:
   140005e3f:	55                   	push   rbp
   140005e40:	48 89 e5             	mov    rbp,rsp
   140005e43:	48 83 ec 30          	sub    rsp,0x30
   140005e47:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140005e4b:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005e4f:	48 83 e8 04          	sub    rax,0x4
   140005e53:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140005e57:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e5b:	8b 10                	mov    edx,DWORD PTR [rax]
   140005e5d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e61:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140005e64:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e68:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140005e6b:	ba 01 00 00 00       	mov    edx,0x1
   140005e70:	89 c1                	mov    ecx,eax
   140005e72:	d3 e2                	shl    edx,cl
   140005e74:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e78:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140005e7b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e7f:	48 89 c1             	mov    rcx,rax
   140005e82:	e8 c7 1e 00 00       	call   140007d4e <__Bfree_D2A>
   140005e87:	90                   	nop
   140005e88:	48 83 c4 30          	add    rsp,0x30
   140005e8c:	5d                   	pop    rbp
   140005e8d:	c3                   	ret

0000000140005e8e <__quorem_D2A>:
   140005e8e:	55                   	push   rbp
   140005e8f:	48 89 e5             	mov    rbp,rsp
   140005e92:	48 83 ec 70          	sub    rsp,0x70
   140005e96:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140005e9a:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140005e9e:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140005ea2:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140005ea5:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140005ea8:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005eac:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140005eaf:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140005eb2:	7e 0a                	jle    140005ebe <__quorem_D2A+0x30>
   140005eb4:	b8 00 00 00 00       	mov    eax,0x0
   140005eb9:	e9 3f 02 00 00       	jmp    1400060fd <__quorem_D2A+0x26f>
   140005ebe:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140005ec2:	48 83 c0 18          	add    rax,0x18
   140005ec6:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140005eca:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   140005ece:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140005ed1:	48 98                	cdqe
   140005ed3:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140005eda:	00 
   140005edb:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140005edf:	48 01 d0             	add    rax,rdx
   140005ee2:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   140005ee6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005eea:	48 83 c0 18          	add    rax,0x18
   140005eee:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005ef2:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140005ef5:	48 98                	cdqe
   140005ef7:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140005efe:	00 
   140005eff:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005f03:	48 01 d0             	add    rax,rdx
   140005f06:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140005f0a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140005f0e:	8b 00                	mov    eax,DWORD PTR [rax]
   140005f10:	48 8b 55 c0          	mov    rdx,QWORD PTR [rbp-0x40]
   140005f14:	8b 12                	mov    edx,DWORD PTR [rdx]
   140005f16:	8d 4a 01             	lea    ecx,[rdx+0x1]
   140005f19:	ba 00 00 00 00       	mov    edx,0x0
   140005f1e:	f7 f1                	div    ecx
   140005f20:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140005f23:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140005f27:	0f 84 c4 00 00 00    	je     140005ff1 <__quorem_D2A+0x163>
   140005f2d:	48 c7 45 d0 00 00 00 	mov    QWORD PTR [rbp-0x30],0x0
   140005f34:	00 
   140005f35:	48 c7 45 c8 00 00 00 	mov    QWORD PTR [rbp-0x38],0x0
   140005f3c:	00 
   140005f3d:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140005f41:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140005f45:	48 89 55 d8          	mov    QWORD PTR [rbp-0x28],rdx
   140005f49:	8b 00                	mov    eax,DWORD PTR [rax]
   140005f4b:	89 c2                	mov    edx,eax
   140005f4d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140005f50:	48 0f af d0          	imul   rdx,rax
   140005f54:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140005f58:	48 01 d0             	add    rax,rdx
   140005f5b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140005f5f:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140005f63:	48 c1 e8 20          	shr    rax,0x20
   140005f67:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140005f6b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005f6f:	8b 00                	mov    eax,DWORD PTR [rax]
   140005f71:	89 c1                	mov    ecx,eax
   140005f73:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140005f77:	89 c2                	mov    edx,eax
   140005f79:	48 89 c8             	mov    rax,rcx
   140005f7c:	48 29 d0             	sub    rax,rdx
   140005f7f:	48 2b 45 d0          	sub    rax,QWORD PTR [rbp-0x30]
   140005f83:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140005f87:	48 8b 45 b0          	mov    rax,QWORD PTR [rbp-0x50]
   140005f8b:	48 c1 e8 20          	shr    rax,0x20
   140005f8f:	83 e0 01             	and    eax,0x1
   140005f92:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140005f96:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005f9a:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140005f9e:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140005fa2:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   140005fa6:	89 10                	mov    DWORD PTR [rax],edx
   140005fa8:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140005fac:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   140005fb0:	73 8b                	jae    140005f3d <__quorem_D2A+0xaf>
   140005fb2:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140005fb6:	8b 00                	mov    eax,DWORD PTR [rax]
   140005fb8:	85 c0                	test   eax,eax
   140005fba:	75 35                	jne    140005ff1 <__quorem_D2A+0x163>
   140005fbc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005fc0:	48 83 c0 18          	add    rax,0x18
   140005fc4:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005fc8:	eb 04                	jmp    140005fce <__quorem_D2A+0x140>
   140005fca:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   140005fce:	48 83 6d e8 04       	sub    QWORD PTR [rbp-0x18],0x4
   140005fd3:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140005fd7:	48 39 45 f0          	cmp    QWORD PTR [rbp-0x10],rax
   140005fdb:	73 0a                	jae    140005fe7 <__quorem_D2A+0x159>
   140005fdd:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140005fe1:	8b 00                	mov    eax,DWORD PTR [rax]
   140005fe3:	85 c0                	test   eax,eax
   140005fe5:	74 e3                	je     140005fca <__quorem_D2A+0x13c>
   140005fe7:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005feb:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   140005fee:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140005ff1:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140005ff5:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005ff9:	48 89 c1             	mov    rcx,rax
   140005ffc:	e8 bc 24 00 00       	call   1400084bd <__cmp_D2A>
   140006001:	85 c0                	test   eax,eax
   140006003:	0f 88 f1 00 00 00    	js     1400060fa <__quorem_D2A+0x26c>
   140006009:	83 45 e4 01          	add    DWORD PTR [rbp-0x1c],0x1
   14000600d:	48 c7 45 d0 00 00 00 	mov    QWORD PTR [rbp-0x30],0x0
   140006014:	00 
   140006015:	48 c7 45 c8 00 00 00 	mov    QWORD PTR [rbp-0x38],0x0
   14000601c:	00 
   14000601d:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140006021:	48 83 c0 18          	add    rax,0x18
   140006025:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140006029:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000602d:	48 83 c0 18          	add    rax,0x18
   140006031:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140006035:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140006039:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000603d:	48 89 55 d8          	mov    QWORD PTR [rbp-0x28],rdx
   140006041:	8b 00                	mov    eax,DWORD PTR [rax]
   140006043:	89 c2                	mov    edx,eax
   140006045:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140006049:	48 01 d0             	add    rax,rdx
   14000604c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140006050:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140006054:	48 c1 e8 20          	shr    rax,0x20
   140006058:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   14000605c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140006060:	8b 00                	mov    eax,DWORD PTR [rax]
   140006062:	89 c1                	mov    ecx,eax
   140006064:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140006068:	89 c2                	mov    edx,eax
   14000606a:	48 89 c8             	mov    rax,rcx
   14000606d:	48 29 d0             	sub    rax,rdx
   140006070:	48 2b 45 d0          	sub    rax,QWORD PTR [rbp-0x30]
   140006074:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140006078:	48 8b 45 b0          	mov    rax,QWORD PTR [rbp-0x50]
   14000607c:	48 c1 e8 20          	shr    rax,0x20
   140006080:	83 e0 01             	and    eax,0x1
   140006083:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140006087:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000608b:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000608f:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140006093:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   140006097:	89 10                	mov    DWORD PTR [rax],edx
   140006099:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000609d:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   1400060a1:	73 92                	jae    140006035 <__quorem_D2A+0x1a7>
   1400060a3:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400060a7:	48 83 c0 18          	add    rax,0x18
   1400060ab:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400060af:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400060b2:	48 98                	cdqe
   1400060b4:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   1400060bb:	00 
   1400060bc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400060c0:	48 01 d0             	add    rax,rdx
   1400060c3:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400060c7:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400060cb:	8b 00                	mov    eax,DWORD PTR [rax]
   1400060cd:	85 c0                	test   eax,eax
   1400060cf:	75 29                	jne    1400060fa <__quorem_D2A+0x26c>
   1400060d1:	eb 04                	jmp    1400060d7 <__quorem_D2A+0x249>
   1400060d3:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   1400060d7:	48 83 6d e8 04       	sub    QWORD PTR [rbp-0x18],0x4
   1400060dc:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400060e0:	48 39 45 f0          	cmp    QWORD PTR [rbp-0x10],rax
   1400060e4:	73 0a                	jae    1400060f0 <__quorem_D2A+0x262>
   1400060e6:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400060ea:	8b 00                	mov    eax,DWORD PTR [rax]
   1400060ec:	85 c0                	test   eax,eax
   1400060ee:	74 e3                	je     1400060d3 <__quorem_D2A+0x245>
   1400060f0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400060f4:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   1400060f7:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   1400060fa:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400060fd:	48 83 c4 70          	add    rsp,0x70
   140006101:	5d                   	pop    rbp
   140006102:	c3                   	ret
   140006103:	90                   	nop
   140006104:	90                   	nop
   140006105:	90                   	nop
   140006106:	90                   	nop
   140006107:	90                   	nop
   140006108:	90                   	nop
   140006109:	90                   	nop
   14000610a:	90                   	nop
   14000610b:	90                   	nop
   14000610c:	90                   	nop
   14000610d:	90                   	nop
   14000610e:	90                   	nop
   14000610f:	90                   	nop

0000000140006110 <__hi0bits_D2A>:
   140006110:	55                   	push   rbp
   140006111:	48 89 e5             	mov    rbp,rsp
   140006114:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140006117:	0f bd 45 10          	bsr    eax,DWORD PTR [rbp+0x10]
   14000611b:	83 f0 1f             	xor    eax,0x1f
   14000611e:	5d                   	pop    rbp
   14000611f:	c3                   	ret

0000000140006120 <bitstob>:
   140006120:	55                   	push   rbp
   140006121:	53                   	push   rbx
   140006122:	48 83 ec 58          	sub    rsp,0x58
   140006126:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   14000612b:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   14000612f:	89 55 28             	mov    DWORD PTR [rbp+0x28],edx
   140006132:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140006136:	c7 45 fc 20 00 00 00 	mov    DWORD PTR [rbp-0x4],0x20
   14000613d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140006144:	eb 07                	jmp    14000614d <bitstob+0x2d>
   140006146:	d1 65 fc             	shl    DWORD PTR [rbp-0x4],1
   140006149:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
   14000614d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140006150:	3b 45 28             	cmp    eax,DWORD PTR [rbp+0x28]
   140006153:	7c f1                	jl     140006146 <bitstob+0x26>
   140006155:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140006158:	89 c1                	mov    ecx,eax
   14000615a:	e8 ae 1a 00 00       	call   140007c0d <__Balloc_D2A>
   14000615f:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140006163:	8b 45 28             	mov    eax,DWORD PTR [rbp+0x28]
   140006166:	83 e8 01             	sub    eax,0x1
   140006169:	c1 f8 05             	sar    eax,0x5
   14000616c:	48 98                	cdqe
   14000616e:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140006175:	00 
   140006176:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000617a:	48 01 d0             	add    rax,rdx
   14000617d:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140006181:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140006185:	48 83 c0 18          	add    rax,0x18
   140006189:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000618d:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140006191:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140006195:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140006199:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000619d:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400061a1:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   1400061a5:	8b 12                	mov    edx,DWORD PTR [rdx]
   1400061a7:	89 10                	mov    DWORD PTR [rax],edx
   1400061a9:	48 83 45 20 04       	add    QWORD PTR [rbp+0x20],0x4
   1400061ae:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400061b2:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   1400061b6:	73 dd                	jae    140006195 <bitstob+0x75>
   1400061b8:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400061bc:	48 2b 45 d8          	sub    rax,QWORD PTR [rbp-0x28]
   1400061c0:	48 c1 f8 02          	sar    rax,0x2
   1400061c4:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400061c7:	eb 1d                	jmp    1400061e6 <bitstob+0xc6>
   1400061c9:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   1400061cd:	75 17                	jne    1400061e6 <bitstob+0xc6>
   1400061cf:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400061d3:	c7 40 14 00 00 00 00 	mov    DWORD PTR [rax+0x14],0x0
   1400061da:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400061de:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   1400061e4:	eb 59                	jmp    14000623f <bitstob+0x11f>
   1400061e6:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   1400061ea:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400061ed:	48 98                	cdqe
   1400061ef:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   1400061f6:	00 
   1400061f7:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   1400061fb:	48 01 d0             	add    rax,rdx
   1400061fe:	8b 00                	mov    eax,DWORD PTR [rax]
   140006200:	85 c0                	test   eax,eax
   140006202:	74 c5                	je     1400061c9 <bitstob+0xa9>
   140006204:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140006207:	8d 50 01             	lea    edx,[rax+0x1]
   14000620a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000620e:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140006211:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140006214:	83 c0 01             	add    eax,0x1
   140006217:	c1 e0 05             	shl    eax,0x5
   14000621a:	89 c3                	mov    ebx,eax
   14000621c:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140006220:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   140006223:	48 63 d2             	movsxd rdx,edx
   140006226:	48 83 c2 04          	add    rdx,0x4
   14000622a:	8b 44 90 08          	mov    eax,DWORD PTR [rax+rdx*4+0x8]
   14000622e:	89 c1                	mov    ecx,eax
   140006230:	e8 db fe ff ff       	call   140006110 <__hi0bits_D2A>
   140006235:	29 c3                	sub    ebx,eax
   140006237:	89 da                	mov    edx,ebx
   140006239:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   14000623d:	89 10                	mov    DWORD PTR [rax],edx
   14000623f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140006243:	48 83 c4 58          	add    rsp,0x58
   140006247:	5b                   	pop    rbx
   140006248:	5d                   	pop    rbp
   140006249:	c3                   	ret

000000014000624a <__gdtoa>:
   14000624a:	55                   	push   rbp
   14000624b:	48 81 ec 00 01 00 00 	sub    rsp,0x100
   140006252:	48 8d ac 24 80 00 00 	lea    rbp,[rsp+0x80]
   140006259:	00 
   14000625a:	48 89 8d 90 00 00 00 	mov    QWORD PTR [rbp+0x90],rcx
   140006261:	89 95 98 00 00 00    	mov    DWORD PTR [rbp+0x98],edx
   140006267:	4c 89 85 a0 00 00 00 	mov    QWORD PTR [rbp+0xa0],r8
   14000626e:	4c 89 8d a8 00 00 00 	mov    QWORD PTR [rbp+0xa8],r9
   140006275:	c7 45 64 00 00 00 00 	mov    DWORD PTR [rbp+0x64],0x0
   14000627c:	48 8b 85 a8 00 00 00 	mov    rax,QWORD PTR [rbp+0xa8]
   140006283:	8b 00                	mov    eax,DWORD PTR [rax]
   140006285:	83 e0 cf             	and    eax,0xffffffcf
   140006288:	89 c2                	mov    edx,eax
   14000628a:	48 8b 85 a8 00 00 00 	mov    rax,QWORD PTR [rbp+0xa8]
   140006291:	89 10                	mov    DWORD PTR [rax],edx
   140006293:	48 8b 85 a8 00 00 00 	mov    rax,QWORD PTR [rbp+0xa8]
   14000629a:	8b 00                	mov    eax,DWORD PTR [rax]
   14000629c:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   14000629f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400062a2:	83 e0 07             	and    eax,0x7
   1400062a5:	83 f8 04             	cmp    eax,0x4
   1400062a8:	0f 84 b0 00 00 00    	je     14000635e <__gdtoa+0x114>
   1400062ae:	83 f8 04             	cmp    eax,0x4
   1400062b1:	0f 8f d5 00 00 00    	jg     14000638c <__gdtoa+0x142>
   1400062b7:	83 f8 03             	cmp    eax,0x3
   1400062ba:	74 74                	je     140006330 <__gdtoa+0xe6>
   1400062bc:	83 f8 03             	cmp    eax,0x3
   1400062bf:	0f 8f c7 00 00 00    	jg     14000638c <__gdtoa+0x142>
   1400062c5:	85 c0                	test   eax,eax
   1400062c7:	0f 84 05 01 00 00    	je     1400063d2 <__gdtoa+0x188>
   1400062cd:	85 c0                	test   eax,eax
   1400062cf:	0f 88 b7 00 00 00    	js     14000638c <__gdtoa+0x142>
   1400062d5:	83 e8 01             	sub    eax,0x1
   1400062d8:	83 f8 01             	cmp    eax,0x1
   1400062db:	0f 87 ab 00 00 00    	ja     14000638c <__gdtoa+0x142>
   1400062e1:	90                   	nop
   1400062e2:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   1400062e9:	8b 00                	mov    eax,DWORD PTR [rax]
   1400062eb:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   1400062ee:	48 8d 4d b4          	lea    rcx,[rbp-0x4c]
   1400062f2:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   1400062f5:	48 8b 85 a0 00 00 00 	mov    rax,QWORD PTR [rbp+0xa0]
   1400062fc:	49 89 c8             	mov    r8,rcx
   1400062ff:	48 89 c1             	mov    rcx,rax
   140006302:	e8 19 fe ff ff       	call   140006120 <bitstob>
   140006307:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   14000630b:	8b 85 98 00 00 00    	mov    eax,DWORD PTR [rbp+0x98]
   140006311:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140006314:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140006318:	48 89 c1             	mov    rcx,rax
   14000631b:	e8 31 16 00 00       	call   140007951 <__trailz_D2A>
   140006320:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006323:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006326:	85 c0                	test   eax,eax
   140006328:	0f 84 8b 00 00 00    	je     1400063b9 <__gdtoa+0x16f>
   14000632e:	eb 66                	jmp    140006396 <__gdtoa+0x14c>
   140006330:	48 8b 85 c0 00 00 00 	mov    rax,QWORD PTR [rbp+0xc0]
   140006337:	c7 00 00 80 ff ff    	mov    DWORD PTR [rax],0xffff8000
   14000633d:	48 8b 85 c8 00 00 00 	mov    rax,QWORD PTR [rbp+0xc8]
   140006344:	48 8d 0d 05 50 00 00 	lea    rcx,[rip+0x5005]        # 14000b350 <.rdata>
   14000634b:	41 b8 08 00 00 00    	mov    r8d,0x8
   140006351:	48 89 c2             	mov    rdx,rax
   140006354:	e8 79 fa ff ff       	call   140005dd2 <__nrv_alloc_D2A>
   140006359:	e9 4a 14 00 00       	jmp    1400077a8 <__gdtoa+0x155e>
   14000635e:	48 8b 85 c0 00 00 00 	mov    rax,QWORD PTR [rbp+0xc0]
   140006365:	c7 00 00 80 ff ff    	mov    DWORD PTR [rax],0xffff8000
   14000636b:	48 8b 85 c8 00 00 00 	mov    rax,QWORD PTR [rbp+0xc8]
   140006372:	48 8d 0d e0 4f 00 00 	lea    rcx,[rip+0x4fe0]        # 14000b359 <.rdata+0x9>
   140006379:	41 b8 03 00 00 00    	mov    r8d,0x3
   14000637f:	48 89 c2             	mov    rdx,rax
   140006382:	e8 4b fa ff ff       	call   140005dd2 <__nrv_alloc_D2A>
   140006387:	e9 1c 14 00 00       	jmp    1400077a8 <__gdtoa+0x155e>
   14000638c:	b8 00 00 00 00       	mov    eax,0x0
   140006391:	e9 12 14 00 00       	jmp    1400077a8 <__gdtoa+0x155e>
   140006396:	8b 55 b0             	mov    edx,DWORD PTR [rbp-0x50]
   140006399:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000639d:	48 89 c1             	mov    rcx,rax
   1400063a0:	e8 50 14 00 00       	call   1400077f5 <__rshift_D2A>
   1400063a5:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400063a8:	01 85 98 00 00 00    	add    DWORD PTR [rbp+0x98],eax
   1400063ae:	8b 55 b4             	mov    edx,DWORD PTR [rbp-0x4c]
   1400063b1:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400063b4:	29 c2                	sub    edx,eax
   1400063b6:	89 55 b4             	mov    DWORD PTR [rbp-0x4c],edx
   1400063b9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400063bd:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400063c0:	85 c0                	test   eax,eax
   1400063c2:	75 3d                	jne    140006401 <__gdtoa+0x1b7>
   1400063c4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400063c8:	48 89 c1             	mov    rcx,rax
   1400063cb:	e8 7e 19 00 00       	call   140007d4e <__Bfree_D2A>
   1400063d0:	eb 01                	jmp    1400063d3 <__gdtoa+0x189>
   1400063d2:	90                   	nop
   1400063d3:	48 8b 85 c0 00 00 00 	mov    rax,QWORD PTR [rbp+0xc0]
   1400063da:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   1400063e0:	48 8b 85 c8 00 00 00 	mov    rax,QWORD PTR [rbp+0xc8]
   1400063e7:	48 8d 0d 6f 4f 00 00 	lea    rcx,[rip+0x4f6f]        # 14000b35d <.rdata+0xd>
   1400063ee:	41 b8 01 00 00 00    	mov    r8d,0x1
   1400063f4:	48 89 c2             	mov    rdx,rax
   1400063f7:	e8 d6 f9 ff ff       	call   140005dd2 <__nrv_alloc_D2A>
   1400063fc:	e9 a7 13 00 00       	jmp    1400077a8 <__gdtoa+0x155e>
   140006401:	48 8d 55 b0          	lea    rdx,[rbp-0x50]
   140006405:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140006409:	48 89 c1             	mov    rcx,rax
   14000640c:	e8 75 23 00 00       	call   140008786 <__b2d_D2A>
   140006411:	66 48 0f 7e c0       	movq   rax,xmm0
   140006416:	48 89 45 a8          	mov    QWORD PTR [rbp-0x58],rax
   14000641a:	8b 55 b4             	mov    edx,DWORD PTR [rbp-0x4c]
   14000641d:	8b 85 98 00 00 00    	mov    eax,DWORD PTR [rbp+0x98]
   140006423:	01 d0                	add    eax,edx
   140006425:	83 e8 01             	sub    eax,0x1
   140006428:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   14000642b:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
   14000642e:	25 ff ff 0f 00       	and    eax,0xfffff
   140006433:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   140006436:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
   140006439:	0d 00 00 f0 3f       	or     eax,0x3ff00000
   14000643e:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   140006441:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006446:	f2 0f 10 15 12 4f 00 	movsd  xmm2,QWORD PTR [rip+0x4f12]        # 14000b360 <.rdata+0x10>
   14000644d:	00 
   14000644e:	66 0f 28 c8          	movapd xmm1,xmm0
   140006452:	f2 0f 5c ca          	subsd  xmm1,xmm2
   140006456:	f2 0f 10 05 0a 4f 00 	movsd  xmm0,QWORD PTR [rip+0x4f0a]        # 14000b368 <.rdata+0x18>
   14000645d:	00 
   14000645e:	f2 0f 59 c8          	mulsd  xmm1,xmm0
   140006462:	f2 0f 10 05 06 4f 00 	movsd  xmm0,QWORD PTR [rip+0x4f06]        # 14000b370 <.rdata+0x20>
   140006469:	00 
   14000646a:	f2 0f 58 c8          	addsd  xmm1,xmm0
   14000646e:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006471:	66 0f ef d2          	pxor   xmm2,xmm2
   140006475:	f2 0f 2a d0          	cvtsi2sd xmm2,eax
   140006479:	f2 0f 10 05 f7 4e 00 	movsd  xmm0,QWORD PTR [rip+0x4ef7]        # 14000b378 <.rdata+0x28>
   140006480:	00 
   140006481:	f2 0f 59 c2          	mulsd  xmm0,xmm2
   140006485:	f2 0f 58 c1          	addsd  xmm0,xmm1
   140006489:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   14000648e:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006491:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140006494:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140006498:	79 03                	jns    14000649d <__gdtoa+0x253>
   14000649a:	f7 5d 60             	neg    DWORD PTR [rbp+0x60]
   14000649d:	81 6d 60 35 04 00 00 	sub    DWORD PTR [rbp+0x60],0x435
   1400064a4:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   1400064a8:	7e 23                	jle    1400064cd <__gdtoa+0x283>
   1400064aa:	66 0f ef c9          	pxor   xmm1,xmm1
   1400064ae:	f2 0f 2a 4d 60       	cvtsi2sd xmm1,DWORD PTR [rbp+0x60]
   1400064b3:	f2 0f 10 05 c5 4e 00 	movsd  xmm0,QWORD PTR [rip+0x4ec5]        # 14000b380 <.rdata+0x30>
   1400064ba:	00 
   1400064bb:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   1400064bf:	f2 0f 10 4d 08       	movsd  xmm1,QWORD PTR [rbp+0x8]
   1400064c4:	f2 0f 58 c1          	addsd  xmm0,xmm1
   1400064c8:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   1400064cd:	f2 0f 10 45 08       	movsd  xmm0,QWORD PTR [rbp+0x8]
   1400064d2:	f2 0f 2c c0          	cvttsd2si eax,xmm0
   1400064d6:	89 45 58             	mov    DWORD PTR [rbp+0x58],eax
   1400064d9:	66 0f ef c0          	pxor   xmm0,xmm0
   1400064dd:	66 0f 2f 45 08       	comisd xmm0,QWORD PTR [rbp+0x8]
   1400064e2:	76 1b                	jbe    1400064ff <__gdtoa+0x2b5>
   1400064e4:	66 0f ef c0          	pxor   xmm0,xmm0
   1400064e8:	f2 0f 2a 45 58       	cvtsi2sd xmm0,DWORD PTR [rbp+0x58]
   1400064ed:	66 0f 2e 45 08       	ucomisd xmm0,QWORD PTR [rbp+0x8]
   1400064f2:	7a 07                	jp     1400064fb <__gdtoa+0x2b1>
   1400064f4:	66 0f 2e 45 08       	ucomisd xmm0,QWORD PTR [rbp+0x8]
   1400064f9:	74 04                	je     1400064ff <__gdtoa+0x2b5>
   1400064fb:	83 6d 58 01          	sub    DWORD PTR [rbp+0x58],0x1
   1400064ff:	c7 45 54 01 00 00 00 	mov    DWORD PTR [rbp+0x54],0x1
   140006506:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
   140006509:	8b 4d b4             	mov    ecx,DWORD PTR [rbp-0x4c]
   14000650c:	8b 95 98 00 00 00    	mov    edx,DWORD PTR [rbp+0x98]
   140006512:	01 ca                	add    edx,ecx
   140006514:	83 ea 01             	sub    edx,0x1
   140006517:	c1 e2 14             	shl    edx,0x14
   14000651a:	01 d0                	add    eax,edx
   14000651c:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000651f:	83 7d 58 00          	cmp    DWORD PTR [rbp+0x58],0x0
   140006523:	78 2e                	js     140006553 <__gdtoa+0x309>
   140006525:	83 7d 58 16          	cmp    DWORD PTR [rbp+0x58],0x16
   140006529:	7f 28                	jg     140006553 <__gdtoa+0x309>
   14000652b:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006530:	48 8b 05 49 51 00 00 	mov    rax,QWORD PTR [rip+0x5149]        # 14000b680 <.refptr.__tens_D2A>
   140006537:	8b 55 58             	mov    edx,DWORD PTR [rbp+0x58]
   14000653a:	48 63 d2             	movsxd rdx,edx
   14000653d:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   140006542:	66 0f 2f c1          	comisd xmm0,xmm1
   140006546:	76 04                	jbe    14000654c <__gdtoa+0x302>
   140006548:	83 6d 58 01          	sub    DWORD PTR [rbp+0x58],0x1
   14000654c:	c7 45 54 00 00 00 00 	mov    DWORD PTR [rbp+0x54],0x0
   140006553:	8b 55 b4             	mov    edx,DWORD PTR [rbp-0x4c]
   140006556:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006559:	29 c2                	sub    edx,eax
   14000655b:	8d 42 ff             	lea    eax,[rdx-0x1]
   14000655e:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140006561:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140006565:	78 0f                	js     140006576 <__gdtoa+0x32c>
   140006567:	c7 45 7c 00 00 00 00 	mov    DWORD PTR [rbp+0x7c],0x0
   14000656e:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006571:	89 45 40             	mov    DWORD PTR [rbp+0x40],eax
   140006574:	eb 0f                	jmp    140006585 <__gdtoa+0x33b>
   140006576:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006579:	f7 d8                	neg    eax
   14000657b:	89 45 7c             	mov    DWORD PTR [rbp+0x7c],eax
   14000657e:	c7 45 40 00 00 00 00 	mov    DWORD PTR [rbp+0x40],0x0
   140006585:	83 7d 58 00          	cmp    DWORD PTR [rbp+0x58],0x0
   140006589:	78 15                	js     1400065a0 <__gdtoa+0x356>
   14000658b:	c7 45 78 00 00 00 00 	mov    DWORD PTR [rbp+0x78],0x0
   140006592:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   140006595:	89 45 3c             	mov    DWORD PTR [rbp+0x3c],eax
   140006598:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   14000659b:	01 45 40             	add    DWORD PTR [rbp+0x40],eax
   14000659e:	eb 15                	jmp    1400065b5 <__gdtoa+0x36b>
   1400065a0:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400065a3:	29 45 7c             	sub    DWORD PTR [rbp+0x7c],eax
   1400065a6:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400065a9:	f7 d8                	neg    eax
   1400065ab:	89 45 78             	mov    DWORD PTR [rbp+0x78],eax
   1400065ae:	c7 45 3c 00 00 00 00 	mov    DWORD PTR [rbp+0x3c],0x0
   1400065b5:	83 bd b0 00 00 00 00 	cmp    DWORD PTR [rbp+0xb0],0x0
   1400065bc:	78 09                	js     1400065c7 <__gdtoa+0x37d>
   1400065be:	83 bd b0 00 00 00 09 	cmp    DWORD PTR [rbp+0xb0],0x9
   1400065c5:	7e 0a                	jle    1400065d1 <__gdtoa+0x387>
   1400065c7:	c7 85 b0 00 00 00 00 	mov    DWORD PTR [rbp+0xb0],0x0
   1400065ce:	00 00 00 
   1400065d1:	c7 45 34 01 00 00 00 	mov    DWORD PTR [rbp+0x34],0x1
   1400065d8:	83 bd b0 00 00 00 05 	cmp    DWORD PTR [rbp+0xb0],0x5
   1400065df:	7e 10                	jle    1400065f1 <__gdtoa+0x3a7>
   1400065e1:	83 ad b0 00 00 00 04 	sub    DWORD PTR [rbp+0xb0],0x4
   1400065e8:	c7 45 34 00 00 00 00 	mov    DWORD PTR [rbp+0x34],0x0
   1400065ef:	eb 1b                	jmp    14000660c <__gdtoa+0x3c2>
   1400065f1:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400065f4:	3d f9 03 00 00       	cmp    eax,0x3f9
   1400065f9:	7f 0a                	jg     140006605 <__gdtoa+0x3bb>
   1400065fb:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400065fe:	3d 02 fc ff ff       	cmp    eax,0xfffffc02
   140006603:	7d 07                	jge    14000660c <__gdtoa+0x3c2>
   140006605:	c7 45 34 00 00 00 00 	mov    DWORD PTR [rbp+0x34],0x0
   14000660c:	c7 45 50 01 00 00 00 	mov    DWORD PTR [rbp+0x50],0x1
   140006613:	c7 45 68 ff ff ff ff 	mov    DWORD PTR [rbp+0x68],0xffffffff
   14000661a:	8b 45 68             	mov    eax,DWORD PTR [rbp+0x68]
   14000661d:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   140006620:	83 bd b0 00 00 00 05 	cmp    DWORD PTR [rbp+0xb0],0x5
   140006627:	0f 84 c5 00 00 00    	je     1400066f2 <__gdtoa+0x4a8>
   14000662d:	83 bd b0 00 00 00 05 	cmp    DWORD PTR [rbp+0xb0],0x5
   140006634:	0f 8f e6 00 00 00    	jg     140006720 <__gdtoa+0x4d6>
   14000663a:	83 bd b0 00 00 00 04 	cmp    DWORD PTR [rbp+0xb0],0x4
   140006641:	74 7e                	je     1400066c1 <__gdtoa+0x477>
   140006643:	83 bd b0 00 00 00 04 	cmp    DWORD PTR [rbp+0xb0],0x4
   14000664a:	0f 8f d0 00 00 00    	jg     140006720 <__gdtoa+0x4d6>
   140006650:	83 bd b0 00 00 00 03 	cmp    DWORD PTR [rbp+0xb0],0x3
   140006657:	0f 84 8e 00 00 00    	je     1400066eb <__gdtoa+0x4a1>
   14000665d:	83 bd b0 00 00 00 03 	cmp    DWORD PTR [rbp+0xb0],0x3
   140006664:	0f 8f b6 00 00 00    	jg     140006720 <__gdtoa+0x4d6>
   14000666a:	83 bd b0 00 00 00 01 	cmp    DWORD PTR [rbp+0xb0],0x1
   140006671:	7f 0e                	jg     140006681 <__gdtoa+0x437>
   140006673:	83 bd b0 00 00 00 00 	cmp    DWORD PTR [rbp+0xb0],0x0
   14000667a:	79 13                	jns    14000668f <__gdtoa+0x445>
   14000667c:	e9 9f 00 00 00       	jmp    140006720 <__gdtoa+0x4d6>
   140006681:	83 bd b0 00 00 00 02 	cmp    DWORD PTR [rbp+0xb0],0x2
   140006688:	74 30                	je     1400066ba <__gdtoa+0x470>
   14000668a:	e9 91 00 00 00       	jmp    140006720 <__gdtoa+0x4d6>
   14000668f:	66 0f ef c9          	pxor   xmm1,xmm1
   140006693:	f2 0f 2a 4d f8       	cvtsi2sd xmm1,DWORD PTR [rbp-0x8]
   140006698:	f2 0f 10 05 e8 4c 00 	movsd  xmm0,QWORD PTR [rip+0x4ce8]        # 14000b388 <.rdata+0x38>
   14000669f:	00 
   1400066a0:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   1400066a4:	f2 0f 2c c0          	cvttsd2si eax,xmm0
   1400066a8:	83 c0 03             	add    eax,0x3
   1400066ab:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   1400066ae:	c7 85 b8 00 00 00 00 	mov    DWORD PTR [rbp+0xb8],0x0
   1400066b5:	00 00 00 
   1400066b8:	eb 66                	jmp    140006720 <__gdtoa+0x4d6>
   1400066ba:	c7 45 50 00 00 00 00 	mov    DWORD PTR [rbp+0x50],0x0
   1400066c1:	83 bd b8 00 00 00 00 	cmp    DWORD PTR [rbp+0xb8],0x0
   1400066c8:	7f 0a                	jg     1400066d4 <__gdtoa+0x48a>
   1400066ca:	c7 85 b8 00 00 00 01 	mov    DWORD PTR [rbp+0xb8],0x1
   1400066d1:	00 00 00 
   1400066d4:	8b 85 b8 00 00 00    	mov    eax,DWORD PTR [rbp+0xb8]
   1400066da:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   1400066dd:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400066e0:	89 45 68             	mov    DWORD PTR [rbp+0x68],eax
   1400066e3:	8b 45 68             	mov    eax,DWORD PTR [rbp+0x68]
   1400066e6:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   1400066e9:	eb 35                	jmp    140006720 <__gdtoa+0x4d6>
   1400066eb:	c7 45 50 00 00 00 00 	mov    DWORD PTR [rbp+0x50],0x0
   1400066f2:	8b 95 b8 00 00 00    	mov    edx,DWORD PTR [rbp+0xb8]
   1400066f8:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400066fb:	01 d0                	add    eax,edx
   1400066fd:	83 c0 01             	add    eax,0x1
   140006700:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006703:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006706:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   140006709:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   14000670c:	83 e8 01             	sub    eax,0x1
   14000670f:	89 45 68             	mov    DWORD PTR [rbp+0x68],eax
   140006712:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006715:	85 c0                	test   eax,eax
   140006717:	7f 07                	jg     140006720 <__gdtoa+0x4d6>
   140006719:	c7 45 b0 01 00 00 00 	mov    DWORD PTR [rbp-0x50],0x1
   140006720:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006723:	89 c1                	mov    ecx,eax
   140006725:	e8 56 f6 ff ff       	call   140005d80 <__rv_alloc_D2A>
   14000672a:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   14000672e:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140006732:	48 89 45 00          	mov    QWORD PTR [rbp+0x0],rax
   140006736:	83 bd b0 00 00 00 01 	cmp    DWORD PTR [rbp+0xb0],0x1
   14000673d:	7f 09                	jg     140006748 <__gdtoa+0x4fe>
   14000673f:	c7 45 44 00 00 00 00 	mov    DWORD PTR [rbp+0x44],0x0
   140006746:	eb 38                	jmp    140006780 <__gdtoa+0x536>
   140006748:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   14000674f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140006752:	83 e8 01             	sub    eax,0x1
   140006755:	89 45 44             	mov    DWORD PTR [rbp+0x44],eax
   140006758:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   14000675c:	74 22                	je     140006780 <__gdtoa+0x536>
   14000675e:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   140006762:	79 07                	jns    14000676b <__gdtoa+0x521>
   140006764:	c7 45 44 02 00 00 00 	mov    DWORD PTR [rbp+0x44],0x2
   14000676b:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000676e:	83 e0 08             	and    eax,0x8
   140006771:	85 c0                	test   eax,eax
   140006773:	74 0b                	je     140006780 <__gdtoa+0x536>
   140006775:	b8 03 00 00 00       	mov    eax,0x3
   14000677a:	2b 45 44             	sub    eax,DWORD PTR [rbp+0x44]
   14000677d:	89 45 44             	mov    DWORD PTR [rbp+0x44],eax
   140006780:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006784:	0f 88 b9 04 00 00    	js     140006c43 <__gdtoa+0x9f9>
   14000678a:	83 7d 6c 0e          	cmp    DWORD PTR [rbp+0x6c],0xe
   14000678e:	0f 8f af 04 00 00    	jg     140006c43 <__gdtoa+0x9f9>
   140006794:	83 7d 34 00          	cmp    DWORD PTR [rbp+0x34],0x0
   140006798:	0f 84 a5 04 00 00    	je     140006c43 <__gdtoa+0x9f9>
   14000679e:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   1400067a2:	0f 85 9b 04 00 00    	jne    140006c43 <__gdtoa+0x9f9>
   1400067a8:	83 7d 58 00          	cmp    DWORD PTR [rbp+0x58],0x0
   1400067ac:	0f 85 91 04 00 00    	jne    140006c43 <__gdtoa+0x9f9>
   1400067b2:	c7 45 b0 00 00 00 00 	mov    DWORD PTR [rbp-0x50],0x0
   1400067b9:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   1400067be:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   1400067c3:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400067c6:	89 45 dc             	mov    DWORD PTR [rbp-0x24],eax
   1400067c9:	8b 45 6c             	mov    eax,DWORD PTR [rbp+0x6c]
   1400067cc:	89 45 d8             	mov    DWORD PTR [rbp-0x28],eax
   1400067cf:	c7 45 70 02 00 00 00 	mov    DWORD PTR [rbp+0x70],0x2
   1400067d6:	83 7d 58 00          	cmp    DWORD PTR [rbp+0x58],0x0
   1400067da:	0f 8e 98 00 00 00    	jle    140006878 <__gdtoa+0x62e>
   1400067e0:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400067e3:	83 e0 0f             	and    eax,0xf
   1400067e6:	89 c2                	mov    edx,eax
   1400067e8:	48 8b 05 91 4e 00 00 	mov    rax,QWORD PTR [rip+0x4e91]        # 14000b680 <.refptr.__tens_D2A>
   1400067ef:	48 63 d2             	movsxd rdx,edx
   1400067f2:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   1400067f7:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   1400067fc:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400067ff:	c1 f8 04             	sar    eax,0x4
   140006802:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140006805:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006808:	83 e0 10             	and    eax,0x10
   14000680b:	85 c0                	test   eax,eax
   14000680d:	74 5e                	je     14000686d <__gdtoa+0x623>
   14000680f:	83 65 60 0f          	and    DWORD PTR [rbp+0x60],0xf
   140006813:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006818:	48 8b 05 91 4d 00 00 	mov    rax,QWORD PTR [rip+0x4d91]        # 14000b5b0 <.refptr.__bigtens_D2A>
   14000681f:	f2 0f 10 48 20       	movsd  xmm1,QWORD PTR [rax+0x20]
   140006824:	f2 0f 5e c1          	divsd  xmm0,xmm1
   140006828:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   14000682d:	83 45 70 01          	add    DWORD PTR [rbp+0x70],0x1
   140006831:	eb 3a                	jmp    14000686d <__gdtoa+0x623>
   140006833:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006836:	83 e0 01             	and    eax,0x1
   140006839:	85 c0                	test   eax,eax
   14000683b:	74 24                	je     140006861 <__gdtoa+0x617>
   14000683d:	83 45 70 01          	add    DWORD PTR [rbp+0x70],0x1
   140006841:	8b 55 b0             	mov    edx,DWORD PTR [rbp-0x50]
   140006844:	48 8b 05 65 4d 00 00 	mov    rax,QWORD PTR [rip+0x4d65]        # 14000b5b0 <.refptr.__bigtens_D2A>
   14000684b:	48 63 d2             	movsxd rdx,edx
   14000684e:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   140006853:	f2 0f 10 4d 08       	movsd  xmm1,QWORD PTR [rbp+0x8]
   140006858:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   14000685c:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   140006861:	d1 7d 60             	sar    DWORD PTR [rbp+0x60],1
   140006864:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006867:	83 c0 01             	add    eax,0x1
   14000686a:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   14000686d:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140006871:	75 c0                	jne    140006833 <__gdtoa+0x5e9>
   140006873:	e9 8b 00 00 00       	jmp    140006903 <__gdtoa+0x6b9>
   140006878:	f2 0f 10 05 10 4b 00 	movsd  xmm0,QWORD PTR [rip+0x4b10]        # 14000b390 <.rdata+0x40>
   14000687f:	00 
   140006880:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   140006885:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   140006888:	f7 d8                	neg    eax
   14000688a:	89 45 5c             	mov    DWORD PTR [rbp+0x5c],eax
   14000688d:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   140006891:	74 70                	je     140006903 <__gdtoa+0x6b9>
   140006893:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006898:	8b 45 5c             	mov    eax,DWORD PTR [rbp+0x5c]
   14000689b:	83 e0 0f             	and    eax,0xf
   14000689e:	89 c2                	mov    edx,eax
   1400068a0:	48 8b 05 d9 4d 00 00 	mov    rax,QWORD PTR [rip+0x4dd9]        # 14000b680 <.refptr.__tens_D2A>
   1400068a7:	48 63 d2             	movsxd rdx,edx
   1400068aa:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   1400068af:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   1400068b3:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   1400068b8:	8b 45 5c             	mov    eax,DWORD PTR [rbp+0x5c]
   1400068bb:	c1 f8 04             	sar    eax,0x4
   1400068be:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   1400068c1:	eb 3a                	jmp    1400068fd <__gdtoa+0x6b3>
   1400068c3:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   1400068c6:	83 e0 01             	and    eax,0x1
   1400068c9:	85 c0                	test   eax,eax
   1400068cb:	74 24                	je     1400068f1 <__gdtoa+0x6a7>
   1400068cd:	83 45 70 01          	add    DWORD PTR [rbp+0x70],0x1
   1400068d1:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   1400068d6:	8b 55 b0             	mov    edx,DWORD PTR [rbp-0x50]
   1400068d9:	48 8b 05 d0 4c 00 00 	mov    rax,QWORD PTR [rip+0x4cd0]        # 14000b5b0 <.refptr.__bigtens_D2A>
   1400068e0:	48 63 d2             	movsxd rdx,edx
   1400068e3:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   1400068e8:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   1400068ec:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   1400068f1:	d1 7d 60             	sar    DWORD PTR [rbp+0x60],1
   1400068f4:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400068f7:	83 c0 01             	add    eax,0x1
   1400068fa:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   1400068fd:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140006901:	75 c0                	jne    1400068c3 <__gdtoa+0x679>
   140006903:	83 7d 54 00          	cmp    DWORD PTR [rbp+0x54],0x0
   140006907:	74 47                	je     140006950 <__gdtoa+0x706>
   140006909:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   14000690e:	f2 0f 10 05 7a 4a 00 	movsd  xmm0,QWORD PTR [rip+0x4a7a]        # 14000b390 <.rdata+0x40>
   140006915:	00 
   140006916:	66 0f 2f c1          	comisd xmm0,xmm1
   14000691a:	76 34                	jbe    140006950 <__gdtoa+0x706>
   14000691c:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006920:	7e 2e                	jle    140006950 <__gdtoa+0x706>
   140006922:	83 7d 68 00          	cmp    DWORD PTR [rbp+0x68],0x0
   140006926:	0f 8e f5 02 00 00    	jle    140006c21 <__gdtoa+0x9d7>
   14000692c:	8b 45 68             	mov    eax,DWORD PTR [rbp+0x68]
   14000692f:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   140006932:	83 6d 58 01          	sub    DWORD PTR [rbp+0x58],0x1
   140006936:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   14000693b:	f2 0f 10 05 55 4a 00 	movsd  xmm0,QWORD PTR [rip+0x4a55]        # 14000b398 <.rdata+0x48>
   140006942:	00 
   140006943:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006947:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   14000694c:	83 45 70 01          	add    DWORD PTR [rbp+0x70],0x1
   140006950:	66 0f ef c9          	pxor   xmm1,xmm1
   140006954:	f2 0f 2a 4d 70       	cvtsi2sd xmm1,DWORD PTR [rbp+0x70]
   140006959:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   14000695e:	f2 0f 59 c8          	mulsd  xmm1,xmm0
   140006962:	f2 0f 10 05 36 4a 00 	movsd  xmm0,QWORD PTR [rip+0x4a36]        # 14000b3a0 <.rdata+0x50>
   140006969:	00 
   14000696a:	f2 0f 58 c1          	addsd  xmm0,xmm1
   14000696e:	f2 0f 11 45 a0       	movsd  QWORD PTR [rbp-0x60],xmm0
   140006973:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
   140006976:	2d 00 00 40 03       	sub    eax,0x3400000
   14000697b:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
   14000697e:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006982:	75 5f                	jne    1400069e3 <__gdtoa+0x799>
   140006984:	48 c7 45 18 00 00 00 	mov    QWORD PTR [rbp+0x18],0x0
   14000698b:	00 
   14000698c:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140006990:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140006994:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006999:	f2 0f 10 0d 07 4a 00 	movsd  xmm1,QWORD PTR [rip+0x4a07]        # 14000b3a8 <.rdata+0x58>
   1400069a0:	00 
   1400069a1:	f2 0f 5c c1          	subsd  xmm0,xmm1
   1400069a5:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   1400069aa:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   1400069af:	f2 0f 10 4d a0       	movsd  xmm1,QWORD PTR [rbp-0x60]
   1400069b4:	66 0f 2f c1          	comisd xmm0,xmm1
   1400069b8:	0f 87 ac 07 00 00    	ja     14000716a <__gdtoa+0xf20>
   1400069be:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   1400069c3:	f2 0f 10 45 a0       	movsd  xmm0,QWORD PTR [rbp-0x60]
   1400069c8:	f3 0f 7e 15 e0 49 00 	movq   xmm2,QWORD PTR [rip+0x49e0]        # 14000b3b0 <.rdata+0x60>
   1400069cf:	00 
   1400069d0:	66 0f 57 c2          	xorpd  xmm0,xmm2
   1400069d4:	66 0f 2f c1          	comisd xmm0,xmm1
   1400069d8:	0f 87 6e 07 00 00    	ja     14000714c <__gdtoa+0xf02>
   1400069de:	e9 42 02 00 00       	jmp    140006c25 <__gdtoa+0x9db>
   1400069e3:	83 7d 50 00          	cmp    DWORD PTR [rbp+0x50],0x0
   1400069e7:	0f 84 22 01 00 00    	je     140006b0f <__gdtoa+0x8c5>
   1400069ed:	f2 0f 10 4d 08       	movsd  xmm1,QWORD PTR [rbp+0x8]
   1400069f2:	f2 0f 10 05 c6 49 00 	movsd  xmm0,QWORD PTR [rip+0x49c6]        # 14000b3c0 <.rdata+0x70>
   1400069f9:	00 
   1400069fa:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   1400069fe:	8b 45 6c             	mov    eax,DWORD PTR [rbp+0x6c]
   140006a01:	8d 50 ff             	lea    edx,[rax-0x1]
   140006a04:	48 8b 05 75 4c 00 00 	mov    rax,QWORD PTR [rip+0x4c75]        # 14000b680 <.refptr.__tens_D2A>
   140006a0b:	48 63 d2             	movsxd rdx,edx
   140006a0e:	f2 0f 10 0c d0       	movsd  xmm1,QWORD PTR [rax+rdx*8]
   140006a13:	f2 0f 5e c1          	divsd  xmm0,xmm1
   140006a17:	f2 0f 10 4d a0       	movsd  xmm1,QWORD PTR [rbp-0x60]
   140006a1c:	f2 0f 5c c1          	subsd  xmm0,xmm1
   140006a20:	f2 0f 11 45 a0       	movsd  QWORD PTR [rbp-0x60],xmm0
   140006a25:	c7 45 b0 00 00 00 00 	mov    DWORD PTR [rbp-0x50],0x0
   140006a2c:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006a31:	f2 0f 5e 45 08       	divsd  xmm0,QWORD PTR [rbp+0x8]
   140006a36:	f2 0f 2c c0          	cvttsd2si eax,xmm0
   140006a3a:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   140006a3d:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006a42:	66 0f ef c9          	pxor   xmm1,xmm1
   140006a46:	f2 0f 2a 4d d4       	cvtsi2sd xmm1,DWORD PTR [rbp-0x2c]
   140006a4b:	f2 0f 59 4d 08       	mulsd  xmm1,QWORD PTR [rbp+0x8]
   140006a50:	f2 0f 5c c1          	subsd  xmm0,xmm1
   140006a54:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006a59:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140006a5c:	8d 48 30             	lea    ecx,[rax+0x30]
   140006a5f:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006a63:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140006a67:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140006a6b:	89 ca                	mov    edx,ecx
   140006a6d:	88 10                	mov    BYTE PTR [rax],dl
   140006a6f:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006a74:	f2 0f 10 45 a0       	movsd  xmm0,QWORD PTR [rbp-0x60]
   140006a79:	66 0f 2f c1          	comisd xmm0,xmm1
   140006a7d:	76 29                	jbe    140006aa8 <__gdtoa+0x85e>
   140006a7f:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006a84:	66 0f ef c9          	pxor   xmm1,xmm1
   140006a88:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006a8c:	7a 0e                	jp     140006a9c <__gdtoa+0x852>
   140006a8e:	66 0f ef c9          	pxor   xmm1,xmm1
   140006a92:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006a96:	0f 84 90 0c 00 00    	je     14000772c <__gdtoa+0x14e2>
   140006a9c:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140006aa3:	e9 84 0c 00 00       	jmp    14000772c <__gdtoa+0x14e2>
   140006aa8:	f2 0f 10 55 a8       	movsd  xmm2,QWORD PTR [rbp-0x58]
   140006aad:	f2 0f 10 45 08       	movsd  xmm0,QWORD PTR [rbp+0x8]
   140006ab2:	66 0f 28 c8          	movapd xmm1,xmm0
   140006ab6:	f2 0f 5c ca          	subsd  xmm1,xmm2
   140006aba:	f2 0f 10 45 a0       	movsd  xmm0,QWORD PTR [rbp-0x60]
   140006abf:	66 0f 2f c1          	comisd xmm0,xmm1
   140006ac3:	0f 87 c3 02 00 00    	ja     140006d8c <__gdtoa+0xb42>
   140006ac9:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006acc:	83 c0 01             	add    eax,0x1
   140006acf:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006ad2:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006ad5:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   140006ad8:	0f 8e 46 01 00 00    	jle    140006c24 <__gdtoa+0x9da>
   140006ade:	f2 0f 10 4d a0       	movsd  xmm1,QWORD PTR [rbp-0x60]
   140006ae3:	f2 0f 10 05 ad 48 00 	movsd  xmm0,QWORD PTR [rip+0x48ad]        # 14000b398 <.rdata+0x48>
   140006aea:	00 
   140006aeb:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006aef:	f2 0f 11 45 a0       	movsd  QWORD PTR [rbp-0x60],xmm0
   140006af4:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006af9:	f2 0f 10 05 97 48 00 	movsd  xmm0,QWORD PTR [rip+0x4897]        # 14000b398 <.rdata+0x48>
   140006b00:	00 
   140006b01:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006b05:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006b0a:	e9 1d ff ff ff       	jmp    140006a2c <__gdtoa+0x7e2>
   140006b0f:	f2 0f 10 4d a0       	movsd  xmm1,QWORD PTR [rbp-0x60]
   140006b14:	8b 45 6c             	mov    eax,DWORD PTR [rbp+0x6c]
   140006b17:	8d 50 ff             	lea    edx,[rax-0x1]
   140006b1a:	48 8b 05 5f 4b 00 00 	mov    rax,QWORD PTR [rip+0x4b5f]        # 14000b680 <.refptr.__tens_D2A>
   140006b21:	48 63 d2             	movsxd rdx,edx
   140006b24:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   140006b29:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006b2d:	f2 0f 11 45 a0       	movsd  QWORD PTR [rbp-0x60],xmm0
   140006b32:	c7 45 b0 01 00 00 00 	mov    DWORD PTR [rbp-0x50],0x1
   140006b39:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006b3e:	f2 0f 5e 45 08       	divsd  xmm0,QWORD PTR [rbp+0x8]
   140006b43:	f2 0f 2c c0          	cvttsd2si eax,xmm0
   140006b47:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   140006b4a:	83 7d d4 00          	cmp    DWORD PTR [rbp-0x2c],0x0
   140006b4e:	74 1c                	je     140006b6c <__gdtoa+0x922>
   140006b50:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006b55:	66 0f ef c9          	pxor   xmm1,xmm1
   140006b59:	f2 0f 2a 4d d4       	cvtsi2sd xmm1,DWORD PTR [rbp-0x2c]
   140006b5e:	f2 0f 59 4d 08       	mulsd  xmm1,QWORD PTR [rbp+0x8]
   140006b63:	f2 0f 5c c1          	subsd  xmm0,xmm1
   140006b67:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006b6c:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140006b6f:	8d 48 30             	lea    ecx,[rax+0x30]
   140006b72:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006b76:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140006b7a:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140006b7e:	89 ca                	mov    edx,ecx
   140006b80:	88 10                	mov    BYTE PTR [rax],dl
   140006b82:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006b85:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   140006b88:	75 73                	jne    140006bfd <__gdtoa+0x9b3>
   140006b8a:	f2 0f 10 4d 08       	movsd  xmm1,QWORD PTR [rbp+0x8]
   140006b8f:	f2 0f 10 05 29 48 00 	movsd  xmm0,QWORD PTR [rip+0x4829]        # 14000b3c0 <.rdata+0x70>
   140006b96:	00 
   140006b97:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006b9b:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   140006ba0:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006ba5:	f2 0f 10 4d a0       	movsd  xmm1,QWORD PTR [rbp-0x60]
   140006baa:	f2 0f 58 4d 08       	addsd  xmm1,QWORD PTR [rbp+0x8]
   140006baf:	66 0f 2f c1          	comisd xmm0,xmm1
   140006bb3:	0f 87 d6 01 00 00    	ja     140006d8f <__gdtoa+0xb45>
   140006bb9:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006bbe:	f2 0f 10 55 a0       	movsd  xmm2,QWORD PTR [rbp-0x60]
   140006bc3:	f2 0f 10 45 08       	movsd  xmm0,QWORD PTR [rbp+0x8]
   140006bc8:	f2 0f 5c c2          	subsd  xmm0,xmm2
   140006bcc:	66 0f 2f c1          	comisd xmm0,xmm1
   140006bd0:	77 02                	ja     140006bd4 <__gdtoa+0x98a>
   140006bd2:	eb 51                	jmp    140006c25 <__gdtoa+0x9db>
   140006bd4:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006bd9:	66 0f ef c9          	pxor   xmm1,xmm1
   140006bdd:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006be1:	7a 0e                	jp     140006bf1 <__gdtoa+0x9a7>
   140006be3:	66 0f ef c9          	pxor   xmm1,xmm1
   140006be7:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006beb:	0f 84 3e 0b 00 00    	je     14000772f <__gdtoa+0x14e5>
   140006bf1:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140006bf8:	e9 32 0b 00 00       	jmp    14000772f <__gdtoa+0x14e5>
   140006bfd:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006c00:	83 c0 01             	add    eax,0x1
   140006c03:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006c06:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006c0b:	f2 0f 10 05 85 47 00 	movsd  xmm0,QWORD PTR [rip+0x4785]        # 14000b398 <.rdata+0x48>
   140006c12:	00 
   140006c13:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006c17:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006c1c:	e9 18 ff ff ff       	jmp    140006b39 <__gdtoa+0x8ef>
   140006c21:	90                   	nop
   140006c22:	eb 01                	jmp    140006c25 <__gdtoa+0x9db>
   140006c24:	90                   	nop
   140006c25:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140006c29:	48 89 45 00          	mov    QWORD PTR [rbp+0x0],rax
   140006c2d:	f2 0f 10 45 e0       	movsd  xmm0,QWORD PTR [rbp-0x20]
   140006c32:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006c37:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   140006c3a:	89 45 58             	mov    DWORD PTR [rbp+0x58],eax
   140006c3d:	8b 45 d8             	mov    eax,DWORD PTR [rbp-0x28]
   140006c40:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   140006c43:	83 bd 98 00 00 00 00 	cmp    DWORD PTR [rbp+0x98],0x0
   140006c4a:	0f 88 bf 01 00 00    	js     140006e0f <__gdtoa+0xbc5>
   140006c50:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   140006c57:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140006c5a:	39 45 58             	cmp    DWORD PTR [rbp+0x58],eax
   140006c5d:	0f 8f ac 01 00 00    	jg     140006e0f <__gdtoa+0xbc5>
   140006c63:	48 8b 05 16 4a 00 00 	mov    rax,QWORD PTR [rip+0x4a16]        # 14000b680 <.refptr.__tens_D2A>
   140006c6a:	8b 55 58             	mov    edx,DWORD PTR [rbp+0x58]
   140006c6d:	48 63 d2             	movsxd rdx,edx
   140006c70:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   140006c75:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   140006c7a:	83 bd b8 00 00 00 00 	cmp    DWORD PTR [rbp+0xb8],0x0
   140006c81:	79 45                	jns    140006cc8 <__gdtoa+0xa7e>
   140006c83:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006c87:	7f 3f                	jg     140006cc8 <__gdtoa+0xa7e>
   140006c89:	48 c7 45 18 00 00 00 	mov    QWORD PTR [rbp+0x18],0x0
   140006c90:	00 
   140006c91:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140006c95:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140006c99:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006c9d:	0f 88 ac 04 00 00    	js     14000714f <__gdtoa+0xf05>
   140006ca3:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006ca8:	f2 0f 10 55 08       	movsd  xmm2,QWORD PTR [rbp+0x8]
   140006cad:	f2 0f 10 05 f3 46 00 	movsd  xmm0,QWORD PTR [rip+0x46f3]        # 14000b3a8 <.rdata+0x58>
   140006cb4:	00 
   140006cb5:	f2 0f 59 c2          	mulsd  xmm0,xmm2
   140006cb9:	66 0f 2f c1          	comisd xmm0,xmm1
   140006cbd:	0f 83 8c 04 00 00    	jae    14000714f <__gdtoa+0xf05>
   140006cc3:	e9 a6 04 00 00       	jmp    14000716e <__gdtoa+0xf24>
   140006cc8:	c7 45 b0 01 00 00 00 	mov    DWORD PTR [rbp-0x50],0x1
   140006ccf:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006cd4:	f2 0f 5e 45 08       	divsd  xmm0,QWORD PTR [rbp+0x8]
   140006cd9:	f2 0f 2c c0          	cvttsd2si eax,xmm0
   140006cdd:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   140006ce0:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006ce5:	66 0f ef c9          	pxor   xmm1,xmm1
   140006ce9:	f2 0f 2a 4d d4       	cvtsi2sd xmm1,DWORD PTR [rbp-0x2c]
   140006cee:	f2 0f 59 4d 08       	mulsd  xmm1,QWORD PTR [rbp+0x8]
   140006cf3:	f2 0f 5c c1          	subsd  xmm0,xmm1
   140006cf7:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006cfc:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140006cff:	8d 48 30             	lea    ecx,[rax+0x30]
   140006d02:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006d06:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140006d0a:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140006d0e:	89 ca                	mov    edx,ecx
   140006d10:	88 10                	mov    BYTE PTR [rax],dl
   140006d12:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006d17:	66 0f ef c9          	pxor   xmm1,xmm1
   140006d1b:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006d1f:	7a 0e                	jp     140006d2f <__gdtoa+0xae5>
   140006d21:	66 0f ef c9          	pxor   xmm1,xmm1
   140006d25:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006d29:	0f 84 da 00 00 00    	je     140006e09 <__gdtoa+0xbbf>
   140006d2f:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006d32:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   140006d35:	0f 85 aa 00 00 00    	jne    140006de5 <__gdtoa+0xb9b>
   140006d3b:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   140006d3f:	74 12                	je     140006d53 <__gdtoa+0xb09>
   140006d41:	83 7d 44 01          	cmp    DWORD PTR [rbp+0x44],0x1
   140006d45:	74 4b                	je     140006d92 <__gdtoa+0xb48>
   140006d47:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140006d4e:	e9 e0 09 00 00       	jmp    140007733 <__gdtoa+0x14e9>
   140006d53:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006d58:	f2 0f 58 c0          	addsd  xmm0,xmm0
   140006d5c:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006d61:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006d66:	66 0f 2f 45 08       	comisd xmm0,QWORD PTR [rbp+0x8]
   140006d6b:	77 28                	ja     140006d95 <__gdtoa+0xb4b>
   140006d6d:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006d72:	66 0f 2e 45 08       	ucomisd xmm0,QWORD PTR [rbp+0x8]
   140006d77:	7a 63                	jp     140006ddc <__gdtoa+0xb92>
   140006d79:	66 0f 2e 45 08       	ucomisd xmm0,QWORD PTR [rbp+0x8]
   140006d7e:	75 5c                	jne    140006ddc <__gdtoa+0xb92>
   140006d80:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140006d83:	83 e0 01             	and    eax,0x1
   140006d86:	85 c0                	test   eax,eax
   140006d88:	74 52                	je     140006ddc <__gdtoa+0xb92>
   140006d8a:	eb 09                	jmp    140006d95 <__gdtoa+0xb4b>
   140006d8c:	90                   	nop
   140006d8d:	eb 07                	jmp    140006d96 <__gdtoa+0xb4c>
   140006d8f:	90                   	nop
   140006d90:	eb 04                	jmp    140006d96 <__gdtoa+0xb4c>
   140006d92:	90                   	nop
   140006d93:	eb 01                	jmp    140006d96 <__gdtoa+0xb4c>
   140006d95:	90                   	nop
   140006d96:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   140006d9d:	eb 17                	jmp    140006db6 <__gdtoa+0xb6c>
   140006d9f:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006da3:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   140006da7:	75 0d                	jne    140006db6 <__gdtoa+0xb6c>
   140006da9:	83 45 58 01          	add    DWORD PTR [rbp+0x58],0x1
   140006dad:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006db1:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140006db4:	eb 10                	jmp    140006dc6 <__gdtoa+0xb7c>
   140006db6:	48 83 6d 00 01       	sub    QWORD PTR [rbp+0x0],0x1
   140006dbb:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006dbf:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140006dc2:	3c 39                	cmp    al,0x39
   140006dc4:	74 d9                	je     140006d9f <__gdtoa+0xb55>
   140006dc6:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006dca:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140006dce:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140006dd2:	0f b6 10             	movzx  edx,BYTE PTR [rax]
   140006dd5:	83 c2 01             	add    edx,0x1
   140006dd8:	88 10                	mov    BYTE PTR [rax],dl
   140006dda:	eb 2e                	jmp    140006e0a <__gdtoa+0xbc0>
   140006ddc:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140006de3:	eb 25                	jmp    140006e0a <__gdtoa+0xbc0>
   140006de5:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006de8:	83 c0 01             	add    eax,0x1
   140006deb:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006dee:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006df3:	f2 0f 10 05 9d 45 00 	movsd  xmm0,QWORD PTR [rip+0x459d]        # 14000b398 <.rdata+0x48>
   140006dfa:	00 
   140006dfb:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006dff:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006e04:	e9 c6 fe ff ff       	jmp    140006ccf <__gdtoa+0xa85>
   140006e09:	90                   	nop
   140006e0a:	e9 24 09 00 00       	jmp    140007733 <__gdtoa+0x14e9>
   140006e0f:	8b 45 7c             	mov    eax,DWORD PTR [rbp+0x7c]
   140006e12:	89 45 4c             	mov    DWORD PTR [rbp+0x4c],eax
   140006e15:	8b 45 78             	mov    eax,DWORD PTR [rbp+0x78]
   140006e18:	89 45 48             	mov    DWORD PTR [rbp+0x48],eax
   140006e1b:	48 c7 45 20 00 00 00 	mov    QWORD PTR [rbp+0x20],0x0
   140006e22:	00 
   140006e23:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140006e27:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140006e2b:	83 7d 50 00          	cmp    DWORD PTR [rbp+0x50],0x0
   140006e2f:	0f 84 e0 00 00 00    	je     140006f15 <__gdtoa+0xccb>
   140006e35:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
   140006e38:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140006e3b:	29 c2                	sub    edx,eax
   140006e3d:	89 55 b0             	mov    DWORD PTR [rbp-0x50],edx
   140006e40:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006e43:	8d 50 01             	lea    edx,[rax+0x1]
   140006e46:	89 55 b0             	mov    DWORD PTR [rbp-0x50],edx
   140006e49:	8b 95 98 00 00 00    	mov    edx,DWORD PTR [rbp+0x98]
   140006e4f:	29 c2                	sub    edx,eax
   140006e51:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   140006e58:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140006e5b:	39 c2                	cmp    edx,eax
   140006e5d:	7d 43                	jge    140006ea2 <__gdtoa+0xc58>
   140006e5f:	83 bd b0 00 00 00 03 	cmp    DWORD PTR [rbp+0xb0],0x3
   140006e66:	74 3a                	je     140006ea2 <__gdtoa+0xc58>
   140006e68:	83 bd b0 00 00 00 05 	cmp    DWORD PTR [rbp+0xb0],0x5
   140006e6f:	74 31                	je     140006ea2 <__gdtoa+0xc58>
   140006e71:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   140006e78:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140006e7b:	8b 95 98 00 00 00    	mov    edx,DWORD PTR [rbp+0x98]
   140006e81:	29 c2                	sub    edx,eax
   140006e83:	8d 42 01             	lea    eax,[rdx+0x1]
   140006e86:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006e89:	83 bd b0 00 00 00 01 	cmp    DWORD PTR [rbp+0xb0],0x1
   140006e90:	7e 68                	jle    140006efa <__gdtoa+0xcb0>
   140006e92:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006e96:	7e 62                	jle    140006efa <__gdtoa+0xcb0>
   140006e98:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006e9b:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   140006e9e:	7d 5a                	jge    140006efa <__gdtoa+0xcb0>
   140006ea0:	eb 0a                	jmp    140006eac <__gdtoa+0xc62>
   140006ea2:	83 bd b0 00 00 00 01 	cmp    DWORD PTR [rbp+0xb0],0x1
   140006ea9:	7e 50                	jle    140006efb <__gdtoa+0xcb1>
   140006eab:	90                   	nop
   140006eac:	8b 45 6c             	mov    eax,DWORD PTR [rbp+0x6c]
   140006eaf:	83 e8 01             	sub    eax,0x1
   140006eb2:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140006eb5:	8b 45 48             	mov    eax,DWORD PTR [rbp+0x48]
   140006eb8:	3b 45 60             	cmp    eax,DWORD PTR [rbp+0x60]
   140006ebb:	7c 08                	jl     140006ec5 <__gdtoa+0xc7b>
   140006ebd:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006ec0:	29 45 48             	sub    DWORD PTR [rbp+0x48],eax
   140006ec3:	eb 19                	jmp    140006ede <__gdtoa+0xc94>
   140006ec5:	8b 45 48             	mov    eax,DWORD PTR [rbp+0x48]
   140006ec8:	29 45 60             	sub    DWORD PTR [rbp+0x60],eax
   140006ecb:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006ece:	01 45 3c             	add    DWORD PTR [rbp+0x3c],eax
   140006ed1:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006ed4:	01 45 78             	add    DWORD PTR [rbp+0x78],eax
   140006ed7:	c7 45 48 00 00 00 00 	mov    DWORD PTR [rbp+0x48],0x0
   140006ede:	8b 45 6c             	mov    eax,DWORD PTR [rbp+0x6c]
   140006ee1:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006ee4:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006ee7:	85 c0                	test   eax,eax
   140006ee9:	79 10                	jns    140006efb <__gdtoa+0xcb1>
   140006eeb:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006eee:	29 45 4c             	sub    DWORD PTR [rbp+0x4c],eax
   140006ef1:	c7 45 b0 00 00 00 00 	mov    DWORD PTR [rbp-0x50],0x0
   140006ef8:	eb 01                	jmp    140006efb <__gdtoa+0xcb1>
   140006efa:	90                   	nop
   140006efb:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006efe:	01 45 7c             	add    DWORD PTR [rbp+0x7c],eax
   140006f01:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006f04:	01 45 40             	add    DWORD PTR [rbp+0x40],eax
   140006f07:	b9 01 00 00 00       	mov    ecx,0x1
   140006f0c:	e8 f6 0f 00 00       	call   140007f07 <__i2b_D2A>
   140006f11:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140006f15:	83 7d 4c 00          	cmp    DWORD PTR [rbp+0x4c],0x0
   140006f19:	7e 26                	jle    140006f41 <__gdtoa+0xcf7>
   140006f1b:	83 7d 40 00          	cmp    DWORD PTR [rbp+0x40],0x0
   140006f1f:	7e 20                	jle    140006f41 <__gdtoa+0xcf7>
   140006f21:	8b 55 40             	mov    edx,DWORD PTR [rbp+0x40]
   140006f24:	8b 45 4c             	mov    eax,DWORD PTR [rbp+0x4c]
   140006f27:	39 c2                	cmp    edx,eax
   140006f29:	0f 4e c2             	cmovle eax,edx
   140006f2c:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006f2f:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006f32:	29 45 7c             	sub    DWORD PTR [rbp+0x7c],eax
   140006f35:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006f38:	29 45 4c             	sub    DWORD PTR [rbp+0x4c],eax
   140006f3b:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006f3e:	29 45 40             	sub    DWORD PTR [rbp+0x40],eax
   140006f41:	83 7d 78 00          	cmp    DWORD PTR [rbp+0x78],0x0
   140006f45:	7e 7e                	jle    140006fc5 <__gdtoa+0xd7b>
   140006f47:	83 7d 50 00          	cmp    DWORD PTR [rbp+0x50],0x0
   140006f4b:	74 65                	je     140006fb2 <__gdtoa+0xd68>
   140006f4d:	83 7d 48 00          	cmp    DWORD PTR [rbp+0x48],0x0
   140006f51:	7e 3b                	jle    140006f8e <__gdtoa+0xd44>
   140006f53:	8b 55 48             	mov    edx,DWORD PTR [rbp+0x48]
   140006f56:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140006f5a:	48 89 c1             	mov    rcx,rax
   140006f5d:	e8 11 12 00 00       	call   140008173 <__pow5mult_D2A>
   140006f62:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140006f66:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140006f6a:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140006f6e:	48 89 c1             	mov    rcx,rax
   140006f71:	e8 d7 0f 00 00       	call   140007f4d <__mult_D2A>
   140006f76:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140006f7a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140006f7e:	48 89 c1             	mov    rcx,rax
   140006f81:	e8 c8 0d 00 00       	call   140007d4e <__Bfree_D2A>
   140006f86:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140006f8a:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140006f8e:	8b 45 78             	mov    eax,DWORD PTR [rbp+0x78]
   140006f91:	2b 45 48             	sub    eax,DWORD PTR [rbp+0x48]
   140006f94:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140006f97:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140006f9b:	74 28                	je     140006fc5 <__gdtoa+0xd7b>
   140006f9d:	8b 55 60             	mov    edx,DWORD PTR [rbp+0x60]
   140006fa0:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140006fa4:	48 89 c1             	mov    rcx,rax
   140006fa7:	e8 c7 11 00 00       	call   140008173 <__pow5mult_D2A>
   140006fac:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140006fb0:	eb 13                	jmp    140006fc5 <__gdtoa+0xd7b>
   140006fb2:	8b 55 78             	mov    edx,DWORD PTR [rbp+0x78]
   140006fb5:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140006fb9:	48 89 c1             	mov    rcx,rax
   140006fbc:	e8 b2 11 00 00       	call   140008173 <__pow5mult_D2A>
   140006fc1:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140006fc5:	b9 01 00 00 00       	mov    ecx,0x1
   140006fca:	e8 38 0f 00 00       	call   140007f07 <__i2b_D2A>
   140006fcf:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140006fd3:	83 7d 3c 00          	cmp    DWORD PTR [rbp+0x3c],0x0
   140006fd7:	7e 13                	jle    140006fec <__gdtoa+0xda2>
   140006fd9:	8b 55 3c             	mov    edx,DWORD PTR [rbp+0x3c]
   140006fdc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140006fe0:	48 89 c1             	mov    rcx,rax
   140006fe3:	e8 8b 11 00 00       	call   140008173 <__pow5mult_D2A>
   140006fe8:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140006fec:	c7 45 38 00 00 00 00 	mov    DWORD PTR [rbp+0x38],0x0
   140006ff3:	83 bd b0 00 00 00 01 	cmp    DWORD PTR [rbp+0xb0],0x1
   140006ffa:	7f 29                	jg     140007025 <__gdtoa+0xddb>
   140006ffc:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
   140006fff:	83 f8 01             	cmp    eax,0x1
   140007002:	75 21                	jne    140007025 <__gdtoa+0xddb>
   140007004:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   14000700b:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000700e:	83 c0 01             	add    eax,0x1
   140007011:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140007014:	7e 0f                	jle    140007025 <__gdtoa+0xddb>
   140007016:	83 45 7c 01          	add    DWORD PTR [rbp+0x7c],0x1
   14000701a:	83 45 40 01          	add    DWORD PTR [rbp+0x40],0x1
   14000701e:	c7 45 38 01 00 00 00 	mov    DWORD PTR [rbp+0x38],0x1
   140007025:	83 7d 3c 00          	cmp    DWORD PTR [rbp+0x3c],0x0
   140007029:	74 22                	je     14000704d <__gdtoa+0xe03>
   14000702b:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000702f:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007032:	8d 50 ff             	lea    edx,[rax-0x1]
   140007035:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007039:	48 63 d2             	movsxd rdx,edx
   14000703c:	48 83 c2 04          	add    rdx,0x4
   140007040:	8b 44 90 08          	mov    eax,DWORD PTR [rax+rdx*4+0x8]
   140007044:	89 c1                	mov    ecx,eax
   140007046:	e8 c5 f0 ff ff       	call   140006110 <__hi0bits_D2A>
   14000704b:	eb 05                	jmp    140007052 <__gdtoa+0xe08>
   14000704d:	b8 1f 00 00 00       	mov    eax,0x1f
   140007052:	2b 45 40             	sub    eax,DWORD PTR [rbp+0x40]
   140007055:	83 e8 04             	sub    eax,0x4
   140007058:	83 e0 1f             	and    eax,0x1f
   14000705b:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   14000705e:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140007061:	01 45 4c             	add    DWORD PTR [rbp+0x4c],eax
   140007064:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140007067:	01 45 7c             	add    DWORD PTR [rbp+0x7c],eax
   14000706a:	83 7d 7c 00          	cmp    DWORD PTR [rbp+0x7c],0x0
   14000706e:	7e 13                	jle    140007083 <__gdtoa+0xe39>
   140007070:	8b 55 7c             	mov    edx,DWORD PTR [rbp+0x7c]
   140007073:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007077:	48 89 c1             	mov    rcx,rax
   14000707a:	e8 b1 12 00 00       	call   140008330 <__lshift_D2A>
   14000707f:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140007083:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140007086:	01 45 40             	add    DWORD PTR [rbp+0x40],eax
   140007089:	83 7d 40 00          	cmp    DWORD PTR [rbp+0x40],0x0
   14000708d:	7e 13                	jle    1400070a2 <__gdtoa+0xe58>
   14000708f:	8b 55 40             	mov    edx,DWORD PTR [rbp+0x40]
   140007092:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007096:	48 89 c1             	mov    rcx,rax
   140007099:	e8 92 12 00 00       	call   140008330 <__lshift_D2A>
   14000709e:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   1400070a2:	83 7d 54 00          	cmp    DWORD PTR [rbp+0x54],0x0
   1400070a6:	74 5a                	je     140007102 <__gdtoa+0xeb8>
   1400070a8:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   1400070ac:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400070b0:	48 89 c1             	mov    rcx,rax
   1400070b3:	e8 05 14 00 00       	call   1400084bd <__cmp_D2A>
   1400070b8:	85 c0                	test   eax,eax
   1400070ba:	79 46                	jns    140007102 <__gdtoa+0xeb8>
   1400070bc:	83 6d 58 01          	sub    DWORD PTR [rbp+0x58],0x1
   1400070c0:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400070c4:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400070ca:	ba 0a 00 00 00       	mov    edx,0xa
   1400070cf:	48 89 c1             	mov    rcx,rax
   1400070d2:	e8 02 0d 00 00       	call   140007dd9 <__multadd_D2A>
   1400070d7:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   1400070db:	83 7d 50 00          	cmp    DWORD PTR [rbp+0x50],0x0
   1400070df:	74 1b                	je     1400070fc <__gdtoa+0xeb2>
   1400070e1:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400070e5:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400070eb:	ba 0a 00 00 00       	mov    edx,0xa
   1400070f0:	48 89 c1             	mov    rcx,rax
   1400070f3:	e8 e1 0c 00 00       	call   140007dd9 <__multadd_D2A>
   1400070f8:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   1400070fc:	8b 45 68             	mov    eax,DWORD PTR [rbp+0x68]
   1400070ff:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   140007102:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140007106:	0f 8f 81 00 00 00    	jg     14000718d <__gdtoa+0xf43>
   14000710c:	83 bd b0 00 00 00 02 	cmp    DWORD PTR [rbp+0xb0],0x2
   140007113:	7e 78                	jle    14000718d <__gdtoa+0xf43>
   140007115:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140007119:	78 37                	js     140007152 <__gdtoa+0xf08>
   14000711b:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000711f:	41 b8 00 00 00 00    	mov    r8d,0x0
   140007125:	ba 05 00 00 00       	mov    edx,0x5
   14000712a:	48 89 c1             	mov    rcx,rax
   14000712d:	e8 a7 0c 00 00       	call   140007dd9 <__multadd_D2A>
   140007132:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140007136:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   14000713a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000713e:	48 89 c1             	mov    rcx,rax
   140007141:	e8 77 13 00 00       	call   1400084bd <__cmp_D2A>
   140007146:	85 c0                	test   eax,eax
   140007148:	7f 23                	jg     14000716d <__gdtoa+0xf23>
   14000714a:	eb 06                	jmp    140007152 <__gdtoa+0xf08>
   14000714c:	90                   	nop
   14000714d:	eb 04                	jmp    140007153 <__gdtoa+0xf09>
   14000714f:	90                   	nop
   140007150:	eb 01                	jmp    140007153 <__gdtoa+0xf09>
   140007152:	90                   	nop
   140007153:	8b 85 b8 00 00 00    	mov    eax,DWORD PTR [rbp+0xb8]
   140007159:	f7 d0                	not    eax
   14000715b:	89 45 58             	mov    DWORD PTR [rbp+0x58],eax
   14000715e:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140007165:	e9 84 05 00 00       	jmp    1400076ee <__gdtoa+0x14a4>
   14000716a:	90                   	nop
   14000716b:	eb 01                	jmp    14000716e <__gdtoa+0xf24>
   14000716d:	90                   	nop
   14000716e:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   140007175:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007179:	48 8d 50 01          	lea    rdx,[rax+0x1]
   14000717d:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140007181:	c6 00 31             	mov    BYTE PTR [rax],0x31
   140007184:	83 45 58 01          	add    DWORD PTR [rbp+0x58],0x1
   140007188:	e9 61 05 00 00       	jmp    1400076ee <__gdtoa+0x14a4>
   14000718d:	83 7d 50 00          	cmp    DWORD PTR [rbp+0x50],0x0
   140007191:	0f 84 14 04 00 00    	je     1400075ab <__gdtoa+0x1361>
   140007197:	83 7d 4c 00          	cmp    DWORD PTR [rbp+0x4c],0x0
   14000719b:	7e 13                	jle    1400071b0 <__gdtoa+0xf66>
   14000719d:	8b 55 4c             	mov    edx,DWORD PTR [rbp+0x4c]
   1400071a0:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400071a4:	48 89 c1             	mov    rcx,rax
   1400071a7:	e8 84 11 00 00       	call   140008330 <__lshift_D2A>
   1400071ac:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   1400071b0:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400071b4:	48 89 45 20          	mov    QWORD PTR [rbp+0x20],rax
   1400071b8:	83 7d 38 00          	cmp    DWORD PTR [rbp+0x38],0x0
   1400071bc:	74 57                	je     140007215 <__gdtoa+0xfcb>
   1400071be:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400071c2:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400071c5:	89 c1                	mov    ecx,eax
   1400071c7:	e8 41 0a 00 00       	call   140007c0d <__Balloc_D2A>
   1400071cc:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   1400071d0:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400071d4:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400071d7:	48 98                	cdqe
   1400071d9:	48 83 c0 02          	add    rax,0x2
   1400071dd:	48 8d 0c 85 00 00 00 	lea    rcx,[rax*4+0x0]
   1400071e4:	00 
   1400071e5:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400071e9:	48 8d 50 10          	lea    rdx,[rax+0x10]
   1400071ed:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400071f1:	48 83 c0 10          	add    rax,0x10
   1400071f5:	49 89 c8             	mov    r8,rcx
   1400071f8:	48 89 c1             	mov    rcx,rax
   1400071fb:	e8 e8 23 00 00       	call   1400095e8 <memcpy>
   140007200:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007204:	ba 01 00 00 00       	mov    edx,0x1
   140007209:	48 89 c1             	mov    rcx,rax
   14000720c:	e8 1f 11 00 00       	call   140008330 <__lshift_D2A>
   140007211:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140007215:	c7 45 b0 01 00 00 00 	mov    DWORD PTR [rbp-0x50],0x1
   14000721c:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140007220:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007224:	48 89 c1             	mov    rcx,rax
   140007227:	e8 62 ec ff ff       	call   140005e8e <__quorem_D2A>
   14000722c:	83 c0 30             	add    eax,0x30
   14000722f:	89 45 74             	mov    DWORD PTR [rbp+0x74],eax
   140007232:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   140007236:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000723a:	48 89 c1             	mov    rcx,rax
   14000723d:	e8 7b 12 00 00       	call   1400084bd <__cmp_D2A>
   140007242:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140007245:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140007249:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000724d:	48 89 c1             	mov    rcx,rax
   140007250:	e8 38 13 00 00       	call   14000858d <__diff_D2A>
   140007255:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   140007259:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   14000725d:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140007260:	85 c0                	test   eax,eax
   140007262:	75 15                	jne    140007279 <__gdtoa+0x102f>
   140007264:	48 8b 55 c0          	mov    rdx,QWORD PTR [rbp-0x40]
   140007268:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000726c:	48 89 c1             	mov    rcx,rax
   14000726f:	e8 49 12 00 00       	call   1400084bd <__cmp_D2A>
   140007274:	89 45 5c             	mov    DWORD PTR [rbp+0x5c],eax
   140007277:	eb 07                	jmp    140007280 <__gdtoa+0x1036>
   140007279:	c7 45 5c 01 00 00 00 	mov    DWORD PTR [rbp+0x5c],0x1
   140007280:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140007284:	48 89 c1             	mov    rcx,rax
   140007287:	e8 c2 0a 00 00       	call   140007d4e <__Bfree_D2A>
   14000728c:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   140007290:	75 70                	jne    140007302 <__gdtoa+0x10b8>
   140007292:	83 bd b0 00 00 00 00 	cmp    DWORD PTR [rbp+0xb0],0x0
   140007299:	75 67                	jne    140007302 <__gdtoa+0x10b8>
   14000729b:	48 8b 85 a0 00 00 00 	mov    rax,QWORD PTR [rbp+0xa0]
   1400072a2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400072a4:	83 e0 01             	and    eax,0x1
   1400072a7:	85 c0                	test   eax,eax
   1400072a9:	75 57                	jne    140007302 <__gdtoa+0x10b8>
   1400072ab:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   1400072af:	75 51                	jne    140007302 <__gdtoa+0x10b8>
   1400072b1:	83 7d 74 39          	cmp    DWORD PTR [rbp+0x74],0x39
   1400072b5:	0f 84 01 02 00 00    	je     1400074bc <__gdtoa+0x1272>
   1400072bb:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   1400072bf:	7f 20                	jg     1400072e1 <__gdtoa+0x1097>
   1400072c1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400072c5:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400072c8:	83 f8 01             	cmp    eax,0x1
   1400072cb:	7f 0b                	jg     1400072d8 <__gdtoa+0x108e>
   1400072cd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400072d1:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   1400072d4:	85 c0                	test   eax,eax
   1400072d6:	74 14                	je     1400072ec <__gdtoa+0x10a2>
   1400072d8:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   1400072df:	eb 0b                	jmp    1400072ec <__gdtoa+0x10a2>
   1400072e1:	83 45 74 01          	add    DWORD PTR [rbp+0x74],0x1
   1400072e5:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   1400072ec:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400072f0:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400072f4:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   1400072f8:	8b 55 74             	mov    edx,DWORD PTR [rbp+0x74]
   1400072fb:	88 10                	mov    BYTE PTR [rax],dl
   1400072fd:	e9 ec 03 00 00       	jmp    1400076ee <__gdtoa+0x14a4>
   140007302:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140007306:	78 2b                	js     140007333 <__gdtoa+0x10e9>
   140007308:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   14000730c:	0f 85 96 01 00 00    	jne    1400074a8 <__gdtoa+0x125e>
   140007312:	83 bd b0 00 00 00 00 	cmp    DWORD PTR [rbp+0xb0],0x0
   140007319:	0f 85 89 01 00 00    	jne    1400074a8 <__gdtoa+0x125e>
   14000731f:	48 8b 85 a0 00 00 00 	mov    rax,QWORD PTR [rbp+0xa0]
   140007326:	8b 00                	mov    eax,DWORD PTR [rax]
   140007328:	83 e0 01             	and    eax,0x1
   14000732b:	85 c0                	test   eax,eax
   14000732d:	0f 85 75 01 00 00    	jne    1400074a8 <__gdtoa+0x125e>
   140007333:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   140007337:	0f 84 db 00 00 00    	je     140007418 <__gdtoa+0x11ce>
   14000733d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007341:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007344:	83 f8 01             	cmp    eax,0x1
   140007347:	7f 0f                	jg     140007358 <__gdtoa+0x110e>
   140007349:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000734d:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   140007350:	85 c0                	test   eax,eax
   140007352:	0f 84 c0 00 00 00    	je     140007418 <__gdtoa+0x11ce>
   140007358:	83 7d 44 02          	cmp    DWORD PTR [rbp+0x44],0x2
   14000735c:	0f 85 83 00 00 00    	jne    1400073e5 <__gdtoa+0x119b>
   140007362:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140007369:	e9 24 01 00 00       	jmp    140007492 <__gdtoa+0x1248>
   14000736e:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007372:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140007376:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   14000737a:	8b 55 74             	mov    edx,DWORD PTR [rbp+0x74]
   14000737d:	88 10                	mov    BYTE PTR [rax],dl
   14000737f:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007383:	41 b8 00 00 00 00    	mov    r8d,0x0
   140007389:	ba 0a 00 00 00       	mov    edx,0xa
   14000738e:	48 89 c1             	mov    rcx,rax
   140007391:	e8 43 0a 00 00       	call   140007dd9 <__multadd_D2A>
   140007396:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000739a:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000739e:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   1400073a2:	75 08                	jne    1400073ac <__gdtoa+0x1162>
   1400073a4:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400073a8:	48 89 45 20          	mov    QWORD PTR [rbp+0x20],rax
   1400073ac:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400073b0:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   1400073b4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400073b8:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400073be:	ba 0a 00 00 00       	mov    edx,0xa
   1400073c3:	48 89 c1             	mov    rcx,rax
   1400073c6:	e8 0e 0a 00 00       	call   140007dd9 <__multadd_D2A>
   1400073cb:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   1400073cf:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   1400073d3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400073d7:	48 89 c1             	mov    rcx,rax
   1400073da:	e8 af ea ff ff       	call   140005e8e <__quorem_D2A>
   1400073df:	83 c0 30             	add    eax,0x30
   1400073e2:	89 45 74             	mov    DWORD PTR [rbp+0x74],eax
   1400073e5:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400073e9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400073ed:	48 89 c1             	mov    rcx,rax
   1400073f0:	e8 c8 10 00 00       	call   1400084bd <__cmp_D2A>
   1400073f5:	85 c0                	test   eax,eax
   1400073f7:	0f 8f 71 ff ff ff    	jg     14000736e <__gdtoa+0x1124>
   1400073fd:	8b 45 74             	mov    eax,DWORD PTR [rbp+0x74]
   140007400:	8d 50 01             	lea    edx,[rax+0x1]
   140007403:	89 55 74             	mov    DWORD PTR [rbp+0x74],edx
   140007406:	83 f8 39             	cmp    eax,0x39
   140007409:	0f 84 b0 00 00 00    	je     1400074bf <__gdtoa+0x1275>
   14000740f:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   140007416:	eb 7a                	jmp    140007492 <__gdtoa+0x1248>
   140007418:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   14000741c:	7e 53                	jle    140007471 <__gdtoa+0x1227>
   14000741e:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007422:	ba 01 00 00 00       	mov    edx,0x1
   140007427:	48 89 c1             	mov    rcx,rax
   14000742a:	e8 01 0f 00 00       	call   140008330 <__lshift_D2A>
   14000742f:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140007433:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140007437:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000743b:	48 89 c1             	mov    rcx,rax
   14000743e:	e8 7a 10 00 00       	call   1400084bd <__cmp_D2A>
   140007443:	89 45 5c             	mov    DWORD PTR [rbp+0x5c],eax
   140007446:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   14000744a:	7f 10                	jg     14000745c <__gdtoa+0x1212>
   14000744c:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   140007450:	75 18                	jne    14000746a <__gdtoa+0x1220>
   140007452:	8b 45 74             	mov    eax,DWORD PTR [rbp+0x74]
   140007455:	83 e0 01             	and    eax,0x1
   140007458:	85 c0                	test   eax,eax
   14000745a:	74 0e                	je     14000746a <__gdtoa+0x1220>
   14000745c:	8b 45 74             	mov    eax,DWORD PTR [rbp+0x74]
   14000745f:	8d 50 01             	lea    edx,[rax+0x1]
   140007462:	89 55 74             	mov    DWORD PTR [rbp+0x74],edx
   140007465:	83 f8 39             	cmp    eax,0x39
   140007468:	74 58                	je     1400074c2 <__gdtoa+0x1278>
   14000746a:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   140007471:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007475:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007478:	83 f8 01             	cmp    eax,0x1
   14000747b:	7f 0b                	jg     140007488 <__gdtoa+0x123e>
   14000747d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007481:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   140007484:	85 c0                	test   eax,eax
   140007486:	74 09                	je     140007491 <__gdtoa+0x1247>
   140007488:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   14000748f:	eb 01                	jmp    140007492 <__gdtoa+0x1248>
   140007491:	90                   	nop
   140007492:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007496:	48 8d 50 01          	lea    rdx,[rax+0x1]
   14000749a:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   14000749e:	8b 55 74             	mov    edx,DWORD PTR [rbp+0x74]
   1400074a1:	88 10                	mov    BYTE PTR [rax],dl
   1400074a3:	e9 46 02 00 00       	jmp    1400076ee <__gdtoa+0x14a4>
   1400074a8:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   1400074ac:	7e 52                	jle    140007500 <__gdtoa+0x12b6>
   1400074ae:	83 7d 44 02          	cmp    DWORD PTR [rbp+0x44],0x2
   1400074b2:	74 4c                	je     140007500 <__gdtoa+0x12b6>
   1400074b4:	83 7d 74 39          	cmp    DWORD PTR [rbp+0x74],0x39
   1400074b8:	75 24                	jne    1400074de <__gdtoa+0x1294>
   1400074ba:	eb 07                	jmp    1400074c3 <__gdtoa+0x1279>
   1400074bc:	90                   	nop
   1400074bd:	eb 04                	jmp    1400074c3 <__gdtoa+0x1279>
   1400074bf:	90                   	nop
   1400074c0:	eb 01                	jmp    1400074c3 <__gdtoa+0x1279>
   1400074c2:	90                   	nop
   1400074c3:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400074c7:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400074cb:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   1400074cf:	c6 00 39             	mov    BYTE PTR [rax],0x39
   1400074d2:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   1400074d9:	e9 9d 01 00 00       	jmp    14000767b <__gdtoa+0x1431>
   1400074de:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   1400074e5:	8b 45 74             	mov    eax,DWORD PTR [rbp+0x74]
   1400074e8:	8d 48 01             	lea    ecx,[rax+0x1]
   1400074eb:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400074ef:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400074f3:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   1400074f7:	89 ca                	mov    edx,ecx
   1400074f9:	88 10                	mov    BYTE PTR [rax],dl
   1400074fb:	e9 ee 01 00 00       	jmp    1400076ee <__gdtoa+0x14a4>
   140007500:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007504:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140007508:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   14000750c:	8b 55 74             	mov    edx,DWORD PTR [rbp+0x74]
   14000750f:	88 10                	mov    BYTE PTR [rax],dl
   140007511:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140007514:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   140007517:	0f 84 ea 00 00 00    	je     140007607 <__gdtoa+0x13bd>
   14000751d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007521:	41 b8 00 00 00 00    	mov    r8d,0x0
   140007527:	ba 0a 00 00 00       	mov    edx,0xa
   14000752c:	48 89 c1             	mov    rcx,rax
   14000752f:	e8 a5 08 00 00       	call   140007dd9 <__multadd_D2A>
   140007534:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140007538:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000753c:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140007540:	75 25                	jne    140007567 <__gdtoa+0x131d>
   140007542:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007546:	41 b8 00 00 00 00    	mov    r8d,0x0
   14000754c:	ba 0a 00 00 00       	mov    edx,0xa
   140007551:	48 89 c1             	mov    rcx,rax
   140007554:	e8 80 08 00 00       	call   140007dd9 <__multadd_D2A>
   140007559:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   14000755d:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007561:	48 89 45 20          	mov    QWORD PTR [rbp+0x20],rax
   140007565:	eb 36                	jmp    14000759d <__gdtoa+0x1353>
   140007567:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000756b:	41 b8 00 00 00 00    	mov    r8d,0x0
   140007571:	ba 0a 00 00 00       	mov    edx,0xa
   140007576:	48 89 c1             	mov    rcx,rax
   140007579:	e8 5b 08 00 00       	call   140007dd9 <__multadd_D2A>
   14000757e:	48 89 45 20          	mov    QWORD PTR [rbp+0x20],rax
   140007582:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007586:	41 b8 00 00 00 00    	mov    r8d,0x0
   14000758c:	ba 0a 00 00 00       	mov    edx,0xa
   140007591:	48 89 c1             	mov    rcx,rax
   140007594:	e8 40 08 00 00       	call   140007dd9 <__multadd_D2A>
   140007599:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   14000759d:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400075a0:	83 c0 01             	add    eax,0x1
   1400075a3:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   1400075a6:	e9 71 fc ff ff       	jmp    14000721c <__gdtoa+0xfd2>
   1400075ab:	c7 45 b0 01 00 00 00 	mov    DWORD PTR [rbp-0x50],0x1
   1400075b2:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   1400075b6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400075ba:	48 89 c1             	mov    rcx,rax
   1400075bd:	e8 cc e8 ff ff       	call   140005e8e <__quorem_D2A>
   1400075c2:	83 c0 30             	add    eax,0x30
   1400075c5:	89 45 74             	mov    DWORD PTR [rbp+0x74],eax
   1400075c8:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400075cc:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400075d0:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   1400075d4:	8b 55 74             	mov    edx,DWORD PTR [rbp+0x74]
   1400075d7:	88 10                	mov    BYTE PTR [rax],dl
   1400075d9:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400075dc:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   1400075df:	7e 29                	jle    14000760a <__gdtoa+0x13c0>
   1400075e1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400075e5:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400075eb:	ba 0a 00 00 00       	mov    edx,0xa
   1400075f0:	48 89 c1             	mov    rcx,rax
   1400075f3:	e8 e1 07 00 00       	call   140007dd9 <__multadd_D2A>
   1400075f8:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   1400075fc:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400075ff:	83 c0 01             	add    eax,0x1
   140007602:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140007605:	eb ab                	jmp    1400075b2 <__gdtoa+0x1368>
   140007607:	90                   	nop
   140007608:	eb 01                	jmp    14000760b <__gdtoa+0x13c1>
   14000760a:	90                   	nop
   14000760b:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   14000760f:	74 26                	je     140007637 <__gdtoa+0x13ed>
   140007611:	83 7d 44 02          	cmp    DWORD PTR [rbp+0x44],0x2
   140007615:	0f 84 ae 00 00 00    	je     1400076c9 <__gdtoa+0x147f>
   14000761b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000761f:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007622:	83 f8 01             	cmp    eax,0x1
   140007625:	7f 50                	jg     140007677 <__gdtoa+0x142d>
   140007627:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000762b:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   14000762e:	85 c0                	test   eax,eax
   140007630:	75 45                	jne    140007677 <__gdtoa+0x142d>
   140007632:	e9 92 00 00 00       	jmp    1400076c9 <__gdtoa+0x147f>
   140007637:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000763b:	ba 01 00 00 00       	mov    edx,0x1
   140007640:	48 89 c1             	mov    rcx,rax
   140007643:	e8 e8 0c 00 00       	call   140008330 <__lshift_D2A>
   140007648:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   14000764c:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140007650:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007654:	48 89 c1             	mov    rcx,rax
   140007657:	e8 61 0e 00 00       	call   1400084bd <__cmp_D2A>
   14000765c:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   14000765f:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140007663:	7f 15                	jg     14000767a <__gdtoa+0x1430>
   140007665:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140007669:	75 61                	jne    1400076cc <__gdtoa+0x1482>
   14000766b:	8b 45 74             	mov    eax,DWORD PTR [rbp+0x74]
   14000766e:	83 e0 01             	and    eax,0x1
   140007671:	85 c0                	test   eax,eax
   140007673:	74 57                	je     1400076cc <__gdtoa+0x1482>
   140007675:	eb 03                	jmp    14000767a <__gdtoa+0x1430>
   140007677:	90                   	nop
   140007678:	eb 01                	jmp    14000767b <__gdtoa+0x1431>
   14000767a:	90                   	nop
   14000767b:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   140007682:	eb 1f                	jmp    1400076a3 <__gdtoa+0x1459>
   140007684:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007688:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   14000768c:	75 15                	jne    1400076a3 <__gdtoa+0x1459>
   14000768e:	83 45 58 01          	add    DWORD PTR [rbp+0x58],0x1
   140007692:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007696:	48 8d 50 01          	lea    rdx,[rax+0x1]
   14000769a:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   14000769e:	c6 00 31             	mov    BYTE PTR [rax],0x31
   1400076a1:	eb 4b                	jmp    1400076ee <__gdtoa+0x14a4>
   1400076a3:	48 83 6d 00 01       	sub    QWORD PTR [rbp+0x0],0x1
   1400076a8:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400076ac:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400076af:	3c 39                	cmp    al,0x39
   1400076b1:	74 d1                	je     140007684 <__gdtoa+0x143a>
   1400076b3:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400076b7:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400076bb:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   1400076bf:	0f b6 10             	movzx  edx,BYTE PTR [rax]
   1400076c2:	83 c2 01             	add    edx,0x1
   1400076c5:	88 10                	mov    BYTE PTR [rax],dl
   1400076c7:	eb 25                	jmp    1400076ee <__gdtoa+0x14a4>
   1400076c9:	90                   	nop
   1400076ca:	eb 01                	jmp    1400076cd <__gdtoa+0x1483>
   1400076cc:	90                   	nop
   1400076cd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400076d1:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400076d4:	83 f8 01             	cmp    eax,0x1
   1400076d7:	7f 0b                	jg     1400076e4 <__gdtoa+0x149a>
   1400076d9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400076dd:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   1400076e0:	85 c0                	test   eax,eax
   1400076e2:	74 09                	je     1400076ed <__gdtoa+0x14a3>
   1400076e4:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   1400076eb:	eb 01                	jmp    1400076ee <__gdtoa+0x14a4>
   1400076ed:	90                   	nop
   1400076ee:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400076f2:	48 89 c1             	mov    rcx,rax
   1400076f5:	e8 54 06 00 00       	call   140007d4e <__Bfree_D2A>
   1400076fa:	48 83 7d 18 00       	cmp    QWORD PTR [rbp+0x18],0x0
   1400076ff:	74 31                	je     140007732 <__gdtoa+0x14e8>
   140007701:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140007706:	74 16                	je     14000771e <__gdtoa+0x14d4>
   140007708:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000770c:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140007710:	74 0c                	je     14000771e <__gdtoa+0x14d4>
   140007712:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140007716:	48 89 c1             	mov    rcx,rax
   140007719:	e8 30 06 00 00       	call   140007d4e <__Bfree_D2A>
   14000771e:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007722:	48 89 c1             	mov    rcx,rax
   140007725:	e8 24 06 00 00       	call   140007d4e <__Bfree_D2A>
   14000772a:	eb 0e                	jmp    14000773a <__gdtoa+0x14f0>
   14000772c:	90                   	nop
   14000772d:	eb 0b                	jmp    14000773a <__gdtoa+0x14f0>
   14000772f:	90                   	nop
   140007730:	eb 08                	jmp    14000773a <__gdtoa+0x14f0>
   140007732:	90                   	nop
   140007733:	eb 05                	jmp    14000773a <__gdtoa+0x14f0>
   140007735:	48 83 6d 00 01       	sub    QWORD PTR [rbp+0x0],0x1
   14000773a:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   14000773e:	48 39 45 e8          	cmp    QWORD PTR [rbp-0x18],rax
   140007742:	73 0f                	jae    140007753 <__gdtoa+0x1509>
   140007744:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007748:	48 83 e8 01          	sub    rax,0x1
   14000774c:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   14000774f:	3c 30                	cmp    al,0x30
   140007751:	74 e2                	je     140007735 <__gdtoa+0x14eb>
   140007753:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007757:	48 89 c1             	mov    rcx,rax
   14000775a:	e8 ef 05 00 00       	call   140007d4e <__Bfree_D2A>
   14000775f:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007763:	c6 00 00             	mov    BYTE PTR [rax],0x0
   140007766:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   140007769:	8d 50 01             	lea    edx,[rax+0x1]
   14000776c:	48 8b 85 c0 00 00 00 	mov    rax,QWORD PTR [rbp+0xc0]
   140007773:	89 10                	mov    DWORD PTR [rax],edx
   140007775:	48 83 bd c8 00 00 00 	cmp    QWORD PTR [rbp+0xc8],0x0
   14000777c:	00 
   14000777d:	74 0e                	je     14000778d <__gdtoa+0x1543>
   14000777f:	48 8b 85 c8 00 00 00 	mov    rax,QWORD PTR [rbp+0xc8]
   140007786:	48 8b 55 00          	mov    rdx,QWORD PTR [rbp+0x0]
   14000778a:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000778d:	48 8b 85 a8 00 00 00 	mov    rax,QWORD PTR [rbp+0xa8]
   140007794:	8b 00                	mov    eax,DWORD PTR [rax]
   140007796:	0b 45 64             	or     eax,DWORD PTR [rbp+0x64]
   140007799:	89 c2                	mov    edx,eax
   14000779b:	48 8b 85 a8 00 00 00 	mov    rax,QWORD PTR [rbp+0xa8]
   1400077a2:	89 10                	mov    DWORD PTR [rax],edx
   1400077a4:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400077a8:	48 81 c4 00 01 00 00 	add    rsp,0x100
   1400077af:	5d                   	pop    rbp
   1400077b0:	c3                   	ret
   1400077b1:	90                   	nop
   1400077b2:	90                   	nop
   1400077b3:	90                   	nop
   1400077b4:	90                   	nop
   1400077b5:	90                   	nop
   1400077b6:	90                   	nop
   1400077b7:	90                   	nop
   1400077b8:	90                   	nop
   1400077b9:	90                   	nop
   1400077ba:	90                   	nop
   1400077bb:	90                   	nop
   1400077bc:	90                   	nop
   1400077bd:	90                   	nop
   1400077be:	90                   	nop
   1400077bf:	90                   	nop

00000001400077c0 <__lo0bits_D2A>:
   1400077c0:	55                   	push   rbp
   1400077c1:	48 89 e5             	mov    rbp,rsp
   1400077c4:	48 83 ec 10          	sub    rsp,0x10
   1400077c8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400077cc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400077d0:	8b 00                	mov    eax,DWORD PTR [rax]
   1400077d2:	f3 0f bc c0          	tzcnt  eax,eax
   1400077d6:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400077d9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400077dd:	8b 10                	mov    edx,DWORD PTR [rax]
   1400077df:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400077e2:	89 c1                	mov    ecx,eax
   1400077e4:	d3 ea                	shr    edx,cl
   1400077e6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400077ea:	89 10                	mov    DWORD PTR [rax],edx
   1400077ec:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400077ef:	48 83 c4 10          	add    rsp,0x10
   1400077f3:	5d                   	pop    rbp
   1400077f4:	c3                   	ret

00000001400077f5 <__rshift_D2A>:
   1400077f5:	55                   	push   rbp
   1400077f6:	48 89 e5             	mov    rbp,rsp
   1400077f9:	48 83 ec 20          	sub    rsp,0x20
   1400077fd:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140007801:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140007804:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007808:	48 83 c0 18          	add    rax,0x18
   14000780c:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140007810:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007814:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007818:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   14000781b:	c1 f8 05             	sar    eax,0x5
   14000781e:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140007821:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007825:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007828:	39 45 e8             	cmp    DWORD PTR [rbp-0x18],eax
   14000782b:	0f 8d e4 00 00 00    	jge    140007915 <__rshift_D2A+0x120>
   140007831:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007835:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007838:	48 98                	cdqe
   14000783a:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140007841:	00 
   140007842:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007846:	48 01 d0             	add    rax,rdx
   140007849:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000784d:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140007850:	48 98                	cdqe
   140007852:	48 c1 e0 02          	shl    rax,0x2
   140007856:	48 01 45 f8          	add    QWORD PTR [rbp-0x8],rax
   14000785a:	83 65 18 1f          	and    DWORD PTR [rbp+0x18],0x1f
   14000785e:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140007862:	0f 84 a3 00 00 00    	je     14000790b <__rshift_D2A+0x116>
   140007868:	b8 20 00 00 00       	mov    eax,0x20
   14000786d:	2b 45 18             	sub    eax,DWORD PTR [rbp+0x18]
   140007870:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140007873:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007877:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000787b:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   14000787f:	8b 10                	mov    edx,DWORD PTR [rax]
   140007881:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140007884:	89 c1                	mov    ecx,eax
   140007886:	d3 ea                	shr    edx,cl
   140007888:	89 d0                	mov    eax,edx
   14000788a:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   14000788d:	eb 3c                	jmp    1400078cb <__rshift_D2A+0xd6>
   14000788f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007893:	8b 10                	mov    edx,DWORD PTR [rax]
   140007895:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140007898:	89 c1                	mov    ecx,eax
   14000789a:	d3 e2                	shl    edx,cl
   14000789c:	89 d1                	mov    ecx,edx
   14000789e:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400078a2:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400078a6:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400078aa:	0b 4d ec             	or     ecx,DWORD PTR [rbp-0x14]
   1400078ad:	89 ca                	mov    edx,ecx
   1400078af:	89 10                	mov    DWORD PTR [rax],edx
   1400078b1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400078b5:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400078b9:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   1400078bd:	8b 10                	mov    edx,DWORD PTR [rax]
   1400078bf:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   1400078c2:	89 c1                	mov    ecx,eax
   1400078c4:	d3 ea                	shr    edx,cl
   1400078c6:	89 d0                	mov    eax,edx
   1400078c8:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   1400078cb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400078cf:	48 3b 45 e0          	cmp    rax,QWORD PTR [rbp-0x20]
   1400078d3:	72 ba                	jb     14000788f <__rshift_D2A+0x9a>
   1400078d5:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400078d9:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   1400078dc:	89 10                	mov    DWORD PTR [rax],edx
   1400078de:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400078e2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400078e4:	85 c0                	test   eax,eax
   1400078e6:	74 2d                	je     140007915 <__rshift_D2A+0x120>
   1400078e8:	48 83 45 f0 04       	add    QWORD PTR [rbp-0x10],0x4
   1400078ed:	eb 26                	jmp    140007915 <__rshift_D2A+0x120>
   1400078ef:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400078f3:	48 8d 42 04          	lea    rax,[rdx+0x4]
   1400078f7:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400078fb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400078ff:	48 8d 48 04          	lea    rcx,[rax+0x4]
   140007903:	48 89 4d f0          	mov    QWORD PTR [rbp-0x10],rcx
   140007907:	8b 12                	mov    edx,DWORD PTR [rdx]
   140007909:	89 10                	mov    DWORD PTR [rax],edx
   14000790b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000790f:	48 3b 45 e0          	cmp    rax,QWORD PTR [rbp-0x20]
   140007913:	72 da                	jb     1400078ef <__rshift_D2A+0xfa>
   140007915:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007919:	48 83 c0 18          	add    rax,0x18
   14000791d:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140007921:	48 29 c2             	sub    rdx,rax
   140007924:	48 89 d0             	mov    rax,rdx
   140007927:	48 c1 f8 02          	sar    rax,0x2
   14000792b:	89 c2                	mov    edx,eax
   14000792d:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007931:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140007934:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007938:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   14000793b:	85 c0                	test   eax,eax
   14000793d:	75 0b                	jne    14000794a <__rshift_D2A+0x155>
   14000793f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007943:	c7 40 18 00 00 00 00 	mov    DWORD PTR [rax+0x18],0x0
   14000794a:	90                   	nop
   14000794b:	48 83 c4 20          	add    rsp,0x20
   14000794f:	5d                   	pop    rbp
   140007950:	c3                   	ret

0000000140007951 <__trailz_D2A>:
   140007951:	55                   	push   rbp
   140007952:	48 89 e5             	mov    rbp,rsp
   140007955:	48 83 ec 40          	sub    rsp,0x40
   140007959:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000795d:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140007964:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007968:	48 83 c0 18          	add    rax,0x18
   14000796c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007970:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007974:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007977:	48 98                	cdqe
   140007979:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140007980:	00 
   140007981:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007985:	48 01 d0             	add    rax,rdx
   140007988:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   14000798c:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140007993:	eb 09                	jmp    14000799e <__trailz_D2A+0x4d>
   140007995:	83 45 f4 20          	add    DWORD PTR [rbp-0xc],0x20
   140007999:	48 83 45 f8 04       	add    QWORD PTR [rbp-0x8],0x4
   14000799e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400079a2:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   1400079a6:	73 0a                	jae    1400079b2 <__trailz_D2A+0x61>
   1400079a8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400079ac:	8b 00                	mov    eax,DWORD PTR [rax]
   1400079ae:	85 c0                	test   eax,eax
   1400079b0:	74 e3                	je     140007995 <__trailz_D2A+0x44>
   1400079b2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400079b6:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   1400079ba:	73 18                	jae    1400079d4 <__trailz_D2A+0x83>
   1400079bc:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400079c0:	8b 00                	mov    eax,DWORD PTR [rax]
   1400079c2:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400079c5:	48 8d 45 e4          	lea    rax,[rbp-0x1c]
   1400079c9:	48 89 c1             	mov    rcx,rax
   1400079cc:	e8 ef fd ff ff       	call   1400077c0 <__lo0bits_D2A>
   1400079d1:	01 45 f4             	add    DWORD PTR [rbp-0xc],eax
   1400079d4:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   1400079d7:	48 83 c4 40          	add    rsp,0x40
   1400079db:	5d                   	pop    rbp
   1400079dc:	c3                   	ret
   1400079dd:	90                   	nop
   1400079de:	90                   	nop
   1400079df:	90                   	nop

00000001400079e0 <dtoa_lock_cleanup>:
   1400079e0:	55                   	push   rbp
   1400079e1:	48 89 e5             	mov    rbp,rsp
   1400079e4:	48 83 ec 40          	sub    rsp,0x40
   1400079e8:	48 8d 05 01 78 00 00 	lea    rax,[rip+0x7801]        # 14000f1f0 <dtoa_CS_init>
   1400079ef:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400079f3:	c7 45 ec 03 00 00 00 	mov    DWORD PTR [rbp-0x14],0x3
   1400079fa:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   1400079fd:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007a01:	87 10                	xchg   DWORD PTR [rax],edx
   140007a03:	89 d0                	mov    eax,edx
   140007a05:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140007a08:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   140007a0c:	75 3d                	jne    140007a4b <dtoa_lock_cleanup+0x6b>
   140007a0e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140007a15:	eb 2e                	jmp    140007a45 <dtoa_lock_cleanup+0x65>
   140007a17:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007a1a:	48 63 d0             	movsxd rdx,eax
   140007a1d:	48 89 d0             	mov    rax,rdx
   140007a20:	48 c1 e0 02          	shl    rax,0x2
   140007a24:	48 01 d0             	add    rax,rdx
   140007a27:	48 c1 e0 03          	shl    rax,0x3
   140007a2b:	48 8d 15 6e 77 00 00 	lea    rdx,[rip+0x776e]        # 14000f1a0 <dtoa_CritSec>
   140007a32:	48 01 d0             	add    rax,rdx
   140007a35:	48 89 c1             	mov    rcx,rax
   140007a38:	48 8b 05 a9 87 00 00 	mov    rax,QWORD PTR [rip+0x87a9]        # 1400101e8 <__IAT_start__>
   140007a3f:	ff d0                	call   rax
   140007a41:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140007a45:	83 7d fc 01          	cmp    DWORD PTR [rbp-0x4],0x1
   140007a49:	7e cc                	jle    140007a17 <dtoa_lock_cleanup+0x37>
   140007a4b:	90                   	nop
   140007a4c:	48 83 c4 40          	add    rsp,0x40
   140007a50:	5d                   	pop    rbp
   140007a51:	c3                   	ret

0000000140007a52 <dtoa_lock>:
   140007a52:	55                   	push   rbp
   140007a53:	48 89 e5             	mov    rbp,rsp
   140007a56:	48 83 ec 40          	sub    rsp,0x40
   140007a5a:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140007a5d:	8b 05 8d 77 00 00    	mov    eax,DWORD PTR [rip+0x778d]        # 14000f1f0 <dtoa_CS_init>
   140007a63:	83 f8 02             	cmp    eax,0x2
   140007a66:	75 2c                	jne    140007a94 <dtoa_lock+0x42>
   140007a68:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007a6b:	48 89 d0             	mov    rax,rdx
   140007a6e:	48 c1 e0 02          	shl    rax,0x2
   140007a72:	48 01 d0             	add    rax,rdx
   140007a75:	48 c1 e0 03          	shl    rax,0x3
   140007a79:	48 8d 15 20 77 00 00 	lea    rdx,[rip+0x7720]        # 14000f1a0 <dtoa_CritSec>
   140007a80:	48 01 d0             	add    rax,rdx
   140007a83:	48 89 c1             	mov    rcx,rax
   140007a86:	48 8b 05 63 87 00 00 	mov    rax,QWORD PTR [rip+0x8763]        # 1400101f0 <__imp_EnterCriticalSection>
   140007a8d:	ff d0                	call   rax
   140007a8f:	e9 ea 00 00 00       	jmp    140007b7e <dtoa_lock+0x12c>
   140007a94:	8b 05 56 77 00 00    	mov    eax,DWORD PTR [rip+0x7756]        # 14000f1f0 <dtoa_CS_init>
   140007a9a:	85 c0                	test   eax,eax
   140007a9c:	0f 85 9e 00 00 00    	jne    140007b40 <dtoa_lock+0xee>
   140007aa2:	48 8d 05 47 77 00 00 	lea    rax,[rip+0x7747]        # 14000f1f0 <dtoa_CS_init>
   140007aa9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140007aad:	c7 45 ec 01 00 00 00 	mov    DWORD PTR [rbp-0x14],0x1
   140007ab4:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   140007ab7:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007abb:	87 10                	xchg   DWORD PTR [rax],edx
   140007abd:	89 d0                	mov    eax,edx
   140007abf:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140007ac2:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140007ac6:	75 58                	jne    140007b20 <dtoa_lock+0xce>
   140007ac8:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140007acf:	eb 2e                	jmp    140007aff <dtoa_lock+0xad>
   140007ad1:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007ad4:	48 63 d0             	movsxd rdx,eax
   140007ad7:	48 89 d0             	mov    rax,rdx
   140007ada:	48 c1 e0 02          	shl    rax,0x2
   140007ade:	48 01 d0             	add    rax,rdx
   140007ae1:	48 c1 e0 03          	shl    rax,0x3
   140007ae5:	48 8d 15 b4 76 00 00 	lea    rdx,[rip+0x76b4]        # 14000f1a0 <dtoa_CritSec>
   140007aec:	48 01 d0             	add    rax,rdx
   140007aef:	48 89 c1             	mov    rcx,rax
   140007af2:	48 8b 05 27 87 00 00 	mov    rax,QWORD PTR [rip+0x8727]        # 140010220 <__imp_InitializeCriticalSection>
   140007af9:	ff d0                	call   rax
   140007afb:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140007aff:	83 7d fc 01          	cmp    DWORD PTR [rbp-0x4],0x1
   140007b03:	7e cc                	jle    140007ad1 <dtoa_lock+0x7f>
   140007b05:	48 8d 05 d4 fe ff ff 	lea    rax,[rip+0xfffffffffffffed4]        # 1400079e0 <dtoa_lock_cleanup>
   140007b0c:	48 89 c1             	mov    rcx,rax
   140007b0f:	e8 1b 9b ff ff       	call   14000162f <atexit>
   140007b14:	c7 05 d2 76 00 00 02 	mov    DWORD PTR [rip+0x76d2],0x2        # 14000f1f0 <dtoa_CS_init>
   140007b1b:	00 00 00 
   140007b1e:	eb 20                	jmp    140007b40 <dtoa_lock+0xee>
   140007b20:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   140007b24:	75 1a                	jne    140007b40 <dtoa_lock+0xee>
   140007b26:	c7 05 c0 76 00 00 02 	mov    DWORD PTR [rip+0x76c0],0x2        # 14000f1f0 <dtoa_CS_init>
   140007b2d:	00 00 00 
   140007b30:	eb 0e                	jmp    140007b40 <dtoa_lock+0xee>
   140007b32:	b9 01 00 00 00       	mov    ecx,0x1
   140007b37:	48 8b 05 0a 87 00 00 	mov    rax,QWORD PTR [rip+0x870a]        # 140010248 <__imp_Sleep>
   140007b3e:	ff d0                	call   rax
   140007b40:	8b 05 aa 76 00 00    	mov    eax,DWORD PTR [rip+0x76aa]        # 14000f1f0 <dtoa_CS_init>
   140007b46:	83 f8 01             	cmp    eax,0x1
   140007b49:	74 e7                	je     140007b32 <dtoa_lock+0xe0>
   140007b4b:	8b 05 9f 76 00 00    	mov    eax,DWORD PTR [rip+0x769f]        # 14000f1f0 <dtoa_CS_init>
   140007b51:	83 f8 02             	cmp    eax,0x2
   140007b54:	75 28                	jne    140007b7e <dtoa_lock+0x12c>
   140007b56:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007b59:	48 89 d0             	mov    rax,rdx
   140007b5c:	48 c1 e0 02          	shl    rax,0x2
   140007b60:	48 01 d0             	add    rax,rdx
   140007b63:	48 c1 e0 03          	shl    rax,0x3
   140007b67:	48 8d 15 32 76 00 00 	lea    rdx,[rip+0x7632]        # 14000f1a0 <dtoa_CritSec>
   140007b6e:	48 01 d0             	add    rax,rdx
   140007b71:	48 89 c1             	mov    rcx,rax
   140007b74:	48 8b 05 75 86 00 00 	mov    rax,QWORD PTR [rip+0x8675]        # 1400101f0 <__imp_EnterCriticalSection>
   140007b7b:	ff d0                	call   rax
   140007b7d:	90                   	nop
   140007b7e:	48 83 c4 40          	add    rsp,0x40
   140007b82:	5d                   	pop    rbp
   140007b83:	c3                   	ret

0000000140007b84 <dtoa_unlock>:
   140007b84:	55                   	push   rbp
   140007b85:	48 89 e5             	mov    rbp,rsp
   140007b88:	48 83 ec 20          	sub    rsp,0x20
   140007b8c:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140007b8f:	8b 05 5b 76 00 00    	mov    eax,DWORD PTR [rip+0x765b]        # 14000f1f0 <dtoa_CS_init>
   140007b95:	83 f8 02             	cmp    eax,0x2
   140007b98:	75 27                	jne    140007bc1 <dtoa_unlock+0x3d>
   140007b9a:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007b9d:	48 89 d0             	mov    rax,rdx
   140007ba0:	48 c1 e0 02          	shl    rax,0x2
   140007ba4:	48 01 d0             	add    rax,rdx
   140007ba7:	48 c1 e0 03          	shl    rax,0x3
   140007bab:	48 8d 15 ee 75 00 00 	lea    rdx,[rip+0x75ee]        # 14000f1a0 <dtoa_CritSec>
   140007bb2:	48 01 d0             	add    rax,rdx
   140007bb5:	48 89 c1             	mov    rcx,rax
   140007bb8:	48 8b 05 69 86 00 00 	mov    rax,QWORD PTR [rip+0x8669]        # 140010228 <__imp_LeaveCriticalSection>
   140007bbf:	ff d0                	call   rax
   140007bc1:	90                   	nop
   140007bc2:	48 83 c4 20          	add    rsp,0x20
   140007bc6:	5d                   	pop    rbp
   140007bc7:	c3                   	ret

0000000140007bc8 <__lo0bits_D2A>:
   140007bc8:	55                   	push   rbp
   140007bc9:	48 89 e5             	mov    rbp,rsp
   140007bcc:	48 83 ec 10          	sub    rsp,0x10
   140007bd0:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140007bd4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007bd8:	8b 00                	mov    eax,DWORD PTR [rax]
   140007bda:	f3 0f bc c0          	tzcnt  eax,eax
   140007bde:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140007be1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007be5:	8b 10                	mov    edx,DWORD PTR [rax]
   140007be7:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007bea:	89 c1                	mov    ecx,eax
   140007bec:	d3 ea                	shr    edx,cl
   140007bee:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007bf2:	89 10                	mov    DWORD PTR [rax],edx
   140007bf4:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007bf7:	48 83 c4 10          	add    rsp,0x10
   140007bfb:	5d                   	pop    rbp
   140007bfc:	c3                   	ret

0000000140007bfd <__hi0bits_D2A>:
   140007bfd:	55                   	push   rbp
   140007bfe:	48 89 e5             	mov    rbp,rsp
   140007c01:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140007c04:	0f bd 45 10          	bsr    eax,DWORD PTR [rbp+0x10]
   140007c08:	83 f0 1f             	xor    eax,0x1f
   140007c0b:	5d                   	pop    rbp
   140007c0c:	c3                   	ret

0000000140007c0d <__Balloc_D2A>:
   140007c0d:	55                   	push   rbp
   140007c0e:	48 89 e5             	mov    rbp,rsp
   140007c11:	48 83 ec 30          	sub    rsp,0x30
   140007c15:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140007c18:	b9 00 00 00 00       	mov    ecx,0x0
   140007c1d:	e8 30 fe ff ff       	call   140007a52 <dtoa_lock>
   140007c22:	83 7d 10 09          	cmp    DWORD PTR [rbp+0x10],0x9
   140007c26:	7f 48                	jg     140007c70 <__Balloc_D2A+0x63>
   140007c28:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140007c2b:	48 98                	cdqe
   140007c2d:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   140007c34:	00 
   140007c35:	48 8d 05 c4 75 00 00 	lea    rax,[rip+0x75c4]        # 14000f200 <freelist>
   140007c3c:	48 8b 04 02          	mov    rax,QWORD PTR [rdx+rax*1]
   140007c40:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007c44:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140007c49:	74 25                	je     140007c70 <__Balloc_D2A+0x63>
   140007c4b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007c4f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140007c52:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007c55:	48 63 d2             	movsxd rdx,edx
   140007c58:	48 8d 0c d5 00 00 00 	lea    rcx,[rdx*8+0x0]
   140007c5f:	00 
   140007c60:	48 8d 15 99 75 00 00 	lea    rdx,[rip+0x7599]        # 14000f200 <freelist>
   140007c67:	48 89 04 11          	mov    QWORD PTR [rcx+rdx*1],rax
   140007c6b:	e9 b1 00 00 00       	jmp    140007d21 <__Balloc_D2A+0x114>
   140007c70:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140007c73:	ba 01 00 00 00       	mov    edx,0x1
   140007c78:	89 c1                	mov    ecx,eax
   140007c7a:	d3 e2                	shl    edx,cl
   140007c7c:	89 d0                	mov    eax,edx
   140007c7e:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140007c81:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140007c84:	83 e8 01             	sub    eax,0x1
   140007c87:	48 98                	cdqe
   140007c89:	48 c1 e0 02          	shl    rax,0x2
   140007c8d:	48 83 c0 27          	add    rax,0x27
   140007c91:	48 c1 e8 03          	shr    rax,0x3
   140007c95:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   140007c98:	83 7d 10 09          	cmp    DWORD PTR [rbp+0x10],0x9
   140007c9c:	7f 4e                	jg     140007cec <__Balloc_D2A+0xdf>
   140007c9e:	48 8b 15 fb 23 00 00 	mov    rdx,QWORD PTR [rip+0x23fb]        # 14000a0a0 <pmem_next>
   140007ca5:	48 8d 05 b4 75 00 00 	lea    rax,[rip+0x75b4]        # 14000f260 <private_mem>
   140007cac:	48 29 c2             	sub    rdx,rax
   140007caf:	48 89 d0             	mov    rax,rdx
   140007cb2:	48 c1 f8 03          	sar    rax,0x3
   140007cb6:	48 89 c2             	mov    rdx,rax
   140007cb9:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140007cbc:	48 01 d0             	add    rax,rdx
   140007cbf:	48 3d 20 01 00 00    	cmp    rax,0x120
   140007cc5:	77 25                	ja     140007cec <__Balloc_D2A+0xdf>
   140007cc7:	48 8b 05 d2 23 00 00 	mov    rax,QWORD PTR [rip+0x23d2]        # 14000a0a0 <pmem_next>
   140007cce:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007cd2:	48 8b 05 c7 23 00 00 	mov    rax,QWORD PTR [rip+0x23c7]        # 14000a0a0 <pmem_next>
   140007cd9:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   140007cdc:	48 c1 e2 03          	shl    rdx,0x3
   140007ce0:	48 01 d0             	add    rax,rdx
   140007ce3:	48 89 05 b6 23 00 00 	mov    QWORD PTR [rip+0x23b6],rax        # 14000a0a0 <pmem_next>
   140007cea:	eb 21                	jmp    140007d0d <__Balloc_D2A+0x100>
   140007cec:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140007cef:	48 c1 e0 03          	shl    rax,0x3
   140007cf3:	48 89 c1             	mov    rcx,rax
   140007cf6:	e8 e5 18 00 00       	call   1400095e0 <malloc>
   140007cfb:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007cff:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140007d04:	75 07                	jne    140007d0d <__Balloc_D2A+0x100>
   140007d06:	b8 00 00 00 00       	mov    eax,0x0
   140007d0b:	eb 3b                	jmp    140007d48 <__Balloc_D2A+0x13b>
   140007d0d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d11:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007d14:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140007d17:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d1b:	8b 55 f4             	mov    edx,DWORD PTR [rbp-0xc]
   140007d1e:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140007d21:	b9 00 00 00 00       	mov    ecx,0x0
   140007d26:	e8 59 fe ff ff       	call   140007b84 <dtoa_unlock>
   140007d2b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d2f:	c7 40 14 00 00 00 00 	mov    DWORD PTR [rax+0x14],0x0
   140007d36:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d3a:	8b 50 14             	mov    edx,DWORD PTR [rax+0x14]
   140007d3d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d41:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140007d44:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d48:	48 83 c4 30          	add    rsp,0x30
   140007d4c:	5d                   	pop    rbp
   140007d4d:	c3                   	ret

0000000140007d4e <__Bfree_D2A>:
   140007d4e:	55                   	push   rbp
   140007d4f:	48 89 e5             	mov    rbp,rsp
   140007d52:	48 83 ec 20          	sub    rsp,0x20
   140007d56:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140007d5a:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140007d5f:	74 71                	je     140007dd2 <__Bfree_D2A+0x84>
   140007d61:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007d65:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140007d68:	83 f8 09             	cmp    eax,0x9
   140007d6b:	7e 0e                	jle    140007d7b <__Bfree_D2A+0x2d>
   140007d6d:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007d71:	48 89 c1             	mov    rcx,rax
   140007d74:	e8 57 18 00 00       	call   1400095d0 <free>
   140007d79:	eb 57                	jmp    140007dd2 <__Bfree_D2A+0x84>
   140007d7b:	b9 00 00 00 00       	mov    ecx,0x0
   140007d80:	e8 cd fc ff ff       	call   140007a52 <dtoa_lock>
   140007d85:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007d89:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140007d8c:	48 98                	cdqe
   140007d8e:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   140007d95:	00 
   140007d96:	48 8d 05 63 74 00 00 	lea    rax,[rip+0x7463]        # 14000f200 <freelist>
   140007d9d:	48 8b 14 02          	mov    rdx,QWORD PTR [rdx+rax*1]
   140007da1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007da5:	48 89 10             	mov    QWORD PTR [rax],rdx
   140007da8:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007dac:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140007daf:	48 98                	cdqe
   140007db1:	48 8d 0c c5 00 00 00 	lea    rcx,[rax*8+0x0]
   140007db8:	00 
   140007db9:	48 8d 15 40 74 00 00 	lea    rdx,[rip+0x7440]        # 14000f200 <freelist>
   140007dc0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007dc4:	48 89 04 11          	mov    QWORD PTR [rcx+rdx*1],rax
   140007dc8:	b9 00 00 00 00       	mov    ecx,0x0
   140007dcd:	e8 b2 fd ff ff       	call   140007b84 <dtoa_unlock>
   140007dd2:	90                   	nop
   140007dd3:	48 83 c4 20          	add    rsp,0x20
   140007dd7:	5d                   	pop    rbp
   140007dd8:	c3                   	ret

0000000140007dd9 <__multadd_D2A>:
   140007dd9:	55                   	push   rbp
   140007dda:	48 89 e5             	mov    rbp,rsp
   140007ddd:	48 83 ec 50          	sub    rsp,0x50
   140007de1:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140007de5:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140007de8:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d
   140007dec:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007df0:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007df3:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140007df6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007dfa:	48 83 c0 18          	add    rax,0x18
   140007dfe:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140007e02:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140007e09:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140007e0c:	48 98                	cdqe
   140007e0e:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140007e12:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007e16:	8b 00                	mov    eax,DWORD PTR [rax]
   140007e18:	89 c2                	mov    edx,eax
   140007e1a:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140007e1d:	48 98                	cdqe
   140007e1f:	48 0f af d0          	imul   rdx,rax
   140007e23:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140007e27:	48 01 d0             	add    rax,rdx
   140007e2a:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140007e2e:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140007e32:	48 c1 e8 20          	shr    rax,0x20
   140007e36:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140007e3a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007e3e:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140007e42:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140007e46:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   140007e4a:	89 10                	mov    DWORD PTR [rax],edx
   140007e4c:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140007e50:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007e53:	3b 45 e4             	cmp    eax,DWORD PTR [rbp-0x1c]
   140007e56:	7c ba                	jl     140007e12 <__multadd_D2A+0x39>
   140007e58:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   140007e5d:	0f 84 9a 00 00 00    	je     140007efd <__multadd_D2A+0x124>
   140007e63:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007e67:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140007e6a:	39 45 e4             	cmp    DWORD PTR [rbp-0x1c],eax
   140007e6d:	7c 67                	jl     140007ed6 <__multadd_D2A+0xfd>
   140007e6f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007e73:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140007e76:	83 c0 01             	add    eax,0x1
   140007e79:	89 c1                	mov    ecx,eax
   140007e7b:	e8 8d fd ff ff       	call   140007c0d <__Balloc_D2A>
   140007e80:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140007e84:	48 83 7d d0 00       	cmp    QWORD PTR [rbp-0x30],0x0
   140007e89:	75 07                	jne    140007e92 <__multadd_D2A+0xb9>
   140007e8b:	b8 00 00 00 00       	mov    eax,0x0
   140007e90:	eb 6f                	jmp    140007f01 <__multadd_D2A+0x128>
   140007e92:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007e96:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007e99:	48 98                	cdqe
   140007e9b:	48 83 c0 02          	add    rax,0x2
   140007e9f:	48 8d 0c 85 00 00 00 	lea    rcx,[rax*4+0x0]
   140007ea6:	00 
   140007ea7:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007eab:	48 8d 50 10          	lea    rdx,[rax+0x10]
   140007eaf:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140007eb3:	48 83 c0 10          	add    rax,0x10
   140007eb7:	49 89 c8             	mov    r8,rcx
   140007eba:	48 89 c1             	mov    rcx,rax
   140007ebd:	e8 26 17 00 00       	call   1400095e8 <memcpy>
   140007ec2:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007ec6:	48 89 c1             	mov    rcx,rax
   140007ec9:	e8 80 fe ff ff       	call   140007d4e <__Bfree_D2A>
   140007ece:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140007ed2:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140007ed6:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140007ed9:	8d 50 01             	lea    edx,[rax+0x1]
   140007edc:	89 55 e4             	mov    DWORD PTR [rbp-0x1c],edx
   140007edf:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
   140007ee3:	89 d1                	mov    ecx,edx
   140007ee5:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140007ee9:	48 98                	cdqe
   140007eeb:	48 83 c0 04          	add    rax,0x4
   140007eef:	89 4c 82 08          	mov    DWORD PTR [rdx+rax*4+0x8],ecx
   140007ef3:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007ef7:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   140007efa:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140007efd:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007f01:	48 83 c4 50          	add    rsp,0x50
   140007f05:	5d                   	pop    rbp
   140007f06:	c3                   	ret

0000000140007f07 <__i2b_D2A>:
   140007f07:	55                   	push   rbp
   140007f08:	48 89 e5             	mov    rbp,rsp
   140007f0b:	48 83 ec 30          	sub    rsp,0x30
   140007f0f:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140007f12:	b9 01 00 00 00       	mov    ecx,0x1
   140007f17:	e8 f1 fc ff ff       	call   140007c0d <__Balloc_D2A>
   140007f1c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007f20:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140007f25:	75 07                	jne    140007f2e <__i2b_D2A+0x27>
   140007f27:	b8 00 00 00 00       	mov    eax,0x0
   140007f2c:	eb 19                	jmp    140007f47 <__i2b_D2A+0x40>
   140007f2e:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007f31:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007f35:	89 50 18             	mov    DWORD PTR [rax+0x18],edx
   140007f38:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007f3c:	c7 40 14 01 00 00 00 	mov    DWORD PTR [rax+0x14],0x1
   140007f43:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007f47:	48 83 c4 30          	add    rsp,0x30
   140007f4b:	5d                   	pop    rbp
   140007f4c:	c3                   	ret

0000000140007f4d <__mult_D2A>:
   140007f4d:	55                   	push   rbp
   140007f4e:	48 89 e5             	mov    rbp,rsp
   140007f51:	48 81 ec 90 00 00 00 	sub    rsp,0x90
   140007f58:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140007f5c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140007f60:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007f64:	8b 50 14             	mov    edx,DWORD PTR [rax+0x14]
   140007f67:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007f6b:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007f6e:	39 c2                	cmp    edx,eax
   140007f70:	7d 18                	jge    140007f8a <__mult_D2A+0x3d>
   140007f72:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007f76:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140007f7a:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007f7e:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140007f82:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140007f86:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140007f8a:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007f8e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140007f91:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140007f94:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007f98:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007f9b:	89 45 c4             	mov    DWORD PTR [rbp-0x3c],eax
   140007f9e:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007fa2:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007fa5:	89 45 c0             	mov    DWORD PTR [rbp-0x40],eax
   140007fa8:	8b 55 c4             	mov    edx,DWORD PTR [rbp-0x3c]
   140007fab:	8b 45 c0             	mov    eax,DWORD PTR [rbp-0x40]
   140007fae:	01 d0                	add    eax,edx
   140007fb0:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140007fb3:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007fb7:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140007fba:	39 45 f8             	cmp    DWORD PTR [rbp-0x8],eax
   140007fbd:	7e 04                	jle    140007fc3 <__mult_D2A+0x76>
   140007fbf:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140007fc3:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007fc6:	89 c1                	mov    ecx,eax
   140007fc8:	e8 40 fc ff ff       	call   140007c0d <__Balloc_D2A>
   140007fcd:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140007fd1:	48 83 7d c8 00       	cmp    QWORD PTR [rbp-0x38],0x0
   140007fd6:	75 0a                	jne    140007fe2 <__mult_D2A+0x95>
   140007fd8:	b8 00 00 00 00       	mov    eax,0x0
   140007fdd:	e9 88 01 00 00       	jmp    14000816a <__mult_D2A+0x21d>
   140007fe2:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140007fe6:	48 83 c0 18          	add    rax,0x18
   140007fea:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140007fee:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140007ff1:	48 98                	cdqe
   140007ff3:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140007ffa:	00 
   140007ffb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007fff:	48 01 d0             	add    rax,rdx
   140008002:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140008006:	eb 0f                	jmp    140008017 <__mult_D2A+0xca>
   140008008:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000800c:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140008012:	48 83 45 f0 04       	add    QWORD PTR [rbp-0x10],0x4
   140008017:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000801b:	48 3b 45 b8          	cmp    rax,QWORD PTR [rbp-0x48]
   14000801f:	72 e7                	jb     140008008 <__mult_D2A+0xbb>
   140008021:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008025:	48 83 c0 18          	add    rax,0x18
   140008029:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000802d:	8b 45 c4             	mov    eax,DWORD PTR [rbp-0x3c]
   140008030:	48 98                	cdqe
   140008032:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140008039:	00 
   14000803a:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000803e:	48 01 d0             	add    rax,rdx
   140008041:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140008045:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140008049:	48 83 c0 18          	add    rax,0x18
   14000804d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140008051:	8b 45 c0             	mov    eax,DWORD PTR [rbp-0x40]
   140008054:	48 98                	cdqe
   140008056:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   14000805d:	00 
   14000805e:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008062:	48 01 d0             	add    rax,rdx
   140008065:	48 89 45 a8          	mov    QWORD PTR [rbp-0x58],rax
   140008069:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   14000806d:	48 83 c0 18          	add    rax,0x18
   140008071:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140008075:	e9 95 00 00 00       	jmp    14000810f <__mult_D2A+0x1c2>
   14000807a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000807e:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140008082:	48 89 55 e8          	mov    QWORD PTR [rbp-0x18],rdx
   140008086:	8b 00                	mov    eax,DWORD PTR [rax]
   140008088:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
   14000808b:	83 7d a4 00          	cmp    DWORD PTR [rbp-0x5c],0x0
   14000808f:	74 79                	je     14000810a <__mult_D2A+0x1bd>
   140008091:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140008095:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140008099:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000809d:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400080a1:	48 c7 45 d0 00 00 00 	mov    QWORD PTR [rbp-0x30],0x0
   1400080a8:	00 
   1400080a9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400080ad:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400080b1:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400080b5:	8b 00                	mov    eax,DWORD PTR [rax]
   1400080b7:	89 c2                	mov    edx,eax
   1400080b9:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
   1400080bc:	48 0f af d0          	imul   rdx,rax
   1400080c0:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400080c4:	8b 00                	mov    eax,DWORD PTR [rax]
   1400080c6:	89 c0                	mov    eax,eax
   1400080c8:	48 01 c2             	add    rdx,rax
   1400080cb:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400080cf:	48 01 d0             	add    rax,rdx
   1400080d2:	48 89 45 98          	mov    QWORD PTR [rbp-0x68],rax
   1400080d6:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
   1400080da:	48 c1 e8 20          	shr    rax,0x20
   1400080de:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   1400080e2:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400080e6:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400080ea:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   1400080ee:	48 8b 55 98          	mov    rdx,QWORD PTR [rbp-0x68]
   1400080f2:	89 10                	mov    DWORD PTR [rax],edx
   1400080f4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400080f8:	48 3b 45 b0          	cmp    rax,QWORD PTR [rbp-0x50]
   1400080fc:	72 ab                	jb     1400080a9 <__mult_D2A+0x15c>
   1400080fe:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140008102:	89 c2                	mov    edx,eax
   140008104:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008108:	89 10                	mov    DWORD PTR [rax],edx
   14000810a:	48 83 45 d8 04       	add    QWORD PTR [rbp-0x28],0x4
   14000810f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008113:	48 3b 45 a8          	cmp    rax,QWORD PTR [rbp-0x58]
   140008117:	0f 82 5d ff ff ff    	jb     14000807a <__mult_D2A+0x12d>
   14000811d:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140008121:	48 83 c0 18          	add    rax,0x18
   140008125:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140008129:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   14000812c:	48 98                	cdqe
   14000812e:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140008135:	00 
   140008136:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000813a:	48 01 d0             	add    rax,rdx
   14000813d:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140008141:	eb 04                	jmp    140008147 <__mult_D2A+0x1fa>
   140008143:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   140008147:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   14000814b:	7e 0f                	jle    14000815c <__mult_D2A+0x20f>
   14000814d:	48 83 6d e0 04       	sub    QWORD PTR [rbp-0x20],0x4
   140008152:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008156:	8b 00                	mov    eax,DWORD PTR [rax]
   140008158:	85 c0                	test   eax,eax
   14000815a:	74 e7                	je     140008143 <__mult_D2A+0x1f6>
   14000815c:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140008160:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140008163:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140008166:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   14000816a:	48 81 c4 90 00 00 00 	add    rsp,0x90
   140008171:	5d                   	pop    rbp
   140008172:	c3                   	ret

0000000140008173 <__pow5mult_D2A>:
   140008173:	55                   	push   rbp
   140008174:	48 89 e5             	mov    rbp,rsp
   140008177:	48 83 ec 40          	sub    rsp,0x40
   14000817b:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000817f:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140008182:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140008185:	83 e0 03             	and    eax,0x3
   140008188:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   14000818b:	83 7d ec 00          	cmp    DWORD PTR [rbp-0x14],0x0
   14000818f:	74 41                	je     1400081d2 <__pow5mult_D2A+0x5f>
   140008191:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
   140008194:	83 e8 01             	sub    eax,0x1
   140008197:	48 98                	cdqe
   140008199:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   1400081a0:	00 
   1400081a1:	48 8d 05 00 1f 00 00 	lea    rax,[rip+0x1f00]        # 14000a0a8 <p05.0>
   1400081a8:	8b 14 02             	mov    edx,DWORD PTR [rdx+rax*1]
   1400081ab:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400081af:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400081b5:	48 89 c1             	mov    rcx,rax
   1400081b8:	e8 1c fc ff ff       	call   140007dd9 <__multadd_D2A>
   1400081bd:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   1400081c1:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   1400081c6:	75 0a                	jne    1400081d2 <__pow5mult_D2A+0x5f>
   1400081c8:	b8 00 00 00 00       	mov    eax,0x0
   1400081cd:	e9 58 01 00 00       	jmp    14000832a <__pow5mult_D2A+0x1b7>
   1400081d2:	c1 7d 18 02          	sar    DWORD PTR [rbp+0x18],0x2
   1400081d6:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   1400081da:	75 09                	jne    1400081e5 <__pow5mult_D2A+0x72>
   1400081dc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400081e0:	e9 45 01 00 00       	jmp    14000832a <__pow5mult_D2A+0x1b7>
   1400081e5:	48 8b 05 74 79 00 00 	mov    rax,QWORD PTR [rip+0x7974]        # 14000fb60 <p5s>
   1400081ec:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400081f0:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400081f5:	75 5e                	jne    140008255 <__pow5mult_D2A+0xe2>
   1400081f7:	b9 01 00 00 00       	mov    ecx,0x1
   1400081fc:	e8 51 f8 ff ff       	call   140007a52 <dtoa_lock>
   140008201:	48 8b 05 58 79 00 00 	mov    rax,QWORD PTR [rip+0x7958]        # 14000fb60 <p5s>
   140008208:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000820c:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140008211:	75 38                	jne    14000824b <__pow5mult_D2A+0xd8>
   140008213:	b9 71 02 00 00       	mov    ecx,0x271
   140008218:	e8 ea fc ff ff       	call   140007f07 <__i2b_D2A>
   14000821d:	48 89 05 3c 79 00 00 	mov    QWORD PTR [rip+0x793c],rax        # 14000fb60 <p5s>
   140008224:	48 8b 05 35 79 00 00 	mov    rax,QWORD PTR [rip+0x7935]        # 14000fb60 <p5s>
   14000822b:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000822f:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140008234:	75 0a                	jne    140008240 <__pow5mult_D2A+0xcd>
   140008236:	b8 00 00 00 00       	mov    eax,0x0
   14000823b:	e9 ea 00 00 00       	jmp    14000832a <__pow5mult_D2A+0x1b7>
   140008240:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008244:	48 c7 00 00 00 00 00 	mov    QWORD PTR [rax],0x0
   14000824b:	b9 01 00 00 00       	mov    ecx,0x1
   140008250:	e8 2f f9 ff ff       	call   140007b84 <dtoa_unlock>
   140008255:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140008258:	83 e0 01             	and    eax,0x1
   14000825b:	85 c0                	test   eax,eax
   14000825d:	74 39                	je     140008298 <__pow5mult_D2A+0x125>
   14000825f:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140008263:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008267:	48 89 c1             	mov    rcx,rax
   14000826a:	e8 de fc ff ff       	call   140007f4d <__mult_D2A>
   14000826f:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140008273:	48 83 7d e0 00       	cmp    QWORD PTR [rbp-0x20],0x0
   140008278:	75 0a                	jne    140008284 <__pow5mult_D2A+0x111>
   14000827a:	b8 00 00 00 00       	mov    eax,0x0
   14000827f:	e9 a6 00 00 00       	jmp    14000832a <__pow5mult_D2A+0x1b7>
   140008284:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008288:	48 89 c1             	mov    rcx,rax
   14000828b:	e8 be fa ff ff       	call   140007d4e <__Bfree_D2A>
   140008290:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008294:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140008298:	d1 7d 18             	sar    DWORD PTR [rbp+0x18],1
   14000829b:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   14000829f:	0f 84 80 00 00 00    	je     140008325 <__pow5mult_D2A+0x1b2>
   1400082a5:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400082a9:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400082ac:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400082b0:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400082b5:	75 61                	jne    140008318 <__pow5mult_D2A+0x1a5>
   1400082b7:	b9 01 00 00 00       	mov    ecx,0x1
   1400082bc:	e8 91 f7 ff ff       	call   140007a52 <dtoa_lock>
   1400082c1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400082c5:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400082c8:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400082cc:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400082d1:	75 3b                	jne    14000830e <__pow5mult_D2A+0x19b>
   1400082d3:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400082d7:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400082db:	48 89 c1             	mov    rcx,rax
   1400082de:	e8 6a fc ff ff       	call   140007f4d <__mult_D2A>
   1400082e3:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400082e7:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400082ea:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400082ee:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400082f1:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400082f5:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400082fa:	75 07                	jne    140008303 <__pow5mult_D2A+0x190>
   1400082fc:	b8 00 00 00 00       	mov    eax,0x0
   140008301:	eb 27                	jmp    14000832a <__pow5mult_D2A+0x1b7>
   140008303:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008307:	48 c7 00 00 00 00 00 	mov    QWORD PTR [rax],0x0
   14000830e:	b9 01 00 00 00       	mov    ecx,0x1
   140008313:	e8 6c f8 ff ff       	call   140007b84 <dtoa_unlock>
   140008318:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000831c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008320:	e9 30 ff ff ff       	jmp    140008255 <__pow5mult_D2A+0xe2>
   140008325:	90                   	nop
   140008326:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000832a:	48 83 c4 40          	add    rsp,0x40
   14000832e:	5d                   	pop    rbp
   14000832f:	c3                   	ret

0000000140008330 <__lshift_D2A>:
   140008330:	55                   	push   rbp
   140008331:	48 89 e5             	mov    rbp,rsp
   140008334:	48 83 ec 60          	sub    rsp,0x60
   140008338:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000833c:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   14000833f:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140008342:	c1 f8 05             	sar    eax,0x5
   140008345:	89 45 d8             	mov    DWORD PTR [rbp-0x28],eax
   140008348:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000834c:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000834f:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008352:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008356:	8b 50 14             	mov    edx,DWORD PTR [rax+0x14]
   140008359:	8b 45 d8             	mov    eax,DWORD PTR [rbp-0x28]
   14000835c:	01 d0                	add    eax,edx
   14000835e:	83 c0 01             	add    eax,0x1
   140008361:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140008364:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008368:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000836b:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   14000836e:	eb 07                	jmp    140008377 <__lshift_D2A+0x47>
   140008370:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
   140008374:	d1 65 fc             	shl    DWORD PTR [rbp-0x4],1
   140008377:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000837a:	3b 45 fc             	cmp    eax,DWORD PTR [rbp-0x4]
   14000837d:	7f f1                	jg     140008370 <__lshift_D2A+0x40>
   14000837f:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008382:	89 c1                	mov    ecx,eax
   140008384:	e8 84 f8 ff ff       	call   140007c0d <__Balloc_D2A>
   140008389:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   14000838d:	48 83 7d d0 00       	cmp    QWORD PTR [rbp-0x30],0x0
   140008392:	75 0a                	jne    14000839e <__lshift_D2A+0x6e>
   140008394:	b8 00 00 00 00       	mov    eax,0x0
   140008399:	e9 19 01 00 00       	jmp    1400084b7 <__lshift_D2A+0x187>
   14000839e:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400083a2:	48 83 c0 18          	add    rax,0x18
   1400083a6:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400083aa:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400083b1:	eb 16                	jmp    1400083c9 <__lshift_D2A+0x99>
   1400083b3:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400083b7:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400083bb:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   1400083bf:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   1400083c5:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   1400083c9:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400083cc:	3b 45 d8             	cmp    eax,DWORD PTR [rbp-0x28]
   1400083cf:	7c e2                	jl     1400083b3 <__lshift_D2A+0x83>
   1400083d1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400083d5:	48 83 c0 18          	add    rax,0x18
   1400083d9:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400083dd:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400083e1:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400083e4:	48 98                	cdqe
   1400083e6:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   1400083ed:	00 
   1400083ee:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400083f2:	48 01 d0             	add    rax,rdx
   1400083f5:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   1400083f9:	83 65 18 1f          	and    DWORD PTR [rbp+0x18],0x1f
   1400083fd:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140008401:	74 71                	je     140008474 <__lshift_D2A+0x144>
   140008403:	b8 20 00 00 00       	mov    eax,0x20
   140008408:	2b 45 18             	sub    eax,DWORD PTR [rbp+0x18]
   14000840b:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   14000840e:	c7 45 dc 00 00 00 00 	mov    DWORD PTR [rbp-0x24],0x0
   140008415:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008419:	8b 10                	mov    edx,DWORD PTR [rax]
   14000841b:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   14000841e:	89 c1                	mov    ecx,eax
   140008420:	d3 e2                	shl    edx,cl
   140008422:	89 d1                	mov    ecx,edx
   140008424:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008428:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000842c:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   140008430:	0b 4d dc             	or     ecx,DWORD PTR [rbp-0x24]
   140008433:	89 ca                	mov    edx,ecx
   140008435:	89 10                	mov    DWORD PTR [rax],edx
   140008437:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000843b:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000843f:	48 89 55 e8          	mov    QWORD PTR [rbp-0x18],rdx
   140008443:	8b 10                	mov    edx,DWORD PTR [rax]
   140008445:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008448:	89 c1                	mov    ecx,eax
   14000844a:	d3 ea                	shr    edx,cl
   14000844c:	89 d0                	mov    eax,edx
   14000844e:	89 45 dc             	mov    DWORD PTR [rbp-0x24],eax
   140008451:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008455:	48 3b 45 c8          	cmp    rax,QWORD PTR [rbp-0x38]
   140008459:	72 ba                	jb     140008415 <__lshift_D2A+0xe5>
   14000845b:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   14000845f:	8b 55 dc             	mov    edx,DWORD PTR [rbp-0x24]
   140008462:	89 10                	mov    DWORD PTR [rax],edx
   140008464:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008468:	8b 00                	mov    eax,DWORD PTR [rax]
   14000846a:	85 c0                	test   eax,eax
   14000846c:	74 2c                	je     14000849a <__lshift_D2A+0x16a>
   14000846e:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140008472:	eb 26                	jmp    14000849a <__lshift_D2A+0x16a>
   140008474:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
   140008478:	48 8d 42 04          	lea    rax,[rdx+0x4]
   14000847c:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140008480:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008484:	48 8d 48 04          	lea    rcx,[rax+0x4]
   140008488:	48 89 4d e0          	mov    QWORD PTR [rbp-0x20],rcx
   14000848c:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000848e:	89 10                	mov    DWORD PTR [rax],edx
   140008490:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008494:	48 3b 45 c8          	cmp    rax,QWORD PTR [rbp-0x38]
   140008498:	72 da                	jb     140008474 <__lshift_D2A+0x144>
   14000849a:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000849d:	8d 50 ff             	lea    edx,[rax-0x1]
   1400084a0:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400084a4:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   1400084a7:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400084ab:	48 89 c1             	mov    rcx,rax
   1400084ae:	e8 9b f8 ff ff       	call   140007d4e <__Bfree_D2A>
   1400084b3:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400084b7:	48 83 c4 60          	add    rsp,0x60
   1400084bb:	5d                   	pop    rbp
   1400084bc:	c3                   	ret

00000001400084bd <__cmp_D2A>:
   1400084bd:	55                   	push   rbp
   1400084be:	48 89 e5             	mov    rbp,rsp
   1400084c1:	48 83 ec 30          	sub    rsp,0x30
   1400084c5:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400084c9:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400084cd:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400084d1:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400084d4:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   1400084d7:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400084db:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400084de:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   1400084e1:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   1400084e4:	29 45 ec             	sub    DWORD PTR [rbp-0x14],eax
   1400084e7:	83 7d ec 00          	cmp    DWORD PTR [rbp-0x14],0x0
   1400084eb:	74 08                	je     1400084f5 <__cmp_D2A+0x38>
   1400084ed:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
   1400084f0:	e9 92 00 00 00       	jmp    140008587 <__cmp_D2A+0xca>
   1400084f5:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400084f9:	48 83 c0 18          	add    rax,0x18
   1400084fd:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140008501:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140008504:	48 98                	cdqe
   140008506:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   14000850d:	00 
   14000850e:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008512:	48 01 d0             	add    rax,rdx
   140008515:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008519:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000851d:	48 83 c0 18          	add    rax,0x18
   140008521:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140008525:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140008528:	48 98                	cdqe
   14000852a:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140008531:	00 
   140008532:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140008536:	48 01 d0             	add    rax,rdx
   140008539:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000853d:	48 83 6d f8 04       	sub    QWORD PTR [rbp-0x8],0x4
   140008542:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008546:	8b 10                	mov    edx,DWORD PTR [rax]
   140008548:	48 83 6d f0 04       	sub    QWORD PTR [rbp-0x10],0x4
   14000854d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008551:	8b 00                	mov    eax,DWORD PTR [rax]
   140008553:	39 c2                	cmp    edx,eax
   140008555:	74 1e                	je     140008575 <__cmp_D2A+0xb8>
   140008557:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000855b:	8b 10                	mov    edx,DWORD PTR [rax]
   14000855d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008561:	8b 00                	mov    eax,DWORD PTR [rax]
   140008563:	39 c2                	cmp    edx,eax
   140008565:	73 07                	jae    14000856e <__cmp_D2A+0xb1>
   140008567:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000856c:	eb 19                	jmp    140008587 <__cmp_D2A+0xca>
   14000856e:	b8 01 00 00 00       	mov    eax,0x1
   140008573:	eb 12                	jmp    140008587 <__cmp_D2A+0xca>
   140008575:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008579:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   14000857d:	73 02                	jae    140008581 <__cmp_D2A+0xc4>
   14000857f:	eb bc                	jmp    14000853d <__cmp_D2A+0x80>
   140008581:	90                   	nop
   140008582:	b8 00 00 00 00       	mov    eax,0x0
   140008587:	48 83 c4 30          	add    rsp,0x30
   14000858b:	5d                   	pop    rbp
   14000858c:	c3                   	ret

000000014000858d <__diff_D2A>:
   14000858d:	55                   	push   rbp
   14000858e:	48 89 e5             	mov    rbp,rsp
   140008591:	48 83 ec 70          	sub    rsp,0x70
   140008595:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008599:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000859d:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400085a1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400085a5:	48 89 c1             	mov    rcx,rax
   1400085a8:	e8 10 ff ff ff       	call   1400084bd <__cmp_D2A>
   1400085ad:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400085b0:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   1400085b4:	75 3e                	jne    1400085f4 <__diff_D2A+0x67>
   1400085b6:	b9 00 00 00 00       	mov    ecx,0x0
   1400085bb:	e8 4d f6 ff ff       	call   140007c0d <__Balloc_D2A>
   1400085c0:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   1400085c4:	48 83 7d d0 00       	cmp    QWORD PTR [rbp-0x30],0x0
   1400085c9:	75 0a                	jne    1400085d5 <__diff_D2A+0x48>
   1400085cb:	b8 00 00 00 00       	mov    eax,0x0
   1400085d0:	e9 ab 01 00 00       	jmp    140008780 <__diff_D2A+0x1f3>
   1400085d5:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400085d9:	c7 40 14 01 00 00 00 	mov    DWORD PTR [rax+0x14],0x1
   1400085e0:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400085e4:	c7 40 18 00 00 00 00 	mov    DWORD PTR [rax+0x18],0x0
   1400085eb:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400085ef:	e9 8c 01 00 00       	jmp    140008780 <__diff_D2A+0x1f3>
   1400085f4:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   1400085f8:	79 21                	jns    14000861b <__diff_D2A+0x8e>
   1400085fa:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400085fe:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140008602:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140008606:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   14000860a:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   14000860e:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140008612:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   140008619:	eb 07                	jmp    140008622 <__diff_D2A+0x95>
   14000861b:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140008622:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008626:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140008629:	89 c1                	mov    ecx,eax
   14000862b:	e8 dd f5 ff ff       	call   140007c0d <__Balloc_D2A>
   140008630:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140008634:	48 83 7d d0 00       	cmp    QWORD PTR [rbp-0x30],0x0
   140008639:	75 0a                	jne    140008645 <__diff_D2A+0xb8>
   14000863b:	b8 00 00 00 00       	mov    eax,0x0
   140008640:	e9 3b 01 00 00       	jmp    140008780 <__diff_D2A+0x1f3>
   140008645:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140008649:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   14000864c:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   14000864f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008653:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140008656:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008659:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000865d:	48 83 c0 18          	add    rax,0x18
   140008661:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140008665:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008668:	48 98                	cdqe
   14000866a:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140008671:	00 
   140008672:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008676:	48 01 d0             	add    rax,rdx
   140008679:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   14000867d:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140008681:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140008684:	89 45 c4             	mov    DWORD PTR [rbp-0x3c],eax
   140008687:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000868b:	48 83 c0 18          	add    rax,0x18
   14000868f:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140008693:	8b 45 c4             	mov    eax,DWORD PTR [rbp-0x3c]
   140008696:	48 98                	cdqe
   140008698:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   14000869f:	00 
   1400086a0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400086a4:	48 01 d0             	add    rax,rdx
   1400086a7:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400086ab:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400086af:	48 83 c0 18          	add    rax,0x18
   1400086b3:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400086b7:	48 c7 45 d8 00 00 00 	mov    QWORD PTR [rbp-0x28],0x0
   1400086be:	00 
   1400086bf:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400086c3:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400086c7:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400086cb:	8b 00                	mov    eax,DWORD PTR [rax]
   1400086cd:	89 c1                	mov    ecx,eax
   1400086cf:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400086d3:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400086d7:	48 89 55 e8          	mov    QWORD PTR [rbp-0x18],rdx
   1400086db:	8b 00                	mov    eax,DWORD PTR [rax]
   1400086dd:	89 c2                	mov    edx,eax
   1400086df:	48 89 c8             	mov    rax,rcx
   1400086e2:	48 29 d0             	sub    rax,rdx
   1400086e5:	48 2b 45 d8          	sub    rax,QWORD PTR [rbp-0x28]
   1400086e9:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   1400086ed:	48 8b 45 b0          	mov    rax,QWORD PTR [rbp-0x50]
   1400086f1:	48 c1 e8 20          	shr    rax,0x20
   1400086f5:	83 e0 01             	and    eax,0x1
   1400086f8:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   1400086fc:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008700:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140008704:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   140008708:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   14000870c:	89 10                	mov    DWORD PTR [rax],edx
   14000870e:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008712:	48 3b 45 b8          	cmp    rax,QWORD PTR [rbp-0x48]
   140008716:	72 a7                	jb     1400086bf <__diff_D2A+0x132>
   140008718:	eb 39                	jmp    140008753 <__diff_D2A+0x1c6>
   14000871a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000871e:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140008722:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140008726:	8b 00                	mov    eax,DWORD PTR [rax]
   140008728:	89 c0                	mov    eax,eax
   14000872a:	48 2b 45 d8          	sub    rax,QWORD PTR [rbp-0x28]
   14000872e:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140008732:	48 8b 45 b0          	mov    rax,QWORD PTR [rbp-0x50]
   140008736:	48 c1 e8 20          	shr    rax,0x20
   14000873a:	83 e0 01             	and    eax,0x1
   14000873d:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140008741:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008745:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140008749:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   14000874d:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   140008751:	89 10                	mov    DWORD PTR [rax],edx
   140008753:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008757:	48 3b 45 c8          	cmp    rax,QWORD PTR [rbp-0x38]
   14000875b:	72 bd                	jb     14000871a <__diff_D2A+0x18d>
   14000875d:	eb 04                	jmp    140008763 <__diff_D2A+0x1d6>
   14000875f:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   140008763:	48 83 6d e0 04       	sub    QWORD PTR [rbp-0x20],0x4
   140008768:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   14000876c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000876e:	85 c0                	test   eax,eax
   140008770:	74 ed                	je     14000875f <__diff_D2A+0x1d2>
   140008772:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140008776:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140008779:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   14000877c:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140008780:	48 83 c4 70          	add    rsp,0x70
   140008784:	5d                   	pop    rbp
   140008785:	c3                   	ret

0000000140008786 <__b2d_D2A>:
   140008786:	55                   	push   rbp
   140008787:	48 89 e5             	mov    rbp,rsp
   14000878a:	48 83 ec 50          	sub    rsp,0x50
   14000878e:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008792:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008796:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000879a:	48 83 c0 18          	add    rax,0x18
   14000879e:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400087a2:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400087a6:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400087a9:	48 98                	cdqe
   1400087ab:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   1400087b2:	00 
   1400087b3:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400087b7:	48 01 d0             	add    rax,rdx
   1400087ba:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400087be:	48 83 6d f8 04       	sub    QWORD PTR [rbp-0x8],0x4
   1400087c3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400087c7:	8b 00                	mov    eax,DWORD PTR [rax]
   1400087c9:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   1400087cc:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   1400087cf:	89 c1                	mov    ecx,eax
   1400087d1:	e8 27 f4 ff ff       	call   140007bfd <__hi0bits_D2A>
   1400087d6:	89 45 dc             	mov    DWORD PTR [rbp-0x24],eax
   1400087d9:	b8 20 00 00 00       	mov    eax,0x20
   1400087de:	2b 45 dc             	sub    eax,DWORD PTR [rbp-0x24]
   1400087e1:	89 c2                	mov    edx,eax
   1400087e3:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400087e7:	89 10                	mov    DWORD PTR [rax],edx
   1400087e9:	83 7d dc 0a          	cmp    DWORD PTR [rbp-0x24],0xa
   1400087ed:	7f 66                	jg     140008855 <__b2d_D2A+0xcf>
   1400087ef:	b8 0b 00 00 00       	mov    eax,0xb
   1400087f4:	2b 45 dc             	sub    eax,DWORD PTR [rbp-0x24]
   1400087f7:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   1400087fa:	89 c1                	mov    ecx,eax
   1400087fc:	d3 ea                	shr    edx,cl
   1400087fe:	89 d0                	mov    eax,edx
   140008800:	0d 00 00 f0 3f       	or     eax,0x3ff00000
   140008805:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   140008808:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000880c:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   140008810:	73 10                	jae    140008822 <__b2d_D2A+0x9c>
   140008812:	48 83 6d f8 04       	sub    QWORD PTR [rbp-0x8],0x4
   140008817:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000881b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000881d:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140008820:	eb 07                	jmp    140008829 <__b2d_D2A+0xa3>
   140008822:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140008829:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   14000882c:	83 c0 15             	add    eax,0x15
   14000882f:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   140008832:	89 c1                	mov    ecx,eax
   140008834:	d3 e2                	shl    edx,cl
   140008836:	41 89 d0             	mov    r8d,edx
   140008839:	b8 0b 00 00 00       	mov    eax,0xb
   14000883e:	2b 45 dc             	sub    eax,DWORD PTR [rbp-0x24]
   140008841:	8b 55 f4             	mov    edx,DWORD PTR [rbp-0xc]
   140008844:	89 c1                	mov    ecx,eax
   140008846:	d3 ea                	shr    edx,cl
   140008848:	89 d0                	mov    eax,edx
   14000884a:	44 09 c0             	or     eax,r8d
   14000884d:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   140008850:	e9 ac 00 00 00       	jmp    140008901 <__b2d_D2A+0x17b>
   140008855:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008859:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   14000885d:	73 10                	jae    14000886f <__b2d_D2A+0xe9>
   14000885f:	48 83 6d f8 04       	sub    QWORD PTR [rbp-0x8],0x4
   140008864:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008868:	8b 00                	mov    eax,DWORD PTR [rax]
   14000886a:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   14000886d:	eb 07                	jmp    140008876 <__b2d_D2A+0xf0>
   14000886f:	c7 45 ec 00 00 00 00 	mov    DWORD PTR [rbp-0x14],0x0
   140008876:	83 6d dc 0b          	sub    DWORD PTR [rbp-0x24],0xb
   14000887a:	83 7d dc 00          	cmp    DWORD PTR [rbp-0x24],0x0
   14000887e:	74 70                	je     1400088f0 <__b2d_D2A+0x16a>
   140008880:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   140008883:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   140008886:	89 c1                	mov    ecx,eax
   140008888:	d3 e2                	shl    edx,cl
   14000888a:	41 89 d0             	mov    r8d,edx
   14000888d:	b8 20 00 00 00       	mov    eax,0x20
   140008892:	2b 45 dc             	sub    eax,DWORD PTR [rbp-0x24]
   140008895:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   140008898:	89 c1                	mov    ecx,eax
   14000889a:	d3 ea                	shr    edx,cl
   14000889c:	89 d0                	mov    eax,edx
   14000889e:	44 09 c0             	or     eax,r8d
   1400088a1:	0d 00 00 f0 3f       	or     eax,0x3ff00000
   1400088a6:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   1400088a9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400088ad:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   1400088b1:	73 10                	jae    1400088c3 <__b2d_D2A+0x13d>
   1400088b3:	48 83 6d f8 04       	sub    QWORD PTR [rbp-0x8],0x4
   1400088b8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400088bc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400088be:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   1400088c1:	eb 07                	jmp    1400088ca <__b2d_D2A+0x144>
   1400088c3:	c7 45 f0 00 00 00 00 	mov    DWORD PTR [rbp-0x10],0x0
   1400088ca:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   1400088cd:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   1400088d0:	89 c1                	mov    ecx,eax
   1400088d2:	d3 e2                	shl    edx,cl
   1400088d4:	41 89 d0             	mov    r8d,edx
   1400088d7:	b8 20 00 00 00       	mov    eax,0x20
   1400088dc:	2b 45 dc             	sub    eax,DWORD PTR [rbp-0x24]
   1400088df:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   1400088e2:	89 c1                	mov    ecx,eax
   1400088e4:	d3 ea                	shr    edx,cl
   1400088e6:	89 d0                	mov    eax,edx
   1400088e8:	44 09 c0             	or     eax,r8d
   1400088eb:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   1400088ee:	eb 11                	jmp    140008901 <__b2d_D2A+0x17b>
   1400088f0:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   1400088f3:	0d 00 00 f0 3f       	or     eax,0x3ff00000
   1400088f8:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   1400088fb:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
   1400088fe:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   140008901:	f2 0f 10 45 d0       	movsd  xmm0,QWORD PTR [rbp-0x30]
   140008906:	48 83 c4 50          	add    rsp,0x50
   14000890a:	5d                   	pop    rbp
   14000890b:	c3                   	ret

000000014000890c <__d2b_D2A>:
   14000890c:	55                   	push   rbp
   14000890d:	53                   	push   rbx
   14000890e:	48 83 ec 58          	sub    rsp,0x58
   140008912:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140008917:	f2 0f 11 45 20       	movsd  QWORD PTR [rbp+0x20],xmm0
   14000891c:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140008920:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140008924:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   140008929:	f2 0f 11 45 d8       	movsd  QWORD PTR [rbp-0x28],xmm0
   14000892e:	b9 01 00 00 00       	mov    ecx,0x1
   140008933:	e8 d5 f2 ff ff       	call   140007c0d <__Balloc_D2A>
   140008938:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000893c:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140008941:	75 0a                	jne    14000894d <__d2b_D2A+0x41>
   140008943:	b8 00 00 00 00       	mov    eax,0x0
   140008948:	e9 68 01 00 00       	jmp    140008ab5 <__d2b_D2A+0x1a9>
   14000894d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008951:	48 83 c0 18          	add    rax,0x18
   140008955:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140008959:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   14000895c:	25 ff ff 0f 00       	and    eax,0xfffff
   140008961:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   140008964:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   140008967:	25 ff ff ff 7f       	and    eax,0x7fffffff
   14000896c:	89 45 dc             	mov    DWORD PTR [rbp-0x24],eax
   14000896f:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   140008972:	c1 e8 14             	shr    eax,0x14
   140008975:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140008978:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   14000897c:	74 0b                	je     140008989 <__d2b_D2A+0x7d>
   14000897e:	8b 45 d0             	mov    eax,DWORD PTR [rbp-0x30]
   140008981:	0d 00 00 10 00       	or     eax,0x100000
   140008986:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   140008989:	8b 45 d8             	mov    eax,DWORD PTR [rbp-0x28]
   14000898c:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   14000898f:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140008992:	85 c0                	test   eax,eax
   140008994:	74 7b                	je     140008a11 <__d2b_D2A+0x105>
   140008996:	48 8d 45 d4          	lea    rax,[rbp-0x2c]
   14000899a:	48 89 c1             	mov    rcx,rax
   14000899d:	e8 26 f2 ff ff       	call   140007bc8 <__lo0bits_D2A>
   1400089a2:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   1400089a5:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   1400089a9:	74 2b                	je     1400089d6 <__d2b_D2A+0xca>
   1400089ab:	8b 55 d0             	mov    edx,DWORD PTR [rbp-0x30]
   1400089ae:	b8 20 00 00 00       	mov    eax,0x20
   1400089b3:	2b 45 f8             	sub    eax,DWORD PTR [rbp-0x8]
   1400089b6:	89 c1                	mov    ecx,eax
   1400089b8:	d3 e2                	shl    edx,cl
   1400089ba:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400089bd:	09 c2                	or     edx,eax
   1400089bf:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400089c3:	89 10                	mov    DWORD PTR [rax],edx
   1400089c5:	8b 55 d0             	mov    edx,DWORD PTR [rbp-0x30]
   1400089c8:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   1400089cb:	89 c1                	mov    ecx,eax
   1400089cd:	d3 ea                	shr    edx,cl
   1400089cf:	89 d0                	mov    eax,edx
   1400089d1:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   1400089d4:	eb 09                	jmp    1400089df <__d2b_D2A+0xd3>
   1400089d6:	8b 55 d4             	mov    edx,DWORD PTR [rbp-0x2c]
   1400089d9:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400089dd:	89 10                	mov    DWORD PTR [rax],edx
   1400089df:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400089e3:	48 83 c0 04          	add    rax,0x4
   1400089e7:	8b 55 d0             	mov    edx,DWORD PTR [rbp-0x30]
   1400089ea:	89 10                	mov    DWORD PTR [rax],edx
   1400089ec:	8b 00                	mov    eax,DWORD PTR [rax]
   1400089ee:	85 c0                	test   eax,eax
   1400089f0:	74 07                	je     1400089f9 <__d2b_D2A+0xed>
   1400089f2:	ba 02 00 00 00       	mov    edx,0x2
   1400089f7:	eb 05                	jmp    1400089fe <__d2b_D2A+0xf2>
   1400089f9:	ba 01 00 00 00       	mov    edx,0x1
   1400089fe:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008a02:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140008a05:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008a09:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140008a0c:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008a0f:	eb 31                	jmp    140008a42 <__d2b_D2A+0x136>
   140008a11:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   140008a15:	48 89 c1             	mov    rcx,rax
   140008a18:	e8 ab f1 ff ff       	call   140007bc8 <__lo0bits_D2A>
   140008a1d:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008a20:	8b 55 d0             	mov    edx,DWORD PTR [rbp-0x30]
   140008a23:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008a27:	89 10                	mov    DWORD PTR [rax],edx
   140008a29:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008a2d:	c7 40 14 01 00 00 00 	mov    DWORD PTR [rax+0x14],0x1
   140008a34:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008a38:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140008a3b:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008a3e:	83 45 f8 20          	add    DWORD PTR [rbp-0x8],0x20
   140008a42:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140008a46:	74 26                	je     140008a6e <__d2b_D2A+0x162>
   140008a48:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140008a4b:	8d 90 cd fb ff ff    	lea    edx,[rax-0x433]
   140008a51:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008a54:	01 c2                	add    edx,eax
   140008a56:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140008a5a:	89 10                	mov    DWORD PTR [rax],edx
   140008a5c:	b8 35 00 00 00       	mov    eax,0x35
   140008a61:	2b 45 f8             	sub    eax,DWORD PTR [rbp-0x8]
   140008a64:	89 c2                	mov    edx,eax
   140008a66:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140008a6a:	89 10                	mov    DWORD PTR [rax],edx
   140008a6c:	eb 43                	jmp    140008ab1 <__d2b_D2A+0x1a5>
   140008a6e:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140008a71:	8d 90 ce fb ff ff    	lea    edx,[rax-0x432]
   140008a77:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008a7a:	01 c2                	add    edx,eax
   140008a7c:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140008a80:	89 10                	mov    DWORD PTR [rax],edx
   140008a82:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008a85:	c1 e0 05             	shl    eax,0x5
   140008a88:	89 c3                	mov    ebx,eax
   140008a8a:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008a8d:	48 98                	cdqe
   140008a8f:	48 c1 e0 02          	shl    rax,0x2
   140008a93:	48 8d 50 fc          	lea    rdx,[rax-0x4]
   140008a97:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008a9b:	48 01 d0             	add    rax,rdx
   140008a9e:	8b 00                	mov    eax,DWORD PTR [rax]
   140008aa0:	89 c1                	mov    ecx,eax
   140008aa2:	e8 56 f1 ff ff       	call   140007bfd <__hi0bits_D2A>
   140008aa7:	29 c3                	sub    ebx,eax
   140008aa9:	89 da                	mov    edx,ebx
   140008aab:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140008aaf:	89 10                	mov    DWORD PTR [rax],edx
   140008ab1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008ab5:	48 83 c4 58          	add    rsp,0x58
   140008ab9:	5b                   	pop    rbx
   140008aba:	5d                   	pop    rbp
   140008abb:	c3                   	ret

0000000140008abc <__strcp_D2A>:
   140008abc:	55                   	push   rbp
   140008abd:	48 89 e5             	mov    rbp,rsp
   140008ac0:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008ac4:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008ac8:	eb 05                	jmp    140008acf <__strcp_D2A+0x13>
   140008aca:	48 83 45 10 01       	add    QWORD PTR [rbp+0x10],0x1
   140008acf:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140008ad3:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140008ad7:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008adb:	0f b6 10             	movzx  edx,BYTE PTR [rax]
   140008ade:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008ae2:	88 10                	mov    BYTE PTR [rax],dl
   140008ae4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008ae8:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140008aeb:	84 c0                	test   al,al
   140008aed:	75 db                	jne    140008aca <__strcp_D2A+0xe>
   140008aef:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008af3:	5d                   	pop    rbp
   140008af4:	c3                   	ret
   140008af5:	90                   	nop
   140008af6:	90                   	nop
   140008af7:	90                   	nop
   140008af8:	90                   	nop
   140008af9:	90                   	nop
   140008afa:	90                   	nop
   140008afb:	90                   	nop
   140008afc:	90                   	nop
   140008afd:	90                   	nop
   140008afe:	90                   	nop
   140008aff:	90                   	nop

0000000140008b00 <__fpclassify>:
   140008b00:	55                   	push   rbp
   140008b01:	48 89 e5             	mov    rbp,rsp
   140008b04:	48 83 ec 10          	sub    rsp,0x10
   140008b08:	f2 0f 11 45 10       	movsd  QWORD PTR [rbp+0x10],xmm0
   140008b0d:	f2 0f 10 45 10       	movsd  xmm0,QWORD PTR [rbp+0x10]
   140008b12:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   140008b17:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140008b1a:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008b1d:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140008b20:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   140008b23:	81 e2 ff ff 0f 00    	and    edx,0xfffff
   140008b29:	09 d0                	or     eax,edx
   140008b2b:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008b2e:	81 65 fc 00 00 f0 7f 	and    DWORD PTR [rbp-0x4],0x7ff00000
   140008b35:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008b38:	0b 45 f8             	or     eax,DWORD PTR [rbp-0x8]
   140008b3b:	85 c0                	test   eax,eax
   140008b3d:	75 07                	jne    140008b46 <__fpclassify+0x46>
   140008b3f:	b8 00 40 00 00       	mov    eax,0x4000
   140008b44:	eb 2f                	jmp    140008b75 <__fpclassify+0x75>
   140008b46:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140008b4a:	75 07                	jne    140008b53 <__fpclassify+0x53>
   140008b4c:	b8 00 44 00 00       	mov    eax,0x4400
   140008b51:	eb 22                	jmp    140008b75 <__fpclassify+0x75>
   140008b53:	81 7d fc 00 00 f0 7f 	cmp    DWORD PTR [rbp-0x4],0x7ff00000
   140008b5a:	75 14                	jne    140008b70 <__fpclassify+0x70>
   140008b5c:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140008b60:	74 07                	je     140008b69 <__fpclassify+0x69>
   140008b62:	b8 00 01 00 00       	mov    eax,0x100
   140008b67:	eb 0c                	jmp    140008b75 <__fpclassify+0x75>
   140008b69:	b8 00 05 00 00       	mov    eax,0x500
   140008b6e:	eb 05                	jmp    140008b75 <__fpclassify+0x75>
   140008b70:	b8 00 04 00 00       	mov    eax,0x400
   140008b75:	48 83 c4 10          	add    rsp,0x10
   140008b79:	5d                   	pop    rbp
   140008b7a:	c3                   	ret
   140008b7b:	90                   	nop
   140008b7c:	90                   	nop
   140008b7d:	90                   	nop
   140008b7e:	90                   	nop
   140008b7f:	90                   	nop

0000000140008b80 <__fpclassifyl>:
   140008b80:	55                   	push   rbp
   140008b81:	53                   	push   rbx
   140008b82:	48 83 ec 38          	sub    rsp,0x38
   140008b86:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140008b8b:	48 89 cb             	mov    rbx,rcx
   140008b8e:	db 2b                	fld    TBYTE PTR [rbx]
   140008b90:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140008b93:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140008b96:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   140008b99:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140008b9d:	98                   	cwde
   140008b9e:	25 ff 7f 00 00       	and    eax,0x7fff
   140008ba3:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008ba6:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140008baa:	75 25                	jne    140008bd1 <__fpclassifyl+0x51>
   140008bac:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140008baf:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008bb2:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
   140008bb5:	0b 45 f8             	or     eax,DWORD PTR [rbp-0x8]
   140008bb8:	85 c0                	test   eax,eax
   140008bba:	75 07                	jne    140008bc3 <__fpclassifyl+0x43>
   140008bbc:	b8 00 40 00 00       	mov    eax,0x4000
   140008bc1:	eb 3d                	jmp    140008c00 <__fpclassifyl+0x80>
   140008bc3:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008bc6:	85 c0                	test   eax,eax
   140008bc8:	78 31                	js     140008bfb <__fpclassifyl+0x7b>
   140008bca:	b8 00 44 00 00       	mov    eax,0x4400
   140008bcf:	eb 2f                	jmp    140008c00 <__fpclassifyl+0x80>
   140008bd1:	81 7d fc ff 7f 00 00 	cmp    DWORD PTR [rbp-0x4],0x7fff
   140008bd8:	75 21                	jne    140008bfb <__fpclassifyl+0x7b>
   140008bda:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140008bdd:	25 ff ff ff 7f       	and    eax,0x7fffffff
   140008be2:	89 c2                	mov    edx,eax
   140008be4:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
   140008be7:	09 d0                	or     eax,edx
   140008be9:	85 c0                	test   eax,eax
   140008beb:	75 07                	jne    140008bf4 <__fpclassifyl+0x74>
   140008bed:	b8 00 05 00 00       	mov    eax,0x500
   140008bf2:	eb 0c                	jmp    140008c00 <__fpclassifyl+0x80>
   140008bf4:	b8 00 01 00 00       	mov    eax,0x100
   140008bf9:	eb 05                	jmp    140008c00 <__fpclassifyl+0x80>
   140008bfb:	b8 00 04 00 00       	mov    eax,0x400
   140008c00:	48 83 c4 38          	add    rsp,0x38
   140008c04:	5b                   	pop    rbx
   140008c05:	5d                   	pop    rbp
   140008c06:	c3                   	ret
   140008c07:	90                   	nop
   140008c08:	90                   	nop
   140008c09:	90                   	nop
   140008c0a:	90                   	nop
   140008c0b:	90                   	nop
   140008c0c:	90                   	nop
   140008c0d:	90                   	nop
   140008c0e:	90                   	nop
   140008c0f:	90                   	nop

0000000140008c10 <__isnan>:
   140008c10:	55                   	push   rbp
   140008c11:	48 89 e5             	mov    rbp,rsp
   140008c14:	48 83 ec 10          	sub    rsp,0x10
   140008c18:	f2 0f 11 45 10       	movsd  QWORD PTR [rbp+0x10],xmm0
   140008c1d:	f2 0f 10 45 10       	movsd  xmm0,QWORD PTR [rbp+0x10]
   140008c22:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   140008c27:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140008c2a:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008c2d:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140008c30:	25 ff ff ff 7f       	and    eax,0x7fffffff
   140008c35:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008c38:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008c3b:	f7 d8                	neg    eax
   140008c3d:	0b 45 fc             	or     eax,DWORD PTR [rbp-0x4]
   140008c40:	c1 e8 1f             	shr    eax,0x1f
   140008c43:	89 c2                	mov    edx,eax
   140008c45:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008c48:	09 d0                	or     eax,edx
   140008c4a:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008c4d:	b8 00 00 f0 7f       	mov    eax,0x7ff00000
   140008c52:	2b 45 f8             	sub    eax,DWORD PTR [rbp-0x8]
   140008c55:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008c58:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008c5b:	c1 f8 1f             	sar    eax,0x1f
   140008c5e:	48 83 c4 10          	add    rsp,0x10
   140008c62:	5d                   	pop    rbp
   140008c63:	c3                   	ret
   140008c64:	90                   	nop
   140008c65:	90                   	nop
   140008c66:	90                   	nop
   140008c67:	90                   	nop
   140008c68:	90                   	nop
   140008c69:	90                   	nop
   140008c6a:	90                   	nop
   140008c6b:	90                   	nop
   140008c6c:	90                   	nop
   140008c6d:	90                   	nop
   140008c6e:	90                   	nop
   140008c6f:	90                   	nop

0000000140008c70 <__isnanl>:
   140008c70:	55                   	push   rbp
   140008c71:	53                   	push   rbx
   140008c72:	48 83 ec 38          	sub    rsp,0x38
   140008c76:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140008c7b:	48 89 cb             	mov    rbx,rcx
   140008c7e:	db 2b                	fld    TBYTE PTR [rbx]
   140008c80:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140008c83:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140008c86:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   140008c89:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140008c8d:	98                   	cwde
   140008c8e:	01 c0                	add    eax,eax
   140008c90:	25 ff ff 00 00       	and    eax,0xffff
   140008c95:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008c98:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
   140008c9b:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   140008c9e:	81 e2 ff ff ff 7f    	and    edx,0x7fffffff
   140008ca4:	09 d0                	or     eax,edx
   140008ca6:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008ca9:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008cac:	f7 d8                	neg    eax
   140008cae:	0b 45 f8             	or     eax,DWORD PTR [rbp-0x8]
   140008cb1:	c1 e8 1f             	shr    eax,0x1f
   140008cb4:	89 c2                	mov    edx,eax
   140008cb6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008cb9:	09 d0                	or     eax,edx
   140008cbb:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008cbe:	b8 fe ff 00 00       	mov    eax,0xfffe
   140008cc3:	2b 45 fc             	sub    eax,DWORD PTR [rbp-0x4]
   140008cc6:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008cc9:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008ccc:	c1 f8 10             	sar    eax,0x10
   140008ccf:	48 83 c4 38          	add    rsp,0x38
   140008cd3:	5b                   	pop    rbx
   140008cd4:	5d                   	pop    rbp
   140008cd5:	c3                   	ret
   140008cd6:	90                   	nop
   140008cd7:	90                   	nop
   140008cd8:	90                   	nop
   140008cd9:	90                   	nop
   140008cda:	90                   	nop
   140008cdb:	90                   	nop
   140008cdc:	90                   	nop
   140008cdd:	90                   	nop
   140008cde:	90                   	nop
   140008cdf:	90                   	nop

0000000140008ce0 <wcsnlen>:
   140008ce0:	55                   	push   rbp
   140008ce1:	48 89 e5             	mov    rbp,rsp
   140008ce4:	48 83 ec 10          	sub    rsp,0x10
   140008ce8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008cec:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008cf0:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   140008cf7:	00 
   140008cf8:	eb 0a                	jmp    140008d04 <wcsnlen+0x24>
   140008cfa:	48 83 45 f8 01       	add    QWORD PTR [rbp-0x8],0x1
   140008cff:	48 83 45 10 02       	add    QWORD PTR [rbp+0x10],0x2
   140008d04:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d08:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140008d0c:	73 0c                	jae    140008d1a <wcsnlen+0x3a>
   140008d0e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008d12:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140008d15:	66 85 c0             	test   ax,ax
   140008d18:	75 e0                	jne    140008cfa <wcsnlen+0x1a>
   140008d1a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d1e:	48 83 c4 10          	add    rsp,0x10
   140008d22:	5d                   	pop    rbp
   140008d23:	c3                   	ret
   140008d24:	90                   	nop
   140008d25:	90                   	nop
   140008d26:	90                   	nop
   140008d27:	90                   	nop
   140008d28:	90                   	nop
   140008d29:	90                   	nop
   140008d2a:	90                   	nop
   140008d2b:	90                   	nop
   140008d2c:	90                   	nop
   140008d2d:	90                   	nop
   140008d2e:	90                   	nop
   140008d2f:	90                   	nop

0000000140008d30 <strnlen>:
   140008d30:	55                   	push   rbp
   140008d31:	48 89 e5             	mov    rbp,rsp
   140008d34:	48 83 ec 10          	sub    rsp,0x10
   140008d38:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008d3c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008d40:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008d44:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008d48:	eb 05                	jmp    140008d4f <strnlen+0x1f>
   140008d4a:	48 83 45 f8 01       	add    QWORD PTR [rbp-0x8],0x1
   140008d4f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d53:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   140008d57:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140008d5b:	73 0b                	jae    140008d68 <strnlen+0x38>
   140008d5d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d61:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140008d64:	84 c0                	test   al,al
   140008d66:	75 e2                	jne    140008d4a <strnlen+0x1a>
   140008d68:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d6c:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   140008d70:	48 83 c4 10          	add    rsp,0x10
   140008d74:	5d                   	pop    rbp
   140008d75:	c3                   	ret
   140008d76:	90                   	nop
   140008d77:	90                   	nop
   140008d78:	90                   	nop
   140008d79:	90                   	nop
   140008d7a:	90                   	nop
   140008d7b:	90                   	nop
   140008d7c:	90                   	nop
   140008d7d:	90                   	nop
   140008d7e:	90                   	nop
   140008d7f:	90                   	nop

0000000140008d80 <_initterm_e>:
   140008d80:	55                   	push   rbp
   140008d81:	48 89 e5             	mov    rbp,rsp
   140008d84:	48 83 ec 30          	sub    rsp,0x30
   140008d88:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008d8c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008d90:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008d94:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008d98:	eb 29                	jmp    140008dc3 <_initterm_e+0x43>
   140008d9a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d9e:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008da1:	48 85 c0             	test   rax,rax
   140008da4:	74 17                	je     140008dbd <_initterm_e+0x3d>
   140008da6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008daa:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008dad:	ff d0                	call   rax
   140008daf:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140008db2:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   140008db6:	74 06                	je     140008dbe <_initterm_e+0x3e>
   140008db8:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140008dbb:	eb 15                	jmp    140008dd2 <_initterm_e+0x52>
   140008dbd:	90                   	nop
   140008dbe:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140008dc3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008dc7:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140008dcb:	72 cd                	jb     140008d9a <_initterm_e+0x1a>
   140008dcd:	b8 00 00 00 00       	mov    eax,0x0
   140008dd2:	48 83 c4 30          	add    rsp,0x30
   140008dd6:	5d                   	pop    rbp
   140008dd7:	c3                   	ret
   140008dd8:	90                   	nop
   140008dd9:	90                   	nop
   140008dda:	90                   	nop
   140008ddb:	90                   	nop
   140008ddc:	90                   	nop
   140008ddd:	90                   	nop
   140008dde:	90                   	nop
   140008ddf:	90                   	nop

0000000140008de0 <__p__fmode>:
   140008de0:	55                   	push   rbp
   140008de1:	48 89 e5             	mov    rbp,rsp
   140008de4:	48 8b 05 15 28 00 00 	mov    rax,QWORD PTR [rip+0x2815]        # 14000b600 <.refptr.__imp__fmode>
   140008deb:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008dee:	5d                   	pop    rbp
   140008def:	c3                   	ret

0000000140008df0 <__p__commode>:
   140008df0:	55                   	push   rbp
   140008df1:	48 89 e5             	mov    rbp,rsp
   140008df4:	48 8b 05 f5 27 00 00 	mov    rax,QWORD PTR [rip+0x27f5]        # 14000b5f0 <.refptr.__imp__commode>
   140008dfb:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008dfe:	5d                   	pop    rbp
   140008dff:	c3                   	ret

0000000140008e00 <__p___initenv>:
   140008e00:	55                   	push   rbp
   140008e01:	48 89 e5             	mov    rbp,rsp
   140008e04:	48 8b 05 d5 27 00 00 	mov    rax,QWORD PTR [rip+0x27d5]        # 14000b5e0 <.refptr.__imp___initenv>
   140008e0b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008e0e:	5d                   	pop    rbp
   140008e0f:	c3                   	ret

0000000140008e10 <_lock_file>:
   140008e10:	55                   	push   rbp
   140008e11:	48 89 e5             	mov    rbp,rsp
   140008e14:	48 83 ec 20          	sub    rsp,0x20
   140008e18:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008e1c:	b9 00 00 00 00       	mov    ecx,0x0
   140008e21:	e8 6a 01 00 00       	call   140008f90 <__acrt_iob_func>
   140008e26:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140008e2a:	72 52                	jb     140008e7e <_lock_file+0x6e>
   140008e2c:	b9 13 00 00 00       	mov    ecx,0x13
   140008e31:	e8 5a 01 00 00       	call   140008f90 <__acrt_iob_func>
   140008e36:	48 3b 45 10          	cmp    rax,QWORD PTR [rbp+0x10]
   140008e3a:	72 42                	jb     140008e7e <_lock_file+0x6e>
   140008e3c:	b9 00 00 00 00       	mov    ecx,0x0
   140008e41:	e8 4a 01 00 00       	call   140008f90 <__acrt_iob_func>
   140008e46:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140008e4a:	48 29 c2             	sub    rdx,rax
   140008e4d:	48 c1 fa 04          	sar    rdx,0x4
   140008e51:	48 b8 ab aa aa aa aa 	movabs rax,0xaaaaaaaaaaaaaaab
   140008e58:	aa aa aa 
   140008e5b:	48 0f af c2          	imul   rax,rdx
   140008e5f:	83 c0 10             	add    eax,0x10
   140008e62:	89 c1                	mov    ecx,eax
   140008e64:	e8 1f 07 00 00       	call   140009588 <_lock>
   140008e69:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008e6d:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   140008e70:	80 cc 80             	or     ah,0x80
   140008e73:	89 c2                	mov    edx,eax
   140008e75:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008e79:	89 50 18             	mov    DWORD PTR [rax+0x18],edx
   140008e7c:	eb 15                	jmp    140008e93 <_lock_file+0x83>
   140008e7e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008e82:	48 83 c0 30          	add    rax,0x30
   140008e86:	48 89 c1             	mov    rcx,rax
   140008e89:	48 8b 05 60 73 00 00 	mov    rax,QWORD PTR [rip+0x7360]        # 1400101f0 <__imp_EnterCriticalSection>
   140008e90:	ff d0                	call   rax
   140008e92:	90                   	nop
   140008e93:	90                   	nop
   140008e94:	48 83 c4 20          	add    rsp,0x20
   140008e98:	5d                   	pop    rbp
   140008e99:	c3                   	ret

0000000140008e9a <_unlock_file>:
   140008e9a:	55                   	push   rbp
   140008e9b:	48 89 e5             	mov    rbp,rsp
   140008e9e:	48 83 ec 20          	sub    rsp,0x20
   140008ea2:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008ea6:	b9 00 00 00 00       	mov    ecx,0x0
   140008eab:	e8 e0 00 00 00       	call   140008f90 <__acrt_iob_func>
   140008eb0:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140008eb4:	72 52                	jb     140008f08 <_unlock_file+0x6e>
   140008eb6:	b9 13 00 00 00       	mov    ecx,0x13
   140008ebb:	e8 d0 00 00 00       	call   140008f90 <__acrt_iob_func>
   140008ec0:	48 3b 45 10          	cmp    rax,QWORD PTR [rbp+0x10]
   140008ec4:	72 42                	jb     140008f08 <_unlock_file+0x6e>
   140008ec6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008eca:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   140008ecd:	80 e4 7f             	and    ah,0x7f
   140008ed0:	89 c2                	mov    edx,eax
   140008ed2:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008ed6:	89 50 18             	mov    DWORD PTR [rax+0x18],edx
   140008ed9:	b9 00 00 00 00       	mov    ecx,0x0
   140008ede:	e8 ad 00 00 00       	call   140008f90 <__acrt_iob_func>
   140008ee3:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140008ee7:	48 29 c2             	sub    rdx,rax
   140008eea:	48 c1 fa 04          	sar    rdx,0x4
   140008eee:	48 b8 ab aa aa aa aa 	movabs rax,0xaaaaaaaaaaaaaaab
   140008ef5:	aa aa aa 
   140008ef8:	48 0f af c2          	imul   rax,rdx
   140008efc:	83 c0 10             	add    eax,0x10
   140008eff:	89 c1                	mov    ecx,eax
   140008f01:	e8 8a 06 00 00       	call   140009590 <_unlock>
   140008f06:	eb 15                	jmp    140008f1d <_unlock_file+0x83>
   140008f08:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008f0c:	48 83 c0 30          	add    rax,0x30
   140008f10:	48 89 c1             	mov    rcx,rax
   140008f13:	48 8b 05 0e 73 00 00 	mov    rax,QWORD PTR [rip+0x730e]        # 140010228 <__imp_LeaveCriticalSection>
   140008f1a:	ff d0                	call   rax
   140008f1c:	90                   	nop
   140008f1d:	90                   	nop
   140008f1e:	48 83 c4 20          	add    rsp,0x20
   140008f22:	5d                   	pop    rbp
   140008f23:	c3                   	ret
   140008f24:	90                   	nop
   140008f25:	90                   	nop
   140008f26:	90                   	nop
   140008f27:	90                   	nop
   140008f28:	90                   	nop
   140008f29:	90                   	nop
   140008f2a:	90                   	nop
   140008f2b:	90                   	nop
   140008f2c:	90                   	nop
   140008f2d:	90                   	nop
   140008f2e:	90                   	nop
   140008f2f:	90                   	nop

0000000140008f30 <_set_invalid_parameter_handler>:
   140008f30:	55                   	push   rbp
   140008f31:	48 89 e5             	mov    rbp,rsp
   140008f34:	48 83 ec 10          	sub    rsp,0x10
   140008f38:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008f3c:	48 8d 05 3d 6c 00 00 	lea    rax,[rip+0x6c3d]        # 14000fb80 <handler>
   140008f43:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008f47:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008f4b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140008f4f:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140008f53:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008f57:	48 87 10             	xchg   QWORD PTR [rax],rdx
   140008f5a:	48 89 d0             	mov    rax,rdx
   140008f5d:	48 83 c4 10          	add    rsp,0x10
   140008f61:	5d                   	pop    rbp
   140008f62:	c3                   	ret

0000000140008f63 <_get_invalid_parameter_handler>:
   140008f63:	55                   	push   rbp
   140008f64:	48 89 e5             	mov    rbp,rsp
   140008f67:	48 8b 05 12 6c 00 00 	mov    rax,QWORD PTR [rip+0x6c12]        # 14000fb80 <handler>
   140008f6e:	5d                   	pop    rbp
   140008f6f:	c3                   	ret

0000000140008f70 <_configthreadlocale>:
   140008f70:	55                   	push   rbp
   140008f71:	48 89 e5             	mov    rbp,rsp
   140008f74:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140008f77:	83 7d 10 01          	cmp    DWORD PTR [rbp+0x10],0x1
   140008f7b:	75 07                	jne    140008f84 <_configthreadlocale+0x14>
   140008f7d:	b8 ff ff ff ff       	mov    eax,0xffffffff
   140008f82:	eb 05                	jmp    140008f89 <_configthreadlocale+0x19>
   140008f84:	b8 02 00 00 00       	mov    eax,0x2
   140008f89:	5d                   	pop    rbp
   140008f8a:	c3                   	ret
   140008f8b:	90                   	nop
   140008f8c:	90                   	nop
   140008f8d:	90                   	nop
   140008f8e:	90                   	nop
   140008f8f:	90                   	nop

0000000140008f90 <__acrt_iob_func>:
   140008f90:	55                   	push   rbp
   140008f91:	48 89 e5             	mov    rbp,rsp
   140008f94:	48 83 ec 20          	sub    rsp,0x20
   140008f98:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140008f9b:	e8 b0 05 00 00       	call   140009550 <__iob_func>
   140008fa0:	48 89 c1             	mov    rcx,rax
   140008fa3:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140008fa6:	48 89 d0             	mov    rax,rdx
   140008fa9:	48 01 c0             	add    rax,rax
   140008fac:	48 01 d0             	add    rax,rdx
   140008faf:	48 c1 e0 04          	shl    rax,0x4
   140008fb3:	48 01 c8             	add    rax,rcx
   140008fb6:	48 83 c4 20          	add    rsp,0x20
   140008fba:	5d                   	pop    rbp
   140008fbb:	c3                   	ret
   140008fbc:	90                   	nop
   140008fbd:	90                   	nop
   140008fbe:	90                   	nop
   140008fbf:	90                   	nop

0000000140008fc0 <wcrtomb>:
   140008fc0:	55                   	push   rbp
   140008fc1:	48 89 e5             	mov    rbp,rsp
   140008fc4:	48 83 ec 40          	sub    rsp,0x40
   140008fc8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008fcc:	89 d0                	mov    eax,edx
   140008fce:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140008fd2:	66 89 45 18          	mov    WORD PTR [rbp+0x18],ax
   140008fd6:	e8 5d 05 00 00       	call   140009538 <___lc_codepage_func>
   140008fdb:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008fde:	e8 5d 05 00 00       	call   140009540 <___mb_cur_max_func>
   140008fe3:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008fe6:	0f b7 55 18          	movzx  edx,WORD PTR [rbp+0x18]
   140008fea:	44 8b 4d fc          	mov    r9d,DWORD PTR [rbp-0x4]
   140008fee:	4c 8b 45 20          	mov    r8,QWORD PTR [rbp+0x20]
   140008ff2:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008ff6:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   140008ff9:	89 4c 24 20          	mov    DWORD PTR [rsp+0x20],ecx
   140008ffd:	48 89 c1             	mov    rcx,rax
   140009000:	e8 7b 00 00 00       	call   140009080 <__mingw_wcrtomb_cp>
   140009005:	48 83 c4 40          	add    rsp,0x40
   140009009:	5d                   	pop    rbp
   14000900a:	c3                   	ret
   14000900b:	90                   	nop
   14000900c:	90                   	nop
   14000900d:	90                   	nop
   14000900e:	90                   	nop
   14000900f:	90                   	nop

0000000140009010 <mbrtowc>:
   140009010:	55                   	push   rbp
   140009011:	48 89 e5             	mov    rbp,rsp
   140009014:	48 83 ec 40          	sub    rsp,0x40
   140009018:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000901c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140009020:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140009024:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140009028:	48 83 7d 28 00       	cmp    QWORD PTR [rbp+0x28],0x0
   14000902d:	75 0b                	jne    14000903a <mbrtowc+0x2a>
   14000902f:	48 8d 05 5a 6b 00 00 	lea    rax,[rip+0x6b5a]        # 14000fb90 <state_mbrtowc.0>
   140009036:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   14000903a:	e8 f9 04 00 00       	call   140009538 <___lc_codepage_func>
   14000903f:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140009042:	e8 f9 04 00 00       	call   140009540 <___mb_cur_max_func>
   140009047:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   14000904a:	4c 8b 4d 28          	mov    r9,QWORD PTR [rbp+0x28]
   14000904e:	4c 8b 45 20          	mov    r8,QWORD PTR [rbp+0x20]
   140009052:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140009056:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000905a:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   14000905d:	89 4c 24 28          	mov    DWORD PTR [rsp+0x28],ecx
   140009061:	8b 4d fc             	mov    ecx,DWORD PTR [rbp-0x4]
   140009064:	89 4c 24 20          	mov    DWORD PTR [rsp+0x20],ecx
   140009068:	48 89 c1             	mov    rcx,rax
   14000906b:	e8 70 01 00 00       	call   1400091e0 <__mingw_mbrtowc_cp>
   140009070:	48 83 c4 40          	add    rsp,0x40
   140009074:	5d                   	pop    rbp
   140009075:	c3                   	ret
   140009076:	90                   	nop
   140009077:	90                   	nop
   140009078:	90                   	nop
   140009079:	90                   	nop
   14000907a:	90                   	nop
   14000907b:	90                   	nop
   14000907c:	90                   	nop
   14000907d:	90                   	nop
   14000907e:	90                   	nop
   14000907f:	90                   	nop

0000000140009080 <__mingw_wcrtomb_cp>:
   140009080:	55                   	push   rbp
   140009081:	48 89 e5             	mov    rbp,rsp
   140009084:	48 83 ec 50          	sub    rsp,0x50
   140009088:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000908c:	89 d0                	mov    eax,edx
   14000908e:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140009092:	44 89 4d 28          	mov    DWORD PTR [rbp+0x28],r9d
   140009096:	66 89 45 18          	mov    WORD PTR [rbp+0x18],ax
   14000909a:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   14000909f:	75 1b                	jne    1400090bc <__mingw_wcrtomb_cp+0x3c>
   1400090a1:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   1400090a6:	74 0a                	je     1400090b2 <__mingw_wcrtomb_cp+0x32>
   1400090a8:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400090ac:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   1400090b2:	b8 01 00 00 00       	mov    eax,0x1
   1400090b7:	e9 17 01 00 00       	jmp    1400091d3 <__mingw_wcrtomb_cp+0x153>
   1400090bc:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   1400090c1:	74 21                	je     1400090e4 <__mingw_wcrtomb_cp+0x64>
   1400090c3:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400090c7:	8b 00                	mov    eax,DWORD PTR [rax]
   1400090c9:	85 c0                	test   eax,eax
   1400090cb:	74 17                	je     1400090e4 <__mingw_wcrtomb_cp+0x64>
   1400090cd:	e8 a6 04 00 00       	call   140009578 <_errno>
   1400090d2:	c7 00 16 00 00 00    	mov    DWORD PTR [rax],0x16
   1400090d8:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   1400090df:	e9 ef 00 00 00       	jmp    1400091d3 <__mingw_wcrtomb_cp+0x153>
   1400090e4:	0f b7 45 18          	movzx  eax,WORD PTR [rbp+0x18]
   1400090e8:	66 85 c0             	test   ax,ax
   1400090eb:	75 18                	jne    140009105 <__mingw_wcrtomb_cp+0x85>
   1400090ed:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   1400090f2:	74 07                	je     1400090fb <__mingw_wcrtomb_cp+0x7b>
   1400090f4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400090f8:	c6 00 00             	mov    BYTE PTR [rax],0x0
   1400090fb:	b8 01 00 00 00       	mov    eax,0x1
   140009100:	e9 ce 00 00 00       	jmp    1400091d3 <__mingw_wcrtomb_cp+0x153>
   140009105:	83 7d 28 00          	cmp    DWORD PTR [rbp+0x28],0x0
   140009109:	75 2b                	jne    140009136 <__mingw_wcrtomb_cp+0xb6>
   14000910b:	0f b7 45 18          	movzx  eax,WORD PTR [rbp+0x18]
   14000910f:	66 3d ff 00          	cmp    ax,0xff
   140009113:	0f 87 a4 00 00 00    	ja     1400091bd <__mingw_wcrtomb_cp+0x13d>
   140009119:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   14000911e:	74 0c                	je     14000912c <__mingw_wcrtomb_cp+0xac>
   140009120:	0f b7 45 18          	movzx  eax,WORD PTR [rbp+0x18]
   140009124:	89 c2                	mov    edx,eax
   140009126:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000912a:	88 10                	mov    BYTE PTR [rax],dl
   14000912c:	b8 01 00 00 00       	mov    eax,0x1
   140009131:	e9 9d 00 00 00       	jmp    1400091d3 <__mingw_wcrtomb_cp+0x153>
   140009136:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   14000913d:	66 c7 45 f6 00 00    	mov    WORD PTR [rbp-0xa],0x0
   140009143:	48 8d 4d 18          	lea    rcx,[rbp+0x18]
   140009147:	8b 45 28             	mov    eax,DWORD PTR [rbp+0x28]
   14000914a:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   14000914e:	48 89 54 24 38       	mov    QWORD PTR [rsp+0x38],rdx
   140009153:	48 c7 44 24 30 00 00 	mov    QWORD PTR [rsp+0x30],0x0
   14000915a:	00 00 
   14000915c:	8b 55 30             	mov    edx,DWORD PTR [rbp+0x30]
   14000915f:	89 54 24 28          	mov    DWORD PTR [rsp+0x28],edx
   140009163:	48 8d 55 f6          	lea    rdx,[rbp-0xa]
   140009167:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   14000916c:	41 b9 01 00 00 00    	mov    r9d,0x1
   140009172:	49 89 c8             	mov    r8,rcx
   140009175:	ba 00 00 00 00       	mov    edx,0x0
   14000917a:	89 c1                	mov    ecx,eax
   14000917c:	48 8b 05 e5 70 00 00 	mov    rax,QWORD PTR [rip+0x70e5]        # 140010268 <__imp_WideCharToMultiByte>
   140009183:	ff d0                	call   rax
   140009185:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140009188:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   14000918c:	74 32                	je     1400091c0 <__mingw_wcrtomb_cp+0x140>
   14000918e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140009191:	3b 45 30             	cmp    eax,DWORD PTR [rbp+0x30]
   140009194:	7f 2a                	jg     1400091c0 <__mingw_wcrtomb_cp+0x140>
   140009196:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140009199:	85 c0                	test   eax,eax
   14000919b:	75 23                	jne    1400091c0 <__mingw_wcrtomb_cp+0x140>
   14000919d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400091a0:	48 63 c8             	movsxd rcx,eax
   1400091a3:	48 8d 55 f6          	lea    rdx,[rbp-0xa]
   1400091a7:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400091ab:	49 89 c8             	mov    r8,rcx
   1400091ae:	48 89 c1             	mov    rcx,rax
   1400091b1:	e8 32 04 00 00       	call   1400095e8 <memcpy>
   1400091b6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400091b9:	48 98                	cdqe
   1400091bb:	eb 16                	jmp    1400091d3 <__mingw_wcrtomb_cp+0x153>
   1400091bd:	90                   	nop
   1400091be:	eb 01                	jmp    1400091c1 <__mingw_wcrtomb_cp+0x141>
   1400091c0:	90                   	nop
   1400091c1:	e8 b2 03 00 00       	call   140009578 <_errno>
   1400091c6:	c7 00 2a 00 00 00    	mov    DWORD PTR [rax],0x2a
   1400091cc:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   1400091d3:	48 83 c4 50          	add    rsp,0x50
   1400091d7:	5d                   	pop    rbp
   1400091d8:	c3                   	ret
   1400091d9:	90                   	nop
   1400091da:	90                   	nop
   1400091db:	90                   	nop
   1400091dc:	90                   	nop
   1400091dd:	90                   	nop
   1400091de:	90                   	nop
   1400091df:	90                   	nop

00000001400091e0 <__mingw_mbrtowc_cp>:
   1400091e0:	55                   	push   rbp
   1400091e1:	48 89 e5             	mov    rbp,rsp
   1400091e4:	48 83 ec 50          	sub    rsp,0x50
   1400091e8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400091ec:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400091f0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400091f4:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   1400091f8:	48 83 7d 18 00       	cmp    QWORD PTR [rbp+0x18],0x0
   1400091fd:	75 1b                	jne    14000921a <__mingw_mbrtowc_cp+0x3a>
   1400091ff:	48 c7 45 10 00 00 00 	mov    QWORD PTR [rbp+0x10],0x0
   140009206:	00 
   140009207:	48 8d 05 12 23 00 00 	lea    rax,[rip+0x2312]        # 14000b520 <.rdata>
   14000920e:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140009212:	48 c7 45 20 01 00 00 	mov    QWORD PTR [rbp+0x20],0x1
   140009219:	00 
   14000921a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000921e:	8b 00                	mov    eax,DWORD PTR [rax]
   140009220:	3d ff 00 00 00       	cmp    eax,0xff
   140009225:	0f 87 b9 01 00 00    	ja     1400093e4 <__mingw_mbrtowc_cp+0x204>
   14000922b:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140009230:	75 0c                	jne    14000923e <__mingw_mbrtowc_cp+0x5e>
   140009232:	48 c7 c0 fe ff ff ff 	mov    rax,0xfffffffffffffffe
   140009239:	e9 bc 01 00 00       	jmp    1400093fa <__mingw_mbrtowc_cp+0x21a>
   14000923e:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140009242:	8b 00                	mov    eax,DWORD PTR [rax]
   140009244:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   140009247:	83 7d 38 01          	cmp    DWORD PTR [rbp+0x38],0x1
   14000924b:	75 0c                	jne    140009259 <__mingw_mbrtowc_cp+0x79>
   14000924d:	0f b6 45 f0          	movzx  eax,BYTE PTR [rbp-0x10]
   140009251:	84 c0                	test   al,al
   140009253:	0f 85 8e 01 00 00    	jne    1400093e7 <__mingw_mbrtowc_cp+0x207>
   140009259:	83 7d 30 00          	cmp    DWORD PTR [rbp+0x30],0x0
   14000925d:	75 2c                	jne    14000928b <__mingw_mbrtowc_cp+0xab>
   14000925f:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140009264:	74 11                	je     140009277 <__mingw_mbrtowc_cp+0x97>
   140009266:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000926a:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   14000926d:	0f b6 d0             	movzx  edx,al
   140009270:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140009274:	66 89 10             	mov    WORD PTR [rax],dx
   140009277:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000927b:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   14000927e:	84 c0                	test   al,al
   140009280:	0f 95 c0             	setne  al
   140009283:	0f b6 c0             	movzx  eax,al
   140009286:	e9 6f 01 00 00       	jmp    1400093fa <__mingw_mbrtowc_cp+0x21a>
   14000928b:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   140009292:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140009299:	0f b6 45 f0          	movzx  eax,BYTE PTR [rbp-0x10]
   14000929d:	84 c0                	test   al,al
   14000929f:	74 1a                	je     1400092bb <__mingw_mbrtowc_cp+0xdb>
   1400092a1:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400092a5:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400092a8:	88 45 f1             	mov    BYTE PTR [rbp-0xf],al
   1400092ab:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400092b2:	c7 45 fc 02 00 00 00 	mov    DWORD PTR [rbp-0x4],0x2
   1400092b9:	eb 73                	jmp    14000932e <__mingw_mbrtowc_cp+0x14e>
   1400092bb:	83 7d 38 02          	cmp    DWORD PTR [rbp+0x38],0x2
   1400092bf:	75 5c                	jne    14000931d <__mingw_mbrtowc_cp+0x13d>
   1400092c1:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400092c5:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400092c8:	0f b6 c0             	movzx  eax,al
   1400092cb:	8b 55 30             	mov    edx,DWORD PTR [rbp+0x30]
   1400092ce:	89 c1                	mov    ecx,eax
   1400092d0:	e8 ad 01 00 00       	call   140009482 <__mingw_isleadbyte_cp>
   1400092d5:	85 c0                	test   eax,eax
   1400092d7:	74 44                	je     14000931d <__mingw_mbrtowc_cp+0x13d>
   1400092d9:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400092dd:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400092e0:	88 45 f0             	mov    BYTE PTR [rbp-0x10],al
   1400092e3:	48 83 7d 20 01       	cmp    QWORD PTR [rbp+0x20],0x1
   1400092e8:	77 15                	ja     1400092ff <__mingw_mbrtowc_cp+0x11f>
   1400092ea:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   1400092ed:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400092f1:	89 10                	mov    DWORD PTR [rax],edx
   1400092f3:	48 c7 c0 fe ff ff ff 	mov    rax,0xfffffffffffffffe
   1400092fa:	e9 fb 00 00 00       	jmp    1400093fa <__mingw_mbrtowc_cp+0x21a>
   1400092ff:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140009303:	48 83 c0 01          	add    rax,0x1
   140009307:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   14000930a:	88 45 f1             	mov    BYTE PTR [rbp-0xf],al
   14000930d:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140009314:	c7 45 fc 02 00 00 00 	mov    DWORD PTR [rbp-0x4],0x2
   14000931b:	eb 11                	jmp    14000932e <__mingw_mbrtowc_cp+0x14e>
   14000931d:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140009321:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140009324:	88 45 f0             	mov    BYTE PTR [rbp-0x10],al
   140009327:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   14000932e:	0f b6 45 f0          	movzx  eax,BYTE PTR [rbp-0x10]
   140009332:	84 c0                	test   al,al
   140009334:	75 24                	jne    14000935a <__mingw_mbrtowc_cp+0x17a>
   140009336:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   14000933b:	74 09                	je     140009346 <__mingw_mbrtowc_cp+0x166>
   14000933d:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140009341:	66 c7 00 00 00       	mov    WORD PTR [rax],0x0
   140009346:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000934a:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140009350:	b8 00 00 00 00       	mov    eax,0x0
   140009355:	e9 a0 00 00 00       	jmp    1400093fa <__mingw_mbrtowc_cp+0x21a>
   14000935a:	83 7d fc 02          	cmp    DWORD PTR [rbp-0x4],0x2
   14000935e:	75 08                	jne    140009368 <__mingw_mbrtowc_cp+0x188>
   140009360:	0f b6 45 f1          	movzx  eax,BYTE PTR [rbp-0xf]
   140009364:	84 c0                	test   al,al
   140009366:	74 64                	je     1400093cc <__mingw_mbrtowc_cp+0x1ec>
   140009368:	66 c7 45 ee ff ff    	mov    WORD PTR [rbp-0x12],0xffff
   14000936e:	44 8b 45 fc          	mov    r8d,DWORD PTR [rbp-0x4]
   140009372:	48 8d 4d f0          	lea    rcx,[rbp-0x10]
   140009376:	8b 45 30             	mov    eax,DWORD PTR [rbp+0x30]
   140009379:	c7 44 24 28 01 00 00 	mov    DWORD PTR [rsp+0x28],0x1
   140009380:	00 
   140009381:	48 8d 55 ee          	lea    rdx,[rbp-0x12]
   140009385:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   14000938a:	45 89 c1             	mov    r9d,r8d
   14000938d:	49 89 c8             	mov    r8,rcx
   140009390:	ba 08 00 00 00       	mov    edx,0x8
   140009395:	89 c1                	mov    ecx,eax
   140009397:	48 8b 05 9a 6e 00 00 	mov    rax,QWORD PTR [rip+0x6e9a]        # 140010238 <__imp_MultiByteToWideChar>
   14000939e:	ff d0                	call   rax
   1400093a0:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   1400093a3:	83 7d f4 01          	cmp    DWORD PTR [rbp-0xc],0x1
   1400093a7:	75 26                	jne    1400093cf <__mingw_mbrtowc_cp+0x1ef>
   1400093a9:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   1400093ae:	74 0b                	je     1400093bb <__mingw_mbrtowc_cp+0x1db>
   1400093b0:	0f b7 55 ee          	movzx  edx,WORD PTR [rbp-0x12]
   1400093b4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400093b8:	66 89 10             	mov    WORD PTR [rax],dx
   1400093bb:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400093bf:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   1400093c5:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   1400093c8:	48 98                	cdqe
   1400093ca:	eb 2e                	jmp    1400093fa <__mingw_mbrtowc_cp+0x21a>
   1400093cc:	90                   	nop
   1400093cd:	eb 01                	jmp    1400093d0 <__mingw_mbrtowc_cp+0x1f0>
   1400093cf:	90                   	nop
   1400093d0:	e8 a3 01 00 00       	call   140009578 <_errno>
   1400093d5:	c7 00 2a 00 00 00    	mov    DWORD PTR [rax],0x2a
   1400093db:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   1400093e2:	eb 16                	jmp    1400093fa <__mingw_mbrtowc_cp+0x21a>
   1400093e4:	90                   	nop
   1400093e5:	eb 01                	jmp    1400093e8 <__mingw_mbrtowc_cp+0x208>
   1400093e7:	90                   	nop
   1400093e8:	e8 8b 01 00 00       	call   140009578 <_errno>
   1400093ed:	c7 00 16 00 00 00    	mov    DWORD PTR [rax],0x16
   1400093f3:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   1400093fa:	48 83 c4 50          	add    rsp,0x50
   1400093fe:	5d                   	pop    rbp
   1400093ff:	c3                   	ret

0000000140009400 <fallback_IsDBCSLeadByteEx>:
   140009400:	55                   	push   rbp
   140009401:	48 89 e5             	mov    rbp,rsp
   140009404:	48 83 ec 40          	sub    rsp,0x40
   140009408:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000940b:	89 d0                	mov    eax,edx
   14000940d:	88 45 18             	mov    BYTE PTR [rbp+0x18],al
   140009410:	48 8d 55 e0          	lea    rdx,[rbp-0x20]
   140009414:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140009417:	89 c1                	mov    ecx,eax
   140009419:	48 8b 05 e0 6d 00 00 	mov    rax,QWORD PTR [rip+0x6de0]        # 140010200 <__imp_GetCPInfo>
   140009420:	ff d0                	call   rax
   140009422:	85 c0                	test   eax,eax
   140009424:	74 51                	je     140009477 <fallback_IsDBCSLeadByteEx+0x77>
   140009426:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
   140009429:	83 f8 02             	cmp    eax,0x2
   14000942c:	75 49                	jne    140009477 <fallback_IsDBCSLeadByteEx+0x77>
   14000942e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140009435:	eb 2c                	jmp    140009463 <fallback_IsDBCSLeadByteEx+0x63>
   140009437:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000943a:	48 98                	cdqe
   14000943c:	0f b6 44 05 e6       	movzx  eax,BYTE PTR [rbp+rax*1-0x1a]
   140009441:	38 45 18             	cmp    BYTE PTR [rbp+0x18],al
   140009444:	72 19                	jb     14000945f <fallback_IsDBCSLeadByteEx+0x5f>
   140009446:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140009449:	83 c0 01             	add    eax,0x1
   14000944c:	48 98                	cdqe
   14000944e:	0f b6 44 05 e6       	movzx  eax,BYTE PTR [rbp+rax*1-0x1a]
   140009453:	3a 45 18             	cmp    al,BYTE PTR [rbp+0x18]
   140009456:	72 07                	jb     14000945f <fallback_IsDBCSLeadByteEx+0x5f>
   140009458:	b8 01 00 00 00       	mov    eax,0x1
   14000945d:	eb 1d                	jmp    14000947c <fallback_IsDBCSLeadByteEx+0x7c>
   14000945f:	83 45 fc 02          	add    DWORD PTR [rbp-0x4],0x2
   140009463:	83 7d fc 0b          	cmp    DWORD PTR [rbp-0x4],0xb
   140009467:	7f 0e                	jg     140009477 <fallback_IsDBCSLeadByteEx+0x77>
   140009469:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000946c:	48 98                	cdqe
   14000946e:	0f b6 44 05 e6       	movzx  eax,BYTE PTR [rbp+rax*1-0x1a]
   140009473:	84 c0                	test   al,al
   140009475:	75 c0                	jne    140009437 <fallback_IsDBCSLeadByteEx+0x37>
   140009477:	b8 00 00 00 00       	mov    eax,0x0
   14000947c:	48 83 c4 40          	add    rsp,0x40
   140009480:	5d                   	pop    rbp
   140009481:	c3                   	ret

0000000140009482 <__mingw_isleadbyte_cp>:
   140009482:	55                   	push   rbp
   140009483:	48 89 e5             	mov    rbp,rsp
   140009486:	48 83 ec 40          	sub    rsp,0x40
   14000948a:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000948d:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140009490:	48 8b 05 09 67 00 00 	mov    rax,QWORD PTR [rip+0x6709]        # 14000fba0 <call_IsDBCSLeadByteEx.0>
   140009497:	48 85 c0             	test   rax,rax
   14000949a:	75 71                	jne    14000950d <__mingw_isleadbyte_cp+0x8b>
   14000949c:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   1400094a3:	00 
   1400094a4:	48 8d 05 85 20 00 00 	lea    rax,[rip+0x2085]        # 14000b530 <.rdata>
   1400094ab:	48 89 c1             	mov    rcx,rax
   1400094ae:	48 8b 05 5b 6d 00 00 	mov    rax,QWORD PTR [rip+0x6d5b]        # 140010210 <__imp_GetModuleHandleA>
   1400094b5:	ff d0                	call   rax
   1400094b7:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400094bb:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400094c0:	74 1b                	je     1400094dd <__mingw_isleadbyte_cp+0x5b>
   1400094c2:	48 8d 15 74 20 00 00 	lea    rdx,[rip+0x2074]        # 14000b53d <.rdata+0xd>
   1400094c9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400094cd:	48 89 c1             	mov    rcx,rax
   1400094d0:	48 8b 05 41 6d 00 00 	mov    rax,QWORD PTR [rip+0x6d41]        # 140010218 <__imp_GetProcAddress>
   1400094d7:	ff d0                	call   rax
   1400094d9:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400094dd:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400094e2:	75 0b                	jne    1400094ef <__mingw_isleadbyte_cp+0x6d>
   1400094e4:	48 8d 05 15 ff ff ff 	lea    rax,[rip+0xffffffffffffff15]        # 140009400 <fallback_IsDBCSLeadByteEx>
   1400094eb:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400094ef:	48 8d 05 aa 66 00 00 	lea    rax,[rip+0x66aa]        # 14000fba0 <call_IsDBCSLeadByteEx.0>
   1400094f6:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400094fa:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400094fe:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140009502:	48 8b 55 e0          	mov    rdx,QWORD PTR [rbp-0x20]
   140009506:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000950a:	48 87 10             	xchg   QWORD PTR [rax],rdx
   14000950d:	4c 8b 05 8c 66 00 00 	mov    r8,QWORD PTR [rip+0x668c]        # 14000fba0 <call_IsDBCSLeadByteEx.0>
   140009514:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140009517:	0f b6 d0             	movzx  edx,al
   14000951a:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   14000951d:	89 c1                	mov    ecx,eax
   14000951f:	41 ff d0             	call   r8
   140009522:	48 83 c4 40          	add    rsp,0x40
   140009526:	5d                   	pop    rbp
   140009527:	c3                   	ret
   140009528:	90                   	nop
   140009529:	90                   	nop
   14000952a:	90                   	nop
   14000952b:	90                   	nop
   14000952c:	90                   	nop
   14000952d:	90                   	nop
   14000952e:	90                   	nop
   14000952f:	90                   	nop

0000000140009530 <__C_specific_handler>:
   140009530:	ff 25 42 6d 00 00    	jmp    QWORD PTR [rip+0x6d42]        # 140010278 <__imp___C_specific_handler>
   140009536:	90                   	nop
   140009537:	90                   	nop

0000000140009538 <___lc_codepage_func>:
   140009538:	ff 25 42 6d 00 00    	jmp    QWORD PTR [rip+0x6d42]        # 140010280 <__imp____lc_codepage_func>
   14000953e:	90                   	nop
   14000953f:	90                   	nop

0000000140009540 <___mb_cur_max_func>:
   140009540:	ff 25 42 6d 00 00    	jmp    QWORD PTR [rip+0x6d42]        # 140010288 <__imp____mb_cur_max_func>
   140009546:	90                   	nop
   140009547:	90                   	nop

0000000140009548 <__getmainargs>:
   140009548:	ff 25 42 6d 00 00    	jmp    QWORD PTR [rip+0x6d42]        # 140010290 <__imp___getmainargs>
   14000954e:	90                   	nop
   14000954f:	90                   	nop

0000000140009550 <__iob_func>:
   140009550:	ff 25 4a 6d 00 00    	jmp    QWORD PTR [rip+0x6d4a]        # 1400102a0 <__imp___iob_func>
   140009556:	90                   	nop
   140009557:	90                   	nop

0000000140009558 <__set_app_type>:
   140009558:	ff 25 4a 6d 00 00    	jmp    QWORD PTR [rip+0x6d4a]        # 1400102a8 <__imp___set_app_type>
   14000955e:	90                   	nop
   14000955f:	90                   	nop

0000000140009560 <__setusermatherr>:
   140009560:	ff 25 4a 6d 00 00    	jmp    QWORD PTR [rip+0x6d4a]        # 1400102b0 <__imp___setusermatherr>
   140009566:	90                   	nop
   140009567:	90                   	nop

0000000140009568 <_amsg_exit>:
   140009568:	ff 25 4a 6d 00 00    	jmp    QWORD PTR [rip+0x6d4a]        # 1400102b8 <__imp__amsg_exit>
   14000956e:	90                   	nop
   14000956f:	90                   	nop

0000000140009570 <_cexit>:
   140009570:	ff 25 4a 6d 00 00    	jmp    QWORD PTR [rip+0x6d4a]        # 1400102c0 <__imp__cexit>
   140009576:	90                   	nop
   140009577:	90                   	nop

0000000140009578 <_errno>:
   140009578:	ff 25 52 6d 00 00    	jmp    QWORD PTR [rip+0x6d52]        # 1400102d0 <__imp__errno>
   14000957e:	90                   	nop
   14000957f:	90                   	nop

0000000140009580 <_initterm>:
   140009580:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 1400102e0 <__imp__initterm>
   140009586:	90                   	nop
   140009587:	90                   	nop

0000000140009588 <_lock>:
   140009588:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 1400102e8 <__imp__lock>
   14000958e:	90                   	nop
   14000958f:	90                   	nop

0000000140009590 <_unlock>:
   140009590:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 1400102f0 <__imp__unlock>
   140009596:	90                   	nop
   140009597:	90                   	nop

0000000140009598 <_crt_atexit>:
   140009598:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 1400102f8 <__imp__crt_atexit>
   14000959e:	90                   	nop
   14000959f:	90                   	nop

00000001400095a0 <abort>:
   1400095a0:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010300 <__imp_abort>
   1400095a6:	90                   	nop
   1400095a7:	90                   	nop

00000001400095a8 <calloc>:
   1400095a8:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010308 <__imp_calloc>
   1400095ae:	90                   	nop
   1400095af:	90                   	nop

00000001400095b0 <exit>:
   1400095b0:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010310 <__imp_exit>
   1400095b6:	90                   	nop
   1400095b7:	90                   	nop

00000001400095b8 <fflush>:
   1400095b8:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010318 <__imp_fflush>
   1400095be:	90                   	nop
   1400095bf:	90                   	nop

00000001400095c0 <fprintf>:
   1400095c0:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010320 <__imp_fprintf>
   1400095c6:	90                   	nop
   1400095c7:	90                   	nop

00000001400095c8 <fputc>:
   1400095c8:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010328 <__imp_fputc>
   1400095ce:	90                   	nop
   1400095cf:	90                   	nop

00000001400095d0 <free>:
   1400095d0:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010330 <__imp_free>
   1400095d6:	90                   	nop
   1400095d7:	90                   	nop

00000001400095d8 <localeconv>:
   1400095d8:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010338 <__imp_localeconv>
   1400095de:	90                   	nop
   1400095df:	90                   	nop

00000001400095e0 <malloc>:
   1400095e0:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010340 <__imp_malloc>
   1400095e6:	90                   	nop
   1400095e7:	90                   	nop

00000001400095e8 <memcpy>:
   1400095e8:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010348 <__imp_memcpy>
   1400095ee:	90                   	nop
   1400095ef:	90                   	nop

00000001400095f0 <setvbuf>:
   1400095f0:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010350 <__imp_setvbuf>
   1400095f6:	90                   	nop
   1400095f7:	90                   	nop

00000001400095f8 <signal>:
   1400095f8:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010358 <__imp_signal>
   1400095fe:	90                   	nop
   1400095ff:	90                   	nop

0000000140009600 <strerror>:
   140009600:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010360 <__imp_strerror>
   140009606:	90                   	nop
   140009607:	90                   	nop

0000000140009608 <strlen>:
   140009608:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010368 <__imp_strlen>
   14000960e:	90                   	nop
   14000960f:	90                   	nop

0000000140009610 <strncmp>:
   140009610:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010370 <__imp_strncmp>
   140009616:	90                   	nop
   140009617:	90                   	nop

0000000140009618 <vfprintf>:
   140009618:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010378 <__imp_vfprintf>
   14000961e:	90                   	nop
   14000961f:	90                   	nop

0000000140009620 <wcslen>:
   140009620:	ff 25 5a 6d 00 00    	jmp    QWORD PTR [rip+0x6d5a]        # 140010380 <__imp_wcslen>
   140009626:	90                   	nop
   140009627:	90                   	nop
   140009628:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000962f:	00 

0000000140009630 <WideCharToMultiByte>:
   140009630:	ff 25 32 6c 00 00    	jmp    QWORD PTR [rip+0x6c32]        # 140010268 <__imp_WideCharToMultiByte>
   140009636:	90                   	nop
   140009637:	90                   	nop

0000000140009638 <VirtualQuery>:
   140009638:	ff 25 22 6c 00 00    	jmp    QWORD PTR [rip+0x6c22]        # 140010260 <__imp_VirtualQuery>
   14000963e:	90                   	nop
   14000963f:	90                   	nop

0000000140009640 <VirtualProtect>:
   140009640:	ff 25 12 6c 00 00    	jmp    QWORD PTR [rip+0x6c12]        # 140010258 <__imp_VirtualProtect>
   140009646:	90                   	nop
   140009647:	90                   	nop

0000000140009648 <TlsGetValue>:
   140009648:	ff 25 02 6c 00 00    	jmp    QWORD PTR [rip+0x6c02]        # 140010250 <__imp_TlsGetValue>
   14000964e:	90                   	nop
   14000964f:	90                   	nop

0000000140009650 <Sleep>:
   140009650:	ff 25 f2 6b 00 00    	jmp    QWORD PTR [rip+0x6bf2]        # 140010248 <__imp_Sleep>
   140009656:	90                   	nop
   140009657:	90                   	nop

0000000140009658 <SetUnhandledExceptionFilter>:
   140009658:	ff 25 e2 6b 00 00    	jmp    QWORD PTR [rip+0x6be2]        # 140010240 <__imp_SetUnhandledExceptionFilter>
   14000965e:	90                   	nop
   14000965f:	90                   	nop

0000000140009660 <MultiByteToWideChar>:
   140009660:	ff 25 d2 6b 00 00    	jmp    QWORD PTR [rip+0x6bd2]        # 140010238 <__imp_MultiByteToWideChar>
   140009666:	90                   	nop
   140009667:	90                   	nop

0000000140009668 <LoadLibraryA>:
   140009668:	ff 25 c2 6b 00 00    	jmp    QWORD PTR [rip+0x6bc2]        # 140010230 <__imp_LoadLibraryA>
   14000966e:	90                   	nop
   14000966f:	90                   	nop

0000000140009670 <LeaveCriticalSection>:
   140009670:	ff 25 b2 6b 00 00    	jmp    QWORD PTR [rip+0x6bb2]        # 140010228 <__imp_LeaveCriticalSection>
   140009676:	90                   	nop
   140009677:	90                   	nop

0000000140009678 <InitializeCriticalSection>:
   140009678:	ff 25 a2 6b 00 00    	jmp    QWORD PTR [rip+0x6ba2]        # 140010220 <__imp_InitializeCriticalSection>
   14000967e:	90                   	nop
   14000967f:	90                   	nop

0000000140009680 <GetProcAddress>:
   140009680:	ff 25 92 6b 00 00    	jmp    QWORD PTR [rip+0x6b92]        # 140010218 <__imp_GetProcAddress>
   140009686:	90                   	nop
   140009687:	90                   	nop

0000000140009688 <GetModuleHandleA>:
   140009688:	ff 25 82 6b 00 00    	jmp    QWORD PTR [rip+0x6b82]        # 140010210 <__imp_GetModuleHandleA>
   14000968e:	90                   	nop
   14000968f:	90                   	nop

0000000140009690 <GetLastError>:
   140009690:	ff 25 72 6b 00 00    	jmp    QWORD PTR [rip+0x6b72]        # 140010208 <__imp_GetLastError>
   140009696:	90                   	nop
   140009697:	90                   	nop

0000000140009698 <GetCPInfo>:
   140009698:	ff 25 62 6b 00 00    	jmp    QWORD PTR [rip+0x6b62]        # 140010200 <__imp_GetCPInfo>
   14000969e:	90                   	nop
   14000969f:	90                   	nop

00000001400096a0 <FreeLibrary>:
   1400096a0:	ff 25 52 6b 00 00    	jmp    QWORD PTR [rip+0x6b52]        # 1400101f8 <__imp_FreeLibrary>
   1400096a6:	90                   	nop
   1400096a7:	90                   	nop

00000001400096a8 <EnterCriticalSection>:
   1400096a8:	ff 25 42 6b 00 00    	jmp    QWORD PTR [rip+0x6b42]        # 1400101f0 <__imp_EnterCriticalSection>
   1400096ae:	90                   	nop
   1400096af:	90                   	nop

00000001400096b0 <DeleteCriticalSection>:
   1400096b0:	ff 25 32 6b 00 00    	jmp    QWORD PTR [rip+0x6b32]        # 1400101e8 <__IAT_start__>
   1400096b6:	90                   	nop
   1400096b7:	90                   	nop
   1400096b8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   1400096bf:	00 

00000001400096c0 <main>:
   1400096c0:	48 83 ec 38          	sub    rsp,0x38
   1400096c4:	e8 7e 81 ff ff       	call   140001847 <__main>
   1400096c9:	e8 a2 80 ff ff       	call   140001770 <get_field()>
   1400096ce:	44 8b 08             	mov    r9d,DWORD PTR [rax]
   1400096d1:	48 89 c1             	mov    rcx,rax
   1400096d4:	49 89 c0             	mov    r8,rax
   1400096d7:	e8 a4 80 ff ff       	call   140001780 <bump(int*)>
   1400096dc:	b9 2a 00 00 00       	mov    ecx,0x2a
   1400096e1:	e8 7a 80 ff ff       	call   140001760 <sink(int)>
   1400096e6:	44 89 c9             	mov    ecx,r9d
   1400096e9:	41 b9 04 00 00 00    	mov    r9d,0x4
   1400096ef:	89 c2                	mov    edx,eax
   1400096f1:	e8 6a 80 ff ff       	call   140001760 <sink(int)>
   1400096f6:	41 8b 08             	mov    ecx,DWORD PTR [r8]
   1400096f9:	41 b8 01 00 00 00    	mov    r8d,0x1
   1400096ff:	01 c2                	add    edx,eax
   140009701:	e8 5a 80 ff ff       	call   140001760 <sink(int)>
   140009706:	48 8d 0d 43 19 00 00 	lea    rcx,[rip+0x1943]        # 14000b050 <.rdata>
   14000970d:	48 c7 44 24 20 08 00 	mov    QWORD PTR [rsp+0x20],0x8
   140009714:	00 00 
   140009716:	01 c2                	add    edx,eax
   140009718:	e8 83 99 ff ff       	call   1400030a0 <__mingw_printf>
   14000971d:	31 c0                	xor    eax,eax
   14000971f:	48 83 c4 38          	add    rsp,0x38
   140009723:	c3                   	ret
   140009724:	90                   	nop
   140009725:	90                   	nop
   140009726:	90                   	nop
   140009727:	90                   	nop
   140009728:	90                   	nop
   140009729:	90                   	nop
   14000972a:	90                   	nop
   14000972b:	90                   	nop
   14000972c:	90                   	nop
   14000972d:	90                   	nop
   14000972e:	90                   	nop
   14000972f:	90                   	nop

0000000140009730 <register_frame_ctor>:
   140009730:	e9 3b 7f ff ff       	jmp    140001670 <__gcc_register_frame>
   140009735:	90                   	nop
   140009736:	90                   	nop
   140009737:	90                   	nop
   140009738:	90                   	nop
   140009739:	90                   	nop
   14000973a:	90                   	nop
   14000973b:	90                   	nop
   14000973c:	90                   	nop
   14000973d:	90                   	nop
   14000973e:	90                   	nop
   14000973f:	90                   	nop
