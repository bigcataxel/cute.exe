section .data
    msg db 'Connected', 0
    len equ $ - msg

section .text
    global _start

_start:
    ; write(1, msg, len)
    mov rax, 1          ; syscall number (sys_write)
    mov rdi, 1          ; file descriptor 1 is stdout
    mov rsi, msg        ; string to print
    mov rdx, len        ; length of the string
    syscall             ; make the syscall

    ; exit(0)
    mov rax, 60         ; syscall number (sys_exit)
    xor rdi, rdi        ; exit code 0
    syscall             ; make the syscall