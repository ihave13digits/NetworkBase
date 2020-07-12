#!/usr/bin/python3

import socket, threading, sys

PORT = 5555

class Server:

    def __init__(self):
        self.bitrate = 1024
        self.max_clients = 2
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.started = False
        self.token = 0

        try:
            self.connection.bind(('0.0.0.0', PORT))
            self.connection.listen()
        except:
            self.connection.close()
            exit()

        self.clients = []

    def handler(self, c, a):
        while self.running:
            data = c.recv(self.bitrate)
            
            # Broadcast data to all clients that aren't the current client in the iteration
            if data:
                print('{}:{} says: {}'.format(a[0], a[1], data))
                for user in self.clients:
                    if user != c:
                        response = str.encode('{}:{} says: {}'.format(a[0], a[1], data))
                        user.send(response)
            else:
                self.clients.remove(c)
                c.close()
                print("{}:{} disconnected\n{} clients left in server.".format(a[0], a[1], len(self.clients)))
                break
            
    def run(self):

        while self.running:
            if self.started and len(self.clients) < 1:
                self.running = False
            if len(self.clients) < self.max_clients:
                c, a = self.connection.accept()
    
                #
                ct = threading.Thread(target=self.handler, args=(c, a))
                ct.daemon = True
                ct.start()


                self.clients.append(c)
                # Show data
                try:
                    print("Token {} belongs to {}".format(self.token, self.clients[self.token]))
                except:
                    pass

                if self.clients:
                    self.started = True
                    try:
                        print("Token {} belongs to {}".format(self.clients[self.token]))
                    except IndexError:
                        if len(self.clients) <= 0:
                            self.connection.close()
                            self.running = False

                self.token += 1
            else:
                pass

class Client:

    def __init__(self, address):
        self.bitrate = 1024
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = True
        
        try:
            self.connection.connect((address, PORT))
            it = threading.Thread(target=self.send)
            it.daemon = True
            it.start()
        except:
            self.connection.close()
            self.connected = False
            exit()

        while self.connected:
            data = self.connection.recv(self.bitrate)
            if not data:
                self.connection.close()
                break
            print(data)

    def send(self):
        while self.connected:
            self.connection.send(bytes(input(": "), 'utf-8'))



if (len(sys.argv) > 2):
    client = Client(sys.argv[2])
elif (len(sys.argv) > 1):
    arg = sys.argv[1]
    if arg == '1' or arg == 'true':
        server = Server()
        server.run()
else:
    pass
