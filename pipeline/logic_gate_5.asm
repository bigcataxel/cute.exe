section .text
global _start

_start:
    ; load 'a' into register eax
    mov eax, 5      ; replace this with actual value or instruction to get [K
it
    
    cmp eax, 5       ; compare the value in eax with 5
    jle less_than_or_equal   ; jump if less than or equal (jump over return[6D[K
return 1)

greater:
    mov eax, 0      ; move 0 into eax to return 0 for 'a > 5' case
    ret             ; return from function

less_than_or_equal:
    inc eax         ; increment eax by one (to make it 1)
    ret             ; return from function