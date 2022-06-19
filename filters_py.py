#python3 filters_py.py
import cv2 as cv
import numpy as np
import ctypes

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
def Sobel_py(img,img_mono,img_arr):
    #Gradient-X
    grad_x = cv.Sobel(img, ddepth=cv.CV_16S, dx=1, dy=0, ksize=3, borderType=cv.BORDER_DEFAULT)
    # Gradient-Y
    grad_y = cv.Sobel(img, ddepth=cv.CV_16S, dx=0, dy=1, ksize=3, borderType=cv.BORDER_DEFAULT)
    #Converting to 8bits unsigned |ABS|
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    #Gxy=sqrt(Gx^2+Gy^2)
    img = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    #Umbral: probar con y sin umbral
    umbral=0.0
    for i in range(48):
        for j in range(84):
            umbral=umbral+img[i][j]
    umbral=umbral/(84*48)

    #Thresholding de la imagen a blanco o negro
    for i in range(0, 48): #Alto
        for j in range(0, 84): #Ancho
            if img[i][j] < umbral:    #Si el pixel es menor al umbral, se guarda 0 en el arreglo dado que es de fondo (pixel no prendido en pantalla)
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
            # https://www.kdnuggets.com/2019/12/convert-rgb-image-grayscale.html
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
    Sobel_mono = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1 volteada 
    img_sobel, Sobel_arr = Sobel_py(img_sobel,Sobel_mono,Sobel_arr)

    exportar_arr(Sobel_arr, "Sobel_prueba1.txt")

    #GLOBAL INTENSITY THRESHOLD FILTER
    img_ithresh = grayscale(img)
    Ithresh_arr = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_mono = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1 volteada 
    img_ithresh, Ithresh_arr = Int_thresh_py(img_ithresh,Ithresh_mono,Ithresh_arr)

    exportar_arr(Ithresh_arr, "ITresh_prueba1.txt")

    cv.imwrite('Results/Grayscale.png',img_ithresh)
    cv.imwrite('Results/Sobel.png',img_sobel)