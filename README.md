# multi-client_chatroom
Python 2 Multi-client chatroom with log-in/sign-up

# Initialize
### Server
  `python server.py`
  
### Client
  `python client.py localhost 5000`
  
## Login/Register
  client decides if he wants to log in or register with an existing account
  ### Log In
    user gives a username and a password, if the info matches a database entry, the user logs in
    otherwise the user must try again
    
  ### Register
    user gives a username and a password, if the username already exists in the database, the user gets to try again
    if there is not such an entry, the user registers successfully and an entry to the database is made
    ![33747790_10211551272873508_8926164247046520832_n](https://user-images.githubusercontent.com/38569768/40589796-95df03f8-61fc-11e8-968d-717d9af1d3e7.png)
    
## Communication
  users write messages to each other and that message is broadcasted to everyone
  there is also the choice to privately message a certain user with `@username` in the beginning of the message
