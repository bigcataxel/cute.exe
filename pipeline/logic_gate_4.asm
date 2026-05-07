section .text
global _start

_start:
    ; load 'a' into register eax
    mov eax, 5   ; replace with actual value or instruction to get it
    
    cmp eax, 4
    jle return0
    ret
return1:
    mov eax, 1
    ret
return0:
    xor eax, eax
    ret