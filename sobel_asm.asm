;sobel_asm(unsigned char *img, unsigned char *sobel_img, unsigned char *sobel_arr, double *sobel_filtered_image,weight_b,weight_g,weight_r)

global sobel_asm 
    section .text 

sobel_asm:
;rdi <- *img 
;rsi <- *sobel_img
;rdx <- *sobel_arr
;rcx <- *sobel_filtered_image 
;xmm0 <- weight_b
;xmm1 <- weight_g
;xmm2 <- weight_r

    xorpd xmm3,xmm3
    xorpd xmm4, xmm4
    xorpd xmm5,xmm5 
    xorpd xmm6,xmm6
    xorpd xmm7,xmm7
    mov r10, 0  
    mov r11, 0
    mov r13, 0

    mov r9, rdi ;salvando *img[0][0][0]
    mov r12, rsi ;salvando *sobel_img[0][0]

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
    inc r10
    cmp r10, 4032   ;84x48
    jl for_gray

sobel:
    xorpd xmm3,xmm3 ;gx
    xorpd xmm4, xmm4 ;gy
    xorpd xmm5, xmm5 ;g
    xorpd xmm6, xmm6 
    xorpd xmm7, xmm7 
    xorpd xmm8, xmm8 ;umbral
    mov r8, 0
    mov r9, 0
    ;r10 vale 4032 para este punto
    mov r11, 0 
    mov r12, rsi    ;*recuperando *sobel_img[0][0]
    mov r14, 0
    mov r15, rcx 

    add r15, 672  
    ;comienza en i=1 (4bytes -> 84x8)

for_i:
    mov r8, 0
    mov r11, r12 

for_j:
    add r15, 8
    ;comienza en j=1 (4bytes)

    xorpd xmm3, xmm3    ;gx=0
    xorpd xmm4, xmm4    ;gy=0
    xorpd xmm5, xmm5    ;g = 0

    ;Convolución:
    mov r14b, byte [r12]
    cvtsi2sd xmm3, r14
    cvtsi2sd xmm4, r14
    ;gx+=1*img[i][j]
    ;gy+=1*img[i][j]
    inc r12 

    mov r14b, byte [r12]
    cvtsi2sd xmm6, r14
    addsd xmm4, xmm6
    addsd xmm4, xmm6
    ;gx+=0*img[i][j+1]
    ;gy+=2*img[i][j+1]
    inc r12 

    mov r14b, byte [r12]
    cvtsi2sd xmm6, r14
    subsd xmm3,xmm6
    addsd xmm4, xmm6
    ;gx+=-1*img[i][j+2]
    ;gy+=1*img[i][j+2]
    add r12, 82

    mov r14b, byte [r12]
    cvtsi2sd xmm6, r14
    addsd xmm3,xmm6
    addsd xmm3,xmm6
    ;gx+=2*img[i+1][j]
    ;gy+=0*img[i+1][j]
    inc r12

    ;gx+=0*img[i+1][j+1]
    ;gy+=0*img[i+1][j+1]
    inc r12 

    mov r14b, byte [r12]
    cvtsi2sd xmm6, r14
    subsd xmm3,xmm6
    subsd xmm3,xmm6
    ;gx+=-2*img[i+1][j+2]
    ;gy+=0*img[i+1][j+2]
    add r12, 82

    mov r14b, byte [r12]
    cvtsi2sd xmm6, r14
    addsd xmm3,xmm6
    subsd xmm4, xmm6
    ;gx+=1*img[i+2][j]
    ;gy+=-1*img[i+2][j]
    inc r12 

    mov r14b, byte [r12]
    cvtsi2sd xmm6, r14
    subsd xmm4, xmm6
    subsd xmm4, xmm6
    ;gx+=0*img[i+2][j+1]
    ;gy+=-2*img[i+2][j+1]
    inc r12 

    mov r14b, byte [r12]
    cvtsi2sd xmm6, r14
    subsd xmm3,xmm6 
    subsd xmm4, xmm6
    ;gx+=-1*img[i+2][j+2]
    ;gy+=-1*img[i+2][j+2] 

    mulsd xmm3, xmm3    ;gx^2
    mulsd xmm4, xmm4    ;gy^2
    addsd xmm3, xmm4    ;gx^2+gy^2
    sqrtsd xmm5, xmm3 
    ;g=sqrt(gx^2+gy^2)

cont_j:
    addsd xmm8, xmm5    ;umbral+=g
    movsd [r15], xmm5  ;sobel_filtered_img[i][j]=g
    inc r11
    mov r12, r11
    inc r8
    cmp r8, 82 
    jl for_j

cont_i:
    inc r12 
    inc r12
    add r15, 8
    add r15, 8

    inc r9
    cmp r9, 46
    jl for_i

umbral:
    sub r10, 260 ;bits totales=82x46, no 84x48
    cvtsi2sd xmm9, r10 
    divsd xmm8, xmm9    ;umbral=umbral/4032.0
    xorpd xmm3, xmm3

    mov r12, rsi    ;*recuperando *output[0]
    mov r15, rcx
    mov r8, 0
    mov r9, 0

for_umbral:
    movsd xmm3, [r15]
    ucomisd  xmm3, xmm8    ;imgn[i][j]<umbral
    jb white_pixel

black_pixel:
    mov r8, 1   

continue_umbral:
    mov byte [r12], r8b ;img_mono[i][j]
    inc r12
    movsd [r15], xmm3
    add r15, 8
    inc r9
    cmp r9, 4032   ;84x48
    jl for_umbral

done:
    ret

white_pixel:
    mov r8, 0
    jmp continue_umbral