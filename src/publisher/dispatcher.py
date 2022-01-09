from src.publisher.message import MessageType, PostMessageType, RequestPostType, SendPostType
from .sender import Sender

class MessageDispatcher:
    def __init__(self, user):
        sender = Sender()

        self.action_dict = {
            MessageType.POST_MESSAGE: PostMessageType(user, sender),
            MessageType.REQUEST_POSTS: RequestPostType(user, sender),
            MessageType.SEND_POSTS: SendPostType(user, sender),
        }

    def action(self, action, message):
        # Build message
        message_built = self.action_dict[action].build(message)

        # Send Message
        # Integrate with Publish
        self.action_dict[action].send(*message_built)