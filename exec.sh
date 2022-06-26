nasm -f elf64 mono_img_asm.asm -o mono_img_asm.o 
nasm -f elf64 sobel_asm.asm -o sobel_asm.o 
nasm -f elf64 mono_array_asm.asm -o mono_array_asm.o 
gcc -c -fpic filters_c.c -o filters_c.o
gcc -shared filters_c.o mono_img_asm.o mono_array_asm.o sobel_asm.o  -o filters_c.so
python3 filters_main.py

