# %%
from tool import *


def build_gaussian_pyramid(image, levels):
    pyramid = [image]
    for i in range(levels - 1):
        image = cv2.pyrDown(image)
        pyramid.append(image)
    return pyramid


def build_laplacian_pyramid(image, levels):
    gaussian_pyramid = build_gaussian_pyramid(image, levels)
    for i in range(len(gaussian_pyramid)):
        print(gaussian_pyramid[i].shape)
    laplacian_pyramid = []
    for i in range(levels - 1):
        expanded = cv2.pyrUp(gaussian_pyramid[i + 1])
        # print(expanded.shape, gaussian_pyramid[i].shape)
        laplacian = cv2.subtract(gaussian_pyramid[i], expanded)
        laplacian_pyramid.append(laplacian)
    laplacian_pyramid.append(gaussian_pyramid[-1])
    return laplacian_pyramid


# img1 = imread("image1.jpg")
# img2 = imread("image2.jpg")

# # 调整图像大小为1280p
# height, width = 1280, 720
# interval = 10
# img1 = cv2.resize(img1, (height, width))
# img2 = cv2.resize(img2, (height, width))


# # 设置图像金字塔的层数
# k = 5

# # 构建高斯金字塔和拉普拉斯金字塔
# gaussian_pyramid1 = build_gaussian_pyramid(img1, k)
# laplacian_pyramid1 = build_laplacian_pyramid(img1, k)
# gaussian_pyramid2 = build_gaussian_pyramid(img2, k)
# laplacian_pyramid2 = build_laplacian_pyramid(img2, k)

# # 创建混合图像
# combined_image = np.zeros((height, (width + interval) * k, 3), dtype=np.uint8)
# combined_image.fill(255)

# # 将不同金字塔层的图像进行混合
# for i in range(k):
#     start_height = 0
#     start_width = i * img1.shape[1]
#     blended_image = cv2.addWeighted(
#         gaussian_pyramid1[i], 0.5, gaussian_pyramid2[i], 0.5, 0
#     )
#     combined_image[
#         start_height : start_height + img1.shape[0],
#         start_width : start_width + img1.shape[1],
#     ] = blended_image

#     combined_image[
#         start_height + img1.shape[0] : start_height + img1.shape[0] * 2,
#         start_width : start_width + img1.shape[1],
#     ] = laplacian_pyramid1[i]

# imwrite(combined_image, "blended_image.jpg")


def showPyramids(img, filename):
    def writePyramidHorizontal(pyramidLst, filename):
        totalWidth = 0
        for layer in pyramidLst:
            totalWidth += layer.shape[1]

        totalHeight = pyramidLst[0].shape[0]
        res_img = np.zeros((totalHeight, totalWidth, 3), dtype=np.uint8)
        res_img.fill(255)

        start_width = 0
        for layer in pyramidLst:
            res_img[
                totalHeight - layer.shape[0] : totalHeight,
                start_width : start_width + layer.shape[1],
            ] = layer
            start_width += layer.shape[1]

        imshow(res_img)
        cv2.imwrite(filename, res_img)

    def writePyramid(pyramidLst, filename):
        totalWidth = pyramidLst[0].shape[1] + pyramidLst[1].shape[1]
        totalHeight = pyramidLst[0].shape[0]

        res_img = np.zeros((totalHeight + 10, totalWidth, 3), dtype=np.uint8)
        res_img.fill(255)

        heightLst = np.zeros((len(pyramidLst) - 1), dtype=np.float32)

        for i, layer in enumerate(pyramidLst[1:]):
            heightLst[i] = layer.shape[0]

        # heightLst /= np.sum(heightLst)
        # heightLst *= totalHeight
        # heightLst = np.round(heightLst).astype(np.uint8)
        # heightLst = np.cumsum(heightLst)
        # heightLst = np.insert(heightLst, 0, 0)
        # print(heightLst)

        res_img[0:totalHeight, 0 : pyramidLst[0].shape[1]] = pyramidLst[0]

        startHeight = 0
        for i, layer in enumerate(pyramidLst[1:]):
            res_img[
                startHeight : startHeight + layer.shape[0],
                pyramidLst[0].shape[1] : pyramidLst[0].shape[1] + layer.shape[1],
            ] = layer
            startHeight += layer.shape[0]

        imshow(res_img)
        cv2.imwrite(filename, res_img)

    img = cv2.resize(img, (1280, 720))
    gaussian_pyramid = build_gaussian_pyramid(img, 5)
    laplacian_pyramid = build_laplacian_pyramid(img, 5)
    writePyramid(gaussian_pyramid, f"{filename}_Gaussian_Pyramid.jpg")
    writePyramid(laplacian_pyramid, f"{filename}_Laplacian_Pyramid.jpg")


for i in range(1, 4):
    showPyramids(
        imread(f"Hybrid_Image\Hybrid_image_{i}A.png"),
        f"Hybrid_image_{i}A",
    )
    showPyramids(
        imread(f"Hybrid_Image\Hybrid_image_{i}B.png"),
        f"Hybrid_image_{i}B",
    )
