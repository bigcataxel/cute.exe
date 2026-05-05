section .data
    filename db '/etc/issue', 0
    buffer   times 128 db 0

section .text
    global _start
_start:
    ; open('/etc/issue')
    mov rax, 2         ; syscall number for 'open'
    mov rdi, filename   ; file name
    xor rsi, rsi        ; flags (O_RDONLY)
    xor rdx, rdx
    syscall

    ; read(file descriptor, buffer, size)
    mov r8, rax         ; save the file descriptor
    mov rax, 0          ; syscall number for 'read'
    mov rdi, r8         ; file descriptor
    mov rsi, buffer     ; buffer to store data
    mov rdx, 128        ; size of buffer
    syscall

    ; write(stdout, buffer, size)
    mov rax, 1          ; syscall number for 'write'
    xor rdi, rdi        ; file descriptor (stdout)
    inc edi
    mov rsi, buffer     ; buffer to print
    mov rdx, rax        ; size of buffer
    syscall

    ; exit(0)
    mov eax, 60         ; syscall number for 'exit'
    xor edi, edi        ; exit code (0)
    syscall