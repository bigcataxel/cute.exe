section .text
    global _start
_start:
    ; load the value to be added into register eax
    mov eax, 9
    ; add 9 to it
    add eax, [rel a]
    ; exit the program
    mov eax, 60
    xor edi, edi
    syscall

section .data
a: dword 12345678h