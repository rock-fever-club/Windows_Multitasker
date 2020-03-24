import numpy as np
import cv2

img = cv2.imread('C:\\my_data\\Pictures and Videos\\Kedarnath Trip\\IMG_20190621_113142.jpg')
print(img)
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

rect = (1,1,665,344)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]

tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
b, g, r = cv2.split(img)
rgba = [b,g,r, alpha]
dst = cv2.merge(rgba,4)
cv2.imshow('bg_transparent', dst)
cv2.imwrite("test.png", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
