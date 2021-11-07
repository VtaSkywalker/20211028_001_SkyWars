class BaseEnemy:
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
        pos : float[2]
            当前所处位置
    """
    def __init__(self, hp, atk, defen, srcImg, crashBox, velocity, pos):
        self.hp = hp
        self.atk = atk
        self.defen = defen
        self.srcImg = srcImg
        self.crashBox = crashBox
        self.velocity = velocity
        self.pos = pos

    def move(self):
        """
            敌人最基本的移动方式，左右来回，稳步前进
        """
        vx = self.velocity[0] # 水平方向上的速度
        vy = self.velocity[1] # 竖直方向上的速度
        # 更新位置
        self.pos[0] += vx
        self.pos[1] += vy

    def crashBoxRescale(self, scale):
        """
            碰撞箱随着图像尺寸放大而放大

            Parameters
            ----------
            scale : float
                放大倍率
        """
        self.crashBox[0] *= scale
        self.crashBox[1] *= scale

    def death(self):
        """
            敌人死亡时执行
        """
        pass

class OneHpEnemy(BaseEnemy):
    """
        1血敌人类，被打一下就没了
    """
    def __init__(self, pos):
        hp = 1
        atk = 5
        defen = 0
        srcImg = "..."
        crashBox = [-1, -1]
        velocity = [7.5, 3]
        BaseEnemy.__init__(self, hp, atk, defen, srcImg, crashBox, velocity, pos=pos)
