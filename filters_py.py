#python filters_py.py
import cv2 as cv
import numpy as np
import math

#CONVERSION A ARRAY DE PANTALLA NOKIA LCD
def NokiaLCD_array(img_mono, img_arr):
    Byte_index = 0
    for i in range(0, 48, 8): #Alto
        for j in range(0, 84): #Ancho
            #Transformando a bloques de 8bits - forma: valor*2^(n-1)
            for n in range(8):
                img_arr[Byte_index]=img_arr[Byte_index]+img_mono[i+n][j]*pow(2,n)
            #Cuando se cumple 8bits, se pasa al siguiente bloque
            Byte_index= Byte_index+1    
    return img_arr

#FILTRO SOBEL
def Sobel_py(img,img_mono,img_arr,sobel_filtered_image):
    sobelx = [1.0, 0.0, -1.0, 2.0, 0.0, -2.0, 1.0, 0.0, -1.0]
    sobely = [1.0, 2.0, 1.0, 0.0, 0.0, 0.0, -1.0, -2.0, -1.0]
    media = 0.0

    for i in range(1, 47): #Alto
        for j in range(1, 83): #Ancho
            #Calculate gx and gy using Sobel (horizontal and vertical gradients)
            index, gx, gy = 0, 0.0, 0.0
            for m in range(i-1, i+2):
                for n in range(j-1, j+2):
                    gx+=sobelx[index]*img[m][n]
                    gy+=sobely[index]*img[m][n]
                    index+=1

            g= math.sqrt(gx ** 2 + gy ** 2)
            sobel_filtered_image[i+1][j+1] = g
            media = media+g
    
    media = media/(82*46)

    #Thresholding de la imagen a blanco o negro
    for i in range(0, 48): #Alto
        for j in range(0, 84): #Ancho
            if sobel_filtered_image[i][j] < media:    #Si el pixel es menor al umbral, se guarda 0 en el arreglo dado que es de fondo (pixel no prendido en pantalla)
                img_mono[i][j]=0
                img[i][j]=255
            else:   
                img[i][j]=0
    
    #Array para NokiaLCD
    img_arr=NokiaLCD_array(img_mono, img_arr)

    return img, img_arr

#FILTRO UMBRAL INTENSIDAD GLOBAL
def Int_thresh_py(img,img_mono,img_arr):
    umbral=0.0
    cont=0
    for i in range(0, 48): #Alto
        for j in range(0, 84): #Ancho        
            if(img[i][j]!=255):
                umbral=umbral+img[i][j]
                cont=cont+1
    umbral=umbral/cont
    #print("Umbral: ", umbral, "Cont:", cont)

    #Thresholding de la imagen a blanco o negro
    for i in range(0, 48): #Alto
        for j in range(0, 84): #Ancho
            if img[i][j] > umbral: #Global Threshold
                img[i][j]=255
                img_mono[i][j]=0
            else:
                img[i][j]=0
    
    #Array para NokiaLCD
    img_arr=NokiaLCD_array(img_mono, img_arr)    
    
    return img, img_arr

#GRAYSCALE FILTER 
def grayscale(img):
    gray = np.zeros((48, 84),dtype='uint8')
    for i in range (len(img)):
        for j in range(len(img[0])):
            # Gray = 0.0722Blue + 0.7152Green + 0.2126Red
            gray[i][j]=int(0.0722*img[i][j][0]+0.7152*img[i][j][1]+0.2126*img[i][j][2])
    return gray

def exportar_arr(img_arr,file_name):
    #Escribiendo el arreglo en un archivo de texto
    file = open(file_name, "w+")
    file.write("char array_py[504] = {")
    for i in range(len(img_arr)-1):
        content = hex(img_arr[i])
        file.write(content)
        file.write(", ")
        if (i % 80)==0:
            file.write("\n")
    content = hex(img_arr[len(img_arr)-1])
    file.write(content)
    file.write("};")
    file.close()

if __name__ == '__main__':   
    img = cv.imread('Photos/MarioBros.png')
    img = cv.resize(img,(84,48), interpolation=cv.INTER_CUBIC)

    #SOBEL FILTER
    img_sobel = grayscale(img)
    Sobel_arr = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_mono = np.zeros((48, 84),dtype='uint8') #Imagen en forma 0 y 1 volteada 
    img_sobel, Sobel_arr = Sobel_py(img_sobel,Sobel_mono,Sobel_arr)

    #exportar_arr(Sobel_arr, "Sobel_prueba1_py.txt")

    #GLOBAL INTENSITY THRESHOLD FILTER
    img_ithresh = grayscale(img)
    Ithresh_arr = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_mono = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1 volteada 
    img_ithresh, Ithresh_arr = Int_thresh_py(img_ithresh,Ithresh_mono,Ithresh_arr)

    #exportar_arr(Ithresh_arr, "ITresh_prueba1.txt")

    #cv.imwrite('Results/Grayscale_py.png',img_ithresh)
    cv.imwrite('Results/Sobel_py.png',img_sobel)