section     .text
global      _start

_start:
    ; load the value to be added into register eax
    mov         eax, 15   ; assuming we have a value in eax (or any other r[1D[K
register) that needs to be incremented by 10.
                          ; if you want to add a constant number like 10 di[2D[K
directly, use mov eax, 10 instead of the line above.
    add         eax, 10   ; adds 10 to the value in eax
                          
    ; exit the program gracefully
    mov         eax, 60   ; syscall number for sys_exit is 60
    xor         edi, edi  ; exit code of 0
    syscall               ; make the system call