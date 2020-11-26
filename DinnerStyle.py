from functools import reduce


class DinnerStyle:
    def __init__(self, dinnerStyle):
        self.data = {}
        self.data.id = dinnerStyle.id
        self.data.name = dinnerStyle.name
        self.data.items = dinnerStyle.items

    def getId(self):
        return self.data.id

    def getName(self):
        return self.data.name

    def setName(self, newName):
        self.data.name = newName

    def getItems(self):
        return self.data.items

    def setItems(self, newItems):
        self.data.items = newItems

    def calcPrice(self):
        return reduce(lambda x, y: x.getPrice() + y.getPrice(), self.data.items)
