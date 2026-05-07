section .text
    global _start

_start:
    ; load a into eax register
    mov eax, 15   ; assuming a = 15 here. Replace with the actual value or [K
register you want to use
    
    cmp eax, 10
    jg greaterThan
    jmp end

greaterThan:
    ; return 1 if a > 10
    mov eax, 1
    jmp end

end:
    ; exit the program
    mov eax, 60   ; syscall number for sys_exit
    xor edi, edi  ; exit code 0
    syscall