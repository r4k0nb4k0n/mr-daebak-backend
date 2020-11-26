import datetime


class Order:
    def __init__(self, order):
        self.data = {}
        self.data.id = order.id
        self.data.customerId = order.customerId
        self.data.cookId = order.cookId
        self.data.delivererId = order.delivererId
        self.data.dateStart = order.dateStart
        self.data.dateEnd = order.dateEnd
        self.data.status = order.status
        self.data.address = order.address
        self.data.contact = order.contact
        self.data.creditCardNumber = order.creditCardNumber

    def getId(self):
        return self.data.id

    def getCustomerId(self):
        return self.data.customerId

    def setCustomerId(self, newCustomerId):
        self.data.customerId = newCustomerId

    def getCookId(self):
        return self.data.cookId

    def setCookId(self, newCookId):
        self.data.cookId = newCookId

    def getDelivererId(self):
        return self.data.delivererId

    def setDelivererId(self, newDelivererId):
        self.data.delivererId = newDelivererId

    def getDateStart(self):
        return self.data.dateStart

    def getDateEnd(self):
        return self.data.dateEnd

    def getStatus(self):
        return self.data.status

    def getAddress(self):
        return self.data.address

    def setAddress(self, newAddress):
        self.data.address = newAddress

    def getContact(self):
        return self.data.contact

    def setContact(self, newContact):
        self.data.contact = newContact

    def getCreditCardNumber(self):
        return self.data.creditCardNumber

    def setCreditCardNumber(self, newCreditCardNumber):
        self.data.creditCardNumber = newCreditCardNumber

    def cancel(self):
        timezone = datetime.timezone(datetime.timedelta(hours=9))
        now = datetime.datetime.now(timezone)
        self.data.status = "Canceled"
        self.data.dateEnd = str(now)

    def cook(self, cookId):
        self.data.status = "Cooking"
        self.data.cookId = cookId

    def deliver(self, delivererId):
        self.data.status = "Delivering"
        self.data.delivererId = delivererId

    def finish(self):
        timezone = datetime.timezone(datetime.timedelta(hours=9))
        now = datetime.datetime.now(timezone)
        self.data.status = "Finished"
        self.data.dateEnd = str(now)
