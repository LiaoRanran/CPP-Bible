
ch84_set_test.exe:     file format pei-x86-64


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
   140001024:	e8 b7 23 00 00       	call   1400033e0 <fflush>
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
   14000103f:	48 8b 05 9a 43 00 00 	mov    rax,QWORD PTR [rip+0x439a]        # 1400053e0 <.refptr.__mingw_app_type>
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
   14000106e:	48 8b 05 6b 43 00 00 	mov    rax,QWORD PTR [rip+0x436b]        # 1400053e0 <.refptr.__mingw_app_type>
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
   1400010e8:	48 8b 05 91 91 00 00 	mov    rax,QWORD PTR [rip+0x9191]        # 14000a280 <__imp_Sleep>
   1400010ef:	ff d0                	call   rax
   1400010f1:	48 8b 05 38 43 00 00 	mov    rax,QWORD PTR [rip+0x4338]        # 140005430 <.refptr.__native_startup_lock>
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
   140001128:	48 8b 05 11 43 00 00 	mov    rax,QWORD PTR [rip+0x4311]        # 140005440 <.refptr.__native_startup_state>
   14000112f:	8b 00                	mov    eax,DWORD PTR [rax]
   140001131:	83 f8 01             	cmp    eax,0x1
   140001134:	75 0a                	jne    140001140 <__tmainCRTStartup+0xb2>
   140001136:	b9 1f 00 00 00       	mov    ecx,0x1f
   14000113b:	e8 68 22 00 00       	call   1400033a8 <_amsg_exit>
   140001140:	48 8b 05 f9 42 00 00 	mov    rax,QWORD PTR [rip+0x42f9]        # 140005440 <.refptr.__native_startup_state>
   140001147:	8b 00                	mov    eax,DWORD PTR [rax]
   140001149:	85 c0                	test   eax,eax
   14000114b:	0f 85 e3 01 00 00    	jne    140001334 <__tmainCRTStartup+0x2a6>
   140001151:	48 8b 05 e8 42 00 00 	mov    rax,QWORD PTR [rip+0x42e8]        # 140005440 <.refptr.__native_startup_state>
   140001158:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000115e:	b9 02 00 00 00       	mov    ecx,0x2
   140001163:	e8 e8 21 00 00       	call   140003350 <__acrt_iob_func>
   140001168:	41 b9 00 00 00 00    	mov    r9d,0x0
   14000116e:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001174:	ba 00 00 00 00       	mov    edx,0x0
   140001179:	48 89 c1             	mov    rcx,rax
   14000117c:	e8 87 22 00 00       	call   140003408 <setvbuf>
   140001181:	48 8d 05 8f fe ff ff 	lea    rax,[rip+0xfffffffffffffe8f]        # 140001017 <safe_flush>
   140001188:	48 89 c1             	mov    rcx,rax
   14000118b:	e8 9f 04 00 00       	call   14000162f <atexit>
   140001190:	85 c0                	test   eax,eax
   140001192:	74 05                	je     140001199 <__tmainCRTStartup+0x10b>
   140001194:	e8 2f 22 00 00       	call   1400033c8 <abort>
   140001199:	e8 a2 12 00 00       	call   140002440 <_pei386_runtime_relocator>
   14000119e:	48 8b 05 1b 43 00 00 	mov    rax,QWORD PTR [rip+0x431b]        # 1400054c0 <.refptr._gnu_exception_handler>
   1400011a5:	48 89 c1             	mov    rcx,rax
   1400011a8:	48 8b 05 c9 90 00 00 	mov    rax,QWORD PTR [rip+0x90c9]        # 14000a278 <__imp_SetUnhandledExceptionFilter>
   1400011af:	ff d0                	call   rax
   1400011b1:	48 8b 15 68 42 00 00 	mov    rdx,QWORD PTR [rip+0x4268]        # 140005420 <.refptr.__mingw_oldexcpt_handler>
   1400011b8:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400011bb:	48 8d 05 3e fe ff ff 	lea    rax,[rip+0xfffffffffffffe3e]        # 140001000 <__mingw_invalidParameterHandler>
   1400011c2:	48 89 c1             	mov    rcx,rax
   1400011c5:	e8 26 21 00 00       	call   1400032f0 <_set_invalid_parameter_handler>
   1400011ca:	e8 81 1b 00 00       	call   140002d50 <_fpreset>
   1400011cf:	e8 18 02 00 00       	call   1400013ec <check_managed_app>
   1400011d4:	89 05 3e 7e 00 00    	mov    DWORD PTR [rip+0x7e3e],eax        # 140009018 <managedapp>
   1400011da:	48 8b 05 ff 41 00 00 	mov    rax,QWORD PTR [rip+0x41ff]        # 1400053e0 <.refptr.__mingw_app_type>
   1400011e1:	8b 00                	mov    eax,DWORD PTR [rax]
   1400011e3:	85 c0                	test   eax,eax
   1400011e5:	74 0c                	je     1400011f3 <__tmainCRTStartup+0x165>
   1400011e7:	b9 02 00 00 00       	mov    ecx,0x2
   1400011ec:	e8 a7 21 00 00       	call   140003398 <__set_app_type>
   1400011f1:	eb 0a                	jmp    1400011fd <__tmainCRTStartup+0x16f>
   1400011f3:	b9 01 00 00 00       	mov    ecx,0x1
   1400011f8:	e8 9b 21 00 00       	call   140003398 <__set_app_type>
   1400011fd:	e8 be 20 00 00       	call   1400032c0 <__p__fmode>
   140001202:	48 8b 15 a7 42 00 00 	mov    rdx,QWORD PTR [rip+0x42a7]        # 1400054b0 <.refptr._fmode>
   140001209:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000120b:	89 10                	mov    DWORD PTR [rax],edx
   14000120d:	e8 be 20 00 00       	call   1400032d0 <__p__commode>
   140001212:	48 8b 15 77 42 00 00 	mov    rdx,QWORD PTR [rip+0x4277]        # 140005490 <.refptr._commode>
   140001219:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000121b:	89 10                	mov    DWORD PTR [rax],edx
   14000121d:	e8 fe 07 00 00       	call   140001a20 <_setargv>
   140001222:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140001225:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140001229:	79 0a                	jns    140001235 <__tmainCRTStartup+0x1a7>
   14000122b:	b9 08 00 00 00       	mov    ecx,0x8
   140001230:	e8 73 21 00 00       	call   1400033a8 <_amsg_exit>
   140001235:	48 8b 05 04 41 00 00 	mov    rax,QWORD PTR [rip+0x4104]        # 140005340 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   14000123c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000123e:	83 f8 01             	cmp    eax,0x1
   140001241:	75 0f                	jne    140001252 <__tmainCRTStartup+0x1c4>
   140001243:	48 8b 05 86 42 00 00 	mov    rax,QWORD PTR [rip+0x4286]        # 1400054d0 <.refptr._matherr>
   14000124a:	48 89 c1             	mov    rcx,rax
   14000124d:	e8 08 13 00 00       	call   14000255a <__mingw_setusermatherr>
   140001252:	48 8b 05 47 41 00 00 	mov    rax,QWORD PTR [rip+0x4147]        # 1400053a0 <.refptr.__globallocalestatus>
   140001259:	8b 00                	mov    eax,DWORD PTR [rax]
   14000125b:	83 f8 ff             	cmp    eax,0xffffffff
   14000125e:	75 0a                	jne    14000126a <__tmainCRTStartup+0x1dc>
   140001260:	b9 ff ff ff ff       	mov    ecx,0xffffffff
   140001265:	e8 c6 20 00 00       	call   140003330 <_configthreadlocale>
   14000126a:	48 8b 15 0f 42 00 00 	mov    rdx,QWORD PTR [rip+0x420f]        # 140005480 <.refptr.__xi_z>
   140001271:	48 8b 05 f8 41 00 00 	mov    rax,QWORD PTR [rip+0x41f8]        # 140005470 <.refptr.__xi_a>
   140001278:	48 89 c1             	mov    rcx,rax
   14000127b:	e8 e0 1f 00 00       	call   140003260 <_initterm_e>
   140001280:	85 c0                	test   eax,eax
   140001282:	74 0a                	je     14000128e <__tmainCRTStartup+0x200>
   140001284:	b9 0a 00 00 00       	mov    ecx,0xa
   140001289:	e8 1a 21 00 00       	call   1400033a8 <_amsg_exit>
   14000128e:	48 8b 05 4b 42 00 00 	mov    rax,QWORD PTR [rip+0x424b]        # 1400054e0 <.refptr._newmode>
   140001295:	8b 00                	mov    eax,DWORD PTR [rax]
   140001297:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000129a:	48 8b 05 ff 41 00 00 	mov    rax,QWORD PTR [rip+0x41ff]        # 1400054a0 <.refptr._dowildcard>
   1400012a1:	44 8b 00             	mov    r8d,DWORD PTR [rax]
   1400012a4:	4c 8d 15 65 7d 00 00 	lea    r10,[rip+0x7d65]        # 140009010 <envp>
   1400012ab:	48 8d 15 56 7d 00 00 	lea    rdx,[rip+0x7d56]        # 140009008 <argv>
   1400012b2:	48 8d 05 4b 7d 00 00 	lea    rax,[rip+0x7d4b]        # 140009004 <argc>
   1400012b9:	48 8d 4d ac          	lea    rcx,[rbp-0x54]
   1400012bd:	48 89 4c 24 20       	mov    QWORD PTR [rsp+0x20],rcx
   1400012c2:	45 89 c1             	mov    r9d,r8d
   1400012c5:	4d 89 d0             	mov    r8,r10
   1400012c8:	48 89 c1             	mov    rcx,rax
   1400012cb:	e8 b8 20 00 00       	call   140003388 <__getmainargs>
   1400012d0:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012d3:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012d7:	79 0a                	jns    1400012e3 <__tmainCRTStartup+0x255>
   1400012d9:	b9 08 00 00 00       	mov    ecx,0x8
   1400012de:	e8 c5 20 00 00       	call   1400033a8 <_amsg_exit>
   1400012e3:	8b 05 1b 7d 00 00    	mov    eax,DWORD PTR [rip+0x7d1b]        # 140009004 <argc>
   1400012e9:	48 8d 15 18 7d 00 00 	lea    rdx,[rip+0x7d18]        # 140009008 <argv>
   1400012f0:	89 c1                	mov    ecx,eax
   1400012f2:	e8 f9 01 00 00       	call   1400014f0 <duplicate_ppstrings>
   1400012f7:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012fa:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012fe:	74 0a                	je     14000130a <__tmainCRTStartup+0x27c>
   140001300:	b9 08 00 00 00       	mov    ecx,0x8
   140001305:	e8 9e 20 00 00       	call   1400033a8 <_amsg_exit>
   14000130a:	48 8b 15 4f 41 00 00 	mov    rdx,QWORD PTR [rip+0x414f]        # 140005460 <.refptr.__xc_z>
   140001311:	48 8b 05 38 41 00 00 	mov    rax,QWORD PTR [rip+0x4138]        # 140005450 <.refptr.__xc_a>
   140001318:	48 89 c1             	mov    rcx,rax
   14000131b:	e8 98 20 00 00       	call   1400033b8 <_initterm>
   140001320:	e8 d2 06 00 00       	call   1400019f7 <__main>
   140001325:	48 8b 05 14 41 00 00 	mov    rax,QWORD PTR [rip+0x4114]        # 140005440 <.refptr.__native_startup_state>
   14000132c:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   140001332:	eb 0a                	jmp    14000133e <__tmainCRTStartup+0x2b0>
   140001334:	c7 05 de 7c 00 00 01 	mov    DWORD PTR [rip+0x7cde],0x1        # 14000901c <has_cctor>
   14000133b:	00 00 00 
   14000133e:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140001342:	75 1e                	jne    140001362 <__tmainCRTStartup+0x2d4>
   140001344:	48 8b 05 e5 40 00 00 	mov    rax,QWORD PTR [rip+0x40e5]        # 140005430 <.refptr.__native_startup_lock>
   14000134b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000134f:	48 c7 45 b0 00 00 00 	mov    QWORD PTR [rbp-0x50],0x0
   140001356:	00 
   140001357:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   14000135b:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000135f:	48 87 10             	xchg   QWORD PTR [rax],rdx
   140001362:	48 8b 05 27 40 00 00 	mov    rax,QWORD PTR [rip+0x4027]        # 140005390 <.refptr.__dyn_tls_init_callback>
   140001369:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000136c:	48 85 c0             	test   rax,rax
   14000136f:	74 1c                	je     14000138d <__tmainCRTStartup+0x2ff>
   140001371:	48 8b 05 18 40 00 00 	mov    rax,QWORD PTR [rip+0x4018]        # 140005390 <.refptr.__dyn_tls_init_callback>
   140001378:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000137b:	41 b8 00 00 00 00    	mov    r8d,0x0
   140001381:	ba 02 00 00 00       	mov    edx,0x2
   140001386:	b9 00 00 00 00       	mov    ecx,0x0
   14000138b:	ff d0                	call   rax
   14000138d:	e8 4e 1f 00 00       	call   1400032e0 <__p___initenv>
   140001392:	48 8b 15 77 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c77]        # 140009010 <envp>
   140001399:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000139c:	48 8b 0d 6d 7c 00 00 	mov    rcx,QWORD PTR [rip+0x7c6d]        # 140009010 <envp>
   1400013a3:	48 8b 15 5e 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c5e]        # 140009008 <argv>
   1400013aa:	8b 05 54 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c54]        # 140009004 <argc>
   1400013b0:	49 89 c8             	mov    r8,rcx
   1400013b3:	89 c1                	mov    ecx,eax
   1400013b5:	e8 06 21 00 00       	call   1400034c0 <main>
   1400013ba:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400013bd:	8b 05 55 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c55]        # 140009018 <managedapp>
   1400013c3:	85 c0                	test   eax,eax
   1400013c5:	75 0a                	jne    1400013d1 <__tmainCRTStartup+0x343>
   1400013c7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013ca:	89 c1                	mov    ecx,eax
   1400013cc:	e8 07 20 00 00       	call   1400033d8 <exit>
   1400013d1:	8b 05 45 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c45]        # 14000901c <has_cctor>
   1400013d7:	85 c0                	test   eax,eax
   1400013d9:	75 05                	jne    1400013e0 <__tmainCRTStartup+0x352>
   1400013db:	e8 d0 1f 00 00       	call   1400033b0 <_cexit>
   1400013e0:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013e3:	48 81 c4 90 00 00 00 	add    rsp,0x90
   1400013ea:	5d                   	pop    rbp
   1400013eb:	c3                   	ret

00000001400013ec <check_managed_app>:
   1400013ec:	55                   	push   rbp
   1400013ed:	48 89 e5             	mov    rbp,rsp
   1400013f0:	48 83 ec 20          	sub    rsp,0x20
   1400013f4:	48 8b 05 f5 3f 00 00 	mov    rax,QWORD PTR [rip+0x3ff5]        # 1400053f0 <.refptr.__mingw_initltsdrot_force>
   1400013fb:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   140001401:	48 8b 05 f8 3f 00 00 	mov    rax,QWORD PTR [rip+0x3ff8]        # 140005400 <.refptr.__mingw_initltsdyn_force>
   140001408:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000140e:	48 8b 05 fb 3f 00 00 	mov    rax,QWORD PTR [rip+0x3ffb]        # 140005410 <.refptr.__mingw_initltssuo_force>
   140001415:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000141b:	48 8b 05 3e 3f 00 00 	mov    rax,QWORD PTR [rip+0x3f3e]        # 140005360 <.refptr.__ImageBase>
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
   140001511:	e8 e2 1e 00 00       	call   1400033f8 <malloc>
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
   14000155c:	e8 b7 1e 00 00       	call   140003418 <strlen>
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
   140001585:	e8 6e 1e 00 00       	call   1400033f8 <malloc>
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
   1400015e8:	e8 13 1e 00 00       	call   140003400 <memcpy>
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
   140001642:	e8 79 1d 00 00       	call   1400033c0 <_crt_atexit>
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
   14000167b:	48 8d 0d 7e 39 00 00 	lea    rcx,[rip+0x397e]        # 140005000 <.rdata>
   140001682:	ff 15 c8 8b 00 00    	call   QWORD PTR [rip+0x8bc8]        # 14000a250 <__imp_GetModuleHandleA>
   140001688:	48 89 c3             	mov    rbx,rax
   14000168b:	48 85 c0             	test   rax,rax
   14000168e:	74 70                	je     140001700 <__gcc_register_frame+0x90>
   140001690:	48 8d 0d 69 39 00 00 	lea    rcx,[rip+0x3969]        # 140005000 <.rdata>
   140001697:	ff 15 d3 8b 00 00    	call   QWORD PTR [rip+0x8bd3]        # 14000a270 <__imp_LoadLibraryA>
   14000169d:	4c 8b 0d b4 8b 00 00 	mov    r9,QWORD PTR [rip+0x8bb4]        # 14000a258 <__imp_GetProcAddress>
   1400016a4:	48 8d 15 68 39 00 00 	lea    rdx,[rip+0x3968]        # 140005013 <.rdata+0x13>
   1400016ab:	48 89 d9             	mov    rcx,rbx
   1400016ae:	48 89 05 6b 79 00 00 	mov    QWORD PTR [rip+0x796b],rax        # 140009020 <hmod_libgcc>
   1400016b5:	4c 89 4d f0          	mov    QWORD PTR [rbp-0x10],r9
   1400016b9:	41 ff d1             	call   r9
   1400016bc:	48 8d 15 66 39 00 00 	lea    rdx,[rip+0x3966]        # 140005029 <.rdata+0x29>
   1400016c3:	48 89 d9             	mov    rcx,rbx
   1400016c6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400016ca:	ff 55 f0             	call   QWORD PTR [rbp-0x10]
   1400016cd:	4c 8b 45 f8          	mov    r8,QWORD PTR [rbp-0x8]
   1400016d1:	48 89 05 28 29 00 00 	mov    QWORD PTR [rip+0x2928],rax        # 140004000 <__data_start__>
   1400016d8:	4d 85 c0             	test   r8,r8
   1400016db:	74 11                	je     1400016ee <__gcc_register_frame+0x7e>
   1400016dd:	48 8d 15 5c 79 00 00 	lea    rdx,[rip+0x795c]        # 140009040 <obj>
   1400016e4:	48 8d 0d 15 49 00 00 	lea    rcx,[rip+0x4915]        # 140006000 <__EH_FRAME_BEGIN__>
   1400016eb:	41 ff d0             	call   r8
   1400016ee:	48 8d 0d 2b 00 00 00 	lea    rcx,[rip+0x2b]        # 140001720 <__gcc_deregister_frame>
   1400016f5:	48 83 c4 38          	add    rsp,0x38
   1400016f9:	5b                   	pop    rbx
   1400016fa:	5d                   	pop    rbp
   1400016fb:	e9 2f ff ff ff       	jmp    14000162f <atexit>
   140001700:	48 8d 05 59 ff ff ff 	lea    rax,[rip+0xffffffffffffff59]        # 140001660 <.weak.__deregister_frame_info.hmod_libgcc>
   140001707:	4c 8d 05 42 ff ff ff 	lea    r8,[rip+0xffffffffffffff42]        # 140001650 <.weak.__register_frame_info.hmod_libgcc>
   14000170e:	48 89 05 eb 28 00 00 	mov    QWORD PTR [rip+0x28eb],rax        # 140004000 <__data_start__>
   140001715:	eb c6                	jmp    1400016dd <__gcc_register_frame+0x6d>
   140001717:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000171e:	00 00 

0000000140001720 <__gcc_deregister_frame>:
   140001720:	55                   	push   rbp
   140001721:	48 89 e5             	mov    rbp,rsp
   140001724:	48 83 ec 20          	sub    rsp,0x20
   140001728:	48 8b 05 d1 28 00 00 	mov    rax,QWORD PTR [rip+0x28d1]        # 140004000 <__data_start__>
   14000172f:	48 85 c0             	test   rax,rax
   140001732:	74 09                	je     14000173d <__gcc_deregister_frame+0x1d>
   140001734:	48 8d 0d c5 48 00 00 	lea    rcx,[rip+0x48c5]        # 140006000 <__EH_FRAME_BEGIN__>
   14000173b:	ff d0                	call   rax
   14000173d:	48 8b 0d dc 78 00 00 	mov    rcx,QWORD PTR [rip+0x78dc]        # 140009020 <hmod_libgcc>
   140001744:	48 85 c9             	test   rcx,rcx
   140001747:	74 0f                	je     140001758 <__gcc_deregister_frame+0x38>
   140001749:	48 83 c4 20          	add    rsp,0x20
   14000174d:	5d                   	pop    rbp
   14000174e:	48 ff 25 eb 8a 00 00 	rex.W jmp QWORD PTR [rip+0x8aeb]        # 14000a240 <__imp_FreeLibrary>
   140001755:	0f 1f 00             	nop    DWORD PTR [rax]
   140001758:	48 83 c4 20          	add    rsp,0x20
   14000175c:	5d                   	pop    rbp
   14000175d:	c3                   	ret
   14000175e:	90                   	nop
   14000175f:	90                   	nop

0000000140001760 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]>:
   140001760:	41 57                	push   r15
   140001762:	41 56                	push   r14
   140001764:	41 55                	push   r13
   140001766:	41 54                	push   r12
   140001768:	55                   	push   rbp
   140001769:	57                   	push   rdi
   14000176a:	56                   	push   rsi
   14000176b:	53                   	push   rbx
   14000176c:	48 83 ec 28          	sub    rsp,0x28
   140001770:	48 89 4c 24 70       	mov    QWORD PTR [rsp+0x70],rcx
   140001775:	48 85 c9             	test   rcx,rcx
   140001778:	0f 84 81 01 00 00    	je     1400018ff <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x19f>
   14000177e:	48 8b 44 24 70       	mov    rax,QWORD PTR [rsp+0x70]
   140001783:	4c 8b 68 18          	mov    r13,QWORD PTR [rax+0x18]
   140001787:	4d 85 ed             	test   r13,r13
   14000178a:	0f 84 4a 01 00 00    	je     1400018da <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x17a>
   140001790:	4d 8b 75 18          	mov    r14,QWORD PTR [r13+0x18]
   140001794:	4d 85 f6             	test   r14,r14
   140001797:	0f 84 1f 01 00 00    	je     1400018bc <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x15c>
   14000179d:	4d 8b 7e 18          	mov    r15,QWORD PTR [r14+0x18]
   1400017a1:	4d 85 ff             	test   r15,r15
   1400017a4:	0f 84 f4 00 00 00    	je     14000189e <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x13e>
   1400017aa:	49 8b 5f 18          	mov    rbx,QWORD PTR [r15+0x18]
   1400017ae:	48 85 db             	test   rbx,rbx
   1400017b1:	0f 84 a7 00 00 00    	je     14000185e <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0xfe>
   1400017b7:	48 8b 7b 18          	mov    rdi,QWORD PTR [rbx+0x18]
   1400017bb:	48 85 ff             	test   rdi,rdi
   1400017be:	74 5b                	je     14000181b <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0xbb>
   1400017c0:	48 8b 6f 18          	mov    rbp,QWORD PTR [rdi+0x18]
   1400017c4:	48 85 ed             	test   rbp,rbp
   1400017c7:	74 77                	je     140001840 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0xe0>
   1400017c9:	48 8b 75 18          	mov    rsi,QWORD PTR [rbp+0x18]
   1400017cd:	48 85 f6             	test   rsi,rsi
   1400017d0:	0f 84 aa 00 00 00    	je     140001880 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x120>
   1400017d6:	4c 8b 66 18          	mov    r12,QWORD PTR [rsi+0x18]
   1400017da:	4d 85 e4             	test   r12,r12
   1400017dd:	74 21                	je     140001800 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0xa0>
   1400017df:	49 8b 4c 24 18       	mov    rcx,QWORD PTR [r12+0x18]
   1400017e4:	e8 77 ff ff ff       	call   140001760 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]>
   1400017e9:	4c 89 e1             	mov    rcx,r12
   1400017ec:	4d 8b 64 24 10       	mov    r12,QWORD PTR [r12+0x10]
   1400017f1:	ba 28 00 00 00       	mov    edx,0x28
   1400017f6:	e8 25 01 00 00       	call   140001920 <operator delete(void*, unsigned long long)>
   1400017fb:	4d 85 e4             	test   r12,r12
   1400017fe:	75 df                	jne    1400017df <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x7f>
   140001800:	4c 8b 66 10          	mov    r12,QWORD PTR [rsi+0x10]
   140001804:	ba 28 00 00 00       	mov    edx,0x28
   140001809:	48 89 f1             	mov    rcx,rsi
   14000180c:	e8 0f 01 00 00       	call   140001920 <operator delete(void*, unsigned long long)>
   140001811:	4d 85 e4             	test   r12,r12
   140001814:	74 6a                	je     140001880 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x120>
   140001816:	4c 89 e6             	mov    rsi,r12
   140001819:	eb bb                	jmp    1400017d6 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x76>
   14000181b:	48 8b 73 10          	mov    rsi,QWORD PTR [rbx+0x10]
   14000181f:	ba 28 00 00 00       	mov    edx,0x28
   140001824:	48 89 d9             	mov    rcx,rbx
   140001827:	e8 f4 00 00 00       	call   140001920 <operator delete(void*, unsigned long long)>
   14000182c:	48 85 f6             	test   rsi,rsi
   14000182f:	74 2d                	je     14000185e <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0xfe>
   140001831:	48 89 f3             	mov    rbx,rsi
   140001834:	eb 81                	jmp    1400017b7 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x57>
   140001836:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   14000183d:	00 00 00 
   140001840:	48 8b 77 10          	mov    rsi,QWORD PTR [rdi+0x10]
   140001844:	ba 28 00 00 00       	mov    edx,0x28
   140001849:	48 89 f9             	mov    rcx,rdi
   14000184c:	e8 cf 00 00 00       	call   140001920 <operator delete(void*, unsigned long long)>
   140001851:	48 85 f6             	test   rsi,rsi
   140001854:	74 c5                	je     14000181b <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0xbb>
   140001856:	48 89 f7             	mov    rdi,rsi
   140001859:	e9 62 ff ff ff       	jmp    1400017c0 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x60>
   14000185e:	49 8b 5f 10          	mov    rbx,QWORD PTR [r15+0x10]
   140001862:	ba 28 00 00 00       	mov    edx,0x28
   140001867:	4c 89 f9             	mov    rcx,r15
   14000186a:	e8 b1 00 00 00       	call   140001920 <operator delete(void*, unsigned long long)>
   14000186f:	48 85 db             	test   rbx,rbx
   140001872:	74 2a                	je     14000189e <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x13e>
   140001874:	49 89 df             	mov    r15,rbx
   140001877:	e9 2e ff ff ff       	jmp    1400017aa <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x4a>
   14000187c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   140001880:	48 8b 75 10          	mov    rsi,QWORD PTR [rbp+0x10]
   140001884:	ba 28 00 00 00       	mov    edx,0x28
   140001889:	48 89 e9             	mov    rcx,rbp
   14000188c:	e8 8f 00 00 00       	call   140001920 <operator delete(void*, unsigned long long)>
   140001891:	48 85 f6             	test   rsi,rsi
   140001894:	74 aa                	je     140001840 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0xe0>
   140001896:	48 89 f5             	mov    rbp,rsi
   140001899:	e9 2b ff ff ff       	jmp    1400017c9 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x69>
   14000189e:	49 8b 5e 10          	mov    rbx,QWORD PTR [r14+0x10]
   1400018a2:	ba 28 00 00 00       	mov    edx,0x28
   1400018a7:	4c 89 f1             	mov    rcx,r14
   1400018aa:	e8 71 00 00 00       	call   140001920 <operator delete(void*, unsigned long long)>
   1400018af:	48 85 db             	test   rbx,rbx
   1400018b2:	74 08                	je     1400018bc <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x15c>
   1400018b4:	49 89 de             	mov    r14,rbx
   1400018b7:	e9 e1 fe ff ff       	jmp    14000179d <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x3d>
   1400018bc:	49 8b 5d 10          	mov    rbx,QWORD PTR [r13+0x10]
   1400018c0:	ba 28 00 00 00       	mov    edx,0x28
   1400018c5:	4c 89 e9             	mov    rcx,r13
   1400018c8:	e8 53 00 00 00       	call   140001920 <operator delete(void*, unsigned long long)>
   1400018cd:	48 85 db             	test   rbx,rbx
   1400018d0:	74 08                	je     1400018da <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x17a>
   1400018d2:	49 89 dd             	mov    r13,rbx
   1400018d5:	e9 b6 fe ff ff       	jmp    140001790 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x30>
   1400018da:	48 8b 44 24 70       	mov    rax,QWORD PTR [rsp+0x70]
   1400018df:	ba 28 00 00 00       	mov    edx,0x28
   1400018e4:	48 8b 58 10          	mov    rbx,QWORD PTR [rax+0x10]
   1400018e8:	48 89 c1             	mov    rcx,rax
   1400018eb:	e8 30 00 00 00       	call   140001920 <operator delete(void*, unsigned long long)>
   1400018f0:	48 85 db             	test   rbx,rbx
   1400018f3:	74 0a                	je     1400018ff <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x19f>
   1400018f5:	48 89 5c 24 70       	mov    QWORD PTR [rsp+0x70],rbx
   1400018fa:	e9 7f fe ff ff       	jmp    14000177e <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]+0x1e>
   1400018ff:	48 83 c4 28          	add    rsp,0x28
   140001903:	5b                   	pop    rbx
   140001904:	5e                   	pop    rsi
   140001905:	5f                   	pop    rdi
   140001906:	5d                   	pop    rbp
   140001907:	41 5c                	pop    r12
   140001909:	41 5d                	pop    r13
   14000190b:	41 5e                	pop    r14
   14000190d:	41 5f                	pop    r15
   14000190f:	c3                   	ret

0000000140001910 <__gxx_personality_seh0>:
   140001910:	ff 25 0a 89 00 00    	jmp    QWORD PTR [rip+0x890a]        # 14000a220 <__imp___gxx_personality_seh0>
   140001916:	90                   	nop
   140001917:	90                   	nop

0000000140001918 <operator new(unsigned long long)>:
   140001918:	ff 25 fa 88 00 00    	jmp    QWORD PTR [rip+0x88fa]        # 14000a218 <__imp__Znwy>
   14000191e:	90                   	nop
   14000191f:	90                   	nop

0000000140001920 <operator delete(void*, unsigned long long)>:
   140001920:	ff 25 ea 88 00 00    	jmp    QWORD PTR [rip+0x88ea]        # 14000a210 <__imp__ZdlPvy>
   140001926:	90                   	nop
   140001927:	90                   	nop

0000000140001928 <std::_Rb_tree_insert_and_rebalance(bool, std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, std::_Rb_tree_node_base&)>:
   140001928:	ff 25 da 88 00 00    	jmp    QWORD PTR [rip+0x88da]        # 14000a208 <__imp__ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_>
   14000192e:	90                   	nop
   14000192f:	90                   	nop

0000000140001930 <std::_Rb_tree_decrement(std::_Rb_tree_node_base*)>:
   140001930:	ff 25 ca 88 00 00    	jmp    QWORD PTR [rip+0x88ca]        # 14000a200 <__imp__ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base>
   140001936:	90                   	nop
   140001937:	90                   	nop
   140001938:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000193f:	00 

0000000140001940 <__do_global_dtors>:
   140001940:	55                   	push   rbp
   140001941:	48 89 e5             	mov    rbp,rsp
   140001944:	48 83 ec 20          	sub    rsp,0x20
   140001948:	eb 1e                	jmp    140001968 <__do_global_dtors+0x28>
   14000194a:	48 8b 05 bf 26 00 00 	mov    rax,QWORD PTR [rip+0x26bf]        # 140004010 <p.0>
   140001951:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001954:	ff d0                	call   rax
   140001956:	48 8b 05 b3 26 00 00 	mov    rax,QWORD PTR [rip+0x26b3]        # 140004010 <p.0>
   14000195d:	48 83 c0 08          	add    rax,0x8
   140001961:	48 89 05 a8 26 00 00 	mov    QWORD PTR [rip+0x26a8],rax        # 140004010 <p.0>
   140001968:	48 8b 05 a1 26 00 00 	mov    rax,QWORD PTR [rip+0x26a1]        # 140004010 <p.0>
   14000196f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001972:	48 85 c0             	test   rax,rax
   140001975:	75 d3                	jne    14000194a <__do_global_dtors+0xa>
   140001977:	90                   	nop
   140001978:	90                   	nop
   140001979:	48 83 c4 20          	add    rsp,0x20
   14000197d:	5d                   	pop    rbp
   14000197e:	c3                   	ret

000000014000197f <__do_global_ctors>:
   14000197f:	55                   	push   rbp
   140001980:	48 89 e5             	mov    rbp,rsp
   140001983:	48 83 ec 30          	sub    rsp,0x30
   140001987:	48 8b 05 c2 39 00 00 	mov    rax,QWORD PTR [rip+0x39c2]        # 140005350 <.refptr.__CTOR_LIST__>
   14000198e:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001991:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140001994:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
   140001998:	75 25                	jne    1400019bf <__do_global_ctors+0x40>
   14000199a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400019a1:	eb 04                	jmp    1400019a7 <__do_global_ctors+0x28>
   1400019a3:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   1400019a7:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400019aa:	8d 50 01             	lea    edx,[rax+0x1]
   1400019ad:	48 8b 05 9c 39 00 00 	mov    rax,QWORD PTR [rip+0x399c]        # 140005350 <.refptr.__CTOR_LIST__>
   1400019b4:	89 d2                	mov    edx,edx
   1400019b6:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   1400019ba:	48 85 c0             	test   rax,rax
   1400019bd:	75 e4                	jne    1400019a3 <__do_global_ctors+0x24>
   1400019bf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400019c2:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   1400019c5:	eb 14                	jmp    1400019db <__do_global_ctors+0x5c>
   1400019c7:	48 8b 05 82 39 00 00 	mov    rax,QWORD PTR [rip+0x3982]        # 140005350 <.refptr.__CTOR_LIST__>
   1400019ce:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   1400019d1:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   1400019d5:	ff d0                	call   rax
   1400019d7:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   1400019db:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   1400019df:	75 e6                	jne    1400019c7 <__do_global_ctors+0x48>
   1400019e1:	48 8d 05 58 ff ff ff 	lea    rax,[rip+0xffffffffffffff58]        # 140001940 <__do_global_dtors>
   1400019e8:	48 89 c1             	mov    rcx,rax
   1400019eb:	e8 3f fc ff ff       	call   14000162f <atexit>
   1400019f0:	90                   	nop
   1400019f1:	48 83 c4 30          	add    rsp,0x30
   1400019f5:	5d                   	pop    rbp
   1400019f6:	c3                   	ret

00000001400019f7 <__main>:
   1400019f7:	55                   	push   rbp
   1400019f8:	48 89 e5             	mov    rbp,rsp
   1400019fb:	48 83 ec 20          	sub    rsp,0x20
   1400019ff:	8b 05 7b 76 00 00    	mov    eax,DWORD PTR [rip+0x767b]        # 140009080 <initialized>
   140001a05:	85 c0                	test   eax,eax
   140001a07:	75 0f                	jne    140001a18 <__main+0x21>
   140001a09:	c7 05 6d 76 00 00 01 	mov    DWORD PTR [rip+0x766d],0x1        # 140009080 <initialized>
   140001a10:	00 00 00 
   140001a13:	e8 67 ff ff ff       	call   14000197f <__do_global_ctors>
   140001a18:	90                   	nop
   140001a19:	48 83 c4 20          	add    rsp,0x20
   140001a1d:	5d                   	pop    rbp
   140001a1e:	c3                   	ret
   140001a1f:	90                   	nop

0000000140001a20 <_setargv>:
   140001a20:	55                   	push   rbp
   140001a21:	48 89 e5             	mov    rbp,rsp
   140001a24:	b8 00 00 00 00       	mov    eax,0x0
   140001a29:	5d                   	pop    rbp
   140001a2a:	c3                   	ret
   140001a2b:	90                   	nop
   140001a2c:	90                   	nop
   140001a2d:	90                   	nop
   140001a2e:	90                   	nop
   140001a2f:	90                   	nop

0000000140001a30 <__dyn_tls_init>:
   140001a30:	55                   	push   rbp
   140001a31:	48 89 e5             	mov    rbp,rsp
   140001a34:	48 83 ec 30          	sub    rsp,0x30
   140001a38:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001a3c:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001a3f:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001a43:	48 8b 05 e6 38 00 00 	mov    rax,QWORD PTR [rip+0x38e6]        # 140005330 <.refptr._CRT_MT>
   140001a4a:	8b 00                	mov    eax,DWORD PTR [rax]
   140001a4c:	83 f8 02             	cmp    eax,0x2
   140001a4f:	74 0d                	je     140001a5e <__dyn_tls_init+0x2e>
   140001a51:	48 8b 05 d8 38 00 00 	mov    rax,QWORD PTR [rip+0x38d8]        # 140005330 <.refptr._CRT_MT>
   140001a58:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   140001a5e:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140001a62:	74 1e                	je     140001a82 <__dyn_tls_init+0x52>
   140001a64:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140001a68:	75 5b                	jne    140001ac5 <__dyn_tls_init+0x95>
   140001a6a:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001a6e:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   140001a71:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001a75:	49 89 c8             	mov    r8,rcx
   140001a78:	48 89 c1             	mov    rcx,rax
   140001a7b:	e8 d1 11 00 00       	call   140002c51 <__mingw_TLScallback>
   140001a80:	eb 43                	jmp    140001ac5 <__dyn_tls_init+0x95>
   140001a82:	48 8d 05 0f 3c 00 00 	lea    rax,[rip+0x3c0f]        # 140005698 <___crt_xd_start__>
   140001a89:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a8d:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001a92:	eb 22                	jmp    140001ab6 <__dyn_tls_init+0x86>
   140001a94:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001a98:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001a9c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001aa0:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001aa3:	48 85 c0             	test   rax,rax
   140001aa6:	74 09                	je     140001ab1 <__dyn_tls_init+0x81>
   140001aa8:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001aac:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001aaf:	ff d0                	call   rax
   140001ab1:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001ab6:	48 8d 05 e3 3b 00 00 	lea    rax,[rip+0x3be3]        # 1400056a0 <__xd_z>
   140001abd:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140001ac1:	75 d1                	jne    140001a94 <__dyn_tls_init+0x64>
   140001ac3:	eb 01                	jmp    140001ac6 <__dyn_tls_init+0x96>
   140001ac5:	90                   	nop
   140001ac6:	48 83 c4 30          	add    rsp,0x30
   140001aca:	5d                   	pop    rbp
   140001acb:	c3                   	ret

0000000140001acc <__tlregdtor>:
   140001acc:	55                   	push   rbp
   140001acd:	48 89 e5             	mov    rbp,rsp
   140001ad0:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001ad4:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140001ad9:	75 07                	jne    140001ae2 <__tlregdtor+0x16>
   140001adb:	b8 00 00 00 00       	mov    eax,0x0
   140001ae0:	eb 05                	jmp    140001ae7 <__tlregdtor+0x1b>
   140001ae2:	b8 00 00 00 00       	mov    eax,0x0
   140001ae7:	5d                   	pop    rbp
   140001ae8:	c3                   	ret

0000000140001ae9 <__dyn_tls_dtor>:
   140001ae9:	55                   	push   rbp
   140001aea:	48 89 e5             	mov    rbp,rsp
   140001aed:	48 83 ec 20          	sub    rsp,0x20
   140001af1:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001af5:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001af8:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001afc:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140001b00:	74 06                	je     140001b08 <__dyn_tls_dtor+0x1f>
   140001b02:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140001b06:	75 18                	jne    140001b20 <__dyn_tls_dtor+0x37>
   140001b08:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001b0c:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   140001b0f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001b13:	49 89 c8             	mov    r8,rcx
   140001b16:	48 89 c1             	mov    rcx,rax
   140001b19:	e8 33 11 00 00       	call   140002c51 <__mingw_TLScallback>
   140001b1e:	eb 01                	jmp    140001b21 <__dyn_tls_dtor+0x38>
   140001b20:	90                   	nop
   140001b21:	48 83 c4 20          	add    rsp,0x20
   140001b25:	5d                   	pop    rbp
   140001b26:	c3                   	ret
   140001b27:	90                   	nop
   140001b28:	90                   	nop
   140001b29:	90                   	nop
   140001b2a:	90                   	nop
   140001b2b:	90                   	nop
   140001b2c:	90                   	nop
   140001b2d:	90                   	nop
   140001b2e:	90                   	nop
   140001b2f:	90                   	nop

0000000140001b30 <_matherr>:
   140001b30:	55                   	push   rbp
   140001b31:	53                   	push   rbx
   140001b32:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140001b39:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140001b3e:	0f 29 75 00          	movaps XMMWORD PTR [rbp+0x0],xmm6
   140001b42:	0f 29 7d 10          	movaps XMMWORD PTR [rbp+0x10],xmm7
   140001b46:	44 0f 29 45 20       	movaps XMMWORD PTR [rbp+0x20],xmm8
   140001b4b:	48 89 4d 50          	mov    QWORD PTR [rbp+0x50],rcx
   140001b4f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001b53:	8b 00                	mov    eax,DWORD PTR [rax]
   140001b55:	83 f8 06             	cmp    eax,0x6
   140001b58:	74 56                	je     140001bb0 <_matherr+0x80>
   140001b5a:	83 f8 06             	cmp    eax,0x6
   140001b5d:	7f 78                	jg     140001bd7 <_matherr+0xa7>
   140001b5f:	83 f8 05             	cmp    eax,0x5
   140001b62:	74 59                	je     140001bbd <_matherr+0x8d>
   140001b64:	83 f8 05             	cmp    eax,0x5
   140001b67:	7f 6e                	jg     140001bd7 <_matherr+0xa7>
   140001b69:	83 f8 04             	cmp    eax,0x4
   140001b6c:	74 5c                	je     140001bca <_matherr+0x9a>
   140001b6e:	83 f8 04             	cmp    eax,0x4
   140001b71:	7f 64                	jg     140001bd7 <_matherr+0xa7>
   140001b73:	83 f8 03             	cmp    eax,0x3
   140001b76:	74 2b                	je     140001ba3 <_matherr+0x73>
   140001b78:	83 f8 03             	cmp    eax,0x3
   140001b7b:	7f 5a                	jg     140001bd7 <_matherr+0xa7>
   140001b7d:	83 f8 01             	cmp    eax,0x1
   140001b80:	74 07                	je     140001b89 <_matherr+0x59>
   140001b82:	83 f8 02             	cmp    eax,0x2
   140001b85:	74 0f                	je     140001b96 <_matherr+0x66>
   140001b87:	eb 4e                	jmp    140001bd7 <_matherr+0xa7>
   140001b89:	48 8d 05 10 35 00 00 	lea    rax,[rip+0x3510]        # 1400050a0 <.rdata>
   140001b90:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001b94:	eb 4d                	jmp    140001be3 <_matherr+0xb3>
   140001b96:	48 8d 05 22 35 00 00 	lea    rax,[rip+0x3522]        # 1400050bf <.rdata+0x1f>
   140001b9d:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001ba1:	eb 40                	jmp    140001be3 <_matherr+0xb3>
   140001ba3:	48 8d 05 36 35 00 00 	lea    rax,[rip+0x3536]        # 1400050e0 <.rdata+0x40>
   140001baa:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001bae:	eb 33                	jmp    140001be3 <_matherr+0xb3>
   140001bb0:	48 8d 05 49 35 00 00 	lea    rax,[rip+0x3549]        # 140005100 <.rdata+0x60>
   140001bb7:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001bbb:	eb 26                	jmp    140001be3 <_matherr+0xb3>
   140001bbd:	48 8d 05 64 35 00 00 	lea    rax,[rip+0x3564]        # 140005128 <.rdata+0x88>
   140001bc4:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001bc8:	eb 19                	jmp    140001be3 <_matherr+0xb3>
   140001bca:	48 8d 05 7f 35 00 00 	lea    rax,[rip+0x357f]        # 140005150 <.rdata+0xb0>
   140001bd1:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001bd5:	eb 0c                	jmp    140001be3 <_matherr+0xb3>
   140001bd7:	48 8d 05 a8 35 00 00 	lea    rax,[rip+0x35a8]        # 140005186 <.rdata+0xe6>
   140001bde:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001be2:	90                   	nop
   140001be3:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001be7:	f2 44 0f 10 40 20    	movsd  xmm8,QWORD PTR [rax+0x20]
   140001bed:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001bf1:	f2 0f 10 78 18       	movsd  xmm7,QWORD PTR [rax+0x18]
   140001bf6:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001bfa:	f2 0f 10 70 10       	movsd  xmm6,QWORD PTR [rax+0x10]
   140001bff:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001c03:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
   140001c07:	b9 02 00 00 00       	mov    ecx,0x2
   140001c0c:	e8 3f 17 00 00       	call   140003350 <__acrt_iob_func>
   140001c11:	48 89 c1             	mov    rcx,rax
   140001c14:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140001c18:	48 8d 05 79 35 00 00 	lea    rax,[rip+0x3579]        # 140005198 <.rdata+0xf8>
   140001c1f:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001c26:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001c2c:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001c32:	49 89 d9             	mov    r9,rbx
   140001c35:	49 89 d0             	mov    r8,rdx
   140001c38:	48 89 c2             	mov    rdx,rax
   140001c3b:	e8 a8 17 00 00       	call   1400033e8 <fprintf>
   140001c40:	b8 00 00 00 00       	mov    eax,0x0
   140001c45:	0f 28 75 00          	movaps xmm6,XMMWORD PTR [rbp+0x0]
   140001c49:	0f 28 7d 10          	movaps xmm7,XMMWORD PTR [rbp+0x10]
   140001c4d:	44 0f 28 45 20       	movaps xmm8,XMMWORD PTR [rbp+0x20]
   140001c52:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140001c59:	5b                   	pop    rbx
   140001c5a:	5d                   	pop    rbp
   140001c5b:	c3                   	ret
   140001c5c:	90                   	nop
   140001c5d:	90                   	nop
   140001c5e:	90                   	nop
   140001c5f:	90                   	nop

0000000140001c60 <__report_error>:
   140001c60:	55                   	push   rbp
   140001c61:	53                   	push   rbx
   140001c62:	48 83 ec 38          	sub    rsp,0x38
   140001c66:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140001c6b:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140001c6f:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001c73:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140001c77:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140001c7b:	48 8d 45 28          	lea    rax,[rbp+0x28]
   140001c7f:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001c83:	b9 02 00 00 00       	mov    ecx,0x2
   140001c88:	e8 c3 16 00 00       	call   140003350 <__acrt_iob_func>
   140001c8d:	48 89 c1             	mov    rcx,rax
   140001c90:	48 8d 05 39 35 00 00 	lea    rax,[rip+0x3539]        # 1400051d0 <.rdata>
   140001c97:	48 89 c2             	mov    rdx,rax
   140001c9a:	e8 49 17 00 00       	call   1400033e8 <fprintf>
   140001c9f:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   140001ca3:	b9 02 00 00 00       	mov    ecx,0x2
   140001ca8:	e8 a3 16 00 00       	call   140003350 <__acrt_iob_func>
   140001cad:	48 89 c1             	mov    rcx,rax
   140001cb0:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001cb4:	49 89 d8             	mov    r8,rbx
   140001cb7:	48 89 c2             	mov    rdx,rax
   140001cba:	e8 69 17 00 00       	call   140003428 <vfprintf>
   140001cbf:	e8 04 17 00 00       	call   1400033c8 <abort>
   140001cc4:	90                   	nop

0000000140001cc5 <mark_section_writable>:
   140001cc5:	55                   	push   rbp
   140001cc6:	48 89 e5             	mov    rbp,rsp
   140001cc9:	48 83 ec 60          	sub    rsp,0x60
   140001ccd:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001cd1:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001cd8:	e9 82 00 00 00       	jmp    140001d5f <mark_section_writable+0x9a>
   140001cdd:	48 8b 0d fc 73 00 00 	mov    rcx,QWORD PTR [rip+0x73fc]        # 1400090e0 <the_secs>
   140001ce4:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001ce7:	48 63 d0             	movsxd rdx,eax
   140001cea:	48 89 d0             	mov    rax,rdx
   140001ced:	48 c1 e0 02          	shl    rax,0x2
   140001cf1:	48 01 d0             	add    rax,rdx
   140001cf4:	48 c1 e0 03          	shl    rax,0x3
   140001cf8:	48 01 c8             	add    rax,rcx
   140001cfb:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001cff:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001d03:	72 56                	jb     140001d5b <mark_section_writable+0x96>
   140001d05:	48 8b 0d d4 73 00 00 	mov    rcx,QWORD PTR [rip+0x73d4]        # 1400090e0 <the_secs>
   140001d0c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d0f:	48 63 d0             	movsxd rdx,eax
   140001d12:	48 89 d0             	mov    rax,rdx
   140001d15:	48 c1 e0 02          	shl    rax,0x2
   140001d19:	48 01 d0             	add    rax,rdx
   140001d1c:	48 c1 e0 03          	shl    rax,0x3
   140001d20:	48 01 c8             	add    rax,rcx
   140001d23:	48 8b 48 18          	mov    rcx,QWORD PTR [rax+0x18]
   140001d27:	4c 8b 05 b2 73 00 00 	mov    r8,QWORD PTR [rip+0x73b2]        # 1400090e0 <the_secs>
   140001d2e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d31:	48 63 d0             	movsxd rdx,eax
   140001d34:	48 89 d0             	mov    rax,rdx
   140001d37:	48 c1 e0 02          	shl    rax,0x2
   140001d3b:	48 01 d0             	add    rax,rdx
   140001d3e:	48 c1 e0 03          	shl    rax,0x3
   140001d42:	4c 01 c0             	add    rax,r8
   140001d45:	48 8b 40 20          	mov    rax,QWORD PTR [rax+0x20]
   140001d49:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001d4c:	89 c0                	mov    eax,eax
   140001d4e:	48 01 c8             	add    rax,rcx
   140001d51:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001d55:	0f 82 41 02 00 00    	jb     140001f9c <mark_section_writable+0x2d7>
   140001d5b:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001d5f:	8b 05 83 73 00 00    	mov    eax,DWORD PTR [rip+0x7383]        # 1400090e8 <maxSections>
   140001d65:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001d68:	0f 8c 6f ff ff ff    	jl     140001cdd <mark_section_writable+0x18>
   140001d6e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001d72:	48 89 c1             	mov    rcx,rax
   140001d75:	e8 c1 11 00 00       	call   140002f3b <__mingw_GetSectionForAddress>
   140001d7a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001d7e:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001d83:	75 13                	jne    140001d98 <mark_section_writable+0xd3>
   140001d85:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001d89:	48 8d 0d 60 34 00 00 	lea    rcx,[rip+0x3460]        # 1400051f0 <.rdata+0x20>
   140001d90:	48 89 c2             	mov    rdx,rax
   140001d93:	e8 c8 fe ff ff       	call   140001c60 <__report_error>
   140001d98:	48 8b 0d 41 73 00 00 	mov    rcx,QWORD PTR [rip+0x7341]        # 1400090e0 <the_secs>
   140001d9f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001da2:	48 63 d0             	movsxd rdx,eax
   140001da5:	48 89 d0             	mov    rax,rdx
   140001da8:	48 c1 e0 02          	shl    rax,0x2
   140001dac:	48 01 d0             	add    rax,rdx
   140001daf:	48 c1 e0 03          	shl    rax,0x3
   140001db3:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001db7:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001dbb:	48 89 42 20          	mov    QWORD PTR [rdx+0x20],rax
   140001dbf:	48 8b 0d 1a 73 00 00 	mov    rcx,QWORD PTR [rip+0x731a]        # 1400090e0 <the_secs>
   140001dc6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001dc9:	48 63 d0             	movsxd rdx,eax
   140001dcc:	48 89 d0             	mov    rax,rdx
   140001dcf:	48 c1 e0 02          	shl    rax,0x2
   140001dd3:	48 01 d0             	add    rax,rdx
   140001dd6:	48 c1 e0 03          	shl    rax,0x3
   140001dda:	48 01 c8             	add    rax,rcx
   140001ddd:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001de3:	e8 9f 12 00 00       	call   140003087 <_GetPEImageBase>
   140001de8:	48 89 c1             	mov    rcx,rax
   140001deb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001def:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140001df2:	41 89 c1             	mov    r9d,eax
   140001df5:	4c 8b 05 e4 72 00 00 	mov    r8,QWORD PTR [rip+0x72e4]        # 1400090e0 <the_secs>
   140001dfc:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001dff:	48 63 d0             	movsxd rdx,eax
   140001e02:	48 89 d0             	mov    rax,rdx
   140001e05:	48 c1 e0 02          	shl    rax,0x2
   140001e09:	48 01 d0             	add    rax,rdx
   140001e0c:	48 c1 e0 03          	shl    rax,0x3
   140001e10:	4c 01 c0             	add    rax,r8
   140001e13:	4a 8d 14 09          	lea    rdx,[rcx+r9*1]
   140001e17:	48 89 50 18          	mov    QWORD PTR [rax+0x18],rdx
   140001e1b:	48 8b 0d be 72 00 00 	mov    rcx,QWORD PTR [rip+0x72be]        # 1400090e0 <the_secs>
   140001e22:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e25:	48 63 d0             	movsxd rdx,eax
   140001e28:	48 89 d0             	mov    rax,rdx
   140001e2b:	48 c1 e0 02          	shl    rax,0x2
   140001e2f:	48 01 d0             	add    rax,rdx
   140001e32:	48 c1 e0 03          	shl    rax,0x3
   140001e36:	48 01 c8             	add    rax,rcx
   140001e39:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001e3d:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140001e41:	41 b8 30 00 00 00    	mov    r8d,0x30
   140001e47:	48 89 c1             	mov    rcx,rax
   140001e4a:	48 8b 05 47 84 00 00 	mov    rax,QWORD PTR [rip+0x8447]        # 14000a298 <__imp_VirtualQuery>
   140001e51:	ff d0                	call   rax
   140001e53:	48 85 c0             	test   rax,rax
   140001e56:	75 3f                	jne    140001e97 <mark_section_writable+0x1d2>
   140001e58:	48 8b 0d 81 72 00 00 	mov    rcx,QWORD PTR [rip+0x7281]        # 1400090e0 <the_secs>
   140001e5f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e62:	48 63 d0             	movsxd rdx,eax
   140001e65:	48 89 d0             	mov    rax,rdx
   140001e68:	48 c1 e0 02          	shl    rax,0x2
   140001e6c:	48 01 d0             	add    rax,rdx
   140001e6f:	48 c1 e0 03          	shl    rax,0x3
   140001e73:	48 01 c8             	add    rax,rcx
   140001e76:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
   140001e7a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001e7e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001e81:	89 c1                	mov    ecx,eax
   140001e83:	48 8d 05 86 33 00 00 	lea    rax,[rip+0x3386]        # 140005210 <.rdata+0x40>
   140001e8a:	49 89 d0             	mov    r8,rdx
   140001e8d:	89 ca                	mov    edx,ecx
   140001e8f:	48 89 c1             	mov    rcx,rax
   140001e92:	e8 c9 fd ff ff       	call   140001c60 <__report_error>
   140001e97:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001e9a:	83 f8 40             	cmp    eax,0x40
   140001e9d:	0f 84 e8 00 00 00    	je     140001f8b <mark_section_writable+0x2c6>
   140001ea3:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001ea6:	83 f8 04             	cmp    eax,0x4
   140001ea9:	0f 84 dc 00 00 00    	je     140001f8b <mark_section_writable+0x2c6>
   140001eaf:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001eb2:	3d 80 00 00 00       	cmp    eax,0x80
   140001eb7:	0f 84 ce 00 00 00    	je     140001f8b <mark_section_writable+0x2c6>
   140001ebd:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001ec0:	83 f8 08             	cmp    eax,0x8
   140001ec3:	0f 84 c2 00 00 00    	je     140001f8b <mark_section_writable+0x2c6>
   140001ec9:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001ecc:	83 f8 02             	cmp    eax,0x2
   140001ecf:	75 09                	jne    140001eda <mark_section_writable+0x215>
   140001ed1:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140001ed8:	eb 07                	jmp    140001ee1 <mark_section_writable+0x21c>
   140001eda:	c7 45 f8 40 00 00 00 	mov    DWORD PTR [rbp-0x8],0x40
   140001ee1:	48 8b 0d f8 71 00 00 	mov    rcx,QWORD PTR [rip+0x71f8]        # 1400090e0 <the_secs>
   140001ee8:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001eeb:	48 63 d0             	movsxd rdx,eax
   140001eee:	48 89 d0             	mov    rax,rdx
   140001ef1:	48 c1 e0 02          	shl    rax,0x2
   140001ef5:	48 01 d0             	add    rax,rdx
   140001ef8:	48 c1 e0 03          	shl    rax,0x3
   140001efc:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001f00:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001f04:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   140001f08:	48 8b 0d d1 71 00 00 	mov    rcx,QWORD PTR [rip+0x71d1]        # 1400090e0 <the_secs>
   140001f0f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001f12:	48 63 d0             	movsxd rdx,eax
   140001f15:	48 89 d0             	mov    rax,rdx
   140001f18:	48 c1 e0 02          	shl    rax,0x2
   140001f1c:	48 01 d0             	add    rax,rdx
   140001f1f:	48 c1 e0 03          	shl    rax,0x3
   140001f23:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001f27:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140001f2b:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   140001f2f:	48 8b 0d aa 71 00 00 	mov    rcx,QWORD PTR [rip+0x71aa]        # 1400090e0 <the_secs>
   140001f36:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001f39:	48 63 d0             	movsxd rdx,eax
   140001f3c:	48 89 d0             	mov    rax,rdx
   140001f3f:	48 c1 e0 02          	shl    rax,0x2
   140001f43:	48 01 d0             	add    rax,rdx
   140001f46:	48 c1 e0 03          	shl    rax,0x3
   140001f4a:	48 01 c8             	add    rax,rcx
   140001f4d:	49 89 c0             	mov    r8,rax
   140001f50:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   140001f54:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001f58:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   140001f5b:	4d 89 c1             	mov    r9,r8
   140001f5e:	41 89 c8             	mov    r8d,ecx
   140001f61:	48 89 c1             	mov    rcx,rax
   140001f64:	48 8b 05 25 83 00 00 	mov    rax,QWORD PTR [rip+0x8325]        # 14000a290 <__imp_VirtualProtect>
   140001f6b:	ff d0                	call   rax
   140001f6d:	85 c0                	test   eax,eax
   140001f6f:	75 1a                	jne    140001f8b <mark_section_writable+0x2c6>
   140001f71:	48 8b 05 d0 82 00 00 	mov    rax,QWORD PTR [rip+0x82d0]        # 14000a248 <__imp_GetLastError>
   140001f78:	ff d0                	call   rax
   140001f7a:	89 c2                	mov    edx,eax
   140001f7c:	48 8d 05 c5 32 00 00 	lea    rax,[rip+0x32c5]        # 140005248 <.rdata+0x78>
   140001f83:	48 89 c1             	mov    rcx,rax
   140001f86:	e8 d5 fc ff ff       	call   140001c60 <__report_error>
   140001f8b:	8b 05 57 71 00 00    	mov    eax,DWORD PTR [rip+0x7157]        # 1400090e8 <maxSections>
   140001f91:	83 c0 01             	add    eax,0x1
   140001f94:	89 05 4e 71 00 00    	mov    DWORD PTR [rip+0x714e],eax        # 1400090e8 <maxSections>
   140001f9a:	eb 01                	jmp    140001f9d <mark_section_writable+0x2d8>
   140001f9c:	90                   	nop
   140001f9d:	48 83 c4 60          	add    rsp,0x60
   140001fa1:	5d                   	pop    rbp
   140001fa2:	c3                   	ret

0000000140001fa3 <restore_modified_sections>:
   140001fa3:	55                   	push   rbp
   140001fa4:	48 89 e5             	mov    rbp,rsp
   140001fa7:	48 83 ec 30          	sub    rsp,0x30
   140001fab:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001fb2:	e9 ad 00 00 00       	jmp    140002064 <restore_modified_sections+0xc1>
   140001fb7:	48 8b 0d 22 71 00 00 	mov    rcx,QWORD PTR [rip+0x7122]        # 1400090e0 <the_secs>
   140001fbe:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001fc1:	48 63 d0             	movsxd rdx,eax
   140001fc4:	48 89 d0             	mov    rax,rdx
   140001fc7:	48 c1 e0 02          	shl    rax,0x2
   140001fcb:	48 01 d0             	add    rax,rdx
   140001fce:	48 c1 e0 03          	shl    rax,0x3
   140001fd2:	48 01 c8             	add    rax,rcx
   140001fd5:	8b 00                	mov    eax,DWORD PTR [rax]
   140001fd7:	85 c0                	test   eax,eax
   140001fd9:	0f 84 80 00 00 00    	je     14000205f <restore_modified_sections+0xbc>
   140001fdf:	48 8b 0d fa 70 00 00 	mov    rcx,QWORD PTR [rip+0x70fa]        # 1400090e0 <the_secs>
   140001fe6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001fe9:	48 63 d0             	movsxd rdx,eax
   140001fec:	48 89 d0             	mov    rax,rdx
   140001fef:	48 c1 e0 02          	shl    rax,0x2
   140001ff3:	48 01 d0             	add    rax,rdx
   140001ff6:	48 c1 e0 03          	shl    rax,0x3
   140001ffa:	48 01 c8             	add    rax,rcx
   140001ffd:	44 8b 10             	mov    r10d,DWORD PTR [rax]
   140002000:	48 8b 0d d9 70 00 00 	mov    rcx,QWORD PTR [rip+0x70d9]        # 1400090e0 <the_secs>
   140002007:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000200a:	48 63 d0             	movsxd rdx,eax
   14000200d:	48 89 d0             	mov    rax,rdx
   140002010:	48 c1 e0 02          	shl    rax,0x2
   140002014:	48 01 d0             	add    rax,rdx
   140002017:	48 c1 e0 03          	shl    rax,0x3
   14000201b:	48 01 c8             	add    rax,rcx
   14000201e:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   140002022:	4c 8b 05 b7 70 00 00 	mov    r8,QWORD PTR [rip+0x70b7]        # 1400090e0 <the_secs>
   140002029:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000202c:	48 63 d0             	movsxd rdx,eax
   14000202f:	48 89 d0             	mov    rax,rdx
   140002032:	48 c1 e0 02          	shl    rax,0x2
   140002036:	48 01 d0             	add    rax,rdx
   140002039:	48 c1 e0 03          	shl    rax,0x3
   14000203d:	4c 01 c0             	add    rax,r8
   140002040:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   140002044:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   140002048:	49 89 d1             	mov    r9,rdx
   14000204b:	45 89 d0             	mov    r8d,r10d
   14000204e:	48 89 ca             	mov    rdx,rcx
   140002051:	48 89 c1             	mov    rcx,rax
   140002054:	48 8b 05 35 82 00 00 	mov    rax,QWORD PTR [rip+0x8235]        # 14000a290 <__imp_VirtualProtect>
   14000205b:	ff d0                	call   rax
   14000205d:	eb 01                	jmp    140002060 <restore_modified_sections+0xbd>
   14000205f:	90                   	nop
   140002060:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140002064:	8b 05 7e 70 00 00    	mov    eax,DWORD PTR [rip+0x707e]        # 1400090e8 <maxSections>
   14000206a:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   14000206d:	0f 8c 44 ff ff ff    	jl     140001fb7 <restore_modified_sections+0x14>
   140002073:	90                   	nop
   140002074:	90                   	nop
   140002075:	48 83 c4 30          	add    rsp,0x30
   140002079:	5d                   	pop    rbp
   14000207a:	c3                   	ret

000000014000207b <__write_memory>:
   14000207b:	55                   	push   rbp
   14000207c:	48 89 e5             	mov    rbp,rsp
   14000207f:	48 83 ec 20          	sub    rsp,0x20
   140002083:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002087:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000208b:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   14000208f:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140002094:	74 25                	je     1400020bb <__write_memory+0x40>
   140002096:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000209a:	48 89 c1             	mov    rcx,rax
   14000209d:	e8 23 fc ff ff       	call   140001cc5 <mark_section_writable>
   1400020a2:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   1400020a6:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400020aa:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400020ae:	49 89 c8             	mov    r8,rcx
   1400020b1:	48 89 c1             	mov    rcx,rax
   1400020b4:	e8 47 13 00 00       	call   140003400 <memcpy>
   1400020b9:	eb 01                	jmp    1400020bc <__write_memory+0x41>
   1400020bb:	90                   	nop
   1400020bc:	48 83 c4 20          	add    rsp,0x20
   1400020c0:	5d                   	pop    rbp
   1400020c1:	c3                   	ret

00000001400020c2 <do_pseudo_reloc>:
   1400020c2:	55                   	push   rbp
   1400020c3:	48 89 e5             	mov    rbp,rsp
   1400020c6:	48 83 c4 80          	add    rsp,0xffffffffffffff80
   1400020ca:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400020ce:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400020d2:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400020d6:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400020da:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   1400020de:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400020e2:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400020e6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400020ea:	48 83 7d e0 07       	cmp    QWORD PTR [rbp-0x20],0x7
   1400020ef:	0f 8e 44 03 00 00    	jle    140002439 <do_pseudo_reloc+0x377>
   1400020f5:	48 83 7d e0 0b       	cmp    QWORD PTR [rbp-0x20],0xb
   1400020fa:	7e 25                	jle    140002121 <do_pseudo_reloc+0x5f>
   1400020fc:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002100:	8b 00                	mov    eax,DWORD PTR [rax]
   140002102:	85 c0                	test   eax,eax
   140002104:	75 1b                	jne    140002121 <do_pseudo_reloc+0x5f>
   140002106:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000210a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000210d:	85 c0                	test   eax,eax
   14000210f:	75 10                	jne    140002121 <do_pseudo_reloc+0x5f>
   140002111:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002115:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002118:	85 c0                	test   eax,eax
   14000211a:	75 05                	jne    140002121 <do_pseudo_reloc+0x5f>
   14000211c:	48 83 45 f8 0c       	add    QWORD PTR [rbp-0x8],0xc
   140002121:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002125:	8b 00                	mov    eax,DWORD PTR [rax]
   140002127:	85 c0                	test   eax,eax
   140002129:	75 0b                	jne    140002136 <do_pseudo_reloc+0x74>
   14000212b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000212f:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002132:	85 c0                	test   eax,eax
   140002134:	74 59                	je     14000218f <do_pseudo_reloc+0xcd>
   140002136:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000213a:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   14000213e:	eb 40                	jmp    140002180 <do_pseudo_reloc+0xbe>
   140002140:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002144:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002147:	89 c2                	mov    edx,eax
   140002149:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000214d:	48 01 d0             	add    rax,rdx
   140002150:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002154:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002158:	8b 10                	mov    edx,DWORD PTR [rax]
   14000215a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000215e:	8b 00                	mov    eax,DWORD PTR [rax]
   140002160:	01 d0                	add    eax,edx
   140002162:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
   140002165:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002169:	48 8d 55 b4          	lea    rdx,[rbp-0x4c]
   14000216d:	41 b8 04 00 00 00    	mov    r8d,0x4
   140002173:	48 89 c1             	mov    rcx,rax
   140002176:	e8 00 ff ff ff       	call   14000207b <__write_memory>
   14000217b:	48 83 45 e8 08       	add    QWORD PTR [rbp-0x18],0x8
   140002180:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002184:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140002188:	72 b6                	jb     140002140 <do_pseudo_reloc+0x7e>
   14000218a:	e9 ab 02 00 00       	jmp    14000243a <do_pseudo_reloc+0x378>
   14000218f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002193:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002196:	83 f8 01             	cmp    eax,0x1
   140002199:	74 18                	je     1400021b3 <do_pseudo_reloc+0xf1>
   14000219b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000219f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400021a2:	89 c2                	mov    edx,eax
   1400021a4:	48 8d 05 c5 30 00 00 	lea    rax,[rip+0x30c5]        # 140005270 <.rdata+0xa0>
   1400021ab:	48 89 c1             	mov    rcx,rax
   1400021ae:	e8 ad fa ff ff       	call   140001c60 <__report_error>
   1400021b3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400021b7:	48 83 c0 0c          	add    rax,0xc
   1400021bb:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400021bf:	e9 65 02 00 00       	jmp    140002429 <do_pseudo_reloc+0x367>
   1400021c4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400021c8:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400021cb:	89 c2                	mov    edx,eax
   1400021cd:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400021d1:	48 01 d0             	add    rax,rdx
   1400021d4:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400021d8:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400021dc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400021de:	89 c2                	mov    edx,eax
   1400021e0:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400021e4:	48 01 d0             	add    rax,rdx
   1400021e7:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   1400021eb:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   1400021ef:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400021f2:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   1400021f6:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400021fa:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400021fd:	0f b6 c0             	movzx  eax,al
   140002200:	83 f8 40             	cmp    eax,0x40
   140002203:	0f 84 b6 00 00 00    	je     1400022bf <do_pseudo_reloc+0x1fd>
   140002209:	83 f8 40             	cmp    eax,0x40
   14000220c:	0f 87 ba 00 00 00    	ja     1400022cc <do_pseudo_reloc+0x20a>
   140002212:	83 f8 20             	cmp    eax,0x20
   140002215:	74 77                	je     14000228e <do_pseudo_reloc+0x1cc>
   140002217:	83 f8 20             	cmp    eax,0x20
   14000221a:	0f 87 ac 00 00 00    	ja     1400022cc <do_pseudo_reloc+0x20a>
   140002220:	83 f8 08             	cmp    eax,0x8
   140002223:	74 0a                	je     14000222f <do_pseudo_reloc+0x16d>
   140002225:	83 f8 10             	cmp    eax,0x10
   140002228:	74 38                	je     140002262 <do_pseudo_reloc+0x1a0>
   14000222a:	e9 9d 00 00 00       	jmp    1400022cc <do_pseudo_reloc+0x20a>
   14000222f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002233:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140002236:	0f b6 c0             	movzx  eax,al
   140002239:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000223d:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002241:	25 80 00 00 00       	and    eax,0x80
   140002246:	48 85 c0             	test   rax,rax
   140002249:	0f 84 9d 00 00 00    	je     1400022ec <do_pseudo_reloc+0x22a>
   14000224f:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002253:	48 0d 00 ff ff ff    	or     rax,0xffffffffffffff00
   140002259:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000225d:	e9 8a 00 00 00       	jmp    1400022ec <do_pseudo_reloc+0x22a>
   140002262:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002266:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002269:	0f b7 c0             	movzx  eax,ax
   14000226c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140002270:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002274:	25 00 80 00 00       	and    eax,0x8000
   140002279:	48 85 c0             	test   rax,rax
   14000227c:	74 71                	je     1400022ef <do_pseudo_reloc+0x22d>
   14000227e:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002282:	48 0d 00 00 ff ff    	or     rax,0xffffffffffff0000
   140002288:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000228c:	eb 61                	jmp    1400022ef <do_pseudo_reloc+0x22d>
   14000228e:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002292:	8b 00                	mov    eax,DWORD PTR [rax]
   140002294:	89 c0                	mov    eax,eax
   140002296:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000229a:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000229e:	25 00 00 00 80       	and    eax,0x80000000
   1400022a3:	48 85 c0             	test   rax,rax
   1400022a6:	74 4a                	je     1400022f2 <do_pseudo_reloc+0x230>
   1400022a8:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400022ac:	48 ba 00 00 00 00 ff 	movabs rdx,0xffffffff00000000
   1400022b3:	ff ff ff 
   1400022b6:	48 09 d0             	or     rax,rdx
   1400022b9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400022bd:	eb 33                	jmp    1400022f2 <do_pseudo_reloc+0x230>
   1400022bf:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400022c3:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400022c6:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400022ca:	eb 27                	jmp    1400022f3 <do_pseudo_reloc+0x231>
   1400022cc:	48 c7 45 b8 00 00 00 	mov    QWORD PTR [rbp-0x48],0x0
   1400022d3:	00 
   1400022d4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400022d8:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400022db:	0f b6 c0             	movzx  eax,al
   1400022de:	48 8d 0d c3 2f 00 00 	lea    rcx,[rip+0x2fc3]        # 1400052a8 <.rdata+0xd8>
   1400022e5:	89 c2                	mov    edx,eax
   1400022e7:	e8 74 f9 ff ff       	call   140001c60 <__report_error>
   1400022ec:	90                   	nop
   1400022ed:	eb 04                	jmp    1400022f3 <do_pseudo_reloc+0x231>
   1400022ef:	90                   	nop
   1400022f0:	eb 01                	jmp    1400022f3 <do_pseudo_reloc+0x231>
   1400022f2:	90                   	nop
   1400022f3:	48 8b 4d b8          	mov    rcx,QWORD PTR [rbp-0x48]
   1400022f7:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400022fb:	8b 00                	mov    eax,DWORD PTR [rax]
   1400022fd:	89 c2                	mov    edx,eax
   1400022ff:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002303:	48 01 c2             	add    rdx,rax
   140002306:	48 89 c8             	mov    rax,rcx
   140002309:	48 29 d0             	sub    rax,rdx
   14000230c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140002310:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   140002314:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140002318:	48 01 d0             	add    rax,rdx
   14000231b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000231f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002323:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002326:	25 ff 00 00 00       	and    eax,0xff
   14000232b:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   14000232e:	83 7d d4 3f          	cmp    DWORD PTR [rbp-0x2c],0x3f
   140002332:	77 67                	ja     14000239b <do_pseudo_reloc+0x2d9>
   140002334:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140002337:	ba 01 00 00 00       	mov    edx,0x1
   14000233c:	89 c1                	mov    ecx,eax
   14000233e:	48 d3 e2             	shl    rdx,cl
   140002341:	48 89 d0             	mov    rax,rdx
   140002344:	48 83 e8 01          	sub    rax,0x1
   140002348:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   14000234c:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   14000234f:	83 e8 01             	sub    eax,0x1
   140002352:	48 c7 c2 ff ff ff ff 	mov    rdx,0xffffffffffffffff
   140002359:	89 c1                	mov    ecx,eax
   14000235b:	48 d3 e2             	shl    rdx,cl
   14000235e:	48 89 d0             	mov    rax,rdx
   140002361:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   140002365:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002369:	48 39 45 c8          	cmp    QWORD PTR [rbp-0x38],rax
   14000236d:	7c 0a                	jl     140002379 <do_pseudo_reloc+0x2b7>
   14000236f:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002373:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   140002377:	7e 22                	jle    14000239b <do_pseudo_reloc+0x2d9>
   140002379:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   14000237d:	4c 8b 4d d8          	mov    r9,QWORD PTR [rbp-0x28]
   140002381:	4c 8b 45 e0          	mov    r8,QWORD PTR [rbp-0x20]
   140002385:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140002388:	48 8d 0d 49 2f 00 00 	lea    rcx,[rip+0x2f49]        # 1400052d8 <.rdata+0x108>
   14000238f:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   140002394:	89 c2                	mov    edx,eax
   140002396:	e8 c5 f8 ff ff       	call   140001c60 <__report_error>
   14000239b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000239f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400023a2:	0f b6 c0             	movzx  eax,al
   1400023a5:	83 f8 40             	cmp    eax,0x40
   1400023a8:	74 63                	je     14000240d <do_pseudo_reloc+0x34b>
   1400023aa:	83 f8 40             	cmp    eax,0x40
   1400023ad:	77 75                	ja     140002424 <do_pseudo_reloc+0x362>
   1400023af:	83 f8 20             	cmp    eax,0x20
   1400023b2:	74 41                	je     1400023f5 <do_pseudo_reloc+0x333>
   1400023b4:	83 f8 20             	cmp    eax,0x20
   1400023b7:	77 6b                	ja     140002424 <do_pseudo_reloc+0x362>
   1400023b9:	83 f8 08             	cmp    eax,0x8
   1400023bc:	74 07                	je     1400023c5 <do_pseudo_reloc+0x303>
   1400023be:	83 f8 10             	cmp    eax,0x10
   1400023c1:	74 1a                	je     1400023dd <do_pseudo_reloc+0x31b>
   1400023c3:	eb 5f                	jmp    140002424 <do_pseudo_reloc+0x362>
   1400023c5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400023c9:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   1400023cd:	41 b8 01 00 00 00    	mov    r8d,0x1
   1400023d3:	48 89 c1             	mov    rcx,rax
   1400023d6:	e8 a0 fc ff ff       	call   14000207b <__write_memory>
   1400023db:	eb 47                	jmp    140002424 <do_pseudo_reloc+0x362>
   1400023dd:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400023e1:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   1400023e5:	41 b8 02 00 00 00    	mov    r8d,0x2
   1400023eb:	48 89 c1             	mov    rcx,rax
   1400023ee:	e8 88 fc ff ff       	call   14000207b <__write_memory>
   1400023f3:	eb 2f                	jmp    140002424 <do_pseudo_reloc+0x362>
   1400023f5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400023f9:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   1400023fd:	41 b8 04 00 00 00    	mov    r8d,0x4
   140002403:	48 89 c1             	mov    rcx,rax
   140002406:	e8 70 fc ff ff       	call   14000207b <__write_memory>
   14000240b:	eb 17                	jmp    140002424 <do_pseudo_reloc+0x362>
   14000240d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002411:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002415:	41 b8 08 00 00 00    	mov    r8d,0x8
   14000241b:	48 89 c1             	mov    rcx,rax
   14000241e:	e8 58 fc ff ff       	call   14000207b <__write_memory>
   140002423:	90                   	nop
   140002424:	48 83 45 f0 0c       	add    QWORD PTR [rbp-0x10],0xc
   140002429:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000242d:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140002431:	0f 82 8d fd ff ff    	jb     1400021c4 <do_pseudo_reloc+0x102>
   140002437:	eb 01                	jmp    14000243a <do_pseudo_reloc+0x378>
   140002439:	90                   	nop
   14000243a:	48 83 ec 80          	sub    rsp,0xffffffffffffff80
   14000243e:	5d                   	pop    rbp
   14000243f:	c3                   	ret

0000000140002440 <_pei386_runtime_relocator>:
   140002440:	55                   	push   rbp
   140002441:	48 89 e5             	mov    rbp,rsp
   140002444:	48 83 ec 30          	sub    rsp,0x30
   140002448:	8b 05 9e 6c 00 00    	mov    eax,DWORD PTR [rip+0x6c9e]        # 1400090ec <was_init.0>
   14000244e:	85 c0                	test   eax,eax
   140002450:	0f 85 88 00 00 00    	jne    1400024de <_pei386_runtime_relocator+0x9e>
   140002456:	8b 05 90 6c 00 00    	mov    eax,DWORD PTR [rip+0x6c90]        # 1400090ec <was_init.0>
   14000245c:	83 c0 01             	add    eax,0x1
   14000245f:	89 05 87 6c 00 00    	mov    DWORD PTR [rip+0x6c87],eax        # 1400090ec <was_init.0>
   140002465:	e8 21 0b 00 00       	call   140002f8b <__mingw_GetSectionCount>
   14000246a:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   14000246d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002470:	48 63 d0             	movsxd rdx,eax
   140002473:	48 89 d0             	mov    rax,rdx
   140002476:	48 c1 e0 02          	shl    rax,0x2
   14000247a:	48 01 d0             	add    rax,rdx
   14000247d:	48 c1 e0 03          	shl    rax,0x3
   140002481:	48 83 c0 0f          	add    rax,0xf
   140002485:	48 c1 e8 04          	shr    rax,0x4
   140002489:	48 c1 e0 04          	shl    rax,0x4
   14000248d:	e8 8e 0d 00 00       	call   140003220 <___chkstk_ms>
   140002492:	48 29 c4             	sub    rsp,rax
   140002495:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   14000249a:	48 83 c0 0f          	add    rax,0xf
   14000249e:	48 c1 e8 04          	shr    rax,0x4
   1400024a2:	48 c1 e0 04          	shl    rax,0x4
   1400024a6:	48 89 05 33 6c 00 00 	mov    QWORD PTR [rip+0x6c33],rax        # 1400090e0 <the_secs>
   1400024ad:	c7 05 31 6c 00 00 00 	mov    DWORD PTR [rip+0x6c31],0x0        # 1400090e8 <maxSections>
   1400024b4:	00 00 00 
   1400024b7:	48 8b 0d a2 2e 00 00 	mov    rcx,QWORD PTR [rip+0x2ea2]        # 140005360 <.refptr.__ImageBase>
   1400024be:	48 8b 15 ab 2e 00 00 	mov    rdx,QWORD PTR [rip+0x2eab]        # 140005370 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   1400024c5:	48 8b 05 b4 2e 00 00 	mov    rax,QWORD PTR [rip+0x2eb4]        # 140005380 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   1400024cc:	49 89 c8             	mov    r8,rcx
   1400024cf:	48 89 c1             	mov    rcx,rax
   1400024d2:	e8 eb fb ff ff       	call   1400020c2 <do_pseudo_reloc>
   1400024d7:	e8 c7 fa ff ff       	call   140001fa3 <restore_modified_sections>
   1400024dc:	eb 01                	jmp    1400024df <_pei386_runtime_relocator+0x9f>
   1400024de:	90                   	nop
   1400024df:	48 89 ec             	mov    rsp,rbp
   1400024e2:	5d                   	pop    rbp
   1400024e3:	c3                   	ret
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

00000001400024f0 <__mingw_raise_matherr>:
   1400024f0:	55                   	push   rbp
   1400024f1:	48 89 e5             	mov    rbp,rsp
   1400024f4:	48 83 ec 50          	sub    rsp,0x50
   1400024f8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400024fb:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400024ff:	f2 0f 11 55 20       	movsd  QWORD PTR [rbp+0x20],xmm2
   140002504:	f2 0f 11 5d 28       	movsd  QWORD PTR [rbp+0x28],xmm3
   140002509:	48 8b 05 e0 6b 00 00 	mov    rax,QWORD PTR [rip+0x6be0]        # 1400090f0 <stUserMathErr>
   140002510:	48 85 c0             	test   rax,rax
   140002513:	74 3e                	je     140002553 <__mingw_raise_matherr+0x63>
   140002515:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140002518:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   14000251b:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000251f:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002523:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   140002528:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   14000252d:	f2 0f 10 45 28       	movsd  xmm0,QWORD PTR [rbp+0x28]
   140002532:	f2 0f 11 45 e8       	movsd  QWORD PTR [rbp-0x18],xmm0
   140002537:	f2 0f 10 45 30       	movsd  xmm0,QWORD PTR [rbp+0x30]
   14000253c:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   140002541:	48 8b 15 a8 6b 00 00 	mov    rdx,QWORD PTR [rip+0x6ba8]        # 1400090f0 <stUserMathErr>
   140002548:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   14000254c:	48 89 c1             	mov    rcx,rax
   14000254f:	ff d2                	call   rdx
   140002551:	eb 01                	jmp    140002554 <__mingw_raise_matherr+0x64>
   140002553:	90                   	nop
   140002554:	48 83 c4 50          	add    rsp,0x50
   140002558:	5d                   	pop    rbp
   140002559:	c3                   	ret

000000014000255a <__mingw_setusermatherr>:
   14000255a:	55                   	push   rbp
   14000255b:	48 89 e5             	mov    rbp,rsp
   14000255e:	48 83 ec 20          	sub    rsp,0x20
   140002562:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002566:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000256a:	48 89 05 7f 6b 00 00 	mov    QWORD PTR [rip+0x6b7f],rax        # 1400090f0 <stUserMathErr>
   140002571:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002575:	48 89 c1             	mov    rcx,rax
   140002578:	e8 23 0e 00 00       	call   1400033a0 <__setusermatherr>
   14000257d:	90                   	nop
   14000257e:	48 83 c4 20          	add    rsp,0x20
   140002582:	5d                   	pop    rbp
   140002583:	c3                   	ret
   140002584:	90                   	nop
   140002585:	90                   	nop
   140002586:	90                   	nop
   140002587:	90                   	nop
   140002588:	90                   	nop
   140002589:	90                   	nop
   14000258a:	90                   	nop
   14000258b:	90                   	nop
   14000258c:	90                   	nop
   14000258d:	90                   	nop
   14000258e:	90                   	nop
   14000258f:	90                   	nop

0000000140002590 <__mingw_SEH_error_handler>:
   140002590:	55                   	push   rbp
   140002591:	48 89 e5             	mov    rbp,rsp
   140002594:	48 83 ec 30          	sub    rsp,0x30
   140002598:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000259c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400025a0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400025a4:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   1400025a8:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   1400025af:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   1400025b6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400025ba:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400025bd:	83 e0 02             	and    eax,0x2
   1400025c0:	85 c0                	test   eax,eax
   1400025c2:	74 0a                	je     1400025ce <__mingw_SEH_error_handler+0x3e>
   1400025c4:	b8 01 00 00 00       	mov    eax,0x1
   1400025c9:	e9 16 02 00 00       	jmp    1400027e4 <__mingw_SEH_error_handler+0x254>
   1400025ce:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400025d2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400025d4:	25 ff ff ff 20       	and    eax,0x20ffffff
   1400025d9:	3d 43 43 47 20       	cmp    eax,0x20474343
   1400025de:	75 18                	jne    1400025f8 <__mingw_SEH_error_handler+0x68>
   1400025e0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400025e4:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400025e7:	83 e0 01             	and    eax,0x1
   1400025ea:	85 c0                	test   eax,eax
   1400025ec:	75 0a                	jne    1400025f8 <__mingw_SEH_error_handler+0x68>
   1400025ee:	b8 00 00 00 00       	mov    eax,0x0
   1400025f3:	e9 ec 01 00 00       	jmp    1400027e4 <__mingw_SEH_error_handler+0x254>
   1400025f8:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400025fc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400025fe:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002603:	0f 84 12 01 00 00    	je     14000271b <__mingw_SEH_error_handler+0x18b>
   140002609:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000260e:	0f 87 c3 01 00 00    	ja     1400027d7 <__mingw_SEH_error_handler+0x247>
   140002614:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   140002619:	0f 87 b8 01 00 00    	ja     1400027d7 <__mingw_SEH_error_handler+0x247>
   14000261f:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   140002624:	0f 83 4c 01 00 00    	jae    140002776 <__mingw_SEH_error_handler+0x1e6>
   14000262a:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000262f:	0f 84 3a 01 00 00    	je     14000276f <__mingw_SEH_error_handler+0x1df>
   140002635:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000263a:	0f 87 97 01 00 00    	ja     1400027d7 <__mingw_SEH_error_handler+0x247>
   140002640:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   140002645:	0f 84 83 01 00 00    	je     1400027ce <__mingw_SEH_error_handler+0x23e>
   14000264b:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   140002650:	0f 87 81 01 00 00    	ja     1400027d7 <__mingw_SEH_error_handler+0x247>
   140002656:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   14000265b:	0f 87 76 01 00 00    	ja     1400027d7 <__mingw_SEH_error_handler+0x247>
   140002661:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   140002666:	0f 83 03 01 00 00    	jae    14000276f <__mingw_SEH_error_handler+0x1df>
   14000266c:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   140002671:	0f 84 57 01 00 00    	je     1400027ce <__mingw_SEH_error_handler+0x23e>
   140002677:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   14000267c:	0f 87 55 01 00 00    	ja     1400027d7 <__mingw_SEH_error_handler+0x247>
   140002682:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002687:	0f 84 8e 00 00 00    	je     14000271b <__mingw_SEH_error_handler+0x18b>
   14000268d:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002692:	0f 87 3f 01 00 00    	ja     1400027d7 <__mingw_SEH_error_handler+0x247>
   140002698:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000269d:	0f 84 2b 01 00 00    	je     1400027ce <__mingw_SEH_error_handler+0x23e>
   1400026a3:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   1400026a8:	0f 87 29 01 00 00    	ja     1400027d7 <__mingw_SEH_error_handler+0x247>
   1400026ae:	3d 02 00 00 80       	cmp    eax,0x80000002
   1400026b3:	0f 84 15 01 00 00    	je     1400027ce <__mingw_SEH_error_handler+0x23e>
   1400026b9:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   1400026be:	0f 85 13 01 00 00    	jne    1400027d7 <__mingw_SEH_error_handler+0x247>
   1400026c4:	ba 00 00 00 00       	mov    edx,0x0
   1400026c9:	b9 0b 00 00 00       	mov    ecx,0xb
   1400026ce:	e8 3d 0d 00 00       	call   140003410 <signal>
   1400026d3:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400026d7:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400026dc:	75 1b                	jne    1400026f9 <__mingw_SEH_error_handler+0x169>
   1400026de:	ba 01 00 00 00       	mov    edx,0x1
   1400026e3:	b9 0b 00 00 00       	mov    ecx,0xb
   1400026e8:	e8 23 0d 00 00       	call   140003410 <signal>
   1400026ed:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400026f4:	e9 e1 00 00 00       	jmp    1400027da <__mingw_SEH_error_handler+0x24a>
   1400026f9:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400026fe:	0f 84 d6 00 00 00    	je     1400027da <__mingw_SEH_error_handler+0x24a>
   140002704:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002708:	b9 0b 00 00 00       	mov    ecx,0xb
   14000270d:	ff d0                	call   rax
   14000270f:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002716:	e9 bf 00 00 00       	jmp    1400027da <__mingw_SEH_error_handler+0x24a>
   14000271b:	ba 00 00 00 00       	mov    edx,0x0
   140002720:	b9 04 00 00 00       	mov    ecx,0x4
   140002725:	e8 e6 0c 00 00       	call   140003410 <signal>
   14000272a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000272e:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002733:	75 1b                	jne    140002750 <__mingw_SEH_error_handler+0x1c0>
   140002735:	ba 01 00 00 00       	mov    edx,0x1
   14000273a:	b9 04 00 00 00       	mov    ecx,0x4
   14000273f:	e8 cc 0c 00 00       	call   140003410 <signal>
   140002744:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000274b:	e9 8d 00 00 00       	jmp    1400027dd <__mingw_SEH_error_handler+0x24d>
   140002750:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002755:	0f 84 82 00 00 00    	je     1400027dd <__mingw_SEH_error_handler+0x24d>
   14000275b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000275f:	b9 04 00 00 00       	mov    ecx,0x4
   140002764:	ff d0                	call   rax
   140002766:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000276d:	eb 6e                	jmp    1400027dd <__mingw_SEH_error_handler+0x24d>
   14000276f:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140002776:	ba 00 00 00 00       	mov    edx,0x0
   14000277b:	b9 08 00 00 00       	mov    ecx,0x8
   140002780:	e8 8b 0c 00 00       	call   140003410 <signal>
   140002785:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002789:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000278e:	75 23                	jne    1400027b3 <__mingw_SEH_error_handler+0x223>
   140002790:	ba 01 00 00 00       	mov    edx,0x1
   140002795:	b9 08 00 00 00       	mov    ecx,0x8
   14000279a:	e8 71 0c 00 00       	call   140003410 <signal>
   14000279f:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   1400027a3:	74 05                	je     1400027aa <__mingw_SEH_error_handler+0x21a>
   1400027a5:	e8 a6 05 00 00       	call   140002d50 <_fpreset>
   1400027aa:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400027b1:	eb 2d                	jmp    1400027e0 <__mingw_SEH_error_handler+0x250>
   1400027b3:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400027b8:	74 26                	je     1400027e0 <__mingw_SEH_error_handler+0x250>
   1400027ba:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400027be:	b9 08 00 00 00       	mov    ecx,0x8
   1400027c3:	ff d0                	call   rax
   1400027c5:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400027cc:	eb 12                	jmp    1400027e0 <__mingw_SEH_error_handler+0x250>
   1400027ce:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400027d5:	eb 0a                	jmp    1400027e1 <__mingw_SEH_error_handler+0x251>
   1400027d7:	90                   	nop
   1400027d8:	eb 07                	jmp    1400027e1 <__mingw_SEH_error_handler+0x251>
   1400027da:	90                   	nop
   1400027db:	eb 04                	jmp    1400027e1 <__mingw_SEH_error_handler+0x251>
   1400027dd:	90                   	nop
   1400027de:	eb 01                	jmp    1400027e1 <__mingw_SEH_error_handler+0x251>
   1400027e0:	90                   	nop
   1400027e1:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400027e4:	48 83 c4 30          	add    rsp,0x30
   1400027e8:	5d                   	pop    rbp
   1400027e9:	c3                   	ret

00000001400027ea <_gnu_exception_handler>:
   1400027ea:	55                   	push   rbp
   1400027eb:	48 89 e5             	mov    rbp,rsp
   1400027ee:	48 83 ec 30          	sub    rsp,0x30
   1400027f2:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400027f6:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400027fd:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002804:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002808:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000280b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000280d:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002812:	3d 43 43 47 20       	cmp    eax,0x20474343
   140002817:	75 1b                	jne    140002834 <_gnu_exception_handler+0x4a>
   140002819:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000281d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002820:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002823:	83 e0 01             	and    eax,0x1
   140002826:	85 c0                	test   eax,eax
   140002828:	75 0a                	jne    140002834 <_gnu_exception_handler+0x4a>
   14000282a:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000282f:	e9 14 02 00 00       	jmp    140002a48 <_gnu_exception_handler+0x25e>
   140002834:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002838:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000283b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000283d:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002842:	0f 84 12 01 00 00    	je     14000295a <_gnu_exception_handler+0x170>
   140002848:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000284d:	0f 87 c3 01 00 00    	ja     140002a16 <_gnu_exception_handler+0x22c>
   140002853:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   140002858:	0f 87 b8 01 00 00    	ja     140002a16 <_gnu_exception_handler+0x22c>
   14000285e:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   140002863:	0f 83 4c 01 00 00    	jae    1400029b5 <_gnu_exception_handler+0x1cb>
   140002869:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000286e:	0f 84 3a 01 00 00    	je     1400029ae <_gnu_exception_handler+0x1c4>
   140002874:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   140002879:	0f 87 97 01 00 00    	ja     140002a16 <_gnu_exception_handler+0x22c>
   14000287f:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   140002884:	0f 84 83 01 00 00    	je     140002a0d <_gnu_exception_handler+0x223>
   14000288a:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   14000288f:	0f 87 81 01 00 00    	ja     140002a16 <_gnu_exception_handler+0x22c>
   140002895:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   14000289a:	0f 87 76 01 00 00    	ja     140002a16 <_gnu_exception_handler+0x22c>
   1400028a0:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   1400028a5:	0f 83 03 01 00 00    	jae    1400029ae <_gnu_exception_handler+0x1c4>
   1400028ab:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400028b0:	0f 84 57 01 00 00    	je     140002a0d <_gnu_exception_handler+0x223>
   1400028b6:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400028bb:	0f 87 55 01 00 00    	ja     140002a16 <_gnu_exception_handler+0x22c>
   1400028c1:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400028c6:	0f 84 8e 00 00 00    	je     14000295a <_gnu_exception_handler+0x170>
   1400028cc:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400028d1:	0f 87 3f 01 00 00    	ja     140002a16 <_gnu_exception_handler+0x22c>
   1400028d7:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   1400028dc:	0f 84 2b 01 00 00    	je     140002a0d <_gnu_exception_handler+0x223>
   1400028e2:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   1400028e7:	0f 87 29 01 00 00    	ja     140002a16 <_gnu_exception_handler+0x22c>
   1400028ed:	3d 02 00 00 80       	cmp    eax,0x80000002
   1400028f2:	0f 84 15 01 00 00    	je     140002a0d <_gnu_exception_handler+0x223>
   1400028f8:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   1400028fd:	0f 85 13 01 00 00    	jne    140002a16 <_gnu_exception_handler+0x22c>
   140002903:	ba 00 00 00 00       	mov    edx,0x0
   140002908:	b9 0b 00 00 00       	mov    ecx,0xb
   14000290d:	e8 fe 0a 00 00       	call   140003410 <signal>
   140002912:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002916:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000291b:	75 1b                	jne    140002938 <_gnu_exception_handler+0x14e>
   14000291d:	ba 01 00 00 00       	mov    edx,0x1
   140002922:	b9 0b 00 00 00       	mov    ecx,0xb
   140002927:	e8 e4 0a 00 00       	call   140003410 <signal>
   14000292c:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002933:	e9 e1 00 00 00       	jmp    140002a19 <_gnu_exception_handler+0x22f>
   140002938:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000293d:	0f 84 d6 00 00 00    	je     140002a19 <_gnu_exception_handler+0x22f>
   140002943:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002947:	b9 0b 00 00 00       	mov    ecx,0xb
   14000294c:	ff d0                	call   rax
   14000294e:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002955:	e9 bf 00 00 00       	jmp    140002a19 <_gnu_exception_handler+0x22f>
   14000295a:	ba 00 00 00 00       	mov    edx,0x0
   14000295f:	b9 04 00 00 00       	mov    ecx,0x4
   140002964:	e8 a7 0a 00 00       	call   140003410 <signal>
   140002969:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000296d:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002972:	75 1b                	jne    14000298f <_gnu_exception_handler+0x1a5>
   140002974:	ba 01 00 00 00       	mov    edx,0x1
   140002979:	b9 04 00 00 00       	mov    ecx,0x4
   14000297e:	e8 8d 0a 00 00       	call   140003410 <signal>
   140002983:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000298a:	e9 8d 00 00 00       	jmp    140002a1c <_gnu_exception_handler+0x232>
   14000298f:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002994:	0f 84 82 00 00 00    	je     140002a1c <_gnu_exception_handler+0x232>
   14000299a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000299e:	b9 04 00 00 00       	mov    ecx,0x4
   1400029a3:	ff d0                	call   rax
   1400029a5:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400029ac:	eb 6e                	jmp    140002a1c <_gnu_exception_handler+0x232>
   1400029ae:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400029b5:	ba 00 00 00 00       	mov    edx,0x0
   1400029ba:	b9 08 00 00 00       	mov    ecx,0x8
   1400029bf:	e8 4c 0a 00 00       	call   140003410 <signal>
   1400029c4:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400029c8:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400029cd:	75 23                	jne    1400029f2 <_gnu_exception_handler+0x208>
   1400029cf:	ba 01 00 00 00       	mov    edx,0x1
   1400029d4:	b9 08 00 00 00       	mov    ecx,0x8
   1400029d9:	e8 32 0a 00 00       	call   140003410 <signal>
   1400029de:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   1400029e2:	74 05                	je     1400029e9 <_gnu_exception_handler+0x1ff>
   1400029e4:	e8 67 03 00 00       	call   140002d50 <_fpreset>
   1400029e9:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400029f0:	eb 2d                	jmp    140002a1f <_gnu_exception_handler+0x235>
   1400029f2:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400029f7:	74 26                	je     140002a1f <_gnu_exception_handler+0x235>
   1400029f9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029fd:	b9 08 00 00 00       	mov    ecx,0x8
   140002a02:	ff d0                	call   rax
   140002a04:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002a0b:	eb 12                	jmp    140002a1f <_gnu_exception_handler+0x235>
   140002a0d:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002a14:	eb 0a                	jmp    140002a20 <_gnu_exception_handler+0x236>
   140002a16:	90                   	nop
   140002a17:	eb 07                	jmp    140002a20 <_gnu_exception_handler+0x236>
   140002a19:	90                   	nop
   140002a1a:	eb 04                	jmp    140002a20 <_gnu_exception_handler+0x236>
   140002a1c:	90                   	nop
   140002a1d:	eb 01                	jmp    140002a20 <_gnu_exception_handler+0x236>
   140002a1f:	90                   	nop
   140002a20:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140002a24:	75 1f                	jne    140002a45 <_gnu_exception_handler+0x25b>
   140002a26:	48 8b 05 e3 66 00 00 	mov    rax,QWORD PTR [rip+0x66e3]        # 140009110 <__mingw_oldexcpt_handler>
   140002a2d:	48 85 c0             	test   rax,rax
   140002a30:	74 13                	je     140002a45 <_gnu_exception_handler+0x25b>
   140002a32:	48 8b 15 d7 66 00 00 	mov    rdx,QWORD PTR [rip+0x66d7]        # 140009110 <__mingw_oldexcpt_handler>
   140002a39:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002a3d:	48 89 c1             	mov    rcx,rax
   140002a40:	ff d2                	call   rdx
   140002a42:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140002a45:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002a48:	48 83 c4 30          	add    rsp,0x30
   140002a4c:	5d                   	pop    rbp
   140002a4d:	c3                   	ret
   140002a4e:	90                   	nop
   140002a4f:	90                   	nop

0000000140002a50 <___w64_mingwthr_add_key_dtor>:
   140002a50:	55                   	push   rbp
   140002a51:	48 89 e5             	mov    rbp,rsp
   140002a54:	48 83 ec 30          	sub    rsp,0x30
   140002a58:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002a5b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002a5f:	8b 05 e3 66 00 00    	mov    eax,DWORD PTR [rip+0x66e3]        # 140009148 <__mingwthr_cs_init>
   140002a65:	85 c0                	test   eax,eax
   140002a67:	75 07                	jne    140002a70 <___w64_mingwthr_add_key_dtor+0x20>
   140002a69:	b8 00 00 00 00       	mov    eax,0x0
   140002a6e:	eb 7b                	jmp    140002aeb <___w64_mingwthr_add_key_dtor+0x9b>
   140002a70:	ba 18 00 00 00       	mov    edx,0x18
   140002a75:	b9 01 00 00 00       	mov    ecx,0x1
   140002a7a:	e8 51 09 00 00       	call   1400033d0 <calloc>
   140002a7f:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a83:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002a88:	75 07                	jne    140002a91 <___w64_mingwthr_add_key_dtor+0x41>
   140002a8a:	b8 ff ff ff ff       	mov    eax,0xffffffff
   140002a8f:	eb 5a                	jmp    140002aeb <___w64_mingwthr_add_key_dtor+0x9b>
   140002a91:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a95:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140002a98:	89 10                	mov    DWORD PTR [rax],edx
   140002a9a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a9e:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140002aa2:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
   140002aa6:	48 8d 05 73 66 00 00 	lea    rax,[rip+0x6673]        # 140009120 <__mingwthr_cs>
   140002aad:	48 89 c1             	mov    rcx,rax
   140002ab0:	48 8b 05 81 77 00 00 	mov    rax,QWORD PTR [rip+0x7781]        # 14000a238 <__imp_EnterCriticalSection>
   140002ab7:	ff d0                	call   rax
   140002ab9:	48 8b 15 90 66 00 00 	mov    rdx,QWORD PTR [rip+0x6690]        # 140009150 <key_dtor_list>
   140002ac0:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ac4:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002ac8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002acc:	48 89 05 7d 66 00 00 	mov    QWORD PTR [rip+0x667d],rax        # 140009150 <key_dtor_list>
   140002ad3:	48 8d 05 46 66 00 00 	lea    rax,[rip+0x6646]        # 140009120 <__mingwthr_cs>
   140002ada:	48 89 c1             	mov    rcx,rax
   140002add:	48 8b 05 84 77 00 00 	mov    rax,QWORD PTR [rip+0x7784]        # 14000a268 <__imp_LeaveCriticalSection>
   140002ae4:	ff d0                	call   rax
   140002ae6:	b8 00 00 00 00       	mov    eax,0x0
   140002aeb:	48 83 c4 30          	add    rsp,0x30
   140002aef:	5d                   	pop    rbp
   140002af0:	c3                   	ret

0000000140002af1 <___w64_mingwthr_remove_key_dtor>:
   140002af1:	55                   	push   rbp
   140002af2:	48 89 e5             	mov    rbp,rsp
   140002af5:	48 83 ec 30          	sub    rsp,0x30
   140002af9:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002afc:	8b 05 46 66 00 00    	mov    eax,DWORD PTR [rip+0x6646]        # 140009148 <__mingwthr_cs_init>
   140002b02:	85 c0                	test   eax,eax
   140002b04:	75 0a                	jne    140002b10 <___w64_mingwthr_remove_key_dtor+0x1f>
   140002b06:	b8 00 00 00 00       	mov    eax,0x0
   140002b0b:	e9 9c 00 00 00       	jmp    140002bac <___w64_mingwthr_remove_key_dtor+0xbb>
   140002b10:	48 8d 05 09 66 00 00 	lea    rax,[rip+0x6609]        # 140009120 <__mingwthr_cs>
   140002b17:	48 89 c1             	mov    rcx,rax
   140002b1a:	48 8b 05 17 77 00 00 	mov    rax,QWORD PTR [rip+0x7717]        # 14000a238 <__imp_EnterCriticalSection>
   140002b21:	ff d0                	call   rax
   140002b23:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   140002b2a:	00 
   140002b2b:	48 8b 05 1e 66 00 00 	mov    rax,QWORD PTR [rip+0x661e]        # 140009150 <key_dtor_list>
   140002b32:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b36:	eb 55                	jmp    140002b8d <___w64_mingwthr_remove_key_dtor+0x9c>
   140002b38:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b3c:	8b 00                	mov    eax,DWORD PTR [rax]
   140002b3e:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   140002b41:	75 36                	jne    140002b79 <___w64_mingwthr_remove_key_dtor+0x88>
   140002b43:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002b48:	75 11                	jne    140002b5b <___w64_mingwthr_remove_key_dtor+0x6a>
   140002b4a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b4e:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002b52:	48 89 05 f7 65 00 00 	mov    QWORD PTR [rip+0x65f7],rax        # 140009150 <key_dtor_list>
   140002b59:	eb 10                	jmp    140002b6b <___w64_mingwthr_remove_key_dtor+0x7a>
   140002b5b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b5f:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   140002b63:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b67:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002b6b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b6f:	48 89 c1             	mov    rcx,rax
   140002b72:	e8 79 08 00 00       	call   1400033f0 <free>
   140002b77:	eb 1b                	jmp    140002b94 <___w64_mingwthr_remove_key_dtor+0xa3>
   140002b79:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b7d:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b81:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b85:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002b89:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b8d:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002b92:	75 a4                	jne    140002b38 <___w64_mingwthr_remove_key_dtor+0x47>
   140002b94:	48 8d 05 85 65 00 00 	lea    rax,[rip+0x6585]        # 140009120 <__mingwthr_cs>
   140002b9b:	48 89 c1             	mov    rcx,rax
   140002b9e:	48 8b 05 c3 76 00 00 	mov    rax,QWORD PTR [rip+0x76c3]        # 14000a268 <__imp_LeaveCriticalSection>
   140002ba5:	ff d0                	call   rax
   140002ba7:	b8 00 00 00 00       	mov    eax,0x0
   140002bac:	48 83 c4 30          	add    rsp,0x30
   140002bb0:	5d                   	pop    rbp
   140002bb1:	c3                   	ret

0000000140002bb2 <__mingwthr_run_key_dtors>:
   140002bb2:	55                   	push   rbp
   140002bb3:	48 89 e5             	mov    rbp,rsp
   140002bb6:	48 83 ec 30          	sub    rsp,0x30
   140002bba:	8b 05 88 65 00 00    	mov    eax,DWORD PTR [rip+0x6588]        # 140009148 <__mingwthr_cs_init>
   140002bc0:	85 c0                	test   eax,eax
   140002bc2:	0f 84 82 00 00 00    	je     140002c4a <__mingwthr_run_key_dtors+0x98>
   140002bc8:	48 8d 05 51 65 00 00 	lea    rax,[rip+0x6551]        # 140009120 <__mingwthr_cs>
   140002bcf:	48 89 c1             	mov    rcx,rax
   140002bd2:	48 8b 05 5f 76 00 00 	mov    rax,QWORD PTR [rip+0x765f]        # 14000a238 <__imp_EnterCriticalSection>
   140002bd9:	ff d0                	call   rax
   140002bdb:	48 8b 05 6e 65 00 00 	mov    rax,QWORD PTR [rip+0x656e]        # 140009150 <key_dtor_list>
   140002be2:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002be6:	eb 46                	jmp    140002c2e <__mingwthr_run_key_dtors+0x7c>
   140002be8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bec:	8b 00                	mov    eax,DWORD PTR [rax]
   140002bee:	89 c1                	mov    ecx,eax
   140002bf0:	48 8b 05 91 76 00 00 	mov    rax,QWORD PTR [rip+0x7691]        # 14000a288 <__imp_TlsGetValue>
   140002bf7:	ff d0                	call   rax
   140002bf9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002bfd:	48 8b 05 44 76 00 00 	mov    rax,QWORD PTR [rip+0x7644]        # 14000a248 <__imp_GetLastError>
   140002c04:	ff d0                	call   rax
   140002c06:	85 c0                	test   eax,eax
   140002c08:	75 18                	jne    140002c22 <__mingwthr_run_key_dtors+0x70>
   140002c0a:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002c0f:	74 11                	je     140002c22 <__mingwthr_run_key_dtors+0x70>
   140002c11:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c15:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140002c19:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c1d:	48 89 c1             	mov    rcx,rax
   140002c20:	ff d2                	call   rdx
   140002c22:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c26:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002c2a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002c2e:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002c33:	75 b3                	jne    140002be8 <__mingwthr_run_key_dtors+0x36>
   140002c35:	48 8d 05 e4 64 00 00 	lea    rax,[rip+0x64e4]        # 140009120 <__mingwthr_cs>
   140002c3c:	48 89 c1             	mov    rcx,rax
   140002c3f:	48 8b 05 22 76 00 00 	mov    rax,QWORD PTR [rip+0x7622]        # 14000a268 <__imp_LeaveCriticalSection>
   140002c46:	ff d0                	call   rax
   140002c48:	eb 01                	jmp    140002c4b <__mingwthr_run_key_dtors+0x99>
   140002c4a:	90                   	nop
   140002c4b:	48 83 c4 30          	add    rsp,0x30
   140002c4f:	5d                   	pop    rbp
   140002c50:	c3                   	ret

0000000140002c51 <__mingw_TLScallback>:
   140002c51:	55                   	push   rbp
   140002c52:	48 89 e5             	mov    rbp,rsp
   140002c55:	48 83 ec 30          	sub    rsp,0x30
   140002c59:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002c5d:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140002c60:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002c64:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002c68:	0f 84 cc 00 00 00    	je     140002d3a <__mingw_TLScallback+0xe9>
   140002c6e:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002c72:	0f 87 ca 00 00 00    	ja     140002d42 <__mingw_TLScallback+0xf1>
   140002c78:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002c7c:	0f 84 b1 00 00 00    	je     140002d33 <__mingw_TLScallback+0xe2>
   140002c82:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002c86:	0f 87 b6 00 00 00    	ja     140002d42 <__mingw_TLScallback+0xf1>
   140002c8c:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140002c90:	74 33                	je     140002cc5 <__mingw_TLScallback+0x74>
   140002c92:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140002c96:	0f 85 a6 00 00 00    	jne    140002d42 <__mingw_TLScallback+0xf1>
   140002c9c:	8b 05 a6 64 00 00    	mov    eax,DWORD PTR [rip+0x64a6]        # 140009148 <__mingwthr_cs_init>
   140002ca2:	85 c0                	test   eax,eax
   140002ca4:	75 13                	jne    140002cb9 <__mingw_TLScallback+0x68>
   140002ca6:	48 8d 05 73 64 00 00 	lea    rax,[rip+0x6473]        # 140009120 <__mingwthr_cs>
   140002cad:	48 89 c1             	mov    rcx,rax
   140002cb0:	48 8b 05 a9 75 00 00 	mov    rax,QWORD PTR [rip+0x75a9]        # 14000a260 <__imp_InitializeCriticalSection>
   140002cb7:	ff d0                	call   rax
   140002cb9:	c7 05 85 64 00 00 01 	mov    DWORD PTR [rip+0x6485],0x1        # 140009148 <__mingwthr_cs_init>
   140002cc0:	00 00 00 
   140002cc3:	eb 7d                	jmp    140002d42 <__mingw_TLScallback+0xf1>
   140002cc5:	e8 e8 fe ff ff       	call   140002bb2 <__mingwthr_run_key_dtors>
   140002cca:	8b 05 78 64 00 00    	mov    eax,DWORD PTR [rip+0x6478]        # 140009148 <__mingwthr_cs_init>
   140002cd0:	83 f8 01             	cmp    eax,0x1
   140002cd3:	75 6c                	jne    140002d41 <__mingw_TLScallback+0xf0>
   140002cd5:	48 8b 05 74 64 00 00 	mov    rax,QWORD PTR [rip+0x6474]        # 140009150 <key_dtor_list>
   140002cdc:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002ce0:	eb 20                	jmp    140002d02 <__mingw_TLScallback+0xb1>
   140002ce2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ce6:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002cea:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002cee:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002cf2:	48 89 c1             	mov    rcx,rax
   140002cf5:	e8 f6 06 00 00       	call   1400033f0 <free>
   140002cfa:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002cfe:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d02:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002d07:	75 d9                	jne    140002ce2 <__mingw_TLScallback+0x91>
   140002d09:	48 c7 05 3c 64 00 00 	mov    QWORD PTR [rip+0x643c],0x0        # 140009150 <key_dtor_list>
   140002d10:	00 00 00 00 
   140002d14:	c7 05 2a 64 00 00 00 	mov    DWORD PTR [rip+0x642a],0x0        # 140009148 <__mingwthr_cs_init>
   140002d1b:	00 00 00 
   140002d1e:	48 8d 05 fb 63 00 00 	lea    rax,[rip+0x63fb]        # 140009120 <__mingwthr_cs>
   140002d25:	48 89 c1             	mov    rcx,rax
   140002d28:	48 8b 05 01 75 00 00 	mov    rax,QWORD PTR [rip+0x7501]        # 14000a230 <__imp_DeleteCriticalSection>
   140002d2f:	ff d0                	call   rax
   140002d31:	eb 0e                	jmp    140002d41 <__mingw_TLScallback+0xf0>
   140002d33:	e8 18 00 00 00       	call   140002d50 <_fpreset>
   140002d38:	eb 08                	jmp    140002d42 <__mingw_TLScallback+0xf1>
   140002d3a:	e8 73 fe ff ff       	call   140002bb2 <__mingwthr_run_key_dtors>
   140002d3f:	eb 01                	jmp    140002d42 <__mingw_TLScallback+0xf1>
   140002d41:	90                   	nop
   140002d42:	b8 01 00 00 00       	mov    eax,0x1
   140002d47:	48 83 c4 30          	add    rsp,0x30
   140002d4b:	5d                   	pop    rbp
   140002d4c:	c3                   	ret
   140002d4d:	90                   	nop
   140002d4e:	90                   	nop
   140002d4f:	90                   	nop

0000000140002d50 <_fpreset>:
   140002d50:	55                   	push   rbp
   140002d51:	48 89 e5             	mov    rbp,rsp
   140002d54:	db e3                	fninit
   140002d56:	90                   	nop
   140002d57:	5d                   	pop    rbp
   140002d58:	c3                   	ret
   140002d59:	90                   	nop
   140002d5a:	90                   	nop
   140002d5b:	90                   	nop
   140002d5c:	90                   	nop
   140002d5d:	90                   	nop
   140002d5e:	90                   	nop
   140002d5f:	90                   	nop

0000000140002d60 <_ValidateImageBase>:
   140002d60:	55                   	push   rbp
   140002d61:	48 89 e5             	mov    rbp,rsp
   140002d64:	48 83 ec 20          	sub    rsp,0x20
   140002d68:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002d6c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002d70:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d74:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d78:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002d7b:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140002d7f:	74 07                	je     140002d88 <_ValidateImageBase+0x28>
   140002d81:	b8 00 00 00 00       	mov    eax,0x0
   140002d86:	eb 4e                	jmp    140002dd6 <_ValidateImageBase+0x76>
   140002d88:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d8c:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002d8f:	48 63 d0             	movsxd rdx,eax
   140002d92:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d96:	48 01 d0             	add    rax,rdx
   140002d99:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002d9d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002da1:	8b 00                	mov    eax,DWORD PTR [rax]
   140002da3:	3d 50 45 00 00       	cmp    eax,0x4550
   140002da8:	74 07                	je     140002db1 <_ValidateImageBase+0x51>
   140002daa:	b8 00 00 00 00       	mov    eax,0x0
   140002daf:	eb 25                	jmp    140002dd6 <_ValidateImageBase+0x76>
   140002db1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002db5:	48 83 c0 18          	add    rax,0x18
   140002db9:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002dbd:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002dc1:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002dc4:	66 3d 0b 02          	cmp    ax,0x20b
   140002dc8:	74 07                	je     140002dd1 <_ValidateImageBase+0x71>
   140002dca:	b8 00 00 00 00       	mov    eax,0x0
   140002dcf:	eb 05                	jmp    140002dd6 <_ValidateImageBase+0x76>
   140002dd1:	b8 01 00 00 00       	mov    eax,0x1
   140002dd6:	48 83 c4 20          	add    rsp,0x20
   140002dda:	5d                   	pop    rbp
   140002ddb:	c3                   	ret

0000000140002ddc <_FindPESection>:
   140002ddc:	55                   	push   rbp
   140002ddd:	48 89 e5             	mov    rbp,rsp
   140002de0:	48 83 ec 20          	sub    rsp,0x20
   140002de4:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002de8:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002dec:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002df0:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002df3:	48 63 d0             	movsxd rdx,eax
   140002df6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002dfa:	48 01 d0             	add    rax,rdx
   140002dfd:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002e01:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002e08:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e0c:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002e10:	0f b7 d0             	movzx  edx,ax
   140002e13:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e17:	48 01 d0             	add    rax,rdx
   140002e1a:	48 83 c0 18          	add    rax,0x18
   140002e1e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002e22:	eb 36                	jmp    140002e5a <_FindPESection+0x7e>
   140002e24:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e28:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140002e2b:	89 c0                	mov    eax,eax
   140002e2d:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002e31:	72 1e                	jb     140002e51 <_FindPESection+0x75>
   140002e33:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e37:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140002e3a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e3e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002e41:	01 d0                	add    eax,edx
   140002e43:	89 c0                	mov    eax,eax
   140002e45:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002e49:	73 06                	jae    140002e51 <_FindPESection+0x75>
   140002e4b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e4f:	eb 1e                	jmp    140002e6f <_FindPESection+0x93>
   140002e51:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002e55:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002e5a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e5e:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002e62:	0f b7 c0             	movzx  eax,ax
   140002e65:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002e68:	72 ba                	jb     140002e24 <_FindPESection+0x48>
   140002e6a:	b8 00 00 00 00       	mov    eax,0x0
   140002e6f:	48 83 c4 20          	add    rsp,0x20
   140002e73:	5d                   	pop    rbp
   140002e74:	c3                   	ret

0000000140002e75 <_FindPESectionByName>:
   140002e75:	55                   	push   rbp
   140002e76:	48 89 e5             	mov    rbp,rsp
   140002e79:	48 83 ec 40          	sub    rsp,0x40
   140002e7d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002e81:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002e85:	48 89 c1             	mov    rcx,rax
   140002e88:	e8 8b 05 00 00       	call   140003418 <strlen>
   140002e8d:	48 83 f8 08          	cmp    rax,0x8
   140002e91:	76 0a                	jbe    140002e9d <_FindPESectionByName+0x28>
   140002e93:	b8 00 00 00 00       	mov    eax,0x0
   140002e98:	e9 98 00 00 00       	jmp    140002f35 <_FindPESectionByName+0xc0>
   140002e9d:	48 8b 05 bc 24 00 00 	mov    rax,QWORD PTR [rip+0x24bc]        # 140005360 <.refptr.__ImageBase>
   140002ea4:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002ea8:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002eac:	48 89 c1             	mov    rcx,rax
   140002eaf:	e8 ac fe ff ff       	call   140002d60 <_ValidateImageBase>
   140002eb4:	85 c0                	test   eax,eax
   140002eb6:	75 07                	jne    140002ebf <_FindPESectionByName+0x4a>
   140002eb8:	b8 00 00 00 00       	mov    eax,0x0
   140002ebd:	eb 76                	jmp    140002f35 <_FindPESectionByName+0xc0>
   140002ebf:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002ec3:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002ec6:	48 63 d0             	movsxd rdx,eax
   140002ec9:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002ecd:	48 01 d0             	add    rax,rdx
   140002ed0:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002ed4:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002edb:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002edf:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002ee3:	0f b7 d0             	movzx  edx,ax
   140002ee6:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002eea:	48 01 d0             	add    rax,rdx
   140002eed:	48 83 c0 18          	add    rax,0x18
   140002ef1:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002ef5:	eb 29                	jmp    140002f20 <_FindPESectionByName+0xab>
   140002ef7:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002efb:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140002eff:	41 b8 08 00 00 00    	mov    r8d,0x8
   140002f05:	48 89 c1             	mov    rcx,rax
   140002f08:	e8 13 05 00 00       	call   140003420 <strncmp>
   140002f0d:	85 c0                	test   eax,eax
   140002f0f:	75 06                	jne    140002f17 <_FindPESectionByName+0xa2>
   140002f11:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f15:	eb 1e                	jmp    140002f35 <_FindPESectionByName+0xc0>
   140002f17:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002f1b:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002f20:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002f24:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002f28:	0f b7 c0             	movzx  eax,ax
   140002f2b:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002f2e:	72 c7                	jb     140002ef7 <_FindPESectionByName+0x82>
   140002f30:	b8 00 00 00 00       	mov    eax,0x0
   140002f35:	48 83 c4 40          	add    rsp,0x40
   140002f39:	5d                   	pop    rbp
   140002f3a:	c3                   	ret

0000000140002f3b <__mingw_GetSectionForAddress>:
   140002f3b:	55                   	push   rbp
   140002f3c:	48 89 e5             	mov    rbp,rsp
   140002f3f:	48 83 ec 30          	sub    rsp,0x30
   140002f43:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002f47:	48 8b 05 12 24 00 00 	mov    rax,QWORD PTR [rip+0x2412]        # 140005360 <.refptr.__ImageBase>
   140002f4e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f52:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f56:	48 89 c1             	mov    rcx,rax
   140002f59:	e8 02 fe ff ff       	call   140002d60 <_ValidateImageBase>
   140002f5e:	85 c0                	test   eax,eax
   140002f60:	75 07                	jne    140002f69 <__mingw_GetSectionForAddress+0x2e>
   140002f62:	b8 00 00 00 00       	mov    eax,0x0
   140002f67:	eb 1c                	jmp    140002f85 <__mingw_GetSectionForAddress+0x4a>
   140002f69:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002f6d:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002f71:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f75:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002f79:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f7d:	48 89 c1             	mov    rcx,rax
   140002f80:	e8 57 fe ff ff       	call   140002ddc <_FindPESection>
   140002f85:	48 83 c4 30          	add    rsp,0x30
   140002f89:	5d                   	pop    rbp
   140002f8a:	c3                   	ret

0000000140002f8b <__mingw_GetSectionCount>:
   140002f8b:	55                   	push   rbp
   140002f8c:	48 89 e5             	mov    rbp,rsp
   140002f8f:	48 83 ec 30          	sub    rsp,0x30
   140002f93:	48 8b 05 c6 23 00 00 	mov    rax,QWORD PTR [rip+0x23c6]        # 140005360 <.refptr.__ImageBase>
   140002f9a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f9e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002fa2:	48 89 c1             	mov    rcx,rax
   140002fa5:	e8 b6 fd ff ff       	call   140002d60 <_ValidateImageBase>
   140002faa:	85 c0                	test   eax,eax
   140002fac:	75 07                	jne    140002fb5 <__mingw_GetSectionCount+0x2a>
   140002fae:	b8 00 00 00 00       	mov    eax,0x0
   140002fb3:	eb 20                	jmp    140002fd5 <__mingw_GetSectionCount+0x4a>
   140002fb5:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002fb9:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002fbc:	48 63 d0             	movsxd rdx,eax
   140002fbf:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002fc3:	48 01 d0             	add    rax,rdx
   140002fc6:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002fca:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fce:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002fd2:	0f b7 c0             	movzx  eax,ax
   140002fd5:	48 83 c4 30          	add    rsp,0x30
   140002fd9:	5d                   	pop    rbp
   140002fda:	c3                   	ret

0000000140002fdb <_FindPESectionExec>:
   140002fdb:	55                   	push   rbp
   140002fdc:	48 89 e5             	mov    rbp,rsp
   140002fdf:	48 83 ec 40          	sub    rsp,0x40
   140002fe3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002fe7:	48 8b 05 72 23 00 00 	mov    rax,QWORD PTR [rip+0x2372]        # 140005360 <.refptr.__ImageBase>
   140002fee:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002ff2:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002ff6:	48 89 c1             	mov    rcx,rax
   140002ff9:	e8 62 fd ff ff       	call   140002d60 <_ValidateImageBase>
   140002ffe:	85 c0                	test   eax,eax
   140003000:	75 07                	jne    140003009 <_FindPESectionExec+0x2e>
   140003002:	b8 00 00 00 00       	mov    eax,0x0
   140003007:	eb 78                	jmp    140003081 <_FindPESectionExec+0xa6>
   140003009:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000300d:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140003010:	48 63 d0             	movsxd rdx,eax
   140003013:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140003017:	48 01 d0             	add    rax,rdx
   14000301a:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000301e:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140003025:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140003029:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   14000302d:	0f b7 d0             	movzx  edx,ax
   140003030:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140003034:	48 01 d0             	add    rax,rdx
   140003037:	48 83 c0 18          	add    rax,0x18
   14000303b:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000303f:	eb 2b                	jmp    14000306c <_FindPESectionExec+0x91>
   140003041:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003045:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140003048:	25 00 00 00 20       	and    eax,0x20000000
   14000304d:	85 c0                	test   eax,eax
   14000304f:	74 12                	je     140003063 <_FindPESectionExec+0x88>
   140003051:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140003056:	75 06                	jne    14000305e <_FindPESectionExec+0x83>
   140003058:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000305c:	eb 23                	jmp    140003081 <_FindPESectionExec+0xa6>
   14000305e:	48 83 6d 10 01       	sub    QWORD PTR [rbp+0x10],0x1
   140003063:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140003067:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   14000306c:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140003070:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140003074:	0f b7 c0             	movzx  eax,ax
   140003077:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   14000307a:	72 c5                	jb     140003041 <_FindPESectionExec+0x66>
   14000307c:	b8 00 00 00 00       	mov    eax,0x0
   140003081:	48 83 c4 40          	add    rsp,0x40
   140003085:	5d                   	pop    rbp
   140003086:	c3                   	ret

0000000140003087 <_GetPEImageBase>:
   140003087:	55                   	push   rbp
   140003088:	48 89 e5             	mov    rbp,rsp
   14000308b:	48 83 ec 30          	sub    rsp,0x30
   14000308f:	48 8b 05 ca 22 00 00 	mov    rax,QWORD PTR [rip+0x22ca]        # 140005360 <.refptr.__ImageBase>
   140003096:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000309a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000309e:	48 89 c1             	mov    rcx,rax
   1400030a1:	e8 ba fc ff ff       	call   140002d60 <_ValidateImageBase>
   1400030a6:	85 c0                	test   eax,eax
   1400030a8:	75 07                	jne    1400030b1 <_GetPEImageBase+0x2a>
   1400030aa:	b8 00 00 00 00       	mov    eax,0x0
   1400030af:	eb 04                	jmp    1400030b5 <_GetPEImageBase+0x2e>
   1400030b1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030b5:	48 83 c4 30          	add    rsp,0x30
   1400030b9:	5d                   	pop    rbp
   1400030ba:	c3                   	ret

00000001400030bb <_IsNonwritableInCurrentImage>:
   1400030bb:	55                   	push   rbp
   1400030bc:	48 89 e5             	mov    rbp,rsp
   1400030bf:	48 83 ec 40          	sub    rsp,0x40
   1400030c3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400030c7:	48 8b 05 92 22 00 00 	mov    rax,QWORD PTR [rip+0x2292]        # 140005360 <.refptr.__ImageBase>
   1400030ce:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400030d2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030d6:	48 89 c1             	mov    rcx,rax
   1400030d9:	e8 82 fc ff ff       	call   140002d60 <_ValidateImageBase>
   1400030de:	85 c0                	test   eax,eax
   1400030e0:	75 07                	jne    1400030e9 <_IsNonwritableInCurrentImage+0x2e>
   1400030e2:	b8 00 00 00 00       	mov    eax,0x0
   1400030e7:	eb 3d                	jmp    140003126 <_IsNonwritableInCurrentImage+0x6b>
   1400030e9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400030ed:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   1400030f1:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400030f5:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   1400030f9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030fd:	48 89 c1             	mov    rcx,rax
   140003100:	e8 d7 fc ff ff       	call   140002ddc <_FindPESection>
   140003105:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140003109:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   14000310e:	75 07                	jne    140003117 <_IsNonwritableInCurrentImage+0x5c>
   140003110:	b8 00 00 00 00       	mov    eax,0x0
   140003115:	eb 0f                	jmp    140003126 <_IsNonwritableInCurrentImage+0x6b>
   140003117:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000311b:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   14000311e:	f7 d0                	not    eax
   140003120:	c1 e8 1f             	shr    eax,0x1f
   140003123:	0f b6 c0             	movzx  eax,al
   140003126:	48 83 c4 40          	add    rsp,0x40
   14000312a:	5d                   	pop    rbp
   14000312b:	c3                   	ret

000000014000312c <__mingw_enum_import_library_names>:
   14000312c:	55                   	push   rbp
   14000312d:	48 89 e5             	mov    rbp,rsp
   140003130:	48 83 ec 50          	sub    rsp,0x50
   140003134:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140003137:	48 8b 05 22 22 00 00 	mov    rax,QWORD PTR [rip+0x2222]        # 140005360 <.refptr.__ImageBase>
   14000313e:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140003142:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003146:	48 89 c1             	mov    rcx,rax
   140003149:	e8 12 fc ff ff       	call   140002d60 <_ValidateImageBase>
   14000314e:	85 c0                	test   eax,eax
   140003150:	75 0a                	jne    14000315c <__mingw_enum_import_library_names+0x30>
   140003152:	b8 00 00 00 00       	mov    eax,0x0
   140003157:	e9 ab 00 00 00       	jmp    140003207 <__mingw_enum_import_library_names+0xdb>
   14000315c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003160:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140003163:	48 63 d0             	movsxd rdx,eax
   140003166:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000316a:	48 01 d0             	add    rax,rdx
   14000316d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140003171:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140003175:	8b 80 90 00 00 00    	mov    eax,DWORD PTR [rax+0x90]
   14000317b:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   14000317e:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140003182:	75 07                	jne    14000318b <__mingw_enum_import_library_names+0x5f>
   140003184:	b8 00 00 00 00       	mov    eax,0x0
   140003189:	eb 7c                	jmp    140003207 <__mingw_enum_import_library_names+0xdb>
   14000318b:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   14000318e:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003192:	48 89 c1             	mov    rcx,rax
   140003195:	e8 42 fc ff ff       	call   140002ddc <_FindPESection>
   14000319a:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000319e:	48 83 7d d8 00       	cmp    QWORD PTR [rbp-0x28],0x0
   1400031a3:	75 07                	jne    1400031ac <__mingw_enum_import_library_names+0x80>
   1400031a5:	b8 00 00 00 00       	mov    eax,0x0
   1400031aa:	eb 5b                	jmp    140003207 <__mingw_enum_import_library_names+0xdb>
   1400031ac:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   1400031af:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400031b3:	48 01 d0             	add    rax,rdx
   1400031b6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400031ba:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400031bf:	75 07                	jne    1400031c8 <__mingw_enum_import_library_names+0x9c>
   1400031c1:	b8 00 00 00 00       	mov    eax,0x0
   1400031c6:	eb 3f                	jmp    140003207 <__mingw_enum_import_library_names+0xdb>
   1400031c8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400031cc:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400031cf:	85 c0                	test   eax,eax
   1400031d1:	75 0b                	jne    1400031de <__mingw_enum_import_library_names+0xb2>
   1400031d3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400031d7:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400031da:	85 c0                	test   eax,eax
   1400031dc:	74 23                	je     140003201 <__mingw_enum_import_library_names+0xd5>
   1400031de:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   1400031e2:	7f 12                	jg     1400031f6 <__mingw_enum_import_library_names+0xca>
   1400031e4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400031e8:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400031eb:	89 c2                	mov    edx,eax
   1400031ed:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400031f1:	48 01 d0             	add    rax,rdx
   1400031f4:	eb 11                	jmp    140003207 <__mingw_enum_import_library_names+0xdb>
   1400031f6:	83 6d 10 01          	sub    DWORD PTR [rbp+0x10],0x1
   1400031fa:	48 83 45 f8 14       	add    QWORD PTR [rbp-0x8],0x14
   1400031ff:	eb c7                	jmp    1400031c8 <__mingw_enum_import_library_names+0x9c>
   140003201:	90                   	nop
   140003202:	b8 00 00 00 00       	mov    eax,0x0
   140003207:	48 83 c4 50          	add    rsp,0x50
   14000320b:	5d                   	pop    rbp
   14000320c:	c3                   	ret
   14000320d:	90                   	nop
   14000320e:	90                   	nop
   14000320f:	90                   	nop

0000000140003210 <_Unwind_Resume>:
   140003210:	ff 25 da 6f 00 00    	jmp    QWORD PTR [rip+0x6fda]        # 14000a1f0 <__IAT_start__>
   140003216:	90                   	nop
   140003217:	90                   	nop
   140003218:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000321f:	00 

0000000140003220 <___chkstk_ms>:
   140003220:	51                   	push   rcx
   140003221:	50                   	push   rax
   140003222:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003228:	48 8d 4c 24 18       	lea    rcx,[rsp+0x18]
   14000322d:	72 19                	jb     140003248 <___chkstk_ms+0x28>
   14000322f:	48 81 e9 00 10 00 00 	sub    rcx,0x1000
   140003236:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   14000323a:	48 2d 00 10 00 00    	sub    rax,0x1000
   140003240:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003246:	77 e7                	ja     14000322f <___chkstk_ms+0xf>
   140003248:	48 29 c1             	sub    rcx,rax
   14000324b:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   14000324f:	58                   	pop    rax
   140003250:	59                   	pop    rcx
   140003251:	c3                   	ret
   140003252:	90                   	nop
   140003253:	90                   	nop
   140003254:	90                   	nop
   140003255:	90                   	nop
   140003256:	90                   	nop
   140003257:	90                   	nop
   140003258:	90                   	nop
   140003259:	90                   	nop
   14000325a:	90                   	nop
   14000325b:	90                   	nop
   14000325c:	90                   	nop
   14000325d:	90                   	nop
   14000325e:	90                   	nop
   14000325f:	90                   	nop

0000000140003260 <_initterm_e>:
   140003260:	55                   	push   rbp
   140003261:	48 89 e5             	mov    rbp,rsp
   140003264:	48 83 ec 30          	sub    rsp,0x30
   140003268:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000326c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140003270:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140003274:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003278:	eb 29                	jmp    1400032a3 <_initterm_e+0x43>
   14000327a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000327e:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140003281:	48 85 c0             	test   rax,rax
   140003284:	74 17                	je     14000329d <_initterm_e+0x3d>
   140003286:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000328a:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000328d:	ff d0                	call   rax
   14000328f:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140003292:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   140003296:	74 06                	je     14000329e <_initterm_e+0x3e>
   140003298:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000329b:	eb 15                	jmp    1400032b2 <_initterm_e+0x52>
   14000329d:	90                   	nop
   14000329e:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   1400032a3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400032a7:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   1400032ab:	72 cd                	jb     14000327a <_initterm_e+0x1a>
   1400032ad:	b8 00 00 00 00       	mov    eax,0x0
   1400032b2:	48 83 c4 30          	add    rsp,0x30
   1400032b6:	5d                   	pop    rbp
   1400032b7:	c3                   	ret
   1400032b8:	90                   	nop
   1400032b9:	90                   	nop
   1400032ba:	90                   	nop
   1400032bb:	90                   	nop
   1400032bc:	90                   	nop
   1400032bd:	90                   	nop
   1400032be:	90                   	nop
   1400032bf:	90                   	nop

00000001400032c0 <__p__fmode>:
   1400032c0:	55                   	push   rbp
   1400032c1:	48 89 e5             	mov    rbp,rsp
   1400032c4:	48 8b 05 05 21 00 00 	mov    rax,QWORD PTR [rip+0x2105]        # 1400053d0 <.refptr.__imp__fmode>
   1400032cb:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400032ce:	5d                   	pop    rbp
   1400032cf:	c3                   	ret

00000001400032d0 <__p__commode>:
   1400032d0:	55                   	push   rbp
   1400032d1:	48 89 e5             	mov    rbp,rsp
   1400032d4:	48 8b 05 e5 20 00 00 	mov    rax,QWORD PTR [rip+0x20e5]        # 1400053c0 <.refptr.__imp__commode>
   1400032db:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400032de:	5d                   	pop    rbp
   1400032df:	c3                   	ret

00000001400032e0 <__p___initenv>:
   1400032e0:	55                   	push   rbp
   1400032e1:	48 89 e5             	mov    rbp,rsp
   1400032e4:	48 8b 05 c5 20 00 00 	mov    rax,QWORD PTR [rip+0x20c5]        # 1400053b0 <.refptr.__imp___initenv>
   1400032eb:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400032ee:	5d                   	pop    rbp
   1400032ef:	c3                   	ret

00000001400032f0 <_set_invalid_parameter_handler>:
   1400032f0:	55                   	push   rbp
   1400032f1:	48 89 e5             	mov    rbp,rsp
   1400032f4:	48 83 ec 10          	sub    rsp,0x10
   1400032f8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400032fc:	48 8d 05 8d 5e 00 00 	lea    rax,[rip+0x5e8d]        # 140009190 <handler>
   140003303:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003307:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000330b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000330f:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140003313:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003317:	48 87 10             	xchg   QWORD PTR [rax],rdx
   14000331a:	48 89 d0             	mov    rax,rdx
   14000331d:	48 83 c4 10          	add    rsp,0x10
   140003321:	5d                   	pop    rbp
   140003322:	c3                   	ret

0000000140003323 <_get_invalid_parameter_handler>:
   140003323:	55                   	push   rbp
   140003324:	48 89 e5             	mov    rbp,rsp
   140003327:	48 8b 05 62 5e 00 00 	mov    rax,QWORD PTR [rip+0x5e62]        # 140009190 <handler>
   14000332e:	5d                   	pop    rbp
   14000332f:	c3                   	ret

0000000140003330 <_configthreadlocale>:
   140003330:	55                   	push   rbp
   140003331:	48 89 e5             	mov    rbp,rsp
   140003334:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140003337:	83 7d 10 01          	cmp    DWORD PTR [rbp+0x10],0x1
   14000333b:	75 07                	jne    140003344 <_configthreadlocale+0x14>
   14000333d:	b8 ff ff ff ff       	mov    eax,0xffffffff
   140003342:	eb 05                	jmp    140003349 <_configthreadlocale+0x19>
   140003344:	b8 02 00 00 00       	mov    eax,0x2
   140003349:	5d                   	pop    rbp
   14000334a:	c3                   	ret
   14000334b:	90                   	nop
   14000334c:	90                   	nop
   14000334d:	90                   	nop
   14000334e:	90                   	nop
   14000334f:	90                   	nop

0000000140003350 <__acrt_iob_func>:
   140003350:	55                   	push   rbp
   140003351:	48 89 e5             	mov    rbp,rsp
   140003354:	48 83 ec 20          	sub    rsp,0x20
   140003358:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000335b:	e8 30 00 00 00       	call   140003390 <__iob_func>
   140003360:	48 89 c1             	mov    rcx,rax
   140003363:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140003366:	48 89 d0             	mov    rax,rdx
   140003369:	48 01 c0             	add    rax,rax
   14000336c:	48 01 d0             	add    rax,rdx
   14000336f:	48 c1 e0 04          	shl    rax,0x4
   140003373:	48 01 c8             	add    rax,rcx
   140003376:	48 83 c4 20          	add    rsp,0x20
   14000337a:	5d                   	pop    rbp
   14000337b:	c3                   	ret
   14000337c:	90                   	nop
   14000337d:	90                   	nop
   14000337e:	90                   	nop
   14000337f:	90                   	nop

0000000140003380 <__C_specific_handler>:
   140003380:	ff 25 22 6f 00 00    	jmp    QWORD PTR [rip+0x6f22]        # 14000a2a8 <__imp___C_specific_handler>
   140003386:	90                   	nop
   140003387:	90                   	nop

0000000140003388 <__getmainargs>:
   140003388:	ff 25 22 6f 00 00    	jmp    QWORD PTR [rip+0x6f22]        # 14000a2b0 <__imp___getmainargs>
   14000338e:	90                   	nop
   14000338f:	90                   	nop

0000000140003390 <__iob_func>:
   140003390:	ff 25 2a 6f 00 00    	jmp    QWORD PTR [rip+0x6f2a]        # 14000a2c0 <__imp___iob_func>
   140003396:	90                   	nop
   140003397:	90                   	nop

0000000140003398 <__set_app_type>:
   140003398:	ff 25 2a 6f 00 00    	jmp    QWORD PTR [rip+0x6f2a]        # 14000a2c8 <__imp___set_app_type>
   14000339e:	90                   	nop
   14000339f:	90                   	nop

00000001400033a0 <__setusermatherr>:
   1400033a0:	ff 25 2a 6f 00 00    	jmp    QWORD PTR [rip+0x6f2a]        # 14000a2d0 <__imp___setusermatherr>
   1400033a6:	90                   	nop
   1400033a7:	90                   	nop

00000001400033a8 <_amsg_exit>:
   1400033a8:	ff 25 2a 6f 00 00    	jmp    QWORD PTR [rip+0x6f2a]        # 14000a2d8 <__imp__amsg_exit>
   1400033ae:	90                   	nop
   1400033af:	90                   	nop

00000001400033b0 <_cexit>:
   1400033b0:	ff 25 2a 6f 00 00    	jmp    QWORD PTR [rip+0x6f2a]        # 14000a2e0 <__imp__cexit>
   1400033b6:	90                   	nop
   1400033b7:	90                   	nop

00000001400033b8 <_initterm>:
   1400033b8:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a2f8 <__imp__initterm>
   1400033be:	90                   	nop
   1400033bf:	90                   	nop

00000001400033c0 <_crt_atexit>:
   1400033c0:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a300 <__imp__crt_atexit>
   1400033c6:	90                   	nop
   1400033c7:	90                   	nop

00000001400033c8 <abort>:
   1400033c8:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a308 <__imp_abort>
   1400033ce:	90                   	nop
   1400033cf:	90                   	nop

00000001400033d0 <calloc>:
   1400033d0:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a310 <__imp_calloc>
   1400033d6:	90                   	nop
   1400033d7:	90                   	nop

00000001400033d8 <exit>:
   1400033d8:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a318 <__imp_exit>
   1400033de:	90                   	nop
   1400033df:	90                   	nop

00000001400033e0 <fflush>:
   1400033e0:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a320 <__imp_fflush>
   1400033e6:	90                   	nop
   1400033e7:	90                   	nop

00000001400033e8 <fprintf>:
   1400033e8:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a328 <__imp_fprintf>
   1400033ee:	90                   	nop
   1400033ef:	90                   	nop

00000001400033f0 <free>:
   1400033f0:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a330 <__imp_free>
   1400033f6:	90                   	nop
   1400033f7:	90                   	nop

00000001400033f8 <malloc>:
   1400033f8:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a338 <__imp_malloc>
   1400033fe:	90                   	nop
   1400033ff:	90                   	nop

0000000140003400 <memcpy>:
   140003400:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a340 <__imp_memcpy>
   140003406:	90                   	nop
   140003407:	90                   	nop

0000000140003408 <setvbuf>:
   140003408:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a348 <__imp_setvbuf>
   14000340e:	90                   	nop
   14000340f:	90                   	nop

0000000140003410 <signal>:
   140003410:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a350 <__imp_signal>
   140003416:	90                   	nop
   140003417:	90                   	nop

0000000140003418 <strlen>:
   140003418:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a358 <__imp_strlen>
   14000341e:	90                   	nop
   14000341f:	90                   	nop

0000000140003420 <strncmp>:
   140003420:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a360 <__imp_strncmp>
   140003426:	90                   	nop
   140003427:	90                   	nop

0000000140003428 <vfprintf>:
   140003428:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a368 <__imp_vfprintf>
   14000342e:	90                   	nop
   14000342f:	90                   	nop

0000000140003430 <VirtualQuery>:
   140003430:	ff 25 62 6e 00 00    	jmp    QWORD PTR [rip+0x6e62]        # 14000a298 <__imp_VirtualQuery>
   140003436:	90                   	nop
   140003437:	90                   	nop

0000000140003438 <VirtualProtect>:
   140003438:	ff 25 52 6e 00 00    	jmp    QWORD PTR [rip+0x6e52]        # 14000a290 <__imp_VirtualProtect>
   14000343e:	90                   	nop
   14000343f:	90                   	nop

0000000140003440 <TlsGetValue>:
   140003440:	ff 25 42 6e 00 00    	jmp    QWORD PTR [rip+0x6e42]        # 14000a288 <__imp_TlsGetValue>
   140003446:	90                   	nop
   140003447:	90                   	nop

0000000140003448 <Sleep>:
   140003448:	ff 25 32 6e 00 00    	jmp    QWORD PTR [rip+0x6e32]        # 14000a280 <__imp_Sleep>
   14000344e:	90                   	nop
   14000344f:	90                   	nop

0000000140003450 <SetUnhandledExceptionFilter>:
   140003450:	ff 25 22 6e 00 00    	jmp    QWORD PTR [rip+0x6e22]        # 14000a278 <__imp_SetUnhandledExceptionFilter>
   140003456:	90                   	nop
   140003457:	90                   	nop

0000000140003458 <LoadLibraryA>:
   140003458:	ff 25 12 6e 00 00    	jmp    QWORD PTR [rip+0x6e12]        # 14000a270 <__imp_LoadLibraryA>
   14000345e:	90                   	nop
   14000345f:	90                   	nop

0000000140003460 <LeaveCriticalSection>:
   140003460:	ff 25 02 6e 00 00    	jmp    QWORD PTR [rip+0x6e02]        # 14000a268 <__imp_LeaveCriticalSection>
   140003466:	90                   	nop
   140003467:	90                   	nop

0000000140003468 <InitializeCriticalSection>:
   140003468:	ff 25 f2 6d 00 00    	jmp    QWORD PTR [rip+0x6df2]        # 14000a260 <__imp_InitializeCriticalSection>
   14000346e:	90                   	nop
   14000346f:	90                   	nop

0000000140003470 <GetProcAddress>:
   140003470:	ff 25 e2 6d 00 00    	jmp    QWORD PTR [rip+0x6de2]        # 14000a258 <__imp_GetProcAddress>
   140003476:	90                   	nop
   140003477:	90                   	nop

0000000140003478 <GetModuleHandleA>:
   140003478:	ff 25 d2 6d 00 00    	jmp    QWORD PTR [rip+0x6dd2]        # 14000a250 <__imp_GetModuleHandleA>
   14000347e:	90                   	nop
   14000347f:	90                   	nop

0000000140003480 <GetLastError>:
   140003480:	ff 25 c2 6d 00 00    	jmp    QWORD PTR [rip+0x6dc2]        # 14000a248 <__imp_GetLastError>
   140003486:	90                   	nop
   140003487:	90                   	nop

0000000140003488 <FreeLibrary>:
   140003488:	ff 25 b2 6d 00 00    	jmp    QWORD PTR [rip+0x6db2]        # 14000a240 <__imp_FreeLibrary>
   14000348e:	90                   	nop
   14000348f:	90                   	nop

0000000140003490 <EnterCriticalSection>:
   140003490:	ff 25 a2 6d 00 00    	jmp    QWORD PTR [rip+0x6da2]        # 14000a238 <__imp_EnterCriticalSection>
   140003496:	90                   	nop
   140003497:	90                   	nop

0000000140003498 <DeleteCriticalSection>:
   140003498:	ff 25 92 6d 00 00    	jmp    QWORD PTR [rip+0x6d92]        # 14000a230 <__imp_DeleteCriticalSection>
   14000349e:	90                   	nop
   14000349f:	90                   	nop

00000001400034a0 <main.cold>:
   1400034a0:	48 89 f9             	mov    rcx,rdi
   1400034a3:	e8 b8 e2 ff ff       	call   140001760 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]>
   1400034a8:	48 89 d9             	mov    rcx,rbx
   1400034ab:	e8 60 fd ff ff       	call   140003210 <_Unwind_Resume>
   1400034b0:	90                   	nop
   1400034b1:	90                   	nop
   1400034b2:	90                   	nop
   1400034b3:	90                   	nop
   1400034b4:	90                   	nop
   1400034b5:	90                   	nop
   1400034b6:	90                   	nop
   1400034b7:	90                   	nop
   1400034b8:	90                   	nop
   1400034b9:	90                   	nop
   1400034ba:	90                   	nop
   1400034bb:	90                   	nop
   1400034bc:	90                   	nop
   1400034bd:	90                   	nop
   1400034be:	90                   	nop
   1400034bf:	90                   	nop

00000001400034c0 <main>:
   1400034c0:	41 54                	push   r12
   1400034c2:	55                   	push   rbp
   1400034c3:	57                   	push   rdi
   1400034c4:	56                   	push   rsi
   1400034c5:	53                   	push   rbx
   1400034c6:	48 83 ec 60          	sub    rsp,0x60
   1400034ca:	31 ff                	xor    edi,edi
   1400034cc:	31 f6                	xor    esi,esi
   1400034ce:	e8 24 e5 ff ff       	call   1400019f7 <__main>
   1400034d3:	48 8d 6c 24 38       	lea    rbp,[rsp+0x38]
   1400034d8:	66 0f ef c0          	pxor   xmm0,xmm0
   1400034dc:	c7 44 24 38 00 00 00 	mov    DWORD PTR [rsp+0x38],0x0
   1400034e3:	00 
   1400034e4:	66 48 0f 6e cd       	movq   xmm1,rbp
   1400034e9:	48 89 6c 24 50       	mov    QWORD PTR [rsp+0x50],rbp
   1400034ee:	48 c7 44 24 58 00 00 	mov    QWORD PTR [rsp+0x58],0x0
   1400034f5:	00 00 
   1400034f7:	66 0f 6c c1          	punpcklqdq xmm0,xmm1
   1400034fb:	0f 29 44 24 40       	movaps XMMWORD PTR [rsp+0x40],xmm0
   140003500:	48 85 ff             	test   rdi,rdi
   140003503:	0f 84 ef 00 00 00    	je     1400035f8 <main+0x138>
   140003509:	48 89 fb             	mov    rbx,rdi
   14000350c:	eb 15                	jmp    140003523 <main+0x63>
   14000350e:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   140003515:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000351c:	00 00 00 00 
   140003520:	48 89 c3             	mov    rbx,rax
   140003523:	8b 53 20             	mov    edx,DWORD PTR [rbx+0x20]
   140003526:	48 8b 43 18          	mov    rax,QWORD PTR [rbx+0x18]
   14000352a:	39 f2                	cmp    edx,esi
   14000352c:	48 0f 4f 43 10       	cmovg  rax,QWORD PTR [rbx+0x10]
   140003531:	0f 9f c1             	setg   cl
   140003534:	48 85 c0             	test   rax,rax
   140003537:	75 e7                	jne    140003520 <main+0x60>
   140003539:	84 c9                	test   cl,cl
   14000353b:	0f 85 ba 00 00 00    	jne    1400035fb <main+0x13b>
   140003541:	39 d6                	cmp    esi,edx
   140003543:	7e 39                	jle    14000357e <main+0xbe>
   140003545:	41 bc 01 00 00 00    	mov    r12d,0x1
   14000354b:	48 39 eb             	cmp    rbx,rbp
   14000354e:	0f 85 cc 00 00 00    	jne    140003620 <main+0x160>
   140003554:	b9 28 00 00 00       	mov    ecx,0x28
   140003559:	e8 ba e3 ff ff       	call   140001918 <operator new(unsigned long long)>
   14000355e:	89 70 20             	mov    DWORD PTR [rax+0x20],esi
   140003561:	41 0f b6 cc          	movzx  ecx,r12b
   140003565:	49 89 e9             	mov    r9,rbp
   140003568:	49 89 d8             	mov    r8,rbx
   14000356b:	48 89 c2             	mov    rdx,rax
   14000356e:	e8 b5 e3 ff ff       	call   140001928 <std::_Rb_tree_insert_and_rebalance(bool, std::_Rb_tree_node_base*, std::_Rb_tree_node_base*, std::_Rb_tree_node_base&)>
   140003573:	48 83 44 24 58 01    	add    QWORD PTR [rsp+0x58],0x1
   140003579:	48 8b 7c 24 40       	mov    rdi,QWORD PTR [rsp+0x40]
   14000357e:	83 c6 01             	add    esi,0x1
   140003581:	83 fe 64             	cmp    esi,0x64
   140003584:	0f 85 76 ff ff ff    	jne    140003500 <main+0x40>
   14000358a:	48 85 ff             	test   rdi,rdi
   14000358d:	0f 84 99 00 00 00    	je     14000362c <main+0x16c>
   140003593:	48 89 f8             	mov    rax,rdi
   140003596:	49 89 e8             	mov    r8,rbp
   140003599:	eb 10                	jmp    1400035ab <main+0xeb>
   14000359b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   1400035a0:	49 89 c0             	mov    r8,rax
   1400035a3:	48 89 c8             	mov    rax,rcx
   1400035a6:	48 85 c0             	test   rax,rax
   1400035a9:	74 16                	je     1400035c1 <main+0x101>
   1400035ab:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   1400035af:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
   1400035b3:	83 78 20 29          	cmp    DWORD PTR [rax+0x20],0x29
   1400035b7:	7f e7                	jg     1400035a0 <main+0xe0>
   1400035b9:	48 89 d0             	mov    rax,rdx
   1400035bc:	48 85 c0             	test   rax,rax
   1400035bf:	75 ea                	jne    1400035ab <main+0xeb>
   1400035c1:	49 39 e8             	cmp    r8,rbp
   1400035c4:	74 09                	je     1400035cf <main+0x10f>
   1400035c6:	41 83 78 20 2b       	cmp    DWORD PTR [r8+0x20],0x2b
   1400035cb:	4c 0f 4d c5          	cmovge r8,rbp
   1400035cf:	49 39 e8             	cmp    r8,rbp
   1400035d2:	48 89 f9             	mov    rcx,rdi
   1400035d5:	0f 95 c0             	setne  al
   1400035d8:	88 44 24 2f          	mov    BYTE PTR [rsp+0x2f],al
   1400035dc:	0f b6 44 24 2f       	movzx  eax,BYTE PTR [rsp+0x2f]
   1400035e1:	e8 7a e1 ff ff       	call   140001760 <std::_Rb_tree<int, int, std::_Identity<int>, std::less<int>, std::allocator<int> >::_M_erase(std::_Rb_tree_node<int>*) [clone .isra.0]>
   1400035e6:	31 c0                	xor    eax,eax
   1400035e8:	48 83 c4 60          	add    rsp,0x60
   1400035ec:	5b                   	pop    rbx
   1400035ed:	5e                   	pop    rsi
   1400035ee:	5f                   	pop    rdi
   1400035ef:	5d                   	pop    rbp
   1400035f0:	41 5c                	pop    r12
   1400035f2:	c3                   	ret
   1400035f3:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   1400035f8:	48 89 eb             	mov    rbx,rbp
   1400035fb:	48 3b 5c 24 48       	cmp    rbx,QWORD PTR [rsp+0x48]
   140003600:	0f 84 3f ff ff ff    	je     140003545 <main+0x85>
   140003606:	48 89 d9             	mov    rcx,rbx
   140003609:	e8 22 e3 ff ff       	call   140001930 <std::_Rb_tree_decrement(std::_Rb_tree_node_base*)>
   14000360e:	8b 50 20             	mov    edx,DWORD PTR [rax+0x20]
   140003611:	e9 2b ff ff ff       	jmp    140003541 <main+0x81>
   140003616:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   14000361d:	00 00 00 
   140003620:	39 73 20             	cmp    DWORD PTR [rbx+0x20],esi
   140003623:	41 0f 9f c4          	setg   r12b
   140003627:	e9 28 ff ff ff       	jmp    140003554 <main+0x94>
   14000362c:	49 89 e8             	mov    r8,rbp
   14000362f:	eb 9e                	jmp    1400035cf <main+0x10f>
   140003631:	48 89 c3             	mov    rbx,rax
   140003634:	e9 67 fe ff ff       	jmp    1400034a0 <main.cold>
   140003639:	90                   	nop
   14000363a:	90                   	nop
   14000363b:	90                   	nop
   14000363c:	90                   	nop
   14000363d:	90                   	nop
   14000363e:	90                   	nop
   14000363f:	90                   	nop

0000000140003640 <register_frame_ctor>:
   140003640:	e9 2b e0 ff ff       	jmp    140001670 <__gcc_register_frame>
   140003645:	90                   	nop
   140003646:	90                   	nop
   140003647:	90                   	nop
   140003648:	90                   	nop
   140003649:	90                   	nop
   14000364a:	90                   	nop
   14000364b:	90                   	nop
   14000364c:	90                   	nop
   14000364d:	90                   	nop
   14000364e:	90                   	nop
   14000364f:	90                   	nop
