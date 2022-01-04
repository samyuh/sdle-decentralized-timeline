import pickle

from pathlib import Path

class Timeline:
    def __init__(self,username):
        self.username = username
        self.messages = []
        ### Tratar depois aqui dos pickles

    """ Message format:
    message = {
        header: {
            id
            user
            time
            seen
        }
        body?: {
            content
        }
    }
    
    """

    ### Based on index?
    def get_messages_from_user(self, user):

        msgs = []
        for message in self.messages:
            if message.header.user == user: 
                msgs.append(message)

        return msgs

    def add_message(self,message):
        self.messages.append(message)

    def save_messages(self):
        ### Json dump or pickle?
        ### Currently using the pickles from the first project
        with open('./storage/messages.pickle', 'wb') as handle:
            pickle.dump(self.storage, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_messages(self):
        try:
            output_file = open("./storage/messages.pickle", 'rb')
            self.storage = pickle.load(output_file)
            output_file.close()
        except Exception:            
            self.logger.log("PROXY", "warning", "No previous state. New state initialize")
            Path("./storage").mkdir(parents=True, exist_ok=True)