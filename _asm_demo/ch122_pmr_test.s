
ch122_pmr_test.exe:     file format pei-x86-64


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
   140001024:	e8 37 25 00 00       	call   140003560 <fflush>
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
   14000103f:	48 8b 05 da 43 00 00 	mov    rax,QWORD PTR [rip+0x43da]        # 140005420 <.refptr.__mingw_app_type>
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
   14000106e:	48 8b 05 ab 43 00 00 	mov    rax,QWORD PTR [rip+0x43ab]        # 140005420 <.refptr.__mingw_app_type>
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
   1400010e8:	48 8b 05 c1 91 00 00 	mov    rax,QWORD PTR [rip+0x91c1]        # 14000a2b0 <__imp_Sleep>
   1400010ef:	ff d0                	call   rax
   1400010f1:	48 8b 05 78 43 00 00 	mov    rax,QWORD PTR [rip+0x4378]        # 140005470 <.refptr.__native_startup_lock>
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
   140001128:	48 8b 05 51 43 00 00 	mov    rax,QWORD PTR [rip+0x4351]        # 140005480 <.refptr.__native_startup_state>
   14000112f:	8b 00                	mov    eax,DWORD PTR [rax]
   140001131:	83 f8 01             	cmp    eax,0x1
   140001134:	75 0a                	jne    140001140 <__tmainCRTStartup+0xb2>
   140001136:	b9 1f 00 00 00       	mov    ecx,0x1f
   14000113b:	e8 e8 23 00 00       	call   140003528 <_amsg_exit>
   140001140:	48 8b 05 39 43 00 00 	mov    rax,QWORD PTR [rip+0x4339]        # 140005480 <.refptr.__native_startup_state>
   140001147:	8b 00                	mov    eax,DWORD PTR [rax]
   140001149:	85 c0                	test   eax,eax
   14000114b:	0f 85 e3 01 00 00    	jne    140001334 <__tmainCRTStartup+0x2a6>
   140001151:	48 8b 05 28 43 00 00 	mov    rax,QWORD PTR [rip+0x4328]        # 140005480 <.refptr.__native_startup_state>
   140001158:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000115e:	b9 02 00 00 00       	mov    ecx,0x2
   140001163:	e8 68 23 00 00       	call   1400034d0 <__acrt_iob_func>
   140001168:	41 b9 00 00 00 00    	mov    r9d,0x0
   14000116e:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001174:	ba 00 00 00 00       	mov    edx,0x0
   140001179:	48 89 c1             	mov    rcx,rax
   14000117c:	e8 07 24 00 00       	call   140003588 <setvbuf>
   140001181:	48 8d 05 8f fe ff ff 	lea    rax,[rip+0xfffffffffffffe8f]        # 140001017 <safe_flush>
   140001188:	48 89 c1             	mov    rcx,rax
   14000118b:	e8 9f 04 00 00       	call   14000162f <atexit>
   140001190:	85 c0                	test   eax,eax
   140001192:	74 05                	je     140001199 <__tmainCRTStartup+0x10b>
   140001194:	e8 af 23 00 00       	call   140003548 <abort>
   140001199:	e8 22 14 00 00       	call   1400025c0 <_pei386_runtime_relocator>
   14000119e:	48 8b 05 5b 43 00 00 	mov    rax,QWORD PTR [rip+0x435b]        # 140005500 <.refptr._gnu_exception_handler>
   1400011a5:	48 89 c1             	mov    rcx,rax
   1400011a8:	48 8b 05 f9 90 00 00 	mov    rax,QWORD PTR [rip+0x90f9]        # 14000a2a8 <__imp_SetUnhandledExceptionFilter>
   1400011af:	ff d0                	call   rax
   1400011b1:	48 8b 15 a8 42 00 00 	mov    rdx,QWORD PTR [rip+0x42a8]        # 140005460 <.refptr.__mingw_oldexcpt_handler>
   1400011b8:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400011bb:	48 8d 05 3e fe ff ff 	lea    rax,[rip+0xfffffffffffffe3e]        # 140001000 <__mingw_invalidParameterHandler>
   1400011c2:	48 89 c1             	mov    rcx,rax
   1400011c5:	e8 a6 22 00 00       	call   140003470 <_set_invalid_parameter_handler>
   1400011ca:	e8 01 1d 00 00       	call   140002ed0 <_fpreset>
   1400011cf:	e8 18 02 00 00       	call   1400013ec <check_managed_app>
   1400011d4:	89 05 3e 7e 00 00    	mov    DWORD PTR [rip+0x7e3e],eax        # 140009018 <managedapp>
   1400011da:	48 8b 05 3f 42 00 00 	mov    rax,QWORD PTR [rip+0x423f]        # 140005420 <.refptr.__mingw_app_type>
   1400011e1:	8b 00                	mov    eax,DWORD PTR [rax]
   1400011e3:	85 c0                	test   eax,eax
   1400011e5:	74 0c                	je     1400011f3 <__tmainCRTStartup+0x165>
   1400011e7:	b9 02 00 00 00       	mov    ecx,0x2
   1400011ec:	e8 27 23 00 00       	call   140003518 <__set_app_type>
   1400011f1:	eb 0a                	jmp    1400011fd <__tmainCRTStartup+0x16f>
   1400011f3:	b9 01 00 00 00       	mov    ecx,0x1
   1400011f8:	e8 1b 23 00 00       	call   140003518 <__set_app_type>
   1400011fd:	e8 3e 22 00 00       	call   140003440 <__p__fmode>
   140001202:	48 8b 15 e7 42 00 00 	mov    rdx,QWORD PTR [rip+0x42e7]        # 1400054f0 <.refptr._fmode>
   140001209:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000120b:	89 10                	mov    DWORD PTR [rax],edx
   14000120d:	e8 3e 22 00 00       	call   140003450 <__p__commode>
   140001212:	48 8b 15 b7 42 00 00 	mov    rdx,QWORD PTR [rip+0x42b7]        # 1400054d0 <.refptr._commode>
   140001219:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000121b:	89 10                	mov    DWORD PTR [rax],edx
   14000121d:	e8 7e 09 00 00       	call   140001ba0 <_setargv>
   140001222:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140001225:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140001229:	79 0a                	jns    140001235 <__tmainCRTStartup+0x1a7>
   14000122b:	b9 08 00 00 00       	mov    ecx,0x8
   140001230:	e8 f3 22 00 00       	call   140003528 <_amsg_exit>
   140001235:	48 8b 05 34 41 00 00 	mov    rax,QWORD PTR [rip+0x4134]        # 140005370 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   14000123c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000123e:	83 f8 01             	cmp    eax,0x1
   140001241:	75 0f                	jne    140001252 <__tmainCRTStartup+0x1c4>
   140001243:	48 8b 05 c6 42 00 00 	mov    rax,QWORD PTR [rip+0x42c6]        # 140005510 <.refptr._matherr>
   14000124a:	48 89 c1             	mov    rcx,rax
   14000124d:	e8 88 14 00 00       	call   1400026da <__mingw_setusermatherr>
   140001252:	48 8b 05 87 41 00 00 	mov    rax,QWORD PTR [rip+0x4187]        # 1400053e0 <.refptr.__globallocalestatus>
   140001259:	8b 00                	mov    eax,DWORD PTR [rax]
   14000125b:	83 f8 ff             	cmp    eax,0xffffffff
   14000125e:	75 0a                	jne    14000126a <__tmainCRTStartup+0x1dc>
   140001260:	b9 ff ff ff ff       	mov    ecx,0xffffffff
   140001265:	e8 46 22 00 00       	call   1400034b0 <_configthreadlocale>
   14000126a:	48 8b 15 4f 42 00 00 	mov    rdx,QWORD PTR [rip+0x424f]        # 1400054c0 <.refptr.__xi_z>
   140001271:	48 8b 05 38 42 00 00 	mov    rax,QWORD PTR [rip+0x4238]        # 1400054b0 <.refptr.__xi_a>
   140001278:	48 89 c1             	mov    rcx,rax
   14000127b:	e8 60 21 00 00       	call   1400033e0 <_initterm_e>
   140001280:	85 c0                	test   eax,eax
   140001282:	74 0a                	je     14000128e <__tmainCRTStartup+0x200>
   140001284:	b9 0a 00 00 00       	mov    ecx,0xa
   140001289:	e8 9a 22 00 00       	call   140003528 <_amsg_exit>
   14000128e:	48 8b 05 8b 42 00 00 	mov    rax,QWORD PTR [rip+0x428b]        # 140005520 <.refptr._newmode>
   140001295:	8b 00                	mov    eax,DWORD PTR [rax]
   140001297:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000129a:	48 8b 05 3f 42 00 00 	mov    rax,QWORD PTR [rip+0x423f]        # 1400054e0 <.refptr._dowildcard>
   1400012a1:	44 8b 00             	mov    r8d,DWORD PTR [rax]
   1400012a4:	4c 8d 15 65 7d 00 00 	lea    r10,[rip+0x7d65]        # 140009010 <envp>
   1400012ab:	48 8d 15 56 7d 00 00 	lea    rdx,[rip+0x7d56]        # 140009008 <argv>
   1400012b2:	48 8d 05 4b 7d 00 00 	lea    rax,[rip+0x7d4b]        # 140009004 <argc>
   1400012b9:	48 8d 4d ac          	lea    rcx,[rbp-0x54]
   1400012bd:	48 89 4c 24 20       	mov    QWORD PTR [rsp+0x20],rcx
   1400012c2:	45 89 c1             	mov    r9d,r8d
   1400012c5:	4d 89 d0             	mov    r8,r10
   1400012c8:	48 89 c1             	mov    rcx,rax
   1400012cb:	e8 38 22 00 00       	call   140003508 <__getmainargs>
   1400012d0:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012d3:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012d7:	79 0a                	jns    1400012e3 <__tmainCRTStartup+0x255>
   1400012d9:	b9 08 00 00 00       	mov    ecx,0x8
   1400012de:	e8 45 22 00 00       	call   140003528 <_amsg_exit>
   1400012e3:	8b 05 1b 7d 00 00    	mov    eax,DWORD PTR [rip+0x7d1b]        # 140009004 <argc>
   1400012e9:	48 8d 15 18 7d 00 00 	lea    rdx,[rip+0x7d18]        # 140009008 <argv>
   1400012f0:	89 c1                	mov    ecx,eax
   1400012f2:	e8 f9 01 00 00       	call   1400014f0 <duplicate_ppstrings>
   1400012f7:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012fa:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012fe:	74 0a                	je     14000130a <__tmainCRTStartup+0x27c>
   140001300:	b9 08 00 00 00       	mov    ecx,0x8
   140001305:	e8 1e 22 00 00       	call   140003528 <_amsg_exit>
   14000130a:	48 8b 15 8f 41 00 00 	mov    rdx,QWORD PTR [rip+0x418f]        # 1400054a0 <.refptr.__xc_z>
   140001311:	48 8b 05 78 41 00 00 	mov    rax,QWORD PTR [rip+0x4178]        # 140005490 <.refptr.__xc_a>
   140001318:	48 89 c1             	mov    rcx,rax
   14000131b:	e8 18 22 00 00       	call   140003538 <_initterm>
   140001320:	e8 52 08 00 00       	call   140001b77 <__main>
   140001325:	48 8b 05 54 41 00 00 	mov    rax,QWORD PTR [rip+0x4154]        # 140005480 <.refptr.__native_startup_state>
   14000132c:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   140001332:	eb 0a                	jmp    14000133e <__tmainCRTStartup+0x2b0>
   140001334:	c7 05 de 7c 00 00 01 	mov    DWORD PTR [rip+0x7cde],0x1        # 14000901c <has_cctor>
   14000133b:	00 00 00 
   14000133e:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140001342:	75 1e                	jne    140001362 <__tmainCRTStartup+0x2d4>
   140001344:	48 8b 05 25 41 00 00 	mov    rax,QWORD PTR [rip+0x4125]        # 140005470 <.refptr.__native_startup_lock>
   14000134b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000134f:	48 c7 45 b0 00 00 00 	mov    QWORD PTR [rbp-0x50],0x0
   140001356:	00 
   140001357:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   14000135b:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000135f:	48 87 10             	xchg   QWORD PTR [rax],rdx
   140001362:	48 8b 05 67 40 00 00 	mov    rax,QWORD PTR [rip+0x4067]        # 1400053d0 <.refptr.__dyn_tls_init_callback>
   140001369:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000136c:	48 85 c0             	test   rax,rax
   14000136f:	74 1c                	je     14000138d <__tmainCRTStartup+0x2ff>
   140001371:	48 8b 05 58 40 00 00 	mov    rax,QWORD PTR [rip+0x4058]        # 1400053d0 <.refptr.__dyn_tls_init_callback>
   140001378:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000137b:	41 b8 00 00 00 00    	mov    r8d,0x0
   140001381:	ba 02 00 00 00       	mov    edx,0x2
   140001386:	b9 00 00 00 00       	mov    ecx,0x0
   14000138b:	ff d0                	call   rax
   14000138d:	e8 ce 20 00 00       	call   140003460 <__p___initenv>
   140001392:	48 8b 15 77 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c77]        # 140009010 <envp>
   140001399:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000139c:	48 8b 0d 6d 7c 00 00 	mov    rcx,QWORD PTR [rip+0x7c6d]        # 140009010 <envp>
   1400013a3:	48 8b 15 5e 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c5e]        # 140009008 <argv>
   1400013aa:	8b 05 54 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c54]        # 140009004 <argc>
   1400013b0:	49 89 c8             	mov    r8,rcx
   1400013b3:	89 c1                	mov    ecx,eax
   1400013b5:	e8 66 23 00 00       	call   140003720 <main>
   1400013ba:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400013bd:	8b 05 55 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c55]        # 140009018 <managedapp>
   1400013c3:	85 c0                	test   eax,eax
   1400013c5:	75 0a                	jne    1400013d1 <__tmainCRTStartup+0x343>
   1400013c7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013ca:	89 c1                	mov    ecx,eax
   1400013cc:	e8 87 21 00 00       	call   140003558 <exit>
   1400013d1:	8b 05 45 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c45]        # 14000901c <has_cctor>
   1400013d7:	85 c0                	test   eax,eax
   1400013d9:	75 05                	jne    1400013e0 <__tmainCRTStartup+0x352>
   1400013db:	e8 50 21 00 00       	call   140003530 <_cexit>
   1400013e0:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013e3:	48 81 c4 90 00 00 00 	add    rsp,0x90
   1400013ea:	5d                   	pop    rbp
   1400013eb:	c3                   	ret

00000001400013ec <check_managed_app>:
   1400013ec:	55                   	push   rbp
   1400013ed:	48 89 e5             	mov    rbp,rsp
   1400013f0:	48 83 ec 20          	sub    rsp,0x20
   1400013f4:	48 8b 05 35 40 00 00 	mov    rax,QWORD PTR [rip+0x4035]        # 140005430 <.refptr.__mingw_initltsdrot_force>
   1400013fb:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   140001401:	48 8b 05 38 40 00 00 	mov    rax,QWORD PTR [rip+0x4038]        # 140005440 <.refptr.__mingw_initltsdyn_force>
   140001408:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000140e:	48 8b 05 3b 40 00 00 	mov    rax,QWORD PTR [rip+0x403b]        # 140005450 <.refptr.__mingw_initltssuo_force>
   140001415:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000141b:	48 8b 05 7e 3f 00 00 	mov    rax,QWORD PTR [rip+0x3f7e]        # 1400053a0 <.refptr.__ImageBase>
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
   140001511:	e8 62 20 00 00       	call   140003578 <malloc>
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
   14000155c:	e8 37 20 00 00       	call   140003598 <strlen>
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
   140001585:	e8 ee 1f 00 00       	call   140003578 <malloc>
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
   1400015e8:	e8 93 1f 00 00       	call   140003580 <memcpy>
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
   140001642:	e8 f9 1e 00 00       	call   140003540 <_crt_atexit>
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
   140001682:	ff 15 f8 8b 00 00    	call   QWORD PTR [rip+0x8bf8]        # 14000a280 <__imp_GetModuleHandleA>
   140001688:	48 89 c3             	mov    rbx,rax
   14000168b:	48 85 c0             	test   rax,rax
   14000168e:	74 70                	je     140001700 <__gcc_register_frame+0x90>
   140001690:	48 8d 0d 69 39 00 00 	lea    rcx,[rip+0x3969]        # 140005000 <.rdata>
   140001697:	ff 15 03 8c 00 00    	call   QWORD PTR [rip+0x8c03]        # 14000a2a0 <__imp_LoadLibraryA>
   14000169d:	4c 8b 0d e4 8b 00 00 	mov    r9,QWORD PTR [rip+0x8be4]        # 14000a288 <__imp_GetProcAddress>
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
   14000174e:	48 ff 25 1b 8b 00 00 	rex.W jmp QWORD PTR [rip+0x8b1b]        # 14000a270 <__imp_FreeLibrary>
   140001755:	0f 1f 00             	nop    DWORD PTR [rax]
   140001758:	48 83 c4 20          	add    rsp,0x20
   14000175c:	5d                   	pop    rbp
   14000175d:	c3                   	ret
   14000175e:	90                   	nop
   14000175f:	90                   	nop

0000000140001760 <default_push()>:
   140001760:	41 56                	push   r14
   140001762:	41 55                	push   r13
   140001764:	41 54                	push   r12
   140001766:	55                   	push   rbp
   140001767:	57                   	push   rdi
   140001768:	56                   	push   rsi
   140001769:	53                   	push   rbx
   14000176a:	48 83 ec 20          	sub    rsp,0x20
   14000176e:	31 ed                	xor    ebp,ebp
   140001770:	31 f6                	xor    esi,esi
   140001772:	45 31 e4             	xor    r12d,r12d
   140001775:	49 bd ff ff ff ff ff 	movabs r13,0x1fffffffffffffff
   14000177c:	ff ff 1f 
   14000177f:	31 db                	xor    ebx,ebx
   140001781:	eb 2f                	jmp    1400017b2 <default_push()+0x52>
   140001783:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   14000178a:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   140001791:	00 00 00 00 
   140001795:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000179c:	00 00 00 00 
   1400017a0:	89 1e                	mov    DWORD PTR [rsi],ebx
   1400017a2:	83 c3 01             	add    ebx,0x1
   1400017a5:	48 83 c6 04          	add    rsi,0x4
   1400017a9:	83 fb 10             	cmp    ebx,0x10
   1400017ac:	0f 84 9e 00 00 00    	je     140001850 <default_push()+0xf0>
   1400017b2:	48 39 ee             	cmp    rsi,rbp
   1400017b5:	75 e9                	jne    1400017a0 <default_push()+0x40>
   1400017b7:	48 89 ee             	mov    rsi,rbp
   1400017ba:	4c 29 e6             	sub    rsi,r12
   1400017bd:	48 89 f2             	mov    rdx,rsi
   1400017c0:	48 c1 fa 02          	sar    rdx,0x2
   1400017c4:	4c 39 ea             	cmp    rdx,r13
   1400017c7:	0f 84 03 1f 00 00    	je     1400036d0 <default_push() [clone .cold]>
   1400017cd:	48 85 d2             	test   rdx,rdx
   1400017d0:	b8 01 00 00 00       	mov    eax,0x1
   1400017d5:	48 0f 45 c2          	cmovne rax,rdx
   1400017d9:	48 01 d0             	add    rax,rdx
   1400017dc:	48 ba ff ff ff ff ff 	movabs rdx,0x1fffffffffffffff
   1400017e3:	ff ff 1f 
   1400017e6:	48 39 d0             	cmp    rax,rdx
   1400017e9:	48 0f 47 c2          	cmova  rax,rdx
   1400017ed:	48 8d 3c 85 00 00 00 	lea    rdi,[rax*4+0x0]
   1400017f4:	00 
   1400017f5:	48 89 f9             	mov    rcx,rdi
   1400017f8:	e8 8b 02 00 00       	call   140001a88 <operator new(unsigned long long)>
   1400017fd:	89 1c 30             	mov    DWORD PTR [rax+rsi*1],ebx
   140001800:	49 89 c6             	mov    r14,rax
   140001803:	48 85 f6             	test   rsi,rsi
   140001806:	74 0e                	je     140001816 <default_push()+0xb6>
   140001808:	49 89 f0             	mov    r8,rsi
   14000180b:	4c 89 e2             	mov    rdx,r12
   14000180e:	48 89 c1             	mov    rcx,rax
   140001811:	e8 6a 1d 00 00       	call   140003580 <memcpy>
   140001816:	49 8d 74 36 04       	lea    rsi,[r14+rsi*1+0x4]
   14000181b:	4d 85 e4             	test   r12,r12
   14000181e:	74 0e                	je     14000182e <default_push()+0xce>
   140001820:	48 89 ea             	mov    rdx,rbp
   140001823:	4c 89 e1             	mov    rcx,r12
   140001826:	4c 29 e2             	sub    rdx,r12
   140001829:	e8 62 02 00 00       	call   140001a90 <operator delete(void*, unsigned long long)>
   14000182e:	83 c3 01             	add    ebx,0x1
   140001831:	49 8d 2c 3e          	lea    rbp,[r14+rdi*1]
   140001835:	4d 89 f4             	mov    r12,r14
   140001838:	83 fb 10             	cmp    ebx,0x10
   14000183b:	0f 85 71 ff ff ff    	jne    1400017b2 <default_push()+0x52>
   140001841:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   140001845:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000184c:	00 00 00 00 
   140001850:	4d 85 e4             	test   r12,r12
   140001853:	74 23                	je     140001878 <default_push()+0x118>
   140001855:	48 89 ea             	mov    rdx,rbp
   140001858:	4c 89 e1             	mov    rcx,r12
   14000185b:	4c 29 e2             	sub    rdx,r12
   14000185e:	48 83 c4 20          	add    rsp,0x20
   140001862:	5b                   	pop    rbx
   140001863:	5e                   	pop    rsi
   140001864:	5f                   	pop    rdi
   140001865:	5d                   	pop    rbp
   140001866:	41 5c                	pop    r12
   140001868:	41 5d                	pop    r13
   14000186a:	41 5e                	pop    r14
   14000186c:	e9 1f 02 00 00       	jmp    140001a90 <operator delete(void*, unsigned long long)>
   140001871:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   140001878:	48 83 c4 20          	add    rsp,0x20
   14000187c:	5b                   	pop    rbx
   14000187d:	5e                   	pop    rsi
   14000187e:	5f                   	pop    rdi
   14000187f:	5d                   	pop    rbp
   140001880:	41 5c                	pop    r12
   140001882:	41 5d                	pop    r13
   140001884:	41 5e                	pop    r14
   140001886:	c3                   	ret
   140001887:	e9 50 1e 00 00       	jmp    1400036dc <default_push() [clone .cold]+0xc>
   14000188c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000140001890 <pmr_push()>:
   140001890:	41 54                	push   r12
   140001892:	55                   	push   rbp
   140001893:	57                   	push   rdi
   140001894:	56                   	push   rsi
   140001895:	53                   	push   rbx
   140001896:	48 81 ec 90 04 00 00 	sub    rsp,0x490
   14000189d:	0f 29 b4 24 80 04 00 	movaps XMMWORD PTR [rsp+0x480],xmm6
   1400018a4:	00 
   1400018a5:	48 8b 05 d4 3a 00 00 	mov    rax,QWORD PTR [rip+0x3ad4]        # 140005380 <__fu0__ZTVNSt3pmr25monotonic_buffer_resourceE>
   1400018ac:	48 be ff ff ff ff ff 	movabs rsi,0x1fffffffffffffff
   1400018b3:	ff ff 1f 
   1400018b6:	48 83 c0 10          	add    rax,0x10
   1400018ba:	66 48 0f 6e f0       	movq   xmm6,rax
   1400018bf:	48 8d 9c 24 80 00 00 	lea    rbx,[rsp+0x80]
   1400018c6:	00 
   1400018c7:	66 48 0f 6e cb       	movq   xmm1,rbx
   1400018cc:	66 0f 6c f1          	punpcklqdq xmm6,xmm1
   1400018d0:	e8 db 01 00 00       	call   140001ab0 <std::pmr::get_default_resource()>
   1400018d5:	48 89 5c 24 68       	mov    QWORD PTR [rsp+0x68],rbx
   1400018da:	45 31 c0             	xor    r8d,r8d
   1400018dd:	45 31 c9             	xor    r9d,r9d
   1400018e0:	48 89 44 24 60       	mov    QWORD PTR [rsp+0x60],rax
   1400018e5:	45 31 db             	xor    r11d,r11d
   1400018e8:	45 31 d2             	xor    r10d,r10d
   1400018eb:	48 8d 5c 24 40       	lea    rbx,[rsp+0x40]
   1400018f0:	66 0f 6f 05 78 37 00 	movdqa xmm0,XMMWORD PTR [rip+0x3778]        # 140005070 <.rdata+0x20>
   1400018f7:	00 
   1400018f8:	0f 29 74 24 40       	movaps XMMWORD PTR [rsp+0x40],xmm6
   1400018fd:	48 c7 44 24 70 00 04 	mov    QWORD PTR [rsp+0x70],0x400
   140001904:	00 00 
   140001906:	48 c7 44 24 78 00 00 	mov    QWORD PTR [rsp+0x78],0x0
   14000190d:	00 00 
   14000190f:	0f 29 44 24 50       	movaps XMMWORD PTR [rsp+0x50],xmm0
   140001914:	eb 1f                	jmp    140001935 <pmr_push()+0xa5>
   140001916:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   14000191d:	00 00 00 
   140001920:	45 89 11             	mov    DWORD PTR [r9],r10d
   140001923:	41 83 c2 01          	add    r10d,0x1
   140001927:	49 83 c1 04          	add    r9,0x4
   14000192b:	41 83 fa 10          	cmp    r10d,0x10
   14000192f:	0f 84 d3 00 00 00    	je     140001a08 <pmr_push()+0x178>
   140001935:	4d 39 c8             	cmp    r8,r9
   140001938:	75 e6                	jne    140001920 <pmr_push()+0x90>
   14000193a:	4c 89 c7             	mov    rdi,r8
   14000193d:	4c 29 df             	sub    rdi,r11
   140001940:	48 89 fa             	mov    rdx,rdi
   140001943:	48 c1 fa 02          	sar    rdx,0x2
   140001947:	48 39 f2             	cmp    rdx,rsi
   14000194a:	0f 84 ab 1d 00 00    	je     1400036fb <pmr_push() [clone .cold]>
   140001950:	48 85 d2             	test   rdx,rdx
   140001953:	b8 01 00 00 00       	mov    eax,0x1
   140001958:	48 0f 45 c2          	cmovne rax,rdx
   14000195c:	48 01 d0             	add    rax,rdx
   14000195f:	48 ba ff ff ff ff ff 	movabs rdx,0x1fffffffffffffff
   140001966:	ff ff 1f 
   140001969:	48 39 d0             	cmp    rax,rdx
   14000196c:	48 0f 47 c2          	cmova  rax,rdx
   140001970:	48 8d 2c 85 00 00 00 	lea    rbp,[rax*4+0x0]
   140001977:	00 
   140001978:	48 8b 44 24 50       	mov    rax,QWORD PTR [rsp+0x50]
   14000197d:	48 39 e8             	cmp    rax,rbp
   140001980:	0f 82 aa 00 00 00    	jb     140001a30 <pmr_push()+0x1a0>
   140001986:	48 8b 4c 24 48       	mov    rcx,QWORD PTR [rsp+0x48]
   14000198b:	49 89 c4             	mov    r12,rax
   14000198e:	49 29 ec             	sub    r12,rbp
   140001991:	48 8d 51 03          	lea    rdx,[rcx+0x3]
   140001995:	48 83 e2 fc          	and    rdx,0xfffffffffffffffc
   140001999:	49 89 d0             	mov    r8,rdx
   14000199c:	49 29 c8             	sub    r8,rcx
   14000199f:	4d 39 c4             	cmp    r12,r8
   1400019a2:	0f 82 88 00 00 00    	jb     140001a30 <pmr_push()+0x1a0>
   1400019a8:	48 01 c8             	add    rax,rcx
   1400019ab:	48 89 54 24 48       	mov    QWORD PTR [rsp+0x48],rdx
   1400019b0:	48 29 d0             	sub    rax,rdx
   1400019b3:	48 89 44 24 50       	mov    QWORD PTR [rsp+0x50],rax
   1400019b8:	48 85 d2             	test   rdx,rdx
   1400019bb:	74 73                	je     140001a30 <pmr_push()+0x1a0>
   1400019bd:	4c 8d 04 2a          	lea    r8,[rdx+rbp*1]
   1400019c1:	48 29 e8             	sub    rax,rbp
   1400019c4:	4c 89 44 24 48       	mov    QWORD PTR [rsp+0x48],r8
   1400019c9:	48 89 44 24 50       	mov    QWORD PTR [rsp+0x50],rax
   1400019ce:	44 89 14 3a          	mov    DWORD PTR [rdx+rdi*1],r10d
   1400019d2:	4d 39 d9             	cmp    r9,r11
   1400019d5:	0f 84 95 00 00 00    	je     140001a70 <pmr_push()+0x1e0>
   1400019db:	4d 29 d9             	sub    r9,r11
   1400019de:	31 c0                	xor    eax,eax
   1400019e0:	41 8b 0c 03          	mov    ecx,DWORD PTR [r11+rax*1]
   1400019e4:	89 0c 02             	mov    DWORD PTR [rdx+rax*1],ecx
   1400019e7:	48 83 c0 04          	add    rax,0x4
   1400019eb:	4c 39 c8             	cmp    rax,r9
   1400019ee:	75 f0                	jne    1400019e0 <pmr_push()+0x150>
   1400019f0:	48 01 d0             	add    rax,rdx
   1400019f3:	41 83 c2 01          	add    r10d,0x1
   1400019f7:	4c 8d 48 04          	lea    r9,[rax+0x4]
   1400019fb:	49 89 d3             	mov    r11,rdx
   1400019fe:	41 83 fa 10          	cmp    r10d,0x10
   140001a02:	0f 85 2d ff ff ff    	jne    140001935 <pmr_push()+0xa5>
   140001a08:	48 89 d9             	mov    rcx,rbx
   140001a0b:	e8 90 00 00 00       	call   140001aa0 <std::pmr::monotonic_buffer_resource::~monotonic_buffer_resource()>
   140001a10:	90                   	nop
   140001a11:	0f 28 b4 24 80 04 00 	movaps xmm6,XMMWORD PTR [rsp+0x480]
   140001a18:	00 
   140001a19:	48 81 c4 90 04 00 00 	add    rsp,0x490
   140001a20:	5b                   	pop    rbx
   140001a21:	5e                   	pop    rsi
   140001a22:	5f                   	pop    rdi
   140001a23:	5d                   	pop    rbp
   140001a24:	41 5c                	pop    r12
   140001a26:	c3                   	ret
   140001a27:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   140001a2e:	00 00 
   140001a30:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001a36:	48 89 ea             	mov    rdx,rbp
   140001a39:	48 89 d9             	mov    rcx,rbx
   140001a3c:	4c 89 4c 24 38       	mov    QWORD PTR [rsp+0x38],r9
   140001a41:	4c 89 5c 24 30       	mov    QWORD PTR [rsp+0x30],r11
   140001a46:	44 89 54 24 2c       	mov    DWORD PTR [rsp+0x2c],r10d
   140001a4b:	e8 58 00 00 00       	call   140001aa8 <std::pmr::monotonic_buffer_resource::_M_new_buffer(unsigned long long, unsigned long long)>
   140001a50:	44 8b 54 24 2c       	mov    r10d,DWORD PTR [rsp+0x2c]
   140001a55:	4c 8b 5c 24 30       	mov    r11,QWORD PTR [rsp+0x30]
   140001a5a:	4c 8b 4c 24 38       	mov    r9,QWORD PTR [rsp+0x38]
   140001a5f:	48 8b 54 24 48       	mov    rdx,QWORD PTR [rsp+0x48]
   140001a64:	48 8b 44 24 50       	mov    rax,QWORD PTR [rsp+0x50]
   140001a69:	e9 4f ff ff ff       	jmp    1400019bd <pmr_push()+0x12d>
   140001a6e:	66 90                	xchg   ax,ax
   140001a70:	48 89 d0             	mov    rax,rdx
   140001a73:	e9 7b ff ff ff       	jmp    1400019f3 <pmr_push()+0x163>
   140001a78:	e9 8a 1c 00 00       	jmp    140003707 <pmr_push() [clone .cold]+0xc>
   140001a7d:	90                   	nop
   140001a7e:	90                   	nop
   140001a7f:	90                   	nop

0000000140001a80 <__gxx_personality_seh0>:
   140001a80:	ff 25 ca 87 00 00    	jmp    QWORD PTR [rip+0x87ca]        # 14000a250 <__imp___gxx_personality_seh0>
   140001a86:	90                   	nop
   140001a87:	90                   	nop

0000000140001a88 <operator new(unsigned long long)>:
   140001a88:	ff 25 ba 87 00 00    	jmp    QWORD PTR [rip+0x87ba]        # 14000a248 <__imp__Znwy>
   140001a8e:	90                   	nop
   140001a8f:	90                   	nop

0000000140001a90 <operator delete(void*, unsigned long long)>:
   140001a90:	ff 25 aa 87 00 00    	jmp    QWORD PTR [rip+0x87aa]        # 14000a240 <__imp__ZdlPvy>
   140001a96:	90                   	nop
   140001a97:	90                   	nop

0000000140001a98 <std::__throw_length_error(char const*)>:
   140001a98:	ff 25 92 87 00 00    	jmp    QWORD PTR [rip+0x8792]        # 14000a230 <__imp__ZSt20__throw_length_errorPKc>
   140001a9e:	90                   	nop
   140001a9f:	90                   	nop

0000000140001aa0 <std::pmr::monotonic_buffer_resource::~monotonic_buffer_resource()>:
   140001aa0:	ff 25 82 87 00 00    	jmp    QWORD PTR [rip+0x8782]        # 14000a228 <__imp__ZNSt3pmr25monotonic_buffer_resourceD1Ev>
   140001aa6:	90                   	nop
   140001aa7:	90                   	nop

0000000140001aa8 <std::pmr::monotonic_buffer_resource::_M_new_buffer(unsigned long long, unsigned long long)>:
   140001aa8:	ff 25 72 87 00 00    	jmp    QWORD PTR [rip+0x8772]        # 14000a220 <__imp__ZNSt3pmr25monotonic_buffer_resource13_M_new_bufferEyy>
   140001aae:	90                   	nop
   140001aaf:	90                   	nop

0000000140001ab0 <std::pmr::get_default_resource()>:
   140001ab0:	ff 25 62 87 00 00    	jmp    QWORD PTR [rip+0x8762]        # 14000a218 <__imp__ZNSt3pmr20get_default_resourceEv>
   140001ab6:	90                   	nop
   140001ab7:	90                   	nop
   140001ab8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   140001abf:	00 

0000000140001ac0 <__do_global_dtors>:
   140001ac0:	55                   	push   rbp
   140001ac1:	48 89 e5             	mov    rbp,rsp
   140001ac4:	48 83 ec 20          	sub    rsp,0x20
   140001ac8:	eb 1e                	jmp    140001ae8 <__do_global_dtors+0x28>
   140001aca:	48 8b 05 3f 25 00 00 	mov    rax,QWORD PTR [rip+0x253f]        # 140004010 <p.0>
   140001ad1:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001ad4:	ff d0                	call   rax
   140001ad6:	48 8b 05 33 25 00 00 	mov    rax,QWORD PTR [rip+0x2533]        # 140004010 <p.0>
   140001add:	48 83 c0 08          	add    rax,0x8
   140001ae1:	48 89 05 28 25 00 00 	mov    QWORD PTR [rip+0x2528],rax        # 140004010 <p.0>
   140001ae8:	48 8b 05 21 25 00 00 	mov    rax,QWORD PTR [rip+0x2521]        # 140004010 <p.0>
   140001aef:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001af2:	48 85 c0             	test   rax,rax
   140001af5:	75 d3                	jne    140001aca <__do_global_dtors+0xa>
   140001af7:	90                   	nop
   140001af8:	90                   	nop
   140001af9:	48 83 c4 20          	add    rsp,0x20
   140001afd:	5d                   	pop    rbp
   140001afe:	c3                   	ret

0000000140001aff <__do_global_ctors>:
   140001aff:	55                   	push   rbp
   140001b00:	48 89 e5             	mov    rbp,rsp
   140001b03:	48 83 ec 30          	sub    rsp,0x30
   140001b07:	48 8b 05 82 38 00 00 	mov    rax,QWORD PTR [rip+0x3882]        # 140005390 <.refptr.__CTOR_LIST__>
   140001b0e:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001b11:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140001b14:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
   140001b18:	75 25                	jne    140001b3f <__do_global_ctors+0x40>
   140001b1a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001b21:	eb 04                	jmp    140001b27 <__do_global_ctors+0x28>
   140001b23:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001b27:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b2a:	8d 50 01             	lea    edx,[rax+0x1]
   140001b2d:	48 8b 05 5c 38 00 00 	mov    rax,QWORD PTR [rip+0x385c]        # 140005390 <.refptr.__CTOR_LIST__>
   140001b34:	89 d2                	mov    edx,edx
   140001b36:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   140001b3a:	48 85 c0             	test   rax,rax
   140001b3d:	75 e4                	jne    140001b23 <__do_global_ctors+0x24>
   140001b3f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b42:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140001b45:	eb 14                	jmp    140001b5b <__do_global_ctors+0x5c>
   140001b47:	48 8b 05 42 38 00 00 	mov    rax,QWORD PTR [rip+0x3842]        # 140005390 <.refptr.__CTOR_LIST__>
   140001b4e:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140001b51:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   140001b55:	ff d0                	call   rax
   140001b57:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   140001b5b:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140001b5f:	75 e6                	jne    140001b47 <__do_global_ctors+0x48>
   140001b61:	48 8d 05 58 ff ff ff 	lea    rax,[rip+0xffffffffffffff58]        # 140001ac0 <__do_global_dtors>
   140001b68:	48 89 c1             	mov    rcx,rax
   140001b6b:	e8 bf fa ff ff       	call   14000162f <atexit>
   140001b70:	90                   	nop
   140001b71:	48 83 c4 30          	add    rsp,0x30
   140001b75:	5d                   	pop    rbp
   140001b76:	c3                   	ret

0000000140001b77 <__main>:
   140001b77:	55                   	push   rbp
   140001b78:	48 89 e5             	mov    rbp,rsp
   140001b7b:	48 83 ec 20          	sub    rsp,0x20
   140001b7f:	8b 05 fb 74 00 00    	mov    eax,DWORD PTR [rip+0x74fb]        # 140009080 <initialized>
   140001b85:	85 c0                	test   eax,eax
   140001b87:	75 0f                	jne    140001b98 <__main+0x21>
   140001b89:	c7 05 ed 74 00 00 01 	mov    DWORD PTR [rip+0x74ed],0x1        # 140009080 <initialized>
   140001b90:	00 00 00 
   140001b93:	e8 67 ff ff ff       	call   140001aff <__do_global_ctors>
   140001b98:	90                   	nop
   140001b99:	48 83 c4 20          	add    rsp,0x20
   140001b9d:	5d                   	pop    rbp
   140001b9e:	c3                   	ret
   140001b9f:	90                   	nop

0000000140001ba0 <_setargv>:
   140001ba0:	55                   	push   rbp
   140001ba1:	48 89 e5             	mov    rbp,rsp
   140001ba4:	b8 00 00 00 00       	mov    eax,0x0
   140001ba9:	5d                   	pop    rbp
   140001baa:	c3                   	ret
   140001bab:	90                   	nop
   140001bac:	90                   	nop
   140001bad:	90                   	nop
   140001bae:	90                   	nop
   140001baf:	90                   	nop

0000000140001bb0 <__dyn_tls_init>:
   140001bb0:	55                   	push   rbp
   140001bb1:	48 89 e5             	mov    rbp,rsp
   140001bb4:	48 83 ec 30          	sub    rsp,0x30
   140001bb8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001bbc:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001bbf:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001bc3:	48 8b 05 96 37 00 00 	mov    rax,QWORD PTR [rip+0x3796]        # 140005360 <.refptr._CRT_MT>
   140001bca:	8b 00                	mov    eax,DWORD PTR [rax]
   140001bcc:	83 f8 02             	cmp    eax,0x2
   140001bcf:	74 0d                	je     140001bde <__dyn_tls_init+0x2e>
   140001bd1:	48 8b 05 88 37 00 00 	mov    rax,QWORD PTR [rip+0x3788]        # 140005360 <.refptr._CRT_MT>
   140001bd8:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   140001bde:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140001be2:	74 1e                	je     140001c02 <__dyn_tls_init+0x52>
   140001be4:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140001be8:	75 5b                	jne    140001c45 <__dyn_tls_init+0x95>
   140001bea:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001bee:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   140001bf1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001bf5:	49 89 c8             	mov    r8,rcx
   140001bf8:	48 89 c1             	mov    rcx,rax
   140001bfb:	e8 d1 11 00 00       	call   140002dd1 <__mingw_TLScallback>
   140001c00:	eb 43                	jmp    140001c45 <__dyn_tls_init+0x95>
   140001c02:	48 8d 05 e7 3a 00 00 	lea    rax,[rip+0x3ae7]        # 1400056f0 <___crt_xd_start__>
   140001c09:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001c0d:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001c12:	eb 22                	jmp    140001c36 <__dyn_tls_init+0x86>
   140001c14:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001c18:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001c1c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c20:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001c23:	48 85 c0             	test   rax,rax
   140001c26:	74 09                	je     140001c31 <__dyn_tls_init+0x81>
   140001c28:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c2c:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001c2f:	ff d0                	call   rax
   140001c31:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001c36:	48 8d 05 bb 3a 00 00 	lea    rax,[rip+0x3abb]        # 1400056f8 <__xd_z>
   140001c3d:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140001c41:	75 d1                	jne    140001c14 <__dyn_tls_init+0x64>
   140001c43:	eb 01                	jmp    140001c46 <__dyn_tls_init+0x96>
   140001c45:	90                   	nop
   140001c46:	48 83 c4 30          	add    rsp,0x30
   140001c4a:	5d                   	pop    rbp
   140001c4b:	c3                   	ret

0000000140001c4c <__tlregdtor>:
   140001c4c:	55                   	push   rbp
   140001c4d:	48 89 e5             	mov    rbp,rsp
   140001c50:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001c54:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140001c59:	75 07                	jne    140001c62 <__tlregdtor+0x16>
   140001c5b:	b8 00 00 00 00       	mov    eax,0x0
   140001c60:	eb 05                	jmp    140001c67 <__tlregdtor+0x1b>
   140001c62:	b8 00 00 00 00       	mov    eax,0x0
   140001c67:	5d                   	pop    rbp
   140001c68:	c3                   	ret

0000000140001c69 <__dyn_tls_dtor>:
   140001c69:	55                   	push   rbp
   140001c6a:	48 89 e5             	mov    rbp,rsp
   140001c6d:	48 83 ec 20          	sub    rsp,0x20
   140001c71:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001c75:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001c78:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001c7c:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140001c80:	74 06                	je     140001c88 <__dyn_tls_dtor+0x1f>
   140001c82:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140001c86:	75 18                	jne    140001ca0 <__dyn_tls_dtor+0x37>
   140001c88:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001c8c:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   140001c8f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001c93:	49 89 c8             	mov    r8,rcx
   140001c96:	48 89 c1             	mov    rcx,rax
   140001c99:	e8 33 11 00 00       	call   140002dd1 <__mingw_TLScallback>
   140001c9e:	eb 01                	jmp    140001ca1 <__dyn_tls_dtor+0x38>
   140001ca0:	90                   	nop
   140001ca1:	48 83 c4 20          	add    rsp,0x20
   140001ca5:	5d                   	pop    rbp
   140001ca6:	c3                   	ret
   140001ca7:	90                   	nop
   140001ca8:	90                   	nop
   140001ca9:	90                   	nop
   140001caa:	90                   	nop
   140001cab:	90                   	nop
   140001cac:	90                   	nop
   140001cad:	90                   	nop
   140001cae:	90                   	nop
   140001caf:	90                   	nop

0000000140001cb0 <_matherr>:
   140001cb0:	55                   	push   rbp
   140001cb1:	53                   	push   rbx
   140001cb2:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140001cb9:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140001cbe:	0f 29 75 00          	movaps XMMWORD PTR [rbp+0x0],xmm6
   140001cc2:	0f 29 7d 10          	movaps XMMWORD PTR [rbp+0x10],xmm7
   140001cc6:	44 0f 29 45 20       	movaps XMMWORD PTR [rbp+0x20],xmm8
   140001ccb:	48 89 4d 50          	mov    QWORD PTR [rbp+0x50],rcx
   140001ccf:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001cd3:	8b 00                	mov    eax,DWORD PTR [rax]
   140001cd5:	83 f8 06             	cmp    eax,0x6
   140001cd8:	74 56                	je     140001d30 <_matherr+0x80>
   140001cda:	83 f8 06             	cmp    eax,0x6
   140001cdd:	7f 78                	jg     140001d57 <_matherr+0xa7>
   140001cdf:	83 f8 05             	cmp    eax,0x5
   140001ce2:	74 59                	je     140001d3d <_matherr+0x8d>
   140001ce4:	83 f8 05             	cmp    eax,0x5
   140001ce7:	7f 6e                	jg     140001d57 <_matherr+0xa7>
   140001ce9:	83 f8 04             	cmp    eax,0x4
   140001cec:	74 5c                	je     140001d4a <_matherr+0x9a>
   140001cee:	83 f8 04             	cmp    eax,0x4
   140001cf1:	7f 64                	jg     140001d57 <_matherr+0xa7>
   140001cf3:	83 f8 03             	cmp    eax,0x3
   140001cf6:	74 2b                	je     140001d23 <_matherr+0x73>
   140001cf8:	83 f8 03             	cmp    eax,0x3
   140001cfb:	7f 5a                	jg     140001d57 <_matherr+0xa7>
   140001cfd:	83 f8 01             	cmp    eax,0x1
   140001d00:	74 07                	je     140001d09 <_matherr+0x59>
   140001d02:	83 f8 02             	cmp    eax,0x2
   140001d05:	74 0f                	je     140001d16 <_matherr+0x66>
   140001d07:	eb 4e                	jmp    140001d57 <_matherr+0xa7>
   140001d09:	48 8d 05 b0 33 00 00 	lea    rax,[rip+0x33b0]        # 1400050c0 <.rdata>
   140001d10:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001d14:	eb 4d                	jmp    140001d63 <_matherr+0xb3>
   140001d16:	48 8d 05 c2 33 00 00 	lea    rax,[rip+0x33c2]        # 1400050df <.rdata+0x1f>
   140001d1d:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001d21:	eb 40                	jmp    140001d63 <_matherr+0xb3>
   140001d23:	48 8d 05 d6 33 00 00 	lea    rax,[rip+0x33d6]        # 140005100 <.rdata+0x40>
   140001d2a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001d2e:	eb 33                	jmp    140001d63 <_matherr+0xb3>
   140001d30:	48 8d 05 e9 33 00 00 	lea    rax,[rip+0x33e9]        # 140005120 <.rdata+0x60>
   140001d37:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001d3b:	eb 26                	jmp    140001d63 <_matherr+0xb3>
   140001d3d:	48 8d 05 04 34 00 00 	lea    rax,[rip+0x3404]        # 140005148 <.rdata+0x88>
   140001d44:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001d48:	eb 19                	jmp    140001d63 <_matherr+0xb3>
   140001d4a:	48 8d 05 1f 34 00 00 	lea    rax,[rip+0x341f]        # 140005170 <.rdata+0xb0>
   140001d51:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001d55:	eb 0c                	jmp    140001d63 <_matherr+0xb3>
   140001d57:	48 8d 05 48 34 00 00 	lea    rax,[rip+0x3448]        # 1400051a6 <.rdata+0xe6>
   140001d5e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001d62:	90                   	nop
   140001d63:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001d67:	f2 44 0f 10 40 20    	movsd  xmm8,QWORD PTR [rax+0x20]
   140001d6d:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001d71:	f2 0f 10 78 18       	movsd  xmm7,QWORD PTR [rax+0x18]
   140001d76:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001d7a:	f2 0f 10 70 10       	movsd  xmm6,QWORD PTR [rax+0x10]
   140001d7f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001d83:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
   140001d87:	b9 02 00 00 00       	mov    ecx,0x2
   140001d8c:	e8 3f 17 00 00       	call   1400034d0 <__acrt_iob_func>
   140001d91:	48 89 c1             	mov    rcx,rax
   140001d94:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140001d98:	48 8d 05 19 34 00 00 	lea    rax,[rip+0x3419]        # 1400051b8 <.rdata+0xf8>
   140001d9f:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001da6:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001dac:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001db2:	49 89 d9             	mov    r9,rbx
   140001db5:	49 89 d0             	mov    r8,rdx
   140001db8:	48 89 c2             	mov    rdx,rax
   140001dbb:	e8 a8 17 00 00       	call   140003568 <fprintf>
   140001dc0:	b8 00 00 00 00       	mov    eax,0x0
   140001dc5:	0f 28 75 00          	movaps xmm6,XMMWORD PTR [rbp+0x0]
   140001dc9:	0f 28 7d 10          	movaps xmm7,XMMWORD PTR [rbp+0x10]
   140001dcd:	44 0f 28 45 20       	movaps xmm8,XMMWORD PTR [rbp+0x20]
   140001dd2:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140001dd9:	5b                   	pop    rbx
   140001dda:	5d                   	pop    rbp
   140001ddb:	c3                   	ret
   140001ddc:	90                   	nop
   140001ddd:	90                   	nop
   140001dde:	90                   	nop
   140001ddf:	90                   	nop

0000000140001de0 <__report_error>:
   140001de0:	55                   	push   rbp
   140001de1:	53                   	push   rbx
   140001de2:	48 83 ec 38          	sub    rsp,0x38
   140001de6:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140001deb:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140001def:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001df3:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140001df7:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140001dfb:	48 8d 45 28          	lea    rax,[rbp+0x28]
   140001dff:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001e03:	b9 02 00 00 00       	mov    ecx,0x2
   140001e08:	e8 c3 16 00 00       	call   1400034d0 <__acrt_iob_func>
   140001e0d:	48 89 c1             	mov    rcx,rax
   140001e10:	48 8d 05 d9 33 00 00 	lea    rax,[rip+0x33d9]        # 1400051f0 <.rdata>
   140001e17:	48 89 c2             	mov    rdx,rax
   140001e1a:	e8 49 17 00 00       	call   140003568 <fprintf>
   140001e1f:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   140001e23:	b9 02 00 00 00       	mov    ecx,0x2
   140001e28:	e8 a3 16 00 00       	call   1400034d0 <__acrt_iob_func>
   140001e2d:	48 89 c1             	mov    rcx,rax
   140001e30:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001e34:	49 89 d8             	mov    r8,rbx
   140001e37:	48 89 c2             	mov    rdx,rax
   140001e3a:	e8 69 17 00 00       	call   1400035a8 <vfprintf>
   140001e3f:	e8 04 17 00 00       	call   140003548 <abort>
   140001e44:	90                   	nop

0000000140001e45 <mark_section_writable>:
   140001e45:	55                   	push   rbp
   140001e46:	48 89 e5             	mov    rbp,rsp
   140001e49:	48 83 ec 60          	sub    rsp,0x60
   140001e4d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001e51:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001e58:	e9 82 00 00 00       	jmp    140001edf <mark_section_writable+0x9a>
   140001e5d:	48 8b 0d 7c 72 00 00 	mov    rcx,QWORD PTR [rip+0x727c]        # 1400090e0 <the_secs>
   140001e64:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e67:	48 63 d0             	movsxd rdx,eax
   140001e6a:	48 89 d0             	mov    rax,rdx
   140001e6d:	48 c1 e0 02          	shl    rax,0x2
   140001e71:	48 01 d0             	add    rax,rdx
   140001e74:	48 c1 e0 03          	shl    rax,0x3
   140001e78:	48 01 c8             	add    rax,rcx
   140001e7b:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001e7f:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001e83:	72 56                	jb     140001edb <mark_section_writable+0x96>
   140001e85:	48 8b 0d 54 72 00 00 	mov    rcx,QWORD PTR [rip+0x7254]        # 1400090e0 <the_secs>
   140001e8c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e8f:	48 63 d0             	movsxd rdx,eax
   140001e92:	48 89 d0             	mov    rax,rdx
   140001e95:	48 c1 e0 02          	shl    rax,0x2
   140001e99:	48 01 d0             	add    rax,rdx
   140001e9c:	48 c1 e0 03          	shl    rax,0x3
   140001ea0:	48 01 c8             	add    rax,rcx
   140001ea3:	48 8b 48 18          	mov    rcx,QWORD PTR [rax+0x18]
   140001ea7:	4c 8b 05 32 72 00 00 	mov    r8,QWORD PTR [rip+0x7232]        # 1400090e0 <the_secs>
   140001eae:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001eb1:	48 63 d0             	movsxd rdx,eax
   140001eb4:	48 89 d0             	mov    rax,rdx
   140001eb7:	48 c1 e0 02          	shl    rax,0x2
   140001ebb:	48 01 d0             	add    rax,rdx
   140001ebe:	48 c1 e0 03          	shl    rax,0x3
   140001ec2:	4c 01 c0             	add    rax,r8
   140001ec5:	48 8b 40 20          	mov    rax,QWORD PTR [rax+0x20]
   140001ec9:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001ecc:	89 c0                	mov    eax,eax
   140001ece:	48 01 c8             	add    rax,rcx
   140001ed1:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001ed5:	0f 82 41 02 00 00    	jb     14000211c <mark_section_writable+0x2d7>
   140001edb:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001edf:	8b 05 03 72 00 00    	mov    eax,DWORD PTR [rip+0x7203]        # 1400090e8 <maxSections>
   140001ee5:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001ee8:	0f 8c 6f ff ff ff    	jl     140001e5d <mark_section_writable+0x18>
   140001eee:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001ef2:	48 89 c1             	mov    rcx,rax
   140001ef5:	e8 c1 11 00 00       	call   1400030bb <__mingw_GetSectionForAddress>
   140001efa:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001efe:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001f03:	75 13                	jne    140001f18 <mark_section_writable+0xd3>
   140001f05:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f09:	48 8d 0d 00 33 00 00 	lea    rcx,[rip+0x3300]        # 140005210 <.rdata+0x20>
   140001f10:	48 89 c2             	mov    rdx,rax
   140001f13:	e8 c8 fe ff ff       	call   140001de0 <__report_error>
   140001f18:	48 8b 0d c1 71 00 00 	mov    rcx,QWORD PTR [rip+0x71c1]        # 1400090e0 <the_secs>
   140001f1f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001f22:	48 63 d0             	movsxd rdx,eax
   140001f25:	48 89 d0             	mov    rax,rdx
   140001f28:	48 c1 e0 02          	shl    rax,0x2
   140001f2c:	48 01 d0             	add    rax,rdx
   140001f2f:	48 c1 e0 03          	shl    rax,0x3
   140001f33:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001f37:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001f3b:	48 89 42 20          	mov    QWORD PTR [rdx+0x20],rax
   140001f3f:	48 8b 0d 9a 71 00 00 	mov    rcx,QWORD PTR [rip+0x719a]        # 1400090e0 <the_secs>
   140001f46:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001f49:	48 63 d0             	movsxd rdx,eax
   140001f4c:	48 89 d0             	mov    rax,rdx
   140001f4f:	48 c1 e0 02          	shl    rax,0x2
   140001f53:	48 01 d0             	add    rax,rdx
   140001f56:	48 c1 e0 03          	shl    rax,0x3
   140001f5a:	48 01 c8             	add    rax,rcx
   140001f5d:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001f63:	e8 9f 12 00 00       	call   140003207 <_GetPEImageBase>
   140001f68:	48 89 c1             	mov    rcx,rax
   140001f6b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001f6f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140001f72:	41 89 c1             	mov    r9d,eax
   140001f75:	4c 8b 05 64 71 00 00 	mov    r8,QWORD PTR [rip+0x7164]        # 1400090e0 <the_secs>
   140001f7c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001f7f:	48 63 d0             	movsxd rdx,eax
   140001f82:	48 89 d0             	mov    rax,rdx
   140001f85:	48 c1 e0 02          	shl    rax,0x2
   140001f89:	48 01 d0             	add    rax,rdx
   140001f8c:	48 c1 e0 03          	shl    rax,0x3
   140001f90:	4c 01 c0             	add    rax,r8
   140001f93:	4a 8d 14 09          	lea    rdx,[rcx+r9*1]
   140001f97:	48 89 50 18          	mov    QWORD PTR [rax+0x18],rdx
   140001f9b:	48 8b 0d 3e 71 00 00 	mov    rcx,QWORD PTR [rip+0x713e]        # 1400090e0 <the_secs>
   140001fa2:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001fa5:	48 63 d0             	movsxd rdx,eax
   140001fa8:	48 89 d0             	mov    rax,rdx
   140001fab:	48 c1 e0 02          	shl    rax,0x2
   140001faf:	48 01 d0             	add    rax,rdx
   140001fb2:	48 c1 e0 03          	shl    rax,0x3
   140001fb6:	48 01 c8             	add    rax,rcx
   140001fb9:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001fbd:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140001fc1:	41 b8 30 00 00 00    	mov    r8d,0x30
   140001fc7:	48 89 c1             	mov    rcx,rax
   140001fca:	48 8b 05 f7 82 00 00 	mov    rax,QWORD PTR [rip+0x82f7]        # 14000a2c8 <__imp_VirtualQuery>
   140001fd1:	ff d0                	call   rax
   140001fd3:	48 85 c0             	test   rax,rax
   140001fd6:	75 3f                	jne    140002017 <mark_section_writable+0x1d2>
   140001fd8:	48 8b 0d 01 71 00 00 	mov    rcx,QWORD PTR [rip+0x7101]        # 1400090e0 <the_secs>
   140001fdf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001fe2:	48 63 d0             	movsxd rdx,eax
   140001fe5:	48 89 d0             	mov    rax,rdx
   140001fe8:	48 c1 e0 02          	shl    rax,0x2
   140001fec:	48 01 d0             	add    rax,rdx
   140001fef:	48 c1 e0 03          	shl    rax,0x3
   140001ff3:	48 01 c8             	add    rax,rcx
   140001ff6:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
   140001ffa:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001ffe:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002001:	89 c1                	mov    ecx,eax
   140002003:	48 8d 05 26 32 00 00 	lea    rax,[rip+0x3226]        # 140005230 <.rdata+0x40>
   14000200a:	49 89 d0             	mov    r8,rdx
   14000200d:	89 ca                	mov    edx,ecx
   14000200f:	48 89 c1             	mov    rcx,rax
   140002012:	e8 c9 fd ff ff       	call   140001de0 <__report_error>
   140002017:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   14000201a:	83 f8 40             	cmp    eax,0x40
   14000201d:	0f 84 e8 00 00 00    	je     14000210b <mark_section_writable+0x2c6>
   140002023:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140002026:	83 f8 04             	cmp    eax,0x4
   140002029:	0f 84 dc 00 00 00    	je     14000210b <mark_section_writable+0x2c6>
   14000202f:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140002032:	3d 80 00 00 00       	cmp    eax,0x80
   140002037:	0f 84 ce 00 00 00    	je     14000210b <mark_section_writable+0x2c6>
   14000203d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140002040:	83 f8 08             	cmp    eax,0x8
   140002043:	0f 84 c2 00 00 00    	je     14000210b <mark_section_writable+0x2c6>
   140002049:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   14000204c:	83 f8 02             	cmp    eax,0x2
   14000204f:	75 09                	jne    14000205a <mark_section_writable+0x215>
   140002051:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140002058:	eb 07                	jmp    140002061 <mark_section_writable+0x21c>
   14000205a:	c7 45 f8 40 00 00 00 	mov    DWORD PTR [rbp-0x8],0x40
   140002061:	48 8b 0d 78 70 00 00 	mov    rcx,QWORD PTR [rip+0x7078]        # 1400090e0 <the_secs>
   140002068:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000206b:	48 63 d0             	movsxd rdx,eax
   14000206e:	48 89 d0             	mov    rax,rdx
   140002071:	48 c1 e0 02          	shl    rax,0x2
   140002075:	48 01 d0             	add    rax,rdx
   140002078:	48 c1 e0 03          	shl    rax,0x3
   14000207c:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140002080:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140002084:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   140002088:	48 8b 0d 51 70 00 00 	mov    rcx,QWORD PTR [rip+0x7051]        # 1400090e0 <the_secs>
   14000208f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002092:	48 63 d0             	movsxd rdx,eax
   140002095:	48 89 d0             	mov    rax,rdx
   140002098:	48 c1 e0 02          	shl    rax,0x2
   14000209c:	48 01 d0             	add    rax,rdx
   14000209f:	48 c1 e0 03          	shl    rax,0x3
   1400020a3:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   1400020a7:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   1400020ab:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   1400020af:	48 8b 0d 2a 70 00 00 	mov    rcx,QWORD PTR [rip+0x702a]        # 1400090e0 <the_secs>
   1400020b6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400020b9:	48 63 d0             	movsxd rdx,eax
   1400020bc:	48 89 d0             	mov    rax,rdx
   1400020bf:	48 c1 e0 02          	shl    rax,0x2
   1400020c3:	48 01 d0             	add    rax,rdx
   1400020c6:	48 c1 e0 03          	shl    rax,0x3
   1400020ca:	48 01 c8             	add    rax,rcx
   1400020cd:	49 89 c0             	mov    r8,rax
   1400020d0:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   1400020d4:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   1400020d8:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   1400020db:	4d 89 c1             	mov    r9,r8
   1400020de:	41 89 c8             	mov    r8d,ecx
   1400020e1:	48 89 c1             	mov    rcx,rax
   1400020e4:	48 8b 05 d5 81 00 00 	mov    rax,QWORD PTR [rip+0x81d5]        # 14000a2c0 <__imp_VirtualProtect>
   1400020eb:	ff d0                	call   rax
   1400020ed:	85 c0                	test   eax,eax
   1400020ef:	75 1a                	jne    14000210b <mark_section_writable+0x2c6>
   1400020f1:	48 8b 05 80 81 00 00 	mov    rax,QWORD PTR [rip+0x8180]        # 14000a278 <__imp_GetLastError>
   1400020f8:	ff d0                	call   rax
   1400020fa:	89 c2                	mov    edx,eax
   1400020fc:	48 8d 05 65 31 00 00 	lea    rax,[rip+0x3165]        # 140005268 <.rdata+0x78>
   140002103:	48 89 c1             	mov    rcx,rax
   140002106:	e8 d5 fc ff ff       	call   140001de0 <__report_error>
   14000210b:	8b 05 d7 6f 00 00    	mov    eax,DWORD PTR [rip+0x6fd7]        # 1400090e8 <maxSections>
   140002111:	83 c0 01             	add    eax,0x1
   140002114:	89 05 ce 6f 00 00    	mov    DWORD PTR [rip+0x6fce],eax        # 1400090e8 <maxSections>
   14000211a:	eb 01                	jmp    14000211d <mark_section_writable+0x2d8>
   14000211c:	90                   	nop
   14000211d:	48 83 c4 60          	add    rsp,0x60
   140002121:	5d                   	pop    rbp
   140002122:	c3                   	ret

0000000140002123 <restore_modified_sections>:
   140002123:	55                   	push   rbp
   140002124:	48 89 e5             	mov    rbp,rsp
   140002127:	48 83 ec 30          	sub    rsp,0x30
   14000212b:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002132:	e9 ad 00 00 00       	jmp    1400021e4 <restore_modified_sections+0xc1>
   140002137:	48 8b 0d a2 6f 00 00 	mov    rcx,QWORD PTR [rip+0x6fa2]        # 1400090e0 <the_secs>
   14000213e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002141:	48 63 d0             	movsxd rdx,eax
   140002144:	48 89 d0             	mov    rax,rdx
   140002147:	48 c1 e0 02          	shl    rax,0x2
   14000214b:	48 01 d0             	add    rax,rdx
   14000214e:	48 c1 e0 03          	shl    rax,0x3
   140002152:	48 01 c8             	add    rax,rcx
   140002155:	8b 00                	mov    eax,DWORD PTR [rax]
   140002157:	85 c0                	test   eax,eax
   140002159:	0f 84 80 00 00 00    	je     1400021df <restore_modified_sections+0xbc>
   14000215f:	48 8b 0d 7a 6f 00 00 	mov    rcx,QWORD PTR [rip+0x6f7a]        # 1400090e0 <the_secs>
   140002166:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002169:	48 63 d0             	movsxd rdx,eax
   14000216c:	48 89 d0             	mov    rax,rdx
   14000216f:	48 c1 e0 02          	shl    rax,0x2
   140002173:	48 01 d0             	add    rax,rdx
   140002176:	48 c1 e0 03          	shl    rax,0x3
   14000217a:	48 01 c8             	add    rax,rcx
   14000217d:	44 8b 10             	mov    r10d,DWORD PTR [rax]
   140002180:	48 8b 0d 59 6f 00 00 	mov    rcx,QWORD PTR [rip+0x6f59]        # 1400090e0 <the_secs>
   140002187:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000218a:	48 63 d0             	movsxd rdx,eax
   14000218d:	48 89 d0             	mov    rax,rdx
   140002190:	48 c1 e0 02          	shl    rax,0x2
   140002194:	48 01 d0             	add    rax,rdx
   140002197:	48 c1 e0 03          	shl    rax,0x3
   14000219b:	48 01 c8             	add    rax,rcx
   14000219e:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   1400021a2:	4c 8b 05 37 6f 00 00 	mov    r8,QWORD PTR [rip+0x6f37]        # 1400090e0 <the_secs>
   1400021a9:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400021ac:	48 63 d0             	movsxd rdx,eax
   1400021af:	48 89 d0             	mov    rax,rdx
   1400021b2:	48 c1 e0 02          	shl    rax,0x2
   1400021b6:	48 01 d0             	add    rax,rdx
   1400021b9:	48 c1 e0 03          	shl    rax,0x3
   1400021bd:	4c 01 c0             	add    rax,r8
   1400021c0:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   1400021c4:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   1400021c8:	49 89 d1             	mov    r9,rdx
   1400021cb:	45 89 d0             	mov    r8d,r10d
   1400021ce:	48 89 ca             	mov    rdx,rcx
   1400021d1:	48 89 c1             	mov    rcx,rax
   1400021d4:	48 8b 05 e5 80 00 00 	mov    rax,QWORD PTR [rip+0x80e5]        # 14000a2c0 <__imp_VirtualProtect>
   1400021db:	ff d0                	call   rax
   1400021dd:	eb 01                	jmp    1400021e0 <restore_modified_sections+0xbd>
   1400021df:	90                   	nop
   1400021e0:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   1400021e4:	8b 05 fe 6e 00 00    	mov    eax,DWORD PTR [rip+0x6efe]        # 1400090e8 <maxSections>
   1400021ea:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   1400021ed:	0f 8c 44 ff ff ff    	jl     140002137 <restore_modified_sections+0x14>
   1400021f3:	90                   	nop
   1400021f4:	90                   	nop
   1400021f5:	48 83 c4 30          	add    rsp,0x30
   1400021f9:	5d                   	pop    rbp
   1400021fa:	c3                   	ret

00000001400021fb <__write_memory>:
   1400021fb:	55                   	push   rbp
   1400021fc:	48 89 e5             	mov    rbp,rsp
   1400021ff:	48 83 ec 20          	sub    rsp,0x20
   140002203:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002207:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000220b:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   14000220f:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140002214:	74 25                	je     14000223b <__write_memory+0x40>
   140002216:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000221a:	48 89 c1             	mov    rcx,rax
   14000221d:	e8 23 fc ff ff       	call   140001e45 <mark_section_writable>
   140002222:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140002226:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   14000222a:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000222e:	49 89 c8             	mov    r8,rcx
   140002231:	48 89 c1             	mov    rcx,rax
   140002234:	e8 47 13 00 00       	call   140003580 <memcpy>
   140002239:	eb 01                	jmp    14000223c <__write_memory+0x41>
   14000223b:	90                   	nop
   14000223c:	48 83 c4 20          	add    rsp,0x20
   140002240:	5d                   	pop    rbp
   140002241:	c3                   	ret

0000000140002242 <do_pseudo_reloc>:
   140002242:	55                   	push   rbp
   140002243:	48 89 e5             	mov    rbp,rsp
   140002246:	48 83 c4 80          	add    rsp,0xffffffffffffff80
   14000224a:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000224e:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002252:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002256:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000225a:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   14000225e:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002262:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002266:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000226a:	48 83 7d e0 07       	cmp    QWORD PTR [rbp-0x20],0x7
   14000226f:	0f 8e 44 03 00 00    	jle    1400025b9 <do_pseudo_reloc+0x377>
   140002275:	48 83 7d e0 0b       	cmp    QWORD PTR [rbp-0x20],0xb
   14000227a:	7e 25                	jle    1400022a1 <do_pseudo_reloc+0x5f>
   14000227c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002280:	8b 00                	mov    eax,DWORD PTR [rax]
   140002282:	85 c0                	test   eax,eax
   140002284:	75 1b                	jne    1400022a1 <do_pseudo_reloc+0x5f>
   140002286:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000228a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000228d:	85 c0                	test   eax,eax
   14000228f:	75 10                	jne    1400022a1 <do_pseudo_reloc+0x5f>
   140002291:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002295:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002298:	85 c0                	test   eax,eax
   14000229a:	75 05                	jne    1400022a1 <do_pseudo_reloc+0x5f>
   14000229c:	48 83 45 f8 0c       	add    QWORD PTR [rbp-0x8],0xc
   1400022a1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400022a5:	8b 00                	mov    eax,DWORD PTR [rax]
   1400022a7:	85 c0                	test   eax,eax
   1400022a9:	75 0b                	jne    1400022b6 <do_pseudo_reloc+0x74>
   1400022ab:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400022af:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400022b2:	85 c0                	test   eax,eax
   1400022b4:	74 59                	je     14000230f <do_pseudo_reloc+0xcd>
   1400022b6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400022ba:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400022be:	eb 40                	jmp    140002300 <do_pseudo_reloc+0xbe>
   1400022c0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400022c4:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400022c7:	89 c2                	mov    edx,eax
   1400022c9:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400022cd:	48 01 d0             	add    rax,rdx
   1400022d0:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400022d4:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400022d8:	8b 10                	mov    edx,DWORD PTR [rax]
   1400022da:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400022de:	8b 00                	mov    eax,DWORD PTR [rax]
   1400022e0:	01 d0                	add    eax,edx
   1400022e2:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
   1400022e5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400022e9:	48 8d 55 b4          	lea    rdx,[rbp-0x4c]
   1400022ed:	41 b8 04 00 00 00    	mov    r8d,0x4
   1400022f3:	48 89 c1             	mov    rcx,rax
   1400022f6:	e8 00 ff ff ff       	call   1400021fb <__write_memory>
   1400022fb:	48 83 45 e8 08       	add    QWORD PTR [rbp-0x18],0x8
   140002300:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002304:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140002308:	72 b6                	jb     1400022c0 <do_pseudo_reloc+0x7e>
   14000230a:	e9 ab 02 00 00       	jmp    1400025ba <do_pseudo_reloc+0x378>
   14000230f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002313:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002316:	83 f8 01             	cmp    eax,0x1
   140002319:	74 18                	je     140002333 <do_pseudo_reloc+0xf1>
   14000231b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000231f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002322:	89 c2                	mov    edx,eax
   140002324:	48 8d 05 65 2f 00 00 	lea    rax,[rip+0x2f65]        # 140005290 <.rdata+0xa0>
   14000232b:	48 89 c1             	mov    rcx,rax
   14000232e:	e8 ad fa ff ff       	call   140001de0 <__report_error>
   140002333:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002337:	48 83 c0 0c          	add    rax,0xc
   14000233b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000233f:	e9 65 02 00 00       	jmp    1400025a9 <do_pseudo_reloc+0x367>
   140002344:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002348:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000234b:	89 c2                	mov    edx,eax
   14000234d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002351:	48 01 d0             	add    rax,rdx
   140002354:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002358:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000235c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000235e:	89 c2                	mov    edx,eax
   140002360:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002364:	48 01 d0             	add    rax,rdx
   140002367:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000236b:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000236f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002372:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002376:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000237a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000237d:	0f b6 c0             	movzx  eax,al
   140002380:	83 f8 40             	cmp    eax,0x40
   140002383:	0f 84 b6 00 00 00    	je     14000243f <do_pseudo_reloc+0x1fd>
   140002389:	83 f8 40             	cmp    eax,0x40
   14000238c:	0f 87 ba 00 00 00    	ja     14000244c <do_pseudo_reloc+0x20a>
   140002392:	83 f8 20             	cmp    eax,0x20
   140002395:	74 77                	je     14000240e <do_pseudo_reloc+0x1cc>
   140002397:	83 f8 20             	cmp    eax,0x20
   14000239a:	0f 87 ac 00 00 00    	ja     14000244c <do_pseudo_reloc+0x20a>
   1400023a0:	83 f8 08             	cmp    eax,0x8
   1400023a3:	74 0a                	je     1400023af <do_pseudo_reloc+0x16d>
   1400023a5:	83 f8 10             	cmp    eax,0x10
   1400023a8:	74 38                	je     1400023e2 <do_pseudo_reloc+0x1a0>
   1400023aa:	e9 9d 00 00 00       	jmp    14000244c <do_pseudo_reloc+0x20a>
   1400023af:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400023b3:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400023b6:	0f b6 c0             	movzx  eax,al
   1400023b9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400023bd:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400023c1:	25 80 00 00 00       	and    eax,0x80
   1400023c6:	48 85 c0             	test   rax,rax
   1400023c9:	0f 84 9d 00 00 00    	je     14000246c <do_pseudo_reloc+0x22a>
   1400023cf:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400023d3:	48 0d 00 ff ff ff    	or     rax,0xffffffffffffff00
   1400023d9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400023dd:	e9 8a 00 00 00       	jmp    14000246c <do_pseudo_reloc+0x22a>
   1400023e2:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400023e6:	0f b7 00             	movzx  eax,WORD PTR [rax]
   1400023e9:	0f b7 c0             	movzx  eax,ax
   1400023ec:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400023f0:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400023f4:	25 00 80 00 00       	and    eax,0x8000
   1400023f9:	48 85 c0             	test   rax,rax
   1400023fc:	74 71                	je     14000246f <do_pseudo_reloc+0x22d>
   1400023fe:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002402:	48 0d 00 00 ff ff    	or     rax,0xffffffffffff0000
   140002408:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000240c:	eb 61                	jmp    14000246f <do_pseudo_reloc+0x22d>
   14000240e:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002412:	8b 00                	mov    eax,DWORD PTR [rax]
   140002414:	89 c0                	mov    eax,eax
   140002416:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000241a:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000241e:	25 00 00 00 80       	and    eax,0x80000000
   140002423:	48 85 c0             	test   rax,rax
   140002426:	74 4a                	je     140002472 <do_pseudo_reloc+0x230>
   140002428:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000242c:	48 ba 00 00 00 00 ff 	movabs rdx,0xffffffff00000000
   140002433:	ff ff ff 
   140002436:	48 09 d0             	or     rax,rdx
   140002439:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000243d:	eb 33                	jmp    140002472 <do_pseudo_reloc+0x230>
   14000243f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002443:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002446:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000244a:	eb 27                	jmp    140002473 <do_pseudo_reloc+0x231>
   14000244c:	48 c7 45 b8 00 00 00 	mov    QWORD PTR [rbp-0x48],0x0
   140002453:	00 
   140002454:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002458:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000245b:	0f b6 c0             	movzx  eax,al
   14000245e:	48 8d 0d 63 2e 00 00 	lea    rcx,[rip+0x2e63]        # 1400052c8 <.rdata+0xd8>
   140002465:	89 c2                	mov    edx,eax
   140002467:	e8 74 f9 ff ff       	call   140001de0 <__report_error>
   14000246c:	90                   	nop
   14000246d:	eb 04                	jmp    140002473 <do_pseudo_reloc+0x231>
   14000246f:	90                   	nop
   140002470:	eb 01                	jmp    140002473 <do_pseudo_reloc+0x231>
   140002472:	90                   	nop
   140002473:	48 8b 4d b8          	mov    rcx,QWORD PTR [rbp-0x48]
   140002477:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000247b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000247d:	89 c2                	mov    edx,eax
   14000247f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002483:	48 01 c2             	add    rdx,rax
   140002486:	48 89 c8             	mov    rax,rcx
   140002489:	48 29 d0             	sub    rax,rdx
   14000248c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140002490:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   140002494:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140002498:	48 01 d0             	add    rax,rdx
   14000249b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000249f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400024a3:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400024a6:	25 ff 00 00 00       	and    eax,0xff
   1400024ab:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   1400024ae:	83 7d d4 3f          	cmp    DWORD PTR [rbp-0x2c],0x3f
   1400024b2:	77 67                	ja     14000251b <do_pseudo_reloc+0x2d9>
   1400024b4:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400024b7:	ba 01 00 00 00       	mov    edx,0x1
   1400024bc:	89 c1                	mov    ecx,eax
   1400024be:	48 d3 e2             	shl    rdx,cl
   1400024c1:	48 89 d0             	mov    rax,rdx
   1400024c4:	48 83 e8 01          	sub    rax,0x1
   1400024c8:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   1400024cc:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400024cf:	83 e8 01             	sub    eax,0x1
   1400024d2:	48 c7 c2 ff ff ff ff 	mov    rdx,0xffffffffffffffff
   1400024d9:	89 c1                	mov    ecx,eax
   1400024db:	48 d3 e2             	shl    rdx,cl
   1400024de:	48 89 d0             	mov    rax,rdx
   1400024e1:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   1400024e5:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400024e9:	48 39 45 c8          	cmp    QWORD PTR [rbp-0x38],rax
   1400024ed:	7c 0a                	jl     1400024f9 <do_pseudo_reloc+0x2b7>
   1400024ef:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400024f3:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   1400024f7:	7e 22                	jle    14000251b <do_pseudo_reloc+0x2d9>
   1400024f9:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   1400024fd:	4c 8b 4d d8          	mov    r9,QWORD PTR [rbp-0x28]
   140002501:	4c 8b 45 e0          	mov    r8,QWORD PTR [rbp-0x20]
   140002505:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140002508:	48 8d 0d e9 2d 00 00 	lea    rcx,[rip+0x2de9]        # 1400052f8 <.rdata+0x108>
   14000250f:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   140002514:	89 c2                	mov    edx,eax
   140002516:	e8 c5 f8 ff ff       	call   140001de0 <__report_error>
   14000251b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000251f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002522:	0f b6 c0             	movzx  eax,al
   140002525:	83 f8 40             	cmp    eax,0x40
   140002528:	74 63                	je     14000258d <do_pseudo_reloc+0x34b>
   14000252a:	83 f8 40             	cmp    eax,0x40
   14000252d:	77 75                	ja     1400025a4 <do_pseudo_reloc+0x362>
   14000252f:	83 f8 20             	cmp    eax,0x20
   140002532:	74 41                	je     140002575 <do_pseudo_reloc+0x333>
   140002534:	83 f8 20             	cmp    eax,0x20
   140002537:	77 6b                	ja     1400025a4 <do_pseudo_reloc+0x362>
   140002539:	83 f8 08             	cmp    eax,0x8
   14000253c:	74 07                	je     140002545 <do_pseudo_reloc+0x303>
   14000253e:	83 f8 10             	cmp    eax,0x10
   140002541:	74 1a                	je     14000255d <do_pseudo_reloc+0x31b>
   140002543:	eb 5f                	jmp    1400025a4 <do_pseudo_reloc+0x362>
   140002545:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002549:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000254d:	41 b8 01 00 00 00    	mov    r8d,0x1
   140002553:	48 89 c1             	mov    rcx,rax
   140002556:	e8 a0 fc ff ff       	call   1400021fb <__write_memory>
   14000255b:	eb 47                	jmp    1400025a4 <do_pseudo_reloc+0x362>
   14000255d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002561:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002565:	41 b8 02 00 00 00    	mov    r8d,0x2
   14000256b:	48 89 c1             	mov    rcx,rax
   14000256e:	e8 88 fc ff ff       	call   1400021fb <__write_memory>
   140002573:	eb 2f                	jmp    1400025a4 <do_pseudo_reloc+0x362>
   140002575:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002579:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000257d:	41 b8 04 00 00 00    	mov    r8d,0x4
   140002583:	48 89 c1             	mov    rcx,rax
   140002586:	e8 70 fc ff ff       	call   1400021fb <__write_memory>
   14000258b:	eb 17                	jmp    1400025a4 <do_pseudo_reloc+0x362>
   14000258d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002591:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002595:	41 b8 08 00 00 00    	mov    r8d,0x8
   14000259b:	48 89 c1             	mov    rcx,rax
   14000259e:	e8 58 fc ff ff       	call   1400021fb <__write_memory>
   1400025a3:	90                   	nop
   1400025a4:	48 83 45 f0 0c       	add    QWORD PTR [rbp-0x10],0xc
   1400025a9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400025ad:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   1400025b1:	0f 82 8d fd ff ff    	jb     140002344 <do_pseudo_reloc+0x102>
   1400025b7:	eb 01                	jmp    1400025ba <do_pseudo_reloc+0x378>
   1400025b9:	90                   	nop
   1400025ba:	48 83 ec 80          	sub    rsp,0xffffffffffffff80
   1400025be:	5d                   	pop    rbp
   1400025bf:	c3                   	ret

00000001400025c0 <_pei386_runtime_relocator>:
   1400025c0:	55                   	push   rbp
   1400025c1:	48 89 e5             	mov    rbp,rsp
   1400025c4:	48 83 ec 30          	sub    rsp,0x30
   1400025c8:	8b 05 1e 6b 00 00    	mov    eax,DWORD PTR [rip+0x6b1e]        # 1400090ec <was_init.0>
   1400025ce:	85 c0                	test   eax,eax
   1400025d0:	0f 85 88 00 00 00    	jne    14000265e <_pei386_runtime_relocator+0x9e>
   1400025d6:	8b 05 10 6b 00 00    	mov    eax,DWORD PTR [rip+0x6b10]        # 1400090ec <was_init.0>
   1400025dc:	83 c0 01             	add    eax,0x1
   1400025df:	89 05 07 6b 00 00    	mov    DWORD PTR [rip+0x6b07],eax        # 1400090ec <was_init.0>
   1400025e5:	e8 21 0b 00 00       	call   14000310b <__mingw_GetSectionCount>
   1400025ea:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400025ed:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400025f0:	48 63 d0             	movsxd rdx,eax
   1400025f3:	48 89 d0             	mov    rax,rdx
   1400025f6:	48 c1 e0 02          	shl    rax,0x2
   1400025fa:	48 01 d0             	add    rax,rdx
   1400025fd:	48 c1 e0 03          	shl    rax,0x3
   140002601:	48 83 c0 0f          	add    rax,0xf
   140002605:	48 c1 e8 04          	shr    rax,0x4
   140002609:	48 c1 e0 04          	shl    rax,0x4
   14000260d:	e8 8e 0d 00 00       	call   1400033a0 <___chkstk_ms>
   140002612:	48 29 c4             	sub    rsp,rax
   140002615:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   14000261a:	48 83 c0 0f          	add    rax,0xf
   14000261e:	48 c1 e8 04          	shr    rax,0x4
   140002622:	48 c1 e0 04          	shl    rax,0x4
   140002626:	48 89 05 b3 6a 00 00 	mov    QWORD PTR [rip+0x6ab3],rax        # 1400090e0 <the_secs>
   14000262d:	c7 05 b1 6a 00 00 00 	mov    DWORD PTR [rip+0x6ab1],0x0        # 1400090e8 <maxSections>
   140002634:	00 00 00 
   140002637:	48 8b 0d 62 2d 00 00 	mov    rcx,QWORD PTR [rip+0x2d62]        # 1400053a0 <.refptr.__ImageBase>
   14000263e:	48 8b 15 6b 2d 00 00 	mov    rdx,QWORD PTR [rip+0x2d6b]        # 1400053b0 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   140002645:	48 8b 05 74 2d 00 00 	mov    rax,QWORD PTR [rip+0x2d74]        # 1400053c0 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000264c:	49 89 c8             	mov    r8,rcx
   14000264f:	48 89 c1             	mov    rcx,rax
   140002652:	e8 eb fb ff ff       	call   140002242 <do_pseudo_reloc>
   140002657:	e8 c7 fa ff ff       	call   140002123 <restore_modified_sections>
   14000265c:	eb 01                	jmp    14000265f <_pei386_runtime_relocator+0x9f>
   14000265e:	90                   	nop
   14000265f:	48 89 ec             	mov    rsp,rbp
   140002662:	5d                   	pop    rbp
   140002663:	c3                   	ret
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

0000000140002670 <__mingw_raise_matherr>:
   140002670:	55                   	push   rbp
   140002671:	48 89 e5             	mov    rbp,rsp
   140002674:	48 83 ec 50          	sub    rsp,0x50
   140002678:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000267b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000267f:	f2 0f 11 55 20       	movsd  QWORD PTR [rbp+0x20],xmm2
   140002684:	f2 0f 11 5d 28       	movsd  QWORD PTR [rbp+0x28],xmm3
   140002689:	48 8b 05 60 6a 00 00 	mov    rax,QWORD PTR [rip+0x6a60]        # 1400090f0 <stUserMathErr>
   140002690:	48 85 c0             	test   rax,rax
   140002693:	74 3e                	je     1400026d3 <__mingw_raise_matherr+0x63>
   140002695:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140002698:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   14000269b:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000269f:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   1400026a3:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   1400026a8:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   1400026ad:	f2 0f 10 45 28       	movsd  xmm0,QWORD PTR [rbp+0x28]
   1400026b2:	f2 0f 11 45 e8       	movsd  QWORD PTR [rbp-0x18],xmm0
   1400026b7:	f2 0f 10 45 30       	movsd  xmm0,QWORD PTR [rbp+0x30]
   1400026bc:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   1400026c1:	48 8b 15 28 6a 00 00 	mov    rdx,QWORD PTR [rip+0x6a28]        # 1400090f0 <stUserMathErr>
   1400026c8:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   1400026cc:	48 89 c1             	mov    rcx,rax
   1400026cf:	ff d2                	call   rdx
   1400026d1:	eb 01                	jmp    1400026d4 <__mingw_raise_matherr+0x64>
   1400026d3:	90                   	nop
   1400026d4:	48 83 c4 50          	add    rsp,0x50
   1400026d8:	5d                   	pop    rbp
   1400026d9:	c3                   	ret

00000001400026da <__mingw_setusermatherr>:
   1400026da:	55                   	push   rbp
   1400026db:	48 89 e5             	mov    rbp,rsp
   1400026de:	48 83 ec 20          	sub    rsp,0x20
   1400026e2:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400026e6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400026ea:	48 89 05 ff 69 00 00 	mov    QWORD PTR [rip+0x69ff],rax        # 1400090f0 <stUserMathErr>
   1400026f1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400026f5:	48 89 c1             	mov    rcx,rax
   1400026f8:	e8 23 0e 00 00       	call   140003520 <__setusermatherr>
   1400026fd:	90                   	nop
   1400026fe:	48 83 c4 20          	add    rsp,0x20
   140002702:	5d                   	pop    rbp
   140002703:	c3                   	ret
   140002704:	90                   	nop
   140002705:	90                   	nop
   140002706:	90                   	nop
   140002707:	90                   	nop
   140002708:	90                   	nop
   140002709:	90                   	nop
   14000270a:	90                   	nop
   14000270b:	90                   	nop
   14000270c:	90                   	nop
   14000270d:	90                   	nop
   14000270e:	90                   	nop
   14000270f:	90                   	nop

0000000140002710 <__mingw_SEH_error_handler>:
   140002710:	55                   	push   rbp
   140002711:	48 89 e5             	mov    rbp,rsp
   140002714:	48 83 ec 30          	sub    rsp,0x30
   140002718:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000271c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002720:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002724:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140002728:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   14000272f:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002736:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000273a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000273d:	83 e0 02             	and    eax,0x2
   140002740:	85 c0                	test   eax,eax
   140002742:	74 0a                	je     14000274e <__mingw_SEH_error_handler+0x3e>
   140002744:	b8 01 00 00 00       	mov    eax,0x1
   140002749:	e9 16 02 00 00       	jmp    140002964 <__mingw_SEH_error_handler+0x254>
   14000274e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002752:	8b 00                	mov    eax,DWORD PTR [rax]
   140002754:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002759:	3d 43 43 47 20       	cmp    eax,0x20474343
   14000275e:	75 18                	jne    140002778 <__mingw_SEH_error_handler+0x68>
   140002760:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002764:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002767:	83 e0 01             	and    eax,0x1
   14000276a:	85 c0                	test   eax,eax
   14000276c:	75 0a                	jne    140002778 <__mingw_SEH_error_handler+0x68>
   14000276e:	b8 00 00 00 00       	mov    eax,0x0
   140002773:	e9 ec 01 00 00       	jmp    140002964 <__mingw_SEH_error_handler+0x254>
   140002778:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000277c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000277e:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002783:	0f 84 12 01 00 00    	je     14000289b <__mingw_SEH_error_handler+0x18b>
   140002789:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000278e:	0f 87 c3 01 00 00    	ja     140002957 <__mingw_SEH_error_handler+0x247>
   140002794:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   140002799:	0f 87 b8 01 00 00    	ja     140002957 <__mingw_SEH_error_handler+0x247>
   14000279f:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   1400027a4:	0f 83 4c 01 00 00    	jae    1400028f6 <__mingw_SEH_error_handler+0x1e6>
   1400027aa:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400027af:	0f 84 3a 01 00 00    	je     1400028ef <__mingw_SEH_error_handler+0x1df>
   1400027b5:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400027ba:	0f 87 97 01 00 00    	ja     140002957 <__mingw_SEH_error_handler+0x247>
   1400027c0:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400027c5:	0f 84 83 01 00 00    	je     14000294e <__mingw_SEH_error_handler+0x23e>
   1400027cb:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400027d0:	0f 87 81 01 00 00    	ja     140002957 <__mingw_SEH_error_handler+0x247>
   1400027d6:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400027db:	0f 87 76 01 00 00    	ja     140002957 <__mingw_SEH_error_handler+0x247>
   1400027e1:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   1400027e6:	0f 83 03 01 00 00    	jae    1400028ef <__mingw_SEH_error_handler+0x1df>
   1400027ec:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400027f1:	0f 84 57 01 00 00    	je     14000294e <__mingw_SEH_error_handler+0x23e>
   1400027f7:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400027fc:	0f 87 55 01 00 00    	ja     140002957 <__mingw_SEH_error_handler+0x247>
   140002802:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002807:	0f 84 8e 00 00 00    	je     14000289b <__mingw_SEH_error_handler+0x18b>
   14000280d:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002812:	0f 87 3f 01 00 00    	ja     140002957 <__mingw_SEH_error_handler+0x247>
   140002818:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000281d:	0f 84 2b 01 00 00    	je     14000294e <__mingw_SEH_error_handler+0x23e>
   140002823:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002828:	0f 87 29 01 00 00    	ja     140002957 <__mingw_SEH_error_handler+0x247>
   14000282e:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002833:	0f 84 15 01 00 00    	je     14000294e <__mingw_SEH_error_handler+0x23e>
   140002839:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000283e:	0f 85 13 01 00 00    	jne    140002957 <__mingw_SEH_error_handler+0x247>
   140002844:	ba 00 00 00 00       	mov    edx,0x0
   140002849:	b9 0b 00 00 00       	mov    ecx,0xb
   14000284e:	e8 3d 0d 00 00       	call   140003590 <signal>
   140002853:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002857:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000285c:	75 1b                	jne    140002879 <__mingw_SEH_error_handler+0x169>
   14000285e:	ba 01 00 00 00       	mov    edx,0x1
   140002863:	b9 0b 00 00 00       	mov    ecx,0xb
   140002868:	e8 23 0d 00 00       	call   140003590 <signal>
   14000286d:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002874:	e9 e1 00 00 00       	jmp    14000295a <__mingw_SEH_error_handler+0x24a>
   140002879:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000287e:	0f 84 d6 00 00 00    	je     14000295a <__mingw_SEH_error_handler+0x24a>
   140002884:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002888:	b9 0b 00 00 00       	mov    ecx,0xb
   14000288d:	ff d0                	call   rax
   14000288f:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002896:	e9 bf 00 00 00       	jmp    14000295a <__mingw_SEH_error_handler+0x24a>
   14000289b:	ba 00 00 00 00       	mov    edx,0x0
   1400028a0:	b9 04 00 00 00       	mov    ecx,0x4
   1400028a5:	e8 e6 0c 00 00       	call   140003590 <signal>
   1400028aa:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400028ae:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400028b3:	75 1b                	jne    1400028d0 <__mingw_SEH_error_handler+0x1c0>
   1400028b5:	ba 01 00 00 00       	mov    edx,0x1
   1400028ba:	b9 04 00 00 00       	mov    ecx,0x4
   1400028bf:	e8 cc 0c 00 00       	call   140003590 <signal>
   1400028c4:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400028cb:	e9 8d 00 00 00       	jmp    14000295d <__mingw_SEH_error_handler+0x24d>
   1400028d0:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400028d5:	0f 84 82 00 00 00    	je     14000295d <__mingw_SEH_error_handler+0x24d>
   1400028db:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400028df:	b9 04 00 00 00       	mov    ecx,0x4
   1400028e4:	ff d0                	call   rax
   1400028e6:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400028ed:	eb 6e                	jmp    14000295d <__mingw_SEH_error_handler+0x24d>
   1400028ef:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400028f6:	ba 00 00 00 00       	mov    edx,0x0
   1400028fb:	b9 08 00 00 00       	mov    ecx,0x8
   140002900:	e8 8b 0c 00 00       	call   140003590 <signal>
   140002905:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002909:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000290e:	75 23                	jne    140002933 <__mingw_SEH_error_handler+0x223>
   140002910:	ba 01 00 00 00       	mov    edx,0x1
   140002915:	b9 08 00 00 00       	mov    ecx,0x8
   14000291a:	e8 71 0c 00 00       	call   140003590 <signal>
   14000291f:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002923:	74 05                	je     14000292a <__mingw_SEH_error_handler+0x21a>
   140002925:	e8 a6 05 00 00       	call   140002ed0 <_fpreset>
   14000292a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002931:	eb 2d                	jmp    140002960 <__mingw_SEH_error_handler+0x250>
   140002933:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002938:	74 26                	je     140002960 <__mingw_SEH_error_handler+0x250>
   14000293a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000293e:	b9 08 00 00 00       	mov    ecx,0x8
   140002943:	ff d0                	call   rax
   140002945:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000294c:	eb 12                	jmp    140002960 <__mingw_SEH_error_handler+0x250>
   14000294e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002955:	eb 0a                	jmp    140002961 <__mingw_SEH_error_handler+0x251>
   140002957:	90                   	nop
   140002958:	eb 07                	jmp    140002961 <__mingw_SEH_error_handler+0x251>
   14000295a:	90                   	nop
   14000295b:	eb 04                	jmp    140002961 <__mingw_SEH_error_handler+0x251>
   14000295d:	90                   	nop
   14000295e:	eb 01                	jmp    140002961 <__mingw_SEH_error_handler+0x251>
   140002960:	90                   	nop
   140002961:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002964:	48 83 c4 30          	add    rsp,0x30
   140002968:	5d                   	pop    rbp
   140002969:	c3                   	ret

000000014000296a <_gnu_exception_handler>:
   14000296a:	55                   	push   rbp
   14000296b:	48 89 e5             	mov    rbp,rsp
   14000296e:	48 83 ec 30          	sub    rsp,0x30
   140002972:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002976:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000297d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002984:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002988:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000298b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000298d:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002992:	3d 43 43 47 20       	cmp    eax,0x20474343
   140002997:	75 1b                	jne    1400029b4 <_gnu_exception_handler+0x4a>
   140002999:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000299d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400029a0:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400029a3:	83 e0 01             	and    eax,0x1
   1400029a6:	85 c0                	test   eax,eax
   1400029a8:	75 0a                	jne    1400029b4 <_gnu_exception_handler+0x4a>
   1400029aa:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400029af:	e9 14 02 00 00       	jmp    140002bc8 <_gnu_exception_handler+0x25e>
   1400029b4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400029b8:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400029bb:	8b 00                	mov    eax,DWORD PTR [rax]
   1400029bd:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400029c2:	0f 84 12 01 00 00    	je     140002ada <_gnu_exception_handler+0x170>
   1400029c8:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400029cd:	0f 87 c3 01 00 00    	ja     140002b96 <_gnu_exception_handler+0x22c>
   1400029d3:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   1400029d8:	0f 87 b8 01 00 00    	ja     140002b96 <_gnu_exception_handler+0x22c>
   1400029de:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   1400029e3:	0f 83 4c 01 00 00    	jae    140002b35 <_gnu_exception_handler+0x1cb>
   1400029e9:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400029ee:	0f 84 3a 01 00 00    	je     140002b2e <_gnu_exception_handler+0x1c4>
   1400029f4:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400029f9:	0f 87 97 01 00 00    	ja     140002b96 <_gnu_exception_handler+0x22c>
   1400029ff:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   140002a04:	0f 84 83 01 00 00    	je     140002b8d <_gnu_exception_handler+0x223>
   140002a0a:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   140002a0f:	0f 87 81 01 00 00    	ja     140002b96 <_gnu_exception_handler+0x22c>
   140002a15:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   140002a1a:	0f 87 76 01 00 00    	ja     140002b96 <_gnu_exception_handler+0x22c>
   140002a20:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   140002a25:	0f 83 03 01 00 00    	jae    140002b2e <_gnu_exception_handler+0x1c4>
   140002a2b:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   140002a30:	0f 84 57 01 00 00    	je     140002b8d <_gnu_exception_handler+0x223>
   140002a36:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   140002a3b:	0f 87 55 01 00 00    	ja     140002b96 <_gnu_exception_handler+0x22c>
   140002a41:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002a46:	0f 84 8e 00 00 00    	je     140002ada <_gnu_exception_handler+0x170>
   140002a4c:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002a51:	0f 87 3f 01 00 00    	ja     140002b96 <_gnu_exception_handler+0x22c>
   140002a57:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002a5c:	0f 84 2b 01 00 00    	je     140002b8d <_gnu_exception_handler+0x223>
   140002a62:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002a67:	0f 87 29 01 00 00    	ja     140002b96 <_gnu_exception_handler+0x22c>
   140002a6d:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002a72:	0f 84 15 01 00 00    	je     140002b8d <_gnu_exception_handler+0x223>
   140002a78:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   140002a7d:	0f 85 13 01 00 00    	jne    140002b96 <_gnu_exception_handler+0x22c>
   140002a83:	ba 00 00 00 00       	mov    edx,0x0
   140002a88:	b9 0b 00 00 00       	mov    ecx,0xb
   140002a8d:	e8 fe 0a 00 00       	call   140003590 <signal>
   140002a92:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002a96:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002a9b:	75 1b                	jne    140002ab8 <_gnu_exception_handler+0x14e>
   140002a9d:	ba 01 00 00 00       	mov    edx,0x1
   140002aa2:	b9 0b 00 00 00       	mov    ecx,0xb
   140002aa7:	e8 e4 0a 00 00       	call   140003590 <signal>
   140002aac:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002ab3:	e9 e1 00 00 00       	jmp    140002b99 <_gnu_exception_handler+0x22f>
   140002ab8:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002abd:	0f 84 d6 00 00 00    	je     140002b99 <_gnu_exception_handler+0x22f>
   140002ac3:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002ac7:	b9 0b 00 00 00       	mov    ecx,0xb
   140002acc:	ff d0                	call   rax
   140002ace:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002ad5:	e9 bf 00 00 00       	jmp    140002b99 <_gnu_exception_handler+0x22f>
   140002ada:	ba 00 00 00 00       	mov    edx,0x0
   140002adf:	b9 04 00 00 00       	mov    ecx,0x4
   140002ae4:	e8 a7 0a 00 00       	call   140003590 <signal>
   140002ae9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002aed:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002af2:	75 1b                	jne    140002b0f <_gnu_exception_handler+0x1a5>
   140002af4:	ba 01 00 00 00       	mov    edx,0x1
   140002af9:	b9 04 00 00 00       	mov    ecx,0x4
   140002afe:	e8 8d 0a 00 00       	call   140003590 <signal>
   140002b03:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002b0a:	e9 8d 00 00 00       	jmp    140002b9c <_gnu_exception_handler+0x232>
   140002b0f:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002b14:	0f 84 82 00 00 00    	je     140002b9c <_gnu_exception_handler+0x232>
   140002b1a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b1e:	b9 04 00 00 00       	mov    ecx,0x4
   140002b23:	ff d0                	call   rax
   140002b25:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002b2c:	eb 6e                	jmp    140002b9c <_gnu_exception_handler+0x232>
   140002b2e:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140002b35:	ba 00 00 00 00       	mov    edx,0x0
   140002b3a:	b9 08 00 00 00       	mov    ecx,0x8
   140002b3f:	e8 4c 0a 00 00       	call   140003590 <signal>
   140002b44:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b48:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002b4d:	75 23                	jne    140002b72 <_gnu_exception_handler+0x208>
   140002b4f:	ba 01 00 00 00       	mov    edx,0x1
   140002b54:	b9 08 00 00 00       	mov    ecx,0x8
   140002b59:	e8 32 0a 00 00       	call   140003590 <signal>
   140002b5e:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002b62:	74 05                	je     140002b69 <_gnu_exception_handler+0x1ff>
   140002b64:	e8 67 03 00 00       	call   140002ed0 <_fpreset>
   140002b69:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002b70:	eb 2d                	jmp    140002b9f <_gnu_exception_handler+0x235>
   140002b72:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002b77:	74 26                	je     140002b9f <_gnu_exception_handler+0x235>
   140002b79:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b7d:	b9 08 00 00 00       	mov    ecx,0x8
   140002b82:	ff d0                	call   rax
   140002b84:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002b8b:	eb 12                	jmp    140002b9f <_gnu_exception_handler+0x235>
   140002b8d:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002b94:	eb 0a                	jmp    140002ba0 <_gnu_exception_handler+0x236>
   140002b96:	90                   	nop
   140002b97:	eb 07                	jmp    140002ba0 <_gnu_exception_handler+0x236>
   140002b99:	90                   	nop
   140002b9a:	eb 04                	jmp    140002ba0 <_gnu_exception_handler+0x236>
   140002b9c:	90                   	nop
   140002b9d:	eb 01                	jmp    140002ba0 <_gnu_exception_handler+0x236>
   140002b9f:	90                   	nop
   140002ba0:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140002ba4:	75 1f                	jne    140002bc5 <_gnu_exception_handler+0x25b>
   140002ba6:	48 8b 05 63 65 00 00 	mov    rax,QWORD PTR [rip+0x6563]        # 140009110 <__mingw_oldexcpt_handler>
   140002bad:	48 85 c0             	test   rax,rax
   140002bb0:	74 13                	je     140002bc5 <_gnu_exception_handler+0x25b>
   140002bb2:	48 8b 15 57 65 00 00 	mov    rdx,QWORD PTR [rip+0x6557]        # 140009110 <__mingw_oldexcpt_handler>
   140002bb9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002bbd:	48 89 c1             	mov    rcx,rax
   140002bc0:	ff d2                	call   rdx
   140002bc2:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140002bc5:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002bc8:	48 83 c4 30          	add    rsp,0x30
   140002bcc:	5d                   	pop    rbp
   140002bcd:	c3                   	ret
   140002bce:	90                   	nop
   140002bcf:	90                   	nop

0000000140002bd0 <___w64_mingwthr_add_key_dtor>:
   140002bd0:	55                   	push   rbp
   140002bd1:	48 89 e5             	mov    rbp,rsp
   140002bd4:	48 83 ec 30          	sub    rsp,0x30
   140002bd8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002bdb:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002bdf:	8b 05 63 65 00 00    	mov    eax,DWORD PTR [rip+0x6563]        # 140009148 <__mingwthr_cs_init>
   140002be5:	85 c0                	test   eax,eax
   140002be7:	75 07                	jne    140002bf0 <___w64_mingwthr_add_key_dtor+0x20>
   140002be9:	b8 00 00 00 00       	mov    eax,0x0
   140002bee:	eb 7b                	jmp    140002c6b <___w64_mingwthr_add_key_dtor+0x9b>
   140002bf0:	ba 18 00 00 00       	mov    edx,0x18
   140002bf5:	b9 01 00 00 00       	mov    ecx,0x1
   140002bfa:	e8 51 09 00 00       	call   140003550 <calloc>
   140002bff:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002c03:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002c08:	75 07                	jne    140002c11 <___w64_mingwthr_add_key_dtor+0x41>
   140002c0a:	b8 ff ff ff ff       	mov    eax,0xffffffff
   140002c0f:	eb 5a                	jmp    140002c6b <___w64_mingwthr_add_key_dtor+0x9b>
   140002c11:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c15:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140002c18:	89 10                	mov    DWORD PTR [rax],edx
   140002c1a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c1e:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140002c22:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
   140002c26:	48 8d 05 f3 64 00 00 	lea    rax,[rip+0x64f3]        # 140009120 <__mingwthr_cs>
   140002c2d:	48 89 c1             	mov    rcx,rax
   140002c30:	48 8b 05 31 76 00 00 	mov    rax,QWORD PTR [rip+0x7631]        # 14000a268 <__imp_EnterCriticalSection>
   140002c37:	ff d0                	call   rax
   140002c39:	48 8b 15 10 65 00 00 	mov    rdx,QWORD PTR [rip+0x6510]        # 140009150 <key_dtor_list>
   140002c40:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c44:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002c48:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c4c:	48 89 05 fd 64 00 00 	mov    QWORD PTR [rip+0x64fd],rax        # 140009150 <key_dtor_list>
   140002c53:	48 8d 05 c6 64 00 00 	lea    rax,[rip+0x64c6]        # 140009120 <__mingwthr_cs>
   140002c5a:	48 89 c1             	mov    rcx,rax
   140002c5d:	48 8b 05 34 76 00 00 	mov    rax,QWORD PTR [rip+0x7634]        # 14000a298 <__imp_LeaveCriticalSection>
   140002c64:	ff d0                	call   rax
   140002c66:	b8 00 00 00 00       	mov    eax,0x0
   140002c6b:	48 83 c4 30          	add    rsp,0x30
   140002c6f:	5d                   	pop    rbp
   140002c70:	c3                   	ret

0000000140002c71 <___w64_mingwthr_remove_key_dtor>:
   140002c71:	55                   	push   rbp
   140002c72:	48 89 e5             	mov    rbp,rsp
   140002c75:	48 83 ec 30          	sub    rsp,0x30
   140002c79:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002c7c:	8b 05 c6 64 00 00    	mov    eax,DWORD PTR [rip+0x64c6]        # 140009148 <__mingwthr_cs_init>
   140002c82:	85 c0                	test   eax,eax
   140002c84:	75 0a                	jne    140002c90 <___w64_mingwthr_remove_key_dtor+0x1f>
   140002c86:	b8 00 00 00 00       	mov    eax,0x0
   140002c8b:	e9 9c 00 00 00       	jmp    140002d2c <___w64_mingwthr_remove_key_dtor+0xbb>
   140002c90:	48 8d 05 89 64 00 00 	lea    rax,[rip+0x6489]        # 140009120 <__mingwthr_cs>
   140002c97:	48 89 c1             	mov    rcx,rax
   140002c9a:	48 8b 05 c7 75 00 00 	mov    rax,QWORD PTR [rip+0x75c7]        # 14000a268 <__imp_EnterCriticalSection>
   140002ca1:	ff d0                	call   rax
   140002ca3:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   140002caa:	00 
   140002cab:	48 8b 05 9e 64 00 00 	mov    rax,QWORD PTR [rip+0x649e]        # 140009150 <key_dtor_list>
   140002cb2:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002cb6:	eb 55                	jmp    140002d0d <___w64_mingwthr_remove_key_dtor+0x9c>
   140002cb8:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002cbc:	8b 00                	mov    eax,DWORD PTR [rax]
   140002cbe:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   140002cc1:	75 36                	jne    140002cf9 <___w64_mingwthr_remove_key_dtor+0x88>
   140002cc3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002cc8:	75 11                	jne    140002cdb <___w64_mingwthr_remove_key_dtor+0x6a>
   140002cca:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002cce:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002cd2:	48 89 05 77 64 00 00 	mov    QWORD PTR [rip+0x6477],rax        # 140009150 <key_dtor_list>
   140002cd9:	eb 10                	jmp    140002ceb <___w64_mingwthr_remove_key_dtor+0x7a>
   140002cdb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002cdf:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   140002ce3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ce7:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002ceb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002cef:	48 89 c1             	mov    rcx,rax
   140002cf2:	e8 79 08 00 00       	call   140003570 <free>
   140002cf7:	eb 1b                	jmp    140002d14 <___w64_mingwthr_remove_key_dtor+0xa3>
   140002cf9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002cfd:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d01:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002d05:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002d09:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002d0d:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002d12:	75 a4                	jne    140002cb8 <___w64_mingwthr_remove_key_dtor+0x47>
   140002d14:	48 8d 05 05 64 00 00 	lea    rax,[rip+0x6405]        # 140009120 <__mingwthr_cs>
   140002d1b:	48 89 c1             	mov    rcx,rax
   140002d1e:	48 8b 05 73 75 00 00 	mov    rax,QWORD PTR [rip+0x7573]        # 14000a298 <__imp_LeaveCriticalSection>
   140002d25:	ff d0                	call   rax
   140002d27:	b8 00 00 00 00       	mov    eax,0x0
   140002d2c:	48 83 c4 30          	add    rsp,0x30
   140002d30:	5d                   	pop    rbp
   140002d31:	c3                   	ret

0000000140002d32 <__mingwthr_run_key_dtors>:
   140002d32:	55                   	push   rbp
   140002d33:	48 89 e5             	mov    rbp,rsp
   140002d36:	48 83 ec 30          	sub    rsp,0x30
   140002d3a:	8b 05 08 64 00 00    	mov    eax,DWORD PTR [rip+0x6408]        # 140009148 <__mingwthr_cs_init>
   140002d40:	85 c0                	test   eax,eax
   140002d42:	0f 84 82 00 00 00    	je     140002dca <__mingwthr_run_key_dtors+0x98>
   140002d48:	48 8d 05 d1 63 00 00 	lea    rax,[rip+0x63d1]        # 140009120 <__mingwthr_cs>
   140002d4f:	48 89 c1             	mov    rcx,rax
   140002d52:	48 8b 05 0f 75 00 00 	mov    rax,QWORD PTR [rip+0x750f]        # 14000a268 <__imp_EnterCriticalSection>
   140002d59:	ff d0                	call   rax
   140002d5b:	48 8b 05 ee 63 00 00 	mov    rax,QWORD PTR [rip+0x63ee]        # 140009150 <key_dtor_list>
   140002d62:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d66:	eb 46                	jmp    140002dae <__mingwthr_run_key_dtors+0x7c>
   140002d68:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d6c:	8b 00                	mov    eax,DWORD PTR [rax]
   140002d6e:	89 c1                	mov    ecx,eax
   140002d70:	48 8b 05 41 75 00 00 	mov    rax,QWORD PTR [rip+0x7541]        # 14000a2b8 <__imp_TlsGetValue>
   140002d77:	ff d0                	call   rax
   140002d79:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002d7d:	48 8b 05 f4 74 00 00 	mov    rax,QWORD PTR [rip+0x74f4]        # 14000a278 <__imp_GetLastError>
   140002d84:	ff d0                	call   rax
   140002d86:	85 c0                	test   eax,eax
   140002d88:	75 18                	jne    140002da2 <__mingwthr_run_key_dtors+0x70>
   140002d8a:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002d8f:	74 11                	je     140002da2 <__mingwthr_run_key_dtors+0x70>
   140002d91:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d95:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140002d99:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002d9d:	48 89 c1             	mov    rcx,rax
   140002da0:	ff d2                	call   rdx
   140002da2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002da6:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002daa:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002dae:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002db3:	75 b3                	jne    140002d68 <__mingwthr_run_key_dtors+0x36>
   140002db5:	48 8d 05 64 63 00 00 	lea    rax,[rip+0x6364]        # 140009120 <__mingwthr_cs>
   140002dbc:	48 89 c1             	mov    rcx,rax
   140002dbf:	48 8b 05 d2 74 00 00 	mov    rax,QWORD PTR [rip+0x74d2]        # 14000a298 <__imp_LeaveCriticalSection>
   140002dc6:	ff d0                	call   rax
   140002dc8:	eb 01                	jmp    140002dcb <__mingwthr_run_key_dtors+0x99>
   140002dca:	90                   	nop
   140002dcb:	48 83 c4 30          	add    rsp,0x30
   140002dcf:	5d                   	pop    rbp
   140002dd0:	c3                   	ret

0000000140002dd1 <__mingw_TLScallback>:
   140002dd1:	55                   	push   rbp
   140002dd2:	48 89 e5             	mov    rbp,rsp
   140002dd5:	48 83 ec 30          	sub    rsp,0x30
   140002dd9:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002ddd:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140002de0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002de4:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002de8:	0f 84 cc 00 00 00    	je     140002eba <__mingw_TLScallback+0xe9>
   140002dee:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002df2:	0f 87 ca 00 00 00    	ja     140002ec2 <__mingw_TLScallback+0xf1>
   140002df8:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002dfc:	0f 84 b1 00 00 00    	je     140002eb3 <__mingw_TLScallback+0xe2>
   140002e02:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002e06:	0f 87 b6 00 00 00    	ja     140002ec2 <__mingw_TLScallback+0xf1>
   140002e0c:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140002e10:	74 33                	je     140002e45 <__mingw_TLScallback+0x74>
   140002e12:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140002e16:	0f 85 a6 00 00 00    	jne    140002ec2 <__mingw_TLScallback+0xf1>
   140002e1c:	8b 05 26 63 00 00    	mov    eax,DWORD PTR [rip+0x6326]        # 140009148 <__mingwthr_cs_init>
   140002e22:	85 c0                	test   eax,eax
   140002e24:	75 13                	jne    140002e39 <__mingw_TLScallback+0x68>
   140002e26:	48 8d 05 f3 62 00 00 	lea    rax,[rip+0x62f3]        # 140009120 <__mingwthr_cs>
   140002e2d:	48 89 c1             	mov    rcx,rax
   140002e30:	48 8b 05 59 74 00 00 	mov    rax,QWORD PTR [rip+0x7459]        # 14000a290 <__imp_InitializeCriticalSection>
   140002e37:	ff d0                	call   rax
   140002e39:	c7 05 05 63 00 00 01 	mov    DWORD PTR [rip+0x6305],0x1        # 140009148 <__mingwthr_cs_init>
   140002e40:	00 00 00 
   140002e43:	eb 7d                	jmp    140002ec2 <__mingw_TLScallback+0xf1>
   140002e45:	e8 e8 fe ff ff       	call   140002d32 <__mingwthr_run_key_dtors>
   140002e4a:	8b 05 f8 62 00 00    	mov    eax,DWORD PTR [rip+0x62f8]        # 140009148 <__mingwthr_cs_init>
   140002e50:	83 f8 01             	cmp    eax,0x1
   140002e53:	75 6c                	jne    140002ec1 <__mingw_TLScallback+0xf0>
   140002e55:	48 8b 05 f4 62 00 00 	mov    rax,QWORD PTR [rip+0x62f4]        # 140009150 <key_dtor_list>
   140002e5c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002e60:	eb 20                	jmp    140002e82 <__mingw_TLScallback+0xb1>
   140002e62:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e66:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002e6a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002e6e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e72:	48 89 c1             	mov    rcx,rax
   140002e75:	e8 f6 06 00 00       	call   140003570 <free>
   140002e7a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002e7e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002e82:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002e87:	75 d9                	jne    140002e62 <__mingw_TLScallback+0x91>
   140002e89:	48 c7 05 bc 62 00 00 	mov    QWORD PTR [rip+0x62bc],0x0        # 140009150 <key_dtor_list>
   140002e90:	00 00 00 00 
   140002e94:	c7 05 aa 62 00 00 00 	mov    DWORD PTR [rip+0x62aa],0x0        # 140009148 <__mingwthr_cs_init>
   140002e9b:	00 00 00 
   140002e9e:	48 8d 05 7b 62 00 00 	lea    rax,[rip+0x627b]        # 140009120 <__mingwthr_cs>
   140002ea5:	48 89 c1             	mov    rcx,rax
   140002ea8:	48 8b 05 b1 73 00 00 	mov    rax,QWORD PTR [rip+0x73b1]        # 14000a260 <__imp_DeleteCriticalSection>
   140002eaf:	ff d0                	call   rax
   140002eb1:	eb 0e                	jmp    140002ec1 <__mingw_TLScallback+0xf0>
   140002eb3:	e8 18 00 00 00       	call   140002ed0 <_fpreset>
   140002eb8:	eb 08                	jmp    140002ec2 <__mingw_TLScallback+0xf1>
   140002eba:	e8 73 fe ff ff       	call   140002d32 <__mingwthr_run_key_dtors>
   140002ebf:	eb 01                	jmp    140002ec2 <__mingw_TLScallback+0xf1>
   140002ec1:	90                   	nop
   140002ec2:	b8 01 00 00 00       	mov    eax,0x1
   140002ec7:	48 83 c4 30          	add    rsp,0x30
   140002ecb:	5d                   	pop    rbp
   140002ecc:	c3                   	ret
   140002ecd:	90                   	nop
   140002ece:	90                   	nop
   140002ecf:	90                   	nop

0000000140002ed0 <_fpreset>:
   140002ed0:	55                   	push   rbp
   140002ed1:	48 89 e5             	mov    rbp,rsp
   140002ed4:	db e3                	fninit
   140002ed6:	90                   	nop
   140002ed7:	5d                   	pop    rbp
   140002ed8:	c3                   	ret
   140002ed9:	90                   	nop
   140002eda:	90                   	nop
   140002edb:	90                   	nop
   140002edc:	90                   	nop
   140002edd:	90                   	nop
   140002ede:	90                   	nop
   140002edf:	90                   	nop

0000000140002ee0 <_ValidateImageBase>:
   140002ee0:	55                   	push   rbp
   140002ee1:	48 89 e5             	mov    rbp,rsp
   140002ee4:	48 83 ec 20          	sub    rsp,0x20
   140002ee8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002eec:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002ef0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002ef4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ef8:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002efb:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140002eff:	74 07                	je     140002f08 <_ValidateImageBase+0x28>
   140002f01:	b8 00 00 00 00       	mov    eax,0x0
   140002f06:	eb 4e                	jmp    140002f56 <_ValidateImageBase+0x76>
   140002f08:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f0c:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002f0f:	48 63 d0             	movsxd rdx,eax
   140002f12:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f16:	48 01 d0             	add    rax,rdx
   140002f19:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f1d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002f21:	8b 00                	mov    eax,DWORD PTR [rax]
   140002f23:	3d 50 45 00 00       	cmp    eax,0x4550
   140002f28:	74 07                	je     140002f31 <_ValidateImageBase+0x51>
   140002f2a:	b8 00 00 00 00       	mov    eax,0x0
   140002f2f:	eb 25                	jmp    140002f56 <_ValidateImageBase+0x76>
   140002f31:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002f35:	48 83 c0 18          	add    rax,0x18
   140002f39:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002f3d:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f41:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002f44:	66 3d 0b 02          	cmp    ax,0x20b
   140002f48:	74 07                	je     140002f51 <_ValidateImageBase+0x71>
   140002f4a:	b8 00 00 00 00       	mov    eax,0x0
   140002f4f:	eb 05                	jmp    140002f56 <_ValidateImageBase+0x76>
   140002f51:	b8 01 00 00 00       	mov    eax,0x1
   140002f56:	48 83 c4 20          	add    rsp,0x20
   140002f5a:	5d                   	pop    rbp
   140002f5b:	c3                   	ret

0000000140002f5c <_FindPESection>:
   140002f5c:	55                   	push   rbp
   140002f5d:	48 89 e5             	mov    rbp,rsp
   140002f60:	48 83 ec 20          	sub    rsp,0x20
   140002f64:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002f68:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002f6c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002f70:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002f73:	48 63 d0             	movsxd rdx,eax
   140002f76:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002f7a:	48 01 d0             	add    rax,rdx
   140002f7d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002f81:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002f88:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f8c:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002f90:	0f b7 d0             	movzx  edx,ax
   140002f93:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f97:	48 01 d0             	add    rax,rdx
   140002f9a:	48 83 c0 18          	add    rax,0x18
   140002f9e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002fa2:	eb 36                	jmp    140002fda <_FindPESection+0x7e>
   140002fa4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002fa8:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140002fab:	89 c0                	mov    eax,eax
   140002fad:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002fb1:	72 1e                	jb     140002fd1 <_FindPESection+0x75>
   140002fb3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002fb7:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140002fba:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002fbe:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002fc1:	01 d0                	add    eax,edx
   140002fc3:	89 c0                	mov    eax,eax
   140002fc5:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002fc9:	73 06                	jae    140002fd1 <_FindPESection+0x75>
   140002fcb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002fcf:	eb 1e                	jmp    140002fef <_FindPESection+0x93>
   140002fd1:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002fd5:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002fda:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002fde:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002fe2:	0f b7 c0             	movzx  eax,ax
   140002fe5:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002fe8:	72 ba                	jb     140002fa4 <_FindPESection+0x48>
   140002fea:	b8 00 00 00 00       	mov    eax,0x0
   140002fef:	48 83 c4 20          	add    rsp,0x20
   140002ff3:	5d                   	pop    rbp
   140002ff4:	c3                   	ret

0000000140002ff5 <_FindPESectionByName>:
   140002ff5:	55                   	push   rbp
   140002ff6:	48 89 e5             	mov    rbp,rsp
   140002ff9:	48 83 ec 40          	sub    rsp,0x40
   140002ffd:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140003001:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140003005:	48 89 c1             	mov    rcx,rax
   140003008:	e8 8b 05 00 00       	call   140003598 <strlen>
   14000300d:	48 83 f8 08          	cmp    rax,0x8
   140003011:	76 0a                	jbe    14000301d <_FindPESectionByName+0x28>
   140003013:	b8 00 00 00 00       	mov    eax,0x0
   140003018:	e9 98 00 00 00       	jmp    1400030b5 <_FindPESectionByName+0xc0>
   14000301d:	48 8b 05 7c 23 00 00 	mov    rax,QWORD PTR [rip+0x237c]        # 1400053a0 <.refptr.__ImageBase>
   140003024:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140003028:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000302c:	48 89 c1             	mov    rcx,rax
   14000302f:	e8 ac fe ff ff       	call   140002ee0 <_ValidateImageBase>
   140003034:	85 c0                	test   eax,eax
   140003036:	75 07                	jne    14000303f <_FindPESectionByName+0x4a>
   140003038:	b8 00 00 00 00       	mov    eax,0x0
   14000303d:	eb 76                	jmp    1400030b5 <_FindPESectionByName+0xc0>
   14000303f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140003043:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140003046:	48 63 d0             	movsxd rdx,eax
   140003049:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000304d:	48 01 d0             	add    rax,rdx
   140003050:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140003054:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   14000305b:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   14000305f:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140003063:	0f b7 d0             	movzx  edx,ax
   140003066:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   14000306a:	48 01 d0             	add    rax,rdx
   14000306d:	48 83 c0 18          	add    rax,0x18
   140003071:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003075:	eb 29                	jmp    1400030a0 <_FindPESectionByName+0xab>
   140003077:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000307b:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   14000307f:	41 b8 08 00 00 00    	mov    r8d,0x8
   140003085:	48 89 c1             	mov    rcx,rax
   140003088:	e8 13 05 00 00       	call   1400035a0 <strncmp>
   14000308d:	85 c0                	test   eax,eax
   14000308f:	75 06                	jne    140003097 <_FindPESectionByName+0xa2>
   140003091:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003095:	eb 1e                	jmp    1400030b5 <_FindPESectionByName+0xc0>
   140003097:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   14000309b:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   1400030a0:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400030a4:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   1400030a8:	0f b7 c0             	movzx  eax,ax
   1400030ab:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   1400030ae:	72 c7                	jb     140003077 <_FindPESectionByName+0x82>
   1400030b0:	b8 00 00 00 00       	mov    eax,0x0
   1400030b5:	48 83 c4 40          	add    rsp,0x40
   1400030b9:	5d                   	pop    rbp
   1400030ba:	c3                   	ret

00000001400030bb <__mingw_GetSectionForAddress>:
   1400030bb:	55                   	push   rbp
   1400030bc:	48 89 e5             	mov    rbp,rsp
   1400030bf:	48 83 ec 30          	sub    rsp,0x30
   1400030c3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400030c7:	48 8b 05 d2 22 00 00 	mov    rax,QWORD PTR [rip+0x22d2]        # 1400053a0 <.refptr.__ImageBase>
   1400030ce:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400030d2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030d6:	48 89 c1             	mov    rcx,rax
   1400030d9:	e8 02 fe ff ff       	call   140002ee0 <_ValidateImageBase>
   1400030de:	85 c0                	test   eax,eax
   1400030e0:	75 07                	jne    1400030e9 <__mingw_GetSectionForAddress+0x2e>
   1400030e2:	b8 00 00 00 00       	mov    eax,0x0
   1400030e7:	eb 1c                	jmp    140003105 <__mingw_GetSectionForAddress+0x4a>
   1400030e9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400030ed:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   1400030f1:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400030f5:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   1400030f9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030fd:	48 89 c1             	mov    rcx,rax
   140003100:	e8 57 fe ff ff       	call   140002f5c <_FindPESection>
   140003105:	48 83 c4 30          	add    rsp,0x30
   140003109:	5d                   	pop    rbp
   14000310a:	c3                   	ret

000000014000310b <__mingw_GetSectionCount>:
   14000310b:	55                   	push   rbp
   14000310c:	48 89 e5             	mov    rbp,rsp
   14000310f:	48 83 ec 30          	sub    rsp,0x30
   140003113:	48 8b 05 86 22 00 00 	mov    rax,QWORD PTR [rip+0x2286]        # 1400053a0 <.refptr.__ImageBase>
   14000311a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000311e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003122:	48 89 c1             	mov    rcx,rax
   140003125:	e8 b6 fd ff ff       	call   140002ee0 <_ValidateImageBase>
   14000312a:	85 c0                	test   eax,eax
   14000312c:	75 07                	jne    140003135 <__mingw_GetSectionCount+0x2a>
   14000312e:	b8 00 00 00 00       	mov    eax,0x0
   140003133:	eb 20                	jmp    140003155 <__mingw_GetSectionCount+0x4a>
   140003135:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003139:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   14000313c:	48 63 d0             	movsxd rdx,eax
   14000313f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003143:	48 01 d0             	add    rax,rdx
   140003146:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000314a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000314e:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140003152:	0f b7 c0             	movzx  eax,ax
   140003155:	48 83 c4 30          	add    rsp,0x30
   140003159:	5d                   	pop    rbp
   14000315a:	c3                   	ret

000000014000315b <_FindPESectionExec>:
   14000315b:	55                   	push   rbp
   14000315c:	48 89 e5             	mov    rbp,rsp
   14000315f:	48 83 ec 40          	sub    rsp,0x40
   140003163:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140003167:	48 8b 05 32 22 00 00 	mov    rax,QWORD PTR [rip+0x2232]        # 1400053a0 <.refptr.__ImageBase>
   14000316e:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140003172:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140003176:	48 89 c1             	mov    rcx,rax
   140003179:	e8 62 fd ff ff       	call   140002ee0 <_ValidateImageBase>
   14000317e:	85 c0                	test   eax,eax
   140003180:	75 07                	jne    140003189 <_FindPESectionExec+0x2e>
   140003182:	b8 00 00 00 00       	mov    eax,0x0
   140003187:	eb 78                	jmp    140003201 <_FindPESectionExec+0xa6>
   140003189:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000318d:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140003190:	48 63 d0             	movsxd rdx,eax
   140003193:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140003197:	48 01 d0             	add    rax,rdx
   14000319a:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000319e:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   1400031a5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400031a9:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   1400031ad:	0f b7 d0             	movzx  edx,ax
   1400031b0:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400031b4:	48 01 d0             	add    rax,rdx
   1400031b7:	48 83 c0 18          	add    rax,0x18
   1400031bb:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400031bf:	eb 2b                	jmp    1400031ec <_FindPESectionExec+0x91>
   1400031c1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400031c5:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   1400031c8:	25 00 00 00 20       	and    eax,0x20000000
   1400031cd:	85 c0                	test   eax,eax
   1400031cf:	74 12                	je     1400031e3 <_FindPESectionExec+0x88>
   1400031d1:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   1400031d6:	75 06                	jne    1400031de <_FindPESectionExec+0x83>
   1400031d8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400031dc:	eb 23                	jmp    140003201 <_FindPESectionExec+0xa6>
   1400031de:	48 83 6d 10 01       	sub    QWORD PTR [rbp+0x10],0x1
   1400031e3:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   1400031e7:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   1400031ec:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400031f0:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   1400031f4:	0f b7 c0             	movzx  eax,ax
   1400031f7:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   1400031fa:	72 c5                	jb     1400031c1 <_FindPESectionExec+0x66>
   1400031fc:	b8 00 00 00 00       	mov    eax,0x0
   140003201:	48 83 c4 40          	add    rsp,0x40
   140003205:	5d                   	pop    rbp
   140003206:	c3                   	ret

0000000140003207 <_GetPEImageBase>:
   140003207:	55                   	push   rbp
   140003208:	48 89 e5             	mov    rbp,rsp
   14000320b:	48 83 ec 30          	sub    rsp,0x30
   14000320f:	48 8b 05 8a 21 00 00 	mov    rax,QWORD PTR [rip+0x218a]        # 1400053a0 <.refptr.__ImageBase>
   140003216:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000321a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000321e:	48 89 c1             	mov    rcx,rax
   140003221:	e8 ba fc ff ff       	call   140002ee0 <_ValidateImageBase>
   140003226:	85 c0                	test   eax,eax
   140003228:	75 07                	jne    140003231 <_GetPEImageBase+0x2a>
   14000322a:	b8 00 00 00 00       	mov    eax,0x0
   14000322f:	eb 04                	jmp    140003235 <_GetPEImageBase+0x2e>
   140003231:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003235:	48 83 c4 30          	add    rsp,0x30
   140003239:	5d                   	pop    rbp
   14000323a:	c3                   	ret

000000014000323b <_IsNonwritableInCurrentImage>:
   14000323b:	55                   	push   rbp
   14000323c:	48 89 e5             	mov    rbp,rsp
   14000323f:	48 83 ec 40          	sub    rsp,0x40
   140003243:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140003247:	48 8b 05 52 21 00 00 	mov    rax,QWORD PTR [rip+0x2152]        # 1400053a0 <.refptr.__ImageBase>
   14000324e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003252:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003256:	48 89 c1             	mov    rcx,rax
   140003259:	e8 82 fc ff ff       	call   140002ee0 <_ValidateImageBase>
   14000325e:	85 c0                	test   eax,eax
   140003260:	75 07                	jne    140003269 <_IsNonwritableInCurrentImage+0x2e>
   140003262:	b8 00 00 00 00       	mov    eax,0x0
   140003267:	eb 3d                	jmp    1400032a6 <_IsNonwritableInCurrentImage+0x6b>
   140003269:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000326d:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140003271:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140003275:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140003279:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000327d:	48 89 c1             	mov    rcx,rax
   140003280:	e8 d7 fc ff ff       	call   140002f5c <_FindPESection>
   140003285:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140003289:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   14000328e:	75 07                	jne    140003297 <_IsNonwritableInCurrentImage+0x5c>
   140003290:	b8 00 00 00 00       	mov    eax,0x0
   140003295:	eb 0f                	jmp    1400032a6 <_IsNonwritableInCurrentImage+0x6b>
   140003297:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000329b:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   14000329e:	f7 d0                	not    eax
   1400032a0:	c1 e8 1f             	shr    eax,0x1f
   1400032a3:	0f b6 c0             	movzx  eax,al
   1400032a6:	48 83 c4 40          	add    rsp,0x40
   1400032aa:	5d                   	pop    rbp
   1400032ab:	c3                   	ret

00000001400032ac <__mingw_enum_import_library_names>:
   1400032ac:	55                   	push   rbp
   1400032ad:	48 89 e5             	mov    rbp,rsp
   1400032b0:	48 83 ec 50          	sub    rsp,0x50
   1400032b4:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400032b7:	48 8b 05 e2 20 00 00 	mov    rax,QWORD PTR [rip+0x20e2]        # 1400053a0 <.refptr.__ImageBase>
   1400032be:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400032c2:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400032c6:	48 89 c1             	mov    rcx,rax
   1400032c9:	e8 12 fc ff ff       	call   140002ee0 <_ValidateImageBase>
   1400032ce:	85 c0                	test   eax,eax
   1400032d0:	75 0a                	jne    1400032dc <__mingw_enum_import_library_names+0x30>
   1400032d2:	b8 00 00 00 00       	mov    eax,0x0
   1400032d7:	e9 ab 00 00 00       	jmp    140003387 <__mingw_enum_import_library_names+0xdb>
   1400032dc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400032e0:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   1400032e3:	48 63 d0             	movsxd rdx,eax
   1400032e6:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400032ea:	48 01 d0             	add    rax,rdx
   1400032ed:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400032f1:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400032f5:	8b 80 90 00 00 00    	mov    eax,DWORD PTR [rax+0x90]
   1400032fb:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400032fe:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140003302:	75 07                	jne    14000330b <__mingw_enum_import_library_names+0x5f>
   140003304:	b8 00 00 00 00       	mov    eax,0x0
   140003309:	eb 7c                	jmp    140003387 <__mingw_enum_import_library_names+0xdb>
   14000330b:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   14000330e:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003312:	48 89 c1             	mov    rcx,rax
   140003315:	e8 42 fc ff ff       	call   140002f5c <_FindPESection>
   14000331a:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000331e:	48 83 7d d8 00       	cmp    QWORD PTR [rbp-0x28],0x0
   140003323:	75 07                	jne    14000332c <__mingw_enum_import_library_names+0x80>
   140003325:	b8 00 00 00 00       	mov    eax,0x0
   14000332a:	eb 5b                	jmp    140003387 <__mingw_enum_import_library_names+0xdb>
   14000332c:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   14000332f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003333:	48 01 d0             	add    rax,rdx
   140003336:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000333a:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   14000333f:	75 07                	jne    140003348 <__mingw_enum_import_library_names+0x9c>
   140003341:	b8 00 00 00 00       	mov    eax,0x0
   140003346:	eb 3f                	jmp    140003387 <__mingw_enum_import_library_names+0xdb>
   140003348:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000334c:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000334f:	85 c0                	test   eax,eax
   140003351:	75 0b                	jne    14000335e <__mingw_enum_import_library_names+0xb2>
   140003353:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003357:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000335a:	85 c0                	test   eax,eax
   14000335c:	74 23                	je     140003381 <__mingw_enum_import_library_names+0xd5>
   14000335e:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   140003362:	7f 12                	jg     140003376 <__mingw_enum_import_library_names+0xca>
   140003364:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003368:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000336b:	89 c2                	mov    edx,eax
   14000336d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003371:	48 01 d0             	add    rax,rdx
   140003374:	eb 11                	jmp    140003387 <__mingw_enum_import_library_names+0xdb>
   140003376:	83 6d 10 01          	sub    DWORD PTR [rbp+0x10],0x1
   14000337a:	48 83 45 f8 14       	add    QWORD PTR [rbp-0x8],0x14
   14000337f:	eb c7                	jmp    140003348 <__mingw_enum_import_library_names+0x9c>
   140003381:	90                   	nop
   140003382:	b8 00 00 00 00       	mov    eax,0x0
   140003387:	48 83 c4 50          	add    rsp,0x50
   14000338b:	5d                   	pop    rbp
   14000338c:	c3                   	ret
   14000338d:	90                   	nop
   14000338e:	90                   	nop
   14000338f:	90                   	nop

0000000140003390 <_Unwind_Resume>:
   140003390:	ff 25 72 6e 00 00    	jmp    QWORD PTR [rip+0x6e72]        # 14000a208 <__IAT_start__>
   140003396:	90                   	nop
   140003397:	90                   	nop
   140003398:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000339f:	00 

00000001400033a0 <___chkstk_ms>:
   1400033a0:	51                   	push   rcx
   1400033a1:	50                   	push   rax
   1400033a2:	48 3d 00 10 00 00    	cmp    rax,0x1000
   1400033a8:	48 8d 4c 24 18       	lea    rcx,[rsp+0x18]
   1400033ad:	72 19                	jb     1400033c8 <___chkstk_ms+0x28>
   1400033af:	48 81 e9 00 10 00 00 	sub    rcx,0x1000
   1400033b6:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   1400033ba:	48 2d 00 10 00 00    	sub    rax,0x1000
   1400033c0:	48 3d 00 10 00 00    	cmp    rax,0x1000
   1400033c6:	77 e7                	ja     1400033af <___chkstk_ms+0xf>
   1400033c8:	48 29 c1             	sub    rcx,rax
   1400033cb:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   1400033cf:	58                   	pop    rax
   1400033d0:	59                   	pop    rcx
   1400033d1:	c3                   	ret
   1400033d2:	90                   	nop
   1400033d3:	90                   	nop
   1400033d4:	90                   	nop
   1400033d5:	90                   	nop
   1400033d6:	90                   	nop
   1400033d7:	90                   	nop
   1400033d8:	90                   	nop
   1400033d9:	90                   	nop
   1400033da:	90                   	nop
   1400033db:	90                   	nop
   1400033dc:	90                   	nop
   1400033dd:	90                   	nop
   1400033de:	90                   	nop
   1400033df:	90                   	nop

00000001400033e0 <_initterm_e>:
   1400033e0:	55                   	push   rbp
   1400033e1:	48 89 e5             	mov    rbp,rsp
   1400033e4:	48 83 ec 30          	sub    rsp,0x30
   1400033e8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400033ec:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400033f0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400033f4:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400033f8:	eb 29                	jmp    140003423 <_initterm_e+0x43>
   1400033fa:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400033fe:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140003401:	48 85 c0             	test   rax,rax
   140003404:	74 17                	je     14000341d <_initterm_e+0x3d>
   140003406:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000340a:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000340d:	ff d0                	call   rax
   14000340f:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140003412:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   140003416:	74 06                	je     14000341e <_initterm_e+0x3e>
   140003418:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000341b:	eb 15                	jmp    140003432 <_initterm_e+0x52>
   14000341d:	90                   	nop
   14000341e:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140003423:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003427:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   14000342b:	72 cd                	jb     1400033fa <_initterm_e+0x1a>
   14000342d:	b8 00 00 00 00       	mov    eax,0x0
   140003432:	48 83 c4 30          	add    rsp,0x30
   140003436:	5d                   	pop    rbp
   140003437:	c3                   	ret
   140003438:	90                   	nop
   140003439:	90                   	nop
   14000343a:	90                   	nop
   14000343b:	90                   	nop
   14000343c:	90                   	nop
   14000343d:	90                   	nop
   14000343e:	90                   	nop
   14000343f:	90                   	nop

0000000140003440 <__p__fmode>:
   140003440:	55                   	push   rbp
   140003441:	48 89 e5             	mov    rbp,rsp
   140003444:	48 8b 05 c5 1f 00 00 	mov    rax,QWORD PTR [rip+0x1fc5]        # 140005410 <.refptr.__imp__fmode>
   14000344b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000344e:	5d                   	pop    rbp
   14000344f:	c3                   	ret

0000000140003450 <__p__commode>:
   140003450:	55                   	push   rbp
   140003451:	48 89 e5             	mov    rbp,rsp
   140003454:	48 8b 05 a5 1f 00 00 	mov    rax,QWORD PTR [rip+0x1fa5]        # 140005400 <.refptr.__imp__commode>
   14000345b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000345e:	5d                   	pop    rbp
   14000345f:	c3                   	ret

0000000140003460 <__p___initenv>:
   140003460:	55                   	push   rbp
   140003461:	48 89 e5             	mov    rbp,rsp
   140003464:	48 8b 05 85 1f 00 00 	mov    rax,QWORD PTR [rip+0x1f85]        # 1400053f0 <.refptr.__imp___initenv>
   14000346b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000346e:	5d                   	pop    rbp
   14000346f:	c3                   	ret

0000000140003470 <_set_invalid_parameter_handler>:
   140003470:	55                   	push   rbp
   140003471:	48 89 e5             	mov    rbp,rsp
   140003474:	48 83 ec 10          	sub    rsp,0x10
   140003478:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000347c:	48 8d 05 0d 5d 00 00 	lea    rax,[rip+0x5d0d]        # 140009190 <handler>
   140003483:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003487:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000348b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000348f:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140003493:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003497:	48 87 10             	xchg   QWORD PTR [rax],rdx
   14000349a:	48 89 d0             	mov    rax,rdx
   14000349d:	48 83 c4 10          	add    rsp,0x10
   1400034a1:	5d                   	pop    rbp
   1400034a2:	c3                   	ret

00000001400034a3 <_get_invalid_parameter_handler>:
   1400034a3:	55                   	push   rbp
   1400034a4:	48 89 e5             	mov    rbp,rsp
   1400034a7:	48 8b 05 e2 5c 00 00 	mov    rax,QWORD PTR [rip+0x5ce2]        # 140009190 <handler>
   1400034ae:	5d                   	pop    rbp
   1400034af:	c3                   	ret

00000001400034b0 <_configthreadlocale>:
   1400034b0:	55                   	push   rbp
   1400034b1:	48 89 e5             	mov    rbp,rsp
   1400034b4:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400034b7:	83 7d 10 01          	cmp    DWORD PTR [rbp+0x10],0x1
   1400034bb:	75 07                	jne    1400034c4 <_configthreadlocale+0x14>
   1400034bd:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400034c2:	eb 05                	jmp    1400034c9 <_configthreadlocale+0x19>
   1400034c4:	b8 02 00 00 00       	mov    eax,0x2
   1400034c9:	5d                   	pop    rbp
   1400034ca:	c3                   	ret
   1400034cb:	90                   	nop
   1400034cc:	90                   	nop
   1400034cd:	90                   	nop
   1400034ce:	90                   	nop
   1400034cf:	90                   	nop

00000001400034d0 <__acrt_iob_func>:
   1400034d0:	55                   	push   rbp
   1400034d1:	48 89 e5             	mov    rbp,rsp
   1400034d4:	48 83 ec 20          	sub    rsp,0x20
   1400034d8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400034db:	e8 30 00 00 00       	call   140003510 <__iob_func>
   1400034e0:	48 89 c1             	mov    rcx,rax
   1400034e3:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   1400034e6:	48 89 d0             	mov    rax,rdx
   1400034e9:	48 01 c0             	add    rax,rax
   1400034ec:	48 01 d0             	add    rax,rdx
   1400034ef:	48 c1 e0 04          	shl    rax,0x4
   1400034f3:	48 01 c8             	add    rax,rcx
   1400034f6:	48 83 c4 20          	add    rsp,0x20
   1400034fa:	5d                   	pop    rbp
   1400034fb:	c3                   	ret
   1400034fc:	90                   	nop
   1400034fd:	90                   	nop
   1400034fe:	90                   	nop
   1400034ff:	90                   	nop

0000000140003500 <__C_specific_handler>:
   140003500:	ff 25 d2 6d 00 00    	jmp    QWORD PTR [rip+0x6dd2]        # 14000a2d8 <__imp___C_specific_handler>
   140003506:	90                   	nop
   140003507:	90                   	nop

0000000140003508 <__getmainargs>:
   140003508:	ff 25 d2 6d 00 00    	jmp    QWORD PTR [rip+0x6dd2]        # 14000a2e0 <__imp___getmainargs>
   14000350e:	90                   	nop
   14000350f:	90                   	nop

0000000140003510 <__iob_func>:
   140003510:	ff 25 da 6d 00 00    	jmp    QWORD PTR [rip+0x6dda]        # 14000a2f0 <__imp___iob_func>
   140003516:	90                   	nop
   140003517:	90                   	nop

0000000140003518 <__set_app_type>:
   140003518:	ff 25 da 6d 00 00    	jmp    QWORD PTR [rip+0x6dda]        # 14000a2f8 <__imp___set_app_type>
   14000351e:	90                   	nop
   14000351f:	90                   	nop

0000000140003520 <__setusermatherr>:
   140003520:	ff 25 da 6d 00 00    	jmp    QWORD PTR [rip+0x6dda]        # 14000a300 <__imp___setusermatherr>
   140003526:	90                   	nop
   140003527:	90                   	nop

0000000140003528 <_amsg_exit>:
   140003528:	ff 25 da 6d 00 00    	jmp    QWORD PTR [rip+0x6dda]        # 14000a308 <__imp__amsg_exit>
   14000352e:	90                   	nop
   14000352f:	90                   	nop

0000000140003530 <_cexit>:
   140003530:	ff 25 da 6d 00 00    	jmp    QWORD PTR [rip+0x6dda]        # 14000a310 <__imp__cexit>
   140003536:	90                   	nop
   140003537:	90                   	nop

0000000140003538 <_initterm>:
   140003538:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a328 <__imp__initterm>
   14000353e:	90                   	nop
   14000353f:	90                   	nop

0000000140003540 <_crt_atexit>:
   140003540:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a330 <__imp__crt_atexit>
   140003546:	90                   	nop
   140003547:	90                   	nop

0000000140003548 <abort>:
   140003548:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a338 <__imp_abort>
   14000354e:	90                   	nop
   14000354f:	90                   	nop

0000000140003550 <calloc>:
   140003550:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a340 <__imp_calloc>
   140003556:	90                   	nop
   140003557:	90                   	nop

0000000140003558 <exit>:
   140003558:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a348 <__imp_exit>
   14000355e:	90                   	nop
   14000355f:	90                   	nop

0000000140003560 <fflush>:
   140003560:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a350 <__imp_fflush>
   140003566:	90                   	nop
   140003567:	90                   	nop

0000000140003568 <fprintf>:
   140003568:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a358 <__imp_fprintf>
   14000356e:	90                   	nop
   14000356f:	90                   	nop

0000000140003570 <free>:
   140003570:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a360 <__imp_free>
   140003576:	90                   	nop
   140003577:	90                   	nop

0000000140003578 <malloc>:
   140003578:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a368 <__imp_malloc>
   14000357e:	90                   	nop
   14000357f:	90                   	nop

0000000140003580 <memcpy>:
   140003580:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a370 <__imp_memcpy>
   140003586:	90                   	nop
   140003587:	90                   	nop

0000000140003588 <setvbuf>:
   140003588:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a378 <__imp_setvbuf>
   14000358e:	90                   	nop
   14000358f:	90                   	nop

0000000140003590 <signal>:
   140003590:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a380 <__imp_signal>
   140003596:	90                   	nop
   140003597:	90                   	nop

0000000140003598 <strlen>:
   140003598:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a388 <__imp_strlen>
   14000359e:	90                   	nop
   14000359f:	90                   	nop

00000001400035a0 <strncmp>:
   1400035a0:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a390 <__imp_strncmp>
   1400035a6:	90                   	nop
   1400035a7:	90                   	nop

00000001400035a8 <vfprintf>:
   1400035a8:	ff 25 ea 6d 00 00    	jmp    QWORD PTR [rip+0x6dea]        # 14000a398 <__imp_vfprintf>
   1400035ae:	90                   	nop
   1400035af:	90                   	nop

00000001400035b0 <VirtualQuery>:
   1400035b0:	ff 25 12 6d 00 00    	jmp    QWORD PTR [rip+0x6d12]        # 14000a2c8 <__imp_VirtualQuery>
   1400035b6:	90                   	nop
   1400035b7:	90                   	nop

00000001400035b8 <VirtualProtect>:
   1400035b8:	ff 25 02 6d 00 00    	jmp    QWORD PTR [rip+0x6d02]        # 14000a2c0 <__imp_VirtualProtect>
   1400035be:	90                   	nop
   1400035bf:	90                   	nop

00000001400035c0 <TlsGetValue>:
   1400035c0:	ff 25 f2 6c 00 00    	jmp    QWORD PTR [rip+0x6cf2]        # 14000a2b8 <__imp_TlsGetValue>
   1400035c6:	90                   	nop
   1400035c7:	90                   	nop

00000001400035c8 <Sleep>:
   1400035c8:	ff 25 e2 6c 00 00    	jmp    QWORD PTR [rip+0x6ce2]        # 14000a2b0 <__imp_Sleep>
   1400035ce:	90                   	nop
   1400035cf:	90                   	nop

00000001400035d0 <SetUnhandledExceptionFilter>:
   1400035d0:	ff 25 d2 6c 00 00    	jmp    QWORD PTR [rip+0x6cd2]        # 14000a2a8 <__imp_SetUnhandledExceptionFilter>
   1400035d6:	90                   	nop
   1400035d7:	90                   	nop

00000001400035d8 <LoadLibraryA>:
   1400035d8:	ff 25 c2 6c 00 00    	jmp    QWORD PTR [rip+0x6cc2]        # 14000a2a0 <__imp_LoadLibraryA>
   1400035de:	90                   	nop
   1400035df:	90                   	nop

00000001400035e0 <LeaveCriticalSection>:
   1400035e0:	ff 25 b2 6c 00 00    	jmp    QWORD PTR [rip+0x6cb2]        # 14000a298 <__imp_LeaveCriticalSection>
   1400035e6:	90                   	nop
   1400035e7:	90                   	nop

00000001400035e8 <InitializeCriticalSection>:
   1400035e8:	ff 25 a2 6c 00 00    	jmp    QWORD PTR [rip+0x6ca2]        # 14000a290 <__imp_InitializeCriticalSection>
   1400035ee:	90                   	nop
   1400035ef:	90                   	nop

00000001400035f0 <GetProcAddress>:
   1400035f0:	ff 25 92 6c 00 00    	jmp    QWORD PTR [rip+0x6c92]        # 14000a288 <__imp_GetProcAddress>
   1400035f6:	90                   	nop
   1400035f7:	90                   	nop

00000001400035f8 <GetModuleHandleA>:
   1400035f8:	ff 25 82 6c 00 00    	jmp    QWORD PTR [rip+0x6c82]        # 14000a280 <__imp_GetModuleHandleA>
   1400035fe:	90                   	nop
   1400035ff:	90                   	nop

0000000140003600 <GetLastError>:
   140003600:	ff 25 72 6c 00 00    	jmp    QWORD PTR [rip+0x6c72]        # 14000a278 <__imp_GetLastError>
   140003606:	90                   	nop
   140003607:	90                   	nop

0000000140003608 <FreeLibrary>:
   140003608:	ff 25 62 6c 00 00    	jmp    QWORD PTR [rip+0x6c62]        # 14000a270 <__imp_FreeLibrary>
   14000360e:	90                   	nop
   14000360f:	90                   	nop

0000000140003610 <EnterCriticalSection>:
   140003610:	ff 25 52 6c 00 00    	jmp    QWORD PTR [rip+0x6c52]        # 14000a268 <__imp_EnterCriticalSection>
   140003616:	90                   	nop
   140003617:	90                   	nop

0000000140003618 <DeleteCriticalSection>:
   140003618:	ff 25 42 6c 00 00    	jmp    QWORD PTR [rip+0x6c42]        # 14000a260 <__imp_DeleteCriticalSection>
   14000361e:	90                   	nop
   14000361f:	90                   	nop

0000000140003620 <std::pmr::monotonic_buffer_resource::do_allocate(unsigned long long, unsigned long long)>:
   140003620:	53                   	push   rbx
   140003621:	48 83 ec 30          	sub    rsp,0x30
   140003625:	b8 01 00 00 00       	mov    eax,0x1
   14000362a:	48 85 d2             	test   rdx,rdx
   14000362d:	48 0f 45 c2          	cmovne rax,rdx
   140003631:	48 8b 51 10          	mov    rdx,QWORD PTR [rcx+0x10]
   140003635:	49 89 c1             	mov    r9,rax
   140003638:	48 39 c2             	cmp    rdx,rax
   14000363b:	72 53                	jb     140003690 <std::pmr::monotonic_buffer_resource::do_allocate(unsigned long long, unsigned long long)+0x70>
   14000363d:	4c 8b 51 08          	mov    r10,QWORD PTR [rcx+0x8]
   140003641:	4d 89 c3             	mov    r11,r8
   140003644:	48 89 d3             	mov    rbx,rdx
   140003647:	49 f7 db             	neg    r11
   14000364a:	4c 29 cb             	sub    rbx,r9
   14000364d:	4b 8d 44 02 ff       	lea    rax,[r10+r8*1-0x1]
   140003652:	4c 21 d8             	and    rax,r11
   140003655:	49 89 c3             	mov    r11,rax
   140003658:	4d 29 d3             	sub    r11,r10
   14000365b:	4c 39 db             	cmp    rbx,r11
   14000365e:	72 30                	jb     140003690 <std::pmr::monotonic_buffer_resource::do_allocate(unsigned long long, unsigned long long)+0x70>
   140003660:	4c 01 d2             	add    rdx,r10
   140003663:	48 89 41 08          	mov    QWORD PTR [rcx+0x8],rax
   140003667:	48 29 c2             	sub    rdx,rax
   14000366a:	48 89 51 10          	mov    QWORD PTR [rcx+0x10],rdx
   14000366e:	48 85 c0             	test   rax,rax
   140003671:	74 1d                	je     140003690 <std::pmr::monotonic_buffer_resource::do_allocate(unsigned long long, unsigned long long)+0x70>
   140003673:	4e 8d 04 08          	lea    r8,[rax+r9*1]
   140003677:	4c 29 ca             	sub    rdx,r9
   14000367a:	4c 89 41 08          	mov    QWORD PTR [rcx+0x8],r8
   14000367e:	48 89 51 10          	mov    QWORD PTR [rcx+0x10],rdx
   140003682:	48 83 c4 30          	add    rsp,0x30
   140003686:	5b                   	pop    rbx
   140003687:	c3                   	ret
   140003688:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000368f:	00 
   140003690:	4c 89 ca             	mov    rdx,r9
   140003693:	4c 89 4c 24 28       	mov    QWORD PTR [rsp+0x28],r9
   140003698:	48 89 4c 24 40       	mov    QWORD PTR [rsp+0x40],rcx
   14000369d:	e8 06 e4 ff ff       	call   140001aa8 <std::pmr::monotonic_buffer_resource::_M_new_buffer(unsigned long long, unsigned long long)>
   1400036a2:	48 8b 4c 24 40       	mov    rcx,QWORD PTR [rsp+0x40]
   1400036a7:	4c 8b 4c 24 28       	mov    r9,QWORD PTR [rsp+0x28]
   1400036ac:	48 8b 41 08          	mov    rax,QWORD PTR [rcx+0x8]
   1400036b0:	48 8b 51 10          	mov    rdx,QWORD PTR [rcx+0x10]
   1400036b4:	eb bd                	jmp    140003673 <std::pmr::monotonic_buffer_resource::do_allocate(unsigned long long, unsigned long long)+0x53>
   1400036b6:	90                   	nop
   1400036b7:	90                   	nop
   1400036b8:	90                   	nop
   1400036b9:	90                   	nop
   1400036ba:	90                   	nop
   1400036bb:	90                   	nop
   1400036bc:	90                   	nop
   1400036bd:	90                   	nop
   1400036be:	90                   	nop
   1400036bf:	90                   	nop

00000001400036c0 <std::pmr::monotonic_buffer_resource::do_deallocate(void*, unsigned long long, unsigned long long)>:
   1400036c0:	c3                   	ret
   1400036c1:	90                   	nop
   1400036c2:	90                   	nop
   1400036c3:	90                   	nop
   1400036c4:	90                   	nop
   1400036c5:	90                   	nop
   1400036c6:	90                   	nop
   1400036c7:	90                   	nop
   1400036c8:	90                   	nop
   1400036c9:	90                   	nop
   1400036ca:	90                   	nop
   1400036cb:	90                   	nop
   1400036cc:	90                   	nop
   1400036cd:	90                   	nop
   1400036ce:	90                   	nop
   1400036cf:	90                   	nop

00000001400036d0 <default_push() [clone .cold]>:
   1400036d0:	48 8d 0d 79 19 00 00 	lea    rcx,[rip+0x1979]        # 140005050 <.rdata>
   1400036d7:	e8 bc e3 ff ff       	call   140001a98 <std::__throw_length_error(char const*)>
   1400036dc:	48 89 c3             	mov    rbx,rax
   1400036df:	4d 85 e4             	test   r12,r12
   1400036e2:	74 0e                	je     1400036f2 <default_push() [clone .cold]+0x22>
   1400036e4:	48 89 ea             	mov    rdx,rbp
   1400036e7:	4c 89 e1             	mov    rcx,r12
   1400036ea:	4c 29 e2             	sub    rdx,r12
   1400036ed:	e8 9e e3 ff ff       	call   140001a90 <operator delete(void*, unsigned long long)>
   1400036f2:	48 89 d9             	mov    rcx,rbx
   1400036f5:	e8 96 fc ff ff       	call   140003390 <_Unwind_Resume>
   1400036fa:	90                   	nop

00000001400036fb <pmr_push() [clone .cold]>:
   1400036fb:	48 8d 0d 4e 19 00 00 	lea    rcx,[rip+0x194e]        # 140005050 <.rdata>
   140003702:	e8 91 e3 ff ff       	call   140001a98 <std::__throw_length_error(char const*)>
   140003707:	48 89 c6             	mov    rsi,rax
   14000370a:	48 89 d9             	mov    rcx,rbx
   14000370d:	e8 8e e3 ff ff       	call   140001aa0 <std::pmr::monotonic_buffer_resource::~monotonic_buffer_resource()>
   140003712:	48 89 f1             	mov    rcx,rsi
   140003715:	e8 76 fc ff ff       	call   140003390 <_Unwind_Resume>
   14000371a:	90                   	nop
   14000371b:	90                   	nop
   14000371c:	90                   	nop
   14000371d:	90                   	nop
   14000371e:	90                   	nop
   14000371f:	90                   	nop

0000000140003720 <main>:
   140003720:	48 83 ec 28          	sub    rsp,0x28
   140003724:	e8 4e e4 ff ff       	call   140001b77 <__main>
   140003729:	e8 32 e0 ff ff       	call   140001760 <default_push()>
   14000372e:	e8 5d e1 ff ff       	call   140001890 <pmr_push()>
   140003733:	31 c0                	xor    eax,eax
   140003735:	48 83 c4 28          	add    rsp,0x28
   140003739:	c3                   	ret
   14000373a:	90                   	nop
   14000373b:	90                   	nop
   14000373c:	90                   	nop
   14000373d:	90                   	nop
   14000373e:	90                   	nop
   14000373f:	90                   	nop

0000000140003740 <register_frame_ctor>:
   140003740:	e9 2b df ff ff       	jmp    140001670 <__gcc_register_frame>
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
