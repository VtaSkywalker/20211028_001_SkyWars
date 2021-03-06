from hashlib import new
from os import remove
from player import Player
from bullet import *
from enemy import *
from item import *
import pygame
import random
import json
import numpy as np

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
        bossName : string[]
            BOSS的类名
        itemDict : dict[]
            所有可能出现的道具（类名）及其权重
            {'itemName' : power}
        itemContainer : BaseItem[]
            道具容器，当前在屏幕范围内的道具
        itemSpawnTable : int[]
            物品生成表，用于后续随机生成物品
        bossTS : float
            最近一次BOSS出现时的时间戳
        level : int
            每击杀一次BOSS，提升一个level，强化新出现的敌人属性
        score : float
            游戏得分
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

        # BOSS名单
        self.bossName = ["BulletRainShooter", "Sticker", "Tracker", "Windmiller", "TieVader", "StarDestroyer", "DeathStar"]

        # 所有可能出现的道具（类名）及其权重
        self.itemDict = {"RecoverItem" : RecoverItem.appearPower, "AddHpLimitItem" : AddHpLimitItem.appearPower, "EnhanceFireItem" : EnhanceFireItem.appearPower, "EnhanceAtkItem" : EnhanceAtkItem.appearPower, "EnhanceDefenItem" : EnhanceDefenItem.appearPower, "BlasterItem" : BlasterItem.appearPower, "AddFirePosItem" : AddFirePosItem.appearPower}

        # 道具容器
        self.itemContainer = []

        # 物品生成表
        self.itemSpawnTable = None
        self.createItemSpawnTable()

        # 最近一次BOSS出现时的时间戳
        self.bossTS = 0

        # level
        self.level = 0

        # 游戏得分
        self.score = 0

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
        for eachFirePos in self.player.firePos:
            newBulletPos = [self.player.pos[0]+eachFirePos[0],self.player.pos[1]+eachFirePos[1]]
            if(self.player.hasBlaster == False):
                newBullet = PlayerBullet(newBulletPos, [0, -10])
            else:
                newBullet = PlayerBlasterBullet(newBulletPos, [0, -10])
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
            # 非最终BOSS情形
            if(eachEnemy.__class__.__name__ != "DeathStar"):
                # 如果间隔时间不够，则不发射子弹
                if(self.timeStamp - eachEnemy.lastTimeFired < eachEnemy.fireInterv):
                    continue
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
                    elif(eachEnemy.__class__.__name__ == "BulletRainShooter"):
                        for eachVelocity in [[5, 0], [3.5355, 3.5355], [0, 5], [-3.5355, 3.5355], [-5, 0], [-3.5355, -3.5355], [0, -5], [3.5355, -3.5355]]:
                            newBulletPos = [eachEnemy.pos[0]+eachFirePos[0],eachEnemy.pos[1]+eachFirePos[1]]
                            newBullet = NormalEnemyBullet(newBulletPos, eachVelocity)
                            newBullet.atk = eachEnemy.atk
                            self.bulletContainer.append(newBullet)
                    # 特殊情形：冲锋者：
                    elif(eachEnemy.__class__.__name__ == "Sticker"):
                        for eachVelocity in [[-0.67, 5], [-0.33, 5], [0, 5], [0.33, 5], [0.67, 5]]:
                            newBulletPos = [eachEnemy.pos[0]+eachFirePos[0],eachEnemy.pos[1]+eachFirePos[1]]
                            newBullet = NormalEnemyBullet(newBulletPos, eachVelocity)
                            newBullet.atk = eachEnemy.atk
                            self.bulletContainer.append(newBullet)
                    # 特殊情形：跟踪者：
                    elif(eachEnemy.__class__.__name__ == "Tracker"):
                        dX = self.player.pos[0] - eachEnemy.pos[0]
                        dY = self.player.pos[1] - eachEnemy.pos[1]
                        L = (dX**2 + dY**2)**0.5
                        bulletVelocity = [dX / L * 5, dY / L * 5]
                        newBulletPos = [eachEnemy.pos[0]+eachFirePos[0],eachEnemy.pos[1]+eachFirePos[1]]
                        newBullet = NormalEnemyBullet(newBulletPos, bulletVelocity)
                        newBullet.atk = eachEnemy.atk
                        self.bulletContainer.append(newBullet)
                    # 特殊情形：风车
                    elif(eachEnemy.__class__.__name__ == "Windmiller"):
                        for eachVelocity in eachEnemy.getBulletVelocity(self.timeStamp):
                            newBulletPos = [eachEnemy.pos[0]+eachFirePos[0],eachEnemy.pos[1]+eachFirePos[1]]
                            newBullet = NormalEnemyBullet(newBulletPos, eachVelocity)
                            newBullet.atk = eachEnemy.atk
                            self.bulletContainer.append(newBullet)
                    # 特殊情形：爵爷
                    elif(eachEnemy.__class__.__name__ == "TieVader"):
                        newBulletPos = [eachEnemy.pos[0]+eachFirePos[0],eachEnemy.pos[1]+eachFirePos[1]]
                        newBullet = EnemyBlasterBullet(newBulletPos, [0, 5])
                        newBullet.atk = eachEnemy.atk
                        self.bulletContainer.append(newBullet)
                    # 特殊情形：歼星舰
                    elif(eachEnemy.__class__.__name__ == "StarDestroyer"):
                        newBulletPos = [eachEnemy.pos[0]+eachFirePos[0],eachEnemy.pos[1]+eachFirePos[1]]
                        newBullet = EnemyBlasterBullet(newBulletPos, [0, 7.5])
                        newBullet.atk = eachEnemy.atk
                        self.bulletContainer.append(newBullet)
                    # 特殊情形：钛战机
                    elif(eachEnemy.__class__.__name__ == "Tie"):
                        newBulletPos = [eachEnemy.pos[0]+eachFirePos[0],eachEnemy.pos[1]+eachFirePos[1]]
                        newBullet = EnemyBlasterBullet(newBulletPos, [0, 5])
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
            # 最终BOSS单独考虑，因为有两种子弹
            else:
                # 普通爆能束
                # 如果间隔时间不够，则不发射子弹
                while True:
                    if(self.timeStamp - eachEnemy.lastTimeFired_blaster < eachEnemy.fireInterv_blaster):
                        break
                    # 随机生成三个位置发射
                    for eachFirePos in [[random.random() * 400, 0], [random.random() * 400, 0], [random.random() * 400, 0]]:
                        newBulletPos = [eachFirePos[0],eachFirePos[1]]
                        newBullet = EnemyBlasterBullet(newBulletPos, [0, 10])
                        newBullet.atk = eachEnemy.atk
                        self.bulletContainer.append(newBullet)
                    # 发射子弹后，更新敌人最近发射时间
                    eachEnemy.lastTimeFired_blaster = self.timeStamp
                    break
                # 光束
                # 如果间隔时间不够，则不发射子弹
                while True:
                    if(self.timeStamp - eachEnemy.lastTimeFired_beam < eachEnemy.fireInterv_beam):
                        break
                    # 对于每个炮口，生成子弹后，将其加入到子弹容器中
                    for eachFirePos in eachEnemy.firePos_beam:
                        newBulletPos = [293, 87]
                        newBullet = DeathStarBeamBullet(newBulletPos, [0, 10])
                        newBullet.atk = eachEnemy.atk
                        self.bulletContainer.append(newBullet)
                    # 发射子弹后，更新敌人最近发射时间
                    eachEnemy.lastTimeFired_beam = self.timeStamp
                    break

    def updateFire(self):
        """
            更新子弹位置，并删除已经到达界外或爆炸结束的子弹
        """
        removeList = []
        for eachBullet in self.bulletContainer:
            eachBullet.move()
            # 如果已经移动到了场外，则删除这个子弹
            if(self.isOutside(eachBullet.pos)):
                removeList.append(eachBullet)
            # 如果子弹已爆炸，则更新子弹爆炸状态
            if(eachBullet.isExplosion):
                if(not eachBullet.nextExplosion()):
                    # 若播放已结束，则移除子弹
                    removeList.append(eachBullet)
        for eachRemoveBullet in removeList:
            self.bulletContainer.remove(eachRemoveBullet)

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
        removeList = []
        self.enemyMove() # 敌人移动
        # 判断敌人与子弹的碰撞以及是否出界
        for eachEnemy in self.enemyContainer:
            # 与子弹的碰撞
            for eachBullet in self.bulletContainer:
                # 被玩家子弹命中扣血
                if(eachBullet.bulletOwner == 'P' and self.isBulletCrashObj(eachEnemy, eachBullet.pos) and eachBullet.isExplosion == False):
                    eachEnemy.hp -= ((eachBullet.atk - eachEnemy.defen) if (eachBullet.atk - eachEnemy.defen >= 1) else 1)
                    # 游戏得分相应地增加
                    self.score += ((eachBullet.atk - eachEnemy.defen) if (eachBullet.atk - eachEnemy.defen >= 1) else 1)
                    # 血量为0时，敌人死亡
                    if(eachEnemy.hp <= 0):
                        if(eachEnemy in self.enemyContainer): # 这里不知道为什么会出现删除时不在列表中的错误，先加上if保险（现在知道了，去掉这句话应该没事）
                            removeList.append(eachEnemy)
                            # 如果死亡的是BOSS，则重设时间戳到打BOSS前的状态，并提升level
                            if(eachEnemy.__class__.__name__ in self.bossName):
                                self.timeStamp = self.bossTS
                                self.player.lastTimeFired = self.bossTS
                                if(eachEnemy.__class__.__name__ == "DeathStar"):
                                    self.level += 3
                                else:
                                    self.level += 1
                            # 敌人死亡时，道具掉落
                            itemXStd = 17
                            itemYStd = 10
                            # 特殊型，多次掉落
                            if(eachEnemy.__class__.__name__ == "BulletRainShooter"):
                                for i in range(3):
                                    self.spawnItem(1, np.array(eachEnemy.pos) + np.array([random.gauss(0, itemXStd), random.gauss(0, itemYStd)]))
                            elif(eachEnemy.__class__.__name__ in ["Sticker", "Tracker"]):
                                for i in range(4):
                                    self.spawnItem(1, np.array(eachEnemy.pos) + np.array([random.gauss(0, itemXStd), random.gauss(0, itemYStd)]))
                            elif(eachEnemy.__class__.__name__ in ["Windmiller", "TieVader"]):
                                for i in range(5):
                                    self.spawnItem(1, np.array(eachEnemy.pos) + np.array([random.gauss(0, itemXStd), random.gauss(0, itemYStd)]))
                                # 击败爵爷时必定掉落爆能束装备
                                if(eachEnemy.__class__.__name__ == "TieVader"):
                                    newItem = BlasterItem(np.array(eachEnemy.pos) + np.array([random.gauss(0, itemXStd), random.gauss(0, itemYStd)]))
                                    self.itemContainer.append(newItem)
                            elif(eachEnemy.__class__.__name__ == "StarDestroyer"):
                                for i in range(10):
                                    self.spawnItem(1, np.array(eachEnemy.pos) + np.array([random.gauss(0, itemXStd), random.gauss(0, itemYStd)]))
                                # 击败歼星舰时必定掉落炮管增加装备
                                newItem = AddFirePosItem(np.array(eachEnemy.pos) + np.array([random.gauss(0, itemXStd), random.gauss(0, itemYStd)]))
                                self.itemContainer.append(newItem)
                            elif(eachEnemy.__class__.__name__ == "DeathStar"):
                                for i in range(20):
                                    self.spawnItem(1, np.array([random.gauss(200, itemXStd), random.gauss(100, itemYStd)]))
                            # 非特殊型，仅一次掉落
                            else:
                                if(eachEnemy.__class__.__name__ == "OneHpEnemy"):
                                    prob = 0.2
                                elif(eachEnemy.__class__.__name__ == "DoubleWarrior"):
                                    prob = 0.33
                                elif(eachEnemy.__class__.__name__ == "TripleShooter"):
                                    prob = 0.33
                                elif(eachEnemy.__class__.__name__ == "Tie"):
                                    prob = 0.45
                                else:
                                    prob = 0
                                self.spawnItem(prob, np.array(eachEnemy.pos) + np.array([random.gauss(0, itemXStd), random.gauss(0, itemYStd)]))
                    # 命中后设置爆炸状态
                    eachBullet.isExplosion = True
                    eachBullet.velocity = [0,0]
                    eachBullet.nextExplosion()
            # 出界一定范围后移除敌人
            effPos = [eachEnemy.pos[0], eachEnemy.pos[1] * 0.8]
            if(self.isOutside(effPos)):
                # BOSS除外
                if(eachEnemy.__class__.__name__ not in self.bossName):
                    removeList.append(eachEnemy)
        for eachRemoveEnemy in removeList:
            try:
                self.enemyContainer.remove(eachRemoveEnemy)
            except:
                continue

    def playerStateUpdate(self):
        """
            更新玩家状态，包括被子弹命中扣血，血量为零触发事件
        """
        # 与子弹的碰撞
        for eachBullet in self.bulletContainer:
            # 命中扣血
            if(self.isBulletCrashObj(self.player, eachBullet.pos) and eachBullet.isExplosion == False):
                self.player.hp -= (eachBullet.atk - self.player.defen) if (eachBullet.atk - self.player.defen >= 1) else 1
                # 死亡时触发事件
                if(self.player.hp <= 0):
                    self.gameover()
                # 命中后设置爆炸状态
                eachBullet.isExplosion = True
                eachBullet.velocity = [0,0]
                eachBullet.nextExplosion()
        # 与物品的碰撞
        removeList = []
        for eachItem in self.itemContainer:
            eachItem.img = pygame.image.load(eachItem.srcImg)
            if(self.isItemPickUp(eachItem)):
                # 根据物品的不同，获得不同的效果
                itemName = eachItem.__class__.__name__
                if(itemName == "RecoverItem"):
                    self.player.hp = self.player.hp + (eachItem.addHp * self.player.hpMax) if(self.player.hp + (eachItem.addHp * self.player.hpMax) <= self.player.hpMax) else self.player.hpMax
                elif(itemName == "AddHpLimitItem"):
                    self.player.hpMax *= (1 + eachItem.addHpLimit)
                elif(itemName == "EnhanceFireItem"):
                    currentFireFreq = 1000 / self.player.fireInterv
                    if(currentFireFreq < 20):
                        newFireFreq = currentFireFreq + eachItem.addFireFreq
                        self.player.fireInterv = 1000 / newFireFreq
                elif(itemName == "EnhanceAtkItem"):
                    self.player.atk *= (1 + eachItem.addAtk)
                elif(itemName == "EnhanceDefenItem"):
                    self.player.defen *= (1 + eachItem.addDefen)
                elif(itemName == "BlasterItem"):
                    self.player.hasBlaster = True
                    self.player.atk *= 2
                elif(itemName == "AddFirePosItem"):
                    self.player.addFirePos()
                    self.player.defen *= 2
                # 吃完道具后，道具消失
                removeList.append(eachItem)
        for eachRemoveItem in removeList:
            self.itemContainer.remove(eachRemoveItem)

    def enemyMove(self):
        """
            敌人移动
            对于特殊的BOSS，还将采取其他的措施
        """
        for eachEnemy in self.enemyContainer:
            # 如果即将越界，则立刻切换方向，切换后再移动
            newPos = [eachEnemy.pos[0]+eachEnemy.velocity[0], eachEnemy.pos[1]+eachEnemy.velocity[1]]
            if(self.isOutside(newPos)):
                if(newPos[0] < 0 or newPos[0] >= self.screenSize[0]): # 横向出界
                    eachEnemy.velocity[0] = -eachEnemy.velocity[0]
            # 移动
            # 特殊情形：Tracker
            if(eachEnemy.__class__.__name__ == "Tracker"):
                eachEnemy.move(self.player.pos)
            # 普通情形
            else:
                eachEnemy.move()
            # 特殊情形：冲锋者的运动状态修改
            if(eachEnemy.__class__.__name__ == "Sticker"):
                eachEnemy.modeSwitch(self.timeStamp)
            # 特殊情形：风车的运动状态修改
            if(eachEnemy.__class__.__name__ == "Windmiller"):
                eachEnemy.modeSwitch(self.timeStamp)
            # 特殊情形：爵爷的运动状态修改
            if(eachEnemy.__class__.__name__ == "TieVader"):
                eachEnemy.modeSwitch(self.timeStamp, self.player.pos)
            # 特殊情形：歼星舰放出钛战机
            if(eachEnemy.__class__.__name__ == "StarDestroyer"):
                if(((self.timeStamp - 1e3 / 60) / 1e3) % 3 > (self.timeStamp / 1e3) % 3):
                    newEnemy = Tie([eachEnemy.pos[0], eachEnemy.pos[1]])
                    self.resetEnemyPowerByLevel(newEnemy)
                    self.enemyContainer.append(newEnemy)
            # 特殊情形：最终BOSS
            if(eachEnemy.__class__.__name__ == "DeathStar"):
                # 炮弹位置切换
                eachEnemy.modeSwitch(self.timeStamp)
                # 放出敌人
                enemyTable = ["OneHpEnemy", "DoubleWarrior", "TripleShooter", "Tie"]
                if(((self.timeStamp - 1e3 / 60) / 1e3) % 3 > (self.timeStamp / 1e3) % 3):
                    for i in range(3):
                        enemyName = enemyTable[int(random.random() * len(enemyTable))]
                        newEnemy = globals()[enemyName]([random.random() * 400, 0])
                        self.resetEnemyPowerByLevel(newEnemy)
                        self.enemyContainer.append(newEnemy)

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
        # 如果BOSS在场，则不生成新的敌人
        if(not self.isBossOnstage()):
            enemySpanConfigFile = open("./config/enemySpanConfig.json", "r")
            enemySpanConfig = json.load(enemySpanConfigFile)
            enemyList = enemySpanConfig["enemies"]
            for eachEnemy in enemyList:
                newEnemy = None
                className = eachEnemy["className"]
                # 间隔固定时间出现的敌人
                if(eachEnemy["appearBy"] == "time"):
                    timeCorr = 0
                    # 对于指定在某个时间段之后才会等间隔出现的敌人，如果时候未到，直接跳过，而如果时间到了，则立刻开始
                    if("firstTime" in eachEnemy.keys()):
                        effTime = eachEnemy["firstTime"] - self.timeStamp
                        if(effTime > 0):
                            continue
                        timeCorr = -eachEnemy["firstTime"]
                    mu = eachEnemy["mu"]
                    std = eachEnemy["std"]
                    dtEnemy = random.gauss(mu, std)
                    while(dtEnemy < 0):
                        dtEnemy = random.gauss(mu, std)
                    if((self.lastTimeStamp + timeCorr) % dtEnemy > (self.timeStamp + timeCorr) % dtEnemy and self.lastTimeStamp < self.timeStamp):
                        # 随机位置生成的敌人
                        if(eachEnemy["appearMode"] == "random"):
                            newEnemy = globals()[className]([random.random()*self.screenSize[0], 0])
                        # 固定位置生成的敌人
                        if(eachEnemy["appearMode"] == "fix"):
                            newEnemy = globals()[className]([eachEnemy["posX"], eachEnemy["posY"]])
                # 在指定时间点立刻生成的敌人
                elif(eachEnemy["appearBy"] == "immediately"):
                    for eachTimeStamp in eachEnemy["spawnAt"]:
                        if(self.lastTimeStamp < eachTimeStamp and self.timeStamp >= eachTimeStamp):
                            # 随机位置生成的敌人
                            if(eachEnemy["appearMode"] == "random"):
                                newEnemy = globals()[className]([random.random()*self.screenSize[0], 0])
                            # 固定位置生成的敌人
                            if(eachEnemy["appearMode"] == "fix"):
                                newEnemy = globals()[className]([eachEnemy["posX"], eachEnemy["posY"]])
                if(newEnemy):
                    self.resetEnemyPowerByLevel(newEnemy)
                    self.enemyContainer.append(newEnemy)
                    # 如果新的敌人是BOSS，则更新BOSS时间戳
                    if(newEnemy.__class__.__name__ in self.bossName):
                        self.bossTS = self.timeStamp
        # 用于下一次的判断
        self.lastTimeStamp = self.timeStamp

    def gameover(self):
        """
            游戏结束触发事件
        """
        print("Game Over! Score : %d" % int(self.score))
        self.player.hp = 0
        pass

    def isBossOnstage(self) -> bool:
        """
            判断BOSS是否在场上
        """
        for eachEnemy in self.enemyContainer:
            if(eachEnemy.__class__.__name__ in self.bossName):
                return True
        return False

    def spawnItem(self, dropProb, pos):
        """
            击杀敌人时调用，尝试生成道具

            Parameters
            ----------
            dropProb : float
                爆率
            pos : float[2]
                爆点
        """
        # 如果没有生成道具，则直接返回
        if(random.random() >= dropProb):
            return
        # 生成道具
        spawnItemName = list(self.itemDict.keys())[self.itemSpawnTable[int(random.random() * len(self.itemSpawnTable))]]
        newItem = globals()[spawnItemName](pos)
        self.itemContainer.append(newItem)

    def itemMove(self):
        """
            物品在场景中移动，其中移出场景的物品被移除
        """
        removeList = []
        for eachItem in self.itemContainer:
            eachItem.move()
            # 出界后移除物品
            effPos = [eachItem.pos[0], eachItem.pos[1] * 0.8]
            if(self.isOutside(effPos)):
                removeList.append(eachItem)
        for eachRemoveItem in removeList:
            self.itemContainer.remove(eachRemoveItem)

    def isItemPickUp(self, item) -> bool:
        """
            检查玩家是否捡到道具

            Parameters
            ----------
            item : BaseItem
                物品
        """
        itemImgRect = item.img.get_rect()
        itemImgRect.centerx = item.pos[0]
        itemImgRect.centery = item.pos[1]
        if(abs(self.player.pos[0] - item.pos[0]) <= (self.player.crashBox[0] + itemImgRect.size[0] / 2) and abs(self.player.pos[1] - item.pos[1]) <= (self.player.crashBox[1] + itemImgRect.size[1] / 2)):
            return True
        return False

    def createItemSpawnTable(self):
        """
            创建物品生成表，用于后续随机生成物品
        """
        self.itemSpawnTable = []
        for (idx, spawnPower) in zip(range(len(self.itemDict.values())), self.itemDict.values()):
            for i in range(spawnPower):
                self.itemSpawnTable.append(idx)

    def resetEnemyPowerByLevel(self, enemy):
        """
            根据level重设敌人属性

            Parameters
            ----------
            enemy : BaseEnemy
        """
        enemy.atk *= (1 + 0.44)**self.level
        enemy.defen *= (1 + 0.15)**self.level
        enemy.hp *= (1 + 0.67)**self.level
        # 非最终BOSS情形
        if(enemy.__class__.__name__  != "DeathStar"):    
            if(enemy.fireInterv >= 50):
                enemy.fireInterv *= (1 - 0.1)**self.level
        # 最终BOSS情形
        else:
            if(enemy.fireInterv_blaster >= 50):
                enemy.fireInterv_blaster *= (1 - 0.15)**self.level
        # 所有BOSS情形
        if(enemy.__class__.__name__  in self.bossName):    
            enemy.maxHp = enemy.hp
