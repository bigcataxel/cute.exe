section .text
global _start

_start:
    ; load 'a' into register eax
    mov eax, 2
    
    cmp eax, 2
    jle else
    ret
else:
    xor eax, eax
    inc eax
    ret