import serial
import time
from threading import Thread
class SerialWriter(Thread):
    def __init__(self, com_port, baud_rate):
        Thread.__init__(self)
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_port = serial.Serial(self.com_port, self.baud_rate, timeout=0)
        self.last_output = ""

    def run(self):
        self.serial_port.open()
        while True:
            try:
                self.write_serial_data()
            except (Exception) as e:
                print(e)

    def write_serial_data(self, message):
        if self.serial_port.isOpen():
            output = "<" + message + ">"

            if output != "self.last_output":

                try:
                    out = output.encode('utf-8')
                    print(out)
                    self.serial_port.write(out)
                    self.last_output = output
                    self.serial_port.close()
                except (Exception) as e:
                    print(e)
        else:
            self.serial_port.open()
            print('Serial port not open : ' + str(self.com_port))

if __name__ == "__main__":
    ser = SerialWriter('com8', 4800)
    while True:
        ser.write_serial_data("test:1")
        time.sleep(1)
