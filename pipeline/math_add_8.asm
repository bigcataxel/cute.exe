section     .text
global      _start

_start:
    ; load the value to be added into register eax
    mov         eax, 0x10        ; assuming that 'a' is 0x10 (change this a[1D[K
as per your requirement)

    ; add 8 to the value in eax and store it back in eax
    add         eax, 0x8

    ; exit the program by calling sys_exit system call number
    mov         edi, eax        ; move result into 'edi' for sys_exit
    mov         eax, 0x3c       ; syscall number for sys_exit is 60 in x86_[4D[K
x86_64 Linux
    syscall