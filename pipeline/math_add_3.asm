section     .text
global      _start

_start:
    ; load the value to be added into register eax
    mov         eax, 3       ; eax = 3
    add         eax, [rel a] ; eax = eax + 3 (value of 'a')
    
    ; exit program
    mov         edi, eax     ; store the result in edi for syscall exit
    mov         eax, 60      ; syscall number for exit is 60
    syscall                ; make the system call

section     .data
a dd          5               ; define a as 5 (you can change this value)