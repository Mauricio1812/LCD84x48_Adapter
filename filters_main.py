# python3 filters_main.py
# bash exec.sh
import cv2 as cv
import numpy as np
import ctypes
import filters_py as fpy

if __name__ == '__main__':

#---------------------------------------------------------------------------------------------------#      
#-----------------------------------------CTYPES FUNCTIONS------------------------------------------#      
#---------------------------------------------------------------------------------------------------#    
    
    lib = ctypes.CDLL('./filters_c.so')
    lib.Sobel_c.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), 
                            np.ctypeslib.ndpointer(dtype=np.ubyte), np.ctypeslib.ndpointer(dtype=float)]
    lib.Int_thresh_c.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2),  
                                np.ctypeslib.ndpointer(dtype=np.ubyte)]
    lib.mono_img_asm.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), 
                                ctypes.c_double, ctypes.c_double, ctypes.c_double]
    lib.sobel_asm.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=3), np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), 
                            np.ctypeslib.ndpointer(dtype=np.ubyte), np.ctypeslib.ndpointer(dtype=float), ctypes.c_double, ctypes.c_double, ctypes.c_double]
    lib.mono_array_asm.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte, ndim=2), np.ctypeslib.ndpointer(dtype=np.ubyte)]

    #Reading and resizing selected image
    img_read = cv.imread('Photos/MarioBros.png') 
    img = fpy.resizing_interpolacion_bilineal(img_read, 48, 84)

#---------------------------------------------------------------------------------------------------#      
#------------------------------------------VARIABLES------------------------------------------------#      
#---------------------------------------------------------------------------------------------------#    

    #VARIABLES: SOBEL
    #ASM
    Sobel_arrASM = np.zeros((505),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_monoASM = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1   
    sobel_filtered_imageASM = np.zeros((48, 84),dtype='float64')  
    #C
    Sobel_arrC = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_monoC = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1   
    sobel_filtered_imageC = np.zeros((48, 84),dtype='float64')  
    #Python
    Sobel_arrPy = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Sobel_monoPy = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1 
    sobel_filtered_imagePy = np.zeros((48, 84),dtype='f') 

    #VARIABLES: INTENSITY THRESHOLD 
    #ASM
    Ithresh_arrASM = np.zeros((505),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_monoASM = np.zeros((48, 84),dtype='uint8') #Imagen en forma 0 y 1
    #C
    Ithresh_arrC = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_monoC = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1  
    #Py
    Ithresh_arrPy = np.zeros((504),dtype='uint8')   #Imagen en arreglo hexadecimal
    Ithresh_monoPy = np.ones((48, 84),dtype='uint8') #Imagen en forma 0 y 1  

#---------------------------------------------------------------------------------------------------#    
#--------------------------------------SOBEL FILTER-------------------------------------------------#        
#---------------------------------------------------------------------------------------------------#        

    #Sobel ASM
    lib.sobel_asm(img, Sobel_monoASM,Sobel_arrASM,sobel_filtered_imageASM, 0.0722, 0.7152, 0.2126)
    lib.mono_array_asm(Sobel_monoASM,Sobel_arrASM)
    cv.imwrite('Results/Sobel_ASM.png',Sobel_monoASM)
    Sobel_arrASM=np.delete(Sobel_arrASM, 504, 0)
    fpy.exportar_arr(Sobel_arrASM, "Arrays/Sobel_ASM.txt")
    # Para ver la imgn en blanco y negro cambiar  mono_img_asm:
    #   -En white_pixel -> mov r8, 255
    #   -En black_pixel -> mov r8,0

    #Sobel C
    lib.Sobel_c(img, Sobel_monoC,Sobel_arrC,sobel_filtered_imageC)
    cv.imwrite('Results/Sobel_c.png',Sobel_monoC)
    fpy.exportar_arr(Sobel_arrC, "Arrays/Sobel_c.txt")

    #Sobel Python
    img_sobelPy = fpy.grayscale(img)
    img_sobelPy, Sobel_arr = fpy.Sobel_py(img_sobelPy,Sobel_monoPy,Sobel_arrPy,sobel_filtered_imagePy)
    cv.imwrite('Results/Sobela_py.png',img_sobelPy)    
    fpy.exportar_arr(Sobel_arr, "Arrays/Sobel_py.txt")

#---------------------------------------------------------------------------------------------------#      
#--------------------------------INTENSITY THRESHOLD------------------------------------------------#      
#---------------------------------------------------------------------------------------------------#      

    #GLOBAL INTENSITY THRESHOLD ASM  
    lib.mono_img_asm(img, Ithresh_monoASM, 0.0722, 0.7152, 0.2126)
    lib.mono_array_asm(Ithresh_monoASM,Ithresh_arrASM)
    cv.imwrite('Results/Intensity_ASM.png',Ithresh_monoASM) 
    Ithresh_arrASM=np.delete(Ithresh_arrASM, 503, 0)
    fpy.exportar_arr(Ithresh_arrASM, "Arrays/Intensity_ASM.txt")
    # Para ver la imgn en blanco y negro cambiar  mono_img_asm:
    #   -En white_pixel -> mov r8, 255
    #   -En black_pixel -> mov r8,0

    #GLOBAL INTENSITY THRESHOLD C   
    lib.Int_thresh_c(img, Ithresh_monoC,Ithresh_arrC)
    cv.imwrite('Results/Intensity_C.png',Ithresh_monoC)
    fpy.exportar_arr(Ithresh_arrC, "Arrays/Intensity_C.txt")  

    #GLOBAL INTENSITY THRESHOLD FILTER
    img_ithreshPy = fpy.grayscale(img)
    img_ithreshPy, Ithresh_arrPy = fpy.Int_thresh_py(img_ithreshPy,Ithresh_monoPy,Ithresh_arrPy)
    fpy.exportar_arr(Ithresh_arrPy, "Arrays/Intensity_py.txt")
    cv.imwrite('Results/Intensity_py.png',img_ithreshPy)
