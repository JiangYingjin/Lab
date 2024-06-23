import cv2, copy, sys
import numpy as np
import sympy as sp
from scipy.integrate import quad
import matplotlib.pyplot as plt
from PIL import Image
import os

# 将 NumPy 的默认截断改为系统允许的最大大小
np.set_printoptions(threshold=sys.maxsize)


def imshow(img_, OpenCV=True):
    """展示图像，默认自动转化 BGR -> RGB。注意！BRG 与 RGB 是恰好相反的。第二个参数传入 0 以关闭。"""
    img = copy.deepcopy(img_)
    # 如果是二值或灰度图像
    if img.ndim == 2:
        plt.imshow(img, cmap="gray")
    # 如果是彩色图像
    if img.ndim == 3:
        # 如果展示的是 OpenCV（BGR）
        if OpenCV:
            # 则要将 OpenCV 的 BGR 图像转换为 RGB 图像
            print("Showing OpenCV Image")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif not OpenCV:
            print("Showing PIL Image")
        plt.imshow(img)
    plt.axis("off")  # 去除坐标轴


def imread(filename: str):
    """用 OpenCV（BGR）读取图片文件，不涉及将 BGR 转为 RGB。资源放置在 Src 文件夹下，传入文件名即可。"""
    # 绝对路径、相对路径判断
    if filename.startswith("C:") or filename.startswith("/"):
        img = cv2.imread(filename)
    else:
        img = cv2.imread(f"Src/{filename}")
    imshow(img)
    return img


def imwrite(img: np.array, filename: str):
    dir = f"{os.path.dirname(__file__)}/Out"
    if not os.path.exists(dir):
        os.mkdir(dir)
    cv2.imwrite(f"{dir}/{filename}", img)


def im_replace(img: np.array, _from: tuple, _to: tuple, not_equal=False):
    """_from 和 _to 传入 RGB 元素如 (255, 255, 0), (0, 0, 0)；not_equal 是不等条件，默认为 False（即等于），若为 True，则替换掉满足不等条件的元素。OpenCV（BGR）的通道差异已经封装处理，按 RGB 传入即可。"""
    # 获取深层拷贝
    img = copy.deepcopy(img)
    # 重塑数组的 shape
    shape = img.shape
    img_flatten = img.reshape((shape[0] * shape[1], shape[2]))
    # 进行替换
    if not_equal:
        # 如果是不相等的话，只要有一个元素不相等成立即可
        img_flatten[np.any(img_flatten != _from[::-1], axis=1)] = _to[::-1]
    else:
        # 如果是相等的话，需要三个元素全都相等成立才行
        img_flatten[np.all(img_flatten == _from[::-1], axis=1)] = _to[::-1]
    # 恢复数组的 shape
    img = img_flatten.reshape((shape[0], shape[1], shape[2]))
    # print(img_flatten)
    imshow(img)
    return img


class UnionFind:
    """采用字典来维护 Parent"""

    def __init__(self, element_num=None):
        self.parent = {}
        if element_num is not None:
            for i in range(element_num):
                self.add(i)

    def add(self, x):
        """工具函数，不单独使用"""
        # 如果已经存在则跳过
        if x in self.parent:
            return
        self.parent[x] = x

    def merge(self, x, y):
        if x not in self.parent:
            self.add(x)
        if y not in self.parent:
            self.add(y)
        # 查找到两个元素的树根
        x = self.find(x)
        y = self.find(y)
        # 如果相等，说明属于同一个集合
        if x == y:
            return
        elif x < y:
            self.parent[y] = x
        else:
            self.parent[x] = y

    def find(self, x):
        # 若 Parent 为自身，则已经找到 root
        if self.parent[x] == x:
            return x
        # 否则不断向上找并更新 Parent
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    # 判断是否属于同一个集合
    def same(self, x, y):
        return self.find(x) == self.find(y)


def ndarr_2dim_val(ndarr, i, j, default_val=0):
    shape = ndarr.shape
    n, m = shape[0], shape[1]

    # 越界返回默认值
    if i < 0 or i >= n or j < 0 or j >= m:
        return default_val
    else:
        return ndarr[i, j]

    try:
        # 需要考虑负值的情况
        result = ndarr[i, j]
    except IndexError:
        result = default_val
    return result
