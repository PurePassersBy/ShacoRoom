# ShacoRoom



## What is ShacoRoom made of?
* A generalized database connector designed for the chat room.

In the connector files, ServerConn.py will manage all requests of 
MySql query sent to the server since it's not safe to allow users
to access database deployed on Ali Student Server. ServerConn plays 
a role of intermediary which deliver the request from users to server.
As for SQLConn.py, it handles the interactive part between server ans database.

* A friends system which has these basic features:

 1. Add、delete friends and accept or refuse others' friend request 
 
 2、Send a friend request to a user even if he/she was offline. He/she 
  will see the information about friend request once login online.




## How to use?

First, try

```python
pip install -r requirements.txt
```

to access dependent file.



