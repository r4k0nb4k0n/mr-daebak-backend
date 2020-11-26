class OrderDetail:
    def __init__(self, orderDetail):
        self.data = {}
        self.data.id = orderDetail.id
        self.data.orderId = orderDetail.orderId
        self.data.dinnerMenu = orderDetail.dinnerMenu
        self.data.dinnerStyle = orderDetail.dinnerStyle

    def getId(self):
        return self.data.id

    def getOrderId(self):
        return self.data.orderId

    def getDinnerMenu(self):
        return self.data.dinnerMenu

    def setDinnerMenu(self, newDinnerMenu):
        self.data.dinnerMenu = newDinnerMenu

    def getDinnerStyle(self):
        return self.data.dinnerStyle

    def setDinnerStyle(self, newDinnerStyle):
        self.data.dinnerStyle = newDinnerStyle

    def calcPrice(self):
        return self.data.dinnerMenu.calcPrice() + self.data.dinnerStyle.calcPrice()
