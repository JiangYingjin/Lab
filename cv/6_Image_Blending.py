# %%
import cv2
import numpy as np


def laplacian_pyramid_blending(A, B, levels):
    # 生成高斯金字塔
    A_copy = A.copy()
    B_copy = B.copy()
    gpA = [A_copy]
    gpB = [B_copy]
    for i in range(levels):
        A_copy = cv2.pyrDown(A_copy)
        B_copy = cv2.pyrDown(B_copy)
        gpA.append(np.float32(A_copy))
        gpB.append(np.float32(B_copy))

    # 生成拉普拉斯金字塔
    lpA = [gpA[levels - 1]]  # 最底层的高斯金字塔图像
    lpB = [gpB[levels - 1]]
    for i in range(levels - 1, 0, -1):
        size = (gpA[i - 1].shape[1], gpA[i - 1].shape[0])
        LA = cv2.subtract(gpA[i - 1], cv2.pyrUp(gpA[i], dstsize=size))
        LB = cv2.subtract(gpB[i - 1], cv2.pyrUp(gpB[i], dstsize=size))
        lpA.append(LA)
        lpB.append(LB)

    # 将两个图像的拉普拉斯金字塔进行融合
    LS = []
    for la, lb in zip(lpA, lpB):
        rows, cols, dpt = la.shape
        ls = np.hstack((la[:, 0 : cols // 2], lb[:, cols // 2 :]))
        LS.append(ls)

    # 重建融合后的图像
    ls_ = LS[0]
    for i in range(1, levels):
        size = (LS[i].shape[1], LS[i].shape[0])
        ls_ = cv2.pyrUp(ls_, dstsize=size)
        ls_ = cv2.add(ls_, LS[i])

    return ls_


# 读取两个图像
image1 = cv2.imread(r"C:\Codes\MATLAB_Files\balloon.png")
image2 = cv2.imread(r"C:\Codes\MATLAB_Files\bulb.png")

# 调整图像大小以保证它们具有相同的尺寸
image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

# 将图像RGB值转换为浮点数
image1 = image1.astype(float)
image2 = image2.astype(float)

# 融合图像
blended_image = laplacian_pyramid_blending(image1, image2, 6)

# 显示融合后的图像
cv2.imshow("Blended Image", blended_image / 255)
cv2.waitKey(0)
cv2.destroyAllWindows()
