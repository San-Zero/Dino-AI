import numpy as np
import cv2

# 設定文件路徑
img_path = 'test.png'
# Read image
img = cv2.imread(img_path)

# 創建一個視窗
cv2.namedWindow("image", flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
cv2.namedWindow("image_roi", flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)

cv2.imshow("image", img)
# 是否顯示網格
showCrosshair = True
# 如果為Ture的話 , 則鼠標的其實位置就作為了roi的中心
# False: 從左上角到右下角選中區域
fromCenter = False
# Select ROI
rect = cv2.selectROI("image", img, showCrosshair, fromCenter)

print("選取的矩形區域")
(x, y, w, h) = rect

# Crop image
imCrop = img[y: y + h, x: x + w]

# Display cropped image
print("left: ", x)
print("top: ", y)
print("width: ", w)
print("height: ", h)

cv2.imshow("image_roi", imCrop)
cv2.imwrite("image_roi.png", imCrop)
cv2.waitKey(0)
