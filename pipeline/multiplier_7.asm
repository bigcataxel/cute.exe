section .text
    global _start
_start:
    ; load the number to be multiplied into register eax
    mov eax, 0x1F     ; replace this with the actual value you want to mult[4D[K
multiply (in hexadecimal)

    ; multiply eax by 7
    imul eax, eax, 0x7  

    ; exit the program gracefully
    mov eax, 60
    xor edi, edi
    syscall