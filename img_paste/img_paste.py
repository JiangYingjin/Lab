from PIL import Image

# 替换图像的单元尺寸（16px * 16px）
unit_pix = 16

# L 是灰度图像
img_bird = Image.open("bird.jpg").convert("L").resize((35 * unit_pix, 35 * unit_pix))

# 对本地图像变量赋值
for i in range(1, 7):
    locals()[f"img{i}"] = Image.open(f"{i}.jpg")

for i in range(35):
    for j in range(35):
        # 截取部分图像
        tmpImg = img_bird.crop(
            (
                i * unit_pix,
                j * unit_pix,
                i * unit_pix + unit_pix,
                j * unit_pix + unit_pix,
            )
        )

        # 计算该部分图像的平均灰度值
        avg_grey = 0
        for x in range(unit_pix):
            for y in range(unit_pix):
                avg_grey += tmpImg.getpixel((x, y)) / 256

        # 对图像进行粘贴
        img_bird.paste(
            # 粘贴的图像变量
            locals()[f"img{6 - int(avg_grey / 256*6)}"],
            # 粘贴的图像区域
            (
                i * unit_pix,
                j * unit_pix,
                i * unit_pix + unit_pix,
                j * unit_pix + unit_pix,
            ),
        )

img_bird.save("converted_bird.jpg")
