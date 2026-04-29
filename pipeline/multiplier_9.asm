section .text
    global _start
_start:
    ; load the number to be multiplied into register eax
    mov eax, 0x13      ; assuming 0x13 is the value of x in hexadecimal
    
    ; multiply eax by 9 (which is 0x9 in hex)
    imul eax, eax, 0x9  

    ; exit the program
    mov eax, 60         ; syscall number for sys_exit
    xor edi, edi        ; exit code 0
    syscall