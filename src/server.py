
################################################
# connection by Rishija	      		       #
# https://github.com/Rishija/python_chatServer #
################################################


import socket
import select
 
def broadcast_data (sock, message):
    #send message to everyone except server and myself
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)
                
def private_data (sock, message):
    #send message in specific user
    for socket in CONNECTION_LIST:
        if socket == sock :
            try :
                socket.send(message)
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":
     
    
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 
    PORT = 5000
    username = []
    #create TCP connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    CONNECTION_LIST.append(server_socket)
    username.append("server")
 
    print("Chat server started on port " + str(PORT))
 
    while 1:
        
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:

            if sock == server_socket:
                
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
                print ("Client (%s, %s) connected" % addr)
                name=sockfd.recv(RECV_BUFFER).decode("ascii")
                print (name)
                username.append(name)
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        private = False
                        cell=CONNECTION_LIST.index(sock)
						#send private message
                        if data[0] == "@":
                            to_who=data.split(None,1)
                            
                            for target in username:
                                if to_who[0][1:]==target:
                                    message = data.split()
                                    to_send = ""
									#exclude username from message
                                    for word in message[1:]:
                                        to_send+= word + " "
                                    to_send+= "\n"
                                    send_to=username.index(target)
                                    private_data(CONNECTION_LIST[send_to],"\r" + "<%s> (private) " % username[cell] + to_send)
                                    private = True
						#no reason to broadcast
                        if private:
                            continue
                        broadcast_data(sock, "\r" + "<%s> " % username[cell] + data)                
                 
                except:
                    print ("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
