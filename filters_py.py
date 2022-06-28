#python filters_py.py
import cv2 as cv
import numpy as np
import math

#CONVERSION A ARRAY DE PANTALLA NOKIA LCD
def NokiaLCD_array(img_mono, img_arr):
    Byte_index = 0
    for i in range(0, 48, 8): #Alto
        for j in range(0, 84): #Ancho
            #Transformando a bloques de 8bits - forma: valor*2^(n)
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
            sobel_filtered_image[i][j] = g
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
    file.write("char bitmapArray[504] = {")
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

#-----------------FUNCIÓN RESIZING DE LA IMAGEN MEDIANTE INTERPOLACIÓN BILINEAL---------------------
def resizing_interpolacion_bilineal(imagen_original, nuevo_altura, nuevo_ancho):
    #Dimensiones originales de la imagen
    altura_original = len(imagen_original)
    ancho_original = len(imagen_original[0])
    canales_imagen = 3 #RGB

    nueva_imagen = np.zeros((nuevo_altura, nuevo_ancho, canales_imagen))

    #Factores de escalamiento para la altura y el ancho
    if nuevo_ancho != 0:
        factor_escala_ancho = ancho_original/nuevo_ancho
    else:
        factor_escala_ancho = 0
    
    if nuevo_altura != 0:
        factor_escala_altura = altura_original/nuevo_altura
    else:
        factor_escala_altura = 0

    #Se recorren todos los pixeles de la nueva imagen mediante dos iterativas
    for i in range(nuevo_altura):
        for j in range(nuevo_ancho):
            #Coordenadas equivalentes de la img original
            x = factor_escala_altura*i
            y = factor_escala_ancho*j
            #Calculando los 4 píxeles de la imagen original más cercanos a x e y 
            x_inferior= int(x)
            if (altura_original-1) <= int(x+1):
                x_superior = altura_original-1
            else:
                x_superior = int(x+1)

            y_inferior = int(y)
            if (ancho_original-1) <= int(y+1):
                y_superior = ancho_original -1
            else:
                y_superior =  int(y+1)
            
            #Si los valores de x e y son valores enteros, no hay necesidad de interpolar, sino
            #asignar los valores de la imagen original a dichas coordenadas 
            if(x_superior == x_inferior) and (y_superior == y_inferior):
                valor_interpolado = imagen_original[int(x), int(y), :]
            #Si x es entero, se interpola la parte solo y
            elif(x_superior == x_inferior):
                valor_vecino1 = imagen_original[int(x), int(y_inferior), :]
                valor_vecino2 = imagen_original[int(x), int(y_superior), :]
                valor_interpolado = valor_vecino1*(y_superior-y)+valor_vecino2*(y-y_inferior)
            #Si y es entero, se interpola la parte solo x
            elif(y_superior == y_inferior):
                valor_vecino1 = imagen_original[int(x_inferior), int(y), :]
                valor_vecino2 = imagen_original[int(x_superior), int(y), :]
                valor_interpolado = (valor_vecino1)*(x_superior-x) + (valor_vecino2)*(x-x_inferior)
            #Si x e y no son enteros, se interpolan ambos valores
            else:
                #Calculo de los valores de los 4 vecinos que se encuentran cercanos a x e y
                valor_vecino1 = imagen_original[x_inferior, y_inferior, :]
                valor_vecino2 = imagen_original[x_superior, y_inferior, :]
                valor_vecino3 = imagen_original[x_inferior, y_superior, :]
                valor_vecino4 = imagen_original[x_superior, y_superior, :]
                #Cálculo de la contribución en un valor interpolado 1 y 2 de los vecinos 1 y 2, así como 3 y 4 respectivamente
                valor_interpolado1 = valor_vecino1*(x_superior-x)+valor_vecino2*(x-x_inferior)
                valor_interpolado2 = valor_vecino3*(x_superior-x)+valor_vecino4*(x-x_inferior)
                #Cálculo de la contribución de los valores interpolados 1 y 2 en un valor interpolado total que ocupara las coordenas i y j
                #de la nueva imagen
                valor_interpolado = (valor_interpolado1)*(y_superior-y)+(valor_interpolado2)*(y-y_inferior)

            nueva_imagen[i,j,:] = valor_interpolado
    return nueva_imagen.astype(np.uint8)

if __name__ == '__main__':   
    img = cv.imread('Photos/Bcat.jpg')
    img = resizing_interpolacion_bilineal(img, 48, 84)
    cv.imwrite('Results/TEST_resize.png',img)

    #SOBEL FILTER
    Sobel_arrPy = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_monoPy = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1 
    sobel_filtered_imagePy = np.zeros((48, 84),dtype='f') 
    img_sobelPy = grayscale(img)
    img_sobelPy, Sobel_arr = Sobel_py(img_sobelPy,Sobel_monoPy,Sobel_arrPy,sobel_filtered_imagePy)
    cv.imwrite('Results/TEST_Sobel_py.png',img_sobelPy)
    #exportar_arr(Sobel_arr, "TEST_Sobel_py.txt")

    #GLOBAL INTENSITY THRESHOLD FILTER
    img_ithresh = grayscale(img)
    Ithresh_arr = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_mono = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1 volteada 
    img_ithresh, Ithresh_arr = Int_thresh_py(img_ithresh,Ithresh_mono,Ithresh_arr)
    cv.imwrite('Results/TEST_Intensity_Py.png',img_ithresh)
    #exportar_arr(Ithresh_arr, "TEST_Intensity_Py.txt")