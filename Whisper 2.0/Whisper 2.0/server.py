import base64
import hashlib
import os
import json
import mysql.connector as mc
from socket import AF_INET, socket, SOCK_STREAM,gethostbyname,gethostname
from threading import Thread
from Cryptodome.Cipher import AES
from Cryptodome import Random

# For AES Encryptiion
BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[0:-ord(s[-1:])]
# We use the symmetric Encryption So this password have to be the same in both client and server
password = "852020"

def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))
 
def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))  

def acceptIncomingConnection():
    while True:
        client , clientAddr = server.accept()
        print("%s : %s has connected."% clientAddr)
        addresses[client] = clientAddr
        # print(client) # the whole data of connection
        # print(addresses[client]) # client IP addr
        Thread(target=handleClient,args=(client,)).start()
def handleClient(client):
    name = bytes.decode(decrypt(client.recv(bufsiz),password))
    clients[client] = name
    while True:
        connetionStart = bytes.decode(decrypt(client.recv(bufsiz),password))
        data = json.loads(connetionStart)
        if data["to"] == "//clientDisconnect":
            client.close()
            del clients[client]
            break
        

clients = {}
addresses = {}

while True:
    user = input("Enter Database username : ")
    dbpassword = input("Enter Password : ")
    try : 
        con = mc.connect(host="localhost",user=user,password=dbpassword)
        os.system('cls')
        break
    except :
        os.system('cls')
        print("Wrong Username or Password!")

cur = con.cursor()
cur.execute("show databases")
alldb = cur.fetchall()
if ("livechat",) not in alldb:
    cur.execute("create database livechat")
    cur.execute("use livechat")
cur.execute("use livechat")

cur.execute("show tables")
alltb = cur.fetchall()
if ("userinfo",) not in alltb:
    cur.execute("create table userinfo (id int primary key not null AUTO_INCREMENT, username varchar(100) not null, email varchar(100) not null, password varchar(50) not null,profile MEDIUMBLOB not null);")

cur.execute("select user from mysql.user")
alluser = cur.fetchall()
if ("bot",) not in alluser:
    cur.execute("create user bot@'%' identified by 'password';")
    cur.execute("GRANT ALL PRIVILEGES ON livechat.* TO 'bot'@'%';")

host = ""
port = 33000
bufsiz = 1024
addr = (host,port)
server = socket(AF_INET,SOCK_STREAM)
server.bind(addr)
print("Server IP : "+gethostbyname(gethostname()))
if __name__ == "__main__":
    server.listen(5)
    acceptThread = Thread(target=acceptIncomingConnection)
    acceptThread.start()
    acceptThread.join()
    server.close()