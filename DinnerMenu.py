from functools import reduce


class DinnerMenu:
    def __init__(self, dinnerMenu):
        self.data = {}
        self.data.id = dinnerMenu.id
        self.data.name = dinnerMenu.name
        self.data.items = dinnerMenu.items

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
