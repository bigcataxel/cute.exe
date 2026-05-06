section .text
global _start

; Point d'entrÃ©e du programme
_start:
    ; Charger les paramÃ¨tres dans des registres
    mov rdi, 0x12345678 ; Adresse de 'data' (ou autre chose)
    mov rsi, 0x8         ; Longueur de 'data'

    ; Appeler la fonction transform
    call transform

    ; Terminer le programme
    mov eax, 60
    xor edi, edi
    syscall

; Fonction transform
transform:
    push rbp        ; sauvegarder l'ancien base de pile
    mov rbp, rsp    ; nouvelle base de pile
    sub rsp, 0x10   ; allouer une zone sur la pile pour les variables local[5D[K
locales (ici rien)

    xor ecx, ecx    ; initialiser le compteur Ã  zÃ©ro
.loop:
    cmp ecx, esi    ; comparer le compteur avec 'len'
    jge .end        ; sortir si 'ecx >= len'
    
    mov al, [rdi+rcx]  ; charger le byte Ã  l'adresse (data + i) dans AL
    xor al, 0xFF       ; faire un XOR avec 0xFF
    mov [rdi+rcx], al  ; sauvegarder le rÃ©sultat de l'XOR Ã  l'adresse (data[5D[K
(data + i)
    
    inc ecx             ; incrÃ©menter le compteur
    jmp .loop           ; revenir au dÃ©but du boucle
.end:
    mov rsp, rbp  ; nettoyer la pile
    pop rbp        ; restaurer l'ancien base de pile
    ret            ; sortir de la fonction