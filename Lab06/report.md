# Lab 06

## Heap out-of-bounds read/write

### 有問題的程式碼
```c
#include <stdio.h>
#include <stdlib.h>

void main()
{
    int *a = malloc(sizeof(int) * 8);
    for (int i = 0; i < 8; i++)
    {
        *(a + i) = i;
    }

    // out-of-bound read;
    int b = *(a + 8);
    // out-of-bound write;
    *(a + 9) = 33;
}
```

### Asan report (無法偵測出錯誤)

### valgrind report (可偵測出錯誤)
```
==3979== Memcheck, a memory error detector
==3979== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==3979== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==3979== Command: ./ex1.out
==3979==
==3979== error calling PR_SET_PTRACER, vgdb might block
==3979== Invalid read of size 4
==3979==    at 0x109193: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex1.out)
==3979==  Address 0x4a8b060 is 0 bytes after a block of size 32 alloc'd
==3979==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==3979==    by 0x10915E: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex1.out)
==3979==
==3979== Invalid write of size 4
==3979==    at 0x1091A1: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex1.out)
==3979==  Address 0x4a8b064 is 4 bytes after a block of size 32 alloc'd
==3979==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==3979==    by 0x10915E: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex1.out)
==3979==
==3979==
==3979== HEAP SUMMARY:
==3979==     in use at exit: 32 bytes in 1 blocks
==3979==   total heap usage: 1 allocs, 0 frees, 32 bytes allocated
==3979==
==3979== LEAK SUMMARY:
==3979==    definitely lost: 32 bytes in 1 blocks
==3979==    indirectly lost: 0 bytes in 0 blocks
==3979==      possibly lost: 0 bytes in 0 blocks
==3979==    still reachable: 0 bytes in 0 blocks
==3979==         suppressed: 0 bytes in 0 blocks
==3979== Rerun with --leak-check=full to see details of leaked memory
==3979==
==3979== For lists of detected and suppressed errors, rerun with: -s
==3979== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)
```

## Stack out-of-bounds read/write

### 有問題的程式碼
```c
#include <stdio.h>
#include <stdlib.h>

void main()
{
    int a[] = {2, 3, 4};

    // out-of-bound read
    int b = *(a + 3);
    // out-of-bound write
    *(a + 4) = 33;
}
```

### Asan report (可偵測出錯誤)
```
=================================================================
==3745==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffffe5d5c90 at pc 0x7f637e07631d bp 0x7ffffe5d5c50 sp 0x7ffffe5d5c40
WRITE of size 4 at 0x7ffffe5d5c90 thread T0
    #0 0x7f637e07631c in main /home/ericlin/NYCU-Software-Testing-2023/Lab06/example2.c:13
    #1 0x7f637d439d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f637d439e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x7f637e076104 in _start (/home/ericlin/NYCU-Software-Testing-2023/Lab06/ex2.out+0x1104)

Address 0x7ffffe5d5c90 is located in stack of thread T0 at offset 48 in frame
    #0 0x7f637e0761d8 in main /home/ericlin/NYCU-Software-Testing-2023/Lab06/example2.c:7

  This frame has 1 object(s):
    [32, 44) 'a' (line 8) <== Memory access at offset 48 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /home/ericlin/NYCU-Software-Testing-2023/Lab06/example2.c:13 in main
Shadow bytes around the buggy address:
  0x10007fcb2b40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fcb2b50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fcb2b60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fcb2b70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fcb2b80: 00 00 00 00 00 00 00 00 00 00 00 00 f1 f1 f1 f1
=>0x10007fcb2b90: 00 04[f3]f3 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fcb2ba0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fcb2bb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fcb2bc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fcb2bd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fcb2be0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==3745==ABORTING
```

### valgrind report (可偵測出錯誤)
```
==4011== Memcheck, a memory error detector
==4011== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==4011== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==4011== Command: ./ex2.out
==4011==
==4011== error calling PR_SET_PTRACER, vgdb might block
*** stack smashing detected ***: terminated
==4011==
==4011== Process terminating with default action of signal 6 (SIGABRT)
==4011==    at 0x48F6A7C: __pthread_kill_implementation (pthread_kill.c:44)
==4011==    by 0x48F6A7C: __pthread_kill_internal (pthread_kill.c:78)
==4011==    by 0x48F6A7C: pthread_kill@@GLIBC_2.34 (pthread_kill.c:89)
==4011==    by 0x48A2475: raise (raise.c:26)
==4011==    by 0x48887F2: abort (abort.c:79)
==4011==    by 0x48E96F5: __libc_message (libc_fatal.c:155)
==4011==    by 0x4996769: __fortify_fail (fortify_fail.c:26)
==4011==    by 0x4996735: __stack_chk_fail (stack_chk_fail.c:24)
==4011==    by 0x10919A: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex2.out)
==4011==
==4011== HEAP SUMMARY:
==4011==     in use at exit: 0 bytes in 0 blocks
==4011==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==4011==
==4011== All heap blocks were freed -- no leaks are possible
==4011==
==4011== For lists of detected and suppressed errors, rerun with: -s
==4011== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
Aborted (core dumped)
```

## Global out-of-bounds read/write

### 有問題的程式碼
```c
#include <stdio.h>
#include <stdlib.h>

int a[] = {2, 3, 4};

void main()
{
    // out-of-bound read
    int b = *(a + 3);
    // out-of-bound write
    *(a + 4) = 33;
}
```

### Asan report (可偵測出錯誤)
```
=================================================================
==3751==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7fb57c1ff030 at pc 0x7fb57c1fc1fe bp 0x7fffc96a2ed0 sp 0x7fffc96a2ec0
WRITE of size 4 at 0x7fb57c1ff030 thread T0
    #0 0x7fb57c1fc1fd in main /home/ericlin/NYCU-Software-Testing-2023/Lab06/example3.c:13
    #1 0x7fb57b5b9d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7fb57b5b9e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x7fb57c1fc104 in _start (/home/ericlin/NYCU-Software-Testing-2023/Lab06/ex3.out+0x1104)

0x7fb57c1ff030 is located 4 bytes to the right of global variable 'a' defined in 'example3.c:6:5' (0x7fb57c1ff020) of size 12
SUMMARY: AddressSanitizer: global-buffer-overflow /home/ericlin/NYCU-Software-Testing-2023/Lab06/example3.c:13 in main
Shadow bytes around the buggy address:
  0x0ff72f837db0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff72f837dc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff72f837dd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff72f837de0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff72f837df0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0ff72f837e00: 00 00 00 00 00 04[f9]f9 f9 f9 f9 f9 00 00 00 00
  0x0ff72f837e10: f9 f9 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
  0x0ff72f837e20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff72f837e30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff72f837e40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff72f837e50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==3751==ABORTING
```

### valgrind report (可偵測出錯誤)
```
==4095== Memcheck, a memory error detector
==4095== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==4095== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==4095== Command: ./ex3.out
==4095==
==4095== error calling PR_SET_PTRACER, vgdb might block
==4095==
==4095== HEAP SUMMARY:
==4095==     in use at exit: 0 bytes in 0 blocks
==4095==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==4095==
==4095== All heap blocks were freed -- no leaks are possible
==4095==
==4095== For lists of detected and suppressed errors, rerun with: -s
==4095== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

## Use-after-free

### 有問題的程式碼
```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
    int *a = malloc(sizeof(int) * 8);
    free(a);

    return a[3];
}
```

### Asan report (可偵測出錯誤)
```
=================================================================
==3611==ERROR: AddressSanitizer: heap-use-after-free on address 0x60300000004c at pc 0x7f30f5fa1210 bp 0x7fffccb63f60 sp 0x7fffccb63f50
READ of size 4 at 0x60300000004c thread T0
    #0 0x7f30f5fa120f in main /home/ericlin/NYCU-Software-Testing-2023/Lab06/example4.c:11
    #1 0x7f30f5359d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f30f5359e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x7f30f5fa1104 in _start (/home/ericlin/NYCU-Software-Testing-2023/Lab06/ex4.out+0x1104)

0x60300000004c is located 12 bytes inside of 32-byte region [0x603000000040,0x603000000060)
freed by thread T0 here:
    #0 0x7f30f5614517 in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:127
    #1 0x7f30f5fa11e2 in main /home/ericlin/NYCU-Software-Testing-2023/Lab06/example4.c:9

previously allocated by thread T0 here:
    #0 0x7f30f5614867 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x7f30f5fa11d7 in main /home/ericlin/NYCU-Software-Testing-2023/Lab06/example4.c:8

SUMMARY: AddressSanitizer: heap-use-after-free /home/ericlin/NYCU-Software-Testing-2023/Lab06/example4.c:11 in main
Shadow bytes around the buggy address:
  0x0c067fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c067fff8000: fa fa 00 00 00 fa fa fa fd[fd]fd fd fa fa fa fa
  0x0c067fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==3611==ABORTING
```

### valgrind report (可偵測出錯誤)
```
==4149== Memcheck, a memory error detector
==4149== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==4149== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==4149== Command: ./ex4.out
==4149==
==4149== error calling PR_SET_PTRACER, vgdb might block
==4149== Invalid read of size 4
==4149==    at 0x109193: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex4.out)
==4149==  Address 0x4a8b04c is 12 bytes inside a block of size 32 free'd
==4149==    at 0x484B27F: free (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==4149==    by 0x10918E: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex4.out)
==4149==  Block was alloc'd at
==4149==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==4149==    by 0x10917E: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex4.out)
==4149==
==4149==
==4149== HEAP SUMMARY:
==4149==     in use at exit: 0 bytes in 0 blocks
==4149==   total heap usage: 1 allocs, 1 frees, 32 bytes allocated
==4149==
==4149== All heap blocks were freed -- no leaks are possible
==4149==
==4149== For lists of detected and suppressed errors, rerun with: -s
==4149== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

## Use-after-return

### 有問題的程式碼
```c
#include <stdio.h>
#include <stdlib.h>

int *func()
{
    int x[] = {2, 3, 4};
    return x;
}

int main()
{
    int *a = func();

    return a[2];
}
```

### Asan report (可偵測出錯誤)
```
=================================================================
==3634==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000008 (pc 0x7f6c9e0f2372 bp 0x000000000001 sp 0x7fffc3ccac20 T0)
==3634==The signal is caused by a READ memory access.
==3634==Hint: address points to the zero page.
    #0 0x7f6c9e0f2372 in main /home/ericlin/NYCU-Software-Testing-2023/Lab06/example5.c:17
    #1 0x7f6c9d4a9d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f6c9d4a9e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x7f6c9e0f2124 in _start (/home/ericlin/NYCU-Software-Testing-2023/Lab06/ex5.out+0x1124)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /home/ericlin/NYCU-Software-Testing-2023/Lab06/example5.c:17 in main
==3634==ABORTING
ericlin@LAPTOP-JU3SMUDU:~/NYCU-Software-Testing-2023/Lab06$ gcc example4.c -o ex4.out
ericlin@LAPTOP-JU3SMUDU:~/NYCU-Software-Testing-2023/Lab06$ valgrind ./ex4.out
==3640== Memcheck, a memory error detector
==3640== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==3640== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==3640== Command: ./ex4.out
==3640==
==3640== error calling PR_SET_PTRACER, vgdb might block
==3640== Invalid read of size 4
==3640==    at 0x109193: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex4.out)
==3640==  Address 0x4a8b04c is 12 bytes inside a block of size 32 free'd
==3640==    at 0x484B27F: free (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==3640==    by 0x10918E: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex4.out)
==3640==  Block was alloc'd at
==3640==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==3640==    by 0x10917E: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex4.out)
==3640==
==3640==
==3640== HEAP SUMMARY:
==3640==     in use at exit: 0 bytes in 0 blocks
==3640==   total heap usage: 1 allocs, 1 frees, 32 bytes allocated
==3640==
==3640== All heap blocks were freed -- no leaks are possible
==3640==
==3640== For lists of detected and suppressed errors, rerun with: -s
==3640== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

### valgrind report (可偵測出錯誤)
```
==4251== Memcheck, a memory error detector
==4251== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==4251== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==4251== Command: ./ex5.out
==4251==
==4251== error calling PR_SET_PTRACER, vgdb might block
==4251== Invalid read of size 4
==4251==    at 0x1091B2: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex5.out)
==4251==  Address 0x8 is not stack'd, malloc'd or (recently) free'd
==4251==
==4251==
==4251== Process terminating with default action of signal 11 (SIGSEGV)
==4251==  Access not within mapped region at address 0x8
==4251==    at 0x1091B2: main (in /home/ericlin/NYCU-Software-Testing-2023/Lab06/ex5.out)
==4251==  If you believe this happened as a result of a stack
==4251==  overflow in your program's main thread (unlikely but
==4251==  possible), you can try to increase the size of the
==4251==  main thread stack using the --main-stacksize= flag.
==4251==  The main thread stack size used in this run was 8388608.
==4251==
==4251== HEAP SUMMARY:
==4251==     in use at exit: 0 bytes in 0 blocks
==4251==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==4251==
==4251== All heap blocks were freed -- no leaks are possible
==4251==
==4251== For lists of detected and suppressed errors, rerun with: -s
==4251== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
Segmentation fault (core dumped)
```

## Try cross Asan redzone read/write

### 有問題的程式碼
```c
#include <stdio.h>
#include <stdlib.h>

void main()
{
    int a[] = {2, 3, 4};

    // out-of-bound read
    int b = a[33];
    // out-of-bound write
    a[34] = 33;
}
```

### Asan report (無法偵測出錯誤)
