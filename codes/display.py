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
        isMoving = False
        playerMovingLR = 0
        playerMovingUD = 0
        # 进入主循环
        while(True):
            for event in pygame.event.get():
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_w):
                        playerMovingUD = 1
                    if(event.key == pygame.K_a):
                        playerMovingLR = -1
                    if(event.key == pygame.K_s):
                        playerMovingUD = -1
                    if(event.key == pygame.K_d):
                        playerMovingLR = 1
                elif(event.type == pygame.KEYUP):
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        playerMovingUD = 0
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        playerMovingLR = 0
            if playerMovingLR > 0:
                self.stage.playerMove(3)
            elif playerMovingLR < 0:
                self.stage.playerMove(1)
            if playerMovingUD > 0:
                self.stage.playerMove(0)
            elif playerMovingUD < 0:
                self.stage.playerMove(2)
            self.draw()
            pygame.time.delay(17)
            pygame.display.update()

    def draw(self) -> None:
        """
            绘制图像
        """
        self.screen.fill((0,0,0))
        self.playerImgRect.centerx = self.stage.player.pos[0]
        self.playerImgRect.centery = self.stage.player.pos[1]
        self.screen.blit(self.playerImg, self.playerImgRect)
        return

if __name__ == "__main__":
    display = Display()
    display.loop()
