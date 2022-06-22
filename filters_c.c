// bash exec.sh

#include <math.h>
#include <stdlib.h>
#include <stdio.h>

extern void mono_img_asm(unsigned char *img, unsigned char *img_ithresh, double weight_b, double weight_g, double weight_r);
extern void mono_array_asm(unsigned char *img_mono, unsigned char *mono_array);

// Filtro a escala de grises
float grayscale(unsigned char *img,unsigned char *img_grayscale){
    int promedio;
    int index, i , j;
    float umbral =0;
    for(i=0;i<48;i++){ //Alto
        for(j=0;j<84;j++){ //Ancho
            index=i*84*3+j*3;
            //Valor promedio pesado
            promedio=0.0722* img[index]+ 0.7152* img[index+1] + 0.2126* img[index+2];           
            index=i*84+j;
            //Asignando valor a img grayscale
            img_grayscale[index]=promedio;
            //printf("%d ", img_ithresh[index]);
            umbral+=promedio; //Calculando umbral para thresholding
        }
    }

    return (umbral/4032);    
}

//Conversión a formato de pantalla LCD
void To_array(unsigned char *img_mono, unsigned char *img_arr){
    int Byte_index=0;
    for(int i=0;i<48;i=8+i){
        for(int j=0;j<84;j++){
            for(int n=0; n<8; n++){
                img_arr[Byte_index]+=(img_mono[(i+n)*84+j]*pow(2, n));
            }
            Byte_index++;
        }
    }
}

void Int_thresh_c(unsigned char *img, unsigned char *img_ithresh, unsigned char *img_arr)
{
    //Convertir a grayscale 
    float umbral;
    umbral = grayscale(img, img_ithresh);
    int index,i,j;

    //Transformando a monocromática: 
    //  Index>umbral -> Píxel blanco
    //  Index<umbral -> Píxel negro
    unsigned char img_mono[48][84];
    for(i=0;i<48;i++){
        for(j=0;j<84;j++){
            index=i*84+j;
            if(img_ithresh[index]>umbral){
                img_ithresh[index]=255;
                img_mono[i][j]=0;
            }else{
                img_ithresh[index]=0;
                img_mono[i][j]=1;
            }
        }
    }

    To_array(img_mono[0], img_arr);

    return;
}

void Sobel_c(unsigned char *img, unsigned char *sobel_img, unsigned char *sobel_arr, float *sobel_filtered_image)
{
    float umbral = grayscale(img,sobel_img);
    float sobelx[9] = {1.0, 0.0, -1.0, 2.0, 0.0, -2.0, 1.0, 0.0, -1.0};
    float sobely[9] = {1.0, 2.0, 1.0, 0.0, 0.0, 0.0, -1.0, -2.0, -1.0};
    float media = 0.0;
    int i,j,m,n,index;
    float gx,gy,g;
    for (i=1;i<47;i++){
        for (j=1;j<83;j++){
            index=0;
            gx=0.0;
            gy=0.0;
            for (m=i-1;m<i+2;m++){ //Convolución por el kernel
                for (n=j-1;n<j+2;n++){
                    gx+=sobelx[index]*sobel_img[m*84+n];
                    gy+=sobely[index]*sobel_img[m*84+n];
                    index++;
                }
            }
            g = sqrt(gx*gx+gy*gy);
            sobel_filtered_image[i*84+j+85]=g; //index-> [(i+1)*84+j+1]
            media+=g;
        }
    }
    media=media/(82*46);

    //Transformando a monocromática: 
    //  Index<umbral -> Píxel blanco
    //  Index>umbral -> Píxel negro
    unsigned char img_mono[48][84];
    for(i=0;i<48;i++){
        for(j=0;j<84;j++){
            if(sobel_filtered_image[i*84+j]<umbral){
                sobel_img[i*84+j]=255;
                img_mono[i][j]=0;
            }else{
                img_mono[i][j]=1;
                sobel_img[i*84+j]=0;
            }
        }
    }

    //Transformando a arreglo en bytes compatible con pantalla LCD
    To_array(img_mono[0],sobel_arr);

    return;
}
