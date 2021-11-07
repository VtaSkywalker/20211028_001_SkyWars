class BaseBullet:
    """
        子弹基类

        Attributes
        ----------
        pos : float[2]
            子弹当前位置
        velocity : float[2]
            子弹发射速度
        srcImg : string
            图像素材所在路径
        atk : float
            攻击力
    """
    def __init__(self, pos, velocity, srcImg):
        self.pos = pos
        self.velocity = velocity
        self.srcImg = None
        self.atk = 0

    def move(self):
        """
            子弹移动
        """
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

class PlayerBullet(BaseBullet):
    """
        玩家发射的子弹

        Attributes
        ----------
    """
    def __init__(self, pos, velocity):
        BaseBullet.__init__(self, pos, velocity, "playerBullet.png")
