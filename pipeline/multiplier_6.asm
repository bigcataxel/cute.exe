section .text
    global _start
_start:
    ; Load the number to be multiplied into register eax
    mov eax, 0x1A   ; Assuming the value of x is 26 in hexadecimal (0x1a)
    
    ; Multiply eax by 6
    imul eax, eax, 6
    
    ; Exit the program
    mov eax, 0x3c   ; Syscall number for exit is 0x3c
    xor edi, edi    ; Return a value of 0 (success) in register edi
    syscall          ; Invoke the system call