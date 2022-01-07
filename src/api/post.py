from src.server import Sender
from src.api.snowflake import Snowflake
import asyncio


class PostMessage:

    

    @staticmethod
    def publish_message(username_sender, users, message):

        snowflake_id = Snowflake.get_id(username_sender, 1)
        snowflake_time = Snowflake.get_current_time()

        msg = {
            'header': {
                'id': snowflake_id,
                'user': username_sender,
                'time': snowflake_time,
                'seen': False,
            },
            'content' : message 
        }

        try:
            asyncio.run(publishing(users, msg)) 
        except Exception as e:
            print(e)
       
        
        # Debugging
        #print(tasks)
        # for user in users:
        #     print(user)
        #     sender = Sender(7004)
        #     sender.send_msg("asdasd")
        ### Do we need to handle a return value?
        

    async def post(self, message):
        try: # TODO: maybe store the already obtained ips and ports, avoiding repetitive requests
            followers_info = await self.server.locate_followers(self.followers)
        except Exception as e:
            print(e)

        #self.timeline.add_message(message)
        await self.publish_message(followers_info, message)



async def send_message(user, message):

    print("starting to send")
    
    sender = Sender(user['port'])
    sender.send_msg(message)

    
    

    ### Do we need to receive any output to verify if the message was delivered?
    ### Do we need to return any value?

async def publishing(users,message):

    tasks = [send_message(user, message) for user in users.values()]
    await asyncio.gather(*tasks)


   