#!/usr/bin/python3

import pickle, socket, _thread

class Server:

    def __init__(self, addr, port):
        self.running = True
        self.connection = None
        self.host = None
        self.port = port
        self.addr = addr
        self.bitrate = 1024
        self.max_clients = 2
        self.clients = set()
        self.games = {}
        self.token = 0
        self.status = 'Offline'

        self.set_connection()

    def set_connection(self):

        af, st, pr, cn, sa = None, None, None, None, None
        
        for res in socket.getaddrinfo(self.host, self.port,
                socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, st, pr, cn, sa = res
        
            try:
                self.connection = socket.socket(af, st, pr)
                self.status = 'Address Family: {}\nSocket Type: {}\nProtocol: {}\nCanon Name: {}\nServer Address: {}'.format(af, st, pr, cn, sa)

            except socket.error as err:
                self.status = err
                self.connection =  None
                continue
            break
        print(self.status)
        if self.connection is None:
            self.status = "Failed to open socket"
            exit(1)
        else:
            self.open_server()
        print(self.status)

    def get_client(self, conn, player):
        conn.send(pickle.dumps(self.clients[player]))
        client_connected = True

        while client_connected:
            try:
                data = pickle.loads(conn.recv(self.bitrate))
                self.clients[player] = data

                if not data:
                    self.clients.remove(player)
                    self.status = "Disconnected"
                    break
                else:
                    for p in self.clients:
                        response = p

                    self.status = "Recieved: {} Sending: {}".format(response, response)
                conn.sendall(pickle.dumps(response))

            except socket.error as err:
                self.status = err
                break
        self.status = "Connection Ended"
        conn.close()
        print(self.status)

    def open_server(self):
        try:
            self.connection.bind((self.addr, self.port))
            self.status = 'Successfully connected\nAddress: {}\nPort: {}'.format(self.addr, self.port)
        except socket.error as err:
            self.status = err

        print(self.status)
        self.connection.listen(self.max_clients)
        self.status = "Waiting on clients"

    def start(self):
        if self.connection != None:
            self.run()
        print(self.status)

    def run(self):
        self.running = False
        while self.running:
            print(self.status)
            conn, addr = self.connection.accept()
            self.status = "Connected to: {}".format(self.addr)
            _thread.start_new_thread(self.get_client, (conn,))
        self.connection.close()

S = Server('', 5555)
S.start()
