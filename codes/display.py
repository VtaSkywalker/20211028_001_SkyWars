from bullet import NormalEnemyBullet, PlayerBullet
from player import Player
from stage import Stage
import pygame
from enemy import *

class DisplayConfig:
    """
        关于显示的一些选项
    """
    doShowCrashBox = True # 是否显示碰撞箱

class Display:
    """
        将图形界面展示出来

        Parameters
        ----------
        stage : Stage
            要被展示出来的界面类
    """
    def __init__(self):
        self.stage = Stage()

    def loop(self):
        """
            进入游戏的主循环
        """
        # 整个窗口的初始化
        pygame.init()
        self.hpInfoHeight = 50 # 血条信息所占的高度
        screenSize = (self.stage.screenSize[0], self.stage.screenSize[1]+self.hpInfoHeight)
        self.screen = pygame.display.set_mode(screenSize)

        # 各图像素材初始化
        self.playerImg, self.playerImgRect = self.initImgSrc(Player.srcImg, scale=Player.scale) # 玩家信息初始化
        self.playerBulletImg, self.playerBulletImgRect = self.initImgSrc(PlayerBullet.srcImg, scale=PlayerBullet.scale) # 玩家子弹信息初始化
        self.normalEnemyBulletImg, self.normalEnemyBulletImgRect = self.initImgSrc(NormalEnemyBullet.srcImg, scale=NormalEnemyBullet.scale) # 普通敌人子弹初始化
        self.oneHpEnemyImg, self.oneHpEnemyImgRect = self.initImgSrc(OneHpEnemy.srcImg, scale=OneHpEnemy.scale) # 1血敌人初始化
        self.doubleWarriorImg, self.doubleWarriorImgRect = self.initImgSrc(DoubleWarrior.srcImg, scale=DoubleWarrior.scale) # 双排敌人初始化
        self.tripleShooterImg, self.dtripleShooterImgRect = self.initImgSrc(TripleShooter.srcImg, scale=TripleShooter.scale) # 三线敌人初始化
        # 进入主循环
        while(True):
            # 事件判定
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    exit(0)

            # 根据按键作出响应
            self.playerMove() # 玩家移动
            self.playerFire() # 玩家子弹发射判定

            # 随着时间流逝，进行每一帧的刷新
            self.bulletMove() # 子弹向前推移
            self.epUpdate() # 敌人和玩家更新

            # 更新时间戳
            self.updateTimeStamp()

            # 绘制并更新图像
            self.draw()
            pygame.display.update()

    def draw(self) -> None:
        """
            绘制图像
        """
        # 初始化-黑屏
        self.screen.fill((0,0,0))
        # 玩家飞机显示
        self.playerImgRect.centerx = self.stage.player.pos[0]
        self.playerImgRect.centery = self.stage.player.pos[1]
        self.screen.blit(self.playerImg, self.playerImgRect)
        # 敌人飞机显示
        for eachEnemy in self.stage.enemyContainer:
            # 1血敌人情形
            if(eachEnemy.__class__.__name__ == "OneHpEnemy"):
                eachEnemyImg = self.oneHpEnemyImg
            # 双排战士情形
            elif(eachEnemy.__class__.__name__ == "DoubleWarrior"):
                eachEnemyImg = self.doubleWarriorImg
            # 三线射手情形
            elif(eachEnemy.__class__.__name__ == "TripleShooter"):
                eachEnemyImg = self.tripleShooterImg
            eachEnemyImgRect = eachEnemyImg.get_rect()
            eachEnemyImgRect.centerx = eachEnemy.pos[0]
            eachEnemyImgRect.centery = eachEnemy.pos[1]
            self.screen.blit(eachEnemyImg, eachEnemyImgRect)
        # 碰撞箱显示
        if(DisplayConfig.doShowCrashBox):
            self.showCrashBox()
        # 子弹显示
        for eachBullet in self.stage.bulletContainer:
            # 玩家子弹情形
            if(eachBullet.__class__.__name__ == "PlayerBullet"):
                # 未爆炸时，显示正常图像
                if(not eachBullet.isExplosion):
                    eachBulletImg = self.playerBulletImg
                    eachBulletImgRect = eachBulletImg.get_rect()
                    eachBulletImgRect.centerx = eachBullet.pos[0]
                    eachBulletImgRect.centery = eachBullet.pos[1]
                # 爆炸时，每帧都要单独考虑显示爆炸图像
                else:
                    eachBulletImg, eachBulletImgRect = self.initImgSrc(eachBullet.srcImg, scale=PlayerBullet.scale)
                    eachBulletImgRect.centerx = eachBullet.pos[0]
                    eachBulletImgRect.centery = eachBullet.pos[1]
            # 普通敌人子弹情形
            if(eachBullet.__class__.__name__ == "NormalEnemyBullet"):
                # 未爆炸时，显示正常图像
                if(not eachBullet.isExplosion):
                    eachBulletImg = self.normalEnemyBulletImg
                    eachBulletImgRect = eachBulletImg.get_rect()
                    eachBulletImgRect.centerx = eachBullet.pos[0]
                    eachBulletImgRect.centery = eachBullet.pos[1]
                # 爆炸时，每帧都要单独考虑显示爆炸图像
                else:
                    eachBulletImg, eachBulletImgRect = self.initImgSrc(eachBullet.srcImg, scale=NormalEnemyBullet.scale)
                    eachBulletImgRect.centerx = eachBullet.pos[0]
                    eachBulletImgRect.centery = eachBullet.pos[1]
            self.screen.blit(eachBulletImg, eachBulletImgRect)
        # 血条显示
        self.showPlayerHp()
        return

    def playerMove(self) -> None:
        """
            在每一帧的循环中，更新玩家移动信息
        """
        if(pygame.key.get_pressed()[pygame.K_w]):
            self.stage.playerMove(0)
        if(pygame.key.get_pressed()[pygame.K_a]):
            self.stage.playerMove(1)
        if(pygame.key.get_pressed()[pygame.K_s]):
            self.stage.playerMove(2)
        if(pygame.key.get_pressed()[pygame.K_d]):
            self.stage.playerMove(3)

    def playerFire(self) -> None:
        """
            在每一帧的循环中，判断玩家是否发射子弹
        """
        if(pygame.key.get_pressed()[pygame.K_k]):
            self.stage.playerFire()

    def bulletMove(self) -> None:
        """
            随着每一帧的更新，刷新子弹的位置
        """
        self.stage.updateFire()

    def updateTimeStamp(self) -> None:
        """
            更新时间戳
        """
        FRAME_INTERV = 17
        pygame.time.delay(FRAME_INTERV)
        self.stage.timeStamp += FRAME_INTERV

    def initImgSrc(self, imgSrc, scale):
        """
            初始化图像素材

            Parameters
            ----------
            imgSrc : string
                素材图像名
            scale : float
                素材拉伸比例

            Returns
            -------
            img : Surface
                素材图像
            rect : pygame.Rect
                图像边框
        """
        img = pygame.image.load(imgSrc)
        rect_org = img.get_rect()
        img = pygame.transform.scale(img, (rect_org.size[0] * scale, rect_org.size[1] * scale))
        rect = img.get_rect()
        return [img, rect]

    def epUpdate(self):
        """
            更新敌人和玩家状态
        """
        self.stage.enemySpan() # 敌人生成
        self.stage.enemyFire() # 敌人发射子弹
        self.stage.enemyStateUpdate() # 敌人状态更新
        self.stage.playerStateUpdate() # 玩家状态更新

    def showPlayerHp(self):
        """
            显示玩家血条
        """
        # 底板绘制
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, self.stage.screenSize[1], self.stage.screenSize[0], self.hpInfoHeight))
        # 边框绘制
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, self.stage.screenSize[1], self.stage.screenSize[0], self.hpInfoHeight), width=1)
        # 血条贴出
        scaleX = 1.2
        scaleY = 1
        hpBarImg = pygame.image.load("img/hpBar.png")
        hpBarImgRect = hpBarImg.get_rect()
        hpBarImg = pygame.transform.scale(hpBarImg, (round(hpBarImgRect.size[0] * scaleX), round(hpBarImgRect.size[1] * scaleY)))
        hpBarImgRect = hpBarImg.get_rect()
        hpBarImgRect.centerx = self.stage.screenSize[0] / 2 + 36
        hpBarImgRect.centery = self.stage.screenSize[1] + self.hpInfoHeight / 2
        self.screen.blit(hpBarImg, hpBarImgRect)
        # 按扣血量百分比遮住血条的相应部分
        imgX = [hpBarImgRect.centerx - hpBarImgRect.size[0] / 2, hpBarImgRect.centerx + hpBarImgRect.size[0] / 2]
        imgY = [hpBarImgRect.centery - hpBarImgRect.size[1] / 2, hpBarImgRect.centery + hpBarImgRect.size[1] / 2]
        hpRemainRatio = self.stage.player.hp / self.stage.player.hpMax
        maskX = [imgX[0] + (imgX[1] - imgX[0]) * hpRemainRatio, imgX[1]]
        maskY = [imgY[0], imgY[1]]
        maskRect = pygame.Rect(maskX[0], maskY[0], maskX[1]-maskX[0], maskY[1]-maskY[0])
        pygame.draw.rect(self.screen, (0, 0, 0), maskRect)

    def showCrashBox(self):
        """
            显示碰撞箱
        """
        # 显示敌人的碰撞箱
        for eachEnemy in self.stage.enemyContainer:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(eachEnemy.pos[0]-eachEnemy.crashBox[0], eachEnemy.pos[1]-eachEnemy.crashBox[1], 2*eachEnemy.crashBox[0]+1, 2*eachEnemy.crashBox[1]+1), width=1)
        # 显示玩家的碰撞箱
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.stage.player.pos[0]-self.stage.player.crashBox[0], self.stage.player.pos[1]-self.stage.player.crashBox[1], 2*self.stage.player.crashBox[0]+1, 2*self.stage.player.crashBox[1]+1), width=1)

if __name__ == "__main__":
    display = Display()
    display.loop()
