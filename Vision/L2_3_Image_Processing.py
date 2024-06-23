# %%
from tool import *

# %%
lena = imread("L1_lena.jpg")
lena = cv2.cvtColor(lena, cv2.COLOR_BGR2GRAY)
# %%
lena_color = imread("L1_lena_color.jpg")


# %%
def show_hist(img):
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    fig, ax = plt.subplots()
    ax.bar(range(256), hist.flatten())
    ax.set_title("Histogram")
    ax.set_xlabel("Bins")
    ax.set_ylabel("# of Pixels")
    plt.show()
    return fig


# %%
lena_hist_fig = show_hist(lena)
lena_hist_fig.savefig("Out/L2_3_lena_hist.png")
# %%
lena_norm = cv2.normalize(lena, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
imshow(lena_norm)
imwrite(lena_norm, "Out/L2_3_lena_norm.jpg")
# %%
lena_norm_hist_fig = show_hist(lena_norm)
lena_norm_hist_fig.savefig("Out/L2_3_lena_norm_hist.png")
# %%
lena_eq = cv2.equalizeHist(lena)
imshow(lena_eq)
imwrite(lena_eq, "Out/L2_3_lena_eq.jpg")
# %%
lena_eq_hist_fig = show_hist(lena_eq)
lena_eq_hist_fig.savefig("Out/L2_3_lena_eq_hist.png")
# %%
lena_color_channels = cv2.split(lena_color)
lena_color_channels_norm = [
    cv2.normalize(c, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    for c in lena_color_channels
]
lena_color_channels_eq = [cv2.equalizeHist(c) for c in lena_color_channels]
lena_color_norm = cv2.merge(lena_color_channels_norm)
lena_color_eq = cv2.merge(lena_color_channels_eq)
# %%
imshow(lena_color_norm)
imwrite(lena_color_norm, "Out/L2_3_lena_color_norm.jpg")
# %%
imshow(lena_color_eq)
imwrite(lena_color_eq, "Out/L2_3_lena_color_eq.jpg")
# %%
