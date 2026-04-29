section .data
    msg db "Connected", 0xA
    len equ $ - msg

section .text
    global _start

_start:
    ; write syscall
    mov eax, 1          ; syscall number (sys_write)
    mov edi, 1           ; file descriptor (stdout)
    mov rsi, msg         ; message to print
    mov edx, len        ; message length
    syscall              ; make the system call

    ; exit syscall
    mov eax, 60          ; syscall number (sys_exit)
    xor edi, edi         ; exit code is 0
    syscall              ; make the system call