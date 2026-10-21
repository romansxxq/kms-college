                                                                               
org 100h

start:
    push cs
    pop ds

    ; Save original INT 9h vector
    mov ax, 3509h
    int 21h
    mov word ptr cs:[old_offset], bx
    mov word ptr cs:[old_segment], es

    ; Install custom INT 9h handler
    push cs
    pop ds
    mov dx, offset new_int9
    mov ax, 2509h
    int 21h

    mov dx, offset msg
    mov ah, 09h
    int 21h

read_key:
    ; Wait for a key using BIOS
    mov ah, 00h
    int 16h

    ; ESC ends the program
    cmp al, 1Bh
    jne read_key

    ; Exclude ESC from the total
    dec word ptr cs:[counter]

    ; Restore original INT 9h vector
    push ds
    mov dx, word ptr cs:[old_offset]
    mov ax, word ptr cs:[old_segment]
    mov ds, ax
    mov ax, 2509h
    int 21h
    pop ds

    ; Display result
    mov dx, offset result
    mov ah, 09h
    int 21h

    mov bx, word ptr cs:[counter]

    mov dl, bh
    mov cl, 4
    shr dl, cl
    call print_hex

    mov dl, bh
    and dl, 0Fh
    call print_hex

    mov dl, bl
    mov cl, 4
    shr dl, cl
    call print_hex

    mov dl, bl
    and dl, 0Fh
    call print_hex

    mov ax, 4C00h
    int 21h

; Custom INT 9h handler
new_int9:
    push ax
    push bx
    push es

    ; Read BIOS keyboard buffer tail before chaining
    mov ax, 40h
    mov es, ax
    mov bx, es:[1Ch]
    mov word ptr cs:[tail_before], bx

    pop es
    pop bx
    pop ax

    ; Call original interrupt handler correctly
    pushf
    call dword ptr cs:[old_offset]

    ; Check whether BIOS buffer tail changed
    push ax
    push bx
    push es

    mov ax, 40h
    mov es, ax
    mov bx, es:[1Ch]

    cmp bx, word ptr cs:[tail_before]
    je no_increment

    inc word ptr cs:[counter]

no_increment:
    pop es
    pop bx
    pop ax

    ; Restore registers saved on entry
    ; The original handler returns here via IRET
    iret

; Print one hexadecimal digit
print_hex:
    and dl, 0Fh
    cmp dl, 9
    jbe digit
    add dl, 7

digit:
    add dl, '0'
    mov ah, 02h
    int 21h
    ret

old_offset dw 0
old_segment dw 0
tail_before dw 0
counter dw 0

msg db 13, 10, 'Press 5 keys, then ESC.', 13, 10, '$'
result db 13, 10, 'Total key presses: $'
