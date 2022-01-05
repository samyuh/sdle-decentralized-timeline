class Message:
    def __init__(self, header, content):
        self.header = header
        self.content = content

    def dump():
        print(f"Message: {self.id}: {self.msg_content}  ExtraInfo: {self.header.dump()}")