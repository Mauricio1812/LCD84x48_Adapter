;void Mono_asm(char *img, char *bmp, double *threshold);
;extern void grayscale_asm(unsigned char *img, unsigned char *output, double g_red, double g_green, double g_blue);

global mono_img_asm 
    section .text 

mono_img_asm:
;rdi <- *img 
;rsi <- *output
;xmm0 <- g_red
;xmm1 <- g_green
;xmm2 <- g_blue

    xorpd xmm3,xmm3
    xorpd xmm4, xmm4
    xorpd xmm5,xmm5 
    xorpd xmm6,xmm6
    xorpd xmm7,xmm7

    mov r9, rdi ;salvando *img
    mov r12, rsi ;salvando *output

    mov r10,0  ;i=0 
    mov r11, 0
    mov r13, 0

for_gray:
   ;Salvando constantes
    movsd xmm3, xmm0
    movsd xmm4, xmm1
    movsd xmm5, xmm2

    ;0.0722* img[index]
    mov r11b, byte [r9]
    cvtsi2sd xmm7, r11
    mulsd xmm3, xmm7
    add r9, 1   

    ;0.7152* img[index+1]
    mov r11b, byte [r9]    
    cvtsi2sd xmm7, r11      
    mulsd xmm4, xmm7
    add r9, 1     

    ;0.2126* img[index+2]
    mov r11b, byte [r9]
    cvtsi2sd xmm7, r11         
    mulsd xmm5, xmm7
    add r9, 1   

    ;promedio=suma de lo anterior
    xorpd xmm6, xmm6
    addsd xmm6, xmm3
    addsd xmm6, xmm4
    addsd xmm6, xmm5
    cvtsd2si r8, xmm6

continue_gray:
    mov [r12], r8
    inc r12
    add r13, r8 ;suma de todas las intensidades
    inc r10
    cmp r10, 4032 ;84x48
    jl for_gray


umbral:
    xorpd xmm3,xmm3 ;umbral
    xorpd xmm4, xmm4 
    mov r12, rsi ;*recuperando *output[0]

    cvtsi2sd xmm3, r13
    cvtsi2sd xmm4, r10
    divsd xmm3, xmm4 ;umbral=suma de intensidades/cantidad de pixeles
    cvtsd2si r13, xmm3 ;r13=umbral

    mov r8, 0
    mov r10, 0
    mov r11, 0

for_umbral:
    mov r11b, byte [r12] 
    cmp r11, r13 ;imgn[i][j]>umbral
    jge white_pixel

black_pixel:
    mov r8, 1

continue_umbral:
    mov byte [r12], r8b
    inc r12
    inc r10
    cmp r10, 4032 ;84x48
    jl for_umbral

done:
    ret


white_pixel:
    mov r8, 0
    jmp continue_umbral


;nasm -f elf64 grayscale_asm.asm -o grayscale_asm.o 