
ch85_uset_test.exe:     file format pei-x86-64


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
   140001024:	e8 07 22 00 00       	call   140003230 <fflush>
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
   1400010e8:	48 8b 05 a9 91 00 00 	mov    rax,QWORD PTR [rip+0x91a9]        # 14000a298 <__imp_Sleep>
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
   14000113b:	e8 b8 20 00 00       	call   1400031f8 <_amsg_exit>
   140001140:	48 8b 05 f9 42 00 00 	mov    rax,QWORD PTR [rip+0x42f9]        # 140005440 <.refptr.__native_startup_state>
   140001147:	8b 00                	mov    eax,DWORD PTR [rax]
   140001149:	85 c0                	test   eax,eax
   14000114b:	0f 85 e3 01 00 00    	jne    140001334 <__tmainCRTStartup+0x2a6>
   140001151:	48 8b 05 e8 42 00 00 	mov    rax,QWORD PTR [rip+0x42e8]        # 140005440 <.refptr.__native_startup_state>
   140001158:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000115e:	b9 02 00 00 00       	mov    ecx,0x2
   140001163:	e8 38 20 00 00       	call   1400031a0 <__acrt_iob_func>
   140001168:	41 b9 00 00 00 00    	mov    r9d,0x0
   14000116e:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001174:	ba 00 00 00 00       	mov    edx,0x0
   140001179:	48 89 c1             	mov    rcx,rax
   14000117c:	e8 df 20 00 00       	call   140003260 <setvbuf>
   140001181:	48 8d 05 8f fe ff ff 	lea    rax,[rip+0xfffffffffffffe8f]        # 140001017 <safe_flush>
   140001188:	48 89 c1             	mov    rcx,rax
   14000118b:	e8 9f 04 00 00       	call   14000162f <atexit>
   140001190:	85 c0                	test   eax,eax
   140001192:	74 05                	je     140001199 <__tmainCRTStartup+0x10b>
   140001194:	e8 7f 20 00 00       	call   140003218 <abort>
   140001199:	e8 f2 10 00 00       	call   140002290 <_pei386_runtime_relocator>
   14000119e:	48 8b 05 1b 43 00 00 	mov    rax,QWORD PTR [rip+0x431b]        # 1400054c0 <.refptr._gnu_exception_handler>
   1400011a5:	48 89 c1             	mov    rcx,rax
   1400011a8:	48 8b 05 e1 90 00 00 	mov    rax,QWORD PTR [rip+0x90e1]        # 14000a290 <__imp_SetUnhandledExceptionFilter>
   1400011af:	ff d0                	call   rax
   1400011b1:	48 8b 15 68 42 00 00 	mov    rdx,QWORD PTR [rip+0x4268]        # 140005420 <.refptr.__mingw_oldexcpt_handler>
   1400011b8:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400011bb:	48 8d 05 3e fe ff ff 	lea    rax,[rip+0xfffffffffffffe3e]        # 140001000 <__mingw_invalidParameterHandler>
   1400011c2:	48 89 c1             	mov    rcx,rax
   1400011c5:	e8 76 1f 00 00       	call   140003140 <_set_invalid_parameter_handler>
   1400011ca:	e8 d1 19 00 00       	call   140002ba0 <_fpreset>
   1400011cf:	e8 18 02 00 00       	call   1400013ec <check_managed_app>
   1400011d4:	89 05 3e 7e 00 00    	mov    DWORD PTR [rip+0x7e3e],eax        # 140009018 <managedapp>
   1400011da:	48 8b 05 ff 41 00 00 	mov    rax,QWORD PTR [rip+0x41ff]        # 1400053e0 <.refptr.__mingw_app_type>
   1400011e1:	8b 00                	mov    eax,DWORD PTR [rax]
   1400011e3:	85 c0                	test   eax,eax
   1400011e5:	74 0c                	je     1400011f3 <__tmainCRTStartup+0x165>
   1400011e7:	b9 02 00 00 00       	mov    ecx,0x2
   1400011ec:	e8 f7 1f 00 00       	call   1400031e8 <__set_app_type>
   1400011f1:	eb 0a                	jmp    1400011fd <__tmainCRTStartup+0x16f>
   1400011f3:	b9 01 00 00 00       	mov    ecx,0x1
   1400011f8:	e8 eb 1f 00 00       	call   1400031e8 <__set_app_type>
   1400011fd:	e8 0e 1f 00 00       	call   140003110 <__p__fmode>
   140001202:	48 8b 15 a7 42 00 00 	mov    rdx,QWORD PTR [rip+0x42a7]        # 1400054b0 <.refptr._fmode>
   140001209:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000120b:	89 10                	mov    DWORD PTR [rax],edx
   14000120d:	e8 0e 1f 00 00       	call   140003120 <__p__commode>
   140001212:	48 8b 15 77 42 00 00 	mov    rdx,QWORD PTR [rip+0x4277]        # 140005490 <.refptr._commode>
   140001219:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000121b:	89 10                	mov    DWORD PTR [rax],edx
   14000121d:	e8 4e 06 00 00       	call   140001870 <_setargv>
   140001222:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140001225:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140001229:	79 0a                	jns    140001235 <__tmainCRTStartup+0x1a7>
   14000122b:	b9 08 00 00 00       	mov    ecx,0x8
   140001230:	e8 c3 1f 00 00       	call   1400031f8 <_amsg_exit>
   140001235:	48 8b 05 04 41 00 00 	mov    rax,QWORD PTR [rip+0x4104]        # 140005340 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   14000123c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000123e:	83 f8 01             	cmp    eax,0x1
   140001241:	75 0f                	jne    140001252 <__tmainCRTStartup+0x1c4>
   140001243:	48 8b 05 86 42 00 00 	mov    rax,QWORD PTR [rip+0x4286]        # 1400054d0 <.refptr._matherr>
   14000124a:	48 89 c1             	mov    rcx,rax
   14000124d:	e8 58 11 00 00       	call   1400023aa <__mingw_setusermatherr>
   140001252:	48 8b 05 47 41 00 00 	mov    rax,QWORD PTR [rip+0x4147]        # 1400053a0 <.refptr.__globallocalestatus>
   140001259:	8b 00                	mov    eax,DWORD PTR [rax]
   14000125b:	83 f8 ff             	cmp    eax,0xffffffff
   14000125e:	75 0a                	jne    14000126a <__tmainCRTStartup+0x1dc>
   140001260:	b9 ff ff ff ff       	mov    ecx,0xffffffff
   140001265:	e8 16 1f 00 00       	call   140003180 <_configthreadlocale>
   14000126a:	48 8b 15 0f 42 00 00 	mov    rdx,QWORD PTR [rip+0x420f]        # 140005480 <.refptr.__xi_z>
   140001271:	48 8b 05 f8 41 00 00 	mov    rax,QWORD PTR [rip+0x41f8]        # 140005470 <.refptr.__xi_a>
   140001278:	48 89 c1             	mov    rcx,rax
   14000127b:	e8 30 1e 00 00       	call   1400030b0 <_initterm_e>
   140001280:	85 c0                	test   eax,eax
   140001282:	74 0a                	je     14000128e <__tmainCRTStartup+0x200>
   140001284:	b9 0a 00 00 00       	mov    ecx,0xa
   140001289:	e8 6a 1f 00 00       	call   1400031f8 <_amsg_exit>
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
   1400012cb:	e8 08 1f 00 00       	call   1400031d8 <__getmainargs>
   1400012d0:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012d3:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012d7:	79 0a                	jns    1400012e3 <__tmainCRTStartup+0x255>
   1400012d9:	b9 08 00 00 00       	mov    ecx,0x8
   1400012de:	e8 15 1f 00 00       	call   1400031f8 <_amsg_exit>
   1400012e3:	8b 05 1b 7d 00 00    	mov    eax,DWORD PTR [rip+0x7d1b]        # 140009004 <argc>
   1400012e9:	48 8d 15 18 7d 00 00 	lea    rdx,[rip+0x7d18]        # 140009008 <argv>
   1400012f0:	89 c1                	mov    ecx,eax
   1400012f2:	e8 f9 01 00 00       	call   1400014f0 <duplicate_ppstrings>
   1400012f7:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012fa:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012fe:	74 0a                	je     14000130a <__tmainCRTStartup+0x27c>
   140001300:	b9 08 00 00 00       	mov    ecx,0x8
   140001305:	e8 ee 1e 00 00       	call   1400031f8 <_amsg_exit>
   14000130a:	48 8b 15 4f 41 00 00 	mov    rdx,QWORD PTR [rip+0x414f]        # 140005460 <.refptr.__xc_z>
   140001311:	48 8b 05 38 41 00 00 	mov    rax,QWORD PTR [rip+0x4138]        # 140005450 <.refptr.__xc_a>
   140001318:	48 89 c1             	mov    rcx,rax
   14000131b:	e8 e8 1e 00 00       	call   140003208 <_initterm>
   140001320:	e8 22 05 00 00       	call   140001847 <__main>
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
   14000138d:	e8 9e 1d 00 00       	call   140003130 <__p___initenv>
   140001392:	48 8b 15 77 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c77]        # 140009010 <envp>
   140001399:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000139c:	48 8b 0d 6d 7c 00 00 	mov    rcx,QWORD PTR [rip+0x7c6d]        # 140009010 <envp>
   1400013a3:	48 8b 15 5e 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c5e]        # 140009008 <argv>
   1400013aa:	8b 05 54 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c54]        # 140009004 <argc>
   1400013b0:	49 89 c8             	mov    r8,rcx
   1400013b3:	89 c1                	mov    ecx,eax
   1400013b5:	e8 e6 1f 00 00       	call   1400033a0 <main>
   1400013ba:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400013bd:	8b 05 55 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c55]        # 140009018 <managedapp>
   1400013c3:	85 c0                	test   eax,eax
   1400013c5:	75 0a                	jne    1400013d1 <__tmainCRTStartup+0x343>
   1400013c7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013ca:	89 c1                	mov    ecx,eax
   1400013cc:	e8 57 1e 00 00       	call   140003228 <exit>
   1400013d1:	8b 05 45 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c45]        # 14000901c <has_cctor>
   1400013d7:	85 c0                	test   eax,eax
   1400013d9:	75 05                	jne    1400013e0 <__tmainCRTStartup+0x352>
   1400013db:	e8 20 1e 00 00       	call   140003200 <_cexit>
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
   140001511:	e8 32 1d 00 00       	call   140003248 <malloc>
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
   14000155c:	e8 0f 1d 00 00       	call   140003270 <strlen>
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
   140001585:	e8 be 1c 00 00       	call   140003248 <malloc>
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
   1400015e8:	e8 63 1c 00 00       	call   140003250 <memcpy>
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
   140001642:	e8 c9 1b 00 00       	call   140003210 <_crt_atexit>
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
   140001682:	ff 15 e0 8b 00 00    	call   QWORD PTR [rip+0x8be0]        # 14000a268 <__imp_GetModuleHandleA>
   140001688:	48 89 c3             	mov    rbx,rax
   14000168b:	48 85 c0             	test   rax,rax
   14000168e:	74 70                	je     140001700 <__gcc_register_frame+0x90>
   140001690:	48 8d 0d 69 39 00 00 	lea    rcx,[rip+0x3969]        # 140005000 <.rdata>
   140001697:	ff 15 eb 8b 00 00    	call   QWORD PTR [rip+0x8beb]        # 14000a288 <__imp_LoadLibraryA>
   14000169d:	4c 8b 0d cc 8b 00 00 	mov    r9,QWORD PTR [rip+0x8bcc]        # 14000a270 <__imp_GetProcAddress>
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
   14000174e:	48 ff 25 03 8b 00 00 	rex.W jmp QWORD PTR [rip+0x8b03]        # 14000a258 <__imp_FreeLibrary>
   140001755:	0f 1f 00             	nop    DWORD PTR [rax]
   140001758:	48 83 c4 20          	add    rsp,0x20
   14000175c:	5d                   	pop    rbp
   14000175d:	c3                   	ret
   14000175e:	90                   	nop
   14000175f:	90                   	nop

0000000140001760 <__gxx_personality_seh0>:
   140001760:	ff 25 d2 8a 00 00    	jmp    QWORD PTR [rip+0x8ad2]        # 14000a238 <__imp___gxx_personality_seh0>
   140001766:	90                   	nop
   140001767:	90                   	nop

0000000140001768 <operator new(unsigned long long)>:
   140001768:	ff 25 c2 8a 00 00    	jmp    QWORD PTR [rip+0x8ac2]        # 14000a230 <__imp__Znwy>
   14000176e:	90                   	nop
   14000176f:	90                   	nop

0000000140001770 <operator delete(void*, unsigned long long)>:
   140001770:	ff 25 b2 8a 00 00    	jmp    QWORD PTR [rip+0x8ab2]        # 14000a228 <__imp__ZdlPvy>
   140001776:	90                   	nop
   140001777:	90                   	nop

0000000140001778 <std::__throw_bad_array_new_length()>:
   140001778:	ff 25 a2 8a 00 00    	jmp    QWORD PTR [rip+0x8aa2]        # 14000a220 <__imp__ZSt28__throw_bad_array_new_lengthv>
   14000177e:	90                   	nop
   14000177f:	90                   	nop

0000000140001780 <std::__throw_bad_alloc()>:
   140001780:	ff 25 92 8a 00 00    	jmp    QWORD PTR [rip+0x8a92]        # 14000a218 <__imp__ZSt17__throw_bad_allocv>
   140001786:	90                   	nop
   140001787:	90                   	nop

0000000140001788 <std::__detail::_Prime_rehash_policy::_M_need_rehash(unsigned long long, unsigned long long, unsigned long long) const>:
   140001788:	ff 25 82 8a 00 00    	jmp    QWORD PTR [rip+0x8a82]        # 14000a210 <__imp__ZNKSt8__detail20_Prime_rehash_policy14_M_need_rehashEyyy>
   14000178e:	90                   	nop
   14000178f:	90                   	nop

0000000140001790 <__do_global_dtors>:
   140001790:	55                   	push   rbp
   140001791:	48 89 e5             	mov    rbp,rsp
   140001794:	48 83 ec 20          	sub    rsp,0x20
   140001798:	eb 1e                	jmp    1400017b8 <__do_global_dtors+0x28>
   14000179a:	48 8b 05 6f 28 00 00 	mov    rax,QWORD PTR [rip+0x286f]        # 140004010 <p.0>
   1400017a1:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017a4:	ff d0                	call   rax
   1400017a6:	48 8b 05 63 28 00 00 	mov    rax,QWORD PTR [rip+0x2863]        # 140004010 <p.0>
   1400017ad:	48 83 c0 08          	add    rax,0x8
   1400017b1:	48 89 05 58 28 00 00 	mov    QWORD PTR [rip+0x2858],rax        # 140004010 <p.0>
   1400017b8:	48 8b 05 51 28 00 00 	mov    rax,QWORD PTR [rip+0x2851]        # 140004010 <p.0>
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
   1400017d7:	48 8b 05 72 3b 00 00 	mov    rax,QWORD PTR [rip+0x3b72]        # 140005350 <.refptr.__CTOR_LIST__>
   1400017de:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017e1:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400017e4:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
   1400017e8:	75 25                	jne    14000180f <__do_global_ctors+0x40>
   1400017ea:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400017f1:	eb 04                	jmp    1400017f7 <__do_global_ctors+0x28>
   1400017f3:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   1400017f7:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400017fa:	8d 50 01             	lea    edx,[rax+0x1]
   1400017fd:	48 8b 05 4c 3b 00 00 	mov    rax,QWORD PTR [rip+0x3b4c]        # 140005350 <.refptr.__CTOR_LIST__>
   140001804:	89 d2                	mov    edx,edx
   140001806:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   14000180a:	48 85 c0             	test   rax,rax
   14000180d:	75 e4                	jne    1400017f3 <__do_global_ctors+0x24>
   14000180f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001812:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140001815:	eb 14                	jmp    14000182b <__do_global_ctors+0x5c>
   140001817:	48 8b 05 32 3b 00 00 	mov    rax,QWORD PTR [rip+0x3b32]        # 140005350 <.refptr.__CTOR_LIST__>
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
   14000184f:	8b 05 2b 78 00 00    	mov    eax,DWORD PTR [rip+0x782b]        # 140009080 <initialized>
   140001855:	85 c0                	test   eax,eax
   140001857:	75 0f                	jne    140001868 <__main+0x21>
   140001859:	c7 05 1d 78 00 00 01 	mov    DWORD PTR [rip+0x781d],0x1        # 140009080 <initialized>
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
   140001893:	48 8b 05 96 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a96]        # 140005330 <.refptr._CRT_MT>
   14000189a:	8b 00                	mov    eax,DWORD PTR [rax]
   14000189c:	83 f8 02             	cmp    eax,0x2
   14000189f:	74 0d                	je     1400018ae <__dyn_tls_init+0x2e>
   1400018a1:	48 8b 05 88 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a88]        # 140005330 <.refptr._CRT_MT>
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
   1400018d2:	48 8d 05 bf 3d 00 00 	lea    rax,[rip+0x3dbf]        # 140005698 <___crt_xd_start__>
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
   140001906:	48 8d 05 93 3d 00 00 	lea    rax,[rip+0x3d93]        # 1400056a0 <__xd_z>
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
   1400019d9:	48 8d 05 c0 36 00 00 	lea    rax,[rip+0x36c0]        # 1400050a0 <.rdata>
   1400019e0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019e4:	eb 4d                	jmp    140001a33 <_matherr+0xb3>
   1400019e6:	48 8d 05 d2 36 00 00 	lea    rax,[rip+0x36d2]        # 1400050bf <.rdata+0x1f>
   1400019ed:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019f1:	eb 40                	jmp    140001a33 <_matherr+0xb3>
   1400019f3:	48 8d 05 e6 36 00 00 	lea    rax,[rip+0x36e6]        # 1400050e0 <.rdata+0x40>
   1400019fa:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019fe:	eb 33                	jmp    140001a33 <_matherr+0xb3>
   140001a00:	48 8d 05 f9 36 00 00 	lea    rax,[rip+0x36f9]        # 140005100 <.rdata+0x60>
   140001a07:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a0b:	eb 26                	jmp    140001a33 <_matherr+0xb3>
   140001a0d:	48 8d 05 14 37 00 00 	lea    rax,[rip+0x3714]        # 140005128 <.rdata+0x88>
   140001a14:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a18:	eb 19                	jmp    140001a33 <_matherr+0xb3>
   140001a1a:	48 8d 05 2f 37 00 00 	lea    rax,[rip+0x372f]        # 140005150 <.rdata+0xb0>
   140001a21:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a25:	eb 0c                	jmp    140001a33 <_matherr+0xb3>
   140001a27:	48 8d 05 58 37 00 00 	lea    rax,[rip+0x3758]        # 140005186 <.rdata+0xe6>
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
   140001a5c:	e8 3f 17 00 00       	call   1400031a0 <__acrt_iob_func>
   140001a61:	48 89 c1             	mov    rcx,rax
   140001a64:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140001a68:	48 8d 05 29 37 00 00 	lea    rax,[rip+0x3729]        # 140005198 <.rdata+0xf8>
   140001a6f:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001a76:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001a7c:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001a82:	49 89 d9             	mov    r9,rbx
   140001a85:	49 89 d0             	mov    r8,rdx
   140001a88:	48 89 c2             	mov    rdx,rax
   140001a8b:	e8 a8 17 00 00       	call   140003238 <fprintf>
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
   140001ad8:	e8 c3 16 00 00       	call   1400031a0 <__acrt_iob_func>
   140001add:	48 89 c1             	mov    rcx,rax
   140001ae0:	48 8d 05 e9 36 00 00 	lea    rax,[rip+0x36e9]        # 1400051d0 <.rdata>
   140001ae7:	48 89 c2             	mov    rdx,rax
   140001aea:	e8 49 17 00 00       	call   140003238 <fprintf>
   140001aef:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   140001af3:	b9 02 00 00 00       	mov    ecx,0x2
   140001af8:	e8 a3 16 00 00       	call   1400031a0 <__acrt_iob_func>
   140001afd:	48 89 c1             	mov    rcx,rax
   140001b00:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001b04:	49 89 d8             	mov    r8,rbx
   140001b07:	48 89 c2             	mov    rdx,rax
   140001b0a:	e8 71 17 00 00       	call   140003280 <vfprintf>
   140001b0f:	e8 04 17 00 00       	call   140003218 <abort>
   140001b14:	90                   	nop

0000000140001b15 <mark_section_writable>:
   140001b15:	55                   	push   rbp
   140001b16:	48 89 e5             	mov    rbp,rsp
   140001b19:	48 83 ec 60          	sub    rsp,0x60
   140001b1d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001b21:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001b28:	e9 82 00 00 00       	jmp    140001baf <mark_section_writable+0x9a>
   140001b2d:	48 8b 0d ac 75 00 00 	mov    rcx,QWORD PTR [rip+0x75ac]        # 1400090e0 <the_secs>
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
   140001b55:	48 8b 0d 84 75 00 00 	mov    rcx,QWORD PTR [rip+0x7584]        # 1400090e0 <the_secs>
   140001b5c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b5f:	48 63 d0             	movsxd rdx,eax
   140001b62:	48 89 d0             	mov    rax,rdx
   140001b65:	48 c1 e0 02          	shl    rax,0x2
   140001b69:	48 01 d0             	add    rax,rdx
   140001b6c:	48 c1 e0 03          	shl    rax,0x3
   140001b70:	48 01 c8             	add    rax,rcx
   140001b73:	48 8b 48 18          	mov    rcx,QWORD PTR [rax+0x18]
   140001b77:	4c 8b 05 62 75 00 00 	mov    r8,QWORD PTR [rip+0x7562]        # 1400090e0 <the_secs>
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
   140001baf:	8b 05 33 75 00 00    	mov    eax,DWORD PTR [rip+0x7533]        # 1400090e8 <maxSections>
   140001bb5:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001bb8:	0f 8c 6f ff ff ff    	jl     140001b2d <mark_section_writable+0x18>
   140001bbe:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001bc2:	48 89 c1             	mov    rcx,rax
   140001bc5:	e8 c1 11 00 00       	call   140002d8b <__mingw_GetSectionForAddress>
   140001bca:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001bce:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001bd3:	75 13                	jne    140001be8 <mark_section_writable+0xd3>
   140001bd5:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001bd9:	48 8d 0d 10 36 00 00 	lea    rcx,[rip+0x3610]        # 1400051f0 <.rdata+0x20>
   140001be0:	48 89 c2             	mov    rdx,rax
   140001be3:	e8 c8 fe ff ff       	call   140001ab0 <__report_error>
   140001be8:	48 8b 0d f1 74 00 00 	mov    rcx,QWORD PTR [rip+0x74f1]        # 1400090e0 <the_secs>
   140001bef:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001bf2:	48 63 d0             	movsxd rdx,eax
   140001bf5:	48 89 d0             	mov    rax,rdx
   140001bf8:	48 c1 e0 02          	shl    rax,0x2
   140001bfc:	48 01 d0             	add    rax,rdx
   140001bff:	48 c1 e0 03          	shl    rax,0x3
   140001c03:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001c07:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c0b:	48 89 42 20          	mov    QWORD PTR [rdx+0x20],rax
   140001c0f:	48 8b 0d ca 74 00 00 	mov    rcx,QWORD PTR [rip+0x74ca]        # 1400090e0 <the_secs>
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
   140001c45:	4c 8b 05 94 74 00 00 	mov    r8,QWORD PTR [rip+0x7494]        # 1400090e0 <the_secs>
   140001c4c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c4f:	48 63 d0             	movsxd rdx,eax
   140001c52:	48 89 d0             	mov    rax,rdx
   140001c55:	48 c1 e0 02          	shl    rax,0x2
   140001c59:	48 01 d0             	add    rax,rdx
   140001c5c:	48 c1 e0 03          	shl    rax,0x3
   140001c60:	4c 01 c0             	add    rax,r8
   140001c63:	4a 8d 14 09          	lea    rdx,[rcx+r9*1]
   140001c67:	48 89 50 18          	mov    QWORD PTR [rax+0x18],rdx
   140001c6b:	48 8b 0d 6e 74 00 00 	mov    rcx,QWORD PTR [rip+0x746e]        # 1400090e0 <the_secs>
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
   140001c9a:	48 8b 05 0f 86 00 00 	mov    rax,QWORD PTR [rip+0x860f]        # 14000a2b0 <__imp_VirtualQuery>
   140001ca1:	ff d0                	call   rax
   140001ca3:	48 85 c0             	test   rax,rax
   140001ca6:	75 3f                	jne    140001ce7 <mark_section_writable+0x1d2>
   140001ca8:	48 8b 0d 31 74 00 00 	mov    rcx,QWORD PTR [rip+0x7431]        # 1400090e0 <the_secs>
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
   140001cd3:	48 8d 05 36 35 00 00 	lea    rax,[rip+0x3536]        # 140005210 <.rdata+0x40>
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
   140001d31:	48 8b 0d a8 73 00 00 	mov    rcx,QWORD PTR [rip+0x73a8]        # 1400090e0 <the_secs>
   140001d38:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d3b:	48 63 d0             	movsxd rdx,eax
   140001d3e:	48 89 d0             	mov    rax,rdx
   140001d41:	48 c1 e0 02          	shl    rax,0x2
   140001d45:	48 01 d0             	add    rax,rdx
   140001d48:	48 c1 e0 03          	shl    rax,0x3
   140001d4c:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d50:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001d54:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   140001d58:	48 8b 0d 81 73 00 00 	mov    rcx,QWORD PTR [rip+0x7381]        # 1400090e0 <the_secs>
   140001d5f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d62:	48 63 d0             	movsxd rdx,eax
   140001d65:	48 89 d0             	mov    rax,rdx
   140001d68:	48 c1 e0 02          	shl    rax,0x2
   140001d6c:	48 01 d0             	add    rax,rdx
   140001d6f:	48 c1 e0 03          	shl    rax,0x3
   140001d73:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d77:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140001d7b:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   140001d7f:	48 8b 0d 5a 73 00 00 	mov    rcx,QWORD PTR [rip+0x735a]        # 1400090e0 <the_secs>
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
   140001db4:	48 8b 05 ed 84 00 00 	mov    rax,QWORD PTR [rip+0x84ed]        # 14000a2a8 <__imp_VirtualProtect>
   140001dbb:	ff d0                	call   rax
   140001dbd:	85 c0                	test   eax,eax
   140001dbf:	75 1a                	jne    140001ddb <mark_section_writable+0x2c6>
   140001dc1:	48 8b 05 98 84 00 00 	mov    rax,QWORD PTR [rip+0x8498]        # 14000a260 <__imp_GetLastError>
   140001dc8:	ff d0                	call   rax
   140001dca:	89 c2                	mov    edx,eax
   140001dcc:	48 8d 05 75 34 00 00 	lea    rax,[rip+0x3475]        # 140005248 <.rdata+0x78>
   140001dd3:	48 89 c1             	mov    rcx,rax
   140001dd6:	e8 d5 fc ff ff       	call   140001ab0 <__report_error>
   140001ddb:	8b 05 07 73 00 00    	mov    eax,DWORD PTR [rip+0x7307]        # 1400090e8 <maxSections>
   140001de1:	83 c0 01             	add    eax,0x1
   140001de4:	89 05 fe 72 00 00    	mov    DWORD PTR [rip+0x72fe],eax        # 1400090e8 <maxSections>
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
   140001e07:	48 8b 0d d2 72 00 00 	mov    rcx,QWORD PTR [rip+0x72d2]        # 1400090e0 <the_secs>
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
   140001e2f:	48 8b 0d aa 72 00 00 	mov    rcx,QWORD PTR [rip+0x72aa]        # 1400090e0 <the_secs>
   140001e36:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e39:	48 63 d0             	movsxd rdx,eax
   140001e3c:	48 89 d0             	mov    rax,rdx
   140001e3f:	48 c1 e0 02          	shl    rax,0x2
   140001e43:	48 01 d0             	add    rax,rdx
   140001e46:	48 c1 e0 03          	shl    rax,0x3
   140001e4a:	48 01 c8             	add    rax,rcx
   140001e4d:	44 8b 10             	mov    r10d,DWORD PTR [rax]
   140001e50:	48 8b 0d 89 72 00 00 	mov    rcx,QWORD PTR [rip+0x7289]        # 1400090e0 <the_secs>
   140001e57:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e5a:	48 63 d0             	movsxd rdx,eax
   140001e5d:	48 89 d0             	mov    rax,rdx
   140001e60:	48 c1 e0 02          	shl    rax,0x2
   140001e64:	48 01 d0             	add    rax,rdx
   140001e67:	48 c1 e0 03          	shl    rax,0x3
   140001e6b:	48 01 c8             	add    rax,rcx
   140001e6e:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   140001e72:	4c 8b 05 67 72 00 00 	mov    r8,QWORD PTR [rip+0x7267]        # 1400090e0 <the_secs>
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
   140001ea4:	48 8b 05 fd 83 00 00 	mov    rax,QWORD PTR [rip+0x83fd]        # 14000a2a8 <__imp_VirtualProtect>
   140001eab:	ff d0                	call   rax
   140001ead:	eb 01                	jmp    140001eb0 <restore_modified_sections+0xbd>
   140001eaf:	90                   	nop
   140001eb0:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001eb4:	8b 05 2e 72 00 00    	mov    eax,DWORD PTR [rip+0x722e]        # 1400090e8 <maxSections>
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
   140001f04:	e8 47 13 00 00       	call   140003250 <memcpy>
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
   140001ff4:	48 8d 05 75 32 00 00 	lea    rax,[rip+0x3275]        # 140005270 <.rdata+0xa0>
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
   14000212e:	48 8d 0d 73 31 00 00 	lea    rcx,[rip+0x3173]        # 1400052a8 <.rdata+0xd8>
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
   1400021d8:	48 8d 0d f9 30 00 00 	lea    rcx,[rip+0x30f9]        # 1400052d8 <.rdata+0x108>
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
   140002298:	8b 05 4e 6e 00 00    	mov    eax,DWORD PTR [rip+0x6e4e]        # 1400090ec <was_init.0>
   14000229e:	85 c0                	test   eax,eax
   1400022a0:	0f 85 88 00 00 00    	jne    14000232e <_pei386_runtime_relocator+0x9e>
   1400022a6:	8b 05 40 6e 00 00    	mov    eax,DWORD PTR [rip+0x6e40]        # 1400090ec <was_init.0>
   1400022ac:	83 c0 01             	add    eax,0x1
   1400022af:	89 05 37 6e 00 00    	mov    DWORD PTR [rip+0x6e37],eax        # 1400090ec <was_init.0>
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
   1400022dd:	e8 8e 0d 00 00       	call   140003070 <___chkstk_ms>
   1400022e2:	48 29 c4             	sub    rsp,rax
   1400022e5:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   1400022ea:	48 83 c0 0f          	add    rax,0xf
   1400022ee:	48 c1 e8 04          	shr    rax,0x4
   1400022f2:	48 c1 e0 04          	shl    rax,0x4
   1400022f6:	48 89 05 e3 6d 00 00 	mov    QWORD PTR [rip+0x6de3],rax        # 1400090e0 <the_secs>
   1400022fd:	c7 05 e1 6d 00 00 00 	mov    DWORD PTR [rip+0x6de1],0x0        # 1400090e8 <maxSections>
   140002304:	00 00 00 
   140002307:	48 8b 0d 52 30 00 00 	mov    rcx,QWORD PTR [rip+0x3052]        # 140005360 <.refptr.__ImageBase>
   14000230e:	48 8b 15 5b 30 00 00 	mov    rdx,QWORD PTR [rip+0x305b]        # 140005370 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   140002315:	48 8b 05 64 30 00 00 	mov    rax,QWORD PTR [rip+0x3064]        # 140005380 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
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
   140002359:	48 8b 05 90 6d 00 00 	mov    rax,QWORD PTR [rip+0x6d90]        # 1400090f0 <stUserMathErr>
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
   140002391:	48 8b 15 58 6d 00 00 	mov    rdx,QWORD PTR [rip+0x6d58]        # 1400090f0 <stUserMathErr>
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
   1400023ba:	48 89 05 2f 6d 00 00 	mov    QWORD PTR [rip+0x6d2f],rax        # 1400090f0 <stUserMathErr>
   1400023c1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023c5:	48 89 c1             	mov    rcx,rax
   1400023c8:	e8 23 0e 00 00       	call   1400031f0 <__setusermatherr>
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
   14000251e:	e8 45 0d 00 00       	call   140003268 <signal>
   140002523:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002527:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000252c:	75 1b                	jne    140002549 <__mingw_SEH_error_handler+0x169>
   14000252e:	ba 01 00 00 00       	mov    edx,0x1
   140002533:	b9 0b 00 00 00       	mov    ecx,0xb
   140002538:	e8 2b 0d 00 00       	call   140003268 <signal>
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
   140002575:	e8 ee 0c 00 00       	call   140003268 <signal>
   14000257a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000257e:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002583:	75 1b                	jne    1400025a0 <__mingw_SEH_error_handler+0x1c0>
   140002585:	ba 01 00 00 00       	mov    edx,0x1
   14000258a:	b9 04 00 00 00       	mov    ecx,0x4
   14000258f:	e8 d4 0c 00 00       	call   140003268 <signal>
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
   1400025d0:	e8 93 0c 00 00       	call   140003268 <signal>
   1400025d5:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400025d9:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400025de:	75 23                	jne    140002603 <__mingw_SEH_error_handler+0x223>
   1400025e0:	ba 01 00 00 00       	mov    edx,0x1
   1400025e5:	b9 08 00 00 00       	mov    ecx,0x8
   1400025ea:	e8 79 0c 00 00       	call   140003268 <signal>
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
   14000275d:	e8 06 0b 00 00       	call   140003268 <signal>
   140002762:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002766:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000276b:	75 1b                	jne    140002788 <_gnu_exception_handler+0x14e>
   14000276d:	ba 01 00 00 00       	mov    edx,0x1
   140002772:	b9 0b 00 00 00       	mov    ecx,0xb
   140002777:	e8 ec 0a 00 00       	call   140003268 <signal>
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
   1400027b4:	e8 af 0a 00 00       	call   140003268 <signal>
   1400027b9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400027bd:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400027c2:	75 1b                	jne    1400027df <_gnu_exception_handler+0x1a5>
   1400027c4:	ba 01 00 00 00       	mov    edx,0x1
   1400027c9:	b9 04 00 00 00       	mov    ecx,0x4
   1400027ce:	e8 95 0a 00 00       	call   140003268 <signal>
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
   14000280f:	e8 54 0a 00 00       	call   140003268 <signal>
   140002814:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002818:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000281d:	75 23                	jne    140002842 <_gnu_exception_handler+0x208>
   14000281f:	ba 01 00 00 00       	mov    edx,0x1
   140002824:	b9 08 00 00 00       	mov    ecx,0x8
   140002829:	e8 3a 0a 00 00       	call   140003268 <signal>
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
   140002876:	48 8b 05 93 68 00 00 	mov    rax,QWORD PTR [rip+0x6893]        # 140009110 <__mingw_oldexcpt_handler>
   14000287d:	48 85 c0             	test   rax,rax
   140002880:	74 13                	je     140002895 <_gnu_exception_handler+0x25b>
   140002882:	48 8b 15 87 68 00 00 	mov    rdx,QWORD PTR [rip+0x6887]        # 140009110 <__mingw_oldexcpt_handler>
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
   1400028af:	8b 05 93 68 00 00    	mov    eax,DWORD PTR [rip+0x6893]        # 140009148 <__mingwthr_cs_init>
   1400028b5:	85 c0                	test   eax,eax
   1400028b7:	75 07                	jne    1400028c0 <___w64_mingwthr_add_key_dtor+0x20>
   1400028b9:	b8 00 00 00 00       	mov    eax,0x0
   1400028be:	eb 7b                	jmp    14000293b <___w64_mingwthr_add_key_dtor+0x9b>
   1400028c0:	ba 18 00 00 00       	mov    edx,0x18
   1400028c5:	b9 01 00 00 00       	mov    ecx,0x1
   1400028ca:	e8 51 09 00 00       	call   140003220 <calloc>
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
   1400028f6:	48 8d 05 23 68 00 00 	lea    rax,[rip+0x6823]        # 140009120 <__mingwthr_cs>
   1400028fd:	48 89 c1             	mov    rcx,rax
   140002900:	48 8b 05 49 79 00 00 	mov    rax,QWORD PTR [rip+0x7949]        # 14000a250 <__imp_EnterCriticalSection>
   140002907:	ff d0                	call   rax
   140002909:	48 8b 15 40 68 00 00 	mov    rdx,QWORD PTR [rip+0x6840]        # 140009150 <key_dtor_list>
   140002910:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002914:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002918:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000291c:	48 89 05 2d 68 00 00 	mov    QWORD PTR [rip+0x682d],rax        # 140009150 <key_dtor_list>
   140002923:	48 8d 05 f6 67 00 00 	lea    rax,[rip+0x67f6]        # 140009120 <__mingwthr_cs>
   14000292a:	48 89 c1             	mov    rcx,rax
   14000292d:	48 8b 05 4c 79 00 00 	mov    rax,QWORD PTR [rip+0x794c]        # 14000a280 <__imp_LeaveCriticalSection>
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
   14000294c:	8b 05 f6 67 00 00    	mov    eax,DWORD PTR [rip+0x67f6]        # 140009148 <__mingwthr_cs_init>
   140002952:	85 c0                	test   eax,eax
   140002954:	75 0a                	jne    140002960 <___w64_mingwthr_remove_key_dtor+0x1f>
   140002956:	b8 00 00 00 00       	mov    eax,0x0
   14000295b:	e9 9c 00 00 00       	jmp    1400029fc <___w64_mingwthr_remove_key_dtor+0xbb>
   140002960:	48 8d 05 b9 67 00 00 	lea    rax,[rip+0x67b9]        # 140009120 <__mingwthr_cs>
   140002967:	48 89 c1             	mov    rcx,rax
   14000296a:	48 8b 05 df 78 00 00 	mov    rax,QWORD PTR [rip+0x78df]        # 14000a250 <__imp_EnterCriticalSection>
   140002971:	ff d0                	call   rax
   140002973:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   14000297a:	00 
   14000297b:	48 8b 05 ce 67 00 00 	mov    rax,QWORD PTR [rip+0x67ce]        # 140009150 <key_dtor_list>
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
   1400029a2:	48 89 05 a7 67 00 00 	mov    QWORD PTR [rip+0x67a7],rax        # 140009150 <key_dtor_list>
   1400029a9:	eb 10                	jmp    1400029bb <___w64_mingwthr_remove_key_dtor+0x7a>
   1400029ab:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029af:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   1400029b3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400029b7:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   1400029bb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029bf:	48 89 c1             	mov    rcx,rax
   1400029c2:	e8 79 08 00 00       	call   140003240 <free>
   1400029c7:	eb 1b                	jmp    1400029e4 <___w64_mingwthr_remove_key_dtor+0xa3>
   1400029c9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029cd:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400029d1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029d5:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   1400029d9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400029dd:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400029e2:	75 a4                	jne    140002988 <___w64_mingwthr_remove_key_dtor+0x47>
   1400029e4:	48 8d 05 35 67 00 00 	lea    rax,[rip+0x6735]        # 140009120 <__mingwthr_cs>
   1400029eb:	48 89 c1             	mov    rcx,rax
   1400029ee:	48 8b 05 8b 78 00 00 	mov    rax,QWORD PTR [rip+0x788b]        # 14000a280 <__imp_LeaveCriticalSection>
   1400029f5:	ff d0                	call   rax
   1400029f7:	b8 00 00 00 00       	mov    eax,0x0
   1400029fc:	48 83 c4 30          	add    rsp,0x30
   140002a00:	5d                   	pop    rbp
   140002a01:	c3                   	ret

0000000140002a02 <__mingwthr_run_key_dtors>:
   140002a02:	55                   	push   rbp
   140002a03:	48 89 e5             	mov    rbp,rsp
   140002a06:	48 83 ec 30          	sub    rsp,0x30
   140002a0a:	8b 05 38 67 00 00    	mov    eax,DWORD PTR [rip+0x6738]        # 140009148 <__mingwthr_cs_init>
   140002a10:	85 c0                	test   eax,eax
   140002a12:	0f 84 82 00 00 00    	je     140002a9a <__mingwthr_run_key_dtors+0x98>
   140002a18:	48 8d 05 01 67 00 00 	lea    rax,[rip+0x6701]        # 140009120 <__mingwthr_cs>
   140002a1f:	48 89 c1             	mov    rcx,rax
   140002a22:	48 8b 05 27 78 00 00 	mov    rax,QWORD PTR [rip+0x7827]        # 14000a250 <__imp_EnterCriticalSection>
   140002a29:	ff d0                	call   rax
   140002a2b:	48 8b 05 1e 67 00 00 	mov    rax,QWORD PTR [rip+0x671e]        # 140009150 <key_dtor_list>
   140002a32:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a36:	eb 46                	jmp    140002a7e <__mingwthr_run_key_dtors+0x7c>
   140002a38:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a3c:	8b 00                	mov    eax,DWORD PTR [rax]
   140002a3e:	89 c1                	mov    ecx,eax
   140002a40:	48 8b 05 59 78 00 00 	mov    rax,QWORD PTR [rip+0x7859]        # 14000a2a0 <__imp_TlsGetValue>
   140002a47:	ff d0                	call   rax
   140002a49:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002a4d:	48 8b 05 0c 78 00 00 	mov    rax,QWORD PTR [rip+0x780c]        # 14000a260 <__imp_GetLastError>
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
   140002a85:	48 8d 05 94 66 00 00 	lea    rax,[rip+0x6694]        # 140009120 <__mingwthr_cs>
   140002a8c:	48 89 c1             	mov    rcx,rax
   140002a8f:	48 8b 05 ea 77 00 00 	mov    rax,QWORD PTR [rip+0x77ea]        # 14000a280 <__imp_LeaveCriticalSection>
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
   140002aec:	8b 05 56 66 00 00    	mov    eax,DWORD PTR [rip+0x6656]        # 140009148 <__mingwthr_cs_init>
   140002af2:	85 c0                	test   eax,eax
   140002af4:	75 13                	jne    140002b09 <__mingw_TLScallback+0x68>
   140002af6:	48 8d 05 23 66 00 00 	lea    rax,[rip+0x6623]        # 140009120 <__mingwthr_cs>
   140002afd:	48 89 c1             	mov    rcx,rax
   140002b00:	48 8b 05 71 77 00 00 	mov    rax,QWORD PTR [rip+0x7771]        # 14000a278 <__imp_InitializeCriticalSection>
   140002b07:	ff d0                	call   rax
   140002b09:	c7 05 35 66 00 00 01 	mov    DWORD PTR [rip+0x6635],0x1        # 140009148 <__mingwthr_cs_init>
   140002b10:	00 00 00 
   140002b13:	eb 7d                	jmp    140002b92 <__mingw_TLScallback+0xf1>
   140002b15:	e8 e8 fe ff ff       	call   140002a02 <__mingwthr_run_key_dtors>
   140002b1a:	8b 05 28 66 00 00    	mov    eax,DWORD PTR [rip+0x6628]        # 140009148 <__mingwthr_cs_init>
   140002b20:	83 f8 01             	cmp    eax,0x1
   140002b23:	75 6c                	jne    140002b91 <__mingw_TLScallback+0xf0>
   140002b25:	48 8b 05 24 66 00 00 	mov    rax,QWORD PTR [rip+0x6624]        # 140009150 <key_dtor_list>
   140002b2c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b30:	eb 20                	jmp    140002b52 <__mingw_TLScallback+0xb1>
   140002b32:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b36:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002b3a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b3e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b42:	48 89 c1             	mov    rcx,rax
   140002b45:	e8 f6 06 00 00       	call   140003240 <free>
   140002b4a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b4e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b52:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002b57:	75 d9                	jne    140002b32 <__mingw_TLScallback+0x91>
   140002b59:	48 c7 05 ec 65 00 00 	mov    QWORD PTR [rip+0x65ec],0x0        # 140009150 <key_dtor_list>
   140002b60:	00 00 00 00 
   140002b64:	c7 05 da 65 00 00 00 	mov    DWORD PTR [rip+0x65da],0x0        # 140009148 <__mingwthr_cs_init>
   140002b6b:	00 00 00 
   140002b6e:	48 8d 05 ab 65 00 00 	lea    rax,[rip+0x65ab]        # 140009120 <__mingwthr_cs>
   140002b75:	48 89 c1             	mov    rcx,rax
   140002b78:	48 8b 05 c9 76 00 00 	mov    rax,QWORD PTR [rip+0x76c9]        # 14000a248 <__imp_DeleteCriticalSection>
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
   140002cd8:	e8 93 05 00 00       	call   140003270 <strlen>
   140002cdd:	48 83 f8 08          	cmp    rax,0x8
   140002ce1:	76 0a                	jbe    140002ced <_FindPESectionByName+0x28>
   140002ce3:	b8 00 00 00 00       	mov    eax,0x0
   140002ce8:	e9 98 00 00 00       	jmp    140002d85 <_FindPESectionByName+0xc0>
   140002ced:	48 8b 05 6c 26 00 00 	mov    rax,QWORD PTR [rip+0x266c]        # 140005360 <.refptr.__ImageBase>
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
   140002d58:	e8 1b 05 00 00       	call   140003278 <strncmp>
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
   140002d97:	48 8b 05 c2 25 00 00 	mov    rax,QWORD PTR [rip+0x25c2]        # 140005360 <.refptr.__ImageBase>
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
   140002de3:	48 8b 05 76 25 00 00 	mov    rax,QWORD PTR [rip+0x2576]        # 140005360 <.refptr.__ImageBase>
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
   140002e37:	48 8b 05 22 25 00 00 	mov    rax,QWORD PTR [rip+0x2522]        # 140005360 <.refptr.__ImageBase>
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
   140002edf:	48 8b 05 7a 24 00 00 	mov    rax,QWORD PTR [rip+0x247a]        # 140005360 <.refptr.__ImageBase>
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
   140002f17:	48 8b 05 42 24 00 00 	mov    rax,QWORD PTR [rip+0x2442]        # 140005360 <.refptr.__ImageBase>
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
   140002f87:	48 8b 05 d2 23 00 00 	mov    rax,QWORD PTR [rip+0x23d2]        # 140005360 <.refptr.__ImageBase>
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

0000000140003060 <_Unwind_Resume>:
   140003060:	ff 25 9a 71 00 00    	jmp    QWORD PTR [rip+0x719a]        # 14000a200 <__IAT_start__>
   140003066:	90                   	nop
   140003067:	90                   	nop
   140003068:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000306f:	00 

0000000140003070 <___chkstk_ms>:
   140003070:	51                   	push   rcx
   140003071:	50                   	push   rax
   140003072:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003078:	48 8d 4c 24 18       	lea    rcx,[rsp+0x18]
   14000307d:	72 19                	jb     140003098 <___chkstk_ms+0x28>
   14000307f:	48 81 e9 00 10 00 00 	sub    rcx,0x1000
   140003086:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   14000308a:	48 2d 00 10 00 00    	sub    rax,0x1000
   140003090:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003096:	77 e7                	ja     14000307f <___chkstk_ms+0xf>
   140003098:	48 29 c1             	sub    rcx,rax
   14000309b:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   14000309f:	58                   	pop    rax
   1400030a0:	59                   	pop    rcx
   1400030a1:	c3                   	ret
   1400030a2:	90                   	nop
   1400030a3:	90                   	nop
   1400030a4:	90                   	nop
   1400030a5:	90                   	nop
   1400030a6:	90                   	nop
   1400030a7:	90                   	nop
   1400030a8:	90                   	nop
   1400030a9:	90                   	nop
   1400030aa:	90                   	nop
   1400030ab:	90                   	nop
   1400030ac:	90                   	nop
   1400030ad:	90                   	nop
   1400030ae:	90                   	nop
   1400030af:	90                   	nop

00000001400030b0 <_initterm_e>:
   1400030b0:	55                   	push   rbp
   1400030b1:	48 89 e5             	mov    rbp,rsp
   1400030b4:	48 83 ec 30          	sub    rsp,0x30
   1400030b8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400030bc:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400030c0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400030c4:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400030c8:	eb 29                	jmp    1400030f3 <_initterm_e+0x43>
   1400030ca:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030ce:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400030d1:	48 85 c0             	test   rax,rax
   1400030d4:	74 17                	je     1400030ed <_initterm_e+0x3d>
   1400030d6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030da:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400030dd:	ff d0                	call   rax
   1400030df:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   1400030e2:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   1400030e6:	74 06                	je     1400030ee <_initterm_e+0x3e>
   1400030e8:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   1400030eb:	eb 15                	jmp    140003102 <_initterm_e+0x52>
   1400030ed:	90                   	nop
   1400030ee:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   1400030f3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030f7:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   1400030fb:	72 cd                	jb     1400030ca <_initterm_e+0x1a>
   1400030fd:	b8 00 00 00 00       	mov    eax,0x0
   140003102:	48 83 c4 30          	add    rsp,0x30
   140003106:	5d                   	pop    rbp
   140003107:	c3                   	ret
   140003108:	90                   	nop
   140003109:	90                   	nop
   14000310a:	90                   	nop
   14000310b:	90                   	nop
   14000310c:	90                   	nop
   14000310d:	90                   	nop
   14000310e:	90                   	nop
   14000310f:	90                   	nop

0000000140003110 <__p__fmode>:
   140003110:	55                   	push   rbp
   140003111:	48 89 e5             	mov    rbp,rsp
   140003114:	48 8b 05 b5 22 00 00 	mov    rax,QWORD PTR [rip+0x22b5]        # 1400053d0 <.refptr.__imp__fmode>
   14000311b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000311e:	5d                   	pop    rbp
   14000311f:	c3                   	ret

0000000140003120 <__p__commode>:
   140003120:	55                   	push   rbp
   140003121:	48 89 e5             	mov    rbp,rsp
   140003124:	48 8b 05 95 22 00 00 	mov    rax,QWORD PTR [rip+0x2295]        # 1400053c0 <.refptr.__imp__commode>
   14000312b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000312e:	5d                   	pop    rbp
   14000312f:	c3                   	ret

0000000140003130 <__p___initenv>:
   140003130:	55                   	push   rbp
   140003131:	48 89 e5             	mov    rbp,rsp
   140003134:	48 8b 05 75 22 00 00 	mov    rax,QWORD PTR [rip+0x2275]        # 1400053b0 <.refptr.__imp___initenv>
   14000313b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000313e:	5d                   	pop    rbp
   14000313f:	c3                   	ret

0000000140003140 <_set_invalid_parameter_handler>:
   140003140:	55                   	push   rbp
   140003141:	48 89 e5             	mov    rbp,rsp
   140003144:	48 83 ec 10          	sub    rsp,0x10
   140003148:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000314c:	48 8d 05 3d 60 00 00 	lea    rax,[rip+0x603d]        # 140009190 <handler>
   140003153:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003157:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000315b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000315f:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140003163:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003167:	48 87 10             	xchg   QWORD PTR [rax],rdx
   14000316a:	48 89 d0             	mov    rax,rdx
   14000316d:	48 83 c4 10          	add    rsp,0x10
   140003171:	5d                   	pop    rbp
   140003172:	c3                   	ret

0000000140003173 <_get_invalid_parameter_handler>:
   140003173:	55                   	push   rbp
   140003174:	48 89 e5             	mov    rbp,rsp
   140003177:	48 8b 05 12 60 00 00 	mov    rax,QWORD PTR [rip+0x6012]        # 140009190 <handler>
   14000317e:	5d                   	pop    rbp
   14000317f:	c3                   	ret

0000000140003180 <_configthreadlocale>:
   140003180:	55                   	push   rbp
   140003181:	48 89 e5             	mov    rbp,rsp
   140003184:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140003187:	83 7d 10 01          	cmp    DWORD PTR [rbp+0x10],0x1
   14000318b:	75 07                	jne    140003194 <_configthreadlocale+0x14>
   14000318d:	b8 ff ff ff ff       	mov    eax,0xffffffff
   140003192:	eb 05                	jmp    140003199 <_configthreadlocale+0x19>
   140003194:	b8 02 00 00 00       	mov    eax,0x2
   140003199:	5d                   	pop    rbp
   14000319a:	c3                   	ret
   14000319b:	90                   	nop
   14000319c:	90                   	nop
   14000319d:	90                   	nop
   14000319e:	90                   	nop
   14000319f:	90                   	nop

00000001400031a0 <__acrt_iob_func>:
   1400031a0:	55                   	push   rbp
   1400031a1:	48 89 e5             	mov    rbp,rsp
   1400031a4:	48 83 ec 20          	sub    rsp,0x20
   1400031a8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400031ab:	e8 30 00 00 00       	call   1400031e0 <__iob_func>
   1400031b0:	48 89 c1             	mov    rcx,rax
   1400031b3:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   1400031b6:	48 89 d0             	mov    rax,rdx
   1400031b9:	48 01 c0             	add    rax,rax
   1400031bc:	48 01 d0             	add    rax,rdx
   1400031bf:	48 c1 e0 04          	shl    rax,0x4
   1400031c3:	48 01 c8             	add    rax,rcx
   1400031c6:	48 83 c4 20          	add    rsp,0x20
   1400031ca:	5d                   	pop    rbp
   1400031cb:	c3                   	ret
   1400031cc:	90                   	nop
   1400031cd:	90                   	nop
   1400031ce:	90                   	nop
   1400031cf:	90                   	nop

00000001400031d0 <__C_specific_handler>:
   1400031d0:	ff 25 ea 70 00 00    	jmp    QWORD PTR [rip+0x70ea]        # 14000a2c0 <__imp___C_specific_handler>
   1400031d6:	90                   	nop
   1400031d7:	90                   	nop

00000001400031d8 <__getmainargs>:
   1400031d8:	ff 25 ea 70 00 00    	jmp    QWORD PTR [rip+0x70ea]        # 14000a2c8 <__imp___getmainargs>
   1400031de:	90                   	nop
   1400031df:	90                   	nop

00000001400031e0 <__iob_func>:
   1400031e0:	ff 25 f2 70 00 00    	jmp    QWORD PTR [rip+0x70f2]        # 14000a2d8 <__imp___iob_func>
   1400031e6:	90                   	nop
   1400031e7:	90                   	nop

00000001400031e8 <__set_app_type>:
   1400031e8:	ff 25 f2 70 00 00    	jmp    QWORD PTR [rip+0x70f2]        # 14000a2e0 <__imp___set_app_type>
   1400031ee:	90                   	nop
   1400031ef:	90                   	nop

00000001400031f0 <__setusermatherr>:
   1400031f0:	ff 25 f2 70 00 00    	jmp    QWORD PTR [rip+0x70f2]        # 14000a2e8 <__imp___setusermatherr>
   1400031f6:	90                   	nop
   1400031f7:	90                   	nop

00000001400031f8 <_amsg_exit>:
   1400031f8:	ff 25 f2 70 00 00    	jmp    QWORD PTR [rip+0x70f2]        # 14000a2f0 <__imp__amsg_exit>
   1400031fe:	90                   	nop
   1400031ff:	90                   	nop

0000000140003200 <_cexit>:
   140003200:	ff 25 f2 70 00 00    	jmp    QWORD PTR [rip+0x70f2]        # 14000a2f8 <__imp__cexit>
   140003206:	90                   	nop
   140003207:	90                   	nop

0000000140003208 <_initterm>:
   140003208:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a310 <__imp__initterm>
   14000320e:	90                   	nop
   14000320f:	90                   	nop

0000000140003210 <_crt_atexit>:
   140003210:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a318 <__imp__crt_atexit>
   140003216:	90                   	nop
   140003217:	90                   	nop

0000000140003218 <abort>:
   140003218:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a320 <__imp_abort>
   14000321e:	90                   	nop
   14000321f:	90                   	nop

0000000140003220 <calloc>:
   140003220:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a328 <__imp_calloc>
   140003226:	90                   	nop
   140003227:	90                   	nop

0000000140003228 <exit>:
   140003228:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a330 <__imp_exit>
   14000322e:	90                   	nop
   14000322f:	90                   	nop

0000000140003230 <fflush>:
   140003230:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a338 <__imp_fflush>
   140003236:	90                   	nop
   140003237:	90                   	nop

0000000140003238 <fprintf>:
   140003238:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a340 <__imp_fprintf>
   14000323e:	90                   	nop
   14000323f:	90                   	nop

0000000140003240 <free>:
   140003240:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a348 <__imp_free>
   140003246:	90                   	nop
   140003247:	90                   	nop

0000000140003248 <malloc>:
   140003248:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a350 <__imp_malloc>
   14000324e:	90                   	nop
   14000324f:	90                   	nop

0000000140003250 <memcpy>:
   140003250:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a358 <__imp_memcpy>
   140003256:	90                   	nop
   140003257:	90                   	nop

0000000140003258 <memset>:
   140003258:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a360 <__imp_memset>
   14000325e:	90                   	nop
   14000325f:	90                   	nop

0000000140003260 <setvbuf>:
   140003260:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a368 <__imp_setvbuf>
   140003266:	90                   	nop
   140003267:	90                   	nop

0000000140003268 <signal>:
   140003268:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a370 <__imp_signal>
   14000326e:	90                   	nop
   14000326f:	90                   	nop

0000000140003270 <strlen>:
   140003270:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a378 <__imp_strlen>
   140003276:	90                   	nop
   140003277:	90                   	nop

0000000140003278 <strncmp>:
   140003278:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a380 <__imp_strncmp>
   14000327e:	90                   	nop
   14000327f:	90                   	nop

0000000140003280 <vfprintf>:
   140003280:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a388 <__imp_vfprintf>
   140003286:	90                   	nop
   140003287:	90                   	nop
   140003288:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000328f:	00 

0000000140003290 <VirtualQuery>:
   140003290:	ff 25 1a 70 00 00    	jmp    QWORD PTR [rip+0x701a]        # 14000a2b0 <__imp_VirtualQuery>
   140003296:	90                   	nop
   140003297:	90                   	nop

0000000140003298 <VirtualProtect>:
   140003298:	ff 25 0a 70 00 00    	jmp    QWORD PTR [rip+0x700a]        # 14000a2a8 <__imp_VirtualProtect>
   14000329e:	90                   	nop
   14000329f:	90                   	nop

00000001400032a0 <TlsGetValue>:
   1400032a0:	ff 25 fa 6f 00 00    	jmp    QWORD PTR [rip+0x6ffa]        # 14000a2a0 <__imp_TlsGetValue>
   1400032a6:	90                   	nop
   1400032a7:	90                   	nop

00000001400032a8 <Sleep>:
   1400032a8:	ff 25 ea 6f 00 00    	jmp    QWORD PTR [rip+0x6fea]        # 14000a298 <__imp_Sleep>
   1400032ae:	90                   	nop
   1400032af:	90                   	nop

00000001400032b0 <SetUnhandledExceptionFilter>:
   1400032b0:	ff 25 da 6f 00 00    	jmp    QWORD PTR [rip+0x6fda]        # 14000a290 <__imp_SetUnhandledExceptionFilter>
   1400032b6:	90                   	nop
   1400032b7:	90                   	nop

00000001400032b8 <LoadLibraryA>:
   1400032b8:	ff 25 ca 6f 00 00    	jmp    QWORD PTR [rip+0x6fca]        # 14000a288 <__imp_LoadLibraryA>
   1400032be:	90                   	nop
   1400032bf:	90                   	nop

00000001400032c0 <LeaveCriticalSection>:
   1400032c0:	ff 25 ba 6f 00 00    	jmp    QWORD PTR [rip+0x6fba]        # 14000a280 <__imp_LeaveCriticalSection>
   1400032c6:	90                   	nop
   1400032c7:	90                   	nop

00000001400032c8 <InitializeCriticalSection>:
   1400032c8:	ff 25 aa 6f 00 00    	jmp    QWORD PTR [rip+0x6faa]        # 14000a278 <__imp_InitializeCriticalSection>
   1400032ce:	90                   	nop
   1400032cf:	90                   	nop

00000001400032d0 <GetProcAddress>:
   1400032d0:	ff 25 9a 6f 00 00    	jmp    QWORD PTR [rip+0x6f9a]        # 14000a270 <__imp_GetProcAddress>
   1400032d6:	90                   	nop
   1400032d7:	90                   	nop

00000001400032d8 <GetModuleHandleA>:
   1400032d8:	ff 25 8a 6f 00 00    	jmp    QWORD PTR [rip+0x6f8a]        # 14000a268 <__imp_GetModuleHandleA>
   1400032de:	90                   	nop
   1400032df:	90                   	nop

00000001400032e0 <GetLastError>:
   1400032e0:	ff 25 7a 6f 00 00    	jmp    QWORD PTR [rip+0x6f7a]        # 14000a260 <__imp_GetLastError>
   1400032e6:	90                   	nop
   1400032e7:	90                   	nop

00000001400032e8 <FreeLibrary>:
   1400032e8:	ff 25 6a 6f 00 00    	jmp    QWORD PTR [rip+0x6f6a]        # 14000a258 <__imp_FreeLibrary>
   1400032ee:	90                   	nop
   1400032ef:	90                   	nop

00000001400032f0 <EnterCriticalSection>:
   1400032f0:	ff 25 5a 6f 00 00    	jmp    QWORD PTR [rip+0x6f5a]        # 14000a250 <__imp_EnterCriticalSection>
   1400032f6:	90                   	nop
   1400032f7:	90                   	nop

00000001400032f8 <DeleteCriticalSection>:
   1400032f8:	ff 25 4a 6f 00 00    	jmp    QWORD PTR [rip+0x6f4a]        # 14000a248 <__imp_DeleteCriticalSection>
   1400032fe:	90                   	nop
   1400032ff:	90                   	nop

0000000140003300 <std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true> >::~_Hashtable()>:
   140003300:	56                   	push   rsi
   140003301:	53                   	push   rbx
   140003302:	48 83 ec 28          	sub    rsp,0x28
   140003306:	48 8b 59 10          	mov    rbx,QWORD PTR [rcx+0x10]
   14000330a:	48 89 ce             	mov    rsi,rcx
   14000330d:	48 85 db             	test   rbx,rbx
   140003310:	74 23                	je     140003335 <std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true> >::~_Hashtable()+0x35>
   140003312:	0f 1f 00             	nop    DWORD PTR [rax]
   140003315:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000331c:	00 00 00 00 
   140003320:	48 89 d9             	mov    rcx,rbx
   140003323:	48 8b 1b             	mov    rbx,QWORD PTR [rbx]
   140003326:	ba 10 00 00 00       	mov    edx,0x10
   14000332b:	e8 40 e4 ff ff       	call   140001770 <operator delete(void*, unsigned long long)>
   140003330:	48 85 db             	test   rbx,rbx
   140003333:	75 eb                	jne    140003320 <std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true> >::~_Hashtable()+0x20>
   140003335:	48 8b 0e             	mov    rcx,QWORD PTR [rsi]
   140003338:	48 8d 46 30          	lea    rax,[rsi+0x30]
   14000333c:	48 39 c1             	cmp    rcx,rax
   14000333f:	74 17                	je     140003358 <std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true> >::~_Hashtable()+0x58>
   140003341:	48 8b 56 08          	mov    rdx,QWORD PTR [rsi+0x8]
   140003345:	48 c1 e2 03          	shl    rdx,0x3
   140003349:	48 83 c4 28          	add    rsp,0x28
   14000334d:	5b                   	pop    rbx
   14000334e:	5e                   	pop    rsi
   14000334f:	e9 1c e4 ff ff       	jmp    140001770 <operator delete(void*, unsigned long long)>
   140003354:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   140003358:	48 83 c4 28          	add    rsp,0x28
   14000335c:	5b                   	pop    rbx
   14000335d:	5e                   	pop    rsi
   14000335e:	c3                   	ret
   14000335f:	90                   	nop

0000000140003360 <main.cold>:
   140003360:	ba 10 00 00 00       	mov    edx,0x10
   140003365:	4c 89 f1             	mov    rcx,r14
   140003368:	4c 89 bc 24 88 00 00 	mov    QWORD PTR [rsp+0x88],r15
   14000336f:	00 
   140003370:	48 89 c3             	mov    rbx,rax
   140003373:	e8 f8 e3 ff ff       	call   140001770 <operator delete(void*, unsigned long long)>
   140003378:	48 8d 4c 24 60       	lea    rcx,[rsp+0x60]
   14000337d:	e8 7e ff ff ff       	call   140003300 <std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true> >::~_Hashtable()>
   140003382:	48 89 d9             	mov    rcx,rbx
   140003385:	e8 d6 fc ff ff       	call   140003060 <_Unwind_Resume>
   14000338a:	90                   	nop
   14000338b:	90                   	nop
   14000338c:	90                   	nop
   14000338d:	90                   	nop
   14000338e:	90                   	nop
   14000338f:	90                   	nop
   140003390:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   140003397:	00 00 00 
   14000339a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000001400033a0 <main>:
   1400033a0:	41 57                	push   r15
   1400033a2:	41 56                	push   r14
   1400033a4:	41 55                	push   r13
   1400033a6:	41 54                	push   r12
   1400033a8:	55                   	push   rbp
   1400033a9:	57                   	push   rdi
   1400033aa:	56                   	push   rsi
   1400033ab:	53                   	push   rbx
   1400033ac:	48 81 ec a8 00 00 00 	sub    rsp,0xa8
   1400033b3:	31 db                	xor    ebx,ebx
   1400033b5:	45 31 ed             	xor    r13d,r13d
   1400033b8:	48 8d b4 24 90 00 00 	lea    rsi,[rsp+0x90]
   1400033bf:	00 
   1400033c0:	48 8d ac 24 80 00 00 	lea    rbp,[rsp+0x80]
   1400033c7:	00 
   1400033c8:	e8 7a e4 ff ff       	call   140001847 <__main>
   1400033cd:	48 89 74 24 60       	mov    QWORD PTR [rsp+0x60],rsi
   1400033d2:	48 c7 44 24 68 01 00 	mov    QWORD PTR [rsp+0x68],0x1
   1400033d9:	00 00 
   1400033db:	48 c7 44 24 70 00 00 	mov    QWORD PTR [rsp+0x70],0x0
   1400033e2:	00 00 
   1400033e4:	48 c7 44 24 78 00 00 	mov    QWORD PTR [rsp+0x78],0x0
   1400033eb:	00 00 
   1400033ed:	c7 84 24 80 00 00 00 	mov    DWORD PTR [rsp+0x80],0x3f800000
   1400033f4:	00 00 80 3f 
   1400033f8:	48 c7 84 24 88 00 00 	mov    QWORD PTR [rsp+0x88],0x0
   1400033ff:	00 00 00 00 00 
   140003404:	48 c7 84 24 90 00 00 	mov    QWORD PTR [rsp+0x90],0x0
   14000340b:	00 00 00 00 00 
   140003410:	4d 85 ed             	test   r13,r13
   140003413:	0f 84 27 02 00 00    	je     140003640 <main+0x2a0>
   140003419:	4c 8b 54 24 68       	mov    r10,QWORD PTR [rsp+0x68]
   14000341e:	48 89 d8             	mov    rax,rbx
   140003421:	31 d2                	xor    edx,edx
   140003423:	49 f7 f2             	div    r10
   140003426:	48 8b 44 24 60       	mov    rax,QWORD PTR [rsp+0x60]
   14000342b:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   14000342f:	49 89 d1             	mov    r9,rdx
   140003432:	49 89 d4             	mov    r12,rdx
   140003435:	48 85 c0             	test   rax,rax
   140003438:	74 29                	je     140003463 <main+0xc3>
   14000343a:	48 8b 08             	mov    rcx,QWORD PTR [rax]
   14000343d:	44 8b 41 08          	mov    r8d,DWORD PTR [rcx+0x8]
   140003441:	41 39 d8             	cmp    r8d,ebx
   140003444:	0f 84 4d 01 00 00    	je     140003597 <main+0x1f7>
   14000344a:	48 8b 09             	mov    rcx,QWORD PTR [rcx]
   14000344d:	48 85 c9             	test   rcx,rcx
   140003450:	74 11                	je     140003463 <main+0xc3>
   140003452:	48 63 41 08          	movsxd rax,DWORD PTR [rcx+0x8]
   140003456:	31 d2                	xor    edx,edx
   140003458:	49 89 c0             	mov    r8,rax
   14000345b:	49 f7 f2             	div    r10
   14000345e:	4c 39 ca             	cmp    rdx,r9
   140003461:	74 de                	je     140003441 <main+0xa1>
   140003463:	b9 10 00 00 00       	mov    ecx,0x10
   140003468:	e8 fb e2 ff ff       	call   140001768 <operator new(unsigned long long)>
   14000346d:	48 c7 00 00 00 00 00 	mov    QWORD PTR [rax],0x0
   140003474:	4d 89 e9             	mov    r9,r13
   140003477:	48 89 ea             	mov    rdx,rbp
   14000347a:	49 89 c6             	mov    r14,rax
   14000347d:	89 58 08             	mov    DWORD PTR [rax+0x8],ebx
   140003480:	4c 8b 44 24 68       	mov    r8,QWORD PTR [rsp+0x68]
   140003485:	48 8d 4c 24 40       	lea    rcx,[rsp+0x40]
   14000348a:	48 c7 44 24 20 01 00 	mov    QWORD PTR [rsp+0x20],0x1
   140003491:	00 00 
   140003493:	4c 8b bc 24 88 00 00 	mov    r15,QWORD PTR [rsp+0x88]
   14000349a:	00 
   14000349b:	e8 e8 e2 ff ff       	call   140001788 <std::__detail::_Prime_rehash_policy::_M_need_rehash(unsigned long long, unsigned long long, unsigned long long) const>
   1400034a0:	4c 8b 6c 24 48       	mov    r13,QWORD PTR [rsp+0x48]
   1400034a5:	80 7c 24 40 00       	cmp    BYTE PTR [rsp+0x40],0x0
   1400034aa:	0f 84 b8 00 00 00    	je     140003568 <main+0x1c8>
   1400034b0:	49 83 fd 01          	cmp    r13,0x1
   1400034b4:	0f 84 57 02 00 00    	je     140003711 <main+0x371>
   1400034ba:	4c 89 e8             	mov    rax,r13
   1400034bd:	48 c1 e8 3c          	shr    rax,0x3c
   1400034c1:	0f 85 5c 02 00 00    	jne    140003723 <main+0x383>
   1400034c7:	4e 8d 04 ed 00 00 00 	lea    r8,[r13*8+0x0]
   1400034ce:	00 
   1400034cf:	4c 89 c1             	mov    rcx,r8
   1400034d2:	4c 89 44 24 38       	mov    QWORD PTR [rsp+0x38],r8
   1400034d7:	e8 8c e2 ff ff       	call   140001768 <operator new(unsigned long long)>
   1400034dc:	4c 8b 44 24 38       	mov    r8,QWORD PTR [rsp+0x38]
   1400034e1:	31 d2                	xor    edx,edx
   1400034e3:	48 89 c1             	mov    rcx,rax
   1400034e6:	49 89 c4             	mov    r12,rax
   1400034e9:	e8 6a fd ff ff       	call   140003258 <memset>
   1400034ee:	31 c0                	xor    eax,eax
   1400034f0:	4c 8b 44 24 70       	mov    r8,QWORD PTR [rsp+0x70]
   1400034f5:	45 31 d2             	xor    r10d,r10d
   1400034f8:	4c 8d 4c 24 70       	lea    r9,[rsp+0x70]
   1400034fd:	48 89 44 24 70       	mov    QWORD PTR [rsp+0x70],rax
   140003502:	4d 85 c0             	test   r8,r8
   140003505:	74 30                	je     140003537 <main+0x197>
   140003507:	4c 89 c1             	mov    rcx,r8
   14000350a:	31 d2                	xor    edx,edx
   14000350c:	4d 8b 00             	mov    r8,QWORD PTR [r8]
   14000350f:	48 63 41 08          	movsxd rax,DWORD PTR [rcx+0x8]
   140003513:	49 f7 f5             	div    r13
   140003516:	49 8d 04 d4          	lea    rax,[r12+rdx*8]
   14000351a:	4c 8b 18             	mov    r11,QWORD PTR [rax]
   14000351d:	4d 85 db             	test   r11,r11
   140003520:	0f 84 52 01 00 00    	je     140003678 <main+0x2d8>
   140003526:	49 8b 13             	mov    rdx,QWORD PTR [r11]
   140003529:	48 89 11             	mov    QWORD PTR [rcx],rdx
   14000352c:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000352f:	48 89 08             	mov    QWORD PTR [rax],rcx
   140003532:	4d 85 c0             	test   r8,r8
   140003535:	75 d0                	jne    140003507 <main+0x167>
   140003537:	48 8b 4c 24 60       	mov    rcx,QWORD PTR [rsp+0x60]
   14000353c:	48 39 f1             	cmp    rcx,rsi
   14000353f:	74 12                	je     140003553 <main+0x1b3>
   140003541:	48 8b 44 24 68       	mov    rax,QWORD PTR [rsp+0x68]
   140003546:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   14000354d:	00 
   14000354e:	e8 1d e2 ff ff       	call   140001770 <operator delete(void*, unsigned long long)>
   140003553:	48 89 d8             	mov    rax,rbx
   140003556:	31 d2                	xor    edx,edx
   140003558:	4c 89 6c 24 68       	mov    QWORD PTR [rsp+0x68],r13
   14000355d:	49 f7 f5             	div    r13
   140003560:	4c 89 64 24 60       	mov    QWORD PTR [rsp+0x60],r12
   140003565:	49 89 d4             	mov    r12,rdx
   140003568:	4c 8b 44 24 60       	mov    r8,QWORD PTR [rsp+0x60]
   14000356d:	4b 8d 0c e0          	lea    rcx,[r8+r12*8]
   140003571:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   140003574:	48 85 c0             	test   rax,rax
   140003577:	0f 84 66 01 00 00    	je     1400036e3 <main+0x343>
   14000357d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140003580:	49 89 06             	mov    QWORD PTR [r14],rax
   140003583:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   140003586:	4c 89 30             	mov    QWORD PTR [rax],r14
   140003589:	48 8b 44 24 78       	mov    rax,QWORD PTR [rsp+0x78]
   14000358e:	4c 8d 68 01          	lea    r13,[rax+0x1]
   140003592:	4c 89 6c 24 78       	mov    QWORD PTR [rsp+0x78],r13
   140003597:	48 83 c3 01          	add    rbx,0x1
   14000359b:	48 83 fb 64          	cmp    rbx,0x64
   14000359f:	0f 85 6b fe ff ff    	jne    140003410 <main+0x70>
   1400035a5:	4d 85 ed             	test   r13,r13
   1400035a8:	0f 84 ec 00 00 00    	je     14000369a <main+0x2fa>
   1400035ae:	4c 8b 54 24 68       	mov    r10,QWORD PTR [rsp+0x68]
   1400035b3:	b8 2a 00 00 00       	mov    eax,0x2a
   1400035b8:	31 d2                	xor    edx,edx
   1400035ba:	49 f7 f2             	div    r10
   1400035bd:	48 8b 44 24 60       	mov    rax,QWORD PTR [rsp+0x60]
   1400035c2:	48 8b 0c d0          	mov    rcx,QWORD PTR [rax+rdx*8]
   1400035c6:	49 89 d3             	mov    r11,rdx
   1400035c9:	48 85 c9             	test   rcx,rcx
   1400035cc:	0f 84 07 01 00 00    	je     1400036d9 <main+0x339>
   1400035d2:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   1400035d5:	44 8b 48 08          	mov    r9d,DWORD PTR [rax+0x8]
   1400035d9:	41 83 f9 2a          	cmp    r9d,0x2a
   1400035dd:	74 2d                	je     14000360c <main+0x26c>
   1400035df:	4c 8b 00             	mov    r8,QWORD PTR [rax]
   1400035e2:	4d 85 c0             	test   r8,r8
   1400035e5:	0f 84 ee 00 00 00    	je     1400036d9 <main+0x339>
   1400035eb:	45 8b 48 08          	mov    r9d,DWORD PTR [r8+0x8]
   1400035ef:	48 89 c1             	mov    rcx,rax
   1400035f2:	31 d2                	xor    edx,edx
   1400035f4:	49 63 c1             	movsxd rax,r9d
   1400035f7:	49 f7 f2             	div    r10
   1400035fa:	49 39 d3             	cmp    r11,rdx
   1400035fd:	0f 85 d6 00 00 00    	jne    1400036d9 <main+0x339>
   140003603:	4c 89 c0             	mov    rax,r8
   140003606:	41 83 f9 2a          	cmp    r9d,0x2a
   14000360a:	75 d3                	jne    1400035df <main+0x23f>
   14000360c:	48 83 39 00          	cmp    QWORD PTR [rcx],0x0
   140003610:	0f 94 c0             	sete   al
   140003613:	83 f0 01             	xor    eax,0x1
   140003616:	48 8d 4c 24 60       	lea    rcx,[rsp+0x60]
   14000361b:	88 44 24 5f          	mov    BYTE PTR [rsp+0x5f],al
   14000361f:	0f b6 44 24 5f       	movzx  eax,BYTE PTR [rsp+0x5f]
   140003624:	e8 d7 fc ff ff       	call   140003300 <std::_Hashtable<int, int, std::allocator<int>, std::__detail::_Identity, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, true, true> >::~_Hashtable()>
   140003629:	31 c0                	xor    eax,eax
   14000362b:	48 81 c4 a8 00 00 00 	add    rsp,0xa8
   140003632:	5b                   	pop    rbx
   140003633:	5e                   	pop    rsi
   140003634:	5f                   	pop    rdi
   140003635:	5d                   	pop    rbp
   140003636:	41 5c                	pop    r12
   140003638:	41 5d                	pop    r13
   14000363a:	41 5e                	pop    r14
   14000363c:	41 5f                	pop    r15
   14000363e:	c3                   	ret
   14000363f:	90                   	nop
   140003640:	48 8b 44 24 70       	mov    rax,QWORD PTR [rsp+0x70]
   140003645:	48 85 c0             	test   rax,rax
   140003648:	74 17                	je     140003661 <main+0x2c1>
   14000364a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
   140003650:	39 58 08             	cmp    DWORD PTR [rax+0x8],ebx
   140003653:	0f 84 3e ff ff ff    	je     140003597 <main+0x1f7>
   140003659:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000365c:	48 85 c0             	test   rax,rax
   14000365f:	75 ef                	jne    140003650 <main+0x2b0>
   140003661:	48 89 d8             	mov    rax,rbx
   140003664:	31 d2                	xor    edx,edx
   140003666:	48 f7 74 24 68       	div    QWORD PTR [rsp+0x68]
   14000366b:	49 89 d4             	mov    r12,rdx
   14000366e:	e9 f0 fd ff ff       	jmp    140003463 <main+0xc3>
   140003673:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140003678:	4c 8b 5c 24 70       	mov    r11,QWORD PTR [rsp+0x70]
   14000367d:	4c 89 19             	mov    QWORD PTR [rcx],r11
   140003680:	48 89 4c 24 70       	mov    QWORD PTR [rsp+0x70],rcx
   140003685:	4c 89 08             	mov    QWORD PTR [rax],r9
   140003688:	48 83 39 00          	cmp    QWORD PTR [rcx],0x0
   14000368c:	74 04                	je     140003692 <main+0x2f2>
   14000368e:	4b 89 0c d4          	mov    QWORD PTR [r12+r10*8],rcx
   140003692:	49 89 d2             	mov    r10,rdx
   140003695:	e9 68 fe ff ff       	jmp    140003502 <main+0x162>
   14000369a:	48 8b 44 24 70       	mov    rax,QWORD PTR [rsp+0x70]
   14000369f:	48 85 c0             	test   rax,rax
   1400036a2:	74 35                	je     1400036d9 <main+0x339>
   1400036a4:	48 8d 4c 24 70       	lea    rcx,[rsp+0x70]
   1400036a9:	eb 23                	jmp    1400036ce <main+0x32e>
   1400036ab:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   1400036b2:	00 00 00 
   1400036b5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   1400036bc:	00 00 00 00 
   1400036c0:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   1400036c3:	48 89 c1             	mov    rcx,rax
   1400036c6:	48 85 d2             	test   rdx,rdx
   1400036c9:	74 0e                	je     1400036d9 <main+0x339>
   1400036cb:	48 89 d0             	mov    rax,rdx
   1400036ce:	83 78 08 2a          	cmp    DWORD PTR [rax+0x8],0x2a
   1400036d2:	75 ec                	jne    1400036c0 <main+0x320>
   1400036d4:	e9 33 ff ff ff       	jmp    14000360c <main+0x26c>
   1400036d9:	b8 01 00 00 00       	mov    eax,0x1
   1400036de:	e9 30 ff ff ff       	jmp    140003613 <main+0x273>
   1400036e3:	48 8b 44 24 70       	mov    rax,QWORD PTR [rsp+0x70]
   1400036e8:	4c 89 74 24 70       	mov    QWORD PTR [rsp+0x70],r14
   1400036ed:	49 89 06             	mov    QWORD PTR [r14],rax
   1400036f0:	48 85 c0             	test   rax,rax
   1400036f3:	74 0f                	je     140003704 <main+0x364>
   1400036f5:	48 63 40 08          	movsxd rax,DWORD PTR [rax+0x8]
   1400036f9:	31 d2                	xor    edx,edx
   1400036fb:	48 f7 74 24 68       	div    QWORD PTR [rsp+0x68]
   140003700:	4d 89 34 d0          	mov    QWORD PTR [r8+rdx*8],r14
   140003704:	48 8d 44 24 70       	lea    rax,[rsp+0x70]
   140003709:	48 89 01             	mov    QWORD PTR [rcx],rax
   14000370c:	e9 78 fe ff ff       	jmp    140003589 <main+0x1e9>
   140003711:	31 d2                	xor    edx,edx
   140003713:	49 89 f4             	mov    r12,rsi
   140003716:	48 89 94 24 90 00 00 	mov    QWORD PTR [rsp+0x90],rdx
   14000371d:	00 
   14000371e:	e9 cb fd ff ff       	jmp    1400034ee <main+0x14e>
   140003723:	49 c1 ed 3d          	shr    r13,0x3d
   140003727:	74 05                	je     14000372e <main+0x38e>
   140003729:	e8 4a e0 ff ff       	call   140001778 <std::__throw_bad_array_new_length()>
   14000372e:	e8 4d e0 ff ff       	call   140001780 <std::__throw_bad_alloc()>
   140003733:	90                   	nop
   140003734:	e9 27 fc ff ff       	jmp    140003360 <main.cold>
   140003739:	48 89 c3             	mov    rbx,rax
   14000373c:	e9 37 fc ff ff       	jmp    140003378 <main.cold+0x18>
   140003741:	90                   	nop
   140003742:	90                   	nop
   140003743:	90                   	nop
   140003744:	90                   	nop
   140003745:	90                   	nop
   140003746:	90                   	nop
   140003747:	90                   	nop
   140003748:	90                   	nop
   140003749:	90                   	nop
   14000374a:	90                   	nop
   14000374b:	90                   	nop
   14000374c:	90                   	nop
   14000374d:	90                   	nop
   14000374e:	90                   	nop
   14000374f:	90                   	nop
   140003750:	90                   	nop
   140003751:	90                   	nop
   140003752:	90                   	nop
   140003753:	90                   	nop
   140003754:	90                   	nop
   140003755:	90                   	nop
   140003756:	90                   	nop
   140003757:	90                   	nop
   140003758:	90                   	nop
   140003759:	90                   	nop
   14000375a:	90                   	nop
   14000375b:	90                   	nop
   14000375c:	90                   	nop
   14000375d:	90                   	nop
   14000375e:	90                   	nop
   14000375f:	90                   	nop

0000000140003760 <register_frame_ctor>:
   140003760:	e9 0b df ff ff       	jmp    140001670 <__gcc_register_frame>
   140003765:	90                   	nop
   140003766:	90                   	nop
   140003767:	90                   	nop
   140003768:	90                   	nop
   140003769:	90                   	nop
   14000376a:	90                   	nop
   14000376b:	90                   	nop
   14000376c:	90                   	nop
   14000376d:	90                   	nop
   14000376e:	90                   	nop
   14000376f:	90                   	nop
