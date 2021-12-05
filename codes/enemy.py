import random
import numpy as np
from pygame.constants import SYSTEM_CURSOR_HAND

class BaseEnemy:

    img = None
    imgRect = None

    """
        敌人基类

        Attributes
        ----------
        hp : float
            血量
        atk : float
            攻击力
        defen : float
            防御力
        srcImg : string
            素材图片路径
        crashBox : float[2]
            敌人的碰撞箱，数组两个元素分别代表在x/y方向上距中心的距离
        velocity : float[2]
            x和y方向移动速度，速度可以被stage修改
        scale : float
            图像拉伸比例
        pos : float[2]
            当前所处位置
        firePos : float[2][]
            炮口相对于飞机的位置，允许拥有多个炮口
        fireInterv : float
            最小发射间隔时间，单位：ms
        lastTimeFired : float
            最近一次发射的时间戳
        img : string
            贴图
        imgRect : Rect
            贴图的矩形
    """
    def __init__(self, hp, atk, defen, srcImg, crashBox, velocity, scale, pos):
        self.hp = hp
        self.atk = atk
        self.defen = defen
        self.srcImg = srcImg
        self.crashBox = crashBox
        self.velocity = velocity
        self.pos = pos
        self.scale = scale
        self.lastTimeFired = 0 # 初始化最近发射时间戳
        self.firePos = None
        self.fireInterv = None
        
    def move(self):
        """
            敌人最基本的移动方式，左右来回，稳步前进
        """
        vx = self.velocity[0] # 水平方向上的速度
        vy = self.velocity[1] # 竖直方向上的速度
        # 更新位置
        self.pos[0] += vx
        self.pos[1] += vy

    def crashBoxRescale(self):
        """
            碰撞箱随着图像尺寸放大而放大

            Parameters
            ----------
        """
        self.crashBox[0] *= self.scale
        self.crashBox[1] *= self.scale

    def death(self):
        """
            敌人死亡时执行
        """
        pass

class OneHpEnemy(BaseEnemy):
    """
        1血敌人类，被打一下就没了
    """
    
    srcImg = "img/oneHpEnemy.png"
    scale = 5

    def __init__(self, pos):
        hp = 1
        atk = 5
        defen = 0
        crashBox = [4, 3]
        velocity = [0, 3]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[0,35]] # 炮口位置
        # 开火间隔，加上一定的高斯误差，看起来更多样
        mu = 800
        std = 33
        self.fireInterv = random.gauss(mu, std)
        while(self.fireInterv <= 0):
            self.fireInterv = random.gauss(mu, std)

class DoubleWarrior(BaseEnemy):
    """
        双排战士，血量中，一次连排发射两个子弹，径直纵向移动，移动速度低，射击速度中等，防御力中
    """

    srcImg = "img/DoubleWarrior.png"
    scale = 5

    def __init__(self, pos):
        hp = 25
        atk = 10
        defen = 5
        crashBox = [4, 3]
        velocity = [0, 1.5]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[-28,9], [28,9]] # 炮口位置
        self.fireInterv = 1000

class TripleShooter(BaseEnemy):
    """
        三线射手，血量低，一次向三个方向发射子弹，径直纵向移动，移动速度中等，射击速度低
    """

    srcImg = "img/TripleShooter.png"
    scale = 5

    def __init__(self, pos):
        hp = 15
        atk = 8
        defen = 5
        crashBox = [4, 3]
        velocity = [0, 2]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[0,30]] # 炮口位置
        self.fireInterv = 1200

class BulletRainShooter(BaseEnemy):
    """
        弹幕敌人，会往一圈方向发射多个子弹，形成环状区域的弹幕攻击，属于小BOSS级别
    """

    srcImg = "img/BulletRainShooter.png"
    scale = 5

    def __init__(self, pos):
        hp = 250
        atk = 15
        defen = 5
        crashBox = [8, 2]
        velocity = [1, 0]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[0,40]] # 炮口位置
        self.fireInterv = 300
        self.maxHp = 250 # BOSS特有的血量上限

class Sticker(BaseEnemy):
    """
        冲锋者，发射5连并排霰弹，5秒随机横向移动模式+3秒向前突刺模式+2秒复位模式，BOSS
    """

    srcImg = "img/Sticker.png"
    scale = 5

    def __init__(self, pos):
        hp = 300
        atk = 5
        defen = 5
        crashBox = [10, 2]
        velocity = [3, 0]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[0,40]] # 炮口位置
        self.fireInterv = 400
        self.maxHp = 300 # BOSS特有的血量上限

    def modeSwitch(self, timeStamp):
        """
            模式切换，体现为速度更改

            Parameters
            ----------
            timeStamp : float
                时间戳
        """
        second = timeStamp / 1e3
        # 复位后
        if(0 <= second % 10 < 0.1):
            self.velocity = [3, 0]
        # 普通模式
        elif(0.1 <= second % 10 < 5):
            pass
        # 冲刺模式
        elif(5 <= second % 10 < 8):
            self.velocity = [0, 2]
        # 复位模式
        else:
            self.velocity = [0, -3]

class Tracker(BaseEnemy):
    """
        跟踪者，位置上不断接近玩家，子弹对着玩家射
    """

    srcImg = "img/Tracker.png"
    scale = 5

    def __init__(self, pos):
        hp = 300
        atk = 15
        defen = 5
        crashBox = [8, 8]
        velocity = [3, 0]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[0,0]] # 炮口位置
        self.fireInterv = 200
        self.maxHp = 300 # BOSS特有的血量上限

    def move(self, playerPos):
        """
            移动方法，覆盖本身自带的

            Parameters
            ----------
            playerPos : float[2]
                玩家的位置
        """
        dX = playerPos[0] - self.pos[0]
        dY = playerPos[1] - self.pos[1]
        L = (dX**2 + dY**2)**0.5
        self.pos[0] += dX / L * 2
        self.pos[1] += dY / L * 2

class Windmiller(BaseEnemy):
    """
        风车，在中心矩形路线移动，并旋转着向四个方向发射子弹
    """

    srcImg = "img/Windmiller.png"
    scale = 7

    def __init__(self, pos):
        hp = 350
        atk = 7
        defen = 5
        crashBox = [10, 10]
        velocity = [0, 0]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[0,0]] # 炮口位置
        self.fireInterv = 100
        self.maxHp = 350 # BOSS特有的血量上限

    def modeSwitch(self, timeStamp):
        """
            模式切换，体现为速度更改

            Parameters
            ----------
            timeStamp : float
                时间戳
        """
        second = timeStamp / 1e3
        # 左
        if(0 <= second % 10 < 2.5):
            self.velocity = [-1, 0]
        # 下
        elif(2.5 <= second % 10 < 5):
            self.velocity = [0, 1]
        # 右
        elif(5 <= second % 10 < 7.5):
            self.velocity = [1, 0]
        # 上
        else:
            self.velocity = [0, -1]

    def getBulletVelocity(self, timeStamp):
        """
            根据时间戳，获取子弹的速度（方向）

            Returns
            -------
            vList : list
                四个方向的子弹的速度
        """
        second = timeStamp / 1e3
        period = 5 # 子弹发射方向旋转一圈所需时间，单位：秒
        theta = -2 * np.pi * (second % period) / period
        v1 = [5 * np.cos(theta), 5 * np.sin(theta)]
        v2 = [5 * -np.sin(theta), 5 * np.cos(theta)]
        v3 = [5 * -np.cos(theta), 5 * -np.sin(theta)]
        v4 = [5 * np.sin(theta), 5 * -np.cos(theta)]
        vList = [v1, v2, v3, v4]
        return vList

class TieVader(BaseEnemy):
    """
        钛战机（Vader），8秒横向移动，2秒追踪玩家
    """

    srcImg = "img/TieVader.png"
    scale = 5

    def __init__(self, pos):
        hp = 400
        atk = 20
        defen = 5
        crashBox = [11, 5]
        velocity = [0, 0]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[-37,40], [37,40], [-43,40], [43,40]] # 炮口位置
        self.fireInterv = 400
        self.maxHp = 400 # BOSS特有的血量上限

    def modeSwitch(self, timeStamp, playerPos):
        """
            模式切换，体现为速度更改

            Parameters
            ----------
            timeStamp : float
                时间戳
            playerPos : float[2]
                玩家位置
        """
        second = timeStamp / 1e3
        # 2秒追击
        if(8 <= second % 10 < 10):
            dX = playerPos[0] - self.pos[0]
            dY = playerPos[1] - self.pos[1]
            L = (dX**2 + dY**2)**0.5
            self.velocity = [5 * dX / L, 5 * dY / L]
        # 8秒横向移动
        elif(0 <= second % 10 < 0.1):
            self.velocity = [3, 0]
        else:
            pass

class StarDestroyer(BaseEnemy):
    """
        歼星舰，本体只能左右移动，但却可以不断地放出普通钛战机对玩家进行攻击。本体也能发射爆能束，且攻击力极高
    """

    srcImg = "img/BulletRainShooter.png"
    scale = 5

    def __init__(self, pos):
        hp = 600
        atk = 30
        defen = 5
        crashBox = [8, 2]
        velocity = [3, 0]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[0,40]] # 炮口位置
        self.fireInterv = 300
        self.maxHp = 600 # BOSS特有的血量上限

class Tie(BaseEnemy):
    """
        普通钛战机，斜着飞行，发射爆能束，攻击力中偏高，血量中，速度快，射速高~~（命中低）~~
    """
    
    srcImg = "img/oneHpEnemy.png"
    scale = 5

    def __init__(self, pos):
        hp = 30
        atk = 15
        defen = 5
        crashBox = [4, 3]
        if(random.random() > 0.5):
            velocity = [5, 2]
        else:
            velocity = [-5, 2]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[0,35]] # 炮口位置
        self.fireInterv = 200 # 开火间隔

class DeathStar(BaseEnemy):
    """
        死星，最终BOSS，爆能束的发射位置是随机的，并且可以随时放出各种类型的敌机，一次放出1——3架
        有两种爆能束可以发射，一种是普通的红色，另一种是能够摧毁行星的绿色
    """

    srcImg = "img/BulletRainShooter.png"
    scale = 5

    def __init__(self, pos):
        hp = 2000
        atk = 30
        defen = 5
        crashBox = [8, 2]
        velocity = [0, 0]
        BaseEnemy.__init__(self, hp, atk, defen, OneHpEnemy.srcImg, crashBox, velocity, OneHpEnemy.scale, pos=pos)
        self.crashBoxRescale()
        self.firePos = [[0,40]] # 炮口位置
        self.fireInterv_beam = 30
        self.fireInterv_blaster = 500
        self.lastTimeFired_beam = 0
        self.lastTimeFired_blaster = 0
        self.firePos_beam = [[0,40]]
        self.firePos_blaster = [[-50,40], [50, 40], [100, 40]]
        self.maxHp = 2000 # BOSS特有的血量上限

    def modeSwitch(self, timeStamp):
        """
            子弹模式的切换

            Parameters
            ----------
            timeStamp : float
                时间戳
        """
        second = timeStamp / 1e3
        # 10秒发射一次光束，一次持续2秒
        if(0 < second % 10 <= 2):
            self.fireInterv_beam = 30
        elif(2 < second % 10 <= 2.1):
            self.fireInterv_beam = 1e4
            self.firePos_beam = [[random.random() * 400 - 200, 40]]
