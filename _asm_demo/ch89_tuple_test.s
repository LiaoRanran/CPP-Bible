
/tmp/ch89_tuple.exe:     file format pei-x86-64


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
   1400010e8:	48 8b 05 e9 90 00 00 	mov    rax,QWORD PTR [rip+0x90e9]        # 14000a1d8 <__imp_Sleep>
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
   14000117c:	e8 d7 20 00 00       	call   140003258 <setvbuf>
   140001181:	48 8d 05 8f fe ff ff 	lea    rax,[rip+0xfffffffffffffe8f]        # 140001017 <safe_flush>
   140001188:	48 89 c1             	mov    rcx,rax
   14000118b:	e8 9f 04 00 00       	call   14000162f <atexit>
   140001190:	85 c0                	test   eax,eax
   140001192:	74 05                	je     140001199 <__tmainCRTStartup+0x10b>
   140001194:	e8 7f 20 00 00       	call   140003218 <abort>
   140001199:	e8 02 11 00 00       	call   1400022a0 <_pei386_runtime_relocator>
   14000119e:	48 8b 05 1b 43 00 00 	mov    rax,QWORD PTR [rip+0x431b]        # 1400054c0 <.refptr._gnu_exception_handler>
   1400011a5:	48 89 c1             	mov    rcx,rax
   1400011a8:	48 8b 05 21 90 00 00 	mov    rax,QWORD PTR [rip+0x9021]        # 14000a1d0 <__imp_SetUnhandledExceptionFilter>
   1400011af:	ff d0                	call   rax
   1400011b1:	48 8b 15 68 42 00 00 	mov    rdx,QWORD PTR [rip+0x4268]        # 140005420 <.refptr.__mingw_oldexcpt_handler>
   1400011b8:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400011bb:	48 8d 05 3e fe ff ff 	lea    rax,[rip+0xfffffffffffffe3e]        # 140001000 <__mingw_invalidParameterHandler>
   1400011c2:	48 89 c1             	mov    rcx,rax
   1400011c5:	e8 76 1f 00 00       	call   140003140 <_set_invalid_parameter_handler>
   1400011ca:	e8 e1 19 00 00       	call   140002bb0 <_fpreset>
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
   14000121d:	e8 5e 06 00 00       	call   140001880 <_setargv>
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
   14000124d:	e8 68 11 00 00       	call   1400023ba <__mingw_setusermatherr>
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
   140001320:	e8 32 05 00 00       	call   140001857 <__main>
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
   1400013b5:	e8 36 1f 00 00       	call   1400032f0 <main>
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
   14000155c:	e8 07 1d 00 00       	call   140003268 <strlen>
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
   140001682:	ff 15 20 8b 00 00    	call   QWORD PTR [rip+0x8b20]        # 14000a1a8 <__imp_GetModuleHandleA>
   140001688:	48 89 c3             	mov    rbx,rax
   14000168b:	48 85 c0             	test   rax,rax
   14000168e:	74 70                	je     140001700 <__gcc_register_frame+0x90>
   140001690:	48 8d 0d 69 39 00 00 	lea    rcx,[rip+0x3969]        # 140005000 <.rdata>
   140001697:	ff 15 2b 8b 00 00    	call   QWORD PTR [rip+0x8b2b]        # 14000a1c8 <__imp_LoadLibraryA>
   14000169d:	4c 8b 0d 0c 8b 00 00 	mov    r9,QWORD PTR [rip+0x8b0c]        # 14000a1b0 <__imp_GetProcAddress>
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
   14000174e:	48 ff 25 43 8a 00 00 	rex.W jmp QWORD PTR [rip+0x8a43]        # 14000a198 <__imp_FreeLibrary>
   140001755:	0f 1f 00             	nop    DWORD PTR [rax]
   140001758:	48 83 c4 20          	add    rsp,0x20
   14000175c:	5d                   	pop    rbp
   14000175d:	c3                   	ret
   14000175e:	90                   	nop
   14000175f:	90                   	nop

0000000140001760 <use_get(std::tuple<int, double, char> const&)>:
   140001760:	0f be 11             	movsx  edx,BYTE PTR [rcx]
   140001763:	f2 0f 2c 41 08       	cvttsd2si eax,QWORD PTR [rcx+0x8]
   140001768:	03 41 10             	add    eax,DWORD PTR [rcx+0x10]
   14000176b:	01 d0                	add    eax,edx
   14000176d:	c3                   	ret
   14000176e:	66 90                	xchg   ax,ax

0000000140001770 <use_bind(std::tuple<int, double, char> const&)>:
   140001770:	0f be 11             	movsx  edx,BYTE PTR [rcx]
   140001773:	f2 0f 2c 41 08       	cvttsd2si eax,QWORD PTR [rcx+0x8]
   140001778:	03 41 10             	add    eax,DWORD PTR [rcx+0x10]
   14000177b:	01 d0                	add    eax,edx
   14000177d:	c3                   	ret
   14000177e:	66 90                	xchg   ax,ax

0000000140001780 <use_agg(P const&)>:
   140001780:	0f be 51 10          	movsx  edx,BYTE PTR [rcx+0x10]
   140001784:	f2 0f 2c 41 08       	cvttsd2si eax,QWORD PTR [rcx+0x8]
   140001789:	03 01                	add    eax,DWORD PTR [rcx]
   14000178b:	01 d0                	add    eax,edx
   14000178d:	c3                   	ret
   14000178e:	66 90                	xchg   ax,ax

0000000140001790 <emit_size()>:
   140001790:	c7 05 e6 78 00 00 18 	mov    DWORD PTR [rip+0x78e6],0x18        # 140009080 <g_obs>
   140001797:	00 00 00 
   14000179a:	c3                   	ret
   14000179b:	90                   	nop
   14000179c:	90                   	nop
   14000179d:	90                   	nop
   14000179e:	90                   	nop
   14000179f:	90                   	nop

00000001400017a0 <__do_global_dtors>:
   1400017a0:	55                   	push   rbp
   1400017a1:	48 89 e5             	mov    rbp,rsp
   1400017a4:	48 83 ec 20          	sub    rsp,0x20
   1400017a8:	eb 1e                	jmp    1400017c8 <__do_global_dtors+0x28>
   1400017aa:	48 8b 05 5f 28 00 00 	mov    rax,QWORD PTR [rip+0x285f]        # 140004010 <p.0>
   1400017b1:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017b4:	ff d0                	call   rax
   1400017b6:	48 8b 05 53 28 00 00 	mov    rax,QWORD PTR [rip+0x2853]        # 140004010 <p.0>
   1400017bd:	48 83 c0 08          	add    rax,0x8
   1400017c1:	48 89 05 48 28 00 00 	mov    QWORD PTR [rip+0x2848],rax        # 140004010 <p.0>
   1400017c8:	48 8b 05 41 28 00 00 	mov    rax,QWORD PTR [rip+0x2841]        # 140004010 <p.0>
   1400017cf:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017d2:	48 85 c0             	test   rax,rax
   1400017d5:	75 d3                	jne    1400017aa <__do_global_dtors+0xa>
   1400017d7:	90                   	nop
   1400017d8:	90                   	nop
   1400017d9:	48 83 c4 20          	add    rsp,0x20
   1400017dd:	5d                   	pop    rbp
   1400017de:	c3                   	ret

00000001400017df <__do_global_ctors>:
   1400017df:	55                   	push   rbp
   1400017e0:	48 89 e5             	mov    rbp,rsp
   1400017e3:	48 83 ec 30          	sub    rsp,0x30
   1400017e7:	48 8b 05 62 3b 00 00 	mov    rax,QWORD PTR [rip+0x3b62]        # 140005350 <.refptr.__CTOR_LIST__>
   1400017ee:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017f1:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400017f4:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
   1400017f8:	75 25                	jne    14000181f <__do_global_ctors+0x40>
   1400017fa:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001801:	eb 04                	jmp    140001807 <__do_global_ctors+0x28>
   140001803:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001807:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000180a:	8d 50 01             	lea    edx,[rax+0x1]
   14000180d:	48 8b 05 3c 3b 00 00 	mov    rax,QWORD PTR [rip+0x3b3c]        # 140005350 <.refptr.__CTOR_LIST__>
   140001814:	89 d2                	mov    edx,edx
   140001816:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   14000181a:	48 85 c0             	test   rax,rax
   14000181d:	75 e4                	jne    140001803 <__do_global_ctors+0x24>
   14000181f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001822:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140001825:	eb 14                	jmp    14000183b <__do_global_ctors+0x5c>
   140001827:	48 8b 05 22 3b 00 00 	mov    rax,QWORD PTR [rip+0x3b22]        # 140005350 <.refptr.__CTOR_LIST__>
   14000182e:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140001831:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   140001835:	ff d0                	call   rax
   140001837:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   14000183b:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   14000183f:	75 e6                	jne    140001827 <__do_global_ctors+0x48>
   140001841:	48 8d 05 58 ff ff ff 	lea    rax,[rip+0xffffffffffffff58]        # 1400017a0 <__do_global_dtors>
   140001848:	48 89 c1             	mov    rcx,rax
   14000184b:	e8 df fd ff ff       	call   14000162f <atexit>
   140001850:	90                   	nop
   140001851:	48 83 c4 30          	add    rsp,0x30
   140001855:	5d                   	pop    rbp
   140001856:	c3                   	ret

0000000140001857 <__main>:
   140001857:	55                   	push   rbp
   140001858:	48 89 e5             	mov    rbp,rsp
   14000185b:	48 83 ec 20          	sub    rsp,0x20
   14000185f:	8b 05 2b 78 00 00    	mov    eax,DWORD PTR [rip+0x782b]        # 140009090 <initialized>
   140001865:	85 c0                	test   eax,eax
   140001867:	75 0f                	jne    140001878 <__main+0x21>
   140001869:	c7 05 1d 78 00 00 01 	mov    DWORD PTR [rip+0x781d],0x1        # 140009090 <initialized>
   140001870:	00 00 00 
   140001873:	e8 67 ff ff ff       	call   1400017df <__do_global_ctors>
   140001878:	90                   	nop
   140001879:	48 83 c4 20          	add    rsp,0x20
   14000187d:	5d                   	pop    rbp
   14000187e:	c3                   	ret
   14000187f:	90                   	nop

0000000140001880 <_setargv>:
   140001880:	55                   	push   rbp
   140001881:	48 89 e5             	mov    rbp,rsp
   140001884:	b8 00 00 00 00       	mov    eax,0x0
   140001889:	5d                   	pop    rbp
   14000188a:	c3                   	ret
   14000188b:	90                   	nop
   14000188c:	90                   	nop
   14000188d:	90                   	nop
   14000188e:	90                   	nop
   14000188f:	90                   	nop

0000000140001890 <__dyn_tls_init>:
   140001890:	55                   	push   rbp
   140001891:	48 89 e5             	mov    rbp,rsp
   140001894:	48 83 ec 30          	sub    rsp,0x30
   140001898:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000189c:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   14000189f:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400018a3:	48 8b 05 86 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a86]        # 140005330 <.refptr._CRT_MT>
   1400018aa:	8b 00                	mov    eax,DWORD PTR [rax]
   1400018ac:	83 f8 02             	cmp    eax,0x2
   1400018af:	74 0d                	je     1400018be <__dyn_tls_init+0x2e>
   1400018b1:	48 8b 05 78 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a78]        # 140005330 <.refptr._CRT_MT>
   1400018b8:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   1400018be:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   1400018c2:	74 1e                	je     1400018e2 <__dyn_tls_init+0x52>
   1400018c4:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   1400018c8:	75 5b                	jne    140001925 <__dyn_tls_init+0x95>
   1400018ca:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   1400018ce:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   1400018d1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400018d5:	49 89 c8             	mov    r8,rcx
   1400018d8:	48 89 c1             	mov    rcx,rax
   1400018db:	e8 d1 11 00 00       	call   140002ab1 <__mingw_TLScallback>
   1400018e0:	eb 43                	jmp    140001925 <__dyn_tls_init+0x95>
   1400018e2:	48 8d 05 af 3d 00 00 	lea    rax,[rip+0x3daf]        # 140005698 <___crt_xd_start__>
   1400018e9:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400018ed:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   1400018f2:	eb 22                	jmp    140001916 <__dyn_tls_init+0x86>
   1400018f4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400018f8:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400018fc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001900:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001903:	48 85 c0             	test   rax,rax
   140001906:	74 09                	je     140001911 <__dyn_tls_init+0x81>
   140001908:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000190c:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000190f:	ff d0                	call   rax
   140001911:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001916:	48 8d 05 83 3d 00 00 	lea    rax,[rip+0x3d83]        # 1400056a0 <__xd_z>
   14000191d:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140001921:	75 d1                	jne    1400018f4 <__dyn_tls_init+0x64>
   140001923:	eb 01                	jmp    140001926 <__dyn_tls_init+0x96>
   140001925:	90                   	nop
   140001926:	48 83 c4 30          	add    rsp,0x30
   14000192a:	5d                   	pop    rbp
   14000192b:	c3                   	ret

000000014000192c <__tlregdtor>:
   14000192c:	55                   	push   rbp
   14000192d:	48 89 e5             	mov    rbp,rsp
   140001930:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001934:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140001939:	75 07                	jne    140001942 <__tlregdtor+0x16>
   14000193b:	b8 00 00 00 00       	mov    eax,0x0
   140001940:	eb 05                	jmp    140001947 <__tlregdtor+0x1b>
   140001942:	b8 00 00 00 00       	mov    eax,0x0
   140001947:	5d                   	pop    rbp
   140001948:	c3                   	ret

0000000140001949 <__dyn_tls_dtor>:
   140001949:	55                   	push   rbp
   14000194a:	48 89 e5             	mov    rbp,rsp
   14000194d:	48 83 ec 20          	sub    rsp,0x20
   140001951:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001955:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001958:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   14000195c:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140001960:	74 06                	je     140001968 <__dyn_tls_dtor+0x1f>
   140001962:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140001966:	75 18                	jne    140001980 <__dyn_tls_dtor+0x37>
   140001968:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   14000196c:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   14000196f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001973:	49 89 c8             	mov    r8,rcx
   140001976:	48 89 c1             	mov    rcx,rax
   140001979:	e8 33 11 00 00       	call   140002ab1 <__mingw_TLScallback>
   14000197e:	eb 01                	jmp    140001981 <__dyn_tls_dtor+0x38>
   140001980:	90                   	nop
   140001981:	48 83 c4 20          	add    rsp,0x20
   140001985:	5d                   	pop    rbp
   140001986:	c3                   	ret
   140001987:	90                   	nop
   140001988:	90                   	nop
   140001989:	90                   	nop
   14000198a:	90                   	nop
   14000198b:	90                   	nop
   14000198c:	90                   	nop
   14000198d:	90                   	nop
   14000198e:	90                   	nop
   14000198f:	90                   	nop

0000000140001990 <_matherr>:
   140001990:	55                   	push   rbp
   140001991:	53                   	push   rbx
   140001992:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140001999:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   14000199e:	0f 29 75 00          	movaps XMMWORD PTR [rbp+0x0],xmm6
   1400019a2:	0f 29 7d 10          	movaps XMMWORD PTR [rbp+0x10],xmm7
   1400019a6:	44 0f 29 45 20       	movaps XMMWORD PTR [rbp+0x20],xmm8
   1400019ab:	48 89 4d 50          	mov    QWORD PTR [rbp+0x50],rcx
   1400019af:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   1400019b3:	8b 00                	mov    eax,DWORD PTR [rax]
   1400019b5:	83 f8 06             	cmp    eax,0x6
   1400019b8:	74 56                	je     140001a10 <_matherr+0x80>
   1400019ba:	83 f8 06             	cmp    eax,0x6
   1400019bd:	7f 78                	jg     140001a37 <_matherr+0xa7>
   1400019bf:	83 f8 05             	cmp    eax,0x5
   1400019c2:	74 59                	je     140001a1d <_matherr+0x8d>
   1400019c4:	83 f8 05             	cmp    eax,0x5
   1400019c7:	7f 6e                	jg     140001a37 <_matherr+0xa7>
   1400019c9:	83 f8 04             	cmp    eax,0x4
   1400019cc:	74 5c                	je     140001a2a <_matherr+0x9a>
   1400019ce:	83 f8 04             	cmp    eax,0x4
   1400019d1:	7f 64                	jg     140001a37 <_matherr+0xa7>
   1400019d3:	83 f8 03             	cmp    eax,0x3
   1400019d6:	74 2b                	je     140001a03 <_matherr+0x73>
   1400019d8:	83 f8 03             	cmp    eax,0x3
   1400019db:	7f 5a                	jg     140001a37 <_matherr+0xa7>
   1400019dd:	83 f8 01             	cmp    eax,0x1
   1400019e0:	74 07                	je     1400019e9 <_matherr+0x59>
   1400019e2:	83 f8 02             	cmp    eax,0x2
   1400019e5:	74 0f                	je     1400019f6 <_matherr+0x66>
   1400019e7:	eb 4e                	jmp    140001a37 <_matherr+0xa7>
   1400019e9:	48 8d 05 b0 36 00 00 	lea    rax,[rip+0x36b0]        # 1400050a0 <.rdata>
   1400019f0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019f4:	eb 4d                	jmp    140001a43 <_matherr+0xb3>
   1400019f6:	48 8d 05 c2 36 00 00 	lea    rax,[rip+0x36c2]        # 1400050bf <.rdata+0x1f>
   1400019fd:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a01:	eb 40                	jmp    140001a43 <_matherr+0xb3>
   140001a03:	48 8d 05 d6 36 00 00 	lea    rax,[rip+0x36d6]        # 1400050e0 <.rdata+0x40>
   140001a0a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a0e:	eb 33                	jmp    140001a43 <_matherr+0xb3>
   140001a10:	48 8d 05 e9 36 00 00 	lea    rax,[rip+0x36e9]        # 140005100 <.rdata+0x60>
   140001a17:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a1b:	eb 26                	jmp    140001a43 <_matherr+0xb3>
   140001a1d:	48 8d 05 04 37 00 00 	lea    rax,[rip+0x3704]        # 140005128 <.rdata+0x88>
   140001a24:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a28:	eb 19                	jmp    140001a43 <_matherr+0xb3>
   140001a2a:	48 8d 05 1f 37 00 00 	lea    rax,[rip+0x371f]        # 140005150 <.rdata+0xb0>
   140001a31:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a35:	eb 0c                	jmp    140001a43 <_matherr+0xb3>
   140001a37:	48 8d 05 48 37 00 00 	lea    rax,[rip+0x3748]        # 140005186 <.rdata+0xe6>
   140001a3e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a42:	90                   	nop
   140001a43:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a47:	f2 44 0f 10 40 20    	movsd  xmm8,QWORD PTR [rax+0x20]
   140001a4d:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a51:	f2 0f 10 78 18       	movsd  xmm7,QWORD PTR [rax+0x18]
   140001a56:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a5a:	f2 0f 10 70 10       	movsd  xmm6,QWORD PTR [rax+0x10]
   140001a5f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a63:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
   140001a67:	b9 02 00 00 00       	mov    ecx,0x2
   140001a6c:	e8 2f 17 00 00       	call   1400031a0 <__acrt_iob_func>
   140001a71:	48 89 c1             	mov    rcx,rax
   140001a74:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140001a78:	48 8d 05 19 37 00 00 	lea    rax,[rip+0x3719]        # 140005198 <.rdata+0xf8>
   140001a7f:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001a86:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001a8c:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001a92:	49 89 d9             	mov    r9,rbx
   140001a95:	49 89 d0             	mov    r8,rdx
   140001a98:	48 89 c2             	mov    rdx,rax
   140001a9b:	e8 98 17 00 00       	call   140003238 <fprintf>
   140001aa0:	b8 00 00 00 00       	mov    eax,0x0
   140001aa5:	0f 28 75 00          	movaps xmm6,XMMWORD PTR [rbp+0x0]
   140001aa9:	0f 28 7d 10          	movaps xmm7,XMMWORD PTR [rbp+0x10]
   140001aad:	44 0f 28 45 20       	movaps xmm8,XMMWORD PTR [rbp+0x20]
   140001ab2:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140001ab9:	5b                   	pop    rbx
   140001aba:	5d                   	pop    rbp
   140001abb:	c3                   	ret
   140001abc:	90                   	nop
   140001abd:	90                   	nop
   140001abe:	90                   	nop
   140001abf:	90                   	nop

0000000140001ac0 <__report_error>:
   140001ac0:	55                   	push   rbp
   140001ac1:	53                   	push   rbx
   140001ac2:	48 83 ec 38          	sub    rsp,0x38
   140001ac6:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140001acb:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140001acf:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001ad3:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140001ad7:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140001adb:	48 8d 45 28          	lea    rax,[rbp+0x28]
   140001adf:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001ae3:	b9 02 00 00 00       	mov    ecx,0x2
   140001ae8:	e8 b3 16 00 00       	call   1400031a0 <__acrt_iob_func>
   140001aed:	48 89 c1             	mov    rcx,rax
   140001af0:	48 8d 05 d9 36 00 00 	lea    rax,[rip+0x36d9]        # 1400051d0 <.rdata>
   140001af7:	48 89 c2             	mov    rdx,rax
   140001afa:	e8 39 17 00 00       	call   140003238 <fprintf>
   140001aff:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   140001b03:	b9 02 00 00 00       	mov    ecx,0x2
   140001b08:	e8 93 16 00 00       	call   1400031a0 <__acrt_iob_func>
   140001b0d:	48 89 c1             	mov    rcx,rax
   140001b10:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001b14:	49 89 d8             	mov    r8,rbx
   140001b17:	48 89 c2             	mov    rdx,rax
   140001b1a:	e8 59 17 00 00       	call   140003278 <vfprintf>
   140001b1f:	e8 f4 16 00 00       	call   140003218 <abort>
   140001b24:	90                   	nop

0000000140001b25 <mark_section_writable>:
   140001b25:	55                   	push   rbp
   140001b26:	48 89 e5             	mov    rbp,rsp
   140001b29:	48 83 ec 60          	sub    rsp,0x60
   140001b2d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001b31:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001b38:	e9 82 00 00 00       	jmp    140001bbf <mark_section_writable+0x9a>
   140001b3d:	48 8b 0d ac 75 00 00 	mov    rcx,QWORD PTR [rip+0x75ac]        # 1400090f0 <the_secs>
   140001b44:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b47:	48 63 d0             	movsxd rdx,eax
   140001b4a:	48 89 d0             	mov    rax,rdx
   140001b4d:	48 c1 e0 02          	shl    rax,0x2
   140001b51:	48 01 d0             	add    rax,rdx
   140001b54:	48 c1 e0 03          	shl    rax,0x3
   140001b58:	48 01 c8             	add    rax,rcx
   140001b5b:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001b5f:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001b63:	72 56                	jb     140001bbb <mark_section_writable+0x96>
   140001b65:	48 8b 0d 84 75 00 00 	mov    rcx,QWORD PTR [rip+0x7584]        # 1400090f0 <the_secs>
   140001b6c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b6f:	48 63 d0             	movsxd rdx,eax
   140001b72:	48 89 d0             	mov    rax,rdx
   140001b75:	48 c1 e0 02          	shl    rax,0x2
   140001b79:	48 01 d0             	add    rax,rdx
   140001b7c:	48 c1 e0 03          	shl    rax,0x3
   140001b80:	48 01 c8             	add    rax,rcx
   140001b83:	48 8b 48 18          	mov    rcx,QWORD PTR [rax+0x18]
   140001b87:	4c 8b 05 62 75 00 00 	mov    r8,QWORD PTR [rip+0x7562]        # 1400090f0 <the_secs>
   140001b8e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b91:	48 63 d0             	movsxd rdx,eax
   140001b94:	48 89 d0             	mov    rax,rdx
   140001b97:	48 c1 e0 02          	shl    rax,0x2
   140001b9b:	48 01 d0             	add    rax,rdx
   140001b9e:	48 c1 e0 03          	shl    rax,0x3
   140001ba2:	4c 01 c0             	add    rax,r8
   140001ba5:	48 8b 40 20          	mov    rax,QWORD PTR [rax+0x20]
   140001ba9:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001bac:	89 c0                	mov    eax,eax
   140001bae:	48 01 c8             	add    rax,rcx
   140001bb1:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001bb5:	0f 82 41 02 00 00    	jb     140001dfc <mark_section_writable+0x2d7>
   140001bbb:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001bbf:	8b 05 33 75 00 00    	mov    eax,DWORD PTR [rip+0x7533]        # 1400090f8 <maxSections>
   140001bc5:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001bc8:	0f 8c 6f ff ff ff    	jl     140001b3d <mark_section_writable+0x18>
   140001bce:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001bd2:	48 89 c1             	mov    rcx,rax
   140001bd5:	e8 c1 11 00 00       	call   140002d9b <__mingw_GetSectionForAddress>
   140001bda:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001bde:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001be3:	75 13                	jne    140001bf8 <mark_section_writable+0xd3>
   140001be5:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001be9:	48 8d 0d 00 36 00 00 	lea    rcx,[rip+0x3600]        # 1400051f0 <.rdata+0x20>
   140001bf0:	48 89 c2             	mov    rdx,rax
   140001bf3:	e8 c8 fe ff ff       	call   140001ac0 <__report_error>
   140001bf8:	48 8b 0d f1 74 00 00 	mov    rcx,QWORD PTR [rip+0x74f1]        # 1400090f0 <the_secs>
   140001bff:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c02:	48 63 d0             	movsxd rdx,eax
   140001c05:	48 89 d0             	mov    rax,rdx
   140001c08:	48 c1 e0 02          	shl    rax,0x2
   140001c0c:	48 01 d0             	add    rax,rdx
   140001c0f:	48 c1 e0 03          	shl    rax,0x3
   140001c13:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001c17:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c1b:	48 89 42 20          	mov    QWORD PTR [rdx+0x20],rax
   140001c1f:	48 8b 0d ca 74 00 00 	mov    rcx,QWORD PTR [rip+0x74ca]        # 1400090f0 <the_secs>
   140001c26:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c29:	48 63 d0             	movsxd rdx,eax
   140001c2c:	48 89 d0             	mov    rax,rdx
   140001c2f:	48 c1 e0 02          	shl    rax,0x2
   140001c33:	48 01 d0             	add    rax,rdx
   140001c36:	48 c1 e0 03          	shl    rax,0x3
   140001c3a:	48 01 c8             	add    rax,rcx
   140001c3d:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001c43:	e8 9f 12 00 00       	call   140002ee7 <_GetPEImageBase>
   140001c48:	48 89 c1             	mov    rcx,rax
   140001c4b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c4f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140001c52:	41 89 c1             	mov    r9d,eax
   140001c55:	4c 8b 05 94 74 00 00 	mov    r8,QWORD PTR [rip+0x7494]        # 1400090f0 <the_secs>
   140001c5c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c5f:	48 63 d0             	movsxd rdx,eax
   140001c62:	48 89 d0             	mov    rax,rdx
   140001c65:	48 c1 e0 02          	shl    rax,0x2
   140001c69:	48 01 d0             	add    rax,rdx
   140001c6c:	48 c1 e0 03          	shl    rax,0x3
   140001c70:	4c 01 c0             	add    rax,r8
   140001c73:	4a 8d 14 09          	lea    rdx,[rcx+r9*1]
   140001c77:	48 89 50 18          	mov    QWORD PTR [rax+0x18],rdx
   140001c7b:	48 8b 0d 6e 74 00 00 	mov    rcx,QWORD PTR [rip+0x746e]        # 1400090f0 <the_secs>
   140001c82:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c85:	48 63 d0             	movsxd rdx,eax
   140001c88:	48 89 d0             	mov    rax,rdx
   140001c8b:	48 c1 e0 02          	shl    rax,0x2
   140001c8f:	48 01 d0             	add    rax,rdx
   140001c92:	48 c1 e0 03          	shl    rax,0x3
   140001c96:	48 01 c8             	add    rax,rcx
   140001c99:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001c9d:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140001ca1:	41 b8 30 00 00 00    	mov    r8d,0x30
   140001ca7:	48 89 c1             	mov    rcx,rax
   140001caa:	48 8b 05 3f 85 00 00 	mov    rax,QWORD PTR [rip+0x853f]        # 14000a1f0 <__imp_VirtualQuery>
   140001cb1:	ff d0                	call   rax
   140001cb3:	48 85 c0             	test   rax,rax
   140001cb6:	75 3f                	jne    140001cf7 <mark_section_writable+0x1d2>
   140001cb8:	48 8b 0d 31 74 00 00 	mov    rcx,QWORD PTR [rip+0x7431]        # 1400090f0 <the_secs>
   140001cbf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001cc2:	48 63 d0             	movsxd rdx,eax
   140001cc5:	48 89 d0             	mov    rax,rdx
   140001cc8:	48 c1 e0 02          	shl    rax,0x2
   140001ccc:	48 01 d0             	add    rax,rdx
   140001ccf:	48 c1 e0 03          	shl    rax,0x3
   140001cd3:	48 01 c8             	add    rax,rcx
   140001cd6:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
   140001cda:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001cde:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001ce1:	89 c1                	mov    ecx,eax
   140001ce3:	48 8d 05 26 35 00 00 	lea    rax,[rip+0x3526]        # 140005210 <.rdata+0x40>
   140001cea:	49 89 d0             	mov    r8,rdx
   140001ced:	89 ca                	mov    edx,ecx
   140001cef:	48 89 c1             	mov    rcx,rax
   140001cf2:	e8 c9 fd ff ff       	call   140001ac0 <__report_error>
   140001cf7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001cfa:	83 f8 40             	cmp    eax,0x40
   140001cfd:	0f 84 e8 00 00 00    	je     140001deb <mark_section_writable+0x2c6>
   140001d03:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d06:	83 f8 04             	cmp    eax,0x4
   140001d09:	0f 84 dc 00 00 00    	je     140001deb <mark_section_writable+0x2c6>
   140001d0f:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d12:	3d 80 00 00 00       	cmp    eax,0x80
   140001d17:	0f 84 ce 00 00 00    	je     140001deb <mark_section_writable+0x2c6>
   140001d1d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d20:	83 f8 08             	cmp    eax,0x8
   140001d23:	0f 84 c2 00 00 00    	je     140001deb <mark_section_writable+0x2c6>
   140001d29:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d2c:	83 f8 02             	cmp    eax,0x2
   140001d2f:	75 09                	jne    140001d3a <mark_section_writable+0x215>
   140001d31:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140001d38:	eb 07                	jmp    140001d41 <mark_section_writable+0x21c>
   140001d3a:	c7 45 f8 40 00 00 00 	mov    DWORD PTR [rbp-0x8],0x40
   140001d41:	48 8b 0d a8 73 00 00 	mov    rcx,QWORD PTR [rip+0x73a8]        # 1400090f0 <the_secs>
   140001d48:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d4b:	48 63 d0             	movsxd rdx,eax
   140001d4e:	48 89 d0             	mov    rax,rdx
   140001d51:	48 c1 e0 02          	shl    rax,0x2
   140001d55:	48 01 d0             	add    rax,rdx
   140001d58:	48 c1 e0 03          	shl    rax,0x3
   140001d5c:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d60:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001d64:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   140001d68:	48 8b 0d 81 73 00 00 	mov    rcx,QWORD PTR [rip+0x7381]        # 1400090f0 <the_secs>
   140001d6f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d72:	48 63 d0             	movsxd rdx,eax
   140001d75:	48 89 d0             	mov    rax,rdx
   140001d78:	48 c1 e0 02          	shl    rax,0x2
   140001d7c:	48 01 d0             	add    rax,rdx
   140001d7f:	48 c1 e0 03          	shl    rax,0x3
   140001d83:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d87:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140001d8b:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   140001d8f:	48 8b 0d 5a 73 00 00 	mov    rcx,QWORD PTR [rip+0x735a]        # 1400090f0 <the_secs>
   140001d96:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d99:	48 63 d0             	movsxd rdx,eax
   140001d9c:	48 89 d0             	mov    rax,rdx
   140001d9f:	48 c1 e0 02          	shl    rax,0x2
   140001da3:	48 01 d0             	add    rax,rdx
   140001da6:	48 c1 e0 03          	shl    rax,0x3
   140001daa:	48 01 c8             	add    rax,rcx
   140001dad:	49 89 c0             	mov    r8,rax
   140001db0:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   140001db4:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001db8:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   140001dbb:	4d 89 c1             	mov    r9,r8
   140001dbe:	41 89 c8             	mov    r8d,ecx
   140001dc1:	48 89 c1             	mov    rcx,rax
   140001dc4:	48 8b 05 1d 84 00 00 	mov    rax,QWORD PTR [rip+0x841d]        # 14000a1e8 <__imp_VirtualProtect>
   140001dcb:	ff d0                	call   rax
   140001dcd:	85 c0                	test   eax,eax
   140001dcf:	75 1a                	jne    140001deb <mark_section_writable+0x2c6>
   140001dd1:	48 8b 05 c8 83 00 00 	mov    rax,QWORD PTR [rip+0x83c8]        # 14000a1a0 <__imp_GetLastError>
   140001dd8:	ff d0                	call   rax
   140001dda:	89 c2                	mov    edx,eax
   140001ddc:	48 8d 05 65 34 00 00 	lea    rax,[rip+0x3465]        # 140005248 <.rdata+0x78>
   140001de3:	48 89 c1             	mov    rcx,rax
   140001de6:	e8 d5 fc ff ff       	call   140001ac0 <__report_error>
   140001deb:	8b 05 07 73 00 00    	mov    eax,DWORD PTR [rip+0x7307]        # 1400090f8 <maxSections>
   140001df1:	83 c0 01             	add    eax,0x1
   140001df4:	89 05 fe 72 00 00    	mov    DWORD PTR [rip+0x72fe],eax        # 1400090f8 <maxSections>
   140001dfa:	eb 01                	jmp    140001dfd <mark_section_writable+0x2d8>
   140001dfc:	90                   	nop
   140001dfd:	48 83 c4 60          	add    rsp,0x60
   140001e01:	5d                   	pop    rbp
   140001e02:	c3                   	ret

0000000140001e03 <restore_modified_sections>:
   140001e03:	55                   	push   rbp
   140001e04:	48 89 e5             	mov    rbp,rsp
   140001e07:	48 83 ec 30          	sub    rsp,0x30
   140001e0b:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001e12:	e9 ad 00 00 00       	jmp    140001ec4 <restore_modified_sections+0xc1>
   140001e17:	48 8b 0d d2 72 00 00 	mov    rcx,QWORD PTR [rip+0x72d2]        # 1400090f0 <the_secs>
   140001e1e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e21:	48 63 d0             	movsxd rdx,eax
   140001e24:	48 89 d0             	mov    rax,rdx
   140001e27:	48 c1 e0 02          	shl    rax,0x2
   140001e2b:	48 01 d0             	add    rax,rdx
   140001e2e:	48 c1 e0 03          	shl    rax,0x3
   140001e32:	48 01 c8             	add    rax,rcx
   140001e35:	8b 00                	mov    eax,DWORD PTR [rax]
   140001e37:	85 c0                	test   eax,eax
   140001e39:	0f 84 80 00 00 00    	je     140001ebf <restore_modified_sections+0xbc>
   140001e3f:	48 8b 0d aa 72 00 00 	mov    rcx,QWORD PTR [rip+0x72aa]        # 1400090f0 <the_secs>
   140001e46:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e49:	48 63 d0             	movsxd rdx,eax
   140001e4c:	48 89 d0             	mov    rax,rdx
   140001e4f:	48 c1 e0 02          	shl    rax,0x2
   140001e53:	48 01 d0             	add    rax,rdx
   140001e56:	48 c1 e0 03          	shl    rax,0x3
   140001e5a:	48 01 c8             	add    rax,rcx
   140001e5d:	44 8b 10             	mov    r10d,DWORD PTR [rax]
   140001e60:	48 8b 0d 89 72 00 00 	mov    rcx,QWORD PTR [rip+0x7289]        # 1400090f0 <the_secs>
   140001e67:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e6a:	48 63 d0             	movsxd rdx,eax
   140001e6d:	48 89 d0             	mov    rax,rdx
   140001e70:	48 c1 e0 02          	shl    rax,0x2
   140001e74:	48 01 d0             	add    rax,rdx
   140001e77:	48 c1 e0 03          	shl    rax,0x3
   140001e7b:	48 01 c8             	add    rax,rcx
   140001e7e:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   140001e82:	4c 8b 05 67 72 00 00 	mov    r8,QWORD PTR [rip+0x7267]        # 1400090f0 <the_secs>
   140001e89:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e8c:	48 63 d0             	movsxd rdx,eax
   140001e8f:	48 89 d0             	mov    rax,rdx
   140001e92:	48 c1 e0 02          	shl    rax,0x2
   140001e96:	48 01 d0             	add    rax,rdx
   140001e99:	48 c1 e0 03          	shl    rax,0x3
   140001e9d:	4c 01 c0             	add    rax,r8
   140001ea0:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   140001ea4:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   140001ea8:	49 89 d1             	mov    r9,rdx
   140001eab:	45 89 d0             	mov    r8d,r10d
   140001eae:	48 89 ca             	mov    rdx,rcx
   140001eb1:	48 89 c1             	mov    rcx,rax
   140001eb4:	48 8b 05 2d 83 00 00 	mov    rax,QWORD PTR [rip+0x832d]        # 14000a1e8 <__imp_VirtualProtect>
   140001ebb:	ff d0                	call   rax
   140001ebd:	eb 01                	jmp    140001ec0 <restore_modified_sections+0xbd>
   140001ebf:	90                   	nop
   140001ec0:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001ec4:	8b 05 2e 72 00 00    	mov    eax,DWORD PTR [rip+0x722e]        # 1400090f8 <maxSections>
   140001eca:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001ecd:	0f 8c 44 ff ff ff    	jl     140001e17 <restore_modified_sections+0x14>
   140001ed3:	90                   	nop
   140001ed4:	90                   	nop
   140001ed5:	48 83 c4 30          	add    rsp,0x30
   140001ed9:	5d                   	pop    rbp
   140001eda:	c3                   	ret

0000000140001edb <__write_memory>:
   140001edb:	55                   	push   rbp
   140001edc:	48 89 e5             	mov    rbp,rsp
   140001edf:	48 83 ec 20          	sub    rsp,0x20
   140001ee3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001ee7:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001eeb:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001eef:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140001ef4:	74 25                	je     140001f1b <__write_memory+0x40>
   140001ef6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001efa:	48 89 c1             	mov    rcx,rax
   140001efd:	e8 23 fc ff ff       	call   140001b25 <mark_section_writable>
   140001f02:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001f06:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140001f0a:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f0e:	49 89 c8             	mov    r8,rcx
   140001f11:	48 89 c1             	mov    rcx,rax
   140001f14:	e8 37 13 00 00       	call   140003250 <memcpy>
   140001f19:	eb 01                	jmp    140001f1c <__write_memory+0x41>
   140001f1b:	90                   	nop
   140001f1c:	48 83 c4 20          	add    rsp,0x20
   140001f20:	5d                   	pop    rbp
   140001f21:	c3                   	ret

0000000140001f22 <do_pseudo_reloc>:
   140001f22:	55                   	push   rbp
   140001f23:	48 89 e5             	mov    rbp,rsp
   140001f26:	48 83 c4 80          	add    rsp,0xffffffffffffff80
   140001f2a:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001f2e:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001f32:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001f36:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140001f3a:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   140001f3e:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001f42:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f46:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001f4a:	48 83 7d e0 07       	cmp    QWORD PTR [rbp-0x20],0x7
   140001f4f:	0f 8e 44 03 00 00    	jle    140002299 <do_pseudo_reloc+0x377>
   140001f55:	48 83 7d e0 0b       	cmp    QWORD PTR [rbp-0x20],0xb
   140001f5a:	7e 25                	jle    140001f81 <do_pseudo_reloc+0x5f>
   140001f5c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f60:	8b 00                	mov    eax,DWORD PTR [rax]
   140001f62:	85 c0                	test   eax,eax
   140001f64:	75 1b                	jne    140001f81 <do_pseudo_reloc+0x5f>
   140001f66:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f6a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f6d:	85 c0                	test   eax,eax
   140001f6f:	75 10                	jne    140001f81 <do_pseudo_reloc+0x5f>
   140001f71:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f75:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001f78:	85 c0                	test   eax,eax
   140001f7a:	75 05                	jne    140001f81 <do_pseudo_reloc+0x5f>
   140001f7c:	48 83 45 f8 0c       	add    QWORD PTR [rbp-0x8],0xc
   140001f81:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f85:	8b 00                	mov    eax,DWORD PTR [rax]
   140001f87:	85 c0                	test   eax,eax
   140001f89:	75 0b                	jne    140001f96 <do_pseudo_reloc+0x74>
   140001f8b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f8f:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f92:	85 c0                	test   eax,eax
   140001f94:	74 59                	je     140001fef <do_pseudo_reloc+0xcd>
   140001f96:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f9a:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140001f9e:	eb 40                	jmp    140001fe0 <do_pseudo_reloc+0xbe>
   140001fa0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fa4:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001fa7:	89 c2                	mov    edx,eax
   140001fa9:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001fad:	48 01 d0             	add    rax,rdx
   140001fb0:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001fb4:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001fb8:	8b 10                	mov    edx,DWORD PTR [rax]
   140001fba:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fbe:	8b 00                	mov    eax,DWORD PTR [rax]
   140001fc0:	01 d0                	add    eax,edx
   140001fc2:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
   140001fc5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001fc9:	48 8d 55 b4          	lea    rdx,[rbp-0x4c]
   140001fcd:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001fd3:	48 89 c1             	mov    rcx,rax
   140001fd6:	e8 00 ff ff ff       	call   140001edb <__write_memory>
   140001fdb:	48 83 45 e8 08       	add    QWORD PTR [rbp-0x18],0x8
   140001fe0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fe4:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140001fe8:	72 b6                	jb     140001fa0 <do_pseudo_reloc+0x7e>
   140001fea:	e9 ab 02 00 00       	jmp    14000229a <do_pseudo_reloc+0x378>
   140001fef:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001ff3:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001ff6:	83 f8 01             	cmp    eax,0x1
   140001ff9:	74 18                	je     140002013 <do_pseudo_reloc+0xf1>
   140001ffb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fff:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002002:	89 c2                	mov    edx,eax
   140002004:	48 8d 05 65 32 00 00 	lea    rax,[rip+0x3265]        # 140005270 <.rdata+0xa0>
   14000200b:	48 89 c1             	mov    rcx,rax
   14000200e:	e8 ad fa ff ff       	call   140001ac0 <__report_error>
   140002013:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002017:	48 83 c0 0c          	add    rax,0xc
   14000201b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000201f:	e9 65 02 00 00       	jmp    140002289 <do_pseudo_reloc+0x367>
   140002024:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002028:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000202b:	89 c2                	mov    edx,eax
   14000202d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002031:	48 01 d0             	add    rax,rdx
   140002034:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002038:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000203c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000203e:	89 c2                	mov    edx,eax
   140002040:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002044:	48 01 d0             	add    rax,rdx
   140002047:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000204b:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000204f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002052:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002056:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000205a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000205d:	0f b6 c0             	movzx  eax,al
   140002060:	83 f8 40             	cmp    eax,0x40
   140002063:	0f 84 b6 00 00 00    	je     14000211f <do_pseudo_reloc+0x1fd>
   140002069:	83 f8 40             	cmp    eax,0x40
   14000206c:	0f 87 ba 00 00 00    	ja     14000212c <do_pseudo_reloc+0x20a>
   140002072:	83 f8 20             	cmp    eax,0x20
   140002075:	74 77                	je     1400020ee <do_pseudo_reloc+0x1cc>
   140002077:	83 f8 20             	cmp    eax,0x20
   14000207a:	0f 87 ac 00 00 00    	ja     14000212c <do_pseudo_reloc+0x20a>
   140002080:	83 f8 08             	cmp    eax,0x8
   140002083:	74 0a                	je     14000208f <do_pseudo_reloc+0x16d>
   140002085:	83 f8 10             	cmp    eax,0x10
   140002088:	74 38                	je     1400020c2 <do_pseudo_reloc+0x1a0>
   14000208a:	e9 9d 00 00 00       	jmp    14000212c <do_pseudo_reloc+0x20a>
   14000208f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002093:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140002096:	0f b6 c0             	movzx  eax,al
   140002099:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000209d:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020a1:	25 80 00 00 00       	and    eax,0x80
   1400020a6:	48 85 c0             	test   rax,rax
   1400020a9:	0f 84 9d 00 00 00    	je     14000214c <do_pseudo_reloc+0x22a>
   1400020af:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020b3:	48 0d 00 ff ff ff    	or     rax,0xffffffffffffff00
   1400020b9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020bd:	e9 8a 00 00 00       	jmp    14000214c <do_pseudo_reloc+0x22a>
   1400020c2:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020c6:	0f b7 00             	movzx  eax,WORD PTR [rax]
   1400020c9:	0f b7 c0             	movzx  eax,ax
   1400020cc:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020d0:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020d4:	25 00 80 00 00       	and    eax,0x8000
   1400020d9:	48 85 c0             	test   rax,rax
   1400020dc:	74 71                	je     14000214f <do_pseudo_reloc+0x22d>
   1400020de:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020e2:	48 0d 00 00 ff ff    	or     rax,0xffffffffffff0000
   1400020e8:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020ec:	eb 61                	jmp    14000214f <do_pseudo_reloc+0x22d>
   1400020ee:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020f2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400020f4:	89 c0                	mov    eax,eax
   1400020f6:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020fa:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020fe:	25 00 00 00 80       	and    eax,0x80000000
   140002103:	48 85 c0             	test   rax,rax
   140002106:	74 4a                	je     140002152 <do_pseudo_reloc+0x230>
   140002108:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000210c:	48 ba 00 00 00 00 ff 	movabs rdx,0xffffffff00000000
   140002113:	ff ff ff 
   140002116:	48 09 d0             	or     rax,rdx
   140002119:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000211d:	eb 33                	jmp    140002152 <do_pseudo_reloc+0x230>
   14000211f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002123:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002126:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000212a:	eb 27                	jmp    140002153 <do_pseudo_reloc+0x231>
   14000212c:	48 c7 45 b8 00 00 00 	mov    QWORD PTR [rbp-0x48],0x0
   140002133:	00 
   140002134:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002138:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000213b:	0f b6 c0             	movzx  eax,al
   14000213e:	48 8d 0d 63 31 00 00 	lea    rcx,[rip+0x3163]        # 1400052a8 <.rdata+0xd8>
   140002145:	89 c2                	mov    edx,eax
   140002147:	e8 74 f9 ff ff       	call   140001ac0 <__report_error>
   14000214c:	90                   	nop
   14000214d:	eb 04                	jmp    140002153 <do_pseudo_reloc+0x231>
   14000214f:	90                   	nop
   140002150:	eb 01                	jmp    140002153 <do_pseudo_reloc+0x231>
   140002152:	90                   	nop
   140002153:	48 8b 4d b8          	mov    rcx,QWORD PTR [rbp-0x48]
   140002157:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000215b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000215d:	89 c2                	mov    edx,eax
   14000215f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002163:	48 01 c2             	add    rdx,rax
   140002166:	48 89 c8             	mov    rax,rcx
   140002169:	48 29 d0             	sub    rax,rdx
   14000216c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140002170:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   140002174:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140002178:	48 01 d0             	add    rax,rdx
   14000217b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000217f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002183:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002186:	25 ff 00 00 00       	and    eax,0xff
   14000218b:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   14000218e:	83 7d d4 3f          	cmp    DWORD PTR [rbp-0x2c],0x3f
   140002192:	77 67                	ja     1400021fb <do_pseudo_reloc+0x2d9>
   140002194:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140002197:	ba 01 00 00 00       	mov    edx,0x1
   14000219c:	89 c1                	mov    ecx,eax
   14000219e:	48 d3 e2             	shl    rdx,cl
   1400021a1:	48 89 d0             	mov    rax,rdx
   1400021a4:	48 83 e8 01          	sub    rax,0x1
   1400021a8:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   1400021ac:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400021af:	83 e8 01             	sub    eax,0x1
   1400021b2:	48 c7 c2 ff ff ff ff 	mov    rdx,0xffffffffffffffff
   1400021b9:	89 c1                	mov    ecx,eax
   1400021bb:	48 d3 e2             	shl    rdx,cl
   1400021be:	48 89 d0             	mov    rax,rdx
   1400021c1:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   1400021c5:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021c9:	48 39 45 c8          	cmp    QWORD PTR [rbp-0x38],rax
   1400021cd:	7c 0a                	jl     1400021d9 <do_pseudo_reloc+0x2b7>
   1400021cf:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021d3:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   1400021d7:	7e 22                	jle    1400021fb <do_pseudo_reloc+0x2d9>
   1400021d9:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   1400021dd:	4c 8b 4d d8          	mov    r9,QWORD PTR [rbp-0x28]
   1400021e1:	4c 8b 45 e0          	mov    r8,QWORD PTR [rbp-0x20]
   1400021e5:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400021e8:	48 8d 0d e9 30 00 00 	lea    rcx,[rip+0x30e9]        # 1400052d8 <.rdata+0x108>
   1400021ef:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   1400021f4:	89 c2                	mov    edx,eax
   1400021f6:	e8 c5 f8 ff ff       	call   140001ac0 <__report_error>
   1400021fb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400021ff:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002202:	0f b6 c0             	movzx  eax,al
   140002205:	83 f8 40             	cmp    eax,0x40
   140002208:	74 63                	je     14000226d <do_pseudo_reloc+0x34b>
   14000220a:	83 f8 40             	cmp    eax,0x40
   14000220d:	77 75                	ja     140002284 <do_pseudo_reloc+0x362>
   14000220f:	83 f8 20             	cmp    eax,0x20
   140002212:	74 41                	je     140002255 <do_pseudo_reloc+0x333>
   140002214:	83 f8 20             	cmp    eax,0x20
   140002217:	77 6b                	ja     140002284 <do_pseudo_reloc+0x362>
   140002219:	83 f8 08             	cmp    eax,0x8
   14000221c:	74 07                	je     140002225 <do_pseudo_reloc+0x303>
   14000221e:	83 f8 10             	cmp    eax,0x10
   140002221:	74 1a                	je     14000223d <do_pseudo_reloc+0x31b>
   140002223:	eb 5f                	jmp    140002284 <do_pseudo_reloc+0x362>
   140002225:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002229:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000222d:	41 b8 01 00 00 00    	mov    r8d,0x1
   140002233:	48 89 c1             	mov    rcx,rax
   140002236:	e8 a0 fc ff ff       	call   140001edb <__write_memory>
   14000223b:	eb 47                	jmp    140002284 <do_pseudo_reloc+0x362>
   14000223d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002241:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002245:	41 b8 02 00 00 00    	mov    r8d,0x2
   14000224b:	48 89 c1             	mov    rcx,rax
   14000224e:	e8 88 fc ff ff       	call   140001edb <__write_memory>
   140002253:	eb 2f                	jmp    140002284 <do_pseudo_reloc+0x362>
   140002255:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002259:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000225d:	41 b8 04 00 00 00    	mov    r8d,0x4
   140002263:	48 89 c1             	mov    rcx,rax
   140002266:	e8 70 fc ff ff       	call   140001edb <__write_memory>
   14000226b:	eb 17                	jmp    140002284 <do_pseudo_reloc+0x362>
   14000226d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002271:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002275:	41 b8 08 00 00 00    	mov    r8d,0x8
   14000227b:	48 89 c1             	mov    rcx,rax
   14000227e:	e8 58 fc ff ff       	call   140001edb <__write_memory>
   140002283:	90                   	nop
   140002284:	48 83 45 f0 0c       	add    QWORD PTR [rbp-0x10],0xc
   140002289:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000228d:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140002291:	0f 82 8d fd ff ff    	jb     140002024 <do_pseudo_reloc+0x102>
   140002297:	eb 01                	jmp    14000229a <do_pseudo_reloc+0x378>
   140002299:	90                   	nop
   14000229a:	48 83 ec 80          	sub    rsp,0xffffffffffffff80
   14000229e:	5d                   	pop    rbp
   14000229f:	c3                   	ret

00000001400022a0 <_pei386_runtime_relocator>:
   1400022a0:	55                   	push   rbp
   1400022a1:	48 89 e5             	mov    rbp,rsp
   1400022a4:	48 83 ec 30          	sub    rsp,0x30
   1400022a8:	8b 05 4e 6e 00 00    	mov    eax,DWORD PTR [rip+0x6e4e]        # 1400090fc <was_init.0>
   1400022ae:	85 c0                	test   eax,eax
   1400022b0:	0f 85 88 00 00 00    	jne    14000233e <_pei386_runtime_relocator+0x9e>
   1400022b6:	8b 05 40 6e 00 00    	mov    eax,DWORD PTR [rip+0x6e40]        # 1400090fc <was_init.0>
   1400022bc:	83 c0 01             	add    eax,0x1
   1400022bf:	89 05 37 6e 00 00    	mov    DWORD PTR [rip+0x6e37],eax        # 1400090fc <was_init.0>
   1400022c5:	e8 21 0b 00 00       	call   140002deb <__mingw_GetSectionCount>
   1400022ca:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400022cd:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400022d0:	48 63 d0             	movsxd rdx,eax
   1400022d3:	48 89 d0             	mov    rax,rdx
   1400022d6:	48 c1 e0 02          	shl    rax,0x2
   1400022da:	48 01 d0             	add    rax,rdx
   1400022dd:	48 c1 e0 03          	shl    rax,0x3
   1400022e1:	48 83 c0 0f          	add    rax,0xf
   1400022e5:	48 c1 e8 04          	shr    rax,0x4
   1400022e9:	48 c1 e0 04          	shl    rax,0x4
   1400022ed:	e8 7e 0d 00 00       	call   140003070 <___chkstk_ms>
   1400022f2:	48 29 c4             	sub    rsp,rax
   1400022f5:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   1400022fa:	48 83 c0 0f          	add    rax,0xf
   1400022fe:	48 c1 e8 04          	shr    rax,0x4
   140002302:	48 c1 e0 04          	shl    rax,0x4
   140002306:	48 89 05 e3 6d 00 00 	mov    QWORD PTR [rip+0x6de3],rax        # 1400090f0 <the_secs>
   14000230d:	c7 05 e1 6d 00 00 00 	mov    DWORD PTR [rip+0x6de1],0x0        # 1400090f8 <maxSections>
   140002314:	00 00 00 
   140002317:	48 8b 0d 42 30 00 00 	mov    rcx,QWORD PTR [rip+0x3042]        # 140005360 <.refptr.__ImageBase>
   14000231e:	48 8b 15 4b 30 00 00 	mov    rdx,QWORD PTR [rip+0x304b]        # 140005370 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   140002325:	48 8b 05 54 30 00 00 	mov    rax,QWORD PTR [rip+0x3054]        # 140005380 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000232c:	49 89 c8             	mov    r8,rcx
   14000232f:	48 89 c1             	mov    rcx,rax
   140002332:	e8 eb fb ff ff       	call   140001f22 <do_pseudo_reloc>
   140002337:	e8 c7 fa ff ff       	call   140001e03 <restore_modified_sections>
   14000233c:	eb 01                	jmp    14000233f <_pei386_runtime_relocator+0x9f>
   14000233e:	90                   	nop
   14000233f:	48 89 ec             	mov    rsp,rbp
   140002342:	5d                   	pop    rbp
   140002343:	c3                   	ret
   140002344:	90                   	nop
   140002345:	90                   	nop
   140002346:	90                   	nop
   140002347:	90                   	nop
   140002348:	90                   	nop
   140002349:	90                   	nop
   14000234a:	90                   	nop
   14000234b:	90                   	nop
   14000234c:	90                   	nop
   14000234d:	90                   	nop
   14000234e:	90                   	nop
   14000234f:	90                   	nop

0000000140002350 <__mingw_raise_matherr>:
   140002350:	55                   	push   rbp
   140002351:	48 89 e5             	mov    rbp,rsp
   140002354:	48 83 ec 50          	sub    rsp,0x50
   140002358:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000235b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000235f:	f2 0f 11 55 20       	movsd  QWORD PTR [rbp+0x20],xmm2
   140002364:	f2 0f 11 5d 28       	movsd  QWORD PTR [rbp+0x28],xmm3
   140002369:	48 8b 05 90 6d 00 00 	mov    rax,QWORD PTR [rip+0x6d90]        # 140009100 <stUserMathErr>
   140002370:	48 85 c0             	test   rax,rax
   140002373:	74 3e                	je     1400023b3 <__mingw_raise_matherr+0x63>
   140002375:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140002378:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   14000237b:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000237f:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002383:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   140002388:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   14000238d:	f2 0f 10 45 28       	movsd  xmm0,QWORD PTR [rbp+0x28]
   140002392:	f2 0f 11 45 e8       	movsd  QWORD PTR [rbp-0x18],xmm0
   140002397:	f2 0f 10 45 30       	movsd  xmm0,QWORD PTR [rbp+0x30]
   14000239c:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   1400023a1:	48 8b 15 58 6d 00 00 	mov    rdx,QWORD PTR [rip+0x6d58]        # 140009100 <stUserMathErr>
   1400023a8:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   1400023ac:	48 89 c1             	mov    rcx,rax
   1400023af:	ff d2                	call   rdx
   1400023b1:	eb 01                	jmp    1400023b4 <__mingw_raise_matherr+0x64>
   1400023b3:	90                   	nop
   1400023b4:	48 83 c4 50          	add    rsp,0x50
   1400023b8:	5d                   	pop    rbp
   1400023b9:	c3                   	ret

00000001400023ba <__mingw_setusermatherr>:
   1400023ba:	55                   	push   rbp
   1400023bb:	48 89 e5             	mov    rbp,rsp
   1400023be:	48 83 ec 20          	sub    rsp,0x20
   1400023c2:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400023c6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023ca:	48 89 05 2f 6d 00 00 	mov    QWORD PTR [rip+0x6d2f],rax        # 140009100 <stUserMathErr>
   1400023d1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023d5:	48 89 c1             	mov    rcx,rax
   1400023d8:	e8 13 0e 00 00       	call   1400031f0 <__setusermatherr>
   1400023dd:	90                   	nop
   1400023de:	48 83 c4 20          	add    rsp,0x20
   1400023e2:	5d                   	pop    rbp
   1400023e3:	c3                   	ret
   1400023e4:	90                   	nop
   1400023e5:	90                   	nop
   1400023e6:	90                   	nop
   1400023e7:	90                   	nop
   1400023e8:	90                   	nop
   1400023e9:	90                   	nop
   1400023ea:	90                   	nop
   1400023eb:	90                   	nop
   1400023ec:	90                   	nop
   1400023ed:	90                   	nop
   1400023ee:	90                   	nop
   1400023ef:	90                   	nop

00000001400023f0 <__mingw_SEH_error_handler>:
   1400023f0:	55                   	push   rbp
   1400023f1:	48 89 e5             	mov    rbp,rsp
   1400023f4:	48 83 ec 30          	sub    rsp,0x30
   1400023f8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400023fc:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002400:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002404:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140002408:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   14000240f:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002416:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000241a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000241d:	83 e0 02             	and    eax,0x2
   140002420:	85 c0                	test   eax,eax
   140002422:	74 0a                	je     14000242e <__mingw_SEH_error_handler+0x3e>
   140002424:	b8 01 00 00 00       	mov    eax,0x1
   140002429:	e9 16 02 00 00       	jmp    140002644 <__mingw_SEH_error_handler+0x254>
   14000242e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002432:	8b 00                	mov    eax,DWORD PTR [rax]
   140002434:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002439:	3d 43 43 47 20       	cmp    eax,0x20474343
   14000243e:	75 18                	jne    140002458 <__mingw_SEH_error_handler+0x68>
   140002440:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002444:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002447:	83 e0 01             	and    eax,0x1
   14000244a:	85 c0                	test   eax,eax
   14000244c:	75 0a                	jne    140002458 <__mingw_SEH_error_handler+0x68>
   14000244e:	b8 00 00 00 00       	mov    eax,0x0
   140002453:	e9 ec 01 00 00       	jmp    140002644 <__mingw_SEH_error_handler+0x254>
   140002458:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000245c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000245e:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002463:	0f 84 12 01 00 00    	je     14000257b <__mingw_SEH_error_handler+0x18b>
   140002469:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000246e:	0f 87 c3 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   140002474:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   140002479:	0f 87 b8 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   14000247f:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   140002484:	0f 83 4c 01 00 00    	jae    1400025d6 <__mingw_SEH_error_handler+0x1e6>
   14000248a:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000248f:	0f 84 3a 01 00 00    	je     1400025cf <__mingw_SEH_error_handler+0x1df>
   140002495:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000249a:	0f 87 97 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   1400024a0:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400024a5:	0f 84 83 01 00 00    	je     14000262e <__mingw_SEH_error_handler+0x23e>
   1400024ab:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400024b0:	0f 87 81 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   1400024b6:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400024bb:	0f 87 76 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   1400024c1:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   1400024c6:	0f 83 03 01 00 00    	jae    1400025cf <__mingw_SEH_error_handler+0x1df>
   1400024cc:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400024d1:	0f 84 57 01 00 00    	je     14000262e <__mingw_SEH_error_handler+0x23e>
   1400024d7:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400024dc:	0f 87 55 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   1400024e2:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400024e7:	0f 84 8e 00 00 00    	je     14000257b <__mingw_SEH_error_handler+0x18b>
   1400024ed:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400024f2:	0f 87 3f 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   1400024f8:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   1400024fd:	0f 84 2b 01 00 00    	je     14000262e <__mingw_SEH_error_handler+0x23e>
   140002503:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002508:	0f 87 29 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   14000250e:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002513:	0f 84 15 01 00 00    	je     14000262e <__mingw_SEH_error_handler+0x23e>
   140002519:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000251e:	0f 85 13 01 00 00    	jne    140002637 <__mingw_SEH_error_handler+0x247>
   140002524:	ba 00 00 00 00       	mov    edx,0x0
   140002529:	b9 0b 00 00 00       	mov    ecx,0xb
   14000252e:	e8 2d 0d 00 00       	call   140003260 <signal>
   140002533:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002537:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000253c:	75 1b                	jne    140002559 <__mingw_SEH_error_handler+0x169>
   14000253e:	ba 01 00 00 00       	mov    edx,0x1
   140002543:	b9 0b 00 00 00       	mov    ecx,0xb
   140002548:	e8 13 0d 00 00       	call   140003260 <signal>
   14000254d:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002554:	e9 e1 00 00 00       	jmp    14000263a <__mingw_SEH_error_handler+0x24a>
   140002559:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000255e:	0f 84 d6 00 00 00    	je     14000263a <__mingw_SEH_error_handler+0x24a>
   140002564:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002568:	b9 0b 00 00 00       	mov    ecx,0xb
   14000256d:	ff d0                	call   rax
   14000256f:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002576:	e9 bf 00 00 00       	jmp    14000263a <__mingw_SEH_error_handler+0x24a>
   14000257b:	ba 00 00 00 00       	mov    edx,0x0
   140002580:	b9 04 00 00 00       	mov    ecx,0x4
   140002585:	e8 d6 0c 00 00       	call   140003260 <signal>
   14000258a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000258e:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002593:	75 1b                	jne    1400025b0 <__mingw_SEH_error_handler+0x1c0>
   140002595:	ba 01 00 00 00       	mov    edx,0x1
   14000259a:	b9 04 00 00 00       	mov    ecx,0x4
   14000259f:	e8 bc 0c 00 00       	call   140003260 <signal>
   1400025a4:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025ab:	e9 8d 00 00 00       	jmp    14000263d <__mingw_SEH_error_handler+0x24d>
   1400025b0:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400025b5:	0f 84 82 00 00 00    	je     14000263d <__mingw_SEH_error_handler+0x24d>
   1400025bb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400025bf:	b9 04 00 00 00       	mov    ecx,0x4
   1400025c4:	ff d0                	call   rax
   1400025c6:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025cd:	eb 6e                	jmp    14000263d <__mingw_SEH_error_handler+0x24d>
   1400025cf:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400025d6:	ba 00 00 00 00       	mov    edx,0x0
   1400025db:	b9 08 00 00 00       	mov    ecx,0x8
   1400025e0:	e8 7b 0c 00 00       	call   140003260 <signal>
   1400025e5:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400025e9:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400025ee:	75 23                	jne    140002613 <__mingw_SEH_error_handler+0x223>
   1400025f0:	ba 01 00 00 00       	mov    edx,0x1
   1400025f5:	b9 08 00 00 00       	mov    ecx,0x8
   1400025fa:	e8 61 0c 00 00       	call   140003260 <signal>
   1400025ff:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002603:	74 05                	je     14000260a <__mingw_SEH_error_handler+0x21a>
   140002605:	e8 a6 05 00 00       	call   140002bb0 <_fpreset>
   14000260a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002611:	eb 2d                	jmp    140002640 <__mingw_SEH_error_handler+0x250>
   140002613:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002618:	74 26                	je     140002640 <__mingw_SEH_error_handler+0x250>
   14000261a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000261e:	b9 08 00 00 00       	mov    ecx,0x8
   140002623:	ff d0                	call   rax
   140002625:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000262c:	eb 12                	jmp    140002640 <__mingw_SEH_error_handler+0x250>
   14000262e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002635:	eb 0a                	jmp    140002641 <__mingw_SEH_error_handler+0x251>
   140002637:	90                   	nop
   140002638:	eb 07                	jmp    140002641 <__mingw_SEH_error_handler+0x251>
   14000263a:	90                   	nop
   14000263b:	eb 04                	jmp    140002641 <__mingw_SEH_error_handler+0x251>
   14000263d:	90                   	nop
   14000263e:	eb 01                	jmp    140002641 <__mingw_SEH_error_handler+0x251>
   140002640:	90                   	nop
   140002641:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002644:	48 83 c4 30          	add    rsp,0x30
   140002648:	5d                   	pop    rbp
   140002649:	c3                   	ret

000000014000264a <_gnu_exception_handler>:
   14000264a:	55                   	push   rbp
   14000264b:	48 89 e5             	mov    rbp,rsp
   14000264e:	48 83 ec 30          	sub    rsp,0x30
   140002652:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002656:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000265d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002664:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002668:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000266b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000266d:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002672:	3d 43 43 47 20       	cmp    eax,0x20474343
   140002677:	75 1b                	jne    140002694 <_gnu_exception_handler+0x4a>
   140002679:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000267d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002680:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002683:	83 e0 01             	and    eax,0x1
   140002686:	85 c0                	test   eax,eax
   140002688:	75 0a                	jne    140002694 <_gnu_exception_handler+0x4a>
   14000268a:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000268f:	e9 14 02 00 00       	jmp    1400028a8 <_gnu_exception_handler+0x25e>
   140002694:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002698:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000269b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000269d:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400026a2:	0f 84 12 01 00 00    	je     1400027ba <_gnu_exception_handler+0x170>
   1400026a8:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400026ad:	0f 87 c3 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   1400026b3:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   1400026b8:	0f 87 b8 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   1400026be:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   1400026c3:	0f 83 4c 01 00 00    	jae    140002815 <_gnu_exception_handler+0x1cb>
   1400026c9:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400026ce:	0f 84 3a 01 00 00    	je     14000280e <_gnu_exception_handler+0x1c4>
   1400026d4:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400026d9:	0f 87 97 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   1400026df:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400026e4:	0f 84 83 01 00 00    	je     14000286d <_gnu_exception_handler+0x223>
   1400026ea:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400026ef:	0f 87 81 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   1400026f5:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400026fa:	0f 87 76 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   140002700:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   140002705:	0f 83 03 01 00 00    	jae    14000280e <_gnu_exception_handler+0x1c4>
   14000270b:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   140002710:	0f 84 57 01 00 00    	je     14000286d <_gnu_exception_handler+0x223>
   140002716:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   14000271b:	0f 87 55 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   140002721:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002726:	0f 84 8e 00 00 00    	je     1400027ba <_gnu_exception_handler+0x170>
   14000272c:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002731:	0f 87 3f 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   140002737:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000273c:	0f 84 2b 01 00 00    	je     14000286d <_gnu_exception_handler+0x223>
   140002742:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002747:	0f 87 29 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   14000274d:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002752:	0f 84 15 01 00 00    	je     14000286d <_gnu_exception_handler+0x223>
   140002758:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000275d:	0f 85 13 01 00 00    	jne    140002876 <_gnu_exception_handler+0x22c>
   140002763:	ba 00 00 00 00       	mov    edx,0x0
   140002768:	b9 0b 00 00 00       	mov    ecx,0xb
   14000276d:	e8 ee 0a 00 00       	call   140003260 <signal>
   140002772:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002776:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000277b:	75 1b                	jne    140002798 <_gnu_exception_handler+0x14e>
   14000277d:	ba 01 00 00 00       	mov    edx,0x1
   140002782:	b9 0b 00 00 00       	mov    ecx,0xb
   140002787:	e8 d4 0a 00 00       	call   140003260 <signal>
   14000278c:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002793:	e9 e1 00 00 00       	jmp    140002879 <_gnu_exception_handler+0x22f>
   140002798:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000279d:	0f 84 d6 00 00 00    	je     140002879 <_gnu_exception_handler+0x22f>
   1400027a3:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400027a7:	b9 0b 00 00 00       	mov    ecx,0xb
   1400027ac:	ff d0                	call   rax
   1400027ae:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027b5:	e9 bf 00 00 00       	jmp    140002879 <_gnu_exception_handler+0x22f>
   1400027ba:	ba 00 00 00 00       	mov    edx,0x0
   1400027bf:	b9 04 00 00 00       	mov    ecx,0x4
   1400027c4:	e8 97 0a 00 00       	call   140003260 <signal>
   1400027c9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400027cd:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400027d2:	75 1b                	jne    1400027ef <_gnu_exception_handler+0x1a5>
   1400027d4:	ba 01 00 00 00       	mov    edx,0x1
   1400027d9:	b9 04 00 00 00       	mov    ecx,0x4
   1400027de:	e8 7d 0a 00 00       	call   140003260 <signal>
   1400027e3:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027ea:	e9 8d 00 00 00       	jmp    14000287c <_gnu_exception_handler+0x232>
   1400027ef:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400027f4:	0f 84 82 00 00 00    	je     14000287c <_gnu_exception_handler+0x232>
   1400027fa:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400027fe:	b9 04 00 00 00       	mov    ecx,0x4
   140002803:	ff d0                	call   rax
   140002805:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000280c:	eb 6e                	jmp    14000287c <_gnu_exception_handler+0x232>
   14000280e:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140002815:	ba 00 00 00 00       	mov    edx,0x0
   14000281a:	b9 08 00 00 00       	mov    ecx,0x8
   14000281f:	e8 3c 0a 00 00       	call   140003260 <signal>
   140002824:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002828:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000282d:	75 23                	jne    140002852 <_gnu_exception_handler+0x208>
   14000282f:	ba 01 00 00 00       	mov    edx,0x1
   140002834:	b9 08 00 00 00       	mov    ecx,0x8
   140002839:	e8 22 0a 00 00       	call   140003260 <signal>
   14000283e:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002842:	74 05                	je     140002849 <_gnu_exception_handler+0x1ff>
   140002844:	e8 67 03 00 00       	call   140002bb0 <_fpreset>
   140002849:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002850:	eb 2d                	jmp    14000287f <_gnu_exception_handler+0x235>
   140002852:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002857:	74 26                	je     14000287f <_gnu_exception_handler+0x235>
   140002859:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000285d:	b9 08 00 00 00       	mov    ecx,0x8
   140002862:	ff d0                	call   rax
   140002864:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000286b:	eb 12                	jmp    14000287f <_gnu_exception_handler+0x235>
   14000286d:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002874:	eb 0a                	jmp    140002880 <_gnu_exception_handler+0x236>
   140002876:	90                   	nop
   140002877:	eb 07                	jmp    140002880 <_gnu_exception_handler+0x236>
   140002879:	90                   	nop
   14000287a:	eb 04                	jmp    140002880 <_gnu_exception_handler+0x236>
   14000287c:	90                   	nop
   14000287d:	eb 01                	jmp    140002880 <_gnu_exception_handler+0x236>
   14000287f:	90                   	nop
   140002880:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140002884:	75 1f                	jne    1400028a5 <_gnu_exception_handler+0x25b>
   140002886:	48 8b 05 93 68 00 00 	mov    rax,QWORD PTR [rip+0x6893]        # 140009120 <__mingw_oldexcpt_handler>
   14000288d:	48 85 c0             	test   rax,rax
   140002890:	74 13                	je     1400028a5 <_gnu_exception_handler+0x25b>
   140002892:	48 8b 15 87 68 00 00 	mov    rdx,QWORD PTR [rip+0x6887]        # 140009120 <__mingw_oldexcpt_handler>
   140002899:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000289d:	48 89 c1             	mov    rcx,rax
   1400028a0:	ff d2                	call   rdx
   1400028a2:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400028a5:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400028a8:	48 83 c4 30          	add    rsp,0x30
   1400028ac:	5d                   	pop    rbp
   1400028ad:	c3                   	ret
   1400028ae:	90                   	nop
   1400028af:	90                   	nop

00000001400028b0 <___w64_mingwthr_add_key_dtor>:
   1400028b0:	55                   	push   rbp
   1400028b1:	48 89 e5             	mov    rbp,rsp
   1400028b4:	48 83 ec 30          	sub    rsp,0x30
   1400028b8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400028bb:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400028bf:	8b 05 a3 68 00 00    	mov    eax,DWORD PTR [rip+0x68a3]        # 140009168 <__mingwthr_cs_init>
   1400028c5:	85 c0                	test   eax,eax
   1400028c7:	75 07                	jne    1400028d0 <___w64_mingwthr_add_key_dtor+0x20>
   1400028c9:	b8 00 00 00 00       	mov    eax,0x0
   1400028ce:	eb 7b                	jmp    14000294b <___w64_mingwthr_add_key_dtor+0x9b>
   1400028d0:	ba 18 00 00 00       	mov    edx,0x18
   1400028d5:	b9 01 00 00 00       	mov    ecx,0x1
   1400028da:	e8 41 09 00 00       	call   140003220 <calloc>
   1400028df:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400028e3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400028e8:	75 07                	jne    1400028f1 <___w64_mingwthr_add_key_dtor+0x41>
   1400028ea:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400028ef:	eb 5a                	jmp    14000294b <___w64_mingwthr_add_key_dtor+0x9b>
   1400028f1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400028f5:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   1400028f8:	89 10                	mov    DWORD PTR [rax],edx
   1400028fa:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400028fe:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140002902:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
   140002906:	48 8d 05 33 68 00 00 	lea    rax,[rip+0x6833]        # 140009140 <__mingwthr_cs>
   14000290d:	48 89 c1             	mov    rcx,rax
   140002910:	48 8b 05 79 78 00 00 	mov    rax,QWORD PTR [rip+0x7879]        # 14000a190 <__imp_EnterCriticalSection>
   140002917:	ff d0                	call   rax
   140002919:	48 8b 15 50 68 00 00 	mov    rdx,QWORD PTR [rip+0x6850]        # 140009170 <key_dtor_list>
   140002920:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002924:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002928:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000292c:	48 89 05 3d 68 00 00 	mov    QWORD PTR [rip+0x683d],rax        # 140009170 <key_dtor_list>
   140002933:	48 8d 05 06 68 00 00 	lea    rax,[rip+0x6806]        # 140009140 <__mingwthr_cs>
   14000293a:	48 89 c1             	mov    rcx,rax
   14000293d:	48 8b 05 7c 78 00 00 	mov    rax,QWORD PTR [rip+0x787c]        # 14000a1c0 <__imp_LeaveCriticalSection>
   140002944:	ff d0                	call   rax
   140002946:	b8 00 00 00 00       	mov    eax,0x0
   14000294b:	48 83 c4 30          	add    rsp,0x30
   14000294f:	5d                   	pop    rbp
   140002950:	c3                   	ret

0000000140002951 <___w64_mingwthr_remove_key_dtor>:
   140002951:	55                   	push   rbp
   140002952:	48 89 e5             	mov    rbp,rsp
   140002955:	48 83 ec 30          	sub    rsp,0x30
   140002959:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000295c:	8b 05 06 68 00 00    	mov    eax,DWORD PTR [rip+0x6806]        # 140009168 <__mingwthr_cs_init>
   140002962:	85 c0                	test   eax,eax
   140002964:	75 0a                	jne    140002970 <___w64_mingwthr_remove_key_dtor+0x1f>
   140002966:	b8 00 00 00 00       	mov    eax,0x0
   14000296b:	e9 9c 00 00 00       	jmp    140002a0c <___w64_mingwthr_remove_key_dtor+0xbb>
   140002970:	48 8d 05 c9 67 00 00 	lea    rax,[rip+0x67c9]        # 140009140 <__mingwthr_cs>
   140002977:	48 89 c1             	mov    rcx,rax
   14000297a:	48 8b 05 0f 78 00 00 	mov    rax,QWORD PTR [rip+0x780f]        # 14000a190 <__imp_EnterCriticalSection>
   140002981:	ff d0                	call   rax
   140002983:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   14000298a:	00 
   14000298b:	48 8b 05 de 67 00 00 	mov    rax,QWORD PTR [rip+0x67de]        # 140009170 <key_dtor_list>
   140002992:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002996:	eb 55                	jmp    1400029ed <___w64_mingwthr_remove_key_dtor+0x9c>
   140002998:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000299c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000299e:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   1400029a1:	75 36                	jne    1400029d9 <___w64_mingwthr_remove_key_dtor+0x88>
   1400029a3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400029a8:	75 11                	jne    1400029bb <___w64_mingwthr_remove_key_dtor+0x6a>
   1400029aa:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029ae:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   1400029b2:	48 89 05 b7 67 00 00 	mov    QWORD PTR [rip+0x67b7],rax        # 140009170 <key_dtor_list>
   1400029b9:	eb 10                	jmp    1400029cb <___w64_mingwthr_remove_key_dtor+0x7a>
   1400029bb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029bf:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   1400029c3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400029c7:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   1400029cb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029cf:	48 89 c1             	mov    rcx,rax
   1400029d2:	e8 69 08 00 00       	call   140003240 <free>
   1400029d7:	eb 1b                	jmp    1400029f4 <___w64_mingwthr_remove_key_dtor+0xa3>
   1400029d9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029dd:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400029e1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029e5:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   1400029e9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400029ed:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400029f2:	75 a4                	jne    140002998 <___w64_mingwthr_remove_key_dtor+0x47>
   1400029f4:	48 8d 05 45 67 00 00 	lea    rax,[rip+0x6745]        # 140009140 <__mingwthr_cs>
   1400029fb:	48 89 c1             	mov    rcx,rax
   1400029fe:	48 8b 05 bb 77 00 00 	mov    rax,QWORD PTR [rip+0x77bb]        # 14000a1c0 <__imp_LeaveCriticalSection>
   140002a05:	ff d0                	call   rax
   140002a07:	b8 00 00 00 00       	mov    eax,0x0
   140002a0c:	48 83 c4 30          	add    rsp,0x30
   140002a10:	5d                   	pop    rbp
   140002a11:	c3                   	ret

0000000140002a12 <__mingwthr_run_key_dtors>:
   140002a12:	55                   	push   rbp
   140002a13:	48 89 e5             	mov    rbp,rsp
   140002a16:	48 83 ec 30          	sub    rsp,0x30
   140002a1a:	8b 05 48 67 00 00    	mov    eax,DWORD PTR [rip+0x6748]        # 140009168 <__mingwthr_cs_init>
   140002a20:	85 c0                	test   eax,eax
   140002a22:	0f 84 82 00 00 00    	je     140002aaa <__mingwthr_run_key_dtors+0x98>
   140002a28:	48 8d 05 11 67 00 00 	lea    rax,[rip+0x6711]        # 140009140 <__mingwthr_cs>
   140002a2f:	48 89 c1             	mov    rcx,rax
   140002a32:	48 8b 05 57 77 00 00 	mov    rax,QWORD PTR [rip+0x7757]        # 14000a190 <__imp_EnterCriticalSection>
   140002a39:	ff d0                	call   rax
   140002a3b:	48 8b 05 2e 67 00 00 	mov    rax,QWORD PTR [rip+0x672e]        # 140009170 <key_dtor_list>
   140002a42:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a46:	eb 46                	jmp    140002a8e <__mingwthr_run_key_dtors+0x7c>
   140002a48:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a4c:	8b 00                	mov    eax,DWORD PTR [rax]
   140002a4e:	89 c1                	mov    ecx,eax
   140002a50:	48 8b 05 89 77 00 00 	mov    rax,QWORD PTR [rip+0x7789]        # 14000a1e0 <__imp_TlsGetValue>
   140002a57:	ff d0                	call   rax
   140002a59:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002a5d:	48 8b 05 3c 77 00 00 	mov    rax,QWORD PTR [rip+0x773c]        # 14000a1a0 <__imp_GetLastError>
   140002a64:	ff d0                	call   rax
   140002a66:	85 c0                	test   eax,eax
   140002a68:	75 18                	jne    140002a82 <__mingwthr_run_key_dtors+0x70>
   140002a6a:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002a6f:	74 11                	je     140002a82 <__mingwthr_run_key_dtors+0x70>
   140002a71:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a75:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140002a79:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002a7d:	48 89 c1             	mov    rcx,rax
   140002a80:	ff d2                	call   rdx
   140002a82:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a86:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002a8a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a8e:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002a93:	75 b3                	jne    140002a48 <__mingwthr_run_key_dtors+0x36>
   140002a95:	48 8d 05 a4 66 00 00 	lea    rax,[rip+0x66a4]        # 140009140 <__mingwthr_cs>
   140002a9c:	48 89 c1             	mov    rcx,rax
   140002a9f:	48 8b 05 1a 77 00 00 	mov    rax,QWORD PTR [rip+0x771a]        # 14000a1c0 <__imp_LeaveCriticalSection>
   140002aa6:	ff d0                	call   rax
   140002aa8:	eb 01                	jmp    140002aab <__mingwthr_run_key_dtors+0x99>
   140002aaa:	90                   	nop
   140002aab:	48 83 c4 30          	add    rsp,0x30
   140002aaf:	5d                   	pop    rbp
   140002ab0:	c3                   	ret

0000000140002ab1 <__mingw_TLScallback>:
   140002ab1:	55                   	push   rbp
   140002ab2:	48 89 e5             	mov    rbp,rsp
   140002ab5:	48 83 ec 30          	sub    rsp,0x30
   140002ab9:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002abd:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140002ac0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002ac4:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002ac8:	0f 84 cc 00 00 00    	je     140002b9a <__mingw_TLScallback+0xe9>
   140002ace:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002ad2:	0f 87 ca 00 00 00    	ja     140002ba2 <__mingw_TLScallback+0xf1>
   140002ad8:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002adc:	0f 84 b1 00 00 00    	je     140002b93 <__mingw_TLScallback+0xe2>
   140002ae2:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002ae6:	0f 87 b6 00 00 00    	ja     140002ba2 <__mingw_TLScallback+0xf1>
   140002aec:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140002af0:	74 33                	je     140002b25 <__mingw_TLScallback+0x74>
   140002af2:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140002af6:	0f 85 a6 00 00 00    	jne    140002ba2 <__mingw_TLScallback+0xf1>
   140002afc:	8b 05 66 66 00 00    	mov    eax,DWORD PTR [rip+0x6666]        # 140009168 <__mingwthr_cs_init>
   140002b02:	85 c0                	test   eax,eax
   140002b04:	75 13                	jne    140002b19 <__mingw_TLScallback+0x68>
   140002b06:	48 8d 05 33 66 00 00 	lea    rax,[rip+0x6633]        # 140009140 <__mingwthr_cs>
   140002b0d:	48 89 c1             	mov    rcx,rax
   140002b10:	48 8b 05 a1 76 00 00 	mov    rax,QWORD PTR [rip+0x76a1]        # 14000a1b8 <__imp_InitializeCriticalSection>
   140002b17:	ff d0                	call   rax
   140002b19:	c7 05 45 66 00 00 01 	mov    DWORD PTR [rip+0x6645],0x1        # 140009168 <__mingwthr_cs_init>
   140002b20:	00 00 00 
   140002b23:	eb 7d                	jmp    140002ba2 <__mingw_TLScallback+0xf1>
   140002b25:	e8 e8 fe ff ff       	call   140002a12 <__mingwthr_run_key_dtors>
   140002b2a:	8b 05 38 66 00 00    	mov    eax,DWORD PTR [rip+0x6638]        # 140009168 <__mingwthr_cs_init>
   140002b30:	83 f8 01             	cmp    eax,0x1
   140002b33:	75 6c                	jne    140002ba1 <__mingw_TLScallback+0xf0>
   140002b35:	48 8b 05 34 66 00 00 	mov    rax,QWORD PTR [rip+0x6634]        # 140009170 <key_dtor_list>
   140002b3c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b40:	eb 20                	jmp    140002b62 <__mingw_TLScallback+0xb1>
   140002b42:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b46:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002b4a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b4e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b52:	48 89 c1             	mov    rcx,rax
   140002b55:	e8 e6 06 00 00       	call   140003240 <free>
   140002b5a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b5e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b62:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002b67:	75 d9                	jne    140002b42 <__mingw_TLScallback+0x91>
   140002b69:	48 c7 05 fc 65 00 00 	mov    QWORD PTR [rip+0x65fc],0x0        # 140009170 <key_dtor_list>
   140002b70:	00 00 00 00 
   140002b74:	c7 05 ea 65 00 00 00 	mov    DWORD PTR [rip+0x65ea],0x0        # 140009168 <__mingwthr_cs_init>
   140002b7b:	00 00 00 
   140002b7e:	48 8d 05 bb 65 00 00 	lea    rax,[rip+0x65bb]        # 140009140 <__mingwthr_cs>
   140002b85:	48 89 c1             	mov    rcx,rax
   140002b88:	48 8b 05 f9 75 00 00 	mov    rax,QWORD PTR [rip+0x75f9]        # 14000a188 <__IAT_start__>
   140002b8f:	ff d0                	call   rax
   140002b91:	eb 0e                	jmp    140002ba1 <__mingw_TLScallback+0xf0>
   140002b93:	e8 18 00 00 00       	call   140002bb0 <_fpreset>
   140002b98:	eb 08                	jmp    140002ba2 <__mingw_TLScallback+0xf1>
   140002b9a:	e8 73 fe ff ff       	call   140002a12 <__mingwthr_run_key_dtors>
   140002b9f:	eb 01                	jmp    140002ba2 <__mingw_TLScallback+0xf1>
   140002ba1:	90                   	nop
   140002ba2:	b8 01 00 00 00       	mov    eax,0x1
   140002ba7:	48 83 c4 30          	add    rsp,0x30
   140002bab:	5d                   	pop    rbp
   140002bac:	c3                   	ret
   140002bad:	90                   	nop
   140002bae:	90                   	nop
   140002baf:	90                   	nop

0000000140002bb0 <_fpreset>:
   140002bb0:	55                   	push   rbp
   140002bb1:	48 89 e5             	mov    rbp,rsp
   140002bb4:	db e3                	fninit
   140002bb6:	90                   	nop
   140002bb7:	5d                   	pop    rbp
   140002bb8:	c3                   	ret
   140002bb9:	90                   	nop
   140002bba:	90                   	nop
   140002bbb:	90                   	nop
   140002bbc:	90                   	nop
   140002bbd:	90                   	nop
   140002bbe:	90                   	nop
   140002bbf:	90                   	nop

0000000140002bc0 <_ValidateImageBase>:
   140002bc0:	55                   	push   rbp
   140002bc1:	48 89 e5             	mov    rbp,rsp
   140002bc4:	48 83 ec 20          	sub    rsp,0x20
   140002bc8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002bcc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002bd0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002bd4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bd8:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002bdb:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140002bdf:	74 07                	je     140002be8 <_ValidateImageBase+0x28>
   140002be1:	b8 00 00 00 00       	mov    eax,0x0
   140002be6:	eb 4e                	jmp    140002c36 <_ValidateImageBase+0x76>
   140002be8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bec:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002bef:	48 63 d0             	movsxd rdx,eax
   140002bf2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bf6:	48 01 d0             	add    rax,rdx
   140002bf9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002bfd:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c01:	8b 00                	mov    eax,DWORD PTR [rax]
   140002c03:	3d 50 45 00 00       	cmp    eax,0x4550
   140002c08:	74 07                	je     140002c11 <_ValidateImageBase+0x51>
   140002c0a:	b8 00 00 00 00       	mov    eax,0x0
   140002c0f:	eb 25                	jmp    140002c36 <_ValidateImageBase+0x76>
   140002c11:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c15:	48 83 c0 18          	add    rax,0x18
   140002c19:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002c1d:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c21:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002c24:	66 3d 0b 02          	cmp    ax,0x20b
   140002c28:	74 07                	je     140002c31 <_ValidateImageBase+0x71>
   140002c2a:	b8 00 00 00 00       	mov    eax,0x0
   140002c2f:	eb 05                	jmp    140002c36 <_ValidateImageBase+0x76>
   140002c31:	b8 01 00 00 00       	mov    eax,0x1
   140002c36:	48 83 c4 20          	add    rsp,0x20
   140002c3a:	5d                   	pop    rbp
   140002c3b:	c3                   	ret

0000000140002c3c <_FindPESection>:
   140002c3c:	55                   	push   rbp
   140002c3d:	48 89 e5             	mov    rbp,rsp
   140002c40:	48 83 ec 20          	sub    rsp,0x20
   140002c44:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002c48:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002c4c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c50:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002c53:	48 63 d0             	movsxd rdx,eax
   140002c56:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c5a:	48 01 d0             	add    rax,rdx
   140002c5d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002c61:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002c68:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c6c:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002c70:	0f b7 d0             	movzx  edx,ax
   140002c73:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c77:	48 01 d0             	add    rax,rdx
   140002c7a:	48 83 c0 18          	add    rax,0x18
   140002c7e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002c82:	eb 36                	jmp    140002cba <_FindPESection+0x7e>
   140002c84:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c88:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140002c8b:	89 c0                	mov    eax,eax
   140002c8d:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002c91:	72 1e                	jb     140002cb1 <_FindPESection+0x75>
   140002c93:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c97:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140002c9a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c9e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002ca1:	01 d0                	add    eax,edx
   140002ca3:	89 c0                	mov    eax,eax
   140002ca5:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002ca9:	73 06                	jae    140002cb1 <_FindPESection+0x75>
   140002cab:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002caf:	eb 1e                	jmp    140002ccf <_FindPESection+0x93>
   140002cb1:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002cb5:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002cba:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002cbe:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002cc2:	0f b7 c0             	movzx  eax,ax
   140002cc5:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002cc8:	72 ba                	jb     140002c84 <_FindPESection+0x48>
   140002cca:	b8 00 00 00 00       	mov    eax,0x0
   140002ccf:	48 83 c4 20          	add    rsp,0x20
   140002cd3:	5d                   	pop    rbp
   140002cd4:	c3                   	ret

0000000140002cd5 <_FindPESectionByName>:
   140002cd5:	55                   	push   rbp
   140002cd6:	48 89 e5             	mov    rbp,rsp
   140002cd9:	48 83 ec 40          	sub    rsp,0x40
   140002cdd:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002ce1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002ce5:	48 89 c1             	mov    rcx,rax
   140002ce8:	e8 7b 05 00 00       	call   140003268 <strlen>
   140002ced:	48 83 f8 08          	cmp    rax,0x8
   140002cf1:	76 0a                	jbe    140002cfd <_FindPESectionByName+0x28>
   140002cf3:	b8 00 00 00 00       	mov    eax,0x0
   140002cf8:	e9 98 00 00 00       	jmp    140002d95 <_FindPESectionByName+0xc0>
   140002cfd:	48 8b 05 5c 26 00 00 	mov    rax,QWORD PTR [rip+0x265c]        # 140005360 <.refptr.__ImageBase>
   140002d04:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002d08:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d0c:	48 89 c1             	mov    rcx,rax
   140002d0f:	e8 ac fe ff ff       	call   140002bc0 <_ValidateImageBase>
   140002d14:	85 c0                	test   eax,eax
   140002d16:	75 07                	jne    140002d1f <_FindPESectionByName+0x4a>
   140002d18:	b8 00 00 00 00       	mov    eax,0x0
   140002d1d:	eb 76                	jmp    140002d95 <_FindPESectionByName+0xc0>
   140002d1f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d23:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002d26:	48 63 d0             	movsxd rdx,eax
   140002d29:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d2d:	48 01 d0             	add    rax,rdx
   140002d30:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002d34:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002d3b:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d3f:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002d43:	0f b7 d0             	movzx  edx,ax
   140002d46:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d4a:	48 01 d0             	add    rax,rdx
   140002d4d:	48 83 c0 18          	add    rax,0x18
   140002d51:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d55:	eb 29                	jmp    140002d80 <_FindPESectionByName+0xab>
   140002d57:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d5b:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140002d5f:	41 b8 08 00 00 00    	mov    r8d,0x8
   140002d65:	48 89 c1             	mov    rcx,rax
   140002d68:	e8 03 05 00 00       	call   140003270 <strncmp>
   140002d6d:	85 c0                	test   eax,eax
   140002d6f:	75 06                	jne    140002d77 <_FindPESectionByName+0xa2>
   140002d71:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d75:	eb 1e                	jmp    140002d95 <_FindPESectionByName+0xc0>
   140002d77:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002d7b:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002d80:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d84:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002d88:	0f b7 c0             	movzx  eax,ax
   140002d8b:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002d8e:	72 c7                	jb     140002d57 <_FindPESectionByName+0x82>
   140002d90:	b8 00 00 00 00       	mov    eax,0x0
   140002d95:	48 83 c4 40          	add    rsp,0x40
   140002d99:	5d                   	pop    rbp
   140002d9a:	c3                   	ret

0000000140002d9b <__mingw_GetSectionForAddress>:
   140002d9b:	55                   	push   rbp
   140002d9c:	48 89 e5             	mov    rbp,rsp
   140002d9f:	48 83 ec 30          	sub    rsp,0x30
   140002da3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002da7:	48 8b 05 b2 25 00 00 	mov    rax,QWORD PTR [rip+0x25b2]        # 140005360 <.refptr.__ImageBase>
   140002dae:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002db2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002db6:	48 89 c1             	mov    rcx,rax
   140002db9:	e8 02 fe ff ff       	call   140002bc0 <_ValidateImageBase>
   140002dbe:	85 c0                	test   eax,eax
   140002dc0:	75 07                	jne    140002dc9 <__mingw_GetSectionForAddress+0x2e>
   140002dc2:	b8 00 00 00 00       	mov    eax,0x0
   140002dc7:	eb 1c                	jmp    140002de5 <__mingw_GetSectionForAddress+0x4a>
   140002dc9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002dcd:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002dd1:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002dd5:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002dd9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ddd:	48 89 c1             	mov    rcx,rax
   140002de0:	e8 57 fe ff ff       	call   140002c3c <_FindPESection>
   140002de5:	48 83 c4 30          	add    rsp,0x30
   140002de9:	5d                   	pop    rbp
   140002dea:	c3                   	ret

0000000140002deb <__mingw_GetSectionCount>:
   140002deb:	55                   	push   rbp
   140002dec:	48 89 e5             	mov    rbp,rsp
   140002def:	48 83 ec 30          	sub    rsp,0x30
   140002df3:	48 8b 05 66 25 00 00 	mov    rax,QWORD PTR [rip+0x2566]        # 140005360 <.refptr.__ImageBase>
   140002dfa:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002dfe:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e02:	48 89 c1             	mov    rcx,rax
   140002e05:	e8 b6 fd ff ff       	call   140002bc0 <_ValidateImageBase>
   140002e0a:	85 c0                	test   eax,eax
   140002e0c:	75 07                	jne    140002e15 <__mingw_GetSectionCount+0x2a>
   140002e0e:	b8 00 00 00 00       	mov    eax,0x0
   140002e13:	eb 20                	jmp    140002e35 <__mingw_GetSectionCount+0x4a>
   140002e15:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e19:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e1c:	48 63 d0             	movsxd rdx,eax
   140002e1f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e23:	48 01 d0             	add    rax,rdx
   140002e26:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002e2a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002e2e:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002e32:	0f b7 c0             	movzx  eax,ax
   140002e35:	48 83 c4 30          	add    rsp,0x30
   140002e39:	5d                   	pop    rbp
   140002e3a:	c3                   	ret

0000000140002e3b <_FindPESectionExec>:
   140002e3b:	55                   	push   rbp
   140002e3c:	48 89 e5             	mov    rbp,rsp
   140002e3f:	48 83 ec 40          	sub    rsp,0x40
   140002e43:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002e47:	48 8b 05 12 25 00 00 	mov    rax,QWORD PTR [rip+0x2512]        # 140005360 <.refptr.__ImageBase>
   140002e4e:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002e52:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e56:	48 89 c1             	mov    rcx,rax
   140002e59:	e8 62 fd ff ff       	call   140002bc0 <_ValidateImageBase>
   140002e5e:	85 c0                	test   eax,eax
   140002e60:	75 07                	jne    140002e69 <_FindPESectionExec+0x2e>
   140002e62:	b8 00 00 00 00       	mov    eax,0x0
   140002e67:	eb 78                	jmp    140002ee1 <_FindPESectionExec+0xa6>
   140002e69:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e6d:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e70:	48 63 d0             	movsxd rdx,eax
   140002e73:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e77:	48 01 d0             	add    rax,rdx
   140002e7a:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002e7e:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002e85:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e89:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002e8d:	0f b7 d0             	movzx  edx,ax
   140002e90:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e94:	48 01 d0             	add    rax,rdx
   140002e97:	48 83 c0 18          	add    rax,0x18
   140002e9b:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002e9f:	eb 2b                	jmp    140002ecc <_FindPESectionExec+0x91>
   140002ea1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ea5:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002ea8:	25 00 00 00 20       	and    eax,0x20000000
   140002ead:	85 c0                	test   eax,eax
   140002eaf:	74 12                	je     140002ec3 <_FindPESectionExec+0x88>
   140002eb1:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140002eb6:	75 06                	jne    140002ebe <_FindPESectionExec+0x83>
   140002eb8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ebc:	eb 23                	jmp    140002ee1 <_FindPESectionExec+0xa6>
   140002ebe:	48 83 6d 10 01       	sub    QWORD PTR [rbp+0x10],0x1
   140002ec3:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002ec7:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002ecc:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002ed0:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002ed4:	0f b7 c0             	movzx  eax,ax
   140002ed7:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002eda:	72 c5                	jb     140002ea1 <_FindPESectionExec+0x66>
   140002edc:	b8 00 00 00 00       	mov    eax,0x0
   140002ee1:	48 83 c4 40          	add    rsp,0x40
   140002ee5:	5d                   	pop    rbp
   140002ee6:	c3                   	ret

0000000140002ee7 <_GetPEImageBase>:
   140002ee7:	55                   	push   rbp
   140002ee8:	48 89 e5             	mov    rbp,rsp
   140002eeb:	48 83 ec 30          	sub    rsp,0x30
   140002eef:	48 8b 05 6a 24 00 00 	mov    rax,QWORD PTR [rip+0x246a]        # 140005360 <.refptr.__ImageBase>
   140002ef6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002efa:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002efe:	48 89 c1             	mov    rcx,rax
   140002f01:	e8 ba fc ff ff       	call   140002bc0 <_ValidateImageBase>
   140002f06:	85 c0                	test   eax,eax
   140002f08:	75 07                	jne    140002f11 <_GetPEImageBase+0x2a>
   140002f0a:	b8 00 00 00 00       	mov    eax,0x0
   140002f0f:	eb 04                	jmp    140002f15 <_GetPEImageBase+0x2e>
   140002f11:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f15:	48 83 c4 30          	add    rsp,0x30
   140002f19:	5d                   	pop    rbp
   140002f1a:	c3                   	ret

0000000140002f1b <_IsNonwritableInCurrentImage>:
   140002f1b:	55                   	push   rbp
   140002f1c:	48 89 e5             	mov    rbp,rsp
   140002f1f:	48 83 ec 40          	sub    rsp,0x40
   140002f23:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002f27:	48 8b 05 32 24 00 00 	mov    rax,QWORD PTR [rip+0x2432]        # 140005360 <.refptr.__ImageBase>
   140002f2e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f32:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f36:	48 89 c1             	mov    rcx,rax
   140002f39:	e8 82 fc ff ff       	call   140002bc0 <_ValidateImageBase>
   140002f3e:	85 c0                	test   eax,eax
   140002f40:	75 07                	jne    140002f49 <_IsNonwritableInCurrentImage+0x2e>
   140002f42:	b8 00 00 00 00       	mov    eax,0x0
   140002f47:	eb 3d                	jmp    140002f86 <_IsNonwritableInCurrentImage+0x6b>
   140002f49:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002f4d:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002f51:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f55:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002f59:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f5d:	48 89 c1             	mov    rcx,rax
   140002f60:	e8 d7 fc ff ff       	call   140002c3c <_FindPESection>
   140002f65:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002f69:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   140002f6e:	75 07                	jne    140002f77 <_IsNonwritableInCurrentImage+0x5c>
   140002f70:	b8 00 00 00 00       	mov    eax,0x0
   140002f75:	eb 0f                	jmp    140002f86 <_IsNonwritableInCurrentImage+0x6b>
   140002f77:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f7b:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002f7e:	f7 d0                	not    eax
   140002f80:	c1 e8 1f             	shr    eax,0x1f
   140002f83:	0f b6 c0             	movzx  eax,al
   140002f86:	48 83 c4 40          	add    rsp,0x40
   140002f8a:	5d                   	pop    rbp
   140002f8b:	c3                   	ret

0000000140002f8c <__mingw_enum_import_library_names>:
   140002f8c:	55                   	push   rbp
   140002f8d:	48 89 e5             	mov    rbp,rsp
   140002f90:	48 83 ec 50          	sub    rsp,0x50
   140002f94:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002f97:	48 8b 05 c2 23 00 00 	mov    rax,QWORD PTR [rip+0x23c2]        # 140005360 <.refptr.__ImageBase>
   140002f9e:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002fa2:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fa6:	48 89 c1             	mov    rcx,rax
   140002fa9:	e8 12 fc ff ff       	call   140002bc0 <_ValidateImageBase>
   140002fae:	85 c0                	test   eax,eax
   140002fb0:	75 0a                	jne    140002fbc <__mingw_enum_import_library_names+0x30>
   140002fb2:	b8 00 00 00 00       	mov    eax,0x0
   140002fb7:	e9 ab 00 00 00       	jmp    140003067 <__mingw_enum_import_library_names+0xdb>
   140002fbc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fc0:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002fc3:	48 63 d0             	movsxd rdx,eax
   140002fc6:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fca:	48 01 d0             	add    rax,rdx
   140002fcd:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002fd1:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002fd5:	8b 80 90 00 00 00    	mov    eax,DWORD PTR [rax+0x90]
   140002fdb:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140002fde:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140002fe2:	75 07                	jne    140002feb <__mingw_enum_import_library_names+0x5f>
   140002fe4:	b8 00 00 00 00       	mov    eax,0x0
   140002fe9:	eb 7c                	jmp    140003067 <__mingw_enum_import_library_names+0xdb>
   140002feb:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   140002fee:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002ff2:	48 89 c1             	mov    rcx,rax
   140002ff5:	e8 42 fc ff ff       	call   140002c3c <_FindPESection>
   140002ffa:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002ffe:	48 83 7d d8 00       	cmp    QWORD PTR [rbp-0x28],0x0
   140003003:	75 07                	jne    14000300c <__mingw_enum_import_library_names+0x80>
   140003005:	b8 00 00 00 00       	mov    eax,0x0
   14000300a:	eb 5b                	jmp    140003067 <__mingw_enum_import_library_names+0xdb>
   14000300c:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   14000300f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003013:	48 01 d0             	add    rax,rdx
   140003016:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000301a:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   14000301f:	75 07                	jne    140003028 <__mingw_enum_import_library_names+0x9c>
   140003021:	b8 00 00 00 00       	mov    eax,0x0
   140003026:	eb 3f                	jmp    140003067 <__mingw_enum_import_library_names+0xdb>
   140003028:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000302c:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000302f:	85 c0                	test   eax,eax
   140003031:	75 0b                	jne    14000303e <__mingw_enum_import_library_names+0xb2>
   140003033:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003037:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000303a:	85 c0                	test   eax,eax
   14000303c:	74 23                	je     140003061 <__mingw_enum_import_library_names+0xd5>
   14000303e:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   140003042:	7f 12                	jg     140003056 <__mingw_enum_import_library_names+0xca>
   140003044:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003048:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000304b:	89 c2                	mov    edx,eax
   14000304d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003051:	48 01 d0             	add    rax,rdx
   140003054:	eb 11                	jmp    140003067 <__mingw_enum_import_library_names+0xdb>
   140003056:	83 6d 10 01          	sub    DWORD PTR [rbp+0x10],0x1
   14000305a:	48 83 45 f8 14       	add    QWORD PTR [rbp-0x8],0x14
   14000305f:	eb c7                	jmp    140003028 <__mingw_enum_import_library_names+0x9c>
   140003061:	90                   	nop
   140003062:	b8 00 00 00 00       	mov    eax,0x0
   140003067:	48 83 c4 50          	add    rsp,0x50
   14000306b:	5d                   	pop    rbp
   14000306c:	c3                   	ret
   14000306d:	90                   	nop
   14000306e:	90                   	nop
   14000306f:	90                   	nop

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
   14000314c:	48 8d 05 5d 60 00 00 	lea    rax,[rip+0x605d]        # 1400091b0 <handler>
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
   140003177:	48 8b 05 32 60 00 00 	mov    rax,QWORD PTR [rip+0x6032]        # 1400091b0 <handler>
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
   1400031d0:	ff 25 2a 70 00 00    	jmp    QWORD PTR [rip+0x702a]        # 14000a200 <__imp___C_specific_handler>
   1400031d6:	90                   	nop
   1400031d7:	90                   	nop

00000001400031d8 <__getmainargs>:
   1400031d8:	ff 25 2a 70 00 00    	jmp    QWORD PTR [rip+0x702a]        # 14000a208 <__imp___getmainargs>
   1400031de:	90                   	nop
   1400031df:	90                   	nop

00000001400031e0 <__iob_func>:
   1400031e0:	ff 25 32 70 00 00    	jmp    QWORD PTR [rip+0x7032]        # 14000a218 <__imp___iob_func>
   1400031e6:	90                   	nop
   1400031e7:	90                   	nop

00000001400031e8 <__set_app_type>:
   1400031e8:	ff 25 32 70 00 00    	jmp    QWORD PTR [rip+0x7032]        # 14000a220 <__imp___set_app_type>
   1400031ee:	90                   	nop
   1400031ef:	90                   	nop

00000001400031f0 <__setusermatherr>:
   1400031f0:	ff 25 32 70 00 00    	jmp    QWORD PTR [rip+0x7032]        # 14000a228 <__imp___setusermatherr>
   1400031f6:	90                   	nop
   1400031f7:	90                   	nop

00000001400031f8 <_amsg_exit>:
   1400031f8:	ff 25 32 70 00 00    	jmp    QWORD PTR [rip+0x7032]        # 14000a230 <__imp__amsg_exit>
   1400031fe:	90                   	nop
   1400031ff:	90                   	nop

0000000140003200 <_cexit>:
   140003200:	ff 25 32 70 00 00    	jmp    QWORD PTR [rip+0x7032]        # 14000a238 <__imp__cexit>
   140003206:	90                   	nop
   140003207:	90                   	nop

0000000140003208 <_initterm>:
   140003208:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a250 <__imp__initterm>
   14000320e:	90                   	nop
   14000320f:	90                   	nop

0000000140003210 <_crt_atexit>:
   140003210:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a258 <__imp__crt_atexit>
   140003216:	90                   	nop
   140003217:	90                   	nop

0000000140003218 <abort>:
   140003218:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a260 <__imp_abort>
   14000321e:	90                   	nop
   14000321f:	90                   	nop

0000000140003220 <calloc>:
   140003220:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a268 <__imp_calloc>
   140003226:	90                   	nop
   140003227:	90                   	nop

0000000140003228 <exit>:
   140003228:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a270 <__imp_exit>
   14000322e:	90                   	nop
   14000322f:	90                   	nop

0000000140003230 <fflush>:
   140003230:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a278 <__imp_fflush>
   140003236:	90                   	nop
   140003237:	90                   	nop

0000000140003238 <fprintf>:
   140003238:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a280 <__imp_fprintf>
   14000323e:	90                   	nop
   14000323f:	90                   	nop

0000000140003240 <free>:
   140003240:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a288 <__imp_free>
   140003246:	90                   	nop
   140003247:	90                   	nop

0000000140003248 <malloc>:
   140003248:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a290 <__imp_malloc>
   14000324e:	90                   	nop
   14000324f:	90                   	nop

0000000140003250 <memcpy>:
   140003250:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a298 <__imp_memcpy>
   140003256:	90                   	nop
   140003257:	90                   	nop

0000000140003258 <setvbuf>:
   140003258:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a2a0 <__imp_setvbuf>
   14000325e:	90                   	nop
   14000325f:	90                   	nop

0000000140003260 <signal>:
   140003260:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a2a8 <__imp_signal>
   140003266:	90                   	nop
   140003267:	90                   	nop

0000000140003268 <strlen>:
   140003268:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a2b0 <__imp_strlen>
   14000326e:	90                   	nop
   14000326f:	90                   	nop

0000000140003270 <strncmp>:
   140003270:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a2b8 <__imp_strncmp>
   140003276:	90                   	nop
   140003277:	90                   	nop

0000000140003278 <vfprintf>:
   140003278:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a2c0 <__imp_vfprintf>
   14000327e:	90                   	nop
   14000327f:	90                   	nop

0000000140003280 <VirtualQuery>:
   140003280:	ff 25 6a 6f 00 00    	jmp    QWORD PTR [rip+0x6f6a]        # 14000a1f0 <__imp_VirtualQuery>
   140003286:	90                   	nop
   140003287:	90                   	nop

0000000140003288 <VirtualProtect>:
   140003288:	ff 25 5a 6f 00 00    	jmp    QWORD PTR [rip+0x6f5a]        # 14000a1e8 <__imp_VirtualProtect>
   14000328e:	90                   	nop
   14000328f:	90                   	nop

0000000140003290 <TlsGetValue>:
   140003290:	ff 25 4a 6f 00 00    	jmp    QWORD PTR [rip+0x6f4a]        # 14000a1e0 <__imp_TlsGetValue>
   140003296:	90                   	nop
   140003297:	90                   	nop

0000000140003298 <Sleep>:
   140003298:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a1d8 <__imp_Sleep>
   14000329e:	90                   	nop
   14000329f:	90                   	nop

00000001400032a0 <SetUnhandledExceptionFilter>:
   1400032a0:	ff 25 2a 6f 00 00    	jmp    QWORD PTR [rip+0x6f2a]        # 14000a1d0 <__imp_SetUnhandledExceptionFilter>
   1400032a6:	90                   	nop
   1400032a7:	90                   	nop

00000001400032a8 <LoadLibraryA>:
   1400032a8:	ff 25 1a 6f 00 00    	jmp    QWORD PTR [rip+0x6f1a]        # 14000a1c8 <__imp_LoadLibraryA>
   1400032ae:	90                   	nop
   1400032af:	90                   	nop

00000001400032b0 <LeaveCriticalSection>:
   1400032b0:	ff 25 0a 6f 00 00    	jmp    QWORD PTR [rip+0x6f0a]        # 14000a1c0 <__imp_LeaveCriticalSection>
   1400032b6:	90                   	nop
   1400032b7:	90                   	nop

00000001400032b8 <InitializeCriticalSection>:
   1400032b8:	ff 25 fa 6e 00 00    	jmp    QWORD PTR [rip+0x6efa]        # 14000a1b8 <__imp_InitializeCriticalSection>
   1400032be:	90                   	nop
   1400032bf:	90                   	nop

00000001400032c0 <GetProcAddress>:
   1400032c0:	ff 25 ea 6e 00 00    	jmp    QWORD PTR [rip+0x6eea]        # 14000a1b0 <__imp_GetProcAddress>
   1400032c6:	90                   	nop
   1400032c7:	90                   	nop

00000001400032c8 <GetModuleHandleA>:
   1400032c8:	ff 25 da 6e 00 00    	jmp    QWORD PTR [rip+0x6eda]        # 14000a1a8 <__imp_GetModuleHandleA>
   1400032ce:	90                   	nop
   1400032cf:	90                   	nop

00000001400032d0 <GetLastError>:
   1400032d0:	ff 25 ca 6e 00 00    	jmp    QWORD PTR [rip+0x6eca]        # 14000a1a0 <__imp_GetLastError>
   1400032d6:	90                   	nop
   1400032d7:	90                   	nop

00000001400032d8 <FreeLibrary>:
   1400032d8:	ff 25 ba 6e 00 00    	jmp    QWORD PTR [rip+0x6eba]        # 14000a198 <__imp_FreeLibrary>
   1400032de:	90                   	nop
   1400032df:	90                   	nop

00000001400032e0 <EnterCriticalSection>:
   1400032e0:	ff 25 aa 6e 00 00    	jmp    QWORD PTR [rip+0x6eaa]        # 14000a190 <__imp_EnterCriticalSection>
   1400032e6:	90                   	nop
   1400032e7:	90                   	nop

00000001400032e8 <DeleteCriticalSection>:
   1400032e8:	ff 25 9a 6e 00 00    	jmp    QWORD PTR [rip+0x6e9a]        # 14000a188 <__IAT_start__>
   1400032ee:	90                   	nop
   1400032ef:	90                   	nop

00000001400032f0 <main>:
   1400032f0:	48 83 ec 28          	sub    rsp,0x28
   1400032f4:	e8 5e e5 ff ff       	call   140001857 <__main>
   1400032f9:	b8 7b 00 00 00       	mov    eax,0x7b
   1400032fe:	c7 05 78 5d 00 00 18 	mov    DWORD PTR [rip+0x5d78],0x18        # 140009080 <g_obs>
   140003305:	00 00 00 
   140003308:	48 83 c4 28          	add    rsp,0x28
   14000330c:	c3                   	ret
   14000330d:	90                   	nop
   14000330e:	90                   	nop
   14000330f:	90                   	nop

0000000140003310 <register_frame_ctor>:
   140003310:	e9 5b e3 ff ff       	jmp    140001670 <__gcc_register_frame>
   140003315:	90                   	nop
   140003316:	90                   	nop
   140003317:	90                   	nop
   140003318:	90                   	nop
   140003319:	90                   	nop
   14000331a:	90                   	nop
   14000331b:	90                   	nop
   14000331c:	90                   	nop
   14000331d:	90                   	nop
   14000331e:	90                   	nop
   14000331f:	90                   	nop
