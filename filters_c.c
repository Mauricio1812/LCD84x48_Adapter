// bash exec.sh

#include <math.h>
#include <stdlib.h>
#include <stdio.h>

extern void mono_img_asm(unsigned char *img, unsigned char *img_ithresh, double g_red, double g_green, double g_blue);
extern void mono_array_asm(unsigned char *img_mono, unsigned char *mono_array);

void Int_thresh_c(unsigned char *img, unsigned char *img_ithresh, unsigned char *img_arr)
{
    //Convertir a grayscale 
    int promedio;
    int index, i , j;
    for(i=0;i<48;i++){ //Alto
        for(j=0;j<84;j++){ //Ancho
            index=i*84*3+j*3;
            //Valor promedio pesado
            promedio=0.0722* img[index]+ 0.7152* img[index+1] + 0.2126* img[index+2];           
            index=i*84+j;
            //Asignando valor a img grayscale
            img_ithresh[index]=promedio;
            //printf("%d ", img_ithresh[index]);
        }
    }

    float umbral=0;
    int cont=0;

    for(i=0;i<48;i++){
        for(j=0;j<84;j++){
            index=i*84+j;
            if(img_ithresh[index]!=255){
                umbral+=img_ithresh[index];
                cont++;
            }
        }
    }
    umbral=umbral/cont;


    unsigned char img_mono[48][84];

    for(i=0;i<48;i++){
        for(j=0;j<84;j++){
            index=i*84+j;
            if(img_ithresh[index]>umbral){
                img_ithresh[index]=255;
                img_mono[i][j]=0;
            }else{
                img_ithresh[index]=0;
                img_mono[i][j];
            }
        }
    }
    
    int Byte_index=0;
    for(i=0;i<48;i=8+i){
        for(j=0;j<84;j++){
            for(int n=0; n<8; n++){
                img_arr[Byte_index]+=(img_mono[i+n][j]*pow(2, n));
            }
            Byte_index++;
        }
    }

    return;
}
