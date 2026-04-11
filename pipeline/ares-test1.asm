section     .data
msg         db      'Connected',0 ; null terminated string
len         equ     $ - msg        ; length of the string

section     .text
global      _start
_start:
    ; write(1, msg, len)
    mov       rax, 1                  ; syscall number (sys_write)
    mov       rdi, 1                  ; file descriptor 1 is stdout
    mov       rsi, msg                ; string to print
    mov       rdx, len                ; length of the string
    syscall                            ; invoke sys_write()
    
    ; exit(0)
    mov       rax, 60                 ; syscall number (sys_exit)
    xor       rdi, rdi                ; exit code is 0
    syscall                            ; invoke sys_exit()