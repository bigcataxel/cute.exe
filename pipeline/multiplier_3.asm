section .text
    global _start
_start:
    ; Load the number to be multiplied into register eax
    mov eax, 0x1F        ; Replace with your desired value
    
    ; Multiply eax by 3
    imul eax, eax, 3      ; Multiplies EAX by 3

    ; Exit the program
    mov eax, 60           ; System call number for exit is 60
    xor edi, edi          ; Exit code 0
    syscall                ; Make the system call