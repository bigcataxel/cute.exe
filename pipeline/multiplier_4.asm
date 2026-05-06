section .text
    global _start
_start:
    ; Load the number to be multiplied into register eax
    mov eax, 0x10        ; Assuming the value is 0x10 (change this as per y[1D[K
your requirement)
    
    ; Multiply eax by 4
    imul eax, eax, 4      ; Result will be in eax

    ; Exit the program
    mov eax, 60           ; System call number for exit is 60 (syscall_grou[13D[K
(syscall_group 1)
    xor edi, edi          ; Exit code 0
    syscall                ; Make the system call