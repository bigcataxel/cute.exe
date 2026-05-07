section .text
    global _start

_start:
    ; Load the value to be checked into register eax
    mov eax, 1337  
    
    ; Compare the value in eax with the constant 1337
    cmp eax, 0x539
    
    ; If they are equal (i.e., the code is 1337), set ZF to 1 and jump to '[1D[K
'equal' block
    je equal
    
    ; If not equal, return 0
    mov eax, 0
    jmp exit

equal:
    ; If they are equal (i.e., the code is 1337), return 1
    mov eax, 1

exit:
    ; Exit program
    mov eax, 60  
    xor edi, edi
    syscall