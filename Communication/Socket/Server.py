import socket
import struct
import time

class Server:
    def __init__(self, ip_addr, port, max_connection = 1):
        '''
            접속 정보 설정
            3 input
                ip_addr : String
                port : int
                max_connection : int
        '''

        # 접속할 서버 주소 (hostname or ip_address or "" -> 빈문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용)
        # 루프백(loopback) 인터페이스 주소 == localhost == 127.0.0.1
        self.SERVER_IP = ip_addr

        # 클라이언트 접속을 대기하는 포트 번호 ( 1~65535 )
        self.SERVER_PORT = port

        # 접속을 허용할 최대 갯수
        self.max_connection = max_connection

        self.create()
        self.bind()
        self.listen()

    def create(self):
        # 소켓 객체를 생성
        # 주소 체계(address family) : IPv4 = AF_INET / Ipv6 = AF_INET6 / AF_UNIX / AF_CAN / AF_PACKET / AF_RDS
        # 소켓 타입 : TCP = SOCK_STREAM / UDP = SOCK_DGRAM / SOCK_RAW / ...
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 포트 사용중 에러 해결 (WinError 10048)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print("server socket create")

    def bind(self):
        # bind() -> 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용
        self.server_socket.bind((self.SERVER_IP, self.SERVER_PORT))

        print("server socket bind")

    def listen(self):
        # 서버가 클라이언트의 접속을 허용
        self.server_socket.listen()

        print("server socket listen")

    def accept_client(self):
            
        try:
            # accept() -> 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴
            self.client_socket, self.addr = self.server_socket.accept()

            # 접속한 클라이언트의 주소
            print("Connected by", self.addr)

        except Exception as e :
            print("accept_client Exception : ", e)
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
    server = Server("127.0.0.1", 7979, 3)
    server.accept_client()
    data = server.recv(1024)
    print( data.decode())

