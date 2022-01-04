
DEBUG = True

class KadServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.loop = None

    def start(self, bootstrap_nodes):

        ### TODO: PLace some ifs here with debug flags
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        if DEBUG:
            log = logging.getLogger('kademlia')
            log.addHandler(handler)
            log.setLevel(logging.DEBUG)

        self.server = Server()


        loop = asyncio.get_event_loop()
        loop.set_debug(True)

        loop.run_until_complete(self.server.listen(interface=self.ip, port=self.port))
        loop.run_until_complete(self.server.bootstrap(bootstrap_nodes))

        ### return the loop instead of permanently running it?
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.stop()
            loop.close()

    def close(self):
        self.server.stop()


    async def register(self,username):

        user = await self.server.get(username)

        if user is None:
            ### fill with the necessary data or create and object that contains all the info instead of a dictionary
            user_data = {
                "followers": []
                "following": []
                "ip": self.ip
                "port":self.port
            }
            ### Should the response from set be analysed?
            await self.server.set(username,user_data)
        else:
            ### Should an exception be raised instead?
            print(f"User already exists")

    

    async def login(self,username):

        user = await self.server.get(username)

         if user is not None:
            ### fill with the necessary data or create and object that contains all the info instead of a dictionary
            user_data = {
                "followers": user.followers
                "following": user.following
                "ip": user.ip
                "port": user.port
            }
            ### Should the response from set be analysed?
            await self.server.set(username,user_data)
        else:
            ### Should an exception be raised instead?
            print(f"User doens't exist")
        
    ### Further methods with more specific getters can be created