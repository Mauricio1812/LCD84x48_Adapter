# python3 filter_main.py
import cv2 as cv
import numpy as np
import ctypes
import filters_py as fpy

if __name__ == '__main__':
    
    lib = ctypes.CDLL('./filters_c.so')
    lib.Sobel_c.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), \
                            np.ctypeslib.ndpointer(dtype=np.ubyte), np.ctypeslib.ndpointer(dtype=float)]

    img = cv.imread('Photos/MarioBros.png')

    #Sobel C
    img_sobel_c = cv.resize(img,(84,48), interpolation=cv.INTER_CUBIC)
    Sobel_arrC = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_monoC = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1     
    sobel_filtered_imageC = np.zeros((48, 84),dtype='float64')  
    lib.Sobel_c(img_sobel_c, Sobel_monoC,Sobel_arrC,sobel_filtered_imageC)
    cv.imwrite('Results/Sobel_c.png',Sobel_monoC)
    fpy.exportar_arr(Sobel_arrC, "Arrays/Sobel_c.txt")

    #SOBEL FILTER
    img = cv.resize(img,(84,48), interpolation=cv.INTER_CUBIC)
    img_sobel = fpy.grayscale(img)
    Sobel_arr = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_mono = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1  
    sobel_filtered_image = np.zeros((48, 84),dtype='f') 
    img_sobel, Sobel_arr = fpy.Sobel_py(img_sobel,Sobel_mono,Sobel_arr,sobel_filtered_image)
    fpy.exportar_arr(Sobel_arr, "Arrays/Sobel_py.txt")
    cv.imwrite('Results/Sobel_py.png',img_sobel)    
