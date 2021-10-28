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

    def show(self):
        """
            显示出图像
        """
        pygame.init()
        screen = pygame.display.set_mode(self.stage.screenSize)
