section .text
    global _start
_start:
    ; load immediate value 7 into eax register
    mov eax, 7
    
    ; compare a with 7
    cmp dword [rsp], eax
    
    ; if a > 7 then set eax to 1 else set eax to 0
    jg greater_than_seven
    xor eax, eax
    ret
greater_than_seven:
    mov eax, 1
    ret