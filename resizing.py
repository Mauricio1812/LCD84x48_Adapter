from types import new_class
import cv2
import numpy as np
import math

def bl_resize(original_img, new_h, new_w):
	old_h = len(img)
	old_w = len(img[0])
	c = len(img[0][0])

	#We will fill-in the values later.
	resized = np.zeros((new_h, new_w, c))
	#resized = [[[0 for i in range(c)]for j in range(new_w)]for k in range(new_h)]

	
	#Calculate horizontal and vertical  scaling factor
	w_scale_factor = (old_w ) / (new_w) if new_h != 0 else 0
	h_scale_factor = (old_h ) / (new_h) if new_w != 0 else 0
	for i in range(new_h):
		for j in range(new_w):
			#map the coordinates back to the original image
			x = i * h_scale_factor
			y = j * w_scale_factor
			#calculate the coordinate values for 4 surrounding pixels.
			x_floor = int(x)
			x_ceil = min( old_h - 1, int(x+1))
			y_floor = int(y)
			y_ceil = min(old_w - 1, int(y+1))

			if (x_ceil == x_floor) and (y_ceil == y_floor):
				q = original_img[int(x), int(y), :]
			elif (x_ceil == x_floor):
				q1 = original_img[int(x), int(y_floor), :]
				q2 = original_img[int(x), int(y_ceil), :]
				q = q1 * (y_ceil - y) + q2 * (y - y_floor)
			elif (y_ceil == y_floor):
				q1 = original_img[int(x_floor), int(y), :]
				q2 = original_img[int(x_ceil), int(y), :]
				q = (q1 * (x_ceil - x)) + (q2	 * (x - x_floor))
			else:
				v1 = original_img[x_floor, y_floor, :]
				v2 = original_img[x_ceil, y_floor, :]
				v3 = original_img[x_floor, y_ceil, :]
				v4 = original_img[x_ceil, y_ceil, :]

				q1 = v1 * (x_ceil - x) + v2 * (x - x_floor)
				q2 = v3 * (x_ceil - x) + v4 * (x - x_floor)
				q = q1 * (y_ceil - y) + q2 * (y - y_floor)
			#resized[i][j][:] = q
			resized[i, j, :] =	q
	return resized

if __name__ == "__main__":

    img =  cv2.imread('Photos/MarioBros.png')

    ancho = 84
    altura = 48

    dim = (ancho, altura)

    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
	#get dimensions of original image
    altura_original = img.shape[0]
    ancho_original = img.shape[1]
    c_original =  img.shape[2]


    img_bl = bl_resize(img, 48, 84)

    cv2.imshow('Resized_bl', img_bl)
    cv2.imshow('Resized_cv2', resized)
    cv2.imshow('imgBGR', img)

    print("Las dimensiones de la imagen es:",img.shape)
    cv2.waitKey(0)

    cv2.destroyAllWindows()