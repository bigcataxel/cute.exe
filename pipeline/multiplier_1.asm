section .text
    global _start
_start:
    ; Load the value of 'x' into register eax
    mov eax, [rel x]
    
    ; Multiply eax by 1 and store the result back in eax
    imul eax, eax, 1

    ; Exit the program
    mov eax, 60
    xor edi, edi
    syscall

section .data
x dd 42 ; Replace with your desired value for 'x'