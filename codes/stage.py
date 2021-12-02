from player import Player
from bullet import *
from enemy import *
import random
import json

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
        # 初始化屏幕
        self.screenSize = (400, 600)
        
        # 初始化玩家
        self.player = Player([self.screenSize[0] * 0.5, self.screenSize[1] * 0.95])
        self.player.crashBoxRescale()
        
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

    def enemyFire(self) -> None:
        """
            敌人发射子弹
        """
        # 对于每个敌人
        for eachEnemy in self.enemyContainer:
            # 如果间隔时间不够，则不发射子弹
            if(self.timeStamp - eachEnemy.lastTimeFired < eachEnemy.fireInterv):
                return
            # 对于每个炮口，生成子弹后，将其加入到子弹容器中
            for eachFirePos in eachEnemy.firePos:
                # 特殊情形：三线射手：
                if(eachEnemy.__class__.__name__ == "TripleShooter"):
                    for eachVelocity in [[0, 5], [-1, 5], [1, 5]]:
                        newBulletPos = [eachEnemy.pos[0]+eachFirePos[0],eachEnemy.pos[1]+eachFirePos[1]]
                        newBullet = NormalEnemyBullet(newBulletPos, eachVelocity)
                        newBullet.atk = eachEnemy.atk
                        self.bulletContainer.append(newBullet)
                # 特殊情形：弹幕敌人：
                if(eachEnemy.__class__.__name__ == "BulletRainShooter"):
                    for eachVelocity in [[5, 0], [3.5355, 3.5355], [0, 5], [-3.5355, 3.5355], [-5, 0], [-3.5355, -3.5355], [0, -5], [3.5355, -3.5355]]:
                        newBulletPos = [eachEnemy.pos[0]+eachFirePos[0],eachEnemy.pos[1]+eachFirePos[1]]
                        newBullet = NormalEnemyBullet(newBulletPos, eachVelocity)
                        newBullet.atk = eachEnemy.atk
                        self.bulletContainer.append(newBullet)
                # 普通情形
                else:
                    newBulletPos = [eachEnemy.pos[0]+eachFirePos[0],eachEnemy.pos[1]+eachFirePos[1]]
                    newBullet = NormalEnemyBullet(newBulletPos, [0, 5])
                    newBullet.atk = eachEnemy.atk
                    self.bulletContainer.append(newBullet)
            # 发射子弹后，更新敌人最近发射时间
            eachEnemy.lastTimeFired = self.timeStamp

    def updateFire(self):
        """
            更新子弹位置，并删除已经到达界外或爆炸结束的子弹
        """
        for eachBullet in self.bulletContainer:
            eachBullet.move()
            # 如果已经移动到了场外，则删除这个子弹
            if(self.isOutside(eachBullet.pos)):
                self.bulletContainer.remove(eachBullet)
            # 如果子弹已爆炸，则更新子弹爆炸状态
            if(eachBullet.isExplosion):
                if(not eachBullet.nextExplosion()):
                    # 若播放已结束，则移除子弹
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
                # 被玩家子弹命中扣血
                if(eachBullet.bulletOwner == 'P' and self.isBulletCrashObj(eachEnemy, eachBullet.pos) and eachBullet.isExplosion == False):
                    eachEnemy.hp -= ((eachBullet.atk - eachEnemy.defen) if (eachBullet.atk >= eachEnemy.defen) else 0)
                    # 血量为0时，敌人死亡
                    if(eachEnemy.hp <= 0):
                        if(eachEnemy in self.enemyContainer): # 这里不知道为什么会出现删除时不在列表中的错误，先加上if保险
                            self.enemyContainer.remove(eachEnemy)
                    # 命中后设置爆炸状态
                    eachBullet.isExplosion = True
                    eachBullet.velocity = [0,0]
                    eachBullet.nextExplosion()
            # 出界一定范围后移除敌人
            effPos = [eachEnemy.pos[0], eachEnemy.pos[1] * 0.8]
            if(self.isOutside(effPos)):
                self.enemyContainer.remove(eachEnemy)

    def playerStateUpdate(self):
        """
            更新玩家状态，包括被子弹命中扣血，血量为零触发事件
        """
        # 与子弹的碰撞
        for eachBullet in self.bulletContainer:
            # 命中扣血
            if(self.isBulletCrashObj(self.player, eachBullet.pos) and eachBullet.isExplosion == False):
                self.player.hp -= (eachBullet.atk - self.player.defen)
                # 死亡时触发事件
                if(self.player.hp <= 0):
                    self.gameover()
                # 命中后设置爆炸状态
                eachBullet.isExplosion = True
                eachBullet.velocity = [0,0]
                eachBullet.nextExplosion()

    def enemyMove(self):
        """
            敌人移动
        """
        for eachEnemy in self.enemyContainer:
            # 如果即将越界，则立刻切换方向，切换后再移动
            newPos = [eachEnemy.pos[0]+eachEnemy.velocity[0], eachEnemy.pos[1]+eachEnemy.velocity[1]]
            if(self.isOutside(newPos)):
                if(newPos[0] < 0 or newPos[0] >= self.screenSize[0]): # 横向出界
                    eachEnemy.velocity[0] = -eachEnemy.velocity[0]
            # 移动
            eachEnemy.move()

    def isBulletCrashObj(self, obj, bulletPos) -> bool:
        """
            检查实体是否被某个子弹命中

            Parameters
            ----------
            obj : BaseEnemy
                实体
            bulletPos : float[2]
                子弹的位置

            Return
            ------
            True / False
                被命中 / 未被命中
        """
        if(obj.pos[0]-obj.crashBox[0] <= bulletPos[0] <= obj.pos[0]+obj.crashBox[0] and obj.pos[1]-obj.crashBox[1] <= bulletPos[1] <= obj.pos[1]+obj.crashBox[1]):
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
        enemySpanConfigFile = open("./config/enemySpanConfig.json", "r")
        enemySpanConfig = json.load(enemySpanConfigFile)
        enemyList = enemySpanConfig["enemies"]
        for eachEnemy in enemyList:
            className = eachEnemy["className"]
            if(eachEnemy["appearBy"] == "time"):
                mu = eachEnemy["mu"]
                std = eachEnemy["std"]
                dtEnemy = random.gauss(mu, std)
                while(dtEnemy < 0):
                    dtEnemy = random.gauss(mu, std)
                if(self.lastTimeStamp % dtEnemy > self.timeStamp % dtEnemy):
                    # 随机位置生成的敌人
                    if(eachEnemy["appearMode"] == "random"):
                        newEnemy = globals()[className]([random.random()*self.screenSize[0], 0])
                    # 固定位置生成的敌人
                    if(eachEnemy["appearMode"] == "fix"):
                        newEnemy = globals()[className]([eachEnemy["posX"], eachEnemy["posY"]])
                    self.enemyContainer.append(newEnemy)
        # 用于下一次的判断
        self.lastTimeStamp = self.timeStamp

    def gameover(self):
        """
            游戏结束触发事件
        """
        print("Game Over!")
        self.player.hp = 0
        pass
