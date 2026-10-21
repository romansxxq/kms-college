
org 100h

start:
    ; Get original INT 9h vector
    mov ax, 3509h
    int 21h

    mov word ptr cs:[old_offset], bx
    mov word ptr cs:[old_segment], es

    ; Install our INT 9h handler
    push cs
    pop ds
    mov dx, offset new_int9
    mov ax, 2509h
    int 21h

    ; Display instructions
    mov dx, offset msg
    mov ah, 09h
    int 21h

wait_key:
    mov ah, 08h
    int 21h

    cmp al, 1Bh
    jne wait_key

    ; Restore original INT 9h vector
    push ds
    mov dx, word ptr cs:[old_offset]
    mov ax, word ptr cs:[old_segment]
    mov ds, ax
    mov ax, 2509h
    int 21h
    pop ds

    ; Display counter
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
    inc word ptr cs:[counter]
    pop ax

    jmp dword ptr cs:[old_offset]

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
counter dw 0

msg db 13, 10, 'Press keys. Press ESC to finish.', 13, 10, '$'
result db 13, 10, 'INT 9h counter (HEX): $'
