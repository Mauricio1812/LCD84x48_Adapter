;mono_array_asm(unsigned char *img_mono, unsigned char *mono_array);

global mono_array_asm 
    section .text 

mono_array_asm:
;rdi <- *img_mono 
;rsi <- *mono_array

    mov r10,0  
    mov r11, 0  
    mov r8, 0
    mov r9, 0
    mov r13, 0
    mov r14, 0
    mov r15, 0

    mov r15, rdi ;img[0][0]
for_alto48:
    mov r11, 0

    mov r14, rdi ;copy latest img[i][0]
for_ancho84:
    mov r8, 0

    ;Binary to Decimal - 8bits vertically
    mov r13b, byte [rdi]
    mov r9, r13
    add r8, r9  ;0

    add rdi, 84
    mov r13b, byte [rdi]
    mov r9, r13
    shl r9, 1
    add r8, r9   ;1

    add rdi, 84
    mov r13b, byte [rdi]
    mov r9, r13
    shl r9, 2
    add r8, r9   ;2

    add rdi, 84
    mov r13b, byte [rdi]
    mov r9, r13
    shl r9, 3
    add r8, r9   ;3

    add rdi, 84
    mov r13b, byte [rdi]
    mov r9, r13
    shl r9, 4
    add r8, r9   ;4

    add rdi, 84
    mov r13b, byte [rdi]
    mov r9, r13
    shl r9, 5
    add r8, r9   ;5

    add rdi, 84
    mov r13b, byte [rdi]
    mov r9, r13
    shl r9, 6
    add r8, r9   ;6

    add rdi, 84
    mov r13b, byte [rdi]
    mov r9, r13
    shl r9, 7
    add r8, r9   ;7

    mov [rsi], r8

cont_ancho84:
    inc rsi ;Byte_index++
    inc r14
    mov rdi, r14 ;img[i][j=j+1]

    inc r11
    cmp r11, 84
    jl for_ancho84

cont_alto48:
    add r15, 672 ;84*8
    mov rdi, r15 ;img[j+8][0]  
    
    add r10, 8
    cmp r10, 48
    jl for_alto48

done:
    ret
