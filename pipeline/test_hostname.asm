
; File Read + Write to stdout - null-byte-free
; Reads /etc/hostname and writes to stdout

section .bss
    align 8
    file_buffer: resq 256

section .rodata
    filename: db "/etc/hostname", 0

section .text
global _start

_start:
    push rbp
    mov rbp, rsp
    
    ; ============ OPEN FILE ============
    lea rdi, [rel filename]
    xor rax, rax
    mov al, 2
    xor rsi, rsi
    xor rdx, rdx
    syscall
    
    cmp rax, 0
    jl .exit_fail
    
    mov r8, rax
    
    ; ============ READ FILE ============
    mov rdi, r8
    lea rsi, [rel file_buffer]
    mov rdx, 256
    xor rax, rax
    syscall
    
    mov r9, rax
    
    ; ============ WRITE TO STDOUT ============
    mov rdi, 1
    lea rsi, [rel file_buffer]
    mov rdx, r9
    xor rax, rax
    mov al, 1
    syscall
    
    ; ============ CLOSE FILE ============
    mov rdi, r8
    xor rax, rax
    mov al, 3
    syscall
    
    ; ============ EXIT ============
    xor rdi, rdi
    xor rax, rax
    mov al, 60
    syscall
    
.exit_fail:
    mov rdi, 1
    xor rax, rax
    mov al, 60
    syscall
