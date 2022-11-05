import cv2



im = cv2.imread('test1.jpeg')

cv2.imwrite("resize_input.jpeg ",cv2.resize(im, (int(img.shape[0]/3), int(img.shape[1]/3)), interpolation = cv2.INTER_AREA))
img_size = img.shape    #hei wid channel
print(img_size)