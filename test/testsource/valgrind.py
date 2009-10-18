#!/bin/env python
import commands
import os
import sys
# Valgrind wrapper that renames the file that's created so we can
# use it to test instrumentation

# This just fakes it and produces a file called cachegrind.out

contents = """desc: I1 cache:         16384 B, 32 B, 8-way associative
desc: D1 cache:         8192 B, 64 B, 4-way associative
desc: L2 cache:         524288 B, 64 B, 8-way associative
cmd: ./loop
events: Ir I1mr I2mr Dr D1mr D2mr Dw D1mw D2mw
fl=loop.c
fn=do_sum
4 3 0 0 0 0 0 1 0 0
6 1 0 0 0 0 0 1 0 0
7 6005 0 0 3002 0 0 1 0 0
8 3000 0 0 2000 0 0 0 0 0
10 1 0 0 1 0 0 0 0 0
12 2 0 0 2 0 0 0 0 0
fn=main
15 6 2 0 0 0 0 1 0 0
18 5 0 0 0 0 0 3 0 0
19 5 0 0 1 0 0 3 0 0
21 1 0 0 0 0 0 0 0 0
22 2 0 0 2 0 0 0 0 0
fl=???
fn=__libc_start_main
0 64 8 5 16 1 0 26 0 0
fn=__GI___fxstat64
0 111 4 2 39 0 0 15 1 1
fn=open_path
0 563 20 11 204 0 0 177 4 4
fn=_dl_important_hwcaps
0 1245 28 14 360 0 0 116 2 2
fn=malloc
0 308 1 1 88 0 0 132 1 0
fn=_dl_sysdep_start_cleanup
0 4 1 1 2 0 0 1 0 0
fn=version_check_doit
0 19 3 2 7 0 0 5 0 0
fn=fillin_rpath
0 183 17 9 58 0 0 46 2 2
fn=__libc_memalign
0 760 7 3 233 0 0 195 4 4
fn=_fini
0 16 2 2 5 1 0 4 0 0
fn=_IO_default_xsputn_internal
0 130 5 4 31 0 0 19 1 0
fn=_IO_printf
0 18 3 2 6 2 0 7 0 0
fn=__init_misc
0 30 3 2 9 1 0 9 1 0
fn=_dl_debug_initialize
0 32 1 1 11 0 0 10 1 0
fn=_dl_check_map_versions_internal
0 1876 29 16 709 19 11 319 9 9
fn=_dl_setup_hash
0 60 2 2 20 4 4 16 1 1
fn=rtld_lock_default_unlock_recursive
0 6 1 1 4 0 0 1 0 0
fn=dl_main
0 1048 108 63 314 30 12 193 17 10
fn=__cxa_finalize
0 34 5 3 10 1 0 8 0 0
fn=_dl_debug_state_internal
0 12 0 0 6 0 0 3 0 0
fn=_IO_setb_internal
0 65 4 2 22 0 0 17 0 0
fn=__new_exitfn
0 100 7 4 23 2 1 12 0 0
fn=memset
0 551 2 1 30 0 0 471 31 31
fn=_IO_doallocbuf_internal
0 24 3 2 10 1 0 6 1 0
fn=_IO_vfprintf_internal
0 428 63 38 118 11 5 78 4 0
fn=fixup
0 240 9 5 90 12 0 45 1 0
fn=_dl_next_tls_modid
0 19 2 2 7 1 0 6 1 1
fn=_IO_file_stat_internal
0 13 2 2 5 0 0 5 0 0
fn=__libc_csu_fini
0 18 2 1 4 0 0 4 0 0
fn=open
0 183 2 1 60 0 0 30 0 0
fn=_dl_map_object_internal
0 848 47 25 262 3 0 207 6 5
fn=__strsep_g
0 2530 3 1 643 1 1 14 0 0
fn=uname
0 8 1 1 2 0 0 0 0 0
fn=_dl_fini
0 340 18 10 149 13 0 46 0 0
fn=calloc
0 120 2 1 40 0 0 40 0 0
fn=__GI__exit
0 3 1 1 1 0 0 0 0 0
fn=_IO_file_doallocate_internal
0 54 7 4 12 1 0 20 1 0
fn=_dl_relocate_object_internal
0 21769 56 31 10606 583 474 1733 14 0
fn=new_do_write
0 48 6 3 19 0 0 15 0 0
fn=do_lookup
0 1039 16 9 472 37 9 144 0 0
fn=brk
0 18 3 2 4 0 0 4 0 0
fn=__libc_global_ctors
0 22 2 1 6 1 0 5 0 0
fn=strrchr
0 61 9 7 7 1 0 2 0 0
fn=_dl_map_object_from_fd
0 1786 86 45 512 7 7 244 14 13
fn=_IO_file_write@@GLIBC_2.1
0 38 5 2 15 0 0 7 0 0
fn=strchr
0 627 13 6 62 2 1 6 0 0
fn=_init
0 43 5 3 16 4 1 14 3 3
fn=_dl_lookup_symbol_internal
0 841 15 9 166 5 2 97 0 0
fn=_IO_cleanup
0 59 5 3 16 0 0 14 0 0
fn=exit
0 82 7 4 22 1 1 17 0 0
fn=munmap
0 18 3 2 6 0 0 0 0 0
fn=_dl_determine_tlsoffset
0 85 11 6 34 0 0 17 0 0
fn=_dl_next_ld_env_entry
0 297 3 2 102 17 17 8 0 0
fn=process_envvars
0 259 15 9 80 1 1 18 3 3
fn=_IO_file_sync@@GLIBC_2.1
0 30 4 2 10 0 0 7 0 0
fn=_IO_flush_all_lockp
0 128 14 8 42 8 2 20 0 0
fn=_dl_lookup_versioned_symbol_internal
0 17133 14 7 3837 136 79 2225 8 4
fn=_dl_start
0 610 42 21 153 15 14 85 9 9
fn=_dl_sysdep_start
0 583 28 15 141 11 8 46 7 7
fn=__GI___xstat64
0 310 6 4 90 0 0 47 0 0
fn=__i686.get_pc_thunk.cx
0 18 0 0 18 0 0 0 0 0
fn=strcmp
0 13570 1 1 4967 232 92 0 0 0
fn=add_name_to_object
0 52 5 3 10 0 0 23 0 0
fn=_dl_catch_error_internal
0 129 6 3 42 0 0 60 2 0
fn=_IO_do_write@@GLIBC_2.1
0 36 3 2 10 0 0 8 0 0
fn=mempcpy
0 441 2 1 207 2 1 103 6 6
fn=_dl_new_object
0 429 19 10 121 1 1 117 10 10
fn=sbrk
0 25 3 2 8 0 0 5 0 0
fn=_IO_file_overflow@@GLIBC_2.1
0 98 10 6 28 0 0 29 0 0
fn=_dl_allocate_tls_storage
0 44 5 3 9 0 0 19 0 0
fn=_dl_load_cache_lookup
0 509 30 16 181 11 11 74 0 0
fn=__GI__setjmp
0 12 2 1 3 0 0 7 0 0
fn=strlen
0 1187 6 3 176 2 2 0 0 0
fn=_IO_file_setbuf@@GLIBC_2.1
0 31 4 3 8 0 0 14 0 0
fn=__write_nocancel
0 10 1 0 5 0 0 1 0 0
fn=__cxa_atexit_internal
0 42 2 1 12 0 0 16 1 1
fn=__libc_csu_init
0 22 3 2 5 0 0 5 0 0
fn=_dl_runtime_resolve
0 30 1 1 18 0 0 12 0 0
fn=_dl_init_internal
0 174 19 11 68 7 0 30 0 0
fn=_dl_init_paths
0 763 20 11 92 1 1 77 2 2
fn=read
0 20 1 1 10 0 0 2 0 0
fn=_dl_unload_cache_internal
0 21 2 1 5 1 0 7 0 0
fn=do_lookup_versioned
0 25352 21 11 11379 551 223 3385 14 1
fn=???
0 953 33 17 826 7 0 60 1 1
fn=__GI__dl_allocate_tls_init
0 84 10 6 31 4 0 19 1 0
fn=openaux
0 90 4 2 33 0 0 24 0 0
fn=_IO_default_setbuf
0 41 7 3 11 0 0 18 0 0
fn=rtld_lock_default_lock_recursive
0 6 1 1 4 0 0 1 0 0
fn=__fxstat64@@GLIBC_2.2
0 18 2 2 5 0 0 3 1 0
fn=_setjmp
0 36 2 1 9 0 0 21 0 0
fn=_dl_sysdep_read_whole_file
0 71 6 3 14 0 0 35 0 0
fn=__find_specmb
0 181 4 2 46 1 1 25 1 0
fn=_dl_check_all_versions
0 83 3 2 26 0 0 12 0 0
fn=_IO_file_xsputn@@GLIBC_2.1
0 233 10 6 78 0 0 41 0 0
fn=_dl_map_object_deps_internal
0 1487 48 27 492 9 1 168 4 3
fn=open_verify
0 490 14 8 196 2 2 119 1 1
fn=_dl_receive_error
0 31 4 3 12 0 0 16 0 0
fn=write
0 2 1 1 1 0 0 0 0 0
fn=_IO_check_libio
0 15 3 2 5 1 0 4 0 0
fn=memcpy
0 194 2 1 122 0 0 82 5 5
fn=__unregister_atfork
0 19 3 2 7 2 1 5 0 0
fn=close
0 24 1 1 6 0 0 0 0 0
fn=mmap
0 79 3 2 18 0 0 4 0 0
fn=match_symbol
0 579 8 4 217 9 6 96 1 1
fn=_dl_cache_libcmp
0 1449 9 4 474 9 9 112 0 0
fn=_dl_initial_error_catch_tsd
0 36 1 0 12 0 0 12 0 0
summary: 116196 1138 639 45063 1785 1001 11959 197 140
"""

open('cachegrind.out','w').write(contents)



