section .text
    global _start
_start:
    ; load the value to be added into register eax
    mov eax, 10   ; for example, we're adding 1 to 10
    
    ; add 1 to eax
    inc eax       

    ; exit the program
    mov eax, 60
    xor edi, edi
    syscall