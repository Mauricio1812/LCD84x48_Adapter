# python3 filter_main.py
import cv2 as cv
import numpy as np
import ctypes
import filters_py as fpy

if __name__ == '__main__':
    
    lib = ctypes.CDLL('./filters_c.so')
    lib.Int_thresh_c.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), np.ctypeslib.ndpointer(dtype=np.ubyte)]
    lib.mono_img_asm.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), ctypes.c_double, ctypes.c_double, ctypes.c_double]
    lib.mono_array_asm.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), np.ctypeslib.ndpointer(dtype=np.ubyte)]

    img = cv.imread('Photos/MarioBros.png')
    img = cv.resize(img,(84,48), interpolation=cv.INTER_CUBIC)

    #SOBEL FILTER
    img_sobel = fpy.grayscale(img)
    Sobel_arr = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_mono = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1 volteada 
    img_sobel, Sobel_arr = fpy.Sobel_py(img_sobel,Sobel_mono,Sobel_arr)

    fpy.exportar_arr(Sobel_arr, "Arrays/Sobel_py.txt")

    #GLOBAL INTENSITY THRESHOLD FILTER
    img_ithresh = fpy.grayscale(img)
    Ithresh_arr = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_mono = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1 volteada 
    img_ithresh, Ithresh_arr = fpy.Int_thresh_py(img_ithresh,Ithresh_mono,Ithresh_arr)

    fpy.exportar_arr(Ithresh_arr, "Arrays/ITresh_py.txt")

    cv.imwrite('Results/Grayscale.png',img_ithresh)
    cv.imwrite('Results/Sobel.png',img_sobel)

    #GLOBAL INTENSITY THRESHOLD C
    imgC1 = cv.resize(img,(84,48), interpolation=cv.INTER_CUBIC)
    Ithresh_arrC1 = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_monoC1 = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1 volteada     
    lib.Int_thresh_c(imgC1, Ithresh_monoC1,Ithresh_arrC1)
    cv.imwrite('Results/GrayscaleC.png',Ithresh_monoC1)
    fpy.exportar_arr(Ithresh_arrC1, "Arrays/ITresh_C.txt")
    

    #GLOBAL INTENSITY THRESHOLD ASM
    imgASM = cv.resize(img,(84,48), interpolation=cv.INTER_CUBIC)
    Ithresh_arrASM = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_monoASM = np.zeros((48, 84),dtype='uint8') #Imagen en forma 0 y 1 volteada     
    lib.mono_img_asm(imgASM, Ithresh_monoASM, 0.0722, 0.7152, 0.2126)
    lib.mono_array_asm(Ithresh_monoASM,Ithresh_arrASM)

    cv.imwrite('Results/GrayscaleASM.png',Ithresh_monoASM) 
    # Para ver la imgn en blanco y negro cambiar  mono_img_asm:
    #   -En white_pixel -> mov r8, 255
    #   -En black_pixel -> mov r8,0
    fpy.exportar_arr(Ithresh_arrASM, "Arrays/ITresh_ASM.txt")


    #bash exec.sh
