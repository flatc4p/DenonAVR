import socket


class DenonAVR:
    def __init__(self, address, name):
        self.name = name
        self.address = address
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isconnected = False

    def connect(self):
        if self.isconnected:
            print("Already connected to AVR!")
        else:
            try:
                self.s.connect((self.address, 23))
            except socket.error:
                print('Connection timed out!')
            else:
                print("Connected to ", self.name, "!" )
                self.isconnected = True

    def disconnect(self):
        if self.isconnected:
            print("Disconnect from ", self.name, "!")
            self.s.detach()
        else:
            print("Not connected to AVR")

    def toggle_standby(self):
        __doc__ = '''Requesting current power status from AVR
        Turn on if in standby, switch to standby if it's on'''
        if self.isconnected:
            self.s.send(b'PW?\r')
            if self.s.recv(256) == b'PWON\r':
                print("Turning off AVR!")
                self.s.send(b'PWSTANDBY\r')
            if self.s.recv(256) == b'PWSTANDBY\r':
                print("Turning on AVR!")
                self.s.send(b'PWON\r')
        else:
            print("Not connected to AVR!")

    def volume(self, volume):
        if volume > 99:
            volume = 99
        if volume < 0:
            volume = 0
        if self.isconnected:
            command = b'MV' + str(volume).encode('UTF-8') + b'\r'
            print("Setting master volume to ", str(volume), "!")
            self.s.send(command)
        else:
            print("Not connected to AVR!")

    def volume_up(self):
        if self.isconnected:
            print("Turning volume up!")
            self.s.send(b"MVUP\r")
            print("Master volume turned up to ", self.s.recv(256))
        else:
            print("Not connected to AVR!")

    def volume_down(self):
        if self.isconnected:
            print("Turning volume down!")
            self.s.send(b"MVDOWN\r")
            print("Master volume turned down to ", self.s.recv(256))
        else:
            print("Not connected to AVR!")
