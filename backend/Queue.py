class Queue:
    def __init__(self, size):
        self.size = size
        self.list = []

    def push(self, element):
        self.list.append(element)
        if len(self.list) > size:
            self.list = self.list[-size:]

    def __len__(self):
        return len(self.list)

    def __getitem__(self, key):
        return self.list[key]
