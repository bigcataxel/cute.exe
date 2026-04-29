section .text
    global _start
_start:
    ; Initialisation des registres pour mmap()
    xor rax, rax        ; RAX = 0 (syscall number for mmap)
    xor rdi, rdi        ; RDI = NULL (addr)
    mov rsi, [rel size] ; RSI = taille du cache Ã  protÃ©ger
    mov rdx, 0x7         ; RDX = 0x7 (prot=PROT_READ|PROT_WRITE)
    mov r10, 0x22        ; R10 = 0x22 (flags=MAP_PRIVATE|MAP_ANONYMOUS)
    xor r8, r8          ; R8 = -1 (fd = -1 => fd auto-detect)
    inc r8              ; R8 = 0 (fd = -1 + 1 => 0)
    xor r9, r9          ; R9 = 0 (offset)
    
    ; Appel systÃ¨me mmap()
    syscall 

    ; RAX contient le pointeur vers la zone mÃ©moire protÃ©gÃ©e par le cache.
    ; On l'enregistre dans .data pour pouvoir y accÃ©der plus tard.
    
section .data
    size dq 0x1000       ; Taille du cache Ã  initialiser (exemple : 4Ko)