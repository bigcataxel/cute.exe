section .text
    global _start
_start:
    ; load immediate value 3 into register eax
    mov eax, 3
    
    ; compare a with 3
    cmp dword [esp + 4], eax
    
    ; if a > 3 then set EAX to 1 else set EAX to 0
    jg greater_than
    xor eax, eax
    ret
greater_than:
    mov eax, 1
    ret