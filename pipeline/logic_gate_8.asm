section .text
global _start

_start:
    ; load 'a' into register eax
    mov eax, 0x12345678
    
    ; compare eax with 8
    cmp eax, 8
    
    ; if a > 8 then set EFLAGS to true (setz) and jump to 'greater' label
    jg greater
    
    ; default return value is 0
    xor eax, eax
    ret

greater:
    ; if we are here, it means that a > 8 so return 1
    mov eax, 1
    ret