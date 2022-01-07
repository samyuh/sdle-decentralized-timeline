
class PostMessage:
    async def send_message(self, user, message):
        # connect = asyncio.open_connection(host=user.ip, port=user.port, loop=asyncio.get_event_loop())
        # reader, writer = await connect

        # print(f"sending message: {message}")
        # writer.write(message.encode())
        # await writer.drain()
        pass
        #sender = Sender(user.port)
        #sender.send_msg(message)

        ### Do we need to receive any output to verify if the message was delivered?
        ### Do we need to return any value?

    async def publish_message(self, users, message):
        tasks = [self.send_message(user, message) for user in users]
        #await asyncio.gather(*tasks) # a '*' to unpack the list into arguments for the gather method
        
        # Debugging
        print(tasks)

        for user in users:
            print(user)
            self.send_message(user, message)
        ### Do we need to handle a return value?

    async def post(self, message):
        try: # TODO: maybe store the already obtained ips and ports, avoiding repetitive requests
            followers_info = await self.server.locate_followers(self.followers)
        except Exception as e:
            print(e)

        #self.timeline.add_message(message)
        await self.publish_message(followers_info, message)

        print(f'Posted message: {message}')