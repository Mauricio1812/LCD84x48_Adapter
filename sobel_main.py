# python3 sobel_main.py
# bash sobel.sh
import cv2 as cv
import numpy as np
import ctypes
import filters_py as fpy

if __name__ == '__main__':
    
    lib = ctypes.CDLL('./filters_c.so')
    lib.Sobel_c.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), 
                            np.ctypeslib.ndpointer(dtype=np.ubyte), np.ctypeslib.ndpointer(dtype=float)]
    lib.sobel_asm.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), 
                            np.ctypeslib.ndpointer(dtype=np.ubyte), np.ctypeslib.ndpointer(dtype=float), ctypes.c_double, ctypes.c_double, ctypes.c_double]
    lib.mono_array_asm.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), np.ctypeslib.ndpointer(dtype=np.ubyte)]

    img = cv.imread('Photos/MarioBros.png') 

    #Sobel ASM
    img_sobel_asm = cv.resize(img,(84,48), interpolation=cv.INTER_CUBIC)
    Sobel_arrASM = np.zeros((505),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_monoASM = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1   
    sobel_filtered_imageASM = np.zeros((48, 84),dtype='float64')  
    lib.sobel_asm(img_sobel_asm, Sobel_monoASM,Sobel_arrASM,sobel_filtered_imageASM, 0.0722, 0.7152, 0.2126)
    lib.mono_array_asm(Sobel_monoASM,Sobel_arrASM)
    cv.imwrite('Results/Sobel_ASM.png',Sobel_monoASM)

    Sobel_arrASM=np.delete(Sobel_arrASM, 504, 0)
    fpy.exportar_arr(Sobel_arrASM, "Arrays/Sobel_ASM.txt")

    #Resizing
    img = cv.resize(img,(84,48), interpolation=cv.INTER_CUBIC)

    #Sobel C
    Sobel_arrC = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_monoC = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1   
    sobel_filtered_imageC = np.zeros((48, 84),dtype='float64')  
    lib.Sobel_c(img, Sobel_monoC,Sobel_arrC,sobel_filtered_imageC)
    cv.imwrite('Results/Sobel_c.png',Sobel_monoC)
    fpy.exportar_arr(Sobel_arrC, "Arrays/Sobel_c.txt")

    #SOBEL FILTER
    img_sobel = fpy.grayscale(img)
    Sobel_arr = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_mono = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1 
    sobel_filtered_image = np.zeros((48, 84),dtype='f') 
    img_sobel, Sobel_arr = fpy.Sobel_py(img_sobel,Sobel_mono,Sobel_arr,sobel_filtered_image)
    cv.imwrite('Results/Sobel_py.png',img_sobel)    
    fpy.exportar_arr(Sobel_arr, "Arrays/Sobel_py.txt")


