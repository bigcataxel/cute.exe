section .text
    global _start
_start:
    ; Load the number to be multiplied into register eax
    mov eax, 0x1F   ; Assuming the value is 31 in decimal (for example)
    
    ; Multiply by 2 using left shift operation
    shl eax, 1      ; Shift left by 1 bit
    
    ; Exit the program
    mov eax, 0x3c   ; Syscall number for exit is 60 in decimal
    xor edi, edi    ; Exit code 0
    syscall          ; Make the system call