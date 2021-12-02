from random import random


import random

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
        hp = 50
        atk = 10
        defen = 0
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
        hp = 30
        atk = 8
        defen = 0
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
