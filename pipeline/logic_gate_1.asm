section .text
global _start

_start:
    ; load 'a' into register eax
    mov eax, 2
    
    cmp eax, 1
    jle else_block
    ret

else_block:
    xor eax, eax
    inc eax
    ret