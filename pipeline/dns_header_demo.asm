
; DNS Query Header - Shellcode PIC (null-byte-free)
xor rax, rax
mov al, 0x0B
mov byte [rdi], al
mov al, 0xAA
mov byte [rdi+1], al
mov al, 0x01
mov byte [rdi+2], al
xor rax, rax
mov byte [rdi+3], al
mov al, 0x00
mov byte [rdi+4], al
mov al, 0x01
mov byte [rdi+5], al
mov al, 0x00
mov byte [rdi+6], al
mov byte [rdi+7], al
mov byte [rdi+8], al
mov byte [rdi+9], al
mov byte [rdi+10], al
mov byte [rdi+11], al
ret
