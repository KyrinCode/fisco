class Tx:
    def __init__(self):
        self.group_id = 0
        self.value = 0

    def show(self):
        s = "{group_id: %d, value: %d}" %(self.group_id, self.value)
        return s

class Msg:
    def __init__(self):
        self.secret = ""
        self.A_addr = ""
        self.B_addr = ""
        self.token_name = ""
        self.value = 0
        self.A2B_transactions = []
        self.B2A_transactions = []

    def show(self):
        print("secret: ", self.secret)
        print("A_addr: ", self.A_addr)
        print("B_addr: ", self.B_addr)
        print("token_name: ", self.token_name)
        print("value: ", self.value)
        print("tx count: ", len(self.A2B_transactions)+len(self.B2A_transactions))
        for i, v in enumerate(self.A2B_transactions, 1):
            print("A->B tx%d: %s" %(i, v.show()))
        for i, v in enumerate(self.B2A_transactions, 1):
            print("B->A tx%d: %s" %(i, v.show()))

class Cus:
    def __init__(self):
        self.secret = ""
        self.from_addr = ""
        self.to_addr = ""
        self.token_name = ""
        self.value = 0
        self.transactions = []

    def show(self):
        print("secret: ", self.secret)
        print("from_addr: ", self.from_addr)
        print("to_addr: ", self.to_addr)
        print("token_name: ", self.token_name)
        print("value: ", self.value)
        print("tx count: ", len(self.transactions))
        for i, v in enumerate(self.transactions, 1):
            print("tx%d: %s" %(i, v.show()))