import socket

server_socket = socket.socket(socket.AF_INET,   # 통신 채널 선택
                              socket.SOCK_STREAM) # TCP 방식으로 하는거

server_socket.bind(('localhost', 12345))  # bind :  12345포트의 아이피에서  서버로서 동작시키겠다. 
server_socket.listen(0)  # listen : 몇 개까지 동시에 참여시킬 것인지  / 0은 자기가 알아서 한다는 뜻  (서버모드로 동작하겠다.)
print("listening")

client_socket, addr = server_socket.accept() # 클라이언트가 접속이 되기 전까지는 대기상태로 머물고
print("accepting")
data = client_socket.recv(65535) # data : 접속이 되면 64k단위로 쪼개서 보냄

print("recieve : " + data.decode()) # 받은 코드를 디코딩 해서 출력

client_socket.send(data)
print("send data")

client_socket.close()
print("종료")