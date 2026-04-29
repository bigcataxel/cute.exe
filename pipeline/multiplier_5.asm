section .text
    global _start
_start:
    ; Load the number to be multiplied into register eax
    mov eax, 0x1F4            ; The hexadecimal representation of 5 is 0x1F[4D[K
0x1F4.
    
    ; Multiply eax by 5 (since we already have the value in eax)
    imul eax, eax              ; This will store the result back into eax

    ; Exit the program
    mov eax, 0x3c             ; Syscall number for exit is 0x3c
    xor edi, edi               ; Exit code 0
    syscall