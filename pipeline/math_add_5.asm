section     .text
global      _start

_start:
    ; load the value to be added into register eax
    mov         eax, 5
    add         eax, [rel a]
    ; exit system call number for x64 Linux is 0x3c
    mov         edi, 0
    mov         eax, 0x3c
    syscall

section     .data
a dd          10