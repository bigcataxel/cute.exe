section .data
    msg db 'Connected', 0xA

section .text
    global _start
_start:
    ; Ãcriture du message dans le descripteur 1 (stdout)
    mov rax, 1              ; numÃ©ro de la syscall write
    mov rdi, 1              
    mov rsi, msg            
    mov rdx, 9               
    syscall                  

    ; Terminaison du programme
    mov eax, 60            ; numÃ©ro de la syscall exit
    xor edi, edi           ; code d'erreur = 0
    syscall