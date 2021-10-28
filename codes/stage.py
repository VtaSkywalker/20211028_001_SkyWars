from player import Player

class Stage:
    """
        场景类

        Parameters
        ----------
        screenSize : int[2]
            场景大小
        player : Player
            玩家
    """

    def __init__(self) -> None:
        self.screenSize = (800, 600)
        self.player = Player([self.screenSize[0] * 0.5, self.screenSize[1] * 0.95])

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
        if(aimPos[0] < 0 or aimPos[0] >= self.screenSize[0] or aimPos[1] < 0 or aimPos[1] >= self.screenSize[1]):
            return False
        return True
