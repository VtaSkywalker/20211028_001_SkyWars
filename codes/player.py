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
        firePos : float[2][]
            炮口相对于飞机的位置
        fireInterv : float
            最小发射间隔时间，单位：ms
        lastTimeFired : float
            最近一次发射的时间戳
        atk : float
            攻击力
        hp : float
            玩家血量
        hpMax : float
            血量上限
        defen : float
            玩家防御力
        hasBlaster : bool = false
            是否有爆能束
    """

    srcImg = "img/player.png"
    scale = 5

    def __init__(self, initPos):
        
        self.pos = initPos
        self.velocity = 5
        self.crashBox = [4, 3]
        self.scale = Player.scale
        self.firePos = [[0,-35]]
        self.fireInterv = 160
        self.lastTimeFired = 0 # 初始化最近发射时间戳为0
        self.atk = 1000 # 攻击力初始化
        self.hp = 100 # 血量初始化
        self.hpMax = 100 # 血量上限初始化
        self.defen = 0 # 防御力初始化
        self.hasBlaster = False # 是否有爆能束

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

    def crashBoxRescale(self):
        """
            碰撞箱随着图像尺寸放大而放大
        """
        self.crashBox[0] *= self.scale
        self.crashBox[1] *= self.scale

    def addFirePos(self):
        """
            添加炮口数量，最多能加到三个
        """
        if(len(self.firePos) == 1):
            self.firePos = [[-6,-35], [6,-35]]
        elif(len(self.firePos) == 2):
            self.firePos = [[-12,-35], [0,-35], [12,-35]]
        else:
            return
