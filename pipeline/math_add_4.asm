section .text
    global _start
_start:
    ; load the value to be added into register eax
    mov eax, 0x10        ; assuming a is 0x10 for example
    
    ; add 4 to it
    add eax, 0x4         

    ; exit the program
    xor edi, edi         ; syscall number for sys_exit = 0x3c
    mov eax, 0x3c        ; syscall number for sys_exit = 0x3c
    syscall