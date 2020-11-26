class User:
    def __init__(self, user):
        self.data = {}
        self.data["id"] = user["id"]
        self.data["email"] = user["email"]
        self.data["hashedPassword"] = user["hashedPassword"]
        self.data["address"] = user["address"]
        self.data["contact"] = user["contact"]
        self.data["type"] = user["type"]
        self.data["important"] = user["important"]

    def getId(self):
        return self.data["id"]

    def setNewPassword(self, newPassword, pwdContext):
        self.data["hashedPassword"] = pwdContext.hash(newPassword)

    def confirmPassword(self, password, pwdContext):
        return pwdContext.verify(password, self.data["hashedPassword"])

    def getEmail(self):
        return self.data["email"]

    def getAddress(self):
        return self.data["address"]

    def setAddress(self, newAddress):
        self.data["address"] = newAddress

    def getContact(self):
        return self.data["contact"]

    def setContact(self, newContact):
        self.data["contact"] = newContact

    def getType(self):
        return self.data["type"]

    def setType(self, newType):
        self.data["type"] = newType

    def getImportant(self):
        return self.data["important"]

    def setImportant(self, newImportant):
        self.data["important"] = newImportant
