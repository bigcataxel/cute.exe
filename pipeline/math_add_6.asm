section .text
    global _start
_start:
    ; load the value to be added into register eax
    mov eax, 6
    
    ; add 6 to the value in eax and store it back in eax
    add eax, [rel a]
    
    ; exit the program by calling sys_exit system call
    mov eax, 0x3c
    xor edi, edi
    syscall

section .data
a: dword 42 ; this is just an example. Replace it with your actual value.