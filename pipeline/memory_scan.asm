section .text
global _start

_start:
    ; Initialize the counter to 0
    mov eax, 0

scan_loop:
    ; Check if we've reached the end of our buffer
    cmp eax, [count]
    jge end_scan

    ; Multiply the current index by 2 and store it in temp
    mov ecx, 2
    mul ecx
    mov [temp], eax

    ; Increment the counter
    inc eax

    ; Jump back to the start of our loop
    jmp scan_loop

end_scan:
    ; Exit the program
    mov eax, 60
    xor edi, edi
    syscall