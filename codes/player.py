class Player:
    """
        玩家类

        Attributes
        ----------
        pos : float[2]
            玩家当前所处坐标位置
        velocity : float
            玩家的移动速度
    """
    def __init__(self, initPos):
        self.pos = initPos
        self.velocity = 5

    def move(self, direction):
        """
            玩家进行移动

            Parameters
            ----------
            direction : int
                移动方向，0:上，1:左，2:下，3:右
        """
        if(direction == 0):
            self.pos[1] -= self.velocity
        elif(direction == 1):
            self.pos[0] -= self.velocity
        elif(direction == 2):
            self.pos[1] += self.velocity
        elif(direction == 3):
            self.pos[0] += self.velocity
