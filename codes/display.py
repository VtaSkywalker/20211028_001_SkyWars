from bullet import PlayerBullet
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
        self.screen = pygame.display.set_mode(self.stage.screenSize)

        # 各图像素材初始化
        self.playerImg, self.playerImgRect = self.initImgSrc(Player.srcImg, scale=Player.scale) # 玩家信息初始化
        self.playerBulletImg, self.playerBulletImgRect = self.initImgSrc(PlayerBullet.srcImg, scale=PlayerBullet.scale) # 子弹信息初始化
        self.oneHpEnemyImg, self.oneHpEnemyImgRect = self.initImgSrc(OneHpEnemy.srcImg, scale=OneHpEnemy.scale) # 1血敌人初始化

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
            self.enemyUpdate() # 敌人更新

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
                eachEnemyImgRect = eachEnemyImg.get_rect()
                eachEnemyImgRect.centerx = eachEnemy.pos[0]
                eachEnemyImgRect.centery = eachEnemy.pos[1]
            self.screen.blit(eachEnemyImg, eachEnemyImgRect)
            if(DisplayConfig.doShowCrashBox):
                self.showCrashBox()
        # 子弹显示
        for eachBullet in self.stage.bulletContainer:
            # 玩家子弹情形
            if(eachBullet.__class__.__name__ == "PlayerBullet"):
                eachBulletImg = self.playerBulletImg
                eachBulletImgRect = eachBulletImg.get_rect()
                eachBulletImgRect.centerx = eachBullet.pos[0]
                eachBulletImgRect.centery = eachBullet.pos[1]
            self.screen.blit(eachBulletImg, eachBulletImgRect)
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

    def enemyUpdate(self):
        """
            更新敌人
        """
        self.stage.enemySpan() # 敌人生成
        self.stage.enemyStateUpdate() # 敌人状态更新

    def showCrashBox(self):
        """
            显示碰撞箱
        """
        # 显示敌人的碰撞箱
        for eachEnemy in self.stage.enemyContainer:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(eachEnemy.pos[0]-eachEnemy.crashBox[0], eachEnemy.pos[1]-eachEnemy.crashBox[1], 2*eachEnemy.crashBox[0]+1, 2*eachEnemy.crashBox[1]+1), width=1)

if __name__ == "__main__":
    display = Display()
    display.loop()
