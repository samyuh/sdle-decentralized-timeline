class Timeline:
    def __init__(self,username):
        self.username = username
        self.messages = []

    async def get_messages_from_user(self,user):

        msgs = []
        for message in self.messages:
            if message.user == user: 
                msgs.append(message)

        return msgs

    async def add_message(self,message)
        self.messages.append(message)