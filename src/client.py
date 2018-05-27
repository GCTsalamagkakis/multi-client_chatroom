################################################
# connection by Rishija	      		       #
# https://github.com/Rishija/python_chatServer #
################################################

import socket
import select
import string
import sys
import os
import sqlite3
 
def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":
     
    conn = sqlite3.connect("users.db")
    dbcursor = conn.cursor()
    command = '''CREATE TABLE IF NOT EXISTS users ('username' text UNIQUE, 'password' text)'''
    dbcursor.execute(command)

     
    logreg=input("press 1 to log in/press 2 to regiser: ") 
    if (logreg==2):
        while True:
            usernamez=raw_input("Select a Username: ")
            passw=raw_input("Select a Password: ")
            command = '''SELECT username FROM users
                         WHERE username=?'''
            dbcursor.execute(command, (usernamez,))
            result = dbcursor.fetchone()
            if result:
                print "This username already exists"
            else:
                command = '''INSERT INTO users VALUES (?, ?)'''
                dbcursor.execute(command, (usernamez, passw))
                conn.commit()
                print "You have succesfully registered"
                break
        
    if logreg==1:
        counter=0
        found=-1
        while True:
            usernamez=raw_input("Give Me Your Username: ")
            passw=raw_input("Give Me Your Password: ")
            command = '''SELECT username, password FROM users
                         WHERE username=? and password=?'''
            dbcursor.execute(command, (usernamez, passw))
            result = dbcursor.fetchone()
            if result:
                print "You have now logged in!"
                break
            else:
                print "the username and/or password are incorrect"
        

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print ('Unable to connect')
        sys.exit()
     
    print ('Connected to remote host. Start sending messages (@username for private message)')
    s.send(usernamez.encode())
    prompt()
    
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if (sock == s):
                data = sock.recv(4096)
                if (not data) :
                    print ('\nDisconnected from chat server')
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()
