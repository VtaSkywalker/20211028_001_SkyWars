from player import Player
from bullet import *
from enemy import *
import random

class Stage:
    """
        场景类

        Parameters
        ----------
        screenSize : int[2]
            场景大小
        player : Player
            玩家
        bulletContainer : BaseBullet[]
            使用列表存储场景中的所有子弹
        timeStamp : float
            时间戳
        lastTimeStamp : float
            最近一次时间戳
        enemyContainer : BaseEnemy[]
            敌人容器，包含所有在场的敌人
    """
    def __init__(self) -> None:
        self.screenSize = (400, 600)
        self.player = Player([self.screenSize[0] * 0.5, self.screenSize[1] * 0.95])
        self.bulletContainer = []
        self.enemyContainer = []
        self.timeStamp = 0 # 初始化游戏时间戳为零
        self.lastTimeStamp = 0 # 最近一次时间戳

    def playerMove(self, direction) -> None:
        """
            玩家移动

            Parameters
            ----------
            direction : int
                移动方向，0:上，1:左，2:下，3:右
        """
        if(direction == 0 and self.checkPlayerMove((self.player.pos[0], self.player.pos[1]-self.player.velocity))):
            self.player.pos[1] -= self.player.velocity
        elif(direction == 1 and self.checkPlayerMove((self.player.pos[0]-self.player.velocity, self.player.pos[1]))):
            self.player.pos[0] -= self.player.velocity
        elif(direction == 2 and self.checkPlayerMove((self.player.pos[0], self.player.pos[1]+self.player.velocity))):
            self.player.pos[1] += self.player.velocity
        elif(direction == 3 and self.checkPlayerMove((self.player.pos[0]+self.player.velocity, self.player.pos[1]))):
            self.player.pos[0] += self.player.velocity

    def checkPlayerMove(self, aimPos) -> bool:
        """
            检查玩家是否能够移动

            Parameters
            ----------
            aimPos : float[2]
                目标移动到的位置
        """
        # 边界判定
        if(self.isOutside(aimPos)):
            return False
        return True

    def playerFire(self) -> None:
        """
            玩家发射子弹
        """
        # 如果间隔时间不够，则不发射子弹
        if(self.timeStamp - self.player.lastTimeFired < self.player.fireInterv):
            return
        # 生成子弹后，将其加入到子弹容器中
        newBulletPos = [self.player.pos[0]+self.player.firePos[0],self.player.pos[1]+self.player.firePos[1]]
        newBullet = PlayerBullet(newBulletPos, [0, -10])
        newBullet.atk = self.player.atk
        self.bulletContainer.append(newBullet)
        # 发射子弹后，更新玩家最近发射时间
        self.player.lastTimeFired = self.timeStamp

    def updateFire(self):
        """
            更新子弹位置，并删除已经到达界外的子弹
        """
        for eachBullet in self.bulletContainer:
            eachBullet.move()
            # 如果已经移动到了场外，则删除这个子弹
            if(self.isOutside(eachBullet.pos)):
                self.bulletContainer.remove(eachBullet)

    def isOutside(self, pos) -> bool:
        """
            边界判定，判断一个坐标是否超出了边界范围

            Parameters
            ----------
            pos : float[2]
                待判断的坐标
        """
        if(pos[0] < 0 or pos[0] >= self.screenSize[0] or pos[1] < 0 or pos[1] >= self.screenSize[1]):
            return True
        return False

    def enemyStateUpdate(self):
        """
            逐个判断敌人的状态，并删除场外或已被消灭的敌人
        """
        self.enemyMove() # 敌人移动
        # 判断敌人与子弹的碰撞以及是否出界
        for eachEnemy in self.enemyContainer:
            # 与子弹的碰撞
            for eachBullet in self.bulletContainer:
                # 命中扣血
                if(self.isBulletCrashEnemy(eachEnemy, eachBullet.pos)):
                    eachEnemy.hp -= ((eachBullet.atk - eachEnemy.defen) if (eachBullet.atk >= eachEnemy.defen) else 0)
                    # 血量为0时，敌人死亡
                    if(eachEnemy.hp <= 0):
                        if(eachEnemy in self.enemyContainer): # 这里不知道为什么会出现删除时不在列表中的错误，先加上if保险
                            self.enemyContainer.remove(eachEnemy)
                    # 命中后子弹消失
                    self.bulletContainer.remove(eachBullet)
            # 出界一定范围后移除敌人
            effPos = [eachEnemy.pos[0], eachEnemy.pos[1] * 0.8]
            if(self.isOutside(effPos)):
                self.enemyContainer.remove(eachEnemy)

    def enemyMove(self):
        """
            敌人移动
        """
        for eachEnemy in self.enemyContainer:
            # 如果即将越界，则立刻切换方向，切换后再移动
            newPos = [eachEnemy.pos[0]+eachEnemy.velocity[0], eachEnemy.pos[1]+eachEnemy.velocity[1]]
            if(self.isOutside(newPos)):
                if(newPos[0] < 0 or newPos[0] > self.screenSize[0]): # 横向出界
                    eachEnemy.velocity[0] = -eachEnemy.velocity[0]
            # 移动
            eachEnemy.move()

    def isBulletCrashEnemy(self, enemy, bulletPos) -> bool:
        """
            检查敌人是否被某个子弹命中

            Parameters
            ----------
            enemy : BaseEnemy
                敌人
            bulletPos : float[2]
                子弹的位置

            Return
            ------
            True / False
                被命中 / 未被命中
        """
        if(enemy.pos[0]-enemy.crashBox[0] <= bulletPos[0] <= enemy.pos[0]+enemy.crashBox[0] and enemy.pos[1]-enemy.crashBox[1] <= bulletPos[1] <= enemy.pos[1]+enemy.crashBox[1]):
            return True
        return False

    def enemyDeath(self):
        """
            敌人死亡时执行
        """
        pass

    def enemySpan(self):
        """
            敌人生成机制
        """
        # 1秒生成一个1血敌人
        dtOneHpEnemy = 1000
        if(self.lastTimeStamp % 1000 > self.timeStamp % 1000):
            newEnemy = OneHpEnemy([random.random()*self.screenSize[0], 0])
            self.enemyContainer.append(newEnemy)
        # 为了方便下一次的判断
        self.lastTimeStamp = self.timeStamp
