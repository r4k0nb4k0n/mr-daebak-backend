class Item:
    def __init__(self, item):
        self.data = {}
        self.data.id = item.id
        self.data.name = item.name
        self.data.type = item.type
        self.data.price = item.price
        self.data.stock = item.stock

    def getId(self):
        return self.data.id

    def getName(self):
        return self.data.name

    def setName(self, newName):
        self.data.name = newName

    def getType(self):
        return self.data.type

    def setType(self, newType):
        self.data.type = newType

    def getPrice(self):
        return self.data.price

    def setPrice(self, newPrice):
        self.data.price = newPrice

    def getStock(self):
        return self.data.stock

    def setStock(self, newStock):
        self.data.stock = newStock
