section .text
global _start

_start:
    ; load 'a' into register eax
    mov eax, 10   ; replace this with actual value or instruction to get it[2D[K
it
    
    cmp eax, 9
    jg greaterThanNine
    jmp end

greaterThanNine:
    ; return 1 (true)
    mov eax, 1
    jmp end

end:
    ; exit the program
    mov eax, 60   ; syscall number for sys_exit
    xor edi, edi  ; exit code 0
    syscall