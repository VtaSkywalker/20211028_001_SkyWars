import os.path
import os

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
        scale : float
            拉伸比例
        atk : float
            攻击力
        bulletOwner : char
            子弹发射人。P：玩家，E：敌人
        isExplosion : bool = False
            是否爆炸
        explosionImgSeq : string[]
            子弹爆炸的动画序列
    """
    def __init__(self, pos, velocity, srcImg):
        self.pos = pos
        self.velocity = velocity
        self.srcImg = None
        self.atk = 0
        self.bulletOwner = None
        self.isExplosion = False
        self.explosionImgSeq = None

    def move(self):
        """
            子弹移动
        """
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def nextExplosion(self) -> bool:
        """
            切换子弹爆炸的动画到下一个帧，如果未播放完，返回True，否则返回False
        """
        imgIndex = self.explosionImgSeq.index(self.srcImg)
        imgIndex += 1
        if(imgIndex == len(self.explosionImgSeq)):
            return False
        # 如果未播放完，则切换到下一帧
        self.srcImg = self.explosionImgSeq[imgIndex]
        return True

class PlayerBullet(BaseBullet):
    """
        玩家发射的子弹

        Attributes
        ----------
    """

    srcImg = "img/playerBullet.png"
    scale = 1
    explosionImgSeqRoot = "img/playerBulletExplosionSeq"

    def __init__(self, pos, velocity):
        BaseBullet.__init__(self, pos, velocity, PlayerBullet.srcImg)
        self.bulletOwner = 'P'
        # 初始化子弹爆炸动画序列
        self.explosionImgSeq = [self.srcImg]
        explosionImgSeqList = os.listdir(PlayerBullet.explosionImgSeqRoot)
        explosionImgSeqList.sort()
        for eachImgName in explosionImgSeqList:
            eachImgPath = os.path.join(PlayerBullet.explosionImgSeqRoot, eachImgName)
            self.explosionImgSeq.append(eachImgPath)

class NormalEnemyBullet(BaseBullet):
    """
        普通敌人发射的子弹

        Attributes
        ----------
    """

    srcImg = "img/normalEnemyBullet.png"
    scale = 1
    explosionImgSeqRoot = "img/enemyBulletExplosionSeq"

    def __init__(self, pos, velocity):
        BaseBullet.__init__(self, pos, velocity, NormalEnemyBullet.srcImg)
        self.bulletOwner = 'E'
        # 初始化子弹爆炸动画序列
        self.explosionImgSeq = [self.srcImg]
        explosionImgSeqList = os.listdir(NormalEnemyBullet.explosionImgSeqRoot)
        explosionImgSeqList.sort()
        for eachImgName in explosionImgSeqList:
            eachImgPath = os.path.join(NormalEnemyBullet.explosionImgSeqRoot, eachImgName)
            self.explosionImgSeq.append(eachImgPath)
