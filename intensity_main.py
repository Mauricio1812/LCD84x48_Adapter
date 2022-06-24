# python3 intensity_main.py
import cv2 as cv
import numpy as np
import ctypes
import filters_py as fpy

if __name__ == '__main__':
    
    lib = ctypes.CDLL('./filters_c.so')
    lib.Int_thresh_c.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2),  
                                np.ctypeslib.ndpointer(dtype=np.ubyte)]
    lib.mono_img_asm.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), 
                                ctypes.c_double, ctypes.c_double, ctypes.c_double]
    lib.mono_array_asm.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), np.ctypeslib.ndpointer(dtype=np.ubyte)]

    img = cv.imread('Photos/MarioBros.png')

    #GLOBAL INTENSITY THRESHOLD ASM
    imgASM = cv.resize(img,(84,48), interpolation=cv.INTER_CUBIC)
    Ithresh_arrASM = np.zeros((505),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_monoASM = np.zeros((48, 84),dtype='uint8') #Imagen en forma 0 y 1      
    lib.mono_img_asm(imgASM, Ithresh_monoASM, 0.0722, 0.7152, 0.2126)
    lib.mono_array_asm(Ithresh_monoASM,Ithresh_arrASM)
    cv.imwrite('Results/Intensity_ASM.png',Ithresh_monoASM) 
    # Para ver la imgn en blanco y negro cambiar  mono_img_asm:
    #   -En white_pixel -> mov r8, 255
    #   -En black_pixel -> mov r8,0

    Ithresh_arrASM=np.delete(Ithresh_arrASM, 504, 0)
    fpy.exportar_arr(Ithresh_arrASM, "Arrays/Intensity_ASM.txt")

    #Resizing
    img = cv.resize(img,(84,48), interpolation=cv.INTER_CUBIC)

    #GLOBAL INTENSITY THRESHOLD C
    Ithresh_arrC1 = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_monoC1 = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1      
    lib.Int_thresh_c(img, Ithresh_monoC1,Ithresh_arrC1)
    cv.imwrite('Results/Intensity_C.png',Ithresh_monoC1)
    fpy.exportar_arr(Ithresh_arrC1, "Arrays/Intensity_C.txt")  

    #GLOBAL INTENSITY THRESHOLD FILTER PYTHON
    img_ithresh = fpy.grayscale(img)
    Ithresh_arr = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_mono = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1  
    img_ithresh, Ithresh_arr = fpy.Int_thresh_py(img_ithresh,Ithresh_mono,Ithresh_arr)
    fpy.exportar_arr(Ithresh_arr, "Arrays/Intensity_py.txt")
    cv.imwrite('Results/Intensity_py.png',img_ithresh)

    #bash intensity.sh
