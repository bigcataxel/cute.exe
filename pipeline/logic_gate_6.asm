section .text
    global _start
_start:
    ; load immediate value 6 into register eax
    mov eax, 6
    
    ; compare a with 6
    cmp dword [rel a], eax
    
    ; if a > 6 then set EAX to 1 else set EAX to 0
    jg greater_than
    xor eax, eax
    ret
greater_than:
    mov eax, 1
    ret