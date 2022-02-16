
import socket
import time

HOST = '127.0.0.1'
PORT = 50007

# HOST = '192.168.0.12'
# PORT = 50001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)

conn, addr = s.accept()

print('Connected by' , addr)
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)
conn.close()

class Client():
    def __init__(self, host, port, packet_size = 4096):
        '''
            접속 정보 설정
            3 input
                host : String
                port : int
                packet_size : int
        '''

        # 접속할 서버 주소 (hostname or ip_address
        # 루프백(loopback) 인터페이스 주소 == localhost == 127.0.0.1
        self.host = host

        # 서버에서 지정된 포트 번호 ( 1~65535 )
        self.port = port

        # 패킷 사이즈
        self.packet_size = packet_size

        self.create()
        self.connect()

    def create(self):
        # 소켓 객체를 생성
        # 주소 체계(address family) : IPv4 = AF_INET / Ipv6 = AF_INET6 / AF_UNIX / AF_CAN / AF_PACKET / AF_RDS
        # 소켓 타입 : TCP = SOCK_STREAM / UDP = SOCK_DGRAM / SOCK_RAW / ...
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("client socket create")

    def connect(self):
        # 서버에 연결
        try:
            self.client_socket.connect((self.host, self.port))
            self.client_socket.settimeout(5)
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            print("connected")
        except Exception as e :
            print("Connect Exception : ", e)
            time.sleep(1)


    def send(self, byte_data) :
        #print('Server ', self , ' called send : ', len(byte_data))
        try :
            self.client_socket.send(byte_data)
        except Exception as e :
            print("send Exception : ", e)
            self.disconnect()

        return True

    def recv(self, size) :
        buf = None
        #print('Server ', self , ' called recv : ', size)
        try :
            buf = self.client_socket.recv(size)
            if not buf :
                return buf
        except Exception as e:
            print("recv Exception : ", e)
            self.disconnect()
        return buf

    def disconnect(self) :
        try :
            print('disconnect called ! : ', self)
            self.client_socket.close()
            self.client_socket = None
        except Exception as e :
            self.client_socket = None
            pass 

    def csv_write(self):
        with open("data.csv", "w") as f:
            for i in range(len(self.data_list)):
                f.write(str(self.data_list[i][3]))
                f.write(',')
                f.write(str(self.data_list[i][4]))
                f.write(',')
                f.write(str(self.data_list[i][5]))
                f.write('\n')


if __name__ == "__main__" :
    client = Client("127.0.0.1", 7979, 3)
    client.send("Hello")
    data = client.recv(1024)
    print( repr(data.decode()) )
