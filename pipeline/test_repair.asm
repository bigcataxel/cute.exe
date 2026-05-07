section .data
    msg db 'Hello',10 ; "Hello" + newline character
    len equ $-msg       ; length of the string
    
section .text
    global _start
_start:
    mov eax,4            ; syscall number (sys_write)
    mov ebx,1            ; file descriptor 1 is stdout
    mov ecx,msg          ; address of string to output
    mov edx,len          ; length of the string
    int 0x80             ; call kernel
    
    mov eax,1            ; syscall number (sys_exit)
    xor ebx,ebx          ; exit code is 0
    int 0x80             ; call kernel
