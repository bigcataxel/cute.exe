section .text
    global _start
_start:
    ; Load the number to be multiplied into register eax
    mov eax, 0x10        ; Assuming the value is 0x10 (change this as per y[1D[K
your requirement)
    
    ; Multiply eax by 8
    imul eax, eax, 8      ; Result will be in eax

    ; Exit the program
    mov eax, 60           ; syscall number for exit is 60
    xor edi, edi          ; Exit code 0
    syscall                ; Make the system call