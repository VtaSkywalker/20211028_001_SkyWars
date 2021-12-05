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
    appearPower = 100

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "RecoverItem"
        self.addHp = 50

class AddHpLimitItem(BaseItem):
    """
        增加血量上限道具类

        Attributes
        ----------
        addHpLimit : float = 25
            增加血量上限的数量
    """

    srcImg = "./img/addHpLimitItem.png"
    appearPower = 50
    
    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "AddHpLimitItem"
        self.addHpLimit = 25
        self.velocity = [0, 4.5]

class EnhanceFireItem(BaseItem):
    """
        火力增强道具类

        Attributes
        ----------
        addFireFreq : int = 1
            每秒的次数提升量
    """

    srcImg = "./img/enhanceFireItem.png"
    appearPower = 50

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "EnhanceFireItem"
        self.addFireFreq = 1
        self.velocity = [0, 4.5]

class EnhanceAtkItem(BaseItem):
    """
        提升攻击道具类

        Attributes
        ----------
        addAtk : float = 2
    """

    srcImg = "./img/enhanceAtkItem.png"
    appearPower = 20

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "EnhanceAtkItem"
        self.addAtk = 2
        self.velocity = [0, 6]

class EnhanceDefenItem(BaseItem):
    """
        提升防御道具类

        Attributes
        ----------
        addDefen : float = 1
    """

    srcImg = "./img/enhanceDefenItem.png"
    appearPower = 20

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "EnhanceDefenItem"
        self.addDefen = 1
        self.velocity = [0, 5]

class BlasterItem(BaseItem):
    """
        拾取后，玩家获得爆能束

        Attributes
        ----------
    """

    srcImg = "./img/blasterItem.png"
    appearPower = 2

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "BlasterItem"
        self.addDefen = 1
        self.velocity = [0, 1]

class AddFirePosItem(BaseItem):
    """
        增加玩家的炮口数

        Attributes
        ----------
    """

    srcImg = "./img/addFirePosItem.png"
    appearPower = 2

    def __init__(self, pos) -> None:
        BaseItem.__init__(self, pos)
        self.itemName = "AddFirePosItem"
        self.velocity = [0, 1]
