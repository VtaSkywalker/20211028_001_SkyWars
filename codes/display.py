from stage import Stage
import pygame

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
        pygame.init()
        self.screen = pygame.display.set_mode(self.stage.screenSize)
        # 玩家信息初始化
        self.playerImg = pygame.image.load("img/player.png")
        playerScale = 5
        self.playerImgRect_org = self.playerImg.get_rect()
        self.playerImg = pygame.transform.scale(self.playerImg, (self.playerImgRect_org.size[0] * playerScale, self.playerImgRect_org.size[1] * playerScale))
        self.playerImgRect = self.playerImg.get_rect()
        self.stage.player.crashBox = self.playerImgRect
        # 子弹信息初始化
        self.playerBulletImg = pygame.image.load("img/playerBullet.png")
        playerBulletScale = 1
        self.playerBulletImgRect_org = self.playerBulletImg.get_rect()
        self.playerBulletImg = pygame.transform.scale(self.playerBulletImg, (self.playerBulletImgRect_org.size[0] * playerBulletScale, self.playerBulletImgRect_org.size[1] * playerBulletScale))
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

if __name__ == "__main__":
    display = Display()
    display.loop()
