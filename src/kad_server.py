

class KadServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.loop = None

    def start_server(self, bootstrap_nodes):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                                      '- %(message)s')
        handler.setFormatter(formatter)



        def connect_to_bootstrap_node(args):
        loop = asyncio.get_event_loop()
        loop.set_debug(True)

        loop.run_until_complete(server.listen(interface=args.ip, port=args.port))
        
        bootstrap_node = (args.ip, 8001)
        loop.run_until_complete(server.bootstrap([bootstrap_node]))

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.stop()
            loop.close()