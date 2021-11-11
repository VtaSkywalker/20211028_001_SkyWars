class Player:
    """
        玩家类

        Attributes
        ----------
        srcImg : string
            玩家的素材图像所在路径
        scale : float
            拉伸比例
        pos : float[2]
            玩家当前所处坐标位置
        velocity : float
            玩家的移动速度
        crashBox : float[2]
            玩家的碰撞箱
        firePos : float[2]
            炮口相对于飞机的位置
        fireInterv : float
            最小发射间隔时间，单位：ms
        lastTimeFired : float
            最近一次发射的时间戳
        atk : float
            攻击力
    """

    srcImg = "img/player.png"
    scale = 5

    def __init__(self, initPos):
        
        self.pos = initPos
        self.velocity = 5
        self.crashBox = None
        self.firePos = [0,-35]
        self.fireInterv = 160
        self.lastTimeFired = 0 # 初始化最近发射时间戳为0
        self.atk = 10 # 攻击力初始化

    def move(self, direction):
        """
            玩家进行移动

            Parameters
            ----------
            direction : int
                移动方向，0:上，1:左，2:下，3:右
        """
        if(direction == 0):
            self.pos[1] -= self.velocity
        elif(direction == 1):
            self.pos[0] -= self.velocity
        elif(direction == 2):
            self.pos[1] += self.velocity
        elif(direction == 3):
            self.pos[0] += self.velocity
