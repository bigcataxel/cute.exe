section .text
    global _start
_start:
    ; Load the number to be multiplied into register eax
    mov eax, 0xA          ; The hexadecimal value of 10 is 0xA
    
    ; Multiply eax by 10
    imul eax, eax, 10      ; This instruction performs the multiplication a[1D[K
and stores the result in eax
                            ; If you want to store it somewhere else, use m[1D[K
mov instead of imul

    ; Exit the program
    mov eax, 60             ; The system call number for exit is 60 on x86_[4D[K
x86_64 Linux systems
    xor edi, edi            ; Exit code 0
    syscall                 ; Make the system call