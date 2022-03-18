import socket
import time
from concurrent.futures import ThreadPoolExecutor

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
        self.server_ip = ip_addr

        # 클라이언트 접속을 대기하는 포트 번호 ( 1~65535 )
        # 포트별 쓰레드풀 생성
        self.server_port = port

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

        print("Server Socket Create")

    def bind(self):
        # bind() -> 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용
        self.server_socket.bind((self.server_ip, self.server_port))

        print("Server Socket Bind")

    def listen(self):
        # 서버가 클라이언트의 접속을 허용
        self.server_socket.listen()

        print("Server Socket Listen")

    def accept_client(self):
        while True:
            try:
                # accept() -> 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴
                self.client_socket, self.addr = self.server_socket.accept()

                # 접속한 클라이언트의 주소
                print("Connected by", self.addr)

            except KeyboardInterrupt:
                raise KeyboardInterrupt

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


class ServerThreadPool():
    def __init__(self, ip_addr, port_list, max_connection):
        self.setup_threadpool()
        self.server_ip = ip_addr
        self.port_list = port_list

    def setup_threadpool(self): 
        self.thread_pool = ThreadPoolExecutor(6)

    def server_port(self):
        print("len(self.port_list) : ", len(self.port_list))
        for i in range(len(self.port_list)):
            self.port = {
                "port" + str(self.port_list[i]) : Server(self.server_ip, self.port_list[i])  
            }
            self.thread_pool.submit( self.port["port" + str(self.port_list[i])].accept_client() )
        print(self.port)

    def close_all_connections(self, port) : 
        print("all connection closed")
        for i in port:
            self.port_list["port" + str(self.port_list[i])].disconnect()


if __name__ == "__main__" :
    ip_addr = "127.0.0.1"
    port_list = [7979, 7980]

    server = ServerThreadPool(ip_addr, port_list, 3)
    server.server_port()
    # server.accept_client()
    # data = server.recv(10)
    # print(data.decode())
    # server.send(data)

