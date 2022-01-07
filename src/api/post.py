from src.server import Sender
import asyncio


class PostMessage:

    

    @staticmethod
    def publish_message(users, message):

        try:
            asyncio.run(publishing(users, message)) 
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
    
    sender = Sender(user['port'])
    sender.send_msg(message)
    

    ### Do we need to receive any output to verify if the message was delivered?
    ### Do we need to return any value?

async def publishing(users,message):

    tasks = [send_message(user, message) for user in users.values()]
    await asyncio.gather(*tasks)


   