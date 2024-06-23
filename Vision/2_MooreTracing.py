# %%
from tool import *

# 读入图像并黑白化
img = imread("2_moore_tracing.png")
img = im_replace(img, (0, 0, 0), (255, 255, 255))
img = im_replace(img, (255, 255, 255), (0, 0, 0), not_equal=True)

# %%
img = img[:, :, 0]
img = np.where(img == 255, 0, 1)


def loopNext(loopingLst: list, currIdx: int):
    """返回下一个下标、下一个元素"""
    nextIdx = currIdx + 1 if currIdx + 1 < len(loopingLst) else 0
    return nextIdx, loopingLst[nextIdx]


def getInitPoint(img):
    """从下到上，从左到右，找到起始点。前景为 1，后景为 0。"""
    M, N = img.shape
    for j in range(N):
        for i in range(M - 1, -1, -1):
            if img[i, j] == 1:
                return i, j


def mooreNeighborhoodTracing(img):
    scanningSeq = [
        ((-1, 1), 5),
        ((0, 1), 7),
        ((1, 1), 7),
        ((1, 0), 1),
        ((1, -1), 1),
        ((0, -1), 3),
        ((-1, -1), 3),
        ((-1, 0), 5),
    ]

    M, N = img.shape

    # 初始化相关参数
    startPoint = getInitPoint(img)
    currPoint = startPoint
    currSeq = 5

    boundaryLst = [currPoint]

    while True:
        # Jocab 终止条件
        if currPoint == startPoint and currSeq == 5 and len(boundaryLst) > 1:
            break

        # 计算下一个点坐标和进入方向
        x, y = currPoint
        nextSeq, ((dx, dy), enterSeq) = loopNext(scanningSeq, currSeq)
        currSeq = nextSeq
        nextPoint = (x + dx, y + dy)

        # 如果下一个点为前景
        if img[nextPoint] == 1:
            # 添加其为边界
            boundaryLst.append(currPoint)
            # 切换当前点
            currPoint = nextPoint
            # 切换进入方向
            currSeq = enterSeq

    # 绘制边界图
    I = np.full((M, N, 3), fill_value=255)
    for point in boundaryLst:
        I[point] = (0, 0, 0)
    imshow(I, OpenCV=False)

    # 返回边界点列表
    return boundaryLst


boundaryLst = mooreNeighborhoodTracing(img)
print(f"Number of Boundary Points:", len(boundaryLst))
print("Boundary Points:", boundaryLst)
