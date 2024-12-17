# %%
from tkinter import *
from time import time
import numpy as np
import threading

# 牛不会逃跑，没有漫步机制
# 修正：1多线程（？删掉试试） 2除以0
from control import Control
from creature import Creature

# ======================================================================== 无用的多线程
# import threading
# def thread_it(func, *args):
#     t = threading.Thread(target=func, args=args)
#     t.setDaemon(True)
#     t.start()
# =========================================================================


class MainWindow(Tk):
    def __init__(self, *args, **kw):
        super().__init__()
        # 窗口标题
        self.title("Ecology System")
        # 设置窗口长宽和坐标
        self.geometry("900x700+50+0")
        # canvas 像素大小设置为 600*600
        self.MAP_SIZE = Creature.MAP_SIZE
        self.BLOCK_SIZE = 600 / self.MAP_SIZE
        self.REFRESH_TIME = 250  # 刷新时间（迭代间隔时间），单位：ms
        self.running = False
        self.endOfRound = False
        self.iterateTaskId = ""

        self.mycontrol = Control(self.MAP_SIZE)
        self.mycontrol.barrier_init([0])
        # self.mycontrol.creature_init(
        #    tiger_num=INIT_TIGER_NUM, cow_num=INIT_COW_NUM, grass_num=INIT_GRASS_NUM
        # )

        # 输入草牛虎的初始数量
        self.tigerEntry = Entry(self)
        self.cowEntry = Entry(self)
        self.grassEntry = Entry(self)
        self.tigerEntry.place(relx=0.85, rely=0.8, relwidth=0.1, relheight=0.05)
        self.cowEntry.place(relx=0.85, rely=0.7, relwidth=0.1, relheight=0.05)
        self.grassEntry.place(relx=0.85, rely=0.6, relwidth=0.1, relheight=0.05)
        self.tigerEntry.insert(0, Creature.INIT_TIGER_NUM)  # 物种初始值在 Creature 里面设置
        self.cowEntry.insert(0, Creature.INIT_COW_NUM)
        self.grassEntry.insert(0, Creature.INIT_GRASS_NUM)

        # 设置初始值的提示标签
        Label(self, text="Number of grass").place(
            relx=0.7, rely=0.6, relwidth=0.15, relheight=0.05
        )
        Label(self, text="Number of cow").place(
            relx=0.7, rely=0.7, relwidth=0.15, relheight=0.05
        )
        Label(self, text="Number of tiger").place(
            relx=0.7, rely=0.8, relwidth=0.15, relheight=0.05
        )

        # 当前各物种数量的标签
        self.current_label = Label()
        self.current_label.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.5)

        # 重新初始化按钮，点击后根据输入的值进行重新初始化
        Button(self, text="Initialize", bg="lightblue", command=self.reInit).place(
            relx=0.72, rely=0.9, relwidth=0.1, relheight=0.05
        )
        self.StartStopBtn = Button(
            self, text="Start", bg="lightgreen", command=self.startStopBtnFunc
        )
        self.StartStopBtn.place(relx=0.85, rely=0.9, relwidth=0.1, relheight=0.05)

        # 初始化地图
        self.canvas = Canvas(
            self, highlightbackground="black", highlightthickness=2, bg="lightgreen"
        )
        self.canvas.place(x=5, y=5, relwidth=0.7, relheight=0.9)
        # for i in range(self.MAP_SIZE + 1):
        #     self.canvas.create_line(
        #         self.BLOCK_SIZE * (1 + i),
        #         self.BLOCK_SIZE,
        #         self.BLOCK_SIZE * (1 + i),
        #         self.BLOCK_SIZE * (self.MAP_SIZE + 1),
        #         width=0.3,
        #     )
        #     self.canvas.create_line(
        #         self.BLOCK_SIZE,
        #         self.BLOCK_SIZE * (1 + i),
        #         self.BLOCK_SIZE * (self.MAP_SIZE + 1),
        #         self.BLOCK_SIZE * (1 + i),
        #         width=0.3,
        #     )

        for i in range(0, self.MAP_SIZE):
            for j in range(0, self.MAP_SIZE):
                if self.mycontrol.BarrierMap[i][j] == 1:
                    self.canvas.create_rectangle(
                        self.BLOCK_SIZE + self.BLOCK_SIZE * j,
                        (self.MAP_SIZE - i) * self.BLOCK_SIZE,
                        self.BLOCK_SIZE + self.BLOCK_SIZE * j + self.BLOCK_SIZE,
                        (self.MAP_SIZE - i) * self.BLOCK_SIZE + self.BLOCK_SIZE,
                        fill="SaddleBrown",
                    )

        # 计时与刷新有关
        self.time = time()

        # 窗口显示
        self.mainloop()

    def paintGrass(self, grass):
        self.canvas.create_rectangle(
            self.BLOCK_SIZE + self.BLOCK_SIZE * grass.pos.X,
            (self.MAP_SIZE - grass.pos.Y) * self.BLOCK_SIZE,
            self.BLOCK_SIZE + self.BLOCK_SIZE * grass.pos.X + self.BLOCK_SIZE,
            (self.MAP_SIZE - grass.pos.Y) * self.BLOCK_SIZE + self.BLOCK_SIZE,
            fill="green",
            outline="",
            tags="creature",
        )

    def paintCow(self, cow):
        self.canvas.create_oval(
            self.BLOCK_SIZE + self.BLOCK_SIZE * cow.pos.X + self.BLOCK_SIZE / 8,
            (self.MAP_SIZE - cow.pos.Y) * self.BLOCK_SIZE + self.BLOCK_SIZE / 8,
            self.BLOCK_SIZE
            + self.BLOCK_SIZE * cow.pos.X
            + self.BLOCK_SIZE
            - self.BLOCK_SIZE / 8,
            (self.MAP_SIZE - cow.pos.Y) * self.BLOCK_SIZE
            + self.BLOCK_SIZE
            - self.BLOCK_SIZE / 8,
            fill="blue",
            tags="creature",
        )

    def paintTiger(self, tiger):
        a = self.BLOCK_SIZE
        x = tiger.pos.X
        y = self.MAP_SIZE - tiger.pos.Y

        self.canvas.create_polygon(
            a * (1 + x - 0.2),
            a * (1 + y - 0.2),
            a * (1 + x + 0.5),
            a * (1 + y - 1.3),
            a * (1 + x + 1.2),
            a * (1 + y - 0.2),
            fill="red",
            tags="creature",
        )

    # 刷新地图
    def iterateToNextState(self):
        # 如果没有跑完整轮的话
        if not self.endOfRound:
            # 如果状态是 Running 的话
            if self.running:
                t01 = time()

                T = threading.Thread(target=self.mycontrol.dayPass)
                T.start()
                T.join()

                # 删除上一张 canvas 图中的生物
                self.canvas.delete("creature")

                t20 = time()

                # 重新设置本图的生物标记
                # 用了多线程反而会严重降低性能，原因未知
                for grass in self.mycontrol.CreatureLst[2]:
                    # threading.Thread(target=self.paintGrass,args=(grass,)).start()
                    self.paintGrass(grass)

                for cow in self.mycontrol.CreatureLst[1]:
                    # threading.Thread(target=self.paintCow,args=(cow,)).start()
                    self.paintCow(cow)

                for tiger in self.mycontrol.CreatureLst[0]:
                    # threading.Thread(target=self.paintTiger,args=(tiger,)).start()
                    self.paintTiger(tiger)

                print("重绘耗时：", time() - t20)

                print("周期耗时：", time() - t01)

                # 实时呈报各物种数量
                self.current_label[
                    "text"
                ] = f"""
                                    Number of grass: {str(len(self.mycontrol.CreatureLst[2]))}
                                    Number of cow: {str(len(self.mycontrol.CreatureLst[1]))}
                                    Number of tiger: {str(len(self.mycontrol.CreatureLst[0]))}
                                    """

                delta_time = time() - self.time
                self.time = time()
                # print(
                #     len(self.mycontrol.grassLst),
                #     len(self.mycontrol.cowLst),
                #     len(self.mycontrol.tigerLst),
                #     delta_time,
                # )

                # 如果 cow 和 tiger 中两者均不为零时
                if len(self.mycontrol.CreatureLst[1]) and len(
                    self.mycontrol.CreatureLst[0]
                ):
                    if delta_time < self.REFRESH_TIME:
                        self.iterateTaskId = self.after(
                            int(self.REFRESH_TIME - delta_time), self.iterateToNextState
                        )
                    elif delta_time >= self.REFRESH_TIME:
                        self.iterateTaskId = self.after(1, self.iterateToNextState)

                # cow 和 tiger 中两者有一者为零，停止程序
                else:
                    self.current_label[
                        "text"
                    ] = f"""
                                        Number of grass: {str(len(self.mycontrol.CreatureLst[2]))}
                                        Number of cow: {str(len(self.mycontrol.CreatureLst[1]))}
                                        Number of tiger: {str(len(self.mycontrol.CreatureLst[0]))}
                                            
                                            End of the simulation."""
                    self.toggleState()
                    self.endOfRound = True

            # 没有跑完整轮但状态是 Stop
            if not self.running:
                self.iterateTaskId = self.after(200, self.iterateToNextState)

    # 按钮更新 creature 数量
    def reInit(self):
        self.mycontrol.creature_init(
            tiger_num=int(self.tigerEntry.get()),
            cow_num=int(self.cowEntry.get()),
            grass_num=int(self.grassEntry.get()),
        )

        # 如果已经有一个 iterateToNextState 在计划执行了，则清除这个计划任务
        if self.iterateTaskId != "":
            self.after_cancel(self.iterateTaskId)

        self.endOfRound = False
        self.toggleState(state=True)
        self.iterateToNextState()

    # 停止时需要显示 Start，运行时需要显示 Stop
    runningStr = ["Start", "Stop"]
    runningColor = ["lightgreen", "pink"]

    # 切换状态，无传入参数则 Toggle，传入参数则指定该状态
    def toggleState(self, state=None):
        if state in [False, True]:
            self.running = state
        else:
            self.running = False if self.running == True else True
        self.StartStopBtn.config(
            text=MainWindow.runningStr[self.running],
            bg=MainWindow.runningColor[self.running],
        )

    def startStopBtnFunc(self):
        if self.endOfRound:
            self.reInit()
        else:
            self.toggleState()


if __name__ == "__main__":
    MainWindow = MainWindow()
