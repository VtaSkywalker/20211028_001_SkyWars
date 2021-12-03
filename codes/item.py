class BaseItem:
    """
        物品基类

        Attributes
        ----------
        itemName : string
            物品的名字，与类名保持一致
        appearPower : float
            出现权重
        srcImg : string
            素材图像所在路径
        img : Image
            图像
        imgRect : Rect
            图像区域
        pos : float[2]
            道具所在位置
        velocity : float
            道具下落速度
    """
    def __init__(self, pos) -> None:
        self.itemName = None
        self.appearPower = None
        self.pos = pos
        self.velocity = [0, 3]

    def move(self):
        """
            子弹移动
        """
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

class RecoverItem(BaseItem):
    """
        回血道具类

        Attributes
        ----------
        addHp : float = 50
            回血量
    """

    srcImg = "./img/recoverItem.png"
    appearPower = 10

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "RecoverItem"
        self.appearPower = 10
        self.addHp = 50

class AddHpLimitItem(BaseItem):
    """
        增加血量上限道具类

        Attributes
        ----------
        addHpLimit : float = 25
            增加血量上限的数量
    """

    srcImg = "./img/recoverItem.png"
    appearPower = 2

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "AddHpLimitItem"
        self.appearPower = 2
        self.addHpLimit = 25

class EnhanceFireItem(BaseItem):
    """
        火力增强道具类

        Attributes
        ----------
        addFireFreq : int = 1
            每秒的次数提升量
    """

    srcImg = "./img/recoverItem.png"
    appearPower = 5

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "EnhanceFireItem"
        self.appearPower = 5
        self.addFireFreq = 1

class EnhanceAtkItem(BaseItem):
    """
        提升攻击道具类

        Attributes
        ----------
        addAtk : float = 2
    """

    srcImg = "./img/recoverItem.png"
    appearPower = 2

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "EnhanceAtkItem"
        self.appearPower = 2
        self.addAtk = 2

class EnhanceDefenItem(BaseItem):
    """
        提升防御道具类

        Attributes
        ----------
        addDefen : float = 1
    """

    srcImg = "./img/recoverItem.png"
    appearPower = 2

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "EnhanceDefenItem"
        self.appearPower = 2
        self.addDefen = 1
