import zmq
from threading import Thread
from time import monotonic,sleep

class MessageReceiver(Thread):
    def __init__(self, box,freq:float=5):
        super().__init__()
        self.ip = 'tcp://127.0.0.1:8050'
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.setsockopt(zmq.SUBSCRIBE, b"")
        self.connect(self.ip)
        self.box =box
        self.timer =1/freq
        print("yeye")

    def run(self):
        while True:
            try:
                s = monotonic()
                self.recv()
                sleep(self.timer-(monotonic()-s))
            except zmq.ZMQError:
                print('could not receive data')
            except (Exception)as e:
                print(e, 'sada')

    def recv(self):
        """
        read data and append to queue
        """
        received_data = self.socket.recv_json()
        data =received_data['payload_data']
        data = self.sort(data)
        depth = data['depth']
        data = {'depth_rov':depth}
        self.box.update(data)
    def sort(self,data):
        d={}
        for dicts in data:
            d[dicts['name']]=dicts['value']
        return d
    def connect(self,ip):
        self.socket.connect(ip)

    def disconnect(self):
        self.socket.disconnect()
