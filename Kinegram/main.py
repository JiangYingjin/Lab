#%%
import os
from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#%%
frames=[]
for i in range(1,9):
    frames.append(np.array(Image.open(f'{i}.png')))


#%% 把frames 变成需要的红白色
for n in range(8):
    for i in range(720):
        for j in range(1280):
            if frames[n][i,j]==0:
                frames[n][i,j]=255
            else:
                frames[n][i,j]=0

#%%
patern=np.ones_like(frames[0])
# index = lambda i: (slice(None), slice(i, None, frame_num:=8))
# for i, frame in enumerate(frames): 
    # patern[index(i)] = frame[index(i)]

#%%
1280/16
for i in range(80):
    for j in range(8):
        patern[:,16*i+2*j]=frames[j][:,16*i+2*j]
        patern[:,16*i+2*j+1]=frames[j][:,16*i+2*j+1]


#%%
Image.fromarray(np.uint8(patern)).show()

#%%
Image.fromarray(np.uint8(frames[0])).show()
#%%
nearlyall255=np.ones_like(frames[0])
for i in range(720):
    for j in range(1280):
        nearlyall255[i,j]=255

img=Image.merge('RGB',(Image.fromarray(nearlyall255),Image.fromarray(np.uint8(patern)),Image.fromarray(np.uint8(patern))))

#%%
img.show()
img.save('kinegram.png')
#%%
def card_when(t):
    card = np.zeros_like(patern)
    card[:, 2*t::16] = 1
    card[:, 2*t+1::16] = 1
    return card

fig = plt.figure()
plt.xticks([])
plt.yticks([])
canvas = plt.imshow(patern * card_when(t=0))

#%%
animat = animation.FuncAnimation(
    fig, lambda t: canvas.set_data(patern * card_when(t=t%80)), interval=500).save('scut.gif')
# plt.show()

#%%
# to_save = 255 * np.repeat(np.expand_dims(1 - card_when(0), -1), 4, axis=-1)
# to_save[card_when(0) != 1][-1]=255
# to_save[card_when(0) != 1][0]=0
# to_save[card_when(0) != 1][1]=0
# to_save[card_when(0) == 1][-1] = 0
# Image.fromarray(to_save).convert("RGBA").save('grid.png')

all0=np.zeros_like(frames[0])
nearlyall255=all0.copy()
nearlyall255[:,:]=255
for i in range(80):
    nearlyall255[:,16*i]=0
    nearlyall255[:,16*i+1]=0

grid=Image.merge('RGBA',(Image.fromarray(np.uint8(all0)),Image.fromarray(np.uint8(all0)),Image.fromarray(np.uint8(all0)),Image.fromarray(np.uint8(nearlyall255))))
grid.save('grid.png')