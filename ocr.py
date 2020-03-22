import cv2
import numpy as np

img = cv2.imread('IMG_0684.jpeg', 0)

img[np.where(img>=[100])] = [255]
img[np.where(img<=[100])] = [0]
#img = cv2.bilateralFilter(img, 9, 75, 75)

#img[np.where(img <= [180])] = [0]

cv2.imwrite('asdf.jpg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()